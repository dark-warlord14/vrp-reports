# pdfium (XFA): wrong object type in CXFA_FFNotify::OpenDropDownList

| Field | Value |
|-------|-------|
| **Issue ID** | [40051296](https://issues.chromium.org/issues/40051296) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-01-19 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.130 Safari/537.36

Steps to reproduce the problem:
xfa/fxfa/cxfa_ffnotify.cpp:53:10: runtime error: downcast of address 0x55d5a648f3a0 which does not point to an object of type 'CXFA_FFComboBox'
0x55d5a648f3a0: note: object is of type 'CXFA_FFListBox'
 00 00 00 00  a0 2d a1 a4 d5 55 00 00  c0 43 4b a6 d5 55 00 00  c0 43 4b a6 d5 55 00 00  02 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CXFA_FFListBox'
    #0 0x55d5a40317ed in (anonymous namespace)::ToComboBox(CXFA_FFWidget*) xfa/fxfa/cxfa_ffnotify.cpp:53:10
    #1 0x55d5a4031549 in CXFA_FFNotify::OpenDropDownList(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:277:3
    #2 0x55d5a2d75918 in CJX_HostPseudoModel::openList(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:300:14

xfa/fxfa/cxfa_ffnotify.cpp:277:24: runtime error: member call on address 0x55d5a648f3a0 which does not point to an object of type 'CXFA_FFComboBox'
0x55d5a648f3a0: note: object is of type 'CXFA_FFListBox'
 00 00 00 00  a0 2d a1 a4 d5 55 00 00  c0 43 4b a6 d5 55 00 00  c0 43 4b a6 d5 55 00 00  02 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CXFA_FFListBox'
    #0 0x55d5a403173e in CXFA_FFNotify::OpenDropDownList(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:277:24
    #1 0x55d5a2d75918 in CJX_HostPseudoModel::openList(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:300:14

xfa/fxfa/cxfa_ffcombobox.cpp:23:10: runtime error: downcast of address 0x55d5a64a4bb0 which does not point to an object of type 'CFWL_ComboBox'
0x55d5a64a4bb0: note: object is of type 'CFWL_ListBox'
 00 00 00 00  98 c1 a1 a4 d5 55 00 00  c0 4b 4a a6 d5 55 00 00  00 00 00 00 00 00 00 00  00 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CFWL_ListBox'
    #0 0x55d5a3ff3f7d in (anonymous namespace)::ToComboBox(CFWL_Widget*) xfa/fxfa/cxfa_ffcombobox.cpp:23:10
    #1 0x55d5a3ff5f78 in CXFA_FFComboBox::OpenDropDownList() xfa/fxfa/cxfa_ffcombobox.cpp:120:3
    #2 0x55d5a40315a6 in CXFA_FFNotify::OpenDropDownList(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:277:24
    #3 0x55d5a2d75918 in CJX_HostPseudoModel::openList(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:300:14

xfa/fxfa/cxfa_ffcombobox.cpp:120:34: runtime error: member call on address 0x55d5a64a4bb0 which does not point to an object of type 'CFWL_ComboBox'
0x55d5a64a4bb0: note: object is of type 'CFWL_ListBox'
 00 00 00 00  98 c1 a1 a4 d5 55 00 00  c0 4b 4a a6 d5 55 00 00  00 00 00 00 00 00 00 00  00 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CFWL_ListBox'
    #0 0x55d5a3ff601d in CXFA_FFComboBox::OpenDropDownList() xfa/fxfa/cxfa_ffcombobox.cpp:120:34
    #1 0x55d5a40315a6 in CXFA_FFNotify::OpenDropDownList(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:277:24
    #2 0x55d5a2d75918 in CJX_HostPseudoModel::openList(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:300:14

xfa/fwl/cfwl_combobox.cpp:195:3: runtime error: member call on address 0x55d5a64a4bb0 which does not point to an object of type 'CFWL_ComboBox'
0x55d5a64a4bb0: note: object is of type 'CFWL_ListBox'
 00 00 00 00  98 c1 a1 a4 d5 55 00 00  c0 4b 4a a6 d5 55 00 00  00 00 00 00 00 00 00 00  00 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CFWL_ListBox'
    #0 0x55d5a412317e in CFWL_ComboBox::OpenDropDownList(bool) xfa/fwl/cfwl_combobox.cpp:195:3
    #1 0x55d5a3ff5fcb in CXFA_FFComboBox::OpenDropDownList() xfa/fxfa/cxfa_ffcombobox.cpp:120:34
    #2 0x55d5a40315a6 in CXFA_FFNotify::OpenDropDownList(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:277:24
    #3 0x55d5a2d75918 in CJX_HostPseudoModel::openList(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:300:14

xfa/fwl/cfwl_combobox.cpp:216:7: runtime error: member call on address 0x55d5a64a4bb0 which does not point to an object of type 'CFWL_ComboBox'
0x55d5a64a4bb0: note: object is of type 'CFWL_ListBox'
 00 00 00 00  98 c1 a1 a4 d5 55 00 00  c0 4b 4a a6 d5 55 00 00  00 00 00 00 00 00 00 00  00 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CFWL_ListBox'
    #0 0x55d5a4123ba1 in CFWL_ComboBox::ShowDropList(bool) xfa/fwl/cfwl_combobox.cpp:216:7
    #1 0x55d5a412315a in CFWL_ComboBox::OpenDropDownList(bool) xfa/fwl/cfwl_combobox.cpp:195:3
    #2 0x55d5a3ff5fcb in CXFA_FFComboBox::OpenDropDownList() xfa/fxfa/cxfa_ffcombobox.cpp:120:34
    #3 0x55d5a40315a6 in CXFA_FFNotify::OpenDropDownList(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:277:24
    #4 0x55d5a2d75918 in CJX_HostPseudoModel::openList(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:300:14

xfa/fwl/cfwl_combobox.h:116:43: runtime error: member access within address 0x55d5a64a4bb0 which does not point to an object of type 'const CFWL_ComboBox'
0x55d5a64a4bb0: note: object is of type 'CFWL_ListBox'
 00 00 00 00  98 c1 a1 a4 d5 55 00 00  c0 4b 4a a6 d5 55 00 00  00 00 00 00 00 00 00 00  00 00 00 00
              ^~~~~~~~~~~~~~~~~~~~~~~
              vptr for 'CFWL_ListBox'
    #0 0x55d5a4120cee in CFWL_ComboBox::IsDropListVisible() const xfa/fwl/cfwl_combobox.h:116:43
    #1 0x55d5a4123218 in CFWL_ComboBox::ShowDropList(bool) xfa/fwl/cfwl_combobox.cpp:216:7
    #2 0x55d5a412315a in CFWL_ComboBox::OpenDropDownList(bool) xfa/fwl/cfwl_combobox.cpp:195:3
    #3 0x55d5a3ff5fcb in CXFA_FFComboBox::OpenDropDownList() xfa/fxfa/cxfa_ffcombobox.cpp:120:34
    #4 0x55d5a40315a6 in CXFA_FFNotify::OpenDropDownList(CXFA_Node*) xfa/fxfa/cxfa_ffnotify.cpp:277:24
    #5 0x55d5a2d75918 in CJX_HostPseudoModel::openList(CFX_V8*, std::__1::vector<v8::Local<v8::Value>, std::__1::allocator<v8::Local<v8::Value> > > const&) fxjs/xfa/cjx_hostpseudomodel.cpp:300:14

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 78.0.3904.130  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-1043508.pdf](attachments/chromium-1043508.pdf) (application/pdf, 728 B)

