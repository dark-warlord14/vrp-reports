# Security: heap-use-after-free in CPDF_FormField::ResetField()

| Field | Value |
|-------|-------|
| **Issue ID** | [40060720](https://issues.chromium.org/issues/40060720) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | tr...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2022-08-30 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

```
// third_party/pdfium/core/fpdfapi/parser/cpdf_indirect_object_holder.h  
class CPDF_IndirectObjectHolder {  
 // ...  
 std::map<uint32_t, RetainPtr<CPDF_Object>> m_IndirectObjs;  
 // ...  

```

CPDF\_Document inherits CPDF\_IndirectObjectHolder and it owns indirect objects used from single pdf document.  

The key of m\_IndirectObjs indicates indirect object number and a value indicates matchted CPDF\_Object.

It is UAF bug is caused by integer overflow. this issue can be triggerd by combining three primitives.  

(1) Increasing last indirect object number  

(2) Setting huge last object number  

(3) Overflow checking for last object number is missing

Once new indirect object is needed (dynamically), it increase last object number(m\_LastObjNum) and place newly created object with it.

```
// third_party/pdfium/core/fpdfapi/parser/cpdf_indirect_object_holder.cpp  
CPDF_Object\* CPDF_IndirectObjectHolder::AddIndirectObject(  
    RetainPtr<CPDF_Object> pObj) {  
  CHECK(!pObj->GetObjNum());  
  pObj->SetObjNum(++m_LastObjNum);  
  
  auto& obj_holder = m_IndirectObjs[m_LastObjNum];  
  obj_holder = std::move(pObj);  
  return obj_holder.Get();  
}  

```

The last object number, m\_LastObjNum, also be updated once higher indirect object is parsed[1][2].

```
// third_party/pdfium/core/fpdfapi/parser/cpdf_indirect_object_holder.cpp  
CPDF_Object\* CPDF_IndirectObjectHolder::GetOrParseIndirectObject(  
    uint32_t objnum) {  
  if (objnum == 0 || objnum == CPDF_Object::kInvalidObjNum)  
    return nullptr;  
  
  // Add item anyway to prevent recursively parsing of same object.  
  auto insert_result = m_IndirectObjs.insert(std::make_pair(objnum, nullptr));  
  if (!insert_result.second)  
    return FilterInvalidObjNum(insert_result.first->second.Get());  
  
  RetainPtr<CPDF_Object> pNewObj = ParseIndirectObject(objnum);  
  if (!pNewObj) {  
    m_IndirectObjs.erase(insert_result.first);  
    return nullptr;  
  }  
  
  pNewObj->SetObjNum(objnum);  
  m_LastObjNum = std::max(m_LastObjNum, objnum);  // \*\*\*\*\* 1 \*\*\*\*\*  
  insert_result.first->second = std::move(pNewObj);  
  return insert_result.first->second.Get();  
}  
  
bool CPDF_IndirectObjectHolder::ReplaceIndirectObjectIfHigherGeneration(  
    uint32_t objnum,  
    RetainPtr<CPDF_Object> pObj) {  
  DCHECK(objnum);  
  if (!pObj || objnum == CPDF_Object::kInvalidObjNum)  
    return false;  
  
  auto& obj_holder = m_IndirectObjs[objnum];  
  const CPDF_Object\* old_object = FilterInvalidObjNum(obj_holder.Get());  
  if (old_object && pObj->GetGenNum() <= old_object->GetGenNum())  
    return false;  
  
  pObj->SetObjNum(objnum);  
  obj_holder = std::move(pObj);  
  m_LastObjNum = std::max(m_LastObjNum, objnum);  // \*\*\*\*\* 2 \*\*\*\*\*  
  return true;  
}  

```

Normally PDF document cannot have object with extremely huge number.  

PDFium checks object number during parsing process and limits max object number is 4 \* 1024 \* 1024.

```
// third_party/pdfium/core/fpdfapi/parser/cpdf_parser.h  
  
  // A limit on the maximum object number in the xref table. Theoretical limits  
  // are higher, but this may be large enough in practice.  
  // Note: This was 1M, but https://crbug.com/910009 encountered a PDF with  
  // object numbers in the 1.7M range. The PDF only has 10K objects, but they  
  // are non-consecutive.  
  static constexpr uint32_t kMaxObjectNumber = 4 \* 1024 \* 1024;  

```
```
// third_party/pdfium/core/fpdfapi/parser/cpdf_hint_tables.cpp  
bool CPDF_HintTables::ReadPageHintTable(CFX_BitStream\* hStream) {  
  // ...  
  uint32_t dwStartObjNum = 1;  
  for (uint32_t i = 0; i < nPages; ++i) {  
    FX_SAFE_UINT32 safeDeltaObj = hStream->GetBits(dwDeltaObjectsBits);  
    safeDeltaObj += dwObjLeastNum;  
    if (!safeDeltaObj.IsValid())  
      return false;  
    m_PageInfos[i].set_objects_count(safeDeltaObj.ValueOrDie());  
    if (i == nFirstPageNum)  
      continue;  
    m_PageInfos[i].set_start_obj_num(dwStartObjNum);   // \*\*\*\*\* 5 \*\*\*\*\*  
    dwStartObjNum += m_PageInfos[i].objects_count();  
  // ...  

```
```
// third_party/pdfium/core/fpdfapi/parser/cpdf_data_avail.cpp  
const CPDF_Dictionary\* CPDF_DataAvail::GetPageDictionary(int index) const {  
  if (!m_pDocument || index < 0 || index >= GetPageCount())  
    return nullptr;  
  const CPDF_Dictionary\* page = m_pDocument->GetPageDictionary(index);  
  if (page)  
    return page;  
  if (!m_pLinearized || !m_pHintTables)  
    return nullptr;  
  
  if (index == static_cast<int>(m_pLinearized->GetFirstPageNo()))  
    return nullptr;  
  FX_FILESIZE szPageStartPos = 0;  
  FX_FILESIZE szPageLength = 0;  
  uint32_t dwObjNum = 0;  
  const bool bPagePosGot = m_pHintTables->GetPagePos(index, &szPageStartPos,   // \*\*\*\*\* 3 \*\*\*\*\*  
                                                     &szPageLength, &dwObjNum);  
  if (!bPagePosGot || !dwObjNum)  
    return nullptr;  
  // We should say to the document, which object is the page.  
  m_pDocument->SetPageObjNum(index, dwObjNum);  
  // Page object already can be parsed in document.  
  if (!m_pDocument->GetIndirectObject(dwObjNum)) {  
    m_pDocument->ReplaceIndirectObjectIfHigherGeneration(  
        dwObjNum,  
        ParseIndirectObjectAt(szPageStartPos, dwObjNum, m_pDocument.Get()));  // \*\*\*\*\* 4 \*\*\*\*\*  
  }  
  if (!ValidatePage(index))  
    return nullptr;  
  return m_pDocument->GetPageDictionary(index);  
}  

```

For Linearized PDF, CPDF\_DataAvail::GetPageDictionary() tries to get CPDF\_Object of page based on hint table. Unlike normal pdf, it is able to set huge object number in hint table[5] and parser doesn't check whether object have huge indirect number[4].

By combining these primitives, it is possible to free indirect objects owned by CPDF\_Document.

(1) Placing victim(will-be-freed) CPDF\_Object with indirect small number like 0, 1, 2 ...  

(2) Setting huge indirect number  

(3) Create indirect objects repeatedly. m\_LastObjNum will be overflowed and objects in front will be replaced and freed by CPDF\_IndirectObjectHolder::AddIndirectObject()  

(4) Dangling pointer is made

Attached pdf file and sanitizer logs show UAF bug caused from this scenario.

**VERSION**  

Chrome Version: Stable / 107.0.5269.0 (Commit 396799b65ad67a7ea10bbdeb1d75029d297bb520)  

Operating System: Ubuntu 20.04 x64

**REPRODUCTION CASE**  

Open `poc.pdf`

**CREDIT INFORMATION**  

Reporter credit: triplepwns

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 12.6 KB)
- [asan.log](attachments/asan.log) (text/plain, 25.6 KB)

