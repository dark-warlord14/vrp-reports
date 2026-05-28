# Spoof on virtual keyboard

| Field | Value |
|-------|-------|
| **Issue ID** | [482433856](https://issues.chromium.org/issues/482433856) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | sa...@gmail.com |
| **Assignee** | pn...@chromium.org |
| **Created** | 2026-02-07 |
| **Bounty** | $2,000.00 |

## Description


VULNERABILITY DETAILS

The bug https://issues.chromium.org/issues/446463993 has been fixed, but this bug appears again in version 146.0.7673.0

when the virtual keyboard is displayed and at the same time the navigation is directed to the other pagethe virtual keyboard still appears and the color of the minibar above the virtual keyboard becomes dynamic (the color follows the --theme-color of the background color so that the writing in the minibar is the same so that the domain is not visible in this bug I use white color) , leading to a spoof.

OS: Android 16
Device: Samsung S25 Edge
Chrome Version:  146.0.7673.0 Canary

Steps to reproduce:
1. download detx1.html,spoofkeyboard1.html in same folder / host detx1.html,spoofkeyboard1.html on local web server using https:// protocol
2. open https://you-can-billowy-nimble-login-secure-docs-google-source-attacker.com/detx1.html or open detx1.html on local web server using https: protocol
3. click the textbox then click the button


## Attachments

- deleted (application/octet-stream, 0 B)
- [detx1.html](attachments/detx1.html) (text/html, 4.4 KB)
- deleted (application/octet-stream, 0 B)
- [spoofkeyboard1.html](attachments/spoofkeyboard1.html) (text/html, 1.1 KB)
- [2026-02-08_new.mp4](attachments/2026-02-08_new.mp4) (video/mp4, 1.1 MB)
- [Screenshot_20260208_080900_Chrome Canary.jpg](attachments/Screenshot_20260208_080900_Chrome Canary.jpg) (image/jpeg, 206.6 KB)
- [Screenshot_20260208_080843_Chrome Canary.jpg](attachments/Screenshot_20260208_080843_Chrome Canary.jpg) (image/jpeg, 89.3 KB)
- [Screen_Recording_20260211_190100_Chrome Canary.mp4](attachments/Screen_Recording_20260211_190100_Chrome Canary.mp4) (video/mp4, 3.0 MB)

## Timeline

### ts...@google.com (2026-02-09)

Setting provisional found-in per reporter, and platform to Android.

### ts...@google.com (2026-02-10)

Assigning per related bug.

### pn...@chromium.org (2026-02-10)

Could this be caused by <https://g-issues.chromium.org/issues/482210535> ?

### pn...@chromium.org (2026-02-10)

Let's check in after <https://crrev.com/c/7560758> lands

### ch...@google.com (2026-02-10)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-10)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### sa...@gmail.com (2026-02-11)

I can reproduce on version Chrome Canary 147.0.7681.0

### pe...@google.com (2026-02-11)

The NextAction date has arrived: 2026-02-11
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### go...@google.com (2026-02-11)

Reminder M146 is already in beta and Stable Promotion is coming soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you

### pn...@chromium.org (2026-02-11)

f2bf4b35730e0abfbbd8c40328b0d2db092f53d3 has not landed in a release vehicle yet. I'll test in a local build.

### pn...@chromium.org (2026-02-12)

I can repro in dev (147.0.7681.0) but not Canary (147.0.7682). I think <https://crrev.com/c/7560758> fixed this.

### ch...@google.com (2026-02-13)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pn...@google.com (2026-02-13)

The fix has already been merged to M146: <http://chromium-review.googlesource.com/c/chromium/src/+/7573416/>

### aj...@google.com (2026-03-11)

Setting Low severity as this has limited user impact.

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. Security UI Spoofing


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/482433856)*
