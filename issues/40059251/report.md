# Security: Browser-side origin confusion for javascript/data URLs opened in a new window/tab by cross-origin iframe

| Field | Value |
|-------|-------|
| **Issue ID** | [40059251](https://issues.chromium.org/issues/40059251) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Sandbox>SiteIsolation, UI>Browser>Navigation, UI>Browser>Permissions |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2022-03-30 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

A cross-origin iframe can spoof the top-frame origin's hostname shown in a JavaScript dialog title (such as alert(), prompt(), etc.) by opening a new window/tab to a blank-ish page (but \*not\* about:blank) and then creating the JS dialog.

Opening a new window requires a single mouse or keyboard interaction within the iframe. However, the keyboard interaction can be easily obtained using focus theft described in <https://crbug.com/chromium/622714>.

I've been able to reproduce the spoof using the following URLs in window.open():  

\* data:,Hello (or just data:, with the trailing comma; using data: alone shows ERR\_INVALID\_URL error page)  

\* javascript: with any payload (e.g. javascript:prompt(...) )  

\* test: (or any external protocol, regardless of whether it has a handler or not)

about:blank itself results in safe behavior (iframe hostname shown in dialog title). about:srcdoc shows ERR\_INVALID\_URL error page.

BISECT RESULTS  

This started reproducing after this commit which landed in M98: <https://chromiumdash.appspot.com/commit/afd3c658f932029bb4953b1e2498a500799c6d7f>

Bisects revealed these commits which affected JS dialog title behavior:  

\* commit 649f10ac64a1df2ac60e5ddf492eaa1a9f99357b (Use GetLastCommittedOrigin in Javascript dialogs; Sep 07 2021) which resulted in the browser showing the top-frame hostname, "top-hostname.tld says". Previously, the dialog title showed "This page says".  

\* commit afd3c658f932029bb4953b1e2498a500799c6d7f (Create initial NavigationEntry on FrameTree initialization; Nov 30 2021) which resulted in the browser showing the incorrect hostname, "top-hostname.tld says". Previously, the dialog title showed "iframe-hostname.tld says".

JS dialogs from iframes directly have not changed behavior and still correctly show "An embedded page at iframe-hostname.tld says".

I haven't analyzed the navigation commit yet in detail, but I will soon to determine whether other browser areas might also be similarly affected.

**VERSION**  

Chrome Version: 99.0.4844.84 (Official Build) (64-bit) (cohort: Stable), 102.0.4973.0 Canary  

Operating System: Windows 10 Version 21H2 (Build 19044.1526)

Chrome Version: 99.0.4844.88 (Official Build) (64-bit) Stable, 102.0.4971.0 Canary  

Operating System: Android 12

**REPRODUCTION CASE**

1. Navigate to <https://alesandroortiz.com/security/chromium/js-dialog-origin-spoof.html>
2. Click anywhere in iframe (or press any key that provides user activation).

Observed: JavaScript dialog title shows hostname of top-most frame origin.  

Expected: JavaScript dialog title shows hostname of initiator origin, which is the iframe origin.

You can also switch between the different scenarios using the links on the page:  

\* popup: Uses "javascript:" URL  

\* tab: Uses "javascript:" URL in new tab  

\* data: Uses "data:,Hello" URL  

\* protocol: Uses "test:" URL  

\* docwrite1: Uses "javascript:document.write(...)" which results in renderer kill  

\* docwrite2: Uses "data:,Hello" URL, then attempts to use document.write(...) which results in a different renderer kill

Behavior is the same whether in a new window (popup) or new tab.

**CREDIT INFORMATION**  

Reporter credit: Sameer and Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [js-dialog-origin-spoof.html](attachments/js-dialog-origin-spoof.html) (text/plain, 752 B)
- [js-dialog-origin-spoof-frame.html](attachments/js-dialog-origin-spoof-frame.html) (text/plain, 2.1 KB)
- [js-dialog-origin-spoof.mp4](attachments/js-dialog-origin-spoof.mp4) (video/mp4, 2.8 MB)
- [js-dialog-expected.png](attachments/js-dialog-expected.png) (image/png, 9.7 KB)
- [js-dialog-origin-spoof-Android.jpg](attachments/js-dialog-origin-spoof-Android.jpg) (image/jpeg, 134.6 KB)
- [origin-spoof-with-content.png](attachments/origin-spoof-with-content.png) (image/png, 35.4 KB)
- [rfh-origin-spoof.html](attachments/rfh-origin-spoof.html) (text/plain, 1.0 KB)
- [rfh-origin-spoof-frame.html](attachments/rfh-origin-spoof-frame.html) (text/plain, 3.4 KB)
- [rfh-origin-spoof.mp4](attachments/rfh-origin-spoof.mp4) (video/mp4, 1.4 MB)
- [rfh-origin-spoof-android-contacts.mp4](attachments/rfh-origin-spoof-android-contacts.mp4) (video/mp4, 151.0 KB)
- [renderer.patch](attachments/renderer.patch) (text/plain, 11.8 KB)
- [browser.patch](attachments/browser.patch) (text/plain, 2.3 KB)
- [rfh-origin-spoof-pt2.html](attachments/rfh-origin-spoof-pt2.html) (text/plain, 1.3 KB)
- [rfh-origin-spoof-pt2-frame.html](attachments/rfh-origin-spoof-pt2-frame.html) (text/plain, 7.6 KB)
- [set-cookie-idb.html](attachments/set-cookie-idb.html) (text/plain, 439 B)
- [broadcast-channel.html](attachments/broadcast-channel.html) (text/plain, 835 B)
- [shared-worker.html](attachments/shared-worker.html) (text/plain, 936 B)
- [shared-worker.js](attachments/shared-worker.js) (text/plain, 475 B)
- [shared-worker-2.html](attachments/shared-worker-2.html) (text/plain, 1.2 KB)
- [rfh-origin-spoof-pt2-regular-renderer.mp4](attachments/rfh-origin-spoof-pt2-regular-renderer.mp4) (video/mp4, 3.5 MB)
- [rfh-origin-spoof-pt2-websocket.mp4](attachments/rfh-origin-spoof-pt2-websocket.mp4) (video/mp4, 689.7 KB)
- [rfh-origin-spoof-pt2-compromised-renderer.mp4](attachments/rfh-origin-spoof-pt2-compromised-renderer.mp4) (video/mp4, 7.7 MB)
- [renderer-postmessage.patch](attachments/renderer-postmessage.patch) (text/plain, 1.3 KB)
- [rfh-origin-spoof-pt3.html](attachments/rfh-origin-spoof-pt3.html) (text/plain, 707 B)
- [rfh-origin-spoof-pt3-frame.html](attachments/rfh-origin-spoof-pt3-frame.html) (text/plain, 2.0 KB)
- [postmessage-to-parent.html](attachments/postmessage-to-parent.html) (text/plain, 569 B)
- [rfh-origin-spoof-pt3-postmessage.mp4](attachments/rfh-origin-spoof-pt3-postmessage.mp4) (video/mp4, 1.3 MB)
- deleted (application/octet-stream, 0 B)

## Timeline

### al...@alesandroortiz.com (2022-03-30)

[Comment Deleted]

### al...@alesandroortiz.com (2022-03-30)

After commit afd3c658f932029bb4953b1e2498a500799c6d7f, I also noticed these new adjacent behaviors that seemed interesting:

A PoC of window.open('javascript:document.write("test")'); results in a renderer kill due to bad_message::RFH_CAN_COMMIT_URL_BLOCKED at  https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=10781;drc=42e75824670baadf21ece40f71b946500af1cbce
A similar PoC of: var win = window.open('data:,Hello'); win.document.write('test'); results in a renderer kill due to bad_message::RFH_INVALID_ORIGIN_ON_COMMIT at https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=10794;drc=42e75824670baadf21ece40f71b946500af1cbce . Using this PoC with any of the other URLs which reproduce the spoof also appears to result in the same renderer kill.

These checks prevent unsafe behaviors, but I would not expect them to be easily reached without a compromised renderer. Once I analyze commit afd3c658f932029bb4953b1e2498a500799c6d7f in detail, I might be able to identify other security issues caused by this navigation behavior change.

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-03-30)

