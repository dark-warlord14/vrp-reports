# Security: heap-buffer-overflow while opening pdf and search box

| Field | Value |
|-------|-------|
| **Issue ID** | [333414305](https://issues.chromium.org/issues/333414305) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Chrome Version** | 123.0.6312.105 |
| **Reporter** | kd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2024-04-09 |
| **Bounty** | $7,000.00 |

## Description

# Steps to reproduce the problem

1. /chrome --enable-logging --v=1 ./poc.pdf
2. Press Ctrl+F to open the search box and enter any string (e.g., heap-buffer-overflow)

# Problem Description

Sorry for not providing a symbolized stack and minimized case for now. I'm working on building Chrome from scratch, but it takes time.
I'll try to come back with a more minimized test case if possible, after I am done with the chrome-symbolized build.

## affected version

I verify it on the official latest stable/dev build (123.0.6312.105/125.0.6396.3)

## Stack trace

just some non-symbolized address (from the latest stable build); I put it in the attachment. you may want to run it on your side if you have a symbolize=2 build.

## Additional

In most of the trails (>10 trails) ASan report the bug, but only once I observe that a hard CHECK in pdfium\_range.cc, line 144 failed.

# Summary

Security: heap-buffer-overflow while opening pdf and search box

# Custom Questions

#### Type of crash:

tab

#### Crash state:

I'll attach the symbolized crash as soon as I finish the debug build.

#### Reporter credit:

Han Zheng (HexHive)

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [another-check-failure.txt](attachments/another-check-failure.txt) (text/plain, 10.9 KB)
- [non-symbolized-asan.txt](attachments/non-symbolized-asan.txt) (text/plain, 9.3 KB)
- [mini.pdf](attachments/mini.pdf) (application/pdf, 255.0 KB)
- [byte_str.bin](attachments/byte_str.bin) (application/octet-stream, 9.5 KB)
- [str.bin](attachments/str.bin) (application/octet-stream, 9.5 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-04-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6560061611507712.

### cl...@appspot.gserviceaccount.com (2024-04-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6236002554150912.

### an...@chromium.org (2024-04-10)

Don't seem to be having much luck with clusterfuzz reproducing this problem (tried both job combinations listed in clusterfuzz instructions).
I was able to reproduce locally with an M123 stable asan build and symbolize the stack trace somewhat.

```
==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x522000080e2c at pc 0x55d6160ccaa4 bp 0x7ffccb0ee370 sp 0x7ffccb0edb30
WRITE of size 5504 at 0x522000080e2c thread T0 (chrome)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x55d6160ccaa3 in __asan_memcpy _asan_rtl_:3
    #1 0x55d625cd0643 in FPDFText_GetText ./../../third_party/pdfium/fpdfsdk/fpdf_text.cpp:348:3
    #2 0x55d6255d4106 in chrome_pdf::PDFiumEngine::SearchUsingICU(std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t> > const&, bool, bool, int, int) ./../../pdf/pdfium/pdfium_engine.cc:1917:7
    #3 0x55d6255d31a7 in chrome_pdf::PDFiumEngine::StartFind(std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t> > const&, bool) ./../../pdf/pdfium/pdfium_engine.cc:1809:7
    #4 0x55d63f2a7bd8 in chrome_pdf::PdfViewWebPlugin::StartFind(blink::WebString const&, bool, int) ./../../pdf/pdf_view_web_plugin.cc:710:12
    #5 0x55d63f2a7d12 in non-virtual thunk to chrome_pdf::PdfViewWebPlugin::StartFind(blink::WebString const&, bool, int) ./../../pdf/pdf_view_web_plugin.cc:0:0
    #6 0x55d634592baa in blink::FindInPage::Find(int, WTF::String const&, mojo::StructPtr<blink::mojom::blink::FindOptions>) ./../../third_party/blink/renderer/core/frame/find_in_page.cc:79:25
    #7 0x55d6237a6326 in blink::mojom::blink::FindInPageStubDispatch::Accept(blink::mojom::blink::FindInPage*, mojo::Message*) ./gen/third_party/blink/public/mojom/frame/find_in_page.mojom-blink.cc:489:13
    #8 0x55d629028f99 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1021:54
    #9 0x55d629045167 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #10 0x55d62902e085 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:706:20
    #11 0x55d629deab8e in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1181:24
    #12 0x55d629dec203 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind_internal.h:752:12
    #13 0x55d629dec203 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind_internal.h:922:12
    #14 0x55d629dec203 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1059:14
    #15 0x55d629dec203 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:972:12
    #16 0x55d627995804 in Run ./../../base/functional/callback.h:156:12
    #17 0x55d627995804 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #18 0x55d6279f49df in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #19 0x55d6279f49df in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #20 0x55d6279f39d9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:41
    #21 0x55d6279f579a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #22 0x55d627891b5c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #23 0x55d6279f64cf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #24 0x55d627929eaf in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #25 0x55d63ea9a96a in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:367:16
    #26 0x55d6250a5e38 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #27 0x55d6250a7361 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #28 0x55d6250a9d9f in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1146:10
    #29 0x55d6250a4190 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:335:36
    #30 0x55d6250a480b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:348:10
    #31 0x55d616104b18 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #32 0x7f2534629d8f in __libc_init_first ??:?

0x522000080e30 is located 0 bytes after 5424-byte region [0x52200007f900,0x522000080e30)
allocated by thread T0 (chrome) here:
    #0 0x55d61610243d in operator new(unsigned long) _asan_rtl_:3
    #1 0x55d61d6f8702 in __libcpp_operator_new<unsigned long> ./../../third_party/libc++/src/include/new:271:10
    #2 0x55d61d6f8702 in __libcpp_allocate ./../../third_party/libc++/src/include/new:295:10
    #3 0x55d61d6f8702 in allocate ./../../third_party/libc++/src/include/__memory/allocator.h:125:32
    #4 0x55d61d6f8702 in __allocate_at_least<std::__Cr::allocator<char16_t> > ./../../third_party/libc++/src/include/__memory/allocate_at_least.h:41:19
    #5 0x55d61d6f8702 in std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t> >::__shrink_or_extend(unsigned long) ./../../third_party/libc++/src/include/string:3259:27
    #6 0x55d627961eb7 in std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t> >::value_type* base::internal::WriteIntoT<std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t> > >(std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t> >*, unsigned long) ./../../base/strings/string_util_impl_helpers.h:459:8
    #7 0x55d6255ba030 in chrome_pdf::internal::PDFiumAPIStringBufferAdapter<std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t> > >::PDFiumAPIStringBufferAdapter(std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t> >*, unsigned long, bool) ./../../pdf/pdfium/pdfium_api_string_buffer_adapter.cc:22:13
    #8 0x55d6255d407d in chrome_pdf::PDFiumEngine::SearchUsingICU(std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t> > const&, bool, bool, int, int) ./../../pdf/pdfium/pdfium_engine.cc:1912:48
    #9 0x55d6255d31a7 in chrome_pdf::PDFiumEngine::StartFind(std::__Cr::basic_string<char16_t, std::__Cr::char_traits<char16_t>, std::__Cr::allocator<char16_t> > const&, bool) ./../../pdf/pdfium/pdfium_engine.cc:1809:7
    #10 0x55d63f2a7bd8 in chrome_pdf::PdfViewWebPlugin::StartFind(blink::WebString const&, bool, int) ./../../pdf/pdf_view_web_plugin.cc:710:12
    #11 0x55d63f2a7d12 in non-virtual thunk to chrome_pdf::PdfViewWebPlugin::StartFind(blink::WebString const&, bool, int) ./../../pdf/pdf_view_web_plugin.cc:0:0
    #12 0x55d634592baa in blink::FindInPage::Find(int, WTF::String const&, mojo::StructPtr<blink::mojom::blink::FindOptions>) ./../../third_party/blink/renderer/core/frame/find_in_page.cc:79:25
    #13 0x55d6237a6326 in blink::mojom::blink::FindInPageStubDispatch::Accept(blink::mojom::blink::FindInPage*, mojo::Message*) ./gen/third_party/blink/public/mojom/frame/find_in_page.mojom-blink.cc:489:13
    #14 0x55d629028f99 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1021:54
    #15 0x55d629045167 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #16 0x55d62902e085 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:706:20
    #17 0x55d629deab8e in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1181:24
    #18 0x55d629dec203 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind_internal.h:752:12
    #19 0x55d629dec203 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind_internal.h:922:12
    #20 0x55d629dec203 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1059:14
    #21 0x55d629dec203 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:972:12
    #22 0x55d627995804 in Run ./../../base/functional/callback.h:156:12
    #23 0x55d627995804 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:202:34
    #24 0x55d6279f49df in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:11)> ./../../base/task/common/task_annotator.h:89:5
    #25 0x55d6279f49df in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:473:23
    #26 0x55d6279f39d9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:338:41
    #27 0x55d6279f579a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #28 0x55d627891b5c in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #29 0x55d6279f64cf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:641:12
    #30 0x55d627929eaf in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #31 0x55d63ea9a96a in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:367:16
    #32 0x55d6250a5e38 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:676:14
    #33 0x55d6250a7361 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:780:12
    #34 0x55d6250a9d9f in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1146:10
    #35 0x55d6250a4190 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:335:36
    #36 0x55d6250a480b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:348:10
    #37 0x55d616104b18 in ChromeMain ./../../chrome/app/chrome_main.cc:192:12
    #38 0x7f2534629d8f in __libc_init_first ??:?

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/anunoy/chrome/chrome+0xe4dbaa3) (BuildId: cc24dd6b7d9ecb8f)
Shadow bytes around the buggy address:
  0x522000080b80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x522000080c00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x522000080c80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x522000080d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x522000080d80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x522000080e00: 00 00 00 00 00[04]fa fa fa fa fa fa fa fa fa fa
  0x522000080e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x522000080f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x522000080f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x522000081000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x522000081080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
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
==1==ADDITIONAL INFO

==1==Note: Please include this section with the ASan report.
Task trace:
    #0 0x55d629ddef81 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1120:13


==1==END OF ADDITIONAL INFO

```

### an...@chromium.org (2024-04-10)

@tsepez can you PTAL? Please re-route as necessary. Thanks!

### kd...@gmail.com (2024-04-11)

I build with DCHECK and  `DCHECK_LE(ret_count, static_cast<size_t>(char_count) + 1);` in `FPDFText_GetText ./../../third_party/pdfium/fpdfsdk/fpdf_text.cpp:346` failed.
and in debugging, I notice that `byte_str`, which is converted from `str.ToUTF16LE()`, is longer than str. I dump two variable's `.c_str` and somewhere decode broken

```
# str.c_str()
000008a0: 0d00 0000 0a00 0000 3ad4 0100 2000 0000  ........:... ...
000008b0: 3d00 0000 2000 0000 2800 0000 41d4 0100  =... ...(...A...

# byte_str.c_str()
00000450: 0d00 0a00 35d8 3adc 2000 3d00 2000 2800  ....5.:. .=. .(.

```

looks like the `3ad4 0100` is decoded to `35d8 3adc`, which in theory these 4B should be decoded to 2B.
I guess some similarly broken conversion increases the `byte_str` length, finally overflows the buffer.

### kd...@gmail.com (2024-04-11)

possible buggy code, I'm not familiar with chrome, it's just for reference

```
// pdfium_range.cc
  PDFiumAPIStringBufferAdapter<std::u16string> api_string_adapter(
      &page_text, text_length, false);                                   // <- allocate text_length (textpage->CountChars()) 
  unsigned short* data =
      reinterpret_cast<unsigned short*>(api_string_adapter.GetData()); 
  int written =
      FPDFText_GetText(pages_[current_page]->GetTextPage(),
                       character_to_start_searching_from, text_length, data);

// fpdf_text.cc
FPDF_EXPORT int FPDF_CALLCONV FPDFText_GetText(FPDF_TEXTPAGE page,
                                               ...
                                               unsigned short* result) {

...
  WideString str = textpage->GetPageText(start_index, char_count); 
...
  ByteString byte_str = str.ToUTF16LE();                               // byte_str_len might be longer than str.GetLength() / 2
  size_t byte_str_len = byte_str.GetLength();
...
  memcpy(result, byte_str.c_str(), byte_str_len);                      // <- assume byte_str_len is equal to page's CountChars/GetCharCount
                                                                       // <- assume don't hold when converting some special char, e,g, chr(0x0001d43a), '𝐺'


```

### pe...@google.com (2024-04-11)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### am...@chromium.org (2024-04-11)

Also cc'ing thestig@ since this is a PDFium issue and also since tsepez@ will be OOO shortly

### ts...@google.com (2024-04-11)

Likely a consequence of https://pdfium-review.googlesource.com/c/pdfium/+/114670 where proper handling of surrogate pairs may allow the string to expand. +nico

### ts...@google.com (2024-04-11)

Actually bisects to https://pdfium-review.googlesource.com/c/pdfium/+/114130 which is earlier in the same batch of CLs. 

### ts...@google.com (2024-04-11)

(So SecurityImpact stable is correct).

### th...@chromium.org (2024-04-11)

Is this a consequence of not taking action on <https://bugs.chromium.org/p/pdfium/issues/detail?id=2133> ?

### ts...@google.com (2024-04-11)

Seems very likely to be 2133.

Consequences are very bad: attacker controlled write of attacker controlled data past the end of buffer when performing a search over an attacker's document.
Where we got unlucky: faulty memcpy() guarded by DCHECK(), not check.

### ts...@chromium.org (2024-04-11)

https://pdfium-review.googlesource.com/c/pdfium/+/118292 is one approach

### ts...@chromium.org (2024-04-12)

That CL has landed, and I manually pulled the patch into a chrome/ASAN build to show that the testcase no longer has issues.

### ap...@google.com (2024-04-12)

Project: chromium/src
Branch: main

commit 45e5211e6bdec4b941c7acfa8fea14a685e93de4
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Fri Apr 12 04:02:09 2024

    Roll PDFium from 3f197528d475 to 2c66e07e9c3b (3 revisions)
    
    https://pdfium.googlesource.com/pdfium.git/+log/3f197528d475..2c66e07e9c3b
    
    2024-04-12 tsepez@chromium.org Spanify CFX_SeekableStreamProxy
    2024-04-12 tsepez@chromium.org Spanify FPDFText_GetText() and FPDF_GetBoundedText().
    2024-04-12 tsepez@chromium.org Don't allow two-arg span constructor without UNSAFE_BUFFER() annotation.
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/pdfium-autoroll
    Please CC dhoss@chromium.org,pdfium-deps-rolls@chromium.org,thestig@chromium.org on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Bug: chromium:333414305
    Tbr: pdfium-deps-rolls@chromium.org
    Change-Id: Iaca4af63fc85df97951f48edecb7b8a5d8d5c02d
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5449057
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1286291}

M       DEPS
M       third_party/pdfium

https://chromium-review.googlesource.com/5449057


### pe...@google.com (2024-04-12)

Setting milestone because of s2 severity.

### pe...@google.com (2024-04-12)

Requesting merge to beta (M124) because latest trunk commit (1286291) appears to be after beta branch point (1274542).
Merge review required: a commit with DEPS changes was detected.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [124].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### ts...@chromium.org (2024-04-12)

1. CL: https://pdfium-review.googlesource.com/c/pdfium/+/118292
2. Canary: Not yet.
3. Stability: Not likely to introduce instability.
4. Compatibility: restores an old behavior.
5. Manual verification: No.

### am...@chromium.org (2024-04-17)

<https://pdfium-review.googlesource.com/c/pdfium/+/118292> approved for merge to M124
thestig@ would you be able to perform the backmerge to branch 6367 since tsepez@ is current OOO?

### th...@chromium.org (2024-04-17)

Uploaded <https://pdfium-review.googlesource.com/c/118450> for the cherry-pick.

### pe...@google.com (2024-04-22)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### am...@google.com (2024-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-22)

Congratulations Han Zheng! The Chrome VRP Panel has decided to award you $7,000 for this report of memory corruption in a sandboxed process. While this is technically a mitigated vulnerability, and eligible for lower reward amounts consistent with mitigated issues [1], the mitigation here is mild, but more importantly in our assessment we believe the power and and attacker control with this issue outweighed was significant enough for this issue to be awarded the standard reward amount of a bug of this class.

A member of the Google finance team (p2p-vrp) will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- nice work!

### pe...@google.com (2024-07-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### kd...@gmail.com (2024-07-22)

Hi, Thanks for the reward!
Will there be CVE assigned for this vulnerability?

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/333414305)*
