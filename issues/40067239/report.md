# I'm reporting an incomplete fix for a prior report (1451211) and (1427865).

| Field | Value |
|-------|-------|
| **Issue ID** | [40067239](https://issues.chromium.org/issues/40067239) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Blink>WebGPU, Internals>GPU>ANGLE, Internals>GPU>SwiftShader |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | au...@gmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2023-07-11 |
| **Bounty** | $15,000.00 |

## Description

**Steps to reproduce the problem:**  

Using multiple bugs in SwiftShader and Angle, the following simple shader code will lead to out-of-bounds accesses on the stack in the GPU process:

...  

uvec4 buf[0x7ffffff]  

out uvec4 value;  

...  

void main() {  

value = buf[0x414141];  

buf[0x414141] = 0x4242424242424242;  

}

See full report in <https://bugs.chromium.org/p/chromium/issues/detail?id=1451211>

**Problem Description:**  

We're concerned that the fix for [1427865](https://bugs.chromium.org/p/chromium/issues/detail?id=1427865) (i.e. the following change: <https://chromium-review.googlesource.com/c/angle/angle/+/4377639>) does not actually fix any of the bugs that are used by the PoC to gain out-of-bounds stack access. Please refer to the detailed report in [1451211](https://bugs.chromium.org/p/chromium/issues/detail?id=1451211), that explains the PoC in detail, provides a full root cause analysis and also demonstrates a full exploit achieving RCE in the GPU process.

I'll attach an updated PoC too in subsequent screens. Thank you for your patience!

**Additional Comments:**  

PoC attached. Thank you!

\*\*Chrome version: \*\* Version 114.0.5678.0 (Developer Build) (x86\_64) \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [simple_poc_new_lldb.log](attachments/simple_poc_new_lldb.log) (text/plain, 8.9 KB)
- [simple_poc_new.html](attachments/simple_poc_new.html) (text/plain, 5.2 KB)
- [simple_poc_new_2.html](attachments/simple_poc_new_2.html) (text/plain, 5.7 KB)
- [vertex-shader-orig.txt](attachments/vertex-shader-orig.txt) (text/plain, 2.6 KB)
- [vertex-shader-translated-gl.txt](attachments/vertex-shader-translated-gl.txt) (text/plain, 924.8 KB)
- [vertex-shader-translated-metal.txt](attachments/vertex-shader-translated-metal.txt) (text/plain, 8.7 KB)
- [chrome.patch](attachments/chrome.patch) (text/plain, 557 B)
- [simple_poc.html](attachments/simple_poc.html) (text/plain, 5.3 KB)

## Timeline

### [Deleted User] (2023-07-11)

[Empty comment from Monorail migration]

### ti...@chromium.org (2023-07-11)

If possible, please provide a POC that works on Stable at soonest.

Regardless, we agree with you that the underlying root cause hasn't been fully addressed in `Cfg::sortAndCombinAllocas` and there are definitely room for variants in the future.

geofflang@, kbr@, syoussefi@: could you take a look at this one?

[Monorail components: Internals>GPU>SwiftShader]

### kb...@chromium.org (2023-07-11)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-07-12)

(I'm not CC'd on https://crbug.com/chromium/1451211)

The POC above fails on Chrome Stable and Canary with:

    vertex error:
ERROR: 0:? : '' : Total size of declared private variables exceeds implementation-defined limit

While understanding the bailout wasn't a fix for the root cause, is there proof that it can be circumvented? In situations where fixing the underlying graphics driver stack wasn't an option, it's been necessary to add similar bailouts to ANGLE's shader compiler in the past.

Shabi, can you look further since you fixed https://crbug.com/chromium/1427865?


### da...@chromium.org (2023-07-12)

[Empty comment from Monorail migration]

### sy...@chromium.org (2023-07-12)

TBH, as long as SwiftShader is unstaffed, I don't anticipate the root cause would get fixed if it can no longer be triggered.

### kb...@chromium.org (2023-07-12)

Just received access to https://crbug.com/chromium/1451211 - that's a remarkable exploit chain. Thank you for investing so much time developing and reporting it.

Do you still see the ability to access an array out-of-bounds, even if isn't rejected by the filtering added in https://crbug.com/chromium/1427865?

Attached is a slightly modified simple_poc_new from above which shrinks the sizes of the arrays to get past the new size check. It unfortunately still crashes inside SwiftShader's rasterization routines per http://crash/0fa92896938e9b96 (Google-internal link):

0x00000000			
0x0000000109344e17	(libvk_swiftshader.dylib -Renderer.cpp:581)		sw::DrawCall::run(vk::Device*, marl::Pool<sw::DrawCall>::Loan const&, marl::Ticket::Queue*, marl::Ticket::Queue*)::$_1::operator()() const
0x0000000109344e17	(libvk_swiftshader.dylib -invoke.h:340)		decltype(std::declval<sw::DrawCall::run(vk::Device*, marl::Pool<sw::DrawCall>::Loan const&, marl::Ticket::Queue*, marl::Ticket::Queue*)::$_1&>()()) std::__Cr::__invoke<sw::DrawCall::run(vk::Device*, marl::Pool<sw::DrawCall>::Loan const&, marl::Ticket::Queue*, marl::Ticket::Queue*)::$_1&>(sw::DrawCall::run(vk::Device*, marl::Pool<sw::DrawCall>::Loan const&, marl::Ticket::Queue*, marl::Ticket::Queue*)::$_1&)
0x0000000109344e17	(libvk_swiftshader.dylib -invoke.h:415)		void std::__Cr::__invoke_void_return_wrapper<void, true>::__call<sw::DrawCall::run(vk::Device*, marl::Pool<sw::DrawCall>::Loan const&, marl::Ticket::Queue*, marl::Ticket::Queue*)::$_1&>(sw::DrawCall::run(vk::Device*, marl::Pool<sw::DrawCall>::Loan const&, marl::Ticket::Queue*, marl::Ticket::Queue*)::$_1&)
0x0000000109344e17	(libvk_swiftshader.dylib -function.h:239)		std::__Cr::__function::__default_alloc_func<sw::DrawCall::run(vk::Device*, marl::Pool<sw::DrawCall>::Loan const&, marl::Ticket::Queue*, marl::Ticket::Queue*)::$_1, void ()>::operator()()
0x0000000109344e17	(libvk_swiftshader.dylib -function.h:723)		void std::__Cr::__function::__policy_invoker<void ()>::__call_impl<std::__Cr::__function::__default_alloc_func<sw::DrawCall::run(vk::Device*, marl::Pool<sw::DrawCall>::Loan const&, marl::Ticket::Queue*, marl::Ticket::Queue*)::$_1, void ()>>(std::__Cr::__function::__policy_storage const*)
0x00000001093125cc	(libvk_swiftshader.dylib -function.h:854)		marl::Scheduler::Worker::runUntilIdle()
0x0000000109311c28	(libvk_swiftshader.dylib -scheduler.cpp:588)		marl::Scheduler::Worker::runUntilShutdown()
0x00000001093123ab	(libvk_swiftshader.dylib -scheduler.cpp:581)		marl::Scheduler::Worker::run()
0x00000001093147cf	(libvk_swiftshader.dylib -scheduler.cpp:385)		marl::Scheduler::Worker::start()::$_0::operator()() const
0x00000001093147cf	(libvk_swiftshader.dylib -invoke.h:340)		decltype(std::declval<marl::Scheduler::Worker::start()::$_0&>()()) std::__Cr::__invoke<marl::Scheduler::Worker::start()::$_0&>(marl::Scheduler::Worker::start()::$_0&)
0x00000001093147cf	(libvk_swiftshader.dylib -invoke.h:415)		void std::__Cr::__invoke_void_return_wrapper<void, true>::__call<marl::Scheduler::Worker::start()::$_0&>(marl::Scheduler::Worker::start()::$_0&)
0x00000001093147cf	(libvk_swiftshader.dylib -function.h:239)		std::__Cr::__function::__default_alloc_func<marl::Scheduler::Worker::start()::$_0, void ()>::operator()()
0x00000001093147cf	(libvk_swiftshader.dylib -function.h:723)		void std::__Cr::__function::__policy_invoker<void ()>::__call_impl<std::__Cr::__function::__default_alloc_func<marl::Scheduler::Worker::start()::$_0, void ()>>(std::__Cr::__function::__policy_storage const*)
0x000000010931716c	(libvk_swiftshader.dylib -function.h:854)		std::__Cr::__function::__policy_func<void ()>::operator()() const
0x000000010931716c	(libvk_swiftshader.dylib -function.h:1168)		std::__Cr::function<void ()>::operator()() const
0x000000010931716c	(libvk_swiftshader.dylib -thread.cpp:387)		marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::__Cr::function<void ()>&&)::'lambda'()::operator()() const
0x000000010931716c	(libvk_swiftshader.dylib -invoke.h:340)		decltype(std::declval<marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::__Cr::function<void ()>&&)::'lambda'()>()()) std::__Cr::__invoke<marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::__Cr::function<void ()>&&)::'lambda'()>(marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::__Cr::function<void ()>&&)::'lambda'()&&)
0x000000010931716c	(libvk_swiftshader.dylib -thread.h:193)		void std::__Cr::__thread_execute<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct>>, marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::__Cr::function<void ()>&&)::'lambda'()>(std::__Cr::tuple<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct>>, marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::__Cr::function<void ()>&&)::'lambda'()>&, std::__Cr::__tuple_indices<>)
0x000000010931716c	(libvk_swiftshader.dylib -thread.h:204)		void* std::__Cr::__thread_proxy<std::__Cr::tuple<std::__Cr::unique_ptr<std::__Cr::__thread_struct, std::__Cr::default_delete<std::__Cr::__thread_struct>>, marl::Thread::Impl::Impl(marl::Thread::Affinity&&, std::__Cr::function<void ()>&&)::'lambda'()>>(void*)
0x00007ff80c6421d2	(libsystem_pthread.dylib + 0x000061d2)		_pthread_start

