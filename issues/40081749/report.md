# Heap-buffer-overflow in url::ParsePort

| Field | Value |
|-------|-------|
| **Issue ID** | [40081749](https://issues.chromium.org/issues/40081749) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | rh...@partner.samsung.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2015-03-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Heap-buffer-overflow happens when parsing a nasty url.

**VERSION**  

Chrome Version: 43.0.2350.0 (Developer Build) (64-bit), Blink @192720  

Operating System: Ubuntu 14.04

**REPRODUCTION CASE**  

Load this test via http with a release ASAN chrome/content\_shell or a debug ASAN content\_shell:

<base href="gopher:��&#279%�:0"></base>
<script src=":"></script>

If you run the test with a debug ASAN Chrome then it will fail on a DHCECK in GURL::InitializeFromCanonicalSpec.  

The backtraces and the test case are attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Attachments

- [crash.html](attachments/crash.html) (text/html, 71 B)
- [overflow_backtrace.txt](attachments/overflow_backtrace.txt) (text/plain, 25.8 KB)
- [dcheck_fail_backtrace.txt](attachments/dcheck_fail_backtrace.txt) (text/plain, 3.4 KB)

## Timeline

### cl...@chromium.org (2015-03-28)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6196559406956544

### cl...@chromium.org (2015-03-29)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6196559406956544

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60c00022aa0e
Crash State:
  url::ParsePort
  blink::KURL::port
  blink::SecurityOrigin::SecurityOrigin
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=311376:311466

Minimized Testcase (0.05 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94CYigilCe3H9ot7OO0Ou3QBkF9A0OsY9szMVtjarWzksibcM7x8ZAdXd_fg3jdJ4Nm4i1bqsVK4LmsRJT4GpMMbvq9afRMyy9KlL-63xnQjT-ELfznGbvemIaBkXpQcjeTD1awjJV3wJnK_uh__uTngQ8MPA
<base href="gopher:��&#279%�:0"><script src=":">


Additional requirements: Requires HTTP



### cl...@chromium.org (2015-03-29)

[Empty comment from Monorail migration]

### ts...@chromium.org (2015-03-30)

[Empty comment from Monorail migration]

### ts...@chromium.org (2015-03-30)

Assigning to Nate based on CF suggestion.  Is is possible you're passing bad input here? Feel free to re-assign as appropriate. Thanks

### ja...@chromium.org (2015-03-30)

I'm suspicious of https://chromium.googlesource.com/chromium/blink/+/5cf6e0e088a76254a2d1ba72dd2867c955f09c4c, since HTMLDocumentParser::resumeParsingAfterYield() is on the stack.

kouhei, would you mind taking a look? Feel free to assign back to me if my theory is wrong.

### cl...@chromium.org (2015-03-30)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ko...@chromium.org (2015-03-31)

[Empty comment from Monorail migration]

### ko...@chromium.org (2015-03-31)

Looks like TokenPreloadScanner::updatePredictedBaseURL accepts invalid urls, and Document::completeURLWithOverride force mark the invalid url passed to it as valid.
Confirmed fix locally, will upload CL with test shortly.

### bu...@chromium.org (2015-04-02)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=193019

------------------------------------------------------------------
r193019 | kouhei@chromium.org | 2015-04-02T09:48:59.810800Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/loading/preload-ignore-invalid-base.html?r1=193019&r2=193018&pathrev=193019
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/parser/badurl-base-preloader-crash.html?r1=193019&r2=193018&pathrev=193019
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.cpp?r1=193019&r2=193018&pathrev=193019
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/loading/preload-ignore-invalid-base-expected.txt?r1=193019&r2=193018&pathrev=193019
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/loading/resources/fail.js?r1=193019&r2=193018&pathrev=193019
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/parser/HTMLPreloadScanner.cpp?r1=193019&r2=193018&pathrev=193019
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/parser/badurl-base-preloader-crash-expected.txt?r1=193019&r2=193018&pathrev=193019

HTMLPreloadScanner should only use valid <base> urls

Before this CL, HTMLPreloadScanner accepted invalid <base> urls and
used it to resolve urls encountered later in the scan.
This CL ensures that only valid urls specified in <base href> are
actually used as base urls.

BUG=471525

Review URL: https://codereview.chromium.org/1044133002
-----------------------------------------------------------------

### in...@chromium.org (2015-04-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-03)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-04)

ClusterFuzz has detected this issue as fixed in range 323578:323649.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6196559406956544

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x60c00022aa0e
Crash State:
  url::ParsePort
  blink::KURL::port
  blink::SecurityOrigin::SecurityOrigin
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=311376:311466
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=323578:323649

Minimized Testcase (0.05 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94CYigilCe3H9ot7OO0Ou3QBkF9A0OsY9szMVtjarWzksibcM7x8ZAdXd_fg3jdJ4Nm4i1bqsVK4LmsRJT4GpMMbvq9afRMyy9KlL-63xnQjT-ELfznGbvemIaBkXpQcjeTD1awjJV3wJnK_uh__uTngQ8MPA
<base href="gopher:��&#279%�:0"><script src=":">


Additional requirements: Requires HTTP

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@google.com (2015-04-08)

Based on revision number, this is already in M43.

### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-09)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-12-17)

This reporter isn't from Samsung as initially thought, so is eligible for consideration under the Chrome Reward Program: https://www.google.com/about/appsecurity/chrome-rewards/

### ti...@google.com (2016-04-22)

Congratulations - our reward panel decided to award you $1000 for this report.

Our finance team will be in touch in about 7 days to collect your payment details for this and other bugs. If that doesn't happen, please reach out to me via email or via this bug so that I can follow up for you.

### ti...@google.com (2016-04-25)

Adding in OP's new email address.

### ti...@google.com (2016-04-25)

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

This issue was migrated from crbug.com/chromium/471525?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081749)*
