# Security: ANGLE libGLESv2 Integer Overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [40077743](https://issues.chromium.org/issues/40077743) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>GPU |
| **Platforms** | Windows |
| **Reporter** | al...@contextis.co.uk |
| **Assignee** | [Deleted User] |
| **Created** | 2013-07-04 |
| **Bounty** | $1,337.00 |

## Description

Description:		Almost Native Graphics Layer Engine (ANGLE) library Integer Overflow
Versions Affected: 	Google Chrome 27.0.1453.116 m
Category: 		Memory Corruption
Reporter:		Alex Chapman of Context Information Security 

Summary:
--------

The Almost Native Graphics Layer Engine (ANGLE) library as used in Google Chrome is vulnerable to an integer overflow vulnerability leading to memory corruption which may allow an attacker to exploit the browser process. The ANGLE library is used by Chrome on Windows as a bridge between the OpenGL ES 2.0 API and DirectX.

Note: As this is a bug in the ANGLE library a bug report has also been submitted to Mozilla.

Analysis:
---------

The issue occurs due to insufficient bounds checking prior to integer multiplication within the Context::drawLineLoop function (libGLESv2/Context.cpp):

    const int spaceNeeded = (count + 1) * sizeof(unsigned int);

    if (!mLineLoopIB)
    {
        mLineLoopIB = new StreamingIndexBuffer(mDevice, INITIAL_INDEX_BUFFER_SIZE, D3DFMT_INDEX32);
    }

    if (mLineLoopIB)
    {
        mLineLoopIB->reserveSpace(spaceNeeded, GL_UNSIGNED_INT);

        UINT offset = 0;
        unsigned int *data = static_cast<unsigned int*>(mLineLoopIB->map(spaceNeeded, &offset));
        startIndex = offset / 4;
        
        if (data)
        {
            switch (type)
            {
              case GL_NONE:   // Non-indexed draw
                for (int i = 0; i < count; i++)
                {
                    data[i] = i;
                }
                data[count] = 0;
                break;

The count variable is directly controlled from javascript with no validation performed by the ANGLE library. Context::drawLineLoop proceeds to request a buffer using the overflowed spaceNeeded variable as the size, and fill the insufficiently allocated memory with data resulting in a heap overflow condition.

The crash occurs within the renderer "gpu-process" (sad tab crash).

Example crash information from Chrome 27.0.1453.116 m:

    (1d48.1614): Access violation - code c0000005 (first chance)
    First chance exceptions are reported before any exception handling.
    This exception may be expected and handled.
    eax=04015000 ebx=7fffffff ecx=002e2c00 edx=00000000 esi=053fa7a8 edi=00000000
    eip=6fb8103c esp=0024e8ac ebp=0024e8bc iopl=0         nv up ei ng nz ac po cy
    cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010293
    libglesv2!Ordinal147+0x239b:
    6fb8103c 890c88          mov     dword ptr [eax+ecx*4],ecx ds:002b:04ba0000=52455343


    ChildEBP RetAddr  Args to Child              
    WARNING: Stack unwind information not available. Following frames may be wrong.
    0024e8bc 6fb827b5 00000000 00000000 00000000 libglesv2!Ordinal147+0x239b
    0024e8e8 6fb6c03c 7ffffffe 00000000 7fffffff libglesv2!Ordinal147+0x3b14
    0024e924 6252486f 00000002 00000000 7fffffff libglesv2!glDrawArrays+0x4f
    0024e968 62524922 6338d5d0 00000000 00000002 chrome_61100000!gpu::gles2::GLES2DecoderImpl::DoDrawArrays+0x17d [c:\b\build\slave\win\build\src\gpu\command_buffer\service\gles2_cmd_decoder.cc @ 6245]
    0024e988 6252a218 00000000 064108c8 00000232 chrome_61100000!gpu::gles2::GLES2DecoderImpl::HandleDrawArrays+0x1d [c:\b\build\slave\win\build\src\gpu\command_buffer\service\gles2_cmd_decoder.cc @ 6271]
    0024ea84 6252e1fa 00000134 00000003 064108c8 chrome_61100000!gpu::gles2::GLES2DecoderImpl::DoCommand+0x3fe [c:\b\build\slave\win\build\src\gpu\command_buffer\service\gles2_cmd_decoder.cc @ 3592]
    0024eab0 6251256a 00000000 0545b688 05455600 chrome_61100000!gpu::CommandParser::ProcessCommand+0xb6 [c:\b\build\slave\win\build\src\gpu\command_buffer\service\cmd_parser.cc @ 72]
    0024ed14 62513a85 05461d40 6367b8d3 0024ed64 chrome_61100000!gpu::GpuScheduler::PutChanged+0xe8 [c:\b\build\slave\win\build\src\gpu\command_buffer\service\gpu_scheduler.cc @ 78]
    0024ed24 624a81af 00000243 00b0e0c0 05455604 chrome_61100000!gpu::CommandBufferService::Flush+0x26 [c:\b\build\slave\win\build\src\gpu\command_buffer\service\command_buffer_service.cc @ 92]
    0024ed64 6280b19e 00000243 00000019 00000243 chrome_61100000!content::GpuCommandBufferStub::OnAsyncFlush+0xb5 [c:\b\build\slave\win\build\src\content\common\gpu\gpu_command_buffer_stub.cc @ 669]
    0024ed7c 624a9f46 00b0e0c0 05455600 05455600 chrome_61100000!FileSystemHostMsg_CancelWrite::Dispatch<content::FileAPIMessageFilter,content::FileAPIMessageFilter,void (__thiscall content::FileAPIMessageFilter::*)(int,int)>+0x26 [c:\b\build\slave\win\build\src\content\common\fileapi\file_system_messages.h @ 138]
    0024eee8 611f0adc 01b0e0c0 00b0e0c0 0024ef34 chrome_61100000!content::GpuCommandBufferStub::OnMessageReceived+0x225 [c:\b\build\slave\win\build\src\content\common\gpu\gpu_command_buffer_stub.cc @ 187]
    0024eef8 624a461e 00b0e0c0 768fd383 00a6c250 chrome_61100000!content::MessageRouter::RouteMessage+0x24 [c:\b\build\slave\win\build\src\content\common\message_router.cc @ 50]
    0024ef34 61331af6 0024f5d8 0024ef54 613319a7 chrome_61100000!content::GpuChannel::HandleMessage+0xad [c:\b\build\slave\win\build\src\content\common\gpu\gpu_channel.cc @ 799]
    0024ef40 613319a7 624a4571 00000000 00a6c250 chrome_61100000!base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall ChromeToMobileService::*)(void)>,void __cdecl(base::WeakPtr<ChromeToMobileService> const &)>::MakeItSo+0x37 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 883]
    0024ef54 6113425b 00a6c240 0024f5d8 00a6c244 chrome_61100000!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall ChromeToMobileService::*)(void)>,void __cdecl(ChromeToMobileService *),void __cdecl(base::WeakPtr<ChromeToMobileService>)>,void __cdecl(ChromeToMobileService *)>::Run+0x15 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1173]
    0024efe8 61133c5e 0024f5d8 0024f010 00a1fe70 chrome_61100000!MessageLoop::RunTask+0x341 [c:\b\build\slave\win\build\src\base\message_loop.cc @ 478]


