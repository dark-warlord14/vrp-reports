# Heap-use-after-free in content::GpuChannelHost::DestroyChannel()

| Field | Value |
|-------|-------|
| **Issue ID** | [40081247](https://issues.chromium.org/issues/40081247) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pi...@chromium.org |
| **Created** | 2015-01-23 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

render\_thread\_impl.cc/h contains the code which causes this use after free.  

render\_thread\_impl.cc has these two variables.

1. scoped\_refptr[webkit::gpu::ContextProviderWebContext](javascript:void(0);) shared\_main\_thread\_contexts\_;
2. scoped\_refptr<GpuChannelHost> gpu\_channel\_

gpu\_channel\_ is passed as a parameter when shared\_main\_thread\_contexts\_ is created.  

When GPU process is terminated render\_thread\_impl.cc creates a new gpu\_channel\_, but does not  

update the gpu\_channel\_ passed to shared\_main\_thread\_contexts\_.  

This behaviour causes use after free of message loop when current process is shut down.

**VERSION**  

Chrome Version: [41.0.2272.16 (64-bit)] + [beta]  

\*Does not reproduce in official beta version 41.0.2272.16  

But reproces in beta version 41.0.2272.16 (64-bit) built with Address Sanitizer.  

Beta version with address sanitizer is downloaded from  

<https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-beta-41.0.2272.16.zip?generation=1421974747540000&alt=media>.  

**Operating System: [Please indicate OS, version, and service pack level]**

```
            [42.0.2285.0 (64-bit)] + [trunk build}  

```

OS : Ubuntu Linux 14.04 64 bit  

Graphics Card: Radeon HD 6370

**REPRODUCTION CASE**

1. Start chrome built with address sanitizer on linux terminal.
2. Download and run testcase\_gpu.html.
3. Wait about 30 seconds till page is redirected to google.com. Sometimes it may take more time.
4. Tab will not display sad tab.  
   
   But address sanitizer output will be displayed on terminal.

\* This test case tries to hang and terminate gpu process.  

crashGpu() method of testcase\_gpu.html contains code which is used to hang gpu process.  

It is possible that this code may not hang your gpu process depending on your graphics card and system configuration.

In that case please follow these steps.

1. Start chrome built with address sanitizer on linux terminal.
2. Download and run testcase\_gpu.html.
3. Open chrome task manager and select GPU process.
4. Click "End Process" button.
5. Page will redirect to google.com.
6. Address sanitizer output will be displayed on terminal.

## **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: [Does not crash current tab. UAF happens when previous process of current tab shuts down, when new process for current tab is created when test case redirects page to google.com.] Crash State: Address sanitizer output

==5747==ERROR: AddressSanitizer: heap-use-after-free on address 0x61200000b6e8 at pc 0x7fe402b0bace bp 0x7fff5d6b47e0 sp 0x7fff5d6b47d8  

READ of size 8 at 0x61200000b6e8 thread T0 (chrome)  

#0 0x7fe402b0bacd in scoped\_refptr[base::internal::IncomingTaskQueue](javascript:void(0);)::operator->() const chrome/src/out/Release/../../base/memory/ref\_counted.h:303:5  

#1 0x7fe402b0c3dd in base::MessageLoop::PostNonNestableTask(tracked\_objects::Location const&, base::Callback<void ()> const&) chrome/src/out/Release/../../base/message\_loop/message\_loop.cc:289:3  

#2 0x7fe402b0e83a in base::MessageLoop::DeleteSoonInternal(tracked\_objects::Location const&, void (\*)(void const\*), void const\*) chrome/src/out/Release/../../base/message\_loop/message\_loop.cc:631:3  

#3 0x7fe40a24b997 in content::GpuChannelHost::DestroyChannel() chrome/src/out/Release/../../content/common/gpu/client/gpu\_channel\_host.cc:238:5  

#4 0x7fe40a24c61a in content::GpuChannelHost::~GpuChannelHost() chrome/src/out/Release/../../content/common/gpu/client/gpu\_channel\_host.cc:321:3  

#5 0x7fe40a24c6cd in content::GpuChannelHost::~GpuChannelHost() chrome/src/out/Release/../../content/common/gpu/client/gpu\_channel\_host.cc:320:35  

#6 0x7fe407940cf2 in scoped\_refptr[content::GpuChannelHost](javascript:void(0);)::operator=(content::GpuChannelHost\*) chrome/src/out/Release/../../base/memory/ref\_counted.h:313:7  

#7 0x7fe40a25b596 in content::WebGraphicsContext3DCommandBufferImpl::~WebGraphicsContext3DCommandBufferImpl() chrome/src/out/Release/../../content/common/gpu/client/webgraphicscontext3d\_command\_buffer\_impl.cc:119:3  

#8 0x7fe40a25b80d in content::WebGraphicsContext3DCommandBufferImpl::~WebGraphicsContext3DCommandBufferImpl() chrome/src/out/Release/../../content/common/gpu/client/webgraphicscontext3d\_command\_buffer\_impl.cc:114:46  

#9 0x7fe40a22e6c2 in content::ContextProviderCommandBuffer::~ContextProviderCommandBuffer() chrome/src/out/Release/../../content/common/gpu/client/context\_provider\_command\_buffer.cc:71:1  

#10 0x7fe40a22e78d in content::ContextProviderCommandBuffer::~ContextProviderCommandBuffer() chrome/src/out/Release/../../content/common/gpu/client/context\_provider\_command\_buffer.cc:59:63  

#11 0x7fe4080e4ed9 in content::RenderThreadImpl::~RenderThreadImpl() chrome/src/out/Release/../../content/renderer/render\_thread\_impl.cc:665:1  

#12 0x7fe4080e543d in content::RenderThreadImpl::~RenderThreadImpl() chrome/src/out/Release/../../content/renderer/render\_thread\_impl.cc:658:39  

#13 0x7fe40805737f in base::internal::scoped\_ptr\_impl<content::ChildThread, base::DefaultDeleter[content::ChildThread](javascript:void(0);) >::reset(content::ChildThread\*) chrome/src/out/Release/../../base/memory/scoped\_ptr.h:247:7  

#14 0x7fe408056e76 in content::ChildProcess::~ChildProcess() chrome/src/out/Release/../../content/child/child\_process.cc:68:5  

#15 0x7fe4081533db in content::RendererMain(content::MainFunctionParams const&) chrome/src/out/Release/../../content/renderer/renderer\_main.cc:231:3  

#16 0x7fe402a8960e in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) chrome/src/out/Release/../../content/app/content\_main\_runner.cc:347:14  

#17 0x7fe402a8b5e3 in content::ContentMainRunnerImpl::Run() chrome/src/out/Release/../../content/app/content\_main\_runner.cc:800:12  

#18 0x7fe402a88d43 in content::ContentMain(content::ContentMainParams const&) chrome/src/out/Release/../../content/app/content\_main.cc:19:15  

#19 0x7fe401cd9901 in ChromeMain chrome/src/out/Release/../../chrome/app/chrome\_main.cc:66:12  

#20 0x7fe3f7753ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287:0

0x61200000b6e8 is located 296 bytes inside of 320-byte region [0x61200000b5c0,0x61200000b700)  

freed by thread T0 (chrome) here:  

#0 0x7fe401cd8fb9 in operator delete(void\*) ??:0:0  

#1 0x7fe402b8346f in base::internal::scoped\_ptr\_impl<base::MessageLoop, base::DefaultDeleter[base::MessageLoop](javascript:void(0);) >::reset(base::MessageLoop\*) chrome/src/out/Release/../../base/memory/scoped\_ptr.h:247:7  

#2 0x7fe4080e593e in content::RenderThreadImpl::Shutdown() chrome/src/out/Release/../../content/renderer/render\_thread\_impl.cc:761:3  

#3 0x7fe408056e6c in content::ChildProcess::~ChildProcess() chrome/src/out/Release/../../content/child/child\_process.cc:67:5  

#4 0x7fe4081533db in content::RendererMain(content::MainFunctionParams const&) chrome/src/out/Release/../../content/renderer/renderer\_main.cc:231:3  

#5 0x7fe402a8960e in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) chrome/src/out/Release/../../content/app/content\_main\_runner.cc:347:14  

#6 0x7fe402a8b5e3 in content::ContentMainRunnerImpl::Run() chrome/src/out/Release/../../content/app/content\_main\_runner.cc:800:12  

#7 0x7fe402a88d43 in content::ContentMain(content::ContentMainParams const&) chrome/src/out/Release/../../content/app/content\_main.cc:19:15  

#8 0x7fe401cd9901 in ChromeMain chrome/src/out/Release/../../chrome/app/chrome\_main.cc:66:12  

#9 0x7fe3f7753ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287:0

previously allocated by thread T0 (chrome) here:  

#0 0x7fe401cd8a39 in operator new(unsigned long) ??:0:0  

#1 0x7fe40815315e in content::RendererMain(content::MainFunctionParams const&) chrome/src/out/Release/../../content/renderer/renderer\_main.cc:150:3  

#2 0x7fe402a8960e in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) chrome/src/out/Release/../../content/app/content\_main\_runner.cc:347:14  

#3 0x7fe402a8b5e3 in content::ContentMainRunnerImpl::Run() chrome/src/out/Release/../../content/app/content\_main\_runner.cc:800:12  

#4 0x7fe402a88d43 in content::ContentMain(content::ContentMainParams const&) chrome/src/out/Release/../../content/app/content\_main.cc:19:15  

#5 0x7fe401cd9901 in ChromeMain chrome/src/out/Release/../../chrome/app/chrome\_main.cc:66:12  

#6 0x7fe3f7753ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287:0

## Attachments

- [testcase_gpu.html](attachments/testcase_gpu.html) (text/html, 1.1 KB)
- [testcase_gpu2.html](attachments/testcase_gpu2.html) (text/html, 462 B)
- [chrome_gpu_output.html](attachments/chrome_gpu_output.html) (text/html, 36.1 KB)

## Timeline

### in...@chromium.org (2015-01-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-23)

Not a dup, confirmed by reporter from fix in 445741

### ri...@chromium.org (2015-01-23)

Thanks for the detailed report!

In the posted ASAN output, it looks like the following happened:

GpuChannelHost's destructor uses main_mesage_loop via RenderThreadImpl::GetMainLoop. Note that RenderThreadImpl::GetMainLoop returns a pointer to the main loop via the message_loop_ member of ChildThread and *not* main_message_loop_ in RenderThreadImpl, even though they have the same value. Thus, doing main_message_loop_.reset() does not clear message_loop_.

gpu_va_context_provider_ is created with a reference to the original GpuChannelHost
GPU process is killed, a new GpuChannelHost is created. Now gpu_va_context_provider_ holds the only ref to the GpuChannelHost.

Now, the renderer thread is shut down
~RenderThreadImpl()
  RenderThreadImpl::Shutdown()
    gpu_channel_->DestroyChannel() // but this is the newly created GpuChannelHost
    ...
    main_message_loop_.reset()  // The old GpuChannelHost will access this via message_loop_.
  gpu_va_context_provider_ is destroyed, it holds the only ref to its GpuChannelHost, so it destroys it, which calls DestroyChannel, which uses main_message_loop.

It looks a little dubious that scoped_refptr is used for GpuChannelHost since we know that the its lifetime may not exceed the lifetime of RenderThreadImpl.

As Chamal mentioned, it does look like a similar situation may be possible with shared_main_thread_contexts_ instead of gpu_va_context_provider_.

Going to err on the side of caution and mark this as high severity. This happens on a shutdown path, so there is little opportunity for an attacker to control the data at the freed object, but I'm not familiar enough with chrome architecture to rule out the possibility of other threads doing allocations at this time.

### kb...@chromium.org (2015-01-23)

Vangelis, could you help find another engineer on the team to diagnose this? I'm overcommitted.


### cl...@chromium.org (2015-01-23)

[Empty comment from Monorail migration]

### pi...@chromium.org (2015-01-24)

Another fallout of 53f081de05b86f73eca4e383a16c8dc723b78a99, I guess the fix in 445741 is not enough.

Previously we were deleting the main_message_loop_ only after gpu_va_context_provider_, media_thread_ and compositor_thread_ which should release all references to the channel.

So we may want to explicitly terminate/destroy those before we destroy main_message_loop_

### ch...@gmail.com (2015-01-24)

Inferno, Reply to https://crbug.com/chromium/451456#c2 -
I actually can't confirm that this is not a duplicate, because I don't have permission to see the test case of https://crbug.com/chromium/445741. Stack traces of both issues are similar.

Also fix for 445741 is not yet available because CQ failed again. 

### in...@chromium.org (2015-01-24)

Thanks Chamal for all your help and will definitely be considered by the reward panel. I will let haraken@ handle the triage for these 2 bugs, looks like piman@ already confirmed that yours is not a dupe.

### ha...@chromium.org (2015-01-26)

Uploaded a fix here (https://codereview.chromium.org/867553003/), but I cannot reproduce the crash and thus I cannot verify if the CL fixes the crash.

Chamal: Would you check if the CL fixes the crash?


### ch...@gmail.com (2015-01-26)

haraken, I can reproduce the crash after fix. I think fix handles the bug in gpu_va_context_provider_. This crash happens because of similar behavior in shared_main_thread_contexts_.

Did both methods listed under "REPRODUCTION CASE" in issue report fail to reproduce?

### cl...@chromium.org (2015-02-09)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-02-23)

[Comment Deleted]

### ch...@gmail.com (2015-02-23)

Issue report mentions 2 methods of reproducing.
1st method does not reproduce now.
Chrome tab will die with "He's Dead Jim" message, when test case attached in issue report is run.
Reason is test case attached in issue report is no longer able to terminate gpu process through gpu_watchdog_thread.cc.
I think gpu process is not terminated, because of the fix provided in
https://codereview.chromium.org/836473003. But I can't confirm.

Only the 2nd method reproduces now. But first need to comment crashGpu method in attached testcase_gpu.html. Otherwise tab will die with "He's Dead Jim" message.
Attached testcase_gpu2.html contains above mentioned change.

Reproduction Steps
-------------------
1. Start chrome built with address sanitizer on linux terminal.
2. Download and run testcase_gpu2.html.
3. Open chrome task manager and select GPU process.
4. Click "End Process" button.
5. Page will redirect to google.com.
6. Address sanitizer output will be displayed on terminal.

### cl...@chromium.org (2015-02-24)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-10)

haraken@: Uh oh! This issue is still open and hasn't been updated in the last 43 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-03-27)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### ha...@chromium.org (2015-03-28)

Fixed in https://codereview.chromium.org/1036773002/

### cl...@chromium.org (2015-03-28)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ch...@gmail.com (2015-03-30)

1. I can still reproduce this bug. 
   But now need to run chrome with --js-flags="--expose-gc" flag and execute steps mentioned in https://crbug.com/chromium/451456#c14.
2. Earlier --js-flags="--expose-gc" flag was not necessary, even if attached testcase had window.gc.
3. It is possible that my computer has some gpu configuration which triggers this bug only in that configuration. So I attached output of chrome://gpu.

4. It is also possible that there is something wrong with my chrome build.
   Haraken, Can you please give me a link to the chrome build you are testing?
   So I can download that build and test on my computer.


### ha...@chromium.org (2015-03-30)

I cannot reproduce the crash in ToT (r321347).

(BTW, I'm not an expert of GPU so it would be great if some expert could take over the bug.)


### in...@chromium.org (2015-03-30)

Chamal, can you please try using https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-322707.zip?generation=1427561378910000&alt=media

### kb...@chromium.org (2015-03-30)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-03-31)

I can reproduce this bug on my computer with chrome build downloaded from link in https://crbug.com/chromium/451456#c22.

Here is the updated reproduction steps with the new addition mentioned in https://crbug.com/chromium/451456#c20.

1. Download testcase_gpu2.html attached in https://crbug.com/chromium/451456#c14.
2. Open chrome with this command in a linux terminal.
   ./chrome --no-sandbox --js-flags="--expose-gc"
4. Open testcase_gpu2.html in chrome.
5. Open chrome task manager and select GPU process.
6. Click "End Process" button.
7. Page will redirect to google.com.
   * At this time tab process of testcase_gpu2.html will be shutdown and a new tab process for google.com will be launched by chrome. If bug does not reproduce please check chrome task manager to see wether this behaviour actually happens.
8. Address sanitizer output will be displayed on terminal.

   

### ti...@google.com (2015-04-08)

Moving back to state assigned while the new repro is checked out.

inferno@ - can you check to see if you can repro based on #24?

### ch...@gmail.com (2015-04-21)

Does steps mentioned in https://crbug.com/chromium/451456#c24 reproduce?


### mb...@chromium.org (2015-04-24)

I'm able to reproduce this using the steps from c#26. Also lowering the severity due to the amount of interaction involved.

vangelis: Could you please take a look or help find an owner for this one? (reassigning based on c#21)

### ti...@google.com (2015-05-07)

@vangelis: can you please provide an update on progress? What's the likelihood that you'll be able to land a fix by the end of next week?

### pi...@chromium.org (2015-05-07)

I can repro the UAF with asan on top-of-trunk.

### pi...@chromium.org (2015-05-07)

[Empty comment from Monorail migration]

### pi...@chromium.org (2015-05-07)

https://codereview.chromium.org/1128233004/ fixes this

### kb...@chromium.org (2015-05-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/765e52870520c6e60d913c307577c1d1fec3a381

commit 765e52870520c6e60d913c307577c1d1fec3a381
Author: piman <piman@chromium.org>
Date: Fri May 08 03:43:01 2015

Fix GpuChannelHost destruction and races

https://codereview.chromium.org/583043005 introduced
GpuChannelHost::DestroyChannel but it introduced a new state to GpuChannelHost
which was not captured everywhere and had races.

1- Ensure GpuChannelHost::DestroyChannel is always called on the main thread, before destruction.
2- properly handle the channel_ == NULL state.
3- Fix races (channel_ is used on any thread on windows, must be locked)

Also make sure contexts are destroyed before the channel, for sanity.

BUG=451456,471822

Review URL: https://codereview.chromium.org/1128233004

Cr-Commit-Position: refs/heads/master@{#328917}

[modify] http://crrev.com/765e52870520c6e60d913c307577c1d1fec3a381/content/browser/gpu/browser_gpu_channel_host_factory.cc
[modify] http://crrev.com/765e52870520c6e60d913c307577c1d1fec3a381/content/common/gpu/client/gpu_channel_host.cc
[modify] http://crrev.com/765e52870520c6e60d913c307577c1d1fec3a381/content/common/gpu/client/gpu_channel_host.h
[modify] http://crrev.com/765e52870520c6e60d913c307577c1d1fec3a381/content/renderer/render_thread_impl.cc


### in...@chromium.org (2015-05-08)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-05-20)

Chrome 43.0.2357.65 is released today. But this bug is not there in release notes.
Is this bug merged to chrome 43.0.2357.65 and is milestone flag correct?

Also is this eligible to go to reward-panel?

### pi...@chromium.org (2015-05-20)

This has not been merged to 43.

### mb...@chromium.org (2015-05-20)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-06-27)

It is possible to still reproduce this issue with asan build of chrome stable version 43.0.2357.130.
Are you planning to merge the fix to chrome version 44?

### pi...@chromium.org (2015-06-29)

It was landed before we branched for 44, so it should be in there.

### ti...@google.com (2015-06-29)

#38: Also, we'll take this through our next reward panel round, so you should have a decision on that in a few weeks.

Please feel free to test Chrome Beta to see if the fix is there.

### mb...@chromium.org (2015-07-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-14)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-08-17)

Congrats: $500 for this report.

### ti...@google.com (2015-08-28)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/451456?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/418206]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081247)*
