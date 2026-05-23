# Security: UAF in FocusController::SetFocusedWindow

| Field | Value |
|-------|-------|
| **Issue ID** | [40058330](https://issues.chromium.org/issues/40058330) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | UI>Accessibility |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ks...@microsoft.com |
| **Created** | 2021-12-23 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

Sorry to interrupt the vacation again, but I found a new uaf while verifying my fix patch of 1275600. This uaf is irrelevant to 1275600, so please do not mark them as duplicates. Since it still needs to turn on the flag AccessibilityTreeForViews, it may not be so urgent, you can fix them after the holiday. And Merry Christmas in advance :)

There is a function `OnRootWindowObjCreated`[1] in `AXAuraObjCache` to observe new window creation. If the set `root_windows_` is empty, the function will add an observer for this window and insert this window into `root_windows_`. When `AXAuraObjCache` is destructed, its destructor will clean up the observer of window `\*root_windows_.begin()`[2]. These aim to only add and remove the observer for the first window in `root_windows_`. However, the use of insert and the sorting in the set `root_windows_` may lead to the unexpected fact:

1. First assume that it observe the creation of the first window: 0x56780, at this time the set `root_windows_` is empty, `OnRootWindowObjCreated` will add an observer for the client of window-0x56780 and insert <0x56780> into `root_windows_`.
2. And then assume that it observe the creation of the second window: 0x12340, at this time the set `root_windows_` is not empty, `OnRootWindowObjCreated` will not add an observer but will insert <0x12340> into `root_windows_`.
3. Since std::set is an ordered container, `root_windows_` will sort the stored windows according to their address value. If `AXAuraObjCache` is destroyed at this time, `\*root_windows_.begin()` is the second window window-0x12340, so the observer for the client of window-0x56780 will not be cleaned up.

Therefore, in the end, when traversing `focus_observers_`[3], the destructed `AXAuraObjCache` will be accessed, resulting in the UAF.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_aura_obj_cache.cc;l=280;drc=9356708a7b47760261c0f895d7fc6a5087f5b55b>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_aura_obj_cache.cc;l=201;drc=9356708a7b47760261c0f895d7fc6a5087f5b55b>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/wm/core/focus_controller.cc;l=288>

Fix suggestion:

Choose to use a sequenced container like vector, deque or list for that.

**VERSION**  

Chrome Version: stable with feature flag: AccessibilityTreeForViews  

Operating System: test in Linux & Win

**REPRODUCTION CASE**

$ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-features=AccessibilityTreeForViews --disable-popup-blocking "<http://localhost:8000/poc.html>"

Because it is necessary to ensure that the address value of the second window is smaller than the first window, the command --disable-popup-blocking aims to help repeated triggers to increase the success rate.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 13.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 824 B)
- poc2.html (text/plain, 55 B)

## Timeline

### [Deleted User] (2021-12-23)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-12-23)

Merry Christmas to you, too :) We're still here: the festive bug triage team. I've triaged this the same way as the other bug and since it's behind a flag right now it has SecurityImpact-None.

[Monorail components: UI>Accessibility]

### do...@chromium.org (2022-01-18)

Sheriff ping on this one: can we please get an update on when this might get looked at?

### al...@chromium.org (2022-01-19)

The feature won't be turned on until at least next quarter, and this will be looked at by @kschmi before that.

### am...@chromium.org (2022-02-10)

Hi, kschmi@, I understand that you may have fixes in flight for some of these AccessibilityTreeForViews. We understand that this feature isn't going to be enabled until next quarter at the earliest, but just wanted to check in on a potential ETA on when these fixes may land. Even if you don't have an exact date, would you mind setting the Next Action to a date at some point for a reminder/ with a note to help you avoid more pings from us security sheriffs/marshals? :) Thank you! 

### ks...@microsoft.com (2022-02-12)

I should have a fix ready on Monday

### le...@gmail.com (2022-02-18)

Friendly ping, any update?

### ks...@microsoft.com (2022-02-18)

I started on this, but will be out tomorrow and Monday. I should be able to land this by next Friday.

### le...@gmail.com (2022-02-18)

Fix suggestion:

