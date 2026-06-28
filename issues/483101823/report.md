# Mojo’s ChannelPosix incorrectly handles >128 file descriptors in a message, leading to fd confusion

| Field | Value |
|-------|-------|
| **Issue ID** | [483101823](https://issues.chromium.org/issues/483101823) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo |
| **Platforms** | Android, Linux, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ff...@google.com |
| **Created** | 2026-02-09 |
| **Bounty** | $30,000.00 |

## Description

---

### Report description

AddressSanitizer: BUS on unknown address

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

1. Running a local web server using python with attached attached `python3 -m http.server 9090`
2. Open chrome to open attached html:

```
user@user:~/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan$ ./chrome --no-sandbox --user-data-dir=/mnt/scratch0/tmp/user_profile_0 --ignore-gpu-blacklist --allow-file-access-from-files --disable-gesture-requirement-for-media-playback --disable-click-to-play --disable-hang-monitor --dns-prefetch-disable --disable-default-apps --disable-component-update --safebrowsing-disable-auto-update --metrics-recording-only --disable-gpu-watchdog --disable-metrics --disable-popup-blocking --disable-prompt-on-repost --enable-experimental-extension-apis --enable-extension-apps --js-flags="--expose-gc --verify-heap" --new-window --no-default-browser-check --no-first-run --no-process-singleton-dialog --enable-shadow-dom --enable-media-stream --use-gl=angle --use-angle=swiftshader --use-cmd-decoder=passthrough --use-fake-device-for-media-stream --use-fake-ui-for-media-stream --disable-in-process-stack-traces --enable-logging=stderr --v=1 --disable-field-trial-config --enable-benchmarking http://localhost:9090/html/1.html

```

3. Wait for 15-60 seconds.

```
AddressSanitizer:DEADLYSIGNAL
=================================================================
==917774==ERROR: AddressSanitizer: BUS on unknown address (pc 0x74ad4b1a15d2 bp 0x7ffe357e7270 sp 0x7ffe357e6a28 T0)
==917774==The signal is caused by a READ memory access.
==917774==Hint: this fault was caused by a dereference of a high value address (see register values below).  Disassemble the provided pc to learn which register was used.
==917774==WARNING: invalid path to external symbolizer!
==917774==WARNING: Failed to use and restart external symbolizer!
    #0 0x74ad4b1a15d2  (/lib/x86_64-linux-gnu/libc.so.6+0x1a15d2) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb)
    #1 0x578e4de77192  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x11401192) (BuildId: 1c3a76e6158d7c46)
    #2 0x578e4de75873  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x113ff873) (BuildId: 1c3a76e6158d7c46)
    #3 0x578e73d16d6c  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x372a0d6c) (BuildId: 1c3a76e6158d7c46)
    #4 0x578e73d17e44  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x372a1e44) (BuildId: 1c3a76e6158d7c46)
    #5 0x578e73d14682  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x3729e682) (BuildId: 1c3a76e6158d7c46)
    #6 0x578e5cb45da8  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x200cfda8) (BuildId: 1c3a76e6158d7c46)
    #7 0x578e647fcf69  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x27d86f69) (BuildId: 1c3a76e6158d7c46)
    #8 0x578e6481aca3  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x27da4ca3) (BuildId: 1c3a76e6158d7c46)
    #9 0x578e64803413  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x27d8d413) (BuildId: 1c3a76e6158d7c46)
    #10 0x578e686bcf0d  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x2bc46f0d) (BuildId: 1c3a76e6158d7c46)
    #11 0x578e686bf381  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x2bc49381) (BuildId: 1c3a76e6158d7c46)
    #12 0x578e64a3c4a6  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x27fc64a6) (BuildId: 1c3a76e6158d7c46)
    #13 0x578e64ab3a97  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x2803da97) (BuildId: 1c3a76e6158d7c46)
    #14 0x578e64ab296a  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x2803c96a) (BuildId: 1c3a76e6158d7c46)
    #15 0x578e648fcf69  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x27e86f69) (BuildId: 1c3a76e6158d7c46)
    #16 0x578e64ab5187  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x2803f187) (BuildId: 1c3a76e6158d7c46)
    #17 0x578e649b77a0  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x27f417a0) (BuildId: 1c3a76e6158d7c46)
    #18 0x578e70cab8b3  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x342358b3) (BuildId: 1c3a76e6158d7c46)
    #19 0x578e607a916c  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x23d3316c) (BuildId: 1c3a76e6158d7c46)
    #20 0x578e607aa470  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x23d34470) (BuildId: 1c3a76e6158d7c46)
    #21 0x578e607ad002  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x23d37002) (BuildId: 1c3a76e6158d7c46)
    #22 0x578e607a6c41  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x23d30c41) (BuildId: 1c3a76e6158d7c46)
    #23 0x578e607a723c  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x23d3123c) (BuildId: 1c3a76e6158d7c46)
    #24 0x578e4d6e8279  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x10c72279) (BuildId: 1c3a76e6158d7c46)
    #25 0x74ad4b02a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb)
    #26 0x74ad4b02a28a  (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb)
    #27 0x578e4d60b029  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x10b95029) (BuildId: 1c3a76e6158d7c46)

==917774==Register values:
rax = 0x00006f6c06404000  rbx = 0x00006f6c06404000  rcx = 0x00006f6c06593eff  rdx = 0x0000000000190000  
rdi = 0x00006f6c06404000  rsi = 0x00006f5ea5d96000  rbp = 0x00007ffe357e7270  rsp = 0x00007ffe357e6a28  
 r8 = 0x0000000000000000   r9 = 0x0000000000006400  r10 = 0x0000000000006400  r11 = 0x0000000000c00000  
r12 = 0x00006f5ea5d96000  r13 = 0x000000000018ffbf  r14 = 0x0000000000190000  r15 = 0x00006f5ea5d96000  
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: BUS (/lib/x86_64-linux-gnu/libc.so.6+0x1a15d2) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb) 

==917774==ADDITIONAL INFO

==917774==Note: Please include this section with the ASan report.
Task trace:
    #0 0x578e686b650b  (/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/chrome+0x2bc4050b) (BuildId: 1c3a76e6158d7c46)


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=917713 --enable-crash-reporter=, --user-data-dir=/home/muriarfad/.config/chromium --enable-experimental-extension-apis --enable-benchmarking --change-stack-guard-on-fork=enable --disable-in-process-stack-traces --no-sandbox --file-url-path-alias=/gen=/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/gen --use-cmd-decoder=passthrough --use-fake-ui-for-media-stream --js-flags=--expose-gc --verify-heap --ozone-platform=x11 --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1770573320846424 --launch-time-ticks=94108848166 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,2103499682532682377,7619645105908947191,2097152 --field-trial-handle=3,i,17759248466882523900,8015743303382578462,262144 --variations-seed-version --pseudonymization-salt-handle=7,i,12083662951007387805,11377774367606478024,4 --trace-process-track-uuid=3190708990997080739 --enable-logging=stderr --v=1`


==917774==END OF ADDITIONAL INFO

==917774==ABORTING

```

4. Some past symbolized errors:

```
muriarfad@hackerenesia:~/chromium/src$ cat ~/Documents/log.log | python3 ./tools/valgrind/asan/asan_symbolize.py 
=================================================================
==907546==ERROR: AddressSanitizer: BUS on unknown address (pc 0x7dfb1c7a15d2 bp 0x7ffcd4f31ff0 sp 0x7ffcd4f317a8 T0)
==907546==The signal is caused by a READ memory access.
==907546==Hint: this fault was caused by a dereference of a high value address (see register values below).  Disassemble the provided pc to learn which register was used.
==907546==WARNING: invalid path to external symbolizer!
==907546==WARNING: Failed to use and restart external symbolizer!
    #0 0x7dfb1c7a15d2 in __memcpy_avx512_unaligned_erms ./string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:523:0
    #1 0x6001e58d3192 in std::__Cr::pair<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>> std::__Cr::__copy_move_unwrap_iters<std::__Cr::__copy_backward_impl<std::__Cr::_RangeAlgPolicy>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>, 0>(base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>) ./gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227:5
    #2 0x6001e58d1873 in base::span<unsigned char, 18446744073709551615ul, unsigned char*>::copy_from(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) requires !std::is_const_v<T> ./gen/third_party/libc++/src/include/__algorithm/copy_backward.h:237:10
    #3 0x60020b772d6c in mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Read(blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:178:36
    #4 0x60020b773e44 in mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, false>>::DeserializeElements(mojo::internal::Array_Data<mojo::internal::Pointer<blink::mojom::internal::SerializedArrayBufferContents_Data>>*, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>*, mojo::Message*) ./gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86:12
    #5 0x60020b770682 in mojo::StructTraits<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Read(blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:107:13
    #6 0x6001f45a1da8 in blink::mojom::blink::LocalFrameStubDispatch::Accept(blink::mojom::blink::LocalFrame*, mojo::Message*) ./gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208:12
    #7 0x6001fc258f69 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #8 0x6001fc276ca3 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #9 0x6001fc25f413 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #10 0x600200118f0d in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #11 0x60020011b381 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #12 0x6001fc4984a6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #13 0x6001fc50fa97 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #14 0x6001fc50e96a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #15 0x6001fc358f69 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #16 0x6001fc511187 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #17 0x6001fc4137a0 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #18 0x6002087078b3 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:369:16
    #19 0x6001f820516c in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:664:14
    #20 0x6001f8206470 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:771:12
    #21 0x6001f8209002 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1147:10
    #22 0x6001f8202c41 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #23 0x6001f820323c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #24 0x6001e5144279 in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #25 0x7dfb1c62a1c9 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #26 0x7dfb1c62a28a in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #27 0x6001e5067029 in _start ??:0:0

==907546==Register values:
rax = 0x000078b809c04000  rbx = 0x000078b809c04000  rcx = 0x000078b809d93eff  rdx = 0x0000000000190000
rdi = 0x000078b809c04000  rsi = 0x000078ac74c80000  rbp = 0x00007ffcd4f31ff0  rsp = 0x00007ffcd4f317a8
 r8 = 0x0000000000000000   r9 = 0x0000000000006400  r10 = 0x0000000000006400  r11 = 0x0000000000c00000
r12 = 0x000078ac74c80000  r13 = 0x000000000018ffbf  r14 = 0x0000000000190000  r15 = 0x000078ac74c80000
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: BUS (/lib/x86_64-linux-gnu/libc.so.6+0x1a15d2) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb)

==907546==ADDITIONAL INFO

==907546==Note: Please include this section with the ASan report.
Task trace:
    #0 0x60020011250b in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1138:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=907485 --enable-crash-reporter=, --user-data-dir=/home/muriarfad/.config/chromium --enable-experimental-extension-apis --enable-benchmarking --change-stack-guard-on-fork=enable --disable-in-process-stack-traces --no-sandbox --file-url-path-alias=/gen=/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/gen --use-cmd-decoder=passthrough --use-fake-ui-for-media-stream --js-flags=--expose-gc --verify-heap --ozone-platform=x11 --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1770573320846423 --launch-time-ticks=93250081671 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,4516236704961484586,13320352640259864875,2097152 --field-trial-handle=3,i,12847715532706039423,16562453594004678723,262144 --variations-seed-version --pseudonymization-salt-handle=7,i,14405156660913596890,2842122626057366863,4 --trace-process-track-uuid=3190708990997080739 --enable-logging=stderr --v=1`


==907546==END OF ADDITIONAL INFO

==907546==ABORTING
muriarfad@hackerenesia:~/chromium/src$ cat ~/Documents/log.log | python3 ./tools/valgrind/asan/asan_symbolize.py 
AddressSanitizer:DEADLYSIGNAL
=================================================================
==913218==ERROR: AddressSanitizer: BUS on unknown address (pc 0x733e7a3a15d2 bp 0x7ffd25289170 sp 0x7ffd25288928 T0)
==913218==The signal is caused by a READ memory access.
==913218==Hint: this fault was caused by a dereference of a high value address (see register values below).  Disassemble the provided pc to learn which register was used.
==913218==WARNING: invalid path to external symbolizer!
==913218==WARNING: Failed to use and restart external symbolizer!
    #0 0x733e7a3a15d2 in __memcpy_avx512_unaligned_erms ./string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:523:0
    #1 0x5cfcb88ca192 in std::__Cr::pair<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>> std::__Cr::__copy_move_unwrap_iters<std::__Cr::__copy_backward_impl<std::__Cr::_RangeAlgPolicy>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>, 0>(base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>) ./gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227:5
    #2 0x5cfcb88c8873 in base::span<unsigned char, 18446744073709551615ul, unsigned char*>::copy_from(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) requires !std::is_const_v<T> ./gen/third_party/libc++/src/include/__algorithm/copy_backward.h:237:10
    #3 0x5cfcde769d6c in mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Read(blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:178:36
    #4 0x5cfcde76ae44 in mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, false>>::DeserializeElements(mojo::internal::Array_Data<mojo::internal::Pointer<blink::mojom::internal::SerializedArrayBufferContents_Data>>*, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>*, mojo::Message*) ./gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86:12
    #5 0x5cfcde767682 in mojo::StructTraits<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Read(blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:107:13
    #6 0x5cfcc7598da8 in blink::mojom::blink::LocalFrameStubDispatch::Accept(blink::mojom::blink::LocalFrame*, mojo::Message*) ./gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208:12
    #7 0x5cfccf24ff69 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #8 0x5cfccf26dca3 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #9 0x5cfccf256413 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #10 0x5cfcd310ff0d in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #11 0x5cfcd3112381 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #12 0x5cfccf48f4a6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #13 0x5cfccf506a97 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #14 0x5cfccf50596a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #15 0x5cfccf34ff69 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #16 0x5cfccf508187 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #17 0x5cfccf40a7a0 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #18 0x5cfcdb6fe8b3 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:369:16
    #19 0x5cfccb1fc16c in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:664:14
    #20 0x5cfccb1fd470 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:771:12
    #21 0x5cfccb200002 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1147:10
    #22 0x5cfccb1f9c41 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #23 0x5cfccb1fa23c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #24 0x5cfcb813b279 in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #25 0x733e7a22a1c9 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #26 0x733e7a22a28a in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #27 0x5cfcb805e029 in _start ??:0:0

==913218==Register values:
rax = 0x00006e0006604000  rbx = 0x00006e0006604000  rcx = 0x00006e0006793eff  rdx = 0x0000000000190000
rdi = 0x00006e0006604000  rsi = 0x00006df3c654a000  rbp = 0x00007ffd25289170  rsp = 0x00007ffd25288928
 r8 = 0x0000000000000000   r9 = 0x0000000000006400  r10 = 0x0000000000006400  r11 = 0x0000000000c00000
r12 = 0x00006df3c654a000  r13 = 0x000000000018ffbf  r14 = 0x0000000000190000  r15 = 0x00006df3c654a000
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: BUS (/lib/x86_64-linux-gnu/libc.so.6+0x1a15d2) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb)

==913218==ADDITIONAL INFO

