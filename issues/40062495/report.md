# Security:  Integer overflows in CountPages

| Field | Value |
|-------|-------|
| **Issue ID** | [40062495](https://issues.chromium.org/issues/40062495) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vu...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2023-01-04 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

The function `CountPages` is a recursive function|2| in `pdfium/core/fpdfapi/parser/cpdf_document.cpp` file.

If the Pages Object has enough `Kids` and the Kid Object must have `Kids` key.

And we can control the Kid Object `Count` value |1|.The Kid Object `Count` value can be 0xFFFFE < CPDF\_Document::kPageMaxNum|1|.

```
int CountPages(RetainPtr<CPDF_Dictionary> pPages,  
               std::set<RetainPtr<CPDF_Dictionary>>\* visited_pages) {  
  int count = pPages->GetIntegerFor("Count");  
  if (count > 0 && count < CPDF_Document::kPageMaxNum)  
    return count;//\*\*\*1\*\*\*  
  RetainPtr<CPDF_Array> pKidList = pPages->GetMutableArrayFor("Kids");  
  if (!pKidList)  
    return 0;  
  count = 0;  
  for (size_t i = 0; i < pKidList->size(); i++) {  
    RetainPtr<CPDF_Dictionary> pKid = pKidList->GetMutableDictAt(i);  
    if (!pKid || pdfium::Contains(\*visited_pages, pKid))  
      continue;  
    if (pKid->KeyExist("Kids")) {  
      // Use |visited_pages| to help detect circular references of pages.  
      ScopedSetInsertion<RetainPtr<CPDF_Dictionary>> local_add(visited_pages,  
                                                               pKid);  
      count += CountPages(std::move(pKid), visited_pages);//\*\*\*2\*\*\*  
    } else {  
      // This page is a leaf node.  
      count++;  
    }  
  }  
  pPages->SetNewFor<CPDF_Number>("Count", count);  
  return count;  
}  

```

**REPRODUCTION CASE**  

pdfium\_test.exe poc.pdf

**CREDIT INFORMATION**  

Reporter credit: Zhiyi Zhang from Codesafe Team of Legendsec at QI-ANXIN Group

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 24.3 KB)
- [windbg.log](attachments/windbg.log) (text/plain, 3.2 KB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 12.2 KB)
- [patch.txt](attachments/patch.txt) (text/plain, 415 B)

## Timeline

### [Deleted User] (2023-01-04)

[Empty comment from Monorail migration]

### vu...@gmail.com (2023-01-04)

Bisect:
https://pdfium.googlesource.com/pdfium/+/215816b7450a577e186cc0e5f1634c4c6610b86b

### vu...@gmail.com (2023-01-04)

update poc.pdf

### da...@chromium.org (2023-01-04)

I'm not clear why this only occurs at that bisect point. The old code did:

-  for (FX_DWORD i = 0; i < pKidList->GetCount(); i++) {
-    CPDF_Dictionary* pKid = pKidList->GetDict(i);
-    if (!pKid) {
-      continue;
-    }
-    if (!pKid->KeyExist("Kids")) {
-      count++;
-    } else {
-      count += _CountPages(pKid, level + 1);
-    }
-  }

Which also looks like it should be possible to overflow. Nonetheless the change to the current code was 4 years ago.

[Monorail components: Internals>Plugins>PDF]

### da...@chromium.org (2023-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-04)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vu...@gmail.com (2023-01-05)

