# Invalid pointer write in GrGpu::clear

| Field | Value |
|-------|-------|
| **Issue ID** | [40076364](https://issues.chromium.org/issues/40076364) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2012-09-27 |
| **Bounty** | $1,000.00 |

## Description


Tested with: 

OS: Windows 7 x64
Graphics: Intel(R) HD Graphics 4000
Chrome 24.0.1279.0 (158985) canary

This issue needs two files in a row to be loaded into an iframe. I have created a runner html-file to help in reproducing this issue. All the needed files are in the attached zip-file.

I haven't been testing on Windows in long time so this crash might be because of old information about Chrome and page-heap compatibility/usage.

Page-heap command:

gflags.exe /p /enable chrome.exe /full

I also have set env-variable CHROME_ALLOCATOR to value winheap

Used commandline-flags while testing:

--user-data-dir=C:/tmp/chrome-prof 
--no-sandbox 
--disable-plugins 
--allow-file-access-from-files
 
Windbg-report from dump-file:

FAULTING_IP: 
chrome_5f2d0000!GrGpu::clear+c0 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grgpu.cpp @ 231]
5f8d6643 f00fc108        lock xadd dword ptr [eax],ecx

EXCEPTION_RECORD:  ffffffff -- (.exr 0xffffffffffffffff)
ExceptionAddress: 5f8d6643 (chrome_5f2d0000!GrGpu::clear+0x000000c0)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 0bdbaf9c
Attempt to write to address 0bdbaf9c

BUGCHECK_STR:  APPLICATION_FAULT_ONE_BIT_INVALID_POINTER_WRITE_EXPLOITABLE_FILL_PATTERN_c0c0c0c0

PRIMARY_PROBLEM_CLASS:  ONE_BIT_EXPLOITABLE_FILL_PATTERN_c0c0c0c0

DEFAULT_BUCKET_ID:  ONE_BIT_EXPLOITABLE_FILL_PATTERN_c0c0c0c0

