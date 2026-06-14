# Security: use-after-free removing a frame from its parent in a beforeload event of an OBJECT element

| Field | Value |
|-------|-------|
| **Issue ID** | [40077343](https://issues.chromium.org/issues/40077343) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | cy...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2013-04-04 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Render process security vulnerability:

A RenderArena use-after-free happens when removing the current frame from its parent in a beforeload event attached to an OBJECT element (child of current frame body).

Spraying some data with JS allows a full control of eax, then a call \*724(%eax) happens (Chrome dev offset).

Forging a complete vtable is of course possible (with some info leak) and would allow a control of the PC.

**VERSION**  

Verified on Google Chrome 26.0.1410.43 (stable)  

Debugged on Chromium 28.0.1461.0 (191833) (dev), Release build with symbols (GYP\_GENERATORS=ninja GYP\_DEFINES='component=shared\_library mac\_strip\_release=0')

Operating System: OSX 10.8.2

**REPRODUCTION CASE**  

Open the attached object-beforeload-chrome.html to reproduce the bug.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash:  

Rendering process (sad tab)  

Crash State:  

See the lldb trace (js comment) in the attached object-beforeload-chrome.html  

Client ID (if relevant):  

Crash Report file name: 4170E48A-E664-4A80-8E8C-D91A3009E3EA.dmp  

Client ID: F909B5C0-6752-4793-F6A5-5853E12D44A6

## Attachments

- [object-beforeload-frame-chrome.html](attachments/object-beforeload-frame-chrome.html) (text/html; charset=us-ascii, 535 B)
- [object-beforeload-chrome.html](attachments/object-beforeload-chrome.html) (text/html; charset=us-ascii, 2.8 KB)
- [pbject-beforeload-crash.html](attachments/pbject-beforeload-crash.html) (text/html; charset=us-ascii, 523 B)
- [object-beforeload-crash-main.html](attachments/object-beforeload-crash-main.html) (text/html; charset=us-ascii, 329 B)

## Timeline

### sc...@gmail.com (2013-04-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-04-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-04-04)

I'm only seeing a NULL crash on ClusterFuzz: https://cluster-fuzz.appspot.com/testcase?key=176713459

That's with the test case hosted as files.

We're trying with HTTP.

### in...@chromium.org (2013-04-04)

Alex, can you please check this on ASAN mac. We can't reproduce this on ASAN linux with or without http.

### sc...@gmail.com (2013-04-04)

Hmm, maybe Mac specific (widget handling / painting treads on some OS-specific stuff). The Apple guys seem to have repro'ed it pretty easily on Mac WebKit.

### cy...@gmail.com (2013-04-04)

The heap spray may need to be adjusted, because if it doesn't work as expected, it'll NULL crash in RenderArena::free.

Also, I've seen that it always NULL crash with Debug builds (I don't know why).

### sc...@gmail.com (2013-04-04)

Yeah, my debug build NULL crashed.

ASAN should catch the use-after-free though, even if the spray doesn't work. ASAN doesn't care whether the read out of the free'd section is NULL or 0x41414141 :-)

Hmm, maybe the attempt at the heap spray cycles ASAN's freelist so hard that it loses track of the free'd section. Lemme build an ASAN build locally and make some adjustements to the repro.....

### cy...@gmail.com (2013-04-04)

Does ClusterFuzz play with Debug builds of Chromium?

### cy...@gmail.com (2013-04-04)

I have just executed the test case on Windows XP 32bit with Google Chrome stable and have the same result:

Thread 0 (crashed)
 0  chrome.dll + 0x1ed0cf
    eip = 0x01e1d0cf   esp = 0x0012f0c0   ebp = 0x0012f138   ebx = 0x04e0a010
    esi = 0x01369800   edi = 0x01303400   eax = 0x43434343   ecx = 0x00000000
    edx = 0x00000000   efl = 0x00010202


### cy...@gmail.com (2013-04-04)

So, IMHO, it's not Mac specific. It just does not work on Debug builds, probably because of ASSERTS.

### sc...@gmail.com (2013-04-05)

Yeah, works fine in a release build on Linux. Congrats, your PoC works amusingly well on 64-bit with no porting effort ;-)

mov    0x20(%rax),%rax
rax            0x4343434343434343

### gl...@chromium.org (2013-04-05)

[Comment Deleted]

### gl...@chromium.org (2013-04-05)

FTR the bug isn't reproducible for me with ASan on Mac. I've also tried increasing the quarantine to 4G, so the freed section should've stayed in the freelist.

### js...@chromium.org (2013-04-05)

From all the evidence it doesn't sound like it's touching anything freed. It really seems like something closer to a type confusion.

### cy...@gmail.com (2013-04-05)

[Comment Deleted]

### cy...@gmail.com (2013-04-05)

Issue is certainly here :

void RenderArena::free(size_t size, void* ptr)
{
    ASSERT(size <= gMaxRecycledSize - 32);
    m_totalSize -= size;

#ifdef ADDRESS_SANITIZER
    ::free(ptr);
#elif !defined(NDEBUG)
    // Use standard free so that memory debugging tools work.
    void* block = static_cast<char*>(ptr) - debugHeaderSize;
    RenderArenaDebugHeader* header = static_cast<RenderArenaDebugHeader*>(block);
    ASSERT(header->signature == signature);
    ASSERT_UNUSED(size, header->size == size);
    ASSERT(header->arena == this);
    header->signature = signatureDead;
    ::free(block);
#else
    // Ensure we have correct alignment for pointers.  Important for Tru64
    size = ROUNDUP(size, sizeof(void*));

    const size_t index = size >> kRecyclerShift;
    void* currentTop = m_recyclers[index];
    m_recyclers[index] = ptr;
    *((void**)ptr) = MaskPtr(currentTop, m_mask);
#endif
}

Debug and ASAN builds do not free pointers the same way.

### js...@chromium.org (2013-04-05)

@cyril - I doubt anyone investigating this is using debug builds of ASAN, since as you've noticed they tend to mask the actual vulnerability. And the problem really doesn't seem to involve a stale entry in the arena, since as your code snippet shows ASAN would be able to track that as a normal free.

### cy...@gmail.com (2013-04-05)

[Comment Deleted]

### cy...@gmail.com (2013-04-05)

In my comprehension, RenderArena is in fact some kind of allocator for RenderBlocks.

When you build with ASAN or in DEBUG mode, RenderArena does plain mallocs / frees, while in Release it acts differently.

That's certainly why only Release builds are vulnerable.

### cy...@gmail.com (2013-04-05)

Idea: wouldn't it be possible to remove those ifdefs (so that it acts like in Release builds) and generate a specific ASAN build ?

### kc...@chromium.org (2013-04-05)

arenas are evil. 
I wonder if anyone measured the impact of doing malloc/free here in release.
It might be comparable to arena, but safer. 

### cy...@gmail.com (2013-04-05)

I really wish I could help you more...

There's another fact I remember, and that's why I thought it's a RenderArena use-after-free :

The vulnerability is easier to control on Safari: just spray (tcmalloc) an ArrayBuffer of the same size as a RenderArena object just after removing the frame from its parent and you're done.

### js...@chromium.org (2013-04-05)

@kcc - Actually, in this case the arena is very helpful. It's been profiled as a net performance win and from a security perspective it's been hardened such that it prevents most RenderObject UAFs from being exploitable. That's why I'm dubious this is a UAF (accepting a potential hole during document destruction), rather than a type confusion, which ASAN also wouldn't necessarily detect.

### sc...@gmail.com (2013-04-05)

@cyril: this is a really curious bug. We'll get to the bottom of it :-)


### cy...@gmail.com (2013-04-15)

So guys, any progress with this curious bug? :)

### sc...@gmail.com (2013-04-15)

Sorry for the lethargic response; we're normally much faster.
Let me try and ping some people to get some prompt action.

### in...@chromium.org (2013-04-15)

Reversed the RenderArena alloc, free code for release and debug. I can easily reproduce the crash. free is here.

 	WebCore::RenderWidget::deref(WebCore::RenderArena * arena)  Line 329
