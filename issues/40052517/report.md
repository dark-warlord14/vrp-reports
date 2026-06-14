# uaf in extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [40052517](https://issues.chromium.org/issues/40052517) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ka...@chromium.org |
| **Created** | 2020-06-08 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36

Steps to reproduce the problem:

Version 85.0.4151.0(Developer Build)

===================================================================================================

A. Tab properties related
1) (optional) id	
The ID of the tab. Tab IDs are unique within a browser session. Under some circumstances a tab may not be assigned an ID; for example, when querying foreign tabs using the sessions API, in which case a session ID may be present. Tab ID can also be set to chrome.tabs.TAB_ID_NONE for apps and devtools windows.

2) index	
The zero-based index of the tab within its window.

3) openerTabId	
The ID of the tab that opened this tab, if any. This property is only present if the opener tab still exists.

B. poc
1)
chrome.tabs.getCurrent(function(var_tab_1){})
chrome.tabs.create({},function(var_tab_2){})
        | tab_1           | tab_2           |
        ------------------------------------- 
        | id : x          | id : y          |
        | index: 1        | index : 2       |
        | openerTabId :   | openerTabId :   |

2) 
chrome.tabs.update(var_tab_1.id,{openerTabId:var_tab_2.id})
chrome.tabs.update(var_tab_2.id,{openerTabId:var_tab_1.id}) 
        | tab_1           | tab_2           |
        ----------------- -------------------
        | id : x          | id : y          |
        | index: 1        | index : 2       |
        | openerTabId : y | openerTabId : x |

3)
chrome.tabs.move(var_tab_1.id,{index:2})
        | -----           | tab_2           | tab_1           |
        ----------------- -------------------------------------
        | id : -          | id : y          | id : x          |
        | index: -        | index : 2       | index: 2        |
        | openerTabId : - | openerTabId : x | openerTabId : y |
    ===>
        | tab_2           | tab_1           | 
        ------------------------------------- 
        | id : y          | id : x          | 
        | index : 1       | index: 2        | 
        | openerTabId : x | openerTabId : y | 

4)
chrome.tabs.discard(var_tab_2.id)
        | tab_2           | tab_1           | 
        ------------------------------------- 
        | id : y          | id : x          | 
        | index : 1       | index: 2        | 
        | openerTabId : x | openerTabId : y | 
    //After discarded tab_2, tab_1 's index become "1", then this function will restore the discarded tab (tab_2) in case it is been activated later.
    chrome/browser/extensions/extension_tab_util.cc:ExtensionTabUtil::CreateTabObject(WebContents* contents,...) {
        ...
        if (tab_strip) {
            WebContents* opener = tab_strip->GetOpenerOfWebContentsAt(tab_index);       <---- //the contents belongs to tab_2, whose index was "1". But the new index "1" points to tab_1, so the opener is tab_2, THE DISCARDED TAB, resulting UAF.
            if (opener) {
            tab_object->opener_tab_id =
                std::make_unique<int>(GetTabIdForExtensions(opener));
            }
        }
        ...
    }

Reprodution Step:
1. extension_poc.zip
2. open chrome
3. click "Settings"->"Load unpacked"
4. select unzipped folder path

What is the expected behavior?

What went wrong?

