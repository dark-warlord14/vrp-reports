# Security: Container-overflow in SavedTabGroupModel::RemoveTabFromGroup

| Field | Value |
|-------|-------|
| **Issue ID** | [40062298](https://issues.chromium.org/issues/40062298) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2022-12-17 |
| **Bounty** | $2,000.00 |

## Description

Chrome Version: 110.0.5481.3 (Official Build) canary (64-bit) (cohort: Clang-64)  

Operating System: Window and Linux

**REPRODUCTION CASE**

1. Open crash.html >> Add the tab to new group >> Save group
2. Now click on the button and wait

==33045==ERROR: AddressSanitizer: container-overflow on address 0x615000507e97 at pc 0x5636da7c6e52 bp 0x7fff2d02e3b0 sp 0x7fff2d02e3a8  

READ of size 1 at 0x615000507e97 thread T0 (chrome)  

==33045==WARNING: invalid path to external symbolizer!  

==33045==WARNING: Failed to use and restart external symbolizer!  

#0 0x5636da7c6e51 in \_\_is\_long ./../../buildtools/third\_party/libc++/trunk/include/string:1682:33  

#1 0x5636da7c6e51 in basic\_string ./../../buildtools/third\_party/libc++/trunk/include/string:2147:16  

#2 0x5636da7c6e51 in base::GUID::GUID(base::GUID const&) ./../../base/guid.cc:162:7  

#3 0x5636d91eb489 in optional\_data\_dtor\_base<const base::GUID &> ./../../third\_party/abseil-cpp/absl/types/internal/optional.h:112:25  

#4 0x5636d91eb489 in optional\_data\_dtor\_base ./../../third\_party/abseil-cpp/absl/types/internal/optional.h:149:15  

#5 0x5636d91eb489 in optional\_data\_dtor\_base ./../../third\_party/abseil-cpp/absl/types/internal/optional.h:206:32  

#6 0x5636d91eb489 in optional<const base::GUID &, false> ./../../third\_party/abseil-cpp/absl/types/optional.h:178:31  

#7 0x5636d91eb489 in SavedTabGroupModel::RemoveTabFromGroup(base::GUID const&, base::GUID const&) ./../../components/saved\_tab\_groups/saved\_tab\_group\_model.cc:256:52  

#8 0x5636ec8d6c0a in SavedTabGroupBrowserListener::TabGroupedStateChanged(absl::optional<tab\_groups::TabGroupId>, content::WebContents\*, int) ./../../chrome/browser/ui/tabs/saved\_tab\_groups/saved\_tab\_group\_model\_listener.cc:82:13  

#9 0x5636ec8e689e in TabStripModel::UngroupTab(int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:2336:14  

#10 0x5636ec8e4290 in TabStripModel::DetachWebContentsImpl(int, int, bool, TabStripModelChange::RemoveReason) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:447:3  

#11 0x5636ec8fcac2 in TabStripModel::CloseWebContentses(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int, TabStripModel::DetachNotifications\*) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:1922:16  

#12 0x5636ec8eafa0 in TabStripModel::CloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:1841:7  

#13 0x5636ec8eb951 in TabStripModel::CloseWebContentsAt(int, unsigned int) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:703:10  

#14 0x5636ec82a6f2 in chrome::CloseWebContents(Browser\*, content::WebContents\*, bool) ./../../chrome/browser/ui/browser\_tabstrip.cc:99:31  

#15 0x5636ceb93732 in Run ./../../base/functional/callback.h:152:12  

#16 0x5636ceb93732 in blink::mojom::LocalMainFrame\_ClosePage\_ForwardToCallback::Accept(mojo::Message\*) ./gen/third\_party/blink/public/mojom/frame/frame.mojom.cc:16521:26  

#17 0x5636dcc25fc9 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:1002:41  

#18 0x5636dcc3aa00 in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#19 0x5636dcc29633 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:694:20  

#20 0x5636ddd7883d in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc\_mojo\_bootstrap.cc:1076:24  

#21 0x5636ddd71ce5 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/functional/bind\_internal.h:700:12  

#22 0x5636ddd71ce5 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> > ./../../base/functional/bind\_internal.h:879:12  

#23 0x5636ddd71ce5 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/functional/bind\_internal.h:973:12  

#24 0x5636ddd71ce5 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:924:12  

#25 0x5636da900c5c in Run ./../../base/functional/callback.h:152:12  

#26 0x5636da900c5c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:157:32  

#27 0x5636da947dfe in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:11)> ./../../base/task/common/task\_annotator.h:85:5  

#28 0x5636da947dfe in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:484:23  

#29 0x5636da946e9d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:335:30  

#30 0x5636da9490b4 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#31 0x5636daa60f94 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:292:55  

#32 0x5636da949b5a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:644:12  

#33 0x5636da88a655 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:140:14  

#34 0x5636d3323ee2 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1054:18  

#35 0x5636d3328c08 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:162:15  

#36 0x5636d331e7e3 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:32:28  

#37 0x5636da667e40 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:704:10  

#38 0x5636da66a186 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1242:10  

#39 0x5636da669bb9 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1098:12  

#40 0x5636da6639d1 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:344:36  

#41 0x5636da664969 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:372:10  

#42 0x5636cae5a726 in ChromeMain ./../../chrome/app/chrome\_main.cc:174:12  

#43 0x7efc655450b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x615000507e97 is located 279 bytes inside of 512-byte region [0x615000507d80,0x615000507f80)  

allocated by thread T0 (chrome) here:  

#0 0x5636cae57f5d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x5636d91e73cd in \_\_libcpp\_operator\_new<unsigned long> ./../../buildtools/third\_party/libc++/trunk/include/new:264:10  

#2 0x5636d91e73cd in \_\_libcpp\_allocate ./../../buildtools/third\_party/libc++/trunk/include/new:290:10  

#3 0x5636d91e73cd in allocate ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator.h:112:38  

#4 0x5636d91e73cd in std::Cr::\_\_allocation\_result<std::Cr::allocator\_traits<std::Cr::allocator<SavedTabGroupTab> >::pointer> std::Cr::\_\_allocate\_at\_least[abi:v160000]<std::Cr::allocator<SavedTabGroupTab> >(std::Cr::allocator<SavedTabGroupTab>&, unsigned long) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocate\_at\_least.h:54:19  

#5 0x5636d91e57d2 in \_\_split\_buffer ./../../buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:323:29  

#6 0x5636d91e57d2 in std::Cr::\_\_wrap\_iter<SavedTabGroupTab\*> std::Cr::vector<SavedTabGroupTab, std::Cr::allocator<SavedTabGroupTab> >::emplace<SavedTabGroupTab>(std::Cr::\_\_wrap\_iter<SavedTabGroupTab const\*>, SavedTabGroupTab&&) ./../../buildtools/third\_party/libc++/trunk/include/vector:1757:53  

#7 0x5636d91e53c1 in SavedTabGroup::AddTab(unsigned long, SavedTabGroupTab) ./../../components/saved\_tab\_groups/saved\_tab\_group.cc:129:15  

#8 0x5636d91eace5 in SavedTabGroupModel::AddTabToGroup(base::GUID const&, SavedTabGroupTab, int) ./../../components/saved\_tab\_groups/saved\_tab\_group\_model.cc:231:42  

#9 0x5636ec8d6f06 in SavedTabGroupBrowserListener::TabGroupedStateChanged(absl::optional<tab\_groups::TabGroupId>, content::WebContents\*, int) ./../../chrome/browser/ui/tabs/saved\_tab\_groups/saved\_tab\_group\_model\_listener.cc:118:11  

#10 0x5636ec8f3752 in TabStripModel::GroupTab(int, tab\_groups::TabGroupId const&) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:2364:14  

#11 0x5636ec8e27a9 in TabStripModel::InsertWebContentsAtImpl(int, std::Cr::unique\_ptr<content::WebContents, std::Cr::default\_delete[content::WebContents](javascript:void(0);) >, int, absl::optional<tab\_groups::TabGroupId>) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:1821:5  

#12 0x5636ec8ef312 in TabStripModel::AddWebContents(std::Cr::unique\_ptr<content::WebContents, std::Cr::default\_delete[content::WebContents](javascript:void(0);) >, int, ui::PageTransition, int, absl::optional<tab\_groups::TabGroupId>) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:974:3  

#13 0x5636ec820b0c in Navigate(NavigateParams\*) ./../../chrome/browser/ui/browser\_navigator.cc:824:41  

#14 0x5636ec82a1be in chrome::AddWebContents(Browser\*, content::WebContents\*, std::Cr::unique\_ptr<content::WebContents, std::Cr::default\_delete[content::WebContents](javascript:void(0);) >, GURL const&, WindowOpenDisposition, blink::mojom::WindowFeatures const&, NavigateParams::WindowAction) ./../../chrome/browser/ui/browser\_tabstrip.cc:87:3  

#15 0x5636ec7dd451 in Browser::AddNewContents(content::WebContents\*, std::Cr::unique\_ptr<content::WebContents, std::Cr::default\_delete[content::WebContents](javascript:void(0);) >, GURL const&, WindowOpenDisposition, blink::mojom::WindowFeatures const&, bool, bool\*) ./../../chrome/browser/ui/browser.cc:1687:3  

#16 0x5636ec7dd4bb in non-virtual thunk to Browser::AddNewContents(content::WebContents\*, std::Cr::unique\_ptr<content::WebContents, std::Cr::default\_delete[content::WebContents](javascript:void(0);) >, GURL const&, WindowOpenDisposition, blink::mojom::WindowFeatures const&, bool, bool\*) ./../../chrome/browser/ui/browser.cc:0:0  

#17 0x5636d44912da in content::WebContentsImpl::ShowCreatedWindow(content::RenderFrameHostImpl\*, int, WindowOpenDisposition, blink::mojom::WindowFeatures const&, bool) ./../../content/browser/web\_contents/web\_contents\_impl.cc:4342:15  

#18 0x5636d3fe7055 in content::RenderFrameHostImpl::ShowCreatedWindow(base::TokenType[blink::LocalFrameTokenTypeMarker](javascript:void(0);) const&, WindowOpenDisposition, mojo::StructPtr[blink::mojom::WindowFeatures](javascript:void(0);), bool, base::OnceCallback<void ()>) ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:5359:34  

#19 0x5636ceb98ca3 in blink::mojom::LocalMainFrameHostStubDispatch::AcceptWithResponder(blink::mojom::LocalMainFrameHost\*, mojo::Message\*, std::Cr::unique\_ptr<mojo::MessageReceiverWithStatus, std::Cr::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) ./gen/third\_party/blink/public/mojom/frame/frame.mojom.cc:18586:13  

#20 0x5636dcc25cd3 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:961:56  

#21 0x5636dcc3a91b in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:48:24  

#22 0x5636dcc29633 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:694:20  

#23 0x5636ddd7883d in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ./../../ipc/ipc\_mojo\_bootstrap.cc:1076:24  

#24 0x5636ddd71ce5 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/functional/bind\_internal.h:700:12  

#25 0x5636ddd71ce5 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> > ./../../base/functional/bind\_internal.h:879:12  

#26 0x5636ddd71ce5 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> ./../../base/functional/bind\_internal.h:973:12  

#27 0x5636ddd71ce5 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:924:12  

#28 0x5636da900c5c in Run ./../../base/functional/callback.h:152:12  

#29 0x5636da900c5c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:157:32  

#30 0x5636da947dfe in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:11)> ./../../base/task/common/task\_annotator.h:85:5  

#31 0x5636da947dfe in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:484:23  

#32 0x5636da946e9d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:335:30  

#33 0x5636da9490b4 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#34 0x5636daa60f94 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:292:55  

#35 0x5636da949b5a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:644:12  

#36 0x5636da88a655 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:140:14  

#37 0x5636d3323ee2 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1054:18  

#38 0x5636d3328c08 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:162:15

HINT: if you don't care about these errors you may set ASAN\_OPTIONS=detect\_container\_overflow=0.  

If you suspect a false positive see also: <https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow>.  

SUMMARY: AddressSanitizer: container-overflow (/home/lbstyle/Desktop/asan-linux-release-1083982/chrome+0x1fe57e51) (BuildId: bf5cba1f5414ef04)  

Shadow bytes around the buggy address:  

0x615000507c00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x615000507c80: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x615000507d00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x615000507d80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x615000507e00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x615000507e80: fc fc[fc]fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x615000507f00: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x615000507f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x615000508000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x615000508080: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x615000508100: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==33045==ABORTING

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 289 B)
- [Video_2022_12_17-2.webm](attachments/Video_2022_12_17-2.webm) (video/webm, 2.5 MB)
- [asan.log](attachments/asan.log) (text/plain, 19.2 KB)
- [Screenshot 2022-12-19 3.24.04 PM.png](attachments/Screenshot 2022-12-19 3.24.04 PM.png) (image/png, 85.9 KB)