Launching Chrome Canary on macOS x86_64 with:

/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary --user-data-dir=/tmp/c1 --use-angle=swiftshader
=> crash

/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary --user-data-dir=/tmp/c1 --use-angle=gl
=> occasional crash (don't yet have the stack trace from this - it might just be a watchdog timeout)

/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary --user-data-dir=/tmp/c1 --use-angle=metal
=> no crash

The OpenGL backend initializes all the global variables in one large and expensive autogenerated function, initGlobals(). Running the exploit hangs the GPU process for many seconds.

Can we try to understand better whether problematic GPU process crashes are still possible?


### kb...@chromium.org (2023-07-12)

There was an issue with the attachments while making the last comment.


### au...@gmail.com (2023-07-13)

Thanks you all for taking a look. I'm catching up so forgive me if I miss a prior question.

It seems like https://chromium-review.googlesource.com/c/angle/angle/+/4503753 also limited the total size across all private variables. We agree that with this change the updated PoC does not reproduce anymore. We didn't see this change anywhere in the issues so apologies for not testing with this applied as well.

Nevertheless, this still relies on the size validation (which as pointed out in the original report already calculates the size incorrectly when comparing with the size SwiftShader actually uses). Finding a bypass for this check would allow the PoC to work again.

This is also not the only problem with the current patch. The other major issue is that the size validation is only done for WebGL contexts (see [`TCompiler::shouldLimitTypeSizes`](https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/angle/src/compiler/translator/Compiler.cpp;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188;bpv=1;bpt=0;l=398)). Anyone with e.g. Mojo capability (for example an attacker with a renderer RCE) can still trigger the original PoC and this would still result in a Sandbox escape.

Since we do not have experience with Mojo and the GPU Mojo API is quite complex, we verified this by patching Chrome and making it think a WebGL context is also a normal OpenGLES2 context instead. This should be equivalent to an attacker doing the Mojo calls manually and setting the context type to OpenGLES2 instead of WebGL. The patch is attached. We've also attached a very slightly modified `simple_poc.html`, since the large array now needs to be manually initialized.

Lastly, it seems that WebGPU also does not have the type size limitations. Is WebGPU supported when running with SwiftShader? If so, this would be an alternative way to still get direct RCE (without renderer RCE).

Thank you!

### ti...@google.com (2023-07-13)

Thanks for the comment Auriela! I discovered crbug.com/1431761 by doing variant analysis on the original report. I've cc'd you to that issue so you can take a look and do more variant analysis if you'd like :)


Were you able to figure out a way to bypass the zero initialization in WebGPU (i.e. Tint will emit OpConstantNull's which will timeout in the GPU)?

### au...@gmail.com (2023-07-13)

Thank you for cc'ing me on 1431761, Tiszka. Is it possible for me to add a colleague to these reports for visibility? We work together and he developed the initial PoC. I think he'd be interested in your VA efforts too and would be able to respond faster than I can. It seems like I can't cc folks myself so I thought I'd ask.

(re: kb's questions, in case it's helpful) From our experience playing around with this, you are likely hitting a JIT compiler failure. Whenever we experienced such a crash we were hitting this particular code: https://source.chromium.org/chromium/chromium/src/+/main:third_party/swiftshader/third_party/subzero/src/IceTargetLoweringX8664.cpp;l=993-1003;bpv=1;bpt=0.
This happens because the JIT compiler has its own internal limit for the amount of permitted stack space.

Thanks!

### ti...@google.com (2023-07-13)

[Comment Deleted]

### ti...@google.com (2023-07-13)

re: aureliaformallaz@ yes just add their email in this report and I will CC them to 1431761

> This is also not the only problem with the current patch. The other major issue is that the size validation is only done for WebGL contexts (see [`TCompiler::shouldLimitTypeSizes`]
I traced through the mojo call and this appears to be the case. I think this is serious enough to be a bug of its own. Nice catch! (new bug here: crbug.com/1464682)

While re-reviewing the patches I also noticed that the size check in ValidateTypeSizeLimitations can also overflow, which can also be used to bypass the check [1] (new bug here: crbug.com/1464680)

Let's keep this bug focused on the overflow in SwiftShader and we can discuss the other two issues in 1464682 & 1464680. aureliaformallaz@ I CC'd you on both if you have anything to add :)

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/angle/src/compiler/translator/ValidateTypeSizeLimitations.cpp;l=245;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188

### kb...@chromium.org (2023-07-13)

The size check was deliberately restricted to WebGL contexts because ANGLE is a general-purpose OpenGL ES implementation, and adding this semi-arbitrary size limitation carries a high risk of breaking real-world content on other platforms. I would dispute the feasibility of triggering it from a compromised renderer; in my opinion, WebGL is needed to make the exploit feasible.

SwiftShader is supported as a WebGPU fallback, but it's not clear to me that this is triggerable from WebGPU vertex shaders since the mechanism for passing in data differs between WebGL and WebGPU. CC'ing enga@ and cwallez@.

tiszka@ graciously volunteered to try to harden SwiftShader's allocation paths - thank you - let me please reassign this while you're looking at it.


[Monorail components: Blink>WebGL Blink>WebGPU Internals>GPU>ANGLE]

### da...@chromium.org (2023-07-13)

Thanks Ken, could you clarify why this isn't possible to trigger from a compromised renderer?

### kb...@chromium.org (2023-07-13)

It seems to me exceedingly difficult to set up a new Mojo connection to the GPU process from a compromised renderer and set it up specifically to use a full GLES2 rather than a WebGL context, and then send it arbitrary commands.


### da...@chromium.org (2023-07-13)

Hm, I'd like to understand more, I'm not sure if my mental model here is the same. Difficulty is not part of the threat model, in the sense that it takes a bunch of engineering work to make it happen. Or is it difficult in the sense that you need to exploit bugs in another process to make it happen? What makes it difficult?

### kb...@chromium.org (2023-07-13)

Maybe my mental model is wrong. One would need to generate a large amount of executable code at run time, which itself would call into many entry points in the renderer process's base image and shared libraries, to set up an arbitrary Mojo connection to the GPU process.

Looking more at the code though, would the attacker only need to call CreateOffscreenGraphicsContext3DProvider with a ContextAttributes struct appropriately set up?
https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/renderer/renderer_blink_platform_impl.h;l=154;drc=3e7ca03f85a480f6ab1c70f03684877ba5cb26ab;bpv=0;bpt=1

If so then I'm wrong about the difficulty, regardless of whether that factors into the decision.


### da...@chromium.org (2023-07-13)

Thanks for helping me understand. The best way to think of a compromised renderer is it can do anything you can do with a patch to chrome. Hobbyists may not be able to do much with a compromise but industry players (vuln shops, govts) have capability to inject anything they'd like at that point.

Additionally, yes that looks like the entrypoint to set up the connection.

### [Deleted User] (2023-07-13)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-07-13)

Thanks for helping me understand too - I'll adjust my mental model of what a compromised renderer can do.

I didn't know, but syoussefi@ and geofflang@ are going to expand the shader variable size restrictions to all contexts in https://crbug.com/chromium/1464682, which should alleviate part of the concern here.


### [Deleted User] (2023-07-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### au...@gmail.com (2023-07-17)

Hello tiszka@ — would you please cc leio.galli@gmail.com on this and 1431761? Thank you!

### ti...@chromium.org (2023-07-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader/+/4e401427f8dd799b17ac6c805391e2da1e017672

commit 4e401427f8dd799b17ac6c805391e2da1e017672
Author: Brendon Tiszka <tiszka@chromium.org>
Date: Thu Jul 13 23:59:54 2023

[subzero] Fix integer overflows during alloca coalescing

Bug: chromium:1427865,chromium:1431761,chromium:1464038,chromium:1464680
Change-Id: Ie09a9ba3709d867544ca045b066b437e2d60da51
Reviewed-on: https://swiftshader-review.googlesource.com/c/SwiftShader/+/71928
Kokoro-Result: kokoro <noreply+kokoro@google.com>
Reviewed-by: Shahbaz Youssefi <syoussefi@google.com>
Presubmit-Ready: Shahbaz Youssefi <syoussefi@google.com>
Reviewed-by: Ben Clayton <bclayton@google.com>
Tested-by: Shahbaz Youssefi <syoussefi@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@google.com>

[modify] https://swiftshader.googlesource.com/SwiftShader/+/4e401427f8dd799b17ac6c805391e2da1e017672/third_party/subzero/src/IceCfg.cpp


### ti...@chromium.org (2023-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@chromium.org (2023-07-18)

1. Which CLs should be backmerged? (Please include Gerrit links.)
https://swiftshader-review.googlesource.com/c/SwiftShader/+/71928

2. Has this fix been tested on Canary?
Yes, 117.0.5895.0

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
Yes it has been verified to not pose any stability regressions and it does not pose potential stability risks

4. Does this fix pose any known compatibility risks?
No

5. Does it require manual verification by the test team? If so, please describe required testing.
No, not required. 

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-19)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-20)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-21)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-21)

