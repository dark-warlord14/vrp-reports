# Security: Heap-use-after-free in ReadAnythingToolbarView 

| Field | Value |
|-------|-------|
| **Issue ID** | [40059492](https://issues.chromium.org/issues/40059492) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Accessibility |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | ms...@google.com |
| **Created** | 2022-04-27 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. download asan-linux-release-995515.zip and unzip
2. run `./chrome --enable-features=UnifiedSidePanel,ReadAnything http://127.0.0.1:8605/poc.html`
3. open side panel, switch the combobox to `Read anything` then switch back to `Reading list`
4. wait until UAF occurs.

**Problem Description:**  

1 `ReadAnythingCoordinator` has a member `unique_ptr<ReadAnythingModel>model_`[1],

chrome/browser/ui/views/side\_panel/read\_anything/read\_anything\_coordinator.h

```
std::unique_ptr<ReadAnythingModel> model_;  //=>[1]  

```

2 When calling CreateContainerView[2], it will create a `ReadAnythingToolbarView` with a raw pointer `model_.get()->GetFontModel`[3], this raw pointer is got from a unique ptr `font_model_`[4].  

Therefore, `ReadAnythingToolbarView` has a raw pointer that point to a unique ptr in `ReadAnythingModel`[5]

chrome/browser/ui/views/side\_panel/read\_anything/read\_anything\_coordinator.cc

```
std::unique_ptr<views::View> ReadAnythingCoordinator::CreateContainerView() {  
  // Create the views.  
  auto toolbar = std::make_unique<ReadAnythingToolbarView>(  
      controller_.get(), model_.get()->GetFontModel());  //=>[2]  

```

chrome/browser/ui/views/side\_panel/read\_anything/read\_anything\_model.h

```
ReadAnythingFontModel\* GetFontModel() { return font_model_.get(); } //=>[3]  
[...]  
const std::unique_ptr<ReadAnythingFontModel> font_model_; //=>[4]  

```

chrome/browser/ui/views/side\_panel/read\_anything/read\_anything\_toolbar\_view.cc

```
  // Create a font selection combobox for the toolbar.  
  auto combobox = std::make_unique<views::Combobox>();  
  combobox->SetCallback(  
      base::BindRepeating(&ReadAnythingToolbarView::FontNameChangedCallback,  
                          weak_pointer_factory_.GetWeakPtr()));  
  combobox->SetSizeToLargestLabel(true);  
  // TODO(1266555): This is placeholder text, remove for final UI.  
  combobox->SetTooltipTextAndAccessibleName(u"Font Choice");  
  combobox->SetModel(model);  //=>[5]  
  
  // Add all views as children.  
  font_combobox_ = AddChildView(std::move(combobox));  

```

3 When closing browser, we can control the destruction order of this two class `ReadAnythingToolbarView` and `ReadAnythingModel`, if we destruct `ReadAnythingModel` first, it will reset the uniquet ptr. When we destruct `ReadAnythingToolbarView`, it will use the dangling pointer.

=================================================================  

==101351==ERROR: AddressSanitizer: heap-use-after-free on address 0x6030005c26c0 at pc 0x557a5410ea57 bp 0x7ffdc84c1860 sp 0x7ffdc84c1858  

READ of size 8 at 0x6030005c26c0 thread T0 (chrome)  

#0 0x557a5410ea56 in Reset base/scoped\_observation.h:70:7  

#1 0x557a5410ea56 in ~ScopedObservation base/scoped\_observation.h:54:26  

#2 0x557a5410ea56 in views::Combobox::~Combobox() ui/views/controls/combobox/combobox.cc:262:1  

#3 0x557a5410eb6d in views::Combobox::~Combobox() ui/views/controls/combobox/combobox.cc:257:23  

#4 0x557a52e9faac in views::View::~View() ui/views/view.cc:254:9  

#5 0x557a5491e5d9 in ~ReadAnythingToolbarView chrome/browser/ui/views/side\_panel/read\_anything/read\_anything\_toolbar\_view.cc:55:51  

#6 0x557a5491e5d9 in ReadAnythingToolbarView::~ReadAnythingToolbarView() chrome/browser/ui/views/side\_panel/read\_anything/read\_anything\_toolbar\_view.cc:55:51  

#7 0x557a52e9faac in views::View::~View() ui/views/view.cc:254:9  

#8 0x557a5490cb59 in ~ReadAnythingContainerView chrome/browser/ui/views/side\_panel/read\_anything/read\_anything\_container\_view.cc:61:55  

#9 0x557a5490cb59 in ReadAnythingContainerView::~ReadAnythingContainerView() chrome/browser/ui/views/side\_panel/read\_anything/read\_anything\_container\_view.cc:61:55  

#10 0x557a54933dda in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#11 0x557a54933dda in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#12 0x557a54933dda in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:269:19  

#13 0x557a54933dda in SidePanelEntry::~SidePanelEntry() chrome/browser/ui/views/side\_panel/side\_panel\_entry.cc:23:33  

#14 0x557a54936118 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#15 0x557a54936118 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#16 0x557a54936118 in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:269:19  

#17 0x557a54936118 in destroy buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator.h:133:15  

#18 0x557a54936118 in destroy<std::\_\_1::unique\_ptr<SidePanelEntry, std::\_\_1::default\_delete<SidePanelEntry> >, void> buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:308:13  

#19 0x557a54936118 in \_\_destruct\_at\_end buildtools/third\_party/libc++/trunk/include/vector:429:9  

#20 0x557a54936118 in clear buildtools/third\_party/libc++/trunk/include/vector:372:29  

#21 0x557a54936118 in ~\_\_vector\_base buildtools/third\_party/libc++/trunk/include/vector:466:9  

#22 0x557a54936118 in std::\_\_1::vector<std::\_\_1::unique\_ptr<SidePanelEntry, std::\_\_1::default\_delete<SidePanelEntry> >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<SidePanelEntry, std::\_\_1::default\_delete<SidePanelEntry> > > >::~vector() buildtools/third\_party/libc++/trunk/include/vector:558:

**Additional Comments:**

\*\*Chrome version: \*\* 98.0.4758.102 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [video.webm](attachments/video.webm) (video/webm, 1.5 MB)
- [poc.html](attachments/poc.html) (text/plain, 61 B)

## Timeline

### dt...@chromium.org (2022-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-27)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-27)

Thanks for the detailed report. +abigailklein to look at.

Assigning High severity as it's a browser process UaF, but only triggers on destruction. Impact=None as this is in a disabled feature as far as I can tell.

[Monorail components: UI>Accessibility]

### ab...@google.com (2022-04-28)

Thanks for assigning, I see the problem and I'll fix this tomorrow.

### ab...@google.com (2022-04-28)

Assigning to Mark who wrote ReadAnythingToolbarView.
Mark is out this week, but can address it next week. Since this is a disabled feature, I think that timeline should be ok.

Some investigation:
The crash occurs because the ComboboxModel is a scoped observer, so when the ReadAnythingToolbarView's combobox is destructed, the combobox's model automatically destroys itself. But with the asan build, the ReadAnythingCoordinator is destroyed before the ReadAnythingToolbarView. When the Coordinator destroys itself, the model is destroyed along with it, meaning that the combox now has a stale pointer to the model.

What needs to happen is: when the coordinator is destroyed, the combobox should call SetModel(nullptr). We should also ensure that we set delegate_ = nullptr to ensure we don't try using it after it has gone stale.

As I was investigating this, I also realized that the comment here [1] is not accurate. This crash clearly teachs us that the UI can outlive the coordinator. We should make the ReadAnythingPageHandler be a ScopedObserver of the model; that way we won't have to stop observing.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/side_panel/read_anything/read_anything_page_handler.cc;l=36?q=read_anything_page_handler&ss=chromium

### an...@chromium.org (2022-05-06)

mschillaci@: Friendly marshal ping for an update. Thanks!

### ms...@google.com (2022-05-06)

anunoy@ - We have been working on a patch and hope to have it in early next week, thanks!

### gi...@appspot.gserviceaccount.com (2022-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6d19b10b5fda471dfaa033931d35ed1aaae56724

commit 6d19b10b5fda471dfaa033931d35ed1aaae56724
Author: Mark Schillaci <mschillaci@google.com>
Date: Thu May 12 19:22:08 2022

[Read Anything] Fix UAF bug in the ReadAnythingToolbarView

This CL addresses a heap-use-after-free issue that was
found in ReadAnythingToolbarView. It is meant to have
no functional changes for a user. We now clean up
pointers when the ReadAnythingCoordinator is destroyed,
and when the views are destroyed. Previously we had
assumed that the views were always destroyed first,
but there are some cases where the coordinator can be
destroyed first in which case the views need to set
their associated points to nullptr and remove
themselves from observer lists.

AX-Relnotes: N/A
Bug: 1320181
Change-Id: I835b6b490c7ab25ff0cb0b1fbe982c17b3844424
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3632664
Reviewed-by: Abigail Klein <abigailbklein@google.com>
Commit-Queue: Mark Schillaci <mschillaci@google.com>
Cr-Commit-Position: refs/heads/main@{#1002784}

[modify] https://crrev.com/6d19b10b5fda471dfaa033931d35ed1aaae56724/chrome/browser/ui/views/side_panel/read_anything/read_anything_coordinator_unittest.cc
[modify] https://crrev.com/6d19b10b5fda471dfaa033931d35ed1aaae56724/chrome/browser/ui/webui/side_panel/read_anything/read_anything_page_handler.h
[modify] https://crrev.com/6d19b10b5fda471dfaa033931d35ed1aaae56724/chrome/browser/ui/views/side_panel/read_anything/read_anything_toolbar_view.h
[modify] https://crrev.com/6d19b10b5fda471dfaa033931d35ed1aaae56724/chrome/browser/ui/views/side_panel/read_anything/read_anything_coordinator.cc
[modify] https://crrev.com/6d19b10b5fda471dfaa033931d35ed1aaae56724/chrome/browser/ui/views/side_panel/read_anything/read_anything_coordinator.h
[modify] https://crrev.com/6d19b10b5fda471dfaa033931d35ed1aaae56724/chrome/browser/ui/views/side_panel/read_anything/read_anything_container_view.h
[modify] https://crrev.com/6d19b10b5fda471dfaa033931d35ed1aaae56724/chrome/browser/ui/views/side_panel/read_anything/read_anything_toolbar_view.cc
[modify] https://crrev.com/6d19b10b5fda471dfaa033931d35ed1aaae56724/chrome/browser/ui/webui/side_panel/read_anything/read_anything_page_handler.cc


### ms...@google.com (2022-05-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-16)

Thank you for this report! Due to this issue requiring user interaction and destruction to trigger, the VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2022-10-06)

Issue no longer being reported, presumed fixed.

### is...@google.com (2022-10-06)

This issue was migrated from crbug.com/chromium/1320181?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059492)*
