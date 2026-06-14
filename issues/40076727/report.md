# Heap-buffer-overflow in matroska_parse_block

| Field | Value |
|-------|-------|
| **Issue ID** | [40076727](https://issues.chromium.org/issues/40076727) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, Internals>Media>FFmpeg |
| **Reporter** | at...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-12-20 |
| **Bounty** | $500.00 |

## Description

Repro-file as attachment.

Tested on: 

OS: Ubuntu 12.04
Chromium: ASAN 26.0.1366.0 (Developer Build 173978)


ASAN-report:

==28572== ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7fb3df11a579 at pc 0x7fb3de89b04c bp 0x7fb3d885ad70 sp 0x7fb3d885ad68
READ of size 1 at 0x7fb3df11a579 thread T5 (FFmpegDemuxer)
    #0 0x7fb3de89b04b in matroska_parse_block ../../third_party/ffmpeg/libavformat/matroskadec.c:0
    #1 0x7fb3de898e4a in matroska_parse_cluster ../../third_party/ffmpeg/libavformat/matroskadec.c:0
    #2 0x7fb3de896785 in matroska_read_packet ../../third_party/ffmpeg/libavformat/matroskadec.c:0
    #3 0x7fb3de8bcac9 in ff_read_packet ??:0
    #4 0x7fb3de8bf130 in read_frame_internal ../../third_party/ffmpeg/libavformat/utils.c:0
    #5 0x7fb3de8be644 in av_read_frame ??:0
    #6 0x7fb3f12c895d in void base::internal::ReturnAsParamAdapter<int>(base::Callback<int ()> const&, int*) ???:0
    #7 0x7fb3ecec0047 in base::(anonymous namespace)::PostTaskAndReplyRelay::Run() ../../base/threading/post_task_and_reply_impl.cc:0
    #8 0x7fb3ece3f1a3 in MessageLoop::RunTask(base::PendingTask const&) ???:0
.
.
.
0x7fb3df11a579 is located 0 bytes to the right of 313-byte region [0x7fb3df11a440,0x7fb3df11a579)
allocated by thread T5 (FFmpegDemuxer) here:
    #0 0x7fb3eaf46eaa in posix_memalign ??:0
    #1 0x7fb3de8fa2f7 in av_malloc ??:0
    #2 0x7fb3de89bf88 in ebml_parse_id ../../third_party/ffmpeg/libavformat/matroskadec.c:0
    #3 0x7fb3de89c103 in ebml_parse_id ../../third_party/ffmpeg/libavformat/matroskadec.c:0
    #4 0x7fb3de898738 in matroska_parse_cluster ../../third_party/ffmpeg/libavformat/matroskadec.c:0
    #5 0x7fb3de896785 in matroska_read_packet ../../third_party/ffmpeg/libavformat/matroskadec.c:0
    #6 0x7fb3de8bcac9 in ff_read_packet ??:0
    #7 0x7fb3de8bf130 in read_frame_internal ../../third_party/ffmpeg/libavformat/utils.c:0
    #8 0x7fb3de8be644 in av_read_frame ??:0
.
.
.


## Attachments

- [chrome-heap-buffer-overflow-matroskaparseblock-04c46.webm](attachments/chrome-heap-buffer-overflow-matroskaparseblock-04c46.webm) (application/octet-stream; charset=binary, 178.5 KB)

## Timeline

### in...@chromium.org (2012-12-20)

Dale, this looks similar to something you fixed recently. https://code.google.com/p/chromium/issues/detail?id=165601. Can you please take a look.

### da...@chromium.org (2012-12-20)

I'll take a look. If it's the same issue, then yeah, that's not fixed on ToT/M25 yet since the M25 FFMpeg roll got delayed. It's getting merged to M25 today, trunk probably not until after the holidays since I need to investigate some Windows issues there. 

### in...@chromium.org (2012-12-20)

Dale, then i think it can be a dupe since ffmpeg fix hasn't rolled. Lets let it roll, then ClusterFuzz will take like a day to confirm that this is fixed.

### da...@chromium.org (2012-12-20)

I think this is a different issue, with the patch for the other issue in place it still occurs. +rbultje for assistance. I'm unable to get a good stack from my mac though.

Is ClusterFuzz detecting this to be the same issue or do you have a link to it's stack trace somewhere?

### in...@chromium.org (2012-12-20)

Dale, i am lazy. I just uploaded it now - https://cluster-fuzz.appspot.com/testcase?key=152499103, lets see what CF says.

### in...@chromium.org (2012-12-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=152499103

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f181b72a579
Crash State:
  - crash stack -
  matroska_parse_block
  matroska_parse_cluster
  matroska_read_packet
  

Minimized Testcase (178.53 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95KvC8KpQelIsagIAMWzbGizdfi3KfcZlIDYiPw2Ds8G_fE91zsGvHuv6GNJJZTkObQ3B5B5xdNpzejogPMrkcMhZ6BdKm7guXzjPCXlmZaJlLDcqTSpbUb1kvlyaBUZ8m-Dh_OZ8FGgqZ9pr49wF0H7Wy6ccpP7vRbaM_UX3BexPD-CcM

### in...@chromium.org (2012-12-20)

Dale, CF just gifted you a nice stack as you wanted :)

### da...@chromium.org (2012-12-20)

Thanks :)

