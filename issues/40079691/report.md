# Security: JavaScript can detect visited links via CSS nested <a><button> + getClientRects height (OSX)

| Field | Value |
|-------|-------|
| **Issue ID** | [40079691](https://issues.chromium.org/issues/40079691) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CSS, Privacy |
| **Platforms** | Mac |
| **Reporter** | fr...@lastfriday.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2014-06-06 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**  

By applying a background color to a CSS selector of "a:visited button", javascript can determine whether a given URL has been visited or not by evaluating the containing element's height via getClientRects(), at least on OSX. It looks like the background-color style causes the <button> to change from a native-looking style to a square style. (The effect can be visually observed too, if you remove the "visibility:hidden" style on the class ".whoa").

**VERSION**  

Chrome Version: 35.0.1916.114 stable  

Operating System: OSX 10.9.3

**REPRODUCTION CASE**  

See attached .html file. Also attaching a screenshot with the containers made visible by removing "visibility:hidden"), but it is not necessary to have the container visible for the script to work.

## Attachments

- [screenshot-buttons-visited-different-height.png](attachments/screenshot-buttons-visited-different-height.png) (image/png, 35.7 KB)
- [index2.html](attachments/index2.html) (text/html, 1.4 KB)

## Timeline

### pa...@chromium.org (2014-06-06)

Thanks for the report and the concise reproduction case!

I can't seem to reproduce the problem on Linux (Chrome 36 beta), for whatever reason. (All items have the same height.) But it does work on OS X.

tsepez, abarth, rsesek: Do you know anyone who could take this bug?

### pa...@chromium.org (2014-06-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-10)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-06-13)

@jchaffraix, could you take a look or help find an owner for this? Thanks.

### cl...@chromium.org (2014-06-22)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-06-24)

Julien - can you please help us find an appropriate owner for this issue?

### jc...@chromium.org (2014-06-27)

@palmer: you can't reproduce it on Linux because we have different styling on native buttons.

The 4px difference is due to a border that gets added to non-native buttons on Mac.

@timwillis: I don't have enough bandwidth for this bug so CC'ing a couple of people in case they want to jump in.

### cl...@chromium.org (2014-07-06)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-07-08)

@leviw: could you please squeeze this onto your todo list?

### le...@chromium.org (2014-07-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-20)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-07-28)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-09)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-17)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-24)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-31)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-08)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-15)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-23)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-30)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-08)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-15)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### le...@chromium.org (2014-10-20)

I started on this ages ago, but I won't get to it in the foreseeable future :(

### cl...@chromium.org (2014-10-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-29)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-10-31)

jchaffraix@ this medium severity security issue needs a bit of TLC - do you know if/when you will be able to look at it, or perhaps suggest other people?

### cl...@chromium.org (2014-11-08)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-15)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-23)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-30)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-07)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-15)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-18)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 58 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-12-19)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 58 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-01-07)

Mike, any ideas on owners from CSS team ? 

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### me...@chromium.org (2015-02-17)

Ping? Any updates on this bug?

### mi...@chromium.org (2015-02-19)

Tim, can you take a look at this please?

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-02-23)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=190632

------------------------------------------------------------------
r190632 | timloh@chromium.org | 2015-02-23T02:46:13.880484Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/resolver/StyleResolver.cpp?r1=190632&r2=190631&pathrev=190632
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/history/visited-link-button-expected.txt?r1=190632&r2=190631&pathrev=190632
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/css/resolver/StyleResolver.h?r1=190632&r2=190631&pathrev=190632
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/history/visited-link-button.html?r1=190632&r2=190631&pathrev=190632

Only compare unvisited background color for LayoutTheme adjustment

This patch makes us compare unvisited background colors consistently
when determining LayoutTheme adjustment. Previously CachedUAStyle would
read out unvisited colors, while authorStyleInfo would read visited
dependent colors.

BUG=381808

Review URL: https://codereview.chromium.org/950743002
-----------------------------------------------------------------

### ti...@chromium.org (2015-02-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-23)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-26)

This will roll in M43 (based on severity and just missing the M42 branch @ 190579).

### ti...@google.com (2015-05-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-01)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-10-09)

Congratulations - our reward panel decided to award you $1,000 for this report. 

Someone from our finance team should be in contact within a week to arrange payment. Please email me at timwillis@ or update this bug if that doesn't happen.

Thanks again for your report!

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### fr...@lastfriday.com (2015-11-07)

Thank you so much for the reward! :)

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/381808?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>CSS, Privacy]
[Monorail mergedwith: crbug.com/chromium/428592]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079691)*
