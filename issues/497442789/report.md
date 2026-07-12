# V8 Sandbox Bypass: Attacker manipulation of ArrayBufferSweeper linked lists results in dangling ArrayBufferExtension pointers

| Field | Value |
|-------|-------|
| **Issue ID** | [497442789](https://issues.chromium.org/issues/497442789) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Bindings, Blink>JavaScript>GarbageCollection, Infra>Client>V8 |
| **Platforms** | Linux |
| **Reporter** | ma...@popax21.dev |
| **Assignee** | ml...@chromium.org |
| **Created** | 2026-03-29 |
| **Bounty** | $20,000.00 |

## Description

---

### Report description

V8 Liftoff EPT extension handle swap: same-type substitution in sandbox heap causes DetachInternal to free wrong BackingStore. UAF on native heap outside V8 sandbox. 3/3 runs confirmed.

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

The `kArrayBufferExtensionTag` external-pointer entry in V8's External Pointer Table (EPT) violates the substitution-safety invariant required by `v8-internal.h:596`. An attacker with in-sandbox arbitrary read/write can swap the EPT extension handles between two `JSArrayBuffer` objects; calling `ArrayBuffer.prototype.transfer()` on the first buffer causes `DetachInternal()` to free the second buffer's `BackingStore` — a native-heap object **outside the V8 sandbox cage**. The second buffer's TypedArray views then reference freed native heap memory. A 4 KB heap spray reliably reclaims the freed region (100% success, 3/3 runs), providing read + write primitives on native heap memory outside the sandbox.

## Root Cause

**File:** `v8/src/objects/js-array-buffer.cc`, function `DetachInternal`, lines 216–239

```
void JSArrayBuffer::DetachInternal(...) {
  // Reads extension handle from sandbox-resident field at +0x28.
  // If swapped to another buffer's handle, points to wrong extension.
  ArrayBufferExtension* extension = array_buffer->extension();
  if (extension) {
    isolate->heap()->DetachArrayBufferExtension(extension);
    // BUG: Frees the WRONG BackingStore if extension was swapped.
    std::shared_ptr<BackingStore> backing_store = array_buffer->RemoveExtension();
  }
  // Victim buffer still has backing_store -> FREED native heap memory
  array_buffer->set_backing_store(isolate, EmptyBackingStoreBuffer());
}

```

The `ManagedResource::ept_entry_` mitigation does not help: it is set once at creation, never updated after a swap. The zap fires on the wrong entry after the swap.

**Invariant violated:** `v8-internal.h:596` — "code using these tags must be substitution-safe, i.e. still operate safely if external pointers of the same type are swapped by an attacker."

## Threat Model

This is a **second-stage sandbox escape** per Chrome's own severity guidelines (`docs/security/severity-guidelines.md`): "renderer sandbox escapes fall into [S1/High]." The prerequisite (in-sandbox R/W) is modeled via `Sandbox.MemoryView` from the official `v8_enable_memory_corruption_api` testing API. No flags are required on Chrome stable to make the JSArrayBuffer fields writable — they are sandbox-resident by design.

## Reproduction

```
# Build V8 with sandbox testing API
gn gen out/Release --args='v8_enable_sandbox=true v8_enable_memory_corruption_api=true is_debug=false'
ninja -C out/Release d8

# Run PoC (3 consecutive runs, 100% reliability)
./out/Release/d8 --sandbox-testing --expose-gc poc_enhanced.js

```

**Expected output (confirmed 3/3 runs, V8 14.8.0, commit abc9bc13bb1):**

```
[+] *** UAF CONFIRMED at size 0x1000 ***
[+] *** SPRAY LANDED! Heap reuse proven! ***
[+] *** CROSS-BUFFER WRITE CONFIRMED in spray[0] ***

```
## Fix Recommendation

Add owner verification in `DetachInternal()` before `RemoveExtension()`:

```
Address bs_from_extension = extension->backing_store()->Data();
Address bs_inline = array_buffer->GetBackingStoreBasePointer();
CHECK_EQ(bs_from_extension, bs_inline);

```
## Affected Versions

All Chrome/Chromium with `v8_enable_sandbox=true` (default since ~Chrome 100). Tested on V8 14.8.0 (commit `abc9bc13bb1`, 2026-03-25). **Not yet patched** at tip-of-tree.

#### Impact analysis

**Who can exploit:** Any attacker who can execute JavaScript in a Chrome renderer (via a malicious webpage). The attacker must first obtain in-sandbox arbitrary read/write — a standard prerequisite for V8 sandbox escape bugs, achievable via JIT type confusion, OOB, or similar first-stage vulnerabilities.

**What they gain:**

1. **Read primitive on native heap outside V8 sandbox:** The UAF TypedArray view reads freed-then-reallocated native heap memory, enabling ASLR bypass by leaking Chromium Framework and libc base addresses.
2. **Write primitive on native heap outside V8 sandbox:** The UAF view writes to the sprayed region, enabling vtable pointer overwrites on C++ objects residing in the freed chunk. This leads to arbitrary code execution in the renderer process, **outside the V8 sandbox boundary**.
3. **Silent bypass of V8's crash filter:** The UAF occurs on native heap memory (not sandbox-resident memory), so `--sandbox-testing` and `--sandbox-fuzzing` both exit 0 — V8's own detection layer does not catch this escape.

**Severity:** S1 (High) — Renderer Sandbox Escape per Chrome's severity guidelines. CVSS 8.3 standalone. The substitution-safety invariant (`v8-internal.h:596`) — the design's core defense against same-type EPT handle swaps — is broken for `kArrayBufferExtensionTag`.

**Prior art confirming impact:** [Issue 384186547](https://issues.chromium.org/issues/384186547) (accepted, $20,000) targeted `ArrayBufferExtension` on the native heap via a different trigger, confirming the V8 team classifies writes to `ArrayBufferExtension` as out-of-sandbox writes.

---

### The cause

#### What version of Chrome have you found the security issue in?

V8 14.8.0 (commit abc9bc13bb1, 2026-03-25)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Sandbox Escape

#### How would you like to be publicly acknowledged for your report?

develicit

## Attachments

- [poc_enhanced.js](attachments/poc_enhanced.js) (text/javascript, 4.2 KB)
- [poc_enhanced.js](attachments/poc_enhanced_74913878.js) (text/javascript, 4.2 KB)

## Timeline

### xi...@chromium.org (2026-03-30)

This report does not provide enough information for us to quickly understand and
reproduce a problem. It will be closed as Won't Fix. Once you have gathered the
required information please open a new issue with a brief description that
attaches all necessary pocs, traces and patches as individual files.

In particular:

- attach a complete symbolized trace as `asan.log` including all additional information

For more information see: <https://chromium.googlesource.com/chromium/src/+/master/docs/security/vrp-faq.md#best-practices-for-security-bug-reporting>

### ch...@google.com (2026-07-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/497442789)*
