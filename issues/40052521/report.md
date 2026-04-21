# Security: heap-use-after-free / double-free in blink::CanvasResourceProvider

| Field | Value |
|-------|-------|
| **Issue ID** | [40052521](https://issues.chromium.org/issues/40052521) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas, Internals>Instrumentation>Memory |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ta...@google.com |
| **Created** | 2020-06-08 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Crashes into either asan double-free or heap-buffer-overflow errors in blink::CanvasResourceProvider

**VERSION**  

linux-release\_asan-linux-release-775897

**REPRODUCTION CASE**  

chrome file:///tmp/canvas\_bug.html

ADDITIONAL INFORMATION

heap bof:

# [15553:15585:0607/110937.564095:ERROR:bus.cc(393)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix") [15553:15585:0607/110937.564220:ERROR:bus.cc(393)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix") [15553:15585:0607/110937.624664:ERROR:bus.cc(393)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix") [15553:15585:0607/110937.624779:ERROR:bus.cc(393)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix") [15580:15580:0607/110937.690683:ERROR:sandbox\_linux.cc(374)] InitializeSandbox() called with multiple threads in process gpu-process. [15553:15639:0607/110937.847025:ERROR:object\_proxy.cc(621)] Failed to call method: org.freedesktop.DBus.Properties.Get: object\_path= /org/freedesktop/UPower: org.freedesktop.DBus.Error.ServiceUnknown: T he name org.freedesktop.UPower was not provided by any .service files [15553:15639:0607/110937.849045:ERROR:object\_proxy.cc(621)] Failed to call method: org.freedesktop.UPower.GetDisplayDevice: object\_path= /org/freedesktop/UPower: org.freedesktop.DBus.Error.ServiceUnknow n: The name org.freedesktop.UPower was not provided by any .service files [15553:15639:0607/110937.849863:ERROR:object\_proxy.cc(621)] Failed to call method: org.freedesktop.UPower.EnumerateDevices: object\_path= /org/freedesktop/UPower: org.freedesktop.DBus.Error.ServiceUnknow n: The name org.freedesktop.UPower was not provided by any .service files

==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x603000716eb8 at pc 0x55aaf03e75fe bp 0x7f8a3be8c120 sp 0x7f8a3be8c118  

READ of size 8 at 0x603000716eb8 thread T57 (DedicatedWorker)  

==1==WARNING: invalid path to external symbolizer!  

==1==WARNING: Failed to use and restart external symbolizer!  

#0 0x55aaf03e75fd in IsEmptyValue<const blink::CanvasMemoryDumpClient \*> ./../../third\_party/blink/renderer/platform/wtf/hash\_traits.h:350  

#1 0x55aaf03e75fd in IsHashTraitsEmptyValue<WTF::HashTraits<blink::CanvasMemoryDumpClient \*>, const blink::CanvasMemoryDumpClient \*> ./../../third\_party/blink/renderer/platform/wtf/hash\_traits.h:355  

#2 0x55aaf03e75fd in IsEmptyBucket ./../../third\_party/blink/renderer/platform/wtf/hash\_table.h:666  

#3 0x55aaf03e75fd in IsEmptyOrDeletedBucket ./../../third\_party/blink/renderer/platform/wtf/hash\_table.h:673  

#4 0x55aaf03e75fd in IsEmptyOrDeletedBucket ./../../third\_party/blink/renderer/platform/wtf/hash\_table.h:841  

#5 0x55aaf03e75fd in RehashTo ./../../third\_party/blink/renderer/platform/wtf/hash\_table.h:1829  

#6 0x55aaf03e75fd in ?? ??:0  

#7 0x55aafe7eea81 in blink::CanvasResourceProvider::~CanvasResourceProvider() ./../../third\_party/blink/renderer/platform/graphics/canvas\_resource\_provider.cc:991  

#8 0x55aafe7eea81 in ?? ??:0  

#9 0x55aafe7e9433 in ~CanvasResourceProviderSharedImage ./../../third\_party/blink/renderer/platform/graphics/canvas\_resource\_provider.cc:215  

#10 0x55aafe7e9433 in ~CanvasResourceProviderSharedImage ./../../third\_party/blink/renderer/platform/graphics/canvas\_resource\_provider.cc:215  

#11 0x55aafe7e9433 in ?? ??:0  

#12 0x55aafe7dccc4 in operator() ./../../buildtools/third\_party/libc++/trunk/include/memory:2378  

#13 0x55aafe7dccc4 in reset ./../../buildtools/third\_party/libc++/trunk/include/memory:2633  

#14 0x55aafe7dccc4 in operator= ./../../buildtools/third\_party/libc++/trunk/include/memory:2591  

#15 0x55aafe7dccc4 in DiscardResourceProvider ./../../third\_party/blink/renderer/platform/graphics/canvas\_resource\_host.cc:38  

#16 0x55aafe7dccc4 in ?? ??:0  

#17 0x55ab020974a3 in blink::OffscreenCanvasRenderingContext2D::TransferToImageBitmap(blink::ScriptState\*) ./../../third\_party/blink/renderer/modules/canvas/offscreencanvas2d/offscreen\_canvas\_rendering\_context\_2d.cc:234  

#18 0x55ab020974a3 in ?? ??:0  

#19 0x55aaffb1292c in blink::OffscreenCanvas::transferToImageBitmap(blink::ScriptState\*, blink::ExceptionState&) ./../../third\_party/blink/renderer/core/offscreencanvas/offscreen\_canvas.cc:207  

#20 0x55aaffb1292c in ?? ??:0  

#21 0x55aafd31cb11 in TransferToImageBitmapMethod ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_offscreen\_canvas.cc:141  

#22 0x55aafd31cb11 in TransferToImageBitmapMethodCallback ./gen/third\_party/blink/renderer/bindings/core/v8/v8\_offscreen\_canvas.cc:265  

#23 0x55aafd31cb11 in ?? ??:0  

#24 0x55aaee2a6890 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:158  

#25 0x55aaee2a6890 in ?? ??:0  

#26 0x55aaee2a43e8 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) ./../../v8/s

... see attached bof.trace\_symbolized

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11f525fd)  

