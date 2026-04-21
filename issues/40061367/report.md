# Multiple checks fail, cross process crash, maybe race condition & use-after-free in video_encoder.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40061367](https://issues.chromium.org/issues/40061367) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>WebCodecs |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | so...@gmail.com |
| **Assignee** | eu...@chromium.org |
| **Created** | 2022-10-15 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**

1. Start a local server
2. Open localhost/index.html
3. Try again more time, if not crashes

With a debug build, the DCHECK will block the crash in video\_encoder.cc, so try without DCHECK

My reproduction ratio for

CHECK(!context.IsEmpty()):  

Debug in visual studio - more than 90%  

ASAN build: about fifty-fifty  

Stable: 0. Just a network changed page in 3 iframe, it's all what I can do with the stable (this maybe scaring if the compiler optimized out the checks)

CHECK(!waiting\_for\_context\_destroyed\_ || notifier\_):  

Debug in visual studio - less than 10%  

ASAN build: less than 20%  

Stable: 0, same as the previus

CRASH on random address in other tab:  

Debug in visual studio - Only 1 time. Unfortunately I have no data.  

ASAN build: 1 time. See the asan-3-other-tab.txt for the asan log  

Stable: 0 now, but I did not as many test as with the ASAN and the debug build

You need patience (or fortune) to reproduce. In same cases every try is success, sametimes 10-12 in row without crash. ASAN not detects anything, only the CHECK errors. :-)

**Problem Description:**  

I started to look into video\_encoder.cc. In the isConfigSupportedWithSoftwareOnly() method it resolves a Promise. I think I can here win the race and write a then\_getter exploit to destroy the context what is used in the DeleteLater() method. I wrote this code without any success, the context is not valid (DCHECK fired), but the browser not crashed, no uaf. After this I tried to define getter for same config parameters (width, height, codec), but the same result, no crash, no uaf. This was the time when I go evil, and I replaced the Iframe with 100 iframes. Bumm, crash. OK. This was the !context.isEmpty() check. Interesting, but the check blocks me. I did no further changes, but next time I get the !waiting\_for\_context\_destroyed\_ || notifier\_ check. Ok, other check, but not the best result. And after this, I tried to open an other tab, and bumm, the visual studio stopped in this method (MetricsWebContentsObserver::OnVisibilityChanged). Unfortunetly this is all info about this crash, but after I reproduced with the ASAN build. I opened the poc, and opened one other tab and loadad a local news portal into it. Bumm. My POC runs like a charm, but the news portal killed (asan-3-other-tab.txt).

I think, that the base problem is that this Promise resolve in the isConfigSupportedWithSoftwareOnly, with this we can create a race with 3 output:

