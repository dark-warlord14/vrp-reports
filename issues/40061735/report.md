# blink::MediaInspectorContextImpl::CullPlayers

| Field | Value |
|-------|-------|
| **Issue ID** | [40061735](https://issues.chromium.org/issues/40061735) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>WebCodecs, Blink>Scheduling |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | tm...@chromium.org |
| **Created** | 2022-11-14 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

os:  

ubuntu 22.04  

chrome version:  

Chromium 109.0.5410.0

repro step:  

Because the repro is not stable, I have no poc yet.  

But I may know what caused it.  

There are 4 related historical issues, and the list is as follows:  

(a)<https://bugs.chromium.org/p/chromium/issues/detail?id=1317714>  

(b)<https://bugs.chromium.org/p/chromium/issues/detail?id=1295786>  

(c)<https://bugs.chromium.org/p/chromium/issues/detail?id=1309120>  

(d)<https://bugs.chromium.org/p/chromium/issues/detail?id=1154468>

[1]The patch of (issue-a) is as follows(please see <https://chromium-review.googlesource.com/c/chromium/src/+/3682060> for more details):  

diff --git a/third\_party/blink/renderer/modules/webcodecs/codec\_logger.h b/third\_party/blink/renderer/modules/webcodecs/codec\_logger.h  

index 5d3f9fd5..034c448 100644  

--- a/third\_party/blink/renderer/modules/webcodecs/codec\_logger.h  

+++ b/third\_party/blink/renderer/modules/webcodecs/codec\_logger.h  

@@ -9,10 +9,10 @@  

#include <string>  

#include "base/check.h"  

+#include "base/location.h"  

...  

-#include "base/location.h"  

...  

@@ -72,9 +72,17 @@  

// This allows us to destroy |parent\_media\_log\_| and stop logging,  

// without causing problems to |media\_log\_| users.  

media\_log\_ = parent\_media\_log\_->Clone();  

+

- task\_runner\_ = task\_runner;  
  
  }

- ~CodecLogger() { DCHECK\_CALLED\_ON\_VALID\_SEQUENCE(sequence\_checker\_); }

- ~CodecLogger() {
- DCHECK\_CALLED\_ON\_VALID\_SEQUENCE(sequence\_checker\_);
- // media logs must be posted for destruction, since they can cause the
- // garbage collector to trigger an immediate cleanup and delete the owning
- // instance of |CodecLogger|.
- task\_runner\_->DeleteSoon(FROM\_HERE, std::move(parent\_media\_log\_));
- }
  
  void SendPlayerNameInformation(const ExecutionContext& context,  
  
  std::string loadedAs) {  
  
  @@ -135,6 +143,9 @@  
  
  // can be safely accessed, and whose raw pointer can be given callbacks.  
  
  std::unique\_ptr[media::MediaLog](javascript:void(0);) media\_log\_;
- // Keep task runner around for posting the media log to upon destruction.
- scoped\_refptr[base::SingleThreadTaskRunner](javascript:void(0);) task\_runner\_;
- SEQUENCE\_CHECKER(sequence\_checker\_);  
  
  };

[2]task\_runner\_->DeleteSoon was re-disabled in a new CL on October 28, resulting the old uaf.  

<https://chromium-review.googlesource.com/c/chromium/src/+/3988688>  

diff --git a/third\_party/blink/renderer/modules/webcodecs/codec\_logger.h b/third\_party/blink/renderer/modules/webcodecs/codec\_logger.h  

index 0d97b9b0..8a0891f 100644  

--- a/third\_party/blink/renderer/modules/webcodecs/codec\_logger.h  

+++ b/third\_party/blink/renderer/modules/webcodecs/codec\_logger.h  

@@ -83,7 +83,10 @@  

// instance of |CodecLogger|.  

if (parent\_media\_log\_) {  

parent\_media\_log\_->Stop();

- ```
   task_runner_->DeleteSoon(FROM_HERE, std::move(parent_media_log_));  
  
  ```

- ```
   // This task runner may be destroyed without running tasks, so don't use  
  
  ```
- ```
   // DeleteSoon() which can leak the log. See https://crbug.com/1376851.  
  
  ```
- ```
   task_runner_->PostTask(FROM_HERE, base::DoNothingWithBoundArgs(  
  
  ```
- ```
                                         std::move(parent_media_log_)));  
  
  ```
  }  
  
  }  
  
  When I was testing, except for the poc from issue-c((<https://bugs.chromium.org/p/chromium/issues/detail?id=1309120>)), none of them were successfully reproduced.  
  
  The UAF can be successfully reproduced after minor modification, but it is stil not stable.It reproed after running for more than 20 minutes.

**Problem Description:**  

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6150000e70f0 at pc 0x56166d33ee0a bp 0x7ffc81142450 sp 0x7ffc81142448  

READ of size 8 at 0x6150000e70f0 thread T0 (chrome)  

#0 0x56166d33ee09 in get ./../../base/memory/scoped\_refptr.h:264:27  

#1 0x56166d33ee09 in Impl ./../../third\_party/blink/renderer/platform/wtf/text/wtf\_string.h:126:43  

#2 0x56166d33ee09 in blink::WebString::WebString(WTF::String const&) ./../../third\_party/blink/renderer/platform/exported/web\_string.cc:154:54  

#3 0x56166b723f40 in blink::MediaInspectorContextImpl::CullPlayers(blink::WebString const&) ./../../third\_party/blink/renderer/core/inspector/inspector\_media\_context\_impl.cc:113:18  

#4 0x56166b7262dd in blink::MediaInspectorContextImpl::NotifyPlayerEvents(blink::WebString, blink::WebVector[blink::InspectorPlayerEvent](javascript:void(0);) const&) ./../../third\_party/blink/renderer/core/inspector/inspector\_media\_context\_impl.cc:182:7  

#5 0x561671f5e75f in content::InspectorMediaEventHandler::SendQueuedMediaEvents(std::Cr::vector<media::MediaLogRecord, std::Cr::allocator[media::MediaLogRecord](javascript:void(0);)>) ./../../content/renderer/media/inspector\_media\_event\_handler.cc:157:25  

#6 0x561671f66c4e in content::BatchingMediaLog::SendQueuedMediaEvents() ./../../content/renderer/media/batching\_media\_log.cc:236:14  

#7 0x561671f6d343 in Invoke<void (content::BatchingMediaLog::\*)(), base::WeakPtr[content::BatchingMediaLog](javascript:void(0);) > ./../../base/functional/bind\_internal.h:646:12  

#8 0x561671f6d343 in MakeItSo<void (content::BatchingMediaLog::\*)(), std::Cr::tuple<base::WeakPtr[content::BatchingMediaLog](javascript:void(0);) > > ./../../base/functional/bind\_internal.h:847:5  

#9 0x561671f6d343 in RunImpl<void (content::BatchingMediaLog::\*)(), std::Cr::tuple<base::WeakPtr[content::BatchingMediaLog](javascript:void(0);) >, 0UL> ./../../base/functional/bind\_internal.h:919:12  

#10 0x561671f6d343 in base::internal::Invoker<base::internal::BindState<void (content::BatchingMediaLog::\*)(), base::WeakPtr[content::BatchingMediaLog](javascript:void(0);)>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:870:12  

#11 0x56165ef849f5 in Run ./../../base/functional/callback.h:174:12  

#12 0x56165ef849f5 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:154:32  

#13 0x56165efccf7c in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:450:11)> ./../../base/task/common/task\_annotator.h:84:5  

#14 0x56165efccf7c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:448:23  

#15 0x56165efcbf16 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:299:30  

#16 0x56165efce3fa in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#17 0x56165ee7f663 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:40:55  

#18 0x56165efcef6b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:608:12  

#19 0x56165ef0f4cd in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#20 0x561674e9b911 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer\_main.cc:313:16  

#21 0x56165dc87533 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:660:14  

#22 0x56165dc89623 in content::RunOtherNamedProcessTypeMain(std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:742:12  

#23 0x56165dc8b829 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1085:10  

#24 0x56165dc8402d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:342:36  

#25 0x56165dc84647 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:370:10  

#26 0x56164e7f6efe in ChromeMain ./../../chrome/app/chrome\_main.cc:174:12  

#27 0x7f8decd6ad8f in \_\_libc\_start\_call\_main ./csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

0x6150000e70f0 is located 368 bytes inside of 472-byte region [0x6150000e6f80,0x6150000e7158)  

freed by thread T0 (chrome) here:  

#0 0x56164e7c3b66 in free *asan\_rtl*:3  

#1 0x56165ae55cf1 in FreeVectorBacking ./../../third\_party/blink/renderer/platform/wtf/allocator/partition\_allocator.h:43:50  

#2 0x56165ae55cf1 in DeallocateBuffer ./../../third\_party/blink/renderer/pl

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.5410.0 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 32.8 KB)
- [launcher.sh](attachments/launcher.sh) (text/plain, 470 B)
- [crash.html](attachments/crash.html) (text/plain, 707 B)
- [xx.mp3](attachments/xx.mp3) (application/octet-stream, 2.3 KB)

## Timeline

### [Deleted User] (2022-11-14)

[Empty comment from Monorail migration]

### em...@gmail.com (2022-11-14)

[Comment Deleted]

### wf...@chromium.org (2022-11-14)

Hi thanks for your report. I'm not entirely sure what you are highlighting here.

As you highlight, there appears to be quite a lot of trunk churn going on here. I'm ccing a few developers out of courtesy but no action is required yet until we have a reproduction. 

Are you able to reproduce your issue on head of chromium or on any released channel of GOogle Chrome? Can you be specific as to which exact version(s) you can reproduce on?

Also, we will need a PoC to proceed further with this issue.



[Monorail components: Blink>Media>WebCodecs Blink>Scheduling]

### em...@gmail.com (2022-11-15)

Sorry, some statements were not made clear.
Yes, as described in the report above, I can reproduce it in version 109.0.5410.0.

I haven't uploaded a new poc for the time being, because the poc in my earlier report (issue-c:https://bugs.chromium.org/p/chromium/issues/detail?id=1309120) can be reproduced again.

But it is more unstable than before. I will try to write a new poc today.
Thanks~


### da...@chromium.org (2022-11-15)

[Empty comment from Monorail migration]

### tm...@chromium.org (2022-11-15)

havent quite solved it yet, here are some notes:
 - content::BatchingMediaLog::SendQueuedMediaEvents is being posted, not called directly, which means it's _not_ happening in the destructor.
 - SendQueuedMediaEvents grabs the lock, and it's touching InspectorMediaEventHandler, so that means that |event_handlers_| hasn't been cleared, which means that BatchingMediaLog::Stop() hasn't been called. 
 - SendQueuedMediaEvents is posted with a weak_ptr_, so the instance should be un-deleted, or else the callback would not have been run, which means that ~BatchingMediaLog has not been executed yet. 

I'm leaning towards something weird with InspectorMediaEventHandler owning a |inspector_context_| which might have been unexpectedly free'd by oilpan too soon.

### tm...@chromium.org (2022-11-15)

I wonder if the right move is to have
InspectorMediaEventHandler give a rawptr reference for itself to MediaInspectorContextImpl and have both of them notify the other of deletion, whoever gets it first.

### em...@gmail.com (2022-11-15)

repro steps:
(1) luanch custom http server
  python3 -m http.server 8001 --dir=/home/xx
(2) I wrote a test script that can open multiple browsers at the same time.(You need to modify the path of the chrome binary and the path of crash.html.) 
./launcher.sh
(3)If it does not repro in about 30 seconds, press ctrl+C to close all browsers and re-run the script.The repro is stable on my machine, and it can be reproed for the first or second time.
The crash.html file is a file from my earlier report(https://bugs.chromium.org/p/chromium/issues/detail?id=1309120) and has been modified briefly.And I think the original crash.html can also be reproduced, but it is not stable.

### em...@gmail.com (2022-11-15)

tested version 
(1)Chromium 110.0.5420.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1071426.zip)
(2)Chromium 109.0.5410.0(custom asab build)
  args.gn
  is_asan = true
  is_debug = false
  enable_nacl = false
  treat_warnings_as_errors = false
  is_component_build=false
  dcheck_always_on = false

### dr...@chromium.org (2022-11-21)

I was able to reproduce this on the second try in M107. Adding appropriate security labels

### [Deleted User] (2022-11-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-29)

tmathmeyer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tm...@chromium.org (2022-11-29)

been out for thanksgiving / sick. Taking a look now from home, will hopefully make more progress in the office tomorrow.

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### tm...@chromium.org (2022-12-02)

[Comment Deleted]

### tm...@chromium.org (2022-12-02)

fix coming soon.
better trace (trying again to get fixed width)
```
=================================================================                                                                                                               
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x617000500440 at pc 0x7fb5e0a95f1a bp 0x7ffe97439d50 sp 0x7ffe97439d48                                            
READ of size 8 at 0x617000500440 thread T0 (chrome)                                                                                                                             
==1==WARNING: invalid path to external symbolizer!                                                                                                                              
==1==WARNING: Failed to use and restart external symbolizer!                                                                                                                    
    #0 0x7fb5e0a95f19  (./../../base/memory/scoped_refptr.h:282) (BuildId: 3c4b979699c1d773)                                                                      
    #1 0x7fb5e890f590  (./../../third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc:113) (BuildId: ce3374af6278a78d)                                                                          
    #2 0x7fb5e89118cd  (./../../third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc:182) (BuildId: ce3374af6278a78d)                                                                          
    #3 0x7fb61f914c6f  (./../../content/renderer/media/inspector_media_event_handler.cc:157) (BuildId: ea27767f31dfdcb7)                                                                             
    #4 0x7fb61f903b2e  (./../../content/renderer/media/batching_media_log.cc:236) (BuildId: ea27767f31dfdcb7)                                                                             
    #5 0x7fb61f90a1e3  (./../../base/functional/bind_internal.h:670) (BuildId: ea27767f31dfdcb7)                                                                             
    #6 0x7fb622a53e29  (./../../base/functional/callback.h:152) (BuildId: fa413c0d4978c13c)                                                                                 
    #7 0x7fb622aa8d97  (./../../base/task/common/task_annotator.h:85) (BuildId: fa413c0d4978c13c)                                                                                 
    #8 0x7fb622aa7aea  (./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:301) (BuildId: fa413c0d4978c13c)                                                                                 
    #9 0x7fb622aaa1f4  (./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:?) (BuildId: fa413c0d4978c13c)                                                                                 
    #10 0x7fb62290bb43  (./../../base/message_loop/message_pump_default.cc:48) (BuildId: fa413c0d4978c13c)                                                                                
    #11 0x7fb622aaac6e  (./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:610) (BuildId: fa413c0d4978c13c)                                                                                
    #12 0x7fb6229bc348  (./../../base/run_loop.cc:141) (BuildId: fa413c0d4978c13c)                                                                                
    #13 0x7fb61fa003be  (./../../content/renderer/renderer_main.cc:330) (BuildId: ea27767f31dfdcb7)                                                                            
    #14 0x7fb61ffbbd3a  (./../../content/app/content_main_runner_impl.cc:662) (BuildId: ea27767f31dfdcb7)                                                                            
    #15 0x7fb61ffbde00  (./../../content/app/content_main_runner_impl.cc:744) (BuildId: ea27767f31dfdcb7)                                                                            
    #16 0x7fb61ffbfe84  (./../../content/app/content_main_runner_impl.cc:1089) (BuildId: ea27767f31dfdcb7)
    #17 0x7fb61ffb856a  (./../../content/app/content_main.cc:344) (BuildId: ea27767f31dfdcb7)
    #18 0x7fb61ffb8b7a  (./../../content/app/content_main.cc:372) (BuildId: ea27767f31dfdcb7)
    #19 0x563d3e7f9aed  (/chromium/src/out/Asan/chrome+0x4337aed) (BuildId: 24ca434a5837f925)
    #20 0x7fb5d0c29209  (/lib/x86_64-linux-gnu/libc.so.6+0x29209) (BuildId: 532d686f61d5422a2617967cbfbecfd4bd6a39c7)

0x617000500440 is located 448 bytes inside of 744-byte region [0x617000500280,0x617000500568)
freed by thread T0 (chrome) here:
    #0 0x563d3e7c6566  (/chromium/src/out/Asan/chrome+0x4304566) (BuildId: 24ca434a5837f925)
    #1 0x7fb5e69f3f2e  (./../../third_party/blink/renderer/platform/wtf/allocator/partition_allocator.h:43) (BuildId: ce3374af6278a78d)
    #2 0x7fb5e8919f18  (./../../third_party/blink/renderer/platform/wtf/vector.h:1850) (BuildId: ce3374af6278a78d)
    #3 0x7fb61f9041a2  (./../../content/renderer/media/batching_media_log.cc:87) (BuildId: ea27767f31dfdcb7)
    #4 0x7fb61484aed5  (./../../media/base/media_log.cc:65) (BuildId: b4bb5fcc09967b25)
    #5 0x7fb5cba9227d  (./../../third_party/blink/renderer/platform/media/web_media_player_impl.cc:569) (BuildId: aa6d17ebcb0d348e)
    #6 0x7fb5cba944cd  (./../../third_party/blink/renderer/platform/media/web_media_player_impl.cc:522) (BuildId: aa6d17ebcb0d348e)
    #7 0x7fb5e84ce0c7  (./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:49) (BuildId: ce3374af6278a78d)
    #8 0x7fb5e84ca51b  (./../../third_party/blink/renderer/core/html/media/html_media_element.cc:541) (BuildId: ce3374af6278a78d)
    #9 0x7fb5de2ade3a  (./../../v8/src/heap/cppgc/prefinalizer-handler.cc:72) (BuildId: dbf54339142ff9eb)
    #10 0x7fb5de2808d1  (./../../v8/src/heap/cppgc/heap-base.cc:208) (BuildId: dbf54339142ff9eb)
    #11 0x7fb5dc5bbf03  (./../../v8/src/heap/cppgc-js/cpp-heap.cc:796) (BuildId: dbf54339142ff9eb)
    #12 0x7fb5dc5d165a  (./../../v8/src/heap/embedder-tracing.cc:74) (BuildId: dbf54339142ff9eb)
    #13 0x7fb5dc6acf50  (./../../v8/src/heap/heap.cc:2279) (BuildId: dbf54339142ff9eb)
    #14 0x7fb5dc6a1bd2  (./../../v8/src/heap/heap.cc:1697) (BuildId: dbf54339142ff9eb)
    #15 0x7fb5dc6a9417  (./../../v8/src/heap/heap.cc:1414) (BuildId: dbf54339142ff9eb)
    #16 0x7fb5dc5bc7e4  (./../../v8/src/heap/embedder-tracing.h:141) (BuildId: dbf54339142ff9eb)
    #17 0x7fb5de2b6806  (./../../v8/src/heap/cppgc/stats-collector.cc:?) (BuildId: dbf54339142ff9eb)
    #18 0x7fb5de2a1444  (./../../v8/src/heap/cppgc/object-allocator.cc:120) (BuildId: dbf54339142ff9eb)
    #19 0x7fb5e8917640  (./../../v8/include/cppgc/allocation.h:117) (BuildId: ce3374af6278a78d)
    #20 0x7fb5e8918092  (./../../v8/include/cppgc/allocation.h:280) (BuildId: ce3374af6278a78d)
    #21 0x7fb5e890dd28  (./../../third_party/blink/renderer/platform/wtf/hash_table.h:1641) (BuildId: ce3374af6278a78d)
    #22 0x7fb5e890d8c5  (./../../third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc:80) (BuildId: ce3374af6278a78d)
    #23 0x7fb5e890f59c  (./../../third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc:113) (BuildId: ce3374af6278a78d)
    #24 0x7fb5e89118cd  (./../../third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc:182) (BuildId: ce3374af6278a78d)
    #25 0x7fb61f914c6f  (./../../content/renderer/media/inspector_media_event_handler.cc:157) (BuildId: ea27767f31dfdcb7)
    #26 0x7fb61f903b2e  (./../../content/renderer/media/batching_media_log.cc:236) (BuildId: ea27767f31dfdcb7)
    #27 0x7fb61f90a1e3  (./../../base/functional/bind_internal.h:670) (BuildId: ea27767f31dfdcb7)
    #28 0x7fb622a53e29  (./../../base/functional/callback.h:152) (BuildId: fa413c0d4978c13c)
    #29 0x7fb622aa8d97  (./../../base/task/common/task_annotator.h:85) (BuildId: fa413c0d4978c13c)

previously allocated by thread T0 (chrome) here:
    #0 0x563d3e7c680e  (/chromium/src/out/Asan/chrome+0x430480e) (BuildId: 24ca434a5837f925)
    #1 0x7fb604358ae8  (./../../base/allocator/partition_allocator/partition_root.h:1866) (BuildId: 69d56673b388bdee)
    #2 0x7fb5e69f4276  (./../../third_party/blink/renderer/platform/wtf/allocator/partition_allocator.h:40) (BuildId: ce3374af6278a78d)
    #3 0x7fb5e69f3dfa  (./../../third_party/blink/renderer/platform/wtf/vector.h:399) (BuildId: ce3374af6278a78d)
    #4 0x7fb5e8919f18  (./../../third_party/blink/renderer/platform/wtf/vector.h:1850) (BuildId: ce3374af6278a78d)
    #5 0x7fb61f9041a2  (./../../content/renderer/media/batching_media_log.cc:87) (BuildId: ea27767f31dfdcb7)
    #6 0x7fb61484aed5  (./../../media/base/media_log.cc:65) (BuildId: b4bb5fcc09967b25)
    #7 0x7fb5cba9227d  (./../../third_party/blink/renderer/platform/media/web_media_player_impl.cc:569) (BuildId: aa6d17ebcb0d348e)
    #8 0x7fb5cba944cd  (./../../third_party/blink/renderer/platform/media/web_media_player_impl.cc:522) (BuildId: aa6d17ebcb0d348e)
    #9 0x7fb5e84ce0c7  (./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:49) (BuildId: ce3374af6278a78d)
    #10 0x7fb5e84ca51b  (./../../third_party/blink/renderer/core/html/media/html_media_element.cc:541) (BuildId: ce3374af6278a78d)
    #11 0x7fb5de2ade3a  (./../../v8/src/heap/cppgc/prefinalizer-handler.cc:72) (BuildId: dbf54339142ff9eb)
    #12 0x7fb5de2808d1  (./../../v8/src/heap/cppgc/heap-base.cc:208) (BuildId: dbf54339142ff9eb)
    #13 0x7fb5dc5bbf03  (./../../v8/src/heap/cppgc-js/cpp-heap.cc:796) (BuildId: dbf54339142ff9eb)
    #14 0x7fb5dc5d165a  (./../../v8/src/heap/embedder-tracing.cc:74) (BuildId: dbf54339142ff9eb)
    #15 0x7fb5dc6acf50  (./../../v8/src/heap/heap.cc:2279) (BuildId: dbf54339142ff9eb)
    #16 0x7fb5dc6a1bd2  (./../../v8/src/heap/heap.cc:1697) (BuildId: dbf54339142ff9eb)
    #17 0x7fb5dc6a9417  (./../../v8/src/heap/heap.cc:1414) (BuildId: dbf54339142ff9eb)
    #18 0x7fb5dc5bc7e4  (./../../v8/src/heap/embedder-tracing.h:141) (BuildId: dbf54339142ff9eb)
    #19 0x7fb5de2b6806  (./../../v8/src/heap/cppgc/stats-collector.cc:?) (BuildId: dbf54339142ff9eb)
    #20 0x7fb5de2a1444  (./../../v8/src/heap/cppgc/object-allocator.cc:120) (BuildId: dbf54339142ff9eb)
    #21 0x7fb5e15346a6  (./../../v8/include/cppgc/allocation.h:117) (BuildId: 3c4b979699c1d773)
    #22 0x7fb5e15344a3  (./../../v8/include/cppgc/allocation.h:280) (BuildId: 3c4b979699c1d773)
    #23 0x7fb5e1533674  (./../../third_party/blink/renderer/platform/wtf/vector.h:399) (BuildId: 3c4b979699c1d773)
    #24 0x7fb5e15330dc  (./../../third_party/blink/renderer/platform/wtf/vector.h:1747) (BuildId: 3c4b979699c1d773)
    #25 0x7fb5e152fe81  (./../../third_party/blink/renderer/platform/wtf/vector.h:1918) (BuildId: 3c4b979699c1d773)
    #26 0x7fb5e156c489  (./../../third_party/blink/renderer/platform/scheduler/main_thread/main_thread_scheduler_impl.cc:1152) (BuildId: 3c4b979699c1d773)
    #27 0x7fb5e1581c32  (./../../third_party/blink/renderer/platform/scheduler/main_thread/main_thread_scheduler_impl.cc:2374) (BuildId: 3c4b979699c1d773)
    #28 0x7fb5e1593e6f  (./../../third_party/blink/renderer/platform/scheduler/main_thread/main_thread_task_queue.cc:160) (BuildId: 3c4b979699c1d773)
    #29 0x7fb5e15970f9  (./../../base/functional/bind_internal.h:670) (BuildId: 3c4b979699c1d773)
```

### tm...@chromium.org (2022-12-02)

here's a description of what happens:

MediaInspectorContextImpl::CullPlayers() {
  for(const auto& playerId : dead_players_) {
     RemovePlayer(playerId);
  }
  ...
}

RemovePlayer can cause a blink GC event, since it messes with traced things. This can cause a GC'd but not deleted WMPI's destructor to be called,
which gives us this call stack:

WebMediaPlayerImpl::~WebMediaPlayerImpl()
MediaLog::OnWebMediaPlayerDestroyed()
BatchingMediaLog::OnWebMediaPlayerDestroyedLocked();
InspectorMediaEventHandler::OnWebMediaPlayerDestroyed();
MediaInspectorContextImpl::DestroyPlayer();

which, if PlayerID is still in the "unsent_player_" vector, will cause it to be moved into the "dead_players_" vector.
If this can happen enough times, then |dead_players_| can get re-allocated to increase it's space. If there's no space at that address, it will get moved,
which invalidates the iterator still being used in the loop in CullPlayers.

I've just uploaded a patch to fix it.

### gi...@appspot.gserviceaccount.com (2022-12-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/819d876e1bb8926b129618ab17b62a76ec4e83d1

commit 819d876e1bb8926b129618ab17b62a76ec4e83d1
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Sat Dec 03 00:09:22 2022

Fix UAF caused by vector operations during iteration

MediaInspectorContextImpl::CullPlayers iterates through dead_players_
to remove their events, but this can cause a GC event which can
end up adding more players to the |dead_players_| vector, causing
it to get re-allocated and it's iterators invalidated.

We can fix this simply by not using an iterator, and removing elements
from the vector before we trigger any GC operations that might cause
other changes to the vector.

Bug: 1383991

Change-Id: I59f5824c156ff58cf6b55ac9b942c8efdb1ed65a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4064295
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1078842}

