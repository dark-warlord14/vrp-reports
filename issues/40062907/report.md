# Security: use of uninitialized member variable in omnibox_popup_view_views.cc:575

| Field | Value |
|-------|-------|
| **Issue ID** | [40062907](https://issues.chromium.org/issues/40062907) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Reporter** | m....@gmail.com |
| **Assignee** | or...@chromium.org |
| **Created** | 2023-02-04 |
| **Bounty** | $4,000.00 |

## Description

**VERSION**  

WIN10 X64

```
# Set build arguments here. See `gn help buildargs`.  
is_component_build = true  
enable_nacl = false  
target_cpu = "x64"  
blink_symbol_level = 2  
v8_symbol_level = 2  
symbol_level = 2  
is_asan = true  
is_debug=false  
dcheck_always_on=false  

```

**REPRODUCTION CASE**

1. Disable backup\_ref\_ptr

```
diff --git a/base/allocator/partition_allocator/partition_alloc.gni b/base/allocator/partition_allocator/partition_alloc.gni  
index 0a4495aebd..105cf20810 100644  
--- a/base/allocator/partition_allocator/partition_alloc.gni  
+++ b/base/allocator/partition_allocator/partition_alloc.gni  
@@ -111,6 +111,7 @@ declare_args() {  
   use_asan_unowned_ptr = false  
 }  
  
+use_asan_backup_ref_ptr = false  
 # Use the version of raw_ptr<T> that allows the embedder to implement custom  
 # logic.  
 use_hookable_raw_ptr = use_asan_backup_ref_ptr  

```

2. chrome --no-sandbox --user-data-dir=test --enable-features=WebUIOmniboxPopup
3. Type anything in the address bar to trigger

Type of crash: [render]

#RCA

1. The OmniboxPopupViewViews class has a webui\_view\_[1] member
2. When USE\_BACKUP\_REF\_PTR is disable and WebUIOmniboxPopup was enable, it cause webui\_view\_ to be uninitialized and used

```
// A view representing the contents of the autocomplete popup.  
class OmniboxPopupViewViews : public views::View,  
                              public OmniboxPopupView,  
                              public views::WidgetObserver {  
 public:  
  // The reference to the child suggestions WebView. Added only if  
  // omnibox::kWebUIOmniboxPopup is enabled.  
  raw_ptr<WebUIOmniboxPopupView> webui_view_;				<<<<<[1]  

```
# ASAN

==5580==ERROR: AddressSanitizer: access-violation on unknown address 0xffffffffffffffff (pc 0x7ff9a7a95e7c bp 0x0074257f7db0 sp 0x0074257f7a60 T0)  

==5580==The signal is caused by a READ memory access.  

#0 0x7ff9a7a95e7b in views::View::GetPreferredSize D:\chromium\src\ui\views\view.cc:536  

#1 0x7ff98819c167 in OmniboxPopupViewViews::GetTargetBounds D:\chromium\src\chrome\browser\ui\views\omnibox\omnibox\_popup\_view\_views.cc:575  

#2 0x7ff98819aa25 in OmniboxPopupViewViews::UpdatePopupAppearance D:\chromium\src\chrome\browser\ui\views\omnibox\omnibox\_popup\_view\_views.cc:437  

#3 0x7ff986745fa8 in OmniboxEditModel::OnPopupResultChanged D:\chromium\src\components\omnibox\browser\omnibox\_edit\_model.cc:2348  

#4 0x7ff986745244 in OmniboxEditModel::OnCurrentMatchChanged D:\chromium\src\components\omnibox\browser\omnibox\_edit\_model.cc:1819  

#5 0x7ff987c683ac in OmniboxController::OnResultChanged D:\chromium\src\components\omnibox\browser\omnibox\_controller.cc:55  

#6 0x7ff985d1c919 in AutocompleteController::NotifyChanged D:\chromium\src\components\omnibox\browser\autocomplete\_controller.cc:1267  

#7 0x7ff985d1bc81 in AutocompleteController::DelayedNotifyChanged D:\chromium\src\components\omnibox\browser\autocomplete\_controller.cc:1277  

#8 0x7ff985d151e9 in AutocompleteController::UpdateResult D:\chromium\src\components\omnibox\browser\autocomplete\_controller.cc:1046  

#9 0x7ff985d1352b in AutocompleteController::Start D:\chromium\src\components\omnibox\browser\autocomplete\_controller.cc:665  

#10 0x7ff9867356f4 in OmniboxEditModel::StartAutocomplete D:\chromium\src\components\omnibox\browser\omnibox\_edit\_model.cc:697  

#11 0x7ff986733f31 in OmniboxEditModel::UpdateInput D:\chromium\src\components\omnibox\browser\omnibox\_edit\_model.cc:622  

#12 0x7ff986743b75 in OmniboxEditModel::OnAfterPossibleChange D:\chromium\src\components\omnibox\browser\omnibox\_edit\_model.cc:1770  

#13 0x7ff986f87b3f in OmniboxViewViews::OnAfterPossibleChange D:\chromium\src\chrome\browser\ui\views\omnibox\omnibox\_view\_views.cc:941  

#14 0x7ff9a79cf211 in views::Textfield::DoInsertChar D:\chromium\src\ui\views\controls\textfield\textfield.cc:1895  

#15 0x7ff986f8dd09 in OmniboxViewViews::DoInsertChar D:\chromium\src\chrome\browser\ui\views\omnibox\omnibox\_view\_views.cc:1490  

#16 0x7ff9a79cc267 in views::Textfield::InsertChar D:\chromium\src\ui\views\controls\textfield\textfield.cc:1484  

#17 0x7ff910a9508f in ui::InputMethodWinBase::OnChar D:\chromium\src\ui\base\ime\win\input\_method\_win\_base.cc:300  

#18 0x7ff910a95b9b in ui::InputMethodWinBase::ProcessUnhandledKeyEvent D:\chromium\src\ui\base\ime\win\input\_method\_win\_base.cc:510  

#19 0x7ff910a9493b in ui::InputMethodWinBase::DispatchKeyEvent D:\chromium\src\ui\base\ime\win\input\_method\_win\_base.cc:237  

#20 0x7ff98e562d8f in aura::WindowEventDispatcher::PreDispatchKeyEvent D:\chromium\src\ui\aura\window\_event\_dispatcher.cc:1102  

#21 0x7ff98e5606e5 in aura::WindowEventDispatcher::PreDispatchEvent D:\chromium\src\ui\aura\window\_event\_dispatcher.cc:579  

#22 0x7ff9ae6bfc7f in ui::EventDispatcherDelegate::DispatchEvent D:\chromium\src\ui\events\event\_dispatcher.cc:50  

#23 0x7ff9ae6c3d95 in ui::EventProcessor::OnEventFromSource D:\chromium\src\ui\events\event\_processor.cc:56  

#24 0x7ff9ae6c698f in ui::EventSource::DeliverEventToSink D:\chromium\src\ui\events\event\_source.cc:118  

#25 0x7ff9ae6c6613 in ui::EventSource::SendEventToSinkFromRewriter D:\chromium\src\ui\events\event\_source.cc:143  

#26 0x7ff9ae6c6119 in ui::EventSource::SendEventToSink D:\chromium\src\ui\events\event\_source.cc:112  

#27 0x7ff9a7bcce94 in views::DesktopWindowTreeHostWin::HandleKeyEvent D:\chromium\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1062  

#28 0x7ff9a7b3826b in views::HWNDMessageHandler::OnKeyEvent D:\chromium\src\ui\views\win\hwnd\_message\_handler.cc:2043  

#29 0x7ff9a7b3223d in views::HWNDMessageHandler::\_ProcessWindowMessage D:\chromium\src\ui\views\win\hwnd\_message\_handler.h:395  

#30 0x7ff9a7b2f70a in views::HWNDMessageHandler::OnWndProc D:\chromium\src\ui\views\win\hwnd\_message\_handler.cc:1135  

#31 0x7ff9aeae92ed in gfx::WindowImpl::WndProc D:\chromium\src\ui\gfx\win\window\_impl.cc:306  

#32 0x7ff9aeae74b6 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> D:\chromium\src\base\win\wrapped\_window\_proc.h:74  

#33 0x7ff9f6438270 in DispatchMessageW+0x740 (C:\WINDOWS\System32\USER32.dll+0x180018270)  

#34 0x7ff9f6437d30 in DispatchMessageW+0x200 (C:\WINDOWS\System32\USER32.dll+0x180017d30)  

#35 0x7ff9a82c07c7 in base::MessagePumpForUI::ProcessMessageHelper D:\chromium\src\base\message\_loop\message\_pump\_win.cc:531  

#36 0x7ff9a82be4cc in base::MessagePumpForUI::ProcessNextWindowsMessage D:\chromium\src\base\message\_loop\message\_pump\_win.cc:498  

#37 0x7ff9a82bdea7 in base::MessagePumpForUI::DoRunLoop D:\chromium\src\base\message\_loop\message\_pump\_win.cc:209  

#38 0x7ff9a82bb5fc in base::MessagePumpWin::Run D:\chromium\src\base\message\_loop\message\_pump\_win.cc:78  

#39 0x7ff9a81975b0 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:649  

#40 0x7ff9a80859b1 in base::RunLoop::Run D:\chromium\src\base\run\_loop.cc:140  

#41 0x7ff9771937c1 in content::BrowserMainLoop::RunMainMessageLoop D:\chromium\src\content\browser\browser\_main\_loop.cc:1066  

#42 0x7ff97719a935 in content::BrowserMainRunnerImpl::Run D:\chromium\src\content\browser\browser\_main\_runner\_impl.cc:162  

#43 0x7ff97718c3b2 in content::BrowserMain D:\chromium\src\content\browser\browser\_main.cc:32  

#44 0x7ff979b0937b in content::RunBrowserProcessMain D:\chromium\src\content\app\content\_main\_runner\_impl.cc:715  

#45 0x7ff979b0cc9b in content::ContentMainRunnerImpl::RunBrowser D:\chromium\src\content\app\content\_main\_runner\_impl.cc:1266  

#46 0x7ff979b0c427 in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content\_main\_runner\_impl.cc:1120  

#47 0x7ff979b06ed8 in content::RunContentProcess D:\chromium\src\content\app\content\_main.cc:335  

#48 0x7ff979b07d9a in content::ContentMain D:\chromium\src\content\app\content\_main.cc:363  

#49 0x7ff97ceb16a0 in ChromeMain D:\chromium\src\chrome\app\chrome\_main.cc:180  

#50 0x7ff7c3275e3a in MainDllLoader::Launch D:\chromium\src\chrome\app\main\_dll\_loader\_win.cc:166  

#51 0x7ff7c3272a92 in main D:\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#52 0x7ff7c354cb07 in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#53 0x7ff9f52726bc in BaseThreadInitThunk+0x1c (C:\WINDOWS\System32\KERNEL32.DLL+0x1800126bc)  

#54 0x7ff9f67edfb7 in RtlUserThreadStart+0x27 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005dfb7)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: access-violation D:\chromium\src\ui\views\view.cc:536 in views::View::GetPreferredSize

==5580==ADDITIONAL INFO

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 7.0 KB)
- [rep.webm](attachments/rep.webm) (video/webm, 537.3 KB)

