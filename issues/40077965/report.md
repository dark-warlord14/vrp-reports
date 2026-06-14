# Heap-use-after-free in ppapi::proxy::PluginResource::NotifyInstanceWasDeleted

| Field | Value |
|-------|-------|
| **Issue ID** | [40077965](https://issues.chromium.org/issues/40077965) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ch...@gmail.com |
| **Assignee** | bb...@chromium.org |
| **Created** | 2013-08-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Test case in <https://crbug.com/chromium/227350> and 159429 reproduces again.

**VERSION**  

Chrome Version: [29.0.1547.57] + [beta]  

[31.0.1607.0 (218472)] + [trunk]  

Operating System: [Ubuntu 12.04 64bit]

**REPRODUCTION CASE**  

ppapi PDF plugin should be available.

1. Download and copy repro.html to local web server.
2. Open chrome and open repro.html.
3. Sad tab is displayed.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State: ASAN output

==28872==ERROR: AddressSanitizer: heap-use-after-free on address 0x61300002ddc8 at pc 0x7f763f509092 bp 0x7fff190c5360 sp 0x7fff190c5358  

READ of size 8 at 0x61300002ddc8 thread T0 (chrome)  

#0 0x7f763f509091 in std::\_Rb\_tree<int, std::pair<int const, scoped\_refptr[ppapi::proxy::PluginResourceCallbackBase](javascript:void(0);) >, std::\_Select1st<std::pair<int const, scoped\_refptr[ppapi::proxy::PluginResourceCallbackBase](javascript:void(0);) > >, std::less<int>, std::allocator<std::pair<int const, scoped\_refptr[ppapi::proxy::PluginResourceCallbackBase](javascript:void(0);) > > >::\_M\_begin() /usr/lib/gcc/x86\_64-linux-gnu/4.6/../../../../include/c++/4.6/bits/stl\_tree.h:493  

#1 0x7f763f52f32e in std::\_Rb\_tree<int, std::pair<int const, scoped\_refptr[ppapi::proxy::PluginResourceCallbackBase](javascript:void(0);) >, std::\_Select1st<std::pair<int const, scoped\_refptr[ppapi::proxy::PluginResourceCallbackBase](javascript:void(0);) > >, std::less<int>, std::allocator<std::pair<int const, scoped\_refptr[ppapi::proxy::PluginResourceCallbackBase](javascript:void(0);) > > >::clear() /usr/lib/gcc/x86\_64-linux-gnu/4.6/../../../../include/c++/4.6/bits/stl\_tree.h:809  

#2 0x7f763d879420 in ppapi::ResourceTracker::DidDeleteInstance(int) out/Release/../../ppapi/shared\_impl/resource\_tracker.cc:160  

#3 0x7f763e84e9c3 in content::HostGlobals::InstanceDeleted(int) out/Release/../../content/renderer/pepper/host\_globals.cc:257  

#4 0x7f763e5cc562 in ~PepperPluginInstanceImpl out/Release/../../content/renderer/pepper/pepper\_plugin\_instance\_impl.cc:563  

#5 0x7f763e5cc17d in ~PepperPluginInstanceImpl out/Release/../../content/renderer/pepper/pepper\_plugin\_instance\_impl.cc:524  

#6 0x7f763e8b36a7 in scoped\_refptr[content::PepperPluginInstanceImpl](javascript:void(0);)::operator=(content::PepperPluginInstanceImpl\*) out/Release/../../base/memory/ref\_counted.h:267  

#7 0x7f763e8b3887 in content::PepperWebPluginImpl::destroy() out/Release/../../content/renderer/pepper/pepper\_webplugin\_impl.cc:126  

#8 0x7f763fbfa03e in ~WebPluginContainerImpl out/Release/../../third\_party/WebKit/Source/web/WebPluginContainerImpl.cpp:648  

#9 0x7f763fbf9edd in ~WebPluginContainerImpl out/Release/../../third\_party/WebKit/Source/web/WebPluginContainerImpl.cpp:642  

#10 0x7f764236e0e3 in WTF::HashTable<WTF::RefPtr[WebCore::Widget](javascript:void(0);), WTF::KeyValuePair<WTF::RefPtr[WebCore::Widget](javascript:void(0);), WebCore::FrameView\*>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::RefPtr[WebCore::Widget](javascript:void(0);), WebCore::FrameView\*> >, WTF::PtrHash<WTF::RefPtr[WebCore::Widget](javascript:void(0);) >, WTF::KeyValuePairHashTraits<WTF::HashTraits<WTF::RefPtr[WebCore::Widget](javascript:void(0);) >, WTF::HashTraits[WebCore::FrameView\\*](javascript:void(0);) >, WTF::HashTraits<WTF::RefPtr[WebCore::Widget](javascript:void(0);) > >::deallocateTable(WTF::KeyValuePair<WTF::RefPtr[WebCore::Widget](javascript:void(0);), WebCore::FrameView\*>\*, int) out/Release/../../third\_party/WebKit/Source/wtf/HashTable.h:876  

#11 0x7f7642367499 in WebCore::WidgetHierarchyUpdatesSuspensionScope::moveWidgets() out/Release/../../third\_party/WebKit/Source/core/rendering/RenderWidget.cpp:69  

#12 0x7f76416b7da9 in ~WidgetHierarchyUpdatesSuspensionScope out/Release/../../third\_party/WebKit/Source/core/rendering/RenderWidget.h:40  

#13 0x7f76416b2c2d in WebCore::ContainerNode::removeChild(WebCore::Node\*, WebCore::ExceptionState&) out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:498  

#14 0x7f76416b14a0 in WebCore::collectChildrenAndRemoveFromOldParent(WebCore::Node\*, WTF::Vector<WTF::RefPtr[WebCore::Node](javascript:void(0);), 11ul>&, WebCore::ExceptionState&) out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:70  

#15 0x7f76416b1139 in WebCore::ContainerNode::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), WebCore::ExceptionState&, WebCore::AttachBehavior) out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:609  

#16 0x7f7641798fda in WebCore::Node::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), WebCore::ExceptionState&, WebCore::AttachBehavior) out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:543  

#17 0x7f7641e419c8 in WebCore::V8Node::appendChildMethodCustom(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) out/Release/../../third\_party/WebKit/Source/bindings/v8/custom/V8NodeCustom.cpp:120  

#18 0x7f7641d1773c in WebCore::NodeV8Internal::appendChildMethodCallbackForMainWorld(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) out/Release/gen/blink/bindings/V8Node.cpp:703  

#19 0x7f763ebe2b77 in v8::internal::FunctionCallbackArguments::Call(v8::Handle[v8::Value](javascript:void(0);) (\*)(v8::Arguments const&)) out/Release/../../v8/src/arguments.cc:103  

addr2line: '': No such file  

#20 0x7f763ec07425 in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1272  

#21 0x7f763ebfaf84 in v8::internal::Builtin\_HandleApiCall(int, v8::internal::Object\*\*, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1288  

#22 0x1a7a88f072ad in  

0x61300002ddc8 is located 72 bytes inside of 384-byte region [0x61300002dd80,0x61300002df00)  

freed by thread T0 (chrome) here:  

#0 0x7f763b0e9e95 in operator delete *asan\_rtl*  

#1 0x7f763d876f9a in ppapi::Resource::NotifyInstanceWasDeleted() out/Release/../../ppapi/shared\_impl/resource.cc:70  

#2 0x7f763f52e36d in ppapi::proxy::PluginResource::NotifyInstanceWasDeleted() out/Release/../../ppapi/proxy/plugin\_resource.cc:62  

#3 0x7f763d879420 in ppapi::ResourceTracker::DidDeleteInstance(int) out/Release/../../ppapi/shared\_impl/resource\_tracker.cc:160  

#4 0x7f763e84e9c3 in content::HostGlobals::InstanceDeleted(int) out/Release/../../content/renderer/pepper/host\_globals.cc:257  

#5 0x7f763e5cc562 in ~PepperPluginInstanceImpl out/Release/../../content/renderer/pepper/pepper\_plugin\_instance\_impl.cc:563  

#6 0x7f763e5cc17d in ~PepperPluginInstanceImpl out/Release/../../content/renderer/pepper/pepper\_plugin\_instance\_impl.cc:524  

#7 0x7f763e8b36a7 in scoped\_refptr[content::PepperPluginInstanceImpl](javascript:void(0);)::operator=(content::PepperPluginInstanceImpl\*) out/Release/../../base/memory/ref\_counted.h:267  

#8 0x7f763e8b3887 in content::PepperWebPluginImpl::destroy() out/Release/../../content/renderer/pepper/pepper\_webplugin\_impl.cc:126  

#9 0x7f763fbfa03e in ~WebPluginContainerImpl out/Release/../../third\_party/WebKit/Source/web/WebPluginContainerImpl.cpp:648  

#10 0x7f763fbf9edd in ~WebPluginContainerImpl out/Release/../../third\_party/WebKit/Source/web/WebPluginContainerImpl.cpp:642  

#11 0x7f764236e0e3 in WTF::HashTable<WTF::RefPtr[WebCore::Widget](javascript:void(0);), WTF::KeyValuePair<WTF::RefPtr[WebCore::Widget](javascript:void(0);), WebCore::FrameView\*>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::RefPtr[WebCore::Widget](javascript:void(0);), WebCore::FrameView\*> >, WTF::PtrHash<WTF::RefPtr[WebCore::Widget](javascript:void(0);) >, WTF::KeyValuePairHashTraits<WTF::HashTraits<WTF::RefPtr[WebCore::Widget](javascript:void(0);) >, WTF::HashTraits[WebCore::FrameView\\*](javascript:void(0);) >, WTF::HashTraits<WTF::RefPtr[WebCore::Widget](javascript:void(0);) > >::deallocateTable(WTF::KeyValuePair<WTF::RefPtr[WebCore::Widget](javascript:void(0);), WebCore::FrameView\*>\*, int) out/Release/../../third\_party/WebKit/Source/wtf/HashTable.h:876  

#12 0x7f7642367499 in WebCore::WidgetHierarchyUpdatesSuspensionScope::moveWidgets() out/Release/../../third\_party/WebKit/Source/core/rendering/RenderWidget.cpp:69  

#13 0x7f76416b7da9 in ~WidgetHierarchyUpdatesSuspensionScope out/Release/../../third\_party/WebKit/Source/core/rendering/RenderWidget.h:40  

#14 0x7f76416b2c2d in WebCore::ContainerNode::removeChild(WebCore::Node\*, WebCore::ExceptionState&) out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:498  

#15 0x7f76416b14a0 in WebCore::collectChildrenAndRemoveFromOldParent(WebCore::Node\*, WTF::Vector<WTF::RefPtr[WebCore::Node](javascript:void(0);), 11ul>&, WebCore::ExceptionState&) out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:70  

#16 0x7f76416b1139 in WebCore::ContainerNode::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), WebCore::ExceptionState&, WebCore::AttachBehavior) out/Release/../../third\_party/WebKit/Source/core/dom/ContainerNode.cpp:609  

#17 0x7f7641798fda in WebCore::Node::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), WebCore::ExceptionState&, WebCore::AttachBehavior) out/Release/../../third\_party/WebKit/Source/core/dom/Node.cpp:543  

#18 0x7f7641e419c8 in WebCore::V8Node::appendChildMethodCustom(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) out/Release/../../third\_party/WebKit/Source/bindings/v8/custom/V8NodeCustom.cpp:120  

#19 0x7f7641d1773c in WebCore::NodeV8Internal::appendChildMethodCallbackForMainWorld(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) out/Release/gen/blink/bindings/V8Node.cpp:703  

#20 0x7f763ebe2b77 in v8::internal::FunctionCallbackArguments::Call(v8::Handle[v8::Value](javascript:void(0);) (\*)(v8::Arguments const&)) out/Release/../../v8/src/arguments.cc:103  

#21 0x7f763ec07425 in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1272  

#22 0x7f763ebfaf84 in v8::internal::Builtin\_HandleApiCall(int, v8::internal::Object\*\*, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1288  

#23 0x1a7a88f072ad in  

#24 0x1a7a88f63a2e in  

#25 0x1a7a88f108b3 in  

#26 0x1a7a88f2acfd in  

#27 0x1a7a88f17e16 in  

#28 0x7f763ec77dd2 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) out/Release/../../v8/src/execution.cc:119  

#29 0x7f763ebb9e78 in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) out/Release/../../v8/src/api.cc:4387  

previously allocated by thread T0 (chrome) here:  

#0 0x7f763b0e9bd5 in operator new *asan\_rtl*  

#1 0x7f763e8908a0 in content::PepperInProcessResourceCreation::CreateURLLoader(int) out/Release/../../content/renderer/pepper/pepper\_in\_process\_resource\_creation.cc:131  

#2 0x7f7642adce63 in ppapi::thunk::(anonymous namespace)::Create(int) out/Release/../../ppapi/thunk/ppb\_url\_loader\_thunk.cc:29  

#3 0x7f762853d2ef in ?? ??:0  

#4 0x1e  

Shadow bytes around the buggy address:  

0x0c267fffdb60: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x0c267fffdb70: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c267fffdb80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c267fffdb90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c267fffdba0: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa  

=>0x0c267fffdbb0: fd fd fd fd fd fd fd fd fd[fd]fd fd fd fd fd fd  

0x0c267fffdbc0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c267fffdbd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c267fffdbe0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c267fffdbf0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c267fffdc00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

## Attachments

- [repro.html](attachments/repro.html) (text/html; charset=us-ascii, 400 B)

## Timeline

### ts...@chromium.org (2013-08-20)

repro'd in 31.0.1606.0 linux / asan.  Bill, I think you took a look at one of these recently, could you take a look at this, too?

### bb...@chromium.org (2013-08-20)

Checking it out.

### sc...@gmail.com (2013-08-24)

Thanks Chamal! Just making sure you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process

I remember that in the past, you were able to provide a repro that faulted at an address of 0x41414141, which a good start towards getting the new higher rewards.

### ch...@gmail.com (2013-08-24)

scarybeasts, thanks a lot for telling me about new rewards. It is really great :)
But this issue not possible to control between the free and the use from javascript. 

