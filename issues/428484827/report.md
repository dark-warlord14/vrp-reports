# Confusion on permission prompt lead to spoof (using split view)

| Field | Value |
|-------|-------|
| **Issue ID** | [428484827](https://issues.chromium.org/issues/428484827) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Prompts, UI>Browser>TopChrome>TabStrip>SplitView |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ag...@google.com |
| **Created** | 2025-06-29 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

when opening a page using "open link in split view" on tab 1 using the file:// protocol and on tab 2 using the file:// protocol also at the same time on tab 1 calls the permission prompt and "open link in split view" is clicked this causes confusion on the permission prompt when the focus moves to tab 2, the victim will think that the permission prompt called from tab 2 will cause spoofing.

VERSION
Chrome Version : 140.0.7267.0 (Official Build) canary (64-bit)
Operating System: Windows 11

REPRODUCTION CASE

 1. enable split view on chrome://flags/hashtag#side-by-side
 2. Download  spoofpermisx.html and perm.html in same folder
 3. Open spoofpermisx.html
 4. Right click the link then choose "Open link in split view"
 5. In tab 2 will open perm.html and show permission (this is from tab 1 using oncontextmenu)




## Attachments

- bandicam 2025-06-29 21-30-09-024.mp4 (video/mp4, 2.1 MB)
- spoofpermisx.html (text/html, 1.3 KB)
- perm.html (text/html, 228 B)

## Timeline

### dc...@chromium.org (2025-06-30)

Given that this seems specific to files (as the permission prompt includes origins), I think this is either low or medium. It might be worth thinking about this more and making sure things like the permission bubble are not confusing though.

### pe...@google.com (2025-06-30)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### ag...@google.com (2025-07-16)

Steven, this seems to fall into the dialogs/scrim theme so I'm assigning to you.

### ag...@google.com (2025-09-03)

Bugjuggler: (b/428484827 unblocked && b/428484827 has no open children) -> agale@

### bu...@google.com (2025-09-03)

Hi. I've received your bug and will wait for b/428484827 to be unblocked and wait for b/428484827's children to be closed and then assign the bug to agale.

### dx...@google.com (2025-09-11)

Project: chromium/src  

Branch:  main  

Author:  Alison Gale [agale@chromium.org](mailto:agale@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6900377>

[SxS] Hide permissions prompt when split tab is inactive

---


Expand for full commit details
```
     
    Pass TabInterface into PermissionRequestManager to observe active state. 
    This is only needed for desktop currently. From there, register 
    callbacks for state events that can be used to determine when the 
    permissions chip can show. 
     
    Change-Id: Ib46fac4264f4966fbc4daabb8aa4bb46eeeeb28e 
    Bug: 428484827,441140179 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6900377 
    Reviewed-by: Eshwar Stalin <estalin@chromium.org> 
    Commit-Queue: Alison Gale <agale@chromium.org> 
    Reviewed-by: Ravjit Uppal <ravjit@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1514437}

```

---

Files:

- M `chrome/browser/permissions/BUILD.gn`
- M `chrome/browser/permissions/permission_request_manager_browsertest.cc`
- M `chrome/browser/ui/tab_helpers.cc`
- M `chrome/browser/ui/views/permissions/chip/chip_controller.cc`
- M `chrome/browser/ui/views/permissions/chip/chip_controller.h`
- M `components/permissions/BUILD.gn`
- M `components/permissions/DEPS`
- M `components/permissions/permission_request_manager.cc`
- M `components/permissions/permission_request_manager.h`

---

Hash: [4162199060c83a9dcdab0e19670d59dc520ee483](https://chromiumdash.appspot.com/commit/4162199060c83a9dcdab0e19670d59dc520ee483)  

Date: Thu Sep 11 18:55:36 2025


---

### bu...@google.com (2025-09-11)

Bug is closed; my job here is done.

### dx...@google.com (2025-09-15)

Project: chromium/src  

Branch:  refs/branch-heads/7390  

Author:  Alison Gale [agale@chromium.org](mailto:agale@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6950796>

[M141] [SxS] Hide permissions prompt when split tab is inactive

---


Expand for full commit details
```
     
    Original change's description: 
    > [SxS] Hide permissions prompt when split tab is inactive 
    >  
    > Pass TabInterface into PermissionRequestManager to observe active state. 
    > This is only needed for desktop currently. From there, register 
    > callbacks for state events that can be used to determine when the 
    > permissions chip can show. 
    >  
    > Change-Id: Ib46fac4264f4966fbc4daabb8aa4bb46eeeeb28e 
    > Bug: 428484827,441140179 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6900377 
    > Reviewed-by: Eshwar Stalin <estalin@chromium.org> 
    > Commit-Queue: Alison Gale <agale@chromium.org> 
    > Reviewed-by: Ravjit Uppal <ravjit@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1514437} 
     
    (cherry picked from commit 4162199060c83a9dcdab0e19670d59dc520ee483) 
     
    Bug: 444709415,428484827,441140179 
    Change-Id: Ib46fac4264f4966fbc4daabb8aa4bb46eeeeb28e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6950796 
    Auto-Submit: Chrome Cherry Picker <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7390@{#990} 
    Cr-Branched-From: d481efce5eb300acbb896686676ebd0352a6f1db-refs/heads/main@{#1509326}

```

---

Files:

- M `chrome/browser/permissions/BUILD.gn`
- M `chrome/browser/permissions/permission_request_manager_browsertest.cc`
- M `chrome/browser/ui/tab_helpers.cc`
- M `chrome/browser/ui/views/permissions/chip/chip_controller.cc`
- M `chrome/browser/ui/views/permissions/chip/chip_controller.h`
- M `components/permissions/BUILD.gn`
- M `components/permissions/DEPS`
- M `components/permissions/permission_request_manager.cc`
- M `components/permissions/permission_request_manager.h`

---

Hash: [c438dcdbfa00a731ed1365645a380dac1e821189](https://chromiumdash.appspot.com/commit/c438dcdbfa00a731ed1365645a380dac1e821189)  

Date: Mon Sep 15 22:24:24 2025


---

### sp...@google.com (2025-09-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
permission prompt spoof but the origin is correct so mitigated


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-12-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> permission prompt spoof but the origin is correct so mitigated

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/428484827)*
