# Integer Overflow in H265 Slice Header Parsing

| Field | Value |
|-------|-------|
| **Issue ID** | [485212874](https://issues.chromium.org/issues/485212874) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Media |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | Latest |
| **Reporter** | am...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2026-02-17 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Build Chrome libfuzzer with below mentioned args
2. execute the fuzzer with attached malformed H265 file
3. Integer Overflow Crash Detected

# Problem Description

An integer overflow exists in Chromium’s H.265 parser during slice header parsing. A crafted H.265 bitstream can trigger an overflow in arithmetic involving parsed slice parameters, resulting in crash

Vulnerable File Area:

```
media/parsers/h265_parser.cc
Function: media::H265Parser::ParseSliceHeader
Line: 1284

```

Build Args:

```
gn gen out/Media --args='
is_asan=true
is_debug=false
is_ubsan_security=true
is_component_build=false
proprietary_codecs=true
ffmpeg_branding="Chrome"
symbol_level=1
use_remoteexec=false
use_libfuzzer=true
angle_enable_metal=false
'

autoninja -C out/Media media_h265_parser_fuzzer

```

Execution Args:

```
./media_h265_parser_fuzzer delta_poc_overflow.h265

```

A poc file with Crafted slice header values cause overflow during parsing is attached below

# Summary

Integer Overflow in H265 Slice Header Parsing

# Custom Questions

#### Crash state:

```
INFO: Running with entropic power schedule (0xFF, 100).
INFO: Seed: 4195144660
INFO: Loaded 1 modules   (2164628 inline 8-bit counters): 2164628 [0x5ba0205e9ac0, 0x5ba0207fa254), 
INFO: Loaded 1 PC tables (2164628 PCs): 2164628 [0x5ba0207fa258,0x5ba022901b98), 
./media_h265_parser_fuzzer: Running 1 inputs 1 time(s) each.
Running: /home/basha/Downloads/win_repro/delta_poc_overflow.h265
../../media/parsers/h265_parser.cc:1284:51: runtime error: signed integer overflow: 268435456 + 1879048192 cannot be represented in type 'int'
    #0 0x5ba01760b60a in media::H265Parser::ParseSliceHeader(media::H265NALU const&, media::H265SliceHeader*, media::H265SliceHeader*) media/parsers/h265_parser.cc:1284:51
    #1 0x5ba0133ac89d in LLVMFuzzerTestOneInput media/parsers/h265_parser_fuzzertest.cc:61:22
    #2 0x5ba0133f027c in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) third_party/libFuzzer/src/FuzzerLoop.cpp:619:13
    #3 0x5ba0133c12b1 in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*, unsigned long) third_party/libFuzzer/src/FuzzerDriver.cpp:328:6
    #4 0x5ba0133c9da0 in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) third_party/libFuzzer/src/FuzzerDriver.cpp:863:9
    #5 0x5ba0133acfdd in main third_party/libFuzzer/src/FuzzerMain.cpp:20:10
    #6 0x7c06d182a1c9 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #7 0x7c06d182a28a in __libc_start_main csu/../csu/libc-start.c:360:3
    #8 0x5ba0132cfb29 in _start (/home/basha/Desktop/chromefuzz/chromium/src/out/UBSanMedia/media_h265_parser_fuzzer+0x7c11b29) (BuildId: 851ee95e8c3708a1)

SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior ../../media/parsers/h265_parser.cc:1284:51 
Executed /home/basha/Downloads/win_repro/delta_poc_overflow.h265 in 184 ms
***
*** NOTE: fuzzing was not performed, you have only
***       executed the target code on a fixed set of inputs.
***


```
#### Reporter credit:

Ameen Basha M K & Mohammed Yasar B

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [delta_poc_overflow.h265](attachments/delta_poc_overflow.h265) (application/octet-stream, 152 B)

## Timeline

### am...@gmail.com (2026-02-17)

Tested on updated chrome (main branch) in linux & mac environment

Hash: 5c2a8c9375a5030995ba8efffe0a9fd380743038


### am...@gmail.com (2026-02-18)

Team, why the issue was moved to Bug Category from Vulnerability, Kindly share details on this

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


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485212874)*
