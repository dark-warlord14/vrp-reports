# UAP in permissions::PermissionRequestQueue::Peek

| Field | Value |
|-------|-------|
| **Issue ID** | [40075944](https://issues.chromium.org/issues/40075944) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | tu...@chromium.org |
| **Created** | 2023-10-31 |
| **Bounty** | $41,000.00 |

## Description

**Steps to reproduce the problem:**  

1.download the attachment and serve a http server in 8000  

2.download the asan build dev version chromium or build the newest chromium  

3.rm -rf /tmp/abcd1234;out/asan/chrome  

4.Click the trigger\_uaf button. Then after 2 seconds, uaf happen.

**Problem Description:**  

In PermissionRequestManager::ReprioritizeCurrentRequestIfNeeded. It check the pending\_permission\_requests\_ is empty at first. And then pop out all invalid requests in pending\_permission\_requests\_[2]. The pop out operation in [2] may make pending\_permission\_requests\_ be empty. So in the pending\_permission\_requests\_.Peek[3] UAP happens.

Exploit analysis:  

We can see from the asan log. The uap position is in [5]. buffer\_ hold the raw pointer of PermissionRequest object[6] rather than raw\_ptr<xxx>. The ValidateRequest[4] will free the PermissionRequest object which is saved in buffer\_ and will not clear the pointer to 0(depends on the implement of the base::circular\_deque container). Then the out of bounds access in [5] will get a wild pointer which points to the freed PermissionRequest object. Then finally will trigger a UAF. At this situation, miracle ptr can't protect it since buffer\_ hold the raw pointer of PermissionRequest object[6] rather than raw\_ptr<xxx>.

bool PermissionRequestManager::ReprioritizeCurrentRequestIfNeeded() {  

if (pending\_permission\_requests\_.IsEmpty() || !IsRequestInProgress() ||  

IsCurrentRequestEmbeddedPermissionElementInitiated()) {  

return true;  

} --------------------[1]

// Pop out all invalid requests in front of the queue.  

while (!pending\_permission\_requests\_.IsEmpty() &&  

!ValidateRequest(pending\_permission\_requests\_.Peek())) {------------[4]  

pending\_permission\_requests\_.Pop();  

} ----------------------[2]

auto current\_request\_fate = CurrentRequestFate::kKeepCurrent;

...

if (current\_request\_fate == CurrentRequestFate::kKeepCurrent &&  

pending\_permission\_requests\_.Peek() -----------------------[3]  

->IsEmbeddedPermissionElementInitiated()) {  

current\_request\_fate = CurrentRequestFate::kPreempt;  

}

...

return true;  

}

const value\_type& front() const {  

DCHECK(!empty());  

return buffer\_[begin\_]; -------------------[5]  

}

std::vector<base::circular\_deque<PermissionRequest\*>> queued\_requests\_; ------------------------[6]

**Additional Comments:**  

Note:

1. This bug just need click the trigger\_uaf button without compromised renderer. And with a compromised renderer, this bug don't need any user gesture because the click button operation is just to use window.open api. A compromised renderer can use this api without any user gesture by patch the user gesture check code in renderer.
2. \*\*\*full bisect information\*\*\* This bug is introduced in <https://chromium-review.googlesource.com/c/chromium/src/+/4915775>. And now only impact the dev version(120.0.6074.0). Beta and stable version are not impact.  
   
   3.\*\*\*a suggestion patch\*\*\* is in the attachment.

\*\*Chrome version: \*\* 120.0.6074.0 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 767 B)
- [poc.html](attachments/poc.html) (text/plain, 937 B)
- [asan.log](attachments/asan.log) (text/plain, 20.1 KB)

## Timeline

### ha...@gmail.com (2023-10-31)

And this is a browser process uaf bug.

### [Deleted User] (2023-10-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-31)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-10-31)