Shadow bytes around the buggy address:  

0x0c06800dad80: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa  

0x0c06800dad90: fd fd fd fd fa fa fd fd fd fd fa fa fd fd fd fd  

0x0c06800dada0: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd  

0x0c06800dadb0: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa  

0x0c06800dadc0: 00 00 00 00 fa fa fd fd fd fd fa fa fd fd fd fd  

=>0x0c06800dadd0: fa fa 00 00 00 00 fa[fa]fd fd fd fa fa fa fd fd  

0x0c06800dade0: fd fa fa fa 00 00 00 fc fa fa fd fd fd fa fa fa  

0x0c06800dadf0: fd fd fd fa fa fa 00 00 00 fa fa fa fa fa fa fa  

0x0c06800dae00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c06800dae10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c06800dae20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

Shadow gap: cc  

==1==ABORTING

double free:

=================================================================  

==1==ERROR: AddressSanitizer: attempting double-free on 0x6060006eb9a0 in thread T40 (DedicatedWorker):  

==1==WARNING: invalid path to external symbolizer!  

==1==WARNING: Failed to use and restart external symbolizer!  

#0 0x56533fe6319d (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x954e19d)  

#1 0x56534886757b (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11f5257b)  

#2 0x565356c6ea81 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x20359a81)  

#3 0x565356c69433 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x20354433)  

#4 0x565356c5ccc4 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x20347cc4)  

#5 0x56535a5174a3 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x23c024a3)  

#6 0x565357f9292c (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x2167d92c)  

#7 0x56535579cb11 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1ee87b11)  

#8 0x565346726890 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xfe11890)  

#9 0x5653467243e8 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xfe0f3e8)  

#10 0x565346721f4d (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xfe0cf4d)  

#11 0x565348737537 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11e22537)  

#12 0x5653486cca94 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11db7a94)  

#13 0x5653486ca5d9 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11db55d9)  

#14 0x5653486ca3b7 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11db53b7)  

#15 0x5653469c3fa9 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x100aefa9)  

#16 0x5653469c2ed0 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x100aded0)  

#17 0x56534660dc04 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xfcf8c04)  

#18 0x565354cc8c12 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1e3b3c12)  

#19 0x565355fc51a3 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1f6b01a3)  

