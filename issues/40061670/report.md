# UAF in search::(anonymous namespace)::NewTabURLDetails::ForProfile(Profile*)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061670](https://issues.chromium.org/issues/40061670) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Core, Internals>Sandbox>SiteIsolation, UI>Browser>Profiles |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2022-11-09 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

os version:ubuntu 22.04  

chromium version:  

[1]Chromium 108.0.5359.10  

[2]Chromium 109.0.5406.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1067909.zip)  

repro steps:  

Because it triggerd from chrome::ExitIgnoreUnloadHandlers()  

This issue needs to be triggered from chrome::ExitIgnoreUnloadHandlers() function, but I don't have a chromos device, so I chose other two alternatives in linux platform.  

The altanative repro-1:  

puppeteer's browser.close will chrome::ExitIgnoreUnloadHandlers(),I wrote a simple test script to achieve continuous automatic restart, execute crash.html, and close.

1. install puppeteer  
   
   export PUPPETEER\_SKIP\_CHROMIUM\_DOWNLOAD=true  
   
   npm install puppeteer
2. run custom http server  
   
   python3 -m http.server 8605 --dir=/home/pwn11/test
3. Modify the real path of crash.html and execute:  
   
   node ./test.js  
   
   In local tests, the browser can reproduce once about the 10th restart.

The altanative repro-2:  

Add the call of the chrome::ExitIgnoreUnloadHandlers() function directly after the post.  

repro-2 will trigger uaf immediately. I think this patch also make sense, please correct me if my understanding is wrong  

+#include "chrome/browser/lifetime/application\_lifetime.h"  