STACK_TEXT:  
chrome_5f2d0000!GrGpu::clear+0xc0 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grgpu.cpp @ 231]
chrome_5f2d0000!GrInOrderDrawBuffer::playback+0x33f [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grinorderdrawbuffer.cpp @ 593]
chrome_5f2d0000!GrContext::resolveRenderTarget+0x2c [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grcontext.cpp @ 1450]
chrome_5f2d0000!SkGpuDevice::flush+0x22 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\skgpudevice.cpp @ 1894]
chrome_5f2d0000!`anonymous namespace'::FilterBufferState::swap+0xb [c:\b\build\slave\win\build\src\cc\ccrendersurfacefilters.cpp @ 289]
chrome_5f2d0000!cc::CCRenderSurfaceFilters::apply+0x3a8 [c:\b\build\slave\win\build\src\cc\ccrendersurfacefilters.cpp @ 439]
chrome_5f2d0000!cc::applyFilters+0xa1 [c:\b\build\slave\win\build\src\cc\ccrenderergl.cpp @ 343]
chrome_5f2d0000!cc::CCRendererGL::drawRenderPassQuad+0x24c [c:\b\build\slave\win\build\src\cc\ccrenderergl.cpp @ 443]
chrome_5f2d0000!cc::CCRendererGL::drawQuad+0x98 [c:\b\build\slave\win\build\src\cc\ccrenderergl.cpp @ 262]
chrome_5f2d0000!cc::CCDirectRenderer::drawRenderPass+0x1d0 [c:\b\build\slave\win\build\src\cc\ccdirectrenderer.cpp @ 185]
chrome_5f2d0000!cc::CCDirectRenderer::drawFrame+0x103 [c:\b\build\slave\win\build\src\cc\ccdirectrenderer.cpp @ 166]
chrome_5f2d0000!cc::CCLayerTreeHostImpl::drawLayers+0xbd [c:\b\build\slave\win\build\src\cc\cclayertreehostimpl.cpp @ 569]
chrome_5f2d0000!cc::CCSingleThreadProxy::doComposite+0x67 [c:\b\build\slave\win\build\src\cc\ccsinglethreadproxy.cpp @ 365]
chrome_5f2d0000!cc::CCSingleThreadProxy::commitAndComposite+0x9c [c:\b\build\slave\win\build\src\cc\ccsinglethreadproxy.cpp @ 339]
chrome_5f2d0000!cc::CCSingleThreadProxy::compositeImmediately+0x8 [c:\b\build\slave\win\build\src\cc\ccsinglethreadproxy.cpp @ 291]
chrome_5f2d0000!WebKit::WebViewImpl::composite+0x3e [c:\b\build\slave\win\build\src\third_party\webkit\source\webkit\chromium\src\webviewimpl.cpp @ 1828]
.
.
.
(btw, I'm using !exploitable crash analyzer extension in windbg so don't freak out with the EXPLOITABLE notes in the windbg analysis :D )



## Attachments

- [repro.zip](attachments/repro.zip) (application/zip; charset=binary, 1.3 KB)

## Timeline

### [Deleted User] (2012-09-27)

Setting flags to get the ball rolling

### at...@gmail.com (2012-09-27)

The run.html nor the individual html-files have no effect on Ubuntu 12.04 x86_64 with ASAN-built Chromium 24.0.1280.0 (Developer Build 159054) 


### [Deleted User] (2012-09-27)

I haven't been able to get this to repro on Windows or Linux.

Can you guys take a look and see if you have better luck or can suggest an owner.

### [Deleted User] (2012-09-27)

https://cluster-fuzz.appspot.com/testcase?key=115341512

### dh...@google.com (2012-09-28)

I see this crash in Windows - https://crash.corp.google.com/reportdetail?reportid=2a5c4b3489f8f12c

Thread 0 *CRASHED* ( EXCEPTION_ACCESS_VIOLATION_WRITE @ 0x1db4ef9c )

0x68762ad8	 [chrome.dll]	 - grgpu.cpp:231 (cs|src)]	GrGpu::clear(SkIRect const *,unsigned int,GrRenderTarget *)
0x6876a536	 [chrome.dll]	 - grinorderdrawbuffer.cpp:592 (cs|src)]	GrInOrderDrawBuffer::playback(GrDrawTarget *)
0x687471ec	 [chrome.dll]	 - grcontext.cpp:1450 (cs|src)]	GrContext::resolveRenderTarget(GrRenderTarget *)
0x68c73880	 [chrome.dll]	 - skgpudevice.cpp:1894 (cs|src)]	SkGpuDevice::flush()
0x69bac793	 [chrome.dll]	 - ccrendersurfacefilters.cpp:288 (cs|src|ann)]	`anonymous namespace'::FilterBufferState::swap()
0x69bacc08	 [chrome.dll]	 - ccrendersurfacefilters.cpp:439 (cs|src|ann)]	cc::CCRenderSurfaceFilters::apply(WebKit::WebFilterOperations const &,unsigned int,cc::FloatSize const &,WebKit::WebGraphicsContext3D *,GrContext *)
0x69ba3a8a	 [chrome.dll]	 - ccrenderergl.cpp:343 (cs|src|ann)]	cc::applyFilters
0x69ba81a1	 [chrome.dll]	 - ccrenderergl.cpp:443 (cs|src|ann)]	cc::CCRendererGL::drawRenderPassQuad(cc::CCDirectRenderer::DrawingFrame &,cc::CCRenderPassDrawQuad const *)
0x69ba882b	 [chrome.dll]	 - ccrenderergl.cpp:261 (cs|src|ann)]	cc::CCRendererGL::drawQuad(cc::CCDirectRenderer::DrawingFrame &,cc::CCDrawQuad const *)
0x69bab671	 [chrome.dll]	 - ccdirectrenderer.cpp:200 (cs|src|ann)]	cc::CCDirectRenderer::drawRenderPass(cc::CCDirectRenderer::DrawingFrame &,cc::CCRenderPass const *)
0x69bab9bd	 [chrome.dll]	 - ccdirectrenderer.cpp:176 (cs|src|ann)]	cc::CCDirectRenderer::drawFrame(WTF::Vector<cc::CCRenderPass *,0> const &,WTF::HashMap<cc::CCRenderPass::Id,WTF::OwnPtr<cc::CCRenderPass>,WTF::IntHash<cc::CCRenderPass::Id>,WTF::HashTraits<cc::CCRenderPass::Id>,WTF::HashTraits<WTF::OwnPtr<cc::CCRenderPass> > > const &)
0x69b90a1e	 [chrome.dll]	 - cclayertreehostimpl.cpp:569 (cs|src|ann)]	cc::CCLayerTreeHostImpl::drawLayers(cc::CCLayerTreeHostImpl::FrameData const &)
0x69b8c557	 [chrome.dll]	 - ccsinglethreadproxy.cpp:356 (cs|src|ann)]	cc::CCSingleThreadProxy::doComposite()
0x69b8cb03	 [chrome.dll]	 - ccsinglethreadproxy.cpp:330 (cs|src|ann)]	cc::CCSingleThreadProxy::commitAndComposite()
0x69b8cbf0	 [chrome.dll]	 - ccsinglethreadproxy.cpp:283 (cs|src|ann)]	cc::CCSingleThreadProxy::compositeImmediately()
0x69436c7e	 [chrome.dll]	 - webviewimpl.cpp:1828 (cs|src|ann)]	WebKit::WebViewImpl::composite(bool)
0x6826318e	 [chrome.dll]	 - render_widget.cc:1020 (cs|src|ann)]	RenderWidget::DoDeferredUpdate()
0x6832ffc1	 [chrome.dll]	 - render_widget.cc:833 (cs|src|ann)]	RenderWidget::DoDeferredUpdateAndSendInputAck()
0x6832ff64	 [chrome.dll]	 - render_widget.cc:829 (cs|src|ann)]	RenderWidget::InvalidationCallback()
0x6832ff03	 [chrome.dll]	 - bind_internal.h:870 (cs|src|ann)]	base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void ( RenderWidget::*)(void)>,void (RenderWidget * const &)>::MakeItSo(base::internal::RunnableAdapter<void ( RenderWidget::*)(void)>,RenderWidget * const &)
0x6832fee1	 [chrome.dll]	 - bind_internal.h:1172 (cs|src|ann)]	base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void ( RenderWidget::*)(void)>,void (RenderWidget *),void (RenderWidget *)>,void (RenderWidget *)>::Run(base::internal::BindStateBase *)
0x68194821	 [chrome.dll]	 - message_loop.cc:470 (cs|src|ann)]	MessageLoop::RunTask(base::PendingTask const &)
0x6819445b	 [chrome.dll]	 - message_loop.cc:661 (cs|src|ann)]	MessageLoop::DoWork()
0x68194bce	 [chrome.dll]	 - message_pump_default.cc:28 (cs|src|ann)]	base::MessagePumpDefault::Run(base::MessagePump::Delegate *)
0x68194126	 [chrome.dll]	 - message_loop.cc:427 (cs|src|ann)]	MessageLoop::RunInternal()
0x6819407e	 [chrome.dll]	 - run_loop.cc:45 (cs|src|ann)]	base::RunLoop::Run()
0x681c2cf2	 [chrome.dll]	 - message_loop.cc:307 (cs|src|ann)]	MessageLoop::Run()
0x681e02b3	 [chrome.dll]	 - renderer_main.cc:239 (cs|src|ann)]	RendererMain(content::MainFunctionParams const &)
0x681785a0	 [chrome.dll]	 - content_main_runner.cc:441 (cs|src|ann)]	content::RunNamedProcessTypeMain(std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &,content::MainFunctionParams const &,content::ContentMainDelegate *)
0x68178527	 [chrome.dll]	 - content_main_runner.cc:734 (cs|src|ann)]	content::ContentMainRunnerImpl::Run()
0x6816a5ef	 [chrome.dll]	 - content_main.cc:35 (cs|src|ann)]	content::ContentMain(HINSTANCE__ *,sandbox::SandboxInterfaceInfo *,content::ContentMainDelegate *)
0x6816a57b	 [chrome.dll]	 - chrome_main.cc:28 (cs|src|ann)]	ChromeMain
0x01227482	 [chrome.exe]	 - client_util.cc:440 (cs|src|ann)]	MainDllLoader::Launch(HINSTANCE__ *,sandbox::SandboxInterfaceInfo *)
0x012264c3	 [chrome.exe]	 - chrome_exe_main_win.cc:76 (cs|src|ann)]	RunChrome(HINSTANCE__ *)
0x0122652e	 [chrome.exe]	 - chrome_exe_main_win.cc:92 (cs|src|ann)]	wWinMain
0x012800e2	 [chrome.exe]	 - crt0.c:275]	__tmainCRTStartup
0x74eb3399	 [kernel32.dll]	 + 0x00013399]	BaseThreadInitThunk
0x77039ef1	 [ntdll.dll]	 + 0x00039ef1]	__RtlUserThreadStart
0x77039ec4	 [ntdll.dll]	 + 0x00039ec4]	_RtlUserThreadStart