hi danakj, https://crbug.com/chromium/1404864#c4 .The old code limits the number of recursive function executions through the value of `level` to prevent integer overflow.
```
-static int _CountPages(CPDF_Dictionary* pPages, int level) {
-  if (level > 128) {
-    return 0;
-  }
-  int count = pPages->GetInteger("Count");
-  if (count > 0 && count < FPDF_PAGE_MAX_NUM) {
-    return count;
-  }
-  CPDF_Array* pKidList = pPages->GetArray("Kids");
-  if (!pKidList) {
-    return 0;
-  }
-  count = 0;
-  for (FX_DWORD i = 0; i < pKidList->GetCount(); i++) {
-    CPDF_Dictionary* pKid = pKidList->GetDict(i);
-    if (!pKid) {
-      continue;
-    }
-    if (!pKid->KeyExist("Kids")) {
-      count++;
-    } else {
-      count += _CountPages(pKid, level + 1);
-    }
-  }
-  pPages->SetAtInteger("Count", count);
-  return count;
-}
```
Patch Suggestion:
1. like the old code, limit the number of recursive function executions.
2. check the `count` value. 

### ts...@chromium.org (2023-01-05)

Lei, do you have time to take a look at this?

### vu...@gmail.com (2023-01-05)

[Comment Deleted]

### vu...@gmail.com (2023-01-05)

According to the understanding of the context, it is also necessary for the patch file to add detection for the maximum value
(CPDF_Document::kPageMaxNum) of count.

Patch.txt

```
diff --git a/core/fpdfapi/parser/cpdf_document.cpp b/core/fpdfapi/parser/cpdf_document.cpp

--- a/core/fpdfapi/parser/cpdf_document.cpp
+++ b/core/fpdfapi/parser/cpdf_document.cpp
@@ -48,6 +48,9 @@ int CountPages(CPDF_Dictionary* pPages,
       // This page is a leaf node.
       count++;
     }
+    if (count > CPDF_Document::kPageMaxNum) {
+      return 0;
+    }
   }
   pPages->SetNewFor<CPDF_Number>("Count", count);
   return count; 
```

### th...@chromium.org (2023-01-05)

Thanks for the suggestion. I've been working on basically  the same thing. Just uploaded https://pdfium-review.googlesource.com/103078

### vu...@gmail.com (2023-01-05)

[Comment Deleted]

### vu...@gmail.com (2023-01-05)

Thanks for accepting the patch suggestion I submitted.
https://pdfium-review.googlesource.com/103078 and https://crbug.com/chromium/1404864#c11 have a little flaw. If the `count` value is `0`.
So I provided a new patch https://crbug.com/chromium/1404864#c12 which avoids this problem.

### vu...@gmail.com (2023-01-05)

Add Bisect:

This bug was introduced in 2016 and affects all current (dev/beta/stable) versions.

### vu...@gmail.com (2023-01-06)

Maybe this is a better patch option. `count >= CPDF_Document::kPageMaxNum`

Patch.txt

