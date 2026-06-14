# OOB read in vp8_decode_frame

| Field | Value |
|-------|-------|
| **Issue ID** | [40096058](https://issues.chromium.org/issues/40096058) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals>Media |
| **Reporter** | in...@chromium.org |
| **Assignee** | sc...@chromium.org |
| **Created** | 2011-10-10 |
| **Bounty** | $1,000.00 |

## Description

credit: Cris + ASAN + ClusterFuzz

Bot CLUSTER_FUZZ_181 on platform LINUX
Chromium Revision : 104057
Webkit Revision : 96650

/mnt/scratch0/chrome/src/out/Release/chrome --allow-file-access-from-files --disable-click-to-play --disable-hang-monitor --disable-metrics --disable-popup-blocking --disable-prompt-on-repost --enable-desktop-notifications --enable-experimental-extension-apis --enable-extension-apps --enable-extension-timeline-api --enable-geolocation --enable-indexed-database --enable-nacl --enable-native-web-workers --enable-search-provider-api-v2 --force-internal-pdf --incognito --js-flags="--expose-gc" --new-window --no-default-browser-check --no-first-run --no-process-singleton-dialog --no-sandbox --single-process --disable-gpu-plugin --disable-gpu-rendering --disable-accelerated-compositing --disable-webgl --disable-accelerated-2d-canvas --user-data-dir=/mnt/scratch0/FuzzTmp/t12 

ASAN:SIGILL
=================================================================
HINT: if your stack trace looks short or garbled, use ASAN_OPTIONS=fast_unwind=0
==24045== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fa7c39bdc18 at pc 0x7fa7ec6c0925 bp 0x7fa7c01f5cd0 sp 0x7fa7c01f53a0
READ of size 1 at 0x7fa7c39bdc18 thread T21
    #0 0x7fa7ec6c0925 in vp8_decode_frame third_party/ffmpeg/patched-ffmpeg/libavcodec/vp8.c:0
    #1 0x7fa7ec6544bb in frame_worker_thread third_party/ffmpeg/patched-ffmpeg/libavcodec/pthread.c:0
    #2 0x7470d61 in AsanThread::ThreadStart() /usr/local/google/asan/address-sanitizer/asan/asan_thread.cc:105
    #3 0x7fa802ddb9ca in start_thread /build/buildd/eglibc-2.11.1/nptl/pthread_create.c:300
    #4 0x7fa800f5b70d in ?? /build/buildd/eglibc-2.11.1/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:114
0x7fa7c39bdc18 is located 0 bytes to the right of 920-byte region [0x7fa7c39bd880,0x7fa7c39bdc18)
allocated by thread T20 here:
    #1 0x7fa7ec748efb in av_malloc 
    #2 0x7fa7ec74902f in av_mallocz 
    #3 0x7fa7ec6544bb in frame_worker_thread third_party/ffmpeg/patched-ffmpeg/libavcodec/pthread.c:0
Thread T21 created by T19 here:
    #1 0x7fa7ec65358e in ff_thread_init 
    #2 0x7fa7ec65f6d9 in avcodec_open2 
    #3 0x73b0378 in media::FFmpegVideoDecodeEngine::Initialize(MessageLoop*, media::VideoDecodeEngine::EventHandler*, media::VideoDecodeContext*, media::VideoDecoderConfig const&) 
    #4 0x739d7a6 in media::FFmpegVideoDecoder::Initialize(media::DemuxerStream*, base::Callback<void ()()> const&, base::Callback<void ()(media::PipelineStatistics const&)> const&) 
    #5 0x73a4c23 in base::internal::Invoker4<false, base::internal::InvokerStorage4<void (media::FFmpegVideoDecoder::*)(media::DemuxerStream*, base::Callback<void ()()> const&, base::Callback<void ()(media::PipelineStatistics const&)> const&), media::FFmpegVideoDecoder*, scoped_refptr<media::DemuxerStream>, base::Callback<void ()()>, base::Callback<void ()(media::PipelineStatistics const&)> >, void (media::FFmpegVideoDecoder::*)(media::DemuxerStream*, base::Callback<void ()()> const&, base::Callback<void ()(media::PipelineStatistics const&)> const&)>::DoInvoke(base::internal::InvokerStorageBase*) 
    #6 0x1d590b1 in MessageLoop::RunTask(MessageLoop::PendingTask const&) 
    #7 0x1d597c1 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) 
    #8 0x1d5ac79 in MessageLoop::DoWork() 
    #9 0x1d6506a in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) 
    #10 0x1d57c4a in MessageLoop::RunInternal() 
    #11 0x1d55db9 in MessageLoop::Run() 
    #12 0x1dcfec8 in base::Thread::ThreadMain() 
    #13 0x1dceb7c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:0
    #14 0x7470d61 in AsanThread::ThreadStart() /usr/local/google/asan/address-sanitizer/asan/asan_thread.cc:105
    #15 0x7fa802ddb9ca in start_thread /build/buildd/eglibc-2.11.1/nptl/pthread_create.c:300
    #16 0x7fa800f5b70d in ?? /build/buildd/eglibc-2.11.1/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:114
Thread T20 created by T19 here:
    #1 0x7fa7ec65358e in ff_thread_init 
    #2 0x7fa7ec65f6d9 in avcodec_open2 
    #3 0x73b0378 in media::FFmpegVideoDecodeEngine::Initialize(MessageLoop*, media::VideoDecodeEngine::EventHandler*, media::VideoDecodeContext*, media::VideoDecoderConfig const&) 
    #4 0x739d7a6 in media::FFmpegVideoDecoder::Initialize(media::DemuxerStream*, base::Callback<void ()()> const&, base::Callback<void ()(media::PipelineStatistics const&)> const&) 
    #5 0x73a4c23 in base::internal::Invoker4<false, base::internal::InvokerStorage4<void (media::FFmpegVideoDecoder::*)(media::DemuxerStream*, base::Callback<void ()()> const&, base::Callback<void ()(media::PipelineStatistics const&)> const&), media::FFmpegVideoDecoder*, scoped_refptr<media::DemuxerStream>, base::Callback<void ()()>, base::Callback<void ()(media::PipelineStatistics const&)> >, void (media::FFmpegVideoDecoder::*)(media::DemuxerStream*, base::Callback<void ()()> const&, base::Callback<void ()(media::PipelineStatistics const&)> const&)>::DoInvoke(base::internal::InvokerStorageBase*) 
    #6 0x1d590b1 in MessageLoop::RunTask(MessageLoop::PendingTask const&) 
    #7 0x1d597c1 in MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) 
    #8 0x1d5ac79 in MessageLoop::DoWork() 
    #9 0x1d6506a in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) 
    #10 0x1d57c4a in MessageLoop::RunInternal() 
    #11 0x1d55db9 in MessageLoop::Run() 
    #12 0x1dcfec8 in base::Thread::ThreadMain() 
    #13 0x1dceb7c in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:0
    #14 0x7470d61 in AsanThread::ThreadStart() /usr/local/google/asan/address-sanitizer/asan/asan_thread.cc:105
    #15 0x7fa802ddb9ca in start_thread /build/buildd/eglibc-2.11.1/nptl/pthread_create.c:300
    #16 0x7fa800f5b70d in ?? /build/buildd/eglibc-2.11.1/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:114
==24045== ABORTING
Shadow byte and word:
  0x1ff4f8737b83: fb
  0x1ff4f8737b80: 00 00 00 fb fb fb fb fb
More shadow bytes:
  0x1ff4f8737b60: 00 00 00 00 00 00 00 00
  0x1ff4f8737b68: 00 00 00 00 00 00 00 00
  0x1ff4f8737b70: 00 00 00 00 00 00 00 00
  0x1ff4f8737b78: 00 00 00 00 00 00 00 00
=>0x1ff4f8737b80: 00 00 00 fb fb fb fb fb
  0x1ff4f8737b88: fb fb fb fb fb fb fb fb
  0x1ff4f8737b90: fa fa fa fa fa fa fa fa
  0x1ff4f8737b98: fa fa fa fa fa fa fa fa
  0x1ff4f8737ba0: fa fa fa fa fa fa fa fa


## Attachments

- [fuzz-bitflip-sc4wtO.webm](attachments/fuzz-bitflip-sc4wtO.webm) (application/octet-stream; charset=binary, 616.0 KB)
- [fix-fuzz-crash.patch](attachments/fix-fuzz-crash.patch) (text/x-diff; charset=us-ascii, 1.6 KB)
- [fix-fuzz-crash.patch](attachments/fix-fuzz-crash_52940292.patch) (text/x-diff; charset=us-ascii, 1.9 KB)
- [mkv-fuxx.patch](attachments/mkv-fuxx.patch) (text/x-diff; charset=us-ascii, 531 B)

## Timeline

### im...@chromium.org (2011-10-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-11)

I can have a look if no-else gets to it, but it'll be a few days.

### im...@chromium.org (2011-10-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-12)

Ok, so this doesn't affect Chrome 14 stable but does affect Chrome 15 beta and trunk.
Accordingly, it is a security regression and must be marked as a release blocker.

### sc...@gmail.com (2011-10-12)

valgrind reports some out-of-bounds writes after the out-of-bounds reads, so upgrading to high severity

### sc...@gmail.com (2011-10-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-12)

Here's the valgrind output up to the first OOB write (as seen on tip of M15 branch):


==24283== Thread 9:
==24283== Invalid read of size 1
        *segment = ref ? *ref : *segment;
==24283==    at 0x16405F71: vp8_decode_frame (vp8.c:595)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283==  Address 0x183c1218 is 0 bytes after a block of size 920 alloc'd
==24283==    at 0x84E5569: posix_memalign (vg_replace_malloc.c:925)
==24283==    by 0x1642E374: av_malloc (mem.c:90)
==24283==    by 0x1642E405: av_mallocz (mem.c:165)
==24283==    by 0x1640A3AC: vp8_decode_frame (vp8.c:79)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283== 
==24283== 
==24283== ---- Attach to debugger ? --- [Return/N/n/Y/y/C/c] ---- ==24283== Invalid read of size 8
==24283==    at 0x16446370: ??? (in /home/chris/chrome_m15/src/out/Debug/libffmpegsumo.so)
==24283==    by 0x1638BD44: ff_put_vp8_epel16_h6_ssse3 (vp8dsp-init.c:157)
==24283==    by 0x1638C04D: ff_put_vp8_epel16_h6v6_ssse3 (vp8dsp-init.c:194)
==24283==    by 0x164053D8: vp8_decode_frame (vp8.c:1087)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283==  Address 0x18403cd8 is 8 bytes after a block of size 268,816 alloc'd
==24283==    at 0x84E5569: posix_memalign (vg_replace_malloc.c:925)
==24283==    by 0x1642E374: av_malloc (mem.c:90)
==24283==    by 0x163F08BA: avcodec_default_get_buffer (utils.c:325)
==24283==    by 0x163EA976: ff_thread_get_buffer (pthread.c:810)
==24283==    by 0x16400ECD: vp8_decode_frame (vp8.c:1556)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283== 
==24283== Invalid read of size 8
==24283==    at 0x16446370: ??? (in /home/chris/chrome_m15/src/out/Debug/libffmpegsumo.so)
==24283==    by 0x1638C04D: ff_put_vp8_epel16_h6v6_ssse3 (vp8dsp-init.c:194)
==24283==    by 0x164053D8: vp8_decode_frame (vp8.c:1087)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283==  Address 0x18403ce0 is 16 bytes after a block of size 268,816 alloc'd
==24283==    at 0x84E5569: posix_memalign (vg_replace_malloc.c:925)
==24283==    by 0x1642E374: av_malloc (mem.c:90)
==24283==    by 0x163F08BA: avcodec_default_get_buffer (utils.c:325)
==24283==    by 0x163EA976: ff_thread_get_buffer (pthread.c:810)
==24283==    by 0x16400ECD: vp8_decode_frame (vp8.c:1556)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283== 
==24283== Invalid read of size 8
==24283==    at 0x16446400: ??? (in /home/chris/chrome_m15/src/out/Debug/libffmpegsumo.so)
==24283==    by 0x1638BBAB: ff_put_vp8_epel8_h4v4_ssse3 (vp8dsp-init.c:190)
==24283==    by 0x1640A008: vp8_decode_frame (vp8.c:1144)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283==  Address 0x184144ac is 67,212 bytes inside a block of size 67,216 alloc'd
==24283==    at 0x84E5569: posix_memalign (vg_replace_malloc.c:925)
==24283==    by 0x1642E374: av_malloc (mem.c:90)
==24283==    by 0x163F08BA: avcodec_default_get_buffer (utils.c:325)
==24283==    by 0x163EA976: ff_thread_get_buffer (pthread.c:810)
==24283==    by 0x16400ECD: vp8_decode_frame (vp8.c:1556)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283== 
==24283== Invalid read of size 8
==24283==    at 0x16446400: ??? (in /home/chris/chrome_m15/src/out/Debug/libffmpegsumo.so)
==24283==    by 0x1638BBAB: ff_put_vp8_epel8_h4v4_ssse3 (vp8dsp-init.c:190)
==24283==    by 0x1640A037: vp8_decode_frame (vp8.c:1145)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283==  Address 0x18424cac is 67,212 bytes inside a block of size 67,216 alloc'd
==24283==    at 0x84E5569: posix_memalign (vg_replace_malloc.c:925)
==24283==    by 0x1642E374: av_malloc (mem.c:90)
==24283==    by 0x163F08BA: avcodec_default_get_buffer (utils.c:325)
==24283==    by 0x163EA976: ff_thread_get_buffer (pthread.c:810)
==24283==    by 0x16400ECD: vp8_decode_frame (vp8.c:1556)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283== 
==24283== Invalid read of size 8
==24283==    at 0x16446400: ??? (in /home/chris/chrome_m15/src/out/Debug/libffmpegsumo.so)
==24283==    by 0x1638BEDD: ff_put_vp8_epel8_h4v6_ssse3 (vp8dsp-init.c:191)
==24283==    by 0x1640A008: vp8_decode_frame (vp8.c:1144)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283==  Address 0x184144c4 is 20 bytes after a block of size 67,216 alloc'd
==24283==    at 0x84E5569: posix_memalign (vg_replace_malloc.c:925)
==24283==    by 0x1642E374: av_malloc (mem.c:90)
==24283==    by 0x163F08BA: avcodec_default_get_buffer (utils.c:325)
==24283==    by 0x163EA976: ff_thread_get_buffer (pthread.c:810)
==24283==    by 0x16400ECD: vp8_decode_frame (vp8.c:1556)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283== 
==24283== Invalid read of size 8
==24283==    at 0x16446400: ??? (in /home/chris/chrome_m15/src/out/Debug/libffmpegsumo.so)
==24283==    by 0x1638BEDD: ff_put_vp8_epel8_h4v6_ssse3 (vp8dsp-init.c:191)
==24283==    by 0x1640A037: vp8_decode_frame (vp8.c:1145)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283==  Address 0x18424cc4 is 20 bytes after a block of size 67,216 alloc'd
==24283==    at 0x84E5569: posix_memalign (vg_replace_malloc.c:925)
==24283==    by 0x1642E374: av_malloc (mem.c:90)
==24283==    by 0x163F08BA: avcodec_default_get_buffer (utils.c:325)
==24283==    by 0x163EA976: ff_thread_get_buffer (pthread.c:810)
==24283==    by 0x16400ECD: vp8_decode_frame (vp8.c:1556)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283== 
==24283== Invalid read of size 8
==24283==    at 0x16446400: ??? (in /home/chris/chrome_m15/src/out/Debug/libffmpegsumo.so)
==24283==    by 0x1638BBAB: ff_put_vp8_epel8_h4v4_ssse3 (vp8dsp-init.c:190)
==24283==    by 0x16408ADB: vp8_decode_frame (vp8.c:1144)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283==  Address 0x184145b4 is not stack'd, malloc'd or (recently) free'd
==24283== 
==24283== Invalid read of size 8
==24283==    at 0x16446400: ??? (in /home/chris/chrome_m15/src/out/Debug/libffmpegsumo.so)
==24283==    by 0x1638BBAB: ff_put_vp8_epel8_h4v4_ssse3 (vp8dsp-init.c:190)
==24283==    by 0x16408B01: vp8_decode_frame (vp8.c:1145)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283==  Address 0x18424db4 is not stack'd, malloc'd or (recently) free'd
==24283== 
==24283== Invalid write of size 1
                    dst[i][y*curframe->linesize[i]-1] = 129;
==24283==    at 0x164012F0: vp8_decode_frame (vp8.c:1633)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283==  Address 0x1848abb7 is 41 bytes before a block of size 67,216 alloc'd
==24283==    at 0x84E5569: posix_memalign (vg_replace_malloc.c:925)
==24283==    by 0x1642E374: av_malloc (mem.c:90)
==24283==    by 0x163F08BA: avcodec_default_get_buffer (utils.c:325)
==24283==    by 0x163EA976: ff_thread_get_buffer (pthread.c:810)
==24283==    by 0x16400ECD: vp8_decode_frame (vp8.c:1556)
==24283==    by 0x163EB272: frame_worker_thread (pthread.c:301)
==24283==    by 0xCADD9C9: start_thread (pthread_create.c:300)
==24283==    by 0xF56B70C: clone (clone.S:112)
==24283== 


### sc...@gmail.com (2011-10-12)

valgrind command-line used:
./out/Debug/chrome --renderer-cmd-prefix='/home/chris/chrome/src/tools/valgrind/valgrind.sh' file:///tmp/oob.webm

where this solution in your .gclient will grab the Linux valgrind binaries used in the above command line:
  { "name"        : "src",
    "url"         : "svn://svn.chromium.org/chrome/trunk/src",
    "custom_deps" : {
"src/third_party/valgrind":
        "http://src.chromium.org/svn/trunk/deps/third_party/valgrind/binaries",
    },
    "safesync_url": "",
  },



### kc...@chromium.org (2011-10-13)

Just FYI. 
There is no easy way to make asan produce more than one error report for one run.
But you can build the code with "-mllvm -asan-instrument-reads=0" which will hide all un-addressable reads from you. So, you will crash on first un-addressable write (if any). This will make the runs even faster (I measured ~30% slowdown)

### rb...@google.com (2011-10-13)

It reproduces in ffmpeg.c commandline tool, the magic is to use the -threads 2 option, i.e.:

./ffmpeg -threads 2 -i file.webm -f null -

The problem appears to be that the threading layer doesn't update the application thread on a size change. That sounds like a big can of worms, so we can either error (which for now is probably the safe solution), or try to implement frame size switching with threading enabled, which - again - is a big can of worms.

### sc...@gmail.com (2011-10-13)

Aha so it was the threading aspect, interesting! :)
Won't we break some playbacks if we error on size change?