- We lost the race, and the context is not destroyed
- We win the race, the context destroyed and nulled, so the CHECK is blocking our way (or not blocking in stable builds, I don't know)
- We totally win the race, the context destroyed, but not nulled and the waiting\_for\_context\_destroyed\_ flag is not set, so no one check can block the code to go on their way until it reaches the crash (maybe in other tabs). I think in this situation we see an use-after-free.

If I am true, then this is what happening here:

static void isConfigSupportedWithSoftwareOnly(  

ScriptPromiseResolver\* resolver,  

VideoEncoderSupport\* support,  

VideoEncoderTraits::ParsedConfig\* config) {  

std::unique\_ptr[media::VideoEncoder](javascript:void(0);) software\_encoder;  

switch (config->codec) {  

...  

}  

if (!software\_encoder) {  

support->setSupported(false);  

resolver->Resolve(support); // <-- This is not our way, we need the DeleteLater()for the crash  

return;  

}

auto done\_callback = [](std::unique\_ptr[media::VideoEncoder](javascript:void(0);) sw\_encoder,  

ScriptPromiseResolver\* resolver,  

VideoEncoderSupport\* support,  

media::EncoderStatus status) {  

support->setSupported(status.is\_ok());  

resolver->Resolve(support); // <-- DESTROY THE CONTEXT HERE  

DeleteLater(resolver->GetScriptState(), std::move(sw\_encoder)); // This can be the next step to the crash  

};  

...  

software\_encoder\_raw->Initialize(  

config->profile, config->options, base::DoNothing(),  

ConvertToBaseOnceCallback(  

CrossThreadBindOnce(done\_callback, std::move(software\_encoder), // <- cross thread binding :-)  

MakeUnwrappingCrossThreadHandle(resolver),  

MakeUnwrappingCrossThreadHandle(support))));  

}

void DeleteLater(ScriptState\* state, std::unique\_ptr<T> ptr) {  

DCHECK(state->ContextIsValid()); // <- This DCHECK is triggered if DCHECKs ara on and the context is destroyed here  

auto\* context = ExecutionContext::From(state); // Here we get our destroyed context, or a valid  

auto runner = context->GetTaskRunner(TaskType::kInternalDefault); // And we go to anywhere, maybe CRASH  

runner->DeleteSoon(FROM\_HERE, std::move(ptr)); // if we reach this, then we can go out from our process (as you can see in the asan log), I think TaskRunner helps in this  

}

What would I do?

1. Check the context in the DeleteLater method
2. Check the ScriptState context handling. ScriptStata gets back invalid contexts (ContextIsValid()=false, but the ExecutionContext::From(state) gives back the context, because ScriptState not checks this in GetContext() and the handle not cleared in this class when the context is destroyed.

// This can return an empty handle if the v8::Context is gone.  

v8::Local[v8::Context](javascript:void(0);) GetContext() const {  

return context\_.NewLocal(isolate\_);  

}

I think the comment is not really true above this method, it can return, but sametimes it returns an something what is invalid context. As this comment is misleading.  

// if (!script\_state\_->contextIsValid()) {  

// // It's possible that the context is already gone.  

// return;  

// }

because contextisvalid is only ContextIsNotEmpty :-)

bool ContextIsValid() const {  

return !context\_.IsEmpty() && per\_context\_data\_;  

}

If the Cross Thread Binding is the bad in this game, then this commit: <https://source.chromium.org/chromium/chromium/src/+/8d121ca5cb79f00535c64c993b8bd901c77ad60a> can be the reason, otherwise it's always existed, or I don't know.

Ask me if I can help You.

Regards,  

Peter

**Additional Comments:**  

Asan logs:  

ASAN-1.txt = Context isempty check crash  

ASAS-2.txt = !waiting\_for\_context\_destroyed\_ || notifier\_ check crash  

ASAN-3-other-tab.txt = Crash on other tab  

ASAN-all-output: my full console output and commands

In the HTML files you will see same unused code. Because the crash reproducution is not easy, and I know that this files with this contents can reproduce all the 3 cases, I didn't delete the unused parts, but it's not too much.

\*\*Chrome version: \*\* 108.0.5340.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan-1.txt](attachments/asan-1.txt) (text/plain, 5.7 KB)
- [asan-2.txt](attachments/asan-2.txt) (text/plain, 5.8 KB)
- [asan-3-other-tab.txt](attachments/asan-3-other-tab.txt) (text/plain, 22.2 KB)
- [asan-all-output.txt](attachments/asan-all-output.txt) (text/plain, 493.3 KB)
- [frame2.html](attachments/frame2.html) (text/plain, 1.6 KB)
- [index.html](attachments/index.html) (text/plain, 891 B)
- [asan-cached.txt](attachments/asan-cached.txt) (text/plain, 12.2 KB)

## Timeline

### [Deleted User] (2022-10-15)

[Empty comment from Monorail migration]

### so...@gmail.com (2022-10-15)

[Comment Deleted]

### so...@gmail.com (2022-10-16)

Today I reproduced one of the self tab crash in the stable (106). I sent 2 reports with my email address.

### so...@gmail.com (2022-10-16)

I tried to reproduce more times.

The other tab crash is not reproducible with the stable release, I can crash only my tab with this POC in the stable, and I can only crash this news portal, only in the dev version on the other tab. So something is interferring with my code on this site, maybe I help for the ng layout to crash with the excessive cpu usage.
So I think this part is only an exotic interesting thing, not a valid, or dangerous bug. But the ng-layout worth to look in, maybe a (not security related) bug exists in this code.
I don't know how many websites exists on the world, but I found first time the only one what crashes with my poc on the other tab. :-D