In addition to the above issue, a bug in the NVIDIA graphics driver (version information in gfx_driver_version.txt) and insufficient validation of the size of allocated memory returned by a call to IDirect3DDevice9::CreateIndexBuffer in StreamingIndexBuffer::reserveSpace (libGLESv2/IndexDataManager.cpp) can also trigger a similar heap overflow condition. With the buggy NVIDIA driver, calls to IDirect3DDevice9::CreateIndexBuffer with large memory sizes (e.g. 0xFFFF0004) fail to allocate the requested amount of memory, but return a success result (HRESULT 0). Subsequent code in StreamingIndexBuffer::reserveSpace does not check the size of memory allocated before returning the buffer to the Context::drawLineLoop function (libGLESv2/Context.cpp) to be used. Context::drawLineLoop proceeds to fill the insufficiently allocated memory with data, assuming a successful memory allocation, resulting in a heap overflow condition: 

Example crash information from Chrome 27.0.1453.116 m:

    (21d8.1b44): Access violation - code c0000005 (first chance)
    First chance exceptions are reported before any exception handling.
    This exception may be expected and handled.
    eax=044aa000 ebx=3fffc000 ecx=002c5800 edx=00000000 esi=034d2fc8 edi=00000000
    eip=6e35103c esp=002ce46c ebp=002ce47c iopl=0         nv up ei ng nz na pe cy
    cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010287
    libglesv2!Ordinal147+0x239b:
    6e35103c 890c88          mov     dword ptr [eax+ecx*4],ecx ds:002b:04fc0000=52455343


    ChildEBP RetAddr  Args to Child              
    WARNING: Stack unwind information not available. Following frames may be wrong.
    002ce47c 6e3527b5 00000000 00000000 00000000 libglesv2!Ordinal147+0x239b
    002ce4a8 6e33c03c 3fffbfff 00000000 3fffc000 libglesv2!Ordinal147+0x3b14
    002ce4e4 650f486f 00000002 00000000 3fffc000 libglesv2!glDrawArrays+0x4f
    002ce528 650f4922 65f5d5d0 00000000 00000002 chrome_63cd0000!gpu::gles2::GLES2DecoderImpl::DoDrawArrays+0x17d [c:\b\build\slave\win\build\src\gpu\command_buffer\service\gles2_cmd_decoder.cc @ 6245]
    002ce548 650fa218 00000000 066808c8 00000232 chrome_63cd0000!gpu::gles2::GLES2DecoderImpl::HandleDrawArrays+0x1d [c:\b\build\slave\win\build\src\gpu\command_buffer\service\gles2_cmd_decoder.cc @ 6271]
    002ce644 650fe1fa 00000134 00000003 066808c8 chrome_63cd0000!gpu::gles2::GLES2DecoderImpl::DoCommand+0x3fe [c:\b\build\slave\win\build\src\gpu\command_buffer\service\gles2_cmd_decoder.cc @ 3592]
    002ce670 650e256a 00000000 02663e08 0266b000 chrome_63cd0000!gpu::CommandParser::ProcessCommand+0xb6 [c:\b\build\slave\win\build\src\gpu\command_buffer\service\cmd_parser.cc @ 72]
    002ce8d4 650e3a85 0274e7e0 6624b8d3 002ce924 chrome_63cd0000!gpu::GpuScheduler::PutChanged+0xe8 [c:\b\build\slave\win\build\src\gpu\command_buffer\service\gpu_scheduler.cc @ 78]
    002ce8e4 650781af 00000243 0274e9c0 0266b004 chrome_63cd0000!gpu::CommandBufferService::Flush+0x26 [c:\b\build\slave\win\build\src\gpu\command_buffer\service\command_buffer_service.cc @ 92]
    002ce924 653db19e 00000243 00000019 00000243 chrome_63cd0000!content::GpuCommandBufferStub::OnAsyncFlush+0xb5 [c:\b\build\slave\win\build\src\content\common\gpu\gpu_command_buffer_stub.cc @ 669]
    002ce93c 65079f46 0274e9c0 0266b000 0266b000 chrome_63cd0000!FileSystemHostMsg_CancelWrite::Dispatch<content::FileAPIMessageFilter,content::FileAPIMessageFilter,void (__thiscall content::FileAPIMessageFilter::*)(int,int)>+0x26 [c:\b\build\slave\win\build\src\content\common\fileapi\file_system_messages.h @ 138]
    002ceaa8 63dc0adc 0174e9c0 0274e9c0 002ceaf4 chrome_63cd0000!content::GpuCommandBufferStub::OnMessageReceived+0x225 [c:\b\build\slave\win\build\src\content\common\gpu\gpu_command_buffer_stub.cc @ 187]
    002ceab8 6507461e 0274e9c0 768fd383 0274e010 chrome_63cd0000!content::MessageRouter::RouteMessage+0x24 [c:\b\build\slave\win\build\src\content\common\message_router.cc @ 50]
    002ceaf4 63f01af6 002cf1a0 002ceb14 63f019a7 chrome_63cd0000!content::GpuChannel::HandleMessage+0xad [c:\b\build\slave\win\build\src\content\common\gpu\gpu_channel.cc @ 799]
    002ceb00 63f019a7 65074571 00000000 0274e010 chrome_63cd0000!base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall ChromeToMobileService::*)(void)>,void __cdecl(base::WeakPtr<ChromeToMobileService> const &)>::MakeItSo+0x37 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 883]
    002ceb14 63d0425b 0274e000 002cf1a0 0274e004 chrome_63cd0000!base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall ChromeToMobileService::*)(void)>,void __cdecl(ChromeToMobileService *),void __cdecl(base::WeakPtr<ChromeToMobileService>)>,void __cdecl(ChromeToMobileService *)>::Run+0x15 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1173]
    002ceba8 63d03c5e 002cf1a0 002cebd0 0265fe70 chrome_63cd0000!MessageLoop::RunTask+0x341 [c:\b\build\slave\win\build\src\base\message_loop.cc @ 478]

