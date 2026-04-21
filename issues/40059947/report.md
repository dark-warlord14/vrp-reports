# Security: heap-use-after-free in SearchNameNodeByNameInternal

| Field | Value |
|-------|-------|
| **Issue ID** | [40059947](https://issues.chromium.org/issues/40059947) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | tr...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2022-06-13 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

third\_party/pdfium/core/fpdfdoc/cpdf\_nametree.cpp

```
CPDF_Object\* SearchNameNodeByNameInternal(CPDF_Dictionary\* pNode,  
                                          const WideString& csName,  
                                          int nLevel,  
                                          size_t\* nIndex,  
                                          CPDF_Array\*\* ppFind,  
                                          int\* pFindIndex) {  
  if (nLevel > kNameTreeMaxRecursion)  
    return nullptr;  
  
  CPDF_Array\* pLimits = pNode->GetArrayFor("Limits"); // \*\*\*\*\* 1 \*\*\*\*\*\*  
  CPDF_Array\* pNames = pNode->GetArrayFor("Names");  
  if (pLimits) {  
    WideString csLeft;  
    WideString csRight;  
    std::tie(csLeft, csRight) = GetNodeLimitsAndSanitize(pLimits); // \*\*\*\*\* 2 \*\*\*\*\*  
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
      return pNames->GetDirectObjectAt(i \* 2 + 1);  
    }  
    \*nIndex += dwCount;  
    return nullptr;  
  }  
  
  // Search through the node's children.  
  CPDF_Array\* pKids = pNode->GetArrayFor("Kids"); // \*\*\*\*\* 5 \*\*\*\*\*  
  if (!pKids)  
    return nullptr;  
  
  for (size_t i = 0; i < pKids->size(); i++) {  
    CPDF_Dictionary\* pKid = pKids->GetDictAt(i);  
    if (!pKid)  
      continue;  
  
    CPDF_Object\* pFound = SearchNameNodeByNameInternal( // \*\*\*\*\* 3 \*\*\*\*\*  
        pKid, csName, nLevel + 1, nIndex, ppFind, pFindIndex);  
    if (pFound)  
      return pFound;  
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
    pLimits->RemoveAt(pLimits->size() - 1); // \*\*\*\*\* 4 \*\*\*\*\*  
  return {csLeft, csRight};  
}  

```

In PDFium, `Document.gotoNamedDest([name])` javascript function bindings calls `SearchNameNodeByNameInternal` function to find matched pdf object with `[name]`. `SearchNameNodeByNameInternal` function gets values mapped with `Limit` key from pdf dictionary named `pNode` and compares with given name [1]. If the name isn't matched, it recursively traverses into values with `Kids` key [3]. `SearchNameNodeByNameInternal` function sanitizes values from `Limit` key before compare by calling `GetNodeLimitsAndSanitize` function [2]. Unrelated values are sanitized(removed) by `GetNodeLimitsAndSanitize` function [4].

The problem is dictionary key `Kids` can have refereces which refer owner of `pNode` node. In this case, `GetNodeLimitsAndSanitize` function call removes owner of `pNode` node and it also leads to free `pNode`, UAF occured at [5].

**VERSION**  

Chrome Version: Stable  

Operating System: Ubuntu 20.04 x64

**REPRODUCTION CASE**  

Open `poc.pdf` with chromium or pdfium\_test

**CREDIT INFORMATION**  

Reporter credit: triplepwns

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 397 B)
- [asan.log](attachments/asan.log) (text/plain, 29.3 KB)

## Timeline

### [Deleted User] (2022-06-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6026622683774976.

### ts...@chromium.org (2022-06-13)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2022-06-13)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-06-14)

Introduced at https://pdfium-review.googlesource.com/c/pdfium/+/86910 - Lei, do you recall why we decided to do this rather than just letting it be?

### [Deleted User] (2022-06-14)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2022-06-14)

Anyways, I'm working on a fix, just wanted to know if we can undo this ...

### th...@chromium.org (2022-06-14)

Is it easy to undo? We may need to undo some more of that CL chain.

### th...@chromium.org (2022-06-15)

Passing the hot potato.

### gi...@appspot.gserviceaccount.com (2022-06-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/ebebb757c1f210ccc16e0cb2b425860a141a4e9f

commit ebebb757c1f210ccc16e0cb2b425860a141a4e9f
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Jun 15 01:22:35 2022

Retain nodes when manipulating their dictionaries in CPDF_NameTree.

-- Pass retain ptrs consistently in a few other places.

