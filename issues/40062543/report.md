# type confusion in chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [40062543](https://issues.chromium.org/issues/40062543) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2023-01-07 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

1.  

2.a  

3.

**Problem Description:**  

a

**Additional Comments:**

\*\*Chrome version: \*\* 108.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [0001-suggest_patch.patch](attachments/0001-suggest_patch.patch) (text/plain, 1.4 KB)

## Timeline

### wx...@gmail.com (2023-01-07)

function  PopulateContextMenuItems
```c++ 
static bool PopulateContextMenuItems(v8::Isolate* isolate,
                                     const v8::Local<v8::Array>& item_array,
                                     std::vector<MenuItemInfo>& items) {
  v8::Local<v8::Context> context = isolate->GetCurrentContext();
  for (uint32_t i = 0; i < item_array->Length(); ++i) {
    v8::Local<v8::Object> item =
        item_array->Get(context, i).ToLocalChecked().As<v8::Object>();  //here just cast v8::object without any check
    v8::Local<v8::Value> type;
    v8::Local<v8::Value> id;
    v8::Local<v8::Value> label;
```


how to trigger?
1) Visit chrome://inspect
2) Open devtools (F12/Ctrl-Shift-i/etc.)
3) Click on 'other' in the left hand pane.
4) Click 'inspect' on one of the 'devtools://' targets - this opens a devtools window
5) In the devtools window console, run `DevToolsHost.showContextMenuAtPoint(1.1, 2.2, [0x41414141]);`

it will crash in debug version or TOT.

### wx...@gmail.com (2023-01-07)

I add the patch code in release version 
```c++
  for (uint32_t i = 0; i < item_array->Length(); ++i) {
    CHECK(item_array->Get(context, i).ToLocalChecked()->IsObject());  // my check
    v8::Local<v8::Object> item =
        item_array->Get(context, i).ToLocalChecked().As<v8::Object>();
```
Crash log:

[11360:20924:0107/151536.348:FATAL:v8_dev_tools_host_custom.cc(68)] Check failed: item_array->Get(context, i).ToLocalChecked()->IsObject().
Backtrace:
        base::debug::CollectStackTrace [0x00007FFBF2684162+18] (D:\work\fuzz\chromium\src\base\debug\stack_trace_win.cc:329)
        base::debug::StackTrace::StackTrace [0x00007FFBF539BEEA+26] (D:\work\fuzz\chromium\src\base\debug\stack_trace.cc:218)
        logging::LogMessage::~LogMessage [0x00007FFBF24DD818+696] (D:\work\fuzz\chromium\src\base\logging.cc:719)
        logging::LogMessage::~LogMessage [0x00007FFBF24E1470+16] (D:\work\fuzz\chromium\src\base\logging.cc:712)
        blink::PopulateContextMenuItems [0x00007FFC0591445B+9019] (D:\work\fuzz\chromium\src\third_party\blink\renderer\bindings\core\v8\custom\v8_dev_tools_host_custom.cc:68)
        blink::V8DevToolsHost::ShowContextMenuAtPointMethodCustom [0x00007FFC05911B0B+1115] (D:\work\fuzz\chromium\src\third_party\blink\renderer\bindings\core\v8\custom\v8_dev_tools_host_custom.cc:153)
        v8::internal::FunctionCallbackArguments::Call [0x00007FFBE9A1671C+1004] (D:\work\fuzz\chromium\src\v8\src\api\api-arguments-inl.h:146)
        v8::internal::`anonymous namespace'::HandleApiCallHelper<0> [0x00007FFBE9A13BE0+2400] (D:\work\fuzz\chromium\src\v8\src\builtins\builtins-api.cc:113)
        v8::internal::Builtin_Impl_HandleApiCall [0x00007FFBE9A115D5+1013] (D:\work\fuzz\chromium\src\v8\src\builtins\builtins-api.cc:148)
        v8::internal::Builtin_HandleApiCall [0x00007FFBE9A10951+305] (D:\work\fuzz\chromium\src\v8\src\builtins\builtins-api.cc:135)
        (No symbol) [0x00007FFB9FE9AA3C]
Task trace:
Backtrace:
        IPC::`anonymous namespace'::ChannelAssociatedGroupController::Accept [0x00007FFBF2E69D3B+3581] (D:\work\fuzz\chromium\src\ipc\ipc_mojo_bootstrap.cc:1018)