Looks like it's overreading the packet despite some size checks, here are the values at time of failure:
[matroska,webm @ 0x9ad9840] n: 0, lace_size[n]: 35 size: 309
[matroska,webm @ 0x9ad9840] n: 1, lace_size[n]: 37 size: 274
[matroska,webm @ 0x9ad9840] n: 2, lace_size[n]: 40 size: 237
[matroska,webm @ 0x9ad9840] n: 3, lace_size[n]: 39 size: 197
[matroska,webm @ 0x9ad9840] n: 4, lace_size[n]: 91 size: 158
[matroska,webm @ 0x9ad9840] n: 5, lace_size[n]: 60 size: 67
<crash>

### da...@chromium.org (2012-12-20)

matroska_parse_laces() slides the buffer ptr forward but does not subtract the metadata size from the buffer size, causing a false positive in a size check later on:

https://codereview.chromium.org/11647042

WDYT Ronald?

### pa...@chromium.org (2012-12-20)

Although we have here a read A/V of size 1, it seems like there is potentially more opportunity for out-of-bounds reading, after the call site of matroska_parse_laces (e.g. when we later go on to call matroska_parse_rm_audio).

Judging by upstream Git repo, the current implementation of matroska_parse_laces dates back to 2012-09-17, well before M23 (current stable). So I am going to say the vulnerability is old. FWIW I can't get the repro webm file to do anything bad on Linux Chrome 23 (the video just ends). But the vulnerable code is the same on all platforms, and another repro might cause more reliable destruction. Setting flags accordingly; feel free to flame me if I'm wrong.

### [Deleted User] (2012-12-21)

Suggested patch is probably OK, I didn't look in-depth tbh. Do you intend to roll & ship this soon, i.e. how quick a review would you like?

### sc...@gmail.com (2012-12-21)

If we think the bug is old, we should tag with the current stable milestone (M23 affected). It's a useful piece of history.

When we set Merge-Merged, we can set the milestone to where we actually fixed it, e.g. Mstone-24, Release-1 (release 0 is frozen) or Mstone-25, Release-0, depending on what we decide.

And shouldn't forget reward-topanel :)

### da...@chromium.org (2012-12-21)