[modify] https://crrev.com/819d876e1bb8926b129618ab17b62a76ec4e83d1/third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc


### tm...@chromium.org (2022-12-03)

[Empty comment from Monorail migration]

### tm...@chromium.org (2022-12-03)

I'm unsure if we should merge this back. It's very hard to exploit into anything but a crash.

### [Deleted User] (2022-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-04)

Requesting merge to stable M108 because latest trunk commit (1078842) appears to be after stable branch point (1058933).

Requesting merge to beta M109 because latest trunk commit (1078842) appears to be after beta branch point (1070088).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-04)

Merge review required: M109 is already shipping to beta.

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

### [Deleted User] (2022-12-04)

Merge review required: M108 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-05)

109 merge approved, please merge this fix to branch 5414 by EOD tomorrow, Tuesday 6 December so this fix can be included in the next M109 beta 

108 merge approved, please merge this fix to branch 5359 by 10am Pacific, Friday, 9 December so this fix can be included in the next M108 Stable refresh 

### tm...@chromium.org (2022-12-05)

merges in progress

### gi...@appspot.gserviceaccount.com (2022-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9eb341b4e65b46e53f98e23ea7e771e3614945b4

commit 9eb341b4e65b46e53f98e23ea7e771e3614945b4
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Mon Dec 05 23:35:49 2022