diff --git a/ui/views/accessibility/ax_aura_obj_cache.cc b/ui/views/accessibility/ax_aura_obj_cache.cc
index af4c6b5c39686..6f3181e857ed5 100644
--- a/ui/views/accessibility/ax_aura_obj_cache.cc
+++ b/ui/views/accessibility/ax_aura_obj_cache.cc
@@ -280,11 +280,11 @@ void AXAuraObjCache::OnWindowFocused(aura::Window* gained_focus,
 void AXAuraObjCache::OnRootWindowObjCreated(aura::Window* window) {
   if (root_windows_.empty() && GetFocusClient(window))
     GetFocusClient(window)->AddObserver(this);
-  root_windows_.insert(window);
+  root_windows_.push_back(window);
 }
 
 void AXAuraObjCache::OnRootWindowObjDestroyed(aura::Window* window) {
-  root_windows_.erase(window);
+  root_windows_.erase(std::find(root_windows_.begin(), root_windows_.end(), window));
   if (root_windows_.empty() && GetFocusClient(window))
     GetFocusClient(window)->RemoveObserver(this);
 
diff --git a/ui/views/accessibility/ax_aura_obj_cache.h b/ui/views/accessibility/ax_aura_obj_cache.h
index db6c31a89d023..674e104894451 100644
--- a/ui/views/accessibility/ax_aura_obj_cache.h
+++ b/ui/views/accessibility/ax_aura_obj_cache.h
@@ -158,7 +158,7 @@ class VIEWS_EXPORT AXAuraObjCache : public aura::client::FocusChangeObserver {
 
   raw_ptr<Delegate> delegate_ = nullptr;
 
-  std::set<aura::Window*> root_windows_;
+  std::vector<aura::Window*> root_windows_;
 
   raw_ptr<aura::Window> focused_window_ = nullptr;
 


### gi...@appspot.gserviceaccount.com (2022-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dbaf781fd16ef36e84ce70572d3f31f30c91dbf1

commit dbaf781fd16ef36e84ce70572d3f31f30c91dbf1
Author: Kurt Catti-Schmidt (SCHMIDT) <kschmi@microsoft.com>
Date: Wed Mar 09 00:55:53 2022

Fix UAF in AXAuraObjCache destruction

AXAuraObjCache maintains a std::set to track root level windows as
|root_windows_|. This set uses pointers as a key, so it is sorted
by pointer address. Upon destruction of AXAuraObjCache, the
|begin_| element is accessed, which could be freed memory,
depending on the relative addresses of cache entries.

The fix is to convert |root_windows_| from a std::set to a
std::vector. Instead of accessing |begin_|, iterate and remove
any potential listeners. This also means iterating to access
elements of |root_windows_|, which changes access times from O(log(N))
to O(N). I do not anticipate this causing any performance issues
though, because top-level windows typically have a very small N.

A unit test was added under ax_aura_obj_cahe_unittest.cc that
simulates these conditions via manual memory management.

Bug: 1282384
Change-Id: Ic6e7cf4b39f1fb7ee18408e8a19245ef5e318c56
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3508957
Reviewed-by: David Tseng <dtseng@chromium.org>
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Commit-Queue: Kurt Catti-Schmidt <kschmi@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#978993}

[modify] https://crrev.com/dbaf781fd16ef36e84ce70572d3f31f30c91dbf1/ui/views/accessibility/ax_aura_obj_cache.h
[modify] https://crrev.com/dbaf781fd16ef36e84ce70572d3f31f30c91dbf1/ui/views/accessibility/ax_aura_obj_cache_unittest.cc
[modify] https://crrev.com/dbaf781fd16ef36e84ce70572d3f31f30c91dbf1/ui/views/accessibility/ax_aura_obj_cache.cc


### le...@gmail.com (2022-03-16)

The patch works well in my local test. I think this issue could be marked as fixed.

### ad...@google.com (2022-03-17)

Thanks kschmi@ and leecraso!

### [Deleted User] (2022-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-23)

Congratulations on another one! The VRP Panel has decided to award you $20,000 for this report. Thanks for another excellent report and nice work! 

### am...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### gm...@google.com (2022-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-06-23)

This issue was migrated from crbug.com/chromium/1282384?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058330)*