The other two (when my own tab is destroyed) is only a CHECK error. :-)

Another thing that is interesting to me, but I think not a big thing:

After a lot of reproduction, my cache poisoned, so now, if I open the browser (the asan version), I get immediatly the attached asan log, something bad is cached. Access-violation on unknown address 0x125e0009a6b4, from the cache, it persisted. :D
This is interesting, but I think this is not dangerous. I can't imagine, that sameone exists on the world who can poison the browser cache with javascript, with the right data, and exploit this access violation.

But I don't know chromium's code and I have not a master level in exploitation, I was always on the other end of the code. 
You can tell what is a real bug, and what not.

Thanks, and a have a nice day.!
Peter

### jd...@chromium.org (2022-10-17)

eugene@: would you mind taking a look at this? I haven't managed to reproduce it myself, but seems plausible. If you're not the right person, feel free to forward it on. Thank you!

Sev-High since it's a UaF in the browser process.

[Monorail components: Blink>Media>WebCodecs]

### [Deleted User] (2022-10-17)

[Empty comment from Monorail migration]

### eu...@chromium.org (2022-10-17)

Webcodecs objects are never instantiated in the browser process. I can believe there can be a renderer crash, but I don't think webcodecs can crash the browser 

### so...@gmail.com (2022-10-17)

eugene@ with my original poc only the renderer crashing. The cached trash can cause crash the in v8, but I think that is not relevant.
My two crash report ID in stable is:
c8ca2cb906332786 and 8af8757717b240fa
If it's helpfull.

### so...@gmail.com (2022-10-17)

Ah, and I don't think this is a high serverity UaF bug.
It's seems to be just 2 check fail what I can do. If the stable crash reports confirm this, then I think nothing bad to see here, and in this case I owe you an apology.

Regards,
 Peter


### so...@gmail.com (2022-10-17)

However, these two check failures pointed out to me that ScriptState->ContextIsValid() may cause problems, as I had suspected during my help with ClusterFuzz https://crbug.com/chromium/1252866.
If one can destroy the context before a method that is based only on the ContextIsValid call runs, then we can work with a non-existent context, and from here it is only up to luck whether it is null (as in the case of the ClusterFuzz error) or not null ( as in the case of one of the check failures in this) and, if it is not null, is there a check after it, or can you continue on the freeway.  E.g. here: 

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/bindings/core/v8/v8_wasm_response_extensions.cc;drc=047c7dc4ee1ce908d7fea38ca063fa2f80f92c77;l=294

If there is a way to destroy the context in a similar way as I do, the ScriptState will say that the context is valid and the promise will be thrown back with a reject. According to the comment, this is not exactly the right mode of operation. And unfortunetly this is that part what is reproducible with stable.

The other thing is that there may be a minor bug in NG's code that maybe somehow manages to allocate a smaller amount of memory than it needs. I am not able to reproduce this with the stable version and the code of the portal is too large to extract the part that causes the error (and I am only a visitor). Maybe this is not a valid problem because the lack of reproduction in stable environment.

The last lesson that can be learned is that the v8 deserializer is unprotected against data coming from the disk cache.  However, this can be very difficult to take advantage of, all my credit to whoever is able to make a remote exploit out of it, and this also cannot be reproduced in the stable release either, even if the poisoned files created by the crash are given as a data directory.

### [Deleted User] (2022-10-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### eu...@chromium.org (2022-10-18)

I got a repro on the most recent canary:

Thread 0 CrRendererMain (id: 0x00004834)CRASHEDMAGIC SIGNATURE THREAD
Exception infoEXCEPTION_BREAKPOINT @0x00007ffa0ec2b04d

