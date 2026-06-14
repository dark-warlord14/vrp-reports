# Security: heap-buffer-overflow in extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [40055799](https://issues.chromium.org/issues/40055799) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API, UI>Browser>TopChrome>TabStrip |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | vm...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2021-05-10 |
| **Bounty** | $10,000.00 |

## Description

**VERSION**  

Chrome Version: (tested on) Version 92.0.4492.0 (Developer Build) (64-bit)  

Operating System: (tested on) Ubuntu20

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State:  

==1011516==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200040ff28 at pc 0x55a123335599 bp 0x7ffd5276ea20 sp 0x7ffd5276ea18  

READ of size 8 at 0x60200040ff28 thread T0 (chrome)  

==1011516==WARNING: invalid path to external symbolizer!  

==1011516==WARNING: Failed to use and restart external symbolizer!  

#0 0x55a123335598 in operator-> ./../../buildtools/third\_party/libc++/trunk/include/memory:1565:19  

#1 0x55a123335598 in TabStripModel::IsTabBlocked(int) const ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:863:10  

#2 0x55a1231bd438 in UpdateCommandsForFind ./../../chrome/browser/ui/browser\_command\_controller.cc:1526:26  

#3 0x55a1231bd438 in chrome::BrowserCommandController::TabBlockedStateChanged(content::WebContents\*, int) ./../../chrome/browser/ui/browser\_command\_controller.cc:912:3  

#4 0x55a123334270 in TabStripModel::SetTabBlocked(int, bool) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:836:14  

#5 0x55a1231ac933 in Browser::SetWebContentsBlocked(content::WebContents\*, bool) ./../../chrome/browser/ui/browser.cc:2181:21  

#6 0x55a121618c59 in BlockWebContentsInteraction ./../../components/web\_modal/web\_contents\_modal\_dialog\_manager.cc:118:16  

#7 0x55a121618c59 in web\_modal::WebContentsModalDialogManager::ShowDialogWithManager(aura::Window\*, std::\_\_1::unique\_ptr<web\_modal::SingleWebContentsDialogManager, std::\_\_1::default\_delete<web\_modal::SingleWebContentsDialogManager> >) ./../../components/web\_modal/web\_contents\_modal\_dialog\_manager.cc:46:5  

#8 0x55a124638edd in constrained\_window::ShowWebModalDialogViews(views::WidgetDelegate\*, content::WebContents\*) ./../../components/constrained\_window/constrained\_window\_views.cc:179:3  

#9 0x55a12382fe4b in ShowConstrainedWebDialog(content::BrowserContext\*, std::\_\_1::unique\_ptr<ui::WebDialogDelegate, std::\_\_1::default\_delete[ui::WebDialogDelegate](javascript:void(0);) >, content::WebContents\*) ./../../chrome/browser/ui/views/constrained\_web\_dialog\_delegate\_views.cc:526:3  

#10 0x55a1198e3d25 in printing::PrintPreviewDialogController::CreatePrintPreviewDialog(content::WebContents\*) ./../../chrome/browser/printing/print\_preview\_dialog\_controller.cc:400:55  

#11 0x55a1198e3512 in printing::PrintPreviewDialogController::PrintPreview(content::WebContents\*) ./../../chrome/browser/printing/print\_preview\_dialog\_controller.cc:222:27  

#12 0x55a119901b99 in printing::PrintViewManager::ShowScriptedPrintPreview(bool) ./../../chrome/browser/printing/print\_view\_manager.cc:322:3  

#13 0x55a10f653083 in printing::mojom::PrintManagerHostStubDispatch::Accept(printing::mojom::PrintManagerHost\*, mojo::Message\*) ./gen/components/printing/common/print.mojom.cc:5525:13  

#14 0x55a119bfa673 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:857:54  

#15 0x55a119c0b8da in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:48:24  

#16 0x55a11b4f3579 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread(mojo::Message) ./../../ipc/ipc\_mojo\_bootstrap.cc:949:24  

#17 0x55a11b4ebd44 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:509:12  

#18 0x55a11b4ebd44 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:648:12  

#19 0x55a11b4ebd44 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0, 1> ./../../base/bind\_internal.h:721:12  

#20 0x55a11b4ebd44 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:690:12  

#21 0x55a1182983d0 in Run ./../../base/callback.h:101:12  

#22 0x55a1182983d0 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:173:33  

#23 0x55a1182d2066 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:357:25  

#24 0x55a1182d1844 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:270:36  

#25 0x55a1181959f0 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:404:48  

