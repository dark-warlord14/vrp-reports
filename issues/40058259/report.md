# Security: Stack-Buffer-Overflow in WebRtcPcm16b_Decode

| Field | Value |
|-------|-------|
| **Issue ID** | [40058259](https://issues.chromium.org/issues/40058259) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC, Blink>WebRTC>Audio |
| **Platforms** | Linux, Windows |
| **Reporter** | vi...@gmail.com |
| **Assignee** | hl...@chromium.org |
| **Created** | 2021-12-17 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

In WebRTC pcm16b codecs audio decoder, there is no check in WebRtcPcm16b\_Decode for ensuring `encoded length` less or equal than `speech` buffer size. This makes assigning speech[i] possible to trigger a buffer overflow when decoding a frame which `len` > `speech` buffer size.

**VERSION**  

\*\* In WebRTC component native. Not sure if Chrome blink is affected. \*\*  

Chrome Version: 96.0.4664.93 stable  

Operating System: Windows, Linux

**REPRODUCTION CASE**  

Make a simple fuzz driver by using "audio\_decoder\_pcm16b\_fuzzer.cc" as template And runing PoC file in the attachment.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==144101==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fbf2faff6a0 at pc 0x55b815766b97 bp 0x7ffc55a56030 sp 0x7ffc55a56028  

WRITE of size 2 at 0x7fbf2faff6a0 thread T0  

#0 0x55b815766b96 in WebRtcPcm16b\_Decode modules/audio\_coding/codecs/pcm16b/pcm16b.c:30:15  

#1 0x55b8157626e7 in webrtc::AudioDecoderPcm16B::DecodeInternal(unsigned char const\*, unsigned long, int, short\*, webrtc::AudioDecoder::SpeechType\*) modules/audio\_coding/codecs/pcm16b/audio\_decoder\_pcm16b.cc:45:16  

#2 0x55b815763202 in webrtc::AudioDecoder::Decode(unsigned char const\*, unsigned long, int, unsigned long, short\*, webrtc::AudioDecoder::SpeechType\*) api/audio\_codecs/audio\_decoder.cc:95:10  

#3 0x55b8155ce1eb in webrtc::FuzzAudioDecoder(webrtc::DecoderFunctionType, unsigned char const\*, unsigned long, webrtc::AudioDecoder\*, int, unsigned long, short\*) test/fuzzers/audio\_decoder\_fuzzer.cc:64:18  

#4 0x55b8155cdfb5 in LLVMFuzzerTestOneInput test/fuzzers/audio\_decoder\_pcm16b\_fuzzer.cc:28:3  

#5 0x55b81563f0c7 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const\*, unsigned long) third\_party/libFuzzer/src/FuzzerLoop.cpp:556:15  

#6 0x55b81560cd3f in fuzzer::RunOneTest(fuzzer::Fuzzer\*, char const\*, unsigned long) third\_party/libFuzzer/src/FuzzerDriver.cpp:292:6  

#7 0x55b81561a1ed in fuzzer::FuzzerDriver(int\*, char\*\*\*, int (\*)(unsigned char const\*, unsigned long)) third\_party/libFuzzer/src/FuzzerDriver.cpp:774:9  

#8 0x55b8156744ac in main third\_party/libFuzzer/src/FuzzerMain.cpp:19:10  

#9 0x7fbf30cad83f in \_\_libc\_start\_main /build/glibc-S7Ft5T/glibc-2.23/csu/../csu/libc-start.c:291

Address 0x7fbf2faff6a0 is located in stack of thread T0 at offset 1696 in frame  

#0 0x55b8155cde7f in LLVMFuzzerTestOneInput test/fuzzers/audio\_decoder\_pcm16b\_fuzzer.cc:16

This frame has 2 object(s):  

[32, 56) 'dec' (line 24)  

[96, 1696) 'output' (line 27) <== Memory access at offset 1696 overflows this variable  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork  

(longjmp and C++ exceptions \*are\* supported)  

SUMMARY: AddressSanitizer: stack-buffer-overflow modules/audio\_coding/codecs/pcm16b/pcm16b.c:30:15 in WebRtcPcm16b\_Decode  

Shadow bytes around the buggy address:  

0x0ff865f57e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff865f57e90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff865f57ea0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff865f57eb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff865f57ec0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0ff865f57ed0: 00 00 00 00[f3]f3 f3 f3 f3 f3 f3 f3 f3 f3 f3 f3  

0x0ff865f57ee0: f3 f3 f3 f3 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff865f57ef0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff865f57f00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff865f57f10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff865f57f20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==144101==ABORTING

## Attachments

- [audio_decoder_pcm16b_fuzzer.cc](attachments/audio_decoder_pcm16b_fuzzer.cc) (text/plain, 1.2 KB)
- [SIGABRT.PC.55555578c792.STACK.945b60fe.CODE.-6.ADDR.0.INSTR.lea____0x146b3b(%rip),%rdi________#_0x0000000000146b42.fuzz](attachments/SIGABRT.PC.55555578c792.STACK.945b60fe.CODE.-6.ADDR.0.INSTR.lea_0x146b3b(%rip),%rdi_#_0x0000000000146b42.fuzz) (application/octet-stream, 3.3 KB)
- [audio_decoder_pcm16b_fuzzer.cc](attachments/audio_decoder_pcm16b_fuzzer.cc) (text/plain, 782 B)

## Timeline

### [Deleted User] (2021-12-17)

[Empty comment from Monorail migration]

### vi...@gmail.com (2021-12-17)

Update fuzzer code.

### me...@chromium.org (2021-12-18)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebRTC>Audio]

### [Deleted User] (2021-12-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-31)

alessiob: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-15)

alessiob: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2022-01-18)

