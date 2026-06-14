# Chrome crashes when dragging tab out during initiation of "Organize Tabs" function

| Field | Value |
|-------|-------|
| **Issue ID** | [325293263](https://issues.chromium.org/issues/325293263) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>CrashReporting, UI>Browser>TopChrome |
| **Platforms** | Mac, Windows |
| **Chrome Version** | 123.0.6301.2 |
| **Reporter** | xp...@gmail.com |
| **Assignee** | em...@google.com |
| **Created** | 2024-02-15 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. Create multiple tabs that are the same e.g. 2 google.com tabs
2. Open the menu to start the "Organize tabs" function.
3. Click "Start Now"
4. Click and drag the 2 google.com tabs out while the "Organize Tabs" function tries to find duplicate tabs. <= Crash

# Problem Description

Crash

# Additional Comments

See video for replication. I can't replicate in ASan, as this feature doesn't work there?

If any googler could tell me why, that'd be very helpful.

# Summary

Chrome crashes when dragging tab out during initiation of "Organize Tabs" function

# Custom Questions

#### How much crashed?

The whole browser

#### Is it a problem with a plugin?

No - It's the browser itself

# Additional Data

Category: Crashes   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- [chrome_rgkGGmLF3s.mp4](attachments/chrome_rgkGGmLF3s.mp4) (video/mp4, 1.8 MB)
- [uaf_asan.txt](attachments/uaf_asan.txt) (text/plain, 29.9 KB)
- [Organize Tab.png](attachments/Organize Tab.png) (image/png, 254.6 KB)
- [ASAN-heap-buffer-overflow.txt](attachments/ASAN-heap-buffer-overflow.txt) (text/plain, 26.7 KB)
- [ASAN-heap-use-after-free.txt](attachments/ASAN-heap-use-after-free.txt) (text/plain, 27.4 KB)
- [Chrome-Use-After-Free.html](attachments/Chrome-Use-After-Free.html) (text/html, 1.8 KB)
- [poc.zip](attachments/poc.zip) (application/zip, 1.0 KB)

## Timeline

### xp...@gmail.com (2024-03-07)

Still crashing latest Chrome Canary 124.0.6339.0

### st...@google.com (2024-05-21)

Assigning bug to emshack@ since I was able to reproduce this bug on my mac on Canary with version 127.0.6492 and on stable with version 125.0.6422.60.  Here is the crash report with my stable build: https://crash.corp.google.com/browse?q=reportid=%27ccb7585d86c416e9%27

### xp...@gmail.com (2024-05-23)

Hi,

Here's an easier way to trigger:

1: Visit: chrome://tab-search.top-chrome/

2: Execute in devtools:

```
setInterval(()=>{
    document.querySelector("body > tab-search-app").apiProxy_.requestTabOrganization();
}, 5);

window.open('https://www.google.com');
window.open('https://www.google.com');
let win = window.open('about:blank');

// closes about:blank tab to trigger UAF
const uaf_trigger = setTimeout(() => { 
    win.close();
}, 750); 

```

I've also included the ASan crash. Sorry, I thought I'd previously attached it before.

### ap...@google.com (2024-05-24)

Project: chromium/src
Branch: main

commit 2a126748612fccf5ab2055b92dfefb7a338584e1
Author: Emily Shack <emshack@chromium.org>
Date:   Fri May 24 17:58:23 2024

    Remove failing CompleteRequest check
    
    It looks like if you start a request and immediately drag a tab out of
    the tab strip, this check fails because the request is still in the
    NOT_STARTED state. Removing the check in favor of returning early for
    any non-STARTED state.
    
    Bug: 325293263
    Change-Id: I7a2a62b236d756a7361c5a3d84341618511d7f3f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5560550
    Reviewed-by: David Pennington <dpenning@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Commit-Queue: Emily Shack <emshack@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1305817}

M       chrome/browser/ui/tabs/organization/tab_organization_request.cc

https://chromium-review.googlesource.com/5560550


### so...@chromium.org (2024-05-29)

As per step 2 in the comment#1 I cant able to see "Organize Tabs" in the menu. Let me know , If there is any flags to be enabled before executing. 

For your reference I have attached screenshot.  