### ch...@gmail.com (2013-08-25)

Tested on new beta version 30.0.1599.14.
This test case does not crash when it is loaded.
But crashes only when page is refreshed.

### in...@chromium.org (2013-08-26)

[Empty comment from Monorail migration]

### 41...@gmail.com (2013-08-26)

hehe same date few hours diff :P 

chamal reported for linux i reported for windows does this matters for reward :P

another repro with object tag:

<object id=pdf-viewer src=filenotnecessary.pdf type="application/pdf"></object>
<script>

			
i = 0;
var pdf;
document.addEventListener('readystatechange', function() {
  
  if (i == 1)
  { 
  
	document.body.appendChild(pdf);
  }
  else
  {
   
	pdf = document.getElementById("pdf-viewer");
  }
  i++;
});

window.addEventListener('DOMContentLoaded', function() {

  pdf.reload();
});
</script> 

### js...@chromium.org (2013-08-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

Bbudge@, friendly ping. This regression is getting older, we should fix soon or revert the regression changeset. We can't leave a high severity regression on trunk.


### bb...@chromium.org (2013-09-03)

inferno@, can you link the regression CL? It's not obvious what it is from this bug. I'm OOO today but will have a look tomorrow.

### in...@chromium.org (2013-09-03)

Fix labels.

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### 41...@gmail.com (2013-09-04)

