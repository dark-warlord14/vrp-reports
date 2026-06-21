# NetError's page AutoReloader leads to multi-download blocker bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [475265304](https://issues.chromium.org/issues/475265304) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | mm...@chromium.org |
| **Created** | 2026-01-13 |
| **Bounty** | $3,000.00 |

## Description

#### VULNERABILITY DETAILS

Chrome's `NetErrorAutoReloader` automatically retries failed navigations (including `ERR_TOO_MANY_REDIRECTS`) after a delay. When a navigation exceeds the 20-redirect limit and fails with `ERR_TOO_MANY_REDIRECTS`, the auto-reloader retries it after a 1-second delay. This retry allows an attacker to trigger downloads without proper user interaction validation, effectively bypassing the multi-download blocker.

The `NetErrorAutoReloader` uses an exponential backoff schedule for retries: 1 second, 5 seconds, 30 seconds, 1 minute, 5 minutes, 10 minutes, and 30 minutes for subsequent attempts. An attacker can leverage this by using a service worker to serve a download on the first retry (after 1 second), causing the error page to persist. The second retry (after 5 seconds) is then used to redirect the user back to the attacker's page, restarting the entire attack loop and allowing unlimited downloads without any user interaction.

##### Breakdown of the attack

1. Attacker automatically redirects the user to a page that triggers a chain of 20 redirects.
2. At the 21st redirect, Chrome triggers `ERR_TOO_MANY_REDIRECTS` and shows an error page.
3. `ShouldAutoReload()` returns `TRUE` because `ERR_TOO_MANY_REDIRECTS` is not in the exclusion list.
4. After a 1-second delay (first retry), `ReloadMainFrame()` reloads the failed URL.
5. The service worker serves a downloadable file. The download is initiated without requiring a user gesture, and the error page remains.
6. After a 5-second delay (second retry), the auto-reloader retries again. This time, the service worker redirects back to the attacker's page.
7. The attack loop restarts, allowing the attacker to trigger unlimited downloads.

I have also attached a video reproducing the attack (`repro.mp4`).

#### BISECT