## Timeline

### [Deleted User] (2022-08-30)

[Empty comment from Monorail migration]

### tr...@gmail.com (2022-08-30)

```cpp
// third_party/pdfium/core/fpdfapi/parser/cpdf_indirect_object_holder.cpp
CPDF_Object* CPDF_IndirectObjectHolder::GetIndirectObject(
    uint32_t objnum) const {
  auto it = m_IndirectObjs.find(objnum);
  return (it != m_IndirectObjs.end()) ? FilterInvalidObjNum(it->second.Get())  // ***** 3 *****
                                      : nullptr;
}

const CPDF_Dictionary* CPDF_DataAvail::GetPageDictionary(int index) const {
  if (!m_pDocument || index < 0 || index >= GetPageCount())
    return nullptr;
  const CPDF_Dictionary* page = m_pDocument->GetPageDictionary(index);
  if (page)
    return page;
  if (!m_pLinearized || !m_pHintTables)
    return nullptr;

  if (index == static_cast<int>(m_pLinearized->GetFirstPageNo()))
    return nullptr;
  FX_FILESIZE szPageStartPos = 0;
  FX_FILESIZE szPageLength = 0;
  uint32_t dwObjNum = 0;
  const bool bPagePosGot = m_pHintTables->GetPagePos(index, &szPageStartPos,
                                                     &szPageLength, &dwObjNum);
  if (!bPagePosGot || !dwObjNum)
    return nullptr;
  // We should say to the document, which object is the page.
  m_pDocument->SetPageObjNum(index, dwObjNum);
  // Page object already can be parsed in document.  // ***** 4 *****
  if (!m_pDocument->GetIndirectObject(dwObjNum)) {  // ***** 1 *****
    m_pDocument->ReplaceIndirectObjectIfHigherGeneration(  // ***** 2 *****
        dwObjNum,
        ParseIndirectObjectAt(szPageStartPos, dwObjNum, m_pDocument.Get()));
  }
  if (!ValidatePage(index))
    return nullptr;
  return m_pDocument->GetPageDictionary(index);
}

bool CPDF_IndirectObjectHolder::ReplaceIndirectObjectIfHigherGeneration(
    uint32_t objnum,
    RetainPtr<CPDF_Object> pObj) {
  DCHECK(objnum);
  if (!pObj || objnum == CPDF_Object::kInvalidObjNum)
    return false;

  auto& obj_holder = m_IndirectObjs[objnum];
  const CPDF_Object* old_object = FilterInvalidObjNum(obj_holder.Get());
  if (old_object && pObj->GetGenNum() <= old_object->GetGenNum())  // ***** 5 *****
    return false;

  pObj->SetObjNum(objnum);
  obj_holder = std::move(pObj);
  m_LastObjNum = std::max(m_LastObjNum, objnum);
  return true;
}
```

