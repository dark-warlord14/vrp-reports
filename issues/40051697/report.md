# Use after free in V8HTMLElementWrapperFactory.cpp

| Field | Value |
|-------|-------|
| **Issue ID** | [40051697](https://issues.chromium.org/issues/40051697) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2011-11-30 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Running attached all.html file causes chrome to display sad tab.

**VERSION**  

Chrome Version: [15.0.874.120] + [stable]  

[17.0.954.0]+ [Developer Build 111694 Linux]  

Operating System: [Ubuntu 10.04]

**REPRODUCTION CASE**

1. Copy attached all.html and geo.html files to same folder.
2. Open all.html file in chrome.
3. Wait about 2 seconds when page loads and click on test button.  
   
   Chrome will display a sad tab.  
   
   But this does not happen always. So we might need to try several times.

I understand that all.html contains some unnecessary lines. I will post a reduced test case as soon as I figure out which parts are unnecessary. Actually this bug occurred to me randomly, while I was testing something else.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State:  

exception record-

#0 0x00007fdf7c026c2a in WTF::RefPtr[WTF::StringImpl](javascript:void(0);)::get (  

this=0x363636363636365e)  

at third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:60  

60 T\* get() const { return m\_ptr; }

stack trace

#0 0x00007fdf7c026c2a in WTF::RefPtr[WTF::StringImpl](javascript:void(0);)::get (  

this=0x363636363636365e)  

at third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:60  

#1 0x00007fdf7c0264ac in WTF::String::impl (this=0x363636363636365e)  

at third\_party/WebKit/Source/JavaScriptCore/wtf/text/WTFString.h:143  

#2 0x00007fdf7c026570 in WTF::AtomicString::impl (this=0x363636363636365e)  

at third\_party/WebKit/Source/JavaScriptCore/wtf/text/AtomicString.h:62  

#3 0x00007fdf7cf754ca in WebCore::createV8HTMLWrapper (  

element=0x7fdf6b1a2d80, forceNewObject=false)  

at out/Debug/obj/gen/webkit/V8HTMLElementWrapperFactory.cpp:801  

#4 0x00007fdf7ca75dd3 in WebCore::toV8 (impl=0x7fdf6b1a2d80,  

forceNewObject=false)  

at third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8HTMLElementCustom.cpp:60  

#5 0x00007fdf7ca75cc8 in WebCore::toV8 (impl=0x7fdf6b1a2d80,  

forceNewObject=false)  

at third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8ElementCustom.cpp:61  

#6 0x00007fdf7cef524f in getElementByIdCallback (args=...)  

at out/Debug/obj/gen/webcore/bindings/V8Document.cpp:1351  

#7 0x00007fdf7bae3bc5 in HandleApiCallHelper<false> (args=...,  

isolate=0x7fdf79666000) at v8/src/builtins.cc:1177  

#8 0x00007fdf7bade6fb in Builtin\_Impl\_HandleApiCall (args=...,  

isolate=0x7fdf79666000) at v8/src/builtins.cc:1194  

#9 0x00007fdf7bade6cc in Builtin\_HandleApiCall (args=...,  

isolate=0x7fdf79666000) at v8/src/builtins.cc:1193  

#10 0x00002c7df3f0420e in ?? ()

registers

rax 0x363636363636365e 3906369333256140382  

rbx 0x0 0  

rcx 0x7fdf6acee180 140597546377600  

rdx 0x0 0  

rsi 0x0 0  

rdi 0x363636363636365e 3906369333256140382  

rbp 0x7fff87f44d30 0x7fff87f44d30  

rsp 0x7fff87f44d30 0x7fff87f44d30  

r8 0x7fdf6ace2890 140597546330256  

r9 0xd74 3444  

r10 0x7fdf79666da0 140597791190432  

r11 0x7fdf72363a4e 140597670591054  

r12 0x7fff87f470e8 140735474331880  

r13 0x1 1  

r14 0x3 3  

r15 0x7fff87f470f0 140735474331888  

rip 0x7fdf7c026c2a 0x7fdf7c026c2a <WTF::RefPtr[WTF::StringImpl](javascript:void(0);)::get() const+12>  

