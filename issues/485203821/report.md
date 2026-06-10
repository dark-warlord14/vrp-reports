# Signed Integer overflow in H264 SEI Parsing

| Field | Value |
|-------|-------|
| **Issue ID** | [485203821](https://issues.chromium.org/issues/485203821) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Media |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 144.0.0.0 |
| **Reporter** | b....@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2026-02-17 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Build chrome libfuzzer with below mentioned args
2. execute the fuzzer with the attached malformed H264 file
3. Signed Integer overflow crash detected

# Problem Description

A signed integer overflow occurs in chromiums H264 parser while processing SEI. The crash happens when multiplying a large parsed value.

Vulnerable file details

```
media/parsers/h264_parser.cc
Function : media::H264Parser::ParseSEI(media::H264SEI*)
Line : 1549

```

Build Args:

```
gn gen out/ASanMedia --args='
is_asan=true 
is_ubsan_security=true 
is_debug=false 
is_component_build=false 
proprietary_codecs=true 
ffmpeg_branding="Chrome" 
symbol_level=1 
use_remoteexec=false
use_libfuzzer=true 
mac_sdk_min="26" 
angle_enable_metal=false
'

autoninja -C out/ASanMedia media_h264_parser_fuzzer

```

Execution args

```
./media_h264_parser_fuzzer h264_sei_overflow.h264

```

Attached a poc file which contains the crafted sei payload for h264 which results in large parsed value causing the integer overflow

# Summary

Signed Integer overflow in H264 SEI Parsing

# Custom Questions

#### Crash state:

Crash state:

```
INFO: Running with entropic power schedule (0xFF, 100).
INFO: Seed: 4038822869
INFO: Loaded 1 modules   (3274258 inline 8-bit counters): 3274258 [0x104c70000, 0x104f8f612), 
ASanMedia/media_h264_parser_fuzzer: Running 1 inputs 1 time(s) each.
Running: /h264_sei_overflow.h264
../../media/parsers/h264_parser.cc:1549:40: runtime error: signed integer overflow: 268435456 * 8 cannot be represented in type 'int'
    #0 0x0001046f02c4 in media::H264Parser::ParseSEI(media::H264SEI*) media/parsers/h264_parser.cc:1549:40
    #1 0x00010457a01c in LLVMFuzzerTestOneInput media/parsers/h264_parser_fuzzertest.cc:65:22
    #2 0x0001045b8438 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) third_party/libFuzzer/src/FuzzerLoop.cpp:619:13
    #3 0x00010458ca74 in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*, unsigned long) third_party/libFuzzer/src/FuzzerDriver.cpp:329:6
    #4 0x0001045946a0 in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) third_party/libFuzzer/src/FuzzerDriver.cpp:864:9
    #5 0x00010457a81c in main third_party/libFuzzer/src/FuzzerMain.cpp:20:10
    #6 0x00018486dd50 in start (/usr/lib/dyld:arm64e+0x8d50)
*
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior ../../media/parsers/h264_parser.cc:1549:40 
Executed /h264_sei_overflow.h264 in 364 ms
***
*** NOTE: fuzzing was not performed, you have only
***       executed the target code on a fixed set of inputs.

***


```
#### Reporter credit:

Mohammed Yasar B & Ameen Basha M K

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [h264_sei_overflow.h264](attachments/h264_sei_overflow.h264) (application/octet-stream, 1.0 MB)

## Timeline

### an...@chromium.org (2026-02-17)

[security shepherd]: Thanks for the report. Assigning this to @eu...@chromium.org who has worked on H264 before.

### dx...@google.com (2026-02-18)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7586436>

media: Fix integer overflows in H264 and H265 parsers

---


Expand for full commit details
```
     
    This change addresses multiple integer overflow issues in the 
    H.264 and H.265 bitstream parsers. 
     
    The following calculations are now protected or validated: 
      - H.264/H.265 `ParseSEI`: The accumulation of SEI message `type` and 
        `payload_size` is now protected using `base::CheckedNumeric`. 
      - H.265 `ParseSliceHeader`: 
         - The summation of `delta_poc_msb_cycle_lt` values is now protected 
           using `base::CheckedNumeric`. 
         - `slice_qp_delta` validation is refactored to check the delta against 
           derived bounds instead of performing a potentially overflowing addition. 
         - `num_entry_point_offsets` upper bound calculation and the subsequent 
           bit skip calculation are now protected using `base::CheckedNumeric`. 
      - H.265 `ParsePredWeightTable`: 
         - `delta_chroma_log2_weight_denom` is now validated against constant 
           bounds [-7, 7] before addition to prevent signed integer overflow. 
     
    Bug: 485203821, 485115554, 485212874 
    Change-Id: Ifc8da5426b0d9f0e3bbfed30d175e62af46bca22 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7586436 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1586702}

```

---

Files:

- M `media/parsers/h264_parser.cc`
- M `media/parsers/h265_parser.cc`

---

Hash: [7cf2bae3b0688de45d5215e768ca987f2967fc46](https://chromiumdash.appspot.com/commit/7cf2bae3b0688de45d5215e768ca987f2967fc46)  

Date: Wed Feb 18 22:30:58 2026


---

### ch...@google.com (2026-02-18)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-02-19)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485203821)*
