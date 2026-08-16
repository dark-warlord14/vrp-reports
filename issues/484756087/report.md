# Implement an IR for ANGLE's translator

| Field | Value |
|-------|-------|
| **Issue ID** | [484756087](https://issues.chromium.org/issues/484756087) |
| **Status** | Accepted |
| **Severity** | S1-High |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | sy...@chromium.org |
| **Assignee** | sy...@chromium.org |
| **Created** | 2026-02-15 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

A crafted GLSL ES 3.0 shader triggers an AST transformation bug in ANGLE's shared compiler frontend that produces an internally inconsistent AST (dangling variable references).

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/angle/angle/>

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

A crafted GLSL ES 3.0 shader triggers an AST transformation bug in ANGLE's shared compiler frontend that produces an internally inconsistent AST (dangling variable references). On the **D3D (Windows)** and **Metal (macOS)** backends, ANGLE's `validateAST` safety check is explicitly disabled (`false`), so the corrupted AST passes through uncaught. ANGLE reports **successful compilation** and emits **malformed output code** containing undeclared variable references, which is then handed directly to the platform GPU driver shader compiler (FXC/DXC or Metal shader compiler). This violates ANGLE's role as the security boundary between untrusted WebGL content and GPU drivers.

## Affected Platforms

| Platform | Backend | `validateAST` | Impact |
| --- | --- | --- | --- |
| **Windows** | D3D9/D3D11 | `false` | Malformed HLSL reaches FXC/DXC |
| **macOS** | Metal | `false` | Malformed MSL reaches Metal compiler |
| Linux | GL | `true` | Caught by validation (no bypass) |
| Android | GL | `true` | Caught by validation (no bypass) |

## Reproducer

**GLSL ES 3.0 shader (262 bytes):**

```
#version 300 es
precision mediump float;
int u0mode; out vec4 fragOut;
void main(){
  vec4 c = vec4(0);
  for(int i=0;i<0;i++){ if(0==u0mode){break;} }
  switch(u0mode){ case 0: case 1: ; }
  switch(u0mode){
    case 0: break;
      vec4 c = vec4(0);
      for(int i=0;i<0;i++) fragOut.g=.0;
    default: c.a=.0;
  }
}

```

**Trigger:** `vec4 c` is declared at function scope, then re-declared (shadowed) inside a `switch/case` block. Multiple switch statements with empty cases cause a tree transformation pass to drop the outer `c` declaration while retaining references to it, creating a dangling symbol reference in the AST.

## Root Cause

1. Shader declares `vec4 c` at function scope
2. Inside a `switch` block, `vec4 c` is re-declared (shadowing)
3. A tree transformation pass (`SeparateDeclarations`, `PruneEmptyCases`, or `PruneNoOps`) processes the repeated switch blocks
4. The transformation drops the outer `c` declaration but leaves references to it in the `default:` case — AST now contains symbol ID 3006 referencing a removed declaration (symbol ID 3004)
5. On GL/Vulkan backends, `validateAST` catches this (`ERROR: 'c' : Found reference to undeclared or inconsistently transformed variable`). On D3D/Metal, `validateAST` is `false` — the corruption passes through silently

**Location:** `src/compiler/translator/Compiler.cpp:774` (validation gate)
**D3D disable:** `src/libANGLE/renderer/d3d/ShaderD3D.cpp:338` (`validateAST = false`)
**Metal disable:** `src/libANGLE/renderer/metal/ShaderMtl.mm:63` (`validateAST = false`)

## Malformed Output Evidence

ANGLE produces the following output while reporting compilation success:

**HLSL (Windows D3D path):**

```
switch (_u0mode) {
  case (0):
    break;
  default:
    (_c3006.w = 0.0);    // UNDECLARED - variable declaration was dropped
    break;
}

```

**ESSL / GLSL 4.50 output:**

```
switch (_uu0mode) {
  case (0):
    break;
  default:
    (_uc.w = 0.0);       // UNDECLARED - same corruption
}

```

In all output formats, ANGLE returns compilation success while emitting code that references a variable (`_c3006` / `_uc`) that is never declared.

#### Impact analysis

Any web page can exploit this without user interaction. By serving a crafted WebGL shader, an attacker bypasses ANGLE's shader validation boundary on Windows (D3D) and macOS (Metal), where the validateAST safety check is disabled. ANGLE reports successful compilation and emits malformed output code containing undeclared variable references, which is then passed directly to the platform GPU driver shader compiler (FXC/DXC on Windows, Metal compiler on macOS).

The attacker gains the ability to deliver structurally invalid shader code to GPU driver compilers that assume their input has been validated. The GPU process runs with broader privileges than the sandboxed renderer process. I believe the GPU driver shader compiler represents a separate security boundary, any vulnerability in how it handles malformed input would be a distinct bug requiring its own fix. ANGLE's role is to ensure malformed shaders never reach that boundary in the first place.

---

### The cause

#### What version of Chrome have you found the security issue in?

Tested on Chrome 145.0.7632.76 (Official Build) (64-bit) (cohort: Stable) (Windows)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Exploit Mitigation Bypass

#### How would you like to be publicly acknowledged for your report?

Jason Villaluna

## Attachments

- [angle_shader_compiler_ast_validation_bypass_poc.html](attachments/angle_shader_compiler_ast_validation_bypass_poc.html) (text/html, 7.3 KB)
- [angle_shader_compiler_ast_validation_bypass_poc.html](attachments/angle_shader_compiler_ast_validation_bypass_poc_73465622.html) (text/html, 7.3 KB)

## Timeline

### an...@chromium.org (2026-02-17)

[security shepherd]: Thanks for the report. Assigning this to @sy...@chromium.org who may be familiar with the component.

### ch...@google.com (2026-02-18)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-18)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sy...@chromium.org (2026-02-18)

I can reproduce the crash with a simpler shader:

```
#version 300 es
precision mediump float;
uniform int u0;
out vec4 fragOut;
void main(){
  switch(u0){
    case 0:
      break;
      vec4 d = vec4(0);
    default:
      d.a=.0;
  }
}

```

It looks like the issue is in how GLSL allows a variable declaration in a case that lives through the next case in combination with that declaration being dead code (it's after `break`)

### dx...@google.com (2026-02-21)

Project: angle/angle  

Branch:  main  

Author:  Shahbaz Youssefi [syoussefi@chromium.org](mailto:syoussefi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7589940>

IR: Fix variable declaration in dead code in `case`

---


Expand for full commit details

```IR: Fix variable declaration in dead code in `case`

```
Corner case fix for when a variable is declared in dead code in a `case` 
block, but it should still be available to the next `case` block. 
 
Bug: angleproject:484756087 
Change-Id: Ic6d95fa180e0ccf18fe3b875db325b3590d04b74 
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7589940 
Commit-Queue: Brian Sheedy <bsheedy@chromium.org> 
Reviewed-by: Matthew Denton <mpdenton@chromium.org>

```
```

---

Files:
* M       `src/compiler/translator/ir/src/builder.rs`
* M       `src/tests/gl_tests/GLSLTest.cpp`

---

Hash: [484cd62d483501b9683be4c78502c8718fa9ef1e](https://chromiumdash.appspot.com/commit/484cd62d483501b9683be4c78502c8718fa9ef1e)\
Date: Wed Feb 18 15:59:05 2026

</details>

---

```

### sy...@chromium.org (2026-02-21)

I've fixed this for the work-in-progress IR. I looked at the AST transformation, but it doesn't look like it can easily be fixed. It'll have to wait until the IR is done and the AST pass is gone.

### ch...@google.com (2026-03-08)

syoussefi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-03-23)

syoussefi: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-05-07)

Project: angle/angle  

Branch:  main  

Author:  Shahbaz Youssefi [syoussefi@chromium.org](mailto:syoussefi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7829599>

AST: Fix variable declaration in dead code in `case`

---


Expand for full commit details

```AST: Fix variable declaration in dead code in `case`

```
Previously fixed for IR here: 
 
https://chromium-review.git.corp.google.com/c/angle/angle/+/7589940 
 
A similar transformation is applied to the AST transformation. 
 
Bug: chromium:484756087 
Change-Id: I579f839613ed5f1e05084f2b1c19bc0dbd386cbc 
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7829599 
Commit-Queue: Shahbaz Youssefi <syoussefi@chromium.org> 
Reviewed-by: Geoff Lang <geofflang@chromium.org>

```
```

---

Files:
* M       `src/compiler/translator/tree_ops/PruneNoOps.cpp`
* M       `src/tests/gl_tests/GLSLTest.cpp`

---

Hash: [ab41985470ba0a74e80ecfd7ec21e4d9ada428da](https://chromiumdash.appspot.com/commit/ab41985470ba0a74e80ecfd7ec21e4d9ada428da)\
Date: Thu May 7 19:25:01 2026

</details>

---

```

### dx...@google.com (2026-05-08)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7830827>

Roll ANGLE from 336e9a1b87e5 to ab41985470ba (1 revision)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/336e9a1b87e5..ab41985470ba 
     
    2026-05-07 syoussefi@chromium.org AST: Fix variable declaration in dead code in `case` 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,yuxinhu@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:484756087 
    Tbr: yuxinhu@google.com 
    Change-Id: I117acc182a2d53b992e296c079da57f7f61cb28b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7830827 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1627432}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [3070f6aa1e56f3f81bd876726bf93f65f17836c0](https://chromiumdash.appspot.com/commit/3070f6aa1e56f3f81bd876726bf93f65f17836c0)  

Date: Fri May 8 02:25:32 2026


---

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. Exploit mitigation bypass.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline. Exploit mitigation bypass.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484756087)*
