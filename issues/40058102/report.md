# Security: fencedframe element bypass the security policy restrictions of the devtools preview limit

| Field | Value |
|-------|-------|
| **Issue ID** | [40058102](https://issues.chromium.org/issues/40058102) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>FencedFrames, UI>Browser>Navigation>MPArch |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2021-12-02 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

fencedframe element bypass the security policy restrictions of the devtools preview limit.  

In the devtools > Network > Preview , we can not click the right button or run any javascript because of the CSP policy.  

However when the webpage contains the fencedframe elemnt, it will break the policy.You can run the javascript in the Preview page.

**VERSION**  

Chrome Version: Version 98.0.4743.0 (Developer Build) (64-bit)  

Operating System: Windows && Linux

**REPRODUCTION CASE**

1. run the webserver : node server.js PS: npm install fastify-static && fastify
2. open the chromium : chrome --user-data-dir=C:/tmp/fencedframe --enable-features=FencedFrames:implementation\_type/mparch <http://localhost:2333/poc.html>
3. open the devtools and reload the webpage
4. run the javascript or right click in the preview page

See the poc.gif

## Attachments

- [poc.gif](attachments/poc.gif) (image/gif, 1.9 MB)
- deleted (application/octet-stream, 0 B)
- [server.js](attachments/server.js) (text/plain, 521 B)
- [poc.html](attachments/poc.html) (text/plain, 287 B)
- [subframe.html](attachments/subframe.html) (text/plain, 307 B)

## Timeline

### [Deleted User] (2021-12-02)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-12-02)

Thanks for your report. Would you please attach all files directly to this bug (not using a 7zip archive)? Thanks!

### 0x...@gmail.com (2021-12-03)

put the html files into the public dirctionary.

### [Deleted User] (2021-12-03)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dt...@chromium.org (2021-12-03)

[Empty comment from Monorail migration]

[Monorail components: Blink>FencedFrames UI>Browser>Navigation>MPArch]

### jd...@chromium.org (2021-12-03)

shivanisha@ can you please take a look at this?

Are fenced frames in origin trial, or otherwise exposed to the web? I'm labeling this bug as such, but I can't tell for sure. If they're really not web-accessible, then this is Impact-None.

### [Deleted User] (2021-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-04)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-16)

shivanisha: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2021-12-16)

Fenced frames are behind a flag which is disabled by default. They are not in origin trial.

### 0x...@gmail.com (2021-12-16)

Even if it needs a disabled flag by default,I think it is also a security issue.

### sh...@chromium.org (2021-12-16)

Sure, updated the labels correctly now (hopefully)

### [Deleted User] (2022-01-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2022-01-18)

Adithya, assigning it to you as it seems related to your MPArch devtools work. If not, feel free to reassign. 

### ad...@chromium.org (2022-01-18)

The issue here is not DevTools related - it's caused due to fenced frames not respecting the sandbox flags of a parent frame. I think after https://crrev.com/c/3308619 lands, the fenced frame won't load inside the sandboxed iframe that loads the preview (because script is disallowed) and this issue should be resolved. 

### ho...@chromium.org (2022-01-24)

[Empty comment from Monorail migration]

### ho...@chromium.org (2022-02-17)

This issue is fixed by r972294.

### [Deleted User] (2022-02-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-17)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-23)

Congratulations - the VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-02-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-05-26)

This issue was migrated from crbug.com/chromium/1276002?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>FencedFrames, UI>Browser>Navigation>MPArch]
[Monorail blocked-on: crbug.com/chromium/1277405]
[Monorail blocking: crbug.com/chromium/1263574]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058102)*