=================================================================
==29939==ERROR: AddressSanitizer: heap-use-after-free on address 0x61d0006ef098 at pc 0x7fbe45882084 bp 0x7fff0c065300 sp 0x7fff0c0652f8
READ of size 8 at 0x61d0006ef098 thread T0 (chrome)
    #0 0x7fbe45882083 in __root ./../../buildtools/third_party/libc++/trunk/include/__tree:1082:59
    #1 0x7fbe45882083 in find<const void *> ./../../buildtools/third_party/libc++/trunk/include/__tree:2574:45
    #2 0x7fbe45882083 in find ./../../buildtools/third_party/libc++/trunk/include/map:1380:68
    #3 0x7fbe45882083 in base::SupportsUserData::GetUserData(void const*) const ./../../base/supports_user_data.cc:26:27
    #4 0x7fbe2e0a1ff3 in FromWebContents ./../../content/public/browser/web_contents_user_data.h:52:44
    #5 0x7fbe2e0a1ff3 in sessions::SessionTabHelper::IdForTab(content::WebContents const*) ./../../components/sessions/content/session_tab_helper.cc:54:13
    #6 0x558e287bc6d5 in GetTabIdForExtensions ./../../chrome/browser/extensions/extension_tab_util.cc:112:10
    #7 0x558e287bc6d5 in extensions::ExtensionTabUtil::CreateTabObject(content::WebContents*, extensions::ExtensionTabUtil::ScrubTabBehavior, extensions::Extension const*, TabStripModel*, int) ./../../chrome/browser/extensions/extension_tab_util.cc:467:33
    #8 0x558e28483a86 in CreateTabObjectHelper ./../../chrome/browser/extensions/api/tabs/tabs_api.cc:280:10
    #9 0x558e28483a86 in extensions::TabsDiscardFunction::Run() ./../../chrome/browser/extensions/api/tabs/tabs_api.cc:2125:54

    #10 0x558e24a6004f in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension_function.cc:442:10
    #11 0x558e24a67635 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int, base::RepeatingCallback<void (ExtensionFunction::ResponseType, base::ListValue const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)> const&) ./../../extensions/browser/extension_function_dispatcher.cc:383:15

    #12 0x558e24a6674a in extensions::ExtensionFunctionDispatcher::Dispatch(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int) ./../../extensions/browser/extension_function_dispatcher.cc:257:5
    #13 0x558e24adf30b in DispatchToMethodImpl<extensions::ExtensionWebContentsObserver, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost *, const ExtensionHostMsg_Request_Params &), content::RenderFrameHost, std::__Cr::tuple<ExtensionHostMsg_Request_Params>, 0> ./../../ipc/ipc_message_templates.h:64:3
    #14 0x558e24adf30b in DispatchToMethod<extensions::ExtensionWebContentsObserver, content::RenderFrameHost, const ExtensionHostMsg_Request_Params &, std::__Cr::tuple<ExtensionHostMsg_Request_Params>> ./../../ipc/ipc_message_templates.h:76:3
    #15 0x558e24adf30b in bool IPC::MessageT<ExtensionHostMsg_Request_Meta, std::__Cr::tuple<ExtensionHostMsg_Request_Params>, void>::Dispatch<extensions::ExtensionWebContentsObserver, extensions::ExtensionWebContentsObserver, content::RenderFrameHost, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost*, ExtensionHostMsg_Request_Params const&)>(IPC::Message const*, extensions::ExtensionWebContentsObserver*, extensions::ExtensionWebContentsObserver*, content::RenderFrameHost*, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost*, ExtensionHostMsg_Request_Params const&)) ./../../ipc/ipc_message_templates.h:139:7
    #16 0x558e24adf0ae in extensions::ExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) ./../../extensions/browser/extension_web_contents_observer.cc:235:5
    #17 0x558e2865c907 in extensions::ChromeExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) ./../../chrome/browser/extensions/chrome_extension_web_contents_observer.cc:94:37
    #18 0x7fbe3b0dcd9e in content::WebContentsImpl::OnMessageReceived(content::RenderFrameHostImpl*, IPC::Message const&) ./../../content/browser/web_contents/web_contents_impl.cc:919:18
    #19 0x7fbe3a52a0f2 in content::RenderFrameHostImpl::OnMessageReceived(IPC::Message const&) ./../../content/browser/frame_host/render_frame_host_impl.cc:1678:18
    #20 0x7fbe3ac20651 in content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) ./../../content/browser/renderer_host/render_process_host_impl.cc:3619:20
    #21 0x7fbe41b3410c in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ./../../ipc/ipc_channel_proxy.cc:327:14
    #22 0x7fbe45893e49 in Run ./../../base/callback.h:99:12
    #23 0x7fbe45893e49 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #24 0x7fbe458d3911 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:329:23
    #25 0x7fbe458d3278 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:254:36
    #26 0x7fbe4578fc9c in HandleDispatch ./../../base/message_loop/message_pump_glib.cc:409:46
    #27 0x7fbe4578fc9c in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:122:43
    #28 0x7fbe108588bc in g_main_context_dispatch ??:0:0