Fix UAF caused by vector operations during iteration

MediaInspectorContextImpl::CullPlayers iterates through dead_players_
to remove their events, but this can cause a GC event which can
end up adding more players to the |dead_players_| vector, causing
it to get re-allocated and it's iterators invalidated.

We can fix this simply by not using an iterator, and removing elements
from the vector before we trigger any GC operations that might cause
other changes to the vector.

Bug: 1383991

(cherry picked from commit 819d876e1bb8926b129618ab17b62a76ec4e83d1)

Change-Id: I59f5824c156ff58cf6b55ac9b942c8efdb1ed65a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4064295
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1078842}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4080812
Auto-Submit: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#456}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/9eb341b4e65b46e53f98e23ea7e771e3614945b4/third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc


### [Deleted User] (2022-12-05)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/988abc21f32ae8ef94099eb1696873d00f0a7253

commit 988abc21f32ae8ef94099eb1696873d00f0a7253
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Mon Dec 05 23:58:56 2022

Fix UAF caused by vector operations during iteration

MediaInspectorContextImpl::CullPlayers iterates through dead_players_
to remove their events, but this can cause a GC event which can
end up adding more players to the |dead_players_| vector, causing
it to get re-allocated and it's iterators invalidated.

We can fix this simply by not using an iterator, and removing elements
from the vector before we trigger any GC operations that might cause
other changes to the vector.

