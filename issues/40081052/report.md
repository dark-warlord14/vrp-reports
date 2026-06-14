# Heap-buffer-overflow in ff_mov_read_stsd_entries

| Field | Value |
|-------|-------|
| **Issue ID** | [40081052](https://issues.chromium.org/issues/40081052) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | [Deleted User] |
| **Assignee** | da...@chromium.org |
| **Created** | 2014-12-22 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2251.0 Safari/537.36

Steps to reproduce the problem:
1. browse to the sample (read_tfra_heap_corruption_test.mp4)

What is the expected behavior?
Sample crashes writing to unpaged memory

6423c9d1 e817820300      call    ffmpegsumo!avio_rb32 (64274bed)
6423c9d6 33d2            xor     edx,edx
6423c9d8 8945f0          mov     dword ptr [ebp-10h],eax
6423c9db 8b45fc          mov     eax,dword ptr [ebp-4]
6423c9de 59              pop     ecx
6423c9df 59              pop     ecx
6423c9e0 8b4df8          mov     ecx,dword ptr [ebp-8]
6423c9e3 8b400c          mov     eax,dword ptr [eax+0Ch]
6423c9e6 894c3808        mov     dword ptr [eax+edi+8],ecx ds:002b:b332d008=????????
6423c9ea 8b4df4          mov     ecx,dword ptr [ebp-0Ch]
6423c9ed 894c380c        mov     dword ptr [eax+edi+0Ch],ecx
6423c9f1 8b45fc          mov     eax,dword ptr [ebp-4]
6423c9f4 8b4df0          mov     ecx,dword ptr [ebp-10h]
6423c9f7 8b400c          mov     eax,dword ptr [eax+0Ch]
6423c9fa 890c07          mov     dword ptr [edi+eax],ecx
6423c9fd 89540704        mov     dword ptr [edi+eax+4],edx
6423ca01 8b45e4          mov     eax,dword ptr [ebp-1Ch]
6423ca04 85c0            test    eax,eax
6423ca06 7e0c            jle     ffmpegsumo!read_tfra+0x1a7 (6423ca14)

static int read_tfra(MOVContext *mov, AVIOContext *f)
{
    MOVFragmentIndex* index = NULL;
    int version, fieldlength, i, j, err;
    int64_t pos = avio_tell(f);
    uint32_t size = avio_rb32(f);
    if (avio_rb32(f) != MKBETAG('t', 'f', 'r', 'a')) {
        return -1;
    }
    av_log(mov->fc, AV_LOG_VERBOSE, "found tfra\n");
    index = av_mallocz(sizeof(MOVFragmentIndex));
    if (!index) {
        return AVERROR(ENOMEM);
    }
    mov->fragment_index_count++;  // ?????? HRM ?????? increment but don't decrement on error?    -----------> Tested as a double free (given the assumption that av_reallocp() can fail
    if ((err = av_reallocp(&mov->fragment_index_data,
                           mov->fragment_index_count *
                           sizeof(MOVFragmentIndex*))) < 0) {
        av_freep(&index);
        return err;
    }
    mov->fragment_index_data[mov->fragment_index_count - 1] =
        index;

    version = avio_r8(f);
    avio_rb24(f);
    index->track_id = avio_rb32(f);
    fieldlength = avio_rb32(f);
    index->item_count = avio_rb32(f);
    index->items = av_mallocz(
            index->item_count * sizeof(MOVFragmentIndexItem));  // <------------------ int wrap
    if (!index->items) {
        return AVERROR(ENOMEM);
    }
    for (i = 0; i < index->item_count; i++) {
        int64_t time, offset;
        if (version == 1) {
            time   = avio_rb64(f);
            offset = avio_rb64(f);
        } else {
            time   = avio_rb32(f);
            offset = avio_rb32(f);
        }
        index->items[i].time = time;
        index->items[i].moof_offset = offset;
        for (j = 0; j < ((fieldlength >> 4) & 3) + 1; j++)
            avio_r8(f);
        for (j = 0; j < ((fieldlength >> 2) & 3) + 1; j++)
            avio_r8(f);
        for (j = 0; j < ((fieldlength >> 0) & 3) + 1; j++)
            avio_r8(f);
    }

    avio_seek(f, pos + size, SEEK_SET);
    return 0;
}

What went wrong?
int32 Wraps on allocation resulting in memory corruption.

  index->item_count = avio_rb32(f);
  index->items = av_mallocz(index->item_count * sizeof(MOVFragmentIndexItem));

Did this work before? N/A 

Chrome version: 41.0.2251.0  Channel: dev
OS Version: 6.3
Flash Version: Shockwave Flash 16.0 r0

This is just a brief overview. Please ask me if you have any questions.

## Attachments

- [read_tfra_heap_corruption_test.mp4](attachments/read_tfra_heap_corruption_test.mp4) (application/octet-stream, 3.0 KB)

## Timeline

### in...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-12-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-23)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5746787565436928

### cl...@chromium.org (2014-12-23)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4818227312984064

### cl...@chromium.org (2014-12-23)

[Comment Deleted]

### in...@chromium.org (2014-12-23)

[Empty comment from Monorail migration]

### pa...@google.com (2014-12-25)

Is there a particular reason to think this is Windows-only? Looks like OS-All to me?

### cl...@chromium.org (2014-12-25)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5740684416909312

### [Deleted User] (2014-12-26)

@pal: Good catch, you're right; it is OS-ALL. I'm not sure why it's labeled as OS-Windows.

### cl...@chromium.org (2014-12-28)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-12-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5157697971290112

### cl...@chromium.org (2015-01-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5635262724964352

### cl...@chromium.org (2015-01-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5157697971290112

Uploader: inferno@chromium.org
Job Type: Windows_asan_chrome_media

Crash Type: Heap-buffer-overflow WRITE 8
Crash Address: 0xb3327b58
Crash State:
  ff_mov_read_stsd_entries
  ff_mov_read_stsd_entries
  ff_mov_read_stsd_entries
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv941xehvDpva85Xqjw7EH6w_mf-4RIW4Mniwx6ZAQga8mlm9wE3PXOOFLr502URjeBXUn3sl08RAQaZ2ET7FVj0HTNOBnn1W3yJGgFR272cPyTW3G_CDwFhgSTMM7k6uDEIWrUz7j2OzODHDY5WIr_B03t8WeA




### cl...@chromium.org (2015-01-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5635262724964352

Uploader: inferno@chromium.org
Job Type: Windows_asan_chrome_media

Crash Type: Heap-buffer-overflow WRITE 8
Crash Address: 0xb3327b58
Crash State:
  ff_mov_read_stsd_entries
  ff_mov_read_stsd_entries
  ff_mov_read_stsd_entries
  

Minimized Testcase (3.02 Kb): https://cluster-fuzz.appspot.com/download/AMIfv9521dslcNnHmJpcbvziwCYvCqoBbo-Jb9bpJUbVDkNFBENZSaAlhWxbX9X1KJ2zi6ZDyXwEIyAt3mTT1e8YTbpksvg-ZO_-Nkx9U2aOAzQMwL_WfhQDLviCc7ZUmXg4XV7-TFeA2ljhbGGRIIyFQRVknc0NVw



### da...@chromium.org (2015-01-05)

Paul, have you already reported this and the other issues upstream? 

### da...@chromium.org (2015-01-06)

Fix for this here: https://code.google.com/p/chromium/issues/detail?id=444533#c21

### da...@chromium.org (2015-01-06)

Fix from upstream listed in https://code.google.com/p/chromium/issues/detail?id=444533#c22

### bu...@chromium.org (2015-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d6cc2ec3bf2acdcb364fda90374158641b4e73be

commit d6cc2ec3bf2acdcb364fda90374158641b4e73be
Author: dalecurtis <dalecurtis@chromium.org>
Date: Tue Jan 06 23:42:29 2015

Roll ffmpeg DEPs for security fixes. Add regression tests.

Pulls in the following fixes:
b9d631d avformat/utils: Clear pointer in ff_alloc_extradata() to avoid leaving a stale pointer in memory
7575fa1 avfilter/buffer: use av_freep() to avoid leaving stale pointers in memory
0aa6981 avformat/matroskadec: Use av_freep() to avoid leaving stale pointers in memory
e860c4c avformat/mov: use av_freep() to avoid leaving stale pointers in memory
c61fcd2 avformat/mov: Clear array to prevent potential out of array read from av_dlog()
a6dd29c avformat/mov: fix integer overflow in mov_read_udta_string()
878627f mov: Fix negative size calculation in mov_read_default().
c179d68 mov: Fix overflow and error handling in read_tfra().

BUG=444533,444522,444539,444546
TEST=regression tests, test cases no longer crash
TBR=scherkus

Review URL: https://codereview.chromium.org/838653002

Cr-Commit-Position: refs/heads/master@{#310173}

[modify] http://crrev.com/d6cc2ec3bf2acdcb364fda90374158641b4e73be/DEPS
[modify] http://crrev.com/d6cc2ec3bf2acdcb364fda90374158641b4e73be/media/ffmpeg/ffmpeg_regression_tests.cc


### in...@chromium.org (2015-01-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### da...@chromium.org (2015-01-13)

Merge request for m40.

### ma...@google.com (2015-01-13)

[Automated comment] Request affecting a post-stable build (M39), manual review required.

### ma...@google.com (2015-01-13)

[Automated comment] Commit may have occurred before M41 branch point (1/10/2015), needs manual review.

### ma...@google.com (2015-01-13)

[Automated comment] Less than 2 weeks to go before stable on M40, manual review required.

### pe...@chromium.org (2015-01-14)

Merge approved for CL d6cc2ec3bf2acdcb364fda90374158641b4e73be, to M41 branch 2272.

### pe...@chromium.org (2015-01-17)

[Empty comment from Monorail migration]

### pe...@google.com (2015-01-17)

[Automated comment] Request affecting a post-stable build (M39), manual review required.

### pe...@google.com (2015-01-17)

[Automated comment] Less than 2 weeks to go before stable on M40, manual review required.

### [Deleted User] (2015-01-20)

Approved for 40.  No more 39s are scheduled removing label.

### [Deleted User] (2015-01-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-20)

ClusterFuzz has detected this issue as fixed in latest custom build.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5635262724964352

Uploader: inferno@chromium.org
Job Type: Windows_asan_chrome_media

Crash Type: Heap-buffer-overflow WRITE 8
Crash Address: 0xb3327b58
Crash State:
  ff_mov_read_stsd_entries
  ff_mov_read_stsd_entries
  ff_mov_read_stsd_entries
  

Minimized Testcase (3.02 Kb): https://cluster-fuzz.appspot.com/download/AMIfv9521dslcNnHmJpcbvziwCYvCqoBbo-Jb9bpJUbVDkNFBENZSaAlhWxbX9X1KJ2zi6ZDyXwEIyAt3mTT1e8YTbpksvg-ZO_-Nkx9U2aOAzQMwL_WfhQDLviCc7ZUmXg4XV7-TFeA2ljhbGGRIIyFQRVknc0NVw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### da...@chromium.org (2015-01-20)

Merged to M40 with:

http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=67392

### dx...@chromium.org (2015-02-03)

[Empty comment from Monorail migration]

### dx...@chromium.org (2015-02-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-04)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Saving the best till last - $5000 for this report.

Notes from panel: Longstanding and readily exploitable regression. $4,000 for the bug + $1000 for the clear reproduction and analysis.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-04-15)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/444522?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081052)*
