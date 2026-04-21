# UAP style_invalidator.cc:192 in blink::StyleInvalidator::PushInvalidationSetsForContainerNode

| Field | Value |
|-------|-------|
| **Issue ID** | [40060437](https://issues.chromium.org/issues/40060437) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CSS |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | fu...@chromium.org |
| **Created** | 2022-07-29 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

#TestOn  

asan-win32-release\_x64-1029569

#Reproduce

1. python -m http.server 1337
2. install node,puppeteer-core
3. node ch.test.js D:\chrome\_asan\asan-win32-release\_x64-1029569\chrome.exe <http://localhost:1337/poc.html>

NOTE:Using puppeteer-core is for stable reproduction, not related to the vulnerability itself.

**Problem Description:**  

#Type of crash  

render tab

#Analysis  

When the DCHECK condition is met at[1], will cause a UAP at [2]

```
void StyleInvalidator::PushInvalidationSetsForContainerNode(  
    ContainerNode& node,  
    SiblingData& sibling_data) {  
  auto pending_invalidations_iterator = pending_invalidation_map_.find(&node);  
  DCHECK(pending_invalidations_iterator != pending_invalidation_map_.end());		<< [1]  
  NodeInvalidationSets& pending_invalidations =  
      pending_invalidations_iterator->value;  
  
  DCHECK(pending_nth_sets_.IsEmpty());  
  
  for (const auto& invalidation_set : pending_invalidations.Siblings()) {			<< [2]  
    CHECK(invalidation_set->IsAlive());  
    if (invalidation_set->IsNthSiblingInvalidationSet()) {  
      AddPendingNthSiblingInvalidationSet(  
          To<NthSiblingInvalidationSet>(\*invalidation_set));  
    } else {  
      sibling_data.PushInvalidationSet(  
          To<SiblingInvalidationSet>(\*invalidation_set));  
    }  
  }  

```

#Patch  

My fix was change DCHECK to CHECK

```
diff --git a/third_party/blink/renderer/core/css/invalidation/style_invalidator.cc b/third_party/blink/renderer/core/css/invalidation/style_invalidator.cc  
index 0463c26..99e7120 100644  
--- a/third_party/blink/renderer/core/css/invalidation/style_invalidator.cc  
+++ b/third_party/blink/renderer/core/css/invalidation/style_invalidator.cc  
@@ -183,7 +183,7 @@  
     ContainerNode& node,  
     SiblingData& sibling_data) {  
   auto pending_invalidations_iterator = pending_invalidation_map_.find(&node);  
-  DCHECK(pending_invalidations_iterator != pending_invalidation_map_.end());  
+  CHECK(pending_invalidations_iterator != pending_invalidation_map_.end());  
   NodeInvalidationSets& pending_invalidations =  
       pending_invalidations_iterator->value;  
   

```
# **Additional Comments:**

==2372==ERROR: AddressSanitizer: use-after-poison on address 0x7ea40080c528 at pc 0x7ffeefc661ac bp 0x000000bfa740 sp 0x000000bfa788  

READ of size 8 at 0x7ea40080c528 thread T0  

==2372==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffeefc661ab in blink::StyleInvalidator::PushInvalidationSetsForContainerNode C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:192  

#1 0x7ffeefc6699a in blink::StyleInvalidator::Invalidate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:292  

#2 0x7ffeefc68564 in blink::StyleInvalidator::InvalidateShadowRootChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:251  

#3 0x7ffeefc692d5 in blink::StyleInvalidator::InvalidateChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:260  

#4 0x7ffeefc668d3 in blink::StyleInvalidator::Invalidate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:315  

#5 0x7ffeefc69091 in blink::StyleInvalidator::InvalidateChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:269  

#6 0x7ffeefc668d3 in blink::StyleInvalidator::Invalidate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:315  

#7 0x7ffeefc69091 in blink::StyleInvalidator::InvalidateChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:269  

#8 0x7ffeefc668d3 in blink::StyleInvalidator::Invalidate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:315  

#9 0x7ffeefc69091 in blink::StyleInvalidator::InvalidateChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:269  

#10 0x7ffeefc668d3 in blink::StyleInvalidator::Invalidate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:315  

#11 0x7ffeefc69091 in blink::StyleInvalidator::InvalidateChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:269  

#12 0x7ffeefc668d3 in blink::StyleInvalidator::Invalidate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:315  

#13 0x7ffeefc69091 in blink::StyleInvalidator::InvalidateChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:269  

#14 0x7ffeefc668d3 in blink::StyleInvalidator::Invalidate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:315  

#15 0x7ffeefc69091 in blink::StyleInvalidator::InvalidateChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:269  

#16 0x7ffeefc668d3 in blink::StyleInvalidator::Invalidate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:315  

#17 0x7ffeefc69091 in blink::StyleInvalidator::InvalidateChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:269  

#18 0x7ffeefc668d3 in blink::StyleInvalidator::Invalidate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:315  

#19 0x7ffeefc69091 in blink::StyleInvalidator::InvalidateChildren C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:269  

#20 0x7ffeefc668d3 in blink::StyleInvalidator::Invalidate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:315  

#21 0x7ffeefc64c58 in blink::StyleInvalidator::Invalidate C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:42  

#22 0x7ffeebaea010 in blink::StyleEngine::InvalidateStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:1690  

#23 0x7ffeeb51852a in blink::Document::UpdateStyleInvalidationIfNeeded C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:1990  

#24 0x7ffeeb519846 in blink::Document::UpdateStyleAndLayoutTreeForThisDocument C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2208  

#25 0x7ffeeb4684b5 in blink::LocalFrameView::UpdateStyleAndLayoutInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3260  

#26 0x7ffeeb453363 in blink::LocalFrameView::UpdateStyleAndLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3212  

#27 0x7ffeeb51a332 in blink::Document::UpdateStyleAndLayout C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2587  

#28 0x7ffeeea8ae28 in blink::HTMLPlugInElement::LayoutEmbeddedContentForJSBindings C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\html\_plugin\_element.cc:493  

#29 0x7ffeeea8a165 in blink::HTMLPlugInElement::PluginWrapper C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\html\_plugin\_element.cc:395  

#30 0x7ffef3697f38 in blink::V8HTMLObjectElement::NamedPropertyGetterCustom C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\custom\v8\_html\_plugin\_element\_custom.cc:146  

#31 0x7ffeefdd79ce in blink::V8HTMLObjectElement::NamedPropertyGetterCallback C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\renderer\bindings\core\v8\v8\_html\_object\_element.cc:97  

#32 0x7ffee2415937 in v8::internal::PropertyCallbackArguments::CallNamedGetter C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:181  

#33 0x7ffee28cf1a1 in v8::internal::`anonymous namespace'::GetPropertyWithInterceptorInternal C:\b\s\w\ir\cache\builder\src\v8\src\objects\js-objects.cc:1216  

#34 0x7ffee28cec56 in v8::internal::JSObject::GetPropertyWithInterceptor C:\b\s\w\ir\cache\builder\src\v8\src\objects\js-objects.cc:5368  

#35 0x7ffee2ac3a85 in v8::internal::Object::GetProperty C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:1173  

#36 0x7ffee23bd12d in v8::internal::LoadIC::Load C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:512  

#37 0x7ffee23e7fb5 in v8::internal::Runtime\_LoadNoFeedbackIC\_Miss C:\b\s\w\ir\cache\builder\src\v8\src\ic\ic.cc:2712  

#38 0x7ffe7fed023b (<unknown module>)

Address 0x7ea40080c528 is a wild pointer inside of access range of size 0x000000000008.  

SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\invalidation\style\_invalidator.cc:192 in blink::StyleInvalidator::PushInvalidationSetsForContainerNode  

Shadow bytes around the buggy address:  

0x0fd500101850: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fd500101860: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fd500101870: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fd500101880: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fd500101890: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0fd5001018a0: 00 00 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fd5001018b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fd5001018c0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fd5001018d0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fd5001018e0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fd5001018f0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

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

==2372==ABORTING

\*\*Chrome version: \*\* asan-win32-release\_x64-1029569 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [6ecd0a5ace7c998c7c9b4d7fcad6e8630efbf2f2.mp4](attachments/6ecd0a5ace7c998c7c9b4d7fcad6e8630efbf2f2.mp4) (video/mp4, 11.5 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 9.8 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 8.4 KB)
- [ch.test.js](attachments/ch.test.js) (text/plain, 5.4 KB)
- [h1.js](attachments/h1.js) (text/plain, 8.1 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 749 B)
- [poc.html](attachments/poc.html) (text/plain, 18.7 KB)
- [testharness.js](attachments/testharness.js) (text/plain, 155.7 KB)
- [test-v-128k-320x240-24fps-8kfr.mp4](attachments/test-v-128k-320x240-24fps-8kfr.mp4) (video/mp4, 37.8 KB)
- [m6.html](attachments/m6.html) (text/plain, 5.2 KB)
- [o2.html](attachments/o2.html) (text/plain, 314.8 KB)
- [rep.mp4](attachments/rep.mp4) (video/mp4, 2.5 MB)
- [load.js](attachments/load.js) (text/plain, 1.0 KB)

## Timeline

### [Deleted User] (2022-07-29)

[Empty comment from Monorail migration]

### bh...@google.com (2022-07-30)

Hi. I am unable to reproduce this.

Do you have a simpler poc for this bug? The current poc has all kind of fuzzing and complex elements, which makes it difficult to understand what is going wrong.

Also, do you have an explanation for what is causing the UAP? I see that you highlighted the stack trace reaching a DCHECK, but it is not clear what is going wrong. why is PushInvalidationSetsForContainerNode being called for an element not in pending_invalidation_map_.?

### m....@gmail.com (2022-08-01)

I made a smaller POC, you can try this POC .

### bh...@google.com (2022-08-01)

Unable to replicate, so cannot set FoundIn. Adding owners to help triage further. Marking medium severity as it is the renderer process.

Hi to the owners. Please let us know if this should be assigned to someone else. And please advice on what should we set the FoundIn to, that is which version of Chrome did the bug first appear in.

[Monorail components: Blink]

### m....@gmail.com (2022-08-02)

Add an original sample, and reproduce the video.
1. python -m http.server 1337
2. chrome.exe --no-sandbox --js-flags='--expose_gc --allow-natives-syntax' --enable-blink-test-features --user-data-dir=test --use-gl=angle --use-angle=swiftshader http://localhost:1337/o2.html
3. Click the HavTest button

### m....@gmail.com (2022-08-02)

Debugging Tips

1. node load.js chrome_bin 
2. Navigate to http://localhost:1337/M6.html (The local test debug version takes a long time to load)
3. Click havtest button
4. Refresh the page and try again, if it doesn't reproduce

```
[14416:12116:0802/154950.321:FATAL:node.cc(2237)] Check failed: !NeedsStyleInvalidation(). 
Backtrace:
	base::debug::CollectStackTrace [0x00007FFDAA773F77+39] (E:\v8\chro2\src\base\debug\stack_trace_win.cc:329)
	base::debug::StackTrace::StackTrace [0x00007FFDAA4537CD+77] (E:\v8\chro2\src\base\debug\stack_trace.cc:221)
	base::debug::StackTrace::StackTrace [0x00007FFDAA453765+37] (E:\v8\chro2\src\base\debug\stack_trace.cc:218)
	logging::LogMessage::~LogMessage [0x00007FFDAA4A9150+208] (E:\v8\chro2\src\base\logging.cc:670)
	logging::LogMessage::~LogMessage [0x00007FFDAA4AAED9+41] (E:\v8\chro2\src\base\logging.cc:664)
	logging::CheckError::~CheckError [0x00007FFDAA40E38F+47] (E:\v8\chro2\src\base\check.cc:215)
	blink::Node::InsertedInto [0x00007FFD77B425BE+270] (E:\v8\chro2\src\third_party\blink\renderer\core\dom\node.cc:2238)
	blink::Element::InsertedInto [0x00007FFD7A14D663+67] (E:\v8\chro2\src\third_party\blink\renderer\core\dom\element.cc:3402)
	blink::HTMLElement::InsertedInto [0x00007FFD7862AB32+34] (E:\v8\chro2\src\third_party\blink\renderer\core\html\html_element.cc:1590)
	blink::PictureInPictureInterstitial::InsertedInto [0x00007FFD7875DB17+2039] (E:\v8\chro2\src\third_party\blink\renderer\core\html\media\picture_in_picture_interstitial.cc:135)
	blink::ContainerNode::NotifyNodeInsertedInternal [0x00007FFD7A0651BD+365] (E:\v8\chro2\src\third_party\blink\renderer\core\dom\container_node.cc:1000)
	blink::ContainerNode::NotifyNodeInsertedInternal [0x00007FFD7A065223+467] (E:\v8\chro2\src\third_party\blink\renderer\core\dom\container_node.cc:995)
	blink::ContainerNode::InsertNodeVector<blink::ContainerNode::AdoptAndAppendChild> [0x00007FFD7A063728+1000] (E:\v8\chro2\src\third_party\blink\renderer\core\dom\container_node.cc:325)
	blink::ContainerNode::AppendChild [0x00007FFD7A05EFAB+699] (E:\v8\chro2\src\third_party\blink\renderer\core\dom\container_node.cc:922)
	blink::Node::ReplaceChildren [0x00007FFD77B38DA3+403] (E:\v8\chro2\src\third_party\blink\renderer\core\dom\node.cc:970)
	blink::ParentNode::replaceChildren [0x00007FFD6D585E48+40] (E:\v8\chro2\src\third_party\blink\renderer\core\dom\parent_node.h:85)
	blink::`anonymous namespace'::v8_element::ReplaceChildrenOperationCallback [0x00007FFD6D5A736C+540] (E:\v8\chro2\src\out\debug\gen\third_party\blink\renderer\bindings\modules\v8\v8_element.cc:3847)
	v8::internal::FunctionCallbackArguments::Call [0x00007FFD7D18586E+286] (E:\v8\chro2\src\v8\src\api\api-arguments-inl.h:147)
	v8::internal::`anonymous namespace'::HandleApiCallHelper<0> [0x00007FFD7D183F46+1446] (E:\v8\chro2\src\v8\src\builtins\builtins-api.cc:112)
	v8::internal::Builtin_Impl_HandleApiCall [0x00007FFD7D182323+611] (E:\v8\chro2\src\v8\src\builtins\builtins-api.cc:143)
	v8::internal::Builtin_HandleApiCall [0x00007FFD7D181A89+185] (E:\v8\chro2\src\v8\src\builtins\builtins-api.cc:130)
	(No symbol) [0x00007FFCFF994EC3]
Crash keys:
  "subresource_url" = "http://localhost:1337/nonesuch.mp4"
  "view-count" = "1"
  "loaded-origin-0" = "http://localhost:1337"
  "web-frame-count" = "2"
  "blink_scheduler_async_stack" = "0x7FFD6EE0D31A 0x7FFD6F9385B1"
  "v8_code_space_firstpage_address" = "0x7ffce0000000"
  "v8_ro_space_firstpage_address" = "0x1f600000000"
  "v8_isolate_address" = "0x1ed88dbe090"
  "switch-17" = "--field-trial-handle=2036,i,1006537455668026090,2488073361599674"
  "switch-16" = "--mojo-platform-channel-handle=2328"
  "switch-15" = "--launch-time-ticks=709995912518"
  "switch-14" = "--renderer-client-id=7"
  "switch-13" = "--enable-main-frame-before-activation"
  "switch-12" = "--num-raster-threads=4"
  "switch-11" = "--device-scale-factor=1.1041666269302368"
  "switch-10" = "--lang=zh-CN"
  "switch-9" = "--video-capture-use-gpu-memory-buffer"
  "switch-8" = "--js-flags=--expose-gc --allow-natives-syntax"
  "switch-7" = "--use-fake-ui-for-media-stream"
  "switch-6" = "--remote-debugging-port=0"
  "switch-5" = "--enable-blink-test-features"
  "switch-4" = "--no-sandbox"
  "switch-3" = "--event-path-policy=0"
  "switch-2" = "--display-capture-permissions-policy-allowed"
  "switch-1" = "--user-data-dir=TMP/chtest_rep_2"
  "num-switches" = "19"
```

### [Deleted User] (2022-08-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dt...@chromium.org (2022-08-02)

[Empty comment from Monorail migration]

### dt...@chromium.org (2022-08-02)

[Empty comment from Monorail migration]

[Monorail components: -Blink Blink>CSS]

### fu...@chromium.org (2022-08-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3edade5d6853d45775dd5b4d4c2b72eecd13932a

commit 3edade5d6853d45775dd5b4d4c2b72eecd13932a
Author: Rune Lillesveen <futhark@chromium.org>
Date: Fri Aug 05 13:21:38 2022

Don't use end() iterator value for pending invalidations

Ideally, we should not have marked a node for style invalidation unless
we have scheduled any invalidation sets for it. Still, we should avoid
crashing if that happens. Adding a NOTREACHED() to be able to detect
any such cases, and potentially fix them.

Speculative fix for 1348474

Bug: 1348474
Change-Id: I873e6ec6ddf4b9021e5a3b872eaad8c7d826877a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3811523
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1031883}

