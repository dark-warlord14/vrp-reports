# Security: UAF in ppapi::ScopedPPResource::CallRelease

| Field | Value |
|-------|-------|
| **Issue ID** | [40077358](https://issues.chromium.org/issues/40077358) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Pepper |
| **Reporter** | ch...@gmail.com |
| **Assignee** | bb...@chromium.org |
| **Created** | 2013-04-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

I ran test case I reported in <https://crbug.com/chromium/159429> on chrome and it reproduces again. Attached a slightly simplified test case.

**VERSION**  

Chrome Version: [27.0.1453.15] + [beta]  

[28.0.1467.0 (192547)] + [trunk build]

Operating System: [Ubuntu 12.04 64 bit]

**REPRODUCTION CASE**

1. If you are running this on trunk build copy libpdf.so to out/Release folder
2. Download and copy test.html to local web server.
3. Open chrome.
4. Open test.html.  
   
   Chrome will display sad tab.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State: [ASAN output]

==5084== ERROR: AddressSanitizer: heap-use-after-free on address 0x602a00018100 at pc 0x7f56ea4a244d bp 0x7fff13d27bf0 sp 0x7fff13d27be8  

READ of size 4 at 0x602a00018100 thread T0 (chrome)  

#0 0x7f56ea4a244c in ppapi::ScopedPPResource::CallRelease() out/Release/../../ppapi/shared\_impl/scoped\_pp\_resource.cc:72  

#1 0x7f56ee7bd3da in ~PPB\_URLLoader\_Impl out/Release/../../webkit/plugins/ppapi/ppb\_url\_loader\_impl.cc:95  

#2 0x7f56ee7bd2ad in ~PPB\_URLLoader\_Impl out/Release/../../webkit/plugins/ppapi/ppb\_url\_loader\_impl.cc:88  

#3 0x7f56ea499b9c in ppapi::ResourceTracker::ReleaseResource(int) out/Release/../../ppapi/shared\_impl/resource\_tracker.cc:84  

#4 0x7f56da9e91cc in ?? ??:0  

#5 0x7f56da994623 in ?? ??:0  

#6 0x7f56da999447 in ?? ??:0  

#7 0x7f56da99a1ec in ?? ??:0  

#8 0x7f56da9eefd4 in ?? ??:0  

#9 0x7f56e8910ca1 in webkit::ppapi::(anonymous namespace)::WrapperClass\_Invoke(NPObject\*, void\*, \_NPVariant const\*, unsigned int, \_NPVariant\*) out/Release/../../webkit/plugins/ppapi/plugin\_object.cc:92  

#10 0x7f56eb673e95 in \_NPN\_Invoke out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/NPV8Object.cpp:189  

#11 0x7f56e9c1ed38 in WebKit::WebBindings::invoke(\_NPP\*, NPObject\*, void\*, \_NPVariant const\*, unsigned int, \_NPVariant\*) out/Release/../../third\_party/WebKit/Source/WebKit/chromium/src/WebBindings.cpp:133  

#12 0x7f56e890dece in webkit::ppapi::(anonymous namespace)::MessageChannelInvoke(NPObject\*, void\*, \_NPVariant const\*, unsigned int, \_NPVariant\*) out/Release/../../webkit/plugins/ppapi/message\_channel.cc:209  

#13 0x7f56eb6c9665 in WebCore::npObjectInvokeImpl(v8::Arguments const&, WebCore::InvokeFunctionType) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/V8NPObject.cpp:118  

#14 0x7f56eddcf1a3 in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1327  

#15 0x3878e3a0654d in  

0x602a00018100 is located 320 bytes inside of 328-byte region [0x602a00017fc0,0x602a00018108)  

freed by thread T0 (chrome) here:  

#0 0x7f56e86a7222 in operator delete(void\*) ??:0  

#1 0x7f56ea498bbe in ppapi::Resource::NotifyInstanceWasDeleted() out/Release/../../ppapi/shared\_impl/resource.cc:70  

#2 0x7f56ea49ade3 in ppapi::ResourceTracker::DidDeleteInstance(int) out/Release/../../ppapi/shared\_impl/resource\_tracker.cc:154  

#3 0x7f56e88914f7 in webkit::ppapi::HostGlobals::InstanceDeleted(int) out/Release/../../webkit/plugins/ppapi/host\_globals.cc:251  

#4 0x7f56e88aa0d4 in ~PluginInstance out/Release/../../webkit/plugins/ppapi/ppapi\_plugin\_instance.cc:432  

#5 0x7f56e88a9d1d in ~PluginInstance out/Release/../../webkit/plugins/ppapi/ppapi\_plugin\_instance.cc:402  

#6 0x7f56e9dcc7d7 in scoped\_refptr[webkit::ppapi::PluginInstance](javascript:void(0);)::operator=(webkit::ppapi::PluginInstance\*) out/Release/../../base/memory/ref\_counted.h:267  

#7 0x7f56ee7bb047 in webkit::ppapi::WebPluginImpl::destroy() out/Release/../../webkit/plugins/ppapi/ppapi\_webplugin\_impl.cc:119  

#8 0x7f56e9c6e7be in ~WebPluginContainerImpl out/Release/../../third\_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:629  

#9 0x7f56e9c6e65d in ~WebPluginContainerImpl out/Release/../../third\_party/WebKit/Source/WebKit/chromium/src/WebPluginContainerImpl.cpp:623  

#10 0x7f56eeb74bd3 in WTF::HashTable<WTF::RefPtr[WebCore::Widget](javascript:void(0);), WTF::KeyValuePair<WTF::RefPtr[WebCore::Widget](javascript:void(0);), WebCore::FrameView\*>, WTF::KeyValuePairKeyExtractor<WTF::KeyValuePair<WTF::RefPtr[WebCore::Widget](javascript:void(0);), WebCore::FrameView\*> >, WTF::PtrHash<WTF::RefPtr[WebCore::Widget](javascript:void(0);) >, WTF::KeyValuePairHashTraits<WTF::HashTraits<WTF::RefPtr[WebCore::Widget](javascript:void(0);) >, WTF::HashTraits[WebCore::FrameView\\*](javascript:void(0);) >, WTF::HashTraits<WTF::RefPtr[WebCore::Widget](javascript:void(0);) > >::deallocateTable(WTF::KeyValuePair<WTF::RefPtr[WebCore::Widget](javascript:void(0);), WebCore::FrameView\*>\*, int) out/Release/../../third\_party/WebKit/Source/WTF/wtf/HashTable.h:1089  

#11 0x7f56eeb6ed4b in WebCore::WidgetHierarchyUpdatesSuspensionScope::moveWidgets() out/Release/../../third\_party/WebKit/Source/WebCore/rendering/RenderWidget.cpp:74  

#12 0x7f56ec11e366 in ~WidgetHierarchyUpdatesSuspensionScope out/Release/../../third\_party/WebKit/Source/WebCore/rendering/RenderWidget.h:41  

#13 0x7f56ec118e2f in WebCore::ContainerNode::removeChild(WebCore::Node\*, int&) out/Release/../../third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:527  

#14 0x7f56ec117aa7 in WebCore::collectChildrenAndRemoveFromOldParent(WebCore::Node\*, WTF::Vector<WTF::RefPtr[WebCore::Node](javascript:void(0);), 11ul>&, int&) out/Release/../../third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:88  

#15 0x7f56ec117708 in WebCore::ContainerNode::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, WebCore::AttachBehavior) out/Release/../../third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:664  

#16 0x7f56ec1e8cc8 in WebCore::Node::appendChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);), int&, WebCore::AttachBehavior) out/Release/../../third\_party/WebKit/Source/WebCore/dom/Node.cpp:581  

#17 0x7f56eb6f6675 in WebCore::V8Node::appendChildMethodCustom(v8::Arguments const&) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8NodeCustom.cpp:116  

#18 0x7f56eddcf1a3 in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1327  

#19 0x3878e3a0654d in  

#20 0x3878e3a44bee in  

#21 0x3878e3a0bc73 in  

#22 0x3878e3a25ffd in  

#23 0x3878e3a0c336 in  

#24 0x7f56ede1c3d1 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) out/Release/../../v8/src/execution.cc:118  

#25 0x7f56edd971e2 in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) out/Release/../../v8/src/api.cc:3891  

#26 0x7f56eb6834a7 in WebCore::ScriptController::callFunctionWithInstrumentation(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:236  

#27 0x7f56eb6831c2 in WebCore::ScriptController::callFunction(v8::Handle[v8::Function](javascript:void(0);), v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:189  

#28 0x7f56ebf34632 in WebCore::V8EventListener::callListenerFunction(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Value](javascript:void(0);), WebCore::Event\*) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/V8EventListener.cpp:95  

#29 0x7f56ebcfa256 in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext\*, WebCore::Event\*, v8::Handle[v8::Value](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:142  

previously allocated by thread T0 (chrome) here:  

#0 0x7f56e86a7062 in operator new(unsigned long) ??:0  

#1 0x7f56ee7ca163 in webkit::ppapi::ResourceCreationImpl::CreateURLLoader(int) out/Release/../../webkit/plugins/ppapi/resource\_creation\_impl.cc:242  

#2 0x7f56ea4d4956 in ppapi::thunk::(anonymous namespace)::Create(int) out/Release/../../ppapi/thunk/ppb\_url\_loader\_thunk.cc:24  

#3 0x7f56da9e958d in ?? ??:0  

#4 0x60500000e87f in

## Attachments

- [test.html](attachments/test.html) (text/html; charset=us-ascii, 392 B)

## Timeline

### ke...@chromium.org (2013-04-08)

cevans, do you want to take a look at this? PDF bug...

I have a Windows crash report. That one's not UAF but still looks bad. e3d9ee69f9dee69c

### sc...@gmail.com (2013-04-08)

I doubt very much it's in PDF ;-) It looks like generic WebKit DOM vs. PPAPI URL loading lifetime issue.

### ke...@chromium.org (2013-04-08)

[Empty comment from Monorail migration]

### ch...@gmail.com (2013-04-09)

I get a different backtrace from gdb on a release build without ASAN.


../../third_party/tcmalloc/chromium/src/tcmalloc.cc:286] Attempt to free invalid pointer 0x40 

