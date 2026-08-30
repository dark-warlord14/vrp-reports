# V8 TryFastAddDataProperty descriptor-array OOB access

| Field | Value |
|-------|-------|
| **Issue ID** | [512592772](https://issues.chromium.org/issues/512592772) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2026-05-12 |
| **Bounty** | $55,000.00 |

## Description

---

### Report description

V8 TryFastAddDataProperty stale descriptor after map normalization causes release write access violation

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/v8/v8.git> (File: src/objects/js-objects.cc)

---

### The problem

#### Please describe the technical details of the vulnerability

**Vulnerability Details: Stale Descriptor in TryFastAddDataProperty**

During JavaScript object layout transitions, specifically when computing public class fields on a `Function` subclass, V8 is vulnerable to a memory-safety issue (OOB Write).

The vulnerable path is in `src/objects/js-objects.cc` within `TryFastAddDataProperty`.

1. The function captures a descriptor index from a fast transition map: `InternalIndex descriptor = new_map->LastAdded();`
2. It then calls `Map::PrepareForDataProperty`. Under specific allocation pressure and representation changes, this preparation normalizes the map into dictionary mode.
3. The affected stable code lacks a dictionary-map guard after preparation. It migrates the object and reuses the stale fast-map descriptor against `new_map->instance_descriptors()`.

In debug builds, this cleanly fails a descriptor bounds check (`7 vs. 0`). In release builds, the stale descriptor metadata reaches `JSObject::WriteToField`, which decodes out-of-bounds `PropertyDetails`, computes a bogus field index, and performs an invalid write (Access Violation `0xC0000005`).

**Minimal Reproduction PoC:**

` ``javascript
let key = "AA";
let value = 2;

class C extends Function {
f0 = 0;
f1 = 1;
f2 = 2;
f3 = 3;
[key] = value;
}

new C('"use strict"');
value = 1.1;
let o2 = new C('"use strict"');

print("keys=" + Object.getOwnPropertyNames(o2).join(","));
` ``

*Note: The upstream commit `3c869652b039fc1fc9fbe035c6af879317e8b9f3` adds the necessary `if (new_map->is_dictionary_map()) return false;` guard, but this fix appears to be missing in the current stable branch.*

#### Impact analysis

**Impact:** A remote attacker can host a malicious webpage containing the crafted JavaScript payload. When a victim visits the page using an affected version of Google Chrome, the vulnerability triggers a memory corruption (Out-Of-Bounds Write) in the V8 engine within the renderer process.

Currently, this reliably causes a renderer crash (Denial of Service) and leaves the Heap in a corrupted state that fails garbage collection (`Scavenger::Process` fatal error).

**Exploitability Status:**
This is a confirmed, normal-JS reachable memory-safety bug in the stable release. It does not require experimental flags or natives. I am actively researching if this corrupted object state can be groomed and shaped into a controlled read/write primitive to achieve Renderer Code Execution (RCE). At this exact moment, I am reporting it as a HIGH severity memory corruption candidate pending further primitive analysis.

---

### The cause

#### What version of Chrome have you found the security issue in?

148.0.7778.96 stable (V8 engine version 14.8.178.14)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Daniel Rodríguez

## Attachments

- [chrome-148.0.7778.96-regress-506689381-23464a7f-b843-4abb-91e2-95895cab2137.dmp](attachments/chrome-148.0.7778.96-regress-506689381-23464a7f-b843-4abb-91e2-95895cab2137.dmp) (application/octet-stream, 347.4 KB)
- [TECHNICAL-REPORT.md](attachments/TECHNICAL-REPORT.md) (text/markdown, 8.1 KB)
- [REPRODUCTION.md](attachments/REPRODUCTION.md) (text/markdown, 3.2 KB)
- [stable-148-v8-14.8.178.14-regress-506689381-strict-function-field-write-crash-release.txt](attachments/stable-148-v8-14.8.178.14-regress-506689381-strict-function-field-write-crash-release.txt) (text/plain, 2.1 KB)
- [tip-v8-15-regress-506689381-strict-function-field-write-crash-debug.txt](attachments/tip-v8-15-regress-506689381-strict-function-field-write-crash-debug.txt) (text/plain, 54 B)
- [stable-148-v8-14.8.178.14-regress-506689381-strict-function-field-write-crash-asan.txt](attachments/stable-148-v8-14.8.178.14-regress-506689381-strict-function-field-write-crash-asan.txt) (text/plain, 3.9 KB)
- [chrome-148.0.7778.96-regress-506689381-browser-repro-headless.txt](attachments/chrome-148.0.7778.96-regress-506689381-browser-repro-headless.txt) (text/plain, 211 B)
- [stable-148-v8-14.8.178.14-regress-506689381-strict-function-field-allocation-pressure-release.txt](attachments/stable-148-v8-14.8.178.14-regress-506689381-strict-function-field-allocation-pressure-release.txt) (text/plain, 1.4 KB)
- [stable-148-v8-14.8.178.14-regress-506689381-strict-function-field-write-crash-debug.txt](attachments/stable-148-v8-14.8.178.14-regress-506689381-strict-function-field-write-crash-debug.txt) (text/plain, 4.0 KB)
- [regress-506689381-browser-repro.html](attachments/regress-506689381-browser-repro.html) (text/html, 701 B)
- [regress-506689381-strict-function-field-allocation-pressure.js](attachments/regress-506689381-strict-function-field-allocation-pressure.js) (text/javascript, 658 B)
- [regress-506689381-strict-function-field-write-crash.js](attachments/regress-506689381-strict-function-field-write-crash.js) (text/javascript, 451 B)

## Timeline

### is...@chromium.org (2026-05-13)

Thank you for the reminder!

Indeed, we haven't merged the fix to M148, M149 yet. Assigning to the author of [the fix](https://crrev.com/c/7807043) to take care of back-merges.

### is...@chromium.org (2026-05-13)

Ah, I didn't notice the CL has a bug. Marking this as a duplicate of [issue 506689381](https://issues.chromium.org/issues/506689381). We'll track back-merges there.

### ch...@google.com (2026-08-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-08-21)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/512592772)*