Stack Quality100%Show frame trust levels
0x00007ffa0ec2b04d	(chrome.dll -v8_binding_for_core.cc:680)		blink::ToExecutionContext(v8::Local<v8::Context>)
0x00007ffa0ec2a307	(chrome.dll -execution_context.cc:86)		blink::ExecutionContext::From(blink::ScriptState const *)
0x00007ffa1514139f	(chrome.dll -video_encoder.cc:116)		blink::`anonymous namespace'::DeleteLater
0x00007ffa1514139f	(chrome.dll -video_encoder.cc:1131)		blink::isConfigSupportedWithSoftwareOnly::<lambda_4>::operator()
0x00007ffa1514139f	(chrome.dll -bind_internal.h:522)		base::internal::FunctorTraits<`lambda at ../../third_party/blink/renderer/modules/webcodecs/video_encoder.cc:1125:24',void>::Invoke
0x00007ffa1514139f	(chrome.dll -bind_internal.h:826)		base::internal::InvokeHelper<0,void,0,1,2>::MakeItSo
0x00007ffa1514139f	(chrome.dll -bind_internal.h:920)		base::internal::Invoker<base::internal::BindState<`lambda at ../../third_party/blink/renderer/modules/webcodecs/video_encoder.cc:1125:24',std::Cr::unique_ptr<media::VideoEncoder,std::Cr::default_delete<media::VideoEncoder> >,blink::internal::BasicUnwrappingCrossThreadHandle<blink::ScriptPromiseResolver,blink::internal::StrongCrossThreadHandleWeaknessPolicy>,blink::internal::BasicUnwrappingCrossThreadHandle<blink::VideoEncoderSupport,blink::internal::StrongCrossThreadHandleWeaknessPolicy> >,void (media::TypedStatus<media::EncoderStatusTraits>)>::RunImpl
0x00007ffa1514139f	(chrome.dll -bind_internal.h:871)		base::internal::Invoker<base::internal::BindState<`lambda at ../../third_party/blink/renderer/modules/webcodecs/video_encoder.cc:1125:24',std::Cr::unique_ptr<media::VideoEncoder,std::Cr::default_delete<media::VideoEncoder> >,blink::internal::BasicUnwrappingCrossThreadHandle<blink::ScriptPromiseResolver,blink::internal::StrongCrossThreadHandleWeaknessPolicy>,blink::internal::BasicUnwrappingCrossThreadHandle<blink::VideoEncoderSupport,blink::internal::StrongCrossThreadHandleWeaknessPolicy> >,void (media::TypedStatus<media::EncoderStatusTraits>)>::RunOnce
0x00007ffa0f9a6c0f	(chrome.dll -callback.h:145)		??base::OnceCallback<void (media::TypedStatus<media::D3D11StatusTraits>)>::Run
0x00007ffa102045ae	(chrome.dll -bind_internal.h:750)		??base::internal::FunctorTraits<base::OnceCallback<void (media::TypedStatus<media::D3D11StatusTraits>)>,void>::Invoke
0x00007ffa102045ae	(chrome.dll -bind_internal.h:826)		??base::internal::InvokeHelper<0,void,0>::MakeItSo
0x00007ffa102045ae	(chrome.dll -bind_internal.h:920)		??base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (media::TypedStatus<media::D3D11StatusTraits>)>,media::TypedStatus<media::D3D11StatusTraits> >,void ()>::RunImpl
0x00007ffa102045ae	(chrome.dll -bind_internal.h:871)		??base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (media::TypedStatus<media::D3D11StatusTraits>)>,media::TypedStatus<media::D3D11StatusTraits> >,void ()>::RunOnce
0x00007ffa0f3a4d29	(chrome.dll -callback.h:145)		base::OnceCallback<void ()>::Run
0x00007ffa0f3a4d29	(chrome.dll -task_annotator.cc:133)		base::TaskAnnotator::RunTaskImpl
0x00007ffa0f3a4d29	(chrome.dll -task_annotator.h:72)		base::TaskAnnotator::RunTask
0x00007ffa0f3a4d29	(chrome.dll -thread_controller_with_message_pump_impl.cc:441)		base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl
0x00007ffa0f3a4d29	(chrome.dll -thread_controller_with_message_pump_impl.cc:297)		base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
0x00007ffa0ef65075	(chrome.dll -message_pump_default.cc:40)		base::MessagePumpDefault::Run(base::MessagePump::Delegate *)
0x00007ffa0b2b12e3	(chrome.dll -thread_controller_with_message_pump_impl.cc:600)		base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool,base::TimeDelta)
0x00007ffa0b20fae6	(chrome.dll -run_loop.cc:141)		base::RunLoop::Run(base::Location const &)
0x00007ffa0d9f458a	(chrome.dll -renderer_main.cc:313)		content::RendererMain(content::MainFunctionParams)
0x00007ffa0d77bd76	(chrome.dll -content_main_runner_impl.cc:752)		content::RunOtherNamedProcessTypeMain(std::Cr::basic_string<char,std::Cr::char_traits<char>,std::Cr::allocator<char> > const &,content::MainFunctionParams,content::ContentMainDelegate *)
0x00007ffa0b3bf0e2	(chrome.dll -content_main_runner_impl.cc:1104)		content::ContentMainRunnerImpl::Run()
0x00007ffa0b3be79f	(chrome.dll -content_main.cc:342)		content::RunContentProcess
0x00007ffa0b3be79f	(chrome.dll -content_main.cc:370)		content::ContentMain(content::ContentMainParams)
0x00007ffa0b3bb8ab	(chrome.dll -chrome_main.cc:175)		ChromeMain
0x00007ff60e9673c3	(chrome.exe -main_dll_loader_win.cc:166)		MainDllLoader::Launch(HINSTANCE__ *,base::TimeTicks)
0x00007ff60e966cfb	(chrome.exe -chrome_exe_main_win.cc:391)		wWinMain
0x00007ff60ea2b2d1	(chrome.exe -exe_common.inl:118)		invoke_main
0x00007ff60ea2b2d1	(chrome.exe -exe_common.inl:288)		__scrt_common_main_seh
0x00007ffa8d9d7033	(KERNEL32.DLL + 0x00017033)		BaseThreadInitThunk
0x00007ffa8de826a0	(ntdll.dll + 0x000526a0)		RtlUserThreadStart