By the way, just curious, Is CPDF_IndirectObjectHolder::ReplaceIndirectObjectIfHigherGeneration() function call in CPDF_DataAvail::GetPageDictionary() is intended [1]?
It is only called once CPDF_IndirectObjectHolder::GetIndirectObject() call failed [1].
CPDF_IndirectObjectHolder::GetIndirectObject() only fails given dwObjnum is not parsed yet [3].
It means CPDF_IndirectObjectHolder::ReplaceIndirectObjectIfHigherGeneration() is only called the object is not parsed for given number.

But according to its name and comment[4], I think ReplaceIndirectObjectIfHigherGeneration() should be called when object is available for given dwObjnum.
Did I misunderstand the intent?


### ts...@chromium.org (2022-08-30)

Nice find.  You wouldn't happen to have a smaller PoC by any chance?

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2022-08-30)

The issue seems to go back quite a ways, setting foundin to earliest supported release.

### [Deleted User] (2022-08-30)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-08-30)

Re C2: looks like the object gets added unconditionally if there is no previous object, so while there's a bit of extra work that doesn't have to happen per the reasoning in C2, it should wind up being inserted (despite what the name might say).

### gi...@appspot.gserviceaccount.com (2022-08-30)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/81ab3354f79765438bad0e9d683adcfce96727fa

