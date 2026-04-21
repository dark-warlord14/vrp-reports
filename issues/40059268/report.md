# heap-buffer-overflow on ui_devtools::UIElement::ReorderChild

| Field | Value |
|-------|-------|
| **Issue ID** | [40059268](https://issues.chromium.org/issues/40059268) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools |
| **Platforms** | Mac, Windows |
| **Reporter** | xp...@gmail.com |
| **Assignee** | lg...@chromium.org |
| **Created** | 2022-04-01 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.43 Safari/537.36

Steps to reproduce the problem:
1. Start chrome/chromium with --enable-ui-devtools
2. Navigate to "chrome://inspect" and click "Native Client".
3. Click button labeled "Inspect Native UI".
4. Press side panel button

What is the expected behavior?
N/A

What went wrong?
heap-buffer-overflow

Did this work before? N/A 

Chrome version: 102.0.4976.0  Channel: canary
OS Version: 11

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 13.4 KB)
- [CTOt1m7oxa.gif](attachments/CTOt1m7oxa.gif) (image/gif, 4.8 MB)

## Timeline

### [Deleted User] (2022-04-01)

[Empty comment from Monorail migration]

### hc...@google.com (2022-04-01)

Confirmed repro instructions in 102.0.4972.0, lgrey@ could you take a look?

[Monorail components: Platform>DevTools]

### [Deleted User] (2022-04-01)

[Empty comment from Monorail migration]

### lg...@chromium.org (2022-04-01)

Repro confirmed on Mac. +pkasting@ who wrote this bit

At first glance, I think we're being bitten by observer ordering. UIElement::AddChild gets called by OnChildViewAdded, but the reorder is triggered by SidePanel's OnChildViewAdded before that has a chance to be called.

[7663:259:0401/124118.466526:FATAL:ui_element.cc(103)] Check failed: static_cast<size_t>(index) < children_.size() (1 vs. 1)
0   libbase.dylib                       0x00000001120cf2bf base::debug::CollectStackTrace(void**, unsigned long) + 31
1   libbase.dylib                       0x0000000111d8db88 base::debug::StackTrace::StackTrace(unsigned long) + 72
2   libbase.dylib                       0x0000000111d8dc0d base::debug::StackTrace::StackTrace(unsigned long) + 29
3   libbase.dylib                       0x0000000111d8dbe5 base::debug::StackTrace::StackTrace() + 37
4   libbase.dylib                       0x0000000111dee213 logging::LogMessage::~LogMessage() + 179
5   libbase.dylib                       0x0000000111def295 logging::LogMessage::~LogMessage() + 21
6   libbase.dylib                       0x0000000111def2b9 logging::LogMessage::~LogMessage() + 25
7   libbase.dylib                       0x0000000111d4592b logging::CheckError::~CheckError() + 43
8   libbase.dylib                       0x0000000111d45405 logging::CheckError::~CheckError() + 21
9   libui_devtools.dylib                0x00000001c37e3c54 ui_devtools::UIElement::ReorderChild(ui_devtools::UIElement*, int) + 516
10  libchrome_dll.dylib                 0x0000000159e9c7a6 ui_devtools::ViewElement::OnChildViewReordered(views::View*, views::View*) + 470
11  libviews.dylib                      0x00000001c58afc2b views::View::ReorderChildView(views::View*, int) + 1451
12  libchrome_dll.dylib                 0x0000000160b3cfc2 SidePanel::OnChildViewAdded(views::View*, views::View*) + 66
13  libviews.dylib                      0x00000001c58c169e views::View::AddChildViewAtImpl(views::View*, int) + 1934
14  libchrome_dll.dylib                 0x0000000160c903bb ReadLaterSidePanelWebView* views::View::AddChildView<ReadLaterSidePanelWebView>(ReadLaterSidePanelWebView*) + 59
15  libchrome_dll.dylib                 0x0000000160c8f639 ReadLaterSidePanelWebView* views::View::AddChildView<ReadLaterSidePanelWebView>(std::__Cr::unique_ptr<ReadLaterSidePanelWebView, std::__Cr::default_delete<ReadLaterSidePanelWebView> >) + 185

### hc...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### hc...@google.com (2022-04-01)

Low severity added since its behind a flag

### [Deleted User] (2022-04-01)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-04-05)

[Empty comment from Monorail migration]

### lg...@chromium.org (2022-04-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b4ac2cf681e719d3d55d90d8b77147733a21b7ed

commit b4ac2cf681e719d3d55d90d8b77147733a21b7ed
Author: Leonard Grey <lgrey@chromium.org>
Date: Fri Apr 08 19:33:08 2022

UIDevTools: guard ViewElement against out of order observers

ViewElement currently keeps its element tree in sync with the
backing view via observer methods. Since observers are called
in order, that means that if a view is added, an observer
method that is called before ViewElement's can manipulate the
tree (for example reordering it), before the ViewElement has
seen the new view. In this case, ViewElement will see the
reorder before it sees the add, and Bad Things happen.

This change tries to detect inconsistencies by checking for
certain preconditions:
- On reorder, that there are the same number of children in
the element and backing view
- On add, that the child element doesn't exist
- On remove, that the child element does exist

and rebuilds the subtree from scratch if they are violated.

This has a minimal post-viz_devtools removal cleanup as well
(will probably follow up with more; this is just enough for
the current change). The semantics of `ClearChildren()` is
changed but this is now the only caller.

Bug: 1312270
Change-Id: I9919377e5b2c82a25105ac53f190dcc72638ba30
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3572481
Reviewed-by: Yuheng Huang <yuhengh@chromium.org>
Commit-Queue: Leonard Grey <lgrey@chromium.org>
Cr-Commit-Position: refs/heads/main@{#990529}

[modify] https://crrev.com/b4ac2cf681e719d3d55d90d8b77147733a21b7ed/components/ui_devtools/views/view_element.h
[modify] https://crrev.com/b4ac2cf681e719d3d55d90d8b77147733a21b7ed/components/ui_devtools/views/view_element_unittest.cc
[modify] https://crrev.com/b4ac2cf681e719d3d55d90d8b77147733a21b7ed/components/ui_devtools/ui_element.cc
[modify] https://crrev.com/b4ac2cf681e719d3d55d90d8b77147733a21b7ed/components/ui_devtools/ui_element.h
[modify] https://crrev.com/b4ac2cf681e719d3d55d90d8b77147733a21b7ed/components/ui_devtools/views/view_element.cc


### lg...@chromium.org (2022-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-13)

[Empty comment from Monorail migration]

### xp...@gmail.com (2022-04-14)

Hi,

Update - I was able to reproduce without the command line switch "--enable-ui-devtools". Maybe this affects the severity :P

Steps:
   1: Navigate to chrome://inspect.
   2: Execute in devtools: chrome.send('launch-ui-devtools',[]);
   3: Open side panel.

Fyi, fix for the bufferoverflow is on latest Chromium, so you'll have to do this on an older asan build.

-

I am not sure if the "chrome.send('launch-ui-devtools',[])" command is intended to be accessible without the command line switch.

Additionally, I can reproduce on Linux.


Thank you!

### am...@google.com (2022-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-13)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us. 

### xp...@gmail.com (2022-06-13)

Thank you team and thank you Amy.

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-07-20)

This issue was migrated from crbug.com/chromium/1312270?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1313309, crbug.com/chromium/1313574]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059268)*
