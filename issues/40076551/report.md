# Security: Use after free on ~AssociatedURLLoader with pdf plugin

| Field | Value |
|-------|-------|
| **Issue ID** | [40076551](https://issues.chromium.org/issues/40076551) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals, Internals>Plugins>PDF |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2012-11-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

I think this is the same issue as 139814. It is possible to fire dom ready state event when plugin is destroyed.

**VERSION**  

Chrome Version: [ 22.0.1229.94] + [stable]  

[24.0.1312.2] + [dev]  

[25.0.1316.0 (165849)] + [trunk build]  

Operating System: [Ubuntu 12.04 64 bit]

**REPRODUCTION CASE**

1. Open attached repro.html with chrome.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State: [Address sanitizer output]  

==5595== ERROR: AddressSanitizer heap-use-after-free on address 0x7f3aa79d9270 at pc 0x7f3aba7bee43 bp 0x7fff8d02e7f0 sp 0x7fff8d02e7e8  

READ of size 8 at 0x7f3aa79d9270 thread T0  

#0 0x7f3aba7bee42 in ~RefPtr third\_party/WebKit/Source/WTF/wtf/RefPtr.h:56  

#1 0x7f3aba7beb1d in ~AssociatedURLLoader third\_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:302  

#2 0x7f3ac152bfcb in ~scoped\_ptr ./base/memory/scoped\_ptr.h:163  

#3 0x7f3ac152bc9d in ~PPB\_URLLoader\_Impl webkit/plugins/ppapi/ppb\_url\_loader\_impl.cc:87  

#4 0x7f3aba6e70b8 in base::RefCounted[ppapi::Resource](javascript:void(0);)::Release() const ./base/memory/ref\_counted.h:92  

#5 0x7f3aaa6561ac in ?? ??:0  

#6 0x7f3a000000d1  

0x7f3aa79d9270 is located 48 bytes inside of 56-byte region [0x7f3aa79d9240,0x7f3aa79d9278)  

freed by thread T0 here:  

#0 0x7f3ac1c52e70 in operator delete(void\*) ??:0  

#1 0x7f3ac152c107 in scoped\_ptr[WebKit::WebURLLoader](javascript:void(0);)::reset(WebKit::WebURLLoader\*) ./base/memory/scoped\_ptr.h:186  

#2 0x7f3aba6e8b2d in ppapi::ResourceTracker::DidDeleteInstance(int) ppapi/shared\_impl/resource\_tracker.cc:144  

#3 0x7f3abe0ac3e6 in webkit::ppapi::HostGlobals::InstanceDeleted(int) webkit/plugins/ppapi/host\_globals.cc:242  

#4 0x7f3abe0bd11e in ~PluginInstance webkit/plugins/ppapi/ppapi\_plugin\_instance.cc:653  

#5 0x7f3abe0bcabd in ~PluginInstance webkit/plugins/ppapi/ppapi\_plugin\_instance.cc:628  

#6 0x7f3ac15264bf in base::RefCounted[webkit::ppapi::PluginInstance](javascript:void(0);)::Release() const ./base/memory/ref\_counted.h:92  

#7 0x7f3aba767eb2 in ~WebPluginContainerImpl third\_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:661  

#8 0x7f3aba767bdd in ~WebPluginContainerImpl third\_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:648  

#9 0x7f3abd216048 in WTF::RefCounted[WebCore::Widget](javascript:void(0);)::deref() third\_party/WebKit/Source/WTF/wtf/RefCounted.h:202  

#10 0x7f3aba8f0c88 in ~WidgetHierarchyUpdatesSuspensionScope third\_party/WebKit/Source/WebCore/rendering/RenderWidget.h:41  

#11 0x7f3aba8ec0de in WebCore::collectChildrenAndRemoveFromOldParent(WebCore::Node\*, WTF::Vector<WTF::RefPtr[WebCore::Node](javascript:void(0);), 11ul>&, int&) third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:92  

#12 0x7f3aba8eb561 in WebCore::ContainerNode::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, bool) third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:570  

#13 0x7f3aba9ed5ff in WebCore::Node::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, bool) third\_party/WebKit/Source/WebCore/dom/Node.cpp:630  

#14 0x7f3abc0724d7 in WebCore::V8Node::appendChildCallback(v8::Arguments const&) third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:120  

previously allocated by thread T0 here:  

#0 0x7f3ac1c52cf0 in operator new(unsigned long) ??:0  

#1 0x7f3aba72bb7c in WebKit::WebFrameImpl::createAssociatedURLLoader(WebKit::WebURLLoaderOptions const&) third\_party/WebKit/Source/WebKit/chromium/src/WebFrameImpl.cpp:1120  

#2 0x7f3ac152d7b5 in webkit::ppapi::PPB\_URLLoader\_Impl::Open(ppapi::URLRequestInfoData const&, int, scoped\_refptr[ppapi::TrackedCallback](javascript:void(0);)) webkit/plugins/ppapi/ppb\_url\_loader\_impl.cc:175  

#3 0x7f3ac152c554 in webkit::ppapi::PPB\_URLLoader\_Impl::Open(int, scoped\_refptr[ppapi::TrackedCallback](javascript:void(0);)) webkit/plugins/ppapi/ppb\_url\_loader\_impl.cc:109  

#4 0x7f3ac0f7088d in ppapi::thunk::(anonymous namespace)::Open(int, int, PP\_CompletionCallback) ppapi/thunk/ppb\_url\_loader\_thunk.cc:38  

#5 0x7f3aaa656709 in ?? ??:0

## Attachments

- [repro.html](attachments/repro.html) (text/html; charset=us-ascii, 490 B)

## Timeline

### ch...@gmail.com (2012-11-05)

If you are testing on trunk build please copy libpdf.so plugin to src/out/Release folder.

### sc...@gmail.com (2012-11-05)

Tom, you're probably ideal to triage this and take it on?

### ts...@chromium.org (2012-11-05)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-11-09)

[Empty comment from Monorail migration]

### ts...@chromium.org (2012-11-14)

~AssociatedURLLoader is being called on top of itself.  It's hard to see the path because of the inability to backtrace through JS, but the ASAN trace at time of free is actually on top of the still-executing call that generates the UAF when control returns to it.


### ts...@chromium.org (2012-11-14)

Putting it all together, here's a composite stack trace of what's really happening:

#0  WebKit::AssociatedURLLoader::~AssociatedURLLoader (this=0x7f0d9a290d80, 
    __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:304
#1  0x00007f0dac0c9680 in scoped_ptr<WebKit::WebURLLoader>::reset (
    this=0x7f0da8894370, p=0x0) at ./base/memory/scoped_ptr.h:186