eflags 0x10202 [ IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0

## Attachments

- [geo.html](attachments/geo.html) (text/html; charset=us-ascii, 134 B)
- [all.html](attachments/all.html) (text/html; charset=us-ascii, 3.3 KB)
- [reproduce.ogv](attachments/reproduce.ogv) (application/ogg; charset=binary, 1.3 MB)
- [all_reduced.html](attachments/all_reduced.html) (text/html; charset=us-ascii, 1.9 KB)
- [all_reduced2.html](attachments/all_reduced2.html) (text/html; charset=us-ascii, 1.9 KB)
- [reproduce.ogv](attachments/reproduce_53327097.ogv) (application/ogg; charset=binary, 2.2 MB)
- [geo.html](attachments/geo_53327152.html) (text/html; charset=us-ascii, 134 B)
- [all_reduced3.html](attachments/all_reduced3.html) (text/html; charset=us-ascii, 1.9 KB)
- [geo.html](attachments/geo_53327171.html) (text/html; charset=us-ascii, 134 B)
- [all_reduced4.html](attachments/all_reduced4.html) (text/html; charset=us-ascii, 2.1 KB)
- [root_cause.html](attachments/root_cause.html) (text/html; charset=us-ascii, 668 B)
- [ContainerNode_before_fix.cpp](attachments/ContainerNode_before_fix.cpp) (text/x-lisp; charset=us-ascii, 37.5 KB)
- [ContainerNode_after_fix.cpp](attachments/ContainerNode_after_fix.cpp) (text/x-lisp; charset=us-ascii, 37.6 KB)
- [ContainerNode_before_fix2.cpp](attachments/ContainerNode_before_fix2.cpp) (text/x-lisp; charset=us-ascii, 37.5 KB)
- [ContainerNode_after_fix2.cpp](attachments/ContainerNode_after_fix2.cpp) (text/x-lisp; charset=us-ascii, 39.8 KB)

## Timeline

### pa...@chromium.org (2011-12-01)

I can't reproduce it in 16 beta or trunk on 64-bit Linux. It needs a file called just.html, but I don't know if that is related.

What is the "crash" button for? I can't get a crash by pressing either "test" or "crash".

Note that I do get a crash when loading the page in trunk because I have a missing plugin:


[16058:16058:2617525732802:FATAL:missing_plugin.cc(157)] Check failed: !plugin()->web_view()->mainFrame()->isLoading(). 
Backtrace:
        base::debug::StackTrace::StackTrace() [0x7ffff22a437a]
        logging::LogMessage::~LogMessage() [0x7ffff22cf502]
        MissingPlugin::UpdateMessage() [0x7ffff2186e4f]
        MissingPlugin::DidFinishLoading() [0x7ffff21870e8]
        webkit::WebViewPlugin::didFinishLoad() [0x7ffff42a593c]
        WebKit::FrameLoaderClientImpl::dispatchDidFinishLoad() [0x7ffff3064463]
        WebCore::FrameLoader::checkLoadCompleteForThisFrame() [0x7ffff38b9c22]
        WebCore::FrameLoader::checkLoadComplete() [0x7ffff38ba3ab]
        WebCore::FrameLoader::checkCompleted() [0x7ffff38b237e]
        WebCore::FrameLoader::loadDone() [0x7ffff38b2130]
        WebCore::CachedResourceLoader::loadDone() [0x7ffff3902f08]
        WebCore::SubresourceLoader::releaseResources() [0x7ffff38e4898]
        WebCore::ResourceLoader::didFinishLoading() [0x7ffff38e00a9]
        WebCore::SubresourceLoader::didFinishLoading() [0x7ffff38e447a]
        WebCore::ResourceLoader::didFinishLoading() [0x7ffff38e08b7]
        WebCore::ResourceHandleInternal::didFinishLoading() [0x7ffff307b4f2]
        webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest() [0x7ffff42cd3fc]
        webkit_glue::WebURLLoaderImpl::Context::HandleDataURL() [0x7ffff42cd71f]
        base::internal::RunnableAdapter<>::Run() [0x7ffff42ce797]
        base::internal::InvokeHelper<>::MakeItSo() [0x7ffff42ce73b]
        base::internal::Invoker<>::Run() [0x7ffff42ce68c]
        base::Callback<>::Run() [0x7ffff154d467]
        MessageLoop::RunTask() [0x7ffff22d4d33]
        MessageLoop::DeferOrRunPendingTask() [0x7ffff22d4e4d]
        MessageLoop::DoWork() [0x7ffff22d566f]
        base::MessagePumpDefault::Run() [0x7ffff22dd7a0]
        MessageLoop::RunInternal() [0x7ffff22d49b5]
        MessageLoop::RunHandler() [0x7ffff22d4868]
        MessageLoop::Run() [0x7ffff22d417b]
        RendererMain() [0x7ffff49ef339]
        (anonymous namespace)::RunNamedProcessTypeMain() [0x7ffff2268045]
        content::ContentMain() [0x7ffff2268626]
        ChromeMain [0x7ffff139363d]
        main [0x7ffff13935fc]
        0x7fffe92b6c4d
        0x7ffff1393509

I think that's because you call for a Java applet in all.html?

It sounds like we need a more complete and reduced test case. Can you please send one? Thanks!

### ch...@gmail.com (2011-12-01)

Just.html file is not required.
It crashes when test button is clicked once the page refreshes. It does not happen always.
crash button is required. It receives a synthetic click event.
I understand that we need a reduced test case. I will try to post one as soon as possible.

### ch...@gmail.com (2011-12-01)

Attached all_reduced.html. Some of the unnecessary sections were removed.
But I think it can be further reduced. I ll post if I managed to do it.

Attached reproduce.ogv, which shows how to reproduce. Anyway it does not reproduce always.

### ch...@gmail.com (2011-12-01)

[Comment Deleted]

### ch...@gmail.com (2011-12-01)

This is the output from Asan.


==12816== ERROR: AddressSanitizer heap-use-after-free on address 0x7fb272eb5aa4 at pc 0x7fb283250801 bp 0x7ffff099aed0 sp 0x7ffff099aea8
READ of size 4 at 0x7fb272eb5aa4 thread T0
    #0 0x7fb283250801 in _ZN7WebCore4toV8EPNS_7ElementEb /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/dom/Node.h:660
    #1 0x7fb283d34338 in _ZN7WebCore16DocumentInternalL22getElementByIdCallbackERKN2v89ArgumentsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/out/Release/obj/gen/webcore/bindings/V8Document.cpp:1351
    #2 0x7fb281449ab3 in HandleApiCallHelper /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/v8/src/builtins.cc:1177
addr2line: '': No such file
    #3 0x31510020420e in  
0x7fb272eb5aa4 is located 36 bytes inside of 232-byte region [0x7fb272eb5a80,0x7fb272eb5b68)
freed by thread T0 here:
    #0 0x7fb285d09bb9 in _ZdlPv _asan_rtl_
    #1 0x7fb2814e3be9 in _ZN2v88internal15RuntimeProfiler9IsEnabledEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/v8/src/runtime-profiler.h:50
previously allocated by thread T0 here:
    #0 0x7fb285d09833 in _Znwm _asan_rtl_
    #1 0x7fb28594a5ae in _ZN7WebCore17HTMLIFrameElement6createERKNS_13QualifiedNameEPNS_8DocumentE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/html/HTMLIFrameElement.cpp:48
    #2 0x7fb283e6a256 in _ZNK3WTF10PassRefPtrIN7WebCore17HTMLIFrameElementEE7leakRefEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161
    #3 0x7fb283e5b1e0 in _ZN7WebCore18HTMLElementFactory17createHTMLElementERKNS_13QualifiedNameEPNS_8DocumentEPNS_15HTMLFormElementEb /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/out/Release/obj/gen/webkit/HTMLElementFactory.cpp:705
    #4 0x7fb282764dde in _ZNK3WTF10PassRefPtrIN7WebCore11HTMLElementEE7leakRefEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:161
    #5 0x7fb2827659b7 in _ZN7WebCore20HTMLConstructionSite17insertHTMLElementERNS_15AtomicHTMLTokenE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/html/parser/HTMLConstructionSite.cpp:293
    #6 0x7fb2826d1ecd in _ZN7WebCore15HTMLTreeBuilder29processGenericRawTextStartTagERNS_15AtomicHTMLTokenE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:2801
    #7 0x7fb2826bf261 in _ZN7WebCore15HTMLTreeBuilder15processStartTagERNS_15AtomicHTMLTokenE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:1230
    #8 0x7fb2826be51f in _ZN7WebCore15HTMLTreeBuilder12processTokenERNS_15AtomicHTMLTokenE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:481
    #9 0x7fb2826be0b5 in _ZN7WebCore15HTMLTreeBuilder28constructTreeFromAtomicTokenERNS_15AtomicHTMLTokenE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:467
    #10 0x7fb2826bdfae in _ZN7WebCore15HTMLTreeBuilder22constructTreeFromTokenERNS_9HTMLTokenE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/html/parser/HTMLTreeBuilder.cpp:452
    #11 0x7fb282675edb in _ZN7WebCore18HTMLDocumentParser13pumpTokenizerENS0_15SynchronousModeE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:263
    #12 0x7fb282677a4e in _ZN7WebCore18HTMLDocumentParser6appendERKNS_15SegmentedStringE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:372
    #13 0x7fb28591488d in ~Deque /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/JavaScriptCore/wtf/Deque.h:370
    #14 0x7fb282f517bf in _ZN7WebCore14DocumentLoader10commitDataEPKcm /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:317
    #15 0x7fb281e5ccf3 in _ZN6WebKit21FrameLoaderClientImpl13committedLoadEPN7WebCore14DocumentLoaderEPKci /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1121
    #16 0x7fb282f513db in _ZN7WebCore14DocumentLoader10commitLoadEPKci /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/loader/DocumentLoader.cpp:303
    #17 0x7fb282fea674 in _ZN7WebCore14ResourceLoader14didReceiveDataEPKcixb /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/loader/ResourceLoader.cpp:291
    #18 0x7fb282fc7f62 in _ZN7WebCore18MainResourceLoader14didReceiveDataEPKcixb /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/loader/MainResourceLoader.cpp:467
    #19 0x7fb282febd6c in _ZN7WebCore24InspectorInstrumentation12hasFrontendsEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third_party/WebKit/Source/WebCore/inspector/InspectorInstrumentation.h:208
    #20 0x7fb281cf52c2 in _ZN18ResourceDispatcher14OnReceivedDataERKN3IPC7MessageEiN4base14FileDescriptorEii /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/common/resource_dispatcher.cc:382
    #21 0x7fb281cf4969 in _ZN18ResourceDispatcher15DispatchMessageERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./content/common/resource_messages.h:144
    #22 0x7fb281cf2700 in _ZN18ResourceDispatcher17OnMessageReceivedERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/common/resource_dispatcher.cc:307


### kc...@chromium.org (2011-12-01)

Chamal, thanks for the report! Suggestion for the future ones: 
1. Run the report through c++filt to get more readable function names. 
2. Strip the "/home/chamal/chrome/home/chrome-svn/tarball/chromium/src/" part from the file names (you can do it by passing "/chromium/src/" to asan_symbolize.py)

### pa...@chromium.org (2011-12-01)

Thanks for the reduced repro. I am still having trouble getting the repro to work repeatably, but I have seen it cause a crash (with a slightly different ASAN result than you have:

==8014== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fbe25fff1ca at pc 0x7fbe50c29cc8 bp 0x7fbe3af21e10 sp 0x7fbe3af21de8
READ of size 1 at 0x7fbe25fff1ca thread T8

[no symbols; running a fresh ASAN build to deal with that]


### ch...@gmail.com (2011-12-02)

I tried to reduce the reproduction html file by removing part by part. But all parts in all_reduced.html seems necessary.

Other thing I noted was all.html attached with original report crashes more often than all_reduced.html.

### ch...@gmail.com (2011-12-04)

Another point noted is this issue occurs only when plugin is blocked due to outdated plugin or lack of permission.

### ch...@gmail.com (2011-12-05)

[Comment Deleted]

### ch...@gmail.com (2011-12-05)

Based on output of Asan I think the iframe with id frm is the one used after being freed.

1). Asan says this error occurs when getElementByIdCallback method of V8Document.cpp is called.
2). Asan also says memory  was allocated by create method of HTMLIFrameElement.cpp.
3). So based on that information we can guess that this error happens when getElementById is called on a iframe.
4). This error happens when test button is clicked.
    Test button calls op() method which has this content.
    document.getElementById('btn1').appendChild(document.getElementById('testr'));
