# Use-of-uninitialized-value in gfx::CubicBezier::SolveCurveX

| Field | Value |
|-------|-------|
| **Issue ID** | [40050182](https://issues.chromium.org/issues/40050182) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>SVG |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | fs...@opera.com |
| **Created** | 2019-09-21 |
| **Bounty** | $4,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5660161319239680

Fuzzer: attekett_surku_fuzzer
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  gfx::CubicBezier::SolveCurveX
  blink::SVGAnimationElement::CalculatePercentForSpline
  blink::SVGAnimationElement::UpdateAnimation
  
Sanitizer: memory (MSAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_msan_chrome&range=676625:676652

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5660161319239680

Issue filed automatically.

See https://www.chromium.org/developers/testing/memorysanitizer#TOC-Reproducing-ClusterFuzz-Bugs for instructions on reproducing this bug locally.

## Timeline

### cl...@chromium.org (2019-09-21)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>SVG UI>GFX]

### sh...@chromium.org (2019-09-21)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sc...@chromium.org (2019-09-23)

fs@, can you take a look given you're in the animation space.

[Monorail components: -UI>GFX]

### sc...@chromium.org (2019-09-23)

And let me know if you need to see the clusterfuzz example.

### sc...@chromium.org (2019-09-23)

[Empty comment from Monorail migration]

### fs...@opera.com (2019-09-23)

Looking at the TC I can't help but think that the following key spline has something to do with it:

0 1 -13243226291074068574 1

..but I'll look a little closer.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a3a0eeb5acf5c6f684dfcd5d23740be8a33e7386

commit a3a0eeb5acf5c6f684dfcd5d23740be8a33e7386
Author: Fredrik Söderquist <fs@opera.com>
Date: Tue Sep 24 16:15:35 2019

Restrict 'keySplines' x-values to the [0, 1] range

Per SMIL[1], all the values in a key spline should be within [0, 1], but
to be consistent with CSS' timing function, allow y-values to be outside
that range (at least for now).

While in ParseKeySplinesInternal(...), rename the |pos_*| local
variables to something that carries a little bit more semantic meaning.

[1] https://www.w3.org/TR/SMIL3/smil-animation.html#adef-keySplines

Bug: 1006544
Change-Id: I6baa4085943eca8144605fb0a5c442bc8486ad87
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1821158
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Commit-Queue: Fredrik Söderquist <fs@opera.com>
Cr-Commit-Position: refs/heads/master@{#699373}

[modify] https://crrev.com/a3a0eeb5acf5c6f684dfcd5d23740be8a33e7386/third_party/blink/renderer/core/svg/svg_animation_element.cc
[add] https://crrev.com/a3a0eeb5acf5c6f684dfcd5d23740be8a33e7386/third_party/blink/web_tests/external/wpt/svg/animations/keysplines-x-limits.html


### cl...@chromium.org (2019-09-25)

ClusterFuzz testcase 5660161319239680 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_msan_chrome&range=699368:699415

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-09-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-26)

Requesting merge to beta M78 because latest trunk commit (699373) appears to be after beta branch point (693954).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-09-26)

fs@ , pls share the change works as intended on canary and the merge is safe for M78

### fs...@opera.com (2019-09-26)

It should be safe to merge. (Not sure "Medium" severity is warranted here, but there's too much code downstream of this value to check for potential issues.)

### sr...@google.com (2019-09-26)

merge approved for M78, branch:3904

### sr...@google.com (2019-09-27)

Please help complete the merge to M78 branch 3904 before Monday Sept 30, end of day PST.

### fs...@opera.com (2019-09-27)

It should be merged already (https://chromium-review.googlesource.com/c/chromium/src/+/1827371) but it seems the bot hasn't noticed (or something)?

### sh...@chromium.org (2019-09-30)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fs...@opera.com (2019-09-30)

Per c#16 I'm removing the Merge-Approved label.

### na...@google.com (2019-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-04)

Congrats! The Panel decided to reward $3,000 for this report + a $1,000 fuzzing bonus :) 

### na...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### sc...@chromium.org (2019-10-16)

Sorry, not sure why I removed you from the bug.

### ad...@google.com (2019-10-17)

Assuming this affects all Blinky platforms.

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1006544?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050182)*