=================================================================
==1301876==ERROR: AddressSanitizer: use-after-poison on address 0x508000264b10 at pc 0x55682528e67c bp 0x7ffecf8b7190 sp 0x7ffecf8b7188
READ of size 8 at 0x508000264b10 thread T0 (chrome)
==1301876==WARNING: invalid path to external symbolizer!
==1301876==WARNING: Failed to use and restart external symbolizer!
    #0 0x55682528e67b in front ./../../base/containers/circular_deque.h:550:20
    #1 0x55682528e67b in permissions::PermissionRequestQueue::Peek() const ./../../components/permissions/permission_request_queue.cc:87:14
    #2 0x5568252750e9 in permissions::PermissionRequestManager::ReprioritizeCurrentRequestIfNeeded() ./../../components/permissions/permission_request_manager.cc:327:36
    #3 0x55682527a870 in permissions::PermissionRequestManager::ShowPrompt() ./../../components/permissions/permission_request_manager.cc:894:8
    #4 0x556825279a02 in permissions::PermissionRequestManager::OnVisibilityChanged(content::Visibility) ./../../components/permissions/permission_request_manager.cc:534:5
    #5 0x556823bad93f in void content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::*)(content::Visibility), content::Visibility&>(void (content::WebContentsObserver::*)(content::Visibility), content::Visibility&) ./../../content/browser/web_contents/web_contents_impl.h:1593:9
    #6 0x556823b88283 in content::WebContentsImpl::SetVisibilityAndNotifyObservers(content::Visibility) ./../../content/browser/web_contents/web_contents_impl.cc:5624:16
    #7 0x556823b58d6d in content::WebContentsImpl::UpdateVisibilityAndNotifyPageAndView(content::Visibility, bool) ./../../content/browser/web_contents/web_contents_impl.cc:4021:5
    #8 0x556823c226fa in content::WebContentsImpl::UpdateWebContentsVisibility(content::Visibility) ./../../content/browser/web_contents/web_contents_impl.cc:9590:3
    #9 0x5568334b9eb5 in aura::Window::SetOcclusionInfo(aura::Window::OcclusionState, SkRegion const&) ./../../ui/aura/window.cc:1019:16
    #10 0x5568334fbf90 in aura::DefaultWindowOcclusionChangeBuilder::~DefaultWindowOcclusionChangeBuilder() ./../../ui/aura/window_occlusion_change_builder.cc:35:15
    #11 0x5568334fc2b3 in aura::DefaultWindowOcclusionChangeBuilder::~DefaultWindowOcclusionChangeBuilder() ./../../ui/aura/window_occlusion_change_builder.cc:26:51
    #12 0x5568334ed1e5 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:68:5
    #13 0x5568334ed1e5 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:297:7
    #14 0x5568334ed1e5 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:263:75
    #15 0x5568334ed1e5 in aura::WindowOcclusionTracker::MaybeComputeOcclusion() ./../../ui/aura/window_occlusion_tracker.cc:350:3
    #16 0x5568334ab35d in aura::Window::SetVisibleInternal(bool) ./../../ui/aura/window.cc:1007:1
    #17 0x5568385f1de8 in views::NativeViewHostAura::ShowWidget(int, int, int, int, int, int) ./../../ui/views/controls/native/native_view_host_aura.cc:241:21
    #18 0x5568385ec60e in views::NativeViewHost::Layout() ./../../ui/views/controls/native/native_view_host.cc:144:22
    #19 0x556833bf938f in views::View::Layout() ./../../ui/views/view.cc:873:14
    #20 0x556833beb060 in views::View::SetBoundsRect(gfx::Rect const&) ./../../ui/views/view.cc:387:7
    #21 0x5568441db6fd in ContentsLayoutManager::Layout(views::View*) ./../../chrome/browser/ui/views/frame/contents_layout_manager.cc:44:19
    #22 0x556833bf9178 in views::View::Layout() ./../../ui/views/view.cc:859:25
    #23 0x556843fdaf33 in BrowserView::UpdateDevToolsForContents(content::WebContents*, bool) ./../../chrome/browser/ui/views/frame/browser_view.cc:4577:24
    #24 0x556843fdd249 in BrowserView::OnActiveTabChanged(content::WebContents*, content::WebContents*, int, int) ./../../chrome/browser/ui/views/frame/browser_view.cc:1736:5
    #25 0x5568432cc205 in Browser::OnActiveTabChanged(content::WebContents*, content::WebContents*, int, int) ./../../chrome/browser/ui/browser.cc:2592:12
    #26 0x5568432cb065 in Browser::OnTabStripModelChanged(TabStripModel*, TabStripModelChange const&, TabStripSelectionChange const&) ./../../chrome/browser/ui/browser.cc:1242:3
    #27 0x55684353a912 in TabStripModel::OnChange(TabStripModelChange const&, TabStripSelectionChange const&) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:417:14
    #28 0x55684353d807 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:521:5
    #29 0x556843548397 in TabStripModel::CloseTabs(base::span<content::WebContents* const, 18446744073709551615ul, content::WebContents* const*>, unsigned int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:1928:5
    #30 0x556843549a87 in TabStripModel::CloseWebContentsAt(int, unsigned int) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:706:3
    #31 0x5568433624b7 in chrome::CloseWebContents(Browser*, content::WebContents*, bool) ./../../chrome/browser/ui/browser_tabstrip.cc:98:31
    #32 0x556823bf5826 in content::WebContentsImpl::Close() ./../../content/browser/web_contents/web_contents_impl.cc:7800:16
    #33 0x55681c5265d9 in blink::mojom::LocalMainFrameHostStubDispatch::Accept(blink::mojom::LocalMainFrameHost*, mojo::Message*) ./gen/third_party/blink/public/mojom/frame/frame.mojom.cc:0:0
    #34 0x55682df04f2e in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1016:54
    #35 0x55682df24099 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #36 0x55682df0a5c5 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:701:20
    #37 0x55682e991932 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc_mojo_bootstrap.cc:1075:24
    #38 0x55682e987cdf in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/functional/bind_internal.h:713:12
    #39 0x55682e987cdf in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> > ./../../base/functional/bind_internal.h:868:12
    #40 0x55682e987cdf in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__Cr::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/functional/bind_internal.h:968:12
    #41 0x55682e987cdf in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:919:12
    #42 0x55682b8dd7e8 in Run ./../../base/functional/callback.h:154:12
    #43 0x55682b8dd7e8 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:201:34
    #44 0x55682b946d38 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:11)> ./../../base/task/common/task_annotator.h:89:5
    #45 0x55682b946d38 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:461:23
    #46 0x55682b945bda in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:326:41
    #47 0x55682b947c4a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #48 0x55682bad76ef in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:646:46
    #49 0x55682badab38 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:274:43
    #50 0x7f31d037d703 in g_clear_list ??:?