#2  0x00007f0dadb77e3d in webkit::ppapi::PPB_URLLoader_Impl::InstanceWasDeleted
    (this=0x7f0da88942c0) at webkit/plugins/ppapi/ppb_url_loader_impl.cc:98
#3  0x00007f0daa71ba26 in ppapi::ResourceTracker::DidDeleteInstance (
    this=0x7f0da8881710, instance=-1749972023)
    at ppapi/shared_impl/resource_tracker.cc:144
#4  0x00007f0dac08820a in webkit::ppapi::HostGlobals::InstanceDeleted (
    this=0x7f0da8881700, instance=-1749972023)
    at webkit/plugins/ppapi/host_globals.cc:242
#5  0x00007f0dac097fd4 in webkit::ppapi::PluginInstance::~PluginInstance (
    this=0x7f0d9a743000, __in_chrg=<optimized out>)
    at webkit/plugins/ppapi/ppapi_plugin_instance.cc:653
#6  0x00007f0dac09832a in webkit::ppapi::PluginInstance::~PluginInstance (
    this=0x7f0d9a743000, __in_chrg=<optimized out>)
    at webkit/plugins/ppapi/ppapi_plugin_instance.cc:654
#7  0x00007f0dac0a770c in base::RefCounted<webkit::ppapi::PluginInstance>::Release (this=0x7f0d9a743008) at ./base/memory/ref_counted.h:92
#8  0x00007f0dadb767de in scoped_refptr<webkit::ppapi::PluginInstance>::operator= (this=0x7f0d9a222738, p=0x0) at ./base/memory/ref_counted.h:277
#9  0x00007f0dadb7598a in webkit::ppapi::WebPluginImpl::destroy (
    this=0x7f0d9a222720) at webkit/plugins/ppapi/ppapi_webplugin_impl.cc:119
