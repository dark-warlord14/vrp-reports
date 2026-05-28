# Security: UaF in Mirroring

| Field | Value |
|-------|-------|
| **Issue ID** | [40067406](https://issues.chromium.org/issues/40067406) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Cast>Streaming |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | av...@gmail.com |
| **Assignee** | bz...@google.com |
| **Created** | 2023-07-14 |
| **Bounty** | $3,000.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

A UaF in Mirroring is caused by the <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/cast_mirroring_service_host.cc;drc=254a229f4653742ec8a64b8749e2b2645fa5ef08;l=616>  

CastMirroringServiceHost

A raw ptr is held in a delayed io thread task. The callback is also called with a raw ptr (miracle pointer protected). Start a web server using npx serve. Make sure there is a chromecast nearby.

1. Wait for a prompt within the page itself to popup.
2. Click the prompt, which will open a real browser window.
3. CLick the browser window’s blank space, to show a cast screen, where you could select the cast sink. After selecting the cast sink, select the white space again, and press the pause button when the website says so.

**VERSION**  

Chrome Version: 114.0.5735.0 (Developer Build) (64-bit)  

Operating System:  

Distributor ID: Ubuntu  

Description: Ubuntu Mantic Minotaur (development branch)  

Release: 23.10  

Codename: mantic

**REPRODUCTION CASE**  

Start a web server using npx serve -l 5000 in the poc directory when extracted.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]** browser  

Crash State: Asan Logs are in the attachments below.  

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Avadhut Mahamuni

## Attachments

- deleted (application/octet-stream, 0 B)
- [asansymbolized.log](attachments/asansymbolized.log) (text/plain, 59.1 KB)
- [2023-07-09 22-02-53.mkv](attachments/2023-07-09 22-02-53.mkv) (application/octet-stream, 2.5 MB)
- [poc2.zip](attachments/poc2.zip) (application/octet-stream, 179.8 KB)
- [poc4.zip](attachments/poc4.zip) (application/octet-stream, 179.1 KB)

## Timeline

### [Deleted User] (2023-07-14)

[Empty comment from Monorail migration]

### av...@gmail.com (2023-07-14)

Video attachment below

### av...@gmail.com (2023-07-14)

I would like to keep this bug private.

### av...@gmail.com (2023-07-14)

updated poc 

### av...@gmail.com (2023-07-14)

You must enable the flag #allow-all-sites-to-initiate-mirroring

### bo...@chromium.org (2023-07-14)

In the absence of mitigating factors, this report would initially appear be Critical severity since it demonstrate memory corruption in the browser process from an uncompromised renderer, but in the ASan log we can see MiraclePtr indicates this bug is protected from exploitation. Thus we downgrade severity by one level per our severity guidelines [0].

Further, we downgrade severity once again because triggering this bug requires users to successfully perform a detailed sequence of specific UI interactions, thereby reducing the bug's practical value to attackers. Hence we land on Medium severity. 

Finally, setting Security_Impact-None because a non-standard flag is required per https://crbug.com/chromium/1464794#c5. [1][2] 

[0] https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#toc-miracleptr
[1] https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#toc-no-impact
[2] source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/media/router/media_router_feature.cc;l=56-58;drc=5578b78366de32caf83044e5ea2268e6d91af766

[Monorail components: Internals>Cast>Streaming]

### av...@gmail.com (2023-07-14)

The bug was introduced in this commit, after the delay was added, and affected stable v114 https://source.chromium.org/chromium/chromium/src/+/af0580f02ae2f1de08ec8557edd9f467d9a2bcb6. 

If there was no delay, the sequenced task runner would process the render frame host destruction after pausing the video capture host. Since the delay was introduced, the render frame host destruction was processed before the usage of video capture host(now destroyed).

### av...@gmail.com (2023-07-14)

It also doesn't seem to be triggerable on builds with dcheck enabled. This would be because the weak ptr of the selfowned receiver was bound on the UI Thread, however the destruction of video capture host was on the IO thread, invalidating the weak ptr on a different thread than the thread the weakptr was bound to. This would crash before the actual UaF occurs. This UaF won't trigger on debug builds. Also, on the previous PoC, there was a out of memory renderer crash. Here is an update that will fix it.

### av...@gmail.com (2023-07-19)

Has there been any updates yet?

### mf...@chromium.org (2023-07-19)

=> to the author of the suspect commit for analysis

### av...@gmail.com (2023-09-05)

bump

### gi...@appspot.gserviceaccount.com (2023-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2ba3a72250e527503d9aa4978d9dd9f065ce6a6f

commit 2ba3a72250e527503d9aa4978d9dd9f065ce6a6f
Author: Benjamin Zielinski <bzielinski@google.com>
Date: Sat Sep 09 00:35:06 2023

[FreezeCast] Fix crash when pausing

In the case where a mirroring session is paused, but then the route is
immediately ended, Chrome crashes. This is because pause is handled with
a posted task, and an object referenced in the task gets deleted when
the route ends.

This change fixes this by moving the delay to
MirroringMediaControllerHostImpl, and handling the delay using a
OneShotTimer that can be cancelled upon the route ending early.

Bug: 1464794
Change-Id: I1cbe85196120b8e5b417faff942593a57e9ec064
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4845076
Reviewed-by: Mark Foltz <mfoltz@chromium.org>
Commit-Queue: Benjamin Zielinski <bzielinski@google.com>
Cr-Commit-Position: refs/heads/main@{#1194393}

[modify] https://crrev.com/2ba3a72250e527503d9aa4978d9dd9f065ce6a6f/components/media_router/browser/mirroring_media_controller_host_impl.cc
[modify] https://crrev.com/2ba3a72250e527503d9aa4978d9dd9f065ce6a6f/chrome/browser/media/cast_mirroring_service_host.cc
[modify] https://crrev.com/2ba3a72250e527503d9aa4978d9dd9f065ce6a6f/components/media_router/browser/mirroring_media_controller_host_impl.h
[modify] https://crrev.com/2ba3a72250e527503d9aa4978d9dd9f065ce6a6f/components/media_router/browser/mirroring_media_controller_host_impl_unittest.cc


### bz...@google.com (2023-09-13)

With the latest change, this should be fixed starting in M119

### [Deleted User] (2023-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-21)

Congratulations Avadhut! The Chrome VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug + $1,000 bisect bonus. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2023-09-22)

[Empty comment from Monorail migration]

### av...@gmail.com (2023-10-23)

Do you know when this will appear on release notes?

### am...@chromium.org (2023-10-26)

Hello, thanks for your question. Since this issue is in a feature that is not launched, this fix would not be represented in release notes. 


### [Deleted User] (2023-12-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-20)

This issue was migrated from crbug.com/chromium/1464794?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067406)*