0x61d0006ef098 is located 24 bytes inside of 2384-byte region [0x61d0006ef080,0x61d0006ef9d0)
freed by thread T0 (chrome) here:
    #0 0x558e242849ad in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x558e26999e22 in operator() ./../../buildtools/third_party/libc++/trunk/include/memory:2378:5
    #2 0x558e26999e22 in reset ./../../buildtools/third_party/libc++/trunk/include/memory:2633:7
    #3 0x558e26999e22 in resource_coordinator::TabLifecycleUnitSource::TabLifecycleUnit::FinishDiscard(mojom::LifecycleUnitDiscardReason) ./../../chrome/browser/resource_coordinator/tab_lifecycle_unit.cc:833:24
    #4 0x558e2699a2bd in resource_coordinator::TabLifecycleUnitSource::TabLifecycleUnit::Discard(mojom::LifecycleUnitDiscardReason) ./../../chrome/browser/resource_coordinator/tab_lifecycle_unit.cc:861:3
    #5 0x558e269a7b9c in resource_coordinator::TabManager::DiscardTabByExtension(content::WebContents*) ./../../chrome/browser/resource_coordinator/tab_manager.cc:251:38
    #6 0x558e284839f5 in extensions::TabsDiscardFunction::Run() ./../../chrome/browser/extensions/api/tabs/tabs_api.cc:2120:43
    #7 0x558e24a6004f in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension_function.cc:442:10
    #8 0x558e24a67635 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int, base::RepeatingCallback<void (ExtensionFunction::ResponseType, base::ListValue const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)> const&) ./../../extensions/browser/extension_function_dispatcher.cc:383:15
    #9 0x558e24a6674a in extensions::ExtensionFunctionDispatcher::Dispatch(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int) ./../../extensions/browser/extension_function_dispatcher.cc:257:5
    #10 0x558e24adf30b in DispatchToMethodImpl<extensions::ExtensionWebContentsObserver, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost *, const ExtensionHostMsg_Request_Params &), content::RenderFrameHost, std::__Cr::tuple<ExtensionHostMsg_Request_Params>, 0> ./../../ipc/ipc_message_templates.h:64:3
    #11 0x558e24adf30b in DispatchToMethod<extensions::ExtensionWebContentsObserver, content::RenderFrameHost, const ExtensionHostMsg_Request_Params &, std::__Cr::tuple<ExtensionHostMsg_Request_Params>> ./../../ipc/ipc_message_templates.h:76:3
    #12 0x558e24adf30b in bool IPC::MessageT<ExtensionHostMsg_Request_Meta, std::__Cr::tuple<ExtensionHostMsg_Request_Params>, void>::Dispatch<extensions::ExtensionWebContentsObserver, extensions::ExtensionWebContentsObserver, content::RenderFrameHost, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost*, ExtensionHostMsg_Request_Params const&)>(IPC::Message const*, extensions::ExtensionWebContentsObserver*, extensions::ExtensionWebContentsObserver*, content::RenderFrameHost*, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost*, ExtensionHostMsg_Request_Params const&)) ./../../ipc/ipc_message_templates.h:139:7
    #13 0x558e24adf0ae in extensions::ExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) ./../../extensions/browser/extension_web_contents_observer.cc:235:5
    #14 0x558e2865c907 in extensions::ChromeExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) ./../../chrome/browser/extensions/chrome_extension_web_contents_observer.cc:94:37
    #15 0x7fbe3b0dcd9e in content::WebContentsImpl::OnMessageReceived(content::RenderFrameHostImpl*, IPC::Message const&) ./../../content/browser/web_contents/web_contents_impl.cc:919:18
    #16 0x7fbe3a52a0f2 in content::RenderFrameHostImpl::OnMessageReceived(IPC::Message const&) ./../../content/browser/frame_host/render_frame_host_impl.cc:1678:18
    #17 0x7fbe3ac20651 in content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) ./../../content/browser/renderer_host/render_process_host_impl.cc:3619:20
    #18 0x7fbe41b3410c in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ./../../ipc/ipc_channel_proxy.cc:327:14
    #19 0x7fbe45893e49 in Run ./../../base/callback.h:99:12
    #20 0x7fbe45893e49 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #21 0x7fbe458d3911 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:329:23
    #22 0x7fbe458d3278 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:254:36
    #23 0x7fbe4578fc9c in HandleDispatch ./../../base/message_loop/message_pump_glib.cc:409:46
    #24 0x7fbe4578fc9c in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:122:43
    #25 0x7fbe108588bc in g_main_context_dispatch ??:0:0

