# Cross-origin stylesheet content is readable using SW

| Field | Value |
|-------|-------|
| **Issue ID** | [40091542](https://issues.chromium.org/issues/40091542) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CSS, Blink>ServiceWorker |
| **Platforms** | Windows |
| **Reporter** | s....@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2018-06-01 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/steal_css.html
2. Reload

What is the expected behavior?
Throws SecurityError on alert (due to access restriction in cross-origin cssText).

What went wrong?
test.shhnjk.com has access to stylesheet content of https://vuln.shhnjk.com/cross-origin.css. Response opaqueness is not considered in stylesheet.

Did this work before? N/A 

Chrome version: 67.0.3396.62  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### go...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-06-01)

I believe this is the same issue as https://github.com/w3c/ServiceWorker/issues/719 (https://crbug.com/chromium/532374)

horo: Can you please confirm? Thanks.

[Monorail components: Blink>ServiceWorker]

### s....@gmail.com (2018-06-01)

#2: It's a different issue. In CSS, there are/were spec bugs where Resource Timing/Service Worker could identify which resource has been fethced by cross-origin stylesheet. But those bugs never revealed whole content of cross-origin stylesheet.

### cr...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-06-04)

This looks real as Firefox blocks the access. The problem is the page can read the contents of the cross-origin CSS.

I'm taking a guess on Security_Severity, security people please adjust if needed.

### sh...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-06-06)

[Empty comment from Monorail migration]

### ja...@chromium.org (2018-06-06)

It isn't "high" severity, since CORB blocks a lot of the sensitive resource types, and CSS doesn't typically contain sensitive data.

### ja...@chromium.org (2018-06-06)

(so I agree with "medium" sensitivity)

### fa...@chromium.org (2018-06-06)

+kouhei: for context for the code review I'm about to send

### fa...@chromium.org (2018-06-06)

+kinuko: ditto

### fa...@chromium.org (2018-06-07)

cc Ben Kelly: FYI this adds a WPT test that Firefox seems to fail. See the comment at https://chromium-review.googlesource.com/c/chromium/src/+/1088719#message-0a24c5d25ce9ee761f8875c5039bb5f02ffeb633

(I can't seem to add you to the code review directly)

### fa...@chromium.org (2018-06-07)

+reviewers from https://chromium-review.googlesource.com/c/chromium/src/+/1088335

### fa...@chromium.org (2018-06-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d981bbb72fb25663f9be476cdedfb16b1edb9054

commit d981bbb72fb25663f9be476cdedfb16b1edb9054
Author: Matt Falkenhagen <falken@chromium.org>
Date: Thu Jun 07 08:19:04 2018

service worker: Add test for CSS cross-origin access.

Tests for https://chromium-review.googlesource.com/c/chromium/src/+/1088335

Bug: 848786
Change-Id: I39d71d9aa2d1c0522c7a386405128297f62a0b24
Reviewed-on: https://chromium-review.googlesource.com/1088719
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#565208}
[delete] https://crrev.com/9af34b4853164a8025c9a34cc0aa120203af75d1/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-request-css-cross-origin-mime-check.https.html
[add] https://crrev.com/d981bbb72fb25663f9be476cdedfb16b1edb9054/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-request-css-cross-origin.https-expected.txt
[add] https://crrev.com/d981bbb72fb25663f9be476cdedfb16b1edb9054/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-request-css-cross-origin.https.html
[modify] https://crrev.com/d981bbb72fb25663f9be476cdedfb16b1edb9054/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-request-css-cross-origin-mime-check-iframe.html
[delete] https://crrev.com/9af34b4853164a8025c9a34cc0aa120203af75d1/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-request-css-cross-origin-mime-check-worker.js
[add] https://crrev.com/d981bbb72fb25663f9be476cdedfb16b1edb9054/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-request-css-cross-origin-read-contents.html
[add] https://crrev.com/d981bbb72fb25663f9be476cdedfb16b1edb9054/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-request-css-cross-origin-worker.js


### s....@gmail.com (2018-06-07)

FYI to falken@:
Following is the relavant spec. You might want to check if your patch also blocks insertRule and deleteRule to cross-origin stylesheet (I believe it does but just in case).
https://www.w3.org/TR/cssom-1/#the-cssstylesheet-interface

### fa...@chromium.org (2018-06-07)

Thanks! So many things to test...

### s....@gmail.com (2018-06-07)

[Comment Deleted]

### [Deleted User] (2018-06-07)

> cc Ben Kelly: FYI this adds a WPT test that Firefox seems to fail. See the comment at https://chromium-review.googlesource.com/c/chromium/src/+/1088719#message-0a24c5d25ce9ee761f8875c5039bb5f02ffeb633

Yea, this seems like a firefox bug.  The stylesheet loader is treating it as a no-cors opaque result even though the service worker is responding with a CORS response.  This is due to how the stylesheet loader handled taining in the past vs what was added for fetch/sw.

I filed a bug:

https://bugzilla.mozilla.org/show_bug.cgi?id=1467454

By the way, you might also want to consider test cases that exercise @import() of further stylesheets.

Thanks for letting me know about the firefox bug.

### bu...@chromium.org (2018-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0c45ffd2a1b2b6b91aaaac989ad10a76765083c6

commit 0c45ffd2a1b2b6b91aaaac989ad10a76765083c6
Author: Matt Falkenhagen <falken@chromium.org>
Date: Fri Jun 08 04:53:00 2018

Disallow access to opaque CSS responses.

Bug: 848786
Change-Id: Ie53fbf644afdd76d7c65649a05c939c63d89b4ec
Reviewed-on: https://chromium-review.googlesource.com/1088335
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#565537}
[delete] https://crrev.com/bf42268f6639e4322eb56507739a33ffcbb7b28b/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-request-css-cross-origin.https-expected.txt
[modify] https://crrev.com/0c45ffd2a1b2b6b91aaaac989ad10a76765083c6/third_party/blink/renderer/core/css/css_style_sheet.cc
[modify] https://crrev.com/0c45ffd2a1b2b6b91aaaac989ad10a76765083c6/third_party/blink/renderer/core/css/parser/css_parser_context.cc
[modify] https://crrev.com/0c45ffd2a1b2b6b91aaaac989ad10a76765083c6/third_party/blink/renderer/core/css/parser/css_parser_context.h
[modify] https://crrev.com/0c45ffd2a1b2b6b91aaaac989ad10a76765083c6/third_party/blink/renderer/core/css/selector_query.cc
[modify] https://crrev.com/0c45ffd2a1b2b6b91aaaac989ad10a76765083c6/third_party/blink/renderer/core/css/selector_query_test.cc
[modify] https://crrev.com/0c45ffd2a1b2b6b91aaaac989ad10a76765083c6/third_party/blink/renderer/core/css/style_rule_import.cc
[modify] https://crrev.com/0c45ffd2a1b2b6b91aaaac989ad10a76765083c6/third_party/blink/renderer/core/css/style_sheet_contents.h
[modify] https://crrev.com/0c45ffd2a1b2b6b91aaaac989ad10a76765083c6/third_party/blink/renderer/core/dom/processing_instruction.cc
[modify] https://crrev.com/0c45ffd2a1b2b6b91aaaac989ad10a76765083c6/third_party/blink/renderer/core/html/link_style.cc


### fa...@chromium.org (2018-06-08)

This should be in a canary soon.

Remaining work:
- make sure @import(), insertRule, deleteRule are blocked
- add automated tests for @import(), insertRule, deleteRule?

### fa...@chromium.org (2018-06-11)

I don't really see in the spec how cross-origin @import() is handled in terms of opaqueness. It looks like it doesn't clear the origin-clean flag. This generally seems like a big topic at least partially related to https://github.com/w3c/ServiceWorker/issues/719.

Today printing cssRules[].cssText only reveals something like: '@import url("https://falken-remote-origin.glitch.me/styles.css");' (regardless of service workers). So I don't think there's a risk of more info being leaked by using a service worker, so no test is needed.

Regarding addRule and deleteRule, using s.h.h.n.j.k's site it looks like Chrome is blocking them when the fix is in:
> document.styleSheets[0].addRule('.crossOrigin', 'color: green;');
VM31:1 Uncaught DOMException: Failed to execute 'addRule' on 'CSSStyleSheet': Cannot access StyleSheet to insertRule
    at <anonymous>:1:25

> document.styleSheets[0].deleteRule(0);
VM66:1 Uncaught DOMException: Failed to execute 'deleteRule' on 'CSSStyleSheet': Cannot access StyleSheet to deleteRule
    at <anonymous>:1:25

Also:
> document.styleSheets[0].insertRule('.crossOrigin {color: green }');

I think it's reasonable to expect implementations to use the same access check as printing cssRules[].cssText so we don't necessarily need to add automated tests for them.

Therefore I'm going to declare this bug fixed but POCs of more security problems are always welcome.

The fix is in M69 and is probably safe for merging to M68 after a canary. Setting NextAction for that. I don't think it needs to merge to stable, so removing Target-67.

### fa...@chromium.org (2018-06-11)

[Empty comment from Monorail migration]

[Monorail components: Blink>CSS]

### sh...@chromium.org (2018-06-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-13)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### s....@gmail.com (2018-06-14)

Edge is also affected by this bug and aiming to fix it in RS5. Could anyone add "Restrict-View-SecurityEmbargo" please? Thanks!

### aw...@chromium.org (2018-06-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-15)

$500 for this one :-)

### aw...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-15)

Per #29, adding SecurityEmbargo for coordination with Edge. RS5 looks like it's going to be released some time in October, so setting a next action to remind us to look at de-restricting.

### ab...@google.com (2018-06-16)

Approving merge to M68. Branch:3440

### bu...@chromium.org (2018-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bd5fda6badfcd473b9d96cb6eba74880125a99b3

commit bd5fda6badfcd473b9d96cb6eba74880125a99b3
Author: Matt Falkenhagen <falken@chromium.org>
Date: Mon Jun 18 00:45:16 2018

M68: Disallow access to opaque CSS responses.

Bug: 848786
Change-Id: Ie53fbf644afdd76d7c65649a05c939c63d89b4ec
Reviewed-on: https://chromium-review.googlesource.com/1088335
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#565537}(cherry picked from commit 0c45ffd2a1b2b6b91aaaac989ad10a76765083c6)
Reviewed-on: https://chromium-review.googlesource.com/1103857
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/branch-heads/3440@{#390}
Cr-Branched-From: 010ddcfda246975d194964ccf20038ebbdec6084-refs/heads/master@{#561733}
[modify] https://crrev.com/bd5fda6badfcd473b9d96cb6eba74880125a99b3/third_party/blink/renderer/core/css/css_style_sheet.cc
[modify] https://crrev.com/bd5fda6badfcd473b9d96cb6eba74880125a99b3/third_party/blink/renderer/core/css/parser/css_parser_context.cc
[modify] https://crrev.com/bd5fda6badfcd473b9d96cb6eba74880125a99b3/third_party/blink/renderer/core/css/parser/css_parser_context.h
[modify] https://crrev.com/bd5fda6badfcd473b9d96cb6eba74880125a99b3/third_party/blink/renderer/core/css/selector_query.cc
[modify] https://crrev.com/bd5fda6badfcd473b9d96cb6eba74880125a99b3/third_party/blink/renderer/core/css/selector_query_test.cc
[modify] https://crrev.com/bd5fda6badfcd473b9d96cb6eba74880125a99b3/third_party/blink/renderer/core/css/style_rule_import.cc
[modify] https://crrev.com/bd5fda6badfcd473b9d96cb6eba74880125a99b3/third_party/blink/renderer/core/css/style_sheet_contents.h
[modify] https://crrev.com/bd5fda6badfcd473b9d96cb6eba74880125a99b3/third_party/blink/renderer/core/dom/processing_instruction.cc
[modify] https://crrev.com/bd5fda6badfcd473b9d96cb6eba74880125a99b3/third_party/blink/renderer/core/html/link_style.cc


### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### s....@gmail.com (2018-10-18)

RS5 release is pending due to some file deleting issue. I would recommend not disclosing this issue until Edge actually ship the fix.

### aw...@google.com (2018-10-19)

Thanks, s.h.h.n.j.k@ - mind updating the bug when RS5 is released?

### s....@gmail.com (2018-10-19)

Will do!

### s....@gmail.com (2018-12-14)

RS5 shipped :)

### aw...@google.com (2018-12-14)

Thanks!

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/848786?no_tracker_redirect=1

[Multiple monorail components: Blink>CSS, Blink>ServiceWorker]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091542)*
