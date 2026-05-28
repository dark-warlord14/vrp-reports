# Type confusion in inline cache prototype loading with Webassembly object prototype

| Field | Value |
|-------|-------|
| **Issue ID** | [447613211](https://issues.chromium.org/issues/447613211) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m-...@github.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2025-09-26 |
| **Bounty** | $50,000.00 |

## Description

Vulnerability details

When loading properties from prototype, inline cache caches the prototype [property holder](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/ic/accessor-assembler.cc;l=1255;drc=1fb4c56b03b105b03c45627871b15b8933ed8a11) and accesses its properties via optimize handlers. In order to avoid map changes in the prototype which may invalidate assumptions in the optimized handlers, inline cache also stores the [`PrototypeChainValidityCell`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/ic/accessor-assembler.cc;l=1116;drc=1fb4c56b03b105b03c45627871b15b8933ed8a11), which gets invalidated when a map change happens in the prototype chain. The [`GetOrCreatePrototypeChainValidityCell`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/map.cc;l=2426;drc=1fb4c56b03b105b03c45627871b15b8933ed8a11) function calls [`TryGetValidityCellHolderMap`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/map.cc;l=2432;drc=1fb4c56b03b105b03c45627871b15b8933ed8a11), which returns `Map::kNoValidityCellSentinel` when the prototype is not a `JSObject`.

```
bool Map::TryGetValidityCellHolderMap(
    Tagged<Map> map, Isolate* isolate,
    Tagged<Map>* out_validity_cell_holder_map) {
  ...
  if (!IsJSObjectThatCanBeTrackedAsPrototype(maybe_prototype)) {   //<--- returns false if prototype is not a JSObject
    return false;
  }
  *out_validity_cell_holder_map = Cast<JSObject>(maybe_prototype)->map();
  return true;
}
...
Handle<UnionOf<Smi, Cell>> Map::GetOrCreatePrototypeChainValidityCell(
    DirectHandle<Map> map, Isolate* isolate,
    DirectHandle<PrototypeInfo>* out_prototype_info) {
  DirectHandle<Map> validity_cell_holder_map;
  {
    Tagged<Map> holder_map;
    if (!TryGetValidityCellHolderMap(*map, isolate, &holder_map)) {
      // Prototype value is not a JSObject.
      return handle(Map::kNoValidityCellSentinel, isolate);  //<------ returns Map::kNoValidityCellSentinel
    }
  ...

```

This becomes problematic with the custom descriptors proposal in WebAssembly, which allows `Wasm` objects to have prototypes. Consider an object with the following prototype chain:

```
obj ({}) -> wasm_obj -> obj_1 ({a : 1})

```

When accessing the property `a`, the prototype chain will be followed, which then fetches the property `a` from `obj_1`. The prototype `obj_1` is then cached in the inline cache handler, but because `wasm_obj` is not a `JSObject`, the `validity_cell` in the handler is going to be `Map::kNoValidityCellSentinel`, allowing the [prototype validity cell check to be bypassed](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/ic/accessor-assembler.cc;l=1949;drc=1fb4c56b03b105b03c45627871b15b8933ed8a11):

```
TNode<MaybeObject> AccessorAssembler::CheckPrototypeValidityCell(
    TNode<Object> maybe_validity_cell, Label* miss) {
  TVARIABLE(MaybeObject, var_cell_value,
            SmiConstant(Map::kNoValidityCellSentinel));

  Label done(this);
  GotoIf(TaggedEqual(maybe_validity_cell,
                     SmiConstant(Map::kNoValidityCellSentinel)),
         &done);
  ...

```

In particular, any change in the map of `obj_1` will not invalidate the inline cache handler, causing type confusion.

As there is currently an [origin trial](https://developer.chrome.com/origintrials/?hl=uk#/view_trial/619807898716864513) for the Webassembly custom descriptors, anyone can register for the origin trial and host a website that can trigger this bug.

Thank you very much for your help and please let me know if there is anything I can help.

REPRODUCTION CASE

To test locally, run the `poc.js` with the `--experimental-wasm-custom-descriptors` flag and the `--allow-natives-syntax` flag to print out debug message. The flag `--experimental-wasm-custom-descriptors` is only needed for local testing to emulate the origin trial. It should cause an OOB access which then loads an object from outside of the boundary of `proto` (A heap number map in my case).

VERSION
v8 commit d32e674
OS: Ubuntu 24.04 LTS

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?

Reporter credit: Man Yue Mo of GitHub Security Lab

## Attachments

- [wasm-module-builder.js](attachments/wasm-module-builder.js) (text/javascript, 76.5 KB)
- [poc.js](attachments/poc.js) (text/javascript, 1.2 KB)
- [cage_rw.js](attachments/cage_rw.js) (text/javascript, 2.8 KB)
- [poc.js](attachments/poc.js) (text/javascript, 1.2 KB)
- [wasm-module-builder.js](attachments/wasm-module-builder.js) (text/javascript, 76.5 KB)

## Timeline

### aj...@google.com (2025-09-26)

Thanks for the report! Sending to the v8 team for triage and tentatively setting labels.

### aj...@google.com (2025-09-26)

Note: the poc needs both files and I'm not 100% sure how to upload that to CF so I have not done so.

### ch...@google.com (2025-09-27)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-09-27)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### m-...@github.com (2025-09-29)

Please find attached a poc (`cage_rw.js`) that demonstrates arbitrary read and write within the v8 heap sandbox. (It uses offsets specific to the commit d32e674) Also I noticed I've used a wrong include directory in the original poc, please find attached a replacement that has the correct directory (`poc.js`). Thanks.

### is...@chromium.org (2025-09-29)

Thank you for the report!

### dx...@google.com (2025-10-06)

Project: v8/v8  

Branch:  main  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7003558>

[wasm-custom-desc] Fix prototype validity cells

---


Expand for full commit details
```
     
    For prototype chains consisting of interleaved JS and Wasm objects, 
    prototype chain tracking must not bail out at the Wasm objects. 
     
    Fixed: 447613211 
    Change-Id: Ibd1a1ffdc7ba1a7540770eecaa908e66b3450268 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7003558 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102944}

```

---

Files:

- M `src/objects/js-objects.cc`
- M `src/objects/map-inl.h`
- M `src/objects/map.cc`
- M `src/objects/map.h`
- M `src/objects/objects-inl.h`
- M `src/objects/objects.h`
- A `test/mjsunit/regress/wasm/regress-447613211.js`

---

Hash: [55496daf90227fb93311c535922f4b2142eeb72c](https://chromiumdash.appspot.com/commit/55496daf90227fb93311c535922f4b2142eeb72c)  

Date: Mon Oct 6 17:23:36 2025


---

### ch...@google.com (2025-10-07)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M142. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [141, 142].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### jk...@chromium.org (2025-10-07)

#9:

1. <https://chromium-review.googlesource.com/7003558>
2. The fix hasn't made it into a Canary yet. Updates here: <https://chromiumdash.appspot.com/commit/55496daf90227fb93311c535922f4b2142eeb72c>
3. No
4. No
5. No

### ts...@google.com (2025-10-07)

Ok, lets hold off for a few days to get this into canary before considering merges.

### ts...@google.com (2025-10-14)

Fix landed in m143, so lets merge to m142 (14.2) and m141 (14.1), targeting a landing in m141 by Fri 17-Oct. 

### sp...@google.com (2025-10-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.

Rationale for this decision:
High-quality report demonstrating controlled write in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### m-...@github.com (2025-10-15)

Thanks. I'd like to donate the reward please. Thank you very much.

### dx...@google.com (2025-10-16)

Project: v8/v8  

Branch:  refs/branch-heads/14.2  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7046403>

Merged: [wasm-custom-desc] Fix prototype validity cells

---


Expand for full commit details
```
     
    For prototype chains consisting of interleaved JS and Wasm objects, 
    prototype chain tracking must not bail out at the Wasm objects. 
     
    Fixed: 447613211 
    (cherry picked from commit 55496daf90227fb93311c535922f4b2142eeb72c) 
     
    Change-Id: I8fced9c8520cddb6c1aad1f23fdf96eec3907ed2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7046403 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.2@{#13} 
    Cr-Branched-From: 37f82dbb9f640dc5eea09870dd391cd3712546e5-refs/heads/14.2.231@{#1} 
    Cr-Branched-From: d1a6089b861336cf4b3887edfd3fdd280b23b5dd-refs/heads/main@{#102804}

```

---

Files:

- M `src/objects/js-objects.cc`
- M `src/objects/map-inl.h`
- M `src/objects/map.cc`
- M `src/objects/map.h`
- M `src/objects/objects-inl.h`
- M `src/objects/objects.h`
- A `test/mjsunit/regress/wasm/regress-447613211.js`

---

Hash: [feda30af94b4a39c0f9e34349a12a78192657f99](https://chromiumdash.appspot.com/commit/feda30af94b4a39c0f9e34349a12a78192657f99)  

Date: Mon Oct 6 17:23:36 2025


---

### pe...@google.com (2025-10-16)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### jk...@chromium.org (2025-10-16)

Turns out we don't need the merge to M141: on that milestone, it's impossible to create the circumstances for triggering the bug, even with the Custom Descriptors Origin Trial. (More details: as of the state of the proposal that we implemented back then, creating a Wasm object with a non-null prototype required wrapping that prototype into a `WebAssembly.DescriptorOptions` object, and the constructor for that object is hidden behind `--experimental-wasm-js-interop`, which is not enabled by the OT.)

#16: Nope, a merge to M138 isn't required either.

### qk...@google.com (2025-10-17)

Labelling as not applicable for M138-LTS, the issue doesn't occur in M138. See comment #17.

### ch...@google.com (2025-12-10)

WARNING: Removing security\_release value because the issue is not on security\_impact-stable or security\_impact-extended hotlists. Please add to the correct hotlist if the issue is on a release branch.

### ch...@google.com (2026-01-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/447613211)*
