# Security: window.location update methods don't always restrict access to local resources

| Field | Value |
|-------|-------|
| **Issue ID** | [40092668](https://issues.chromium.org/issues/40092668) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2018-10-11 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Two of the window.location update methods (window.location.replace() and window.location.href = ...) don't always restrict access to local resources. This allows an extension to load an iframe containing a local file resource, even when "Allow access to file URLs" is disabled. An extension could then retrieve the contents of the iframe using a method like chrome.tabs.captureVisibleTab.

**VERSION**  

Chrome Version: 69.0.3497.100 + stable  

Operating System: Windows 10 Pro, version 1803

**REPRODUCTION CASE**

1. Install the attached extension. Ensure that "Allow access to file URLs" is disabled.
2. Once installed, the extension will open a new tab, pointing to the poc.html file it contains.
3. This file includes an iframe, with the src set to file:///C:/ initially. As the extension doesn't have access to file URLs, an error should be logged to the console stating that the tab is "Not allowed to load local resource: file:///C:/".
4. JavaScript included on the page will then change the location of the iframe to a non-local resource, using location.replace(). In this case, it will be changed to <https://www.google.com/> (this won't actually load due to cross-origin restrictions, but that has no impact on the issue here).
5. After waiting for the navigation in step 4 to complete, the JavaScript will then change the location of the iframe to file:///C:/, again using location.replace(). This should result in the same error referenced in step 3. Instead, the call will succeed and the directory listing will be loaded.

The fact that an extension can load a local resource in an iframe is problematic, because even though the extension can't interact with the iframe contents directly (due to cross-origin restrictions), it can capture the contents of the iframe in other ways, for example by using chrome.tabs.captureVisibleTab.

I think this also exposes a weakness in the protections that were put in place for chrome.tabs.captureVisibleTab in <https://bugs.chromium.org/p/chromium/issues/detail?id=810220>; namely that the protections only consider the location of the top level page and not any of the sub-frames within it. I'll file a second issue for that.

When testing, I was unable to exploit the behaviour on a standard webpage. When going through the steps above, the location.replace() call in the last step wouldn't show any error message, but the iframe location would be changed to about:blank. My assumption is that there's some other mechanism that prevents local resources from being loaded by a standard webpage.

This issue isn't restricted to using location.replace(). Using location.href = ... works equally well. Using location.assign() doesn't work, however, due to cross-origin restrictions.

In terms of the site used in step 4, from what I can tell, it can be any non-local site (i.e. not a file:///, chrome-extension:// or chrome:// page). It doesn't appear to be necessary for the site to actually be successfully loaded.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [window_location_poc.zip](attachments/window_location_poc.zip) (application/octet-stream, 1.4 KB)
- [background.js](attachments/background.js) (text/plain, 67 B)
- [manifest.json](attachments/manifest.json) (text/plain, 314 B)
- [poc.html](attachments/poc.html) (text/plain, 273 B)
- [poc.js](attachments/poc.js) (text/plain, 308 B)

## Timeline

### de...@gmail.com (2018-10-11)

The issue regarding chrome.tabs.captureVisibleTab has been filed here: https://bugs.chromium.org/p/chromium/issues/detail?id=894411

### wf...@chromium.org (2018-10-11)

devin, can you take a look at this and triage? Thanks.

[Monorail components: Platform>Extensions]

### wf...@chromium.org (2018-10-11)

unzipped

### rd...@chromium.org (2018-10-11)

Interesting. Nasko, Charlie, Alex: is being able to embed file URLs in unrelated pages WAI?  If so, then I think this is largely WAI as well (though we'll then need to separately fix https://crbug.com/chromium/894411).  If not, then we should fix this, and in doing so, fix https://crbug.com/chromium/894411.

### cr...@chromium.org (2018-10-11)

This definitely sounds like a security issue.  The report correctly notes that web pages are not allowed to load file:// URLs in iframes, and I would certainly expect that to apply to extension pages as well.  Indeed, step 3 indicates that we try to prevent navigating to a file:// URL in extensions, but apparently something about the error page and second attempt in steps 4-5 allows it to work.

(Caveat: I haven't tried to repro this yet, but it sounds worth fixing.)

[Monorail components: UI>Browser>Navigation]

### rd...@chromium.org (2018-10-11)

Thanks, Charlie!  If this is an issue with the error page and navigation, is this something that one of y'all could look into (or triage)?

### al...@chromium.org (2018-10-11)

I can repro on Linux ToT, if I replace the "file:///c:/" with "file:///".  In the second attempt, the navigation happens via a proxy, so I suspect something's wrong with checking for file: navigations on that path.

### al...@chromium.org (2018-10-11)

OK, did a bit more digging.

First, it seems that we're indeed missing the "Not allowed to load local resource" check on the path for navigating remote frames.  For local frames, the navigations happen via HTMLFrameElementBase::OpenURL() -> HTMLFrameOwnerElement::LoadOrRedirectSubframe() -> LocalFrame::ScheduleNavigation(), which then continues as ScheduledURLNavigation::Fire() -> FrameLoader::StartNavigation() -> 
FrameLoader::PrepareRequestForThisFrame().  PrepareRequestForThisFrame() is what has this security check:

  if (!request.OriginDocument()->GetSecurityOrigin()->CanDisplay(url)) {
    request.OriginDocument()->AddConsoleMessage(ConsoleMessage::Create(
        kSecurityMessageSource, kErrorMessageLevel,
        "Not allowed to load local resource: " + url.ElidedString()));

On the remote frame navigation path, we just have HTMLFrameOwnerElement::LoadOrRedirectSubframe() -> RemoteFrame::ScheduleNavigation() ->  RemoteFrame::Navigate(), which goes on to send an OpenURL IPC to the browser, never performing the same CanDisplay() check.  Should be fairly straightforward to add it, and that'll fix this bug - assuming the renderer isn't compromised. :)

To withstand compromised renderers, we handle this on the browser side as well.  I think this is supposed to happen as part of FilterURL(), which rewrites the file:// URL to about:blank if the navigating renderer can't request file: URLs, thanks to ChildProcessSecurityPolicyImpl::CanRequestURL() returning false.  This is what happens if we navigate a remote subframe on a HTTP page to file:// - there's no  warning (which would be fixed by adding the above check), but there's no security issue either, as we just load a blank page.

Interestingly, this is also what happens when I try to manually inject file: URLs into other installed extensions (such as chrome-extension://mhjfbmdgcfjbbpaeojofohoefgiehjai/index.html, the built-in PDF extension) - I can't get the directory listing in the iframe to show.  However, for this particular extension, the file: URL *is* allowed to be requested, thanks to this code in ExtensionWebContentsObserver::RenderFrameCreated:

  // Some extensions use file:// URLs.
  //
  // Note: this particular grant isn't relevant for hosted apps, but in the
  // future we should be careful about granting privileges to hosted app
  // subframes in places like this, since they currently stay in process with
  // their parent. A malicious site shouldn't be able to gain a hosted app's
  // privileges just by embedding a subframe to a popular hosted app.
  if (type == Manifest::TYPE_EXTENSION ||
      type == Manifest::TYPE_LEGACY_PACKAGED_APP) {
    ExtensionPrefs* prefs = ExtensionPrefs::Get(browser_context_);
    if (prefs->AllowFileAccess(extension->id())) {
      content::ChildProcessSecurityPolicy::GetInstance()->GrantRequestScheme(
          render_frame_host->GetProcess()->GetID(), url::kFileScheme);
    }
  }

Now, questions for Devlin:

1) Why would this extension be granting file access here?  I don't see anything special in the manifest - is it perhaps due to installing it as an unpacked extension?  (I tried loading another unpacked extension, and it did this grant as well, but a couple of other extensions installed from the web store didn't seem to do it.)  If this affects only unpacked extensions, this would be less severe.

2) It seems this path legitimately allows some extensions to request file URLs.  So then it seems that step 3 in the repro should've just worked - is it actually correct that the renderer is blocking file: access in that case?


### al...@chromium.org (2018-10-11)

Ah, my theory about unpacked extensions in (1) of c#8 seems to be true: https://cs.chromium.org/chromium/src/chrome/browser/extensions/extension_service.cc?l=1617&rcl=da29c7f2a3be80010b0f379b075628b1b8adfd6f -
 "Unpacked extensions default to allowing file access".

### de...@gmail.com (2018-10-12)

I'm not too familiar with the actual implementation, so I'm happy to be corrected, but my understanding is that the default file access that's granted to unpacked extensions is reflected in the "Allow access to file URLs" setting. I specifically unchecked that setting for the extension while I was testing. It's possible it doesn't do what I expect, though.

If it's helpful at all, I also went through the steps manually for two extensions installed the usual way (the built-in PDF extension and uBlock Origin) and was able to load the local resource in both cases. I did the tests by opening the extension pages and running the location commands manually within the developer tools console (I'm not sure if that would make a difference).

### sh...@chromium.org (2018-10-12)

[Empty comment from Monorail migration]

### rd...@chromium.org (2018-10-12)

Unpacked extensions default to allowing file access.  This has been the case as far back as I can remember, and is something I'd like to change, but first we'd need to ascertain if anything in particular would break.  That said, I don't think that's the issue here - as long as we correctly respect the "Extension is allowed file access" bit, then I think this is reasonable from a security perspective.  However, I don't think that bit should necessarily allow extensions to embed file iframes.

> 1) Why would this extension be granting file access here?  I don't see anything special in the manifest - is it perhaps due to installing it as an unpacked extension?  (I tried loading another unpacked extension, and it did this grant as well, but a couple of other extensions installed from the web store didn't seem to do it.)  If this affects only unpacked extensions, this would be less severe.

