# use-after-poison in mojo::SimpleWatcher::OnHandleReady - image_bitmap_factories.cc Check failed: script_state->ContextIsValid(). 

| Field | Value |
|-------|-------|
| **Issue ID** | [40942439](https://issues.chromium.org/issues/40942439) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection, Internals>Mojo |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2023-11-14 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os version:  

ubuntu:22.04  

macos 14.0

tested chrome version:  

Chromium 121.0.6128.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1224132.zip)  

Chromium 113.0.5624.0(I believe it should be possible to reproduce earlier than this version.）  

Repro Steps:  

1 python3 -m http.server 8000 --dir=|Path|  

2 ./chrome --user-data-dir=/tmp/xx <http://localhost:8000/crash.html>  

Wait for more than ten seconds to reproduce.If it doesn't reproduce, you can try a few more times.

**Problem Description:**  

==2392274==ERROR: AddressSanitizer: use-after-poison on address 0x7eb900b9c450 at pc 0x5600a9f04480 bp 0x7ffdee8a21f0 sp 0x7ffdee8a21e8  

READ of size 4 at 0x7eb900b9c450 thread T0 (chrome)  

#0 0x5600a9f0447f in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:252:19  

#1 0x5600a9f05417 in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);) &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind\_internal.h:713:12  

#2 0x5600a9f05417 in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind\_internal.h:896:5  

#3 0x5600a9f05417 in void base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::\*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::\_\_Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>&&, std::\_\_Cr::integer\_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/functional/bind\_internal.h:968:12  

#4 0x5600a7836f18 in Run ./../../base/functional/callback.h:154:12  

#5 0x5600a7836f18 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:201:34  

#6 0x5600a78a1ff8 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:11)> ./../../base/task/common/task\_annotator.h:89:5  

#7 0x5600a78a1ff8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:461:23  

#8 0x5600a78a0d3a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:326:41  

#9 0x5600a78a2efa in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#10 0x5600a7702cdf in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:40:55  

#11 0x5600a78a3e10 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:626:12  

#12 0x5600a77b756c in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#13 0x5600c1874d13 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer\_main.cc:366:16  

#14 0x5600a448c40b in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:674:14  

#15 0x5600a448df17 in content::RunOtherNamedProcessTypeMain(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:778:12  

#16 0x5600a4491706 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1138:10  

#17 0x5600a4489edd in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:334:36  

#18 0x5600a448a60f in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:347:10  

#19 0x5600a614a840 in HeadlessChildMain ./../../headless/app/headless\_shell.cc:191:12  

#20 0x5600a614a840 in headless::HeadlessShellMain(content::ContentMainParams) ./../../headless/app/headless\_shell.cc:252:5  

#21 0x560092fbdb2a in ChromeMain ./../../chrome/app/chrome\_main.cc:175:14  

#22 0x7fda6d429d8f in \_\_libc\_start\_call\_main ./csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

Address 0x7eb900b9c450 is a wild pointer inside of access range of size 0x000000000004.  

SUMMARY: AddressSanitizer: use-after-poison (/home/pwn11/asan-linux-release/chrome+0x262fc47f) (BuildId: 490e27dd1eaca0b6)  

Shadow bytes around the buggy address:  

0x7eb900b9c180: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x7eb900b9c200: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x7eb900b9c280: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x7eb900b9c300: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7  

0x7eb900b9c380: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 f7 f7 f7  

=>0x7eb900b9c400: f7 f7 f7 f7

**Additional Comments:**

\*\*Chrome version: \*\* 113.0.5624.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.3 KB)

## Timeline

### [Deleted User] (2023-11-14)

[Empty comment from Monorail migration]

### ar...@google.com (2023-11-14)

(current security shepherd here)

Thanks!

I can reproduce by following the instructions provided.
I reproduced on both 121.0.6115.0 (canary) and 118.0.5993.0 (stable-extended)

Severity-High: Memory corruption in a renderer process without no specific user interactions. One potential mitigating factor could be the unreliability and the time it takes to trigger the bugs, but I did not take this into account here.

Security-Impact: Stable-extended

There are already several similar bugs:
https://bugs.chromium.org/p/chromium/issues/list?q=%22use-after-poison%20in%20mojo%3A%3ASimpleWatcher%3A%3AOnHandleReady%22&can=1

