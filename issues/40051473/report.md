# Security: Use-after-poison in AudioWorkletNode

| Field | Value |
|-------|-------|
| **Issue ID** | [40051473](https://issues.chromium.org/issues/40051473) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Messaging, Blink>WebAudio |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | da...@davidmanouchehri.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2020-02-09 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Inside AudioWorkletNode::Create, we can end up in a state where GetExecutionContext() is executed on a garbage collected context.

We can trigger this edge case through the following steps:

1. Create an iframe and append it to our document to get a new ExecutionContext
2. Create a OfflineAudioContext within our new iframe's ExecutionContext
3. Add a new AudioWorklet on our OfflineAudioContext
4. Remove the iframe's ExecutionContext, which calls ContextLifecycleObserver::ContextDestroyed -> AudioContext::ContextDestroyed -> AudioContext::Uninitialize() -> BaseAudioContext::Uninitialize()
5. Create a new AudioWorkletNode, which will attempt to use the context that was uninitialized

AudioWorkletNode\* AudioWorkletNode::Create(  

ScriptState\* script\_state,  

BaseAudioContext\* context,  

const String& name,  

const AudioWorkletNodeOptions\* options,  

ExceptionState& exception\_state) {  

...  

auto\* channel =  

MakeGarbageCollected<MessageChannel>(context->GetExecutionContext()); // <-------------- UAP  

MessagePortChannel processor\_port\_channel = channel->port2()->Disentangle();  

...  

}

This should be reachable from both AudioContext and OfflineAudioContext; my test case uses OfflineAudioContext because I find it pretty annoying when I accidentally play random noise out of my speakers while debugging.

**VERSION**  

Tested on 80.0.3987.87 + stable and 82.0.4053.0 + canary  

Operating System: Any

**REPRODUCTION CASE**  

Put audio.html, audio.js, and processor.js in the same folder, then serve that folder over HTTPS (AudioWorklets do not obey --allow-insecure-localhost for some reason). You can use any web server you want, but I used caddy as it's quick to set up.

cd /home/dave/0days/chrome/0010/ # You should have Caddyfile, audio.html, audio.js, and processor.js in this folder  

curl <https://getcaddy.com> | bash -s personal # I'm not suggesting this is best practice =P  

caddy -quic

Open <https://localhost:44444/audio.html> after your HTTPS web server is running.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Tab/renderer  

Crash State:  

Received signal 11 SEGV\_MAPERR 000000000000  

#0 0x7f37c737bdc9 base::debug::CollectStackTrace()  

#1 0x7f37c72b6653 base::debug::StackTrace::StackTrace()  

#2 0x7f37c737b970 base::debug::(anonymous namespace)::StackDumpSignalHandler()  

#3 0x7f37bb4ca890 (/lib/x86\_64-linux-gnu/libpthread-2.27.so+0x1288f)  

#4 0x7f37c02f8175 blink::MessagePort::MessagePort()  

#5 0x7f37c02f8001 blink::MessageChannel::MessageChannel()  

#6 0x7f37bcbc3125 blink::AudioWorkletNode::Create()  

#7 0x7f37bce4c465 blink::audio\_worklet\_node\_v8\_internal::ConstructorCallback()  

#8 0x7f37bd7f7182 v8::internal::FunctionCallbackArguments::Call()  

#9 0x7f37bd7f6215 v8::internal::(anonymous namespace)::HandleApiCallHelper<>()  

#10 0x7f37bd7f5b3f v8::internal::Builtin\_Impl\_HandleApiCall()  

#11 0x7f37bd6d11b8 Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit  

r8: 00003a702a1e2e50 r9: 0000000000000007 r10: 00003cbb143cf8a0 r11: 00007f37c02f80b0  

r12: 00002c1a005d2ac0 r13: 00003a702a0de6e8 r14: 0000000000000000 r15: 00002c1a005d3b48  

di: 00003a702a1e2e90 si: 0000000000000000 bp: 00007ffc5a50c280 bx: 00003a702a1e2e00  

dx: 000000005a50c201 ax: 00007f37c0a15e48 cx: 00007f37c0a15df8 sp: 00007ffc5a50c270  

ip: 00007f37c02f8175 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000004  

trp: 000000000000000e msk: 0000000000000000 cr2: 0000000000000000  

[end of stack trace]

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: David Manouchehri

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### da...@davidmanouchehri.com (2020-02-09)

The owner for this one would likely be @hongchan.

This bug is *extremely* similar to these tickets, which were both rated at Security_Severity-High.

https://bugs.chromium.org/p/chromium/issues/detail?id=977107
https://bugs.chromium.org/p/chromium/issues/detail?id=959700

### cl...@chromium.org (2020-02-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6239840602488832.

### ca...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### da...@davidmanouchehri.com (2020-02-10)

Could I see how the testcase for ClusterFuzz was written? I'm familiar with how to write simple V8 test cases, but I don't know how to do more complicated ones like this.

### cl...@chromium.org (2020-02-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Messaging Blink>WebAudio]

### cl...@chromium.org (2020-02-10)

ClusterFuzz testcase 6239840602488832 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2020-02-10)