Bug: 1383991

(cherry picked from commit 819d876e1bb8926b129618ab17b62a76ec4e83d1)

Change-Id: I59f5824c156ff58cf6b55ac9b942c8efdb1ed65a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4064295
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Reviewed-by: Thomas Guilbert <tguilbert@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1078842}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4081318
Auto-Submit: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1091}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/988abc21f32ae8ef94099eb1696873d00f0a7253/third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc


### rz...@google.com (2022-12-06)

[Empty comment from Monorail migration]

### rz...@google.com (2022-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-06)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-12-06)

1. https://crrev.com/c/4081072
2. Low. No conflicts, only a simple build issue
3. 108, 109
4. Yes

### gm...@google.com (2022-12-06)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-12)

[Empty comment from Monorail migration]

### gm...@google.com (2022-12-13)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-14)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4e9f92ed75a9550987cf0cf1e51181dc75eec93a

commit 4e9f92ed75a9550987cf0cf1e51181dc75eec93a
Author: Ted Meyer <tmathmeyer@chromium.org>
Date: Thu Dec 15 09:59:41 2022

[M102-LTS] Fix UAF caused by vector operations during iteration

M102 merge issues:
  Build issue, dead_players_.empty() used instead of
  dead_players_.IsEmpty() (inspector_media_context_impl.cc:112)

MediaInspectorContextImpl::CullPlayers iterates through dead_players_
to remove their events, but this can cause a GC event which can
end up adding more players to the |dead_players_| vector, causing
it to get re-allocated and it's iterators invalidated.

We can fix this simply by not using an iterator, and removing elements
from the vector before we trigger any GC operations that might cause
other changes to the vector.

Bug: 1383991

(cherry picked from commit 819d876e1bb8926b129618ab17b62a76ec4e83d1)

Change-Id: I59f5824c156ff58cf6b55ac9b942c8efdb1ed65a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4064295
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1078842}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4081072
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1411}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/4e9f92ed75a9550987cf0cf1e51181dc75eec93a/third_party/blink/renderer/core/inspector/inspector_media_context_impl.cc


### rz...@google.com (2022-12-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1383991?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Media>WebCodecs, Blink>Scheduling]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061735)*