### rb...@google.com (2011-10-13)

My initial suspicion was wrong, it wasn't a size change in the bitstream, actually the fuzzer changed the size as indicated in the file container. The bitstream size is valid and different, so it changes it back but some variables weren't properly updated.

This patch fixes all valgrind warnings I see with this file, including the invalid writes, and also fixes the crash. If OK and applied, I'll send this upstream also.

### rb...@google.com (2011-10-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-13)

Nice work! Andrew, who should review this patch, land it to Chromium trunk, merge it to Chromium 15, rebuild Windows binaries, etc?

### ao...@gmail.com (2011-10-13)

Could someone check if segv-ffffffffffffffb8.webm at http://haltp.org/aoh/misc/webm/ crashes after applying fix-fuzz-crash.patch? It fixed 2/3 distinct WebM crash cases here, but that one remains.

### rb...@google.com (2011-10-13)

Actual embarassing code bug caused that one, fixed in attached.

Let me know when this is in chrome builds so I can send it upstream.

### sc...@chromium.org (2011-10-13)

CL http://codereview.chromium.org/8289001/

### sc...@chromium.org (2011-10-13)

DEPS roll underway for Linux/Mac -- ***still need windows binaries at this point in time***

### sc...@gmail.com (2011-10-13)

Thanks Aki for the catch. We should definitely consider your contributions here for reward :)

