# heap-buffer-overflow in MoveWebContentsAtImpl(extension)

| Field | Value |
|-------|-------|
| **Issue ID** | [40053963](https://issues.chromium.org/issues/40053963) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@gmail.com |
| **Assignee** | co...@chromium.org |
| **Created** | 2020-11-23 |
| **Bounty** | $15,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36

Steps to reproduce the problem:
tested version:
Chromium 88.0.4288.0
Chromium 89.0.4327.0 
tested OS version:
ubuntu 20.04

The crash occurs immediately after the plug-in is loaded.

What is the expected behavior?

What went wrong?
=================================================================
==20047==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200072d1a8 at pc 0x55bd538f4567 bp 0x7ffc1518da10 sp 0x7ffc1518da08
READ of size 8 at 0x60200072d1a8 thread T0 (chrome)
    #0 0x55bd538f4566 in release ./../../buildtools/third_party/libc++/trunk/include/memory:2623:26
    #1 0x55bd538f4566 in operator= ./../../buildtools/third_party/libc++/trunk/include/memory:2552:15
    #2 0x55bd538f4566 in __move_backward<std::unique_ptr<TabStripModel::WebContentsData> *, std::unique_ptr<TabStripModel::WebContentsData> *> ./../../buildtools/third_party/libc++/trunk/include/algorithm:1876:21
    #3 0x55bd538f4566 in move_backward<std::unique_ptr<TabStripModel::WebContentsData> *, std::unique_ptr<TabStripModel::WebContentsData> *> ./../../buildtools/third_party/libc++/trunk/include/algorithm:1905:12
    #4 0x55bd538f4566 in std::__1::vector<std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> >, std::__1::allocator<std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> > > >::__move_range(std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> >*, std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> >*, std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> >*) ./../../buildtools/third_party/libc++/trunk/include/vector:1760:5
    #5 0x55bd538ebf21 in std::__1::vector<std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> >, std::__1::allocator<std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> > > >::insert(std::__1::__wrap_iter<std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> > const*>, std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> >&&) ./../../buildtools/third_party/libc++/trunk/include/vector:1818:13
    #6 0x55bd538d5854 in TabStripModel::MoveWebContentsAtImpl(int, int, bool) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:1936:18
    #7 0x55bd538e0712 in MoveAndSetGroup ./../../chrome/browser/ui/tabs/tab_strip_model.cc:2099:5
    #8 0x55bd538e0712 in TabStripModel::MoveTabsAndSetGroupImpl(std::__1::vector<int, std::__1::allocator<int> > const&, int, base::Optional<tab_groups::TabGroupId>) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:2072:5
    #9 0x55bd538df2b6 in TabStripModel::AddToNewGroupImpl(std::__1::vector<int, std::__1::allocator<int> > const&, tab_groups::TabGroupId const&) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:2015:3
    #10 0x55bd538deaec in TabStripModel::AddToNewGroup(std::__1::vector<int, std::__1::allocator<int> > const&) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:1056:3
    #11 0x55bd5210411f in extensions::TabsGroupFunction::Run() ./../../chrome/browser/extensions/api/tabs/tabs_api.cc:1842:24
    #12 0x55bd4442e7bd in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension_function.cc:448:10
    #13 0x55bd44436275 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int, base::RepeatingCallback<void (ExtensionFunction::ResponseType, base::ListValue const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)> const&) ./../../extensions/browser/extension_function_dispatcher.cc:383:15
    #14 0x55bd444352fa in extensions::ExtensionFunctionDispatcher::Dispatch(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int) ./../../extensions/browser/extension_function_dispatcher.cc:257:5
    #15 0x55bd444a9ec7 in DispatchToMethodImpl<extensions::ExtensionWebContentsObserver, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost *, const ExtensionHostMsg_Request_Params &), content::RenderFrameHost, std::tuple<ExtensionHostMsg_Request_Params>, 0> ./../../ipc/ipc_message_templates.h:65:3
    #16 0x55bd444a9ec7 in DispatchToMethod<extensions::ExtensionWebContentsObserver, content::RenderFrameHost, const ExtensionHostMsg_Request_Params &, std::tuple<ExtensionHostMsg_Request_Params> > ./../../ipc/ipc_message_templates.h:77:3
    #17 0x55bd444a9ec7 in bool IPC::MessageT<ExtensionHostMsg_Request_Meta, std::__1::tuple<ExtensionHostMsg_Request_Params>, void>::Dispatch<extensions::ExtensionWebContentsObserver, extensions::ExtensionWebContentsObserver, content::RenderFrameHost, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost*, ExtensionHostMsg_Request_Params const&)>(IPC::Message const*, extensions::ExtensionWebContentsObserver*, extensions::ExtensionWebContentsObserver*, content::RenderFrameHost*, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost*, ExtensionHostMsg_Request_Params const&)) ./../../ipc/ipc_message_templates.h:140:7
    #18 0x55bd444a9c40 in extensions::ExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) ./../../extensions/browser/extension_web_contents_observer.cc:235:5
    #19 0x55bd5235c007 in extensions::ChromeExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) ./../../chrome/browser/extensions/chrome_extension_web_contents_observer.cc:94:37
    #20 0x55bd43909aa0 in content::WebContentsImpl::OnMessageReceived(content::RenderFrameHostImpl*, IPC::Message const&) ./../../content/browser/web_contents/web_contents_impl.cc:1157:18
    #21 0x55bd43359be7 in content::RenderFrameHostImpl::OnMessageReceived(IPC::Message const&) ./../../content/browser/renderer_host/render_frame_host_impl.cc:1839:18
    #22 0x55bd4c5c5207 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ./../../ipc/ipc_channel_proxy.cc:325:14
    #23 0x55bd49301197 in Run ./../../base/callback.h:101:12
    #24 0x55bd49301197 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:163:33
    #25 0x55bd4933e431 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351:25
    #26 0x55bd4933db84 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264:36
    #27 0x55bd4922c910 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:404:48
    #28 0x55bd493403fc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:460:12
    #29 0x55bd492ae9a0 in base::RunLoop::Run() ./../../base/run_loop.cc:131:14
    #30 0x55bd49d9f180 in ChromeBrowserMainParts::MainMessageLoopRun(int*) ./../../chrome/browser/chrome_browser_main.cc:1710:15
    #31 0x55bd427be5a8 in content::BrowserMainLoop::RunMainMessageLoopParts() ./../../content/browser/browser_main_loop.cc:1021:29
    #32 0x55bd427c4455 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:150:15
    #33 0x55bd427b6345 in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser_main.cc:47:28
    #34 0x55bd49011f2b in RunBrowserProcessMain ./../../content/app/content_main_runner_impl.cc:520:10
    #35 0x55bd49011f2b in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) ./../../content/app/content_main_runner_impl.cc:1010:10
    #36 0x55bd490111e2 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:885:12
    #37 0x55bd4900ad7e in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:372:36
    #38 0x55bd4900b36c in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:398:10
    #39 0x55bd3e1528f7 in ChromeMain ./../../chrome/app/chrome_main.cc:130:12
    #40 0x7f598e4c41e2 in __libc_start_main /build/glibc-5mDdLG/glibc-2.30/csu/../csu/libc-start.c:308:16

0x60200072d1a8 is located 8 bytes to the left of 16-byte region [0x60200072d1b0,0x60200072d1c0)
allocated by thread T0 (chrome) here:
    #0 0x55bd3e14fddd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55bd538ec066 in __libcpp_allocate ./../../buildtools/third_party/libc++/trunk/include/new:253:10
    #2 0x55bd538ec066 in allocate ./../../buildtools/third_party/libc++/trunk/include/memory:1853:37
    #3 0x55bd538ec066 in allocate ./../../buildtools/third_party/libc++/trunk/include/memory:1570:21
    #4 0x55bd538ec066 in __split_buffer ./../../buildtools/third_party/libc++/trunk/include/__split_buffer:318:29
    #5 0x55bd538ec066 in std::__1::vector<std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> >, std::__1::allocator<std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> > > >::insert(std::__1::__wrap_iter<std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> > const*>, std::__1::unique_ptr<TabStripModel::WebContentsData, std::__1::default_delete<TabStripModel::WebContentsData> >&&) ./../../buildtools/third_party/libc++/trunk/include/vector:1825:53
    #6 0x55bd538cef2e in TabStripModel::InsertWebContentsAtImpl(int, std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, int, base::Optional<tab_groups::TabGroupId>) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:1687:18
    #7 0x55bd538dce9d in TabStripModel::AddWebContents(std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, int, ui::PageTransition, int, base::Optional<tab_groups::TabGroupId>) ./../../chrome/browser/ui/tabs/tab_strip_model.cc:987:3
    #8 0x55bd537ee0d3 in Navigate(NavigateParams*) ./../../chrome/browser/ui/browser_navigator.cc:684:41
    #9 0x55bd524b6166 in extensions::ExtensionTabUtil::OpenTab(ExtensionFunction*, extensions::ExtensionTabUtil::OpenTabParams const&, bool, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >*) ./../../chrome/browser/extensions/extension_tab_util.cc:308:3
    #10 0x55bd520f7f7e in extensions::TabsCreateFunction::Run() ./../../chrome/browser/extensions/api/tabs/tabs_api.cc:1169:7
    #11 0x55bd4442e7bd in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension_function.cc:448:10
    #12 0x55bd44436275 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int, base::RepeatingCallback<void (ExtensionFunction::ResponseType, base::ListValue const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)> const&) ./../../extensions/browser/extension_function_dispatcher.cc:383:15
    #13 0x55bd444352fa in extensions::ExtensionFunctionDispatcher::Dispatch(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int) ./../../extensions/browser/extension_function_dispatcher.cc:257:5
    #14 0x55bd444a9ec7 in DispatchToMethodImpl<extensions::ExtensionWebContentsObserver, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost *, const ExtensionHostMsg_Request_Params &), content::RenderFrameHost, std::tuple<ExtensionHostMsg_Request_Params>, 0> ./../../ipc/ipc_message_templates.h:65:3
    #15 0x55bd444a9ec7 in DispatchToMethod<extensions::ExtensionWebContentsObserver, content::RenderFrameHost, const ExtensionHostMsg_Request_Params &, std::tuple<ExtensionHostMsg_Request_Params> > ./../../ipc/ipc_message_templates.h:77:3
    #16 0x55bd444a9ec7 in bool IPC::MessageT<ExtensionHostMsg_Request_Meta, std::__1::tuple<ExtensionHostMsg_Request_Params>, void>::Dispatch<extensions::ExtensionWebContentsObserver, extensions::ExtensionWebContentsObserver, content::RenderFrameHost, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost*, ExtensionHostMsg_Request_Params const&)>(IPC::Message const*, extensions::ExtensionWebContentsObserver*, extensions::ExtensionWebContentsObserver*, content::RenderFrameHost*, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost*, ExtensionHostMsg_Request_Params const&)) ./../../ipc/ipc_message_templates.h:140:7
    #17 0x55bd444a9c40 in extensions::ExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) ./../../extensions/browser/extension_web_contents_observer.cc:235:5
    #18 0x55bd5235c007 in extensions::ChromeExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) ./../../chrome/browser/extensions/chrome_extension_web_contents_observer.cc:94:37
    #19 0x55bd43909aa0 in content::WebContentsImpl::OnMessageReceived(content::RenderFrameHostImpl*, IPC::Message const&) ./../../content/browser/web_contents/web_contents_impl.cc:1157:18
    #20 0x55bd43359be7 in content::RenderFrameHostImpl::OnMessageReceived(IPC::Message const&) ./../../content/browser/renderer_host/render_frame_host_impl.cc:1839:18
    #21 0x55bd4c5c5207 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ./../../ipc/ipc_channel_proxy.cc:325:14
    #22 0x55bd49301197 in Run ./../../base/callback.h:101:12
    #23 0x55bd49301197 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:163:33
    #24 0x55bd4933e431 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:351:25
    #25 0x55bd4933db84 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:264:36
    #26 0x55bd4922d689 in HandleDispatch ./../../base/message_loop/message_pump_glib.cc:374:46
    #27 0x55bd4922d689 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:124:43
    #28 0x7f599011f8bc in g_main_context_dispatch ??:0:0

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/test/chromium/gsutil/asan-linux-release-830071/chrome+0x1fa48566)
Shadow bytes around the buggy address:
  0x0c04800dd9e0: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa 00 fa
  0x0c04800dd9f0: fa fa 00 00 fa fa 00 00 fa fa 00 fa fa fa 00 fa
  0x0c04800dda00: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00
  0x0c04800dda10: fa fa 00 fa fa fa 00 fa fa fa fd fa fa fa fd fa
  0x0c04800dda20: fa fa fd fd fa fa fd fd fa fa 00 fa fa fa fd fa
