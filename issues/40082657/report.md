# Security: Heap-use-after-free in UsbContext::UsbEventHandler::Stop

| Field | Value |
|-------|-------|
| **Issue ID** | [40082657](https://issues.chromium.org/issues/40082657) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Platform>Extensions>API |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@chromium.org |
| **Created** | 2015-08-10 |
| **Bounty** | $3,000.00 |

## Description

I encountered a UAF when I opened chrome://inspect/#devices and closed Chrome. These two actions can be automated by an extension, and probably also by an app using the chrome.usb API, so this issue could be abused when a user installs a malicious extension/app (the extension doesn't need any permissions, the app would require usb permissions).

The sequence leading to the UAF seems to be:

void UsbContext::UsbEventHandler::ThreadMain() {
  ...
  while (base::subtle::Acquire_Load(&running_)) { // 3. Signalled.
    ...
  delete this;                                    // 4. Freed UsbContext::UsbEventHandler
}
void UsbContext::UsbEventHandler::Stop() {
  base::subtle::Release_Store(&running_, 0);      // 1. Signal other thread
  libusb_interrupt_handle_event(context_);        // 2. Some I/O in a third-party library.
  base::PlatformThread::Join(thread_handle_);     // 5. UAF.
}

Storing the thread handle in a local variable before signaling will probably solve the above problem.
This is a regression and introduced with 0fa66a8dc57470d805c22eea20c29dfec2c4d634 (45.0.2430.0, currently on the beta channel).


==29292==ERROR: AddressSanitizer: heap-use-after-free on address 0x603000424888 at pc 0x56355024571b bp 0x7ffcdd9a8af0 sp 0x7ffcdd9a8ae8
READ of size 8 at 0x603000424888 thread T0 (chromium)
    #0 0x56355024571a in Stop device/usb/usb_context.cc:66:30
    #1 0x56355024571a in ~UsbContext device/usb/usb_context.cc:76:0
    #2 0x56355024571a in device::UsbContext::~UsbContext() device/usb/usb_context.cc:74:0
    #3 0x563550232221 in DeleteInternal base/memory/ref_counted.h:193:44
    #4 0x563550232221 in Destruct base/memory/ref_counted.h:156:0
    #5 0x563550232221 in Release base/memory/ref_counted.h:184:0
    #6 0x563550232221 in Release base/memory/ref_counted.h:403:0
    #7 0x563550232221 in ~scoped_refptr base/memory/ref_counted.h:298:0
    #8 0x563550232221 in device::UsbServiceImpl::~UsbServiceImpl() device/usb/usb_service_impl.cc:593:0
    #9 0x56355023235d in device::UsbServiceImpl::~UsbServiceImpl() device/usb/usb_service_impl.cc:584:35
    #10 0x563548ed5b6d in base::MessageLoop::~MessageLoop() base/message_loop/message_loop.cc:166:3
    #11 0x563548c4689d in base::MessageLoopForUI::~MessageLoopForUI() base/message_loop/message_loop.h:564:19
    #12 0x5635513de40d in content::BrowserMainLoop::~BrowserMainLoop() content/browser/browser_main_loop.cc:401:37
    #13 0x563550e28d6a in operator() base/memory/scoped_ptr.h:128:5
    #14 0x563550e28d6a in reset base/memory/scoped_ptr.h:248:0
    #15 0x563550e28d6a in reset base/memory/scoped_ptr.h:377:0
    #16 0x563550e28d6a in content::BrowserMainRunnerImpl::Shutdown() content/browser/browser_main_runner.cc:268:0
    #17 0x563550e27ceb in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:28:3
    #18 0x563548e01a7d in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:792:12
    #19 0x563548dff1fa in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:15
    #20 0x56354812ebe2 in ChromeMain chrome/app/chrome_main.cc:66:12
    #21 0x7f406ff5b78f in __libc_start_main ??:0:0

0x603000424888 is located 24 bytes inside of 32-byte region [0x603000424870,0x603000424890)
freed by thread T36 (UsbEventHandler) here:
    #0 0x56354812d0db in operator delete(void*) ??:0:0
    #1 0x56355024531d in device::UsbContext::UsbEventHandler::ThreadMain() device/usb/usb_context.cc:60:3
    #2 0x563548f5b17e in base::(anonymous namespace)::ThreadFunc(void*) base/threading/platform_thread_posix.cc:64:3
    #3 0x7f4071754353 in start_thread ??:0:0

previously allocated by thread T0 (chromium) here:
    #0 0x56354812cb1b in operator new(unsigned long) ??:0:0
    #1 0x56355024544c in device::UsbContext::UsbContext(libusb_context*) device/usb/usb_context.cc:71:20
    #2 0x563550230bfe in device::UsbServiceImpl::UsbServiceImpl(libusb_context*, scoped_refptr<base::SequencedTaskRunner>) device/usb/usb_service_impl.cc:555:20
    #3 0x5635502309d0 in device::UsbServiceImpl::Create(scoped_refptr<base::SequencedTaskRunner>) device/usb/usb_service_impl.cc:549:14
    #4 0x56355022e386 in device::UsbService::GetInstance(scoped_refptr<base::SequencedTaskRunner>) device/usb/usb_service.cc:36:5
    #5 0x5635489ab751 in ChromeDeviceClient::GetUsbService() chrome/browser/chrome_device_client.cc:20:10
    #6 0x563548c08371 in (anonymous namespace)::EnumerateOnUIThread(crypto::RSAPrivateKey*, base::Callback<void (std::__1::vector<scoped_refptr<AndroidUsbDevice>, std::__1::allocator<scoped_refptr<AndroidUsbDevice> > > const&)> const&, scoped_refptr<base::SingleThreadTaskRunner>) chrome/browser/devtools/device/usb/android_usb_device.cc:281:25
    #7 0x563548c147bf in Run base/bind_internal.h:157:12
    #8 0x563548c147bf in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(crypto::RSAPrivateKey*, base::Callback<void (std::__1::vector<scoped_refptr<AndroidUsbDevice>, std::__1::allocator<scoped_refptr<AndroidUsbDevice> > > const&)> const&, scoped_refptr<base::SingleThreadTaskRunner>)>, base::internal::TypeList<crypto::RSAPrivateKey* const&, base::Callback<void (std::__1::vector<scoped_refptr<AndroidUsbDevice>, std::__1::allocator<scoped_refptr<AndroidUsbDevice> > > const&)> const&, base::SingleThreadTaskRunner*> >::MakeItSo(base::internal::RunnableAdapter<void (*)(crypto::RSAPrivateKey*, base::Callback<void (std::__1::vector<scoped_refptr<AndroidUsbDevice>, std::__1::allocator<scoped_refptr<AndroidUsbDevice> > > const&)> const&, scoped_refptr<base::SingleThreadTaskRunner>)>, crypto::RSAPrivateKey* const&, base::Callback<void (std::__1::vector<scoped_refptr<AndroidUsbDevice>, std::__1::allocator<scoped_refptr<AndroidUsbDevice> > > const&)> const&, base::SingleThreadTaskRunner*) base/bind_internal.h:293:0
    #9 0x563548fb1cd2 in Run base/callback.h:396:12
    #10 0x563548fb1cd2 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:49:0
    #11 0x563548ed935f in base::MessageLoop::RunTask(base::PendingTask const&) base/message_loop/message_loop.cc:481:3
    #12 0x563548eda7e4 in DeferOrRunPendingTask base/message_loop/message_loop.cc:490:5
    #13 0x563548eda7e4 in base::MessageLoop::DoWork() base/message_loop/message_loop.cc:602:0
    #14 0x563548faed97 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:313:31
    #15 0x563548f0aac8 in base::RunLoop::Run() base/run_loop.cc:55:3
    #16 0x5635488068d1 in ChromeBrowserMainParts::MainMessageLoopRun(int*) chrome/browser/chrome_browser_main.cc:1731:3
    #17 0x5635513e897e in content::BrowserMainLoop::RunMainMessageLoopParts() content/browser/browser_main_loop.cc:890:21
    #18 0x563550e28a15 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner.cc:211:5
    #19 0x563550e27cb8 in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:26:15
    #20 0x563548e01a7d in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:792:12
    #21 0x563548dff1fa in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:15
    #22 0x56354812ebe2 in ChromeMain chrome/app/chrome_main.cc:66:12
    #23 0x7f406ff5b78f in __libc_start_main ??:0:0

Thread T36 (UsbEventHandler) created by T0 (chromium) here:
    #0 0x5635480ef7b9 in __interceptor_pthread_create ??:0:0
    #1 0x563548f5ab0a in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, base::PlatformThreadHandle*, base::ThreadPriority) base/threading/platform_thread_posix.cc:103:13
    #2 0x5635502454ee in Create base/threading/platform_thread.h:161:12
    #3 0x5635502454ee in UsbEventHandler device/usb/usb_context.cc:39:0
    #4 0x5635502454ee in device::UsbContext::UsbContext(libusb_context*) device/usb/usb_context.cc:71:0
    #5 0x563550230bfe in device::UsbServiceImpl::UsbServiceImpl(libusb_context*, scoped_refptr<base::SequencedTaskRunner>) device/usb/usb_service_impl.cc:555:20
    #6 0x5635502309d0 in device::UsbServiceImpl::Create(scoped_refptr<base::SequencedTaskRunner>) device/usb/usb_service_impl.cc:549:14
    #7 0x56355022e386 in device::UsbService::GetInstance(scoped_refptr<base::SequencedTaskRunner>) device/usb/usb_service.cc:36:5
    #8 0x5635489ab751 in ChromeDeviceClient::GetUsbService() chrome/browser/chrome_device_client.cc:20:10
    #9 0x563548c08371 in (anonymous namespace)::EnumerateOnUIThread(crypto::RSAPrivateKey*, base::Callback<void (std::__1::vector<scoped_refptr<AndroidUsbDevice>, std::__1::allocator<scoped_refptr<AndroidUsbDevice> > > const&)> const&, scoped_refptr<base::SingleThreadTaskRunner>) chrome/browser/devtools/device/usb/android_usb_device.cc:281:25
    #10 0x563548c147bf in Run base/bind_internal.h:157:12
    #11 0x563548c147bf in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (*)(crypto::RSAPrivateKey*, base::Callback<void (std::__1::vector<scoped_refptr<AndroidUsbDevice>, std::__1::allocator<scoped_refptr<AndroidUsbDevice> > > const&)> const&, scoped_refptr<base::SingleThreadTaskRunner>)>, base::internal::TypeList<crypto::RSAPrivateKey* const&, base::Callback<void (std::__1::vector<scoped_refptr<AndroidUsbDevice>, std::__1::allocator<scoped_refptr<AndroidUsbDevice> > > const&)> const&, base::SingleThreadTaskRunner*> >::MakeItSo(base::internal::RunnableAdapter<void (*)(crypto::RSAPrivateKey*, base::Callback<void (std::__1::vector<scoped_refptr<AndroidUsbDevice>, std::__1::allocator<scoped_refptr<AndroidUsbDevice> > > const&)> const&, scoped_refptr<base::SingleThreadTaskRunner>)>, crypto::RSAPrivateKey* const&, base::Callback<void (std::__1::vector<scoped_refptr<AndroidUsbDevice>, std::__1::allocator<scoped_refptr<AndroidUsbDevice> > > const&)> const&, base::SingleThreadTaskRunner*) base/bind_internal.h:293:0
    #12 0x563548fb1cd2 in Run base/callback.h:396:12
    #13 0x563548fb1cd2 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:49:0
    #14 0x563548ed935f in base::MessageLoop::RunTask(base::PendingTask const&) base/message_loop/message_loop.cc:481:3
    #15 0x563548eda7e4 in DeferOrRunPendingTask base/message_loop/message_loop.cc:490:5
    #16 0x563548eda7e4 in base::MessageLoop::DoWork() base/message_loop/message_loop.cc:602:0
    #17 0x563548faed97 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:313:31
    #18 0x563548f0aac8 in base::RunLoop::Run() base/run_loop.cc:55:3
    #19 0x5635488068d1 in ChromeBrowserMainParts::MainMessageLoopRun(int*) chrome/browser/chrome_browser_main.cc:1731:3
    #20 0x5635513e897e in content::BrowserMainLoop::RunMainMessageLoopParts() content/browser/browser_main_loop.cc:890:21
    #21 0x563550e28a15 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner.cc:211:5
    #22 0x563550e27cb8 in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:26:15
    #23 0x563548e01a7d in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:792:12
    #24 0x563548dff1fa in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:15
    #25 0x56354812ebe2 in ChromeMain chrome/app/chrome_main.cc:66:12
    #26 0x7f406ff5b78f in __libc_start_main ??:0:0

SUMMARY: AddressSanitizer: heap-use-after-free (/tmp/46.0.2476.0-asan/chromium+0xa7b571a)
Shadow bytes around the buggy address:
  0x0c068007c8c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c068007c8d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c068007c8e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c068007c8f0: fa fa fa fa fa fa 00 00 00 fa fa fa fd fd fd fd
  0x0c068007c900: fa fa fd fd fd fd fa fa fd fd fd fa fa fa fd fd
=>0x0c068007c910: fd[fd]fa fa fd fd fd fa fa fa fd fd fd fa fa fa
  0x0c068007c920: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fa
  0x0c068007c930: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd
  0x0c068007c940: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa
  0x0c068007c950: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fa
  0x0c068007c960: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
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
==29292==ABORTING



## Timeline

### js...@chromium.org (2015-08-10)

[Empty comment from Monorail migration]

### ro...@chromium.org (2015-08-10)

Nice catch. I agree that copying before signaling in Stop should resolve this. Fix incoming.

### bu...@chromium.org (2015-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3219ab0a9caf806b6dda0fe970869735726a5481

commit 3219ab0a9caf806b6dda0fe970869735726a5481
Author: rockot <rockot@chromium.org>
Date: Mon Aug 10 18:49:35 2015

Fix UAF on libusb thread

BUG=518749
TBR=reillyg@chromium.org

Review URL: https://codereview.chromium.org/1275223005

Cr-Commit-Position: refs/heads/master@{#342653}

[modify] http://crrev.com/3219ab0a9caf806b6dda0fe970869735726a5481/device/usb/usb_context.cc


### bu...@chromium.org (2015-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7ecee444661e8b855c15171615d68162602c39fa

commit 7ecee444661e8b855c15171615d68162602c39fa
Author: reillyg <reillyg@chromium.org>
Date: Mon Aug 10 22:18:54 2015

Remove "delete this" pattern from UsbContext completely.

This change fixes a much rarer possible use-after-free on USB context
shutdown than commit 3219ab0a9caf806b6dda0fe970869735726a5481. If there
is an event that wakes up the event loop thread after running_ is set to
false then the context could be freed before the attempt to wake it up
with libusb_interrupt_handle_event() is made, instead signaling a freed
object.

This change instead makes it the responsibility of UsbContext to free
the UsbEventHandler once its thread has been joined.

BUG=518749
R=rockot@chromium.org

Review URL: https://codereview.chromium.org/1281373002

Cr-Commit-Position: refs/heads/master@{#342711}

[modify] http://crrev.com/7ecee444661e8b855c15171615d68162602c39fa/device/usb/usb_context.cc
[modify] http://crrev.com/7ecee444661e8b855c15171615d68162602c39fa/device/usb/usb_context.h


### re...@chromium.org (2015-08-11)

Requesting a merge of the second patch (which removes the code added in the first patch as a result of the more generic solution) to M-45.

### cl...@chromium.org (2015-08-11)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### re...@chromium.org (2015-08-11)

Thanks clusterfuzz!

### pe...@google.com (2015-08-11)

Approved for M45 (branch: 2454)

### bu...@chromium.org (2015-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fb1944dab73e2db9807a40bcfe84d901d38aa29e

commit fb1944dab73e2db9807a40bcfe84d901d38aa29e
Author: Reilly Grant <reillyg@chromium.org>
Date: Tue Aug 11 22:56:58 2015

Merge M45: Remove "delete this" pattern from UsbContext completely.

This change fixes a much rarer possible use-after-free on USB context
shutdown than commit 3219ab0a9caf806b6dda0fe970869735726a5481. If there
is an event that wakes up the event loop thread after running_ is set to
false then the context could be freed before the attempt to wake it up
with libusb_interrupt_handle_event() is made, instead signaling a freed
object.

This change instead makes it the responsibility of UsbContext to free
the UsbEventHandler once its thread has been joined.

BUG=518749
R=rockot@chromium.org

Review URL: https://codereview.chromium.org/1281373002

Cr-Commit-Position: refs/heads/master@{#342711}
(cherry-picked from commit 7ecee444661e8b855c15171615d68162602c39fa)

Review URL: https://codereview.chromium.org/1291543002 .

Cr-Commit-Position: refs/branch-heads/2454@{#286}
Cr-Branched-From: 12bfc3360892ec53cd00fc239a47e5298beb063b-refs/heads/master@{#338390}

[modify] http://crrev.com/fb1944dab73e2db9807a40bcfe84d901d38aa29e/device/usb/usb_context.cc
[modify] http://crrev.com/fb1944dab73e2db9807a40bcfe84d901d38aa29e/device/usb/usb_context.h


### cl...@chromium.org (2015-08-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-08-12)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/fb1944dab73e2db9807a40bcfe84d901d38aa29e

commit fb1944dab73e2db9807a40bcfe84d901d38aa29e
Author: Reilly Grant <reillyg@chromium.org>
Date: Tue Aug 11 22:56:58 2015


### ro...@robwu.nl (2015-08-13)

Verified that the bug does not occur any more, as follows:

1. Start an ASAN build of Chrome with a new profile.
2. Set the "On startup" setting to "Open a specific page or set of pages" (chrome://inspect).
3. Visit chrome://inspect and quit Chrome.

4. If step 3 did not cause the UAF, start Chrome again (which conveniently navigates to chrome://inspect thanks to step 2) and quit Chrome.

Without the patch, ASAN would show a UAF within a few attempts.

With the patch, there is no UAF any more.

### ti...@google.com (2015-08-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-18)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-30)

We're through the reward backlog of head/beta bugs!

$3,000 for this report Rob. 

Panel notes: limited to chrome:// scheme and also required an extension - mitigating circumstances.

I'll add this to the payment run for next week.

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/518749?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082657)*
