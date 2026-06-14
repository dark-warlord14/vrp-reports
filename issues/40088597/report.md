# Security: Arbitrary bad cast in optimized Javascript code

| Field | Value |
|-------|-------|
| **Issue ID** | [40088597](https://issues.chromium.org/issues/40088597) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Reporter** | sk...@chromium.org |
| **Assignee** | ms...@chromium.org |
| **Created** | 2017-08-03 |
| **Bounty** | $5,000.00 |

## Description

VULNERABILITY DETAILS
Specially crafted JavaScript can cause Chrome to use an instance of any class as if it was an instance of pretty much any other class. This allows an "arbitrary bad cast": an attacker can call almost any method of almost any class `A` on an object of almost any other class `B`.

In order to trigger this issue, an object of class `A` is first set as the `__proto__` of an object of class `B`. Then, the code repeatedly attempts to use the `B` object as if it was of type `A` by reading/writing an attribute or calling a method that is valid for `A`. This will fail at first and throw an exception, which can be handled using a try ... catch block. After doing this in a loop a number of times, it will eventually succeed. At this point, the code that handles reading/writing the attribute or calling the method of class `A` will be executed on the object of type `B`: this is effectively a bad cast of a `B` object to `A` (or type confusion if you will).

I believe this problem is caused by the JavaScript being optimized by v8 after running repeatedly for some time: unlike the unoptimized code, the optimized code is missing a critical type check. However, I have not been able to confirm this is the root cause, as I am not familiar enough with v8: figuring this out would take time and I would like to have the issue fixed sooner rather than later. Obviously, I was also not able to find out where the type should be inserted in the code to fix this issue. My bet is that it's in the compiled JavaScript that calls the `...Callback` functions in "\gen\blink\bindings\core\v8\": uncompiled JavaScript appears to call this function to set an attribute only if the `__proto__` has not been modified (otherwise it throws an exception). This suggests the check in the uncompiled code happens before this call, and should probably also happen before this call in the compiled JavaScript.

VERSION
Chrome Version: 61.0.3163.26 dev (beta and release not affected, bug reproduces in 62.0.3175.2 Canary)
Operating System: [Windows 10.0.14393 & .15063]

REPRODUCTION CASE
Minimal repro:
var oVictim = new DOMRect();
oVictim.__proto__ = new DOMMatrix();
while (1) try { oVictim.m11; } catch (e) {};

I have attached a minimal repro, a Proof-of-Concept that shows this issue can be used as an arbitrary write-what-where, and a Proof-of-Concept that shows this issue can be used to leak information from memory.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab (crash is in the renderer process)
Crash State: not relevant: this is a bad cast where the attacker can control the class of the object being cast, the class it is being cast to, and the method called; this issue can be triggered without crashing, or with a near arbitrary number of different stacks depending on the classes used and the methods called.
Client ID (if relevant): n/a

EXPLOITABILITY
This bug gives a very high level of control to an attacker and can be easily exploited reliably. The information leak and write-what-where shown in the Proof-of-Concept can be used together to reliably and completely compromise the process. It should be possible to execute arbitrary code bypassing all mitigations to prevent this. Also, as long as site-isolation is not enabled, it should also be possible to turn this issue into a reliable UXSS.

I am about to go on holiday and was unable to finish a working exploit that executes arbitrary code before I go. Obviously, I did not want to sit on this, so I'm reporting this without a full exploit. I would consider writing a working exploit that executes arbitrary code when I get back if you guys would appreciate the effort and the reward would increase sufficiently to justify the effort.




## Attachments

- [repro.html](attachments/repro.html) (text/plain, 133 B)
- [PoC - write-what-where.html](attachments/PoC - write-what-where.html) (text/plain, 1.6 KB)
- [PoC - information disclosure.html](attachments/PoC - information disclosure.html) (text/plain, 12.2 KB)
- [AVR@NULL fdd.fbd @ chrome.exe!chrome_child.dll!blink։։TransformationMatrix։։M11.html](attachments/AVR@NULL fdd.fbd @ chrome.exe!chrome_child.dll!blink։։TransformationMatrix։։M11.html) (text/plain, 167.8 KB)
- [AV_@Invalid 7b5.537 @ chrome.exe!chrome_child.dll!blink։։TransformationMatrix։։SetM11.html](attachments/AV_@Invalid 7b5.537 @ chrome.exe!chrome_child.dll!blink։։TransformationMatrix։։SetM11.html) (text/plain, 177.3 KB)
- [PoC - code execution.html](attachments/PoC - code execution.html) (text/plain, 15.9 KB)

## Timeline

### sk...@chromium.org (2017-08-03)

In case you're interested in crash details, I've attached BugId reports.

repro.html
  => AVR@NULL fdd.fbd @ chrome.exe!chrome_child.dll!blink։։TransformationMatrix։։M11
PoC - write-what-where.html
  => AV_@Invalid 7b5.537 @ chrome.exe!chrome_child.dll!blink։։TransformationMatrix։։SetM11

Obviously, the information disclosure does not cause a crash.

### mb...@chromium.org (2017-08-03)

Thanks for the report! Submitting a full exploit later is perfectly fine. Even if the panel has already reviewed it, we can take a second look once the exploit is ready and will adjust the reward amount based on the table at https://www.google.com/about/appsecurity/chrome-rewards/index.html#rewards

### el...@chromium.org (2017-08-03)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### el...@chromium.org (2017-08-03)

+V8 sheriff

### ms...@chromium.org (2017-08-04)

Seems to be a TurboFan issue.

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### ms...@chromium.org (2017-08-04)

My bisect currently stops at 9dbafbd5d3eeab36fb8aaa48185bd228658783f6, but I am pretty sure that is just because the try-catch disables the lowering before that CL and the actual bug is farther back.

### sh...@chromium.org (2017-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-04)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-08-04)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-08-04)

Pls apply appropriate OSs label. 

+awhalley@ (Security TPM)

### ms...@chromium.org (2017-08-07)

I'll take a look.

### sh...@chromium.org (2017-08-07)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ms...@chromium.org (2017-08-07)

Applies to all OSes. I have a fix in flight: https://chromium-review.googlesource.com/c/603615

### bu...@chromium.org (2017-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/1d92fd2edf771d4d5739dd473f8614af87f722f8

commit 1d92fd2edf771d4d5739dd473f8614af87f722f8
Author: Michael Starzinger <mstarzinger@chromium.org>
Date: Tue Aug 08 08:53:13 2017

[turbofan] Fix missing holder lookup in AccessInfoFactory.

This makes sure we perform a proper holder lookup when trying to inline
API accessors calls in TurboFan. Inlining is completely disabled in case
the holder is not found, otherwise the appropriate holder is passed via
the {PropertyAccessInfo} structure (if different from the receiver).

R=bmeurer@chromium.org
TEST=cctest/test-api/ReceiverSignature
BUG=chromium:752149

Change-Id: I7b192724afd99d651b6477b2f2c8b403a10efb9d
Reviewed-on: https://chromium-review.googlesource.com/603615
Commit-Queue: Michael Starzinger <mstarzinger@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#47216}
[modify] https://crrev.com/1d92fd2edf771d4d5739dd473f8614af87f722f8/src/compiler/access-info.cc
[modify] https://crrev.com/1d92fd2edf771d4d5739dd473f8614af87f722f8/src/compiler/js-native-context-specialization.cc
[modify] https://crrev.com/1d92fd2edf771d4d5739dd473f8614af87f722f8/src/compiler/js-native-context-specialization.h
[modify] https://crrev.com/1d92fd2edf771d4d5739dd473f8614af87f722f8/test/cctest/test-api.cc


### ms...@chromium.org (2017-08-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-08-09)

Congrats! The VRP panel decided to award $5,000 for this bug!

### aw...@chromium.org (2017-08-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-10)

This bug requires manual review: M61 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-10)