#10 0x00007f0daa76caef in WebKit::WebPluginContainerImpl::~WebPluginContainerImpl (this=0x7f0d9a4a16c0, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:661
#11 0x00007f0daa76cb84 in WebKit::WebPluginContainerImpl::~WebPluginContainerImpl (this=0x7f0d9a4a16c0, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:662
#12 0x00007f0daa76fb5a in WTF::RefCounted<WebCore::Widget>::deref (
    this=0x7f0d9a4a16c8) at third_party/WebKit/Source/WTF/wtf/RefCounted.h:202
#13 0x00007f0dab01643f in WTF::derefIfNotNull<WebCore::Widget> (
    ptr=0x7f0d9a4a16c0) at third_party/WebKit/Source/WTF/wtf/PassRefPtr.h:53
#14 0x00007f0dab01635d in WTF::RefPtr<WebCore::Widget>::~RefPtr (
    this=0x7f0d9ac95400, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WTF/wtf/RefPtr.h:56
#15 0x00007f0dabb76622 in WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>::~KeyValuePair (this=0x7f0d9ac95400, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WTF/wtf/HashTraits.h:190
#16 0x00007f0dabb765eb in WTF::HashTable<WTF::RefPtr<WebCore::Widget>, WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*> >, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::KeyValuePairHashTraits<WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> > >::deallocateTable (
    table=0x7f0d9ac953f0, size=8)
    at third_party/WebKit/Source/WTF/wtf/HashTable.h:1089
#17 0x00007f0dabb75bc0 in WTF::HashTable<WTF::RefPtr<WebCore::Widget>, WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*> >, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::KeyValuePairHashTraits<WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> > >::~HashTable (
    this=0x7fffa705b890, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WTF/wtf/HashTable.h:371
#18 0x00007f0dabb75882 in WTF::HashMap<WTF::RefPtr<WebCore::Widget>, WebCore::FrameView*, WTF::PtrHash<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WTF::RefPtr<WebCore::Widget> >, WTF::HashTraits<WebCore::FrameView*> >::~HashMap (
    this=0x7fffa705b890, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WTF/wtf/RefPtrHashMap.h:32
#19 0x00007f0dabb739f3 in WebCore::WidgetHierarchyUpdatesSuspensionScope::moveWidgets (this=0x7fffa705b9df)
    at third_party/WebKit/Source/WebCore/rendering/RenderWidget.cpp:73
#20 0x00007f0daa84c3b6 in WebCore::WidgetHierarchyUpdatesSuspensionScope::~WidgetHierarchyUpdatesSuspensionScope (this=0x7fffa705b9df, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WebCore/rendering/RenderWidget.h:41
#21 0x00007f0daa847b69 in WebCore::ContainerNode::removeChild (
    this=0x7f0d9a478a80, oldChild=0x7f0d9a733c30, ec=@0x7fffa705bbf8: 0)
    at third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:436
#22 0x00007f0daa846341 in WebCore::collectChildrenAndRemoveFromOldParent (
    node=0x7f0d9a733c30, nodes=..., ec=@0x7fffa705bbf8: 0)
    at third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:92
#23 0x00007f0daa84838b in WebCore::ContainerNode::appendChild (
    this=0x7f0d9a478a80, newChild=..., ec=@0x7fffa705bbf8: 0, 
    shouldLazyAttach=true)
    at third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:570
