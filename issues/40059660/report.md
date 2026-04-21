# AddressSanitizer: use-after-poison blink\renderer\bindings\core\v8\script_promise_resolver.h:164 in 

| Field | Value |
|-------|-------|
| **Issue ID** | [40059660](https://issues.chromium.org/issues/40059660) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | pa...@microsoft.com |
| **Created** | 2022-05-13 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

#TestOn  

asan-win32-release\_x64-1003023

#Reproduce  

chrome.exe --no-sandbox --js-flags="--expose-gc --verify-heap" --user-data-dir=test fuzz-00588.html

Type of crash  

render tab

**Problem Description:**  

#Analysis  

Introduce by this CL <https://chromium-review.googlesource.com/c/chromium/src/+/3642429>

1. WebGLRenderingContextBase and make\_xr\_compatible\_resolver\_(ScriptPromiseResolver) are on-heap object.
2. We can't operate on on-heap objects in the destructor, because the destructor order of on-heap objects is not guaranteed, and the wrong use here leads to UAP.

**Additional Comments:**  

PS.  

My FUZZER running on CF also reported this problem (<https://clusterfuzz.com/testcase-detail/5351579121287168>),  

but he is still in the production of minimal samples, I don't want to wait for CF's automatic process report, So I submitted the report manually.

# #asan

==7776==ERROR: AddressSanitizer: use-after-poison on address 0x7e89003974fc at pc 0x7ffae700d55a bp 0x00bcce7fde60 sp 0x00bcce7fdea8  

READ of size 4 at 0x7e89003974fc thread T0  

#0 0x7ffae700d559 in blink::ScriptPromiseResolver::ResolveOrReject<blink::DOMArrayBuffer \*> C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\script\_promise\_resolver.h:164  

#1 0x7ffaf0eb0007 in blink::WebGLRenderingContextBase::CompleteXrCompatiblePromiseIfPending C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\webgl\webgl\_rendering\_context\_base.cc:824  

#2 0x7ffaf0eb741f in blink::WebGLRenderingContextBase::~WebGLRenderingContextBase C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\webgl\webgl\_rendering\_context\_base.cc:1350  

#3 0x7ffaf0f52161 in blink::WebGL2RenderingContext::~WebGL2RenderingContext C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\modules\webgl\webgl2\_rendering\_context.h:36  

#4 0x7ffadeeeb947 in cppgc::internal::HeapVisitor<cppgc::internal::(anonymous namespace)::MutatorThreadSweeper>::Traverse C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\heap-visitor.h:47  

#5 0x7ffadeee6e39 in cppgc::internal::Sweeper::SweeperImpl::Finish C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc:885  

#6 0x7ffadeee256f in cppgc::internal::Sweeper::SweeperImpl::Start C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc:784  

#7 0x7ffadeee17c0 in cppgc::internal::Sweeper::Start C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc\sweeper.cc:1062  

#8 0x7ffadd66f722 in v8::internal::CppHeap::TraceEpilogue C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc-js\cpp-heap.cc:690  

#9 0x7ffadd68062f in v8::internal::LocalEmbedderHeapTracer::TraceEpilogue C:\b\s\w\ir\cache\builder\src\v8\src\heap\embedder-tracing.cc:72  

#10 0x7ffadd746bd1 in v8::internal::Heap::PerformGarbageCollection C:\b\s\w\ir\cache\builder\src\v8\src\heap\heap.cc:2353  

#11 0x7ffadd73a4d2 in v8::internal::Heap::CollectGarbage C:\b\s\w\ir\cache\builder\src\v8\src\heap\heap.cc:1859  

#12 0x7ffadd742536 in v8::internal::Heap::PreciseCollectAllGarbage C:\b\s\w\ir\cache\builder\src\v8\src\heap\heap.cc:1680  

#13 0x7ffadd0590f4 in v8::Isolate::RequestGarbageCollectionForTesting C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:8601  

#14 0x7ffadd66b027 in v8::internal::CppHeap::CollectGarbageForTesting C:\b\s\w\ir\cache\builder\src\v8\src\heap\cppgc-js\cpp-heap.cc:772  

#15 0x7ffadff83900 in blink::ThreadState::CollectAllGarbageForTesting C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\heap\thread\_state.cc:191  

#16 0x7ffadff83763 in blink::ThreadState::SafePoint C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\heap\thread\_state.cc:166  

#17 0x7ffae0009071 in blink::GCTaskObserver::DidProcessTask C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\heap\gc\_task\_runner.h:52  

#18 0x7ffae18ff20e in base::sequence\_manager::internal::SequenceManagerImpl::NotifyDidProcessTask C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\sequence\_manager\_impl.cc:968  

#19 0x7ffae18fe3b1 in base::sequence\_manager::internal::SequenceManagerImpl::DidRunTask C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\sequence\_manager\_impl.cc:737  

#20 0x7ffae4816e28 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:395  

#21 0x7ffae48162e9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:290  

#22 0x7ffae47f3349 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#23 0x7ffae48187ea in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:497  

#24 0x7ffae1853867 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#25 0x7ffae42d1671 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:290  

#26 0x7ffae1410b13 in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:700  

#27 0x7ffae141274f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1039  

#28 0x7ffae140f143 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407  

#29 0x7ffae140f8cc in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435  

#30 0x7ffad60f14be in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#31 0x7ff768e75d62 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#32 0x7ff768e72b7d in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:385  

#33 0x7ff769273e1b in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#34 0x7ffb67637033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#35 0x7ffb67c02650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

Address 0x7e89003974fc is a wild pointer inside of access range of size 0x000000000004.  

SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\script\_promise\_resolver.h:164 in blink::ScriptPromiseResolver::ResolveOrReject<blink::DOMArrayBuffer \*>  

Shadow bytes around the buggy address:  

0x121153bf2e40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x121153bf2e50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x121153bf2e60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x121153bf2e70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x121153bf2e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x121153bf2e90: 00 00 00 00 00 00 00 00 00 00 00 00 f7 f7 f7[f7]  

0x121153bf2ea0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 00  

0x121153bf2eb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x121153bf2ec0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x121153bf2ed0: 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7  

0x121153bf2ee0: f7 f7 f7 f7 f7 f7 f7 00 f7 f7 f7 f7 f7 f7 f7 f7  

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

==7776==ABORTING

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 7.1 KB)
- [fuzz-00588.html](attachments/fuzz-00588.html) (text/plain, 243 B)

## Timeline

### dt...@chromium.org (2022-05-13)

[Empty comment from Monorail migration]

### dt...@chromium.org (2022-05-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-13)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-05-13)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-05-13)

Created a revert: https://chromium-review.googlesource.com/c/chromium/src/+/3648278

### kb...@chromium.org (2022-05-13)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-05-15)

CF confirms that revert has fixed the regression. I'm not sure what additional action is needed here. I think we can close this. Thanks, all for reporting, and helping with the reverts and management of this bug.

[Monorail components: Blink>Bindings]

### [Deleted User] (2022-05-15)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-15)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-05-15)

This is trunk churn, also, I did set those labels thankyouverymuch. Please don't re-open this bug again.

### [Deleted User] (2022-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-15)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-27)

Congratulations on another one! The VRP Panel has decided to award you $5000 for this report + $1000 fuzzer bonus. Thank you for your contributions to Chrome Fuzzing and in reporting this issue to us! 

### am...@google.com (2022-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-11)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M104. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-11)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-06-13)

See https://crbug.com/chromium/1325259#c10; there's nothing to merge here; this was introduced and reverted during M104; so is not active in M104 anymore.

### am...@chromium.org (2022-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1325259?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1321399]
[Monorail mergedwith: crbug.com/chromium/1325492]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059660)*
