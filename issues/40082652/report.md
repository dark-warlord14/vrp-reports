# Security: Overflow in VertexBufferInterface::reserveVertexSpace causes memory-safety bug

| Field | Value |
|-------|-------|
| **Issue ID** | [40082652](https://issues.chromium.org/issues/40082652) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Reporter** | [Deleted User] |
| **Assignee** | jm...@chromium.org |
| **Created** | 2015-08-09 |
| **Bounty** | $5,000.00 |

## Description

[I reported the following bug to Mozilla (for its manifestations in Firefox, Thunderbird, etc.) at https://bugzilla.mozilla.org/show_bug.cgi?id=1190526 . Since the bug is in Angle, a Google library, I am also reporting it here. Version and reproduction information pertain to Firefox. I do not know whether it can also be reproduced in Chrome.

The bug is present in the latest available Angle at https://github.com/google/angle/blob/master/src/libANGLE/renderer/d3d/VertexBuffer.cpp]


VertexBufferInterface::reserveVertexSpace (gfx\angle\src\libGLESv2\renderer\d3d\VertexBuffer.cpp) can incur an overflow with a specially-crafted set of shader attribute arrays. The overflow causes VertexBufferInterface::storeVertexAttributes to fail to allocate a large-enough buffer, then to write the contents of one or more shader attribute arrays (whose contents an attacker can prescribe) far beyond the buffer's end.

This bug can be manifested [in Firefox 40b8 x64 on Win7 SP1 with D3D 11] (see attached proof-of-concept [0] and details below) and probably also [in Firefox x64] under Linux x64. Someone with more knowledge of WebGL might also be able to manifest this bug under Win32 and other 32-bit platforms.

Details:
------------------------------------------------------------------------------------------------------

The bug is in VertexBufferInterface::reserveVertexSpace:

135: gl::Error VertexBufferInterface::reserveVertexSpace(const gl::VertexAttribute &attrib, GLsizei count, GLsizei instances)

136: {
137:    gl::Error error(GL_NO_ERROR);
138:
139:    unsigned int requiredSpace;
140:    error = mVertexBuffer->getSpaceRequired(attrib, count, instances, &requiredSpace);
141:    if (error.isError())
142:    {
143:        return error;
144:    }
145:
146:    // Protect against integer overflow
147:    if (mReservedSpace + requiredSpace < mReservedSpace)
148:    {
149:        return gl::Error(GL_OUT_OF_MEMORY, "Unable to reserve %u extra bytes in internal vertex buffer, "
150:                         "it would result in an overflow.", requiredSpace);
151:    }
152:
153:    mReservedSpace += requiredSpace;
154:
155:    // Align to 16-byte boundary
156:    mReservedSpace = rx::roundUp (mReservedSpace, 16u);
157:
158:    return gl::Error(GL_NO_ERROR);
159: }

The checks on line 147-51 close the overflow window, but the round-up on line 156 reopens it just a crack. If the WebGL program  uses 8 attribute arrays of size 0x1FFFFFF8, mReservedSpace on line 156 rounds up each time (from 0x1FFFFFF8 to 0x20000000 on the 1st array, 0x3ffffff8 to 0x40000000 on the 2nd) and finally overflows from 0xFFFFFFF8 to 0 on the last array.

Later, when VertexBufferInterface::storeVertexAttributes is called to save the attributes into the buffer, it calls StreamingVertexBufferInterface::reserveSpace  with that same buffer size (0). reserveSpace then leaves the existing default buffer of length 0x100000 bytes [1] in place:

209: gl::Error StreamingVertexBufferInterface::reserveSpace(unsigned int size)
210: {
211:     unsigned int curBufferSize = getBufferSize();
212:     if (size > curBufferSize)
213:     {
214:         gl::Error error = setBufferSize(std::max(size, 3 * curBufferSize / 2));
215:         if (error.isError())
216:         {
217:             return error;
218:         }
219:         setWritePosition(0);
220:     }
221:     else if (getWritePosition() + size > curBufferSize)
222:     {
223:         gl::Error error = discard();
224:         if (error.isError())
225:         {
226:             return error;
227:         }
228:         setWritePosition(0);
229:     }
230: 
231:     return gl::Error(GL_NO_ERROR);
232: }

(size == 0, so control skips from line 212 to line 221, and thence to line 231).

Finally, VertexBufferInterface::storeVertexAttributes is called to copy an entire attribute array into the (0x100000-byte) buffer:

116:    error = mVertexBuffer->storeVertexAttributes(attrib, currentValue, start, count, instances, mWritePosition);

Since all of the proof-of-concept attribute arrays are 0x1FFFFFF8 bytes, this causes a potentially huge overrun. In testing the POC several times, this has had various effects:

1. Writing into a structure from which the video driver extracts a pointer, resulting in an attempt to read an invalid address (and probably other undetected corruption before the exception). This example is included, below. I saw this problem twice in different guises.

2. Writing into a function pointer, causing the video driver to attempt to call a function at an invalid address.

3. Writing into a function pointer, causing nss3.dll!PR_GetEnv to attempt to call a function at an invalid address.

4. A stack overflow with unknown corruption beforehand.

5. The display going blank, then partially repainting, with the message "Display driver nvlddmkm stopped responding and has successfully recovered" popping up, followed by an exception hitting an inaccessible page.

6. Hitting an inaccessible page, causing an exception, after overwriting varied amounts of unowned memory with no visible effects.

------------------------------------------------------------------------------------------------------
Manifesting the bug 

The following crash occured while running the attached proof-of-concept program. The setup was to run FF 40b8 x64 on Win7 SP1 (I wasn't able to find 39.0 x64. Where is it distributed?). I attached the VS debugger to FF, then opened 4 windows and navigated to the following sites in 3 of them:

   Dynamic procedural terrain (http://alteredqualia.com/three/examples/webgl_terrain_dynamic.html )
   Bill Nye Reading Mean Tweets (https://www.youtube.com/watch?v=mm4Rwyi-k08 )
   WebGL Aquarium (http://webglsamples.org/aquarium/aquarium.html )

[See note [2]]

I then ran the proof-of-concept program in the 4th window. At the "unresponsive script" alert box, I clicked "continue". A few seconds later the following crash appeared in VS:

Exception thrown at 0x000007FEEA9CE79A (nvwgf2umx.dll) in firefox.exe: 0xC0000005: Access violation reading location 0xFFFFFFFFFFFFFFFF.

Investigating, I found that the actual address that was read to cause the exception was different. Reading the code stream:

000007FEEA9CE760  mov         qword ptr [rsp+10h],rbx  
000007FEEA9CE765  push        rdi  
000007FEEA9CE766  mov         rcx,qword ptr [r9+20h]  
000007FEEA9CE76A  or          r11,0FFFFFFFFFFFFFFFFh  
000007FEEA9CE76E  xor         r10d,r10d  
000007FEEA9CE771  xor         ebx,ebx  
000007FEEA9CE773  mov         rdi,rdx  
000007FEEA9CE776  test        rcx,rcx  
000007FEEA9CE779  je          000007FEEA9CE806  
000007FEEA9CE77F  mov         rdx,qword ptr [rcx+40h]  
000007FEEA9CE783  mov         qword ptr [rsp+10h],rsi  
000007FEEA9CE788  mov         rax,qword ptr [rdx]  
000007FEEA9CE78B  test        rax,rax  
000007FEEA9CE78E  je          000007FEEA9CE7BD  
000007FEEA9CE790  mov         r10,qword ptr [rax+1E8h]  
000007FEEA9CE797  mov         rbx,rdx  
> 000007FEEA9CE79A  mov         rax,qword ptr [r10+118h]  
000007FEEA9CE7A1  mov         r11,qword ptr [r10+110h]  
000007FEEA9CE7A8  cmp         r11,rax  
000007FEEA9CE7AB  cmovbe      r11,rax  
000007FEEA9CE7AF  mov         rax,qword ptr [r10+120h]  
000007FEEA9CE7B6  cmp         r11,rax  

We find that r10 at the crashing instruction is 0x433a0000433a0000, which is exactly the bad data that the POC writes [3]. r10 came from [rax+1E8h], which contained:

0x000000003D384F98  00 00 3a 43 00 00 3a 43 00 00 3a 43 00 00 3a 43  ..:C..:C..:C..:C
0x000000003D384FA8  00 00 3a 43 00 00 3a 43 00 00 3a 43 00 00 3a 43  ..:C..:C..:C..:C
0x000000003D384FB8  00 00 3a 43 00 00 3a 43 00 00 3a 43 00 00 3a 43  ..:C..:C..:C..:C
0x000000003D384FC8  00 00 3a 43 00 00 3a 43 00 00 3a 43 00 00 3a 43  ..:C..:C..:C..:C
0x000000003D384FD8  00 00 3a 43 00 00 3a 43 00 00 3a 43 00 00 3a 43  ..:C..:C..:C..:C
0x000000003D384FE8  00 00 3a 43 00 00 3a 43 00 00 3a 43 00 00 3a 43  ..:C..:C..:C..:C

The thread's registers were:

RAX = 000000003D384DB0 RBX = 000000000F36D540 RCX = 000000000F36B180 RDX = 000000000F36D540 
RSI = 0000000000000002 RDI = 000000000FBFE958 R8  = 000000000FBFE9A8 R9  = 000000000F36D770 
R10 = 433A0000433A0000 R11 = FFFFFFFFFFFFFFFF R12 = 0000000000000002 R13 = 0000000000000002 
R14 = 00000000542CA6A0 R15 = 000000000F36D770 RIP = 000007FEEA9CE79A RSP = 000000000FBFE910 
RBP = 00000000004C2DD0 EFL = 00010202 

And the thread's stack was:

>	nvwgf2umx.dll!000007feea9ce79a()	Unknown
 	nvwgf2umx.dll!000007feea94b040()	Unknown
 	nvwgf2umx.dll!000007feea94ac14()	Unknown
 	nvwgf2umx.dll!000007feea3b944e()	Unknown
 	nvwgf2umx.dll!000007feea2c2df4()	Unknown
 	nvwgf2umx.dll!000007feea3ea279()	Unknown
 	d3d11.dll!CResource<struct ID3D11Resource>::Map<0,5>(class CContext *,class CResource<struct 

ID3D11Resource> *,unsigned int,enum D3D11_MAP,unsigned int,struct D3D11_MAPPED_SUBRESOURCE *)	Unknown
 	d3d11.dll!CContext::ID3D11DeviceContext1_Map_<1>(struct ID3D11DeviceContext1 *,struct ID3D11Resource 

*,unsigned int,enum D3D11_MAP,unsigned int,struct D3D11_MAPPED_SUBRESOURCE *)	Unknown
 	xul.dll!mozilla::layers::CompositorD3D11::UpdateConstantBuffers() Line 1347	C++
 	xul.dll!mozilla::layers::CompositorD3D11::ClearRect(const 

mozilla::gfx::RectTyped<mozilla::gfx::UnknownUnits> & aRect) Line 600	C++
 	xul.dll!mozilla::layers::CompositorD3D11::BeginFrame(const nsIntRegion & aInvalidRegion, const 

mozilla::gfx::RectTyped<mozilla::gfx::UnknownUnits> * aClipRectIn, const 

mozilla::gfx::RectTyped<mozilla::gfx::UnknownUnits> & aRenderBounds, 

mozilla::gfx::RectTyped<mozilla::gfx::UnknownUnits> * aClipRectOut, 

mozilla::gfx::RectTyped<mozilla::gfx::UnknownUnits> * aRenderBoundsOut) Line 1076	C++
 	xul.dll!mozilla::layers::LayerManagerComposite::Render() Line 718	C++
 	xul.dll!mozilla::layers::LayerManagerComposite::EndTransaction(void (mozilla::layers::PaintedLayer *, 

gfxContext *, const nsIntRegion &, mozilla::layers::DrawRegionClip, const nsIntRegion &, void *) * aCallback, 

void * aCallbackData, mozilla::layers::LayerManager::EndTransactionFlags aFlags) Line 319	C++
 	xul.dll!mozilla::layers::LayerManagerComposite::EndEmptyTransaction

(mozilla::layers::LayerManager::EndTransactionFlags aFlags) Line 262	C++
 	xul.dll!mozilla::layers::CompositorParent::CompositeToTarget(mozilla::gfx::DrawTarget * aTarget, const 

mozilla::gfx::IntRectTyped<mozilla::gfx::UnknownUnits> * aRect) Line 1143	C++
 	xul.dll!mozilla::layers::CompositorVsyncScheduler::Composite(mozilla::TimeStamp aVsyncTimestamp) Line 

519	C++
 	xul.dll!RunnableMethod<SoftwareDisplay,void (__cdecl SoftwareDisplay::*)(mozilla::TimeStamp) 

__ptr64,Tuple1<mozilla::TimeStamp> >::Run() Line 311	C++
 	xul.dll!MessageLoop::DoWork() Line 456	C++
 	xul.dll!base::MessagePumpForUI::DoRunLoop() Line 217	C++
 	xul.dll!base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate) Line 78	C++
 	xul.dll!MessageLoop::RunHandler() Line 227	C++
 	xul.dll!MessageLoop::Run() Line 201	C++
 	xul.dll!base::Thread::ThreadMain() Line 173	C++
 	xul.dll!`anonymous namespace'::ThreadFunc(void * closure) Line 27	C++
 	kernel32.dll!BaseThreadInitThunk()	Unknown
 	ntdll.dll!RtlUserThreadStart()	Unknown

and the thread's description was:

Not Flagged	>	0x00000CF4	0x00	Worker Thread	xul.dll!`anonymous namespace'::ThreadFunc	

nvwgf2umx.dll!000007feea9ce79a	Normal


BUT the main thread was still in memcpy, still overwriting memory that it didn't own:

Not Flagged		0x000012B0	0x00	Main Thread	Main Thread	msvcr120.dll!memcpy	Normal

and its stack was:

 	msvcr120.dll!memcpy() Line 357	Unknown
>	libGLESv2.dll!rx::VertexBuffer11::storeVertexAttributes(const gl::VertexAttribute & attrib, const 

gl::VertexAttribCurrentValueData & currentValue, int start, int count, int instances, unsigned int offset) Line 

122	C++
 	libGLESv2.dll!rx::VertexBufferInterface::storeVertexAttributes(const gl::VertexAttribute & attrib, 

const gl::VertexAttribCurrentValueData & currentValue, int start, int count, int instances, unsigned int * 

outStreamOffset) Line 116	C++
 	libGLESv2.dll!rx::VertexDataManager::storeAttribute(const gl::VertexAttribute & attrib, const 

gl::VertexAttribCurrentValueData & currentValue, rx::TranslatedAttribute * translated, int start, int count, 

int instances) Line 295	C++
 	libGLESv2.dll!rx::VertexDataManager::prepareVertexData(const gl::State & state, int start, int count, 

rx::TranslatedAttribute * translated, int instances) Line 131	C++
 	libGLESv2.dll!rx::Renderer11::applyVertexBuffer(const gl::State & state, int first, int count, int 

instances) Line 994	C++
 	libGLESv2.dll!gl::Context::drawArrays(unsigned int mode, int first, int count, int instances) Line 1786	

C++
 	libGLESv2.dll!glDrawArrays(unsigned int mode, int first, int count) Line 1387	C++
 	xul.dll!mozilla::gl::GLContext::fDrawArrays(unsigned int mode, int first, int count) Line 1144	C++
 	xul.dll!mozilla::WebGLContext::DrawArrays(unsigned int mode, int first, int count) Line 142	C++
 	xul.dll!mozilla::dom::WebGLRenderingContextBinding::drawArrays(JSContext * cx, JS::Handle<JSObject *> 

obj, mozilla::WebGLContext * self, const JSJitMethodCallArgs & args) Line 10758	C++
 	xul.dll!mozilla::dom::GenericBindingMethod(JSContext * cx, unsigned int argc, JS::Value * vp) Line 2615	

C++
 	xul.dll!js::Invoke(JSContext * cx, JS::CallArgs args, js::MaybeConstruct construct) Line 753	C++
 	xul.dll!Interpret(JSContext * cx, js::RunState & state) Line 2962	C++
 	xul.dll!js::RunScript(JSContext * cx, js::RunState & state) Line 683	C++
 	xul.dll!js::Invoke(JSContext * cx, JS::CallArgs args, js::MaybeConstruct construct) Line 756	C++
 	xul.dll!js::Invoke(JSContext * cx, const JS::Value & thisv, const JS::Value & fval, unsigned int argc, 

const JS::Value * argv, JS::MutableHandle<JS::Value> rval) Line 790	C++
 	xul.dll!mozilla::dom::EventHandlerNonNull::Call(JSContext * cx, JS::Handle<JS::Value> aThisVal, 

mozilla::dom::Event & event, JS::MutableHandle<JS::Value> aRetVal, mozilla::ErrorResult & aRv) Line 260	C++
 	xul.dll!mozilla::dom::EventHandlerNonNull::Call<nsISupports * __ptr64>(nsISupports * const & thisVal, 

mozilla::dom::Event & event, JS::MutableHandle<JS::Value> aRetVal, mozilla::ErrorResult & aRv, const char * 

aExecutionReason, mozilla::dom::CallbackObject::ExceptionHandling aExceptionHandling, JSCompartment * 

aCompartment) Line 351	C++
 	xul.dll!mozilla::JSEventHandler::HandleEvent(nsIDOMEvent * aEvent) Line 216	C++
 	xul.dll!mozilla::EventListenerManager::HandleEventInternal(nsPresContext * aPresContext, 

mozilla::WidgetEvent * aEvent, nsIDOMEvent * * aDOMEvent, mozilla::dom::EventTarget * aCurrentTarget, 

nsEventStatus * aEventStatus) Line 1129	C++
 	xul.dll!mozilla::EventTargetChainItem::HandleEventTargetChain(nsTArray<mozilla::EventTargetChainItem> & 

aChain, mozilla::EventChainPostVisitor & aVisitor, mozilla::EventDispatchingCallback * aCallback, 

mozilla::ELMCreationDetector & aCd) Line 301	C++
 	xul.dll!mozilla::EventDispatcher::Dispatch(nsISupports * aTarget, nsPresContext * aPresContext, 

mozilla::WidgetEvent * aEvent, nsIDOMEvent * aDOMEvent, nsEventStatus * aEventStatus, 

mozilla::EventDispatchingCallback * aCallback, nsTArray<mozilla::dom::EventTarget *> * aTargets) Line 638	

C++
 	xul.dll!nsDocumentViewer::LoadComplete(nsresult aStatus) Line 1000	C++
 	xul.dll!nsDocShell::EndPageLoad(nsIWebProgress * aProgress, nsIChannel * aChannel, nsresult aStatus) 

Line 7562	C++
 	xul.dll!nsDocShell::OnStateChange(nsIWebProgress * aProgress, nsIRequest * aRequest, unsigned int 

aStateFlags, nsresult aStatus) Line 7371	C++
 	xul.dll!nsDocLoader::DoFireOnStateChange(nsIWebProgress * const aProgress, nsIRequest * const aRequest, 

int & aStateFlags, const nsresult aStatus) Line 1250	C++
 	xul.dll!nsDocLoader::doStopDocumentLoad(nsIRequest * request, nsresult aStatus) Line 829	C++
 	xul.dll!nsDocLoader::DocLoaderIsEmpty(bool aFlushLayout) Line 721	C++
 	xul.dll!nsDocLoader::OnStopRequest(nsIRequest * aRequest, nsISupports * aCtxt, nsresult aStatus) Line 

606	C++
 	xul.dll!nsLoadGroup::RemoveRequest(nsIRequest * request, nsISupports * ctxt, nsresult aStatus) Line 652	

C++
 	xul.dll!nsDocument::DoUnblockOnload() Line 9160	C++
 	xul.dll!nsDocument::UnblockOnload(bool aFireSync) Line 9089	C++
 	xul.dll!nsDocument::DispatchContentLoadedEvents() Line 5225	C++
 	xul.dll!nsRunnableMethodImpl<void (__cdecl imgRequestProxy::*)(void) __ptr64,1>::Run() Line 811	C++
 	xul.dll!nsThread::ProcessNextEvent(bool aMayWait, bool * aResult) Line 872	C++
 	xul.dll!mozilla::ipc::MessagePump::Run(base::MessagePump::Delegate * aDelegate) Line 95	C++
 	xul.dll!MessageLoop::RunHandler() Line 227	C++
 	xul.dll!MessageLoop::Run() Line 201	C++
 	xul.dll!nsBaseAppShell::Run() Line 167	C++
 	xul.dll!nsAppShell::Run() Line 180	C++
 	xul.dll!nsAppStartup::Run() Line 281	C++
 	xul.dll!XREMain::XRE_mainRun() Line 4079	C++
 	xul.dll!XREMain::XRE_main(int argc, char * * argv, const nsXREAppData * aAppData) Line 4170	C++
 	xul.dll!XRE_main(int argc, char * * argv, const nsXREAppData * aAppData, unsigned int aFlags) Line 4260	

C++
 	firefox.exe!do_main(int argc, char * * argv, nsIFile * xreDirectory) Line 214	C++
 	firefox.exe!NS_internal_main(int argc, char * * argv) Line 480	C++
 	firefox.exe!wmain(int argc, wchar_t * * argv) Line 138	C++
 	firefox.exe!__tmainCRTStartup() Line 255	C
 	kernel32.dll!BaseThreadInitThunk()	Unknown
 	ntdll.dll!RtlUserThreadStart()	Unknown

Examining the libGLESv2.dll!rx::VertexBuffer11::storeVertexAttributes frame, we find that the code used the following parameters:

  0x000000003bed0000 pData
+ 0x00000000000e0a20 offset
= 0x000000003BFB0A20 attribute buffer base
  0x000000003C0B0A1F attribute buffer end

  0x000000003D384F98 is the address from which the video driver read its pointer

Examining the main thread code memcpy frame, we see that the thread stopped at:

000007FEF6BBC623  nop         word ptr [rax+rax]  
000007FEF6BBC630  mov         rax,qword ptr [rdx+rcx]  
--- No source file -------------------------------------------------------------
> 000007FEF6BBC634  mov         r10,qword ptr [rdx+rcx+8]  
000007FEF6BBC639  add         rcx,20h  
000007FEF6BBC63D  mov         qword ptr [rcx-20h],rax  
000007FEF6BBC641  mov         qword ptr [rcx-18h],r10  
000007FEF6BBC645  mov         rax,qword ptr [rdx+rcx-10h]  
000007FEF6BBC64A  mov         r10,qword ptr [rdx+rcx-8]  
000007FEF6BBC64F  dec         r9  
000007FEF6BBC652  mov         qword ptr [rcx-10h],rax  
000007FEF6BBC656  mov         qword ptr [rcx-8],r10  
000007FEF6BBC65A  jne         MoveSmall+190h (07FEF6BBC630h)  
000007FEF6BBC65C  and         r8,1Fh  
000007FEF6BBC660  jmp         mcpy00aa+73h (07FEF6BBC457h)  

with registers:

RAX = 433A0000433A0000 RBX = 000000000023B230 RCX = 000000003D48F820 RDX = 000000006404F5E0 
RSI = 0000000000000000 RDI = 00000000494C1800 R8  = 000000001FFFFFF8 R9  = 0000000000F5908F 
R10 = 433A0000433A0000 R11 = 000000003BFB0A20 R12 = 00000000111BEDC0 R13 = 000000002AFBB400 
R14 = 000000003BFB0A20 R15 = 0000000000000004 RIP = 000007FEF6BBC634 RSP = 000000000023B0D8 
RBP = 000000000023B171 EFL = 00000212 

So the last data it wrote was at

0x000000003D48F820 - 8 == 0x000000003D48F818


This means that memcpy wrote

  0x000000003D48F818 - 0x000000003BFB0A20 == 0x00000000014DEDF8

bytes, beginning at the buffer's base, extending far beyond its end, including the memory from which the video driver read its pointer, and terminating only when the OS suspended the process's threads due to the exception in the video driver thread.


------------------------------------------------------------------------------------------------------
[0] Extract poc.js, poc.htm, and glMatrix-0.9.5.min.js . Save them all in the same folder and load poc.htm from that folder.

[1] This is set by VertexDataManager::VertexDataManager using the constant INITIAL_STREAM_BUFFER_SIZE.

[2] It's probably easiest to reproduce obviously adverse effects from this bug by running 2 windows of "Dynamic Procedural Terrain" and one of "Bill Nye Reading Mean Tweets". You might need to try it several times. You can witness the overwriting directly by putting a breakpoint on VertexBuffer11::storeVertexAttributes and stepping into its call to vertexFormatInfo.copyFunction.

[3] See poc.js line 149, which assigns the (float) attribute array elements the value 0xba. This is represented as 0x433a0000.

## Attachments

- [glMatrix-0.9.5.min.js](attachments/glMatrix-0.9.5.min.js) (text/javascript, 18.3 KB)
- [poc.js](attachments/poc.js) (text/javascript, 8.3 KB)
- [poc.htm](attachments/poc.htm) (text/html, 1.4 KB)

## Timeline

### [Deleted User] (2015-08-09)

On a meta note, this bug-reporting system does not send the reporter a message for the initial report. Is there some configuration option that controls this feature?

### [Deleted User] (2015-08-10)

There is a similar bug in VertexBufferInterface::storeVertexAttributes at line 136:

136:    mWritePosition = rx::roundUp(mWritePosition, 16u);

but I have not yet examined whether it can be leveraged into a vulnerability.

### js...@chromium.org (2015-08-10)

kbr@ - Could you forward this on to the appropriate person on angle?

### [Deleted User] (2015-08-10)

Hi again. I just received an email update spawned by https://crbug.com/chromium/518206#c3, and notice that its subject line was the subject line of the bug, and its contents were the entire contents of https://crbug.com/chromium/518206#c3. This is very bad, since the email was not encrypted. Please fix this bug.

### [Deleted User] (2015-08-10)

BTW, when I wrote "The bug is present in the latest available Angle at https://github.com/google/angle/blob/master/src/libANGLE/renderer/d3d/VertexBuffer.cpp" I did not mean to imply that it wasn't present in release versions. It is, which is how I discovered it in the Mozilla codebase. The Mozilla codebase in question (39.0) appears to be using Angle version 2422 (from the readme.chromium file in the Angle root folder).


### kb...@chromium.org (2015-08-10)

Jamie: could you please investigate this? CC'ing Geoff and Corentin too. Not sure whether this might be fixed already.


### jm...@chromium.org (2015-08-10)

OK, will look.

### jm...@chromium.org (2015-08-10)

CL up at https://chromium-review.googlesource.com/#/c/292391/ , PTAL

### cl...@chromium.org (2015-08-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/3dfcdcb635dadabf8f2239347dbb512929d50f24

commit 3dfcdcb635dadabf8f2239347dbb512929d50f24
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Aug 10 18:28:54 2015

D3D: Fix buffer overflow in VertexBuffer.cpp.

Under certain situations an integer overflow could lead to ANGLE
writing to places where it shouldn't.

BUG=518206

Change-Id: I9217685daecb160a4072fbf79c26e5bee9f4621e
Reviewed-on: https://chromium-review.googlesource.com/292391
Reviewed-by: Corentin Wallez <cwallez@chromium.org>
Tested-by: Jamie Madill <jmadill@chromium.org>

[modify] http://crrev.com/3dfcdcb635dadabf8f2239347dbb512929d50f24/src/libANGLE/renderer/d3d/VertexBuffer.cpp
[modify] http://crrev.com/3dfcdcb635dadabf8f2239347dbb512929d50f24/src/tests/gl_tests/BufferDataTest.cpp


### bu...@chromium.org (2015-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/3dfcdcb635dadabf8f2239347dbb512929d50f24

commit 3dfcdcb635dadabf8f2239347dbb512929d50f24
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Aug 10 18:28:54 2015

D3D: Fix buffer overflow in VertexBuffer.cpp.

Under certain situations an integer overflow could lead to ANGLE
writing to places where it shouldn't.

BUG=518206

Change-Id: I9217685daecb160a4072fbf79c26e5bee9f4621e
Reviewed-on: https://chromium-review.googlesource.com/292391
Reviewed-by: Corentin Wallez <cwallez@chromium.org>
Tested-by: Jamie Madill <jmadill@chromium.org>

[modify] http://crrev.com/3dfcdcb635dadabf8f2239347dbb512929d50f24/src/libANGLE/renderer/d3d/VertexBuffer.cpp
[modify] http://crrev.com/3dfcdcb635dadabf8f2239347dbb512929d50f24/src/tests/gl_tests/BufferDataTest.cpp


### bu...@chromium.org (2015-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/3dfcdcb635dadabf8f2239347dbb512929d50f24

commit 3dfcdcb635dadabf8f2239347dbb512929d50f24
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Aug 10 18:28:54 2015

D3D: Fix buffer overflow in VertexBuffer.cpp.

Under certain situations an integer overflow could lead to ANGLE
writing to places where it shouldn't.

BUG=518206

Change-Id: I9217685daecb160a4072fbf79c26e5bee9f4621e
Reviewed-on: https://chromium-review.googlesource.com/292391
Reviewed-by: Corentin Wallez <cwallez@chromium.org>
Tested-by: Jamie Madill <jmadill@chromium.org>

[modify] http://crrev.com/3dfcdcb635dadabf8f2239347dbb512929d50f24/src/libANGLE/renderer/d3d/VertexBuffer.cpp
[modify] http://crrev.com/3dfcdcb635dadabf8f2239347dbb512929d50f24/src/tests/gl_tests/BufferDataTest.cpp


### bu...@chromium.org (2015-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/35da6f914f054c08b1e8ae8181d0cd964834d27f

commit 35da6f914f054c08b1e8ae8181d0cd964834d27f
Author: jmadill <jmadill@chromium.org>
Date: Tue Aug 11 01:04:49 2015

Roll ANGLE 519a5be..3dfcdcb

https://chromium.googlesource.com/angle/angle.git/+log/519a5be..3dfcdcb

BUG=504872,518206,510151

TEST=bots
TBR=bajones@chromium.org,zmo@chromium.org

Review URL: https://codereview.chromium.org/1283903002

Cr-Commit-Position: refs/heads/master@{#342763}

[modify] http://crrev.com/35da6f914f054c08b1e8ae8181d0cd964834d27f/DEPS


### jm...@chromium.org (2015-08-11)

Fix currently baking in Canary. Marking as merge-requested for M45,

Fix CL is here: https://chromium-review.googlesource.com/292391

Fix should be quite minimal, and plugs a high-impact security hole. Also might want to request for M44.

googlebugs@lastland.net if you could verify as well that would help.

### [Deleted User] (2015-08-11)

> googlebugs@lastland.net if you could verify as well that would help.

I'll try merging the fix into my next Firefox build and testing it. That probably will occur tomorrow.

### [Deleted User] (2015-08-11)

BTW, where should I report security bugs after Google Code goes read-only?

### pe...@google.com (2015-08-12)

Approved for M45 (branch: 2454)

### cl...@chromium.org (2015-08-12)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-08-12)

[Empty comment from Monorail migration]

### jm...@chromium.org (2015-08-12)

> BTW, where should I report security bugs after Google Code goes read-only?

Still here. The Chromium part of Google code will keep operating as usual after the rest goes read-only.

### bu...@chromium.org (2015-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/dd235e051a57f48e25164833c0d20f54a30855a0

commit dd235e051a57f48e25164833c0d20f54a30855a0
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Aug 10 18:28:54 2015

D3D: Fix buffer overflow in VertexBuffer.cpp.

Under certain situations an integer overflow could lead to ANGLE
writing to places where it shouldn't.

BUG=518206

Change-Id: I9217685daecb160a4072fbf79c26e5bee9f4621e
Reviewed-on: https://chromium-review.googlesource.com/293200
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Tested-by: Jamie Madill <jmadill@chromium.org>

[modify] http://crrev.com/dd235e051a57f48e25164833c0d20f54a30855a0/src/libANGLE/renderer/d3d/VertexBuffer.cpp
[modify] http://crrev.com/dd235e051a57f48e25164833c0d20f54a30855a0/src/tests/gl_tests/BufferDataTest.cpp


### bu...@chromium.org (2015-08-12)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=77272

------------------------------------------------------------------
r77272 | jmadill@google.com | 2015-08-12T13:57:27.530595Z

-----------------------------------------------------------------

### [Deleted User] (2015-08-13)

My build broke, so I haven't yet tested the fix. I should be able to test it today.

### jm...@chromium.org (2015-08-13)

Thanks, let me know today and I'll mark it merge-requested for M44.

### [Deleted User] (2015-08-13)

There is some exotic problem with FF x64 builds. I am attempting to diagnose the latest failure, having to do with undefined symbols like __imp_fprintf when linking mozalloc.dll. I'll keep you updated. I've previously only built FF x86, which is why I hadn't ironed out these problems earlier.

Do you happen to have any clues?

### jm...@chromium.org (2015-08-14)

Not sure about the undefined symbols -- are those something to do with ANGLE, or totally separate?

Going to mark merge requested for M44, since we probably shouldn't wait too much longer. 

Fix baked in Canary for a while, and merged to M45.

Fix CL is here: https://chromium-review.googlesource.com/292391

Fix should be quite minimal, and plugs a high-impact security hole.


### pe...@google.com (2015-08-14)

[Automated comment] Request affecting a post-stable build (M44), manual review required.

### pe...@chromium.org (2015-08-14)

Merge approved for m44 branch 2403.

### [Deleted User] (2015-08-14)

OK, I finally got the build working. The new code detects the impending overflow and errors out as expected, preventing control from being transferred to storeVertexAttributes.

### jm...@chromium.org (2015-08-14)

Great, thanks for verifying. Going to merge to M44.

### bu...@chromium.org (2015-08-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/709dc46cbd06c98b7450d702ade3210eef831a70

commit 709dc46cbd06c98b7450d702ade3210eef831a70
Author: Jamie Madill <jmadill@chromium.org>
Date: Mon Aug 10 18:28:54 2015

D3D: Fix buffer overflow in VertexBuffer.cpp.

Under certain situations an integer overflow could lead to ANGLE
writing to places where it shouldn't.

BUG=518206

Change-Id: I9217685daecb160a4072fbf79c26e5bee9f4621e
Reviewed-on: https://chromium-review.googlesource.com/293820
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Tested-by: Jamie Madill <jmadill@chromium.org>

[modify] http://crrev.com/709dc46cbd06c98b7450d702ade3210eef831a70/src/libANGLE/renderer/d3d/VertexBuffer.cpp
[modify] http://crrev.com/709dc46cbd06c98b7450d702ade3210eef831a70/src/tests/gl_tests/BufferDataTest.cpp


### bu...@chromium.org (2015-08-14)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=77346

------------------------------------------------------------------
r77346 | jmadill@google.com | 2015-08-14T17:52:26.175702Z

-----------------------------------------------------------------

### [Deleted User] (2015-08-19)

[Comment Deleted]

### [Deleted User] (2015-08-19)

Is there going to be a bounty for this bug?

### ti...@google.com (2015-08-31)

#34: We'll take it to the reward panel and you should have a decision in a few weeks from now - details here: https://www.google.com/about/appsecurity/chrome-rewards/

### [Deleted User] (2015-08-31)

#35: Thanks.

### ti...@google.com (2015-10-14)

My apologies for the delay here - this one fell off my radar. I'll put in the next panel round.

### cl...@chromium.org (2015-11-18)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-04-22)

The bad news: It took *way* too long to get you an answer here.

The good news: Our reward panel decided to reward you $5,000 for this report. The panel noted that the amount was at the top end of the band due to the great initial report, write-up and POC provided.

Our finance team should be in touch in 7 days to collect your payment details. If that doesn't happen, please email me at timwillis@ or update this bug so that I can chase that for you.

Congratulations and thanks for your extended patience here. 

### ti...@google.com (2016-04-22)

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

This issue was migrated from crbug.com/chromium/518206?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082652)*