Unpacked extensions are autogranted file access, but users can also grant the extension file access explicitly.  And obviously, after an extension is uninstalled, it shouldn't be able to continue making these requests.

> 2) It seems this path legitimately allows some extensions to request file URLs.  So then it seems that step 3 in the repro should've just worked - is it actually correct that the renderer is blocking file: access in that case?

We let extensions inject on file URLs and XHR to file URLs iff they have file access (and also declare the scheme in their permissions), but I wouldn't have expected this to necessarily allow them to embed file iframes.  The permissions to inject and XHR are also properly revoked on extension disable/removal, so even if an extension page remains open (e.g. through the about:blank trick here, or a content script), we will then properly block the request on both the browser and renderer.

It's unfortunate that this also seems to allow iframed file URLs as well.  I' be curious if there's any extensions currently relying on that behavior, or if it's something we can change.  Other frames are generally restricted to the same rules as the open web, so I think it would align with our model as well (for instance, even if an extension has access to a particular URL and can fetch it, the iframe will still respect typical iframing rules like x-frame options).

### al...@chromium.org (2018-10-12)

#10: Can you post your repro steps with the built-in PDF extension?  And also whether it works on Chrome Canary?  When I tried to repro for that extension manually via DevTools, I couldn't get the file listing to show up, so I wonder what we're doing differently.