0x508000264b10 is located 16 bytes before 96-byte region [0x508000264b20,0x508000264b80)
allocated by thread T0 (chrome) here:
    #0 0x556817430c1d in operator new(unsigned long) _asan_rtl_:3
    #1 0x55682528d6da in __libcpp_operator_new<unsigned long> ./../../third_party/libc++/src/include/new:272:10
    #2 0x55682528d6da in __libcpp_allocate ./../../third_party/libc++/src/include/new:298:10
    #3 0x55682528d6da in allocate ./../../third_party/libc++/src/include/__memory/allocator.h:114:38
    #4 0x55682528d6da in __allocate_at_least<std::__Cr::allocator<base::circular_deque<permissions::PermissionRequest *> > > ./../../third_party/libc++/src/include/__memory/allocate_at_least.h:55:19
    #5 0x55682528d6da in __vallocate ./../../third_party/libc++/src/include/vector:756:29
    #6 0x55682528d6da in std::__Cr::vector<base::circular_deque<permissions::PermissionRequest*>, std::__Cr::allocator<base::circular_deque<permissions::PermissionRequest*>>>::vector(unsigned long) ./../../third_party/libc++/src/include/vector:1195:9
    #7 0x556825280de9 in permissions::PermissionRequestManager::PermissionRequestManager(content::WebContents*) ./../../components/permissions/permission_request_manager.cc:772:27
    #8 0x55684304c87d in CreateForWebContents<> ./../../content/public/browser/web_contents_user_data.h:61:32
    #9 0x55684304c87d in TabHelpers::AttachTabHelpers(content::WebContents*) ./../../chrome/browser/ui/tab_helpers.cc:450:3
    #10 0x556843353f92 in AttachTabHelpers ./../../chrome/browser/ui/browser_navigator.cc:89:5
    #11 0x556843353f92 in (anonymous namespace)::CreateTargetContents(NavigateParams const&, GURL const&) ./../../chrome/browser/ui/browser_navigator.cc:557:3
    #12 0x556843350870 in Navigate(NavigateParams*) ./../../chrome/browser/ui/browser_navigator.cc:818:28
    #13 0x5568434df223 in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser*, chrome::startup::IsProcessStartup, std::__Cr::vector<StartupTab, std::__Cr::allocator<StartupTab>> const&) ./../../chrome/browser/ui/startup/startup_browser_creator_impl.cc:331:5
    #14 0x5568434e2060 in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::__Cr::vector<StartupTab, std::__Cr::allocator<StartupTab>> const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, chrome::startup::IsProcessStartup, bool) ./../../chrome/browser/ui/startup/startup_browser_creator_impl.cc:665:13
    #15 0x5568434ddc2d in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(chrome::startup::IsProcessStartup) ./../../chrome/browser/ui/startup/startup_browser_creator_impl.cc:458:22
    #16 0x5568434dcc79 in StartupBrowserCreatorImpl::Launch(Profile*, chrome::startup::IsProcessStartup, std::__Cr::unique_ptr<OldLaunchModeRecorder, std::__Cr::default_delete<OldLaunchModeRecorder>>) ./../../chrome/browser/ui/startup/startup_browser_creator_impl.cc:189:32
    #17 0x5568434d1ad8 in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, std::__Cr::unique_ptr<OldLaunchModeRecorder, std::__Cr::default_delete<OldLaunchModeRecorder>>) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:693:9
    #18 0x5568434d3ce6 in StartupBrowserCreator::ProcessLastOpenedProfiles(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, Profile*, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*>> const&) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:1356:5
    #19 0x5568434d2e22 in StartupBrowserCreator::LaunchBrowserForLastProfiles(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, StartupProfileInfo, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*>> const&) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:780:3
    #20 0x5568434d0814 in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, StartupProfileInfo, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*>> const&) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:0:5
    #21 0x5568434ce73d in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, StartupProfileInfo, std::__Cr::vector<Profile*, std::__Cr::allocator<Profile*>> const&) ./../../chrome/browser/ui/startup/startup_browser_creator.cc:647:10
    #22 0x55682a29b30d in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() ./../../chrome/browser/chrome_browser_main.cc:1716:25
    #23 0x55682a2998a6 in ChromeBrowserMainParts::PreMainMessageLoopRun() ./../../chrome/browser/chrome_browser_main.cc:1197:18
    #24 0x556821c8c035 in content::BrowserMainLoop::PreMainMessageLoopRun() ./../../content/browser/browser_main_loop.cc:1002:28
    #25 0x556821c9459f in Invoke<int (content::BrowserMainLoop::*)(), content::BrowserMainLoop *> ./../../base/functional/bind_internal.h:713:12
    #26 0x556821c9459f in MakeItSo<int (content::BrowserMainLoop::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:868:12
    #27 0x556821c9459f in RunImpl<int (content::BrowserMainLoop::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:968:12
    #28 0x556821c9459f in base::internal::Invoker<base::internal::BindState<int (content::BrowserMainLoop::*)(), base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, int ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:919:12
    #29 0x5568239f0cd8 in Run ./../../base/functional/callback.h:154:12
    #30 0x5568239f0cd8 in content::StartupTaskRunner::RunAllTasksNow() ./../../content/browser/startup_task_runner.cc:42:29
    #31 0x556821c8ae58 in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser_main_loop.cc:913:25
    #32 0x556821c97372 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) ./../../content/browser/browser_main_runner_impl.cc:139:15
    #33 0x556821c84cd6 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:30:32
    #34 0x55682859198b in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:707:10
    #35 0x55682859673e in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1298:10
    #36 0x556828595bee in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1142:12
    #37 0x55682858e36d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:334:36
    #38 0x55682858ea9f in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:347:10
    #39 0x556817433312 in ChromeMain ./../../chrome/app/chrome_main.cc:190:12
    #40 0x7f31cee456c9 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