I don't really have an owner to assign this bug. So I will tentatively send it to @mlippautz and try to ask clusterfuzz to reproduce.


[Monorail components: Blink>GarbageCollection Internals>Mojo]

### cl...@chromium.org (2023-11-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4522839307124736.

### ar...@google.com (2023-11-14)

Pending clusterfuzz job: https://clusterfuzz.com/testcase-detail/4522839307124736

### [Deleted User] (2023-11-14)

[Empty comment from Monorail migration]

### ml...@chromium.org (2023-11-14)

Similar to MiraclePtr, we are generally not owning all memory safety bugs that we find in the renderer. We are generally happy to help but I think there should be another owner here.

### ar...@google.com (2023-11-14)

Yes, this makes sense. I should probably just have CCed. Sorry about this. Hopefully Clusterfuzz could bring us potentially more informations.

The mojo::SimpleWatcher::Context is holding a WeakPtr over a mojo::SimpleWatcher. We are using it after poison. This suggest the mojo::SimpleWatcher instance is part of a larger struct held by a garbage collected object.
I would expect the GC to run the destructor, in particular the ~WeakPtrFactory(), before poisoning memory.

### ml...@chromium.org (2023-11-14)

Where is the ~WeakPtrFactory run? That generally must happen in a pre-finalizer iirc.

### [Deleted User] (2023-11-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@google.com (2023-11-15)

> Where is the ~WeakPtrFactory run? That generally must happen in a pre-finalizer iirc.

If the GC classes doesn't have a pre finalizer? What happens? We don't run the destructors?

If yes, I see a couple of SimpleWatcher in GC classes not using prefinalizer.

For instance the bugs involves navigations, and this SimpleWatch would be a great match:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/url_loader/worker_main_script_loader.h;l=96;bpv=1;bpt=1?q=SimpleWatcher%20Member%20-USING_PRE_FINALIZER&ss=chromium

@mlippautz@chromium.org does it makes sense to you?

### ml...@chromium.org (2023-11-15)

Yes, this makes sense.

If we don't clear out the WekPtrFactory, then we may have mojo still use the object. However, after the GC deems it unreachable, it will poison it and only later invoke the dtor.

### ar...@google.com (2023-11-15)

Okay, so to fix this bug, we need to find the SimpleWatcher owned directly or indirectly by a garbage collected object who isn't resetting it during prefinalizer.

I will take a look and find the culprit and/or the fix.

### ar...@google.com (2023-11-15)

The POC creates in a loop many documents. The DocumentLoader is a GC object. It indirectly owns a SimpleWatcher via:
DocumentLoader -> WebNavigationBodyLoader -> NavigationBodyLoader -> SimplerWatcher.

I see no prefinalizer. So, I am assuming this is one of the root cause.
I will try adding one and get back to you.





### ml...@chromium.org (2023-11-15)

Wasn't there a project that marked all of these uses of WeakPtrFactory as unsafe if they weren'd cleared in a prefinalizer?

### ar...@google.com (2023-11-15)

[Comment Deleted]

### ar...@google.com (2023-11-15)

Yes. This was Paul project. +CC paulsemel@ FYI.

Coincidentally, and surprisingly to me, it looks like I asked why it was not WeakPtrFactory:
https://chromium-review.googlesource.com/c/chromium/src/+/4003175/comment/8fafd07e_aa47d53d/
You made a reply I didn't understand. After that, I guess we lost track of it.

### ml...@chromium.org (2023-11-15)

I meant that if the object that is using the WeakPtr doesn't outlive the GCed object holding the WeakPtrFactory we are safe. In this case we are not because even if SimpleWatcher is considered dead it is still refererred to by the WeakPtr.

### ar...@google.com (2023-11-15)

Thanks!

I did more investigations. This is a different problem. The potential issue with the DocumentLoader/NavigationBodyLoader will be investigated elsewhere. I opened https://crbug.com/chromium/1502511.


We are reaching this DCHECK:

image_bitmap_factories.cc(158)] Check failed: script_state->ContextIsValid(). 

