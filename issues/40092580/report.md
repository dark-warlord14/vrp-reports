# Data URLs can be loaded on the top frame using iOS Mobile Chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [40092580](https://issues.chromium.org/issues/40092580) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2018-09-29 |
| **Bounty** | $500.00 |

## Description

Steps to reproduce the problem:
1. View "<script>document.location.href = "data:text/html,Hello!";</script>" on Desktop Chrome
2. Notice "Not allowed to navigate top frame to data URL" error in developer console
3. View same page in mobile Chrome for iOS
4. Watch top frame load the data URL without error

What is the expected behavior?
iOS Mobile Chrome should refuse to navigate top frame to data URLs

What went wrong?
The top frame loaded the data URL

Did this work before? N/A 

Chrome version: iOS Mobile Chrome Version 69.0.3497.105  Channel: n/a
OS Version: iOS 12.0
Flash Version:

## Timeline

### do...@chromium.org (2018-09-30)

https://crbug.com/chromium/594215 was meant to disallow top-frame navigation to data URLs. It's possible we can't do that on iOS since we don't control WKWebView.

+meacer, +euegenebut, can you follow up here? Marking as low severity for now since we allowed data URLs for a long time before getting rid of them.

[Monorail components: UI>Browser>Navigation]

### sh...@chromium.org (2018-10-01)

[Empty comment from Monorail migration]

### eu...@chromium.org (2018-10-01)

Blocking data:// URLs should be doable on iOS. Mustafa, could you please confirm that we should block all data:// URL responses, unless the navigation's transition type is PAGE_TRANSITION_TYPED or the load will result in Download Manager presentation.

Thanks!

### me...@chromium.org (2018-10-01)

The logic to check whether to block on non-iOS platforms uses is_browser_initiated bit on the navigation. Is that available on iOS?

If not, PAGE_TRANSITION_TYPED + Download Manager sounds like a good approximation to me but you might want to check with navigation folks as well.

### eu...@chromium.org (2018-10-01)

Thanks Mustafa! Do you know which content API we use for checking is_browser_initiated bit? 

### me...@chromium.org (2018-10-01)

Sorry, it's IsRendererInitiated, not browser :) It's in NavigationHandle: https://cs.chromium.org/chromium/src/content/browser/frame_host/blocked_scheme_navigation_throttle.cc?rcl=49993008676b4624600f439cbb91eb4fbc8b15b3&l=57

(Note that we also have a blink side check to determine if the data URL's mime type is going to be rendered or downloaded: https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/loader/frame_loader.cc?rcl=49993008676b4624600f439cbb91eb4fbc8b15b3&l=702. This kicks in for things like <a href="data:...">)

### eu...@chromium.org (2018-10-01)

Thanks! iOS has NavigationContext::IsRendererInitiated, which is the same flag as NavigationHandle::IsRendererInitiated().

Could you please clarify what should be done with renderer-initiated downloads. Block or Allow?




### me...@chromium.org (2018-10-01)

Downloads should always be fine whether renderer or browser initiated (the blocking is only concerned about rendering the data URL inside a tab).

### eu...@chromium.org (2018-10-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/23263d5acb19cb17be4548a7bfd80135f098f064

commit 23263d5acb19cb17be4548a7bfd80135f098f064
Author: Eugene But <eugenebut@google.com>
Date: Tue Oct 09 00:25:52 2018

Block rendering data URLs for renderer-initiated main frame navigations.

This increased the complexity for already complex method, so there
will be follow up CL with refactoring.

testWindowOpenWithAboutNewTabScript test was removed as invalid.

Bug: 890558
Cq-Include-Trybots: luci.chromium.try:ios-simulator-cronet;luci.chromium.try:ios-simulator-full-configs
Change-Id: I41d9ef0b1fee7551e358cc3f651776a4cb7f8b7e
Reviewed-on: https://chromium-review.googlesource.com/c/1266607
Reviewed-by: Mohammad Refaat <mrefaat@chromium.org>
Commit-Queue: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/heads/master@{#597751}
[modify] https://crrev.com/23263d5acb19cb17be4548a7bfd80135f098f064/ios/chrome/browser/web/window_open_by_dom_egtest.mm
[modify] https://crrev.com/23263d5acb19cb17be4548a7bfd80135f098f064/ios/testing/data/http_server_files/window_open.html
[modify] https://crrev.com/23263d5acb19cb17be4548a7bfd80135f098f064/ios/web/web_state/ui/crw_web_controller.mm
[modify] https://crrev.com/23263d5acb19cb17be4548a7bfd80135f098f064/ios/web/web_state/ui/crw_web_controller_unittest.mm


### eu...@chromium.org (2018-10-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-22)

Hi pickrrya@ - thanks for the report - the VRP panel decided to award $500. Cheers!

### aw...@google.com (2018-10-22)

A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in our release notes?

### aw...@chromium.org (2018-10-22)

[Empty comment from Monorail migration]

### pi...@gmail.com (2018-10-23)

Awesome, thanks! Please credit "Ryan Pickren (ryanpickren.com)"

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/890558?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/799657]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092580)*
