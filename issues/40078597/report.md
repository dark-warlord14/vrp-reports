# Heap-use-after-free in WebCore::RenderInline::willBeDestroyed

| Field | Value |
|-------|-------|
| **Issue ID** | [40078597](https://issues.chromium.org/issues/40078597) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Layout |
| **Reporter** | cl...@chromium.org |
| **Assignee** | jc...@chromium.org |
| **Created** | 2013-12-24 |
| **Bounty** | $2,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5091034006552576

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61200002df80
Crash State:
  - crash stack -
  WebCore::RenderInline::willBeDestroyed
  WebCore::RenderObject::destroy
  - free stack -
  WebCore::RenderBlock::removeChild
  WebCore::RenderObject::willBeDestroyed
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=241803:241817

Minimized Testcase (0.96 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97wtDtQIVVy3BNEkxSazfPCJD15mYFU18MAIDYJyCwnGVzm7XHTwjciOaurCWsKZLtQNpMobnl3EoYDOLcyk1ndXoz2EezmuBpCZvru8lSK7g7sUnNRqnAWBsaEHJSIc19fyvONLTuTi5cHc3irAjkk31MfLw

## Timeline

### cl...@chromium.org (2013-12-24)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### mb...@chromium.org (2013-12-30)

Any idea who a good owner for this might be, inferno@?

### in...@chromium.org (2014-01-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-01-01)

This is stable continuation issue, regression from http://src.chromium.org/viewvc/blink?view=rev&revision=164125. confirmed locally.

reverted in r164405.

### cl...@chromium.org (2014-01-01)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-01-04)

ClusterFuzz has detected this issue as fixed in range 242799:242830.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5091034006552576

Fuzzer: Miaubiz_css_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61200002df80
Crash State:
  - crash stack -
  WebCore::RenderInline::willBeDestroyed
  WebCore::RenderObject::destroy
  - free stack -
  WebCore::RenderBlock::removeChild
  WebCore::RenderObject::willBeDestroyed
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=241803:241817
Fixed: https://cluster-fuzz.appspot.com/revisions?range=242799:242830

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97wtDtQIVVy3BNEkxSazfPCJD15mYFU18MAIDYJyCwnGVzm7XHTwjciOaurCWsKZLtQNpMobnl3EoYDOLcyk1ndXoz2EezmuBpCZvru8lSK7g7sUnNRqnAWBsaEHJSIc19fyvONLTuTi5cHc3irAjkk31MfLw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### dh...@google.com (2014-01-07)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-09)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-04-14)

Thanks for the report - $2000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### la...@google.com (2015-01-09)

Migrate from Cr-Blink-Rendering to Cr-Blink-Layout

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/330626?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/331029]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078597)*
