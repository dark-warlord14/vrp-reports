# Security: heap-use-after-free in SearchNameNodeByNameInternal

| Field | Value |
|-------|-------|
| **Issue ID** | [40060719](https://issues.chromium.org/issues/40060719) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | tr...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2022-08-30 |
| **Bounty** | $10,000.00 |

## Description

```
const CPDF_Object\* SearchNameNodeByNameInternal(  
    const RetainPtr<CPDF_Dictionary>& pNode,  
    const WideString& csName,  
    int nLevel,  
    size_t\* nIndex,  
    RetainPtr<CPDF_Array>\* ppFind,  
    int\* pFindIndex) {  
  if (nLevel > kNameTreeMaxRecursion)  
    return nullptr;  
  
  RetainPtr<CPDF_Array> pLimits = pNode->GetMutableArrayFor("Limits");  
  RetainPtr<CPDF_Array> pNames = pNode->GetMutableArrayFor("Names");  
  if (pLimits) {  
    WideString csLeft;  
    WideString csRight;  
    std::tie(csLeft, csRight) = GetNodeLimitsAndSanitize(pLimits.Get());  //  \*\*\*\*\* 1 \*\*\*\*\*  
    // Skip this node if the name to look for is smaller than its lower limit.  
    if (csName.Compare(csLeft) < 0)  
      return nullptr;  
  
    // Skip this node if the name to look for is greater than its higher limit,  
    // and the node itself is a leaf node.  
    if (csName.Compare(csRight) > 0 && pNames) {  
      if (ppFind)  
        \*ppFind = pNames;  
      if (pFindIndex)  
        \*pFindIndex = fxcrt::CollectionSize<int32_t>(\*pNames) / 2 - 1;  
      return nullptr;  
    }  
  }  
  
  // If the node is a leaf node, look for the name in its names array.  
  if (pNames) {  
    size_t dwCount = pNames->size() / 2;  
    for (size_t i = 0; i < dwCount; i++) {  
      WideString csValue = pNames->GetUnicodeTextAt(i \* 2);  
      int32_t iCompare = csValue.Compare(csName);  
      if (iCompare > 0)  
        break;  
      if (ppFind)  
        \*ppFind = pNames;  
      if (pFindIndex)  
        \*pFindIndex = pdfium::base::checked_cast<int32_t>(i);  
      if (iCompare < 0)  
        continue;  
  
      \*nIndex += i;  
      return pNames->GetDirectObjectAt(i \* 2 + 1);   //  \*\*\*\*\* 4 \*\*\*\*\*  
    }  
    \*nIndex += dwCount;  
    return nullptr;  
  }  
  
  // Search through the node's children.  
  RetainPtr<CPDF_Array> pKids = pNode->GetMutableArrayFor("Kids");  
  if (!pKids)  
    return nullptr;  
  
  for (size_t i = 0; i < pKids->size(); i++) {  //  \*\*\*\*\* 5 \*\*\*\*\*  
    RetainPtr<CPDF_Dictionary> pKid = pKids->GetMutableDictAt(i); //  \*\*\*\*\* 7 \*\*\*\*\*  
    if (!pKid)  
      continue;  
  
    const CPDF_Object\* pFound = SearchNameNodeByNameInternal(   //  \*\*\*\*\* 3 \*\*\*\*\*  
        pKid, csName, nLevel + 1, nIndex, ppFind, pFindIndex);  
    if (pFound)  
      return pFound;   //  \*\*\*\*\* 6 \*\*\*\*\*  
  }  
  return nullptr;  
}  
  
std::pair<WideString, WideString> GetNodeLimitsAndSanitize(  
    CPDF_Array\* pLimits) {  
  DCHECK(pLimits);  
  WideString csLeft = pLimits->GetUnicodeTextAt(0);  
  WideString csRight = pLimits->GetUnicodeTextAt(1);  
  // If the lower limit is greater than the upper limit, swap them.  
  if (csLeft.Compare(csRight) > 0) {  
    pLimits->SetNewAt<CPDF_String>(0, csRight.AsStringView());  
    pLimits->SetNewAt<CPDF_String>(1, csLeft.AsStringView());  
    csLeft = pLimits->GetUnicodeTextAt(0);  
    csRight = pLimits->GetUnicodeTextAt(1);  
  }  
  while (pLimits->size() > 2)  
    pLimits->RemoveAt(pLimits->size() - 1); //  \*\*\*\*\* 2 \*\*\*\*\*  
  return {csLeft, csRight};  
}  

```

This bug is similiar to <https://crbug.com/chromium/1335861>.  

SearchNameNodeByNameInternal() function could call itself recursively[3] and it calls GetNodeLimitsAndSanitize() to truncate CPDF\_Array with length greater then 2 [1][2]. <https://crbug.com/chromium/1335861> have showed it is possible to make dangling pointer.

<https://crbug.com/chromium/1335861> has been patched with commit 3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6 by introducing RetainPtr<> on many places to extend lifetime of accessed CPDF\_Object objects. So the CPDF\_Object could alive after its owner is removed from GetNodeLimitsAndSanitize().

Unfortunately, this patch is not enough. SearchNameNodeByNameInternal() functions could return dangled CPDF\_Object pointer and UAF will occur once accessing returned pointer.

SearchNameNodeByNameInternal() will return pointer once matched object is found in item for "Names" key[4].

Once matched object isn't found, SearchNameNodeByNameInternal() iterates "Kids" item list[5] and call itself recursively for child [3]. Once some pointer is returned(found), it returns that value[6]. RetainPtr<> is used[7] to prevent "Kids" items being freed during this iteration. Because SearchNameNodeByNameInternal() may free some objects.

The problem is that RetainPtr<> at [7] prevent object is being freed during iteration only. SearchNameNodeByNameInternal() can returns found object[6] but the lifetime of returned object could be ended within iteration and SearchNameNodeByNameInternal() function scope. As a result, a dangling pointer is returned because the object's lifetime ends at the same time it returns.

**VERSION**  

Chrome Version: Stable / 107.0.5269.0 (Commit 396799b65ad67a7ea10bbdeb1d75029d297bb520)  

Operating System: Ubuntu 20.04 x64

**REPRODUCTION CASE**  

Open `poc.pdf`

**CREDIT INFORMATION**  

Reporter credit: triplepwns

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 29.2 KB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 492 B)

