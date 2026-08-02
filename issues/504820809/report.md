# WebGL can disclose stale stencil contents because ANGLE robust framebuffer initialization honors attacker-controlled stencilMask(0)

| Field | Value |
|-------|-------|
| **Issue ID** | [504820809](https://issues.chromium.org/issues/504820809) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android, Linux, Windows, ChromeOS |
| **Reporter** | mu...@winfunc.com |
| **Assignee** | ge...@google.com |
| **Created** | 2026-04-21 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

VULNERABILITY DETAILS

ANGLE's OpenGL robust-resource-initialization path can preserve stale stencil contents because the
internal clear helper in `BlitGL::SetClearState()` sets `glClearStencil(0)` but never restores the
front/back stencil write masks to all-ones before the later `glClear(GL_STENCIL_BUFFER_BIT)`.

On the GL backend, `FramebufferGL::ensureAttachmentsInitialized()` routes first-use attachment
initialization through `BlitGL::clearFramebuffer()`. If attacker-controlled WebGL state has already
latched `stencilMask(0)` into the underlying GL state machine, the internal stencil clear can be
suppressed while ANGLE still marks the attachment initialized. A later stencil-tested draw can then
turn the stale stencil bits into script-readable color output.

The sink is still present in current source:

```
if (stencilClear)
{
    stateManager->setClearStencil(0);
    *outClearMask |= GL_STENCIL_BUFFER_BIT;
}

```

Source references:

- `third_party/angle/src/libANGLE/context_private_call.inl.h`
- `third_party/angle/src/libANGLE/State.cpp`
- `third_party/angle/src/libANGLE/renderer/gl/StateManagerGL.cpp`
- `third_party/angle/src/libANGLE/Framebuffer.cpp`
- `third_party/angle/src/libANGLE/renderer/gl/FramebufferGL.cpp`
- `third_party/angle/src/libANGLE/renderer/gl/BlitGL.cpp`

The attached browser PoC primes a fresh `DEPTH24_STENCIL8` renderbuffer with stencil value `1`,
deletes it, syncs `stencilMask(0)` on a separate initialized framebuffer, then allocates a new
depth-stencil attachment and triggers robust initialization on first use. It finally uses
stencil-tested drawing plus `readPixels()` to detect non-zero stale stencil state.

On the latest Chromium `main` tip I synced for this validation pass, the browser leak is immediate.
Importantly, on this Linux/NVIDIA system it reproduces without any backend-forcing flags such as
`--use-gl=angle`, `--use-angle=gl`, or `--ignore-gpu-blocklist`; Chromium's default startup path
still selects `ANGLE (NVIDIA Corporation, NVIDIA L4/PCIe/SSE2, OpenGL 4.5.0)` for WebGL on this
machine. The first attempted victim allocation already produced `sum(red)=4177920`, which is the
full `128 x 128 x 255` frame, meaning the primed all-ones stencil pattern survived robust
initialization intact.

VERSION

Chrome Version: Chromium `149.0.7804.0` + dev (local ASan build from commit `edf6e4e6f9d6427ecb954106f5b889f94c30de88`)

Operating System: Ubuntu `22.04.5 LTS` x86\_64

GPU / GL renderer: `ANGLE (NVIDIA Corporation, NVIDIA L4/PCIe/SSE2, OpenGL 4.5.0)` on desktop Linux

REPRODUCTION CASE

Attachments:

- `poc.html`
- `stencil_browser_default_no_backend_flags_14978040.log`

Numbered repro steps:

1. Use a Chromium build configured to run WebGL through ANGLE's GL backend on a real GPU-backed X
   server.
2. Serve the attached PoC locally:

```
python3 -m http.server 8000

```

3. Run Chromium directly. The following command includes only convenience flags for profile/log
   hygiene; it does not force a specific GL backend:

```
out/asan/chrome \
  --user-data-dir=/tmp/chrome-stencil-poc \
  --no-first-run \
  --disable-background-networking \
  --disable-default-apps \
  --disable-sync \
  --metrics-recording-only \
  --enable-logging=stderr \
  'http://127.0.0.1:8000/poc.html?iters=2000&logEvery=50&test=nonzero'

```

Observed result:

```
[poc] UNMASKED_RENDERER_WEBGL=ANGLE (NVIDIA Corporation, NVIDIA L4/PCIe/SSE2, OpenGL 4.5.0)
[poc] sync FBO prepared
[poc] LEAK observed iteration=0 sum(red)=4177920

```

The attached `poc.html` also supports the exact `stencilFunc(EQUAL, 1, 0xFF)` mode from the
minimal write-up, but the attached browser run uses the broader `NOTEQUAL, 0` detection mode to maximize reliability when validating reused stencil contents.

Type of crash: N/A (stale stencil disclosure; no crash required)

Crash State:

```
N/A

```

Client ID (if relevant): N/A

CREDIT INFORMATION

Reporter credit: Mufeed VH from Winfunc Research (winfunc.com)

## Attachments

- [poc.html](attachments/poc.html) (text/html, 5.3 KB)
- [stencil_browser_default_no_backend_flags_14978040.log](attachments/stencil_browser_default_no_backend_flags_14978040.log) (text/plain, 7.9 KB)

## Timeline

### pe...@google.com (2026-04-22)

@mu...@winfunc.com This may end up s2 because there is not a demonstration of cross origin but i have yet to rule that out.
If you can resubmit one that demonstrates clear cross origin data access it will get at least an s1

### pe...@google.com (2026-04-22)

Setting s1 for now as cross origin uncertainty

### ch...@google.com (2026-04-23)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-04-24)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7785196>

GL: Set stencil write mask before clearing for robust init

---


Expand for full commit details
```
     
    Fixed: chromium:504820809 
    Change-Id: I45f2746e3e4e239d9bf72219330484349d441723 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7785196 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `src/libANGLE/renderer/gl/BlitGL.cpp`
- M `src/tests/gl_tests/RobustResourceInitTest.cpp`

---

Hash: [9f099a5d233f7c311d0f3d3651365e0979fcba91](https://chromiumdash.appspot.com/commit/9f099a5d233f7c311d0f3d3651365e0979fcba91)  

Date: Wed Apr 22 17:28:09 2026


---

### mu...@winfunc.com (2026-05-01)

Post-fix Question: I noticed the fix has landed in ANGLE main. Could you confirm whether this issue is expected to receive a CVE when it reaches Chrome Stable? Also, is it being considered for merge/cherry-pick to a Stable or Beta branch, or will it ride the normal release train?

### aj...@google.com (2026-05-05)

-> Medium as this is a limited read in the gpu (High requires a fully controlled Read)

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### mu...@winfunc.com (2026-05-15)

Question: How are CVEs assigned and on what basis? For this vulnerability, now that it's fixed, would a CVE be issued? I'd love to know if some findings are exempt or if there's a criteria for it.

### ch...@google.com (2026-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/504820809)*
