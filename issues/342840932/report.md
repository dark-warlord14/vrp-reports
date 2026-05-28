# Security: Internal Compiler Error(Duplicate non-aggregate type declarations are not allowed) in tint::spirv::writer::IRFuzzer

| Field | Value |
|-------|-------|
| **Issue ID** | [342840932](https://issues.chromium.org/issues/342840932) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Android |
| **Reporter** | de...@gmail.com |
| **Assignee** | jr...@google.com |
| **Created** | 2024-05-26 |
| **Bounty** | $5,000.00 |

## Description

## REPRODUCE

1. gn gen out/libfuzzer --args="use\_libfuzzer=true tint\_build\_cmds=true"
2. ninja -C out/libfuzzer tint\_wgsl\_fuzzer
3. out/libfuzzer/tint\_wgsl\_fuzzer poc.wgsl

## CRASH LOG

For the full content, refer to log.txt. This is just a summary.

```
spirv:1:1 error: Duplicate non-aggregate type declarations are not allowed. Opcode: TypeImage id: 26
  %26 = OpTypeImage %uint 1D 0 0 0 2 R32ui

```
## Note

From this issue, it can be seen that this is the new SPIR-V writer currently being used for Android: <https://issues.chromium.org/issues/340992052#comment15>

## CRASH INFO AND CREDIT

Type of crash: gpu

Reporter credit: gelatin dessert

## Attachments

- [log.txt](attachments/log.txt) (text/plain, 70.4 KB)
- [poc.wgsl](attachments/poc.wgsl) (application/octet-stream, 8.3 KB)

## Timeline

### mp...@google.com (2024-05-28)

jrprice@ can you check if this one has security implications? If not I can remove view restrictions.

### bc...@chromium.org (2024-05-29)

Reduced to:

```
@group(0) @binding(0) var image_dup_src: texture_storage_1d<r32uint,read>;
@group(0) @binding(1) var image_dst: texture_storage_1d<r32uint,write>;

// for #1307 loads with ivec2 coords.

```

Note: the comment is important, as this seeds the side-band fuzzer data.

This looks like the SPIR-V writer is not handling the `readonly_and_readwrite_storage_textures` feature correctly.   

I think it's highly unlikely that this is security impacting, but I'll let jrprice decide.

### bc...@google.com (2024-05-29)

Fix up for review: <https://dawn-review.googlesource.com/c/dawn/+/190621>

### ap...@google.com (2024-05-29)

Project: dawn
Branch: main

commit c509bb3757c02beecfd6d74ef7aae9ee94b1e3ed
Author: Ben Clayton <bclayton@google.com>
Date:   Wed May 29 13:53:19 2024

    [tint][ir][spirv] Deduplicate storage textures with different accesses
    
    `readonly_and_readwrite_storage_textures` adds support for storage texture with read and write access controls. SPIR-V does not consider these different types, and need deduplicating.
    
    Fixed: 342840932
    Change-Id: I3ecb0b7ac4dabe414eece04343d1089ffb9af570
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/190621
    Commit-Queue: dan sinclair <dsinclair@chromium.org>
    Reviewed-by: David Neto <dneto@google.com>
    Auto-Submit: Ben Clayton <bclayton@google.com>
    Reviewed-by: dan sinclair <dsinclair@chromium.org>

M       src/tint/lang/spirv/writer/printer/printer.cc
M       src/tint/lang/spirv/writer/type_test.cc
A       test/tint/bug/chromium/342840932.wgsl
A       test/tint/bug/chromium/342840932.wgsl.expected.dxc.hlsl
A       test/tint/bug/chromium/342840932.wgsl.expected.fxc.hlsl
A       test/tint/bug/chromium/342840932.wgsl.expected.glsl
A       test/tint/bug/chromium/342840932.wgsl.expected.msl
A       test/tint/bug/chromium/342840932.wgsl.expected.spvasm
A       test/tint/bug/chromium/342840932.wgsl.expected.wgsl

https://dawn-review.googlesource.com/190621


### pe...@google.com (2024-05-29)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

### jr...@google.com (2024-05-29)

> can you check if this one has security implications?

After discussion in our team, we believe there is the potential that passing invalid SPIR-V to a Vulkan driver could cause unknown issues that may include security-impacting effects. We are not aware of any specific exploit that can be triggered for this particular case, but cannot decisively rule out such exploits at this time. This particular bug is limited to Android devices.

mpdenton@ please LMK if you any need more information to assess the severity. I can take care of merging the bug fix back to whichever branches will require it based on the perceived severity.

### mp...@google.com (2024-05-30)

Thanks for the analysis! I'll mark this as S1, but as an aside could you elaborate what you think the "unknown issues that may include security-impacting effects" might be?

### pe...@google.com (2024-05-31)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-31)

This is sufficiently serious that it should be merged to extended stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M124. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125, 126].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-05-31)