#20 0x56535570984c (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1edf484c)  

#21 0x56535570cb63 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1edf7b63)  

#22 0x5653563168c4 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1fa018c4)  

#23 0x5653563147a1 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1f9ff7a1)  

#24 0x565356314381 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1f9ff381)  

#25 0x56535884eb9f (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f39b9f)  

#26 0x5653588278aa (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f128aa)  

#27 0x5653588204fc (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f0b4fc)  

#28 0x56534a80f3cd (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13efa3cd)  

#29 0x56534a8481c8 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13f331c8)  

#30 0x56534a847afc (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13f32afc)  

#31 0x56534a7491c0 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13e341c0)  

#32 0x56534a8493e8 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13f343e8)  

#33 0x56534a7bfe6a (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13eaae6a)  

#34 0x565348a83af5 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1216eaf5)  

#35 0x56534a91c241 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x14007241)  

#36 0x7f98df3e86da (/lib/x86\_64-linux-gnu/libpthread.so.0+0x76da)

0x6060006eb9a0 is located 0 bytes inside of 64-byte region [0x6060006eb9a0,0x6060006eb9e0)  

freed by thread T41 (DedicatedWorker) here:  

#0 0x56533fe6319d (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x954e19d)  

#1 0x56534886757b (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11f5257b)  

#2 0x565356c6ea81 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x20359a81)  

#3 0x565356c69433 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x20354433)  

#4 0x565356c5ccc4 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x20347cc4)  

#5 0x56535a5174a3 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x23c024a3)  

#6 0x565357f9292c (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x2167d92c)  

#7 0x56535579cb11 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1ee87b11)  

#8 0x565346726890 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xfe11890)  

#9 0x5653467243e8 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xfe0f3e8)  

#10 0x565346721f4d (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xfe0cf4d)  

#11 0x565348737537 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11e22537)  

#12 0x5653486cca94 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11db7a94)  

#13 0x5653486ca5d9 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11db55d9)  

#14 0x5653486ca3b7 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11db53b7)  

#15 0x5653469c3fa9 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x100aefa9)  

#16 0x5653469c2ed0 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x100aded0)  

#17 0x56534660dc04 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xfcf8c04)  

#18 0x565354cc8c12 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1e3b3c12)  

#19 0x565355fc51a3 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1f6b01a3)  

#20 0x56535570984c (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1edf484c)  

#21 0x56535570cb63 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1edf7b63)  

#22 0x5653563168c4 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1fa018c4)  

#23 0x5653563147a1 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1f9ff7a1)  

#24 0x565356314381 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1f9ff381)  

#25 0x56535884eb9f (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f39b9f)  

#26 0x5653588278aa (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f128aa)  

#27 0x5653588204fc (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f0b4fc)  

#28 0x56534a80f3cd (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13efa3cd)  

#29 0x56534a8481c8 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13f331c8)

previously allocated by thread T41 (DedicatedWorker) here:  

#0 0x56533fe6341d (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x954e41d)  

#1 0x56534efb2459 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1869d459)  

#2 0x565348867224 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11f52224)  

#3 0x565348866e9c (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11f51e9c)  

#4 0x5653488666cd (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11f516cd)  

#5 0x565356c689e7 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x203539e7)  

#6 0x565356c5e3d7 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x203493d7)  

#7 0x565357f9474f (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x2167f74f)  

#8 0x56535a517f39 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x23c02f39)  

#9 0x56535a3677a4 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x23a527a4)  

#10 0x56535a4f88ba (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x23be38ba)  

#11 0x565346726890 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xfe11890)  

#12 0x5653467243e8 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xfe0f3e8)  

#13 0x565346721f4d (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xfe0cf4d)  

#14 0x565348737537 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11e22537)  

#15 0x5653486cca94 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11db7a94)  

#16 0x5653486ca5d9 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11db55d9)  

#17 0x5653486ca3b7 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11db53b7)  

#18 0x5653469c3fa9 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x100aefa9)  

#19 0x5653469c2ed0 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x100aded0)  

#20 0x56534660dc04 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xfcf8c04)  

#21 0x565354cc8c12 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1e3b3c12)  

#22 0x565355fc51a3 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1f6b01a3)  

