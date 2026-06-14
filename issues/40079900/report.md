# Penguins Puzzle WebGL game frequent Aw Snap

| Field | Value |
|-------|-------|
| **Issue ID** | [40079900](https://issues.chromium.org/issues/40079900) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Reporter** | co...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2014-06-25 |
| **Bounty** | $3,000.00 |

## Description

Steps to reproduce the problem:
1. Go to http://penguinspuzzle.appspot.com/penguins.html?lev=24 on Chrome for Android
2. Wait for several seconds
3. Tab crashes

What is the expected behavior?
No Crash

What went wrong?
From logcat I seem to always get:

E/v8      (16988): Stacktrace (dead0000-dead0001) 0x6d8080a1 0x6da080d1: 
E/v8      (16988): ==== JS stack trace =========================================
E/v8      (16988): 
E/v8      (16988): Security context: 0x22112c6d <String[33]: http://penguinspuzzle.appspot.com>
E/v8      (16988):     1: DefaultNumber [native runtime.js:381] (this=0x777f9bed <JS Object>#0#,a=0x6d8080a1 <the hole>)
E/v8      (16988):     2: NonNumberToNumber [native runtime.js:325] (this=0x777f9bed <JS Object>#0#,a=0x6d8080a1 <the hole>)
E/v8      (16988):     3: MUL(aka MUL) [native runtime.js:142] (this=0x6d8080a1 <the hole>,a=0x2d964ae1 <Number: 0>)
E/v8      (16988):     8: mat_mult [http://penguinspuzzle.appspot.com/penguins.html?lev=23:428] (this=0x77786629 <JS Global Object>#1#,A=0x2d964725 <JS Array[4]>#2#,B=0x2d9648a1 <JS Array[4]>#3#)
E/v8      (16988):     9: updateView [http://penguinspuzzle.appspot.com/penguins.html?lev=23:~1996] (this=0x777cc2fd <a Level with map 0x6e599289>#4#)
E/v8      (16988):    10: tick [http://penguinspuzzle.appspot.com/penguins.html?lev=23:~2319] (this=0x77786629 <JS Global Object>#1#)
E/v8      (16988):    11: arguments adaptor frame: 1->0
E/v8      (16988): 
E/v8      (16988): ==== Details ===============================================

Crashed report ID: 

How much crashed? Just one tab

Is it a problem with a plugin? N/A 

Did this work before? N/A 

Chrome version: Chrome 35.0.1916.141 1916141  Channel: stable
OS Version: 4.4.2
Flash Version: 

This also happens in a mobile optimised version that I have created (see http://cosinusoidally.github.io/test/index3.html). Does not reproduce on desktop Chrome or any version of Firefox (mobile, desktop and Firefox OS). I've seen the crash on every Android device I have tried (the backtrace above is from a Tegra Note 7).

When I attempt to use Chrome remote debugging the issue seems to disappear.

## Timeline

### kr...@chromium.org (2014-06-27)

Able to repro in S4(SPH-L720) with M37-37.0.2062.2

Crash id -d3ff24b63579143c 

### [Deleted User] (2014-06-27)

[Empty comment from Monorail migration]

### co...@gmail.com (2015-04-02)

This still repros on Chrome for Android  41.0.2272.96 . It has also has reproed on every version of Chrome for Android that I have tested since my initial report.

As far as I can tell it is a v8 bug (since the bug seems to go away if the debugger is enabled), but it could also be a WebGL bug, it's difficult to say as I am quite unfamiliar with low level debugging of Chrome on Android.

### ad...@chromium.org (2015-04-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2015-04-07)

See duped V8 issue for other repros, but I can repro on stable. Looks like we're seeing lots of this on Stable:

https://crash.corp.google.com/browse?q=product.Name%3D%27Chrome_Android%27%20AND%20custom_data.ChromeCrashProto.ptype%3D%27renderer%27%20AND%20product.version%3D%2741.0.2272.96%27%20OMIT%20RECORD%20IF%20SUM(CrashedStackTrace.StackFrame.FunctionName%3D%27v8%3A%3Ainternal%3A%3ALookupIterator%3A%3AGetRoot%27)%20%3D%200

Assigning to verwaest as this is a CHECK in LookupIterator. Also CCing yangguo as this looks similar to https://crbug.com/chromium/403509, but the stack traces are different (not related to DOM exceptions).

Note that from what I can tell this is only seen on Android.

### ve...@chromium.org (2015-04-07)

This only CHECKs in the LookupIterator since someone is leaking an internal object, the hole in this case according to the stacktrace. Probably an ARM-specific bug in this case. Probably something holey-array related given the arrays in the trace. I'll have a look at the repro tomorrow.

### ve...@chromium.org (2015-04-13)

[Empty comment from Monorail migration]

### ve...@chromium.org (2015-04-13)

This exposes a pretty severe security bug. Will be fixed by https://codereview.chromium.org/1087463003/

### bu...@chromium.org (2015-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/434b456b519e62ed814061c87bb424182887170d

commit 434b456b519e62ed814061c87bb424182887170d
Author: verwaest <verwaest@chromium.org>
Date: Mon Apr 13 16:25:38 2015

Fix indirect push

BUG=chromium:388665
LOG=n

Review URL: https://codereview.chromium.org/1087463003

Cr-Commit-Position: refs/heads/master@{#27795}

[modify] http://crrev.com/434b456b519e62ed814061c87bb424182887170d/src/hydrogen.cc
[add] http://crrev.com/434b456b519e62ed814061c87bb424182887170d/test/mjsunit/regress/regress-indirect-push-unchecked.js


### in...@chromium.org (2015-04-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ha...@chromium.org (2015-04-21)

Can we merge this M43? Is this security bug so severe that we need to merge it into M42 stable too?

### ha...@chromium.org (2015-04-21)

Shouldn't this be a Pri=0 or Pri=1?

### ve...@chromium.org (2015-04-21)

Yes this can and should be merged back to wherever necessary. It's a severe security issue. @jkummerow: would you mind merging this back as I'm currently at the chrome/apps memory event?

### ha...@chromium.org (2015-04-22)

Adding Alex (M42) and Anthony (M43) who are handling the Chrome desktop releases.

### ha...@chromium.org (2015-04-22)

[Empty comment from Monorail migration]

### ha...@chromium.org (2015-04-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/baf880d43993ceab4e2c88c23551b4996aaeaa2d

commit baf880d43993ceab4e2c88c23551b4996aaeaa2d
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Wed Apr 22 12:01:42 2015

Version 4.3.61.11 (cherry-pick)

Merged 434b456b519e62ed814061c87bb424182887170d

Fix indirect push

BUG=chromium:388665
LOG=N
R=yangguo@chromium.org

Review URL: https://codereview.chromium.org/1072403011

Cr-Commit-Position: refs/branch-heads/4.3@{#14}
Cr-Branched-From: f5c0a23a505616796a628d64f4ffe377d1fc4bcf-refs/heads/4.3.61@{#1}
Cr-Branched-From: 0a7d4f496a554028de0ab5a963c3a004e693b4cb-refs/heads/master@{#27508}

[modify] http://crrev.com/baf880d43993ceab4e2c88c23551b4996aaeaa2d/include/v8-version.h
[modify] http://crrev.com/baf880d43993ceab4e2c88c23551b4996aaeaa2d/src/hydrogen.cc
[add] http://crrev.com/baf880d43993ceab4e2c88c23551b4996aaeaa2d/test/mjsunit/regress/regress-indirect-push-unchecked.js


### bu...@chromium.org (2015-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/4e2c3b2e093d1fd6b610b51f46b131c4bbdf8038

commit 4e2c3b2e093d1fd6b610b51f46b131c4bbdf8038
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Wed Apr 22 12:06:42 2015

Version 4.2.77.17 (cherry-pick)

Merged 434b456b519e62ed814061c87bb424182887170d

Fix indirect push

BUG=chromium:388665
LOG=N
R=yangguo@chromium.org

Review URL: https://codereview.chromium.org/1095903004

Cr-Commit-Position: refs/branch-heads/4.2@{#20}
Cr-Branched-From: 3dfd929ea07487f2295553df397720d8d75d227c-refs/heads/4.2.77@{#2}
Cr-Branched-From: e0110920d6f98f0ba2ac0d680f635ae3f094a04e-refs/heads/master@{#26757}

[modify] http://crrev.com/4e2c3b2e093d1fd6b610b51f46b131c4bbdf8038/include/v8-version.h
[modify] http://crrev.com/4e2c3b2e093d1fd6b610b51f46b131c4bbdf8038/src/hydrogen.cc
[add] http://crrev.com/4e2c3b2e093d1fd6b610b51f46b131c4bbdf8038/test/mjsunit/regress/regress-indirect-push-unchecked.js


### ti...@google.com (2015-04-22)

amineer@ - will this make the next push of M42?

### am...@chromium.org (2015-04-22)

Yup.

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-20)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-10-09)

Congratulations - our vulnerability reward panel decided to award you $3,000 for this report!

Panel notes: looks nice for exploitation. A tip for future reports - if you provide a minimized crash and a PoC with the report, you are likely to receive a higher bounty payment. Details here: https://www.google.com/about/appsecurity/chrome-rewards/

Our finance team should be in contact within a week to arrange payment. If that doesn't happen, please email me at timwillis@ or update the bug so that I can follow-up.

Thanks again for your report!

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/388665?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/v8/4012]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079900)*
