# Heap buffer overflow (read) in skcms curve table lookup via crafted ICC profile

| Field | Value |
|-------|-------|
| **Issue ID** | [492744328](https://issues.chromium.org/issues/492744328) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | kj...@chromium.org |
| **Created** | 2026-03-14 |
| **Bounty** | $3,000.00 |

## Description

## Summary

A heap-buffer-overflow (read of size 2) occurs in skcms's TRC curve table
evaluation when processing an ICC profile with a `curv` tag whose
`table_entries` value triggers IEEE 754 float32 precision loss in the index
computation. This is reachable from web content by embedding the crafted ICC
profile in a WebP image's ICCP chunk and loading it via an `<img>` tag.

## Affected component

`third_party/skia/modules/skcms` — the skcms color management library used by
Chrome's image decoding pipeline.

## Root cause

In `modules/skcms/src/Transform_inl.h` line 619 (SIMD path) and
`modules/skcms/skcms.cc` line 307 (scalar path), the curve table index is
computed as:

```
F ix = max_(F0, min_(v, F1)) * (float)(curve->table_entries - 1);
I32 lo = cast<I32>(ix);

```

`table_entries - 1` is a `uint32_t`. When its value exceeds 2^24 (16,777,216),
the cast to `float` (IEEE 754 single-precision, 24-bit significand) can round
**up**. Specifically, for `table_entries = 16,777,220`:

- `table_entries - 1 = 16,777,219`
- `(float)16,777,219 = 16,777,220.0f` (round-to-even rounds UP)
- With input `v = 1.0f`: `lo = 16,777,220`
- Valid index range: `[0, 16,777,219]`
- **`lo` is 1 past the valid end of the table**

This causes `gather_16()` (`Transform_inl.h:458`) to read 2 bytes past the
end of the curve table data, which is the end of the ICC profile heap
allocation.

## Steps to reproduce

### Method 1: Chromium (confirms web-reachable attack surface)

1. Generate the PoC: `python3 gen_webp_skcms_oob.py`
2. Launch ASAN Chromium:
   ```
   path/to/chrome --no-sandbox file:///path/to/poc.html
   
   ```
3. ASAN reports `heap-buffer-overflow` (READ of size 2) in the renderer process.

### Method 2: Standalone skcms test (fully symbolized trace)

Build against Skia source:

```
c++ -std=c++17 -fsanitize=address -g \
    -I modules/skcms -I modules/skcms/src -DSKCMS_PORTABLE \
    poc/test_skcms_oob.c modules/skcms/skcms.cc \
    modules/skcms/src/skcms_TransformBaseline.cc \
    -lm -o test_skcms_oob
./test_skcms_oob

```
## ASAN output (symbolized, standalone build)

```
==333367==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7bb63c3fe95c
READ of size 2 at 0x7bb63c3fe95c thread T0
    #0 load<short unsigned int, unsigned char> modules/skcms/src/Transform_inl.h:100
    #1 operator() modules/skcms/src/Transform_inl.h:455
    #2 gather_16 modules/skcms/src/Transform_inl.h:458
    #3 table modules/skcms/src/Transform_inl.h:635
    #4 Exec_table_r_k modules/skcms/src/Transform_inl.h:1276
    #5 Exec_table_r modules/skcms/src/Transform_inl.h:1276
    #6 exec_stages modules/skcms/src/Transform_inl.h:1545
    #7 skcms_private::baseline::run_program modules/skcms/src/Transform_inl.h:1593
    #8 skcms_Transform modules/skcms/skcms.cc:3057
    #9 main poc/test_skcms_oob.c:194

0x7bb63c3fe95c is located 0 bytes after 33554780-byte region [...]

```
## ASAN output (Chromium renderer, unsymbolized)

```
==332007==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7b300489395c
READ of size 2 at 0x7b300489395c thread T0 (chrome)
    #0 0x5567111d0f02  (chrome+0x1200bf02)
    [... full trace in chromium_asan_trace.txt ...]

0x7b300489395c is located 0 bytes after 33554780-byte region
[0x7b3002893800,0x7b300489395c)

Command line: .../chrome --type=renderer [...]

```
## Attack vector

1. Attacker crafts an ICC profile with a `curv` TRC tag containing
   `table_entries = 16,777,220` (requiring ~32 MB of curve data).
2. The ICC profile is embedded in a WebP image's ICCP chunk (WebP has no
   aggregate size limit on ICCP data, unlike JPEG's ~16.7 MB or PNG/libpng's
   ~8 MB limits).
3. Victim loads an HTML page containing `<img src="malicious.webp">`.
4. Chrome's WebP decoder extracts the ICC profile, `skcms_Parse` accepts it,
   and `skcms_Transform` is called during color conversion, triggering the
   OOB read in the renderer process.

No user interaction beyond page navigation is required.

## Impact