5). In this method getElementById is called twice, but only iframe is testr.
    But iframe with id testr cannot be the cause of use after free because it is never removed from the document by any of the javascript code in document.
6). But this method calls appendChild method which fires a DOMSubtreeModified event.
    Which will cause the sendEvent() method to execute.
7). sendEvent method has many getElementById calls but only time it calls getElementById on a iframe is in it's last line.
     document.removeChild(document.getElementById('frm'));
   
    So this is why I think the cause of use after free is iframe with id frm.

### ch...@gmail.com (2011-12-07)

Added these printf statements to TreeScope.cpp's addElementById method and removeElementById. These methods adds and deletes elements from DocumentOrderedMap.

void TreeScope::addElementById(const AtomicString& elementId, Element* element)
{
	printf("chamal: TreeScope addElementById%s\n", elementId.string().utf8().data());
    m_elementsById.add(elementId.impl(), element);
}

void TreeScope::removeElementById(const AtomicString& elementId, Element* element)
{
	printf("chamal: TreeScope removeElementById%s\n", elementId.string().utf8().data());
    m_elementsById.remove(elementId.impl(), element);
}

addElementById method is called three times for iframe with id frm.
removeElementById method is called only once for iframe with id frm.

In normal situations chrome will say Object not found when we call getElementById method on a object removed from document. But in this case DocumentOrderedMap contains the frm iframe which actually should have been removed from DocumentOrderedMap.

