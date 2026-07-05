# GPU sandbox escape on macOS via lsd.modifydb > RCE

| Field | Value |
|-------|-------|
| **Issue ID** | [491422244](https://issues.chromium.org/issues/491422244) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Video |
| **Platforms** | Mac |
| **Chrome Version** | 147.0.7704.0 |
| **Reporter** | ma...@advert.com.au |
| **Assignee** | da...@chromium.org |
| **Created** | 2026-03-10 |
| **Bounty** | $25,000.00 |

## Description

# Steps to reproduce the problem

Tested on 147.0.7704.0

1. `patch -p1 < poc.diff`
2. `gn gen out/Default --args='is_debug=false' && autoninja -C out/Default content_shell`
3. `out/Default/Content\ Shell.app/Contents/MacOS/Content\ Shell "data:text/html,<h1>trigger</h1>"`
4. Wait a few seconds for the GPU process to register the handler, then quit content\_shell.
5. Trigger mailto: from terminal, Chrome, or any app: `open "mailto:test@example.com"`
6. Observe: `~/Desktop/gpu_escape_poc.txt` is created and TextEdit opens. The file contains `uname -a` and `uptime` output, proving code execution outside the GPU sandbox.

# Problem Description

The GPU sandbox policy ([`sandbox/policy/mac/gpu.sb` line 28](https://source.chromium.org/chromium/chromium/src/+/main:sandbox/policy/mac/gpu.sb;l=28)) grants `com.apple.lsd.modifydb` Mach service access. This is GPU-only, not granted to renderer, audio, or utility sandboxes.

Combined with the GPU sandbox's file-write permission to `DARWIN_USER_CACHE_DIR` ([`gpu.sb` lines 122-126](https://source.chromium.org/chromium/chromium/src/+/main:sandbox/policy/mac/gpu.sb;l=122)), a compromised GPU process can:

1. Resolve `DARWIN_USER_CACHE_DIR` via `confstr(_CS_DARWIN_USER_CACHE_DIR)`
2. Write a `.app` bundle there (sandbox permits file-write)
3. Strip quarantine xattr via `removexattr()` (permitted because `gpu.sb` grants `file-write*` to this directory, which includes `file-write-xattr`)
4. Call `LSRegisterURL` to register the app with Launch Services
5. Call `LSSetDefaultHandlerForURLScheme` to claim `mailto:` (and `chickennuggets://`)
6. When Chrome loads a page with `window.location = "mailto:..."`, Chrome dispatches to the OS, which launches the hijacked handler outside the sandbox

The PoC demonstrates this from inside `HandleRasterCHROMIUM` in [`gpu/command_buffer/service/raster_decoder.cc`](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/raster_decoder.cc;l=3036), reachable from a compromised renderer via GPU command buffer IPC. The payload writes a file to `~/Desktop/gpu_escape_poc.txt` and opens TextEdit.

The `mailto:` hijack is particularly impactful: every website with a "contact us" or "email" link uses `mailto:`, and the hijack is system-wide (affects Chrome, Safari, Slack, and every other application). `window.location = "mailto:..."` fires automatically on page load with zero user interaction.

# Additional Comments

- Content Shell does not dispatch external protocol navigations. In Chrome, `window.location = "mailto:..."` will trigger the RCE.
- `com.apple.lsd.modifydb` was added in [f92299c](https://chromium.googlesource.com/chromium/src/+/f92299c) (2019-04-24, [bug 871280](https://issues.chromium.org/issues/871280)): "macOS V2 Sandbox: Allow lsd.modifydb in GPU v2 sandbox." Present for ~7 years across all Chrome releases since Chrome 76.

# Summary

GPU sandbox escape on macOS via lsd.modifydb > RCE

# Custom Questions

#### Type of crash:

no crash, clean sandbox escape.

#### Crash state:

No crash reports available as we are working within the GPU sandbox policy ([`sandbox/policy/mac/gpu.sb` line 28](https://source.chromium.org/chromium/chromium/src/+/main:sandbox/policy/mac/gpu.sb;l=28)).
output of `~/Desktop/gpu_escape_poc.txt`:

```
Darwin Macbook.local 25.3.0 Darwin Kernel Version 25.3.0: Wed Jan 28 20:53:31 PST 2026; root:xnu-12377.81.4~5/RELEASE_ARM64_T8122 x86_64
 0:16  up 21 days,  3:17, 18 users, load averages: 1.99 1.71 1.81

```
#### Reporter credit:

Mark Blaszczyk

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [poc.diff](attachments/poc.diff) (text/x-diff, 5.1 KB)

## Timeline

### ns...@chromium.org (2026-03-10)

Neat PoC, thank you!

Setting Severity medium and P1 as per guidelines.

Mark, please take a look.

### dc...@chromium.org (2026-03-12)

I'm guessing this is not really specific to 147 so tagging this was 146 as the current extended stable.

### ma...@chromium.org (2026-03-12)

Good bug. Thanks for the report!

Ken, can you help or find someone who can help on this? We seem to have lost track of what `com.apple.lsd.modifydb` was needed for, since it’s been there since the beginning of the V2 sandbox. Ideally, we’d just get rid of it.

### ma...@advert.com.au (2026-03-13)

looks like [crbug.com/871280](https://crbug.com/871280)

My interpretation is that lsd.mapdb should be enough, plus tightening of file-write-\* so file-write-xattr cannot strip quarantine/+x.

Untested diff below.

```
diff --git a/sandbox/policy/mac/gpu.sb b/sandbox/policy/mac/gpu.sb
index 9d98e441d5..691bca68f3 100644
--- a/sandbox/policy/mac/gpu.sb
+++ b/sandbox/policy/mac/gpu.sb
@@ -25,7 +25,6 @@
   (global-name "com.apple.cvmsServ")
   (global-name "com.apple.gpumemd.source")
   (global-name "com.apple.lsd.mapdb")
-  (global-name "com.apple.lsd.modifydb")
   (global-name "com.apple.powerlog.plxpclogger.xpc")
   (global-name "com.apple.PowerManagement.control")
   (global-name "com.apple.SecurityServer")
@@ -119,7 +118,9 @@
 )

 ; crbug.com/980134
-(allow file-read* file-write*
+; Restrict file-write to data/create/unlink only — the GPU process does not need
+; file-write-xattr (quarantine stripping), file-write-mode, or file-write-owner.
+(allow file-read* file-write-data file-write-create file-write-unlink
   (subpath (param darwin-user-cache-dir))
   (subpath (param darwin-user-dir))
   (subpath (param darwin-user-temp-dir))

```

### ch...@google.com (2026-03-13)

Setting milestone because of s2 severity.

### ma...@advert.com.au (2026-03-13)

Would s2 be the correct severity here?

### kb...@chromium.org (2026-03-13)

The folks who worked on [crbug.com/871280](https://crbug.com/871280) no longer work on Chromium.

Dale - could you or someone on the media team please test the suggested tightening of `gpu.sb` and see whether any media / video regressions happen?

### da...@chromium.org (2026-03-16)

The crashes all pre-date the M-series chips, so might need vetting on a x86 mac. @eu...@chromium.org do you still have an intel mac for testing?

I've put up <https://chromium-review.git.corp.google.com/c/chromium/src/+/7671372?tab=checks> based on the patch in [comment#5](https://issues.chromium.org/issues/491422244#comment5) to see if it can pass the CQ at least.

### da...@chromium.org (2026-03-16)

Looks like playback passes the CQ, but the WebNN tests start failing with the tightened sandbox:

```
[56745:1634365:0316/130054.818258:ERROR:services/webnn/coreml/graph_impl_coreml.mm:432] [WebNN] Error Domain=com.apple.CoreML Code=0 "compiler error: Encountered an error while compiling a neural network model: Failed to set owner and group on copied weights during compilation. Error description: You don’t have permission to save the file “weights.bin” in the folder “weights”." UserInfo={NSLocalizedDescription=compiler error: Encountered an error while compiling a neural network model: Failed to set owner and group on copied weights during compilation. Error description: You don’t have permission to save the file “weights.bin” in the folder “weights”.}

```

### da...@chromium.org (2026-03-16)

WDYT @re...@chromium.org ?

### re...@chromium.org (2026-03-16)

I'm not sure why CoreML tries to set file ownership since the file should already be owned by the current user since the application just created it. However, this code is outside our control so I wonder if we can allow file-write-owner without reducing the effectiveness of this mitigation.

I'm reaching out to our contact at Apple to ask why CoreML requires this permission.

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  main  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7671372>

Tighten macOS GPU sandbox restrictions

---


Expand for full commit details
```
     
    These were added back in 2018 and don't seem to be necessary 
    anymore. 
     
    Changes suggested by mark <at> advert.com.au 
     
    Fixed: 491422244 
    Change-Id: Ie7c37352b0b9fbb324611eb247bae9b4ab4ad467 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7671372 
    Reviewed-by: Mark Mentovai <mark@chromium.org> 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600856}

```

---

Files:

- M `sandbox/policy/mac/gpu.sb`

---

Hash: [7082f06110390405f1ecd750a783101b40e8fbfa](https://chromiumdash.appspot.com/commit/7082f06110390405f1ecd750a783101b40e8fbfa)  

Date: Tue Mar 17 23:03:31 2026


---

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### aj...@google.com (2026-06-24)

S1 as this described a sandbox escape on MacOS where we expect the GPU process to be reasonably sandboxed.

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
GPU Sandbox bypass.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491422244)*