[Comment Deleted]

### am...@chromium.org (2023-07-21)

https://swiftshader-review.googlesource.com/c/SwiftShader/+/71928 was already approved for merge via review in 1464680
As also mentioned there, despite git watcher not updating this bug with the autoroller status from the second fix, it appears it was actually picked up in a swiftshader roll: https://dawn-review.googlesource.com/c/dawn/+/141700

Merges approved for 116, 115, and 114 
At your earliest convenience please merge this fix to branch 5845 -- M116/beta, branch 5790 -- M115/Stable, and branch 5735 -- M114/Extended 
Please complete all merges by EOD Tuesday, 25 July so this fix can be included in the next updates for all active release branches -- ty!

### am...@chromium.org (2023-07-21)

(round 2, because I borked this up earlier) cc'ing another external party based on the explicit request of the external reporter in https://crbug.com/chromium/1464038#c23 

### gi...@appspot.gserviceaccount.com (2023-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/83b0bdb696d81b2d94e3aee77b3b6f86b96274c3

commit 83b0bdb696d81b2d94e3aee77b3b6f86b96274c3
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jul 24 17:52:17 2023

Roll SwiftShader from 222e07b368b1 to 8d9a45b1f3ab (12 revisions)

https://swiftshader.googlesource.com/SwiftShader.git/+log/222e07b368b1..8d9a45b1f3ab