```
[1019211:1:1115/130617.282419:FATAL:image_bitmap_factories.cc(158)] Check failed: script_state->ContextIsValid().
    #0 0x55fc09597fce in ___interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4357:13
    #1 0x55fc244fadc8 in base::debug::CollectStackTrace(void const**, unsigned long) ./../../base/debug/stack_trace_posix.cc:1040:7
    #2 0x55fc244a7fa9 in StackTrace ./../../base/debug/stack_trace.cc:221:12
    #3 0x55fc244a7fa9 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:218:28
    #4 0x55fc241232c6 in logging::LogMessage::~LogMessage() ./../../base/logging.cc:705:29
    #5 0x55fc240c58d9 in ~DCheckLogMessage ./../../base/check.cc:90:3
    #6 0x55fc240c58d9 in logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage() ./../../base/check.cc:86:32
    #7 0x55fc240c5400 in logging::NotReachedError::~NotReachedError() ./../../base/check.cc:267:3
    #8 0x55fc3c692f82 in blink::ImageBitmapFactories::CreateImageBitmapFromBlob(blink::ScriptState*, blink::ImageBitmapSource*, std::__Cr::optional<gfx::Rect>, blink::ImageBitmapOptions const*) ./../../third_party/blink/renderer/modules/canvas/imagebitmap/image_bitmap_factories.cc:158:3
    #9 0x55fc3c6944c9 in blink::ImageBitmapFactories::CreateImageBitmap(blink::ScriptState*, blink::ImageBitmapSource*, std::__Cr::optional<gfx::Rect>, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/canvas/imagebitmap/image_bitmap_factories.cc:227:12
    #10 0x55fc3c6936d3 in blink::ImageBitmapFactories::CreateImageBitmap(blink::ScriptState*, blink::V8UnionBlobOrHTMLCanvasElementOrHTMLImageElementOrHTMLVideoElementOrImageBitmapOrImageDataOrOffscreenCanvasOrSVGImageElementOrVideoFrame const*, blink::ImageBitmapOptions const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/canvas/imagebitmap/image_bitmap_factories.cc:190:10
    #11 0x55fc39b07715 in createImageBitmap ./../../third_party/blink/renderer/modules/canvas/imagebitmap/image_bitmap_factories.h:90:12
    #12 0x55fc39b07715 in blink::(anonymous namespace)::v8_window::CreateImageBitmapOperationOverload1(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_window.cc:14532:23
    #13 0x55fc39ab2f76 in blink::(anonymous namespace)::v8_window::CreateImageBitmapOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_window.cc:0:0
    #14 0x55fc17a743d0 in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc:0:0
```

If we ignore the DCHECK, then we are hitting the issue with the SimpleWatcher.
ImageBitmapFactories -> FileReaderLoader -> SimpleWatcher -> WeakPtrFactory;


So, we should do two things:
1. Fix the DCHECK
2. Add a prefinalizer in FileReaderLoader cancelling the SimpleWatcher.


@fserb, can I assign this security bug to you, as the main OWNER of this directory? (2) seems easy to do, but (1) would require more knowledge. 



### fs...@chromium.org (2023-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-28)

jpgravel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2023-11-28)

[security shepherd]: Hi jpgravel@! Just following up to see if you have had the chance to take a look, specifically, c#18? Thanks!

### pa...@chromium.org (2023-11-29)

Just took a look at this, since I rewrote most of the `FileReaderLoader` APIs. Not having a finalizer in `FileReaderLoader` is deliberate, and the way this class must be used should prevent any issues with both `mojo::SimpleWatcher` and `mojo::ScopedDataPipeConsumerHandle` (which could trigger similar issues IIRC).

It seems to me that the fact that the `DCHECK` fails is the real issue here, since the loader is created a bit after the check. I am not an expert with context/lifetime, so I am unsure why this can happen.

Normally, we watch the context lifetime as soon as the loaders are created, and thus if the context would be to change while reading a file/blob, we should correctly cancel and clean both loaders state.

### pa...@chromium.org (2023-11-29)

I should have a fix for this: crrev.com/c/5071252.

### gi...@appspot.gserviceaccount.com (2023-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c4d2f15b8f97076c8fd0f9aa5814b94db698b75c

commit c4d2f15b8f97076c8fd0f9aa5814b94db698b75c
Author: Paul Semel <paulsemel@chromium.org>
Date: Wed Nov 29 14:23:04 2023

ImageBitmapFactory: fix empty context dcheck

Fixed: 1502102
Change-Id: Ib42d2897d62136ae835561bcf56884b5624060a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5071252
Commit-Queue: Paul Semel <paulsemel@chromium.org>
Reviewed-by: Jean-Philippe Gravel <jpgravel@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1230617}

