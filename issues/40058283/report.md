# Security: heap-buffer-overflow in TabStripModel::MoveWebContentsAtImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40058283](https://issues.chromium.org/issues/40058283) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Windows |
| **Reporter** | st...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2021-12-18 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

With the Touch UI layout, dragging a tab group after a tab that has just closed causes a heap-buffer-overflow.

**VERSION**  

Chrome Version: 99.0.4774.0  

Operating System: Windows 10

**REPRODUCTION CASE**

1. chrome --top-chrome-touch-ui=enabled
2. Add the NTP to a new tab group
3. Open poc.html in a new tab
4. Drag the tab group to the right of poc.html

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser Crash State:

==15532==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x127bf1b11f18 at pc 0x7ffbbad33ac5 bp 0x00bc837fde60 sp 0x00bc837fdea8  

READ of size 8 at 0x127bf1b11f18 thread T0  

==15532==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffbbad33ac4 in std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::\_\_move\_range C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1763  

#1 0x7ffbbad2dc11 in std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::insert C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1821  

#2 0x7ffbbad18d51 in TabStripModel::MoveWebContentsAtImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:2018  

#3 0x7ffbbad1a3af in TabStripModel::MoveGroupTo C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:681  

#4 0x7ffbc284c027 in TabStripPageHandler::MoveGroup C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\tab\_strip\tab\_strip\_page\_handler.cc:673  

#5 0x7ffbb43472e0 in tab\_strip::mojom::PageHandlerStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\chrome\browser\ui\webui\tab\_strip\tab\_strip.mojom.cc:1841  

#6 0x7ffbb8d2b919 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:900  

#7 0x7ffbbb6864f2 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#8 0x7ffbb8d2f190 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:657  

#9 0x7ffbb8d4355f in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1104  

#10 0x7ffbb8d42331 in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:724  

#11 0x7ffbbb6864f2 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#12 0x7ffbb8d26897 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:556  

#13 0x7ffbb8d28475 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:614  

#14 0x7ffbb8d7c652 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#15 0x7ffbb89d87e4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#16 0x7ffbbb53d605 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#17 0x7ffbbb53ccd8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#18 0x7ffbb8a7fb46 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#19 0x7ffbb8a7ddd8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#20 0x7ffbbb53ecd1 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#21 0x7ffbb8958403 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#22 0x7ffbb1b25037 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#23 0x7ffbb1b2a479 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#24 0x7ffbb1b1e602 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#25 0x7ffbb45bfe2f in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#26 0x7ffbb45c2eff in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1160  

#27 0x7ffbb45c2032 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#28 0x7ffbb45be1ed in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#29 0x7ffbb45bf278 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#30 0x7ffbaddf148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#31 0x7ff6fb715b65 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#32 0x7ff6fb712c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#33 0x7ff6fbb1969f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#34 0x7ffc5ca67033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#35 0x7ffc5e9c2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x127bf1b11f18 is located 8 bytes to the left of 64-byte region [0x127bf1b11f20,0x127bf1b11f60)  

allocated by thread T0 here:  

#0 0x7ff6fb7c28bb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffbcb397bfe in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffbbad2dcfa in std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::insert C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1828  

#3 0x7ffbbad120ee in TabStripModel::InsertWebContentsAtImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1740  

#4 0x7ffbbad11a34 in TabStripModel::InsertWebContentsAt C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:366  

#5 0x7ffbc0154564 in chrome::`anonymous namespace'::AddRestoredTabImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_tabrestore.cc:164  

#6 0x7ffbc015366e in chrome::AddRestoredTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_tabrestore.cc:243  

#7 0x7ffbbd2b706e in BrowserLiveTabContext::AddRestoredTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_live\_tab\_context.cc:218  

#8 0x7ffbb3635f2a in sessions::TabRestoreServiceHelper::RestoreTab C:\b\s\w\ir\cache\builder\src\components\sessions\core\tab\_restore\_service\_helper.cc:854  