Thanks !!

### xp...@gmail.com (2024-05-29)

Re #6: I do not know. It's not a flag and neither something I've been able to control. I hear the term "finch flag" coined a few times. Is it one of those?

#6, if you need, I can create you a renderer patch that bypasses it so that you can turn it on. Let me know.

### xp...@gmail.com (2024-06-01)

Re #6: I have noticed a section in chrome://settings called "AI". If you have this section please turn on "Try out experimental AI features" and then "Tab Organizer".

### xp...@gmail.com (2024-06-02)

Hi,

I am still able to reproduce the UAF/crash using steps from `#4` after `#5` CL/patch. Though `#5` CL does fix my original steps, I guess there were two UAFs here?

After doing some digging on why this is still triggerable, it made me realize that this UAF is triggerable from a webpage with certain steps. It looks to be a race-condition. I have created `Chrome-Use-After-Free.html` to demonstrate a 2 click process to a non-protected UAF and heap-buffer-overflow.

I have included both ASan stack traces below and the POC.

# Steps:

1: Open `Chrome-Use-After-Free.html` in Chrome.

2: Click "Start UAF" button (this click isn't necessary in a real world scenario).

3: Click to 'Search Tabs" button in upper left corner.

4: Click "Check now" to start Chrome Organizer.

# Note:

- Depending on how fast or slow your PC is, you may need to adjust `SetTimeout` or `SetInterval` functions. On my setup, this reproduces 100% of the time.
- I think this can be done with a "one click" from an extension. Extensions can open Chrome WebUI tabs like `chrome://tab-search.top-chrome`. An extension can't directly manipulate Chrome pages, but simply having tabs open like `chrome://tab-search.top-chrome` allows an attacker to indirectly call some of the tab-organizer functions when creating tabs, like `apiProxy_.requestTabOrganization()`, our main culprit for this UAF/HBO.

### dr...@chromium.org (2024-06-04)

[security triage] Per [#comment9](https://issues.chromium.org/issues/325293263#comment9), this is not fully fixed and a UAF so marking it as a "Vulnerability" to get into our security bug triage process.

### pe...@google.com (2024-06-04)

Thank you for providing more feedback. Adding the requester to the CC list.

### xp...@gmail.com (2024-06-04)

Extension variant:

1: Extract poc.zip and add it as an extension to Chrome.

2: Go to the top right and click the three dots to open the Chrome main-menu.

3: Click "Organize tabs" => UAF or HBO.

OR

1: Go top left and open "Search Tabs"

2: Press "Organize tabs" => UAF or HBO

### ap...@google.com (2024-06-11)

Project: chromium/src
Branch: main

commit 6deaee3ef2270ad7b4f62ef166f49df2c50a89c7
Author: Emily Shack <emshack@chromium.org>
Date:   Tue Jun 11 17:02:45 2024

    Use weak pointer for complete/fail requests
    
    Bug: 325293263
    Change-Id: Ib6952c7c558af5193f79a8dab98427d26631eb84
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5618014
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: David Pennington <dpenning@chromium.org>
    Commit-Queue: Emily Shack <emshack@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1313489}

M       chrome/browser/ui/tabs/organization/tab_organization_request.cc
M       chrome/browser/ui/tabs/organization/tab_organization_request.h

https://chromium-review.googlesource.com/5618014


### em...@google.com (2024-06-11)

I wasn't able to reliably reproduce this but am hoping the above CL fixes the issue, speculatively marking as fixed.

### xp...@gmail.com (2024-06-11)

Hello, I can confirm CL @ `#13` fixed the UAF/HBO in both the extension and webpage variant's. Thank you v/ much for the fix.

### sp...@google.com (2024-06-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
report of moderately mitigated memory corruption bug in a non-sandboxed process; least mitigated scenario has precondition of installation of malicious extension + mild user interaction 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-21)

Thank your for your efforts, Sven, and reporting this issue to us! Nice to see some folks converting over to the Bugcrowd payments process already! :D

### xp...@gmail.com (2024-06-22)

Yes, thank you for adding that option! :)

Thank you for the reward as well. Have a nice weekend.

### pe...@google.com (2024-09-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/325293263)*
