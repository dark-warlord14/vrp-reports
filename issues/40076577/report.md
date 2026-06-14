# Invalid pointer write in GrRenderTarget::onRelease

| Field | Value |
|-------|-------|
| **Issue ID** | [40076577](https://issues.chromium.org/issues/40076577) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>GPU |
| **Reporter** | at...@gmail.com |
| **Assignee** | su...@chromium.org |
| **Created** | 2012-11-14 |
| **Bounty** | $1,000.00 |

## Description


Tested with:

OS: Windows 7 x64
Google Chrome: 25.0.1325.0 (167602) canary and 23.0.1271.64 (165188) m

The repro-file causes crash even without page-heap on both tested versions of Chrome. I haven't tested this on Linux with ASAN-build Chrome.

Repro-file:

<html>
<body>
<script>
var canvas=document.body.appendChild(document.createElement("canvas"));
canvas.setAttribute("width",3741)
canvas.setAttribute("height",3769)
var ctx=canvas.getContext("2d")
ctx.arc(3000,1000,173620738554745,-1.8508984587215662,-261354.2985719186,true)
ctx.setShadow(400,2000,700,100)
ctx.stroke()
setTimeout(function(){location.reload()},50)
</script>
</body>
</html>

WinDBG-analysis from dump-file:

FAULTING_IP: 
chrome_522c0000!GrRenderTarget::onRelease+13 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grrendertarget.cpp @ 125]
528e7911 f00fc110        lock xadd dword ptr [eax],edx

EXCEPTION_RECORD:  ffffffff -- (.exr 0xffffffffffffffff)
ExceptionAddress: 528e7911 (chrome_522c0000!GrRenderTarget::onRelease+0x00000013)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 0fdd9f84
Attempt to write to address 0fdd9f84

EXCEPTION_PARAMETER1:  00000001

EXCEPTION_PARAMETER2:  0fdd9f84

WRITE_ADDRESS:  0fdd9f84 

FOLLOWUP_IP: 
chrome_522c0000!v8::String::ExternalStringResourceBase::Dispose+c [c:\b\build\slave\win\build\src\v8\include\v8.h @ 1152]
5232110b c3              ret

