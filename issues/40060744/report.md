# Security: UAF in CompoundTabContainer

| Field | Value |
|-------|-------|
| **Issue ID** | [40060744](https://issues.chromium.org/issues/40060744) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip |
| **Platforms** | Windows |
| **Reporter** | le...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2022-09-01 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

If enable the `SplitTabStrip` feature, the TabStrip will use CompoundTabContainer rather than TabContainerImpl as tab container[1].

CompoundTabContainer will use different TabContainerImpl for pinned tabs and unpinned tabs[2].

```
CompoundTabContainer::CompoundTabContainer(  
    const raw_ref<TabContainerController> controller,  
    TabHoverCardController\* hover_card_controller,  
    TabDragContextBase\* drag_context,  
    TabSlotController& tab_slot_controller,  
    views::View\* scroll_contents_view)  
    : controller_(controller),  
      pinned_tab_container_controller_(  
          std::make_unique<PinnedTabContainerController>(controller)),  
      pinned_tab_container_(\*AddChildView(std::make_unique<TabContainerImpl>(   <<------- pinned_tab_container_  
          \*(pinned_tab_container_controller_.get()),  
          hover_card_controller,  
          drag_context,  
          tab_slot_controller,  
          scroll_contents_view))),  
      unpinned_tab_container_controller_(  
          std::make_unique<UnpinnedTabContainerController>(controller)),  
      unpinned_tab_container_(\*AddChildView(std::make_unique<TabContainerImpl>( <<------- unpinned_tab_container_  
          \*(unpinned_tab_container_controller_.get()),  
          hover_card_controller,  
          drag_context,  
          tab_slot_controller,  
          scroll_contents_view))) {  

```

When a tab changes from unpinned to pinned[3], the `slots_`[4] of the `pinned_tab_container` will insert this tab slot, but the `slots_` of the `unpinned_tab_container` will not erase this slot while just set the slot state to kClosed[5].

```
void CompoundTabContainer::SetTabPinned(int model_index, TabPinned pinned) {  
  if (pinned == TabPinned::kPinned) {  
    CHECK_EQ(model_index, NumPinnedTabs());  
    std::unique_ptr<Tab> tab = unpinned_tab_container_->TransferTabOut(0);  
    pinned_tab_container_->AddTab(std::move(tab), model_index, pinned);  
  } else {  
    CHECK_EQ(model_index, NumPinnedTabs() - 1);  
    std::unique_ptr<Tab> tab =  
        pinned_tab_container_->TransferTabOut(model_index);  
    unpinned_tab_container_->AddTab(std::move(tab), 0, pinned);  
  }  
  
  Layout();  
}  
  
void TabStripLayoutHelper::RemoveTabAt(int model_index, Tab\* tab) {  
  const int slot_index = GetSlotIndexForExistingTab(model_index);  
  slots_[slot_index].state =  
      slots_[slot_index].state.WithOpen(TabOpen::kClosed);   <<------- [5]  
}  

```

At this point, when the tab destructed, only the `pinned_tab_container` where the view is located will be notified[6] and erase the slot from its `slots_`[7].

The UAF will be triggered when the dangling view pointer saved in the `slots_` of the `unpinned_tab_container` gets access[8].

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/tab_strip.cc;l=138;drc=9adeb2978b5af805032f756fa005f64421b56e82>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/compound_tab_container.cc;l=156;drc=9adeb2978b5af805032f756fa005f64421b56e82>

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/compound_tab_container.cc;l=228;bpv=1;bpt=0;drc=9adeb2978b5af805032f756fa005f64421b56e82>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/tab_strip_layout_helper.h;l=164;drc=2b680639853c40e13f5a78901a354146a864541a>  

[5]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/tab_strip_layout_helper.cc;l=119;drc=2b680639853c40e13f5a78901a354146a864541a>

[6]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/animation/bounds_animator.cc;l=287;drc=4b1c308a1fc5e7d63663059107d69e044cfa30a2>  

[7]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/tab_strip_layout_helper.cc;l=128;drc=2b680639853c40e13f5a78901a354146a864541a>  

[8]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/tabs/tab_strip_layout_helper.cc;l=274;drc=2b680639853c40e13f5a78901a354146a864541a>

**VERSION**

Test in win.

Head with SplitTabStrip feature.

Bisect:  

<https://source.chromium.org/chromium/chromium/src/+/9adeb2978b5af805032f756fa005f64421b56e82>

**REPRODUCTION CASE**

$ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-features=SplitTabStrip --load-extension="/path/to/extension”

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file.

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 33.8 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 212 B)
- [background.js](attachments/background.js) (text/plain, 443 B)
- [asan.log](attachments/asan.log) (text/plain, 19.2 KB)

