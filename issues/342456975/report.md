#  URL spoof in Omnibox

| Field | Value |
|-------|-------|
| **Issue ID** | [342456975](https://issues.chromium.org/issues/342456975) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Accessibility>ReadingMode, UI>Browser>Omnibox |
| **Platforms** | Windows |
| **Chrome Version** | 127.0.6493.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | jd...@chromium.org |
| **Created** | 2024-05-24 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Go to any website e.g badssl.com then navigate to google.com
2. Right-click and select "Open in reading mode"
3. Go back to badssl.com

# Problem Description

badss.com site is displayed in content area but address bar is incorrect.

# Summary

URL spoof in Omnibox

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- [Screencast from 24 ماي, 2024 +01 02:42:44.webm](attachments/Screencast from 24 ماي, 2024 +01 02_42_44.webm) (application/octet-stream, 787.8 KB)
- [screen-capture.webm](attachments/screen-capture.webm) (video/webm, 4.0 MB)

## Timeline

### bo...@google.com (2024-05-24)

I am unable to reproduce. I tried 127.0.6485.0 (canary/ToT), 126.0.6478.17 (beta), and 125.0.6422.76 (stable) on Linux x64.

Closing as Wont Fix (not reproducible), but feel free to reopen or refile if additional information becomes available.

### ch...@gmail.com (2024-05-24)

I am still able to repro this on Canary 127.0.6498.3 on Windows. 

### bo...@google.com (2024-05-24)

A helpful colleague was able to repro on Windows.

### bo...@google.com (2024-05-24)

Assigning S2 because it doesn't seem like the attacker as arbitrary control over the contents of the Omnibox. If that's an incorrect assessment, please let us know. Also, users must perform multi-step precise actions to trigger the spoof, so S2 seems quite reasonable.

### dp...@chromium.org (2024-05-24)

Unassigning from myself for now, until omnibox specific OWNERS have a chance to audit this bug.

### bo...@google.com (2024-05-24)

Routing to Omnibox folks to ensure ownership. Please feel free to reroute as needed.

### pe...@google.com (2024-05-25)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-05-25)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-06-08)

jdonnelly: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-06-23)

jdonnelly: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-07-10)

Bumping the priority of this issue since it will affect an upcoming release.

### ch...@gmail.com (2024-07-16)

This seems like fixed on Canary.

### am...@chromium.org (2024-07-16)

I'm going to go ahead and close this as fixed.
jdonnelly@ can you identify any work that would have been done here.
Since there was no action here, I'm operating on the premise that this is a duplicate or was resolved based on ongoing work. It would be helpful to verify that and merge issues appropriately.
Thank you!

### pe...@google.com (2024-07-17)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2024-07-17)

This was resolved outside of this report. We're looking to identify the CL or other report that resulted in resolution of this issue.
No merge needed here.

### sp...@google.com (2024-07-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI spoof with precondition of many navigations


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-25)

Congratulations, Khalil! Thank you for reporting this issue to us.

### pe...@google.com (2024-10-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### al...@alesandroortiz.com (2024-10-25)

Out of curiosity, did bisect on this.

Was introduced on May 20th by <https://crrev.com/f9be2df3f4a4fb9b1b98d3e479f9646f0848ce98>.

Was reverted on May 27th in response to non-security regression ([issue 342967842](https://issues.chromium.org/issues/342967842)): <https://crrev.com/458d51e98be96c3540e371bd7f41a726b74c2d9d>

The original CL was relanded on May 30th without the Read Anything (aka reading mode) changes, to avoid the regression (and also avoid the security issue reported here): <https://crrev.com/63bbdea262b93b652f2aa11617931eec9352b45f>

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/342456975)*
