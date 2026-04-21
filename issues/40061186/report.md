# Security: use-after-poison interface_endpoint_client.cc:900 in mojo::InterfaceEndpointClient::HandleValidatedMessage

| Field | Value |
|-------|-------|
| **Issue ID** | [40061186](https://issues.chromium.org/issues/40061186) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>PeerConnection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | ht...@chromium.org |
| **Created** | 2022-09-30 |
| **Bounty** | $10,000.00 |

## Description

#Summary
SUMMARY: AddressSanitizer: use-after-poison interface_endpoint_client.cc:900 in mojo::InterfaceEndpointClient::HandleValidatedMessage

#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-1053385.zip

#Reproduce
I submitted this issue a long time ago(#1274315). At that time, because it was very difficult to reproduce, it was impossible to make a minimum POC to locate the problem.
This time I wrote some automated scripts and finally found a minimal POC that can be reproduced by local tests
I will first provide a minimum POC that I can reproduce locally to help the analysis of the root cause of the issue.

Type of crash
Render tab

#Analysis
Work in progress

#ASAN
=================================================================
==15728==ERROR: AddressSanitizer: use-after-poison on address 0x7ee70044e0f8 at pc 0x7ffe6a032938 bp 0x00e0913fe540 sp 0x00e0913fe588
READ of size 8 at 0x7ee70044e0f8 thread T0
==15728==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffe6a032937 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:989
    #1 0x7ffe6cdf151e in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #2 0x7ffe6a035efe in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:689
    #3 0x7ffe6a04c10a in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:1096
    #4 0x7ffe6a04affa in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex_router.cc:716
    #5 0x7ffe6cdf151e in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #6 0x7ffe6a02c4b0 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:561
    #7 0x7ffe6a02ddd1 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:618
    #8 0x7ffe6a02f32b in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(),base::WeakPtr<mojo::Connector> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:865
    #9 0x7ffe69d720fa in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:133
    #10 0x7ffe6cc8d539 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:441
    #11 0x7ffe6cc8c34d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:297
    #12 0x7ffe6cc696bb in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40
    #13 0x7ffe6cc8f7fb in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:600
    #14 0x7ffe69d0cd82 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #15 0x7ffe6c6b7594 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:313
    #16 0x7ffe698988bb in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:752
    #17 0x7ffe6989ab68 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1105
    #18 0x7ffe69896a1f in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:342
    #19 0x7ffe69897102 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:370
    #20 0x7ffe699cb807 in headless::`anonymous namespace'::RunContentMain C:\b\s\w\ir\cache\builder\src\headless\app\headless_shell.cc:176
    #21 0x7ffe699cb1cd in headless::RunChildProcessIfNeeded C:\b\s\w\ir\cache\builder\src\headless\app\headless_shell.cc:878
    #22 0x7ffe699c7c9f in headless::HeadlessShellMain C:\b\s\w\ir\cache\builder\src\headless\app\headless_shell.cc:691
    #23 0x7ffe5d771484 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:160
    #24 0x7ff70e105c22 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:166
    #25 0x7ff70e102bd7 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:395
    #26 0x7ff70e5237cf in __scrt_common_main_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #27 0x7fff1e7a7033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)
    #28 0x7fff1ee026a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

Address 0x7ee70044e0f8 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:989 in mojo::InterfaceEndpointClient::HandleValidatedMessage
Shadow bytes around the buggy address:
  0x7ee70044de00: 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ee70044de80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ee70044df00: 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ee70044df80: f7 f7 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ee70044e000: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 f7 f7 f7 f7
=>0x7ee70044e080: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]
  0x7ee70044e100: f7 f7 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ee70044e180: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ee70044e200: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ee70044e280: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ee70044e300: f7 f7 f7 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
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
==15728==ABORTING

## Attachments

- [m15.html](attachments/m15.html) (text/plain, 8.8 KB)
- [h1.js](attachments/h1.js) (text/plain, 827 B)
- [asan_0930.txt](attachments/asan_0930.txt) (text/plain, 6.3 KB)
- [rca0929.diff](attachments/rca0929.diff) (text/plain, 3.9 KB)
- [fix_a.diff](attachments/fix_a.diff) (text/plain, 1.8 KB)
- deleted (application/octet-stream, 0 B)
- [fix_b.diff](attachments/fix_b.diff) (text/plain, 1.7 KB)

## Timeline

### [Deleted User] (2022-09-30)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-09-30)

#Analysis
receiver_ has not been disconnected when PeerConnectionTracker is recycled
I think the root cause of the issue is the same as https://bugs.chromium.org/p/chromium/issues/detail?id=1043603.


third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.h:293
```
  THREAD_CHECKER(main_thread_);
  mojo::Remote<blink::mojom::blink::PeerConnectionTrackerHost>
      peer_connection_tracker_host_;
  mojo::Receiver<blink::mojom::blink::PeerConnectionManager> receiver_{this};	<<

  scoped_refptr<base::SingleThreadTaskRunner> main_thread_task_runner_;
};
```

### m....@gmail.com (2022-09-30)

[Comment Deleted]

### m....@gmail.com (2022-09-30)

#RCA

Adding a log when gc recycles PeerConnectionTracker can find that the receiver_ has not been disconnected

```
+USING_PRE_FINALIZER(PeerConnectionTracker, Dispose);

+void PeerConnectionTracker::Dispose(){
+  LOG(WARNING)<<"[11000]PeerConnectionTracker::Dispose ->> receiver_: "<<receiver_.is_bound();
+}

[4256:15896:1001/000708.627:ERROR:media_devices.cc(238)] [11000]MediaDevices::getUserMedia
[4256:15896:1001/000709.590:WARNING:peer_connection_tracker.cc(678)] [11000]PeerConnectionTracker::Dispose ->> receiver_: 1

```

### m....@gmail.com (2022-09-30)

Patch for RCA

### m....@gmail.com (2022-09-30)

#Fix
There are 2 ways to fix it.
1. Reset receiver_ when gc recycles PeerConnectionTracker like issue(1043603).
2. Use HeapMojoReceiver to ensure that receiver_ is reset automatically



### m....@gmail.com (2022-09-30)

2. Use HeapMojoReceiver to ensure that receiver_ is reset automatically

### mp...@chromium.org (2022-10-03)

Thanks for the report!

[Monorail components: Blink>WebRTC>PeerConnection]

### [Deleted User] (2022-10-03)

[Empty comment from Monorail migration]

### ht...@chromium.org (2022-10-03)

Tried to reproduce (I combined m15.html and h1.js into one file, but otherwise changed nothing) under a freshly compiled Chromium, but was not able to get a crash. (This may be due to my inexperience with ASAN, different environment, or something else - I only have Linux boxes).

Using HeapMojoReceiver means (if I understand it correctly) that the Mojo receiver will be safely garbage collected, so I'd think that fix b is "likely to be harmless at worst", and seems the more reasonable way to fix the issue. Comments welcome.



### m....@gmail.com (2022-10-03)

You can see if comments 4, 5 help locate the problem. 

### [Deleted User] (2022-10-03)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ht...@chromium.org (2022-10-05)

The pattern here seems to be consistent with the issue described in https://docs.google.com/document/d/1mYKbNgVzQUbc0zKLjiBcO5Ue_VTh3sIwj8glHU-azQ8/edit#heading=h.xgjl2srtytjt - so HeapMojoReceiver should be the right fix.


### gi...@appspot.gserviceaccount.com (2022-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e3437317c4cd8401f0f0d599b61751bbe0e1ec70

commit e3437317c4cd8401f0f0d599b61751bbe0e1ec70
Author: Harald Alvestrand <hta@chromium.org>
Date: Thu Oct 06 06:32:41 2022

Use HeapMojoReceiver rather than mojo::Receiver for PeerConnectionTracker

HeapMojoReceiver is recommended for garbage collected objects, avoiding
problems with conflicting lifetimes.

Bug: chromium:1369882
Change-Id: Ic38e761cf4275e6d7b30a6d7e2daa5d1596e67a4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3936144
Reviewed-by: Henrik Boström <hbos@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1055630}

