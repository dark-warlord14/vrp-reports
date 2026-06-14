# WebGLContext.getContextAttributes() triggers resource leak on page reload

| Field | Value |
|-------|-------|
| **Issue ID** | [333182464](https://issues.chromium.org/issues/333182464) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API |
| **Platforms** | Linux |
| **Chrome Version** | 123.0.6312.105 |
| **Reporter** | ei...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2024-04-08 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Open this file in a new tab:

```
<!DOCTYPE html>
<html lang="en">
<body>
    <canvas id="canvas"></canvas>
    <script>
        const resource = new Uint8Array(100000000).fill(42);
        const attributes = canvas.getContext('webgl2').getContextAttributes();
    </script>
</body>
</html>

```

2. Use Dev Tools to capture a heap snapshot. This will be about 100MB in size
3. Reload the page
4. Capture another heap snapshot. This will be about 200MB. Triggering GC with the "Collect garbage"-button does not affect this. Subsequent reloads will not cause a larger heap than this.

# Problem Description

I've been investigating a resource leak in a large WebGL application that seems to happen when you reload the page, I've found a minimal way to reproduce the issue. For some reason, if I call getContextAttributes() the resources won't be cleaned up on a page reload.

The resources are cleaned up correctly on 122.0.6261.128, so this seems to be a regression.

I'm running Ubuntu 22.04 (6.5.0-26-generic). Since this seems to be WebGL related I've tried both OpenGL and Vulkan angle backends, and both are affected.

# Summary

WebGLContext.getContextAttributes() triggers resource leak on page reload

# Additional Data

Category: JavaScript   

Chrome Channel: Stable   

Regression: Yes

## Attachments

- [Heap-Snapshot-100MB.heapsnapshot](attachments/Heap-Snapshot-100MB.heapsnapshot) (application/octet-stream, 2.2 MB)
- [Heap-Snapshot-200MB.heapsnapshot](attachments/Heap-Snapshot-200MB.heapsnapshot) (application/octet-stream, 2.8 MB)

## Timeline

### de...@google.com (2024-04-09)

Labels: Needs-Triage-M123

### kb...@chromium.org (2024-04-10)

I can see the reported problem but it seems impossible to me that a WebGL change could have caused a behavioral difference in this area. It sounds like the entire past JavaScript context is still reachable for some reason.

Here are 2 heap snapshots. I don't know how to tell what if anything is the retaining root of the Uint8Array's backing store. Could I please ask the V8 GC folks to look at this and advise?

### ml...@chromium.org (2024-04-10)

I think this is actually a security issue. We leak and expose the V8 context through some caching artifact here.

Technical details:

1. `v8::internal::DictionaryTemplateInfo` is used to create dictionary templates.
2. The template caches the map to speed up dictionary creation
3. The map is per context
4. Templates are per Isolates
5. This mixes contexts in scenarios where cross-origin iframes are used (e.g. some Android configurations).

It also manifests as a leak here in the sense that we always leak 1 context (the first one to use the template) which holds the array in the repro.

### pe...@google.com (2024-04-10)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### kb...@chromium.org (2024-04-10)

Thank you so much Michael for tracking this down. It sounds like this regressed in some recent release, so if you can link this to any related bug and/or bisect it too, that would be appreciated.

### ml...@chromium.org (2024-04-10)

Good point, this likely regressed when switching to using new `DictionaryTemplate`s on V8's API in M123.

<https://chromiumdash.appspot.com/commit/eacca1b20cb0e8e55381482c1183f79702fab218>

Fix is on the way here: <https://chromium-review.googlesource.com/c/v8/v8/+/5443270>

### ap...@google.com (2024-04-10)

Project: v8/v8
Branch: main

commit 819f64c6c4705c21252ea8411a81d0b19a32337f
Author: Michael Lippautz <mlippautz@chromium.org>
Date:   Wed Apr 10 20:46:07 2024

    [api] Fix instantiation of DictionaryTemplate across contexts
    
    The current version would allow instantiating the same template (which
    is per Isolate) across various contexts without creating the proper
    new map transitions. Map::Copy() was not sufficient to handle this
    case.
    
    Instead, rely on the already existing template instantiations cache
    which is context specific.
    
    Bug: chromium:333182464
    Change-Id: I44f76ca120ba24a3f17d50f6307c83d9734a9c08
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5443270
    Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#93304}

M       src/api/api-natives.cc
M       src/heap/factory.cc
M       src/objects/templates-inl.h
M       src/objects/templates.cc
M       src/objects/templates.h
M       src/objects/templates.tq

https://chromium-review.googlesource.com/5443270


### kb...@chromium.org (2024-04-10)

Thank you Michael - you're a champ! I linked this bug to the one from <https://chromiumdash.appspot.com/commit/eacca1b20cb0e8e55381482c1183f79702fab218> .

Release managers will want to know whether your fix should be backported - could you offer your opinion?

### ap...@google.com (2024-04-10)

Project: v8/v8
Branch: main

commit 3ec395eaf15633a40add571e9183dfec0d0bc29a
Author: Deepti Gandluri <gdeepti@chromium.org>
Date:   Wed Apr 10 22:00:34 2024

    Revert "[api] Fix instantiation of DictionaryTemplate across contexts"
    
    This reverts commit 819f64c6c4705c21252ea8411a81d0b19a32337f.
    
    Reason for revert: Causes fails on the blink-wpt bot: https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Blink%20Linux/30216/overview
    
    Original change's description:
    > [api] Fix instantiation of DictionaryTemplate across contexts
    >
    > The current version would allow instantiating the same template (which
    > is per Isolate) across various contexts without creating the proper
    > new map transitions. Map::Copy() was not sufficient to handle this
    > case.
    >
    > Instead, rely on the already existing template instantiations cache
    > which is context specific.
    >
    > Bug: chromium:333182464
    > Change-Id: I44f76ca120ba24a3f17d50f6307c83d9734a9c08
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5443270
    > Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    > Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#93304}
    
    Bug: chromium:333182464
    Change-Id: I0af35fdc2bcc6e9b143273aae8f429c23bca650c
    No-Presubmit: true
    No-Tree-Checks: true
    No-Try: true
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5445569
    Auto-Submit: Deepti Gandluri <gdeepti@chromium.org>
    Owners-Override: Deepti Gandluri <gdeepti@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#93305}

M       src/api/api-natives.cc
M       src/heap/factory.cc
M       src/objects/templates-inl.h
M       src/objects/templates.cc
M       src/objects/templates.h
M       src/objects/templates.tq

https://chromium-review.googlesource.com/5445569


### ap...@google.com (2024-04-11)

Project: chromium/src
Branch: main

commit 1ebb0bf299402ded80617f455114fa8687a7cb50
Author: Michael Lippautz <mlippautz@chromium.org>
Date:   Thu Apr 11 07:00:10 2024

    Skip test until V8 has rolled
    
    The test was marked as pass based on a bug where a map would leak across
    contexts.
    
    The test needs to be rebaselined after rolling V8.
    
    Bug: chromium:333182464
    Change-Id: I009faff70099885ae539fa28bf1e8e006eed3312
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5446264
    Auto-Submit: Michael Lippautz <mlippautz@chromium.org>
    Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1285641}