STACK_TEXT:  
002eeba4 528c8bbc 528f2c6f 0d237f98 002eebd8 chrome_522c0000!GrRenderTarget::onRelease+0x13 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grrendertarget.cpp @ 125]
002eeba8 528f2c6f 0d237f98 002eebd8 5232110b chrome_522c0000!GrResource::release+0xf [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grresource.cpp @ 29]
002eebb4 5232110b 00000001 528f3254 11f50fe0 chrome_522c0000!GrGLRenderTarget::`scalar deleting destructor'+0x11
002eebbc 528f3254 11f50fe0 0d237f98 528c8bbc chrome_522c0000!v8::String::ExternalStringResourceBase::Dispose+0xc [c:\b\build\slave\win\build\src\v8\include\v8.h @ 1152]
002eebc8 528c8bbc 528f30cf 00000000 002eec04 chrome_522c0000!GrGLTexture::onRelease+0x96 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\gl\grgltexture.cpp @ 63]
002eebcc 528f30cf 00000000 002eec04 528e3dbb chrome_522c0000!GrResource::release+0xf [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grresource.cpp @ 29]
002eebd8 528e3dbb 00000001 528ddb9b 11000fb0 chrome_522c0000!GrGLTexture::`scalar deleting destructor'+0x11
002eebe0 528ddb9b 11000fb0 13b08f90 00000000 chrome_522c0000!GrTexture::internal_dispose+0x56 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grtexture.cpp @ 40]
002eec04 528e7942 01004bd0 10ff6be0 13b08f90 chrome_522c0000!GrResourceCache::purgeAsNeeded+0xf6 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grresourcecache.cpp @ 342]
002eec18 528d9d89 10ff6be0 11000fb0 0fc58f90 chrome_522c0000!GrRenderTarget::onRelease+0x44 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grrendertarget.cpp @ 125]
002eec28 528f1346 10fb2f88 528c9d10 10c74f78 chrome_522c0000!GrGpu::abandonResources+0x34 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grgpu.cpp @ 71]
002eec30 528c9d10 10c74f78 10fb2f88 0fc58f90 chrome_522c0000!GrGpuGL::abandonResources+0x8 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\gl\grgpugl_program.cpp @ 78]
002eec48 5361fac7 10fb2f88 5361fbc1 0fe22fc0 chrome_522c0000!GrContext::contextDestroyed+0x13 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grcontext.cpp @ 129]
002eec50 5361fbc1 0fe22fc0 002eec80 5361bd66 chrome_522c0000!WebCore::GraphicsContext3DPrivate::~GraphicsContext3DPrivate+0x21 [c:\b\build\slave\win\build\src\third_party\webkit\source\webcore\platform\chromium\support\graphicscontext3dprivate.cpp @ 74]
002eec5c 5361bd66 00000001 10c74f78 0fe22fc0 chrome_522c0000!WebCore::GraphicsContext3DPrivate::`scalar deleting destructor'+0xb
.
.
.



## Attachments

- [Chrome-last.dmp](attachments/Chrome-last.dmp) (application/octet-stream; charset=binary, 153.4 KB)
- [test.html](attachments/test.html) (text/plain; charset=us-ascii, 392 B)

## Timeline

### in...@chromium.org (2012-11-14)

[Empty comment from Monorail migration]

### kb...@chromium.org (2012-11-14)

[Empty comment from Monorail migration]

### [Deleted User] (2012-11-15)

I was unable to reproduce this in '23.0.1271.64 (Official Build 165188) m' on Windows 7 x64. Things got real slow but Chrome didn't crash. My machine has an NVIDIA Quadro 600 with the 8.17.12.9670 driver. 

### at...@gmail.com (2012-11-15)

I forget to give my HW-specs.

Graphics: Intel HD 4000 (Laptop with i5-3210M Processor)

From about:gpu on Chrome:

Driver Information
Initialization time	85
Sandboxed	false
GPU0	VENDOR = 0x8086, DEVICE= 0x0166
Optimus	false
AMD switchable	false
Driver vendor	Intel Corporation
Driver version	9.17.10.2875
Driver date	10-17-2012
Pixel shader version	3.0
Vertex shader version	3.0

Graphics Feature Status
Canvas: Hardware accelerated
Compositing: Hardware accelerated on all pages and threaded
3D CSS: Hardware accelerated
CSS Animation: Accelerated and threaded
WebGL: Hardware accelerated
WebGL multisampling: Hardware accelerated
Flash 3D: Hardware accelerated
Flash Stage3D: Hardware accelerated
Texture Sharing: Hardware accelerated
Video Decode: Hardware accelerated
Video: Hardware accelerated
Panel Fitting: Unavailable. Hardware acceleration disabled.

### [Deleted User] (2012-11-15)

I enabled gpu canvas on our Windows 7 64 bit laptop (with a GMA-X4500HD integrated GPU) but was still unable to reproduce this using '23.0.1271.64 (Official Build 165188) m'.

### at...@gmail.com (2012-11-15)

you could try to increase/decrease the time in location.reload() timeout. Or remove the timeout and try manually refresh the page. Without the timeout it took at max 8 refresh to crash the tab with 23.0.1271.64 official build 165188.

### at...@gmail.com (2012-11-15)

Have you tried to enable page-heap?

### at...@gmail.com (2012-11-25)

I tried this with another machine with Intel i3-3225 CPU and Intel HD 4000 graphics. Issue reproduced easily. I used gflags.exe /p /enable chrome.exe /full and enviromental variable CHROME_ALLOCATOR set to "winheap". I was not able to reproduce this on a machine with AMD E450 CPU and it's integrated graphics. Tested with Chrome version 25.0.1334.0 (Official Build 169347) canary 

### [Deleted User] (2012-11-26)

I tried unsuccessfully to reproduce on a Win7 64 system with an NVIDIA card and PageHeap enabled.

### [Deleted User] (2012-12-10)

Has anyone been able to reproduce this? Without a reproducible example I'm not sure how we can move forward on this.

### at...@gmail.com (2012-12-10)

FWIW this still reproduces easily on my laptop, with Intel HD 4000. 

### pa...@chromium.org (2012-12-18)

Say, kbr, can we try this in the GPU lab with its various GPUs? I assume we have at least one of the chips attekett does.

### kb...@chromium.org (2012-12-18)

+zmo, anantha

I think either zmo or anantha should be able to help you run tests on the various GPU bots around.


### er...@chromium.org (2012-12-18)

I wasn't able to reproduce a crash (with or without page heap)

However when I run that repro it destroys my entire system performance, making Windows unusable until I kill Chrome's GPU process.

I suspect the test is exhausting the GPU memory.

I am running on 64-bit Windows 7 SP1, with a Quadro 600 (driver version 296.70)

### in...@chromium.org (2013-01-07)

attekett, are you still able to reproduce this on trunk ?

### at...@gmail.com (2013-01-07)


Chrome 26.0.1376.0 (175264) canary

gflags.exe /p /enable chrome.exe /full
$env:CHROME_ALLOCATOR='winheap'

FAULTING_IP: 
chrome_63490000!GrRenderTarget::onRelease+10 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grrendertarget.cpp @ 129]
63ae6ecd f00fc110        lock xadd dword ptr [eax],edx

EXCEPTION_RECORD:  ffffffff -- (.exr 0xffffffffffffffff)
ExceptionAddress: 63ae6ecd (chrome_63490000!GrRenderTarget::onRelease+0x00000010)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 0b694fac
Attempt to write to address 0b694fac

Crash-dump as attachment. I try to get the crash-report uploaded later.

Without page-heap and $env:CHROME_ALLOCATOR='winheap' I only got null-pointer crash.

FAULTING_IP: 
chrome_5b9b0000!GrGpu::abandonResources+46 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grgpu.cpp @ 71]
5bff8d2a 8990bc020000    mov     dword ptr [eax+2BCh],edx

EXCEPTION_RECORD:  ffffffff -- (.exr 0xffffffffffffffff)
ExceptionAddress: 5bff8d2a (chrome_5b9b0000!GrGpu::abandonResources+0x00000046)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 000002bc
Attempt to write to address 000002bc



### [Deleted User] (2013-01-07)

I will try again on another machine to repro this one.

### [Deleted User] (2013-01-07)

[Comment Deleted]

### [Deleted User] (2013-01-07)

No repro on an older machine with GMA 3000 graphics. I tried Canary and a local build (debug and release).

### at...@gmail.com (2013-01-07)

Crash-ID 07c202052e1b55ae

Monday 7. january 2013 18.09.33

That should be the correct one. For some reason I got few "Crash not uploaded. Error=0x8004fffd." before Chrome successfully uploaded the crash stats.

### er...@chromium.org (2013-01-07)

For the record, error 0x8004fffd indicates that the crash was not uploaded due to client side throttling (IIRC it is limited to 5 crash reports per day).

### [Deleted User] (2013-01-30)

Has anyone tried this on a machine with an Intel HD 4000 gpu?

### [Deleted User] (2013-02-04)

Can anyone hear me? 

robertphillips, eroman, bsalomon did any of you try this with an Intel HD 4000 gpu?

zmo, anantha do you guys have access to a machine with this GPU where we could try this?

### [Deleted User] (2013-02-04)

We here in Skia land do not have access to a machine with an HD 4000.

### zm...@chromium.org (2013-02-04)

The retina ones have Intel HD 4000 as the integrated GPUs.  I have one on my desk (borrowed from Victoria)

### er...@chromium.org (2013-02-05)

> robertphillips, eroman, bsalomon did any of you try this with an Intel HD 4000 gpu?
eroman did not.

### in...@chromium.org (2013-02-11)

zmo@, can you please try the repro and see if it reproduces for you.

### zm...@chromium.org (2013-02-13)

Sorry I didn't realize this is a Windows crash case.  The retina with Intel HD 4000 is Mac, and I can't reproduce the crash on it.

Remove myself from the owner, but I have an old laptop with Intel GPU (forget which one).  I'll give it a try when I get back home.


### [Deleted User] (2013-02-13)

zmo@, I tried at least one machine with an older Intel GPU and could not
repro.

### ts...@chromium.org (2013-02-19)

@zmo - please find an appropriate owner for this, or suggest a path forward.  Thanks!

### ts...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### [Deleted User] (2013-02-19)

Tom, can we try to find a machine with these specs?  Unless we can repro the problem it will be hard to troubleshoot it.

Brian, Rob, would this sample snippet create any overly large textures by any chance? 


### [Deleted User] (2013-02-19)

All intermediate textures *should* be clipped to the size of the canvas (3741x3769).

### [Deleted User] (2013-02-19)

I'll buy a machine with the HD4000 and the quoted i5 CPU. Hopefully that'll be good enough.

@attekett if you can provide an exact make and model number for the laptop in question that would be even better.

### [Deleted User] (2013-02-19)

Tom, Should we order it for either NC or MTL? I'm happy to take this bug if I can repro it.

### [Deleted User] (2013-02-19)

In general I'm trying to get more aggressive about procuring machines in
cases like this; the developer time trying to diagnose it from afar isn't
worth the cost of just buying the laptop.

I agree it would be great to have one in MTL or NC or both, as well as MTV
(where we could add it to the roster of devices that the QA team uses,
since it's apparently "different" in some way).

If you'd like to order one I'd say go for it. If you'd like me to get one
for you I'm happy to ship it to you, too.

### at...@gmail.com (2013-02-19)

ASUS 
Model: A55A
MB Ver: K55A
ID: 3C

Sold under model name ASUS A55A SX009V in Finland

http://usa.asus.com/Notebooks/Versatile_Performance/K55A/#specifications

http://www.asus.fi/Notebooks/Versatile_Performance/K55A/#specifications

usa.asus.com doesn't seem to have the laptop with same cpu than asus.fi 
btw. the asus.fi site is also mainly in english.

CPU on my laptop is Intel® Core™ i5 3210M 2.5 GHz


### [Deleted User] (2013-03-06)

Anantha got one of these laptops for the QA team. Ligi, can you try the test file on it? It's in the original post but also attached here. If it crashes, either Vangelis or Al can take a look at it, and I can order one for the Skia guys too.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2013-03-18)

Quick ping. Stable's coming up so we want to at least triage this. Ligi can you use the new machine Anantha got to see if this test case is reproducible on it? If it is, then we can take a closer look

### li...@chromium.org (2013-03-18)

[Comment Deleted]

### li...@chromium.org (2013-03-18)

Tom , We are yet to receive the GPU systems that we ordered . 

But was able to reproduce the crash in - NVIDIA Quadro FX 3450/4000 SDI. Loaded the test.html file and left the system idle for sometime ~ 10-15mins , & got a renderer crash.

Build Tested - 27.0.1444.3 (Official Build 188745) 

Crash ID
========
28baf2b03862207c

Crash Report
=============

Thread 0 *CRASHED* ( EXCEPTION_ACCESS_VIOLATION_READ @ 0xfffffffffbaf2ef7 )

0x5f1589df	 [chrome.dll]	 - graphicscontext3dchromium.cpp:220]	WebCore::GraphicsContext3D::makeContextCurrent()
0x5e2a61cd	 [chrome.dll]	 - sharedgraphicscontext3d.cpp:68]	WebCore::SharedGraphicsContext3DImpl::getOrCreateContext()
0x5e268cb9	 [chrome.dll]	 - imagebufferskia.cpp:77]	WebCore::createAcceleratedCanvas
0x5e2690ee	 [chrome.dll]	 - imagebufferskia.cpp:163]	WebCore::ImageBuffer::ImageBuffer(WebCore::IntSize const &,float,WebCore::ColorSpace,WebCore::RenderingMode,WebCore::DeferralMode,bool &)
0x5e18c995	 [chrome.dll]	 - imagebuffer.h:90]	WebCore::ImageBuffer::create(WebCore::IntSize const &,float,WebCore::ColorSpace,WebCore::RenderingMode,WebCore::DeferralMode)
0x5e18da63	 [chrome.dll]	 - htmlcanvaselement.cpp:569]	WebCore::HTMLCanvasElement::createImageBuffer()
0x5e1ccc8d	 [chrome.dll]	 - canvasrenderingcontext2d.cpp:1222]	WebCore::CanvasRenderingContext2D::applyShadow()
0x5e1ccc64	 [chrome.dll]	 - canvasrenderingcontext2d.cpp:1217]	WebCore::CanvasRenderingContext2D::setShadow(WebCore::FloatSize const &,float,unsigned int)
0x5e1cc971	 [chrome.dll]	 - canvasrenderingcontext2d.cpp:1175]	WebCore::CanvasRenderingContext2D::setShadow(float,float,float,float)
0x5e6e0d13	 [chrome.dll]	 - v8canvasrenderingcontext2d.cpp:1576]	WebCore::CanvasRenderingContext2DV8Internal::setShadow2Method
0x5e6e1b11	 [chrome.dll]	 - v8canvasrenderingcontext2d.cpp:1622]	WebCore::CanvasRenderingContext2DV8Internal::setShadowMethod
0x5e6e1b50	 [chrome.dll]	 - v8canvasrenderingcontext2d.cpp:1634]	WebCore::CanvasRenderingContext2DV8Internal::setShadowMethodCallback
0x5e03e076	 [chrome.dll]	 - builtins.cc:1327]	v8::internal::HandleApiCallHelper<0>
0x5e03c2e7	 [chrome.dll]	 - builtins.cc:1345]	v8::internal::Builtin_HandleApiCall
0x0034eba7			
0x37d08090			
0x5dfd96c9	 [chrome.dll]	 - execution.cc:118]	v8::internal::Invoke
0x5dfd9992	 [chrome.dll]	 - execution.cc:181]	v8::internal::Execution::Call(v8::internal::Handle<v8::internal::Object>,v8::internal::Handle<v8::internal::Object>,int,v8::internal::Handle<v8::internal::Object> * const,bool *,bool)
0x5df4e313	 [chrome.dll]	 - api.cc:1823]	v8::Script::Run()
0x5e454814	 [chrome.dll]	 - scriptrunner.cpp:52]	WebCore::ScriptRunner::runCompiledScript(v8::Handle<v8::Script>,WebCore::ScriptExecutionContext *)
0x5e3101e3	 [chrome.dll]	 - scriptcontroller.cpp:283]	WebCore::ScriptController::compileAndRunScript(WebCore::ScriptSourceCode const &)
0x5e3103df	 [chrome.dll]	 - scriptcontroller.cpp:307]	WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const &)
0x5df47c64	 [chrome.dll]	 - scriptelement.cpp:312]	WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const &)
0x5df475c3	 [chrome.dll]	 - scriptelement.cpp:243]	WebCore::ScriptElement::prepareScript(WTF::TextPosition const &,WebCore::ScriptElement::LegacyTypeSupport)
0x5e1f7d8c	 [chrome.dll]	 - htmlscriptrunner.cpp:301]	WebCore::HTMLScriptRunner::runScript(WebCore::Element *,WTF::TextPosition const &)
0x5e1f78f2	 [chrome.dll]	 - htmlscriptrunner.cpp:174]	WebCore::HTMLScriptRunner::execute(WTF::PassRefPtr<WebCore::Element>,WTF::TextPosition const &)
0x5e1a0a8f	 [chrome.dll]	 - htmldocumentparser.cpp:435]	WebCore::HTMLDocumentParser::processParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)
0x5e1a01bf	 [chrome.dll]	 - htmldocumentparser.cpp:322]	WebCore::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)
0x5e1d9f4b	 [chrome.dll]	 - functional.h:522]	WTF::BoundFunctionImpl<WTF::FunctionWrapper<void ( WebCore::HTMLDocumentParser::*)(WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>,void (WTF::WeakPtr<WebCore::HTMLDocumentParser>,WTF::PassOwnPtr<WebCore::HTMLDocumentParser::ParsedChunk>)>::operator()()
0x5f16aeb3	 [chrome.dll]	 - mainthreadchromium.cpp:61]	WTF::callFunctionObject
0x5ddd9b5e	 [chrome.dll]	 - bind_internal.h:1173]	base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (*)(void const *)>,void (void const *),void (void const *)>,void (void const *)>::Run(base::internal::BindStateBase *)
0x5ddc06c0	 [chrome.dll]	 - message_loop.cc:476]	MessageLoop::RunTask(base::PendingTask const &)
0x5ddc10eb	 [chrome.dll]	 - message_loop.cc:671]	MessageLoop::DoWork()
0x5de05c70	 [chrome.dll]	 - message_pump_default.cc:29]	base::MessagePumpDefault::Run(base::MessagePump::Delegate *)
0x5ddf7d77	 [chrome.dll]	 - trace_event_impl.cc:1101]	base::debug::TraceLog::AddTraceEventEtw(char,char const *,void const *,char const *)
0x5f4d8765	 [chrome.dll]	 - renderer_main.cc:226]	content::RendererMain(content::MainFunctionParams const &)

Not reproducible using the following GPU cards.

1. Intel(R) Graphics Media Accelerator 3150
2. Mobile Intel(R) 945 Express Chipset

### [Deleted User] (2013-03-19)

Hmmm, that's a totally different card and driver than the original report,
so interesting to know it isn't necessarily driver specific, maybe just
timing related.

Still, until we can get a machine in the hands of Brian or one of the other
canvas guys we can't do much about this. My hope was that we could repro it
on that laptop and get one for the NC or MTL offices too. Since this
doesn't seem urgent, let's wait and see if the machine in the original
report repros and then decide.

### in...@chromium.org (2013-03-19)

[Empty comment from Monorail migration]

### [Deleted User] (2013-03-21)

Bulk Edit

### [Deleted User] (2013-03-21)

Bulk edit

### [Deleted User] (2013-03-21)

Bulk edit

### li...@chromium.org (2013-04-02)

Was able to reproduce the crash consistently  in all the channels using the system  which was originally reported.
used the sample testcase from https://crbug.com/chromium/161077#c38 to reproduce this issue.

Builds tested
=======
26.0.1410.43
27.0.1453.12

Crash ID
--------
c2ac003e14b46456
6994b38ebe4f1f66

Crash Report
========
Thread 0 *CRASHED* ( EXCEPTION_ACCESS_VIOLATION_WRITE @ 0x0000034c )

0x6e816179	 [chrome.dll]	 - grgpu.cpp:65]	GrGpu::abandonResources()
0x00113875			
0x23f04023	

System Configuration
==============
ASUS
CPU - Intel (R) Core i-5-3210M , 2.5GHz

GPU Information
==========
Intel(R) HD Graphics 4000
Driver Version : 9.17.10.2828


### ju...@chromium.org (2013-04-03)

It would be useful to repro using a debug build, with a debugger attached.  If you can get the machine in that state, then ping one of use by IM, and we can remote desktop onto the machine to inspect.

### in...@chromium.org (2013-04-03)

M26 has sailed. Moving all m25 bugs to m26.

### li...@chromium.org (2013-04-05)

This is not a regression happens in all the channels ,hence  don't know the range of the chromium builds, to do further debugging . 

### [Deleted User] (2013-04-05)

Ligi can you use whatever version you were able to repro with in #48 and set it up so that junov can remote desktop onto the machine and poke at it?

### [Deleted User] (2013-04-16)

ligimole, friendly ping

### li...@chromium.org (2013-04-17)

Talked to Justin and provided all the available informations.

Justin was able to make out the cause and mentioned that will have a fix within a week or two. Once the fix is ready he plans to send the build , so that I can verify in ASUS system with Intel(R) HD Graphics 4000 .

### ju...@chromium.org (2013-04-17)

It is a graphics context lost due to allocation of a 0x0 pbo. We need to a) fix the source of the problem and b) make 2d canvases more robust to context losses.

### ju...@chromium.org (2013-04-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-02)

[Empty comment from Monorail migration]

### ju...@chromium.org (2013-05-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-02)

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### ju...@chromium.org (2013-05-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-07)

Sugoi@, are you looking into this. As part of Security Code 28, we want to get this high severity security bug fixed soon.

### su...@chromium.org (2013-05-07)

I don't have access to any hardware where this bug can be reproduced. Based on the info that we have here, I already committed a speculative fix in Skia for this bug last week, which should have rolled into Chrome by now, which would need to be double checked on the proper hardware. If it is still reproducible, please send me a stack trace or any pertinent information. Thanks.

### su...@chromium.org (2013-05-07)

To be more precise : The fix was in Skia version 8982. Note that it has rolled into chromium source, which is at revision 9003, but not in Canary, which is still at revision 8974.

### in...@chromium.org (2013-05-07)

Attekett, please look for Windows Canary 28.0.1500.3 when available (should be tonight/tmrw) to verify this fix. We really appreciate your help.

### in...@chromium.org (2013-05-07)

Attekett, 28.0.1500.3 canary looks out (i could update it ::) Can you please verify the fix. Thanks a lot.

### at...@gmail.com (2013-05-08)


I can still reproduce with the test case from https://crbug.com/chromium/161077#c38.

OS: Windows 7 x64
Google Chrome: 28.0.1500.4 (Official Build 198823) canary

Without page-heap:

Crash ID 8fd3fbba1cd1ac0f

FAULTING_IP: 
chrome_5d880000!GrGpu::abandonResources+46 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grgpu.cpp @ 65]
5df248af 899038030000    mov     dword ptr [eax+338h],edx

EXCEPTION_RECORD:  ffffffff -- (.exr 0xffffffffffffffff)
ExceptionAddress: 5df248af (chrome_5d880000!GrGpu::abandonResources+0x00000046)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 00000338
Attempt to write to address 00000338

With page-heap /full:

Crash ID f164ebd3090862c8

FAULTING_IP: 
chrome_5ac60000!GrRenderTarget::onRelease+10 [c:\b\build\slave\win\build\src\third_party\skia\src\gpu\grrendertarget.cpp @ 129]
5b32214a f00fc110        lock xadd dword ptr [eax],edx

EXCEPTION_RECORD:  ffffffff -- (.exr 0xffffffffffffffff)
ExceptionAddress: 5b32214a (chrome_5ac60000!GrRenderTarget::onRelease+0x00000010)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 0f36bfa4
Attempt to write to address 0f36bfa4


### su...@chromium.org (2013-05-08)

Hi attekett

Thanks for the info. Can you also paste the log messages at the bottom of the "chrome:gpu" page ?
So, after you crash, go to "chrome:gpu" (type it in the address bar like any other URL). At the bottom, the last section should be called "log messages". If you can copy-paste that info here, it may give us more info about the crash. Thanks.

### at...@gmail.com (2013-05-08)

From about:gpu

Log Messages

GpuProcessHostUIShim: The GPU process exited normally. Everything is okay.
GpuProcessHostUIShim: The GPU process exited normally. Everything is okay.
[1656:3764:0508/142142:ERROR:gles2_cmd_decoder.cc(9093)] : Offscreen context lost via ARB/EXT_robustness. Reset status = GL_UNKNOWN_CONTEXT_RESET_EXT
[1656:3764:0508/142142:ERROR:gles2_cmd_decoder.cc(2825)] : GLES2DecoderImpl: Context lost during MakeCurrent.
[1656:3764:0508/142142:ERROR:gles2_cmd_decoder.cc(2830)] : Exiting GPU process because some drivers cannot reset a D3D device in the Chrome GPU process sandbox.
GpuProcessHostUIShim: The GPU process exited normally. Everything is okay.

### su...@chromium.org (2013-05-08)

Debugging this issue blindly will take too much time. Brian proposed to order the proper hardware to debug this, so I'm assigning the issue to him.

### [Deleted User] (2013-05-08)

Laptop should be here tomorrow.

### in...@chromium.org (2013-05-08)

Thanks Bsalomon@. Please see if a fix is possible by end of next week. We are targeting closing all our high severity bugs by then.

### [Deleted User] (2013-05-10)

The Skia access violation bug was fixed in r9102 of Skia. It missed today's Skia roll and so will hit chromium on Monday morning.

### in...@chromium.org (2013-05-10)

Thanks for the fix.

### [Deleted User] (2013-05-13)

It's marked merge-approved, what branches should it be merged to?

### in...@chromium.org (2013-05-13)

it needs to be merged to m27. i hope we got in before m28 branched, otherwise m28 as well.

### [Deleted User] (2013-05-13)

Thanks. I merged it to M27 and M28.

### in...@chromium.org (2013-05-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-06-03)

@attekett: a golden oldie! We finally got it.
$1000


### pa...@chromium.org (2013-06-24)

Payment on the way...

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

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

This issue was migrated from crbug.com/chromium/161077?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>GPU]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076577)*