Can you please show me the code section of WebKit which free's elements?


### in...@chromium.org (2011-12-07)

http://www.google.com/codesearch#OAMlx_jo-ck/src/third_party/WebKit/Source/WebCore/rendering/RenderArena.cpp&exact_package=chromium&ct=rc&cd=2&q=renderarena

Chamal, if you can provide us with a repro that reliably crashes under ASAN, that will increase your chances of a higher reward.

### ch...@gmail.com (2011-12-07)

Attached all_reduced2.html which reproduces well.

Steps
-----
1. Disable permission to run applets on localhost or 127.0.0.1
2. Copy all_reduced2.html to a folder served by local web server.
3. Open all_reduced2.html in chrome.
4. all_reduced2.html file tries to load a applet.
   Keep the mouse cursor over this applet and keep moving the cursor over applet.
   Aplets text should change to "Ice-tea plugin needs permission".
   This step looks odd but it is necessary :).
   Do not click on any of the buttons. Chrome will display sad tab after about 5 seconds.

Please see attached reproduce.ogv if instructions are not clear.

This bug also reproduces in chrome stable version 15.0.874.121 on Ubuntu 10.04.


### sk...@chromium.org (2011-12-08)

RCE in renderer = high severity

### js...@chromium.org (2011-12-08)

@skylined, did you confirm the vulnerability before setting the severity? So far no one else has been able to produce a repro.

