# Heap OOB read in Blink text shaping

| Field | Value |
|-------|-------|
| **Issue ID** | [491080830](https://issues.chromium.org/issues/491080830) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Fonts |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2026-03-09 |
| **Bounty** | $2,000.00 |

## Description

### VULNERABILITY DETAILS

A heap-buffer-overflow read occurs in Blink text shaping when `CaseMappingHarfBuzzBufferFiller::FillSlowCase()` advances UTF-16 with a wrong bound argument.

In `third_party/blink/renderer/platform/fonts/shaping/case_mapping_harfbuzz_buffer_filler.cc:80`, the code calls:

```
U16_FWD_1(buffer.data(), new_char_index, num_characters);

```

inside a loop whose index is absolute (`char_index` starts at `start_index`, not `0`).

When shaping a non-zero subrange (`start_index > 0`) that includes a trailing unpaired lead surrogate, `U16_FWD_1` can read one UTF-16 code unit past the end of the backing buffer.

This vulnerability leads to limited OOB read adjacent to UTF-16 buffer end under attacker-influenced text/range shaping state.

### VERSION

- Chrome Version: `Chromium 147.0.7725.0` (`asan-debug`, dev)
- Operating System: `Ubuntu 24.04.3 LTS (Noble Numbat)`, Linux kernel `6.14.0-37-generic` (x86\_64)

### REPRODUCTION CASE

Attached minimal single-file PoC:

- `crash_20260309_050715_agent21_min.html`

Opening it in Chrome would lead to the crash.

### FOR CRASHES, ADDITIONAL INFORMATION

- Type of crash: Renderer process crash (tab crash)
- Crash state: ASAN heap-buffer-overflow (READ of size 2)
  - Top frame:
    - `blink::CaseMappingHarfBuzzBufferFiller::FillSlowCase(...)`
    - `third_party/blink/renderer/platform/fonts/shaping/case_mapping_harfbuzz_buffer_filler.cc:80:17`
  - Call path includes:
    - `CaseMappingHarfBuzzBufferFiller::CaseMappingHarfBuzzBufferFiller(...)`
    - `HarfBuzzShaper::ShapeSegment(...)`
  - Full symbolized ASAN trace attached:
    - `agent21_min_run6.stderr.log`

### CREDIT INFORMATION

- Reporter credit: `heapracer`

---

## Detailed root cause

### Vulnerable location

- `third_party/blink/renderer/platform/fonts/shaping/case_mapping_harfbuzz_buffer_filler.cc:66-101`
- Faulting statement at `:80`

### Fault pattern

The loop is driven in absolute text coordinates:

```
for (unsigned char_index = start_index;
     char_index < start_index + num_characters;) {
  unsigned new_char_index = char_index;
  U16_FWD_1(buffer.data(), new_char_index, num_characters);
  ...
}

```

`U16_FWD_1` expects a length bound in the same coordinate space as the index. Here, `new_char_index` is absolute but the supplied bound is only `num_characters` (subrange length), not `start_index + num_characters` (subrange end in absolute coordinates).

With `start_index > 0`, this mismatch allows out-of-range access during surrogate-pair probing at range boundaries.

## Attachments

- [agent21_min_run6.stderr.log](attachments/agent21_min_run6.stderr.log) (text/plain, 39.4 KB)
- [crash_20260309_050715_agent21_min.html](attachments/crash_20260309_050715_agent21_min.html) (text/html, 170.7 KB)

## Timeline

### ns...@chromium.org (2026-03-09)

Thank you for your bug report.

Setting P1/S1 as this is a renderer OOB.

ikilpatrick@, please take a look.

Also, this looks like it should hit stable from when the last change happened to the problematic code. Please update found-in if that's not the case.

### ik...@chromium.org (2026-03-09)

I'm not the right engineer for this.

I think this line was originally added in:
<https://chromium.googlesource.com/chromium/src/+/de2db20f1ddb41f0c8de88ab9d376cbf40769a0c>

Assigning to [drott@chromium.org](mailto:drott@chromium.org) but also cc'ing @tk...@chromium.org due to safe buffers.

### ch...@google.com (2026-03-10)

Setting milestone because of s0/s1 severity.

### dr...@chromium.org (2026-03-11)

Thanks for the report, proposed fix in <https://crrev.com/c/7655112>

### dx...@google.com (2026-03-11)

Project: chromium/src  

Branch:  main  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7655112>

Fix U16\_FWD\_1 increment boundary in CaseMappingHarfBuzzBufferFiller

---


Expand for full commit details
```
     
    To work safely, the macro needs the boundary to be greater than the 
    start index at the time of use. If this precondition is not met, an 
    overrun can occur. Fix this by using the correct buffer boundary. 
     
    Fixed: 491080830 
    Change-Id: I707b95ccdc8294f722d627b9255540309b03a572 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7655112 
    Commit-Queue: Rune Lillesveen <futhark@chromium.org> 
    Auto-Submit: Dominik Röttsches <drott@chromium.org> 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1597614}

```

---

Files:

- M `third_party/blink/renderer/platform/fonts/shaping/case_mapping_harfbuzz_buffer_filler.cc`

---

Hash: [a8e675e9a31596b695262732746738e475ccac9a](https://chromiumdash.appspot.com/commit/a8e675e9a31596b695262732746738e475ccac9a)  

Date: Wed Mar 11 10:04:10 2026


---

### ch...@google.com (2026-03-11)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1597614) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to dev (M147) because latest trunk commit (1597614) appears to be after dev branch point (1596535).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-12)

**Merge approved:** your change passed merge requirements and is auto-approved for M147. Please go ahead and merge the CL to branch 7727 (refs/branch-heads/7727) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-12)

Merge review required: M146 is already shipping to stable.

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

### dr...@chromium.org (2026-03-12)

awhalley@, drubery@ please advise on whether you would like to merge this to stable. The fix is minimal and low risk IMO, see <https://chromium-review.git.corp.google.com/c/chromium/src/+/7655112> - one boundary change for the Unicode codepoint-by-codepoint increment macro.

### dr...@chromium.org (2026-03-12)

Yep I see no crashes in Canary and this is an S1, so we should merge it to Stable. Approving for M146.

### dr...@chromium.org (2026-03-13)

M146 merge in <https://chromium-review.git.corp.google.com/c/chromium/src/+/7665800>

### dx...@google.com (2026-03-13)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7660702>

[Merge] Fix U16\_FWD\_1 increment boundary in CaseMappingHarfBuzzBufferFiller

---


Expand for full commit details
```
     
    To work safely, the macro needs the boundary to be greater than the 
    start index at the time of use. If this precondition is not met, an 
    overrun can occur. Fix this by using the correct buffer boundary. 
     
    (cherry picked from commit a8e675e9a31596b695262732746738e475ccac9a) 
     
    Fixed: 491080830 
    Change-Id: I707b95ccdc8294f722d627b9255540309b03a572 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7655112 
    Commit-Queue: Rune Lillesveen <futhark@chromium.org> 
    Auto-Submit: Dominik Röttsches <drott@chromium.org> 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1597614} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7660702 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#234} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `third_party/blink/renderer/platform/fonts/shaping/case_mapping_harfbuzz_buffer_filler.cc`

---

Hash: [5711c908fd0559419bcd0a9b52e8cc7856dcb9d8](https://chromiumdash.appspot.com/commit/5711c908fd0559419bcd0a9b52e8cc7856dcb9d8)  

Date: Fri Mar 13 13:08:40 2026


---

### pe...@google.com (2026-03-13)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-03-13)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7665800>

[Merge] Fix U16\_FWD\_1 increment boundary in CaseMappingHarfBuzzBufferFiller

---


Expand for full commit details
```
     
    To work safely, the macro needs the boundary to be greater than the 
    start index at the time of use. If this precondition is not met, an 
    overrun can occur. Fix this by using the correct buffer boundary. 
     
    (cherry picked from commit a8e675e9a31596b695262732746738e475ccac9a) 
     
    Fixed: 491080830 
    Change-Id: I707b95ccdc8294f722d627b9255540309b03a572 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7655112 
    Commit-Queue: Rune Lillesveen <futhark@chromium.org> 
    Auto-Submit: Dominik Röttsches <drott@chromium.org> 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1597614} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7665800 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2498} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/platform/fonts/shaping/case_mapping_harfbuzz_buffer_filler.cc`

---

Hash: [6eade825700c6a020d3f87c88694d255678e97bc](https://chromiumdash.appspot.com/commit/6eade825700c6a020d3f87c88694d255678e97bc)  

Date: Fri Mar 13 13:13:47 2026


---

### pe...@google.com (2026-03-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-03-18)

1. one CL only: https://chromium-review.git.corp.google.com/c/chromium/src/+/7671497
2. Low - there was no conflict
3. 146 and 147
4. Yes.

### an...@google.com (2026-03-31)

Merge approved for LTS-138

### dx...@google.com (2026-04-02)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7671497>

[M138-LTS] Fix U16\_FWD\_1 increment boundary in CaseMappingHarfBuzzBufferFiller

---


Expand for full commit details
```
     
    To work safely, the macro needs the boundary to be greater than the 
    start index at the time of use. If this precondition is not met, an 
    overrun can occur. Fix this by using the correct buffer boundary. 
     
    Fixed: 491080830 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7655112 
    Commit-Queue: Rune Lillesveen <futhark@chromium.org> 
    Auto-Submit: Dominik Röttsches <drott@chromium.org> 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1597614} 
    (cherry picked from commit a8e675e9a31596b695262732746738e475ccac9a) 
     
    Change-Id: I7d76b3b125f03e0cc7134c30826a6238a998c7e5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7671497 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Reviewed-by: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3517} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/renderer/platform/fonts/shaping/case_mapping_harfbuzz_buffer_filler.cc`

---

Hash: [9ccd6dbe24b2d3fc553aca78c1c4916960062c3e](https://chromiumdash.appspot.com/commit/9ccd6dbe24b2d3fc553aca78c1c4916960062c3e)  

Date: Thu Apr 2 18:01:44 2026


---

### ct...@chromium.org (2026-04-15)

Downgrading to S-2 as this only demonstrates a renderer OOB read, per <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md#:~:text=An%20out%2Dof%2Dbounds%20read%20in%20a%20renderer%20process>

### sp...@google.com (2026-04-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

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

### pe...@google.com (2026-05-07)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-07)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7829178>
2. Low. No conflict
3. 138, 146 and 147
4. Yes.

### dx...@google.com (2026-05-25)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7829178>

[M144-LTS] Fix U16\_FWD\_1 increment boundary in CaseMappingHarfBuzzBufferFiller

---


Expand for full commit details
```
     
    To work safely, the macro needs the boundary to be greater than the 
    start index at the time of use. If this precondition is not met, an 
    overrun can occur. Fix this by using the correct buffer boundary. 
     
    Fixed: 491080830 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7655112 
    Commit-Queue: Rune Lillesveen <futhark@chromium.org> 
    Auto-Submit: Dominik Röttsches <drott@chromium.org> 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1597614} 
    (cherry picked from commit a8e675e9a31596b695262732746738e475ccac9a) 
     
    Change-Id: I09dc4a7a9b1cdc7f2e1d4cd3c9a878b61fdc6396 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7829178 
    Owners-Override: Michael Ershov <miersh@google.com> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Reviewed-by: Dominik Röttsches <drott@chromium.org> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4886} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/platform/fonts/shaping/case_mapping_harfbuzz_buffer_filler.cc`

---

Hash: [6998afa0166083d9ccc565bd5270ec797234e088](https://chromiumdash.appspot.com/commit/6998afa0166083d9ccc565bd5270ec797234e088)  

Date: Mon May 25 16:35:01 2026


---

### ch...@google.com (2026-06-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491080830)*