#24 0x00007f0daa8f9fbf in WebCore::Node::appendChild (this=0x7f0d9a478a80, 
    newChild=..., ec=@0x7fffa705bbf8: 0, shouldLazyAttach=true)
    at third_party/WebKit/Source/WebCore/dom/Node.cpp:613
#25 0x00007f0dab3999df in WebCore::V8Node::appendChildCallback (args=...)
    at third_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:120
#26 0x00007f0daabb0cf0 in v8::internal::HandleApiCallHelper<false> (args=..., 
    isolate=0x7f0da885a000) at v8/src/builtins.cc:1146
#27 0x00007f0daababa2e in v8::internal::Builtin_Impl_HandleApiCall (args=..., 
    isolate=0x7f0da885a000) at v8/src/builtins.cc:1164
#28 0x00007f0daabab9ff in v8::internal::Builtin_HandleApiCall (args=..., 
    isolate=0x7f0da885a000) at v8/src/builtins.cc:1163

... JS frames omitted ...

#0  v8::Function::Call (this=0x7f0da89450f0, recv=..., argc=1, 
    argv=0x7fffa705c390) at v8/src/api.cc:3654
#1  0x00007f0dab33f5e6 in WebCore::ScriptController::callFunctionWithInstrumentation (context=0x7f0d9ae69180, function=..., receiver=..., argc=1, 
    args=0x7fffa705c390)
    at third_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:231
#2  0x00007f0dab33f1f8 in WebCore::ScriptController::callFunction (
    this=0x7f0da88c1280, function=..., receiver=..., argc=1, 
    args=0x7fffa705c390)
    at third_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:184
#3  0x00007f0dab36d3b1 in WebCore::V8EventListener::callListenerFunction (
    this=0x7f0d9a2225a0, context=0x7f0d9ae69180, jsEvent=..., event=
    0x7f0d9a293460)
    at third_party/WebKit/Source/WebCore/bindings/v8/V8EventListener.cpp:95
#4  0x00007f0dab832058 in WebCore::V8AbstractEventListener::invokeEventHandler (
    this=0x7f0d9a2225a0, context=0x7f0d9ae69180, event=0x7f0d9a293460, 
    jsEvent=...)
    at third_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:142
#5  0x00007f0dab831dc7 in WebCore::V8AbstractEventListener::handleEvent (
    this=0x7f0d9a2225a0, context=0x7f0d9ae69180, event=0x7f0d9a293460)
    at third_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:102
#6  0x00007f0daa8dfda2 in WebCore::EventTarget::fireEventListeners (
    this=0x7f0d9ae69000, event=0x7f0d9a293460, d=0x7f0d9a69e780, entry=...)
    at third_party/WebKit/Source/WebCore/dom/EventTarget.cpp:210
#7  0x00007f0daa8dfb62 in WebCore::EventTarget::fireEventListeners (
    this=0x7f0d9ae69000, event=0x7f0d9a293460)
    at third_party/WebKit/Source/WebCore/dom/EventTarget.cpp:175
#8  0x00007f0daa90110a in WebCore::Node::handleLocalEvents (
    this=0x7f0d9ae69000, event=0x7f0d9a293460)
    at third_party/WebKit/Source/WebCore/dom/Node.cpp:2547
#9  0x00007f0daa988b09 in WebCore::EventContext::handleLocalEvents (
    this=0x7f0d9ad4ad80, event=0x7f0d9a293460)
    at third_party/WebKit/Source/WebCore/dom/EventContext.cpp:54
#10 0x00007f0daa979691 in WebCore::EventDispatcher::dispatchEventAtTarget (
    this=0x7fffa705c890, event=...)
    at third_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:304
#11 0x00007f0daa9789bf in WebCore::EventDispatcher::dispatchEvent (
    this=0x7fffa705c890, prpEvent=...)
    at third_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:257
