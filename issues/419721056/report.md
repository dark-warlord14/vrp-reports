# `showSaveFilePicker()` DIalog can Overlaid on Other Origin lead to Origin Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [419721056](https://issues.chromium.org/issues/419721056) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Mac |
| **Chrome Version** | 136.0.0.0 |
| **Reporter** | fr...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2025-05-23 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Access poc.html
2. Click anywhere at the poc.html
3. Browse any sites and after 3sec the dialog will appear on other origin

# Problem Description

This vulnerability occurs when the showSaveFilePicker() dialog can be overlaid on another origin . By default, if a page is inactive or not actively accessed by the user, any dialogs should remain inactive, even if the dialog delayed. The dialog should only appear again when the user actively interacts with the page.

# Summary

`showSaveFilePicker()` DIalog can Overlaid on Other Origin lead to Origin Spoofing

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [showsavefilepicker can overlaid on other origin.mov](attachments/showsavefilepicker can overlaid on other origin.mov) (video/quicktime, 14.5 MB)
- [poc.html](attachments/poc.html) (text/html, 1.3 KB)

## Timeline

### pa...@chromium.org (2025-05-23)

Thanks for the report. Can you provide the mentioned `poc.html` file?

### fr...@gmail.com (2025-05-23)

Sorry, i've forgot to provide the poc.html, here is it

### pe...@google.com (2025-05-23)

Thank you for providing more feedback. Adding the requester to the CC list.

### pa...@chromium.org (2025-05-23)

Thanks. TBH, I am unsure how this could be actionable, since it requires the user to switch tab with the right timing. It is somewhat related to [issue 40059071](https://issues.chromium.org/issues/40059071), although in that case the window is not opened by JS. @jarhar, WDYT about this? I read in the other bug in idea about showing the origin in the file picker, which would somewhat mitigate that. Setting low severity for now, but this might just not be a bug at all.

### ja...@chromium.org (2025-05-28)

I think that `<input type=file>` has a mitigation for this which we should add to the file system apis

### ja...@chromium.org (2025-05-28)

It looks like this patch implemented a mitigation for `<input type=file>`: <https://chromium-review.googlesource.com/c/chromium/src/+/4755412>

### pe...@google.com (2025-05-29)

The NextAction date has arrived: 2025-05-29
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### fr...@gmail.com (2025-07-09)

Hi team, is there any update on this?

### dx...@google.com (2025-08-14)

Project: chromium/src  

Branch:  main  

Author:  Joey Arhar [jarhar@chromium.org](mailto:jarhar@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6599151>

Make FileSystem picker APIs only work when tab is visible

---


Expand for full commit details
```
     
    A similar fix was made for <input type=file> in 
    commit 3afe258e082d2f69abdb518c740cbd563d753d4f 
     
    Fixed: 419721056 
    Change-Id: Ib0cac0eb8dacc3f9636e8a7f7570f9d93c5d54e1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6599151 
    Reviewed-by: Fergal Daly <fergal@chromium.org> 
    Commit-Queue: Joey Arhar <jarhar@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1501693}

```

---

Files:

- M `chrome/browser/ui/views/file_system_access/file_system_access_browsertest.cc`
- M `content/browser/file_system_access/file_system_access_manager_impl.cc`
- M `content/browser/file_system_access/file_system_access_manager_impl_unittest.cc`

---

Hash: [7dc60931c299a6b9d59e7cab51692de39ecace54](https://chromiumdash.appspot.com/commit/7dc60931c299a6b9d59e7cab51692de39ecace54)  

Date: Thu Aug 14 23:45:13 2025


---

### fr...@gmail.com (2025-08-28)

Hi team, any updates regarding the VRP decision?

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### fr...@gmail.com (2025-08-28)

Thanks for the reward!

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

### ch...@google.com (2025-11-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/419721056)*
