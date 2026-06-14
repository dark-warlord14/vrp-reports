# Heap-use-after-free in printing::PrintWebViewHelper::RenderPageContent

| Field | Value |
|-------|-------|
| **Issue ID** | [40087233](https://issues.chromium.org/issues/40087233) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Printing |
| **Platforms** | Linux, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2017-04-02 |
| **Bounty** | $3,000.00 |

## Description

Chrome Version: 59.0.3059.0 canary + stable
Operating System: Windows 7

Stack traces WinDBG:
 
00000000`0026cce0 000007fe`ee94702f chrome_child!printing::PrintWebViewHelper::PrintPageInternal+0x20a [c:\b\build\slave\win64-pgo\build\src\components\printing\renderer\print_web_view_helper.cc @ 1917]
00000000`0026cdd0 000007fe`ee944382 chrome_child!printing::PrintWebViewHelper::RenderPreviewPage+0xc3 [c:\b\build\slave\win64-pgo\build\src\components\printing\renderer\print_web_view_helper.cc @ 1337]
00000000`0026cf10 000007fe`ee94575e chrome_child!printing::PrintWebViewHelper::CreatePreviewDocument+0x326 [c:\b\build\slave\win64-pgo\build\src\components\printing\renderer\print_web_view_helper.cc @ 1293]
00000000`0026d030 000007fe`ee943e26 chrome_child!printing::PrintWebViewHelper::OnFramePreparedForPreviewDocument+0x1e [c:\b\build\slave\win64-pgo\build\src\components\printing\renderer\print_web_view_helper.cc @ 1216]
00000000`0026d060 000007fe`ee945fdd chrome_child!printing::PrepareFrameAndViewForPrint::CopySelectionIfNeeded+0x3e [c:\b\build\slave\win64-pgo\build\src\components\printing\renderer\print_web_view_helper.cc @ 793]
00000000`0026d090 000007fe`ee945d06 chrome_child!printing::PrintWebViewHelper::PrepareFrameForPreviewDocument+0x109 [c:\b\build\slave\win64-pgo\build\src\components\printing\renderer\print_web_view_helper.cc @ 1205]
00000000`0026d0f0 000007fe`ee942bb9 chrome_child!printing::PrintWebViewHelper::OnPrintPreview+0x1d6 [c:\b\build\slave\win64-pgo\build\src\components\printing\renderer\print_web_view_helper.cc @ 1184]
00000000`0026d190 000007fe`ed6cd216 chrome_child!IPC::MessageT<PrintMsg_PrintPreview_Meta,std::tuple<base::DictionaryValue>,void>::Dispatch<printing::PrintWebViewHelper,printing::PrintWebViewHelper,void,void (__cdecl printing::PrintWebViewHelper::*)(base::DictionaryValue const & __ptr64) __ptr64>+0xbd [c:\b\build\slave\win64-pgo\build\src\ipc\ipc_message_templates.h @ 121]
00000000`0026d260 000007fe`ecc39791 chrome_child!printing::PrintWebViewHelper::OnMessageReceived+0x58f202 [c:\b\build\slave\win64-pgo\build\src\components\printing\renderer\print_web_view_helper.cc @ 1005]
00000000`0026d300 000007fe`ecc380aa chrome_child!content::RenderFrameImpl::OnMessageReceived+0x101 [c:\b\build\slave\win64-pgo\build\src\content\renderer\render_frame_impl.cc @ 1492]
00000000`0026d4b0 000007fe`ecc37f88 chrome_child!content::ChildThreadImpl::OnMessageReceived+0xaa [c:\b\build\slave\win64-pgo\build\src\content\child\child_thread_impl.cc @ 751]
00000000`0026d540 000007fe`ecadd5bb chrome_child!IPC::ChannelProxy::Context::OnDispatchMessage+0x28 [c:\b\build\slave\win64-pgo\build\src\ipc\ipc_channel_proxy.cc @ 330]
00000000`0026d570 000007fe`ecae0625 chrome_child!base::debug::TaskAnnotator::RunTask+0x1eb [c:\b\build\slave\win64-pgo\build\src\base\debug\task_annotator.cc @ 52]
00000000`0026d6d0 000007fe`ecada466 chrome_child!blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue+0x269 [c:\b\build\slave\win64-pgo\build\src\third_party\webkit\source\platform\scheduler\base\task_queue_manager.cc @ 380]
00000000`0026d960 000007fe`ed0bde77 chrome_child!blink::scheduler::TaskQueueManager::DoWork+0xfe [c:\b\build\slave\win64-pgo\build\src\third_party\webkit\source\platform\scheduler\base\task_queue_manager.cc @ 245]
00000000`0026dad0 000007fe`ecadd5bb chrome_child!base::internal::Invoker<base::internal::BindState<void (__cdecl blink::scheduler::TaskQueueManager::*)(base::TimeTicks,bool) __ptr64,base::WeakPtr<blink::scheduler::TaskQueueManager>,base::TimeTicks,bool>,void __cdecl(void)>::Run+0x4f [c:\b\build\slave\win64-pgo\build\src\base\bind_internal.h @ 343]
00000000`0026db10 000007fe`ecae0194 chrome_child!base::debug::TaskAnnotator::RunTask+0x1eb [c:\b\build\slave\win64-pgo\build\src\base\debug\task_annotator.cc @ 52]
00000000`0026dc70 000007fe`ecaddb20 chrome_child!base::MessageLoop::RunTask+0xb8 [c:\b\build\slave\win64-pgo\build\src\base\message_loop\message_loop.cc @ 422]
00000000`0026dd90 000007fe`ecadc37f chrome_child!base::MessageLoop::DoWork+0x194 [c:\b\build\slave\win64-pgo\build\src\base\message_loop\message_loop.cc @ 523]


## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 210 B)
- [heap-use-after-free on address 0x0113ecd4.txt](attachments/heap-use-after-free on address 0x0113ecd4.txt) (text/plain, 19.0 KB)

## Timeline

### do...@chromium.org (2017-04-03)

Do you have a crash ID?

thestig, do you mind having a look and triaging further? Thanks!

[Monorail components: Internals>Printing]

### ch...@gmail.com (2017-04-03)

[Comment Deleted]

### ch...@gmail.com (2017-04-03)

[Comment Deleted]

### sh...@chromium.org (2017-04-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-03)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2017-04-03)

Crash/e9b6438ee0000000.

### th...@chromium.org (2017-04-04)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-04-07)

Actually, it's print preview's fault. Repros on Linux too.

### cl...@chromium.org (2017-04-07)

Detailed report: https://clusterfuzz.com/testcase?key=6319911212417024

Job Type: mac_asan_chrome
Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6130000c1570
Crash State:
  printing::PrintWebViewHelper::RenderPageContent
  printing::PrintWebViewHelper::RenderPage
  printing::PrintWebViewHelper::RenderPreviewPage
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Reproducer Testcase: https://clusterfuzz.com/download/AMIfv95ecus9z4ljcDVcpOf94a8rs7ijeTwYmfhyz-_AGWwufEw7Yyx0SdGpyC0OSiNsfrky8eSlFwNJSI-KxzdQitn4LkVBdEhADleE-4k4c2c0BVxbhAZ_xkugEbjTKem5fDl7LsW0OKtAnv9UUgfc0aW8CYh3XVYE_ODaHHyEHKlPyu6TTd8lxELMxuZYjyZ6gNrVv4ScMvyDy9NTcHTj8OnpQJL-Nd56CmCykLx4QhdexK3LApEpOAYfhoEGWHT8Lgvqa2LxxcIFXEwzmXb6UPUk0UQOjfpYUGDNF_xvVoMj6vOypRAtvKA4YwZAl-XiW579ES8A0knnHlYd7csJVbd2CNd3I9NxhbYkN5M4nSDYm3mA-E4?testcase_id=6319911212417024


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2017-04-07)