#12 0x00007f0daa977028 in WebCore::EventDispatchMediator::dispatchEvent (
    this=0x7f0d9a290e40, dispatcher=0x7fffa705c890)
    at third_party/WebKit/Source/WebCore/dom/EventDispatchMediator.cpp:52
#13 0x00007f0daa977adc in WebCore::EventDispatcher::dispatchEvent (
    node=0x7f0d9ae69000, mediator=...)
    at third_party/WebKit/Source/WebCore/dom/EventDispatcher.cpp:127
#14 0x00007f0daa901204 in WebCore::Node::dispatchEvent (this=0x7f0d9ae69000, 
    event=...) at third_party/WebKit/Source/WebCore/dom/Node.cpp:2562
#15 0x00007f0daa85ee6c in WebCore::Document::setReadyState (
    this=0x7f0d9ae69000, readyState=WebCore::Document::Complete)
    at third_party/WebKit/Source/WebCore/dom/Document.cpp:1226
#16 0x00007f0dab632019 in WebCore::FrameLoader::checkCompleted (
    this=0x7f0da88c0c98)
    at third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:770
#17 0x00007f0dab631e22 in WebCore::FrameLoader::loadDone (this=0x7f0da88c0c98)
    at third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:719
#18 0x00007f0dab68c22c in WebCore::CachedResourceLoader::loadDone (
    this=0x7f0d9aca6d80)
    at third_party/WebKit/Source/WebCore/loader/cache/CachedResourceLoader.cpp:701
#19 0x00007f0dab66750e in WebCore::SubresourceLoader::releaseResources (
    this=0x7f0d9a546000)
    at third_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:318
#20 0x00007f0dab66219b in WebCore::ResourceLoader::cancel (this=0x7f0d9a546000, 
    error=...)
    at third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:407
#21 0x00007f0dab661f4b in WebCore::ResourceLoader::cancel (this=0x7f0d9a546000)
    at third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:356
#22 0x00007f0dab66611b in WebCore::SubresourceLoader::cancelIfNotFinishing (
    this=0x7f0d9a546000)
    at third_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:99
#23 0x00007f0dab67c163 in WebCore::CachedRawResource::allClientsRemoved (
    this=0x7f0d9acf5e00)
    at third_party/WebKit/Source/WebCore/loader/cache/CachedRawResource.cpp:96
#24 0x00007f0dab67f392 in WebCore::CachedResource::removeClient (
    this=0x7f0d9acf5e00, client=0x7f0d9a56eec8)
    at third_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:513
#25 0x00007f0dab622859 in WebCore::DocumentThreadableLoader::clearResource (
    this=0x7f0d9a56eea0)
    at third_party/WebKit/Source/WebCore/loader/DocumentThreadableLoader.cpp:177
#26 0x00007f0dab622775 in WebCore::DocumentThreadableLoader::cancel (
    this=0x7f0d9a56eea0)
    at third_party/WebKit/Source/WebCore/loader/DocumentThreadableLoader.cpp:159
#27 0x00007f0daa79d98d in WebKit::AssociatedURLLoader::cancel (
    this=0x7f0d9a290d80)
    at third_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:364
#28 0x00007f0daa79d388 in WebKit::AssociatedURLLoader::~AssociatedURLLoader (
    this=0x7f0d9a290d80, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:303
#29 0x00007f0daa79d3f6 in WebKit::AssociatedURLLoader::~AssociatedURLLoader (
    this=0x7f0d9a290d80, __in_chrg=<optimized out>)
    at third_party/WebKit/Source/WebKit/chromium/src/AssociatedURLLoader.cpp:304
#30 0x00007f0dac0c95e5 in scoped_ptr<WebKit::WebURLLoader>::~scoped_ptr (
    this=0x7f0da8894370, __in_chrg=<optimized out>)
    at ./base/memory/scoped_ptr.h:163