### dh...@google.com (2012-09-28)

I didn't personally repro it but saw these crashes in crash server starting from 1278.0

### [Deleted User] (2012-09-28)

I am able to reproduce this on Windows.

### [Deleted User] (2012-09-28)

So ... it looks like a texture Chrome hands to Skia is being deleted before Skia gets around to using it. The problem appears to be occurring when the brightness SVG filter is being applied to a CSS layer so I think Stephen may have more insight into the problem (maybe we are missing a flush?). Here is the stack trace I am seeing with the --single-process flag in a Debug build:

 	chrome.dll!_wassert(const wchar_t * expr, const wchar_t * filename, unsigned int lineno)  Line 325	C
 	chrome.dll!gpu::Logger::~Logger()  Line 20 + 0x15 bytes	C++
 	chrome.dll!gpu::Logger::CheckTrue<bool>(const bool & x, const char * file, int line, const char * x_name, const char * check_name)  Line 50 + 0x90 bytes	C++
 	chrome.dll!gpu::gles2::StrictIdHandler::MarkAsUsedForBind(unsigned int id)  Line 74 + 0x62 bytes	C++
 	chrome.dll!gpu::gles2::ThreadSafeIdHandlerWrapper::MarkAsUsedForBind(unsigned int id)  Line 188 + 0x19 bytes	C++
 	chrome.dll!gpu::gles2::GLES2Implementation::BindTextureHelper(unsigned int target, unsigned int texture)  Line 2442 + 0x20 bytes	C++
 	chrome.dll!gpu::gles2::GLES2Implementation::BindTexture(unsigned int target, unsigned int texture)  Line 67	C++
 	chrome.dll!GLES2BindTexture(unsigned int target, unsigned int texture)  Line 33	C++
 	chrome.dll!GrGpuGL::flushBoundTextureAndParams(int stage, const GrTextureParams & params, GrGLTexture * nextTexture)  Line 2046 + 0x49 bytes	C++
 	chrome.dll!GrGpuGL::flushBoundTextureAndParams(int stage)  Line 2028	C++
 	chrome.dll!GrGpuGL::flushGraphicsState(GrGpu::DrawType type)  Line 406	C++
 	chrome.dll!GrGpu::setupClipAndFlushState(GrGpu::DrawType type)  Line 347 + 0x16 bytes	C++
 	chrome.dll!GrGpu::onDrawNonIndexed(GrPrimitiveType type, int startVertex, int vertexCount)  Line 406 + 0x15 bytes	C++
 	chrome.dll!GrDrawTarget::drawNonIndexed(GrPrimitiveType type, int startVertex, int vertexCount)  Line 782 + 0x1b bytes	C++
 	chrome.dll!GrInOrderDrawBuffer::playback(GrDrawTarget * target)  Line 570	C++
 	chrome.dll!GrInOrderDrawBuffer::flushTo(GrDrawTarget * target)  Line 99 + 0xc bytes	C++
 	chrome.dll!GrContext::flushDrawBuffer()  Line 1176	C++
 	chrome.dll!GrContext::flush(int flagsBitfield)  Line 1159	C++
 	chrome.dll!GrContext::resolveRenderTarget(GrRenderTarget * target)  Line 1454	C++
 	chrome.dll!SkGpuDevice::flush()  Line 1937	C++
 	chrome.dll!SkCanvas::flush()  Line 541 + 0x12 bytes	C++
