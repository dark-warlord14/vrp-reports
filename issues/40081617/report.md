# Popups can be moved below the taskbar in windows

| Field | Value |
|-------|-------|
| **Issue ID** | [40081617](https://issues.chromium.org/issues/40081617) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Aura |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | dy...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2015-03-14 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36

Steps to reproduce the problem:
1. Create a popup window
2. Move it to 0,window.screen.availHeight + 10

What is the expected behavior?
The popup window to be constrained above the taskbar

What went wrong?
The popup window goes below the taskbar, rendering it invisible. This is exploitable for playing music or running other various tasks in the background even after the tab has been closed without user consent. I can imagine this would be usable for advertisers or gathering false impressions on advertisements.

Did this work before? No 

Chrome version: 41.0.2272.89  Channel: stable
OS Version: 6.3
Flash Version: Shockwave Flash 17.0 r0

## Attachments

- [PoC.html](attachments/PoC.html) (text/html, 313 B)
- [Screen Shot 2015-05-20 at 3.49.07 PM.png](attachments/Screen Shot 2015-05-20 at 3.49.07 PM.png) (image/png, 22.0 KB)

## Timeline

### js...@chromium.org (2015-03-15)

I can't get this to work on Windows 8.1. It always shows up in the corner, with the window's full menu bar above the start bar. Have you tried it on more than one system, or on different OSes?

### dy...@gmail.com (2015-03-15)

Yes, I've tried it on 3 different machines running windows 8 or 8.1

### wf...@chromium.org (2015-03-16)

I can repro this on Windows 8.1 on both Stable and Canary, and the Window sits below the task bar.

### me...@chromium.org (2015-03-16)

I can repro on Linux too. The window isn't visible at all but there is a new process in the task manager.

### cl...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### ke...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2015-05-20)

FWIW, on Mac OS X the window is clamped to a certain minimum size, and is not allowed to completely hide off the screen — the Mac OS X window title bar is always present. However, by tweaking the PoC, I was able to sort of get close (see screenshot). I'm going to say "close enough".

Can anyone take this on? Basically, we need to clamp the allowable values for the arguments to window.moveTo.

### pi...@chromium.org (2015-05-21)

Is this a blink issue or a OS-platform issue?

### pa...@chromium.org (2015-05-21)

I feel it is fundamentally a platform issue — the platform should not let applications do Bad Things such as hide windows. More platforms should be like Mac OS X, and OS X should arguably do more to ensure that running windows are visible and usable.

But, given that we can't control what the various platform vendors do, we can at least mitigate the problem in Blink/Chrome by ensuring that we never ask the platform to hide a window.

### pi...@chromium.org (2015-05-21)

Sorry, by "platform" i mean front-end-specific OS code, as opposed to having renderers/Blink/JS enforce the policies. 

### st...@chromium.org (2015-05-21)

[Empty comment from Monorail migration]

### cp...@chromium.org (2015-06-05)

reassign to Mr. J for distribution or wontfixing


### ha...@chromium.org (2015-10-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-12-01)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-01-22)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

[Monorail components: -Security>UX]

### ra...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

[Monorail components: -Security>UX]

### aa...@google.com (2017-05-25)

[Empty comment from Monorail migration]

### ag...@chromium.org (2017-10-02)

This is reportedly used by cryptomining Javascript: crbug.com/770414

### js...@chromium.org (2017-10-02)

Sounds like it dovetails into the visibility work that the too-many-tabs team is doing.

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### pa...@chromium.org (2018-02-14)

Friendly ping. This annoyance is pretty old by now, and things like #19 should concern us.

### dy...@gmail.com (2018-02-14)

Question: 
So I know it's been a few years since this was reported, but given this has been actively exploited in the wild, appears to have real implications + value to attackers, and was not disclosed to any third parties by me personally, will this be eligible for a VRP submission?

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-20)

This issue has been Available for over a year. If it's no longer important or seems unlikely to be fixed, please consider closing it out. If it is important, please re-triage the issue.

Sorry for the inconvenience if the bug really should have been left as Available.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2019-02-26)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript]

### ke...@chromium.org (2019-10-11)

This no longer repros for me on Linux, Windows or Mac. The window appears near the bottom left of the screen.

Closing it out.

### sh...@chromium.org (2019-10-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-14)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-23)

Congrats! The Panel decided to award $500 for this report :) 

### na...@google.com (2019-10-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-01-18)

This issue was migrated from crbug.com/chromium/467329?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081617)*
