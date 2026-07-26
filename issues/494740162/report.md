# Use-after-free of std::list iterator in FormFiller::UndoAutofill via duplicate FieldGlobalIds

| Field | Value |
|-------|-------|
| **Issue ID** | [494740162](https://issues.chromium.org/issues/494740162) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | pi...@google.com |
| **Created** | 2026-03-21 |
| **Bounty** | $3,000.00 |

## Description

# Use-after-free of std::list iterator in FormFiller::UndoAutofill via duplicate FieldGlobalIds

## Summary

A use-after-free in the browser process can be triggered by a compromised renderer that sends a FormData containing duplicate FieldRendererIds through the `mojom::AutofillDriver::AskForValuesToFill` IPC. When the user fills a form with Autofill and subsequently undoes the fill, the browser's `FormFiller::UndoAutofill` iterates over all fields including duplicates, erasing fill history entries one by one. Because duplicates were silently collapsed into a single map entry during the fill, the loop drains the map and frees the underlying `std::list` node while a stale iterator to that node remains in use for subsequent iterations. The dangling iterator is not protected by MiraclePtr since the freed object is an STL list node, not a `raw_ptr`-wrapped member. This affects all platforms.

## Bisect

Introducing Commit: `a58a578316bfa8edc0dcc649581e9a394509964d`

- Date: 2025-05-07
- Author: Jihad Hanna [jihadghanna@google.com](mailto:jihadghanna@google.com)
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/6515317>

This CL changed `UndoAutofill` from erasing the entire fill history entry once after the loop to erasing entries per-field inside the loop (to fix [crbug.com/416019464](https://crbug.com/416019464)). The new `EraseFieldFillingEntry` deletes the `std::list` node when the map empties, but the loop still holds `fill_operation_it` — so duplicate field IDs from a compromised renderer can drain the map early and free the node mid-iteration.

## Root Cause

The browser process does not enforce that `FieldRendererId` values are unique within a single `FormData`. The `FormData::fields()` accessor documents this explicitly, noting that collisions can occur when the renderer is compromised:

```
// components/autofill/core/common/form_data.h:295-310
//
// WARNING: `fields` may contain duplicates:
//
// Usually, FormFieldData::global_id() ... uniquely identify
// objects in `fields`. This is reliable enough for practical purposes, but
// not guaranteed.
//
// Collisions are possible in rare cases. Two known scenarios are:
// - The renderer is compromised and sends duplicates.

```

Neither `IsValidFormData()` nor `bad_message::CheckFieldInForm()` reject a FormData with duplicate field IDs. `IsValidFormData()` checks only string lengths and field count; `CheckFieldInForm()` checks only whether a given `field_id` exists somewhere in the form.

When a form is filled through Autofill, `FormAutofillHistory::AddFormFillingEntry` records per-field undo state in a `std::map<FieldGlobalId, FieldFillingEntry>` within a `std::list` node. Because `std::map::emplace` does not overwrite existing entries, duplicate `FieldGlobalId` values in the input are silently collapsed into a single map key:

```
// components/autofill/core/browser/filling/form_autofill_history.cc:64-90
for (const auto [field, autofill_field] :
     base::zip(filled_fields, filled_autofill_fields)) {
  size_ +=
      history_.front()
          .emplace(field->global_id(), FieldFillingEntry(...))
          .second;  // returns false (no increment) for duplicate keys
}

```

The asymmetry emerges during undo. `FormFiller::UndoAutofill` retrieves a single `fill_operation_it` pointing to the list node, then iterates over all fields in the FormData, including every duplicate:

```
// components/autofill/core/browser/filling/form_filler.cc:782-821
for (FormFieldData& field : fields) {
    auto it = fill_operation_it->find(field.global_id());
    CHECK(it != fill_operation_it->end());
    const FormAutofillHistory::FieldFillingEntry& previous_state = it->second;
    // ...
    if (action_persistence == mojom::ActionPersistence::kFill) {
      // ...
      form_autofill_history_.EraseFieldFillingEntry(fill_operation_it,
                                                    field.global_id());
    }
}

```

Each call to `EraseFieldFillingEntry` removes one key from the map. When the map becomes empty, it frees the entire list node:

```
// components/autofill/core/browser/filling/form_autofill_history.cc:98-105
void FormAutofillHistory::EraseFieldFillingEntry(
    std::list<FormFillingEntry>::iterator fill_operation,
    FieldGlobalId field_id) {
  fill_operation->erase(field_id);
  if (fill_operation->empty()) {
    EraseFormFillEntry(fill_operation);  // history_.erase(fill_operation)
  }
}

```

With N unique fields and 2N total fields (each duplicated), the first N iterations of the loop erase all unique keys, draining the map to zero entries and freeing the list node. On iteration N+1, the code dereferences `fill_operation_it` to call `find()` on the freed map, producing a heap-use-after-free in the browser process's main thread.

This UAF is not mitigated by any existing defense. MiraclePtr does not apply because the dangling reference is a standard library list iterator, not a `raw_ptr<>` class member. The `CHECK(it != fill_operation_it->end())` guard executes after the UAF at `fill_operation_it->find()`, so it cannot prevent the invalid access.

## Reproduce

Tested at commit `7c89d33808e551aed6122c1f324864784011c158`.

Apply the renderer-only patch (simulates a compromised renderer by duplicating all fields in `ExtractFormData`):

```
cd ~/chromium/src
git apply patch.diff
autoninja -C out/asan-release chrome

```

Start an HTTP server and launch the ASAN build:

```
python3 -m http.server 8888 &

out/asan-release/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp/poc-$(date +%s)

```

Trigger manually:

1. Navigate to `chrome://settings/addresses`, click "Add", fill in any address, and save.
2. Navigate back to `http://127.0.0.1:8888/poc.html`.
3. Click the **first** form field (name field) and select the autofill address suggestion to fill the form.
4. Click the **first** field (name field) again — it must be the first/leftmost field for the "Undo Autofill" option to appear.
5. Select "Undo Autofill" from the dropdown.

The browser process crashes with the following ASAN report:

```
==3727567==ERROR: AddressSanitizer: heap-use-after-free on address 0x7b485150ee68 at pc 0x56328503622a bp 0x7ffe4ca09270 sp 0x7ffe4ca09268
READ of size 8 at 0x7b485150ee68 thread T0 (chrome)
    #0 in autofill::FormFiller::UndoAutofill(...) gen/third_party/libc++/src/include/__tree:950:54
    #1 in autofill::BrowserAutofillManager::UndoAutofill(...) browser_autofill_manager.cc:2167
    #2 in autofill::BrowserAutofillManager::OnAskForValuesToFillImpl(...) browser_autofill_manager.cc:1273
    ...
    #11 in autofill::mojom::AutofillDriverStubDispatch::Accept(...) autofill_driver.mojom.cc:1899

freed by thread T0 (chrome) here:
    #0 in operator delete
    #1 in std::list<...>::erase(...)
    #2 in autofill::FormAutofillHistory::EraseFieldFillingEntry(...) form_autofill_history.cc:110
    #3 in autofill::FormFiller::UndoAutofill(...) form_filler.cc:818
    #4 in autofill::BrowserAutofillManager::UndoAutofill(...) browser_autofill_manager.cc:2167
    #5 in autofill::BrowserAutofillManager::OnAskForValuesToFillImpl(...) browser_autofill_manager.cc:1273

SUMMARY: AddressSanitizer: heap-use-after-free gen/third_party/libc++/src/include/__tree:950:54 in autofill::FormFiller::UndoAutofill(...)

```

The complete ASAN log is in `asan.log`.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [asan-mac.log](attachments/asan-mac.log) (text/plain, 37.6 KB)
- [poc.html](attachments/poc.html) (text/html, 611 B)
- [patch.diff](attachments/patch.diff) (text/x-diff, 1.1 KB)
- [poc_demo.mp4](attachments/poc_demo.mp4) (video/mp4, 4.0 MB)
- [asan.log](attachments/asan.log) (text/plain, 41.3 KB)

## Timeline

### je...@gmail.com (2026-03-21)

Reproduce Video Here

### el...@google.com (2026-03-24)

Security shepherd: thanks for the report! This reproed for me.

I was using Chromium 2db2ed897cf5211a899bed82f3f2ca330e85d0d4 on macOS 26.3.1a
with this build config:

```
dcheck_always_on = true
is_asan = true
is_component_build = true
is_debug = false
symbol_level = 1
use_remoteexec = true
use_siso = true

```

and I got the attached ASAN report. Given that this requires a bit of a user gesture, and a compromised renderer, this is Sev-1 for us. Over to Autofill :)

### el...@google.com (2026-03-24)

Forgot the actual asan log.

### el...@google.com (2026-03-24)

After some discussion with battre@ about how unlikely the user gestures are, I'm going to knock this down to Sev-2, because it requires both a compromised renderer and a weird user gesture.

### ch...@google.com (2026-03-25)

Setting milestone because of s2 severity.

### ji...@google.com (2026-03-31)

Gianmarco, let me know if you need help with context.

### pi...@google.com (2026-04-09)

A fix for this crash in currently under review [here](https://chromium-review.git.corp.google.com/c/chromium/src/+/7743400).

### dx...@google.com (2026-04-14)

Project: chromium/src  

Branch:  main  

Author:  Gianmarco Picarella [picarella@google.com](mailto:picarella@google.com)  

Link:    <https://chromium-review.googlesource.com/7743400>

Fix use-after-free of std::list iterator in FormFiller::UndoAutofill

---


Expand for full commit details
```
     
    Fixes a use-after-free crash in FormFiller::UndoAutofill(…) when 
    handling forms containing fields with duplicate FieldGlobalId. 
     
    Currently, FormAutofillHistory silently collapses these duplicate IDs 
    into a single entry. However, FormFiller::UndoAutofill(…) iterates over 
    all fields in the FormData to erase them. Calling 
    EraseFieldFillingEntry(…) for the duplicate IDs frees the underlying 
    std::list node prematurely. Subsequent loop iterations then attempt to 
    access this freed memory using a stale iterator, resulting in a browser 
    process crash. 
     
    This change resolved the problem by calling EraseFieldFillingEntry(…) on 
    the subset of unique FieldGlobalIds in a separate for loop. We also 
    fixed a minor bug in FormAutofillHistory::EraseFieldFillingEntry(…) by 
    updating size_ appropriately. 
     
    Bug: 494740162 
    Change-Id: Ic95dee48fa3ef8d2e3688880a3e49a6a37e4442b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7743400 
    Reviewed-by: Christoph Schwering <schwering@google.com> 
    Commit-Queue: Gianmarco Picarella <picarella@google.com> 
    Reviewed-by: Jihad Hanna <jihadghanna@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1614452}

```

---

Files:

- M `components/autofill/core/browser/filling/form_autofill_history.cc`
- M `components/autofill/core/browser/filling/form_autofill_history.h`
- M `components/autofill/core/browser/filling/form_filler.cc`

---

Hash: [c7c2ce4068f1ddf78b2c019a7d4fec6a0a8800ea](https://chromiumdash.appspot.com/commit/c7c2ce4068f1ddf78b2c019a7d4fec6a0a8800ea)  

Date: Tue Apr 14 14:57:24 2026


---

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Highly mitigated sandbox escape with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494740162)*
