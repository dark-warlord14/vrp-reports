# Security: Out-of-bounds write in ChunkDemuxer (SAIO box)

| Field | Value |
|-------|-------|
| **Issue ID** | [40086453](https://issues.chromium.org/issues/40086453) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Video |
| **Reporter** | wy...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2017-01-10 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Integer overflow happens in ChunkDemuxer of Chrome(Android), leading to Out-of-bounds Write.

FFmpegDemuxer and ChunkDemuxer in Chrome.

<https://cs.chromium.org/chromium/src/media/blink/webmediaplayer_impl.cc?dr=CSs&sq=package:chromium&rcl=1484007841&l=1643>

```
void WebMediaPlayerImpl::StartPipeline() {  
	//...  

	#if !defined(MEDIA_DISABLE_FFMPEG)  
	    Demuxer::MediaTracksUpdatedCB media_tracks_updated_cb =  
	        BIND_TO_RENDER_LOOP(&WebMediaPlayerImpl::OnFFmpegMediaTracksUpdated);  

	    demuxer_.reset(new FFmpegDemuxer(media_task_runner_, data_source_.get(),  
	                                     encrypted_media_init_data_cb,  
	                                     media_tracks_updated_cb, media_log_));  
	#else  
	    OnError(PipelineStatus::DEMUXER_ERROR_COULD_NOT_OPEN);  
	    return;  
	#endif  
	} else {  
	  DCHECK(!chunk_demuxer_);  
	  DCHECK(!data_source_);  

	  chunk_demuxer_ = new ChunkDemuxer(  
	      BIND_TO_RENDER_LOOP(&WebMediaPlayerImpl::OnDemuxerOpened),  
	      encrypted_media_init_data_cb, media_log_);  
	  demuxer_.reset(chunk_demuxer_);  
	}  

	//...  
}  

```

When playing video by Media Source Extentions(MSE), chrome will call ChunkDemuxer to parse video.

ChunkDemuxer provide some media formats, such as <https://cs.chromium.org/chromium/src/media/formats/>.

When parsing 'SAIO' box of MP4 in file box\_definitions.cc, integer overflow happens.

```
https://cs.chromium.org/chromium/src/media/formats/mp4/box_definitions.cc  

bool SampleAuxiliaryInformationOffset::Parse(BoxReader\* reader) {  
  RCHECK(reader->ReadFullBoxHeader());  
  if (reader->flags() & 1)  
    RCHECK(reader->SkipBytes(8));  

  uint32_t count;  
  RCHECK(reader->Read4(&count) &&  
         reader->HasBytes(count \* (reader->version() == 1 ? 8 : 4)));  
  offsets.resize(count);  

  for (uint32_t i = 0; i < count; i++) {  
    if (reader->version() == 1) {  
      RCHECK(reader->Read8(&offsets[i]));  
    } else {  
      RCHECK(reader->Read4Into8(&offsets[i]));  
    }  
  }  
  return true;  
}  

```

count is read from mp4 file, which is between 0x0 and 0xffffffff. when reader->version() == 1, count \* 8 will integer overflow, which bypass reader->HasBytes RCHECK.  

What's more, offsets is defined as std::vector<uint64\_t> offsets;, offsets.resize(count) will malloc count \* sizeof(uint64\_t) bytes, this will also overflow, leading to out-of-bounds write.

**VERSION**  

Chrome Version: [55.0.2883.91] + [stable]  

Operating System: [Android OS, 6.0.1, Nexus 6P]

**REPRODUCTION CASE**  

PoC is attached as follow.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tag]  

Crash State:  

(gdb) bt  

#0 0x776964b8 in std::\_\_ndk1::vector<unsigned long long, std::\_\_ndk1::allocator<unsigned long long> >::\_\_append(unsigned int) ()  

from /home/ubuntu/ext/Android/NDK/my-ndk-tool-arm/bin/debug\_chrome/lib/libchrome.so  

#1 0x77885ef0 in ?? () from /home/ubuntu/ext/Android/NDK/my-ndk-tool-arm/bin/debug\_chrome/lib/libchrome.so  

