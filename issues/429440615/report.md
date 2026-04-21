# Permission element inner div with style -webkit-text-stroke-width: thick;font-weight: bolder; can be abused if no element in the parent chain has any -webkit-text-stroke-width: thick;font-weight: bolder; are set. [429440615] - Chromium

| Field | Value |
|-------|-------|
| **Issue ID** | [429440615](https://issues.chromium.org/issues/429440615) |
| **Status** | Unknown |
| **Severity** | Unknown |
| **Priority** | Unknown |
| **Component** | Unknown |
| **Reporter** | Unknown |
| **Bounty** | Confirmed (amount unknown) |

## Description

This bug is similar to
https://issues.chromium.org/issues/398803201,
https://issues.chromium.org/issues/423670839,
https://issues.chromium.org/issues/428455319,
https://issues.chromium.org/issues/429270814

when -webkit-text-stroke-width: thick;font-weight: bolder;  are embedded in a tag above the <permission> tag, for example a div or something else, this affects the <permission> tag, thus covering the text in the <permission> tag. if style -webkit-text-stroke-width: thick;font-weight: bolder;   embedded directly in the <permission> tag are not affected. The impact is that sites can potentially trick users to trigger permission prompts even if the permission is currently in a DENY state for that origin. (It does not however bypass the permission prompt in any way)

references for some css that can and cannot be embedded in the <permission> tag: https://developer.chrome.com/blog/permission-element-origin-trial?hl=en

## Attachments

- unknown (, 0 B)
- unknown (, 0 B)
- unknown (, 0 B)
- unknown (, 0 B)

## Timeline

### ah...@google.com (2025-07-04)

[Primary Security Shepherd]

Provisionally setting severity to S3 similar to the linked issues.

Provisionally setting foundIn to the current extended stable

@an...@google.com could you please take a look?

Thanks!

### ch...@google.com (2025-07-05)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-07-08)

Project: chromium/src  
Branch: main  
Author: Andy Paicu [andypaicu@chromium.org](mailto:andypaicu@chromium.org)  
Link:      <https://chromium-review.googlesource.com/6705900>

[PEPC] Prevent -webkit-text-stroke/-webkit-text-fill on the permission element

---


Expand for full commit details

```
    Even though these properties are not allowed for the permission element, 
    it seems they get inherited to the inner text anyways. Therefore reset 
    them manually. 
     
    Fixed: 429440615 
    Change-Id: Ie17b82de959c92ba808d3c966385f31527ef2ea1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6705900 
    Reviewed-by: Mason Freed <masonf@chromium.org> 
    Commit-Queue: Andy Paicu <andypaicu@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1483611}
```

---

Files:

- M `third_party/blink/renderer/core/html/html_permission_element.cc`
- A `third_party/blink/web_tests/external/wpt/html/semantics/permission-element/text-stroke-and-fill-ref.html`
- A `third_party/blink/web_tests/external/wpt/html/semantics/permission-element/text-stroke-and-fill.tentative.html`

---

Hash: c5539496a8fd440a8f9ad62031184a109307efd7  
Date:  Tue Jul 8 08:46:38 2025



---

### sa...@gmail.com (2025-07-25)

redacted

### am...@chromium.org (2025-07-28)

Bugs are assessed by the VRP in order of severity. This issue will be assessed at a future VRP panel session, and as always, the report will be updated with the outcome of that assessment. Please refrain from pinging the report for updates in the meantime. Thank you for your patience.

### am...@chromium.org (2025-09-05)

A comprehensive reward for the various reports of similar, low / more abuse-like impact was issued via 428455319.

### ch...@google.com (2025-10-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### wf...@chromium.org (2025-11-13)

Reporter - please do not restrict your uploads, comments or delete comments.

The Chromium VRP relies on openness and it is a fundamental part of the program that bug reports and attachments will be public once fixed, so that other researchers can build upon the work on previous research, to help further secure our users.

If you continue to restrict and/or delete attachments (except for valid reasons such as accidental upload of PII) then the panel might consider future measures such as disqualification from the VRP program or other consequences at the panel's discretion.

### wf...@chromium.org (2025-11-13)

Re-uploading restricting attachment from comment 0

### sa...@gmail.com (2025-11-13)

Im sorry i have unrestricted it

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/429440615)*