Task trace
0x00007ffa0d0c82d0	(chrome.dll -scoped_refptr.h:244)		scoped_refptr<base::internal::BindStateBase>::scoped_refptr
0x00007ffa0d0c82d0	(chrome.dll -callback_internal.h:174)		base::internal::CallbackBase::CallbackBase
0x00007ffa0d0c82d0	(chrome.dll -callback.h:119)		base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>::OnceCallback
0x00007ffa0d0c82d0	(chrome.dll -vpx_video_encoder.cc:241)		media::VpxVideoEncoder::Initialize(media::VideoCodecProfile,media::VideoEncoder::Options const &,base::RepeatingCallback<void >,base::OnceCallback<void >)

### so...@gmail.com (2022-10-19)

My last repro on stable: ed654599950b36c9

The reproduction in stable is really hard, rarely crashing. If I true, then helps, if I do any cpu intensive task parallel outside chrome (like rendering in blender, build a large source code, etc).

### gi...@appspot.gserviceaccount.com (2022-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2acf28478008315f302fd52b571623e784be707b

commit 2acf28478008315f302fd52b571623e784be707b
Author: Eugene Zemtsov <eugene@chromium.org>
Date: Thu Oct 20 19:11:49 2022

webcodecs: Fix race in VE.isConfigSupported() promise resolution

If the context is destroyed before VideoEncoder calls `done_callback`, bad
things can happen. That's why we extract a callback runner before doing
anything asynchronous. Since we hold a ref-counted pointer to the
runner it should be safe now.

Bug: 1375059
Change-Id: I984ab27e03e50bd5ae4bf0eb13431834b14f89b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3965544
Commit-Queue: Eugene Zemtsov <eugene@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1061737}

[modify] https://crrev.com/2acf28478008315f302fd52b571623e784be707b/third_party/blink/renderer/modules/webcodecs/video_encoder.cc


### eu...@chromium.org (2022-10-20)

[Empty comment from Monorail migration]

### eu...@chromium.org (2022-10-21)

[Empty comment from Monorail migration]

### eu...@chromium.org (2022-10-21)

sokkis@ could you please validate that the latest Chrome canary can't be crashed this way anymore? 

### [Deleted User] (2022-10-21)

