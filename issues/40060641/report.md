# Security: potential buffer overflow in zlib - CVE-2022-37434

| Field | Value |
|-------|-------|
| **Issue ID** | [40060641](https://issues.chromium.org/issues/40060641) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **CVE IDs** | CVE-2022-37434 |
| **Reporter** | ri...@sap.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2022-08-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

In zlib a potential buffer overflow was fixed recently. See: <https://github.com/madler/zlib/commit/eff308af425b67093bab25f80f1ae950166bece1>  

The fix introduced a null pointer deref, which was fixed as well. See: <https://github.com/madler/zlib/commit/1eb7682f845ac9e9bf9ae35bbfb3bad5dacbd91d>

The fix is in zlib develop branch at this point in time, not reached zlib master yet.

**VERSION**  

The corrections are not in Chromium master yet - somehow expectable. If exploitable in Chromium as well, could you please update zlib accordingly, probably once this reached a stable version in zlib?

**CREDIT INFORMATION**  

Originally found by Evgeny Legerov of @intevydis, see <https://github.com/ivd38/zlib_overflow>. I (Richard Lorenz from SAP) just stumbled across this one in our open source scans, because we integrated Chromium Embedded Framework within SAP Business Client.

Best regards,  

Richard

## Attachments

- [tot_unpatched.png](attachments/tot_unpatched.png) (image/png, 441.1 KB)
- [sync_patched.png](attachments/sync_patched.png) (image/png, 504.8 KB)

## Timeline

### [Deleted User] (2022-08-21)

[Empty comment from Monorail migration]

### sr...@google.com (2022-08-22)

Thanks Richard for letting us know!

cavalcantii@ can you take a look at this?
The commit message sounds reasonably scary so I'm marking this as high risk for now.
I checked that we don't have the updated code in cs.chromium.org/ yet.

### sr...@google.com (2022-08-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2022-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2022-08-23)

Thanks for add, I really appreciate it.

I will backport the fixes from madler/dev branch to Chromium's zlib.

That being said, the CVE (https://github.com/advisories/GHSA-cfmr-vrgj-vqwv) states that only code that calls inflateGetHeader() API is impacted and a quick search in chromium repository shows that we *don't* use the impacted API.

 

### ca...@chromium.org (2022-08-23)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-08-24)

Patch on:
https://chromium-review.googlesource.com/c/chromium/src/+/3853109

### ca...@chromium.org (2022-08-24)

Confirmed that the changes in the 'devel' branch will fix the reported payload crash (https://github.com/ivd38/zlib_overflow) and added a new unit test for the reported CVE.


### ca...@chromium.org (2022-08-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/29ee00aece42bd66b1a7196aa41275baad2dd512

commit 29ee00aece42bd66b1a7196aa41275baad2dd512
Author: Adenilson Cavalcanti <cavalcantii@chromium.org>
Date: Thu Aug 25 20:35:55 2022

Sync with zlib 1.2.12.1, patch 1 of N

Ported:
 - Change version number on develop branch to 1.2.12.1.
 - Fix odd error in Visual C compiler preventing automatic promotion.
 - Fix inflateBack to detect invalid input with distances too far.
 - Have infback() deliver all of the available output up to any error.
 - Fix a bug when getting a gzip header extra field with inflate().
 - Fix extra field processing bug that dereferences NULL state->head.
 - Fix some typos.

Bug: 1355103
Change-Id: I838b3f7c885a97d72e040e5a5224bc0aa58068fb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3853109
Reviewed-by: Hans Wennborg <hans@chromium.org>
Commit-Queue: Adenilson Cavalcanti <cavalcantii@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1039413}

[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/deflate.c
[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/crc32.c
[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/contrib/optimizations/inflate.c
[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/inflate.c
[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/inftrees.c
[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/contrib/tests/infcover.h
[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/README.chromium
[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/inftrees.h
[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/trees.c
[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/contrib/tests/utils_unittest.cc
[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/contrib/tests/infcover.cc
[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/zlib.h
[modify] https://crrev.com/29ee00aece42bd66b1a7196aa41275baad2dd512/third_party/zlib/infback.c


### ca...@chromium.org (2022-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-26)

Requesting merge to stable M104 because latest trunk commit (1039413) appears to be after stable branch point (1012729).

Requesting merge to beta M105 because latest trunk commit (1039413) appears to be after beta branch point (1027018).

Requesting merge to dev M106 because latest trunk commit (1039413) appears to be after dev branch point (1036826).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2022-08-26)

@sroettger: just to confirm, but someone else will take care of merging the changes in the branches (i.e. M104, M105, M106), correct?

### [Deleted User] (2022-08-26)

Merge review required: M105 has already been cut for stable release.

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

### [Deleted User] (2022-08-26)

Merge review required: M104 is already shipping to stable.

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

### [Deleted User] (2022-08-26)

Merge approved: your change passed merge requirements and is auto-approved for M106. Please go ahead and merge the CL to branch 5249 (refs/branch-heads/5249) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2022-08-29)

Please merge your change to M106 branch 5249 by noon PT today so we can take it in for this week's dev/beta release. Thank you.

### sr...@google.com (2022-08-29)

This merge has been approved for M106, please help complete your merges asap (before 4pm PST) today, so the change can be included in this weeks RC build for dev/beta releases. 

We would like to get the changes as much beta time as possible, so please compelete your merges asap.

### ca...@chromium.org (2022-08-30)

For M106:
https://chromium-review.googlesource.com/c/chromium/src/+/3863592

### ca...@chromium.org (2022-08-30)

@govind and @srinivassista: is there a special procedure to cherry-pick for M104 + M105 or can I do everything simply using gerrit?

### go...@chromium.org (2022-08-30)

cavalcantii@, you can use gerrit for M104 and M105 merges but please wait until merge approval.

### gi...@appspot.gserviceaccount.com (2022-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7

commit 9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7
Author: Adenilson Cavalcanti <cavalcantii@chromium.org>
Date: Tue Aug 30 02:34:17 2022

Sync with zlib 1.2.12.1, patch 1 of N

Ported:
 - Change version number on develop branch to 1.2.12.1.
 - Fix odd error in Visual C compiler preventing automatic promotion.
 - Fix inflateBack to detect invalid input with distances too far.
 - Have infback() deliver all of the available output up to any error.
 - Fix a bug when getting a gzip header extra field with inflate().
 - Fix extra field processing bug that dereferences NULL state->head.
 - Fix some typos.

(cherry picked from commit 29ee00aece42bd66b1a7196aa41275baad2dd512)

Bug: 1355103
Change-Id: I838b3f7c885a97d72e040e5a5224bc0aa58068fb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3853109
Reviewed-by: Hans Wennborg <hans@chromium.org>
Commit-Queue: Adenilson Cavalcanti <cavalcantii@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1039413}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3863592
Auto-Submit: Adenilson Cavalcanti <cavalcantii@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Adenilson Cavalcanti <cavalcantii@chromium.org>
Cr-Commit-Position: refs/branch-heads/5249@{#198}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/deflate.c
[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/crc32.c
[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/inflate.c
[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/contrib/optimizations/inflate.c
[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/inftrees.c
[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/contrib/tests/infcover.h
[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/README.chromium
[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/inftrees.h
[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/trees.c
[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/contrib/tests/utils_unittest.cc
[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/contrib/tests/infcover.cc
[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/zlib.h
[modify] https://crrev.com/9c85bcaa16d5d2201da98c682a60fc8a04d1a3d7/third_party/zlib/infback.c


### [Deleted User] (2022-08-30)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-30)

this issue does appear to impact shipped versions of Chrome, please go ahead and merge this fix to 104/Extended, branch 5112 and 105/Stable, branch 5195 at your earliest convenience -- thank you! 

### rz...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-31)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-31)

1. 6 CLs https://chromium-review.googlesource.com/q/topic:5005_1355103
The fix, and the CL chain that precedes it and wasn't merged to 102 yet

2. Low, only a conflict in the documentation.
3. 106, approved for 104, 105
4. Yes

### am...@google.com (2022-08-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-31)

Hi Richard, thank you for reporting this to us so we could pick up this fix and get it into Chrome. To show our appreciate, the Chrome Vulnerability Rewards Panel (VRP) would like to extend to you a $1,000 as a thank you. Thank you for taking the time to report this issue to us! 

### am...@chromium.org (2022-08-31)

hi cavalcantii@ while I have approved the fix to be merged to 105 and 104, please hold off on completing these merges for now (until next week), as we are needing to cut a respin for 105 and 104 soon due to an unrelated issue 

### ca...@chromium.org (2022-08-31)

Coolio.

### ca...@chromium.org (2022-08-31)

I friendly reminder that zlib runs both in a sandbox (e.g. inside of the Renderer, PNG image decoder) as also in a privileged level (i.e. network operations, content-encoding: gzip).

### gi...@appspot.gserviceaccount.com (2022-09-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6887ee5130d407126adbc374cdfa14391218341a

commit 6887ee5130d407126adbc374cdfa14391218341a
Author: Hans Wennborg <hans@chromium.org>
Date: Thu Sep 01 09:18:23 2022

[zlib] Add a fuzzer which would have found CVE-2022-37434

The fuzzer does inflation with inflateGetHeader() enabled, using varying
sizes for the gzip header fields and processing the data in varying
chunk sizes.

With the CVE fix reverted, it finds the bug in a minute or two. Having
it will prevent regressions in this area, and perhaps it will find
some other problem.

Bug: 1355103
Change-Id: I2103b111d40dd8f5277069d83db6792ed06b3152
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3865887
Commit-Queue: Hans Wennborg <hans@chromium.org>
Reviewed-by: Adenilson Cavalcanti <cavalcantii@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1041966}

[modify] https://crrev.com/6887ee5130d407126adbc374cdfa14391218341a/third_party/zlib/contrib/tests/fuzzers/BUILD.gn
[add] https://crrev.com/6887ee5130d407126adbc374cdfa14391218341a/third_party/zlib/contrib/tests/fuzzers/inflate_with_header_fuzzer.cc


### gm...@google.com (2022-09-01)

[Empty comment from Monorail migration]

### ri...@sap.com (2022-09-01)

Hi there,

Thanks a lot for the prompt replies and corrections - it is very much appreciated. We are looking forward to seeing them in Chromium Embedded Framework soon too...

Best regards and thanks again,
Richard

### [Deleted User] (2022-09-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-09-07)

hi cavalcantii@, you are free to go ahead and merge this fix to 104/extended (branch 5112) and 105/Stable (branch 5195) at your earliest convenience. Please merge by 10am PST Friday, 9 September so this update can be included in the next Extended and Stable respins. Thank you! 

### pb...@google.com (2022-09-08)

This merge has been approved for M105, please help complete your merges asap (before 4pm PST) today, so the change can be included in next weeks RC build for Stable releases.





### ca...@chromium.org (2022-09-08)

For M105:
https://chromium-review.googlesource.com/c/chromium/src/+/3880734


### ca...@chromium.org (2022-09-08)

For M104:
https://chromium-review.googlesource.com/c/chromium/src/+/3882484


### ca...@chromium.org (2022-09-08)

@amyressler and @pbommana: given is past 7 days since the original patch landed, does the cherry-picks above require approval by other zlib owners?

### sr...@google.com (2022-09-08)

I have CQ+2 both the CL's, they had owners approved. 

### gi...@appspot.gserviceaccount.com (2022-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b9ce892d03399f8057a12cabca455117b9d1c488

commit b9ce892d03399f8057a12cabca455117b9d1c488
Author: Adenilson Cavalcanti <cavalcantii@chromium.org>
Date: Thu Sep 08 23:04:37 2022

Sync with zlib 1.2.12.1, patch 1 of N

Ported:
 - Change version number on develop branch to 1.2.12.1.
 - Fix odd error in Visual C compiler preventing automatic promotion.
 - Fix inflateBack to detect invalid input with distances too far.
 - Have infback() deliver all of the available output up to any error.
 - Fix a bug when getting a gzip header extra field with inflate().
 - Fix extra field processing bug that dereferences NULL state->head.
 - Fix some typos.

(cherry picked from commit 29ee00aece42bd66b1a7196aa41275baad2dd512)

Bug: 1355103
Change-Id: I838b3f7c885a97d72e040e5a5224bc0aa58068fb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3853109
Reviewed-by: Hans Wennborg <hans@chromium.org>
Commit-Queue: Adenilson Cavalcanti <cavalcantii@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1039413}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3880734
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5195@{#1088}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/deflate.c
[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/crc32.c
[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/inflate.c
[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/contrib/optimizations/inflate.c
[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/inftrees.c
[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/contrib/tests/infcover.h
[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/README.chromium
[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/inftrees.h
[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/trees.c
[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/contrib/tests/utils_unittest.cc
[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/contrib/tests/infcover.cc
[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/infback.c
[modify] https://crrev.com/b9ce892d03399f8057a12cabca455117b9d1c488/third_party/zlib/zlib.h


### gi...@appspot.gserviceaccount.com (2022-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3282d7c26175d6a3a25a234a671afb6b290bd09a

commit 3282d7c26175d6a3a25a234a671afb6b290bd09a
Author: Adenilson Cavalcanti <cavalcantii@chromium.org>
Date: Fri Sep 09 19:23:30 2022

Sync with zlib 1.2.12.1, patch 1 of N

Ported:
 - Change version number on develop branch to 1.2.12.1.
 - Fix odd error in Visual C compiler preventing automatic promotion.
 - Fix inflateBack to detect invalid input with distances too far.
 - Have infback() deliver all of the available output up to any error.
 - Fix a bug when getting a gzip header extra field with inflate().
 - Fix extra field processing bug that dereferences NULL state->head.
 - Fix some typos.

(cherry picked from commit 29ee00aece42bd66b1a7196aa41275baad2dd512)

Bug: 1355103
Change-Id: I838b3f7c885a97d72e040e5a5224bc0aa58068fb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3853109
Reviewed-by: Hans Wennborg <hans@chromium.org>
Commit-Queue: Adenilson Cavalcanti <cavalcantii@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1039413}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3882484
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5112@{#1568}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/deflate.c
[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/crc32.c
[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/inflate.c
[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/contrib/optimizations/inflate.c
[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/inftrees.c
[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/contrib/tests/infcover.h
[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/README.chromium
[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/inftrees.h
[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/trees.c
[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/contrib/tests/utils_unittest.cc
[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/contrib/tests/infcover.cc
[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/infback.c
[modify] https://crrev.com/3282d7c26175d6a3a25a234a671afb6b290bd09a/third_party/zlib/zlib.h


### am...@chromium.org (2022-09-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### ha...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-20)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-09-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd

commit 99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd
Author: Adenilson Cavalcanti <cavalcantii@chromium.org>
Date: Wed Sep 21 21:01:25 2022

[M102-LTS] Sync with zlib 1.2.12.1, patch 1 of N

M102 merge issues:
  - third_party/zlib/README.chromium:
    Conflicts with a few doc lines that aren't present in 102.
  - Cherry-picked the CL chain with sequence 11-15 to fix conflicts
    in the changed code.

Ported:
 - Change version number on develop branch to 1.2.12.1.
 - Fix odd error in Visual C compiler preventing automatic promotion.
 - Fix inflateBack to detect invalid input with distances too far.
 - Have infback() deliver all of the available output up to any error.
 - Fix a bug when getting a gzip header extra field with inflate().
 - Fix extra field processing bug that dereferences NULL state->head.
 - Fix some typos.

(cherry picked from commit 29ee00aece42bd66b1a7196aa41275baad2dd512)

Bug: 1355103
Change-Id: I838b3f7c885a97d72e040e5a5224bc0aa58068fb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3853109
Reviewed-by: Hans Wennborg <hans@chromium.org>
Commit-Queue: Adenilson Cavalcanti <cavalcantii@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1039413}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3863276
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Adenilson Cavalcanti <cavalcantii@chromium.org>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1360}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/deflate.c
[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/crc32.c
[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/contrib/optimizations/inflate.c
[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/inflate.c
[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/inftrees.c
[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/contrib/tests/infcover.h
[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/README.chromium
[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/inftrees.h
[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/trees.c
[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/contrib/tests/utils_unittest.cc
[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/contrib/tests/infcover.cc
[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/infback.c
[modify] https://crrev.com/99d8d1c3f825dc9fd0e66d21c35c0b5ff67f14bd/third_party/zlib/zlib.h


### rz...@google.com (2022-09-22)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-11-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1355103?no_tracker_redirect=1

[Auto-CCs applied]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060641)*