==913218==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5cfcd310950b in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1138:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=913150 --enable-crash-reporter=, --user-data-dir=/home/muriarfad/.config/chromium --enable-experimental-extension-apis --enable-benchmarking --change-stack-guard-on-fork=enable --disable-in-process-stack-traces --no-sandbox --file-url-path-alias=/gen=/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/gen --use-cmd-decoder=passthrough --use-fake-ui-for-media-stream --js-flags=--expose-gc --verify-heap --ozone-platform=x11 --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1770573320846423 --launch-time-ticks=93736367221 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,3228206022457344240,13020516879037013189,2097152 --field-trial-handle=3,i,2339203777569848650,18283472546708328929,262144 --variations-seed-version --pseudonymization-salt-handle=7,i,15440548128994902973,3876358496120658501,4 --trace-process-track-uuid=3190708990997080739 --enable-logging=stderr --v=1`


==913218==END OF ADDITIONAL INFO

==913218==ABORTING
AddressSanitizer: CHECK failed: sanitizer_linux_libcdep.cpp:184 "((pthread_getattr_np(pthread_self(), &attr))) == ((0))" (0x18, 0x0) (tid=913218)
    #0 0x5cfcb810af71 in __asan::CheckUnwind() _asan_rtl_:0
    #1 0x5cfcb811f662 in __sanitizer::CheckFailed(char const*, int, char const*, unsigned long long, unsigned long long) sanitizer_termination.cpp:0:0
    #2 0x5cfcb812014b in __sanitizer::GetThreadStackTopAndBottom(bool, unsigned long*, unsigned long*) sanitizer_linux_libcdep.cpp:0:0
    #3 0x5cfcb81203df in __sanitizer::GetThreadStackAndTls(bool, unsigned long*, unsigned long*, unsigned long*, unsigned long*) sanitizer_linux_libcdep.cpp:0:0
    #4 0x5cfcb8105763 in __asan::PlatformUnpoisonStacks() _asan_rtl_:0
    #5 0x5cfcb810aadc in __asan_handle_no_return ??:0:0
    #6 0x5cfccf2f2d5e in base::debug::AsanService::Abort() _asan_rtl_:3
    #7 0x5cfccf2f3349 in base::debug::AsanService::RunErrorCallbacks(char const*) _asan_rtl_:5
    #8 0x5cfcb81067de in __asan::ScopedInErrorReport::~ScopedInErrorReport() _asan_rtl_:0
    #9 0x5cfcb8106083 in __asan::ReportDeadlySignal(__sanitizer::SignalContext const&) _asan_rtl_:0
    #10 0x5cfcb81056d7 in __asan::AsanOnDeadlySignal(int, void*, void*) _asan_rtl_:0
    #11 0x733e7a24532f in __GI___sigaction :?
    #12 0x733e7a3a15d1 in __memcpy_avx512_unaligned_erms ./string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:522:0
    #13 0x5cfcb80fe3e7 in __asan_memmove ??:0:0
    #14 0x5cfcb88ca192 in std::__Cr::pair<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>> std::__Cr::__copy_move_unwrap_iters<std::__Cr::__copy_backward_impl<std::__Cr::_RangeAlgPolicy>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>, 0>(base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>) ./gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227:5
    #15 0x5cfcb88c8873 in base::span<unsigned char, 18446744073709551615ul, unsigned char*>::copy_from(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) requires !std::is_const_v<T> ./gen/third_party/libc++/src/include/__algorithm/copy_backward.h:237:10
    #16 0x5cfcde769d6c in mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Read(blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:178:36
    #17 0x5cfcde76ae44 in mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, false>>::DeserializeElements(mojo::internal::Array_Data<mojo::internal::Pointer<blink::mojom::internal::SerializedArrayBufferContents_Data>>*, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>*, mojo::Message*) ./gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86:12
    #18 0x5cfcde767682 in mojo::StructTraits<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Read(blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:107:13
    #19 0x5cfcc7598da8 in blink::mojom::blink::LocalFrameStubDispatch::Accept(blink::mojom::blink::LocalFrame*, mojo::Message*) ./gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208:12
    #20 0x5cfccf24ff69 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #21 0x5cfccf26dca3 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #22 0x5cfccf256413 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #23 0x5cfcd310ff0d in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #24 0x5cfcd3112381 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #25 0x5cfccf48f4a6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #26 0x5cfccf506a97 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #27 0x5cfccf50596a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #28 0x5cfccf34ff69 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #29 0x5cfccf508187 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #30 0x5cfccf40a7a0 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #31 0x5cfcdb6fe8b3 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:369:16
    #32 0x5cfccb1fc16c in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:664:14
    #33 0x5cfccb1fd470 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:771:12
    #34 0x5cfccb200002 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1147:10
    #35 0x5cfccb1f9c41 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #36 0x5cfccb1fa23c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #37 0x5cfcb813b279 in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #38 0x733e7a22a1c9 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #39 0x733e7a22a28a in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #40 0x5cfcb805e029 in _start ??:0:0
muriarfad@hackerenesia:~/chromium/src$ cat ~/Documents/log.log | python3 ./tools/valgrind/asan/asan_symbolize.py 
AddressSanitizer:DEADLYSIGNAL
=================================================================
==916761==ERROR: AddressSanitizer: BUS on unknown address (pc 0x70a45d9a15d2 bp 0x7ffdd9701090 sp 0x7ffdd9700848 T0)
==916761==The signal is caused by a READ memory access.
==916761==Hint: this fault was caused by a dereference of a high value address (see register values below).  Disassemble the provided pc to learn which register was used.
==916761==WARNING: invalid path to external symbolizer!
==916761==WARNING: Failed to use and restart external symbolizer!
    #0 0x70a45d9a15d2 in __memcpy_avx512_unaligned_erms ./string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:523:0
    #1 0x5e69e235a192 in std::__Cr::pair<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>> std::__Cr::__copy_move_unwrap_iters<std::__Cr::__copy_backward_impl<std::__Cr::_RangeAlgPolicy>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>, 0>(base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>) ./gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227:5
    #2 0x5e69e2358873 in base::span<unsigned char, 18446744073709551615ul, unsigned char*>::copy_from(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) requires !std::is_const_v<T> ./gen/third_party/libc++/src/include/__algorithm/copy_backward.h:237:10
    #3 0x5e6a081f9d6c in mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Read(blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:178:36
    #4 0x5e6a081fae44 in mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, false>>::DeserializeElements(mojo::internal::Array_Data<mojo::internal::Pointer<blink::mojom::internal::SerializedArrayBufferContents_Data>>*, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>*, mojo::Message*) ./gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86:12
    #5 0x5e6a081f7682 in mojo::StructTraits<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Read(blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:107:13
    #6 0x5e69f1028da8 in blink::mojom::blink::LocalFrameStubDispatch::Accept(blink::mojom::blink::LocalFrame*, mojo::Message*) ./gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208:12
    #7 0x5e69f8cdff69 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #8 0x5e69f8cfdca3 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #9 0x5e69f8ce6413 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #10 0x5e69fcb9ff0d in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #11 0x5e69fcba2381 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #12 0x5e69f8f1f4a6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #13 0x5e69f8f96a97 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #14 0x5e69f8f9596a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #15 0x5e69f8ddff69 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #16 0x5e69f8f98187 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #17 0x5e69f8e9a7a0 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #18 0x5e6a0518e8b3 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:369:16
    #19 0x5e69f4c8c16c in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:664:14
    #20 0x5e69f4c8d470 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:771:12
    #21 0x5e69f4c90002 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1147:10
    #22 0x5e69f4c89c41 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #23 0x5e69f4c8a23c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #24 0x5e69e1bcb279 in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #25 0x70a45d82a1c9 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #26 0x70a45d82a28a in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #27 0x5e69e1aee029 in _start ??:0:0

==916761==Register values:
rax = 0x00006b6406204000  rbx = 0x00006b6406204000  rcx = 0x00006b6406393eff  rdx = 0x0000000000190000
rdi = 0x00006b6406204000  rsi = 0x00006b59b87fa000  rbp = 0x00007ffdd9701090  rsp = 0x00007ffdd9700848
 r8 = 0x0000000000000000   r9 = 0x0000000000006400  r10 = 0x0000000000006400  r11 = 0x0000000000c00000
r12 = 0x00006b59b87fa000  r13 = 0x000000000018ffbf  r14 = 0x0000000000190000  r15 = 0x00006b59b87fa000
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: BUS (/lib/x86_64-linux-gnu/libc.so.6+0x1a15d2) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb)

==916761==ADDITIONAL INFO

==916761==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5e69fcb9950b in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1138:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=916692 --enable-crash-reporter=, --user-data-dir=/home/muriarfad/.config/chromium --enable-experimental-extension-apis --enable-benchmarking --change-stack-guard-on-fork=enable --disable-in-process-stack-traces --no-sandbox --file-url-path-alias=/gen=/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/gen --use-cmd-decoder=passthrough --use-fake-ui-for-media-stream --js-flags=--expose-gc --verify-heap --ozone-platform=x11 --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1770573320846424 --launch-time-ticks=94028227199 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,716098165892424561,2927052676965616427,2097152 --field-trial-handle=3,i,9732730137437471690,9817359595895367838,262144 --variations-seed-version --pseudonymization-salt-handle=7,i,18318080019641890604,3305019043374413672,4 --trace-process-track-uuid=3190708990997080739 --enable-logging=stderr --v=1`


==916761==END OF ADDITIONAL INFO

==916761==ABORTING
muriarfad@hackerenesia:~/chromium/src$ cat ~/Documents/log.log | python3 ./tools/valgrind/asan/asan_symbolize.py 
AddressSanitizer:DEADLYSIGNAL
=================================================================
==917774==ERROR: AddressSanitizer: BUS on unknown address (pc 0x74ad4b1a15d2 bp 0x7ffe357e7270 sp 0x7ffe357e6a28 T0)
==917774==The signal is caused by a READ memory access.
==917774==Hint: this fault was caused by a dereference of a high value address (see register values below).  Disassemble the provided pc to learn which register was used.
==917774==WARNING: invalid path to external symbolizer!
==917774==WARNING: Failed to use and restart external symbolizer!
    #0 0x74ad4b1a15d2 in __memcpy_avx512_unaligned_erms ./string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:523:0
    #1 0x578e4de77192 in std::__Cr::pair<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>> std::__Cr::__copy_move_unwrap_iters<std::__Cr::__copy_backward_impl<std::__Cr::_RangeAlgPolicy>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>, 0>(base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>) ./gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227:5
    #2 0x578e4de75873 in base::span<unsigned char, 18446744073709551615ul, unsigned char*>::copy_from(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) requires !std::is_const_v<T> ./gen/third_party/libc++/src/include/__algorithm/copy_backward.h:237:10
    #3 0x578e73d16d6c in mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Read(blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:178:36
    #4 0x578e73d17e44 in mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, false>>::DeserializeElements(mojo::internal::Array_Data<mojo::internal::Pointer<blink::mojom::internal::SerializedArrayBufferContents_Data>>*, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>*, mojo::Message*) ./gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86:12
    #5 0x578e73d14682 in mojo::StructTraits<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Read(blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:107:13
    #6 0x578e5cb45da8 in blink::mojom::blink::LocalFrameStubDispatch::Accept(blink::mojom::blink::LocalFrame*, mojo::Message*) ./gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208:12
    #7 0x578e647fcf69 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #8 0x578e6481aca3 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #9 0x578e64803413 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #10 0x578e686bcf0d in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #11 0x578e686bf381 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #12 0x578e64a3c4a6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #13 0x578e64ab3a97 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #14 0x578e64ab296a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #15 0x578e648fcf69 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #16 0x578e64ab5187 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #17 0x578e649b77a0 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #18 0x578e70cab8b3 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:369:16
    #19 0x578e607a916c in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:664:14
    #20 0x578e607aa470 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:771:12
    #21 0x578e607ad002 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1147:10
    #22 0x578e607a6c41 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #23 0x578e607a723c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #24 0x578e4d6e8279 in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #25 0x74ad4b02a1c9 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #26 0x74ad4b02a28a in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #27 0x578e4d60b029 in _start ??:0:0

==917774==Register values:
rax = 0x00006f6c06404000  rbx = 0x00006f6c06404000  rcx = 0x00006f6c06593eff  rdx = 0x0000000000190000
rdi = 0x00006f6c06404000  rsi = 0x00006f5ea5d96000  rbp = 0x00007ffe357e7270  rsp = 0x00007ffe357e6a28
 r8 = 0x0000000000000000   r9 = 0x0000000000006400  r10 = 0x0000000000006400  r11 = 0x0000000000c00000
r12 = 0x00006f5ea5d96000  r13 = 0x000000000018ffbf  r14 = 0x0000000000190000  r15 = 0x00006f5ea5d96000
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: BUS (/lib/x86_64-linux-gnu/libc.so.6+0x1a15d2) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb)

==917774==ADDITIONAL INFO

==917774==Note: Please include this section with the ASan report.
Task trace:
    #0 0x578e686b650b in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1138:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=917713 --enable-crash-reporter=, --user-data-dir=/home/muriarfad/.config/chromium --enable-experimental-extension-apis --enable-benchmarking --change-stack-guard-on-fork=enable --disable-in-process-stack-traces --no-sandbox --file-url-path-alias=/gen=/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/gen --use-cmd-decoder=passthrough --use-fake-ui-for-media-stream --js-flags=--expose-gc --verify-heap --ozone-platform=x11 --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1770573320846424 --launch-time-ticks=94108848166 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,2103499682532682377,7619645105908947191,2097152 --field-trial-handle=3,i,17759248466882523900,8015743303382578462,262144 --variations-seed-version --pseudonymization-salt-handle=7,i,12083662951007387805,11377774367606478024,4 --trace-process-track-uuid=3190708990997080739 --enable-logging=stderr --v=1`


==917774==END OF ADDITIONAL INFO

==917774==ABORTING

```
#### Impact analysis

OOB read.

---

### The cause

#### What version of Chrome have you found the security issue in?

146.0.7670.2

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

muriarfad

## Attachments

- [2026-02-10 03-03-37.mp4](attachments/2026-02-10 03-03-37.mp4) (video/mp4, 41.0 MB)
- [1.html](attachments/1.html) (text/html, 1.1 KB)
- [2026-02-10 03-37-10.mp4](attachments/2026-02-10 03-37-10.mp4) (video/mp4, 31.0 MB)
- 2026-02-10 06-24-21.mp4 (video/mp4, 38.5 MB)
- [Screenshot from 2026-02-10 06-35-22.png](attachments/Screenshot from 2026-02-10 06-35-22.png) (image/png, 175.9 KB)
- [2026-02-10 07-08-16.mp4](attachments/2026-02-10 07-08-16.mp4) (video/mp4, 56.7 MB)
- [2026-02-10 07-16-06.mp4](attachments/2026-02-10 07-16-06.mp4) (video/mp4, 80.5 MB)
- [Screenshot from 2026-02-10 14-46-48.png](attachments/Screenshot from 2026-02-10 14-46-48.png) (image/png, 239.7 KB)
- [Screenshot_20260217_165857_Chrome.png](attachments/Screenshot_20260217_165857_Chrome.png) (image/png, 88.3 KB)
- [2.html](attachments/2.html) (text/html, 1.2 KB)
- [4.html](attachments/4.html) (text/html, 1.9 KB)
- [2026-02-25 02-51-24.mp4](attachments/2026-02-25 02-51-24.mp4) (video/mp4, 160.3 MB)
- [log.log](attachments/log.log) (text/plain, 11.9 KB)
- [gdb.txt](attachments/gdb.txt) (text/plain, 29.2 KB)

## Timeline

### mu...@gmail.com (2026-02-09)

```
user@user:~/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan$ ./chrome --no-sandbox --enable-logging=stderr --v=1 --js-flags="--print-bytecode --allow-natives-syntax" http://localhost:9090/html/1.html

```
```
muriarfad@hackerenesia:~/chromium/src$ cat ~/Documents/log.log | python3 ./tools/valgrind/asan/asan_symbolize.py 
Received signal 7 BUS_ADRERR 77d4d024efc0
    #0 0x6012922c2b66 in ___interceptor_backtrace ??:0:0
    #1 0x6012a9872768 in base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) ./../../base/debug/stack_trace_posix.cc:1048:7
    #2 0x6012a9832577 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:280:20
    #3 0x6012a9871b6f in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:483:3
    #4 0x7d1f7a245330 in __GI___sigaction :?
    #5 0x7d1f7a3a15d2 in __memcpy_avx512_unaligned_erms ./string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:522:0
    #6 0x60129231b3e8 in __asan_memmove ??:0:0
    #7 0x601292ae7193 in std::__Cr::pair<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>> std::__Cr::__copy_move_unwrap_iters<std::__Cr::__copy_backward_impl<std::__Cr::_RangeAlgPolicy>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>, 0>(base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>) ./gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227:5
    #8 0x601292ae5874 in base::span<unsigned char, 18446744073709551615ul, unsigned char*>::copy_from(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) requires !std::is_const_v<T> ./gen/third_party/libc++/src/include/__algorithm/copy_backward.h:237:10
    #9 0x6012b8986d6d in mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Read(blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:178:36
    #10 0x6012b8987e45 in mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, false>>::DeserializeElements(mojo::internal::Array_Data<mojo::internal::Pointer<blink::mojom::internal::SerializedArrayBufferContents_Data>>*, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>*, mojo::Message*) ./gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86:12
    #11 0x6012b8984683 in mojo::StructTraits<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Read(blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:107:13
    #12 0x6012a17b5da9 in blink::mojom::blink::LocalFrameStubDispatch::Accept(blink::mojom::blink::LocalFrame*, mojo::Message*) ./gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208:12
    #13 0x6012a946cf6a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #14 0x6012a948aca4 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #15 0x6012a9473414 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #16 0x6012ad32cf0e in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #17 0x6012ad32f382 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #18 0x6012a96ac4a7 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #19 0x6012a9723a98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #20 0x6012a972296b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #21 0x6012a956cf6a in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #22 0x6012a9725188 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #23 0x6012a96277a1 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #24 0x6012b591b8b4 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:369:16
    #25 0x6012a541916d in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:664:14
    #26 0x6012a541a471 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:771:12
    #27 0x6012a541d003 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1147:10
    #28 0x6012a5416c42 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #29 0x6012a541723d in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #30 0x60129235827a in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #31 0x7d1f7a22a1ca in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #32 0x7d1f7a22a28b in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #33 0x60129227b02a in _start ??:0:0
  r8: 0000000000000000  r9: 0000000000006400 r10: 0000000000006400 r11: 0000000000c00000
 r12: 000077d4d00bf000 r13: 000000000018ffbf r14: 0000000000190000 r15: 000077d4d00bf000
  di: 000077e03e004000  si: 000077d4d00bf000  bp: 00007ffdff24db30  bx: 000077e03e004000
  dx: 0000000000190000  ax: 000077e03e004000  cx: 000077e03e193eff  sp: 00007ffdff24d2e8
  ip: 00007d1f7a3a15d2 efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 000077d4d024efc0