Detailed Report: https://clusterfuzz.com/testcase?key=6239840602488832

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  blink::MessagePort::MessagePort
  blink::MessageChannel::MessageChannel
  blink::AudioWorkletNode::Create
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=739901

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6239840602488832

Additional requirements: Requires HTTP

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6239840602488832 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### da...@davidmanouchehri.com (2020-02-10)

[Comment Deleted]

### ca...@chromium.org (2020-02-10)

Re https://crbug.com/chromium/1050419#c4: multiple files can be zipped and uploaded as a zip to clusterfuzz, which will open index.html, or run poc.js.

### ca...@chromium.org (2020-02-10)

I was able to reproduce by running locally. hongchan, can you PTAL? Thanks. Triaging as high based on previous memory safety bugs in this code.

### ca...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ho...@chromium.org (2020-02-11)

Actually this also has implication on the broader subject: what would be the right behavior of BaseAudioContext when the associated ExecutionContext goes away? I think this is undefined and perhaps a problem that the spec needs to address.

Until then, I am fine with throwing an exception from the factory method. I'll write up a CL soon.

Thanks David!

### ho...@chromium.org (2020-02-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-02-12)

ClusterFuzz testcase 6239840602488832 appears to be flaky, updating reproducibility label.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2f1cdb3418f3645a50a7bd73e9aecd8040c75827

commit 2f1cdb3418f3645a50a7bd73e9aecd8040c75827
Author: Hongchan Choi <hongchan@chromium.org>
Date: Wed Feb 12 18:46:25 2020

Throw an exception when AudioWorkletNode is created on a destroyed ExecutionContext

The repro case creates an AudioWorkletNode after the ExecutionContext
goes away. (detached iframe) AudioWorkletNode is equipped with a
MessageChannel which requires a valid ExecutionContext.

AudioWorkletNode is not fully functional without message ports anyway,
so we can throw an exception in this case.

Test: Locally confirmed the ASAN build doesn't crash with the repro anymore.
Bug: 1050419
Change-Id: I52af9f877e2ad31923c6380dc0732eb6c97ab407
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2051386
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#740754}

[modify] https://crrev.com/2f1cdb3418f3645a50a7bd73e9aecd8040c75827/third_party/blink/renderer/modules/webaudio/audio_worklet_node.cc


### ho...@chromium.org (2020-02-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-02-12)

Detailed Report: https://clusterfuzz.com/testcase?key=6239840602488832

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  blink::MessagePort::MessagePort
  blink::MessageChannel::MessageChannel
  blink::AudioWorkletNode::Create
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=739901

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6239840602488832

Additional requirements: Requires HTTP

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6239840602488832 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2020-02-13)

Detailed Report: https://clusterfuzz.com/testcase?key=6239840602488832

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  blink::MessagePort::MessagePort
  blink::MessageChannel::MessageChannel
  blink::AudioWorkletNode::Create
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=739901

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6239840602488832

Additional requirements: Requires HTTP

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6239840602488832 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### da...@davidmanouchehri.com (2020-02-13)

[Comment Deleted]

### ho...@chromium.org (2020-02-13)

I think this is "sort of" verified by CF. Now it says not reproducible at all. The case was reliably reproducible before rev 739901 and the patch is at 740754.

### [Deleted User] (2020-02-15)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-15)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-18)

[Empty comment from Monorail migration]

### mm...@google.com (2020-02-18)

hongchan@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

p.s.
I know that you've submitted a few of those recently. If this issue is of the similar nature as the previous ones, please feel free to skip submitting the form this time :)

### mm...@google.com (2020-02-18)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-20)

Congrats! The Panel decided to award $7,500 for this report! Nice one! 

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### da...@davidmanouchehri.com (2020-03-05)

Awesome! Is there a CVE assigned yet?

### [Deleted User] (2020-05-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-05-20)

This issue was migrated from crbug.com/chromium/1050419?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Messaging, Blink>WebAudio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051473)*
