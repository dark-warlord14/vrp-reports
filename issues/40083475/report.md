# Heap-buffer-overflow in blink::TimerBase::stop

| Field | Value |
|-------|-------|
| **Issue ID** | [40083475](https://issues.chromium.org/issues/40083475) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms |
| **Platforms** | Windows |
| **Reporter** | mi...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2015-12-30 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6507228867067904

Fuzzer: miaubiz_css_fuzzer
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Heap-buffer-overflow WRITE 16
Crash Address: 0x0e10eb80
Crash State:
  blink::TimerBase::stop
  blink::HTMLInputElement::onSearch
  blink::internal::CallClosureTask::performTask
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome_no_sandbox&range=367066:367086

Minimized Testcase (2.46 Kb): https://cluster-fuzz.appspot.com/download/AMIfv949s5zLX2O72IaUKD-OZadGlpi91QBaNU4xqtiTdUtobqloCZINUl4MLFLbalBEs_ZnQwU6x1JWKeK0nrjOAKj1sTAjMaXm2USHl2YXHblaOnShKCRoGIEr9N3SQJlmVV8QT1cXneQW4EdK1vjcBkaXV-c7sQ

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### in...@chromium.org (2015-12-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-31)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### mb...@chromium.org (2015-12-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6491273566879744

Fuzzer: miaubiz_css_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 16
Crash Address: 0xafd87fe8
Crash State:
  blink::TimerBase::stop
  blink::SearchInputType::stopSearchEventTimer
  blink::HTMLInputElement::onSearch
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=365683:365986

Minimized Testcase (1.51 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95sK86vVAQYEkLdaXgFvBg5FEJMqsYIdEq3WYAzcHD-Gc3Lf6BhTW7fTa9ylmhITdnuuF3Tg9KNkVDjEZke7m28DATVvAT4PweQM0hRF9U8KD_Trji7Oy0Fez2oxu6KIz3vZb03KxBdPVAstwH8oDOQkBiLeQ

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### tk...@chromium.org (2016-01-06)

This is a regression by the fix for https://crbug.com/chromium/570427, and it was merged to M48 branch.


### tk...@chromium.org (2016-01-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-06)

[Empty comment from Monorail migration]

### tk...@chromium.org (2016-01-06)

[Empty comment from Monorail migration]

### ko...@chromium.org (2016-01-06)

[Comment Deleted]

### ko...@chromium.org (2016-01-06)

[Comment Deleted]

### bu...@chromium.org (2016-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/83b72340208ddb3112d7bee1dadff92aa3fd7af2

commit 83b72340208ddb3112d7bee1dadff92aa3fd7af2
Author: tkent <tkent@chromium.org>
Date: Wed Jan 06 05:28:23 2016

Fix a crash in HTMLInputElement::onSearch.

Since crrev.com/365773, HTMLInputElement::onSearch can be called with non-search
InputType.
 - Virtualize the content of HTMLInputElement::onSearch
 - Remove SearchInputType::stopSearchEventTimer
   It is used only internally, and its content is one line.

BUG=573284
TEST=automated

Review URL: https://codereview.chromium.org/1560973002

Cr-Commit-Position: refs/heads/master@{#367781}

[add] http://crrev.com/83b72340208ddb3112d7bee1dadff92aa3fd7af2/third_party/WebKit/LayoutTests/fast/forms/search/search-change-type-before-onsearch.html
[modify] http://crrev.com/83b72340208ddb3112d7bee1dadff92aa3fd7af2/third_party/WebKit/Source/core/html/HTMLInputElement.cpp
[modify] http://crrev.com/83b72340208ddb3112d7bee1dadff92aa3fd7af2/third_party/WebKit/Source/core/html/forms/InputType.cpp
[modify] http://crrev.com/83b72340208ddb3112d7bee1dadff92aa3fd7af2/third_party/WebKit/Source/core/html/forms/InputType.h
[modify] http://crrev.com/83b72340208ddb3112d7bee1dadff92aa3fd7af2/third_party/WebKit/Source/core/html/forms/SearchInputType.cpp
[modify] http://crrev.com/83b72340208ddb3112d7bee1dadff92aa3fd7af2/third_party/WebKit/Source/core/html/forms/SearchInputType.h


### tk...@chromium.org (2016-01-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-01-06)

[Auto-generated comment by a script] We noticed that this issue is targeted for M-48; it appears the fix may have landed after branch point, meaning a merge might be required. Please confirm if a merge is required here - if so add Merge-Request-48 label, otherwise remove Merge-TBD label. Thanks.

### cl...@chromium.org (2016-01-06)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-06)

ClusterFuzz has detected this issue as fixed in range 367728:367781.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6491273566879744

Fuzzer: miaubiz_css_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 16
Crash Address: 0xafd87fe8
Crash State:
  blink::TimerBase::stop
  blink::SearchInputType::stopSearchEventTimer
  blink::HTMLInputElement::onSearch
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=365683:365986
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=367728:367781

Minimized Testcase (1.51 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95sK86vVAQYEkLdaXgFvBg5FEJMqsYIdEq3WYAzcHD-Gc3Lf6BhTW7fTa9ylmhITdnuuF3Tg9KNkVDjEZke7m28DATVvAT4PweQM0hRF9U8KD_Trji7Oy0Fez2oxu6KIz3vZb03KxBdPVAstwH8oDOQkBiLeQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### tk...@chromium.org (2016-01-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-07)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6507228867067904

Fuzzer: miaubiz_css_fuzzer
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Heap-buffer-overflow WRITE 16
Crash Address: 0x0e10eb80
Crash State:
  blink::TimerBase::stop
  blink::HTMLInputElement::onSearch
  blink::internal::CallClosureTask::performTask
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome_no_sandbox&range=367066:367086

Minimized Testcase (2.46 Kb): https://cluster-fuzz.appspot.com/download/AMIfv949s5zLX2O72IaUKD-OZadGlpi91QBaNU4xqtiTdUtobqloCZINUl4MLFLbalBEs_ZnQwU6x1JWKeK0nrjOAKj1sTAjMaXm2USHl2YXHblaOnShKCRoGIEr9N3SQJlmVV8QT1cXneQW4EdK1vjcBkaXV-c7sQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ti...@google.com (2016-01-07)

Congrats your change is auto-approved for M48 (branch: 2564)

### bu...@chromium.org (2016-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/890b7c98bcee9bc8e4b8d25e35e5ddad6b6f5a36

commit 890b7c98bcee9bc8e4b8d25e35e5ddad6b6f5a36
Author: Kent Tamura <tkent@chromium.org>
Date: Thu Jan 07 04:48:32 2016

Fix a crash in HTMLInputElement::onSearch.

Since crrev.com/365773, HTMLInputElement::onSearch can be called with non-search
InputType.
 - Virtualize the content of HTMLInputElement::onSearch
 - Remove SearchInputType::stopSearchEventTimer
   It is used only internally, and its content is one line.

BUG=573284
TEST=automated

Review URL: https://codereview.chromium.org/1560973002

Cr-Commit-Position: refs/heads/master@{#367781}
(cherry picked from commit 83b72340208ddb3112d7bee1dadff92aa3fd7af2)

Review URL: https://codereview.chromium.org/1563883005 .

Cr-Commit-Position: refs/branch-heads/2564@{#500}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[add] http://crrev.com/890b7c98bcee9bc8e4b8d25e35e5ddad6b6f5a36/third_party/WebKit/LayoutTests/fast/forms/search/search-change-type-before-onsearch.html
[modify] http://crrev.com/890b7c98bcee9bc8e4b8d25e35e5ddad6b6f5a36/third_party/WebKit/Source/core/html/HTMLInputElement.cpp
[modify] http://crrev.com/890b7c98bcee9bc8e4b8d25e35e5ddad6b6f5a36/third_party/WebKit/Source/core/html/forms/InputType.cpp
[modify] http://crrev.com/890b7c98bcee9bc8e4b8d25e35e5ddad6b6f5a36/third_party/WebKit/Source/core/html/forms/InputType.h
[modify] http://crrev.com/890b7c98bcee9bc8e4b8d25e35e5ddad6b6f5a36/third_party/WebKit/Source/core/html/forms/SearchInputType.cpp
[modify] http://crrev.com/890b7c98bcee9bc8e4b8d25e35e5ddad6b6f5a36/third_party/WebKit/Source/core/html/forms/SearchInputType.h


### bu...@chromium.org (2016-01-07)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/890b7c98bcee9bc8e4b8d25e35e5ddad6b6f5a36

commit 890b7c98bcee9bc8e4b8d25e35e5ddad6b6f5a36
Author: Kent Tamura <tkent@chromium.org>
Date: Thu Jan 07 04:48:32 2016


### sh...@chromium.org (2016-04-13)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-30)

(non-stable bug reward panel backlog round)

$3,500 for this one as well ($3k for the bug, $500 for the fuzzer).

### aw...@chromium.org (2016-06-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/573284?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083475)*
