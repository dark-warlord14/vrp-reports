# OOB write in SkSLRasterPipelineBuilder

| Field | Value |
|-------|-------|
| **Issue ID** | [355465305](https://issues.chromium.org/issues/355465305) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hy...@gmail.com |
| **Assignee** | br...@google.com |
| **Created** | 2024-07-25 |
| **Bounty** | $10,000.00 |

## Description

---

### Report description

OOB write in SkSLRasterPipelineBuilder

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

#### Steps to reproduce

(Chromium)

1. Apply the `chromium.diff` patch (there's a small binary array to register the glyph in the GPU process and draw it with a DrawSlugOp).
2. Generate drawable\_picture.skp.hh using the python script and add it to `src/gpu/command_buffer/client`.
3. Build and run the browser (an access violation should happen after a few seconds, but maybe you will need to interact with something to trigger the PoC).

(Skia standalone)

1. Apply the 'skia\_DO\_NOT\_USE\_IN\_CHROMIUM.diff' to `FuzzMain.cpp`
2. Generate the `.skp` file using the python script then run `./out/<..>/fuzz`.

#### Vulnerability Details

In Chromium when registering a typeface in the GPU process via the font manager service we are currently allowed to write glyphs with `SkPictures` where deserialization is handled by Skia with restrictions to certain objects like SKSL shaders.

However a `SkPicture` also allows nested objects, and `procs` (the structure that disallows SKSL) is not being properly forwarded to them. So it's still quite trivial to create a situation where arbitrary SKSL is reachable again from a compromised renderer:

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/core/SkPicture.cpp;l=186;drc=4268052f5025da8b928c9e59a04493b396acaad3;bpv=0;bpt=1>
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/core/SkPictureData.cpp;l=528;drc=4268052f5025da8b928c9e59a04493b396acaad3;bpv=1;bpt=1>
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/core/SkPictureData.cpp;l=545;drc=4268052f5025da8b928c9e59a04493b396acaad3>
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/core/SkPictureData.cpp;l=354;drc=2017cd8a8925f180257662f78eaf9eb93e8e394d>
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/core/SkTypeface.cpp;l=250;drc=4268052f5025da8b928c9e59a04493b396acaad3>
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/utils/SkCustomTypeface.cpp;l=510;drc=4268052f5025da8b928c9e59a04493b396acaad3>
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/utils/SkCustomTypeface.cpp;l=485;drc=4268052f5025da8b928c9e59a04493b396acaad3>
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/include/core/SkDrawable.h;l=140;drc=4268052f5025da8b928c9e59a04493b396acaad3>

(The `procs` object is already lost at this point).

For example, currently if we serialize a typeface inside a SkPicture, `procs` will not be forwarded during deserialization, therefore the new nested glyphs will be allowed to deserialize whatever skia flattenables they want.

In the SKSL compiler, looks like function return values do not count against the maximum slot size limit. But they do when building the raster pipeline (the CPU one, which is used by default with `SkRuntimeColorFilter`, even on Ganesh):
(<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/sksl/codegen/SkSLRasterPipelineCodeGenerator.cpp;l=1190>)

```
SlotRange SlotManager::createSlots(std::string name,
                                   const Type& type,
                                   Position pos,
                                   bool isFunctionReturnValue) {
    size_t nslots = type.slotCount();
    ....

    SlotRange result = {fSlotCount, (int)nslots};
    fSlotCount += nslots; // <----- [1]
    return result;
}

```

So we can use some function in an expression that returns a big structure to make `fSlotCount` become large enough to overflow the total slot allocation size [2] which doesn't use safe integers.
Now we have three unsafe spans [3] [4] [5] to work it.
(<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/sksl/codegen/SkSLRasterPipelineBuilder.cpp;l=1672?q=allocateSlotData&ss=chromium>)

```
Program::SlotData Program::allocateSlotData(SkArenaAlloc* alloc) const {
    // Allocate a contiguous slab of slot data for immutables, values, and stack entries.
    const int N = SkOpts::raster_pipeline_highp_stride;
    const int scalarWidth = 1 * sizeof(float);
    const int vectorWidth = N * sizeof(float);
    const int allocSize = vectorWidth * (fNumValueSlots + fNumTempStackSlots) +
                          scalarWidth * fNumImmutableSlots; <---- [2]
    float* slotPtr = static_cast<float*>(alloc->makeBytesAlignedTo(allocSize, vectorWidth));
    sk_bzero(slotPtr, allocSize);

    // Store the temp stack immediately after the values, and immutable data after the stack.
    SlotData s;
    s.values    = SkSpan{slotPtr,        N * fNumValueSlots}; <--- [3]
    s.stack     = SkSpan{s.values.end(), N * fNumTempStackSlots}; <--- [4]
    s.immutable = SkSpan{s.stack.end(),  1 * fNumImmutableSlots}; <--- [5]
    return s;
}

```

The OOB write will happen later [6] with 's.immutable' while trying to copy shader constants to slots:

```
    ...
    // Copy all immutable values into the immutable slots.
    for (const Instruction& inst : fInstructions) {
        if (inst.fOp == BuilderOp::store_immutable_value) {
            slots.immutable[inst.fSlotA] = sk_bit_cast<float>(inst.fImmA); <--- [6]
        }
    }
    ....

```

The SKSL compiler is currently a premium attack surface to research from an attacker's perspective, because looks like it's not ready yet to process untrusted input.

Thanks!

#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

A compromised renderer could use the GPU process to gain a wider attack surface and escape the sandbox.

---

### The cause

#### What version of Chrome have you found the security issue in?

I'm testing in the "main" branch, so "dev" I guess

#### Is the security issue related to a crash?

Yes

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

Renan Rios (@HyHy100)

## Attachments

- [stacktrace.txt](attachments/stacktrace.txt) (text/plain, 17.2 KB)
- [chromium.diff](attachments/chromium.diff) (text/x-patch, 7.6 KB)
- [skia_DO_NOT_USE_IN_CHROMIUM.diff](attachments/skia_DO_NOT_USE_IN_CHROMIUM.diff) (text/x-patch, 1.5 KB)
- [genskpic.py](attachments/genskpic.py) (text/x-python, 7.3 KB)
- [genskpic_M121_AND_BELOW.py](attachments/genskpic_M121_AND_BELOW.py) (text/x-python, 6.8 KB)

## Timeline

### ma...@chromium.org (2024-07-25)

[security shepherd]
This reproduced as a crash of the renderer as described on Linux, but on macOS it manifested as broken rendering and `glRasterCHROMIUM: RasterCHROMIUM: serialization failure` errors.

I have not attempted to bisect this, nor determined when this was introduced. Provisionally setting Found In to extended stable. Please revise this once we understand when this was introduced.

Setting Severity to S1 based on the OOB write. The fact that this requires local patches to reproduces suggest there may be mitigating factors that prevent this from being exploitable directly from web content. If that's the case, it may be appropriate to downgrade the severity.

Assigning to hcm@ per the triage guidelines for Skia bugs.

### hy...@gmail.com (2024-07-26)

Some notes to the team:
1. The python script only generates skpicts for 64-bit systems, this is because I wrote `size_t`'s as `uint64`'s when serializing them in the script.
2. I have only reproduced the GPU process crash on Linux and Windows, haven't tried on MacOS.
3. I reproduced it with both the SW backend and Ganesh in standalone Skia, haven't tried with Graphite.
4. This is a GPU process crash from a compromised renderer, as shown in the stacktrace.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**
Type of crash:  GPU process.

### pe...@google.com (2024-07-26)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-26)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### hy...@gmail.com (2024-07-27)

### Bisect

I tried to reproduce this crash with all skia chrome branches via `skpbench` from <https://chromium.googlesource.com/skia/+refs> since `M115` (the branch where SkRP replaced SkVM) and all of them reproduced the bug.

For branches below `M122` I had to replace the skpict version number with a lower one in the script because the one I'm using right now is too new.

You can see it by yourself by compiling the `M115` skia branch with ASAN and generating the skpict using the attached modified script.

Then load it in skpbench from the command line using:

```
./out/asan/skpbench --src pic.skp --config gles

```

You will see:

```
 accum    median       max       min   stddev  samples  sample_ms  clock  metric  config    bench
./../src/sksl/codegen/SkSLRasterPipelineBuilder.cpp:1515:39: runtime error: signed integer overflow: 32 * 692934984 cannot be represented in type 'int'

```

---

I think making [fAllowSKSL](https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/core/SkReadBuffer.h;l=257;drc=41374c974d98f8cf67134f9ddb8d96d398154dfe) / [fAllowSKSL](https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/include/core/SkSerialProcs.h;l=114;drc=105770df485ace262780d95126bb60b1a16ec340) `false` by default instead of `true` at least in chromium builds could be a nice thing, because it exposes a whole attack surface if accidentally enabled:

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/utils/SkCustomTypeface.cpp;l=485;drc=4268052f5025da8b928c9e59a04493b396acaad3>

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/include/core/SkDrawable.h;l=141;drc=4268052f5025da8b928c9e59a04493b396acaad3>

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/core/SkFlattenable.cpp;l=153;drc=105770df485ace262780d95126bb60b1a16ec340>

---

Edit: I confirmed that the bug is also affecting Android Chrome, however looks like `SkOpts::raster_pipeline_highp_stride` is a platform-dependent value, so I had to recalculate the overflow (maybe it's also the reason why it didn't crash on MacOS).

Note that the GPU process is a highly privileged process there.

```
* thread #15, name = 'CrGpuMain', stop reason = signal SIGSEGV: address access protected (fault address: 0x7311ace699a0)
    frame #0: 0x0000731181f011d4 libskia.cr.so`SkSL::RP::Program::makeStages(this=0x000073125d495990, pipeline=0x000073119c017f50, alloc=0x000073119c018a50, uniforms=SkSpan @ 0x000073119c017e30, slots=0x000073119c017f90) const at SkSLRasterPipelineBuilder.cpp:1859:42
   1856	    // Copy all immutable values into the immutable slots.
   1857	    for (const Instruction& inst : fInstructions) {
   1858	        if (inst.fOp == BuilderOp::store_immutable_value) {
-> 1859	            slots.immutable[inst.fSlotA] = sk_bit_cast<float>(inst.fImmA);
   1860	        }
   1861	    }
   1862
[..]```

```

### ar...@chromium.org (2024-08-06)

Hi @hcm,

I'm following up on this security bug. We aim to have a fix available to all users within 60 days, which would necessitate landing a fix within the first week or two. Could you please confirm you know you are assigned this bug? I will duplicate this message on chat.

Note that this bug is not confirmed at the moment. See #2

Secondary Security Shepherd

### ar...@chromium.org (2024-08-06)

[hcm@chromium.org](mailto:hcm@chromium.org) => [hcm@google.com](mailto:hcm@google.com)

### br...@google.com (2024-08-06)

Quick fix incoming, with a more thorough fix to typeface serialization to follow. (As well as as a separate fix for the SkSL/RP issue).

### ap...@google.com (2024-08-06)

Project: skia
Branch: main

commit 05097fb7293043906fd8aa118c6adc3012c5b074
Author: Brian Osman <brianosman@google.com>
Date:   Tue Aug 06 14:19:00 2024

    Disallow SkSL when deserializing drawables in custom typefaces
    
    Bug: 355465305
    Change-Id: Ifb87db5e8d0d0c29449e6a3e82254189e3f2d33b
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/886696
    Reviewed-by: Ben Wagner <bungeman@google.com>
    Commit-Queue: Brian Osman <brianosman@google.com>

M       src/utils/SkCustomTypeface.cpp

https://skia-review.googlesource.com/886696


### ap...@google.com (2024-08-06)

Project: chromium/src
Branch: main

commit 22fc7992830d36e154fe6f7400fc2abf47e621cc
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Tue Aug 06 21:54:50 2024

    Roll Skia from ae7f55727030 to 968a00456bc5 (5 revisions)
    
    https://skia.googlesource.com/skia.git/+log/ae7f55727030..968a00456bc5
    
    2024-08-06 kjlubick@google.com Refactor sk_app and other test code to be more Bazel friendly
    2024-08-06 kjlubick@google.com [bazel] Add graphite rules for native vulkan backend
    2024-08-06 skia-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 9335f3149740 to 699b3c2a0349 (2 revisions)
    2024-08-06 brianosman@google.com Disallow SkSL when deserializing drawables in custom typefaces
    2024-08-06 kjlubick@google.com [bazel] Add graphite modules for native Metal backend
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/skia-autoroll
    Please CC brianosman@google.com,skiabot@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Skia: https://bugs.chromium.org/p/skia/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
    Cq-Do-Not-Cancel-Tryjobs: true
    Bug: chromium:355465305
    Tbr: brianosman@google.com
    Change-Id: Ia227a36f650da6edea3d03136ceae56a10dafee7
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5767436
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1338126}

M       DEPS
M       third_party/skia

https://chromium-review.googlesource.com/5767436


### br...@google.com (2024-08-06)

+markbrand and +fmalita. I think this bug is strongly related to [Issue 40064341](https://issues.chromium.org/issues/40064341). Reporter has found another way to reach arbitrary picture serialization (and prior the fix, without the SkSL guard being enabled). In talking with other Skia folks - it's actually surprising to us that the custom typeface code is even compiled into Chrome -- it may only be necessary for Skottie (Florin?). If it's not necessary, it would be ideal to actually remove that translation unit entirely.

### fm...@google.com (2024-08-07)

It doesn't look like custom TF was added to Chrome for Skottie specifically, but it's likely true that Skottie is the only client at the moment. Custom TFs are used to support inline/custom Lottie fonts (glyphs encoded as paths), and we only use SkPath glyphs - never SkDrawables. Maybe another option is to disable the SkDrawable API in custom TF for Chrome?

### br...@google.com (2024-08-09)

markrowe@ : I haven't tried to reproduce this in the context of chrome, but the two pieces of this bug are both present for several milestones. We should treat it as being viable in stable. To that end, I'd propose we cherry-pick the targeted fix ([comment #10](https://issues.chromium.org/issues/355465305#comment10)).

### ma...@chromium.org (2024-08-09)

Once the bug has been marked as fixed the automation should start the process to get changes merged to the relevant place (<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-labels.md#TOC-Merge-labels>):

> Once you've landed a complete fix for a security bug, please immediately mark the bug as Fixed. Do not request merges: Sheriffbot will request appropriate merges to beta or stable according to our guidelines. However, it is really helpful if you comment upon any unusual stability or compatibility risks of merging.
> 
> (Some Chromium teams traditionally deal with merges before marking bugs as Fixed. Please don't do that for security bugs.)

### br...@google.com (2024-08-09)

OK. I've gone ahead and marked this as fixed (via the change in [comment #10](https://issues.chromium.org/issues/355465305#comment10)). There are other parts to the vulnerability (and I have other changes in flight), but that first change is the most straightforward patch to prevent running unsafe code in the GPU process.

### ma...@chromium.org (2024-08-09)

Sounds good. Please make sure there is a bug of type `Vulnerability` tracking that remaining work so it will also be visible to the security team.

### pe...@google.com (2024-08-10)

Requesting merge to extended stable (M126) because latest trunk commit (1338126) appears to be after extended stable branch point (1300313).
Requesting merge to stable (M127) because latest trunk commit (1338126) appears to be after stable branch point (1313161).
Requesting merge to beta (M128) because latest trunk commit (1338126) appears to be after beta branch point (1331488).
Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127, 128].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### br...@google.com (2024-08-10)

1. We should backmerge <https://skia-review.googlesource.com/c/skia/+/886696>
2. That CL landed in 129.0.6642.0, and I have not seen any associated stability bugs in Canary (though it only has three days of coverage).
3. No, the scope of the fix is very minor. It disables a code path that was never intended to be reachable (in the GPU process). The current vulnerability is only able to trigger that code path via hand-crafted PaintOps sent from a compromised renderer process.
4. No.
5. No.

Cherry pick CLs:
126: <https://skia-review.googlesource.com/c/skia/+/888576>
127: <https://skia-review.googlesource.com/c/skia/+/887881>
128: <https://skia-review.googlesource.com/c/skia/+/888577>

### am...@chromium.org (2024-08-12)

<https://skia-review.googlesource.com/c/skia/+/886696> approved for M128 -- please merge this fix to branch 6613 at soonest so this fix can be included in tomorrow's cut of M128 Early Stable

The last planned release of M127 Stable is being cut right now for release tomorrow and there are no further planned releases of M126 Extended, so merges to M127 and M126 are not needed.

### ap...@google.com (2024-08-12)

Project: skia
Branch: chrome/m128

commit fb67954b7e76dc59567dd1f87734ada0cd1bc7f6
Author: Brian Osman <brianosman@google.com>
Date:   Tue Aug 06 14:19:00 2024

    Disallow SkSL when deserializing drawables in custom typefaces
    
    Bug: 355465305
    Change-Id: Ifb87db5e8d0d0c29449e6a3e82254189e3f2d33b
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/886696
    Reviewed-by: Ben Wagner <bungeman@google.com>
    Commit-Queue: Brian Osman <brianosman@google.com>
    (cherry picked from commit 05097fb7293043906fd8aa118c6adc3012c5b074)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/888577

M       src/utils/SkCustomTypeface.cpp

https://skia-review.googlesource.com/888577


### br...@google.com (2024-08-12)

I updated the Merge status based on some documentation I found. (The fix has been merged, but I think the blintz rule doesn't know about Skia's chrome release branches). Just wanted to make sure I did it right... (I Removed Approved-128 from `Merge` and added `Merged-128`)?

### pe...@google.com (2024-08-12)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### br...@google.com (2024-08-12)

re: [Comment #23](https://issues.chromium.org/issues/355465305#comment23), No and no. (This was a pre-existing problem).

### ap...@google.com (2024-08-13)

Project: skia
Branch: main

commit d1b243ba90f0698ced6fadc460adb9d66c248946
Author: Brian Osman <brianosman@google.com>
Date:   Fri Aug 09 14:50:21 2024

    [SkSL:RP] Prevent overflow when computing slot allocation size
    
    Bug: 355465305
    Change-Id: Ife25289f7b3489701c67b7dc5d30e473019a1193
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/888376
    Reviewed-by: Julia Lavrova <jlavrova@google.com>
    Commit-Queue: Brian Osman <brianosman@google.com>

M       src/sksl/codegen/SkSLRasterPipelineBuilder.cpp
M       src/sksl/codegen/SkSLRasterPipelineBuilder.h
M       tests/RasterPipelineCodeGeneratorTest.cpp

https://skia-review.googlesource.com/888376


### ap...@google.com (2024-08-13)

Project: chromium/src
Branch: main

commit bd820bd5430a3c07460111b7f2762ab38333f2a8
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Tue Aug 13 19:37:31 2024

    Roll Skia from de92181f1c5f to d1b243ba90f0 (1 revision)
    
    https://skia.googlesource.com/skia.git/+log/de92181f1c5f..d1b243ba90f0
    
    2024-08-13 brianosman@google.com [SkSL:RP] Prevent overflow when computing slot allocation size
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/skia-autoroll
    Please CC michaelludwig@google.com,skiabot@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Skia: https://bugs.chromium.org/p/skia/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
    Cq-Do-Not-Cancel-Tryjobs: true
    Bug: chromium:355465305
    Tbr: michaelludwig@google.com
    Change-Id: I8a61e6825f04bda357903e3168a5cbb4dfd3f7a1
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5786627
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1341188}

M       DEPS
M       third_party/skia

https://chromium-review.googlesource.com/5786627


### sp...@google.com (2024-08-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of memory corruption in a highly privileged process (GPU) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-16)

Congratulations Renan! Thank you for your efforts and reporting this issue to us.

### hy...@gmail.com (2024-08-16)

Thank you VRP and thank you Brian for fixing this bug!

Also, for a valid functional exploit, since this bug can only be triggered from a compromised renderer, am I allowed to create a small renderer patch that sends the skpict/sksl to the GPU process from JavaScript and only exploit the GPU process side? Or do I need to chain it with a renderer RCE?

### am...@chromium.org (2024-08-21)

re: c#29 -- thanks for the question and for your interesting in submitting a functional exploit; yes, please feel free to use a patch to simulate a compromised renderer and focus your exploit on the Skia -> GPU process RCE. Cheers!

### pe...@google.com (2024-09-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-09-12)

1. <http://review.skia.org/896658> for 126, <http://review.skia.org/892616> and <http://review.skia.org/892676> for 120
2. Low, no conflicts
3. 128
4. Yes

### ap...@google.com (2024-09-16)

Project: skia
Branch: chrome/m120

commit a59291ec277803d5b231b1a82ab2275e4823bd3f
Author: Brian Osman <brianosman@google.com>
Date:   Fri Aug 09 14:50:21 2024

    [M120-LTS][SkSL:RP] Prevent overflow when computing slot allocation size
    
    Bug: 355465305
    Change-Id: Ife25289f7b3489701c67b7dc5d30e473019a1193
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/888376
    Commit-Queue: Brian Osman <brianosman@google.com>
    (cherry picked from commit d1b243ba90f0698ced6fadc460adb9d66c248946)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/892676
    Reviewed-by: Michael Ludwig <michaelludwig@google.com>

M       src/sksl/codegen/SkSLRasterPipelineBuilder.cpp
M       src/sksl/codegen/SkSLRasterPipelineBuilder.h
M       tests/RasterPipelineCodeGeneratorTest.cpp

https://skia-review.googlesource.com/892676


### ap...@google.com (2024-09-16)

Project: skia
Branch: chrome/m120

commit f584fa6994d4ee1dbb1b87f5d37e20d2be0f5720
Author: Brian Osman <brianosman@google.com>
Date:   Tue Aug 06 14:19:00 2024

    [M120-LTS] Disallow SkSL when deserializing drawables in custom typefaces
    
    Bug: 355465305
    Change-Id: Ifb87db5e8d0d0c29449e6a3e82254189e3f2d33b
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/886696
    Commit-Queue: Brian Osman <brianosman@google.com>
    (cherry picked from commit 05097fb7293043906fd8aa118c6adc3012c5b074)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/892616
    Reviewed-by: Michael Ludwig <michaelludwig@google.com>

M       src/utils/SkCustomTypeface.cpp

https://skia-review.googlesource.com/892616


### ap...@google.com (2024-09-16)

Project: skia
Branch: chrome/m120

commit 7ba220b34a1b39728bcba5f7fd5a8960557f6042
Author: Michael Ludwig <michaelludwig@google.com>
Date:   Mon Sep 16 19:00:21 2024

    Revert "[M120-LTS][SkSL:RP] Prevent overflow when computing slot allocation size"
    
    This reverts commit a59291ec277803d5b231b1a82ab2275e4823bd3f.
    
    Reason for revert: unit test uses code not in m120.
    
    Original change's description:
    > [M120-LTS][SkSL:RP] Prevent overflow when computing slot allocation size
    >
    > Bug: 355465305
    > Change-Id: Ife25289f7b3489701c67b7dc5d30e473019a1193
    > Reviewed-on: https://skia-review.googlesource.com/c/skia/+/888376
    > Commit-Queue: Brian Osman <brianosman@google.com>
    > (cherry picked from commit d1b243ba90f0698ced6fadc460adb9d66c248946)
    > Reviewed-on: https://skia-review.googlesource.com/c/skia/+/892676
    > Reviewed-by: Michael Ludwig <michaelludwig@google.com>
    
    Bug: 355465305
    Change-Id: I27fe9fa6d769c84955bbbc2ca01c10305d4349b2
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/899717
    Auto-Submit: Michael Ludwig <michaelludwig@google.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

M       src/sksl/codegen/SkSLRasterPipelineBuilder.cpp
M       src/sksl/codegen/SkSLRasterPipelineBuilder.h
M       tests/RasterPipelineCodeGeneratorTest.cpp

https://skia-review.googlesource.com/899717


### ap...@google.com (2024-09-17)

Project: skia
Branch: chrome/m126

commit b5bb998be272be2f78d7c365002066bf9bd412cd
Author: Brian Osman <brianosman@google.com>
Date:   Fri Aug 09 14:50:21 2024

    [M126-LTS][SkSL:RP] Prevent overflow when computing slot allocation size
    
    Bug: 355465305
    Change-Id: Ife25289f7b3489701c67b7dc5d30e473019a1193
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/888376
    Commit-Queue: Brian Osman <brianosman@google.com>
    (cherry picked from commit d1b243ba90f0698ced6fadc460adb9d66c248946)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/896658
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Reviewed-by: Michael Ludwig <michaelludwig@google.com>

M       src/sksl/codegen/SkSLRasterPipelineBuilder.cpp
M       src/sksl/codegen/SkSLRasterPipelineBuilder.h
M       tests/RasterPipelineCodeGeneratorTest.cpp

https://skia-review.googlesource.com/896658


### ap...@google.com (2024-09-18)

Project: skia
Branch: chrome/m120

commit 77fe8841d9ec287eeb3d3f70fc0a674162664064
Author: Michael Ludwig <michaelludwig@google.com>
Date:   Wed Sep 18 20:03:57 2024

    Reland "[M120-LTS][SkSL:RP] Prevent overflow when computing slot allocation size"
    
    This reverts commit 7ba220b34a1b39728bcba5f7fd5a8960557f6042.
    
    Reason for revert: removing unit test that fails to compile in m120
    since all that's needed is the actual SkSL::RP updates for the LTS
    chrome release.
    
    Original change's description:
    > Revert "[M120-LTS][SkSL:RP] Prevent overflow when computing slot allocation size"
    >
    > This reverts commit a59291ec277803d5b231b1a82ab2275e4823bd3f.
    >
    > Reason for revert: unit test uses code not in m120.
    >
    > Original change's description:
    > > [M120-LTS][SkSL:RP] Prevent overflow when computing slot allocation size
    > >
    > > Bug: 355465305
    > > Change-Id: Ife25289f7b3489701c67b7dc5d30e473019a1193
    > > Reviewed-on: https://skia-review.googlesource.com/c/skia/+/888376
    > > Commit-Queue: Brian Osman <brianosman@google.com>
    > > (cherry picked from commit d1b243ba90f0698ced6fadc460adb9d66c248946)
    > > Reviewed-on: https://skia-review.googlesource.com/c/skia/+/892676
    > > Reviewed-by: Michael Ludwig <michaelludwig@google.com>
    >
    > Bug: 355465305
    > Change-Id: I27fe9fa6d769c84955bbbc2ca01c10305d4349b2
    > No-Presubmit: true
    > No-Tree-Checks: true
    > No-Try: true
    > Reviewed-on: https://skia-review.googlesource.com/c/skia/+/899717
    > Auto-Submit: Michael Ludwig <michaelludwig@google.com>
    > Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    
    Bug: 355465305
    Change-Id: Iea2884487313206150f98becbbf22a5a286ff512
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/901140
    Reviewed-by: Robert Phillips <robertphillips@google.com>

M       src/sksl/codegen/SkSLRasterPipelineBuilder.cpp
M       src/sksl/codegen/SkSLRasterPipelineBuilder.h

https://skia-review.googlesource.com/901140


### pe...@google.com (2024-11-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/355465305)*
