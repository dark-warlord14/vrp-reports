# Security: UAF in: gpu::raster::RasterDecoderImpl::Initialize

| Field | Value |
|-------|-------|
| **Issue ID** | [40071126](https://issues.chromium.org/issues/40071126) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Compositing>OOP-Raster |
| **Platforms** | Mac |
| **Reporter** | zh...@gmail.com |
| **Assignee** | su...@chromium.org |
| **Created** | 2023-09-01 |
| **Bounty** | $15,000.00 |

## Description

**Steps to reproduce the problem:**

1. Download asan-mac-release-1180014
2. Start Chromium on mac `./Chromium.app/Contents/MacOS/Chromium --enable-features=SkiaGraphite --no-sandbox`
3. Visit <http://127.0.0.1:8000/index.html>, wait for UAF

**Problem Description:**  

It is currently unclear when the vulnerability was introduced.Bisect coming soon

**Additional Comments:**

\*\*Chrome version: \*\* 117.0.5932.0 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 56.6 KB)
- [index.html](attachments/index.html) (text/plain, 78 B)
- [poc.mov](attachments/poc.mov) (video/quicktime, 5.5 MB)
- [asan.log](attachments/asan.log) (text/plain, 31.5 KB)

## Timeline

### [Deleted User] (2023-09-01)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-09-01)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-09-01)

[Empty comment from Monorail migration]

### za...@chromium.org (2023-09-01)

Hi geofflang@ can you please take a look at this gpu::raster related bug? Thanks! 

[Monorail components: Internals>Compositing>OOP-Raster]

### [Deleted User] (2023-09-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zh...@gmail.com (2023-09-04)

RCA here:

In the `CurrentGL` struct, a `raw_ptr` pointing to `GLApi` is stored, and the field name is `Api` [1]

```c++
struct GL_EXPORT CurrentGL {
  raw_ptr<GLApi, DanglingUntriaged> Api = nullptr;
  raw_ptr<DriverGL, DanglingUntriaged> Driver = nullptr;
  raw_ptr<const GLVersionInfo, AcrossTasksDanglingUntriaged> Version = nullptr;
};
```

[1] https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/gl_bindings.h;l=531-535;drc=8c0874163bb6f015d7b326c154db9307d53ca8c3

The lifecycle of `CurrentGL` is owned by `GLContext`: [2],this means that when the GLContext object is destroyed, CurrentGL is also destroyed:

[2] https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/gl_context.h;l=340?q=gl_context.h:32


Let's go back to the class with UAF vulnerability, which is `RasterDecoderImpl`:[3]

[3] https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/raster_decoder.cc;l=1112;bpv=0;bpt=0

The `RasterDecoderImpl` class stores a raw_ptr field `api_` pointing to `gl::GLApi`: [4]


[4] https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/raster_decoder.cc;drc=8c0874163bb6f015d7b326c154db9307d53ca8c3;bpv=0;bpt=0;l=976

When the `RasterDecoderImpl::Initialize` function is called, the `api_` field will be assigned a value. The relevant logic is as follows:[5]

[5] https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/gl_bindings.h;drc=8c0874163bb6f015d7b326c154db9307d53ca8c3;bpv=0;bpt=0;l=562

```c++
#define g_current_gl_context GetGlContextForCurrentThread()->Api.get()
```

Here it will try to get the first field `Api` of the `CurrentGL` struct through `GetGlContextForCurrentThread()->Api`.

However, the `GLContext` has been freed before then, so the `CurrentGL` has also been freed early.

So `GetGlContextForCurrentThread()->Api` actually accesses the `Api` field of the struct `CurrentGL` that has been freed, triggering a UAF vulnerability.

This is a GPU use-after-free vulnerability and cannot be protected by MiraclePtr.

### zh...@gmail.com (2023-09-04)

Correct me if I'm wrong,according to the above analysis, the bisect commit should be this one:

https://chromium-review.googlesource.com/c/chromium/src/+/1403977

Because a long time ago [1] , the lifecycle of the `CurrentGL` object has been owned by `GLContext`:

[1] https://codereview.chromium.org/2629633003/patch/20001/5680423082393600

From that point on, there is no relevant logic to ensure that the `GlContext` object is not destroyed when this line is executed [2]

[2] https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/raster_decoder.cc;l=1112;bpv=0;bpt=0

