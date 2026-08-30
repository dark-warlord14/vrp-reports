# V8 TryFastAddDataProperty descriptor-array OOB access

| Field | Value |
|-------|-------|
| **Issue ID** | [513753575](https://issues.chromium.org/issues/513753575) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2026-05-16 |
| **Bounty** | $55,000.00 |

## Description

---

### Report description

Missing dictionary-map guard in TryFastAddDataProperty after map normalization. It causes the use of a stale descriptor, leading to an invalid write in JSObject::WriteToField.

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/v8/v8.git>

---

### The problem

#### Please describe the technical details of the vulnerability

**Vulnerability Details: Missing Dictionary-Map Guard in `TryFastAddDataProperty`**

The root cause is a memory-safety bug in V8 object properties and map transitions (Bug `506689381`).

`TryFastAddDataProperty` records a fast-map descriptor, calls `Map::PrepareForDataProperty`, and then keeps using that descriptor even when preparation normalizes the map into dictionary mode. In that state, the descriptor no longer refers to a valid fast field in the returned map.

While Debug builds catch this via `DescriptorArray::GetDetails` (using descriptor `7` against `0` descriptors), Release and ASan builds continue execution into `JSObject::WriteToField`. In `WriteToField`, the stale `PropertyDetails` produce an invalid write.

**Reachability & Fix:**
The issue is reachable from normal JavaScript via computed class fields on a class extending `Function`. The stable tree lacks a dictionary-map guard after `Map::PrepareForDataProperty`, which can be fixed by adding `if (new_map->is_dictionary_map()) return false;` immediately after the preparation step.

#### Impact analysis

**Direct Impact:**
The primary impact is a confirmed memory-safety bug causing a release-reachable invalid write in V8 object-property handling from normal JavaScript.

**Exploitability Evidence (Impact Extension):**
To demonstrate the severity of this bug as a renderer-compromise candidate, I have included a supporting exploitability chain. By utilizing a DataView retarget primitive, it is possible to corrupt `WasmTableObject::current_length_`. Because `WebAssembly.Table.get/set` bounds checks rely on this logical length while the actual elements reside in a smaller `FixedArray`, this inflation allows tagged OOB reads and writes past the table's real backing store.

With specific heap grooming, this OOB access shapes into a `JSArray` object-elements to double-elements overlap. This yields:

- Compressed in-cage `addrof` / `fakeobj` primitives for existing heap object pointers.
- Fake `JSArray` construction in controlled double storage.
- Retargetable in-cage JS heap reads/writes.

---

### The cause

#### What version of Chrome have you found the security issue in?

148.0.7778.168 Stable, 148.0.7778.167 Stable (Chrome for Testing)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

Daniel Rodríguez

## Attachments

- [Reports-20260516.zip](attachments/Reports-20260516.zip) (application/x-zip-compressed, 33.3 MB)
- [regress-506689381-strict-function-field-write-crash.js](attachments/regress-506689381-strict-function-field-write-crash.js) (text/javascript, 451 B)
- [regress-506689381-browser-repro.html](attachments/regress-506689381-browser-repro.html) (text/html, 701 B)

## Timeline

### ch...@google.com (2026-05-16)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ch...@google.com (2026-05-20)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### bi...@google.com (2026-05-20)

Leszek, could you ptal and check if it's another dup of [b/506689381](https://issues.chromium.org/issues/506689381)?

### ch...@google.com (2026-08-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/513753575)*