#26 0x55a1182d317c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:466:12  

#27 0x55a118218251 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:133:14  

#28 0x55a10fce2208 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:993:20  

#29 0x55a10fce6cf5 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:152:15  

#30 0x55a10fcdbbb5 in content::BrowserMain(content::MainFunctionParams const&) ./../../content/browser/browser\_main.cc:47:28  

#31 0x55a117f6ddf9 in RunBrowserProcessMain ./../../content/app/content\_main\_runner\_impl.cc:597:10  

#32 0x55a117f6ddf9 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) ./../../content/app/content\_main\_runner\_impl.cc:1080:10  

#33 0x55a117f6d0e7 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content\_main\_runner\_impl.cc:955:12  

#34 0x55a117f676b6 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:372:36  

#35 0x55a117f67c0c in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content\_main.cc:398:10  

#36 0x55a10ad3256b in ChromeMain ./../../chrome/app/chrome\_main.cc:151:12  

#37 0x7fea8b57c0b2 in \_\_libc\_start\_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16  

0x60200040ff28 is located 8 bytes to the left of 8-byte region [0x60200040ff30,0x60200040ff38)  

allocated by thread T0 (chrome) here:  

#0 0x55a10ad2f8cd in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:99:3  

#1 0x55a1233474e5 in \_\_libcpp\_operator\_new<unsigned long> ./../../buildtools/third\_party/libc++/trunk/include/new:235:10  

#2 0x55a1233474e5 in \_\_libcpp\_allocate ./../../buildtools/third\_party/libc++/trunk/include/new:261:10  

#3 0x55a1233474e5 in allocate ./../../buildtools/third\_party/libc++/trunk/include/memory:778:38  

#4 0x55a1233474e5 in allocate ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:260:20  

#5 0x55a1233474e5 in \_\_split\_buffer ./../../buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:314:29  

#6 0x55a1233474e5 in std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::insert(std::\_\_1::\_\_wrap\_iter<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > const\*>, std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >&&) ./../../buildtools/third\_party/libc++/trunk/include/vector:1827:53  

#7 0x55a123327165 in TabStripModel::InsertWebContentsAtImpl(int, std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, base::Optional<tab\_groups::TabGroupId>) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:1768:18  

#8 0x55a123326b70 in TabStripModel::InsertWebContentsAt(int, std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, base::Optional<tab\_groups::TabGroupId>) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:395:10  

#9 0x55a121780357 in extensions::WindowsCreateFunction::Run() ./../../chrome/browser/extensions/api/tabs/tabs\_api.cc:705:25  

#10 0x55a111aac960 in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension\_function.cc:513:10  

#11 0x55a111ab51f0 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost\*, int, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&)>) ./../../extensions/browser/extension\_function\_dispatcher.cc:395:15  

#12 0x55a111ab45fd in extensions::ExtensionFunctionDispatcher::Dispatch(mojo::StructPtr[extensions::mojom::RequestParams](javascript:void(0);), content::RenderFrameHost\*, int, base::OnceCallback<void (bool, base::Value, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&)>) ./../../extensions/browser/extension\_function\_dispatcher.cc:257:3  

#13 0x55a111aa9a9a in extensions::ExtensionFrameHost::Request(mojo::StructPtr[extensions::mojom::RequestParams](javascript:void(0);), base::OnceCallback<void (bool, base::Value, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&)>) ./../../extensions/browser/extension\_frame\_host.cc:40:9  

#14 0x55a10f275e0f in extensions::mojom::LocalFrameHostStubDispatch::AcceptWithResponder(extensions::mojom::LocalFrameHost\*, mojo::Message\*, std::\_\_1::unique\_ptr<mojo::MessageReceiverWithStatus, std::\_\_1::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);) >) ./gen/extensions/common/mojom/frame.mojom.cc:2205:13  

#15 0x55a119bfa61f in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:823:56  

#16 0x55a119c0b8da in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:48:24  

#17 0x55a11b4f3579 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread(mojo::Message) ./../../ipc/ipc\_mojo\_bootstrap.cc:949:24  

#18 0x55a11b4ebd44 in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:509:12  

#19 0x55a11b4ebd44 in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> ./../../base/bind\_internal.h:648:12  

#20 0x55a11b4ebd44 in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0, 1> ./../../base/bind\_internal.h:721:12  

#21 0x55a11b4ebd44 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/bind\_internal.h:690:12  

#22 0x55a1182983d0 in Run ./../../base/callback.h:101:12  

#23 0x55a1182983d0 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:173:33  