Merge approved: your change passed merge requirements and is auto-approved for M108. Please go ahead and merge the CL to branch 5359 (refs/branch-heads/5359) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-21)

Merge review required: M107 has already been cut for stable release.

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

### eu...@chromium.org (2022-10-21)

1. Why does your merge fit within the merge criteria for these milestones?
Fixing UaF in the renderer 

2. What changes specifically would you like to merge? Please link to Gerrit.
 https://chromium-review.googlesource.com/c/chromium/src/+/3965544

3. Have the changes been released and tested on canary?
yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
no

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
yes, please use steps from https://crbug.com/chromium/1375059#c1


### so...@gmail.com (2022-10-22)

I tried it and I can't crash the canary.

Thank you for the fix!
Peter

### [Deleted User] (2022-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-23)

[Empty comment from Monorail migration]

### sr...@google.com (2022-10-24)

The bug has been approved for a merge to M108 branch, Please complete your merges asap today before 3pm PST so they can be included in the RC build for this week ( dev release tomorrow and same build promoting to beta this thursday)

### am...@chromium.org (2022-10-24)

Thanks for fixing this issue, this is a high severity security bug, so this fix should also be backmerged to 106/Extended; added label accordingly. 
Merge for both 106 and 107 will need be deferred until later this week as m107 stable is released tomorrow and 106 Extended is being delayed to the following day. 
I'll revisit for review and approval later this week. 

In the future, please do not manually add merge review and request labels. Once the issue is fixed, please simply update status as Fixed and the bot will update accordingly with the appropriate labels based on severity and impact. :) 

### gi...@appspot.gserviceaccount.com (2022-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/59cc9d850e55f88a677fab5d06809fd0ae8e79c3

commit 59cc9d850e55f88a677fab5d06809fd0ae8e79c3
Author: Eugene Zemtsov <eugene@chromium.org>
Date: Mon Oct 24 22:59:42 2022

webcodecs: Fix race in VE.isConfigSupported() promise resolution

If the context is destroyed before VideoEncoder calls `done_callback`, bad
things can happen. That's why we extract a callback runner before doing
anything asynchronous. Since we hold a ref-counted pointer to the
runner it should be safe now.

(cherry picked from commit 2acf28478008315f302fd52b571623e784be707b)

Bug: 1375059
Change-Id: I984ab27e03e50bd5ae4bf0eb13431834b14f89b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3965544
Commit-Queue: Eugene Zemtsov <eugene@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1061737}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3975890
Auto-Submit: Eugene Zemtsov <eugene@chromium.org>
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#273}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/59cc9d850e55f88a677fab5d06809fd0ae8e79c3/third_party/blink/renderer/modules/webcodecs/video_encoder.cc


### am...@chromium.org (2022-10-31)

107 merge approved, please merge this fix to branch 5304 by 11am PST Friday, 4 November so this fix can be included in the next 107/stable security refresh
106 merge approved, please merge this fix to branch 5249 by 11am PST Friday, 4 November so this fix can be included in the next 106/extended stable security refresh 

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. In the interim, please let us know what name/tag/handle you would like us to use in acknowledging you for discovering and reporting this issue. 

Thank you for your efforts in discovering and reporting this issue to us! Nice work! 

### so...@gmail.com (2022-11-03)

Thank you!

I would like to use my full name: Peter Nemeth

### [Deleted User] (2022-11-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-04)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wo...@chromium.org (2022-11-04)

My attempt to cherry pick https://chromium-review.googlesource.com/c/chromium/src/+/3965544 to 107 (refs/branch-heads/5304) via gerrit UI showed failure due to  merge conflicts.

### wo...@chromium.org (2022-11-04)

(investigating merge-conflicts in manual cherry-pick locally; eugene@ may be back at desk soon also to take a look)


### eu...@chromium.org (2022-11-04)

I'll take a look soon.

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3224ac18acbb307c5a9b39beb30de4a43e6f3ad9

commit 3224ac18acbb307c5a9b39beb30de4a43e6f3ad9
Author: Matt Wolenetz <wolenetz@chromium.org>
Date: Fri Nov 04 21:57:02 2022