### ch...@gmail.com (2011-12-08)

I also cannot reproduce in chrome version 18.0.965.0 (Developer Build 113390 Linux) Release build. Debug build it reproduces but less occasionally.

### sk...@chromium.org (2011-12-08)

@jschuh: no. I set the severity to what I expect it to be given the information we have so far. I assume you are against this and want to have no severity rating until we are sure?

### ke...@chromium.org (2011-12-08)

@skylined: jschuh's recommendation is in line with what we have been using in our triage guidelines: http://www.chromium.org/Home/chromium-security/security-bug-lifecycle

One benefit of waiting until verification is that we reduce noise in our bug count metrics.

### js...@chromium.org (2011-12-08)

We'll leave it untriaged for now. @inferno has tried it against clusterfuzz and hasn't gotten any consistent hits. If nothing shows up in aother few days we'll close it out.


### ch...@gmail.com (2011-12-09)

Can you guys please copy the geo.html attached with report to same folder as all_recudeced2.html and try to reproduce.
I forgot to mention it in steps in https://crbug.com/chromium/105867#c14.

### ch...@gmail.com (2011-12-12)

[Comment Deleted]

### ch...@gmail.com (2011-12-12)

I think this error happens because of below mentioned method get called on below mentioned order on frame with id frm.
Some details mentioned below are my assumptions.

Methods
-------

1). DocumentOrderedMap::add(AtomicStringImpl* key, Element* element)
2). DocumentOrderedMap::add(AtomicStringImpl* key, Element* element)
3). DocumentOrderedMap::get(AtomicStringImpl* key, const TreeScope* scope)
4). Node::removeChild(Node* oldChild, ExceptionCode& ec)
5). Node::removeChild(Node* oldChild, ExceptionCode& ec)
6). DocumentOrderedMap::get(AtomicStringImpl* key, const TreeScope* scope)
7). DocumentOrderedMap::remove(AtomicStringImpl* key, Element* element)
8). DocumentOrderedMap::get(AtomicStringImpl* key, const TreeScope* scope)
9). Node::removeChild(Node* oldChild, ExceptionCode& ec)
10).Node::removeChild(Node* oldChild, ExceptionCode& ec)
11). DocumentOrderedMap::get(AtomicStringImpl* key, const TreeScope* scope)

a). In steps 1 and 2 DocumentOrderedMap::add is called on frm iframe twice. This causes frm iframe to be added to m_duplicateCounts of DocumentOrderedMap.
    I think duplicateCounts is used for storing multiple elements with same id. There is only one element with id frm in this test case.
    Think this is the main cause of this use after free.
b). Then in steps 3 to 6 DocumentOrderedMap::get and Node::removeChild is called. Think frm iframe is not removed or freed by Node::removeChild for some reason I could not find.
c). In step 7 DocumentOrderedMap::remove is called which removes the frm iframe from m_map Map in DocumentOrderedMap.
    But frm iframe is still in duplicateCounts because of reason mentioned in a) .
d). In step 8 DocumentOrderedMap::get is called. frm iframe is not in m_map.
    But it gets added to m_map because frm iframe is still in m_duplicateCounts and document tree.
   
    inline Element* DocumentOrderedMap::get(AtomicStringImpl* key, const TreeScope* scope) const
	{
	    ASSERT(key);

	    m_map.checkConsistency();

	    Element* element = m_map.get(key);
	    if (element)
	    {
		return element;
	    }

	    if (m_duplicateCounts.contains(key)) {
		// We know there's at least one node that matches; iterate to find the first one.
		for (Node* node = scope->firstChild(); node; node = node->traverseNextNode()) {
		    if (!node->isElementNode())
		        continue;
		    element = static_cast<Element*>(node);
		    if (!keyMatches(key, element))
		        continue;
		    m_duplicateCounts.remove(key);
		    m_map.set(key, element);
		    return element;
		}
		ASSERT_NOT_REACHED();
	    }

	    return 0;
	}
e). In step 9 and 10 Node::removeChild is called which actually causes frm iframe to be removed and freed.
f). In step 11 DocumentOrderedMap::get(AtomicStringImpl* key, const TreeScope* scope) is called.
    Freed element frm iframe still exists in m_map which causes the use after free.


If any of the chrome engineers can log in to my pc using chrome remote desktop i can reproduce and show in chrome stable version.

