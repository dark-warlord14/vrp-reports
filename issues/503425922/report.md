# apply_stch uint32 accumulation OOB write (Chromium renderer SEGV)

| Field | Value |
|-------|-------|
| **Issue ID** | [503425922](https://issues.chromium.org/issues/503425922) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Fonts |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2026-04-16 |
| **Bounty** | $10,000.00 |

## Description

---

### Report description

apply\_stch uint32 accumulation OOB write (Chromium renderer SEGV)

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/third_party/+/refs/heads/main>

---

### The problem

#### Please describe the technical details of the vulnerability

- Upstream advisory: <https://github.com/harfbuzz/harfbuzz/security/advisories/GHSA-5xrh-8c3h-7c49>
- Upstream fix PR: <https://github.com/harfbuzz/harfbuzz/pull/5929>

## Summary

In HarfBuzz `apply_stch` (`src/hb-ot-shaper-arabic.cc`), the MEASURE pass
accumulates `extra_glyphs_needed` (uint32) across multiple STCH groups in
one buffer. The overflow-detected `break` exits only the inner per-group
loop; the outer `step` loop continues to CUT, which walks all groups and
writes the full (non-wrapped) number of entries into a buffer sized by the
partial pre-overflow value. Result: heap OOB write.

Chromium is reachable because Blink feeds an entire Arabic script run to
`hb_shape()` with no fragment cap (Firefox has `MAX_SHAPING_LENGTH=32760`).

## Repro

Artifacts (this directory):

- `stch_of3.ttf` – 844 B crafted font; `stch` → `beh → [tile_f, tile_r]`
- `poc.html` – `@font-face` loads the font, lays out 16,909,322 ×
  `BEH ALEF` pairs in one RTL run.

Serve and point an ASan Chromium at the page:

```
python3 -m http.server 8899 &
ASAN_OPTIONS="log_path=/tmp/asan.log:handle_segv=1:allow_user_segv_handler=0:detect_leaks=0:symbolize=1" \
  ~/asan/asan-chromium/content_shell --no-sandbox --disable-hang-monitor \
  http://127.0.0.1:8899/poc.html

# takes 10-60s

```

Renderer SEGVs after page load; ASan log at `/tmp/asan.log.<pid>`.

## Root cause

`src/hb-ot-shaper-arabic.cc` MEASURE block (pre-fix):

```
if (unlikely (hb_unsigned_mul_overflows (n_copies, n_repeating, &added_glyphs) ||
              hb_unsigned_add_overflows (extra_glyphs_needed, added_glyphs,
                                         &extra_glyphs_needed)))
  break;            // exits inner loop only

```

After the break, the outer `if (step == MEASURE) { buffer->ensure (…); }`
uses the partial `extra_glyphs_needed` → small allocation → CUT OOB.

## Credit

Matej Smycka

#### Impact analysis

Any website the victim visits can trigger this bug by serving a crafted font and some Arabic text. It reliably crashes the renderer tab on 64bit as the write lands far outside the process memory. 32bit would land into the process. The 64bit is unlikely to be exploited as controlled write, however it may be possible.

---

### The cause

#### What version of Chrome have you found the security issue in?

148.0.7750.0 [ASan content\_shell, Linux x86\_64]

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Matej Smycka

## Attachments

- [asan-stacktrace-symbolized.txt](attachments/asan-stacktrace-symbolized.txt) (text/plain, 23.2 KB)
- [stch_of3.ttf](attachments/stch_of3.ttf) (font/ttf, 844 B)
- [poc.html](attachments/poc.html) (text/html, 693 B)

## Timeline

### an...@chromium.org (2026-04-17)

This seems to be an unfixed variant of <https://issues.chromium.org/491516670> perhaps?
Setting severity to S1 (memory corruption in renderer).

### an...@chromium.org (2026-04-17)

Setting FoundIn to 147 based on age of previous fix. Please update if not accurate.

### ch...@google.com (2026-04-18)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-18)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ch...@google.com (2026-05-04)

**M148** merge request created. **Please update [crbug/509414656](https://crbug.com/509414656) to have this merge reviewed.**

### dx...@google.com (2026-05-08)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Dominik Röttsches [drott@chromium.org](mailto:drott@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7810458>

[merge] Cherry-pick apply\_stch() fix

---


Expand for full commit details
```
     
    Cherry-pick upstream fix for issue below: 
    https://github.com/harfbuzz/harfbuzz/pull/5929 
     
    Merging by pulling in chromium/m148 branch of HarfBuzz 
    which I prepared earlier. 
     
    https://chromium-review.googlesource.com/q/project:external/github.com/harfbuzz/harfbuzz+branch:chromium/m148 
     
    Bug: 503425922 
    Fixed: 509414656 
    Change-Id: I2987b5f1d4f2ba3d559c58b84fa3a3f68beae9ef 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7810458 
    Reviewed-by: Daniil Sakhapov <sakhapov@chromium.org> 
    Commit-Queue: Dominik Röttsches <drott@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7778@{#2552} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `DEPS`
- M `third_party/harfbuzz/src`

---

Hash: [71a1e763a70a51e868e52b61c4906fa113d19e40](https://chromiumdash.appspot.com/commit/71a1e763a70a51e868e52b61c4906fa113d19e40)  

Date: Fri May 8 20:00:46 2026


---

### pe...@google.com (2026-05-08)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2026-05-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
High quality. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503425922)*