[To 107] webcodecs: Fix race in VE.isConfigSupported() promise resolution

If the context is destroyed before VideoEncoder calls `done_callback`, bad
things can happen. That's why we extract a callback runner before doing
anything asynchronous. Since we hold a ref-counted pointer to the
runner it should be safe now.

(cherry picked from commit 2acf28478008315f302fd52b571623e784be707b)

Bug: 1375059
Change-Id: I984ab27e03e50bd5ae4bf0eb13431834b14f89b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3965544
Commit-Queue: Eugene Zemtsov <eugene@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1061737}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4006476
Reviewed-by: Eugene Zemtsov <eugene@chromium.org>
Commit-Queue: Matthew Wolenetz <wolenetz@chromium.org>
Cr-Commit-Position: refs/branch-heads/5304@{#1173}
Cr-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}

[modify] https://crrev.com/3224ac18acbb307c5a9b39beb30de4a43e6f3ad9/third_party/blink/renderer/modules/webcodecs/video_encoder.cc


### gi...@appspot.gserviceaccount.com (2022-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a1cbf05b41630f8a1c5d080d6f3b04e1c1818388

commit a1cbf05b41630f8a1c5d080d6f3b04e1c1818388
Author: Matt Wolenetz <wolenetz@chromium.org>
Date: Fri Nov 04 22:06:47 2022

[M106] webcodecs: Fix race in VE.isConfigSupported() promise resolution

If the context is destroyed before VideoEncoder calls `done_callback`, bad
things can happen. That's why we extract a callback runner before doing
anything asynchronous. Since we hold a ref-counted pointer to the
runner it should be safe now.

(cherry picked from commit 2acf28478008315f302fd52b571623e784be707b)

Bug: 1375059
Change-Id: I984ab27e03e50bd5ae4bf0eb13431834b14f89b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3965544
Commit-Queue: Eugene Zemtsov <eugene@chromium.org>
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1061737}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4005574
Reviewed-by: Matthew Wolenetz <wolenetz@chromium.org>
Cr-Commit-Position: refs/branch-heads/5249@{#911}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/a1cbf05b41630f8a1c5d080d6f3b04e1c1818388/third_party/blink/renderer/modules/webcodecs/video_encoder.cc


### rz...@google.com (2022-11-07)

[Empty comment from Monorail migration]

### rz...@google.com (2022-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-07)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-11-07)

1. Just https://crrev.com/c/4002979
2. Low, simple naming conflicts
3. 106, 107, 108
4. Yes

### am...@chromium.org (2022-11-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-08)

[Empty comment from Monorail migration]

### gm...@google.com (2022-11-08)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-09)

[Empty comment from Monorail migration]

### gm...@google.com (2022-11-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cf188ee814557945f2da184b5fbf7c31410c42e6

commit cf188ee814557945f2da184b5fbf7c31410c42e6
Author: Matt Wolenetz <wolenetz@chromium.org>
Date: Wed Nov 16 10:21:34 2022

[M102-LTS] webcodecs: Fix race in VE.isConfigSupported() promise resolution

If the context is destroyed before VideoEncoder calls `done_callback`, bad
things can happen. That's why we extract a callback runner before doing
anything asynchronous. Since we hold a ref-counted pointer to the
runner it should be safe now.

(cherry picked from commit 2acf28478008315f302fd52b571623e784be707b)

(cherry picked from commit a1cbf05b41630f8a1c5d080d6f3b04e1c1818388)

Bug: 1375059
Change-Id: I984ab27e03e50bd5ae4bf0eb13431834b14f89b7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3965544
Commit-Queue: Eugene Zemtsov <eugene@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1061737}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4005574
Cr-Original-Commit-Position: refs/branch-heads/5249@{#911}
Cr-Original-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4002979
Reviewed-by: Michael Ershov <miersh@google.com>
Reviewed-by: Eugene Zemtsov <eugene@chromium.org>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1389}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/cf188ee814557945f2da184b5fbf7c31410c42e6/third_party/blink/renderer/modules/webcodecs/video_encoder.cc


### vo...@google.com (2022-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1375059?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061367)*