### js...@chromium.org (2011-12-13)

[Empty comment from Monorail migration]

### ch...@gmail.com (2011-12-14)

Attached slightly modified reproduction case.

How to reproduce - NEW STEPS
-----------------------------

1. Copy all_reduced3.html and geo.html to same folder.
   THIS FOLDER SHOULD BE HOSTED BY LOCAL WEB SERVER AND YOU SHOULD ACCESS THE URL LIKE
   http:///127.0.0.1/all_reduced3.html. 
   IF WE ACCESS THIS FROM LOCAL FILE SYSTEM THIS WILL NOT WORK.
2. Deny permission to run plugins for 127.0.0.1 under chrome preferences.
3. Load 127.0.0.1/all_reduced3.html in chrome web browser.
4. SLOWLY KEEP MOVING THE MOUSE OVER APPLET.
5. Chrome will display sad tab.

Please try this on a slower machine if it does not reproduce on your developer machines. If this runs too fast it will not reproduce.

Please let me know if it does not reproduce.

### ch...@gmail.com (2011-12-18)

Is this error reproducible?

### js...@chromium.org (2011-12-20)

Sorry, but we've been unable to reproduce after repeated attempts on numerous platforms with ASAN and non-ASAN builds. Given that no one else has been able to trigger this condition I'm closing it out.


### ch...@gmail.com (2011-12-22)

I understand my reproduction case is not good enough. I also tried to make it simple so many times. Will it be possible to post a desktop recording, recorded while trying to reproduce this issue, please. I just want to see how fast the applet loads and unloads on your machine.

### ch...@gmail.com (2012-01-11)

Attached a test case which reproduces consistently and this test case does not need to move the mouse over applet as with previous test cases.

Steps
-----
1. Download and copy all_reduced4.html and geo.html to same folder and host them on local web server.
2. Open chrome. Load all_reduced4.html through web server. Loading as a file will not work.
3. Wait about 10 seconds. Chrome will display sad tab.

Reproduces on these versions
----------------------------

16.0.912.75 stable
18.0.1004.0 (Developer Build 117172 Linux)

If this test case also does not reproduce I would like to share my pc, so a chrome engineer can log in to my pc and check this issue.

### [Deleted User] (2012-01-11)

Heyo... It reproduces on trunk :)