These bugs have been tested on Windows 7 and 8.1 x64.

Proof of Concept:
-----------------

Enclosed in the zip file is a HTML file which triggers the interger overflow and subsequent heap corruption on affected browser versions on Windows systems.

* Expected Result of running angle_crash.html = No crash
* Actual Result of running angle_crash.html = Access violation - code c0000005 with heap corrupted


## Attachments

- [20130704 libGLESv2 Integer Overflow.zip](attachments/20130704 libGLESv2 Integer Overflow.zip) (application/zip; charset=binary, 1.3 KB)

## Timeline

### ke...@chromium.org (2013-07-04)

Thanks for the report. I can verify a GPU process crash.

vangelis: can you please find somebody to investigate this, and file a bug in the ANGLE tracker?

### sc...@gmail.com (2013-07-04)

[+kbr -- I bet this one interests you too]

### sc...@gmail.com (2013-07-04)

@alex.chapman: BTW, nice report, thanks.

### [Deleted User] (2013-07-08)

Shannon, can you please have a look and pass it along as needed? Thanks!


### sh...@chromium.org (2013-07-08)

This affects legacy ANGLE since at least January 2012, as well as master and es3proto branches. In master and es3proto branches, it will affect draw calls using triangle fan primitives in addition to line loops.

Tracking in ANGLE https://crbug.com/chromium/444.

