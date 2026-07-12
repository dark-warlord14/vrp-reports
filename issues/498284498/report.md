# OOB and UAF in pdfium lcms

| Field | Value |
|-------|-------|
| **Issue ID** | [498284498](https://issues.chromium.org/issues/498284498) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ts...@google.com |
| **Created** | 2026-03-31 |
| **Bounty** | $7,000.00 |

## Description

### Summary

In lcms, [cmsStageAllocCLut16bitGranular() / cmsStageAllocCLutFloatGranular()](https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/third_party/lcms/src/cmslut.c;l=561) compute `outputChan * CubeSize(clutPoints, inputChan)` in `cmsUInt32Number` without checking the caller-side multiplication. The crafted CLUT dimensions can make the multiplication wrap, allocate a tiny CLUT, leading to the heap-buffer-overflow.

### Details

`CPDF_ICCBasedCS::v_Load` validates `/N` and then asks `CPDF_DocPageData` for an ICC profile. `CPDF_IccProfile` immediately constructs an lcms-backed transform from the stream bytes. That means a malformed ICC stream reaches lcms during colorspace loading, before page rendering has a chance to reject or sanitize the profile.

The untrusted ICC bytes are handed to lcms from [CPDF\_IccProfile::CPDF\_IccProfile](https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/core/fpdfapi/page/cpdf_iccprofile.cpp;l=24):

```
auto transform =
    fxcodec::IccTransform::CreateTransformSRGB(stream_acc_->GetSpan());
if (!transform) {
  return;
}

uint32_t components = transform->components();
if (components != expected_components) {
  return;
}

src_components_ = components;
transform_ = std::move(transform);

```

`CubeSize()` rejects only internal overflow in the dimension product, but the caller still multiplies that product by `outputChan` in 32 bits. With the crafted CLUT dimensions, `CubeSize(clutPoints, inputChan)` stays below `UINT_MAX`, yet `outputChan * CubeSize()` wraps to a tiny `nEntries`. lcms therefore allocates a much smaller CLUT than the interpolation parameters describe.

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/third_party/lcms/src/cmslut.c;l=666>

```
    // There is a potential integer overflow on conputing n and nEntries.
    NewElem -> nEntries = n = outputChan * CubeSize(clutPoints, inputChan);
    NewElem -> HasFloatValues = TRUE;

    if (n == 0) {
        cmsStageFree(NewMPE);
        return NULL;
    }

    NewElem ->Tab.TFloat  = (cmsFloat32Number*) _cmsCalloc(ContextID, n, sizeof(cmsFloat32Number));

```

Therefore, the out-of-bounds access happens immediately during [cmsCreateExtendedTransform](https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/third_party/lcms/src/cmsxform.c;l=1237).

### Reproduction

Host the pdf file using `python3 -m http.server 8080`

Simply load the POC pdf file to the chromium (e.g., `https://storage.googleapis.com/chromium-browser-asan/mac-release-arm64/asan-mac-release-1607812.zip`)

Running with

```
./asan-mac-release-1607812/Chromium.app/Contents/MacOS/Chromium --no-sandbox http://localhost:8080/poc.pdf

```

You would observe the OOB shown in `asan.txt`.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 28.7 KB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 840 B)
- [symbolized_stacktrace.txt](attachments/symbolized_stacktrace.txt) (text/plain, 11.1 KB)
- [asan_uaf.txt](attachments/asan_uaf.txt) (text/plain, 27.4 KB)
- [uaf_poc.pdf](attachments/uaf_poc.pdf) (application/pdf, 15.8 KB)

## Timeline

### ja...@google.com (2026-03-31)

[security triage]
I reproduced this on Linux using Canary. I'm working on getting a symbolized asan trace.

### ja...@google.com (2026-03-31)

Reproduced using 148.0.7764.0

### ja...@google.com (2026-03-31)

[security triage]
Setting severity to medium for "An out-of-bounds read in a renderer process". See: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md#toc-medium-severity>

### ja...@google.com (2026-03-31)

This didn't reproduce in beta (147)