## Timeline

### [Deleted User] (2022-08-30)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-08-31)

I was able to repro on Windows and Linux at stable (105.0.5195.54). Assuming all platform are affected. 

This seems like a pretty straightforward high severity report due to UAF plausibly leading to RCE in a sandboxed process. 

[Monorail components: Internals>Plugins>PDF]

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-31)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-08-31)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d

commit d51720c9bb55d1163ab4fdcdc6981e753aa2354d
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Aug 31 20:43:37 2022

Return retained const objects from SearchNameNodeByNameInternal()

Bug: chromium:1358075
Change-Id: I4c06f6c8c148804fa71a7ef156524be4776b2d16
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97210
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/fxjs/cjs_document.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/core/fpdfapi/parser/cpdf_number.h
[modify] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/core/fpdfdoc/cpdf_nametree.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/fpdfsdk/fpdf_view.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/core/fpdfapi/parser/cpdf_stream.h
[add] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/testing/resources/javascript/bug_1358075.in
[modify] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/core/fpdfdoc/cpdf_nametree.h
[modify] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/core/fpdfdoc/cpdf_nametree_unittest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/xfa/fxfa/cxfa_ffdoc.cpp
[add] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/testing/resources/javascript/bug_1358075_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/core/fpdfdoc/cpdf_dest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/core/fpdfapi/parser/cpdf_array.h
[modify] https://pdfium.googlesource.com/pdfium/+/d51720c9bb55d1163ab4fdcdc6981e753aa2354d/core/fpdfapi/parser/cpdf_dictionary.h


### ts...@chromium.org (2022-08-31)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cf6844b54e573ac4c0290c3391a58ec8c16d2833

commit cf6844b54e573ac4c0290c3391a58ec8c16d2833
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Sep 01 09:12:52 2022

Roll PDFium from 48c2e69051b9 to 435a508730a6 (7 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/48c2e69051b9..435a508730a6

2022-08-31 tsepez@chromium.org Remove unused non-const form of CPDF_Object::SafeGetDirect()
2022-08-31 tsepez@chromium.org Add two more RetainPtr tests.
2022-08-31 tsepez@chromium.org Avoid ref-churn when move conversion constructing RetainPtrs
2022-08-31 nigi@chromium.org Roll third_party/abseil-cpp/ 62a4d6866..fd07f9469 (4 commits)
2022-08-31 nigi@chromium.org Roll tools/clang/ c8f1e5e5b..3d8d88e8b (4 commits)
2022-08-31 tsepez@chromium.org Return retained const objects from SearchNameNodeByNameInternal()
2022-08-31 nigi@chromium.org Roll third_party/freetype/src/ 2db58e061..1a242558b (8 commits)

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

Bug: chromium:1358075
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I88700e53d31b581160842ee8d32d62b111558ae1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3868512
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1041956}