#31 0x00007f0dadb77d5a in webkit::ppapi::PPB_URLLoader_Impl::~PPB_URLLoader_Impl
    (this=0x7f0da88942c0, __in_chrg=<optimized out>)
    at webkit/plugins/ppapi/ppb_url_loader_impl.cc:88
#32 0x00007f0dadb77dee in webkit::ppapi::PPB_URLLoader_Impl::~PPB_URLLoader_Impl
    (this=0x7f0da88942c0, __in_chrg=<optimized out>)
    at webkit/plugins/ppapi/ppb_url_loader_impl.cc:90
#33 0x00007f0da9b0df9e in base::RefCounted<ppapi::Resource>::Release (
    this=0x7f0da88942c8) at ./base/memory/ref_counted.h:92
#34 0x00007f0daa71b3d3 in ppapi::ResourceTracker::ReleaseResource (
    this=0x7f0da8881710, res=190) at ppapi/shared_impl/resource_tracker.cc:74
#35 0x00007f0dac08fcb5 in webkit::ppapi::(anonymous namespace)::ReleaseResource
    (resource=190) at webkit/plugins/ppapi/plugin_module.cc:163
#36 0x00007f0d9c150bdd in ?? ()
   from /usr/local/google/tsepez/c2/src/out/Debug/libpdf.so
#37 0x00007f0d9c0fcbf4 in ?? ()
   from /usr/local/google/tsepez/c2/src/out/Debug/libpdf.so
#38 0x00007f0d9c101e78 in ?? ()
   from /usr/local/google/tsepez/c2/src/out/Debug/libpdf.so
#39 0x00007f0d9c102c1d in ?? ()
   from /usr/local/google/tsepez/c2/src/out/Debug/libpdf.so
#40 0x00007f0d9c156935 in ?? ()
   from /usr/local/google/tsepez/c2/src/out/Debug/libpdf.so
#41 0x00007f0dac0f0aef in webkit::ppapi::(anonymous namespace)::WrapperClass_Invoke (object=0x7f0d9a21e320, method_name=0x7f0d9a21e340, argv=0x7f0d9a250bf0, 
    argc=0, result=0x7fffa705db20) at webkit/plugins/ppapi/plugin_object.cc:92
#42 0x00007f0dab3344c2 in _NPN_Invoke (npp=0x0, npObject=0x7f0d9a21e320, 
    methodName=0x7f0d9a21e340, arguments=0x7f0d9a250bf0, argumentCount=0, 
    result=0x7fffa705db20)
    at third_party/WebKit/Source/WebCore/bindings/v8/NPV8Object.cpp:182
#43 0x00007f0daa73a95d in WebKit::WebBindings::invoke (npp=0x0, 
    object=0x7f0d9a21e320, method=0x7f0d9a21e340, args=0x7f0d9a250bf0, 
    argCount=0, result=0x7fffa705db20)
    at third_party/WebKit/Source/WebKit/chromium/src/WebBindings.cpp:139
#44 0x00007f0dac0edcbe in webkit::ppapi::(anonymous namespace)::MessageChannelInvoke (np_obj=0x7f0d9a6734b0, name=0x7f0d9a21e340, args=0x7f0d9a250bf0, 
    arg_count=0, result=0x7fffa705db20)
    at webkit/plugins/ppapi/message_channel.cc:209
#45 0x00007f0dab3743ae in WebCore::npObjectInvokeImpl (args=..., 
    functionId=WebCore::InvokeMethod)
    at third_party/WebKit/Source/WebCore/bindings/v8/V8NPObject.cpp:118
#46 0x00007f0dab374539 in WebCore::npObjectMethodHandler (args=...)
    at third_party/WebKit/Source/WebCore/bindings/v8/V8NPObject.cpp:151
#47 0x00007f0daabb0cf0 in v8::internal::HandleApiCallHelper<false> (args=..., 
    isolate=0x7f0da885a000) at v8/src/builtins.cc:1146
#48 0x00007f0daababa2e in v8::internal::Builtin_Impl_HandleApiCall (args=..., 
    isolate=0x7f0da885a000) at v8/src/builtins.cc:1164
