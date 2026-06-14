# Security: Crash in content::`anonymous namespace'::OnInstallPaymentApp

| Field | Value |
|-------|-------|
| **Issue ID** | [40096130](https://issues.chromium.org/issues/40096130) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Payments |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2019-08-28 |
| **Bounty** | $10,000.00 |

## Description

Chrome Version: 78.0.3895.0 (Official Build) canary (64-bit)
Operating System: MacOS

1. Lunch a new incognito window and open the test case.
2. Click somewhere.
3. After two seconds click on the backward arrow to go back to the test case 
4. Click quickly on the forward arrow to go google.com 

This bug can take several tries to repro the crash.

Crash/5aeab74ab0211af7
Crash/065f11b472669947
Crash/90ca055271a42d04

rax=0000000012b8b2b0 rbx=000000000098e620 rcx=0000000012b8b2b0
rdx=00000000131943d0 rsi=000000000098e630 rdi=000000000098e628
rip=000007feebf05b77 rsp=000000000098e4e0 rbp=000007feef1fee58
 r8=0000000000000000  r9=000007feebf05b70 r10=0000000400000004
r11=000007feec401bc1 r12=0000000000000000 r13=000000000098e598
r14=000000001d5d4128 r15=0000000000000000
iopl=0         nv up ei pl nz na pe nc
cs=0033  ss=0000  ds=0000  es=0000  fs=0053  gs=002b             efl=00010202
*** WARNING: Unable to verify checksum for chrome.dll
chrome_7feeb7a0000!rlz::RLZTracker::WrapperURLLoaderFactory::`vcall'{8}'+0x7:
000007fe`ebf05b77 4d8b5208        mov     r10,qword ptr [r10+8] ds:00000004`0000000c=????????????????
0:000> k
  *** Stack trace for last set context - .thread/.cxr resets it
Child-SP          RetAddr           Call Site
00000000`0098e4e0 000007fe`ec401c25 chrome_7feeb7a0000!rlz::RLZTracker::WrapperURLLoaderFactory::`vcall'{8}'+0x7
00000000`0098e510 000007fe`ec40445d chrome_7feeb7a0000!content::`anonymous namespace'::OnInstallPaymentApp+0x64 [c:\b\s\w\ir\cache\builder\src\content\browser\payments\payment_app_provider_impl.cc @ 421]
00000000`0098e5f0 000007fe`ec3ffd1a chrome_7feeb7a0000!base::internal::Invoker<base::internal::BindState<void (*)(const url::Origin &, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext *, long long),url::Origin,mojo::StructPtr<payments::mojom::PaymentRequestEventData>,base::OnceCallback<void (long long)>,base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)> >,void (content::BrowserContext *, long long)>::RunOnce+0x6b [c:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 641]
00000000`0098e650 000007fe`eb7e1d51 chrome_7feeb7a0000!content::`anonymous namespace'::SelfDeleteInstaller::FinishInstallation+0x9a [c:\b\s\w\ir\cache\builder\src\content\browser\payments\payment_app_installer.cc @ 0]
00000000`0098e6a0 000007fe`eb7df645 chrome_7feeb7a0000!base::TaskAnnotator::RunTask+0x121 [c:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 142]
00000000`0098e7a0 000007fe`eb7df3a1 chrome_7feeb7a0000!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x185 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 366]
00000000`0098e970 000007fe`eb84ce04 chrome_7feeb7a0000!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork+0x61 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 221]
00000000`0098ea00 000007fe`eb7e6c7e chrome_7feeb7a0000!base::MessagePumpForUI::DoRunLoop+0xc4 [c:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 218]
00000000`0098eac0 000007fe`eb7df1f6 chrome_7feeb7a0000!base::MessagePumpWin::Run+0x4e [c:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 76]
00000000`0098eb10 000007fe`eb7deb7e chrome_7feeb7a0000!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x86 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 463]
00000000`0098eb60 000007fe`eba65a83 chrome_7feeb7a0000!base::RunLoop::Run+0x1ae [c:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 158]
00000000`0098ec00 000007fe`eba6595f chrome_7feeb7a0000!ChromeBrowserMainParts::MainMessageLoopRun+0x53 [c:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc @ 1857]
00000000`0098ec90 000007fe`eba6591d chrome_7feeb7a0000!content::BrowserMainLoop::RunMainMessageLoopParts+0x35 [c:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc @ 1002]
00000000`0098ed10 000007fe`eb7f682c chrome_7feeb7a0000!content::BrowserMainRunnerImpl::Run+0x11 [c:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc @ 150]
00000000`0098ed40 000007fe`eb7f674e chrome_7feeb7a0000!content::BrowserMain+0xc5 [c:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc @ 47]
00000000`0098ede0 000007fe`eb7acbc8 chrome_7feeb7a0000!content::RunBrowserProcessMain+0x59 [c:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 544]
00000000`0098ee40 000007fe`eb7ac94f chrome_7feeb7a0000!content::ContentMainRunnerImpl::RunServiceManager+0x248 [c:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 950]
00000000`0098eee0 000007fe`eb7a29f3 chrome_7feeb7a0000!content::ContentMainRunnerImpl::Run+0x173 [c:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 0]
00000000`0098f0a0 000007fe`eb7a246b chrome_7feeb7a0000!service_manager::Main+0x4b4 [c:\b\s\w\ir\cache\builder\src\services\service_manager\embedder\main.cc @ 423]
00000000`0098f350 000007fe`eb7a15ad chrome_7feeb7a0000!content::ContentMain+0x3e [c:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 19]


## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 441.7 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)

## Timeline

### ct...@chromium.org (2019-08-28)

I was able to reproduce this on an ASAN build of r690908 (see full asan log below). For reproducing, I had to click the forward arrow (in step #4) _before_ it became clickable again visually.

Tentatively setting this to Sev-Critical: This appears to be a use-after-free in the browser process. While the current repro for this requires a fair bit of manual interaction to trigger it, I'm not currently convinced that this couldn't be worked around with a more clever exploit. If we decide that the user interaction is a hard requirement (and not just a way to trigger an otherwise reachable race condition) then we may be able to downgrade this to a Sev-High.

Adding payments owners: please help investigate this as soon as you are able. For Sev-Critical bugs we aim to deliver a fix to all affected Chrome users in 30 days. Please reach out if you have any questions. Thanks!

I'll work on bisecting this to determine the impact and I will update this bug when I have more details.

ASAN log below:

==175587==ERROR: AddressSanitizer: heap-use-after-free on address 0x6180001d48a0 at pc 0x55e4dff3f606 bp 0x7ffe3973bfd0 sp 0x7ffe3973bfc8
READ of size 8 at 0x6180001d48a0 thread T0 (chrome)
    #0 0x55e4dff3f605 in void base::internal::FunctorTraits<void (payments::ServiceWorkerPaymentInstrument::IdentityObserver::*)(url::Origin const&, long), void>::Invoke<void (payments::ServiceWorkerPaymentInstrument::IdentityObserver::*)(url::Origin const&, long), payments::ServiceWorkerPaymentInstrument::IdentityObserver*, url::Origin, long>(void (payments::ServiceWorkerPaymentInstrument::IdentityObserver::*)(url::Origin const&, long), payments::ServiceWorkerPaymentInstrument::IdentityObserver*&&, url::Origin&&, long&&) base/bind_internal.h:499:12
    #1 0x55e4dff3f2be in void base::internal::InvokeHelper<false, void>::MakeItSo<void (payments::ServiceWorkerPaymentInstrument::IdentityObserver::*)(url::Origin const&, long), payments::ServiceWorkerPaymentInstrument::IdentityObserver*, url::Origin, long>(void (payments::ServiceWorkerPaymentInstrument::IdentityObserver::*&&)(url::Origin const&, long), payments::ServiceWorkerPaymentInstrument::IdentityObserver*&&, url::Origin&&, long&&) base/bind_internal.h:599:12
    #2 0x55e4dff3eff6 in void base::internal::Invoker<base::internal::BindState<void (payments::ServiceWorkerPaymentInstrument::IdentityObserver::*)(url::Origin const&, long), base::internal::UnretainedWrapper<payments::ServiceWorkerPaymentInstrument::IdentityObserver>, url::Origin>, void (long)>::RunImpl<void (payments::ServiceWorkerPaymentInstrument::IdentityObserver::*)(url::Origin const&, long), std::__Cr::tuple<base::internal::UnretainedWrapper<payments::ServiceWorkerPaymentInstrument::IdentityObserver>, url::Origin>, 0ul, 1ul>(void (payments::ServiceWorkerPaymentInstrument::IdentityObserver::*&&)(url::Origin const&, long), std::__Cr::tuple<base::internal::UnretainedWrapper<payments::ServiceWorkerPaymentInstrument::IdentityObserver>, url::Origin>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, long&&) base/bind_internal.h:672:12
    #3 0x55e4dff3ed57 in base::internal::Invoker<base::internal::BindState<void (payments::ServiceWorkerPaymentInstrument::IdentityObserver::*)(url::Origin const&, long), base::internal::UnretainedWrapper<payments::ServiceWorkerPaymentInstrument::IdentityObserver>, url::Origin>, void (long)>::RunOnce(base::internal::BindStateBase*, long) base/bind_internal.h:641:12
    #4 0x7f2eb0113971 in base::OnceCallback<void (long)>::Run(long) && base/callback.h:98:12
    #5 0x7f2eb235a9b6 in content::(anonymous namespace)::OnInstallPaymentApp(url::Origin const&, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext*, long) content/browser/payments/payment_app_provider_impl.cc:421:41
    #6 0x7f2eb2381b39 in void base::internal::FunctorTraits<void (*)(url::Origin const&, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext*, long), void>::Invoke<void (*)(url::Origin const&, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext*, long), url::Origin, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext*, long>(void (*&&)(url::Origin const&, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext*, long), url::Origin&&, mojo::StructPtr<payments::mojom::PaymentRequestEventData>&&, base::OnceCallback<void (long)>&&, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>&&, content::BrowserContext*&&, long&&) base/bind_internal.h:399:12
    #7 0x7f2eb238179f in void base::internal::InvokeHelper<false, void>::MakeItSo<void (*)(url::Origin const&, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext*, long), url::Origin, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext*, long>(void (*&&)(url::Origin const&, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext*, long), url::Origin&&, mojo::StructPtr<payments::mojom::PaymentRequestEventData>&&, base::OnceCallback<void (long)>&&, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>&&, content::BrowserContext*&&, long&&) base/bind_internal.h:599:12
    #8 0x7f2eb23816cf in void base::internal::Invoker<base::internal::BindState<void (*)(url::Origin const&, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext*, long), url::Origin, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)> >, void (content::BrowserContext*, long)>::RunImpl<void (*)(url::Origin const&, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext*, long), std::__Cr::tuple<url::Origin, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)> >, 0ul, 1ul, 2ul, 3ul>(void (*&&)(url::Origin const&, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext*, long), std::__Cr::tuple<url::Origin, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)> >&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>, content::BrowserContext*&&, long&&) base/bind_internal.h:672:12
    #9 0x7f2eb2381497 in base::internal::Invoker<base::internal::BindState<void (*)(url::Origin const&, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)>, content::BrowserContext*, long), url::Origin, mojo::StructPtr<payments::mojom::PaymentRequestEventData>, base::OnceCallback<void (long)>, base::OnceCallback<void (mojo::InlinedStructPtr<payments::mojom::PaymentHandlerResponse>)> >, void (content::BrowserContext*, long)>::RunOnce(base::internal::BindStateBase*, content::BrowserContext*, long) base/bind_internal.h:641:12
    #10 0x7f2eb2353dbb in base::OnceCallback<void (content::BrowserContext*, long)>::Run(content::BrowserContext*, long) && base/callback.h:98:12
    #11 0x7f2eb234f8b5 in content::(anonymous namespace)::SelfDeleteInstaller::FinishInstallation(bool) content/browser/payments/payment_app_installer.cc:182:28
    #12 0x7f2eb2350180 in void base::internal::FunctorTraits<void (content::(anonymous namespace)::SelfDeleteInstaller::*)(bool), void>::Invoke<void (content::(anonymous namespace)::SelfDeleteInstaller::*)(bool), scoped_refptr<content::(anonymous namespace)::SelfDeleteInstaller>, bool>(void (content::(anonymous namespace)::SelfDeleteInstaller::*)(bool), scoped_refptr<content::(anonymous namespace)::SelfDeleteInstaller>&&, bool&&) base/bind_internal.h:499:12
    #13 0x7f2eb234fe05 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (content::(anonymous namespace)::SelfDeleteInstaller::*)(bool), scoped_refptr<content::(anonymous namespace)::SelfDeleteInstaller>, bool>(void (content::(anonymous namespace)::SelfDeleteInstaller::*&&)(bool), scoped_refptr<content::(anonymous namespace)::SelfDeleteInstaller>&&, bool&&) base/bind_internal.h:599:12
    #14 0x7f2eb234fbe2 in void base::internal::Invoker<base::internal::BindState<void (content::(anonymous namespace)::SelfDeleteInstaller::*)(bool), scoped_refptr<content::(anonymous namespace)::SelfDeleteInstaller>, bool>, void ()>::RunImpl<void (content::(anonymous namespace)::SelfDeleteInstaller::*)(bool), std::__Cr::tuple<scoped_refptr<content::(anonymous namespace)::SelfDeleteInstaller>, bool>, 0ul, 1ul>(void (content::(anonymous namespace)::SelfDeleteInstaller::*&&)(bool), std::__Cr::tuple<scoped_refptr<content::(anonymous namespace)::SelfDeleteInstaller>, bool>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>) base/bind_internal.h:672:12
    #15 0x7f2eb234faf8 in base::internal::Invoker<base::internal::BindState<void (content::(anonymous namespace)::SelfDeleteInstaller::*)(bool), scoped_refptr<content::(anonymous namespace)::SelfDeleteInstaller>, bool>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:641:12
    #16 0x7f2ec50c3104 in base::OnceCallback<void ()>::Run() && base/callback.h:98:12
    #17 0x7f2ec557b125 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:142:33
    #18 0x7f2ec565fbe1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365:23
    #19 0x7f2ec565dfad in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #20 0x7f2ec56606ae in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #21 0x7f2ec52bece1 in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:392:46
    #22 0x7f2ec52c147a in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:108:43
    #23 0x7f2e13bccd86 in g_main_context_dispatch (/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4dd86)

0x6180001d48a0 is located 32 bytes inside of 832-byte region [0x6180001d4880,0x6180001d4bc0)
freed by thread T0 (chrome) here:
    #0 0x55e4ce28443d in operator delete(void*) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:160:3
    #1 0x55e4dfdcbf47 in payments::PaymentRequest::~PaymentRequest() components/payments/content/payment_request.cc:107:35
    #2 0x55e4dff1dd3f in std::__Cr::default_delete<payments::PaymentRequest>::operator()(payments::PaymentRequest*) const buildtools/third_party/libc++/trunk/include/memory:2338:5
    #3 0x55e4dff1dcb8 in std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> >::reset(payments::PaymentRequest*) buildtools/third_party/libc++/trunk/include/memory:2651:7
    #4 0x55e4dff1bca8 in std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> >::~unique_ptr() buildtools/third_party/libc++/trunk/include/memory:2605:19
    #5 0x55e4dff1cc6d in std::__Cr::pair<payments::PaymentRequest* const, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >::~pair() buildtools/third_party/libc++/trunk/include/utility:315:29
    #6 0x55e4dff1cc48 in void std::__Cr::allocator_traits<std::__Cr::allocator<std::__Cr::__tree_node<std::__Cr::__value_type<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >, void*> > >::__destroy<std::__Cr::pair<payments::PaymentRequest* const, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > > >(std::__Cr::integral_constant<bool, false>, std::__Cr::allocator<std::__Cr::__tree_node<std::__Cr::__value_type<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >, void*> >&, std::__Cr::pair<payments::PaymentRequest* const, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >*) buildtools/third_party/libc++/trunk/include/memory:1747:23
    #7 0x55e4dff1cb2e in void std::__Cr::allocator_traits<std::__Cr::allocator<std::__Cr::__tree_node<std::__Cr::__value_type<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >, void*> > >::destroy<std::__Cr::pair<payments::PaymentRequest* const, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > > >(std::__Cr::allocator<std::__Cr::__tree_node<std::__Cr::__value_type<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >, void*> >&, std::__Cr::pair<payments::PaymentRequest* const, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >*) buildtools/third_party/libc++/trunk/include/memory:1595:14
    #8 0x55e4dff213ee in std::__Cr::__tree<std::__Cr::__value_type<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >, std::__Cr::__map_value_compare<payments::PaymentRequest*, std::__Cr::__value_type<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >, std::__Cr::less<payments::PaymentRequest*>, true>, std::__Cr::allocator<std::__Cr::__value_type<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > > > >::erase(std::__Cr::__tree_const_iterator<std::__Cr::__value_type<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >, std::__Cr::__tree_node<std::__Cr::__value_type<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >, void*>*, long>) buildtools/third_party/libc++/trunk/include/__tree:2561:5
    #9 0x55e4dff20dc1 in unsigned long std::__Cr::__tree<std::__Cr::__value_type<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >, std::__Cr::__map_value_compare<payments::PaymentRequest*, std::__Cr::__value_type<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > >, std::__Cr::less<payments::PaymentRequest*>, true>, std::__Cr::allocator<std::__Cr::__value_type<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > > > >::__erase_unique<payments::PaymentRequest*>(payments::PaymentRequest* const&) buildtools/third_party/libc++/trunk/include/__tree:2584:5
    #10 0x55e4dff1c1ac in std::__Cr::map<payments::PaymentRequest*, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> >, std::__Cr::less<payments::PaymentRequest*>, std::__Cr::allocator<std::__Cr::pair<payments::PaymentRequest* const, std::__Cr::unique_ptr<payments::PaymentRequest, std::__Cr::default_delete<payments::PaymentRequest> > > > >::erase(payments::PaymentRequest* const&) buildtools/third_party/libc++/trunk/include/map:1304:25
    #11 0x55e4dff1ac6b in payments::PaymentRequestWebContentsManager::DestroyRequest(payments::PaymentRequest*) components/payments/content/payment_request_web_contents_manager.cc:61:21
    #12 0x55e4dfdd5e51 in payments::PaymentRequest::UserCancelled() components/payments/content/payment_request.cc:649:13
    #13 0x55e4deb567f7 in payments::PaymentRequestDialogView::Cancel() chrome/browser/ui/views/payments/payment_request_dialog_view.cc:126:13
    #14 0x7f2e80ef2b0a in views::DialogDelegate::Close() ui/views/window/dialog_delegate.cc:156:12
    #15 0x7f2e80ee9832 in views::DialogClientView::CanClose() ui/views/window/dialog_client_view.cc:120:52
    #16 0x7f2e80f04f7e in views::NonClientView::CanClose() ui/views/window/non_client_view.cc:87:24
    #17 0x7f2e80eb5323 in views::Widget::CloseWithReason(views::Widget::ClosedReason) ui/views/widget/widget.cc:587:46
    #18 0x7f2e80eb5bc6 in views::Widget::Close() ui/views/widget/widget.cc:615:3
    #19 0x55e4dfdbed50 in constrained_window::NativeWebContentsModalDialogManagerViews::Close() components/constrained_window/native_web_contents_modal_dialog_manager_views.cc:129:24
    #20 0x55e4da3d2ac4 in web_modal::WebContentsModalDialogManager::CloseAllDialogs() components/web_modal/web_contents_modal_dialog_manager.cc:124:37
    #21 0x55e4da3d2d0e in web_modal::WebContentsModalDialogManager::DidFinishNavigation(content::NavigationHandle*) components/web_modal/web_contents_modal_dialog_manager.cc:139:5
    #22 0x7f2eb36280db in content::WebContentsImpl::DidFinishNavigation(content::NavigationHandle*) content/browser/web_contents/web_contents_impl.cc:4400:14
    #23 0x7f2eb155b6b8 in content::NavigationRequest::~NavigationRequest() content/browser/frame_host/navigation_request.cc:945:20
    #24 0x7f2eb155c2eb in content::NavigationRequest::~NavigationRequest() content/browser/frame_host/navigation_request.cc:931:41
    #25 0x7f2eb149576f in std::__Cr::default_delete<content::NavigationRequest>::operator()(content::NavigationRequest*) const buildtools/third_party/libc++/trunk/include/memory:2338:5
    #26 0x7f2eb1487e08 in std::__Cr::unique_ptr<content::NavigationRequest, std::__Cr::default_delete<content::NavigationRequest> >::reset(content::NavigationRequest*) buildtools/third_party/libc++/trunk/include/memory:2651:7
    #27 0x7f2eb15d726b in content::NavigatorImpl::DidNavigate(content::RenderFrameHostImpl*, FrameHostMsg_DidCommitProvisionalLoad_Params const&, std::__Cr::unique_ptr<content::NavigationRequest, std::__Cr::default_delete<content::NavigationRequest> >, bool) content/browser/frame_host/navigator_impl.cc:314:24
    #28 0x7f2eb161ed3b in content::RenderFrameHostImpl::DidCommitNavigationInternal(std::__Cr::unique_ptr<content::NavigationRequest, std::__Cr::default_delete<content::NavigationRequest> >, FrameHostMsg_DidCommitProvisionalLoad_Params*, bool) content/browser/frame_host/render_frame_host_impl.cc:6792:35
    #29 0x7f2eb161cdee in content::RenderFrameHostImpl::DidCommitNavigation(std::__Cr::unique_ptr<content::NavigationRequest, std::__Cr::default_delete<content::NavigationRequest> >, std::__Cr::unique_ptr<FrameHostMsg_DidCommitProvisionalLoad_Params, std::__Cr::default_delete<FrameHostMsg_DidCommitProvisionalLoad_Params> >, mojo::StructPtr<content::mojom::DidCommitProvisionalLoadInterfaceParams>) content/browser/frame_host/render_frame_host_impl.cc:7101:8

previously allocated by thread T0 (chrome) here:
    #0 0x55e4ce283bdd in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:99:3
    #1 0x55e4dff1b6b2 in std::__Cr::__unique_if<payments::PaymentRequest>::__unique_single std::__Cr::make_unique<payments::PaymentRequest, content::RenderFrameHost*&, content::WebContents*&, std::__Cr::unique_ptr<payments::ContentPaymentRequestDelegate, std::__Cr::default_delete<payments::ContentPaymentRequestDelegate> >, payments::PaymentRequestWebContentsManager*, payments::PaymentRequestDisplayManager*, mojo::InterfaceRequest<payments::mojom::PaymentRequest>, payments::PaymentRequest::ObserverForTest*&>(content::RenderFrameHost*&, content::WebContents*&, std::__Cr::unique_ptr<payments::ContentPaymentRequestDelegate, std::__Cr::default_delete<payments::ContentPaymentRequestDelegate> >&&, payments::PaymentRequestWebContentsManager*&&, payments::PaymentRequestDisplayManager*&&, mojo::InterfaceRequest<payments::mojom::PaymentRequest>&&, payments::PaymentRequest::ObserverForTest*&) buildtools/third_party/libc++/trunk/include/memory:3131:28
    #2 0x55e4dff1a505 in payments::PaymentRequestWebContentsManager::CreatePaymentRequest(content::RenderFrameHost*, content::WebContents*, std::__Cr::unique_ptr<payments::ContentPaymentRequestDelegate, std::__Cr::default_delete<payments::ContentPaymentRequestDelegate> >, mojo::InterfaceRequest<payments::mojom::PaymentRequest>, payments::PaymentRequest::ObserverForTest*) components/payments/content/payment_request_web_contents_manager.cc:35:22
    #3 0x55e4d664e257 in payments::CreatePaymentRequest(mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*) chrome/browser/payments/payment_request_factory.cc:42:9
    #4 0x55e4d48fe4c1 in void base::internal::FunctorTraits<void (*)(mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*), void>::Invoke<void (* const&)(mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*), mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*>(void (* const&)(mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*), mojo::InterfaceRequest<payments::mojom::PaymentRequest>&&, content::RenderFrameHost*&&) base/bind_internal.h:399:12
    #5 0x55e4d48fe326 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (* const&)(mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*), mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*>(void (* const&)(mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*), mojo::InterfaceRequest<payments::mojom::PaymentRequest>&&, content::RenderFrameHost*&&) base/bind_internal.h:599:12
    #6 0x55e4d48fe2ba in void base::internal::Invoker<base::internal::BindState<void (*)(mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*)>, void (mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*)>::RunImpl<void (* const&)(mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*), std::__Cr::tuple<> const&>(void (* const&)(mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*), std::__Cr::tuple<> const&, std::__Cr::integer_sequence<unsigned long>, mojo::InterfaceRequest<payments::mojom::PaymentRequest>&&, content::RenderFrameHost*&&) base/bind_internal.h:672:12
    #7 0x55e4d48fe17b in base::internal::Invoker<base::internal::BindState<void (*)(mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*)>, void (mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*)>::Run(base::internal::BindStateBase*, mojo::InterfaceRequest<payments::mojom::PaymentRequest>&&, content::RenderFrameHost*) base/bind_internal.h:654:12
    #8 0x55e4d49006ed in base::RepeatingCallback<void (mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*)>::Run(mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*) const & base/callback.h:132:12
    #9 0x55e4d48ff6e8 in service_manager::CallbackBinder<payments::mojom::PaymentRequest, content::RenderFrameHost*>::RunCallback(base::RepeatingCallback<void (mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*)> const&, mojo::InterfaceRequest<payments::mojom::PaymentRequest>, content::RenderFrameHost*) services/service_manager/public/cpp/interface_binder.h:76:14
    #10 0x55e4d48ff2fc in service_manager::CallbackBinder<payments::mojom::PaymentRequest, content::RenderFrameHost*>::BindInterface(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, content::RenderFrameHost*) services/service_manager/public/cpp/interface_binder.h:69:7
    #11 0x55e4d03df660 in service_manager::BinderRegistryWithArgs<content::RenderFrameHost*>::BindInterface(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, content::RenderFrameHost*) services/service_manager/public/cpp/binder_registry.h:96:19
    #12 0x55e4d03dd2c5 in service_manager::BinderRegistryWithArgs<content::RenderFrameHost*>::TryBindInterface(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, mojo::ScopedHandleBase<mojo::MessagePipeHandle>*, content::RenderFrameHost*) services/service_manager/public/cpp/binder_registry.h:125:7
    #13 0x55e4d48929ec in ChromeContentBrowserClient::BindInterfaceRequestFromFrame(content::RenderFrameHost*, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, mojo::ScopedHandleBase<mojo::MessagePipeHandle>) chrome/browser/chrome_content_browser_client.cc:3815:41
    #14 0x7f2eb165548f in content::RenderFrameHostImpl::GetInterface(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, mojo::ScopedHandleBase<mojo::MessagePipeHandle>) content/browser/frame_host/render_frame_host_impl.cc:6294:38
    #15 0x7f2ea4d71151 in service_manager::mojom::InterfaceProviderStubDispatch::Accept(service_manager::mojom::InterfaceProvider*, mojo::Message*) gen/services/service_manager/public/mojom/interface_provider.mojom.cc:138:13
    #16 0x7f2eb16c6892 in service_manager::mojom::InterfaceProviderStub<mojo::RawPtrImplRefTraits<service_manager::mojom::InterfaceProvider> >::Accept(mojo::Message*) gen/services/service_manager/public/mojom/interface_provider.mojom.h:125:12
    #17 0x7f2ec600d99c in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:554:54
    #18 0x7f2ec600c89a in mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:140:18
    #19 0x7f2ec6008c36 in mojo::FilterChain::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/filter_chain.cc:40:17
    #20 0x7f2ec6012d0b in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:357:19
    #21 0x7f2ec603cb15 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) mojo/public/cpp/bindings/lib/multiplex_router.cc:877:42
    #22 0x7f2ec603b2dc in mojo::internal::MultiplexRouter::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/multiplex_router.cc:598:38
    #23 0x7f2ec6008c36 in mojo::FilterChain::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/filter_chain.cc:40:17
    #24 0x7f2ec5fc6869 in mojo::Connector::DispatchMessage(mojo::Message) mojo/public/cpp/bindings/lib/connector.cc:514:49
    #25 0x7f2ec5fc9797 in mojo::Connector::ReadAllAvailableMessages() mojo/public/cpp/bindings/lib/connector.cc:589:12
    #26 0x7f2ec5fc8bf8 in mojo::Connector::OnHandleReadyInternal(unsigned int) mojo/public/cpp/bindings/lib/connector.cc:422:3
    #27 0x7f2ec5fc889a in mojo::Connector::OnWatcherHandleReady(unsigned int) mojo/public/cpp/bindings/lib/connector.cc:383:3
    #28 0x7f2ec5fe165e in void base::internal::FunctorTraits<void (mojo::Connector::*)(unsigned int), void>::Invoke<void (mojo::Connector::*)(unsigned int), mojo::Connector*, unsigned int>(void (mojo::Connector::*)(unsigned int), mojo::Connector*&&, unsigned int&&) base/bind_internal.h:499:12
    #29 0x7f2ec5fe1295 in void base::internal::InvokeHelper<false, void>::MakeItSo<void (mojo::Connector::* const&)(unsigned int), mojo::Connector*, unsigned int>(void (mojo::Connector::* const&)(unsigned int), mojo::Connector*&&, unsigned int&&) base/bind_internal.h:599:12

SUMMARY: AddressSanitizer: heap-use-after-free base/bind_internal.h:499:12 in void base::internal::FunctorTraits<void (payments::ServiceWorkerPaymentInstrument::IdentityObserver::*)(url::Origin const&, long), void>::Invoke<void (payments::ServiceWorkerPaymentInstrument::IdentityObserver::*)(url::Origin const&, long), payments::ServiceWorkerPaymentInstrument::IdentityObserver*, url::Origin, long>(void (payments::ServiceWorkerPaymentInstrument::IdentityObserver::*)(url::Origin const&, long), payments::ServiceWorkerPaymentInstrument::IdentityObserver*&&, url::Origin&&, long&&)
Shadow bytes around the buggy address:
  0x0c30800328c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c30800328d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c30800328e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c30800328f0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0c3080032900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c3080032910: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080032920: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080032930: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080032940: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080032950: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080032960: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==175587==ABORTING

[Monorail components: Blink>Payments UI>Browser>Payments]

### mp...@google.com (2019-08-28)

It looks critical severity, as the deletion path here is triggered by tearing down UI with the back button, but I'm pretty sure you can trigger the same PaymentRequestWebContentsManager::DestroyRequest from JS simply by calling abort() on the PaymentRequest, see here: https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/payments/payment_request.cc?rcl=b4cf908d54223181b17058e757d3a3b7013d13c6&l=1366

In any case the bug the base::Unretained pointer to a PaymentRequest is taken here: https://cs.chromium.org/chromium/src/components/payments/content/service_worker_payment_instrument.cc?rcl=dc4bc92406d1791cecaf5b22d881aba9c0abd2e6&l=236

And the callback is later called using the possibly-deleted pointer on successful OnInstallPaymentApp.

Since PaymentRequest objects can be trivially deleted directly from JS, we need to be sure that there aren't any base::Unretained(payment_request_ptr)'s lying around elsewhere. We may want to ref-count PaymentRequest's or use true WeakPtr's.

### ct...@chromium.org (2019-08-29)

Removing extraneous label.

### ct...@chromium.org (2019-08-29)

In earlier revisions, this is easier to trigger. For example:

On r670016 this only takes clicking the back button after 2 seconds (no fast interactions).
On r669968 this crashes without any user interaction (after triggering the payment request).

The earliest revision that I was able to get it to crash was r669944, but no nearby commits seem relevant.

Updating this to Impact-Beta for now, and I'll see if I can track down a real bisect soon.



### ct...@chromium.org (2019-08-29)

[Empty comment from Monorail migration]

### ro...@chromium.org (2019-08-29)

> Since PaymentRequest objects can be trivially deleted directly from JS, we need to be sure that there aren't any base::Unretained(payment_request_ptr)'s lying around elsewhere. We may want to ref-count PaymentRequest's or use true WeakPtr's.

Good point, I will comb through the component for base::Unreated being used in production code. Preliminary search shows 19 instances that I can convert to WeakPtrs:

https://cs.chromium.org/search/?q=file:payment+-file:test+base::Unretained&sq=package:chromium&type=cs

### ro...@chromium.org (2019-08-29)

The IdentityObserver interface was added in r685529: https://crrev.com/c/1742207 . The crashes from the older revisions must be coming from another base::Unretained() in the code.

### sh...@chromium.org (2019-08-29)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2019-08-29)

Patch in review @ https://crrev.com/c/1776225

### dg...@google.com (2019-08-29)

 rouslan@ can you please weigh in if this should indeed block M77 Beta today? Thanks

### ro...@chromium.org (2019-08-29)

dgagnon@: It should be OK to cut a beta release today. I will merge the fix into M-77 ASAP after it lands. It's currently in the CQ.

### ro...@chromium.org (2019-08-29)

FYI, IdentityObserver that is causing the crashes was added in M-78.

https://chromiumdash.appspot.com/commit/1f95f0902dedf67aa8a9bf78dfa47afbbfe5942c

### dg...@google.com (2019-08-29)

Great, thank you.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6555229a7ab0bfa07a9a778204fac44baa2309ab

commit 6555229a7ab0bfa07a9a778204fac44baa2309ab
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Thu Aug 29 17:28:21 2019

[Web Payment] base::Unretained considered harmful.

It's very difficult to use base::Unretained correctly, because it
requires careful, correct, manual management of object lifetime. This is
amplified in Web Payment API component, where the renderer can terminate
the Mojo connection, which deletes the corresponding Mojo service in the
browser process. As a mitigation, this patch replaces all 30 uses of
base::Unretained from the Web Payment API component.

After this patch, the following command prints no output:
$ git grep base::Unretained | grep -i payment | grep -v test | grep -v components/autofill

Bug: 998679
Change-Id: I198cfe4495942bfdfa15be7e5b97ff0b676ae1de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1776225
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: Danyao Wang <danyao@chromium.org>
Cr-Commit-Position: refs/heads/master@{#691692}

[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/chrome/browser/android/payments/service_worker_payment_app_bridge.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/chrome/browser/ui/views/payments/credit_card_editor_view_controller.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/chrome/browser/ui/views/payments/credit_card_editor_view_controller.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/chrome/browser/ui/views/payments/payment_method_view_controller.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/chrome/browser/ui/views/payments/payment_request_dialog_view.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/chrome/browser/ui/views/payments/payment_request_sheet_controller.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/chrome/browser/ui/views/payments/payment_request_sheet_controller.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/chrome/browser/ui/views/payments/payment_sheet_view_controller.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/chrome/browser/ui/views/payments/profile_list_view_controller.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/chrome/browser/ui/views/payments/shipping_address_editor_view_controller.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/chrome/browser/ui/views/payments/shipping_address_editor_view_controller.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/mock_identity_observer.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/mock_identity_observer.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/payment_details_converter.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/payment_details_converter.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/payment_handler_host.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/payment_handler_host.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/payment_instrument_unittest.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/payment_request.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/payment_request_state.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/payment_request_state.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/payment_request_state_unittest.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/service_worker_payment_app_factory.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/service_worker_payment_instrument.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/service_worker_payment_instrument.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/content/service_worker_payment_instrument_unittest.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/core/autofill_payment_instrument.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/core/autofill_payment_instrument.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/core/can_make_payment_query.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/core/can_make_payment_query.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/core/payment_instrument.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/core/payment_manifest_downloader.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/components/payments/core/payment_manifest_downloader.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/content/browser/payments/payment_app_info_fetcher.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/content/browser/payments/payment_app_info_fetcher.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/content/browser/payments/payment_manager.cc
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/ios/chrome/browser/payments/ios_payment_instrument.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/ios/chrome/browser/payments/ios_payment_instrument.mm
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/ios/chrome/browser/payments/payment_request.h
[modify] https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab/ios/chrome/browser/payments/payment_request.mm


### ro...@chromium.org (2019-08-29)

I would like to merge https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab into M-77 because it fixes a range of crashes from tearing down the PaymentRequest instance and UI, including this bug here. The patch is a bug-fix and is not a new feature.

### sh...@chromium.org (2019-08-29)

This bug requires manual review: We are only 11 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2019-08-29)

chromium.khalil@ and cthomp@: Could you double check that the use-after-free is fixed after r691692?

### ro...@chromium.org (2019-08-29)

> 1. Does your merge fit within the Merge Decision Guidelines?
> - Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
> - Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Yes

> 2. Links to the CLs you are requesting to merge.

https://crrev.com/6555229a7ab0bfa07a9a778204fac44baa2309ab

> 3. Has the change landed and been verified on master/ToT?

Landed and verified on ToT.

> 4. Why are these changes required in this milestone after branch?

Fix a security bug.

> 5. Is this a new feature?

No, this is a bug fix.

> 6. If it is a new feature, is it behind a flag using finch?

N/A

### mp...@google.com (2019-08-29)

Nice job removing every usage of base::Unretained!

### ct...@chromium.org (2019-08-29)

Manually testing on trunk I wasn't able to reproduce the crash anymore.

### la...@google.com (2019-08-29)

merge approved for M77 branch 3865

### ch...@gmail.com (2019-08-29)

I can’t reproduce this either any more. Thanks for the quick fix! 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fb75c3db2b7f03d0f11b5fd9500b777566b872e0

commit fb75c3db2b7f03d0f11b5fd9500b777566b872e0
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Thu Aug 29 20:46:52 2019

Merge M-77: [Web Payment] base::Unretained considered harmful.

It's very difficult to use base::Unretained correctly, because it
requires careful, correct, manual management of object lifetime. This is
amplified in Web Payment API component, where the renderer can terminate
the Mojo connection, which deletes the corresponding Mojo service in the
browser process. As a mitigation, this patch replaces all 30 uses of
base::Unretained from the Web Payment API component.

After this patch, the following command prints no output:
$ git grep base::Unretained | grep -i payment | grep -v test | grep -v components/autofill

TBR=rouslan@chromium.org

(cherry picked from commit 6555229a7ab0bfa07a9a778204fac44baa2309ab)

Bug: 998679
Change-Id: I198cfe4495942bfdfa15be7e5b97ff0b676ae1de
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1776225
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: Danyao Wang <danyao@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#691692}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1776799
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/branch-heads/3865@{#676}
Cr-Branched-From: 0cdcc6158160790658d1f033d3db873603250124-refs/heads/master@{#681094}

[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/chrome/browser/ui/views/payments/credit_card_editor_view_controller.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/chrome/browser/ui/views/payments/credit_card_editor_view_controller.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/chrome/browser/ui/views/payments/payment_method_view_controller.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/chrome/browser/ui/views/payments/payment_request_dialog_view.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/chrome/browser/ui/views/payments/payment_request_sheet_controller.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/chrome/browser/ui/views/payments/payment_request_sheet_controller.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/chrome/browser/ui/views/payments/payment_sheet_view_controller.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/chrome/browser/ui/views/payments/profile_list_view_controller.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/chrome/browser/ui/views/payments/shipping_address_editor_view_controller.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/chrome/browser/ui/views/payments/shipping_address_editor_view_controller.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/content/payment_details_converter.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/content/payment_details_converter.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/content/payment_handler_host.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/content/payment_handler_host.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/content/payment_request.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/content/payment_request_state.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/content/payment_request_state.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/content/service_worker_payment_app_factory.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/content/service_worker_payment_instrument.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/content/service_worker_payment_instrument.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/core/autofill_payment_instrument.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/core/autofill_payment_instrument.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/core/can_make_payment_query.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/core/can_make_payment_query.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/core/payment_instrument.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/core/payment_manifest_downloader.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/components/payments/core/payment_manifest_downloader.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/content/browser/payments/payment_app_info_fetcher.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/content/browser/payments/payment_app_info_fetcher.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/content/browser/payments/payment_manager.cc
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/ios/chrome/browser/payments/ios_payment_instrument.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/ios/chrome/browser/payments/ios_payment_instrument.mm
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/ios/chrome/browser/payments/payment_request.h
[modify] https://crrev.com/fb75c3db2b7f03d0f11b5fd9500b777566b872e0/ios/chrome/browser/payments/payment_request.mm


### ro...@chromium.org (2019-08-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-30)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-09-05)

Congrats! The Panel decided to reward $10,000 for this report! 

### na...@google.com (2019-09-05)

[Empty comment from Monorail migration]

### ka...@google.com (2019-09-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2020-01-07)

rouslan@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### is...@google.com (2020-01-07)

This issue was migrated from crbug.com/chromium/998679?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096130)*
