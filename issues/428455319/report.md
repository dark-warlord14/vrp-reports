# Permission element inner div with style text-emphasis:꧁; and text-emphasis-position: over right; can be abused if no element in the parent chain has any text-emphasis:꧁; and text-emphasis-position: over right; are set.

| Field | Value |
|-------|-------|
| **Issue ID** | [428455319](https://issues.chromium.org/issues/428455319) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Permissions>PermissionElement |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2025-06-29 |
| **Bounty** | $1,000.00 |

## Description

This bug is similar to 
https://issues.chromium.org/issues/398803201, 
https://issues.chromium.org/issues/423670839

when text-emphasis:꧁; and text-emphasis-position: over right; are embedded in a tag above the <permission> tag, for example a div or something else, this affects the <permission> tag, thus covering the text in the <permission> tag. if style text-emphasis:꧁; and text-emphasis-position: over right;  embedded directly in the <permission> tag are not affected. The impact is that sites can potentially trick users to trigger permission prompts even if the permission is currently in a DENY state for that origin. (It does not however bypass the permission prompt in any way)

references for some css that can and cannot be embedded in the <permission> tag: https://developer.chrome.com/blog/permission-element-origin-trial?hl=en

## Attachments

- [pocpepc.html](attachments/pocpepc.html) (text/html, 1.5 KB)
- [bandicam 2025-06-29 20-56-04-190.mp4](attachments/bandicam 2025-06-29 20-56-04-190.mp4) (video/mp4, 2.9 MB)

## Timeline

### dc...@chromium.org (2025-06-30)

Marking this as no security impact (since this appears to be an experimental web platform feature) and low severity similar to the other bugs in this area.

### dc...@chromium.org (2025-06-30)

Though hmm, maybe this is actually an origin trial, in which case it's not security impact none... let me look a bit more closely.

### an...@chromium.org (2025-06-30)

The impact is that it can allow a site to trigger a permission request even if it was previously blocked. It is an origin trial indeed, though I'm not sure how much this falls under security vs annoyance.

### sa...@gmail.com (2025-06-30)

some css elements are restricted to prevent clickjcking or other phishing https://github.com/andypaicu/PEPC/blob/main/explainer.md#locking-the-pepc-style

### ch...@google.com (2025-06-30)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@gmail.com (2025-06-30)

deleted

### dx...@google.com (2025-07-02)

Project: chromium/src  

Branch: main  

Author: Thomas Nguyen [tungnh@chromium.org](mailto:tungnh@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6696007>

[PEPC] Reset CSS inherited style for permission's internal text element.

---


Expand for full commit details
```
     
    This ensures that the permission's internal text will not inherit text 
    style from its parent. 
     
     
    Bug: 428455319 
    Change-Id: I8d4b61efe010fd4ea24913afaaafba8b9105a80f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6696007 
    Commit-Queue: Thomas Nguyen <tungnh@chromium.org> 
    Reviewed-by: Joey Arhar <jarhar@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1481641}

```

---

Files:

- M `third_party/blink/renderer/core/html/resources/permission.css`
- A `third_party/blink/web_tests/external/wpt/html/semantics/permission-element/inherited-css-ref.html`
- A `third_party/blink/web_tests/external/wpt/html/semantics/permission-element/inherited-css-tentative.html`

---

Hash: 6ab0f046554dcc728e6e875de79578ae95bb3e5f  

Date:  Wed Jul 2 15:41:08 2025


---

### sa...@gmail.com (2025-07-03)

is this already fixed?

### tu...@chromium.org (2025-07-04)

Yes, marked as fixed. Thanks for the report.

### sa...@gmail.com (2025-07-25)

Hi thank you, is this report eligible for reward like https://issues.chromium.org/issues/423670839 (same as this report)?

### am...@chromium.org (2025-07-28)

Bugs are assessed by the VRP in order of severity. This issue will be assessed at a future VRP panel session, and as always, the report will be updated with the outcome of that assessment. Please refrain from pinging the report for updates in the meantime. Thank you for your patience.

### sp...@google.com (2025-09-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
$1,000 comprehensive reward for multiple reports of this low impact security UI issue in various places in Permission Element (for issue 428455319, 429440615, 433820888, 437510229, and not yet resolved issues 429270814 and 425159951) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-10-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### aj...@chromium.org (2025-10-23)

Please unrestrict pocs, description and comments.

### sa...@gmail.com (2025-10-23)

hi sorry i have unrestricted it thank you

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/428455319)*
