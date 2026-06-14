# Heap-buffer-overflow in ps_table_add

| Field | Value |
|-------|-------|
| **Issue ID** | [40084275](https://issues.chromium.org/issues/40084275) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | bu...@chromium.org |
| **Created** | 2016-05-10 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4548226098659328

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 7
Crash Address: 0x61b000014f90
Crash State:
  ps_table_add
  parse_encoding
  parse_dict
  
Recommended Security Severity: Medium


Minimized Testcase (85.95 Kb): https://cluster-fuzz.appspot.com/download/AMIfv974Qq4DJnQhgEru8jsM7evXOlzFUSJOmzjhxQuOddFVxEazhqmQk4PFiclviwuSiKl9VInpYUmOr2wRo59_dfPQa0qPgdKkfURYxtyYmToQLSl689-xHbWenDQf1Qs3SYVQg36x3SrzrfJzRgrbvpgB216t_VtHnlngozPLVcKe0ChCz88

Filer: mmoroz

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### mm...@chromium.org (2016-05-10)

bungeman@, could we please update freetype?

Last time when we've discussed that we had a conclusion that it is not used in the Chromium (https://codereview.chromium.org/1776323002/).

But if I understand the crash correctly, it can be reached through pdfium and definitely worth to be updated.

### mm...@chromium.org (2016-05-10)

Setting PDFium component + adding ochang@ as an expert in pdfium stuff.

[Monorail components: Internals>Plugins>PDF]

### mm...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-10)

[Empty comment from Monorail migration]

### oc...@chromium.org (2016-05-10)

My understanding is that freetype is only shipped for Android (freetype-android). For other platforms, e.g. Linux, it is only used for testing and development, and never shipped in a production build (we link with system freetype).

Setting Impact to None.

### mm...@chromium.org (2016-05-10)

I agree. But why cannot we update freetype? Does an update require many resources to be done?

Or, asking this in another way: what is the reason to have _very_ old version of a library with a huge number of known vulnerabilities in the repo?

My position is:
A) if it isn't used at all, it should be removed
B) if it is used somewhere (tests, for example), it should be updated

May be I'm wrong. What do you think?

### oc...@chromium.org (2016-05-10)

For for pdfium at least, updating our bundled freetype (which is only used for testing/fuzzing) is a tedious task because it breaks our pixel tests due to slight font rendering differences.

I would assume that updating third_party/freetype2 has similar issues for other tests, and the effort required isn't worth the minor gains it has given that it is never shipped to actual users.

### oc...@chromium.org (2016-05-10)

(I could be wrong -- bungeman probably has a better answer to this).

### mm...@chromium.org (2016-05-24)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-05-27)

Discussed this offline. I'm going to mark this as Stable impacting rather than None. ExternalDependency is more appropriate.

### cl...@chromium.org (2016-07-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4519118002978816

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 13
Crash Address: 0x619000002714
Crash State:
  ps_table_add
  parse_encoding
  parse_dict
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=314095:314100

Minimized Testcase (59.11 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95JMpq0mL4_28rcvrBpsp2Y8b8tY_BW7ZDcuRvTOw5oRc0vMN1ttDu192ga9ImneQX0cn5EJn_gdoqsnuV48BshEmxGYLr8XTq8hp4SjgCeEPsp3hA93enNYmMv9ZPKeeuZtw1cIkeKidiIgHxNXDVztyi_gkDVUpJCV-1bRnGQ_K5IymQ?testcase_id=4519118002978816

Filer: mmoroz

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-07-31)

ClusterFuzz has detected this issue as fixed in range 408642:408661.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4548226098659328

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 7
Crash Address: 0x61b000014f90
Crash State:
  ps_table_add
  parse_encoding
  parse_dict
  
Recommended Security Severity: Medium

Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_media&range=408642:408661

Minimized Testcase (85.95 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94ySAYpjdXuytNTIWfvSupaihS8QFhuZUEtf9yqoFH7ONGGD9bHgR1JDv5c_oZeIAiKrvK07wHF8yiSQ2LjG2jw-4Gw3nZydCWPcJ3mCBV_o2KlCPjLY8SSSALh_OX7F4fHhUHq3tOkidCD0y4PnvHaKYNFBs1fLZn4METfvv9OTeqK3kc?testcase_id=4548226098659328

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-07-31)

ClusterFuzz has detected this issue as fixed in range 408633:408661.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4519118002978816

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 13
Crash Address: 0x619000002714
Crash State:
  ps_table_add
  parse_encoding
  parse_dict
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=314095:314100
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=408633:408661

Minimized Testcase (59.11 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95JMpq0mL4_28rcvrBpsp2Y8b8tY_BW7ZDcuRvTOw5oRc0vMN1ttDu192ga9ImneQX0cn5EJn_gdoqsnuV48BshEmxGYLr8XTq8hp4SjgCeEPsp3hA93enNYmMv9ZPKeeuZtw1cIkeKidiIgHxNXDVztyi_gkDVUpJCV-1bRnGQ_K5IymQ?testcase_id=4519118002978816

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-07-31)

ClusterFuzz testcase is verified as fixed, closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2016-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-08-03)

Your change meets the bar and is auto-approved for M53 (branch: 2785)

### go...@chromium.org (2016-08-04)

Is there anything to merge here? If not, please remove "Merge-Approved-53" label. Thank you.

### sh...@chromium.org (2016-08-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2016-08-08)

No, there's nothing to merge. I don't even know why this is an issue considering third_party/freetype2 isn't actually shipped.

### go...@chromium.org (2016-08-08)

Removing "Merge-Approved-53"label per https://crbug.com/chromium/610644#c21. Thank you.

### aw...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-26)

[Comment Deleted]

### aw...@chromium.org (2016-08-26)

Thanks as ever - $1,500 for this one.

### aw...@chromium.org (2016-08-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-11-06)

This issue was migrated from crbug.com/chromium/610644?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/594972]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084275)*