Additional screenshots:
* js-dialog-expected.png: Expected JS dialog behavior (from 98.0.4738.0 developer build).
* js-dialog-origin-spoof-Android.png: Repro in Chrome for Android 99.0.4844.88 Stable.

### al...@alesandroortiz.com (2022-03-30)

Minor correction:
* ... (Use GetLastCommittedOrigin in Javascript dialogs; Sep 07 2021) which resulted in the browser showing the iframe page hostname, "iframe-hostname.tld says". Previously, the dialog title showed "This page says".

### al...@alesandroortiz.com (2022-03-30)

As an FYI, I've already identified other impacted areas that are more sensitive, such as permission prompt UI + permission checks, so the impact is *not* limited to JS dialogs like I initially thought.

I've verified this allows an iframe to use the spoofed origin's permissions if previously granted. For example, if example.com already has camera access, and a malicious iframe performs this attack, the iframe can immediately gain camera access without any additional user interaction or prompts. If permission had not been previously granted, the popup/tab will show the spoofed origin in the permission prompt.

### al...@alesandroortiz.com (2022-03-31)

In terms of sandboxed iframes:
* Dialog PoCs work with sandbox="allow-scripts allow-popups allow-modals" (or "allow-popups-to-escape-sandbox" instead of "allow-modals")
* Permission PoCs work with sandbox="allow-scripts allow-popups allow-same-origin" (not 100% sure if all of them require "allow-same-origin").

### al...@alesandroortiz.com (2022-03-31)

Since this issue seems related to the initial document state, there are also additional cases that keep the initial document for an extended period of time, like a slow-loading page. For example, the following PoC run from within the iframe has the same spoofing behavior until the URL commits, if it ever does. An attacker can keep setting window.location to the slow-loading URL and the page will never commit.

var win = window.open('https://aogarantiza.com/chromium/slow.php'); // Script delayed by 10 seconds
setInterval(() => { win.location = 'https://aogarantiza.com/chromium/slow.php'; }, 8000); // We re-navigate every 8 seconds
win.navigator.mediaDevices.getDisplayMedia(); // Permission dialog remains shown with spoofed origin despite re-navigations, and re-attempts also work if user closes permission UI.

I'll attach proper PoCs and screen recordings for the permission UI + logic checks tomorrow.

### al...@alesandroortiz.com (2022-03-31)

In the same vein as https://crbug.com/chromium/1311820#c8, using a URL that responds with HTTP status code 204 also results in the same spoofing behavior (like https://aogarantiza.com/204.php )

### mk...@google.com (2022-03-31)

+Arthur for the //content level analysis of whether anything's going wrong with the origin during commit.

+Balazs for the permissions angle.

### hc...@google.com (2022-03-31)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-03-31)

Still exploring further impacts.

I was able to keep the origin spoofed in permission UI/checks + JS dialogs \*and\* also write HTML to the new window/tab by returning a string in a javascript: URL (either on initial window.open() call or by calling win.location after). See attached screenshot and basic PoC below for quick reference. (Will share proper PoCs later today.)

Within attacker iframe: var win = window.open('javascript:"**Hello** World"'); win.navigator.mediaDevices.getUserMedia({video: true});

### [Deleted User] (2022-03-31)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-03-31)

Additional impact: XFO header bypass. Spoofed origin's iframe with XFO set to sameorigin is allowed to load in the new window/tab alongside attacker-controlled code.

### en...@chromium.org (2022-03-31)

I have been able to reproduce at least the JS dialog and permission related issues on trunk (have not looked into the XFO bypass).

Following the steps of the POC, the new window's main frame ends up in an inconsistent state where the security origin is calculated correctly on the Blink side, but on the browser side, the RenderFrameHost's last committed origin is set to an incorrect value: the old main frame's origin, not the initiator origin. This (incorrect) origin is then used as the basis for controlling access to permission-gated capabilities, as well as all the UI surfaces referenced above.

Change crrev.com/c/3237491 strikes me as a plausible regression point based on bisect results, but I have not verified myself. Tentatively adding author and reviewer, setting component, and, as the CL initially shipped in 98.0.4739.0, tentatively setting found-in milestone to M98. Furthermore, as the issue seems to be with the //content implementation, marking all OS'es where Chromium uses it.

[Monorail components: UI>Browser>Navigation]

### [Deleted User] (2022-03-31)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2022-03-31)

