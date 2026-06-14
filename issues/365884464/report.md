# out of bound write in skia  DrawAtlasOpImpl::DrawAtlasOpImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [365884464](https://issues.chromium.org/issues/365884464) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 128.0.0.0 |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ja...@google.com |
| **Created** | 2024-09-11 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. build skia skpbench
2. out/asan/skpbench --src output.skp --config gl
3. you will see

```
raven@192 ~/w/s/skia (main)> out/asan/skpbench --src output.skp --config gl
   accum    median       max       min   stddev  samples  sample_ms  clock  metric  config    bench
alloc_size------>>-2147483616
../../src/gpu/ganesh/ops/DrawAtlasOp.cpp:191:53: runtime error: applying non-zero offset 8 to null pointer
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior ../../src/gpu/ganesh/ops/DrawAtlasOp.cpp:191:53 in 
fish: Job 1, 'out/asan/skpbench --src output.…' terminated by signal SIGABRT (Abort)
``

# Problem Description
above all

# Summary
out of bound write in skia  DrawAtlasOpImpl::DrawAtlasOpImpl

# Additional Data
Category: Security \
Chrome Channel: Not sure \
Regression: N/A

```

## Attachments

- [output.skp](attachments/output.skp) (application/x-koan, 921.6 MB)

## Timeline

### wx...@gmail.com (2024-09-11)

```
DrawAtlasOpImpl::DrawAtlasOpImpl(GrProcessorSet* processorSet, const SkPMColor4f& color,
                                 const SkMatrix& viewMatrix, GrAAType aaType, int spriteCount,
                                 const SkRSXform* xforms, const SkRect* rects,
                                 const SkColor* colors)
        : GrMeshDrawOp(ClassID()), fHelper(processorSet, aaType), fColor(color) {
    SkASSERT(xforms);
    SkASSERT(rects);

    fViewMatrix = viewMatrix;
    Geometry& installedGeo = fGeoData.push_back();
    installedGeo.fColor = color;

    // Figure out stride and offsets
    // Order within the vertex is: position [color] texCoord
    size_t texOffset = sizeof(SkPoint);
    size_t vertexStride = 2 * sizeof(SkPoint);
    fHasColors = SkToBool(colors);
    if (colors) {
        texOffset += sizeof(GrColor);
        vertexStride += sizeof(GrColor);
    }

    // Compute buffer size and alloc buffer
    fQuadCount = spriteCount;
    int allocSize = static_cast<int>(4 * vertexStride * spriteCount);    ---->>here will be a negative number.
    installedGeo.fVerts.reset(allocSize);
    uint8_t* currVertex = installedGeo.fVerts.begin();

    SkRect bounds = SkRectPriv::MakeLargestInverted();
    // TODO4F: Preserve float colors
    int paintAlpha = GrColorUnpackA(installedGeo.fColor.toBytes_RGBA());
    for (int spriteIndex = 0; spriteIndex < spriteCount; ++spriteIndex) {
        // Transform rect
        SkPoint strip[4];
        const SkRect& currRect = rects[spriteIndex];
        xforms[spriteIndex].toTriStrip(currRect.width(), currRect.height(), strip);

        // Copy colors if necessary
        if (colors) {
            // convert to GrColor
            SkColor spriteColor = colors[spriteIndex];
            if (paintAlpha != 255) {
                spriteColor = SkColorSetA(spriteColor,
                                          SkMulDiv255Round(SkColorGetA(spriteColor), paintAlpha));
            }
            GrColor grColor = SkColorToPremulGrColor(spriteColor);

            *(reinterpret_cast<GrColor*>(currVertex + sizeof(SkPoint))) = grColor; --->>>>>>>>>>>>>>>>>>here will cause out of bound write.

```

### wx...@gmail.com (2024-09-11)

we can control spriteCount, so that we could write 4GB data.