>	chrome.dll!`anonymous namespace'::FilterBufferState::swap()  Line 308	C++
 	chrome.dll!WebCore::CCRenderSurfaceFilters::apply(const WebKit::WebFilterOperations & filters, unsigned int textureId, const WebCore::FloatSize & size, WebKit::WebGraphicsContext3D * context3D, GrContext * grContext)  Line 458	C++
 	chrome.dll!WebCore::applyFilters(WebCore::CCRendererGL * renderer, const WebKit::WebFilterOperations & filters, WebCore::CCScopedTexture * sourceTexture)  Line 364 + 0x36 bytes	C++
 	chrome.dll!WebCore::CCRendererGL::drawRenderPassQuad(WebCore::CCDirectRenderer::DrawingFrame & frame, const WebCore::CCRenderPassDrawQuad * quad)  Line 464 + 0x1d bytes	C++
 	chrome.dll!WebCore::CCRendererGL::drawQuad(WebCore::CCDirectRenderer::DrawingFrame & frame, const WebCore::CCDrawQuad * quad)  Line 283	C++
 	chrome.dll!WebCore::CCDirectRenderer::drawRenderPass(WebCore::CCDirectRenderer::DrawingFrame & frame, const WebCore::CCRenderPass * renderPass)  Line 186 + 0x26 bytes	C++
 	chrome.dll!WebCore::CCDirectRenderer::drawFrame(const WTF::Vector<WebCore::CCRenderPass *,0> & renderPassesInDrawOrder, const WTF::HashMap<int,WTF::OwnPtr<WebCore::CCRenderPass>,WTF::IntHash<unsigned int>,WTF::HashTraits<int>,WTF::HashTraits<WTF::OwnPtr<WebCore::CCRenderPass> > > & renderPassesById)  Line 162 + 0x21 bytes	C++
 	chrome.dll!WebCore::CCLayerTreeHostImpl::drawLayers(const WebCore::CCLayerTreeHostImpl::FrameData & frame)  Line 569 + 0x2b bytes	C++
 	chrome.dll!WebCore::CCSingleThreadProxy::doComposite()  Line 339 + 0x21 bytes	C++
 	chrome.dll!WebCore::CCSingleThreadProxy::commitAndComposite()  Line 313 + 0x8 bytes	C++
 	chrome.dll!WebCore::CCSingleThreadProxy::compositeImmediately()  Line 281 + 0x8 bytes	C++
 	chrome.dll!WebCore::CCLayerTreeHost::composite()  Line 445	C++
 	chrome.dll!WebKit::WebLayerTreeViewImpl::composite()  Line 173	C++
 	chrome.dll!WebKit::WebViewImpl::composite(bool __formal)  Line 1831 + 0x20 bytes	C++
 	chrome.dll!RenderWidget::DoDeferredUpdate()  Line 1010 + 0x19 bytes	C++
 	chrome.dll!RenderWidget::DoDeferredUpdateAndSendInputAck()  Line 825	C++
 	chrome.dll!RenderWidget::InvalidationCallback()  Line 820	C++
 	chrome.dll!base::internal::RunnableAdapter<void (__thiscall RenderWidget::*)(void)>::Run(RenderWidget * object)  Line 134 + 0x25 bytes	C++
 	chrome.dll!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall RenderWidget::*)(void)>,void __cdecl(RenderWidget * const &)>::MakeItSo(base::internal::RunnableAdapter<void (__thiscall RenderWidget::*)(void)> runnable, RenderWidget * const & a1)  Line 871	C++
 	chrome.dll!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall RenderWidget::*)(void)>,void __cdecl(RenderWidget *),void __cdecl(RenderWidget *)>,void __cdecl(RenderWidget *)>::Run(base::internal::BindStateBase * base)  Line 1172 + 0x33 bytes	C++
 	chrome.dll!base::Callback<void __cdecl(void)>::Run()  Line 389 + 0xe bytes	C++
 	chrome.dll!MessageLoop::RunTask(const base::PendingTask & pending_task)  Line 462	C++
 	chrome.dll!MessageLoop::DeferOrRunPendingTask(const base::PendingTask & pending_task)  Line 475	C++
 	chrome.dll!MessageLoop::DoWork()  Line 648 + 0xc bytes	C++
 	chrome.dll!base::MessagePumpForUI::DoRunLoop()  Line 239 + 0x1d bytes	C++
 	chrome.dll!base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate, base::MessagePumpDispatcher * dispatcher)  Line 64 + 0xf bytes	C++
 	chrome.dll!base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate)  Line 47 + 0x1c bytes	C++
 	chrome.dll!MessageLoop::RunInternal()  Line 419 + 0x29 bytes	C++
 	chrome.dll!MessageLoop::RunHandler()  Line 393	C++
 	chrome.dll!base::RunLoop::Run()  Line 46	C++
 	chrome.dll!MessageLoop::Run()  Line 300	C++
 	chrome.dll!base::Thread::Run(MessageLoop * message_loop)  Line 134	C++
 	chrome.dll!base::Thread::ThreadMain()  Line 169 + 0x16 bytes	C++
 	chrome.dll!base::`anonymous namespace'::ThreadFunc(void * params)  Line 59 + 0xe bytes	C++
 	kernel32.dll!748e339a() 	
 	[Frames below may be incorrect and/or missing, no symbols loaded for kernel32.dll]	
 	ntdll.dll!770f9ef2() 	
 	ntdll.dll!770f9ec5() 	


