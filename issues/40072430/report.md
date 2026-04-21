# Security: Container-Overflow in chrome_pdf::PDFiumRange::GetScreenRects

| Field | Value |
|-------|-------|
| **Issue ID** | [40072430](https://issues.chromium.org/issues/40072430) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pw...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2023-09-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Clicking on a specific Widget in the PDF causes a Container Overflow. I have attached a video demonstrating how to reproduce it.

The PDF file is still quite large and hasn't been minimized yet. Would it be acceptable to share it via Google Drive if you provide me with your email address?

**VERSION**  

Chrome Version: 118.0.5965.0 (Developer Build) (arm64)  

Operating System: MacOS 13.4.1 (c) (22F770820d)

**REPRODUCTION CASE**

1. Open poc.pdf.
2. Click on the Input Box on the 2nd page.
3. While pressing the PageDown key, continue clicking at the same location.

**CREDIT INFORMATION**  

Reporter credit: [pwn2car]

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 18.7 KB)
- [repro.mov](attachments/repro.mov) (video/quicktime, 2.3 MB)

## Timeline

### [Deleted User] (2023-09-15)

[Empty comment from Monorail migration]

### nh...@google.com (2023-09-15)

You can share the PoC with me

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2023-09-15)

[Empty comment from Monorail migration]

### pw...@gmail.com (2023-09-15)

I have shared poc with you through Google Drive.

https://drive.google.com/file/d/1YT0fnWOtKW1mg0wpP1w8w4Pz_EBgzxp3/view?usp=sharing

### [Deleted User] (2023-09-15)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2023-09-15)

It took a few tries, but I got it to repro locally.

### th...@chromium.org (2023-09-15)

nharper@: Can you set the security labels?

### th...@chromium.org (2023-09-15)

This is the local ASAN output, which has line numbers:

==1813807==ERROR: AddressSanitizer: container-overflow on address 0x5060003c4580 at pc 0x555eee65ec83 bp 0x7fffb0083070 sp 0x7fffb0083068
READ of size 8 at 0x5060003c4580 thread T0 (chrome)
    #0 0x555eee65ec82 in GetForDereference base/allocator/partition_allocator/pointers/raw_ptr.h:820:48
    #1 0x555eee65ec82 in operator-> base/allocator/partition_allocator/pointers/raw_ptr.h:577:12
    #2 0x555eee65ec82 in chrome_pdf::PDFiumRange::GetScreenRects(gfx::Point const&, double, chrome_pdf::PageOrientation) const pdf/pdfium/pdfium_range.cc:88:22
    #3 0x555eee5e5cce in chrome_pdf::PDFiumEngine::OnSelectionPositionChanged() pdf/pdfium/pdfium_engine.cc:3746:13
    #4 0x555eee5e743d in chrome_pdf::PDFiumEngine::ScrolledToYPosition(int) pdf/pdfium/pdfium_engine.cc:630:3
    #5 0x555f0191e894 in blink::WebPluginContainerImpl::ReportGeometry() third_party/blink/renderer/core/exported/web_plugin_container_impl.cc:545:16

0x5060003c4580 is located 0 bytes inside of 56-byte region [0x5060003c4580,0x5060003c45b8)
allocated by thread T0 (chrome) here:
    #0 0x555ede5c079d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x555eee61d869 in __libcpp_operator_new<unsigned long> third_party/libc++/src/include/new:272:10
    #2 0x555eee61d869 in __libcpp_allocate third_party/libc++/src/include/new:298:10
    #3 0x555eee61d869 in allocate third_party/libc++/src/include/__memory/allocator.h:114:38
    #4 0x555eee61d869 in __allocate_at_least<std::__Cr::allocator<chrome_pdf::PDFiumRange> > third_party/libc++/src/include/__memory/allocate_at_least.h:55:19
    #5 0x555eee61d869 in __split_buffer third_party/libc++/src/include/__split_buffer:377:29
    #6 0x555eee61d869 in void std::__Cr::vector<chrome_pdf::PDFiumRange, std::__Cr::allocator<chrome_pdf::PDFiumRange>>::__push_back_slow_path<chrome_pdf::PDFiumRange>(chrome_pdf::PDFiumRange&&) third_party/libc++/src/include/vector:1616:49
    #7 0x555eee5f8560 in push_back third_party/libc++/src/include/vector:1648:9
    #8 0x555eee5f8560 in chrome_pdf::PDFiumEngine::OnSingleClick(int, int) pdf/pdfium/pdfium_engine.cc:1205:14
    #9 0x555eee5f676c in chrome_pdf::PDFiumEngine::OnLeftMouseDown(blink::WebMouseEvent const&) pdf/pdfium/pdfium_engine.cc:1300:5
    #10 0x555eee5efc4b in OnMouseDown pdf/pdfium/pdfium_engine.cc:1193:14
    #11 0x555eee5efc4b in chrome_pdf::PDFiumEngine::HandleInputEvent(blink::WebInputEvent const&) pdf/pdfium/pdfium_engine.cc:944:12
    #12 0x555f097b209c in HandleWebInputEvent pdf/pdf_view_web_plugin.cc:2053:16
    #13 0x555f097b209c in chrome_pdf::PdfViewWebPlugin::HandleInputEvent(blink::WebCoalescedInputEvent const&, ui::Cursor*) pdf/pdf_view_web_plugin.cc:555:7
    #14 0x555f0191813e in blink::WebPluginContainerImpl::HandleMouseEvent(blink::MouseEvent&) third_party/blink/renderer/core/exported/web_plugin_container_impl.cc:832:20

