# Security: PEPC element max-(width|height) restrictions can be bypassed with larger min-(width|height) value

| Field | Value |
|-------|-------|
| **Issue ID** | [341947676](https://issues.chromium.org/issues/341947676) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2024-05-22 |
| **Bounty** | $2,000.00 |

## Description

#### SUMMARY

The Page Embedded Permission Control (PEPC) element has renderer-side checks to ensure the element is displayed safely within a page. These checks can be bypassed by setting a large min-(width|height) value.

Based on this commit [1], PEPC will be in origin trial soon (although I haven't seen a milestone yet).

PEPC is behind a flag since M121 [2].

[1] <https://chromium.googlesource.com/chromium/src/+/7fb7ce92aac3851d7e7245b19b9526730a23a923>

[2] <https://chromestatus.com/feature/5125006551416832>

#### VULNERABILITY DETAILS

Commit 5f43fa2ff837dcab4d73f6ee527460ee6797e3d4 [3] implemented checks for (min|max)-(width|height) CSS values, but they only enforce a minimum value for min-(width|height) and a maximum value for max-(width|height).

The current code [4] does not seem to enforce a maximum value for min-(width|height) or a minimum value for max-(width|height).

In Blink, min-(width|height) values take precedence over max-(width|height) values. Therefore, a page can set a large min-(width|height) value that is larger than the maximum allowed (width|height) or max-(width|height) values to bypass the maximum dimensions restrictions.

[3] `Limit min/max-height/width for PEPC` (April 12, 2024) <https://chromium.googlesource.com/chromium/src/+/5f43fa2ff837dcab4d73f6ee527460ee6797e3d4>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/html_permission_element.cc;l=508-523;drc=c0265133106c7647e90f9aaa4377d28190b1a6a9>

POTENTIAL SOLUTION

In addition to existing enforcement [4], also enforce maximum value for min-(width|height) to avoid it being larger than the clamped max-(width|height) value. It may also be helpful to enforce a minimum value for max-(width|height), although I don't think there's any current or planned conditions where Blink will invert the current prioritization of these rules.

#### VERSION

Chrome Version: 127.0.6493.2 Canary, 125.0.6422.60 Stable.

Requires `--enable-features=PermissionElement` flag on all channels.

Operating System: Windows 10 Version 22H2 (Build 19045.4170)

#### BISECT

Prior to the commit below, these CSS properties weren't restricted, so technically starts reproducing since early permission element implementations. But since the report is for a bypass of these restrictions, it makes sense to show bisect only after restrictions were introduced.

Starts reproducing on commit <https://chromium.googlesource.com/chromium/src/+/5f43fa2ff837dcab4d73f6ee527460ee6797e3d4>

Landed in 125.0.6415.0 in April 12, 2024: <https://chromiumdash.appspot.com/commit/5f43fa2ff837dcab4d73f6ee527460ee6797e3d4>

Verified repro down to 125.0.6415.0.

#### REPRODUCTION CASE

Prerequisites: Run Chrome with `--enable-features=PermissionElement` flag.

##### Scenario 1: PEPC element with only text visible (fairly hidden)

1. Navigate to <https://alesandroortiz.com/security/chromium/pepc-size.html>
2. Click anywhere below the text

Observed: PEPC element dimensions are larger than the intended safe values. User can interact with PEPC element that bypasses these restrictions.

Expected: PEPC element dimensions are clamped to safe values.

##### Scenario 2: PEPC element fully visible

1. Navigate to <https://alesandroortiz.com/security/chromium/pepc-size-visible.html>

Observed: PEPC element dimensions are larger than the intended safe values. User can interact with PEPC element that bypasses these restrictions.

Expected: PEPC element dimensions are clamped to safe values.

##### Control: Shows the intended maximum dimensions when using width/height with a PEPC element

1. Navigate to <https://alesandroortiz.com/security/chromium/pepc-size-control.html>

Observed: PEPC element dimensions are clamped to safe values, even when width/height values are larger than intended safe values.

##### Demo: Shows renderer's behavior with conflicting CSS (min|max)-(width|height) values with a div element

1. Navigate to <https://alesandroortiz.com/security/chromium/css-min-max.html>

Observed: Renderer will set element dimensions to the min-(width|height) values, even if the max-(width|height) value is smaller than the min-(width|height) value.

#### CREDIT INFORMATION

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- pepc-size.html (text/html, 731 B)
- pepc-size-visible.html (text/html, 731 B)
- pepc-size-control.html (text/html, 269 B)
- css-min-max.html (text/html, 384 B)
- [pepc-size.mp4](attachments/pepc-size.mp4) (video/mp4, 1.5 MB)

## Timeline

### ps...@google.com (2024-05-22)

Thank you for the report OP.

Marking as Security_Impact-None as feature is gated behind a flag. Was able to reproduce all steps on linux cloud top.  

Assigning to @andypaicu as they landed the constraining CL mentioned in the bug. 

### ap...@google.com (2024-05-24)

Project: chromium/src
Branch: main

commit 1fa5805fe6a4df6a1eacf969c065ba474a5c6e3a
Author: Andy Paicu <andypaicu@chromium.org>
Date:   Fri May 24 14:52:38 2024

    [PEPC] Clamp min-width/height based on the maximum allowed value as well
    
    The min/max-width/height properties for the permission element are
    bounded in an effort to prevent the width/height from going above/below
    certain hard-set limits. However the min-width/height will overrule
    the max-width/height if it's bigger. This means that the current
    restrictions can be bypassed in one direction by setting the
    min-width/height to very large values, as they are currently only lower
    bounded (restricted from being too small). This CL instead changes the
    logic to clamp the min-width/height so that it also has an upper bound.
    
    Fixed: 341947676
    Change-Id: I6fe68b6d9f07e4041e5c4455fc34dce167b01be5
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5563906
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
    Commit-Queue: Andy Paicu <andypaicu@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1305710}

M       third_party/blink/renderer/core/html/html_permission_element.cc
M       third_party/blink/renderer/core/html/html_permission_element.h
M       third_party/blink/web_tests/external/wpt/html/semantics/permission-element/bounded-sizes.tentative.html
A       third_party/blink/web_tests/external/wpt/html/semantics/permission-element/large-min-size-reftest-ref.html
A       third_party/blink/web_tests/external/wpt/html/semantics/permission-element/large-min-size-reftest.tentative.html

https://chromium-review.googlesource.com/5563906


### pe...@google.com (2024-05-24)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

### al...@alesandroortiz.com (2024-05-24)

Verified as fixed using snapshot build 1305767 [1] on Windows 10 Version 22H2 (Build 19045.4412).

Thanks for the quick fix!

[1] <https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/1305767/>

### an...@chromium.org (2024-05-27)

Thank you for verifying.

### pe...@google.com (2024-05-27)

Merge review required: M126 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

### an...@chromium.org (2024-05-27)

1. This is a fix for a security issue for a feature behind a flag. This issue is an blocker for starting the OT.
2. https://chromium-review.googlesource.com/c/chromium/src/+/5563906
3. Yes
4. Yes, behind a flag. No active experiments in release channels.
5. -
6. Does not require manual verification.

### pe...@google.com (2024-05-27)

Setting milestone because of s2 severity.

### am...@chromium.org (2024-05-28)

I've reviewed <https://chromium-review.googlesource.com/c/chromium/src/+/5563906> on canary and there isn't anything that presents concerns on that front. However, from reviewing this change, any issues from this fix is not likely something to come across in Canary data as much as present potential functional issues.
Upon review, I'm inclined to tentatively approve this fix for merge to M126.

However, there is only one more M126 Beta update (on Thursday) *before* M126 Stable RC cut is next Tuesday, please ensure there is no functionality risk or other potential issue before merging.
If there is no potential functional or other risk concerns, then please merge to branch 6478 by EOD tomorrow (Wednesday 29 May) so this fix can be included in the next M126 Beta update.

### an...@chromium.org (2024-05-29)

We do have WPT tests that make use of the functionality being altered and in the worst-case the feature can be disabled via Finch entirely. The fix is scoped specifically to the feature and has no risk of affecting other functionality.

This issue is an OT blocker so I think it's better to take the relatively small risk and fallback on finch or delay the OT if it turns out that there is an issue since the alternative without this fix would be to delay the OT anyways.

Based on this reasoning I'm starting the merge to 6478.

### ap...@google.com (2024-05-29)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 7e688c44daa1af50683dfdba644ceffc85873c35
Author: Andy Paicu <andypaicu@chromium.org>
Date:   Wed May 29 12:04:11 2024

    [PEPC] Clamp min-width/height based on the maximum allowed value as well
    
    The min/max-width/height properties for the permission element are
    bounded in an effort to prevent the width/height from going above/below
    certain hard-set limits. However the min-width/height will overrule
    the max-width/height if it's bigger. This means that the current
    restrictions can be bypassed in one direction by setting the
    min-width/height to very large values, as they are currently only lower
    bounded (restricted from being too small). This CL instead changes the
    logic to clamp the min-width/height so that it also has an upper bound.
    
    (cherry picked from commit 1fa5805fe6a4df6a1eacf969c065ba474a5c6e3a)
    
    Fixed: 341947676
    Change-Id: I6fe68b6d9f07e4041e5c4455fc34dce167b01be5
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5563906
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
    Commit-Queue: Andy Paicu <andypaicu@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1305710}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5576999
    Auto-Submit: Andy Paicu <andypaicu@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#806}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/core/html/html_permission_element.cc
M       third_party/blink/renderer/core/html/html_permission_element.h
M       third_party/blink/web_tests/external/wpt/html/semantics/permission-element/bounded-sizes.tentative.html
A       third_party/blink/web_tests/external/wpt/html/semantics/permission-element/large-min-size-reftest-ref.html
A       third_party/blink/web_tests/external/wpt/html/semantics/permission-element/large-min-size-reftest.tentative.html

https://chromium-review.googlesource.com/5576999


### pe...@google.com (2024-05-29)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### vo...@google.com (2024-05-30)

According to bisect in the report, this was introduced in M125 so it's not applicable to M120 LTS.

### pg...@google.com (2024-06-10)

updating Impact based on [comment #3](https://issues.chromium.org/issues/341947676#comment3) - this feature was off by default at the time of fix

### sp...@google.com (2024-06-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$1,000 for report of lower impact exploit mitigation bypass + $1,000 bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-28)

Thank you for your efforts and for digging into PEPC, Alesandro and reporting this issue to us! 

### al...@alesandroortiz.com (2024-06-28)

Thanks for the reward!

### pe...@google.com (2024-09-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/341947676)*
