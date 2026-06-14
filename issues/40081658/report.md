# Container-overflow in blink::FEColorMatrix::createImageFilter

| Field | Value |
|-------|-------|
| **Issue ID** | [40081658](https://issues.chromium.org/issues/40081658) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SVG |
| **Reporter** | cl...@chromium.org |
| **Assignee** | sc...@chromium.org |
| **Created** | 2015-03-18 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6357880798707712

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Container-overflow READ 4
Crash Address: 0x602000065750
Crash State:
  blink::FEColorMatrix::createImageFilter
  blink::FilterEffect::createImageFilterWithoutValidation
  blink::SkiaImageFilterBuilder::build
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=316793:316810

Minimized Testcase (5.82 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97pnz2ZhT8jbhH--6BisaAdiCglwJovyAYeifbmnKHi3mhI2BwRp1FssTPUBHEJh51UvtFGIL8nYoOgdJlY6GXIN1Zw81CdoKC_eEnegMabkGGSGcA-ArNA4Upme8O5uxDRAAOlfkYb6OeVjmi5EfYvYLTEog

Filer: ochang

## Timeline

### cl...@chromium.org (2015-03-18)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6380843153489920

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Container-overflow READ {*}
Crash Address: 0x6080000314a0
Crash State:
  blink::FEColorMatrix::createImageFilter
  blink::FilterEffect::createImageFilterWithoutValidation
  blink::SkiaImageFilterBuilder::build
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=316591:316716

Minimized Testcase (4.54 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94BNSQc7v1fXcdoOa46P8ZACznWWSj64cyvu5EkKbDanazE4G3SLRPL_4oxiHrlPDwRd7Hfw7XxWIm40qk8BPr7RaJLV856hLlds7sBApNziIlWcHeNO1CNUXK9WdMAVqH5MFz97XBpnuUgXxQyPePVA0GOkA

Filer: ochang

### oc...@chromium.org (2015-03-18)

It appears that the size of |values| isn't checked for createColorFilter in FEColorMatrix.cpp. After some initial investigation for one of these crashes (the first), it appears to be happening because an empty WTF::Vector being passed to FEColorMatrix::setValues, with createColorFilter being called later on on this |m_values|'s |.data()| afterwards. 

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/platform/graphics/filters/FEColorMatrix.cpp&sq=package:chromium&type=cs&l=128

### oc...@chromium.org (2015-03-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-19)

[Empty comment from Monorail migration]

### se...@chromium.org (2015-03-19)

Historically, this code has always assumed at least 20 elements in that vector in the Matrix case, and the callers seem to ensure this:

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/svg/SVGFEColorMatrixElement.cpp&q=FEColorMatrix::create&sq=package:chromium&type=cs&l=139
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/layout/FilterEffectRenderer.cpp&q=FEColorMatrix::create&sq=package:chromium&type=cs&l=125
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/layout/FilterEffectRenderer.cpp&q=FEColorMatrix::create&sq=package:chromium&type=cs&l=152

We could easily add a check, but I can't think what might have changed here.

### oc...@chromium.org (2015-03-19)

Here's the backtrace for what I believe is the offending setValues (which sets the zero length vector).

#0  shrink () at ../../third_party/WebKit/Source/wtf/Vector.h:991
#1  operator= () at ../../third_party/WebKit/Source/wtf/Vector.h:811
#2  0x000000000ef0d53b in setValues () at ../../third_party/WebKit/Source/platform/graphics/filters/FEColorMatrix.cpp:68
#3  0x000000000f562145 in setFilterEffectAttribute () at ../../third_party/WebKit/Source/core/svg/SVGFEColorMatrixElement.cpp:81
#4  0x00000000091eee18 in primitiveAttributeChanged () at ../../third_party/WebKit/Source/core/layout/svg/LayoutSVGResourceFilter.cpp:148
#5  0x00000000092ebfce in primitiveAttributeChanged () at ../../third_party/WebKit/Source/core/layout/svg/LayoutSVGResourceFilterPrimitive.h:53
#6  primitiveAttributeChanged () at ../../third_party/WebKit/Source/core/svg/SVGFilterPrimitiveStandardAttributes.cpp:143
#7  0x000000000f562692 in svgAttributeChanged () at ../../third_party/WebKit/Source/core/svg/SVGFEColorMatrixElement.cpp:97
#8  0x00000000092c6449 in attributeChanged () at ../../third_party/WebKit/Source/core/svg/SVGElement.cpp:859
#9  0x0000000005ed47ca in didModifyAttribute () at ../../third_party/WebKit/Source/core/dom/Element.cpp:2950
#10 setAttributeInternal () at ../../third_party/WebKit/Source/core/dom/Element.cpp:1059
#11 setAttribute () at ../../third_party/WebKit/Source/core/dom/Element.cpp:1012
#12 0x00000000098edd36 in setAttributeMethod () at gen/blink/bindings/core/v8/V8Element.cpp:1391
#13 setAttributeMethodCallback () at gen/blink/bindings/core/v8/V8Element.cpp:1401
#14 0x0000000004294ade in Call () at ../../v8/src/arguments.cc:33
#15 0x00000000031f5a83 in HandleApiCallHelper<false> () at ../../v8/src/builtins.cc:1077
#16 0x0000000003206e25 in Builtin_implHandleApiCall () at ../../v8/src/builtins.cc:1100
#17 Builtin_HandleApiCall () at ../../v8/src/builtins.cc:1096


### sc...@chromium.org (2015-03-19)

senorblanco, do you want to own it and fix it? I overlooked it due to misconfigured email filters, but can fix it if you like.

### mb...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-04)

ClusterFuzz has detected this issue as fixed in range 323876:323879.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6357880798707712

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Container-overflow READ 4
Crash Address: 0x602000065750
Crash State:
  blink::FEColorMatrix::createImageFilter
  blink::FilterEffect::createImageFilterWithoutValidation
  blink::SkiaImageFilterBuilder::build
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=316793:316810
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=323876:323879

Minimized Testcase (5.82 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97pnz2ZhT8jbhH--6BisaAdiCglwJovyAYeifbmnKHi3mhI2BwRp1FssTPUBHEJh51UvtFGIL8nYoOgdJlY6GXIN1Zw81CdoKC_eEnegMabkGGSGcA-ArNA4Upme8O5uxDRAAOlfkYb6OeVjmi5EfYvYLTEog

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-04-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4967816457879552

Fuzzer: Inferno_layout_test_unmodified
Job Type: Linux_asan_chrome_mp

Crash Type: Container-overflow READ 4
Crash Address: 0x602000064c90
Crash State:
  blink::FEColorMatrix::createImageFilter
  blink::FilterEffect::createImageFilterWithoutValidation
  blink::SkiaImageFilterBuilder::build
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=317506:317512

Minimized Testcase (4.49 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Mw4W9TOpnQ2Vm7PggpCoak2JfP3eabrPGR89CVHvt9GbMI2uWw22-YZP2kRRQgX1lASxapQVy4hICStDclwStuC_ZM6_783FaQuTDzgBEWf_ocJDQNjt0XP_RSO5gcEgqDU6fKyklwShSnIs_nWSjx1Az2w

Filer: inferno

### in...@chromium.org (2015-04-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-04-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-10)

schenney@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### sc...@chromium.org (2015-04-10)

I can't reproduce this on ToT and we do get a console error for invalid values attribute. I agree that we shouldn't be checking but I'll make sure the setAttribute caller is always passing the correct size.

### in...@chromium.org (2015-04-10)

Are you using an ASAN build with these env options set. You need the detect_container_overflow=1

ASAN_OPTIONS = alloc_dealloc_mismatch=0:strict_memcmp=0:redzone=128:malloc_context_size=128:detect_stack_use_after_return=1:max_uar_stack_size_log=16:handle_segv=1:symbolize=false:check_malloc_usable_size=0:fast_unwind_on_fatal=1:allocator_may_return_null=1:detect_odr_violation=0:detect_container_overflow=1

### bu...@chromium.org (2015-04-10)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=193571

------------------------------------------------------------------
r193571 | schenney@chromium.org | 2015-04-10T22:35:26.259585Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGFEColorMatrixElement.cpp?r1=193571&r2=193570&pathrev=193571
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/graphics/filters/FEColorMatrix.cpp?r1=193571&r2=193570&pathrev=193571

Explicitly enforce values size in feColorMatrix.

R=senorblanco@chromium.org
BUG=468519

Review URL: https://codereview.chromium.org/1075413002
-----------------------------------------------------------------

### cl...@chromium.org (2015-04-13)

ClusterFuzz has detected this issue as fixed in range 324711:324828.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4967816457879552

Fuzzer: Inferno_layout_test_unmodified
Job Type: Linux_asan_chrome_mp

Crash Type: Container-overflow READ 4
Crash Address: 0x602000064c90
Crash State:
  blink::FEColorMatrix::createImageFilter
  blink::FilterEffect::createImageFilterWithoutValidation
  blink::SkiaImageFilterBuilder::build
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=317506:317512
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=324711:324828

Minimized Testcase (4.49 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Mw4W9TOpnQ2Vm7PggpCoak2JfP3eabrPGR89CVHvt9GbMI2uWw22-YZP2kRRQgX1lASxapQVy4hICStDclwStuC_ZM6_783FaQuTDzgBEWf_ocJDQNjt0XP_RSO5gcEgqDU6fKyklwShSnIs_nWSjx1Az2w

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-04-13)

[Empty comment from Monorail migration]

### sc...@chromium.org (2015-04-13)

I have to reopen. The fix violates the web spec so we'll need another round.

### sc...@chromium.org (2015-04-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-04-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=193911

------------------------------------------------------------------
r193911 | schenney@chromium.org | 2015-04-16T23:40:41.049067Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/graphics/filters/FEColorMatrix.cpp?r1=193911&r2=193910&pathrev=193911
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/filters/feColorMatrix-setAttribute-crash1-expected.txt?r1=193911&r2=193910&pathrev=193911
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/filters/feColorMatrix-setAttribute-crash2-expected.txt?r1=193911&r2=193910&pathrev=193911
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/svg/SVGFEColorMatrixElement.cpp?r1=193911&r2=193910&pathrev=193911
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/graphics/filters/FEColorMatrix.h?r1=193911&r2=193910&pathrev=193911
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/filters/feColorMatrix-setAttribute-crash1.html?r1=193911&r2=193910&pathrev=193911
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/filters/feColorMatrix-setAttribute-crash2.html?r1=193911&r2=193910&pathrev=193911

Rework the checks for too-few values in feColorMatrix filter.

Revert the prevous fix because it was flat-out wrong for some
filters. Here we add checks at all points the values are used,
because it is impossible to enforce an always-valid m_values vector
inside the FEColorMatrix object.

For example, we need to support any ordering of setAttribute('type', ...)
and setAttribute('values', ...), but the valid number of values depends
on the type. We couldn't set the type from "hueRotate" to "matrix", for
example, without first adding more values than are necessary for the
"hueRotate". That's a bad user experience.

R=fs@opera.com,ed@opera.com,pdr@chromium.org
BUG=468519

Review URL: https://codereview.chromium.org/1087283002
-----------------------------------------------------------------

### in...@chromium.org (2015-04-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-21)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-05-08)

Merge requested for M43 (branch 2357)

### la...@google.com (2015-05-08)

[Automated comment] Reverts referenced in bugdroid comments, needs manual review.

### la...@google.com (2015-05-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-13)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=195283

------------------------------------------------------------------
r195283 | schenney@chromium.org | 2015-05-13T01:13:11.384514Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2357/LayoutTests/svg/filters/feColorMatrix-setAttribute-crash1.html?r1=195283&r2=195282&pathrev=195283
   A http://src.chromium.org/viewvc/blink/branches/chromium/2357/LayoutTests/svg/filters/feColorMatrix-setAttribute-crash2.html?r1=195283&r2=195282&pathrev=195283
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/platform/graphics/filters/FEColorMatrix.cpp?r1=195283&r2=195282&pathrev=195283
   A http://src.chromium.org/viewvc/blink/branches/chromium/2357/LayoutTests/svg/filters/feColorMatrix-setAttribute-crash1-expected.txt?r1=195283&r2=195282&pathrev=195283
   A http://src.chromium.org/viewvc/blink/branches/chromium/2357/LayoutTests/svg/filters/feColorMatrix-setAttribute-crash2-expected.txt?r1=195283&r2=195282&pathrev=195283
   M http://src.chromium.org/viewvc/blink/branches/chromium/2357/Source/platform/graphics/filters/FEColorMatrix.h?r1=195283&r2=195282&pathrev=195283

Rework the checks for too-few values in feColorMatrix filter.

Revert the prevous fix because it was flat-out wrong for some
filters. Here we add checks at all points the values are used,
because it is impossible to enforce an always-valid m_values vector
inside the FEColorMatrix object.

For example, we need to support any ordering of setAttribute('type', ...)
and setAttribute('values', ...), but the valid number of values depends
on the type. We couldn't set the type from "hueRotate" to "matrix", for
example, without first adding more values than are necessary for the
"hueRotate". That's a bad user experience.

TBR=laforge@chromium.org
BUG=468519

Review URL: https://codereview.chromium.org/1087283002

(cherry picked from commit 9ae9e4492c79ea25f96297f198c4ad57636ab049)

Review URL: https://codereview.chromium.org/1135023003
-----------------------------------------------------------------

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-28)

$1000 for the bug, $500 Fuzzer bonus for a total of $1500. I'll start payment shortly. 

### ti...@google.com (2015-06-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### cl...@chromium.org (2015-07-28)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/468519?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/475469]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081658)*