#23 0x56535570984c (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1edf484c)  

#24 0x56535570cb63 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1edf7b63)  

#25 0x5653563168c4 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1fa018c4)  

#26 0x5653563147a1 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1f9ff7a1)  

#27 0x565356314381 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1f9ff381)  

#28 0x56535884eb9f (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f39b9f)  

#29 0x5653588278aa (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f128aa)

Thread T40 (DedicatedWorker) created by T0 (chrome) here:  

#0 0x56533fe4e2ca (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x95392ca)  

#1 0x56534a91b4ce (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x140064ce)  

#2 0x56534a89ac92 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13f85c92)  

#3 0x565348a82055 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1216d055)  

#4 0x5653489f0cda (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x120dbcda)  

#5 0x5653588427d6 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f2d7d6)  

#6 0x56535882caa2 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f17aa2)  

#7 0x5653588202ed (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f0b2ed)  

#8 0x56535883c3bb (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f273bb)  

#9 0x56535881cb56 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f07b56)  

#10 0x5653587fe005 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21ee9005)  

#11 0x5653588479b6 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f329b6)  

#12 0x565357f5215c (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x2163d15c)  

#13 0x5653488c00c9 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11fab0c9)  

#14 0x5653488fa1da (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11fe51da)  

#15 0x56534892a1d0 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x120151d0)  

#16 0x56534896731a (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1205231a)  

#17 0x56534892a339 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x12015339)  

#18 0x565359de6a36 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x234d1a36)  

#19 0x565359def6c9 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x234da6c9)  

#20 0x565359dfeda5 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x234e9da5)  

#21 0x56534265c072 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xbd47072)  

#22 0x5653415cb4c1 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xacb64c1)  

#23 0x56534acc4ca0 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143afca0)  

#24 0x56534acd1356 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143bc356)  

#25 0x56534acdca4c (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143c7a4c)  

#26 0x56534acdb2d6 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143c62d6)  

#27 0x56534acd1356 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143bc356)  

#28 0x56534acbe2f6 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143a92f6)  

#29 0x56534acbfc67 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143aac67)  

#30 0x56534ad2162f (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1440c62f)  

#31 0x56534a80f3cd (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13efa3cd)  

#32 0x56534a8481c8 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13f331c8)  

#33 0x56534a847afc (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13f32afc)  

#34 0x56534a7491c0 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13e341c0)  

#35 0x56534a8493e8 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13f343e8)  

#36 0x56534a7bfe6a (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13eaae6a)  

#37 0x56535b7ec572 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x24ed7572)  

#38 0x565349756ebf (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x12e41ebf)  

#39 0x56534975a225 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x12e45225)  

#40 0x5653498e9c67 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x12fd4c67)  

#41 0x56534975534f (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x12e4034f)  

#42 0x56533fe8f503 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x957a503)  

#43 0x7f98d7afab96 (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)

Thread T41 (DedicatedWorker) created by T0 (chrome) here:  

#0 0x56533fe4e2ca (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x95392ca)  

#1 0x56534a91b4ce (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x140064ce)  

#2 0x56534a89ac92 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13f85c92)  

#3 0x565348a82055 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1216d055)  

#4 0x5653489f0cda (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x120dbcda)  

#5 0x5653588427d6 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f2d7d6)  

#6 0x56535882caa2 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f17aa2)  

#7 0x5653588202ed (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f0b2ed)  

#8 0x56535883c3bb (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f273bb)  

#9 0x56535881cb56 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f07b56)  

#10 0x5653587fe005 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21ee9005)  

#11 0x5653588479b6 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x21f329b6)  

#12 0x565357f5215c (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x2163d15c)  

#13 0x5653488c00c9 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11fab0c9)  

#14 0x5653488fa1da (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x11fe51da)  

#15 0x56534892a1d0 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x120151d0)  

#16 0x56534896731a (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1205231a)  

#17 0x56534892a339 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x12015339)  

#18 0x565359de6a36 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x234d1a36)  

#19 0x565359def6c9 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x234da6c9)  

#20 0x565359dfeda5 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x234e9da5)  

#21 0x56534265c072 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xbd47072)  

#22 0x5653415cb4c1 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0xacb64c1)  

