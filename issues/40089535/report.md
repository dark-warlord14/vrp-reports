# Security:V8:Type Confusion Leads To OOB Read Write

| Field | Value |
|-------|-------|
| **Issue ID** | [40089535](https://issues.chromium.org/issues/40089535) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **CVE IDs** | CVE-2017-15428 |
| **Reporter** | so...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2017-11-07 |
| **Bounty** | $3,000.00 |

## Description

VULNERABILITY DETAILS
There is a type confusion problem in the String.prototype.replace runtime call.If we change the RegExp type(from fast regexp to slow regexp),we will also go to the fast regexp code path.At last,this will cause OOB Read Write of the lastIndex.

VERSION
Chrome Version: 62.0.3202.89 Stable 64 bit
Operating System:  Windows 10 1703 64bit

REPRODUCTION CASE
In the zip file |poc_11_7.zip|,pass is :dabaodabao222
In the debug build,it will crash in CSA_ASSERT(this, IsFastRegExp(context, regexp)) of the function TF_BUILTIN(RegExpReplace, RegExpBuiltinsAssembler);
In the release build,it will crash in the address 0x300000008,and please note that,this addresss we can control it through control the lastIndex value.


## Attachments

- [poc_11_7.zip](attachments/poc_11_7.zip) (application/octet-stream, 434 B)

## Timeline

### so...@gmail.com (2017-11-07)

The patch is very simple,we must generate the code with |BranchIfFastRegExp| after the callback.

### el...@chromium.org (2017-11-08)

This sounds somewhat similar to https://crbug.com/chromium/708247 which was fixed in July.

[Monorail components: Blink>JavaScript]

### aw...@chromium.org (2017-11-08)

To V8 triage sheriff.

### jg...@chromium.org (2017-11-08)

Thanks for the report. #2 is correct, this has the same root cause.

We do the fast path check, then the ToString operation which can end up in user-controlled JS and perform arbitrary changes on the regexp instance.

This affects String.p.{match,replace,search,split}. I'm working on a fix. 

### bu...@chromium.org (2017-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/55a98076827edac8eba775f8025df3749bcd8367

commit 55a98076827edac8eba775f8025df3749bcd8367
Author: jgruber <jgruber@chromium.org>
Date: Wed Nov 08 09:49:33 2017

[string] Fix regexp fast path in MaybeCallFunctionAtSymbol

The regexp fast path in MaybeCallFunctionAtSymbol had an issue in which
we'd call ToString after checking that the given {object} was a fast
regexp and deciding to take the fast path. This is invalid since
ToString() can call into user-controlled JS and may mutate {object}.

There's no way to place the ToString call correctly in this instance:
1 before BranchIfFastRegExp, it's a spec violation if we end up on the
  slow regexp path;
2 the problem with the current location is already described above;
3 and we can't place it into the fast-path regexp builtin (e.g.
  RegExpReplace) either due to the same reasons as 1.

The solution in this CL is to restrict the fast path to string
arguments only, i.e. cases where ToString would be a nop and can safely
be skipped.

Bug: chromium:782145
Change-Id: Ifd35b3a9a6cf2e77c96cb860a8ec98eaec35aa85
Reviewed-on: https://chromium-review.googlesource.com/758257
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#49213}
[modify] https://crrev.com/55a98076827edac8eba775f8025df3749bcd8367/src/builtins/builtins-string-gen.cc
[modify] https://crrev.com/55a98076827edac8eba775f8025df3749bcd8367/src/builtins/builtins-string-gen.h
[add] https://crrev.com/55a98076827edac8eba775f8025df3749bcd8367/test/mjsunit/regress/regress-782145.js


### jg...@chromium.org (2017-11-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-08)

This bug requires manual review: We don't branch M64 until 2017-11-30.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jg...@chromium.org (2017-11-08)

Sorry, Merge-Request-64 should've been for 62, fixing labels. Canary coverage should be coming tonight.

### sh...@chromium.org (2017-11-08)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-11-08)

Please mark this with appropriate OS labels.

M62 is already being ramped-up. If this is not an absolutely critical P0 bug, then fix should be targeted for M63. 

### jg...@chromium.org (2017-11-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-08)

This bug requires manual review: Less than 23 days to go before AppStore submit on M63
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-11-08)

+awhalley@ for merge review

### sh...@chromium.org (2017-11-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-10)

govind@ - good for 63

### go...@chromium.org (2017-11-10)

Approving merge to M63 branch 3239 based on https://crbug.com/chromium/782145#c15. Please merge ASAP. Thank you.

### ha...@chromium.org (2017-11-10)

This has a high security impact and thus should be merged to 62 too.

### jg...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-11-10)

awhalley@ do you have any clue why there is no milestone label applied by security triage anymore?

### bu...@chromium.org (2017-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/cfc3404fa89957994efd8d1f614dd06f8e075ccf

commit cfc3404fa89957994efd8d1f614dd06f8e075ccf
Author: jgruber <jgruber@chromium.org>
Date: Fri Nov 10 08:33:08 2017

Merged: [string] Fix regexp fast path in MaybeCallFunctionAtSymbol

The regexp fast path in MaybeCallFunctionAtSymbol had an issue in which
we'd call ToString after checking that the given {object} was a fast
regexp and deciding to take the fast path. This is invalid since
ToString() can call into user-controlled JS and may mutate {object}.