### nh...@google.com (2023-09-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-15)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-09-16)

It's not too hard to prevent this issue, but I'm still looking into why it's happening in the first place. PDFiumEngine::OnFocusedAnnotationUpdated() is getting called in the middle of what appears to be a bunch of read operations.

### th...@chromium.org (2023-09-16)

Because PDFiumPage::GetTextPage() can trigger a page load, which can then call PDFiumPage::GetPage() and trigger JS within the PDF.

### [Deleted User] (2023-09-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2023-09-19)

Uploaded https://crrev.com/c/4875506 to try to fix this issue.

### [Deleted User] (2023-09-19)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-09-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e250e8eb2bf9f423a42ebca5ad7a98fcd32ce37c

commit e250e8eb2bf9f423a42ebca5ad7a98fcd32ce37c
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Sep 19 20:13:28 2023

PDF: Ensure page used in PDFiumRange are loaded

Currently, calling PDFiumRange::GetScreenRects() can trigger a PDFium
page load, which can have surprising side effects. Prevent this from
happening by ensuring the page is loaded in the PDFiumRange ctor, and
use the existing PDFiumPage::ScopedUnloadPreventer mechanism to prevent
page unloads while PDFiumRange is alive.

To make this work, update PDFiumPage::ScopedUnloadPreventer so it is
public, and make it copyable. Add a unit test to make sure copying
ScopedUnloadPreventer works as expected.

Bug: 1483194
Change-Id: I66b6050258b7f359982c9b73762f0dc0e64e0ed7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4875506
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1198572}

[modify] https://crrev.com/e250e8eb2bf9f423a42ebca5ad7a98fcd32ce37c/pdf/pdfium/pdfium_range.h
[modify] https://crrev.com/e250e8eb2bf9f423a42ebca5ad7a98fcd32ce37c/pdf/pdfium/pdfium_page.h
[modify] https://crrev.com/e250e8eb2bf9f423a42ebca5ad7a98fcd32ce37c/pdf/pdfium/pdfium_page_unittest.cc
[modify] https://crrev.com/e250e8eb2bf9f423a42ebca5ad7a98fcd32ce37c/pdf/pdfium/pdfium_range.cc
[modify] https://crrev.com/e250e8eb2bf9f423a42ebca5ad7a98fcd32ce37c/pdf/pdfium/pdfium_page.cc
[modify] https://crrev.com/e250e8eb2bf9f423a42ebca5ad7a98fcd32ce37c/pdf/pdfium/pdfium_engine.cc


### th...@chromium.org (2023-09-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-20)

Requesting merge to beta M118 because latest trunk commit (1198572) appears to be after beta branch point (1192594).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-20)

Merge review required: M118 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2023-09-20)

I defer the merge decision to the security team.

### am...@chromium.org (2023-09-28)

118 merge approved for https://crrev.com/c/4875506
Please merge this fix to branch 5993 by EOD Monday, 2 October so this fix can be included in the M118 Stable RC and included in the M118 Stable release on 10 October -- ty

### th...@chromium.org (2023-09-28)

M118 merge in CQ: https://crrev.com/c/4903317

### gi...@appspot.gserviceaccount.com (2023-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/03612bacdbd003dc390fe3f58ed172665a2253dc

commit 03612bacdbd003dc390fe3f58ed172665a2253dc
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Sep 29 00:23:48 2023

