# Security: UAF in AXVirtualViewWrapper

| Field | Value |
|-------|-------|
| **Issue ID** | [40058306](https://issues.chromium.org/issues/40058306) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Accessibility |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ks...@microsoft.com |
| **Created** | 2021-12-21 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**

In `AXVirtualViewWrapper`[1], there is no observing function like `OnViewIsDeleting()` in `AXViewObjWrapper`. Therefore, after `VirtualView` is destroyed, the wrapper stored in `cache_`[3] is not cleaned up. Finally, the destroyed `VirtualView` get used when traversing `cache_`[3] in the callback function `SerializeTreeUpdates`[4], which eventually leads to the uaf.

\*Note\*: This uaf is different from 1275600, please do not mark them as duplicates.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_virtual_view_wrapper.cc;l=16;drc=5a04092f83bd4d48d259d50ac0927613575009a4>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_view_obj_wrapper.cc;l=94;drc=f89b12288a0c173460340fb5066ea9f71c4becc2>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/views_ax_tree_manager.cc;l=157;drc=53ce88e9970e693493a5085cdfe287bd8794aa37>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/views_ax_tree_manager.cc;l=113;drc=ab7a15d89d306a247ae4db287b2455e492867c01>

Fix suggestion:

Add an observation function like `OnViewIsDeleting()` for `AXVirtualViewWrapper` to observe the destruction of `VirtualView`.

**VERSION**  

Chrome Version: stable with feature flag: AccessibilityTreeForViews  

Operating System: test in Linux & Win

**REPRODUCTION CASE**

$ ./out/xxxx/chrome --user-data-dir="/tmp/tt" --enable-features=AccessibilityTreeForViews "<http://localhost:8000/poc.html>"

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab

## Attachments

- [asan](attachments/asan) (text/plain, 12.9 KB)
- deleted (application/octet-stream, 0 B)
- [poc.html](attachments/poc.html) (text/plain, 379 B)
- [share.html](attachments/share.html) (text/plain, 119 B)

## Timeline

### [Deleted User] (2021-12-21)

[Empty comment from Monorail migration]

### le...@gmail.com (2021-12-21)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-12-21)

Thanks for the report. UAF in the browser process is critical, but it seems like there is some user interaction required, so downgrading by one level.

kschmi: Could you PTAL since you worked on https://crbug.com/chromium/1275600? Thanks.

[Monorail components: UI>Accessibility]

### do...@chromium.org (2022-01-18)

Sheriff ping: it looks like there are a lot of issues in the AccessibilityTreeForViews feature. Are there plans to launch this feature at any point?

### ks...@microsoft.com (2022-01-19)

This isn't planned to be released until at least next quarter. I realize the severity of these bugs and will try to get fixes in this week.

### am...@chromium.org (2022-02-10)

Hi, kschmi@, I understand that you may have fixes in flight for some of these AccessibilityTreeForViews. We understand that this feature isn't going to be enabled until next quarter at the earliest, but just wanted to check in on a potential ETA on when these fixes may land. Even if you don't have an exact date, would you mind setting the Next Action to a date in the future as a ballpark ETA/ with a note to help you avoid more pings from us security sheriffs/marshals? :) Thank you! 

### ks...@microsoft.com (2022-02-12)

I should have a fix ready on Monday

### ks...@microsoft.com (2022-02-18)

I started on this, but will be out tomorrow and Monday. I should be able to land this by next Friday.

### le...@gmail.com (2022-02-18)

Looking forward to the fix, and about the fix suggestion of this issue:

There is cleanup operation when `AXVirtualView` is destructed[1], but different `AXAuraObjCache` could focus on same `AXVirtualView`:

Cache1 => aura_view_to_id_map1 => AXVirtualViewWarper1 => focus on AXVirtualView1 => set `ax_aura_obj_cache_` to Cache1
Cache2 => aura_view_to_id_map2 => AXVirtualViewWarper2 => focus on AXVirtualView1 => set `ax_aura_obj_cache_` to Cache2

~AXVirtualView => ax_aura_obj_cache_->Remove(this) => cleanup the cache_ of Cache2

The `cache_` of Cache1 does not get cleaned up => access the destroyed `AXVirtualView` through the `cache_` of Cache1 causes the UAF.

So there are maybe two ways to make a fix:

1. Ensure that only one cache focuses on an `AXVirtualView`.
2. Add an observation function like `OnViewIsDeleting()` for `AXVirtualViewWrapper` to observe the destruction of `VirtualView` instead of cleanup the cache in `~AXVirtualView`.

[1]. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_virtual_view.cc;l=72;drc=04bcd29269bac41a91e087814d2368064e2b93d2
[2]. https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_aura_obj_cache.cc;l=176;drc=de533fceff84e830847b2a2bd66d017c06372d98

### gi...@appspot.gserviceaccount.com (2022-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a4cfa137aa73473116e817442406906a9c940fbd

commit a4cfa137aa73473116e817442406906a9c940fbd
Author: Kurt Catti-Schmidt (SCHMIDT) <kschmi@microsoft.com>
Date: Tue Mar 15 20:54:29 2022

Fix UAF in AXVirtualViewWrapper when added to multiple AXAuraObjCaches

This UAF can occur when a single AXVirtualView exists in two different
AXAuraObjCaches. I traced this down to |AXVirtualView::set_cache|
being called when an |ax_aura_obj_cache_| is already present.

Since it doesn't make sense for the same node to exist in two
caches, the fix here is to simply remove the AXVirtualView from
its existing |ax_aura_obj_cache_| (if present) before overwriting it.

A unit test was added that validates this behavior.

Bug: 1281808
Change-Id: I9670ef0e1dc955024e425e4547c463e4a032edad
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3517987
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Commit-Queue: Kurt Catti-Schmidt <kschmi@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#981308}

[modify] https://crrev.com/a4cfa137aa73473116e817442406906a9c940fbd/ui/views/accessibility/ax_virtual_view_unittest.cc
[modify] https://crrev.com/a4cfa137aa73473116e817442406906a9c940fbd/ui/views/accessibility/ax_virtual_view.h
[modify] https://crrev.com/a4cfa137aa73473116e817442406906a9c940fbd/ui/views/accessibility/ax_virtual_view.cc


### le...@gmail.com (2022-03-23)

The fix works well in the local test. This issue could be marked as fixed.

### ad...@google.com (2022-03-25)

Thanks leecraso@.

### ks...@microsoft.com (2022-03-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-11)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $15,000 for this report. Thanks for your efforts and great work! 

### am...@google.com (2022-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-07-05)

This issue was migrated from crbug.com/chromium/1281808?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058306)*
