# heap-use-after-free on FedCmAccountSelectionView::ShowDialogWidget

| Field | Value |
|-------|-------|
| **Issue ID** | [382399969](https://issues.chromium.org/issues/382399969) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 131.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | np...@google.com |
| **Created** | 2024-12-05 |
| **Bounty** | $36,000.00 |

## Description

# Steps to reproduce the problem

I'll take up some space for the report first. RCA analysis, bitset, and the fix patch will be uploaded tomorrow because it's a bit late now and I need to go to bed.

# Problem Description

I'll take up some space for the report first. RCA analysis, bitset, and patch will be uploaded tomorrow because it's a bit late now and I need to go to bed.

# Summary

heap-use-after-free on FedCmAccountSelectionView::ShowDialogWidget

# Custom Questions

#### Type of crash:

browser

#### Crash state:

see asan.log

#### Reporter credit:

lime(@limeSec\_)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [login.html](attachments/login.html) (text/html, 73 B)
- [poc.html](attachments/poc.html) (text/html, 701 B)
- [server.js](attachments/server.js) (text/javascript, 2.0 KB)
- [uaf16.log](attachments/uaf16.log) (text/plain, 160.6 KB)
- [poc1.mov](attachments/poc1.mov) (video/quicktime, 21.3 MB)
- [symbolized_stacktrace.txt](attachments/symbolized_stacktrace.txt) (text/plain, 164.5 KB)
- login.html (text/html, 73 B)
- poc.html (text/html, 710 B)
- server.js (text/javascript, 1.9 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 29.1 MB)
- [RCA.md](attachments/RCA.md) (text/markdown, 13.3 KB)
- [permissions_bypass](attachments/permissions_bypass) (application/octet-stream, 1.4 KB)
- [permissions_bypass.mov](attachments/permissions_bypass.mov) (video/quicktime, 17.8 MB)

## Timeline

### ja...@chromium.org (2024-12-05)

[security shepherd] Thanks for the report and the recording. I'm working on reproducing it.

### ja...@chromium.org (2024-12-05)

Using the poc on a developer build of Chrome I got:

```

[2295425:2295425:1205/123249.536845:INFO:CONSOLE(10)] "The 'mediation' parameter should be used outside of 'identity' in the FedCM API call.", source: http://localhost:8000/poc.html (10)
../../base/allocator/partition_allocator/src/partition_alloc/partition_address_space.h(89) PA_NOTREACHED() hit.

```

### ja...@chromium.org (2024-12-05)

This was on 133.0.6852.0 (Developer Build) unknown (64-bit)

### ja...@chromium.org (2024-12-05)

Hi erikchen@ I was able to reproduce this on M133. Can you take a look?

### ja...@chromium.org (2024-12-05)

Adding FedCM as the component. Looking for other owners.

### ja...@chromium.org (2024-12-05)

On second look, assigning to npm@ based on [crrev.com/c/5783631](https://crrev.com/c/5783631)

### ja...@chromium.org (2024-12-05)

Added a symbolized stack trace from chromium-133.0.6876.4

### ja...@chromium.org (2024-12-05)

Does not reproduce in: 130.0.6723.0 (Developer Build) custom (64-bit)

### li...@gmail.com (2024-12-05)

Hi @ja
I found and repro on commit `e32ea50c62`, I know the `Root cause`, and I will write the `RCA` soon. :)

### am...@chromium.org (2024-12-06)

hi lime, thanks for the report -- when you're available to do so, please provide clear steps to reproduce here. Setting needs-feedback to help denote that in our triage queue.
Looking at stack trace you've attached in your original report, it appears there are a number of command line flags that were used to get that outcome. It would would be helpful to know if those are all necessary as well as help assure we can effectively triage. Thanks!

### li...@gmail.com (2024-12-06)

##RCA:

0. When calling `ShowErrorDialog`, `RemoveNonHeaderChildViewsAndUpdateHeaderIfNeeded` will be called,

```
void AccountSelectionModalView::ShowErrorDialog(
    const std::u16string& idp_for_display,
    const content::IdentityProviderMetadata& idp_metadata,
    const std::optional<TokenError>& error) {
  RemoveNonHeaderChildViewsAndUpdateHeaderIfNeeded();

  std::u16string summary_text;
  std::u16string description_text;
  std::tie(summary_text, description_text) =
      GetErrorDialogText(error, rp_for_display_, idp_for_display);


```

1. Then the `child_views` of `AccountSelectionModalView` will be traversed. Except for `body_label_`, all other views will be deleted.

```
void AccountSelectionModalView::
    RemoveNonHeaderChildViewsAndUpdateHeaderIfNeeded() {
  // body_label_ does not apply to the loading modal so it's added to header
  // here.
  if (!body_label_) {
    body_label_ = header_view_->AddChildView(std::make_unique<views::Label>(
        l10n_util::GetStringUTF16(IDS_ACCOUNT_SELECTION_CHOOSE_AN_ACCOUNT),
        views::style::CONTEXT_DIALOG_BODY_TEXT, views::style::STYLE_BODY_4));
    SetLabelProperties(body_label_);
    body_label_->SetFocusBehavior(FocusBehavior::ALWAYS);
  }

  [...]

  const std::vector<raw_ptr<views::View, VectorExperimental>> child_views =
      children();
  for (views::View* child_view : child_views) {
    if (child_view != header_view_) {
      RemoveChildView(child_view);
      delete child_view;
    }
  }
}


```

2. Then finish running `AccountSelectionModalView::ShowErrorDialog`, and then run `FedCmAccountSelectionView::ShowErrorDialog`. If `tab_->IsInForeground() && CanFitInWebContents()` is satisfied, the Dialog Widget will be shown.

```
bool FedCmAccountSelectionView::ShowErrorDialog(
    const std::string& rp_for_display,
    const std::string& idp_etld_plus_one,
    blink::mojom::RpContext rp_context,
    blink::mojom::RpMode rp_mode,
    const content::IdentityProviderMetadata& idp_metadata,
    const std::optional<TokenError>& error) {
  [...]

  // If a modal dialog was created previously but there is no modal support for
  // this type of dialog, reset account_selection_view_ to create a bubble
  // dialog instead. We also reset for widget multi IDP to recalculate the title
  // and other parts of the header.
  if ((rp_mode == blink::mojom::RpMode::kPassive && idp_list_.size() > 1) ||
      (rp_mode == blink::mojom::RpMode::kActive && !has_modal_support)) {
    Close(/*notify_delegate=*/false);
  }

  bool create_view = !account_selection_view_;
  if (create_view) {
    CreateViewAndWidget(rp_for_display_, base::UTF8ToUTF16(idp_etld_plus_one),
                        rp_context, rp_mode, has_modal_support);
  }

  account_selection_view_->ShowErrorDialog(
      base::UTF8ToUTF16(idp_etld_plus_one), idp_metadata, error);
  UpdateDialogPositionIfModal();

  [...]

  if (tab_->IsInForeground() && CanFitInWebContents()) { //
    ShowDialogWidget();
  }
  // Else:
  // The dialog is not guaranteed to be shown. The dialog will be hidden if the
  // associated web contents are hidden.
  return true;
}


```

3. Then `GetDialogWidget()->Show()`; will be run.

```
void FedCmAccountSelectionView::ShowDialogWidget() {
  Browser* browser = chrome::FindBrowserWithTab(web_contents());
  if (browser &&
      browser->tab_strip_model()->GetActiveWebContents() != web_contents()) {
    // This is unexpected since we should never reach this codepath when the
    // WebContents is not the active one. Dump to get debug info on when this
    // happens.
    base::debug::DumpWithoutCrashing();
  }

  input_protector_->VisibilityChanged(true);
  GetDialogWidget()->Show();
  [...]

```

4. Because I have M3 Arm, I use mac’s NativeWidget, and then in SetInitialFocus

```
void NativeWidgetMac::Show(ui::mojom::WindowShowState show_state,
                           const gfx::Rect& restore_bounds) {
  [...]                         
  delegate_->SetInitialFocus(show_state);
}
---------------------------------------------------------------
bool Widget::SetInitialFocus(ui::mojom::WindowShowState show_state) {
  FocusManager* focus_manager = GetFocusManager();
  if (!focus_manager || !widget_delegate_)
    return false;
  View* v = widget_delegate_->GetInitiallyFocusedView(); //Get InitiallyFocusedView, but if we close the view initially, the view here is already in a hanging pointer state.
  if (!focus_on_creation_ ||
      show_state == ui::mojom::WindowShowState::kInactive ||
      show_state == ui::mojom::WindowShowState::kMinimized) {
    // If not focusing the window now, tell the focus manager which view to
    // focus when the window is restored.
    if (v)
      focus_manager->SetStoredFocusView(v); //pass pointer
    return true;
  } 
  [...]
}
--------------------------------------------------------------
void FocusManager::SetStoredFocusView(View* focus_view) {
  view_tracker_for_stored_view_->SetView(focus_view);
}
--------------------------------------------------------------
void ViewTracker::SetView(View* view) {
  if (view == view_)
    return;

  observation_.Reset();
  view_ = view; // 
  if (view_)
    observation_.Observe(view_.get());// put raw_ptr
}

```

0. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/account_selection_modal_view.cc;l=545?q=AccountSelectionModalView::ShowErrorDialog&ss=chromium%2Fchromium%2Fsrc>
1. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/account_selection_modal_view.cc;drc=5103ac6102b144aff2bb3b45fe525521ecf3320d;l=926?q=AccountSelectionModalView::ShowErrorDialog&ss=chromium%2Fchromium%2Fsrc>
2. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc;l=488;drc=4b478230012ff4109d3d7d2b1ec61df9b0897b8d>
3. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc;l=97?q=FedCmAccountSelectionView::ShowDialogWidget&ss=chromium%2Fchromium%2Fsrc>
4. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/widget/native_widget_mac.mm;l=644?q=NativeWidgetMac::Show&ss=chromium%2Fchromium%2Fsrc>

bitset:
bitset: 8b78167057eff3f61304a48f6600a62e67a713b7

fix suggestions:
use weak\_ptr to tracker the views.

repro.

1. Create a web server using node.js node ./server.js
2. Launch chrome and navigate to <http://localhost:8000/poc.html>
3. ./Chromium <http://localhost:8000/poc.html>
4. then see mov.

### li...@gmail.com (2024-12-06)

Hello Amy, I'm glad you contacted me. I have just finished writing the report and reproducing the vulnerability does not require any Chrome command-line parameters. Please refer to my latest comment for the replication steps:)

### pe...@google.com (2024-12-06)

Thank you for providing more feedback. Adding the requester to the CC list.

### ja...@chromium.org (2024-12-06)

Assuming that this isn't mitigated by MiraclePtr, I'm giving this a tentative severity of High (S1) because it looks like a use after free in the Browser process but is mitigated by the fact that the user has to be tricked into interacting with the dialog a certain way. This can be changed as we learn more about the issue.

### pe...@google.com (2024-12-06)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-12-06)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-12-06)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### li...@gmail.com (2024-12-06)

as I found, not protected by MiraclePtr, because turning on ASAN is different from not turning it on.

```
#if PA_BUILDFLAG(USE_ASAN_BACKUP_REF_PTR)
  if (brp_config.process_affected_by_brp_flag) {
    base::RawPtrAsanService::GetInstance().Configure(
        base::EnableDereferenceCheck(
            base::features::kBackupRefPtrAsanEnableDereferenceCheckParam.Get()),
        base::EnableExtractionCheck(
            base::features::kBackupRefPtrAsanEnableExtractionCheckParam.Get()),
        base::EnableInstantiationCheck(
            base::features::kBackupRefPtrAsanEnableInstantiationCheckParam
                .Get()));
  } else {
    base::RawPtrAsanService::GetInstance().Configure(
        base::EnableDereferenceCheck(false), base::EnableExtractionCheck(false),
        base::EnableInstantiationCheck(false));
  }

```

[0].<https://source.chromium.org/chromium/chromium/src/+/main:base/allocator/partition_alloc_support.cc;l=1026?q=RawPtrAsanService&ss=chromium%2Fchromium%2Fsrc>

### li...@gmail.com (2024-12-06)

one click and normal trigger poc.

Build on commit: 4b47823

### np...@google.com (2024-12-06)

Sorry I did not have time to look into this today but maybe we can get a bisect? It's not immediately clear to me what the cause of the uaf is.

### li...@gmail.com (2024-12-07)

Hello, @npm, if you encounter any problems, you can take a look at my very detailed write-up, which may be helpful to you.

By the way, I want to mention that my analysis was in the latest commit, but the root cause is the same.

The actual bitset is here:
<https://source.chromium.org/chromium/chromium/src/+/8b78167057eff3f61304a48f6600a62e67a713b7>

### np...@google.com (2024-12-09)

Ah thanks for sharing that, the fix should be very easy.

### ap...@google.com (2024-12-09)

Project: chromium/src  

Branch: main  

Author: Nicolás Peña <[npm@chromium.org](mailto:npm@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6078188>

[FedCM] Reset verifying\_focus\_view\_ when needed

---


Expand for full commit details
```
[FedCM] Reset verifying_focus_view_ when needed 
 
In RemoveNonHeaderChildViewsAndUpdateHeaderIfNeeded(), we remove all 
views that are not in the header. This means all pointers to views that 
are not in the header need to be reset. The pointers are reorganized to 
account for this distinction so it is harder to make the mistake in the 
future. The error test is also augmented to include showing account UI, 
which would surface this bug under ASAN bots. 
 
Fixed: 382399969 
Change-Id: I49c123e0b0f87f47715e14f7eb0b67b66eb9657e 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6078188 
Reviewed-by: Zachary Tan <tanzachary@chromium.org> 
Commit-Queue: Nicolás Peña <npm@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1393744}

```

---

Files:

- M `chrome/browser/ui/views/webid/account_selection_modal_view.cc`
- M `chrome/browser/ui/views/webid/account_selection_modal_view.h`
- M `chrome/browser/ui/views/webid/account_selection_modal_view_browsertest.cc`

---

Hash: f3d43d9f550d0ae4e479b3dcec6fdb0e3cc8979f  

Date:  Mon Dec 09 17:56:46 2024


---

### li...@gmail.com (2024-12-11)

Fedcm permission bypass: This patch here simulates a compromised renderer.

### am...@chromium.org (2024-12-11)

Hi Lime, thank you for this, but I'm not sure I'm understanding this being provided at this time. Are you saying that newly landed fix can be bypassed? Or are you simply conveying additional information?

### li...@gmail.com (2024-12-11)

Not a fixed bypass, this is simply conveying additional information. Because I am conducting in-depth research on whether this vulnerability can be exploited and synchronizing it

### np...@google.com (2024-12-11)

limmmmmeeee can you check from your side that your poc is now fixed? The fix is now in Canary (chrome://version 133.0.6888.0 or higher)

### li...@gmail.com (2024-12-11)

Okay, I tested it on `commit:fc5bcb88c3`, the latest commit. The fix works well, without crashing

### sp...@google.com (2024-12-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $36000.00 for this report.

Rationale for this decision:
$35,000 for high quality report of demonstrated memory corruption in a non-sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-12)

Congratulations on another one, lime! Thank you for your excellent efforts and reporting this issue to us -- great work!

### np...@google.com (2024-12-12)

Security folks - Does this need to be merged to M132?

### am...@chromium.org (2024-12-12)

Only if the bisect is incorrect; looking at the bisect that was used here the bug was introduced in 133 (https://chromiumdash.appspot.com/commit/8b78167057eff3f61304a48f6600a62e67a713b7) so no backmerge to 132 would be necessary if that is the case.

### np...@google.com (2024-12-12)

That was merged to 132. <https://chromiumdash.appspot.com/commit/8068b337947edba9a4e412f020217b885a5fb252>

### np...@google.com (2024-12-12)

Side note: it's unfortunate that chromiumdash does not make merges obvious, you'd think it could

### am...@chromium.org (2024-12-12)

it unfortunately does in the cherry pick link, I just completely failed to notice that -- thanks for catching that. 
I'll review this for 132 backmerge

### np...@google.com (2024-12-12)

Ah yes missed that too (I just guessed it would have been merged). Ok will merge if merge is approved

### am...@chromium.org (2024-12-12)

not seeing any issues related to the fix on Canary, please feel free to merge this fix (https://crrev.com/c/6078188) to branch 6834 at your earliest convenience so this fix can be included in next week's Beta before winter holiday release freeze 

### ap...@google.com (2024-12-13)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Nicolás Peña <[npm@chromium.org](mailto:npm@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6091938>

[M132][FedCM] Reset verifying\_focus\_view\_ when needed

---


Expand for full commit details
```
[M132][FedCM] Reset verifying_focus_view_ when needed 
 
In RemoveNonHeaderChildViewsAndUpdateHeaderIfNeeded(), we remove all 
views that are not in the header. This means all pointers to views that 
are not in the header need to be reset. The pointers are reorganized to 
account for this distinction so it is harder to make the mistake in the 
future. The error test is also augmented to include showing account UI, 
which would surface this bug under ASAN bots. 
 
(cherry picked from commit f3d43d9f550d0ae4e479b3dcec6fdb0e3cc8979f) 
 
Fixed: 382399969 
Change-Id: I49c123e0b0f87f47715e14f7eb0b67b66eb9657e 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6078188 
Reviewed-by: Zachary Tan <tanzachary@chromium.org> 
Commit-Queue: Nicolás Peña <npm@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1393744} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6091938 
Cr-Commit-Position: refs/branch-heads/6834@{#2101} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `chrome/browser/ui/views/webid/account_selection_modal_view.cc`
- M `chrome/browser/ui/views/webid/account_selection_modal_view.h`
- M `chrome/browser/ui/views/webid/account_selection_modal_view_browsertest.cc`

---

Hash: ffd98da4ceff933431b90f1cd6b264a931ded58f  

Date:  Fri Dec 13 06:52:16 2024


---

### pe...@google.com (2024-12-13)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### np...@google.com (2024-12-13)

1. Regression in M132
2. No this should not affect M126.

### qk...@google.com (2024-12-16)

Labeling as LTS-NotApplicable-126 as the comment #41 mentioned.

### ch...@google.com (2025-03-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/382399969)*
