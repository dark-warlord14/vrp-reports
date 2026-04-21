# Security: pdfium - write past end of heap buffer when parsing invalid JPEG2000 image

| Field | Value |
|-------|-------|
| **Issue ID** | [40081439](https://issues.chromium.org/issues/40081439) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2015-02-17 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

A PDF file containing a malformed JPEG2000 image causes opj\_pi\_next\_cprl and opj\_pi\_next\_lrcp in pdfium's bundled openjpeg to write past the end of a heap buffer. More specifically, an attacker can rewrite a 16-bit integer at some location past the end of the buffer from 0x0000 to 0x0001:

```
 if (!pi->include[index]) {  
     pi->include[index] = 1;  
     return OPJ_TRUE;  
 }  

```

It's possible to write to locations up to 16 bytes beyond the end of the buffer or maybe even more. I suspect code execution may be possible despite having no control over the contents of the write but don't have the exploit-writing skills to confirm this.

Reported upstream: <https://code.google.com/p/openjpeg/issues/detail?id=476>

**VERSION**  

pdfium\_test 7435e8e5 on Gentoo Linux Hardened x86\_64  

Chrome Version: 40.0.2214.111 stable  

Operating System: Gentoo Linux Hardened x86\_64

**REPRODUCTION CASE**  

Attached. Note that in order to crash the uninstrumented Chrome plugin reliably, I had to create openjpeg-svn-id000179-opj\_pi\_next\_cprl-demo.pdf which contains multiple images; for analysis please use the other files instead.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: plugin crash / pdfium\_test crash  

Crash State (for openjpeg-svn-id000179-opj\_pi\_next\_cprl-buffer-overflow-id000178svn.pdf):  

==1060== Invalid write of size 2  

==1060== at 0x3B9C2F: opj\_pi\_next\_lrcp (pi.c:261)  

==1060== by 0x3BF4DA: opj\_pi\_next (pi.c:1858)  

==1060== by 0x3F507B: opj\_t2\_decode\_packets (t2.c:406)  

==1060== by 0x3C3985: opj\_tcd\_t2\_decode (tcd.c:1532)  

==1060== by 0x3C31B4: opj\_tcd\_decode\_tile (tcd.c:1272)  

==1060== by 0x3B1319: opj\_j2k\_decode\_tile (j2k.c:7914)  

==1060== by 0x3B5810: opj\_j2k\_decode\_tiles (j2k.c:9428)  

==1060== by 0x3AF8DC: opj\_j2k\_exec (j2k.c:7292)  

==1060== by 0x3B5FDE: opj\_j2k\_decode (j2k.c:9619)  

==1060== by 0x324E62: opj\_jp2\_decode (jp2.c:1406)  

==1060== by 0x321092: opj\_decode (openjpeg.c:412)  

==1060== by 0x31CE2C: CJPX\_Decoder::Init(unsigned char const\*, int) (fx\_codec\_jpx\_opj.cpp:632)  

==1060== Address 0x6921f98 is 8 bytes after a block of size 96 alloc'd  

==1060== at 0x4C2D50F: calloc (vg\_replace\_malloc.c:623)  

==1060== by 0x3BD0C3: opj\_pi\_create\_decode (pi.c:1234)  

==1060== by 0x3F4D89: opj\_t2\_decode\_packets (t2.c:375)  

==1060== by 0x3C3985: opj\_tcd\_t2\_decode (tcd.c:1532)  

==1060== by 0x3C31B4: opj\_tcd\_decode\_tile (tcd.c:1272)  

==1060== by 0x3B1319: opj\_j2k\_decode\_tile (j2k.c:7914)  

==1060== by 0x3B5810: opj\_j2k\_decode\_tiles (j2k.c:9428)  

==1060== by 0x3AF8DC: opj\_j2k\_exec (j2k.c:7292)  

==1060== by 0x3B5FDE: opj\_j2k\_decode (j2k.c:9619)  

==1060== by 0x324E62: opj\_jp2\_decode (jp2.c:1406)  

==1060== by 0x321092: opj\_decode (openjpeg.c:412)  

==1060== by 0x31CE2C: CJPX\_Decoder::Init(unsigned char const\*, int) (fx\_codec\_jpx\_opj.cpp:632)

## Attachments

- [openjpeg-svn-id000179-opj_pi_next_cprl-pdfium.zip](attachments/openjpeg-svn-id000179-opj_pi_next_cprl-pdfium.zip) (application/zip, 3.4 KB)

## Timeline

### in...@chromium.org (2015-02-17)

Oh no, the openjpeg issue tracker is public :(

### ma...@gmail.com (2015-02-17)

Whoops, sorry about that. Do they have some other security reporting process I should have used instead? They do have some way of marking security-critical bugs as private because I ran into a few unviewable reports researching other crashes, but there doesn't seem to be any way to actually report them.

### in...@chromium.org (2015-02-17)

+cc openjpeg folks who can mark the bug as private and help with fix. (if that function is available).

### js...@chromium.org (2015-02-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### an...@gmail.com (2015-02-21)

Thanks, it has been made private (and priority-critical) on the openjpeg issue tracker

### ju...@foxitsoftware.com (2015-02-26)

@antonin, 

For these openjpeg issues raised in chromium/pdfium, shall we open another issues in openjpeg or just cc you guys in these issues tracked in chromium/pdfium?

### cl...@chromium.org (2015-03-13)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-27)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-12)

jun_fang@: Uh oh! This issue is still open and hasn't been updated in the last 44 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-20)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### th...@chromium.org (2015-04-20)

Jun, can you CC tsepez@ and me on https://code.google.com/p/openjpeg/issues/detail?id=476 ? We are curious how this is going but can't see the OpenJPEG bug.

### ju...@foxitsoftware.com (2015-04-20)

Seem that https://crbug.com/chromium/476 has been deleted from openjpeg. I can't find it in the issue list of openjpeg.

### ma...@gmail.com (2015-04-20)

openjpeg https://crbug.com/chromium/476 is still there, it's just non-public. I can see it still but I don't appear to have sufficient permissions to CC you in on it. No real activity though; I suggested a possible patch a couple of months back but that's about it really.

### ju...@foxitsoftware.com (2015-04-20)

[Comment Deleted]

### ti...@google.com (2015-05-07)

Checking in here - what's the status of the openjpeg issue?

### cl...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2015-05-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-05-19)

I dont think we can wait forever here, can we just patch our own copy of openjpeg in pdfium with makosoft@'s patch (c#16). Jun/Tom, can you please help here.

### ju...@foxitsoftware.com (2015-05-19)

OK. I will create a patch in pdfium.

### ti...@google.com (2015-05-21)

Hey Jun - when do you expect to have the patch finished by? I ask because we're currently trying to clear out a list of older bugs that are important and this one is on our list.

### ju...@foxitsoftware.com (2015-05-21)

I try to understand the patch in c#16 and it takes me several days to know the backround of JPEG2000. I plan to submit a patch on May 25th. 

### ju...@foxitsoftware.com (2015-05-26)

Pending in https://codereview.chromium.org/1160663002/.

### ju...@foxitsoftware.com (2015-05-26)

Fixed in https://pdfium.googlesource.com/pdfium/+/cddfde0cddbc8467e0d5fa04c30405ee257750fc.

### cl...@chromium.org (2015-05-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6e5d15268c5d75ba15189ce0a6050845068eb06b

commit 6e5d15268c5d75ba15189ce0a6050845068eb06b
Author: tsepez <tsepez@chromium.org>
Date: Wed Jun 03 00:50:49 2015

Roll PDFium to b29338d

This brings in:
b29338d Fix windows compile: fix size_t vs. int mismatch
e06b686 kill IPDF_DocParser().
4ff7a42 Fix heap use after free in Document::DoFieldDelay and Document::delay
8e1b608 Add missing comma to third_party.gyp
cafa3fd Run V8 in predictable mode for pdfium_test
8ba4a3c Fix suppressions for 2015-05-28 drop
878b819 Roll DEPS to pick up 2015-05-28 corpus drop.
6b776fe Fix ALL the include guards.
14f57a1 Remove rendundant ../include from paths of files in include/ directory
cddfde0 Upgrade openjpeg to r3002
5f566b3 Update copy of safe_math_impl.h to take a fix from upstream:
e6406b3 Fix four annoying warnings: Two "set but unused".
bc4b82e Fix an endless loop in CJBig2_HuffmanTable::parseFromCodedBuffer
79569e7 Get test running scripts to detect and report common error.
e9ccc9b Integer overflow in CJBig2_Image::expand
3a25130 Tidy public fpdfview.h and fpdf_flatten.h.
b190fc2 Turn on warnings for usage of disabled V8 APIs
981a346 Re-land: Remove FX_Alloc() null checks now that it can't return NULL.
bf4aa2c Revert "Remove FX_Alloc() null checks now that it can't return NULL."
eb65277 Remove FX_Alloc() null checks now that it can't return NULL.
59f4b44 Fix Heap Overflow in CJBig2_Image::expand
3b60890 Cleanup if early return from opj_j2k_copy_default_tcp_and_create_tcd().
3fea540 Replace v8::Handle with v8::Local and v8::Persistent with v8::Global
0c94bc4 Change FX_Alloc to FX_Try_Alloc in _JpegEncode
31b3a2b Add safe FX_Alloc2D() macro
a88e3a1 Add myself to OWNERS file
d94df88 Replace deprecated with non-deprecated V8 APIs
1962d61 Fix leaks in embedder test's FlateEncode() usage and in FlateEncode().
69b4bc7 Disable allocation tests that hose the bot.
acae925 Initialize members of CPDF_TextPageFind class.
61ffad8 Fix leaks in the embedder tests themselves.
9f6f348 Abort on OOM by default in FX_Alloc().
dc0bd92 Remove FX_NEW_VECTOR() macros.
7f3b99a Fix potential UAF in ConcatInPlace.
b60617f Fix another batch of compiler warnings.

BUG=459215,482639,483981,486538,487928,488302
R=thestig@chromium.org

Review URL: https://codereview.chromium.org/1159433007

Cr-Commit-Position: refs/heads/master@{#332514}

[modify] http://crrev.com/6e5d15268c5d75ba15189ce0a6050845068eb06b/DEPS


### bu...@chromium.org (2015-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/af1125ea286450ceecc23a37c6710bcf0b2d1ce6

commit af1125ea286450ceecc23a37c6710bcf0b2d1ce6
Author: engedy <engedy@chromium.org>
Date: Wed Jun 03 09:15:29 2015

Revert of Roll PDFium to b29338d (patchset #2 id:20001 of https://codereview.chromium.org/1159433007/)

Reason for revert:
Causes compile errors on "Linux GN Clobber" bot:

../../third_party/pdfium/core/src/fxcrt/fx_basic_memmgr_unittest.cpp:23:31:error: expression result unused [-Werror,-Wunused-value]
    EXPECT_DEATH_IF_SUPPORTED(FX_Alloc(int, kMaxIntAlloc), "");

Archived full build log: https://goo.gl/4OImxB.

Original issue's description:
> Roll PDFium to b29338d
>
> This brings in:
> b29338d Fix windows compile: fix size_t vs. int mismatch
> e06b686 kill IPDF_DocParser().
> 4ff7a42 Fix heap use after free in Document::DoFieldDelay and Document::delay
> 8e1b608 Add missing comma to third_party.gyp
> cafa3fd Run V8 in predictable mode for pdfium_test
> 8ba4a3c Fix suppressions for 2015-05-28 drop
> 878b819 Roll DEPS to pick up 2015-05-28 corpus drop.
> 6b776fe Fix ALL the include guards.
> 14f57a1 Remove rendundant ../include from paths of files in include/ directory
> cddfde0 Upgrade openjpeg to r3002
> 5f566b3 Update copy of safe_math_impl.h to take a fix from upstream:
> e6406b3 Fix four annoying warnings: Two "set but unused".
> bc4b82e Fix an endless loop in CJBig2_HuffmanTable::parseFromCodedBuffer
> 79569e7 Get test running scripts to detect and report common error.
> e9ccc9b Integer overflow in CJBig2_Image::expand
> 3a25130 Tidy public fpdfview.h and fpdf_flatten.h.
> b190fc2 Turn on warnings for usage of disabled V8 APIs
> 981a346 Re-land: Remove FX_Alloc() null checks now that it can't return NULL.
> bf4aa2c Revert "Remove FX_Alloc() null checks now that it can't return NULL."
> eb65277 Remove FX_Alloc() null checks now that it can't return NULL.
> 59f4b44 Fix Heap Overflow in CJBig2_Image::expand
> 3b60890 Cleanup if early return from opj_j2k_copy_default_tcp_and_create_tcd().
> 3fea540 Replace v8::Handle with v8::Local and v8::Persistent with v8::Global
> 0c94bc4 Change FX_Alloc to FX_Try_Alloc in _JpegEncode
> 31b3a2b Add safe FX_Alloc2D() macro
> a88e3a1 Add myself to OWNERS file
> d94df88 Replace deprecated with non-deprecated V8 APIs
> 1962d61 Fix leaks in embedder test's FlateEncode() usage and in FlateEncode().
> 69b4bc7 Disable allocation tests that hose the bot.
> acae925 Initialize members of CPDF_TextPageFind class.
> 61ffad8 Fix leaks in the embedder tests themselves.
> 9f6f348 Abort on OOM by default in FX_Alloc().
> dc0bd92 Remove FX_NEW_VECTOR() macros.
> 7f3b99a Fix potential UAF in ConcatInPlace.
> b60617f Fix another batch of compiler warnings.
>
> BUG=459215,482639,483981,486538,487928,488302
> R=thestig@chromium.org
>
> Committed: https://crrev.com/6e5d15268c5d75ba15189ce0a6050845068eb06b
> Cr-Commit-Position: refs/heads/master@{#332514}

TBR=thestig@chromium.org,tsepez@chromium.org
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=459215,482639,483981,486538,487928,488302

Review URL: https://codereview.chromium.org/1162103004

Cr-Commit-Position: refs/heads/master@{#332579}

[modify] http://crrev.com/af1125ea286450ceecc23a37c6710bcf0b2d1ce6/DEPS


### bu...@chromium.org (2015-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1203cc8c7e82ab31d99190ccd595e813ac7ab9f9

commit 1203cc8c7e82ab31d99190ccd595e813ac7ab9f9
Author: tsepez <tsepez@chromium.org>
Date: Wed Jun 03 21:26:06 2015

Roll PDFium to 7bb4d8d

This brings in:
7bb4d8d Fix fx_basic_memmgr_unittest.cpp under stricter GN rules
a76f557 Automated test case for 487928.
b29338d Fix windows compile: fix size_t vs. int mismatch
e06b686 kill IPDF_DocParser().
4ff7a42 Fix heap use after free in Document::DoFieldDelay and Document::delay
8e1b608 Add missing comma to third_party.gyp
cafa3fd Run V8 in predictable mode for pdfium_test
8ba4a3c Fix suppressions for 2015-05-28 drop
878b819 Roll DEPS to pick up 2015-05-28 corpus drop.
6b776fe Fix ALL the include guards.
14f57a1 Remove rendundant ../include from paths of files in include/ directory
cddfde0 Upgrade openjpeg to r3002
5f566b3 Update copy of safe_math_impl.h to take a fix from upstream:
e6406b3 Fix four annoying warnings: Two "set but unused".
bc4b82e Fix an endless loop in CJBig2_HuffmanTable::parseFromCodedBuffer
79569e7 Get test running scripts to detect and report common error.
e9ccc9b Integer overflow in CJBig2_Image::expand
3a25130 Tidy public fpdfview.h and fpdf_flatten.h.
b190fc2 Turn on warnings for usage of disabled V8 APIs
981a346 Re-land: Remove FX_Alloc() null checks now that it can't return NULL.
bf4aa2c Revert "Remove FX_Alloc() null checks now that it can't return NULL."
eb65277 Remove FX_Alloc() null checks now that it can't return NULL.
59f4b44 Fix Heap Overflow in CJBig2_Image::expand
3b60890 Cleanup if early return from opj_j2k_copy_default_tcp_and_create_tcd().
3fea540 Replace v8::Handle with v8::Local and v8::Persistent with v8::Global
0c94bc4 Change FX_Alloc to FX_Try_Alloc in _JpegEncode
31b3a2b Add safe FX_Alloc2D() macro
a88e3a1 Add myself to OWNERS file
d94df88 Replace deprecated with non-deprecated V8 APIs
1962d61 Fix leaks in embedder test's FlateEncode() usage and in FlateEncode().
69b4bc7 Disable allocation tests that hose the bot.
acae925 Initialize members of CPDF_TextPageFind class.
61ffad8 Fix leaks in the embedder tests themselves.
9f6f348 Abort on OOM by default in FX_Alloc().
dc0bd92 Remove FX_NEW_VECTOR() macros.
7f3b99a Fix potential UAF in ConcatInPlace.
b60617f Fix another batch of compiler warnings.

BUG=459215,482639,483981,486538,487928,488302
R=thestig@chromium.org

Committed: https://crrev.com/6e5d15268c5d75ba15189ce0a6050845068eb06b
Cr-Commit-Position: refs/heads/master@{#332514}

Review URL: https://codereview.chromium.org/1159433007

Cr-Commit-Position: refs/heads/master@{#332687}

[modify] http://crrev.com/1203cc8c7e82ab31d99190ccd595e813ac7ab9f9/DEPS


### ti...@google.com (2015-07-08)

Merge-requested to M44 (2403) PDFium branch.

### pe...@google.com (2015-07-08)

[Automated comment] Reverts referenced in bugdroid comments, needs manual review.

### pe...@google.com (2015-07-10)

You're going to need to give me very specific CLs that need to go to M44 pdfium.  We don't just roll a whole bunch of CLs.  Then they'll need to be cherry-picked after I approve.

### pe...@google.com (2015-07-10)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-07-13)

Need to cherrypick https://pdfium.googlesource.com/pdfium/+/cddfde0cddbc8467e0d5fa04c30405ee257750fc

### pe...@chromium.org (2015-07-13)

Approved for merge to m44 branch https://pdfium.googlesource.com/pdfium/+log/refs/heads/chromium/2403.

Thanks Lei.

### pe...@chromium.org (2015-07-13)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-17)

@makosoft: We took this through our reward panel and decided to reward you with $3,000 for this report. We'll get in contact regarding payment details within a week. If that doesn't happen, please email me at timwillis@

Congratulations!

### ti...@google.com (2015-08-28)

Payment in process: waiting on supplier enrollment

### cl...@chromium.org (2015-09-01)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/459215?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081439)*