It looks like we're dereferencing rend().

[Monorail components: UI>Browser>Permissions>Prompts]

### [Deleted User] (2023-10-31)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-10-31)

Thanks for reproduction. I forget attach the asan.log. Here's my asan.log.

### dc...@chromium.org (2023-10-31)

I /think/ this is high, because I don't see any virtual calls involved here–otherwise, this would be a critical.

If I missed something, please do comment here, and we can reassess the severity.

### dc...@chromium.org (2023-10-31)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-10-31)

The furture exploit will have attack vector to hijack control flow.

Here is a possible attack way:
1. Attacker fake the uaf object to pass the IsEmbeddedPermissionElementInitiated[1] check and set current_request_fate = CurrentRequestFate::kPreempt;  .
2. In the following CurrentRequestFate::kPreempt case. The validated_requests_set_.find(next_candidate) != validated_requests_set_.end() will be bypassed because ValidateRequest function before has removed the uaf object from validated_requests_set_. 
3.Then the control flow goes to pending_permission_requests_.PushFront[3].  The uaf object will be pushed to the pending_permission_requests_ again. 
4. At this time, there's a dangling pointer in pending_permission_requests_ .
5. Attacker can use this dangling pointer to call a callback by following way:
PermissionRequestManager::CleanUpRequests()
->CancelledIncludingDuplicates(pending_request)
->request->Cancelled()

