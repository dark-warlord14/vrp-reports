# Security: Chrome fullscreen without any warning and dialog no orgin for spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40090303](https://issues.chromium.org/issues/40090303) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Mac |
| **Reporter** | xi...@gmail.com |
| **Assignee** | sp...@chromium.org |
| **Created** | 2018-01-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome fullscreen without any warning ,dialog no orgin.The attacker may insert an image of a fake omnibox in its place, thus spoofing it.

**VERSION**  

Chrome 64.0.3282.119 on macOS High Sierra 10.13.3

**REPRODUCTION CASE**  

1.Access <http://xisigr.com/test/spoof/chrome/fullscreen.html>  

2.Click on the "gmail.com" button.  

3.Fullscreen without any warning ,dialog no orgin.

## Attachments

- [fullscreenpopuptest.html](attachments/fullscreenpopuptest.html) (text/plain, 933 B)

## Timeline

### el...@chromium.org (2018-01-26)

This attack doesn't seem to work in 64.0.3282.119 and later on Windows; the prompt dialog causes the full-screen mode to exit immediately.

In contrast, the spoof seems to work perfectly on Mac.



### av...@chromium.org (2018-01-26)

What is the behavior that you see?

On my Mac, in 65.0.3315.3 I see:
1. The page goes fullscreen
2. The page loads a gmail spoof image
3. The page shows a dialog, kicking it out of fullscreen
4. The page is shown non-fullscreen but with a dialog attached.

On my Mac I cannot repro a failure to exit fullscreen.

### el...@chromium.org (2018-01-26)

Re #2: I'm not kicked out of full-screen by the prompt on Mac. I tried changing chrome://flags#secondary-ui-md but that didn't make a difference.

[Monorail components: UI>Browser>FullScreen]

### av...@chromium.org (2018-01-26)

What Mac OS are you using? I'm on 10.11 and things work.

### el...@chromium.org (2018-01-26)

10.13.2 (17C205) on a 2015 MacBook Pro.

### me...@chromium.org (2018-01-26)

I'm seeing the same behavior as elawrence on a 2012 Macbook Pro with 66.0.3331.0.

avi: I hope you don't mind me assigning this to you so that it has an owner.

### av...@chromium.org (2018-01-26)

What is your OS version?

### me...@chromium.org (2018-01-26)

Same as Eric, High Sierra (10.13.2)

### ra...@chromium.org (2018-01-30)

I can also repro, albeit on High Sierra with M63. It's fairly nasty as the escape key doesn't seem to exit fullscreen. 

### sh...@chromium.org (2018-01-31)

[Empty comment from Monorail migration]

### av...@chromium.org (2018-02-07)

Sarah, has fullscreen changed in 10.13? Popups kick pages out of fullscreen in 10.11.

### sp...@chromium.org (2018-02-07)

Yes, it looks like the fullscreen transition process has changed on 10.13. This broke some stuff recently. I can take over this issue and have a look

### av...@chromium.org (2018-02-07)

That would be awesome. I'll stick around; if there are any issues related to dialogs that you need a hand with, poke me.

### av...@chromium.org (2018-02-07)

Attaching a file to easily go into fullscreen and trigger popups.

### sp...@chromium.org (2018-02-07)

Thanks! I suspect this is an async issue. I was the one who fixed this on 10.12 and earlier, so I have a good idea on where to look.

### bu...@chromium.org (2018-02-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a390da5e987c936ca7785d948c635ea67da02552

commit a390da5e987c936ca7785d948c635ea67da02552
Author: spqchan <spqchan@chromium.org>
Date: Thu Feb 08 20:55:42 2018

[Mac] Fix Fullscreen Spoofing Issue on 10.13

On 10.13, -didEnteredFullscreen: is called before the
fullscreen transition actually gets finished. As a result,
AppKit ignores -toggleFullscreen: inside that runloop and will
print "not in a fullscreen state". To fix this issue, call
-toggleFullscreen: asynchronously.

Bug: 806162
Change-Id: If0d3559c68bfb38ba70da86894f1231f976ee403
Reviewed-on: https://chromium-review.googlesource.com/909080
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Sarah Chan <spqchan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#535506}
[modify] https://crrev.com/a390da5e987c936ca7785d948c635ea67da02552/chrome/browser/ui/cocoa/browser_window_controller.mm
[modify] https://crrev.com/a390da5e987c936ca7785d948c635ea67da02552/chrome/browser/ui/cocoa/browser_window_controller_private.h
[modify] https://crrev.com/a390da5e987c936ca7785d948c635ea67da02552/chrome/browser/ui/cocoa/browser_window_controller_private.mm


### sh...@chromium.org (2018-02-22)

spqchan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sp...@chromium.org (2018-02-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-24)

[Empty comment from Monorail migration]

### aw...@google.com (2018-02-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-07)

Congrats! the Chrome VRP panel decided to award $1,000 for this report. Cheers!

### aw...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-03-19)

Since this landed before March 1st, no merge needed for 66. 

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sd...@chromium.org (2018-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/806162?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/640466]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090303)*