### de...@gmail.com (2018-10-15)

Here are the steps I went through:
1. Opened the extension page (chrome-extension://mhjfbmdgcfjbbpaeojofohoefgiehjai/index.html) in a new tab.
2. Opened the developer tools console and ran the following commands:
var iframe = document.createElement("iframe");
document.body.appendChild(iframe);
iframe.contentWindow.location.replace("https://www.google.com/");
iframe.contentWindow.location.replace("file:///C:/");

There may need to be a small gap between the last two commands in order to give the navigation in the second last command time to complete (if the last command is run immediately after, it may not work).

I can't reproduce the issue in Chrome Canary. Going through the above steps in that version simply results in about:blank being loaded in the iframe (even though the last location.replace() call doesn't show any error message).

### rd...@chromium.org (2018-10-15)

alexmos@ is investigating; passing ownership.

### al...@chromium.org (2018-10-15)

https://crbug.com/chromium/894399#c14: I still can't repro using those steps on Win 69.0.3497.100 stable.  I see about:blank being loaded in the iframe after the last call.  Same behavior on dev and canary.  Can you try your repro in a clean profile?

https://crbug.com/chromium/894399#c12:
Thanks for the context!  If file URL permissions are only supposed to be used for XHRs and injecting on file URLs, it seems that the browser process should just block navigations to file URLs in extensions, since presumably it's already blocked by the renderer for the local frame navigation path, due to the CanDisplay() check from c#8.  Is there a sample test extension somewhere that uses the file permission like this?  It'd be nice to check without relying on the unpacked extension auto-grant.

