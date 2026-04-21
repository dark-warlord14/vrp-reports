# Security: UaF in printing::PrintRenderFrameHelper::PreviewPageRendered()

| Field | Value |
|-------|-------|
| **Issue ID** | [40053481](https://issues.chromium.org/issues/40053481) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Browser>PrintPreview |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2020-10-01 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4278.0 Safari/537.36

Steps to reproduce the problem:
1. Open the testcase

Received signal 11 SEGV_MAPERR ffffe541b001861b
#0 0x55555ac855f9 base::debug::CollectStackTrace()
#1 0x55555abfafe3 base::debug::StackTrace::StackTrace()
#2 0x55555ac8519b base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7ffff7fa73c0 (/usr/lib/x86_64-linux-gnu/libpthread-2.31.so+0x153bf)
#4 0x55555f3806a8 content::AXTreeSnapshotterImpl::SnapshotContentTree()
#5 0x55555f38057a content::AXTreeSnapshotterImpl::Snapshot()
#6 0x55555fb5fa1f printing::PrintRenderFrameHelper::PreviewPageRendered()
#7 0x55555fb5f2ff printing::PrintRenderFrameHelper::RenderPreviewPage()
#8 0x55555fb5e60a printing::PrintRenderFrameHelper::CreatePreviewDocument()
#9 0x55555fb5dcc5 printing::PrintRenderFrameHelper::OnFramePreparedForPreviewDocument()
#10 0x55555fb5d05c printing::PrintRenderFrameHelper::PrepareFrameForPreviewDocument()
#11 0x55555fb5c403 printing::PrintRenderFrameHelper::PrintPreview()
#12 0x55555901556a printing::mojom::PrintRenderFrameStubDispatch::Accept()
#13 0x55555b36f026 mojo::InterfaceEndpointClient::HandleValidatedMessage()
#14 0x55555b371e09 mojo::MessageDispatcher::Accept()
#15 0x55555ba13115 IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread()
#16 0x55555ba10a97 base::internal::Invoker<>::RunOnce()
#17 0x55555ac47586 base::TaskAnnotator::RunTask()
#18 0x55555ac585dd base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#19 0x55555ac582d8 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#20 0x55555ac0f45a base::MessagePumpDefault::Run()
#21 0x55555ac58c57 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#22 0x55555ac2f18e base::RunLoop::Run()
#23 0x55555ba15bdc IPC::SyncChannel::WaitForReplyWithNestedMessageLoop()
#24 0x55555ba15b09 IPC::SyncChannel::WaitForReply()
#25 0x55555ba15519 IPC::SyncChannel::Send()
#26 0x55555f3b9b38 content::RenderThreadImpl::Send()
#27 0x55555fb5b3ec printing::PrintRenderFrameHelper::RequestPrintPreview()
#28 0x55555fb5adb5 printing::PrintRenderFrameHelper::ScriptedPrint()
#29 0x55555f2f7016 content::RenderFrameImpl::ScriptedPrint()
#30 0x55555e9b613e blink::ChromeClient::Print()
#31 0x55555e937d15 blink::FrameLoader::DidFinishNavigation()
#32 0x55555e937b21 blink::FrameLoader::FinishedParsing()
#33 0x55555ddb75b3 blink::Document::FinishedParsing()
#34 0x55555e5da278 blink::HTMLDocumentParser::PrepareToStopParsing()
#35 0x55555e5dc7bf blink::HTMLDocumentParser::ProcessTokenizedChunkFromBackgroundParser()
#36 0x55555e5db625 blink::HTMLDocumentParser::PumpPendingSpeculations()
#37 0x55555e5db458 blink::HTMLDocumentParser::ResumeParsingAfterYield()
#38 0x55555a7a2a10 blink::TaskHandle::Runner::Run()
#39 0x55555ac47586 base::TaskAnnotator::RunTask()
#40 0x55555ac585dd base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#41 0x55555ac582d8 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#42 0x55555ac0f45a base::MessagePumpDefault::Run()
#43 0x55555ac58bfd base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#44 0x55555ac2f18e base::RunLoop::Run()
#45 0x55555faa1486 content::RendererMain()
#46 0x55555aba398a content::RunZygote()
#47 0x55555aba4c4c content::ContentMainRunnerImpl::Run()
#48 0x55555aba2076 content::RunContentProcess()
#49 0x55555aba2a5c content::ContentMain()
#50 0x5555583abaca ChromeMain
#51 0x7ffff67dc0b3 __libc_start_main
#52 0x5555583ab8ea _start

What is the expected behavior?
No Crash

What went wrong?
Crash

Did this work before? Yes 

Chrome version: 87.0.4278.0  Channel: canary
OS Version: OS X 10.12.6
Flash Version:

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 210 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 7.4 MB)

## Timeline

### ch...@gmail.com (2020-10-01)

This may be a regression from https://crrev.com/7195ad440cbf73df4003dc134551ecb19c24e26c.
 
Crash/c4ee674d282f4d4e.

### do...@chromium.org (2020-10-01)

[Empty comment from Monorail migration]

### do...@chromium.org (2020-10-01)

I can confirm an Aw Snap page, but the browser doesn't crash, so it appears to be a UaF in the renderer (aka Medium severity), not the browser process. Specifically, looks like [1], |render_frame_| is gone.

https://crrev.com/7195ad440cbf73df4003dc134551ecb19c24e26c was merged into M86 2 days ago on https://crbug.com/chromium/1122964. If that's the root cause, we might need to merge a fix on top of that ASAP. The crashes have started rolling in on Canary after that CL was landed, so it does seem pretty suspicious.