so as it reaches to reward panel my question is same:

chamal reported for linux and i reported for windows does this considered for 2 rewards?


### in...@chromium.org (2013-09-04)

41.w4r10r, this looks to be the same bug, with the same stack on both windows and linux. So, it won't qualify for double rewards.

### bb...@chromium.org (2013-09-04)

Looking at the previous version of this:
https://code.google.com/p/chromium/issues/detail?id=227350

We landed a refactoring of the URLLoader proxy which we thought would fix this issue, and it was in M29 but had to be reverted last week because it broke Docs print preview. The refactoring is in M30 and a different fix will be merged back into M30. So this should be fixed for M30 at least.

I'm not sure how to fix this for M29. It's non-trivial, since the code is quite different from trunk now. I think there have been several fixes for this and similar issues in the past. Is there a particular CL that we think would improve the situation if it were reverted?

### cl...@chromium.org (2013-09-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6050852536057856

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x614000046ac8
Crash State:
  - crash stack -
  ppapi::proxy::PluginResource::NotifyInstanceWasDeleted
  ppapi::ResourceTracker::DidDeleteInstance
  - free stack -
  ppapi::Resource::NotifyInstanceWasDeleted
  ppapi::proxy::PluginResource::NotifyInstanceWasDeleted
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=148563:148586