[modify] https://crrev.com/cf6844b54e573ac4c0290c3391a58ec8c16d2833/DEPS


### ts...@chromium.org (2022-09-01)

Anyways, I'm likely in a few days to re-write any code returning CPDF_ parser objects to return ref-counted objects always, rather than keep hitting these one by one.


### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

Requesting merge to extended stable M104 because latest trunk commit (1041956) appears to be after extended stable branch point (1012729).

Requesting merge to stable M105 because latest trunk commit (1041956) appears to be after stable branch point (1027018).

Requesting merge to beta M106 because latest trunk commit (1041956) appears to be after beta branch point (1036826).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

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

### [Deleted User] (2022-09-07)

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

### [Deleted User] (2022-09-07)

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

### am...@chromium.org (2022-09-08)

tentatively approving merge for this fix to M104, M105, and M106; please ensure there are no stability issues or other concerns with backmerging this fix. If there are no issues, please merge to branch M105 (branch 5195) and M104 (branch 5112) ASAP/ before 10am PDT tomorrow, so this fix can be included in the next stable and extended stable security respins. 

Merge also approved for M106, please merge to branch 5249 at your earliest convenience. Thanks! 

### pb...@google.com (2022-09-08)

This merge has been approved for M105, please help complete your merges asap (before 4pm PST) today, so the change can be included in next weeks RC build for Stable releases.





### ts...@chromium.org (2022-09-08)

Create cherry-picks for M106 and M105; M104 had conflicts.

### sr...@google.com (2022-09-08)

chatted with thomas , he is working on merges to all 3 branches

### gi...@appspot.gserviceaccount.com (2022-09-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73

commit ad499fdd89b71dd3041380d4da1a7c8b91496a73
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Sep 08 22:57:34 2022

[M106] Return retained const objects from SearchNameNodeByNameInternal()

Bug: chromium:1358075
Change-Id: I4c06f6c8c148804fa71a7ef156524be4776b2d16
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97210
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit d51720c9bb55d1163ab4fdcdc6981e753aa2354d)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97734
Commit-Queue: Lei Zhang <thestig@chromium.org>
Auto-Submit: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/fxjs/cjs_document.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/core/fpdfapi/parser/cpdf_number.h
[modify] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/core/fpdfdoc/cpdf_nametree.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/fpdfsdk/fpdf_view.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/core/fpdfapi/parser/cpdf_stream.h
[add] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/testing/resources/javascript/bug_1358075.in
[modify] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/core/fpdfdoc/cpdf_nametree.h
[modify] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/core/fpdfdoc/cpdf_nametree_unittest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/xfa/fxfa/cxfa_ffdoc.cpp
[add] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/testing/resources/javascript/bug_1358075_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/core/fpdfdoc/cpdf_dest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/core/fpdfapi/parser/cpdf_array.h
[modify] https://pdfium.googlesource.com/pdfium/+/ad499fdd89b71dd3041380d4da1a7c8b91496a73/core/fpdfapi/parser/cpdf_dictionary.h


### [Deleted User] (2022-09-08)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-09-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6

commit e5664aceeffbeba83e402776fc5eca0e95c27eb6
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Sep 08 23:01:17 2022

[M105] Return retained const objects from SearchNameNodeByNameInternal()

Bug: chromium:1358075
Change-Id: I4c06f6c8c148804fa71a7ef156524be4776b2d16
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97210
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit d51720c9bb55d1163ab4fdcdc6981e753aa2354d)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97735
Commit-Queue: Lei Zhang <thestig@chromium.org>
Auto-Submit: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/fxjs/cjs_document.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/core/fpdfapi/parser/cpdf_number.h
[modify] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/core/fpdfdoc/cpdf_nametree.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/fpdfsdk/fpdf_view.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/core/fpdfapi/parser/cpdf_stream.h
[add] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/testing/resources/javascript/bug_1358075.in
[modify] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/core/fpdfdoc/cpdf_nametree_unittest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/core/fpdfdoc/cpdf_nametree.h
[modify] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/xfa/fxfa/cxfa_ffdoc.cpp
[add] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/testing/resources/javascript/bug_1358075_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/core/fpdfdoc/cpdf_dest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/core/fpdfapi/parser/cpdf_dictionary.h
[modify] https://pdfium.googlesource.com/pdfium/+/e5664aceeffbeba83e402776fc5eca0e95c27eb6/core/fpdfapi/parser/cpdf_array.h


