# heap-use-after-free in MediaStreamManager::GetRawDeviceIdsOpenedForFrame

| Field | Value |
|-------|-------|
| **Issue ID** | [347373236](https://issues.chromium.org/issues/347373236) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GetUserMedia |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | br...@chromium.org |
| **Created** | 2024-06-15 |
| **Bounty** | $5,000.00 |

## Description


Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS

The GetPrimaryMainFrame[1] function will return RenderFrameHostImpl raw pointer. And it is passed as a callback parameter to GetRawDeviceIdsOpenedForFrame [0], which eventually results in  UAF at [2].




void WebContentsImpl::GetMediaCaptureRawDeviceIdsOpened(
    blink::mojom::MediaStreamType type,
    base::OnceCallback<void(std::vector<std::string>)> callback) {
  DCHECK_CURRENTLY_ON(BrowserThread::UI);
  CHECK(type == blink::mojom::MediaStreamType::DEVICE_AUDIO_CAPTURE ||
        type == blink::mojom::MediaStreamType::DEVICE_VIDEO_CAPTURE);

  MediaStreamManager* media_stream_manager =
      BrowserMainLoop::GetInstance()->media_stream_manager();
  if (!media_stream_manager) {
    std::move(callback).Run({});
    return;
  }

  GetIOThreadTaskRunner({})->PostTask(
      FROM_HERE,
      base::BindOnce(&MediaStreamManager::GetRawDeviceIdsOpenedForFrame,
                     base::Unretained(media_stream_manager),
                     GetPrimaryMainFrame(), type,                              //[0]
                     base::BindPostTaskToCurrentDefault(std::move(callback))));
}

----------------------------------------------------

RenderFrameHostImpl* WebContentsImpl::GetPrimaryMainFrame() {
  return const_cast<RenderFrameHostImpl*>(             //[1]
      std::as_const(*this).GetPrimaryMainFrame());
}

----------------------------------------------------


void MediaStreamManager::GetRawDeviceIdsOpenedForFrame(
    RenderFrameHost* render_frame_host,
    blink::mojom::MediaStreamType type,
    GetRawDeviceIdsOpenedForFrameCallback callback) const {
  DCHECK_CURRENTLY_ON(BrowserThread::IO);
  CHECK(render_frame_host);
  auto collect_all_render_frame_host_ids = base::BindOnce(
      [](RenderFrameHost* render_frame_host) {
        base::flat_set<GlobalRenderFrameHostId> all_render_frame_host_ids;
        render_frame_host->ForEachRenderFrameHost(                            //[2] UAF occur
            [&all_render_frame_host_ids](RenderFrameHost* render_frame_host) {
              all_render_frame_host_ids.insert(
                  render_frame_host->GetGlobalId());
            });
        return all_render_frame_host_ids;
      },
      render_frame_host);

  GetUIThreadTaskRunner()->PostTaskAndReplyWithResult(
      FROM_HERE, std::move(collect_all_render_frame_host_ids),
      base::BindPostTaskToCurrentDefault(
          base::BindOnce(&MediaStreamManager::GetRawDeviceIdsOpenedForFrameIds,
                         base::Unretained(this), type, std::move(callback))));
}



----------------------------------------------------






[0] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=11123

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;drc=90cac1911508d3d682a67c97aa62483eb712f69a;l=1586

[2] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/media/media_stream_manager.cc;l=2898;drc=90cac1911508d3d682a67c97aa62483eb712f69a


VERSION
Chrome Version: newest
Operating System: Macos

REPRODUCTION CASE

1.Please make sure the microphone or camera permissions are enabled
2.out/Default/Chromium.app/Contents/MacOS/Chromium http://127.0.0.1:9000/poc.html about:blank
3.Need a little interaction, click the button.


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]


