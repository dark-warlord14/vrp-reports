# Security: Out-of-bounds write in ChunkDemuxer (TRUN box)

| Field | Value |
|-------|-------|
| **Issue ID** | [40086452](https://issues.chromium.org/issues/40086452) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Video |
| **CVE IDs** | CVE-2017-5037 |
| **Reporter** | wy...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2017-01-10 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

After reading the source code of Chrome(Android), I find Chrome do some check with video by FFmpegDemuxer and ChunkDemuxer.

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

When playing video by Media Source Extentions(MSE), chrome will call ChunkDemuxer to parse video file.

ChunkDemuxer provide some media formats, such as <https://cs.chromium.org/chromium/src/media/formats/>.

When parsing 'TRUN' box of MP4 in file box\_definitions.cc, integer overflow happens.

```
https://cs.chromium.org/chromium/src/media/formats/mp4/box_definitions.cc  

bool TrackFragmentRun::Parse(BoxReader\* reader)  
{  
	//...  
	RCHECK(reader->ReadFullBoxHeader() &&  
	         reader->Read4(&sample_count));  
	  
	//...  
	int fields = sample_duration_present + sample_size_present +  
	      sample_flags_present + sample_composition_time_offsets_present;  
	RCHECK(reader->HasBytes(fields \* sample_count));  

	if (sample_duration_present)  
	    sample_durations.resize(sample_count);  
	if (sample_size_present)  
	    sample_sizes.resize(sample_count);  
	if (sample_flags_present)  
	    sample_flags.resize(sample_count);  
	if (sample_composition_time_offsets_present)  
	    sample_composition_time_offsets.resize(sample_count);  

	//...  
}  

```

sample\_count is read from mp4 file, which is between 0x0 and 0xffffffff. And fields can be 0, 1, 2, 3, 4. So fields \* sample\_count can be overflow, and bypass the reader->HasBytes RCHECK.

What's more, sample\_durations is defined as std::vector<uint32\_t> sample\_durations;, sample\_durations.resize(sample\_count) will malloc sample\_count \* sizeof(uint32\_t) bytes, this will also overflow, leading to out-of-bounds write.

**VERSION**  

Chrome Version: [55.0.2883.91] + [stable]  

Operating System: [Android OS, 6.0.1, Nexus 6P]

**REPRODUCTION CASE**  

PoC is attached as follow.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tag]  

Crash State:  

rogram received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 25730]  

0x76f27faa in std::\_\_ndk1::vector<unsigned int, std::\_\_ndk1::allocator<unsigned int> >::\_\_append(unsigned int) ()  

from /home/ubuntu/ext/Android/NDK/my-ndk-tool-arm/bin/debug\_chrome/lib/libchrome.so  

(gdb) i r  

r0 0x7bddf510 2078143760  

r1 0x0 0  

r2 0x7fffcd46 2147470662  

r3 0x7bdec000 2078195712  

r4 0x7ba47a44 2074376772  

r5 0x7bddf510 2078143760  

r6 0x80000002 2147483650  

r7 0x7bddf518 2078143768  

r8 0x1 1  

r9 0x0 0  

r10 0x0 0  

r11 0x7d804000 2105556992  

r12 0x1 1  

sp 0x7590a050 0x7590a050  

lr 0x4010fe6b 1074855531  

pc 0x76f27faa 0x76f27faa <std::\_\_ndk1::vector<unsigned int, std::\_\_ndk1::allocator<unsigned int> >::\_\_append(unsigned int)+102>  

cpsr 0x280d0030 671940656

PATCH:  

--- box\_definitions\_a.cc 2017-01-10 14:53:55.000000000 +0800  

+++ box\_definitions\_b.cc 2017-01-10 14:59:10.000000000 +0800  

@@ -1122,15 +1122,20 @@

```
   int fields = sample_duration_present + sample_size_present +  
       sample_flags_present + sample_composition_time_offsets_present;  
+  RCHECK(((sample_count \* fields) / fields) == sample_count);  
   RCHECK(reader->HasBytes(fields \* sample_count));  
   
   if (sample_duration_present)  
+    RCHECK(((sample_count \* sizeof(uint32_t)) / sizeof(uint32_t)) == sample_count);  
     sample_durations.resize(sample_count);  
   if (sample_size_present)  
+    RCHECK(((sample_count \* sizeof(uint32_t)) / sizeof(uint32_t)) == sample_count);  
     sample_sizes.resize(sample_count);  
   if (sample_flags_present)  
+    RCHECK(((sample_count \* sizeof(uint32_t)) / sizeof(uint32_t)) == sample_count);  
     sample_flags.resize(sample_count);  
   if (sample_composition_time_offsets_present)  
+    RCHECK(((sample_count \* sizeof(uint32_t)) / sizeof(uint32_t)) == sample_count);  
     sample_composition_time_offsets.resize(sample_count);  
   
   for (uint32_t i = 0; i < sample_count; ++i) {  

```