## Timeline

### bo...@chromium.org (2022-09-01)

Confirming I can reproduce on Windows@107/canary. Non-standard flag required, so Security_Impact-None. Medium severity due to non-standard flag. 

Note exploitation of this bug should be prevented by MiraclePtr on platforms where it is available. The intent is to eventually downgrade such reports into a normal (non-security) bug, but for now we are ignoring the MiraclePtr mitigation. 

If you were to submit additional analysis regarding MiraclePtr bypasses or effectiveness then it would be regarded favorably during VRP review. 

[Monorail components: UI>Browser>TopChrome>TabStrip]

### ad...@google.com (2022-09-02)

(auto-cc on security bug)

### tb...@chromium.org (2022-09-06)

Thanks for the submission and the detailed repro! This could've been quite tricky to figure out.

The next steps here would likely be to add a TransferTabOut-analogous method to TabStripLayoutHelper for use by TabContainerImpl::TransferTabOut. And probably rename RemoveTabAt to make it more clear that it does no actual removing of tabs :)

For adetaylor@, bookholt@, whoever it might concern - I wasn't concerned with CompoundTabContainer's memory safety since I'm working behind a feature flag. Is that reasonable, and if no, how should I protect it so I can iterate on it without needing to worry about security implications of doing so? NB I only need the flag to be in the chrome://flags UI for convenience of sharing with cross-functional folks, so maybe making it command line only would help?

### [Deleted User] (2022-09-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6002da3a80200ff7e69bd617ed5dad12f70905fa

commit 6002da3a80200ff7e69bd617ed5dad12f70905fa
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Tue Sep 13 22:20:17 2022

Actually remove tab from layout helper when transferring tabs out of a TabContainer.

Turns out TabStripLayoutHelper::RemoveTabAt only marked a tab as animating closed, instead of actually removing it. Renamed RemoveTabAt->MarkTabAsClosing and OnTabDestroyed->RemoveTab, then called the correct method for TransferTabOut's usecase.

This fixes a UAF in CompoundTabContainer when a tab is closed after being pinned or unpinned, because TransferTabOut left the tab behind in TabStripLayoutHelper::slots_, and that pointer didn't get cleaned up when the tab was later closed.

Bug: 1358870
Change-Id: I07781f04a45fba5459b966b966bff172b5248f01
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3885122
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: David Pennington <dpenning@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1046600}

[modify] https://crrev.com/6002da3a80200ff7e69bd617ed5dad12f70905fa/chrome/browser/ui/views/tabs/tab_strip_layout_helper.h
[modify] https://crrev.com/6002da3a80200ff7e69bd617ed5dad12f70905fa/chrome/browser/ui/views/tabs/tab_strip_layout_helper.cc
[modify] https://crrev.com/6002da3a80200ff7e69bd617ed5dad12f70905fa/chrome/browser/ui/views/tabs/tab_container_impl.cc


### tb...@chromium.org (2022-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations on another one leecraso and Guang Gong! The VRP Panel has decided to award you $7,000 for this report of a mildly mitigated security bug + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-12-22)

This issue was migrated from crbug.com/chromium/1358870?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1346023]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060744)*