=================================================================
==21851==ERROR: AddressSanitizer: heap-use-after-free on address 0x622000354100 at pc 0x00010f635a40 bp 0x00016ee74fd0 sp 0x00016ee74fc8
READ of size 8 at 0x622000354100 thread T0
==21851==WARNING: invalid path to external symbolizer!
==21851==WARNING: Failed to use and restart external symbolizer!
    #0 0x10f635a3c in base::internal::Invoker<base::internal::FunctorTraits<content::MediaStreamManager::GetRawDeviceIdsOpenedForFrame(content::RenderFrameHost*, blink::mojom::MediaStreamType, base::OnceCallback<void (std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>)>) const::$_0&&, content::RenderFrameHost*&&>, base::internal::BindState<false, false, false, content::MediaStreamManager::GetRawDeviceIdsOpenedForFrame(content::RenderFrameHost*, blink::mojom::MediaStreamType, base::OnceCallback<void (std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>)>) const::$_0, base::internal::UnretainedWrapper<content::RenderFrameHost, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>> ()>::RunOnce(base::internal::BindStateBase*)+0x254 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1b05a3c)
    #1 0x10f647cb0 in void base::internal::ReturnAsParamAdapter<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>>>(base::OnceCallback<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>> ()>, std::__Cr::unique_ptr<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>>, std::__Cr::default_delete<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>>>>*)+0x160 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1b17cb0)
    #2 0x10f6483e4 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(base::OnceCallback<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>> ()>, std::__Cr::unique_ptr<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>>, std::__Cr::default_delete<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>>>>*), base::OnceCallback<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>> ()>&&, std::__Cr::unique_ptr<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>>, std::__Cr::default_delete<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>>>>*&&>, base::internal::BindState<false, true, false, void (*)(base::OnceCallback<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>> ()>, std::__Cr::unique_ptr<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>>, std::__Cr::default_delete<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>>>>*), base::OnceCallback<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>> ()>, base::internal::UnretainedWrapper<std::__Cr::unique_ptr<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>>, std::__Cr::default_delete<base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>>>>, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x19c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1b183e4)
    #3 0x1037204a4 in base::internal::PostTaskAndReplyRelay::RunTaskAndPostReply(base::internal::PostTaskAndReplyRelay)+0x160 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x20c4a4)
    #4 0x103720854 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay&&>, base::internal::BindState<false, true, false, void (*)(base::internal::PostTaskAndReplyRelay), base::internal::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase*)+0x110 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x20c854)
    #5 0x1036a1a94 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x18da94)
    #6 0x10370abbc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f8 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f6bbc)
    #7 0x10370a028 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f6028)
    #8 0x1038540e4 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c4 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x3400e4)
    #9 0x1038427f0 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x32e7f0)
    #10 0x103852688 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x33e688)
    #11 0x1918ba4d4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7e4d4)
    #12 0x90610001918ba468  (<unknown module>)
    #13 0x644d0001918ba1d8  (<unknown module>)
    #14 0xc1608001918b8dc4  (<unknown module>)
    #15 0x18508001918b8430  (<unknown module>)
    #16 0x753c80019c05c198  (<unknown module>)
    #17 0x655b00019c05be28  (<unknown module>)
    #18 0xe46400019c05bd2c  (<unknown module>)
    #19 0x801f800195117d64  (<unknown module>)
    #20 0x6a2500019590d804  (<unknown module>)
    #21 0x810600011b4b0b24  (<unknown module>)
    #22 0x1038427f0 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x32e7f0)
    #23 0x11b4b07e8 in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x1a4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2d807e8)
    #24 0x19510b098 in -[NSApplication run]+0x1d8 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64+0x2d098)
    #25 0x1e0e000103856000  (<unknown module>)
    #26 0x1038512a4 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x28c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x33d2a4)
    #27 0x10370c16c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f816c)
    #28 0x1036354d0 in base::RunLoop::Run(base::Location const&)+0x438 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1214d0)
    #29 0x10e8a3df0 in content::BrowserMainLoop::RunMainMessageLoop()+0x178 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0xd73df0)
    #30 0x10e8aa0f4 in content::BrowserMainRunnerImpl::Run()+0x30 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0xd7a0f4)
    #31 0x10e89c80c in content::BrowserMain(content::MainFunctionParams)+0x1f8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0xd6c80c)
    #32 0x110c663b0 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*)+0x1ac (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x31363b0)
    #33 0x110c68fb0 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x8dc (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x3138fb0)
    #34 0x110c684ac in content::ContentMainRunnerImpl::Run()+0x490 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x31384ac)
    #35 0x110c6468c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x670 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x313468c)
    #36 0x110c64f44 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x3134f44)
    #37 0x11873aeac in ChromeMain+0x338 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0xaeac)
    #38 0x100f88b80 in main+0x1f8 (/Users/test/chromium/src/out/Default/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000b80)
    #39 0x1914520dc  (<unknown module>)
    #40 0xa85efffffffffffc  (<unknown module>)