By doing an initial bisect, I found that the issue was introduced between 791932 and 791966 (<https://chromium.googlesource.com/chromium/src/+log/74fcfa083f8f12b9a7e5181176921dc6a2b2d5de..281c417f3a79f4220addb3592c241f9e3913bb28>).

After investigating, it became clear that the commit that introduced the issue is <https://chromium.googlesource.com/chromium/src/+/4408a0fab85c8a2d4aafe3ede4a42524109dbb15>, and it landed on M86.0.4215.0.

#### VERSION

Chrome Version: 143.0.7499.170 (Stable)   

Chrome Version: 144.0.7559.31 (Beta)   

Chrome Version: 145.0.7587.5 (Dev)   

Chrome Version: 145.0.7618.0 (Canary)   

Operating System: Windows 11 24H2

#### REPRODUCTION CASE

##### Steps to setup the PoC

1. Download the following files: `index.html` and `sw.js`.
2. Move all files into the same folder.
3. Serve the files using a local web server (e.g., `python -m http.server 8080`).

##### Steps to reproduce the issue

1. Navigate to `http://localhost:8080/index.html`.
2. Chrome will show an `ERR_TOO_MANY_REDIRECTS` error page. After 1 second (first retry), `NetErrorAutoReloader` automatically retries the last URL.
3. The service worker serves the download file. Notice that `bypass.txt` is downloaded without additional user interaction.
4. After 5 seconds (second retry), the auto-reloader retries again. The service worker now redirects back to `index.html`.
5. The attack loop restarts automatically, triggering another download after 1 second. This cycle repeats indefinitely, allowing unlimited downloads without any user interaction.

#### CREDIT INFORMATION

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [index.html](attachments/index.html) (text/html, 651 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 2.8 MB)
- [sw.js](attachments/sw.js) (text/javascript, 1.2 KB)

## Timeline

### wf...@chromium.org (2026-01-13)

Thanks for the report. This is quite clever. It does bypass the download limit protections, so I am triaging as Sev-Low.

### mm...@chromium.org (2026-01-13)

It looks like we should perhaps rethink the logic in <https://source.chromium.org/chromium/chromium/src/+/main:components/error_page/content/browser/net_error_auto_reloader.cc;l=177> - we currently schedule a reload if a navigation doesn't commit, and we're showing an error page. This can happen if a load stalls, and a user cancels it (in which case, reloading might be good to do)...but also is presumably happening if a download is triggered.

I'm not sure if we can easily carve out the download case, though it would probably be safest only to trigger another reload if the original reload we triggered return an error code, and we just suppressed the error page by a ShouldSuppressErrorPage() call. I'm not that familiar with navigation, but may be sufficient just to set a bool if we suppress an error page, and check it clear it if a navigation was cancelled. That may not be perfect, in the case there is a user-initiated navigation around the time we cancel an auto-reload, but if a multi-download exploit requires the user also navigate the page around the time we're suppressing a reload, that's probably good enough.

### wf...@chromium.org (2026-01-15)

low sev bugs need owners, sorry, but if you wait 30 days... <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#TOC-Low-severity> :)

### mm...@chromium.org (2026-03-03)

I am actually going to fix this. The simplest thing to do is just to not auto-reload again if the previous navigation was not aborted due specifically to the AutoReloader. It's a pretty straightforward change.

It does mean if anything else interrupts the auto-reload chain (The user cancelling an auto-reload, or navigating and then cancelling before commit), we'll stop auto-reloading as well, but I'm not sure either of those is a bad thing.

Auto-reloading is strictly a best effort thing, so doing it a little less aggressively shouldn't be a big problem.

### mm...@chromium.org (2026-03-04)

[ricea] Thought I'd be sending out a CL to you today, but ran into some issues I need to look into. May end up being next week before I send out the CL.

### dx...@google.com (2026-03-09)

Project: chromium/src  

Branch:  main  

Author:  Matt Menke [mmenke@chromium.org](mailto:mmenke@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7629083>

Make NetErrorAutoReloader less aggressive.

---


Expand for full commit details
```
     
    On certain main frame network errors, NetErrorAutoReloader will 
    periodically reload the page, and keep on doing so until a new page is 
    committed, checking on every failed commit if the last commit was an 
    error page that needed reloading, and starting a reload timer if so, 
    as well as cancelling commits of an identical new error page. It does 
    not check the reason that a commit failed, so a commit being cancelled 
    because of a 204, or a download, will not stop the reloaded from 
    trying to reload the page. 
     
    This CL instead only starts the autoreload time on failed commits if 
    that failed commit was due to the AutoReloader itself cancelling the 
    previous commit, due to it being the same error page. 
     
    So now, e.g., cancelling an auto reload, triggering a download (which 
    looks like a cancelled navigation), or starting a new load and then 
    cancelling it before commit will all stop the auto reload timer. 
    This is a bit more user friendly, though going offline and then online 
    again will restart the reload timer (as will another navigation 
    resulting in a network error, whether it's the same error or a new 
    one). 
     
    Fixed: 475265304 
    Change-Id: If12a2256c33bf5f91c7ad544c0ad3e2f682df855 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7629083 
    Reviewed-by: Adam Rice <ricea@chromium.org> 
    Commit-Queue: mmenke <mmenke@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1596504}

```

---

Files:

- M `components/error_page/content/browser/net_error_auto_reloader.cc`
- M `components/error_page/content/browser/net_error_auto_reloader.h`
- M `components/error_page/content/browser/net_error_auto_reloader_browsertest.cc`

---

Hash: [69fd5caaf52d636159a13ee893e63de0fd249495](https://chromiumdash.appspot.com/commit/69fd5caaf52d636159a13ee893e63de0fd249495)  

Date: Mon Mar 9 19:05:58 2026


---

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
web platform privilege escalation, low impact, plus bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/475265304)*