### rd...@chromium.org (2018-10-16)

> Is there a sample test extension somewhere that uses the file permission like this?  It'd be nice to check without relying on the unpacked extension auto-grant.

You could take a look at the ones in chrome/test/data/extensions/api_test/cross_origin_xhr.  You can trim the manifest down a bit more by just requesting the file scheme (e.g., `"permissions": ["file://*"]`).

[1] https://chromium.googlesource.com/chromium/src/+/8d628983e3a3dcd5174f1793ea5345febec04d89/chrome/test/data/extensions/api_test/cross_origin_xhr

### de...@gmail.com (2018-10-16)

I wasn't able to reproduce the issue in a completely clean profile. It seems it may be partly due to interaction with another extension. The proof of concept extension consistently reproduces the issue in my original profile. Aside from the default set of extensions, the only thing I installed there was uBlock Origin.

I can reproduce in a new profile in the current stable build (69.0.3497.100) by going through the following steps:

1. Create the new profile.
2. Install uBlock Origin.
3. Install the proof of concept extension attached to this issue.
4. Disable file access for the proof of concept extension.

At that point, the file listing shows up consistently when I reload the proof of concept extension.

I haven't been able to reproduce the issue at all in Chrome Beta or Canary.

### al...@chromium.org (2018-10-16)

Thanks for the new details.  I still can't repro in a clean profile on Win stable 69.0.3497.100, even with uBlock Origin installed, using steps in either c#18 or c#14.  kenrb@ was able to repro c#18 in one of his profiles on 69.0.3497.100 but not c#14, and also there was no repro of either c#18 or c#14 in a clean profile.  Neither one of us can run a bisect to figure out what got fixed, since there's no repro in any of the bisected builds.

### al...@chromium.org (2018-10-16)

derceg86@gmail.com: can you please paste in your variations from chrome://version, so that we can check if a field trial is needed for the repro to work?

### de...@gmail.com (2018-10-17)

Sure, here's the list of variations that appear:
c134752e-1ece3553
3e006338-3f4a17df
1a0d11d4-2f9febdf
ebeb14fc-3f4a17df
752a9400-3d47f4f4
b7e2524c-ca7d8d80
8fe39baa-3f4a17df
241fff6c-ca7d8d80
8502ae4f-e1031ab5
3095aa95-3f4a17df
c27fec31-2d5b6ed9
7c1bc906-f55a7974
47e5d3db-3d47f4f4
9ca1387e-ca7d8d80
1149accc-5c943877
4dc30737-b8a5ea08
c865fdc1-ca7d8d80
a582a1b8-ad75ce17
8ee5ed19-ca7d8d80
74658432-ca7d8d80
ebbb4e0a-ca7d8d80
e56c5101-7d60f345
267255c3-f4950e99
249dd49a-f3d16784
88a387d2-ee748cef
334aa58d-3f4a17df
5e3a236d-4113a79e
edbcf7c5-1cc1312c
de47491b-33c3eba5
43f62d3b-28165b59
3a0563a1-65222f0b
9e5c75f1-1039a221
6872f671-991e1e1
332bb593-3d47f4f4
f79cb77b-3f4a17df
2ca9c26b-3f4a17df
4ea303a6-ecbb250e
6e6e0c7e-3f17a7d8
d92562a9-441539fd
7aa46da5-c946b150
4da5ae82-91c810ef
2c1d398c-3f4a17df
6973a1cf-3f4a17df
cc54eb06-28165b59
cac0a91c-77662737
58a025e3-36e97b2c
df072bba-ca7d8d80
ff29b1bd-1c82c12a
ddf77e2c-ca7d8d80
1354da85-f1a864dc
17507c76-ca7d8d80
494d8760-52325d43
f47ae82a-86f22ee5
3ac60855-486e2a9c
f296190c-71ff9dce
4442aae2-d7f6b13c
ed1d377-e1cc0f14
75f0f0a0-d7f6b13c
e2b18481-3a9ae350
e7e71889-e1cc0f14
b1ceb06f-d1372334
3a4029d-ca7d8d80
6ab94979-3f4a17df
94e68624-803f8fc4
81c6897f-3d47f4f4

