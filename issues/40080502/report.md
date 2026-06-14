# Use-of-uninitialized-value in SkOpSegment::addTCoincident

| Field | Value |
|-------|-------|
| **Issue ID** | [40080502](https://issues.chromium.org/issues/40080502) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ca...@chromium.org |
| **Created** | 2014-09-19 |
| **Bounty** | $2,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6329355903959040

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  SkOpSegment::addTCoincident
  SkOpContour::calcCoincidentWinding
  CoincidenceCheck
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=287661:287842

Minimized Testcase (0.77 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96tAQvajZkrVOoMU3Og1hgetG-kaI-odzo4zpxJQBtqHGGatPQQiP4RBqx1ROGtGfpu9N703ecLWi54tCzRwjyBdr5B8_-_iMvlwTtVNsWdgQl8G4PHKrPbAzIzggLEuKlDlXrsmC7CaSHYKthB_SqFJP8Ucw
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<title></title>
<desc>
</desc>
<defs>
<clipPath id="orez">
<path d="M172.5,96h-34.9c0-18.8-12.8-34.6-30.1-39.2l9-33.7
	 c-6.3-1.7-12.9-2.6-19.5-2.6v34.9h0c-18.8,0-34.6,12.8-39.2,
	 30.1l-33.7-9c-1.7,6.3-2.6,12.9-2.6,19.5h34.9v0c0,
	 109.2,172.5,102.7,172.5,96z" />
  <path	d="M172.5,96h-34.9c0-15-8.2-28.1-20.3-35.1l17.5-30.2
  c-11.1-6.4-24-10.1-37.7-10.1v34.9c-15,0-28.1,
  8.2-35.1,20.3L31.6,58.3c-6.4,
  11.1-10.1,24-10.1,37.7h34.9c0,15,8.2,28.1,20.3,35.1
			c-16,0-29.4,10.8-33.3,25.6L333333333333333333333333333335,119.4
			29.4-10.8,33.3-25.6l28.7,7.7C160.4,
			147.3,161.2,141.7,161.2,136z">
  </path>
</clipPath>
</defs>

<image clip-path="url(#orez)" width="200" height="200" xlink:href="a10.jpg">




Filer: inferno

## Timeline

### in...@chromium.org (2014-09-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-19)

[Empty comment from Monorail migration]

### ca...@chromium.org (2014-09-19)

Proposed fix checked into Skia as

https://skia.googlesource.com/skia/+/630240d18805faf81d8e75172496ad165c2226b2

### jw...@chromium.org (2014-09-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-21)

ClusterFuzz has detected this issue as fixed in range 295711:295724.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6329355903959040

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  SkOpSegment::addTCoincident
  SkOpContour::calcCoincidentWinding
  CoincidenceCheck
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=287661:287842
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=295711:295724

Minimized Testcase (0.77 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96tAQvajZkrVOoMU3Og1hgetG-kaI-odzo4zpxJQBtqHGGatPQQiP4RBqx1ROGtGfpu9N703ecLWi54tCzRwjyBdr5B8_-_iMvlwTtVNsWdgQl8G4PHKrPbAzIzggLEuKlDlXrsmC7CaSHYKthB_SqFJP8Ucw
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<title></title>
<desc>
</desc>
<defs>
<clipPath id="orez">
<path d="M172.5,96h-34.9c0-18.8-12.8-34.6-30.1-39.2l9-33.7
	 c-6.3-1.7-12.9-2.6-19.5-2.6v34.9h0c-18.8,0-34.6,12.8-39.2,
	 30.1l-33.7-9c-1.7,6.3-2.6,12.9-2.6,19.5h34.9v0c0,
	 109.2,172.5,102.7,172.5,96z" />
  <path	d="M172.5,96h-34.9c0-15-8.2-28.1-20.3-35.1l17.5-30.2
  c-11.1-6.4-24-10.1-37.7-10.1v34.9c-15,0-28.1,
  8.2-35.1,20.3L31.6,58.3c-6.4,
  11.1-10.1,24-10.1,37.7h34.9c0,15,8.2,28.1,20.3,35.1
			c-16,0-29.4,10.8-33.3,25.6L333333333333333333333333333335,119.4
			29.4-10.8,33.3-25.6l28.7,7.7C160.4,
			147.3,161.2,141.7,161.2,136z">
  </path>
</clipPath>
</defs>

<image clip-path="url(#orez)" width="200" height="200" xlink:href="a10.jpg">

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ca...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-22)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ca...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### hc...@chromium.org (2014-09-22)

Cary, looking into this, it doesn't appear to have come up in the crash reports on 37, only 38 and later, so the only cherry pick we need is to the Skia M38 branch.

### ca...@chromium.org (2014-09-22)

merged into skia/chrome/m38_2125

### [Deleted User] (2014-09-22)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-24)

Marking as merge-merged based on c#10

### ti...@chromium.org (2014-10-07)

$2000 for this report ($1500 for the bug, $500 ClusterFuzz bonus).  

### ti...@google.com (2014-12-08)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-12-29)

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

This issue was migrated from crbug.com/chromium/415866?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080502)*