It's just that before, we failed to release the `GlContext` object before executing the sentence `api_ = gl::g_current_gl_context;`, which resulted in the vulnerability never being discovered.

### zh...@gmail.com (2023-09-04)

If you have any further discoveries, please let me know too, this is indeed an interesting vulnerability, I'm still wondering why MiraclePtr doesn't protect against this in this case.

### zh...@gmail.com (2023-09-04)

According to the current analysis, the reason why MiraclePtr cannot protect this vulnerability is as follows:

[1] https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/gl_bindings.h;l=565;drc=8c0874163bb6f015d7b326c154db9307d53ca8c3;bpv=0;bpt=0


```c++
// This #define is here to support autogenerated code.
#define g_current_gl_context GetGlContextForCurrentThread()->Api.get()
#define g_current_gl_driver GetGlContextForCurrentThread()->Driver
#define g_current_gl_version GetGlContextForCurrentThread()->Version.get()
GL_EXPORT CurrentGL*& GetGlContextForCurrentThread(); // here !!! !!! return a *&
```

`GetGlContextForCurrentThread()` returns a raw pointer pointing to the `CurrentGL` reference, so when `GlContext` is destroyed, `CurrentGL` is destroyed, and then the raw pointer pointing to the `CurrentGL` reference is accessed through `GetGlContextForCurrentThread()` again, which will not be protected by MiraclePtr.

### ge...@chromium.org (2023-09-05)

[Empty comment from Monorail migration]

### su...@chromium.org (2023-09-05)

Marking this as Security_Impact-None since Graphite hasn't been launched yet on any channel and moreover we don't plan to ship to stable at least until M119/120.

### su...@chromium.org (2023-09-05)

Ok, I think I know what might be going on. This is a potential sequence of events with Graphite enabled:

1) GL context (say for WebGL) is created which causes GetGlContextForCurrentThread() to be set to it.
2) Some backpressure fences are enqueued on this context.
3) The context is released i.e. current context is now null.
4) The context is destroyed while backpressure fences are enqueued and we enter the main logic in ReleaseBackpressureFences.
5) RasterDecoderImpl::Initialize gets the GetGlContextForCurrentThread() to set api_

The code in GLContextEGL::ReleaseBackpressureFences looks like this:

```
  if (has_backpressure_fences) {
    // If this context is not current, bind this context's API so that the YUV
    // converter can safely destruct
    GLContext* current_context = GetRealCurrent();
    if (current_context != this) {
      SetCurrentGL(GetCurrentGL());
    }

    ...

    // Rebind the current context's API if needed.
    if (current_context && current_context != this) {
      SetCurrentGL(current_context->GetCurrentGL());
    }
  }
```
At the beginning, current_context is null because of 3) and we call SetCurrentGL with the GLContextEGL being destroyed. At the end, we will skip the SetCurrentGL call that's supposed to restore the CurrentGL to the previous value because current_context is null.

The code should IMO be:

```
    // Rebind the current context's API if needed.
    if (current_context != this) {
      SetCurrentGL(current_context ? current_context->GetCurrentGL() : nullptr);
    }
```

This will ensure the GetGlContextForCurrentThread() will be null when RasterDecoderImpl::Initialize runs which will make this is a nullptr deref. That is still an issue so I think we should also guard the code like this:

```
  if (shared_context_state_->GrContextIsGL()) {
    CHECK(shared_context_state_->IsCurrent(/*surface=*/nullptr, /*needs_gl=*/true);
    api_ = gl::g_current_gl_context;
  }
```
This is needed because with Graphite, SharedContextState::MakeCurrent doesn't make the GL context current unless needs_gl = true which is never the case. Without Graphite, needs_gl is ignored as GrContextIsGL is true (Skia runs on GL after all).

### su...@chromium.org (2023-09-05)

> That is still an issue so I think we should also guard the code like this:

I meant "That is still an issue so I think we should also guard the code setting api_ in RasterDecoderImpl::Initialize like this:"

I'm going to try to reproduce this and see what's actually calling SetCurrentGL.

### be...@google.com (2023-09-05)

Adding Hotlist-RBS-Removed for tracking purposes.

### va...@chromium.org (2023-09-06)

I'd remove api_ from RasterDecoder all together. Ideally it should have no api specific bits, but those 2 (mac workaround and glGetError()) can query context before relevant calls.