=>0x0c04800dda30: fa fa fd fa fa[fa]00 00 fa fa fd fa fa fa fd fa
  0x0c04800dda40: fa fa fd fa fa fa fd fd fa fa 00 fa fa fa 00 fa
  0x0c04800dda50: fa fa 00 fa fa fa 00 fa fa fa 00 00 fa fa 00 00
  0x0c04800dda60: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00
  0x0c04800dda70: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00
  0x0c04800dda80: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00
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
==20047==ABORTING

Did this work before? N/A 

Chrome version: Chromium 88.0.4288.0  Channel: n/a
OS Version: 20.04
Flash Version:

## Attachments

- [background.js](attachments/background.js) (text/plain, 232 B)
- [manifest.json](attachments/manifest.json) (text/plain, 372 B)

## Timeline

### [Deleted User] (2020-11-23)

[Empty comment from Monorail migration]

### mb...@chromium.org (2020-11-23)

cyan: Could you take a look at this or help find another owner?

[Monorail components: Platform>Extensions>API UI>Browser>TabStrip>TabGroups]

### cy...@chromium.org (2020-11-23)

-> connily@ for extensions + tabs?

### co...@chromium.org (2020-11-23)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d375f99a808e300fe615ad614bec0474ea9b89b7

commit d375f99a808e300fe615ad614bec0474ea9b89b7
Author: Connie Wan <connily@chromium.org>
Date: Tue Nov 24 00:01:05 2020