Program received signal SIGSEGV, Segmentation fault.
0x000055555672e7d0 in tcmalloc::Abort() ()
(gdb) bt
#0  0x000055555672e7d0 in tcmalloc::Abort() ()
#1  0x0000555556735fb2 in tcmalloc::Log(tcmalloc::LogMode, char const*, int, tcmalloc::LogItem, tcmalloc::LogItem, tcmalloc::LogItem, tcmalloc::LogItem) ()
#2  0x000055555672add3 in (anonymous namespace)::InvalidFree(void*) ()
#3  0x0000555558a617bd in webkit::ppapi::PPB_URLLoader_Impl::~PPB_URLLoader_Impl() ()
#4  0x0000555558a61859 in webkit::ppapi::PPB_URLLoader_Impl::~PPB_URLLoader_Impl() ()
#5  0x00007fffec14c82d in ?? ()
   from /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/out/Release/libpdf.so
#6  0x00007fffec0f6d14 in ?? ()
   from /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/out/Release/libpdf.so
#7  0x00007fffec0fb544 in ?? ()
   from /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/out/Release/libpdf.so
#8  0x00007fffec0fc2cd in ?? ()
   from /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/out/Release/libpdf.so
#9  0x00007fffec152605 in ?? ()
   from /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/out/Release/libpdf.so