Ronald: Due to the holidays, so long as we get it before m24 stable roll (january'ish) it's probably fine.

### da...@chromium.org (2013-01-02)

Ronald: Further thoughts?

### [Deleted User] (2013-01-03)

See patch itself; lgtm from my side.

### bu...@chromium.org (2013-01-04)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=175176

------------------------------------------------------------------------
r175176 | dalecurtis@google.com | 2013-01-04T20:09:44.467918Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/libavformat/matroskadec.c?r1=175176&r2=175175&pathrev=175176

Matroska fix for BUG=167069
------------------------------------------------------------------------

### bu...@chromium.org (2013-01-04)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=175180

------------------------------------------------------------------------
r175180 | dalecurtis@google.com | 2013-01-04T20:20:15.085882Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_demuxer_unittest.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/chunk_demuxer_unittest.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/webm/webm_stream_parser.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/base/limits.h?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/pipeline_integration_test.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/audio_renderer_impl_unittest.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/ffmpeg/ffmpeg_common.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_audio_decoder_unittest.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_audio_decoder.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/decrypting_demuxer_stream_unittest.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/decrypting_demuxer_stream.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_audio_decoder.h?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/base/audio_decoder_config.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/decrypting_audio_decoder_unittest.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/mp4/mp4_stream_parser.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/base/audio_decoder_config.h?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/audio_file_reader_unittest.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/audio_file_reader.cc?r1=175180&r2=175179&pathrev=175180
   M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/audio_decoder_selector_unittest.cc?r1=175180&r2=175179&pathrev=175180

Roll FFMpeg for M26. Fix ffmpeg float audio decoding.

FFmpeg now outputs float for some audio decoders.  Unfortunately our pipeline
doesn't support float between the FFmpegAudioDecoder and AudioRenderer at
present.  As such, we need to convert the data into an integer format first.

As a byproduct of this, AMR support for ChromeOS is finally fixed and adding
support for PCM float is trivial.

In summary this patch adds:
- A SampleFormat property to AudioDecoderConfig.
- AVSampleFormat <-> SampleFormat converters in FFmpegCommon.
- Fixes ChromeOS AMR playback.
- Finally plumbs pcm_f32le support (enabled in FFmpeg long ago).
- Add decoder support for float planar and float interleaved playback.

BUG=109085, 158187, 167069
TEST=unittests, layout tests, and demos all pass under tooling without issue.

Review URL: https://codereview.chromium.org/11280301
------------------------------------------------------------------------

### in...@chromium.org (2013-01-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-10)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=32363

------------------------------------------------------------------------
r32363 | dalecurtis@google.com | 2013-01-10T18:56:52.268030Z

------------------------------------------------------------------------

### bu...@chromium.org (2013-01-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=176122

------------------------------------------------------------------------
r176122 | dalecurtis@google.com | 2013-01-10T18:55:19.219479Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/ffmpeg/1364/libavformat/matroskadec.c?r1=176122&r2=176121&pathrev=176122

Merge lace size fix for BUG=167069
------------------------------------------------------------------------

### da...@chromium.org (2013-01-10)

M24 is the only branch left. Let me know when it's okay to merge.

### sc...@gmail.com (2013-01-10)

If the change made it out successfully to a M25 dev, then go ahead.

### sc...@gmail.com (2013-01-11)

Actually, this bug doesn't seem too serious?
If you concur, we can probably just let this be and roll into M25. WDYT?

### sc...@gmail.com (2013-01-17)

M25 it is.

### sc...@gmail.com (2013-01-22)

@attekett: $500 for the OOB read!

### cl...@chromium.org (2013-01-22)

ClusterFuzz has detected this issue as fixed in latest custom build.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=152499103

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f181b72a579
Crash State:
  - crash stack -
  matroska_parse_block
  matroska_parse_cluster
  matroska_read_packet
  

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95KvC8KpQelIsagIAMWzbGizdfi3KfcZlIDYiPw2Ds8G_fE91zsGvHuv6GNJJZTkObQ3B5B5xdNpzejogPMrkcMhZ6BdKm7guXzjPCXlmZaJlLDcqTSpbUb1kvlyaBUZ8m-Dh_OZ8FGgqZ9pr49wF0H7Wy6ccpP7vRbaM_UX3BexPD-CcM

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-02-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-02-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/167069?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media>FFmpeg]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076727)*
