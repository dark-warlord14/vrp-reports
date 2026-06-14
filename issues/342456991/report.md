# Type confusion in TryFastAddDataProperty

| Field | Value |
|-------|-------|
| **Issue ID** | [342456991](https://issues.chromium.org/issues/342456991) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m-...@github.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2024-05-24 |
| **Bounty** | $25,000.00 |

## Description

VULNERABILITY DETAILS

When cloning an object using `FastAssign` [1], if the `source` object has an accessor, it'll be called to get the property value that is then used in the call of `CreateDataProperty` [2]. In particular, the accessor can cause the map of `target` to become deprecated:

```
var x = {};
x.a0 = 1;
var x1 = {};
x1.a0 = 1;
//Creates a transition from map {a0} to {a0, prop}
x1.prop = 1;

x.__defineGetter__("prop", function() {
  let obj = {};
  obj.a0 = 1.5; //<------ map of x and x1 are now deprecated
  return 1;
});

x.z = 1;
delete x.z;
//Cloning calls accessor `prop` of x before calling `CreateDataProperty` to create property `prop` on target
var y = {...x};

```

`CreateDataProperty` then uses `TryFastAddDataProperty` to add the property `prop` to the `target` object:

```
bool TryFastAddDataProperty(Isolate* isolate, Handle<JSObject> object,
                            Handle<Name> name, Handle<Object> value,
                            PropertyAttributes attributes) {
  Tagged<Map> map =
      TransitionsAccessor(isolate, object->map())
          .SearchTransition(*name, PropertyKind::kData, attributes);
  if (map.is_null()) return false;
  ...
  new_map = Map::PrepareForDataProperty(isolate, new_map, descriptor,
                                        PropertyConstness::kConst, value);
  ...
  object->WriteToField(descriptor,
                       new_map->instance_descriptors()->GetDetails(descriptor),
                       *value);
  return true;
}

```

`TryFastAddDataProperty` first search for a transition `map` to property `prop`. This will find the `map` of `x1`, which is also deprecated. The deprecated `map` is then passed to `Map::PrepareForDataProperty`, which will try to update it:

```
Handle<Map> Map::PrepareForDataProperty(Isolate* isolate, Handle<Map> map,
                                        InternalIndex descriptor,
                                        PropertyConstness constness,
                                        Handle<Object> value) {
  // Update to the newest map before storing the property.
  map = Update(isolate, map);
  // Dictionaries can store any property value.
  DCHECK(!map->is_dictionary_map());
  return UpdateDescriptorForValue(isolate, map, descriptor, constness, value);

```

However, as pointed out in [bug 40062884](https://issues.chromium.org/issues/40062884) (<https://issues.chromium.org/issues/40062884>), updating a deprecated map can cause it to become a dictionary map. As the call `WriteToField` [3] in `TryFastAddDataProperty` still assumes `new_map` is a fast map, it'll use `FastPropertyAtPut` to write the property:

```
void JSObject::WriteToField(InternalIndex descriptor, PropertyDetails details,
                            Tagged<Object> value) {
  ...
  FieldIndex index = FieldIndex::ForDetails(map(), details);
  if (details.representation().IsDouble()) {
    ...
  } else {
    FastPropertyAtPut(index, value);
  }
}

```

When `new_map` becomes a dictionary map due to update, this will cause a confusion between `PropertyArray` and `NameDictionary` and can cause internal properties of the `NameDictionary` to be overwritten, which can then be used to cause OOB access from the `NameDictionary`.

1. <https://source.chromium.org/chromium/chromium/src/+/43a0264b838298d9cb369562af2cf419a2b62987:v8/src/objects/js-objects.cc;l=277>
2. <https://source.chromium.org/chromium/chromium/src/+/43a0264b838298d9cb369562af2cf419a2b62987:v8/src/objects/js-objects.cc;l=394>
3. <https://source.chromium.org/chromium/chromium/src/+/43a0264b838298d9cb369562af2cf419a2b62987:v8/src/objects/js-objects.cc;l=3556>

The bug affects stable version from 125.0.6422.60 onwards and is introduced in this commit: <https://source.chromium.org/chromium/_/chromium/v8/v8/+/f6b1dd8ec7cad9f9794b5176be1bed7e06584015>

Thank you very much for your help and please let me know if there is anything I can help.

VERSION

d8 commit 1ecc8c6 (head) and 12.5.277.8 (stable)
OS: Ubuntu 22.04 LTS

REPRODUCTION CASE

Please find attached two test cases, crash.js and leak\_hole.js. The test case crash.js will just crash with an OOB write, and leak\_hole.js will use the OOB access to leak the `hole` object. Both run on standalone `d8`. The `leak_hole.js` test case uses `--allow-natives-syntax` to print out the `hole` object that is leaked.

CREDIT INFORMATION

Reporter credit: Man Yue Mo of GitHub Security Lab

## Attachments

- [crash.js](attachments/crash.js) (text/javascript, 448 B)
- [leak_hole.js](attachments/leak_hole.js) (text/javascript, 762 B)
- [calc.html](attachments/calc.html) (text/html, 5.8 KB)

## Timeline

### el...@chromium.org (2024-05-28)

Thanks for the report! I reproed the crash with crash.js, and I'm feeding that test case to ClusterFuzz.

### el...@chromium.org (2024-05-28)

Over to v8 shepherd, with provisional Pri-1 Sev-1.

### cl...@appspot.gserviceaccount.com (2024-05-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6306788407181312.

### 24...@project.gserviceaccount.com (2024-05-28)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-05-28)

Detailed Report: https://clusterfuzz.com/testcase?key=6306788407181312

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !map->is_dictionary_map() in map.cc
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=92888:92889

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6306788407181312

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@google.com (2024-05-29)

Great work! Thanks! Leszek, could you please take a look?

### pe...@google.com (2024-05-29)

Setting milestone because of s0/s1 severity.

### ap...@google.com (2024-05-31)

[Details redacted due to bug visibility]

Change-Id: I2e44619d51db043980f1b4ebb9d31a0f0aa0a7aa
https://chrome-internal-review.googlesource.com/7346176


### ap...@google.com (2024-05-31)

Project: v8/v8
Branch: main

commit cbd847cb1c2eaa126f0b96f002241c2ef5aa7c89
Author: Leszek Swirski <leszeks@chromium.org>
Date:   Fri May 31 12:45:57 2024

    [map] Don't update maps in PrepareForDataProperty
    
    ... because we might update to a dictionary map. Instead, DCHECK that
    the map isn't deprecated, and fix callers to first update the map.
    
    Bug: 342456991
    Change-Id: I8a966437d816c8e0200333c4068854432caf5729
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5588058
    Reviewed-by: Igor Sheludko <ishell@chromium.org>
    Auto-Submit: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94175}

M       src/objects/js-objects.cc
M       src/objects/map.cc

https://chromium-review.googlesource.com/5588058


### m-...@github.com (2024-05-31)

Please find attached an exploit on Chrome version 125.0.6422.112. If successful, it should launch the calculator on Ubuntu 22.04. Tested on a build with this config:

```
is_debug = false
symbol_level = 1
blink_symbol_level = 1
dcheck_always_on = false
is_official_build = true
chrome_pgo_phase = 0
v8_symbol_level = 1

```

### le...@chromium.org (2024-05-31)

Nice find, thanks for the report. Should be fixed with the above patch, I suspect we should backmerge the fix.

### pe...@google.com (2024-05-31)

This is sufficiently serious that it should be merged to stable. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M125. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### 24...@project.gserviceaccount.com (2024-06-01)

ClusterFuzz testcase 6306788407181312 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=94174:94175

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### pe...@google.com (2024-06-01)

Merge review required: M126 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-06-01)

