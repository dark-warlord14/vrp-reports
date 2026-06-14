# Heap-use-after-free in SkOpSegment::addT

| Field | Value |
|-------|-------|
| **Issue ID** | [40080229](https://issues.chromium.org/issues/40080229) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | fm...@chromium.org |
| **Created** | 2014-08-20 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4972996906188800

Fuzzer: Attekett_surku_fuzzer
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x04513d80
Crash State:
  SkOpSegment::addT
  SkOpSegment::addTPair
  SkOpSegment::addCancelOutsides
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=287661:287842

Minimized Testcase (1.13 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97x6XRIjP0GNDZZig7XAl7AlWO92pdj4juzp2LapRa9P8HwoZDk6v8emzpYQbsbj7dZpFqJcRZNuq_ZsAPkmd5UtBW184gWUEGHCN1nxGeo0LT3jMslHjJIF4auN7-3fU9OG0MwpKMSqCr5S4y1O_TQiTlPpg
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<clipPath id="orez">
  <path transform="translate(-100,-96)"
	 d="M172.5,96h-34.9c0-18.8-12.8-34.6-30.1-39.2l9-33.7
	 c-6.3-1.7-12.9-2.6-19.5-2.6v34.9h0c-18.8,0-34.6,12.8-39.2,
	 30.1l-33.7-9c-1.7,6.3-2.6,12.9-2.6,19.5h34.9v0c0,
	 109.2,172.5,102.7,172.5,96z" />
  <path transform="translate(-100,-96)"
	d="M172.5,96h-34.9c0-15-8.2-28.1-20.3-35.1l17.5-30.2
  c-11.1-6.4-24-10.1-37.7-10.1v34.9c-15,0-28.1,
  8.2-35.1,20.3L31.6,58.3c-6.4,
  11.1-10.1,24-10.1,37.7h34.9c0,15,8.2,28.1,20.3,35.1
			147.3,161.2,141.7,161.2,136z"></path>
  <path transform="translate(-100,-136)"
	 d="M161.2,136h-29.7c0-16-10.8-29.4-25.6-33.3l7.7-28.7
		  c-5.4-1.4-10.9-2.2-16.6-2.2v29.7h0
			c-16,0-29.4,10.8-33.3,25.6L35,119.4
			147.3,161.2,141.7,161.2,136z"></path>
  <path transform="translate(-100,-136)"
	 d="M161.2,136h-29.7c0-16-10.8-29.4-25.6-33.3l7.7-28.7
		  c-5.4-1.4-10.9-2.2-16.6-2.2v29.7h0
			c-16,0-29.4,10.8-33.3,25.6L35,119.4
			147.3,161.2,141.7,161.2,136z">
	</path>
  </clipPath>
</defs>

<image clip-path="url(#orez)" width="200" height="200" xlink:href="a10.jpg">


Filer: inferno

## Timeline

### in...@chromium.org (2014-08-20)

maybe regression from http://src.chromium.org/viewvc/blink?view=rev&revision=179529

### pd...@chromium.org (2014-08-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-20)

[Empty comment from Monorail migration]

### ca...@google.com (2014-08-20)

skia-side fix is here: https://codereview.chromium.org/489853002/

### cl...@chromium.org (2014-08-20)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### fm...@chromium.org (2014-08-20)

Thanks Cary.

### cl...@chromium.org (2014-08-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-21)

ClusterFuzz has detected this issue as fixed in range 290818:290912.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4972996906188800

Fuzzer: Attekett_surku_fuzzer
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x04513d80
Crash State:
  SkOpSegment::addT
  SkOpSegment::addTPair
  SkOpSegment::addCancelOutsides
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=287661:287842
Fixed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=290818:290912

Minimized Testcase (1.13 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97x6XRIjP0GNDZZig7XAl7AlWO92pdj4juzp2LapRa9P8HwoZDk6v8emzpYQbsbj7dZpFqJcRZNuq_ZsAPkmd5UtBW184gWUEGHCN1nxGeo0LT3jMslHjJIF4auN7-3fU9OG0MwpKMSqCr5S4y1O_TQiTlPpg
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs>
<clipPath id="orez">
  <path transform="translate(-100,-96)"
	 d="M172.5,96h-34.9c0-18.8-12.8-34.6-30.1-39.2l9-33.7
	 c-6.3-1.7-12.9-2.6-19.5-2.6v34.9h0c-18.8,0-34.6,12.8-39.2,
	 30.1l-33.7-9c-1.7,6.3-2.6,12.9-2.6,19.5h34.9v0c0,
	 109.2,172.5,102.7,172.5,96z" />
  <path transform="translate(-100,-96)"
	d="M172.5,96h-34.9c0-15-8.2-28.1-20.3-35.1l17.5-30.2
  c-11.1-6.4-24-10.1-37.7-10.1v34.9c-15,0-28.1,
  8.2-35.1,20.3L31.6,58.3c-6.4,
  11.1-10.1,24-10.1,37.7h34.9c0,15,8.2,28.1,20.3,35.1
			147.3,161.2,141.7,161.2,136z"></path>
  <path transform="translate(-100,-136)"
	 d="M161.2,136h-29.7c0-16-10.8-29.4-25.6-33.3l7.7-28.7
		  c-5.4-1.4-10.9-2.2-16.6-2.2v29.7h0
			c-16,0-29.4,10.8-33.3,25.6L35,119.4
			147.3,161.2,141.7,161.2,136z"></path>
  <path transform="translate(-100,-136)"
	 d="M161.2,136h-29.7c0-16-10.8-29.4-25.6-33.3l7.7-28.7
		  c-5.4-1.4-10.9-2.2-16.6-2.2v29.7h0
			c-16,0-29.4,10.8-33.3,25.6L35,119.4
			147.3,161.2,141.7,161.2,136z">
	</path>
  </clipPath>
</defs>

<image clip-path="url(#orez)" width="200" height="200" xlink:href="a10.jpg">

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### mb...@chromium.org (2014-11-17)

Thanks again for the fuzzer contribution! This one qualified for a $1000 reward.

### cl...@chromium.org (2014-11-26)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-08)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/405417?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080229)*