[end of stack trace]
Received signal 7 BUS_ADRERR 77d4c47acfc0
    #0 0x6012922c2b66 in ___interceptor_backtrace ??:0:0
    #1 0x6012a9872768 in base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) ./../../base/debug/stack_trace_posix.cc:1048:7
    #2 0x6012a9832577 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:280:20
    #3 0x6012a9871b6f in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:483:3
    #4 0x7d1f7a245330 in __GI___sigaction :?
    #5 0x7d1f7a3a15d2 in __memcpy_avx512_unaligned_erms ./string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:522:0
    #6 0x60129231b3e8 in __asan_memmove ??:0:0
    #7 0x601292ae7193 in std::__Cr::pair<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>> std::__Cr::__copy_move_unwrap_iters<std::__Cr::__copy_backward_impl<std::__Cr::_RangeAlgPolicy>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>, 0>(base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>) ./gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227:5
    #8 0x601292ae5874 in base::span<unsigned char, 18446744073709551615ul, unsigned char*>::copy_from(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) requires !std::is_const_v<T> ./gen/third_party/libc++/src/include/__algorithm/copy_backward.h:237:10
    #9 0x6012b8986d6d in mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Read(blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:178:36
    #10 0x6012b8987e45 in mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, false>>::DeserializeElements(mojo::internal::Array_Data<mojo::internal::Pointer<blink::mojom::internal::SerializedArrayBufferContents_Data>>*, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>*, mojo::Message*) ./gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86:12
    #11 0x6012b8984683 in mojo::StructTraits<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Read(blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:107:13
    #12 0x6012a17b5da9 in blink::mojom::blink::LocalFrameStubDispatch::Accept(blink::mojom::blink::LocalFrame*, mojo::Message*) ./gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208:12
    #13 0x6012a946cf6a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #14 0x6012a948aca4 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #15 0x6012a9473414 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #16 0x6012ad32cf0e in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #17 0x6012ad32f382 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #18 0x6012a96ac4a7 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #19 0x6012a9723a98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #20 0x6012a972296b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #21 0x6012a956cf6a in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #22 0x6012a9725188 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #23 0x6012a96277a1 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #24 0x6012b591b8b4 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:369:16
    #25 0x6012a541916d in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:664:14
    #26 0x6012a541a471 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:771:12
    #27 0x6012a541d003 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1147:10
    #28 0x6012a5416c42 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #29 0x6012a541723d in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #30 0x60129235827a in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #31 0x7d1f7a22a1ca in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #32 0x7d1f7a22a28b in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #33 0x60129227b02a in _start ??:0:0
  r8: 0000000000000000  r9: 0000000000006400 r10: 0000000000006400 r11: 0000000000c00000
 r12: 000077d4c461d000 r13: 000000000018ffbf r14: 0000000000190000 r15: 000077d4c461d000
  di: 000077e013804000  si: 000077d4c461d000  bp: 00007ffdff24db30  bx: 000077e013804000
  dx: 0000000000190000  ax: 000077e013804000  cx: 000077e013993eff  sp: 00007ffdff24d2e8
  ip: 00007d1f7a3a15d2 efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 000077d4c47acfc0
[end of stack trace]

```

### mu...@gmail.com (2026-02-09)

reduce + array with `4096`

```
AddressSanitizer:DEADLYSIGNAL
=================================================================
==981611==ERROR: AddressSanitizer: BUS on unknown address (pc 0x70c6e1fa167f bp 0x7ffe54cfaa70 sp 0x7ffe54cfa228 T0)
==981611==The signal is caused by a READ memory access.
==981611==Hint: this fault was caused by a dereference of a high value address (see register values below).  Disassemble the provided pc to learn which register was used.
==981611==WARNING: invalid path to external symbolizer!
==981611==WARNING: Failed to use and restart external symbolizer!
    #0 0x70c6e1fa167f in __memcpy_avx512_unaligned_erms ./string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:590:0
    #1 0x61e134a47590 in std::__Cr::pair<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>> std::__Cr::__copy_move_unwrap_iters<std::__Cr::__copy_impl, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>, 0>(base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>) ./gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227:5
    #2 0x61e134a46d1e in base::span<unsigned char, 18446744073709551615ul, unsigned char*>::copy_from(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) requires !std::is_const_v<T> ./gen/third_party/libc++/src/include/__algorithm/copy.h:134:10
    #3 0x61e15a8e7d6c in mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Read(blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:178:36
    #4 0x61e15a8e8e44 in mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, false>>::DeserializeElements(mojo::internal::Array_Data<mojo::internal::Pointer<blink::mojom::internal::SerializedArrayBufferContents_Data>>*, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>*, mojo::Message*) ./gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86:12
    #5 0x61e15a8e5682 in mojo::StructTraits<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Read(blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:107:13
    #6 0x61e143716da8 in blink::mojom::blink::LocalFrameStubDispatch::Accept(blink::mojom::blink::LocalFrame*, mojo::Message*) ./gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208:12
    #7 0x61e14b3cdf69 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #8 0x61e14b3ebca3 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #9 0x61e14b3d4413 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #10 0x61e14f28df0d in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #11 0x61e14f290381 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #12 0x61e14b60d4a6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #13 0x61e14b684a97 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #14 0x61e14b68396a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #15 0x61e14b4cdf69 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #16 0x61e14b686187 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #17 0x61e14b5887a0 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #18 0x61e15787c8b3 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:369:16
    #19 0x61e14737a16c in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:664:14
    #20 0x61e14737b470 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:771:12
    #21 0x61e14737e002 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1147:10
    #22 0x61e147377c41 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #23 0x61e14737823c in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #24 0x61e1342b9279 in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #25 0x70c6e1e2a1c9 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #26 0x70c6e1e2a28a in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #27 0x61e1341dc029 in _start ??:0:0

==981611==Register values:
rax = 0x00006b880cab8000  rbx = 0x00006b880cab8000  rcx = 0x000000000008c000  rdx = 0x00000000000a0000
rdi = 0x00006b880cacc000  rsi = 0x00006cc63583d000  rbp = 0x00007ffe54cfaa70  rsp = 0x00007ffe54cfa228
 r8 = 0x00006b880cab8000   r9 = 0xfffffec1d728f000  r10 = 0x0000000000002800  r11 = 0x0000000000000000
r12 = 0x00006cc635829000  r13 = 0x000000000009ffbf  r14 = 0x00000000000a0000  r15 = 0x00006cc635829000
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: BUS (/lib/x86_64-linux-gnu/libc.so.6+0x1a167f) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb)

==981611==ADDITIONAL INFO

==981611==Note: Please include this section with the ASan report.
Task trace:
    #0 0x61e14f28750b in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1138:13


Command line: `/proc/self/exe --type=renderer --crashpad-handler-pid=981545 --enable-crash-reporter=, --user-data-dir=/home/muriarfad/.config/chromium --enable-experimental-extension-apis --enable-benchmarking --change-stack-guard-on-fork=enable --disable-in-process-stack-traces --no-sandbox --file-url-path-alias=/gen=/home/muriarfad/chromium/src/tools/get_asan_chrome/chromium-146.0.7670.2-linux-asan/gen --use-cmd-decoder=passthrough --use-fake-ui-for-media-stream --js-flags=--expose-gc --verify-heap --ozone-platform=x11 --lang=en-US --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1770573320846423 --launch-time-ticks=97887777404 --shared-files=v8_context_snapshot_data:100 --metrics-shmem-handle=4,i,16534190608762054902,14758755304776447906,2097152 --field-trial-handle=3,i,183990449478635248,17065697434323621691,262144 --variations-seed-version --pseudonymization-salt-handle=7,i,14316432282514470788,15353979178190715538,4 --trace-process-track-uuid=3190708990997080739 --enable-logging=stderr --v=1`


==981611==END OF ADDITIONAL INFO

==981611==ABORTING


```

### ts...@google.com (2026-02-09)

DNR locally on Chromium 146.0.7674.0.  Reporter, please, please minimize the cmd line flags to the exact set that is required for reproduction, as this will help us determine if the result is in scope.


### mu...@gmail.com (2026-02-09)

Hi team.

I run with minimal the cmd line flags:

```
--no-sandbox --enable-logging=stderr --v=1 http://localhost:9090/1.html

```
```
muriarfad@hackerenesia:~/chromium/src$ cat ~/Documents/log.log | python3 ./tools/valgrind/asan/asan_symbolize.py 
Received signal 7 BUS_ADRERR 7815d6bda000
    #0 0x5b6949dd7b66 in ___interceptor_backtrace ??:0:0
    #1 0x5b6961387768 in base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) ./../../base/debug/stack_trace_posix.cc:1048:7
    #2 0x5b6961347577 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:280:20
    #3 0x5b6961386b6f in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:483:3
    #4 0x7d6881245330 in __GI___sigaction :?
    #5 0x7d68813a167f in __memcpy_avx512_unaligned_erms ./string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:588:0
    #6 0x5b6949e303e8 in __asan_memmove ??:0:0
    #7 0x5b694a5fc193 in std::__Cr::pair<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>> std::__Cr::__copy_move_unwrap_iters<std::__Cr::__copy_backward_impl<std::__Cr::_RangeAlgPolicy>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>, 0>(base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>) ./gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227:5
    #8 0x5b694a5fa874 in base::span<unsigned char, 18446744073709551615ul, unsigned char*>::copy_from(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) requires !std::is_const_v<T> ./gen/third_party/libc++/src/include/__algorithm/copy_backward.h:237:10
    #9 0x5b697049bd6d in mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Read(blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:178:36
    #10 0x5b697049ce45 in mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, false>>::DeserializeElements(mojo::internal::Array_Data<mojo::internal::Pointer<blink::mojom::internal::SerializedArrayBufferContents_Data>>*, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>*, mojo::Message*) ./gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86:12
    #11 0x5b6970499683 in mojo::StructTraits<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Read(blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:107:13
    #12 0x5b69592cada9 in blink::mojom::blink::LocalFrameStubDispatch::Accept(blink::mojom::blink::LocalFrame*, mojo::Message*) ./gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208:12
    #13 0x5b6960f81f6a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #14 0x5b6960f9fca4 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #15 0x5b6960f88414 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #16 0x5b6964e41f0e in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #17 0x5b6964e44382 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #18 0x5b69611c14a7 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #19 0x5b6961238a98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #20 0x5b696123796b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #21 0x5b6961081f6a in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #22 0x5b696123a188 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12
    #23 0x5b696113c7a1 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #24 0x5b696d4308b4 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:369:16
    #25 0x5b695cf2e16d in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:664:14
    #26 0x5b695cf2f471 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:771:12
    #27 0x5b695cf32003 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1147:10
    #28 0x5b695cf2bc42 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #29 0x5b695cf2c23d in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #30 0x5b6949e6d27a in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #31 0x7d688122a1ca in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #32 0x7d688122a28b in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #33 0x5b6949d9002a in _start ??:0:0
  r8: 0000782013004000  r9: 0000000a3c43e000 r10: 0000000000002800 r11: 0000000000000000
 r12: 00007815d6bc6000 r13: 000000000009ffbf r14: 00000000000a0000 r15: 00007815d6bc6000
  di: 0000782013018000  si: 00007815d6bda000  bp: 00007ffc55f7ec70  bx: 0000782013004000
  dx: 00000000000a0000  ax: 0000782013004000  cx: 000000000008c000  sp: 00007ffc55f7e428
  ip: 00007d68813a167f efl: 0000000000010212 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 00007815d6bda000
[end of stack trace]

```

### mu...@gmail.com (2026-02-09)

Here's the poc video.

I download the asan chrome at this night around 10.00pm jakarta time.

### pe...@google.com (2026-02-09)

Thank you for providing more feedback. Adding the requester to the CC list.

### mu...@gmail.com (2026-02-09)

DNR with this flag :

`./chrome --no-sandbox --disable-in-process-stack-traces --enable-logging=stderr --v=1 http://localhost:9090/1.html`

But in the logging:

```
[1112721:1112721:0210/063403.537493:VERBOSE1:extensions/renderer/dispatcher.cc:577] Num tracked contexts: 2
[1112735:1112735:0210/063406.587886:VERBOSE1:extensions/renderer/dispatcher.cc:779] Num tracked contexts: 0

```

and got black screen, it's like the renderer is not running.

### mu...@gmail.com (2026-02-10)

I would like to provide an update regarding the reproduction of this issue. I have confirmed that the crash occurs on the latest official stable build: `Version 144.0.7559.132 (Official Build) (64-bit)`.

I performed a clean installation of google-chrome-stable and tested the PoC with default configurations. The result is consistent with my previous findings: a SIGBUS (Bus Error) during memory access in the IPC layer.

A crash report has been successfully generated and uploaded via Chrome's internal crash reporter.
Crash UIUD: `3534ce83-4067-4393-8571-d0978a79be94`, Uploaded Crash ReportID: `c2cea45792b4f33e`

This confirms that the vulnerability is present in the current stable release and does not depend on specific debug flags or a non-sandboxed environment.

### mu...@gmail.com (2026-02-10)

The newest poc with `google-chrome-stable --enable-logging=stderr --v=1 http://localhost:9090`

```
Crash from Tuesday, February 10, 2026 at 7:16:17 AM
Status:	Uploaded
Uploaded Crash Report ID:	216e5515a0c10a96
Upload Time:	Tuesday, February 10, 2026 at 7:31:51 AM

```

### ts...@google.com (2026-02-10)

Hmm.  When running with --enable-logging=stdder, many pages now seem to give me
[... render_process_host_impl.cc:5994] Terminating render process for bad Mojo message: Received bad user message: repeated OnV8ContextCreated notification

### mu...@gmail.com (2026-02-11)

Hi team,

I've been testing my PoC on Windows with ASan enabled. During execution, I observed some unusual memory behavior:

Initially, memory usage peaked at 4GB, then dropped to 1-2GB.

After running the PoC for about 3 minutes then refresh the page, Chromium's memory usage spiked significantly, exceeding 10GB.

After displaying this, I encountered the error listed below:

