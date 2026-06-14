# Crash in content::RendererClipboardWriteContext::WriteBitmapFromPixels

| Field | Value |
|-------|-------|
| **Issue ID** | [40079486](https://issues.chromium.org/issues/40079486) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ur...@chromium.org |
| **Created** | 2014-05-02 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6418992455483392

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_media

Crash Type: UNKNOWN
Crash Address: 0x000000010670
Crash State:
  - crash stack -
  libc.so.6
  content::RendererClipboardWriteContext::WriteBitmapFromPixels
  content::WebClipboardImpl::writeImage
  

Minimized Testcase (8.42 Kb): https://cluster-fuzz.appspot.com/download/AMIfv946zCVlEcVXRJUQQJwyvMTypvJ5GJ5vdpc7pz7RS5EYe1BiQAwqQsM_oY3lJAnbRv17UQdVCtGm1KRm1IMGKoZ6qZxid4KYZaAoIG4qvoxJp0uPGQb5ODRbF0ikGMBmocLTNUaZD2JE0Y5q0peC14rVYDR0pg

Additional requirements: Requires Interaction Gestures


-----

Repro:
Open this (bad) image in Chrome:
https://cluster-fuzz.appspot.com/download/AMIfv946zCVlEcVXRJUQQJwyvMTypvJ5GJ5vdpc7pz7RS5EYe1BiQAwqQsM_oY3lJAnbRv17UQdVCtGm1KRm1IMGKoZ6qZxid4KYZaAoIG4qvoxJp0uPGQb5ODRbF0ikGMBmocLTNUaZD2JE0Y5q0peC14rVYDR0pg
Then right-click (on empty space where image would have been displayed) -> "Copy image" -> Crash.

Why does this happen?
Somehow, the renderer clipboard gets an SkBitmap with valid width & height -- but NULL pixels.

And why does that happen?
My guess is that, image decoder was able to get width/height from the image file (and so, you can see "(150 x 112)" in the page title), but decode failed somewhere down-the-line when decoding pixels.

## Timeline

### cl...@chromium.org (2014-05-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6418992455483392

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_media

Crash Type: UNKNOWN
Crash Address: 0x000000010670
Crash State:
  - crash stack -
  libc.so.6
  content::RendererClipboardWriteContext::WriteBitmapFromPixels
  content::WebClipboardImpl::writeImage
  

Minimized Testcase (8.42 Kb): https://cluster-fuzz.appspot.com/download/AMIfv946zCVlEcVXRJUQQJwyvMTypvJ5GJ5vdpc7pz7RS5EYe1BiQAwqQsM_oY3lJAnbRv17UQdVCtGm1KRm1IMGKoZ6qZxid4KYZaAoIG4qvoxJp0uPGQb5ODRbF0ikGMBmocLTNUaZD2JE0Y5q0peC14rVYDR0pg

Additional requirements: Requires Interaction Gestures

### in...@chromium.org (2014-05-02)

Clipboard and memcpy :( yikes :(

void RendererClipboardWriteContext::WriteBitmapFromPixels(
    ui::Clipboard::ObjectMap* objects,
    const void* pixels,
    const gfx::Size& size) {
.......
  memcpy(shared_buf_->memory(), pixels, buf_size);

### dc...@chromium.org (2014-05-02)

|pixels| is null. |pixels| should never be null.

### dc...@chromium.org (2014-05-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-05-04)

ClusterFuzz has detected this issue as fixed in latest custom build.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6418992455483392

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_media

Crash Type: UNKNOWN
Crash Address: 0x000000010670
Crash State:
  - crash stack -
  libc.so.6
  content::RendererClipboardWriteContext::WriteBitmapFromPixels
  content::WebClipboardImpl::writeImage
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv946zCVlEcVXRJUQQJwyvMTypvJ5GJ5vdpc7pz7RS5EYe1BiQAwqQsM_oY3lJAnbRv17UQdVCtGm1KRm1IMGKoZ6qZxid4KYZaAoIG4qvoxJp0uPGQb5ODRbF0ikGMBmocLTNUaZD2JE0Y5q0peC14rVYDR0pg

Additional requirements: Requires Interaction Gestures

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### dc...@chromium.org (2014-05-05)

This is still crashing.

Alpha, would you be able to find an owner for this? I'm not sure why the returned SkBitmap is bogus, since I'm not familiar at all with the image decoding pipeline.

### cl...@chromium.org (2014-05-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4646148134404096

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000000003f0
Crash State:
  - crash stack -
  libc.so.6
  content::RendererClipboardWriteContext::WriteBitmapFromPixels
  content::WebClipboardImpl::writeImage
  
Regressed: https://cluster-fuzz.appspot.com//revisions?job=linux_asan_chrome_mp&range=266423:266861

Minimized Testcase (0.70 Kb): https://cluster-fuzz.appspot.com/download/AMIfv968rtCCWwDLhzSUpDfrzMv7HRFvpbc4PIc4LzjN85iU6f9WFgYLSYMlxWM_aRDuX2Z8D7xv3oQ4l1YnnXEEHjixN6SvNprq-CQoFAHg85iM9Je2j13lstKPe1k9gnqrRGqL3u3Apc4vZ4zbC-bJfZ800RiD8Q

Additional requirements: Requires Interaction Gestures



### in...@chromium.org (2014-05-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-05-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-05-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-05-13)

looks like overflow in 4 * size.width() * size.height();

50	piman@chromium.org	111097	    return;
51	 	 	
52	 	 	  uint32 buf_size = 4 * size.width() * size.height();
53	 	 	
54	 	 	  // Allocate a shared memory buffer to hold the bitmap bits.
55	 	 	  shared_buf_.reset(ChildThread::current()->AllocateSharedMemory(buf_size));
56	erg@chromium.org	194608	  if (!shared_buf_)
57	piman@chromium.org	111097	    return;
58	 	 	
59	 	 	  // Copy the bits into shared memory
60	 	 	  DCHECK(shared_buf_->memory());
61	 	 	  memcpy(shared_buf_->memory(), pixels, buf_size);

### cl...@chromium.org (2014-05-13)

[Empty comment from Monorail migration]

### pi...@chromium.org (2014-05-14)

r111097 only moved the code...

It's not the overflow, the size comes out as 16x16x4.
The problem is that, as noted in #2, pixels is NULL (which also means, it's not a High security issue).

Anyway, I got https://codereview.chromium.org/289573002 which fixes the overflow, and works around NULL pixels as well as non-32-bits bitmaps (which would OOB read).

### in...@chromium.org (2014-05-14)

Changing severity based on last comment "on-32-bits bitmaps (which would OOB read)."

### dc...@chromium.org (2014-05-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e4be88bde4a9b1f0d9a56bfc68447e0105657457

commit e4be88bde4a9b1f0d9a56bfc68447e0105657457
Author: piman@chromium.org <piman@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Tue May 20 19:26:31 2014

Workaround bad bitmaps in clibpoard code

- Some bitmaps end up with a NULL getPixels(). Don't try to copy ot of that.
- Only try to copy 32-bit bitmaps
- Protect against overflow in size computation

BUG=369621

Review URL: https://codereview.chromium.org/289573002

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@271730 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-05-20)

------------------------------------------------------------------
r271730 | piman@chromium.org | 2014-05-20T19:26:31.200851Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/webclipboard_impl.cc?r1=271730&r2=271729&pathrev=271730
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/renderer_clipboard_client.cc?r1=271730&r2=271729&pathrev=271730

Workaround bad bitmaps in clibpoard code

- Some bitmaps end up with a NULL getPixels(). Don't try to copy ot of that.
- Only try to copy 32-bit bitmaps
- Protect against overflow in size computation

BUG=369621

Review URL: https://codereview.chromium.org/289573002
-----------------------------------------------------------------

### pi...@chromium.org (2014-05-20)

Not sure how far back we want to merge. Turns out non-32 bit bitmaps apparently can't happen so that's not a concern. Overflow could happen if we can have a large bitmap whose size doesn't fit in 32 bits, but I'm not sure if that's actually possible.

### cl...@chromium.org (2014-05-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-05-22)

piman@ - as this is an externally-reported medium severity bug, I'd like to at least get this into M36/beta. Any issues with merging this to M36/beta?

### dc...@chromium.org (2014-05-22)

Removing the fixed flag, because the underlying issue (some webp images cause Image::nativeImageForCurrentFrame to return a SkBitmap with NULL pixels) hasn't been fixed yet.

Handing this off to urvang@ per hclam@'s suggestion.

We should merge piman@'s patch though.

### [Deleted User] (2014-05-22)

Adding reveman as well. reveman: Is this the OOM issue you mentioned?


### pi...@chromium.org (2014-05-22)

[Empty comment from Monorail migration]

### [Deleted User] (2014-05-22)

[Empty comment from Monorail migration]

### [Deleted User] (2014-05-22)

Approved only for 36.

### pi...@chromium.org (2014-05-22)

Merged to 36 as r272325.
Re-requesting merge for 35.

### bu...@chromium.org (2014-05-22)

------------------------------------------------------------------
r272325 | piman@chromium.org | 2014-05-22T21:32:58.131155Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/content/renderer/webclipboard_impl.cc?r1=272325&r2=272324&pathrev=272325
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/content/renderer/renderer_clipboard_client.cc?r1=272325&r2=272324&pathrev=272325

Merge 271730 "Workaround bad bitmaps in clibpoard code"

> Workaround bad bitmaps in clibpoard code
> 
> - Some bitmaps end up with a NULL getPixels(). Don't try to copy ot of that.
> - Only try to copy 32-bit bitmaps
> - Protect against overflow in size computation
> 
> BUG=369621
> 
> Review URL: https://codereview.chromium.org/289573002

TBR=piman@chromium.org

Review URL: https://codereview.chromium.org/287363006
-----------------------------------------------------------------

### bu...@chromium.org (2014-05-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0a93504a2fadc7f4ce5aaa1feca219c2799dd2ee

commit 0a93504a2fadc7f4ce5aaa1feca219c2799dd2ee
Author: piman@chromium.org <piman@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Thu May 22 21:32:58 2014

Merge 271730 "Workaround bad bitmaps in clibpoard code"

> Workaround bad bitmaps in clibpoard code
> 
> - Some bitmaps end up with a NULL getPixels(). Don't try to copy ot of that.
> - Only try to copy 32-bit bitmaps
> - Protect against overflow in size computation
> 
> BUG=369621
> 
> Review URL: https://codereview.chromium.org/289573002

TBR=piman@chromium.org

Review URL: https://codereview.chromium.org/287363006

git-svn-id: svn://svn.chromium.org/chrome/branches/1985/src@272325 0039d316-1c4b-4281-b951-d872f2087c98



### ur...@chromium.org (2014-05-22)

+WebP folks, FYI

Discussed offline with dcheng@ on this, and here's my preliminary understanding.

Repro:
Open this (bad) image in Chrome:
https://cluster-fuzz.appspot.com/download/AMIfv946zCVlEcVXRJUQQJwyvMTypvJ5GJ5vdpc7pz7RS5EYe1BiQAwqQsM_oY3lJAnbRv17UQdVCtGm1KRm1IMGKoZ6qZxid4KYZaAoIG4qvoxJp0uPGQb5ODRbF0ikGMBmocLTNUaZD2JE0Y5q0peC14rVYDR0pg
Then right-click (on empty space where image would have been displayed) -> "Copy image" -> Crash.

Why does this happen?
Somehow, the renderer clipboard gets an SkBitmap with valid width & height -- but NULL pixels.

And why does that happen?
My guess is that, image decoder was able to get width/height from the image file (and so, you can see "(150 x 112)" in the page title), but decode failed somewhere down-the-line when decoding pixels.

Ideally, once the image decoding has been marked as failed, it's SkBitmap should not have valid width/height.

Let me try to see if this is something specific to WebP, or can happen with other image formats to.

### cl...@chromium.org (2014-05-25)

ClusterFuzz has detected this issue as fixed in range 271393:271739.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4646148134404096

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x0000000003f0
Crash State:
  - crash stack -
  libc.so.6
  content::RendererClipboardWriteContext::WriteBitmapFromPixels
  content::WebClipboardImpl::writeImage
  
Regressed: https://cluster-fuzz.appspot.com//revisions?job=linux_asan_chrome_mp&range=266423:266861
Fixed: https://cluster-fuzz.appspot.com//revisions?job=linux_asan_chrome_mp&range=271393:271739

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv968rtCCWwDLhzSUpDfrzMv7HRFvpbc4PIc4LzjN85iU6f9WFgYLSYMlxWM_aRDuX2Z8D7xv3oQ4l1YnnXEEHjixN6SvNprq-CQoFAHg85iM9Je2j13lstKPe1k9gnqrRGqL3u3Apc4vZ4zbC-bJfZ800RiD8Q

Additional requirements: Requires Interaction Gestures

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-05-25)

Can we file seperate bug for c#20 and close this one as fixed. it is hard to track stuff in release notes this way.

### ti...@chromium.org (2014-05-27)

Ping urvang@? See c#30 (and then c#20).

### ur...@chromium.org (2014-05-27)

Yes, pls feel free to open a new bug for this.

### ka...@google.com (2014-05-29)

go ahead piman.

### pi...@chromium.org (2014-05-29)

Merged to 35 as r273614

### bu...@chromium.org (2014-05-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a731dc4f8999fcf110c5ee08f8f282edf19efe15

commit a731dc4f8999fcf110c5ee08f8f282edf19efe15
Author: piman@chromium.org <piman@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Thu May 29 22:03:21 2014

Merge 271730 "Workaround bad bitmaps in clibpoard code"

> Workaround bad bitmaps in clibpoard code
> 
> - Some bitmaps end up with a NULL getPixels(). Don't try to copy ot of that.
> - Only try to copy 32-bit bitmaps
> - Protect against overflow in size computation
> 
> BUG=369621
> 
> Review URL: https://codereview.chromium.org/289573002

TBR=piman@chromium.org

Review URL: https://codereview.chromium.org/306053002

git-svn-id: svn://svn.chromium.org/chrome/branches/1916/src@273614 0039d316-1c4b-4281-b951-d872f2087c98



### pi...@chromium.org (2014-05-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-05-29)

------------------------------------------------------------------
r273614 | piman@chromium.org | 2014-05-29T22:03:21.206113Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/content/renderer/renderer_clipboard_client.cc?r1=273614&r2=273613&pathrev=273614
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/content/renderer/webclipboard_impl.cc?r1=273614&r2=273613&pathrev=273614

Merge 271730 "Workaround bad bitmaps in clibpoard code"

> Workaround bad bitmaps in clibpoard code
> 
> - Some bitmaps end up with a NULL getPixels(). Don't try to copy ot of that.
> - Only try to copy 32-bit bitmaps
> - Protect against overflow in size computation
> 
> BUG=369621
> 
> Review URL: https://codereview.chromium.org/289573002

TBR=piman@chromium.org

Review URL: https://codereview.chromium.org/306053002
-----------------------------------------------------------------

### ti...@chromium.org (2014-05-30)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-06-06)

Congrats Atte - $500 for this report.

### ti...@chromium.org (2014-06-09)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-05)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

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

### bu...@chromium.org (2019-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0b694217046d6b2bfa5814676e8615c18e6a45ff

commit 0b694217046d6b2bfa5814676e8615c18e6a45ff
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Thu Jan 03 05:25:18 2019

System Clipboard: Remove extraneous check for bitmap.getPixels()

https://crbug.com/chromium/369621 originally led to this check being introduced via
https://codereview.chromium.org/289573002/patch/40001/50002, but after
https://crrev.com/c/1345809, I'm not sure that it's still necessary.

This change succeeds when tested against the "minimized test case" provided in
crbug.com/369621 's description, but I'm unsure how to make the minimized test
case fail, so this doesn't prove that the change would succeed against the
fuzzer's test case (which originally filed the bug).

As I'm unable to view the relevant fuzzer test case, (see crbug.com/918705),
I don't know exactly what may have caused the fuzzer to fail. Therefore,
I've added a CHECK for the time being, so that we will be notified in canary
if my assumption was incorrect.

Bug: 369621
Change-Id: Ie9b47a4b38ba1ed47624de776015728e541d27f7
Reviewed-on: https://chromium-review.googlesource.com/c/1393436
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Kai Ninomiya <kainino@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#619591}
[modify] https://crrev.com/0b694217046d6b2bfa5814676e8615c18e6a45ff/third_party/blink/renderer/core/clipboard/system_clipboard.cc


### is...@google.com (2019-01-03)

This issue was migrated from crbug.com/chromium/369621?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079486)*
