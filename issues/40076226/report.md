# Security: Heap-use-after-free in ChromeComposeClient::ShowComposeDialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40076226](https://issues.chromium.org/issues/40076226) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>ContentSuggestions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | de...@chromium.org |
| **Created** | 2023-11-06 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. apply the patch and compile chromium with ASAN enabled
2. Start a server at the folder of poc.html
3. `./Chromium --enable-features=Compose,ComposeNudge --user-data-dir=./tmp http://127.0.0.1:8605/poc.html about:blank`
4. Click the textarea and choose the popup, then click the textarea again. When you see the second popup, click it and press `Ctrl+w` at the same time. Last, click anywhere of the browser.

\*\*Note that I can only reproduce this on Mac with M1 chip.\*\*

**Problem Description:**

1. Analysis

In `ChromeComposeClient::ShowComposeDialog`, it will show a compose dialog.

```
void ChromeComposeClient::ShowComposeDialog(  
    autofill::AutofillComposeDelegate::UiEntryPoint ui_entry_point,  
    const autofill::FormFieldData& trigger_field,  
    std::optional<autofill::AutofillClient::PopupScreenLocation>  
        popup_screen_location,  
    ComposeCallback callback) {  
  CreateSessionIfNeeded(trigger_field, std::move(callback));  
  if (!skip_show_dialog_for_test_) {  
    // The bounds given by autofill are relative to the top level frame. Here we  
    // offset by the WebContents container to make up for that.  
    gfx::RectF bounds_in_screen = trigger_field.bounds;  
    bounds_in_screen.Offset(  
        GetWebContents().GetContainerBounds().OffsetFromOrigin());  
    compose_dialog_controller_ =  
        chrome::ShowComposeDialog(GetWebContents(), bounds_in_screen);  
  }  
}  

```

This is a `WebUIBubbleDialogView` and it could still be shown when we close the WebContents after the UI was created immediately on MAC M1.

```
void WebUIBubbleDialogView::ShowUI() {  
  DCHECK(GetWidget());  
  GetWidget()->Show();  
  web_view_->GetWebContents()->Focus();  
}  

```

When clicking the browser, the UI will lose focus and should be closed. But the `ChromeComposeClient` has been destructed because the WebContents is closed, so there is a UAF when accessing the freed UI.

```
void WebUIBubbleDialogView::ClearContentsWrapper() {  
  if (!contents_wrapper_)  
    return;  
  DCHECK_EQ(this, contents_wrapper_->GetHost().get());  
  DCHECK_EQ(web_view_->web_contents(), contents_wrapper_->web_contents());  
  web_view_->SetWebContents(nullptr);  
  contents_wrapper_->web_contents()->WasHidden();  
  contents_wrapper_->SetHost(nullptr);  
  contents_wrapper_ = nullptr;  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/compose/chrome_compose_client.cc;l=97>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bubble/webui_bubble_dialog_view.cc;l=111>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bubble/webui_bubble_dialog_view.cc;l=78>

2. Bisect

This UAF is introduced in this commit: <https://chromium-review.googlesource.com/c/chromium/src/+/4953087>  

This UAF affects Beta 120.0.6099.5, Dev 120.0.6090.0.

**Additional Comments:**

\*\*Chrome version: \*\* 120 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 168 B)
- [asan.txt](attachments/asan.txt) (text/plain, 17.6 KB)
- [patch.txt](attachments/patch.txt) (text/plain, 1.1 KB)
- [video.mov](attachments/video.mov) (video/quicktime, 5.6 MB)

## Timeline

### [Deleted User] (2023-11-06)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-11-06)

dewittj@, is compose going to be launched on Android? I assume that the Android implementation might not have the same bug though.

(Also, what component can I put this bug under? I don't see one in https://source.chromium.org/chromium/chromium/src/+/main:components/compose/DIR_METADATA)

This is high, or possibly even medium, due to:
- protected by BRP
- requires user interaction

### dc...@chromium.org (2023-11-06)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-11-06)

[Empty comment from Monorail migration]

### de...@google.com (2023-11-06)

Re https://crbug.com/chromium/1499835#c2:
- We have been using an internal bug component go/chrome-compose-bug
- This may be launched eventually on Android... however it is currently compiled out of non-desktop platforms.

Note that this is behind a flag for the moment, so impossible to trigger under normal circumstances.

[Monorail components: UI>Browser>ContentSuggestions]

### de...@chromium.org (2023-11-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eda1c0ca98f94c47a569d1bc749ef295e299e224

commit eda1c0ca98f94c47a569d1bc749ef295e299e224
Author: Justin DeWitt <dewittj@chromium.org>
Date: Tue Nov 14 20:01:00 2023

Lifetime of Compose's BubbleContentsWrapperT matches its BubbleDialogView.

Previously the ChromeComposeClient would own (indirectly) the
BubbleContentsWrapperT via ChromeComposeDialogController. Normally this
would not be a problem as the dialog closes right after the web
contents, but it was possible for the webui to reference the destroyed
WebContents in certain scenarios.

Bug: 1499835
Change-Id: Id8c7ea3caad2dc9d4eb20cb97804b0cbadd0f230
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5021240
Reviewed-by: Jeffrey Cohen <jeffreycohen@chromium.org>
Commit-Queue: Justin DeWitt <dewittj@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1224489}

[add] https://crrev.com/eda1c0ca98f94c47a569d1bc749ef295e299e224/chrome/browser/compose/compose_dialog_browsertest.cc
[add] https://crrev.com/eda1c0ca98f94c47a569d1bc749ef295e299e224/chrome/test/data/compose/test2.html
[modify] https://crrev.com/eda1c0ca98f94c47a569d1bc749ef295e299e224/chrome/browser/ui/views/compose/compose_dialog_view.cc
[modify] https://crrev.com/eda1c0ca98f94c47a569d1bc749ef295e299e224/chrome/test/BUILD.gn
[modify] https://crrev.com/eda1c0ca98f94c47a569d1bc749ef295e299e224/chrome/browser/ui/BUILD.gn
[modify] https://crrev.com/eda1c0ca98f94c47a569d1bc749ef295e299e224/chrome/browser/ui/views/compose/compose_dialog_view.h
[modify] https://crrev.com/eda1c0ca98f94c47a569d1bc749ef295e299e224/chrome/browser/ui/views/compose/chrome_compose_dialog_controller.cc
[modify] https://crrev.com/eda1c0ca98f94c47a569d1bc749ef295e299e224/chrome/browser/ui/webui/compose/compose_ui.cc
[modify] https://crrev.com/eda1c0ca98f94c47a569d1bc749ef295e299e224/chrome/browser/ui/views/compose/chrome_compose_dialog_controller.h


### de...@chromium.org (2023-11-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-22)

Congratulations, Krace! The Chrome VRP Panel has decided to award you $2,000 for this report for a highly mitigated security bug - mitigated by MiraclePtr protection and user gesture -- + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us.

### am...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### is...@google.com (2023-11-27)

This issue was migrated from crbug.com/chromium/1499835?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076226)*
