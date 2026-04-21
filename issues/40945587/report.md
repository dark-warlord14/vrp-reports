# Security: Heap-use-after-free in WebUIBubbleDialogView::ClearContentsWrapper

| Field | Value |
|-------|-------|
| **Issue ID** | [40945587](https://issues.chromium.org/issues/40945587) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>ContentSuggestions |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | me...@gmail.com |
| **Assignee** | de...@chromium.org |
| **Created** | 2023-11-24 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**

1. apply the patch and compile chromium with ASAN enabled. The patch only turns on the compose.
2. Start a server at the folder of poc.html
3. `./Chromium --enable-features=Compose,ComposeNudge --user-data-dir=./tmp http://127.0.0.1:8605/poc.html`
4. Right click the textarea and choose "Lorem ipsum", then close the browser via the dock.

\*\*Note that I can only reproduce this on Mac with M1 chip.\*\*

**Problem Description:**

1. Analysis

When closing the browser with `WebUIBubbleDialogView` opened, the `contents_wrapper_` will be deleted before `WebUIBubbleDialogView` is destructed. However, in the Destructor of `WebUIBubbleDialogView`[1], `contents_wrapper_` will be used again[2], causing UAF.

```
WebUIBubbleDialogView::~WebUIBubbleDialogView() {  
  ClearContentsWrapper();  
}  

```
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

To verify the above conclusion, I added some debug information to output the addresses of the `contents_wrapper_` and `web_view_`:

```
diff --git a/chrome/browser/ui/views/bubble/webui_bubble_dialog_view.cc b/chrome/browser/ui/views/bubble/webui_bubble_dialog_view.cc  
index a731e644f77..3d82356edd1 100644  
--- a/chrome/browser/ui/views/bubble/webui_bubble_dialog_view.cc  
+++ b/chrome/browser/ui/views/bubble/webui_bubble_dialog_view.cc  
@@ -76,6 +76,8 @@ WebUIBubbleDialogView::~WebUIBubbleDialogView() {  
 }  
  
 void WebUIBubbleDialogView::ClearContentsWrapper() {  
+LOG(ERROR)<<" contents_wrapper_ "<<contents_wrapper_.get();  
+LOG(ERROR)<<" web_view_ "<<web_view_.get();  
   if (!contents_wrapper_)  
     return;  
   DCHECK_EQ(this, contents_wrapper_->GetHost().get());  

```

The debug log proves that the address of `contents_wrapper_`(0x611000510bc0) is deleted before use.

```
[1480:259:1124/163448.723805:ERROR:webui_bubble_dialog_view.cc(79)]  contents_wrapper_ 0x611000510bc0  
[1480:259:1124/163448.723842:ERROR:webui_bubble_dialog_view.cc(80)]  web_view_ 0x619000cd5580  
=================================================================  
==1480==ERROR: AddressSanitizer: heap-use-after-free on address 0x611000510bc0 at pc 0x000104102c4c bp 0x00016da461b0 sp 0x00016da461a8  
READ of size 1 at 0x611000510bc0 thread T0  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bubble/webui_bubble_dialog_view.cc;l=74;bpv=1;bpt=0;drc=c5aebfb40ad8443d46c6b1930044ade7fcfc0137>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bubble/webui_bubble_dialog_view.cc;l=78;drc=c5aebfb40ad8443d46c6b1930044ade7fcfc0137;bpv=1;bpt=0>

2. Bisect  
   
   This commit allows `ComposeDialogView` to inherit from `WebUIBubbleDialogView`, providing an entry point for UAF: <https://chromium-review.googlesource.com/c/chromium/src/+/5021240> And it affects Dev 121.0.6129.0, Canary 121.0.6129.0.  
   
   Actually the raw\_ptr of `contents_wrapper_` has been introduced for a long time.
3. Suggested Patch  
   
   Change the `contents_wrapper_` to a weak ptr.

**Additional Comments:**

\*\*Chrome version: \*\* 119.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 168 B)
- [patch.txt](attachments/patch.txt) (text/plain, 2.0 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 25.8 KB)
- [video.mov](attachments/video.mov) (video/quicktime, 3.7 MB)

## Timeline

### [Deleted User] (2023-11-24)

[Empty comment from Monorail migration]

### el...@chromium.org (2023-11-24)

Thanks for the report, and good find :)

I have not yet run your repro case, but I read over the code and I can see the bug you are talking about. ComposeDialogView subclasses WebUIBubbleDialogView, and WebUIBubbleDialogView tries to use a raw pointer to something owned by its own subclass inside its own destructor, which is never safe, because the subclass destructor will already have run when the superclass destructor is invoked. Using WeakPtr to reference the subclass-owned object might be the most expedient fix, but it seems inherently risky to structure the object graph this way.

I'm going to bump this to Pri-1 and kick it over to dewittj@, who wrote a bunch of the involved code in eda1c0ca98f94c47a569d1bc749ef295e299e224. However, this is a bug in an unshipped feature (Compose) so there is little current impact.

[Monorail components: UI>Browser>ContentSuggestions]

### de...@chromium.org (2023-11-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed

commit 47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed
Author: Justin DeWitt <dewittj@chromium.org>
Date: Tue Dec 05 23:45:11 2023

WebUI: Make WebUIBubbleDialogView hold a weak pointer to BubbleContentsWrapper.

WebUIBubbleDialogView dereferences BubbleContentsManager in its
destructor, but BubbleContentsWrapper is not a View and so may be
destroyed before or after BubbleContentsWrapper.

Bug: 1505002, b:313664294
Change-Id: I2911621d8541088ae4773541698095e68c1ddbfd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5085847
Commit-Queue: Justin DeWitt <dewittj@chromium.org>
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Reviewed-by: John Palmer <jopalmer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1233644}

[modify] https://crrev.com/47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed/chrome/browser/ui/views/bubble/bubble_contents_wrapper_unittest.cc
[modify] https://crrev.com/47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed/chrome/browser/ui/views/bubble/webui_bubble_dialog_view_unittest.cc
[modify] https://crrev.com/47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed/chrome/browser/ui/webui/ash/mako/mako_bubble_coordinator.cc
[modify] https://crrev.com/47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed/chrome/browser/ui/views/bubble/bubble_contents_wrapper.h
[modify] https://crrev.com/47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed/chrome/browser/ui/views/bubble/webui_bubble_dialog_view.cc
[modify] https://crrev.com/47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed/chrome/browser/ui/views/compose/compose_dialog_view.cc
[modify] https://crrev.com/47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed/chrome/browser/ui/views/bubble/webui_bubble_manager_unittest.cc
[modify] https://crrev.com/47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed/chrome/browser/ui/webui/ash/emoji/emoji_ui.cc
[modify] https://crrev.com/47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed/chrome/browser/ui/views/bubble/webui_bubble_manager.h
[modify] https://crrev.com/47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed/chrome/browser/ui/views/bubble/webui_bubble_dialog_view.h
[modify] https://crrev.com/47de8d5f05c98634e3dc3ec4dadc42cb6bdbc7ed/chrome/browser/ui/views/bubble/webui_bubble_manager_browsertest.cc


### de...@chromium.org (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-07)

[Empty comment from Monorail migration]

### me...@gmail.com (2024-01-25)

Hello, any update about the reward?

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations Krace! The Chrome VRP Panel has decided to award you $1,000 for this report of a significantly mitigated security bug -- mitigated by BRP protection, not being remote exploitable, and user gesture. Thank you for your efforts and reporting this issue to us! 

### am...@chromium.org (2024-02-02)

Sincere apologies it looks like we missed the bisect bonus on the original reward amount. I've just updated the reward amount to reflect that! 

### me...@gmail.com (2024-02-02)

[Comment Deleted]

### me...@gmail.com (2024-02-02)

Thank you :)

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1505002?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40945587)*
