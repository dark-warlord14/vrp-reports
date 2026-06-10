# Heap use-after-free in ClipboardOzone on Linux/X11 when pasting into the omnibox

| Field | Value |
|-------|-------|
| **Issue ID** | [482711647](https://issues.chromium.org/issues/482711647) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Ozone |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | po...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2026-02-08 |
| **Bounty** | Confirmed (amount unknown) |

## Description

---

### Report description

Heap use-after-free in ClipboardOzone on Linux/X11 when pasting into the omnibox

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/>

---

### The problem

#### Please describe the technical details of the vulnerability

#### 1. technical details

On Linux/X11 builds using Ozone, the synchronous clipboard read path in `ui::ClipboardOzone` returns a `base::span<uint8_t>` that can outlive the underlying heap buffer.

The helper class `ClipboardOzone::AsyncClipboardOzone` provides a synchronous wrapper around the asynchronous `PlatformClipboard::RequestClipboardData` API. In the non-owner (“slow path”) case, it constructs a `base::span` over the contents of a `scoped_refptr<base::RefCountedBytes>` that is held only by a local variable:

```
// ui/base/clipboard/clipboard_ozone.cc
base::span<uint8_t> ReadClipboardDataAndWait(ClipboardBuffer buffer,
                                             const std::string& mime_type) {
  if (buffer == ClipboardBuffer::kSelection && !IsSelectionBufferAvailable())
    return {};

  // Fast path: safe, backed by member offered_data_.
  if (platform_clipboard_->IsSelectionOwner(buffer)) {
    auto it = offered_data_[buffer].find(mime_type);
    if (it == offered_data_[buffer].end())
      return {};
    return base::span(it->second->as_vector());
  }

  // Slow path: unsafe, 'data' is a local scoped_refptr.
  if (auto data = Read(buffer, mime_type))
    return base::span(data->as_vector());

  return {};
}

```

Here, `PlatformClipboard::Data` is defined as:

```
// ui/ozone/public/platform_clipboard.h
using Data = scoped_refptr<base::RefCountedBytes>;

```

The `Read()` helper wraps the asynchronous platform call using a stack-allocated `Request<PlatformClipboard::Data>`:

```
// ui/base/clipboard/clipboard_ozone.cc
PlatformClipboard::Data Read(ClipboardBuffer buffer,
                             const std::string& mime_type) {
  using ReadRequest = Request<PlatformClipboard::Data>;
  ReadRequest request;
  platform_clipboard_->RequestClipboardData(
      buffer, mime_type,
      base::BindOnce(&ReadRequest::Finish, request.GetWeakPtr()));
  return request.TakeResultSync();
}

```

On X11/Ozone, `RequestClipboardData()` ultimately allocates a fresh `RefCountedBytes` and returns it only via this callback:

```
// ui/ozone/platform/x11/x11_clipboard_ozone.cc
void X11ClipboardOzone::RequestClipboardData(
    ClipboardBuffer buffer,
    const std::string& mime_type,
    PlatformClipboard::RequestDataClosure callback) {
  auto atoms = mime_type == kMimeTypePlainText
                   ? helper_->GetTextAtoms()
                   : helper_->GetAtomsForFormat(
                         ClipboardFormatType::CustomPlatformType(mime_type));
  auto selection_data = helper_->Read(buffer, atoms);
  std::move(callback).Run(selection_data.TakeBytes());
}

// ui/base/x/selection_utils.cc
scoped_refptr<base::RefCountedBytes> SelectionData::TakeBytes() {
  if (!memory_.get())
    return nullptr;
  auto* memory = memory_.release();
  return base::MakeRefCounted<base::RefCountedBytes>(*memory);
}

```

In the slow path of `ReadClipboardDataAndWait()`:

- `Read()` returns a `PlatformClipboard::Data` into the local variable `data`.
- `base::span(data->as_vector())` is returned to the caller.
- On function return, `data` is destroyed; if it held the last reference, the `RefCountedBytes` and its internal `std::vector<unsigned char>` are freed.
- The caller keeps using the returned `base::span<uint8_t>`, which now points to freed memory.

The synchronous text read path in `ClipboardOzone` uses this span after `ReadClipboardDataAndWait()` returns:

```
// ui/base/clipboard/clipboard_ozone.cc
void ClipboardOzone::ReadText(ClipboardBuffer buffer,
                              const DataTransferEndpoint* data_dst,
                              std::u16string* result) const {
  DCHECK(CalledOnValidThread());
  auto clipboard_data = async_clipboard_ozone_->ReadClipboardDataAndWait(
      buffer, kMimeTypePlainText);

  if (!IsReadAllowed(GetSource(buffer), data_dst, clipboard_data))
    return;

  RecordRead(ClipboardFormatMetric::kText);
  *result = base::UTF8ToUTF16(std::string_view(
      reinterpret_cast<char*>(clipboard_data.data()), clipboard_data.size()));
}

```

When the process is not the selection owner, this path uses the dangling `clipboard_data` span to construct a `std::string_view` and passes it into `base::UTF8ToUTF16`, which calls `IsStringASCII` on freed heap memory. This matches the ASan report:

- Read at `base::internal::DoIsStringASCII<char>()` / `base::UTF8ToUTF16()`.
- Caller: `ui::ClipboardOzone::ReadText` → `GetClipboardText` → `OmniboxViewViews::OnOmniboxPaste`.
- Freed from `base::RefCountedBytes::~RefCountedBytes()` in `AsyncClipboardOzone::ReadClipboardDataAndWait`.
- `MiraclePtr Status: NOT PROTECTED`.

The fast path inside `ReadClipboardDataAndWait()` (`IsSelectionOwner(buffer) == true`) is safe because it uses `offered_data_`, a member `flat_map<ClipboardBuffer, PlatformClipboard::DataMap>` whose `PlatformClipboard::Data` entries outlive the function call.

#### 2. vulnerability reproduction

Preconditions:

- Debian 12 environment.
- Linux build of Chromium/Chrome using Ozone with the X11 platform (`--ozone-platform=x11`).
- ASan-instrumented component build generated via:
  - `gn gen out/asan_debug --args=\"is_debug=true is_component_build=true is_asan=true\"`

Reproduction steps (high level):

1. Build and launch the ASan-instrumented browser:
   - `ASAN_OPTIONS=detect_odr_violation=0 ./chrome --ozone-platform=x11`
2. Use a web page or any other method to place attacker-controlled UTF-8 text onto the system clipboard (for example, by selecting and copying crafted text).
3. Focus the omnibox (address bar) and trigger the paste action (e.g., `Ctrl+V`).
4. Observe that the browser process crashes with an ASan heap-use-after-free report in `base::internal::DoIsStringASCII<char>()`, with a stack that includes:
   - `ui::ClipboardOzone::ReadText`
   - `chrome::GetClipboardText` (omnibox helper)
   - `OmniboxViewViews::OnOmniboxPaste`
   - `AsyncClipboardOzone::ReadClipboardDataAndWait`
     and the report notes `MiraclePtr Status: NOT PROTECTED`.

The crash reproduces reliably when the clipboard selection is owned by another application or by the compositor (so that the slow path of `ReadClipboardDataAndWait()` is used).

#### Impact analysis

On supported Linux/X11 builds of Chrome/Chromium using Ozone, a malicious website that can influence clipboard contents and convince a user to copy from the page and paste into the omnibox can reliably trigger a heap use-after-free in the browser (non-sandboxed) process.

In the current proof of concept, exploitation yields:

- A deterministic heap use-after-free and memory corruption in the browser process during UTF-8 to UTF-16 conversion of clipboard text.
- A reproducible browser process crash (denial of service) under ASan.

---

### The cause

#### What version of Chrome have you found the security issue in?

146.0.7666.1/stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

Povcfe of Tencent Security Xuanwu Lab

## Attachments

- [clipboard_ozone_uaf.mp4](attachments/clipboard_ozone_uaf.mp4) (video/mp4, 19.8 MB)
- [clipboard_ozone_uaf.log](attachments/clipboard_ozone_uaf.log) (application/octet-stream, 23.9 KB)

## Timeline

### po...@gmail.com (2026-02-08)

#### patch

```
diff --git a/ui/base/clipboard/clipboard_ozone.cc b/ui/base/clipboard/clipboard_ozone.cc
--- a/ui/base/clipboard/clipboard_ozone.cc
+++ b/ui/base/clipboard/clipboard_ozone.cc
@@ -277,21 +277,29 @@
 	    return DataTransferEndpoint(std::move(url));
 	  }
 
-	  base::span<uint8_t> ReadClipboardDataAndWait(ClipboardBuffer buffer,
-	                                               const std::string& mime_type) {
+	  // Synchronous helper that returns an owning copy of the clipboard bytes for
+	  // the given buffer and MIME type. Returning an owning container here avoids
+	  // exposing spans to storage whose lifetime is tied to local
+	  // scoped_refptr<RefCountedBytes> instances.
+	  std::vector<uint8_t> ReadClipboardDataAndWait(ClipboardBuffer buffer,
+	                                                const std::string& mime_type) {
 	    if (buffer == ClipboardBuffer::kSelection && !IsSelectionBufferAvailable())
 	      return {};
 
 	    // We can use a fastpath if we are the owner of the selection.
 	    if (platform_clipboard_->IsSelectionOwner(buffer)) {
 	      auto it = offered_data_[buffer].find(mime_type);
 	      if (it == offered_data_[buffer].end())
 	        return {};
-	      return base::span(it->second->as_vector());
+	      const auto& vec = it->second->as_vector();
+	      return std::vector<uint8_t>(vec.begin(), vec.end());
 	    }
 
-	    if (auto data = Read(buffer, mime_type))
-	      return base::span(data->as_vector());
+	    if (auto data = Read(buffer, mime_type)) {
+	      const auto& vec = data->as_vector();
+	      return std::vector<uint8_t>(vec.begin(), vec.end());
+	    }
 
 	    return {};
 	  }


```

### th...@chromium.org (2026-02-10)

I'm not able to repro the issue. Your report mentions attacker-controlled text. Is there any particular text I'm supposed to use to repro?

```
thomasanderson@tomanderson:~/dev/chromium_1/src$ git rev-parse HEAD
0375a482aa9a493c3c6f82e7574305a6e7e74f51
thomasanderson@tomanderson:~/dev/chromium_1/src$ cat out/asan_debug/args.gn
is_debug = true
is_component_build = true
is_asan = true
use_remoteexec = true
thomasanderson@tomanderson:~/dev/chromium_1/src$ echo $XDG_CURRENT_DESKTOP
GNOME
thomasanderson@tomanderson:~/dev/chromium_1/src$ echo $XDG_SESSION_TYPE
x11
thomasanderson@tomanderson:~/dev/chromium_1/src$ ASAN_OPTIONS=detect_odr_violation=0 out/asan_debug/chrome --ozone-platform=x11

```

### po...@gmail.com (2026-02-10)

Any content will do, just make sure there is content in the clipboard, and then copying the content into the URL address bar will trigger it.

My reproduction environment is the default desktop of Debian 12. If you need more information, please contact me.

### po...@gmail.com (2026-02-10)

I might know where the problem is. You should try pasting content into Chrome’s URL bar from outside of Chrome. For
example, I copied a piece of text (<https://google.com>) from the terminal, and when I used Ctrl+V to paste it into
Chrome’s URL bar, it triggered a crash.

### th...@chromium.org (2026-02-10)

I'm not able to repro with text copied from external apps. Does the issue still repro for you on ToT?

### ts...@google.com (2026-02-10)

I am unable to repo as well on Linux 299d726057a74a4cd83d1bfef23d5079aa88b035

### po...@gmail.com (2026-02-10)

Yes, I'm using the latest tag 146.0.7666.1 compiled with ASAN, and whenever I copy external content into the URL address bar, it consistently triggers the issue.

I analyzed the problem, implemented a patch, and then the issue no longer occurs.

### po...@gmail.com (2026-02-10)

Maybe I could try making a Docker. I'll give it a shot.

### po...@gmail.com (2026-02-10)

By the way, can you possibly see, through the debugging process, whether Chrome can execute the code near the location indicated by the ASAN log?

### pe...@google.com (2026-02-10)

Thank you for providing more feedback. Adding the requester to the CC list.

### th...@chromium.org (2026-02-11)

Re [comment#10](https://issues.chromium.org/issues/482711647#comment10): Yes, I see that `ReadClipboardDataAndWait` is getting hit on my build.

### el...@chromium.org (2026-02-11)

This is Needs-Feedback from us because we still can't repro this locally.

### po...@gmail.com (2026-02-12)

I don’t think our Linux environment should affect reproducing the vulnerability. On version 146.0.7666.1 built with
ASan, I can reliably reproduce this issue by copying external content into the URL address bar. I saw that when you
tried to reproduce the vulnerability, your setup was not the same as mine, so I pulled the latest 147.0.7683.1 code,
and in my tests this time I did not see a UAF crash. So we can consider that the vulnerability does not exist in the
version you are using. If you want to reproduce this issue, please keep your setup consistent with mine; or, if you
believe it has already been fixed in the latest version, you can ignore it.

### pe...@google.com (2026-02-12)

Thank you for providing more feedback. Adding the requester to the CC list.

### ja...@chromium.org (2026-02-13)

Thanks for the information bug reporter.

I was able to reproduce the issue from the original report and instructions. All I had to do was right click in the omnibox. I'll try to bisect when it got fixed. The crash output is here:

```
$ git checkout 146.0.7666.1
$ autoninja -C out/asan chrome
$ ASAN_OPTIONS=detect_odr_violation=0 ./out/asan/chrome --ozone-platform=x11 --user-data-dir=`mktemp -d`

==264673==ERROR: AddressSanitizer: heap-use-after-free on address 0x7c0c3a51a190 at pc 0x7fcd9fdc7849 bp 0x7ffffaa308e0 sp 0x7ffffaa308d8
READ of size 8 at 0x7c0c3a51a190 thread T0 (chrome)
    #0 0x7fcd9fdc7848 in bool base::internal::DoIsStringASCII<char>(char const*, unsigned long) base/strings/string_util_impl_helpers.h:204:22
    #1 0x7fcd9fdbe623 in base::IsStringASCII(std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>) base/strings/string_util.cc:241:10
    #2 0x7fcd9fdeeed0 in bool base::(anonymous namespace)::UTFConversion<std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>, std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t>>>(std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>> const&, std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t>>*) base/strings/utf_string_conversions.cc:201:7
    #3 0x7fcd9fdeed6c in base::UTF8ToUTF16(char const*, unsigned long, std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t>>*) base/strings/utf_string_conversions.cc:230:10
    #4 0x7fcd9fdef16a in base::UTF8ToUTF16(std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>) base/strings/utf_string_conversions.cc:237:3
    #5 0x7fcd71989d88 in ui::ClipboardOzone::ReadText(ui::ClipboardBuffer, ui::DataTransferEndpoint const*, std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t>>*) const ui/base/clipboard/clipboard_ozone.cc:784:13
    #6 0x55e1789ac496 in GetClipboardText(bool) chrome/browser/ui/omnibox/clipboard_utils.cc:54:16
    #7 0x55e18aa59e5f in OmniboxViewViews::GetLabelForCommandId(int) const chrome/browser/ui/views/omnibox/omnibox_view_views.cc:1365:7
    #8 0x55e18aa5a2fc in non-virtual thunk to OmniboxViewViews::GetLabelForCommandId(int) const chrome/browser/ui/views/omnibox/omnibox_view_views.cc
    #9 0x7fcd9b4ce71e in ui::SimpleMenuModel::GetLabelAt(unsigned long) const ui/menus/simple_menu_model.cc:452:23
    #10 0x7fcd1563175b in views::MenuModelAdapter::AddMenuItemFromModelAt(ui::MenuModel*, unsigned long, views::MenuItemView*, unsigned long, int) ui/views/controls/menu/menu_model_adapter.cc:132:35
    #11 0x7fcd156320cd in views::MenuModelAdapter::AppendMenuItemFromModel(ui::MenuModel*, unsigned long, views::MenuItemView*, int) ui/views/controls/menu/menu_model_adapter.cc:165:10
    #12 0x7fcd1563217b in views::MenuModelAdapter::AppendMenuItem(views::MenuItemView*, ui::MenuModel*, unsigned long) ui/views/controls/menu/menu_model_adapter.cc:171:10
    #13 0x7fcd156300be in views::MenuModelAdapter::BuildMenuImpl(views::MenuItemView*, ui::MenuModel*) ui/views/controls/menu/menu_model_adapter.cc:305:32
    #14 0x7fcd1562fad4 in views::MenuModelAdapter::BuildMenu(views::MenuItemView*) ui/views/controls/menu/menu_model_adapter.cc:60:3
    #15 0x7fcd15630773 in views::MenuModelAdapter::CreateMenu() ui/views/controls/menu/menu_model_adapter.cc:67:3
    #16 0x7fcd15642f70 in views::internal::MenuRunnerImplAdapter::MenuRunnerImplAdapter(ui::MenuModel*, base::RepeatingCallback<void ()>) ui/views/controls/menu/menu_runner_impl_adapter.cc:20:53
    #17 0x7fcd1563bb54 in views::internal::MenuRunnerImplInterface::Create(ui::MenuModel*, int, base::RepeatingCallback<void ()>) ui/views/controls/menu/menu_runner_impl.cc:69:14
    #18 0x7fcd1563a0aa in views::MenuRunner::MenuRunner(ui::MenuModel*, int, base::RepeatingCallback<void ()>) ui/views/controls/menu/menu_runner.cc:25:13
    #19 0x7fcd1557e8bd in std::__Cr::unique_ptr<views::MenuRunner, std::__Cr::default_delete<views::MenuRunner>> std::__Cr::make_unique<views::MenuRunner, ui::SimpleMenuModel*, int, 0>(ui::SimpleMenuModel*&&, int&&) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:30
    #20 0x7fcd157e3c60 in views::Textfield::UpdateContextMenu() ui/views/controls/textfield/textfield.cc:3068:26
    #21 0x7fcd157e36a3 in views::Textfield::ShowContextMenuForViewImpl(views::View*, gfx::Point const&, ui::mojom::MenuSourceType) ui/views/controls/textfield/textfield.cc:1262:3
    #22 0x7fcd1546bbce in views::ContextMenuController::ShowContextMenuForView(views::View*, gfx::Point const&, ui::mojom::MenuSourceType) ui/views/context_menu_controller.cc:30:3
    #23 0x7fcd159e0fcf in views::View::ShowContextMenu(gfx::Point const&, ui::mojom::MenuSourceType) ui/views/view.cc:2171:29
    #24 0x7fcd159dbff9 in views::View::ProcessMousePressed(ui::MouseEvent const&) ui/views/view.cc:3793:7
    #25 0x7fcd159db902 in views::View::OnMouseEvent(ui::MouseEvent*) ui/views/view.cc:1741:11
    #26 0x7fcd93f45477 in ui::EventHandler::OnEvent(ui::Event*) ui/events/event_handler.cc:36:5
    #27 0x7fcd159db746 in views::View::OnEvent(ui::Event*) ui/views/view.cc:1726:21
    #28 0x7fcd93f3683c in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:189:12
    #29 0x7fcd93f3583c in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:138:5
    #30 0x7fcd93f3509c in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:84:14
    #31 0x7fcd93f34be3 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15
    #32 0x7fcd15a53788 in views::internal::RootView::OnMousePressed(ui::MouseEvent const&) ui/views/widget/root_view.cc:557:9
    #33 0x7fcd15a87c7e in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:2135:35
    #34 0x7fcd15c01d36 in views::DesktopNativeWidgetAura::OnMouseEvent(ui::MouseEvent*) ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:1445:30
    #35 0x7fcd93f45477 in ui::EventHandler::OnEvent(ui::Event*) ui/events/event_handler.cc:36:5
    #36 0x7fcd93f3683c in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:189:12
    #37 0x7fcd93f3583c in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:138:5
    #38 0x7fcd93f3509c in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:84:14
    #39 0x7fcd93f34be3 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15
    #40 0x7fcd93f47e21 in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:72:19
    #41 0x7fcd93f487f0 in non-virtual thunk to ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc
    #42 0x7fcd93f4d018 in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:119:16
    #43 0x7fcd93f4cacc in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:134:12
    #44 0x7fcd93f4c720 in ui::EventSource::SendEventToSink(ui::Event const*) ui/events/event_source.cc:113:10
    #45 0x7fcd4ac591f0 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event*) ui/aura/window_tree_host_platform.cc:300:38
    #46 0x7fcd15c1136e in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event*) ui/views/widget/desktop_aura/desktop_window_tree_host_linux.cc:250:29
    #47 0x7fcda280217b in void base::internal::DecayedFunctorTraits<void (ui::PlatformWindowDelegate::*)(ui::Event*), ui::PlatformWindowDelegate*>::Invoke<void (ui::PlatformWindowDelegate::*)(ui::Event*), ui::PlatformWindowDelegate*, ui::Event*>(void (ui::PlatformWindowDelegate::*)(ui::Event*), ui::PlatformWindowDelegate*&&, ui::Event*&&) base/functional/bind_internal.h:740:12
    #48 0x7fcda2801f14 in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (ui::PlatformWindowDelegate::*&&)(ui::Event*), ui::PlatformWindowDelegate*>, void, 0ul>::MakeItSo<void (ui::PlatformWindowDelegate::*)(ui::Event*), std::__Cr::tuple<base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, ui::Event*>(void (ui::PlatformWindowDelegate::*&&)(ui::Event*), std::__Cr::tuple<base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, ui::Event*&&) base/functional/bind_internal.h:932:12
    #49 0x7fcda2801cac in void base::internal::Invoker<base::internal::FunctorTraits<void (ui::PlatformWindowDelegate::*&&)(ui::Event*), ui::PlatformWindowDelegate*>, base::internal::BindState<true, true, false, void (ui::PlatformWindowDelegate::*)(ui::Event*), base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (ui::Event*)>::RunImpl<void (ui::PlatformWindowDelegate::*)(ui::Event*), std::__Cr::tuple<base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(void (ui::PlatformWindowDelegate::*&&)(ui::Event*), std::__Cr::tuple<base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>, ui::Event*&&) base/functional/bind_internal.h:1069:14
    #50 0x7fcda2801aa6 in base::internal::Invoker<base::internal::FunctorTraits<void (ui::PlatformWindowDelegate::*&&)(ui::Event*), ui::PlatformWindowDelegate*>, base::internal::BindState<true, true, false, void (ui::PlatformWindowDelegate::*)(ui::Event*), base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (ui::Event*)>::RunOnce(base::internal::BindStateBase*, ui::Event*) base/functional/bind_internal.h:982:12
    #51 0x7fcd93f9943a in base::OnceCallback<void (ui::Event*)>::Run(ui::Event*) && base/functional/callback.h:155:12
    #52 0x7fcd93f98494 in ui::DispatchEventFromNativeUiEvent(ui::Event* const&, base::OnceCallback<void (ui::Event*)>) ui/events/ozone/events_ozone.cc:37:25
    #53 0x7fcda2b441a4 in ui::X11Window::DispatchUiEvent(ui::Event*, x11::Event const&) ui/ozone/platform/x11/x11_window.cc:1421:3
    #54 0x7fcda2b4350f in ui::X11Window::DispatchEvent(ui::Event* const&) ui/ozone/platform/x11/x11_window.cc:1372:3
    #55 0x7fcd9c4fb406 in ui::PlatformEventSource::DispatchEvent(ui::Event*) ui/events/platform/platform_event_source.cc:93:29
    #56 0x7fccc11af192 in ui::X11EventSource::OnEvent(x11::Event const&) ui/events/platform/x11/x11_event_source.cc:301:5
    #57 0x7fcc63443067 in std::__Cr::__invoke_result_impl<void, void (x11::EventObserver::*&)(x11::Event const&), x11::EventObserver&, x11::Event const&>::type std::__Cr::__invoke<void (x11::EventObserver::*&)(x11::Event const&), x11::EventObserver&, x11::Event const&>(void (x11::EventObserver::*&)(x11::Event const&), x11::EventObserver&, x11::Event const&) gen/third_party/libc++/src/include/__type_traits/invoke.h:90:27
    #58 0x7fcc63441014 in std::__Cr::__invoke_result_impl<void, void (x11::EventObserver::*&)(x11::Event const&), x11::EventObserver&, x11::Event const&>::type std::__Cr::invoke<void (x11::EventObserver::*&)(x11::Event const&), x11::EventObserver&, x11::Event const&>(void (x11::EventObserver::*&)(x11::Event const&), x11::EventObserver&, x11::Event const&) gen/third_party/libc++/src/include/__functional/invoke.h:29:10
    #59 0x7fcc633d7908 in void base::ObserverList<x11::EventObserver, false, true, base::internal::UncheckedObserverAdapter<(partition_alloc::internal::RawPtrTraits)1, false>>::Notify<void (x11::EventObserver::*)(x11::Event const&), x11::Event>(T, x11::Event const&) base/observer_list.h:398:7
    #60 0x7fcc633c6e20 in x11::Connection::DispatchEvent(x11::Event const&) ui/gfx/x/connection.cc:588:20
    #61 0x7fcc633c6cbe in x11::Connection::ProcessNextEvent() ui/gfx/x/connection.cc:680:3
    #62 0x7fcc633c6587 in x11::Connection::Dispatch() ui/gfx/x/connection.cc:566:5
    #63 0x7fccc11f92cd in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_watcher_glib.cc:57:15
    #64 0x7fccc0504384  (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x5c384) (BuildId: 7f30e2b6280e8ddfec64e2ce9fd9bf312f2aa06e)

0x7c0c3a51a190 is located 0 bytes inside of 35-byte region [0x7c0c3a51a190,0x7c0c3a51a1b3)
freed by thread T0 (chrome) here:
    #0 0x55e16b0fdb22 in operator delete(void*, unsigned long) (/.../repos/chromium/src/out/asan/chrome+0xef8eb22) (BuildId: c49f7d643280a506080383ed80809579bc217060)
    #1 0x7fcd9f96a1e5 in void std::__Cr::__libcpp_deallocate<unsigned char>(std::__Cr::__type_identity<unsigned char>::type*, std::__Cr::__element_count, unsigned long) gen/third_party/libc++/src/include/__new/allocate.h:63:10
    #2 0x7fcd9f96a185 in std::__Cr::allocator<unsigned char>::deallocate(unsigned char*, unsigned long) gen/third_party/libc++/src/include/__memory/allocator.h:107:7
    #3 0x7fcd9f969fe4 in std::__Cr::allocator_traits<std::__Cr::allocator<unsigned char>>::deallocate(std::__Cr::allocator<unsigned char>&, unsigned char*, unsigned long) gen/third_party/libc++/src/include/__memory/allocator_traits.h:289:9
    #4 0x7fcd9f96a771 in std::__Cr::vector<unsigned char, std::__Cr::allocator<unsigned char>>::__destroy_vector::operator()() gen/third_party/libc++/src/include/__vector/vector.h:250:9
    #5 0x7fcd9f964e8b in std::__Cr::vector<unsigned char, std::__Cr::allocator<unsigned char>>::~vector() gen/third_party/libc++/src/include/__vector/vector.h:259:67
    #6 0x7fcd9fa91b94 in base::RefCountedBytes::~RefCountedBytes() base/memory/ref_counted_memory.cc:33:35
    #7 0x7fcd9fa91bc8 in base::RefCountedBytes::~RefCountedBytes() base/memory/ref_counted_memory.cc:33:35
    #8 0x7fcd719b78d2 in void base::RefCountedThreadSafe<base::RefCountedMemory, base::DefaultRefCountedThreadSafeTraits<base::RefCountedMemory>>::DeleteInternal<base::RefCountedMemory>(base::RefCountedMemory const*) base/memory/ref_counted.h:438:5
    #9 0x7fcd719b7864 in base::DefaultRefCountedThreadSafeTraits<base::RefCountedMemory>::Destruct(base::RefCountedMemory const*) base/memory/ref_counted.h:391:5
    #10 0x7fcd719b783b in base::RefCountedThreadSafe<base::RefCountedMemory, base::DefaultRefCountedThreadSafeTraits<base::RefCountedMemory>>::Release() const base/memory/ref_counted.h:427:7
    #11 0x7fcd719b77ed in scoped_refptr<base::RefCountedBytes>::Release(base::RefCountedBytes*) base/memory/scoped_refptr.h:392:8
    #12 0x7fcd719b7791 in scoped_refptr<base::RefCountedBytes>::~scoped_refptr() base/memory/scoped_refptr.h:280:7
    #13 0x7fcd719b1eb1 in ui::ClipboardOzone::AsyncClipboardOzone::ReadClipboardDataAndWait(ui::ClipboardBuffer, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) ui/base/clipboard/clipboard_ozone.cc:293:14
    #14 0x7fcd71989c53 in ui::ClipboardOzone::ReadText(ui::ClipboardBuffer, ui::DataTransferEndpoint const*, std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t>>*) const ui/base/clipboard/clipboard_ozone.cc:777:49
    #15 0x55e1789ac496 in GetClipboardText(bool) chrome/browser/ui/omnibox/clipboard_utils.cc:54:16
    #16 0x55e18aa59e5f in OmniboxViewViews::GetLabelForCommandId(int) const chrome/browser/ui/views/omnibox/omnibox_view_views.cc:1365:7
    #17 0x55e18aa5a2fc in non-virtual thunk to OmniboxViewViews::GetLabelForCommandId(int) const chrome/browser/ui/views/omnibox/omnibox_view_views.cc
    #18 0x7fcd9b4ce71e in ui::SimpleMenuModel::GetLabelAt(unsigned long) const ui/menus/simple_menu_model.cc:452:23
    #19 0x7fcd1563175b in views::MenuModelAdapter::AddMenuItemFromModelAt(ui::MenuModel*, unsigned long, views::MenuItemView*, unsigned long, int) ui/views/controls/menu/menu_model_adapter.cc:132:35
    #20 0x7fcd156320cd in views::MenuModelAdapter::AppendMenuItemFromModel(ui::MenuModel*, unsigned long, views::MenuItemView*, int) ui/views/controls/menu/menu_model_adapter.cc:165:10
    #21 0x7fcd1563217b in views::MenuModelAdapter::AppendMenuItem(views::MenuItemView*, ui::MenuModel*, unsigned long) ui/views/controls/menu/menu_model_adapter.cc:171:10
    #22 0x7fcd156300be in views::MenuModelAdapter::BuildMenuImpl(views::MenuItemView*, ui::MenuModel*) ui/views/controls/menu/menu_model_adapter.cc:305:32
    #23 0x7fcd1562fad4 in views::MenuModelAdapter::BuildMenu(views::MenuItemView*) ui/views/controls/menu/menu_model_adapter.cc:60:3
    #24 0x7fcd15630773 in views::MenuModelAdapter::CreateMenu() ui/views/controls/menu/menu_model_adapter.cc:67:3
    #25 0x7fcd15642f70 in views::internal::MenuRunnerImplAdapter::MenuRunnerImplAdapter(ui::MenuModel*, base::RepeatingCallback<void ()>) ui/views/controls/menu/menu_runner_impl_adapter.cc:20:53
    #26 0x7fcd1563bb54 in views::internal::MenuRunnerImplInterface::Create(ui::MenuModel*, int, base::RepeatingCallback<void ()>) ui/views/controls/menu/menu_runner_impl.cc:69:14
    #27 0x7fcd1563a0aa in views::MenuRunner::MenuRunner(ui::MenuModel*, int, base::RepeatingCallback<void ()>) ui/views/controls/menu/menu_runner.cc:25:13
    #28 0x7fcd1557e8bd in std::__Cr::unique_ptr<views::MenuRunner, std::__Cr::default_delete<views::MenuRunner>> std::__Cr::make_unique<views::MenuRunner, ui::SimpleMenuModel*, int, 0>(ui::SimpleMenuModel*&&, int&&) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:30
    #29 0x7fcd157e3c60 in views::Textfield::UpdateContextMenu() ui/views/controls/textfield/textfield.cc:3068:26

previously allocated by thread T0 (chrome) here:
    #0 0x55e16b0fcf1d in operator new(unsigned long) (/.../repos/chromium/src/out/asan/chrome+0xef8df1d) (BuildId: c49f7d643280a506080383ed80809579bc217060)
    #1 0x7fcd9f9682fd in unsigned char* std::__Cr::__libcpp_allocate<unsigned char>(std::__Cr::__element_count, unsigned long) gen/third_party/libc++/src/include/__new/allocate.h:43:28
    #2 0x7fcd9f968284 in std::__Cr::allocator<unsigned char>::allocate(unsigned long) gen/third_party/libc++/src/include/__memory/allocator.h:92:14
    #3 0x7fcd9f96821c in std::__Cr::allocator<unsigned char>::allocate_at_least(unsigned long) gen/third_party/libc++/src/include/__memory/allocator.h:99:13
    #4 0x7fcd9f96815c in std::__Cr::allocation_result<unsigned char*, unsigned long> std::__Cr::allocator_traits<std::__Cr::allocator<unsigned char>>::allocate_at_least<std::__Cr::allocator<unsigned char>>(std::__Cr::allocator<unsigned char>&, unsigned long) gen/third_party/libc++/src/include/__memory/allocator_traits.h:280:22
    #5 0x7fcd9f967e32 in auto std::__Cr::__allocate_at_least<std::__Cr::allocator<unsigned char>>(std::__Cr::allocator<unsigned char>&, unsigned long) gen/third_party/libc++/src/include/__memory/allocate_at_least.h:36:16
    #6 0x7fcd9f967847 in std::__Cr::vector<unsigned char, std::__Cr::allocator<unsigned char>>::__vallocate(unsigned long) gen/third_party/libc++/src/include/__vector/vector.h:580:25
    #7 0x7fcd9fa94ffd in void std::__Cr::vector<unsigned char, std::__Cr::allocator<unsigned char>>::__init_with_size<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>>(base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, unsigned long) gen/third_party/libc++/src/include/__vector/vector.h:598:7
    #8 0x7fcd9fa93564 in std::__Cr::vector<unsigned char, std::__Cr::allocator<unsigned char>>::vector<base::CheckedContiguousIterator<unsigned char const>, 0>(base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>) gen/third_party/libc++/src/include/__vector/vector.h:211:5
    #9 0x7fcd9fa91e04 in base::RefCountedBytes::RefCountedBytes(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) base/memory/ref_counted_memory.cc:39:7
    #10 0x7fcc63adffb1 in scoped_refptr<base::RefCountedBytes> base::MakeRefCounted<base::RefCountedBytes, base::RefCountedMemory&>(base::RefCountedMemory&) base/memory/scoped_refptr.h:151:16
    #11 0x7fcc63adcf7e in ui::SelectionData::TakeBytes() ui/base/x/selection_utils.cc:220:10
    #12 0x7fcda2b14ebe in ui::X11ClipboardOzone::RequestClipboardData(ui::ClipboardBuffer, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, base::OnceCallback<void (scoped_refptr<base::RefCountedBytes> const&)>) ui/ozone/platform/x11/x11_clipboard_ozone.cc:49:42
    #13 0x7fcd719d03b1 in ui::ClipboardOzone::AsyncClipboardOzone::Read(ui::ClipboardBuffer, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) ui/base/clipboard/clipboard_ozone.cc:385:26
    #14 0x7fcd719b1e63 in ui::ClipboardOzone::AsyncClipboardOzone::ReadClipboardDataAndWait(ui::ClipboardBuffer, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) ui/base/clipboard/clipboard_ozone.cc:293:21
    #15 0x7fcd71989c53 in ui::ClipboardOzone::ReadText(ui::ClipboardBuffer, ui::DataTransferEndpoint const*, std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t>>*) const ui/base/clipboard/clipboard_ozone.cc:777:49
    #16 0x55e1789ac496 in GetClipboardText(bool) chrome/browser/ui/omnibox/clipboard_utils.cc:54:16
    #17 0x55e18aa59e5f in OmniboxViewViews::GetLabelForCommandId(int) const chrome/browser/ui/views/omnibox/omnibox_view_views.cc:1365:7
    #18 0x55e18aa5a2fc in non-virtual thunk to OmniboxViewViews::GetLabelForCommandId(int) const chrome/browser/ui/views/omnibox/omnibox_view_views.cc
    #19 0x7fcd9b4ce71e in ui::SimpleMenuModel::GetLabelAt(unsigned long) const ui/menus/simple_menu_model.cc:452:23
    #20 0x7fcd1563175b in views::MenuModelAdapter::AddMenuItemFromModelAt(ui::MenuModel*, unsigned long, views::MenuItemView*, unsigned long, int) ui/views/controls/menu/menu_model_adapter.cc:132:35
    #21 0x7fcd156320cd in views::MenuModelAdapter::AppendMenuItemFromModel(ui::MenuModel*, unsigned long, views::MenuItemView*, int) ui/views/controls/menu/menu_model_adapter.cc:165:10
    #22 0x7fcd1563217b in views::MenuModelAdapter::AppendMenuItem(views::MenuItemView*, ui::MenuModel*, unsigned long) ui/views/controls/menu/menu_model_adapter.cc:171:10
    #23 0x7fcd156300be in views::MenuModelAdapter::BuildMenuImpl(views::MenuItemView*, ui::MenuModel*) ui/views/controls/menu/menu_model_adapter.cc:305:32
    #24 0x7fcd1562fad4 in views::MenuModelAdapter::BuildMenu(views::MenuItemView*) ui/views/controls/menu/menu_model_adapter.cc:60:3
    #25 0x7fcd15630773 in views::MenuModelAdapter::CreateMenu() ui/views/controls/menu/menu_model_adapter.cc:67:3
    #26 0x7fcd15642f70 in views::internal::MenuRunnerImplAdapter::MenuRunnerImplAdapter(ui::MenuModel*, base::RepeatingCallback<void ()>) ui/views/controls/menu/menu_runner_impl_adapter.cc:20:53
    #27 0x7fcd1563bb54 in views::internal::MenuRunnerImplInterface::Create(ui::MenuModel*, int, base::RepeatingCallback<void ()>) ui/views/controls/menu/menu_runner_impl.cc:69:14
    #28 0x7fcd1563a0aa in views::MenuRunner::MenuRunner(ui::MenuModel*, int, base::RepeatingCallback<void ()>) ui/views/controls/menu/menu_runner.cc:25:13
    #29 0x7fcd1557e8bd in std::__Cr::unique_ptr<views::MenuRunner, std::__Cr::default_delete<views::MenuRunner>> std::__Cr::make_unique<views::MenuRunner, ui::SimpleMenuModel*, int, 0>(ui::SimpleMenuModel*&&, int&&) gen/third_party/libc++/src/include/__memory/unique_ptr.h:756:30

SUMMARY: AddressSanitizer: heap-use-after-free base/strings/string_util_impl_helpers.h:204:22 in bool base::internal::DoIsStringASCII<char>(char const*, unsigned long)
Shadow bytes around the buggy address:
  0x7c0c3a519f00: f7 fa fd fd fd fd fd fd f7 fa 00 00 00 00 00 00
  0x7c0c3a519f80: f7 fa fa fa fa fa fa fa f7 fa fa fa fa fa fa fa
  0x7c0c3a51a000: f7 fa fa fa fa fa fa fa f7 fa fa fa fa fa fa fa
  0x7c0c3a51a080: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fd
  0x7c0c3a51a100: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fa
=>0x7c0c3a51a180: f7 fa[fd]fd fd fd fd fa f7 fa 00 00 00 00 00 00
  0x7c0c3a51a200: f7 fa 00 00 00 00 00 fa f7 fa fd fd fd fd fd fa
  0x7c0c3a51a280: f7 fa fa fa fa fa fa fa f7 fa fa fa fa fa fa fa
  0x7c0c3a51a300: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd
  0x7c0c3a51a380: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fa
  0x7c0c3a51a400: f7 fa fa fa fa fa fa fa f7 fa fa fa fa fa fa fa
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

==264673==ADDITIONAL INFO

==264673==Note: Please include this section with the ASan report.
Task trace:


Command line: `./out/asan/chrome --ozone-platform=x11 --user-data-dir=/tmp/tmp.wJRgYhL143 --flag-switches-begin --flag-switches-end`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==264673==END OF ADDITIONAL INFO

==264673==ABORTING

```

### ma...@google.com (2026-02-13)

Security shepherd: Treating this as S1 for a browser UaF mitigated by specific user interaction.

### ja...@chromium.org (2026-02-14)

OK, @th...@chromium.org bisected the fix to <https://chromium-review.googlesource.com/c/chromium/src/+/7538501>

According to the commit message it was introduced in [crrev.com/c/7523005](https://crrev.com/c/7523005)

### ja...@chromium.org (2026-02-14)

Sorry, the previous message should have read: OK, @th...@chromium.org, I bisected the fix to <https://chromium-review.googlesource.com/c/chromium/src/+/7538501>

I'll add that as the code changes and mark this as fixed.

### ja...@chromium.org (2026-02-14)

Or actually, @th...@chromium.org could you take a look and see if anything else needs to be fixed in order to prevent this from being exploitable?

### ch...@google.com (2026-02-14)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-14)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### th...@chromium.org (2026-02-17)

Thanks for bisecting. It looks like this was broken between r1576950 and r1578222. These were before the M146 branch point so no backport is required.

### ch...@google.com (2026-02-18)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M145. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-02-19)

Thanks! Removing merge labels.

### sp...@google.com (2026-03-05)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Duplicate. Consequences were previously mitigated and the fix landed before this issue was created.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-05-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Duplicate. Consequences were previously mitigated and the fix landed before this issue was created.
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/482711647)*
