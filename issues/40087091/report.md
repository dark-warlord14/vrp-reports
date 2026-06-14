# Heap-use-after-free in cr_png_set_longjmp_fn

| Field | Value |
|-------|-------|
| **Issue ID** | [40087091](https://issues.chromium.org/issues/40087091) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Images>Codecs |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | [Deleted User] |
| **Created** | 2017-03-18 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://clusterfuzz.com/testcase?key=5061179409170432

Fuzzer: cdiehl_peach
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61a000003150
Crash State:
  cr_png_set_longjmp_fn
  blink::PNGImageDecoder::headerAvailable
  blink::PNGImageReader::parseSize
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=456626:457730

Reproducer Testcase: https://clusterfuzz.com/download/AMIfv941s6DoQsVYeUxAf6q_3Xct1V9AiHyHiw1aXYJivVStXvanuekf_5d2POW79I_CRr4qEdUFRAV8uGtv0lHixEaWJjR2rqMkk3cWMAPckuQKPH85S0VnUtvv2ZmBYKdDMPHEX_kmuvEc1dRBbYAaOC_pdhVWyBV70nN2GUFmQ9SqKTLDdMQZNVOd1mjYYqpDOZKQnw6eqA8p54i8v7ydd6CWMSSKNEYZYvVKo9IBHM639xYCxfjWCN7VP7DD40L2dIoI9IUts3j8pBVQuOy6GLhJBJ6pSEHgloc-2pt2aH5dd4UAEd1vDd6V5KNZI35OqvfeCySYBOWO0Zp7G_r8JX4fb03dcwesF_ww8AJcrzQSaiQqt2-QWZ-qVZej_653ytsU6db4VuVLPmCv6zpcHIYT7tms-w?testcase_id=5061179409170432


Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### sh...@chromium.org (2017-03-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-19)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-03-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-03-20)

scroggo - although out of range, it looks like you made a change recently in PNG image decoders.  Could you please take a look or re-assign as appropriate?  Thanks

### ts...@chromium.org (2017-03-20)

[Empty comment from Monorail migration]

[Monorail components: Blink>Image]

### [Deleted User] (2017-03-22)

The range is incorrect - this is in fact due to my CL https://codereview.chromium.org/2618633004, so you assigned this to the right person.

The problem occurs when PNGImageDecoder::headerAvailable calls ImageDecoder::setSize. The latter calls setFailed, which, as of my CL, now deletes the PNGImageReader holding the pngstructp. When we try to dereference it, it is no longer valid.

My earlier patchsets had a similar problem with initFrameBuffer, which I fixed before submitting. In that case, I updated initFrameBuffer to stop calling setFailed, and the callers to call setFailed themselves.

I see three possible solutions:

A) Make setSize no longer call setFailed, similar to the approach of initFrameBuffer
B) Make setFailed not delete the reader. This would be different from the other decoder implementations (ICO, GIF, and BMP), and it would mean that we don't free up memory that we could have.
C) Not attempt to call longjmp when setSize fails. In theory, this would be problematic because headerAvailable is (sometimes) called from within libpng, so libpng would continue to operate (and presumably dereference the png_structp later). In practice, setSize is only called when headerAvailable is called directly by the PNGImageReader. Maybe a refactor here makes sense.

[Monorail components: -Blink>Image Internals>Images>Codecs]

### [Deleted User] (2017-03-22)

A fix is at https://codereview.chromium.org/2766263002, which takes approach (C), including a refactor. It likely *also* makes sense to do (A), to be consistent with initFrameBuffer and more resilient to future changes, but as I explored (C) it seemed like a good refactor whether we do (A) or not.

### [Deleted User] (2017-03-22)

More thoughts on this:
(A) looks to be a bigger refactor, and perhaps not necessary. We could easily make the base class implementation not call setFailed, but the callers still call setFailed from within objects that get deleted by it. These are safe, though, because they exit without trying to access deleted objects.

### bu...@chromium.org (2017-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fab1444fe6528ac403acf28945492f001f3d932e