```
    for (int spriteIndex = 0; spriteIndex < spriteCount; ++spriteIndex) {  
        // Transform rect
        SkPoint strip[4];
        const SkRect& currRect = rects[spriteIndex];
        xforms[spriteIndex].toTriStrip(currRect.width(), currRect.height(), strip);

        // Copy colors if necessary
        if (colors) {
            // convert to GrColor
            SkColor spriteColor = colors[spriteIndex];
            if (paintAlpha != 255) {
                spriteColor = SkColorSetA(spriteColor,
                                          SkMulDiv255Round(SkColorGetA(spriteColor), paintAlpha));
            }
            GrColor grColor = SkColorToPremulGrColor(spriteColor);

            *(reinterpret_cast<GrColor*>(currVertex + sizeof(SkPoint))) = grColor;
            *(reinterpret_cast<GrColor*>(currVertex + vertexStride + sizeof(SkPoint))) = grColor;
            *(reinterpret_cast<GrColor*>(currVertex + 2 * vertexStride + sizeof(SkPoint))) =
                    grColor;
            *(reinterpret_cast<GrColor*>(currVertex + 3 * vertexStride + sizeof(SkPoint))) =
                    grColor;
        }

        // Copy position and uv to verts
        *(reinterpret_cast<SkPoint*>(currVertex)) = strip[0];
        *(reinterpret_cast<SkPoint*>(currVertex + texOffset)) =
                SkPoint::Make(currRect.fLeft, currRect.fTop);
        SkRectPriv::GrowToInclude(&bounds, strip[0]);
        currVertex += vertexStride;

        *(reinterpret_cast<SkPoint*>(currVertex)) = strip[1];
        *(reinterpret_cast<SkPoint*>(currVertex + texOffset)) =
                SkPoint::Make(currRect.fLeft, currRect.fBottom);
        SkRectPriv::GrowToInclude(&bounds, strip[1]);
        currVertex += vertexStride;

        *(reinterpret_cast<SkPoint*>(currVertex)) = strip[2];
        *(reinterpret_cast<SkPoint*>(currVertex + texOffset)) =
                SkPoint::Make(currRect.fRight, currRect.fTop);
        SkRectPriv::GrowToInclude(&bounds, strip[2]);
        currVertex += vertexStride;

        *(reinterpret_cast<SkPoint*>(currVertex)) = strip[3];
        *(reinterpret_cast<SkPoint*>(currVertex + texOffset)) =
                SkPoint::Make(currRect.fRight, currRect.fBottom);
        SkRectPriv::GrowToInclude(&bounds, strip[3]);
        currVertex += vertexStride;
    }

```

### an...@chromium.org (2024-09-11)

Thanks for the report! Assigning S1 due to memory corruption in the GPU process. Note I haven't reproduced this issue since the information looks plausible. Set FoundIn as 128 (latest stable).

### pe...@google.com (2024-09-11)

Setting milestone because of s0/s1 severity.

### ap...@google.com (2024-09-12)

Project: skia
Branch: main

commit 2b40b50ea423e11073b742b3bd785975a6019046
Author: James Godfrey-Kittle <jamesgk@google.com>
Date:   Wed Sep 11 16:18:40 2024

    [ganesh] Avoid int overflow in DrawAtlasOpImpl
    
    Bug: b/365884464
    Change-Id: I4dc9f259165c88c1d7ae5dc38c6cae02ca18f509
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/898756
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>
    Reviewed-by: Brian Osman <brianosman@google.com>

M       src/gpu/ganesh/ops/DrawAtlasOp.cpp

https://skia-review.googlesource.com/898756


### wx...@gmail.com (2024-09-13)

LGTM

### pe...@google.com (2024-09-18)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128, 129, 130].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ja...@google.com (2024-09-18)

1. <http://review.skia.org/898756>
2. This fix has been in Canary since 130.0.6715.0 on Windows, Mac and Android, and has not caused any stability regressions
3. No
4. No
5. No

### am...@chromium.org (2024-09-18)

Please merge this fix to branch M129 / branch 6668 and M128 / branch 6613 by EOD Thursday, 19 September so this fix can be included in the next Stable and Extended Stable updates -- thank you