### sc...@chromium.org (2011-10-14)

ronald's patch makes media_unittest fail:
DecodeFrame_SmallerHeight
DecodeFrame_SmallerWidth

[==========] Running 1 test from 1 test case.
[----------] Global test environment set-up.
[----------] 1 test from FFmpegVideoDecodeEngineTest
[ RUN      ] FFmpegVideoDecodeEngineTest.DecodeFrame_SmallerHeight
[31454:31454:1013/164532:1172957193:ERROR:process_util_posix.cc(134)] Received signal 11
	base::debug::StackTrace::StackTrace() [0x5f0a7e]
	base::(anonymous namespace)::StackDumpSignalHandler() [0x5e5f53]
	0x7fc61d336af0
	avcodec_default_release_buffer [0x7fc6178e7b38]
	release_delayed_buffers [0x7fc6178e3191]
	frame_thread_free [0x7fc6178e3345]
	avcodec_close [0x7fc6178e877f]
	media::FFmpegVideoDecodeEngine::~FFmpegVideoDecodeEngine() [0x5a1c62]
	media::FFmpegVideoDecodeEngineTest::~FFmpegVideoDecodeEngineTest() [0x55d79b]
	media::FFmpegVideoDecodeEngineTest_DecodeFrame_SmallerHeight_Test::~FFmpegVideoDecodeEngineTest_DecodeFrame_SmallerHeight_Test() [0x55dc8e]
	testing::TestInfo::Run() [0x60b763]
	testing::TestCase::Run() [0x60b877]
	testing::internal::UnitTestImpl::RunAllTests() [0x60bb0d]
	testing::UnitTest::Run() [0x60a273]
	base::TestSuite::Run() [0x5f55e8]
	main [0x4c9dae]
	0x7fc61d321c4d
	0x4088a9