0x622000354100 is located 0 bytes inside of 5328-byte region [0x622000354100,0x6220003555d0)
freed by thread T0 here:
    #0 0x101b48524 in __sanitizer_finish_switch_fiber+0xa24 (/Users/test/chromium/src/out/Default/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x60524)
    #1 0x10f8d3270 in content::RenderFrameHostManager::~RenderFrameHostManager()+0xa8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1da3270)
    #2 0x10f564708 in content::FrameTreeNode::~FrameTreeNode()+0xd14 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1a34708)
    #3 0x10f5549d8 in content::FrameTree::~FrameTree()+0x54 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1a249d8)
    #4 0x10fe82830 in content::WebContentsImpl::~WebContentsImpl()+0x1508 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x2352830)
    #5 0x10fe84fe0 in content::WebContentsImpl::~WebContentsImpl()+0x8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x2354fe0)
    #6 0x11fbbdd38 in tabs::TabModel::~TabModel()+0x1bc (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x748dd38)
    #7 0x11fbd40b8 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*)+0x5ac (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x74a40b8)
    #8 0x11fbddffc in TabStripModel::CloseTabs(base::span<content::WebContents* const, 18446744073709551615ul, content::WebContents* const*>, unsigned int)+0xb90 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x74adffc)
    #9 0x11fbdd188 in TabStripModel::CloseAllTabs()+0x368 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x74ad188)
    #10 0x120549f74 in BrowserView::OnWindowCloseRequested()+0x128 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x7e19f74)
    #11 0x13a965048 in views::Widget::CloseWithReason(views::Widget::ClosedReason)+0x190 (/Users/test/chromium/src/out/Default/libui_views.dylib:arm64+0x3b1048)
    #12 0x11bdfde2c in BrowserCloseManager::CloseBrowsers()+0x220 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x36cde2c)
    #13 0x11bdfe32c in BrowserCloseManager::TryToCloseBrowsers()+0x228 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x36ce32c)
    #14 0x11bdfbc20 in chrome::CloseAllBrowsers()+0x104 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x36cbc20)
    #15 0x11b496b4c in -[AppController tryToTerminateApplication:]+0xf4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2d66b4c)
    #16 0x11b4b05e0 in -[BrowserCrApplication terminate:]+0x3c (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2d805e0)
    #17 0x11c184ebc in (anonymous namespace)::ExitHandler::ExitWhenPossibleOnUIThread(int)+0x1d4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x3a54ebc)
    #18 0x11c1851c4 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(int)>, base::internal::BindState<false, true, false, void (*)(int)>, void (int)>::RunOnce(base::internal::BindStateBase*, int)+0xe0 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x3a551c4)
    #19 0x11ae1e588 in base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (int)>&&, int&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (int)>, int>, void ()>::RunOnce(base::internal::BindStateBase*)+0x188 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x26ee588)
    #20 0x1036a1a94 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x18da94)
    #21 0x10370abbc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f8 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f6bbc)
    #22 0x10370a028 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f6028)
    #23 0x1038540e4 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c4 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x3400e4)
    #24 0x1038427f0 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x32e7f0)
    #25 0x103852688 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x33e688)
    #26 0x1918ba4d4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7e4d4)
    #27 0x90610001918ba468  (<unknown module>)
    #28 0x644d0001918ba1d8  (<unknown module>)
    #29 0xc1608001918b8dc4  (<unknown module>)