---Type <return> to continue, or q <return> to quit---c
#10 0x0000555555ddf01e in webkit::ppapi::(anonymous namespace)::WrapperClass_Invoke(NPObject*, void*, _NPVariant const*, unsigned int, _NPVariant*) ()
#11 0x000055555726c8bf in _NPN_Invoke ()
#12 0x0000555555ddcd60 in webkit::ppapi::(anonymous namespace)::MessageChannelInvoke(NPObject*, void*, _NPVariant const*, unsigned int, _NPVariant*) ()
#13 0x0000555557291d47 in WebCore::npObjectInvokeImpl(v8::Arguments const&, WebCore::InvokeFunctionType) ()
#14 0x0000555557291e9e in WebCore::npObjectMethodHandler(v8::Arguments const&)
    ()
#15 0x00005555585a8c96 in v8::internal::Builtin_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) ()

### ch...@gmail.com (2013-04-16)

1. PPB_URLLoader_Impl(ppb_url_loader_impl.h) is a subclass of ppapi::Resource(ppapi/shared_impl/resource.h). 
2. But for some strange reason destructor of ppapi::Resource is not executed when destructor of PPB_URLLoader_Impl is executed.
3. Think that is why this bug happens. 
Because destructor of ppapi::Resource should be executed to remove PPB_URLLoader_Impl instance from ResourceMap live_resources_ of ResourceTracker(ppapi/shared_impl/resource_tracker.cc).
4. Otherwise PPB_URLLoader_Impl isntance will remain in ResourceMap live_resources_ of ResourceTracker even after being deleted.

