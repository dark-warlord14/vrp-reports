# Security: Heap-use-after-free in SavedTabGroupButton::MoveGroupToNewWindowPressed

| Field | Value |
|-------|-------|
| **Issue ID** | [40063876](https://issues.chromium.org/issues/40063876) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2023-04-03 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

commit at 7c1556f35c5205157de0a2ac2d2edb7194a00052

1. compile chromium on Mac with M1 chip, enable ASAN
2. Open chromium and save at least FIVE tabGroups, this will show the overflow menu in the bookmark bar
3. run `./asan-linux-release-1118297/chrome --user-data-dir=/tmp/noexist --enable-features=TabGroupsSave http://127.0.0.1:8605/poc.html`
4. open the savedTabgroup overflow menu and right-click to choose `open new tabgroup in new window`. On Mac with M1 chip, this overflow menu will not close, then right-click to choose `open new tabgroup in new window` again

## **Problem Description:**

**Additional Comments:**

1. Analysis

According to the ASAN log, the freed memory is a String, after I explore the source code, I find that in function `SessionIdGenerator::NewUnique`[1], as long as you refer to `local_state_`(even if just LOG it), here are some assembly code that will new a String as shown in ASAN log and then delete it[2].

But I don't figure out how this string is passed to the TabGroup and used in `TabGroupModel::GetTabGroup`[3].

```
SessionID SessionIdGenerator::NewUnique() {  
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);  
  // Init() should have been called in production (which initializes  
  // |local_state_|), but for test convenience, we allow operating even without  
  // underlying prefs.  
  if (local_state_) {  
    IncrementValueBy(1);  
    local_state_->SetInt64(kLastValuePref, last_value_);  
  } else {  
    // Test-only path. Will CHECK-fail if Init() is called later.  
    ++last_value_;  
  }  
  DCHECK(SessionID::IsValidValue(last_value_));  
  return SessionID::FromSerializedValue(last_value_);  
}  

```
```
   0x7fffd6ebacac <NewUnique()+588>:	mov    WORD PTR [r15+0x32],0x0  
   0x7fffd6ebacb3 <NewUnique()+595>:	mov    BYTE PTR [r15+0x34],0x0  
   0x7fffd6ebacb8 <NewUnique()+600>:	mov    edi,0x20  
   0x7fffd6ebacbd <NewUnique()+605>:	call   0x7fffd6ebc730 <_Znwm@plt>  // new a string here.  
......  
   0x7fffd6ebadc8 <NewUnique()+872>:	mov    rdi,QWORD PTR [r13+0x0]  
   0x7fffd6ebadcc <NewUnique()+876>:	call   0x7fffd6ebc790 <_ZdlPv@plt>  // delete the string   

```
```
TabGroup\* TabGroupModel::GetTabGroup(const tab_groups::TabGroupId& id) const {  
  DCHECK(ContainsTabGroup(id));  
  return groups_.find(id)->second.get(); //  freed string is used here.  
}  

```

Then I found the root cause maybe is that `local_group_id_`[4] in `SavedTabGroupButton::MoveGroupToNewWindowPressed` don't have a value even if we have clicked this button(Mac M1 sometimes will not close the overflow menu for some reason, so the overflow menu's status will also not be changed[5]). When we press `Open tabGroup in new window` again, `SavedTabGroupButton::MoveGroupToNewWindowPressed` will call `service_->OpenSavedTabGroupInBrowser(browser_with_local_group_id, guid_);` because the `local_group_id_` doesn't have value.