>	WebCore::RenderWidget::destroy()  Line 122
 	WebCore::RenderObject::destroyAndCleanupAnonymousWrappers()  Line 2514 + 0x12 bytes
 	WebCore::Node::detach()  Line 1098
 	WebCore::ContainerNode::detach()  Line 801
 	WebCore::Element::detach()  Line 1324
 	WebCore::HTMLPlugInElement::detach()  Line 103
 	WebCore::HTMLPlugInImageElement::detach()  Line 201
 	WebCore::ContainerNode::detachChildren()  Line 215 + 0x12 bytes
 	WebCore::ContainerNode::detach()  Line 799
 	WebCore::Element::detach()  Line 1324
 	WebCore::ContainerNode::detachChildren()  Line 215 + 0x12 bytes
 	WebCore::ContainerNode::detach()  Line 799
 	WebCore::Element::detach()  Line 1324
 	WebCore::ContainerNode::detachChildren()  Line 215 + 0x12 bytes
 	WebCore::ContainerNode::detach()  Line 799
 	WebCore::Document::detach()  Line 2019
 	WebCore::Document::prepareForDestruction()  Line 2046 + 0x12 bytes
 	WebCore::Frame::setView(WTF::PassRefPtr<WebCore::FrameView> view)  Line 257
 	WebCore::FrameLoader::closeAndRemoveChild(WebCore::Frame * child)  Line 2225
 	WebCore::FrameLoader::detachFromParent()  Line 2308
 	WebCore::FrameLoader::frameDetached()  Line 2285
 	WebCore::HTMLFrameOwnerElement::disconnectContentFrame()  Line 85
 	WebCore::ChildFrameDisconnector::disconnectCollectedFrameOwners()  Line 315
 	WebCore::ChildFrameDisconnector::disconnect(WebCore::ChildFrameDisconnector::DisconnectPolicy policy)  Line 335
 	WebCore::willRemoveChild(WebCore::Node * child)  Line 439 + 0x26 bytes
 	WebCore::ContainerNode::removeChild(WebCore::Node * oldChild, int & ec)  Line 502 + 0xe bytes
 	WebCore::Node::removeChild(WebCore::Node * oldChild, int & ec)  Line 558
 	WebCore::V8Node::removeChildMethodCustom(const v8::Arguments & args)  Line 101 + 0x10 bytes
 	WebCore::NodeV8Internal::removeChildMethodCallbackForMainWorld(const v8::Arguments & args)  Line 555 + 0xd bytes
 	v8.dll!v8::internal::HandleApiCallHelper<0>(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args, v8::internal::Isolate * isolate)  Line 1327 + 0x13 bytes
 	v8.dll!v8::internal::Builtin_Impl_HandleApiCall(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args, v8::internal::Isolate * isolate)  Line 1345 + 0x11 bytes
 	v8.dll!v8::internal::Builtin_HandleApiCall(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args, v8::internal::Isolate * isolate)  Line 1344 + 0x46 bytes
 	2fc0a716()	
 	2fc410e3()	
 	2fc0f101()	
 	2fc22a52()	
 	2fc0f64a()	
 	v8.dll!v8::internal::Invoke(bool is_construct, v8::internal::Handle<v8::internal::JSFunction> function, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * args, bool * has_pending_exception)  Line 118 + 0x19 bytes
 	v8.dll!v8::internal::Execution::Call(v8::internal::Handle<v8::internal::Object> callable, v8::internal::Handle<v8::internal::Object> receiver, int argc, v8::internal::Handle<v8::internal::Object> * argv, bool * pending_exception, bool convert_receiver)  Line 181 + 0x1f bytes
 	v8.dll!v8::Function::Call(v8::Handle<v8::Object> recv, int argc, v8::Handle<v8::Value> * argv)  Line 3891 + 0x2d bytes
 	WebCore::ScriptController::callFunctionWithInstrumentation(WebCore::ScriptExecutionContext * context, v8::Handle<v8::Function> function, v8::Handle<v8::Object> receiver, int argc, v8::Handle<v8::Value> * args)  Line 234 + 0x22 bytes
 	WebCore::ScriptController::callFunction(v8::Handle<v8::Function> function, v8::Handle<v8::Object> receiver, int argc, v8::Handle<v8::Value> * args)  Line 187 + 0x53 bytes
 	WebCore::V8EventListener::callListenerFunction(WebCore::ScriptExecutionContext * context, v8::Handle<v8::Value> jsEvent, WebCore::Event * event)  Line 91 + 0x2d bytes
 	WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext * context, WebCore::Event * event, v8::Handle<v8::Value> jsEvent)  Line 138 + 0x1f bytes
 	WebCore::V8AbstractEventListener::handleEvent(WebCore::ScriptExecutionContext * context, WebCore::Event * event)  Line 99
 	WebCore::EventTarget::fireEventListeners(WebCore::Event * event, WebCore::EventTargetData * d, WTF::Vector<WebCore::RegisteredEventListener,1> & entry)  Line 257 + 0x22 bytes
 	WebCore::EventTarget::fireEventListeners(WebCore::Event * event)  Line 203 + 0x14 bytes
 	WebCore::Node::handleLocalEvents(WebCore::Event * event)  Line 2317
 	WebCore::EventContext::handleLocalEvents(WebCore::Event * event)  Line 58 + 0x24 bytes
 	WebCore::EventDispatcher::dispatchEventAtTarget()  Line 168 + 0x32 bytes
 	WebCore::EventDispatcher::dispatch()  Line 125 + 0x8 bytes
 	WebCore::EventDispatchMediator::dispatchEvent(WebCore::EventDispatcher * dispatcher)  Line 55
 	WebCore::EventDispatcher::dispatchEvent(WebCore::Node * node, WTF::PassRefPtr<WebCore::EventDispatchMediator> mediator)  Line 56 + 0x2a bytes
 	WebCore::Node::dispatchEvent(WTF::PassRefPtr<WebCore::Event> event)  Line 2337 + 0x33 bytes
 	WebCore::Node::dispatchBeforeLoadEvent(const WTF::String & sourceURL)  Line 2415
 	WebCore::HTMLPlugInElement::dispatchBeforeLoadEvent(const WTF::String & sourceURL)  Line 135 + 0xc bytes
 	WebCore::HTMLObjectElement::updateWidget(WebCore::PluginCreationOption pluginCreationOption)  Line 313 + 0x16 bytes
 	WebCore::FrameView::updateWidget(WebCore::RenderObject * object)  Line 2279 + 0x14 bytes
 	WebCore::FrameView::updateWidgets()  Line 2312
 	WebCore::FrameView::performPostLayoutTasks()  Line 2383 + 0x8 bytes
 	WebCore::FrameView::layout(bool allowSubtree)  Line 1176
 	WebCore::Document::implicitClose()  Line 2385
 	WebCore::FrameLoader::checkCallImplicitClose()  Line 815
 	WebCore::FrameLoader::checkCompleted()  Line 759
 	WebCore::FrameLoader::finishedParsing()  Line 692
 	WebCore::Document::finishedParsing()  Line 4336
 	WebCore::HTMLConstructionSite::finishedParsing()  Line 343 + 0x18 bytes
 	WebCore::HTMLTreeBuilder::finished()  Line 2831
 	WebCore::HTMLDocumentParser::end()  Line 766
 	WebCore::HTMLDocumentParser::attemptToRunDeferredScriptsAndEnd()  Line 777
 	WebCore::HTMLDocumentParser::prepareToStopParsing()  Line 214
 	WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk> popChunk)  Line 453 + 0xf bytes
 	WebCore::HTMLDocumentParser::pumpPendingSpeculations()  Line 485
 	WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk> chunk)  Line 334
 	WTF::FunctionWrapper<void (__thiscall WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()(const WTF::WeakPtr<WebCore::HTMLDocumentParser> & c, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk> p1)  Line 254 + 0x24 bytes
 	WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (__thiscall WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>,void __cdecl(WTF::WeakPtr<WebCore::HTMLDocumentParser>,WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()()  Line 523
 	WTF::Function<void __cdecl(void)>::operator()()  Line 704 + 0x1a bytes
 	WTF::callFunctionObject(void * context)  Line 62
 	glue.dll!base::internal::RunnableAdapter<void (__cdecl*)(void *)>::Run(void * const & a1)  Line 171 + 0x18 bytes
 	glue.dll!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__cdecl*)(void *)>,void __cdecl(void * const &)>::MakeItSo(base::internal::RunnableAdapter<void (__cdecl*)(void *)> runnable, void * const & a1)  Line 872
 	glue.dll!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__cdecl*)(void *)>,void __cdecl(void *),void __cdecl(void *)>,void __cdecl(void *)>::Run(base::internal::BindStateBase * base)  Line 1173 + 0x19 bytes
 	base.dll!base::Callback<void __cdecl(void)>::Run()  Line 396 + 0xe bytes
 	base.dll!base::MessageLoop::RunTask(const base::PendingTask & pending_task)  Line 476
 	base.dll!base::MessageLoop::DeferOrRunPendingTask(const base::PendingTask & pending_task)  Line 489
 	base.dll!base::MessageLoop::DoWork()  Line 669 + 0xc bytes
 	base.dll!base::MessagePumpForUI::DoRunLoop()  Line 241 + 0x1d bytes
 	base.dll!base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate, base::MessagePumpDispatcher * dispatcher)  Line 64 + 0xf bytes
 	base.dll!base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate)  Line 48 + 0x1c bytes
 	base.dll!base::MessageLoop::RunInternal()  Line 431 + 0x29 bytes
 	base.dll!base::MessageLoop::RunHandler()  Line 405
 	base.dll!base::RunLoop::Run()  Line 46
 	base.dll!base::MessageLoop::Run()  Line 312
 	base.dll!base::Thread::Run(base::MessageLoop * message_loop)  Line 153
 	base.dll!base::Thread::ThreadMain()  Line 197 + 0x16 bytes
 	base.dll!base::`anonymous namespace'::ThreadFunc(void * params)  Line 57 + 0xe bytes
 	kernel32.dll!@BaseThreadInitThunk@12()  + 0x12 bytes	
 	ntdll.dll!___RtlUserThreadStart@8()  + 0x27 bytes	
 	ntdll.dll!__RtlUserThreadStart@8()  + 0x1b bytes	


    RenderObjectSet::const_iterator end = m_widgetUpdateSet->end();
    for (RenderObjectSet::const_iterator it = m_widgetUpdateSet->begin(); it != end; ++it) {
        RenderObject* object = *it;
        objects.uncheckedAppend(object);
        if (object->isEmbeddedObject()) {
            RenderEmbeddedObject* embeddedObject = static_cast<RenderEmbeddedObject*>(object);
            embeddedObject->ref();
        }
    }

    for (size_t i = 0; i < size; ++i) {
        RenderObject* object = objects[i];
        updateWidget(object); /////free happens here from synchronous beforeload.
        m_widgetUpdateSet->remove(object);
    }

    RenderArena* arena = m_frame->document()->renderArena();
    for (size_t i = 0; i < size; ++i) {
        RenderObject* object = objects[i];
        if (object->isEmbeddedObject()) {
            RenderEmbeddedObject* embeddedObject = static_cast<RenderEmbeddedObject*>(object);
            embeddedObject->deref(arena); /// use happens here.
        }
    }

### gl...@chromium.org (2013-04-16)

FTR the bug manifests as a NULL deref for me under iOS simulator:

=================================================================
==77882==ERROR: AddressSanitizer: SEGV on unknown address 0xf4f40420 (pc 0xf4f40420 sp 0xb015bedc bp 0xb015bf18 T3)
AddressSanitizer can not provide additional info.
    #0 0xf4f4041f
    #0 0x1acbcc4d in WebCore::RenderWidget::updateWidgetGeometry() (in WebCore) + 29
    #1 0x1acbd764 in WebCore::RenderWidget::updateWidgetPosition() (in WebCore) + 36
    #2 0x1a568e2a in WebCore::FrameView::updateWidget(WebCore::RenderEmbeddedObject*) (in WebCore) + 186
    #3 0x1a568f43 in WebCore::FrameView::updateWidgets() (in WebCore) + 259
    #4 0x1a564ddd in WebCore::FrameView::performPostLayoutTasks() (in WebCore) + 381
    #5 0x1a56cc75 in WebCore::Timer<WebCore::FrameView>::fired() (in WebCore) + 37
    #6 0x1aee115b in WebCore::ThreadTimers::sharedTimerFiredInternal() (in WebCore) + 171
    #7 0x1aee1035 in WebCore::ThreadTimers::sharedTimerFired() (in WebCore) + 21
    #8 0x1ad2ec4f in WebCore::timerFired(__CFRunLoopTimer*, void*) (in WebCore) + 63
    #9 0x14f8d375 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_TIMER_CALLBACK_FUNCTION__ (in CoreFoundation) + 21
    #10 0x14f8ce05 in __CFRunLoopDoTimer (in CoreFoundation) + 533
    #11 0x14f74a81 in __CFRunLoopRun (in CoreFoundation) + 1809
    #12 0x14f73f43 in CFRunLoopRunSpecific (in CoreFoundation) + 275
    #13 0x14f73e1a in CFRunLoopRunInMode (in CoreFoundation) + 122
    #14 0x1af20c4f in RunWebThread(void*) (in WebCore) + 607
    #15 0x1430a210 in __asan::AsanThread::ThreadStart _asan_rtl_
Thread T3 created by T0 here:
    #0 0x142fcd9c in wrap_pthread_create _asan_rtl_
    #1 0x1af20856 in StartWebThread() (in WebCore) + 614
    #2 0x9555f018 in pthread_once (in libsystem_c.dylib) + 76
    #3 0x1af205e3 in WebThreadEnable (in WebCore) + 35
    #4 0x1a0d64ff in +[WebView(WebPrivate) enableWebThread] (in WebKit) + 287
    #5 0x1a0d47ea in WebKitInitialize (in WebKit) + 58
    #6 0x15814e1e in UIApplicationInitialize (in UIKit) + 242
    #7 0x15811c24 in UIApplicationMain (in UIKit) + 227
    #8 0x3009 in +[GTMLogger standardLogger] GTMLogger.m:62
    #9 0x2a34 in +[GTMLogger setSharedLogger:] GTMLogger.m:55
    #10 0x0 in 0x00001000 (in Chromium)
==77882==ABORTING


Not sure yet why ASan didn't find the NULL deref here.

### gl...@chromium.org (2013-04-16)

s/didn't find the NULL deref/didn't find the UAF/

### [Deleted User] (2013-04-16)

Yes. This bug involves two of my favorite dead-man-walking sections of code.  1. Frame-loading being driven from the rendering tree and 2. updateWidgetPositions().  Both are security risks, and both are slated for removal in Blink (now that we don't have Mac WK1 constraints).

WJ has expressed interest in both of these removals, but any one of us layout folks may get to it in the near term.

This bug can (and will) be fixed w/o these architectural corrections.  I will take a look ASAP (this week).

I'm slightly surprised we didn't have explicit test coverage of this case.  We've definitely had bugs very similar to this (removing a frame from inside a onbeforeload).

### cy...@gmail.com (2013-04-16)

"I'm slightly surprised we didn't have explicit test coverage of this case.  We've definitely had bugs very similar to this (removing a frame from inside a onbeforeload)."

The fact that it happens in an OBJECT beforeload seems to be crucial here. Maybe you covered other kind of elements?

### [Deleted User] (2013-04-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-04-16)

@glider: I do think it's worth spending time understanding why ASAN doesn't flag this as security. It looks like our internal fuzzing hit a substantially similar test case: https://cluster-fuzz.appspot.com/testcase?key=172181623, but it didn't get flagged as security.

Maybe there's some ASAN (or Chrome!) code tweak we could make that would fix this misdetection and therefore reveal a bunch of other "hidden" security bugs that we've already generated test cases for?

### sc...@gmail.com (2013-04-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-04-17)

Finally have ASAN stack. Just revert http://trac.webkit.org/changeset/97009 and add gc() call in handleBeforeLoad(). See the free on line 2027 m_renderArena.clear();, previously ASAN bypassed arena and just used malloc, free.

==19343== ERROR: AddressSanitizer: heap-use-after-free on address 0x607200151eb0 at pc 0x7f4b8a8315c2 bp 0x7fff8263b830 sp 0x7fff8263b828
READ of size 8 at 0x607200151eb0 thread T0 (chrome)
    #0 0x7f4b8a8315c1 in WTF::RefPtr<WebCore::Widget>::operator!() const out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:66
    #1 0x7f4b8f0c75db in WebCore::RenderWidget::updateWidgetPosition() out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderWidget.cpp:335
    #2 0x7f4b8c0be07f in WebCore::FrameView::updateWidgets() out/Release/../../third_party/WebKit/Source/WebCore/page/FrameView.cpp:2314
    #3 0x7f4b8c0b537e in WebCore::FrameView::performPostLayoutTasks() out/Release/../../third_party/WebKit/Source/WebCore/page/FrameView.cpp:2386
    #4 0x7f4b8c0b4b0f in WebCore::FrameView::layout(bool) out/Release/../../third_party/WebKit/Source/WebCore/page/FrameView.cpp:1175
    #5 0x7f4b8c6be33a in WebCore::Document::implicitClose() out/Release/../../third_party/WebKit/Source/WebCore/dom/Document.cpp:2366
    #6 0x7f4b8bfbc354 in WebCore::FrameLoader::checkCompleted() out/Release/../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:755
    #7 0x7f4b8bfba417 in WebCore::FrameLoader::finishedParsing() out/Release/../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:688
    #8 0x7f4b8c6cd8c3 in WebCore::Document::finishedParsing() out/Release/../../third_party/WebKit/Source/WebCore/dom/Document.cpp:4314
    #9 0x7f4b8a8de5e4 in WebCore::HTMLDocumentParser::prepareToStopParsing() out/Release/../../third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:213
    #10 0x7f4b8a8e0f4f in WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) out/Release/../../third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:453
    #11 0x7f4b8a8df105 in WebCore::HTMLDocumentParser::pumpPendingSpeculations() out/Release/../../third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:483
    #12 0x7f4b8a8dfb2e in WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) out/Release/../../third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:333
    #13 0x7f4b8a96c69e in WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()(WTF::WeakPtr<WebCore::HTMLDocumentParser> const&, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) out/Release/../../third_party/WebKit/Source/wtf/Functional.h:254
    #14 0x7f4b8a96c569 in WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>, void (WTF::WeakPtr<WebCore::HTMLDocumentParser>, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()() out/Release/../../third_party/WebKit/Source/wtf/Functional.h:522
    #15 0x7f4b8d55eafd in WTF::callFunctionObject(void*) out/Release/../../third_party/WebKit/Source/wtf/chromium/MainThreadChromium.cpp:61
    #16 0x7f4b8a5e80c6 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(void*)>, void (void* const&)>::MakeItSo(base::internal::RunnableAdapter<void (*)(void*)>, void* const&) out/Release/../../base/bind_internal.h:871
    #17 0x7f4b8a636c64 in base::MessageLoop::RunTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:474
    #18 0x7f4b8a63744b in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:486
    #19 0x7f4b8a637671 in base::MessageLoop::DoWork() out/Release/../../base/message_loop.cc:669
    #20 0x7f4b8a64312f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) out/Release/../../base/message_pump_default.cc:29
    #21 0x7f4b8a6363b7 in base::MessageLoop::RunInternal() out/Release/../../base/message_loop.cc:431
    #22 0x7f4b8a66d7c9 in base::RunLoop::Run() out/Release/../../base/run_loop.cc:45
    #23 0x7f4b8a635121 in base::MessageLoop::Run() out/Release/../../base/message_loop.cc:311
    #24 0x7f4b8f465a5d in content::RendererMain(content::MainFunctionParams const&) out/Release/../../content/renderer/renderer_main.cc:226
    #25 0x7f4b8d7c6583 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) out/Release/../../content/app/content_main_runner.cc:383
    #26 0x7f4b8d7c6ea3 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) out/Release/../../content/app/content_main_runner.cc:439
    #27 0x7f4b8d7c7b9a in content::ContentMainRunnerImpl::Run() out/Release/../../content/app/content_main_runner.cc:736
    #28 0x7f4b8d7c5cab in content::ContentMain(int, char const**, content::ContentMainDelegate*) out/Release/../../content/app/content_main.cc:35
    #29 0x7f4b88a44f2a in ChromeMain out/Release/../../chrome/app/chrome_main.cc:32
    #30 0x7f4b88a44e7a in main out/Release/../../chrome/app/chrome_exe_main_gtk.cc:34
    #31 0x7f4b8171576c in
    #32 0x7f4b88a44da4 in
0x607200151eb0 is located 1456 bytes inside of 8192-byte region [0x607200151900,0x607200153900)
freed by thread T0 (chrome) here:
    #0 0x7f4b88a38f92 in __interceptor_free
    #1 0x7f4b8fde40d3 in WebCore::FreeArenaList(WebCore::ArenaPool*, WebCore::Arena*) out/Release/../../third_party/WebKit/Source/WebCore/platform/Arena.cpp:177
    #2 0x7f4b8c6fa575 in void WTF::deleteOwnedPtr<WebCore::RenderArena>(WebCore::RenderArena*) out/Release/../../third_party/WebKit/Source/wtf/OwnPtrCommon.h:47
    #3 0x7f4b8c6bfeef in WebCore::Document::detach() out/Release/../../third_party/WebKit/Source/WebCore/dom/Document.cpp:2027
    #4 0x7f4b8c0a51ba in WebCore::Frame::setView(WTF::PassRefPtr<WebCore::FrameView>) out/Release/../../third_party/WebKit/Source/WebCore/page/Frame.cpp:248
    #5 0x7f4b8bfc7c10 in WebCore::FrameLoader::closeAndRemoveChild(WebCore::Frame*) out/Release/../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:2222
    #6 0x7f4b8bfc7a46 in WebCore::FrameLoader::detachFromParent() out/Release/../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:2305
    #7 0x7f4b8bfc80a2 in WebCore::FrameLoader::frameDetached() out/Release/../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:2282
    #8 0x7f4b8a8cf62a in WebCore::HTMLFrameOwnerElement::disconnectContentFrame() out/Release/../../third_party/WebKit/Source/WebCore/html/HTMLFrameOwnerElement.cpp:84
    #9 0x7f4b8c69c4c0 in WebCore::ChildFrameDisconnector::disconnectCollectedFrameOwners() out/Release/../../third_party/WebKit/Source/WebCore/dom/ContainerNodeAlgorithms.h:314
    #10 0x7f4b8c697f38 in WebCore::willRemoveChild(WebCore::Node*) out/Release/../../third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:439
    #11 0x7f4b8c697a53 in WebCore::ContainerNode::removeChild(WebCore::Node*, int&) out/Release/../../third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:502
    #12 0x7f4b8c766bd1 in WebCore::Node::removeChild(WebCore::Node*, int&) out/Release/../../third_party/WebKit/Source/WebCore/dom/Node.cpp:557
    #13 0x7f4b8d2ee4bc in WebCore::V8Node::removeChildMethodCustom(v8::Arguments const&) out/Release/../../third_party/WebKit/Source/bindings/v8/custom/V8NodeCustom.cpp:101
    #14 0x7f4b8e2be983 in v8::internal::MaybeObject* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) out/Release/../../v8/src/builtins.cc:1327
    #15 0x7f4b5970654d
    #16 0x7f4b5974dec7
    #17 0x7f4b5970bc73
    #18 0x7f4b59725ffd
    #19 0x7f4b5970c336
    #15 0x7f4b8e30bbb1 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) out/Release/../../v8/src/execution.cc:118
    #16 0x7f4b8e286aa2 in v8::Function::Call(v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) out/Release/../../v8/src/api.cc:3891
    #17 0x7f4b8d25fc97 in WebCore::ScriptController::callFunctionWithInstrumentation(WebCore::ScriptExecutionContext*, v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) out/Release/../../third_party/WebKit/Source/bindings/v8/ScriptController.cpp:234
    #18 0x7f4b8d25f9b2 in WebCore::ScriptController::callFunction(v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) out/Release/../../third_party/WebKit/Source/bindings/v8/ScriptController.cpp:187
    #19 0x7f4b8d404cb2 in WebCore::V8EventListener::callListenerFunction(WebCore::ScriptExecutionContext*, v8::Handle<v8::Value>, WebCore::Event*) out/Release/../../third_party/WebKit/Source/bindings/v8/V8EventListener.cpp:91
    #20 0x7f4b8d4036f7 in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext*, WebCore::Event*, v8::Handle<v8::Value>) out/Release/../../third_party/WebKit/Source/bindings/v8/V8AbstractEventListener.cpp:138
    #21 0x7f4b8d4034ba in WebCore::V8AbstractEventListener::handleEvent(WebCore::ScriptExecutionContext*, WebCore::Event*) out/Release/../../third_party/WebKit/Source/bindings/v8/V8AbstractEventListener.cpp:98
    #22 0x7f4b8c73d1b2 in WebCore::EventTarget::fireEventListeners(WebCore::Event*, WebCore::EventTargetData*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) out/Release/../../third_party/WebKit/Source/WebCore/dom/EventTarget.cpp:257
    #23 0x7f4b8c73cb3d in WebCore::EventTarget::fireEventListeners(WebCore::Event*) out/Release/../../third_party/WebKit/Source/WebCore/dom/EventTarget.cpp:203
    #24 0x7f4b8c7fc7f5 in WebCore::EventContext::handleLocalEvents(WebCore::Event*) const out/Release/../../third_party/WebKit/Source/WebCore/dom/EventContext.cpp:58
previously allocated by thread T0 (chrome) here:
    #0 0x7f4b88a39072 in __interceptor_malloc
    #1 0x7f4b8fde3e4b in WebCore::ArenaAllocate(WebCore::ArenaPool*, unsigned int, unsigned int&) out/Release/../../third_party/WebKit/Source/WebCore/platform/Arena.cpp:131
    #2 0x7f4b8ee0ff03 in WebCore::RenderArena::allocate(unsigned long) out/Release/../../third_party/WebKit/Source/WebCore/rendering/RenderArena.cpp:133
    #3 0x7f4b8c6bfab9 in WebCore::Document::attach() out/Release/../../third_party/WebKit/Source/WebCore/dom/Document.cpp:1950
    #4 0x7f4b8c0a5a72 in WebCore::Frame::setDocument(WTF::PassRefPtr<WebCore::Document>) out/Release/../../third_party/WebKit/Source/WebCore/page/Frame.cpp:287
    #5 0x7f4b8bfaf724 in WebCore::DocumentWriter::begin(WebCore::KURL const&, bool, WebCore::Document*) out/Release/../../third_party/WebKit/Source/WebCore/loader/DocumentWriter.cpp:140
    #6 0x7f4b8bf98c28 in WebCore::DocumentLoader::commitData(char const*, unsigned long) out/Release/../../third_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:684
    #7 0x7f4b89ffe429 in WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader*, char const*, int) out/Release/../../third_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1046
    #8 0x7f4b8bf9ae79 in WebCore::DocumentLoader::commitLoad(char const*, int) out/Release/../../third_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:665
    #9 0x7f4b8c00febd in WebCore::CachedRawResource::data(WTF::PassRefPtr<WebCore::ResourceBuffer>) out/Release/../../third_party/WebKit/Source/WebCore/loader/cache/CachedRawResource.cpp:67
    #10 0x7f4b8bff0197 in WebCore::ResourceLoader::sendDataToResource(char const*, int) out/Release/../../third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:525
    #11 0x7f4b8bff0476 in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle*, char const*, int, int) out/Release/../../third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:507
    #12 0x7f4b8cdde300 in content::ResourceDispatcher::OnReceivedData(IPC::Message const&, int, int, int, int) out/Release/../../content/common/resource_dispatcher.cc:414
    #13 0x7f4b8cde0774 in bool ResourceMsg_DataReceived::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, int, int, int, int>(IPC::Message const*, content::ResourceDispatcher*, content::ResourceDispatcher*, void (content::ResourceDispatcher::*)(IPC::Message const&, int, int, int, int)) out/Release/../../content/common/resource_messages.h:243
    #14 0x7f4b8cddd022 in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) out/Release/../../content/common/resource_dispatcher.cc:611
    #15 0x7f4b8cddc360 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/resource_dispatcher.cc:305
    #16 0x7f4b8cc89b40 in content::ChildThread::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/child_thread.cc:241
    #17 0x7f4b89a66ad4 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) out/Release/../../ipc/ipc_channel_proxy.cc:261
    #18 0x7f4b89a6d9d8 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) out/Release/../../base/bind_internal.h:899
    #19 0x7f4b8a636c64 in base::MessageLoop::RunTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:474
    #20 0x7f4b8a63744b in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:486
    #21 0x7f4b8a637671 in base::MessageLoop::DoWork() out/Release/../../base/message_loop.cc:669
    #22 0x7f4b8a64312f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) out/Release/../../base/message_pump_default.cc:29
    #23 0x7f4b8a6363b7 in base::MessageLoop::RunInternal() out/Release/../../base/message_loop.cc:431
    #24 0x7f4b8a66d7c9 in base::RunLoop::Run() out/Release/../../base/run_loop.cc:45
    #25 0x7f4b8a635121 in base::MessageLoop::Run() out/Release/../../base/message_loop.cc:311
    #26 0x7f4b8f465a5d in content::RendererMain(content::MainFunctionParams const&) out/Release/../../content/renderer/renderer_main.cc:226
    #27 0x7f4b8d7c6583 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) out/Release/../../content/app/content_main_runner.cc:383
    #28 0x7f4b8d7c6ea3 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) out/Release/../../content/app/content_main_runner.cc:439
    #29 0x7f4b8d7c7b9a in content::ContentMainRunnerImpl::Run() out/Release/../../content/app/content_main_runner.cc:736
Shadow bytes around the buggy address:
  0x0c0ec0022380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022390: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec00223a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec00223b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec00223c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c0ec00223d0: fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd
  0x0c0ec00223e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec00223f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022410: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022420: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:     fa
  Heap righ redzone:     fb
  Freed Heap region:     fd
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
==19343== ABORTING
[0417/085006:ERROR:nacl_helper_linux.cc(262)] NaCl helper process running without a sandbox!
Most likely you need to configure your SUID sandbox correctly



### sc...@gmail.com (2013-04-17)

Good job @inferno, does this mean you have a fix pending? :D

### cy...@gmail.com (2013-04-17)

Hi! So, that's good news, it seems that you identified the whole problem now.

Basically, I was not wrong about that RenderArena object UAF?

### in...@chromium.org (2013-04-17)

@scarybeasts - i don't have a fix yet. But this is a pretty bad situation where renderarena itself is freed (and all the renderobjects with it), i don't see an easy way to recover from this, so probably hard crash might be worth considering.

@cyril - yes you were right about renderarena uaf, we were just trying to understand how it got freed. Thanks for the awesome bug.

### in...@chromium.org (2013-04-17)

https://codereview.chromium.org/14329005/

### [Deleted User] (2013-04-18)

My understanding of the test case is as follows:

1. the outer document loads an iframe.
2. In that iframe, it registers for its own load event.
3. in that iframe's load event, it creates a new object and appends it to the outer document's body (right after the <iframe>) setting a beforeload listener on this new <object>.
4.  In the beforeload of this <object> it registers a SubTreeModified mutation event listener.
5. On the second call(?!) to the beforeload listener it removes the original iframe (which is still in its load event), which causes synchronous destruction of the iframe's DOM/rendering tree and RenderArena.
6.  When the stack unwinds and the load event completes we attempt an updateWidgetPositions, and BOOM.

Why this check isn't saving our souls:
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/WebCore/dom/Document.cpp&q=Document::implicitClose&sq=package:chromium&type=cs&l=2336
I'm not sure.

I'd need to see full stacks from inferno's reproduction.

Although I suspect that some of inferno's hardening may be correct, I'm not sure that it's the right fix for this bug.

As noted before, we need to kill the Widget tree with fire.  And we also need to kill the fact that loads are issued from the rendering tree. :)  Either of those efforts being completed would have avoided this bug.

### in...@chromium.org (2013-04-18)

full stacks, sorry for missing frames in free stacks in last time.

<subprocess.Popen object at 0x7f9e0dccfb10>
[24758:24758:0417/100519:ERROR:zygote_host_impl_linux.cc(146)] Running without the SUID sandbox! See https://code.google.com/p/chromium/wiki/LinuxSUIDSandboxDevelopment for more information on developing with the sandbox on.
[24758:24797:0417/100526:ERROR:object_proxy.cc(624)] Failed to get name owner. Got org.freedesktop.DBus.Error.NameHasNoOwner: Could not get owner of name 'org.chromium.Mtpd': no such name
[24758:24797:0417/100526:ERROR:object_proxy.cc(624)] Failed to get name owner. Got org.freedesktop.DBus.Error.NameHasNoOwner: Could not get owner of name 'org.chromium.Mtpd': no such name
[24758:24758:0417/100527:ERROR:object_proxy.cc(529)] Failed to call method: org.chromium.Mtpd.EnumerateStorages: object_path= /org/chromium/Mtpd: org.freedesktop.DBus.Error.ServiceUnknown: The name org.chromium.Mtpd was not provided by any .service files
=================================================================
==24813== ERROR: AddressSanitizer: heap-use-after-free on address 0x607200156b00 at pc 0x7fc9925f81e2 bp 0x7fff71473590 sp 0x7fff71473588
READ of size 8 at 0x607200156b00 thread T0 (chrome)
    #0 0x7fc9925f81e1 in WTF::RefPtr<WebCore::Widget>::operator!() const out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:66
    #1 0x7fc994992adb in WebCore::RenderWidget::updateWidgetPosition() out/Release/../../third_party/WebKit/Source/core/rendering/RenderWidget.cpp:335
    #2 0x7fc99605cfcf in WebCore::FrameView::updateWidgets() out/Release/../../third_party/WebKit/Source/core/page/FrameView.cpp:2314
    #3 0x7fc996054b5e in WebCore::FrameView::performPostLayoutTasks() out/Release/../../third_party/WebKit/Source/core/page/FrameView.cpp:2386
    #4 0x7fc9960542ef in WebCore::FrameView::layout(bool) out/Release/../../third_party/WebKit/Source/core/page/FrameView.cpp:1175
    #5 0x7fc99580cfca in WebCore::Document::implicitClose() out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:2366
    #6 0x7fc995f48db4 in WebCore::FrameLoader::checkCompleted() out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:755
    #7 0x7fc995f46e77 in WebCore::FrameLoader::finishedParsing() out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:688
    #8 0x7fc99581c9a3 in WebCore::Document::finishedParsing() out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:4314
    #9 0x7fc9926ab1e4 in WebCore::HTMLDocumentParser::prepareToStopParsing() out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:213
    #10 0x7fc9926ada3f in WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:453
    #11 0x7fc9926abd05 in WebCore::HTMLDocumentParser::pumpPendingSpeculations() out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:483
    #12 0x7fc9926ac5ee in WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:333
    #13 0x7fc99276540e in WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()(WTF::WeakPtr<WebCore::HTMLDocumentParser> const&, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) out/Release/../../third_party/WebKit/Source/wtf/Functional.h:254
    #14 0x7fc9927652d9 in WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>, void (WTF::WeakPtr<WebCore::HTMLDocumentParser>, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()() out/Release/../../third_party/WebKit/Source/wtf/Functional.h:522
    #15 0x7fc994465e4d in WTF::callFunctionObject(void*) out/Release/../../third_party/WebKit/Source/wtf/chromium/MainThreadChromium.cpp:61
    #16 0x7fc99242ec56 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(void*)>, void (void* const&)>::MakeItSo(base::internal::RunnableAdapter<void (*)(void*)>, void* const&) out/Release/../../base/bind_internal.h:871
    #17 0x7fc99247d7f4 in base::MessageLoop::RunTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:474
    #18 0x7fc99247dfdb in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:486
    #19 0x7fc99247e201 in base::MessageLoop::DoWork() out/Release/../../base/message_loop.cc:669
    #20 0x7fc992489cbf in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) out/Release/../../base/message_pump_default.cc:29
    #21 0x7fc99247cf47 in base::MessageLoop::RunInternal() out/Release/../../base/message_loop.cc:431
    #22 0x7fc9924b4359 in base::RunLoop::Run() out/Release/../../base/run_loop.cc:45
    #23 0x7fc99247bcb1 in base::MessageLoop::Run() out/Release/../../base/message_loop.cc:311
    #24 0x7fc996e0796d in content::RendererMain(content::MainFunctionParams const&) out/Release/../../content/renderer/renderer_main.cc:226
    #25 0x7fc994a7af93 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) out/Release/../../content/app/content_main_runner.cc:383
    #26 0x7fc994a7b8b3 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) out/Release/../../content/app/content_main_runner.cc:439
    #27 0x7fc994a7c5aa in content::ContentMainRunnerImpl::Run() out/Release/../../content/app/content_main_runner.cc:736
    #28 0x7fc994a7a6bb in content::ContentMain(int, char const**, content::ContentMainDelegate*) out/Release/../../content/app/content_main.cc:35
    #29 0x7fc99025421a in ChromeMain out/Release/../../chrome/app/chrome_main.cc:32
    #30 0x7fc99025416a in main out/Release/../../chrome/app/chrome_exe_main_gtk.cc:39
    #31 0x7fc988f2276c in
    #32 0x7fc990254094 in
0x607200156b00 is located 1792 bytes inside of 8192-byte region [0x607200156400,0x607200158400)
freed by thread T0 (chrome) here:
    #0 0x7fc990248282 in __interceptor_free
    #1 0x7fc996b80e73 in WebCore::FreeArenaList(WebCore::ArenaPool*, WebCore::Arena*) out/Release/../../third_party/WebKit/Source/core/platform/Arena.cpp:177
    #2 0x7fc995850945 in void WTF::deleteOwnedPtr<WebCore::RenderArena>(WebCore::RenderArena*) out/Release/../../third_party/WebKit/Source/wtf/OwnPtrCommon.h:47
    #3 0x7fc99580ebaf in WebCore::Document::detach() out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:2027
    #4 0x7fc9960454ea in WebCore::Frame::setView(WTF::PassRefPtr<WebCore::FrameView>) out/Release/../../third_party/WebKit/Source/core/page/Frame.cpp:248
    #5 0x7fc995f54660 in WebCore::FrameLoader::closeAndRemoveChild(WebCore::Frame*) out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:2222
    #6 0x7fc995f54496 in WebCore::FrameLoader::detachFromParent() out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:2305
    #7 0x7fc995f54af2 in WebCore::FrameLoader::frameDetached() out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:2282
    #8 0x7fc9925a064a in WebCore::HTMLFrameOwnerElement::disconnectContentFrame() out/Release/../../third_party/WebKit/Source/core/html/HTMLFrameOwnerElement.cpp:84
    #9 0x7fc9957e51d0 in WebCore::ChildFrameDisconnector::disconnectCollectedFrameOwners() out/Release/../../third_party/WebKit/Source/core/dom/ContainerNodeAlgorithms.h:314
    #10 0x7fc9957e0af8 in WebCore::willRemoveChild(WebCore::Node*) out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:439
    #11 0x7fc9957e05e3 in WebCore::ContainerNode::removeChild(WebCore::Node*, int&) out/Release/../../third_party/WebKit/Source/core/dom/ContainerNode.cpp:502
    #12 0x7fc9958c0951 in WebCore::Node::removeChild(WebCore::Node*, int&) out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:557
    #13 0x7fc9920f225c in WebCore::V8Node::removeChildMethodCustom(v8::Arguments const&) out/Release/../../third_party/WebKit/Source/bindings/v8/custom/V8NodeCustom.cpp:101
    #14 0x7fc99531e2f3 in v8::internal::MaybeObject* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) out/Release/../../v8/src/builtins.cc:1327
    #15 0x22f1b800654d
    #16 0x22f1b804dec7
    #17 0x22f1b800bc73
    #18 0x22f1b8025ffd
    #19 0x22f1b800c336
    #15 0x7fc99536b521 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) out/Release/../../v8/src/execution.cc:118
    #16 0x7fc9952e6412 in v8::Function::Call(v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) out/Release/../../v8/src/api.cc:3891
    #17 0x7fc992061ad7 in WebCore::ScriptController::callFunctionWithInstrumentation(WebCore::ScriptExecutionContext*, v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) out/Release/../../third_party/WebKit/Source/bindings/v8/ScriptController.cpp:234
    #18 0x7fc9920617f2 in WebCore::ScriptController::callFunction(v8::Handle<v8::Function>, v8::Handle<v8::Object>, int, v8::Handle<v8::Value>*) out/Release/../../third_party/WebKit/Source/bindings/v8/ScriptController.cpp:187
    #19 0x7fc9921f3b82 in WebCore::V8EventListener::callListenerFunction(WebCore::ScriptExecutionContext*, v8::Handle<v8::Value>, WebCore::Event*) out/Release/../../third_party/WebKit/Source/bindings/v8/V8EventListener.cpp:91
    #20 0x7fc9921f2597 in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext*, WebCore::Event*, v8::Handle<v8::Value>) out/Release/../../third_party/WebKit/Source/bindings/v8/V8AbstractEventListener.cpp:138
    #21 0x7fc9921f235a in WebCore::V8AbstractEventListener::handleEvent(WebCore::ScriptExecutionContext*, WebCore::Event*) out/Release/../../third_party/WebKit/Source/bindings/v8/V8AbstractEventListener.cpp:98
    #22 0x7fc995893ac2 in WebCore::EventTarget::fireEventListeners(WebCore::Event*, WebCore::EventTargetData*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) out/Release/../../third_party/WebKit/Source/core/dom/EventTarget.cpp:257
    #23 0x7fc99589344d in WebCore::EventTarget::fireEventListeners(WebCore::Event*) out/Release/../../third_party/WebKit/Source/core/dom/EventTarget.cpp:203
    #24 0x7fc995958695 in WebCore::EventContext::handleLocalEvents(WebCore::Event*) const out/Release/../../third_party/WebKit/Source/core/dom/EventContext.cpp:58
    #25 0x7fc99594ffe3 in WebCore::EventDispatcher::dispatchEventAtTarget() out/Release/../../third_party/WebKit/Source/core/dom/EventDispatcher.cpp:168
    #26 0x7fc99594fa48 in WebCore::EventDispatcher::dispatch() out/Release/../../third_party/WebKit/Source/core/dom/EventDispatcher.cpp:125
    #27 0x7fc99594e6bb in WebCore::EventDispatchMediator::dispatchEvent(WebCore::EventDispatcher*) const out/Release/../../third_party/WebKit/Source/core/dom/EventDispatchMediator.cpp:54
    #28 0x7fc99594e82d in WebCore::EventDispatcher::dispatchEvent(WebCore::Node*, WTF::PassRefPtr<WebCore::EventDispatchMediator>) out/Release/../../third_party/WebKit/Source/core/dom/EventDispatcher.cpp:56
    #29 0x7fc9958ca7c4 in WebCore::Node::dispatchEvent(WTF::PassRefPtr<WebCore::Event>) out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:2337
    #30 0x7fc9958cc10b in WebCore::Node::dispatchBeforeLoadEvent(WTF::String const&) out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:2414
    #31 0x7fc9925f7c74 in WebCore::HTMLPlugInElement::dispatchBeforeLoadEvent(WTF::String const&) out/Release/../../third_party/WebKit/Source/core/html/HTMLPlugInElement.cpp:135
    #32 0x7fc9925f0b22 in WebCore::HTMLObjectElement::updateWidget(WebCore::PluginCreationOption) out/Release/../../third_party/WebKit/Source/core/html/HTMLObjectElement.cpp:313
    #33 0x7fc99605cc6a in WebCore::FrameView::updateWidget(WebCore::RenderObject*) out/Release/../../third_party/WebKit/Source/core/page/FrameView.cpp:2282
    #34 0x7fc99605cfcf in WebCore::FrameView::updateWidgets() out/Release/../../third_party/WebKit/Source/core/page/FrameView.cpp:2314
    #35 0x7fc996054b5e in WebCore::FrameView::performPostLayoutTasks() out/Release/../../third_party/WebKit/Source/core/page/FrameView.cpp:2386
    #36 0x7fc9960542ef in WebCore::FrameView::layout(bool) out/Release/../../third_party/WebKit/Source/core/page/FrameView.cpp:1175
    #37 0x7fc99580cfca in WebCore::Document::implicitClose() out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:2366
    #38 0x7fc995f48db4 in WebCore::FrameLoader::checkCompleted() out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:755
    #39 0x7fc995f46e77 in WebCore::FrameLoader::finishedParsing() out/Release/../../third_party/WebKit/Source/core/loader/FrameLoader.cpp:688
    #40 0x7fc99581c9a3 in WebCore::Document::finishedParsing() out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:4314
    #41 0x7fc9926ab1e4 in WebCore::HTMLDocumentParser::prepareToStopParsing() out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:213
    #42 0x7fc9926ada3f in WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:453
    #43 0x7fc9926abd05 in WebCore::HTMLDocumentParser::pumpPendingSpeculations() out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:483
    #44 0x7fc9926ac5ee in WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) out/Release/../../third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:333
    #45 0x7fc99276540e in WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()(WTF::WeakPtr<WebCore::HTMLDocumentParser> const&, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>) out/Release/../../third_party/WebKit/Source/wtf/Functional.h:254
    #46 0x7fc9927652d9 in WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>, void (WTF::WeakPtr<WebCore::HTMLDocumentParser>, WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()() out/Release/../../third_party/WebKit/Source/wtf/Functional.h:522
    #47 0x7fc994465e4d in WTF::callFunctionObject(void*) out/Release/../../third_party/WebKit/Source/wtf/chromium/MainThreadChromium.cpp:61
    #48 0x7fc99242ec56 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(void*)>, void (void* const&)>::MakeItSo(base::internal::RunnableAdapter<void (*)(void*)>, void* const&) out/Release/../../base/bind_internal.h:871
    #49 0x7fc99247d7f4 in base::MessageLoop::RunTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:474
    #50 0x7fc99247dfdb in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:486
    #51 0x7fc99247e201 in base::MessageLoop::DoWork() out/Release/../../base/message_loop.cc:669
    #52 0x7fc992489cbf in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) out/Release/../../base/message_pump_default.cc:29
    #53 0x7fc99247cf47 in base::MessageLoop::RunInternal() out/Release/../../base/message_loop.cc:431
    #54 0x7fc9924b4359 in base::RunLoop::Run() out/Release/../../base/run_loop.cc:45
    #55 0x7fc99247bcb1 in base::MessageLoop::Run() out/Release/../../base/message_loop.cc:311
    #56 0x7fc996e0796d in content::RendererMain(content::MainFunctionParams const&) out/Release/../../content/renderer/renderer_main.cc:226
    #57 0x7fc994a7af93 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) out/Release/../../content/app/content_main_runner.cc:383
    #58 0x7fc994a7b8b3 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) out/Release/../../content/app/content_main_runner.cc:439
    #59 0x7fc994a7c5aa in content::ContentMainRunnerImpl::Run() out/Release/../../content/app/content_main_runner.cc:736
    #60 0x7fc994a7a6bb in content::ContentMain(int, char const**, content::ContentMainDelegate*) out/Release/../../content/app/content_main.cc:35
    #61 0x7fc99025421a in ChromeMain out/Release/../../chrome/app/chrome_main.cc:32
    #62 0x7fc99025416a in main out/Release/../../chrome/app/chrome_exe_main_gtk.cc:39
    #63 0x7fc988f2276c in
previously allocated by thread T0 (chrome) here:
    #0 0x7fc990248362 in __interceptor_malloc
    #1 0x7fc996b80beb in WebCore::ArenaAllocate(WebCore::ArenaPool*, unsigned int, unsigned int&) out/Release/../../third_party/WebKit/Source/core/platform/Arena.cpp:131
    #2 0x7fc9946ddff3 in WebCore::RenderArena::allocate(unsigned long) out/Release/../../third_party/WebKit/Source/core/rendering/RenderArena.cpp:133
    #3 0x7fc99580e779 in WebCore::Document::attach() out/Release/../../third_party/WebKit/Source/core/dom/Document.cpp:1950
    #4 0x7fc996045da2 in WebCore::Frame::setDocument(WTF::PassRefPtr<WebCore::Document>) out/Release/../../third_party/WebKit/Source/core/page/Frame.cpp:287
    #5 0x7fc995f3d474 in WebCore::DocumentWriter::begin(WebCore::KURL const&, bool, WebCore::Document*) out/Release/../../third_party/WebKit/Source/core/loader/DocumentWriter.cpp:140
    #6 0x7fc995f286c8 in WebCore::DocumentLoader::commitData(char const*, unsigned long) out/Release/../../third_party/WebKit/Source/core/loader/DocumentLoader.cpp:684
    #7 0x7fc99180ec29 in WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader*, char const*, int) out/Release/../../third_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1046
    #8 0x7fc995f2a6c9 in WebCore::DocumentLoader::commitLoad(char const*, int) out/Release/../../third_party/WebKit/Source/core/loader/DocumentLoader.cpp:665
    #9 0x7fc995fa679d in WebCore::CachedRawResource::data(WTF::PassRefPtr<WebCore::ResourceBuffer>) out/Release/../../third_party/WebKit/Source/core/loader/cache/CachedRawResource.cpp:67
    #10 0x7fc995f7db37 in WebCore::ResourceLoader::sendDataToResource(char const*, int) out/Release/../../third_party/WebKit/Source/core/loader/ResourceLoader.cpp:525
    #11 0x7fc995f7de16 in WebCore::ResourceLoader::didReceiveData(WebCore::ResourceHandle*, char const*, int, int) out/Release/../../third_party/WebKit/Source/core/loader/ResourceLoader.cpp:507
    #12 0x7fc9942da6e0 in content::ResourceDispatcher::OnReceivedData(IPC::Message const&, int, int, int, int) out/Release/../../content/common/resource_dispatcher.cc:414
    #13 0x7fc9942dcb54 in bool ResourceMsg_DataReceived::Dispatch<content::ResourceDispatcher, content::ResourceDispatcher, int, int, int, int>(IPC::Message const*, content::ResourceDispatcher*, content::ResourceDispatcher*, void (content::ResourceDispatcher::*)(IPC::Message const&, int, int, int, int)) out/Release/../../content/common/resource_messages.h:243
    #14 0x7fc9942d9402 in content::ResourceDispatcher::DispatchMessage(IPC::Message const&) out/Release/../../content/common/resource_dispatcher.cc:611
    #15 0x7fc9942d8740 in content::ResourceDispatcher::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/resource_dispatcher.cc:305
    #16 0x7fc994185f20 in content::ChildThread::OnMessageReceived(IPC::Message const&) out/Release/../../content/common/child_thread.cc:241
    #17 0x7fc991276bf4 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) out/Release/../../ipc/ipc_channel_proxy.cc:261
    #18 0x7fc99127daf8 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) out/Release/../../base/bind_internal.h:899
    #19 0x7fc99247d7f4 in base::MessageLoop::RunTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:474
    #20 0x7fc99247dfdb in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) out/Release/../../base/message_loop.cc:486
    #21 0x7fc99247e201 in base::MessageLoop::DoWork() out/Release/../../base/message_loop.cc:669
    #22 0x7fc992489cbf in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) out/Release/../../base/message_pump_default.cc:29
    #23 0x7fc99247cf47 in base::MessageLoop::RunInternal() out/Release/../../base/message_loop.cc:431
    #24 0x7fc9924b4359 in base::RunLoop::Run() out/Release/../../base/run_loop.cc:45
    #25 0x7fc99247bcb1 in base::MessageLoop::Run() out/Release/../../base/message_loop.cc:311
    #26 0x7fc996e0796d in content::RendererMain(content::MainFunctionParams const&) out/Release/../../content/renderer/renderer_main.cc:226
    #27 0x7fc994a7af93 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) out/Release/../../content/app/content_main_runner.cc:383
    #28 0x7fc994a7b8b3 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) out/Release/../../content/app/content_main_runner.cc:439
    #29 0x7fc994a7c5aa in content::ContentMainRunnerImpl::Run() out/Release/../../content/app/content_main_runner.cc:736
    #30 0x7fc994a7a6bb in content::ContentMain(int, char const**, content::ContentMainDelegate*) out/Release/../../content/app/content_main.cc:35
    #31 0x7fc99025421a in ChromeMain out/Release/../../chrome/app/chrome_main.cc:32
    #32 0x7fc99025416a in main out/Release/../../chrome/app/chrome_exe_main_gtk.cc:39
    #33 0x7fc988f2276c in
Shadow bytes around the buggy address:
  0x0c0ec0022d10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022d20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022d30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022d40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022d50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c0ec0022d60:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022d70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022d80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022d90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022da0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c0ec0022db0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:     fa
  Heap righ redzone:     fb
  Freed Heap region:     fd
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
==24813== ABORTING
[0417/100717:ERROR:nacl_helper_linux.cc(262)] NaCl helper process running without a sandbox!
Most likely you need to configure your SUID sandbox correctly



### [Deleted User] (2013-04-18)

Bah!  FrameView::updateWidget is just completely unsafe.  It's not OK to hold pointers to RenderObjects (which are allocated in an arena) in a set like that.  We need to make sure that set is cleared before the arena can be.

I believe the fix is to make the document leaving the frame tell the FrameView to clear its widget update list.

At least from the iOS simulator stack, it looks like a timer is being fired to handle post-layout tasks, and the FrameView (which may itself be dead?) has a list of widgets (which no longer have a RenderArena backing them?) to be UAF'd.

### [Deleted User] (2013-04-18)

Ahha!  So the trick is that we're inside the set-walk of updateWidgets. :)

I would expect us to be hitting this ASSERT, based on your updated stacks?
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/page/FrameView.cpp&q=updateWidgets&sq=package:chromium&type=cs&l=2267

### [Deleted User] (2013-04-18)

From the code, I might expect that the RenderWidget was removing itself from the update set:
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/rendering/RenderEmbeddedObject.cpp&q=removeWidgetToUpdate&sq=package:chromium&type=cs&l=87

But it's possible it can't reach it's frameView() from this callstack.  We are inside Frame::setView() which may be related.

### [Deleted User] (2013-04-18)

canHaveWidget() is always true in Blink... but I don't believe that it ever needs to be:
https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/rendering/RenderEmbeddedObject.cpp&q=addWidgetToUpdate&sq=package:chromium&l=256&type=cs

I think we should try setting canHaveWidget() to false and running the tests. If they pass, this bug is then impossible, and another huge chunk of the Widget mess is gone. :)

### in...@chromium.org (2013-04-18)

I remember I didnt hit that assert. Clearing the widget update list might work, we need to be careful about 
1) We can still trigger UAF in the last statement of FrameView::updateWidget

pluginElement->updateWidget(CreateAnyWidgetType); /// free point
        } else
            ASSERT_NOT_REACHED();

        // Caution: it's possible the object was destroyed again, since loading a
        // plugin may run any arbitrary JavaScript.
        embeddedObject->updateWidgetPosition(); /// this is renderer, so can trigger use after free. we should probably still get it from element->renderer() and have null check here.
    }
}

I think we could cleanup code and instead of iterating over renderobjects, we can keep a vector of their elements and iterate over that. 

### [Deleted User] (2013-04-18)

The whole widget insanity needs to die.  Yes, we could change to hold on to elements instead, but we really shouldn't need to hold onto anything. :)  I'm trying the "nuke from orbit" solution of returning false from canHaveWidget() now.

### [Deleted User] (2013-04-18)

My naive "canHaveWidget" removal fails a zillion tests.  I'll have to look more closely tomorrow.

### [Deleted User] (2013-04-18)

I looked at your proposed change again.  I think it's fine, but no need to crash.  Make it not crash and add the test and we're good to go.

### in...@chromium.org (2013-04-18)

I did write the layouttest, but when writing the fix, i don't see any way to safely recover without breaking functionality. Please see my last comment(C#9) in https://codereview.chromium.org/14329005/.

### cy...@gmail.com (2013-04-19)

Hi @inferno: it seems to me that there's a little mistake in the layout test, because there's no parent.dsm function anymore, but it's still 'used' in handleBeforeLoad.
That's certainly not a big issue, but in case you missed it...

### in...@chromium.org (2013-04-22)

Thanks Cyril ! I attached the wrong file, see the typo in name as well - pbject-beforeload-crash instead of object-beforeload-crash. That one has the old parent.dsm call, had indent issues, etc.

### in...@chromium.org (2013-04-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-04-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-04-23)

https://src.chromium.org/viewvc/blink?view=rev&revision=148933

### bu...@chromium.org (2013-04-23)

------------------------------------------------------------------------
r148933 | inferno@chromium.org | 2013-04-23T21:31:42.866975Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/beforeload/object-beforeload-crash-main-expected.txt?r1=148933&r2=148932&pathrev=148933
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/dom/Document.cpp?r1=148933&r2=148932&pathrev=148933
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/beforeload/object-beforeload-crash-main.html?r1=148933&r2=148932&pathrev=148933
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/FrameView.cpp?r1=148933&r2=148932&pathrev=148933
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/beforeload/resources/object-beforeload-crash.html?r1=148933&r2=148932&pathrev=148933
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/page/FrameView.h?r1=148933&r2=148932&pathrev=148933

UpdateWidget() can fire beforeload event synchronously blowing away RenderArena and its associated RenderObjects. In that case, we bail-out and clear m_widgetUpdateSet set.

BUG=226696

Review URL: https://codereview.chromium.org/14329005
------------------------------------------------------------------------

### sc...@gmail.com (2013-05-03)

@cyril.cattiaux: thanks again for a really good report, and welcome to the Chromium VRP! :D
This report qualifies for a $2000 reward -- $1000 base for a good quality report and a $1000 bonus for demonstrating exploitability with a repro that faults at an attacker-specified address.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### cy...@gmail.com (2013-05-06)

Thank you!

That's my first report, when and how I will get the reward?

B.R.

### in...@chromium.org (2013-05-06)

Cyril - Chris / Parisa should contact you by email on the next steps.

### sc...@gmail.com (2013-05-06)

M27 is https://src.chromium.org/viewvc/blink?view=rev&revision=149764

### bu...@chromium.org (2013-05-06)

------------------------------------------------------------------------
r149764 | cevans@chromium.org | 2013-05-06T18:37:22.626126Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/page/FrameView.h?r1=149764&r2=149763&pathrev=149764
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/dom/Document.cpp?r1=149764&r2=149763&pathrev=149764
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/page/FrameView.cpp?r1=149764&r2=149763&pathrev=149764

Merge Blink r148933 to M27

BUG=226696
TBR=inferno@chromium.org

Review URL: https://codereview.chromium.org/14999003
------------------------------------------------------------------------

### sc...@gmail.com (2013-05-17)

[Empty comment from Monorail migration]

### jo...@chromium.org (2013-05-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-06-08)

reverted on trunk in r152074, on m27 branch as well.

We will uptake alternate fix - http://trac.webkit.org/changeset/149185

### in...@chromium.org (2013-06-08)

https://codereview.chromium.org/16695002/

### in...@chromium.org (2013-06-08)

reverted from m28 in r152075.
reverted from m27 in r152073.
reverted from trunk in r152074.

and another fix in cq in https://codereview.chromium.org/16695002/. We would need to merge this on m27 and m28. for m27 on monday.

### in...@chromium.org (2013-06-09)

https://src.chromium.org/viewvc/blink?view=rev&revision=152086

Chris, can you please help to merge this on m27.

### sc...@gmail.com (2013-06-10)

Yeah, I've got this Monday, I'll merge to M27 and M28. Thanks!!

### sc...@gmail.com (2013-06-11)

M27: r152168

### sc...@gmail.com (2013-06-11)

M28: r152169

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### cy...@gmail.com (2013-08-23)

Hi. I haven't received any reward from Google yet, nor any email in my box. Is it normal ?

Thank you very much.

Best regards,

Cyril

### pa...@chromium.org (2013-08-23)

Hey Cyril,

Thanks for following up! Your payment did slip through the cracks of our reward process, so I'm really sorry about the delay :( Our finance team should be following up with you ASAP to set you up for payment.

Sorry again!
Parisa

### sc...@gmail.com (2013-08-24)

@cyril.cattiaux: Sorry about that, we'll get it fixed ASAP as noted in the above comment.

Separately, I wonder if you saw http://googleonlinesecurity.blogspot.com/2013/08/security-rewards-at-google-two.html ? We're now paying up to $5000 for reports like this, with the requirement that the researcher demonstrate the bug is nasty. Repros that fault at 0x43434343 go a long way to showing that a bug is nasty ;-) Full requirements at http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process

TL;DR -- might be a good time to re-run your fuzzer :D

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### pa...@chromium.org (2013-12-20)

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

This issue was migrated from crbug.com/chromium/226696?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077343)*