## Timeline

### pd...@gmail.com (2020-01-19)

[Empty comment from Monorail migration]

### pd...@gmail.com (2020-01-19)

Note: Chrome doesn't use XFA.

### ct...@chromium.org (2020-01-21)

Tentatively setting Severity-High for type confusion.

[Monorail components: Internals>Plugins>PDF]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-23)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/02b6176bd77acf5672f56f1091ce5e495e5687fc

commit 02b6176bd77acf5672f56f1091ce5e495e5687fc
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Jan 23 18:15:08 2020

Avoid casting CXFA_FFListBox to CXFA_FFComboBox.

They are different subclasses of CXFA_FFDropDown.

Bug: chromium:1043508
Change-Id: If8ea04117ce3c7d2c4e1256b8c0b5b6bde593bad
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/65450
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/02b6176bd77acf5672f56f1091ce5e495e5687fc/xfa/fxfa/cxfa_ffdropdown.h
[modify] https://pdfium.googlesource.com/pdfium/+/02b6176bd77acf5672f56f1091ce5e495e5687fc/xfa/fxfa/cxfa_ffcombobox.h
[modify] https://pdfium.googlesource.com/pdfium/+/02b6176bd77acf5672f56f1091ce5e495e5687fc/xfa/fxfa/cxfa_ffnotify.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/02b6176bd77acf5672f56f1091ce5e495e5687fc/xfa/fxfa/cxfa_ffdropdown.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/02b6176bd77acf5672f56f1091ce5e495e5687fc/xfa/fxfa/cxfa_ffcombobox.cpp


### ts...@chromium.org (2020-01-23)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/388ddae23eb169260fe640dc3b6ed13c24f40288

commit 388ddae23eb169260fe640dc3b6ed13c24f40288
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jan 23 22:03:58 2020

Roll src/third_party/pdfium c040c8f85051..e386b83c7d0a (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/c040c8f85051..e386b83c7d0a

git log c040c8f85051..e386b83c7d0a --date=short --first-parent --format='%ad %ae %s'
2020-01-23 thestig@chromium.org Roll third_party/freetype/src/ 50b013871..e5038be70 (2 commits)
2020-01-23 maawas@microsoft.com Adding password form flag for text fields in fpdf_annot.h
2020-01-23 tsepez@chromium.org Avoid casting CXFA_FFListBox to CXFA_FFComboBox.
2020-01-23 maawas@microsoft.com Move get form field logic to common method in fpdf_annot.h
2020-01-23 nigi@chromium.org Add a pixel test with invalid bfranges inside ToUnicode map.

Created with:
  gclient setdep -r src/third_party/pdfium@e386b83c7d0a

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1021762,chromium:1043508
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I1f35a228e82af5e7b7169f2f5e7d07b891d6a5b9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2017655
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#734599}

[modify] https://crrev.com/388ddae23eb169260fe640dc3b6ed13c24f40288/DEPS


### sh...@chromium.org (2020-01-24)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-30)

Congrats! The Panel decided to award $5,000 for this report!

### na...@google.com (2020-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-30)

This issue was migrated from crbug.com/chromium/1043508?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051296)*
