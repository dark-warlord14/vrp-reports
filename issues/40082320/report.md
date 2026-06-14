# Heap-use-after-free in WebLocalFrameImpl::printBegin

| Field | Value |
|-------|-------|
| **Issue ID** | [40082320](https://issues.chromium.org/issues/40082320) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Printing |
| **Platforms** | Linux, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2015-06-20 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

Use after free bug happens in WebLocalFrameImpl::printBegin of WebKit/Source/web/WebLocalFrameImpl.cpp file.  

You have to open attached print.pdf file in a pdf editor to view javascript code which cause this bug.

Document Javascript section of print.pdf file has this code.  

function printDoc()  

{  

this.print(true);  

}  

app.setTimeOut('printDoc()',3000);

"Document Will Print" Document Action of print.pdf file has this code.  

app.alert('Press Ok or press escape key',3);

SIMILAR BUG  

<https://crbug.com/chromium/159165>

**VERSION**

Chrome Version: [45.0.2437.0] + [trunk build]  

[44.0.2403.52] + [beta]  

[43.0.2357.125] + [stable]  

\* Does not crash in official stable version for linux.  

But does crash with asan release for same version.  

<https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-stable-43.0.2357.125.zip?generation=1434714233401000&alt=media>

Operating System:

Ubuntu 14.04 (64 bit)  

Windows 8.1 (64 bit)

**REPRODUCTION CASE**

1. Open print.pdf with chrome.
2. Chrome will display print preview page and an alert dialog in 3 seconds.
3. Press OK on alert dialog or press escape key.  
   
   Mimehandler process for pdf will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [Mimehandler process for pdf]  

Crash State: Address sanitizer output

AddressSanitizer: heap-use-after-free on address 0x60c00007e35c at pc 0x7fef84eb1f24 bp 0x7fff53c0d170 sp 0x7fff53c0d168  

READ of size 4 at 0x60c00007e35c thread T0 (chrome)  

#0 0x7fef84eb1f23 in size third\_party/WebKit/Source/wtf/Vector.h:694:38  

#1 0x7fef84eb1f23 in WTF::Vector<blink::IntRect, 0ul, WTF::DefaultAllocator>::fill(blink::IntRect const&, unsigned long) third\_party/WebKit/Source/wtf/Vector.h:932:0  

#2 0x7fef84eb1149 in blink::ChromePluginPrintContext::computePageRects(blink::FloatRect const&, float, float, float, float&) third\_party/WebKit/Source/web/WebLocalFrameImpl.cpp:511:9  

#3 0x7fef84ea2741 in blink::WebLocalFrameImpl::printBegin(blink::WebPrintParams const&, blink::WebNode const&) third\_party/WebKit/Source/web/WebLocalFrameImpl.cpp:1398:5  

#4 0x7fef8c57b730 in printing::PrepareFrameAndViewForPrint::PrepareFrameAndViewForPrint(PrintMsg\_Print\_Params const&, blink::WebLocalFrame\*, blink::WebNode const&, bool) components/printing/renderer/print\_web\_view\_helper.cc:650:5  

#5 0x7fef8c585d5f in printing::PrintWebViewHelper::PrepareFrameForPreviewDocument() components/printing/renderer/print\_web\_view\_helper.cc:1100:30  

#6 0x7fef8c581e9c in printing::PrintWebViewHelper::OnPrintPreview(base::DictionaryValue const&) components/printing/renderer/print\_web\_view\_helper.cc:1081:3  

#7 0x7fef8c58118c in DispatchToMethodImpl<printing::PrintWebViewHelper, void (printing::PrintWebViewHelper::\*)(const base::DictionaryValue &), base::DictionaryValue, 0> base/tuple.h:254:3  

#8 0x7fef8c58118c in DispatchToMethod<printing::PrintWebViewHelper, void (printing::PrintWebViewHelper::\*)(const base::DictionaryValue &), base::DictionaryValue> base/tuple.h:261:0  

#9 0x7fef8c58118c in Dispatch<printing::PrintWebViewHelper, printing::PrintWebViewHelper, void, void (printing::PrintWebViewHelper::\*)(const base::DictionaryValue &)> components/printing/common/print\_messages.h:343:0  

#10 0x7fef8c58118c in printing::PrintWebViewHelper::OnMessageReceived(IPC::Message const&) components/printing/renderer/print\_web\_view\_helper.cc:894:0  

#11 0x7fef8a367973 in content::RenderViewImpl::OnMessageReceived(IPC::Message const&) content/renderer/render\_view\_impl.cc:1289:9  

#12 0x7fef8d397237 in content::MessageRouter::RouteMessage(IPC::Message const&) content/common/message\_router.cc:54:3  

#13 0x7fef8d39705c in content::MessageRouter::OnMessageReceived(IPC::Message const&) content/common/message\_router.cc:46:10  

#14 0x7fef8a1b1a09 in content::ChildThreadImpl::OnMessageReceived(IPC::Message const&) content/child/child\_thread\_impl.cc:612:10  

#15 0x7fef82f3446d in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc\_channel\_proxy.cc:294:3  

#16 0x7fef81b2da17 in Run base/callback.h:396:12  

#17 0x7fef81b2da17 in base::debug::TaskAnnotator::RunTask(char const\*, char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:62:0  

#18 0x7fef8a2d749b in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(unsigned long, bool, base::PendingTask\*) components/scheduler/child/task\_queue\_manager.cc:690:5  

#19 0x7fef8a2d5842 in scheduler::TaskQueueManager::DoWork(bool) components/scheduler/child/task\_queue\_manager.cc:643:9  

#20 0x7fef81b2da17 in Run base/callback.h:396:12  

#21 0x7fef81b2da17 in base::debug::TaskAnnotator::RunTask(char const\*, char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:62:0  

#22 0x7fef81a4952f in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:458:3  

#23 0x7fef81a4a564 in DeferOrRunPendingTask base/message\_loop/message\_loop.cc:468:5  

#24 0x7fef81a4a564 in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:580:0  

#25 0x7fef81a50a90 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:34:21  

#26 0x7fef81a798e8 in base::RunLoop::Run() base/run\_loop.cc:55:3  

#27 0x7fef81a47e4e in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:286:3  

#28 0x7fef8a3c8c9d in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:220:7  

#29 0x7fef8196e4c3 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:307:14  

#30 0x7fef8197034d in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:802:12  

#31 0x7fef8196da7a in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:15  

#32 0x7fef80c27ef2 in ChromeMain chrome/app/chrome\_main.cc:66:12  

#33 0x7fef76492ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287:0

0x60c00007e35c is located 28 bytes inside of 128-byte region [0x60c00007e340,0x60c00007e3c0)  

freed by thread T0 (chrome) here:  

#0 0x7fef80c2751b in operator delete(void\*) ??:0:0  

#1 0x7fef84ea25d6 in deletePtr third\_party/WebKit/Source/wtf/OwnPtrCommon.h:52:9  

#2 0x7fef84ea25d6 in operator= third\_party/WebKit/Source/wtf/OwnPtr.h:146:0  

#3 0x7fef84ea25d6 in blink::WebLocalFrameImpl::printBegin(blink::WebPrintParams const&, blink::WebNode const&) third\_party/WebKit/Source/web/WebLocalFrameImpl.cpp:1391:0  

#4 0x7fef8c57b730 in printing::PrepareFrameAndViewForPrint::PrepareFrameAndViewForPrint(PrintMsg\_Print\_Params const&, blink::WebLocalFrame\*, blink::WebNode const&, bool) components/printing/renderer/print\_web\_view\_helper.cc:650:5  

#5 0x7fef8c585d5f in printing::PrintWebViewHelper::PrepareFrameForPreviewDocument() components/printing/renderer/print\_web\_view\_helper.cc:1100:30  

#6 0x7fef8c581e9c in printing::PrintWebViewHelper::OnPrintPreview(base::DictionaryValue const&) components/printing/renderer/print\_web\_view\_helper.cc:1081:3  

#7 0x7fef8c58118c in DispatchToMethodImpl<printing::PrintWebViewHelper, void (printing::PrintWebViewHelper::\*)(const base::DictionaryValue &), base::DictionaryValue, 0> base/tuple.h:254:3  

#8 0x7fef8c58118c in DispatchToMethod<printing::PrintWebViewHelper, void (printing::PrintWebViewHelper::\*)(const base::DictionaryValue &), base::DictionaryValue> base/tuple.h:261:0  

#9 0x7fef8c58118c in Dispatch<printing::PrintWebViewHelper, printing::PrintWebViewHelper, void, void (printing::PrintWebViewHelper::\*)(const base::DictionaryValue &)> components/printing/common/print\_messages.h:343:0  

#10 0x7fef8c58118c in printing::PrintWebViewHelper::OnMessageReceived(IPC::Message const&) components/printing/renderer/print\_web\_view\_helper.cc:894:0  

#11 0x7fef8a367973 in content::RenderViewImpl::OnMessageReceived(IPC::Message const&) content/renderer/render\_view\_impl.cc:1289:9  

#12 0x7fef8d397237 in content::MessageRouter::RouteMessage(IPC::Message const&) content/common/message\_router.cc:54:3  

#13 0x7fef8d39705c in content::MessageRouter::OnMessageReceived(IPC::Message const&) content/common/message\_router.cc:46:10  

#14 0x7fef8a1b1a09 in content::ChildThreadImpl::OnMessageReceived(IPC::Message const&) content/child/child\_thread\_impl.cc:612:10  

#15 0x7fef82f3446d in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc\_channel\_proxy.cc:294:3  

#16 0x7fef81b2da17 in Run base/callback.h:396:12  

#17 0x7fef81b2da17 in base::debug::TaskAnnotator::RunTask(char const\*, char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:62:0  

#18 0x7fef8a2d749b in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(unsigned long, bool, base::PendingTask\*) components/scheduler/child/task\_queue\_manager.cc:690:5  

#19 0x7fef8a2d5842 in scheduler::TaskQueueManager::DoWork(bool) components/scheduler/child/task\_queue\_manager.cc:643:9  

#20 0x7fef81b2da17 in Run base/callback.h:396:12  

#21 0x7fef81b2da17 in base::debug::TaskAnnotator::RunTask(char const\*, char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:62:0  

#22 0x7fef81a4952f in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:458:3  

#23 0x7fef81a4a564 in DeferOrRunPendingTask base/message\_loop/message\_loop.cc:468:5  

#24 0x7fef81a4a564 in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:580:0  

#25 0x7fef81a50a90 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:34:21  

#26 0x7fef81a798e8 in base::RunLoop::Run() base/run\_loop.cc:55:3  

#27 0x7fef81a47e4e in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:286:3  

#28 0x7fef82f4922e in IPC::SyncChannel::WaitForReplyWithNestedMessageLoop(IPC::SyncChannel::SyncContext\*) ipc/ipc\_sync\_channel.cc:555:5  

#29 0x7fef82f48dd3 in IPC::SyncChannel::WaitForReply(IPC::SyncChannel::SyncContext\*, base::WaitableEvent\*) ipc/ipc\_sync\_channel.cc:520:7  

#30 0x7fef82f48568 in IPC::SyncChannel::Send(IPC::Message\*) ipc/ipc\_sync\_channel.cc:494:3  

#31 0x7fef8a1b0c14 in content::ChildThreadImpl::Send(IPC::Message\*) content/child/child\_thread\_impl.cc:510:10  

#32 0x7fef8a346c48 in content::RenderThreadImpl::Send(IPC::Message\*) content/renderer/render\_thread\_impl.cc:859:13  

#33 0x7fef8a3a534f in content::RenderWidget::Send(IPC::Message\*) content/renderer/render\_widget.cc:754:10  

#34 0x7fef8a3004a1 in content::RenderFrameImpl::RunJavaScriptMessage(content::JavaScriptMessageType, std::\_\_1::basic\_string<unsigned short, base::string16\_char\_traits, std::\_\_1::allocator<unsigned short> > const&, std::\_\_1::basic\_string<unsigned short, base::string16\_char\_traits, std::\_\_1::allocator<unsigned short> > const&, GURL const&, std::\_\_1::basic\_string<unsigned short, base::string16\_char\_traits, std::\_\_1::allocator<unsigned short> >\*) content/renderer/render\_frame\_impl.cc:1721:3  

#35 0x7fef8a31d1a2 in content::RenderFrameImpl::runModalAlertDialog(blink::WebString const&) content/renderer/render\_frame\_impl.cc:2968:3  

#36 0x7fef84f23893 in blink::ChromeClientImpl::openJavaScriptAlertDelegate(blink::LocalFrame\*, WTF::String const&) third\_party/WebKit/Source/web/ChromeClientImpl.cpp:418:9  

#37 0x7fef86c61e99 in bool blink::openJavaScriptDialog<>(blink::ChromeClient\*, bool (blink::ChromeClient::\*)(blink::LocalFrame\*, WTF::String const&), blink::LocalFrame&, WTF::String const&, blink::ChromeClient::DialogType) third\_party/WebKit/Source/core/page/ChromeClient.cpp:95:19

previously allocated by thread T0 (chrome) here:  

#0 0x7fef80c26f5b in operator new(unsigned long) ??:0:0  

#1 0x7fef84ea23ed in blink::WebLocalFrameImpl::printBegin(blink::WebPrintParams const&, blink::WebNode const&) third\_party/WebKit/Source/web/WebLocalFrameImpl.cpp:1389:45  

#2 0x7fef8c57b730 in printing::PrepareFrameAndViewForPrint::PrepareFrameAndViewForPrint(PrintMsg\_Print\_Params const&, blink::WebLocalFrame\*, blink::WebNode const&, bool) components/printing/renderer/print\_web\_view\_helper.cc:650:5  

#3 0x7fef8c585d5f in printing::PrintWebViewHelper::PrepareFrameForPreviewDocument() components/printing/renderer/print\_web\_view\_helper.cc:1100:30  

#4 0x7fef8c581e9c in printing::PrintWebViewHelper::OnPrintPreview(base::DictionaryValue const&) components/printing/renderer/print\_web\_view\_helper.cc:1081:3  

#5 0x7fef8c58118c in DispatchToMethodImpl<printing::PrintWebViewHelper, void (printing::PrintWebViewHelper::\*)(const base::DictionaryValue &), base::DictionaryValue, 0> base/tuple.h:254:3  

#6 0x7fef8c58118c in DispatchToMethod<printing::PrintWebViewHelper, void (printing::PrintWebViewHelper::\*)(const base::DictionaryValue &), base::DictionaryValue> base/tuple.h:261:0  

#7 0x7fef8c58118c in Dispatch<printing::PrintWebViewHelper, printing::PrintWebViewHelper, void, void (printing::PrintWebViewHelper::\*)(const base::DictionaryValue &)> components/printing/common/print\_messages.h:343:0  

#8 0x7fef8c58118c in printing::PrintWebViewHelper::OnMessageReceived(IPC::Message const&) components/printing/renderer/print\_web\_view\_helper.cc:894:0  

#9 0x7fef8a367973 in content::RenderViewImpl::OnMessageReceived(IPC::Message const&) content/renderer/render\_view\_impl.cc:1289:9  

#10 0x7fef8d397237 in content::MessageRouter::RouteMessage(IPC::Message const&) content/common/message\_router.cc:54:3  

#11 0x7fef8d39705c in content::MessageRouter::OnMessageReceived(IPC::Message const&) content/common/message\_router.cc:46:10  

#12 0x7fef8a1b1a09 in content::ChildThreadImpl::OnMessageReceived(IPC::Message const&) content/child/child\_thread\_impl.cc:612:10  

#13 0x7fef82f3446d in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc\_channel\_proxy.cc:294:3  

#14 0x7fef81b2da17 in Run base/callback.h:396:12  

#15 0x7fef81b2da17 in base::debug::TaskAnnotator::RunTask(char const\*, char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:62:0  

#16 0x7fef8a2d749b in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(unsigned long, bool, base::PendingTask\*) components/scheduler/child/task\_queue\_manager.cc:690:5  

#17 0x7fef8a2d5842 in scheduler::TaskQueueManager::DoWork(bool) components/scheduler/child/task\_queue\_manager.cc:643:9  

#18 0x7fef81b2da17 in Run base/callback.h:396:12  

#19 0x7fef81b2da17 in base::debug::TaskAnnotator::RunTask(char const\*, char const\*, base::PendingTask const&) base/debug/task\_annotator.cc:62:0  

#20 0x7fef81a4952f in base::MessageLoop::RunTask(base::PendingTask const&) base/message\_loop/message\_loop.cc:458:3  

#21 0x7fef81a4a564 in DeferOrRunPendingTask base/message\_loop/message\_loop.cc:468:5  

#22 0x7fef81a4a564 in base::MessageLoop::DoWork() base/message\_loop/message\_loop.cc:580:0  

#23 0x7fef81a50a90 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:34:21  

#24 0x7fef81a798e8 in base::RunLoop::Run() base/run\_loop.cc:55:3  

#25 0x7fef81a47e4e in base::MessageLoop::Run() base/message\_loop/message\_loop.cc:286:3  

#26 0x7fef8a3c8c9d in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer\_main.cc:220:7  

#27 0x7fef8196e4c3 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) content/app/content\_main\_runner.cc:307:14  

#28 0x7fef8197034d in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:802:12  

#29 0x7fef8196da7a in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:15  

#30 0x7fef80c27ef2 in ChromeMain chrome/app/chrome\_main.cc:66:12  

#31 0x7fef76492ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/chamal/chrome/src/out/Release/chrome+0x6875f23)  

Shadow bytes around the buggy address:  

0x0c1880007c10: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c1880007c20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1880007c30: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c1880007c40: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c1880007c50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c1880007c60: fa fa fa fa fa fa fa fa fd fd fd[fd]fd fd fd fd  

0x0c1880007c70: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c1880007c80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c1880007c90: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c1880007ca0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x0c1880007cb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

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

## Attachments

- [print.pdf](attachments/print.pdf) (application/pdf, 1.1 KB)
- [print.pdf](attachments/print_52997078.pdf) (application/pdf, 1.1 KB)
- [print.html](attachments/print.html) (text/html, 149 B)

## Timeline

### cl...@chromium.org (2015-06-22)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5015665595908096

### es...@chromium.org (2015-06-22)

I'm not able to reproduce this. chamal.desilva, is there any more information you can provide? Have you tried on a tip-of-tree ASAN build?

Also adding a couple people who might be able to help. 

### ch...@gmail.com (2015-06-22)

I can reproduce on tip-of-tree ASAN.
version: 45.0.2438.0 (64-bit).

1. Did the test case reach step 2 in reproduction steps mentioned in issue report?

2. Would you be able to provide a link to the chrome version that you are testing?
So I can download it to my PC and test.

### dg...@chromium.org (2015-06-22)

I'm not sure who is the right person to assign it to. dsinclair@, can you triage please?

### es...@chromium.org (2015-06-22)

Re #3, yes, I pressed "Ok" on the alert dialog. I tested on https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-symbolized-linux-release-335186.zip?generation=1434687657321000&alt=media

### es...@chromium.org (2015-06-22)

[Empty comment from Monorail migration]

### es...@chromium.org (2015-06-22)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-06-23)

Reproduces in my PC with chrome downloaded from link mentioned in #5.

### ch...@gmail.com (2015-06-23)

Attached a test case which does not need any user interaction.

OS: Ubuntu 14.04
 
1. Download print.html and print.pdf.
2. Copy them to same folder of local web server.
3. Open asan build of chrome in a terminal.
4. Open print.html with chrome.
5. Chrome will display print preview page and an alert dialog in 3 seconds.
   Don't press OK button of alert dialog.
6. Page will be redirected to http://127.0.0.1 in after 6 seconds.
7. You will not see anything crashing.
   But asan output for crash will be displayed in terminal.

### es...@chromium.org (2015-06-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-23)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5687111389282304

### cl...@chromium.org (2015-06-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-26)

[Empty comment from Monorail migration]

### jw...@chromium.org (2015-06-28)

I've assigned to dsinclair to triage.

### jw...@chromium.org (2015-06-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-28)

[Empty comment from Monorail migration]

### ds...@chromium.org (2015-06-29)

eae@ for triage. It looks like it's crashing in printing code, who would be the right person to deal with printing?

### jw...@chromium.org (2015-06-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-07-01)

vitalybuka@ is our printing expert, can you please take a look.

### vi...@chromium.org (2015-07-03)

Can't reproduce too. Not sure what to do with this.

Everything happens inside of single call to blink::WebLocalFrameImpl::printBegin. Calling printing code has no control over this. Maybe pluggin/webkit layer.

### ch...@gmail.com (2015-07-03)

Did this issue reproduce in jww's machine or this issue does not reproduce in all machines?


### vi...@chromium.org (2015-07-03)

I tried only my Ubuntu workstation.

### jw...@chromium.org (2015-07-06)

No, I was not able to repro, which is why I assigned for triage.

### ch...@gmail.com (2015-07-06)

Is it possible to cc this bug to tsepez? He might be able to help because he has fixed this similar https://crbug.com/chromium/159165.

### vi...@chromium.org (2015-07-06)

https://crbug.com/chromium/159165 looks very different to me

### ch...@gmail.com (2015-07-06)

This issue does not reproduce if destination is set to "Save as PDF" in print preview options of chrome. I am sorry I did not notice this because I have a printer attached to my PC and it's set as destination.

New Steps
---------

1. Open Printer settings window of your OS. I tested this only on Ubuntu 14.04.
2. Add a printer and make it default.
3. Open chrome with a clean user data directory. So chrome will pick newly added printer as default.
   chrome --user-data-dir=/pathto/clean_directory
6. Open print.pdf with chrome.(print.pdf is attached in issue report)
7. Chrome will display print preview page and an alert dialog in 3 seconds.
   At this point chrome should display destination as newly added printer.
7. Press OK on alert dialog or press escape key.
   Mimehandler process for pdf will crash.



### in...@chromium.org (2015-07-06)

vitalybuka@, can you please take a look based on c#26.

### vi...@chromium.org (2015-07-08)

Thanks, can reproduce with selected printer.
It's a regression:
https://chromium.googlesource.com/chromium/src/+log/5fb2ffe4b404d28242d8f62fcfa6c0c1bdaddc4f..0fe1057d8ccd0378b615308d4f74f130812a9178

### vi...@chromium.org (2015-07-08)

For this document it started after http:://codereview.chromium.org/981843003


### vi...@chromium.org (2015-07-08)

[Empty comment from Monorail migration]

### vi...@chromium.org (2015-07-08)

Fixing typo in URL: http://codereview.chromium.org/981843003

### bu...@chromium.org (2015-07-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8fa5a358cb32085b51daf92df8fd4a79b3931f81

commit 8fa5a358cb32085b51daf92df8fd4a79b3931f81
Author: vitalybuka <vitalybuka@chromium.org>
Date: Thu Jul 09 18:45:44 2015

Crash on nested IPC handlers in PrintWebViewHelper

Class is not designed to handle nested IPC. Regular flows also does not
expect them. Still during printing of plugging them may show message
boxes and start nested message loops.
For now we are going just crash. If stats show us that this case is
frequent we will have to do something more complicated.

BUG=502562

Review URL: https://codereview.chromium.org/1228693002

Cr-Commit-Position: refs/heads/master@{#338100}

[modify] http://crrev.com/8fa5a358cb32085b51daf92df8fd4a79b3931f81/components/printing/renderer/print_web_view_helper.cc
[modify] http://crrev.com/8fa5a358cb32085b51daf92df8fd4a79b3931f81/components/printing/renderer/print_web_view_helper.h


### in...@chromium.org (2015-07-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### mb...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### vi...@chromium.org (2015-07-16)

[Empty comment from Monorail migration]

### pe...@google.com (2015-07-16)

[Automated comment] Less than 2 weeks to go before stable on M44, manual review required.

### ke...@google.com (2015-07-17)

What OS is this for? Please add a label.

### pe...@chromium.org (2015-07-17)

Please merge to M-44 branch 2403 soon.  Will be in next stable refresh.

### pe...@chromium.org (2015-07-18)

Please finish the merge to M44 in the next 5 days to be part of the next stable refresh.

+inferno to make sure it happens.

### pe...@chromium.org (2015-07-23)

bump.  finish merge please.

### vi...@chromium.org (2015-07-23)

merging

### bu...@chromium.org (2015-07-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ae840a4a8cb747df6459e90d8a6d0d0442b68df3

commit ae840a4a8cb747df6459e90d8a6d0d0442b68df3
Author: Vitaly Buka <vitalybuka@chromium.org>
Date: Thu Jul 23 17:57:07 2015

Merge: Crash on nested IPC handlers in PrintWebViewHelper

Class is not designed to handle nested IPC. Regular flows also does not
expect them. Still during printing of plugging them may show message
boxes and start nested message loops.
For now we are going just crash. If stats show us that this case is
frequent we will have to do something more complicated.

BUG=502562

Review URL: https://codereview.chromium.org/1228693002

Cr-Commit-Position: refs/heads/master@{#338100}
(cherry picked from commit 8fa5a358cb32085b51daf92df8fd4a79b3931f81)

Review URL: https://codereview.chromium.org/1246673005 .

Cr-Commit-Position: refs/branch-heads/2403@{#549}
Cr-Branched-From: f54b8097a9c45ed4ad308133d49f05325d6c5070-refs/heads/master@{#330231}

[modify] http://crrev.com/ae840a4a8cb747df6459e90d8a6d0d0442b68df3/components/printing/renderer/print_web_view_helper.cc
[modify] http://crrev.com/ae840a4a8cb747df6459e90d8a6d0d0442b68df3/components/printing/renderer/print_web_view_helper.h


### ti...@google.com (2015-08-31)

Adding Release-0-M45 to make sure this goes out in the M45 release notes, even though it looks like it shipped earlier.

### ti...@google.com (2015-08-31)

Congrats - $3,000 for this report. 

We'll credit you in the release notes as anonymous, though note that this report will become publicly accessible. If you want this report to not become public in the future, please let me know.

I'll start payment this week, so you should have the reward in 2-3 weeks from today.

Any questions, please either update the bug or reach out to me at timwillis@

### ti...@google.com (2015-09-04)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-10-15)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/502562?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082320)*
