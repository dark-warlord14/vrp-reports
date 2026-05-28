# Security: [Esc] KeyPress Does Not Work in FullScreen While navigator.share Is Active

| Field | Value |
|-------|-------|
| **Issue ID** | [40067914](https://issues.chromium.org/issues/40067914) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebShare, UI>Browser>FullScreen |
| **Platforms** | Windows |
| **Reporter** | pu...@gmail.com |
| **Assignee** | mg...@chromium.org |
| **Created** | 2023-07-22 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

We Can Prevent [Esc] KeyPress in Full Screen Mode Using navigator.share

**VERSION**  

Chrome Version: [115.0.5790.99] + [stable]  

Operating System: [Windows 10]

**REPRODUCTION CASE**

1. Open PocIndex.html
2. Double Click [Click Me!] button
3. Done

**CREDIT INFORMATION**  

Reporter credit: Umar Farooq

## Attachments

- [PufIndex.html](attachments/PufIndex.html) (text/plain, 464 B)
- [New Poc.mp4](attachments/New Poc.mp4) (video/mp4, 373.5 KB)
- [New Reproduce.mp4](attachments/New Reproduce.mp4) (video/mp4, 381.9 KB)
- [poc.html](attachments/poc.html) (text/html, 550 B)

## Timeline

### [Deleted User] (2023-07-22)

[Empty comment from Monorail migration]

### fl...@google.com (2023-07-24)

Note this issue is very similar to 1465524, and might be a duplicate, though I'll leave that to more experienced UX folks to determine.

finnur@, would you mind assessing severity here?

[Monorail components: Blink>Fullscreen Blink>WebShare]

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### fl...@google.com (2023-07-24)

Reassigning to mgiuca@ since finnur@ is OOO for a while & mgiuca@ will be back tomorrow to triage.

### ma...@google.com (2023-07-27)

Re https://crbug.com/chromium/1467032#c2, I don't think they're quite the same issue.

1465524 was about showing a share dialog beyond a cross-origin navigation, so that it's unclear which site caused the dialog. This looks like a case where the site manages to occlude the fullscreen notification, which I think we consider to be a possible spoofing issue (see e.g. https://crbug.com/1170584). 

Going to set Severity-Medium here since this effectively allows sites to spoof trusted UI, mitigated by required user interaction.

### mg...@chromium.org (2023-07-28)

There's some overlap here with https://crbug.com/chromium/1259654 due to the same reporter reporting the same repro case and video to show two different bugs. (Pro tip: Ideally, create two separate repros and videos to show different bugs, this was a bit hard to understand what the issue was because of showing two bugs at the same time.)

Even this contains two semi-related issues:
1. The title of this bug (Esc keypress does not work while share is active).
2. The fact that the fullscreen bubble shows behind the share sheet, making it hard to see.

Note that I tested this on ChromeOS and the bubble showed in front of the share sheet. So this is Windows and possibly macOS bug only.

It is probably very hard to fix this. The share sheet is an OS window, not part of the browser. The fullscreen bubble is part of browser UI.

I think this is mitigated by the fact that you have to double-click the button. It's basically working as intended: the first click goes into full screen and consumes a user gesture. Web Share requires a user gesture which doesn't exist after going fullscreen. The second click is required to trigger a Web Share. Essentially the user is taking two distinct actions, and seeing the two results.

The fullscreen bubble is still visible, though partly obscured by the share sheet. The fact that [Esc] doesn't exit full screen is expected, because you clicked a subsequent button to trigger the share sheet.

It is possibly exploitable by creating a game where you have to rapidly punch the monkey and your many clicks create the two clicks. But I think this is kind of intrinsic to how the user gesture system works, and fullscreen / web share are just two APIs that consume gestures and are therefore exploitable.

### [Deleted User] (2023-07-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-11)

mgiuca: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-25)

mgiuca: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@chromium.org (2023-09-12)

[Empty comment from Monorail migration]

### ik...@chromium.org (2023-09-12)

-Blink>Fullscreen This doesn't appear to be related to Blink's requestFullscreen API behaviour (rather the UI).

[Monorail components: -Blink>Fullscreen UI>Browser>FullScreen]

### pu...@gmail.com (2023-09-26)

Would you kindly give me an update?


### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-24)

[Empty comment from Monorail migration]

### pu...@gmail.com (2023-11-02)

any updates?

### pu...@gmail.com (2023-11-24)

any updates?


### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1467032?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WebShare, UI>Browser>FullScreen]
[Monorail mergedwith: crbug.com/chromium/1469807]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-07)

Thank you for providing more feedback. Adding the requester to the cc list.

### pu...@gmail.com (2024-05-30)

Would you kindly give me an update?

What’s the current status of this Issue.

Thank you!

### dm...@google.com (2024-06-13)

+Hoch who (I believe) is working in this area?

### mh...@microsoft.com (2024-06-13)

Though I'm not currently doing anything in this area, I did do the Windows implementation of navigator.share, and mgiuca is correct that all these behaviors are currently expected.

Playing around with some other similar APIs like window.print and window.showDirectoryPicker I notice that they switch out of fullscreen before showing their additional dialog-like UI (though I also noticed there is a bug filed for this for showDirectoryPicker). What about adopting a similar behavior for navigator.share - intentionally exiting full screen upon invocation?

### pu...@gmail.com (2024-07-02)

Would you kindly give me an update?

What’s the current status of this Issue.

Thank you!

### dm...@google.com (2024-07-09)

> Playing around with some other similar APIs like window.print and window.showDirectoryPicker I notice that they switch out of fullscreen before showing their additional dialog-like UI (though I also noticed there is a bug filed for this for showDirectoryPicker). What about adopting a similar behavior for navigator.share - intentionally exiting full screen upon invocation?

that works for me!

### pu...@gmail.com (2024-08-06)

@mgiuca

Friendly Ping: Would you kindly give me an update?

Thanks!

### pu...@gmail.com (2024-08-06)

- New Related Bug While navigator.share Is Active [Esc] KeyPress Does Not Work In navigator.keyboard.lock in Fullscreen

attached a video reproducing the attack & Poc.

REPRODUCTION CASE

1. Load Attacked HTML File in Your Localhost or Server
2. Open PocIndex.html
3. Double Click [Click Me!] button
4. Hold [Esc] Key
5. this will not exit Fullscreen window due to navigator.share Is Active

### ap...@google.com (2024-10-18)

Project: chromium/src  

Branch: main  

Author: Hoch Hochkeppel <[mhochk@microsoft.com](mailto:mhochk@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/5938489>

Exit fullscreen on Windows for navigator.share

---


Expand for full commit details
```
Exit fullscreen on Windows for navigator.share

The 'Share' experience on Windows is designed with a windowed
experience in mind, and results in unintuitive behaviors when invoked
from a fullscreen context. To mitigate any risks from these behaviors,
and to ensure the optimal user experience, this change ensures that
fullscreen is exited prior to starting the Windows portion of the
'Share' flow.

Bug: 40067914
Change-Id: I36af174544f738965e988e8d0fb4b29349cad8c5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5938489
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Commit-Queue: Hoch Hochkeppel <mhochk@microsoft.com>
Reviewed-by: Amanda Baker <ambake@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#1370877}

```

---

Files:

- M `chrome/browser/webshare/share_service_browsertest.cc`
- M `chrome/browser/webshare/share_service_impl.cc`

---

Hash: 92bebd7aaa776384c1a62b1814ce8de1ab90ea75  

Date:  Fri Oct 18 23:07:16 2024


---

### pu...@gmail.com (2024-10-22)

Verified Testing! this vulnerability is fixed! in latest Chrome canary Version 132.0.6791.0 (Official Build) canary (64-bit)

Thank you!

### pe...@google.com (2024-10-26)

mgiuca: Uh oh! This issue still open and hasn't been updated in the last 456 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-10)

mgiuca: Uh oh! This issue still open and hasn't been updated in the last 471 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2024-11-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
with the addition of the new and more security impactful POC in c#36, $5,000 for report of moderate impact security UI spoof


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-14)

Congratulation Umar! Thank you for your work here and providing that improved POC and steps to reproduction in c#36 better demonstrating the security impact of this issue -- nice work!

### pu...@gmail.com (2024-11-14)

Thanks for the reward Really appreciate it.

### pu...@gmail.com (2024-12-23)

Any update Regarding CVE for this Vulnerability Thank you

### am...@chromium.org (2024-12-23)

CVEs are issued when the fix ships in a Stable channel update. [1]
This fix landed on 132, so it will receive a CVE when 132 Stable ships on 14 January 2025.

[1] <https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#will-i-receive-a-cve-for-my-bug>

### ph...@google.com (2025-02-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067914)*
