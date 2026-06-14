# Portrait photos (taken by Pixel3aXL) with EXIF crash on Desktop

| Field | Value |
|-------|-------|
| **Issue ID** | [40053265](https://issues.chromium.org/issues/40053265) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | zu...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2020-09-06 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36

Example URL:
http://ik1-333-26678.vs.sakura.ne.jp/ImageLoadTest/

Steps to reproduce the problem:
1. Select Filechooser button.
2. Select portrait photo attached this ticket.
3. If you use chrome on Mac, web application will shutting down. If you use chrome on Android, broken image appear.

What is the expected behavior?
Load and show image correctly.

What went wrong?
The expected behavior is loading image correctly. This problem just cause if I use portrait photo which taken by Pixel3aXL. If I use landscape photo that taken by Pixel3aXL, this problem not cause.

Does it occur on multiple sites: N/A

Is it a problem with a plugin? No 

Did this work before? N/A 

Does this work in other browsers? Yes

Chrome version: 84.0.4147.135  Channel: n/a
OS Version: OS X 10.15.6
Flash Version: 

I use Construct3 to develop this applicaton, so I reported their bug report system too.
https://github.com/Scirra/Construct-3-bugs/issues/4160

But they think it is Chrome problem because it work correctly other browsers.

## Attachments

- [IMG_20200828_193925.jpg](attachments/IMG_20200828_193925.jpg) (image/jpeg, 1.7 MB)
- [IMG_20200828_193928.jpg](attachments/IMG_20200828_193928.jpg) (image/jpeg, 1.7 MB)
- [1125337.mp4](attachments/1125337.mp4) (video/mp4, 907.0 KB)
- [exif-orientation-resources.zip](attachments/exif-orientation-resources.zip) (application/octet-stream, 81.7 KB)
- [bug.html](attachments/bug.html) (text/plain, 19.0 KB)

## Timeline

### sw...@chromium.org (2020-09-06)

[Empty comment from Monorail migration]

### al...@chromium.org (2020-09-07)

Able to reproduce the issue on reported Chrome version #84.0.4147.135 using Mac Mojave 10.14.6 as per steps mentioned in https://crbug.com/chromium/1125337#c0. 

Reproducible in:
--------------------------
Canary #87.0.4256.0
Dev #87.0.4252.0
Beta #86.0.4240.22
Stable #85.0.4183.83

Bisect information:
-------------------------------
Good Build: 84.0.4146.0  
Bad Build: 84.0.4147.0   

You are probably looking for a change made after 768688 (known good), but no later than 768689 (first known bad)
Change log: https://chromium.googlesource.com/chromium/src/+log/ce0438fbe6a73cef3324c219ed20ab2e4a331779..4b1c55f5bd3f608a7704f5b155bf21c6a350ce7d
Change-Id: I4dd59766769bbb7175d8216845f19f9122129e16
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2198654

schenney@ Please help us in reassigning the issue if it is not related to your change.


Thanks..!

[Monorail components: Blink>Image]

### sc...@chromium.org (2020-09-07)

Linux crashes also. The portrait image has EXIF data to orient it correctly. My guess is that the page is trying to convert the image somehow and failing now that Chrome by default will respect the image orientation found in EXIF data.

### as...@scirra.com (2020-09-07)

We make the framework used for the submission. FWIW as far as I can tell the problem is: we call createImageBitmap() on the image, then upload it to a WebGL texture with texSubImage2D, which is the method it crashes in. Could well be that it gets the wrong orientation and uploads with the wrong data layout.

### sc...@chromium.org (2020-09-08)

Crash stack:
[5196:775:0907/211642.537902:INFO:CONSOLE(1313)] "[C3 runtime] Hosted in DOM, rendering with WebGL 2 [ANGLE (ATI Technologies Inc., AMD Radeon Pro 560X OpenGL Engine, OpenGL 4.1 core)] (standard compositing)", source: http://ik1-333-26678.vs.sakura.ne.jp/ImageLoadTest/scripts/c3runtime.js (1313)
[5234:775:0907/211646.477780:ERROR:gles2_cmd_decoder_passthrough_doers.cc(3729)] Not implemented reached in error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoSetDisjointValueSyncCHROMIUM(gpu::gles2::DisjointValueSync *)
Received signal 11 SEGV_MAPERR 7fd6dbf48000
0   libbase.dylib                       0x0000000109abbb5f base::debug::CollectStackTrace(void**, unsigned long) + 31
1   libbase.dylib                       0x00000001097d9f8b base::debug::StackTrace::StackTrace(unsigned long) + 75
2   libbase.dylib                       0x00000001097da00d base::debug::StackTrace::StackTrace(unsigned long) + 29
3   libbase.dylib                       0x00000001097d9fe8 base::debug::StackTrace::StackTrace() + 40
4   libbase.dylib                       0x0000000109abba06 base::debug::(anonymous namespace)::StackDumpSignalHandler(int, __siginfo*, void*) + 1414
5   libsystem_platform.dylib            0x00007fff6e46a5fd _sigtramp + 29
6   ???                                 0x00000026e7600000 0x0 + 167090585600
7   libblink_platform.dylib             0x00000001affd0484 void blink::(anonymous namespace)::Unpack<18, unsigned char, unsigned char>(unsigned char const*, unsigned char*, unsigned int) + 84
8   libblink_platform.dylib             0x00000001b0074b5a void blink::(anonymous namespace)::FormatConverter::Convert<(blink::WebGLImageConversion::DataFormat)18, (blink::WebGLImageConversion::DataFormat)0, (blink::WebGLImageConversion::AlphaOp)0>() + 1002
9   libblink_platform.dylib             0x00000001b0067683 void blink::(anonymous namespace)::FormatConverter::Convert<(blink::WebGLImageConversion::DataFormat)18, (blink::WebGLImageConversion::DataFormat)0>(blink::WebGLImageConversion::AlphaOp) + 99
10  libblink_platform.dylib             0x00000001affd3739 void blink::(anonymous namespace)::FormatConverter::Convert<(blink::WebGLImageConversion::DataFormat)18>(blink::WebGLImageConversion::DataFormat, blink::WebGLImageConversion::AlphaOp) + 313
11  libblink_platform.dylib             0x00000001affcfefa blink::(anonymous namespace)::FormatConverter::Convert(blink::WebGLImageConversion::DataFormat, blink::WebGLImageConversion::DataFormat, blink::WebGLImageConversion::AlphaOp) + 218
12  libblink_platform.dylib             0x00000001affce9aa blink::WebGLImageConversion::PackPixels(unsigned char const*, blink::WebGLImageConversion::DataFormat, unsigned int, unsigned int, blink::IntRect const&, int, unsigned int, int, unsigned int, unsigned int, blink::WebGLImageConversion::AlphaOp, void*, bool) + 1674
13  libblink_platform.dylib             0x00000001affcec97 blink::WebGLImageConversion::ExtractImageData(unsigned char const*, blink::WebGLImageConversion::DataFormat, blink::IntSize const&, blink::IntRect const&, int, int, unsigned int, unsigned int, bool, bool, WTF::Vector<unsigned char, 0u, WTF::PartitionAllocator>&) + 615
14  libblink_modules.dylib              0x00000001bc7aa70b blink::WebGLRenderingContextBase::TexImageHelperImageBitmap(blink::WebGLRenderingContextBase::TexImageFunctionID, unsigned int, int, int, unsigned int, unsigned int, int, int, int, blink::ImageBitmap*, blink::IntRect const&, int, int, blink::ExceptionState&) + 2571
15  libblink_modules.dylib              0x00000001bc7ac3c4 blink::WebGLRenderingContextBase::texSubImage2D(unsigned int, int, int, int, unsigned int, unsigned int, blink::ImageBitmap*, blink::ExceptionState&) + 276
16  libblink_modules.dylib              0x00000001bc7317df blink::WebGL2RenderingContextBase::texSubImage2D(unsigned int, int, int, int, unsigned int, unsigned int, blink::ImageBitmap*, blink::ExceptionState&) + 223
17  libblink_modules.dylib              0x00000001bafccf5f blink::(anonymous namespace)::TexSubImage2DOperationOverload7(v8::FunctionCallbackInfo<v8::Value> const&) + 5055
18  libblink_modules.dylib              0x00000001baf31e52 blink::(anonymous namespace)::TexSubImage2DOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) + 8994
19  libv8.dylib                         0x0000000138b043d9 v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) + 921
20  libv8.dylib                         0x0000000138b025e6 v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) + 2038
21  libv8.dylib                         0x0000000138b0054a v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) + 490
22  libv8.dylib                         0x0000000138b00068 v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) + 152
23  libv8.dylib                         0x00000001384cbf9f Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit + 63
24  libv8.dylib                         0x0000000138217d58 Builtins_InterpreterEntryTrampoline + 216
[end of stack trace]
[0907/211744.082523:WARNING:process_memory_mac.cc(93)] mach_vm_read(0x7ffee759c000, 0x2000): (os/kern) invalid address (1)