### cr...@chromium.org (2018-10-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5f8671e7667b8b133bd3664100012a3906e92d65

commit 5f8671e7667b8b133bd3664100012a3906e92d65
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Fri Oct 19 02:10:11 2018

Add a check for disallowing remote frame navigations to local resources.

Previously, RemoteFrame navigations did not perform any renderer-side
checks and relied solely on the browser-side logic to block disallowed
navigations via mechanisms like FilterURL.  This means that blocked
remote frame navigations were silently navigated to about:blank
without any console error message.

This CL adds a CanDisplay check to the remote navigation path to match
an equivalent check done for local frame navigations.  This way, the
renderer can consistently block disallowed navigations in both cases
and output an error message.

Bug: 894399
Change-Id: I172f68f77c1676f6ca0172d2a6c78f7edc0e3b7a
Reviewed-on: https://chromium-review.googlesource.com/c/1282390
Reviewed-by: Charlie Reis <creis@chromium.org>
Reviewed-by: Nate Chapin <japhet@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#601022}
[modify] https://crrev.com/5f8671e7667b8b133bd3664100012a3906e92d65/content/browser/security_exploit_browsertest.cc
[modify] https://crrev.com/5f8671e7667b8b133bd3664100012a3906e92d65/content/browser/site_per_process_browsertest.cc
[modify] https://crrev.com/5f8671e7667b8b133bd3664100012a3906e92d65/third_party/blink/renderer/core/frame/remote_frame.cc


### rd...@chromium.org (2018-10-22)

[Empty comment from Monorail migration]

### al...@chromium.org (2018-10-22)

https://crbug.com/chromium/894399#c21: thanks.  I tried to manually enable a few experiments that were active in #21 but not on my machine, but I still couldn't find anything that would allow me to repro locally.  And overall, none of the field trial differences jump out as possibly related to this.

https://crbug.com/chromium/894399#c23 fixes the renderer-side checks for remote frames to be consistent with the local frame cases, i.e., by canceling the navigation attempt, staying on the old page, and displaying the error message in the console.  I verified this in 72.0.3588.0.  This fix isn't really intended as a security enforcement, since a compromised renderer can bypass it.  For that, we also have the browser-side enforcement in FilterURL.  To recap, we think there might've been a separate problem in that enforcement that caused the file:/// access to be maintained even after turning off permission for the (unpacked) extension to access file URLs, but it must've been fixed independently somewhere along the way (the reporter couldn't repro in Beta or Canary; I could not repro in any profiles or channels; kenrb@ could repro on Stable in an older profile but not on a clean profile; bisect also couldn't repro).  Based on this, I don't think we can do any more work here, so closing as fixed.

### sh...@chromium.org (2018-10-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-01)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-11-01)

+awhalley@ (Security TPM) for M71 merge review.

### aw...@google.com (2018-11-01)

govind@ - good for 71

### go...@chromium.org (2018-11-01)