tabs.group(): Dedupe tab IDs before grouping

This intentionally doesn't throw an error, to be consistent with other functions such as tabs.move().

Includes a regression test for the attached bug.

Bug: 1151799
Change-Id: I8ee69bae769c63e0f0d48aadc3f45a2c8f821752
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2556004
Commit-Queue: Connie Wan <connily@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#830370}

[modify] https://crrev.com/d375f99a808e300fe615ad614bec0474ea9b89b7/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/d375f99a808e300fe615ad614bec0474ea9b89b7/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc
[modify] https://crrev.com/d375f99a808e300fe615ad614bec0474ea9b89b7/chrome/browser/ui/tabs/tab_strip_model.cc


### co...@chromium.org (2020-11-24)

Requesting merge to M88 for crrev.com/c/2556004 to fix this issue.

### [Deleted User] (2020-11-24)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-25)

Your change meets the bar and is auto-approved for M88. Please go ahead and merge the CL to branch 4324 (refs/branch-heads/4324) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3de5dcc2758e03111be0f7e8dec23c8dd908742b

commit 3de5dcc2758e03111be0f7e8dec23c8dd908742b
Author: Connie Wan <connily@chromium.org>
Date: Wed Nov 25 01:16:57 2020

tabs.group(): Dedupe tab IDs before grouping

This intentionally doesn't throw an error, to be consistent with other functions such as tabs.move().

Includes a regression test for the attached bug.

(cherry picked from commit d375f99a808e300fe615ad614bec0474ea9b89b7)

Bug: 1151799
Change-Id: I8ee69bae769c63e0f0d48aadc3f45a2c8f821752
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2556004
Commit-Queue: Connie Wan <connily@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#830370}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2559229
Reviewed-by: Connie Wan <connily@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#320}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/3de5dcc2758e03111be0f7e8dec23c8dd908742b/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/3de5dcc2758e03111be0f7e8dec23c8dd908742b/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc
[modify] https://crrev.com/3de5dcc2758e03111be0f7e8dec23c8dd908742b/chrome/browser/ui/tabs/tab_strip_model.cc


### co...@chromium.org (2020-11-25)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-25)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-25)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-03)

On discussion at the VRP panel we are upping the severity here to High.

Thanks for the report - the panel has decided to award $15,000 :)

### ad...@google.com (2020-12-04)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1151799?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053963)*