Minimized Testcase (0.30 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97Nl7NrQzYmDTmKFuRhcghyiDZYD_56S_8LPtzaMzO-IWhenLmVDPStMq7w5Ud0nUGB0PeXMv39f7DrIUS48-ktKPPq2t9K4-wstd4haF5dj7CSPX_VKC-JAFmkhGdrI8d26tx3aqnro3qz9c2l9uB3wM4nTw
<embed id=pdf-viewer src=filenotnecessary.pdf><script>
i = 0;
document.addEventListener('readystatechange', function() {
  
  {
        document.body.appendChild(e);
  }
});

window.addEventListener('DOMContentLoaded', function() {
  e = document.getElementById('pdf-viewer');
  e.reload();
});

</script>

Additional requirements: Requires HTTP



### in...@chromium.org (2013-09-05)

From regression range,only http://src.chromium.org/viewvc/chrome?view=rev&revision=148567 makes sense.

### ch...@gmail.com (2013-09-05)

Like all the previous issues related to ready state event and domcontentloaded event, this issue also happens because a ready state event can be fired when loaders are canceled within domcontentloaded event.

Please check whether it is possible to solve this stacktrace. This is how ready state event is fired.

Breakpoint 1, WebCore::Document::setReadyState (this=0x61e00000d880, 
    readyState=WebCore::Document::Complete)
    at ../../third_party/WebKit/Source/core/dom/Document.cpp:1112
1112        dispatchEvent(Event::create(eventNames().readystatechangeEvent));
(gdb) bt
#0  WebCore::Document::setReadyState (this=0x61e00000d880, 
    readyState=WebCore::Document::Complete)
    at ../../third_party/WebKit/Source/core/dom/Document.cpp:1112
