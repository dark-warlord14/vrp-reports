# Security: UAF in ViewsAXTreeManager

| Field | Value |
|-------|-------|
| **Issue ID** | [40058092](https://issues.chromium.org/issues/40058092) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | UI>Accessibility |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ks...@microsoft.com |
| **Created** | 2021-12-01 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

If the AccessibilityTreeForViews flag is enabled, an |ax\_tree\_manager\_| will be made based on the root\_view[1]. And in ViewsAXTreeManager, a callback function will be post into SequencedTaskRunner[2], it will finally call[3] |GetUniqueId()| and access the root\_view[4]. So, if this callback function is called after root\_view gets destroyed, it will trigger this uaf.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/view_accessibility.cc;l=74;drc=c952d4ee1621e7ffd1225550dfbf240984e1a11f>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/views_ax_tree_manager.cc;l=113;drc=0e45c020c43b1a9f6d2870ff7f92b30a2f03a458>

[3]. The call path is shown in asan:  

callback SerializeTreeUpdates => tree\_serializer\_.SerializeChanges => LeastCommonAncestor => tree\_->GetId => node->GetUniqueId()

[4]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_view_obj_wrapper.cc;l=83;drc=f89b12288a0c173460340fb5066ea9f71c4becc2>

Fix suggestion:

OnWidgetClosing should have responded to the event, but according to the log, it did not:

It seems that because different widgets correspond to the same root\_view, some widgets are not destroyed, but their root\_view has been destroyed.

The fix patch should make observations on other widgets corresponding to the root\_view.

void ViewsAXTreeManager::OnWidgetDestroyed(Widget\* widget) {  

LOG(ERROR)<<">> ViewsAXTreeManager::OnWidgetDestroyed "<<this<<" "<<widget\_;  

if (widget->is\_top\_level())  

views::WidgetAXTreeIDMap::GetInstance().RemoveWidget(widget);

widget\_ = nullptr;

void ViewsAXTreeManager::OnWidgetClosing(Widget\* widget) {  

LOG(ERROR)<<">> ViewsAXTreeManager::OnWidgetClosing "<<this<<" "<<widget\_;  

if (widget->is\_top\_level())  

views::WidgetAXTreeIDMap::GetInstance().RemoveWidget(widget);

widget\_ = nullptr;  

}

void ViewsAXTreeManager::SerializeTreeUpdates() {  

LOG(ERROR)<<">> ViewsAXTreeManager::SerializeTreeUpdates "<<this<<" "<<widget\_;

# [23536:12968:1201/233311.858:ERROR:views\_ax\_tree\_manager.cc(127)] >> ViewsAXTreeManager::OnWidgetClosing 000011C911CB8380 000011BF1209A580 [23536:12968:1201/233312.999:ERROR:views\_ax\_tree\_manager.cc(142)] >> ViewsAXTreeManager::SerializeTreeUpdates 000011C911B7FD80 000011BF11BF4A80 [23536:12968:1201/233313.378:ERROR:views\_ax\_tree\_manager.cc(142)] >> ViewsAXTreeManager::SerializeTreeUpdates 000011C911BA6C80 000011BF11CA6680 [23536:12968:1201/233313.437:ERROR:views\_ax\_tree\_manager.cc(118)] >> ViewsAXTreeManager::OnWidgetDestroyed 000011C911CB8380 0000000000000000 [23536:12968:1201/233313.440:ERROR:widget.cc(190)] >> ~Widget : 000011BF1209A580 [23536:12968:1201/233313.441:ERROR:root\_view.cc(214)] >> ~RootView : 000011C311ECB880 [23536:12968:1201/233313.441:ERROR:root\_view.cc(218)] >> ~RootView Done : 000011C311ECB880 [23536:12968:1201/233313.442:ERROR:widget.cc(210)] >> ~Widget Done : 000011BF1209A580 [23536:12968:1201/233313.446:ERROR:view\_accessibility.cc(70)] >> ViewAccessibility : 0000000000000000 [23536:12968:1201/233313.446:ERROR:view\_accessibility.cc(70)] >> ViewAccessibility : 0000000000000000 [23536:12968:1201/233313.446:ERROR:view\_accessibility.cc(70)] >> ViewAccessibility : 0000000000000000 [23536:12968:1201/233313.446:ERROR:view\_accessibility.cc(70)] >> ViewAccessibility : 0000000000000000 [23536:12968:1201/233313.447:ERROR:view\_accessibility.cc(70)] >> ViewAccessibility : 000011BF11BF4A80 [23536:12968:1201/233313.447:ERROR:view\_accessibility.cc(70)] >> ViewAccessibility : 000011BF11BF4A80 [23536:12968:1201/233313.448:ERROR:view\_accessibility.cc(70)] >> ViewAccessibility : 000011BF11BF4A80 [23536:12968:1201/233313.521:ERROR:views\_ax\_tree\_manager.cc(142)] >> ViewsAXTreeManager::SerializeTreeUpdates 000011C911B7FD80 000011BF11BF4A80

==23536==ERROR: AddressSanitizer: heap-use-after-free on address 0x11c311ecbad8 at pc 0x7ff90a2253da bp 0x004fc8bfbb60 sp 0x004fc8bfbba8

**VERSION**  

Chrome Version: stable with feature flag: AccessibilityTreeForViews  

Operating System: test in Linux & Win

**REPRODUCTION CASE**

$ ./out/xxxx/chrome --user-data-dir="/tmp/tt" --enable-features=AccessibilityTreeForViews --disable-popup-blocking "<http://localhost:8000/poc.html>"

\* --disable-popup-blocking is not a necessary condition, it is just to quickly trigger this bug.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 12.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 296 B)
- [poc.html](attachments/poc.html) (text/plain, 233 B)

## Timeline

### [Deleted User] (2021-12-01)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-12-01)

Hi niktar@: can you please take a look at this urgently?

This looks like a web-accessible UAF in the browser process, which is a critical security vulnerability*.

Feel free to re-assign as needed, but we need to make sure this is addressed ASAP. Thanks!


* I'm assuming that AccessibilityTreeForViews is enabled for, e.g., screen reader users. If that flag is purely still in development (i.e. it is never used by real users), then this would be Impact-None. It'd still be important to fix, but not an emergency. 

[Monorail components: UI>Accessibility]

### [Deleted User] (2021-12-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-12-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5697164216696832.

### jd...@chromium.org (2021-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-12-06)

It looks to me that AccessibilityTreeForViews is disabled by default. Setting this to Impact: None. Additionally, ClusterFuzz can't repro the bug, though that may just be that it's failing there.

aleventhal/nektar: can you please follow up on this report please?


### al...@chromium.org (2021-12-06)

[Empty comment from Monorail migration]

### ks...@microsoft.com (2021-12-06)

[Empty comment from Monorail migration]

### ks...@microsoft.com (2021-12-06)

Agreeing with the assessment that this isn't enabled for users so it should be fixed, but isn't an emergency. I'll get a fix in some time this week.

### [Deleted User] (2021-12-15)

Pri-0 bugs are critical regressions or serious emergencies, and this bug has not been updated in three days. Could you please provide an update, or adjust the priority to a more appropriate level if applicable?

If a fix is in active development, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ks...@microsoft.com (2021-12-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/53ce88e9970e693493a5085cdfe287bd8794aa37

commit 53ce88e9970e693493a5085cdfe287bd8794aa37
Author: Kurt Catti-Schmidt (SCHMIDT) <kschmi@microsoft.com>
Date: Sat Dec 18 09:59:36 2021

Clear Widgets without a root view from WidgetAXTreeIDMap

This bug manifests when a root view has been cleared, but the
Widget is still around. The simplest mitigation for this
scenario is to remove widgets from WidgetAXTreeIDMap when we detect
a null root view.

I was unable to come up with a reasonable way to add a reliable unit
test for this scenario. Widget::DestroyRootViewAny is protected and
deprecated. Any ideas would be appreciated!

Bug: 1275600
Change-Id: I71d8ed42c71bc6f2184d1650e8ddc6870caf20db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3346380
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Commit-Queue: Kurt Catti-Schmidt <kschmi@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#952732}

[modify] https://crrev.com/53ce88e9970e693493a5085cdfe287bd8794aa37/ui/views/accessibility/views_ax_tree_manager.cc


### ks...@microsoft.com (2021-12-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-19)

[Empty comment from Monorail migration]

### le...@gmail.com (2021-12-20)

Thanks for your handle, but unfortunately this uaf could still trigger. The root cause is `ViewsAXTreeManager::OnViewEvent` will create a wrapper[1] for the view, and save its AXNodeID into `modified_nodes_`. When executing the callback function `SerializeTreeUpdates`, modified_nodes_ will be visited to read the AXNodeID to get the wrapper[2], and finally access the view saved in the wrapper[3]. The view has been destroyed, but the `cache_` and `modified_nodes_` are not cleaned up, which finnally leads to this UAF.

[1]. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/views_ax_tree_manager.cc;l=104;drc=53ce88e9970e693493a5085cdfe287bd8794aa37
[2]. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/views_ax_tree_manager.cc;l=157;drc=53ce88e9970e693493a5085cdfe287bd8794aa37
[3]. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_view_obj_wrapper.cc;l=83;drc=f89b12288a0c173460340fb5066ea9f71c4becc2

### le...@gmail.com (2021-12-20)

After some debugging, I found that the cause of the bug is:

During `AXAuraObjCache::CreateInternal`[1], `GetUniqueId`[2] may do some create and finally call `NotifyViewEvent`. So `OnViewEvent` will get a response again, and finally call `CreateInternal`[1] again. If there is no content with the key `aura_view` stored in `aura_view_to_id_map` at this time, a new key-value pair will be created and stored into `aura_view_to_id_map`.

And after `GetUniqueId`, it will back to the code `(*aura_view_to_id_map)[aura_view] = id;`[5]. Although `(*aura_view_to_id_map)[aura_view]` already has an `id` at this time, it will still be modified to a new `id`. But at this time, the `wrapper` corresponding to the old `id` is still stored in `cache_`.
y
This eventually leads to that:

After the destruction of the view observed by this wrapper, `OnViewIsDeleting`[6] will be called. However, since the old id is no longer stored in `aura_view_to_id_map`, its corresponding wrapper in `cache_` cannot be cleaned up[7], which finally leads to the result described in #17 and the uaf.

[1]. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_aura_obj_cache.cc;l=301;drc=53ce88e9970e693493a5085cdfe287bd8794aa37
[2]. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_aura_obj_cache.cc;l=313;drc=53ce88e9970e693493a5085cdfe287bd8794aa37
[3]. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_event_manager.cc;l=30;drc=53ce88e9970e693493a5085cdfe287bd8794aa37
[4]. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/views_ax_tree_manager.cc;l=102;drc=53ce88e9970e693493a5085cdfe287bd8794aa37
[5]. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_aura_obj_cache.cc;l=314;drc=53ce88e9970e693493a5085cdfe287bd8794aa37
[6]. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_view_obj_wrapper.cc;l=94;drc=53ce88e9970e693493a5085cdfe287bd8794aa37
[7]. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_aura_obj_cache.cc;l=338;drc=53ce88e9970e693493a5085cdfe287bd8794aa37


The following patch works, but it seems there can be a more elegant way.

diff --git a/ui/views/accessibility/ax_aura_obj_cache.cc b/ui/views/accessibility/ax_aura_obj_cache.cc
index c1b8a6bbead..8a3b61ef639 100644
--- a/ui/views/accessibility/ax_aura_obj_cache.cc
+++ b/ui/views/accessibility/ax_aura_obj_cache.cc
@@ -311,6 +320,10 @@ AXAuraObjWrapper* AXAuraObjCache::CreateInternal(

   auto wrapper = std::make_unique<AuraViewWrapper>(this, aura_view);
   ui::AXNodeID id = wrapper->GetUniqueId();
+
+  if ((*aura_view_to_id_map)[aura_view] != ui::kInvalidAXNodeID)
+    cache_.erase((*aura_view_to_id_map)[aura_view]);
+
   (*aura_view_to_id_map)[aura_view] = id;
   cache_[id] = std::move(wrapper);
   return cache_[id].get();

### am...@chromium.org (2022-01-05)

reopening based on https://crbug.com/chromium/1275600#c17 that this UAF can still be triggered; kschmi@ would you PTAL, since this code isn't presently enabled for users, certainly not critical to address right away, but definitely want to make sure this is fully resolved before we close this issue out completely. Thank you! 

### le...@gmail.com (2022-01-14)

Hi kschmi@, friendly ping, any updates about these issues? If there are any questions, please feel free to contact me.

### do...@chromium.org (2022-01-18)

Sheriff ping on this: can we please get some attention on this issue. We cannot enable the AccessibilityTreeForViews feature with this bug still open, and the reporter has kindly provided a code snippet that may address the issue.

### ks...@microsoft.com (2022-01-19)

Apologies for the delay. I'll try to get fixes for this and 1281808 in this week. This feature isn't enabled beyond users manually specifying the flag, and isn't on our schedule for release this quarter.

### le...@gmail.com (2022-01-28)

Sorry to bother, but it seems this issue hasn't been updated in a while, is there anything I can do to help? 

### me...@chromium.org (2022-02-01)

kschmi: Friendly security sheriff ping. Have you had a chance to land the fixes? Thanks!

### le...@gmail.com (2022-02-04)

Seems the owner doesn't have time to fix these issues, maybe assigning to someone else is a more appropriate choice

### am...@chromium.org (2022-02-10)

Hi, kschmi@, I understand that you may have fixes in flight for some of these AccessibilityTreeForViews. We understand that this feature isn't going to be enabled until next quarter at the earliest, but just wanted to check in on a potential ETA on when these fixes may land. Even if you don't have an exact date, would you mind setting the Next Action to a date in the future as a ballpark ETA/ with a note to help you avoid more pings from us security sheriffs/marshals? :) Thank you!

### ks...@microsoft.com (2022-02-18)

I started on this, but will be out tomorrow and Monday. I should be able to land this by next Friday.

### le...@gmail.com (2022-02-25)

[Comment Deleted]

### le...@gmail.com (2022-02-25)

Hi kschmi@, I noticed that you are working on fixing this lately, but there seem to be some errors in crrev.com/c/3489148:

As mentioned in https://crbug.com/chromium/1275600#c18, the newly added check code in the patch should be after the `GetUniqueId` function call rather than the `find` call.

diff --git a/ui/views/accessibility/ax_aura_obj_cache.cc b/ui/views/accessibility/ax_aura_obj_cache.cc
index c1b8a6bbead..8a3b61ef639 100644
--- a/ui/views/accessibility/ax_aura_obj_cache.cc
+++ b/ui/views/accessibility/ax_aura_obj_cache.cc
@@ -311,6 +320,10 @@ AXAuraObjWrapper* AXAuraObjCache::CreateInternal(

   auto wrapper = std::make_unique<AuraViewWrapper>(this, aura_view);
   ui::AXNodeID id = wrapper->GetUniqueId();      <<<<<--------------------- check should after this
+
+  if ((*aura_view_to_id_map)[aura_view] != ui::kInvalidAXNodeID)
+    cache_.erase((*aura_view_to_id_map)[aura_view]);
+
   (*aura_view_to_id_map)[aura_view] = id;
   cache_[id] = std::move(wrapper);
   return cache_[id].get();


It is because `GetUniqueId` will do some create and call `NotifyViewEvent`, and finally call `CreateInternal` again to store a new key-value pair into `aura_view_to_id_map`. 
And after the function `GetUniqueId` is called, it will return to `(*aura_view_to_id_map)[aura_view] = id;` to continue execution. At this point, the key-value pair of the current id already exists in `aura_view_to_id_map`, therefore a check is required here.

And if you still cannot be able to reproduce this locally, you can try this new poc:

$ ./out/xxxx/chrome --user-data-dir="/tmp/tt" --enable-features=AccessibilityTreeForViews --disable-popup-blocking "http://localhost:8000/poc.html"

### le...@gmail.com (2022-02-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/08ba9f8c7e85e3eb0fe0ef613f3aafa9fcf6a4aa

commit 08ba9f8c7e85e3eb0fe0ef613f3aafa9fcf6a4aa
Author: Kurt Catti-Schmidt (SCHMIDT) <kschmi@microsoft.com>
Date: Fri Mar 04 19:58:07 2022

UAF in ViewsAXTreeManager follow up

This is a follow-up to
https://chromium-review.googlesource.com/c/chromium/src/+/3346380
...in which I added some null checks that fixed the UAF locally.

The bug opener indicated that this UAF can still be hit after that change. They
have provided several excellent repro's that will trigger it.

The core of the issue here is that the 'LoadComplete' event that gets fired upon
construction of ViewsAXTreeManager cannot be fired synchronously, as the
AXAuraObjectCache has not added the wrapper from the cache at that point.

This trimmed call stack demonstrates the issue :

00 ViewAccessibility::ViewAccessibility view: 0x1cdea37b220
01 ViewAXPlatformNodeDelegate::ViewAXPlatformNodeDelegate
...
04 ViewAccessibility::Create
05 View::GetViewAccessibility
06 AXViewObjWrapper::GetUniqueId
...
08 AXAuraObjCache::GetOrCreate
09 ViewsAXTreeManager::OnViewEvent
0a AXEventManager::NotifyViewEvent
0b View::NotifyAccessibilityEvent (LoadComplete)
0c ViewsAXTreeManager::ViewsAXTreeManager
...
0e ViewAccessibility::ViewAccessibility this: view: 0x1cdea37b220
0f ViewAXPlatformNodeDelegate::ViewAXPlatformNodeDelegate
...
12 ViewAccessibility::Create
13 View::GetViewAccessibility
14 AXViewObjWrapper::GetUniqueId
15 AXAuraObjCache::CreateInternal<views::AXViewObjWrapper,views::View>
16 AXAuraObjCache::GetOrCreate
17 ViewsAXTreeManager::OnViewEvent
...
21 Widget::Init

Reading from the bottom up, you can see the expected 'ViewAccessibility::Create'
call upon creating the root Widget. However, on frame 0b,
View::NotifyAccessibilityEvent (LoadComplete) calls into
AXViewObjWrapper::GetUniqueId, which creates *another* ViewAccessibility, for
the same View as above (in this case, 0x1cdea37b220). There should never be
two ViewAccessibility nodes for the same view, and why the UAF is possible.

My fix here is to simply fire LoadComplete asynchronously. That allows the stack
to unwind such that the first call to |AXAuraObjCache::GetOrCreate| adds the
wrapper to the cache, so when LoadComplete is finally called, it is able to
retrieve it instead of creating a second one.

A unit test and DCHECK were added to enforce this. The unit test hits the
DCHECK without the asynchronous LoadComplete.

Bug: 1275600
Change-Id: I17ee35c26af95a3ba79a79da75107087c767eef2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3489148
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Commit-Queue: Kurt Catti-Schmidt <kschmi@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#977783}

[modify] https://crrev.com/08ba9f8c7e85e3eb0fe0ef613f3aafa9fcf6a4aa/ui/views/accessibility/views_ax_tree_manager.h
[modify] https://crrev.com/08ba9f8c7e85e3eb0fe0ef613f3aafa9fcf6a4aa/ui/views/accessibility/ax_aura_obj_cache_unittest.cc
[modify] https://crrev.com/08ba9f8c7e85e3eb0fe0ef613f3aafa9fcf6a4aa/ui/views/accessibility/ax_aura_obj_cache.cc
[modify] https://crrev.com/08ba9f8c7e85e3eb0fe0ef613f3aafa9fcf6a4aa/ui/views/accessibility/views_ax_tree_manager_unittest.cc
[modify] https://crrev.com/08ba9f8c7e85e3eb0fe0ef613f3aafa9fcf6a4aa/ui/views/accessibility/views_ax_tree_manager.cc


### le...@gmail.com (2022-03-08)

Great patch, it works well in my local test. I think this issue could be marked as fixed.

### ad...@google.com (2022-03-17)

Thanks both. Marking as fixed + verified.

### am...@google.com (2022-03-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-23)

Congratulations, leecraso and Guang Gong - the VRP Panel has decided to award you $20,000 for this report! Thank you for efforts and excellent work! 

### am...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### gm...@google.com (2022-04-04)

[Empty comment from Monorail migration]

### vo...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### vo...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-05)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2022-04-05)

1. https://crrev.com/c/3489148 and https://crrev.com/c/3346380
2. Low - not very big changes and no conflicts
3. only M101
4. Yes

### gm...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cc7709952bf1883d1a9d38318334605e90a2008f

commit cc7709952bf1883d1a9d38318334605e90a2008f
Author: Zakhar Voit <voit@google.com>
Date: Wed Apr 06 12:13:44 2022

[M96-LTS] UAF in ViewsAXTreeManager follow up

This is a follow-up to
https://chromium-review.googlesource.com/c/chromium/src/+/3346380
...in which I added some null checks that fixed the UAF locally.

The bug opener indicated that this UAF can still be hit after that change. They
have provided several excellent repro's that will trigger it.

The core of the issue here is that the 'LoadComplete' event that gets fired upon
construction of ViewsAXTreeManager cannot be fired synchronously, as the
AXAuraObjectCache has not added the wrapper from the cache at that point.

This trimmed call stack demonstrates the issue :

00 ViewAccessibility::ViewAccessibility view: 0x1cdea37b220
01 ViewAXPlatformNodeDelegate::ViewAXPlatformNodeDelegate
...
04 ViewAccessibility::Create
05 View::GetViewAccessibility
06 AXViewObjWrapper::GetUniqueId
...
08 AXAuraObjCache::GetOrCreate
09 ViewsAXTreeManager::OnViewEvent
0a AXEventManager::NotifyViewEvent
0b View::NotifyAccessibilityEvent (LoadComplete)
0c ViewsAXTreeManager::ViewsAXTreeManager
...
0e ViewAccessibility::ViewAccessibility this: view: 0x1cdea37b220
0f ViewAXPlatformNodeDelegate::ViewAXPlatformNodeDelegate
...
12 ViewAccessibility::Create
13 View::GetViewAccessibility
14 AXViewObjWrapper::GetUniqueId
15 AXAuraObjCache::CreateInternal<views::AXViewObjWrapper,views::View>
16 AXAuraObjCache::GetOrCreate
17 ViewsAXTreeManager::OnViewEvent
...
21 Widget::Init

Reading from the bottom up, you can see the expected 'ViewAccessibility::Create'
call upon creating the root Widget. However, on frame 0b,
View::NotifyAccessibilityEvent (LoadComplete) calls into
AXViewObjWrapper::GetUniqueId, which creates *another* ViewAccessibility, for
the same View as above (in this case, 0x1cdea37b220). There should never be
two ViewAccessibility nodes for the same view, and why the UAF is possible.

My fix here is to simply fire LoadComplete asynchronously. That allows the stack
to unwind such that the first call to |AXAuraObjCache::GetOrCreate| adds the
wrapper to the cache, so when LoadComplete is finally called, it is able to
retrieve it instead of creating a second one.

A unit test and DCHECK were added to enforce this. The unit test hits the
DCHECK without the asynchronous LoadComplete.

(cherry picked from commit 08ba9f8c7e85e3eb0fe0ef613f3aafa9fcf6a4aa)

Bug: 1275600
Change-Id: I17ee35c26af95a3ba79a79da75107087c767eef2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3489148
Commit-Queue: Kurt Catti-Schmidt <kschmi@microsoft.com>
Cr-Original-Commit-Position: refs/heads/main@{#977783}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3570852
Reviewed-by: Simon Hangl <simonha@google.com>
Owners-Override: Simon Hangl <simonha@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1571}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/cc7709952bf1883d1a9d38318334605e90a2008f/ui/views/accessibility/views_ax_tree_manager.h
[modify] https://crrev.com/cc7709952bf1883d1a9d38318334605e90a2008f/ui/views/accessibility/ax_aura_obj_cache_unittest.cc
[modify] https://crrev.com/cc7709952bf1883d1a9d38318334605e90a2008f/ui/views/accessibility/ax_aura_obj_cache.cc
[modify] https://crrev.com/cc7709952bf1883d1a9d38318334605e90a2008f/ui/views/accessibility/views_ax_tree_manager_unittest.cc
[modify] https://crrev.com/cc7709952bf1883d1a9d38318334605e90a2008f/ui/views/accessibility/views_ax_tree_manager.cc


### vo...@google.com (2022-04-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cf84a9f82611a5f1b32f2805d1d842cf3a3d48d8

commit cf84a9f82611a5f1b32f2805d1d842cf3a3d48d8
Author: Kurt Catti-Schmidt (SCHMIDT) <kschmi@microsoft.com>
Date: Wed Apr 06 15:02:44 2022

[M96-LTS] Clear Widgets without a root view from WidgetAXTreeIDMap

This bug manifests when a root view has been cleared, but the
Widget is still around. The simplest mitigation for this
scenario is to remove widgets from WidgetAXTreeIDMap when we detect
a null root view.

I was unable to come up with a reasonable way to add a reliable unit
test for this scenario. Widget::DestroyRootViewAny is protected and
deprecated. Any ideas would be appreciated!

(cherry picked from commit 53ce88e9970e693493a5085cdfe287bd8794aa37)

Bug: 1275600
Change-Id: I71d8ed42c71bc6f2184d1650e8ddc6870caf20db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3346380
Commit-Queue: Kurt Catti-Schmidt <kschmi@microsoft.com>
Cr-Original-Commit-Position: refs/heads/main@{#952732}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3571107
Reviewed-by: Simon Hangl <simonha@google.com>
Owners-Override: Simon Hangl <simonha@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1572}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/cf84a9f82611a5f1b32f2805d1d842cf3a3d48d8/ui/views/accessibility/views_ax_tree_manager.cc


### [Deleted User] (2022-06-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1275600?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058092)*
