# UNKNOWN in SkReader32::readString

| Field | Value |
|-------|-------|
| **Issue ID** | [40082060](https://issues.chromium.org/issues/40082060) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2015-05-11 |
| **Bounty** | $5,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5652598367977472

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: UNKNOWN
Crash Address: 0x26560629
Crash State:
  SkReader32::readString
  SkPicturePlayback::handleOp
  SkPicturePlayback::draw
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=321145:321361

Minimized Testcase (1.12 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97Zl-NFe4CsPe5inlV-0kO_DmAyDYtwy0dTsWd2RldDYry9pIaM2Y-Udxcpz8jJ6uCVtQQQMvjkWQggHZUda80K1o0TXWYdvdK_u4T7NzZhC5xTLSsiP7nDiNvvP_2l8oTQND8sB6s0RjiUeFSjLZqSzEsLtQ

Filer: mbarbella

## Timeline

### mb...@chromium.org (2015-05-11)

Bulk edit: I'm starting to look at some of the crashes from the batch of test cases we got now, but could use help with triage.

### mb...@chromium.org (2015-05-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-18)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-05-18)

The issue here appears to be an unchecked string size (in this case):

readString is called twice in SkPicturePlayback::handleOp for COMMENTs:

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/skia/src/core/SkPicturePlayback.cpp&sq=package:chromium&type=cs&l=211

Inside readString, the length is read through a readInt and used is passed to ->skip(). This skip size is not checked in Release builds (potentially leading to fCurr >= fStop), and the subsequent readString will attempt to read invalid data. 

This could seems like a serious arbitrary (relative) read as the result of the string read (assuming we didn't crash) is added as a comment to the canvas (I'm assuming this can be read by an attacker).

sugoi@, reed@, senorblanco@, do any of you want to contribute or suggest a patch for this? There may be other similar instances so the real fix might be somewhere else rather than in the functions described above?

### oc...@chromium.org (2015-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2015-05-18)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-05-19)

After taking another closer look at this, a lot of the SkPicturePlayback/SkReader32 code look very scary. Is there any reason why an SkValidatingReadBuffer isn't used here instead of an SkReader32?

### re...@google.com (2015-05-19)

Just a performance concern. We added the Validating variant when we wanted to deserialize drawings for cross-process use, but have been assuming it would be a slow-down for the simpler case. This is something we will measure.

### [Deleted User] (2015-05-19)

I believe SkPipe and so SkDeferredCanvas remain as performance-critical parts of Skia using SkReader32.  SkValidatingReadBuffer and SkReader32 serve slightly different functions with different APIs, and SkValidatingReadBuffer _is_ in use here, but it'd certainly be fine to use SkValidatingReadBuffer more when deserializing pictures, or to buff SkReader32 up with a validating mode.

This looks like another case where we're deserializing an SkPictureShader.  Don't we shut up all these fuzzer alerts at once by disallowing their serialization in Chrome (i.e. when   SK_DISALLOW_CROSSPROCESS_PICTUREIMAGEFILTERS is set)?

### se...@chromium.org (2015-05-19)

SkPictureShader != SkPictureImageFilter. SK_DISALLOW_CROSSPROCESS_PICTUREIMAGEFILTERS handles the latter. If it's in danger of being deserialized in Chrome (which it seems it is), SkPictureShader should be protected by an #ifdef as well. Or the same one, renamed.

In general, we should be very cautious about what gets added to SkGlobalInitialization_chromium.cpp, since IIUC this controls what is whitelisted for deserialization in Chrome. At a minimum, any new classes added for deserialization should be added to SampleFilterFuzz.cpp.

### [Deleted User] (2015-05-19)

Uh, sure, SK_DISALLOW_CROSSPROCESS_PICTURES seems fine.

We're still only serializing (and thus fuzzing) image filters right?  No plans to expand to pictures?  If I'm reading this right, the chain we're seeing here is SkRectShaderImageFilter -> SkPictureShader -> SkPicture, so snuffing out SkPictureShader should do the trick.

Speaking of SkGlobalInitialization_chromium.cpp, why is SkPictureImageFilter in there?

### se...@chromium.org (2015-05-19)

Re: #14: When capturing SKPs in Trace Viewer, it's nice to be able to capture them with the SkPictureImageFilters intact. Although they're not currently supported for the accelerated reference filter implementation which serializes to the browser process (due to the security issues above), they are supported for the in-process case (e.g., SVG filters on SVG content).

Doing a compile with the #ifdef disabled allows folks to capture SKPs containing them.

### [Deleted User] (2015-05-19)

Ah, yeah, that is handy.

Do we get the same effect by moving the #ifdef guard to SkGlobalInitialization_chromium.cpp?

#ifndef SK_DISALLOW_CROSSPROCESS_PICTURES
        SK_DEFINE_FLATTENABLE_REGISTRAR_ENTRY(SkPictureImageFilter)
        SK_DEFINE_FLATTENABLE_REGISTRAR_ENTRY(SkPictureShader)
#endif

### se...@chromium.org (2015-05-19)

I don't think it's quite the same, since the serialization/deserialization still "works" with the disable on, it just writes out an SkPictureImageFilter with an empty SkPicture (doesn't traverse into the SkPicture) and renders black for that content. If we removed it from the initialization, it might fail at [de]serialization time and [read]write a NULL into the stream, causing other unpleasantness. To be honest, I'm not certain exactly what the result would be.

### [Deleted User] (2015-05-19)

Gotcha.  Sounds like the best plan is to just guard SkPictureShader in the same way we do SkPicutreImageFilter today.

### oc...@chromium.org (2015-05-20)

This sounds like a fairly simple patch if I'm understanding this correctly, and should fix quite a few high severity bugs we have right now. 

mtklein@, Could you please make this a priority if that's possible?



### bu...@chromium.org (2015-05-20)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/76be9c8dc0e5306ef81c2987848088cdec7ccd3f

commit 76be9c8dc0e5306ef81c2987848088cdec7ccd3f
Author: mtklein <mtklein@chromium.org>
Date: Wed May 20 19:05:15 2015

Don't serialize SkPictures in SkPictureShaders when in untrusted mode.

This requires we "first" add a has-picture bool to SkPictureShader serialized format.

BUG=chromium:486947, billions and billions of others.

Review URL: https://codereview.chromium.org/1151663002

[modify] http://crrev.com/76be9c8dc0e5306ef81c2987848088cdec7ccd3f/include/core/SkPicture.h
[modify] http://crrev.com/76be9c8dc0e5306ef81c2987848088cdec7ccd3f/src/core/SkPictureShader.cpp
[modify] http://crrev.com/76be9c8dc0e5306ef81c2987848088cdec7ccd3f/src/core/SkReadBuffer.h


### in...@chromium.org (2015-05-20)

Thanks!

### am...@chromium.org (2015-05-20)

Is there a merge required here?

### [Deleted User] (2015-05-20)

So continuing to use this bug as a proxy for all other bugs, I believe a merge is required for these bugs if and only if we possibly can actually try to send an SkRectShaderImageFilter wrapping an SkPictureShader from a renderer to the browser process.  If this is only produceable by the fuzzer, I don't think there's any need to merge anything.  That is, I see .fil files representing these tests cases; are they representable as web pages?  I don't personally know how to answer these questions.


clusterfuzz will go through and confirm that these failures cease, right?  As the author of the fix, I'd feel warmer and fuzzier if the bot can confirm the fix.

### in...@chromium.org (2015-05-20)

Yes CF will verify them in ~1 day.

### se...@chromium.org (2015-05-20)

The danger is that a compromised renderer could construct a malicious stream as above (SkPictureShader inside an SkRectShaderImageFilter) and mess with the browser process.

### [Deleted User] (2015-05-20)

Ah, yeah, I guess from that perspective the answer to "can we possibly actually try to send an ... to the browser process" is yes for all "...".  A compromised renderer can do anything.

Sounds like this wants to be merged to all branches all the way back to when we started sending image filters to the browser process, right?

### se...@chromium.org (2015-05-20)

Well, back to when SkPictureShader was added, since that was more recent IIRC. But security team will tell us where they want the merges.

We should probably add a comment to src/ports/SkGlobalInitialization_chromium.cpp asking folks to add a change to SampleFilterFuzz when they add a new class to be serialized. Then we would have caught this sooner. (Unless such a comment draws too much attention to sensitive code. I don't know what the best practice is here.)

### mb...@chromium.org (2015-05-20)

It's a very good idea to add the comment mentioned in c#27.

### cl...@chromium.org (2015-05-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-05-21)

ClusterFuzz has detected this issue as fixed in range 330758:330903.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5652598367977472

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: UNKNOWN
Crash Address: 0x26560629
Crash State:
  SkReader32::readString
  SkPicturePlayback::handleOp
  SkPicturePlayback::draw
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=321145:321361
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=330758:330903

Minimized Testcase (1.12 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97Zl-NFe4CsPe5inlV-0kO_DmAyDYtwy0dTsWd2RldDYry9pIaM2Y-Udxcpz8jJ6uCVtQQQMvjkWQggHZUda80K1o0TXWYdvdK_u4T7NzZhC5xTLSsiP7nDiNvvP_2l8oTQND8sB6s0RjiUeFSjLZqSzEsLtQ

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ti...@google.com (2015-06-11)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-12)

[Empty comment from Monorail migration]

### pe...@google.com (2015-06-12)

Approved for M44 (branch: 2403)

### bu...@chromium.org (2015-06-16)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/921827bbc78717f514ebd11bf55ac0dd2fe9308c

commit 921827bbc78717f514ebd11bf55ac0dd2fe9308c
Author: mtklein <mtklein@chromium.org>
Date: Tue Jun 16 20:23:03 2015

Add a note to SkGlobalInitialization_chromium.cpp.

BUG=chromium:486947

Review URL: https://codereview.chromium.org/1193453004

[modify] http://crrev.com/921827bbc78717f514ebd11bf55ac0dd2fe9308c/src/ports/SkGlobalInitialization_chromium.cpp


### pe...@chromium.org (2015-07-06)

Please finish merging your CL into M44 asap.  You have one week before stable candidate is built.

### [Deleted User] (2015-07-07)

Thanks for the reminder.  I just landed a merge into Skia's M44 branch.

https://skia.googlesource.com/skia/+/1dd3830b7254eaea8d710b256f7f040668f02458

(Don't know if bugdroid will pick it up.)

### pe...@chromium.org (2015-07-13)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-17)

cloudfuzzer: $5000 for this report.

### cl...@chromium.org (2015-08-26)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/486947?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082060)*
