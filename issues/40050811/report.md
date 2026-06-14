# v8: Wrong JIT code that triggers SIGTRAP at runtime

| Field | Value |
|-------|-------|
| **Issue ID** | [40050811](https://issues.chromium.org/issues/40050811) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ta...@gmail.com |
| **Assignee** | mv...@chromium.org |
| **Created** | 2019-11-27 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36

Steps to reproduce the problem:
The following PoC found by fuzzing crashes the release build of v8 8.0.0 (commit a5376b7e8f647b69184c54462e48e2a4423aff44 on Nov 11th).

PoC:
function write(begin, end, step) {
  for (var i = begin; i >= end; i += step) {
    step = end - begin;
    begin >>>= 805306382;
  }
}

var buffer = new ArrayBuffer(16384);
var view = new Uint32Array(buffer);

for (let i = 0; i < 10000; i++) {
  write(Infinity, 1, view[65536], 1);
}

What is the expected behavior?

What went wrong?
Run d8 in GDB, you are expected to get the crash like below:

Thread 1 "d8" received signal SIGTRAP, Trace/breakpoint trap.
0x00007ea999482bc3 in ?? ()

(gdb) x/10i $pc - 0x10
   0x7ea999482bb3:      test   %esi,0x0(%rcx)
   0x7ea999482bb6:      add    %al,(%rax)
   0x7ea999482bb8:      cmp    -0x20(%r13),%rsp
   0x7ea999482bbc:      jbe    0x7ea999482bfa
   0x7ea999482bc2:      int3   
=> 0x7ea999482bc3:      movabs $0xc800000000,%rcx
   0x7ea999482bcd:      push   %rcx
   0x7ea999482bce:      movabs $0x555557737f10,%rbx
   0x7ea999482bd8:      mov    $0x1,%eax
   0x7ea999482bdd:      movabs $0x7ebfeafc18c1,%rsi

Did this work before? N/A 

Chrome version: 78.0.3904.108  Channel: stable
OS Version: 
Flash Version: 

By Soyeon Park and Wen Xu at SSLab, Georgia Tech

## Timeline

### cl...@chromium.org (2019-11-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6034802327027712.

### pa...@chromium.org (2019-11-27)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2019-11-27)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/b89d4249c0955337d2bd55cc304905fc43a3a2f7 ([nojit] Migrate JSEntry variants to builtins).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2019-11-27)

Detailed Report: https://clusterfuzz.com/testcase?key=6034802327027712

Fuzzer: 
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: Trap
Crash Address: 0x000000000000
Crash State:
  Builtins_JSEntryTrampoline
  Builtins_JSEntry
  v8::internal::Invoke
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=58087:58088

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6034802327027712

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6034802327027712 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### jg...@chromium.org (2019-11-28)

Gotta pass this on since I'm OOO starting now.

### ne...@chromium.org (2019-11-28)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### cl...@chromium.org (2019-11-28)

[Empty comment from Monorail migration]

### mv...@chromium.org (2019-11-28)

[Empty comment from Monorail migration]

### mv...@chromium.org (2019-12-02)

Loop variable analysis doesn't recognize that the initial type of the
loop variable phi combined with the increment type may produce a NaN
result through the addition of two infinities of differing sign.

This leads to unreachable code and a SIGINT crash.

The fix is to consider this case before typing the loop variable phi,
falling back to more conservative typing if discovered.

Fix in flight: https://chromium-review.googlesource.com/c/v8/v8/+/1946352

----
Security implications are, I think, low, because TurboFan recognized the contradiction and inserted a break. But it's a good bug.


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/b8b6075021ade0969c6b8de9459cd34163f7dbe1

commit b8b6075021ade0969c6b8de9459cd34163f7dbe1
Author: Mike Stanton <mvstanton@chromium.org>
Date: Mon Dec 02 15:20:52 2019

[TurboFan] Loop variable analysis requires more sensitivity

Loop variable analysis doesn't recognize that the initial type of the
loop variable phi combined with the increment type may produce a NaN
result through the addition of two infinities of differing sign.

This leads to unreachable code and a SIGINT crash.

The fix is to consider this case before typing the loop variable phi,
falling back to more conservative typing if discovered.

R=neis@chromium.org

Bug: chromium:1028863
Change-Id: Ic4b5189c4c50c5bbe29e46050de630fd0673de9f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1946352
Commit-Queue: Michael Stanton <mvstanton@chromium.org>
Reviewed-by: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65291}

