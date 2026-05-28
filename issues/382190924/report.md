# Extension popup can render over PWA Install Prompt

| Field | Value |
|-------|-------|
| **Issue ID** | [382190924](https://issues.chromium.org/issues/382190924) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Windows |
| **Chrome Version** | 131.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | ms...@google.com |
| **Created** | 2024-12-04 |
| **Bounty** | $500.00 |

## Description

# Steps to reproduce the problem

This vulnerability is almost the same as <https://issues.chromium.org/issues/40058873> but it occurs on PWA Install Prompt

# Problem Description

Install Extension
Click + Key press Ctr + A
Double click install pwa will install

# Additional Comments

Version 133.0.6847.2 (Official Build) dev (64-bit)
Attaching Video Proof

# Summary

Extension popup can render over PWA Install Prompt

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [screen-capture (2).webm](attachments/screen-capture (2).webm) (video/webm, 781.9 KB)
- [extensionpopuppwa.zip](attachments/extensionpopuppwa.zip) (application/zip, 3.0 KB)
- [pwa.zip](attachments/pwa.zip) (application/zip, 3.5 KB)
- [screen-capture (21).webm](attachments/screen-capture (21).webm) (video/webm, 1.1 MB)

## Timeline

### ja...@google.com (2024-12-04)

[security shepherd] Apologies. I added the NextAction to the wrong bug. I'll take a look

### an...@chromium.org (2024-12-05)

[secondary security shepherd]: This looks to be a realistic spoofing scenario, and the PoC looks almost exactly the same as [issue 359949844](https://issues.chromium.org/issues/359949844). Assigning this to [kerenzhu@google.com](mailto:kerenzhu@google.com) to see if this issue still persists or if this is seems to be a new use case.

### ke...@google.com (2024-12-05)

The protection was [added](https://crrev.com/c/5995850) to PWAConfirmationBubbleView and the entire class was [removed](https://chromium-review.googlesource.com/c/chromium/src/+/6065542) yesterday (11/04).

msiem@, I think you are familiar with the new PWA installation dialogs. Can you help set up the protection there?

### li...@gmail.com (2024-12-31)

deleted

### am...@chromium.org (2025-05-08)

hi kerenzhu@ and msiem@, the reporter of this issues believes this issue to be resolved. Can you please confirm this has been resolved, and if so, please add the resolving CL to `fixed by code changes` field. Thanks in advance.

### li...@gmail.com (2025-05-13)

Video Proof

### aj...@chromium.org (2025-05-30)

May be a dupe of [issue 382540635](https://issues.chromium.org/issues/382540635)

### aj...@chromium.org (2025-05-30)

(note: this issue reported earlier than 382540635)

### ke...@google.com (2025-05-30)

It was fixed and then regressed, see my explanation at <http://b/382190924#comment4>.

### di...@google.com (2025-05-30)

I believe this was fixed in [this CL](https://chromium-review.googlesource.com/c/chromium/src/+/6395316), which [landed v136.0.7093.0 onwards](https://chromiumdash.appspot.com/commit/948ad96d4f4b30e0a785c96295a644c71988dd60). We can mark this as closed.

### ch...@google.com (2025-05-30)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
report of lower impact security UI issue, with low potential for exploitability and low potential for user harm


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### li...@gmail.com (2025-06-05)

tks

### ch...@google.com (2025-09-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/382190924)*
