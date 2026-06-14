# use after free due to floats not cleared (overflow)

| Field | Value |
|-------|-------|
| **Issue ID** | [40088277](https://issues.chromium.org/issues/40088277) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2011-02-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

continued from <https://crbug.com/chromium/73526>

**VERSION**  

Chrome Version:  

Chromium 11.0.682.0 (Developer Build f504cfe)  

WebKit 534.22 (git@58b0446) == r79479

**REPRODUCTION CASE**  

attached  

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:  

==12302== Address 0xf7d44ab is 91 bytes inside a block of size 96 free'd  

==12302== at 0x4C29146: free (vg\_replace\_malloc.c:913)  

==12302== by 0x1E3ECFF: WebCore::RenderObject::~RenderObject() (in /home/clooney/chromium/src/out/Release/chrome)  

==12302== by 0x1DF9156: WebCore::RenderEmbeddedObject::~RenderEmbeddedObject() (in /home/clooney/chromium/src/out/Release/chrome)  

==12302== by 0x1E3971A: WebCore::RenderObject::arenaDelete(WebCore::RenderArena\*, void\*) (in /home/clooney/chromium/src/out/Release/chrome)  

==12302==  

==12302== Jump to the invalid address stated on the next line  

==12302== at 0x0: ???  

==12302== by 0x1DC5968: WebCore::RenderBlock::insertFloatingObject(WebCore::RenderBox\*) (in /home/clooney/chromium/src/out/Release/chrome)  

==12302== by 0x1DE008D: WebCore::RenderBlock::layoutInlineChildren(bool, int&, int&) (in /home/clooney/chromium/src/out/Release/chrome)

## Attachments

- [134.html](attachments/134.html) (text/html; charset=us-ascii, 4.1 KB)
- [stillInserting.html](attachments/stillInserting.html) (text/plain; charset=us-ascii, 899 B)
- [73962.tbz2](attachments/73962.tbz2) (application/x-bzip2; charset=binary, 19.2 KB)
- [73962_and_then_017281118.html](attachments/73962_and_then_017281118.html) (text/html; charset=us-ascii, 29.2 KB)
- [73962_and_then_012266131.html](attachments/73962_and_then_012266131.html) (text/html; charset=us-ascii, 12.7 KB)
- [73962_and_then_005138659.html](attachments/73962_and_then_005138659.html) (application/octet-stream; charset=binary, 57.5 KB)
- [73962_and_then_032739559.html](attachments/73962_and_then_032739559.html) (application/octet-stream; charset=binary, 42.2 KB)
- [73962_and_then_037409112.html](attachments/73962_and_then_037409112.html) (application/octet-stream; charset=binary, 54.8 KB)
- [73962_and_then_022397075.html](attachments/73962_and_then_022397075.html) (text/html; charset=us-ascii, 103.6 KB)
- [73962_and_then_027756414.html](attachments/73962_and_then_027756414.html) (text/html; charset=us-ascii, 26.2 KB)
- [73962-repro.html](attachments/73962-repro.html) (text/plain; charset=us-ascii, 279 B)
- [73962-x.html](attachments/73962-x.html) (text/plain; charset=us-ascii, 362 B)
- [checkFloats73962.html](attachments/checkFloats73962.html) (text/plain; charset=us-ascii, 1.0 KB)

## Timeline

### mi...@gmail.com (2011-02-24)

33 additional repros

### mi...@gmail.com (2011-02-24)

more repros. these don't have the magical webkit-columns style

these may be completely different bugs too.  I'm having trouble binning these unfixed bugs that look the same.

### [Deleted User] (2011-02-24)

I was able to reproduce the crash with 134.html.

Load the file and refresh. If it doesn't crash, keep refreshing. In fact I see two crashes being logged here.

Stack Trace 1
--------------
Thread 0 *CRASHED* ( EXCEPTION_ACCESS_VIOLATION_EXEC @ 0x04641f88 )

0x04641f88			
0x67940c51	 [chrome.dll	 - renderblocklinelayout.cpp:870]	WebCore::RenderBlock::layoutInlineChildren(bool,int &,int &)
0x6790b537	 [chrome.dll	 - renderblock.cpp:1222]	WebCore::RenderBlock::layoutBlock(bool,int)
0x6790b22c	 [chrome.dll	 - renderblock.cpp:1120]	WebCore::RenderBlock::layout()
0x6790cc5a	 [chrome.dll	 - renderblock.cpp:1958]	WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox *,WebCore::RenderBlock::MarginInfo &,int &,int &)
0x6790ca86	 [chrome.dll	 - renderblock.cpp:1896]	WebCore::RenderBlock::layoutBlockChildren(bool,int &)
0x6790b547	 [chrome.dll	 - renderblock.cpp:1224]	WebCore::RenderBlock::layoutBlock(bool,int)
0x6790b22c	 [chrome.dll	 - renderblock.cpp:1120]	WebCore::RenderBlock::layout()
0x6790d12b	 [chrome.dll	 - renderblock.cpp:2137]	WebCore::RenderBlock::layoutPositionedObjects(bool)
0x6790b68b	 [chrome.dll	 - renderblock.cpp:1255]	WebCore::RenderBlock::layoutBlock(bool,int)
0x6790b22c	 [chrome.dll	 - renderblock.cpp:1120]	WebCore::RenderBlock::layout()
0x678ebdbd	 [chrome.dll	 - renderview.cpp:130]	WebCore::RenderView::layout()
0x66fcb419	 [chrome.dll	 - frameview.cpp:906]	WebCore::FrameView::layout(bool)
0x66fcd823	 [chrome.dll	 - frameview.cpp:2383]	WebCore::FrameView::updateLayoutAndStyleIfNeededRecursive()
0x674a0074	 [chrome.dll	 - render_widget.cc:563]	RenderWidget::DoDeferredUpdate()
0x674a0001	 [chrome.dll	 - render_widget.cc:541]	RenderWidget::CallDoDeferredUpdate()
0x674a1a0c	 [chrome.dll	 - ipc_message.h:136]	IPC::Message::Dispatch<RenderView,RenderView>(IPC::Message const *,RenderView *,RenderView *,void ( RenderView::*)(void))
0x6749f5c4	 [chrome.dll	 - render_widget.cc:165]	RenderWidget::OnMessageReceived(IPC::Message const &)
0x6746b7c5	 [chrome.dll	 - render_view.cc:1120]	RenderView::OnMessageReceived(IPC::Message const &)
0x677d1032	 [chrome.dll	 - message_router.cc:46]	MessageRouter::RouteMessage(IPC::Message const &)
0x677d1004	 [chrome.dll	 - message_router.cc:38]	MessageRouter::OnMessageReceived(IPC::Message const &)
0x677c1c05	 [chrome.dll	 - child_thread.cc:168]	ChildThread::OnMessageReceived(IPC::Message const &)
0x675e5644	 [chrome.dll	 - task.h:331]	RunnableMethod<ChromeAppCacheService,void ( ChromeAppCacheService::*)(GURL const &),Tuple1<GURL> >::Run()
0x67436115	 [chrome.dll	 - message_loop.cc:367]	MessageLoop::RunTask(Task *)
0x6743619c	 [chrome.dll	 - message_loop.cc:376]	MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const &)
0x67436549	 [chrome.dll	 - message_loop.cc:569]	MessageLoop::DoWork()
0x6744c1d1	 [chrome.dll	 - message_pump_default.cc:50]	base::MessagePumpDefault::Run(base::MessagePump::Delegate *)
0x67436096	 [chrome.dll	 - message_loop.cc:342]	MessageLoop::RunInternal()
0x6743601b	 [chrome.dll	 - message_loop.cc:315]	MessageLoop::RunHandler()
0x67435f0f	 [chrome.dll	 - message_loop.cc:239]	MessageLoop::Run()
0x674633f9	 [chrome.dll	 - renderer_main.cc:300]	RendererMain(MainFunctionParams const &)
0x66f74ad1	 [chrome.dll	 - chrome_main.cc:950]	ChromeMain
0x010d1b37	 [chrome.exe	 - client_util.cc:280]	MainDllLoader::Launch(HINSTANCE__ *,sandbox::SandboxInterfaceInfo *)
0x010d10e9	 [chrome.exe	 - chrome_exe_main_win.cc:46]	wWinMain
0x01119863	 [chrome.exe	 - crt0.c:263]	__tmainCRTStartup
0x75ce3676	 [kernel32.dll	 + 0x00013676]	BaseThreadInitThunk
0x77479f01	 [ntdll.dll	 + 0x00039f01]	__RtlUserThreadStart
0x77479ed4	 [ntdll.dll	 + 0x00039ed4]	_RtlUserThreadStart