[modify] https://crrev.com/e3437317c4cd8401f0f0d599b61751bbe0e1ec70/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.h
[modify] https://crrev.com/e3437317c4cd8401f0f0d599b61751bbe0e1ec70/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.cc


### ht...@chromium.org (2022-10-06)

Despite not being able to reproduce, I'm marking this bug as "fixed", since the problem appears to be an instance of a well known problem.
Reporter, if you can test on Canary in a day or two in your configuration where the bug reproduces, that would be most appreciated.


### m....@gmail.com (2022-10-06)

Reproduced on asan-win32-release_x64-1055146 and not on asan-win32-release_x64-1055708, so the patch works fine.


### [Deleted User] (2022-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-06)

Requesting merge to stable M106 because latest trunk commit (1055630) appears to be after stable branch point (1036826).

Requesting merge to beta M107 because latest trunk commit (1055630) appears to be after beta branch point (1047731).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-07)

Merge review required: M107 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-07)

Merge review required: M106 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ht...@chromium.org (2022-10-07)

1. Possible security issue. No exploit in the wild known.
2. https://chromium-review.googlesource.com/c/chromium/src/+/3936144
3. Yes.
4. No. It is a simple bug fix.
5. N/A
6. No, I don't think so.


### am...@chromium.org (2022-10-07)

