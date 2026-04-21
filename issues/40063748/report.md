# UAF in content::NavigationState::RunCommitSameDocumentNavigationCallback

| Field | Value |
|-------|-------|
| **Issue ID** | [40063748](https://issues.chromium.org/issues/40063748) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Linux, Mac, Windows |
| **Reporter** | em...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2023-03-24 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

chrome version:  

Chromium 113.0.5653.0  

Chromium 114.0.5673.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1121654.zip)  

os version:  

ubuntu 22.04

repro step:  

1 python3 -m http.server 8000 --dir=|dir path to poc.html|  

2 ./chrome <http://localhost:8000/poc.html> --user-data-dir=/tmp/1111  

3 the uaf will be reproduced immediately.

I also tested with the latest official release version, and the crash(sig 11) will be reproduced immediately.But I haven't analyzed it yet, so I can't guarantee 100% that it is the same issue.

# **Problem Description:**

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6040000963f8 at pc 0x55bf218727de bp 0x7ffdc0484f70 sp 0x7ffdc0484f68  

READ of size 8 at 0x6040000963f8 thread T0 (chrome)  

#0 0x55bf218727dd in operator bool ./../../base/memory/scoped\_refptr.h:318:43  

#1 0x55bf218727dd in is\_null ./../../base/functional/callback\_internal.h:127:34  

#2 0x55bf218727dd in operator bool ./../../base/functional/callback\_internal.h:128:44  

#3 0x55bf218727dd in operator bool ./../../base/functional/callback.h:109:45  

#4 0x55bf218727dd in content::NavigationState::RunCommitSameDocumentNavigationCallback(blink::mojom::CommitResult) ./../../content/renderer/navigation\_state.cc:92:7  

#5 0x55bf216f6b75 in content::RenderFrameImpl::CommitSameDocumentNavigation(mojo::StructPtr[blink::mojom::CommonNavigationParams](javascript:void(0);), mojo::StructPtr[blink::mojom::CommitNavigationParams](javascript:void(0);), base::OnceCallback<void (blink::mojom::CommitResult)>) ./../../content/renderer/render\_frame\_impl.cc:3102:21  

#6 0x55befe74639b in content::mojom::FrameStubDispatch::AcceptWithResponder(content::mojom::Frame\*, mojo::Message\*, std::Cr::unique\_ptr<mojo::MessageReceiverWithStatus, std::Cr::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);)>) ./gen/content/common/frame.mojom.cc:2976:13  

#7 0x55bf0cd5c35f in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:968:56  

#8 0x55bf0cd77942 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#9 0x55bf0cd61ff8 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:695:20  

#10 0x55bf0d5c3807 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc\_mojo\_bootstrap.cc:1069:24  

#11 0x55bf0d5b873d in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/functional/bind\_internal.h:770:12  

#12 0x55bf0d5b873d in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> > ./../../base/functional/bind\_internal.h:949:12  

#13 0x55bf0d5b873d in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/functional/bind\_internal.h:1044:12  

#14 0x55bf0d5b873d in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:995:12  

#15 0x55bf0a983e32 in Run ./../../base/functional/callback.h:152:12  

#16 0x55bf0a983e32 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:149:34  

#17 0x55bf0a9dadf3 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:475:11)> ./../../base/task/common/task\_annotator.h:89:5  

#18 0x55bf0a9dadf3 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:473:23  

#19 0x55bf0a9d9bb5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:339:41  

#20 0x55bf0a9dc494 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#21 0x55bf0a86bab3 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:48:55  

#22 0x55bf0a9dd159 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:634:12  

#23 0x55bf0a90644f in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:140:14  

#24 0x55bf218ffe4e in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer\_main.cc:336:16  

#25 0x55bf07ea8174 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:709:14  

#26 0x55bf07ea9a80 in content::RunOtherNamedProcessTypeMain(std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> cons

**Additional Comments:**

\*\*Chrome version: \*\* 113.0.5653.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 406 B)
- [asan.log](attachments/asan.log) (text/plain, 35.2 KB)

## Timeline

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-03-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6202744696930304.