Backtrace stopped: previous frame identical to this frame (corrupt stack?)  

(gdb) i r  

r0 0x7aa33060 2057515104  

r1 0x8 8  

r2 0x3fff660d 1073702413  

r3 0x7aa80000 2057830400  

r4 0x7b21c5ec 2065810924  

r5 0x7aa33060 2057515104  

r6 0x40000001 1073741825  

r7 0x7aa33068 2057515112  

r8 0x798e1dd8 2039356888  

r9 0x7abf43b8 2059355064  

r10 0x0 0  

r11 0x7ce04000 2095071232  

r12 0x1 1  

sp 0x7590d078 0x7590d078  

lr 0x4010fe6b 1074855531  

pc 0x776964b8 0x776964b8 <std::\_\_ndk1::vector<unsigned long long, std::\_\_ndk1::allocator<unsigned long long> >::\_\_append(unsigned int)+108>  

cpsr 0x280d0030 671940656

PATCH:  

--- box\_definitions\_a.cc 2017-01-10 14:53:55.000000000 +0800  

+++ box\_definitions\_b.cc 2017-01-10 15:07:55.000000000 +0800  

@@ -123,8 +123,12 @@  

RCHECK(reader->SkipBytes(8));

```
   uint32_t count;  
-  RCHECK(reader->Read4(&count) &&  
-         reader->HasBytes(count \* (reader->version() == 1 ? 8 : 4)));  
+  RCHECK(reader->Read4(&count));  
+  uint32_t version = (reader->version() == 1 ? 8 : 4);  
+  RCHECK(((count \* version) / version) == count);  
+  RCHECK(reader->HasBytes(count \* version));  
+    
+  RCHECK(((count \* sizeof(uint64_t)) / sizeof(uint64_t)) == count);  
   offsets.resize(count);  
   
   for (uint32_t i = 0; i < count; i++) {

```

## Attachments

- [PoC.zip](attachments/PoC.zip) (application/octet-stream, 4.8 MB)
- [patch.diff](attachments/patch.diff) (application/octet-stream, 635 B)

## Timeline

### ke...@chromium.org (2017-01-17)

chcunningham@chromium.org please take a look or assign this to someone who can. Thanks.

[Monorail components: Internals>Media>Video]

### in...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### ch...@chromium.org (2017-01-18)

Confirmed the crash on x86 linux and android. Same observations as https://bugs.chromium.org/p/chromium/issues/detail?id=679640#c6

Will have a patch out shortly.

### ch...@chromium.org (2017-01-18)

Patch here: https://codereview.chromium.org/2648433002

### ch...@chromium.org (2017-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5041e28550903b40c925d66f6bb5bb6a6baed15b

commit 5041e28550903b40c925d66f6bb5bb6a6baed15b
Author: chcunningham <chcunningham@chromium.org>
Date: Thu Jan 19 01:19:03 2017

MSE: Fix Mp4 SAIO parsing overflow

SampleAuxiliaryInformationOffset::Parse
count can take any value between 0x0 and 0xffffffff. We must
check for size_t overflow when multiplying count by
"bytes_per_offset". We should also avoid attempting to resize vectors
beyond their max_size() (potential OOB depending on stl library impl).

BUG=679641
TEST=unit test, manual verification of POC.

Review-Url: https://codereview.chromium.org/2648433002
Cr-Commit-Position: refs/heads/master@{#444584}

[modify] https://crrev.com/5041e28550903b40c925d66f6bb5bb6a6baed15b/media/formats/mp4/box_definitions.cc
[modify] https://crrev.com/5041e28550903b40c925d66f6bb5bb6a6baed15b/media/formats/mp4/box_reader_unittest.cc


### ch...@chromium.org (2017-01-23)

Bulk requesting merge to 56 for 
679640, 679641, 679645, 679646, 679647

Will skip merge to 55 following discussion here:
https://bugs.chromium.org/p/chromium/issues/detail?id=679653#c11

### sh...@chromium.org (2017-01-23)

This bug requires manual review: We are only 7 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), gkihumba@(cros), bustamante@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@google.com (2017-01-23)