#1  0x000055555e3792ed in WebCore::FrameLoader::checkCompleted (
    this=0x61700000eb70)
    at ../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:438
#2  0x000055555e1caaa3 in WebCore::ResourceFetcher::didLoadResource (
    this=0x611000001a80, resource=<optimized out>)
    at ../../third_party/WebKit/Source/core/fetch/ResourceFetcher.cpp:971
#3  0x000055555e1d98a9 in WebCore::ResourceLoader::releaseResources (
    this=0x61900007a880)
    at ../../third_party/WebKit/Source/core/fetch/ResourceLoader.cpp:91
#4  0x000055555e1da536 in WebCore::ResourceLoader::cancel (
    this=0x61900007a880, error=...)
    at ../../third_party/WebKit/Source/core/fetch/ResourceLoader.cpp:237
#5  0x000055555e1da1c6 in WebCore::ResourceLoader::cancel (this=0x7fffffff6ea0)
    at ../../third_party/WebKit/Source/core/fetch/ResourceLoader.cpp:202
#6  0x000055555e1b664f in WebCore::Resource::cancelTimerFired (
    this=0x61900007ad80, timer=0xe06ffa59)
    at ../../third_party/WebKit/Source/core/fetch/Resource.cpp:470
#7  0x000055555e1b8fc0 in WebCore::Resource::removeClient (
    this=0x61900007ad80, client=0x7fffffff76c0)
    at ../../third_party/WebKit/Source/core/fetch/Resource.cpp:439
---Type <return> to continue, or q <return> to quit---c
#8  0x000055555e36f920 in WebCore::DocumentThreadableLoader::clearResource (
    this=<optimized out>)
    at ../../third_party/WebKit/Source/core/loader/DocumentThreadableLoader.cpp:183
#9  0x000055555e36f6a1 in WebCore::DocumentThreadableLoader::cancelWithError (
    this=0x6110000322c0, error=...)
    at ../../third_party/WebKit/Source/core/loader/DocumentThreadableLoader.cpp:165
#10 0x000055555e36f416 in WebCore::DocumentThreadableLoader::cancel (
    this=0x7fffffff6ea0)
    at ../../third_party/WebKit/Source/core/loader/DocumentThreadableLoader.cpp:148
#11 0x000055555b91d580 in WebKit::AssociatedURLLoader::~AssociatedURLLoader (
    this=0x60600007e500)
    at ../../third_party/WebKit/Source/web/AssociatedURLLoader.cpp:303