Note: Google Test filter = FFmpegVideoDecodeEngineTest.DecodeFrame_SmallerHeight
[==========] Running 1 test from 1 test case.
[----------] Global test environment set-up.
[----------] 1 test from FFmpegVideoDecodeEngineTest
[ RUN      ] FFmpegVideoDecodeEngineTest.DecodeFrame_SmallerHeight
[31457:31457:1013/164532:1172998218:ERROR:process_util_posix.cc(134)] Received signal 11
	base::debug::StackTrace::StackTrace() [0x5f0a7e]
	base::(anonymous namespace)::StackDumpSignalHandler() [0x5e5f53]
	0x7fe88bd50af0
	avcodec_default_release_buffer [0x7fe886301b38]
	release_delayed_buffers [0x7fe8862fd191]
	frame_thread_free [0x7fe8862fd345]
	avcodec_close [0x7fe88630277f]
	media::FFmpegVideoDecodeEngine::~FFmpegVideoDecodeEngine() [0x5a1c62]
	media::FFmpegVideoDecodeEngineTest::~FFmpegVideoDecodeEngineTest() [0x55d79b]
	media::FFmpegVideoDecodeEngineTest_DecodeFrame_SmallerHeight_Test::~FFmpegVideoDecodeEngineTest_DecodeFrame_SmallerHeight_Test() [0x55dc8e]
	testing::TestInfo::Run() [0x60b763]
	testing::TestCase::Run() [0x60b877]
	testing::internal::UnitTestImpl::RunAllTests() [0x60bb0d]
	testing::UnitTest::Run() [0x60a273]
	base::TestSuite::Run() [0x5f55e8]
	main [0x4c9dae]
	0x7fe88bd3bc4d
	0x4088a9