[modify] https://crrev.com/c4d2f15b8f97076c8fd0f9aa5814b94db698b75c/third_party/blink/renderer/modules/canvas/imagebitmap/image_bitmap_factories.cc


### [Deleted User] (2023-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-29)

Requesting merge to extended stable M118 because latest trunk commit (1230617) appears to be after extended stable branch point (1192594).

Requesting merge to stable M119 because latest trunk commit (1230617) appears to be after stable branch point (1204232).

Requesting merge to beta M120 because latest trunk commit (1230617) appears to be after beta branch point (1217362).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-29)

Thanks for the quick response on this one paulsemel@. The last planned releases of M119 Stable and M118 Extended Stable were shipped yesterday, so I'm removing review labels for those. Since this just (albeit small) just landed, I'll revisit in a couple of days for M120 merge review. M120 Stable RC was cut yesterday, so there is plenty of bake time and review before deadlines for the first security update of M120. 

### am...@google.com (2023-11-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-30)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us --- nice work! 

### [Deleted User] (2023-11-30)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1502102&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>GarbageCollection,Internals>Mojo&entry.975983575=jpgravel@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-30)

Merge review required: M120 has already been cut for stable release.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-04)

120 merge approved for https://crrev.com/c/5071252
please merge this fix to branch 6099 at your earliest convenience (and before EOD Thursday, 7 December) so this fix can be included in the first security update of M120 Stable -- thanks! 

### sr...@google.com (2023-12-05)

[Empty comment from Monorail migration]

### va...@chromium.org (2023-12-05)

[Empty comment from Monorail migration]

### jp...@chromium.org (2023-12-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/76340163a820d608214be06807e24bcc326a97fb

commit 76340163a820d608214be06807e24bcc326a97fb
Author: Paul Semel <paulsemel@chromium.org>
Date: Wed Dec 06 15:52:56 2023

[M120] ImageBitmapFactory: fix empty context dcheck

Approved by:
https://bugs.chromium.org/p/chromium/issues/detail?id=1502102#c34

(cherry picked from commit c4d2f15b8f97076c8fd0f9aa5814b94db698b75c)

Fixed: 1502102
Change-Id: Ib42d2897d62136ae835561bcf56884b5624060a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5071252
Commit-Queue: Paul Semel <paulsemel@chromium.org>
Reviewed-by: Jean-Philippe Gravel <jpgravel@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1230617}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5088373
Auto-Submit: Arthur Sonzogni <arthursonzogni@google.com>
Reviewed-by: Paul Semel <paulsemel@chromium.org>
Cr-Commit-Position: refs/branch-heads/6099@{#1416}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/76340163a820d608214be06807e24bcc326a97fb/third_party/blink/renderer/modules/canvas/imagebitmap/image_bitmap_factories.cc


### [Deleted User] (2023-12-06)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2023-12-07)

> This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any
> additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
> 1. Was this issue a regression for the milestone it was found in?
No.
> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?
Unsure, first change was merged on March 30, 2023.

### rz...@google.com (2023-12-07)

[Empty comment from Monorail migration]

### rz...@google.com (2023-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-12-11)

1. https://crrev.com/c/5097973
2. Low, no conflicts
3. 120
4. Yes

### na...@google.com (2023-12-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-12-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-14)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### na...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/762390959765f38c016a3b9e5a50fa7532f7d265

commit 762390959765f38c016a3b9e5a50fa7532f7d265
Author: Paul Semel <paulsemel@chromium.org>
Date: Fri Jan 12 19:07:29 2024

[M114-LTS] ImageBitmapFactory: fix empty context dcheck

(cherry picked from commit c4d2f15b8f97076c8fd0f9aa5814b94db698b75c)

Fixed: 1502102
Change-Id: Ib42d2897d62136ae835561bcf56884b5624060a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5071252
Commit-Queue: Paul Semel <paulsemel@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1230617}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5097973
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Paul Semel <paulsemel@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1662}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/762390959765f38c016a3b9e5a50fa7532f7d265/third_party/blink/renderer/modules/canvas/imagebitmap/image_bitmap_factories.cc


### rz...@google.com (2024-01-12)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-12)

This issue was migrated from crbug.com/chromium/1502102?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GarbageCollection, Internals>Mojo]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40942439)*