#12 0x000055555b91d51e in WebKit::AssociatedURLLoader::~AssociatedURLLoader (
    this=0x60600007e500)
    at ../../third_party/WebKit/Source/web/AssociatedURLLoader.cpp:302
#13 0x000055555a2c8423 in content::PepperURLLoaderHost::~PepperURLLoaderHost (
    this=0x61200003d540)
    at ../../content/renderer/pepper/pepper_url_loader_host.cc:102
#14 0x000055555a2c824e in content::PepperURLLoaderHost::~PepperURLLoaderHost (
    this=0x61200003d540)
---Type <return> to continue, or q <return> to quit---c
    at ../../content/renderer/pepper/pepper_url_loader_host.cc:64
#15 0x0000555557fa5185 in ppapi::host::PpapiHost::OnHostMsgResourceDestroyed (
    this=<optimized out>, resource=<optimized out>)
    at ../../ppapi/host/ppapi_host.cc:262
#16 0x0000555557fa4f6b in PpapiHostMsg_ResourceDestroyed::Dispatch<ppapi::host::PpapiHost, ppapi::host::PpapiHost, void (ppapi::host::PpapiHost::*)(int)> (
    msg=<optimized out>, obj=0x610000009f40, sender=<optimized out>, 
    func=<optimized out>) at ../../ppapi/proxy/ppapi_messages.h:1165
#17 0x0000555557fa3775 in ppapi::host::PpapiHost::OnMessageReceived (
    this=0x610000009f40, msg=...) at ../../ppapi/host/ppapi_host.cc:63
#18 0x000055555a56fd6e in content::PepperInProcessRouter::SendToHost (
    this=<optimized out>, msg=<optimized out>)
    at ../../content/renderer/pepper/pepper_in_process_router.cc:113
#19 0x000055555a571944 in base::internal::InvokeHelper<false, bool, base::internal::RunnableAdapter<bool (content::PepperInProcessRouter::*)(IPC::Message*)>, void (content::PepperInProcessRouter*, IPC::Message* const&)>::MakeItSo(base::internal::RunnableAdapter<bool (content::PepperInProcessRouter::*)(IPC::Message*)>, content::PepperInProcessRouter*, IPC::Message* const&) (a1=<optimized out>, 
    a2=@0x7fffffff8b00: 0x6040000dfad0, runnable=...)
    at ../../base/bind_internal.h:890
#20 0x000055555a5716fc in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<bool (content::PepperInProcessRouter::*)(IPC::Message*)>, bool (content::PepperInProcessRouter*, IPC::Message*), void (base::inte---Type <return> to continue, or q <return> to quit---c
rnal::UnretainedWrapper<content::PepperInProcessRouter>)>, bool (content::PepperInProcessRouter*, IPC::Message*)>::Run(base::internal::BindStateBase*, IPC::Message* const&) (base=<optimized out>, x2=@0x7fffffff8b00: 0x6040000dfad0)
    at ../../base/bind_internal.h:1219
#21 0x000055555a571e7a in content::PepperInProcessRouter::Channel::Send (
    this=<optimized out>, message=<optimized out>)
    at ../../content/renderer/pepper/pepper_in_process_router.cc:30
#22 0x000055555b1fd3fa in ppapi::proxy::PluginResource::~PluginResource (
    this=0x61300004fc00) at ../../ppapi/proxy/plugin_resource.cc:28
#23 0x000055555b2a4d5e in ppapi::proxy::URLLoaderResource::~URLLoaderResource (
    this=0x61300004fc00) at ../../ppapi/proxy/url_loader_resource.cc:70
#24 0x0000555559543048 in ppapi::ResourceTracker::ReleaseResource (
    this=<optimized out>, res=<optimized out>)
    at ../../ppapi/shared_impl/resource_tracker.cc:90
#25 0x00007fffe924d17d in ?? ()
   from /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/out/Release/libpdf.so
#26 0x00007fffe9208e26 in ?? ()
   from /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/out/Release/libpdf.so
#27 0x00007fffe92094fe in ?? ()
   from /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/out/Release/libpdf.so
#28 0x00007fffe9212b88 in ?? ()
   from /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/out/Release/libpdf.so
#29 0x00007fffe9213a6d in ?? ()
   from /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/out/Release/libpdf.so
#30 0x00007fffe92529f1 in ?? ()
   from /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/out/Release/libpdf.so
