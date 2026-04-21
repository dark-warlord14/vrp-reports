# Chrome's Profile Picker UAF

| Field | Value |
|-------|-------|
| **Issue ID** | [40934491](https://issues.chromium.org/issues/40934491) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Profiles |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | no...@ssd-disclosure.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2023-10-01 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**

### REPRODUCTION CASE

When there is one user profile of Chrome, [chrome://profile-picker](javascript:void(0);) directly entered into the address bar, and deletes the profile by pressing the button., Use After Free occurs.

**Problem Description:**

### ROOT CAUSE ANALYSIS

### Free

```
WebUIImpl::~WebUIImpl() {  
  // Delete the controller first, since it may also be keeping a pointer to some  
  // of the handlers and can call them at destruction.  
  // Note: Calling this might delete |web_content_| and |frame_host_|. The two  
  // pointers are now potentially dangling.  
  // See https://crbug.com/1308391  
  controller_.reset(); // [0]  
  
  remote_.reset();  
  receiver_.reset();  
}  

```

[0] When a profile is deleted, all windows belonging to the profile are closed, and also the `controller_` object is freed.

### Use

```
void ProfilePickerHandler::HandleRemoveProfile(const base::Value::List& args) {  
  CHECK_EQ(1U, args.size());  
  const base::Value& profile_path_value = args[0];  
  absl::optional<base::FilePath> profile_path =  
      base::ValueToFilePath(profile_path_value);  
  
  if (!profile_path) {  
    NOTREACHED();  
    return;  
  }  
  
#if BUILDFLAG(IS_CHROMEOS_LACROS)  
  // On Lacros, the primary profile should never be deleted.  
  CHECK(!Profile::IsMainProfilePath(\*profile_path));  
#endif  // BUILDFLAG(IS_CHROMEOS_LACROS)  
  
  RecordProfilePickerAction(ProfilePickerAction::kDeleteProfile);  
  webui::DeleteProfileAtPath(\*profile_path,  
                             ProfileMetrics::DELETE_PROFILE_USER_MANAGER); // [1]  
  
  DCHECK(profile_statistics_keep_alive_);  
  profile_statistics_keep_alive_.reset();  
}  

```

[1] The `HandleRemoveProfile` function is called to delete the profile, and UAF occurs when accessing the already freed `webui` object.

### RECOMMENDED PATCH

```
--- a/browser/ui/webui/signin/profile_picker_handler.cc  
+++ b/browser/ui/webui/signin/profile_picker_handler.cc  
@@ -838,6 +838,7 @@  
 #endif  // BUILDFLAG(IS_CHROMEOS_LACROS)  
   
   RecordProfilePickerAction(ProfilePickerAction::kDeleteProfile);  
+  CHECK(webui);  
   webui::DeleteProfileAtPath(\*profile_path,  
                              ProfileMetrics::DELETE_PROFILE_USER_MANAGER);  
   

```

---

Patching vulnerabilities seems very important because attackers can exploit this using Chrome Extension.

---

### VERSION

\* Chrome Version: 118.0.5961.0 (Developer Build) (x86\_64), Also Stable.  

\* Operating System: macOS Ventura 13.4.1 (22F770820d)

### CREDIT

parkminchan, working for SSD Labs Korea.

**Additional Comments:**

\*\*Chrome version: \*\* 118.0.5691.0 \*\*Channel: \*\* Stable

**OS:** Mac OS

## Attachments

- [readme.md](attachments/readme.md) (text/plain, 2.5 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 34.3 KB)

## Timeline

### [Deleted User] (2023-10-01)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-10-01)

Thank you for the report!

Hello alexilin@chromium.org I see that you have made changes to this file in the past. Would you be able to help triage this bug to the proper owner? Thanks!

[Monorail components: UI>Browser>Profiles]

### [Deleted User] (2023-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-01)

[Empty comment from Monorail migration]

### al...@chromium.org (2023-10-02)

droger@, could you help triage this?

### dr...@chromium.org (2023-10-02)

This probably can only happen when opening the profile picker in a tab, which is intended for debugging only and is not supposed to be a user-facing feature.

We should still fix that though.

### al...@chromium.org (2023-10-02)

Right. A Chrome extension can open this URL though and use this UaF for an exploit, so this is more important that it might sound.

### [Deleted User] (2023-10-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2023-10-03)

> This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

I don't think this is a regression. Not sure why the bots believes that. Removing the spurious labels like ReleaseBlockStable.

I would not fix this on M118 at this point. Moving to M119.

### be...@google.com (2023-10-03)

Adding Hotlist-RBS-Removed for tracking purposes.

### [Deleted User] (2023-10-03)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2023-10-04)

I don't understand why the bot insists that it's a regression. Adding ReleaseBlock-NA to silence it.

### dr...@chromium.org (2023-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ca9e7b45b8341f435e02456ce5d0c23a5f1f697a

commit ca9e7b45b8341f435e02456ce5d0c23a5f1f697a
Author: David Roger <droger@chromium.org>
Date: Thu Oct 05 16:37:17 2023

[profiles] Fix crash when deleting a profile from the picker in a tab

Deleting the profile could delete the picker itself if it was loaded in
a tab. This was unexpected by the `ProfilePickerHandler` and caused a
Use-After-Free.

This CL fixes the UaF, and adds tests for profile deletion (including a
regression test).

Fixed: 1488267
Change-Id: Ic3b749f28046cb9dd141386b1ad897d4eeffa688
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4909536
Reviewed-by: Gabriel Oliveira <gabolvr@google.com>
Commit-Queue: David Roger <droger@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1205882}

[modify] https://crrev.com/ca9e7b45b8341f435e02456ce5d0c23a5f1f697a/chrome/browser/ui/views/profiles/profile_picker_view_browsertest.cc
[modify] https://crrev.com/ca9e7b45b8341f435e02456ce5d0c23a5f1f697a/chrome/browser/ui/webui/signin/profile_picker_handler.h
[modify] https://crrev.com/ca9e7b45b8341f435e02456ce5d0c23a5f1f697a/chrome/browser/ui/webui/signin/profile_picker_handler.cc


### [Deleted User] (2023-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-05)

Requesting merge to dev M119 because latest trunk commit (1205882) appears to be after dev branch point (1204232).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2023-10-09)

