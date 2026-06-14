# Security: chrome_child!mov_read_keys - Heap corruption as a result of an off-by-1 zero allocation

| Field | Value |
|-------|-------|
| **Issue ID** | [40085298](https://issues.chromium.org/issues/40085298) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media |
| **Reporter** | [Deleted User] |
| **Assignee** | wo...@chromium.org |
| **Created** | 2016-09-03 |
| **Bounty** | $5,500.00 |

## Description

**VULNERABILITY DETAILS**

FFMPEG MP4 decoder contains an Off-by-1 validation results in an allocation of size 0, followed by corrupting an arbitrary number of pointers out of bounds on the heap, where each is pointing to controllable or uninitialized data.

Additional details in attached file: mov\_read\_keys-heap\_corruption-pmehta.readme.txt

<https://cs.chromium.org/chromium/src/third_party/ffmpeg/libavformat/mov.c?rcl=0&l=3145>

static int mov\_read\_keys(MOVContext \*c, AVIOContext \*pb, MOVAtom atom)  

{  

uint32\_t count;  

uint32\_t i;

```
if (atom.size < 8)  
    return 0;  

avio_skip(pb, 4);  
count = avio_rb32(pb);	// count = 0x3FFFFFFF  
if (count > UINT_MAX / sizeof(\*c->meta_keys)) {  // <------------------------------------ This check should be    if(count >= UINT_MAX ...  
    av_log(c->fc, AV_LOG_ERROR,  
           "The 'keys' atom with the invalid key count: %d\n", count);  
    return AVERROR_INVALIDDATA;  
}  

c->meta_keys_count = count + 1;  // 0x3FFFFFFF + 1 = 0x40000000  
c->meta_keys = av_mallocz(c->meta_keys_count \* sizeof(\*c->meta_keys)); // results in an allocation of size 0, followed by corrupting an arbitrary number of pointers out of bounds on the heap   

```

.text:1159A4DE push edi ; s  

.text:1159A4DF call \_avio\_rb32 <--------- read arbitrary DWORD  

.text:1159A4E4 mov esi, eax  

.text:1159A4E6 add esp, 10h  

.text:1159A4E9 mov [ebp+var\_4], esi  

.text:1159A4EC cmp esi, 3FFFFFFFh <--------- Size check  

.text:1159A4F2 jbe short loc\_1159A511 <---------- JBE, should be JB  

.text:1159A4F4 mov eax, [ebp+c]  

.text:1159A4F7 push esi  

.text:1159A4F8 push offset aTheKeysAtomWit ; "The 'keys' atom with the invalid key co"...  

.text:1159A4FD push 10h ; level  

.text:1159A4FF push dword ptr [eax+4] ; avcl  

.text:1159A502 call \_av\_log  

.text:1159A507 add esp, 10h  

.text:1159A50A mov eax, 0BEBBB1B7h  

.text:1159A50F jmp short loc\_1159A590  

.text:1159A511 ; ---------------------------------------------------------------------------  

.text:1159A511  

.text:1159A511 loc\_1159A511: ; CODE XREF: mov\_read\_keys+3Cj  

.text:1159A511 push ebx  

.text:1159A512 mov ebx, [ebp+c]  

.text:1159A515 lea eax, [esi+1]  

.text:1159A518 mov [ebx+2Ch], eax  

.text:1159A51B shl eax, 2 <-------------- Int wrap, allocate zero  

.text:1159A51E push eax ; size  

.text:1159A51F call \_av\_mallocz  

.text:1159A524 mov [ebx+28h], eax

**VERSION**  

Chrome Version: Version 53.0.2785.89 m stable (32-bit only)  

Operating System: All, testing done on Windows

**REPRODUCTION CASE**  

see attached file, mov\_read\_keys-heap\_corruption-pmehta.mp4

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: Varies depending on exploitation techniques.

## Attachments

- [mov_read_keys-heap_corruption-pmehta.readme.txt](attachments/mov_read_keys-heap_corruption-pmehta.readme.txt) (text/plain, 6.9 KB)
- deleted (application/octet-stream, 0 B)
- [mov_read_keys-heap_corruption-pmehta.mp4.bin](attachments/mov_read_keys-heap_corruption-pmehta.mp4.bin) (application/octet-stream, 512.1 KB)

## Timeline

### [Deleted User] (2016-09-03)

Oops... the attached mp4 was crashing the browser... lol. While amusing, this this was unintentional!

I've re-attached the sample with a different extension.

### aa...@google.com (2016-09-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-09-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6505664681869312

### aa...@google.com (2016-09-03)

Thanks Paul for the report.

[Monorail components: Internals>Media]

### cl...@chromium.org (2016-09-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6505664681869312

Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x0da11df0
Crash State:
  mov_read_keys
  mov_read_default
  mov_read_meta
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=415934:416413

Minimized Testcase (512.08 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95VK4o2x1zGBuu9r1ybHj0BxqBroXg6ydAPe9lVj5AFOU_FQuq-9D1nXmJi3hiP-lmKBlXDXQXzprq7ewyTHxd7dpMVw4H8b56SRjletDEznibA5NpeLefeVi5sLTOE_S80snpcCnTbAOx4Ghh6tvJWBqCv6mfCz0wP79Bzwzoi8e8jUZ0?testcase_id=6505664681869312

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### aa...@google.com (2016-09-03)

Author: servolk
Project: chromium
Changelist: https://chromium.googlesource.com/chromium/src/+/4fba1f0c2c06184687345d202f0afd08ae8dde2a
Time: Fri Sep 02 02:04:50 2016
File ffmpeg_demuxer.cc is changed in this cl (and is part of stack frame #4, "media::FFmpegDemuxer::Initialize")
Minimum distance from crash line to modified line: 19. (file: ffmpeg_demuxer.cc, crashed on: 883, modified: 902).

### se...@chromium.org (2016-09-06)

So this is actually a vulnerability in ffmpeg (ffmpeg/libavformat/mov.c) and not in Chromium code. Reassigning to wolenetz@ who is about to roll ffmpeg.

### se...@chromium.org (2016-09-06)

[Empty comment from Monorail migration]

### se...@chromium.org (2016-09-06)

Btw, I have just checked FFmpeg upstream and it looks to me like the issue is still not fixed there. Perhaps we should send a patch to FFmpeg? I can do that, but I'm wondering if we should disclose how it was found and give them access to this bug? Or just send the fix without any explanations?

### se...@chromium.org (2016-09-07)

FYI I've sent a patch to ffmpeg-devel:
http://ffmpeg.org/pipermail/ffmpeg-devel/2016-September/199089.html

### se...@chromium.org (2016-09-08)

The patch has landed in ffmpeg, I guess, we should get it with the next ffmpeg roll.

### wo...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2016-09-09)

The patch looks good to me. Is there anything I can do to help out, or is this starting to wrap up?

### wo...@chromium.org (2016-09-09)

I'll look into cherry-picking this into Chromium ASAP.

### wo...@chromium.org (2016-09-09)

ffmpeg chromium git CR: https://chromium-review.googlesource.com/#/c/383956

Once that lands, I'll roll DEPS in ToT ASAP for it to bake and then begin merging back. Thank you, servolk@ for putting together the patch and sending it upstream already.

### bu...@chromium.org (2016-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/third_party/ffmpeg/+/12183cc1619bd0ae001fc61aa5434b76e2ca5cea

commit 12183cc1619bd0ae001fc61aa5434b76e2ca5cea
Author: Matt Wolenetz <wolenetz@chromium.org>
Date: Fri Sep 09 23:22:47 2016

avformat/mov: Fix potential integer overflow in mov_read_keys

Actual allocation size is computed as (count + 1)*sizeof(meta_keys), so
we need to check that (count + 1) won't cause overflow.

Signed-off-by: Michael Niedermayer <michael@niedermayer.cc>
(cherry picked from commit 347cb14b7cba7560e53f4434b419b9d8800253e7)

BUG=643948

Change-Id: I30d9d9dad8812e969ea52afcfcfbea6bcc0bf208
Reviewed-on: https://chromium-review.googlesource.com/383956
Reviewed-by: Xiaohan Wang <xhwang@chromium.org>

[modify] https://crrev.com/12183cc1619bd0ae001fc61aa5434b76e2ca5cea/libavformat/mov.c
[modify] https://crrev.com/12183cc1619bd0ae001fc61aa5434b76e2ca5cea/chromium/patches/README


### bu...@chromium.org (2016-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/third_party/ffmpeg/+/12183cc1619bd0ae001fc61aa5434b76e2ca5cea

commit 12183cc1619bd0ae001fc61aa5434b76e2ca5cea
Author: Matt Wolenetz <wolenetz@chromium.org>
Date: Fri Sep 09 23:22:47 2016

avformat/mov: Fix potential integer overflow in mov_read_keys

Actual allocation size is computed as (count + 1)*sizeof(meta_keys), so
we need to check that (count + 1) won't cause overflow.

Signed-off-by: Michael Niedermayer <michael@niedermayer.cc>
(cherry picked from commit 347cb14b7cba7560e53f4434b419b9d8800253e7)

BUG=643948

Change-Id: I30d9d9dad8812e969ea52afcfcfbea6bcc0bf208
Reviewed-on: https://chromium-review.googlesource.com/383956
Reviewed-by: Xiaohan Wang <xhwang@chromium.org>

[modify] https://crrev.com/12183cc1619bd0ae001fc61aa5434b76e2ca5cea/libavformat/mov.c
[modify] https://crrev.com/12183cc1619bd0ae001fc61aa5434b76e2ca5cea/chromium/patches/README


### bu...@chromium.org (2016-09-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6e5925dcef736146fa6eed5f2d88c9820963704e

commit 6e5925dcef736146fa6eed5f2d88c9820963704e
Author: wolenetz <wolenetz@chromium.org>
Date: Sat Sep 10 02:08:54 2016

Roll src/third_party/ffmpeg/ 35740fc7b..12183cc16 (5 commits).

https://chromium.googlesource.com/chromium/third_party/ffmpeg.git/+log/35740fc7b72a..12183cc1619b

$ git log 35740fc7b..12183cc16 --date=short --no-merges --format='%ad %ae %s'
2016-09-09 wolenetz avformat/mov: Fix potential integer overflow in mov_read_keys
2016-09-01 chcunningham Detect basename collisions irrespective of file extension.
2016-08-30 chcunningham Adding generate_gn_unittests.py to PRESUBMIT
2016-08-30 chcunningham FFmpeg generate_gn.py: Fix tests and logic reduction algorithm.
2016-08-29 apatole Fix Chrome ARM64 linux compilation errors

TBR=chcunningham@chromium.org,servolk@chromium.org, xhwang@chromium.org
BUG=643948,627567,535788,613452

Review-Url: https://codereview.chromium.org/2330633002
Cr-Commit-Position: refs/heads/master@{#417800}

[modify] https://crrev.com/6e5925dcef736146fa6eed5f2d88c9820963704e/DEPS


### wo...@chromium.org (2016-09-12)

Currently the expected fix is in trunk, awaiting CF confirmation that it's fixed.
CC+=bustamante@ and govind@ in anticipation of requesting merges to m54 and m53 once CF verifies trunk is fixed.

### go...@chromium.org (2016-09-12)

+ awhalley@chromium.org, this change is not yet baked in Beta so it we can't take it for this week M53 Stable release correct? 

Adding M54 label based on https://crbug.com/chromium/643948#c22.

### aw...@chromium.org (2016-09-12)

Hi govind@ - correct, not for this week's M53 release.

### sh...@chromium.org (2016-09-27)

wolenetz: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2016-10-11)

The testcase has been marked as non reproducible on ClusterFuzz. Should we mark this as Fixed?

### cl...@chromium.org (2016-10-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6754734893694976

### sh...@chromium.org (2016-10-11)

wolenetz: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-21)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-10-21)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### go...@chromium.org (2016-10-22)

+awhalley@ (Secutiy TPM) for M55 review.

### aw...@chromium.org (2016-10-24)

Good bug to take for M55.  An alternative to the full DEPS roll would be to cherry pick:

2016-09-09 wolenetz avformat/mov: Fix potential integer overflow in mov_read_keys

into an M55 branch, if that might be lower risk.



### aw...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-10-24)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### go...@chromium.org (2016-10-24)

Approving merge to M55 branch 2883 based on https://crbug.com/chromium/643948#c35 & #36. Please merge ASAP. Thank you.

### wo...@chromium.org (2016-10-24)

This actually landed in M55 (https://bugs.chromium.org/p/chromium/issues/detail?id=643948#c21 https://chromium.googlesource.com/chromium/src.git/+/6e5925dcef736146fa6eed5f2d88c9820963704e r417800), and was awaiting potential merge to M54 and M53, though didn't get approval for those.

### wo...@chromium.org (2016-10-24)

Per #22 and repeated attempts to get CF to verify this as fixed (finally successful Oct 11 per #27), this was awaiting such confirmation for merge to M54 (and originally, M53 too).

bustamante@: CF, as of #27, confirms, so requesting merge to M54 now.

### di...@chromium.org (2016-10-26)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### di...@chromium.org (2016-10-26)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### bu...@google.com (2016-10-26)

Per discussion with awhalley@, approved for merging into 54

### aw...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-27)

The panel awarded $5,500 for this - thanks for a great report!

### bu...@chromium.org (2016-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/third_party/ffmpeg/+/cf2d534bf049984bf179d09488c5c86735ddbc1d

commit cf2d534bf049984bf179d09488c5c86735ddbc1d
Author: Matt Wolenetz <wolenetz@chromium.org>
Date: Fri Oct 28 01:38:43 2016

avformat/mov: Fix potential integer overflow in mov_read_keys

Actual allocation size is computed as (count + 1)*sizeof(meta_keys), so
we need to check that (count + 1) won't cause overflow.

Signed-off-by: Michael Niedermayer <michael@niedermayer.cc>
(cherry picked from commit 347cb14b7cba7560e53f4434b419b9d8800253e7)

BUG=643948

Change-Id: I30d9d9dad8812e969ea52afcfcfbea6bcc0bf208
Reviewed-on: https://chromium-review.googlesource.com/383956
Reviewed-by: Xiaohan Wang <xhwang@chromium.org>
(cherry picked from commit 12183cc1619bd0ae001fc61aa5434b76e2ca5cea)

TBR=xhwang@chromium.org

Change-Id: I8fdb5c4120cb35f6e83166c139b53d22301d6c6b
Reviewed-on: https://chromium-review.googlesource.com/404650
Reviewed-by: Matthew Wolenetz <wolenetz@chromium.org>

[modify] https://crrev.com/cf2d534bf049984bf179d09488c5c86735ddbc1d/libavformat/mov.c
[modify] https://crrev.com/cf2d534bf049984bf179d09488c5c86735ddbc1d/chromium/patches/README


### wo...@chromium.org (2016-10-28)

The label "merge-merged-m54-cherry-picks" added in #46 doesn't mean this is merged to M54 yet. An M54 git-drover of a DEPS roll for ffmpeg to cf2d534b still needs to occur to complete this merge to M54.

### bu...@chromium.org (2016-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0a318e4039f7af462baf77fe309f5e40a33ecda1

commit 0a318e4039f7af462baf77fe309f5e40a33ecda1
Author: Matt Wolenetz <wolenetz@chromium.org>
Date: Fri Oct 28 02:09:34 2016

M54: Roll FFmpeg 75976ae..cf2d534b

https://chromium.googlesource.com/chromium/third_party/ffmpeg/+log/75976ae..cf2d534b

cf2d534 avformat/mov: Fix potential integer overflow in mov_read_keys

BUG=643948
TBR=xhwang@chromium.org

Review URL: https://codereview.chromium.org/2453323005 .

Cr-Commit-Position: refs/branch-heads/2840@{#791}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/0a318e4039f7af462baf77fe309f5e40a33ecda1/DEPS


### am...@chromium.org (2016-10-28)

The buildspec change was merged for realzies with https://chrome-internal.googlesource.com/chrome/tools/buildspec.git/+/e715515d727225044e25fc34872d73f71b8d04ea

### wo...@chromium.org (2016-10-28)

amineer@, thank you for updating the buildspec. (#48 had no effect on the release branch builds.)

### aw...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@google.com (2017-01-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/643948?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/591845]
[Monorail mergedwith: crbug.com/chromium/643947]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085298)*