#31 0x000055555a596d88 in content::(anonymous namespace)::WrapperClass_Invoke (
    object=<optimized out>, method_name=<optimized out>, argv=<optimized out>, 
    argc=<optimized out>, result=<optimized out>)
    at ../../content/renderer/pepper/plugin_object.cc:87
#32 0x000055555d94ce77 in _NPN_Invoke (npp=<optimized out>, 
    npObject=0x6030000816a0, methodName=0x603000081460, 
    arguments=0x6020000613b0, argumentCount=0, result=0x2)
    at ../../third_party/WebKit/Source/bindings/v8/NPV8Object.cpp:217
#33 0x000055555a54992f in content::(anonymous namespace)::MessageChannelInvoke
    (np_obj=<optimized out>, name=0x603000081460, args=0x6020000613b0, 
    arg_count=0, result=0x7fffffff9960)
    at ../../content/renderer/pepper/message_channel.cc:165
#34 0x000055555d9a0941 in WebCore::npObjectInvokeImpl (args=..., 
    functionId=<optimized out>)
---Type <return> to continue, or q <return> to quit---c
    at ../../third_party/WebKit/Source/bindings/v8/V8NPObject.cpp:125
#35 0x000055555ae185c0 in v8::internal::FunctionCallbackArguments::Call (
    this=0x7fffffff9ca0, 
    f=0x55555d9a01e0 <WebCore::npObjectMethodHandler(v8::FunctionCallbackInfo<v8::Value> const&)>) at ../../v8/src/arguments.cc:56
#36 0x000055555a8e0049 in v8::internal::HandleApiCallHelper<false> (
    isolate=0x62c000000200, args=...) at ../../v8/src/builtins.cc:1272
#37 0x000055555a8d38e5 in v8::internal::Builtin_HandleApiCall (
    args_length=<optimized out>, args_object=<optimized out>, 
    isolate=0x62c000000200) at ../../v8/src/builtins.cc:1288

tsepez@chromium.org tried to solve this in https://crbug.com/chromium/139814, but there was a technical difficulty. See comments 42 to 46 in https://crbug.com/chromium/139814.

### ch...@gmail.com (2013-09-05)

I think this is a blink issue rather than a pdf issue.

### jh...@chromium.org (2013-09-05)