#49 0x00007f0daabab9ff in v8::internal::Builtin_HandleApiCall (args=..., 
    isolate=0x7f0da885a000) at v8/src/builtins.cc:1163

... JS frames omitted ...


### ts...@chromium.org (2012-11-14)

[Empty comment from Monorail migration]

### ts...@chromium.org (2012-11-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-11-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=168150

------------------------------------------------------------------------
r168150 | tsepez@chromium.org | 2012-11-16T07:35:55.599869Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/plugins/ppapi/ppb_url_loader_impl.cc?r1=168150&r2=168149&pathrev=168150

Break path whereby AssociatedURLLoader::~AssociatedURLLoader() is re-entered on top of itself.

BUG=159429

Review URL: https://chromiumcodereview.appspot.com/11359222
------------------------------------------------------------------------

### in...@chromium.org (2012-11-16)

[Empty comment from Monorail migration]

### ch...@gmail.com (2012-11-17)

Is this issue eligible for reward?

### in...@chromium.org (2012-11-17)

Chamal, yes this will go the reward panel for discussion. Please don't worry if the tag does not get added, we do review fixed bugs from time to time.

### ch...@gmail.com (2012-11-18)

Now I get a null pointer exception when I run the reproduction case (repro.html) on Ubuntu linux 12.04.

Address Sanitizer output
------------------------
==6950== ERROR: AddressSanitizer: SEGV on unknown address 0x000000000010 (pc 0x7f83d919be84 sp 0x7fffc9789b20 bp 0x7f83d1cf7948 T0)
AddressSanitizer can not provide additional info.
    #0 0x7f83d919be83 (/lib/x86_64-linux-gnu/libpthread-2.15.so+0x9e83)

### ts...@chromium.org (2012-11-19)

Hmm.  Debug build and non-ASAN prod builds don't trip over the NULL deref, which is strange because it doesn't take ASAN magic to find NULL derefs. The crash is coming out of libpdf.so itself:

#0  __pthread_mutex_lock (mutex=0x40) at pthread_mutex_lock.c:50
#1  0x00007f12e751ec51 in ?? ()
   from /usr/local/google/tsepez/c2/src/out/Release/libpdf.so
#2  0x00007f12e7523e78 in ?? ()
   from /usr/local/google/tsepez/c2/src/out/Release/libpdf.so
#3  0x00007f12e7524c1d in ?? ()
   from /usr/local/google/tsepez/c2/src/out/Release/libpdf.so
#4  0x00007f12e7578935 in ?? ()
   from /usr/local/google/tsepez/c2/src/out/Release/libpdf.so
#5  0x00007f12f9c20c0d in webkit::ppapi::(anonymous namespace)::WrapperClass_Invoke (object=<optimized out>, method_name=<optimized out>, argv=0x7f12e7578860, 
    argc=0, result=<optimized out>) at webkit/plugins/ppapi/plugin_object.cc:92
#6  0x00007f12f8807ed7 in _NPN_Invoke (npp=0x0, npObject=<optimized out>, 
    methodName=0x38, arguments=<optimized out>, argumentCount=251, 
    result=0x7fffb1e1ffc0)
    at third_party/WebKit/Source/WebCore/bindings/v8/NPV8Object.cpp:183
#7  0x00007f12f781ff29 in WebKit::WebBindings::invoke (npp=0x0, object=0x10, 
    method=0x40, args=0xfb, argCount=64, result=0x38)
    at third_party/WebKit/Source/WebKit/chromium/src/WebBindings.cpp:139
#8  0x00007f12f9c1dc57 in webkit::ppapi::(anonymous namespace)::MessageChannelInvoke (np_obj=<optimized out>, name=0x7f12e25e9c40, args=0x7f12e25eac40, 
    arg_count=0, result=0x7fffb1e1ffc0)
    at webkit/plugins/ppapi/message_channel.cc:208