The OS field is missing from this merge request, please populate OS field to ensure merge request is reviewed by the correct release manager.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pg...@google.com (2024-06-04)

There are no more scheduled releases for M124/M125 - removing label

### jr...@google.com (2024-06-04)

1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://dawn-review.googlesource.com/c/dawn/+/190621>

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes.

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

No.

### jr...@google.com (2024-06-04)

mpdenton@:

> as an aside could you elaborate what you think the "unknown issues that may include security-impacting effects" might be?

The GPU driver that we are handing this invalid SPIR-V too is an opaque blob, some of which is in user mode and some in kernel mode. Although this particular example is pretty benign and I wouldn't imagine there is any real security issue here, it's hard to know for sure exactly what assumptions might be violated in the driver, leading to bad internal state and subsequent issues. I don't have a specific, exploitable side effect in mind though.

### mp...@google.com (2024-06-04)

Thanks, so in the GPU process the process goes WGSL -> SPIR-V -> usermode gpu driver -> kernel mode gpu driver? And normally, we expect the WGSL -> SPIR-V conversion to produce a sufficiently constrained and "valid" SPIR-V output such that GPU drivers, which are normally relatively soft targets, should be somewhat protected from untrusted inputs?

### jr...@google.com (2024-06-04)

> we expect the WGSL -> SPIR-V conversion to produce a sufficiently constrained and "valid" SPIR-V output such that GPU drivers, which are normally relatively soft targets, should be somewhat protected from untrusted inputs?

Correct. Vulkan, the API that the GPU drivers implement, does minimal (if any) validation, so it's on us to make sure we only use it in valid ways.

### pg...@google.com (2024-06-05)

Merge approved for M126! Please cherry pick the fix to branch 6478 by Thursday June 13th EOD MTV time to get this fix into the next stable respin

### sp...@google.com (2024-06-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
$5,000 for report of potential, but not demonstrated, memory corruption in the GPU process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-05)

Congratulations, gelatin! While we were able to make a potentially security relevant change to mitigate potential exploitation of this issue in the GPU process, there was no security impact demonstrated by or able to be gleaned from the information in your report; therefore, we are extended a reduced reward for this report. Thank you again for your efforts!

### ap...@google.com (2024-06-05)

Project: dawn
Branch: chromium/6478

commit e690a3e85f063749eb14628cf977afc31075c76a
Author: Ben Clayton <bclayton@google.com>
Date:   Wed Jun 05 20:16:59 2024

    [tint][ir][spirv] Deduplicate storage textures with different accesses
    
    `readonly_and_readwrite_storage_textures` adds support for storage texture with read and write access controls. SPIR-V does not consider these different types, and need deduplicating.
    
    Fixed: 342840932
    Change-Id: I3ecb0b7ac4dabe414eece04343d1089ffb9af570
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/190621
    Commit-Queue: dan sinclair <dsinclair@chromium.org>
    Reviewed-by: David Neto <dneto@google.com>
    Auto-Submit: Ben Clayton <bclayton@google.com>
    Reviewed-by: dan sinclair <dsinclair@chromium.org>
    (cherry picked from commit c509bb3757c02beecfd6d74ef7aae9ee94b1e3ed)
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/191841
    Auto-Submit: James Price <jrprice@google.com>

M       src/tint/lang/spirv/writer/printer/printer.cc
M       src/tint/lang/spirv/writer/type_test.cc
A       test/tint/bug/chromium/342840932.wgsl
A       test/tint/bug/chromium/342840932.wgsl.expected.dxc.hlsl
A       test/tint/bug/chromium/342840932.wgsl.expected.fxc.hlsl
A       test/tint/bug/chromium/342840932.wgsl.expected.glsl
A       test/tint/bug/chromium/342840932.wgsl.expected.msl
A       test/tint/bug/chromium/342840932.wgsl.expected.spvasm
A       test/tint/bug/chromium/342840932.wgsl.expected.wgsl

https://dawn-review.googlesource.com/191841


### pe...@google.com (2024-09-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/342840932)*