## Timeline

### [Deleted User] (2022-12-17)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-12-17)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-12-17)

Please enable #tab-groups-save flag.

### aj...@google.com (2022-12-17)

Note that closing a window is not normally possible from web contents, but an extension could probably script this.

UI mediated browser uaf -> Medium 

dljames - is this enabled for any users yet (e.g. via Finch?)

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### [Deleted User] (2022-12-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-17)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-17)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dl...@google.com (2022-12-17)

ajgo - This is not enabled for any users yet, unless the respective feature flag is manually turned on. 

I believe this was caused by the recent web contents changes that were made to allow the updating of the tabs in the saved groups. I will look into this on 12/19 and update as I get more information. 

Thank you!

### aj...@google.com (2022-12-17)

Thanks- adding Impact=None as this is not enabled anywhere.

### aj...@google.com (2022-12-17)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-17)

(auto-cc on security bug)

### [Deleted User] (2022-12-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-19)

[Empty comment from Monorail migration]

### dl...@chromium.org (2022-12-19)

Played around with this for about an hour and was not able to reproduce the overflow on Linux. I will give it another shot tomorrow with another device.
Otherwise, marking as WontFix as of 111.0.5488.0 if I am unable to reproduce tomorrow.

### dl...@chromium.org (2022-12-19)