### [Deleted User] (2023-01-07)

[Empty comment from Monorail migration]

### wx...@gmail.com (2023-01-07)

[Comment Deleted]

### wx...@gmail.com (2023-01-07)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-01-09)

No crash in M108 asan build following these directions. Can you have a look again and provide another way to reproduce?

### wx...@gmail.com (2023-01-09)

I still can produce. It will only crash in debug build or release build with my check patch

### dc...@chromium.org (2023-01-13)

Stack trace with dcheck asan at r1092052 (DCHECK is almost certainly sufficient)

#
# Fatal error in ../../v8/src/api/api-inl.h, line 130
# Debug check failed: that == nullptr || v8::internal::Object( *reinterpret_cast<const v8::internal::Address*>(that)) .IsJSReceiver().
#
#
#
#FailureMessage Object: 0x7f45153a8060#0 0x55616186e807 (/usr/local/google/home/dcheng/src/chrome-moo/src/out/asan/chrome+0x11444806)
    #0 0x556176f731a2 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:899:7
    #1 0x556176bc0133 in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace.cc:221:12
    #2 0x556176bc0133 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:218:28
    #3 0x55617f105d2c in gin::(anonymous namespace)::PrintStackTrace() ./../../gin/v8_platform.cc:45:27
    #4 0x55617e34ed1f in V8_Fatal(char const*, int, char const*, ...) ./../../v8/src/base/logging.cc:164:38
    #5 0x55617e34ddcf in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) ./../../v8/src/base/logging.cc:57:3
    #6 0x5561679c6b78 in v8::Utils::OpenHandle(v8::Object const*, bool) ./../../v8/src/api/api-inl.h:130:1
    #7 0x5561679c6b78 in v8::Object::Get(v8::Local<v8::Context>, v8::Local<v8::Value>) ./../../v8/src/api/api.cc:4730:15
    #8 0x5561903ea212 in blink::PopulateContextMenuItems(v8::Isolate*, v8::Local<v8::Array> const&, std::Cr::vector<blink::MenuItemInfo, std::Cr::allocator<blink::MenuItemInfo>>&) ./../../third_party/blink/renderer/bindings/core/v8/custom/v8_dev_tools_host_custom.cc:76:16
    #9 0x5561903e98bc in blink::V8DevToolsHost::ShowContextMenuAtPointMethodCustom(v8::FunctionCallbackInfo<v8::Value> const&) ./../../third_party/blink/renderer/bindings/core/v8/custom/v8_dev_tools_host_custom.cc:152:8
    #10 0x556167befe13 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:146:3
    #11 0x556167be9b00 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, unsigned long*, int) ./../../v8/src/builtins/builtins-api.cc:113:36
    #12 0x556167be6557 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:148:5
    #13 0x556167be54b6 in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:135:1
