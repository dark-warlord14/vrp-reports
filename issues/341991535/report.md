# Security: Container-overflow in STGEverythingMenu::ExecuteCommand

| Field | Value |
|-------|-------|
| **Issue ID** | [341991535](https://issues.chromium.org/issues/341991535) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Linux |
| **Chrome Version** | 125.0.6422.60  |
| **Reporter** | me...@gmail.com |
| **Assignee** | pe...@google.com |
| **Created** | 2024-05-22 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. download asan-linux-release-1303566.zip and unzip
2. start a http server at the folder of poc.html
3. run `./asan-linux-release-1303566/chrome --user-data-dir=/tmp/noexist http://127.0.0.1:8605/poc.html about:blank`
4. add the `poc.html` to TabGroup and then save it. Click the *STGEverythingMenu Button* to show the popup menu, after the `poc.html` is closed, click the saved group in the popup menu.

# Problem Description

## 1. Analysis

The UI of *Saved Group* in the `STGEverythingMenu` is not deleted when the group is closed, we could still access it[1] via click the popup menu, leading to container-overflow.

```
void STGEverythingMenu::ExecuteCommand(int command_id, int event_flags) {
  if (command_id == IDC_CREATE_NEW_TAB_GROUP) {
    base::RecordAction(base::UserMetricsAction(
        "TabGroups_SavedTabGroups_CreateNewGroupTriggeredFromEverythingMenu"));
    browser_->command_controller()->ExecuteCommand(command_id);
  } else {
    base::RecordAction(base::UserMetricsAction(
        "TabGroups_SavedTabGroups_OpenedFromEverythingMenu"));
    const auto* const group = GetTabGroupForCommandId(command_id); // access the deleted group
    if (group->saved_tabs().empty()) {
      return;
    }
    auto* const keyed_service =
        SavedTabGroupServiceFactory::GetForProfile(browser_->profile());
    keyed_service->OpenSavedTabGroupInBrowser(browser_, group->saved_guid());
  }
}

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_everything_menu.cc;l=154>

## 2. Bisect

This problem is introduced in this commit: <https://chromium-review.googlesource.com/c/chromium/src/+/5420175>
This issues affects Chrome Stable 125.0.6422.60

## 3. Suggested Patch

Delete the SavedGroup from popup menu when it is removed.

# Summary

Security: Container-overflow in STGEverythingMenu::ExecuteCommand

# Custom Questions

#### Type of crash:

browser

#### Crash state:

=================================================================
==206051==ERROR: AddressSanitizer: container-overflow on address 0x50d0004efba0 at pc 0x55712d846363 bp 0x7ffcbf6a4770 sp 0x7ffcbf6a4768
READ of size 8 at 0x50d0004efba0 thread T0 (chrome)
#0 0x55712d846362 in empty third\_party/libc++/src/include/vector:602:18
#1 0x55712d846362 in tab\_groups::STGEverythingMenu::ExecuteCommand(int, int) chrome/browser/ui/views/bookmarks/saved\_tab\_groups/saved\_tab\_group\_everything\_menu.cc:155:29
#2 0x7f7800a642e5 in views::internal::MenuRunnerImpl::OnMenuClosed(views::internal::MenuControllerDelegate::NotifyType, views::MenuItemView\*, int) ui/views/controls/menu/menu\_runner\_impl.cc:237:29
#3 0x7f7800a0cf59 in views::MenuController::ExitMenu() ui/views/controls/menu/menu\_controller.cc:3232:13
#4 0x7f7800a13f7f in ReallyAccept ui/views/controls/menu/menu\_controller.cc:1937:3
#5 0x7f7800a13f7f in views::MenuController::Accept(views::MenuItemView\*, int) ui/views/controls/menu/menu\_controller.cc:1917:3
#6 0x7f7800a1bcc2 in views::MenuController::OnKeyPressed(ui::KeyEvent const&) ui/views/controls/menu/menu\_controller.cc:1740:15
#7 0x7f7800a1a5e5 in views::MenuController::OnWillDispatchKeyEvent(ui::KeyEvent\*) ui/views/controls/menu/menu\_controller.cc:1349:19
#8 0x7f781d29c258 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:187:12
#9 0x7f781d29bd78 in ui::EventDispatcher::DispatchEventToEventHandlers(std::\_\_Cr::vector<base::raw\_ptr<ui::EventHandler, (partition\_alloc::internal::RawPtrTraits)1>, std::\_\_Cr::allocator<base::raw\_ptr<ui::EventHandler, (partition\_alloc::internal::RawPtrTraits)1>>>*, ui::Event*) ui/events/event\_dispatcher.cc:174:7
#10 0x7f781d29a628 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:122:3
#11 0x7f781d299eab in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:82:14
#12 0x7f781d299ade in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:54:15
#13 0x7f781d2a04d9 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:72:19
#14 0x7f780e596dd9 in aura::WindowTreeHost::DispatchKeyEventPostIME(ui::KeyEvent\*) ui/aura/window\_tree\_host.cc:309:23
#15 0x7f780fdb5f85 in ui::InputMethodBase::DispatchKeyEventPostIME(ui::KeyEvent\*) const ui/base/ime/input\_method\_base.cc:137:43
#16 0x7f77fad8e907 in ui::InputMethodAuraLinux::DispatchKeyEvent(ui::KeyEvent\*) ui/base/ime/linux/input\_method\_auralinux.cc:210:15
#17 0x7f780e561400 in aura::WindowEventDispatcher::PreDispatchKeyEvent(aura::Window\*, ui::KeyEvent\*) ui/aura/window\_event\_dispatcher.cc:1105:54
#18 0x7f780e55df59 in aura::WindowEventDispatcher::PreDispatchEvent(ui::EventTarget\*, ui::Event\*) ui/aura/window\_event\_dispatcher.cc:562:15
#19 0x7f781d2999d3 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:50:34
#20 0x7f781d2a04d9 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:72:19
#21 0x7f781d2a454b in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:119:16
#22 0x7f781d2a3b63 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:134:12
#23 0x7f780e5a2a50 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:285:38
#24 0x7f7800dd7bab in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event\*) ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_linux.cc:248:29
#25 0x7f7833bb702f in Invoke<void (ui::PlatformWindowDelegate::*)(ui::Event *), ui::PlatformWindowDelegate *, ui::Event *> base/functional/bind\_internal.h:738:12
#26 0x7f7833bb702f in MakeItSo<void (ui::PlatformWindowDelegate::*)(ui::Event *), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> >, ui::Event *> base/functional/bind\_internal.h:930:12
#27 0x7f7833bb702f in RunImpl<void (ui::PlatformWindowDelegate::*)(ui::Event *), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind\_internal.h:1067:14
#28 0x7f7833bb702f in base::internal::Invoker<base::internal::FunctorTraits<void (ui::PlatformWindowDelegate::*&&)(ui::Event*), ui::PlatformWindowDelegate*>, base::internal::BindState<true, true, false, void (ui::PlatformWindowDelegate::*)(ui::Event*), base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void (ui::Event\*)>::RunOnce(base::internal::BindStateBase\*, ui::Event\*) base/functional/bind\_internal.h:980:12
#29 0x7f781d2bf449 in Run base/functional/callback.h:156:12
#30 0x7f781d2bf449 in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ui/events/ozone/events\_ozone.cc:29:25
#31 0x7f7833cb5f49 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/ozone/platform/x11/x11\_window.cc:1399:3
#32 0x7f7833cb54ac in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc:1351:3
#33 0x7f7833cb642f in non-virtual thunk to ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.cc
#34 0x7f78209638f3 in ui::PlatformEventSource::DispatchEvent(ui::Event\*) ui/events/platform/platform\_event\_source.cc:97:29
#35 0x7f77be2b937f in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11\_event\_source.cc:309:5
#36 0x7f77fa8aba4e in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:544:14
#37 0x7f77fa8ab2b5 in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:643:3
#38 0x7f77fa8aa6eb in x11::Connection::Dispatch() ui/gfx/x/connection.cc:521:5
#39 0x7f77be2cb112 in ui::(anonymous namespace)::XSourceDispatch(\_GSource\*, int (*)(void*), void\*) ui/events/platform/x11/x11\_event\_watcher\_glib.cc:57:15
#40 0x7f77bedea04d in g\_main\_context\_dispatch (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x5204d) (BuildId: 2c1d2f9d4a08c71a36797aeb246ab7ae377934ea)

0x50d0004efba0 is located 80 bytes inside of 136-byte region [0x50d0004efb50,0x50d0004efbd8)
allocated by thread T0 (chrome) here:
#0 0x55712280200d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:86:3
#1 0x557125e8b5d0 in \_\_libcpp\_operator\_new<unsigned long> third\_party/libc++/src/include/new:270:10
#2 0x557125e8b5d0 in \_\_libcpp\_allocate third\_party/libc++/src/include/new:294:10
#3 0x557125e8b5d0 in allocate third\_party/libc++/src/include/\_\_memory/allocator.h:119:32
#4 0x557125e8b5d0 in \_\_allocate\_at\_least<std::\_\_Cr::allocator<tab\_groups::SavedTabGroup> > third\_party/libc++/src/include/\_\_memory/allocate\_at\_least.h:41:19
#5 0x557125e8b5d0 in \_\_split\_buffer third\_party/libc++/src/include/\_\_split\_buffer:342:25
#6 0x557125e8b5d0 in std::\_\_Cr::vector<tab\_groups::SavedTabGroup, std::\_\_Cr::allocator<tab\_groups::SavedTabGroup>>::insert(std::\_\_Cr::\_\_wrap\_iter<tab\_groups::SavedTabGroup const\*>, tab\_groups::SavedTabGroup const&) third\_party/libc++/src/include/vector:1596:49
#7 0x557125e7831d in InsertGroupImpl components/saved\_tab\_groups/saved\_tab\_group\_model.cc:648:21
#8 0x557125e7831d in tab\_groups::SavedTabGroupModel::Add(tab\_groups::SavedTabGroup) components/saved\_tab\_groups/saved\_tab\_group\_model.cc:132:3
#9 0x55712cda6a8b in tab\_groups::SavedTabGroupKeyedService::SaveGroup(tab\_groups::TabGroupId const&, bool) chrome/browser/ui/tabs/saved\_tab\_groups/saved\_tab\_group\_keyed\_service.cc:251:10
#10 0x55712e2e58e6 in TabGroupEditorBubbleView::OnSaveTogglePressed() chrome/browser/ui/views/tabs/tab\_group\_editor\_bubble\_view.cc:516:30
#11 0x55712e2e90bd in Invoke<void (TabGroupEditorBubbleView::*)(), TabGroupEditorBubbleView *> base/functional/bind\_internal.h:738:12
#12 0x55712e2e90bd in MakeItSo<void (TabGroupEditorBubbleView::*const &)(), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<TabGroupEditorBubbleView, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> > &> base/functional/bind\_internal.h:930:12
#13 0x55712e2e90bd in RunImpl<void (TabGroupEditorBubbleView::*const &)(), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<TabGroupEditorBubbleView, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> > &, 0UL> base/functional/bind\_internal.h:1067:14
#14 0x55712e2e90bd in base::internal::Invoker<base::internal::FunctorTraits<void (TabGroupEditorBubbleView::* const&)(), TabGroupEditorBubbleView*>, base::internal::BindState<true, true, false, void (TabGroupEditorBubbleView::*)(), base::internal::UnretainedWrapper<TabGroupEditorBubbleView, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void ()>::Run(base::internal::BindStateBase*) base/functional/bind\_internal.h:987:12
#15 0x7f780088d1da in base::RepeatingCallback<void ()>::Run() const & base/functional/callback.h:344:12
#16 0x7f780095e4aa in operator() ui/views/controls/button/button.cc:134:63
#17 0x7f780095e4aa in \_\_invoke<base::Overloaded<(lambda at ../../ui/views/controls/button/button.cc:133:11), (lambda at ../../ui/views/controls/button/button.cc:134:11), (lambda at ../../ui/views/controls/button/button.cc:135:11)>, base::RepeatingCallback<void ()> &> third\_party/libc++/src/include/\_\_type\_traits/invoke.h:150:25
#18 0x7f780095e4aa in invoke<base::Overloaded<(lambda at ../../ui/views/controls/button/button.cc:133:11), (lambda at ../../ui/views/controls/button/button.cc:134:11), (lambda at ../../ui/views/controls/button/button.cc:135:11)>, base::RepeatingCallback<void ()> &> third\_party/libc++/src/include/\_\_functional/invoke.h:28:10
#19 0x7f780095e4aa in Run<0UL, 1UL> third\_party/abseil-cpp/absl/types/internal/variant.h:922:12
#20 0x7f780095e4aa in operator()<1UL> third\_party/abseil-cpp/absl/types/internal/variant.h:910:12
#21 0x7f780095e4aa in \_\_invoke<absl::variant\_internal::PerformVisitation<base::Overloaded<(lambda at ../../ui/views/controls/button/button.cc:133:11), (lambda at ../../ui/views/controls/button/button.cc:134:11), (lambda at ../../ui/views/controls/button/button.cc:135:11)>, absl::variant<base::OnceCallback<void ()>, base::RepeatingCallback<void ()>, base::RepeatingCallback<void (const ui::Event &)> > &>, std::\_\_Cr::integral\_constant<unsigned long, 1UL> > third\_party/libc++/src/include/\_\_type\_traits/invoke.h:150:25
#22 0x7f780095e4aa in invoke<absl::variant\_internal::PerformVisitation<base::Overloaded<(lambda at ../../ui/views/controls/button/button.cc:133:11), (lambda at ../../ui/views/controls/button/button.cc:134:11), (lambda at ../../ui/views/controls/button/button.cc:135:11)>, absl::variant<base::OnceCallback<void ()>, base::RepeatingCallback<void ()>, base::RepeatingCallback<void (const ui::Event &)> > &>, std::\_\_Cr::integral\_constant<unsigned long, 1UL> > third\_party/libc++/src/include/\_\_functional/invoke.h:28:10
#23 0x7f780095e4aa in Run third\_party/abseil-cpp/absl/types/internal/variant.h:296:12
#24 0x7f780095e4aa in Run<absl::variant\_internal::PerformVisitation<base::Overloaded<(lambda at ../../ui/views/controls/button/button.cc:133:11), (lambda at ../../ui/views/controls/button/button.cc:134:11), (lambda at ../../ui/views/controls/button/button.cc:135:11)>, absl::variant<base::OnceCallback<void ()>, base::RepeatingCallback<void ()>, base::RepeatingCallback<void (const ui::Event &)> > &> > third\_party/abseil-cpp/absl/types/internal/variant.h:363:16
#25 0x7f780095e4aa in visit<base::Overloaded<(lambda at ../../ui/views/controls/button/button.cc:133:11), (lambda at ../../ui/views/controls/button/button.cc:134:11), (lambda at ../../ui/views/controls/button/button.cc:135:11)>, absl::variant<base::OnceCallback<void ()>, base::RepeatingCallback<void ()>, base::RepeatingCallback<void (const ui::Event &)> > &> third\_party/abseil-cpp/absl/types/variant.h:428:10
#26 0x7f780095e4aa in views::Button::PressedCallback::Run(ui::Event const&) ui/views/controls/button/button.cc:131:10
#27 0x7f7800965c89 in views::Button::NotifyClick(ui::Event const&) ui/views/controls/button/button.cc:737:15
#28 0x7f780096e64d in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ui/views/controls/button/button\_controller.cc
#29 0x7f781d2b4eb2 in ui::ScopedTargetHandler::OnEvent(ui::Event\*) ui/events/scoped\_target\_handler.cc:30:24
#30 0x7f781d29c258 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:187:12
#31 0x7f781d29a91f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:136:5
#32 0x7f781d299eab in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:82:14
#33 0x7f781d299ade in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:54:15
#34 0x7f7800cb8370 in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ui/views/widget/root\_view.cc:557:9
#35 0x7f7800cf3fd6 in views::Widget::OnMouseEvent(ui::MouseEvent\*) ui/views/widget/widget.cc:1846:20
#36 0x7f7800d9c9b4 in views::NativeWidgetAura::OnMouseEvent(ui::MouseEvent\*) ui/views/widget/native\_widget\_aura.cc
#37 0x7f781d29c258 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:187:12
#38 0x7f781d29a91f in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:136:5
#39 0x7f781d299eab in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:82:14
#40 0x7f781d299ade in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:54:15
#41 0x7f781d2a04d9 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:72:19
#42 0x7f781d2a454b in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:119:16
#43 0x7f781d2a3b63 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:134:12
#44 0x7f780e5a2a50 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:285:38
#45 0x7f7800dd7bab in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event\*) ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_linux.cc:248:29
#46 0x7f7833bb702f in Invoke<void (ui::PlatformWindowDelegate::*)(ui::Event *), ui::PlatformWindowDelegate *, ui::Event *> base/functional/bind\_internal.h:738:12
#47 0x7f7833bb702f in MakeItSo<void (ui::PlatformWindowDelegate::*)(ui::Event *), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> >, ui::Event *> base/functional/bind\_internal.h:930:12
#48 0x7f7833bb702f in RunImpl<void (ui::PlatformWindowDelegate::*)(ui::Event *), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> >, 0UL> base/functional/bind\_internal.h:1067:14
#49 0x7f7833bb702f in base::internal::Invoker<base::internal::FunctorTraits<void (ui::PlatformWindowDelegate::*&&)(ui::Event*), ui::PlatformWindowDelegate*>, base::internal::BindState<true, true, false, void (ui::PlatformWindowDelegate::*)(ui::Event*), base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, void (ui::Event\*)>::RunOnce(base::internal::BindStateBase\*, ui::Event\*) base/functional/bind\_internal.h:980:12
#50 0x7f781d2bf75e in Run base/functional/callback.h:156:12
#51 0x7f781d2bf75e in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ui/events/ozone/events\_ozone.cc:37:25
#52 0x7f7833cb5f49 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/ozone/platform/x11/x11\_window.cc:1399:3

HINT: if you don't care about these errors you may set ASAN\_OPTIONS=detect\_container\_overflow=0.
If you suspect a false positive see also: <https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow>.
SUMMARY: AddressSanitizer: container-overflow third\_party/libc++/src/include/vector:602:18 in empty
Shadow bytes around the buggy address:
0x50d0004ef900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
0x50d0004ef980: fa fa fa fa f7 fa fd fd fd fd fd fd fd fd fd fd
0x50d0004efa00: fd fd fd fd fd fd fd fd fa fa fa fa fa fa f7 fa
0x50d0004efa80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
0x50d0004efb00: fa fa fa fa fa fa fa fa f7 fa fc fc fc fc fc fc
=>0x50d0004efb80: fc fc fc fc[fc]fc fc fc fc fc fc fa fa fa fa fa
0x50d0004efc00: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fd fd
0x50d0004efc80: fd fd fd fd fd fd fa fa fa fa fa fa f7 fa fd fd
0x50d0004efd00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
0x50d0004efd80: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd
0x50d0004efe00: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
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

==206051==ADDITIONAL INFO

==206051==Note: Please include this section with the ASan report.
Task trace:

==206051==END OF ADDITIONAL INFO
==206051==ABORTING

#### Reporter credit:

Weipeng Jiang (@Krace) of VRI

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- poc.html (text/html, 121 B)
- video.webm (video/webm, 719.0 KB)

## Timeline

### ps...@google.com (2024-05-22)

I was able to reproduce this on the current asan Linux build.  I am triaging as high severity.
pengchaocai: Assigning over to you as it looks like you as https://chromium-review.googlesource.com/c/chromium/src/+/5420175 does seem to most likely candidate for this issue. Could you please take a look? 

### pe...@google.com (2024-05-22)

Setting milestone because of s0/s1 severity.

### ap...@google.com (2024-05-30)

Project: chromium/src
Branch: main

commit 5430fda85bc85c4dd9dc92fbe6c892c86373d7d7
Author: Pengchao Cai <pengchaocai@chromium.org>
Date:   Thu May 30 18:05:16 2024

    [tab group v2] Avoid accessing deleted group in menus
    
    While the Everything menu and/or context menus are open, it's possible
    that some saved tab groups get deleted remotely, leading to the menus
    displaying stale tab groups. Executing these menu commands are now
    dangerous.
    
    This CL audited all the commands that could potentially crash and added
    necessary runtime checks.
    
    Also replaced pointer references to saved tab groups with Uuids since
    dereferencing those pointers to deleted groups may become undefined.
    
    Change-Id: I2defb212ea42cde318a1ddfaa3b8726eae092510
    Bug: 341991535
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5560557
    Reviewed-by: Darryl James <dljames@chromium.org>
    Commit-Queue: pengchao Cai <pengchaocai@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1308133}

M       chrome/browser/ui/tabs/saved_tab_groups/saved_tab_group_utils.cc
M       chrome/browser/ui/tabs/saved_tab_groups/saved_tab_group_utils.h
M       chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_everything_menu.cc
M       chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_everything_menu.h

https://chromium-review.googlesource.com/5560557


### pe...@google.com (2024-05-31)

Requesting merge to stable (M125) because latest trunk commit (1308133) appears to be after stable branch point (1287751).
Requesting merge to beta (M126) because latest trunk commit (1308133) appears to be after beta branch point (1300313).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-05-31)

I don't think it's necessary to merge the fix into M125 since the feature is behind a flag and the flag is off until M126.

Answer to the questions: 
1,  https://chromium-review.googlesource.com/c/chromium/src/+/5560557
2,  yes
3, no
4, no
5, no

### pe...@google.com (2024-05-31)

Merge review required: M126 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-05-31)

Merge review required: M125 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-05-31)

1, security fix
2, https://chromium-review.googlesource.com/c/chromium/src/+/5560557
3, yes
4, yes, and yes it's behind a finch flag and experiments active in canary dev and beta
5, n/a
6, n/a

### pg...@google.com (2024-06-05)

The fix is a bit involved, but the fix has been sitting in canary for a good long while and canary looks good - nothing relevant to be seen.

Merge approved for M126! Please merge the fix to branch 6478 by Thursday June 13th EOD MTV time to get this fix into the next stable respin

Thanks for your patience here through all the repeated questionnaires (:

### sp...@google.com (2024-06-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$2,000 for report of heavily mitigated memory corruption in a non-sandboxed process + $1,000 bisect bonus 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-05)

Congratulations Krace! Nice to see a report from you. Thank you for your efforts and reporting this issue to us!

### ap...@google.com (2024-06-06)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 43e3878d646048c898f9e10e429285e5cbb3e37a
Author: Pengchao Cai <pengchaocai@chromium.org>
Date:   Thu Jun 06 18:51:03 2024

    [M126][tab group v2] Avoid accessing deleted group in menus
    
    While the Everything menu and/or context menus are open, it's possible
    that some saved tab groups get deleted remotely, leading to the menus
    displaying stale tab groups. Executing these menu commands are now
    dangerous.
    
    This CL audited all the commands that could potentially crash and added
    necessary runtime checks.
    
    Also replaced pointer references to saved tab groups with Uuids since
    dereferencing those pointers to deleted groups may become undefined.
    
    (cherry picked from commit 5430fda85bc85c4dd9dc92fbe6c892c86373d7d7)
    
    Change-Id: I2defb212ea42cde318a1ddfaa3b8726eae092510
    Bug: 341991535
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5560557
    Reviewed-by: Darryl James <dljames@chromium.org>
    Commit-Queue: pengchao Cai <pengchaocai@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1308133}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5601724
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6478@{#1238}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       chrome/browser/ui/tabs/saved_tab_groups/saved_tab_group_utils.cc
M       chrome/browser/ui/tabs/saved_tab_groups/saved_tab_group_utils.h
M       chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_everything_menu.cc
M       chrome/browser/ui/views/bookmarks/saved_tab_groups/saved_tab_group_everything_menu.h

https://chromium-review.googlesource.com/5601724


### pe...@google.com (2024-09-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/341991535)*
