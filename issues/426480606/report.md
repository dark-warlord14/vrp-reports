# open link in split view view leads to the origin of an external protocol handler prompt obscured (Windows)

| Field | Value |
|-------|-------|
| **Issue ID** | [426480606](https://issues.chromium.org/issues/426480606) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip>SplitView |
| **Platforms** | Windows |
| **Chrome Version** | 138.0.7204.35 |
| **Reporter** | pu...@gmail.com |
| **Assignee** | ag...@google.com |
| **Created** | 2025-06-20 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. Enable the #side-by-side flag
2. Open <https://microsoft-application-new-ai.glitch.me> in Chrome Browser
3. Right click and open in Split view

`Result:` external protocol handler prompt obscured and showing above microsoft.com

# Problem Description

opening link in split view leads to origin of an external protocol handler prompt could have been obscured could lead to spoofing in split view window and leads to execute

Attacker can disable opening links So the attacker instruct user to open in split view, the user tries to open link in split view this leads the origin of an external protocol handler prompt could have been obscured lead to spoofing and execute harmful protocol

the origin can be hidden from the external protocol dialog which leads to execute malicious external protocol applications
in split view external protocol handler prompt could have been obscured could lead to spoofing and leads to execute malicious protocol

# Summary

open link in split view view leads to the origin of an external protocol handler prompt obscured

# Custom Questions

#### Reporter credit:

Puf

# Additional Data

Category: Security   

Chrome Channel: Beta   

Regression: N/A \

## Attachments

- [chrome repro.mp4](attachments/chrome repro.mp4) (video/mp4, 2.6 MB)
- expected.png (image/png, 77.1 KB)
- actual.png (image/png, 49.6 KB)
- deleted (application/octet-stream, 0 B)
- [Verified Fix.mp4](attachments/Verified Fix.mp4) (video/mp4, 313.6 KB)

## Timeline

### aj...@google.com (2025-06-20)

CCing split view folks to take a look and setting severity Medium as an omnibox spoof.

### aj...@google.com (2025-06-20)

impact=None as this needs a flag.

### aj...@google.com (2025-06-20)

It would also be helpful if the right component can be added :)

### ag...@google.com (2025-06-23)

From initial testing it appears that the behavior for "Open link in new tab" and "Open in split view" is the same. Can you clarify whether there is a bug with the existing "Open link in new tab" as well or if not, what the difference in behavior between that and "Open in split view" is?

### pu...@gmail.com (2025-06-23)

there is existing bug " Open link in new window "

" <https://issues.chromium.org/issues/40056198> "

### pe...@google.com (2025-06-23)

Thank you for providing more feedback. Adding the requester to the CC list.

### ag...@google.com (2025-06-24)

redacted

### ag...@google.com (2025-06-24)

Added this bug to our list of tasks for the project. I'll unassign myself so anyone on my team can pick it up

### dc...@chromium.org (2025-06-27)

Sorry, but security bugs should have an owner :) Even if it's just medium severity.

### ag...@google.com (2025-06-27)

Bugjuggler: wait 4w -> agale@

### bu...@google.com (2025-06-27)

Hi. I've received your bug and will wait until 2025-07-25 10:54 -0700 PDT and then assign the bug to agale.

### za...@google.com (2025-08-07)

Bugjuggler: wait 4w -> agale@

Hi agle@, can you please help assign this bug to an owner? Security bug should have an owner. Thanks!

### za...@google.com (2025-08-07)

deleted

### bu...@google.com (2025-08-07)

Hi. I've received your bug and will wait until 2025-09-04 13:13 -0400 EDT and then assign the bug to agale.

### ag...@google.com (2025-08-12)

It looks like the site used for the repro steps is no longer up. WOuld you be able to provide an HTML version of this page? I think this might have been fixed by this CL so I want to confirm: https://chromium-review.googlesource.com/c/chromium/src/+/6838198

### pu...@gmail.com (2025-08-12)

Glitch service stopped, I forgot to upload poc file

here i have Attached POC html file

I have verified this issue is fixed

Steps to reproduce the problem

1. Enable the #side-by-side flag
2. Upload file in your server and Open POC link file in Chrome Browser
3. Right click and open in Split view

`Result:` Spoof in split view

Thank you

### pu...@gmail.com (2025-08-12)

I Have created Latest Video and verified this issue is fixed. Version 141.0.7344.1 canary

Thank you

### ag...@google.com (2025-08-12)

Great, thanks for confirming!

### sp...@google.com (2025-08-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### pu...@gmail.com (2025-08-22)

Thank you so much

### ch...@google.com (2025-11-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/426480606)*
