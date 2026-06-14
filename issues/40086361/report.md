# Security: Address spoofing in Omnibox with HTTPS lock

| Field | Value |
|-------|-------|
| **Issue ID** | [40086361](https://issues.chromium.org/issues/40086361) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | Linux |
| **Reporter** | gn...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2017-01-01 |
| **Bounty** | $2,000.00 |

## Description

DESCRIPTION:  

Address spoofing in Omnibox with HTTPS lock

**VERSION**  

Chrome Version: Version 55.0.2883.87 (64-bit) stable  

Operating System: Ubuntu 16.04.1 LTS

**REPRODUCTION CASE**

Open a new tab and navigate to <https://utf7.ml/t/chrome_url_spoof_1.html.(See> the video)  

This issue is similar to <https://bugs.chromium.org/p/chromium/issues/detail?id=567445>.  

Perhaps it only works on Linux because the pop-up window doesn't remove the focus from the Omnibox.

POC:  

<https://utf7.ml/t/chrome_url_spoof_1.html>

\* This POC may not work because of different screen resolution. But a dedicated attacker could improve them given he has access to the victim's screen resolution.

## Attachments

- [vlcsnap-2017-01-01-15h15m31s376.png](attachments/vlcsnap-2017-01-01-15h15m31s376.png) (image/png, 142.4 KB)
- [video.webm](attachments/video.webm) (video/webm, 1.2 MB)
- [chrome_url_spoof_1.html](attachments/chrome_url_spoof_1.html) (text/plain, 159 B)
- [chrome_url_spoof_2.html](attachments/chrome_url_spoof_2.html) (text/plain, 87.8 KB)

## Timeline

### el...@chromium.org (2017-01-01)

Notably, the spoofed omnibox isn't the omnibox of the foreground window, but rather a background window.

[Monorail components: UI>Browser>Omnibox]

### ke...@chromium.org (2017-01-02)

palmer@: Can you take this, since you fixed a similar issue previously?

### pa...@chromium.org (2017-01-03)

I don't work on security UX anymore. Passing to that crew...

### es...@chromium.org (2017-01-10)

I think this is a pretty convincing spoof, though as https://crbug.com/chromium/677716#c1 points out, an interaction with the background window would reveal the real origin.

Have poked around a little bit and it seems that focus is somehow ending up in the omnibox of the second tab, with the cursor at the end of the URL. No idea why yet, will continue poking tomorrow. +creis in case he has any thoughts.

(Couldn't repro on Mac, btw. But the behavior on Mac is a little odd: focus ends up in the omnibox of the second tab, but with the whole URL selected.)

### cr...@chromium.org (2017-01-10)

I see the similarity with https://crbug.com/chromium/567445-- this is another case where FocusLocationBarByDefault is giving the omnibox focus when it shouldn't, thus scrolling the origin out of view and making the spoof possible.  Interesting that it affects the background tab this time, which is kind of a mitigating factor but I agree it's still a bad outcome.

Note: The repro doesn't fully work on Linux in M57.  In both 57.0.2970.0 Linux Dev and a debug build (57.0.2975.0), the background tab gets focus and is shown on top of the login popup.  Even if you put the fake login in that tab instead of a popup, the origin would become visible when you focus the password field to type in it.  (Maybe using an alert like https://crbug.com/chromium/567445 would work?)

Anyway, I did repro the bug in 55.0.2883.33.  A bisect would be useful to see when this behavior changed, and whether M56 is affected.

The actual bug itself appears to be in ShouldFocusLocationBarByDefault in browser.cc, which returns true if a tab is committing the New Tab Page (chrome://newtab).  That function doesn't check whether the tab is actually the selected tab in the window!  As a result, it's giving focus to the attacker's tab in step 2 of the attack, after it sends the opener back from chrome_url_spoof_1.html to the NTP.  estark@, would you like to update that, or should I?

I've also attached the two attack files for posterity (noting that the attack from https://crbug.com/chromium/567445 is no longer available).

[Monorail components: UI>Browser>Navigation]

### cr...@chromium.org (2017-01-11)

I've got a CL started for this.

### bu...@chromium.org (2017-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8f3a9a68b2dcdd2c54cf49a41ad34729ab576702

commit 8f3a9a68b2dcdd2c54cf49a41ad34729ab576702
Author: creis <creis@chromium.org>
Date: Thu Jan 12 20:19:26 2017

Don't focus the location bar for NTP navigations in non-selected tabs.

BUG=677716
TEST=See bug for repro steps.

Review-Url: https://codereview.chromium.org/2624373002
Cr-Commit-Position: refs/heads/master@{#443338}

[modify] https://crrev.com/8f3a9a68b2dcdd2c54cf49a41ad34729ab576702/chrome/browser/ui/browser.cc
[modify] https://crrev.com/8f3a9a68b2dcdd2c54cf49a41ad34729ab576702/chrome/browser/ui/browser_focus_uitest.cc


### cr...@chromium.org (2017-01-12)

Should be fixed in tomorrow's canary.  After that bakes for a day or so, I'll see about merging it to M-56.

Note that the change in behavior I mentioned in https://crbug.com/chromium/677716#c5 was due to r426905, which changed how focus works.  That's present in M56, and it prevents the exploit from working as written.  As noted, though, there may be a different way to set up a spoof with this bug in M56.

Either way, this fix is probably worth merging to avoid any risk of a spoof, since the focus behavior is still problematic even after r426905.

### cr...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-13)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-01-17)

Requesting merge of r443338 to M56.  This is a small, low-risk change that has baked on Canary for several days, and I've verified it on Linux Dev 57.0.2984.0.

Note that the exact spoof described in this bug doesn't work as is in M56 already (per comments 5 and 8), but I do think the bug is risky enough to make other types of spoofs possible, and we should likely merge it.

### sh...@chromium.org (2017-01-17)

This bug requires manual review: We are only 13 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), gkihumba@(cros), bustamante@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@google.com (2017-01-18)

Approved for merge into M56

### bu...@chromium.org (2017-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/27ebece83822341efae80096834c649ce6822e64

commit 27ebece83822341efae80096834c649ce6822e64
Author: Charles Reis <creis@chromium.org>
Date: Wed Jan 18 23:56:32 2017

Don't focus the location bar for NTP navigations in non-selected tabs.

BUG=677716
TEST=See bug for repro steps.

Review-Url: https://codereview.chromium.org/2624373002
Cr-Commit-Position: refs/heads/master@{#443338}
(cherry picked from commit 8f3a9a68b2dcdd2c54cf49a41ad34729ab576702)

Review-Url: https://codereview.chromium.org/2640773003 .
Cr-Commit-Position: refs/branch-heads/2924@{#796}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/27ebece83822341efae80096834c649ce6822e64/chrome/browser/ui/browser.cc
[modify] https://crrev.com/27ebece83822341efae80096834c649ce6822e64/chrome/browser/ui/browser_focus_uitest.cc


### aw...@chromium.org (2017-01-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

Congratulations! The panel decided to award $2,000 for this bug!  A member of our finance team will be in touch to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-01-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/677716?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086361)*