Full report @ http://crash/reportdetail?reportid=ff931cf8dade2596

Stack Trace 2
--------------
Thread 0 *CRASHED* ( EXCEPTION_ACCESS_VIOLATION_READ @ 0x0000009c )

0x6790f352	 [chrome.dll	 - renderblock.cpp:3073]	WebCore::RenderBlock::insertFloatingObject(WebCore::RenderBox *)
0x67940c51	 [chrome.dll	 - renderblocklinelayout.cpp:870]	WebCore::RenderBlock::layoutInlineChildren(bool,int &,int &)
0x6790b537	 [chrome.dll	 - renderblock.cpp:1222]	WebCore::RenderBlock::layoutBlock(bool,int)
0x6790b22c	 [chrome.dll	 - renderblock.cpp:1120]	WebCore::RenderBlock::layout()
0x6790cc5a	 [chrome.dll	 - renderblock.cpp:1958]	WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox *,WebCore::RenderBlock::MarginInfo &,int &,int &)
0x6790ca86	 [chrome.dll	 - renderblock.cpp:1896]	WebCore::RenderBlock::layoutBlockChildren(bool,int &)
0x6790b547	 [chrome.dll	 - renderblock.cpp:1224]	WebCore::RenderBlock::layoutBlock(bool,int)
0x6790b22c	 [chrome.dll	 - renderblock.cpp:1120]	WebCore::RenderBlock::layout()
0x6790d12b	 [chrome.dll	 - renderblock.cpp:2137]	WebCore::RenderBlock::layoutPositionedObjects(bool)
0x6790b68b	 [chrome.dll	 - renderblock.cpp:1255]	WebCore::RenderBlock::layoutBlock(bool,int)
0x6790b22c	 [chrome.dll	 - renderblock.cpp:1120]	WebCore::RenderBlock::layout()
0x678ebdbd	 [chrome.dll	 - renderview.cpp:130]	WebCore::RenderView::layout()
0x66fcb419	 [chrome.dll	 - frameview.cpp:906]	WebCore::FrameView::layout(bool)
0x66fb0171	 [chrome.dll	 - document.cpp:2114]	WebCore::Document::implicitClose()
0x66f966f0	 [chrome.dll	 - frameloader.cpp:898]	WebCore::FrameLoader::checkCallImplicitClose()
0x66f965f5	 [chrome.dll	 - frameloader.cpp:846]	WebCore::FrameLoader::checkCompleted()
0x66f96e51	 [chrome.dll	 - frameloader.cpp:1209]	WebCore::FrameLoader::completed()
0x66f96609	 [chrome.dll	 - frameloader.cpp:850]	WebCore::FrameLoader::checkCompleted()
0x66f9b0fe	 [chrome.dll	 - frameloader.cpp:3306]	WebCore::FrameLoader::mainReceivedCompleteError(WebCore::DocumentLoader *,WebCore::ResourceError const &)
0x67000217	 [chrome.dll	 - documentloader.cpp:205]	WebCore::DocumentLoader::mainReceivedError(WebCore::ResourceError const &,bool)
0x66f9a02e	 [chrome.dll	 - frameloader.cpp:2843]	WebCore::FrameLoader::receivedMainResourceError(WebCore::ResourceError const &,bool)
0x671861c0	 [chrome.dll	 - utf8.cpp:275]	WTF::Unicode::convertUTF8ToUTF16(char const * *,char const *,wchar_t * *,wchar_t *,bool)
0x6718201e	 [chrome.dll	 - wtfstring.cpp:746]	WTF::String::fromUTF8(char const *,unsigned int)
0x6729e7b6	 [chrome.dll	 - weburlerror.cpp:66]	WebKit::WebURLError::operator WebCore::ResourceError()
0x67098d47	 [chrome.dll	 - mainresourceloader.cpp:84]	WebCore::MainResourceLoader::receivedError(WebCore::ResourceError const &)
0x67099751	 [chrome.dll	 - mainresourceloader.cpp:485]	WebCore::MainResourceLoader::didFail(WebCore::ResourceError const &)
0x67098a86	 [chrome.dll	 - resourceloader.cpp:445]	WebCore::ResourceLoader::didFail(WebCore::ResourceHandle *,WebCore::ResourceError const &)
0x672987a1	 [chrome.dll	 - resourcehandle.cpp:198]	WebCore::ResourceHandleInternal::didFail(WebKit::WebURLLoader *,WebKit::WebURLError const &)
0x67837d9f	 [chrome.dll	 - weburlloader_impl.cc:653]	webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest(net::URLRequestStatus const &,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &,base::Time const &)
0x677dcd00	 [chrome.dll	 - xhash:637]	stdext::_Hash<stdext::_Hmap_traits<int,NPObjectBase *,stdext::hash_compare<int,std::less<int> >,std::allocator<std::pair<int const ,NPObjectBase *> >,0> >::lower_bound(int const &)
...... (7 stack frames dropped.)
0x677c1b9d	 [chrome.dll	 - child_thread.cc:144]	ChildThread::OnMessageReceived(IPC::Message const &)
0x672ed84b	 [chrome.dll	 - ipc_channel_proxy.cc:235]	IPC::ChannelProxy::Context::AddFilter(IPC::ChannelProxy::MessageFilter *)
0x672ed859	 [chrome.dll	 - ipc_channel_proxy.cc:242]	IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const &)
0x675e5644	 [chrome.dll	 - task.h:331]	RunnableMethod<ChromeAppCacheService,void ( ChromeAppCacheService::*)(GURL const &),Tuple1<GURL> >::Run()
0x67436115	 [chrome.dll	 - message_loop.cc:367]	MessageLoop::RunTask(Task *)
0x6743619c	 [chrome.dll	 - message_loop.cc:376]	MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const &)
0x67436549	 [chrome.dll	 - message_loop.cc:569]	MessageLoop::DoWork()
0x6744c1d1	 [chrome.dll	 - message_pump_default.cc:50]	base::MessagePumpDefault::Run(base::MessagePump::Delegate *)
0x75cf9dd8	 [kernel32.dll	 + 0x00029dd8]	ReadProcessMemoryStub
0x67436096	 [chrome.dll	 - message_loop.cc:342]	MessageLoop::RunInternal()
0x681a4b0f	 [chrome.dll	 + 0x01234b0f]	
0x6743601b	 [chrome.dll	 - message_loop.cc:315]	MessageLoop::RunHandler()
0x67435f0f	 [chrome.dll	 - message_loop.cc:239]	MessageLoop::Run()
0x674633f9	 [chrome.dll	 - renderer_main.cc:300]	RendererMain(MainFunctionParams const &)
0x74646c64	 [ntmarta.dll	 + 0x00006c64]	AccGetSidFromToken
0x66f8fadb	 [chrome.dll	 - central_freelist.cc:220]	tcmalloc::CentralFreeList::RemoveRange(void * *,void * *,int)
0x66f8f245	 [chrome.dll	 - thread_cache.cc:149]	tcmalloc::ThreadCache::FetchFromCentralCache(unsigned int,unsigned int)
0x66f87f71	 [chrome.dll	 - thread_cache.h:346]	tcmalloc::ThreadCache::Allocate(unsigned int,unsigned int)
0x66f88f5a	 [chrome.dll	 - tcmalloc.cc:985]	`anonymous namespace'::do_malloc(unsigned int)

Full report @ http://crash/reportdetail?reportid=b6fd23806250c305

Renderer crash reproducible on Google Chrome 9.0.597.98 (Official Build 74359), 10.0.648.114 (Official Build 75702), 11.0.682.0 (Official Build 75806)

### mi...@gmail.com (2011-02-25)

@inferno: do you want still more repros?  I feel kind of silly, especially since I can't tell if a particular repro is related to this issue at all.  I have ~500 more.

### in...@chromium.org (2011-02-25)

Thanks miaubiz. Let me go through these first, i will let you know if i need more repros. 

### mi...@gmail.com (2011-02-25)

[Comment Deleted]

### in...@chromium.org (2011-02-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-26)

[Empty comment from Monorail migration]

### er...@chromium.org (2011-03-01)

We also see this crash in the wild.

For instance, loading this page:
  http://www.viciados-gc.com/

(I tested on Chrome 11, and it crashes with similar looking callstack: http://crash/reportdetail?reportid=a2ec2c3d09a11c70)


### mi...@gmail.com (2011-03-14)

have you had a chance to look at this yet?

### in...@chromium.org (2011-03-14)

We will. This is much harder to fix and one of the options we are considering is to just crash when such an integer overflow happens. A long term fix is to convert all height stuff to floats but take might take more time. we still need a short-term solution.

### la...@chromium.org (2011-03-19)

**VULNERABILITY DETAILS**  

continued from <https://crbug.com/chromium/73526>

**VERSION**  

Chrome Version:  

Chromium 11.0.682.0 (Developer Build f504cfe)  

WebKit 534.22 (git@58b0446) == r79479

**REPRODUCTION CASE**  

attached  

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:  

==12302== Address 0xf7d44ab is 91 bytes inside a block of size 96 free'd  

==12302== at 0x4C29146: free (vg\_replace\_malloc.c:913)  

==12302== by 0x1E3ECFF: WebCore::RenderObject::~RenderObject() (in /home/clooney/chromium/src/out/Release/chrome)  

==12302== by 0x1DF9156: WebCore::RenderEmbeddedObject::~RenderEmbeddedObject() (in /home/clooney/chromium/src/out/Release/chrome)  

==12302== by 0x1E3971A: WebCore::RenderObject::arenaDelete(WebCore::RenderArena\*, void\*) (in /home/clooney/chromium/src/out/Release/chrome)  

==12302==  

==12302== Jump to the invalid address stated on the next line  

==12302== at 0x0: ???  

==12302== by 0x1DC5968: WebCore::RenderBlock::insertFloatingObject(WebCore::RenderBox\*) (in /home/clooney/chromium/src/out/Release/chrome)  

==12302== by 0x1DE008D: WebCore::RenderBlock::layoutInlineChildren(bool, int&, int&) (in /home/clooney/chromium/src/out/Release/chrome)

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-04-08)

webkit bug - https://bugs.webkit.org/show_bug.cgi?id=57121

### sk...@chromium.org (2011-04-08)

@miaubiz: if you have repros for any crashes that you don't know what to do with, please send them to me. I can feed them into my fuzzer framework, which should identify and bucketize crashes and minimize the repro's automatically, so I can file them.

### mi...@gmail.com (2011-04-11)

here's another one.

it doesn't have any large numbers in it.

### mi...@gmail.com (2011-04-14)

can you check this one too, please

==6194==    at 0x0: ???
==6194==    by 0x1AA92FB: WebCore::RenderBlock::checkFloatsInCleanLine(WebCore::RootInlineBox*, WTF::Vector<WebCore::RenderBlock::FloatWithRect, 0ul>&, unsigned long&, bool&, bool&) (in /home/clooney/chromium/src/out/Release/chrome)


### sc...@gmail.com (2011-04-15)

[Empty comment from Monorail migration]

### mi...@gmail.com (2011-04-16)

is it fixed?

### sc...@gmail.com (2011-04-16)

Ohh... not yet. It is being worked on :)

### in...@chromium.org (2011-04-17)

Ok, so main fix is in place - http://trac.webkit.org/changeset/84096
there is a regression that it brought (currently in review) - https://bugs.webkit.org/show_bug.cgi?id=58736. Before picking that, we would need the temp rebaseline that mitz did in http://trac.webkit.org/changeset/84098. After mitz fixes the regression, then i will retest with all miaubiz testcase (also will ask miaubiz to run his overflow awesome fuzzer again) and then hopefully close this down. I would be very happy if no other crashes remain.


### mi...@gmail.com (2011-04-17)

looks like you managed to avoid using CRASH() after all.

let me know when it's ready and I'll go at it.  

### mi...@gmail.com (2011-04-17)

took a quick look and I can't repro with the original stuff but the checkFloatsInCleanLine stuff is still going to bad instruction pointers.

I might not be able to distinguish between that, and this bug, if they are different.

shall I upload repros to @skylined or someone else, or what should we do?

there's about ~50k repros.  they take about 2.5gigs but should compress pretty nicely, since it's mostly the same stuff in every file :D

example attached

### in...@chromium.org (2011-04-17)

Thank you Miaubiz for your enthusiasm. The webkit fix is still not uptaken by chromium [http://svnsearch.org/svnsearch/repos/CHROMIUM/search?logMessage=webkit%20roll&path=%2Ftrunk], we are still waiting for the next webkit roll. Once that completes [probably sometime tmrw], please try it on chromium trunk and upload a few repros with different stacktraces (problem here is many of the different repros will also crash with same stacktrace).

### in...@chromium.org (2011-04-17)

Sorry we still need to wait for https://bugs.webkit.org/show_bug.cgi?id=58736. Mitz introduced this regression, so we do need him to fix it and then uptake in chrome, before we do further testing.

### mi...@gmail.com (2011-04-17)

@inferno: I built with webkit git master branch (r84100) because I was over-eager.  

but will check back when 58736 gets fixed

### in...@chromium.org (2011-04-18)

ok, so webkit https://crbug.com/chromium/58736 is fixed in http://trac.webkit.org/changeset/84119.

So, merge sequence
1. http://trac.webkit.org/changeset/84096
2. http://trac.webkit.org/changeset/84098
3. http://trac.webkit.org/changeset/84119

Note that this is a very risky merge. touches an important area in floats.

Miaubiz, if you want to try, you can run your fuzzers on webkit trunk and please let us know (attach here) different looking crash testcases.

### mi...@gmail.com (2011-04-18)

Only thing that's still reproing with webkit trunk is the checkFloatsInCleanLine issue.


### in...@chromium.org (2011-04-18)

Thanks Miaubiz. Filed a new bug for the checkFloatsInCleanLine issue. http://code.google.com/p/chromium/issues/detail?id=79746

Closing this bug.

### sc...@gmail.com (2011-05-02)

We'll let these just roll into M12 (which branched at WebKit r84325)

### sc...@gmail.com (2011-06-02)

@miaubiz -- thanks for great work in this bug and also 79746. We'll reward them separately. $1000 for this one; thanks for all the help and back-and-forth, valgrind analysis appreciated as always.

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

### sc...@gmail.com (2011-06-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-09)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/73962?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/74289]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088277)*
