# Security: OfflinePageAutoFetcher UAF 2

| Field | Value |
|-------|-------|
| **Issue ID** | [40050032](https://issues.chromium.org/issues/40050032) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Offline |
| **Platforms** | Android |
| **Reporter** | bt...@gmail.com |
| **Assignee** | ha...@google.com |
| **Created** | 2019-09-02 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

Under the covers, when AddInterface is called with a task runner (<https://cs.chromium.org/chromium/src/chrome/browser/chrome_content_browser_client.cc?l=4423&rcl=7acee7ba237db6175a22c18183556c1858b5fcb8>) it ends up posting the `BindInterface` callback to the task runner (<https://cs.chromium.org/chromium/src/services/service_manager/public/cpp/interface_binder.h?l=65&rcl=7acee7ba237db6175a22c18183556c1858b5fcb8>). This can lead to race conditions when passing raw pointers as a callback argument to the `BindInterface` whenever DeleteOnThread isn't used.

The first obvious use of this vulnerable code pattern I came across was in OfflinePageAutoFetcher.

```
#if defined(OS_ANDROID)  
 frame_interfaces_parameterized_->AddInterface( /\*\*\* RFHI raw pointer \*\*\*/  
     base::BindRepeating(&offline_pages::OfflinePageAutoFetcher::Create),  
     base::CreateSingleThreadTaskRunner({BrowserThread::UI})); /\*\*\* \*Post to UI Thread\*\*/  
#endif  

```

OfflinePageAutoFetcher::Create is posted to the UI thread, which is racy with the destruction of RenderFrameHost. This can lead to a Use-After-Free.

```
OfflinePageAutoFetcher::OfflinePageAutoFetcher(  
   content::RenderFrameHost\* render_frame_host)  
   : last_committed_url_(render_frame_host->GetLastCommittedURL()) { /\*\*\* UAF \*\*\*/  
 TabAndroid\* tab = FindTab(render_frame_host);  
 if (!tab) {  
   return;  
 }  
 auto_fetcher_service_ =  
     OfflinePageAutoFetcherServiceFactory::GetForBrowserContext(  
         render_frame_host->GetProcess()->GetBrowserContext());  
 android_tab_id_ = tab->GetAndroidId();  
}  

```

This vulnerability was present before the last report I made - I missed it on my first audit :(. Setting up the race is slightly different as we need to flood the UI thread with messages this time in order to win the race reliably

Recommended Fix: Pass the renderer process id and routing id. Safe example here <https://cs.chromium.org/chromium/src/chrome/browser/speech/chrome_speech_recognition_manager_delegate.cc?l=106&rcl=a25cb96624aa6d8f85e53794eb7c4114f150051d>

This somewhat scary code pattern that could have also been used to trigger <https://bugs.chromium.org/p/chromium/issues/detail?id=912520> without reloading the page manually.

**VERSION**  

Chrome Version: 78.0.3901.0 asan build  

Chrome Version: 76.0.3809.132 release build  

Operating System: Android  

<https://cs.chromium.org/chromium/src/chrome/browser/chrome_content_browser_client.cc?l=4422&rcl=e612cceca48a4fef25160da175a2a2038d3a76f3>  

Test Device 1: Android 9: Pixel3 Build/PQ2A.190205.001  

Test Device 2: Android 9: Pixel2 Build/PPR2.180905.005

**REPRODUCTION CASE**

Setup  

\* Build chromium for android and install chrome\_public\_apk  

\* Enable "command line flags on non rooted" to use MojoJS (<https://www.chromium.org/developers/how-tos/run-chromium-with-flags#TOC-Android>)  

\* Set the flag --enable-blink-features=MojoJS  

\* out/arm64.release/bin/chrome\_public\_apk argv --args=' --enable-blink-features=MojoJS'  

\* Relaunch chromium and ensure enable-blink-features=MojoJS is enabled in chrome://version

Step 1  

Use my generated JS mojo bindings (should work with head)  

$ tar xvf repro.tar.gz  

or  

$ cp -r /path/to/chrome/.../out/Asan/gen .  

and generate the offline\_page\_auto\_fetcher.mojom.js file yourself by moving the mojom file to its own directory or grab it from codesearch <https://cs.chromium.org/chromium/src/out/android-Debug/gen/chrome/common/offline_page_auto_fetcher.mojom.js>

Step 2  

$ cd repro  

$ python -m SimpleHTTPServer 8000

Step 3  

Browse to hostname:8000/race.html

Note: It is easy to understand the root cause of this issue without an Android setup device by applying a small patch to any of the calls to AddInterface in chrome\_content\_browser\_client.cc and modifying the poc slightly to call these interfaces instead. For example, modifying BadgeManager::BindRequest to post to the UI thread.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

```
#if !defined(OS_ANDROID)  
  frame_interfaces_parameterized_->AddInterface(  
      base::BindRepeating(&badging::BadgeManager::BindRequest),  
+++ base::CreateSingleThreadTaskRunner({BrowserThread::UI}));  
#endif  

```

==7621==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x0057f4b83080 at pc 0x006f0e59a960 bp 0x007fca2ad1d0 sp 0x007fca2ad1c8  

READ of size 8 at 0x0057f4b83080 thread T0 (chromium.chrome)  

#0 offline\_pages::OfflinePageAutoFetcher::OfflinePageAutoFetcher(content::RenderFrameHost\*) ./../../chrome/browser/offline\_pages/android/offline\_page\_auto\_fetcher.cc:43  

#1 std::\_\_1::\_\_unique\_if<offline\_pages::OfflinePageAutoFetcher>::\_\_unique\_single std::\_\_1::make\_unique<offline\_pages::OfflinePageAutoFetcher, content::RenderFrameHost\*&>(content::RenderFrameHost\*&) ./../../buildtools/third\_party/libc++/trunk/include/memory:3131  

#2 offline\_pages::OfflinePageAutoFetcher::Create(mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*) ./../../chrome/browser/offline\_pages/android/offline\_page\_auto\_fetcher.cc:80  

#3 void base::internal::FunctorTraits<void (\*)(mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*), void>::Invoke<void (\* const&)(mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*), mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*>(void (\* const&)(mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*), mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);)&&, content::RenderFrameHost\*&&) ./../../base/bind\_internal.h:399  

#4 void base::internal::InvokeHelper<false, void>::MakeItSo<void (\* const&)(mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*), mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*>(void (\* const&)(mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*), mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);)&&, content::RenderFrameHost\*&&) ./../../base/bind\_internal.h:599  

#5 base::RepeatingCallback<void (mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*)>::Run(mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*) const & ./../../base/callback.h:132  

#6 void base::internal::FunctorTraits<void (\*)(base::RepeatingCallback<void (mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*)> const&, mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*), void>::Invoke<void (\*)(base::RepeatingCallback<void (mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*)> const&, mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*), base::RepeatingCallback<void (mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*)>, mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*>(void (\*&&)(base::RepeatingCallback<void (mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*)> const&, mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*), base::RepeatingCallback<void (mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);), content::RenderFrameHost\*)>&&, mojo::InterfaceRequest[chrome::mojom::OfflinePageAutoFetcher](javascript:void(0);)&&, content::RenderFrameHost\*&&) ./../../base/bind\_internal.h:399  

#7 base::OnceCallback<void ()>::Run() && ./../../base/callback.h:98  

#8 base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:365  

#9 base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219  

#10 base::MessagePumpForUI::OnNonDelayedLooperCallback() ./../../base/message\_loop/message\_pump\_android.cc:194  

#11 base::(anonymous namespace)::NonDelayedLooperCallback(int, int, void\*) ./../../base/message\_loop/message\_pump\_android.cc:70  

#12 0x6fb7e23474 (/system/lib64/libutils.so+0x14474)  

#13 0x6fb7e2308c (/system/lib64/libutils.so+0x1408c)  

#14 0x6fb93b9c2c (/system/lib64/libandroid\_runtime.so+0x120c2c)  

#15 0x74c0e69c (/dev/ashmem/dalvik-jit-code-cache (deleted)+0xe69c)

Address 0x0057f4b83080 is a wild pointer.  

SUMMARY: AddressSanitizer: heap-buffer-overflow (/data/app/org.chromium.chrome-E0w-UtJeh42LDRxTRKHucA==/lib/arm64/libchrome.so+0x1344d95c)  

Shadow bytes around the buggy address:  

0x001afe9705c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x001afe9705d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x001afe9705e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x001afe9705f0: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa fa  

0x001afe970600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x001afe970610:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x001afe970620: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x001afe970630: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x001afe970640: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x001afe970650: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x001afe970660: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

Shadow gap: cc  

==7621==ABORTING

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Brendon Tiszka

## Attachments

- [repro.tar.gz](attachments/repro.tar.gz) (application/octet-stream, 4.2 MB)

## Timeline

### ct...@chromium.org (2019-09-03)

Thanks for the detailed report and for including a recommended fix! Setting Severity-High (memory corruption in browser process accessible via compromised renderer) and Impact-Stable.

harringtond@ can you please look into this high severity security bug? Thanks!

[Monorail components: UI>Browser>Offline]

### bt...@gmail.com (2019-09-03)

We might be able to come up with a more systemic fix, which would prevent this class from happening in the future, by changing the `bindargs` for `frame_interfaces_parameterized_` (https://cs.chromium.org/chromium/src/chrome/browser/chrome_content_browser_client.h?l=702&rcl=f4952ec921e83c1399dbcef76774ded442cd948e) to either a weakptr or render_process_id+routing_id. This would require a bit more effort, a design choice like that early on would have prevented both this issue and my previous report from what I can tell.

I'm messing around with these fixes, but I have a busy week so I don't know if I can complete it before the next update.

If it seems like something worthy of the "Patch Reward Program" I would be down to do it if that program allows doubling up for charity. I would not be able to complete the fix before m77 though.

### ha...@google.com (2019-09-03)

I'm working on a fix. My plan is to add an alternative to 'frame_interfaces_parameterized_' which binds GlobalFrameRoutingId instead. I'll switch OfflinePageAutoFetcher to use that instead.

Then we can migrate other users of frame_interfaces_parameterized_ in follow-up CLs, assuming no one comes up with a better option.

### ha...@google.com (2019-09-03)

I was able to reproduce with your instructions, Thanks!

Here's my WIP CL which does avoid the UAF: 
https://chromium-review.googlesource.com/c/chromium/src/+/1782695/

### ha...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### av...@chromium.org (2019-09-03)

I can think of a few people who’ve thought about routing IDs, and who might have some thoughts on this.

### dc...@chromium.org (2019-09-04)

If the AddInterface() call didn't specify a task runner, would we still post a task?

### bt...@gmail.com (2019-09-04)

I don't believe so. I think the callback is run on the current thread if no task runner is specified. https://cs.chromium.org/chromium/src/services/service_manager/public/cpp/interface_binder.h?l=69-76&rcl=fb4743ddbdbc46b0918ef1c5d5aa1542eaf8e9a9

My understanding might be wrong here though.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f60bd503a540b7ddf0920dc26b8a9cf403b9c7f3

commit f60bd503a540b7ddf0920dc26b8a9cf403b9c7f3
Author: Dan Harrington <harringtond@chromium.org>
Date: Thu Sep 05 17:30:33 2019

Fix crash in OfflinePageAutoFetcher

Previously, it was possible that the RenderFrameHost was destroyed before
attempted access by OfflinePageAutoFetcher::Create().

The fix is to avoid passing a task runner, which would PostTask().

Bug: 1000002
Change-Id: Ibb3859e9a859442cd80ef04d483c5c4ea37d01f8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1782695
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Dan H <harringtond@chromium.org>
Cr-Commit-Position: refs/heads/master@{#693827}

[modify] https://crrev.com/f60bd503a540b7ddf0920dc26b8a9cf403b9c7f3/chrome/browser/chrome_content_browser_client.cc


### bt...@gmail.com (2019-09-09)

Will this make it into m77?

### ha...@google.com (2019-09-09)

It looks like it's too late, but I'll request merge and see.

### sh...@chromium.org (2019-09-09)

This bug requires manual review: We are only 0 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2019-09-09)

1. Maybe nasko@ can confirm criticality of this fix.
2. https://chromium-review.googlesource.com/c/chromium/src/+/1782695
3. Landed in canary Sept 6: https://chromiumdash.appspot.com/commit/f60bd503a540b7ddf0920dc26b8a9cf403b9c7f3
    I verified the auto-fetch feature works in canary.
4. This is a security vulnerability.
5. No


### bt...@gmail.com (2019-09-09)

Was mostly curious, but awesome :)

I think adetaylor@  and awhalley@ help with security related merges

### na...@chromium.org (2019-09-09)

I think the CL is simple enough to be fine merging in M77. I wouldn't say we need a respin for it, but having it included in a potential respin would be nice. It is a use-after-free bug in the browser, which we have seen lately are potentially exploitable to escape Chrome's standbox.

### sh...@chromium.org (2019-09-10)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-11)

Yep, there will be at least one security respin of M77 so we should include this once we're sufficiently confident of its stability.

### la...@google.com (2019-09-13)

merge approved for M77 branch 3865

### na...@google.com (2019-09-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@chromium.org (2019-09-17)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-18)

[Empty comment from Monorail migration]

### va...@chromium.org (2019-09-18)

[Description Changed]

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $20,000 for this report :) 

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-03)

harringtond@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2019-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bt...@gmail.com (2020-04-18)

[Comment Deleted]

### bt...@gmail.com (2020-04-18)

[Comment Deleted]

### is...@google.com (2020-04-18)

This issue was migrated from crbug.com/chromium/1000002?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050032)*