Indeed, this is a WebGL crash, not even clear that it's in Chromium code.

I'm pretty sure that if you use canvas to display the image it will work correctly, because Chrome displays it fine if you just load the image as an image.

[Monorail components: -Blink>Image Blink>WebGL]

### en...@chromium.org (2020-09-08)

The call to gpu::gles2::GLES2DecoderPassthroughImpl::DoSetDisjointValueSyncCHROMIUM doesn't seem relevant.

Looks like it's calling Unpack on kDataFormatBGRA8

https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/platform/graphics/gpu/webgl_image_conversion.cc;l=882;drc=36c0310725bd6a03de6c11dae1d4986e7e64bb18;bpv=1;bpt=1

If it's working for landscape but not portrait, it seems reasonably there's a bug in the unpack code or the code which computes and allocates the destination size.


### en...@chromium.org (2020-09-08)

ImageBitmap::width/height use SizeRespectingOrientation, but ImageBitmap::Size does not.
https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/imagebitmap/image_bitmap.cc;l=1093

We're passing in the oriented source dimensions here: https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc;l=6046;drc=36c0310725bd6a03de6c11dae1d4986e7e64bb18;bpv=1;bpt=1?q=f:webgl_rendering_context_Base

But then using the unoriented source dimensions here:
https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc;l=6011;drc=36c0310725bd6a03de6c11dae1d4986e7e64bb18;bpv=1;bpt=1?q=f:webgl_rendering_context_Base