commit 81ab3354f79765438bad0e9d683adcfce96727fa
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Aug 30 23:34:48 2022

Enforce maximum legal object number during linearized parses.

- Watch for overflow of object numbers.
- Re-validate CPDF_Object pointer after notification in CPDF_FormField.

Bug: chromium:1358090
Change-Id: I1effd8f47277d177c804dd14b20b101e71780067
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97130
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/81ab3354f79765438bad0e9d683adcfce96727fa/core/fpdfdoc/cpdf_formfield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/81ab3354f79765438bad0e9d683adcfce96727fa/core/fpdfapi/parser/cpdf_hint_tables.cpp


### ts...@chromium.org (2022-08-30)

Thanks again for the thorough analysis. We've broken this chain of events in several spots with the above patch.

### gi...@appspot.gserviceaccount.com (2022-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8ea9984709cf3da55ef2f1ea2760ade9748ace85

commit 8ea9984709cf3da55ef2f1ea2760ade9748ace85
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Aug 31 06:29:03 2022

Roll PDFium from 5e49f9cccf75 to 48c2e69051b9 (13 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/5e49f9cccf75..48c2e69051b9

2022-08-31 tsepez@chromium.org Add new kConstants for form controls
2022-08-30 tsepez@chromium.org Enforce maximum legal object number during linearized parses.
2022-08-30 nigi@chromium.org Roll buildtools/third_party/libunwind/trunk/ 012c3438e..42aa6de55 (10 commits)
2022-08-30 nigi@chromium.org Roll Fuchsia SDK from 9.20220729.1.1 to 9.20220830.0.1.
2022-08-30 nigi@chromium.org Roll buildtools/third_party/libc++abi/trunk/ 039323b94..48afced8a (6 commits)
2022-08-30 nigi@chromium.org Roll third_party/depot_tools/ 5fb99f65c..3528d4d3c (47 commits; 5 trivial rolls)
2022-08-30 nigi@chromium.org Roll base/trace_event/common/ d115b033c..640fc6dc8 (3 commits)
2022-08-30 nigi@chromium.org Roll third_party/zlib/ c4e126880..926ac230d (2 commits)
2022-08-30 nigi@chromium.org Roll third_party/skia/ 3605b5fd7..73fb58ce0 (544 commits)
2022-08-30 nigi@chromium.org Roll tools/memory/ 41d69d665..e5f1a8a76 (2 commits)
2022-08-30 nigi@chromium.org Roll third_party/icu/ 50ec7b382..bbdc7d893 (4 commits)
2022-08-30 tsepez@chromium.org Pass spans to CFX_FloatRect::GetBBox()
2022-08-30 tsepez@chromium.org Avoid pointer arithmetic in CFX_FileBufferArchive

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

Bug: chromium:1358090
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I3baeeaef423b22c69fbd5bbe23d87da97d08aaf2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3867130
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1041381}

[modify] https://crrev.com/8ea9984709cf3da55ef2f1ea2760ade9748ace85/DEPS


### tr...@gmail.com (2022-08-31)

https://crbug.com/chromium/1358090#c3: The structure of a linearized pdf is not only complex, but I also created a proof-of-concept by fixing many parts of the structure for convenience(e.g. inserting garbage bytes). I've been trying to make a smaller PoC, but unfortunately, it's hard to do with my current structure.

### tr...@gmail.com (2022-08-31)

[Comment Deleted]

### tr...@gmail.com (2022-08-31)

