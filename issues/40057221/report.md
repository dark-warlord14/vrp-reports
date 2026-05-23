# SUMMARY: AddressSanitizer: use-after-poison event_listener_map.cc:144 in blink::EventListenerMap::Add

| Field | Value |
|-------|-------|
| **Issue ID** | [40057221](https://issues.chromium.org/issues/40057221) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection |
| **Platforms** | Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2021-09-10 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4594.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-918757.zip

#Reproduce
This problem is not stable to reproduce manually. I wrote an automated script here through puppeteer, which is easier to reproduce, but nodejs needs to be installed.
The automated tool fails to give the minicase, I will try to make the minicase by hand.

1. install nodejs
2. python -m http.server 80
3. node ch.test.js D:\chrome_asan\asan-win32-release_x64-918757\chrome.exe http://localhost/poc.html
4. wait asan report

What is the expected behavior?

What went wrong?
Type of crash
render tab

Did this work before? N/A 

Chrome version: 94.0.4594.0  Channel: n/a
OS Version: 10.0

#Analysis
Not Yet

#Patch
Not yet

#asan
=================================================================
==10908==ERROR: AddressSanitizer: use-after-poison on address 0x7ea800137a68 at pc 0x7ffc4bc1fcba bp 0x00db1bff9980 sp 0x00db1bff99c8
READ of size 8 at 0x7ea800137a68 thread T0
==10908==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffc4bc1fcb9 in blink::EventListenerMap::Add C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_listener_map.cc:144
    #1 0x7ffc48792235 in blink::EventTarget::AddEventListenerInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_target.cc:481
    #2 0x7ffc4f2c7b2e in blink::VideoWakeLock::VideoWakeLock C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\media\video_wake_lock.cc:25
    #3 0x7ffc4b7eb592 in blink::HTMLVideoElement::HTMLVideoElement C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\media\html_video_element.cc:104
    #4 0x7ffc4ba8a54f in blink::HTMLVideoConstructor C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\core\html_element_factory.cc:678
    #5 0x7ffc4ba7e747 in blink::HTMLElementFactory::Create C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\core\html_element_factory.cc:857
    #6 0x7ffc484c98af in blink::Document::CreateElementForBinding C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:1071
    #7 0x7ffc53a8398a in blink::`anonymous namespace'::v8_document::CreateElementOperationCallbackForMainWorld C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_document.cc:5352
    #8 0x7ffc3faeafe7 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:152
    #9 0x7ffc3fae8364 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
    #10 0x7ffc3fae574f in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:142
    #11 0x7ffc3fae4a9c in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130
    #12 0x7ea0000c113b  (<unknown module>)

Address 0x7ea800137a68 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_listener_map.cc:144 in blink::EventListenerMap::Add
Shadow bytes around the buggy address:
  0x127f23ca6ef0: f7 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x127f23ca6f00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x127f23ca6f10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x127f23ca6f20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x127f23ca6f30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x127f23ca6f40: 00 00 00 00 00 00 00 00 00 00 00 00 00[f7]f7 f7
  0x127f23ca6f50: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x127f23ca6f60: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x127f23ca6f70: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x127f23ca6f80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x127f23ca6f90: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
==10908==ABORTING

## Attachments

- deleted (application/octet-stream, 0 B)
- [asan.txt](attachments/asan.txt) (text/plain, 3.9 KB)
- [poc.zip](attachments/poc.zip) (application/octet-stream, 68.3 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 4.0 KB)
- [tsan.txt](attachments/tsan.txt) (text/plain, 6.7 KB)
- [tsan2.txt](attachments/tsan2.txt) (text/plain, 12.4 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [tsan3.txt](attachments/tsan3.txt) (text/plain, 12.1 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [poc_0915.zip](attachments/poc_0915.zip) (application/octet-stream, 163.2 KB)
- [2021-09-16 144239.png](attachments/2021-09-16 144239.png) (image/png, 13.6 KB)

## Timeline

### [Deleted User] (2021-09-10)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-10)

Thanks for the node-based test case. I've given it a try, but realistically there's little chance of me getting it to work. I've got to make it work on a Linux box, where port is is occupied, and different versions of node/puppeteer are available.

I've also fiddled around extensively with the poc manually, but to no avail.

I'll have a peek at the ASAN trace and think about whether we've got enough information to pass it onto the engineering team without a readily reproducible POC.

### ad...@google.com (2021-09-10)

(of course, I could impose on a coworker to set up node/puppeteer/etc. on a Windows machine, if necessary)

### ad...@google.com (2021-09-10)

OK, I unfortunately don't think there's quite enough here to pass this onto our engineering teams. We realistically need both the 'free' and 'use' stack traces to be able to make progress.

I'm happy to ask a colleague with a Windows box to try to reproduce this, but we also need to make it easier for our engineers to reproduce and fix this, and a puppeteer-based arrangement sounds hard to make consistently reproducible. So, if you are working on making a reduced test case, I'd prefer to wait. Let me know if that's still your plan.

(Of course, the absolute ideal case is a single fully-automated POC file which we can feed to ClusterFuzz. That benefits us because it automatically bisects to the regression range, assigns the right engineers, and verifies the fix automatically - as well as various labelling tasks. If you can manage to produce such a POC that'd be amazing!)

### m....@gmail.com (2021-09-12)

re https://crbug.com/chromium/1248435#c4
The original sample is very stable to reproduce in the windows environment.

I tried to make the mini sample manually, but found it very strange, even if I delete some code that is confirmed not to be executed, it will affect the reproduce of the issue.

However, it is not completely without any gains. The asan version under liunx cannot be tested normally, but the tsan(tsan.test.poc.zip,gs://chromium-browser-tsan/linux-release/tsan-linux-release-920573.zip) version can. Although tsan cannot reproduce the situation in windows, but found two new crash stack, which seems to be related to the problem to be found.

At the same time, the fuzzer machine also throws a similar new asan stack.

Combined with the new information, I guess it is that when the VideoWakeLock object is constructed or when blink::ContainerNode::NotifyNodeInsertedInternal is called, it can trigger a user callback and cause the HTMLVideoElement to be freed and eventually lead to UAF.

I will try to compile the debug version and add some output information to locate the problem.

```
HTMLVideoElement::HTMLVideoElement(Document& document)
    : HTMLMediaElement(html_names::kVideoTag, document),

---cut---

  custom_controls_fullscreen_detector_ =
      MakeGarbageCollected<MediaCustomControlsFullscreenDetector>(*this);

  wake_lock_ = MakeGarbageCollected<VideoWakeLock>(*this); <<<

  EnsureUserAgentShadowRoot();
  UpdateStateIfNeeded();
}
```

TSAN(new)
```
ThreadSanitizer:DEADLYSIGNAL
==8151==ERROR: ThreadSanitizer: SEGV on unknown address 0x0000000000fd (pc 0x5594e473acdd bp 0x000000000002 sp 0x7ffd1b0357e0 T8151)
==8151==The signal is caused by a READ memory access.
==8151==Hint: address points to the zero page.
    #0 atomic_load<__sanitizer::atomic_uint16_t> /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/tsan/../sanitizer_common/sanitizer_atomic_clang_x86.h:46:14 (chrome+0x3f85cdd)
    #1 NoTsanAtomicLoad<unsigned short> /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/tsan/rtl/tsan_interface_atomic.cpp:213:10 (chrome+0x3f85cdd)
    #2 AtomicLoad<unsigned short> /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/tsan/rtl/tsan_interface_atomic.cpp:235:9 (chrome+0x3f85cdd)
    #3 __tsan_atomic16_load /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/tsan/rtl/tsan_interface_atomic.cpp:499:3 (chrome+0x3f85cdd)
    #4 __cxx_atomic_load<unsigned short> buildtools/third_party/libc++/trunk/include/atomic:1006:12 (chrome+0x77fd4d0)
    #5 load buildtools/third_party/libc++/trunk/include/atomic:1615:17 (chrome+0x77fd4d0)
    #6 LoadEncoded<cppgc::internal::AccessMode::kAtomic, cppgc::internal::HeapObjectHeader::EncodedHalf::kHigh, std::__1::memory_order_acquire> v8/src/heap/cppgc/heap-object-header.h:304:40 (chrome+0x77fd4d0)
    #7 IsInConstruction<cppgc::internal::AccessMode::kAtomic> v8/src/heap/cppgc/heap-object-header.h:237:7 (chrome+0x77fd4d0)
    #8 MarkAndPush v8/src/heap/cppgc/marking-state.h:193:14 (chrome+0x77fd4d0)
    #9 cppgc::internal::MarkingStateBase::MarkAndPush(void const*, cppgc::TraceDescriptor) v8/src/heap/cppgc/marking-state.h:184:3 (chrome+0x77fd4d0)
    #10 v8::internal::UnifiedHeapMarkingVisitorBase::Visit(void const*, cppgc::TraceDescriptor) v8/src/heap/cppgc-js/unified-heap-marking-visitor.cc:24:18 (chrome+0x77fd48a)
    #11 Trace<cppgc::Visitor *, blink::HeapAllocator> third_party/blink/renderer/platform/wtf/vector.h (chrome+0xf5f1229)
    #12 Trace third_party/blink/renderer/platform/heap/collection_support/heap_vector.h:66:47 (chrome+0xf5f1229)
    #13 Trace v8/include/cppgc/trace-trait.h:86:34 (chrome+0xf5f1229)
    #14 Trace<blink::HeapVector<std::__1::pair<WTF::AtomicString, cppgc::internal::BasicMember<blink::HeapVector<blink::RegisteredEventListener, 1>, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy> >, 2> > v8/include/cppgc/visitor.h:133:5 (chrome+0xf5f1229)
    #15 blink::EventListenerMap::Trace(cppgc::Visitor*) const third_party/blink/renderer/core/dom/events/event_listener_map.cc:228:12 (chrome+0xf5f1229)
```

ASAN(new)

```
==8584==ERROR: AddressSanitizer: use-after-poison on address 0x7eab0013cb44 at pc 0x7ff8769ffb26 bp 0x0062555f9760 sp 0x0062555f97a8
READ of size 4 at 0x7eab0013cb44 thread T0
==8584==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff8769ffb25 in blink::EventListenerMap::Add C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_listener_map.cc:144
    #1 0x7ff873572235 in blink::EventTarget::AddEventListenerInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_target.cc:481
    #2 0x7ff87a0a4c73 in blink::MediaCustomControlsFullscreenDetector::Attach C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\media\media_custom_controls_fullscreen_detector.cc:86
    #3 0x7ff8765cc087 in blink::HTMLVideoElement::InsertedInto C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\media\html_video_element.cc:128
    #4 0x7ff873922821 in blink::ContainerNode::NotifyNodeInsertedInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:994
    #5 0x7ff87391d032 in blink::ContainerNode::InsertNodeVector<blink::ContainerNode::AdoptAndAppendChild> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:333
    #6 0x7ff873918613 in blink::ContainerNode::AppendChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:913
    #7 0x7ff8736b50f2 in blink::Node::appendChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\node.cc:757
    #8 0x7ff877396e2a in blink::`anonymous namespace'::v8_node::AppendChildOperationCallbackForMainWorld C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_node.cc:476
    #9 0x7ff86a8cafe7 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:152
    #10 0x7ff86a8c8364 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
    #11 0x7ff86a8c574f in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:142
    #12 0x7ff86a8c4a9c in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130
    #13 0x7ea4000c113b  (<unknown module>)
```

### [Deleted User] (2021-09-12)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2021-09-13)


I think I know the root cause of the problem. The key information can be obtained from tsan2.txt.

1. When the HTMLVideoElement constructor is called, the constructor may continue to call MakeGarbageCollected to create a new GC object, and creating a new GC object may cause garbage collection to be executed.
2. The HTMLVideoElement constructor is still in the construction stage when it is called, there is no pointer to it, causing itself to be freed, resulting in UAF.

The tsan2 log shows a situation. 
When the HTMLVideoElement constructor is called, the HTMLMediaElement constructor will be called[1], and the HTMLMediaElement constructor will call MakeGarbageCollected to create a new GC object[2], which will eventually lead to garbage collection.

I’m not sure that the analysis must be accurate, but if so, then this is a general problem.

```
third_party/blink/renderer/core/html/media/html_video_element.cc:82
HTMLVideoElement::HTMLVideoElement(Document& document)
    : HTMLMediaElement(html_names::kVideoTag, document),		<<[1]
      remoting_interstitial_(nullptr),

<<<CUT>>>
  custom_controls_fullscreen_detector_ =
      MakeGarbageCollected<MediaCustomControlsFullscreenDetector>(*this);

  wake_lock_ = MakeGarbageCollected<VideoWakeLock>(*this);

  EnsureUserAgentShadowRoot();
  UpdateStateIfNeeded();
}

third_party/blink/renderer/core/html/media/html_media_element.cc:506
HTMLMediaElement::HTMLMediaElement(const QualifiedName& tag_name,
                                   Document& document)
    : HTMLElement(tag_name, document),
      ExecutionContextLifecycleStateObserver(GetExecutionContext()),
      load_timer_(document.GetTaskRunner(TaskType::kInternalMedia),
                  this,
                  &HTMLMediaElement::LoadTimerFired),
<<<CUT>>>
      async_event_queue_(
          MakeGarbageCollected<EventQueue>(GetExecutionContext(),			<<[2]
                                           TaskType::kMediaElementEvent)),
```

### m....@gmail.com (2021-09-13)

Another possibility is that in the constructor, some Member<> xx has not been assigned. At this time, triggering GC will cause Trace to access uninitialized memory.

### ad...@google.com (2021-09-13)

So your theory is:

1. Something creates an HTMLVideoElement
2. HTMLVideoElement constructor first calls base class (HTMLMediaElement) constructor.
3. HTMLMediaElement constructor makes something garbage collected
4. Due to memory pressure, a GC is triggered
5. GC traces the HTMLVideoElement
6. The Member<T> members of HTMLVideoElement have not yet been zeroed, because we haven't yet started to run the constructor for the HTMLVideoElement itself
7. Therefore the tracing algorithm gets given non-null, but invalid member pointers.

Right?

As you say, this would be a general problem. It feels like such a core part of Oilpan that there must be some guard against this. Anyway! I'll see if I can reproduce the tsan poc.

### [Deleted User] (2021-09-13)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-13)

m.cooolie@ - chatted with people here who know about Oilpan. My description in https://crbug.com/chromium/1248435#c9 is wrong: step 5 onwards shouldn't normally happen because partially-constructed objects are treated specially by the GC, and shouldn't normally be traced.

mlippautz@ - security sheriff here. I haven't managed to reproduce this either with the original reproduction case (I don't have a handy Linux box) or the modified case in https://crbug.com/chromium/1248435#c5.

Nevertheless there does seem to be something wrong and there's plenty of stack traces to look into. Evidence from https://crbug.com/chromium/1248435#c7 suggests it's something to do with partially-constructed objects, perhaps? Hoping you can spot the problem. Please pass back to me if not, and we'll keep working on reproducing it!

### ml...@chromium.org (2021-09-14)

Few thoughts without having had a look at the repro.

m.cooolie@gmail.com:
> 2. The HTMLVideoElement constructor is still in the construction stage when it is called, there is no pointer to it, causing itself to be freed, resulting in UAF.

During construction there's a pointer to the actual memory on the stack somewhere which conservative stack canning finds to retain in-construction objects.

adetaylor@google.com:
> 6. The Member<T> members of HTMLVideoElement have not yet been zeroed, because we haven't yet started to run the constructor for the HTMLVideoElement itself
> 7. Therefore the tracing algorithm gets given non-null, but invalid member pointers.

In construction objects are traced conservatively and each memory location is checked for proper containment within the heap.

[Monorail components: Blink>GarbageCollection]

### ml...@chromium.org (2021-09-14)

[Empty comment from Monorail migration]

### ml...@chromium.org (2021-09-14)

I am currently failing to reproduce this somehow locally with a fresh tsan/asan build.

I will continue but if by any chance you have local gn args and a command line that works for you on Linux64 that would be great.

### m....@gmail.com (2021-09-14)

RE https://crbug.com/chromium/1248435#c14
1. I downloaded it directly from here gs://chromium-browser-tsan/linux-release/tsan-linux-release-920573.zip
2. You need to wait for a while after running ch.test, it will reproduce within ten minutes, if it still fails, I can provide a replay video.

### ml...@chromium.org (2021-09-14)

I have no ready to use node environment where I can run a puppeteer script which is why generally a single executing script would be super useful.

### m....@gmail.com (2021-09-14)

Sorry for that,I also tried to make a sample to reproduce without puppeteer but failed

### ml...@chromium.org (2021-09-14)

I did repro some TSAN errors with the prebuilt binary but fail to find any symbols. How did you symbolize the trace?

### m....@gmail.com (2021-09-14)

https://crbug.com/chromium/1248435#c18

export TSAN_OPTIONS="external_symbolizer_path=llvm-symbolizer"

Set llvm-symbolizer to the path on your machine

### ml...@chromium.org (2021-09-14)

I have been running the tsan.test.poc.zip (fuzz-00001.html) with `gs://chromium-browser-tsan/linux-release/tsan-linux-release-920573.zip` now for some time and have not been able to reproduce any race.

node ~/Downloads/ch.test.js ~/Downloads/tsan-linux-release-920573/chrome http://localhost:8000/fuzz-00001.html



### m....@gmail.com (2021-09-14)

Sorry again~
Some URLs in the code are hard-coded, so if you use port 8000, some necessary JS loading will fail. You can try port 80.

sudo python -m http.server 80

```
<script src="http://localhost/webgl-test-utils.js"></script>
<script src="http://localhost/h1.js"></script>
--CUT--

```

### ml...@chromium.org (2021-09-14)

Neither the ASAN nor the TSAN repro works for me locally on Linux with custom builds or the gs:// provided build :/

I think the setup is now okay, as I see the following

[0914/141035.378665:INFO:CONSOLE(3245)] "++++++++++++++++++start++++++++++++++++++", source: http://localhost/poc.html (3245)
[0914/141035.381427:INFO:CONSOLE(3260)] "++++++++++++++++++swap++++++++++++++++++", source: http://localhost/poc.html (3260)
[0914/141035.497605:INFO:CONSOLE(852)] "++++++++++++++++++trigger1++++++++++++++++++", source: http://localhost/poc.html (852)
[0914/141035.625951:ERROR:gles2_cmd_decoder.cc(3613)] ContextResult::kFatalFailure: fail_if_major_perf_caveat + swiftshader
[0914/141035.983392:INFO:CONSOLE(927)] "WebGL: INVALID_ENUM: bindBuffer: invalid target", source: http://localhost/poc.html (927)
[0914/141035.983866:INFO:CONSOLE(927)] "WebGL: INVALID_ENUM: bufferData: invalid target", source: http://localhost/poc.html (927)
[0914/141036.666271:INFO:CONSOLE(184)] "WebGL: INVALID_VALUE: enableVertexAttribArray: index out of range", source: http://localhost/webgl-test-utils.js (184)
[0914/141036.666676:INFO:CONSOLE(185)] "WebGL: INVALID_VALUE: vertexAttribPointer: index out of range", source: http://localhost/webgl-test-utils.js (185)
[0914/141037.167976:INFO:CONSOLE(1024)] "The provided value 'undefined' is not a valid enum value of type ImageSmoothingQuality.", source: http://localhost/poc.html (1024)
[0914/141038.339761:INFO:CONSOLE(1170)] "WebGL: INVALID_OPERATION: attachShader: shader attachment already has shader", source: http://localhost/poc.html (1170)
[0914/141038.439277:INFO:CONSOLE(1178)] "WebGL: INVALID_VALUE: getVertexAttrib: index out of range", source: http://localhost/poc.html (1178)
[0914/141042.923314:INFO:CONSOLE(1693)] "WebGL: INVALID_ENUM: getBufferParameter: invalid parameter name", source: http://localhost/poc.html (1693)
[0914/141044.202682:INFO:CONSOLE(1808)] "WebGL: INVALID_ENUM: getBufferParameter: invalid target", source: http://localhost/poc.html (1808)
fuzz->bef close:http://localhost/poc.html tick->405996
fuzz->aft close:http://localhost/poc.html tick->406107
fuzz->aft clearTimeout:http://localhost/poc.html tick->406107
[0914/141046.229356:ERROR:gles2_cmd_decoder.cc(10096)] [.WebGL-0x61b0000d0480]GL ERROR :GL_INVALID_OPERATION : glDrawArrays: buffer format and fragment output variable type incompatible
fuzz->aft sleep2:http://localhost/poc.html tick->411112
fuzz->url setTimeout:http://localhost/poc.html tick->411112
fuzz->url newPage:http://localhost/poc.html tick->411112
fuzz->bef goto:http://localhost/poc.html
fuzz->aft goto:http://localhost/poc.html tick->413750
fuzz->aft click:http://localhost/poc.html tick->415664


### m....@gmail.com (2021-09-14)

Attachment is  windows x64 asan reproduce video.

I will try reproduce with liunx tsan

### m....@gmail.com (2021-09-14)

Tsan can still reproduce the problem, but the time is uncertain. After waiting 15 minutes this time, I found that it has reproduced and it is the new stack content. I am editing the video because of the long time.



```
hreadSanitizer:DEADLYSIGNAL
==19858==ERROR: ThreadSanitizer: SEGV on unknown address 0xfffffffffffffffd (pc 0x55c214343cdd bp 0x000000000002 sp 0x7ffe4c56c550 T19858)
==19858==The signal is caused by a READ memory access.
    #0 atomic_load<__sanitizer::atomic_uint16_t> /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/tsan/../sanitizer_common/sanitizer_atomic_clang_x86.h:46:14 (chrome+0x3f85cdd)
    #1 NoTsanAtomicLoad<unsigned short> /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/tsan/rtl/tsan_interface_atomic.cpp:213:10 (chrome+0x3f85cdd)
    #2 AtomicLoad<unsigned short> /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/tsan/rtl/tsan_interface_atomic.cpp:235:9 (chrome+0x3f85cdd)
    #3 __tsan_atomic16_load /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/tsan/rtl/tsan_interface_atomic.cpp:499:3 (chrome+0x3f85cdd)
    #4 __cxx_atomic_load<unsigned short> buildtools/third_party/libc++/trunk/include/atomic:1006:12 (chrome+0x77fd4d0)
    #5 load buildtools/third_party/libc++/trunk/include/atomic:1615:17 (chrome+0x77fd4d0)
    #6 LoadEncoded<cppgc::internal::AccessMode::kAtomic, cppgc::internal::HeapObjectHeader::EncodedHalf::kHigh, std::__1::memory_order_acquire> v8/src/heap/cppgc/heap-object-header.h:304:40 (chrome+0x77fd4d0)
    #7 IsInConstruction<cppgc::internal::AccessMode::kAtomic> v8/src/heap/cppgc/heap-object-header.h:237:7 (chrome+0x77fd4d0)
    #8 MarkAndPush v8/src/heap/cppgc/marking-state.h:193:14 (chrome+0x77fd4d0)
    #9 cppgc::internal::MarkingStateBase::MarkAndPush(void const*, cppgc::TraceDescriptor) v8/src/heap/cppgc/marking-state.h:184:3 (chrome+0x77fd4d0)
    #10 v8::internal::UnifiedHeapMarkingVisitorBase::Visit(void const*, cppgc::TraceDescriptor) v8/src/heap/cppgc-js/unified-heap-marking-visitor.cc:24:18 (chrome+0x77fd48a)
    #11 Trace<cppgc::Visitor *, blink::HeapAllocator> third_party/blink/renderer/platform/wtf/vector.h (chrome+0xf5f1229)
    #12 Trace third_party/blink/renderer/platform/heap/collection_support/heap_vector.h:66:47 (chrome+0xf5f1229)
    #13 Trace v8/include/cppgc/trace-trait.h:86:34 (chrome+0xf5f1229)
    #14 Trace<blink::HeapVector<std::__1::pair<WTF::AtomicString, cppgc::internal::BasicMember<blink::HeapVector<blink::RegisteredEventListener, 1>, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy> >, 2> > v8/include/cppgc/visitor.h:133:5 (chrome+0xf5f1229)
    #15 blink::EventListenerMap::Trace(cppgc::Visitor*) const third_party/blink/renderer/core/dom/events/event_listener_map.cc:228:12 (chrome+0xf5f1229)
    #16 Trace v8/include/cppgc/trace-trait.h:86:34 (chrome+0xf5ea200)
    #17 Trace<blink::EventListenerMap> v8/include/cppgc/visitor.h:133:5 (chrome+0xf5ea200)
    #18 blink::EventTargetData::Trace(cppgc::Visitor*) const third_party/blink/renderer/core/dom/events/event_target.cc:219:12 (chrome+0xf5ea200)
    #19 Trace v8/include/cppgc/trace-trait.h:86:34 (chrome+0xf5e6d11)
    #20 Trace<blink::EventTargetData> v8/include/cppgc/visitor.h:133:5 (chrome+0xf5e6d11)
    #21 Trace third_party/blink/renderer/core/dom/node.cc:2709:49 (chrome+0xf5e6d11)
    #22 cppgc::internal::TraceTraitBase<blink::(anonymous namespace)::EventTargetDataObject>::Trace(cppgc::Visitor*, void const*) v8/include/cppgc/trace-trait.h:86:34 (chrome+0xf5e6d11)
    #23 operator() v8/src/heap/cppgc/marker.cc:479:17 (chrome+0x8154e94)
    #24 DrainWorklistWithPredicate<150UL, heap::base::Worklist<cppgc::TraceDescriptor, 512>::Local, (lambda at ../../v8/src/heap/cppgc/marker.cc:473:15), (lambda at ../../v8/src/heap/cppgc/marker.cc:102:7)> v8/src/heap/cppgc/marking-state.h:454:5 (chrome+0x8154e94)
    #25 DrainWorklistWithBytesAndTimeDeadline<150UL, heap::base::Worklist<cppgc::TraceDescriptor, 512>::Local, (lambda at ../../v8/src/heap/cppgc/marker.cc:473:15)> v8/src/heap/cppgc/marker.cc:101:10 (chrome+0x8154e94)
    #26 cppgc::internal::MarkerBase::ProcessWorklistsWithDeadline(unsigned long, v8::base::TimeTicks) v8/src/heap/cppgc/marker.cc:470:12 (chrome+0x8154e94)
    #27 cppgc::internal::MarkerBase::AdvanceMarkingWithLimits(v8::base::TimeDelta, unsigned long) v8/src/heap/cppgc/marker.cc:402:15 (chrome+0x8154166)
    #28 v8::internal::CppHeap::AdvanceTracing(double) v8/src/heap/cppgc-js/cpp-heap.cc:457:16 (chrome+0x77f4c29)
    #29 non-virtual thunk to v8::internal::CppHeap::AdvanceTracing(double) v8/src/heap/cppgc-js/cpp-heap.cc (chrome+0x77f4d1a)
    #30 v8::internal::LocalEmbedderHeapTracer::Trace(double) v8/src/heap/embedder-tracing.cc:67:26 (chrome+0x77fe95e)
    #31 v8::internal::MarkCompactCollector::PerformWrapperTracing() v8/src/heap/mark-compact.cc:1900:42 (chrome+0x78a9302)
    #32 v8::internal::MarkCompactCollector::MarkLiveObjects() v8/src/heap/mark-compact.cc:2092:9 (chrome+0x78910a7)
    #33 v8::internal::MarkCompactCollector::CollectGarbage() v8/src/heap/mark-compact.cc:586:3 (chrome+0x7890261)
    #34 v8::internal::Heap::MarkCompact() v8/src/heap/heap.cc:2475:29 (chrome+0x7846ee1)
    #35 v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags) v8/src/heap/heap.cc:2205:7 (chrome+0x78440c7)
    #36 v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags) v8/src/heap/heap.cc:1791:13 (chrome+0x7840670)
    #37 v8::internal::Heap::AllocateRawWithLightRetrySlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) v8/src/heap/heap.cc:5454:7 (chrome+0x78520fc)
    #38 v8::internal::Heap::AllocateRawWithRetryOrFailSlowPath(int, v8::internal::AllocationType, v8::internal::AllocationOrigin, v8::internal::AllocationAlignment) v8/src/heap/heap.cc:5471:7 (chrome+0x78521ac)
    #39 AllocateRawWith<v8::internal::Heap::kRetryOrFail> v8/src/heap/heap-inl.h:346:14 (chrome+0x780a855)
    #40 v8::internal::Factory::AllocateRaw(int, v8::internal::AllocationType, v8::internal::AllocationAlignment) v8/src/heap/factory.cc:370:29 (chrome+0x780a855)
    #41 AllocateRaw v8/src/heap/factory-base.cc:860:18 (chrome+0x780233a)
    #42 AllocateRawWithImmortalMap v8/src/heap/factory-base.cc:851:23 (chrome+0x780233a)
    #43 v8::internal::FactoryBase<v8::internal::Factory>::NewRawOneByteString(int, v8::internal::AllocationType) v8/src/heap/factory-base.cc:553:52 (chrome+0x780233a)
    #44 v8::internal::Factory::NewStringFromOneByte(v8::base::Vector<unsigned char const> const&, v8::internal::AllocationType) v8/src/heap/factory.cc:724:3 (chrome+0x780c7e8)
    #45 NewStringFromAsciiChecked v8/src/heap/factory.h:253:12 (chrome+0x7821e35)
    #46 CharToString v8/src/heap/factory.cc:3087:19 (chrome+0x7821e35)
    #47 v8::internal::Factory::HeapNumberToString(v8::internal::Handle<v8::internal::HeapNumber>, double, v8::internal::NumberCacheMode) v8/src/heap/factory.cc:3152:27 (chrome+0x7821e35)
    #48 v8::internal::Factory::NumberToString(v8::internal::Handle<v8::internal::Object>, v8::internal::NumberCacheMode) v8/src/heap/factory.cc:3131:10 (chrome+0x7821514)
    #49 v8::internal::CallPrinter::PrintLiteral(v8::internal::Handle<v8::internal::Object>, bool) v8/src/ast/prettyprinter.cc:617:32 (chrome+0x761d725)
    #50 VisitLiteral v8/src/ast/prettyprinter.cc:271:3 (chrome+0x7621225)
    #51 v8::internal::CallPrinter::VisitNoStackOverflowCheck(v8::internal::AstNode*) v8/src/ast/prettyprinter.h:77:3 (chrome+0x7621225)
    #52 Visit v8/src/ast/prettyprinter.h:77:3 (chrome+0x761f4e7)
    #53 Find v8/src/ast/prettyprinter.cc:72:5 (chrome+0x761f4e7)
    #54 FindArguments v8/src/ast/prettyprinter.cc:599:5 (chrome+0x761f4e7)
    #55 v8::internal::CallPrinter::VisitCall(v8::internal::Call*) v8/src/ast/prettyprinter.cc:451:3 (chrome+0x761f4e7)
    #56 v8::internal::CallPrinter::VisitNoStackOverflowCheck(v8::internal::AstNode*) v8/src/ast/prettyprinter.h:77:3 (chrome+0x7620f95)
    #57 v8::internal::CallPrinter::VisitAssignment(v8::internal::Assignment*) v8/src/ast/prettyprinter.h (chrome+0x761e93e)
    #58 v8::internal::CallPrinter::VisitNoStackOverflowCheck(v8::internal::AstNode*) v8/src/ast/prettyprinter.h (chrome+0x7620c9b)
    #59 Visit v8/src/ast/prettyprinter.h:77:3 (chrome+0x7620dd1)
    #60 Find v8/src/ast/prettyprinter.cc:72:5 (chrome+0x7620dd1)
    #61 FindStatements v8/src/ast/prettyprinter.cc:592:5 (chrome+0x7620dd1)
    #62 VisitBlock v8/src/ast/prettyprinter.cc:95:3 (chrome+0x7620dd1)
    #63 v8::internal::CallPrinter::VisitNoStackOverflowCheck(v8::internal::AstNode*) v8/src/ast/prettyprinter.h:77:3 (chrome+0x7620dd1)
    #64 Visit v8/src/ast/prettyprinter.h:77:3 (chrome+0x7620dd1)
    #65 Find v8/src/ast/prettyprinter.cc:72:5 (chrome+0x7620dd1)
    #66 FindStatements v8/src/ast/prettyprinter.cc:592:5 (chrome+0x7620dd1)
    #67 VisitBlock v8/src/ast/prettyprinter.cc:95:3 (chrome+0x7620dd1)
    #68 v8::internal::CallPrinter::VisitNoStackOverflowCheck(v8::internal::AstNode*) v8/src/ast/prettyprinter.h:77:3 (chrome+0x7620dd1)
    #69 Visit v8/src/ast/prettyprinter.h:77:3 (chrome+0x761cd36)
    #70 Find v8/src/ast/prettyprinter.cc:72:5 (chrome+0x761cd36)
    #71 v8::internal::CallPrinter::VisitTryCatchStatement(v8::internal::TryCatchStatement*) v8/src/ast/prettyprinter.cc:207:3 (chrome+0x761cd36)
    #72 v8::internal::CallPrinter::VisitNoStackOverflowCheck(v8::internal::AstNode*) v8/src/ast/prettyprinter.h:77:3 (chrome+0x7620e15)
    #73 Visit v8/src/ast/prettyprinter.h:77:3 (chrome+0x7620dd1)
    #74 Find v8/src/ast/prettyprinter.cc:72:5 (chrome+0x7620dd1)
    #75 FindStatements v8/src/ast/prettyprinter.cc:592:5 (chrome+0x7620dd1)
    #76 VisitBlock v8/src/ast/prettyprinter.cc:95:3 (chrome+0x7620dd1)
    #77 v8::internal::CallPrinter::VisitNoStackOverflowCheck(v8::internal::AstNode*) v8/src/ast/prettyprinter.h:77:3 (chrome+0x7620dd1)
    #78 Visit v8/src/ast/prettyprinter.h:77:3 (chrome+0x761cd36)
    #79 Find v8/src/ast/prettyprinter.cc:72:5 (chrome+0x761cd36)
    #80 v8::internal::CallPrinter::VisitTryCatchStatement(v8::internal::TryCatchStatement*) v8/src/ast/prettyprinter.cc:207:3 (chrome+0x761cd36)
    #81 v8::internal::CallPrinter::VisitNoStackOverflowCheck(v8::internal::AstNode*) v8/src/ast/prettyprinter.h:77:3 (chrome+0x7620e15)
    #82 Visit v8/src/ast/prettyprinter.h:77:3 (chrome+0x7620dd1)
    #83 Find v8/src/ast/prettyprinter.cc:72:5 (chrome+0x7620dd1)
    #84 FindStatements v8/src/ast/prettyprinter.cc:592:5 (chrome+0x7620dd1)
    #85 VisitBlock v8/src/ast/prettyprinter.cc:95:3 (chrome+0x7620dd1)
    #86 v8::internal::CallPrinter::VisitNoStackOverflowCheck(v8::internal::AstNode*) v8/src/ast/prettyprinter.h:77:3 (chrome+0x7620dd1)
    #87 Visit v8/src/ast/prettyprinter.h:77:3 (chrome+0x76211e8)
    #88 Find v8/src/ast/prettyprinter.cc:72:5 (chrome+0x76211e8)
    #89 FindStatements v8/src/ast/prettyprinter.cc:592:5 (chrome+0x76211e8)
    #90 VisitFunctionLiteral v8/src/ast/prettyprinter.cc:224:3 (chrome+0x76211e8)
    #91 v8::internal::CallPrinter::VisitNoStackOverflowCheck(v8::internal::AstNode*) v8/src/ast/prettyprinter.h:77:3 (chrome+0x76211e8)
    #92 Visit v8/src/ast/prettyprinter.h:77:3 (chrome+0x761bacb)
    #93 Find v8/src/ast/prettyprinter.cc:72:5 (chrome+0x761bacb)
    #94 v8::internal::CallPrinter::Print(v8::internal::FunctionLiteral*, int) v8/src/ast/prettyprinter.cc:58:3 (chrome+0x761bacb)
    #95 v8::internal::ErrorUtils::ThrowLoadFromNullOrUndefined(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::MaybeHandle<v8::internal::Object>) v8/src/execution/messages.cc:926:36 (chrome+0x77bf047)
    #96 v8::internal::LoadIC::Load(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Name>, bool, v8::internal::Handle<v8::internal::Object>) v8/src/ic/ic.cc:431:7 (chrome+0x7957c7c)
    #97 __RT_impl_Runtime_LoadNoFeedbackIC_Miss v8/src/ic/ic.cc:2555:3 (chrome+0x79679d0)
    #98 v8::internal::Runtime_LoadNoFeedbackIC_Miss(int, unsigned long*, v8::internal::Isolate*) v8/src/ic/ic.cc:2540:1 (chrome+0x79679d0)
    #99 <null> <null> (0x7edd000d6837)

ThreadSanitizer can not provide additional info.
SUMMARY: ThreadSanitizer: SEGV /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/tsan/../sanitizer_common/sanitizer_atomic_clang_x86.h:46:14 in atomic_load<__sanitizer::atomic_uint16_t>
==19858==ABORTING


```

### m....@gmail.com (2021-09-14)

Only keep the reproduced video of the key information, the time required for tsan to reproduce this problem is not very stable, so the easiest way is to wait a while to check the log~

### ml...@chromium.org (2021-09-14)

I have now a Win64 setup with the repro in #0 up and running without success.

It's likely just dependent on memory pressure and hardware specs.

### m....@gmail.com (2021-09-14)

re https://crbug.com/chromium/1248435#c26

I Have tested on 32gb(16core) 64gb(32core) memory with windows and 12gb(4core) with ubuntu.


### ad...@google.com (2021-09-14)

mlippautz@, sorry, it wasn't my intention that you try to reproduce this, I'm sorry you spent lots of time on it today. It was my hope that you might be able to get a clue just by code inspection of the various stack traces.

Is there hope that you can resolve this by spotting clues in the stack traces that the reporter has provided?

If not, I'm sorry m.cooolie@, we know from bitter experience that such complicated test cases are almost never reproducible when moved to a different environment. I think we'll need to mark this as WontFix until you can come up with a *much* simpler test case. I'm sure you've found a real bug here, but it's not actionable unless we can reproduce it or there's convincing proof of the root cause.

### ml...@chromium.org (2021-09-14)

> mlippautz@, sorry, it wasn't my intention that you try to reproduce this, I'm sorry you spent lots of time on it today. It was my hope that you might be able to get a clue just by code inspection of the various stack traces.

Unfortunately, I don't see anything obvious. These codepaths are executed all over the place in all builds, so it's likely a corner case.

> Is there hope that you can resolve this by spotting clues in the stack traces that the reporter has provided?

Not really, it looks like a conservative GC doesn't find an object that supposedly has a reference still somewhere on the stack.

I have the setup now, so I keep the repro running for a few more hours to see if anything starts to repro. After all, this looks like a real issue.

### m....@gmail.com (2021-09-15)

I don’t think it has anything to do with the machine configuration or environment. My five windows machines with different configurations can reproduce stably. I will provide a modified ch.test2 (using the new user profile each time), you can try again Or change a colleague to see if it can reproduce.

node ch.test2.js D:\chrome_asan\asan-win32-release_x64-920053\chrome.exe http://localhost/poc.html

http server request log should like this.
```
poc>python3 -m http.server 80
Serving HTTP on :: port 80 (http://[::]:80/) ...
::1 - - [15/Sep/2021 10:52:22] "GET /poc.html HTTP/1.1" 200 -
::1 - - [15/Sep/2021 10:52:22] "GET /webgl-test-utils.js HTTP/1.1" 200 -
::1 - - [15/Sep/2021 10:52:22] "GET /h1.js HTTP/1.1" 200 -
::1 - - [15/Sep/2021 10:52:22] "GET /test.jpg HTTP/1.1" 200 -
::1 - - [15/Sep/2021 10:52:22] "GET /viper.ogg HTTP/1.1" 200 -
::1 - - [15/Sep/2021 10:52:22] "GET /viper.mp3 HTTP/1.1" 200 -
::1 - - [15/Sep/2021 10:52:22] "GET /demicmAudioShort.mp3 HTTP/1.1" 200 -
::1 - - [15/Sep/2021 10:52:22] "GET /test.mp4 HTTP/1.1" 200 -
::1 - - [15/Sep/2021 10:52:40] code 404, message File not found
::1 - - [15/Sep/2021 10:52:40] "GET /non-exist.mp4 HTTP/1.1" 404 -
```

### ad...@google.com (2021-09-15)

mlippautz@ do you have access to a Windows machine? If I impose on a colleague to spend a bit of time tomorrow trying to reproduce the original (Windows, ASAN) case, will that benefit you in trying to diagnose this, or do we really need a reliable cross-platform poc?

### ml...@chromium.org (2021-09-15)

I actually tried to repro #0 on a Win64 cloudtop that I use for these purposes without luck.

Linux POC is always way easier to work with but if we get it running on one of our Win64 corp configs that would likely make this actionable.

### m....@gmail.com (2021-09-15)

A newly discovered stack frame.
```
=================================================================
==10792==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7ffcb36e8060 at pc 0x7ffca4165fbe bp 0x0040d0bfd240 sp 0x0040d0bfd288
READ of size 8 at 0x7ffcb36e8060 thread T0
==10792==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffca4165fbd in blink::EventListenerMap::Add C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_listener_map.cc:144
    #1 0x7ffca0d2ad15 in blink::EventTarget::AddEventListenerInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_target.cc:481
    #2 0x7ffca785df73 in blink::MediaCustomControlsFullscreenDetector::Attach C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\media\media_custom_controls_fullscreen_detector.cc:86
    #3 0x7ffca3d2efd7 in blink::HTMLVideoElement::InsertedInto C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\media\html_video_element.cc:128
    #4 0x7ffca10dbdf1 in blink::ContainerNode::NotifyNodeInsertedInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:994
    #5 0x7ffca10d6602 in blink::ContainerNode::InsertNodeVector<blink::ContainerNode::AdoptAndAppendChild> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:333
    #6 0x7ffca10d1be3 in blink::ContainerNode::AppendChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:913
    #7 0x7ffca0e6dd82 in blink::Node::appendChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\node.cc:757
    #8 0x7ffca4b0280a in blink::`anonymous namespace'::v8_node::AppendChildOperationCallbackForMainWorld C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_node.cc:476
    #9 0x7ffc97f00857 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:152
    #10 0x7ffc97efdbd4 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
    #11 0x7ffc97efafbf in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:142
    #12 0x7ffc97efa30c in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130
    #13 0x7ee6000c113b  (<unknown module>)

0x7ffcb36e8060 is located 32 bytes to the left of global variable '<string literal>' defined in '../..\third_party/blink/renderer/core/intersection_observer/element_intersection_observer_data.h:52:12' (0x7ffcb36e8080) of size 32
  '<string literal>' is ascii string 'ElementIntersectionObserverData'
0x7ffcb36e8060 is located 8 bytes to the right of global variable '??_7ElementIntersectionObserverData@blink@@6B@' defined in '../../third_party/blink/renderer/core/intersection_observer/element_intersection_observer_data.cc' (0x7ffcb36e8040) of size 24
SUMMARY: AddressSanitizer: global-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_listener_map.cc:144 in blink::EventListenerMap::Add
Shadow bytes around the buggy address:
  0x11705e1dcfb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11705e1dcfc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11705e1dcfd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11705e1dcfe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11705e1dcff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x11705e1dd000: 00 00 00 00 00 00 00 00 00 00 00 f9[f9]f9 f9 f9
  0x11705e1dd010: 00 00 00 00 f9 f9 f9 f9 00 00 00 00 00 00 00 00
  0x11705e1dd020: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11705e1dd030: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11705e1dd040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11705e1dd050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==10792==ABORTING
```

### ml...@chromium.org (2021-09-15)

The stack trace won't help here as we already know the breaking area. The underlying issue is likely somewhere buried deeper in the GC/bindigns infrastructure.

If we get a reliable repro we can investigate this.

### m....@gmail.com (2021-09-15)

I have no idea why you can't reproduce stably.

### wf...@chromium.org (2021-09-15)

I cannot reproduce with the set of poc/instructions in #30. Perhaps this is hardware specific? I am trying in a VM.

I am using node version 14.17.6, puppeteer-core@10.2.0 and asan-win32-release_x64-920053 on Win 10 21h1 OS Build 19043.1237 with VMware SVGA display adapter.

### ad...@google.com (2021-09-15)

mlippautz@ we discussed this within security. Normally, we don't pass un-reproducible bugs onto engineering teams (except in the rare case that a root cause is identified), but I think in this case we're all agreed that there almost certainly _is_ a bug here so we'd like to ask you if you can dig further.

I think you won't be able to reproduce this on:
- A corp machine (we do not allow running of non-trivial test cases on corp machines)
- Any kind of VM (because we have now tried three different VM environments, with no success)
- Anything non-Windows

So I think the remaining option here is for you to go and buy a Windows PC and expense it. It would be worth getting one which closely matches one of the configurations on which m.cooolie@ has hit this problem. m.cooolie@ please would you describe the PC configurations you used. And mlippautz@ please let me know if you have trouble getting permission to expense a PC - I'll poke people as necessary.

Even then I _still_ think it's a 50/50 chance whether this is reproducible. It seems to me quite likely that this is dependent on timing, timezones, locales, GPU drivers, or any number of other things that we haven't thought of.

Assuming this is sufficient render memory corruption to achieve code execution => high severity.

### m....@gmail.com (2021-09-16)

re https://crbug.com/chromium/1248435#c36 https://crbug.com/chromium/1248435#c32
Test file from https://crbug.com/chromium/1248435#c30

I tested it in various environments, and the results are as follows. 
It does confirm that poc.html is difficult to trigger in a virtual machine environment, but the trigger probability of fuzz-00001.html in a 12gb 6core environment is basically the same as that of the real machine.
So I suggest to use fuzz-00001.html to test

VMWare base on RealPc(AMD Ryzen 7 PRO 4750G with Radeon Graphics (16 CPUs 64gbRAM))

File	VMWare(2core 8gbRAM)	VMWare(6core 12gbRAM)	RealPc(AMD Ryzen 7 PRO 4750G with Radeon Graphics (16 CPUs 64gbRAM))	i9 9900k(16core 32gbRAM gtx1060ti)
poc.html	NOT REPRODUCE	NOT REPRODUCE	REPRODUCE Stable	REPRODUCE Stable
fuzz-00001.html	REPRODUCE need long time	REPRODUCE Stable	REPRODUCE Stable	REPRODUCE Stable



### ml...@chromium.org (2021-09-16)

Still cannot reproduce but I have a theory that I think can lead to that specific crash which relates it to https://crbug.com/chromium/1244057.

What we found in the other issue is that one specific marking barrier that keeps the marking state consistent (no marked -> unmarked reference) was not firing in certain cases (slot on stack). We assumed it benign as it looked like we only had a single callsite and we couldn't see how that creates more issues. Turns out the barrier is also generally used for HashTable here [1].

Potential repro:
- Some blink::Node's have out-of-line EventTargetData which is stored in an EventTargetDataMap [2].
- That hash map is an ephemeron map for EventTargetDataObject and there's no other edge to EventTargetDataObject, so missing out on the ephemeron entry could lead to UAF.
- EventTargetDataObject inlines EventTargetData which inlines EventListenerMap which stores its entries in a HeapVector with inline capacity of 2 [3]. This means that the first 2 elements in this HeapVector are actually residing in EventTargetDataObject.
- So, missing out on marking EventTargetDataObject may explain a UAP in EventListenerMap and a dangling pointer.

Repro, assuming the write barrier in [1] doesn't fire. The issue doesn't even need concurrency but just incremental marking. Concurrent marking would suffer from the same issue though.

1. GC: Starts incremental marking.
2. Add a special Node with out-of-line EventTargetData and tries to add an event listener
3. GC: Incremental marking marks the already existing EventTargetDataMap and processes all existing ephemerons.
4. Add a new EventTargetDataObject.
5. GC: The write barrier doesn't fire, so the ephemeron entry is actually not processed
6: GC: In some final atomic GC pause, we don't clear the ephemeron entry, as they key -- the actual Node -- is still alive. What's wrong here is that value is not marked.
7: GC: Value of the ephemeron map (EventTargetDataObject) is swept and poisoned.
8. Any further access to the EventTargetDataObject, e.g., on a next GC, would trigger a UAP, or a TSAN race if that memory is already used otherwise.

We are working on a fix which requires one V8 and one Blink change.

m.cooolie@: It would be great if you could then run a new Chrome build through your repro.

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/wtf/hash_table.h;l=1882
[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/dom/node.cc;drc=2507e0d8b56f6c1b1fb53280d9453a93cee69cfa;bpv=1;bpt=1;l=2722?q=EventListenerMap&ss=chromium
[3] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/dom/events/event_listener_map.h;l=87?q=EventListenerMap&ss=chromium

### m....@gmail.com (2021-09-16)

re https://crbug.com/chromium/1248435#c32
Can i download prebuild version form here gs://chromium-browser-asan/win32-release_x64/?

### ml...@chromium.org (2021-09-16)

#40: We already submitted V8's patch but can only submit the Blink part once V8 rolls into Chromium. I will udpate once that happens and a prebuilt version should be available.

adetaylor@: Do you know how backmerges that need to go in sync work? We will have a Blink patch that also requires a patched (with a backmerge) V8 version. It's okay if V8 is first but it's not okay if Chromium is first.

### ml...@chromium.org (2021-09-16)

For the record, these are the patches:
- https://chromium-review.googlesource.com/c/v8/v8/+/3162127
- https://chromium-review.googlesource.com/c/chromium/src/+/3162170

### ad...@google.com (2021-09-16)

Re https://crbug.com/chromium/1248435#c41: for backmerges, when we get to that point, you should land the V8 change then wait until the V8 post-commit testing has designated a new LKGR for that V8 branch, then it should be OK to land the Blink CL.

### [Deleted User] (2021-09-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-09-16)

This is going to be in first re-spin right adetaylor@ or do we need to recut stable RC?

### ad...@google.com (2021-09-16)

Good question. As I marked this as FoundIn-94, Sheriffbot regards this as a regression and is thus blocking release.

However, I was unable to reproduce it and therefore we don't know whether it affects M93. I'm going to assume that it does, and remove RBS. We don't need to recut stable RC to await a fix.

### om...@chromium.org (2021-09-16)

Assuming our current understanding of this bug (as described in c#39) is correct, then this is specific to the Oilpan library which launched in M94 and thus the FoundIn-94 label is correct.

### ad...@google.com (2021-09-17)

Ah OK. That is a little awkward then. We don't ship high severity security regressions, so in principle we should block M94 till a fix has landed. In practice, that seems like not the right thing to do since these fixes are a little speculative. I'm not going to re-add RBS at this stage, but srinivassista@, keep your eyes on this one.

### ml...@chromium.org (2021-09-17)

Update: We are currently not rolling, so we cannot land crafted the Blink fix...

I suggest to not have RBS as the repro is really narrow and we have not actually seen it even pop up on crash/ as well. It would be bucketed somewhere under EventListenerMap.

Related: b/200206856

### gi...@appspot.gserviceaccount.com (2021-09-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2592254463789fd4c2ab6a4bce9f12cd1d7f93e5

commit 2592254463789fd4c2ab6a4bce9f12cd1d7f93e5
Author: Omer Katz <omerkatz@chromium.org>
Date: Fri Sep 17 13:16:22 2021

heap: Fix data race in HashTable::ExpandBuffer

ExpandBuffer uses memset to clear the original backnig store after
copying the contents to a temporary backing store. Allocating the
temporary backing store could start a GC, which means the original
backing store could be concurrently traced while memset is clearing it.

Drive-by: use more efficient version of AtomicMemzero in Reinitialize.

Bug: 1248435
Change-Id: Ieddc426625babfd1efb00bc33b1b4a60396a0cfd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3168851
Commit-Queue: Omer Katz <omerkatz@chromium.org>
Commit-Queue: Kentaro Hara <haraken@chromium.org>
Auto-Submit: Omer Katz <omerkatz@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#922492}

[modify] https://crrev.com/2592254463789fd4c2ab6a4bce9f12cd1d7f93e5/third_party/blink/renderer/platform/wtf/hash_table.h


### om...@chromium.org (2021-09-17)

Both CLs fro c#42 landed, but have reached canary yet.
M94 goes to stable on Sep 21st and we should try to back merge the above CLs as soon as possible.
Requesting merge to M94 and will submit them once the CLs have been tested on canary.
(since we need to wait for the V8 CL to roll before back merging the Blink CL, we might not have time to back merge both before M94 hits stable.)

### [Deleted User] (2021-09-17)

This bug requires manual review: We are only 3 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### om...@chromium.org (2021-09-17)

1. Yes, these CLs form a fix to a high impact security issue.
2. https://chromium-review.googlesource.com/c/v8/v8/+/3162127 and https://chromium-review.googlesource.com/c/chromium/src/+/3162170
3. CLs have landed on ToT, should reach canary soon and will be verified before they are back merged.
4. No
5. M94 introduced possible security issue in the form of a use-after-free, the CLs fix the issue.
6. No
7. No


### om...@chromium.org (2021-09-19)

Both CLs landed on Canary in 96.0.4646.0

### ml...@chromium.org (2021-09-20)

m.coolie@: Could you try reproducing from anything r922622+? [1]

E.g., gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-922637.zip ?

[1] https://chromiumdash.appspot.com/commit/ecce7fa146b20e4a6eb3ae5d4df2333b294b47f4

### m....@gmail.com (2021-09-20)

No longer reproduce on asan-win32-release_x64-922637.zip.

### ml...@chromium.org (2021-09-20)

For posterity, this is the description of the underlying bug:

//### 0. T_main: New `entry` was added and the table should be expanded. GC is off.

template <typename Key,
          typename Value,
          typename Extractor,
          typename HashFunctions,
          typename Traits,
          typename KeyTraits,
          typename Allocator>
Value*
HashTable<Key, Value, Extractor, HashFunctions, Traits, KeyTraits, Allocator>::
    ExpandBuffer(unsigned new_table_size, Value* entry, bool& success) {
  success = false;
  DCHECK_LT(table_size_, new_table_size);
  CHECK(Allocator::IsAllocationAllowed());

//### 1. T_main: GC is off, `table_` is expanded in size.
  if (!table_ ||
      !Allocator::template ExpandHashTableBacking<ValueType, HashTable>(
          table_, new_table_size * sizeof(ValueType)))
    return nullptr;

  success = true;

  Value* new_entry = nullptr;
  unsigned old_table_size = table_size_;
  ValueType* original_table = table_;

  ValueType* temporary_table = AllocateTable(old_table_size);
//### 2. T_main: The allocation started a GC
//### 3. T_gc: Concurrent marking picks up `table_` (kept on stack as `original_table`) through a global variable. Nothing is marked yet.
  for (unsigned i = 0; i < old_table_size; i++) {
    if (&table_[i] == entry)
      new_entry = &temporary_table[i];
    if (IsEmptyOrDeletedBucket(table_[i])) {
      DCHECK_NE(&table_[i], entry);
      if (Traits::kEmptyValueIsZero) {
        memset(&temporary_table[i], 0, sizeof(ValueType));
      } else {
        InitializeBucket(temporary_table[i]);
      }
    } else {
      Mover<ValueType, Allocator, Traits,
            Traits::template NeedsToForbidGCOnMove<>::value>::
          Move(std::move(table_[i]), temporary_table[i]);
      table_[i].~ValueType();
    }
  }
  table_ = temporary_table;
  Allocator::template BackingWriteBarrier(&table_);
//### 4. T_main: The temporary table (`temporary_table`) which things have been moved to is enqueue for a write barrier strongifying all elements.

//### 5. T_gc: The GC finds a random subset of buckts in `original_table` to be alive as it processes the backing while it's zeroed at the same time on the main thread. For ephemeron buckets this means that no ephemeron callback is registered for a bucket if it is zero.
  if (Traits::kEmptyValueIsZero) {
    AtomicMemzero(original_table, new_table_size * sizeof(ValueType));
  } else {
    for (unsigned i = 0; i < new_table_size; i++)
      InitializeBucket(original_table[i]);
  }
//### 6. T_main: Call to RehashTo with the `original_table` as new backing.
  new_entry = RehashTo(original_table, new_table_size, new_entry);

  return new_entry;
}

template <typename Key,
          typename Value,
          typename Extractor,
          typename HashFunctions,
          typename Traits,
          typename KeyTraits,
          typename Allocator>
Value*
HashTable<Key, Value, Extractor, HashFunctions, Traits, KeyTraits, Allocator>::
    RehashTo(ValueType* new_table, unsigned new_table_size, Value* entry) {

//### 6. T_main: A temporary hash table with the `original_table` backing is created on stack.

  HashTable new_hash_table(RawStorageTag{}, new_table, new_table_size);

//### 7. T_main: Entries are moved over from `temporary_table` to `original_table`. Moving of an ephemeron pair with Member<> also clears the moved from Member<> meaning that the barrier in 4. will not find any pointers.

  Value* new_entry = nullptr;
  for (unsigned i = 0; i != table_size_; ++i) {
    if (IsEmptyOrDeletedBucket(table_[i])) {
      DCHECK_NE(&table_[i], entry);
      continue;
    }
    Value* reinserted_entry = new_hash_table.Reinsert(std::move(table_[i]));
    if (&table_[i] == entry) {
      DCHECK(!new_entry);
      new_entry = reinserted_entry;
    }
  }

//### 8. T_main: BUG: This barrier should strongify all entries in the `original_table` again but didn't as it had a wrong bailout for on-stack slots.
  Allocator::TraceBackingStoreIfMarked(new_hash_table.table_);

//### 9. T_main: At this point we have a backing store of ephemeron buckets that has only a partial set of backing buckets registered for ephemeron processing and has not had all its buckets strongified. Since for ephemeron it's likely that Key is the only retainer of Value, this results in a live Key with a dead Value. The final weak callback that should clear dead buckets will not remove any such inconsistent pairs, as the Key is alive (and thus the bucket is considered alive).

  ValueType* old_table = table_;
  unsigned old_table_size = table_size_;

  // This swaps the newly allocated buffer with the current one. The store to
  // the current table has to be atomic to prevent races with concurrent marker.
//### 10. T_main: This regular backing barrier does not fire as the backing store was already marked black.
  AsAtomicPtr(&table_)->store(new_hash_table.table_, std::memory_order_relaxed);
  Allocator::template BackingWriteBarrier(&table_);
  table_size_ = new_table_size;

  new_hash_table.table_ = old_table;
  new_hash_table.table_size_ = old_table_size;

  // Explicitly clear since garbage collected HashTables don't do this on
  // destruction.
  new_hash_table.clear();

  deleted_count_ = 0;

  return new_entry;
}

### ad...@google.com (2021-09-20)

Thanks for the write-up, that's really interesting.

Marking as Verified per https://crbug.com/chromium/1248435#c58.

### [Deleted User] (2021-09-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-20)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-09-21)

I'm very sorry to reopen the case, the fuzzer based on the asan-win32-release_x64-922637.zip version still has the same crash for a while.
=================================================================
==10784==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7ffab8cf32a0 at pc 0x7ffaa97b9f6e bp 0x0078b49fb8a0 sp 0x0078b49fb8e8
READ of size 8 at 0x7ffab8cf32a0 thread T0
==10784==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffaa97b9f6d in blink::EventListenerMap::Add C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_listener_map.cc:144
    #1 0x7ffaa63bec65 in blink::EventTarget::AddEventListenerInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_target.cc:481
    #2 0x7ffaace8c273 in blink::MediaCustomControlsFullscreenDetector::Attach C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\media\media_custom_controls_fullscreen_detector.cc:86
    #3 0x7ffaa938fd67 in blink::HTMLVideoElement::InsertedInto C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\media\html_video_element.cc:128
    #4 0x7ffaa676b531 in blink::ContainerNode::NotifyNodeInsertedInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:994
    #5 0x7ffaa6765d42 in blink::ContainerNode::InsertNodeVector<blink::ContainerNode::AdoptAndAppendChild> C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:333
    #6 0x7ffaa6761323 in blink::ContainerNode::AppendChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:913
    #7 0x7ffaa6500ee2 in blink::Node::appendChild C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\node.cc:757
    #8 0x7ffaaa14c90a in blink::`anonymous namespace'::v8_node::AppendChildOperationCallbackForMainWorld C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_node.cc:476
    #9 0x7ffa9d557817 in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:152
    #10 0x7ffa9d554b94 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
    #11 0x7ffa9d551f7f in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:142
    #12 0x7ffa9d5512cc in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130
    #13 0x7ecf000c113b  (<unknown module>)

0x7ffab8cf32a0 is located 32 bytes to the left of global variable '<string literal>' defined in '../..\third_party/blink/renderer/core/intersection_observer/element_intersection_observer_data.h:52:12' (0x7ffab8cf32c0) of size 32
  '<string literal>' is ascii string 'ElementIntersectionObserverData'
0x7ffab8cf32a0 is located 8 bytes to the right of global variable '??_7ElementIntersectionObserverData@blink@@6B@' defined in '../../third_party/blink/renderer/core/intersection_observer/element_intersection_observer_data.cc' (0x7ffab8cf3280) of size 24
SUMMARY: AddressSanitizer: global-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\events\event_listener_map.cc:144 in blink::EventListenerMap::Add
Shadow bytes around the buggy address:
  0x11d831b9e600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e610: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e620: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e630: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e640: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x11d831b9e650: 00 00 00 f9[f9]f9 f9 f9 00 00 00 00 f9 f9 f9 f9
  0x11d831b9e660: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e670: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e690: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x11d831b9e6a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==10784==ABORTING

### ad...@google.com (2021-09-21)

Thanks. I copied https://crbug.com/chromium/1248435#c63 to a new bug, https://crbug.com/chromium/1251673.

PLEASE DISCUSS ONGOING WORK OVER THERE instead of here.

It makes things like merge labels much easier.

### am...@chromium.org (2021-09-21)

in response to https://crbug.com/chromium/1248435#c54, 94 stable RC was already cut before this CL was landed for release today; I've gone ahead and approved for merge to 94 now; as long as no issues seen from Canary testing, please go ahead and backmerge the Blink fix to M94/branch 4606 so it an be included in the next stable refresh 

### om...@google.com (2021-09-22)

We need to back merge and roll the v8 CL (https://chromium-review.googlesource.com/c/v8/v8/+/3162127) first before back merging the Blink fix.
Is there a specific branch we should back merge to?

### va...@google.com (2021-09-23)

Please back merge v8 CLs into the correct V8 release branch.
This branch ref (in that case https://chromium.googlesource.com/v8/v8/+/refs/heads/9.4-lkgr) is used on the chromium end.
Please BM the blink change afterwards.

srinivassista@ FYI - Anything else we need to do?

### am...@google.com (2021-09-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-23)

And another one - congratulations! The VRP Panel has decided to award you $7500 for this report. Thank you for this report! 

### m....@gmail.com (2021-09-23)

Thank you~

### gi...@appspot.gserviceaccount.com (2021-09-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/2bc226d4704d0eecc0ab0095b092ba69b31f2b2c

commit 2bc226d4704d0eecc0ab0095b092ba69b31f2b2c
Author: Omer Katz <omerkatz@chromium.org>
Date: Thu Sep 16 11:49:37 2021

cppgc: Add GetWriteBarrierType that ignores slots

GetWriteBarrierType used to consider the slot so that a barrier is not
triggered for on-stack slots. For strongifying weak collections we want
the write barrier to trigger even if the backing store is only reachable
from stack.

Blink counterpart: crrev.com/c/3162170

(cherry picked from commit ed0459770fff9e5ee3e9107c6efff58e6f801058)

Bug: chromium:1248435, chromium:1244057
Change-Id: I75b1ca62ad5de7bae3d2f4c1a9acce839f3ccdc1
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3162127
Commit-Queue: Omer Katz <omerkatz@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#76872}
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3181531
Cr-Commit-Position: refs/branch-heads/9.4@{#35}
Cr-Branched-From: 3b51863bc25492549a8bf96ff67ce481b1a3337b-refs/heads/9.4.146@{#1}
Cr-Branched-From: 2890419fc8fb9bdb507fdd801d76fa7dd9f022b5-refs/heads/master@{#76233}

[modify] https://crrev.com/2bc226d4704d0eecc0ab0095b092ba69b31f2b2c/include/cppgc/internal/write-barrier.h
[modify] https://crrev.com/2bc226d4704d0eecc0ab0095b092ba69b31f2b2c/include/cppgc/heap-consistency.h


### am...@google.com (2021-09-24)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/636651f9f4311b52cc0a1587e4d988b3233c9502

commit 636651f9f4311b52cc0a1587e4d988b3233c9502
Author: Omer Katz <omerkatz@chromium.org>
Date: Sun Sep 26 22:31:41 2021

heap: Fix write barrier for HashTable backing store

Use version of GetWriteBarrierType that allows for strongifying backing
store reachable only from stack.

This CL is dependant on crrev.com/c/3162127

(cherry picked from commit ecce7fa146b20e4a6eb3ae5d4df2333b294b47f4)

Bug: 1248435, 1244057
Change-Id: I1fb7f46e401bf524fee418eff9de282cf3d362d0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3162170
Commit-Queue: Omer Katz <omerkatz@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#922622}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3183343
Cr-Commit-Position: refs/branch-heads/4606@{#1225}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/636651f9f4311b52cc0a1587e4d988b3233c9502/third_party/blink/renderer/platform/heap/impl/heap_allocator_impl.h
[modify] https://crrev.com/636651f9f4311b52cc0a1587e4d988b3233c9502/third_party/blink/renderer/platform/wtf/allocator/partition_allocator.h
[modify] https://crrev.com/636651f9f4311b52cc0a1587e4d988b3233c9502/third_party/blink/renderer/platform/heap/v8_wrapper/heap_allocator_impl.h
[modify] https://crrev.com/636651f9f4311b52cc0a1587e4d988b3233c9502/third_party/blink/renderer/platform/wtf/hash_table.h
[modify] https://crrev.com/636651f9f4311b52cc0a1587e4d988b3233c9502/third_party/blink/renderer/platform/heap/test/incremental_marking_test.cc


### om...@chromium.org (2021-10-01)

The fixes above landed in M96 and were back merged to M94. We should also merge them to M95.

### [Deleted User] (2021-10-01)

Merge review required: M95 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### om...@chromium.org (2021-10-01)

1. Yes, these CLs form a fix to a high impact security issue.
2. https://chromium-review.googlesource.com/c/v8/v8/+/3162127 and https://chromium-review.googlesource.com/c/chromium/src/+/3162170
3. Yes.
4. No
5. Not Chrome OS
6. No


### am...@chromium.org (2021-10-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-01)

Please go ahead and merge the V8 fix into the appropriate V8 release branch for M95, and the Blink fix into branch 4638. Thanks again all for your all your efforts with this one! 

### om...@chromium.org (2021-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1248435?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1250466]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057221)*
