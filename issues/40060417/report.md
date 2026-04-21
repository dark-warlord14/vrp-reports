# Security: UAF in UserNoteService

| Field | Value |
|-------|-------|
| **Issue ID** | [40060417](https://issues.chromium.org/issues/40060417) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Creation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | gu...@google.com |
| **Created** | 2022-07-27 |
| **Bounty** | $30,000.00 |

## Description

**VULNERABILITY DETAILS**

After observing DidFinishNavigation[1] event, UserNoteService will call[2] |OnNoteMetadataFetchedForNavigation| asynchronously with |{rfh}| as parameter:

```
void UserNoteService::OnFrameNavigated(content::RenderFrameHost\* rfh) {  
  [...]  
  
  std::vector<content::RenderFrameHost\*> frames = {rfh};  
  UserNoteStorage::UrlSet urls = {rfh->GetLastCommittedURL()};  
  storage_->GetNoteMetadataForUrls(  
      std::move(urls),  
      base::BindOnce(&UserNoteService::OnNoteMetadataFetchedForNavigation, <<<=====  
                     weak_ptr_factory_.GetWeakPtr(), frames, rfh));  
}  

```

So there is a race between the destruct of the RenderFrameHost |rfh| and the execution of the callback function.  

Accessing |all\_frames[0]|[3] after |rfh| is destroyed will trigger this UAF.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/user_notes/user_notes_tab_helper.cc;l=36;drc=a33ca7f30c9f6a875cdfb6ce37bb277131d10eaa>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:components/user_notes/browser/user_note_service.cc;l=75;drc=25c9d917a88f5ad952718f61d0279c5f448cc730>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:components/user_notes/browser/user_note_service.cc;l=386;drc=25c9d917a88f5ad952718f61d0279c5f448cc730>

**VERSION**  

Chrome Version: head with UserNotes feature.

**REPRODUCTION CASE**

$ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-features=UserNotes,UnifiedSidePanel "<http://localhost:8000/trigger.html>"  

Click the trigger button.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 30.5 KB)
- [poc.html](attachments/poc.html) (text/plain, 369 B)
- [reload.html](attachments/reload.html) (text/plain, 109 B)

## Timeline

### le...@gmail.com (2022-07-27)

Sry, "http://localhost:8000/trigger.html" should be "http://localhost:8000/poc.html".

### [Deleted User] (2022-07-27)

[Empty comment from Monorail migration]

### bh...@google.com (2022-07-28)

Thanks for the report. Guillaume, please let us know if this should be assigned to someone else.

[Monorail components: UI>Browser>Creation]

### bh...@google.com (2022-07-28)

I reproduced this in linux for M105, and could not reproduce for M104. This can also be verified by looking at the commit dates on the appropriate files.

### [Deleted User] (2022-07-28)

[Empty comment from Monorail migration]

### bh...@google.com (2022-07-28)

Setting Security impact none as this feature is disabled by default. 

### bh...@google.com (2022-07-28)

CCing other owners.

### bo...@chromium.org (2022-07-28)

Thanks for the report! Yup, looks like we need to use a WeakPtr here. 

I believe gujen@ may be OOO on leave by now. I'm on vacation for a week but will take a look when I return if gujen@ is actually out. (Since this is unshipped I don't believe there's urgency here).

### le...@gmail.com (2022-07-28)

Yes, it's hidden behind a new feature flag, so it's not that urgent, please enjoy your vacation. And I also submitted another UAF bug for this module, you can handle it together: crbug.com/1348113

### gu...@google.com (2022-07-29)

I haven't left just yet, will take a look today and Monday

### gu...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### gu...@google.com (2022-08-08)

Posting an update here due to "NextAction":
This has been in review for some time, just waiting for David to come back from vacation to review
https://chromium-review.googlesource.com/c/chromium/src/+/3803510

### gi...@appspot.gserviceaccount.com (2022-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/732f33b643eec81eb79ec3f60fb56a03e13aed6c

commit 732f33b643eec81eb79ec3f60fb56a03e13aed6c
Author: Guillaume Jenkins <gujen@google.com>
Date: Tue Aug 09 21:58:15 2022

[Notes] use weak document pointer for async operations

Fixes a UAF issue with UserNotes async operations involving
RenderFrameHost pointers. All async APIs now use WeakDocumentPtrs
and validate them before using them.

While at it, this also removes the navigated_frame parameter of the
OnNoteMetadataFetchedForNavigation method, since it wasn't actually
needed (all_frames[0] is sufficient).

Bug: 1347707
Change-Id: Ieb4def5da5afdc21c3b61b77c08cbf4d49d63d04
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3803510
Commit-Queue: Guillaume Jenkins <gujen@google.com>
Reviewed-by: David Bokan <bokan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1033218}

[modify] https://crrev.com/732f33b643eec81eb79ec3f60fb56a03e13aed6c/components/user_notes/browser/user_note_service.cc
[modify] https://crrev.com/732f33b643eec81eb79ec3f60fb56a03e13aed6c/components/user_notes/browser/user_note_utils.cc
[modify] https://crrev.com/732f33b643eec81eb79ec3f60fb56a03e13aed6c/components/user_notes/browser/user_note_utils_unittest.cc
[modify] https://crrev.com/732f33b643eec81eb79ec3f60fb56a03e13aed6c/components/user_notes/browser/user_note_service_unittest.cc
[modify] https://crrev.com/732f33b643eec81eb79ec3f60fb56a03e13aed6c/components/user_notes/browser/user_note_utils.h
[modify] https://crrev.com/732f33b643eec81eb79ec3f60fb56a03e13aed6c/components/user_notes/browser/user_note_service.h


### gu...@google.com (2022-08-10)

Should be fixed now!

### [Deleted User] (2022-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-10)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-17)

Congratulations, Leecraso! The VRP Panel has decided to award you $30,000 for this report under the updated VRP reward amounts. Thank you for your efforts in reporting this issue to us and great work! 

### le...@gmail.com (2022-08-18)

Thanks for the increased bonuses and new rules.

### am...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-11-16)

This issue was migrated from crbug.com/chromium/1347707?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060417)*