```
==24216==ERROR: AddressSanitizer failed to allocate 0xb19000 (11636736) bytes of FakeStack (error code: 1455)
==24216==Dumping process modules:
        0x022683e50000-0x022683f27000 C:\WINDOWS\System32\OLEAUT32.dll
        0x7ff7854f0000-0x7ff78678b000 D:\asan\chromium-146.0.7680.2-win64-asan\chrome.exe
        0x7ff8356e0000-0x7ff835920000 D:\asan\chromium-146.0.7680.2-win64-asan\dbghelp.dll
        0x7ff845610000-0x7ff845645000 C:\WINDOWS\SYSTEM32\WINMM.dll
        0x7ff849650000-0x7ff84966e000 D:\asan\chromium-146.0.7680.2-win64-asan\VCRUNTIME140.dll
        0x7ff84c050000-0x7ff84c05b000 C:\WINDOWS\SYSTEM32\VERSION.dll
        0x7ff84f7f0000-0x7ff84fa57000 C:\WINDOWS\SYSTEM32\DWrite.dll
        0x7ff852770000-0x7ff85277a000 C:\WINDOWS\SYSTEM32\DPAPI.DLL
        0x7ff852b80000-0x7ff852c25000 C:\WINDOWS\System32\bcryptprimitives.dll
        0x7ff852c30000-0x7ff852d7b000 C:\WINDOWS\System32\ucrtbase.dll
        0x7ff852f80000-0x7ff8530ab000 C:\WINDOWS\System32\gdi32full.dll
        0x7ff8539e0000-0x7ff853a83000 C:\WINDOWS\System32\msvcp_win.dll
        0x7ff853a90000-0x7ff853e81000 C:\WINDOWS\System32\KERNELBASE.dll
        0x7ff853e90000-0x7ff854007000 C:\WINDOWS\System32\CRYPT32.dll
        0x7ff854010000-0x7ff854037000 C:\WINDOWS\System32\win32u.dll
        0x7ff854360000-0x7ff854391000 C:\WINDOWS\System32\IMM32.DLL
        0x7ff854b90000-0x7ff854c44000 C:\WINDOWS\System32\ADVAPI32.dll
        0x7ff854d10000-0x7ff854ed6000 C:\WINDOWS\System32\USER32.dll
        0x7ff854fe0000-0x7ff855089000 C:\WINDOWS\System32\msvcrt.dll
        0x7ff855110000-0x7ff8551b6000 C:\WINDOWS\System32\sechost.dll
        0x7ff8551c0000-0x7ff855234000 C:\WINDOWS\System32\WS2_32.dll
        0x7ff855420000-0x7ff8554e9000 C:\WINDOWS\System32\KERNEL32.DLL
        0x7ff8557b0000-0x7ff8558c8000 C:\WINDOWS\System32\RPCRT4.dll
        0x7ff855de0000-0x7ff855e0b000 C:\WINDOWS\System32\GDI32.dll
        0x7ff855e10000-0x7ff856196000 C:\WINDOWS\System32\combase.dll
        0x7ff8562a0000-0x7ff856508000 C:\WINDOWS\SYSTEM32\ntdll.dll
        0x7fff1e3d0000-0x7fff5bd2e000 D:\asan\chromium-146.0.7680.2-win64-asan\chrome.dll
        0x7fff87400000-0x7fff87e06000 D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll
        0x7fff8ff40000-0x7fff90501000 D:\asan\chromium-146.0.7680.2-win64-asan\chrome_elf.dll
AddressSanitizer: CHECK failed: sanitizer_common.cpp:61 "((0 && "unable to mmap")) != (0)" (0x0, 0x0) (tid=23200)
==4348==ERROR: AddressSanitizer failed to allocate 0x800000 (8388608) bytes of StackStore (error code: 1455)
==4348==Dumping process modules:
        0x02a508850000-0x02a508927000 C:\WINDOWS\System32\OLEAUT32.dll
        0x7ff7854f0000-0x7ff78678b000 D:\asan\chromium-146.0.7680.2-win64-asan\chrome.exe
        0x7ff805af0000-0x7ff805bcc000 C:\Windows\System32\windows.internal.shell.broker.dll
        0x7ff80a780000-0x7ff80a7ef000 C:\Windows\System32\CryptoWinRT.dll
        0x7ff80a890000-0x7ff80a8b1000 C:\Windows\System32\PCShellCommonProxyStub.dll
        0x7ff80c080000-0x7ff80c353000 C:\WINDOWS\system32\explorerframe.dll
        0x7ff820ff0000-0x7ff8210c5000 C:\WINDOWS\system32\twinapi.dll
        0x7ff8216a0000-0x7ff8217fa000 C:\Windows\System32\wpnapps.dll
        0x7ff825c80000-0x7ff825cda000 C:\WINDOWS\system32\dataexchange.dll
        0x7ff827db0000-0x7ff827dcb000 C:\WINDOWS\system32\NetworkExplorer.dll
        0x7ff82ac30000-0x7ff82aca9000 C:\WINDOWS\SYSTEM32\OLEACC.dll
        0x7ff82ad70000-0x7ff82adbf000 C:\Windows\System32\vaultcli.dll
        0x7ff82bf70000-0x7ff82c203000 C:\WINDOWS\WinSxS\amd64_microsoft.windows.common-controls_6595b64144ccf1df_6.0.26100.7824_none_3e0870b2e3345462\COMCTL32.dll
        0x7ff82c210000-0x7ff82c892000 C:\Windows\System32\Windows.Media.dll
        0x7ff82ccc0000-0x7ff82cdd5000 C:\WINDOWS\system32\PCPKsp.dll
        0x7ff82d430000-0x7ff82d4ac000 C:\Windows\System32\cryptngc.dll
        0x7ff82e340000-0x7ff82e362000 C:\WINDOWS\system32\nlansp_c.dll
        0x7ff82e740000-0x7ff82e800000 C:\WINDOWS\SYSTEM32\mscms.dll
        0x7ff82e810000-0x7ff82e9f5000 C:\Windows\System32\InputHost.dll
        0x7ff82f190000-0x7ff82f235000 C:\WINDOWS\system32\directmanipulation.dll
        0x7ff835c00000-0x7ff835c8c000 C:\WINDOWS\system32\ncryptprov.dll
        0x7ff836c70000-0x7ff836dbf000 C:\Windows\System32\Windows.UI.Immersive.dll
        0x7ff83bad0000-0x7ff83bb8c000 C:\Windows\System32\Windows.Networking.Connectivity.dll
        0x7ff83d050000-0x7ff83d1a6000 C:\Windows\System32\Windows.UI.dll
        0x7ff83d640000-0x7ff83d789000 C:\WINDOWS\SYSTEM32\textinputframework.dll
        0x7ff83dc50000-0x7ff83dc61000 C:\WINDOWS\System32\perfos.dll
        0x7ff83df70000-0x7ff83e0aa000 C:\WINDOWS\system32\Windows.Storage.Search.dll
        0x7ff83e3b0000-0x7ff83e3e2000 C:\WINDOWS\SYSTEM32\cldapi.dll
        0x7ff83e7e0000-0x7ff83e89f000 C:\Windows\System32\Windows.FileExplorer.Common.dll
        0x7ff83e8b0000-0x7ff83e979000 C:\Windows\System32\OneCoreCommonProxyStub.dll
        0x7ff83e980000-0x7ff83e9f4000 C:\Windows\System32\CapabilityAccessManagerClient.dll
        0x7ff83ece0000-0x7ff83ee59000 C:\Windows\System32\Windows.System.Launcher.dll
        0x7ff83f080000-0x7ff83f157000 C:\Windows\System32\Windows.ApplicationModel.dll
        0x7ff83f280000-0x7ff83f344000 C:\Windows\System32\Windows.StateRepositoryPS.dll
        0x7ff840070000-0x7ff84030e000 C:\WINDOWS\System32\icu.dll
        0x7ff840320000-0x7ff8403df000 C:\WINDOWS\System32\StructuredQuery.dll
        0x7ff841370000-0x7ff8413b8000 C:\WINDOWS\SYSTEM32\windows.staterepositoryclient.dll
        0x7ff842590000-0x7ff8425e6000 C:\WINDOWS\SYSTEM32\pdh.dll
        0x7ff842a30000-0x7ff842a91000 C:\Windows\System32\FWPolicyIOMgr.dll
        0x7ff842cf0000-0x7ff843340000 C:\Windows\System32\OneCoreUAPCommonProxyStub.dll
        0x7ff845610000-0x7ff845645000 C:\WINDOWS\SYSTEM32\WINMM.dll
        0x7ff8463a0000-0x7ff8463e3000 C:\WINDOWS\system32\XmlLite.dll
        0x7ff846460000-0x7ff84647a000 C:\WINDOWS\SYSTEM32\windows.staterepositorycore.dll
        0x7ff846590000-0x7ff8465aa000 C:\WINDOWS\SYSTEM32\tbs.dll
        0x7ff847430000-0x7ff847460000 C:\WINDOWS\system32\mssprxy.dll
        0x7ff8474d0000-0x7ff8474f8000 C:\WINDOWS\system32\ngcksp.dll
        0x7ff848bc0000-0x7ff848e04000 C:\Windows\System32\twinapi.appcore.dll
        0x7ff849650000-0x7ff84966e000 D:\asan\chromium-146.0.7680.2-win64-asan\VCRUNTIME140.dll
        0x7ff849dc0000-0x7ff849e20000 C:\Windows\System32\usermgrproxy.dll
        0x7ff84a530000-0x7ff84a549000 C:\WINDOWS\System32\npmproxy.dll
        0x7ff84a930000-0x7ff84a94b000 C:\WINDOWS\SYSTEM32\wkscli.dll
        0x7ff84acb0000-0x7ff84acd3000 C:\WINDOWS\SYSTEM32\dhcpcsvc.DLL
        0x7ff84b640000-0x7ff84b767000 C:\WINDOWS\SYSTEM32\WINHTTP.dll
        0x7ff84bbf0000-0x7ff84bc88000 C:\WINDOWS\System32\MMDevApi.dll
        0x7ff84bee0000-0x7ff84befe000 C:\WINDOWS\SYSTEM32\dhcpcsvc6.DLL
        0x7ff84c050000-0x7ff84c05b000 C:\WINDOWS\SYSTEM32\VERSION.dll
        0x7ff84c140000-0x7ff84c422000 C:\WINDOWS\SYSTEM32\CoreUIComponents.dll
        0x7ff84d290000-0x7ff84d2a7000 C:\WINDOWS\SYSTEM32\usermgrcli.dll
        0x7ff84d7a0000-0x7ff84d810000 C:\WINDOWS\System32\netprofm.dll
        0x7ff84e4a0000-0x7ff84e5a3000 C:\WINDOWS\SYSTEM32\PROPSYS.dll
        0x7ff84f7f0000-0x7ff84fa57000 C:\WINDOWS\SYSTEM32\DWrite.dll
        0x7ff84fc90000-0x7ff84fdb7000 C:\Windows\System32\CoreMessaging.dll
        0x7ff850540000-0x7ff85054d000 C:\WINDOWS\SYSTEM32\Secur32.dll
        0x7ff850570000-0x7ff85060e000 C:\WINDOWS\SYSTEM32\apphelp.dll
        0x7ff850620000-0x7ff85064a000 C:\WINDOWS\SYSTEM32\WTSAPI32.dll
        0x7ff8506b0000-0x7ff8506c2000 C:\WINDOWS\SYSTEM32\pfclient.dll
        0x7ff8506d0000-0x7ff85077b000 C:\WINDOWS\system32\uxtheme.dll
        0x7ff850b80000-0x7ff850bb1000 C:\WINDOWS\SYSTEM32\dwmapi.dll
        0x7ff851110000-0x7ff851154000 C:\Windows\System32\fwbase.dll
        0x7ff8511a0000-0x7ff851251000 C:\Windows\System32\FirewallAPI.dll
        0x7ff851300000-0x7ff851334000 C:\WINDOWS\SYSTEM32\IPHLPAPI.DLL
        0x7ff851340000-0x7ff85146c000 C:\WINDOWS\SYSTEM32\DNSAPI.dll
        0x7ff8514a0000-0x7ff8514ad000 C:\WINDOWS\SYSTEM32\netutils.dll
        0x7ff851880000-0x7ff8518b9000 C:\WINDOWS\system32\rsaenh.dll
        0x7ff851920000-0x7ff85193b000 C:\WINDOWS\SYSTEM32\kernel.appcore.dll
        0x7ff851a40000-0x7ff851a76000 C:\WINDOWS\system32\ntmarta.dll
        0x7ff851bc0000-0x7ff851c09000 C:\WINDOWS\SYSTEM32\SspiCli.dll
        0x7ff851e90000-0x7ff851efb000 C:\WINDOWS\system32\mswsock.dll
        0x7ff851f00000-0x7ff851f31000 C:\WINDOWS\SYSTEM32\gpapi.dll
        0x7ff851f40000-0x7ff851f6b000 C:\WINDOWS\SYSTEM32\USERENV.dll
        0x7ff852160000-0x7ff85217b000 C:\WINDOWS\System32\CRYPTSP.dll
        0x7ff852180000-0x7ff85218c000 C:\WINDOWS\SYSTEM32\CRYPTBASE.dll
        0x7ff8521d0000-0x7ff8521e3000 C:\WINDOWS\System32\MSASN1.dll
        0x7ff852330000-0x7ff85236f000 C:\Windows\System32\NTASN1.dll
        0x7ff852380000-0x7ff8523b0000 C:\Windows\System32\ncrypt.dll
        0x7ff8526e0000-0x7ff85270d000 C:\WINDOWS\System32\DEVOBJ.dll
        0x7ff852710000-0x7ff852767000 C:\WINDOWS\SYSTEM32\cfgmgr32.dll
        0x7ff852770000-0x7ff85277a000 C:\WINDOWS\SYSTEM32\DPAPI.DLL
        0x7ff852780000-0x7ff8527e3000 C:\WINDOWS\SYSTEM32\WINSTA.dll
        0x7ff8529c0000-0x7ff8529d4000 C:\WINDOWS\SYSTEM32\UMPDC.dll
        0x7ff8529e0000-0x7ff852a3e000 C:\WINDOWS\SYSTEM32\powrprof.dll
        0x7ff852a70000-0x7ff852a99000 C:\WINDOWS\SYSTEM32\profapi.dll
        0x7ff852aa0000-0x7ff852aca000 C:\Windows\System32\bcrypt.dll
        0x7ff852b80000-0x7ff852c25000 C:\WINDOWS\System32\bcryptprimitives.dll
        0x7ff852c30000-0x7ff852d7b000 C:\WINDOWS\System32\ucrtbase.dll
        0x7ff852d80000-0x7ff852e02000 C:\WINDOWS\System32\WINTRUST.dll
        0x7ff852e10000-0x7ff852f7a000 C:\WINDOWS\System32\wintypes.dll
        0x7ff852f80000-0x7ff8530ab000 C:\WINDOWS\System32\gdi32full.dll
        0x7ff8530b0000-0x7ff853913000 C:\WINDOWS\System32\Windows.Storage.dll
        0x7ff8539e0000-0x7ff853a83000 C:\WINDOWS\System32\msvcp_win.dll
        0x7ff853a90000-0x7ff853e81000 C:\WINDOWS\System32\KERNELBASE.dll
        0x7ff853e90000-0x7ff854007000 C:\WINDOWS\System32\CRYPT32.dll
        0x7ff854010000-0x7ff854037000 C:\WINDOWS\System32\win32u.dll
        0x7ff854040000-0x7ff8541d7000 C:\WINDOWS\System32\ole32.dll
        0x7ff8541e0000-0x7ff85433f000 C:\WINDOWS\System32\MSCTF.dll
        0x7ff854360000-0x7ff854391000 C:\WINDOWS\System32\IMM32.DLL
        0x7ff854430000-0x7ff854b82000 C:\WINDOWS\System32\SHELL32.dll
        0x7ff854b90000-0x7ff854c44000 C:\WINDOWS\System32\ADVAPI32.dll
        0x7ff854d10000-0x7ff854ed6000 C:\WINDOWS\System32\USER32.dll
        0x7ff854fe0000-0x7ff855089000 C:\WINDOWS\System32\msvcrt.dll
        0x7ff855110000-0x7ff8551b6000 C:\WINDOWS\System32\sechost.dll
        0x7ff8551c0000-0x7ff855234000 C:\WINDOWS\System32\WS2_32.dll
        0x7ff855240000-0x7ff855336000 C:\WINDOWS\System32\shcore.dll
        0x7ff855420000-0x7ff8554e9000 C:\WINDOWS\System32\KERNEL32.DLL
        0x7ff8554f0000-0x7ff8554fa000 C:\WINDOWS\System32\NSI.dll
        0x7ff855520000-0x7ff855587000 C:\WINDOWS\System32\SHLWAPI.dll
        0x7ff8557b0000-0x7ff8558c8000 C:\WINDOWS\System32\RPCRT4.dll
        0x7ff855950000-0x7ff855dd9000 C:\WINDOWS\System32\SETUPAPI.dll
        0x7ff855de0000-0x7ff855e0b000 C:\WINDOWS\System32\GDI32.dll
        0x7ff855e10000-0x7ff856196000 C:\WINDOWS\System32\combase.dll
        0x7ff8561a0000-0x7ff856250000 C:\WINDOWS\System32\clbcatq.dll
        0x7ff8562a0000-0x7ff856508000 C:\WINDOWS\SYSTEM32\ntdll.dll
        0x7fff1e3d0000-0x7fff5bd2e000 D:\asan\chromium-146.0.7680.2-win64-asan\chrome.dll
        0x7fff87400000-0x7fff87e06000 D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll
        0x7fff8ff40000-0x7fff90501000 D:\asan\chromium-146.0.7680.2-win64-asan\chrome_elf.dll
AddressSanitizer: CHECK failed: sanitizer_common.cpp:61 "((0 && "unable to mmap")) != (0)" (0x0, 0x0) (tid=24052)
==4348==WARNING: Can't read from symbolizer at fd 4768
==4348==WARNING: Can't write to symbolizer at fd 4788
==24216==WARNING: Can't read from symbolizer at fd 588
==24216==WARNING: Can't write to symbolizer at fd 580
    #0 0x7fff8745826a  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005826a)
    #1 0x7fff874194e4  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x1800194e4)
    #2 0x7fff87405696  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x180005696)
    #3 0x7fff87414f62  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x180014f62)
    #4 0x7fff8743946f  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18003946f)
    #5 0x7fff8745b8b5  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005b8b5)
    #6 0x7fff8745bd5b  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005bd5b)
    #7 0x7fff8745bef5  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005bef5)
    #8 0x7fff8745dd4e  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005dd4e)
    #9 0x7ff85544e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #10 0x7ff85632c40b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c40b)

    #0 0x7fff8745826a  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005826a)
    #1 0x7fff874194e4  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x1800194e4)
    #2 0x7fff87405696  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x180005696)
    #3 0x7fff8741594e  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18001594e)
    #4 0x7fff8741b135  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18001b135)
    #5 0x7fff8741af7b  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18001af7b)
    #6 0x7fff8741d2a7  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18001d2a7)
    #7 0x7fff8741d75a  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18001d75a)
    #8 0x7fff8741d50f  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18001d50f)
    #9 0x7fff87432216  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x180032216)
    #10 0x7fff8742d108  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18002d108)
    #11 0x7fff8744c885  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18004c885)
    #12 0x7ff852c45d14  (C:\WINDOWS\System32\ucrtbase.dll+0x180015d14)
    #13 0x7ff82cce091b  (C:\WINDOWS\system32\PCPKsp.dll+0x18002091b)
    #14 0x7ff82cd079cb  (C:\WINDOWS\system32\PCPKsp.dll+0x1800479cb)
    #15 0x7ff82cce6c09  (C:\WINDOWS\system32\PCPKsp.dll+0x180026c09)
    #16 0x7ff82cd497a4  (C:\WINDOWS\system32\PCPKsp.dll+0x1800897a4)
    #17 0x7ff82cce8d66  (C:\WINDOWS\system32\PCPKsp.dll+0x180028d66)
    #18 0x7ff82cd1aa53  (C:\WINDOWS\system32\PCPKsp.dll+0x18005aa53)
    #19 0x7ff82ccfaa05  (C:\WINDOWS\system32\PCPKsp.dll+0x18003aa05)
    #20 0x7ff82ccfa7ee  (C:\WINDOWS\system32\PCPKsp.dll+0x18003a7ee)
    #21 0x7ff82ccfb84c  (C:\WINDOWS\system32\PCPKsp.dll+0x18003b84c)
    #22 0x7ff852391550  (C:\Windows\System32\ncrypt.dll+0x180011550)
    #23 0x7fff30d35d62 in crypto::`anonymous namespace'::UnexportableKeyProviderWin::GenerateSigningKeySlowly C:\b\s\w\ir\cache\builder\src\crypto\unexportable_key_win.cc:647:18
    #24 0x7fff30d2ffbf in crypto::`anonymous namespace'::MeasureTpmOperationsInternal C:\b\s\w\ir\cache\builder\src\crypto\unexportable_key_metrics.cc:231:17
    #25 0x7fff30d3291f in base::internal::DecayedFunctorTraits<void (*)(crypto::UnexportableKeyProvider::Config),crypto::UnexportableKeyProvider::Config &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:673
    #26 0x7fff30d3291f in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (*&&)(crypto::UnexportableKeyProvider::Config),crypto::UnexportableKeyProvider::Config &&>,void,0>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932
    #27 0x7fff30d3291f in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(crypto::UnexportableKeyProvider::Config),crypto::UnexportableKeyProvider::Config &&>,base::internal::BindState<0,1,0,void (*)(crypto::UnexportableKeyProvider::Config),crypto::UnexportableKeyProvider::Config>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069
    #28 0x7fff30d3291f in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl *&&)(struct crypto::UnexportableKeyProvider::Config), struct crypto::UnexportableKeyProvider::Config &&>, struct base::internal::BindState<0, 1, 0, void (__cdecl *)(struct crypto::UnexportableKeyProvider::Config), struct crypto::UnexportableKeyProvider::Config>, (void)>::RunOnce(class base::internal::BindStateBase *) C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982:12
    #29 0x7fff32716a98 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #30 0x7fff32716a98 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:229:34
    #31 0x7fff3266792c in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:112
    #32 0x7fff3266792c in base::internal::TaskTracker::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:687
    #33 0x7fff3266792c in base::internal::TaskTracker::RunContinueOnShutdown(struct base::internal::Task &, class base::TaskTraits const &, class base::internal::TaskSource *, class base::internal::SequenceToken const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:664:3
    #34 0x7fff326662f0 in base::internal::TaskTracker::RunTaskWithShutdownBehavior C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:699
    #35 0x7fff326662f0 in base::internal::TaskTracker::RunTask(struct base::internal::Task, class base::internal::TaskSource *, class base::TaskTraits const &) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:502:5
    #36 0x7fff326653dc in base::internal::TaskTracker::RunAndPopNextTask(class base::internal::RegisteredTaskSource) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:392:5
    #37 0x7fff3264ede0 in base::internal::WorkerThread::RunWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:473:36
    #38 0x7fff3264d54f in base::internal::WorkerThread::RunBackgroundPooledWorker(void) C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:364:3
    #39 0x7fff32542fde in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:112:13
    #40 0x7fff8745dd7e  (D:\asan\chromium-146.0.7680.2-win64-asan\clang_rt.asan_dynamic-x86_64.dll+0x18005dd7e)
    #41 0x7ff85544e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #42 0x7ff85632c40b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c40b)