M       third_party/blink/web_tests/TestExpectations

https://chromium-review.googlesource.com/5446264


### ml...@chromium.org (2024-04-11)

I think this is S1 as it allows XSS when running without site isolation. With site isolation we shouldn't have any issue here.

### ap...@google.com (2024-04-11)

Project: v8/v8
Branch: main

commit b505dbee47b2d718fad79aec7dd3ee440db28b37
Author: Michael Lippautz <mlippautz@chromium.org>
Date:   Wed Apr 10 20:46:07 2024

    Reland "[api] Fix instantiation of DictionaryTemplate across contexts"
    
    This is a reland of commit 819f64c6c4705c21252ea8411a81d0b19a32337f
    
    CL is unchanged. Blink needs rebaselining here.
    
    Original change's description:
    > [api] Fix instantiation of DictionaryTemplate across contexts
    >
    > The current version would allow instantiating the same template (which
    > is per Isolate) across various contexts without creating the proper
    > new map transitions. Map::Copy() was not sufficient to handle this
    > case.
    >
    > Instead, rely on the already existing template instantiations cache
    > which is context specific.
    >
    > Bug: chromium:333182464
    > Change-Id: I44f76ca120ba24a3f17d50f6307c83d9734a9c08
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5443270
    > Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    > Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#93304}
    
    Bug: chromium:333182464
    Change-Id: Icc2606f110505a77852fe9a49ab94a28ea515a3b
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5446983
    Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#93308}

