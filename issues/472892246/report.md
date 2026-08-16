# Chrome Android address bar shows stale eTLD when navigating to longer attacker-controlled domains

| Field | Value |
|-------|-------|
| **Issue ID** | [472892246](https://issues.chromium.org/issues/472892246) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Chrome Version** | 145.0.7608.0 |
| **Reporter** | ga...@gmail.com |
| **Assignee** | pe...@google.com |
| **Created** | 2026-01-02 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Open Chrome on Android (tested on Chrome Canary 142.0.7396.0, Android 15).
2. In a single tab, navigate to:
   <https://www.aaaaa.auths.account.google.c>
3. Observe that the address bar correctly displays:
   <https://www.aaaaa.auths.account.google.c>
4. Without opening a new tab, navigate to:
   <https://www.aaaaa.auths.account.google.c.rebelsec.id>
5. Observe that the address bar still displays:
   <https://www.aaaaa.auths.account.google.c>
   even though the actual origin has changed.
6. Repeat the same steps with other domains:
   - <https://www.aaaaa.auths.account.google.ru>
     → <https://www.aaaaa.auths.account.google.ru.rebelsec.idds>
   - <https://www.aaaaa.auths.account.google.co.id>
     → <https://www.aaaaa.auths.account.google.co.id.evilsite.com>
7. In all cases, the address bar continues to display the previous eTLD-based domain,
   while the loaded page is served from an attacker-controlled suffix domain.

# Problem Description

Chrome Android fails to update the visible address bar when navigating within the same
tab from a long, trusted-looking domain to a longer attacker-controlled domain that
shares the same prefix.

After visiting a crafted domain such as:
<https://www.aaaaa.auths.account.google.co.id>

and navigating to:
<https://www.aaaaa.auths.account.google.co.id.evilsite.com>

the address bar continues to display:
<https://www.aaaaa.auths.account.google.co.id>

This results in a mismatch between the displayed URL and the actual page origin.
The user is led to believe they are still on a trusted domain, while the content
is served from an attacker-controlled domain.

This behavior is state-dependent and occurs when navigation happens within the same tab.
Opening the attacker-controlled URL in a fresh tab correctly displays the full domain.

This behavior appears related to previous Chromium issues Spoof on Address Bar

- <https://issues.chromium.org/issues/443408317> but differs in that the
  displayed domain is entirely stale rather than merely truncated.

# Summary

Chrome Android address bar shows stale eTLD when navigating to longer attacker-controlled domains

# Custom Questions

#### Reporter credit:

Galatia Sijabat

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [PoC.mp4](attachments/PoC.mp4) (video/mp4, 9.2 MB)
- [WhatsApp Image 2026-01-02 at 20.00.58.jpeg](attachments/WhatsApp Image 2026-01-02 at 20.00.58.jpeg) (image/jpeg, 24.4 KB)
- [WhatsApp Image 2026-01-02 at 20.01.44.jpeg](attachments/WhatsApp Image 2026-01-02 at 20.01.44.jpeg) (image/jpeg, 23.8 KB)
- [WhatsApp Image 2026-01-02 at 20.02.32.jpeg](attachments/WhatsApp Image 2026-01-02 at 20.02.32.jpeg) (image/jpeg, 25.2 KB)

## Timeline

### ke...@chromium.org (2026-01-02)

Thanks for the report.

This does appear to be a quirky behaviour. Following the initial navigation, the omnibox displays the the end of the domain in the URL. But after a subsequent navigation that makes the URL longer, it does not. This likely means the display window for the URL is not being updated even though the domain has changed.

Flagging as low severity.

pnoland@: Is this something easy to fix?

### ga...@gmail.com (2026-04-22)

Hi,

just checking in — is there any update on this issue?

### pe...@google.com (2026-04-22)

I think pnoland@ landed a fix for this a while ago. I can't repro this anymore.

### ch...@google.com (2026-04-22)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ga...@gmail.com (2026-05-01)

Hi,

Thank you for the update.

I’d like to clarify the current resolution, as there seems to be a mismatch in the bug history:

- The issue was initially triaged as a valid UI inconsistency in the omnibox (P2 / S3), where the address bar displayed a stale eTLD after navigation.
- Later, it was mentioned that the issue had been fixed and was no longer reproducible.
- However, the bug is now marked as “Won’t Fix (Not reproducible)” and the “Fixed By Code Changes” field is still empty.

From my understanding, if the issue is no longer reproducible due to a fix, this would indicate that the reported behavior was valid at the time of submission.

Could you please clarify:

1. Whether this issue was indeed fixed, and if so, which CL(s) addressed it?
2. If it was fixed, whether this report qualifies for VRP reward?

I appreciate your time and clarification.

### ke...@chromium.org (2026-05-07)

peilinwang@: Can you please look at the questions in [comment #6](https://issues.chromium.org/issues/472892246#comment6)?

If this was a known issue that was fixed then it should be duped into the previous bug. Either way the resolution should be clarified.

### pe...@google.com (2026-05-07)

Sorry didn't get to this earlier, I updated the bug.

### pe...@google.com (2026-05-07)

I don't know anything about the VRP reward.

### ke...@chromium.org (2026-05-07)

This bug is older, so I am going to reverse the duplication. The VRP panel will sort it out.

### ga...@gmail.com (2026-05-17)

Hi team,

any updates regarding the VRP decision?

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Security UI Spoofing


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ga...@gmail.com (2026-05-22)

Hi team,

Thanks for the bounty, I really appreciate it!

I also wanted to ask whether this report would be eligible for public disclosure or receive a CVE assignment in the future.

### ch...@google.com (2026-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/472892246)*