PS D:\asan\chromium-146.0.7680.2-win64-asan> Received fatal exception 0xe0000008
        KERNELBASE!RaiseException [0x7ff853b5a80a+8a]
        chrome!partition_alloc::internal::OnNoMemoryInternal [0x7fff328f46c3+193] (C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\oom.cc:72)
        chrome!partition_alloc::TerminateBecauseOutOfMemory [0x7fff328f46f5+15] (C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\oom.cc:92)
        chrome!partition_alloc::internal::OnNoMemory [0x7fff328f471a+1a] (C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\oom.cc:102)
        chrome!blink::PartitionsOutOfMemoryUsing2G [0x7fff387cf5c0+f0] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\allocator\partitions.cc:268)
        chrome!blink::Partitions::HandleOutOfMemory [0x7fff387ce11f+24f] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\allocator\partitions.cc:413)
        chrome!partition_alloc::PartitionRoot::OutOfMemory [0x7fff328e2066+206] (C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.cc:862)
        chrome!partition_alloc::internal::`anonymous namespace'::PartitionOutOfMemoryMappingFailure [0x7fff328f0ee3+c3] (C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_bucket.cc:46)
        chrome!partition_alloc::internal::`anonymous namespace'::PartitionDirectMap [0x7fff328f0cc5+ce5] (C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_bucket.cc:276)
        chrome!partition_alloc::internal::PartitionBucket::SlowPathAlloc [0x7fff328eddcf+4ff] (C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_bucket.cc:1311)
        chrome!partition_alloc::PartitionRoot::Alloc<12> [0x7fff3cf9a7a3+1293] (C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:532)
        chrome!blink::ArrayBufferContents::ArrayBufferContents [0x7fff3cf96410+380] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\typed_arrays\array_buffer\array_buffer_contents.cc:0)
        chrome!mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView,blink::ArrayBufferContents>::Read [0x7fff3d796939+279] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\messaging\blink_transferable_message_mojom_traits.cc:171)
        chrome!mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>,blink::Vector<blink::ArrayBufferContents,1,blink::PartitionAllocator>,mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBuffer [0x7fff3d79829e+20e] (C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\array_serialization.h:433)
        chrome!mojo::StructTraits<blink::mojom::TransferableMessageDataView,blink::BlinkTransferableMessage>::Read [0x7fff3d79490b+35b] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\messaging\blink_transferable_message_mojom_traits.cc:107)
        chrome!blink::mojom::blink::LocalFrameStubDispatch::Accept [0x7fff2b47b7fe+1a7e] (C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\public\mojom\frame\frame.mojom-blink.cc:18721)
        chrome!mojo::InterfaceEndpointClient::HandleValidatedMessage [0x7fff3243bd95+bc5] (C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1088)
        chrome!mojo::MessageDispatcher::Accept [0x7fff324389fd+29d] (C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:51)
        chrome!mojo::InterfaceEndpointClient::HandleIncomingMessage [0x7fff3244247f+18f] (C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747)
        chrome!IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread [0x7fff35e3dbb7+4e7] (C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1199)
        chrome!base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous  [0x7fff35e400d2+1f2] (C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982)
        chrome!base::TaskAnnotator::RunTaskImpl [0x7fff32716a99+3c9] (C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:229)
        chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x7fff326e7067+c57] (C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:472)
        chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x7fff326e5ef4+1f4] (C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346)
        chrome!base::MessagePumpDefault::Run [0x7fff32850c21+311] (C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42)
        chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x7fff326e8d70+490] (C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:647)
        chrome!base::RunLoop::Run [0x7fff3278e6bd+4dd] (C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:137)
        chrome!content::RendererMain [0x7fff3cc75fc6+d86] (C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:369)
        chrome!content::RunOtherNamedProcessTypeMain [0x7fff2e38785e+3be] (C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:762)
        chrome!content::ContentMainRunnerImpl::Run [0x7fff2e389efc+7dc] (C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1147)
        chrome!content::RunContentProcess [0x7fff2e37ddd0+9c0] (C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:358)
        chrome!content::ContentMain [0x7fff2e37e573+1d3] (C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:371)
        chrome!ChromeMain [0x7fff1e3d2b07+5d7] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:191)
        chrome!MainDllLoader::Launch [0x7ff7854f4808+928] (C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:204)
        chrome!main [0x7ff7854f2075+1005] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351)
        chrome!__scrt_common_main_seh [0x7ff7859e9fc0+10c] (D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288)
        KERNEL32!BaseThreadInitThunk [0x7ff85544e8d7+17]
        ntdll!RtlUserThreadStart [0x7ff85632c40c+2c]
=================================================================
==9308==ERROR: AddressSanitizer: unknown exception on unknown address 0x7ff853b5a80a (pc 0x7ff853b5a80a bp 0x000000000003 sp 0x00591c3fdec0 T0)
==9308==*** WARNING: Failed to initialize DbgHelp!              ***
==9308==*** Most likely this means that the app is already      ***
==9308==*** using DbgHelp, possibly with incompatible flags.    ***
==9308==*** Due to technical reasons, symbolization might crash ***
==9308==*** or produce wrong results.                           ***
    #0 0x7ff853b5a809  (C:\WINDOWS\System32\KERNELBASE.dll+0x1800ca809)
    #1 0x7fff328f46c2 in partition_alloc::internal::OnNoMemoryInternal(unsigned __int64) C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\oom.cc:68:3
    #2 0x7fff328f46f4 in partition_alloc::TerminateBecauseOutOfMemory(unsigned __int64) C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\oom.cc:92:3
    #3 0x7fff328f4719 in partition_alloc::internal::OnNoMemory(unsigned __int64) C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\oom.cc:102:3
    #4 0x7fff387cf5bf in blink::PartitionsOutOfMemoryUsing2G C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\allocator\partitions.cc:268:3
    #5 0x7fff387ce11e in blink::Partitions::HandleOutOfMemory(unsigned __int64) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\allocator\partitions.cc:411:5
    #6 0x7fff328e2065 in partition_alloc::PartitionRoot::OutOfMemory(unsigned __int64) C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.cc:862:5
    #7 0x7fff328f0ee2 in partition_alloc::internal::`anonymous namespace'::PartitionOutOfMemoryMappingFailure C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_bucket.cc:46:9
    #8 0x7fff328f0cc4 in partition_alloc::internal::`anonymous namespace'::PartitionDirectMap C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_bucket.cc:273:7
    #9 0x7fff328eddce in partition_alloc::internal::PartitionBucket::SlowPathAlloc(class partition_alloc::PartitionRoot *, enum partition_alloc::internal::AllocFlags, unsigned __int64, unsigned __int64, struct partition_alloc::internal::SlotSpanMetadata **, bool *) C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_bucket.cc:1311:9
    #10 0x7fff3cf9a7a2 in partition_alloc::PartitionRoot::AllocFromBucket C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:1311
    #11 0x7fff3cf9a7a2 in partition_alloc::PartitionRoot::RawAlloc C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:2508
    #12 0x7fff3cf9a7a2 in partition_alloc::PartitionRoot::AllocInternalNoHooks C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:2404
    #13 0x7fff3cf9a7a2 in partition_alloc::PartitionRoot::AllocInternal C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:2321
    #14 0x7fff3cf9a7a2 in partition_alloc::PartitionRoot::AllocInline C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:538
    #15 0x7fff3cf9a7a2 in partition_alloc::PartitionRoot::Alloc<12>(unsigned __int64, char const *) C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\src\partition_alloc\partition_root.h:532:12
    #16 0x7fff3cf9640f in blink::ArrayBufferContents::AllocateMemory C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\typed_arrays\array_buffer\array_buffer_contents.cc:248
    #17 0x7fff3cf9640f in blink::ArrayBufferContents::ArrayBufferContents(unsigned __int64, class std::__Cr::optional<unsigned __int64>, unsigned __int64, enum blink::ArrayBufferContents::SharingType, enum blink::ArrayBufferContents::InitializationPolicy, enum blink::ArrayBufferContents::AllocationFailureBehavior) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\typed_arrays\array_buffer\array_buffer_contents.cc
    #18 0x7fff3d796938 in mojo::StructTraits<class blink::mojom::SerializedArrayBufferContentsDataView, class blink::ArrayBufferContents>::Read(class blink::mojom::SerializedArrayBufferContentsDataView, class blink::ArrayBufferContents *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\messaging\blink_transferable_message_mojom_traits.cc:171:30
    #19 0x7fff3d79829d in mojo::internal::Serializer<blink::mojom::SerializedArrayBufferContentsDataView,blink::ArrayBufferContents>::Deserialize C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\public\mojom\array_buffer\array_buffer_contents.mojom-shared.h:86
    #20 0x7fff3d79829d in mojo::internal::Deserialize C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\serialization_forward.h:73
    #21 0x7fff3d79829d in mojo::internal::ArraySerializer<class mojo::ArrayDataView<class blink::mojom::SerializedArrayBufferContentsDataView>, class blink::Vector<class blink::ArrayBufferContents, 1, class blink::PartitionAllocator>, class mojo::internal::ArrayIterator<struct mojo::ArrayTraits<class blink::Vector<class blink::ArrayBufferContents, 1, class blink::PartitionAllocator>>, class blink::Vector<class blink::ArrayBufferContents, 1, class blink::PartitionAllocator>, 0>>::DeserializeElements(class mojo::internal::Array_Data<struct mojo::internal::Pointer<class blink::mojom::internal::SerializedArrayBufferContents_Data>> *, class blink::Vector<class blink::ArrayBufferContents, 1, class blink::PartitionAllocator> *, class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\array_serialization.h:433:12
    #22 0x7fff3d79490a in mojo::internal::Serializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>,blink::Vector<blink::ArrayBufferContents,1,blink::PartitionAllocator> >::Deserialize C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\array_serialization.h:553
    #23 0x7fff3d79490a in mojo::internal::Deserialize C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\serialization_forward.h:73
    #24 0x7fff3d79490a in blink::mojom::TransferableMessageDataView::ReadArrayBufferContentsArray C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\public\mojom\messaging\transferable_message.mojom-data-view.h:110
    #25 0x7fff3d79490a in mojo::StructTraits<class blink::mojom::TransferableMessageDataView, struct blink::BlinkTransferableMessage>::Read(class blink::mojom::TransferableMessageDataView, struct blink::BlinkTransferableMessage *) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\messaging\blink_transferable_message_mojom_traits.cc:107:13
    #26 0x7fff2b47b7fd in mojo::internal::Serializer<blink::mojom::TransferableMessageDataView,blink::BlinkTransferableMessage>::Deserialize C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\public\mojom\messaging\transferable_message.mojom-shared.h:208
    #27 0x7fff2b47b7fd in mojo::internal::Deserialize C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\serialization_forward.h:73
    #28 0x7fff2b47b7fd in blink::mojom::LocalFrame_PostMessageEvent_ParamsDataView::ReadMessage C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\public\mojom\frame\frame.mojom-params-data.h:6718
    #29 0x7fff2b47b7fd in blink::mojom::blink::LocalFrameStubDispatch::Accept(class blink::mojom::blink::LocalFrame *, class mojo::Message *) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\public\mojom\frame\frame.mojom-blink.cc:18721:39
    #30 0x7fff3243bd94 in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1085:54
    #31 0x7fff324389fc in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:51:24
    #32 0x7fff3244247e in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:747:20
    #33 0x7fff35e3dbb6 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1199:24
    #34 0x7fff35e400d1 in base::internal::DecayedFunctorTraits<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:740
    #35 0x7fff35e400d1 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,void,0,1,2>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:932
    #36 0x7fff35e400d1 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,base::internal::BindState<1,1,0,void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),scoped_refptr<IPC::ChannelAssociatedGroupController>,mojo::Message,IPC::`anonymous namespace'::ScopedUrgentMessageNotification>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1069
    #37 0x7fff35e400d1 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::`anonymous namespace'::ScopedUrgentMessageNotification &&>,base::internal::BindState<1,1,0,void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::`anonymous namespace'::ScopedUrgentMessageNotification),scoped_refptr<IPC::ChannelAssociatedGroupController>,mojo::Message,IPC::`anonymous namespace'::ScopedUrgentMessageNotification>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:982:12
    #38 0x7fff32716a98 in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:155
    #39 0x7fff32716a98 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:229:34
    #40 0x7fff326e7066 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:112
    #41 0x7fff326e7066 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:472:23
    #42 0x7fff326e5ef3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:346:40
    #43 0x7fff32850c20 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:42:55
    #44 0x7fff326e8d6f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:647:12
    #45 0x7fff3278e6bc in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:135:14
    #46 0x7fff3cc75fc5 in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:369:16
    #47 0x7fff2e38785d in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:762:14
    #48 0x7fff2e389efb in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1147:10
    #49 0x7fff2e37ddcf in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:358:36
    #50 0x7fff2e37e572 in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:371:10
    #51 0x7fff1e3d2b06 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:191:12
    #52 0x7ff7854f4807 in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:204:12
    #53 0x7ff7854f2074 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:351:20
    #54 0x7ff7859e9fbf in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #55 0x7ff7859e9fbf in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #56 0x7ff85544e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #57 0x7ff85632c40b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c40b)

