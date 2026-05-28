# WebAssembly OOB memory access due to cached memory index confusion

| Field | Value |
|-------|-------|
| **Issue ID** | [362780326](https://issues.chromium.org/issues/362780326) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2024-08-29 |
| **Bounty** | $20,000.00 |

## Description

### VULNERABILITY DETAILS

#### Summary

WebAssembly OOB memory access on `SmiTagging<8>` platforms due to i31.get\_s sign extension

#### Details

On platforms where `SmiTagging<8>` is used, the following Liftoff code is generated for `i31.get_s` opcode:

```
  void I31GetS(FullDecoder* decoder, const Value& input, Value* result) {
    LiftoffRegList pinned;
    LiftoffRegister src = pinned.set(__ PopToRegister());
    MaybeEmitNullCheck(decoder, src.gp(), pinned, input.type);
    LiftoffRegister dst = __ GetUnusedRegister(kGpReg, {src}, {});
    if constexpr (SmiValuesAre31Bits()) {
      __ emit_i32_sari(dst.gp(), src.gp(), kSmiTagSize);
    } else {
      DCHECK(SmiValuesAre32Bits());
      // Topmost bit is already sign-extended.
      __ emit_i64_sari(dst, src, kSmiTagSize + kSmiShiftSize);     // [!] 64bit shift arithmetic right may clobber upper bits with 1s
    }
    __ PushRegister(kI32, dst);
  }

```

This results in the `dst` register to be a full 64bit signed value, with the top bits clobbered to 1. This can be abused to cause OOB writes, for example with `i64.store` on a WASM memory as the full 64bit register is used for indexing.

Exploitability is slightly questionable on Chrome, but my current analysis is that it's technically possible on certain conditions. A similar reference would be [b/351327767](https://issues.chromium.org/issues/351327767), but in this case we have a limited offset write to the negative direction - as memory32 does not have guard pages on the lower address side ("left" side), we can fill up the 4gb v8 sandbox space and overwrite memory there.

#### Bisect

The following commit that introduced Liftoff i31 support seems to be the problematic commit:  

<https://chromiumdash.appspot.com/commit/432c0a78e95244f19de30a83552d6dad4c86c7f1>

### VERSION

See bisect commit release info in Chromium Dash for more info.

Chrome Version: ?? (Is there an official build that uses `SmiTagging<8>`?)  

Operating System: Likely non-x64 & non-arm64 by default due to pointer compression enabled by default, [src](https://source.chromium.org/chromium/chromium/src/+/main:v8/BUILD.bazel;drc=7e5f34d1c1dfde9855b90d3f3767504be6e2fdae;l=303)

### REPRODUCTION CASE

Attached as `poc.html` which crashes `d8` built with the following gn flags (note the last line):

```
is_debug=false
dcheck_always_on=false
target_cpu="x64"
v8_enable_pointer_compression=false

```

`d8` binary and `snapshot_blob.bin` built with the above gn flags also attached (based on commit aff6071). PoC is tailor-made to crash `d8`, so running this on Chrome builds with `SmiTagging<8>` will likely not crash (trap handler seems to mistakenly assume a guard page at lower address side and captures it).

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Renderer (d8)  

Crash State: Aborts in malloc-related functions in worker due to memory corruption

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n)

---

P.S. Please let me know if `SmiTagging<8>` builds are a real thing, thanks :)

## Attachments

- [d8](attachments/d8) (application/x-sharedlib, 38.1 MB)
- [snapshot_blob.bin](attachments/snapshot_blob.bin) (application/octet-stream, 385.1 KB)
- [poc.js](attachments/poc.js) (text/javascript, 72.2 KB)

## Timeline

### se...@gmail.com (2024-08-29)

Forgot the attachments, adding them here. Also, the PoC is `poc.js` for use in `d8` and not a html file.

### ti...@chromium.org (2024-08-29)

(security shepherd)

I was able to reproduce with the specified build flags, however I also don't think we have any 64 bit platforms with pointer compression disabled (`SmiTagging<8>`).
Setting the hypothetical severity to S1, marking it Security\_Impact-None, and setting OS=Linux as it only probably affects d8. Passing off to the current V8 security shepherd sroettger@ who might be more up to date with this :)

### pe...@google.com (2024-08-29)

The Found In field may only contain numeric values.
Some values couldn't be corrected but were removed, please verify that any important data wasn't lost.
You can see the changes by toggling full history on the issue.

### sr...@google.com (2024-08-30)

Security_Impact-None sounds right to me. I don't think we're shipping this configuration.

### jk...@chromium.org (2024-08-30)

Just a quick comment to confirm that we don't ship SmiTagging<8> in Chrome. I believe Node.js uses it.

(I won't get to this for at least 2-3 weeks; if you think it's more urgent than that, please assign it to someone else.)

### jk...@chromium.org (2024-10-16)

Made a patch for this just because it's a quick way to reduce the number of open issues by one: <https://chromium-review.googlesource.com/c/v8/v8/+/5937815>

### ap...@google.com (2024-10-16)

Project: v8/v8  

Branch: main  

Author: Jakob Kummerow <[jkummerow@chromium.org](mailto:jkummerow@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5937815>

[wasm][32-bit Smis] Fix i31.get\_s in Liftoff

---


Expand for full commit details
```
[wasm][32-bit Smis] Fix i31.get_s in Liftoff

The upper half of the register holding the i32 value returned
by this operation should be zeroed out.
This patch has no impact on pointer-compressed configurations.

Fixed: 362780326
Change-Id: I87723db962cb826570b5772d14857f79e4269b8f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5937815
Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
Reviewed-by: Clemens Backes <clemensb@chromium.org>
Commit-Queue: Clemens Backes <clemensb@chromium.org>
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/main@{#96626}

```

---

Files:

- M `src/wasm/baseline/liftoff-compiler.cc`

---

Hash: 2dddda9a22e42925fb280a80eb1b74e77793b437  

Date:  Wed Oct 16 16:18:13 2024


---

### am...@chromium.org (2024-10-22)

Thanks for the report, Seunghyun. Since this issue does not impact a shipped, production configuration of Chrome, this report is unfortunately not eligible for a Chrome VRP reward.

### pe...@google.com (2025-01-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/362780326)*
