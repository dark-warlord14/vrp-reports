# Missing range validation on slice_qp_delta

| Field | Value |
|-------|-------|
| **Issue ID** | [484665123](https://issues.chromium.org/issues/484665123) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Media |
| **Platforms** | Linux, ChromeOS |
| **CVE IDs** | CVE-2022-21813, CVE-2022-21814 |
| **Reporter** | lu...@icloud.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2026-02-15 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

Missing range validation on slice\_qp\_delta

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/+/main/media/parsers/h264_parser.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

At `h264_parser.cc:1485`, `slice_qp_delta` is read via `READ_SE_OR_RETURN` with no range check. The H.264 spec (ITU-T H.264 §7.4.3) requires `SliceQPY = 26 + pic_init_qp_minus26 + slice_qp_delta` to be in `[0, 51 + 6*bit_depth_luma_minus8]`. The sibling fields `slice_alpha_c0_offset_div2` and `slice_beta_offset_div2` ARE validated 14 lines later at lines 1499 and 1502:

```
// Line 1485: not validated:
READ_SE_OR_RETURN(&shdr->slice_qp_delta);
// Missing: range check on SliceQPY

// Lines 1499/1502: validated:
READ_SE_OR_RETURN(&shdr->slice_alpha_c0_offset_div2);
IN_RANGE_OR_RETURN(shdr->slice_alpha_c0_offset_div2, -6, 6);
READ_SE_OR_RETURN(&shdr->slice_beta_offset_div2);
IN_RANGE_OR_RETURN(shdr->slice_beta_offset_div2, -6, 6);

```

`READ_SE_OR_RETURN` accepts exp-Golomb coded values up to approximately ±2³⁰. The unvalidated `int` value flows from the parser through `H264Decoder` to the VA-API delegate at `h264_vaapi_video_decoder_delegate.cc:504`, where `SHDRToSP(slice_qp_delta)` assigns it to `VASliceParameterBufferH264.slice_qp_delta` (int8\_t), causing int→int8\_t narrowing. For example:

- `slice_qp_delta=500` → int8\_t truncation → `-12`
- `slice_qp_delta=100` → survives truncation as `100`, producing `SliceQPY=126` — an OOB index into the 52-entry QP table
- `slice_qp_delta=128` → int8\_t truncation → `-128` (sign flip)

This is the same bug class as [Issue 482862710](https://issues.chromium.org/issues/482862710) (`second_chroma_qp_index_offset`, P1/S1), and was not addressed by the follow-up CLs:

- CL 7572949: fixed `second_chroma_qp_index_offset`
- CL 7574217: fixed `pic_parameter_set_id`, `idr_pic_id`, `changing_slice_group_idc`
- CL 7577373: fixed H.265 parser fields

None of these CLs addressed `slice_qp_delta`.

**Platform scope:** VA-API only (Linux x86, ChromeOS x86). D3D11 passes raw bitstream to the DXVA decoder and does not extract `slice_qp_delta` into separate struct fields. Confirmed via grep of `media/gpu/windows/` showing zero matches for `slice_qp_delta`. V4L2 similarly does not extract it into V4L2 control structs, also confirmed via grep of `media/gpu/v4l2/` showing zero matches. The parser-level spec violation affects all platforms, but only VA-API has the int→int8\_t narrowing as a concrete exploitation vector.

**Fix:** Add range validation matching the spec constraint on SliceQPY. A conservative static bound:

```
IN_RANGE_OR_RETURN(shdr->slice_qp_delta, -51, 51);

```

Or the precise spec-derived bound:

```
int slice_qp_y = 26 + pps->pic_init_qp_minus26 + shdr->slice_qp_delta;
TRUE_OR_RETURN(slice_qp_y >= 0 && slice_qp_y <= 51 + 6 * sps->bit_depth_luma_minus8);

```

**Reproduction:** I have a standalone C++ PoC (28-byte Annex-B bitstream with `slice_qp_delta=500`) and a Chromium-style unit test with some test cases that demonstrate:

1. Parser accepts extreme values (500, -500, 1000, -1000) — `kOk`
2. int→int8\_t truncation: 500 → -12
3. Values just outside spec range (26, -27) accepted
4. int8\_t sign flip: 128 → -128

#### Impact analysis

Same trust boundary analysis as [Issue 482862710](https://issues.chromium.org/issues/482862710). The unvalidated `slice_qp_delta` reaches kernel GPU drivers via the VA-API path when a user visits a page containing a malicious `<video>` element. The GPU sandbox does not mitigate this as the GPU process is designed to make VA-API calls, so malformed parameters reach the kernel through the sandbox's allowed syscall surface.

The out-of-range `SliceQPY` value is used by drivers for QP-dependent operations (quantization parameter lookup, deblocking filter strength). With `slice_qp_delta=100` (survives int8\_t truncation intact), `SliceQPY = 26 + 0 + 100 = 126`, overshooting the 52-entry QP table by 74 entries. If the driver uses this for array indexing without clamping, this is a kernel OOB read.

CVE-2022-21813 and CVE-2022-21814 (NVIDIA) were this exact bug class. The parser must enforce spec compliance regardless of individual driver behavior.

---

### The cause

#### What version of Chrome have you found the security issue in?

Current main branch

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Luke Francis

## Attachments

- [slice_qp_delta_test.cc](attachments/slice_qp_delta_test.cc) (application/octet-stream, 5.9 KB)
- [slice_qp_delta_poc.cc](attachments/slice_qp_delta_poc.cc) (application/octet-stream, 6.4 KB)

## Timeline

### ma...@google.com (2026-02-17)

Security shepherd: Adding some folks from 482862710. eugene@, PTAL?

### ch...@google.com (2026-02-17)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-17)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2026-02-18)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7586715>

media: Validate slice\_qp\_delta and slice\_qs\_delta in H264Parser

---


Expand for full commit details
```
     
    This CL adds range validation for slice_qp_delta and slice_qs_delta 
    during slice header parsing to ensure compliance with the H.264 spec. 
     
    According to Section 7.4.3 "Slice header semantics": 
     
       For `slice_qp_delta`: 
       "The variable SliceQPY is derived as 
       SliceQPY = 26 + pic_init_qp_minus26 + slice_qp_delta 
       The value of SliceQPY shall be in the range of -QpBdOffset_Y to 51, inclusive." 
       where QpBdOffset_Y = 6 * bit_depth_luma_minus8. 
     
       For `slice_qs_delta`: 
       "The variable SliceQSY is derived as 
       SliceQSY = 26 + pic_init_qs_minus26 + slice_qs_delta 
       The value of SliceQSY shall be in the range of 0 to 51, inclusive." 
     
    Adding these checks ensures that malformed or malicious streams are 
    rejected early in the parsing stage, preventing out-of-range values 
    from reaching accelerated decoders. 
     
    Bug: 484665123 
    Change-Id: I68e789b477ce24ac97be7c2b5701ebdcc3e229bc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7586715 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1586159}

```

---

Files:

- M `media/parsers/h264_parser.cc`

---

Hash: [77af3dfce928a72a2836e1232cb7ba62054e3027](https://chromiumdash.appspot.com/commit/77af3dfce928a72a2836e1232cb7ba62054e3027)  

Date: Wed Feb 18 03:05:24 2026


---

### da...@chromium.org (2026-02-23)

~~FWIW it looks like we already had a fuzzer bug open for this at [issue 469979147](https://issues.chromium.org/issues/469979147) -- I just hadn't got around to fixing it yet.~~

Edit: Actually I think fixing this issue just kept the fuzzer from reaching the failing spot in [issue 469979147](https://issues.chromium.org/issues/469979147). This report is also high quality and more clearly actionable than the fuzzer report.

### ma...@google.com (2026-02-23)

[Security shepherd] Do we know if there are GPU drivers vulnerable to this? Or is it a reasonably likely that there are? If so, I think this would probably warrant at least S1/High (and a merge).

### da...@chromium.org (2026-02-23)

We don't have any evidence there are vulnerable drivers. I don't think it's reasonably likely, but there's almost no data to support such a conclusion one way or the other.

### wf...@chromium.org (2026-02-24)

[vrp panel] curious if anyone could answer how this did not get prevented by the container range validation? is it because it's third party code?

### eu...@chromium.org (2026-02-24)

Container parsers never go so deep into codec bitstream details.
No, this isn't 3rd party code.

### lu...@icloud.com (2026-04-23)

Hey, this has been at reward-topanel for ~2 months, any update on when the panel might review? Thank you.

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
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484665123)*