Merge review required: M125 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-06-03)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=342456991&entry.958145677=Linux&entry.763880440=Stable&entry.1678852700=High&entry.763402679=Blink>JavaScript&entry.975983575=leszeks@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

### pg...@google.com (2024-06-05)

Merge approved for M126! Please berge the fix to branch 12.6 by Thursday June 13th EOD MTV time to get this fix into the next stable respin

There are no more scheduled releases for M125 - removing label

### sp...@google.com (2024-06-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
$20,000 for high quality report of V8 security bug with demonstrable security impact with impact to Stable channel + $5,000 reward for exploit 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-05)

Congratulations and amazing work, Man Yue Mo! Thank you for your efforts and providing this exceptional report of this V8 issue -- great work!

### m-...@github.com (2024-06-06)

amyressler@ Thanks. I'd like to donate the reward please. Thank you very much for your help.

### pe...@google.com (2024-06-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-06-10)

Project: v8/v8
Branch: refs/branch-heads/12.6

commit 4cc886d6ff3cb052a6766f5fd7be64594f9f3ed9
Author: Leszek Swirski <leszeks@chromium.org>
Date:   Fri May 31 12:45:57 2024

    Merged: [map] Don't update maps in PrepareForDataProperty
    
    ... because we might update to a dictionary map. Instead, DCHECK that
    the map isn't deprecated, and fix callers to first update the map.
    
    (cherry picked from commit cbd847cb1c2eaa126f0b96f002241c2ef5aa7c89)
    
    
    Bug: 342456991
    Change-Id: If6cbcac18201a36716c649d85358b57707b21332
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5615934
    Auto-Submit: Adam Klein <adamk@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/12.6@{#24}
    Cr-Branched-From: 3c9fa12db3183a6f4ea53d2675adb66ea1194529-refs/heads/12.6.228@{#2}
    Cr-Branched-From: 981bb15ba4dbf9e2381dfc94ec2c4af0b9c6a0b6-refs/heads/main@{#93835}

M       src/objects/js-objects.cc
M       src/objects/map.cc

https://chromium-review.googlesource.com/5615934


### pe...@google.com (2024-06-10)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2024-06-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-06-20)

1. <https://crrev.com/c/5638980>
2. Low, but TryFastAddDataProperty() isn't defined in 120, so the changes in js-objects were discarded. We need confirmation from the author that the CL still fixing the issue for 120.
3. 126
4. Yes, with the author's approval.

### rz...@google.com (2024-07-15)

Removing the merge request for LTS-120 as the regressed range from [comment #6](https://issues.chromium.org/issues/342456991#comment6) starts in 125.

### pe...@google.com (2024-09-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### dx...@google.com (2026-05-29)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7883043>

[test] Last batch of regression tests

---


Expand for full commit details
```
     
    TAG=AGY 
     
    Bug: 517688821 
     
    Bug: 40061466 
    Bug: 40066473 
    Bug: 342456991 
    Bug: 343507800 
    Bug: 366381662 
    Bug: 368311899 
    Bug: 372269618 
    Bug: 383647255 
    Bug: 392521083 
    Bug: 398999390 
    Bug: 40059920 
    Bug: 40060821 
    Bug: 40064370 
    Bug: 40065138 
    Bug: 40282100 
    Bug: 40892749 
    Bug: 41484971 
    Bug: 420636529 
    Bug: 42203224 
    Bug: 423459708 
    Bug: 450328966 
    Bug: 452296415 
    Bug: 469143679 
    Bug: 476233066 
    Bug: 478659010 
    Bug: 485267831 
    Bug: 508811477 
    Change-Id: I692cb14ebeac04eaa77c867e9377ebd19b4b909b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7883043 
    Auto-Submit: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#107659}

```

---

Files:

- A `test/mjsunit/compiler/regress-40061466.js`
- A `test/mjsunit/maglev/regress-40066473.js`
- A `test/mjsunit/regress/regress-342456991.js`
- A `test/mjsunit/regress/regress-343507800.js`
- A `test/mjsunit/regress/regress-366381662.js`
- A `test/mjsunit/regress/regress-368311899.js`
- A `test/mjsunit/regress/regress-372269618.js`
- A `test/mjsunit/regress/regress-383647255.js`
- A `test/mjsunit/regress/regress-392521083.js`
- A `test/mjsunit/regress/regress-398999390.js`
- A `test/mjsunit/regress/regress-40059920.js`
- A `test/mjsunit/regress/regress-40060821.js`
- A `test/mjsunit/regress/regress-40064370.js`
- A `test/mjsunit/regress/regress-40065138.js`
- A `test/mjsunit/regress/regress-40282100.js`
- A `test/mjsunit/regress/regress-40892749.js`
- A `test/mjsunit/regress/regress-41484971.js`
- A `test/mjsunit/regress/regress-420636529.js`
- A `test/mjsunit/regress/regress-42203224.js`
- A `test/mjsunit/regress/regress-423459708.js`
- A `test/mjsunit/regress/regress-450328966.js`
- A `test/mjsunit/regress/regress-452296415.js`
- A `test/mjsunit/regress/regress-469143679.js`
- A `test/mjsunit/regress/regress-476233066-1.js`
- A `test/mjsunit/regress/regress-476233066-2.js`
- A `test/mjsunit/regress/regress-478659010.js`
- A `test/mjsunit/regress/regress-485267831.js`
- A `test/mjsunit/regress/regress-508811477.js`

---

Hash: [a5d1a1cc6911f1d1c7f30da136c8f252b05a58dc](https://chromiumdash.appspot.com/commit/a5d1a1cc6911f1d1c7f30da136c8f252b05a58dc)  

Date: Fri May 29 12:59:59 2026


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/342456991)*