Looks like a stale HTMLElement in the v8 bindings.

 WTF::RefPtr<WTF::StringImpl>::get()  Line 60 + 0x11 bytes	C++
 WTF::String::impl()  Line 142 + 0x16 bytes	C++
 WTF::AtomicString::impl()  Line 62 + 0x16 bytes	C++
 WebCore::createV8HTMLWrapper(WebCore::HTMLElement * element=0x0f65e790, bool forceNewObject=false)  Line 802 + 0xf bytes	C++
 WebCore::toV8(WebCore::HTMLElement * impl=0x0f65e790, bool forceNewObject=false)  Line 60 + 0x12 bytes	C++
 WebCore::toV8(WebCore::Element * impl=0x0f65e790, bool forceNewObject=false)  Line 61 + 0x1b bytes	C++
 WebCore::DocumentInternal::getElementByIdCallback(const v8::Arguments & args={...})  Line 1352 + 0x24 bytes	C++
 v8::internal::HandleApiCallHelper<0>(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args={...}, v8::internal::Isolate * isolate=0x0093a000)  Line 1220 + 0x13 bytes	C++
 v8::internal::Builtin_Impl_HandleApiCall(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args={...}, v8::internal::Isolate * isolate=0x0093a000)  Line 1237 + 0x11 bytes	C++
 v8::internal::Builtin_HandleApiCall(v8::internal::`anonymous-namespace'::BuiltinArguments<1> args={...}, v8::internal::Isolate * isolate=0x0093a000)  Line 1236 + 0x43 bytes	C++
 ...


Filed upstream as https://bugs.webkit.org/show_bug.cgi?id=76087


### ch...@gmail.com (2012-01-12)

Can I get access to view the webkit bug please? When I try to visit https://bugs.webkit.org/show_bug.cgi?id=76087 it says "You are not authorized to access bug".

### in...@chromium.org (2012-01-20)

Chamal, sorry for the late reply. Please register on bugs.webkit.org and let me know your email, I will then add you as cc.

Please note that this testcase in c#29 is not reduced, and will not qualify for the higher reward. Do you want to take a shot at minimizing this ?

### ch...@gmail.com (2012-01-20)

I am registered at webkit. My username email is chamalsl@yahoo.com in webkit.

I understand that my reproduction case is not good. I ll try my best to post a simple test case.

### ch...@gmail.com (2012-01-23)

[Comment Deleted]

### ch...@gmail.com (2012-01-23)

1. I was unable to further reduce the test case.
2. But I was able to reduce the test case to demonstrate the root cause of this bug.
   It is attached with this comment as root_cause.html.
3. As mentioned in https://crbug.com/chromium/105867#c11 the object used after being freed is iframe with id frm.
4. As mentioned in https://crbug.com/chromium/105867#c23, the root cause of this bug is frm iframe is added to  DocumentOrderedMap twice.
   Which causes frm iframe to be added to m_duplicateCounts set of DocumentOrderedMap. root_cause.html demonstrates this behavior.
   I assume m_duplicateCounts set is used when there are multiple elements with same id (Is my assumption correct?).In this test case there is only one element with id frm.
  We can confirm this behavior if we add this printf statement to third_party/WebKit/Source/WebCore/dom/TreeScope.cpp's addElementById method like this.

void TreeScope::addElementById(const AtomicString& elementId, Element* element)
{
	printf("TreeScope addElementById %s\n", elementId.string().utf8().data());

	if (strcmp(elementId.string().utf8().data(), "frm") == 0)
	{
		printf("TreeScope addElementById frm \n");
	}
    m_elementsById.add(elementId.impl(), element);
}

5. I think adding frm iframe twice to DocumentOrderedMap when there is only one element with id frm is a bug. Is it a correct?
   If this behavior (or bug) can be stopped then the crash bug mentioned with this report can be fixed.

 

### ch...@gmail.com (2012-01-23)

Regarding https://crbug.com/chromium/105867#c35
---------------------

1. frm iframe is added to DocumentOrderedMap first when document is loaded.
2. frm iframe is added to DocumentOrderedMap second as a result of appendChild call on sendEvent javascript method in root_cause.html file.
3. I think frm iframe is removed and added to document when appendChild call is executed.
4. But it is not removed from DocumentOrderedMap.
5. That is why frm iframe is added to  m_duplicateCounts set of DocumentOrderedMap.
This is the main cause of bug and if this can be fixed this bug can be fixed.
If my comment is not clear please tell me.

### js...@chromium.org (2012-01-23)

Could someone familiar with the v8 bindings take a look at this? It seems like we have a lifetime issue here, but the repro is not reliable and we've had no luck in tracking this down.

### in...@chromium.org (2012-01-23)

The last M16 patch is already gone. Mass-updating all of these to M17

### ch...@gmail.com (2012-01-24)

@jschuh 
Are my comments 35 and 36 clear? If not please tell me which parts are not clear?
If the root cause mentioned by https://crbug.com/chromium/105867#c35 and 36 can be fixed, then this issue can be fixed.


### ch...@gmail.com (2012-01-24)

As the fix I suggest modifying the ContainerNode::removeChild(Node* oldChild, ExceptionCode& ec) method of ContainerNode.cpp.
Attached ContainerNode_before_fix.cpp contains the contents of ContainerNode.cpp before fix.
Attached ContainerNode_after_fix.cpp contains the contents of ContainerNode.cpp after fix.
If you diff the files you can see the change I did to fix this issue.
This fix fixes this bug, but it may break existing code.
Can a chrome engineer check this proposed code change please?

### ch...@gmail.com (2012-01-24)

Proposed fix 2
---------------
Attached another possible fix.

### js...@chromium.org (2012-01-24)

Chamal, I appreciate you're enthusiasm but this is not the way to propose a fix. If you want to propose a patch in WebKit, then please follow the guidance here: http://www.webkit.org/coding/contributing.html

Before posting a patch for review, please make sure to run the layout tests and ensure your approach doesn't introduce any new regressions. In the case of these changes, I expect you will see numerous new test failures because they violate the mutation event standard.

### pa...@chromium.org (2012-01-25)

FWIW, I can't get root_cause.html to reproduce on 17 beta or trunk (both on Linux).

### ch...@gmail.com (2012-01-25)

palmer, root_cause.html does not crash. It just adds frm iframe to m_duplicateCounts set of DocumentOrderedMap, which is the cause of this bug.

### ch...@gmail.com (2012-01-26)

I think the fixes I proposed earlier introduces some new bugs. So I don't feel comfortable to submit a patch.


### pa...@chromium.org (2012-01-30)

I get this stack trace:

Program received signal SIGSEGV, Segmentation fault.
0x00007ffff27c9e56 in WTF::RefPtr<WTF::StringImpl>::get (
    this=0x363636363636365e)
    at third_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:60
60              T* get() const { return m_ptr; }
(gdb) bt
#0  0x00007ffff27c9e56 in WTF::RefPtr<WTF::StringImpl>::get (
    this=0x363636363636365e)
    at third_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:60
#1  0x00007ffff27c9414 in WTF::String::impl (this=0x363636363636365e)
    at third_party/WebKit/Source/JavaScriptCore/wtf/text/WTFString.h:142
#2  0x00007ffff27c95de in WTF::AtomicString::impl (this=0x363636363636365e)
    at third_party/WebKit/Source/JavaScriptCore/wtf/text/AtomicString.h:63
#3  0x00007ffff380b08c in WebCore::createV8HTMLWrapper (element=
    0x7fffe1a27120, forceNewObject=false)
    at out/Debug/obj/gen/webkit/V8HTMLElementWrapperFactory.cpp:820
#4  0x00007ffff32c010f in WebCore::toV8 (impl=0x7fffe1a27120, 
    forceNewObject=false)
    at third_party/WebKit/Source/WebCore/bindings/v8/custom/V8HTMLElementCustom.cpp:60
#5  0x00007ffff32c0004 in WebCore::toV8 (impl=0x7fffe1a27120, 
    forceNewObject=false)
    at third_party/WebKit/Source/WebCore/bindings/v8/custom/V8ElementCustom.cpp:61
#6  0x00007ffff3787b08 in WebCore::DocumentInternal::getElementByIdCallback (
    args=...) at out/Debug/obj/gen/webcore/bindings/V8Document.cpp:1375
#7  0x00007ffff21d5ce7 in v8::internal::HandleApiCallHelper<false> (args=..., 
    isolate=0x7fffefc03000) at v8/src/builtins.cc:1220
#8  0x00007ffff21d08e5 in v8::internal::Builtin_Impl_HandleApiCall (args=..., 
---Type <return> to continue, or q <return> to quit---
    isolate=0x7fffefc03000) at v8/src/builtins.cc:1237
#9  0x00007ffff21d08b6 in v8::internal::Builtin_HandleApiCall (args=..., 
    isolate=0x7fffefc03000) at v8/src/builtins.cc:1236
#10 0x000008f71b50420e in ?? ()
...

From what I can tell, the calls go: toV8, toV8, wrapper, deref bad pointer. japhet owns the two toV8 functions, so I'm assigning to him provisionally. Before that, in HandleApiCallHelper, is code owned by lrn and sgjesse, so CCing them in case they can inform us.

### sc...@gmail.com (2012-02-07)

@japhet: got time to take this one down this month? We'd love to get it fixed in an important security patch targeted for early March.

### sc...@gmail.com (2012-02-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2012-02-16)

Chatted with japhet and I said I'd take a look.  Can someone CC me on the WebKit bug (https://bugs.webkit.org/show_bug.cgi?id=76087)?

### sc...@gmail.com (2012-02-16)

Looks like someone took care of this (I see adamk@chromium.org)

### ad...@chromium.org (2012-02-17)

I've been looking at this, and it's definitely pretty hairy: I can reproduce the crash, but the number of involved elements (plugins + iframes + reloading) makes it hard to pin down. Will give it another go tomorrow.

### ch...@gmail.com (2012-02-17)

Adam, iframe with id frm is the one used after being freed.
I now understand a bit about why this error happens and I have tried to explain in my comments. Please see https://crbug.com/chromium/105867#c11, 23 and my other comments. If my comments are not clear please tell me. I ll try to explain a bit more.

### ad...@chromium.org (2012-02-17)

Uploaded patch (with tests) to WebKit bug.

### in...@chromium.org (2012-02-18)

http://trac.webkit.org/changeset/108152

### sc...@gmail.com (2012-02-18)

Thanks for taking this to completion, Adam! :D

### ad...@chromium.org (2012-02-22)

Note: the referenced WebKit change includes a bug. Please see https://bugs.webkit.org/show_bug.cgi?id=79162 (and probably also merge that change when it lands).

### in...@chromium.org (2012-02-22)

Okies, we will merge both http://trac.webkit.org/changeset/108152 and http://trac.webkit.org/changeset/108415 to m17.

### sc...@gmail.com (2012-03-01)

M17: http://trac.webkit.org/changeset/109354, http://trac.webkit.org/changeset/109355
M18: http://trac.webkit.org/changeset/109356, http://trac.webkit.org/changeset/109357

### sc...@gmail.com (2012-03-03)

@chamal: congrats! Your efforts to get us a good repro case finally came good so we'd like to reward you $1000. Thanks for persevering :)

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2012-03-03)

[Empty comment from Monorail migration]

### ch...@gmail.com (2012-03-03)

Thank you very much for the reward :)

### ch...@gmail.com (2012-03-13)

Sorry for troubling you. When can I receive the reward for this issue? :)

### sc...@gmail.com (2012-03-13)

We are just reworking our payments process, sorry for the delay. I will do yours first when we're back.

### ch...@gmail.com (2012-03-13)

Thanks a lot chris :)

### ch...@gmail.com (2012-03-23)

When can I receive the reward for this issue? :)

### sc...@gmail.com (2012-03-27)

Payment in flight for all three issues / $3000
Do let us know when it arrives safely.

### ch...@gmail.com (2012-04-04)

Received the money for all 3 issues today :)
Thanks a lot:)

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/105867?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051697)*
