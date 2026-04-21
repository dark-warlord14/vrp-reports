# Chrome Theme contains link to malware, safe browser does not catch it

| Field | Value |
|-------|-------|
| **Issue ID** | [40062523](https://issues.chromium.org/issues/40062523) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Themes |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2023-01-05 |
| **Bounty** | $1,000.00 |

## Description

Hello, 

I found one of the security issue on the Chrome Browser wallpaper.

Detail:
When using add any of the wallpaper on Chrome it also highlights the "Wallpaper Owner/Creator name" with the credit link, I found that one of the creators with copyright "
Tessellation Extra 4
Justin Prno — Walli" bypass the security check and redirects the users to the malicious site.


When a user clicks on the creator link the link redirects to a malicious site and asks to install malicious software/extension into the system.


I am an Ethical hacker who helps businesses to find and solve security bugs on user-level, I am expecting that the Chrome team will resolve this.

Regards
Fardeen Siddiqui

## Attachments

- [Screenshot 2023-01-05 at 9.25.33 PM.png](attachments/Screenshot 2023-01-05 at 9.25.33 PM.png) (image/png, 78.9 KB)
- [Screenshot 2023-01-05 at 9.26.39 PM.png](attachments/Screenshot 2023-01-05 at 9.26.39 PM.png) (image/png, 281.4 KB)
- [Screenshot 2023-01-05 at 9.26.39 PM.png](attachments/Screenshot 2023-01-05 at 9.26.39 PM.png) (image/png, 281.4 KB)

## Timeline

### [Deleted User] (2023-01-05)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-01-05)

[Empty comment from Monorail migration]

[Monorail components: Services>Safebrowsing]

### dr...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### np...@chromium.org (2023-01-28)

Is there a particular theme that is linking to a malicious site? Can you provide a link to that theme in the https://chrome.google.com/webstore/category/themes?

If not, can you show a video or upload a repro that demonstrates how Chrome is navigating to a malicious link w/o it being checked by Safe Browsing?

### np...@chromium.org (2023-02-14)

Closing for lack of sufficient details.

### ad...@google.com (2023-04-26)

This has been re-reported with more details in https://crbug.com/chromium/1440220.

These links were removed in https://critique.corp.google.com/cl/480204162 from some cloud-pushed data. This was just based on SSL errors (as reported in https://crbug.com/chromium/1311696) but josiahk@ has reproduced these sites redirecting to malware on an iPhone, even if not on desktop, so it sounds like they are indeed harmful.

Some of these shanga links are still hard-coded in Chrome itself:
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/welcome/ntp_background_handler.cc;l=138?q=shanga

It feels to me like we therefore have to make possibly three fixes:

1) remove these hard-coded links which point to questionable sites
2) check that safe browsing blocks these
3) (possibly? Devlin?) if folks have a theme which we then change because the links were malicious, can we force-reload the theme?

nparker, WDYT? Does that sound like the right set of steps to take?

It's unclear what the actual security impact here is, but if the user can be enticed to go to a malicious site, it's possible that some harm could result, so I'm going to call this Security_Severity-Low.

### ad...@google.com (2023-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-26)

[Empty comment from Monorail migration]

### np...@chromium.org (2023-04-26)

Just to clarify I understand, the situation is this:

This built-in theme offers the following link on the NTP:
  https://walli.shanga.co/image/view/?id=370
That site either shows random ads, or redirects to malicious content (probably through a sketchy ad network). Safe Browsing hasn't been warning on those.

Ade: Yes, your actions make sense to me. I've filed http://b/279800765 w/ Safe Browsing for #2.

### np...@chromium.org (2023-04-26)

pauladedeji -- Can you find an owner for this? We should remove the shanga.co URLs from themes since they are at best broken, but sometimes redirecting to malware.

I'm not able to repro this theme showing a clickable URL, but the report says it is somewhere. My attempt on m112.0.5615.137: I click the pencil on the NTP, then go to "Change Theme," select "Geometric shapes," and then the 5th theme. That show the text "Tessellation 15 Justin Prno — Walli" on the theme but it's not clickable. Like this: https://screenshot.googleplex.com/7yhTYEWJWSSA69a



[Monorail components: UI>Browser>Themes]

### jo...@chromium.org (2023-04-27)

The clickable URLs come from if the user selected the background through the Welcome flow at chrome://welcome. The action URLs are hard-coded [1] for the Welcome flow and do not pull from the same database that the NTP pulls from. It seems the URLs were removed for NTP but not for the Welcome flow. I'll implement the fix.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/welcome/ntp_background_handler.cc;drc=9269d4ed0dde3bcd3837f75a50a2944674555186;l=138

### jo...@google.com (2023-04-27)

A second clickable link flow (how I hit it) is the same as https://crbug.com/chromium/1405223#c10, with the modification that I hadn't changed the theme in 2022, so the clickable link was still there (never updated) - wild guessing there's X000 - X0,000 other users who haven't changed their theme from one of the shape wallpapers, who will be offered the bad link every time they open new tab page (as I was until yesterday when I switched my theme, and switched it back)

### jo...@chromium.org (2023-04-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6d9afff4ed56d2af9b6808868fdbfbd74ddc3ded

commit 6d9afff4ed56d2af9b6808868fdbfbd74ddc3ded
Author: John Lee <johntlee@chromium.org>
Date: Thu Apr 27 21:28:46 2023

Welcome: Remove attribution URLs for some NTP backgrounds

Fixed: 1405223
Change-Id: Id2f321e6d6f7fc1e941f4ee76511af7ff1c608cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4484884
Commit-Queue: John Lee <johntlee@chromium.org>
Reviewed-by: Demetrios Papadopoulos <dpapad@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1136800}

[modify] https://crrev.com/6d9afff4ed56d2af9b6808868fdbfbd74ddc3ded/chrome/browser/ui/webui/welcome/ntp_background_handler.cc


### np...@chromium.org (2023-04-27)

walli.shanga[.]co/ has been added to Safe Browsing's "Social Engineering" blocklist, so users who haven't updated will be safe as well. It shows a warning.

### jo...@google.com (2023-04-28)

Thanks Adrian, Grace, John, and Nathan!!

### jo...@google.com (2023-04-28)

So, just one more minor thing (if someone was still bored) would be to add some shim code to conditionally remove the href part of the links for existing users, so that in a future milestone, they won't hit a red warning page if accidentally clicking a walli.shanga attribution link on NTP (that way we don't have to figure out how to force-push a built-in theme update)

### [Deleted User] (2023-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-12)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. In the meantime, please let us know what name/handle/tag or other identifier you would like us to use in acknowledging you for reporting this issue. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2023-05-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-04)

This issue was migrated from crbug.com/chromium/1405223?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Services>Safebrowsing, UI>Browser>Themes]
[Monorail mergedwith: crbug.com/chromium/1440220, crbug.com/chromium/1441312]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062523)*
