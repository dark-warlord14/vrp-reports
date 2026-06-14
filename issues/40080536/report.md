# Mixed content resources (e.g. scripts) can be loaded using redirection

| Field | Value |
|-------|-------|
| **Issue ID** | [40080536](https://issues.chromium.org/issues/40080536) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader |
| **Reporter** | [Deleted User] |
| **Assignee** | mk...@chromium.org |
| **Created** | 2014-09-25 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36

Steps to reproduce the problem:
I created LayoutTest to illustrate the case:  https://codereview.chromium.org/608473003

What is the expected behavior?
Insecure mixed content shouldn't be loaded.

What went wrong?
stable: script blocked
canary: warning, script executed
blink dev: no warning, script executed

Did this work before? Yes I think it is partially introduced by https://codereview.chromium.org/561153002

Chrome version:   Channel: n/a
OS Version: 
Flash Version:

## Timeline

### [Deleted User] (2014-09-25)

Please add mkwst@chromium.org to CC. I can't or don't know how.

### mb...@chromium.org (2014-09-26)

[Empty comment from Monorail migration]

### mk...@chromium.org (2014-09-26)

Yup. Happily, you found this before the branch point. Thanks!

Patches in flight...

### rs...@chromium.org (2014-09-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8ff9db81f82f40305f85de7e01d82c0a354d6755

commit 8ff9db81f82f40305f85de7e01d82c0a354d6755
Author: mkwst <mkwst@chromium.org>
Date: Sat Sep 27 05:17:27 2014

Pass request context and frame type down to Blink for redirect responses.

We're currently not passing the request context or frame type correctly
when performing redirects, which breaks our mixed content checking
functionality for those requests. This is the Chromium side of a fix.
Blink side to follow.

BUG=417841

Review URL: https://codereview.chromium.org/605103003

Cr-Commit-Position: refs/heads/master@{#297104}

[modify] https://chromium.googlesource.com/chromium/src.git/+/8ff9db81f82f40305f85de7e01d82c0a354d6755/content/child/web_url_loader_impl.cc


### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-09-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/11f1567dce41d3f15481fa2df0f6a334455e7adb

commit 11f1567dce41d3f15481fa2df0f6a334455e7adb
Author: mkwst <mkwst@chromium.org>
Date: Tue Sep 30 10:16:44 2014

WebURLLoaderMock should set a request context for redirects.

BUG=417841

Review URL: https://codereview.chromium.org/607383002

Cr-Commit-Position: refs/heads/master@{#297397}

[modify] https://chromium.googlesource.com/chromium/src.git/+/11f1567dce41d3f15481fa2df0f6a334455e7adb/content/test/weburl_loader_mock.cc


### bu...@chromium.org (2014-09-30)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=182940

------------------------------------------------------------------
r182940 | mkwst@chromium.org | 2014-09-30T16:59:01.043072Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/mixedContent/insecure-script-through-redirection-expected.txt?r1=182940&r2=182939&pathrev=182940
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/mixedContent/resources/frame-with-insecure-script-through-redirection.html?r1=182940&r2=182939&pathrev=182940
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/mixedContent/redirect-https-to-http-script-in-iframe-expected.txt?r1=182940&r2=182939&pathrev=182940
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/mixedContent/insecure-script-through-redirection.html?r1=182940&r2=182939&pathrev=182940
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/ResourceLoader.cpp?r1=182940&r2=182939&pathrev=182940

Mixed Content: Don't override a request's context during redirects.

After https://codereview.chromium.org/605103003/, we have a request
context and frame type for incoming requests generated during redirects.
This patch removes the 'RequestContextInternal' override that was in
place, as it's now actively harmful.

The test was provided by mmaliszkiewicz@opera.com.

BUG=417841

Review URL: https://codereview.chromium.org/608733002
-----------------------------------------------------------------

### mk...@chromium.org (2014-09-30)

Missed the branch, obviously. I'll let this bake on ToT for a day or three, than request a merge back to Beta.

### cl...@chromium.org (2014-10-08)

mkwst@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-15)

mkwst@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-23)

mkwst@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-30)