#13 0x5560ffeafcf8 <unknown>
[0113/015216.974395:WARNING:exception_snapshot_linux.cc(349)] thread ID 1 not found in process
[0113/015216.974673:ERROR:process_snapshot_linux.cc(129)] thread not found 1
Received signal 4 ILL_ILLOPN 55617e382d78
    #0 0x55616186e807 in backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4434:13
    #1 0x556176f731a2 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:899:7
    #2 0x556176bc0133 in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace.cc:221:12
    #3 0x556176bc0133 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:218:28
    #4 0x556176f71c1b in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:392:3
    #5 0x7f451825af90 in __GI___sigaction :?
    #6 0x55617e382d78 in v8::base::OS::Abort()::$_0::operator()() const ./../../v8/src/base/platform/platform-posix.cc:685:5
    #7 0x55617e382d78 in v8::base::OS::Abort() ./../../v8/src/base/platform/platform-posix.cc:685:5
    #8 0x55617e34ed4e in V8_Fatal(char const*, int, char const*, ...) ./../../v8/src/base/logging.cc:167:3
    #9 0x55617e34ddcf in v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) ./../../v8/src/base/logging.cc:57:3
    #10 0x5561679c6b78 in v8::Utils::OpenHandle(v8::Object const*, bool) ./../../v8/src/api/api-inl.h:130:1
    #11 0x5561679c6b78 in v8::Object::Get(v8::Local<v8::Context>, v8::Local<v8::Value>) ./../../v8/src/api/api.cc:4730:15
    #12 0x5561903ea212 in blink::PopulateContextMenuItems(v8::Isolate*, v8::Local<v8::Array> const&, std::Cr::vector<blink::MenuItemInfo, std::Cr::allocator<blink::MenuItemInfo>>&) ./../../third_party/blink/renderer/bindings/core/v8/custom/v8_dev_tools_host_custom.cc:76:16
    #13 0x5561903e98bc in blink::V8DevToolsHost::ShowContextMenuAtPointMethodCustom(v8::FunctionCallbackInfo<v8::Value> const&) ./../../third_party/blink/renderer/bindings/core/v8/custom/v8_dev_tools_host_custom.cc:152:8
    #14 0x556167befe13 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:146:3
    #15 0x556167be9b00 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, unsigned long*, int) ./../../v8/src/builtins/builtins-api.cc:113:36
    #16 0x556167be6557 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:148:5
    #17 0x556167be54b6 in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:135:1
#15 0x5560ffeafcf8 <unknown>
  r8: 000055619749d118  r9: 0000000000000000 r10: efffffffffffffff r11: 0000000000000202
 r12: 00000fe8a307e508 r13: 00007f45153a8020 r14: 00007f45183f2840 r15: 00007f45153a8060
  di: 00007f4514ef7000  si: 0000000000000001  bp: 00007ffd7e040970  bx: 00007ffd7e040980
  dx: 00007f45194e5000  ax: 623aa5efc8467300  cx: 00007f4514ef7000  sp: 00007ffd7e040970
  ip: 000055617e382d78 efl: 0000000000010202 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000006 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]

This is a type confusion bug in the renderer, which would normally be high due to the potential for allowing an attacker to potentially gain arbitrary code execution. However, the severity is mitigated by the user interactions required to trigger this.

(I think this may affect Android as well; however, IIRC, using devtools on Android requires adb...)

[Monorail components: Platform>DevTools]

### [Deleted User] (2023-01-13)

[Empty comment from Monorail migration]

### ya...@google.com (2023-01-13)

I think the severity is fairly low since this cannot be programatically exploited. User interaction is necessary in order to execute arbitrary JS code in the DevTools' context.

However, I agree that we should get this fixed.

The fix is to perform an object check here: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/bindings/core/v8/custom/v8_dev_tools_host_custom.cc;l=69;drc=c60368c4e84069693180aedbe1ece21d25837501

And it would be nice to add a test similar to this https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/http/tests/devtools/elements/copy-styles.js;l=25;drc=047c7dc4ee1ce908d7fea38ca063fa2f80f92c77

### ya...@google.com (2023-01-13)

Benedikt, could you find someone on your team to carry out this work? It should be fairly straightforward.

### bm...@chromium.org (2023-01-13)

Danil, please take a look.

### [Deleted User] (2023-01-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-13)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/954e76692edf965e588ee80350c20ad403f82ea0

commit 954e76692edf965e588ee80350c20ad403f82ea0
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Jan 17 05:28:30 2023

Check arguments type in DevToolsHost.showContextMenuAtPoint

Bug: 1405574
Change-Id: Id06637839096402e05a2278b06f2f84b3037e21d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4165089
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1093205}

[add] https://crrev.com/954e76692edf965e588ee80350c20ad403f82ea0/third_party/blink/web_tests/http/tests/devtools/show-context-menu.js
[modify] https://crrev.com/954e76692edf965e588ee80350c20ad403f82ea0/third_party/blink/renderer/bindings/core/v8/custom/v8_dev_tools_host_custom.cc
[add] https://crrev.com/954e76692edf965e588ee80350c20ad403f82ea0/third_party/blink/web_tests/http/tests/devtools/show-context-menu-expected.txt