2023-07-24 bclayton@google.com LLVMReactor: Remove CreateFreeze() call
2023-07-23 bclayton@google.com LLVMReactor: Clamp RHS of bit shifts using type width
2023-07-22 bclayton@google.com Fix another 'sign-compare' warning as error
2023-07-22 bclayton@google.com Fix 'sign-compare' warning as error
2023-07-21 bclayton@google.com LLVMReactor: Clamp RHS of bit shifts.
2023-07-21 swiftshader.regress@gmail.com Regres: Update test lists @ 4a260c12
2023-07-21 bclayton@google.com ExecutableMemory: Use VirtualAlloc() instead of `new` on windows
2023-07-20 avi@google.com Don't allow Swiftshader to be compiled as ARC
2023-07-18 tiszka@chromium.org [subzero] Fix integer overflows during alloca coalescing
2023-07-12 aredulla@google.com [ssci] Added Shipped field to READMEs
2023-07-11 jif@google.com [LLVM 16] Have Swiftshader built with Android.bp use LLVM 16.
2023-07-04 jif@google.com [LLVM 16] Shifts do not generate poison values

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/swiftshader-chromium-autoroll
Please CC capn@chromium.org,swiftshader-eng+autoroll@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in SwiftShader: https://bugs.chromium.org/p/swiftshader/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:linux_chromium_msan_rel_ng;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1427865,chromium:1431761,chromium:1464038,chromium:1464680,chromium:1466124,chromium:733237
Tbr: swiftshader-eng+autoroll@google.com
Change-Id: Ifea78e22e4b836267a9094fffa87ddda27516f1c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4711308
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1174303}

