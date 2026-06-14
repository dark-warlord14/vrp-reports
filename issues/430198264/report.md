# IntersectionObserver's visibility check can be bypassed through SVG filters

| Field | Value |
|-------|-------|
| **Issue ID** | [430198264](https://issues.chromium.org/issues/430198264) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Geometry |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2025-07-08 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

`IntersectionObserver` has the `trackVisibility` option to make sure that an element is visible to the user. This is used to prevent clickjacking, since a parent frame can no longer cover the element with its own graphics in order to trick the user into performing an unwanted action.

However, through some trickery, an undetectable overlay can still be created by using SVG filters. For example, it is possible to use the `feDisplacementMap` filter to put graphics in an area up to 10% beyond the element bounds.

Doing this would still be detected by the `IntersectionObserver`, but this can be bypassed by quickly changing the opacity of the element (doing so probably resets its bounds somehow?).

The result is the ability to controllably cover up an iframe with any kinds of graphics without setting off its `IntersectionObserver`.

**VERSION**  

Chrome Version: Stable, 140.0.7259.2 Dev
Operating System: Windows, Android, macOS

**REPRODUCTION CASE**

1. Download the included files.
2. Open `invisible-bypass.html`.
3. Observe how the frame on the page gets covered with a fake button, but its background is still green (it'd turn red if not visible).
4. Click the fake button.

Note: To make testing the repro easier, the target frame is same-origin. This vulnerability works cross-origin too, as demonstrated in my demo video.

**CREDIT INFORMATION**  

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?  

Reporter credit: Lyra Rebane (rebane2001)

## Attachments

- demo.mp4 (video/mp4, 168.4 KB)
- overlay.png (image/png, 1.1 KB)
- target.html (text/html, 1016 B)
- isvisible-bypass.html (text/html, 750 B)
- target.html (text/html, 1018 B)

## Timeline

### re...@gmail.com (2025-07-08)

Impact is similar to that of [Issue 333708039](https://issues.chromium.org/issues/333708039)

### el...@chromium.org (2025-07-08)

Thanks for the report! I reproduced the described behavior with 137.0.7151.120 (current stable) and 140.0.7281.0 (current canary) on macOS 15.5. Apparently we are supposed to provide a strong guarantee that [IntersectionObserver doesn't deliver false positives for isVisible](https://web.dev/articles/intersectionobserver-v2#how_does_intersection_observerv2_fix_this) so I agree that this is a security bug as well. I'm going to call this Severity-Medium provisionally and route it to the Blink Geometry team.

### el...@chromium.org (2025-07-08)

I'm guessing that 138 and 139 are affected by this as well, but I have not tested on those versions.

### re...@gmail.com (2025-07-08)

Yep I tested on 138 too, it's affected.

### re...@gmail.com (2025-07-08)

Fixed the alert text in target.html (doesn't affect repro).

### el...@chromium.org (2025-07-08)

-> szager@ from 333708039 :)

### ch...@google.com (2025-07-09)

Setting milestone because of s2 severity.

### ch...@google.com (2025-07-23)

szager: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-07)

szager: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-22)

szager: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-06)

szager: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-21)

szager: Uh oh! This issue still open and hasn't been updated in the last 74 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-06)

szager: Uh oh! This issue still open and hasn't been updated in the last 89 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-21)

szager: Uh oh! This issue still open and hasn't been updated in the last 104 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-05)

szager: Uh oh! This issue still open and hasn't been updated in the last 119 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-20)

szager: Uh oh! This issue still open and hasn't been updated in the last 134 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-05)

szager: Uh oh! This issue still open and hasn't been updated in the last 149 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-20)

szager: Uh oh! This issue still open and hasn't been updated in the last 164 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-04)

szager: Uh oh! This issue still open and hasn't been updated in the last 179 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-19)

szager: Uh oh! This issue still open and hasn't been updated in the last 194 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-02-03)

szager: Uh oh! This issue still open and hasn't been updated in the last 209 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-02-18)

szager: Uh oh! This issue still open and hasn't been updated in the last 224 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-02-20)

Project: chromium/src  

Branch:  main  

Author:  Stefan Zager [szager@chromium.org](mailto:szager@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7597074>

Fix equality operator for blink::ReferenceFilterOp

---


Expand for full commit details
```
     
    Filter operations are created during style recalc, but some of them 
    (specifically, box-reflect and reference filters) need layout 
    information to compute their visual overflow extent. For box-reflect, 
    this is handled by always creating the filter operation ad hoc when 
    requested[1], presumably after pre-paint has generated the necessary 
    geometry information. For reference filters, this is handled by 
    annotating the style-generated ReferenceFilterOp with its fully resolved 
    compositor filter during pre-paint[2]. 
     
    It can happen that a ReferenceFilterOp is re-created during style 
    recalc, even when the operation has not changed. When this happens, the 
    style diff passed to StyleDidChange() won't indicate that filters have 
    changed, because the equality comparison for ReferenceFilterOp doesn't 
    check whether the resolved compositor filters match. If nothing else in 
    the style diff causes the element to be marked for paint property 
    update, it will skip the building of compositor filters during 
    pre-paint, and the ReferenceFilterOp will not get annotated with its 
    resolved compositor filter. This doesn't break rendering, because the 
    EffectPaintPropertyNode will continue to point to the 
    previously-computed compositor filter. However, it *does* break hit 
    testing of visual overflow, which relies on the style-created 
    FilterReferenceOp being annotated with the compositor filter[3]. 
     
    This CL changes the equality comparison for ReferenceFilterOp so that it 
    considers the annotated compositor filter. A pointer comparison is 
    sufficient; for a newly-created ReferenceFilterOp it will always be 
    `nullptr` and should force paint property update. 
     
    [1]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/paint/paint_layer.cc;drc=d209eefee6037bd0905e43f88570fda8edab89a1;l=2397 
     
    [2]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/paint/filter_effect_builder.cc;drc=3bbce24997c008ef45d4253542ec7f0a5a97e571;l=402 
     
    [3]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/style/filter_operation.cc;drc=d209eefee6037bd0905e43f88570fda8edab89a1;l=46 
     
    Bug: 430198264 
    Change-Id: I6f3215a603a6ed831431635c37d865216d0bb333 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7597074 
    Commit-Queue: Stefan Zager <szager@chromium.org> 
    Reviewed-by: Philip Rogers <pdr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1588040}

```

---

Files:

- M `third_party/blink/renderer/core/layout/hit_testing_test.cc`
- M `third_party/blink/renderer/core/style/filter_operation.cc`

---

Hash: [cd1b8be760040aeaa4ad11783bdcf550947920bd](https://chromiumdash.appspot.com/commit/cd1b8be760040aeaa4ad11783bdcf550947920bd)  

Date: Fri Feb 20 21:22:41 2026


---

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
Moderate impact exploit mitigation bypass


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### re...@gmail.com (2026-03-11)

awesome, thank you! <3

### ch...@google.com (2026-05-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/430198264)*
