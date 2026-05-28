# Security: `Android` Top-level redirect from cross-origin iframe by setting `Content-Security-Policy: sandbox allow-top-navigation` Bypass of Issue 1251790

| Field | Value |
|-------|-------|
| **Issue ID** | [364508691](https://issues.chromium.org/issues/364508691) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>PopupBlocker |
| **Platforms** | Android |
| **Reporter** | el...@gmail.com |
| **Assignee** | lb...@google.com |
| **Created** | 2024-09-04 |
| **Bounty** | $3,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
Reference from the report:
https://issues.chromium.org/issues/41493458

Based on report #41493458 has been fixed where every request that comes out of the iframe src that will be redirected to another domain will be blocked by chrome in the block setting, but the alert popup redirect or popup block is not protected in the tap delay on android that has been applied to the permission access prompt, where every prompt that appears will have a delay until the new user can tap or click to protect against tapjacking or clickjacking.

However, on Chrome Android it is not applied to notifications or redirect prompts, or blocked popups that can be tapjacked.

VERSION
Chrome Version: Chrome 128.0.6613.99 Stable
Chrome Version: Chrome Canary 130.0.6694.0
Operating System: Android 14; Infinix X678B Build/UP1A.231005.007

REPRODUCTION CASE
1. Open https://getbounty.online/allow.html
2. Tap 10x or 4x on the button
3. Redirect blocked bypass

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Om Apip

## Attachments

- [allow.html](attachments/allow.html) (text/html, 2.4 KB)
- [CANARY_130.mp4](attachments/CANARY_130.mp4) (video/mp4, 5.2 MB)
- [Chrome_128.mp4](attachments/Chrome_128.mp4) (video/mp4, 5.3 MB)
- [demo.htm](attachments/demo.htm) (text/html, 67 B)

## Timeline

### ct...@chromium.org (2024-09-04)

Thanks for the report! Could you please attach the source for the remote server in the allow.html file? (<https://painted-dandelion-juravenator.glitch.me/demo>). In the future please try to make pocs self-contained and locally reproducible (multiple files, requiring starting up a local server, etc. are all fine).

The security consequences of the "allow popups" prompt are somewhat limited, and this requires a fair amount of user interaction to trick the user into accepting the prompt, so initially setting this as Severity-Low (S3) and FoundIn-128.

lbrady@ would you be a good person to take a look at this given your work on [Issue 41493458](https://issues.chromium.org/issues/41493458)? If not, feel free to pass this back to me and I can find another owner.

### fe...@gmail.com (2024-09-04)

Thank you for your suggestion, I will do it next time, and here are the files you requested, thank you.

### ct...@chromium.org (2024-09-05)

Thanks!

Also cc'ing lazzzis@ who I think did the port of the old Popup Blocker infobar to the newer Messages implementation, since this may be more browser UI related than iframe/activation related.

### pe...@google.com (2024-09-05)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### fe...@gmail.com (2024-10-25)

any update team?

### lb...@google.com (2024-10-25)

I haven't had time to take a look at this. I agree with cthomp@'s assessment and confirmed with lazzzis@ that this is a UI issue rather than something directly involving the web platform. I'll try to find time in the coming weeks to sit down and get a fix in place. Thanks for your patience!

### lb...@google.com (2024-11-08)

Reassigning to lazzzis@ as this fix is going to be more involved than originally anticipated, and I don't have as much knowledge about this part of the codebase.

### fe...@gmail.com (2025-05-12)

Hi team, any update on this?

### fe...@gmail.com (2025-08-18)

Hi guys, I just want to make sure regarding this vulnerability, is it still a priority or is it no longer considered important? 

### la...@google.com (2025-08-18)

still in engineer's backlog. Will take a look when time allows. Thanks for reminding.

### la...@google.com (2025-08-19)

This should be fixed in a CL merged early this year <https://chromium-review.googlesource.com/c/chromium/src/+/6411166>

Could you verify if this is still reproducible?

### fe...@gmail.com (2025-08-19)

i have checked, yap already fixed

### ch...@google.com (2025-08-19)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### fe...@gmail.com (2025-08-20)

thanks guys for your response , may i know for the bounty?

### pe...@google.com (2025-08-22)

The NextAction date has arrived: 2025-08-22
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### fe...@gmail.com (2025-08-25)

hi guys, please let me know if I get the Bounty or not ?

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Due to the lack of potential for security consequences for a user presented by this issue combined with the significant user interaction and specific time required here, we consider this to be a functional bug. 
Additionally, the fix that resolved this issue was due to a previous report of a slightly different issue with a low-impact security outcome. This report is unfortunately not eligible for a Chrome VRP reward.

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### ch...@google.com (2025-11-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/364508691)*