M       src/api/api-natives.cc
M       src/heap/factory.cc
M       src/objects/templates-inl.h
M       src/objects/templates.cc
M       src/objects/templates.h
M       src/objects/templates.tq

https://chromium-review.googlesource.com/5446983


### ap...@google.com (2024-04-11)

Project: chromium/src
Branch: main

commit d5619ec1fa353f3068718ce9df54fc885340f3bd
Author: Michael Lippautz <mlippautz@chromium.org>
Date:   Thu Apr 11 10:57:30 2024

    Fix test expectation
    
    No-try: true
    Bug: chromium:333182464
    Change-Id: I1af237fe79ddeef064b340240720f78e462c83b8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5447010
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1285731}

M       third_party/blink/web_tests/TestExpectations

https://chromium-review.googlesource.com/5447010


### pe...@google.com (2024-04-11)

Setting milestone because of s0/s1 severity.

### ap...@google.com (2024-04-12)

Project: chromium/src
Branch: main

commit 57a8715f7ff27e66cea1c88b47c1484eee87a814
Author: Michael Lippautz <mlippautz@chromium.org>
Date:   Fri Apr 12 14:09:37 2024

    Rebaseline test after V8 roll
    
    Adjust test expectations after landing the fix for DictionaryTemplate.
    
    Bug: chromium:333182464
    Change-Id: I4750e70780fdf0ee30aa7d35af22deb5d9ae19bf
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5447540
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Auto-Submit: Michael Lippautz <mlippautz@chromium.org>
    Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1286462}

M       third_party/blink/web_tests/TestExpectations
M       third_party/blink/web_tests/external/wpt/streams/readable-streams/global-expected.txt

https://chromium-review.googlesource.com/5447540


### pe...@google.com (2024-04-15)

Requesting merge to stable (M123) because latest trunk commit (1286462) appears to be after stable branch point (1262506).
Requesting merge to beta (M124) because latest trunk commit (1286462) appears to be after beta branch point (1274542).
Merge review required: a reverted commit was detected after the merge request.


Merge review required: a reverted commit was detected after the merge request.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [123, 124].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### ml...@chromium.org (2024-04-15)

> 1. Which CLs should be backmerged? (Please include Gerrit links.)

Fix: <https://chromium-review.googlesource.com/c/v8/v8/+/5446983>

Possibly also the Blink CLs, to disable the tests:

- <https://chromium-review.googlesource.com/c/chromium/src/+/5446264>
- <https://chromium-review.googlesource.com/c/chromium/src/+/5447010>

The test disable would need to land before V8 rolls with the fix.

> 2. Has this fix been verified on Canary to not pose any stability regressions?

The fix is on Canary; no known issues.

> 3. Does this fix pose any potential non-verifiable stability risks?

The fix is in V8 and actually requires Blink CLs that change test expectations to pass Blink web tests.

Depending on whether these are running, this could cause issues.

> 4. Does this fix pose any known compatibility risks?

See 3. Merging the test expectations could be tricky.

> 5. Does it require manual verification by the test team? If so, please describe required testing.

There's no additional testing required.

### pe...@google.com (2024-04-16)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=333182464&entry.958145677=Linux&entry.763880440=Stable&entry.1678852700=High&entry.763402679=Blink>JavaScript>API&entry.975983575=mlippautz@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

### am...@chromium.org (2024-04-18)