Bug: chromium:1335861
Change-Id: If23cf6b6ec39ef02384beaa6745e1c7256160cba
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/94430
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/ebebb757c1f210ccc16e0cb2b425860a141a4e9f/core/fpdfapi/parser/cpdf_dictionary.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/ebebb757c1f210ccc16e0cb2b425860a141a4e9f/core/fpdfapi/parser/cpdf_array.cpp
[add] https://pdfium.googlesource.com/pdfium/+/ebebb757c1f210ccc16e0cb2b425860a141a4e9f/testing/resources/javascript/bug_1335681_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/ebebb757c1f210ccc16e0cb2b425860a141a4e9f/core/fpdfdoc/cpdf_nametree.cpp
[add] https://pdfium.googlesource.com/pdfium/+/ebebb757c1f210ccc16e0cb2b425860a141a4e9f/testing/resources/javascript/bug_1335681.in
[modify] https://pdfium.googlesource.com/pdfium/+/ebebb757c1f210ccc16e0cb2b425860a141a4e9f/core/fpdfapi/parser/cpdf_dictionary.h
[modify] https://pdfium.googlesource.com/pdfium/+/ebebb757c1f210ccc16e0cb2b425860a141a4e9f/core/fpdfapi/parser/cpdf_array.h


### ts...@chromium.org (2022-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/116c0d891c6b71ead0da6d5b2bb463bf93e84743

commit 116c0d891c6b71ead0da6d5b2bb463bf93e84743
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jun 15 17:38:26 2022

Roll PDFium from 960d9640aa7c to 1ab810ed60e5 (2 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/960d9640aa7c..1ab810ed60e5

2022-06-15 thestig@chromium.org Move the definition of FS_QUADPOINTSF to fpdfview.h.
2022-06-15 tsepez@chromium.org Retain nodes when manipulating their dictionaries in CPDF_NameTree.

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

Bug: chromium:1335861
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I4ce7a0b9dcb804348111f084ba546f67c4154f52
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3707645
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1014512}

[modify] https://crrev.com/116c0d891c6b71ead0da6d5b2bb463bf93e84743/DEPS


### [Deleted User] (2022-06-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-06-15)

+bookholt as this might be a place to hunt for variants, if you were so inclined.

### am...@google.com (2022-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-24)

Congratulations, triplepwns! The VRP Panel has decided to award you $7,500 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@chromium.org (2022-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-24)

Requesting merge to extended stable M102 because latest trunk commit (1014512) appears to be after extended stable branch point (992738).

Requesting merge to stable M103 because latest trunk commit (1014512) appears to be after stable branch point (1002911).

Requesting merge to beta M104 because latest trunk commit (1014512) appears to be after beta branch point (1012729).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-24)

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

### [Deleted User] (2022-06-24)

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-24)

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

### am...@chromium.org (2022-06-28)

Hi Tom, thanks for landing this fix. I can't access the native commit, but based on the autoroll commit there does not seem to be any issues with this merge and it has had sufficient bake time on canary. 
Merge approved for 104, please merge to branch 5112 at your earliest availability to do so, so this fix can be included in M104 beta on Wednesday. 

Withholding merge approval for 102 and 103 at this time as release TPMs do not want new fixes merged to those release channels for another day or two at this time. 
Will revisit merge approval for ES and Stable later this week. 

### ts...@chromium.org (2022-06-28)

Merge at https://pdfium-review.googlesource.com/c/pdfium/+/94750

### sr...@google.com (2022-06-28)

This bug has been approved for Merge to M104 and the merge has not been completed , Please merge your change asap to M104 branch before 2pm PST today ( tuesday Jun 28) as I will be cutting Beta RC build at that time for this week's beta release. I would like to get these  CL's merged asap so we get good beta coverage 

### gi...@appspot.gserviceaccount.com (2022-06-28)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/c7c276ce1192f043affb2098ac7ce44f7fd7f084

commit c7c276ce1192f043affb2098ac7ce44f7fd7f084
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Jun 28 17:02:30 2022

[M104] Retain nodes when manipulating dictionaries in CPDF_NameTree.

-- Pass retain ptrs consistently in a few other places.

Bug: chromium:1335861
Change-Id: If23cf6b6ec39ef02384beaa6745e1c7256160cba
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/94430
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit ebebb757c1f210ccc16e0cb2b425860a141a4e9f)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/94750

[modify] https://pdfium.googlesource.com/pdfium/+/c7c276ce1192f043affb2098ac7ce44f7fd7f084/core/fpdfapi/parser/cpdf_dictionary.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/c7c276ce1192f043affb2098ac7ce44f7fd7f084/core/fpdfapi/parser/cpdf_array.cpp
[add] https://pdfium.googlesource.com/pdfium/+/c7c276ce1192f043affb2098ac7ce44f7fd7f084/testing/resources/javascript/bug_1335681_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/c7c276ce1192f043affb2098ac7ce44f7fd7f084/core/fpdfdoc/cpdf_nametree.cpp
[add] https://pdfium.googlesource.com/pdfium/+/c7c276ce1192f043affb2098ac7ce44f7fd7f084/testing/resources/javascript/bug_1335681.in
[modify] https://pdfium.googlesource.com/pdfium/+/c7c276ce1192f043affb2098ac7ce44f7fd7f084/core/fpdfapi/parser/cpdf_array.h
[modify] https://pdfium.googlesource.com/pdfium/+/c7c276ce1192f043affb2098ac7ce44f7fd7f084/core/fpdfapi/parser/cpdf_dictionary.h