#9 0x7ffbb363267a in sessions::TabRestoreServiceHelper::RestoreEntryById C:\b\s\w\ir\cache\builder\src\components\sessions\core\tab\_restore\_service\_helper.cc:423  

#10 0x7ffbb3632121 in sessions::TabRestoreServiceHelper::RestoreMostRecentEntry C:\b\s\w\ir\cache\builder\src\components\sessions\core\tab\_restore\_service\_helper.cc:376  

#11 0x7ffbb364749e in sessions::TabRestoreServiceImpl::RestoreMostRecentEntry C:\b\s\w\ir\cache\builder\src\components\sessions\core\tab\_restore\_service\_impl.cc:1473  

#12 0x7ffbc009a121 in chrome::RestoreTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_tab\_restorer.cc:116  

#13 0x7ffbbd22fd76 in chrome::BrowserCommandController::ExecuteCommandWithDisposition C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_command\_controller.cc:482  

#14 0x7ffbbe628545 in BrowserView::AcceleratorPressed C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser\_view.cc:3425  

#15 0x7ffbbe0cd24f in ui::AcceleratorManager::Process C:\b\s\w\ir\cache\builder\src\ui\base\accelerators\accelerator\_manager.cc:83  

#16 0x7ffbbb14da80 in views::FocusManager::ProcessAccelerator C:\b\s\w\ir\cache\builder\src\ui\views\focus\focus\_manager.cc:536  

#17 0x7ffbbe61f911 in BrowserView::PreHandleKeyboardEvent C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\frame\browser\_view.cc:2361  

#18 0x7ffbb2a24faa in content::WebContentsImpl::PreHandleKeyboardEvent C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:3228  

#19 0x7ffbb271fe6f in content::RenderWidgetHostImpl::ForwardKeyboardEventWithCommands C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_impl.cc:1781  

#20 0x7ffbb276305b in content::RenderWidgetHostViewAura::ForwardKeyboardEventWithLatencyInfo C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_view\_aura.cc:2603  

#21 0x7ffbb2d83c40 in content::RenderWidgetHostViewEventHandler::OnKeyEvent C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_widget\_host\_view\_event\_handler.cc:274  

#22 0x7ffbb9657485 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#23 0x7ffbb96569a5 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#24 0x7ffbb965628f in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#25 0x7ffbb9655ed0 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#26 0x7ffbbe0ee5dc in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#27 0x7ffbb9f351e4 in aura::WindowTreeHost::DispatchKeyEventPostIME C:\b\s\w\ir\cache\builder\src\ui\aura\window\_tree\_host.cc:363

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1763 in std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::\_\_move\_range  

Shadow bytes around the buggy address:  

0x04bf6f6e2390: 00 00 00 00 fc fc fc fc fa fa fa fa fd fd fd fd  

0x04bf6f6e23a0: fd fd fd fa fa fa fa fa fd fd fd fd fd fd fd fa  

0x04bf6f6e23b0: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa  

0x04bf6f6e23c0: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x04bf6f6e23d0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fa  

=>0x04bf6f6e23e0: fa fa fa[fa]00 00 00 00 fc fc fc fc fa fa fa fa  

0x04bf6f6e23f0: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  

0x04bf6f6e2400: fd fd fd fa fa fa fa fa fd fd fd fd fd fd fd fa  

0x04bf6f6e2410: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

0x04bf6f6e2420: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x04bf6f6e2430: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

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

==15532==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 55 B)
- [heap-buffer-overflow.mp4](attachments/heap-buffer-overflow.mp4) (video/mp4, 4.2 MB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 478.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 162 B)

## Timeline

### [Deleted User] (2021-12-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-12-20)

connily: PTAL as well. Also split from https://crbug.com/chromium/1278789. (I can't get the touch UI work on Mac so I can't repro yet)

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### [Deleted User] (2021-12-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@gmail.com (2021-12-24)