Any idea why destructor of ppapi::Resource is not executed when it's subclass PPB_URLLoader_Impl is deleted?

### [Deleted User] (2013-04-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-04-18)

Tom, Trung, Carlos, any idea on c#5 ?

### ch...@gmail.com (2013-04-22)

About https://crbug.com/chromium/227350#c5 - Destructor of PPB_URLLoader_Impl gets called again before the first call to destructor finish executing. The second call happens before the parent class ppapi::Resource's destructor is called.

### in...@chromium.org (2013-04-22)

Chamal, you seem to have understood the problem ? Want a take a shot at uploading a fix and get higher reward :)

### ch...@gmail.com (2013-04-23)

[Comment Deleted]

### ch...@gmail.com (2013-04-23)

Managed to create a fix and submit a patch. but it is a hacky fix. Please check whether it is ok.
https://codereview.chromium.org/13856014

Even though this fix fixes this use after free, we need to find a solution to the problem of ready state event being fired when loader objects are cancelled. All these issues 139814,159429,177620,176882 and 227350 happen because of it. Maybe we have to consider adding ready state event to a event queue and fire it bit later if it does not violate any specifications. I tried to find a fix to this ready state event issue but it is bit hard for me because I don't know much about that area.

### cp...@chromium.org (2013-04-23)

Adding Bill.

### in...@chromium.org (2013-04-23)

[Empty comment from Monorail migration]

### bb...@chromium.org (2013-04-23)

[Empty comment from Monorail migration]

### bb...@chromium.org (2013-04-25)

Brett, this is another reentrancy crash in URLLoader. I noticed you reviewed tsepez;s fixes to this a while ago:
https://chromiumcodereview.appspot.com/11359222

Patchset #2 looks like the fix being proposed for this issue, but you mentioned that the URLLoader refactoring would solve this problem. I know that your refactoring CL got stalled on main document loading issues. How hard would it be to revive that CL and fix it? Would it be better to hack this for now?


### br...@chromium.org (2013-04-25)

The thing that stopped my URLLoader patch from landing was handle document load for nacl. Otherwise the patch should still be good. It could probably be picked up by somebody and fixed up in a couple of days.

### bb...@chromium.org (2013-04-28)

I'm working on it:
https://codereview.chromium.org/14371021/

We'll see if it helps here.

### in...@chromium.org (2013-04-28)

[Empty comment from Monorail migration]

### vi...@chromium.org (2013-04-30)

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

### bb...@chromium.org (2013-05-01)

test.html no longer crashes the renderer.

### in...@chromium.org (2013-05-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-03)

@chamal: thanks for your continuing excellent work!
Happy to reward you $1000 for this case.

### ch...@gmail.com (2013-05-03)

Thank you very much for the reward!

### sc...@gmail.com (2013-05-06)

M27 is https://src.chromium.org/viewvc/chrome?view=rev&revision=198490

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

### sc...@gmail.com (2013-05-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


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

This issue was migrated from crbug.com/chromium/227350?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077358)*