previously allocated by thread T0 (chrome) here:
    #0 0x558e2428414d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x7fbe3b0cf70b in content::WebContentsImpl::CreateWithOpener(content::WebContents::CreateParams const&, content::RenderFrameHostImpl*) ./../../content/browser/web_contents/web_contents_impl.cc:769:7
    #2 0x7fbe3b0cf39e in Create ./../../content/browser/web_contents/web_contents_impl.cc:327:10
    #3 0x7fbe3b0cf39e in content::WebContents::Create(content::WebContents::CreateParams const&) ./../../content/browser/web_contents/web_contents_impl.cc:322:10
    #4 0x558e29d57323 in CreateTargetContents ./../../chrome/browser/ui/browser_navigator.cc:437:7
    #5 0x558e29d57323 in Navigate(NavigateParams*) ./../../chrome/browser/ui/browser_navigator.cc:634:28
    #6 0x558e287b965a in extensions::ExtensionTabUtil::OpenTab(ExtensionFunction*, extensions::ExtensionTabUtil::OpenTabParams const&, bool, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >*) ./../../chrome/browser/extensions/extension_tab_util.cc:305:3
    #7 0x558e28470edc in extensions::TabsCreateFunction::Run() ./../../chrome/browser/extensions/api/tabs/tabs_api.cc:1070:7
    #8 0x558e24a6004f in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension_function.cc:442:10
    #9 0x558e24a67635 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int, base::RepeatingCallback<void (ExtensionFunction::ResponseType, base::ListValue const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)> const&) ./../../extensions/browser/extension_function_dispatcher.cc:383:15
    #10 0x558e24a6674a in extensions::ExtensionFunctionDispatcher::Dispatch(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int) ./../../extensions/browser/extension_function_dispatcher.cc:257:5
    #11 0x558e24adf30b in DispatchToMethodImpl<extensions::ExtensionWebContentsObserver, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost *, const ExtensionHostMsg_Request_Params &), content::RenderFrameHost, std::__Cr::tuple<ExtensionHostMsg_Request_Params>, 0> ./../../ipc/ipc_message_templates.h:64:3
    #12 0x558e24adf30b in DispatchToMethod<extensions::ExtensionWebContentsObserver, content::RenderFrameHost, const ExtensionHostMsg_Request_Params &, std::__Cr::tuple<ExtensionHostMsg_Request_Params>> ./../../ipc/ipc_message_templates.h:76:3
    #13 0x558e24adf30b in bool IPC::MessageT<ExtensionHostMsg_Request_Meta, std::__Cr::tuple<ExtensionHostMsg_Request_Params>, void>::Dispatch<extensions::ExtensionWebContentsObserver, extensions::ExtensionWebContentsObserver, content::RenderFrameHost, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost*, ExtensionHostMsg_Request_Params const&)>(IPC::Message const*, extensions::ExtensionWebContentsObserver*, extensions::ExtensionWebContentsObserver*, content::RenderFrameHost*, void (extensions::ExtensionWebContentsObserver::*)(content::RenderFrameHost*, ExtensionHostMsg_Request_Params const&)) ./../../ipc/ipc_message_templates.h:139:7
    #14 0x558e24adf0ae in extensions::ExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) ./../../extensions/browser/extension_web_contents_observer.cc:235:5
    #15 0x558e2865c907 in extensions::ChromeExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost*) ./../../chrome/browser/extensions/chrome_extension_web_contents_observer.cc:94:37
    #16 0x7fbe3b0dcd9e in content::WebContentsImpl::OnMessageReceived(content::RenderFrameHostImpl*, IPC::Message const&) ./../../content/browser/web_contents/web_contents_impl.cc:919:18
    #17 0x7fbe3a52a0f2 in content::RenderFrameHostImpl::OnMessageReceived(IPC::Message const&) ./../../content/browser/frame_host/render_frame_host_impl.cc:1678:18
    #18 0x7fbe3ac20651 in content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) ./../../content/browser/renderer_host/render_process_host_impl.cc:3619:20
    #19 0x7fbe41b3410c in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ./../../ipc/ipc_channel_proxy.cc:327:14
    #20 0x7fbe45893e49 in Run ./../../base/callback.h:99:12
    #21 0x7fbe45893e49 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:142:33
    #22 0x7fbe458d3911 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:329:23
    #23 0x7fbe458d3278 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:254:36
    #24 0x7fbe4578ec90 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:443:48
    #25 0x7fbe458d4b69 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:443:12
    #26 0x7fbe4582bed6 in base::RunLoop::Run() ./../../base/run_loop.cc:124:14
    #27 0x558e2610b6cc in ChromeBrowserMainParts::MainMessageLoopRun(int*) ./../../chrome/browser/chrome_browser_main.cc:1676:15
    #28 0x7fbe39fabb42 in content::BrowserMainLoop::RunMainMessageLoopParts() ./../../content/browser/browser_main_loop.cc:1051:29
    #29 0x7fbe39fb25b1 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:150:15
    #30 0x7fbe39fa39ac in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser_main.cc:47:28
    #31 0x7fbe3bfc3989 in RunBrowserProcessMain ./../../content/app/content_main_runner_impl.cc:496:10
    #32 0x7fbe3bfc3989 in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) ./../../content/app/content_main_runner_impl.cc:941:10
    #33 0x7fbe3bfc2d21 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:839:12
    #34 0x7fbe45b411b5 in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:454:29
    #35 0x7fbe3bfbde16 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10

