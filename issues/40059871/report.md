# Security: heap-buffer-overflow in chrome_pdf::PDFiumEngine::GetNamedDestination

| Field | Value |
|-------|-------|
| **Issue ID** | [40059871](https://issues.chromium.org/issues/40059871) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac |
| **Reporter** | tr...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2022-06-06 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

pdf/pdfium/pdfium\_engine.cc

```
absl::optional<PDFEngine::NamedDestination> PDFiumEngine::GetNamedDestination(  
    const std::string& destination) {  
  // Look for the destination.  
  FPDF_DEST dest = FPDF_GetNamedDestByName(doc(), destination.c_str());  
  if (!dest) {  
    // Look for a bookmark with the same name.  
    std::u16string destination_wide = base::UTF8ToUTF16(destination);  
    FPDF_WIDESTRING destination_pdf_wide =  
        reinterpret_cast<FPDF_WIDESTRING>(destination_wide.c_str());  
    FPDF_BOOKMARK bookmark = FPDFBookmark_Find(doc(), destination_pdf_wide);  
    if (bookmark)  
      dest = FPDFBookmark_GetDest(doc(), bookmark);  
  }  
  
  if (!dest)  
    return {};  
  
  int page = FPDFDest_GetDestPageIndex(doc(), dest); // \*\*\*\*\* 1 \*\*\*\*\*  
  if (page < 0)  
    return {};  
  
  PDFEngine::NamedDestination result;  
  result.page = page;  
  unsigned long view_int =  
      FPDFDest_GetView(dest, &result.num_params, result.params);  
  
  // FPDFDest_GetView() gets the in-page coordinates directly from the PDF  
  // document. The in-page coordinates need to be transformed into in-screen  
  // coordinates before getting sent to the viewport.  
  PDFiumPage\* page_ptr = pages_[page].get(); // \*\*\*\*\* 2 \*\*\*\*\*  
  ParamsTransformPageToScreen(view_int, page_ptr, result.params); // \*\*\*\*\* 3 \*\*\*\*\*  
  
  if (view_int == PDFDEST_VIEW_XYZ)  
    result.xyz_params = GetXYZParamsString(dest, page_ptr); // \*\*\*\*\* 4 \*\*\*\*\*\*  
  
  result.view = ConvertViewIntToViewString(view_int);  
  return result;  
}  

```

A value of integer type variable named `page` retrieved from function call `FPDFDest_GetDestPageIndex` [1]. It is later used as index of `pages_` vector of `std::unique_ptr<PDFiumPage>` to obtain `PDFiumPage` pointer, named `page_ptr` [2].

The problem is that there is no boundary checks are performed between [1] and [2]. As a result, Out-of-bounds accesses can occur in [2] and `page_ptr` can points unintended address. The malformed `page_ptr` is later used in [3] and [4].

**VERSION**  

Chrome Version: Version 104.0.5103.0 (Developer Build) (64-bit)  

Operating System: Ubuntu 20.04 x64  

Chromium commit: e8bd9641fddf5246cb63d70839096b832cedd630  

Build options: is\_debug=false is\_asan=true dcheck\_always\_on=false

**REPRODUCTION CASE**  

Open `load.html`

**CREDIT INFORMATION**  

Reporter credit: triplepwns

## Attachments

- [asan_log.txt](attachments/asan_log.txt) (text/plain, 15.8 KB)
- [load.html](attachments/load.html) (text/plain, 46 B)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 124 B)

## Timeline

### [Deleted User] (2022-06-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5205640758886400.

### cl...@chromium.org (2022-06-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-07)

Detailed Report: https://clusterfuzz.com/testcase?key=5205640758886400

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x6090001ad358
Crash State:
  chrome_pdf::PdfViewPluginBase::HandleGetNamedDestinationMessage
  chrome_pdf::PdfViewPluginBase::HandleMessage
  base::internal::Invoker<base::internal::BindState<void
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1011084

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5205640758886400

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### cl...@chromium.org (2022-06-07)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Core Internals>Plugins>PDF]

### [Deleted User] (2022-06-07)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-07)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-06-07)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Core]

### th...@chromium.org (2022-06-07)

Looks like r535877 or some earlier CL did not do the bound check, but that wasn't a problem because it simply got returned as an int. It wasn't until r843710 where `page` was being used to access `pages_`, thus making this issue possible.

### ni...@chromium.org (2022-06-08)

[Empty comment from Monorail migration]

### tr...@gmail.com (2022-06-08)

Additionally, I think it affects stable chrome (102.0.5005.61) and it is exploitable bug. A attacker can controls PDFiumPage pointer and Call chains from `ParamsTransformPageToScreen` function uses it. e.g. `ParamsTransformPageToScreen` -> `PDFiumPage::TransformPageToScreenY` -> `PDFiumPage::GetPage`. It lead to write member variable(engine_, page_, ...) or access another pointer(page_, ...) includes vtable.

### gi...@appspot.gserviceaccount.com (2022-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/03f42df3bdbca820dc813e70bad48b3aeb6e7632

commit 03f42df3bdbca820dc813e70bad48b3aeb6e7632
Author: Hui Yingst <nigi@chromium.org>
Date: Thu Jun 09 23:39:42 2022

Handle out-of-range page numbers from named destinations.

A named destination in a PDF file sometimes can contain an out-of-range
page number, which will trigger out-of-bounds accesses in
PDFiumEngine::GetNamedDestination().