LGTM, all the bugs are fixed with the same CL which I'm ok merging since it's fairly isolated.

### sh...@chromium.org (2017-01-24)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bcae749c7aaec4bc26e22a3acb6183dabdce2c96

commit bcae749c7aaec4bc26e22a3acb6183dabdce2c96
Author: Chris Cunningham <chcunningham@chromium.org>
Date: Tue Jan 24 22:01:02 2017

[TO 56] Fix mp4 parsing security bugs.

-- Cherry-pick notes --

This CL is a merge of the following cherry-picked commits:
d5e2e15 MSE: Fix moar mp4 parsing security bugs.
5041e28 MSE: Fix Mp4 SAIO parsing overflow
24f5635 MSE: Fix Mp4 TRUN parsing overflow

These each had conflicts due to dependency on safe_math.h functions
that are not present in this branch (base::CheckMul).

-- CL description --

Boxes with various sub-entries read the entry count from the user
provided mp4. Do not trust the counts. Check for size_t and vector
resize() overflow to avoid OOB writes in vector allocation.

Additionally, verify we have enough bytes to continue parsing before
allocating vectors to store parsed data.

Also evaluated other box_definition.cc vector resize() calls. Added
one additional check for SampleEncryptionEntry (probably overkill).

BUG=679645, 679646, 679647, 679653, 679640, 679641
TESTS=new unit tests, manual verification of PoCs
TBR=dalecurtis@chromium.org

Review-Url: https://codereview.chromium.org/2654913002 .
Cr-Commit-Position: refs/branch-heads/2924@{#857}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/bcae749c7aaec4bc26e22a3acb6183dabdce2c96/media/formats/mp4/box_definitions.cc
[modify] https://crrev.com/bcae749c7aaec4bc26e22a3acb6183dabdce2c96/media/formats/mp4/box_reader_unittest.cc


### sh...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-13)

Congratulations! The panel decided to award $1,000 each for these bugs (679653,679647,679646,679645,679641,679640)

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### wy...@gmail.com (2017-03-09)

Will a CVE number be assigned?

### aw...@google.com (2017-03-15)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@gmail.com (2017-09-10)

hi, i'm working on a paper for my last college exam i was wondering how i could reproduce this from the PoC, I'm guessing i have to change the assetURL var to the path on my pc, but when i open the html file no video starts playing

### ch...@chromium.org (2017-09-11)

I don't recall the details, but it may be that video file is just whats needed to reproduce the crash - lacking any real media content. 

### wy...@gmail.com (2017-09-12)

Hi, just opened the PoC.html file. And the bug only exites on Android Chrome, version under 55.0.2883.91

### lu...@gmail.com (2017-10-14)

yes i figured that out but i still can't manage to reproduce it on that version of chrome, i open the PoC.html with chrome on android 6.0.1 but nothing happens

### lu...@gmail.com (2017-10-16)

[Comment Deleted]

### lu...@gmail.com (2017-10-19)

can someone explain in detail this: "offsets.resize(count) will malloc count * sizeof(uint64_t) bytes, this will also overflow"

so i think the malloc comes from the resize method but why would it overflow? count is 4 bytes and sizeof(uint64_t) is 8 bytes which makes 32 bytes total allocated space. What's the max you can allocate in this particular case?


### wy...@gmail.com (2017-10-20)

count * sizeof(uint64_t), the value of 'count', not the length of 'count', the max value of count can be 0xffffffff.

### lu...@gmail.com (2017-10-20)

[Comment Deleted]

### lu...@gmail.com (2017-10-21)

offsets.resize(count) will malloc count * sizeof(uint64_t) bytes this sentence still doesn't make any sense to me why does 0xffffffff * sizeof(uint64_t) overflow? the max_size() of offsets is 2^61 and 0xffffffff * sizeof(uint64_t)  doesn't even come close to that value.

### lu...@gmail.com (2017-10-21)

better yet what is offsets.max_size() in this case ?

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/679641?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086453)*