Test decodes these two I frames sequentially to see hpw the decoder reacts to changes in dimensions:

http://src.chromium.org/viewvc/chrome/trunk/src/media/test/data/

vp8-I-frame-320x240
vp8-I-frame-160x240

vp8-I-frame-320x240
vp8-I-frame-320x120

Any thoughts?

### sc...@chromium.org (2011-10-14)

rbultje's latest patch is good to go!

rolling DEPS now...

### ao...@gmail.com (2011-10-14)

Could you double-check http://haltp.org/aoh/misc/webm/sigill-p2.webm. I'm getting an ASAN:SIGILL at avcodec_default_release_buffer() which wasn't there before, but I may well have forgotten some changes or misapplied the patch. It takes hours to do a clean build here, so posting now since you're about to apply it.

### ao...@gmail.com (2011-10-14)

One more thing, r105464 seems to have fixed that one and the others, but sigill-p2-2.webm gives a "WRITE of size 4 at 0x7fb578041384 thread T38". I'll add other cases there should they show up. Sorry to Columbo again :)

### sc...@gmail.com (2011-10-14)

@aohelin: where are all these files coming from? :)
Could you point us to the full set so that our (awesome) ffmpeg development can get them all valgrind clean?

### ao...@gmail.com (2011-10-14)

@scarybeasts: I usually make files as they are needed, so there is no complete set. This one had the .webm files from Chromium tests as samples, and prefixes of a few videos from the net, and Radamsa was used to make mutated videos. The samples used here at webm-samples.tgz in case you want to try out.