We compute the destination size using the oriented source dimensions here, though the row alignment is 1 so it shouldn't matter if we use the transpose.
https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/platform/graphics/gpu/webgl_image_conversion.cc;l=3959;drc=36c0310725bd6a03de6c11dae1d4986e7e64bb18;bpv=1;bpt=1

Then, the source stride is computed using the unoriented dimensions, and the destination stride is computed using the oriented dimensions.
And the unpack operation goes row-by-row using the oriented dimensions' width/height.

the image in provided is 3840 x 2160, rotated to be 2160 x 3840,
                                             (unoriented)                          (oriented)

which means Chromium's code will copy 3840 rows, 2160 texels wide, but strided by 3840 texels -- and it overruns the destination buffer. This code is both wrong, and also requires a destination of 3840 x 3840, not 3840 x 2160.


### en...@chromium.org (2020-09-08)

Adding security labels and CC'ing WebGL team members for visibility.

### en...@chromium.org (2020-09-08)

[Empty comment from Monorail migration]

### en...@chromium.org (2020-09-08)

Reassigning to schenney@. Looks like https://chromium-review.googlesource.com/c/chromium/src/+/2198654 changed ImageBitmap.width and .height to report oriented sizes, but perhaps should have changed ImageBitmap::Size, or updated existing usages of width/height/Size to match oriented/unoriented.

### kb...@chromium.org (2020-09-08)

Is this the same bug as https://crbug.com/chromium/1100470? Started work on that, but got stalled a bit with other priorities.


### en...@chromium.org (2020-09-08)

I think it's very related though not exactly the same. This one overwrites the destination buffer because the sizes it's using for calculation are mismatched. However, that's a little different from reading back the ImageBitmap content column-by-column (one possible solution) instead of row-by-row to account for a 90 degree rotation.

### sc...@chromium.org (2020-09-08)

It may or may not be the same issue as 1100470, though it is related in the sense the WebGL doesn't handle image-orientation in general.

Regarding ImageBitmap.width and ImageBitmap.height, we need to choose something and the choice is the new default. It's unfortunate until we can address the WebGL issue but somewhat unavoidable without spec work (that admittedly I have lax on following through with).

So the fix is to make sure that the various methods in https://crbug.com/chromium/1125337#c7 all agree on the dimensions? Does it matter if the image data actually matches those dimensions for non-square images (beyond the total size matching)?

### en...@chromium.org (2020-09-09)

I think that as long as the dimensions match, we'll be okay with the buffer overflow, but we will still have the problem in https://crbug.com/chromium/1100470 where the image is not actually rotated. Though, even if they match but we choose the oriented dimensions instead of the unoriented dimension, the rows will probably be both rotated and very skewed since we'll be copying column data as row data.

