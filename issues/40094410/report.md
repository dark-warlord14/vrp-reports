# Security: Download dialog spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40094410](https://issues.chromium.org/issues/40094410) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads, UI>Browser>Navigation, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | rs...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2019-03-27 |
| **Bounty** | $500.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

This vector allows an attacker to spoof the download dialog on any domain, including invalid ones by the use of setting the location to an crafted invalid data url.

It is a bypass of <https://bugs.chromium.org/p/chromium/issues/detail?id=632514> and also an much easier attack vector

When a loaded tabs location is changed to a data url containing a invalid data type such as 'data:foo/bar,content of file' chrome will be default download or prompt the user to download via the origin in the tab.

An malicious user can abuse this to spoof download dialogs. This works both via a ref from window.open and from window.opener

**VERSION**  

Chrome Version: 73.0.3683.86 stable  

Operating System: Ubuntu 18.04.2 LTS

**REPRODUCTION CASE**  

I have made a POC at <http://192.210.213.209/chrome-download-spoon-silver-trust-xen-trouble-tension-lips.html>  

The source code for above is <https://gist.github.com/RonniSkansing/df7e330024ae640ed07cac346d855013>

To reproduce locally

- open a tab with any page and run the following script

var r = window.open('<https://google.com>');  

r.location.href = 'data:a/b, Content of spoofed file';  

r.location.href = 'data:a/b, Content of spoofed file';  

r.location.href = 'data:a/b, Content of spoofed file';  

r.location.href = 'data:a/b, Content of spoofed file';  

r.location.href = 'data:a/b, Content of spoofed file';  

r.focus();

- A dialog with "google.com wants to \n Download multiple files"

Reporter credit: Ronni Skansing (skansing.dk)

## Attachments

- [google-poc-blur.png](attachments/google-poc-blur.png) (image/png, 123.1 KB)
- [poc-twitter-blur.png](attachments/poc-twitter-blur.png) (image/png, 184.5 KB)
- [poc-ftp-address-blur.png](attachments/poc-ftp-address-blur.png) (image/png, 95.2 KB)

## Timeline

### dr...@chromium.org (2019-03-27)

This reproduces on M73. The wrong domain appears in the prompt. I'm guessing that this is more of a downloads/navigation issue than the UI being incorrect, so cc'ing a few Downloads and Navigation people.


[Monorail components: UI>Browser>Downloads UI>Browser>Navigation UI>Browser>Permissions>Prompts]

### na...@chromium.org (2019-03-27)

Adding meacer@, who worked on blocking data: URL navigations in top level windows. I thought navigating an opened window is a case where we block data: URLs, but if this reproes then something is not working correctly.

Also adding some more navigation folks.

### me...@chromium.org (2019-03-27)

We explicitly allow navigations that end up as downloads in data URLs: https://cs.chromium.org/chromium/src/content/browser/frame_host/blocked_scheme_navigation_throttle.cc?rcl=a7ae450d0d465647eaff6dec086bd3f1aabd2a7d&l=35 (and https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/loader/frame_loader.cc?rcl=a7ae450d0d465647eaff6dec086bd3f1aabd2a7d&l=829 for the renderer side)

### na...@chromium.org (2019-03-27)

At this point in time, all renderer initiated navigations have an initiator origin attached to them. Maybe we should use this information to ensure we are showing a correct prompt?

### mb...@chromium.org (2019-04-08)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-29)

Mustafa, would you mind being an owner for this?

### me...@chromium.org (2019-07-30)

This is not specific to data URLs, it's a problem with downloads in general. This POC also works:

function download() {
  var r = window.open('https://google.com');
  r.focus();
  setInterval(function() {
    r.location.href = "https://speed.hetzner.de/100MB.bin";
  }, 1000);
 
My gut feeling is that we should just block cross-origin top-frame multiple download requests and never show the prompt. I'd also argue blocking cross-origin top-frame downloads, but that sounds like it could be a widespread pattern, and I don't know if we'll break legitimate uses.

Navigation folks, WDYT?

### qi...@chromium.org (2019-07-30)

For #7, the origins on the multiple download request popup has been fixed in M76 (crbug.com/970378). So when Chrome prompt user for the multiple download requests, it will show ""https://speed.hetzner.de/" instead of "https://google.com" for the example in #7. The first download will still go through though. 

### me...@chromium.org (2019-07-31)

qinmin: Thanks! You are right, the dialog is now showing the correct origin.

I'm assuming https://crbug.com/chromium/970378 is not the same issue, as that one outright allows multiple downloads. Is that correct? Did the fix for that happen to fix this issue as well?

### qi...@chromium.org (2019-07-31)

Not quite the same issue, but closely related. That issue is caused by using chrome://srcdoc as the origin, and bypassing multiple download restrictions.
The fix to that bug should apply to this one.

### me...@chromium.org (2019-07-31)

Thanks, marking as fixed.

VRP folk: the fix is at https://bugs.chromium.org/p/chromium/issues/detail?id=970378#c24

### sh...@chromium.org (2019-08-01)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-12)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

Per https://crbug.com/chromium/946633#c11 the fix is in https://crbug.com/chromium/970378 which is going to come out in Release-0-M77, so marking this thusly too.

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-30)

Congrats! The Panel decided to reward $500 for this report :) 

### na...@google.com (2019-09-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/946633?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Downloads, UI>Browser>Navigation, UI>Browser>Permissions>Prompts]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094410)*