## Timeline

### [Deleted User] (2023-02-04)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-02-04)

reproduce video

### m....@gmail.com (2023-02-04)

bisect:
https://chromium-review.googlesource.com/c/chromium/src/+/4126240

### m....@gmail.com (2023-02-04)

Type of crash: [Browser]

### fl...@google.com (2023-02-07)

m.cooolie@, thanks so much for the excellent report; really appreciate the bisection and clear instructions.

Setting Security_Severity-Medium because of the uninitialized memory read in the renderer.

Setting Security-Impact-None because WebUIOmniboxPopup is still an experimental feature.

mahmadi@chromium.org, I'm assigning this to you since it looks like you're most familiar with this part of the codebase.  If you're not the right person to take it on, feel free to reassign.

[Monorail components: UI>Browser>Omnibox]

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-07-21)

Hi Orin, could you please take a look at this?

### or...@chromium.org (2023-07-22)

Right, the original proof of concept code baked into OmniboxViewViews had a bug and I already fixed it during the refactor, here:

[Re-reland [omnibox] Split WebUI impl out from OmniboxPopupViewViews (4620649) · Gerrit Code Review](https://crrev.com/c/4620649)

Thanks for the report, though! ASAN's great!

### [Deleted User] (2023-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-22)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-27)

Congratulations on another one! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-02)

[Empty comment from Monorail migration]

### is...@google.com (2023-11-02)

This issue was migrated from crbug.com/chromium/1412965?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1413953]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062907)*