### kb...@chromium.org (2020-09-09)

Should we attempt to fix this before or after https://crbug.com/chromium/1100470?

I'd like to just conclusively extract the correctly-oriented data from these images. Realistically though with other administrative deadlines I'm not going to get to https://crbug.com/chromium/1100470 in the next week or two.


### sc...@chromium.org (2020-09-09)

I'll investigate fixing this next after the thing I'm on now. Probably next week. I need to write code to pre-rotate the image for a background painting issue and it's probably the same code can be used to fix the WebGL issue. We also need to pre-rotate for a security/privacy issue.

### kb...@chromium.org (2020-09-09)

OK. In case they're useful, here are the image resources I created for a WebGL conformance test for https://crbug.com/chromium/1100470 but haven't yet had time to put into a test.


### sc...@chromium.org (2020-09-21)

[Empty comment from Monorail migration]

### fs...@opera.com (2020-09-21)

@ https://crbug.com/chromium/1125337#c16 : We have Image::ResizeAndOrientImage which ought be a (more generic version) of that. (As used by for example Image::AsSkBitmapForCurrentFrame to achieve something similar.)

### sc...@chromium.org (2020-09-21)

Right, I knew there was code somewhere to explicitly rotate the image, and the issue is hooking everything up. Sorry I wasn't clearer.

### kb...@chromium.org (2020-09-23)

schenney@ can you provide any progress update on this bug? Should I be looking into it instead?


### ad...@google.com (2020-09-24)

Yep it would be great to have an update here. It's really not good to have image formats which can cause potentially exploitable crashes in the renderer, because it's so easy for attackers to arrange for images to be injected into Chrome by so many different mechanisms. I'd really like to get this fix into the first M86 build.

### sc...@chromium.org (2020-09-24)

I'll probably get to it in the next 2 working days. I might need some help
with tests.

Stephen.

### sc...@chromium.org (2020-09-30)

[Empty comment from Monorail migration]

### kb...@chromium.org (2020-10-02)

Since this bug is restricted view, but https://crbug.com/chromium/1100470 which depends on it is not, posting this here separately:

A comprehensive WebGL-based test case for this is up for review at https://github.com/KhronosGroup/WebGL/pull/3155 .

It can be tested locally by merging it into a local clone of the repository, serving it up locally with an HTTP server, and navigating to (assuming on port 8080):
http://localhost:8080/sdk/tests/conformance/textures/misc/exif-orientation.html

schenney@, appreciate your help on this. It's not necessary for you to fix all of the cases if that's difficult; let me know how we can share the work.


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/be406827420af365918ac296376b83406ce1d1a5

commit be406827420af365918ac296376b83406ce1d1a5
Author: Kenneth Russell <kbr@chromium.org>
Date: Sat Oct 03 02:16:33 2020

Roll WebGL 71413e9..91b544d

https://chromium.googlesource.com/external/khronosgroup/webgl.git/+log/71413e9..91b544d

Bug: 1100470, 1125337
Tbr: jdarpinian@chromium.org
Tbr: shrekshao@google.com
Cq-Include-Trybots: luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-angle-rel;luci.chromium.try:win-angle-rel-32;luci.chromium.try:win-angle-rel-64
Change-Id: I185e7703aeeb5eccb59e0286a5fbb4e11a3c08e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2446538
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Reviewed-by: Shrek Shao <shrekshao@google.com>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#813475}

[modify] https://crrev.com/be406827420af365918ac296376b83406ce1d1a5/DEPS
[modify] https://crrev.com/be406827420af365918ac296376b83406ce1d1a5/content/test/gpu/gpu_tests/test_expectations/webgl2_conformance_expectations.txt
[modify] https://crrev.com/be406827420af365918ac296376b83406ce1d1a5/content/test/gpu/gpu_tests/test_expectations/webgl_conformance_expectations.txt
[modify] https://crrev.com/be406827420af365918ac296376b83406ce1d1a5/content/test/gpu/gpu_tests/webgl_conformance_revision.txt


### kb...@chromium.org (2020-10-03)

The WebGL conformance test is in the Chromium tree. Any fixes can be easily tested by following these instructions:

https://chromium.googlesource.com/chromium/src.git/+/master/docs/gpu/gpu_testing.md#Running-the-GPU-Tests-Locally