### se...@chromium.org (2012-09-28)

[Empty comment from Monorail migration]

### se...@chromium.org (2012-09-28)

Can repro the crash in Mac canary (r159213).

Bisecting gives me the range http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog.html?url=/trunk/src&range=157975%3A157988

which includes a Skia roll r5594:r5633:

http://src.chromium.org/viewvc/chrome?view=rev&revision=157977



### se...@chromium.org (2012-09-28)

Bisecting on Win gives this narrower range:    http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog.html?url=/tru
nk/src&range=157970%3A157980

### se...@chromium.org (2012-09-28)

Whoops, fixed URL:  http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog.html?url=%2Ftrunk%2Fsrc&range=157970:157980

Intersecting the two gives 157975:157980.

### se...@chromium.org (2012-09-28)

I don't see a crash on Linux, although I do see this:

[27311:27311:0928/170207:ERROR:gles2_cmd_decoder.cc(5176)] RENDER WARNING: texture bound to texture unit 0 is not renderable. It maybe non-power-of-2 and have  incompatible texture filtering or is not 'texture complete'

(note that this is with "Override software rendering list" to get accelerated canvas).

### se...@chromium.org (2012-09-28)

Note:  Enabling threaded compositing makes the crash go away on Win and Mac, and makes the above error message go away on Linux.  I suspect this is because filters do not re-use the SharedGraphicsContext3D (the one used by canvas) when the threaded compositor is enabled, so there are no conflicts between filters and canvas.

