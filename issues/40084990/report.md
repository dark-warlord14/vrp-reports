# Security: If two windows are in fullscreen at the same time they can navigate to different origins without fullscreen being exited automatically.

| Field | Value |
|-------|-------|
| **Issue ID** | [40084990](https://issues.chromium.org/issues/40084990) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Windows |
| **Reporter** | he...@gmail.com |
| **Assignee** | br...@chromium.org |
| **Created** | 2016-08-01 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability allows to change the page the user is browsing while in fullscreen without exiting the user from fullscreen. This allows the attacker to display arbitrary content making the user think it's from the original webpage he was navigating.

**VERSION**  

Chrome Version: 53.0.2785.34 beta-m  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Access <http://lbherrera.me/fullscreen.html>
2. Click on the "YES" button.
3. Click on the youtube URL that shows up.
4. A youtube video should be displayed in a popup. Put the video in fullscreen.
5. After a few seconds, an alert dialog will pop telling that the origin is now lbherrera.me instead of youtube.com

\*The popup that appears in the bottom of the page in step 2 can be hidden using a "popunder" script.

## Attachments

- [fullscreen-spoof.html](attachments/fullscreen-spoof.html) (text/plain, 1.2 KB)

## Timeline

### he...@gmail.com (2016-08-01)

I meant to say shift the focus between different origins, not actually navigate.

A better title would be:
If two windows are in fullscreen at the same time they can shift the focus to each other without fullscreen being exited automatically.

### ri...@chromium.org (2016-08-01)

Adding some folks from https://crbug.com/chromium/591776.

This is similar to that bug, but in the opposite direction - when fullscreen on one window is enabled, it can hide the full screen indicator on another window.

[Monorail components: Security>UX UI>Browser>FullScreen]

### sh...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-03)

I was unable to reproduce this problem on the Mac? The steps are outcomes are not very clear.

When I:

1. Click the URL
2. Click the YES button

a small window appears in the corner. Then when I 

3. Click the YouTube URL

I get the YouTube video fullscreen in its own space. After some number of seconds I am switched out of the YouTube video space back to my original space and see a modal dialog. When I click OK I am taken back to the YouTube video space. I'm not seeing how this is a security/spoofing problem on the Mac.

Sending back to Windows triage.

### he...@gmail.com (2016-08-03)

#https://crbug.com/chromium/633352#c5, I didn't test on Mac, only on Windows 7. The steps you took are correct, but the outcome is different than on Windows.

I uploaded a video showing the bug (it is marked as unlisted):
https://www.youtube.com/watch?v=kXf5VFA-6jE

### sh...@chromium.org (2016-08-03)

Thank you for posting the video. Yeah, it's a different outcome on the Mac.


### ri...@chromium.org (2016-08-03)

Oops, sorry, I had reproed on Linux, which is why I assumed it was OS-All.

### ra...@chromium.org (2016-08-04)

I can't repro on linux - I think this is a windows-specific bug. On linux when the original window goes fullscreen, the other window can't put itself on top. That seems like reasonable behavior to me. 

Assigning to jschuh for windows team triage.

Although I'm reluctant to class this as a security bug at all - a website that opens a popup can manipulate that window and even close it which is always going to open up the door to spoofing type attacks like this.

### ra...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

[Monorail components: -Security>UX]

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2018-10-03)

jschuh is not the right person for this. Enamel or Windows friends?

### aw...@google.com (2019-01-14)

(bulk edit: herrerahlb@gmail.com is the new email address for luan.herrera@hotmail.com)

### jd...@chromium.org (2019-11-21)

brucedawson: can you take a look and help us to route this as needed? We like to keep security bugs moving. Thanks!

### br...@chromium.org (2019-11-21)

I don't have any perspective on whether this is a security bug or not, and I'm traveling today and Friday so I won't be able to do anything until Monday.

### br...@chromium.org (2019-11-28)

The page at http://lbherrera.me/fullscreen.html seems to have been deleted, or at least I can't view it.

Is the behavior on OSX that full-screen mode is left when the top-level domain on the page changes? wfh@ might have some thoughts on how serious an issue this is for Windows users.


### pa...@chromium.org (2019-12-03)

luan.herrera, can you please attach the demo to this bug? Thanks!


### jd...@chromium.org (2019-12-23)

luan.herrera: gentle ping re: comments 17 and 18.

### he...@gmail.com (2020-01-07)

Sorry for the delay, I was traveling on vacation this last month and didn't have access to my computer.
Here is the PoC (https://lbherrera.github.io/lab/chrome-5ce89d53/index.html) for this bug (which isn't working anymore due to it already having been fixed).

I also tracked when the root cause (#c1) for this bug was fixed and found out https://bugs.chromium.org/p/chromium/issues/detail?id=800056

### me...@chromium.org (2020-01-07)

Thanks Luan! I did a bisect and can confirm that crrev.com/c/852378 fixed this. The bug for that fix (https://crbug.com/chromium/800056) was branched off of https://crbug.com/chromium/776418 which sounds similar to this one. This bug is a year older though.

VRP folks, please take a look and see if https://crbug.com/chromium/776418 is a duplicate of this one.

### me...@chromium.org (2020-01-07)

Attaching the PoC.

### sh...@chromium.org (2020-01-08)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-23)

Unfortunately the Panel declined to reward this report

### he...@gmail.com (2020-01-23)

Hi, could I get a clarification from the panel on why it was declined?
Was the root cause of both bugs deemed different? I feel like they are the same, but on that occasion, the panel decided to reward https://crbug.com/chromium/776418 - even though my report came one year earlier.

Thanks!

### pa...@chromium.org (2020-02-05)

I will raise this at the next panel meeting for reconsideration. Do you have more insight as to how this would be exploitable?

### he...@gmail.com (2020-02-06)

Yes, it would be a spoofing attack similar to the one shown in https://crbug.com/chromium/776418.

I recorded a video reproducing the attack:
https://www.youtube.com/watch?v=WPoUbNHkdqI

And here is the PoC used:
https://lbherrera.github.io/lab/chrome/spoof/index.html

### na...@google.com (2020-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-11)

Congrats! The Panel decided to award $1,000 for this report!

### na...@google.com (2020-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-15)

This issue was migrated from crbug.com/chromium/633352?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084990)*