by removing the Skip expectations added above, and with --test-filter=conformance/textures/exif-orientation.html

or just start an HTTP server pointing at src/third_party/webgl/src/ and loading the test from localhost.


### kb...@chromium.org (2020-10-06)

[Empty comment from Monorail migration]

### kb...@chromium.org (2020-10-06)

A duplicate https://crbug.com/chromium/1130173 was just filed about this issue. Here's the self-contained test case from it.

Per that issue, this test case loads an 800x600 JPEG with blink::ImageOrientation = kOriginRightTop. ImageBitmap reports the size as 600x800, but the underlying code paths which refer to the Image derived from it think it's 800x600, leading to the crash.

frame #0: 0x00000001b90bd2fb libblink_platform.dylib`blink::simd::UnpackOneRowOfBGRA8LittleToRGBA8(source=0x00007ffee21bb008, destination=0x00007ffee21bb000, pixels_per_row=0x00007ffee21bb014) at webgl_image_conversion_sse.h:128:12
   125 	  unsigned pixels_per_row_trunc = (pixels_per_row / 4) * 4;
   126 	
   127 	  for (unsigned i = 0; i < pixels_per_row_trunc; i += 4) {
-> 128 	    bgra = _mm_loadu_si128((const __m128i*)(source));
   129 	    rgba = _mm_shufflehi_epi16(_mm_shufflelo_epi16(bgra, 0xB1), 0xB1);
   130 	
   131 	    rgba = _mm_or_si128(_mm_and_si128(rgba, br_mask),
(lldb) p i
(unsigned int) $14 = 256

(lldb) bt
* thread #1, name = 'CrRendererMain', queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=1, address=0x7fbf801d5000)
  * frame #0: 0x00000001b90bd2fb libblink_platform.dylib`blink::simd::UnpackOneRowOfBGRA8LittleToRGBA8(source=0x00007ffee21bb008, destination=0x00007ffee21bb000, pixels_per_row=0x00007ffee21bb014) at webgl_image_conversion_sse.h:128:12
    frame #1: 0x00000001b8f96a24 libblink_platform.dylib`void blink::(anonymous namespace)::Unpack<18, unsigned char, unsigned char>(source="", destination="", pixels_per_row=600) at webgl_image_conversion.cc:890:3
    frame #2: 0x00000001b903b13a libblink_platform.dylib`void blink::(anonymous namespace)::FormatConverter::Convert<(this=0x00007ffee21bb338)18, (blink::WebGLImageConversion::DataFormat)0, (blink::WebGLImageConversion::AlphaOp)0>() at webgl_image_conversion.cc:3478:9
    frame #3: 0x00000001b902dc63 libblink_platform.dylib`void blink::(anonymous namespace)::FormatConverter::Convert<(this=0x00007ffee21bb338, alpha_op=kAlphaDoNothing)18, (blink::WebGLImageConversion::DataFormat)0>(blink::WebGLImageConversion::AlphaOp) at webgl_image_conversion.cc:3344:5
    frame #4: 0x00000001b8f99d19 libblink_platform.dylib`void blink::(anonymous namespace)::FormatConverter::Convert<(this=0x00007ffee21bb338, dst_format=kDataFormatRGBA8, alpha_op=kAlphaDoNothing)18>(blink::WebGLImageConversion::DataFormat, blink::WebGLImageConversion::AlphaOp) at webgl_image_conversion.cc:3314:5
    frame #5: 0x00000001b8f9649a libblink_platform.dylib`blink::(anonymous namespace)::FormatConverter::Convert(this=0x00007ffee21bb338, src_format=kDataFormatBGRA8, dst_format=kDataFormatRGBA8, alpha_op=kAlphaDoNothing) at webgl_image_conversion.cc:3279:5
    frame #6: 0x00000001b8f94f4a libblink_platform.dylib`blink::WebGLImageConversion::PackPixels(source_data="", source_data_format=kDataFormatBGRA8, source_data_width=800, source_data_height=600, source_data_sub_rectangle=0x00007ffee21bb950, depth=1, source_unpack_alignment=0, unpack_image_height=800, destination_format=6408, destination_type=5121, alpha_op=kAlphaDoNothing, destination_data=0x0000004394a04010, flip_y=false) at webgl_image_conversion.cc:4097:13
    frame #7: 0x00000001b8f95237 libblink_platform.dylib`blink::WebGLImageConversion::ExtractImageData(image_data="", source_data_format=kDataFormatBGRA8, image_data_size=0x00007ffee21bb758, source_image_sub_rectangle=0x00007ffee21bb950, depth=1, unpack_image_height=0, format=6408, type=5121, flip_y=false, premultiply_alpha=false, data=0x00007ffee21bb760) at webgl_image_conversion.cc:3966:8
    frame #8: 0x00000001c5c071fb libblink_modules.dylib`blink::WebGLRenderingContextBase::TexImageHelperImageBitmap(this=0x0000001f75c6da68, function_id=kTexSubImage2D, target=3553, level=0, internalformat=0, format=6408, type=5121, xoffset=0, yoffset=0, zoffset=0, bitmap=0x0000001b726a9708, source_sub_rect=0x00007ffee21bb950, depth=1, unpack_image_height=0, exception_state=0x00007ffee21bc030) at webgl_rendering_context_base.cc:6104:10
    frame #9: 0x00000001c5c08eb4 libblink_modules.dylib`blink::WebGLRenderingContextBase::texSubImage2D(this=0x0000001f75c6da68, target=3553, level=0, xoffset=0, yoffset=0, format=6408, type=5121, bitmap=0x0000001b726a9708, exception_state=0x00007ffee21bc030) at webgl_rendering_context_base.cc:6319:3
...


### kb...@chromium.org (2020-10-06)

[Empty comment from Monorail migration]

### no...@chromium.org (2020-10-06)

EXIF orientation 'F' test images: https://github.com/noell/jpg-exif-test-images


 

### kb...@chromium.org (2020-10-06)

Thanks noel@. A WebGL conformance test was written in https://www.khronos.org/registry/webgl/sdk/tests/conformance/textures/misc/exif-orientation.html / https://github.com/KhronosGroup/WebGL/blob/master/sdk/tests/conformance/textures/misc/exif-orientation.html .


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f373458c504c2d115c42f31b29ff5c19674acbbc

commit f373458c504c2d115c42f31b29ff5c19674acbbc
Author: Stephen Chenney <schenney@chromium.org>
Date: Thu Oct 08 22:45:43 2020

[Image-Orientation] Implement WebGL image-orientation

When creating textures for WebGL, always orient images
with EXIF orientation data.

This change also corrects the transposed size reported by
ImageBitmap. And it removes superfluous arguments from
CopyImageData.

Bug: 1100470, 1125337
Change-Id: I79aa798327a3582939aa574723926b3325c80e7c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2459400
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Stephen Chenney <schenney@chromium.org>
Cr-Commit-Position: refs/heads/master@{#815359}

[modify] https://crrev.com/f373458c504c2d115c42f31b29ff5c19674acbbc/content/test/gpu/gpu_tests/test_expectations/webgl2_conformance_expectations.txt
[modify] https://crrev.com/f373458c504c2d115c42f31b29ff5c19674acbbc/content/test/gpu/gpu_tests/test_expectations/webgl_conformance_expectations.txt
[modify] https://crrev.com/f373458c504c2d115c42f31b29ff5c19674acbbc/third_party/blink/renderer/core/imagebitmap/image_bitmap.cc
[modify] https://crrev.com/f373458c504c2d115c42f31b29ff5c19674acbbc/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc


### sc...@chromium.org (2020-10-08)

Starting by requesting a merge to M-87 once it lives in Canary for a couple of days. Target would be Monday, 10/12/2020.

Then we'll go for M-86 given the security impact. Release managers, if there's a reason to move faster please let me know ASAP. e.g. an M-86 Stable re-spin planned.

### ad...@google.com (2020-10-09)

schenney@ thanks for being proactive! There will be a scheduled M86 stable refresh in about 10 days. I'll approve merge to M87 on Monday and if things are looking good, almost certainly M86 as well for that scheduled refresh.

### [Deleted User] (2020-10-09)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-09)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-10-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-12)

Approving merge to M87. Please merge to branch 4280.

As for M86: schenney@ there will be an Android security refresh cut tomorrow. Does this affect Android? (Does the 'broken image' in the description imply a crash somewhere?) If so, I'm inclined to include it. Please do reply to https://crbug.com/chromium/1125337#c36 or https://crbug.com/chromium/1125337#c38 but the most important thing is any views on stability risks.

### sc...@chromium.org (2020-10-12)

I believe the change does affect Android. So here are the answers.

1. Does your merge fit within the Merge Decision Guidelines?
The change fixes a security and functionality issue rated as Security-SeverityHigh. It affects real sites including Google properties.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2459400

3. Has the change landed and been verified on ToT?
Yes, landed, no issues reported.

4. Does this change need to be merged into other active release branches (M-1, M+1)?
Already in the CQ for M--87. M-86 is the only other active branch.

5. Why are these changes required in this milestone after branch?
Security issue rated as High.

6. Is this a new feature?
No, feature has been present for several releases.

7. If it is a new feature, is it behind a flag using finch?
N/A

### sc...@chromium.org (2020-10-12)

I should add, this is a localized change primarily making use of existing code that has been thoroughly used for a long time.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4fe5ed2c9c5ca452243552dca024b7202c58abee

commit 4fe5ed2c9c5ca452243552dca024b7202c58abee
Author: Stephen Chenney <schenney@chromium.org>
Date: Mon Oct 12 21:37:22 2020

[Image-Orientation] Implement WebGL image-orientation

M-87 merge.

When creating textures for WebGL, always orient images
with EXIF orientation data.

This change also corrects the transposed size reported by
ImageBitmap. And it removes superfluous arguments from
CopyImageData.

(cherry picked from commit f373458c504c2d115c42f31b29ff5c19674acbbc)

Bug: 1100470, 1125337
Change-Id: I79aa798327a3582939aa574723926b3325c80e7c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2459400
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Stephen Chenney <schenney@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#815359}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2464430
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#274}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/4fe5ed2c9c5ca452243552dca024b7202c58abee/third_party/blink/renderer/core/imagebitmap/image_bitmap.cc
[modify] https://crrev.com/4fe5ed2c9c5ca452243552dca024b7202c58abee/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc


### ad...@google.com (2020-10-13)

Thanks. Approving merge to M86, branch 4240.

### sc...@chromium.org (2020-10-13)

M-86 merge is in the queue: https://chromium-review.googlesource.com/c/chromium/src/+/2469776

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f440137cd96a18f64b9931e8f369670197204d55

commit f440137cd96a18f64b9931e8f369670197204d55
Author: Stephen Chenney <schenney@chromium.org>
Date: Wed Oct 14 02:52:47 2020

[Image-Orientation] Implement WebGL image-orientation

M-86 merge.

When creating textures for WebGL, always orient images
with EXIF orientation data.

This change also corrects the transposed size reported by
ImageBitmap. And it removes superfluous arguments from
CopyImageData.

(cherry picked from commit f373458c504c2d115c42f31b29ff5c19674acbbc)

Bug: 1100470, 1125337
Change-Id: I79aa798327a3582939aa574723926b3325c80e7c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2459400
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Stephen Chenney <schenney@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#815359}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2469776
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1237}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/f440137cd96a18f64b9931e8f369670197204d55/third_party/blink/renderer/core/imagebitmap/image_bitmap.cc
[modify] https://crrev.com/f440137cd96a18f64b9931e8f369670197204d55/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc


### ad...@google.com (2020-10-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-14)

zubora.amaebi@gmail.com thanks very much for this bug report. As it turned out to have security implications, it went for consideration with our Vulnerability Rewards Program panel. As it was disclosed elsewhere rather than reported directly to us, it's not technically within the rules of the program, but the VRP panel has nevertheless decided to award $500 as a 'thank you'. Someone from our finance team will get in touch.

You'll also be credited in the next Chrome release notes. How would you like to be credited?

Thanks again!

### zu...@gmail.com (2020-10-16)

adetaylor@google.com 
>VRP panel has nevertheless decided to award $500 as a 'thank you'. Someone from our finance team will get in touch.
Thank you as well. I'm glad I was able to help you. 

>You'll also be credited in the next Chrome release notes. How would you like to be credited?
I don't know the details, but if you are going to credit my name , it would be nice if you use "amaebi_jp".

### ad...@google.com (2020-10-16)

> it would be nice if you use "amaebi_jp".

Perfect, thanks!

### ad...@google.com (2020-10-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-06)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2022-07-15)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1125337?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/158753]
[Monorail blocking: crbug.com/chromium/1100470, crbug.com/chromium/1344973]
[Monorail mergedwith: crbug.com/chromium/1130116, crbug.com/chromium/1130173]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053265)*