Detailed report: https://clusterfuzz.com/testcase?key=6319911212417024

Job Type: mac_asan_chrome
Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6130000b33b0
Crash State:
  printing::PrintWebViewHelper::RenderPageContent
  printing::PrintWebViewHelper::RenderPage
  printing::PrintWebViewHelper::RenderPreviewPage
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=mac_asan_chrome&range=455700:456019

Reproducer Testcase: https://clusterfuzz.com/download/AMIfv94Rs2NLvzXotzI3yVs90kRYp5pruZNlsE4BPt52-U5CrDXoi1bVQapZ3SvorAsKsy7Fi0L4ouCcxxKV5WsF4WWBkDLR2PjxRqmT264ATBdAYvAAn6xyEQiS9tglKuwyTGnjE-q_8XKIQCbbCsS4G-u4pWdV2Q-XqlgUC1u7GOdBF9SNibceHyHdEK2la7O2TcCTYZXpzSfmG7PLjQryM-NLOXwGrrdwhT1k_IQN5XsVEodkEUlyNZ763EazMuweBBEClsq4Kr5HHtmhTvYfVejuIxJP1ih5atdAk5xCA4J8mvPeli-4wyfB-L94pnF2CtQnCf-XR_M583tDD5reH3xdr7KHbvwvSdvp7bIeZbhOqLBG7fJcfnmjzFpD3UBDj7OcFm2s-XAdZHbaTyLbXwB3QV2YKg?testcase_id=6319911212417024


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### aw...@google.com (2017-04-07)

+enne@ per the clusterfuzz regression guess:

