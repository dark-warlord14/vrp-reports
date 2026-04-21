# Security: Security UI Spoofing on Chrome for Android due to the tabstrip hiding the fullscreen notification 

| Field | Value |
|-------|-------|
| **Issue ID** | [40946724](https://issues.chromium.org/issues/40946724) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>FullScreen, UI>Browser>Mobile>TabStrip |
| **Platforms** | Android |
| **Reporter** | ch...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2023-11-29 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 121.0.6150.0  

Operating System: Android Pixel 7 Pro

**REPRODUCTION CASE**

1. Create a group containing two tabs
2. Open PoC.html in one tab and tap anywhere on the page
3. tap on tab overview button then back to the page

## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 440.1 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.0 KB)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 432.2 KB)
- [screen-20251212-050630.mp4](attachments/screen-20251212-050630.mp4) (video/mp4, 8.5 MB)
- [Fri Jan 09 2026 11:22:38 GMT-0800 (Pacific Standard Time).png](attachments/Fri Jan 09 2026 11_22_38 GMT-0800 (Pacific Standard Time).png) (image/png, 351.3 KB)

## Timeline

### ch...@gmail.com (2023-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-29)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-11-29)

I was able to repro this on M119. Setting to Medium severity based on other fullscreen notification bugs.
Assigning to takumif@ for now. Please re-route as appropriate. Thanks!

[Monorail components: UI>Browser>FullScreen UI>Browser>Mobile>TabStrip]

### [Deleted User] (2023-11-29)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-30)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2023-12-04)

Another way to repro this bug.

### an...@chromium.org (2023-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-05)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-12-12)

Any update on this bug? 

Thanks!

### [Deleted User] (2023-12-13)

takumif: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-25)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-04)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ch...@gmail.com (2024-01-30)

Any update here? thanks!

### is...@google.com (2024-01-30)

This issue was migrated from crbug.com/chromium/1506081?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>FullScreen, UI>Browser>Mobile>TabStrip]
[Monorail components added to Component Tags custom field.]

### ch...@gmail.com (2024-02-14)

Any update on this bug? thanks.

### ch...@gmail.com (2024-03-01)

Friendly ping

### pg...@google.com (2024-10-08)

[secondary shepherd]  

A group of fullscreen related issues have been ensted under [issue 325849018](https://issues.chromium.org/issues/325849018), which is in turn blocked by [issue 314694019](https://issues.chromium.org/issues/314694019).

[takumif@chromium.org](mailto:takumif@chromium.org) - could you provide a quick update to one of these bugs on what the plan or timeline for tackling these might be?

### ta...@chromium.org (2024-10-09)

Differentiated trust for fullscreen is currently being actively worked on, and Muyao is now leading that effort.

### pg...@google.com (2024-10-18)

Hi muyaoxu@, could you explain why you updated the severity? the severity was set as S2 per the [severity guidelines](https://chromium.googlesource.com/chromium/src/+/lkgr/docs/security/severity-guidelines.md) and is used by automation and future prioritization. It is not normally a field that should be updated by non-security folks, but we do appreciate additional info to re-assess!

### mu...@google.com (2024-10-22)

I was bulk-editing multiple fullscreen toast related bugs to S3 and P2.

Fullscreen toast isn't the only cue for informing users that they are entering fullscreen. Also, the fullscreen API requires user gestures before allowing the site to enter fullscreen. As a result, I think the current priority and severity make more sense to me.

### pg...@google.com (2024-10-22)

Got it! I do think often fullscreen bugs end up on the border of S2 and S3, and for this bug, I agree that there is a case for marking it as severity=Low - thanks for the additional context.

For the future, we generally appreciate having a discussion and having security folks set the severity instead, as other teams may use the severity field in different ways than how security uses it, and many of our automation, backmerging, etc can depend on the severity field in ways that isnt apparent.

### mu...@google.com (2024-10-22)

That's fair. I didn't know that the severity is used for other purposes.

### ch...@gmail.com (2025-12-12)

Verified in Canary. Fixed 

### ct...@chromium.org (2026-01-07)

Re: [Comment #24](https://issues.chromium.org/issues/40946724#comment24)

> Fullscreen toast isn't the only cue for informing users that they are entering fullscreen. Also, the fullscreen API requires user gestures before allowing the site to enter fullscreen. As a result, I think the current priority and severity make more sense to me.

What are the other cues that show on Android? The original video does not show any visible cues that I could see. (A single user gesture is not really a security mitigation here for UI spoofing.)

### mu...@google.com (2026-01-09)

I was referring to the duplicate status bar at the top of the viewport and the UI transition into fullscreen mode. That said, I agree these are subtle indicators that users might easily overlook.

### sp...@google.com (2026-01-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
UI spoofing requiring complex prerequisites and multiple gestures


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-03-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> UI spoofing requiring complex prerequisites and multiple gestures

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40946724)*