@c17: Is there a way to quickly verify that 148567 is the breaking point (e.g. run @ r148566 and ASAN doesn't catch a use-after-free, run @ r148567 and ASAN catches it)?

The report in c16 looks to my untrained eye like Pepper is disposing of something twice. The change (148567) - besides adding a now-removed flag - simply added a new function to the PPB_PDF struct, and the impl. in chrome/renderer/pepper/ppb_pdf_impl.cc, which doesn't give me any obvious ideas on how that would cause a UAF. Of course, I didn't see anything else in the regression range that makes sense.

### in...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### bb...@chromium.org (2013-09-05)

I was able to reproduce this on ToT with repro.html. In Debug mode, a crash is triggered by trying to add a ref to a ref counted object that is in its dtor. That's consistent with a UAF.

Something odd is happening though. I see two URLLoader resources being created, as the PDF plugin prepares to load its document. However, the first URLLoaderResource isn't being destructed properly. Only one of its base class dtors is called. It may be memory corruption but I'll need to debug further to try to see what's going on. Since the dtor that removes the resource from the tracker doesn't run, it doesn't get removed from the live resource list, causing the UAF.

### in...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### bb...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### jh...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### bb...@chromium.org (2013-09-05)

A little more printf debugging reveals that the PluginResource destructor sends the destruct message to the host but never exits. It looks like a hang, but there shouldn't be multiple threads for in-process plugins.

### bb...@chromium.org (2013-09-05)

I think I've tracked this down. It's unique to in-process plugins.

The repro.html file causes a load to start, then a reload, then moves the plugin element when the ready state changes. The instance is torn down while we're in one of the URLLoaderResource dtors, before it has removed itself from the tracker. The resource tracker tries to use the object which is half destructed.

I'll post a simple fix. Note that a PDF change will also be needed, as the repro.html forces it into a state it doesn't like, hitting a NOTREACHED which needs to be changed.

### bb...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### bb...@chromium.org (2013-09-06)

I'm having trouble with the PDF-side fix. The repro page causes it to crash with the PPAPI fix.

### in...@chromium.org (2013-09-06)

Does PPAPI fix fixes the use-after-free and leave like a harmless null crash on pdf side ? If yes, then this bug should be closed with uaf fix and then open a new bug for functional fix.

### bb...@chromium.org (2013-09-06)

I haven't observed a crash in renderer code with the PPAPI fix.

I believe the PDF plugin doesn't handle various URL loader failures well but I'm having difficulty debugging on both Mac and Windows. There are at least two NOTREACHED that are hit that I have observed, but my fixes there don't prevent crashes. It appears somewhat 'racy' as it doesn't always crash.

I'll put the fix up for review.

### bb...@chromium.org (2013-09-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-06)

[Comment Deleted]

### bu...@chromium.org (2013-09-11)

------------------------------------------------------------------------
r222614 | bbudge@chromium.org | 2013-09-11T20:08:06.652285Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/pepper/pepper_in_process_router.cc?r1=222614&r2=222613&pathrev=222614
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/pepper/pepper_in_process_router.h?r1=222614&r2=222613&pathrev=222614

Change the PepperInProcessRouter to defer resource destruction messages.
This changes the in process "proxy" so it posts tasks to send resource destruction messages
instead of calling them directly. This prevents several kinds of reentrancy into the plugin-side
code. In this case, when a URLLoader is released, the plugin can finish before the host cancels
the load and potentially deletes the instance.

BUG=276368

Review URL: https://chromiumcodereview.appspot.com/23688004
------------------------------------------------------------------------

### in...@chromium.org (2013-09-11)

[Empty comment from Monorail migration]

### bb...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### bb...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### bu...@chromium.org (2013-09-12)

------------------------------------------------------------------------
r222786 | bbudge@chromium.org | 2013-09-12T16:02:14.729814Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1599/src/content/renderer/pepper/pepper_in_process_router.cc?r1=222786&r2=222785&pathrev=222786
   M http://src.chromium.org/viewvc/chrome/branches/1599/src/content/renderer/pepper/pepper_in_process_router.h?r1=222786&r2=222785&pathrev=222786

Merge 222614 "Change the PepperInProcessRouter to defer resource..."

> Change the PepperInProcessRouter to defer resource destruction messages.
> This changes the in process "proxy" so it posts tasks to send resource destruction messages
> instead of calling them directly. This prevents several kinds of reentrancy into the plugin-side
> code. In this case, when a URLLoader is released, the plugin can finish before the host cancels
> the load and potentially deletes the instance.
> 
> BUG=276368
> 
> Review URL: https://chromiumcodereview.appspot.com/23688004

TBR=bbudge@chromium.org

Review URL: https://codereview.chromium.org/23536043
------------------------------------------------------------------------

### in...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-12)

ClusterFuzz has detected this issue as fixed in range 222370:222668.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6050852536057856

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x614000046ac8
Crash State:
  - crash stack -
  ppapi::proxy::PluginResource::NotifyInstanceWasDeleted
  ppapi::ResourceTracker::DidDeleteInstance
  - free stack -
  ppapi::Resource::NotifyInstanceWasDeleted
  ppapi::proxy::PluginResource::NotifyInstanceWasDeleted
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=148563:148586
Fixed: https://cluster-fuzz.appspot.com/revisions?range=222370:222668

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97Nl7NrQzYmDTmKFuRhcghyiDZYD_56S_8LPtzaMzO-IWhenLmVDPStMq7w5Ud0nUGB0PeXMv39f7DrIUS48-ktKPPq2t9K4-wstd4haF5dj7CSPX_VKC-JAFmkhGdrI8d26tx3aqnro3qz9c2l9uB3wM4nTw

Additional requirements: Requires HTTP

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

41.w4r10r, what name would you like us to use when we give you credit for this bug in the release notes on the Chrome blog?

### 41...@gmail.com (2013-09-26)

kindly give credites to: 41.w4r10r@garage4hackers.com

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

@chamal: $1000. No obvious control between free / use in ASAN stack.

### ch...@gmail.com (2013-09-28)

Thank you very much for the reward!

### pa...@chromium.org (2013-10-18)

Payment kicked off @chamal for this one and 265221. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/276368?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/276690]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077965)*