### [Deleted User] (2022-06-28)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-06-29)

The CL that introduced the issue isn't present in M96 branch. Waiting to see if the current merge request will be approved for 102 (https://crbug.com/1335861#c24)

### rz...@google.com (2022-06-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-08)

Merge approved for M102/ES and M103/Stable, please merge this fix to M102 (branch 5005) and M103 (branch 5060) at your earliest convenience. Thank you! 

### [Deleted User] (2022-07-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-07-12)

Thanks sheriffbot. Will merge today.

### th...@chromium.org (2022-07-12)

https://pdfium-review.googlesource.com/95270 and https://pdfium-review.googlesource.com/95271 created.

### ni...@chromium.org (2022-07-12)

Re thestig@ : Thanks for creating the merges! 

### gi...@appspot.gserviceaccount.com (2022-07-12)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6

commit 3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Jul 12 18:13:14 2022

M102: Retain nodes when manipulating their dictionaries in CPDF_NameTree.

-- Pass retain ptrs consistently in a few other places.

Bug: chromium:1335861
Change-Id: If23cf6b6ec39ef02384beaa6745e1c7256160cba
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/94430
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit ebebb757c1f210ccc16e0cb2b425860a141a4e9f)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/95271
Reviewed-by: Nigi <nigi@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/core/fpdfapi/parser/cpdf_dictionary.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/core/fpdfapi/parser/cpdf_array.cpp
[add] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/testing/resources/javascript/bug_1335681_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/core/fpdfdoc/cpdf_nametree.cpp
[add] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/testing/resources/javascript/bug_1335681.in
[modify] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/core/fpdfapi/parser/cpdf_array.h
[modify] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/core/fpdfapi/parser/cpdf_dictionary.h


### gi...@appspot.gserviceaccount.com (2022-07-12)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/57e40e8fe1404cbfb611a64cb686868932a5b052

commit 57e40e8fe1404cbfb611a64cb686868932a5b052
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Jul 12 18:13:08 2022

M103: Retain nodes when manipulating their dictionaries in CPDF_NameTree.

-- Pass retain ptrs consistently in a few other places.

Bug: chromium:1335861
Change-Id: If23cf6b6ec39ef02384beaa6745e1c7256160cba
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/94430
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit ebebb757c1f210ccc16e0cb2b425860a141a4e9f)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/95270
Reviewed-by: Nigi <nigi@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/57e40e8fe1404cbfb611a64cb686868932a5b052/core/fpdfapi/parser/cpdf_dictionary.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/57e40e8fe1404cbfb611a64cb686868932a5b052/core/fpdfapi/parser/cpdf_array.cpp
[add] https://pdfium.googlesource.com/pdfium/+/57e40e8fe1404cbfb611a64cb686868932a5b052/testing/resources/javascript/bug_1335681_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/57e40e8fe1404cbfb611a64cb686868932a5b052/core/fpdfdoc/cpdf_nametree.cpp
[add] https://pdfium.googlesource.com/pdfium/+/57e40e8fe1404cbfb611a64cb686868932a5b052/testing/resources/javascript/bug_1335681.in
[modify] https://pdfium.googlesource.com/pdfium/+/57e40e8fe1404cbfb611a64cb686868932a5b052/core/fpdfapi/parser/cpdf_array.h
[modify] https://pdfium.googlesource.com/pdfium/+/57e40e8fe1404cbfb611a64cb686868932a5b052/core/fpdfapi/parser/cpdf_dictionary.h


### gi...@appspot.gserviceaccount.com (2022-07-12)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6

commit 3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Jul 12 18:13:14 2022

M102: Retain nodes when manipulating their dictionaries in CPDF_NameTree.

-- Pass retain ptrs consistently in a few other places.

Bug: chromium:1335861
Change-Id: If23cf6b6ec39ef02384beaa6745e1c7256160cba
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/94430
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit ebebb757c1f210ccc16e0cb2b425860a141a4e9f)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/95271
Reviewed-by: Nigi <nigi@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/core/fpdfapi/parser/cpdf_dictionary.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/core/fpdfapi/parser/cpdf_array.cpp
[add] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/testing/resources/javascript/bug_1335681_expected.txt
[modify] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/core/fpdfdoc/cpdf_nametree.cpp
[add] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/testing/resources/javascript/bug_1335681.in
[modify] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/core/fpdfapi/parser/cpdf_array.h
[modify] https://pdfium.googlesource.com/pdfium/+/3466cc056b052eb5e8e9d7d5f8f2aa3ab33e3bd6/core/fpdfapi/parser/cpdf_dictionary.h


### rz...@google.com (2022-07-15)

Already merged to 102

### am...@chromium.org (2022-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1335861?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059947)*