merges approved to disable the tests:
<https://crrev.com/c/5446264>
<https://crrev.com/c/5447010>

and for the fix: <https://crrev.com/c/5446983>
please merge to M124 (branch 12.4 for V8 / branch 6367 for disabling blink tests) at your earliest convenience before 10am Pacific tomorrow (Friday, 19 April)

### ap...@google.com (2024-04-18)

Project: chromium/src
Branch: refs/branch-heads/6367

commit d946dac5082e0e7af609399f96b353998df394fd
Author: Michael Lippautz <mlippautz@chromium.org>
Date:   Thu Apr 18 18:24:02 2024

    Disable test to allow backmerging V8 fix
    
    The test returns the wrong result after V8 is fixed. Disable the test.
    
    (cherry picked from commit 1ebb0bf299402ded80617f455114fa8687a7cb50)
    (cherry picked from commit d5619ec1fa353f3068718ce9df54fc885340f3bd)
    
    Bug: chromium:333182464
    Change-Id: I40437327f24cf30751af83635513480e2f847399
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5465849
    Auto-Submit: Michael Lippautz <mlippautz@chromium.org>
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
    Reviewed-by: Shu-yu Guo <syg@chromium.org>
    Commit-Queue: Shu-yu Guo <syg@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6367@{#915}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       third_party/blink/web_tests/TestExpectations

https://chromium-review.googlesource.com/5465849


### ap...@google.com (2024-04-18)

Project: v8/v8
Branch: refs/branch-heads/12.4

commit 309fa00f7a4778d2fb6417e21c5c8985cf5d5136
Author: Michael Lippautz <mlippautz@chromium.org>
Date:   Wed Apr 10 20:46:07 2024

    Merged: Reland "[api] Fix instantiation of DictionaryTemplate across contexts"
    
    This is a reland of commit 819f64c6c4705c21252ea8411a81d0b19a32337f
    
    CL is unchanged. Blink needs rebaselining here.
    
    Original change's description:
    > [api] Fix instantiation of DictionaryTemplate across contexts
    >
    > The current version would allow instantiating the same template (which
    > is per Isolate) across various contexts without creating the proper
    > new map transitions. Map::Copy() was not sufficient to handle this
    > case.
    >
    > Instead, rely on the already existing template instantiations cache
    > which is context specific.
    >
    > Bug: chromium:333182464
    > Change-Id: I44f76ca120ba24a3f17d50f6307c83d9734a9c08
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5443270
    > Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    > Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#93304}
    
    (cherry picked from commit b505dbee47b2d718fad79aec7dd3ee440db28b37)
    
    Bug: chromium:333182464
    Change-Id: Iab273403a0b645ae5b8d501a93202fed904ccd44
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5463594
    Reviewed-by: Shu-yu Guo <syg@chromium.org>
    Commit-Queue: Shu-yu Guo <syg@chromium.org>
    Auto-Submit: Michael Lippautz <mlippautz@chromium.org>
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.4@{#26}
    Cr-Branched-From: 309640da62fae0485c7e4f64829627c92d53b35d-refs/heads/12.4.254@{#1}
    Cr-Branched-From: 5dc24701432278556a9829d27c532f974643e6df-refs/heads/main@{#92862}

M       src/api/api-natives.cc
M       src/heap/factory.cc
M       src/objects/templates-inl.h
M       src/objects/templates.cc
M       src/objects/templates.h
M       src/objects/templates.tq

https://chromium-review.googlesource.com/5463594


### am...@chromium.org (2024-04-23)

Hi OP, thank you for this report. Can you let us know what name or handle you'd like us to use in publicly acknowledging you for this finding? Thanks!

### ei...@gmail.com (2024-04-23)

Hi! Just "Eirik" will work fine. Thanks for the speedy fix!

### am...@google.com (2024-04-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-25)

Congratulations Eirik! The Chrome VRP Panel has decided to award you $2,000 for this report of an data leak / information disclosure. A member of the Google finance p2p-vrp team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-07-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/333182464)*