- **Type**: Heap buffer overflow (read), 2 bytes past allocation boundary
- **Process**: Renderer (sandboxed)
- **Trigger**: Web-accessible via `<img>` tag, no user interaction
- **Potential**: Information disclosure from adjacent heap data. The 2 leaked
  bytes are used as a uint16 curve table value, which influences the color of
  rendered pixels — an attacker could potentially extract the leaked value by
  reading back pixel colors via canvas.

## Suggested fix

Cast `table_entries - 1` to `double` before the multiplication, or clamp the
computed index to `table_entries - 1`:

```
// In Transform_inl.h, table():
I32 lo = cast<I32>(ix);
lo = min_(lo, (int)(curve->table_entries - 1));  // clamp

// In skcms.cc, eval_curve():
int lo = (int) ix;
if (lo >= (int)curve->table_entries) lo = curve->table_entries - 1;

```
## Files in this directory

- `skcms_oob.webp` — PoC WebP image (32 MB, crafted ICC profile)
- `poc.html` — HTML page that loads the WebP via `<img>` (open as file:// URL)
- `gen_webp_skcms_oob.py` — Python script to regenerate the WebP PoC
- `test_skcms_oob.c` — Standalone skcms test (symbolized ASAN trace)
- `chromium_asan_trace.txt` — Full Chromium ASAN output
- `standalone_asan_trace.txt` — Full symbolized standalone ASAN output

## Chrome version

Tested on ASAN Chromium build (x64 Linux):

- `is_asan = true`, `is_lsan = true`, `target_cpu = "x64"`
- BuildId: `ab479cbc146d320b`

## Affected versions

All versions of Chrome shipping skcms with table-based TRC curve support
(the vulnerable code has been present since skcms's initial implementation).

## Attachments

- [test_skcms_oob.c](attachments/test_skcms_oob.c) (text/x-csrc, 7.5 KB)
- [standalone_asan_trace.txt](attachments/standalone_asan_trace.txt) (text/plain, 3.6 KB)
- [skcms_oob.webp](attachments/skcms_oob.webp) (image/webp, 32.0 MB)
- [poc.html](attachments/poc.html) (text/html, 221 B)
- [gen_webp_skcms_oob.py](attachments/gen_webp_skcms_oob.py) (text/x-python, 11.4 KB)
- [chromium_asan_trace.txt](attachments/chromium_asan_trace.txt) (text/plain, 10.5 KB)

## Timeline

### ma...@gmail.com (2026-03-14)

## Bisect

The vulnerable code was introduced in the skcms repository on **2018-03-05**:

**SIMD path** (`Transform_inl.h`, the `table()` function):

```
Commit:  8a7ec86c049f7e1345e7418f10f676ce0a849727
Date:    2018-03-05 14:18:41 -0500
Author:  Mike Klein <mtklein@chromium.org>
Message: support 16-bit TRC tables in src profiles

```

This commit added:

```
SI F table_16(const skcms_Curve* curve, F v) {
    F ix = max_(F0, min_(v, F1)) * (float)(curve->table_entries - 1);
    I32 lo = CAST(I32, ix),

```

**Scalar path** (`skcms.cc`, the `eval_curve()` function) was introduced on
**2018-04-06** in commit `8a72781` and moved into `skcms.c` on 2018-07-02
in commit `99b01c0`.

Both paths have had the same `(float)(table_entries - 1)` pattern since
their introduction — the bug has been present for over 8 years.

### ch...@google.com (2026-03-15)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-15)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ma...@gmail.com (2026-03-15)

I wanted to patch that using Gerrit, however I am not sure how to create patch with limited visibility, I was only able to create a public patch.

If you point me to some resource I will gladly do it.

### kj...@chromium.org (2026-03-16)

AFAICT, our Gerrit instance is not set up to handle limited visibility patches. We usually just upload a patch with a link to the bug and minimal explanation of the vulnerability.

### dx...@google.com (2026-03-16)

Project: skcms  

Branch:  main  

Author:  Kaylee Lubick [kjlubick@google.com](mailto:kjlubick@google.com)  

Link:    <https://skia-review.googlesource.com/1187536>

Tighten max table entries when parsing and evaluating ICC curves

---


Expand for full commit details
```
     
    We have some assumptions elsewhere in the code that hinge on this 
    being smaller than 2^24. 
     
    This will make parsing fail if we are given more than ~16 million 
    table entries in the profile and makes sure profiles given to us 
    conform to that limit. 
     
    This limit may impact some fringe WebP images in Chromium; see 
    linked bug for more details. 
     
    Bug: b/492744328 
    Change-Id: I4ca302b490021e2276a55f949f36125dab44196d 
    Reviewed-on: https://skia-review.googlesource.com/c/skcms/+/1187536 
    Reviewed-by: Florin Malita <fmalita@google.com> 
    Auto-Submit: Kaylee Lubick <kjlubick@google.com>

```

---

Files:

- M `skcms.cc`

---

Hash: 0ac639262d12e2aa9183c63203a5428e400f40fe  

Date: Mon Mar 16 16:32:52 2026


---

### kj...@chromium.org (2026-03-16)

Update: I've landed a fix and we are in the process of rolling it into Skia and then Chromium

### kj...@google.com (2026-03-17)

<https://review.skia.org/1187478> is the roll into Skia.

<https://crrev.com/c/7671867> is the roll into Chromium.

This is fixed, but we'll want to backport this to Stable, Beta, and the LTS releases due to the fact this has existed for quite a while.

### ch...@google.com (2026-03-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-17)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-17)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-17)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-17)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### kj...@google.com (2026-03-17)

Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: This is a fix to security vulnerability
- What changes specifically would you like to merge? <https://skia-review.git.corp.google.com/c/skia/+/1187478>
- Have the changes been released and tested on canary? They just made it to Canary yesterday.
- Is this a new feature? No.
- If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? This does not require manual verification.

### dr...@chromium.org (2026-03-18)

No crashes in Canary. Approved to merge to M146 and M147.

### go...@google.com (2026-03-19)

Please merge your change to M147 by 2:00 PM PT today so we can take it in for tomorrow's M147 beta release. Thank you.

### kj...@google.com (2026-03-19)

M146 cherry pick <https://review.skia.org/1190596>

M147 cherry pick <https://review.skia.org/1190576>

### ch...@google.com (2026-03-24)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2026-03-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### kj...@google.com (2026-03-24)

Regarding #20

1. No, this was pre-existing
2. No, this is part of a feature that's been here since 2018 or so

### vi...@google.com (2026-04-03)

Hi. I’m evaluating the necessary changes to eventually cherry-pick this for M138-LTS, but if we follow the same logic used for M146 and M147 then it would involve autorolling 15 revisions of skcms into branch m138 of Skia.

I have two questions, maybe Kaylee could help here:

1. Is the new bazelisk rolled in M146 and M147 cherry-picks (<https://skia-review.git.corp.google.com/c/skcms/+/1187557>?) related to the fix for this bug - is that necessary?
2. If so, I’m considering just cherry-pick the actual skcms fix directly in Skia `chrome/m138` branch: <https://skia-review.git.corp.google.com/c/skia/+/1202678>. Do you think this could be feasible?

Thank you,

### kj...@google.com (2026-04-03)

Yes, I think we only need the skcms.cc change, not any of the other changes. I'd have to make sure it still compiles locally though as we don't have CQ support on that branch.

### dx...@google.com (2026-04-07)

Project: skia  

Branch:  chrome/m138  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://skia-review.googlesource.com/1202678>

[M138-LTS] Tighten max table entries when parsing and evaluating ICC curves

---


Expand for full commit details
```
     
    We have some assumptions elsewhere in the code that hinge on this 
    being smaller than 2^24. 
     
    This will make parsing fail if we are given more than ~16 million 
    table entries in the profile and makes sure profiles given to us 
    conform to that limit. 
     
    This limit may impact some fringe WebP images in Chromium; see 
    linked bug for more details. 
     
    Bug: b/492744328 
    Change-Id: If3c07e4fe62a19fad010ddd3827392ef4340d913 
    Reviewed-on: https://skia-review.googlesource.com/c/skcms/+/1187536 
    Reviewed-by: Florin Malita <fmalita@google.com> 
    Auto-Submit: Kaylee Lubick <kjlubick@google.com> 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1202678 
    Reviewed-by: Kaylee Lubick <kjlubick@google.com>

```

---

Files:

- M `modules/skcms/skcms.cc`

---

Hash: 17265c8a43358f8cb5b43ef6992c3565edcfaa57  

Date: Fri Apr 3 16:58:38 2026


---

### pe...@google.com (2026-05-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-04)

1. <https://skia-review.git.corp.google.com/c/skia/+/1222818>
2. Simple - no conflicts and pretty similar to the M138 merge
3. 138, 146, 147
4. Yes

### dx...@google.com (2026-05-04)

Project: skia  

Branch:  chrome/m144  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://skia-review.googlesource.com/1222818>

[M144-LTS] Tighten max table entries when parsing and evaluating ICC curves

---


Expand for full commit details
```
     
    We have some assumptions elsewhere in the code that hinge on this 
    being smaller than 2^24. 
     
    This will make parsing fail if we are given more than ~16 million 
    table entries in the profile and makes sure profiles given to us 
    conform to that limit. 
     
    This limit may impact some fringe WebP images in Chromium; see 
    linked bug for more details. 
     
    Bug: b/492744328 
    Change-Id: Id68a3e970aaba29b284617120fdff2612f7664fa 
    Reviewed-on: https://skia-review.googlesource.com/c/skcms/+/1187536 
    Reviewed-by: Florin Malita <fmalita@google.com> 
    Auto-Submit: Kaylee Lubick <kjlubick@google.com> 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1202678 
    Reviewed-by: Kaylee Lubick <kjlubick@google.com> 
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/1222818

```

---

Files:

- M `modules/skcms/skcms.cc`

---

Hash: cd0c5f445516ea4e90e02b5f634cbc5ca23b5a44  

Date: Thu Apr 30 19:02:21 2026


---

### sp...@google.com (2026-06-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492744328)*