### gi...@appspot.gserviceaccount.com (2023-09-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/46df8ac690ba1bcbafc82e97ccc32610e1b9f51a

commit 46df8ac690ba1bcbafc82e97ccc32610e1b9f51a
Author: Sunny Sachanandani <sunnyps@chromium.org>
Date: Wed Sep 06 23:18:43 2023

graphite: Do not cache GLApi pointer in RasterDecoder

With Graphite, SharedContextState won't make its GLContext current ever
so the thread local CurrentGL pointer can be null. Do not cache this
nullptr in RasterDecoderImpl::api_, and instead retrieve it when needed
like other we do elsewhere (which is not expensive in the first place).

Bug: 1478112
Change-Id: I48f2c4c708656a040d84d65580e1192fdb1c2d86
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4847892
Commit-Queue: Victor Miura <vmiura@chromium.org>
Reviewed-by: Victor Miura <vmiura@chromium.org>
Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org>
Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1193309}

[modify] https://crrev.com/46df8ac690ba1bcbafc82e97ccc32610e1b9f51a/gpu/command_buffer/service/raster_decoder.cc


### su...@chromium.org (2023-09-06)

[Empty comment from Monorail migration]

### su...@chromium.org (2023-09-06)

This particular issue is fixed by the CL in https://crbug.com/chromium/1478112#c18, but I have another CL in review that makes the CurrentGL setting code a bit more robust: https://chromium-review.googlesource.com/c/chromium/src/+/4846817

### su...@chromium.org (2023-09-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/02192f2ef00110141c17f1255198f60b01f64d1d

commit 02192f2ef00110141c17f1255198f60b01f64d1d
Author: Sunny Sachanandani <sunnyps@chromium.org>
Date: Sat Sep 09 01:55:34 2023

gpu: Fix potential CurrentGL dangling pointer

There's a potential issue with GLContextEGL::ReleaseBackpressureFences
leaving the thread local CurrentGL pointer set if there was no previous
current context. This means that the pointer will be dangling when the
context is destroyed. This ordinarily doesn't happen with Ganesh/GL
since there's almost always a current GL context, but it's possible with
Graphite when SharedContext won't ever make its context current.

This CL also cleans up the code related to setting the thread local
CurrentGL pointer:

- GetGlContextForCurrentThread returns a reference to the thread local
  CurrentGL pointer so it's renamed to ThreadLocalCurrentGL and is
  not exposed via gl_bindings.h (see below).
- GetThreadLocalCurrentGL returns the CurrentGL pointer and is exported
  in gl_bindings.h. It does not return a mutable reference though.
- SetCurrentGL sets the thread local CurrentGL pointer so it's renamed
  to SetThreadLocalCurrentGL to distinguish it from GetCurrentGL which
  is an accessor on the GLContext class.

Bug: 1478112
Change-Id: Idd489ba129b2a59f8fcf5dd4edf379c3e9fe05aa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4846817
Reviewed-by: Zhenyao Mo <zmo@chromium.org>
Commit-Queue: Sunny Sachanandani <sunnyps@chromium.org>
Auto-Submit: Sunny Sachanandani <sunnyps@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1194415}

[modify] https://crrev.com/02192f2ef00110141c17f1255198f60b01f64d1d/ui/gl/gl_implementation.cc
[modify] https://crrev.com/02192f2ef00110141c17f1255198f60b01f64d1d/ui/gl/gl_context_egl.cc
[modify] https://crrev.com/02192f2ef00110141c17f1255198f60b01f64d1d/gpu/command_buffer/service/external_semaphore.cc
[modify] https://crrev.com/02192f2ef00110141c17f1255198f60b01f64d1d/ui/gl/gl_bindings.h
[modify] https://crrev.com/02192f2ef00110141c17f1255198f60b01f64d1d/ui/gl/gl_gl_api_implementation.cc
[modify] https://crrev.com/02192f2ef00110141c17f1255198f60b01f64d1d/ui/gl/gl_gl_api_implementation.h
[modify] https://crrev.com/02192f2ef00110141c17f1255198f60b01f64d1d/ui/gl/gl_context.cc


### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations  zh1x1an1221! The VRP Panel has decided to award you $15,000 for this high-quality GPU security bug report. Thank you for your efforts in discovering and reporting this issue to us -- great work!!!

### zh...@gmail.com (2023-09-15)

Thank you also for your efficient bug fixing work！！！

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1478112?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1423574]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071126)*