Sheriff ping for attention on this one. Adding more folks from Blink>WebRTC>Audio - can you please take a look and triage this bug ASAP?

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### ke...@chromium.org (2022-02-09)

Assigning to hlundin@ for triage. Assistance resolving this is appreciated.

### hl...@chromium.org (2022-02-11)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-02-11)

Lowering the priority since Chrome blink is NOT affected.
`AudioDecoderPcm16B` and `AudioEncoderPcm16B ` are not used, but I believe we should keep them for testing.

### [Deleted User] (2022-02-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2022-02-14)

[Empty comment from Monorail migration]

### hl...@chromium.org (2022-02-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-15)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/ac341df436895ff901aeb1310f150241499c29d7

commit ac341df436895ff901aeb1310f150241499c29d7
Author: Henrik Lundin <henrik.lundin@webrtc.org>
Date: Tue Feb 15 15:13:34 2022

Adding fuzzer for PCM16b decoder and fixing a fuzzer problem

Bug: chromium:1280852
Change-Id: I7f6c5de86ceee01156743c0389c59f875e53bb5f
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/251580
Reviewed-by: Minyue Li <minyue@webrtc.org>
Commit-Queue: Henrik Lundin <henrik.lundin@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#36005}

[add] https://crrev.com/ac341df436895ff901aeb1310f150241499c29d7/test/fuzzers/audio_decoder_pcm16b_fuzzer.cc
[modify] https://crrev.com/ac341df436895ff901aeb1310f150241499c29d7/modules/audio_coding/codecs/pcm16b/audio_decoder_pcm16b.cc
[modify] https://crrev.com/ac341df436895ff901aeb1310f150241499c29d7/test/fuzzers/BUILD.gn


### gi...@appspot.gserviceaccount.com (2022-02-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0fb95f3a8485d8cf9c77ab17932109810aad84a1

commit 0fb95f3a8485d8cf9c77ab17932109810aad84a1
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Feb 15 19:26:20 2022

Roll WebRTC from 1b083a998b07 to ac341df43689 (2 revisions)

https://webrtc.googlesource.com/src.git/+log/1b083a998b07..ac341df43689

2022-02-15 henrik.lundin@webrtc.org Adding fuzzer for PCM16b decoder and fixing a fuzzer problem
2022-02-15 hta@webrtc.org Add restrictive visibility to all targets in //pc

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1280852
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: Id5b7dce592a99aa530bf20d2173dbb2ea789f731
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3464699
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#971366}

[modify] https://crrev.com/0fb95f3a8485d8cf9c77ab17932109810aad84a1/DEPS


### vi...@gmail.com (2022-02-16)

Thanks for the fixing. I wonder know issue like this not in Chrome release could award a CVE or not? 

### hl...@chromium.org (2022-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-23)

As Chrome Blink is not impact, this issue is unfortunately not eligible for a VRP reward. To respond to the question in https://crbug.com/chromium/1280852#c18, we are unable to provide a CVE since this issue does not manifest in or impact Chrome. 

### hl...@chromium.org (2022-02-24)

I believe that the PCM16B codec (a.k.a. "L16") is in fact included in the standard Chromium build. It is not included in the standard SDP offer/answer, but you can munge the offer and answer to use L16. Routing back to reward-topanel with this info.

### am...@google.com (2022-03-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-03)

Congratulations, the VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be in touch soon to arrange payment. In the interim, please let us know by what name, handle/tag, or other identifier you would like us to use in acknowledging you for this finding. Thank you for reporting this issue to us!


### vi...@gmail.com (2022-03-04)

Thank you!

### am...@google.com (2022-03-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-03-28)

[Comment Deleted]

### am...@chromium.org (2022-03-29)

[Comment Deleted]

### vi...@gmail.com (2022-03-29)

Please credit to Ying Wang and Yakun Zhang of Baidu Security. Thanks.

### [Deleted User] (2022-05-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1280852?no_tracker_redirect=1

[Multiple monorail components: Blink>WebRTC, Blink>WebRTC>Audio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058259)*
