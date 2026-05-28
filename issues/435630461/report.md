# V8 Sandbox Bypass: OOB Write using %TypedArray%.prototype.set due to element type/size TOCTOU

| Field | Value |
|-------|-------|
| **Issue ID** | [435630461](https://issues.chromium.org/issues/435630461) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | kr...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2025-08-01 |
| **Bounty** | $7,000.00 |

## Description

### VULNERABILITY DETAILS

#### Summary

V8 sandbox bypass, writes with controlled content can be made to any address within ~192 GB[1] past the guard region at the end of the sandbox. JS side-effects or background thread(s) can be used to corrupt the destination`TypedArray` during the execution of `%TypedArray%.prototype.set` to use a map of a greater element size, after bounds checks and before write addresses are calculated resulting in addresses that go OOB.

[1] Calculated using `max_index (32 GB - 1 byte -1 byte) * max_element_size (8 bytes) - guard_region_size (64 GB)`.

#### Details

**Note:** For the details here, the slow paths for copying elements are shown because it was convenient to write the PoC (deterministic thanks to JS side-effects). However, the underlying issue can affect the other paths too if timing is favourable and can affect `TypedArray.prototype.copyWithin` too (if the map can be changed right before [element\_size is retrieved and used for the memmove](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/builtins/builtins-typed-array.cc;l=120;drc=63573961c495297e1a3352b09b880640090b96e9)).

Suppose we call `biggestUint8ArrayPossible.set(object with custom getters, a sufficiently large and valid index)`.
Then, after `TypedArrayPrototypeSet` does the necessary bounds validations we end up in:

```
// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/builtins/typed-array-set.tq;l=111;drc=d9a500d6d0429e25d09a9f6b04384cd14caf6095
transitioning macro TypedArrayPrototypeSetArray(
    implicit context: Context, receiver: JSAny)(target: JSTypedArray,
    targetLength: uintptr, arrayArg: JSAny, targetOffset: uintptr,
    targetOffsetOverflowed: bool): void labels IfOffsetOutOfBounds {
  const src: JSReceiver = ToObject_Inline(context, arrayArg);

  // [!!!] This invokes a JS side effect allowing us to change the map of the target
  // to one of a larger element size (eg. BigUint64) instead.
  const srcLengthNum: Number = GetLengthProperty(src);

  if (targetOffsetOverflowed) goto IfOffsetOutOfBounds;

  const srcLength = ChangeSafeIntegerNumberToUintPtr(srcLengthNum)
      otherwise IfOffsetOutOfBounds;
  // [!!!] The following check passes as it is using targetLength which has gone stale
  CheckIntegerIndexAdditionOverflow(srcLength, targetOffset, targetLength)
      otherwise IfOffsetOutOfBounds;

  if (srcLength == 0) return;

  try {
    if (IsBigInt64ElementsKind(target.elements_kind)) goto IfSlow;
    //  ... snipped..
  } label IfSlow deferred {
    TypedArraySet(
        context, target, src, srcLengthNum, Convert<Number>(targetOffset));
  }
}

```

Since none of the validation cares about the actual target whose map had changed, execution continues on to `Runtime_TypedArraySet`, where the wrong `ElementsAccessor` is retrieved:

```
// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/runtime/runtime-typedarray.cc;l=201;drc=2c073a142ee5bcd6418f76c359be2f73fd479857
RUNTIME_FUNCTION(Runtime_TypedArraySet) {
  // ...snipped..
  CHECK(TryNumberToSize(args[2], &length));
  size_t offset;
  CHECK(TryNumberToSize(args[3], &offset));
  // [!] Retrieves the wrong ElementsAcessor here (BigUint64ElementsAccessor instead of Uint8ElementsAccessor)
  ElementsAccessor* accessor = target->GetElementsAccessor(); 
  return accessor->CopyElements(isolate, source, target, length, offset);
}

```

Later on in `CopyElementsHandleSlow`, a JS side-effect can be used to revert the map change and move the external pointer to the edge of the sandbox:

```
// https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/elements.cc;l=4219;drc=2b6168a326657e241cd3f770ca0b316b5f966795
static Tagged<Object> CopyElementsHandleSlow(
    DirectHandle<JSAny> source, DirectHandle<JSTypedArray> destination,
    size_t length, size_t offset) {
  Isolate* isolate = Isolate::Current();
  for (size_t i = 0; i < length; i++) {
    DirectHandle<Object> elem;
    LookupIterator it(isolate, source, i);
    // [!!!] Triggers a JS side-effect, with which we can:
    // 1. Revert the map of destination to the Uint8Array one
    // 2. Change external pointer of destination to point to the end of the sandbox
    ASSIGN_RETURN_FAILURE_ON_EXCEPTION(isolate, elem,
                                        Object::GetProperty(&it));
    // ...snipped...
    // [!!!] Since the map was reverted, the following bounds checks will pass
    // as element_size() is still 1 when GetLengthOrOutOfBounds calls it
    bool out_of_bounds = false;
    size_t new_length = destination->GetLengthOrOutOfBounds(out_of_bounds);
    if (V8_UNLIKELY(out_of_bounds || destination->WasDetached() ||
                    new_length <= offset + i)) {
      continue;
    }
    // [!!!] Calls BigUint64ElementsAccessor's SetImpl
    SetImpl(destination, InternalIndex(offset + i), *elem);
  }
  return *isolate->factory()->undefined_value();
}

```

Then [BigUint64ElementsAccessor's SetImpl](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/elements.cc;l=3419;drc=d32f634388f26f8c7bbb98c82fa9718d30636b1e) calculates the write address like so: `auto* entry_ptr = static_cast<ElementType*>(typed_array->DataPtr()) + entry.raw_value();`

Since `ElementType` is 8 bytes big, with a sufficiently large index we can write past the guard region at the end of the sandbox.

### VERSION

V8 commit: 10ab2cd9337372103f64acf340f3461ed3d970e3

#### REPRODUCTION CASE

**Build args**:

```
is_debug=false
is_asan=true
v8_enable_sandbox=true
v8_enable_memory_corruption_api=true
dcheck_always_on=false
target_cpu="x64"

```

**Shell args**: `--sandbox-testing typed-array-oob-write.js`

**Sample output**:

```
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.

## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 7ff9ffffffef

==== C stack trace ===============================

./out/asan_no_dcheck/d8(__interceptor_backtrace+0x46)[0x5f99b79bf8a6]
./out/asan_no_dcheck/d8(+0x5e30cb2)[0x5f99bc506cb2]
/lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x7258cb445330]
./out/asan_no_dcheck/d8(+0x23cf6db)[0x5f99b8aa56db]
./out/asan_no_dcheck/d8(+0x2c39290)[0x5f99b930f290]
./out/asan_no_dcheck/d8(+0x5c59ef6)[0x5f99bc32fef6]
[end of stack trace]
Segmentation fault

```
### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Sandbox violation

### CREDIT INFORMATION

Reporter credit: Krishna Ravishankar (@krsh732)

## Attachments

- [typed-array-oob-write.js](attachments/typed-array-oob-write.js) (text/javascript, 1.3 KB)

## Timeline

### ja...@chromium.org (2025-08-02)

[security shepherd]

Thanks for the report and clear write up. I'm sending this to clusterfuzz at the moment to get a bisect. Then I'll follow up with the triage.

### cl...@appspot.gserviceaccount.com (2025-08-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5853239408787456.

### ja...@chromium.org (2025-08-02)

[security shepherd]
Following the sandbox bypass triage guidelines:

- severity set to Medium (S2)
- Priority P1
- Security\_Impact-None
- Adding to V8 Sandbox hotlist.

### 24...@project.gserviceaccount.com (2025-08-02)

Testcase 5853239408787456 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5853239408787456.

### kr...@gmail.com (2025-08-02)

Looks like #5 failed because the `v8_enable_sandbox=true` and `v8_enable_memory_corruption_api=true` gn args were missing.

### cl...@appspot.gserviceaccount.com (2025-08-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6094798314209280.

### cl...@chromium.org (2025-08-04)

Bisects to commit b40a364440cbe4353a5eb01f567448872f5a1c6d (<https://crrev.com/c/6140873>)

```
Revert temporary fix for issue 40070746

Now that we have the proper fix in place, we no longer need massive
guard regions after the sandbox to mitigate the issue. However, as
described in the issue, the previous guard region size of 32GB is not
quite sufficient, so we now use 64GB to be on the safe side.

```

Which is related, but didn't introduce this issue.

Marja, can you still take this one?

### ma...@chromium.org (2025-08-04)

Wow, thanks for a cool bug report! I can have a look but I don't promise to get this fully sorted out before my vacation which starts in 48 hours :) (Esp because we might have the same type of bait-and-switching might be going on in other places too, as the report points out.)

### ja...@chromium.org (2025-08-04)

[security shepherd]
Provisionally adding OS as Desktop platforms, since it's in d8.

### kr...@gmail.com (2025-08-04)

> (Esp because we might have the same type of bait-and-switching might be going on in other places too, as the report points out.)

Yeah, FWIW it's definitely possible in other places. Even without trying to race, I can confirm for example that `copyWithin` does suffer from the same issue:

```
// NOTE: this example will fail because of an invalid read outside the sandbox... 
// In practice, it can still be used for controlled content writes past the guard if you
// have an r/w page inside the sandbox that is sufficiently close to the edge.
// Or it can be used to move data past the guard to some other area past the guard.
setField64(dest, kExternalPointerOffset, 0xffffffffffn << kSandboxedPointerShift);
dest.copyWithin({
    valueOf() {
        setField(dest, kMapOffset, bigUint64ArrayMap);
        return kMaxSafeBufferSizeForSandbox - 1;
    }
}, -3, -2);

```

---

As an aside, I tried to think of ways to fix it myself over the weekend, but couldn't get anywhere satisfactory. I thought of adding `SBXCHECK(index < kMaxSafeBufferSizeForSandbox / sizeof(ElementType))` or something to that effect somewhere, but:

1. In my very limited experience, there doesn't seem to be a single unified place or few handful of places where we can just add this check and be done with.
2. Even if all the relevant places were caught now, someone might need to remember to check again in some future code path.

Then I also wondered if the guard regions could be increased so it wouldn't matter even if the bait-and-switch occurred, but I figured massive guard regions are probably undesirable for some reason which is why it was shrunk again in <https://crrev.com/c/6140873>

PS: Hope you have a nice vacation! :)

### ma...@chromium.org (2025-08-05)

After thinking about this a bit... I think, ideally, bait-and-switching like this should be covered by the guard region. That'd require us to set the guard region to 32 GB \* 8 = 256 GB. I'll loop in the sandbox experts to check what they think.

### ma...@chromium.org (2025-08-05)

Update: we can't unfortunately make the guard region big enough (on Android). The current thinking is that just before accessing the backing store with an offset, we need to limit (truncate) the offset. This might need to happen in a bunch of places, and finding all of them is error-prone, but we don't currently have a viable alternative.

### kr...@gmail.com (2025-08-05)

Ah, that's unfortunate but makes sense. Out of curiosity, is there a particular reason for why the offset would be truncated as opposed to a `SBXCHECK?`

### ma...@chromium.org (2025-08-05)

It can be SBXCHECK where that is available, but in generated code we'll prob need to just truncate.

### ma...@chromium.org (2025-08-05)

Oops, I forgot to refer to this bug, but this revert just landed, as a first aid: <https://chromium-review.googlesource.com/c/v8/v8/+/6818343>

I'll work on a proper fix in September after I'm back.

### dx...@google.com (2025-09-05)

Project: v8/v8  

Branch:  main  

Author:  Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6818292>

[sandbox] Add checks to places where we access TypedArrays - part 1

---


Expand for full commit details
```
     
    Because of potential ElementsKind switcheroo, we might be pointing 
    outside the sandbox when doing the data + index * element size math, and 
    the sandbox guard region is not big enough to save us. 
     
    This is still incomplete - other places need similar checks. 
     
    Bug: 435630461 
    Change-Id: Ie206255753d00a51640170e6cb131329aa79b7cb 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6818292 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Reviewed-by: Anton Bikineev <bikineev@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102272}

```

---

Files:

- M `src/objects/elements.cc`
- A `test/mjsunit/sandbox/regress-435630461.js`

---

Hash: [bebbd2a5489dafdcacb42450fd0e414205f1fc65](https://chromiumdash.appspot.com/commit/bebbd2a5489dafdcacb42450fd0e414205f1fc65)  

Date: Thu Sep 4 09:31:14 2025


---

### dx...@google.com (2025-09-09)

Project: v8/v8  

Branch:  main  

Author:  Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6929562>

Revert "[sandbox] Add checks to places where we access TypedArrays - part 1"

---


Expand for full commit details
```
     
    This reverts commit bebbd2a5489dafdcacb42450fd0e414205f1fc65. 
     
    Reason for revert: b/443847151 
     
    Original change's description: 
    > [sandbox] Add checks to places where we access TypedArrays - part 1 
    > 
    > Because of potential ElementsKind switcheroo, we might be pointing 
    > outside the sandbox when doing the data + index * element size math, and 
    > the sandbox guard region is not big enough to save us. 
    > 
    > This is still incomplete - other places need similar checks. 
    > 
    > Bug: 435630461 
    > Change-Id: Ie206255753d00a51640170e6cb131329aa79b7cb 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6818292 
    > Commit-Queue: Marja Hölttä <marja@chromium.org> 
    > Reviewed-by: Anton Bikineev <bikineev@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#102272} 
     
    Bug: 435630461 
    Fixed: 443847151 
    Change-Id: Ie60492c15160bbbaafc455f4dc65219b7bedb068 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6929562 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102342}

```

---

Files:

- M `src/objects/elements.cc`
- D `test/mjsunit/sandbox/regress-435630461.js`

---

Hash: [4987c534f02e16e1871c7e3aaa6f45eac07582ab](https://chromiumdash.appspot.com/commit/4987c534f02e16e1871c7e3aaa6f45eac07582ab)  

Date: Tue Sep 9 08:25:20 2025


---

### dx...@google.com (2025-09-16)

Project: v8/v8  

Branch:  main  

Author:  Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6943372>

Reland: [sandbox] Add checks to places where we access TypedArrays - part 1

---


Expand for full commit details
```
     
    Because of potential ElementsKind switcheroo, we might be pointing 
    outside the sandbox when doing the data + index * element size math, and 
    the sandbox guard region is not big enough to save us. 
     
    This is still incomplete - other places need similar checks. 
     
    Bug: 435630461 
    Change-Id: If5ab3a11c5123718cae8c231dc2e9bce0da21855 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6943372 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Reviewed-by: Anton Bikineev <bikineev@chromium.org> 
    Auto-Submit: Marja Hölttä <marja@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102528}

```

---

Files:

- M `src/objects/elements.cc`
- M `src/sandbox/sandbox.h`
- A `test/mjsunit/sandbox/regress-435630461.js`

---

Hash: [fb9c018080153be9e7517c59913a314842cb0f4b](https://chromiumdash.appspot.com/commit/fb9c018080153be9e7517c59913a314842cb0f4b)  

Date: Fri Sep 12 13:37:18 2025


---

### dx...@google.com (2025-09-19)

Project: v8/v8  

Branch:  main  

Author:  Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6968758>

[sandbox] Faster and more robust sandbox checks for TypedArrays

---


Expand for full commit details
```
     
    This is a rewrite of 
    https://chromium-review.googlesource.com/c/v8/v8/+/6943372 . 
     
    1) In functions iterating TypedArrays, don't SBXCHECK for each element. 
    This is achieved by moving the check from SetImpl into the callers. 
     
    2) Do a more robust check that the element size * length stays within 
    our expected limits. This protects against the ElementsKind switcheroo 
    and also protects us against a potential problem where we first do 
    SBCHECK(InsideSandbox(base_ptr + ...)) and then read the base_ptr again. 
     
    Bug: 445980778,435630461 
    Change-Id: I0545435b0639ed32b1fa7f1514c204f8d003bd3d 
    Fixed: 445980778 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6968758 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102637}

```

---

Files:

- M `src/objects/elements.cc`

---

Hash: [2daccd5242836cd0f2fedbbdf4ea8ad450e0092b](https://chromiumdash.appspot.com/commit/2daccd5242836cd0f2fedbbdf4ea8ad450e0092b)  

Date: Fri Sep 19 12:04:16 2025


---

### om...@google.com (2026-01-12)

@ma...@google.com did the CLs in comments #19 and #20 cover all known access?
I see a "part 1" but no other parts, and wondering what's remains open here.

### ma...@chromium.org (2026-01-13)

Current status:

Unfortunately I haven't been able to audit all the TypedArray-related code to see whether this problem occurs in other places.

Most runtime funcs probably go through these elements.cc bottlenecks, but there might be other code paths which have this problem.

### ml...@google.com (2026-01-13)

As discussed offline: The concrete problem has been fixed.

Follow up auditing work is tracked in [issue 475479180](https://issues.chromium.org/issues/475479180).

### kr...@gmail.com (2026-01-13)

Re [comment#22](https://issues.chromium.org/issues/435630461#comment22) and [comment#23](https://issues.chromium.org/issues/435630461#comment23): I think `copyWithin` as alluded to in [comment#1](https://issues.chromium.org/issues/435630461#comment1) and later shown in [comment#11](https://issues.chromium.org/issues/435630461#comment11) is still an issue. Should these comments be restricted? Either way, the fix is simple:

```
diff --git a/src/builtins/builtins-typed-array.cc b/src/builtins/builtins-typed-array.cc
index d283ace0bb0..1069ff0306e 100644
--- a/src/builtins/builtins-typed-array.cc
+++ b/src/builtins/builtins-typed-array.cc
@@ -123,7 +123,12 @@ BUILTIN(TypedArrayPrototypeCopyWithin) {
 
   size_t element_size = array->element_size();
   to = to * element_size;
+  SBXCHECK_LT(to, ArrayBuffer::kMaxByteLength);
   from = from * element_size;
+  SBXCHECK_LT(from, ArrayBuffer::kMaxByteLength);
+  // SBXCHECK for `count` is skipped as both the src and dest of the following
+  // memmove should start inside the sandbox or the guard region. So oversized
+  // counts will end up hitting the guard region anyway.
   count = count * element_size;
 
   uint8_t* data = static_cast<uint8_t*>(array->DataPtr());

```

So feel free to let me know if I should just put up a CL for review.

### ma...@chromium.org (2026-01-14)

Thanks for pointing that out! You're right, CopyWithin does have this problem.

If you'd like to upload a fix, that's of course a very welcome contribution. Otherwise, I'll do it.

You'll prob want SBXCHECK\_LE instead of SBXCHECK\_LT, since the max byte length is still an allowed byte length.

### kr...@gmail.com (2026-01-14)

I'll upload the diff shortly once I run tests.

> You'll prob want SBXCHECK\_LE instead of SBXCHECK\_LT, since the max byte length is still an allowed byte length.

~~Since `from` and `to` are byte indices, I think we want them to be <= max length - 1 which is < max length?~~

Edit: Going to post a patch that just checks `SBXCHECK_LE(element_size * len, ArrayBuffer::kMaxByteLength);` so the above isn't relevant anymore.

### dx...@google.com (2026-01-15)

Project: v8/v8  

Branch:  main  

Author:  Krishna Ravishankar [krishna.ravi732@gmail.com](mailto:krishna.ravi732@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7474043>

[sandbox] SBXCHECK bounds in %TypedArray%.prototype.copyWithin

---


Expand for full commit details
```
     
    Fixed: 435630461 
    Change-Id: Id800f8f620abbd790cd5bcf2f62fa1d4c8545d0a 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7474043 
    Reviewed-by: Marja Hölttä <marja@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Auto-Submit: Krishna Ravishankar <krishna.ravi732@gmail.com> 
    Cr-Commit-Position: refs/heads/main@{#104712}

```

---

Files:

- M `src/builtins/builtins-typed-array.cc`

---

Hash: [79f19850daf5c38193c495aa9f749087018d1fc2](https://chromiumdash.appspot.com/commit/79f19850daf5c38193c495aa9f749087018d1fc2)  

Date: Wed Jan 14 13:56:15 2026


---

### sp...@google.com (2026-01-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Memory corruption outside the V8 sandbox plus a patch bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-03-05)

Project: v8/v8  

Branch:  main  

Author:  Marja Hölttä [marja@chromium.org](mailto:marja@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7637689>

[typed arrays] Fix another case of ElementsKind switcheroo in TypedArray.p.set

---


Expand for full commit details
```
     
    Fixed: 489633222 
    Bug: 435630461 
    Change-Id: Ib5f0348f58a55a154293fe0c5aaa356a8ad9fb8f 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7637689 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Auto-Submit: Marja Hölttä <marja@chromium.org> 
    Commit-Queue: Marja Hölttä <marja@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105616}

```

---

Files:

- M `src/objects/elements.cc`

---

Hash: [3e6b9f2f40dc80af7c98075bcd2b1ed63cdca286](https://chromiumdash.appspot.com/commit/3e6b9f2f40dc80af7c98075bcd2b1ed63cdca286)  

Date: Thu Mar 5 13:05:57 2026


---

### ch...@google.com (2026-04-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/435630461)*