previously allocated by thread T0 here:
    #0 0x101b4811c in __sanitizer_finish_switch_fiber+0x61c (/Users/test/chromium/src/out/Default/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x6011c)
    #1 0x10f7e37b4 in content::RenderFrameHostFactory::Create(content::SiteInstance*, scoped_refptr<content::RenderViewHostImpl>, content::RenderFrameHostDelegate*, content::FrameTree*, content::FrameTreeNode*, int, mojo::PendingAssociatedRemote<content::mojom::Frame>, base::TokenType<blink::LocalFrameTokenTypeMarker> const&, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken, bool, content::RenderFrameHostImpl::LifecycleStateImpl, scoped_refptr<content::BrowsingContextState>)+0x270 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1cb37b4)
    #2 0x10f8d5134 in content::RenderFrameHostManager::CreateRenderFrameHost(content::RenderFrameHostManager::CreateFrameCase, content::SiteInstanceImpl*, int, mojo::PendingAssociatedRemote<content::mojom::Frame>, base::TokenType<blink::LocalFrameTokenTypeMarker> const&, base::TokenType<blink::DocumentTokenTypeMarker> const&, base::UnguessableToken, bool, scoped_refptr<content::BrowsingContextState>)+0x830 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1da5134)
    #3 0x10f8d431c in content::RenderFrameHostManager::InitRoot(content::SiteInstanceImpl*, bool, blink::FramePolicy, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::UnguessableToken const&)+0x648 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1da431c)
    #4 0x10f55bb7c in content::FrameTree::Init(content::SiteInstanceImpl*, bool, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::RenderFrameHostImpl*, blink::FramePolicy const&, base::UnguessableToken const&)+0x128 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1a2bb7c)
    #5 0x10f40cbcc in content::PrerenderHost::PrerenderHost(content::PrerenderAttributes const&, content::WebContentsImpl&, base::WeakPtr<content::PreloadingAttempt>, std::__Cr::unique_ptr<content::DevToolsPrerenderAttempt, std::__Cr::default_delete<content::DevToolsPrerenderAttempt>>)+0x6e8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x18dcbcc)
    #6 0x10f428424 in content::(anonymous namespace)::PrerenderHostBuilder::Build(content::PrerenderAttributes const&, content::WebContentsImpl&)+0x218 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x18f8424)
    #7 0x10f4257ec in content::PrerenderHostRegistry::CreateAndStartHost(content::PrerenderAttributes const&, content::PreloadingAttempt*)+0xb78 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x18f57ec)
    #8 0x10ff2c8e8 in content::WebContentsImpl::StartPrerendering(GURL const&, content::PreloadingTriggerType, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, ui::PageTransition, content::PreloadingHoldbackStatus, content::PreloadingAttempt*, base::RepeatingCallback<bool (GURL const&)>, base::RepeatingCallback<void (content::NavigationHandle&)>)+0x344 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x23fc8e8)
    #9 0x11b9c44f4 in PrerenderManager::StartPrerenderDirectUrlInput(GURL const&, content::PreloadingAttempt&)+0x35c (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x32944f4)
    #10 0x11b9d26b4 in predictors::AutocompleteActionPredictor::StartPrerendering(GURL const&, content::WebContents&, gfx::Size const&)+0x300 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x32a26b4)
    #11 0x12062e614 in ChromeOmniboxClient::DoPrerender(AutocompleteMatch const&)+0x1a4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x7efe614)
    #12 0x12062e30c in ChromeOmniboxClient::OnTextChanged(AutocompleteMatch const&, bool, std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t>> const&, AutocompleteResult const&, bool)+0x274 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x7efe30c)
    #13 0x11f8a85c0 in OmniboxEditModel::OnChanged()+0x228 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x71785c0)
    #14 0x11f8b7ab0 in OmniboxEditModel::OnPopupDataChanged(std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t>> const&, bool, std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t>> const&, std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t>> const&, std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t>> const&, bool, std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t>> const&, AutocompleteMatch const&)+0xc94 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x7187ab0)
    #15 0x11f8b9c58 in OmniboxEditModel::OnCurrentMatchChanged()+0x3dc (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x7189c58)
    #16 0x11f8a37b4 in OmniboxController::OnResultChanged(AutocompleteController*, bool)+0x208 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x71737b4)
    #17 0x11e74982c in AutocompleteController::NotifyChanged()+0x5f4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x601982c)
    #18 0x11e74d3d8 in base::internal::Invoker<base::internal::FunctorTraits<void (AutocompleteController::*&&)(), AutocompleteController*>, base::internal::BindState<true, true, false, void (AutocompleteController::*)(), base::internal::UnretainedWrapper<AutocompleteController, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x601d3d8)
    #19 0x11e78ba90 in AutocompleteProviderDebouncer::Run()+0x154 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x605ba90)
    #20 0x11e78bd88 in base::internal::Invoker<base::internal::FunctorTraits<void (AutocompleteProviderDebouncer::*&&)(), AutocompleteProviderDebouncer*>, base::internal::BindState<true, true, false, void (AutocompleteProviderDebouncer::*)(), base::internal::UnretainedWrapper<AutocompleteProviderDebouncer, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x184 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x605bd88)
    #21 0x1037ad058 in base::OneShotTimer::RunUserTask()+0x1a0 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x299058)
    #22 0x11e73d4b0 in AutocompleteController::RequestNotifyChanged(bool, bool)+0x1ac (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x600d4b0)
    #23 0x11e73cad4 in AutocompleteController::UpdateResult(AutocompleteController::UpdateType)+0x674 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x600cad4)
    #24 0x11e73b924 in AutocompleteController::Start(AutocompleteInput const&)+0xbcc (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x600b924)
    #25 0x11f8a2814 in OmniboxController::StartAutocomplete(AutocompleteInput const&) const+0x168 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x7172814)
    #26 0x11f8ab640 in OmniboxEditModel::StartAutocomplete(bool, bool)+0x85c (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x717b640)
    #27 0x11f8a9ed4 in OmniboxEditModel::UpdateInput(bool, bool)+0x1e0 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x7179ed4)
    #28 0x11f8b87b8 in OmniboxEditModel::OnAfterPossibleChange(OmniboxView::StateChanges const&, bool)+0x6d8 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x71887b8)
    #29 0x1206e6e34 in OmniboxViewViews::OnAfterPossibleChange(bool)+0x180 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x7fb6e34)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1b05a3c) in base::internal::Invoker<base::internal::FunctorTraits<content::MediaStreamManager::GetRawDeviceIdsOpenedForFrame(content::RenderFrameHost*, blink::mojom::MediaStreamType, base::OnceCallback<void (std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>)>) const::$_0&&, content::RenderFrameHost*&&>, base::internal::BindState<false, false, false, content::MediaStreamManager::GetRawDeviceIdsOpenedForFrame(content::RenderFrameHost*, blink::mojom::MediaStreamType, base::OnceCallback<void (std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>)>) const::$_0, base::internal::UnretainedWrapper<content::RenderFrameHost, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, base::internal::flat_tree<content::GlobalRenderFrameHostId, std::__Cr::identity, std::__Cr::less<void>, std::__Cr::vector<content::GlobalRenderFrameHostId, std::__Cr::allocator<content::GlobalRenderFrameHostId>>> ()>::RunOnce(base::internal::BindStateBase*)+0x254
