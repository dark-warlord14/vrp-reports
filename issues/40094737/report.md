# Security: UAF in ServiceWorkerPaymentInstrument

| Field | Value |
|-------|-------|
| **Issue ID** | [40094737](https://issues.chromium.org/issues/40094737) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>ServiceWorker |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2019-04-25 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36

Steps to reproduce the problem:
1. run the attached script
$ python -m SimpleHTTPServer&
$./out/asan/chrome --user-data-dir=/tmp/xxxx "http://localhost:8080/index.html"
2. Click the pay button and then click the back button in the top left corner.
3. Change the payment method to pay by bank card and click the pay button.
4. Wait about five minutes (why? to wait for the timeout: https://cs.chromium.org/chromium/src/content/browser/service_worker/service_worker_version.cc?l=62&gsn=kRequestTimeout&rcl=3f30fd7106594d0714776efa15c7cb6af042003c).
5. Then the callback function will trigger the UAF.

What is the expected behavior?

What went wrong?
When we click the pay button, a response_helper_ will be created
https://cs.chromium.org/chromium/src/components/payments/content/payment_request_state.cc?g=0&l=302&rcl=5c24af4f7b9897f494c2a63525c2b953862a779e
And it will pass itself into service_worker_payment_instrument or autofill_payment_instrument (depend on the payment method) as a delegate.
https://cs.chromium.org/chromium/src/components/payments/content/service_worker_payment_instrument.cc?rcl=5c24af4f7b9897f494c2a63525c2b953862a779e&l=222

The OnPaymentAppInvoked function (https://cs.chromium.org/chromium/src/components/payments/content/service_worker_payment_instrument.cc?rcl=5c24af4f7b9897f494c2a63525c2b953862a779e&l=284) will be bound as a callback into IO-thread.
https://cs.chromium.org/chromium/src/content/browser/payments/payment_app_provider_impl.cc?g=0&l=375&rcl=5c24af4f7b9897f494c2a63525c2b953862a779e

And it will be called when the service worker is timed out.
https://cs.chromium.org/chromium/src/content/browser/payments/payment_app_provider_impl.cc?g=0&rcl=5c24af4f7b9897f494c2a63525c2b953862a779e&l=171

But before the timeout, we could click the back button and pay by bank card. It will create a new response_helper_ and release the old response_helper_. And we get into the autofill_payment_instrument, so the  delegate_ in service_worker_payment_instrument will not be changed, it will also point to the old response_helper_. After the time out, delegate_->OnInstrumentDetailsReady will be called and UAF will be triggered.

It may cause sandbox escape without RCE.

Did this work before? N/A 

Chrome version: 74.0.3729.108  Channel: n/a
OS Version: 10.0
Flash Version:

## Attachments

- [asan_crash](attachments/asan_crash) (text/plain, 12.5 KB)
- [index.html](attachments/index.html) (text/plain, 458 B)
- [index.html](attachments/index_53038601.html) (text/plain, 1.1 KB)
- [Selection_432.png](attachments/Selection_432.png) (image/png, 36.8 KB)
- [payment.png](attachments/payment.png) (image/png, 87.6 KB)
- [2019-04-27 01-36-16.mp4](attachments/2019-04-27 01-36-16.mp4) (video/mp4, 5.7 MB)

## Timeline

### mm...@chromium.org (2019-04-25)

Thanks for your report. Unfortunately, I have some problems reproducing the issue. For example, when I run Chrome for the first time, I cannot click the "Pay" button -- it's grey. So, I've added a card. When I run it for the second time, the card is auto-selected, so I click Pay, click Back, then I'm getting confused on the step 3. I've added one more card and switched to it, but that didn't reproduce the bug. What am I doing wrong?

### le...@gmail.com (2019-04-26)

I am sorry that I did not express it clearly. There are two payment methods: Bank card payment and Web based payment. Step 2 means to pay by Web based payment. The Web based payment method I use in index.html is 'https://bobpay.xyz/pay', which is also an example payment method in the official document( https://developers.google.com/web/fundamentals/payments/payment-apps-developer-guide/web-payment-apps). But its domain name seems to have expired, which can still be used normally yesterday. You can implement this payment service locally or use 'https://google.com/pay' or other Web based payment.

### sh...@chromium.org (2019-04-26)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2019-04-26)

If you choose to use google pay, this file may help you.

### mm...@chromium.org (2019-04-26)

I still can't click the Pay button. Please see the screenshot attached. I'm using the following build: https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-654165.zip

### le...@gmail.com (2019-04-26)

It seems the service worker of google pay is not installed, try to delete the code in index.html:

,{
	supportedMethods: 'basic-card'
}

and execute the code only through the web-based payment method.
Then execute the previous code using the same --user-data-dir after the google pay can be used.

### sh...@chromium.org (2019-04-26)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2019-04-26)

The Step 2 should be like this

### mm...@chromium.org (2019-04-26)

Do I need to set up anything in my Chrome in order to get that Google Pay method to appear?

### le...@gmail.com (2019-04-26)

No need.

### sh...@chromium.org (2019-04-26)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2019-04-26)

I recorded a video that might help you solve this problem.

### le...@gmail.com (2019-04-26)

After that, you can add a card and go to step 3, 4 and 5. 

### mm...@chromium.org (2019-04-26)

Nice, thanks so much for providing the video :) Now I'm able to replicate the flow you've described and am hoping to see the crash!

### mm...@chromium.org (2019-04-26)

Yay, I've got it! :)

$ ./chrome --user-data-dir=prof "http://localhost:8000/index.html"
[134254:134254:0426/113146.038604:ERROR:textfield.cc(1748)] Not implemented reached in virtual bool views::Textfield::ShouldDoLearning()
=================================================================
==134254==ERROR: AddressSanitizer: heap-use-after-free on address 0x6180001ce080 at pc 0x55aaecca966a bp 0x7ffc4cb14050 sp 0x7ffc4cb14048
READ of size 8 at 0x6180001ce080 thread T0 (chrome)
    #0 0x55aaecca9669 in payments::ServiceWorkerPaymentInstrument::OnPaymentAppInvoked(mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>) components/payments/content/service_worker_payment_instrument.cc:289:16
    #1 0x55aaeccae864 in Invoke<void (payments::ServiceWorkerPaymentInstrument::*)(mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>), base::WeakPtr<payments::ServiceWorkerPaymentInstrument>, mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse> > base/bind_internal.h:499:12
    #2 0x55aaeccae864 in MakeItSo<void (payments::ServiceWorkerPaymentInstrument::*)(mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>), base::WeakPtr<payments::ServiceWorkerPaymentInstrument>, mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse> > base/bind_internal.h:619
    #3 0x55aaeccae864 in RunImpl<void (payments::ServiceWorkerPaymentInstrument::*)(mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>), std::__1::tuple<base::WeakPtr<payments::ServiceWorkerPaymentInstrument> >, 0> base/bind_internal.h:672
    #4 0x55aaeccae864 in base::internal::Invoker<base::internal::BindState<void (payments::ServiceWorkerPaymentInstrument::*)(mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>), base::WeakPtr<payments::ServiceWorkerPaymentInstrument> >, void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>::RunOnce(base::internal::BindStateBase*, mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>&&) base/bind_internal.h:641
    #5 0x55aadde27a99 in Run base/callback.h:97:12
    #6 0x55aadde27a99 in Invoke<base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse> > base/bind_internal.h:560
    #7 0x55aadde27a99 in MakeItSo<base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse> > base/bind_internal.h:599
    #8 0x55aadde27a99 in RunImpl<base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, std::__1::tuple<mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse> >, 0> base/bind_internal.h:672
    #9 0x55aadde27a99 in base::internal::Invoker<base::internal::BindState<base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse> >, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:641
    #10 0x55aae3be0703 in Run base/callback.h:97:12
    #11 0x55aae3be0703 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:148
    #12 0x55aae3c13f1f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:363:23
    #13 0x55aae3c1504c in DoWork base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260:7
    #14 0x55aae3c1504c in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #15 0x55aae3b2af66 in HandleDispatch base/message_loop/message_pump_glib.cc:263:25
    #16 0x55aae3b2af66 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:109
    #17 0x7f85402add06 in g_main_context_dispatch (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4dd06)

0x6180001ce080 is located 0 bytes inside of 880-byte region [0x6180001ce080,0x6180001ce3f0)
freed by thread T0 (chrome) here:
    #0 0x55aada5dcf6d in operator delete(void*) /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:166:3
    #1 0x55aaec4a3cea in payments::PaymentSheetViewController::ButtonPressed(views::Button*, ui::Event const&) chrome/browser/ui/views/payments/payment_sheet_view_controller.cc:552:38
    #2 0x55aae9520ecf in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ui/views/controls/button/button_controller.cc:47:38
    #3 0x55aae9517364 in ui::ScopedTargetHandler::OnEvent(ui::Event*) ui/events/scoped_target_handler.cc:32:24
    #4 0x55aae5417367 in DispatchEvent ui/events/event_dispatcher.cc:193:12
    #5 0x55aae5417367 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:142
    #6 0x55aae5416aa4 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:86:14
    #7 0x55aae541678a in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:58:15
    #8 0x55aae961b95b in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ui/views/widget/root_view.cc:453:9
    #9 0x55aae9637f9b in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1254:20
    #10 0x55aae5417367 in DispatchEvent ui/events/event_dispatcher.cc:193:12
    #11 0x55aae5417367 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:142
    #12 0x55aae5416aa4 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:86:14
    #13 0x55aae541678a in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:58:15
    #14 0x55aae7a77e8e in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:57:17
    #15 0x55aae7a17d16 in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:113:16
    #16 0x55aae7a178c0 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:138:12
    #17 0x55aae96ca068 in views::DesktopWindowTreeHostX11::DispatchMouseEvent(ui::MouseEvent*) ui/views/widget/desktop_aura/desktop_window_tree_host_x11.cc:1824:5
    #18 0x55aae96cda03 in views::DesktopWindowTreeHostX11::DispatchEvent(_XEvent* const&) ui/views/widget/desktop_aura/desktop_window_tree_host_x11.cc:2174:13
    #19 0x55aae96cf26f in non-virtual thunk to views::DesktopWindowTreeHostX11::DispatchEvent(_XEvent* const&) ui/views/widget/desktop_aura/desktop_window_tree_host_x11.cc
    #20 0x55aae53e9ee5 in ui::PlatformEventSource::DispatchEvent(_XEvent*) ui/events/platform/platform_event_source.cc:101:29
    #21 0x55aae61addae in ExtractCookieDataDispatchEvent ui/events/platform/x11/x11_event_source.cc:246:14
    #22 0x55aae61addae in ui::X11EventSource::DispatchXEvents() ui/events/platform/x11/x11_event_source.cc:139
    #23 0x55aae79bdfeb in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_source_glib.cc:40:15
    #24 0x7f85402adb74 in g_main_context_dispatch (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4db74)

previously allocated by thread T0 (chrome) here:
    #0 0x55aada5dc70d in operator new(unsigned long) /b/swarming/w/ir/k/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:105:3
    #1 0x55aaecc6b86a in make_unique<payments::PaymentResponseHelper, const std::__1::basic_string<char> &, payments::PaymentRequestSpec *&, payments::PaymentInstrument *&, payments::ContentPaymentRequestDelegate *&, autofill::AutofillProfile *&, autofill::AutofillProfile *&, payments::PaymentRequestState *> buildtools/third_party/libc++/trunk/include/memory:3131:28
    #2 0x55aaecc6b86a in payments::PaymentRequestState::GeneratePaymentResponse() components/payments/content/payment_request_state.cc:302
    #3 0x55aaec4a3cea in payments::PaymentSheetViewController::ButtonPressed(views::Button*, ui::Event const&) chrome/browser/ui/views/payments/payment_sheet_view_controller.cc:552:38
    #4 0x55aae9520ecf in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ui/views/controls/button/button_controller.cc:47:38
    #5 0x55aae9517364 in ui::ScopedTargetHandler::OnEvent(ui::Event*) ui/events/scoped_target_handler.cc:32:24
    #6 0x55aae5417367 in DispatchEvent ui/events/event_dispatcher.cc:193:12
    #7 0x55aae5417367 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:142
    #8 0x55aae5416aa4 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:86:14
    #9 0x55aae541678a in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:58:15
    #10 0x55aae961b95b in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ui/views/widget/root_view.cc:453:9
    #11 0x55aae9637f9b in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1254:20
    #12 0x55aae5417367 in DispatchEvent ui/events/event_dispatcher.cc:193:12
    #13 0x55aae5417367 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:142
    #14 0x55aae5416aa4 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:86:14
    #15 0x55aae541678a in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:58:15
    #16 0x55aae7a77e8e in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:57:17
    #17 0x55aae7a17d16 in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:113:16
    #18 0x55aae7a178c0 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const*, ui::EventRewriter const*) ui/events/event_source.cc:138:12
    #19 0x55aae96ca068 in views::DesktopWindowTreeHostX11::DispatchMouseEvent(ui::MouseEvent*) ui/views/widget/desktop_aura/desktop_window_tree_host_x11.cc:1824:5
    #20 0x55aae96cda03 in views::DesktopWindowTreeHostX11::DispatchEvent(_XEvent* const&) ui/views/widget/desktop_aura/desktop_window_tree_host_x11.cc:2174:13
    #21 0x55aae96cf26f in non-virtual thunk to views::DesktopWindowTreeHostX11::DispatchEvent(_XEvent* const&) ui/views/widget/desktop_aura/desktop_window_tree_host_x11.cc
    #22 0x55aae53e9ee5 in ui::PlatformEventSource::DispatchEvent(_XEvent*) ui/events/platform/platform_event_source.cc:101:29
    #23 0x55aae61addae in ExtractCookieDataDispatchEvent ui/events/platform/x11/x11_event_source.cc:246:14
    #24 0x55aae61addae in ui::X11EventSource::DispatchXEvents() ui/events/platform/x11/x11_event_source.cc:139
    #25 0x55aae79bdfeb in ui::(anonymous namespace)::XSourceDispatch(_GSource*, int (*)(void*), void*) ui/events/platform/x11/x11_event_source_glib.cc:40:15
    #26 0x7f85402adb74 in g_main_context_dispatch (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4db74)

SUMMARY: AddressSanitizer: heap-use-after-free components/payments/content/service_worker_payment_instrument.cc:289:16 in payments::ServiceWorkerPaymentInstrument::OnPaymentAppInvoked(mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)
Shadow bytes around the buggy address:
  0x0c3080031bc0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080031bd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080031be0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080031bf0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c3080031c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c3080031c10:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080031c20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080031c30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080031c40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080031c50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080031c60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
  Shadow gap:              cc
==134254==ABORTING


[Monorail components: Blink>ServiceWorker UI>Browser>Payments]

### le...@gmail.com (2019-04-26)

Well done :P

### ro...@chromium.org (2019-04-26)

Impacts web developers that use Payment Request directly with both Google Pay and Basic Card, which is a small subset of all web developers, but still needs fixing. I'll look into it.

### ro...@chromium.org (2019-04-26)

Danyao: FYI, this is related to the service worker staying alive after cancelling payment on desktop.

### ro...@chromium.org (2019-04-26)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-26)

Just to clarify the severity, this could've been Critical, as the potential impact is RCE outside of the sandbox, but due to complicated way of reproducing this (requires user interaction + 300 sec timeout), I've assigned High. More info on the severity is available at https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md

Rouslan, if the fix is going to be straightforward, we can attempt merging this into M-75. Otherwise, M-76 should be fine, I assume.

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### ro...@chromium.org (2019-04-29)

I don't know much about Fuchsia, but Android is not affected by this, because it uses a different code path.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/761d65ebcac0cdb730fd27b87e207201ac38e3b4

commit 761d65ebcac0cdb730fd27b87e207201ac38e3b4
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Mon Apr 29 20:08:01 2019

[Payment Handler] Don't wait for response from closed payment app.

Before this patch, tapping the back button on top of the payment handler
window on desktop would not affect the |response_helper_|, which would
continue waiting for a response from the payment app. The service worker
of the closed payment app could timeout after 5 minutes and invoke the
|response_helper_|. Depending on what else the user did afterwards, in
the best case scenario, the payment sheet would display a "Transaction
failed" error message. In the worst case scenario, the
|response_helper_| would be used after free.

This patch clears the |response_helper_| in the PaymentRequestState and
in the ServiceWorkerPaymentInstrument after the payment app is closed.

After this patch, the cancelled payment app does not show "Transaction
failed" and does not use memory after it was freed.

Bug: 956597
Change-Id: I64134b911a4f8c154cb56d537a8243a68a806394
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1588682
Reviewed-by: anthonyvd <anthonyvd@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#654995}

[modify] https://crrev.com/761d65ebcac0cdb730fd27b87e207201ac38e3b4/chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc
[modify] https://crrev.com/761d65ebcac0cdb730fd27b87e207201ac38e3b4/components/payments/content/payment_request_state.cc
[modify] https://crrev.com/761d65ebcac0cdb730fd27b87e207201ac38e3b4/components/payments/content/payment_request_state.h
[modify] https://crrev.com/761d65ebcac0cdb730fd27b87e207201ac38e3b4/components/payments/content/service_worker_payment_instrument.cc
[modify] https://crrev.com/761d65ebcac0cdb730fd27b87e207201ac38e3b4/components/payments/content/service_worker_payment_instrument.h
[modify] https://crrev.com/761d65ebcac0cdb730fd27b87e207201ac38e3b4/components/payments/core/payment_instrument.h


### ro...@chromium.org (2019-04-29)

Will let this patch bake for 24 hours.

### ro...@chromium.org (2019-04-30)

Would like to merge https://crrev.com/761d65ebcac0cdb730fd27b87e207201ac38e3b4 to M-75.

### sh...@chromium.org (2019-04-30)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-04-30)

adetaylor@ can you please review this security fix merge request for M75

### sh...@chromium.org (2019-05-01)

Your change meets the bar and is auto-approved for M75. Please go ahead and merge the CL to branch 3770 (refs/branch-heads/3770) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/51c818e911b53fbf30a313c787049864f6275d07

commit 51c818e911b53fbf30a313c787049864f6275d07
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Wed May 01 13:34:11 2019

[Merge M75][PH] Don't wait for response from closed payment app.

Before this patch, tapping the back button on top of the payment handler
window on desktop would not affect the |response_helper_|, which would
continue waiting for a response from the payment app. The service worker
of the closed payment app could timeout after 5 minutes and invoke the
|response_helper_|. Depending on what else the user did afterwards, in
the best case scenario, the payment sheet would display a "Transaction
failed" error message. In the worst case scenario, the
|response_helper_| would be used after free.

This patch clears the |response_helper_| in the PaymentRequestState and
in the ServiceWorkerPaymentInstrument after the payment app is closed.

After this patch, the cancelled payment app does not show "Transaction
failed" and does not use memory after it was freed.

(cherry picked from commit 761d65ebcac0cdb730fd27b87e207201ac38e3b4)

Bug: 956597
Change-Id: I64134b911a4f8c154cb56d537a8243a68a806394
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1588682
Reviewed-by: anthonyvd <anthonyvd@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#654995}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1591414
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/branch-heads/3770@{#256}
Cr-Branched-From: a9eee1c7c727ef42a15d86e9fa7b77ff0e63840a-refs/heads/master@{#652427}

[modify] https://crrev.com/51c818e911b53fbf30a313c787049864f6275d07/chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc
[modify] https://crrev.com/51c818e911b53fbf30a313c787049864f6275d07/components/payments/content/payment_request_state.cc
[modify] https://crrev.com/51c818e911b53fbf30a313c787049864f6275d07/components/payments/content/payment_request_state.h
[modify] https://crrev.com/51c818e911b53fbf30a313c787049864f6275d07/components/payments/content/service_worker_payment_instrument.cc
[modify] https://crrev.com/51c818e911b53fbf30a313c787049864f6275d07/components/payments/content/service_worker_payment_instrument.h
[modify] https://crrev.com/51c818e911b53fbf30a313c787049864f6275d07/components/payments/core/payment_instrument.h


### sh...@chromium.org (2019-05-01)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-06)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-05-09)

Congrats! The Panel decided to reward $5,000 for this report :) 

### na...@google.com (2019-05-09)

[Empty comment from Monorail migration]

### ro...@chromium.org (2019-05-09)

Well deserved --- the report was excellent! 

### cr...@appspot.gserviceaccount.com (2019-05-10)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/51c818e911b53fbf30a313c787049864f6275d07

Commit: 51c818e911b53fbf30a313c787049864f6275d07
Author: rouslan@chromium.org
Commiter: rouslan@chromium.org
Date: 2019-05-01 13:34:11 +0000 UTC

[Merge M75][PH] Don't wait for response from closed payment app.

Before this patch, tapping the back button on top of the payment handler
window on desktop would not affect the |response_helper_|, which would
continue waiting for a response from the payment app. The service worker
of the closed payment app could timeout after 5 minutes and invoke the
|response_helper_|. Depending on what else the user did afterwards, in
the best case scenario, the payment sheet would display a "Transaction
failed" error message. In the worst case scenario, the
|response_helper_| would be used after free.

This patch clears the |response_helper_| in the PaymentRequestState and
in the ServiceWorkerPaymentInstrument after the payment app is closed.

After this patch, the cancelled payment app does not show "Transaction
failed" and does not use memory after it was freed.

(cherry picked from commit 761d65ebcac0cdb730fd27b87e207201ac38e3b4)

Bug: 956597
Change-Id: I64134b911a4f8c154cb56d537a8243a68a806394
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1588682
Reviewed-by: anthonyvd <anthonyvd@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#654995}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1591414
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/branch-heads/3770@{#256}
Cr-Branched-From: a9eee1c7c727ef42a15d86e9fa7b77ff0e63840a-refs/heads/master@{#652427}


### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-04)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-04)

Greetings, could you confirm how you'd like this credited in the release notes?

### le...@gmail.com (2019-06-04)

Thanks. I prefer "leecraso of Beihang University and Guang Gong of Alpha Team, Qihoo 360". 

### aw...@chromium.org (2019-06-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-08-07)

This issue was migrated from crbug.com/chromium/956597?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094737)*
