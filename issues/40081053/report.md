# Heap Corruption - FFMPEG libavformat\mov.c - Use-After-Free/Double Free

| Field | Value |
|-------|-------|
| **Issue ID** | [40081053](https://issues.chromium.org/issues/40081053) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | [Deleted User] |
| **Assignee** | da...@chromium.org |
| **Created** | 2014-12-22 |
| **Bounty** | $4,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2251.0 Safari/537.36

Steps to reproduce the problem:
1. Browse to sample (mov_metadata_raw_heap_corruption.m4a)
2. Refresh

What is the expected behavior?
Sample crashes within ntdll!RtlFreeHeap due to an invalid pointer.

Use-After-Free/Double Free can be achieved by corrupting the LFH UserPtr stored in the av_malloc header

static int mov_metadata_raw(MOVContext *c, AVIOContext *pb,
                            unsigned len, const char *key)
{
    char *value = av_malloc(len + 1);
    if (!value)
        return AVERROR(ENOMEM);
    avio_read(pb, value, len);
    value[len] = 0;
    return av_dict_set(&c->fc->metadata, key, value, AV_DICT_DONT_STRDUP_VAL);
}

ffmpegsumo!mov_metadata_raw:
6423ad76 55              push    ebp
6423ad77 8bec            mov     ebp,esp
6423ad79 56              push    esi
6423ad7a 57              push    edi
6423ad7b 8b7d10          mov     edi,dword ptr [ebp+10h] ss:002b:06cbf808=ffffffff
6423ad7e 8d4701          lea     eax,[edi+1]
6423ad81 50              push    eax
6423ad82 e8493e0500      call    ffmpegsumo!av_malloc (6428ebd0)
6423ad87 8bf0            mov     esi,eax
6423ad89 59              pop     ecx
6423ad8a 85f6            test    esi,esi
6423ad8c 7505            jne     ffmpegsumo!mov_metadata_raw+0x1d (6423ad93)
6423ad93 57              push    edi
6423ad94 56              push    esi
6423ad95 ff750c          push    dword ptr [ebp+0Ch]
6423ad98 e88f9e0300      call    ffmpegsumo!avio_read (64274c2c)
6423ad9d 8b4508          mov     eax,dword ptr [ebp+8]
6423ada0 6a08            push    8

eax=06355a00 ebx=04feb320 ecx=04feb320 edx=050a5930 esi=050a5940 edi=ffffffff
eip=6423ada2 esp=06cbf7e0 ebp=06cbf7f8 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000246
ffmpegsumo!mov_metadata_raw+0x2c:
6423ada2 c6043e00        mov     byte ptr [esi+edi],0       ds:002b:050a593f=05

6423ada2 c6043e00        mov     byte ptr [esi+edi],0       ds:002b:050a593f=05    <------------------------- Write null byte at offset -1
6423ada6 56              push    esi
6423ada7 8b4004          mov     eax,dword ptr [eax+4]
6423adaa ff7514          push    dword ptr [ebp+14h]
6423adad 0574040000      add     eax,474h
6423adb2 50              push    eax
6423adb3 e8e5f80400      call    ffmpegsumo!av_dict_set (6428a69d)
6423adb8 83c41c          add     esp,1Ch
6423adbb 5f              pop     edi
6423adbc 5e              pop     esi
6423adbd 5d              pop     ebp
6423adbe c3              ret

0:012> dd esi-4    
050a593c  050a5930 <----- Gets corrupted 			
                   667a5a20 06355e18 00000010
050a594c  000000c0 00000088 00000000 1893eb9e

What went wrong?
Int wrap on allocation, followed by memory corruption at offset -1. The pointer stored in the av_malloc header was corrupted.

Did this work before? N/A 

Chrome version: 41.0.2251.0  Channel: dev
OS Version: 6.3
Flash Version: Shockwave Flash 16.0 r0

## Attachments

- [mov_metadata_raw_heap_corruption.m4a](attachments/mov_metadata_raw_heap_corruption.m4a) (application/octet-stream, 1.5 KB)
- [mov_metadata_raw_fixes.patch](attachments/mov_metadata_raw_fixes.patch) (application/octet-stream, 1.0 KB)

## Timeline

### in...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-12-23)

Hey Paul, I don't see that code in ffmpeg's mov.c, as least not on the latest master branch. Any idea what happened to it?

### [Deleted User] (2014-12-23)

ffmpeg for some reason doesn't have a the source code browsable by file. You have to search for "mov.c" to find it, but you can find the code here:

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/ffmpeg/libavformat/mov.c&q=mov_metadata_raw&sq=package:chromium&type=cs&l=212

### pa...@google.com (2014-12-25)

As with the other bugs, are we sure this is Windows-only?

### cl...@chromium.org (2014-12-25)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6107751045398528

### [Deleted User] (2014-12-26)

Same mis-label, should be OS-ALL.

### cl...@chromium.org (2014-12-28)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-12-28)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-12-28)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-12-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5120346612039680

### cl...@chromium.org (2015-01-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5138117710315520

### da...@chromium.org (2015-01-06)

I sent a patch for this issue upstream based on Paul's analysis. Once upstream verifies the patches I'll land them in our repository.

### da...@chromium.org (2015-01-06)

Michael fixed this in a more appropriate position:

http://git.videolan.org/?p=ffmpeg.git;a=commit;h=3859868c75313e318ebc5d0d33baada62d45dd75

### in...@chromium.org (2015-01-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### da...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### da...@chromium.org (2015-01-13)

(Merge request is for M40)

### ma...@google.com (2015-01-13)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### da...@chromium.org (2015-01-13)

https://crrev.com/d6cc2ec3bf2acdcb364fda90374158641b4e73be is the commit, not sure why it didn't show up here.

### pe...@chromium.org (2015-01-14)

Merge approved for CL d6cc2ec3bf2acdcb364fda90374158641b4e73be, to M41 branch 2272.

### da...@chromium.org (2015-01-15)

This is already present in M41, it needs to be in M40. I believe we're currently waiting for the first point release.

### in...@chromium.org (2015-01-15)

[Empty comment from Monorail migration]

### da...@chromium.org (2015-01-20)

Merged to M40 with:

http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=67392

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### dx...@chromium.org (2015-02-03)

[Empty comment from Monorail migration]

### dx...@chromium.org (2015-02-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-04)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congratulations - $4000 for this report. 

Notes from reward panel: $3000 for the bug + $1000 for the clear explanation where the bug was located.

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

This issue was migrated from crbug.com/chromium/444539?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081053)*