### ds...@chromium.org (2023-01-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

Requesting merge to beta M110 because latest trunk commit (1093205) appears to be after beta branch point (1084008).

Merge review required: M110 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2023-01-19)

1. https://chromium-review.googlesource.com/c/chromium/src/+/4165089
2. Yes
3. Should be fine
4. No
5. See https://crbug.com/chromium/1405574#c1

### am...@chromium.org (2023-01-19)

M110 merge approved, please merge this fix to branch 5481 at your earliest convenience 

### go...@chromium.org (2023-01-20)

[Bulk Edit]

Please merge your change to M110 branch ASAP.

Branch details: https://chromiumdash.appspot.com/branches

### gi...@appspot.gserviceaccount.com (2023-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0c132a0677828ef5e5fd71eefa33a47fd8779bc0

commit 0c132a0677828ef5e5fd71eefa33a47fd8779bc0
Author: Danil Somsikov <dsv@chromium.org>
Date: Fri Jan 20 15:04:49 2023

[M110] Check arguments type in DevToolsHost.showContextMenuAtPoint

(cherry picked from commit 954e76692edf965e588ee80350c20ad403f82ea0)

Bug: 1405574
Change-Id: Id06637839096402e05a2278b06f2f84b3037e21d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4165089
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1093205}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4183821
Cr-Commit-Position: refs/branch-heads/5481@{#498}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[add] https://crrev.com/0c132a0677828ef5e5fd71eefa33a47fd8779bc0/third_party/blink/web_tests/http/tests/devtools/show-context-menu.js
[modify] https://crrev.com/0c132a0677828ef5e5fd71eefa33a47fd8779bc0/third_party/blink/renderer/bindings/core/v8/custom/v8_dev_tools_host_custom.cc
[add] https://crrev.com/0c132a0677828ef5e5fd71eefa33a47fd8779bc0/third_party/blink/web_tests/http/tests/devtools/show-context-menu-expected.txt


### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-27)

Congratulations! The VRP Panel has decided to award you $1,000 for this report of a very heavily mitigated security bug. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2023-07-06)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-13)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-13)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-07-13)

1. https://crrev.com/c/4682776
2. Low - small change, no conflicts
3. M110
4. Yes

### gm...@google.com (2023-07-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e22a9d0d03c6b11a6bf783ef2ad8c00a9fc8881b

commit e22a9d0d03c6b11a6bf783ef2ad8c00a9fc8881b
Author: Danil Somsikov <dsv@chromium.org>
Date: Mon Jul 17 02:27:49 2023

[M108-LTS] Check arguments type in DevToolsHost.showContextMenuAtPoint

(cherry picked from commit 954e76692edf965e588ee80350c20ad403f82ea0)

(cherry picked from commit 0c132a0677828ef5e5fd71eefa33a47fd8779bc0)

Bug: 1405574
Change-Id: Id06637839096402e05a2278b06f2f84b3037e21d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4165089
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Kouhei Ueno <kouhei@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1093205}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4183821
Cr-Original-Commit-Position: refs/branch-heads/5481@{#498}
Cr-Original-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4682776
Owners-Override: Simon Hangl <simonha@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Simon Hangl <simonha@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1491}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[add] https://crrev.com/e22a9d0d03c6b11a6bf783ef2ad8c00a9fc8881b/third_party/blink/web_tests/http/tests/devtools/show-context-menu.js
[modify] https://crrev.com/e22a9d0d03c6b11a6bf783ef2ad8c00a9fc8881b/third_party/blink/renderer/bindings/core/v8/custom/v8_dev_tools_host_custom.cc
[add] https://crrev.com/e22a9d0d03c6b11a6bf783ef2ad8c00a9fc8881b/third_party/blink/web_tests/http/tests/devtools/show-context-menu-expected.txt


### vo...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1405574?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062543)*