[Empty comment from Monorail migration]

### aj...@google.com (2022-12-19)

This repros on Windows pretty easily. (build from 2ab4891)

use_goma = true
enable_ipc_fuzzer = true
is_asan = true
is_component_build = false
is_debug = false
blink_symbol_level = 0
symbol_level = 2
v8_enable_verify_heap = true
use_libfuzzer = true
dcheck_always_on = false

### aj...@google.com (2022-12-19)

also repros at affc006

### dl...@chromium.org (2022-12-19)

Weird, I will try this again on Windows. 

Attaching a screenshot of what I am seeing on Linux. Looks like empty tabs are being saved into the group and only once clicking them do we crash. 

Any thoughts here @dpenning?

### [Deleted User] (2022-12-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dp...@chromium.org (2022-12-20)

This is a feature which is under active development and is not released yet and is not planned to be released until 112, we are aware of this bug but this shouldnt be a release blocker for stable. ajgo@google.com unless you have a different opinion here im removing ReleaseBlock-Stable. I will followup with a fix to prevent these empty URLs from being added to saved groups, and will make sure they arent openable.

### dp...@chromium.org (2022-12-20)

[Empty comment from Monorail migration]

### aj...@google.com (2022-12-20)

https://crbug.com/chromium/1401965#c26 makes sense - you might be in a losing battle with a robot but I agree this doesn't block a stable release.

