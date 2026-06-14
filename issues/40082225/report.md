# Integer-overflow in sfntly::FontData::Bound

| Field | Value |
|-------|-------|
| **Issue ID** | [40082225](https://issues.chromium.org/issues/40082225) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia>PDF |
| **Reporter** | cl...@chromium.org |
| **Assignee** | th...@chromium.org |
| **Created** | 2015-06-05 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6220248129208320

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_ubsan_chrome

Crash Type: Integer-overflow
Crash Address: 
Crash State:
  sfntly::FontData::Bound
  sfntly::ReadableFontData::ReadableFontData
  sfntly::WritableFontData::WritableFontData
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_ubsan_chrome&range=331347:332301

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95A4tXXwAwyvtD6khUeKfDiYBQ_ZUfyH0UQ4uYviGvbdEBt7OMFrlTdeyTSX-zBakI1oZbr8A3XKyHzMQ1VBXVdG9AoXO_ws0uYbJwZ175y5yqKUmmuEj3R9Z0UE2fbB4mdFtPvQG0UlD9ssLHy4enlNPr1wd74E85psYHJgE7go50gzQw


Additional requirements: Requires Gestures

Filer: ochang

## Timeline

### oc...@chromium.org (2015-06-05)

Not sure about the exploitability (or the label) of this one so I marked this as medium. However, it shouldn't hurt to add a check for integer overflow here.

### cl...@chromium.org (2015-06-05)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-06-07)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-06-08)

I talked to Arthur and he's not taking this bug. He says third_party/sfntly is just a snapshot of upstream, which is in google3. Thus the team that owns the code there needs to fix it. (Or maybe merge a fix?)

+stuartg,jungshik from depot/google3/typography/OWNERS. Sftnly is in //depot/google3/typography/font/sfntly/

Also, removing the PDF label since it's not a bug in the PDF plugin, but rather code in the Skia PDF generator.

### th...@chromium.org (2015-06-08)

sfntly::FontData::Bound() is identifical in the google3 copy and hasn't changed since 2011. The code probably just needs to check:

offset <= std::numeric_limits<int32>::max() - length

before checking:

offset + length > Size()

### th...@chromium.org (2015-06-08)

cl/95469737

### oc...@chromium.org (2015-06-08)

Thanks for taking this!

### th...@chromium.org (2015-06-09)

Well, my CL got reverted because some sfntly tests failed. I don't even know where those tests run within google3.

+dml@ since he has been actively working on the google3 version of sfntly.

### th...@chromium.org (2015-06-10)

Part of the problem is we are using FontData::GROWABLE_SIZE, which is set to INT_MAX, so we are almost guaranteeing an integer overflow here.

So I talked to Arthur and he pointed out that the C++ version is just mirroring the Java sfntly code. In FontData.java, the bound() function also does the same thing. I'm not a Java expert, so please correct me if I'm wrong, but since |offset| and |length| are primitives, they overflow just like C++ integers. We should fix the Java version as well then?

### th...@chromium.org (2015-06-10)

Attempt 2 in cl/95606739

### th...@chromium.org (2015-06-29)

Fix landed in cl/96914065 but I'm going out of town. Can someone do the merge in Chromium?

### cl...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-10)

ClusterFuzz has detected this issue as potentially fixed, but it appears to be flaky.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6220248129208320

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_ubsan_chrome

Crash Type: Integer-overflow
Crash Address: 
Crash State:
  sfntly::FontData::Bound
  sfntly::ReadableFontData::ReadableFontData
  sfntly::WritableFontData::WritableFontData
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_ubsan_chrome&range=331347:332301

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95A4tXXwAwyvtD6khUeKfDiYBQ_ZUfyH0UQ4uYviGvbdEBt7OMFrlTdeyTSX-zBakI1oZbr8A3XKyHzMQ1VBXVdG9AoXO_ws0uYbJwZ175y5yqKUmmuEj3R9Z0UE2fbB4mdFtPvQG0UlD9ssLHy4enlNPr1wd74E85psYHJgE7go50gzQw


Additional requirements: Requires Gestures

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### th...@chromium.org (2015-07-14)

We'll wait for stuartg@ to get back to figure out the sftnly upstreaming situation. AFAICT, this bug has been around forever, so waiting a bit longer should be ok.

### cl...@chromium.org (2015-08-05)

thestig@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-26)

thestig@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### js...@chromium.org (2015-08-28)

stuartg@ : are you going to merge cl/96914065 to the sfntly in github?  

 thestig@: do you see any issue with merging the above cl to Chromium's copy of sfntly directly? 


### cl...@chromium.org (2015-09-18)

thestig@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### th...@chromium.org (2015-09-18)

jsin: stuartg's last email was he was travelling and to talk to arthurhsu. arthurhsu sits right next to me and says he's out of the sftnly game.

