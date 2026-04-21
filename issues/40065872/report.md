# Security: Autofill Exploit Using Custom CSS Cursor

| Field | Value |
|-------|-------|
| **Issue ID** | [40065872](https://issues.chromium.org/issues/40065872) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | br...@google.com |
| **Created** | 2023-06-15 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Using the proof of concept below , an attacker could create an engaging website, for example, for verification purposes or other methods, to lure the victim into unknowingly providing sensitive autofill data like address or credit card information of the victim.

Here, the autofill selection is obscured by the custom CSS cursor, and the victim is lured into pressing keys (Arrow down and Enter), which are used to capture sensitive autofill data. Additionally, a popup window is used to force the autofill to fit within a small view, effectively hiding the autofill selection menu.

**VERSION**  

Chrome Version: 116.0.5817.0 (Official Build) dev (64-bit) (cohort: Dev)

**REPRODUCTION CASE**

1. Download the attached files to a folder
2. Start a Python server on the same folder by running the command `python -m http.server 8080` (this is important).
3. Open the Chrome browser and navigate to the server at `http://{YOUR-SERVER-IP}:8080/poc.html` to Begin testing.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.4 KB)
- [popup.html](attachments/popup.html) (text/plain, 4.0 KB)
- [step-1.png](attachments/step-1.png) (image/png, 2.9 KB)
- [step-2.png](attachments/step-2.png) (image/png, 2.6 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 659.9 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 1.4 MB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 1.5 MB)

## Timeline

### [Deleted User] (2023-06-15)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-06-15)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-06-15)

[Comment Deleted]

### dc...@chromium.org (2023-06-16)

The repro case is a bit flaky for me on Mac; it seems like the fields don't always get focused when I click. However, I am able to get the fields focused.

But at least on Mac, I also notice that if I use the keyboard to select autofill entries, it hides the custom cursor and it's very obvious there's an autofill menu. I tried to test this on Windows as well, but my current Windows machine is in the cloud, and custom cursor bugs don't reproduce over remote desktop connections :(

Are you testing this on ChromeOS?


[Monorail components: UI>Browser>Autofill]

### fa...@gmail.com (2023-06-16)

I have only tested this on Windows.

### [Deleted User] (2023-06-16)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@gmail.com (2023-06-16)

> The repro case is a bit flaky for me on Mac; it seems like the fields don't always get focused when I click. However, I am able to get the fields focused.

> But at least on Mac, I also notice that if I use the keyboard to select autofill entries, it hides the custom cursor and it's very obvious there's an autofill menu.

Okay, can you share the code modified for Mac? Maybe I could try to work with that and properly align it with the cursor. Thanks!

### xi...@chromium.org (2023-06-20)

Thanks for the report. I can't reproduce the exact spoof case, but I get the idea that the cursor can hide info being filled into a form and the info is sent without user awareness. This is pretty similar to https://crbug.com/1385714. The difference is that this is spoofing autofill menu while the other bug is spoofing permission prompt. The fix on the other bug is to disable custom cursor while a permissions prompt is open.Maybe we can apply the same restriction when an autofill menu is shown?

+battre@ and other autofill owners to take a look. Setting severity as low (same severity as https://crbug.com/1385714).

### [Deleted User] (2023-06-20)

[Empty comment from Monorail migration]

### ba...@chromium.org (2023-06-21)

Chris, could you please take a look?

### [Deleted User] (2023-06-21)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@gmail.com (2023-06-22)

This is what happens behind the scenes.

### fa...@gmail.com (2023-06-24)

[Comment Deleted]

### fa...@gmail.com (2023-06-24)

[Comment Deleted]

### fa...@gmail.com (2023-06-24)

Thanks for reviewing this issue. I feel like the security severity is underrated. This is more convincing and similar to crbug.com/1290664 (medium) reported by Alessandro Ortiz. Could you look into it and set a higher severity rating if possible?

I look forward to your response. Have a nice day :)

### sc...@google.com (2023-06-26)

The PoC doesn't work reliably for me either, but the key point seems to be that the custom cursor can overlay with the Autofill popup. The cursor in the video from https://crbug.com/chromium/1455133#c2 hides large parts of the Autofill popup.

This seems to be the same in https://crbug.com/chromium/1434330. My view for potential fixes is in 1434330#c22.

I'm not sure why the PoC uses a popup window.

Bruno, could you take a look?

### fa...@gmail.com (2023-06-26)

I used a popup so that the user can focus on the window without the chance of moving the cursor away. The small popup can also hide if the victim has multiple autofill data, which it couldn't properly hide without it due to the maximum cursor size. However, it seems that this only works for me, haha :)

>This seems to be the same in https://crbug.com/chromium/1434330. My view for potential fixes is in 1434330#c22.

Is the issue discussed at 1434330 using the same method of CSS cursor images to hide? I hope my issue is not a duplicate. :(

### es...@chromium.org (2023-07-14)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-07-29)

[Comment Deleted]

### fa...@gmail.com (2023-07-29)

[Comment Deleted]

### br...@google.com (2023-08-03)

Hey Chris, sorry for the delay here. I think this case is different from 1434330#c22 because a new window can have an arbitrary size, so it can always completely cover the popup.

@fazim I am not completely familiar with all the other bugs so I have to check that, I will update this soon.



### fa...@gmail.com (2023-10-29)

Friendly ping

### br...@google.com (2023-10-30)

Hi Fazim thanks for the ping.

We recently started disallowing custom cursor when the autofill popup is open. Can you please try to reproduce this again? Thanks

### fa...@gmail.com (2023-10-30)

Hi. I tried again on the latest Chrome version, and the custom cursor is disabled when the autofill popup is opened. Also, here's a video. Nicely fixed!

### br...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-10-30)

[Comment Deleted]

### fa...@gmail.com (2023-10-30)

[Comment Deleted]

### br...@google.com (2023-10-30)

Hi Fazim.

The bug was fixed by another engineer due to another bug created. However I talked to @schwering@google.com and the procedure is indeed to mark it as fixed, with a reference to the bug that landed the CLs that fixed the problem: https://bugs.chromium.org/p/chromium/issues/detail?id=1472404

I believe now the security team will analyse it and decide on a reward. I will also reach out to them and keep you updated on this bug.

Thank you

### [Deleted User] (2023-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-30)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-02)

Congratulations Shaheen! The Chrome VRP panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@chromium.org (2023-11-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-11-02)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-11-02)

[Comment Deleted]

### fa...@gmail.com (2023-11-02)

[Comment Deleted]

### am...@chromium.org (2023-11-02)

Hi Shaheen, thanks for your question. The reporter of https://crbug.com/chromium/1472404 was awarded $3,000 because they also received a bisect bonus. When I just now updated the release notes so that you got credit and associated with that CVE, I forgot to update the reward amount. 
I will make a note to update the reward amount in the release notes to $2,000 to reflect your actual reward amount. 

Reward amounts are decided based on the security implications and impact and exploitability of the bug and report quality. 
The impact of this issue, combined with reproducibility and preciseness of placement and preconditions of convincing a user to engage in a specific manner displayed in this report is more closely aligned with https://crbug.com/chromium/1385714 which received a similar reward amount. 

### fa...@gmail.com (2023-11-02)

Okay, thanks for the bounty again! :)

### am...@google.com (2023-11-03)

[Empty comment from Monorail migration]

### fa...@gmail.com (2024-01-24)

deleted

### is...@google.com (2024-01-24)

This issue was migrated from crbug.com/chromium/1455133?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1463276, crbug.com/chromium/1472404]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065872)*
