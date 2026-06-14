# Heap-double-free in j2k_read_ppm_v3

| Field | Value |
|-------|-------|
| **Issue ID** | [40081393](https://issues.chromium.org/issues/40081393) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ha...@hboeck.de |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-02-11 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.35 Safari/537.36

Steps to reproduce the problem:
1. Attached file will expose a double free in pdfium.

Will attach address sanitizer output.


## Attachments

- [doublefree.pdf.asan.txt](attachments/doublefree.pdf.asan.txt) (text/plain, 4.4 KB)
- [doublefree.pdf](attachments/doublefree.pdf) (application/pdf, 350 B)

## Timeline

### ha...@hboeck.de (2015-02-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-11)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5702547801636864

### js...@chromium.org (2015-02-11)

This one isn't reproducing. What version were you testing against?

### ha...@hboeck.de (2015-02-11)

I reproduced it with the pre-built asan package from here:
https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-symbolized-linux-release-315577.zip?generation=1423603643978000&alt=media

That's the version from yesterday. (the crash dump came from a version I built myself a while ago, but I always re-test against a recent pre-built version)

### js...@chromium.org (2015-02-11)

Any special requirements? Did you have to give it a long timeout? Was it in 64-bit ASAN, etc?

### cl...@chromium.org (2015-02-12)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5703056486825984

### cl...@chromium.org (2015-02-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5703056486825984

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-double-free
Crash Address: 0x6090000093e0
Crash State:
  j2k_read_ppm_v3
  opj_j2k_read_header_procedure
  opj_j2k_read_header
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=289356:289512

Minimized Testcase (0.34 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96_bE1jGv895QtSnW3Y7ToJc5o4TJyifX5PNYwqM0IaON7dru17L-WgmbLJzaC_Rwt6qyRQV7hCy89yCHIqzQ1Q2p4Kd_5260iWSNnUDjFdHAj0kPRqXA0CkU1xcIJVnvCUcQ4VQp9P1fyyG_Ucr3pzYcfzKw



### ha...@hboeck.de (2015-02-12)

Don't know if you still have an issue (latest clusterfuzz message indicates it's reproduced now), but this was on 64 bit linux, with asan enabled (using the pre-built asan packages), reproducible with running the attached pdf through pdfium_test

### js...@chromium.org (2015-02-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-25)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ju...@foxitsoftware.com (2015-02-26)

It's pending in https://codereview.chromium.org/960183004/.

### ju...@foxitsoftware.com (2015-02-27)

Fixed in https://pdfium.googlesource.com/pdfium/+/ec61a859344dc6d2a60e4cbcd1555e6d317f2add.

### cl...@chromium.org (2015-02-27)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-03-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-16)

Merge requested for M42.

### am...@google.com (2015-03-16)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### am...@chromium.org (2015-03-17)

merge approved for m42

### cl...@chromium.org (2015-03-21)

ClusterFuzz has detected this issue as fixed in range 321566:321633.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5703056486825984

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: Heap-double-free
Crash Address: 0x6090000093e0
Crash State:
  j2k_read_ppm_v3
  opj_j2k_read_header_procedure
  opj_j2k_read_header
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=289356:289512
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=321566:321633

Minimized Testcase (0.34 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96_bE1jGv895QtSnW3Y7ToJc5o4TJyifX5PNYwqM0IaON7dru17L-WgmbLJzaC_Rwt6qyRQV7hCy89yCHIqzQ1Q2p4Kd_5260iWSNnUDjFdHAj0kPRqXA0CkU1xcIJVnvCUcQ4VQp9P1fyyG_Ucr3pzYcfzKw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@google.com (2015-03-26)

@jun_fang: Please merge your fix to M42 (branch 2311).

### ju...@foxitsoftware.com (2015-03-27)

It has been merged.

### ti...@google.com (2015-03-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2015-03-31)

Marking as merged per c#23.

### th...@chromium.org (2015-03-31)

We still need to roll DEPS on the branch to pick up the merge. I'll do it today when I merge + roll DEPS for https://crbug.com/chromium/465322.

### bu...@chromium.org (2015-03-31)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=71114

------------------------------------------------------------------
r71114 | thestig@google.com | 2015-03-31T20:09:45.036236Z

-----------------------------------------------------------------

### ti...@google.com (2015-04-09)

Congratulations - $2000 for this report.

Notes from reward panel: "Doesn't look like there's control between use and free"

Someone from our finance team should be in contact in the next two weeks to arrange payment.

Thanks again for your report!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-05)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/457493?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081393)*
