# Security: ui::AXPlatformNodeWin Use-After-Free issue

| Field | Value |
|-------|-------|
| **Issue ID** | [41491428](https://issues.chromium.org/issues/41491428) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Accessibility, UI>Browser>Panels |
| **Platforms** | Windows |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ks...@microsoft.com |
| **Created** | 2024-01-15 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

## Root Case

### Alloc

When using customize chrome feature, the 'side panel' will be opened. The `SetCustomizeChromeSidePanelVisible` function will be called here:

```
void CustomizeChromeSidePanelController::SetCustomizeChromeSidePanelVisible(  
    bool visible,  
    CustomizeChromeSection section) {  
  auto\* side_panel_ui = GetSidePanelUI();  
  if (!side_panel_ui) {  
    return;  
  }  
  DCHECK(IsCustomizeChromeEntryAvailable());  
  if (visible) {  
    side_panel_ui->Show(SidePanelEntry::Id::kCustomizeChrome);  
    if (customize_chrome_ui_) {  
      customize_chrome_ui_->ScrollToSection(section);  
      section_.reset();  
    } else {  
      section_ = section;  
    }  
  } else {  
    side_panel_ui->Close();  
  }  
}  

```

SetCustomizeChromeSidePanelVisible proceeds to call SidePanelCoordinator. When SidePanelCoordinator executes the SidePanelWebUIView function and creates the view, it creates an \*AXPlatformNode\* object through ViewAXPlatformNodeDelegate.

```
AXPlatformNode\* AXPlatformNode::Create(AXPlatformNodeDelegate\* delegate) {  // <---------- [0]  
  // Make sure ATL is initialized in this module.  
  win::CreateATLModuleIfNeeded();  
  
  CComObject<AXPlatformNodeWin>\* instance = nullptr;  
  HRESULT hr = CComObject<AXPlatformNodeWin>::CreateInstance(&instance);  
  DCHECK(SUCCEEDED(hr));  
  instance->Init(delegate);  
  instance->AddRef();  
  return instance;  
}  

```
### Free

When you do not close customize chrome side panel and then create a new tab (NewTabButton::OnMouseReleased) or switch to another tab (TabStrip::SelectTab), \*View::~View\* will be triggered. Then call \*ui::AXPlatformNodeBase::Destroy\* through \*~ViewAXPlatformNodeDelegate\*.

```
void AXPlatformNodeBase::Destroy() {  
  g_unique_id_map.Get().erase(GetUniqueId());  
  AXPlatformNode::Destroy(); // <<---------- [1]  
  delegate_ = nullptr;  
  Dispose();  
}  

```
### Use

The UAF vulnerability occurs when UiaRaiseAutomationEvent is executed to \*ui::AXPlatformNodeWin::Navigate\*. [3]

[0] <https://source.chromium.org/chromium/chromium/src/+/main:ui/accessibility/platform/ax_platform_node_win.cc;drc=705ff26ec9a4b46193ba161c3e90d597acddefdd;l=308>  

[1] <https://source.chromium.org/chromium/chromium/src/+/main:ui/accessibility/platform/ax_platform_node_base.cc;drc=705ff26ec9a4b46193ba161c3e90d597acddefdd;l=448>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:ui/accessibility/platform/ax_platform_node_win.cc;drc=705ff26ec9a4b46193ba161c3e90d597acddefdd;l=5062>

### RECOMMENDED PATCH

I think that when fixing this issue, we can refer to the approach of patch [0] ?

[0] <https://chromium.googlesource.com/chromium/src/+/3186a0be55861e06ba8d8b89f4dd9ddadb829a27%5E%21/#F0>

**VERSION**  

Chrome Version: 122.0.6250.0  

Operating System: Windows 11

**REPRODUCTION CASE**

1. Click 'Customize this page' on tab
2. Click 'New Tab' (+ button) or switch other tab
3. Trigger UAF

**CREDIT INFORMATION**

Reporter credit: Zhenjiang Zhao of pangu team, Qianxin

## Attachments

- [repro-1-15.mp4](attachments/repro-1-15.mp4) (video/mp4, 4.1 MB)
- [UAF-2.asan](attachments/UAF-2.asan) (text/plain, 15.5 KB)

## Timeline

### [Deleted User] (2024-01-15)

[Empty comment from Monorail migration]

### sw...@gmail.com (2024-01-15)

add ASAN log

### za...@google.com (2024-01-17)

Hi jessemckenna@, can you please help take a look at this bug? Our reporter has attached detailed log and code pointers. Please feel free to reassign. Thank you.

[Monorail components: UI>Browser>Panels]

### [Deleted User] (2024-01-17)

[Empty comment from Monorail migration]

### je...@google.com (2024-01-17)

Looking now.

### je...@google.com (2024-01-18)

Status update: I haven't been able to repro this on my local build. I tried a regular build and ASAN build, but they both worked fine when opening or switching to another tab while the "customize Chrome" sidebar is open. I tried the exact version listed in the original bug too, just in case the issue was fixed in later versions, but still no dice.

Maybe it's racey - if so I may need to try inserting sleeps in certain places to force it to trigger. I'll try that next.

### [Deleted User] (2024-01-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### je...@google.com (2024-01-18)

Following up on my previous comment, I just realized that I'm not able to repro this because it requires UI automation - the ASAN log provided shows that the "use" part of the UAF happens when we receive a WM_GETOBJECT message, which is sent by Microsoft Active Accessibility and Microsoft UI Automation.

I don't have any means to repro UI automation bugs. aleventhal@: would you be able to assist with this bug?

[Monorail components: UI>Accessibility]

### al...@chromium.org (2024-01-18)

Ben, can someone from your team take a look?

### be...@microsoft.com (2024-01-18)

Yes, absolutely! This looks extremely similar to https://bugs.chromium.org/p/chromium/issues/detail?id=1456463, which we were blocked on for not having a repro case. This should make it super actionable!

Thank you for reporting sweetdewtemple@gmail.com, and thanks to Zhenjiang Zhao of pangu team, Qianxin!

+ Kurt, I think you're looking at something similar in Edge? Could it be related?

### ks...@microsoft.com (2024-01-18)

I can repro this! There are two prerequisites not listed above:

1. In Windows, enable Text Cursor Indicator (search windows settings for "Text Cursor Indicator")
2. Launch Chrome with --enable-features=UiaProvider

...then follow the repro steps above:

1. Click 'Customize this page' on tab
2. Click 'New Tab' (+ button) or switch other tab
3. Trigger UAF

Looking into a fix for this now.

### be...@microsoft.com (2024-01-18)

+1 on the additional repro steps.

UIA is currently enabled for 50% of Canary users, so we might need to force enable it if we want to be sure to reproduce.

The text cursor indicator is the "assistive technology", or more UIA client, that we were searching for. I cannot reproduce with Narrator.

### ks...@microsoft.com (2024-01-18)

I think I have a fix. I noticed that in the crashing case, GetDelegate() *is* a fragment root (in this case,  AXFragmentRootPlatformNodeWin)

Based on the documentation, in this case, we should be setting the out pointer as `nullptr` - "Because the implementing element is a fragment root, it does not enable navigation to a parent element or sibling elements." https://learn.microsoft.com/en-us/dotnet/api/system.windows.automation.provider.irawelementproviderfragment.navigate

Adding a check for this in AXPlatformNodeWin::Navigate fixes the repro crash:

  gfx::NativeViewAccessible neighbor = nullptr;
  switch (direction) {
    case NavigateDirection_Parent: {
      if (AXFragmentRootWin::GetForAcceleratedWidget(GetDelegate()->GetTargetForNativeAccessibilityEvent()) == GetDelegate()) {
         return S_OK;
      }

I need to do some more testing and research before I go with this route, but this looks like it could be the fix. Seems like this is only possible with Views objects, due to how the fragment roots are constructed.

### ha...@google.com (2024-01-19)

[Empty comment from Monorail migration]

### ks...@microsoft.com (2024-01-19)

I've found that the suggested fix in https://crbug.com/chromium/1518452#c15 isn't correct. It fixes the crash, but causes other issues. The quote from the documentation above isn't quite correct in all cases (including here), so it breaks tree navigation for popups (like the datetime pickers).

I dug in a bit deeper and found the real root cause:

NativeViewHostAura keeps track of an IAccessible object via:

void NativeViewHostAura::SetParentAccessible(
    gfx::NativeViewAccessible accessible) {
  host_->native_view()->SetProperty(
      aura::client::kParentNativeViewAccessibleKey, accessible);
}

...however, if the View heirarchy changes in such a way that the view owning the IAccessible is destroyed, the accessible object pointed to via kParentNativeViewAccessibleKey is now destoryed, so kParentNativeViewAccessibleKey is holding a weak reference to a dead object, hence the crash.

NativeViewHostAura::NativeViewDetaching clears this pointer, but NativeViewHostAura::RemovedFromWidget doesn't. There appears to be cases where a View gets destroyed (and hence the underlying IAccessible), but the NativeViewHostAura doesn't get detatched/destroyed.

Adding the following to NativeViewHostAura::RemovedFromWidget:

   host_->native_view()->ClearProperty(aura::client::kParentNativeViewAccessibleKey);

...also fixes this crash in a much safer way. However, it might break accessibility in certain conditions. So I'm going to dig into this a bit more and see where it can reset the right value.

### ks...@microsoft.com (2024-01-19)

Assigning this to myself

### gi...@appspot.gserviceaccount.com (2024-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2e0f9326cf8cc0fb7d02eb675e9c67356bcd99a1

commit 2e0f9326cf8cc0fb7d02eb675e9c67356bcd99a1
Author: Kurt Catti-Schmidt <kschmi@microsoft.com>
Date: Wed Jan 24 01:35:29 2024

[UIA] Clear accessible parent when a WebView is removed

This CL fixes a UAF in AXPlatformNodeWin::Navigate, when the
current node is an AXFragmentRoot and the direction is
NavigateDirection_Parent. In that case, the GetParent call ends up
in RenderWidgetHostViewAura::GetParentNativeViewAccessible, and
at that point, the NativeViewAccessible (IAccessible in this case) has
already been freed.

This is because NativeViewHostAura::RemovedFromWidget may end up keeping
the NativeViewHostAura alive but removing host_->native_view(), freeing
the ViewAccessibility object with it (which owns the IAccessible that
gets cleared here).

The general fix to this is to clear the parent accessible object
when a WebView is removed.

Bug: 1456463,1518452
Change-Id: Ib7ccaa7030dc98a0e6cc8a4e197b895c9048e49d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5214694
Commit-Queue: Kurt Catti-Schmidt <kschmi@microsoft.com>
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Benjamin Beaudry <benjamin.beaudry@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#1251174}

[modify] https://crrev.com/2e0f9326cf8cc0fb7d02eb675e9c67356bcd99a1/ui/views/controls/webview/webview.cc
[modify] https://crrev.com/2e0f9326cf8cc0fb7d02eb675e9c67356bcd99a1/ui/views/controls/webview/webview.h
[modify] https://crrev.com/2e0f9326cf8cc0fb7d02eb675e9c67356bcd99a1/ui/views/controls/webview/webview_unittest.cc


### ks...@microsoft.com (2024-01-24)

This is now fixed in Chrome Canary build 123.0.6262.0 (Official Build) canary (32-bit) (cohort: Clang-32) 

### ks...@microsoft.com (2024-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-25)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M122, which branched on 2024-01-22 (Chromium branch: 6261, Chromium branch position: 1250580)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gr...@chromium.org (2024-01-26)

the fix is now shipping to dev in 123.0.6262.5. i would like to merge r1251174 to 122 so that we can enable the UIAProvider study on beta channel sooner rather than later. as of this moment, there are no new crashes on canary or dev since the fix landed. i'll look again early next week to confirm.

### [Deleted User] (2024-01-26)

Merge approved: your change passed merge requirements and is auto-approved for M122. Please go ahead and merge the CL to branch 6261 (refs/branch-heads/6261) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-29)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2024-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f762b8aead8dae7c70ed1fb519ebe36cb8e9e9d2

commit f762b8aead8dae7c70ed1fb519ebe36cb8e9e9d2
Author: Kurt Catti-Schmidt <kschmi@microsoft.com>
Date: Tue Jan 30 09:58:48 2024

[UIA] Clear accessible parent when a WebView is removed

This CL fixes a UAF in AXPlatformNodeWin::Navigate, when the
current node is an AXFragmentRoot and the direction is
NavigateDirection_Parent. In that case, the GetParent call ends up
in RenderWidgetHostViewAura::GetParentNativeViewAccessible, and
at that point, the NativeViewAccessible (IAccessible in this case) has
already been freed.

This is because NativeViewHostAura::RemovedFromWidget may end up keeping
the NativeViewHostAura alive but removing host_->native_view(), freeing
the ViewAccessibility object with it (which owns the IAccessible that
gets cleared here).

The general fix to this is to clear the parent accessible object
when a WebView is removed.

(cherry picked from commit 2e0f9326cf8cc0fb7d02eb675e9c67356bcd99a1)

Bug: 1456463,1518452
Change-Id: Ib7ccaa7030dc98a0e6cc8a4e197b895c9048e49d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5214694
Commit-Queue: Kurt Catti-Schmidt <kschmi@microsoft.com>
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Benjamin Beaudry <benjamin.beaudry@microsoft.com>
Cr-Original-Commit-Position: refs/heads/main@{#1251174}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5240532
Reviewed-by: Nicola Tommasi <tommasin@chromium.org>
Commit-Queue: Nicola Tommasi <tommasin@chromium.org>
Commit-Queue: Greg Thompson <grt@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Nicola Tommasi <tommasin@chromium.org>
Auto-Submit: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/branch-heads/6261@{#261}
Cr-Branched-From: 9755d9d81e4a8cb5b4f76b23b761457479dbb06b-refs/heads/main@{#1250580}

[modify] https://crrev.com/f762b8aead8dae7c70ed1fb519ebe36cb8e9e9d2/ui/views/controls/webview/webview.cc
[modify] https://crrev.com/f762b8aead8dae7c70ed1fb519ebe36cb8e9e9d2/ui/views/controls/webview/webview.h
[modify] https://crrev.com/f762b8aead8dae7c70ed1fb519ebe36cb8e9e9d2/ui/views/controls/webview/webview_unittest.cc


### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations! The Chrome VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug, mitigated by race condition and user gesture. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1518452?no_tracker_redirect=1

[Multiple monorail components: UI>Accessibility, UI>Browser>Panels]
[Monorail components added to Component Tags custom field.]

### pg...@chromium.org (2024-03-29)

Removing incorrectly added label - this bug was fixed in head/Beta

### pe...@google.com (2024-05-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2024-05-20)

Hello reporter, we consider attachments/POCs included with reports to be an integral part of the report (<https://g.co/chrome/vrp>) -- especially when it is the original report itself, so I've restored the original report and the attachment. Please refrain from re-deleting them in the future.

### ni...@google.com (2024-06-18)

This issue seems to no longer be occurring. So I am marking as verified.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41491428)*