This CL makes PDFiumEngine::GetNamedDestination() treat an invalid page
number as an error and return an empty result. Also adds a unit test
for this function to test getting both valid and invalid page
destinations.

Bug: 1333374
Change-Id: I8a62274146430c6f4bf170f652d4b158d907924b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3696844
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Nigi <nigi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1012771}

[add] https://crrev.com/03f42df3bdbca820dc813e70bad48b3aeb6e7632/pdf/test/data/named_destinations.in
[add] https://crrev.com/03f42df3bdbca820dc813e70bad48b3aeb6e7632/pdf/test/data/named_destinations.pdf
[modify] https://crrev.com/03f42df3bdbca820dc813e70bad48b3aeb6e7632/pdf/pdfium/pdfium_engine_unittest.cc
[modify] https://crrev.com/03f42df3bdbca820dc813e70bad48b3aeb6e7632/pdf/pdfium/pdfium_engine.cc


### ni...@chromium.org (2022-06-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-10)

ClusterFuzz testcase 5205640758886400 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1012766:1012771

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### th...@chromium.org (2022-06-10)

This bug has existed since 89.0.4389.0. We'll work with the release managers to figure out what branches the fix will get merged back to.

### tr...@gmail.com (2022-06-11)

Could you re-consider security severity for this? Previously similar bug was reported and it's severity is High: (https://bugs.chromium.org/p/chromium/issues/detail?id=1283198). As mentioned in https://crbug.com/chromium/1333374#c12, this bug is exploitable.

### th...@chromium.org (2022-06-11)

I believe a human from the security team will look this over. So far a lot of the triage has been done automatically by a bot, and we know how trustworthy they are...

### [Deleted User] (2022-06-11)

Requesting merge to dev M104 because latest trunk commit (1012771) appears to be after dev branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-11)

Merge approved: your change passed merge requirements and is auto-approved for M104. Please go ahead and merge the CL to branch 5112 (refs/branch-heads/5112) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-06-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9bde86769f09bb74a2292fc31f4cbe54dbd4297a

commit 9bde86769f09bb74a2292fc31f4cbe54dbd4297a
Author: Hui Yingst <nigi@chromium.org>
Date: Mon Jun 13 19:59:16 2022

Handle out-of-range page numbers from named destinations.

A named destination in a PDF file sometimes can contain an out-of-range
page number, which will trigger out-of-bounds accesses in
PDFiumEngine::GetNamedDestination().

This CL makes PDFiumEngine::GetNamedDestination() treat an invalid page
number as an error and return an empty result. Also adds a unit test
for this function to test getting both valid and invalid page
destinations.

(cherry picked from commit 03f42df3bdbca820dc813e70bad48b3aeb6e7632)

Bug: 1333374
Change-Id: I8a62274146430c6f4bf170f652d4b158d907924b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3696844
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Nigi <nigi@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1012771}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3703483
Auto-Submit: Nigi <nigi@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#37}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[add] https://crrev.com/9bde86769f09bb74a2292fc31f4cbe54dbd4297a/pdf/test/data/named_destinations.in
[add] https://crrev.com/9bde86769f09bb74a2292fc31f4cbe54dbd4297a/pdf/test/data/named_destinations.pdf
[modify] https://crrev.com/9bde86769f09bb74a2292fc31f4cbe54dbd4297a/pdf/pdfium/pdfium_engine_unittest.cc
[modify] https://crrev.com/9bde86769f09bb74a2292fc31f4cbe54dbd4297a/pdf/pdfium/pdfium_engine.cc


### tr...@gmail.com (2022-07-08)

May I ask when is reward for this report will be confirmed?
Thanks for Google team's efforts for security. 

### th...@chromium.org (2022-07-08)

Hopefully a week or 2? Some folks may be out on summer holiday, so things are a bit slower than normal.

### tr...@gmail.com (2022-07-08)

Oh I didn't think about summer holiday period. Thanks for you anwser. Have a nice day!

### am...@chromium.org (2022-07-08)

Hello, yes, this bug report is in our queue for VRP review and will be reviewed at a future session. Many folks have been and are on travel right now, so we are still reviewing bugs, just at a slower capacity. Thank you for your patience. 

### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-28)

Congratulations, triplepwns! The the VRP Panel has decide to award you $7500 for this report. Thank you for your efforts in reporting this issue to us and great work! 

### am...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### tr...@gmail.com (2022-08-29)

Is this bug eligible to get CVE?

### am...@chromium.org (2022-08-29)

Hello, as this issue was discovered and impacted Head, it was fixed before impact to a Stable channel release and would not receive a CVE. 

### th...@chromium.org (2022-08-29)

I'm not sure how ClusterFuzz determined Security_Impact-Head, but r843710 introduced the access to `pages_[page]`, and that was first in the 89.0.4389.0 release.

### th...@chromium.org (2022-08-29)

Based on the metadata section on https://clusterfuzz.com/testcase-detail/5205640758886400, it looks like ClusterFuzz failed to do the regression phase properly.

ochang@ / metzman@: Is this a known issue?

### tr...@gmail.com (2022-09-08)

As described in https://crbug.com/chromium/1333374#c18 and https://crbug.com/chromium/1333374#c33, I believe it had impacted stable versions. Please check if it is eligible for receiving CVE.

Thanks.

### [Deleted User] (2022-09-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1333374?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059871)*