#24 0x55a1182d2066 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:357:25  

#25 0x55a1182d1844 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:270:36  

#26 0x55a118196769 in HandleDispatch ./../../base/message\_loop/message\_pump\_glib.cc:374:46  

#27 0x55a118196769 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:124:43  

#28 0x7fea8d39a17c in g\_main\_context\_dispatch ??:0:0  

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/yhn/chrome/asan-linux-release-876982/chrome+0x232d2598)  

Shadow bytes around the buggy address:  

0x0c0480079f90: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480079fa0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480079fb0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480079fc0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480079fd0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

=>0x0c0480079fe0: fa fa fd fd fa[fa]00 fa fa fa fd fa fa fa fd fa  

0x0c0480079ff0: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fd  

0x0c048007a000: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x0c048007a010: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c048007a020: fa fa 00 fa fa fa 00 fa fa fa 00 fa fa fa fd fd  

0x0c048007a030: fa fa fd fd fa fa fd fa fa fa fd fd fa fa fd fa  

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

Shadow gap: cc  

==1011516==ABORTING

**REPRODUCTION CASE**

1. install extension\_poc.zip [will provide ASAP]

**CREDIT INFORMATION**  

**Reporter credit: [goes here]**

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 649 B)
- [background.js](attachments/background.js) (text/plain, 56 B)
- [1.html](attachments/1.html) (text/plain, 45 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [extension01.js](attachments/extension01.js) (text/plain, 4.2 KB)
- [extension02.js](attachments/extension02.js) (text/plain, 19.8 KB)
- manifest.json (text/plain, 617 B)
- [log-beta](attachments/log-beta) (text/plain, 6.2 KB)
- [Screencast from 2021年06月09日 10时39分16秒.webm](attachments/Screencast from 2021年06月09日 10时39分16秒.webm) (video/webm, 5.4 MB)

## Timeline

### [Deleted User] (2021-05-10)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-05-10)

Note: If you could, do not attach a zip file, please attach the individual files directly.

### vm...@gmail.com (2021-05-12)

Sorry for the delay, I've encountered some problems in minimizing the poc, the process of minimizing would effect the stability. In order to be as accuracy as possible, I will keep looking for the other ways, but now I can provide the poc that have less code and 5%-20% of stability, hoping to help you fix it.

This will need 2 extensions, so you'd better run with "--load-extension=./extension01,./extension02".

The 2 extensions can share the same config files:
- extension01
    manifest.json
    background.js
    js/1.html
    js/extension01.js
- extension02
    manifest.json
    background.js
    js/1.html
    js/extension02.js

### [Deleted User] (2021-05-12)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vm...@gmail.com (2021-05-12)

Hi again, I just noticed that after the updates of May 10, the TAB's attributes "highlight" have been changed. So the above js files(extension01.js
,extension02.js) need some changes. I' ve tested it on Version 92.0.4504.0 (Developer Build) (64-bit).

### xi...@chromium.org (2021-05-12)

Thanks for the report and the PoC. This looks like an issue with the tabGroups extension API. I'm not able to reproduce it on my asan build for some reason though. +connily@, could you take a look? Thanks!

Setting the severity to Medium because this is extension API and requires two extensions to be installed at once. Setting the impact to Head for now. vmth4869@, are you able to reproduce the issue on Chrome Beta or Stable?

[Monorail components: Platform>Extensions>API UI>Browser>TabStrip]

### vm...@gmail.com (2021-05-13)

Yes, I am able to reproduce this issue on both Chrome Beta and Stable. But both beta and stable need manifest version to be 3, so PoC needs to be changed again..
Here are the manifest file and asan log on beta(asan-linux-beta-91.0.4472.57). I can't get asan on stable, but I am able to get signal SIGSEGV on it.

### vm...@gmail.com (2021-05-13)

As for the requirement for reproducing this issue, it probably don't need 2 extensions, though it looks like it in my PoC. Any way I will try if there is a more stable way. Thx.

### [Deleted User] (2021-05-13)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-13)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2021-05-17)

Solomon, could you take a look at this and see if your recent fixes address this as well? I'm not quite sure if it overlaps, but I don't have the bandwidth to investigate. Thanks for your help!

### vm...@gmail.com (2021-05-18)

Hi, it seems that Commit33109f1 cannot fix it, I just reproduce the issue on Version 92.0.4512.0 (Developer Build) (64-bit).

### so...@chromium.org (2021-05-18)

[Empty comment from Monorail migration]

### so...@chromium.org (2021-05-25)

