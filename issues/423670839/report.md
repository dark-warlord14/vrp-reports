# Permission element inner div  with style text-decoration-line: line-through; and text-decoration-thickness  can be abused if no element in the parent chain has any text-decoration-line: line-through; and text-decoration-thickness are  set.

| Field | Value |
|-------|-------|
| **Issue ID** | [423670839](https://issues.chromium.org/issues/423670839) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Permissions>PermissionElement |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2025-06-10 |
| **Bounty** | $500.00 |

## Description

This bug is similar to <https://issues.chromium.org/issues/398803201>, when text-decoration-line: line-through; and text-decoration-thickness: are embedded in a tag above the <permission> tag, for example a div or something else, this affects the <permission> tag, thus covering the text in the <permission> tag. if style text-decoration-line: line-through; and text-decoration-thickness embedded directly in the <permission> tag are not affected. The impact is that sites can potentially trick users to trigger permission prompts even if the permission is currently in a DENY state for that origin. (It does not however bypass the permission prompt in any way)

references for some css that can and cannot be embedded in the <permission> tag:
<https://developer.chrome.com/blog/permission-element-origin-trial?hl=en>

## Attachments

- [fontpepc.html](attachments/fontpepc.html) (text/html, 1.4 KB)
- [bandicam 2025-06-10 11-19-20-944.mp4](attachments/bandicam 2025-06-10 11-19-20-944.mp4) (video/mp4, 2.6 MB)

## Timeline

### ke...@chromium.org (2025-06-11)

Thanks for the report.

andypaicu@: PTAL?

Not entirely related to the report, but trying to reproduce this on Canary I see a crash. I don't know if you want to create a separate bug for that, or if it's already known: crash/a6c6e9b4058efb00

### ch...@google.com (2025-06-12)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-06-28)

Project: chromium/src  

Branch: main  

Author: Thomas Nguyen [tungnh@chromium.org](mailto:tungnh@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6681790>

[PEPC] Disallow text-decoration CSS property

---


Expand for full commit details
```
     
    The CSS Text Decoration Module Level 3 spec (https://drafts.csswg.org/css-text-decor-3/#decorating-box) says PEPC's internal container needs `display: inline-box`. That doesn't work with our current layout, so we'll just reset the base text-decoration to get the same result. 
     
    Bug: 423670839 
    Change-Id: I53b574d2bc2c9e0e03b62a145cce3f682466866e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6681790 
    Reviewed-by: Joey Arhar <jarhar@chromium.org> 
    Commit-Queue: Thomas Nguyen <tungnh@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1480204}

```

---

Files:

- M `third_party/blink/renderer/core/html/html_permission_element.cc`
- A `third_party/blink/web_tests/external/wpt/html/semantics/permission-element/text-decoration-ref.html`
- A `third_party/blink/web_tests/external/wpt/html/semantics/permission-element/text-decoration-tentative.html`

---

Hash: 9344dfce9c3a39fd2f6757d3b20390a86f5e5298  

Date:  Sat Jun 28 08:42:47 2025


---

### sa...@gmail.com (2025-06-30)

some css elements are restricted to prevent clickjcking or other phishing https://github.com/andypaicu/PEPC/blob/main/explainer.md#locking-the-pepc-style

### sp...@google.com (2025-07-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Thank you reward for report of a lower-impact issue that resulted in a security beneficial change


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-10-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### aj...@chromium.org (2025-10-23)

Please unrestrict pocs, description and comments.

### sa...@gmail.com (2025-10-23)

hi sorry i have unrestricted it thank you

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/423670839)*