When possible, please CC the other researcher (see https://crbug.com/chromium/1311820#c1).

### en...@chromium.org (2022-03-31)

[Empty comment from Monorail migration]

### ra...@chromium.org (2022-03-31)

Thanks for cc-ing, just a quick comment on crrev.com/c/3237491: the changes in that CL has been disabled/put behind a flag for M98+. We're currently experimenting with it on M100 Canary/Dev/Beta, and in M100+ you can enable/disable the changes there with chrome://flags/#initial-navigation-entry, maybe it's worth checking if it repros with/without the flag?

### al...@alesandroortiz.com (2022-03-31)

I tried flipping that flag on Canary last night and didn't notice any effect on my PoCs, but don't remember which one I was testing specifically. I suspect if one worked, most or all of them probably will work.

I'll try flipping the flag again soon to re-verify.. Also worth noting this repros the same on Stable + Canary (other than slightly diff. behavior with data: URLs that can cause PoCs to fail, so try to avoid those when testing)

### en...@chromium.org (2022-03-31)

I can confirm that at least the scenario "tab" does repro on trunk regardless the chrome://flags/#initial-navigation-entry flag state. I can see the flag having an effect on whether NavigationController::GetLastCommittedEntryIndex() returns -1 (flag off) or 0 (flag on) for the new WebContents, but its main frame last committed origin is set to the old main frame's origin in both cases.

### en...@chromium.org (2022-03-31)

CC'ing collaborating researcher as requested by reporter in https://crbug.com/chromium/1311820#c1.

### al...@alesandroortiz.com (2022-03-31)

Thanks for CC'ing the second researcher.

Can confirm https://crbug.com/chromium/1311820#c20 and https://crbug.com/chromium/1311820#c21, no behavior change with chrome://flags/#initial-navigation-entry enabled or disabled on Canary using Windows.

Additional impact: Can load spoofed origin iframe despite CSP: frame-ancestors 'self' (like XFO bypass in https://crbug.com/chromium/1311820#c14)

I watched rakina@'s BlinkOn 15 talk, and this slide (https://docs.google.com/presentation/d/1WyXLGiOUlM5teP_G-RO21jJ1-CYLsZKm0FZ2WH7xgkA/edit#slide=id.gfd3939d74a_0_56) from ~Nov 2021 says the window object was kept between the initial empty document and the next document. The 23rd slide says "The window reuse thing is still there and we need to deal with it" and I can repro with same-origin navigations to the attacker origin, but am unable to repro with the target origin. Is this enforced by the renderer, or are there additional browser-side protections that prevent this (like changing the process)?

More generally curious what a compromised renderer could do with this behavior. chrome://process-internals shows the new window/tab being locked to the attacker site (as expected) so I don't expect impacts with browser-enforced Site Isolation (unless chained with another vulnerability).

### ra...@chromium.org (2022-04-01)

OK, I think this is caused by my CL moving this line where we set a new popup's origin with the opener's LastCommittedOrigin() from RenderFrameHostImpl::CreateNewWindow: https://chromium-review.googlesource.com/c/chromium/src/+/3237491/60/content/browser/renderer_host/render_frame_host_impl.cc#b6737

to setting it to the opener's LastCommittedOrigin from FrameTree::Init https://chromium-review.googlesource.com/c/chromium/src/+/3237491/60/content/browser/renderer_host/frame_tree.cc#812

Apparently FrameTree's GetOriginalOpener() always points to the main frame instead of the opener (from the comment, this is actually for security too?): https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=9076;drc=7fb345a0da63049b102e1c0bcdc8d7831110e324. I guess we can fix this by passing the actual opener of the FrameTree (the subframe) and getting the origin from the correct frame, I'll work on a CL to do that soon. I confirmed that moving the code back to where it was fixes the bug (at least it doesn't repro with the iframe case for me)

Regarding the window reuse comment from https://crbug.com/chromium/1311820#c23: can you clarify what you mean by "I can repro with same-origin navigations to the attacker origin, but am unable to repro with the target origin."? The window reuse happens on navigations from an initial empty document to a same-origin URL, and happens entirely within the renderer here: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/document_loader.cc;l=2188;drc=d56e835b6f878da732633a836c459fa17c8eb4b8


### cr...@chromium.org (2022-04-01)

Thanks for the fantastic and detailed report!  I'm reviewing rakina@'s fix at https://chromium-review.googlesource.com/c/chromium/src/+/3564826 and working through some questions.  Should be able to send replies later today.

CC'ing avi@ for FYI, given the behavior of GetOriginalOpener mentioned in https://crbug.com/chromium/1311820#c24 (from https://crbug.com/chromium/705316) and the dialog change in r918887.  Adding Permissions component due to the impact from https://crbug.com/chromium/1311820#c6 and https://crbug.com/chromium/1311820#c12, and Site Isolation given the general implications of getting the RFH's origin wrong, even if the ProcessLock is correct (per https://crbug.com/chromium/1311820#c23).

For severity, the dialog origin spoof has some mitigating factors (e.g., can only be done in a popup while address bar shows about:blank, requires user interaction, requires being an iframe on a victim origin), so I would normally consider that a Medium.  Since there are also additional impacts from the permission leak and XFO/CSP bypass, though, I'm tentatively inclined to rate this as High.  Others can feel free to weigh in on that.

[Monorail components: Internals>Sandbox>SiteIsolation UI>Browser>Permissions]

### al...@alesandroortiz.com (2022-04-01)

rakina@: Thanks for identifying the root cause, I was still catching up with the docs explaining the CL's context and barely starting to analyze the navigation CL itself.

For impact analysis, I had focused on code that used last_committed_origin_ for security checks. There's still potentially more impacts based on last_committed_origin_, though the more severe impacts luckily seem mitigated by process locks or URL checks (since the URL itself isn't spoofed, just the origin).

Based on your analysis, I took a quick look at SetOriginDependentStateOfNewFrame(). The header comment + definition indicate this method also affects isolation_info_ which might cause additional impacts, if they aren't mitigated by process locks or URL checks. I have a few paths that seem viable, so I'll continue investigating to fully understand impacts.

  // Set the |last_committed_origin_|, |isolation_info_|, and
  // |permissions_policy_| of |this| frame, inheriting the origin from
  // |new_frame_creator| as appropriate (e.g. depending on whether |this| frame
  // should be sandboxed / should have an opaque origin instead).
  void SetOriginDependentStateOfNewFrame(const url::Origin& new_frame_creator);

I agree GetOriginalOpener() should be renamed. I'm also going to analyze other uses of this (there's not that many) for potential impacts.

Re: window reuse, if we're at the initial empty document with {origin: https://alesandroortiz.com, URL: about:blank, processLock: https://aogarantiza.com} and navigate to https://alesandroortiz.com (target), the window object isn't reused. But starting from the same initial document and navigating to https://aogarantiza.com (same-origin) does result in reuse.

My question is whether window reuse (or lack of reuse) is only renderer-enforced (in the code you referenced or elsewhere), in which case a compromised renderer could then set window properties on the site (which is limited UXSS?), or if this is also enforced by the browser via process swap due to incompatible process locks (without browser the process swap, I think the commit would be blocked, like in the docwrite1/docwrite2 scenarios which kill the renderer).

### al...@alesandroortiz.com (2022-04-01)

engedy@: Also thanks for confirming that last_committed_origin_ was incorrectly set in https://crbug.com/chromium/1311820#c15. I strongly suspected yesterday that something (later identified in https://crbug.com/chromium/1311820#c24) was setting this to an incorrect value, but didn't have a recent local build to confirm the state.

### cr...@chromium.org (2022-04-01)

The fix looks good. 

I'm also wondering whether other callers of GetOriginalOpener are problematic?

It appears that most callers only pass the result to WebContents::FromRenderFrameHost, so they don't care which frame in the WebContents in the actual owner.  The call in performance_manager_tab_helper.cc might be wrong, but I'm not sure if that has security implications.  I'm also nervous about this part of the comment:
  // ... This traces all the way back, so if the original owner was closed,
  // but _it_ had an original owner, this will return the original owner's
  // original owner, etc.
That suggests it might not even return the WebContents that some of the call sites might be expecting.  This seems like a difficult API to use safely, so it needs at least a rename (as rakina@ notes in the CL) or possibly a different way to solve https://crbug.com/chromium/705316.  That will be a good followup item.

Separately, I wondered why doesn't the bug occur for actual navigations to "about:blank" (or for navigations to "").  It appears that we do set the wrong origin in the popup's RenderFrameHost when creating the RenderFrameHost, but we then correct it to the subframe opener's origin when we get a subsequent DidCommitNavigation for the about:blank page.  That explains why the bug only affects cases where there's no actual commit in the popup, which (as rakina@ shows in the test) means it also affects URLs that return 204 No Content, or for URLs that turn out to be downloads.

### [Deleted User] (2022-04-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2022-04-04)

Thanks all!

re https://crbug.com/chromium/1311820#c26: 
> My question is whether window reuse (or lack of reuse) is only renderer-enforced (in the code you referenced or elsewhere), in which case a compromised renderer could then set window properties on the site (which is limited UXSS?), or if this is also enforced by the browser via process swap due to incompatible process locks (without browser the process swap, I think the commit would be blocked, like in the docwrite1/docwrite2 scenarios which kill the renderer).

Yes, the window reuse is renderer-enforced, but I think the renderer process & SiteInstance that the popup is assigned to is actually correct (the popup will use the same process as the subframe opener) as it's not affected by the code moved in my CL, so a compromised renderer won't be able to access cross-site data. Cross-document navigations will compare against the RFH's SiteInstance instead of last_committed_origin_, so the new document will commit in the correct process too, so luckily don't have problems in that area.

re https://crbug.com/chromium/1311820#c28: Yep, I took a look at crbug.com/705316 and it seems like it is the way it is for popup/popunder blocking code that doesn't exist anymore. I'll try to change it to track WebContents (or maybe FrameTree?) which was already suggested in crbug.com/705316#c3 anyways.

### gi...@appspot.gserviceaccount.com (2022-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4eb716ef5cdbca4db3a9377ee6390964d0d4025f

commit 4eb716ef5cdbca4db3a9377ee6390964d0d4025f
Author: Rakina Zata Amni <rakina@chromium.org>
Date: Tue Apr 05 21:32:46 2022

Don't use GetOriginalOpener to get opener's origin on FrameTree initialization

When setting the origin of the new main RFH on FrameTree initialization,
we base it on the opener's origin if it exists. GetOriginalOpener()
was used to get the opener, but that function will actually return the
main frame of the opener. This means when the FrameTree is opened by a
non-main frame, we might inherit the wrong origin.

This CL fixes the bug by getting the actual opener using GetOpener()
instead, and adds a regression test and warning note to
GetOriginalOpener().

Bug: 1311820, 1291764
Change-Id: I7e6f63a394ba4188eee3ce3043b174a2695508eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3564826
Reviewed-by: Charlie Reis <creis@chromium.org>
Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
Cr-Commit-Position: refs/heads/main@{#989165}

[modify] https://crrev.com/4eb716ef5cdbca4db3a9377ee6390964d0d4025f/content/browser/renderer_host/render_frame_host_impl_browsertest.cc
[modify] https://crrev.com/4eb716ef5cdbca4db3a9377ee6390964d0d4025f/content/browser/renderer_host/frame_tree.h
[modify] https://crrev.com/4eb716ef5cdbca4db3a9377ee6390964d0d4025f/content/public/browser/web_contents.h
[modify] https://crrev.com/4eb716ef5cdbca4db3a9377ee6390964d0d4025f/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/4eb716ef5cdbca4db3a9377ee6390964d0d4025f/content/browser/renderer_host/frame_tree.cc


### al...@alesandroortiz.com (2022-04-14)

Hi folks, apologies for radio silence. I was out sick with COVID, 95% recovered now.

I verified the https://crbug.com/chromium/1311820#c31 fix using the JS dialog PoC on 102.0.5002.2 Canary and a local build.

Will provide additional PoCs within a few days (dependent on my recovery), and continue impact analysis now that I have a working Chromium build environment again.

### al...@alesandroortiz.com (2022-04-17)

Attached PoCs for XFO sameorigin, CSP frame-ancestors 'self', and various permission check + permission prompt origin spoofs..

Repro steps for most permission prompt scenarios:
1. Navigate to https://alesandroortiz.com/security/chromium/rfh-origin-spoof.html
2. Select any of the permission scenarios.
3. Click anywhere in iframe (or press any key that provides user activation).
4. (For some permission prompts: Click in the new window/tab if the permission prompt requires user activation, as instructed on the page.)

Observed: Permission prompt shows hostname of top-most frame origin.
Expected: Permission prompt shows hostname of initiator origin, which is the iframe origin.

Repro steps for permission check bypass (using camera permission scenario):
1. Navigate to https://alesandroortiz.com/security/chromium/rfh-origin-spoof.html?permission-camera (camera permission scenario)
2. Click anywhere in iframe (or press any key that provides user activation).
3. Allow camera permission for spoofed top-most frame origin (https://alesandroortiz.com)
4. Perform steps 1-2 again.

Observed: If the spoofed origin already has the permission allowed, after step 2 the attacker page can immediately gain access to data allowed for the spoofed origin. In other words, if https://alesandroortiz.com already has camera access, and the malicious iframe on https://aogarantiza.com performs the attack, the iframe can immediately gain camera access without any additional user interaction or prompts.
Expected: If the spoofed origin already has the permission allowed, after step 2 the attacker page still requires permission based on the attacker origin.

Repro steps for X-Frame-Origin: sameorigin bypass:
1. Navigate to https://alesandroortiz.com/security/chromium/rfh-origin-spoof.html?xfo-sameorigin (protected iframe: https://alesandroortiz.com/security/chromium/xfo-same-origin-frame.html )
2. Click anywhere in iframe (or press any key that provides user activation).

Repro steps for Content-Security-Policy: frame-ancestors 'self' bypass:
1. Navigate to https://alesandroortiz.com/security/chromium/rfh-origin-spoof.html?csp-frame-ancestors (protected iframe: https://alesandroortiz.com/security/chromium/csp-frame-ancestors-frame.html )
2. Click anywhere in iframe (or press any key that provides user activation).

For both XFO sameorigin and CSP frame-ancestors bypass:
Observed: The protected iframe with the corresponding header is allowed to be embedded by attacker origin (https://aogarantiza.com) because browser thinks it's embedded by spoofed origin (https://alesandroortiz.com)
Expected: The protected iframe with the corresponding header is not allowed to be embedded by attacker origin (https://aogarantiza.com)

Repro steps for Android Contacts permission prompt scenario:
1. On Android, navigate to https://alesandroortiz.com/security/chromium/rfh-origin-spoof.html?permission-contacts
2. Click anywhere in iframe.
3. Click on the new tab since permission requires user activation.

Observed: Contacts permission propt shows hostname of top-most frame origin.
Expected: Contacts permission prompt shows hostname of initiator origin, which is the iframe origin.

### al...@alesandroortiz.com (2022-04-20)

Hi folks, will this be merged to Stable and other supported versions?

I've identified additional impacts, most of which require a compromised renderer. I'll submit complete PoCs this week.

* Cookies: read/write access to spoofed origin
* postMessage: can send and receive messages as spoofed origin. Send: https://attacker.com can send message to https://example.com and source origin is set to spoofed https://example.com origin. Receive: https://attacker.com can receive message sent by https://example.com using postMessage(msg, 'https://example.com')
* IndexedDB: read/write access to spoofed origin database
* BackgroundChannel: allows attacker to send and receive messages to/from spoofed origin BroadcastChannels (requires knowing channel name, not a hurdle if code uses static name; not sure if dynamic name can be discovered without bruteforcing)
* WebSockets: spoofed origin header

In general, anything that checks the process lock is secure, since that is not spoofed. Otherwise, anything that only checks against storage key or isolation info is affected, which is a large number of areas. Still performing further impact analysis, since some of the likely impacted areas require more complex simulated renderer exploits which I'm still figuring out.

RenderFrameHostImpl::SetOriginDependentStateOfNewFrame(), which is passed the spoofed origin, sets the storage key, isolation info, and last committed origin for the RFH here:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=3864;drc=6782d9e010c9f3ad7a442169ee9f574bbdca6ee6

### al...@alesandroortiz.com (2022-04-20)

[Comment Deleted]

### ra...@chromium.org (2022-04-21)

Thanks Alesandro, and sorry for the lack of replies, I've been out sick as well. Let me request to merge crrev.com/c/3564826, and send some follow-up CLs to improve GetOriginalOpener() soon.

### [Deleted User] (2022-04-21)

Merge review required: M101 has already been cut for stable release.

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
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-21)

Merge review required: M100 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2022-04-21)

1. Why does your merge fit within the merge criteria for these milestones?
It's a security bug with high severity (origin confusion on new popups)

2. What changes specifically would you like to merge? Please link to Gerrit.
crrev.com/c/3564826

3. Have the changes been released and tested on canary?
Yes, it got into 102.0.4987.0 

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No


### [Deleted User] (2022-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-23)

merges to M101 and M100 approved as this fix has been on canary for 17 days; please merge this fix to branch 4951 (M101) and 4896 (M100) at your earliest availability so this fix can be in the first security respin for M101 Stable and M100 Extended

### gi...@appspot.gserviceaccount.com (2022-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/432027aab772952238842f73730f166aaaea1026

commit 432027aab772952238842f73730f166aaaea1026
Author: Rakina Zata Amni <rakina@chromium.org>
Date: Mon Apr 25 05:56:35 2022

[Merge to M101] Don't use GetOriginalOpener to get opener's origin on FrameTree initialization

When setting the origin of the new main RFH on FrameTree initialization,
we base it on the opener's origin if it exists. GetOriginalOpener()
was used to get the opener, but that function will actually return the
main frame of the opener. This means when the FrameTree is opened by a
non-main frame, we might inherit the wrong origin.

This CL fixes the bug by getting the actual opener using GetOpener()
instead, and adds a regression test and warning note to
GetOriginalOpener().

(cherry picked from commit 4eb716ef5cdbca4db3a9377ee6390964d0d4025f)

Bug: 1311820, 1291764
Change-Id: I7e6f63a394ba4188eee3ce3043b174a2695508eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3564826
Reviewed-by: Charlie Reis <creis@chromium.org>
Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#989165}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3599936
Auto-Submit: Rakina Zata Amni <rakina@chromium.org>
Reviewed-by: Nidhi Jaju <nidhijaju@chromium.org>
Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
Owners-Override: Nidhi Jaju <nidhijaju@chromium.org>
Cr-Commit-Position: refs/branch-heads/4951@{#1029}
Cr-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}

[modify] https://crrev.com/432027aab772952238842f73730f166aaaea1026/content/browser/renderer_host/frame_tree.h
[modify] https://crrev.com/432027aab772952238842f73730f166aaaea1026/content/browser/renderer_host/render_frame_host_impl_browsertest.cc
[modify] https://crrev.com/432027aab772952238842f73730f166aaaea1026/content/public/browser/web_contents.h
[modify] https://crrev.com/432027aab772952238842f73730f166aaaea1026/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/432027aab772952238842f73730f166aaaea1026/content/browser/renderer_host/frame_tree.cc


### [Deleted User] (2022-04-25)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2941a90229d258462afa72bb62e5cbe1691e57ea

commit 2941a90229d258462afa72bb62e5cbe1691e57ea
Author: Rakina Zata Amni <rakina@chromium.org>
Date: Mon Apr 25 06:18:19 2022

[Merge to M100] Don't use GetOriginalOpener to get opener's origin on FrameTree initialization

When setting the origin of the new main RFH on FrameTree initialization,
we base it on the opener's origin if it exists. GetOriginalOpener()
was used to get the opener, but that function will actually return the
main frame of the opener. This means when the FrameTree is opened by a
non-main frame, we might inherit the wrong origin.

This CL fixes the bug by getting the actual opener using GetOpener()
instead, and adds a regression test and warning note to
GetOriginalOpener().

(cherry picked from commit 4eb716ef5cdbca4db3a9377ee6390964d0d4025f)

Bug: 1311820, 1291764
Change-Id: I7e6f63a394ba4188eee3ce3043b174a2695508eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3564826
Reviewed-by: Charlie Reis <creis@chromium.org>
Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#989165}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3600157
Auto-Submit: Rakina Zata Amni <rakina@chromium.org>
Reviewed-by: Nidhi Jaju <nidhijaju@chromium.org>
Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
Owners-Override: Nidhi Jaju <nidhijaju@chromium.org>
Cr-Commit-Position: refs/branch-heads/4896@{#1179}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/2941a90229d258462afa72bb62e5cbe1691e57ea/content/browser/renderer_host/frame_tree.h
[modify] https://crrev.com/2941a90229d258462afa72bb62e5cbe1691e57ea/content/browser/renderer_host/render_frame_host_impl_browsertest.cc
[modify] https://crrev.com/2941a90229d258462afa72bb62e5cbe1691e57ea/content/public/browser/web_contents.h
[modify] https://crrev.com/2941a90229d258462afa72bb62e5cbe1691e57ea/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/2941a90229d258462afa72bb62e5cbe1691e57ea/content/browser/renderer_host/frame_tree.cc


### rz...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### rz...@google.com (2022-04-25)

Fixed code isn't present on M96

### al...@alesandroortiz.com (2022-04-27)

Status update: I'm still working on the PoCs, and have found additional impacts. Will provide an update as soon as possible (still recovering from COVID, so not working every day).

Feel free to delay reward decision for a week or two until I have finished submitting PoCs and completed impact analysis. I'll indicate in the future when my analysis is complete (and probably provide a summary since it's scattered across comments).

(wfh@ reached out to me about this, so leaving here for posterity.)

### gi...@appspot.gserviceaccount.com (2022-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3a48ae495c67e516af53ed92f079ef1dfe551833

commit 3a48ae495c67e516af53ed92f079ef1dfe551833
Author: Rakina Zata Amni <rakina@chromium.org>
Date: Thu May 05 03:39:56 2022

Make 'original opener' functions a bit clearer

The term 'original opener' is a bit confusing as it has a lot of
subtleties (tracking live main frame in the opener chain, etc). This CL
attempts to clarify the functions that expose the 'original opener' by
explicitly calling out the subtleties in the name and modifying the
comments. This CL does not change any functionality of the functions
(except changing one function to return WebContents instead of RFH).

Bug: 1311820
Change-Id: I9ec6e7b9493627c6ec7642e54578994135be4551
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3624259
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
Reviewed-by: Chris Hamilton <chrisha@chromium.org>
Cr-Commit-Position: refs/heads/main@{#999737}

[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/content/browser/net/cross_origin_opener_policy_reporter.cc
[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/content/browser/web_contents/web_contents_impl_browsertest.cc
[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/chrome/browser/devtools/devtools_window.cc
[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/content/public/browser/web_contents.h
[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/content/browser/renderer_host/frame_tree_node.cc
[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/content/browser/renderer_host/render_frame_host_manager_browsertest.cc
[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/chrome/browser/ui/blocked_content/popunder_preventer.cc
[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/content/browser/renderer_host/frame_tree_node.h
[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/components/performance_manager/performance_manager_tab_helper.cc
[modify] https://crrev.com/3a48ae495c67e516af53ed92f079ef1dfe551833/content/browser/devtools/render_frame_devtools_agent_host.cc


### am...@chromium.org (2022-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-16)

Hello Alesandro, reached out directly via email but reminder to please provide any additional POCs for consideration by EOD Monday, 23 May so we can make a finalized reward decision. 

### al...@alesandroortiz.com (2022-05-22)

I'm finalizing the PoCs and will submit them by EOD Monday, but had unexpected issues with the XFO, CSP, and postMessage PoCs using a build of tag 102.0.4986.0.

For some reason, https://alesandroortiz.com/security/chromium/rfh-origin-spoof.html?xfo-sameorigin *does* repro on build 989138 from https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/989138/ (also repros with ASan build 989137) but *does not* repro on my build of tag 102.0.4986.0 (6e809c51f21ef770b2ad4d552f9089d0940dc716). The repro failures are due to CORS lock vs initiator check failures at https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/initiator_lock_compatibility.cc;l=54;drc=e4ee4155a3981eea3c01194d24748e97429530df probably when performing the iframe navigation.

This unexpected behavior difference affects the XFO, CSP, and postMessage PoCs.
* The XFO and CSP PoCs are reproducible without a compromised renderer using build 989138.
* The postMessage PoC requires a compromised renderer to *receive* messages from the target origin, therefore this *should* work on a main branch checkout with renderer modifications. Sending messages with spoofed origin probably won't work due to browser-side checks.

Is there any relevant difference between checking out a tag and checking out main branch, if both don't appear to have the fix from commit 4eb716ef5cdbca4db3a9377ee6390964d0d4025f? After Wednesday, I'll try to do a main branch checkout with enough history to checkout the commit immediately prior to the fix to see if I can repro the postMessage PoC like I did in mid-April (#c34).

### al...@alesandroortiz.com (2022-05-22)

Also worth noting the repro video from https://crbug.com/chromium/1311820#c33 is from latest Stable at that date, which according to https://chromiumdash.appspot.com/releases?platform=Windows was 100.0.4896.127 and I was able to repro the XFO and CSP PoCs there.

### al...@alesandroortiz.com (2022-05-23)

Additional impacts and PoCs below. I'll provide a summary of all identified impacts and PoCs in a follow-up comment.

Not requiring compromised renderer:
* IndexedDB: read + write access to spoofed origin
* CacheStorage (self.caches): read + write access to spoofed origin
* BroadcastChannel: send + receive messages on spoofed origin's channel
* WebSockets: spoofed origin header on requests

Requiring compromised renderer:
* Cookies: read + write access to spoofed origin
* SharedWorkers: connect to existing SharedWorker created by target origin
* SharedWorkers: create SharedWorker with arbitrary code, send + receive messages to/from target, obtain a URL loader for spoofed origin

Details below:

===== Scenarios not requiring compromised renderer =====
Setup for scenarios not requiring compromised renderer:
1. Download and install/use known-vulnerable version of Chromium (prior to r989165 / 4eb716ef5cdbca4db3a9377ee6390964d0d4025f). For Windows, I used https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/989138/

=== IndexedDB: read + write access to spoofed origin ===
IndexedDBs might contain sensitive data from target. Tampered data used by target might also cause unwanted behavior in target.

Line where spoofed storage_key is used for IndexedDB: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/indexed_db/database_impl.cc;l=50;drc=36f2c0dfbc7fe2b88e2f34f0c06fb48b44eff6f4

Repro steps:
* Optional: Before interacting with iframe, create initial IndexedDB on target origin: https://alesandroortiz.com/security/chromium/set-cookie-idb.html
1. Navigate to https://alesandroortiz.com/security/chromium/rfh-origin-spoof-pt2.html?indexeddb
2. Click within iframe (or press any key) to open window and run PoC.
* Optional: Inspect IndexedDB by opening DevTools for alesandroortiz.com -> Application -> IndexedDB.

Observed: Popup with spoofed origin can read and write IndexedDBs for spoofed origin.
Expected: Attacker code cannot read or write IndexedDBs for another origin.

=== CacheStorage (self.caches): read + write access to spoofed origin ===
CacheStorage is typically used by ServiceWorkers to cache requests, but can also be used by windows or other worker types for other purposes.
Existing cache entries may contain sensitive data.
Tampered cache entries can result in code execution or other unwanted behavior if the tampered entry is used by the target. For example, a ServiceWorker may use the tampered entry for a page load resulting in attacker content and code running.

Line where spoofed storage_key is used for CacheStorage:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_process_host_impl.cc;l=1883;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437
Called by RFHI (for window): https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=10254;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437
Called by SharedWorkerHost: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/shared_worker_host.cc;l=475;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437
Other worker types seem to use similar logic, so they're likely affected.

Repro steps:
1. Navigate to https://alesandroortiz.com/security/chromium/rfh-origin-spoof-pt2.html?cachestorage
2. Click within iframe (or press any key) to open window and run PoC.
* Optional: Inspect CacheStorage by opening DevTools for alesandroortiz.com -> Application -> CacheStorage.

Observed: Popup with spoofed origin can read and write CacheStorage for spoofed origin.
Expected: Attacker code cannot read or write CacheStorage for another origin.

=== BroadcastChannel: send + receive messages on spoofed origin's channel ===
Channel name must be known. This is not a hurdle if channel name is static. If dynamically generated, bruteforcing might be possible.
Target may send sensitive data to the channel, which is received by attacker.
Attacker can also send messages to the channel, which may result in unwanted behavior or tampered data in target.

Line where spoofed storage_key is used for BroadcastChannel: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/broadcast_channel/broadcast_channel_provider.cc;l=27;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437
Called by RFHI (for window): https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=8824;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437
Called by SharedWorkerHost: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/shared_worker_host.cc;l=490;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437
Other worker types seem to use similar logic, so they're likely affected.

Repro steps:
1. Before or after interacting with iframe, open BroadcastChannel on target origin (keep page open when running PoC): https://alesandroortiz.com/security/chromium/broadcast-channel.html
2. Navigate to https://alesandroortiz.com/security/chromium/rfh-origin-spoof-pt2.html?broadcastchannel
3. Click within iframe (or press any key) to open window and run PoC.

Observed: Popup with spoofed origin can send and receive messages on target origin's BroadcastChannel. PoC output indicates attacker page successfully receives messages sent by target page and vice versa.
Expected: Attacker code can only send and receive messages on attacker origin's BroadcastChannel.

=== WebSockets: spoofed origin header on requests ===
WebSocket requests use spoofed origin header. Unclear about impacts other than bypassing server-side origin checks that trust the origin header.

Repro steps:
1. Navigate to https://alesandroortiz.com/security/chromium/rfh-origin-spoof.html (the PoC doesn't matter)
2. Click within iframe (or press any key) to open window with spoofed origin.
3. Open DevTools console for popup.
4. In console, run: `new WebSocket('wss://example.com')`.
5. In DevTools network tab, click the WebSocket request and observe the request headers.

Observed: Origin header is of spoofed origin (https://alesandroortiz.com)
Expected: Origin header is of attacker origin (https://aogarantiza.com)

===== Scenarios requiring compromised renderer =====
Setup for scenarios requiring compromised renderer:
1. Checkout Chromium HEAD from tag 102.0.4986.0 or commit 248158e6ec0e618a30f01e311cf1b9815ba51bce from main branch, which do not contain the fix from r989165 / commit 4eb716ef5cdbca4db3a9377ee6390964d0d4025f. I've verified these steps with the tag checkout method.
2. Apply the attached renderer.patch using `git apply renderer.patch`. Some parts of the patch are required for all PoCs, other parts are required only for specific PoCs, but for simplicity I've made a single patch file.
3. Optional: Apply the attached browser.patch using `git apply browser.patch`. This adds browser-side logging that does not affect behavior. Helps verify the state of the URL loader in the SharedWorker scenario.
4. Build Chromium after applying patches.
5. Use the patched Chromium build when running these PoCs.

=== Cookies: read + write access to spoofed origin (with compromised renderer) ===
This requires compromised renderer. Cookies might contain sensitive data from target. Tampered data used by target might also cause unwanted behavior in target.

CookieJar::Cookies() reads cookies: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/cookie_jar.cc;l=76;drc=07ba20653612c99122c4f741c7cc1d58c0fe755d
CookieJar::SetCookie() writes cookies: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/cookie_jar.cc;l=54;drc=07ba20653612c99122c4f741c7cc1d58c0fe755d

They both call RestrictedCookieManager with spoofed renderer-side values to match the spoofed browser-side origin: https://source.chromium.org/chromium/chromium/src/+/main:services/network/restricted_cookie_manager.cc;l=824;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437

RestrictedCookieManager::ValidateAccessToCookiesAt() checks renderer-provided values against spoofed origin, which succeeds: https://source.chromium.org/chromium/chromium/src/+/main:services/network/restricted_cookie_manager.cc;l=869;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437

RestrictedCookieManager is created with spoofed origin and isolation info here: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=10278;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437

Repro steps:
* Optional: Before interacting with iframe, set initial cookie on target origin: https://alesandroortiz.com/security/chromium/set-cookie-idb.html
1. Navigate to https://alesandroortiz.com/security/chromium/rfh-origin-spoof-pt2.html?cookie
2. Click within iframe (or press any key) to open window and run PoC.
* Optional: Inspect cookies by opening DevTools for alesandroortiz.com -> Application -> Cookies.

Observed: Popup with spoofed origin + compromised renderer can read and write cookies for spoofed origin.
Expected: Attacker code cannot read or write cookies for another origin.

=== SharedWorkers: connect to existing SharedWorker created by target origin (with compromised renderer) ===
This requires compromised renderer. If an attacker knows the URL (and name if relevant) of an existing SharedWorker created by the target origin, they can connect to the existing SharedWorker. This allows the attacker to send + receive messages to/from the worker.

* Worker is created by target page, therefore it's running on target page's process. Attacker cannot tamper with worker's executed code directly.
* Attacker page can send messages to target's existing worker to perform sensitive actions or tamper with data.
* Attacker page can receive messages from target's existing worker containing sensitive data.

Page JS runs `new SharedWorker(url)`. This causes renderer to make SharedWorkerConnector::Connect() call to browser, handled by browser here: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/shared_worker_connector_impl.cc;l=35;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437
The call has spoofed URL info to match the URL of the existing worker (e.g. https://alesandroortiz.com/security/chromium/shared-worker.js)

That eventually calls SharedWorkerServiceImpl::ConnectToWorker(): https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/shared_worker_service_impl.cc;l=113;drc=b41db61995ded8bd8ee37dfba0c09d7c17d78e55

This security check is bypassed, since renderer-provided URL's origin will match spoofed storage_key:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/shared_worker_service_impl.cc;l=136;drc=b41db61995ded8bd8ee37dfba0c09d7c17d78e55

Then tries to find existing worker using FindMatchingSharedWorkerHost() with renderer-provided URL: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/shared_worker_service_impl.cc;l=156;drc=b41db61995ded8bd8ee37dfba0c09d7c17d78e55

Which checks existing workers for matching storage_key, URL, and name (if provided):
https://source.chromium.org/chromium/chromium/src/+/main:content/public/browser/shared_worker_instance.cc;l=49;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437

If an existing worker is found, the browser will add the page as a client: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/shared_worker_service_impl.cc;l=178;drc=b41db61995ded8bd8ee37dfba0c09d7c17d78e55

Repro steps:
1. Before interacting with iframe, open SharedWorker on target origin: https://alesandroortiz.com/security/chromium/shared-worker.html
2. Click within iframe (or press any key) to open window and run PoC.
* Optional: Open the Task Manager to observe the SharedWorker is running in the same process as the target page (safe).
* Optional: Go to chrome://inspect/#workers to inspect the SharedWorker.

Observed: Popup with spoofed origin + compromised renderer can send and receive messages to/from SharedWorker on spoofed origin.
Expected: Attacker code cannot send or receive messages to/from SharedWorker for another origin.

=== SharedWorkers: create SharedWorker with arbitrary code, send + receive messages, obtain a URL loader for spoofed origin (with compromised renderer) ===
This requires compromised renderer. Attacker can create SharedWorker running in same process as attacker page. This SharedWorker will use the spoofed storage_key and obtain a URL loader for the spoofed origin from the browser.

This allows an attacker to do all of the following:
* Create a SharedWorker even if the target origin does not respond with valid SharedWorker JS code.
  * Attacker can run a worker without valid SharedWorker code on the target origin. Only prerequisite is an HTTP status code 200 response.
  * SharedWorkers are created in same renderer process as attacker page. The renderer process controls the executed code in the SharedWorker. Therefore, an attacker can arbitrarily set the executed code if an existing SharedWorker at the URL is not running.
* Send + receive messages to/from target's client pages that connect to the attacker's SharedWorker.
  * Attacker can create a SharedWorker with attacker-controlled code at any URL within target origin (see prior item in list).
  * If an attacker page tries to connect to a SharedWorker at the same URL, the browser will connect the target page to the attacker's SharedWorker.
  * Attacker worker can send messages to target's client pages to perform sensitive actions or tamper with data.
  * Attacker worker can receive messages from target's client pages containing sensitive data.
  * If there's an existing target-controlled SharedWorker at the URL the attacker wants to impersonate, the attacker can indirectly stop the SharedWorker by crashing the network process. They can do this by intentionally creating a CORS lock failure in the popup with: caches.open('v1').then(function(cache) { return cache.add('https://alesandroortiz.com/'); }); After stopping the worker, the attacker can create its own worker to replace the original worker.
* Obtain a URL loader for the spoofed origin.
  * This URL loader can make HTTP requests to target origin with target origin's cookies (including HttpOnly cookies) and read responses while bypassing CORS checks.

Similar to the previous SharedWorker scenario, after page JS runs `new SharedWorker(url)`, the browser goes through the same steps except it will not find an existing worker.

When there's no existing worker, the browser will create a SharedWorker using the spoofed storage_key and the renderer-provided URL: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/shared_worker_service_impl.cc;l=192;drc=b41db61995ded8bd8ee37dfba0c09d7c17d78e55

SharedWorkerServiceImpl::CreateWorker() will create the SharedWorker in the process provided by the SiteInstance, which is the process of the attacker page:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/shared_worker_service_impl.cc;l=289;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/shared_worker_service_impl.cc;l=315;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437

WorkerScriptFetcher::CreateAndStart() creates a subresource URL loader factory based on the spoofed storage_key and other spoofed values. This URL loader allows the SharedWorker to perform HTTP requests as the origin without triggering CORS checks.
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/worker_script_fetcher.cc;l=262;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437

Goes through a bunch of callbacks until it ends up here:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/shared_worker_service_impl.cc;l=390;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437

Then the URL loader is sent to the renderer: 
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/worker_host/shared_worker_host.cc;l=339;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/worker/shared_worker_factory.mojom;l=80;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437

And used by the renderer:
https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/worker/embedded_shared_worker_stub.cc;l=99;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437
https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/worker/embedded_shared_worker_stub.cc;l=114;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437
https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/worker/embedded_shared_worker_stub.cc;l=173;drc=fbd2df0534c28fd59aed44421d6f3fbeda89c437
(and passed along much further until it's used by fetch() in JS, but a compromised renderer could use it as soon as it's sent by the browser)

In the PoC with renderer.patch applied, the renderer overrides the source in https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/workers/worker_classic_script_loader.cc;l=334;drc=ab1268c40421a390b722774f40f103cf4b2b04cc to return the following payload:
```
console.info('This is renderer-overridden /?sharedworker');var ports = [];
onconnect=(e) => {
  console.info('onconnect:', e);var port = e.ports[0];ports.push(port);
  port.addEventListener('message', (e) => {
    console.info('message:', e);var workerResult = 'Result (from compromised worker): ' + ((e.data[0] * e.data[1]) + 5000);ports.forEach((port) => {port.postMessage(workerResult);});
  });
  port.start();
  fetch('https://alesandroortiz.com/.netlify/functions/echo-cookies')
  .then(r => r.text()).then(r => { console.info(r); ports.forEach((port) => { port.postMessage('Response from target origin with cookies: ' + r); }); });
}
```
The echo-cookies URL will respond with the cookies received in the HTTP request, which demonstrates that the browser is sending the target origin's cookies in a request initiated by the attacker.

Repro steps:
1. Click within iframe (or press any key) to open window and run PoC.
2. After interacting with iframe, open SharedWorker (2) on target origin: https://alesandroortiz.com/security/chromium/shared-worker-2.html
3. Open the Task Manager to observe the SharedWorker is running in the same process as the attacker page (unsafe).
* Optional: Go to chrome://inspect/#workers to inspect the SharedWorker.

Observed: Popup with spoofed origin + compromised renderer can:
  * create SharedWorker for spoofed origin, with arbitrary code, on same process as attacker page
  * send and receive messages to/from target's client pages
  * obtain URL loader for spoofed origin and use it to perform HTTP requests to target origin with full cookies

Expected: Attacker code cannot create SharedWorker for another origin and cannot obtain URL loader for another origin.

### al...@alesandroortiz.com (2022-05-23)

Attached video for scenarios requiring compromised renderer.

### al...@alesandroortiz.com (2022-05-23)

As noted in https://crbug.com/chromium/1311820#c34, anything that uses the browser-side spoofed storage key, isolation info, and last committed origin without additional robust security checks (mainly process locks) is affected:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=3864;drc=6782d9e010c9f3ad7a442169ee9f574bbdca6ee6

This list is not exhaustive, but other areas I didn't check likely would have had equivalent impacts as these areas.

Summary of identified impacts and provided PoCs:

Verified on build 989138 (not requiring compromised renderer):
1. JS dialogs: origin spoof (original report)
2. Permission prompt origin spoof (#c33)
    * Including Android Contacts permission prompt origin spoof.
3. Permission check bypass if spoofed origin had permission previously granted (#c33)
4. X-Frame-Options: sameorigin bypass (#c33)
5. Content-Security-Policy: frame-ancestors 'self' bypass (#c33)
6. IndexedDB: read + write access to spoofed origin (#c55)
7. CacheStorage (self.caches): read + write access to spoofed origin (#c55)
    * Typically used by ServiceWorkers to cache responses, but can also be used by windows or other worker types for other purposes.
8. BroadcastChannel: send + receive messages on spoofed origin's channel
  * Channel name must be known (not a hurdle if static name)
9. WebSockets: spoofed origin header on requests (#c55)

Verified on checkout of tag 102.0.4986.0, with simulated compromised renderer:
10. Cookies: read + write access to spoofed origin (#c55)
11. SharedWorkers: connect to existing SharedWorker created by target origin (#c55)
  * Worker is created by target page, therefore it's running on target page's process. Attacker cannot tamper with worker's executed code directly.
  * Attacker page can send messages to target's existing worker to perform sensitive actions or tamper with data.
  * Attacker page can receive messages from target's existing worker containing sensitive data.
12. SharedWorkers: create SharedWorker with arbitrary code, send + receive messages to/from target, obtain a URL loader for spoofed origin (#c55)
  * Worker is created by attacker page, therefore it's running on attacker page's process. Attacker can tamper with worker's executed code directly.
    * Attacker can run a worker without valid SharedWorker code on the target origin, since compromised renderer can arbitrarily set executed code. Only prerequisite is an HTTP status code 200 response.
    * If an existing worker is running, an attacker can indirectly stop the worker by crashing the network process. After stopping the worker, the attacker can create its own worker to replace the original worker.
  * Attacker worker can send messages to target's client pages to perform sensitive actions or tamper with data.
  * Attacker worker can receive messages from target's client pages containing sensitive data.
  * Attacker worker can make HTTP requests to target origin with target origin's cookies (including HttpOnly cookies) and read responses while bypassing CORS checks.
  
Will need to re-verify using main branch checkout without fix, with simulated compromised renderer:
13. postMessage: receive messages from spoofed origin with postMessage(msg, targetOrigin)

Unconfirmed impact:
* ServiceWorkers: SharedWorkers seem to have the necessary information to create a ServiceWorker on the spoofed origin (similar to how they obtain a URL loader for the spoofed origin). I tried verifying this, but the C++ code around this is complex and I haven't gotten it to fully work yet. But I haven't identified any security checks that would prevent this from being successful.

### al...@alesandroortiz.com (2022-05-23)

Feel free to send this to the reward panel now since I think I've maximized the impact, other than the unconfirmed ServiceWorker impact in https://crbug.com/chromium/1311820#c57 which seems likely but I haven't been able to fully verify due to my limited C++ skills and code complexity. I can provide more information on the theoretical impact and my partially-working code if someone on the Chromium team wants to take a look at it further.

### am...@google.com (2022-05-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-27)

Congratulations, Alesandro and Sameer! The VRP Panel has decided to award you $20,000 for this report. Thank you for your efforts in your discovery and reporting of this site isolation bypass issue and excellent work! 

### al...@alesandroortiz.com (2022-05-27)

Thanks for the reward! Really appreciate it.

### am...@chromium.org (2022-05-27)

We really appreciate your fantastic report and this awesome finding! :) 

### al...@alesandroortiz.com (2022-05-28)

Update on https://crbug.com/chromium/1311820#c53: Issue reproducing some PoCs turned out to be caused by my renderer patch (from https://crbug.com/chromium/1311820#c55) modifying document_loader.cc in a way that triggered the renderer kill.

I can repro XFO and CSP PoCs using a clean build of tag 102.0.4986.0. I'm also able to repro postMessage PoC with a compromised renderer using a patch without the document_loader.cc modifications. I've attached the patch specifically for the postMessage PoC.

Technically the renderer process receives the message even without a compromised renderer, but a compromised renderer is probably the only way to read and use the received message.

Setup for scenarios requiring compromised renderer:
1. Checkout Chromium HEAD from tag 102.0.4986.0 or commit 248158e6ec0e618a30f01e311cf1b9815ba51bce from main branch, which do not contain the fix from r989165 / commit 4eb716ef5cdbca4db3a9377ee6390964d0d4025f. I've verified these steps with the tag checkout method.
2. Apply the attached renderer-postmessage.patch using `git apply renderer-postmessage.patch`.
3. Build Chromium after applying patches.
4. Use the patched Chromium build when running these PoCs.

Repro steps:
1. Navigate to https://alesandroortiz.com/security/chromium/rfh-origin-spoof-pt3.html?postmessage
2. Click within the iframe (or press any key) to open window and run PoC.
* Optional: Open DevTools console to observe error messages that would usually be thrown by renderer.

Observed: Popup with spoofed origin can receive postMessages from iframes or other sources intended for spoofed origin (when target page uses postMessage(msg, targetOrigin)). A compromised renderer allows attacker to read and use the message.
Expected: Renderer cannot receive postMessages intended for another origin.

### al...@alesandroortiz.com (2022-05-28)

Receiving postMessages intended for the spoofed origin is possible because the browser checks the origin of the recipient here, which is set to the spoofed origin: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_proxy_host.cc;l=513;drc=7fb345a0da63049b102e1c0bcdc8d7831110e324

Sending postMessages as the spoofed origin is not possible due to the check a few lines below: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_proxy_host.cc;l=520;drc=7fb345a0da63049b102e1c0bcdc8d7831110e324

### am...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1311820?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, UI>Browser>Navigation, UI>Browser>Permissions]
[Monorail components added to Component Tags custom field.]

### th...@gmail.com (2025-07-25)

redacted

### th...@gmail.com (2025-08-16)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059251)*
