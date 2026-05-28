# WebAuthn Attestation dialog can hide the full-screen notification.

| Field | Value |
|-------|-------|
| **Issue ID** | [333313912](https://issues.chromium.org/issues/333313912) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Android |
| **Chrome Version** | 125.0.6402.0 - Pixel 7 Pro |
| **Reporter** | ch...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2024-04-08 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Go to <https://lbstyle.github.io/alert.html>
2. Click on the button and select "Use a different phone or tablet."
3. Observe that the full-screen notification doesn't appear at the right time.

# Problem Description

The full-screen notification should appear after tapping on "Use a different phone or tablet" directly.

# Summary

WebAuthn Attestation dialog can hide the full-screen notification.

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- [screen_spoof.mp4](attachments/screen_spoof.mp4) (video/mp4, 579.4 KB)
- [screen-20250219-063310.mp4](attachments/screen-20250219-063310.mp4) (video/mp4, 23.2 MB)

## Timeline

### ar...@chromium.org (2024-04-08)

From: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/shepherd.md#assign>

```
> Fullscreen bugs the Open Screen team is taking ownership of Full Screen issues, including security bugs.
> Please assign Full Screen security issues to takumif@chromium.org and cc: atadres@chromium.org,
> muyaoxu@google.com, and mfoltz@chromium.org. They are also working on holistic solutions to improving
> the security of fullscreen, so please remember to look for potential duplicates of ongoing work.

```

### ar...@chromium.org (2024-04-08)

I can reproduce on Android. Setting to Medium severity based on other fullscreen notification bugs.
Assigning to takumif@ for now. Please re-route as appropriate. Thanks!

### pe...@google.com (2024-04-08)

Setting milestone because of s2 severity.

### pe...@google.com (2024-04-08)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ta...@chromium.org (2024-04-08)

Jinsuk, do you know how we handle the overlap of other surfaces with the fullscreen toast in Clank?

### ji...@google.com (2024-04-08)

> Jinsuk, do you know how we handle the overlap of other surfaces with the fullscreen toast in Clank?

It was not always possible to my experiments. There are some Android system UI that can occlude Fullscreen toast, with apparently no workaround. Placing the toast in other positions won't do the trick either, since it has been just a matter of time that a new clever way to work around it pops up again. Which makes me think the toast is probably not the ideal way for the fullscreen notification.

### ji...@google.com (2024-04-08)

In case it is useful, I wrote up [a summary](https://docs.google.com/document/d/1buuKsV07d61mCtihR2zbTnwy3qW5j8BqGi4x44h9VnA/edit?tab=t.0#heading=h.w9xk49zanjp7) of my ongoing effort back then, against external Fullscreen security reports on Android. Feel free to let me know if you have questions. Some details might have already faded away in my head though.

### pe...@google.com (2024-04-23)

takumif: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-05-08)

takumif: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@gmail.com (2024-05-24)

Any update here? Thanks

### ch...@gmail.com (2024-11-28)

any update on this bug? thanks!

### li...@google.com (2024-12-02)

When I visit the site in c#0, it looks nothing like the demo -- it asks me to upload a photo.

### ch...@gmail.com (2024-12-02)

Sorry, I updated that link, but it looks like it's fixed. You can try to reproduce the issue manually.

1. Go to permission.site.
2. Tap Full-Screen.
3. Tap WebAuthn Attestation, then select "Use a different phone or tablet".

Observe that the full-screen warning appears when you cancel the dialog.

In the older version, even if you canceled the dialog, the full-screen warning did not appear for a long time.

### ch...@gmail.com (2024-12-11)

Can someone please verify this?

### ch...@gmail.com (2025-01-20)

Friendly ping.

### ch...@gmail.com (2025-02-19)

I think this was fixed by some earlier changes.

### ch...@gmail.com (2025-02-19)

Verified on 135.0.7019.0 Canary.

1. Go to https://lbstyle.github.io/alert.html
2. Click in the input and try to select "Use a different phone or tablet."

Observe that the full-screen notification appears at the right time. 

### ch...@gmail.com (2025-07-07)

Can someone please review this bug? It has been fixed for a while now.

### ch...@gmail.com (2025-10-30)

Verification is required according to comment #18.

### ch...@gmail.com (2025-12-09)

@muyaoxu Friendly ping. This issue has not been reproducible for quite some time. Could you update the status?

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
highly mitigated security UI spoofing


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-03-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/333313912)*
