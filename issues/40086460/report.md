# Security: Out-of-bounds write in ChunkDemuxer (SDTP box)

| Field | Value |
|-------|-------|
| **Issue ID** | [40086460](https://issues.chromium.org/issues/40086460) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Video |
| **Reporter** | wy...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2017-01-10 |
| **Bounty** | $1,000.00 |

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

When playing video by Media Source Extention, chrome will call ChunkDemuxer to parse video.

ChunkDemuxer provide some media formats, such as <https://cs.chromium.org/chromium/src/media/formats/>.

When parsing 'SDTP' box of MP4 in file box\_definitions.cc, integer overflow happens.

```
https://cs.chromium.org/chromium/src/media/formats/mp4/box_definitions.cc  

bool IndependentAndDisposableSamples::Parse(BoxReader\* reader) {  
  RCHECK(reader->ReadFullBoxHeader());  
  RCHECK(reader->version() == 0);  
  RCHECK(reader->flags() == 0);  

  int sample_count = reader->box_size() - reader->pos();  
  sample_depends_on_.resize(sample_count);  
  for (int i = 0; i < sample_count; ++i) {  
    uint8_t sample_info;  
    RCHECK(reader->Read1(&sample_info));  

    sample_depends_on_[i] =  
        static_cast<SampleDependsOn>((sample_info >> 4) & 0x3);  

    RCHECK(sample_depends_on_[i] != kSampleDependsOnReserved);  
  }  

  return true;  
}  

```

sample\_count is from mp4 file, which is between 0x0 and 0xffffffff.  

sample\_depends\_on\_ is defined as std::vector<SampleDependsOn> sample\_depends\_on\_;, sample\_depends\_on\_.resize(sample\_count); will malloc sample\_count \* sizeof(SampleDependsOn) bytes, this will also overflow, leading to out-of-bounds write.

Because SDTP is in encrypted video, playing encrypted video requires deploying a whole system using Encrypted Media Extensions(EME). So I will not provide a PoC file, just patch file.

PATCH:  

--- box\_definitions\_a.cc 2017-01-10 14:53:55.000000000 +0800  

+++ box\_definitions\_b.cc 2017-01-10 16:15:11.000000000 +0800  

@@ -1326,6 +1326,7 @@  

RCHECK(reader->flags() == 0);

```
   int sample_count = reader->box_size() - reader->pos();  
+  RCHECK(((sample_count \* sizeof(SampleDependsOn)) / sizeof(SampleDependsOn)) == sample_count);  
   sample_depends_on_.resize(sample_count);  
   for (int i = 0; i < sample_count; ++i) {  
     uint8_t sample_info;  

```

## Attachments

- deleted (application/octet-stream, 0 B)
- [patch.diff](attachments/patch.diff) (application/octet-stream, 448 B)

## Timeline

### wy...@gmail.com (2017-01-10)

[Empty comment from Monorail migration]

### wy...@gmail.com (2017-01-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

[Monorail components: Internals>Media>Video]

### in...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### ch...@chromium.org (2017-01-19)

Unlike the other bugs (e.g. https://crbug.com/chromium/679647), I am not able to write a unit test to verify this and suspect it may not actually be possible to trigger the overflow.

The struggle is how to make sample_count large enough that sample_count * sizeof(SampleDependsOn) will overflow 32bits. sizeof(SampleDependsOn) == 4, so to overflow the sample_count must be >= 1,073,741,824... or ~1GB. Because sample_count is computed as box_size - pos_, this means box_size must also be roughly 1GB. 

MSE SourceBuffer code does not allow a box of this size to be appended. SourceBuffer will attempt to make room for the append, but will throw a QUOTA_EXCEEDED [0] exception and abort. The current maximum bytes for any one source buffer is 150MB [1][2].


The next thought is, what if we just append the first few bytes of a box that claims to have the massive 1GB box size. This is possible, but in such a case we will abort while parsing the box header when we observe the box_size > the appended buffer_size [4]. This abort occurs before any vectors are allocated.

Still, it is probably best not to rely on this external append size protection forever. I will go ahead and add a guard to IndependentAndDisposableSamples::Parse to ensure we do not allow this vector resize to cause overflows down the road. 

[0] https://cs.chromium.org/chromium/src/third_party/WebKit/Source/modules/mediasource/SourceBuffer.cpp?rcl=1484842630&l=1109
[1] https://cs.chromium.org/chromium/src/media/filters/source_buffer_stream.cc?rcl=1484842630&l=695
[2] https://cs.chromium.org/chromium/src/media/filters/source_buffer_platform.cc?rcl=1484842630&l=12
[4] https://cs.chromium.org/chromium/src/media/formats/mp4/box_reader.cc?rcl=0&l=293

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

I notice the milestone is M-55? Would we want to ship a release update just for these, or is the idea to merge to 55 in case an update goes out? 

Requesting merge to 55 and 56. This and related changes made the cut for 57.

### sh...@chromium.org (2017-01-23)

This bug requires manual review: We are only 7 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), gkihumba@(cros), bustamante@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-01-23)

We are not planning any further M55 stable releases.

### ch...@chromium.org (2017-01-23)

Ok, sounds good for 55. 

Heads up: I'll request merge 56 for other related bugs (this came in with a burst of 5 other externally reported security bugs in very similar code paths).

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

### sh...@chromium.org (2017-05-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/679653?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086460)*
