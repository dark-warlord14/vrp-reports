# Use-of-uninitialized-value in blink::encodePixels

| Field | Value |
|-------|-------|
| **Issue ID** | [40083052](https://issues.chromium.org/issues/40083052) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Image |
| **Platforms** | Linux |
| **CVE IDs** | CVE-2016-1614 |
| **Reporter** | cl...@chromium.org |
| **Assignee** | xi...@chromium.org |
| **Created** | 2015-10-18 |
| **Bounty** | $2,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4554939064385536

Fuzzer: cdiehl_dharma
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::encodePixels
  blink::JPEGImageEncoder::encode
  blink::ImageDataBuffer::encodeImage
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=354036:354071

Minimized Testcase (0.21 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96NwXb5p8OM7rTejXFc0-TmKs-c-UFPTsBy_JIKpEcKsOcmE1-xwOF5EmBi4G1jbJK1j04Q0u1afIHDqnp78JFNGJzH_6rK_zTp6K3P3rNlGq1JRdfWvSsa_-IW9Sz6Lh3BRPzQRSmB2FLykG9mSSv1W42C3A

Filer: inferno

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### in...@chromium.org (2015-10-18)

Author: xidachen
Component: chromium
Changelist: https://chromium.googlesource.com/chromium/src//+/1db4c96ec3d12c0a121325d1b6e63ecd4bbf0ed8
Time: Wed Oct 14 18:05:08 2015
Lines 49-52 of file UnacceleratedImageBufferSurface.cpp which potentially caused crash are changed in this cl (frame #6, "blink::UnacceleratedImageBufferSurface::UnacceleratedImageBufferSurface").
Minimum distance from crash line to modified line: 0. (file: UnacceleratedImageBufferSurface.cpp, crashed on: 49, modified: 49).

### cl...@chromium.org (2015-10-19)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-10-19)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-10-19)

[Empty comment from Monorail migration]

### xi...@chromium.org (2015-10-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-19)

[Empty comment from Monorail migration]

### ju...@chromium.org (2015-10-19)

I think the problem here is with  HTMLCanvasElement::toImageData.  That function assume that ImageData::create will initialize the image data. What I think you should do is conditionally initialize in all the cases where the ImageData is not filled.
1) if there is no m_context, if taking the snapshot failed (in 2 places), or if the readPixels failed (in 2 places).

### bu...@chromium.org (2015-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1998d1cc5f2985cdeac94d3e669b0e7901a77bbb

commit 1998d1cc5f2985cdeac94d3e669b0e7901a77bbb
Author: jbroman <jbroman@chromium.org>
Date: Mon Oct 19 21:59:21 2015

ImageBitmap: Change two enum uses.

An earlier CL (https://codereview.chromium.org/1382883002/) made two changes
which seem to have unintended effects on behaviour.

1. The ImageBitmap constructor asserts that its data is opaque (whereas
previously it took the default NonOpaque opacity mode), but if this is so
it should have a comment justifying it.

2. UnacceleratedImageBufferSurface is clearings the SkSurface if it was
told _not_ to initialize image pixels, which seems like an inversion of the
intended condition.

BUG=543515,544691

Review URL: https://codereview.chromium.org/1407393002

Cr-Commit-Position: refs/heads/master@{#354880}

[modify] http://crrev.com/1998d1cc5f2985cdeac94d3e669b0e7901a77bbb/third_party/WebKit/Source/core/frame/ImageBitmap.cpp
[modify] http://crrev.com/1998d1cc5f2985cdeac94d3e669b0e7901a77bbb/third_party/WebKit/Source/platform/graphics/UnacceleratedImageBufferSurface.cpp


### oc...@chromium.org (2015-10-19)

Assuming fixed based on #8.

### cl...@chromium.org (2015-10-19)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-10-20)

ClusterFuzz has detected this issue as fixed in range 354812:354905.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4554939064385536

Fuzzer: cdiehl_dharma
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::encodePixels
  blink::JPEGImageEncoder::encode
  blink::ImageDataBuffer::encodeImage
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=354036:354071
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=354812:354905

Minimized Testcase (0.21 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96NwXb5p8OM7rTejXFc0-TmKs-c-UFPTsBy_JIKpEcKsOcmE1-xwOF5EmBi4G1jbJK1j04Q0u1afIHDqnp78JFNGJzH_6rK_zTp6K3P3rNlGq1JRdfWvSsa_-IW9Sz6Lh3BRPzQRSmB2FLykG9mSSv1W42C3A

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ti...@google.com (2015-11-28)

Tagging for trunk roll with M48 (MSan bug + heavily used codepath) - shout out if you want to nominate for an M47 patch as it is a tiny change.

### ti...@google.com (2016-01-20)

Congrats - $2000 for this report ($1500 for the report + $500 clusterfuzz bonus). I'll start the payment process next week. CVE ID coming shortly.

### ti...@google.com (2016-01-20)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

CVE-2016-1614

### cl...@chromium.org (2016-01-26)

Bulk update: removing view restriction from closed bugs.

### [Deleted User] (2016-02-18)

[Comment Deleted]

### in...@chromium.org (2016-02-18)

Tim, can you comment on the payment process for this.

### ti...@google.com (2016-02-18)

Hmm... I'll look into it. Did you receive any of the usual emails about payment/POs?
I'll email you off this thread to follow up.

### [Deleted User] (2016-02-18)

[Comment Deleted]

### ti...@google.com (2016-03-12)

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

This issue was migrated from crbug.com/chromium/544691?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083052)*