Author: enne
Project: chromium
Changelist: https://chromium.googlesource.com/chromium/src/+/d2501577f2df0764eda66614ddf429e230062562
Time: Thu Mar 09 19:59:17 2017
File pdf_metafile_skia.cc is changed in this cl (and is part of stack frame #5, "printing::PdfMetafileSkia::~PdfMetafileSkia"; frame #6, "~PdfMetafileSkia"; frame #7, "printing::PdfMetafileSkia::~PdfMetafileSkia")
File pdf_metafile_skia.cc is changed in this cl (and is part of stack frame #1, "PdfMetafileSkia"; frame #2, "printing::PdfMetafileSkia::PdfMetafileSkia")
Minimum distance from crash line to modified line: 53. (file: pdf_metafile_skia.cc, crashed on: 150, modified: 203).

### th...@chromium.org (2017-04-08)

Before r455840, the UAF still exists, just with a slightly different call stack. CF is probably confused by that.

### th...@chromium.org (2017-04-08)

Looking back, when PrintWebViewHelper was still a RenderViewObserver, this test case would have caused a NULL-dereference because some WebFrame pointer was NULL. Trying to fix that would result in a blank print preview. However, there would have been a renderer UAF eventually on shutdown if the older code avoided the NULL deref.

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-22)

thestig: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-04-25)

A friendly reminder that M59 Beta  launch is coming soon! Your bug is labelled as Release Block Beta. All fixes need to be merged into the release branch (3071) latest by tomorrow, 04/26 4:00 PM PT in order to make into the desktop Beta final build cut. Thank you!

### th...@chromium.org (2017-04-26)

Punting to stable.

### th...@chromium.org (2017-04-27)

https://codereview.chromium.org/2849483002/

### bu...@chromium.org (2017-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9c0e322c8de168b121cd6ae8cba92cd3214e5b1f

commit 9c0e322c8de168b121cd6ae8cba92cd3214e5b1f
Author: thestig <thestig@chromium.org>
Date: Fri Apr 28 01:45:05 2017

Defer deletion in PrintWebViewHelper while handling IPC messages.

Also calculate modifiability only once in PrintPreviewContext.
This does less repeated work, and prevents accessing frames after
their deletion.

BUG=707549

Review-Url: https://codereview.chromium.org/2849483002
Cr-Commit-Position: refs/heads/master@{#467810}

[modify] https://crrev.com/9c0e322c8de168b121cd6ae8cba92cd3214e5b1f/components/printing/renderer/print_web_view_helper.cc
[modify] https://crrev.com/9c0e322c8de168b121cd6ae8cba92cd3214e5b1f/components/printing/renderer/print_web_view_helper.h


### cl...@chromium.org (2017-04-28)

ClusterFuzz has detected this issue as fixed in range 467799:467817.

Detailed report: https://clusterfuzz.com/testcase?key=6319911212417024

Job Type: mac_asan_chrome
Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6130000b33b0
Crash State:
  printing::PrintWebViewHelper::RenderPageContent
  printing::PrintWebViewHelper::RenderPage
  printing::PrintWebViewHelper::RenderPreviewPage
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=mac_asan_chrome&range=455700:456019
Fixed: https://clusterfuzz.com/revisions?job=mac_asan_chrome&range=467799:467817

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6319911212417024


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-04-28)

ClusterFuzz testcase 6319911212417024 is verified as fixed, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-04-28)

Let's try for a M59 merge next week.

### ch...@gmail.com (2017-04-28)

Lei, could you please take a look at https://crbug.com/chromium/716474?

### sh...@chromium.org (2017-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-30)

Your change meets the bar and is auto-approved for M59. Please go ahead and merge the CL to branch 3071 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-05-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b6b5a52b378f25b3d7c917c119c1da28c4c2900b

commit b6b5a52b378f25b3d7c917c119c1da28c4c2900b
Author: Lei Zhang <thestig@chromium.org>
Date: Wed May 03 22:54:35 2017

M59: Defer deletion in PrintWebViewHelper while handling IPC messages.

Also calculate modifiability only once in PrintPreviewContext.
This does less repeated work, and prevents accessing frames after
their deletion.

BUG=707549

Review-Url: https://codereview.chromium.org/2849483002
Cr-Commit-Position: refs/heads/master@{#467810}
(cherry picked from commit 9c0e322c8de168b121cd6ae8cba92cd3214e5b1f)

Review-Url: https://codereview.chromium.org/2857313002 .
Cr-Commit-Position: refs/branch-heads/3071@{#385}
Cr-Branched-From: a106f0abbf69dad349d4aaf4bcc4f5d376dd2377-refs/heads/master@{#464641}

[modify] https://crrev.com/b6b5a52b378f25b3d7c917c119c1da28c4c2900b/components/printing/renderer/print_web_view_helper.cc
[modify] https://crrev.com/b6b5a52b378f25b3d7c917c119c1da28c4c2900b/components/printing/renderer/print_web_view_helper.h


### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### aw...@google.com (2017-05-05)

Very nice!  The panel decided to award $3,000 for this bug :-)

### aw...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-05-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-08-04)

This issue was migrated from crbug.com/chromium/707549?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/726680]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087233)*