commit fab1444fe6528ac403acf28945492f001f3d932e
Author: scroggo <scroggo@chromium.org>
Date: Thu Mar 23 14:17:08 2017

Refactor PNGImageDecoder's call to setSize

In the existing code, if setSize fails, PNGImageDecoder attempts to
dereference the png_structp owned by m_reader. But setSize calls
setFailed on failure, deleting m_reader in the process.

As it turns out, it is unnecessary to dereference the png_structp in
this case anyway. The intent is to call longjmp in order to stop
libpng's processing, but this block of code is only executed when this
method is called directly by m_reader, so no need to longjmp.

This method, headerAvailable, is called for each frame of a PNG, but
the setup code (e.g. setSize) only needs to be done once for the entire
image. Separate the pieces that only need to be done once from
headerAvailable. This makes it more clear that there is no need to
longjmp; use a boolean return instead. Now if setSize fails, no part
of m_reader will be accessed.

Move the extra size check into a new override of setSize, and move the
color space setup code to its own method.

Add a test image that reports a size that is too big for
ImageDecoder::setSize. Attempting to decode the size should fail.

BUG=702934

Review-Url: https://codereview.chromium.org/2766263002
Cr-Commit-Position: refs/heads/master@{#459074}

[add] https://crrev.com/fab1444fe6528ac403acf28945492f001f3d932e/third_party/WebKit/LayoutTests/images/resources/crbug702934.png
[modify] https://crrev.com/fab1444fe6528ac403acf28945492f001f3d932e/third_party/WebKit/Source/platform/image-decoders/png/PNGImageDecoder.cpp
[modify] https://crrev.com/fab1444fe6528ac403acf28945492f001f3d932e/third_party/WebKit/Source/platform/image-decoders/png/PNGImageDecoder.h
[modify] https://crrev.com/fab1444fe6528ac403acf28945492f001f3d932e/third_party/WebKit/Source/platform/image-decoders/png/PNGImageDecoderTest.cpp
[modify] https://crrev.com/fab1444fe6528ac403acf28945492f001f3d932e/third_party/WebKit/Source/platform/image-decoders/png/PNGImageReader.cpp


### [Deleted User] (2017-03-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-03-24)

ClusterFuzz has detected this issue as fixed in range 459063:459096.

Detailed report: https://clusterfuzz.com/testcase?key=5061179409170432

Fuzzer: cdiehl_peach
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61a000003150
Crash State:
  cr_png_set_longjmp_fn
  blink::PNGImageDecoder::headerAvailable
  blink::PNGImageReader::parseSize
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=456626:457730
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=459063:459096

Reproducer Testcase: https://clusterfuzz.com/download/AMIfv941s6DoQsVYeUxAf6q_3Xct1V9AiHyHiw1aXYJivVStXvanuekf_5d2POW79I_CRr4qEdUFRAV8uGtv0lHixEaWJjR2rqMkk3cWMAPckuQKPH85S0VnUtvv2ZmBYKdDMPHEX_kmuvEc1dRBbYAaOC_pdhVWyBV70nN2GUFmQ9SqKTLDdMQZNVOd1mjYYqpDOZKQnw6eqA8p54i8v7ydd6CWMSSKNEYZYvVKo9IBHM639xYCxfjWCN7VP7DD40L2dIoI9IUts3j8pBVQuOy6GLhJBJ6pSEHgloc-2pt2aH5dd4UAEd1vDd6V5KNZI35OqvfeCySYBOWO0Zp7G_r8JX4fb03dcwesF_ww8AJcrzQSaiQqt2-QWZ-qVZej_653ytsU6db4VuVLPmCv6zpcHIYT7tms-w?testcase_id=5061179409170432


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2017-03-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-31)

Groovy! The panel decided to award $3,000 for this bug, plus the $500 clusterfuzz bonus.  Cheers!

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-06-30)

This issue was migrated from crbug.com/chromium/702934?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087091)*
