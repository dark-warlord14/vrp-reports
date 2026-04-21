# AddressSanitizer: use-after-poison cc\layers\texture_layer.cc:169 in cc::TextureLayer::Update

| Field | Value |
|-------|-------|
| **Issue ID** | [40058360](https://issues.chromium.org/issues/40058360) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Compositing |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2021-12-29 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4676.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-954268.zip

#Reproduce
1. unzip poc
2. python -m http.server 80
2. chrome --js-flags='--expose_gc --allow-natives-syntax' --no-sandbox --enable-blink-test-features --user-data-dir=notexits http://localhost/fuzz-00001.html

What is the expected behavior?

What went wrong?
ype of crash
render tab

Minipoc
Come soon

#Analysis
Not yet

#Patch
Not yet

#asan
=================================================================
==15896==ERROR: AddressSanitizer: use-after-poison on address 0x7ed800139000 at pc 0x7ffa5b9fe3c1 bp 0x00fe491fe820 sp 0x00fe491fe868
READ of size 8 at 0x7ed800139000 thread T0
==15896==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffa5b9fe3c0 in cc::TextureLayer::Update C:\b\s\w\ir\cache\builder\src\cc\layers\texture_layer.cc:169
    #1 0x7ffa5b988b8e in cc::LayerTreeHost::DoUpdateLayers C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:885
    #2 0x7ffa5b9881a6 in cc::LayerTreeHost::UpdateLayers C:\b\s\w\ir\cache\builder\src\cc\trees\layer_tree_host.cc:749
    #3 0x7ffa5e8dd4ad in cc::ProxyMain::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\proxy_main.cc:315
    #4 0x7ffa627ef2d2 in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::*)(std::__1::unique_ptr<cc::BeginMainFrameAndCommitState,std::__1::default_delete<cc::BeginMainFrameAndCommitState> >),base::WeakPtr<cc::ProxyMain>,std::__1::unique_ptr<cc::BeginMainFrameAndCommitState,std::__1::default_delete<cc::BeginMainFrameAndCommitState> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:741
    #5 0x7ffa592043e4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #6 0x7ffa5bd2eb35 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356
    #7 0x7ffa5bd2e208 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261
    #8 0x7ffa5bd07137 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:38
    #9 0x7ffa5bd30201 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468
    #10 0x7ffa59182f53 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140
    #11 0x7ffa5b7fe732 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:283
    #12 0x7ffa54e29b59 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:678
    #13 0x7ffa54e2b72f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1028
    #14 0x7ffa54e279ad in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #15 0x7ffa54e28a38 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:426
    #16 0x7ffa4e6e148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177
    #17 0x7ff69a225b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #18 0x7ff69a222b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #19 0x7ff69a62753f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #20 0x7ffb038c7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #21 0x7ffb04162650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

Address 0x7ed800139000 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\cc\layers\texture_layer.cc:169 in cc::TextureLayer::Update
Shadow bytes around the buggy address:
  0x1280d7ca71b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1280d7ca71c0: 00 f7 f7 f7 f7 f7 f7 00 00 00 00 00 00 00 00 00
  0x1280d7ca71d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1280d7ca71e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x1280d7ca71f0: 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00
=>0x1280d7ca7200:[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x1280d7ca7210: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 00
  0x1280d7ca7220: 00 00 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7
  0x1280d7ca7230: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x1280d7ca7240: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x1280d7ca7250: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
==15896==ABORTING

Did this work before? N/A 

Chrome version: 100.0.4676.0  Channel: n/a
OS Version: 10.0

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 5.0 KB)
- [ch.test.js](attachments/ch.test.js) (text/plain, 4.3 KB)
- [poc.zip](attachments/poc.zip) (application/octet-stream, 84.0 KB)
- [rca2.diff](attachments/rca2.diff) (text/plain, 4.1 KB)
- [PATCH.diff](attachments/PATCH.diff) (text/plain, 1.8 KB)

## Timeline

### [Deleted User] (2021-12-29)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-12-29)

In order to reproduce stably, I provide an automated testing tool based on puppeteer.

Step to rep
1. unzip poc.zip
2. instal node & puppeteer-core
3. python -m http.server 80 (The port is hard-coded in the code, so please do not modify the port and relative path)
4. node ch.test.js D:\chrome_asan\asan-win32-release_x64-954268\chrome.exe http://localhost/fuzz-00001.html

ps:There will be a permission request pop-up window, you need to click on Alloc, I don’t confirm whether this is necessary, because the minimum POC was not made successfully, this may be caused by the code generated by the fuzzer, I think it has nothing to do with this vulnerability, I will analyze it in depth



### ke...@chromium.org (2022-01-04)

szager@: This hasn't been bisected, but you've been working in this area lately. Can you PTAL?

[Monorail components: Blink>Compositing]

### [Deleted User] (2022-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2022-01-05)

[Comment Deleted]

### m....@gmail.com (2022-01-05)

#RCA
ImageLayerBridge is a gc object and has a function named Dispose, but Dispose is still not marked with the USING_PRE_FINALIZER macro but called when ImageLayerBridge is destructed. 
We know that the timing of calling the destructor of the GC object and the timing of the object being GC are inconsistent That caused this UAP issue.

1. ImageLayerBridge is GC object and has a member scoped_refptr<cc::TextureLayer> layer_;
2. When ImageLayerBridge GCed and ImageLayerBridge destructed not called yet because it's GC object
3. TextureLayer has a raw pointer to ImageLayerBridge("raw_ptr<TextureLayerClient> client_;")
4. When cc::TextureLayer::Update get called,he didn’t know that ImageLayerBridge had been freed, leading to UAP


I modified some codes to add some debugging information when TextureLayerClient was constructed and destructed, ImageLayerBridge was destructed and TextureLayer::Update was called.
Providing debugging information can clearly find that UAP occurred shortly after ImageLayerBridge was GCed. At this time, the destructor of ImageLayerBridge was not called.

```
# 00007EB300130210 UAP 
[12968:13816:0105/181351.654:ERROR:texture_layer.cc(30)] [1283124]TextureLayer::CreateForMailbox->>00007E9700130170
Backtrace:
	base::debug::CollectStackTrace [0x00007FFC03CAFBB2+18] (E:\v8\chro2\src\base\debug\stack_trace_win.cc:305)
	base::debug::StackTrace::StackTrace [0x00007FFC039A1A65+37] (E:\v8\chro2\src\base\debug\stack_trace.cc:200)
	cc::TextureLayer::CreateForMailbox [0x00007FFBF93EB671+529] (E:\v8\chro2\src\cc\layers\texture_layer.cc:32)
	blink::ImageLayerBridge::ImageLayerBridge [0x00007FFBBF60C9AD+461] (E:\v8\chro2\src\third_party\blink\renderer\platform\graphics\gpu\image_layer_bridge.cc:61)
	blink::MakeGarbageCollected<blink::ImageLayerBridge,blink::OpacityMode> [0x00007FFBBAF77C80+77] (E:\v8\chro2\src\third_party\blink\renderer\platform\heap\garbage_collected.h:34)
	blink::ImageBitmapRenderingContextBase::ImageBitmapRenderingContextBase [0x00007FFBBAF77B61+381] (E:\v8\chro2\src\third_party\blink\renderer\modules\canvas\imagebitmap\image_bitmap_rendering_context_base.cc:24)

[12968:13816:0105/181352.062:ERROR:texture_layer.cc(175)] [1283124]TextureLayer::Update->>00007E9700130170
[12968:13816:0105/181353.073:ERROR:texture_layer.cc(175)] [1283124]TextureLayer::Update->>00007E9700130170
[12968:13816:0105/181354.074:ERROR:texture_layer.cc(175)] [1283124]TextureLayer::Update->>00007E9700130170
[12968:13816:0105/181354.910:ERROR:image_layer_bridge.h(42)] [1283124]ImageLayerBridge::Dispose2->>00007E9700130170 <<
[12968:13816:0105/181355.074:ERROR:texture_layer.cc(175)] [1283124]TextureLayer::Update->>00007E9700130170
=================================================================
==12968==ERROR: AddressSanitizer: use-after-poison on address 0x7e9700130170 at pc 0x7ffbf93edfef bp 0x00f7ebdfc1a0 sp 0x00f7ebdfc1e8
READ of size 8 at 0x7e9700130170 thread T0

    #0 0x7ffbf93edfee in cc::TextureLayer::Update E:\v8\chro2\src\cc\layers\texture_layer.cc:176
    #1 0x7ffbf961383e in cc::LayerTreeHost::DoUpdateLayers E:\v8\chro2\src\cc\trees\layer_tree_host.cc:885
    #2 0x7ffbf9612e67 in cc::LayerTreeHost::UpdateLayers E:\v8\chro2\src\cc\trees\layer_tree_host.cc:749
    #3 0x7ffbf970f229 in cc::ProxyMain::BeginMainFrame E:\v8\chro2\src\cc\trees\proxy_main.cc:315
```

### m....@gmail.com (2022-01-05)

#PATCH
My fix is to use USING_PRE_FINALIZER to ensure that Dispose is called when the object is GC instead of when it is destructed

```
diff --git a/third_party/blink/renderer/platform/graphics/gpu/image_layer_bridge.cc b/third_party/blink/renderer/platform/graphics/gpu/image_layer_bridge.cc
index a3c1153f96..66e58eafb9 100644
--- a/third_party/blink/renderer/platform/graphics/gpu/image_layer_bridge.cc
+++ b/third_party/blink/renderer/platform/graphics/gpu/image_layer_bridge.cc
@@ -70,8 +70,7 @@ ImageLayerBridge::ImageLayerBridge(OpacityMode opacity_mode)
 }
 
 ImageLayerBridge::~ImageLayerBridge() {
-  if (!disposed_)
-    Dispose();
+  ;
 }
 
 void ImageLayerBridge::SetImage(scoped_refptr<StaticBitmapImage> image) {
@@ -115,6 +114,9 @@ void ImageLayerBridge::SetUV(const gfx::PointF& left_top,
 }
 
 void ImageLayerBridge::Dispose() {
+  if (disposed_)
+    return;
+
   if (layer_) {
     layer_->ClearClient();
     layer_ = nullptr;
diff --git a/third_party/blink/renderer/platform/graphics/gpu/image_layer_bridge.h b/third_party/blink/renderer/platform/graphics/gpu/image_layer_bridge.h
index 45e20f41d9..85fe9cf341 100644
--- a/third_party/blink/renderer/platform/graphics/gpu/image_layer_bridge.h
+++ b/third_party/blink/renderer/platform/graphics/gpu/image_layer_bridge.h
@@ -11,6 +11,7 @@
 #include "third_party/blink/renderer/platform/graphics/graphics_types.h"
 #include "third_party/blink/renderer/platform/graphics/static_bitmap_image.h"
 #include "third_party/blink/renderer/platform/heap/garbage_collected.h"
+#include "third_party/blink/renderer/platform/heap/prefinalizer.h"
 #include "third_party/blink/renderer/platform/platform_export.h"
 #include "ui/gfx/geometry/point_f.h"
 
@@ -29,6 +30,7 @@ namespace blink {
 class PLATFORM_EXPORT ImageLayerBridge
     : public GarbageCollected<ImageLayerBridge>,
       public cc::TextureLayerClient {
+  USING_PRE_FINALIZER(ImageLayerBridge, Dispose);
  public:
   ImageLayerBridge(OpacityMode);
   ImageLayerBridge(const ImageLayerBridge&) = delete;

```

### sz...@chromium.org (2022-01-05)

cc junov@ for canvas

I can't reproduce this; can you try applying this patch and see if it fixes the problem:

https://chromium-review.googlesource.com/c/chromium/src/+/3363951

?

### sz...@chromium.org (2022-01-05)

cc aaronhk

### m....@gmail.com (2022-01-06)

re https://crbug.com/chromium/1283124#c10
Still reproduce after applying that patch.

### sz...@chromium.org (2022-01-06)

re https://crbug.com/chromium/1283124#c12 -- I uploaded a new patch set, could you try again?

### m....@gmail.com (2022-01-07)

re https://crbug.com/chromium/1283124#c13
No longer after applying that patch.

### sz...@chromium.org (2022-01-07)

Great! Thank you for the report.

### gi...@appspot.gserviceaccount.com (2022-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/73f2599ca7c91c29308f809e07cfdc3726730203

commit 73f2599ca7c91c29308f809e07cfdc3726730203
Author: Stefan Zager <szager@chromium.org>
Date: Fri Jan 07 21:39:39 2022

Do complete teardown of context in canvas pre-finalizer

Bug: chromium:1283124
Change-Id: If7b9178835ffc240c849d893ac4cf02e654b16b2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3363951
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Reviewed-by: Justin Novosad <junov@chromium.org>
Commit-Queue: Stefan Zager <szager@chromium.org>
Cr-Commit-Position: refs/heads/main@{#956671}

[modify] https://crrev.com/73f2599ca7c91c29308f809e07cfdc3726730203/third_party/blink/renderer/core/html/canvas/canvas_rendering_context.h
[modify] https://crrev.com/73f2599ca7c91c29308f809e07cfdc3726730203/third_party/blink/renderer/modules/canvas/imagebitmap/image_bitmap_rendering_context_base.cc
[modify] https://crrev.com/73f2599ca7c91c29308f809e07cfdc3726730203/third_party/blink/renderer/modules/canvas/imagebitmap/image_bitmap_rendering_context_base.h


### sz...@chromium.org (2022-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-10)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-13)

And another one! The VRP Panel has decided to award you $5000 for this report. Thank you for your efforts and great work. 

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

Not requesting merge to dev (M99) because latest trunk commit (956671) appears to be prior to dev branch point (961656). If this is incorrect, please replace the Merge-NA-99 label with Merge-Request-99. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1283124?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058360)*
