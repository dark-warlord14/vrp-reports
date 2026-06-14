# Security: no user interaction: URL spoofing using blob + @ (iOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40052466](https://issues.chromium.org/issues/40052466) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2020-06-02 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36

Steps to reproduce the problem:
1. Go to poc1.html
2. auto redirect to Spoofed URL (hence, no user interaction)

What is the expected behavior?
About:blank#Blocked (cloning the behavior of Android + Windows)

What went wrong?
blob:accounts.google.com

Did this work before? N/A 

Chrome version: 83.0.4103.61  Channel: stable
OS Version: 10.0
Flash Version: 

>Not reproducible in Android

## Attachments

- [Blob.jpeg](attachments/Blob.jpeg) (image/jpeg, 18.1 KB)
- [poc1.html](attachments/poc1.html) (text/plain, 260 B)

## Timeline

### mb...@chromium.org (2020-06-04)

stkhapugin: Would you mind taking a look at this? It doesn't reproduce on other platforms, and looks at least similar to https://crbug.com/chromium/1069246.

I'm tentatively setting medium severity here, but I'll defer to folks more familiar with URL formatting if they'd like to change it.

[Monorail components: UI>Browser>Omnibox UI>Security>UrlFormatting]

### [Deleted User] (2020-06-05)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-16)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-17)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-18)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-19)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-20)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-21)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-22)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-23)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 21 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-24)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 22 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-25)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 23 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-26)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 24 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-28)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 26 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-29)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 27 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-30)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-01)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-02)

stkhapugin: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@chromium.org (2020-07-03)

I don't think this is about URL formatting, instead the navigation should be blocked, right? 

[Monorail components: UI>Browser>Navigation]

### ra...@gmail.com (2020-07-03)

Yes, Cloning the behavior of Android. Omnibox should read about:blank#blocked. 

### [Deleted User] (2020-07-03)

gambard: Uh oh! This issue still open and hasn't been updated in the last 31 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-04)

gambard: Uh oh! This issue still open and hasn't been updated in the last 32 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-05)

gambard: Uh oh! This issue still open and hasn't been updated in the last 33 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ga...@chromium.org (2020-07-06)

I can reproduce on Chrome on mac.
Also, I am not sure to understand what should be blocked here. The "Blob:" is correctly shown.

Assigning to security people for guidance.

### ga...@chromium.org (2020-07-06)

[Empty comment from Monorail migration]

### ga...@chromium.org (2020-07-06)

disregard #25 about mac, the URL is indeed about:blank#blocked.

### mb...@chromium.org (2020-07-06)

Removing myself to get this back in the security queue. 

### ra...@gmail.com (2020-07-16)

Any update on this? Stkhpugin@

### st...@chromium.org (2020-07-16)

[Empty comment from Monorail migration]

### aj...@google.com (2020-07-23)

Assigning an owner. Please suggest someone to work on this security issue.

### aj...@google.com (2020-07-23)

[Empty comment from Monorail migration]

### st...@chromium.org (2020-07-24)

Again, this is not about incorrect URL display, the displayed URL correctly reflects the model state and is well formatted. 

Is the URL wrong? I don't know. 

[Monorail components: -UI>Browser>Omnibox -UI>Security>UrlFormatting]

### ga...@chromium.org (2020-07-24)

estark@: what should be the behaviour here?
Is it blocking load if the page is trying to load blob:https://something?
Is that a security issue?

### cr...@chromium.org (2020-07-24)

This is a legitimate medium severity bug.  I think it's the iOS equivalent of https://crbug.com/chromium/646278, given how the fix in r420436 works (and the description in https://crbug.com/646278#c5).

Here's what happens on desktop.  The attack puts together a blob URL like "blob:http://csreis.github.io/94b18894-6061-427a-bce0-c56a584acc30" (if you run it from http://csreis.github.io).  That commits without a problem.  Then the replaceState call tries to commit something like "blob:http://accounts.google.com                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       @csreis.github.io/" (with lots of spaces).

FilterURL looks at that URL, where ChildProcessSecurityPolicyImpl::CanRequestURL sees that it's valid but that IsMalformedBlobURL returns true.  That causes it to fail FilterURL and get rewritten to about:blank#blocked. 

Can Chrome for iOS add a similar check as IsMalformedBlobURL to committed URLs?  Does it already have something similar to FilterURL for that purpose?

### ga...@chromium.org (2020-07-27)

After checking, the bug is coming from the replaceState allowing the URL to be replaced. This is not something we control as it is done by WebKit.
A bug to WebKit should probably be filed.
Ali: could you confirm?

### aj...@chromium.org (2020-07-27)

That's correct, we don't get a navigation policy callback for the replaceState call, so we can't block it. I've filed https://bugs.webkit.org/show_bug.cgi?id=214846.

One way this attack is mitigated in Safari is that the URL bar displays the origin of the blob URL rather than the full URL (so, e.g., when serving from localhost, it shows "localhost", not blob://https://acounts.google.com...."). The full URL is only shown after tapping on the URL bar. Should we display the URL this way as well? We already do this for non-blob URLs.

### cr...@chromium.org (2020-07-27)

Oh, is the URL eliding logic on Chrome for iOS different from Android and Desktop for full URLs?  If we only show the origin already in the elided state already, then it does seem like that should apply to blob: and filesystem: URLs as well as normal URLs.

### cr...@chromium.org (2020-07-27)

And is that what just happened in stkhapugin@'s r791841 in https://crbug.com/chromium/1080395?

Do filesystem: URLs exist on iOS, BTW?  I think those were Chrome-specific but I'm not sure if Chrome for iOS supports them.  If they are supported, you might check to see if a similar fix is needed for them.

### aj...@chromium.org (2020-07-28)

Thanks for the pointer to r791841! I verified that for the test case in this bug, we now only display the origin in the omnibox, even after tapping on the omnibox. 

filesystem: URLs aren't supported by WebKit.

### [Deleted User] (2020-07-28)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-03)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M85. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-03)

This bug requires manual review: Less than 18 days to go before AppStore submit on M85
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-08-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-05)

Congratulations, the VRP panel decided to award $1000 for this report.

### ad...@google.com (2020-08-06)

[Empty comment from Monorail migration]

### bi...@google.com (2020-08-13)

stkhapugin@ M85 Release cut is this week. Kindly update details requested on c44. 

### bi...@google.com (2020-08-13)

[Empty comment from Monorail migration]

### bi...@google.com (2020-08-13)

Based on discussion with  adetaylor@ punting to M86. 

### ra...@gmail.com (2020-10-27)

[Comment Deleted]

### [Deleted User] (2020-11-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1090352?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052466)*