Thanks for the fast fix! 
M107 merge approved, please merge to branch 5304 
M106 merge approved, please merge to branch 5249 by 10am PST, Monday, 10 October, so this fix can be in the next stable/106 security respin -- thank you! 

### gi...@appspot.gserviceaccount.com (2022-10-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cb9dff93f3d45f4c130d4c72817b1255a4359bca

commit cb9dff93f3d45f4c130d4c72817b1255a4359bca
Author: Harald Alvestrand <hta@chromium.org>
Date: Mon Oct 10 08:37:15 2022

[Merge to M106] Use HeapMojoReceiver rather than mojo::Receiver for PeerConnectionTracker

HeapMojoReceiver is recommended for garbage collected objects, avoiding
problems with conflicting lifetimes.

(cherry picked from commit e3437317c4cd8401f0f0d599b61751bbe0e1ec70)

Bug: chromium:1369882
Change-Id: Ic38e761cf4275e6d7b30a6d7e2daa5d1596e67a4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3936144
Reviewed-by: Henrik Boström <hbos@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1055630}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3934344
Commit-Queue: Henrik Boström <hbos@chromium.org>
Auto-Submit: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/branch-heads/5249@{#790}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/cb9dff93f3d45f4c130d4c72817b1255a4359bca/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.h
[modify] https://crrev.com/cb9dff93f3d45f4c130d4c72817b1255a4359bca/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.cc


### [Deleted User] (2022-10-10)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/81f2600e674ab7498dae9dc30208eb3de2669603

commit 81f2600e674ab7498dae9dc30208eb3de2669603
Author: Harald Alvestrand <hta@chromium.org>
Date: Mon Oct 10 09:40:41 2022

[Merge to M107] Use HeapMojoReceiver rather than mojo::Receiver for PeerConnectionTracker

HeapMojoReceiver is recommended for garbage collected objects, avoiding
problems with conflicting lifetimes.

(cherry picked from commit e3437317c4cd8401f0f0d599b61751bbe0e1ec70)

Bug: chromium:1369882
Change-Id: Ic38e761cf4275e6d7b30a6d7e2daa5d1596e67a4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3936144
Reviewed-by: Henrik Boström <hbos@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1055630}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3935057
Commit-Queue: Henrik Boström <hbos@chromium.org>
Auto-Submit: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/branch-heads/5304@{#587}
Cr-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}

[modify] https://crrev.com/81f2600e674ab7498dae9dc30208eb3de2669603/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.h
[modify] https://crrev.com/81f2600e674ab7498dae9dc30208eb3de2669603/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.cc


### am...@chromium.org (2022-10-11)

[Empty comment from Monorail migration]

### vo...@google.com (2022-10-11)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations and nice finding! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### vo...@google.com (2022-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2022-10-18)

1. Just one https://crrev.com/c/3944306
2. Low - small changes, no conflicts with 102 branch
3. Yes, M106
4. Yes

### gm...@google.com (2022-10-18)

[Empty comment from Monorail migration]

### gm...@google.com (2022-10-26)

[Empty comment from Monorail migration]

### vo...@google.com (2022-10-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6fd00b7cbca35504a44cd15def3004a979ce8aef

commit 6fd00b7cbca35504a44cd15def3004a979ce8aef
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed Nov 02 14:03:26 2022

[M102-LTS] Use HeapMojoReceiver rather than mojo::Receiver for PeerConnectionTracker

HeapMojoReceiver is recommended for garbage collected objects, avoiding
problems with conflicting lifetimes.

(cherry picked from commit e3437317c4cd8401f0f0d599b61751bbe0e1ec70)

Bug: chromium:1369882
Change-Id: Ic38e761cf4275e6d7b30a6d7e2daa5d1596e67a4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3936144
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1055630}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3943460
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1380}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/6fd00b7cbca35504a44cd15def3004a979ce8aef/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.h
[modify] https://crrev.com/6fd00b7cbca35504a44cd15def3004a979ce8aef/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.cc


### gm...@google.com (2022-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1369882?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061186)*
