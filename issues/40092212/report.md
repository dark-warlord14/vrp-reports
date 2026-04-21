# Function Signature Mismatch Error When Using Dynamic Linking for WebAssembly

| Field | Value |
|-------|-------|
| **Issue ID** | [40092212](https://issues.chromium.org/issues/40092212) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | kn...@gmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2018-08-17 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36

Steps to reproduce the problem:
1. Unzip testcase.zip
2. Start a http server
3. Open application in Chrome e.g. http://localhost:8080
4. Observe function signature mismatch runtime error

What is the expected behavior?
There should be no error and the line "start-:test" should be printed out. This is not reproducible in Firefox.

What went wrong?
Not sure. 

Did this work before? No 

Does this work in other browsers? Yes

Chrome version: 68.0.3440.84  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- [testcase.zip](attachments/testcase.zip) (application/octet-stream, 1.8 MB)

## Timeline

### ds...@chromium.org (2018-08-17)

+cc sbc,jgravelle in case it's a tool bug instead of an engine bug.

[Monorail components: Blink>JavaScript>WebAssembly]

### kn...@gmail.com (2018-08-17)

[Empty comment from Monorail migration]

### kn...@gmail.com (2018-08-17)

I have uploaded my test case again.

### su...@chromium.org (2018-08-19)

[Empty comment from Monorail migration]

### ti...@chromium.org (2018-08-20)

I can reproduce this in ToT Chrome.
It throws a function signature mismatch error which is visible in the devtools console.
Firefox nightly does not exhibit the problem.
Investigating.


### ti...@chromium.org (2018-08-29)

Made some progress debugging this, but haven't root caused it yet.

The application does have some kind of application-level error (which is fine). This manifests in the console message:

"(index):1237 __pad_and_output:__op is null!!!"

I have verified that v8's 3 execution tiers (interpreter, liftoff, and turbofan), as well as Firefox all execute the program up to the error exactly the same afaict (same sequences to calls of imports, same memory checksum).

When the application enters its own error handling code, divergance occurs. Firefox continues to the end of the program and prints a couple more lines, whereas V8's execution tiers run into errors and disagree (turbofan and liftoff throw the signature mismatch and the interpreter throws memory index out of bounds).

Given that the memory state does not diverge before the error handling code, I suspect it might be our implementation of (mutable) globals, so I am looking into that now.

### ti...@chromium.org (2018-08-30)

[Empty comment from Monorail migration]

### ti...@chromium.org (2018-08-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/09a717dbb9666231bc09ed6740f2270fe79f45b0

commit 09a717dbb9666231bc09ed6740f2270fe79f45b0
Author: Ben L. Titzer <titzer@chromium.org>
Date: Thu Aug 30 15:54:14 2018

[wasm] Fix dispatch table instance update

This CL fixes a bug where the receiving instance was updated improperly
in the dispatch table(s) of an imported table.

BUG=chromium:875322
R=mstarzinger@chromium.org

Change-Id: Ib5af238a0847bf332a12863523e897f59f137c1d
Reviewed-on: https://chromium-review.googlesource.com/1196886
Reviewed-by: Michael Starzinger <mstarzinger@chromium.org>
Commit-Queue: Ben Titzer <titzer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#55534}
[modify] https://crrev.com/09a717dbb9666231bc09ed6740f2270fe79f45b0/src/wasm/module-compiler.cc
[add] https://crrev.com/09a717dbb9666231bc09ed6740f2270fe79f45b0/test/mjsunit/wasm/import-table.js


### ti...@chromium.org (2018-08-30)

[Empty comment from Monorail migration]

### ti...@chromium.org (2018-08-30)

Requesting backmerge to 69 and 70.

### sh...@chromium.org (2018-08-30)

This bug requires manual review: We don't branch M70 until 2018-08-30.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-08-30)

This bug requires manual review: We are only 4 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-08-30)

Cl listed at #9 landed 3 hrs back, not in canary yet. We're cutting M69 stable RC today.

+inferno@ for M69 merge review as awhalley@ is OOO. 

### in...@chromium.org (2018-08-30)

Bug needs to get backed on canary first, lets wait on m69 respin for this.

### go...@chromium.org (2018-08-30)

Sure, thank you inferno@.

### sh...@chromium.org (2018-08-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-31)

[Empty comment from Monorail migration]

### ab...@google.com (2018-09-04)

how do results look in canary?

### kn...@gmail.com (2018-09-05)

I just tried dynamic linking and its working on Version 71.0.3542.0 (Official Build) canary (64-bit). Great job!

When can we get this fix onto Chrome production?

### ti...@chromium.org (2018-09-05)

