# Heap-buffer-overflow in SkPngCodecBase::createColorTable

| Field | Value |
|-------|-------|
| **Issue ID** | [406054655](https://issues.chromium.org/issues/406054655) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Images>Codecs, Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | at...@gmail.com |
| **Assignee** | lu...@google.com |
| **Created** | 2025-03-25 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5267720912175104

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x78a8a0830907
Crash State:
  SkPngCodecBase::createColorTable
  SkPngCodecBase::initializeXforms
  SkPngRustCodec::startDecoding
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=1419302:1419326

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5267720912175104

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Attachments

- basn3p01-based-long2-trns.png (image/png, 365 B)
- basn3p01-based-long-plte.png (image/png, 874 B)
- basn3p01-based-long-trns.png (image/png, 111 B)
- basn3p01-based-ok.png (image/png, 109 B)

## Timeline

### 24...@project.gserviceaccount.com (2025-03-25)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-03-25)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/2fb340acd7b8c24f03ea19782ef11073aba98608 (Roll Fontations, Skrifa to 0.27

List of changes:
https://github.com/googlefonts/fontations/compare/skrifa-v0.26.5...skrifa-v0.27.0

Updated crates:

* read-fonts: 0.25.3 => 0.26.0
* skrifa: 0.26.5 => 0.27.0

Crates vetted for
"safe-to-deploy", "does-not-implement-crypto", "ub-risk-0"

Bug: chromium:40045339
Change-Id: I8b3e59a6f49e8fc158d39639cb935037284e35a7
Cq-Include-Trybots: chromium/try:android-rust-arm32-rel
Cq-Include-Trybots: chromium/try:android-rust-arm64-dbg
Cq-Include-Trybots: chromium/try:android-rust-arm64-rel
Cq-Include-Trybots: chromium/try:linux-rust-x64-dbg
Cq-Include-Trybots: chromium/try:linux-rust-x64-rel
Cq-Include-Trybots: chromium/try:win-rust-x64-dbg
Cq-Include-Trybots: chromium/try:win-rust-x64-rel
Disable-Rts: True
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6248957
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Auto-Submit: Dominik Röttsches <drott@chromium.org>
Commit-Queue: Łukasz Anforowicz <lukasza@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1419317}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### ch...@google.com (2025-03-26)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-03-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2025-03-26)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### lu...@google.com (2025-03-26)

Impact:

- `SkPngRustCodec` is disabled by default, but we are currently running Rust PNG field trials in Canary/Dev/Beta in M135+ (see `finch/gcl_studies/RustyPng.gcl`)
- `SkPngCodecBase::createColorTable` has been present in Chrome for a long time and impacts decoding via `SkPngCodec` and `SkPngRustCodec`. OTOH this issue doesn't seem to be affecting `SkPngCodec`, only `SkPngRustCodec`.

`SkPngCodecBase::createColorTable` has been moved from `SkPngCodec.cpp` into `SkPngCodecBase.cpp` in <http://review.skia.org/c/skia/+/889151> (see new code [here](https://skia-review.googlesource.com/c/skia/+/889151/17/src/codec/SkPngCodecBase.cpp#263) and old code [here](https://skia-review.googlesource.com/c/skia/+/889151/17/src/codec/SkPngCodec.cpp#b274)).

Invalid/unexpected `numColorsWithAlpha` and/or `numColors` can cause issues in the old and new code:

- `numColors` greater than 256 can write-beyond/overflow the stack-allocated `colorTable` (when calling `SkOpts::RGB_to_RGB1` or `SkOpts::RGB_to_BGR1`)
- `numColorsWithAlpha` greater than `numColors` can 1) write-beyond/overflow the stack-allocated `colorTable` and 2) read-beyond/overflow the `palette` data.

This issue is surfacing now, because Rust `png` decoder returns a span/slice to the **whole** payload of a `PLTE` or `tRNS` chunk. In contrast, `libpng` limits the size of the `PLTE` and `tRNS` chunks - see [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libpng/pngset.c;l=575-586;drc=87c3217dc3fec0f441b68f33d339b7f3a707b11d) and [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libpng/pngset.c;l=1004-1013;drc=87c3217dc3fec0f441b68f33d339b7f3a707b11d). I have crafted `basn3p01-based-long-plte.png` (`PLTE` has 257 entries), `basn3p01-based-long-trns.png` (`tRNS` has 3 entries - 1 more than `PLTE`), `basn3p01-based-long2-trns.png` (`tRNS` has 257 entries) and tested 3 PNG decoders that ship in Chromium (`SkPngRustCodec`, `SkPngCodec`, `blink::PNGImageDecoder`) - only `SkPngRustCodec` is affected by this issue.

### lu...@google.com (2025-03-26)

redacted

### ap...@google.com (2025-03-26)

Project: skia  

Branch: main  

Author: Lukasz Anforowicz <[lukasza@chromium.org](mailto:lukasza@chromium.org)>  

Link:      <https://skia-review.googlesource.com/970356>

[rust png] Sanitize the size of `PLTE` and `tRNS` chunks.

---