1. Which CLs should be backmerged? (Please include Gerrit links.)
https://crrev.com/ca9e7b45b8341f435e02456ce5d0c23a5f1f697a

2. Has this fix been tested on Canary?
Verified on Mac Canary 120.0.6055.0

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
No and No.

4. Does this fix pose any known compatibility risks?
No

5. Does it require manual verification by the test team? If so, please describe required testing.
No

### dr...@chromium.org (2023-10-10)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-10-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-11)

This UAF is BRP protected and is mitigated by extension to leverage the non-user facing UI vector.
That being said, the bot did the right thing here and limited merge request to 119, current beta and not Stable. 
There do not appear to be any stability or other risks for backmerge during the bake time so far, as such approving 119 merge for https://crrev.com/c/4909536, please merge this fix to branch 6045 at your earliest convenience. 

### am...@google.com (2023-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-11)

Congratulations on another one, parkminchan! The Chrome VRP Panel has decided to award you $1,000 for this report of a significantly mitigated security bug. The reward amount was decided upon based on this UAF being BRP protected and mitigated by user interaction. Thank you for your efforts and reporting this issue to us! 

### gi...@appspot.gserviceaccount.com (2023-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/158e171a33d35dc443f9e42dbf5c536aeb72fb83

commit 158e171a33d35dc443f9e42dbf5c536aeb72fb83
Author: David Roger <droger@chromium.org>
Date: Thu Oct 12 09:19:43 2023

[profiles] Fix crash when deleting a profile from the picker in a tab

Deleting the profile could delete the picker itself if it was loaded in
a tab. This was unexpected by the `ProfilePickerHandler` and caused a
Use-After-Free.

This CL fixes the UaF, and adds tests for profile deletion (including a
regression test).

(cherry picked from commit ca9e7b45b8341f435e02456ce5d0c23a5f1f697a)

Fixed: 1488267
Change-Id: Ic3b749f28046cb9dd141386b1ad897d4eeffa688
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4909536
Reviewed-by: Gabriel Oliveira <gabolvr@google.com>
Commit-Queue: David Roger <droger@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1205882}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4931679
Auto-Submit: David Roger <droger@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/6045@{#349}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/158e171a33d35dc443f9e42dbf5c536aeb72fb83/chrome/browser/ui/views/profiles/profile_picker_view_browsertest.cc
[modify] https://crrev.com/158e171a33d35dc443f9e42dbf5c536aeb72fb83/chrome/browser/ui/webui/signin/profile_picker_handler.h
[modify] https://crrev.com/158e171a33d35dc443f9e42dbf5c536aeb72fb83/chrome/browser/ui/webui/signin/profile_picker_handler.cc


### am...@google.com (2023-10-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### no...@ssd-disclosure.com (2023-11-26)

Hi,

Can you please fix the credit to:
Minchin Park

Please don't use "Dohyun Lee (@l33d0hyun)" as the default as it is incorrect

### am...@chromium.org (2023-11-29)

Hi, thanks for letting us know. The security fix announcement has been updated to reflect this change: https://chromereleases.googleblog.com/2023/10/stable-channel-update-for-desktop_31.html

Since there are different individuals being credited from a single account, I've updated our database to reflect SSD Labs Korea as the public entry to be associated for accounts from this email address. We'll try to keep an eye out for individual names to be added to that for acknowledgement for future issues. 

### no...@ssd-disclosure.com (2023-11-29)

[Comment Deleted]

### no...@ssd-disclosure.com (2023-11-29)

The credit should be:
***Minchan Park***

You wrote:
***Minchin Lee***

### [Deleted User] (2024-01-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1488267?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40934491)*