void PermissionRequest::Cancelled(bool is_final_decision) {
  permission_decided_callback_.Run(CONTENT_SETTING_DEFAULT,
                                   /*is_one_time=*/false, is_final_decision);
}
We can see from cancelled function.  the callback's structure including the function pointer is all controlled by user. Thus they can hijack control flow.



  if (current_request_fate == CurrentRequestFate::kKeepCurrent &&
      pending_permission_requests_.Peek()
          ->IsEmbeddedPermissionElementInitiated()) {   ---------------[1]
    current_request_fate = CurrentRequestFate::kPreempt;  
  }

  switch (current_request_fate) {
    case CurrentRequestFate::kKeepCurrent:
      return true;
    case CurrentRequestFate::kPreempt: {
      DCHECK(!pending_permission_requests_.IsEmpty());
      auto* next_candidate = pending_permission_requests_.Peek();

      // Consider a case of infinite loop here (eg: 2 low priority requests can
      // preempt each other, causing a loop). We only preempt the current
      // request if the next candidate has just been added to pending queue but
      // not validated yet.
      if (validated_requests_set_.find(next_candidate) !=
          validated_requests_set_.end()) {   -----------------[2]
        return true;
      }

      pending_permission_requests_.Pop();
      PreemptAndRequeueCurrentRequest();
      pending_permission_requests_.PushFront(next_candidate); ----------------[3]
      ScheduleDequeueRequestIfNeeded();
      return false;
    }

### dc...@chromium.org (2023-10-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-31)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-31)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-10-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/944ef12262f26ef9bd18cc92606cb07c302e9d8a

commit 944ef12262f26ef9bd18cc92606cb07c302e9d8a
Author: Thomas Nguyen <tungnh@chromium.org>
Date: Tue Oct 31 18:03:52 2023

Check non-empty precondition before peek and pop permissions queue

Bug: 1497867
Change-Id: Ie9a32813eb45bd8ff707572d66264bcbd8d46b15
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4993484
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1217735}

[modify] https://crrev.com/944ef12262f26ef9bd18cc92606cb07c302e9d8a/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/944ef12262f26ef9bd18cc92606cb07c302e9d8a/components/permissions/permission_request_queue_unittest.cc
[modify] https://crrev.com/944ef12262f26ef9bd18cc92606cb07c302e9d8a/components/permissions/permission_request_queue.h
[modify] https://crrev.com/944ef12262f26ef9bd18cc92606cb07c302e9d8a/components/permissions/permission_request_queue.cc


### am...@chromium.org (2023-10-31)

Adding other permissions owners / engineers to this issue -- can someone PTAL at soonest. 
It appears that andypaicu@ and tungnh@ are both out until 2 November. This is a recently introduced security regression and as such is a beta channel release blocker (M120 beta was scheduled to be released tomorrow)

### tu...@chromium.org (2023-10-31)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-10-31)

[Empty comment from Monorail migration]

### go...@chromium.org (2023-10-31)

Not M120 just branched last night so in order to trigger a new canary we needed to merge the change to M120 branch 6099, here is M120 merge in CQ - https://chromium-review.googlesource.com/c/chromium/src/+/4994308.

### go...@chromium.org (2023-10-31)

M120 merge landed - https://chromium-review.googlesource.com/c/chromium/src/+/4994308. 

Triggered a new Android & Desktop #120.0.6099.4. Requesting Android Beta qualification for release  tomorrow for the same canary #120.0.6099.4 pending canary coverage.

Please update the bug with the canary result tomorrow. 

### go...@chromium.org (2023-10-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-31)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-01)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M120, which branched on 2023-10-30 (Chromium branch: 6099, Chromium branch position: 1217362)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-01)

has already been merged to 120

### vo...@google.com (2023-11-02)

Introduced in M120 (https://crrev.com/c/4915775) so not applicable to M114 LTS.

### [Deleted User] (2023-11-02)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M120, which branched on 2023-10-30 (Chromium branch: 6099, Chromium branch position: 1217362)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-02)

this was already merged to 120; adding merge-na- label to quell the satisfy the bot

### am...@google.com (2023-11-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-09)

Congratulations! The Chrome VRP Panel has decided to award you $30,000 + $10,000 baseline renderer RCE since a compromised renderer was not needed + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us -- excellent work! 

### ha...@gmail.com (2023-11-10)

Thanks for the reward!

### am...@google.com (2023-11-11)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1497867?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075944)*
