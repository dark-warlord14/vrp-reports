# GPU process crash via WebGPU shader - UAF in SimplifyCFG at SimplifyCFG.cpp:4743

| Field | Value |
|-------|-------|
| **Issue ID** | [344639860](https://issues.chromium.org/issues/344639860) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint, Internals>GPU>Dawn |
| **Platforms** | Windows |
| **Reporter** | wg...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2024-06-04 |
| **Bounty** | $10,000.00 |

## Description

##### VULNERABILITY DETAILS

Chromium translates wgsl shaders via tint to an OS-specific shader format. On Windows, the OS-specific file format is hlsl, processed in dxcompiler.dll. When compiling chrome-generated hlsl files, this triggers an UAF inside the hlsl compiler.

##### VERSION

Chrome Version: Pre-compiled ASAN Chromium 127.0.6520.0 (Developer Build) (64-bit)   

Operating System: Win10 Build 19045.4291

##### REPRODUCTION CASE

Attached is a .html file containing a WebGPU shader. Opening the html file (on windows with the D3D12 backend) crashes the GPU process. Note that the crash may NOT manifest on machines which support the 6.6 shader model.

Reproducing the issue stand-alone on Linux also possible:

1. Compile the standalone.wgsl with tint (commit 3c05043f3c070f78b33b3f51124b661f97ec6512) to hlsl via `./tint standalone.wgsl -o standalone.hlsl`. I also attached standalone.hlsl, but you should get the very same file when compiling standalone.wgsl yourself
2. Compile the hlsl with dxc (commit 978d36221daecfb745fde05a78bd134a389cb934): `./dxc-3.7 standalone.hlsl -T cs_6_2 -HV 2018`. This should trigger an ASAN violation. Setting the shader model to `cs_6_6` prevents the UAF.

I verified this bug is not fixed by the upstream patches for [bug 339169163](https://issues.chromium.org/issues/339169163) or [bug 342428008](https://issues.chromium.org/issues/342428008).

##### Attached:

- html that triggers an ASAN violation in chromium
- wgsl for producing the hlsl shader
- the hlsl shader
- asan log file

## Attachments

- [asanFold](attachments/asanFold) (application/octet-stream, 23.3 KB)
- [indexFoldTwoEntryPhiNode.html](attachments/indexFoldTwoEntryPhiNode.html) (text/html, 3.5 KB)
- [standalone.hlsl](attachments/standalone.hlsl) (application/octet-stream, 1.3 KB)
- [standalone.wgsl](attachments/standalone.wgsl) (application/octet-stream, 1.1 KB)

## Timeline

### ke...@chromium.org (2024-06-04)

Thanks for the report.

Another to amairano@.

### am...@google.com (2024-06-05)

Looking at the ASAN call stack, this looks like an invalid deletion of a PHI node created, deleted, and then UAF'd all in SimplifyCFG. This might be a similar bug as the one [I fixed a few weeks ago](https://github.com/microsoft/DirectXShaderCompiler/pull/6628) for [b/338103465](https://issues.chromium.org/issues/338103465).

### am...@google.com (2024-06-05)

Thanks, [wgslfuzz@gmail.com](mailto:wgslfuzz@gmail.com), as usual for the excellent bug reports. In future, would you mind inlining the ASAN output as you were doing for past bugs? It makes it a lot easier to do an initial triage without having to download files. Thanks!

### pe...@google.com (2024-06-05)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-06-05)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### wg...@gmail.com (2024-06-05)

Absolutely, I'll do so going forwards. And sorry for the potential duplicates, I'm currently de-duplicating the crashes on the instruction pointer of the use. Maybe its better to also consider the address of the free.

### am...@google.com (2024-06-05)

> And sorry for the potential duplicates, I'm currently de-duplicating the crashes on the instruction pointer of the use. Maybe its better to also consider the address of the free.

I think considering the address of the call to free might be better, as the subsequent use could happen in multiple places depending on other variables.

### ch...@google.com (2024-06-07)

Fix is up for review in upstream DXC: <https://github.com/microsoft/DirectXShaderCompiler/pull/6680>

### ch...@google.com (2024-06-11)

The upstream DXC PR has now been merged. We'll test in Canary once it has rolled into Dawn and then Chromium.

### ch...@google.com (2024-06-12)

Fix rolled into Dawn: <https://dawn.googlesource.com/dawn/+/236295367f2e20a213d0b80f06d8b32175e54731>

Dawn rolled into Chromium: <https://chromium-review.googlesource.com/c/chromium/src/+/5625269>

Landed in 128.0.6535.0: <https://chromiumdash.appspot.com/commit/7cb330156dcffbf97c3eda1aba1fb3606641e42b>

@amaiorano: Can you verify the fix on a Windows ASAN Chromium build of Canary 128.0.6535.0?

### am...@google.com (2024-06-12)

Tested by opening attached `indexFoldTwoEntryPhiNode.html` in `chromium-128.0.6535.0-win64-asan`, and no more ASAN failure. Opening the same file in `chromium-127.0.6532.0-win64-asan` produces the ASAN failure reported here.

### pe...@google.com (2024-06-13)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### ch...@google.com (2024-06-13)

1. Which CLs should be backmerged? (Please include Gerrit links.)

- Upstream fix in DXC: <https://github.com/microsoft/DirectXShaderCompiler/pull/6680>
- Fix rolled into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/192928>
- Dawn rolled into Chromium: <https://chromium-review.googlesource.com/c/chromium/src/+/5625269>

Note that the DXC fix will be cherry-picked to a custom branch in our DXC mirror, then updated in a Dawn custom branch for Chrome release.

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes

3. Does this fix pose any potential non-verifiable stability risks?

No

4. Does this fix pose any known compatibility risks?

No

5. Does it require manual verification by the test team? If so, please describe required testing.

Yes. Test by opening indexFoldTwoEntryPhiNode.html in Canary, and note that the GPU process does not crash. The console output does not show any errors, as expected, but simply outputs the GPUDevice and GPURenderPipeline state.

### am...@chromium.org (2024-06-14)

reviewed canary data for <https://chromium-review.googlesource.com/c/chromium/src/+/5625269> based on the changes made in the upstream fix (<https://github.com/microsoft/DirectXShaderCompiler/pull/6680/commits/33259a83ea6ddc0df9b8f528d04a3bda6642348e>) and not seeing any issues on canary related to this change.

Merges approved for M127 Beta and M126 Stable;
Please merge this fix to branches 6533 and 6478 respectively

Please note that M126 Stable update is being cut tomorrow (I believe, thought it maybe pushed to Monday); if this can be merged before RC cut, that would be ideal. If not, it can go into the following week's respin.

### ap...@google.com (2024-06-14)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6478

commit 93c3cf1c787f45336d074da3ad8984116f979c32
Author: Natalie Chouinard <chouinard@google.com>
Date:   Fri Jun 14 13:29:19 2024

    Fix another UAF in SimplifyCFG (#6680)
    
    In certain cases of unreachable code, SimplifyCFG could try to replace a
    phi node with a select where the phi node itself was the select's
    condition. This resulted in an ASAN use-after-free during SimplifyCFG.
    
    The test case added isn't quite ideal because by the end of the
    SimplifyCFG pass, the phi node is restored to its original state both
    before and after this fix. However, an ASAN build of `dxopt` or
    `check-clang-dxc` will identify a heap-use-after-free failure in the
    intermediary steps of this test without this patch and succeeds with it.
    
    This was also fixed in upstream LLVM:
    https://github.com/llvm/llvm-project/commit/602ab248335e1540e82667e74fea44b7f042e112
    
    Bug: 344639860
    Change-Id: I743e96fb172de867c89cad51805edf96387c04ec
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5631796
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>
    Reviewed-by: James Price <jrprice@google.com>

M       lib/Transforms/Utils/SimplifyCFG.cpp
A       tools/clang/test/DXC/Passes/SimplifyCFG/simplifycfg-uaf-phi-condition.ll

https://chromium-review.googlesource.com/5631796


### ap...@google.com (2024-06-14)

Project: dawn
Branch: chromium/6478

commit 7db472f649211faefebee9520fb36b3ffba22e27
Author: Natalie Chouinard <chouinard@google.com>
Date:   Fri Jun 14 13:58:13 2024

    DEPS: Update DXC to patched branch
    
    Bug: 344639860
    Change-Id: I19f98b2df41d5a44d1e2c005af15fbf5540ba85b
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/193860
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>
    Reviewed-by: James Price <jrprice@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/193860


### ch...@google.com (2024-06-14)

Merge to M126 done: <https://chromium.googlesource.com/chromium/src.git/+/2d778735eb5eef4c52f32e7a19a7af6649d23941>

Merge to M127 pending DXC mirror branch creation: <https://crbug.com/347228164>

### ap...@google.com (2024-06-17)

Project: dawn
Branch: chromium/6533

commit 6f9e3469772c29c7277500b7dce1d952c1103a77
Author: Natalie Chouinard <chouinard@google.com>
Date:   Mon Jun 17 14:14:03 2024

    DEPS: Update DXC to patched branch
    
    Bug: 344639860
    Change-Id: I2f3724aada7b55e560582dd7480af05675b02914
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/194120
    Reviewed-by: Antonio Maiorano <amaiorano@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/194120


### ch...@google.com (2024-06-17)

Merge to M127 done now too: <https://chromium.googlesource.com/chromium/src.git/+/2ec092015ca09d8011ea9e31ade09828a73ec3f3>

### sp...@google.com (2024-06-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
memory corruption in the GPU process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-21)

Nice work once again and congratulations! Thank you for reporting this issue to us!

### pe...@google.com (2024-09-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/344639860)*