### me...@chromium.org (2013-07-09)

[Empty comment from Monorail migration]

### me...@chromium.org (2013-07-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-11)

Looks like https://code.google.com/p/angleproject/issues/detail?id=444 is almost ready for checkin.

### sh...@chromium.org (2013-07-11)

Fix has landed in ANGLE's legacy and master branches.

### in...@chromium.org (2013-07-11)

Apatrick@, can you please uptake the angle fix in chromium and help to cherry pick fix in m29 as well. Thanks!

### in...@chromium.org (2013-07-24)

Apatrick@, friendly ping. Has the angle fix landed in chromium trunk ??

### [Deleted User] (2013-07-26)

In progress for trunk:
https://codereview.chromium.org/20795003/

### [Deleted User] (2013-07-26)

I had to abandon the patch in #12. Now here for trunk:
https://codereview.chromium.org/20723006/

And this is to test the cherry-picking for M29:
https://codereview.chromium.org/20774004/

### [Deleted User] (2013-07-31)

The fixes are now rolled into trunk. Canary 30.0.1582.0 has them. I will watch stability for a bit and then request merge to 29.

### sc...@gmail.com (2013-07-31)

@apatrick: would you mind following up on the patches? For example, I see these things:

1)

    if (static_cast<unsigned int>(count + 1) > (std::numeric_limits<unsigned int>::max() / sizeof(unsigned int)))
    {
        ERR("Could not create a 32-bit looping index buffer for GL_LINE_LOOP, too many indices required.");
        return gl::error(GL_OUT_OF_MEMORY);
    }

    const unsigned int spaceNeeded = (count + 1) * sizeof(unsigned int);
    if (!mLineLoopIB->reserveBufferSpace(spaceNeeded, GL_UNSIGNED_INT))