I haven't been able to reproduce a consistent crash with a normal debug build. I only saw one unrelated crash while using the attached extension. Will try to reproduce with an asan build.

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### so...@chromium.org (2021-06-08)

I'm not able to reproduce a crash with the same stack trace in https://crbug.com/chromium/1207315#c0. However, the extensions do cause a crash with asan=true for a different reason: "FATAL:service_worker_task_queue.cc(107)] Check failed: !process_manager->HasServiceWorker(*worker_id_). " Tested on Linux.

### vm...@gmail.com (2021-06-09)

[Comment Deleted]

### vm...@gmail.com (2021-06-09)

[Comment Deleted]

### vm...@gmail.com (2021-06-09)

I understand this is not a stable one to reproduce, and yes, there are certain chances that crashed on 'Check failed'. I made a video to show how it occur on my pc.

### vm...@gmail.com (2021-06-10)

If you use a script to run continuously, it will be much easier to trigger than manually.

### sr...@google.com (2021-06-14)

adding Amy to help triage if this is RBS for M92.

### so...@chromium.org (2021-06-14)

Thanks for the video. I rolled back to branch 4492 as described in https://crbug.com/chromium/1207315#c1. I'm on Linux (not Ubuntu) and still unable to see asan errors with these extensions.

### am...@chromium.org (2021-06-15)

in talking to Solomon yesterday in a separate thread, reproducing this issue has not been achieved despite multiple attempts; it seems safe to remove the RBS label at this point 

### [Deleted User] (2021-06-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vm...@gmail.com (2021-06-17)

hi, I build a brach_4472 with asan today, and it can repro. 

$ git branch -vv
  1b673f6c28b5095292d5b9cabb1d72cc8bee25fa 4e7c969173ad Organize ash/system/accessibility
* branch_4472                              4bb19460e8d8 [branch-heads/4472] Incrementing VERSION to 91.0.4472.114



### co...@chromium.org (2021-06-18)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>TabStrip UI>Browser>TopChrome>TabStrip]

### ad...@google.com (2021-06-21)

Fixing labels per https://crbug.com/chromium/1207315#c24

### co...@chromium.org (2021-06-29)

[Empty comment from Monorail migration]

### so...@chromium.org (2021-07-02)

dpenning@ is likely taking over these Tabs core related bugs.

### dp...@chromium.org (2021-07-09)

https://chromium-review.googlesource.com/c/chromium/src/+/3017321

fixes this issue.

### rs...@chromium.org (2021-07-09)

[Empty comment from Monorail migration]

### dp...@chromium.org (2021-07-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-13)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M92. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-13)

This bug requires manual review: We are only 6 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-07-13)

dpenning@ do you consider that this bug and https://crbug.com/chromium/1216898 have the same root cause, i.e. are duplicates? This matters from the point of view of VRP rewards and credits.

Which is the earliest affected version? 92 (per this bug) or 93 (per the other bug?) That's important to ensure we consider merging to the right release channels. Thanks!

### sr...@google.com (2021-07-14)

friendly ping ^

### dp...@chromium.org (2021-07-15)

adetaylor@ they are indeed duplicates. I have reason to believe the earliest affected version is older than 92 but I didn't specifically test back that far.

### ad...@google.com (2021-07-15)

Thank you. I'm going to mark this as a duplicate of the other bug, because that's the one with the fix and the technical narrative, but any VRP rewards should go to the earlier report.

### [Deleted User] (2021-07-16)

[Empty comment from Monorail migration]

### vm...@gmail.com (2021-07-19)

Hi, my understanding is that this is marked as duplicate, but this can get VRP rewards, am I right?

### am...@google.com (2021-07-19)

Hi vmth, yes, your bug was reported first, so yours will be the one that will be reviewed by the VRP Panel for a potential reward.

### vm...@gmail.com (2021-07-29)

[Comment Deleted]

### am...@chromium.org (2021-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-11)

Congratulations, Huinian Yang! The VRP Panel has decided to award you $10,000 for this report. Nice work! 

### am...@google.com (2021-08-13)

[Empty comment from Monorail migration]

### vm...@gmail.com (2021-08-26)

Hi, my credit info would be: Huinian Yang (@vmth6) of Amber Security Lab, OPPO Mobile Telecommunications Corp. Ltd. 
Thanks:)

### am...@chromium.org (2021-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-31)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1207315?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions>API, UI>Browser>TopChrome>TabStrip]
[Monorail mergedinto: crbug.com/chromium/1216898]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055799)*