#23 0x56534acc4ca0 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143afca0)  

#24 0x56534acd1356 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143bc356)  

#25 0x56534acdca4c (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143c7a4c)  

#26 0x56534acdb2d6 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143c62d6)  

#27 0x56534acd1356 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143bc356)  

#28 0x56534acbe2f6 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143a92f6)  

#29 0x56534acbfc67 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x143aac67)  

#30 0x56534ad2162f (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x1440c62f)  

#31 0x56534a80f3cd (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13efa3cd)  

#32 0x56534a8481c8 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13f331c8)  

#33 0x56534a847afc (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13f32afc)  

#34 0x56534a7491c0 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13e341c0)  

#35 0x56534a8493e8 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13f343e8)  

#36 0x56534a7bfe6a (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x13eaae6a)  

#37 0x56535b7ec572 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x24ed7572)  

#38 0x565349756ebf (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x12e41ebf)  

#39 0x56534975a225 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x12e45225)  

#40 0x5653498e9c67 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x12fd4c67)  

#41 0x56534975534f (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x12e4034f)  

#42 0x56533fe8f503 (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x957a503)  

#43 0x7f98d7afab96 (/lib/x86\_64-linux-gnu/libc.so.6+0x21b96)

SUMMARY: AddressSanitizer: double-free (/home/dalanath/chrome/asan-linux-release-775897/chrome+0x954e19d)  

==1==ABORTING

**CREDIT INFORMATION**  

Antti Levomäki and Christian Jalio from Forcepoint

## Attachments

- [bof.trace_symbolized](attachments/bof.trace_symbolized) (application/octet-stream, 37.8 KB)
- [double_free.asan_symbolized](attachments/double_free.asan_symbolized) (application/octet-stream, 44.6 KB)
- [canvas_bug.html](attachments/canvas_bug.html) (text/plain, 1.5 KB)

## Timeline

### cl...@chromium.org (2020-06-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5767021075169280.

### mb...@chromium.org (2020-06-08)

[Empty comment from Monorail migration]

[Monorail components: Blink>Canvas]

### mb...@chromium.org (2020-06-09)

[Empty comment from Monorail migration]

### mb...@chromium.org (2020-06-09)

juanmihd: Would you mind taking a look or helping to find another owner for this? I don't see a specific CL that might have caused this, but noticed that you've touched some of the related code recently.

### ju...@chromium.org (2020-06-09)

[Empty comment from Monorail migration]

### ju...@chromium.org (2020-06-09)

The clusterfuzz issue linked in https://crbug.com/chromium/1092385#c1, does not seem to report the same bug as the issue description.

### ju...@chromium.org (2020-06-09)

tasak@, I've seen that you've recently added this CanvasMemoryDumpProvider class, it seems there is a double free of the Hash Table that it's being used inside the MemoryDump. Could you take a look at this?

[Monorail components: Internals>Instrumentation>Memory]

### [Deleted User] (2020-06-09)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bd...@chromium.org (2020-06-25)

@tasak, have you been able to get a chance to look at this?

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### rs...@chromium.org (2020-07-28)

tasak@: Could you please investigate this or find a better owner? We don't like to let security bugs, especially High bugs, go unaddressed for so long.

### go...@chromium.org (2020-07-29)

M85 is already in  Beta and Stable promotion coming soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If yes, please make sure to land the fix & request a merge to M85 ASAP, so the change gets enough beta coverage. Thank you.

### ta...@google.com (2020-07-29)

Sorry. Looking.


### ta...@google.com (2020-07-29)

I'm trying to reproduce the crash locally. Just looking at the above stacktrace, WTF::HashSet<CanvasMemoryDumpClient*> seems to touch "CanvasMemoryDumpClient*" while rehash or WTF::HashSet<> seems to have the issue.


### ta...@google.com (2020-07-29)

I see. 
CanvasMemoryDumpProvider shoud be thread-safe, but currently thread-unsafe. Register and Unregister will be invoked by different threads and ... WTF::HashSet is also thread-unsafe. So this crash will occur.


### ta...@google.com (2020-07-29)

I've just uploaded its fixing CL.
(Added the reviewers to CC.)


### ta...@google.com (2020-07-29)

