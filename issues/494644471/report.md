# UAF in UpdateShapeActive of PDF Ink V2

| Field | Value |
|-------|-------|
| **Issue ID** | [494644471](https://issues.chromium.org/issues/494644471) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF>Ink Signatures |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2026-03-21 |
| **Bounty** | $4,000.00 |

## Description

### Summary

[DiscardStroke()](https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdfium/pdfium_engine.cc;l=5077) erases `stroked_pages_unload_preventers_[page_index]` when no `ink_stroke_data_` entries remain for that page, without checking whether `ink_modeled_shape_map_` still holds `FPDF_PAGEOBJECT` handles cached by [LoadV2InkPathsForPage()](https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdfium/pdfium_engine.cc;l=5123). Once unpinned, the page can unload and free the underlying page-object storage. A subsequent Undo calls [UpdateShapeActive()](https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdfium/pdfium_engine.cc;l=5159), which passes the now-dangling handle to `FPDFPageObj_SetIsActive()`, resulting in a renderer UAF.

### Details

[LoadV2InkPathsForPage()](https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdfium/pdfium_engine.cc;l=5123) caches raw `FPDF_PAGEOBJECT` handles in `ink_modeled_shape_map_` and pins the page via `stroked_pages_unload_preventers_` so those handles stay valid:

```
PDFiumEngine::LoadV2InkPathsForPage(int page_index) {
...
  for (auto& read_result : read_results) {
    InkModeledShapeId id(next_ink_modeled_shape_id_++);
    page_shape_map[id] = std::move(read_result.shape);
    ink_modeled_shape_map_[id] = read_result.page_object; // cache raw handle
  }

...
  CHECK(!stroked_pages_unload_preventers_.contains(page_index));

...
  if (!page_shape_map.empty()) {
    stroked_pages_unload_preventers_.insert(
        {page_index, PDFiumPage::ScopedUnloadPreventer(page)}); // pin page
  }
}

```

[DiscardStroke()](https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdfium/pdfium_engine.cc;l=5077) removes the unload preventer by checking only `ink_stroke_data_`, never `ink_modeled_shape_map_`:

```
void PDFiumEngine::DiscardStroke(int page_index, InkStrokeId id) {
  CHECK(PageIndexInBounds(page_index));
  auto it = ink_stroke_data_.find(id);
  CHECK(it != ink_stroke_data_.end());
  for (FPDF_PAGEOBJECT page_object : it->second.page_objects) {
    bool result =
        FPDFPage_RemoveObject(pages_[page_index]->GetPage(), page_object);
    CHECK(result);

    // FPDFPage_RemoveObject() transferred ownership of `page_object` to the
    // caller. Free it since `page_object` is being discarded.
    FPDFPageObj_Destroy(page_object);
  }
  ink_stroke_data_.erase(it);

  bool page_still_has_strokes =
      std::ranges::any_of(ink_stroke_data_, [page_index](const auto& it) {
        return it.second.page_index == page_index;
      });
  if (!page_still_has_strokes) {
    stroked_pages_unload_preventers_.erase(page_index);  // <-- bug: ignores loaded V2 shapes
  }
}

```

[ApplyUndoRedoDiscards()](https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdf_ink_module.cc;l=1764) calls `DiscardStroke` for every stroke in the discarded redo tail. When the discarded stroke is the last user-added stroke on a page that still has preloaded V2 ink, the unload preventer is removed while `ink_modeled_shape_map_` still holds cached handles.

Once unpinned, scrolling the page off-screen frees the underlying page-object storage. A subsequent Undo walks `loaded_v2_shapes_` into [UpdateShapeActive()](https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdfium/pdfium_engine.cc;l=5159), which forwards the now-dangling handle to `FPDFPageObj_SetIsActive()`, leading to the UAF:

```
void PDFiumEngine::UpdateShapeActive(int page_index,
                                     InkModeledShapeId id,
                                     bool active) {
  auto it = ink_modeled_shape_map_.find(id);
  bool result = FPDFPageObj_SetIsActive(it->second, active); // stale handle
}

```
### Bisection

This issue is introduced by the commit <https://chromium-review.googlesource.com/c/chromium/src/+/5997152>, which introduce the vulnerable `LoadV2InkPathsForPage` function.

### Reproduction

Download chrome from <https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1602931.zip>

Put the `background.js`, `manifest.json`, `test.pdf` under a directory as an extension.

Run with

```
./chrome --load-extension=/path/to/ext --no-sandbox --window-size=900,420 about:blank

```

You would observe the UAF shown in `asan.txt`

NOTE that we need the `--window-size=900,420`, since we hardcode the scroll down length in the extension. If we run against other window size, it needs the adjustment of the POC extension accordingly.

> This is also reproducible manually: open the bundled `test.pdf` in Chrome, enter draw mode (which loads the V2 ink paths), draw a stroke then Ctrl+Z, switch to eraser and make any erase gesture, scroll page 1 out of view, then Ctrl+Z. The extension automates the above sequence. Hence you just need to put three attached POC files under an extension directory.

### Suggested Fix

[chrome\_pdf::PDFiumEngine::DiscardStroke()](https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdfium/pdfium_engine.cc;l=5077) should only erase `stroked_pages_unload_preventers_[page_index]` when the page has neither remaining `ink_stroke_data_` entries nor any loaded V2 shapes still represented in `ink_modeled_shape_map_` / `loaded_v2_shapes_`.

We should also reject tale cached shape handles before [chrome\_pdf::PDFiumEngine::UpdateShapeActive()](https://source.chromium.org/chromium/chromium/src/+/main:pdf/pdfium/pdfium_engine.cc;l=5159) calls `FPDFPageObj_SetIsActive()`, so page unload cannot leave a dangling `FPDF_PAGEOBJECT` behind.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 17.9 KB)
- [background.js](attachments/background.js) (text/javascript, 7.7 KB)
- [manifest.json](attachments/manifest.json) (application/json, 325 B)
- [test.pdf](attachments/test.pdf) (application/pdf, 2.5 KB)

## Timeline

### sk...@google.com (2026-03-24)

This report uses a flag that is known to reduce security in the browser, so this
is WontFix. If it still reproduces for you without that flag, please open a new
report.

### he...@gmail.com (2026-03-24)

I wonder which flag which is known to reduce the security in browser?

NOTE that the `--no-sandbox` is just for getting the ASAN trace more conveniently since this is a renderer memory corruption. This can also be reproduced without the `--no-sandbox`.

### ch...@google.com (2026-03-24)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### he...@gmail.com (2026-03-24)

Thank you. I wonder which part of the report is missing. I think I've try my best to make this high-quality report including the details, bisection, reproduction. Does this means you cannot reproduce it or simply based on the flags?

NOTE: There's no other sensitive flags used to break the browser security, and NO explicit security guidelines claims that any of the `--window-size`, `--no-sandbox`, `--load-extension` reduces the security.

To clarify:

1. The `--load-extension` is just for loading the POC extension more conveniently, it is same with the user which download/install the online extension.
2. The `--no-sandbox` is just to disable the renderer sandbox to make us able to observer the ASAN stack trace in the renderer. This does NOT means that the memory corruption only happens only with this flag. Instead, we can also reproduce without this flag, and you would observe that the renderer crash with signal 6 which means the underlying ASAN detects the renderer memory corruption.
3. The `--window-size`, as mentioned in the report, is only used to make the window size fixed to make the page scroll more deterministically. We can also achieve dynamically scroll length in the POC, but it does not effect the reachability of this vulnerability.

Overall, I think it is still a security vulnerability, and I cannot understand why I need to open up a new report since this is complete.

Thank you very much!

### he...@gmail.com (2026-03-24)

I understand you won't reply on this issue since you've decided this is INVALID. Although I didn't get any of the feedback about this report, so called "uses a flag that is known to reduce security" doesn't meets any of the severity guidelines.

Thank you very much and appreciate your decision and this is what I'm surprised since the `--no-sandbox` is always used during security issues among chromium.

### th...@chromium.org (2026-03-24)

1. I tried the PoC with sandboxing turned on in an ASAN-enabled build. I still expect a crash to happen, but it didn't.
2. I tried the manual repro steps, but given test.pdf only has 1 page, how does one actually scroll it out of view?

### th...@chromium.org (2026-03-24)

In any case, with an appropriate PDF, I can repro, so reopening.

### th...@chromium.org (2026-03-25)

Just some nitpicks about the report itself.

- <https://chromium-review.googlesource.com/c/chromium/src/+/5997152> added PDFiumEngine::LoadV2InkPathsForPage(), but it did not add PDFiumEngine::UpdateShapeActive(), so it's related, but did not actually pinpoint when the issue started.
- The suggested fix has the right sentiments, but the concrete suggestions do not quite make sense.

### dx...@google.com (2026-03-25)

Project: chromium/src  

Branch:  main  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7699593>

[PDF Ink Signatures] Fix page unloading prevention for shapes

---


Expand for full commit details
```
     
    In PDFiumEngine, `stroked_pages_unload_preventers_` prevents page 
    unloading if a page has strokes or shapes. However, DiscardStroke() only 
    checks for strokes before removing `stroked_pages_unload_preventers_` 
    entries. Add in the missing check for shapes. 
     
    To help DiscardStroke() determine which pages have shapes, repurpose the 
    existing DCHECK-only `pages_with_loaded_v2_ink_paths_` set. Change its 
    semantics so LoadV2InkPathsForPage() only adds to the set when a page 
    has shapes. The sanity check that `pages_with_loaded_v2_ink_paths_` was 
    performing was not very useful anyway. 
     
    Bug: 494644471 
    Change-Id: I6a29720cd5464d1e7cb04fb0ed51e66d4435c32b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7699593 
    Reviewed-by: Andy Phan <andyphan@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1604965}

```

---

Files:

- M `pdf/pdfium/pdfium_engine.cc`
- M `pdf/pdfium/pdfium_engine.h`
- M `pdf/pdfium/pdfium_engine_unittest.cc`

---

Hash: [96187fc8ea0e2bcf3a316c88a309398783c600f7](https://chromiumdash.appspot.com/commit/96187fc8ea0e2bcf3a316c88a309398783c600f7)  

Date: Wed Mar 25 18:15:27 2026


---

### ch...@google.com (2026-03-26)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-26)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1604965) appears to be after stable branch point (1582197).

Requesting merge to beta (M147) because latest trunk commit (1604965) appears to be after beta branch point (1596535).

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-26)

Merge review required: M147 has already been cut for stable release.

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-26)

Merge review required: M146 is already shipping to stable.

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### th...@chromium.org (2026-03-27)

1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/7699593>

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes

3. Does this fix pose any potential non-verifiable stability risks?

No

4. Does this fix pose any known compatibility risks?

No

5. Does it require manual verification by the test team? If so, please describe required testing.

No

### dr...@chromium.org (2026-03-27)

No crashes in Canary after 24 hours. Approved to merge to M146 and M147. Our release cut for M146 is Monday at 11am Pacific time, so please try to land by then.

### dx...@google.com (2026-03-27)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7707110>

M147: [PDF Ink Signatures] Fix page unloading prevention for shapes

---


Expand for full commit details
```
     
    In PDFiumEngine, `stroked_pages_unload_preventers_` prevents page 
    unloading if a page has strokes or shapes. However, DiscardStroke() only 
    checks for strokes before removing `stroked_pages_unload_preventers_` 
    entries. Add in the missing check for shapes. 
     
    To help DiscardStroke() determine which pages have shapes, repurpose the 
    existing DCHECK-only `pages_with_loaded_v2_ink_paths_` set. Change its 
    semantics so LoadV2InkPathsForPage() only adds to the set when a page 
    has shapes. The sanity check that `pages_with_loaded_v2_ink_paths_` was 
    performing was not very useful anyway. 
     
    (cherry picked from commit 96187fc8ea0e2bcf3a316c88a309398783c600f7) 
     
    Bug: 494644471 
    Change-Id: I6a29720cd5464d1e7cb04fb0ed51e66d4435c32b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7699593 
    Reviewed-by: Andy Phan <andyphan@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1604965} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7707110 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#1677} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `pdf/pdfium/pdfium_engine.cc`
- M `pdf/pdfium/pdfium_engine.h`
- M `pdf/pdfium/pdfium_engine_unittest.cc`

---

Hash: [6c6c7dd395a1bceafdd762fc9b8546c71686e924](https://chromiumdash.appspot.com/commit/6c6c7dd395a1bceafdd762fc9b8546c71686e924)  

Date: Fri Mar 27 22:00:16 2026


---

### dx...@google.com (2026-03-27)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7708211>

M146: [PDF Ink Signatures] Fix page unloading prevention for shapes

---


Expand for full commit details
```
     
    In PDFiumEngine, `stroked_pages_unload_preventers_` prevents page 
    unloading if a page has strokes or shapes. However, DiscardStroke() only 
    checks for strokes before removing `stroked_pages_unload_preventers_` 
    entries. Add in the missing check for shapes. 
     
    To help DiscardStroke() determine which pages have shapes, repurpose the 
    existing DCHECK-only `pages_with_loaded_v2_ink_paths_` set. Change its 
    semantics so LoadV2InkPathsForPage() only adds to the set when a page 
    has shapes. The sanity check that `pages_with_loaded_v2_ink_paths_` was 
    performing was not very useful anyway. 
     
    (cherry picked from commit 96187fc8ea0e2bcf3a316c88a309398783c600f7) 
     
    Bug: 494644471 
    Change-Id: I6a29720cd5464d1e7cb04fb0ed51e66d4435c32b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7699593 
    Reviewed-by: Andy Phan <andyphan@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1604965} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7708211 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#3361} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `pdf/pdfium/pdfium_engine.cc`
- M `pdf/pdfium/pdfium_engine.h`
- M `pdf/pdfium/pdfium_engine_unittest.cc`

---

Hash: [4bffec53d7021bef7abb07b7fb7679779750dd40](https://chromiumdash.appspot.com/commit/4bffec53d7021bef7abb07b7fb7679779750dd40)  

Date: Fri Mar 27 22:15:21 2026


---

### sp...@google.com (2026-04-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
Baseline with bisect. Mildly mitigated (non-sandboxed) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494644471)*