Shadow bytes around the buggy address:
  0x622000353e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x622000353f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x622000353f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x622000354000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x622000354080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x622000354100:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x622000354180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x622000354200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x622000354280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x622000354300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x622000354380: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==21851==ADDITIONAL INFO

==21851==Note: Please include this section with the ASan report.
Task trace:
    #0 0x10f622fe8 in content::MediaStreamManager::GetRawDeviceIdsOpenedForFrame(content::RenderFrameHost*, blink::mojom::MediaStreamType, base::OnceCallback<void (std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>)>) const+0x2d8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1af2fe8)
    #1 0x10ff2dc10 in content::WebContentsImpl::GetMediaCaptureRawDeviceIdsOpened(blink::mojom::MediaStreamType, base::OnceCallback<void (std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>)>)+0x22c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x23fdc10)




CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: anonymous




I made a small change to the code to make it easier to trigger the vulnerability.

patch.diff
@@ -11116,6 +11039,9 @@ void WebContentsImpl::GetMediaCaptureRawDeviceIdsOpene
     return;
   }
 
+  LOG(ERROR)<<"GetRawDeviceIdsOpenedForFrame----------";
+  sleep(5);
+
   GetIOThreadTaskRunner({})->PostTask(
       FROM_HERE,
       base::BindOnce(&MediaStreamManager::GetRawDeviceIdsOpenedForFrame,
@@ -11125,3 +11051,4 @@ void WebContentsImpl::GetMediaCaptureRawDeviceIdsOpene






Fix 

use WeakPtr or don't use pointer



commit  introduce

https://chromium-review.googlesource.com/c/chromium/src/+/4976193









## Attachments

- [poc.html](attachments/poc.html) (text/html, 107 B)
- [poc.mov](attachments/poc.mov) (video/quicktime, 31.0 MB)

## Timeline

### ha...@gmail.com (2024-06-15)

Although this vulnerability requires a little interaction, it seems to be exploitable and can be used to escape the sandbox.I recorded a video, I hope it can help you, but I need to delete it later because it involves my information.

### [Deleted User] (2024-06-17)

I was unable to reproduce this bug on linux with the patch applied on an asan build. Here are the reproduction steps that I used:

1. run a web server to serve poc.html (e.g. python3 -m http.server)
2. load that page in the asan build with the sleep patched in
3. open site settings for that page (e.g. localhost:8000) and enable camera and microphone
4. reload the page (or restart chrome)
5. open the page info (tune icon to the left of the URL), and click on the right-pointing arrow next to camera or microphone

### ha...@gmail.com (2024-06-18)

You can follow my steps.It's easy to reproduce.

### pe...@google.com (2024-06-18)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-06-18)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-06-24)

Project: chromium/src
Branch: main

commit 1b90408171198d05295a02b4c5ffdbe011f13636
Author: Bryant Chandler <bryantchandler@chromium.org>
Date:   Mon Jun 24 17:28:53 2024

    [media_preview] Fix pointer tear down order problem
    
    Holding a RenderFrameHost* in the `OnceBinding` isn't safe,
    because the `RenderFrameHost` can be destroyed before the
    binding. This CL changes the task strategy so that the
    RenderFrameHost* doesn't need to be bound in a callback.
    
    Tested using the repro steps in the bug and this change stops
    it from reproducing.
    
    Fixed: 347373236
    Change-Id: Id639f317b0f37a508833aba9fe52ffc5c0ed590c
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5640501
    Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
    Commit-Queue: Bryant Chandler <bryantchandler@chromium.org>
    Reviewed-by: Guido Urdaneta <guidou@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1318653}

M       content/browser/renderer_host/media/media_stream_manager.cc
M       content/browser/web_contents/web_contents_impl.cc

https://chromium-review.googlesource.com/5640501


### br...@chromium.org (2024-06-24)

Does this need to be merged back to M126 and M127?

### pe...@google.com (2024-06-25)

Requesting merge to stable (M126) because latest trunk commit (1318653) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1318653) appears to be after beta branch point (1313161).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### pe...@google.com (2024-06-25)