a) What if count is UINT_MAX? (or, -1 as a signed value). "count + 1" will overflow to 0 and not enough space will be allocated.
b) The check is done using unsigned values, but spaceNeeded is signed. What happens if a large "count" value results in a negative speceNeeded result? This may cause mayhem.

2)

    const unsigned int numTris = count - 2;

    if (numTris * 3 > (std::numeric_limits<unsigned int>::max() / sizeof(unsigned int)))
    {
        ERR("Could not create a scratch index buffer for GL_TRIANGLE_FAN, too many indices required.");
        return gl::error(GL_OUT_OF_MEMORY);
    }

    const unsigned int spaceNeeded = (numTris * 3) * sizeof(unsigned int);
    if (!mTriangleFanIB->reserveBufferSpace(spaceNeeded, GL_UNSIGNED_INT))

a) This looks like this might block large values of "numTris" but NOT _very large_ values, because there could well be an integer overflow on the LHS as part of "numTris * 3". I do hope I'm wrong but it looks suspect.
b) What if "count" is just 0 or 1? Is this checked elsewhere? If not, wouldn't "count - 2" suffer integer underflow?

### [Deleted User] (2013-07-31)

@scarybeasts, inferno asked me to merge these to trunk and M29. See #11. I didn't actually work on them.

### sc...@gmail.com (2013-07-31)

@apatrick: yeah, sorry I wasn't clear, I wanted to make sure the people who did work on these are contacted.

### [Deleted User] (2013-07-31)

Oh I see. shannonwoods is on the cc list.

### ge...@chromium.org (2013-07-31)

Looking into this now, will have fixes up shortly.

### ge...@chromium.org (2013-07-31)

I've created the patch sets to fix the issues (if anyone wanted to provide additional reviews):
master: https://codereview.appspot.com/12196043/
legacy: https://codereview.appspot.com/12199043
es3proto: https://codereview.appspot.com/12200043


### [Deleted User] (2013-08-07)

I have merged the patches into an angle branch for M29. It's here:

https://code.google.com/p/angleproject/source/browse/?name=chrome_m29

See the changes after f576cb24c8fc, which is what 1547 references in the buildspec.

### ke...@google.com (2013-08-08)

29 is basically done, and respins are only for release blockers.  I'll let Chris decide what he wants to do here, but this certainly needs trunk bake time first.

### [Deleted User] (2013-08-12)

The buildspec change is ready here. I just need yes or no.

https://chromereviews.googleplex.com/9623014

### ke...@google.com (2013-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2013-08-12)

Noticed this was labelled M-27.

### sc...@gmail.com (2013-08-13)

Looks like the buildspec change for the M29 branch was landed? Switching to Merge-Merged. Let me know if I misunderstood.

### pa...@chromium.org (2013-08-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-08-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-20)

Hey Alex,

Thanks again for the report. On top of being a cool bug, the reward panel was impressed with the quality of your report, so we're going to give this one $1337. Someone should be in touch to get your payment info within a few weeks.

### al...@contextis.co.uk (2013-08-22)

Brilliant, thanks for investigating and fixing this one.

Look forward to working with you all again in the future.
Cheers,
Alex

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


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

This issue was migrated from crbug.com/chromium/257363?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>GPU]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077743)*
