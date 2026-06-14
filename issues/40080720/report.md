# Heap-use-after-free in matroska_read_seek

| Field | Value |
|-------|-------|
| **Issue ID** | [40080720](https://issues.chromium.org/issues/40080720) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>FFmpeg |
| **Platforms** | Linux |
| **Reporter** | ao...@gmail.com |
| **Assignee** | xh...@chromium.org |
| **Created** | 2014-10-26 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36

Steps to reproduce the problem:
1. $ chrome-asan uaf-w4-matroska_read_seek.html
2. Wait about 4 seconds.
3. ASan spots the issue.

What is the expected behavior?
ASan doesn't spot a use after free issue.

What went wrong?
It does.

Did this work before? N/A 

Chrome version: 40.0.2200.0  Channel: stable
OS Version: 3.2.0
Flash Version: Shockwave Flash 14.0 r0

==789==ERROR: AddressSanitizer: heap-use-after-free on address 0x61300006fdb4 at pc 0x7f30d6f2bc3c bp 0x7f30ad250ba0 sp 0x7f30ad250b98
WRITE of size 4 at 0x61300006fdb4 thread T10 (FFmpegDemuxer)
    #0 0x7f30d6f2bc3b in matroska_read_seek /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavformat/matroskadec.c:2959
    #1 0x7f30d6f658b4 in seek_frame_internal /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavformat/utils.c:2050
    #2 0x7f30d6f652bf in av_seek_frame /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/ffmpeg/libavformat/utils.c:2082
    #3 0x7f30f20e72f7 in base::internal::InvokeHelper<false, int, base::internal::RunnableAdapter<int (*)(AVFormatContext*, int, long, int)>, void (AVFormatContext* const&, int const&, long const&, int const&)>::MakeItSo(base::internal::RunnableAdapter<int (*)(AVFormatContext*, int, long, int)>, AVFormatContext* const&, int const&, long const&, int const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:947
    #4 0x7f30e921d56e in void base::internal::ReturnAsParamAdapter<int>(base::Callback<int ()> const&, int*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/task_runner_util.h:23
    #5 0x7f30e921e5fa in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(base::Callback<int ()> const&, int*)>, void (base::Callback<int ()> const&, int* const&)>::MakeItSo(base::internal::RunnableAdapter<void (*)(base::Callback<int ()> const&, int*)>, base::Callback<int ()> const&, int* const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:898
    #6 0x7f30e953b2b0 in base::(anonymous namespace)::PostTaskAndReplyRelay::Run() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/threading/post_task_and_reply_impl.cc:42
    #7 0x7f30e953bbc4 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::(anonymous namespace)::PostTaskAndReplyRelay::*)()>, void (base::(anonymous namespace)::PostTaskAndReplyRelay*)>::MakeItSo(base::internal::RunnableAdapter<void (base::(anonymous namespace)::PostTaskAndReplyRelay::*)()>, base::(anonymous namespace)::PostTaskAndReplyRelay*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:871
    #8 0x7f30e953b8ea in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::(anonymous namespace)::PostTaskAndReplyRelay::*)()>, void (base::(anonymous namespace)::PostTaskAndReplyRelay*), void (base::internal::UnretainedWrapper<base::(anonymous namespace)::PostTaskAndReplyRelay>)>, void (base::(anonymous namespace)::PostTaskAndReplyRelay*)>::Run(base::internal::BindStateBase*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../base/bind_internal.h:1166
[...]

## Attachments

- [uaf-w4-matroska_read_seek.webm](attachments/uaf-w4-matroska_read_seek.webm) (application/octet-stream, 94.0 KB)
- [uaf-w4-matroska_read_seek.html](attachments/uaf-w4-matroska_read_seek.html) (text/html, 73 B)

## Timeline

### in...@chromium.org (2014-10-26)

Feel so good to have you back Aki. Thanks for the bug.

### cl...@chromium.org (2014-10-26)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5742749755113472

### in...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5742749755113472

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x61400008fd74
Crash State:
  matroska_read_seek
  av_seek_frame
  void base::internal::ReturnAsParamAdapter<int>
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=107432:107524

Minimized Testcase (91.30 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96BEBwfNgYtp7NFRW6PdUxsHTwbr2hLLAZJXIw4kphk2mpi2E5kbknHrbD8mufQIfwWsNNFG4sWgu43cOV4K12QCqD7xXCWp2BS57RkOAcZCsidTsL4uIfyYUSickfqTPYJwvF72KPskU9kA02ZwYZoRWO_BAYJoBV50clFF2a-iSdADeA



### cl...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5742749755113472

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x61400008fd74
Crash State:
  matroska_read_seek
  av_seek_frame
  void base::internal::ReturnAsParamAdapter<int>
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=107432:107524

Minimized Testcase (91.30 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96BEBwfNgYtp7NFRW6PdUxsHTwbr2hLLAZJXIw4kphk2mpi2E5kbknHrbD8mufQIfwWsNNFG4sWgu43cOV4K12QCqD7xXCWp2BS57RkOAcZCsidTsL4uIfyYUSickfqTPYJwvF72KPskU9kA02ZwYZoRWO_BAYJoBV50clFF2a-iSdADeA



### da...@chromium.org (2014-10-27)

Xiaohan can you see if this is fixed in the upcoming roll?

### xh...@chromium.org (2014-10-27)

[Empty comment from Monorail migration]

### xh...@chromium.org (2014-10-27)

Thanks for reminding. I'll keep an eye.

### cl...@chromium.org (2014-11-04)

xhwang@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### xh...@chromium.org (2014-11-06)

[Empty comment from Monorail migration]

### xh...@chromium.org (2014-11-06)

With the latest ffmpeg [1] I can still repro this crash.

[1]
commit f05855414ed4cce97c06ba2a31f4987af47e6d4e
Author: Carl Eugen Hoyos <cehoyos@ag.or.at>
Date:   Wed Oct 29 16:27:04 2014


### bu...@chromium.org (2014-11-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/25eeccf24ff44b010f12879c57979d89bc9ee820

commit 25eeccf24ff44b010f12879c57979d89bc9ee820
Author: xhwang <xhwang@chromium.org>
Date: Fri Nov 07 01:50:46 2014

Roll FFmpeg DEPS.

This includes two bug fixes.

BUG=419060,427266

Review URL: https://codereview.chromium.org/705193002

Cr-Commit-Position: refs/heads/master@{#303160}

[modify] https://chromium.googlesource.com/chromium/src.git/+/25eeccf24ff44b010f12879c57979d89bc9ee820/DEPS


### xh...@chromium.org (2014-11-07)

Fixed by https://gerrit.chromium.org/gerrit/72102

### cl...@chromium.org (2014-11-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-08)

ClusterFuzz has detected this issue as fixed in range 303095:303227.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5742749755113472

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x61400008fd74
Crash State:
  matroska_read_seek
  av_seek_frame
  void base::internal::ReturnAsParamAdapter<int>
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=107432:107524
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=303095:303227

Minimized Testcase (91.30 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96BEBwfNgYtp7NFRW6PdUxsHTwbr2hLLAZJXIw4kphk2mpi2E5kbknHrbD8mufQIfwWsNNFG4sWgu43cOV4K12QCqD7xXCWp2BS57RkOAcZCsidTsL4uIfyYUSickfqTPYJwvF72KPskU9kA02ZwYZoRWO_BAYJoBV50clFF2a-iSdADeA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### xh...@chromium.org (2014-11-13)

This has been in the trunk for a few days and it's confirmed by ClusterFuzz. Request to merge to M39.

### cl...@chromium.org (2014-11-13)

[Empty comment from Monorail migration]

### xh...@chromium.org (2014-11-13)

For the record, this has been upstreamed to FFmpeg: https://ffmpeg.org/pipermail/ffmpeg-devel/2014-November/165067.html

### [Deleted User] (2014-11-14)

Merge approved for 40.

### xh...@chromium.org (2014-11-14)

matthewyuan: The fix was landed before the branch cut so it's already in M40. I was requesting merge to M39. What do you think of that?

### ma...@google.com (2014-11-15)

Alex is the person you should ask.  +amineer.

### xh...@chromium.org (2014-11-18)

amineer: Kindly ping?

### am...@chromium.org (2014-11-18)

+mbarbella@ from the security team.  M39 has already been released to stable (the merge request came after stable candidate was cut by a few days) and I don't plan to take anything that isn't critical.  Martin, do we need this in M39, or can we wait until M40?


### mb...@chromium.org (2014-11-18)

This looks like it would be worth including, especially since the roll also includes the fix for https://crbug.com/chromium/419060.

### xh...@chromium.org (2014-11-18)

To fix merge the fixes to M39, I need roll the DEPS for FFmpeg, which will bring the following CLs. Ignore the "Merge ...." Cls, which are empty. Then we only have a few minor changes, so the risk is small.

Note that this roll will also fix https://crbug.com/chromium/419060.

* | | |   399d38b (old_origin/master, old_origin/HEAD) Merge "avcodec/vorbisdec: Fix off by 1 error in ptns_to_read"
|\ \ \ \
| * | | | d4608b7 avcodec/vorbisdec: Fix off by 1 error in ptns_to_read
* | | | |   48401be Merge "Fix read-after-free in matroska_read_seek()."
|\ \ \ \ \
| |/ / / /
| * | | | 45a523e Fix read-after-free in matroska_read_seek().
| |/ / /
* | | |   a632b75 Merge "Update README.chromium with additional details."
|\ \ \ \
| * | | | 19e113d Update README.chromium with additional details.
* | | | | dfda919 Include version number when building ffmpegsumo.dll
| |/ / /
|/| | |
* | | | 4bc3dc1 (old_origin/merge-m40) avformat/os_support: Add _DEFAULT_SOURCE to hide warning about _SVID_SOURCE depreciation
* | | | eca71c3 Add linux-noasm configs for ChromiumOS, ChromeOS.
* | | | a6b106c Fix os_config of ffmpeg_options.gni for ChromeOS.
* | | | 438ff61 Update config files for MIPS Linux


### xh...@chromium.org (2014-11-18)

For the record, the current M39 branch is at:

438ff61 Update config files for MIPS Linux

### am...@chromium.org (2014-12-03)

I don't want to roll this many changes - removing merge approval for now.  timwillis@, can we punt to M40?  xhwang@, how viable is branching and cherry-picking?

### da...@chromium.org (2014-12-03)

Those are all harmless changes plus two security fixes.  If there are any problems with a merge the branch just won't compile (though the listed ones should be fine).

### am...@chromium.org (2014-12-03)

spoke with dale, merge is approved for m39 branch 2171.  please roll deps by tomorrow evening PST.

### [Deleted User] (2014-12-10)

Since issue does not relate to 40.  I will remove the 40 label.

### xh...@chromium.org (2014-12-10)

For the record:

This was fixed in M40 per #14 and verified on M40 per #17.

The fix was also merged to M39 in https://codereview.chromium.org/755623005/, but I don't know why this issue wasn't updated with that.

### in...@chromium.org (2014-12-15)

We might not have another m39 roll. Will just pickup in M40.

### ti...@google.com (2015-01-22)

Congratulations - $2000 for this report! Notes from reward panel: "$2000 as no control between use and free".

We've credited you in the release notes as "aohelin" - let me know if you want to use a different name/handle. 

Someone should be in touch within a few weeks to arrange payment.

### ao...@gmail.com (2015-01-23)

Awesome, thanks :)

"Aki Helin of OUSPG" is how I've been usually been credited as.

### ti...@google.com (2015-01-23)

Cool - updated with your usual name: http://googlechromereleases.blogspot.com/2015/01/stable-update.html

### cl...@chromium.org (2015-02-13)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-15)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### ti...@google.com (2015-04-15)

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

This issue was migrated from crbug.com/chromium/427266?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/426560]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080720)*
