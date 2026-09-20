# PDFium NameTree lookup-only path still truncates /Limits

| Field | Value |
|-------|-------|
| **Issue ID** | [519007689](https://issues.chromium.org/issues/519007689) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | PDFium |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sd...@gmail.com |
| **Assignee** | ts...@google.com |
| **Created** | 2026-06-02 |
| **Bounty** | $500.00 |

## Description

PDFium CL 146590 states that lookup-only operations should not truncate the
/Limits array:

  Do not truncate /Limits array for lookup-only operations

However, current main still appears to trim /Limits in the lookup-only path.

In core/fpdfdoc/cpdf_nametree.cpp, SearchNameNodeByNameInternal() documents that
node_to_insert is non-null only when the caller wants insertion-position
information. CPDF_NameTree::LookupValue() calls SearchNameNodeByName() with
node_to_insert == nullptr, so nullptr is the lookup-only path.

Current code:

  // When lookup-only: do not truncate the /Limits array.
  if (!node_to_insert) {
    TrimNodeLimits(pLimits.Get());
  }

This seems reversed: lookup-only calls still execute TrimNodeLimits(). The
condition likely should be node_to_insert instead of !node_to_insert, or the
comment and CL intent need clarification.

The existing test GetFromTreeWithLimitsArrayWith4Items verifies lookup succeeds
with a 4-element /Limits array, but it does not assert that LookupValue() leaves
the /Limits array length unchanged. A regression check could assert that the
array still has size 4 after LookupValue().

Upstream CL:
https://pdfium-review.googlesource.com/c/pdfium/+/146590

Current file:
https://pdfium.googlesource.com/pdfium/+/refs/heads/main/core/fpdfdoc/cpdf_nametree.cpp

## Timeline

### ts...@google.com (2026-06-02)

Sure would seem that way. 

### ts...@google.com (2026-06-02)

https://pdfium-review.git.corp.google.com/c/pdfium/+/146590/11..12 proves I did this wrong.

### dx...@google.com (2026-06-02)

Project: pdfium  

Branch:  main  

Author:  Tom Sepez [tsepez@google.com](mailto:tsepez@google.com)  

Link:    <https://pdfium-review.googlesource.com/149034>

Fix logic botch in cpdf\_nametree.cpp

---


Expand for full commit details
```
     
    Introduced in 
      https://pdfium-review.googlesource.com/c/pdfium/+/146590 
     
    -- Add a better test. 
     
    Bug: 519007689 
    Change-Id: I98b01afc6e05941e3c2a10821cea88e9c275b354 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/149034 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    Auto-Submit: Tom Sepez <tsepez@chromium.org> 
    Reviewed-by: Lei Zhang <thestig@chromium.org> 
    Commit-Queue: Tom Sepez <tsepez@chromium.org>

```

---

Files:

- M `core/fpdfdoc/cpdf_nametree.cpp`
- M `core/fpdfdoc/cpdf_nametree_unittest.cpp`

---

Hash: 2dcb53e64dfe79c2388465420299b174dabef94c  

Date: Tue Jun 2 21:30:04 2026


---

### dx...@google.com (2026-06-03)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7897749>

Roll PDFium from d438a4e6186f to 2dcb53e64dfe (16 revisions)

---


Expand for full commit details
```
     
    https://pdfium.googlesource.com/pdfium.git/+log/d438a4e6186f..2dcb53e64dfe 
     
    2026-06-02 tsepez@google.com Fix logic botch in cpdf_nametree.cpp 
    2026-06-02 ask@chromium.org Update siso_version to b18cb0f263cfcc2f17a925cb211972a32dc211f6 
    2026-06-02 ask@chromium.org Roll third_party/skia/ d10ea850c..e4281d5a7 (283 commits; 48 trivial rolls) 
    2026-06-02 ask@chromium.org Roll third_party/libunwind/src/ 71192be15..d6c7a21e9 (1 commit) 
    2026-06-02 ask@chromium.org Roll tools/win/ d16e6b55b..faefd1b6f (2 commits) 
    2026-06-02 ask@chromium.org Roll third_party/clang-format/script/ 08cce2b81..6eddfb5ec (2 commits) 
    2026-06-02 ask@chromium.org Roll clang+rust 
    2026-06-02 ask@chromium.org Roll v8/ 8e10f842e..0c6c73eea (692 commits) 
    2026-06-02 aryankrishnan4b@gmail.com Replace c-style casts in cfgas_decimal.cpp with static_casts 
    2026-06-02 ask@chromium.org Roll third_party/rust/ dbc491d22..19243287c (57 commits) 
    2026-06-02 tycket033@gmail.com Prevent import hang on circular page parents 
    2026-06-01 ask@chromium.org Roll build, buildtools, libc++, and llvm-libc 
    2026-06-01 ask@chromium.org Roll third_party/nasm/ 358842b6b..525a09a81 (4 commits) 
    2026-06-01 ask@chromium.org Roll third_party/libjpeg_turbo/ d1f5f2393..640f254ad (2 commits) 
    2026-06-01 ask@chromium.org Roll third_party/freetype/src/ 6d9fc45fc..b08a2eb0d (29 commits) 
    2026-06-01 ask@chromium.org Roll Harfbuzz and icu 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/pdfium-autoroll 
    Please CC akall@google.com,dhoss@chromium.org,thestig@chromium.org on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:517126568,chromium:519007689 
    Tbr: akall@google.com 
    Change-Id: Ie3287873364cdacb2175b8e93fbc0d4745d915d9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7897749 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1640619}

```

---

Files:

- M `DEPS`
- M `third_party/pdfium`

---

Hash: [11ae0efa597ff9c2fd169fcbe7e6e178501b79a7](https://chromiumdash.appspot.com/commit/11ae0efa597ff9c2fd169fcbe7e6e178501b79a7)  

Date: Wed Jun 3 01:16:30 2026


---

### sd...@gmail.com (2026-06-03)

Security impact note:

This appears to be a follow-up issue in a fix for a CVE-class PDFium bug. Since
the current main branch still performs /Limits truncation in the lookup-only
path despite the stated security fix intent, could the security team please
assess whether this represents an incomplete fix or a security regression, and
whether it should be tracked under the existing CVE/bug or as a separate
security issue?

If this report is considered actionable under the Chrome VRP, please also route
it for the normal CVE and reward eligibility assessment.

### ch...@google.com (2026-06-03)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-06-04)

Requesting merge to M149 because latest trunk commit is in 151.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M150 because latest trunk commit is in 151.

### ch...@google.com (2026-06-04)

**M149** merge request created. **Please update [crbug/519857185](https://crbug.com/519857185) to have this merge reviewed.**

### ch...@google.com (2026-06-04)

**M150** merge request created. **Please update [crbug/519857066](https://crbug.com/519857066) to have this merge reviewed.**

### dx...@google.com (2026-06-08)

Project: pdfium  

Branch:  chromium/7827  

Author:  Tom Sepez [tsepez@google.com](mailto:tsepez@google.com)  

Link:    <https://pdfium-review.googlesource.com/149410>

[M149] Fix logic botch in cpdf\_nametree.cpp

---


Expand for full commit details
```
     
    Original change's description: 
    > Fix logic botch in cpdf_nametree.cpp 
    > 
    > Introduced in 
    >   https://pdfium-review.googlesource.com/c/pdfium/+/146590 
    > 
    > -- Add a better test. 
    > 
    > Bug: 519007689 
    > Change-Id: I98b01afc6e05941e3c2a10821cea88e9c275b354 
    > Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/149034 
    > Commit-Queue: Lei Zhang <thestig@chromium.org> 
    > Auto-Submit: Tom Sepez <tsepez@chromium.org> 
    > Reviewed-by: Lei Zhang <thestig@chromium.org> 
    > Commit-Queue: Tom Sepez <tsepez@chromium.org> 
     
    (cherry picked from commit 2dcb53e64dfe79c2388465420299b174dabef94c) 
     
    Bug: 519857185,519007689 
    Change-Id: I98b01afc6e05941e3c2a10821cea88e9c275b354 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/149410 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com>

```

---

Files:

- M `core/fpdfdoc/cpdf_nametree.cpp`
- M `core/fpdfdoc/cpdf_nametree_unittest.cpp`

---

Hash: be702d63baba7507bb1f6f6ff2d35be9c133c08c  

Date: Mon Jun 8 22:32:04 2026


---

### dx...@google.com (2026-06-08)

Project: pdfium  

Branch:  chromium/7871  

Author:  Tom Sepez [tsepez@google.com](mailto:tsepez@google.com)  

Link:    <https://pdfium-review.googlesource.com/149430>

[M150] Fix logic botch in cpdf\_nametree.cpp

---


Expand for full commit details
```
     
    Original change's description: 
    > Fix logic botch in cpdf_nametree.cpp 
    > 
    > Introduced in 
    >   https://pdfium-review.googlesource.com/c/pdfium/+/146590 
    > 
    > -- Add a better test. 
    > 
    > Bug: 519007689 
    > Change-Id: I98b01afc6e05941e3c2a10821cea88e9c275b354 
    > Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/149034 
    > Commit-Queue: Lei Zhang <thestig@chromium.org> 
    > Auto-Submit: Tom Sepez <tsepez@chromium.org> 
    > Reviewed-by: Lei Zhang <thestig@chromium.org> 
    > Commit-Queue: Tom Sepez <tsepez@chromium.org> 
     
    (cherry picked from commit 2dcb53e64dfe79c2388465420299b174dabef94c) 
     
    Bug: 519857066,519007689 
    Change-Id: I98b01afc6e05941e3c2a10821cea88e9c275b354 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/149430 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com>

```

---

Files:

- M `core/fpdfdoc/cpdf_nametree.cpp`
- M `core/fpdfdoc/cpdf_nametree_unittest.cpp`

---

Hash: c052afb72a08d79a26bcf3103d11f344981b09f1  

Date: Mon Jun 8 22:41:47 2026


---

### pe...@google.com (2026-06-08)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-06-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-06-12)

1. <https://pdfium-review.git.corp.google.com/c/pdfium/+/149770>
2. Medium. No conflicts, and even though I couldn’t run it through CQ, I’ve built it locally just fine.
3. M149 and M150
4. Yes

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Baseline. Other process renderer.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-06-22)

Project: pdfium  

Branch:  chromium/7559  

Author:  Tom Sepez [tsepez@google.com](mailto:tsepez@google.com)  

Link:    <https://pdfium-review.googlesource.com/149770>

[M144-LTS] Fix logic botch in cpdf\_nametree.cpp

---


Expand for full commit details
```
[M144-LTS] Fix logic botch in cpdf_nametree.cpp

Introduced in
  https://pdfium-review.googlesource.com/c/pdfium/+/146590

-- Add a better test.

Bug: 519007689
Change-Id: I98b01afc6e05941e3c2a10821cea88e9c275b354
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/149034
Commit-Queue: Lei Zhang <thestig@chromium.org>
Auto-Submit: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 2dcb53e64dfe79c2388465420299b174dabef94c)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/149770
Reviewed-by: Tom Sepez <tsepez@chromium.org>

```

---

Files:

- M `core/fpdfdoc/cpdf_nametree.cpp`
- M `core/fpdfdoc/cpdf_nametree_unittest.cpp`

---

Hash: e879aad21e9b1bed44355f5bd0af69e465dfdfbc  

Date: Mon Jun 22 22:44:43 2026


---

### sd...@gmail.com (2026-07-15)

Hi Chrome VRP Team,

Thank you for the reward decision.

I would like to ask whether this rewarded PDFium issue is eligible for CVE assignment.

The issue was awarded under:
Rationale: Baseline. Other process renderer.

The fix has been merged here:
<https://pdfium-review.googlesource.com/c/pdfium/+/149034>

Could you please confirm whether this issue is within scope for CVE assignment by Google CNA? If it is eligible, I would appreciate it if a CVE could be assigned. If it is not eligible, could you please let me know the reason so I can reference the issue appropriately in any future write-up?

Best regards,
Zhilei Zhang

### ch...@google.com (2026-09-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/519007689)*