[modify] https://crrev.com/b8b6075021ade0969c6b8de9459cd34163f7dbe1/src/compiler/graph-reducer.cc
[modify] https://crrev.com/b8b6075021ade0969c6b8de9459cd34163f7dbe1/src/compiler/typer.cc
[add] https://crrev.com/b8b6075021ade0969c6b8de9459cd34163f7dbe1/test/mjsunit/regress/regress-crbug-1028863.js


### sh...@chromium.org (2019-12-02)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mv...@chromium.org (2019-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-12-02)

ClusterFuzz testcase 6034802327027712 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=65290:65291

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-12-02)

[Empty comment from Monorail migration]

### mv...@chromium.org (2019-12-03)

I'd like to merge this to 79.

### sh...@chromium.org (2019-12-03)

This bug requires manual review: We are only 6 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-12-03)

This is security severity low, change is not yet baked in canary and we're cutting M79 stable RC today.  Can this wait until M80  OR M79 respin?


+adetaylor@ (Security TPM) 

### mv...@chromium.org (2019-12-03)

Sorry, after further discussion with Georg, I see that it should be security high. The contradiction was found because we run loop peeling, and this happened to give us the information to expose the contradiction (and insert the int3). I'll answer the rest of the questions asap.

### mv...@chromium.org (2019-12-03)

1. The fix has:
 * Full automated unit test coverage (unit test in CL).
  * Deployed in Canary for at least 24 hours
  * Safe Merge: I believe yes. The code change is such that a "bailout path" from loop variable analysis is widened. So the general effect of the change is that we notice more situations in which we should not optimize the loop code more deeply.

2. Here is the CL to merge: https://chromium-review.googlesource.com/c/v8/v8/+/1946352

3. Verified by Clusterfuzz, run 24 hours on Canary.
4. Why required? Security severity is high enough to warrant it.
5. Not a new feature, not behind a flag.

### ad...@google.com (2019-12-03)

Yes, let's merge.

### go...@chromium.org (2019-12-03)

Approving merge to M79 branch 3945, please merge now. We're cutting M79 Stable RC soon. 

### mv...@chromium.org (2019-12-03)

My apologies...Canary coverage is *not* in place. Current canary has v8 4.0.418, and my fix is in 4.0.425. I'll keep a close eye and merge after 24 hours coverage. Mistake on my part !


### go...@chromium.org (2019-12-03)

No worries, thank you mvstanton@.

As this change has no canary coverage yet and we're cutting M79 Stable RC today, we can consider this for next M79 respin so by then change will be well baked in lower channels. 

Flipping back to Merge-Review-79. 

### sh...@chromium.org (2019-12-04)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mv...@chromium.org (2019-12-06)

Hi folks. We now have 24 hours of canary coverage with chrome 80.0.3986.0.

### pb...@chromium.org (2019-12-06)

Approving merge to M79 branch 3945 based on https://crbug.com/chromium/1028863#c26, please merge now I will trigger new M79 stable RC Soon.

### ad...@google.com (2019-12-06)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-12-07)

This is merged to M79 - https://chromium.googlesource.com/v8/v8.git/+/0b240bf91337e72dfcde2e006fff847b6ed70a2c

### go...@chromium.org (2019-12-07)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-10)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### ta...@gmail.com (2019-12-11)

Could you change the credit in the release blog to Soyeon Park and Wen Xu at SSLab, Georgia Tech please, thanks a lot!

### ad...@chromium.org (2019-12-11)

Done, thanks for the update!

### na...@google.com (2019-12-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-17)

Congrats! The Panel decided to reward $5,000 for this report

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1028863?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050811)*