```cpp
--- a/core/fpdfapi/parser/cpdf_hint_tables.cpp
+++ b/core/fpdfapi/parser/cpdf_hint_tables.cpp
@@ -13,6 +13,7 @@
 #include "core/fpdfapi/parser/cpdf_dictionary.h"
 #include "core/fpdfapi/parser/cpdf_document.h"
 #include "core/fpdfapi/parser/cpdf_linearized_header.h"
+#include "core/fpdfapi/parser/cpdf_parser.h"
 #include "core/fpdfapi/parser/cpdf_read_validator.h"
 #include "core/fpdfapi/parser/cpdf_stream.h"
 #include "core/fpdfapi/parser/cpdf_stream_acc.h"
@@ -101,7 +102,7 @@
 
   // Item 1: The least number of objects in a page.
   const uint32_t dwObjLeastNum = hStream->GetBits(32);
-  if (!dwObjLeastNum)
+  if (!dwObjLeastNum || dwObjLeastNum >= CPDF_Parser::kMaxObjectNumber)
     return false;
 
   // Item 2: The location of the first page's page object.
@@ -164,7 +165,7 @@
   m_PageInfos[nFirstPageNum].set_start_obj_num(    // ***** 2 *****
       m_pLinearized->GetFirstPageObjNum());
   // The object number of remaining pages starts from 1.
-  uint32_t dwStartObjNum = 1;
+  FX_SAFE_UINT32 dwStartObjNum = 1;
   for (uint32_t i = 0; i < nPages; ++i) {
     FX_SAFE_UINT32 safeDeltaObj = hStream->GetBits(dwDeltaObjectsBits);
     safeDeltaObj += dwObjLeastNum;
@@ -173,8 +174,12 @@
     m_PageInfos[i].set_objects_count(safeDeltaObj.ValueOrDie());
     if (i == nFirstPageNum)
       continue;
-    m_PageInfos[i].set_start_obj_num(dwStartObjNum);
+    m_PageInfos[i].set_start_obj_num(dwStartObjNum.ValueOrDie());    // ***** 1 *****
     dwStartObjNum += m_PageInfos[i].objects_count();
+    if (!dwStartObjNum.IsValid() ||
+        dwStartObjNum.ValueOrDie() >= CPDF_Parser::kMaxObjectNumber) {
+      return false;
+    }
   }
   hStream->ByteAlign();
```

https://crbug.com/chromium/1358090#c7:
Thanks for the really quick fix! It seems patch makes page info in hint table cannot have big object number[1].
but I think there is possiblity that first page have big object number since there is no checks[2]. (note: I haven't tested it, so I'm not sure if this is actually possible.)

How about doing a check on that code path[2] as well?

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-31)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-31)

Requesting merge to extended stable M104 because latest trunk commit (1041381) appears to be after extended stable branch point (1012729).

Requesting merge to stable M105 because latest trunk commit (1041381) appears to be after stable branch point (1027018).

Requesting merge to dev M106 because latest trunk commit (1041381) appears to be after dev branch point (1036826).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-31)

Merge review required: a commit with DEPS changes was detected.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-31)

Merge review required: a commit with DEPS changes was detected.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-31)

Merge review required: a commit with DEPS changes was detected.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-09-01)

re: https://crbug.com/chromium/1358090#c12 - I uploaded https://pdfium-review.googlesource.com/97275 to do more validation to address your concern.

### am...@chromium.org (2022-09-08)

Merges approved for both https://pdfium.googlesource.com/pdfium/+/81ab3354f79765438bad0e9d683adcfce96727fa and https://pdfium-review.googlesource.com/97275

please merge both fixes to M105/stable (branch 5195) and M104/extended (branch 5112) ASAP before 10am PDT tomorrow, Friday, 9 September so they can be included in the next security respins 

Please also merge to M106/beta (branch 5249) at your earliest convenience. Thank you! 

### pb...@google.com (2022-09-08)

This merge has been approved for M105, please help complete your merges asap (before 4pm PST) today, so the change can be included in next weeks RC build for Stable releases.





### sr...@google.com (2022-09-08)

chatted with thomas , he is working on merges to all 3 branches

### gi...@appspot.gserviceaccount.com (2022-09-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/4a744f89e2ca3db90ad7f72f3ea8ed85db7ac747