Merge review required: M127 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-06-25)

Merge review required: M126 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), srinivassista (Desktop)

### br...@chromium.org (2024-06-25)

1. <https://chromium-review.googlesource.com/5640501>
2. Verified stable on Canary
3. I don't think so
4. No compatibility risk
5. No manual verification needed.

### am...@chromium.org (2024-06-25)

Since this fix just landed ~ 24 hours ago, I'll revisit it tomorrow once it has had a bit more bake time on Canary 

### am...@chromium.org (2024-07-01)

https://crrev.com/c/5640501 approved for merge to M126 Stable and M127 Beta; please merge this fix to M127 / branch 6533 and M126 / branch 6478 at your earliest convenience and by NLT EOD Thursday, 11 July so this fix can be included in the M126 Stable respin following release freeze and the M127 Stable RC occurring directly after the current release freeze



### am...@chromium.org (2024-07-01)

guidou@chromium.org -- can you please take care of the merge as bryandtchandler@ is currently OOO? 

### sp...@google.com (2024-07-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
$4,000 for report of moderately mitigated memory corruption in a non-sandboxed process + $1,000 bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-03)

Congratulations on another one! Thank you for your efforts and reporting this issue to us.

### ha...@gmail.com (2024-07-03)

Hi VRP,

[Issue 347373236](https://issues.chromium.org/issues/347373236) is a render\_frame\_host vulnerability with a little interaction, similar to <https://issues.chromium.org/issues/325936438>. I don't know why my vulnerability was judged as Moderately Mitigated. I think it should be Mildly Mitigated. I hope you can re-judge it.

### am...@chromium.org (2024-07-04)

Hi, thank you for reaching out. This issue was judged as moderately mitigated based on the permission to give the website access to microphone and/or camera permissions, the user interaction in the web content, race condition and page tear down to trigger. The combinations of these preconditions result in the rating of this issue being rated as moderately mitigated and resulting in a $4,000 reward for the report of the issue. There were a slightly less amount of mitigation in the issue you linked which resulted in slightly higher reward and a rating of the low end of mildly mitigated for that report.

### pe...@google.com (2024-07-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### da...@google.com (2024-07-08)

Please land your merges before COP Tuesday to ensure it is included in this weeks Beta release.

For gitwatcher to update your merge request to Merge-Merged you will need to **include the bug id in the commit message**.


### ap...@google.com (2024-07-08)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 947a80df8e81e15f7858f901406ebd50f0091b95
Author: Bryant Chandler <bryantchandler@chromium.org>
Date:   Mon Jul 08 18:01:06 2024

    [M126][media_preview] Fix pointer tear down order problem
    
    Holding a RenderFrameHost* in the `OnceBinding` isn't safe,
    because the `RenderFrameHost` can be destroyed before the
    binding. This CL changes the task strategy so that the
    RenderFrameHost* doesn't need to be bound in a callback.
    
    Tested using the repro steps in the bug and this change stops
    it from reproducing.
    
    (cherry picked from commit 1b90408171198d05295a02b4c5ffdbe011f13636)
    
    Fixed: 347373236
    Change-Id: Id639f317b0f37a508833aba9fe52ffc5c0ed590c
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5640501
    Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
    Commit-Queue: Bryant Chandler <bryantchandler@chromium.org>
    Reviewed-by: Guido Urdaneta <guidou@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1318653}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5683923
    Cr-Commit-Position: refs/branch-heads/6478@{#1723}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       content/browser/renderer_host/media/media_stream_manager.cc
M       content/browser/web_contents/web_contents_impl.cc

https://chromium-review.googlesource.com/5683923


### ap...@google.com (2024-07-08)

Project: chromium/src
Branch: refs/branch-heads/6533

commit f940ca04ed55df9ce454873a50d6535a59333b49
Author: Bryant Chandler <bryantchandler@chromium.org>
Date:   Mon Jul 08 18:20:32 2024

    [M127][media_preview] Fix pointer tear down order problem
    
    Holding a RenderFrameHost* in the `OnceBinding` isn't safe,
    because the `RenderFrameHost` can be destroyed before the
    binding. This CL changes the task strategy so that the
    RenderFrameHost* doesn't need to be bound in a callback.
    
    Tested using the repro steps in the bug and this change stops
    it from reproducing.
    
    (cherry picked from commit 1b90408171198d05295a02b4c5ffdbe011f13636)
    
    Fixed: 347373236
    Change-Id: Id639f317b0f37a508833aba9fe52ffc5c0ed590c
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5640501
    Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
    Commit-Queue: Bryant Chandler <bryantchandler@chromium.org>
    Reviewed-by: Guido Urdaneta <guidou@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1318653}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5683882
    Cr-Commit-Position: refs/branch-heads/6533@{#1165}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       content/browser/renderer_host/media/media_stream_manager.cc
M       content/browser/web_contents/web_contents_impl.cc

https://chromium-review.googlesource.com/5683882


### rz...@google.com (2024-07-29)

Labelling as not applicable for LTS-120 because the changed code isn't present in the branch.

### pe...@google.com (2024-10-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/347373236)*