### gi...@appspot.gserviceaccount.com (2022-09-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137

commit 497f077a1d46bfeacb4eef83b223ae7b0fc51137
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Sep 08 23:05:34 2022

[M104] Return retained const objects from SearchNameNodeByNameInternal()

Cherry-pick of d51720c9bb55d1163ab4fdcdc6981e753aa2354d + manual
conflict resolution.

Bug: chromium:1358075
Change-Id: Ibb20a6feaf79f7b351f22c607c306da40026d53e
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97739
Auto-Submit: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/fxjs/cjs_document.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/core/fpdfapi/parser/cpdf_number.h
[modify] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/core/fpdfdoc/cpdf_nametree.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/fpdfsdk/fpdf_view.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/core/fpdfapi/parser/cpdf_stream.h
[add] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/testing/resources/javascript/bug_1358075.in
[modify] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/core/fpdfdoc/cpdf_nametree.h
[modify] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/core/fpdfdoc/cpdf_nametree_unittest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/xfa/fxfa/cxfa_ffdoc.cpp
[add] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/testing/resources/javascript/bug_1358075_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/core/fpdfdoc/cpdf_dest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/core/fpdfapi/parser/cpdf_dictionary.h
[modify] https://pdfium.googlesource.com/pdfium/+/497f077a1d46bfeacb4eef83b223ae7b0fc51137/core/fpdfapi/parser/cpdf_array.h


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

1. Just https://pdfium-review.googlesource.com/c/pdfium/+/97752
2. Low, conflicting return types for the changed functions
3. 105, 106
4. Yes

### gm...@google.com (2022-09-12)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-20)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-22)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84

commit 367f6bdb5c33addff80da82238912e2d93a32b84
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Sep 22 19:13:22 2022

[M102-LTS] Return retained const objects from SearchNameNodeByNameInternal()

M102 merge issues:
  core/fpdfapi/parser/cpdf_number.h:
    non-const ToNumber() isn't present in M102

  core/fpdfdoc/cpdf_nametree.h/cpp:
    Conflicting return types of SearchNameNodeByNameInternal(),
    SearchNameNodeByNameInternal(), SearchNameNodeByName(),
    GetNamedDestFromObject(), LookupOldStyleNamedDest(), LookupNamedDest(),
    LookupValue(), and LookupNewStyleNamedDest() - They return non-const
    pointers in M102.

  fxjs/cjs_document.cpp:
    Conflicting type of dest_array in gotoNamedDest().

  xfa/fxfa/cxfa_ffdoc.cpp:
    Conflicting type of pObject and pStream in GetPDFNamedImage().

Bug: chromium:1358075
Change-Id: I4c06f6c8c148804fa71a7ef156524be4776b2d16
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97210
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit d51720c9bb55d1163ab4fdcdc6981e753aa2354d)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/97752
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>

[modify] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/fxjs/cjs_document.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/core/fpdfapi/parser/cpdf_number.h
[modify] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/core/fpdfdoc/cpdf_nametree.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/fpdfsdk/fpdf_view.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/core/fpdfapi/parser/cpdf_stream.h
[add] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/testing/resources/javascript/bug_1358075.in
[modify] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/core/fpdfdoc/cpdf_nametree.h
[modify] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/core/fpdfdoc/cpdf_nametree_unittest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/xfa/fxfa/cxfa_ffdoc.cpp
[add] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/testing/resources/javascript/bug_1358075_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/core/fpdfdoc/cpdf_dest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/core/fpdfapi/parser/cpdf_array.h
[modify] https://pdfium.googlesource.com/pdfium/+/367f6bdb5c33addff80da82238912e2d93a32b84/core/fpdfapi/parser/cpdf_dictionary.h


### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-22)

Congratulations, triplepwns! The VRP Panel has decided to award you $10,000 for this report. Thank you for your effort in reporting this issue to us -- great work! 

### rz...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1358075?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060719)*