==9308==Register values:
rax = 1e1630400d8  rbx = 1e10151e840  rcx = 1  rdx = 7fff8743226e
rdi = e0000008  rsi = 1  rbp = 3  rsp = 591c3fdec0
r8  = 7fff8742d2b0  r9  = 7fff8745f157  r10 = 591c3fd240  r11 = 1e1630400d8
r12 = 1e163380000  r13 = 3c202a3d00  r14 = 1e10151e848  r15 = 1e10151e880
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: unknown exception (C:\WINDOWS\System32\KERNELBASE.dll+0x1800ca809)

==9308==ADDITIONAL INFO

==9308==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7fff35e379d9 in IPC::ChannelAssociatedGroupController::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1138:13


Command line: `"D:\asan\chromium-146.0.7680.2-win64-asan\chrome.exe" --type=renderer --no-pre-read-main-dll --start-stack-profiler --no-sandbox --file-url-path-alias="/gen=D:\asan\chromium-146.0.7680.2-win64-asan\gen" --video-capture-use-gpu-memory-buffer --lang=en-GB --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=6 --time-ticks-at-unix-epoch=-1770798845742282 --launch-time-ticks=4429262234 --metrics-shmem-handle=3628,i,17760320730036678764,16441529384394133465,2097152 --field-trial-handle=1800,i,8562694781650815085,5659428738592661033,262144 --variations-seed-version --pseudonymization-salt-handle=1796,i,16933453736116520373,2695850560606981916,4 --trace-process-track-uuid=3190708991934122588 --enable-logging=stderr --v=1 --mojo-platform-channel-handle=3636 /prefetch:1`


==9308==END OF ADDITIONAL INFO

==9308==ABORTING

```

### mu...@gmail.com (2026-02-11)

I have successfully reproduced the bug and submitted the corresponding crash reports using the official / stable build.

Could you please verify if the reports `216e5515a0c10a96` and `c2cea45792b4f33e` have been reviewed or analyzed internally?, I would appreciate it if this account could be CC'ed or added to those reports for further tracking.

Thank you for your assistance.
Best regards.

### mu...@gmail.com (2026-02-12)

Hi Team.

I would provide a new info.

I have built the chromium with debug version, then I got the errors:

```
Received signal 7 BUS_ADRERR 7678135ea000
#0 0x7678904ea909 base::debug::CollectStackTrace() [../../base/debug/stack_trace_posix.cc:1048:7]
#1 0x76789049454a base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:280:20]
#2 0x7678904944b5 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:275:28]
#3 0x7678904ea179 base::debug::(anonymous namespace)::StackDumpSignalHandler() [../../base/debug/stack_trace_posix.cc:483:3]
#4 0x767837045330 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4532f)
#5 0x7678371a167f (/usr/lib/x86_64-linux-gnu/libc.so.6+0x1a167e)
#6 0x767861336991 std::__Cr::__constexpr_memmove<>() [gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227:5]
#7 0x767861336924 std::__Cr::__copy_trivial_impl<>() [gen/third_party/libc++/src/include/__algorithm/copy_move_common.h:64:3]
#8 0x767861336759 _ZNKSt4__Cr11__copy_implclIKhhTnNS_9enable_ifIXsr38__can_lower_copy_assignment_to_memmoveIT_T0_EE5valueEiE4typeELi0EEENS_4pairIPS4_PS5_EES9_S9_SA_ [gen/third_party/libc++/src/include/__algorithm/copy.h:127:12]
#9 0x767861370498 _ZNSt4__Cr24__copy_move_unwrap_itersINS_11__copy_implEN4base25CheckedContiguousIteratorIKhEES5_NS3_IhEETnNS_9enable_ifIXsr12__can_rewrapIT0_T2_EE5valueEiE4typeELi0EEENS_4pairIS8_S9_EES8_T1_S9_ [gen/third_party/libc++/src/include/__algorithm/copy_move_common.h:94:19]
#10 0x7678613702e1 std::__Cr::__copy<>() [gen/third_party/libc++/src/include/__algorithm/copy.h:134:10]
#11 0x76786140457e _ZNKSt4__Cr6ranges6__copyclITkNS0_11input_rangeERN4base4spanIKhLm18446744073709551615EPS5_EETkNS_20weakly_incrementableENS3_25CheckedContiguousIteratorIhEEQ19indirectly_copyableIDTclL_ZNS0_5__cpo5beginEEclsr3stdE7declvalIRT_EEEET0_EEENS0_13in_out_resultINS_7_IfImplIX14borrowed_rangeISC_EEE7_SelectISE_NS0_8danglingEEESF_EEOSC_SF_ [gen/third_party/libc++/src/include/__algorithm/ranges_copy.h:52:18]
#12 0x7678614041f7 _ZN4base4spanIhLm18446744073709551615EPhE9copy_fromENS0_IKhLm18446744073709551615EPS3_EEQntsr3stdE10is_const_vIT_E [../../base/containers/span.h:1138:9]
#13 0x767864bc5532 mojo::StructTraits<>::Read() [../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:176:36]
#14 0x767864bc9313 mojo::internal::Serializer<>::Deserialize() [gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86:12]
#15 0x767864bc904b mojo::internal::Deserialize<>() [../../mojo/public/cpp/bindings/lib/serialization_forward.h:73:12]
#16 0x767864bc8e98 mojo::internal::ArraySerializer<>::DeserializeElements() [../../mojo/public/cpp/bindings/lib/array_serialization.h:433:12]
#17 0x767864bc8dac mojo::internal::Serializer<>::Deserialize() [../../mojo/public/cpp/bindings/lib/array_serialization.h:553:12]
#18 0x767864bc8d5b mojo::internal::Deserialize<>() [../../mojo/public/cpp/bindings/lib/serialization_forward.h:73:12]
#19 0x767864bc598d blink::mojom::TransferableMessageDataView::ReadArrayBufferContentsArray<>() [gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-data-view.h:110:12]
#20 0x767864bc4dc3 mojo::StructTraits<>::Read() [../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:107:13]
#21 0x767864bf5713 mojo::internal::Serializer<>::Deserialize() [gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208:12]
#22 0x7678662bd95b mojo::internal::Deserialize<>()
#23 0x76786623849d blink::mojom::LocalFrame_PostMessageEvent_ParamsDataView::ReadMessage<>() [gen/third_party/blink/public/mojom/frame/frame.mojom-params-data.h:6753:12]
#24 0x76786620cd30 blink::mojom::blink::LocalFrameStubDispatch::Accept() [gen/third_party/blink/public/mojom/frame/frame.mojom-blink.cc:18721:39]
#25 0x767862ff7ee6 blink::mojom::blink::LocalFrameStub<>::Accept() [gen/third_party/blink/public/mojom/frame/frame.mojom-blink.h:1887:12]
#26 0x76788fb8e890 mojo::InterfaceEndpointClient::HandleValidatedMessage() [../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54]
#27 0x76788fb8dfb4 mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept() [../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:383:18]
#28 0x76788fba7456 mojo::MessageDispatcher::Accept() [../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24]
#29 0x76788fb906e1 mojo::InterfaceEndpointClient::HandleIncomingMessage() [../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20]
#30 0x76788995b327 IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread() [../../ipc/ipc_mojo_bootstrap.cc:1199:24]
#31 0x76788995c52a base::internal::DecayedFunctorTraits<>::Invoke<>() [../../base/functional/bind_internal.h:740:12]
#32 0x76788995c43b base::internal::InvokeHelper<>::MakeItSo<>() [../../base/functional/bind_internal.h:932:12]
#33 0x76788995c39d base::internal::Invoker<>::RunImpl<>() [../../base/functional/bind_internal.h:1069:14]
#34 0x76788995c309 base::internal::Invoker<>::RunOnce() [../../base/functional/bind_internal.h:982:12]
#35 0x7678900fd31c base::OnceCallback<>::Run() [../../base/functional/callback.h:155:12]
#36 0x76789030463e base::TaskAnnotator::RunTaskImpl() [../../base/task/common/task_annotator.cc:229:34]
#37 0x76789037bf18 base::TaskAnnotator::RunTask<>() [../../base/task/common/task_annotator.h:112:5]
#38 0x76789037b9ae base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl() [../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:472:23]
#39 0x76789037b01a base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() [../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40]
#40 0x76789037bbe3 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#41 0x767890194078 base::MessagePumpDefault::Run() [../../base/message_loop/message_pump_default.cc:42:55]
#42 0x76789037c5b7 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run() [../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:647:12]
#43 0x7678902715eb base::RunLoop::Run() [../../base/run_loop.cc:135:14]
#44 0x767899f76052 content::RendererMain() [../../content/renderer/renderer_main.cc:369:16]
#45 0x76789a3f4581 content::RunZygote() [../../content/app/content_main_runner_impl.cc:664:14]
#46 0x76789a3f4e09 content::RunOtherNamedProcessTypeMain() [../../content/app/content_main_runner_impl.cc:771:12]
#47 0x76789a3f63b1 content::ContentMainRunnerImpl::Run() [../../content/app/content_main_runner_impl.cc:1147:10]
#48 0x76789a3f246d content::RunContentProcess() [../../content/app/content_main.cc:358:36]
#49 0x76789a3f2976 content::ContentMain() [../../content/app/content_main.cc:371:10]
#50 0x5aa659cb5109 main
#51 0x76783702a1ca (/usr/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9)
#52 0x76783702a28b __libc_start_main
#53 0x5aa659cb4faa _start
  r8: 000019482b404000  r9: ffffa2d017ed6000 r10: 0000000000000000 r11: 0000000000000246
 r12: 0000000000000005 r13: 0000000000000000 r14: 0000000000000000 r15: 000076789bf91000
  di: 000019482b4c0000  si: 00007678135ea000  bp: 00007ffdc32fbfd0  bx: 00007ffdc32ffc88
  dx: 00000000000d1600  ax: 000019482b404000  cx: 0000000000015600  sp: 00007ffdc32fbfa8
  ip: 00007678371a167f efl: 0000000000010212 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 00007678135ea000
[end of stack trace]