[modify] https://crrev.com/3edade5d6853d45775dd5b4d4c2b72eecd13932a/third_party/blink/renderer/core/css/invalidation/style_invalidator.cc


### fu...@chromium.org (2022-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-05)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fu...@chromium.org (2022-08-05)

I have not been able to reproduce (only tested on Linux, I don't have Windows), which means I cannot set a sensible FoundIn. The code that crashes has been like that for years, but it's unclear if what makes it end up in that state is new or not.


### fu...@chromium.org (2022-08-08)

m.coolie@gmail.com: Do you have any idea if ending up with this crash is a recent regression?


### m....@gmail.com (2022-08-08)

No longer reproduced on asan-win32-release_x64-1032438

### aj...@google.com (2022-08-08)

Setting FoundIn-104 as code is oldish and that is the latest Extended Stable.

I had tried to repro this on the associated asan build (win32-release_x64_asan-win32-release_x64-1012724) but could not - however the repro is not minimized so it is difficult to have confidence in it.

### fu...@chromium.org (2022-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-09)

Merge review required: M105 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-09)

Merge review required: M104 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-09)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-09)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-08-10)

1. The requested merge is a fix for a Medium Severity Security issue
2. https://chromium-review.googlesource.com/c/chromium/src/+/3811523
3. Yes
4. No, not a new feature
5. -
6. No


### am...@google.com (2022-08-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-17)

Congratulations! The VRP Panel has decided to award you $7,000 for this report based on the updated Chrome VRP reward amounts [1]. Thank you for your efforts in reporting this issue to us! Nice work! 
[1] https://g.co/chrome/vrp

### am...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-21)

Hello OP, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them. 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1348474?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1348424]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060437)*