### ap...@google.com (2024-09-18)

Project: skia
Branch: chrome/m128

commit cd98397d0c2c3eb1d5a8d76aade3c87c2e0d28ac
Author: James Godfrey-Kittle <jamesgk@google.com>
Date:   Wed Sep 11 16:18:40 2024

    [ganesh] Avoid int overflow in DrawAtlasOpImpl
    
    Bug: b/365884464
    Change-Id: I4dc9f259165c88c1d7ae5dc38c6cae02ca18f509
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/898756
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>
    Reviewed-by: Brian Osman <brianosman@google.com>
    (cherry picked from commit 2b40b50ea423e11073b742b3bd785975a6019046)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/901176
    Reviewed-by: Michael Ludwig <michaelludwig@google.com>

M       src/gpu/ganesh/ops/DrawAtlasOp.cpp

https://skia-review.googlesource.com/901176


### ap...@google.com (2024-09-18)

Project: skia
Branch: chrome/m129

commit dda581d538cb6532cda841444e7b4ceacde01ec9
Author: James Godfrey-Kittle <jamesgk@google.com>
Date:   Wed Sep 11 16:18:40 2024

    [ganesh] Avoid int overflow in DrawAtlasOpImpl
    
    Bug: b/365884464
    Change-Id: I4dc9f259165c88c1d7ae5dc38c6cae02ca18f509
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/898756
    Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>
    Reviewed-by: Brian Osman <brianosman@google.com>
    (cherry picked from commit 2b40b50ea423e11073b742b3bd785975a6019046)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/901177
    Reviewed-by: Michael Ludwig <michaelludwig@google.com>

M       src/gpu/ganesh/ops/DrawAtlasOp.cpp

https://skia-review.googlesource.com/901177


### pe...@google.com (2024-09-18)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ja...@google.com (2024-09-18)

1. No
2. No

### pe...@google.com (2024-09-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-09-21)

1. https://skia-review.googlesource.com/c/skia/+/901496 for 126
2. Low, No merge conflict.
3. 128 and 129
4. Yes


### ts...@google.com (2024-09-26)

Skia should strongly consider updating the debug-only SkAsserts for negative size parameters in TArray::reset() to a full-up CHECK() as the cost of the branch is likely cheap compared to the subsequent reallocations.

### ap...@google.com (2024-09-30)

Project: skia  

Branch: chrome/m126  

Author: James Godfrey-Kittle <[jamesgk@google.com](mailto:jamesgk@google.com)>  

Link:      <https://skia-review.googlesource.com/901496>

[M126-LTS][ganesh] Avoid int overflow in DrawAtlasOpImpl

---


Expand for full commit details
```
[M126-LTS][ganesh] Avoid int overflow in DrawAtlasOpImpl

Bug: b/365884464
Change-Id: I4dc9f259165c88c1d7ae5dc38c6cae02ca18f509
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/898756
Commit-Queue: James Godfrey-Kittle <jamesgk@google.com>
Reviewed-by: Brian Osman <brianosman@google.com>
(cherry picked from commit 2b40b50ea423e11073b742b3bd785975a6019046)
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/901177
Reviewed-by: Michael Ludwig <michaelludwig@google.com>
(cherry picked from commit dda581d538cb6532cda841444e7b4ceacde01ec9)
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/901496
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com>
Reviewed-by: James Godfrey-Kittle <jamesgk@google.com>

```

---

Files:

- M `src/gpu/ganesh/ops/DrawAtlasOp.cpp`

---

Hash: 234e3d4b37e9d398016018ae64c6059ae7eb9559  

Date:  Wed Sep 11 16:18:40 2024


---

### sp...@google.com (2024-09-30)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of speculative / theoretical integer overflow / memory corruption in the GPU process (no demonstrated memory corruption)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-30)

Congratulations! Since this was a report of a speculative issue and write or other memory corruption was not demonstrated, this report is only eligible for a lesser reward amount. Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-12-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/365884464)*