I guess maybe I should just merge this into Chromium's copy of sftnly. This has been on the back burner due to bug bankruptcy. Will look at this... when I wake up.

### th...@chromium.org (2015-09-19)

https://codereview.chromium.org/1359543002 out for review. (No, I did not just wake up.)

### th...@chromium.org (2015-09-19)

Can't land, since that's just mirroring the code.google.com SVN repo which is read only. We need to switch Chromium to use the github sfntly repo, and then land the fix there.

### th...@chromium.org (2015-09-23)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-09-24)

FYI, I made a pull request with sftnly upstream on GitHub.

### th...@chromium.org (2015-09-26)

https://codereview.chromium.org/1367323002 out to roll DEPS for the new sftnly repo.

### th...@chromium.org (2015-09-26)

It's Friday afternoon and the office is looking empty. I expect the fix to land next week, and then we can consider a merge to M-46. M-45 probably won't take anymore merges at this point.

### bu...@chromium.org (2015-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3e7d8e08a0fd550e03c5d83621871bd36803e727

commit 3e7d8e08a0fd550e03c5d83621871bd36803e727
Author: thestig <thestig@chromium.org>
Date: Mon Sep 28 23:54:46 2015

Pull sfntly from GitHub instead of code.google.com.

- Pick up latest release
- Adjust build files
- Update README.chromium

BUG=497302

Review URL: https://codereview.chromium.org/1367323002

Cr-Commit-Position: refs/heads/master@{#351207}

[modify] http://crrev.com/3e7d8e08a0fd550e03c5d83621871bd36803e727/DEPS
[modify] http://crrev.com/3e7d8e08a0fd550e03c5d83621871bd36803e727/skia/config/SkUserConfig.h
[modify] http://crrev.com/3e7d8e08a0fd550e03c5d83621871bd36803e727/third_party/sfntly/BUILD.gn
[modify] http://crrev.com/3e7d8e08a0fd550e03c5d83621871bd36803e727/third_party/sfntly/README.chromium
[modify] http://crrev.com/3e7d8e08a0fd550e03c5d83621871bd36803e727/third_party/sfntly/sfntly.gyp
[modify] http://crrev.com/3e7d8e08a0fd550e03c5d83621871bd36803e727/tools/checklicenses/checklicenses.py


### th...@chromium.org (2015-09-29)

I don't really want to merge to M46 unless someone tells me to. :)

### bu...@chromium.org (2015-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d02508f8c010b1415f5f1521a6f4cee260d1f8a9

commit d02508f8c010b1415f5f1521a6f4cee260d1f8a9
Author: thestig <thestig@chromium.org>
Date: Tue Sep 29 02:22:23 2015

Fix the win64 GN build after r351207.

BUG=497302
TBR=arthurhsu@chromium.org

Review URL: https://codereview.chromium.org/1373143002

Cr-Commit-Position: refs/heads/master@{#351236}

[modify] http://crrev.com/d02508f8c010b1415f5f1521a6f4cee260d1f8a9/third_party/sfntly/BUILD.gn


### cl...@chromium.org (2015-09-29)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ti...@google.com (2015-10-12)

#28 - Agree - let's roll this in with M-47 as I'd rather not push this last minute to M46.

### th...@chromium.org (2015-10-12)

This made it in before the M47 branch date. No merging required AFAICT.

### ti...@google.com (2015-12-01)

Congrats - $1000 for this report. I'll start payment later this week.

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-05)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-01-05)

[Empty comment from Monorail migration]

### du...@chromium.org (2016-08-26)

Re-opening this as Clusterfuzz has detected a similar crash, Clusterfuzz updates in below comment.Please let us know if its not related to.

### cl...@chromium.org (2016-08-26)

[Comment Deleted]

### sh...@chromium.org (2016-08-28)

[Comment Deleted]

### th...@chromium.org (2016-08-30)

durga.behera: Erm, https://crbug.com/chromium/497302#c38 is also misfiled. Please do not file new bugs as duplicates of bugs that have been closed for over 6 months. Reopening old bugs confused everyone, including sheriffbot.

### th...@chromium.org (2016-08-30)

Deleting https://crbug.com/chromium/497302#c38 and https://crbug.com/chromium/497302#c39; restoring labels; closing bug.

### mm...@chromium.org (2016-08-30)

Fixing memory tools labels.

### mm...@chromium.org (2016-08-30)

LibFuzzer hasn't been used here.

### du...@chromium.org (2016-08-31)

thestig@/mmoroz@ : Thank you for the update, will update/file them accordingly going further.

### sh...@chromium.org (2016-12-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### th...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Skia Internals>Skia>PDF]

### is...@google.com (2018-09-05)

This issue was migrated from crbug.com/chromium/497302?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/535324]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082225)*