mkwst@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-10-30)

merge approved for m39 branch 2171.

### cl...@chromium.org (2014-10-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-11-03)

Dev/Bug owner, please merge to M-39 branch 2171 asap. We need all these security fixes to go into the first stable.

### mk...@chromium.org (2014-11-05)

Sorry, this fell off my radar. Merging now.

### bu...@chromium.org (2014-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e05ef94bc59529a827f2667e59f5d2294533b836

commit e05ef94bc59529a827f2667e59f5d2294533b836
Author: Mike West <mkwst@chromium.org>
Date: Wed Nov 05 14:41:25 2014

MIX: Merging two patches back to 2171.

Patch 1
------------------------------------------------------------------------
WebURLLoaderMock should set a request context for redirects.

BUG=417841

Review URL: https://codereview.chromium.org/607383002

Cr-Commit-Position: refs/heads/master@{#297397}
(cherry picked from commit 11f1567dce41d3f15481fa2df0f6a334455e7adb)

Patch 2
------------------------------------------------------------------------
Pass request context and frame type down to Blink for redirect responses.

We're currently not passing the request context or frame type correctly
when performing redirects, which breaks our mixed content checking
functionality for those requests. This is the Chromium side of a fix.
Blink side to follow.

BUG=417841

Review URL: https://codereview.chromium.org/605103003

Cr-Commit-Position: refs/heads/master@{#297104}
(cherry picked from commit 8ff9db81f82f40305f85de7e01d82c0a354d6755)

BUG=417841
TBR=jochen@chromium.org

Review URL: https://codereview.chromium.org/699953004

Cr-Commit-Position: refs/branch-heads/2171@{#357}
Cr-Branched-From: 267aeeb8d85c8503a7fd12bd14654b8ea78d3974-refs/heads/master@{#297060}

[modify] https://chromium.googlesource.com/chromium/src.git/+/e05ef94bc59529a827f2667e59f5d2294533b836/content/child/web_url_loader_impl.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/e05ef94bc59529a827f2667e59f5d2294533b836/content/test/weburl_loader_mock.cc


### bu...@chromium.org (2014-11-05)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=184874

------------------------------------------------------------------
r184874 | mkwst@chromium.org | 2014-11-05T14:54:49.756968Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2171/LayoutTests/http/tests/security/mixedContent/insecure-script-through-redirection.html?r1=184874&r2=184873&pathrev=184874
   M http://src.chromium.org/viewvc/blink/branches/chromium/2171/Source/core/fetch/ResourceLoader.cpp?r1=184874&r2=184873&pathrev=184874
   A http://src.chromium.org/viewvc/blink/branches/chromium/2171/LayoutTests/http/tests/security/mixedContent/insecure-script-through-redirection-expected.txt?r1=184874&r2=184873&pathrev=184874
   A http://src.chromium.org/viewvc/blink/branches/chromium/2171/LayoutTests/http/tests/security/mixedContent/resources/frame-with-insecure-script-through-redirection.html?r1=184874&r2=184873&pathrev=184874
   M http://src.chromium.org/viewvc/blink/branches/chromium/2171/LayoutTests/http/tests/security/mixedContent/redirect-https-to-http-script-in-iframe-expected.txt?r1=184874&r2=184873&pathrev=184874

Merge 182940 "Mixed Content: Don't override a request's context ..."

> Mixed Content: Don't override a request's context during redirects.
> 
> After https://codereview.chromium.org/605103003/, we have a request
> context and frame type for incoming requests generated during redirects.
> This patch removes the 'RequestContextInternal' override that was in
> place, as it's now actively harmful.
> 
> The test was provided by mmaliszkiewicz@opera.com.
> 
> BUG=417841
> 
> Review URL: https://codereview.chromium.org/608733002

TBR=mkwst@chromium.org

Review URL: https://codereview.chromium.org/708443002
-----------------------------------------------------------------

### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-05)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M39 label.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-17)

Thanks for the report! This one qualified for a $1000 reward.

### ti...@google.com (2014-12-09)

Reward payment in progress.

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-29)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-02-06)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/417841?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080536)*