```

### mu...@gmail.com (2026-02-13)

I think, when an ArrayBuffer larger than 64KB is transferred via postMessage() between the parent and the iframe, Chromium uses `mojom::BigBuffer` which creates a shared memory region in `/dev/shm`. From analyzing `sudo lsof | grep "/dev/shm"`, it can be seen that 8 Chrome threads are accessing the same shared memory file simultaneously. The bug occurs due to size confusion: the serializing thread reads size metadata from the writable FD, but during deserialization a concurrent operation like ConvertToReadOnly() swaps the FD handles occurs, so the deserializer thread reads different size metadata from the readonly FD - resulting in memcpy trying to copy more bytes than it actually allocated (e.g. claiming 11.6MB when it is actually only 1.5MB), causing a SIGBUS crash at Blink\_transferable\_message\_mojom\_traits.cc:176 when accessing unmapped memory.

### mu...@gmail.com (2026-02-16)

Hi Google Chrome Security team.

After performing some reproductions on Linux, Windows, and the stable build, along with the crash report ID sent internally via the stable build, I'm curious about this report.

Is this report valid or invalid?

Is it appropriate to change the status of this report from new to triaged?

Thank you for your attention. Best regards.

### mu...@gmail.com (2026-02-17)

In chrome android:

### ma...@google.com (2026-02-17)

Security shepherd: Thanks for the additional repro work and crash reports (216e5515a0c10a96 and c2cea45792b4f33e). I'm unsure whether this crash has security implications. Blink messaging owners, could you help assess this further?

For now, I'm provisionally marking this S1 to get it out of the triage queue.

### me...@chromium.org (2026-02-17)

This almost sounds more like a mojo issue than a messaging issue. Or at least I don't think the messaging code is doing anything particularly weird here, besides using BigBuffer in as far as I can tell the "correct" way. Maybe @dc...@chromium.org has more insights?

### mu...@gmail.com (2026-02-17)

Hi team.
After analyzing and debugging with my latest poc,
when transferring a buffer between an iframe and its parent process.
This is a race condition, and the buffer is continuously sent.
I suspect that when the transfer buffer then goes through the mojo, because the old buffer is never used, it triggers garbage collection.
In fact, the buffer is in the memcpy process, triggering a sigbus because the pointer referring to the buffer has been detached or unmapped.

It's probably a use-after-unmap case.

Here's the latest poc and debug version backtrace.

```
#0  __memcpy_avx512_unaligned_erms () at ../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:590
#1  0x00007f98d0adc071 in std::__Cr::__constexpr_memmove<unsigned char, unsigned char const> (__dest=0x268c17144000 "\253\253\253\253\253\253\253\253\253\253"..., __src=0x7f97d82f7000 "\315\314LN\315\314LN\315", <incomplete sequence \314>..., __n=589824) at gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227
#2  0x00007f98d0adc004 in std::__Cr::__copy_trivial_impl<unsigned char const, unsigned char> (__first=0x7f97d82f7000 "\315\314LN\315\314LN\315", <incomplete sequence \314>..., __last=0x7f97d8387000 "", __result=0x268c17144000 "\253\253\253\253\253\253\253\253\253\253"...) at gen/third_party/libc++/src/include/__algorithm/copy_move_common.h:64
#3  0x00007f98d0adbe39 in operator()<const unsigned char, unsigned char, 0> (this=0x7fffd9e7744f, __first=0x7f97d82f7000 "\315\314LN\315\314LN\315", <incomplete sequence \314>..., __last=0x7f97d8387000 "", __result=0x268c17144000 "\253\253\253\253\253\253\253\253\253\253"...) at gen/third_party/libc++/src/include/__algorithm/copy.h:127
#4  0x00007f98d0b15b78 in __copy_move_unwrap_iters (__first=..., __last=..., __out_first=...) at gen/third_party/libc++/src/include/__algorithm/copy_move_common.h:94
#5  0x00007f98d0b159c1 in std::__Cr::__copy<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char> > (__first=..., __last=..., __result=...) at gen/third_party/libc++/src/include/__algorithm/copy.h:134
#6  0x00007f98d0ba9c5e in operator()<base::span<const unsigned char, 18446744073709551615UL, const unsigned char *> &, base::CheckedContiguousIterator<unsigned char> > (this=0x7f98ce8df4f0 <std::__Cr::ranges::__cpo::copy>, __r=..., __result=...) at gen/third_party/libc++/src/include/__algorithm/ranges_copy.h:52
#7  0x00007f98d0ba98d7 in copy_from (this=0x7fffd9e777b8, other=...) at ../../base/containers/span.h:1138
#8  0x00007f98d439e4e2 in mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Read (data=..., out=0x7fffd9e77d08) at ../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:176
#9  0x00007f98d43a22c3 in mojo::internal::Serializer<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Deserialize (input=0x387c00c15d00, output=0x7fffd9e77d08, message=0x7fffd9e795d0) at gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86
#10 0x00007f98d43a1ffb in mojo::internal::Deserialize<blink::mojom::SerializedArrayBufferContentsDataView, blink::mojom::internal::SerializedArrayBufferContents_Data*, blink::ArrayBufferContents, mojo::Message*&> (input=@0x7fffd9e77930: 0x387c00c15d00, output=0x7fffd9e77d08, args=@0x7fffd9e77950: 0x7fffd9e795d0) at ../../mojo/public/cpp/bindings/lib/serialization_forward.h:73
#11 0x00007f98d43a1e48 in mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator> >, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, false> >::DeserializeElements (input=0x387c00c15cf0, output=0x7fffd9e77cf8, message=0x7fffd9e795d0) at ../../mojo/public/cpp/bindings/lib/array_serialization.h:433
#12 0x00007f98d43a1d5c in mojo::internal::Serializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator> >::Deserialize (input=0x387c00c15cf0, output=0x7fffd9e77cf8, message=0x7fffd9e795d0) at ../../mojo/public/cpp/bindings/lib/array_serialization.h:553
#13 0x00007f98d43a1d0b in mojo::internal::Deserialize<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, mojo::internal::Array_Data<mojo::internal::Pointer<blink::mojom::internal::SerializedArrayBufferContents_Data> >*&, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::Message*&> (input=@0x7fffd9e779e8: 0x387c00c15cf0, output=0x7fffd9e77cf8, args=@0x7fffd9e77b40: 0x7fffd9e795d0) at ../../mojo/public/cpp/bindings/lib/serialization_forward.h:73
#14 0x00007f98d439e93d in blink::mojom::TransferableMessageDataView::ReadArrayBufferContentsArray<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator> > (this=0x7fffd9e77b38, output=0x7fffd9e77cf8) at gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-data-view.h:110
#15 0x00007f98d439dd73 in mojo::StructTraits<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Read (data=..., out=0x7fffd9e787e0) at ../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:107
#16 0x00007f98d43ce6c3 in mojo::internal::Serializer<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Deserialize (input=0x387c00c15bf0, output=0x7fffd9e787e0, message=0x7fffd9e795d0) at gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208
#17 0x00007f98d5b1d87b in mojo::internal::Deserialize<blink::mojom::TransferableMessageDataView, blink::mojom::internal::TransferableMessage_Data*&, blink::BlinkTransferableMessage, mojo::Message*&> (input=@0x7fffd9e77db8: 0x387c00c15bf0, output=0x7fffd9e787e0, args=@0x7fffd9e787d8: 0x7fffd9e795d0) at ../../mojo/public/cpp/bindings/lib/serialization_forward.h:73
#18 0x00007f98d5a90cdd in blink::mojom::LocalFrame_PostMessageEvent_ParamsDataView::ReadMessage<blink::BlinkTransferableMessage> (this=0x7fffd9e787d0, output=0x7fffd9e787e0) at gen/third_party/blink/public/mojom/frame/frame.mojom-params-data.h:6706
#19 0x00007f98d5a05bb0 in blink::mojom::blink::LocalFrameStubDispatch::Accept (impl=0x1f5c0048dc88, message=0x7fffd9e795d0) at gen/third_party/blink/public/mojom/frame/frame.mojom-blink.cc:18709
#20 0x00007f98d27bbec6 in blink::mojom::blink::LocalFrameStub<mojo::RawPtrImplRefTraits<blink::mojom::blink::LocalFrame> >::Accept (this=0x1f5c0048de28, message=0x7fffd9e795d0) at gen/third_party/blink/public/mojom/frame/frame.mojom-blink.h:1875
#21 0x00007f9936d2c850 in mojo::InterfaceEndpointClient::HandleValidatedMessage (this=0x387c007cde80, message=0x7fffd9e795d0) at ../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085
#22 0x00007f9936d2bf74 in mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept (this=0x387c007cdfc0, message=0x7fffd9e795d0) at ../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:383
#23 0x00007f9936d45416 in mojo::MessageDispatcher::Accept (this=0x387c007cdfd0, message=0x7fffd9e795d0) at ../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51
#24 0x00007f9936d2e6a1 in mojo::InterfaceEndpointClient::HandleIncomingMessage (this=0x387c007cde80, message=0x7fffd9e795d0) at ../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747
#25 0x00007f99215d23b7 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread (this=0x387c00014200, message=..., scoped_urgent_message_notification=...) at ../../ipc/ipc_mojo_bootstrap.cc:1199
#26 0x00007f99215d35ba in base::internal::DecayedFunctorTraits<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>::Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> (method=(void (IPC::ChannelAssociatedGroupController::*)(IPC::ChannelAssociatedGroupController * const, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)) 0x7f99215d21d0 <IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)>, receiver_ptr=scoped_refptr((IPC::ChannelAssociatedGroupController *)0x387c00014200), args=..., args=...) at ../../base/functional/bind_internal.h:740
#27 0x00007f99215d34cb in base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, void, 0ul, 1ul, 2ul>::MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>>(void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>&&) (functor=@0x387c00b10430: (void (IPC::ChannelAssociatedGroupController::*)(IPC::ChannelAssociatedGroupController * const, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)) 0x7f99215d21d0 <IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)>, bound=...) at ../../base/functional/bind_internal.h:932
#28 0x00007f99215d342d in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void()>::RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0ul, 1ul, 2ul> (functor=@0x387c00b10430: (void (IPC::ChannelAssociatedGroupController::*)(IPC::ChannelAssociatedGroupController * const, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)) 0x7f99215d21d0 <IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)>, bound=...) at ../../base/functional/bind_internal.h:1069
#29 0x00007f99215d3399 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void()>::RunOnce (base=0x387c00b10410) at ../../base/functional/bind_internal.h:982
#30 0x00007f99355004cc in base::OnceCallback<void ()>::Run() && (this=0x387c00637078) at ../../base/functional/callback.h:155
#31 0x00007f993570781e in base::TaskAnnotator::RunTaskImpl (this=0x387c000942f8, pending_task=From Accept()@ipc/ipc_mojo_bootstrap.cc:0x472 = {...}) at ../../base/task/common/task_annotator.cc:229
#32 0x00007f993577f258 in base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_4>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_4&&) (this=0x387c000942f8, event_name=..., pending_task=From Accept()@ipc/ipc_mojo_bootstrap.cc:0x472 = {...}, args=...) at ../../base/task/common/task_annotator.h:112
#33 0x00007f993577ece5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl (this=0x387c00094000, continuation_lazy_now=0x7fffd9e79c40) at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475
#34 0x00007f993577e34a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork (this=0x387c00094000) at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346
#35 0x00007f993577ef23 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() () from /home/muriarfad/chromium/src/out/debug/libbase.so
#36 0x00007f9935597468 in base::MessagePumpDefault::Run (this=0x387c00034360, delegate=0x387c00094120) at ../../base/message_loop/message_pump_default.cc:42
#37 0x00007f993577f8f7 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run (this=0x387c00094000, application_tasks_allowed=0x1, timeout=106751991 days, 4:00:54.775807) at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650
#38 0x00007f993567485b in base::RunLoop::Run (this=0x7fffd9e7a078, location=RendererMain()@content/renderer/renderer_main.cc:0x16c) at ../../base/run_loop.cc:135
#39 0x00007f992b1b5833 in content::RendererMain (parameters=...) at ../../content/renderer/renderer_main.cc:364
#40 0x00007f992b65e767 in content::RunZygote (delegate=0x7fffd9e7b1f8) at ../../content/app/content_main_runner_impl.cc:664
#41 0x00007f992b65efe9 in content::RunOtherNamedProcessTypeMain (process_type=..., main_function_params=..., delegate=0x7fffd9e7b1f8) at ../../content/app/content_main_runner_impl.cc:771
#42 0x00007f992b6605fb in content::ContentMainRunnerImpl::Run (this=0x3878000bc000) at ../../content/app/content_main_runner_impl.cc:1147
#43 0x00007f992b65c5ed in content::RunContentProcess (params=..., content_main_runner=0x3878000bc000) at ../../content/app/content_main.cc:358
#44 0x00007f992b65caf6 in content::ContentMain (params=...) at ../../content/app/content_main.cc:371
#45 0x000058d2c62d66e0 in ChromeMain (argc=0x8, argv=0x7fffd9e7b3e8) at ../../chrome/app/chrome_main.cc:191
#46 0x000058d2c62d6392 in main (argc=0x8, argv=0x7fffd9e7b3e8) at ../../chrome/app/chrome_exe_main_aura.cc:17
#47 0x00007f98b3e2a1ca in __libc_start_call_main (main=main@entry=0x58d2c62d6370 <main(int, char const**)>, argc=argc@entry=0x8, argv=argv@entry=0x7fffd9e7b3e8) at ../sysdeps/nptl/libc_start_call_main.h:58
#48 0x00007f98b3e2a28b in __libc_start_main_impl (main=0x58d2c62d6370 <main(int, char const**)>, argc=0x8, argv=0x7fffd9e7b3e8, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7fffd9e7b3d8) at ../csu/libc-start.c:360
#49 0x000058d2c62d62aa in _start ()