### se...@chromium.org (2012-09-28)

As a workaround, we could use the same filter context as threaded compositing does, even when single-threaded (ie., not share the canvas context), but it would be nice to know how this is getting broken.  Something about flushing the SkCanvas is hinky (which should only be used for filters, but perhaps has some stale canvas commands in it?  maybe a draw of a deleted bitmap or something?).

### [Deleted User] (2012-09-28)

There appear to be two bugs.

1) Ganesh has a ref count issue. When clearing a render target that is not the last RT rendered into we may incorrectly delete the previous RT.

2) The texture id passed to CCRenderSurfaceFilters::apply is invalid by the time Ganesh goes to draw from it. I'm not sure if it was already deleted before CCRenderSurfaceFilters was invoked.

I'm preparing a Skia patch for 1) now.



### [Deleted User] (2012-09-28)

Patch for 1) up at https://codereview.appspot.com/6584043



### sc...@gmail.com (2012-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2012-09-28)

I see some warning logs:

[14124:19624:0928/174124:ERROR:gles2_cmd_decoder.cc(5222)] RENDER WARNING: texture bound to texture unit 0 is not renderable. It maybe non-power-of-2 and have  incompatible texture filtering or is not 'texture complete'


### se...@chromium.org (2012-09-28)

#19:  see #13

