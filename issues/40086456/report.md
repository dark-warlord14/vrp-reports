# Out-of-bounds write in ChunkDemuxer (ELST box)

| Field | Value |
|-------|-------|
| **Issue ID** | [40086456](https://issues.chromium.org/issues/40086456) |
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

When parsing 'ELST' box of MP4 in file box\_definitions.cc, integer overflow happens.

```
https://cs.chromium.org/chromium/src/media/formats/mp4/box_definitions.cc  

bool EditList::Parse(BoxReader\* reader) {  
  uint32_t count;  
  RCHECK(reader->ReadFullBoxHeader() && reader->Read4(&count));  

  if (reader->version() == 1) {  
    RCHECK(reader->HasBytes(count \* 20));  
  } else {  
    RCHECK(reader->HasBytes(count \* 12));  
  }  
  edits.resize(count);  

  for (std::vector<EditListEntry>::iterator edit = edits.begin();  
       edit != edits.end(); ++edit) {  
    if (reader->version() == 1) {  
      RCHECK(reader->Read8(&edit->segment_duration) &&  
             reader->Read8s(&edit->media_time));  
    } else {  
      RCHECK(reader->Read4Into8(&edit->segment_duration) &&  
             reader->Read4sInto8s(&edit->media_time));  
    }  
    RCHECK(reader->Read2s(&edit->media_rate_integer) &&  
           reader->Read2s(&edit->media_rate_fraction));  
  }  
  return true;  
}  

```

count is read from mp4 file, which is between 0x0 and 0xffffffff. when reader->version() == 1, count \* 20 will integer overflow, which bypass reader->HasBytes RCHECK.  

What's more, edits is defined as std::vector<EditListEntry> edits;, edits.resize(count); will malloc count \* sizeof(EditListEntry) bytes, this will also overflow, leading to out-of-bounds write.

**VERSION**  

Chrome Version: [55.0.2883.91] + [stable]  

Operating System: [Android OS, 6.0.1, Nexus 6P]

**REPRODUCTION CASE**  

PoC is attached as follow.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tag]  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 28739]  

0x40121108 in memset () from /home/ubuntu/ext/Android/NDK/my-ndk-tool-arm/bin/debug\_nexus5\_4.4.0\_chrome/lib/libc.so  

(gdb) bt  

#0 0x40121108 in memset () from /home/ubuntu/ext/Android/NDK/my-ndk-tool-arm/bin/debug\_nexus5\_4.4.0\_chrome/lib/libc.so  

#1 0x7788607c in ?? () from /home/ubuntu/ext/Android/NDK/my-ndk-tool-arm/bin/debug\_nexus5\_4.4.0\_chrome/lib/libchrome.so  

Backtrace stopped: previous frame identical to this frame (corrupt stack?)  

(gdb) i r  

r0 0x76b37ff8 1991475192  

r1 0x0 0  

r2 0x18 24  

r3 0x76df3d25 1994341669  

r4 0x7a88dac0 2055789248  

r5 0x7ffff19f 2147479967  

r6 0x76b226c8 1991386824  

r7 0x76b226e0 1991386848  

r8 0x76b37ff8 1991475192  

r9 0x76b2d890 1991432336  

r10 0x0 0  

r11 0x31804000 830488576  

r12 0x796ffa74 2037381748  

sp 0x75909d6c 0x75909d6c  

lr 0x7788607d 2005426301  

pc 0x40121108 0x40121108 <memset+44>  

cpsr 0x80d0010 135069712

PATCH:  

--- box\_definitions\_a.cc 2017-01-10 14:53:55.000000000 +0800  

+++ box\_definitions\_b.cc 2017-01-10 15:13:42.000000000 +0800  

@@ -473,10 +473,13 @@  

RCHECK(reader->ReadFullBoxHeader() && reader->Read4(&count));

```
   if (reader->version() == 1) {  
+    RCHECK(((count \* 20) / 20) == count);  
     RCHECK(reader->HasBytes(count \* 20));  
   } else {  
+    RCHECK(((count \* 12) / 12) == count);  
     RCHECK(reader->HasBytes(count \* 12));  
   }  
+  RCHECK(((count \* sizeof(EditListEntry)) / sizeof(EditListEntry)) == count);  
   edits.resize(count);  
   
   for (std::vector<EditListEntry>::iterator edit = edits.begin();  

```

## Attachments

- [PoC.zip](attachments/PoC.zip) (application/octet-stream, 4.8 MB)
- [patch.diff](attachments/patch.diff) (application/octet-stream, 605 B)

## Timeline

### ke...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

[Monorail components: Internals>Media>Video]

### in...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### ch...@chromium.org (2017-01-18)

Confirmed crash. Same observations as https://bugs.chromium.org/p/chromium/issues/detail?id=679640#c6

Patch out shortly.

### bu...@chromium.org (2017-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d5e2e152b550e4fbfff9b08e7bdf7c9d4c937438

commit d5e2e152b550e4fbfff9b08e7bdf7c9d4c937438
Author: chcunningham <chcunningham@chromium.org>
Date: Fri Jan 20 01:48:24 2017

MSE: Fix moar mp4 parsing security bugs.

Boxes with various sub-entries read the entry count from the user
provided mp4. Do not trust the counts. Check for size_t and vector
resize() overflow to avoid OOB writes in vector allocation.

Additionally, verify we have enough bytes to continue parsing before
allocating vectors to store parsed data.

Also evaluated other box_definition.cc vector resize() calls. Added
one additional check for SampleEncryptionEntry (probably overkill).

BUG=679645,679646,679647,679653
TEST=Verified POCs no longer crash. New unit tests.

Review-Url: https://codereview.chromium.org/2643123002
Cr-Commit-Position: refs/heads/master@{#444935}

[modify] https://crrev.com/d5e2e152b550e4fbfff9b08e7bdf7c9d4c937438/media/formats/mp4/box_definitions.cc
[modify] https://crrev.com/d5e2e152b550e4fbfff9b08e7bdf7c9d4c937438/media/formats/mp4/box_reader_unittest.cc


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

### aw...@google.com (2017-03-15)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/679645?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086456)*