My CL is https://chromium-review.googlesource.com/c/chromium/src/+/2324689/


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/943646ed1cfdd38dd84a83e38daa31e3cdc55844

commit 943646ed1cfdd38dd84a83e38daa31e3cdc55844
Author: Takashi Sakamoto <tasak@google.com>
Date: Wed Jul 29 12:11:24 2020

CanvasMemoryDumpProvider should be thread-safe.

RegisterClient and UnregisterClient methods will be invoked in different threads at the same time. This causes ASAN crashes.

Bug: 1092385
Change-Id: I67ed7fd1925bde72770c8c5b4f737258e9564de5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2324689
Commit-Queue: Takashi Sakamoto <tasak@google.com>
Reviewed-by: Bartek Nowierski <bartekn@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#792654}

[modify] https://crrev.com/943646ed1cfdd38dd84a83e38daa31e3cdc55844/third_party/blink/renderer/platform/instrumentation/canvas_memory_dump_provider.cc
[modify] https://crrev.com/943646ed1cfdd38dd84a83e38daa31e3cdc55844/third_party/blink/renderer/platform/instrumentation/canvas_memory_dump_provider.h


### ta...@google.com (2020-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-29)

Requesting merge to beta M85 because latest trunk commit (792654) appears to be after beta branch point (782793).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-29)

This bug requires manual review: M85's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2020-07-29)

+adetaylor@ (Security TPM) for M85 merge review. CL listed at #19 landed 7 hrs back not in canary yet. Thank you.

### ad...@chromium.org (2020-07-29)

Please merge to M85, branch 4183, after this has had a day of canary coverage.

### go...@chromium.org (2020-07-30)

Please merge your change to M85 branch 4183 ASAP. Thank you.

### ta...@google.com (2020-07-31)

Yeah, I waited for 1 day and no issue was filed. I will merge now.


### ta...@google.com (2020-07-31)

I've just created a cherry-pick: https://chromium-review.googlesource.com/c/chromium/src/+/2330876 


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a6a0366d8576c276cf17f69e8bb77b89bd69bc7f

commit a6a0366d8576c276cf17f69e8bb77b89bd69bc7f
Author: Takashi Sakamoto <tasak@google.com>
Date: Fri Jul 31 03:45:56 2020

CanvasMemoryDumpProvider should be thread-safe.

RegisterClient and UnregisterClient methods will be invoked in different threads at the same time. This causes ASAN crashes.

(cherry picked from commit 943646ed1cfdd38dd84a83e38daa31e3cdc55844)

Bug: 1092385
Change-Id: I67ed7fd1925bde72770c8c5b4f737258e9564de5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2324689
Commit-Queue: Takashi Sakamoto <tasak@google.com>
Reviewed-by: Bartek Nowierski <bartekn@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#792654}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2330876
Reviewed-by: Takashi Sakamoto <tasak@google.com>
Cr-Commit-Position: refs/branch-heads/4183@{#1080}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/a6a0366d8576c276cf17f69e8bb77b89bd69bc7f/third_party/blink/renderer/platform/instrumentation/canvas_memory_dump_provider.cc
[modify] https://crrev.com/a6a0366d8576c276cf17f69e8bb77b89bd69bc7f/third_party/blink/renderer/platform/instrumentation/canvas_memory_dump_provider.h


### ta...@google.com (2020-07-31)

I'm looking at https://luci-milo.appspot.com/p/chrome/builders/ci/win64-beta/7008.


### ta...@google.com (2020-07-31)

No compilaiton error. However InstallServiceWorkItemTest.Do_FreshInstall failure was found. I'm looking at it.



### ta...@google.com (2020-07-31)

https://ci.chromium.org/p/chrome/builders/ci/win64-beta/7009 didn't s ow  InstallServiceWorkItemTest.Do_FreshInstall failure. The test looks flaky.
I think this issue is fixed and the patch was correctly merged.



### ad...@google.com (2020-08-03)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-08-05)

tasak@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-08-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-05)

Congratulations! The VRP panel has decided to award you $5000 for this bug.

### ad...@google.com (2020-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1092385?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Canvas, Internals>Instrumentation>Memory]
[Monorail mergedwith: crbug.com/chromium/1092419]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052521)*