### [Deleted User] (2022-12-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-26)

[Empty comment from Monorail migration]

### dp...@chromium.org (2022-12-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-27)

[Empty comment from Monorail migration]

### li...@chromium.org (2022-12-28)

[Empty comment from Monorail migration]

### li...@chromium.org (2022-12-28)

Another reporter seems to have found the root cause of this in crbug.com/1403917 . 

Looks like this was introduced recently in this CL https://chromium-review.googlesource.com/c/chromium/src/+/4032404 with the addition of an optional tab_id in SavedTabGroupUpdatedLocally(). 

I'm not extremely familiar with TabGroups but it looks like RemoveTab only needs the tab_id to get an index, so passing in the index might fix this? Swapping the calls to SavedTabGroupUpdatedLocally() and RemoveTab() doesn't look like it would work since SavedTabGroupUpdatedLocally() may also delete the tab_id now.

### [Deleted User] (2022-12-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-28)

[Empty comment from Monorail migration]

### dp...@chromium.org (2022-12-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-31)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-01)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-03)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9164268736dc5c6a57b69b4c1a10e69efef2e40c

commit 9164268736dc5c6a57b69b4c1a10e69efef2e40c
Author: dljames <dljames@google.com>
Date: Tue Jan 03 22:04:23 2023

[ SavedTabGroup ] Ungroup UAF Bug Fix

Fixes a uaf that would occur when ungrouping a saved group from the tab
group editor bubble view in the tab strip.

Change-Id: Ieb6df65369ba6c377ccfbd893c0c441cf890aae9
Bug: 1401965
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4130410
Reviewed-by: Eshwar Stalin <estalin@chromium.org>
Reviewed-by: Alison Gale <agale@chromium.org>
Commit-Queue: Darryl James <dljames@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1088377}

[modify] https://crrev.com/9164268736dc5c6a57b69b4c1a10e69efef2e40c/components/saved_tab_groups/saved_tab_group_model.cc


### dl...@chromium.org (2023-01-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-12)

Congratulations, Khalil! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug. Thank you for your efforts in reporting this issue to us! 

### am...@google.com (2023-01-14)

[Empty comment from Monorail migration]

### dl...@chromium.org (2023-01-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-04-12)

This issue was migrated from crbug.com/chromium/1401965?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1403664, crbug.com/chromium/1403917, crbug.com/chromium/1407513]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062298)*