```

### mu...@gmail.com (2026-02-17)

[#439305148](https://issues.chromium.org/issues/439305148), same sigbus but different root cause?

### aj...@chromium.org (2026-02-17)

+mojo friends - reporter - thanks for all the examples we probably have enough to go on here - the Windows crash is an OOM but the linux ones look actionable.

### ch...@google.com (2026-02-18)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-18)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mu...@gmail.com (2026-02-24)

```
rax            0xddc1b344000       0xddc1b344000
rbx            0x7ffe535996b8      0x7ffe535996b8
rcx            0x40000             0x40000
rdx            0x80000             0x80000
rsi            0x739e06159000      0x739e06159000
rdi            0xddc1b384000       0xddc1b384000
rbp            0x7ffe53595400      0x7ffe53595400
rsp            0x7ffe535953d8      0x7ffe535953d8
r8             0xddc1b344000       0xddc1b344000
r9             0xffff9a3e1522b000  0xffff9a3e1522b000
r10            0x0                 0x0
r11            0x246               0x246
r12            0x8                 0x8
r13            0x0                 0x0
r14            0x0                 0x0
r15            0x739eb6b27000      0x739eb6b27000
rip            0x739e33ba167f      0x739e33ba167f <__memcpy_avx512_unaligned_erms+831>
eflags         0x10212             [ AF IF RF ]
cs             0x33                0x33
ss             0x2b                0x2b
ds             0x0                 0x0
es             0x0                 0x0
fs             0x0                 0x0
gs             0x0                 0x0
k0             0x9000              0x9000
k1             0xffffffffffff      0xffffffffffff
k2             0xffffffff          0xffffffff
k3             0x0                 0x0
k4             0x10020020          0x10020020
k5             0x0                 0x0
k6             0x4000080001000     0x4000080001000
k7             0x0                 0x0
fs_base        0x739e0d706dc0      0x739e0d706dc0
gs_base        0x0                 0x0
#0  __memcpy_avx512_unaligned_erms () at ../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:590
#1  0x0000739e506d3e61 in std::__Cr::__constexpr_memmove<unsigned char, unsigned char const> (__dest=0xddc1b344000 "\253\253\253\253\253"..., __src=0x739e06119000 "\315\314L", <incomplete sequence \315>..., __n=524288) at gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227
#2  0x0000739e506d3df4 in std::__Cr::__copy_trivial_impl<unsigned char const, unsigned char> (__first=0x739e06119000 "\315\314L", <incomplete sequence \315>..., __last=0x739e06199000 "", __result=0xddc1b344000 "\253\253\253\253\253"...) at gen/third_party/libc++/src/include/__algorithm/copy_move_common.h:64
#3  0x0000739e506d3c29 in operator()<const unsigned char, unsigned char, 0> (this=0x7ffe5359557f, __first=0x739e06119000 "\315\314L", <incomplete sequence \315>..., __last=0x739e06199000 "", __result=0xddc1b344000 "\253\253\253\253\253"...) at gen/third_party/libc++/src/include/__algorithm/copy.h:127
#4  0x0000739e5070d978 in __copy_move_unwrap_iters (__first=..., __last=..., __out_first=...) at gen/third_party/libc++/src/include/__algorithm/copy_move_common.h:94
#5  0x0000739e5070d7c1 in std::__Cr::__copy<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char> > (__first=..., __last=..., __result=...) at gen/third_party/libc++/src/include/__algorithm/copy.h:134
#6  0x0000739e507a1a0e in operator()<base::span<const unsigned char, 18446744073709551615UL, const unsigned char *> &, base::CheckedContiguousIterator<unsigned char> > (this=0x739e4e4dc0e0 <std::__Cr::ranges::__cpo::copy>, __r=..., __result=...) at gen/third_party/libc++/src/include/__algorithm/ranges_copy.h:52
#7  0x0000739e507a1687 in copy_from (this=0x7ffe535958e0, other=...) at ../../base/containers/span.h:1138
#8  0x0000739e53f7767f in mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Read (data=..., out=0x7ffe53595e28) at ../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:156
#9  0x0000739e53f7b4b3 in mojo::internal::Serializer<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Deserialize (input=0x31fc012d5c00, output=0x7ffe53595e28, message=0x7ffe535976f0) at gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86
#10 0x0000739e53f7b1eb in mojo::internal::Deserialize<blink::mojom::SerializedArrayBufferContentsDataView, blink::mojom::internal::SerializedArrayBufferContents_Data*, blink::ArrayBufferContents, mojo::Message*&> (input=@0x7ffe53595a50: 0x31fc012d5c00, output=0x7ffe53595e28, args=@0x7ffe53595a70: 0x7ffe535976f0) at ../../mojo/public/cpp/bindings/lib/serialization_forward.h:73
#11 0x0000739e53f7b038 in mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator> >, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, false> >::DeserializeElements (input=0x31fc012d5bf0, output=0x7ffe53595e18, message=0x7ffe535976f0) at ../../mojo/public/cpp/bindings/lib/array_serialization.h:433
#12 0x0000739e53f7af4c in mojo::internal::Serializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator> >::Deserialize (input=0x31fc012d5bf0, output=0x7ffe53595e18, message=0x7ffe535976f0) at ../../mojo/public/cpp/bindings/lib/array_serialization.h:553
#13 0x0000739e53f7aefb in mojo::internal::Deserialize<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, mojo::internal::Array_Data<mojo::internal::Pointer<blink::mojom::internal::SerializedArrayBufferContents_Data> >*&, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::Message*&> (input=@0x7ffe53595b08: 0x31fc012d5bf0, output=0x7ffe53595e18, args=@0x7ffe53595c60: 0x7ffe535976f0) at ../../mojo/public/cpp/bindings/lib/serialization_forward.h:73
#14 0x0000739e53f77add in blink::mojom::TransferableMessageDataView::ReadArrayBufferContentsArray<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator> > (this=0x7ffe53595c58, output=0x7ffe53595e18) at gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-data-view.h:110
#15 0x0000739e53f76f53 in mojo::StructTraits<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Read (data=..., out=0x7ffe53596900) at ../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:95
#16 0x0000739e53fa7963 in mojo::internal::Serializer<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Deserialize (input=0x31fc012d5af0, output=0x7ffe53596900, message=0x7ffe535976f0) at gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208
#17 0x0000739e556eea8b in mojo::internal::Deserialize<blink::mojom::TransferableMessageDataView, blink::mojom::internal::TransferableMessage_Data*&, blink::BlinkTransferableMessage, mojo::Message*&> (input=@0x7ffe53595ed8: 0x31fc012d5af0, output=0x7ffe53596900, args=@0x7ffe535968f8: 0x7ffe535976f0) at ../../mojo/public/cpp/bindings/lib/serialization_forward.h:73
#18 0x0000739e55661eed in blink::mojom::LocalFrame_PostMessageEvent_ParamsDataView::ReadMessage<blink::BlinkTransferableMessage> (this=0x7ffe535968f0, output=0x7ffe53596900) at gen/third_party/blink/public/mojom/frame/frame.mojom-params-data.h:6706
#19 0x0000739e555d6d80 in blink::mojom::blink::LocalFrameStubDispatch::Accept (impl=0x18a40048ddb0, message=0x7ffe535976f0) at gen/third_party/blink/public/mojom/frame/frame.mojom-blink.cc:18709
#20 0x0000739e52385856 in blink::mojom::blink::LocalFrameStub<mojo::RawPtrImplRefTraits<blink::mojom::blink::LocalFrame> >::Accept (this=0x18a40048df50, message=0x7ffe535976f0) at gen/third_party/blink/public/mojom/frame/frame.mojom-blink.h:1875
#21 0x0000739eb61ec830 in mojo::InterfaceEndpointClient::HandleValidatedMessage (this=0x31fc008f4d00, message=0x7ffe535976f0) at ../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085
#22 0x0000739eb61ebf54 in mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept (this=0x31fc008f4e40, message=0x7ffe535976f0) at ../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:383
#23 0x0000739eb62053f6 in mojo::MessageDispatcher::Accept (this=0x31fc008f4e50, message=0x7ffe535976f0) at ../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51
#24 0x0000739eb61ee681 in mojo::InterfaceEndpointClient::HandleIncomingMessage (this=0x31fc008f4d00, message=0x7ffe535976f0) at ../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747
#25 0x0000739ead6ac9e7 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread (this=0x31fc00014200, message=..., scoped_urgent_message_notification=...) at ../../ipc/ipc_mojo_bootstrap.cc:1199
#26 0x0000739ead6adbea in base::internal::DecayedFunctorTraits<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>::Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> (method=(void (IPC::ChannelAssociatedGroupController::*)(IPC::ChannelAssociatedGroupController * const, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)) 0x739ead6ac800 <IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)>, receiver_ptr=scoped_refptr((IPC::ChannelAssociatedGroupController *)0x31fc00014200), args=..., args=...) at ../../base/functional/bind_internal.h:740
#27 0x0000739ead6adafb in base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, void, 0ul, 1ul, 2ul>::MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>>(void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>&&) (functor=@0x31fc000d0050: (void (IPC::ChannelAssociatedGroupController::*)(IPC::ChannelAssociatedGroupController * const, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)) 0x739ead6ac800 <IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)>, bound=...) at ../../base/functional/bind_internal.h:932
#28 0x0000739ead6ada5d in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void()>::RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0ul, 1ul, 2ul> (functor=@0x31fc000d0050: (void (IPC::ChannelAssociatedGroupController::*)(IPC::ChannelAssociatedGroupController * const, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)) 0x739ead6ac800 <IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification)>, bound=...) at ../../base/functional/bind_internal.h:1069
#29 0x0000739ead6ad9c9 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void()>::RunOnce (base=0x31fc000d0030) at ../../base/functional/bind_internal.h:982
#30 0x0000739eb5302a0c in base::OnceCallback<void ()>::Run() && (this=0x31fc006b6078) at ../../base/functional/callback.h:155
#31 0x0000739eb550d67e in base::TaskAnnotator::RunTaskImpl (this=0x31fc000942f8, pending_task=From Accept()@ipc/ipc_mojo_bootstrap.cc:0x472 = {...}) at ../../base/task/common/task_annotator.cc:229
#32 0x0000739eb55850c8 in base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_4>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_4&&) (this=0x31fc000942f8, event_name=..., pending_task=From Accept()@ipc/ipc_mojo_bootstrap.cc:0x472 = {...}, args=...) at ../../base/task/common/task_annotator.h:112
#33 0x0000739eb5584b55 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl (this=0x31fc00094000, continuation_lazy_now=0x7ffe53597d60) at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475
#34 0x0000739eb55841ba in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork (this=0x31fc00094000) at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346
#35 0x0000739eb5584d93 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() () from /home/muriarfad/chromium/src/out/debug/libbase.so
#36 0x0000739eb539c7e8 in base::MessagePumpDefault::Run (this=0x31fc00034420, delegate=0x31fc00094120) at ../../base/message_loop/message_pump_default.cc:42
#37 0x0000739eb5585767 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run (this=0x31fc00094000, application_tasks_allowed=0x1, timeout=106751991 days, 4:00:54.775807) at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650
#38 0x0000739eb547a6eb in base::RunLoop::Run (this=0x7ffe53598198, location=RendererMain()@content/renderer/renderer_main.cc:0x16c) at ../../base/run_loop.cc:135
#39 0x0000739eaac90ad3 in content::RendererMain (parameters=...) at ../../content/renderer/renderer_main.cc:364
#40 0x0000739eab13a7a7 in content::RunZygote (delegate=0x7ffe535994c8) at ../../content/app/content_main_runner_impl.cc:664
#41 0x0000739eab13b029 in content::RunOtherNamedProcessTypeMain (process_type=..., main_function_params=..., delegate=0x7ffe535994c8) at ../../content/app/content_main_runner_impl.cc:771
#42 0x0000739eab13c67b in content::ContentMainRunnerImpl::Run (this=0x31f8000b0000) at ../../content/app/content_main_runner_impl.cc:1152
#43 0x0000739eab13862d in content::RunContentProcess (params=..., content_main_runner=0x31f8000b0000) at ../../content/app/content_main.cc:358
#44 0x0000739eab138b36 in content::ContentMain (params=...) at ../../content/app/content_main.cc:371
#45 0x000062128a206600 in ChromeMain (argc=0x8, argv=0x7ffe535996b8) at ../../chrome/app/chrome_main.cc:191
#46 0x000062128a2062b2 in main (argc=0x8, argv=0x7ffe535996b8) at ../../chrome/app/chrome_exe_main_aura.cc:17
#47 0x0000739e33a2a1ca in __libc_start_call_main (main=main@entry=0x62128a206290 <main(int, char const**)>, argc=argc@entry=0x8, argv=argv@entry=0x7ffe535996b8) at ../sysdeps/nptl/libc_start_call_main.h:58
#48 0x0000739e33a2a28b in __libc_start_main_impl (main=0x62128a206290 <main(int, char const**)>, argc=0x8, argv=0x7ffe535996b8, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7ffe535996a8) at ../csu/libc-start.c:360
#49 0x000062128a2061ca in _start ()

```

### aj...@chromium.org (2026-02-24)

[security triage] Hello please do not add attachments as Restricted.

### mu...@gmail.com (2026-02-24)

I apologize, team.

### mu...@gmail.com (2026-02-24)

`muriarfad@hackerenesia:~/chromium/src/tools/get_asan_chrome/chromium-147.0.7695.0-linux-asan$ ./chrome --no-sandbox --enable-logging=stderr --v=1 http://localhost:9090/4.html`

Note the newest asan version:
It cannot direct sigbus. when open the html directly it won't sigbus. it will display black page.
Then to get sigbus, first navigate to root folder. after that open the html page.

```
muriarfad@hackerenesia:~/chromium/src$ cat ~/Documents/log.log | python ./tools/valgrind/asan/asan_symbolize.py 
[59862:59862:0100/000000.399971:ERROR:base/memory/platform_shared_memory_region_posix.cc:214] Creating shared memory in /dev/shm/.org.chromium.Chromium.yl9InC failed: Too many open files (24)
[0225/023758.426214:ERROR:third_party/crashpad/crashpad/util/process/process_memory_linux.cc:50] pread64: Input/output error (5)
Received signal 7 BUS_ADRERR 6d5bad700000
    #0 0x5e8e0df59b86 in ___interceptor_backtrace ??:0:0
    #1 0x5e8e256a16f8 in base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) ./../../base/debug/stack_trace_posix.cc:1048:7
    #2 0x5e8e2565f1a7 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:280:20
    #3 0x5e8e256a0aff in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:483:3
    #4 0x72a650a45330 in __GI___sigaction :?
    #5 0x72a650ba167f in __memcpy_avx512_unaligned_erms ./string/../sysdeps/x86_64/multiarch/memmove-vec-unaligned-erms.S:588:0
    #6 0x5e8e0dfb23f8 in __asan_memmove ??:0:0
    #7 0x5e8e0e7b1fa3 in std::__Cr::pair<base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>> std::__Cr::__copy_move_unwrap_iters<std::__Cr::__copy_backward_impl<std::__Cr::_RangeAlgPolicy>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>, 0>(base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char const>, base::CheckedContiguousIterator<unsigned char>) ./gen/third_party/libc++/src/include/__string/constexpr_c_functions.h:227:5
    #8 0x5e8e0e7b0684 in base::span<unsigned char, 18446744073709551615ul, unsigned char*>::copy_from(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) requires !std::is_const_v<T> ./gen/third_party/libc++/src/include/__algorithm/copy_backward.h:237:10
    #9 0x5e8e3489b73b in mojo::StructTraits<blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents>::Read(blink::mojom::SerializedArrayBufferContentsDataView, blink::ArrayBufferContents*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:173:36
    #10 0x5e8e3489c7e5 in mojo::internal::ArraySerializer<mojo::ArrayDataView<blink::mojom::SerializedArrayBufferContentsDataView>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, mojo::internal::ArrayIterator<mojo::ArrayTraits<blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>>, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>, false>>::DeserializeElements(mojo::internal::Array_Data<mojo::internal::Pointer<blink::mojom::internal::SerializedArrayBufferContents_Data>>*, blink::Vector<blink::ArrayBufferContents, 1u, blink::PartitionAllocator>*, mojo::Message*) ./gen/third_party/blink/public/mojom/array_buffer/array_buffer_contents.mojom-shared.h:86:12
    #11 0x5e8e348990a3 in mojo::StructTraits<blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage>::Read(blink::mojom::TransferableMessageDataView, blink::BlinkTransferableMessage*) ./../../third_party/blink/renderer/core/messaging/blink_transferable_message_mojom_traits.cc:107:13
    #12 0x5e8e1d50da14 in blink::mojom::blink::LocalFrameStubDispatch::Accept(blink::mojom::blink::LocalFrame*, mojo::Message*) ./gen/third_party/blink/public/mojom/messaging/transferable_message.mojom-shared.h:208:12
    #13 0x5e8e25298c0a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #14 0x5e8e252b6944 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:51:24
    #15 0x5e8e2529f0b4 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #16 0x5e8e291926fe in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #17 0x5e8e29194b72 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:740:12
    #18 0x5e8e254d80c7 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/functional/callback.h:155:12
    #19 0x5e8e2554f67a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/common/task_annotator.h:112:5
    #20 0x5e8e2554e4eb in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #21 0x5e8e25398d2a in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #22 0x5e8e25550d88 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #23 0x5e8e25453371 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #24 0x5e8e317e27ff in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:364:16
    #25 0x5e8e211b5210 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:664:14
    #26 0x5e8e211b6551 in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:771:12
    #27 0x5e8e211b9189 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1150:10
    #28 0x5e8e211b2c22 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #29 0x5e8e211b321d in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #30 0x5e8e0dfef25a in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #31 0x72a650a2a1ca in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #32 0x72a650a2a28b in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #33 0x5e8e0df1202a in _start ??:0:0
  r8: 00006d681f0a4000  r9: 0000000c719ec000 r10: 0000000000002400 r11: 0000000000000000
 r12: 00006d5bad6b8000 r13: 000000000008ffbf r14: 0000000000090000 r15: 00006d5bad6b8000
  di: 00006d681f0ec000  si: 00006d5bad700000  bp: 00007ffe02743c30  bx: 00006d681f0a4000
  dx: 0000000000090000  ax: 00006d681f0a4000  cx: 0000000000048000  sp: 00007ffe027433e8
  ip: 000072a650ba167f efl: 0000000000010212 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 00006d5bad700000
[end of stack trace]

```

### mu...@gmail.com (2026-02-26)

Hi, team.

```
1. Ping-pong continues → each round opens new shared memory
2. /dev/shm FD limit reached (error "Too many open files")
3. Shared memory region 0x7b197602b000 mmaped → success (virtual addr available)
4. AVX512 memcpy started:
- src base: 0x7b197602b000 (eg)
- dst base: 0x79c413004000 (eg)
- size: 0x90000 (576KB)
5. Copy successful for the first 294,912 bytes (50%)
6. At offset 0x48000 → page access 0x7b1976073000
7. Kernel: page mapped but backing /dev/shm invalid
(due to "too many open files" → backing truncated/invalid)
8. CPU raise #PF → kernel send SIGBUS BUS_ADRERR
9. Crash in __memcpy_avx512+588

```

Could I ask a question?

copy-after-unmap? copy-after-delete? use-after-unmap? use-after-detach?

### dc...@chromium.org (2026-02-26)

I don't think this is a bug. There's no use-after-X at all here; the address space itself is reserved and other interesting objects aren't going to be mapped into that range. It's just that accessing that range won't ever work and you get a `SIGBUS`.

There are other ways you can get a `SIGBUS` while reading shmem; for example, using `ftruncate()` on the backing file.

But these aren't security bugs because you can't use it to unexpectedly write to some other object or use it to leak information you didn't already have–and `SIGBUS` is fatal. You could try to be really defensive with a `SIGBUS` handler, but that is non-trivial to get correct–people have previously considered doing this (<https://groups.google.com/a/chromium.org/g/chromium-dev/c/_JOoxSpBlj0/m/e4guxp1UBQAJ>) but it's not a complexity tradeoff that we've determined to be worth it.

### mu...@gmail.com (2026-02-26)

Thanks for clarifying.

How about oob read at first sigbus?

On Fri, Feb 27, 2026, 6:17 AM <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/483101823
>
> *Changed*
> status:  Assigned → Intended Behavior
>
> *dc...@chromium.org <dc...@chromium.org> added comment #30
> <https://issues.chromium.org/issues/483101823#comment30>:*
>
> I don't think this is a bug. There's no use-after-X at all here; the
> address space itself is reserved and other interesting objects aren't going
> to be mapped into that range. It's just that accessing that range won't
> ever work and you get a SIGBUS.
>
> There are other ways you can get a SIGBUS while reading shmem; for
> example, using ftruncate() on the backing file.
>
> But these aren't security bugs because you can't use it to unexpectedly
> write to some other object or use it to leak information you didn't already
> have–and SIGBUS is fatal. You could try to be really defensive with a
> SIGBUS handler, but that is non-trivial to get correct–people have
> previously considered doing this (
> https://groups.google.com/a/chromium.org/g/chromium-dev/c/_JOoxSpBlj0/m/e4guxp1UBQAJ)
> but it's not a complexity tradeoff that we've determined to be worth it.
>
> _______________________________
>
> *Reference Info: 483101823 AddressSanitizer: BUS on unknown address*
> component:  Public Trackers > 1362134 > Chromium > Internals > Mojo
> <https://issues.chromium.org/components/1456296>
> status:  Intended Behavior
> reporter:  muriarfad@gmail.com
> assignee:  dc...@chromium.org
> cc:  aj...@chromium.org, an...@chromium.org, el...@chromium.org, and 8
> more
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P1
> severity:  S1
> found in:  144
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, Security_Impact-Extended
> <https://issues.chromium.org/hotlists/5432548>
> retention:  Component default
> Component Ancestor Tags:  Internals, Internals>Mojo
> Component Tags:  Internals>Mojo
> Milestone:  144
> OS:  Android, Fuchsia, Linux, Mac, Windows, ChromeOS
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you have the following role(s) on the
> issue: cc, reporter, starred
> Unsubscribe from this issue
> <https://issues.chromium.org/issues/483101823?unsubscribe=true>.
>


### ch...@google.com (2026-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483101823)*