```
void SavedTabGroupButton::MoveGroupToNewWindowPressed(int event_flags) {  
  Browser\* const browser_with_local_group_id =  
      local_group_id_.has_value()  
          ? service_->listener()->GetBrowserWithTabGroupId(  
                local_group_id_.value())  
          : base::to_address(browser_);  
  
  if (!local_group_id_.has_value()) {  
    // Open the group in the browser the button was pressed.  
    service_->OpenSavedTabGroupInBrowser(browser_with_local_group_id, guid_);  
  }  
  
  // Move the open group to a new browser window.  
  const SavedTabGroup\* group = service_->model()->Get(guid_);  
  browser_with_local_group_id->tab_strip_model()  
      ->delegate()  
      ->MoveGroupToNewWindow(group->local_group_id().value());  
}  

```
```
void SavedTabGroupButton::UpdateButtonData(const SavedTabGroup& group) {  
  SetText(group.title());  
  SetTooltipText(group.title());  
  SetAccessibleName(group.title());  
  tab_group_color_id_ = group.color();  
  local_group_id_ = group.local_group_id();  
  guid_ = group.saved_guid();  
  tabs_.clear();  
  tabs_ = group.saved_tabs();  
  
  int button_height = GetLayoutConstant(BOOKMARK_BAR_BUTTON_HEIGHT);  
  if (GetText().empty()) {  
    // When the text is empty force the button to have square dimensions.  
    // Likewise, we already have a constant that denotes the standard button  
    // height for all elements in the bookmarks bar. As such, we will use this  
    // constant for the width of the button to create a square that will  
    // comfortably fit in the bookmarks bar.  
    SetPreferredSize(gfx::Size(button_height, button_height));  
  } else {  
    SetPreferredSize(CalculatePreferredSize());  
  }  
}  

```

I also try to comment out the `if(!local_group_id.has_value())` to test this issue on Linux, it can be triggered.  

If you want to repro this on Linux, try this patch:

```
diff --git a/chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_button.cc b/chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_button.cc  
index 350b2b743c9ba..917e7b7eef93b 100644  
--- a/chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_button.cc  
+++ b/chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_button.cc  
@@ -286,15 +286,16 @@ void SavedTabGroupButton::TabMenuItemPressed(const GURL& url, int event_flags) {  
   
 void SavedTabGroupButton::MoveGroupToNewWindowPressed(int event_flags) {  
   Browser\* const browser_with_local_group_id =  
-      local_group_id_.has_value()  
-          ? service_->listener()->GetBrowserWithTabGroupId(  
-                local_group_id_.value())  
-          : base::to_address(browser_);  
+  //    local_group_id_.has_value()  
+  //        ? service_->listener()->GetBrowserWithTabGroupId(  
+  //              local_group_id_.value())  
+  //        : base::to_address(browser_);  
+           base::to_address(browser_);  
   
-  if (!local_group_id_.has_value()) {  
+  //if (!local_group_id_.has_value()) {  
     // Open the group in the browser the button was pressed.  
     service_->OpenSavedTabGroupInBrowser(browser_with_local_group_id, guid_);  
-  }  
+  //}  
   
   // Move the open group to a new browser window.  
   const SavedTabGroup\* group = service_->model()->Get(guid_);  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/sessions/core/session_id_generator.cc;l=69>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_group_model.cc;l=48;bpv=1;bpt=1>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_button.cc;l=294>  

[5] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_button.cc;l=145>

2. Bisect

This problem is introduced in this commit: adce575cb2e089a3a1c0d326db96ae16389fc525  

<https://chromium-review.googlesource.com/c/chromium/src/+/4237451>

This affects Canary 113.0.5656.0 and Dev 113.0.5668.0

\*\*Chrome version: \*\* 113.0.5656.0 \*\*Channel: \*\* Canary

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 26.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 12 B)
- [video.mov](attachments/video.mov) (video/quicktime, 4.2 MB)

## Timeline

### [Deleted User] (2023-04-03)

[Empty comment from Monorail migration]

### mp...@chromium.org (2023-04-03)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### dl...@chromium.org (2023-04-03)

Hello Hello, thanks for the bug!

I was not able to reproduce this on Linux 114.0.5686.0 dev, so I believe this is already fixed. When you get a chance, can you try the reproduction steps on that version and see if the issue still persists? (I don't have a Mac with an M1 chip readily availble D:) 

For context there was a change made in this CL [1] that closes the overflow menu when its respective browser is no longer active. This should prevent this bug from happening as you will need to reopen the overflow menu which should update the buttons contained inside, specifically, local_group_id_.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/4375218

 

### ad...@google.com (2023-04-03)

(I am a bot: this is an auto-cc on a security bug)

### me...@gmail.com (2023-04-04)

re https://crbug.com/chromium/1429999#c3:
Actually I test it on Mac M1 with version 114.0.5692.0 DEV, it can also repro.

If you want to repro it on Linux, you should apply the patch as I mentioned.

For Mac, it does not need any patch to repro.


### dl...@chromium.org (2023-04-07)

Apologies for the delayed response!

Applying your patch I was able to reproduce the issue, and this makes sense because the group we are trying to open is already open when we go back to the first browser.

I was able to test this on a Mac M1 device and was still not able to reproduce this because the menu closes once the browser it is open in loses focus. This means we will need to reopen the menu preventing the stale data seen in the attached video and in the analysis (very good analysis by the way!).

I wonder if the patch in https://crbug.com/chromium/1429999#c3 had not landed on the dev version used to reproduce the uaf in https://crbug.com/chromium/1429999#c5. Can you try updating the dev browser and try to reproduce this again?

Thank you!

### me...@gmail.com (2023-04-10)

re https://crbug.com/chromium/1429999#c6:
I test it with the patch in https://crbug.com/chromium/1429999#c3, but it is still reproducible.

### me...@gmail.com (2023-04-19)

PING~

### dl...@chromium.org (2023-04-19)

Oops! A little swamped, will take a look on Friday. Sorry!

### dl...@chromium.org (2023-04-21)

Update: I was able to get the overflow menu to stay open after triggering MoveGroupToNewWindow. Meaning this bug is valid and my patch in https://crbug.com/chromium/1429999#c3 does not prevent this. My fault.

I won't be able to fix this today but will keep it top of mind going into next week. My current thoughts are that we need to change what view has ownership over the overflow menu so we can more easily manage when to close the menu. I will still need to think about what this will look like, and research into which observer functions we can use before I can begin implementing.

I want to say there is an obvious solution here but I haven't thought of one.

### me...@gmail.com (2023-05-25)

any update?

### dl...@chromium.org (2023-05-25)

Sorry! I have not gotten a chance to work on this one (I may un-assign myself), but we have run into a similar bug on windows where deleting a group in the overflow menu doesn't refresh the menu causing a similar UAF when you try to interact with the button.

I will pick this back up once I get a few other tasks done first and no one has picked this up before then.

Sorry again!



### dp...@chromium.org (2023-05-25)

adding tbergquist@ as an owner since they are also involved with implementation to see if they can you help with this security bug.

### gi...@appspot.gserviceaccount.com (2023-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d2251d4f11f5d5f795b6590bdb058b58eeb0ebb1

commit d2251d4f11f5d5f795b6590bdb058b58eeb0ebb1
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Thu May 25 21:58:47 2023

[Saved Tab Groups] Change when the STG bar overflow menu is closed.

Two changes:
- Close the overflow menu when the model changes. This fixes a crash when interacting with a button whose group has been removed from the model.
- Don't automatically close the overflow menu during a drag session. This may fix an issue where a saved tab group button drag is canceled on Windows when dragging a button out of the overflow menu.

Bug: 1429999,1448342
Change-Id: I76619de88364e33c2470a2f3f2a7376cef809691
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4569024
Reviewed-by: Darryl James <dljames@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1149394}

[modify] https://crrev.com/d2251d4f11f5d5f795b6590bdb058b58eeb0ebb1/chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_bar.cc


### me...@gmail.com (2023-05-29)

Hi, can we mark this as fixed? I've verified that it is no longer reproducible.

### dp...@chromium.org (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### me...@gmail.com (2023-06-25)

Hello, any updates about the reward?

### am...@google.com (2023-06-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-27)

Congratulations, Krace! The VRP Panel has decided to award you $2,000 for this report of heavily mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### me...@gmail.com (2023-06-28)

Thank you.

### am...@google.com (2023-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-06)

This issue was migrated from crbug.com/chromium/1429999?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063876)*
