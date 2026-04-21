# Security: heap-buffer-overflow components/ui_devtools/ui_element.cc:112:5

| Field | Value |
|-------|-------|
| **Issue ID** | [40060875](https://issues.chromium.org/issues/40060875) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Views>UIDevtools |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2022-09-08 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. Use prebuilt linux chromeOS (gs://chromium-browser-asan/linux-release-chromeos/asan-linux-release-1044347.zip) or any lower version.
2. --enable-ui-devtools=9223 in command line and navigate to devtools://devtools/bundled/devtools\_app.html?uiDevTools=true&ws=127.0.0.1:9223/0 from ash browser.
3. navigate to screen recorder at systems tray or hit F5 from keyboard

**Problem Description:**  

The `UIElement::ReorderChild` function has no checking when the `i` value is higher/lower than `pos`, so when the screenRecorder is fired while --enable-ui-devtools=9223 and devtools are enabled, it's lead to Heap BoF.

```
void UIElement::ReorderChild(UIElement\* child, int index) {  
  auto i = std::find(children_.begin(), children_.end(), child);  
  DCHECK(i != children_.end());  
  DCHECK_GE(index, 0);  
  DCHECK_LT(static_cast<size_t>(index), children_.size());  
  
  // If |child| is already at the desired position, there's nothing to do.  
  const auto pos = std::next(children_.begin(), index);  
  if (i == pos)  
    return;  
  
  // Rotate |child| to be at the desired position.  
  if (pos < i)  
    std::rotate(pos, i, std::next(i));  
  else  
    std::rotate(i, std::next(i), std::next(pos)); <---[1]  
  
  delegate()->OnUIElementReordered(child->parent(), child);  
}  

```

suggestion fix:

```
  if (pos < i)  
    std::rotate(pos, i, std::next(i));  
  else if (pos < i) <--- can prevent heap BoF  
    std::rotate(i, std::next(i), std::next(pos));  
  
or  
  
  if (pos < i)  
    std::rotate(pos, i, std::next(i));  
  else   
    std::rotate(i, std::next(pos), std::next(pos)); <--- as attached suggestion_fix.webm can also prevent heap BoF  
  delegate()->OnUIElementReordered(child->parent(), child);  
  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/ui_devtools/ui_element.cc;l=97-115?q=components%2Fui_devtools%2Fui_element.cc&ss=chromium%2Fchromium%2Fsrc>

**Additional Comments:**  

this issue is affecting stable channel.

\*\*Chrome version: \*\* 107.0.5287.0 + this probable affect to sable version \*\*Channel: \*\* Dev

**OS:** Chrome OS

## Attachments

- [ui_element_asan.log](attachments/ui_element_asan.log) (text/plain, 20.4 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 9.1 MB)
- [suggestion_fix.webm](attachments/suggestion_fix.webm) (video/webm, 9.7 MB)
- [1361204-without-flags.webm](attachments/1361204-without-flags.webm) (video/webm, 8.6 MB)

## Timeline

### rh...@gmail.com (2022-09-08)

uploading suggestion_fix.webm

### [Deleted User] (2022-09-08)

[Empty comment from Monorail migration]

### aa...@google.com (2022-09-09)

Assigning to kerenzhu from ui_devtools/OWNERS

Setting impact as None because this requires running chrome with an extra flag.

[Monorail components: UI>Shell]

### ke...@chromium.org (2022-09-09)

[Empty comment from Monorail migration]

[Monorail components: -UI>Shell Internals>Views>UIDevtools]

### rh...@gmail.com (2022-09-09)

Hi,

For an update, this heap BoF issue can be triggered without '--enable-ui-devtools=9223', tested on head main #1037404 (lower version than first submitted report on https://crbug.com/chromium/1361204#c0) and other lower version it was reproduced, but requires more steps.

(1) Open browser
(2) Navigate chrome://inspect and open devtools
(3) Type chrome.send('launch-ui-devtools',[]); 
(4) Navigate to screen recorder at systems tray or hit F5 from keyboard

Thanks


### ad...@google.com (2022-09-09)

(auto-cc on security bug)

### ke...@chromium.org (2022-09-19)

The fix will be more complicated than suggested in https://crbug.com/chromium/1361204#c0. WindowElement is supposed to track aura::Window's children, however when the crash happens, the size of aura::Window::children() is larger than the size of WindowElement::children_. Therefore, the index passed to ReorderChild can be out of bound.

### rh...@gmail.com (2022-10-17)

hello,

is there anyone fixing this issue?
thanks

### ro...@chromium.org (2022-11-01)

This is on our queue, but as mentioned above, this requires navigating to internal chrome pages, which is generally restricted. This means a user needs to go out of their way to get to chrome://inspect, similar to specifying the --enable-ui-devtools flag above.

### rh...@gmail.com (2022-11-01)

Hello,

Thank you very much for the update. 

>> this requires navigating to internal chrome pages, which is generally restricted. This means a user needs to go out of their way to get to chrome://inspect
Yes, it is not normal behavior and needs extra steps to trigger the bug. Anyway developer can fix this issue whenever they able.

### rh...@gmail.com (2023-01-09)

Sorry for the ping. Any chance I can get the update for the bug?

### ke...@chromium.org (2023-01-09)

Sorry I have not been active on this bug lately. Will take a look this week.

### gi...@appspot.gserviceaccount.com (2023-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/83159fb1551c660a50be8a1aad1bb256f7e9e126

commit 83159fb1551c660a50be8a1aad1bb256f7e9e126
Author: Keren Zhu <kerenzhu@chromium.org>
Date: Tue Jan 10 23:33:03 2023

ash: defer re-ordering in CaptureModeSession::ParentContainerObserver()

CaptureModeSession::ParentContainerObserver() will re-order windows
during window adding / removing. In general, reentrantly modifying a
tree is not a good idea. In practice, this is causing crash in
UI DevTools that tracks the window hierarchy, because at the time
re-ordering happens the DevTools have not yet updated its tracked
windows. Fix this by deferring re-ordering in a posted task.

Bug: 1361204
Change-Id: I06217595715d382c6b957e0b90931c7cbf391e52
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4152795
Reviewed-by: Leonard Grey <lgrey@chromium.org>
Reviewed-by: James Cook <jamescook@chromium.org>
Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1091067}

[modify] https://crrev.com/83159fb1551c660a50be8a1aad1bb256f7e9e126/ash/capture_mode/capture_mode_camera_unittests.cc
[modify] https://crrev.com/83159fb1551c660a50be8a1aad1bb256f7e9e126/components/ui_devtools/dom_agent.cc
[modify] https://crrev.com/83159fb1551c660a50be8a1aad1bb256f7e9e126/ash/capture_mode/capture_mode_session.cc


### ke...@chromium.org (2023-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-11)

[Empty comment from Monorail migration]

### rh...@gmail.com (2023-01-13)

karen@,

Thanks for quick fix!, no longer crash on Canary.

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug. Thank you for your efforts in reporting this issue to us! 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1361204?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060875)*