### se...@chromium.org (2012-09-28)

Enne, James:  Any idea why the compositor would hand the filters a bad texture?  (see Brian's #2 in https://crbug.com/chromium/152707#c16)

Having trouble bisecting this part, since the warning doesn't appear during a bisect, for some reason (stderr hidden?)

### in...@chromium.org (2012-10-01)

[Empty comment from Monorail migration]

### se...@chromium.org (2012-10-01)

Total speculation:  the canvas (and its backing store) have been destroyed, but the compositor is still attempting to draw it, so it hands the dead canvas texture to filters.  Maybe the check for a dead texture comes too late for RenderSurface to know about it.  I'll try sticking in some printfs and/or tracing to test this theory.

Brian, with your fix, is the crash gone and only the warning remains?

### [Deleted User] (2012-10-01)

That should be the case. Brian's fix rolled into Chrome at r159475.

### se...@chromium.org (2012-10-01)

Printfs don't bear the theory out:  it seems that the filters are being applied to a non-canvas texture which is invalid the first time, but becomes valid after the first draw.  Two accelerated ImageBuffers are created, with two associated textures; both are destroyed before the first filter draw.  The filters are applied to some other texture (perhaps the pre-rendered RenderSurface?  or a compositor tile?)

0x7fe4bbd33b80:  ImageBuffer::ImageBuffer()
createAcceleratedCanvas() created texture 1
0x7fe4bbd33680:  ImageBuffer::ImageBuffer()
createAcceleratedCanvas() created texture 2
0x7fe4bbd33680:  ImageBuffer::~ImageBuffer()
Canvas2DLayerBridge::~Canvas2DLayerBridge()
texture was 2
0x7fe4bbd33b80:  ImageBuffer::~ImageBuffer()
Canvas2DLayerBridge::~Canvas2DLayerBridge()
texture was 1
applyFilters(), contentsTexture is 70
CCRenderSurfaceFilters::apply() to texture 70
[6607:6607:1001/112831:ERROR:gles2_cmd_decoder.cc(5176)] RENDER WARNING: texture bound to texture unit 0 is not renderable. It maybe non-power-of-2 and have  incompatible texture filtering or is not 'texture complete'
applyFilters(), contentsTexture is 70
CCRenderSurfaceFilters::apply() to texture 70
applyFilters(), contentsTexture is 70
CCRenderSurfaceFilters::apply() to texture 70

Adding some more printfs to figure out where this texture is created.

### se...@chromium.org (2012-10-01)

Bad texture seems to be allocated by CCResourceProvider::createGLTexture():

0x7fc8b3666b80:  ImageBuffer::ImageBuffer()
createAcceleratedCanvas() created texture 1
0x7fc8b3666680:  ImageBuffer::ImageBuffer()
createAcceleratedCanvas() created texture 2
0x7fc8b3666680:  ImageBuffer::~ImageBuffer()
Canvas2DLayerBridge::~Canvas2DLayerBridge()
texture was 2
0x7fc8b3666b80:  ImageBuffer::~ImageBuffer()
Canvas2DLayerBridge::~Canvas2DLayerBridge()
texture was 1
CCResourceProvider::createGLTexture() 1
CCResourceProvider::createGLTexture() 2
CCResourceProvider::createGLTexture() 3
CCResourceProvider::createGLTexture() 4
CCResourceProvider::createGLTexture() 5
[...]
CCResourceProvider::createGLTexture() 70
applyFilters(), contentsTexture is 70
sourceTexture id is 70
lock texture id is 70
CCRenderSurfaceFilters::apply() to texture 70
[8909:8909:1001/115132:ERROR:gles2_cmd_decoder.cc(5176)] RENDER WARNING: texture bound to texture unit 0 is not renderable. It maybe non-power-of-2 and have  incompatible texture filtering or is not 'texture complete'

### se...@chromium.org (2012-10-01)

Hmm; I take it back.  It's likely not to be 70, since that's the source texture and unlikely to be bound as a render target (unless something's uberbroken).  I'll sync past Brian's change and see if I still see this error, then see who's binding what.

### se...@chromium.org (2012-10-01)

More notes:  sticking a flush on the compositor context anywhere in drawRenderPassQuad() (even at the end of the function) seems to make the warning go away.  Note that the filters code flushes its context prior to returning, so this isn't a case of not flushing before a cross-context texture draw.

### se...@chromium.org (2012-10-01)

Curiouser and curiouser:  if I flush the compositor context after drawRenderPassQuad() returns, it *doesn't* make the warning go away.

Narrowing it down a bit further:  it seems that it's the SkBitmap destructor:  if I flush the compositor context before the SkBitmap is destroyed, the warning goes away.

(This is the texture-backed SkBitmap that holds the result of filtering).

Not sure why flushing the compositor context affects Ganesh, though.

### se...@chromium.org (2012-10-02)

Another WAG:  skia is deleting the filtered texture in the SkBitmap destructor (in Skia's GL context), so flushing the compositor context forces it to draw, just in case skia's context gets handled by the GPU process before the compositor's context does.

OTOH, I don't think skia should be deleting the texture, since it's a scratch texture that should just go back to cache.  Also, it also shouldn't be binding that texture as an FBO, so the warning doesn't make sense.  (It would be helpful if the warning printed the textureID, and ideally the client-side one, not the service-side one.)

At this point I'm kind of flailing and out of ideas, and since the crashing bug appears to be fixed with Brian's change, I'm tempted to unown this and lower its priority.

### se...@chromium.org (2012-10-03)

I've opened http://crbug.com/153776 to track the warning.  Marking this one as fixed.

### se...@chromium.org (2012-10-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-03)

Does it need merging to m23, m22 branches ?

### [Deleted User] (2012-10-03)

Yes and yes. I'll merge the fix to the two Skia branches.

### in...@chromium.org (2012-10-03)

[Empty comment from Monorail migration]

### [Deleted User] (2012-10-03)

The merges are in.

M22: http://code.google.com/p/skia/source/detail?r=5790
M23: http://code.google.com/p/skia/source/detail?r=5791

### sc...@gmail.com (2012-10-03)

cc: @kerz to make sure it was ok to merge to the M22 branch at this time.

### [Deleted User] (2012-10-04)

Apologies if I jumped the gone on that. I'll revert if we don't want it in M22. The fix is very safe IMO.

### sc...@gmail.com (2012-10-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-29)

@attekett: nice bug, thanks! Looks like we might already have shipped the fix without proper release notes along with the Pwnium patch -- oops!

Anyway, $1000 of course!

### se...@chromium.org (2012-11-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-14)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/152707?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail mergedwith: crbug.com/chromium/153243]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076364)*