```
diff --git a/core/fpdfapi/parser/cpdf_document.cpp b/core/fpdfapi/parser/cpdf_document.cpp

--- a/core/fpdfapi/parser/cpdf_document.cpp
+++ b/core/fpdfapi/parser/cpdf_document.cpp
@@ -48,6 +48,9 @@ int CountPages(CPDF_Dictionary* pPages,
       // This page is a leaf node.
       count++;
     }
+    if (count >= CPDF_Document::kPageMaxNum) {
+      return 0;
+    }
   }
   pPages->SetNewFor<CPDF_Number>("Count", count);
   re

### th...@chromium.org (2023-01-07)

Thanks for noticing the issue with the original solution. I added a test in https://pdfium-review.googlesource.com/103132 for that case.

Also thanks for the suggestion in https://crbug.com/chromium/1404864#c17, but I decided to use an Optional, so CountPages() can still bail out early on error.

### gi...@appspot.gserviceaccount.com (2023-01-12)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/5688d711a1d7104debb5651d71b14ee7dd3c8bcf

commit 5688d711a1d7104debb5651d71b14ee7dd3c8bcf
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Jan 12 20:24:54 2023

Validate the page count.

In CountPages(), which recursively calls itself, validate the page
count. When any part of the pages tree contains bad data, bail out.

Bug: chromium:1404864
Change-Id: Ifdbc14213ec3f963b4b2cb5793b83c15d03336e8
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/103078
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/5688d711a1d7104debb5651d71b14ee7dd3c8bcf/core/fpdfapi/parser/cpdf_document.cpp


### gi...@appspot.gserviceaccount.com (2023-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/da88c5430932f6cffd35c6915075fba6adf27ccd

commit da88c5430932f6cffd35c6915075fba6adf27ccd
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Jan 13 03:42:12 2023

Roll PDFium from 5e8468a4179b to a4147f8478c7 (13 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/5e8468a4179b..a4147f8478c7

2023-01-13 tsepez@chromium.org Revert "Hide FPDF_GetArrayBufferAllocatorSharedInstance() for incompatible V8"
2023-01-13 asweintraub@google.com Resolves the following technical debt issue:
2023-01-13 asweintraub@google.com Resolves the following technical debt issue:
2023-01-13 asweintraub@google.com Resolves 3 instances of the following issue:
2023-01-13 asweintraub@google.com Resolves the following technical debt issue:
2023-01-12 asweintraub@google.com Resolves the following 11 technical debt issues:
2023-01-12 nigi@chromium.org Remove bug_691967.pdf from the suppression list
2023-01-12 andyphan@chromium.org Add regression test for rendering long dashed lines
2023-01-12 thestig@chromium.org Restrict the object types that FPDF_CopyViewerPreferences() copies.
2023-01-12 thestig@chromium.org Validate the page count.
2023-01-12 thestig@chromium.org Add FPDFViewEmbedderTest.DocumentWithEmptyPageTreeNode.
2023-01-12 nigi@chromium.org Update Skia expectation for radial_shading_point_at_border.in
2023-01-12 tsepez@chromium.org Hide FPDF_GetArrayBufferAllocatorSharedInstance() for incompatible V8

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1325244,chromium:1404202,chromium:1404864
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I3cd29b14dddab57cf8cce8402e68979598eeba58
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4162253
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1092227}

[modify] https://crrev.com/da88c5430932f6cffd35c6915075fba6adf27ccd/DEPS


### th...@chromium.org (2023-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations, Zhiyi! The VRP Panel has decided to award you $10,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### vu...@gmail.com (2023-02-02)

Thanks Amy!

### am...@chromium.org (2023-02-02)

For some reason the bot did not request merge approval for this issue. Since M110 becomes Stable next week, please merge this issue to M110, branch 5418 so this fix can be included in the first M110/Stable refresh. Thank you! 

### th...@chromium.org (2023-02-02)

Ack. Will merge.

### am...@chromium.org (2023-02-02)

apologies for my muddled message above, should have just simply said "please merge this fix" rather than this issue; 

### gi...@appspot.gserviceaccount.com (2023-02-02)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/b15f1b6966496c72391a0e2a1e20b4e6c28536fc

commit b15f1b6966496c72391a0e2a1e20b4e6c28536fc
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Feb 02 21:44:09 2023

M110: Validate the page count.

In CountPages(), which recursively calls itself, validate the page
count. When any part of the pages tree contains bad data, bail out.

Bug: chromium:1404864
Change-Id: Ifdbc14213ec3f963b4b2cb5793b83c15d03336e8
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/103078
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 5688d711a1d7104debb5651d71b14ee7dd3c8bcf)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/103570

[modify] https://pdfium.googlesource.com/pdfium/+/b15f1b6966496c72391a0e2a1e20b4e6c28536fc/core/fpdfapi/parser/cpdf_document.cpp


### vu...@gmail.com (2023-02-09)

hello , Chrome 110 stable version has been released, but I don't see the CVE number about this case .

### am...@chromium.org (2023-02-09)

Hello. Please see https://crbug.com/chromium/1404864#c28. This fix was backmerged to M110 after the first ‘M110 Stable release was cut on 31 January, which was released yesterday. This fix will ship in the first Stable refresh on 21 February. 

### am...@chromium.org (2023-02-20)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1404864?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062495)*
