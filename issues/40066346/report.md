# Initiator origin not shown in external protocol dialog with context menu open in new window / open in incognito window options inside an iframe

| Field | Value |
|-------|-------|
| **Issue ID** | [40066346](https://issues.chromium.org/issues/40066346) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | fe...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2023-06-24 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

I refer to this report:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1219354>

previously using tel://, where chromium has patched it. In this case I bypassed it by using iframe+documen.write in it.

**VERSION**  

Chrome Version: [Version 114.0.5735.134 (Official Build) (64-bit)  

] + [stable]  

Operating System: [Windows 11]

**REPRODUCTION CASE**  

On the Chrome Desktop Application, using tel:// should show the origin, but in the tel:// open link function in new tabs or private browsers it doesn't show the origin. This should not be possible because according to this report the patch has already been released:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1219354>

An empty origin in the dialog can be achieved with iframe+document.write, it can trick the sandbox into detecting the origin.

Step Reproduction:

1. Open the poc.html
2. Right click on the link and open it in incognito mode to new tab, or new window.

What is the expected behavior?  

the file destination does appear when clicking on the loading page but not in incognito mode, new tab, and new window.

Affected product versions:  

Chrome Version 114.0.5735.134 (Official Build) (64-bit)  

Chromium 116.0.5810.0 (Developer Build) (64-bit)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 910 B)
- [video1157081385.mp4](attachments/video1157081385.mp4) (video/mp4, 8.9 MB)
- [video1247889169.mp4](attachments/video1247889169.mp4) (video/mp4, 2.0 MB)
- [poc_all.html](attachments/poc_all.html) (text/plain, 1.1 KB)
- [poc2.html](attachments/poc2.html) (text/plain, 262 B)

## Timeline

### [Deleted User] (2023-06-24)

[Empty comment from Monorail migration]

### ah...@google.com (2023-06-26)

Thanks for the report!
I was able to reproduce the behaviour on windows.

Looks very similar to https://crbug.com/chromium/1219354. Setting severity as low.


[Monorail components: UI>Browser]

### fe...@gmail.com (2023-06-26)

Yes, that's right, I referred to the previous report and bypassed the previous patch

### [Deleted User] (2023-06-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-26)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ah...@google.com (2023-06-27)

ellyjones@chromium.org could you please take a look if this is on your end?

### fe...@gmail.com (2023-07-07)

any update on this?, i want to request if this report valid, i want to use Reporter credit with name Kang Ali

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### el...@chromium.org (2023-07-18)

I don't have an update at the moment, sorry - it is on my todo list but not at the top.

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-07-27)

Re-titling this to make it a bit clearer.

It seems like just an iframe is required here. Something like this repros locally for me:
```
<!DOCTYPE html>
<html>
<body>
  <h1>Opening and Closing Popup Windows</h1>
  <iframe srcdoc='<p>Click <a href="tel://newwindow">here</a> for open.</p>'></iframe>
</body>
</html>
```

I haven't looked at the external protocol dialog code but I'm 99% sure it's because of this:
```
const GURL& GetDocumentURL(const content::ContextMenuParams& params) {
  return params.frame_url.is_empty() ? params.page_url : params.frame_url;
}
```

For subframes like this example, the frame URL will be about:blank (or about:srcdoc). It looks like we populate these URLs on the browser side here [1]:

```
  // Validate the URLs in |params|.  If the renderer can't request the URLs
  // directly, don't show them in the context menu.
  ContextMenuParams validated_params(params);
  // Freshly constructed ContextMenuParams have empty `page_url` and `frame_url`
  // - populate them based on trustworthy, browser-side data.
  validated_params.page_url = GetOutermostMainFrame()->GetLastCommittedURL();
  if (GetParentOrOuterDocument()) {
    // Only populate |frame_url| for subframes and fencedframes.
    validated_params.frame_url = GetLastCommittedURL();
  }
```

So it would be trivial to plumb through the last committed origin as well.

Ideally, I think we would pass an url::Origin through the external protocol handling code as well, rather than a GURL. The one thing we need to be careful of is that if the origin is opaque, we want to blame the *precursor* origin. I'm not sure if we have a good helper for that...

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/renderer_host/render_frame_host_impl.cc;l=7570;drc=714e1e34e823b7b4bc172fa4bdefee5aaf5e5fff

### fe...@gmail.com (2023-07-27)


Hello team, after i check, this applies not only to tell:// but to all: like
  zoommtg://