M118: PDF: Ensure page used in PDFiumRange are loaded

Currently, calling PDFiumRange::GetScreenRects() can trigger a PDFium
page load, which can have surprising side effects. Prevent this from
happening by ensuring the page is loaded in the PDFiumRange ctor, and
use the existing PDFiumPage::ScopedUnloadPreventer mechanism to prevent
page unloads while PDFiumRange is alive.

To make this work, update PDFiumPage::ScopedUnloadPreventer so it is
public, and make it copyable. Add a unit test to make sure copying
ScopedUnloadPreventer works as expected.

(cherry picked from commit e250e8eb2bf9f423a42ebca5ad7a98fcd32ce37c)

Bug: 1483194
Change-Id: I66b6050258b7f359982c9b73762f0dc0e64e0ed7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4875506
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1198572}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4903317
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5993@{#940}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/03612bacdbd003dc390fe3f58ed172665a2253dc/pdf/pdfium/pdfium_range.h
[modify] https://crrev.com/03612bacdbd003dc390fe3f58ed172665a2253dc/pdf/pdfium/pdfium_page.h
[modify] https://crrev.com/03612bacdbd003dc390fe3f58ed172665a2253dc/pdf/pdfium/pdfium_page_unittest.cc
[modify] https://crrev.com/03612bacdbd003dc390fe3f58ed172665a2253dc/pdf/pdfium/pdfium_range.cc
[modify] https://crrev.com/03612bacdbd003dc390fe3f58ed172665a2253dc/pdf/pdfium/pdfium_page.cc
[modify] https://crrev.com/03612bacdbd003dc390fe3f58ed172665a2253dc/pdf/pdfium/pdfium_engine.cc


### [Deleted User] (2023-09-29)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-09-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-29)

Congratulations on another one, pwn2car! The Chrome VRP Panel has decided to award you $1,000 for this report of a heavily mitigated security bug in a sandboxed process. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-30)

[Empty comment from Monorail migration]

### vo...@google.com (2023-10-04)

[Empty comment from Monorail migration]

### vo...@google.com (2023-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-05)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-10-05)

1. https://crrev.com/c/4911373
2. Low - small change and no conflicts
3. M118
4. Yes

### na...@google.com (2023-10-05)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### gm...@google.com (2023-10-24)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/08bde79c717f1cff2cc2c9beb34ed2970a0186d1

commit 08bde79c717f1cff2cc2c9beb34ed2970a0186d1
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Oct 25 13:26:21 2023

[M114-LTS] PDF: Ensure page used in PDFiumRange are loaded

Currently, calling PDFiumRange::GetScreenRects() can trigger a PDFium
page load, which can have surprising side effects. Prevent this from
happening by ensuring the page is loaded in the PDFiumRange ctor, and
use the existing PDFiumPage::ScopedUnloadPreventer mechanism to prevent
page unloads while PDFiumRange is alive.

To make this work, update PDFiumPage::ScopedUnloadPreventer so it is
public, and make it copyable. Add a unit test to make sure copying
ScopedUnloadPreventer works as expected.

(cherry picked from commit e250e8eb2bf9f423a42ebca5ad7a98fcd32ce37c)

(cherry picked from commit 03612bacdbd003dc390fe3f58ed172665a2253dc)

Bug: 1483194
Change-Id: I66b6050258b7f359982c9b73762f0dc0e64e0ed7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4875506
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1198572}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4903317
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/branch-heads/5993@{#940}
Cr-Original-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4911373
Reviewed-by: Lei Zhang <thestig@chromium.org>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1626}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/08bde79c717f1cff2cc2c9beb34ed2970a0186d1/pdf/pdfium/pdfium_range.h
[modify] https://crrev.com/08bde79c717f1cff2cc2c9beb34ed2970a0186d1/pdf/pdfium/pdfium_page.h
[modify] https://crrev.com/08bde79c717f1cff2cc2c9beb34ed2970a0186d1/pdf/pdfium/pdfium_page_unittest.cc
[modify] https://crrev.com/08bde79c717f1cff2cc2c9beb34ed2970a0186d1/pdf/pdfium/pdfium_range.cc
[modify] https://crrev.com/08bde79c717f1cff2cc2c9beb34ed2970a0186d1/pdf/pdfium/pdfium_page.cc
[modify] https://crrev.com/08bde79c717f1cff2cc2c9beb34ed2970a0186d1/pdf/pdfium/pdfium_engine.cc


### vo...@google.com (2023-10-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1483194?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072430)*