SUMMARY: AddressSanitizer: heap-use-after-free (/home/yhn/chromium/chromium-src/src/out/chrome_asan_shared/libbase.so+0x372083)
Shadow bytes around the buggy address:
  0x0c3a800d5dc0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a800d5dd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a800d5de0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a800d5df0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3a800d5e00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c3a800d5e10: fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a800d5e20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a800d5e30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a800d5e40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a800d5e50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3a800d5e60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==29939==ABORTING

Did this work before? N/A 

Chrome version: Version 85.0.4151.0(Developer Build)  Channel: n/a
OS Version: Ubuntu18.04
Flash Version:

## Attachments

- extension_poc.zip (application/octet-stream, 1.4 KB)

## Timeline

### mb...@chromium.org (2020-06-08)

rdevlin.cronin: Could you please take a look or reassign to an appropriate owner?

[Monorail components: Platform>Extensions>API]

### rd...@chromium.org (2020-06-08)

Thanks for the report!

I don't have the bandwidth to look into this one just yet - Karan, do you think you'd be able to investigate?

### [Deleted User] (2020-06-09)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-09)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-09)

[Empty comment from Monorail migration]

### ka...@chromium.org (2020-06-09)

Will TAL by EOD.

### ka...@chromium.org (2020-06-10)

Thanks for the great report. Was able to repro it. 

The only correction I'd make is that after step 3), chrome.tabs.move(var_tab_1.id,{index:2}),

the opener for tab_2 is itself (This breaks an invariant which causes the UAF subsequently). 

