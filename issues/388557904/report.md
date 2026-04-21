#  access-violation on unknown address 0x7ffde90a6f3c in chrome_pdf::`anonymous namespace'::GetRotatedRectF 

| Field | Value |
|-------|-------|
| **Issue ID** | [388557904](https://issues.chromium.org/issues/388557904) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2025-01-09 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS
access-violation on unknown address 0x7ffde90a6f3c in chrome_pdf::`anonymous namespace'::GetRotatedRectF 

VERSION
Chromium	133.0.6941.0 (Developer Build) (64-bit) 
OS	Windows 11 Version 24H2 (Build 26100.2605)

REPRODUCTION CASE
1. Download the latest asan build.
2. run the command: ./chrome.exe --no-sandbox --user-data-dir=C:/tmp/zzz  http://localhost:8000/poc.html

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab]
=================================================================
==25228==ERROR: AddressSanitizer: access-violation on unknown address 0x7ffde90a6f3c (pc 0x7ff9cbff8c9e bp 0x00db1d5fb9a0 sp 0x00db1d5fb840 T0)
==25228==The signal is caused by a READ memory access.
==25228==*** WARNING: Failed to initialize DbgHelp!              ***
==25228==*** Most likely this means that the app is already      ***
==25228==*** using DbgHelp, possibly with incompatible flags.    ***
==25228==*** Due to technical reasons, symbolization might crash ***
==25228==*** or produce wrong results.                           ***
[31272:31316:0109/110645.574:ERROR:fm_registration_token_uploader.cc(186)] Client is missing for kUser scope
[31272:31316:0109/110645.574:ERROR:fm_registration_token_uploader.cc(186)] Client is missing for kUser scope
[31272:25008:0109/110646.321:ERROR:registration_request.cc(291)] Registration response error message: DEPRECATED_ENDPOINT
    #0 0x7ff9cbff8c9d in chrome_pdf::`anonymous namespace'::GetRotatedRectF C:\b\s\w\ir\cache\builder\src\pdf\pdfium\pdfium_page.cc:354
    #1 0x7ff9cbff8c9d in chrome_pdf::PDFiumPage::GetBoundingBox(void) C:\b\s\w\ir\cache\builder\src\pdf\pdfium\pdfium_page.cc:782:7
    #2 0x7ff9dbd8ad0c in chrome_pdf::PdfViewWebPlugin::HandleGetPageBoundingBoxMessage(class base::Value::Dict const &) C:\b\s\w\ir\cache\builder\src\pdf\pdf_view_web_plugin.cc:1654:35
    #3 0x7ff9dbd89fb0 in chrome_pdf::PdfViewWebPlugin::OnMessage(class base::Value::Dict const &) C:\b\s\w\ir\cache\builder\src\pdf\pdf_view_web_plugin.cc:1608:3
    #4 0x7ff9df92c078 in base::internal::DecayedFunctorTraits<void (chrome_pdf::PostMessageReceiver::Client::*)(const base::Value::Dict &),base::WeakPtr<chrome_pdf::PostMessageReceiver::Client> &&,base::Value::Dict &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:729
    #5 0x7ff9df92c078 in base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (chrome_pdf::PostMessageReceiver::Client::*&&)(const base::Value::Dict &),base::WeakPtr<chrome_pdf::PostMessageReceiver::Client> &&,base::Value::Dict &&>,void,0,1>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:945
    #6 0x7ff9df92c078 in base::internal::Invoker<base::internal::FunctorTraits<void (chrome_pdf::PostMessageReceiver::Client::*&&)(const base::Value::Dict &),base::WeakPtr<chrome_pdf::PostMessageReceiver::Client> &&,base::Value::Dict &&>,base::internal::BindState<1,1,0,void (chrome_pdf::PostMessageReceiver::Client::*)(const base::Value::Dict &),base::WeakPtr<chrome_pdf::PostMessageReceiver::Client>,base::Value::Dict>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1058
    #7 0x7ff9df92c078 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl chrome_pdf::PostMessageReceiver::Client::*&&)(class base::Value::Dict const &), class base::WeakPtr<class chrome_pdf::PostMessageReceiver::Client> &&, class base::Value::Dict &&>, struct base::internal::BindState<1, 1, 0, void (__cdecl chrome_pdf::PostMessageReceiver::Client::*)(class base::Value::Dict const &), class base::WeakPtr<class chrome_pdf::PostMessageReceiver::Client>, class base::Value::Dict>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:971:12
    #8 0x7ff9cd966acc in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #9 0x7ff9cd966acc in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:210:34
    #10 0x7ff9d29a5a94 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #11 0x7ff9d29a5a94 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:472:23
    #12 0x7ff9d29a47e9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:332:40
    #13 0x7ff9d29e761e in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40:55
    #14 0x7ff9d29a7782 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:645:12
    #15 0x7ff9cd9c4e7e in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #16 0x7ff9d19f5535 in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:337:16
    #17 0x7ff9cb731b81 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:777:14
    #18 0x7ff9cb733dc0 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1146:10
    #19 0x7ff9cb7280a5 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:348:36
    #20 0x7ff9cb728c4d in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:361:10
    #21 0x7ff9bc7a1681 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #22 0x7ff62c2b435d in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #23 0x7ff62c2b2006 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #24 0x7ff62c82f12b in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #25 0x7ff62c82f12b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #26 0x7ffaa368e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #27 0x7ffaa4e3fbcb  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800dfbcb)

==25228==Register values:
rax = 7ff9e90a6f40  rbx = db1d5fb920  rcx = 785cea1acbec  rdx = ffffffff
rdi = 12106f50f7c0  rsi = db1d5fbb40  rbp = db1d5fb9a0  rsp = db1d5fb840
r8  = 11f26fa71200  r9  = 20  r10 = 12346f806000  r11 = fdfdfdfdfdfdfdfd
r12 = db1d5fb840  r13 = 1ec6f480000  r14 = 12126f5c32c0  r15 = 0
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation C:\b\s\w\ir\cache\builder\src\pdf\pdfium\pdfium_page.cc:354 in chrome_pdf::`anonymous namespace'::GetRotatedRectF

==25228==ADDITIONAL INFO

==25228==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ff9df92b9eb in chrome_pdf::PostMessageReceiver::PostMessageW(class v8::Local<class v8::Value>) C:\b\s\w\ir\cache\builder\src\pdf\post_message_receiver.cc:131:7
    #1 0x7ff9cdc451c5 in mojo::SimpleWatcher::Context::Notify(unsigned int, struct MojoHandleSignalsState, unsigned int) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple_watcher.cc:102:13


Command line: `"./chrome.exe" --type=renderer --string-annotations --user-data-dir=C:/tmp/zzz --no-pre-read-main-dll --pdf-renderer --no-sandbox --file-url-path-alias="/gen=asan\gen" --video-capture-use-gpu-memory-buffer --lang=en-US --js-flags=--jitless --device-scale-factor=1.5 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=9 --time-ticks-at-unix-epoch=-1736218503358671 --launch-time-ticks=173501150759 --metrics-shmem-handle=4356,i,11093616363079205023,10641701609597647046,2097152 --field-trial-handle=4540,i,11787306298688871873,6099382784474387663,262144 --variations-seed-version --mojo-platform-channel-handle=4536 /prefetch:1`


==25228==END OF ADDITIONAL INFO
==25228==ABORTING

## Attachments

- poc.html (text/html, 39 B)
- poc.pdf (application/pdf, 124 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-01-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5080675354869760.

### jd...@chromium.org (2025-01-10)

Clusterfuzz is still working out some of the details here, but setting OS and FoundIn labels conservatively and passing to thestig@ for investigation.

Lei, feel free to reassign or change labels as makes sense. Thanks!

### 24...@project.gserviceaccount.com (2025-01-10)

Detailed Report: https://clusterfuzz.com/testcase?key=5080675354869760

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x5c10398be0d4
Crash State:
  chrome_pdf::PDFiumPage::GetBoundingBox
  chrome_pdf::PdfViewWebPlugin::HandleGetPageBoundingBoxMessage
  chrome_pdf::PdfViewWebPlugin::OnMessage
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1337243:1337247

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5080675354869760

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### pe...@google.com (2025-01-10)

Setting milestone because of s2 severity.

### pe...@google.com (2025-01-10)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### th...@chromium.org (2025-01-11)

FPDFPage\_GetRotation() returned -1, and PDFiumPage::GetBoundingBox() casted that to enum class Rotation which doesn't define an enum value for -1. Is it normal for ASAN to report accessing that enum as a wild read?

### ap...@google.com (2025-01-11)

Project: chromium/src  

Branch: main  

Author: Lei Zhang <[thestig@chromium.org](mailto:thestig@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6168649>

PDF: Handle FPDFPage\_GetRotation() error in PDFiumPage::GetBoundingBox()

---


Expand for full commit details
```
PDF: Handle FPDFPage_GetRotation() error in PDFiumPage::GetBoundingBox() 
 
If FPDFPage_GetRotation() returns -1, do not cast that to enum class 
Rotation, which does not have a corresponding enum value. 
 
Bug: 388557904 
Change-Id: Id6e3c788a67b6ce4c36e09b38bdb913ad548dd13 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6168649 
Commit-Queue: Lei Zhang <thestig@chromium.org> 
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com> 
Reviewed-by: Andy Phan <andyphan@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1405103}

```

---

Files:

- M `pdf/pdfium/pdfium_page.cc`

---

Hash: ba6a7c96e3ce949154a188aecb117fb04f2bc2ac  

Date:  Fri Jan 10 17:06:26 2025


---

### th...@chromium.org (2025-01-11)

ClusterFuzz will hopefully verify over the weekend.

### 24...@project.gserviceaccount.com (2025-01-11)

ClusterFuzz testcase 5080675354869760 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1405101:1405104

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2025-01-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of user information disclosure / read on an uninitialized address in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-23)

Congratulations -- thank you for your efforts and reporting this issue to us. Nice work!

### ch...@google.com (2025-04-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of user information disclosure / read on an uninitialized address in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/388557904)*
