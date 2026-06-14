# Uninitialized variable usage in ANGLE may cause a memory disclosure

| Field | Value |
|-------|-------|
| **Issue ID** | [40090901](https://issues.chromium.org/issues/40090901) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | al...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2018-03-24 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Blit11::copyAndConvert(/src/libANGLE/renderer/d3d/d3d11/Blit11.cpp) does not check the return value of ID3D11DeviceContext::Map, when it's called on a system which has Nvidia drivers below a certain version installed:

1515: gl::Error Blit11::copyAndConvert  

...  

1530:{  

1531: ANGLE\_TRY(initResources());  

1532:  

1533: ID3D11DeviceContext \*deviceContext = mRenderer->getDeviceContext();  

...  

1550: // Work around timeouts/TDRs in older NVIDIA drivers.  

1551: if (mRenderer->getWorkarounds().depthStencilBlitExtraCopy)  

1552: {  

1553: D3D11\_MAPPED\_SUBRESOURCE mapped;  

1554: deviceContext->Map(destStaging.get(), 0, D3D11\_MAP\_READ, 0, &mapped);  

1555: deviceContext->UpdateSubresource(dest.get(), destSubresource, nullptr, mapped.pData,  

1556: mapped.RowPitch, mapped.DepthPitch);  

1557: deviceContext->Unmap(destStaging.get(), 0);  

1558: }  

...  

1565: return gl::NoError();  

1566:}

On line 1554, ID3D11DeviceContext::Map is called, and the call is expected to assign a value to the `mapped` local variable. However, Map can fail in certain circumstances, as per the documentation (<https://msdn.microsoft.com/en-us/library/windows/desktop/ff476457(v=vs.85).aspx>). In practice it is known to fail on the OOM condition (<https://community.amd.com/thread/128535>), which may be specifically induced by the attacker. In case that the Map call fails, then ID3D11DeviceContext::UpdateSubresource will be called (line 1555), that will copy whatever data is pointed to by the random content of the uninitialized variable `mapped` to the output buffer provided by the caller.

Reachability analysis:

There are multiple code paths which result in calling the vulnerable function. Consider the following call chain, for example:

(JavaScript WebGL2 context) ->  

Context::blitFramebuffer ->  

Framebuffer::blit ->  

FramebufferD3D::blit ->  

Framebuffer11::blitImpl ->  

Renderer11::blitRenderbufferRect ->  

Blit11::copyStencil ->  

Blit11::copyDepthStencilImpl ->  

Blit11::copyAndConvert.

The vulnerable function Blit11::copyAndConvert is reachable via the blitFramebuffer Javascript function of the WebGL2 context. In case that the vulnerability is triggered, ID3D11DeviceContext::UpdateSubresource will copy data from a random pointer (as it's provided by the random contents of the uninitialized variable `mapped`) to the destination rectangle provided in the arguments to blitFramebuffer. The pixels of the displayed rectangle can then be read back by the attacker via canvas.getImageData (<https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/getImageData>), thereby resulting in memory disclosure.

Exploitation:

1. groom the stack in order to cause a meaningful memory pointer appearing in the `mapped` variable, while it's still uninitialized (via leftowers from previous stack operations)
2. cause an OOM, or otherwise induce a fallible condition to ID3D11DeviceContext::UpdateSubresource
3. call WebGL2's blitFramebuffer (within an initialized WebGL2 context, etc.)
4. draw the leaked buffer on the screen
5. read the drawn pixels back via canvas.getImageData, which represent memory bytes
6. use the obtained memory data (which may contain pointers to executable modules or some sensitive data) to bypass ASLR, or to read user's passwords, for example.

**VERSION**  

The issue was verified in the latest trunk code of ANGLE.

**REPRODUCTION CASE**  

I don't have a repro, since it requires very specific conditions to trigger. Specifically, the vulnerable path of the code will be triggered, if the system has Nvidia drivers, and the drivers version is below 13.6881, as per GenerateWorkarounds() (/src/libANGLE/renderer/d3d/d3d11/renderer11\_utils.cpp).

## Timeline

### el...@chromium.org (2018-03-24)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>ANGLE]

### ct...@chromium.org (2018-03-26)

geofflang@: Could you please take a look and help triage this report? I'm not familiar with the ANGLE and GPU code.

Reporter: How much control over the memory read target are you able to have?

I'm setting this as Severity-Medium (consistent with a renderer memory read vulnerability), and Impact-Head for now. If we have reason to think the vulnerability has been in the code longer, we should update the Security_Impact label appropriately.

### ct...@chromium.org (2018-03-26)

[Empty comment from Monorail migration]

### al...@gmail.com (2018-03-26)

cthomp@: that's a good question. You can see in the call to ID3D11DeviceContext::UpdateSubresource (line 1555) that both width and depth of the read target subresource are attacker controlled, via mapped.RowPitch and mapped.DepthPitch, correspondingly. The variable `mapped` is of type  D3D11_MAPPED_SUBRESOURCE, which is defined as follows:

typedef struct D3D11_MAPPED_SUBRESOURCE {
  void *pData;
  UINT RowPitch;
  UINT DepthPitch;
} D3D11_MAPPED_SUBRESOURCE;

https://msdn.microsoft.com/en-us/library/windows/desktop/ff476182(v=vs.85).aspx

In the above structure, RowPitch and DepthPitch members are located at offsets +sizeof(size_t) and +sizeof(size_t)+4 from the start of the uninitialized structure. Meaning that, if the attacker has succeeded to groom the stack such that this memory contains the values of her choice, then the maximal length of the read operation from the memory pointed to by pData may be up to UINT_MAX*UINT_MAX, or 0x7fffffff'ffffffff.

In addition, it seems from the DirectX documentation (https://msdn.microsoft.com/en-us/library/windows/desktop/ff476486(v=vs.85).aspx), that the UpdateSubresource operation may be constrained and/or defined by the size of the destination resource, which is again attacker controlled, via JavaScript arguments to blitFramebuffer().

I have zero practical experience with DirectX however, and so I may be mistaken in the above theoretical calculations, as far as the inner logic of DirectX operations or/and any constraints inside ID3D11DeviceContext::UpdateSubresource() are concerned.

### sh...@chromium.org (2018-03-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-26)

[Empty comment from Monorail migration]

### ge...@chromium.org (2018-03-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-03-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/a571f28d40342b3e509d1c2a299340b5d451b1a3

commit a571f28d40342b3e509d1c2a299340b5d451b1a3
Author: Geoff Lang <geofflang@chromium.org>
Date: Mon Mar 26 16:19:47 2018

Check result of D3D11 map operation in Blit11::copyAndConvert.

BUG=825503

Change-Id: I407ded1970266bc4fa975850d5700544b9f17b4b
Reviewed-on: https://chromium-review.googlesource.com/980693
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/a571f28d40342b3e509d1c2a299340b5d451b1a3/src/libANGLE/renderer/d3d/d3d11/Blit11.cpp


### ge...@chromium.org (2018-03-26)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-03-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5c849d31db87f160aed138c694ea614bf6d5f1d9

commit 5c849d31db87f160aed138c694ea614bf6d5f1d9
Author: angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Tue Mar 27 03:28:55 2018

Roll src/third_party/angle/ 822a84b19..84fdc62c6 (8 commits)

https://chromium.googlesource.com/angle/angle.git/+log/822a84b1959f..84fdc62c6160

$ git log 822a84b19..84fdc62c6 --date=short --no-merges --format='%ad %ae %s'
2018-03-19 jiawei.shao Fix a compile error when ANGLE_D3D9EX == ANGLE_DISABLED
2017-10-03 geofflang Implement robust resource initialization for OpenGL.
2018-03-20 oetuaho Clean up checkCanBeLValue
2018-01-27 kbr Update stencil validation rules for WebGL
2018-03-19 oetuaho Rely on hash to check for some mangled name matches
2018-03-23 oetuaho Clarify aliasing rules in CHROMIUM_bind_uniform_location
2018-03-26 geofflang Check result of D3D11 map operation in Blit11::copyAndConvert.
2018-03-22 oetuaho Move ReplaceVariable to tree_util directory

Created with:
  roll-dep src/third_party/angle
BUG=chromium:693090,chromium:806557,chromium:823856,chromium:825503


The AutoRoll server is located here: https://angle-chromium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


CQ_INCLUDE_TRYBOTS=luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
TBR=lucferron@chromium.org

Change-Id: Ib864a0492b29de58564d5522977c11d6623dad4a
Reviewed-on: https://chromium-review.googlesource.com/981675
Reviewed-by: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: angle-chromium-autoroll <angle-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#545968}
[modify] https://crrev.com/5c849d31db87f160aed138c694ea614bf6d5f1d9/DEPS


### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-01)

Thanks for the report! The VRP panel decided to award $500 for this report. A member of our finance team will be in touch to arrange for payment.

### aw...@google.com (2018-04-01)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-07-03)

This issue was migrated from crbug.com/chromium/825503?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090901)*