When tab_2 is discarded, its opener still refers to the discarded WebContents (even tab_1's opener will refer to the discarded WebContents now). 

There would be other ways to repro this as well, for example after chrome.tabs.move, we could have also done,

			chrome.tabs.remove(var_tab_2.id, () => {
				chrome.tabs.get(var_tab_1.id, () => {});
			});


### ka...@chromium.org (2020-06-10)

CL in progress: https://chromium-review.googlesource.com/c/chromium/src/+/2238557

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d9fb8cd7e3bbbd03968505cfdb0ef26f40d33cc6

commit d9fb8cd7e3bbbd03968505cfdb0ef26f40d33cc6
Author: Karandeep Bhatia <karandeepb@chromium.org>
Date: Wed Jun 10 21:45:04 2020

TabStripModel: Fix UAF by preventing openers with dangling reference.

TabStripModel::FixOpeners(index) is called to ensure that no
WebContentsData has its opener set to the WebContents at the given
|index|. It does this by setting the opener of any tabs that reference
the tab at |index| to that tab's opener. However this can cause a tab to
be its own opener (example consider two tabs which are the openers for
each other).

If such a tab (a tab which is its own opener) is removed, the same
FixOpeners logic would cause the opener of any tabs referencing it to
point to a dangling pointer. This can lead to use-after-free errors.

Fix this by ensuring that a tab can't be its own opener. Also add some
DCHECKs checking the same.

BUG=1092308
TEST=Ensure the test extension in https://crbug.com/chromium/1092308 doesn't crash under
ASAN.

Change-Id: I90d8b5342de96400dee2d502868273c6965937c0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2238557
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#777127}

[modify] https://crrev.com/d9fb8cd7e3bbbd03968505cfdb0ef26f40d33cc6/chrome/browser/ui/tabs/tab_strip_model.cc
[modify] https://crrev.com/d9fb8cd7e3bbbd03968505cfdb0ef26f40d33cc6/chrome/browser/ui/tabs/tab_strip_model.h
[modify] https://crrev.com/d9fb8cd7e3bbbd03968505cfdb0ef26f40d33cc6/chrome/browser/ui/tabs/tab_strip_model_unittest.cc


### ka...@chromium.org (2020-06-10)

Should be fixed.  mbarbella@: Do you think this warrants a merge to M84? It's relatively easy for an extension to do trigger this, though I don't think it can be triggered normally (without an extension).

### mb...@chromium.org (2020-06-11)

Once this is marked as fixed our automation will kick in and I think it would likely request a merge for this one. At a glance I certainly do think it warrants one, though.

### ka...@chromium.org (2020-06-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-12)

[Empty comment from Monorail migration]

### ka...@chromium.org (2020-06-12)

Requesting a merge to M84. This was marked as a High severity security bug in c#1.

Note that it should be now available on canary but there isn't really a way to test this on canary since it only crashes on an asan enabled build. 

Also, I think this should be safe to merge. sky@ please comment if you think otherwise (since you'll be more familiar with the immediate code).

### [Deleted User] (2020-06-12)

This bug requires manual review: M84's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sk...@chromium.org (2020-06-12)

I think this should be safe to merge, but is this really worth merging? How long have we had this bug? Maybe something changed in the extensions side to make it more likely to happen?

### ad...@google.com (2020-06-12)

karandeepb@ - do you know when this bug was introduced? Was it M85, M84, M83 or earlier? (If earlier, there's no need to be more specific!) We need to set the Security_Impact label correctly, and then (as mbarbella@ says) merge automation will kick in.

It's also important to set that correctly because the automation has currently marked this as a release blocker for M85 on the basis that it's a serious regression.

### ad...@google.com (2020-06-12)

[Empty comment from Monorail migration]

### ka...@chromium.org (2020-06-12)

> I think this should be safe to merge, but is this really worth merging? How long have we had this bug? Maybe something changed in the extensions side to make it more likely to happen?

> karandeepb@ - do you know when this bug was introduced?

I am not sure. AFAIK nothing has changed recently with the tabs api. (Devlin might be able to add more). My guess is that this has existed for a long time but wasn't discovered since it's 
   - only triggered by an extension.
   - UAF is undefined behavior so it might not have a visible effect to the user (For example, nothing happens on a non-asan enabled build)

It's a UAF that can be easily triggered by an extension. Whether this warrants a merge or not, I'll leave up to the folks from the security team (adetaylor@, mbarbella@).


### ad...@google.com (2020-06-12)

Thanks, that's helpful. I'm adjusting labels on the assumption this was present in M83 or before.

As a browser process UaF, this is a potential sandbox escape, but as it requires the user to have been persuaded to install an extension this is mitigated down to High severity. Our rules would normally merge this back to the current stable branch, but we've just missed the branch cut for the final M83 release. As such I'm going to approve merge to M84 and I think that'll be sufficient.

Approving merge to M84 branch 4147. Please have a lookout for problems on Canary before merging.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/579d29cf2bef6c630e4b2f5cf7d702b6bc1b030c

commit 579d29cf2bef6c630e4b2f5cf7d702b6bc1b030c
Author: Karandeep Bhatia <karandeepb@chromium.org>
Date: Fri Jun 12 23:58:34 2020

[Merge M84] TabStripModel: Fix UAF by preventing openers with dangling reference.

TabStripModel::FixOpeners(index) is called to ensure that no
WebContentsData has its opener set to the WebContents at the given
|index|. It does this by setting the opener of any tabs that reference
the tab at |index| to that tab's opener. However this can cause a tab to
be its own opener (example consider two tabs which are the openers for
each other).

If such a tab (a tab which is its own opener) is removed, the same
FixOpeners logic would cause the opener of any tabs referencing it to
point to a dangling pointer. This can lead to use-after-free errors.

Fix this by ensuring that a tab can't be its own opener. Also add some
DCHECKs checking the same.

BUG=1092308
TEST=Ensure the test extension in https://crbug.com/chromium/1092308 doesn't crash under
ASAN.
TBR=sky@chromium.org

(cherry picked from commit d9fb8cd7e3bbbd03968505cfdb0ef26f40d33cc6)

Change-Id: I90d8b5342de96400dee2d502868273c6965937c0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2238557
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#777127}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2243857
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#622}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/579d29cf2bef6c630e4b2f5cf7d702b6bc1b030c/chrome/browser/ui/tabs/tab_strip_model.cc
[modify] https://crrev.com/579d29cf2bef6c630e4b2f5cf7d702b6bc1b030c/chrome/browser/ui/tabs/tab_strip_model.h
[modify] https://crrev.com/579d29cf2bef6c630e4b2f5cf7d702b6bc1b030c/chrome/browser/ui/tabs/tab_strip_model_unittest.cc


### na...@google.com (2020-06-15)

[Empty comment from Monorail migration]

### ad...@google.com (2020-06-18)

It turns out there's going to be another M83 refresh, so per normal processes we should merge this. (Especially since the commit description is so obviously about UaFs, we know this commit will be getting attention from our patch-gapping adversaries, though hopefully given the requirement for an extension they won't be able to exploit it particularly rapidly -- giving this context in response to https://crbug.com/chromium/1092308#c17).

Approving merge to M83, branch 4103, assuming this continues to look good in Canary..


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/91beaf6cdd30b4ffb1f45e500c43d29b3752748d

commit 91beaf6cdd30b4ffb1f45e500c43d29b3752748d
Author: Karandeep Bhatia <karandeepb@chromium.org>
Date: Thu Jun 18 22:31:20 2020

[Merge M83] TabStripModel: Fix UAF by preventing openers with dangling reference.

TabStripModel::FixOpeners(index) is called to ensure that no
WebContentsData has its opener set to the WebContents at the given
|index|. It does this by setting the opener of any tabs that reference
the tab at |index| to that tab's opener. However this can cause a tab to
be its own opener (example consider two tabs which are the openers for
each other).

If such a tab (a tab which is its own opener) is removed, the same
FixOpeners logic would cause the opener of any tabs referencing it to
point to a dangling pointer. This can lead to use-after-free errors.

Fix this by ensuring that a tab can't be its own opener. Also add some
DCHECKs checking the same.

BUG=1092308
TEST=Ensure the test extension in https://crbug.com/chromium/1092308 doesn't crash under
ASAN.
TBR=sky@chromium.org

(cherry picked from commit d9fb8cd7e3bbbd03968505cfdb0ef26f40d33cc6)

Change-Id: I90d8b5342de96400dee2d502868273c6965937c0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2238557
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#777127}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2252939
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#712}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/91beaf6cdd30b4ffb1f45e500c43d29b3752748d/chrome/browser/ui/tabs/tab_strip_model.cc
[modify] https://crrev.com/91beaf6cdd30b4ffb1f45e500c43d29b3752748d/chrome/browser/ui/tabs/tab_strip_model.h
[modify] https://crrev.com/91beaf6cdd30b4ffb1f45e500c43d29b3752748d/chrome/browser/ui/tabs/tab_strip_model_unittest.cc


### ad...@google.com (2020-06-22)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-06-22)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-06-24)

Congrats! The Panel decided to award $20,000 for this report

### na...@google.com (2020-06-24)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-06-30)

karandeepb@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2020-07-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1092308?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052517)*