I did just "$ while true; do radamsa -f drop,inc,dec,dup,flip,stut=3,u8ins,perm=2,surf=4,u8ed -o rad-%n.webm samples/*.* -v -n 20; $HOME/chromium/src/out/Release/chrome --incognito rad-*.webm &> out & sleep 10; grep ASAN out && break; pkill -9 chrome; rm out rad-*.webm; pkill -9 chrome; done" to test the patches, which found the extra issues pretty easily on an Atom.

A more complete test like this will be running semi-continuously over here in a while :)

### sc...@gmail.com (2011-10-14)

@aohelin: sorry, I probably wasn't clear.

I was after a complete set of the files that have caused _crashes_ in your recent testing of Chrome. We switched to a new VP8 codec, which is why we're very interested and why you are seeing new crashes recently :)

### ao...@gmail.com (2011-10-14)

@scarybeasts: Ah, I've only been testing WebM for two days and copied the few crashers manually. I'll add a crashes.tgz to that directory once WebM is part of the scripted tests and the crashes are collected automatically.

### sc...@gmail.com (2011-10-14)

Ok, any chance you could quickly enumerate the URLs for the crashers you've manually copied thus far?

It'd be nice to have a list of all the URLs in one single comment.

### ao...@gmail.com (2011-10-14)