newWinContent
whatsapp
ms-calculator::
and everything
, you can check the video below.


### fe...@gmail.com (2023-07-27)

POC File

### fe...@gmail.com (2023-08-08)

any update on this?

### el...@chromium.org (2023-08-08)

Hi! No update from me, I'm afraid.

### lu...@chromium.org (2023-08-09)

Initiator origin is not shown / plumbed through when a user copy&pastes a URL from a web frame into an Omnibox.  And currently Chrome treats context-menu-initiated navigations as-if the user typed the URL into an Omnibox.  (Same treatment is given to ctrl-clicking or shift-clicking links instead of choosing open in new tab/window via context menu. 
 Behavior in other scenarios has been also discussed earlier in https://docs.google.com/document/d/1YdakWfCR29pVNHURgceKrM_zjGN61xdnCXdZIGpQzxQ/edit?usp=sharing)

This concept hasn't been well-represented in web specs so far.  https://w3c.github.io/webappsec-fetch-metadata/#directly-user-initiated is one attempt to formalize this.

Maybe we should reconsider the current behavior and start treating some additional navigations as renderer-initiated?  I wonder what mkwst@'s, creis@'s, and aaj@'s take on this is...

[Monorail components: -UI>Browser UI>Browser>Navigation]

### [Deleted User] (2023-08-09)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-08-09)

[Empty comment from Monorail migration]

### aa...@google.com (2023-08-11)

I'm not very familiar with the security impact of not showing the origin in the external protocol dialog, but this seems relatively low risk, given that it requires both an explicit interaction with the context menu and clicking through the dialog in the newly opened tab. It seems unlikely that websites would be able to force this to happen without substantial social engineering, and even then the impact is not entirely clear (depends on the protocol and the behavior of the handling application).

From a web security perspective I think the current behavior of features like Fetch Metadata headers is what we want, i.e. we should treat interactions that can't be spoofed by a website without social engineering as non-webby / not renderer initiated. But maybe we want to still show the initiator origin in cases like this bug.

### fe...@gmail.com (2023-08-11)

you can refer to this report https://bugs.chromium.org/p/chromium/issues/detail?id=1219354

For the details information

### [Deleted User] (2023-08-15)

[Empty comment from Monorail migration]

### fe...@gmail.com (2023-08-18)

any update on this?

### fe...@gmail.com (2023-08-25)

Hi team,
since June there has been no improvement in this report, is there an update?


### gi...@appspot.gserviceaccount.com (2023-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4f292f92e527173452a005bdc35df59faa78c4f3

commit 4f292f92e527173452a005bdc35df59faa78c4f3
Author: Elly Fong-Jones <ellyjones@google.com>
Date: Tue Aug 29 18:13:47 2023

content: unconditionally populate frame_url in ContextMenuParams

The prior design only populated frame_url when the initiating frame was
a subframe, which led to code in quite a few places to use frame_url if
present and page_url otherwise, or to test for an empty frame_url as a
signal that the initiator was a subframe.

This change makes frame_url unconditional, and adds a separate parameter
for whether the initiator is a subframe. It also refactors
TestRenderViewContextMenu slightly to make some of the factory arguments
for that class optional, since nearly all call sites pass the same
values.

This is a preparatory refactor for a behavior change in passing invoker
origins through the context menu.

Bug: 1457702
Change-Id: I11cc1118efa76334616690848fb97be355bb2044
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4790929
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Elly FJ <ellyjones@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1189629}

