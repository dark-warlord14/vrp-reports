# The name attribute length on a PWA's manifest doesn't have a limit, which allows an attacker to spoof its message and origin

| Field | Value |
|-------|-------|
| **Issue ID** | [40061287](https://issues.chromium.org/issues/40061287) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | fi...@chromium.org |
| **Created** | 2022-10-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The name attribute retrieved from a PWA's manifest is reflected on several parts of the Chrome UI, and due to the lack of restricting its maximum length, an attacker can spoof the PWA's installation dialog with an arbitrary message and even hide the origin displayed on it.

I have attached a video (repro.mkv) reproducing the attack as well as a picture (dialog.png) showing how the PWA's installation dialog is supposed to look.

**VERSION**  

Chrome Version: 105.0.5195.125 (Official Build) (64-bit)  

Operating System: Ubuntu 20.04

**REPRODUCTION CASE**

1. Download "index.html", "manifest.json", "script.js", "sw.js" and serve the files through a web server.
2. Access <http://localhost> and click on the install button located in the top-right position of the address bar.
3. A spoofed PWA's installation dialog will be shown with an attacker-controlled message and without an origin being displayed.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [script.js](attachments/script.js) (text/plain, 84 B)
- [sw.js](attachments/sw.js) (text/plain, 142 B)
- [manifest.json](attachments/manifest.json) (text/plain, 1.3 KB)
- [dialog.png](attachments/dialog.png) (image/png, 38.4 KB)
- [index.html](attachments/index.html) (text/plain, 563 B)
- [repro.mkv](attachments/repro.mkv) (application/octet-stream, 797.6 KB)
- [Screen Shot 2022-10-18 at 12.59.17 PM.png](attachments/Screen Shot 2022-10-18 at 12.59.17 PM.png) (image/png, 153.8 KB)
- [Mon Dec 02 2024 16:34:00 GMT+0000 (Greenwich Mean Time).png](attachments/Mon Dec 02 2024 16_34_00 GMT+0000 (Greenwich Mean Time).png) (image/png, 20.6 KB)

## Timeline

### [Deleted User] (2022-10-09)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-10-09)

Thanks for the report and the PoC. I have reproduced this behavior as well. 

[Monorail components: UI>Browser>WebAppInstalls]

### an...@chromium.org (2022-10-09)

CC'ing some people to take a look; please re-route if you are not the right person(s) to resolve this issue. Thank you.

### an...@chromium.org (2022-10-09)

Setting severity to medium  (A bug that allows web content to tamper with trusted browser UI).
Setting foundin to M105 (official stable build repro).

### an...@chromium.org (2022-10-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-09)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-10-09)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-10-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-10)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2022-10-11)

dmurph@: would you mind taking a look at this and re-routing as appropriate? The repro is on dPWAs, which seems like your territory.

In particular, this may be as simple as throwing the URL through ElideURL [1]

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/url_formatter/elide_url.h

### dm...@chromium.org (2022-10-18)

I'm not quite sure I understand. The dialog seems to stretch? And I can still see the origin?

See screenshot attached

### dm...@chromium.org (2022-10-18)

[Empty comment from Monorail migration]

### he...@gmail.com (2022-10-18)

https://crbug.com/chromium/1372911#c12 - I think the origin wasn't hidden because the dialog wasn't stretched enough to leave your screen (I would assume this happened because of your screen resolution). Try adding more "spaces" to the name attribute of the manifest.json file and retrying the PoC.

In a real attack, the manifest.json file would be generated and tailored to each user's screen resolution.
You can also check the repro.mkv video to see what it looks like on a 1920x1080 resolution.

### dm...@chromium.org (2022-10-20)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-11-02)

dmurph@: Security bugs should have owners. Is there anyone who is able to look at this that you can pass it to?

### [Deleted User] (2022-11-04)

dmurph: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-14)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2022-11-17)

Chatting with Penny - we think we can model Extensions and limit the short_name to 12 characters.

In the backlog now.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### dm...@chromium.org (2022-12-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-02)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-12)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-23)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-02)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### dm...@chromium.org (2023-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-20)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-30)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-08)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-19)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### dm...@chromium.org (2023-07-21)

We have this as a P2 priority work item to tackle this year - but it may be pushed to 2024. We need this for some UX refreshes, so the likelihood we get to this is pretty high.

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

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

This issue was migrated from crbug.com/chromium/1372911?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-09)

Thank you for providing more feedback. Adding the requester to the cc list.

### pe...@google.com (2024-10-26)

dmurph: Uh oh! This issue still open and hasn't been updated in the last 462 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-10)

dmurph: Uh oh! This issue still open and hasn't been updated in the last 477 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fi...@chromium.org (2024-12-02)

I'm not sure there's an issue here anymore...

This is a screenshot from ChromeOS and I tested on Windows as well. In both cases the long name is elided, as per 
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/web_apps/web_app_views_utils.cc;l=18;drc=5108636c70c0b08fdbeb57de2640a22e138f6685

### he...@gmail.com (2024-12-13)

Hey, since this is a security issue that might be eligible for a bounty via the Chrome VRP, I think it should be marked as "Fixed" instead of "Won't Fix". Looks like the bugs that originated the fix (<https://source.chromium.org/chromium/chromium/src/+/c7bbe21415591042334587fab29a528ea864de1b>) are newer ([bug 36740149](https://issues.chromium.org/issues/36740149) and [bug 383523099](https://issues.chromium.org/issues/383523099)) than this one.

Could someone from the security team take a look? Thanks!

### am...@chromium.org (2025-01-07)

It does seem likely that this issue would have been resolved more recently, such as by <https://crrev.com/c/6089150> or a related change given that this issue was still reproducible earlier this year as per a duplicate report of the same issue ([crbug/324519299](https://crbug.com/324519299)).
Closing this report as Fixed rather than WontFix since there are VRP implications as mentioned in in c#55.

### pe...@google.com (2025-01-07)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-01-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-09)

Congratulations Luan! Thank you for your initial efforts in reporting this issue to us as well as the follow up to let us know it had been resolved by a recent change. Cheers!

### ch...@google.com (2025-04-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061287)*
