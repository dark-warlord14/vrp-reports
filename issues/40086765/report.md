# Bad-cast to blink::LayoutInline from blink::LayoutSVGText;blink::LineLayoutInline::lastLineBox;blink::LayoutBlockFlow::createLineBoxes

| Field | Value |
|-------|-------|
| **Issue ID** | [40086765](https://issues.chromium.org/issues/40086765) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ec...@igalia.com |
| **Created** | 2017-02-11 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6175207984463872

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_ubsan_vptr_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x2abbba068000
Crash State:
  Bad-cast to blink::LayoutInline from blink::LayoutSVGText
  blink::LineLayoutInline::lastLineBox
  blink::LayoutBlockFlow::createLineBoxes
  
Sanitizer: undefined (UBSAN)

Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_ubsan_vptr_chrome&range=449612:449646

Reproducer Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97kConIitupit1nYK09BulcdpMNGKY1GlLAF8sbKmpv3jgXvIRcA-PSHhLXOH6PMg6x87YDThMOc2mrMXnFX8xi858801bBHuVzrWoBGbswePnikPiIOgegUs9jVaKL6sOWqa_uATQC-791qO6Vy1dFDeeExV_KjaXLuKoDgTTEsIt8bYzxFDFciH2DhRoDYw5gaqn6n-Acz0LZfTVwr6NhUAY0dNW6wfIHWYDXXGOatAob3YqnGp5tGusqEDRS0Gz_wCFPSjmKxKy3SO3CsskECe4nSRKuPJCq8z6HJchEdLgO7Q4DndiRxvAmfGJI9Y0f_N4yRldDT8JzKU12rXOXS0-hfNYSRLQCSSv6FUvSM1NtrddbYjelfH7nxMpM-iOX737Syy9EZl901HP-3E7u6nbWHQ?testcase_id=6175207984463872


Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### sh...@chromium.org (2017-02-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-11)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-02-11)

[Empty comment from Monorail migration]

### ji...@chromium.org (2017-02-11)

Hi ecobos@igalia.com, could you take a look to see if this is caused by your latest cl https://codereview.chromium.org/2685113002?  Please feel free to re-assign. Thanks!

[Monorail components: Blink>Layout]

### ec...@igalia.com (2017-02-11)

Sure, I missed one call-site for <marker> elements, I'll submit a fix soon.

### ec...@igalia.com (2017-02-11)

https://codereview.chromium.org/2694573002/

### bu...@chromium.org (2017-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9d35915a17f98cbdeb655d3bfac57f1432f858b4

commit 9d35915a17f98cbdeb655d3bfac57f1432f858b4
Author: ecobos <ecobos@igalia.com>
Date: Sat Feb 11 22:32:04 2017

Don't unconditionally create a LayoutObject for SVGMarkerElement.

This is a followup to https://codereview.chromium.org/2685113002/. I
missed this override.

BUG=691196

Review-Url: https://codereview.chromium.org/2694573002
Cr-Commit-Position: refs/heads/master@{#449877}

[add] https://crrev.com/9d35915a17f98cbdeb655d3bfac57f1432f858b4/third_party/WebKit/LayoutTests/svg/crash-svg-marker-in-html.html
[modify] https://crrev.com/9d35915a17f98cbdeb655d3bfac57f1432f858b4/third_party/WebKit/Source/core/svg/SVGMarkerElement.cpp
[modify] https://crrev.com/9d35915a17f98cbdeb655d3bfac57f1432f858b4/third_party/WebKit/Source/core/svg/SVGMarkerElement.h


### ec...@igalia.com (2017-02-12)

Should be fixed now, let me know if I should do anything else.

Thanks for the report :)

### ec...@igalia.com (2017-02-12)

Oh, also maybe worth noting. Without asan this crashes in a SECURITY_DCHECK, so I'm not sure whether it's exploitable or not.

### cl...@chromium.org (2017-02-12)

ClusterFuzz has detected this issue as fixed in range 449876:449877.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6175207984463872

Fuzzer: miaubiz_svg_fuzzer
Job Type: linux_ubsan_vptr_chrome
Platform Id: linux

Crash Type: Bad-cast
Crash Address: 0x2abbba068000
Crash State:
  Bad-cast to blink::LayoutInline from blink::LayoutSVGText
  blink::LineLayoutInline::lastLineBox
  blink::LayoutBlockFlow::createLineBoxes
  
Sanitizer: undefined (UBSAN)

Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_ubsan_vptr_chrome&range=449612:449646
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_ubsan_vptr_chrome&range=449876:449877

Reproducer Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97kConIitupit1nYK09BulcdpMNGKY1GlLAF8sbKmpv3jgXvIRcA-PSHhLXOH6PMg6x87YDThMOc2mrMXnFX8xi858801bBHuVzrWoBGbswePnikPiIOgegUs9jVaKL6sOWqa_uATQC-791qO6Vy1dFDeeExV_KjaXLuKoDgTTEsIt8bYzxFDFciH2DhRoDYw5gaqn6n-Acz0LZfTVwr6NhUAY0dNW6wfIHWYDXXGOatAob3YqnGp5tGusqEDRS0Gz_wCFPSjmKxKy3SO3CsskECe4nSRKuPJCq8z6HJchEdLgO7Q4DndiRxvAmfGJI9Y0f_N4yRldDT8JzKU12rXOXS0-hfNYSRLQCSSv6FUvSM1NtrddbYjelfH7nxMpM-iOX737Syy9EZl901HP-3E7u6nbWHQ?testcase_id=6175207984463872


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-02-12)

ClusterFuzz testcase 6175207984463872 is verified as fixed, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-02-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-28)

Nice one! The panel decided to award $3,500 for this bug!  Thanks!

### aw...@chromium.org (2017-02-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-05-21)

This issue was migrated from crbug.com/chromium/691196?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/691204]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086765)*