The ones so far are:
  http://haltp.org/aoh/misc/webm/gen-prot-098.webm
  http://haltp.org/aoh/misc/webm/gen-prot-2a7.webm
  http://haltp.org/aoh/misc/webm/segv-ffffffffffffffb8.webm
  http://haltp.org/aoh/misc/webm/sigill-p2-2.webm
  http://haltp.org/aoh/misc/webm/sigill-p2-3.webm
  http://haltp.org/aoh/misc/webm/sigill-p2.webm

### rb...@google.com (2011-10-14)

Hah, this one is not in the vp8 decoder. ;-).

==6389== Invalid write of size 4
==6389==    at 0x46D097: matroska_parse_block (matroskadec.c:1844)
==6389==    by 0x46DA35: matroska_parse_cluster (matroskadec.c:1985)
==6389==    by 0x46DAC6: matroska_read_packet (matroskadec.c:2004)
==6389==    by 0x4E4980: av_read_packet (utils.c:730)
==6389==    by 0x4E6343: av_read_frame_internal (utils.c:1188)
==6389==    by 0x4E9900: avformat_find_stream_info (utils.c:2360)
==6389==    by 0x4E92C2: av_find_stream_info (utils.c:2249)
==6389==    by 0x40FC6D: opt_input_file (ffmpeg.c:3371)
==6389==    by 0x4132F4: parse_options (cmdutils.c:283)
==6389==    by 0x412979: main (ffmpeg.c:4544)
==6389==  Address 0x62ccbc4 is 0 bytes after a block of size 4 alloc'd
==6389==    at 0x4C26676: memalign (vg_replace_malloc.c:581)
==6389==    by 0x4C266CF: posix_memalign (vg_replace_malloc.c:709)
==6389==    by 0xAF5710: av_malloc (mem.c:90)
==6389==    by 0xAF57E6: av_mallocz (mem.c:165)
==6389==    by 0x46CE1E: matroska_parse_block (matroskadec.c:1789)
==6389==    by 0x46DA35: matroska_parse_cluster (matroskadec.c:1985)
==6389==    by 0x46DAC6: matroska_read_packet (matroskadec.c:2004)
==6389==    by 0x4E4980: av_read_packet (utils.c:730)
==6389==    by 0x4E6343: av_read_frame_internal (utils.c:1188)
==6389==    by 0x4E9900: avformat_find_stream_info (utils.c:2360)
==6389==    by 0x4E92C2: av_find_stream_info (utils.c:2249)
==6389==    by 0x40FC6D: opt_input_file (ffmpeg.c:3371)