[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/chrome/browser/extensions/api/context_menus/extension_context_menu_browsertest.cc
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/chrome/browser/renderer_context_menu/render_view_context_menu_test_util.h
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/chrome/browser/renderer_context_menu/context_menu_content_type_unittest.cc
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/chrome/browser/extensions/native_bindings_apitest.cc
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/content/public/browser/context_menu_params.h
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/chrome/browser/safe_browsing/safe_browsing_blocking_page_test.cc
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/chrome/browser/extensions/api/web_navigation/web_navigation_apitest.cc
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/components/renderer_context_menu/context_menu_content_type.cc
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/chrome/browser/renderer_context_menu/render_view_context_menu_test_util.cc
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/chrome/browser/renderer_context_menu/render_view_context_menu_browsertest.cc
[modify] https://crrev.com/4f292f92e527173452a005bdc35df59faa78c4f3/chrome/browser/renderer_context_menu/render_view_context_menu_unittest.cc


### gi...@appspot.gserviceaccount.com (2023-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227

commit ce814564a75dfc5ba5fbf83e3a0e8f7df669c227
Author: Ian Wells <iwells@chromium.org>
Date: Tue Aug 29 23:17:35 2023

Revert "content: unconditionally populate frame_url in ContextMenuParams"

This reverts commit 4f292f92e527173452a005bdc35df59faa78c4f3.

Reason for revert: Likely to be causing failures on MSan bots https://ci.chromium.org/ui/p/chromium/builders/ci/Linux%20ChromiumOS%20MSan%20Tests and https://ci.chromium.org/ui/p/chromium/builders/ci/Linux%20MSan%20Tests

Original change's description:
> content: unconditionally populate frame_url in ContextMenuParams
>
> The prior design only populated frame_url when the initiating frame was
> a subframe, which led to code in quite a few places to use frame_url if
> present and page_url otherwise, or to test for an empty frame_url as a
> signal that the initiator was a subframe.
>
> This change makes frame_url unconditional, and adds a separate parameter
> for whether the initiator is a subframe. It also refactors
> TestRenderViewContextMenu slightly to make some of the factory arguments
> for that class optional, since nearly all call sites pass the same
> values.
>
> This is a preparatory refactor for a behavior change in passing invoker
> origins through the context menu.
>
> Bug: 1457702
> Change-Id: I11cc1118efa76334616690848fb97be355bb2044
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4790929
> Reviewed-by: Avi Drissman <avi@chromium.org>
> Reviewed-by: Nasko Oskov <nasko@chromium.org>
> Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
> Reviewed-by: Scott Violet <sky@chromium.org>
> Commit-Queue: Elly FJ <ellyjones@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1189629}

Bug: 1457702
Change-Id: If9d1c662be6e2a8ea971d749663b54f12e23756a
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4824706
Commit-Queue: Ian Wells <iwells@chromium.org>
Owners-Override: Ian Wells <iwells@chromium.org>
Auto-Submit: Ian Wells <iwells@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1189815}