commit 4a744f89e2ca3db90ad7f72f3ea8ed85db7ac747
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Sep 08 20:12:14 2022

[M106] Enforce maximum legal object number during linearized parses.

- Watch for overflow of object numbers.
- Re-validate CPDF_Object pointer after notification in CPDF_FormField.

Bug: chromium:1358090
Change-Id: I1effd8f47277d177c804dd14b20b101e71780067
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97130
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 81ab3354f79765438bad0e9d683adcfce96727fa)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97731
Commit-Queue: Lei Zhang <thestig@chromium.org>
Auto-Submit: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/4a744f89e2ca3db90ad7f72f3ea8ed85db7ac747/core/fpdfdoc/cpdf_formfield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/4a744f89e2ca3db90ad7f72f3ea8ed85db7ac747/core/fpdfapi/parser/cpdf_hint_tables.cpp


### [Deleted User] (2022-09-08)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-09-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/a664388970569270f7644bd70efd980705753662

commit a664388970569270f7644bd70efd980705753662
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Sep 08 21:45:44 2022

[M104] Enforce maximum legal object number during linearized parses.

- Watch for overflow of object numbers.
- Re-validate CPDF_Object pointer after notification in CPDF_FormField.

Bug: chromium:1358090
Change-Id: I1effd8f47277d177c804dd14b20b101e71780067
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97130
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 81ab3354f79765438bad0e9d683adcfce96727fa)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97733
Auto-Submit: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/a664388970569270f7644bd70efd980705753662/core/fpdfdoc/cpdf_formfield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/a664388970569270f7644bd70efd980705753662/core/fpdfapi/parser/cpdf_hint_tables.cpp


### gi...@appspot.gserviceaccount.com (2022-09-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/b9316f8b8f1fb43eeae26a6cdc6f5d23267c5f0f

commit b9316f8b8f1fb43eeae26a6cdc6f5d23267c5f0f
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Sep 08 21:50:04 2022

[M105] Enforce maximum legal object number during linearized parses.

- Watch for overflow of object numbers.
- Re-validate CPDF_Object pointer after notification in CPDF_FormField.

Bug: chromium:1358090
Change-Id: I1effd8f47277d177c804dd14b20b101e71780067
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97130
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 81ab3354f79765438bad0e9d683adcfce96727fa)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97732
Auto-Submit: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/b9316f8b8f1fb43eeae26a6cdc6f5d23267c5f0f/core/fpdfdoc/cpdf_formfield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/b9316f8b8f1fb43eeae26a6cdc6f5d23267c5f0f/core/fpdfapi/parser/cpdf_hint_tables.cpp


### rz...@google.com (2022-09-09)

[Empty comment from Monorail migration]

### rz...@google.com (2022-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-09-09)

1. Just https://pdfium-review.googlesource.com/c/pdfium/+/97751
2. Low, no conflicts
3. 104, 105, 106
4. Yes

### am...@google.com (2022-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-09)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in reporting this issue to us -- nice work! 

### gm...@google.com (2022-09-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-22)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/329a2d285470276c85267856543d9a13e1bc46af

commit 329a2d285470276c85267856543d9a13e1bc46af
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Sep 22 18:10:01 2022

[M102-LTS] Enforce maximum legal object number during linearized parses.

- Watch for overflow of object numbers.
- Re-validate CPDF_Object pointer after notification in CPDF_FormField.

Bug: chromium:1358090
Change-Id: I1effd8f47277d177c804dd14b20b101e71780067
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97130
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 81ab3354f79765438bad0e9d683adcfce96727fa)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97751
Reviewed-by: Nicolás Peña Moreno <npm@chromium.org>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>

[modify] https://pdfium.googlesource.com/pdfium/+/329a2d285470276c85267856543d9a13e1bc46af/core/fpdfdoc/cpdf_formfield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/329a2d285470276c85267856543d9a13e1bc46af/core/fpdfapi/parser/cpdf_hint_tables.cpp


### rz...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1358090?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060720)*