1. https://source.chromium.org/chromium/chromium/src/+/master:content/renderer/accessibility/render_accessibility_impl.cc;l=138?q=SnapshotContentTree&ss=chromium

[Monorail components: UI>Browser>PrintPreview]

### do...@chromium.org (2020-10-01)

+cc adetaylor FYI

### do...@chromium.org (2020-10-01)

[Empty comment from Monorail migration]

### th...@chromium.org (2020-10-01)

It's not my CL. I reverted it locally and the issue still repros. Bisecting...

### th...@chromium.org (2020-10-01)

Also, probably does not affect Android, as it doesn't have Print Preview.

### th...@chromium.org (2020-10-01)

Seeing how the stacktrace goes into AXTreeSnapshotterImpl code, it makes sense this bisects to https://chromium.googlesource.com/chromium/src/+log/1b9debd6..f10aedf3 and is due to r806069. I forget what the launch status is, but it affects users on Stable.

### th...@chromium.org (2020-10-01)

Well, I have a proposed fix. https://chromium-review.googlesource.com/2442375

### th...@chromium.org (2020-10-01)

Hopefully I'm adding the right labels. One can look up the "ExportTaggedPDF" Finch study to see what the current state is.

### ch...@gmail.com (2020-10-01)

This is very similar to https://crbug.com/chromium/707549.

### cl...@chromium.org (2020-10-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5726165006614528.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/30261f9de11e776b50dc8c726308b8495db4232c

commit 30261f9de11e776b50dc8c726308b8495db4232c
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Oct 01 19:18:54 2020

Check RF is alive In PrintRenderFrameHelper::PreviewPageRendered().

Do not take an accessibility snapshot if the RenderFrame is gone.

Bug: 1133983
Change-Id: I612cc72936a1dcedc5180c24eae067e47237b09b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2442375
Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/heads/master@{#812851}

[modify] https://crrev.com/30261f9de11e776b50dc8c726308b8495db4232c/components/printing/renderer/print_render_frame_helper.cc


### th...@chromium.org (2020-10-01)

M87 branch cut is today. It's not obvious if the fix is going to make the cut. I can verify the fix on Canary channel as soon as it is available there, and we can figure out merging after that.

### ad...@chromium.org (2020-10-01)

Yep. If this is fixed, please mark the bug as fixed, and then Sheriffbot will add appropriate merge requests. (Though for a few days immediately after branch cut poor Sheriffbot wanders around in a daze, as if they've been too heavily on the gin. So I will try to keep an eye out too).

### th...@chromium.org (2020-10-01)

[Empty comment from Monorail migration]

### ch...@gmail.com (2020-10-01)

I just verified the fix on the latest version of Chromium 87.0.4280.0 refs/heads/master@{#812851} and I couldn't repro the crash. Fixed.

### ch...@gmail.com (2020-10-02)

Double-check, the use-after-free is fixed on 87.0.4280.0 canary.

### th...@chromium.org (2020-10-02)

Thanks for checking! We'll go through the merge process in the near future.

### [Deleted User] (2020-10-02)

[Empty comment from Monorail migration]

### th...@chromium.org (2020-10-02)

Looks like M87 branched at r812852, and the CL for this bug landed at r812851.

### cl...@chromium.org (2020-10-02)

ClusterFuzz testcase 5726165006614528 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=812830:812851

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### th...@chromium.org (2020-10-05)

adeltaylor@: Shall we request a merge for M86? I think we can skip M85, given M86 is about to go to Stable.

### ad...@chromium.org (2020-10-05)

Yes please. Sheriffbot would do so anyway, so I will short cut it.

I won't approve this until initial M86 stable has rolled out properly, which will be a few days at least.

### [Deleted User] (2020-10-05)

This bug requires manual review: We are only 0 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-10-07)

Renderer UaF is normally High unless there's a significant mitigation, so bumping up severity.

### th...@chromium.org (2020-10-07)

adetaylor: Are you going to reply to https://crbug.com/chromium/1133983#c26? Should I?

### ad...@google.com (2020-10-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-07)

Congratulations, the VRP panel has decided to award $5000 for this report.

### ad...@google.com (2020-10-08)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-12)

thestig@ - sorry, I didn't spot https://crbug.com/chromium/1133983#c28. That's for you to reply. However based on https://crbug.com/chromium/1133983#c24 and the simplicity of the fix I am approving merge to M86 even without those answers.

Please merge to branch 4240.

### go...@google.com (2020-10-12)

Please merge your change to M86 branch 4240 now so it can be included in this week M86 respin for Android. Thank you.

### th...@chromium.org (2020-10-12)

https://chromium-review.googlesource.com/c/chromium/src/+/2466395 in CQ.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/45b694478464c0dd62626e16beee97f43593b599

commit 45b694478464c0dd62626e16beee97f43593b599
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Oct 12 21:00:54 2020

M86: Check RF is alive In PrintRenderFrameHelper::PreviewPageRendered().

Do not take an accessibility snapshot if the RenderFrame is gone.

(cherry picked from commit 30261f9de11e776b50dc8c726308b8495db4232c)

Tbr: dmazzoni@chromium.org
Bug: 1133983
Change-Id: I612cc72936a1dcedc5180c24eae067e47237b09b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2442375
Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#812851}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2466395
Reviewed-by: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1221}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/45b694478464c0dd62626e16beee97f43593b599/components/printing/renderer/print_render_frame_helper.cc


### ad...@google.com (2020-10-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-01-08)

This issue was migrated from crbug.com/chromium/1133983?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1133982]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053481)*