There's no way to place the ToString call correctly in this instance:
1 before BranchIfFastRegExp, it's a spec violation if we end up on the
  slow regexp path;
2 the problem with the current location is already described above;
3 and we can't place it into the fast-path regexp builtin (e.g.
  RegExpReplace) either due to the same reasons as 1.

The solution in this CL is to restrict the fast path to string
arguments only, i.e. cases where ToString would be a nop and can safely
be skipped.

NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
TBR=yangguo@chromium.org

Bug: chromium:782145
Change-Id: Ifd35b3a9a6cf2e77c96cb860a8ec98eaec35aa85
Reviewed-on: https://chromium-review.googlesource.com/763207
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.2@{#88}
Cr-Branched-From: efa2ac4129d30c7c72e84c16af3d20b44829f990-refs/heads/6.2.414@{#1}
Cr-Branched-From: a861ebb762a60bf5cc2a274faee3620abfb06311-refs/heads/master@{#47693}
[modify] https://crrev.com/cfc3404fa89957994efd8d1f614dd06f8e075ccf/src/builtins/builtins-string-gen.cc
[modify] https://crrev.com/cfc3404fa89957994efd8d1f614dd06f8e075ccf/src/builtins/builtins-string-gen.h
[add] https://crrev.com/cfc3404fa89957994efd8d1f614dd06f8e075ccf/test/mjsunit/regress/regress-782145.js


### bu...@chromium.org (2017-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/a3b2981a1fde72df6594a790dfb76475492f5da1

commit a3b2981a1fde72df6594a790dfb76475492f5da1
Author: jgruber <jgruber@chromium.org>
Date: Fri Nov 10 08:46:58 2017

Merged: [string] Fix regexp fast path in MaybeCallFunctionAtSymbol

The regexp fast path in MaybeCallFunctionAtSymbol had an issue in which
we'd call ToString after checking that the given {object} was a fast
regexp and deciding to take the fast path. This is invalid since
ToString() can call into user-controlled JS and may mutate {object}.

There's no way to place the ToString call correctly in this instance:
1 before BranchIfFastRegExp, it's a spec violation if we end up on the
  slow regexp path;
2 the problem with the current location is already described above;
3 and we can't place it into the fast-path regexp builtin (e.g.
  RegExpReplace) either due to the same reasons as 1.

The solution in this CL is to restrict the fast path to string
arguments only, i.e. cases where ToString would be a nop and can safely
be skipped.

NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
TBR=yangguo@chromium.org

Bug: chromium:782145
Change-Id: Id61611a767f3dc871b47403147818707686c46d1
Reviewed-on: https://chromium-review.googlesource.com/763208
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.3@{#59}
Cr-Branched-From: 094a7c93dcdcd921de3883ba4674b7e1a0feffbe-refs/heads/6.3.292@{#1}
Cr-Branched-From: 18b8fbb528a8021e04a029e06eafee50b918bce0-refs/heads/master@{#48432}
[modify] https://crrev.com/a3b2981a1fde72df6594a790dfb76475492f5da1/src/builtins/builtins-string-gen.cc
[modify] https://crrev.com/a3b2981a1fde72df6594a790dfb76475492f5da1/src/builtins/builtins-string-gen.h
[add] https://crrev.com/a3b2981a1fde72df6594a790dfb76475492f5da1/test/mjsunit/regress/regress-782145.js


### jg...@chromium.org (2017-11-10)

Merged to 62 and 63, removing RBS. Thanks all!

### aw...@chromium.org (2017-11-12)

hablich@ - re https://crbug.com/chromium/782145#c19, no idea - they should be - will follow up!

### aw...@google.com (2017-11-14)

[Empty comment from Monorail migration]

### so...@gmail.com (2017-11-14)

[Comment Deleted]

### aw...@chromium.org (2017-11-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-11-16)

Nice one soulchen8650@! The VRP panel decided to award $3,000 for this report!

### aw...@chromium.org (2017-11-16)

[Empty comment from Monorail migration]

### of...@google.com (2017-11-27)

Node 8 (V8 6.1) backport: https://github.com/nodejs/node/pull/17354

### so...@gmail.com (2017-12-07)

#27:

Hello,awhalley

It seems this issue has been fixed in the stable release 63.0.3239.84:
https://chromereleases.googleblog.com/2017/12/stable-channel-update-for-desktop.html

But I can't see my acknowledgement information on it.Is that something wrong?I want to see my name on it.


### so...@gmail.com (2017-12-07)

Hello,

Could someone answer my question?

### el...@chromium.org (2017-12-07)

Re #30/#31: Andrew works in Pacific Time Zone and can respond to your question when he gets in.

My guess is that this was inadvertently overlooked for the initial M63 notes because the fix got merged all the way back to M62.

### so...@gmail.com (2017-12-07)

I see.

But when can this issue assign a CVE and see my acknowledgement information on the chrome release website?

Thanks

### aw...@google.com (2017-12-07)

Hi soulchen8650@ - very sorry this one fell through the cracks. This is CVE-2017-15428, and I'll update the release blog by the end of play today.

### aw...@google.com (2017-12-08)

see https://chromereleases.googleblog.com/2017/11/stable-channel-update-for-desktop_13.html

### sh...@chromium.org (2018-02-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/782145?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089535)*
