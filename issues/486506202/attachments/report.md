## VULNERABILITY DETAILS

### Summary

When decoding WebM VP9 content with alpha enabled, Chromium allocates an uninitialized alpha-plane buffer and copies only the visible-width alpha pixels into it. If the decoded frame's coded width exceeds its visible width, the per-row padding bytes remain uninitialized. WebCodecs `VideoFrame.copyTo()` allows JavaScript to request a copy using a rectangle bounded by the frame's coded size. For CPU-backed frames, the copy path copies the full requested width per row from the alpha plane, so JavaScript can read the uninitialized padding bytes. This results in renderer heap information disclosure.

### Description

WebM demuxing supports alpha for VP9 by storing alpha data in `BlockAdditional` side data: the first 8 bytes of the side data are the `BlockAddID` in big endian; when that value is `1`, the remainder is stored in the `DecoderBuffer`'s `side_data()->alpha_data` (see `media/formats/webm/webm_cluster_parser.cc`). When the track's `AlphaMode` element is `1`, Chromium sets `VideoDecoderConfig::AlphaMode::kHasAlpha` (`media/formats/webm/webm_video_client.cc`).

In `VpxVideoDecoder`, the external frame buffer path is used only for VP9 (`memory_pool_` is created only when `config.codec() == VideoCodec::kVP9`). For VP9 with alpha, the alpha plane is allocated in `FrameBufferPool::AllocateAlphaPlaneForFrameBuffer()` (`media/base/frame_buffer_pool.cc`), which uses `base::UncheckedMalloc()` and does not initialize the memory. The alpha plane is then filled via `libyuv::CopyPlane()` with width = `vpx_image_alpha->d_w` (visible width) and height = `vpx_image_alpha->d_h`. When the stride (coded width) is greater than `d_w`, the remaining bytes at the end of each row are never written and remain uninitialized.

The resulting `VideoFrame` has `coded_size` from `vpx_image->w` and `visible_rect` from `(d_w, d_h)`. In Blink WebCodecs, `VideoFrame.copyTo()` accepts a source rectangle that is validated against the frame's coded size. For mappable frames, `CopyMappablePlanes()` copies `src_rect.width()` bytes per row from each plane without clamping to the visible rect. By passing a rectangle that spans the full coded width, JavaScript can copy and then read the uninitialized alpha-plane padding.

The precondition is that the decoded VP9 frame has coded width > visible width (e.g. due to stride alignment). When this holds, the read is deterministic; the content of the leaked bytes depends on allocator state.

---

## VERSION

- **Chrome Version:** 145.0.7632.110 (Official Build) (64-bit)
- **Operating System:** platform-independent. Verified on: Windows 10 x86_64, Linux x86_64, macOS AArch64, Android AArch64

---

## REPRODUCTION CASE

1. Create a WebM file containing VP9 video with alpha:
   - `TrackEntry` `AlphaMode` = `1`
   - Alpha data in `BlockAdditional` with `BlockAddID` = `1`
   - Frames where coded width > visible width (e.g. odd or non-aligned width such as 9, 17).

   This WebM file can be created using ffmpeg with the following command:

   ```bash
   ffmpeg -f lavfi -i "color=c=gray:s=17x17" -frames:v 1 -pix_fmt yuva420p -c:v libvpx-vp9 -y vp9_17x17.webm
   ```

2. Load the video in Chrome (e.g. via `<video>` or fetch + decode).

3. Obtain a `VideoFrame` for a decoded frame (e.g. wrap the current frame from an `HTMLVideoElement` using the WebCodecs `VideoFrame` constructor).

4. Call:

   ```js
   frame.copyTo(destination, { rect: { x: 0, y: 0, width: frame.codedWidth, height: frame.codedHeight } });
   ```

5. Inspect the alpha plane in the destination buffer (plane index `3` for `I420A`). Bytes from column `frame.visibleRect.width` to `frame.codedWidth - 1` on each row are uninitialized and may contain heap data.

Minimal proof-of-concept: a VP9-with-alpha WebM (e.g. 9×9 or 17×17) and an HTML page that decodes one frame, calls `copyTo` with the coded rect, and logs the alpha-plane padding bytes.

**Attached:**
* **exploit_poc.html** : Proof Of Concept script showing a full leak
* **vp9_17x17.webm** : VP9-with-alpha WebM file 17x17
* **heap_ptr_leak.html** : Proof Of Concept script for x86_64 which accurately retrieves a heap pointer from the leak

The HTML files are written to be served from a web server and not just be opened locally.

**Example of how to serve the files:**
```py
python3 -m http.server 8000
```
Navigate to http://127.0.0.1:8000/exploit_poc.html to display the uninitialized heap memory disclosure

---

## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Not applicable (information disclosure; no crash).

---

## EXPLOITATION SCENARIOS

- **Renderer heap disclosure:**  An attacker serves a page that decodes a crafted VP9-with-alpha WebM and uses `VideoFrame.copyTo()` with a coded-size rectangle to read uninitialized alpha-plane padding, disclosing renderer heap bytes to JavaScript.
- Repeated decoding with different frame sizes can sample multiple allocations and increase the chance of observing useful data (e.g. pointers, strings).

---

## IMPACT

**Severity:** Medium

Uninitialized renderer heap bytes become readable by JavaScript. This provides a defense-in-depth bypass and can support further exploitation (e.g. heap layout disclosure for a separate exploit).

---

## CREDIT INFORMATION

**Reporter:** Octane Security (Giovanni Vignone, Paolo Gentry, Robert van Eijk)