The heap buffer overflow happens at

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_strip_model.cc;l=2018;drc=43c99a312a3fa5736d6eca4db63908c08ddafff3

    contents_data_.insert(contents_data_.begin() + to_position,
                            std::move(moved_data));

as there is no check if `to_position` is out of bounds of `contents_data_`.


---------------------------------------------------------------------------------------------------------


The fix would be to constrain `to_index` in `TabStripModel::MoveGroupTo`
and add a CHECK in `TabStripModel::MoveWebContentsAtImpl` to crash in case it's called with an invalid index.


https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_strip_model.cc;l=671;drc=0e45c020c43b1a9f6d2870ff7f92b30a2f03a458

to_index = ConstrainMoveIndex(to_index, false);


https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_strip_model.cc;l=2013;drc=43c99a312a3fa5736d6eca4db63908c08ddafff3

CHECK_LT(index, static_cast<int>(contents_data_.size()));
CHECK_LT(to_position, static_cast<int>(contents_data_.size()));
// or
CHECK(ContainsIndex(index));
CHECK(ContainsIndex(to_position));

### [Deleted User] (2022-01-01)

connily: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2022-01-06)

Here's another, I can help with a Windows repro if that's the only OS relevant.

### dp...@chromium.org (2022-01-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c2fe04dcc3bcf122d9a9909b4367739b5bde33ad

commit c2fe04dcc3bcf122d9a9909b4367739b5bde33ad
Author: dljames <dljames@google.com>
Date: Thu Jan 13 22:41:13 2022

Added error handling when tab dragging a tab group to the right of a tab

Bug: 1281078
Change-Id: I05bf4ed6e7e489c668c045c316479946da16dedc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3387954
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Auto-Submit: Darryl James <dljames@chromium.org>
Commit-Queue: Darryl James <dljames@chromium.org>
Cr-Commit-Position: refs/heads/main@{#958882}

[modify] https://crrev.com/c2fe04dcc3bcf122d9a9909b4367739b5bde33ad/chrome/browser/ui/tabs/tab_strip_model.cc


### st...@gmail.com (2022-01-14)

I can confirm that after https://crbug.com/chromium/1281078#c10 both
- manually dragging a tab group,
- sending a mojo message: `document.querySelector("tabstrip-tab-list").shadowRoot.querySelector("#unpinnedTabs > tabstrip-tab").tabsApi_.handler.moveGroup(groupId,9999)`
correctly clamp the tab group to the end.

### dp...@chromium.org (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-15)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-20)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and nice work! 

### am...@google.com (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

Not requesting merge to dev (M99) because latest trunk commit (958882) appears to be prior to dev branch point (961656). If this is incorrect, please replace the Merge-NA-99 label with Merge-Request-99. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@gmail.com (2022-01-30)

Hi Amy,

Thanks! I wanted to ask: I was just going through tab strip issues and found https://crbug.com/chromium/1239057, which has, IMO, identical repro complexity but got a different reward.
I attached a video showing that with multiple tabs closing at the same time, this is quite easy to repro. 
Would it be possible for the panel to reconsider this issue?

### am...@chromium.org (2022-02-18)

Hello, Thomas. Thanks for reaching out about this and following up with an email request. Apologies for the delay as we worked through our bug reward decisions. 
The other issue you linked as an example (https://crbug.com/chromium/1239057) was discovered and reported mid last year, and was relatively early on during very recent trend of reports away from issues triggered by remote content to issues that were strongly or solely dependent on user interaction. While these issues are important as well and can be exploited by a convincing attacker and a convinced user, they aren't as strongly exploitable and impactful as the bug reports that demonstrate exploitability with report content or the most limited. We have started to adjust reward amounts accordingly and have updated our VRP reward rules and guidelines [1] recently to reflect that. 

Based on this and while we appreciate your efforts and reporting this issue to us, the VRP Panel has decided that the original reward amount is sufficient for this report. 

[1] https://bughunters.google.com/about/rules/5745167867576320

### [Deleted User] (2022-04-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1281078?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058283)*
