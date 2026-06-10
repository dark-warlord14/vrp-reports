# Drag link 🔗 to Tab leads to the origin of an external protocol handler prompt could have been obscured with spoofing 

| Field | Value |
|-------|-------|
| **Issue ID** | [377028613](https://issues.chromium.org/issues/377028613) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>DataTransfer, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pu...@gmail.com |
| **Assignee** | sa...@microsoft.com |
| **Created** | 2024-11-03 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS

Drag link 🔗 to new Tab leads to the origin of an external protocol handler prompt could have been obscured

If a User Drag protocol link 🔗 to New Tab 📑, it does not show origin information📄 in external protocol Permission prompt 

there is threat to exploit this Vulnerability:
if Attacker disable links & right click menu this will force user to drag link or image to new tab
Attacker can add custom domain name with protocol which shows in URL/navigation Bar ex: `calc:google.com`

I have attached video 🌐🔗🔒 reproducing the attack. ✅

VERSION
Chrome Version: 131.0.6778.24 (Official Build) beta (64-bit)
Operating System: [Windows 10 🖥️🖱️]

`REPRODUCTION CASE`
1. Load Attacked HTML File in Your Localhost or Server
2. Open PufIndex.html 
3. Drag Link to new tab (or) Drag image to new tab
    `Result: ` origin information does not show in external protocol Permission prompt



## Attachments

- [Puf_POC.mp4](attachments/Puf_POC.mp4) (video/mp4, 971.0 KB)
- [pufindex.html](attachments/pufindex.html) (text/html, 1.0 KB)

## Timeline

### pe...@google.com (2024-11-04)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### dc...@chromium.org (2024-11-04)

This is very reminiscent of [issue 40060490](https://issues.chromium.org/issues/40060490). The initiator of a link drag is kind of a complex question, but the page itself can't initiate a drag—a user has to do it.

Similarly, in the aforementioned bug, the user has to initiate the action through the right-click menu.

I am tentatively triaging this as low severity, but please be aware that even though [issue 40060490](https://issues.chromium.org/issues/40060490) was considered a low severity security bug, this bug (and the previous bug) are both something I consider to be borderline not security relevant, and that the bug may be updated as such.

### dc...@chromium.org (2024-11-04)

If we do decide to fix this, note that the drag initiator should already be stamped into the drag data, so we can just read out that origin and use it: <https://source.chromium.org/chromium/chromium/src/+/main:ui/base/dragdrop/os_exchange_data.h;l=86;drc=7ca19e90455499b289ad61929d827876a60304f1>

### ch...@chromium.org (2024-11-19)

@ragoulik , any chance you or anyone on the Microsoft side is interested in looking into this bug?

### ap...@google.com (2024-12-10)

Project: chromium/src  

Branch: main  

Author: Samba Murthy Bandaru <[sambamurthy.bandaru@microsoft.com](mailto:sambamurthy.bandaru@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/6043038>

Populate initiator origin in NavigateParams for dropped url links

---


Expand for full commit details
```
Populate initiator origin in NavigateParams for dropped url links 
 
External protocol permission prompt wasn't showing origin information 
when a url link is dropped into new tab because |NavigateParams| are 
not populated with |initator_orgin| from the drop data. Fixed it. 
 
Bug: 377028613 
Change-Id: Ic25396679c39f193d41d28739cc681cbafbf6ab9 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6043038 
Reviewed-by: Dan Clark <daniec@microsoft.com> 
Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
Commit-Queue: Sambamurthy Bandaru <sambamurthy.bandaru@microsoft.com> 
Cr-Commit-Position: refs/heads/main@{#1394046}

```

---

Files:

- M `chrome/browser/ui/views/frame/browser_root_view.cc`
- M `chrome/browser/ui/views/frame/browser_root_view.h`
- M `chrome/browser/ui/views/frame/browser_root_view_browsertest.cc`
- M `content/public/test/navigation_handle_observer.cc`
- M `content/public/test/navigation_handle_observer.h`

---

Hash: 2fff20f1c6b9c209316b1d9cb450f065ff2b1f38  

Date:  Tue Dec 10 02:30:26 2024


---

### sp...@google.com (2024-12-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Thank you reward for an issue with low potential for user harm that resulted in a helpful change in Chrome


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-12)

As mentioned in c#3, the potential for this issue to result in user harm and security impact is very low. Because we did make a change that may be helpful to users because of this report, we did want to show our appreciation for that. Thank you!

### pu...@gmail.com (2024-12-12)

Thank you amy

and thank you for Quick Decision on Bounty I appreciate it

### pu...@gmail.com (2024-12-12)

[am...@chromium.org](mailto:am...@chromium.org)

According to this Ref Issues I provided its show it is a vulnerability

Please see Ref Here:

#1 <https://issues.chromium.org/issues/40060490>

#2 <https://issues.chromium.org/issues/40056198>

#3 <https://issues.chromium.org/issues/40066346>

Kindly please Change Type back to " Vulnerability "

if e.g. evil.com is embedded in an iframe of legit.com and the user drag link to new tab in the iframe in that case Chrome don't tell the user that this came from evil.com and they might think it's from legit.com (even though the new window has no content from legit.com).

<https://issues.chromium.org/issues/40056198#comment5>

### am...@chromium.org (2024-12-12)

All the other issues you linked here are 1) not the same issue, and 2) are lower impact / low severity issues. In our assessment, we concur with c#3 that the security impact here is quite low and requires the user to specifically choose to engage in a non-standard use gesture that is required here. 
We're happy to show appreciation for this report since there was a beneficial change to Chrome made, but we do not see this as a security issue. The issue type here has been updated to reflect that. 


### ch...@google.com (2025-03-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/377028613)*