### ja...@google.com (2026-03-31)

Also not in Dev 148.0.7753.0

### ja...@google.com (2026-03-31)

Choosing an owner to take a look. Would you mind taking a look?

### ts...@google.com (2026-04-01)

I can take this.

### ch...@google.com (2026-04-01)

Setting milestone because of s2 severity.

### ch...@google.com (2026-04-01)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2026-04-01)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ts...@google.com (2026-04-01)

Reporter: this should likely be reported upstream to lcms as well.  We're going to patch it in chrome, but they should know as well.

Javier:  Curious that this didn't reproduce in some versions. I'd expect this to be unchanged for a long time, so probably not a regression.

### he...@gmail.com (2026-04-01)

Thank you very much for the pending fix. I'll also report to the upstream.

I also craft another POC pdf which can trigger the UAF crash which can further increase the severity on the current unfixed version.

After the CL 145650 landed, I'll verify against the ToT build.

Many Thanks!

### ts...@google.com (2026-04-01)

Yep. I tested my forthcoming patch against the Uaf, and it reproduced before the patch, but not after (I put a couple of additional overflow tests into it that I found by inspection).  See  https://pdfium-review.googlesource.com/c/pdfium/+/145650 

I updated the report title to reflect the more serious category than just the OOB read.

### dx...@google.com (2026-04-01)

Project: pdfium  

Branch:  main  

Author:  Tom Sepez [tsepez@google.com](mailto:tsepez@google.com)  

Link:    <https://pdfium-review.googlesource.com/145650>

Add additional overflow checks to LCMS.

---


Expand for full commit details
```
     
    Fix instance in linked bug, plus several variants noticed by 
    inspection. 
     
    Bug: 498284498 
    Change-Id: Ica659b2c484e4b25f2201e57a8ceeb6403ed85cd 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145650 
    Commit-Queue: Tom Sepez <tsepez@chromium.org> 
    Reviewed-by: Nicolás Peña <npm@chromium.org>

```

---

Files:

- A `third_party/lcms/0037-theoretical-overflow.patch`
- M `third_party/lcms/README.pdfium`
- M `third_party/lcms/src/cmscgats.c`
- M `third_party/lcms/src/cmslut.c`
- M `third_party/lcms/src/cmsnamed.c`
- M `third_party/lcms/src/cmstypes.c`

---

Hash: 79d84a59fb337f5ae4c1c9fee60677c29a310f46  

Date: Wed Apr 1 19:10:23 2026


---

### dx...@google.com (2026-04-01)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7722366>

Roll PDFium from fefe0007f317 to 79d84a59fb33 (1 revision)

---


Expand for full commit details
```
     
    https://pdfium.googlesource.com/pdfium.git/+log/fefe0007f317..79d84a59fb33 
     
    2026-04-01 tsepez@google.com Add additional overflow checks to LCMS. 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/pdfium-autoroll 
    Please CC dhoss@chromium.org,thestig@chromium.org,thestig@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:498284498 
    Tbr: thestig@google.com 
    Change-Id: I032f003018bcfa525638475aeea552ac6e429000 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7722366 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1608820}

```

---

Files:

- M `DEPS`
- M `third_party/pdfium`

---

Hash: [76e186e0069755d70447fd6f00f37eeaebd414a8](https://chromiumdash.appspot.com/commit/76e186e0069755d70447fd6f00f37eeaebd414a8)  

Date: Wed Apr 1 22:33:22 2026


---

### he...@gmail.com (2026-04-05)

Thank you for the fix. I've report this issue to the upstream as well in <https://github.com/mm2/Little-CMS/security/advisories/GHSA-25p2-vjmh-4245> and I am waiting for the upstream maintainer's reply. Thank you very much!

### he...@gmail.com (2026-04-22)

Update about the upstream repo: the upstream maintainer has applied the similar check and patched on its lcms.

Thank you very much.

### aj...@google.com (2026-06-18)

-> High as this is a uaf in the renderer (comment 14)

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
High Quality. Renderer UAF.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/498284498)*