[modify] https://crrev.com/83b0bdb696d81b2d94e3aee77b3b6f86b96274c3/DEPS


### [Deleted User] (2023-07-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-27)

as discussed in issue https://bugs.chromium.org/p/chromium/issues/detail?id=1464680#c34 and c#33 we can defer backmerge of https://swiftshader-review.googlesource.com/c/SwiftShader/+/71928 

updating merge labels 

### am...@google.com (2023-07-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-27)

Congratulations! The VRP Panel has decided to award you $15,000 for this report of a GPU process memory corruption bug and the variant analysis that resulted from it. A member of our finance team will be in touch to arrange payment. In the meantime, please let us know how you would like to be acknowledged for this issue in our security fix notes. 
We sincerely appreciate you for taking the time and effort to follow-up on this issue and provide this detailed report and insight to us! 

### am...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### au...@gmail.com (2023-08-01)

Thank you Amy & team. For the security fix notes, please attribute this report to 'Apple Security Engineering and Architecture (SEAR)'

### am...@chromium.org (2023-08-01)

While the swiftshader change was not merged here, the hotfix for this change was landed and merged through work on https://crbug.com/chromium/1464682, which is shipping in tomorrow's M115 security update. Labeling this issue according so it can be included and acknowledged in release notes. 

Thank you OP for providing attribution information for that. Your work will be acknowledged accordingly as requested! 

### am...@google.com (2023-08-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1464038?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WebGL, Blink>WebGPU, Internals>GPU>ANGLE, Internals>GPU>SwiftShader]
[Monorail blocked-on: crbug.com/chromium/1427865, crbug.com/chromium/1451211, crbug.com/chromium/1464682]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067239)*