### rb...@google.com (2011-10-14)

Nice find, easy fix. ;-). I'll submit a patch for the repo in a few seconds.

### sc...@chromium.org (2011-10-14)

Nice!

Committed as r105521 and DEPS roll is in commit queue:
http://codereview.chromium.org/8298006/

### sc...@chromium.org (2011-10-14)

Windows binaries committed -- rolling DEPS.

### rb...@google.com (2011-10-14)

4 hours have gone since the last commit and no new crashers yet, we may be on to something here. :-).

### sc...@gmail.com (2011-10-14)

Beware -- Aki's probably on the European timezone and his machine is probably running whilst he sleeps :D

### sc...@chromium.org (2011-10-14)

internal/external DEPS roll complete!

woo! marking as fixed

when we're ready we'll need to update M15 DEPS to pull in new FFmpeg code

### sc...@chromium.org (2011-10-14)

fixed for realz

### sc...@chromium.org (2011-10-14)

M15 DEPS ready to land when we're satisfied w/ trunk
https://chromereviews.googleplex.com/3594016

### sc...@chromium.org (2011-10-14)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-15)

[Empty comment from Monorail migration]

### sc...@chromium.org (2011-10-17)

Merged into 874 as r18655.

### in...@chromium.org (2011-10-17)

Thanks Andrew for merging.

### sc...@gmail.com (2012-01-23)

@aohelin: thanks for your help here; from the bug history, seems like your repros caught an issue other than the one we had under control :) Hence, a $1000 Chromium Security Reward.

### ao...@gmail.com (2012-01-23)

@scarybeasts excellent, thanks :)

### sc...@gmail.com (2012-02-16)

Catching up on reward payment, Aki. A $7133.70 batch on its way to way! Thanks again for your continuing awesomeness :D

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=18587

------------------------------------------------------------------------
r18587 | scherkus@google.com | 2011-10-14T22:37:58.644857Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=18588

------------------------------------------------------------------------
r18588 | scherkus@google.com | 2011-10-14T22:47:17.831542Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=18655

------------------------------------------------------------------------
r18655 | scherkus@google.com | 2011-10-17T20:34:50.777565Z

------------------------------------------------------------------------

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-05-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/99652?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals>Media]
[Monorail mergedwith: crbug.com/chromium/100003]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096058)*