### cl...@chromium.org (2023-03-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-03-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-03-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-03-25)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Core Internals>Mojo]

### cl...@chromium.org (2023-03-25)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/a13f65ab7525741cbb450b231a557969f5fab7b7 (Store a CommitSameDocumentNavigationCallback on NavigationState).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2023-03-25)

Detailed Report: https://clusterfuzz.com/testcase?key=6202744696930304

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60b000170118
Crash State:
  content::NavigationState::RunCommitSameDocumentNavigationCallback
  content::RenderFrameImpl::CommitSameDocumentNavigation
  content::mojom::FrameStubDispatch::AcceptWithResponder
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1113503:1113524

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6202744696930304

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### [Deleted User] (2023-03-25)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-25)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2023-03-27)

[Empty comment from Monorail migration]

### ra...@chromium.org (2023-03-28)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Core -Internals>Mojo UI>Browser>Navigation]

### gi...@appspot.gserviceaccount.com (2023-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5872c2159909eb6c92c1d87d058f50bfafeb50bc

commit 5872c2159909eb6c92c1d87d058f50bfafeb50bc
Author: Nate Chapin <japhet@chromium.org>
Date: Tue Mar 28 16:10:30 2023

Handle the case where a new navigation happens synchronously inside RenderFrameImpl::CommitSameDocumentNavigation

This is broken after https://chromium-review.googlesource.com/c/chromium/src/+/4300672

Bug: 1427449
Change-Id: Ie6ec0a597eeb45e3a7ae11215fc010d284a997bf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4375397
Commit-Queue: Nate Chapin <japhet@chromium.org>
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1123066}

[add] https://crrev.com/5872c2159909eb6c92c1d87d058f50bfafeb50bc/third_party/blink/web_tests/external/wpt/navigation-api/navigate-event/replaceState-inside-back-handler.html
[modify] https://crrev.com/5872c2159909eb6c92c1d87d058f50bfafeb50bc/content/renderer/render_frame_impl.cc


### pb...@google.com (2023-03-29)

This issue is marked as M113 Stable release blocker, please help triage the issue and help confirm if this is indeed serious enough to block Beta release and if so get a fix landed asap to trunk and verify on canary build and request a merge to M113 so we can get this to Dev/beta release quickly. If this is not critical enough to warrant RBS, please drop the RBS label

### ja...@chromium.org (2023-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-29)

Merge approved: your change passed merge requirements and is auto-approved for M113. Please go ahead and merge the CL to branch 5672 (refs/branch-heads/5672) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-03-29)

ClusterFuzz testcase 6202744696930304 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1123065:1123075

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/233b9921add89975ad91886bfde13b8b58fa411a

commit 233b9921add89975ad91886bfde13b8b58fa411a
Author: Nate Chapin <japhet@chromium.org>
Date: Thu Mar 30 17:18:47 2023

Handle the case where a new navigation happens synchronously inside RenderFrameImpl::CommitSameDocumentNavigation

This is broken after https://chromium-review.googlesource.com/c/chromium/src/+/4300672

(cherry picked from commit 5872c2159909eb6c92c1d87d058f50bfafeb50bc)

Bug: 1427449
Change-Id: Ie6ec0a597eeb45e3a7ae11215fc010d284a997bf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4375397
Commit-Queue: Nate Chapin <japhet@chromium.org>
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1123066}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4382568
Auto-Submit: Nate Chapin <japhet@chromium.org>
Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
Cr-Commit-Position: refs/branch-heads/5672@{#144}
Cr-Branched-From: 5f2a72468eda1eb945b3b5a2298b5d1cd678521e-refs/heads/main@{#1121455}

[add] https://crrev.com/233b9921add89975ad91886bfde13b8b58fa411a/third_party/blink/web_tests/external/wpt/navigation-api/navigate-event/replaceState-inside-back-handler.html
[modify] https://crrev.com/233b9921add89975ad91886bfde13b8b58fa411a/content/renderer/render_frame_impl.cc


### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-05)

Congratulations on another one, Cassidy Kim! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1427449?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063748)*