Expand for full commit details
```
[rust png] Sanitize the size of `PLTE` and `tRNS` chunks. 
 
Bug: chromium:406054655 
Change-Id: I9c3115a463b65e5ae0dab793c0f35d92ed2f5534 
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/970356 
Reviewed-by: Florin Malita <fmalita@google.com> 
Commit-Queue: Łukasz Anforowicz <lukasza@google.com>

```

---

Files:

- M `src/codec/SkPngCodecBase.cpp`

---

Hash: cc84a862695504c7f10253c5a79997928f640b42  

Date:  Wed Mar 26 16:48:11 2025


---

### dx...@google.com (2025-03-26)

Project: chromium/src  

Branch: main  

Author: chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:      <https://chromium-review.googlesource.com/6397670>

Roll Skia from 1d342ecc41fb to cc84a8626955 (2 revisions)

---


Expand for full commit details
```
     
    https://skia.googlesource.com/skia.git/+log/1d342ecc41fb..cc84a8626955 
     
    2025-03-26 lukasza@chromium.org [rust png] Sanitize the size of `PLTE` and `tRNS` chunks. 
    2025-03-26 jvanverth@google.com [graphite] Fix SkBitmap creation in ClipAtlasManager. 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/skia-autoroll 
    Please CC maxhudnell@google.com,skiabot@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in Skia: https://bugs.chromium.org/p/skia/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-android-arm64;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel 
    Cq-Do-Not-Cancel-Tryjobs: true 
    Bug: chromium:406054655 
    Tbr: maxhudnell@google.com 
    Change-Id: I42d628ac7dfa4ab50518d6a763ac721c32653598 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6397670 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1438372}

```

---

Files:

- M `DEPS`
- M `third_party/skia`

---

Hash: c60b0dcb93eb5e5a8a08d35832fff1460defd232  

Date:  Wed Mar 26 20:38:41 2025


---

### lu...@google.com (2025-03-26)

Let's wait until the fix gets released in a Canary and then we can figure out the next steps.  It seems that we are quite late in the M135 release cycle (per https://chromiumdash.appspot.com/schedule the early stable release has already started today - March 26th) so I am not sure if merging the fix to M135 is a feasible option.  And it seems that the alternative of postponing the launch to M136 doesn't have many downsides.  So I think I'll go ahead and start working on a CL to add a new `min_version` requirement to the field trial.

### 24...@project.gserviceaccount.com (2025-03-27)

ClusterFuzz testcase 5267720912175104 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_media&range=1438360:1438380

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2025-03-27)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [135].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### lu...@google.com (2025-03-27)

RE: [#comment13](https://issues.chromium.org/issues/406054655#comment13)

> This is sufficiently serious that it should be merged to beta.

Ack. We can also postpone launching the Rust PNG project to M136.

> But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135.

I think we could follow the process outlined at in [`//chrome/skia/g3doc/user/chrome-skia-cherry-pick.md`](https://g3doc.corp.google.com/chrome/skia/g3doc/user/chrome-skia-cherry-pick.md) to merge <https://skia-review.googlesource.com/c/skia/+/970356>

> Which CLs should be backmerged? (Please include Gerrit links.)

<https://skia-review.googlesource.com/c/skia/+/970356>

> Has this fix been verified on Canary to not pose any stability regressions?

The fix has [been released](https://chromiumdash.appspot.com/commit/c60b0dcb93eb5e5a8a08d35832fff1460defd232) in 136.0.7093.0

> Does this fix pose any potential non-verifiable stability risks?

I don't think so.

> Does this fix pose any known compatibility risks?

No.

> Does it require manual verification by the test team? If so, please describe required testing.

No manual verification required.

> (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

Done.

### pg...@google.com (2025-03-27)

we would backmerge the fix at least for the security respin of M135 on April 8!

giving this at least another day to check canary before approving merges!

### lu...@google.com (2025-03-27)

RE: [#comment15](https://issues.chromium.org/issues/406054655#comment15): @pgrace:

FWIW I have already disabled the field trial on M135, so this bug shouldn't affect M135 anymore: cl/741206000

### pg...@google.com (2025-03-28)

thank you! updating foundin accordingly!

### sp...@google.com (2025-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $9000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process + $2,000 fuzzer bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-03)

Congratulations Atte! Thank you for your past fuzzing contributions that resulted in this report!

### ch...@google.com (2025-04-30)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

- M135, which branched on 2025-03-03 (Chromium branch: 7049, Chromium branch position: 1427262)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove TBD-## from the Merge field and replace it with NA-## (where ## corresponds to the milestone under evaluation). If a merge is necessary, add the requested milestone(s) to the Merge-Request field. If you're not sure, reach out to the relevant release manager (can be found at <https://chromiumdash.appspot.com/schedule>).

To learn more about the merge process, including how to land any required merges, see <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>.

### lu...@google.com (2025-04-30)

RE: TBD-135 / [#comment20](https://issues.chromium.org/issues/406054655#comment20):

As pointed out in [#comment16](https://issues.chromium.org/issues/406054655#comment16) and [#comment17](https://issues.chromium.org/issues/406054655#comment17) this issue does not apply to M135 (the affected code was disabled in M135 using a Finch config).

### ch...@google.com (2025-07-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $7,000 for report of memory corruption in a sandboxed process + $2,000 fuzzer bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/406054655)*
