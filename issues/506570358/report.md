# V8 Sandbox Escape: CppHeapPointerTable evacuation entry causes out-of-sandbox CppGC mark-bit write

| Field | Value |
|-------|-------|
| **Issue ID** | [506570358](https://issues.chromium.org/issues/506570358) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 149.0.7811.0 |
| **Reporter** | sm...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2026-04-26 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

1. Chrome build with v8 sbx memory corruption api enabled

I used following:

```
is_asan = true
is_component_build = false
symbol_level = 2
dcheck_always_on = false
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true

```

2. Run the attached `poc.html`

In my environment, I used following command:

```
chrome --disable-gpu --ozone-platform=headless --js-flags='--sandbox-testing --expose-gc --stress-compaction' file:///media/samsung870/p0tato/v8/v8/workdir/chrome-cppheap-reach/vrp/poc.html

```

The PoC is GC-layout sensitive. Some runs stop at an earlier metadata read (`erf=0x4`), while successful runs reach the CppGC mark-bit write sink (`erf=0x7`) shown below. If a read-classified violation is observed, please rerun the same command.

- The analysis is still in progress; I will upload a minimized PoC once the trigger conditions are fully understood.

# Problem Description

```
// v8/src/heap/marking-visitor-inl.h
table->Mark(space, handle, slot.address());
Address cpp_heap_pointer = table->Get(handle, kAnyCppHeapPointer);
cpp_marking_state()->MarkAndPush(reinterpret_cast<void*>(cpp_heap_pointer));

```

The marker mutates the table entry state before fetching the pointer value from the same handle. If compaction creates an evacuation entry, the later `Get(handle, kAnyCppHeapPointer)` path does not enforce at runtime that the entry is still a normal pointer entry.

Relevant current-source locations:

- `v8/src/heap/marking-visitor-inl.h` — `VisitCppHeapPointer()` calls `Mark()` then `Get()` then `MarkAndPush()`.
- `v8/src/sandbox/cppheap-pointer-table-inl.h` — `CppHeapPointerTable::Mark()` calls `MaybeCreateEvacuationEntry()`.
- `v8/src/sandbox/compactible-external-entity-table-inl.h` — `MaybeCreateEvacuationEntry()` writes `MakeEvacuationEntry(handle_location)`.
- `v8/src/sandbox/cppheap-pointer-table-inl.h` — `CppHeapPointerTable::Get()` relies on DCHECK before `GetPointer()`.
- `v8/src/heap/cppgc/heap-object-header.h` — `TryMarkAtomic()` performs the final write.

## Crash state

Representative successful run:
...
r15: 000063175aaa1648
di: 000063175aaa1646
dx: 00000000000007cb
ax: 00000000000007ca
ip: 000063172f2c0747
erf: 0000000000000007

```

Interpretation:

- `erf=0x7` indicates a write fault.
- `r15` is the faulting address.
- `ax=0x07ca` and `dx=0x07cb` show the attempted CppGC mark-bit transition.
- The faulting write is the atomic CAS in `HeapObjectHeader::TryMarkAtomic()`.

# Summary
V8 Sandbox Escape: CppHeapPointerTable evacuation entry causes out-of-sandbox CppGC mark-bit write

# Custom Questions
#### Type of crash: 
v8 sandbox violation

# Additional Data
Category: Security \
Chrome Channel: Not sure \
Regression: N/A \

```

## Attachments

- [crash.log](attachments/crash.log) (text/plain, 5.0 KB)
- [poc.html](attachments/poc.html) (text/html, 62.7 KB)
- [crash.log](attachments/crash_75975860.log) (text/plain, 6.5 KB)
- [poc.html](attachments/poc_75991650.html) (text/html, 5.0 KB)
- [fix.patch](attachments/fix.patch) (text/x-diff, 944 B)
- [crash.log](attachments/crash_76004209.log) (text/plain, 3.4 KB)
- [poc.html](attachments/poc_76004210.html) (text/html, 5.1 KB)

## Timeline

### sm...@gmail.com (2026-04-26)

I noticed that current V8 SBX Bypass reward program doesn't accept `--stress-compaction` flag. This PoC doesn't require `--stress-compaction`. Root Cause is same.

```
/path/to/chrome --disable-gpu --headless=new --dump-dom --js-flags='--sandbox-testing --expose-gc --single-threaded' file:///path/to/poc.html

```

### sm...@gmail.com (2026-04-26)

## Bisect

[36f70f432c4d](https://chromium-review.googlesource.com/c/v8/v8/+/5563324) (2024-05-27), `[sandbox] Introduce CppHeapPointerTable and custom tagging scheme`.

The vulnerable CppHeapPointerTable `Get()` path has existed since the initial CppHeapPointerTable commit and has not gained a runtime pointer-entry check.

### sm...@gmail.com (2026-04-26)

## Patch

(If you've confirmed the vulnerability is valid and patch looks good, I wanna upload this as a CL.)

Table compaction algorithm still needs evacuation entries, so the fix should not remove `MaybeCreateEvacuationEntry()`. The security boundary should instead be enforced at the point where a CppHeap pointer table entry is decoded as a CppHeap pointer.

`CppHeapPointerTable::Get()` should reject non-pointer entries in release builds before returning a decoded address. This check must be a sandbox-relevant runtime check, not only a `DCHECK`, because the handle value lives in sandboxed object memory and can be corrupted by the sandbox attacker model.

```
// v8/src/sandbox/cppheap-pointer-table-inl.h
Address CppHeapPointerTableEntry::GetPointer(
    CppHeapPointerTagRange tag_range) const {
  auto payload = payload_.load(std::memory_order_relaxed);
  SBXCHECK(payload.ContainsPointer());
  return payload.Untag(tag_range);
}

bool CppHeapPointerTableEntry::HasPointer(
    CppHeapPointerTagRange tag_range) const {
  auto payload = payload_.load(std::memory_order_relaxed);
  return payload.ContainsPointer() && payload.IsTaggedWithTagIn(tag_range);
}

```

The important part is the `ContainsPointer()` runtime check. A tag-range check alone is insufficient because `kAnyCppHeapPointer` currently spans `kFirstTag..kLastTag`, which includes special table-entry tags such as `kEvacuationEntryTag` and `kFreeEntryTag`. Therefore an evacuation entry can pass the broad tag range even though its payload is a handle-slot address, not a CppHeap object pointer.

### sm...@gmail.com (2026-04-27)

crash PoC without `--dump-dom` flag (tested checkout 3989a516b2b8095cddf76c2c33f9556b14082571, no-ASan):

Run:

```
/path/to/chrome --disable-gpu --headless=new --js-flags='--sandbox-testing --expose-gc --single-threaded' --file:///path/to/poc.html

```

chrome built with:

```
is_debug = false
is_asan = false
is_component_build = false
symbol_level = 2
blink_symbol_level = 2
v8_symbol_level = 2
dcheck_always_on = false
v8_enable_sandbox = true
v8_enable_memory_corruption_api = true

```

### ar...@google.com (2026-04-28)

Thanks for the report. I was able to reproduce the crash with your args and also a smaller set of them:

```
./out/asan/chrome --headless --js-flags='--sandbox-testing --expose-gc' /tmp/poc.html

```

Dominik CYPTAL?

### sm...@gmail.com (2026-04-28)

If you need any additional information for analysis, please feel free to let me know

### di...@chromium.org (2026-04-28)

The crash is a bit tricky to reproduce for me. I have a [CL](https://chromium-review.git.corp.google.com/c/v8/v8/+/7791153) and with it applied I am not able to reproduce this locally anymore. At the same I would expect to see SBXCHECK failures instead - but I am not. So I am not sure if I am still triggering this case. Could you please check whether the CL fixes this?

### sm...@gmail.com (2026-04-28)

[#comment8](https://issues.chromium.org/issues/506570358#comment8) Since it's 2 AM here, I need to sleep now. I’ll check if that CL resolves the issue when I wake up. I’m in the GMT+9 time zone, sorry for the delay...

### di...@chromium.org (2026-04-28)

No worries ;)

I believe I understand now why I don't see SBXCHECK failures with the fix. For this table we return nullptr instead of crashing on [tag mismatches](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/sandbox/tagged-payload.h;l=55;drc=868ed9b7d285b249a3b6dddde4f5fb0f80f608db?q=TaggedPayload::Untag&ss=chromium). It would still be great if you could test the fix as well though.

### sm...@gmail.com (2026-04-29)

I tested the CL locally and confirmed that it behaves as you described. CL looks like it fixes the issue. Thank you for the quick patch.

### dx...@google.com (2026-04-29)

Project: v8/v8  

Branch:  main  

Author:  Dominik Inführ [dinfuehr@chromium.org](mailto:dinfuehr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7791153>

[sandbox] Shrink kAnyCppPointer tag range

---


Expand for full commit details
```
     
    kAnyCppHeapPointer included free list and evacuation entries as well. 
    But those do not contain a valid pointer to a cppgc object. 
     
    Bug: 506570358 
    Change-Id: I5283cf58ceb48e8718004958f257693591272734 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7791153 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Dominik Inführ <dinfuehr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106918}

```

---

Files:

- M `include/v8-sandbox.h`

---

Hash: [1274811629c2e825338c10092115ab9736b9d102](https://chromiumdash.appspot.com/commit/1274811629c2e825338c10092115ab9736b9d102)  

Date: Tue Apr 28 12:40:43 2026


---

### sm...@gmail.com (2026-04-29)

Reporter Credit: Jihyeon Jeong (Compsec Lab, Seoul National University / Research Intern)

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
v8 Sandbox


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### sm...@gmail.com (2026-06-26)

deleted

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/506570358)*
