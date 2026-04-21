# Security: heap-use-after-free in ProfileImpl::IsSameOrParent

| Field | Value |
|-------|-------|
| **Issue ID** | [40058486](https://issues.chromium.org/issues/40058486) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions>API, Webstore |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | db...@chromium.org |
| **Created** | 2022-01-13 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

When an extension install confirmation dialog is accepted, an `approval` with a `profile` pointer is added to `g_pending_approvals`.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/webstore_private/webstore_private_api.cc;l=765;drc=82f2898b695b46280dcece62f22bcf72ecdc266b>

std::unique\_ptr[WebstoreInstaller::Approval](javascript:void(0);) approval(  

WebstoreInstaller::Approval::CreateWithNoInstallPrompt(  

profile\_, details().id, std::move(parsed\_manifest\_), false));  

approval->use\_app\_installed\_bubble = !!details().app\_install\_bubble;  

// If we are enabling the launcher, we should not show the app list in order  

// to train the user to open it themselves at least once.  

approval->skip\_post\_install\_ui = !!details().enable\_launcher;  

approval->dummy\_extension = dummy\_extension\_.get();  

approval->installing\_icon = gfx::ImageSkia::CreateFrom1xBitmap(icon\_);  

approval->bypassed\_safebrowsing\_friction = friction\_dialog\_shown\_;  

if (details().authuser)  

approval->authuser = \*details().authuser;  

g\_pending\_approvals.Get().PushApproval(std::move(approval));

Once the extension is ready to install, the `approval` is removed from `g_pending_approvals`.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/webstore_private/webstore_private_api.cc;l=921;drc=82f2898b695b46280dcece62f22bcf72ecdc266b>

approval\_ =  

g\_pending\_approvals.Get().PopApproval(profile, params->expected\_id);

By closing the Web Store tab, we can prevent Web Store's chrome.webstorePrivate.completeInstall from calling the C++ code and the approval from being removed from `g_pending_approvals`. For debug purposes, setting a breakpoint in DevTools at `chrome.webstorePrivate.completeInstall(` works the same.

Now, closing the browser window has destroyed the `profile`.

In the other profile (either the same after relaunch or a second profile), we will install the same extension.

The `PopApproval` will go thru the approvals, and pass the (destroyed) `profile` pointer to `ProfileImpl::IsSameOrParent`.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/webstore_private/webstore_private_api.cc;l=129;drc=82f2898b695b46280dcece62f22bcf72ecdc266b>

std::unique\_ptr[WebstoreInstaller::Approval](javascript:void(0);) PendingApprovals::PopApproval(  

Profile\* profile,  

const std::string& id) {  

for (auto iter = approvals\_.begin(); iter != approvals\_.end(); ++iter) {  

if (iter->get()->extension\_id == id &&  

profile->IsSameOrParent(iter->get()->profile)) { <--- iter->get()->profile can be already destroyed  

std::unique\_ptr[WebstoreInstaller::Approval](javascript:void(0);) approval = std::move(\*iter);  

approvals\_.erase(iter);  

return approval;  

}  

}  

return nullptr;  

}

And `IsSameOrParent` will call `GetOriginalProfile()` on the `profile`.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile_impl.cc;l=1350;drc=45dc15e901ba2d7ca5549c9551ccb1cb3f6f9ec5>

bool ProfileImpl::IsSameOrParent(Profile\* profile) {  

return profile && profile->GetOriginalProfile() == this;  

}

**VERSION**  

Chrome Version: 99.0.4820.0  

Operating System: Windows 10

**REPRODUCTION CASE**  

This can be reproduced with one profile or multiple profiles as well.

Case A (single profile):

1. Open Chromium
2. Make sure it stays alive after the browser window is closed, e.g. by opening the profile manager
3. Open any extension/app in the Web Store (<https://chrome.google.com/webstore/detail/aapbdbdomjkkjkaonfhkkikfgjllcleb>)
4. Click "Add to Chrome"
5. Click "Add extension" and immediately close the tab
6. Relaunch the browser window and open the Web Store page
7. Click "Add to Chrome" and "Add extension"

Case B (two profiles):

1. Open two browser windows, each with a different profile
2. In both windows, open any extension/app in the Web Store (<https://chrome.google.com/webstore/detail/aapbdbdomjkkjkaonfhkkikfgjllcleb>)

> Profile 1 window:

3. Click "Add to Chrome"
4. Click "Add extension" and immediately close the tab
5. Close this browser window

> Profile 2 window:

6. Click "Add to Chrome" and "Add extension"

We can verify that the approval wasn't deleted by trying to install the extension in the original profile: "This item is already being downloaded and added into Chrome."

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser Crash State:

==39768==ERROR: AddressSanitizer: heap-use-after-free on address 0x1179f3a2ac40 at pc 0x7ff835941855 bp 0x0030f9bfdf00 sp 0x0030f9bfdf48  

READ of size 8 at 0x1179f3a2ac40 thread T0  

==39768==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff835941854 in ProfileImpl::IsSameOrParent C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:1351  

#1 0x7ff842ba0e4a in extensions::`anonymous namespace'::PendingApprovals::PopApproval C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\api\webstore_private\webstore_private_api.cc:131 #2 0x7ff842ba687e in extensions::WebstorePrivateCompleteInstallFunction::Run C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\api\webstore_private\webstore_private_api.cc:922 #3 0x7ff82de3de0b in ExtensionFunction::RunWithValidation C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function.cc:513 #4 0x7ff82de45092 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function_dispatcher.cc:401 #5 0x7ff82de4440b in extensions::ExtensionFunctionDispatcher::Dispatch C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function_dispatcher.cc:257 #6 0x7ff82de3b446 in extensions::ExtensionFrameHost::Request C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_frame_host.cc:46 #7 0x7ff82b6d1bb7 in extensions::mojom::LocalFrameHostStubDispatch::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\extensions\common\mojom\frame.mojom.cc:2087 #8 0x7ff82de3c5e6 in extensions::mojom::LocalFrameHostStub<mojo::RawPtrImplRefTraits<extensions::mojom::LocalFrameHost> >::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\extensions\common\mojom\frame.mojom.h:295 #9 0x7ff8331f9fdd in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:863 #10 0x7ff835b61bc5 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:48 #11 0x7ff8331fd840 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:658 #12 0x7ff833a7eb3b in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1008  

#13 0x7ff833a78757 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:741  

#14 0x7ff832eaca84 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#15 0x7ff835a1c2d5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#16 0x7ff835a1b9a8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#17 0x7ff832f55496 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#18 0x7ff832f53728 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#19 0x7ff835a1d9a1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#20 0x7ff832e2b5f3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#21 0x7ff82bfa2edd in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#22 0x7ff82bfa82fd in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#23 0x7ff82bf9c565 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#24 0x7ff82ea5e633 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#25 0x7ff82ea61673 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1160  

#26 0x7ff82ea607a6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#27 0x7ff82ea5ca7d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#28 0x7ff82ea5db08 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#29 0x7ff8282d148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#30 0x7ff7cbdc5b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#31 0x7ff7cbdc2b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#32 0x7ff7cc1c323f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#33 0x7ff8e0047033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#34 0x7ff8e06e2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x1179f3a2ac40 is located 0 bytes inside of 424-byte region [0x1179f3a2ac40,0x1179f3a2ade8)  

freed by thread T0 here:  

#0 0x7ff7cbe72b9b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff8359423e9 in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:861  

#2 0x7ff83595405f in ProfileDestroyer::DestroyOriginalProfileNow C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_destroyer.cc:133  

#3 0x7ff835953893 in ProfileDestroyer::DestroyProfileWhenAppropriate C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_destroyer.cc:61  

#4 0x7ff832cc0cc1 in ProfileManager::ProfileInfo::~ProfileInfo C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1683  

#5 0x7ff832cc75e7 in std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:315  

#6 0x7ff832cc7ade in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::\_\_map\_value\_compare<base::FilePath,std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::less[base::FilePath](javascript:void(0);),1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > > > >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2422  

#7 0x7ff832cc7a33 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::\_\_map\_value\_compare<base::FilePath,std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::less[base::FilePath](javascript:void(0);),1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > > > >::\_\_erase\_unique[base::FilePath](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2445  

#8 0x7ff832cbe3f2 in ProfileManager::RemoveProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1788  

#9 0x7ff832cbe168 in ProfileManager::DeleteProfileIfNoKeepAlive C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1518  

#10 0x7ff832cbdc35 in ProfileManager::RemoveKeepAlive C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1475  

#11 0x7ff832eaca84 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#12 0x7ff835a1c2d5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#13 0x7ff835a1b9a8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#14 0x7ff832f55496 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#15 0x7ff832f53728 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#16 0x7ff835a1d9a1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#17 0x7ff832e2b5f3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#18 0x7ff82bfa2edd in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#19 0x7ff82bfa82fd in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#20 0x7ff82bf9c565 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#21 0x7ff82ea5e633 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#22 0x7ff82ea61673 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1160  

#23 0x7ff82ea607a6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#24 0x7ff82ea5ca7d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#25 0x7ff82ea5db08 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#26 0x7ff8282d148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#27 0x7ff7cbdc5b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169

previously allocated by thread T0 here:  

#0 0x7ff7cbe72c9b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff8456e4fbe in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff835936ddd in Profile::CreateProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:366  

#3 0x7ff832cbbe89 in ProfileManager::CreateProfileHelper C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1379  

#4 0x7ff832caf736 in ProfileManager::CreateAndInitializeProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1826  

#5 0x7ff832cad2e6 in ProfileManager::GetProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:744  

#6 0x7ff83879cb9c in GetStartupProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup\_browser\_creator.cc:1392  

#7 0x7ff835731c75 in `anonymous namespace'::CreatePrimaryProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:420  

#8 0x7ff83572ecfa in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1425  

#9 0x7ff83572d890 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1080  

#10 0x7ff82bfa08fe in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:978  

#11 0x7ff82cdeda29 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup\_task\_runner.cc:43  

#12 0x7ff82bf9fd5b in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:886  

#13 0x7ff82bfa77ed in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:132  

#14 0x7ff82bf9c510 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:26  

#15 0x7ff82ea5e633 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#16 0x7ff82ea61673 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1160  

#17 0x7ff82ea607a6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#18 0x7ff82ea5ca7d in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#19 0x7ff82ea5db08 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#20 0x7ff8282d148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#21 0x7ff7cbdc5b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#22 0x7ff7cbdc2b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#23 0x7ff7cc1c323f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#24 0x7ff8e0047033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#25 0x7ff8e06e2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:1351 in ProfileImpl::IsSameOrParent  

Shadow bytes around the buggy address:  

0x038132145530: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x038132145540: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x038132145550: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x038132145560: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x038132145570: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

=>0x038132145580: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd  

0x038132145590: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0381321455a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0381321455b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

0x0381321455c0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0381321455d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==39768==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [uaf.mp4](attachments/uaf.mp4) (video/mp4, 5.5 MB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 5.7 MB)
- [asan.log](attachments/asan.log) (text/plain, 20.9 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 294 B)
- [background.js](attachments/background.js) (text/plain, 2.7 KB)
- [extension-poc.mp4](attachments/extension-poc.mp4) (video/mp4, 1.4 MB)
- [focus.html](attachments/focus.html) (text/plain, 32 B)
- [focus.js](attachments/focus.js) (text/plain, 101 B)
- [popup.html](attachments/popup.html) (text/plain, 1 B)

## Timeline

### [Deleted User] (2022-01-13)

[Empty comment from Monorail migration]

### ct...@chromium.org (2022-01-14)

I was unable to reproduce this on Linux (ASAN release r958106, which matches current M99 canary) using the "single profile" steps -- after closing the tab a new window immediately pops up with the "Google Translate has been added to Chromium" confirmation bubble. I'm spinning up a Windows machine to test there next.

### st...@gmail.com (2022-01-16)

In my testing, the time window between PushApproval to PopApproval ranged anywhere from tens of milliseconds to tens of seconds.
However, this is now irrelevant to the repro steps as I realized this doesn't have to involve a tab close race at all if the tab is closed before the dialog is closed.

Updated repro steps:
================

Case A (single profile):
1. Open Chromium
2. Make sure it stays alive after the browser window is closed, e.g. by opening the profile manager
3. Open any extension/app in the Web Store (https://chrome.google.com/webstore/detail/aapbdbdomjkkjkaonfhkkikfgjllcleb)
4. Click "Add to Chrome"
5. Close the Web Store tab
6. Click "Add extension"
7. Relaunch the browser window and open the Web Store page
8. Click "Add to Chrome" and "Add extension"

Case B (two profiles):
1. Open two browser windows, each with a different profile
2. In both windows, open any extension/app in the Web Store (https://chrome.google.com/webstore/detail/aapbdbdomjkkjkaonfhkkikfgjllcleb)
> Profile 1 window:
3. Click "Add to Chrome"
4. Close the Web Store tab
5. Click "Add extension"
6. Close this browser window
> Profile 2 window:
7. Click "Add to Chrome" and "Add extension"


There are various different ways to close the Web Store tab while keeping the install confirmation dialog open. The dialog lives in the context of a browser window, not the Web Store tab, so closing the tab will keep it open.
- In a window with 2 tabs (Web Store + NTP), click "Add to Chrome" and close the tab a second later. A few seconds later the dialog will open over the NTP. This requires some timing but I can reproduce this most of the time.
or
- With 2 windows, click "Add to Chrome". A dialog will open over window 1. In window 2, use the new TopChrome Tab Search feature to close the Web Store tab.
or
- Kill the tab via the task manager / extension / etc...

The important thing is to prevent the Web Store page to send a mojo message via the JavaScript function `chrome.webstorePrivate.completeInstall`.

### aj...@google.com (2022-01-19)

I too am not able to repro this although I expect the race isn't easy to trigger.

igorruvinov@chromium.org: based on recent history you've done recent actual work in this file - could you take a look or suggest someone that is working in this area now?

Tentatively setting FoundIn-96 and severity=medium - this would be High but there is significant user interaction and no web control poc at present.

stw.stw.tom: it would be wonderful if you could create a poc which demonstrates that a website or extension can make this happen reliably.

[Monorail components: Platform>Extensions>API Webstore]

### [Deleted User] (2022-01-19)

[Empty comment from Monorail migration]

### ig...@google.com (2022-01-19)

That work was a one-off so I'm unfortunately not very familiar with extensions-related code. Assigning to rdevlin.cronin@chromium.org to take a look or reassign to another team member.

### st...@gmail.com (2022-01-19)

https://crbug.com/chromium/1286940#c4: In my updated repro steps in https://crbug.com/chromium/1286940#c3, no timing/race is required for it to reproduce anymore. I uploaded a new screen recording showing this. So following the steps in https://crbug.com/chromium/1286940#c3 by closing the tab first using Tab Search (for example), this should be reproducible 100% of the time. The repro steps in https://crbug.com/chromium/1286940#c0 still work but need fast timing, whereas the steps (closing the tab before accepting the dialog) in https://crbug.com/chromium/1286940#c3 don't require any timing.

There are countless ways to close a tab, either by the user (using Tab Search / Task manager), by a website (payment/webID dialog), or an extension. Some of the repro steps could by done by an extension, but the user would still need to click "Add extension" in the dialog.

### [Deleted User] (2022-01-19)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-19)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2022-01-21)

By carefully following the steps in the video I can indeed cause this crash to happen.

My feeling is that there are too many user interactions for us to consider this as a serious security issue, it is very unlikely to be useful to an attacker as there is no way to control this from the web or from an extension. We will turn this into a normal regression in a couple of days and address it.

If you can demonstrate an automatic POC with much less user interaction, then we will keep this in the security queue.


### aj...@google.com (2022-01-21)

Assigning to an arbitrary OWNER - please route to someone that can take a look!

### st...@gmail.com (2022-01-21)

Working on an extension POC with less user interaction.

### st...@gmail.com (2022-01-22)

I've created an extension that removes the need for some of the steps, reducing the user interaction to the following:

1. Open Profile manager
2. "Add to Chrome" -> "Add extension"
3. Reopen the browser (in Profile manager)
4. "Add to Chrome" -> "Add extension"

The extension takes care of preventing `completeInstall` being called in step 2 when the user tries to install the extension. It is done by automatically closing the Web Store tab once the dialog is open. After the dialog is closed, the window (profile) is closed. User reopens the profile, tries to install the extension, UAF.

### aj...@google.com (2022-01-24)

Thanks that is a better demonstration, we appreciate the extra effort! Setting sev=high as this is a browser uaf reachable via an extension.

### [Deleted User] (2022-01-27)

dbertoni: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3da687e35069ff2ec44af3140923359ecb67005c

commit 3da687e35069ff2ec44af3140923359ecb67005c
Author: David Bertoni <dbertoni@chromium.org>
Date: Tue Feb 01 20:32:17 2022

[Extensions] Fix UAF issue in webstorePrivate API.

The webstorePrivate API keeps a list of objects with pointers to
Profile instances and those objects can, in rare cases, outlive
them. This CL adds code to observe Profile lifetimes and remove
any objects that are associated with Profile instances that are
destroyed.

Bug: 1286940
Change-Id: I6e8acc44469f7af3ecb5c522363d4365d9514107
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3416494
Auto-Submit: David Bertoni <dbertoni@chromium.org>
Reviewed-by: Kelvin Jiang <kelvinjiang@chromium.org>
Commit-Queue: Kelvin Jiang <kelvinjiang@chromium.org>
Cr-Commit-Position: refs/heads/main@{#965847}

[modify] https://crrev.com/3da687e35069ff2ec44af3140923359ecb67005c/chrome/browser/extensions/api/webstore_private/webstore_private_api.h
[modify] https://crrev.com/3da687e35069ff2ec44af3140923359ecb67005c/chrome/browser/extensions/api/webstore_private/webstore_private_api.cc
[modify] https://crrev.com/3da687e35069ff2ec44af3140923359ecb67005c/chrome/browser/extensions/api/webstore_private/webstore_private_unittest.cc


### db...@chromium.org (2022-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

Requesting merge to stable M98 because latest trunk commit (965847) appears to be after stable branch point (950365).

Requesting merge to dev M99 because latest trunk commit (965847) appears to be after dev branch point (961656).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

Merge approved: your change passed merge requirements and is auto-approved for M99. Please go ahead and merge the CL to branch 4844 (refs/branch-heads/4844) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

Merge review required: M98 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-02-08)

[Bulk Edit] Your change has been approved for M99 branch,please go ahead and merge the CL's to M99 branch(go/chrome-branches) manually asap so that they would be part of tomorrows M99 Beta release.

### am...@chromium.org (2022-02-09)

merge tentatively approved to M98, please confirm there are no stability issues or other concerns and merge to branch 4758 NLT Thursday, 10 February so this fix can be included in next week's Stable channel respin -- thank you! 

### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and nice work! 

### gi...@appspot.gserviceaccount.com (2022-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/92513389e86c68a162574a74c55c0cf34cbab073

commit 92513389e86c68a162574a74c55c0cf34cbab073
Author: David Bertoni <dbertoni@chromium.org>
Date: Fri Feb 11 20:04:44 2022

[Extensions] Fix UAF issue in webstorePrivate API.

The webstorePrivate API keeps a list of objects with pointers to
Profile instances and those objects can, in rare cases, outlive
them. This CL adds code to observe Profile lifetimes and remove
any objects that are associated with Profile instances that are
destroyed.

(cherry picked from commit 3da687e35069ff2ec44af3140923359ecb67005c)

Bug: 1286940
Change-Id: I6e8acc44469f7af3ecb5c522363d4365d9514107
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3416494
Auto-Submit: David Bertoni <dbertoni@chromium.org>
Reviewed-by: Kelvin Jiang <kelvinjiang@chromium.org>
Commit-Queue: Kelvin Jiang <kelvinjiang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#965847}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3457262
Reviewed-by: David Bertoni <dbertoni@chromium.org>
Commit-Queue: David Bertoni <dbertoni@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#1149}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/92513389e86c68a162574a74c55c0cf34cbab073/chrome/browser/extensions/api/webstore_private/webstore_private_api.h
[modify] https://crrev.com/92513389e86c68a162574a74c55c0cf34cbab073/chrome/browser/extensions/api/webstore_private/webstore_private_api.cc
[modify] https://crrev.com/92513389e86c68a162574a74c55c0cf34cbab073/chrome/browser/extensions/api/webstore_private/webstore_private_unittest.cc


### [Deleted User] (2022-02-11)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-02-12)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8bccbf86d76c1ff282248c9f2e0c3092267a1f9b

commit 8bccbf86d76c1ff282248c9f2e0c3092267a1f9b
Author: David Bertoni <dbertoni@chromium.org>
Date: Tue Feb 15 18:27:21 2022

[Extensions] Fix UAF issue in webstorePrivate API.

The webstorePrivate API keeps a list of objects with pointers to
Profile instances and those objects can, in rare cases, outlive
them. This CL adds code to observe Profile lifetimes and remove
any objects that are associated with Profile instances that are
destroyed.

(cherry picked from commit 3da687e35069ff2ec44af3140923359ecb67005c)

(cherry picked from commit 3da687e35069ff2ec44af3140923359ecb67005c)

Bug: 1286940
Change-Id: I2490f4f9f7e92ee83c4bb5ecc2e2b57f023f3fd3
Cr-Original-Commit-Position: refs/heads/main@{#965847}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3462525
Auto-Submit: David Bertoni <dbertoni@chromium.org>
Reviewed-by: Tim <tjudkins@chromium.org>
Commit-Queue: Tim <tjudkins@chromium.org>
Cr-Commit-Position: refs/branch-heads/4844@{#552}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/8bccbf86d76c1ff282248c9f2e0c3092267a1f9b/chrome/browser/extensions/api/webstore_private/webstore_private_api.h
[modify] https://crrev.com/8bccbf86d76c1ff282248c9f2e0c3092267a1f9b/chrome/browser/extensions/api/webstore_private/webstore_private_api.cc
[modify] https://crrev.com/8bccbf86d76c1ff282248c9f2e0c3092267a1f9b/chrome/browser/extensions/api/webstore_private/webstore_private_unittest.cc


### rz...@google.com (2022-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-16)

1. Just https://crrev.com/c/3461368
2. Low, no conflicts
3. 98, 99
4. Yes

### gm...@google.com (2022-02-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/17abdb65f470f7d150e1abd79d0812121e7095a8

commit 17abdb65f470f7d150e1abd79d0812121e7095a8
Author: David Bertoni <dbertoni@chromium.org>
Date: Thu Feb 17 12:08:22 2022

[M96-LTS][Extensions] Fix UAF issue in webstorePrivate API.

The webstorePrivate API keeps a list of objects with pointers to
Profile instances and those objects can, in rare cases, outlive
them. This CL adds code to observe Profile lifetimes and remove
any objects that are associated with Profile instances that are
destroyed.

(cherry picked from commit 3da687e35069ff2ec44af3140923359ecb67005c)

Bug: 1286940
Change-Id: I6e8acc44469f7af3ecb5c522363d4365d9514107
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3416494
Auto-Submit: David Bertoni <dbertoni@chromium.org>
Commit-Queue: Kelvin Jiang <kelvinjiang@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#965847}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3461368
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1479}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/17abdb65f470f7d150e1abd79d0812121e7095a8/chrome/browser/extensions/api/webstore_private/webstore_private_api.h
[modify] https://crrev.com/17abdb65f470f7d150e1abd79d0812121e7095a8/chrome/browser/extensions/api/webstore_private/webstore_private_api.cc
[modify] https://crrev.com/17abdb65f470f7d150e1abd79d0812121e7095a8/chrome/browser/extensions/api/webstore_private/webstore_private_unittest.cc


### rz...@google.com (2022-02-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1286940?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions>API, Webstore]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058486)*
