# use-after-poison network_state_notifier.cc:314 in blink::NetworkStateNotifier::NotifyObserversOnTaskRunner

| Field | Value |
|-------|-------|
| **Issue ID** | [40055783](https://issues.chromium.org/issues/40055783) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Network |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2021-05-08 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4494.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
asan-win32-release_x64-880310

#Reproduce
python3.6m -m http.server 8000
open http://localhost:8000/fuzz-00024.html
Repeatedly disable and enable network interfaces

What is the expected behavior?

What went wrong?

#Observe
```
=================================================================
==11964==ERROR: AddressSanitizer: use-after-poison on address 0x7eda34e54688 at pc 0x7ff810f4428b bp 0x00e73bdfea10 sp 0x00e73bdfea58
READ of size 8 at 0x7eda34e54688 thread T40
==11964==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff810f4428a in blink::NetworkStateNotifier::NotifyObserversOnTaskRunner C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\network\network_state_notifier.cc:314
    #1 0x7ff810f467e1 in base::internal::Invoker<base::internal::BindState<void (blink::NetworkStateNotifier::*)(WTF::HashMap<scoped_refptr<base::SingleThreadTaskRunner>,std::__1::unique_ptr<blink::NetworkStateNotifier::ObserverList,std::__1::default_delete<blink::NetworkStateNotifier::ObserverList> >,WTF::RefPtrHash<base::SingleThreadTaskRunner>,WTF::HashTraits<scoped_refptr<base::SingleThreadTaskRunner> >,WTF::HashTraits<std::__1::unique_ptr<blink::NetworkStateNotifier::ObserverList,std::__1::default_delete<blink::NetworkStateNotifier::ObserverList> > >,WTF::PartitionAllocator> *, blink::NetworkStateNotifier::ObserverType, scoped_refptr<base::SingleThreadTaskRunner>, const blink::NetworkStateNotifier::NetworkState &),WTF::CrossThreadUnretainedWrapper<blink::NetworkStateNotifier>,WTF::CrossThreadUnretainedWrapper<WTF::HashMap<scoped_refptr<base::SingleThreadTaskRunner>,std::__1::unique_ptr<blink::NetworkStateNotifier::ObserverList,std::__1::default_delete<blink::NetworkStateNotifier::ObserverList> >,WTF::RefPtrHash<base::SingleThreadTaskRunner>,WTF::HashTraits<scoped_refptr<base::SingleThreadTaskRunner> >,WTF::HashTraits<std::__1::unique_ptr<blink::NetworkStateNotifier::ObserverList,std::__1::default_delete<blink::NetworkStateNotifier::ObserverList> > >,WTF::PartitionAllocator> >,blink::NetworkStateNotifier::ObserverType,scoped_refptr<base::SingleThreadTaskRunner>,blink::NetworkStateNotifier::NetworkState>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690
    #2 0x7ff8123e101a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #3 0x7ff814b3cb0c in base::sequence_manager::internal::ThreadControllerImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_impl.cc:199
    #4 0x7ff814b3f7d3 in base::internal::Invoker<base::internal::BindState<void (base::sequence_manager::internal::ThreadControllerImpl::*)(base::sequence_manager::internal::ThreadControllerImpl::WorkType),base::WeakPtr<base::sequence_manager::internal::ThreadControllerImpl>,base::sequence_manager::internal::ThreadControllerImpl::WorkType>,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:703
    #5 0x7ff8123e101a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:178
    #6 0x7ff814b41a5f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:357
    #7 0x7ff814b410d9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:270
    #8 0x7ff812491c70 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #9 0x7ff81248fe58 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #10 0x7ff814b43104 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:466
    #11 0x7ff812366ba3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134
    #12 0x7ff8124278f9 in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:312
    #13 0x7ff812427e10 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:383
    #14 0x7ff8124b2a1f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:121
    #15 0x7ff748d8dac7 in __asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:279
    #16 0x7ff896fc7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #17 0x7ff897362650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

Address 0x7eda34e54688 is a wild pointer inside of access range of size 0x000000000008.
SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\network\network_state_notifier.cc:314 in blink::NetworkStateNotifier::NotifyObserversOnTaskRunner
Shadow bytes around the buggy address:
  0x12686f7ca880: 00 00 00 00 00 f7 00 00 00 00 f7 f7 f7 f7 f7 f7
  0x12686f7ca890: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x12686f7ca8a0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x12686f7ca8b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x12686f7ca8c0: 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x12686f7ca8d0: f7[f7]f7 f7 f7 f7 f7 00 00 00 00 00 f7 f7 f7 f7
  0x12686f7ca8e0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x12686f7ca8f0: f7 f7 00 00 00 00 00 00 f7 f7 f7 f7 f7 f7 f7 00
  0x12686f7ca900: 00 00 00 00 f7 00 00 00 00 00 f7 00 00 00 00 f7
  0x12686f7ca910: 00 00 00 00 f7 00 00 00 00 00 00 00 f7 00 00 00
  0x12686f7ca920: 00 00 00 00 f7 00 00 00 00 00 00 00 f7 00 00 00
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
  Shadow gap:              cc
Thread T40 created by T0 here:
    #0 0x7ff748d8e5b2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ff8124b1dfe in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ff812426bca in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:187
    #3 0x7ff80c6627ba in content::RenderProcessHostImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_process_host_impl.cc:1861
    #4 0x7ff80c6455d2 in content::RenderFrameHostManager::InitRenderView C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:2806
    #5 0x7ff80c63cdb5 in content::RenderFrameHostManager::ReinitializeMainRenderFrame C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:3032
    #6 0x7ff80c63ab48 in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:1052
    #7 0x7ff80c63970c in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:807
    #8 0x7ff80c3bf5e5 in content::FrameTreeNode::CreatedNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree_node.cc:532
    #9 0x7ff80c579c5f in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigator.cc:596
    #10 0x7ff80c4e957e in content::NavigationControllerImpl::NavigateWithoutEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:3302
    #11 0x7ff80c4e8734 in content::NavigationControllerImpl::LoadURLWithParams C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:1136
    #12 0x7ff81462afb9 in `anonymous namespace'::LoadURLInContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:386
    #13 0x7ff814628316 in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:658
    #14 0x7ff81bafc291 in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:313
    #15 0x7ff81bafe06f in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:582
    #16 0x7ff81bafb438 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:429
    #17 0x7ff81bafaaa0 in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:218
    #18 0x7ff817aece4e in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:689
    #19 0x7ff817af2d09 in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1200
    #20 0x7ff817aec349 in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1127
    #21 0x7ff817aea973 in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:624
    #22 0x7ff814c7c310 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1647
    #23 0x7ff814c79dbe in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1039
    #24 0x7ff80bb771de in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:960
    #25 0x7ff80c90f283 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:41
    #26 0x7ff80bb766e8 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:868
    #27 0x7ff80bb7e125 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:131
    #28 0x7ff80bb72cd4 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:43
    #29 0x7ff8120fcbe8 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:597
    #30 0x7ff8120ff51f in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1080
    #31 0x7ff8120fe72f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:955
    #32 0x7ff8120fba97 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372
    #33 0x7ff8120fc08b in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
    #34 0x7ff8080a145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:151
    #35 0x7ff748ce5bd1 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #36 0x7ff748ce2c1d in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:369
    #37 0x7ff7490cbb7f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #38 0x7ff896fc7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #39 0x7ff897362650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

==11964==ABORTING

```

Did this work before? N/A 

Chrome version: asan-win32-release_x64-880310  Channel: n/a
OS Version: 10.0
Flash Version:

## Attachments

- [fuzz-00024.html](attachments/fuzz-00024.html) (text/plain, 84.4 KB)
- deleted (application/octet-stream, 0 B)
- [patch.diff](attachments/patch.diff) (text/plain, 835 B)

## Timeline

### [Deleted User] (2021-05-08)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-05-10)

Thanks for reporting this. I'm having trouble reproducing this. It seems your test case has a lot of potentially unrelated bits (e.g. I see a variety of vertex shaders and videos), which seem like they'd be fairly unrelated to the problem at hand.

Could you describe the method you're using to frequently enable and disable the network adapters? Using 'netsh' in a loop to enable/disable an adapter, I'm unable to repro.

CC'ing jkarlin, given commit https://source.chromium.org/chromium/chromium/src/+/5d34987de6cffb8d747c5ed16e82614e9146cc0a and https://crbug.com/chromium/1170148

Josh: Would a NetLog be useful here for diagnostics?

Setting some initial triage labels based on past issues and this being in the renderer.

[Monorail components: Blink>Network]

### m....@gmail.com (2021-05-11)

Yes, I found this accidentally while fuzzing other modules. Here is a reproduced video, and then I will try to make a minicase.
#TestOn
Windows NT 10.0; Win64; x64
asan-win32-release_x64-880310

### [Deleted User] (2021-05-11)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-11)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-11)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@chromium.org (2021-05-14)

Thanks for the detailed report! I am able to repro by calling OnNetworkConnectionChanged from BrowserOnlineStateNotifier with online/offline parameters every 10 seconds with the given document. Will investigate.

### jk...@chromium.org (2021-05-14)

Notes to self:

The issue is that the observer is being deleted but isn't being unregistered with the NetworkStateNotifier before that happens. So the next time the notifier goes to make a notification, it calls out to a deleted observer.

So the question becomes, why isn't the unregister method being called? From tracking down the code, the Document has a Member<NetworkStateObserver>. The NetworkStateObserver has a std::unique_ptr<NetworkStateNotifier::NetworkStateObserverHandle>. The handle is a RAII object and will unregister the observer on destruction. So we need to make sure it gets destroyed before the NetworkStateObserver goes away. But that's not happening. I'm not very familiar with Oilpan but I'm guessing it's because the NetworkStateObserver's destructor isn't being called and so the unique_ptr for the handle isn't properly destroyed. Instead, it looks as if NetworkStateObserver is supposed to get a "ContextDestroyed" call from the ExecutionContextLifecycleObserver, but that's clearly not always happening. So, I guess I need to find a way to ensure that ContextDestroyed gets called. I have to say, I sure wish I could depend on RAII. Oilpan is complicated.


### jk...@chromium.org (2021-05-15)

Looking at the comment history in https://codereview.chromium.org/2714643008/, it seems that this kind of issue isn't a big surprise. Reassigning to Kinuko as she understands the object lifetime model here much better than I do.

Kinuko: There are cases in which NetworkStateObserver::ContextDestroyed isn't getting called before the observer is destroyed, and so the NetworkStateNotifier's raw pointer triggers a UAF. We could change the notifier to hold weakptrs, which is at least safer, but doesn't fix the underlying problem that we're not cleaning up our observer properly.

I was able to prevent the problem in my local test by calling network_sate_observer_->ContextDestroyed() in Document::Shutdown() but I don't know if that's a good idea or not. 

To reproduce, patch in the following code to periodically simulate switching from online/offline. If you let this run with asan for 20-30 seconds on the repro page given in the first post, it should trigger.



─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
modified: content/browser/net/browser_online_state_observer.cc
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
@ browser_online_state_observer.cc:7 @

#include "content/browser/net/browser_online_state_observer.h"

#include "base/threading/thread_task_runner_handle.h"
#include "content/browser/renderer_host/render_process_host_impl.h"
#include "content/public/browser/notification_service.h"
#include "content/public/browser/notification_types.h"
@ browser_online_state_observer.cc:18 @ BrowserOnlineStateObserver::BrowserOnlineStateObserver() {
  net::NetworkChangeNotifier::AddMaxBandwidthObserver(this);
  registrar_.Add(this, content::NOTIFICATION_RENDERER_PROCESS_CREATED,
                 content::NotificationService::AllSources());
  base::ThreadTaskRunnerHandle::Get()->PostDelayedTask(FROM_HERE, base::BindOnce(&BrowserOnlineStateObserver::Switch, base::Unretained(this)), base::TimeDelta::FromSeconds(10));
}
 
void BrowserOnlineStateObserver::Switch() {
  LOG(ERROR) << "Switching!";
  for (RenderProcessHost::iterator it(RenderProcessHost::AllHostsIterator());
       !it.IsAtEnd(); it.Advance()) {
    // TODO(https://crbug.com/813045): Remove this check once we have a better
    // way of iterating the hosts.
    if (it.GetCurrentValue()->IsInitializedAndNotDead()) {
      it.GetCurrentValue()->GetRendererInterface()->OnNetworkConnectionChanged(
      !online_ ? net::NetworkChangeNotifier::CONNECTION_ETHERNET
              : net::NetworkChangeNotifier::CONNECTION_NONE,
      1.0);
    }
  }
  online_ = !online_;
  base::ThreadTaskRunnerHandle::Get()->PostDelayedTask(FROM_HERE, base::BindOnce(&BrowserOnlineStateObserver::Switch, base::Unretained(this)), base::TimeDelta::FromSeconds(10));
}

BrowserOnlineStateObserver::~BrowserOnlineStateObserver() {
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
modified: content/browser/net/browser_online_state_observer.h
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
@ browser_online_state_observer.h:34 @ class BrowserOnlineStateObserver
               const content::NotificationSource& source,
               const content::NotificationDetails& details) override;

  void Switch();
 
 private:
  content::NotificationRegistrar registrar_;
  bool online_ = true;

  DISALLOW_COPY_AND_ASSIGN(BrowserOnlineStateObserver);
};

### [Deleted User] (2021-05-22)

kinuko: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2021-05-24)

Try to provide a solution to use the FINALIZER feature of GC to ensure that the observer is unregistered when the NetworkStateObserver class is released
```
diff --git a/document.cc b/document.cc
index 244d0f6..c850e00 100644
--- a/document.cc
+++ b/document.cc
@@ -581,6 +581,7 @@ class Document::NetworkStateObserver final
     : public GarbageCollected<Document::NetworkStateObserver>,
       public NetworkStateNotifier::NetworkStateObserver,
       public ExecutionContextLifecycleObserver {
+  USING_PRE_FINALIZER(NetworkStateObserver, Dispose);
  public:
   explicit NetworkStateObserver(ExecutionContext* context)
       : ExecutionContextLifecycleObserver(context) {
@@ -609,6 +610,10 @@ class Document::NetworkStateObserver final
     ExecutionContextLifecycleObserver::Trace(visitor);
   }
 
+  void Dispose() {
+    UnregisterAsObserver(GetExecutionContext());
+  }
+
  private:
   std::unique_ptr<NetworkStateNotifier::NetworkStateObserverHandle>
       online_observer_handle_;
```

### jk...@chromium.org (2021-05-24)

I don't know enough about the blink GC to say whether USING_PRE_FINALIZER is a good idea. Will USING_PRE_FINALIZER work if the owning class doesn't have a PRE_FINALIZER? What is the performance cost to a PRE_FINALIZER?

Adding haraken for guidance.

### ha...@google.com (2021-05-25)

Can we call UnregisterAsObserver() when the ExecutionContext is detached (i.e., when ContextDestroyed is called)?

It's nice to clean up things in ContextDestroyed rather than a pre-finalizer. The timing of ContextDestroyed is well defined & most things are expected to stop on the execution context detachment. The timing of a pre-finalizer is GC-dependent.


### rs...@chromium.org (2021-05-25)

See https://crbug.com/chromium/1206928#c9 ; ContextDestroyed is set to unregister, but in some sequence of events (unclear to me and jkarlin@), it isn't called. 

Specifically:
- https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/network/network_state_notifier.cc;l=115;drc=9771c1d3c659820e5112794451a50286c2320f97 is the scoped handle that is supposed to unregister
- This is held by https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/netinfo/network_information.cc;l=262;drc=9771c1d3c659820e5112794451a50286c2320f97 and released (dtor'd) by https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/netinfo/network_information.cc;l=271;drc=9771c1d3c659820e5112794451a50286c2320f97
- Which is called by ContextDestroyed here - https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/netinfo/network_information.cc;l=253;drc=9771c1d3c659820e5112794451a50286c2320f97



### [Deleted User] (2021-06-05)

kinuko: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ki...@chromium.org (2021-06-09)

This had slipped under my radar, sorry for the delay.

Reg: ContextDestroyed and ExecutionContext sequence (rephrasing some of https://crbug.com/chromium/1206928#c9 and https://crbug.com/chromium/1206928#c14):

NetworkInformation implements ExecutionContextLifecycleObserver, and surely utilizes ContextDestroyed in order to determine if it needs to stop observing (and unregister the observers).  This also tries to avoid starting a new observer after ContextDestroyed is called, with a flag context_stopped_.

Relevant methods are:  NetworkInformation::ContextDestroyed(), NetworkInformation::{Start,Stop}Observing

So for regular sequences it looks it's doing the right thing.  One thing I wondered (which relates to the issue I hit in the fore-mentioned CL) is if the NetworkInformation might be created after the context is detached.  We check navigator.GetExecutionContext() before creating NetworkInformation in NetworkInformation::connection(), but don't check IsContextDestroyed() there.  I don't know if that's relevant in this case but if so we should avoid starting to observe (or even create a network information) if the context is already destroyed.

Looks like the newer RAII change is made by hajimehoshi@ in this CL, could you look into this one?
https://chromium-review.googlesource.com/c/chromium/src/+/722859/



### ha...@chromium.org (2021-06-09)

Sorry but I don't remember the fix 4 years ago...

> We check navigator.GetExecutionContext() before creating NetworkInformation in NetworkInformation::connection(), but don't check IsContextDestroyed() there.

So, would adding the check somewhere fix this issue?

### ad...@google.com (2021-07-14)

Assuming this applies to M91 based on the Security_Impact originally set.

### ha...@chromium.org (2021-08-03)

I couldn't reproduce the same crash with the HTML file on my local machine.

I think this change will fix the issue:

```
diff --git a/third_party/blink/renderer/modules/netinfo/network_information.cc b/third_party/blink/renderer/modules/netinfo/network_information.cc
index ec8bd7ac82fab..0817e742f0217 100644
--- a/third_party/blink/renderer/modules/netinfo/network_information.cc
+++ b/third_party/blink/renderer/modules/netinfo/network_information.cc
@@ -277,6 +277,9 @@ const char NetworkInformation::kSupplementName[] = "NetworkInformation";
 NetworkInformation* NetworkInformation::connection(NavigatorBase& navigator) {
   if (!navigator.GetExecutionContext())
     return nullptr;
+  if (navigator.GetExecutionContext()->IsContextDestroyed())
+    return nullptr;
+
   NetworkInformation* supplement =
       Supplement<NavigatorBase>::From<NetworkInformation>(navigator);
   if (!supplement) {
```

As I'm not so familiar with NetworkInformation, I'd be happy if anyone could give me an advice how to write a test. Thanks,

### m....@gmail.com (2021-08-03)

You can try reproduce with https://crbug.com/chromium/1206928#c9  patch.

### ha...@chromium.org (2021-08-04)

Thanks. Apparently, even with https://crbug.com/chromium/1206928#c19, the issue was not fixed:

```
    #1 0x7fa2b967a33f in Run ./../../base/callback.h:98:12
    #2 0x7fa2b967a33f in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:178:33
    #3 0x7fa2b96ea58f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360:23
    #4 0x7fa2b96e9178 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:36
    #5 0x7fa2b96eb471 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #6 0x7fa2b94d5f6c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #7 0x7fa2b96ec24c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467:12
    #8 0x7fa2b95bec38 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #9 0x7fa2ae61f91d in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:261:16
    #10 0x7fa2aea7e644 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:582:14
    #11 0x7fa2aea8401b in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:973:10
    #12 0x7fa2aea7b771 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:390:36
    #13 0x7fa2aea7d592 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:418:10
    #14 0x5616bfc9eca4 in ChromeMain ./../../chrome/app/chrome_main.cc:168:12
    #15 0x7fa250cc6d09 in __libc_start_main ./csu/../csu/libc-start.c:308:16

Address 0x7ebc28b4a6d8 is a wild pointer inside of access range of size 0x000000000008.                                                                                                                                                       
SUMMARY: AddressSanitizer: use-after-poison (/usr/local/google/home/hajimehoshi/chromium/src/out/Default/libblink_platform.so+0x2ea253f)                                                                                                      
Shadow bytes around the buggy address:                                                                                                                                                                                                        
  0x0fd805161480: 00 00 f7 00 00 00 00 00 00 00 f7 00 00 00 00 00                                                                                                                                                                             
  0x0fd805161490: 00 00 f7 f7 f7 f7 f7 f7 00 00 00 00 f7 00 00 00                                                                                                                                                                             
  0x0fd8051614a0: 00 00 00 f7 00 00 00 00 00 00 f7 f7 f7 f7 f7 f7                                                                                                                                                                             
  0x0fd8051614b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7                                                                                                                                                                             
  0x0fd8051614c0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7                                                                                                                                                                             
=>0x0fd8051614d0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7                                                                                                                                                                             
  0x0fd8051614e0: f7 f7 00 00 00 00 00 00 00 f7 f7 f7 f7 f7 f7 f7                                                                                                                                                                             
  0x0fd8051614f0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7                                                                                                                                                                             
  0x0fd805161500: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd805161510: f7 f7 f7 f7 f7 f7 00 00 00 00 00 f7 f7 f7 f7 f7
  0x0fd805161520: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
==1==ABORTING
```

Hmm...

### ha...@chromium.org (2021-08-05)

Kinuko: Unfortunately the fix https://crbug.com/chromium/1206928#c19 based on https://crbug.com/chromium/1206928#c16 didn't fix. As I don't have a good insight in NetworkStateNotifier, could you help me with this? Thanks,

P.S.

I missed pasting the top of the stack trace at https://crbug.com/chromium/1206928#c21:

```
#0 0x7fa267ea353f in blink::NetworkStateNotifier::NotifyObserversOnTaskRunner(WTF::HashMap<scoped_refptr<base::SingleThreadTaskRunner>, std::__Cr::unique_ptr<blink::NetworkStateNotifier::ObserverList, std::__Cr::default_delete<blink::NetworkStateNotifier::ObserverList> >, WTF::RefPtrHash<base::SingleThreadTaskRunner>, WTF::HashTraits<scoped_refptr<base::SingleThreadTaskRunner> >, WTF::HashTraits<std::__Cr::unique_ptr<blink::NetworkStateNotifier::ObserverList, std::__Cr::default_delete<blink::NetworkStateNotifier::ObserverList> > >, WTF::PartitionAllocator>*, blink::NetworkStateNotifier::ObserverType, scoped_refptr<base::SingleThreadTaskRunner>, blink::NetworkStateNotifier::NetworkState const&) ./../../third_party/blink/renderer/platform/wtf/vector.h:0:36
```

So apparently the same issue still remains even after https://crbug.com/chromium/1206928#c19.

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### jk...@chromium.org (2021-09-14)

[Empty comment from Monorail migration]

### jk...@chromium.org (2021-09-14)

[Empty comment from Monorail migration]

### ri...@chromium.org (2021-09-15)

[Empty comment from Monorail migration]

### ri...@chromium.org (2021-09-15)

I have a fix: https://chromium-review.googlesource.com/c/chromium/src/+/3163158

I don't have a test because I haven't yet analysed the exact chain of events that triggers the use-after-poison.

### gi...@appspot.gserviceaccount.com (2021-09-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/af84d38b5cf5ee24f432ae8273bc2dad1e075f0e

commit af84d38b5cf5ee24f432ae8273bc2dad1e075f0e
Author: Adam Rice <ricea@chromium.org>
Date: Fri Sep 17 04:56:28 2021

Move NetworkStateObserver from document to window

Previously NetworkStateObserver was a nested class of Document. Make it
a nested class of LocalDOMWindow instead, since they have the same
lifetime and it fires "online" and "offline" events at the window, not
the document.

BUG=1206928

Change-Id: I2a1080915cf56cfa47eae65594fe6edcc8c2130a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3167550
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/heads/main@{#922429}

[modify] https://crrev.com/af84d38b5cf5ee24f432ae8273bc2dad1e075f0e/third_party/blink/renderer/core/frame/local_dom_window.h
[modify] https://crrev.com/af84d38b5cf5ee24f432ae8273bc2dad1e075f0e/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/af84d38b5cf5ee24f432ae8273bc2dad1e075f0e/third_party/blink/renderer/core/frame/local_dom_window.cc
[modify] https://crrev.com/af84d38b5cf5ee24f432ae8273bc2dad1e075f0e/third_party/blink/renderer/core/dom/document.h


### ri...@chromium.org (2021-09-17)

Do we need a merge?

### [Deleted User] (2021-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-29)

I'm unsure as to why Sheriffbot hasn't kicked in a merge request; please go ahead and merge this to M95, branch 4638 at your earliest convenience

### gi...@appspot.gserviceaccount.com (2021-09-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/36028012d8977e3e226de641f561887f1f90e0e4

commit 36028012d8977e3e226de641f561887f1f90e0e4
Author: Adam Rice <ricea@chromium.org>
Date: Thu Sep 30 13:35:07 2021

Move NetworkStateObserver from document to window

Previously NetworkStateObserver was a nested class of Document. Make it
a nested class of LocalDOMWindow instead, since they have the same
lifetime and it fires "online" and "offline" events at the window, not
the document.

BUG=1206928

(cherry picked from commit af84d38b5cf5ee24f432ae8273bc2dad1e075f0e)

Change-Id: I2a1080915cf56cfa47eae65594fe6edcc8c2130a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3167550
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#922429}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3196231
Cr-Commit-Position: refs/branch-heads/4638@{#476}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[modify] https://crrev.com/36028012d8977e3e226de641f561887f1f90e0e4/third_party/blink/renderer/core/frame/local_dom_window.h
[modify] https://crrev.com/36028012d8977e3e226de641f561887f1f90e0e4/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/36028012d8977e3e226de641f561887f1f90e0e4/third_party/blink/renderer/core/frame/local_dom_window.cc
[modify] https://crrev.com/36028012d8977e3e226de641f561887f1f90e0e4/third_party/blink/renderer/core/dom/document.h


### am...@google.com (2021-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-30)

Congratulations - the VRP Panel has decided to award you $5,000 for this report. Thank you for this report and your efforts! 

### am...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### gi...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9195f68df5e133aef84fde2363a2c905708438ae

commit 9195f68df5e133aef84fde2363a2c905708438ae
Author: Adam Rice <ricea@chromium.org>
Date: Fri Nov 19 13:10:32 2021

[M90-LTS] Move NetworkStateObserver from document to window

Previously NetworkStateObserver was a nested class of Document. Make it
a nested class of LocalDOMWindow instead, since they have the same
lifetime and it fires "online" and "offline" events at the window, not
the document.

M90 merge notes:
  Simple conflicts because main contains different member declarations around
  the removed network_state_observer_ and a different declaration of the
  removed NetworkStateObserver class

BUG=1206928

(cherry picked from commit af84d38b5cf5ee24f432ae8273bc2dad1e075f0e)

Change-Id: I2a1080915cf56cfa47eae65594fe6edcc8c2130a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3167550
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#922429}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3240831
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1667}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/9195f68df5e133aef84fde2363a2c905708438ae/third_party/blink/renderer/core/frame/local_dom_window.h
[modify] https://crrev.com/9195f68df5e133aef84fde2363a2c905708438ae/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/9195f68df5e133aef84fde2363a2c905708438ae/third_party/blink/renderer/core/frame/local_dom_window.cc
[modify] https://crrev.com/9195f68df5e133aef84fde2363a2c905708438ae/third_party/blink/renderer/core/dom/document.h


### rz...@google.com (2021-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1206928?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1249355]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055783)*
