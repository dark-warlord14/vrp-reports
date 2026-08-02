# Turbolev: incorrent opcode effect modeling can lead to arbitrary code execution

| Field | Value |
|-------|-------|
| **Issue ID** | [503975738](https://issues.chromium.org/issues/503975738) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turboshaft |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pj...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2026-04-19 |
| **Bounty** | $55,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

VULNERABILITY DETAILS

Turbolev: incorrent opcode effect modeling can lead to arbitrary code execution

`StringSliceOp` is modeled as an allocating operation that does not write:

```
struct StringSliceOp : FixedArityOperationT<3, StringSliceOp> {
  static constexpr OpEffects effects =
      OpEffects()
          .CanAllocateWithoutIdentity()
          .CanDependOnChecks();
  // .........
}

```

`LateLoadEliminationAnalyzer` does not invalidate cached memory state for
non-writing operations in the generic path:

```
void LateLoadEliminationAnalyzer::ProcessBlock(const Block& block,
                                               bool compute_start_snapshot) {
  // .........

  for (OpIndex op_idx : graph_.OperationIndices(block)) {
    Operation& op = graph_.Get(op_idx);
    if (ShouldSkipOptimizationStep()) continue;
    if (ShouldSkipOperation(op)) continue;
    switch (op.opcode) {
      // .........
      default:
        CHECK(!op.Effects().can_write());
        TRACE("> Process other op (id=" << op_idx << ")");
        InvalidateAllNonAliasingInputs(op);

        break;
    }
  }

  FinishBlock(&block);
}

```

That means a cached `LoadMapField(s)` survives across `w.slice(0, 2)` even though `StringSliceOp` allocates and a young-generation collection can run during that allocation.

`CheckedInternalizedString` later uses the cached map to decide whether the receiver is already internalized or still a `ThinString`, and the thin-string path reads `ThinString::actual_` directly from the receiver:

```
V<Map> map = __ LoadMapField(object);
V<Word32> instance_type = __ LoadInstanceTypeField(map);
...
V<InternalizedString> intern_string =
    __ template LoadField<InternalizedString>(
        object, AccessBuilder::ForThinStringActual());

```

During scavenge, V8 rewrites a live `ThinString` reference to its canonical internalized target:

```
template <typename THeapObjectSlot>
SlotCallbackResult Scavenger::EvacuateThinString(
    Tagged<Map> map, THeapObjectSlot slot, Tagged<ThinString> object,
    SafeHeapObjectSize object_size) {
  static_assert(std::is_same_v<THeapObjectSlot, FullHeapObjectSlot> ||
                    std::is_same_v<THeapObjectSlot, HeapObjectSlot>,
                "Only FullHeapObjectSlot and HeapObjectSlot are expected here");
  if (shortcut_strings_) {
    // The ThinString should die after Scavenge, so avoid writing the proper
    // forwarding pointer and instead just signal the actual object as forwarded
    // reference.
    Tagged<String> actual = object->actual();
    // ThinStrings always refer to internalized strings, which are always in old
    // space.
    DCHECK(!HeapLayout::InYoungGeneration(actual));
    UpdateHeapObjectReferenceSlot(slot, actual);
    return REMOVE_SLOT;
  }

  DCHECK_EQ(ObjectFields::kMaybePointers,
            Map::ObjectFieldsFrom(map->visitor_id()));
  return EvacuateObjectDefault(map, slot, object, object_size,
                               ObjectFields::kMaybePointers);
}

```

So after the `slice` allocation, the live slot for `s` contains the oldspace internalized string, while late load elimination still believes that the slot has the earlier thinstring map. `CheckedInternalizedString` takes the ThinString path and loads `*(s + 12)` from the now-internalized sequential one-byte string, i.e. from string payload bytes rather than a heap pointer.

EXPLOIT

We would also like to provide an exploit demonstrating the impact of this vulnerability. With this vulnerability, an attacker can craft `fakeobj` primitives very easily.

```
./out.gn/x64.release/d8 --allow-natives-syntax --turbolev ./exp.js
[*] Exploit by Project WhatForLunch
[+] cage base: 0x00002d8700000000
[+] partition alloc: 0x000009d400000000
[+] code ptr table: 0x00007f38c11d8000
[+] dispatch handle: 0x0000000000136000, table offset: 0x0000000000013600
[+] rwx addr: 0x000055c9c95c0980
[+] 🙀 get shell
sh-5.3# echo pwned 
pwned
sh-5.3# 

```

VERSION

Commit: f9c925ae3c037167a19b8bf0f76bbd3b295146e3 (Fri Apr 17 21:04:15 2026)

Bisect: commit introduces the problem.

REPRODUCTION CASE

`poc.js` and `getshell.js` are attached. Please run with:

```
./out.gn/x64.release/d8 \
  --allow-natives-syntax \
  --turbolev \
  ./exp.js

```

release build was compiled with the following args.gn

```
dcheck_always_on = false
is_debug = false
target_cpu = "x64"
is_component_build = false
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
v8_enable_sandbox = false

```

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: CHECK failure, Controlled write on release

CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?

Reporter credit: Project WhatForLunch (@pjwhatforlunch)

## Attachments

- [exp.js](attachments/exp.js) (text/javascript, 7.4 KB)
- [poc.js](attachments/poc.js) (text/javascript, 1.4 KB)
- [release_chrome_pop_calc.mov](attachments/release_chrome_pop_calc.mov) (video/quicktime, 3.5 MB)
- [exp_pop_calc_release_chrome.html](attachments/exp_pop_calc_release_chrome.html) (text/html, 15.8 KB)

## Timeline

### dm...@chromium.org (2026-04-20)

Thanks for the report. That's kind of a dupe of 480438199, cf in particular <https://crbug.com/480438199#comment16>:

> [...] there might be more cases of this happening without going through the CopyFastSmiOrObjectElements builtin, since LateLoadElimination assumes that string shapes "don't matter" (cf <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/turboshaft/late-load-elimination-reducer.h;l=953-969;drc=e137c54cdb8f80c9dc70534ff016aa2e0246b6f0>), and so it assumes that GCs don't invalidate anything. This was true for Turbofan (cf previous link), but isn't true for Turbolev anymore. I'll work on a more generic fix.

That being said, given that I still haven't addressed this problem in 2 months, it might be fair to not dupe-close..

### dm...@chromium.org (2026-04-20)

(triaging note: impact is None given that Turbolev is still disabled by default)

### ar...@google.com (2026-04-20)

> (triaging note: impact is None given that Turbolev is still disabled by default)

Updating flags.

### dm...@chromium.org (2026-04-21)

Fun fact: with `w.slice` (as is the case in your repro), then LateLoadElimination does the wrong thing, but with `w.substring` instead (and same arguments) then the bug comes from ValueNumbering 🥲
(well, LateLoadElimination would also have been wrong, but ValueNumberingReducer just does the wrong elimination before)

### dx...@google.com (2026-04-24)

Project: v8/v8  

Branch:  main  

Author:  Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7789510>

[turbolev] GC can and does invalidate string maps

---


Expand for full commit details
```
     
    This wasn't an issue for Turbofan, since it very rarely rely on 
    specific string maps. However, Maglev care more about string maps, so 
    we need to make sure that we take into account that the GC can change 
    string maps. 
     
    Fixed: 503975738 
    Change-Id: Ib3cfe55748ec1c6460aa60a109a2cb48feadd022 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7789510 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106809}

```

---

Files:

- M `src/compiler/turboshaft/late-load-elimination-reducer.cc`
- M `src/compiler/turboshaft/late-load-elimination-reducer.h`
- M `src/compiler/turboshaft/value-numbering-reducer.h`
- M `test/mjsunit/mjsunit.status`
- A `test/mjsunit/turbolev/regress-503975738-1.js`
- A `test/mjsunit/turbolev/regress-503975738-2.js`

---

Hash: [af59a517e78e418061f7df708986e78e2203e85d](https://chromiumdash.appspot.com/commit/af59a517e78e418061f7df708986e78e2203e85d)  

Date: Thu Apr 23 15:12:35 2026


---

### pj...@gmail.com (2026-04-30)

According to VRP exploit requirement, we would like to provide a full exploit pop calculator with release version of Chrome. We test the exploit on Ubuntu 22.04 and Chrome 146.0.7680.71.

and run with

```
/opt/chrome-linux64/chrome --headless=new --no-sandbox --disable-crashpad --disable-breakpad --disable-crash-reporter --enable-logging=stderr --user-data-dir=/home/user --js-flags="--allow-natives-syntax --expose-gc --turbolev" "http://<name>/exp_pop_calc_release_chrome.html"

```

the exploit and screen recording are attached.

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
High quality. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503975738)*
