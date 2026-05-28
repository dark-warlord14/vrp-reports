# Security: container-overflow in chrome::ReloadInternal

| Field | Value |
|-------|-------|
| **Issue ID** | [339061099](https://issues.chromium.org/issues/339061099) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Input>KeyboardShortcuts |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 124.0.6324.0 |
| **CVE IDs** | CVE-2024-5497 |
| **Reporter** | zh...@gmail.com |
| **Assignee** | tb...@google.com |
| **Created** | 2024-05-07 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. Download asan mac 1265061
2. `./Chromium.app/Contents/MacOS/Chromium --no-sandbox http://127.0.0.1/ about:blank --user-data-dir=/tmp/userdata/t1`
3. Just submit any information that meets the requirements in the form of index.html,
4. Then hold down shift to select the `index.html` and `about:blank` tabs, then press `command+R` to refresh the two tabs, and container-overflow will be triggered stably.(Part of the user interaction in the process can be replaced by JavaScript, such as automatic form submission. I won’t go into details here)

# Problem Description

Security: container-overflow in chrome::ReloadInternal.No additional features are required to trigger the vulnerability.

# Summary

Security: container-overflow in chrome::ReloadInternal

# Custom Questions

#### Type of crash:

browser

#### Crash state:

```
=================================================================
==55019==ERROR: AddressSanitizer: container-overflow on address 0x60200058fb98 at pc 0x00017b3b123a bp 0x7ff7b19eeef0 sp 0x7ff7b19eeee8
READ of size 8 at 0x60200058fb98 thread T0
==55019==WARNING: invalid path to external symbolizer!
==55019==WARNING: Failed to use and restart external symbolizer!
    #0 0x17b3b1239 in chrome::(anonymous namespace)::ReloadInternal(Browser*, WindowOpenDisposition, bool)+0x799 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x22776239)
    #1 0x17b3b0a4d in chrome::Reload(Browser*, WindowOpenDisposition)+0xcd (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x22775a4d)
    #2 0x17b398ac5 in chrome::BrowserCommandController::ExecuteCommandWithDisposition(int, WindowOpenDisposition, base::TimeTicks)+0x2b55 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x2275dac5)
    #3 0x17b0b53aa in BrowserFrameMac::ExecuteCommand(int, WindowOpenDisposition, bool)+0xba (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x2247a3aa)
    #4 0x1724d0f40 in non-virtual thunk to views::NativeWidgetMacNSWindowHost::ExecuteCommand(int, WindowOpenDisposition, bool, bool*)+0x90 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x19895f40)
    #5 0x17b087765 in -[BrowserWindowCommandHandler commandDispatch:window:]+0x205 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x2244c765)
    #6 0x16c5b50c6 in -[CommandDispatcher dispatch:forHandler:]+0x56 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x1397a0c6)
    #7 0x7ff81ef422b5 in -[NSApplication(NSResponder) sendAction:to:from:]+0x150 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x22b2b5)
    #8 0x1674c9d5d in __43-[BrowserCrApplication sendAction:to:from:]_block_invoke+0x12d (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xe88ed5d)
    #9 0x16894cc59 in base::apple::CallWithEHFrame(void () block_pointer)+0x9 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xfd11c59)
    #10 0x1674c98e5 in -[BrowserCrApplication sendAction:to:from:]+0x565 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xe88e8e5)
    #11 0x7ff81f02eb50 in -[NSMenuItem _corePerformAction]+0x1c6 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x317b50)
    #12 0x7ff81f69490d in _NSMenuPerformActionWithHighlighting+0xb8 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x97d90d)
    #13 0x7ff81f4d0704 in -[NSMenu _performActionForItem:atIndex:fromEvent:]+0xc4 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x7b9704)
    #14 0x7ff81f02dae0 in -[NSMenu performKeyEquivalent:]+0x1b3 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x316ae0)
    #15 0x7ff81f666e8b in routeKeyEquivalent+0x2ac (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x94fe8b)
    #16 0x7ff81f6644c9 in -[NSApplication(NSEventRouting) sendEvent:]+0x36d (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x94d4c9)
    #17 0x1674cb213 in __34-[BrowserCrApplication sendEvent:]_block_invoke+0x2f3 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xe890213)
    #18 0x16894cc59 in base::apple::CallWithEHFrame(void () block_pointer)+0x9 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xfd11c59)
    #19 0x1674ca8fc in -[BrowserCrApplication sendEvent:]+0x90c (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xe88f8fc)
    #20 0x7ff81f21f5c1 in -[NSApplication _handleEvent:]+0x40 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x5085c1)
    #21 0x7ff81ed47029 in -[NSApplication run]+0x27f (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x30029)
    #22 0x168959c18 in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate*)+0x368 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xfd1ec18)
    #23 0x1689554c3 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x303 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xfd1a4c3)
    #24 0x16885729d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x49d (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xfc1c29d)
    #25 0x1687987e4 in base::RunLoop::Run(base::Location const&)+0x544 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xfb5d7e4)
    #26 0x1611a7424 in content::BrowserMainLoop::RunMainMessageLoop()+0x1c4 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x856c424)
    #27 0x1611adc82 in content::BrowserMainRunnerImpl::Run()+0x32 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x8572c82)
    #28 0x16119e453 in content::BrowserMain(content::MainFunctionParams)+0x223 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x8563453)
    #29 0x1661004ff in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*)+0x1df (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xd4c54ff)
    #30 0x166102f7e in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x41e (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xd4c7f7e)
    #31 0x166102917 in content::ContentMainRunnerImpl::Run()+0x687 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xd4c7917)
    #32 0x1660fe80d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x72d (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xd4c380d)
    #33 0x1660ff25c in content::ContentMain(content::ContentMainParams)+0x1cc (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xd4c425c)
    #34 0x158c403bc in ChromeMain+0x3cc (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x53bc)
    #35 0x10e50fba6 in main+0x1e6 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/MacOS/Chromium:x86_64+0x100000ba6)
    #36 0x7ff81b287365 in start+0x795 (/usr/lib/dyld:x86_64+0xfffffffffff5c365)

0x60200058fb98 is located 8 bytes inside of 16-byte region [0x60200058fb90,0x60200058fba0)
allocated by thread T0 here:
    #0 0x10ed09292 in __asan_memmove+0x2ac2 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x51292)
    #1 0x182b94b27 in operator new(unsigned long)+0x27 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x29f59b27)
    #2 0x1591247bb in void std::__Cr::vector<unsigned long, std::__Cr::allocator<unsigned long>>::__assign_with_size<unsigned long*, unsigned long*>(unsigned long*, unsigned long*, long)+0xeb (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x4e97bb)
    #3 0x1713e9cc9 in ui::ListSelectionModel::operator=(ui::ListSelectionModel const&)+0x59 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x187aecc9)
    #4 0x17b56583f in TabStripModel::SetSelection(ui::ListSelectionModel, TabStripModelObserver::ChangeReason, bool)+0x4bf (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x2292a83f)
    #5 0x17b56f323 in TabStripModel::ExtendSelectionTo(int)+0x1a3 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x22934323)
    #6 0x17c8338e4 in non-virtual thunk to TabStrip::ExtendSelectionTo(Tab*)+0x264 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x23bf88e4)
    #7 0x17c74262d in Tab::OnMousePressed(ui::MouseEvent const&)+0x60d (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x23b0762d)
    #8 0x17241acd3 in views::View::ProcessMousePressed(ui::MouseEvent const&)+0x353 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x197dfcd3)
    #9 0x17241a71a in views::View::OnMouseEvent(ui::MouseEvent*)+0x5a (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x197df71a)
    #10 0x16c65e27c in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*)+0x20c (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x13a2327c)
    #11 0x16c65cd6b in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*)+0x68b (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x13a21d6b)
    #12 0x16c65c34b in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*)+0x23b (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x13a2134b)
    #13 0x16c65bee2 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*)+0x202 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x13a20ee2)
    #14 0x172448b55 in views::internal::RootView::OnMousePressed(ui::MouseEvent const&)+0x595 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x1980db55)
    #15 0x172479c76 in views::Widget::OnMouseEvent(ui::MouseEvent*)+0x626 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x1983ec76)
    #16 0x1724c97a0 in non-virtual thunk to views::NativeWidgetMacNSWindowHost::OnMouseEvent(std::__Cr::unique_ptr<ui::Event, std::__Cr::default_delete<ui::Event>>)+0x100 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x1988e7a0)
    #17 0x16eb4efc9 in -[BridgedContentView mouseEvent:]+0x219 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x15f13fc9)
    #18 0x7ff81ef3c2f2 in -[NSWindow(NSEventRouting) _handleMouseDownEvent:isDelayedEvent:]+0x11e5 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x2252f2)
    #19 0x7ff81eeb50cd in -[NSWindow(NSEventRouting) _reallySendEvent:isDelayedEvent:]+0x193 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x19e0cd)
    #20 0x7ff81eeb4d1e in -[NSWindow(NSEventRouting) sendEvent:]+0x158 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x19dd1e)
    #21 0x16eb64177 in -[NativeWidgetMacNSWindow sendEvent:]+0x427 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x15f29177)
    #22 0x7ff81f6642b5 in -[NSApplication(NSEventRouting) sendEvent:]+0x159 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x94d2b5)
    #23 0x1674cb213 in __34-[BrowserCrApplication sendEvent:]_block_invoke+0x2f3 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xe890213)
    #24 0x16894cc59 in base::apple::CallWithEHFrame(void () block_pointer)+0x9 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xfd11c59)
    #25 0x1674ca8fc in -[BrowserCrApplication sendEvent:]+0x90c (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xe88f8fc)
    #26 0x7ff81f21f5c1 in -[NSApplication _handleEvent:]+0x40 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x5085c1)
    #27 0x7ff81ed47029 in -[NSApplication run]+0x27f (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:x86_64+0x30029)
    #28 0x168959c18 in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate*)+0x368 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xfd1ec18)
    #29 0x1689554c3 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x303 (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0xfd1a4c3)

HINT: if you don't care about these errors you may set ASAN_OPTIONS=detect_container_overflow=0.
If you suspect a false positive see also: https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow.
SUMMARY: AddressSanitizer: container-overflow (/Users/zh1x1an/Downloads/mac-release_asan-mac-release-1265061/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/124.0.6324.0/Chromium Framework:x86_64+0x22776239) in chrome::(anonymous namespace)::ReloadInternal(Browser*, WindowOpenDisposition, bool)+0x799
Shadow bytes around the buggy address:
  0x60200058f900: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fa
  0x60200058f980: f7 fa fd fd f7 fa fd fd f7 fa fd fa f7 fa fd fd
  0x60200058fa00: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fd
  0x60200058fa80: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x60200058fb00: f7 fa fd fa f7 fa fd fd f7 fa fd fa f7 fa fd fd
=>0x60200058fb80: f7 fa 00[fc]f7 fa fd fd f7 fa fd fa f7 fa 00 fa
  0x60200058fc00: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fd
  0x60200058fc80: f7 fa fd fa f7 fa fd fa f7 fa fd fa f7 fa fd fa
  0x60200058fd00: f7 fa fd fa f7 fa fd fa f7 fa fd fd f7 fa fd fd
  0x60200058fd80: f7 fa fd fd f7 fa fd fd f7 fa fd fd f7 fa fd fd
  0x60200058fe00: f7 fa fd fd f7 fa fd fa f7 fa 00 fa f7 fa fd fd
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

==55019==ADDITIONAL INFO

==55019==Note: Please include this section with the ASan report.
Task trace:

==55019==END OF ADDITIONAL INFO
==55019==ABORTING
Received signal 6

```
# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 21.0 KB)
- [index.html](attachments/index.html) (text/html, 1.0 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 25.6 MB)

## Timeline

### zh...@gmail.com (2024-05-07)

Update a `poc.mov`. The steps to reproduce the vulnerability are very stable and can be reproduced stably on both Intel and ARM on Mac without any additional features.

RCA and Bisect coming soon!

### zh...@gmail.com (2024-05-07)

## Bisect commit

<https://chromiumdash.appspot.com/commit/a8425e98fcc1a6a9c7d4e69112f678ad53d2d763>

**This vulnerability can be triggered on any system.**

Bisect commit was tested on Linux:

1. `Download asan-linux-release-585600`, the above vulnerability **cannot** be reproduced.
2. `Download asan-linux-release-585605`, the above vulnerability **can** be reproduced.

### ca...@chromium.org (2024-05-07)

I was able to reproduce this on the current stable in Linux, given that this is memory corruption in the browser process, but requires user interaction, I'll triage this as high severity (reporter: if you have evidence that the interaction can be automated, this might be a critical instead).
andrewxu: This seems related to the functionality added in crrev.com/c/1180516. Could you please take a look (and reassign as appropriate if you're no longer working on this)? Thanks.

### df...@google.com (2024-05-07)

Unclear why this was reassigned to me? I do not own the code and was not party to the change.

### an...@chromium.org (2024-05-08)

@dfried Thank you for taking a look :)  I was trying to leave a comment after re-assignment but I lost editing right. I wrote an email to explain.

### zh...@gmail.com (2024-05-08)

I can use this HTML to automatically submit the form, but for now, the multi-tab refresh function used to trigger the vulnerability seems difficult to replace with simple HTML+javascript.

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up Form</title>
</head>
<body>
<h1>Sign Up</h1>
<form id="form1" action="/submit" method="POST">
    <div>
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" value="aaa">
    </div>
    <div>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" value="a@a">
    </div>
    <div>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password"  autocomplete="new-password" value="aaa">
    </div>
    <div>
        <label for="repeatPassword">Repeat Password:</label>
        <input type="password" id="repeatPassword" name="repeatPassword" autocomplete="new-password" value="aaa">
    </div>
    <button id="click" type="submit">Sign Up</button>
</form>

<script>
    setTimeout(function() {
        document.getElementById("click").click();
    },3000);
</script>
</body>
</html>

```

### pe...@google.com (2024-05-08)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-08)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### zh...@gmail.com (2024-05-09)

## RCA here

In the `ListSelectionModel` class, a `SelectedIndices selected_indices_;` is stored

[selected\_indices\_](https://source.chromium.org/chromium/chromium/src/+/main:ui/base/models/list_selection_model.h;l=124?q=content:%22SelectedIndices%20selected_indices_;%22&sq=) which is a [base::flat\_set](https://source.chromium.org/chromium/chromium/src/+/main:base/containers/flat_set.h;l=152-156;drc=4106e2406bd1b7219657a730bc389eb3a4629daa), essentially the same as `std::vector`

```
using SelectedIndices = base::flat_set<size_t>;

```
```
template <class Key,
          class Compare = std::less<>,
          class Container = std::vector<Key>>
using flat_set = typename ::base::internal::
    flat_tree<Key, std::identity, Compare, Container>;

```

This `flat_set` is the structure that ultimately triggers the `container-overflow` vulnerability. Let’s look at the trigger path:

There is a relatively clear description in [Bisect commit](https://chromiumdash.appspot.com/commit/a8425e98fcc1a6a9c7d4e69112f678ad53d2d763):

> Before modification, Only one tab was refreshed after pressing Ctrl-R regardless of how many tabs you selected. But pressing Ctrl-W was able to close several tabs.

Select multiple tags through shift, and then pressing Ctrl-R (command+R on macos) will execute [chrome::ReloadInternal](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_commands.cc;l=433-466?q=browser_commands.cc:433) Function:

```
void ReloadInternal(Browser* browser,
                    WindowOpenDisposition disposition,
                    bool bypass_cache) {
  const WebContents* active_contents =
      browser->tab_strip_model()->GetActiveWebContents();
  const auto& selected_indices =
      browser->tab_strip_model()->selection_model().selected_indices(); // @audit: Use lldb to debug this `flat_set`. At this time, its size is 2 and its capacity is also 2.
  for (int index : selected_indices) {

```

The details of `selected_indices` in `lldb` are as follows:

```
Printing description of selected_indices:
(const ui::ListSelectionModel::SelectedIndices &) selected_indices = 0x00006130001e22c8: {
  comp_ = {}
  body_ = size=2 {
    __begin_ = 0x00006020005934b0
    __end_ = 0x00006020005934c0
    __end_cap_ = {
      std::__Cr::__compressed_pair_elem<unsigned long *, 0, false> = {
        __value_ = 0x00006020005934c0
      }
    }
  }
}

```

Then in the `chrome::ReloadInternal` function, there is a large section [for loop](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_commands.cc;l=440-464?q=browser_commands.cc:433), there is a key logic that will cause the `size` of `flat_set` to be changed **from 2 to 1**. Let’s take a look at this path:

```
for (int index : selected_indices) {
    //...
    //...
    if (!devtools || !devtools->ReloadInspectedWebContents(bypass_cache)) {
      new_tab->GetController().Reload( // @audit: selected_indices_.size() will change here !!! !!!
          bypass_cache ? kBypassingType : kNormalType, true);
    }
  }

```

If you want to execute this `new_tab->GetController().Reload`, you need to ensure that the browser does not open the devtools at this time (this is easy to meet the conditions), and then the following call chain will be executed:

[NavigationControllerImpl::Reload](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_controller_impl.cc;l=891-949?q=navigation_controller_impl.cc:949)

[WebContentsImpl::ActivateAndShowRepostFormWarningDialog](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=7521-7524;drc=4106e2406bd1b7219657a730bc389eb3a4629daa?q=WebContentsImpl::ActivateAndShowRepostFormWarningDialog&ss=chromium%2Fchromium%2Fsrc)

[WebContentsImpl::Activate](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=3740-3743;drc=4106e2406bd1b7219657a730bc389eb3a4629daa?q=WebContentsImpl::ActivateAndShowRepostFormWarningDialog&ss=chromium%2Fchromium%2Fsrc)

[Browser::ActivateContents](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser.cc;l=1839-1845?q=Browser::ActivateContents)

**Finally, the key [TabStripModel::ActivateTabAt](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_strip_model.cc;l=653-670;drc=4106e2406bd1b7219657a730bc389eb3a4629daa) funciont will be called**:

```
void TabStripModel::ActivateTabAt(int index,
                                  TabStripUserGestureDetails user_gesture) {
  ReentrancyCheck reentrancy_check(&reentrancy_guard_);

  CHECK(ContainsIndex(index));
  TRACE_EVENT0("ui", "TabStripModel::ActivateTabAt");

  scrubbing_metrics_.IncrementPressCount(user_gesture);

  ui::ListSelectionModel new_model = selection_model_;
  new_model.SetSelectedIndex(index);
  SetSelection(
      std::move(new_model),
      user_gesture.type != TabStripUserGestureDetails::GestureType::kNone
          ? TabStripModelObserver::CHANGE_REASON_USER_GESTURE
          : TabStripModelObserver::CHANGE_REASON_NONE,
      /*triggered_by_other_operation=*/false);
}

```

In the `TabStripModel::ActivateTabAt` function, a `new_model` will be created, and `new_model` will execute [SetSelectedIndex](https://source.chromium.org/chromium/chromium/src/+/main:ui/base/models/list_selection_model.cc;l=106-117;drc=4106e2406bd1b7219657a730bc389eb3a4629daa) function (the index passed in is 0 at this time):

```
void ListSelectionModel::SetSelectedIndex(std::optional<size_t> index) {
  anchor_ = active_ = index;
  selected_indices_.clear();
  if (index.has_value()) { // @audit: The if here satisfies the condition
    selected_indices_.insert(index.value());

    // selected_indices_.size() is 1 now !!! !!!

    // The reason for adding last_accessed_map_ specifically in SetSelectedIndex
    // is that it is the primary method responsible for updating the selected
    // index, and it's where we have a clear indication of when a tab is being
    // actively selected by user.
    last_accessed_map_[index.value()] = base::Time::Now();
  }
}

```

In the `ListSelectionModel::SetSelectedIndex` function, `selected_indices_.clear();` will be executed first, at this time `selected_indices_.size()` is **0**, and then `selected_indices_.insert(index.value());` will be executed, At this time `selected_indices_.size()` is **1**

Then return to the `TabStripModel::ActivateTabAt` function, which will execute [SetSelection](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_strip_model.cc;l=663-664?q=TabStripModel::ActivateTabAt) function and pass this `selected_indices_.size()` as the `new_model` of **1** through `std::move` as the first parameter

**Follow up the execution to [TabStripModel::SetSelection](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tabs/tab_strip_model.cc;l=2322-2349?q=TabStripModel::SetSelection)**

```
TabStripSelectionChange TabStripModel::SetSelection(
    ui::ListSelectionModel new_model,
    TabStripModelObserver::ChangeReason reason,
    bool triggered_by_other_operation) {

  //...
  //...
  selection_model_ = new_model; // @audit: Here new_model is assigned to selection_model_

```

Therefore, it will be called: [ListSelectionModel operator=](https://source.chromium.org/chromium/chromium/src/+/main:ui/base/models/list_selection_model.cc;l=72-73?q=content:%22ListSelectionModel%26%20ListSelectionModel::operator%3D(const%20ListSelectionModel%26)%20%3D%22)

```
ListSelectionModel& ListSelectionModel::operator=(const ListSelectionModel&) =
    default;

```

The `flat_set` that ultimately triggers the vulnerability, that is, `SelectedIndices`, is a [field](https://source.chromium.org/chromium/chromium/src/+/main:ui/base/models/list_selection_model.h;l=124;drc=4106e2406bd1b7219657a730bc389eb3a4629daa) in the `ListSelectionModel` class

So it will also execute:

```
flat_tree& operator=(const flat_tree&) = default;

```

And finally call:

```
  _LIBCPP_CONSTEXPR_SINCE_CXX20 _LIBCPP_HIDE_FROM_ABI void __destruct_at_end(pointer __new_last) _NOEXCEPT {
    size_type __old_size = size();
    __base_destruct_at_end(__new_last);
    __annotate_shrink(__old_size); // @audit: That is, through shrink, change the size of selected_indices_ from 2 to 1
  }

```

In this case, the `__begin_` address of `selected_indices_` remains unchanged and the `__end_` address is reduced by 8 (because the size of `std::vector` is not stored in memory)

Finally, return to the vulnerability [chrome::ReloadInternal](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_commands.cc;l=433-466?q=browser_commands.cc:433) function:

```
for (int index : selected_indices) {
    //...
    //...
    if (!devtools || !devtools->ReloadInspectedWebContents(bypass_cache)) {
      new_tab->GetController().Reload(
          bypass_cache ? kBypassingType : kNormalType, true);
    }
  }

```

When the for loop continues to execute, **the memory accessed by the for loop changes from 0x00006020005934b0 to 0x00006020005934b8, but at this time the `__end_` of the vector changes from 0x00006020005934c0 to 0x00006020005934b8**

before:

```
Printing description of selected_indices:
(const ui::ListSelectionModel::SelectedIndices &) selected_indices = 0x00006130001e22c8: {
  comp_ = {}
  body_ = size=2 {
    __begin_ = 0x00006020005934b0
    __end_ = 0x00006020005934c0
    __end_cap_ = {
      std::__Cr::__compressed_pair_elem<unsigned long *, 0, false> = {
        __value_ = 0x00006020005934c0
      }
    }
  }
}

```

**after**:

```
Printing description of selected_indices:
(const ui::ListSelectionModel::SelectedIndices &) selected_indices = 0x00006130001e22c8: {
  comp_ = {}
  body_ = size=1 {
    __begin_ = 0x00006020005934b0
    __end_ = 0x00006020005934b8  // @audit: changed !!!
    __end_cap_ = {
      std::__Cr::__compressed_pair_elem<unsigned long *, 0, false> = {
        __value_ = 0x00006020005934c0
      }
    }
  }
}

```

When the `__end_` of the vector has been shrink, still accessing the memory before shrink will trigger `container-overflow` （Heap-buffer-overflow is not triggered here because the capacity at this time is still 2）.

**Since this is not an overflow access to the memory of std::vector through `[]` or `.at`, libc++ harding cannot Defend against this vulnerability**

### zh...@gmail.com (2024-05-13)

Friendly ping，any update？

### an...@chromium.org (2024-05-13)

Thank you for following up :)

This issue is on my radar. Currently distracted by other tasks, but will take a closer look later today :)   

### df...@google.com (2024-05-13)

The correct points of context for this are likely dpenning@ and tbergquist@, who are doing work on TabStripModel.

Feel free to reassign to one of them if you can't track down the issue yourself.

### an...@chromium.org (2024-05-15)

Did some early investigation and I understand the issue now :)

In my previous CL (https://chromium-review.googlesource.com/c/chromium/src/+/1180516), I introduced a const reference to the selected tab indices (https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_commands.cc;l=439;drc=914bc349fa0368615c16a6ff195db67211375bb4;bpv=1;bpt=0). The code assumes that the tab selection model does not change during reload, which is actually wrong, just as pointed out by the issue reporter in the comment10.

I am not very familiar with the details of tab strip model. Therefore, I may not be the right person to fix it.  +dpenning +tbergquist Could you help reassign  this issue please :)

### tb...@google.com (2024-05-16)

Okay, this makes sense. Thanks OP for the detailed analysis! Andrew's summary seems on point to me - in the repro, the selection model changes during the refresh process, which the reload browser command isn't expecting. The const reference to the selected indices is thus not actually safe to take.

Easy fix would be to just make a copy, or better yet, converting the indices into a vector of WebContents\* before doing the reloading.

### ap...@google.com (2024-05-20)

Project: chromium/src
Branch: main

commit 9cce0c95e740f637e1436cfa472b532c9ec35bfd
Author: Taylor Bergquist <tbergquist@chromium.org>
Date:   Mon May 20 21:29:09 2024

    Fix container overflow when reloading multiple tabs.
    
    When multiple tabs are selected, the reload command reloads all of them.
    The selection model can change as a result of reloading a tab (e.g. when
    one of the tabs is a submitted form). The reload command is not
    expecting the selected tabs to change while it's iterating over them,
    and can end up overflowing the selected indices container.
    
    This CL simply converts the selected indices into a more-resilient
    vector of selected WebContents* before reloading anything.
    
    Bug: 339061099
    Change-Id: I0c0b66fc93ddcbe57b42646126a1f2ca651b2df2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5545011
    Reviewed-by: Peter Boström <pbos@chromium.org>
    Reviewed-by: David Pennington <dpenning@chromium.org>
    Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1303471}

M       chrome/browser/ui/browser_commands.cc

https://chromium-review.googlesource.com/5545011


### pe...@google.com (2024-05-24)

Requesting merge to extended stable (M124) because latest trunk commit (1303471) appears to be after extended stable branch point (1274542).
Requesting merge to stable (M125) because latest trunk commit (1303471) appears to be after stable branch point (1287751).
Requesting merge to beta (M126) because latest trunk commit (1303471) appears to be after beta branch point (1300313).
Merge review required: M124 is already shipping to stable.


Merge review required: M125 is already shipping to stable.


Merge review required: M126 is already shipping to beta.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124, 125, 126].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### tb...@google.com (2024-05-24)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/5545011>
2. I haven't done any active verification on Canary.
3. I don't think so
4. No
5. Not required, but the test team could check the POC for stability (no need to use asan, just exercise the code). See OP for instructions and the required file index.html.

### am...@chromium.org (2024-05-24)

I've reviewed the fix (<https://crrev.com/c/5545011>) on Canary and there do not seem to be any issues presented by it. Please be sure to confirm on your side as well before engaging with backmerge.

merges approved for M126 beta (branch 6478), M125 Stable (branch 6422), and M124 Extended (branch 6367) at soonest, before eod Monday so this fix can be included in next updates for each

### ap...@google.com (2024-05-28)

Project: chromium/src
Branch: refs/branch-heads/6367

commit a679cb8b0de664a7b6043fba68e1134cf1221e22
Author: Taylor Bergquist <tbergquist@chromium.org>
Date:   Tue May 28 13:43:24 2024

    Fix container overflow when reloading multiple tabs.
    
    When multiple tabs are selected, the reload command reloads all of them.
    The selection model can change as a result of reloading a tab (e.g. when
    one of the tabs is a submitted form). The reload command is not
    expecting the selected tabs to change while it's iterating over them,
    and can end up overflowing the selected indices container.
    
    This CL simply converts the selected indices into a more-resilient
    vector of selected WebContents* before reloading anything.
    
    (cherry picked from commit 9cce0c95e740f637e1436cfa472b532c9ec35bfd)
    
    Bug: 339061099
    Change-Id: I0c0b66fc93ddcbe57b42646126a1f2ca651b2df2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5545011
    Reviewed-by: Peter Boström <pbos@chromium.org>
    Reviewed-by: David Pennington <dpenning@chromium.org>
    Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1303471}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5574988
    Auto-Submit: Daniel Yip <danielyip@google.com>
    Owners-Override: Daniel Yip <danielyip@google.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6367@{#1241}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       chrome/browser/ui/browser_commands.cc

https://chromium-review.googlesource.com/5574988


### pe...@google.com (2024-05-28)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### pb...@google.com (2024-05-28)

Cherry picked the CL mentioned in [comment#18](https://issues.chromium.org/issues/339061099#comment18) to M125 and M126 branches, I see that M124 cherry pick is already donw

M125 : <https://chromium-review.googlesource.com/c/chromium/src/+/5576834>
M126 : <https://chromium-review.googlesource.com/c/chromium/src/+/5576874>

### ap...@google.com (2024-05-28)

Project: chromium/src
Branch: refs/branch-heads/6422

commit ccbe9cb86bf4f100160ad1fd7180415ce2ca8758
Author: Taylor Bergquist <tbergquist@chromium.org>
Date:   Tue May 28 18:26:47 2024

    Fix container overflow when reloading multiple tabs.
    
    When multiple tabs are selected, the reload command reloads all of them.
    The selection model can change as a result of reloading a tab (e.g. when
    one of the tabs is a submitted form). The reload command is not
    expecting the selected tabs to change while it's iterating over them,
    and can end up overflowing the selected indices container.
    
    This CL simply converts the selected indices into a more-resilient
    vector of selected WebContents* before reloading anything.
    
    (cherry picked from commit 9cce0c95e740f637e1436cfa472b532c9ec35bfd)
    
    Bug: 339061099
    Change-Id: I0c0b66fc93ddcbe57b42646126a1f2ca651b2df2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5545011
    Reviewed-by: Peter Boström <pbos@chromium.org>
    Reviewed-by: David Pennington <dpenning@chromium.org>
    Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1303471}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5576834
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
    Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
    Cr-Commit-Position: refs/branch-heads/6422@{#1174}
    Cr-Branched-From: 9012208d0ce02e0cf0adb9b62558627c356f3278-refs/heads/main@{#1287751}

M       chrome/browser/ui/browser_commands.cc

https://chromium-review.googlesource.com/5576834


### am...@chromium.org (2024-05-28)

M126 merge completed earlier, removing approval

### sp...@google.com (2024-05-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$2,000 for report of highly mitigated memory corruption in the browser process, mitigated by user interaction and very narrow window / potential for exploitability by an attacker + $1,000 bisect bonus

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are not already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-30)

Thank you for this report zh1x1an1221! While in our assessment this bugs is highly mitigated, with low degree of potential exploitability and attacker control, we did want to commend your work here and detailed report which definitely resulted in a slightly higher reward amount for a highly mitigated bug. Nice work1

### zh...@gmail.com (2024-05-30)

Thank you very much, but I have some additions this time:

According to the rules:

<https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules>

> Reward amounts for mitigated security bugs
> Mitigated security bugs are eligible for VRP rewards, but at a reduced reward amount.

> We have defined levels for mitigated security bugs accordingly:

> Mildly mitigated: Security bug with minimal mitigations; e.g. a security bug reliably triggered by two or fewer standard user interactions OR winning a race condition; does not require profile destruction or shutdown to trigger

> Moderately mitigated: Security bug with multiple mitigations; e.g. a malicious extension combined with user interaction or other mitigation, or winning a race condition combined with another mitigation

> Highly mitigated: Security bug with multiple types of mitigations or triggered by a series of steps; e.g. a security bug triggered by a series of user interactions or involving a non-standard/unlikely workflow
> A use-after-free protected by BackupRefPtr / MiraclePtr is considered to be highly mitigated.
> Substantially mitigated: A heavily mitigated security bug, not likely to be able to be exploited in a real-world scenario; e.g. a bug requiring a series of implausible user interactions – such issues are not generally considered security issues and may not be eligible for a VRP reward.

**This vulnerability report should be a Mildly mitigated, not a Highly mitigated**

To trigger this, the vulnerability **does** require user interaction, **but the user interaction actually only has two steps, that is, the victim only needs to select 2 or more tabs and click the refresh page button in Chrome.**

The purpose of designing this function is to provide convenience to users so that they can refresh multiple tabs at a time, and the only thing required to trigger the vulnerability is this standard interaction. This is exactly the function itself.

I provided proof in [#comment7](https://issues.chromium.org/issues/339061099#comment7) that the operation of submitting the form can be completed automatically. So this part of user interaction can be completely avoided.

In addition, there is **no need to close Chrome, destroy the profile, do not need any race, is not protected by libc++ harding, and is not mitigated by miracle pointers (this is not a uaf vulnerability)**

Combining the above points, according to the vulnerability rules, I think this should be considered a **Mildly mitigated** Security bug, so I sincerely ask you to reconsider it here, thank you very much

### zh...@gmail.com (2024-05-30)

> mitigated by user interaction and very narrow window

Moreover, this vulnerability does not require any race, so there is no concept of narrow window. It only needs to use js to automatically submit the form like [#comment7](https://issues.chromium.org/issues/339061099#comment7), and then the victim triggers the interaction.

The setTimeout time I wrote can be modified to be very short. 3s is just an example, so there is no narrow window. I hope it does not cause misunderstanding.

### pe...@google.com (2024-05-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### vo...@google.com (2024-05-30)

1. <https://crrev.com/c/5584557>
2. Low - no conflicts
3. M124, M125
4. Yes

### wf...@chromium.org (2024-05-30)

re: #27 and #28 - Thanks for your query about the reward - expect a response to this next week, in the meantime we appreciate your patience.

### zh...@gmail.com (2024-05-31)

re: [#comment31](https://issues.chromium.org/issues/339061099#comment31) Thank you very much. I will wait patiently.

### zh...@gmail.com (2024-06-03)

At the same time, I think the description in the announcement is also inaccurate, because the triggering of this vulnerability has nothing to do with Keyboard Inputs, but only with multiple page refreshes. This may be the main reason why this vulnerability is mistakenly considered to be Highly mitigated.

```
CVE-2024-5497: Out of bounds memory access in Keyboard Inputs. Reported by zh1x1an1221 of Ant Group Tianqiong Security Lab on 2024-05-07

```

### am...@chromium.org (2024-06-05)

Thanks for the feedback about the CVE description. Tagging pgrace@ -- you may want to adjust this CVE description to Browser UI or something more reflective of the issue.

### am...@chromium.org (2024-06-05)

re c#33 `. This may be the main reason why this vulnerability is mistakenly considered to be Highly mitigated.`

The VRP reward decision and consideration of this being a highly mitigated issue has nothing to do with the CVE description however.
While we appreciate the POC in c#7, there is still the precondition of the multi-tab refresh and timing element.
Additionally in the analysis in c#10, while helpful, does not demonstrate the execution and trigging this issue in a remote and realistic scenario without mitigations of user gesture of timing issues.

### pg...@google.com (2024-06-05)

thank you for the feedback! the CVE description was updated and ive added a note to update the release notes accordingly as well

### ap...@google.com (2024-07-09)

Project: chromium/src
Branch: refs/branch-heads/6099

commit dba0f828f2b66bb4e4ea9f3122affb18bd3b8f10
Author: Taylor Bergquist <tbergquist@chromium.org>
Date:   Tue Jul 09 15:13:40 2024

    [M120-LTS] Fix container overflow when reloading multiple tabs.
    
    When multiple tabs are selected, the reload command reloads all of them.
    The selection model can change as a result of reloading a tab (e.g. when
    one of the tabs is a submitted form). The reload command is not
    expecting the selected tabs to change while it's iterating over them,
    and can end up overflowing the selected indices container.
    
    This CL simply converts the selected indices into a more-resilient
    vector of selected WebContents* before reloading anything.
    
    (cherry picked from commit 9cce0c95e740f637e1436cfa472b532c9ec35bfd)
    
    (cherry picked from commit a679cb8b0de664a7b6043fba68e1134cf1221e22)
    
    Bug: 339061099
    Change-Id: I0c0b66fc93ddcbe57b42646126a1f2ca651b2df2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5545011
    Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1303471}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5574988
    Auto-Submit: Daniel Yip <danielyip@google.com>
    Owners-Override: Daniel Yip <danielyip@google.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Original-Commit-Position: refs/branch-heads/6367@{#1241}
    Cr-Original-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5584557
    Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
    Commit-Queue: Mohamed Omar <mohamedaomar@google.com>
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com>
    Owners-Override: Mohamed Omar <mohamedaomar@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#2040}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       chrome/browser/ui/browser_commands.cc

https://chromium-review.googlesource.com/5584557


### pe...@google.com (2024-08-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339061099)*
