# Security: Internal Compiler Error(OpTypeFunction may not take more than 255 arguments. OpTypeFunction <id> '267[%267]' has 256 arguments) in tint::spirv::writer::IRFuzzer

| Field | Value |
|-------|-------|
| **Issue ID** | [354748060](https://issues.chromium.org/issues/354748060) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Android |
| **Reporter** | de...@gmail.com |
| **Assignee** | jr...@google.com |
| **Created** | 2024-07-23 |
| **Bounty** | $10,000.00 |

## Description

## REPRODUCE

1. gn gen out/libfuzzer --args="use\_libfuzzer=true tint\_build\_cmds=true"
2. ninja -C out/libfuzzer tint\_wgsl\_fuzzer
3. out/libfuzzer/tint\_wgsl\_fuzzer --filter="writer" poc.wgsl

## CRASH LOG

For the full content, refer to log.txt. This is just a summary.

```
spirv:1:1 error: OpTypeFunction may not take more than 255 arguments. OpTypeFunction <id> '267[%267]' has 256 arguments.
  %267 = OpTypeFunction %void %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function__arr_int_uint_3 %_arr_uint_uint_1 %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int %_ptr_Function_int

```
## Note

The vulnerability is currently affecting the new SPIR-V writer being used for Android. Please refer to my previous report.(<https://issues.chromium.org/u/4/issues/342840932>)

The final comment `// for #1307 loads with ivec2 coords`. is just to keep the fuzzer happy; otherwise, it won't generate the option parameters.

If we don't use --filter="writer", it might cause crashes in other fuzzers. Of course, that is also a problem, but I believe the one here is more serious.

## CRASH INFO AND CREDIT

Type of crash: gpu

Reporter credit: gelatin dessert

## Attachments

- [log.txt](attachments/log.txt) (text/plain, 97.1 KB)
- [poc.wgsl](attachments/poc.wgsl) (application/octet-stream, 13.3 KB)

## Timeline

### de...@gmail.com (2024-07-23)

Hi [jrprice@google.com](mailto:jrprice@google.com),

I believe you are the owner of this issue. Could you help take a look at it?

Thanks!

### ma...@chromium.org (2024-07-23)

[security shepherd]: Confirmed that this reproduced with <https://crrev.com/2a56a339733110a480e660017808926d5a930c7d> on Linux and macOS.

From bisecting, this failure first appeared with <https://crrev.com/5e6de05721b6e1feef8f893fae445b3f5c80a959>. This was a Dawn roll. I see a number of validation commits mentioned in the roll so it's possible this introduced the validation that detects the problem, rather than being the source of the regression.

My understanding is that the SPIR-V writer is generating invalid SPIR-V. Based on <https://crbug.com/342840932#comment7> and <https://crbug.com/342840932#comment14>, this is a potential security issue as the SPIR-V code is handed off to a graphics driver that is likely not hardened against invalid inputs.

Setting as S1 on this basis. Assigning to jrprice@ based on his involvement in <https://crbug.com/342840932>.

### pe...@google.com (2024-07-24)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-24)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### jr...@google.com (2024-07-24)

Thanks for the report. Confirmed that we produce invalid SPIR-V and that this is reproducible in a production Chrome flow, and that it is potentially security impacting on Android due to invalid SPIR-V being passed to the graphics driver.

I've put a fix up for review here:
<https://dawn-review.googlesource.com/c/dawn/+/200014>

### ap...@google.com (2024-07-24)

Project: dawn
Branch: main

commit 3f657b9e679dc3a9f35f4a9f880f5da02ae86478
Author: James Price <jrprice@google.com>
Date:   Wed Jul 24 19:11:19 2024

    [spirv] Fail for functions with >255 parameters
    
    Some IR transforms add new parameters to existing functions, which can
    cause a valid input shader to exceed SPIR-V limit of 255
    parameters. We can't easily fix this, so just fail gracefully and
    class it as a spurious failure as per the WGSL spec.
    
    Fixed: 354748060
    Change-Id: I31b1d1eddc2b75e237e3f01f967f4bb3e3488cee
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200014
    Reviewed-by: David Neto <dneto@google.com>
    Auto-Submit: James Price <jrprice@google.com>
    Commit-Queue: David Neto <dneto@google.com>

M       src/tint/lang/spirv/writer/printer/printer.cc
M       src/tint/lang/spirv/writer/writer_test.cc

https://dawn-review.googlesource.com/200014


### pe...@google.com (2024-07-25)

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

### am...@chromium.org (2024-07-26)

merges approved for <https://dawn-review.googlesource.com/c/dawn/+/200014> -- please merge to:
M126 / branch 6478 (extended stable)
M127 / branch 6533 (stable)
M128 / branch 6613 (beta) at soonest so these fixes can be included in the next respective updates

### ap...@google.com (2024-07-27)

Project: dawn
Branch: chromium/6613

commit 9e12a15979615111af43befcd441762d23060001
Author: James Price <jrprice@google.com>
Date:   Sat Jul 27 00:59:03 2024

    [spirv] Fail for functions with >255 parameters
    
    Some IR transforms add new parameters to existing functions, which can
    cause a valid input shader to exceed SPIR-V limit of 255
    parameters. We can't easily fix this, so just fail gracefully and
    class it as a spurious failure as per the WGSL spec.
    
    Fixed: 354748060
    Change-Id: I31b1d1eddc2b75e237e3f01f967f4bb3e3488cee
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200014
    Reviewed-by: David Neto <dneto@google.com>
    Auto-Submit: James Price <jrprice@google.com>
    Commit-Queue: David Neto <dneto@google.com>
    (cherry picked from commit 3f657b9e679dc3a9f35f4a9f880f5da02ae86478)
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200237
    Reviewed-by: Ken Russell <kbr@google.com>

M       src/tint/lang/spirv/writer/printer/printer.cc
M       src/tint/lang/spirv/writer/writer_test.cc

https://dawn-review.googlesource.com/200237


### ap...@google.com (2024-07-27)

Project: dawn
Branch: chromium/6478

commit d7bb3b5c98653ca95aa46b137dbc7f14999a76ba
Author: James Price <jrprice@google.com>
Date:   Sat Jul 27 00:58:30 2024

    [spirv] Fail for functions with >255 parameters
    
    Some IR transforms add new parameters to existing functions, which can
    cause a valid input shader to exceed SPIR-V limit of 255
    parameters. We can't easily fix this, so just fail gracefully and
    class it as a spurious failure as per the WGSL spec.
    
    Fixed: 354748060
    Change-Id: I31b1d1eddc2b75e237e3f01f967f4bb3e3488cee
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200014
    Reviewed-by: David Neto <dneto@google.com>
    Auto-Submit: James Price <jrprice@google.com>
    Commit-Queue: David Neto <dneto@google.com>
    (cherry picked from commit 3f657b9e679dc3a9f35f4a9f880f5da02ae86478)
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200274
    Reviewed-by: Ken Russell <kbr@google.com>

M       src/tint/lang/spirv/writer/printer/printer.cc
M       src/tint/lang/spirv/writer/writer_test.cc

https://dawn-review.googlesource.com/200274


### ap...@google.com (2024-07-27)

Project: dawn
Branch: chromium/6613

commit 9e12a15979615111af43befcd441762d23060001
Author: James Price <jrprice@google.com>
Date:   Sat Jul 27 00:59:03 2024

    [spirv] Fail for functions with >255 parameters
    
    Some IR transforms add new parameters to existing functions, which can
    cause a valid input shader to exceed SPIR-V limit of 255
    parameters. We can't easily fix this, so just fail gracefully and
    class it as a spurious failure as per the WGSL spec.
    
    Fixed: 354748060
    Change-Id: I31b1d1eddc2b75e237e3f01f967f4bb3e3488cee
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200014
    Reviewed-by: David Neto <dneto@google.com>
    Auto-Submit: James Price <jrprice@google.com>
    Commit-Queue: David Neto <dneto@google.com>
    (cherry picked from commit 3f657b9e679dc3a9f35f4a9f880f5da02ae86478)
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200237
    Reviewed-by: Ken Russell <kbr@google.com>

M       src/tint/lang/spirv/writer/printer/printer.cc
M       src/tint/lang/spirv/writer/writer_test.cc

https://dawn-review.googlesource.com/200237


### ap...@google.com (2024-07-27)

Project: dawn
Branch: chromium/6533

commit c18555c6b616b07fde3e679e6955a4a72870ae1c
Author: James Price <jrprice@google.com>
Date:   Sat Jul 27 02:52:23 2024

    [spirv] Fail for functions with >255 parameters
    
    Some IR transforms add new parameters to existing functions, which can
    cause a valid input shader to exceed SPIR-V limit of 255
    parameters. We can't easily fix this, so just fail gracefully and
    class it as a spurious failure as per the WGSL spec.
    
    Fixed: 354748060
    Change-Id: I31b1d1eddc2b75e237e3f01f967f4bb3e3488cee
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200014
    Reviewed-by: David Neto <dneto@google.com>
    Auto-Submit: James Price <jrprice@google.com>
    Commit-Queue: David Neto <dneto@google.com>
    (cherry picked from commit 3f657b9e679dc3a9f35f4a9f880f5da02ae86478)
    Reviewed-on: https://dawn-review.googlesource.com/c/dawn/+/200275
    Reviewed-by: Ken Russell <kbr@google.com>

M       src/tint/lang/spirv/writer/printer/printer.cc
M       src/tint/lang/spirv/writer/writer_test.cc

https://dawn-review.googlesource.com/200275


### jr...@google.com (2024-07-29)

All merges have landed, please let me know if there's anything else that needs to be done here.

### sp...@google.com (2024-08-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
baseline report of potential memory corruption in a highly privileged process (GPU) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-16)

Congratulations gelatin! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-10-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/354748060)*