[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/chrome/browser/extensions/api/context_menus/extension_context_menu_browsertest.cc
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/chrome/browser/renderer_context_menu/render_view_context_menu_test_util.h
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/chrome/browser/renderer_context_menu/context_menu_content_type_unittest.cc
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/chrome/browser/extensions/native_bindings_apitest.cc
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/content/public/browser/context_menu_params.h
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/chrome/browser/safe_browsing/safe_browsing_blocking_page_test.cc
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/chrome/browser/extensions/api/web_navigation/web_navigation_apitest.cc
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/components/renderer_context_menu/context_menu_content_type.cc
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/chrome/browser/renderer_context_menu/render_view_context_menu_test_util.cc
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/chrome/browser/renderer_context_menu/render_view_context_menu_browsertest.cc
[modify] https://crrev.com/ce814564a75dfc5ba5fbf83e3a0e8f7df669c227/chrome/browser/renderer_context_menu/render_view_context_menu_unittest.cc


### gi...@appspot.gserviceaccount.com (2023-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/66321127ce9d3b926eb2949831d973fb8ef6e4c5

commit 66321127ce9d3b926eb2949831d973fb8ef6e4c5
Author: Elly <ellyjones@chromium.org>
Date: Wed Aug 30 23:48:27 2023

[reland] content: unconditionally populate frame_url in ContextMenuParams

The prior design only populated frame_url when the initiating frame was
a subframe, which led to code in quite a few places to use frame_url if
present and page_url otherwise, or to test for an empty frame_url as a
signal that the initiator was a subframe.

This change makes frame_url unconditional, and adds a separate parameter
for whether the initiator is a subframe. It also refactors
TestRenderViewContextMenu slightly to make some of the factory arguments
for that class optional, since nearly all call sites pass the same
values.

This is a preparatory refactor for a behavior change in passing invoker
origins through the context menu.

This change is a re-land of
https://chromium-review.googlesource.com/c/chromium/src/+/4790929,
which introduced an MSan test failure because of the uninitialized
is_subframe member in ContextMenuParams.

Bug: 1457702
Change-Id: I7980017b0333fdfe4b421b8e2feda1320d41db4f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4790929
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Elly FJ <ellyjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1189629}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4827951
Cr-Commit-Position: refs/heads/main@{#1190414}

[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/chrome/browser/extensions/api/context_menus/extension_context_menu_browsertest.cc
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/chrome/browser/renderer_context_menu/render_view_context_menu_test_util.h
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/chrome/browser/renderer_context_menu/context_menu_content_type_unittest.cc
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/chrome/browser/extensions/native_bindings_apitest.cc
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/content/public/browser/context_menu_params.h
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/chrome/browser/safe_browsing/safe_browsing_blocking_page_test.cc
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/chrome/browser/extensions/api/web_navigation/web_navigation_apitest.cc
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/components/renderer_context_menu/context_menu_content_type.cc
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/chrome/browser/renderer_context_menu/render_view_context_menu_test_util.cc
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/chrome/browser/renderer_context_menu/render_view_context_menu_browsertest.cc
[modify] https://crrev.com/66321127ce9d3b926eb2949831d973fb8ef6e4c5/chrome/browser/renderer_context_menu/render_view_context_menu_unittest.cc


### gi...@appspot.gserviceaccount.com (2023-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4e893e4e646e96bd9246d251e3fcb4ac614ece51

commit 4e893e4e646e96bd9246d251e3fcb4ac614ece51
Author: Jiewei Qian <qjw@chromium.org>
Date: Thu Aug 31 04:30:21 2023

Revert "[reland] content: unconditionally populate frame_url in ContextMenuParams"

This reverts commit 66321127ce9d3b926eb2949831d973fb8ef6e4c5.

Reason for revert: Break linux-chromeos-chrome

https://ci.chromium.org/ui/b/8771283259639514113

Original change's description:
> [reland] content: unconditionally populate frame_url in ContextMenuParams
>
> The prior design only populated frame_url when the initiating frame was
> a subframe, which led to code in quite a few places to use frame_url if
> present and page_url otherwise, or to test for an empty frame_url as a
> signal that the initiator was a subframe.
>
> This change makes frame_url unconditional, and adds a separate parameter
> for whether the initiator is a subframe. It also refactors
> TestRenderViewContextMenu slightly to make some of the factory arguments
> for that class optional, since nearly all call sites pass the same
> values.
>
> This is a preparatory refactor for a behavior change in passing invoker
> origins through the context menu.
>
> This change is a re-land of
> https://chromium-review.googlesource.com/c/chromium/src/+/4790929,
> which introduced an MSan test failure because of the uninitialized
> is_subframe member in ContextMenuParams.
>
> Bug: 1457702
> Change-Id: I7980017b0333fdfe4b421b8e2feda1320d41db4f
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4790929
> Reviewed-by: Avi Drissman <avi@chromium.org>
> Reviewed-by: Nasko Oskov <nasko@chromium.org>
> Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
> Reviewed-by: Scott Violet <sky@chromium.org>
> Commit-Queue: Elly FJ <ellyjones@chromium.org>
> Cr-Original-Commit-Position: refs/heads/main@{#1189629}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4827951
> Cr-Commit-Position: refs/heads/main@{#1190414}

Bug: 1457702
Change-Id: I300257a3e106a19e9c07abe77449e0b35c22ef8a
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4829344
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Jiewei Qian <qjw@chromium.org>
Auto-Submit: Jiewei Qian <qjw@chromium.org>
Owners-Override: Jiewei Qian <qjw@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1190533}

[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/chrome/browser/extensions/api/context_menus/extension_context_menu_browsertest.cc
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/chrome/browser/renderer_context_menu/render_view_context_menu_test_util.h
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/chrome/browser/renderer_context_menu/context_menu_content_type_unittest.cc
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/chrome/browser/extensions/native_bindings_apitest.cc
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/content/public/browser/context_menu_params.h
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/chrome/browser/safe_browsing/safe_browsing_blocking_page_test.cc
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/chrome/browser/extensions/api/web_navigation/web_navigation_apitest.cc
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/components/renderer_context_menu/context_menu_content_type.cc
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/chrome/browser/renderer_context_menu/render_view_context_menu_test_util.cc
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/chrome/browser/renderer_context_menu/render_view_context_menu_browsertest.cc
[modify] https://crrev.com/4e893e4e646e96bd9246d251e3fcb4ac614ece51/chrome/browser/renderer_context_menu/render_view_context_menu_unittest.cc


### gi...@appspot.gserviceaccount.com (2023-09-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9881638409cf492850b57ade0a8089545a847c3c

commit 9881638409cf492850b57ade0a8089545a847c3c
Author: Elly <ellyjones@chromium.org>
Date: Tue Sep 05 17:02:45 2023

[reland 2] content: unconditionally populate frame_url in ContextMenuParams

The prior design only populated frame_url when the initiating frame was
a subframe, which led to code in quite a few places to use frame_url if
present and page_url otherwise, or to test for an empty frame_url as a
signal that the initiator was a subframe.

This change makes frame_url unconditional, and adds a separate parameter
for whether the initiator is a subframe. It also refactors
TestRenderViewContextMenu slightly to make some of the factory arguments
for that class optional, since nearly all call sites pass the same
values.

This is a preparatory refactor for a behavior change in passing invoker
origins through the context menu.

This change is a re-land of
https://chromium-review.googlesource.com/c/chromium/src/+/4790929,
which introduced an MSan test failure because of the uninitialized
is_subframe member in ContextMenuParams.

This change is a subsequent re-land of
https://chromium-review.googlesource.com/c/chromium/src/+/4827951, which
introduced a branded lens build test failure on ChromeOS that the CQ
bots didn't catch.

Bug: 1457702
Change-Id: I87807acfa63179f3cbdde410ee9b02acd27e8c9a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4790929
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Elly FJ <ellyjones@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1189629}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4827951
Cr-Original-Commit-Position: refs/heads/main@{#1190414}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4833488
Cr-Commit-Position: refs/heads/main@{#1192528}

[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/chrome/browser/extensions/api/context_menus/extension_context_menu_browsertest.cc
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/chrome/browser/renderer_context_menu/render_view_context_menu_test_util.h
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/chrome/browser/renderer_context_menu/context_menu_content_type_unittest.cc
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/chrome/browser/extensions/native_bindings_apitest.cc
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/content/public/browser/context_menu_params.h
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/chrome/browser/safe_browsing/safe_browsing_blocking_page_test.cc
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/chrome/browser/extensions/api/web_navigation/web_navigation_apitest.cc
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/components/renderer_context_menu/context_menu_content_type.cc
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/chrome/browser/renderer_context_menu/render_view_context_menu_browsertest.cc
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/chrome/browser/renderer_context_menu/render_view_context_menu_test_util.cc
[modify] https://crrev.com/9881638409cf492850b57ade0a8089545a847c3c/chrome/browser/renderer_context_menu/render_view_context_menu_unittest.cc


### fe...@gmail.com (2023-09-15)

any update team?

### el...@chromium.org (2023-10-12)

Here's my current understanding of what's going on:

In the proof of concept, we have a main frame on some origin (example.com). That main frame opens a new popup window with an iframe in it. The popup window's iframe contains a URL which, when clicked, runs a script that adds a second nested iframe. The nested iframe has a different opaque origin (right?) and inside that iframe is a tel:// link. Right-clicking that tel:// link and opening it in a new tab shows an external protocol dialog that has no origin attribution, but we think it should instead be attributed to example.com.

I believe that a simpler PoC (which I have tried) is: have a main frame on example.com, which contains a subframe on an opaque origin, which itself contains a tel:// link. Right-click that tel:// link and open it in a new tab; the resulting external protocol dialog should be attributed to example.com but is not.

To fix that, I have a CL: https://chromium-review.googlesource.com/c/chromium/src/+/4763411 but it's not very clear what the security concept we're trying to get at is. What the user cares about is "where did this URL really come from", which in this case is the origin of the main frame, but if the iframe had a non-opaque origin, it could be something else instead. For example, if good.com iframes bad.com and the user right-clicks a link in the bad.com iframe, the origin should instead show as bad.com. I guess it depends on who controls the content of the iframe?

### cr...@chromium.org (2023-10-12)

https://crbug.com/chromium/1457702#c30: Thanks! "Where did this URL really come from" tends to be tracked as the "precursor origin" for opaque origins, which is accessible via url::Origin::GetTupleOrPrecursorTupleIfOpaque.  Is that sufficient for showing the right value in the dialog?

### gi...@appspot.gserviceaccount.com (2023-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/593d7d909bc07024a3f79772aa678cab22bc9e59

commit 593d7d909bc07024a3f79772aa678cab22bc9e59
Author: Elly <ellyjones@chromium.org>
Date: Thu Oct 19 23:27:38 2023

content: pass initiator origin through for context menu

This change:
1. Modifies RenderFrameHostImpl to pass the initiating frame's origin
   through when invoking the renderer context menu
2. Modifies some of the renderer context menu classes to plumb that
   origin through when loading a URL
3. Adds an end-to-end test to the ContextMenuBrowserTest suite to
   validate this new behavior

Fixed: 1457702
Change-Id: If134600bd2aaf836bc297a110a2368e9096a8402
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4763411
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Elly FJ <ellyjones@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1212452}

[modify] https://crrev.com/593d7d909bc07024a3f79772aa678cab22bc9e59/components/renderer_context_menu/render_view_context_menu_base.h
[modify] https://crrev.com/593d7d909bc07024a3f79772aa678cab22bc9e59/components/renderer_context_menu/render_view_context_menu_base.cc
[modify] https://crrev.com/593d7d909bc07024a3f79772aa678cab22bc9e59/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/593d7d909bc07024a3f79772aa678cab22bc9e59/chrome/browser/renderer_context_menu/render_view_context_menu.h
[modify] https://crrev.com/593d7d909bc07024a3f79772aa678cab22bc9e59/chrome/browser/extensions/api/web_navigation/web_navigation_apitest.cc
[modify] https://crrev.com/593d7d909bc07024a3f79772aa678cab22bc9e59/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/593d7d909bc07024a3f79772aa678cab22bc9e59/chrome/browser/renderer_context_menu/render_view_context_menu_browsertest.cc
[modify] https://crrev.com/593d7d909bc07024a3f79772aa678cab22bc9e59/content/public/browser/context_menu_params.h
[modify] https://crrev.com/593d7d909bc07024a3f79772aa678cab22bc9e59/chrome/browser/renderer_context_menu/render_view_context_menu_unittest.cc


### cr...@chromium.org (2023-10-20)

Elly: Just to confirm, this isn't fixed yet, is it?  Your comment at https://chromium-review.googlesource.com/c/chromium/src/+/4763411/comment/7468995e_a5cc329e/ indicated more changes (and a test) were needed for the tel: dialog.

### fe...@gmail.com (2023-10-20)

Hi team, Have you seen https://crbug.com/chromium/1457702#c12, not only tel:// but calculator, etc. can also be used

### el...@chromium.org (2023-10-23)

#34: It is not fixed yet - one more CL is needed I think.
#35: Yep, I did see that. They all go through the same code path anyawy so when I land the fix it should fix all of them.

### el...@chromium.org (2023-10-26)

Good news and bad news!

Good news: The plumbing I thought I'd need to write in a followup CL is actually already there, and neither the reporter's original PoC nor my simpler one (attached) repro the bug any more. Woo!

Bad news: I still do need to write that new test :)

### fe...@gmail.com (2023-11-13)

Hi team, any update on this? After over 2 weeks

### fe...@gmail.com (2023-11-28)

HiTeam, @ellyj...@chromium.org and  @creis@chromium.org 

I have verified Version 120.0.6090.0 (Developer Build) (64-bit) and the bug has apparently been patched and can no longer be used.

Thanks

### el...@chromium.org (2023-11-28)

That's good to hear! This bug is therefore Fixed, and I've filed a followup (https://bugs.chromium.org/p/chromium/issues/detail?id=1505769) for the missing test coverage.

### [Deleted User] (2023-11-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-28)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-30)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us.

### am...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-04)

[Comment Deleted]

### pg...@google.com (2023-12-06)

[Comment Deleted]

### pg...@google.com (2023-12-06)

[Comment Deleted]

### am...@chromium.org (2024-01-08)

This was discovered to be a duplicate of a previous report only after this issue was fixed and the CL landed. Since all merge and release mechanics have been completed, merging this issue into the older issue. 

### am...@chromium.org (2024-01-08)

[Comment Deleted]

### am...@chromium.org (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1457702?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1350028]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-08-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### er...@microsoft.com (2024-08-28)

The design here is interesting. 

A common use case for opaque origins is for a page to be able to render untrusted content provided by a 3rd party. Using an opaque origin ensures that the content does not have access to the origin that served it, lest it abuse the security context's ambient permissions.

By showing the originator's origin in the security prompt, we are now asking the user whether they trust the site to launch the app, but the site's use of the opaque origin may itself represent the site saying "Hey, I don't trust this content, pretend it didn't come from me."

We see a similar thing with a SANDBOX'd frame -- it's not allowed to open an application protocol by default, but if the user right-clicks and chooses Open-in-new-tab, not only do we allow launching the protocol, but the security prompt shows the origin that was trying to explicitly disavow ownership of that content.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066346)*
