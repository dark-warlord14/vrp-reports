# Heap-buffer-overflow read in libavformat `mov_seek_stream` / `can_seek_to_key_sample` via a crafted HEVC MP4 and an HTMLMediaElement seek

| Field | Value |
|-------|-------|
| **Issue ID** | [507090179](https://issues.chromium.org/issues/507090179) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media>FFmpeg |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | qw...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2026-04-27 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description

Heap-buffer-overflow read in libavformat `mov_seek_stream` / `can_seek_to_key_sample` via a crafted HEVC MP4 and an HTMLMediaElement seek

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src>

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

A crafted MP4 with one HEVC video track and one valid Opus audio track makes libavformat's `mov_seek_stream` retry path call `can_seek_to_key_sample(st, requested_sample, next_ts)` with `requested_sample = -1`. The bounds guard at `third_party/ffmpeg/libavformat/mov.c:11601` is a signed `int` compare (`if (sample >= sc->sample_offsets_count)`) and lets `-1` through, after which line 11604 reads `sti->index_entries[-1].timestamp` — an 8-byte heap out-of-bounds READ 16 bytes before a 1536-byte `index_entries` buffer allocated by `av_reallocp_array`. Trigger is `<video src=poc.mp4>` plus a JS `video.currentTime = 0` (or any value mapping to PTS 0 on the HEVC track); no user gesture, autoplay opt-in, or experimental feature flag is required for the web trigger.

## Affected versions

- Crash reproduced and ASAN log captured on **149.0.7802.0** Linux ASAN. The Chromium `149.0.7802.0` tag pins `third_party/ffmpeg` to the `chromium/third_party/ffmpeg` fork at **`b5e18fb9da84e26ceef30d4e4886696bf59337c0`**.
- Source reviewed in a Chromium checkout from 2026-04-27 whose DEPS pin `third_party/ffmpeg` to **`64c21ea132c48271dd3ce497eeb008187eb7d3f1`**; the vulnerable hunk is still present there. `third_party/ffmpeg` `file:line` anchors below refer to that pinned ffmpeg revision. Chromium-side `ffmpeg_demuxer.cc` references are by function name because line numbers may drift between Chromium checkouts. Both pins contain the prerequisite commit identified in the Bisect section.

## Root cause

Three conditions compose:

1. **`can_seek_to_key_sample` uses a signed-`int` upper-bound compare.** `third_party/ffmpeg/libavformat/mov.c:11592-11616`:
   
   ```
   static int can_seek_to_key_sample(AVStream *st, int sample, int64_t requested_pts)
   {
       MOVStreamContext *sc = st->priv_data;
       FFStream *const sti = ffstream(st);
       int64_t key_sample_dts, key_sample_pts;
   
       if (st->codecpar->codec_id != AV_CODEC_ID_HEVC)
           return 1;
       if (sample >= sc->sample_offsets_count)        // sample is int, count is int — sample = -1 passes
           return 1;
       key_sample_dts = sti->index_entries[sample].timestamp;          // line 11604: OOB read
       key_sample_pts = key_sample_dts + sc->sample_offsets[sample] + sc->dts_shift;
       if (is_open_key_sample(sc, sample) && key_sample_pts > requested_pts)
           return 0;
       return 1;
   }
   
   ```
   
   `MOVStreamContext::sample_offsets_count` is `int` (signed) at `third_party/ffmpeg/libavformat/isom.h:247`, so the only guard rejects `sample >= count` but never `sample < 0`.
2. **The retry path in `mov_seek_stream` feeds the result of `av_index_search_timestamp(..., flags)` straight into `can_seek_to_key_sample`.** `third_party/ffmpeg/libavformat/mov.c:11634-11655`:
   
   ```
   for (;;) {
       sample = av_index_search_timestamp(st, timestamp, flags);
       if (sample < 0 && sti->nb_index_entries && timestamp < sti->index_entries[0].timestamp)
           sample = 0;                                                  // fix-up applies only to the first call
       if (sample < 0)
           return AVERROR_INVALIDDATA;
       if (!sample || can_seek_to_key_sample(st, sample, timestamp))
           break;
       next_ts = timestamp - FFMAX(sc->min_sample_duration, 1);         // crafted file: min_sample_duration = 0, so next_ts = timestamp - 1
       requested_sample = av_index_search_timestamp(st, next_ts, flags);// returns -1 when no entry has ts <= next_ts
       if (sample != requested_sample && !can_seek_to_key_sample(st, requested_sample, next_ts))
           break;                                                        // requested_sample = -1 reaches the function with no fix-up
       timestamp = next_ts;
   }
   
   ```
   
   The fix-up after the first `av_index_search_timestamp` is not mirrored on `requested_sample`, so `-1` flows directly into condition (1).
3. **The crafted MP4 forces the first `can_seek_to_key_sample` call to return 0, so the retry path is taken.** The first `av_index_search_timestamp` returns a non-zero midpoint sample. For that sample, `can_seek_to_key_sample` evaluates `is_open_key_sample(midpoint) && key_sample_pts > requested_pts`; the crafted MP4 makes both true, so the function returns 0 and the loop falls into the retry path. `make_poc_mp4.py` builds a moov with `stts` `count=4 duration=0` (so `min_sample_duration = 0`), `ctts` offsets `[100,200,300,400,...]` (so `key_sample_pts > 0` for any midpoint), `stss` marking every sample sync, an `sgpd` of `grouping_type=sync` whose first entry has `nal_unit_type = HEVC_NAL_CRA_NUT (21)`, and **N separate `sbgp` entries each with `count=1, group_description_index=1`**. The split-`sbgp` shape is required because `build_open_gop_key_points` at `third_party/ffmpeg/libavformat/mov.c:4631-4640` uses a constant `sample_id` inside the inner loop and only ratchets `sample_id` between outer `sbgp` entries:
   
   ```
   for (uint32_t i = 0; i < sc->sync_group_count; i++) {
       const MOVSbgp *sg = &sc->sync_group[i];
       if (sg->index == cra_index)
           for (uint32_t j = 0; j < sg->count; j++)
               sc->open_key_samples[k++] = sample_id;     // inner loop sees a fixed sample_id
       sample_id += sg->count;                            // ratchets only between outer entries
   }
   
   ```
   
   With one `sbgp` entry of `count=N`, `open_key_samples` becomes `[0,0,...,0]` and `is_open_key_sample(midpoint) = 0`, so the first `can_seek_to_key_sample` returns 1 and the retry path is never entered. With N per-sample `sbgp` entries of `count=1`, `open_key_samples = [0,1,...,N-1]`, `is_open_key_sample(midpoint) = 1`, the first call returns 0, and the loop falls into the OOB second call.

The HEVC track does not have to be supported by the Chromium media stack. On Chromium-branded builds with `ENABLE_PLATFORM_HEVC=false`, `FFmpegDemuxerStream::Create` rejects the HEVC `AVStream`, but `FFmpegDemuxer::OnFindStreamInfoDone` only logs the unsupported video track and `continue`s from the stream-construction loop. It does not set `stream->discard = AVDISCARD_ALL` for that HEVC `AVStream`. The HEVC stream therefore remains in `format_context->streams[]`. When a seek is then issued for the surviving Opus track, `mov_read_seek` walks every stream because `seek_individually` defaults to 1 (`third_party/ffmpeg/libavformat/mov.c:11725-11742`, default at `:11773`), so `mov_seek_stream` runs on the zombie HEVC stream and reaches the bug.

## Reproduction

Extract the attached `poc.html`, `poc.mp4`, `make_poc_mp4.py`, and `asan.log` into an empty working directory and `cd` into it. Download the ASAN build into the same directory so that `chrome` and `llvm-symbolizer` sit next to the PoC files. All commands below are run from that directory; every path is relative.

1. Download the 149.0.7802.0 Linux ASAN build using `get_asan_chrome.py` (which ships in the Chromium source tree at `tools/get_asan_chrome/get_asan_chrome.py`):
   
   ```
   python3 get_asan_chrome.py --version 149.0.7802.0 --output-dir .
   
   ```
   
   Unzip the resulting archive and move `chrome`, `llvm-symbolizer`, and the sibling runtime files into the working directory.
2. Serve the PoC over a local HTTP origin (single command line):
   
   ```
   python3 -m http.server 8000
   
   ```
3. In another shell, run the ASAN build against the PoC (single command line):
   
   ```
   ASAN_OPTIONS=detect_leaks=0:symbolize=1:allocator_may_return_null=1:halt_on_error=1:external_symbolizer_path=./llvm-symbolizer ./chrome --no-sandbox --user-data-dir=/tmp/asan_profile --headless=new --no-first-run --disable-breakpad --disable-crash-reporter "http://127.0.0.1:8000/poc.html" 2> asan.log
   
   ```

`make_poc_mp4.py` is the deterministic builder for `poc.mp4`; running it regenerates the same 26 KB MP4 used to capture the attached `asan.log`. The attached `asan.log` was captured with the command above.

## Crash evidence

From `asan.log`:

```
==343409==ERROR: AddressSanitizer: use-after-poison on address 0x7449f7300d70 at pc 0x59cbcbeeadcc bp 0x7299ee5992a0 sp 0x7299ee599298
READ of size 8 at 0x7449f7300d70 thread T4 (ThreadPoolForeg)
    #0 0x59cbcbeeadcb in mov_seek_stream third_party/ffmpeg/libavformat/mov.c:11604:49

```

Allocation context (the buffer the read is past):

```
0x7449f7300d70 is located 16 bytes before 1536-byte region [0x7449f7300d80,0x7449f7301380)
allocated by thread T4 (ThreadPoolForeg) here:
    #0 realloc
    #1 av_reallocp_array third_party/ffmpeg/libavutil/mem.c:165:11

```

ASAN labels the report `use-after-poison` because the byte before the user region is poisoned by PartitionAlloc (Chromium's heap allocator) via `__asan_poison_memory_region` rather than ASAN's own malloc-shim left-redzone. The semantic is identical to `heap-buffer-overflow` — a read past the start of an allocation. The crashing process is the renderer, confirmed by the command line in the log's ADDITIONAL INFO block (`/proc/self/exe --type=renderer ...`). The task trace shows the crash on the media demuxer seek path: `media::FFmpegDemuxer::SeekInternal` posts `AVSeekFrame` to a blocking task runner, and the OOB read fires on that runner's `ThreadPoolForeg` thread.

## Bisect

The bug landed when the retry path in `mov_seek_stream` was added; before that commit, the loop just decremented `timestamp` without making a second `can_seek_to_key_sample` call, so no caller ever passed a negative `sample`.

- **Commit**: `d1b96c380826c505a8c7e655b5ad4fdb0c2de167` (FFmpeg upstream; carried into Chromium's `chromium/third_party/ffmpeg` fork)
- **Subject**: `avformat/mov: avoid seeking back to 0 on HEVC open GOP files`
- **Date**: 2024-05-21
- **Upstream URL**: <https://git.ffmpeg.org/gitweb/ffmpeg.git/commit/d1b96c380826c505a8c7e655b5ad4fdb0c2de167>

The exact hunk that introduces the unguarded second call:

```
--- a/libavformat/mov.c
+++ b/libavformat/mov.c
@@ -10133,7 +10133,7 @@ static int mov_seek_stream(AVFormatContext *s, AVStream *st, int64_t timestamp,
 {
     MOVStreamContext *sc = st->priv_data;
     FFStream *const sti = ffstream(st);
-    int sample, time_sample, ret;
+    int sample, time_sample, ret, next_ts, requested_sample;
     unsigned int i;
@@ -10154,7 +10154,17 @@ static int mov_seek_stream(AVFormatContext *s, AVStream *st, int64_t timestamp,
         if (!sample || can_seek_to_key_sample(st, sample, timestamp))
             break;
-        timestamp -= FFMAX(sc->min_sample_duration, 1);
+        next_ts = timestamp - FFMAX(sc->min_sample_duration, 1);
+        requested_sample = av_index_search_timestamp(st, next_ts, flags);
+        if (!can_seek_to_key_sample(st, requested_sample, next_ts) && sample != requested_sample)
+            break;
+        timestamp = next_ts;
     }

```

The earlier prerequisite that introduced `can_seek_to_key_sample` itself is FFmpeg `ab77b878f1` (<https://git.ffmpeg.org/gitweb/ffmpeg.git/commit/ab77b878f1>, "avformat/mov: fix seeking with HEVC open GOP files", 2022-05-19). The first chromium fork merge that pulled `d1b96c3808` into `chromium/third_party/ffmpeg` is `d4258358c7672ae3ccaac0ffb16c5169bbff273c` (<https://chromium.googlesource.com/chromium/third_party/ffmpeg/+/d4258358c7672ae3ccaac0ffb16c5169bbff273c>, 2024-09-20). Both the 149.0.7802.0 pin (`b5e18fb9da...`) and the current pin (`64c21ea132...`) include all of these prerequisites.

## Suggested patch

Tighten `can_seek_to_key_sample`'s bounds check to reject negative `sample` in addition to over-large values:

```
--- a/third_party/ffmpeg/libavformat/mov.c
+++ b/third_party/ffmpeg/libavformat/mov.c
@@ -11598,7 +11598,8 @@ static int can_seek_to_key_sample(AVStream *st, int sample, int64_t requested_pt
     if (st->codecpar->codec_id != AV_CODEC_ID_HEVC)
         return 1;

-    if (sample >= sc->sample_offsets_count)
+    if (sample < 0 || sample >= sti->nb_index_entries ||
+        sample >= sc->sample_offsets_count)
         return 1;

     key_sample_dts = sti->index_entries[sample].timestamp;

```

Rationale: `sample` is `int`, and the function reads `sti->index_entries[sample]` and `sc->sample_offsets[sample]` immediately after. `av_index_search_timestamp` is documented to return a negative number when no matching entry exists; the existing fix-up at `mov_seek_stream:11637` only catches the first call's negative result. Rejecting `sample < 0` and bounding against both `nb_index_entries` and `sample_offsets_count` at the function boundary closes the OOB read where it happens and matches the two array accesses on the next two lines.

#### Impact analysis

ASAN reports an out-of-bounds heap READ of size 8, landing 16 bytes before the start of a 1536-byte `index_entries` allocation, inside the renderer process (sandboxed). The trigger is a `<video src=...>` element pointing at the crafted MP4 plus a single `video.currentTime` seek.

---

### The cause

#### What version of Chrome have you found the security issue in?

149.0.7802.0 dev

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Wongi Lee (@\_qwerty\_po) of Theori with Xint Code, Jungwoo Lee (@physicube).

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.9 KB)
- [make_poc_mp4.py](attachments/make_poc_mp4.py) (text/x-python, 17.1 KB)
- [asan.log](attachments/asan.log) (application/octet-stream, 7.0 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 26.3 KB)

## Timeline

### ye...@google.com (2026-04-30)

Assigning to an ffmpeg owner, could you PTAL or assign to someone else if there is a better assignee?

### da...@chromium.org (2026-04-30)

Sure will take a look.

### da...@chromium.org (2026-04-30)

Sent upstream as <https://code.ffmpeg.org/FFmpeg/FFmpeg/pulls/22976>

### ch...@google.com (2026-05-01)

Setting milestone because of s0/s1 severity.

### qw...@gmail.com (2026-05-02)

Could you please add [jwlee2217@gmail.com](mailto:jwlee2217@gmail.com) to the CC list so that both accounts can access the issue?

### dx...@google.com (2026-05-05)

Project: chromium/third\_party/ffmpeg  

Branch:  master  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7819356>

avformat/mov: Fix negative index given to can\_seek\_to\_key\_sample()

---


Expand for full commit details
```
     
    The potentially negative return value of av_index_search_timestamp() 
    wasn't being handled before passing it to can_seek_to_key_sample(). 
     
    Found by Wongi Lee (@_qwerty_po) of Theori with Xint Code, 
    Jungwoo Lee (@physicube). 
     
    Signed-off-by: Dale Curtis <dalecurtis@chromium.org> 
    Bug: 507090179 
    Change-Id: I3037acb8e3d6cd5eedb7ef812569673d9be61879 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/third_party/ffmpeg/+/7819356 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>

```

---

Files:

- M `libavformat/mov.c`

---

Hash: [a87f87d880452edb43738d90ae2948ba1c22581e](https://chromiumdash.appspot.com/commit/a87f87d880452edb43738d90ae2948ba1c22581e)  

Date: Tue May 5 22:04:27 2026


---

### da...@chromium.org (2026-05-05)

Upstream landed the fix, rolling it into Chrome now.

### dx...@google.com (2026-05-06)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7819266>

Roll FFmpeg from 9b84150fa4e6 to a87f87d88045 (1 revision)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/chromium/third_party/ffmpeg/+log/9b84150fa4e6..a87f87d88045 
     
    2026-05-05 dalecurtis@chromium.org avformat/mov: Fix negative index given to can_seek_to_key_sample() 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/ffmpeg-chromium 
    Please CC chromium-ffmpeg-roll@rotations.google.com,videostack-eng@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in FFmpeg: https://g-issues.chromium.org/issues/new?450394703 
    To file a bug in Chromium: https://g-issues.chromium.org/issues/new?component=450394703 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Tbr: chromium-ffmpeg-roll@rotations.google.com 
    Change-Id: Icaa516feb7b48890763b96d376ae9bba6e151e83 
    Fixed: 507090179 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7819266 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1625856}

```

---

Files:

- M `DEPS`
- M `third_party/ffmpeg`

---

Hash: [3fa9afb285ca7bd1446512c309a49c23b02a3df6](https://chromiumdash.appspot.com/commit/3fa9afb285ca7bd1446512c309a49c23b02a3df6)  

Date: Wed May 6 00:43:09 2026


---

### ch...@google.com (2026-05-06)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-05-06)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### da...@chromium.org (2026-05-06)

(This bot is incredibly obnoxious)

### aj...@google.com (2026-05-12)

Medium as this is a read in the renderer.

### sp...@google.com (2026-05-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect (Patch not used). User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/507090179)*
