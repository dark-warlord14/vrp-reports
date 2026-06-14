# Security: Heap-use-after-free in TypedArray.toLocaleString

| Field | Value |
|-------|-------|
| **Issue ID** | [40093490](https://issues.chromium.org/issues/40093490) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2018-12-17 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

TypedArray |join|, |toString|, and |toLocaleString| have been recently ported to Torque. The check whether it is safe to use the fast accessor for TypedArray elements is as follows:

src/v8/src/builtins/array-join.tq:109:  

CannotUseSameArrayAccessor<JSTypedArray>(implicit context: Context)(  

loadFn: LoadJoinElementFn, receiver: JSReceiver, initialMap: Map,  

initialLen: Number): never  

labels Cannot, Can {  

// It is assumed that neither loading a typed array element nor converting a  

// number to string have side-effects. As such, it safe to use the initial  

// LoadJoinElement specialization and it cannot change through out the join  

// call.  

assert(!IsDetachedBuffer(UnsafeCast<JSTypedArray>(receiver).buffer));  

goto Can;  

}

While this comment is correct for |join| and |toString|, |TypedArray.toLocaleString| does have side-effects since it calls |Number.toLocaleString|, which could be redefined by a user.  

The redefined method might detach the typed array's backing store, leading to a use-after-free condition.

**VERSION**  

Google Chrome 73.0.3642.0 (Official Build) canary (32-bit) (cohort: Clang-32)  

Google Chrome 73.0.3639.1 (Official Build) dev (64-bit) (cohort: Dev)

**REPRODUCTION CASE**

<script>
array = new Int8Array(1024 \\* 1024);
Number.prototype.toLocaleString = function() {
try {
postMessage("", "", [array.buffer]);
} catch { }
}
array.toLocaleString();
</script>

The usual TypedArray PoC that steals cross-origin image data is also attached.

## Attachments

- [locale_image.html](attachments/locale_image.html) (text/plain, 1.6 KB)
- [locale.log](attachments/locale.log) (text/plain, 1.5 KB)

## Timeline

### cl...@chromium.org (2018-12-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5154418099748864.

### cl...@chromium.org (2018-12-17)

Testcase 5154418099748864 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5154418099748864.

### ca...@chromium.org (2018-12-17)

Looks like this doesn't repro on CF, but I was able to reproduce the crash locally. Passing to the V8 sheriff for further triage.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2018-12-18)

Bisected on chromium, got range: 615880 (known good), 615882 (first known bad)

This contains the roll of V8 7.3.106: ba46085641fdcec0a2bbc9d1d77f1fe965ef1768

This contains d1c15973d32287e3cb54afbab57a1cc334ab81f2 ([builtins] Port TypedArray join, toString, and toLocaleString to Torque.).

Assigning to Jakob (reviewer).

### jg...@chromium.org (2018-12-18)

Thanks Clemens. Peter, do you have time to take a look in the next days?

### pe...@gmail.com (2018-12-18)

Jakob, I'm taking a look now.
Thanks.

### sh...@chromium.org (2018-12-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/682db7845c6ff77c60073899f9a5c59e22888061

commit 682db7845c6ff77c60073899f9a5c59e22888061
Author: peterwmwong <peter.wm.wong@gmail.com>
Date: Tue Dec 18 15:06:15 2018

[typedarray] Add TA.p.toLocaleString check for a detached buffer.

Bug: chromium:915783
Change-Id: I053ee6e905a98e0aafcabcf0838ada836a05c181
Reviewed-on: https://chromium-review.googlesource.com/c/1382553
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Commit-Queue: Peter Wong <peter.wm.wong@gmail.com>
Cr-Commit-Position: refs/heads/master@{#58327}
[modify] https://crrev.com/682db7845c6ff77c60073899f9a5c59e22888061/src/builtins/array-join.tq
[add] https://crrev.com/682db7845c6ff77c60073899f9a5c59e22888061/test/mjsunit/regress/regress-crbug-915783.js


### jg...@chromium.org (2018-12-18)

Thanks for the quick fix!

### sh...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-07)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-10)

Thanks for your report. The panel has decided to reward $5,000 :) 



### na...@google.com (2019-01-10)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-03-27)

This issue was migrated from crbug.com/chromium/915783?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093490)*