Approving merge to M71 branch 3578 based on https://crbug.com/chromium/894399#c31. Please merge ASAP. Thank you.

### go...@chromium.org (2018-11-01)

Pls merge your change to M71 branch 3578 ASAP so we can pick it up for next beta release. Thank you.

### cr...@appspot.gserviceaccount.com (2018-11-02)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/719b5e284e6e3391cadde1e225af240fc559ff26

Commit: 719b5e284e6e3391cadde1e225af240fc559ff26
Author: alexmos@chromium.org
Commiter: alexmos@chromium.org
Date: 2018-11-02 16:58:28 +0000 UTC

Merge to M71: Add a check for disallowing remote frame navigations to local resources.

Previously, RemoteFrame navigations did not perform any renderer-side
checks and relied solely on the browser-side logic to block disallowed
navigations via mechanisms like FilterURL.  This means that blocked
remote frame navigations were silently navigated to about:blank
without any console error message.

This CL adds a CanDisplay check to the remote navigation path to match
an equivalent check done for local frame navigations.  This way, the
renderer can consistently block disallowed navigations in both cases
and output an error message.

TBR=alexmos@chromium.org

(cherry picked from commit 5f8671e7667b8b133bd3664100012a3906e92d65)

Bug: 894399
Change-Id: I172f68f77c1676f6ca0172d2a6c78f7edc0e3b7a
Reviewed-on: https://chromium-review.googlesource.com/c/1282390
Reviewed-by: Charlie Reis <creis@chromium.org>
Reviewed-by: Nate Chapin <japhet@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#601022}
Reviewed-on: https://chromium-review.googlesource.com/c/1315531
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#472}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}

### bu...@chromium.org (2018-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/719b5e284e6e3391cadde1e225af240fc559ff26

commit 719b5e284e6e3391cadde1e225af240fc559ff26
Author: Alex Moshchuk <alexmos@chromium.org>
Date: Fri Nov 02 16:58:28 2018

Merge to M71: Add a check for disallowing remote frame navigations to local resources.

Previously, RemoteFrame navigations did not perform any renderer-side
checks and relied solely on the browser-side logic to block disallowed
navigations via mechanisms like FilterURL.  This means that blocked
remote frame navigations were silently navigated to about:blank
without any console error message.

This CL adds a CanDisplay check to the remote navigation path to match
an equivalent check done for local frame navigations.  This way, the
renderer can consistently block disallowed navigations in both cases
and output an error message.

TBR=alexmos@chromium.org

(cherry picked from commit 5f8671e7667b8b133bd3664100012a3906e92d65)

Bug: 894399
Change-Id: I172f68f77c1676f6ca0172d2a6c78f7edc0e3b7a
Reviewed-on: https://chromium-review.googlesource.com/c/1282390
Reviewed-by: Charlie Reis <creis@chromium.org>
Reviewed-by: Nate Chapin <japhet@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#601022}
Reviewed-on: https://chromium-review.googlesource.com/c/1315531
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/branch-heads/3578@{#472}
Cr-Branched-From: 4226ddf99103e493d7afb23a4c7902ee496108b6-refs/heads/master@{#599034}
[modify] https://crrev.com/719b5e284e6e3391cadde1e225af240fc559ff26/content/browser/security_exploit_browsertest.cc
[modify] https://crrev.com/719b5e284e6e3391cadde1e225af240fc559ff26/content/browser/site_per_process_browsertest.cc
[modify] https://crrev.com/719b5e284e6e3391cadde1e225af240fc559ff26/third_party/blink/renderer/core/frame/remote_frame.cc


### aw...@chromium.org (2018-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-02)

Nice one derceg86@! $2,000 for this report :-)

### aw...@google.com (2018-11-02)

A member of our finance team will be in touch to arrange for payment.

### aw...@google.com (2018-11-02)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/894399?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Browser>Navigation]
[Monorail mergedwith: crbug.com/chromium/894411]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092668)*