+awhalley@ for M61 merge review.

### aw...@google.com (2017-08-11)

govind@ - good for 61

### go...@chromium.org (2017-08-11)

Approving merge to M61 branch 3163 based on https://crbug.com/chromium/752149#c23. Please merge ASAP. Thank you.

### sh...@chromium.org (2017-08-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-16)

Please merge you change to M61 branch 3163 by 4:00 PM PT tomorrow, Thursday (08/17) so we can take it in for next week Beta release. Thank you.

### bu...@chromium.org (2017-08-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/8fa6b0cd85c5288b922b65ff06d44e24905ff10f

commit 8fa6b0cd85c5288b922b65ff06d44e24905ff10f
Author: Michael Starzinger <mstarzinger@google.com>
Date: Mon Aug 21 08:51:20 2017

Merged: [turbofan] Fix missing holder lookup in AccessInfoFactory.

Revision: 1d92fd2edf771d4d5739dd473f8614af87f722f8

BUG=chromium:752149
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=jarin@chromium.org

Change-Id: I02e7ee93e8c5eb5f3f73cdb1c30eaf71cd40e3f6
Reviewed-on: https://chromium-review.googlesource.com/623048
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.1@{#51}
Cr-Branched-From: 1bf2e10ddb194d4c2871a87a4732613419de892d-refs/heads/6.1.534@{#1}
Cr-Branched-From: e825c4318eb2065ffdf9044aa6a5278635c36427-refs/heads/master@{#46746}
[modify] https://crrev.com/8fa6b0cd85c5288b922b65ff06d44e24905ff10f/src/compiler/access-info.cc
[modify] https://crrev.com/8fa6b0cd85c5288b922b65ff06d44e24905ff10f/src/compiler/js-native-context-specialization.cc
[modify] https://crrev.com/8fa6b0cd85c5288b922b65ff06d44e24905ff10f/src/compiler/js-native-context-specialization.h
[modify] https://crrev.com/8fa6b0cd85c5288b922b65ff06d44e24905ff10f/test/cctest/test-api.cc


### go...@chromium.org (2017-08-21)

Removing "Merge-Approved-61" label as this is already merged to M61 at https://crbug.com/chromium/752149#c27.

### sk...@gmail.com (2017-08-21)

[Comment Deleted]

### sk...@chromium.org (2017-08-21)

The arbitrary read/write can be used with my old "R + W = E" technique (http://blog.skylined.nl/20160622001.html) to execute arbitrary code, so this should already prove the issue is easy to exploit. e.g. a recent SSD exploit used the same technique (https://blogs.securiteam.com/index.php/archives/3379.

But in case exploitability is not sufficiently proven, I've attached another PoC that proves control over the instruction pointer by calling 0x41414141. Using the information leak we could create ROP gadgets and then execute them by modifying the instruction pointer, providing another vector to running arbitrary code.

I trust this "demonstrates that the bug reported can be easily, actively and reliably used against [y]our users".

### aw...@google.com (2017-08-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-01-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-22)

[Comment Deleted]

### aw...@google.com (2018-01-22)

Nice one! The VRP Panel decided to increase the reward to $7,500 :-)

### aw...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### sk...@chromium.org (2018-01-22)

Thanks, much appreciated!

### is...@google.com (2018-01-22)

This issue was migrated from crbug.com/chromium/752149?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088597)*