## Attachments

- [PoC.zip](attachments/PoC.zip) (application/octet-stream, 4.8 MB)
- [patch.diff](attachments/patch.diff) (application/octet-stream, 1.1 KB)

## Timeline

### cl...@chromium.org (2017-01-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6336757240168448

### ke...@chromium.org (2017-01-17)

chcunningham@chromium.org please take a look or assign this to someone who can. Thanks.

[Monorail components: Blink>Media>Video]

### ke...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Media>Video Internals>Media>Video]

### in...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-01-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6331331421405184

### ch...@chromium.org (2017-01-18)

Thanks for reporting. Will have a patch out shortly. 

> sample_count is read from mp4 file, which is between 0x0 and 0xffffffff. And fields can be 0, 1, 2, 3, 4. So fields * sample_count can be overflow, and bypass the reader->HasBytes RCHECK.

I am definitely observing this.

> What's more, sample_durations is defined as std::vector<uint32_t> sample_durations;, sample_durations.resize(sample_count) will malloc sample_count * sizeof(uint32_t) bytes, this will also overflow, leading to out-of-bounds write. 

I observe the crash on Android. I'm not c++ savvy enough to confirm its OOB, but seems plausible. The crash is triggered by sample_durations.resize(2147483650), ultimately crashing deep in ndk/stl code on a line with a "placement" call to new.

Misc notes:
On 32bit linux we see the crash on the same resize(), but caused by uncaught 'std::length_error'.
On 64bit linux we just hit OOM trying to do the resize (new size is otherwise valid) and the process is killed.

### wy...@gmail.com (2017-01-18)

Yes, you are right. 
During my testing, I also find out this issue only exits on Android. And the crash reason is that the argument of resize() call is too big.

### ch...@chromium.org (2017-01-18)

Patch is here. https://codereview.chromium.org/2643573003

May fix other issues in that same review... will ask reviewers. 


### bu...@chromium.org (2017-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/24f5635bb25006c6ac263c47e64c8b1cfa0b0f7a

commit 24f5635bb25006c6ac263c47e64c8b1cfa0b0f7a
Author: chcunningham <chcunningham@chromium.org>
Date: Wed Jan 18 22:53:52 2017

MSE: Fix Mp4 TRUN parsing overflow

TrackFragmentRun::Parse
sample_count can take any value between 0x0 and 0xffffffff. We must
check for size_t overflow when multiplying sample_count by "fields".
We should also avoid attempting to resize vectors beyond their
max_size() (potential OOB depending on stl library impl).

BUG=679640,
TEST=unit test, manual verification of POC.

Review-Url: https://codereview.chromium.org/2643573003
Cr-Commit-Position: refs/heads/master@{#444524}

[modify] https://crrev.com/24f5635bb25006c6ac263c47e64c8b1cfa0b0f7a/media/formats/mp4/box_definitions.cc
[modify] https://crrev.com/24f5635bb25006c6ac263c47e64c8b1cfa0b0f7a/media/formats/mp4/box_reader_unittest.cc


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

### wy...@gmail.com (2017-02-14)

[Comment Deleted]

### wy...@gmail.com (2017-02-14)

[Comment Deleted]

### wy...@gmail.com (2017-02-22)

[Comment Deleted]

### aw...@chromium.org (2017-02-22)

Hi wykcomputer@ - sorry, only just saw this. I'll take a look and get back to you shortly.

### wy...@gmail.com (2017-02-28)

[Comment Deleted]

### aw...@chromium.org (2017-02-28)

Hello - we've queued this up for discussion at the next VRP panel.  It might take a few weeks but it means the if there are any changes to amounts it can be made at the same time.  Cheers!

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### wy...@gmail.com (2017-03-10)

Hello, I find only one CVE number(CVE-2017-5037) for https://crbug.com/chromium/679640.
But why no CVE numbers for issue(679653,679647,679646,679645,679641)???

release here:
https://chromereleases.googleblog.com/2017/03/stable-channel-update-for-desktop.html

### wy...@gmail.com (2017-03-14)

[Comment Deleted]

### aw...@google.com (2017-03-15)

Hello wykcomputer@.  After reviewing the Mitre CVE counting rules, I have issued CVEs for the remaining issues, the bugs are now updated. (Note that the reward payments are still in review per your request, sorry that's taking a while)

### wy...@gmail.com (2017-03-16)

OK. Thanks, will you update the following security bulletin, or on the next release? 
https://chromereleases.googleblog.com/2017/03/stable-channel-update-for-desktop.html

### aw...@google.com (2017-04-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/679640?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086452)*
