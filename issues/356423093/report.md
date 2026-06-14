# Security: segment fault in dawn DXC

| Field | Value |
|-------|-------|
| **Issue ID** | [356423093](https://issues.chromium.org/issues/356423093) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>WebGL |
| **Platforms** | Windows |
| **Reporter** | de...@gmail.com |
| **Assignee** | am...@google.com |
| **Created** | 2024-07-31 |
| **Bounty** | $10,000.00 |

## Description

## Reproduce

1. Download Dawn
   <https://dawn.googlesource.com/dawn/+/HEAD/docs/building.md>
2. Build tint:
   `gn gen out/test --args="is_debug=true" && ninja -C out/test tint`
   or
   `gn gen out/test --args="is_debug=false" && ninja -C out/test tint`
3. run: `out/test/tint --format "hlsl" poc.wgsl --dxc out/dxc_harness/libdxcompiler.so"`

## CRASH LOG

### DEBUG OUTPUT

```
tint: ../../third_party/dxc/lib/IR/Constants.cpp:1379: static ConstantAggregateZero *llvm::ConstantAggregateZero::get(Type *): Assertion `(Ty->isStructTy() || Ty->isArrayTy() || Ty->isVectorTy()) && "Cannot create an aggregate zero of non-aggregate type!"' failed.

```
### RELEASE OUTPUT

```
segmentation fault 

```
## Other

I submitted this vulnerability to dxc two weeks ago (<https://github.com/microsoft/DirectXShaderCompiler/security/advisories/GHSA-cj56-xpmc-42mv>), but they haven't responded at all. Since this poc is simple enough, it also affects chromium.

@ [amaiorano@google.com](mailto:amaiorano@google.com). I know you have been addressing the security issues of dxc in chromium. Could you take a look?

## Attachments

- [test.wgsl](attachments/test.wgsl) (application/octet-stream, 1.1 KB)
- [test.html](attachments/test.html) (text/html, 2.5 KB)

## Timeline

### kr...@google.com (2024-08-02)

Can you run it with ASAN? Right now there is not enough information to determine severity.

### de...@gmail.com (2024-08-05)

I'm unable to determine the severity of the problem. Please CC to [amaiorano@google.com](mailto:amaiorano@google.com) for a look.

### pe...@google.com (2024-08-05)

Thank you for providing more feedback. Adding the requester to the CC list.

### pe...@google.com (2024-08-05)

The NextAction date has arrived: 2024-08-05
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### kr...@google.com (2024-08-05)

Unable to determine the severity, so setting S1 provisionally. Please update as needed.

### kr...@google.com (2024-08-05)

Setting Found-In to current extended stable

### pe...@google.com (2024-08-06)

Setting milestone because of s0/s1 severity.

### am...@google.com (2024-08-09)

Attaching a test.html file that contains the attached wgsl, and that reproduces the GPU process crash when opened in Chrome. [dessertgelatin@gmail.com](mailto:dessertgelatin@gmail.com) in the future, please also attach a similar html file. You should be able to reproduce asan errors using a [prebuilt ASAN build](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/asan.md#pre_built-chrome-binaries) if it doesn't reproduce in Canary.

### am...@google.com (2024-08-09)

Opened a fix PR on DXC: <https://github.com/microsoft/DirectXShaderCompiler/pull/6855>

### am...@google.com (2024-08-13)

- Upstream fix landed: <https://github.com/microsoft/DirectXShaderCompiler/pull/6855>
- Fix rolled from DXC mirror into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/202174>
- Fix rolled from Dawn into Chromium: <https://chromium-review.googlesource.com/c/chromium/src/+/5782591>

### am...@google.com (2024-08-13)

- Opening `test.html` from [comment #9](https://issues.chromium.org/issues/356423093#comment9) in `chromium-129.0.6646.0-win64-asan` results in GPU crash, while opening it in `chromium-129.0.6654.0-win64-asan` it no longer crashes.

### pe...@google.com (2024-08-13)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127, 128].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@google.com (2024-08-13)

1. Which CLs should be backmerged? (Please include Gerrit links.)

- Upstream fix landed: <https://github.com/microsoft/DirectXShaderCompiler/pull/6855>
- Fix rolled from DXC mirror into Dawn: <https://dawn-review.googlesource.com/c/dawn/+/202174>
- Fix rolled from Dawn into Chromium: <https://chromium-review.googlesource.com/c/chromium/src/+/5782591>

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes.

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

Opening `test.html` from [comment #9](https://issues.chromium.org/issues/356423093#comment9) in `chromium-129.0.6646.0-win64-asan` results in GPU crash, while opening it in `chromium-129.0.6654.0-win64-asan` it no longer crashes.

### am...@chromium.org (2024-08-13)

`I submitted this vulnerability to dxc two weeks ago (https://github.com/microsoft/DirectXShaderCompiler/security/advisories/GHSA-cj56-xpmc-42mv), but they haven't responded at all. Since this poc is simple enough, it also affects chromium.` for future reference, DirectX compiler is owned by MSFT. These bugs can be submitted directly upstream to Microsoft via MSRC (<https://msrc.microsoft.com/report/vulnerability/new>)

### am...@chromium.org (2024-08-13)

Since the DAWN -> Chromium roll just landed < 24 hours ago, going to let this get a bit more bake time before I review for backmerge

### de...@gmail.com (2024-08-13)

Thank you for your reply. I previously submitted other dxc issues to Microsoft via msrc, but they marked them as low and will not fix them. Because dxc is similar to sqlite as a basic library, vulnerabilities sometimes depend on whether the upper-layer application can pass robust hlsl to it. Otherwise, it is not a remote attack surface and Microsoft will not address it. So this seems to be the responsibility of dawn and it extremely affects the security of chrome. So I will still submit to chrome. Thank you very much for your attention to security.

### de...@gmail.com (2024-08-13)

Regarding how to submit dxc vulnerabilities to Google, I and other developers have discussed in other issues. Only dxc vulnerabilities that can be triggered through webgpu will I submit to Google. In fact, I found that there are too many vulnerabilities in dxc and it can crash at will. Since we cannot independently render d3d, it seems that we can only increase robustness at the upper layer. Thanks again to Chrome for its emphasis on security. Only you will solve these security problems.

### de...@gmail.com (2024-08-13)

Hi, Amy, please understand dxc as another sqlite. In a sense, we are discussing webgpu and websql, not just dxc and sqlite. So this seems to be in line with Google's vulnerability reward program because third parties will not solve these vulnerabilities that can lead to chrome sandbox escapes. For them, this doesn't even belong to the remote attack surface. So this may have to continue to be submitted to Google for processing. I tried to contact Microsoft, but failed. They didn't treat it as a remote attack surface and responded negatively.

### am...@chromium.org (2024-08-13)

Hello! Apologies for not responding sooner -- I'm just now seeing your messages (thank you for the ping). You are very welcome to continue to report these issues in DirectX, especially when there's demonstrated impact in Chrome, directly to us. My sincere apologies if my comment in c#15 was able to be interpreted as we were not considering these in our scope or that we did not want to receive these reports. That is absolutely not the case. I only made my comment in [comment #15](https://issues.chromium.org/issues/356423093#comment15) since you specifically mentioned in your original report that you tried reporting them via DirectX github and they were unresponsive. I wanted to hope you would have a better reporting experience if you reported those issues to MSRC, especially since this is the guidance that Microsoft has given directly to us and what has been requested.

I'm sorry to hear this has not been your experience.

As you mentioned, we have definitely rewarded these DXC bugs in the past and our GPU team has been kind enough to land patches upstream for not just us, but other downstream entities that use DXC.
We'll continue to do that so long as your keep demonstrating impact in Chrome. So please do not take my comment in c#15 as a request to not report them to us or interpret it as that we won't consider them reward eligible. We'll happily accept them and they're definitely within the scope of our program. We have no plans to change that.

### de...@gmail.com (2024-08-14)

Hi, Amy, Thank you for your reply. Additionally, even through MSRC, they won't respond or fix it. I have tried all these.

### sp...@google.com (2024-08-16)

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

Congratulations on another one! Thank you for your efforts and reporting this issue to us!

### am...@chromium.org (2024-08-17)

no issues apparent since the Dawn -> Chromium roll <https://chromium-review.googlesource.com/c/chromium/src/+/5782591> with the upstream DXC fix was landed; M128 merge approved, please merge this fix to branch 6533 at your earliest convenience

M128 Stable RC has already been cut earlier this week for release next week; unless there is a recut, this will go into the first update.

### pe...@google.com (2024-08-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-08-21)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6533

commit f788a944a6fc1c8db0c7ea985f82eae0a9baa0dc
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Wed Aug 21 09:33:18 2024

    scalarrepl-param-hlsl: fix zero replacement in entry (#6855)
    
    This is the same fix as was done in
    https://github.com/microsoft/DirectXShaderCompiler/pull/6516 except that
    this is for replace uses of zero-init for instructions in the entry
    block.
    
    Bug: 356423093
    Change-Id: I3f56e7ee00c33551a9d9063615b3dbd9af1e3272
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5804181
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: David Neto <dneto@google.com>

M       lib/Transforms/Scalar/ScalarReplAggregatesHLSL.cpp
A       tools/clang/test/DXC/Passes/ScalarReplHLSL/scalarrepl-param-hlsl-entry-replace-zero-recurse-to-float.ll
A       tools/clang/test/DXC/Passes/ScalarReplHLSL/scalarrepl-param-hlsl-entry-replace-zero-recurse-to-int.ll

https://chromium-review.googlesource.com/5804181


### ap...@google.com (2024-08-21)

Project: dawn
Branch: chromium/6533

commit 22e6cae32f7534edd04a7e8421e0d38b43e8516b
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Wed Aug 21 14:02:02 2024

    DEPS: Update DXC to patched branch
    
    Bug: 356423093
    Change-Id: I596e7554681fa634fc3367ce62dbbe85e6f3a936
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/203354
    Reviewed-by: James Price <jrprice@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/203354


### am...@google.com (2024-08-21)

The fix has been cherry-picked to M128/6533.

### am...@google.com (2024-08-21)

Hmm actually, M128 is not 6533, but 6613. I got confused by [#comment24](https://issues.chromium.org/issues/356423093#comment24). So I have actually merged this to M127/6533. [amyressler@chromium.org](mailto:amyressler@chromium.org) let me know if I need to revert that merge. I assume I need to merge this to M128/6613 now?

### am...@chromium.org (2024-08-21)

EEeesh, I'm so sorry about that. Yes, 6533 is not M128 but M127. It should be fine to leave it. There are no planned releases of M127, and it's not an Extended Stable channel either.
Yes, this should be merged to 6613 -- M128.

### ap...@google.com (2024-08-22)

Project: external/github.com/microsoft/DirectXShaderCompiler
Branch: refs/branch-heads/patches/6613

commit 3ea0e7f6b5f464814d6b896eaf69cbd5ebe7fac4
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Wed Aug 21 16:33:57 2024

    scalarrepl-param-hlsl: fix zero replacement in entry (#6855)
    
    This is the same fix as was done in
    https://github.com/microsoft/DirectXShaderCompiler/pull/6516 except that
    this is for replace uses of zero-init for instructions in the entry
    block.
    
    Bug: 356423093
    Change-Id: Ie41fa096859439be17a9d5d373bba46ddff0d497
    Reviewed-on: https://chromium-review.googlesource.com/c/external/github.com/microsoft/DirectXShaderCompiler/+/5805421
    Reviewed-by: James Price <jrprice@google.com>
    Reviewed-by: David Neto <dneto@google.com>

M       lib/Transforms/Scalar/ScalarReplAggregatesHLSL.cpp
A       tools/clang/test/DXC/Passes/ScalarReplHLSL/scalarrepl-param-hlsl-entry-replace-zero-recurse-to-float.ll
A       tools/clang/test/DXC/Passes/ScalarReplHLSL/scalarrepl-param-hlsl-entry-replace-zero-recurse-to-int.ll

https://chromium-review.googlesource.com/5805421


### ap...@google.com (2024-08-22)

Project: dawn
Branch: chromium/6613

commit 5f86f5a316f4e082b2419d8b954ebb79c2be590d
Author: Antonio Maiorano <amaiorano@google.com>
Date:   Thu Aug 22 17:18:55 2024

    DEPS: Update DXC to patched branch
    
    Bug: 356423093
    Change-Id: I139523c16d7d0d8d8c760c52cd5bf9900458be49
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/203574
    Reviewed-by: James Price <jrprice@google.com>

M       DEPS
M       third_party/dxc

https://dawn-review.googlesource.com/203574


### am...@google.com (2024-08-22)

The fix has been actually merged to M128/6613: <https://chromium.googlesource.com/chromium/src.git/+/d77a624a962d972b9de243ae106eac54b01c1f0d>

This should now be complete.

### am...@chromium.org (2024-08-23)

Thanks so much! again, apologies for the earlier error!

### am...@chromium.org (2024-08-27)

Upon further evaluation, while we appreciate the effort here to get this resolved based on potential security relevancy in the GPU process on Chrome, there was no security relevant GPU crash exhibited and no exploitability demonstrated. We're going to need to convert this to a functional issue since there's no exploitability demonstrated or determined.

### pe...@google.com (2024-11-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/356423093)*