I had a look at crash reports, and everything looks normal with yesterday's canary.

### ab...@google.com (2018-09-05)

approved - branch:3538

### aw...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### ti...@chromium.org (2018-09-06)

This needs to be merged to 69 as well.

### bu...@chromium.org (2018-09-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d67885e6da3d65846a6553e6897a5aa9b30c1150

commit d67885e6da3d65846a6553e6897a5aa9b30c1150
Author: Ben L. Titzer <titzer@chromium.org>
Date: Thu Sep 06 07:39:20 2018

Merged: [wasm] Fix dispatch table instance update

This CL fixes a bug where the receiving instance was updated improperly
in the dispatch table(s) of an imported table.

BUG=chromium:875322
R=​mstarzinger@chromium.org
CC=titzer@chromium.org

Change-Id: I2c1ca840147b1d315abe6d9237822511a1cd826b
Originally-reviewed-on: https://chromium-review.googlesource.com/1196886
No-Try: true
No-Presubmit: true
No-Treechecks: true
Reviewed-on: https://chromium-review.googlesource.com/1208573
Reviewed-by: Michael Starzinger <mstarzinger@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/branch-heads/7.0@{#7}
Cr-Branched-From: 6e2adae6f7f8e891cfd01f3280482b20590427a6-refs/heads/7.0.276@{#1}
Cr-Branched-From: bc08a8624cbbea7a2d30071472bc73ad9544eadf-refs/heads/master@{#55424}
[modify] https://crrev.com/d67885e6da3d65846a6553e6897a5aa9b30c1150/src/wasm/module-compiler.cc
[add] https://crrev.com/d67885e6da3d65846a6553e6897a5aa9b30c1150/test/mjsunit/wasm/import-table.js


### cl...@chromium.org (2018-09-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-09-06)

This is a security bug found outside of Google. Making this a release blocker. We should ensure that it's included in next week's M-69 respin.

### aw...@chromium.org (2018-09-06)

This hasn't had the level of bake time that a stable merge would usually require, but fix would indeed be good to take and we've got confirmation from two senior v8 engineers that they'd like the fix merged, so I'm happy with taking it for 69.

### aw...@chromium.org (2018-09-06)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-09-06)

Approving merge to M69 branch 3497 based on https://crbug.com/chromium/875322#c27 and #28. 

### bu...@chromium.org (2018-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/442977e1ae21e3df4e7cc5cc880f728dcc0c2711

commit 442977e1ae21e3df4e7cc5cc880f728dcc0c2711
Author: Ben L. Titzer <titzer@chromium.org>
Date: Fri Sep 07 08:18:18 2018

Merged: [wasm] Fix dispatch table instance update

This CL fixes a bug where the receiving instance was updated improperly
in the dispatch table(s) of an imported table.

BUG=chromium:875322
R=​mstarzinger@chromium.org
CC=titzer@chromium.org

Change-Id: Iff24953a1fb6a8ab794e12a7a976d544b56fc3c2
Originally-reviewed-on: https://chromium-review.googlesource.com/1196886
No-Try: true
No-Presubmit: true
No-Treechecks: true
Reviewed-on: https://chromium-review.googlesource.com/1212922
Reviewed-by: Michael Starzinger <mstarzinger@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.9@{#45}
Cr-Branched-From: d7b61abe7b48928aed739f02bf7695732d359e7e-refs/heads/6.9.427@{#1}
Cr-Branched-From: b7e108d6016bf6b7de3a34e6d61cb522f5193460-refs/heads/master@{#54504}
[modify] https://crrev.com/442977e1ae21e3df4e7cc5cc880f728dcc0c2711/src/wasm/module-compiler.cc
[add] https://crrev.com/442977e1ae21e3df4e7cc5cc880f728dcc0c2711/test/mjsunit/wasm/import-table.js


### cl...@chromium.org (2018-09-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-11)

Hi knightacesg@ - thanks for the report! The VRP panel has decided to award $3,000 for this bug. A member of our finance team will be in touch to arrange payment. Cheers!

### aw...@google.com (2018-09-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-25)

Pardon the delay. A CVE has has been allocated for this bug, and https://chromereleases.googleblog.com/2018/09/stable-channel-update-for-desktop_11.html updated accordingly. Cheers!

### aw...@chromium.org (2018-09-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### of...@google.com (2018-12-28)

Node.js v10.x PR: https://github.com/nodejs/node/pull/25242

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-08)

titzer@ - is there any reason this still needs to be marked as Restrict-View-Google

### ti...@chromium.org (2019-01-08)

Nope, its fixed and was merged all the way back to 6.9.

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/875322?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092212)*