#9  0x00007f12f8868ebb in WebCore::npObjectInvokeImpl (args=..., 
    functionId=<optimized out>)
    at third_party/WebKit/Source/WebCore/bindings/v8/V8NPObject.cpp:117
#10 0x00007f12f7e352c3 in v8::internal::HandleApiCallHelper<false> (
    isolate=<optimized out>, args=...) at v8/src/builtins.cc:1164
... JS Frames follow ...

I'll file a follow up non-security bug and assign it to @cevans who understands pdfs.


### sc...@gmail.com (2012-11-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-11-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=170562

------------------------------------------------------------------------
r170562 | cevans@chromium.org | 2012-11-30T21:56:44.472730Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/webkit/plugins/ppapi/ppb_url_loader_impl.cc?r1=170562&r2=170561&pathrev=170562

Merge 168150 - Break path whereby AssociatedURLLoader::~AssociatedURLLoader() is re-entered on top of itself.

BUG=159429

Review URL: https://chromiumcodereview.appspot.com/11359222

TBR=tsepez@chromium.org
Review URL: https://codereview.chromium.org/11411296
------------------------------------------------------------------------

### bu...@chromium.org (2012-11-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=170563

------------------------------------------------------------------------
r170563 | cevans@chromium.org | 2012-11-30T21:57:13.393294Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1312/src/webkit/plugins/ppapi/ppb_url_loader_impl.cc?r1=170563&r2=170562&pathrev=170563

Merge 168150 - Break path whereby AssociatedURLLoader::~AssociatedURLLoader() is re-entered on top of itself.

BUG=159429

Review URL: https://chromiumcodereview.appspot.com/11359222

TBR=tsepez@chromium.org
Review URL: https://codereview.chromium.org/11411297
------------------------------------------------------------------------

### sc...@gmail.com (2012-12-04)

Thank you Chamal! $1000

### ch...@gmail.com (2012-12-04)

Thank you very much for the reward :)

### sc...@gmail.com (2012-12-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-14)

Payment in system as part of $2500 batch.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-02-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bb...@chromium.org (2013-04-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-05-01)

------------------------------------------------------------------------
r197686 | bbudge@chromium.org | 2013-05-01T19:23:34.180965Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/ppapi/shared_impl/resource.cc?r1=197686&r2=197685&pathrev=197686
   M http://src.chromium.org/viewvc/chrome/trunk/src/ppapi/shared_impl/resource.h?r1=197686&r2=197685&pathrev=197686
   M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/plugins/ppapi/ppb_url_loader_impl.cc?r1=197686&r2=197685&pathrev=197686

Remove Pepper URLLoader from resource tracker early.
This protects against double delete if the instance is destroyed
as a result of canceling a load.

BUG=159429,227350

Review URL: https://chromiumcodereview.appspot.com/14695002
------------------------------------------------------------------------

### bu...@chromium.org (2013-05-06)

------------------------------------------------------------------------
r198490 | cevans@chromium.org | 2013-05-06T18:45:56.280960Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1453/src/ppapi/shared_impl/resource.cc?r1=198490&r2=198489&pathrev=198490
   M http://src.chromium.org/viewvc/chrome/branches/1453/src/ppapi/shared_impl/resource.h?r1=198490&r2=198489&pathrev=198490
   M http://src.chromium.org/viewvc/chrome/branches/1453/src/webkit/plugins/ppapi/ppb_url_loader_impl.cc?r1=198490&r2=198489&pathrev=198490

Merge 197686 "Remove Pepper URLLoader from resource tracker early."

> Remove Pepper URLLoader from resource tracker early.
> This protects against double delete if the instance is destroyed
> as a result of canceling a load.
> 
> BUG=159429,227350
> 
> Review URL: https://chromiumcodereview.appspot.com/14695002

TBR=bbudge@chromium.org

Review URL: https://codereview.chromium.org/14869007
------------------------------------------------------------------------

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/159429?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals, Internals>Plugins>PDF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076551)*