namespace pdf {

// static  

@@ -73,11 +76,17 @@ PdfNavigationThrottle::WillStartRequest() {  

params.is\_renderer\_initiated = false;  

params.is\_pdf = true;  

base::SequencedTaskRunnerHandle::Get()->PostTask(  

FROM\_HERE,  

base::BindOnce(  

[](base::WeakPtr[content::WebContents](javascript:void(0);) web\_contents,  

const content::OpenURLParams& params) {  

if (!web\_contents)  

return;  

// `MimeHandlerViewGuest` navigates its embedder for calls to  

@@ -92,6 +101,11 @@ PdfNavigationThrottle::WillStartRequest() {  

// non-`kPdfExtensionId` URL.  

},  

contents->GetWeakPtr(), std::move(params)));

- ```
   chrome::ExitIgnoreUnloadHandlers();  
  
  ```
  return CANCEL\_AND\_IGNORE;  
  
  }

**Problem Description:**

1. There is a uaf issue here(see <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/search/search.cc;drc=4a8573cb240df29b0e4d9820303538fb28e31d84;l=176>) , which can be triggered by chrome::ExitIgnoreUnloadHandlers()[see https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/lifetime/application\_lifetime.cc;bpv=1;bpt=1;l=86?q=chrome%2Fbrowser%2Flifetime%2Fapplication\_lifetime.cc].This code path can be triggered when Chrome is forced closed for a pending update, and trigger by default on ChromeOS(see <https://bugs.chromium.org/p/chromium/issues/detail?id=1370562#c3,if> you can't access this page,see <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_browser_main_posix.cc;drc=74e6b58d295dae0f6445e29f8ef0f1cb1d841684;l=129>).
2. When chrome::ExitIgnoreUnloadHandlers() triggered,the profile will be deleted[0](see <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile_impl.cc;drc=d74c6f83d652451bee76a40de988d19a2ac5f2cc;l=1011>).

void ProfileImpl::DestroyOffTheRecordProfile(Profile\* otr\_profile) {  

CHECK(otr\_profile);  

OTRProfileID profile\_id = otr\_profile->GetOTRProfileID();  

DCHECK(HasOffTheRecordProfile(profile\_id));  

otr\_profiles\_.erase(profile\_id); ==>[0]free profile  

#if BUILDFLAG(ENABLE\_EXTENSIONS)  

// Extensions are only supported on primary OTR profile.  

if (profile\_id == OTRProfileID::PrimaryID()) {  

ExtensionPrefValueMapFactory::GetForBrowserContext(this)  

->ClearAllIncognitoSessionOnlyPreferences();  

}  

#endif  

}

3. after callback end[1],OpenURLParams's destructor(content::~OpenURLParams()) will be called. The call chain as follows:  
   
   <0>content::OpenURLParams::~OpenURLParams()-><1>~SiteInstanceImpl()-><2>SiteInstanceImpl::ShouldUseProcessPerSite()-><3>search::(anonymous namespace)::NewTabURLDetails::ForProfile(Profile\*)  
   
   <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/site_instance_impl.cc;bpv=1;bpt=1;l=384?q=content%2Fbrowser%2Fsite_instance_impl.cc:386:34>  
   
   content::OpenURLParams params =  
   
   content::OpenURLParams::FromNavigationHandle(navigation\_handle());  
   
   params.url = original\_url.value();  
   
   params.transition = ui::PAGE\_TRANSITION\_AUTO\_SUBFRAME;  
   
   params.is\_renderer\_initiated = false;  
   
   params.is\_pdf = true;

base::SequencedTaskRunnerHandle::Get()->PostTask(  

FROM\_HERE,  

base::BindOnce(  

[](base::WeakPtr[content::WebContents](javascript:void(0);) web\_contents,  

const content::OpenURLParams& params) {  

if (!web\_contents)  

return; [1] web\_contents will be null, and trigger content::~OpenURLParams()  

// `MimeHandlerViewGuest` navigates its embedder for calls to  

// `WebContents::OpenURL()`, so use `LoadURLWithParams()` directly  

// instead.  

web\_contents->GetController().LoadURLWithParams(  

content::NavigationController::LoadURLParams(params));

```
        // Note that we don't need to register the stream's URL loader as a  
        // subresource, as `MimeHandlerViewGuest::ReadyToCommitNavigation()`  
        // will handle this as soon as we navigate to a  
        // non-`kPdfExtensionId` URL.  
      },  
      contents->GetWeakPtr(), std::move(params)));  

in call chain<2>,Get the previously freed profile pointer again[2]，and eventually uaf will be triggered[0].  
bool SiteInstanceImpl::ShouldUseProcessPerSite() const {  
    BrowserContext\* browser_context = browsing_instance_->GetBrowserContext(); [2]  
return has_site_ && site_info_.ShouldUseProcessPerSite(browser_context);  
}  
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/site_instance_impl.cc;drc=7d286973e02b87e66ea0893e9b5e4093e908976b;l=384  

```

**Additional Comments:**

\*\*Chrome version: \*\* 108.0.5359.10 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [test.js](attachments/test.js) (text/plain, 804 B)
- [test.pdf](attachments/test.pdf) (application/pdf, 11 B)
- [crash.html](attachments/crash.html) (text/plain, 528 B)
- [asan.log](attachments/asan.log) (text/plain, 27.8 KB)

## Timeline

### [Deleted User] (2022-11-09)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-09)

Thanks for your report. I think this could only be hit in practice in ash, like you said (chrome os). I'm passing it to the Chrome OS folks to take a look.

[Monorail components: Internals>Core UI>Browser>Profiles]

### ps...@google.com (2022-11-10)

@mahmadi - can you take a look, and re-route if you are not the right owner?

### ps...@google.com (2022-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-10)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-10)

It looks to be like the code might go back before 108, are you sure this regression started in 108?

reporter: can you check this on 107.0.5304.x and 106.0.5249.x?

### em...@gmail.com (2022-11-10)

Both versions can be reproduced, but it feels that it takes a little longer to reproduce in version 106.0.5249.12.
tested versions:
Chromium 106.0.5249.12(gs://chromium-browser-asan/linux-release/asan-linux-release-1036826.zip)
Chromium 107.0.5304.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1047791.zip) 


### [Deleted User] (2022-11-11)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-11)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-11)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-11)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-11)

Sorry to step in here, but security bugs cannot go without owners. mahmadi@, if you are not the correct owner for this please re-route it to someone more appropriate to own this issue. Thank you.

### ma...@chromium.org (2022-11-11)

I don't work on CrOS and I'm not familiar with trace in the description. Assigning back to CrOS security owners for bisect and triage. 

### [Deleted User] (2022-11-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-12)

[Empty comment from Monorail migration]

### ps...@google.com (2022-11-14)

@tiborg: you are listed as the owner of chrome/browser/search/search.cc - can you take a look and route appropriately?


### ti...@chromium.org (2022-11-15)

IIUC, we get passed a dangling Profile pointer in NewTabURLDetails::ForProfile. If so, I don't think this can be fixed well in //chrome/browser/search/search.cc. Rather, we should not invoke search::ShouldUseProcessPerSiteForInstantSiteURL at [1]. Passing to lukasza@, one of the site isolation owners, to investigate or route further.


[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_content_browser_client.cc;l=1915?q=ShouldUseProcessPerSite%20file:cc%20-file:test&sq=-file:%5Eout%2F

### lu...@chromium.org (2022-11-15)

alexmos@, can you PTAL?  I would trust you more than myself with figuring out the best way to proceed here.

It seems to me that the problem here is that SiteInstanceImpl (a ref-counted class) can refer to an already-destroyed/dangling BrowserContext (via SiteInstanceImpl::browsing_instance_ => BrowsingInstance::isolation_context_ => IsolationContext::browser_or_resource_context_ => BrowserOrResourceContext::union_::browser_context_).

It is possible to subscribe to BrowserContextShutdownNotifierFactory's notifications about BrowserContext getting destroyed.  See: https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/extension_protocols.cc;l=973-978;drc=49f9d9415a5616b6061daa80eb3c737f5e2e8253.  Still, what can/should SiteInstanceImpl/BrowsingInstance/IsolationContext do at such time?  Since SiteInstanceImpl is ref-counted, it needs to remain alive (right?) in an inert/no-op state.

Another aspect to consider is whether a SiteInstance / BrowsingInstance / IsolationContext can be created when BrowserContext::ShutdownStarted().  And if so, then what should be done at that point (constructors are infallible, maybe the caller of the constructor should have errored out earlier?).

[Monorail components: Internals>Sandbox>SiteIsolation]

### lu...@chromium.org (2022-11-15)

Other thoughts:

- BrowserContextShutdownNotifierFactory and BrowserContextKeyedServiceShutdownNotifierFactory are not available in the //content layer.  I don't know if there is a separate, //content-layer-friendly mechanism to get notified about BrowserContext destruction.  If not, then maybe something can be hooked up to BrowserContextImpl::NotifyWillBeDestroyed.

- It seems difficult to require that //chrome layer deletes all references to SiteInstances before destroying the BrowserContext.  In particular, it seems quite natural that OpenURLParams (which include `scoped_refptr<SiteInstance>`) are bound as a parameter of a posted task - the "posting" may happen while BrowserContext is still alive, and the "running" (or dropping of the task) can happen after BrowserContext destruction.

### da...@chromium.org (2022-11-15)

Chatted with lukasza and have some thoughts from there.

1. A refcounted type (scoped_refptr<SiteInstance>) which has a non-owning pointer to something else is fraught. This introduces a lifetime relationship that is inherently changeable at runtime (by holding a reference). This makes it unreasonable for a developer to be able to write code without introducing a lifetime-related bug that results in a crash.

2. Removing refcounting from SiteInstance seems hard or wrong even perhaps.

3. Yes, we could make Chrome crash when this goes wrong without being a security bug. We should advocate for improving security without indoctrinating crashes into the system, which cause low reliability for users, and hurt our top level goals of users loving and using Chrome.

4. We have a systemic issue in Chrome right now wrt BrowserContext/Profile and lifetimes. Security sheriffs are being swamped with bug reports of things owned by Profile (KeyedService) posting tasks with pointers that are destroyed by Profile destruction. This is yet another shape of the same problem.

The general shape of the problem is pointers attached to the lifetime of a profile being stored in tasks that outlive the profile. The DanglingPointerDetector could catch these bugs and surface them very visibly to developers for them to resolve them. It does so by crashes though, and we need a systematic thing to solve the problem once the DPD uncovers them. What shape should the solution have?

It feels like a task graph scheduling problem, in a way. We have a lot of frame-associated tasks, or web contents associated, or profile associated. And those tasks should not run past the lifetime of the associated thing. Our only mechanism to do that now is to make them all be methods on the associated thing and then WeakPtr. Yet that doesn't scale to posting tasks in the wide array of frame/webcontents/profile-associated types.

+gab for this.

5. It is generally better to make errors visible in the code, so I think maybe we should stop holding a BrowserContext pointer in SiteInstance (see 1) and replace it with something that can obviously fail if you've outlived the BrowserContext, in lieu of a more wholistic answer to tasks with expired pointers running.

### lu...@chromium.org (2022-11-16)

In a discussion with creis@ and alexmos@ earlier today, it was pointed out that the callback should *not* run after BrowserContext/Profile destruction.  This is indeed what is happening here - the callback *is* getting cancelled (because of the first argument - WeakPtr<WebContents>;  this bug report does point out that "web_contents will be null, and trigger content::~OpenURLParams()").  But cancellation of the callback is not sufficient to prevent UaF - the problem is that SiteInstanceImpl's destructor can be called when the BrowserContext/Profile is gone, but doesn't handle this situation in a robust way.

Examples of how SiteInstanceImpl's destructor may dereference dangling pointers when called after BrowserContext destruction:

1. ~SiteInstanceImpl => SiteInstanceGroup::RemoveSiteInstance => `process_->Cleanup()` (AFAIU `process_` may be dangling after BrowserContext destruction?)
2. ~SiteInstanceImpl => ContentBrowserClient::SiteInstanceDeleting
2.1. This is arbitrary code, so calling it in such a sensitive situation seems risky
2.2. ChromeContentBrowserClient::SiteInstanceDeleting => SiteInstanceImpl::HasProcess
2.2.1. SiteInstanceImpl::HasProcess => SiteInstanceImpl::ShouldUseProcessPerSite [this is the focus of this bug report - this may deference a dangling BrowserContext pointer]
2.2.2. SiteInstanceImpl::HasProcess => RenderProcessHostImpl::GetSoleProcessHostForSite [called with a dangling isolation context AFAIU]


### lu...@chromium.org (2022-11-16)

2.3. ChromeContentBrowserClient::SiteInstanceDeleting => ChromeContentBrowserClientExtensionsPart::SiteInstanceDeleting
2.3.1. Gets the (potentially dangling) BrowserContext pointer as the very first thing


### al...@chromium.org (2022-11-16)

Thanks for looking at this so far, lukasza@.  Adding a couple more thoughts:

1. I don't think it make sense to allow a SiteInstance to ever outlive its profile, just like it doesn't make sense to have WebContents, RFH, RPH, etc outlive their profile.  The primary things that should keep SiteInstance alive are references in RenderFrameHost, RenderFrameProxyHost, workers, and (Frame)NavigationEntries.  I'd expect all of these to go away when the respective WebContents goes away, which should be triggered prior to the profile going away. Here, it seems the WebContents has gone away, but the SiteInstance is kept alive by OpenURLParams::source_site_instance.  Do we actually need that reference to source_site_instance in OpenURLParams?  I tried looking at how it's used and didn't really find much beyond using it to determine the BrowserContext in a couple of places like [1] and [2], which we could probably plumb through in a different way.  Maybe we can remove OpenURLParams::source_site_instance, since that does complicate reasoning about what can keep a SiteInstance alive?

2.  IIUC, we have a PostTask to start a navigation which runs after the profile in which to start that navigation has been destroyed.  (It checks for this via the WC weakptr, but that's unfortunately not enough due to the SiteInstance reference in OpenURLParams.)  Can we set up this PostTask in such a way that it's canceled earlier, when we first know the profile is going to go away?

3. I'm not sure we can change SiteInstance to not be refcounted.  There might be room to retrieve the BrowserContext in a different way, rather than storing a pointer to it in BrowsingInstance/IsolationContext, e.g. via RenderProcessHost::GetBrowserContext().  But unfortunately that is also based on storing a pointer, so I'm not sure that's going to be any better.

4. Re: making SiteInstance destructor resilient to having a Profile that's already been destroyed - maybe that can be a short-term solution, but it'd be nice to avoid ever getting into such a situation in the first place.  Supporting something like this makes reasoning about lifetimes even more complicated, especially since this is exposed outside of content via SiteInstanceDeleting.  I also agree about the potentially dangling reference to a SiteInstance's process, and I also worry about things that will be kept alive by the SiteInstance, like BrowsingInstance and SiteInstanceGroup and the stuff inside those classes.

5. I think creis@ had a proposal in a different context to not actually free anything when the whole browser is shutting down, as that just creates unnecessary work.  This might be helpful for mitigating UAFs in cases like this. Charlie, is there a reference to this?

6. creis@ and I were chatting about how reproducible this might be. It doesn't seem like an attacker could trigger a whole browser shutdown like this from JS, and I'm not sure one could even trigger an OTR profile destruction, as we can some checks on when a window can be self-closed that should prevent that.  So that should limit the exploitability of this.


[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator_params.cc;l=65;drc=addb7782cec77e05c29617541c3275bd57eb3189

[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator.cc;l=434;drc=addb7782cec77e05c29617541c3275bd57eb3189.


### al...@chromium.org (2022-11-16)

+yangsharon@ who's already looked into removing OpenURLParams::source_site_instance (as part of SiteInstanceGroup work) and mentioned it might be complicated, unfortunately.

### lu...@chromium.org (2022-11-17)

RE: https://crbug.com/chromium/1382761#c25: alexmos@: 1: The primary things that should keep SiteInstance alive are references in RenderFrameHost, RenderFrameProxyHost, workers, and (Frame)NavigationEntries

I note that the things listed above seem to all be //content-internal.  Therefore I wonder if we can avoid leaking SiteInstance's ref-count-ability over //content/public API?  (similarly to RenderProcessHost?  hopefully without having to roll an ad-hoc ref-counting scheme like RPH does).

Otherwise (i.e. if we continue exposing ref-count-ability via //content/public API) even if we get rid of OpenURLParams::source_site_instance, then inevitably other `scoped_refptr<SiteInstance>` cases might pop up in other posted tasks.

Hiding ref-count-ability from //content/public API would probably require reworking how long-lived SiteInstance references are represented above the //content layer.  `scoped_refptr<SiteInstance>` would no longer be possible.  Maybe we could/should introduce a SiteInstanceId to use in such cases?


RE: https://crbug.com/chromium/1382761#c25: alexmos@: 5/6: whole browser shutdown

Maybe I misunderstood, but AFAIU the repro does *not* require shutting down the whole browser - it only requires a single profile going away (e.g. closing an incognito window).

### da...@chromium.org (2022-11-17)

> 5. I think creis@ had a proposal in a different context to not actually free anything when the whole browser is shutting down, as that just creates unnecessary work.  This might be helpful for mitigating UAFs in cases like this. Charlie, is there a reference to this?

Profiles can be destroyed in other contexts than browser shutdown, so if this isn't more strongly tied to shutdown than I understand it to be, this won't solve the issue.

### da...@chromium.org (2022-11-17)

> I note that the things listed above seem to all be //content-internal.  Therefore I wonder if we can avoid leaking SiteInstance's ref-count-ability over //content/public API?  (similarly to RenderProcessHost?  hopefully without having to roll an ad-hoc ref-counting scheme like RPH does).

> Hiding ref-count-ability from //content/public API would probably require reworking how long-lived SiteInstance references are represented above the //content layer.  `scoped_refptr<SiteInstance>` would no longer be possible.  Maybe we could/should introduce a SiteInstanceId to use in such cases?


Right, if the pointer is in the API, or can be retrieved from the SiteInstanceId, then its refcounting would be known, since the ref-countability is part of the type and we allow constructing a scoped_refptr<T> from a native T* pointer. All of this is sad... but yeah.

But if we had a different type that was used in the public API and isn't refcounted that would hide it.

### da...@chromium.org (2022-11-17)

> 4. Re: making SiteInstance destructor resilient to having a Profile that's already been destroyed - maybe that can be a short-term solution, but it'd be nice to avoid ever getting into such a situation in the first place.  Supporting something like this makes reasoning about lifetimes even more complicated, especially since this is exposed outside of content via SiteInstanceDeleting.  I also agree about the potentially dangling reference to a SiteInstance's process, and I also worry about things that will be kept alive by the SiteInstance, like BrowsingInstance and SiteInstanceGroup and the stuff inside those classes.

Also want to big +1 this I really appreciate this.

### ob...@google.com (2022-11-18)

Hello-

Thank you for the activity on this, as this is marked ReleaseBlock-Stable for M-108, a reminder that we promote to Stable on 12/01 which is just after the holiday next week.

### al...@chromium.org (2022-11-19)

+kmoon@, +thestig@ as FYI since the PdfNavigationThrottle's PostTask to schedule a navigation is at the center of this.

A few updates after spending some more time on this today.  I've verified I can repro this locally, using the second approach of calling chrome::ExitIgnoreUnloadHandlers() after the PostTask.  So far, I couldn't repro this with anything but hard browser shutdown done by ExitIgnoreUnloadHandlers.  For example, it seems that the typical incognito shutdown path is a bit more asynchronous, and if I start it just after scheduling the task, the posted task manages to run after the WebContents has shut down but before the profile gets destroyed yet (so things are fine).  I'm not very familiar with the intricacies of browser shutdown, though, and it might still be entirely possible with the right interleaving of tasks.

I've chatted with yangsharon@ about removing source_site_instance from OpenURLParams, which would be an ideal solution and would also help SiteInstanceGroups, but that's quite an involved effort with some tricky dependencies that we'd need to figure out.  For example, we tried removing it from just one dependency in https://chromium-review.googlesource.com/c/chromium/src/+/3449332 but even that one didn't work out.  So while this might be something we could do eventually, this approach is unlikely to be practical in the short term.

Another idea that came up was to keep SiteInstance refcounted within //content but hide this outside of //content (perhaps excluding tests).  Instead, fields like OpenURLParams::source_site_instance could use SiteInstanceId and then we could introduce an ability to convert that ID back to a SiteInstance and do a null check at that point.  That still sounds fairly far-reaching and not very mergeable.

I also noticed that this problem may be possible in other places that PostTask a navigation with OpenURLParams, in particular PDFIFrameNavigationThrottle::LoadPlaceholderHTML() in [1].  (I don't recall when that's used - I think it might be when the PDF viewer is unavailable?)  Interestingly, this uses a helper class (PdfWebContentsLifetimeHelper) tied to the WebContents lifetime for the task, so the task won't run at all once the helper object goes away, unlike PdfNavigationThrottle where it runs but exits right away due to the null WebContents weakptr.  Unfortunately, that doesn't prevent the bug from happening, as the task still sits around in the task queue with the bound OpenURLParams, even after we've invalidated the PdfWebContentsLifetimeHelper and after the profile is destroyed.  We only destroy the task and its OpenURLParams once we get to it in the queue, which is too late (see WorkQueue::RemoveAllCancelledTasksFromFrontImpl).  I don't know if we have any options for destroying the task and its params sooner in a case like this?  gab@, any thoughts?

I guess we could do something along option (2) from https://crbug.com/chromium/1382761#c25 if we make the task cancelable (e.g., with base::CancelableTaskTracker) and then cancel/destroy it when the BrowserContext is being destroyed, rather than waiting for the task to go away later.  We could introduce an API somewhere in content/public for doing this, which would allow scheduling navigations without the risk of the posted task outliving the BrowserContext.

In the very short term, though, given https://crbug.com/chromium/1382761#c31 I think there's a workaround we could put in place while we discuss and explore more systematic options such as those above.  For PdfNavigationThrottle, the source_site_instance in OpenURLParams should always point to the PDF extension in the main frame (we know that the extension always creates and navigates a subframe in the MimeHandlerView guest WebContents to the PDF URL).  We could just clear source_site_instance from OpenURLParams before posting the task.  Then, if the task runs and the WebContents is still there, we could fill in the source_site_instance from web_contents->GetPrimaryMainFrame()->GetSiteInstance() before proceeding with LoadURLWithParams().  Or, alternatively, we could just leave source_site_instance unassigned, since I'm not sure we even need it (technically, this is a browser-initiated navigation, and it doesn't involve data/about URLs which typically use source_site_instance).  This should be a small fix and easily mergeable.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/plugins/pdf_iframe_navigation_throttle.cc;l=167;drc=bfb8c49dbe07823ef4ebf1a857be9a4d288d1120

### km...@chromium.org (2022-11-21)

The quick fix SGTM; I assume we have test coverage that would fail if messing with source_site_instance was a problem.

### al...@chromium.org (2022-11-22)

After quite a bit of exploration I think I've managed to write a test for this (WIP CL at https://chromium-review.googlesource.com/c/chromium/src/+/4043432).  One thing I noticed is that in the test the issue is actually first caught when ChromeContentBrowserClient::ShouldUseProcessPerSite() uses Profile::FromBrowserContext(), where we have logic that tracks all valid BrowserContexts to verify that a BrowserContext can be converted to a Profile [1].  That logic is currently behind a DCHECK and intended to catch incorrect casts in tests, so if DCHECKs are off then we'll hit the repro with a UAF.  So as another improvement we should consider expanding the use of [1] outside of tests to maybe catch issues like this a bit earlier, before the UAF actually happens.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile.cc;l=243-257;drc=7473aada23e43186bbbd4491f8f7f5630e34e109

### ob...@google.com (2022-11-22)

Is this fix addressing a crash and or a security issue? Would like to know how to manage this as we are promoting to Stable in about a week.

### gi...@appspot.gserviceaccount.com (2022-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9f9db7e8406998b525d5fa1786800ce2e3fc3215

commit 9f9db7e8406998b525d5fa1786800ce2e3fc3215
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Tue Nov 22 22:11:57 2022

Reset source SiteInstance before scheduling PDF navigations in subframes.

This CL fixes a SiteInstance/BrowserContext lifetime issue in
PdfNavigationThrottle::WillStartRequest(), which cancels certain
subframe PDF navigations and schedules replacement navigations with
slightly tweaked params via a PostTask.  The PostTask takes in
OpenURLParams, which contains the source SiteInstance in a
scoped_refptr.  Unfortunately, https://crbug.com/chromium/1382761 shows that the
BrowserContext can get destroyed after the task is scheduled but
before it runs, and even though the task uses a WebContents WeakPtr to
return early in that case, the task's OpenURLParams would only get
destroyed and decrement the source SiteInstance's refcount at the time
of that early return, which is already after the BrowserContext is
destroyed.  When the (source) SiteInstance destructor runs and tries
to use the SiteInstance's BrowserContext, things blow up.

As a short-term fix, we can avoid keeping the source SiteInstance
alive longer than its BrowserContext by not passing it through
OpenURLParams, but rather setting it directly when the task runs.
This is possible because in this case the source SiteInstance should
always be the SiteInstance of the PDF extension loaded in the guest's
main frame.

Longer-term, we should find a more systematic way to fix these
problems, for example by not exposing refcounting of SiteInstances
outside of //content or introducing an API for scheduling navigations
that is robust against BrowserContext destruction.  See the bug for
more details and other ideas.

Bug: 1382761
Change-Id: I88370a1bc0700d2a49553b9d3b1ecbaf5ce62cb0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4043432
Reviewed-by: K. Moon <kmoon@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1074889}

[modify] https://crrev.com/9f9db7e8406998b525d5fa1786800ce2e3fc3215/content/public/test/mock_navigation_handle.h
[modify] https://crrev.com/9f9db7e8406998b525d5fa1786800ce2e3fc3215/components/pdf/browser/pdf_navigation_throttle.cc
[modify] https://crrev.com/9f9db7e8406998b525d5fa1786800ce2e3fc3215/components/pdf/browser/pdf_navigation_throttle_unittest.cc
[modify] https://crrev.com/9f9db7e8406998b525d5fa1786800ce2e3fc3215/chrome/browser/pdf/pdf_extension_test.cc


### al...@chromium.org (2022-11-23)

I've filed https://crbug.com/chromium/1393148 for all the followup work that was discussed in this issue.  The immediate security issue should now be fixed by r1074889.  

https://crbug.com/chromium/1382761#c35: this is a security issue, not a crash. Updating OS labels - I think this affects all desktop platforms, but not Android (since PdfNavigationThrottle isn't used on Android IIUC).

### [Deleted User] (2022-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-24)

Requesting merge to beta M108 because latest trunk commit (1074889) appears to be after beta branch point (1058933).

Requesting merge to dev M109 because latest trunk commit (1074889) appears to be after dev branch point (1070088).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-24)

Merge approved: your change passed merge requirements and is auto-approved for M109. Please go ahead and merge the CL to branch 5414 (refs/branch-heads/5414) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-24)

Merge review required: M108 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-11-28)

Responding to https://crbug.com/chromium/1382761#c42:

1. Why does your merge fit within the merge criteria for these milestones?
Fixes a medium severity security issue.

2. What changes specifically would you like to merge? Please link to Gerrit.
r1074889

3. Have the changes been released and tested on canary?
Yes, r1074889 went out in 110.0.5435.0.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No


### pb...@google.com (2022-11-28)

[Bulk Edit] This merge has been approved for M109, please help complete your merges asap (before 4pm PST) today, so the change can be included in this week's RC build for dev/beta releases

### gi...@appspot.gserviceaccount.com (2022-11-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8255f4190823fe704c4a16694a2ab16b510b8cb1

commit 8255f4190823fe704c4a16694a2ab16b510b8cb1
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Mon Nov 28 21:35:44 2022

[M109] Reset source SiteInstance before scheduling PDF navigations in subframes.

This CL fixes a SiteInstance/BrowserContext lifetime issue in
PdfNavigationThrottle::WillStartRequest(), which cancels certain
subframe PDF navigations and schedules replacement navigations with
slightly tweaked params via a PostTask.  The PostTask takes in
OpenURLParams, which contains the source SiteInstance in a
scoped_refptr.  Unfortunately, https://crbug.com/chromium/1382761 shows that the
BrowserContext can get destroyed after the task is scheduled but
before it runs, and even though the task uses a WebContents WeakPtr to
return early in that case, the task's OpenURLParams would only get
destroyed and decrement the source SiteInstance's refcount at the time
of that early return, which is already after the BrowserContext is
destroyed.  When the (source) SiteInstance destructor runs and tries
to use the SiteInstance's BrowserContext, things blow up.

As a short-term fix, we can avoid keeping the source SiteInstance
alive longer than its BrowserContext by not passing it through
OpenURLParams, but rather setting it directly when the task runs.
This is possible because in this case the source SiteInstance should
always be the SiteInstance of the PDF extension loaded in the guest's
main frame.

Longer-term, we should find a more systematic way to fix these
problems, for example by not exposing refcounting of SiteInstances
outside of //content or introducing an API for scheduling navigations
that is robust against BrowserContext destruction.  See the bug for
more details and other ideas.

(cherry picked from commit 9f9db7e8406998b525d5fa1786800ce2e3fc3215)

Bug: 1382761
Change-Id: Ie24e12534c0c8a990c62279a45f7211d2a93a212
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4043432
Reviewed-by: K. Moon <kmoon@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1074889}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4060150
Cr-Commit-Position: refs/branch-heads/5414@{#266}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/8255f4190823fe704c4a16694a2ab16b510b8cb1/content/public/test/mock_navigation_handle.h
[modify] https://crrev.com/8255f4190823fe704c4a16694a2ab16b510b8cb1/components/pdf/browser/pdf_navigation_throttle.cc
[modify] https://crrev.com/8255f4190823fe704c4a16694a2ab16b510b8cb1/chrome/browser/pdf/pdf_extension_test.cc
[modify] https://crrev.com/8255f4190823fe704c4a16694a2ab16b510b8cb1/components/pdf/browser/pdf_navigation_throttle_unittest.cc


### am...@chromium.org (2022-11-30)

M108 merge approved, please merge this fix to branch 5359 at your earliest convenience. 

### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### gi...@appspot.gserviceaccount.com (2022-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/282f304f66147236c0816d66364fc6b45724e5ca

commit 282f304f66147236c0816d66364fc6b45724e5ca
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Fri Dec 02 18:24:10 2022

[M108] Reset source SiteInstance before scheduling PDF navigations in subframes.

This CL fixes a SiteInstance/BrowserContext lifetime issue in
PdfNavigationThrottle::WillStartRequest(), which cancels certain
subframe PDF navigations and schedules replacement navigations with
slightly tweaked params via a PostTask.  The PostTask takes in
OpenURLParams, which contains the source SiteInstance in a
scoped_refptr.  Unfortunately, https://crbug.com/chromium/1382761 shows that the
BrowserContext can get destroyed after the task is scheduled but
before it runs, and even though the task uses a WebContents WeakPtr to
return early in that case, the task's OpenURLParams would only get
destroyed and decrement the source SiteInstance's refcount at the time
of that early return, which is already after the BrowserContext is
destroyed.  When the (source) SiteInstance destructor runs and tries
to use the SiteInstance's BrowserContext, things blow up.

As a short-term fix, we can avoid keeping the source SiteInstance
alive longer than its BrowserContext by not passing it through
OpenURLParams, but rather setting it directly when the task runs.
This is possible because in this case the source SiteInstance should
always be the SiteInstance of the PDF extension loaded in the guest's
main frame.

Longer-term, we should find a more systematic way to fix these
problems, for example by not exposing refcounting of SiteInstances
outside of //content or introducing an API for scheduling navigations
that is robust against BrowserContext destruction.  See the bug for
more details and other ideas.

(cherry picked from commit 9f9db7e8406998b525d5fa1786800ce2e3fc3215)

Bug: 1382761
Change-Id: I9a08847e05cfca85eb4f9f2a5bb95815e90c6042
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4043432
Reviewed-by: K. Moon <kmoon@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1074889}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4073806
Cr-Commit-Position: refs/branch-heads/5359@{#1066}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/282f304f66147236c0816d66364fc6b45724e5ca/components/pdf/browser/pdf_navigation_throttle.cc
[modify] https://crrev.com/282f304f66147236c0816d66364fc6b45724e5ca/content/public/test/mock_navigation_handle.h
[modify] https://crrev.com/282f304f66147236c0816d66364fc6b45724e5ca/components/pdf/browser/pdf_navigation_throttle_unittest.cc
[modify] https://crrev.com/282f304f66147236c0816d66364fc6b45724e5ca/chrome/browser/pdf/pdf_extension_test.cc


### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-12)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-14)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1382761?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Core, Internals>Sandbox>SiteIsolation, UI>Browser>Profiles]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061670)*
