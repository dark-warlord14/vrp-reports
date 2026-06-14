# Heap-use-after-free in xmlSwitchEncoding

| Field | Value |
|-------|-------|
| **Issue ID** | [40081535](https://issues.chromium.org/issues/40081535) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>XML |
| **Reporter** | cl...@chromium.org |
| **Assignee** | sc...@chromium.org |
| **Created** | 2015-03-04 |
| **Bounty** | $1,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6428336859906048

Fuzzer: Attekett_surku_fuzzer
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 1
Crash Address: 0x04210004
Crash State:
  asan_check_1_byte_read_access_no_flags
  blink::parseChunk
  blink::XMLDocumentParser::doWrite
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_syzyasan_chrome&range=318869:318962

Minimized Testcase (64.69 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94bw-sWI7dS3WMQFIxCQeHAmAHx8DE5S18iyjCAjKeWzYQ6npCsPlWDSUo0f5lYoptv476yv9BxPJxrglywSKEl4iY43uG0W7Aknk5HAgjglXuvzaieA0RmB_jM2AMzZNls_JvS9u13zLaRxVjOD0dZbcp7vui7H16oyL_5dy5EJuI54ig

Filer: inferno

## Attachments

- [C--clusterfuzz-slave-bot-inputs-fuzzer-testcases-disk-fuzz-224.xml](attachments/C--clusterfuzz-slave-bot-inputs-fuzzer-testcases-disk-fuzz-224.xml) (application/xml, 64.0 KB)
- [0001-Repro-for-bug-748972.patch](attachments/0001-Repro-for-bug-748972.patch) (application/octet-stream, 23.0 KB)

## Timeline

### in...@chromium.org (2015-03-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-04)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5706901866676224

### cl...@chromium.org (2015-03-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-04)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5706901866676224

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x631000028829
Crash State:
  xmlSwitchEncoding
  blink::parseChunk
  blink::XMLDocumentParser::doWrite
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=268656:269696

Minimized Testcase (64.01 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97O0jiRc0_9Z7_1uF7i34qNlg0mCDQ5CTPlKVwaIPRigmeEfk-9b8UtPx7u-8UY_Pgsxa1uPKHZHPIBnImeKQrkS6h4DjvLUGFaDD6Ici8i8avq9ODS9wRvSoTcHAwP2NDPm77fY01CMhP3F2x8XA0vdzt5BfWrCsq0LBdcL_A60qAzQN4



### in...@chromium.org (2015-03-04)

Author: mahesh.kk@samsung.com
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/b67dcce799ba3616321eb94d02e1efcc6b3fb316
Time: Fri May 09 20:32:45 2014
Files DecodedDataDocumentParser.cpp, XMLDocumentParser.cpp are changed in this cl (and is part of stack frame #5, "blink::DecodedDataDocumentParser::updateDocument"; frame #6, "blink::DecodedDataDocumentParser::appendBytes")
Minimum distance from crash line to modified line: 37. (file: DecodedDataDocumentParser.cpp, crashed on: 73, modified: 36).

Author: tkent@chromium.org
Component: blink
Changelist: https://chromium.googlesource.com/chromium/blink.git/+/34dabf9e8e15a0c2150a7ed10b75960c8a58da5d
Time: Sat May 10 04:05:43 2014
File XMLDocumentParser.cpp is changed in this cl (and is part of stack frame #1, "blink::switchEncoding"; frame #2, "blink::parseChunk"; frame #3, "blink::XMLDocumentParser::doWrite"; frame #4, "blink::XMLDocumentParser::append")
Minimum distance from crash line to modified line: 44. (file: XMLDocumentParser.cpp, crashed on: 903, modified: 947).

### in...@chromium.org (2015-03-04)

looks like just a OOB read, lowering severity.

### cl...@chromium.org (2015-03-05)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-03-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-03-18)

ch.dumez@ you reviewed the change. the original dev is not responding. can you please verify and revert the change if needed.

### tk...@chromium.org (2015-03-23)

Both of #5 CLs didn't change the code logic.
This looks a bug of libxml2.


### tk...@chromium.org (2015-03-23)

[Empty comment from Monorail migration]

### tk...@chromium.org (2015-03-23)

Hmm, our usage is wrong according to a comment in xmlSwitchEncoding() of libxml.

        /*The raw input characters are encoded
         *in UTF-16. As we expect this function
         *to be called after xmlCharEncInFunc, we expect


### in...@chromium.org (2015-03-23)

+cc Daniel, libxml maintainer.

Crash stack:
syzyasan_rtl!agent::asan::ErrorInfoGetBadAccessKind+0xf (FPO: [Non-Fpo]) (CONV: cdecl) [e:/b/build/slave/syzygy_official/build/src/syzygy/agent/asan/error_info.cc @ 256]
syzyasan_rtl!agent::asan::ErrorInfoGetBadAccessInformation+0x7e (FPO: [Non-Fpo]) (CONV: cdecl) [e:/b/build/slave/syzygy_official/build/src/syzygy/agent/asan/error_info.cc @ 178]
syzyasan_rtl!agent::asan::AsanRuntime::GetBadAccessInformation+0x5a [e:/b/build/slave/syzygy_official/build/src/syzygy/agent/asan/asan_runtime.cc @ 768]
syzyasan_rtl!agent::asan::ReportBadMemoryAccess+0x1ef (FPO: [Non-Fpo]) (CONV: cdecl) [e:/b/build/slave/syzygy_official/build/src/syzygy/agent/asan/asan_rtl_utils.cc @ 107]
syzyasan_rtl!asan_check_1_byte_read_access_no_flags+0x4c (FPO: [Non-Fpo]) (CONV: cdecl) [e:/b/build/slave/syzygy_official/build/src/syzygy/agent/asan/memory_interceptors.cc @ 279]
blink::parseChunk+0x5f (FPO: [Non-Fpo]) (CONV: cdecl) [third_party/webkit/source/core/xml/parser/xmldocumentparser.cpp @ 575]
blink::XMLDocumentParser::doWrite+0xeb [third_party/webkit/source/core/xml/parser/xmldocumentparser.cpp @ 899]
blink::XMLDocumentParser::append+0x72 [third_party/webkit/source/core/xml/parser/xmldocumentparser.cpp @ 370]
blink::DecodedDataDocumentParser::appendBytes+0x56 [third_party/webkit/source/core/dom/decodeddatadocumentparser.cpp @ 76]
blink::DocumentWriter::addData+0x6f [third_party/webkit/source/core/loader/documentwriter.cpp @ 95]
blink::DocumentLoader::commitData+0x82 [third_party/webkit/source/core/loader/documentloader.cpp @ 513]
blink::DocumentLoader::dataReceived+0x88 [third_party/webkit/source/core/loader/documentloader.cpp @ 541]
blink::RawResource::appendData+0xa3 [third_party/webkit/source/core/fetch/rawresource.cpp @ 48]
blink::ResourceLoader::didReceiveData+0x89 [third_party/webkit/source/core/fetch/resourceloader.cpp @ 433]
content::WebURLLoaderImpl::Context::OnReceivedData+0xe0 [content/child/web_url_loader_impl.cc @ 713]
content::ResourceDispatcher::OnReceivedData+0x2f4 [content/child/resource_dispatcher.cc @ 268]
ResourceMsg_DataReceived::Dispatch<content::ResourceDispatcher,content::ResourceDispatcher,void,void (__thiscall content::ResourceDispatcher::*)(int,int,int,int)>+0x2b (FPO: [Non-Fpo]) (CONV: cdecl) [content/common/resource_messages.h @ 338]
content::ResourceDispatcher::DispatchMessageW+0x19b [content/child/resource_dispatcher.cc @ 512]
content::ResourceDispatcher::OnMessageReceived+0xe2 [content/child/resource_dispatcher.cc @ 117]
base::internal::Invoker<IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall remoting::protocol::ChannelMultiplexer::*)(std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &)>,void __cdecl(remoting::protocol::ChannelMultiplexer *,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &),base::internal::TypeList<base::WeakPtr<remoting::protocol::ChannelMultiplexer>,std::basic_string<char,std::char_traits<char>,std::allocator<char> > > >,base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr<remoting::protocol::ChannelMultiplexer> >,base::internal::UnwrapTraits<std::basic_string<char,std::char_traits<char>,std::allocator<char> > > >,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall remoting::protocol::ChannelMultiplexer::*)(std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &)>,base::internal::TypeList<base::WeakPtr<remoting::protocol::ChannelMultiplexer> const &,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &> >,void __cdecl(void)>::Run+0x47 (FPO: [Non-Fpo]) (CONV: cdecl) [base/bind_internal.h @ 346]
base::debug::TaskAnnotator::RunTask+0x1e9 [base/debug/task_annotator.cc @ 63]
content::TaskQueueManager::ProcessTaskFromWorkQueue+0x170 [content/renderer/scheduler/task_queue_manager.cc @ 515]
content::TaskQueueManager::DoWork+0xe3 [content/renderer/scheduler/task_queue_manager.cc @ 473]
base::internal::Invoker<IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall content::TaskQueueManager::*)(bool)>,void __cdecl(content::TaskQueueManager *,bool),base::internal::TypeList<base::WeakPtr<content::TaskQueueManager>,bool> >,base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr<content::TaskQueueManager> >,base::internal::UnwrapTraits<bool> >,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall content::TaskQueueManager::*)(bool)>,base::internal::TypeList<base::WeakPtr<content::TaskQueueManager> const &,bool const &> >,void __cdecl(void)>::Run+0x3f (FPO: [Non-Fpo]) (CONV: cdecl) [base/bind_internal.h @ 346]
base::debug::TaskAnnotator::RunTask+0x1e9 [base/debug/task_annotator.cc @ 63]
base::MessageLoop::RunTask+0x204 [base/message_loop/message_loop.cc @ 451]
base::MessageLoop::DoWork+0x1b2 [base/message_loop/message_loop.cc @ 571]
base::MessagePumpDefault::Run+0xb7 [base/message_loop/message_pump_default.cc @ 33]
base::MessageLoop::RunHandler+0x30 [base/message_loop/message_loop.cc @ 414]
base::RunLoop::Run+0x58 [base/run_loop.cc @ 56]
base::MessageLoop::Run+0x16 [base/message_loop/message_loop.cc @ 308]
content::RendererMain+0x3ab (FPO: [Non-Fpo]) (CONV: cdecl) [content/renderer/renderer_main.cc @ 221]
content::RunNamedProcessTypeMain+0x101 (FPO: [Non-Fpo]) (CONV: cdecl) [content/app/content_main_runner.cc @ 382]
content::ContentMainRunnerImpl::Run+0xa6 [content/app/content_main_runner.cc @ 768]
content::ContentMain+0x23 (FPO: [Non-Fpo]) (CONV: cdecl) [content/app/content_main.cc @ 19]
ChromeMain+0x6b (FPO: [Non-Fpo]) (CONV: cdecl) [chrome/app/chrome_dllmain.cc @ 69]
chrome+0x7982!unknown
chrome+0x49bf!unknown
chrome!IsSandboxedProcess+0x212b6!unknown
kernel32!BaseThreadInitThunk+0x12!unknown
ntdll!RtlInitializeExceptionChain+0x63!unknown
ntdll!RtlInitializeExceptionChain+0x36!unknown

Free stack:
syzyasan_rtl!agent::asan::WindowsHeapAdapter::HeapReAlloc+0x86 [e:/b/build/slave/syzygy_official/build/src/syzygy/agent/asan/windows_heap_adapter.cc @ 97]
syzyasan_rtl!asan_HeapReAlloc+0x3a [e:/b/build/slave/syzygy_official/build/src/syzygy/agent/asan/asan_rtl_impl.cc @ 114]
realloc+0x43 [f:/dd/vctools/crt/crtw32/heap/realloc.c @ 85]
xmlBufferGrow+0x7f [third_party/libxml/src/tree.c @ 7102]
xmlCharEncInFunc+0x7c [third_party/libxml/src/encoding.c @ 2062]
xmlParserInputBufferPush+0x60 [third_party/libxml/src/xmlio.c @ 3074]
xmlParseChunk+0x182 [third_party/libxml/src/parser.c @ 11735]
blink::parseChunk+0x98 [third_party/webkit/source/core/xml/parser/xmldocumentparser.cpp @ 575]
blink::XMLDocumentParser::doWrite+0xeb [third_party/webkit/source/core/xml/parser/xmldocumentparser.cpp @ 899]
blink::XMLDocumentParser::append+0x72 [third_party/webkit/source/core/xml/parser/xmldocumentparser.cpp @ 370]
blink::DecodedDataDocumentParser::appendBytes+0x56 [third_party/webkit/source/core/dom/decodeddatadocumentparser.cpp @ 76]
blink::DocumentWriter::addData+0x6f [third_party/webkit/source/core/loader/documentwriter.cpp @ 95]
blink::DocumentLoader::commitData+0x82 [third_party/webkit/source/core/loader/documentloader.cpp @ 513]
blink::DocumentLoader::dataReceived+0x88 [third_party/webkit/source/core/loader/documentloader.cpp @ 541]
blink::RawResource::appendData+0xa3 [third_party/webkit/source/core/fetch/rawresource.cpp @ 48]
blink::ResourceLoader::didReceiveData+0x89 [third_party/webkit/source/core/fetch/resourceloader.cpp @ 433]
content::WebURLLoaderImpl::Context::OnReceivedData+0xe0 [content/child/web_url_loader_impl.cc @ 713]
content::ResourceDispatcher::OnReceivedData+0x2f4 [content/child/resource_dispatcher.cc @ 268]
ResourceMsg_DataReceived::Dispatch<content::ResourceDispatcher,content::ResourceDispatcher,void,void (__thiscall content::ResourceDispatcher::*)(int,int,int,int)>+0x2b [content/common/resource_messages.h @ 338]
content::ResourceDispatcher::DispatchMessageW+0x19b [content/child/resource_dispatcher.cc @ 512]
content::ResourceDispatcher::OnMessageReceived+0xe2 [content/child/resource_dispatcher.cc @ 117]
base::internal::Invoker<IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall remoting::protocol::ChannelMultiplexer::*)(std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &)>,void __cdecl(remoting::protocol::ChannelMultiplexer *,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &),base::internal::TypeList<base::WeakPtr<remoting::protocol::ChannelMultiplexer>,std::basic_string<char,std::char_traits<char>,std::allocator<char> > > >,base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr<remoting::protocol::ChannelMultiplexer> >,base::internal::UnwrapTraits<std::basic_string<char,std::char_traits<char>,std::allocator<char> > > >,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall remoting::protocol::ChannelMultiplexer::*)(std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &)>,base::internal::TypeList<base::WeakPtr<remoting::protocol::ChannelMultiplexer> const &,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &> >,void __cdecl(void)>::Run+0x47 [base/bind_internal.h @ 346]
base::debug::TaskAnnotator::RunTask+0x1e9 [base/debug/task_annotator.cc @ 63]
content::TaskQueueManager::ProcessTaskFromWorkQueue+0x170 [content/renderer/scheduler/task_queue_manager.cc @ 515]
content::TaskQueueManager::DoWork+0xe3 [content/renderer/scheduler/task_queue_manager.cc @ 473]
base::internal::Invoker<IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall content::TaskQueueManager::*)(bool)>,void __cdecl(content::TaskQueueManager *,bool),base::internal::TypeList<base::WeakPtr<content::TaskQueueManager>,bool> >,base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr<content::TaskQueueManager> >,base::internal::UnwrapTraits<bool> >,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall content::TaskQueueManager::*)(bool)>,base::internal::TypeList<base::WeakPtr<content::TaskQueueManager> const &,bool const &> >,void __cdecl(void)>::Run+0x3f [base/bind_internal.h @ 346]
base::debug::TaskAnnotator::RunTask+0x1e9 [base/debug/task_annotator.cc @ 63]
base::MessageLoop::RunTask+0x204 [base/message_loop/message_loop.cc @ 451]
base::MessageLoop::DoWork+0x1b2 [base/message_loop/message_loop.cc @ 571]
base::MessagePumpDefault::Run+0xb7 [base/message_loop/message_pump_default.cc @ 33]
base::MessageLoop::RunHandler+0x30 [base/message_loop/message_loop.cc @ 414]
base::MessageLoop::Run+0x16 [base/message_loop/message_loop.cc @ 308]
content::RendererMain+0x3ab [content/renderer/renderer_main.cc @ 221]
content::RunNamedProcessTypeMain+0x101 [content/app/content_main_runner.cc @ 382]
content::ContentMainRunnerImpl::Run+0xa6 [content/app/content_main_runner.cc @ 768]
content::ContentMain+0x23 [content/app/content_main.cc @ 19]
ChromeMain+0x6b [chrome/app/chrome_dllmain.cc @ 69]
chrome+0x7982!unknown
chrome+0x49bf!unknown
chrome!IsSandboxedProcess+0x212b6!unknown
kernel32!BaseThreadInitThunk+0x12!unknown
ntdll!RtlInitializeExceptionChain+0x63!unknown
ntdll!RtlInitializeExceptionChain+0x36!unknown

Allocation stack:
syzyasan_rtl!agent::asan::WindowsHeapAdapter::HeapReAlloc+0x2c [e:/b/build/slave/syzygy_official/build/src/syzygy/agent/asan/windows_heap_adapter.cc @ 89]
syzyasan_rtl!asan_HeapReAlloc+0x3a [e:/b/build/slave/syzygy_official/build/src/syzygy/agent/asan/asan_rtl_impl.cc @ 114]
realloc+0x43 [f:/dd/vctools/crt/crtw32/heap/realloc.c @ 85]
xmlBufferGrow+0x7f [third_party/libxml/src/tree.c @ 7102]
xmlCharEncInFunc+0x7c [third_party/libxml/src/encoding.c @ 2062]
xmlParserInputBufferPush+0x60 [third_party/libxml/src/xmlio.c @ 3074]
xmlParseChunk+0x182 [third_party/libxml/src/parser.c @ 11735]
blink::parseChunk+0x98 [third_party/webkit/source/core/xml/parser/xmldocumentparser.cpp @ 575]
blink::XMLDocumentParser::doWrite+0xeb [third_party/webkit/source/core/xml/parser/xmldocumentparser.cpp @ 899]
blink::XMLDocumentParser::append+0x72 [third_party/webkit/source/core/xml/parser/xmldocumentparser.cpp @ 370]
blink::DecodedDataDocumentParser::appendBytes+0x56 [third_party/webkit/source/core/dom/decodeddatadocumentparser.cpp @ 76]
blink::DocumentWriter::addData+0x6f [third_party/webkit/source/core/loader/documentwriter.cpp @ 95]
blink::DocumentLoader::commitData+0x82 [third_party/webkit/source/core/loader/documentloader.cpp @ 513]
blink::DocumentLoader::dataReceived+0x88 [third_party/webkit/source/core/loader/documentloader.cpp @ 541]
blink::RawResource::appendData+0xa3 [third_party/webkit/source/core/fetch/rawresource.cpp @ 48]
blink::ResourceLoader::didReceiveData+0x89 [third_party/webkit/source/core/fetch/resourceloader.cpp @ 433]
content::WebURLLoaderImpl::Context::OnReceivedData+0xe0 [content/child/web_url_loader_impl.cc @ 713]
content::ResourceDispatcher::OnReceivedData+0x2f4 [content/child/resource_dispatcher.cc @ 268]
ResourceMsg_DataReceived::Dispatch<content::ResourceDispatcher,content::ResourceDispatcher,void,void (__thiscall content::ResourceDispatcher::*)(int,int,int,int)>+0x2b [content/common/resource_messages.h @ 338]
content::ResourceDispatcher::DispatchMessageW+0x19b [content/child/resource_dispatcher.cc @ 512]
content::ResourceDispatcher::OnMessageReceived+0xe2 [content/child/resource_dispatcher.cc @ 117]
base::internal::Invoker<IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall remoting::protocol::ChannelMultiplexer::*)(std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &)>,void __cdecl(remoting::protocol::ChannelMultiplexer *,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &),base::internal::TypeList<base::WeakPtr<remoting::protocol::ChannelMultiplexer>,std::basic_string<char,std::char_traits<char>,std::allocator<char> > > >,base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr<remoting::protocol::ChannelMultiplexer> >,base::internal::UnwrapTraits<std::basic_string<char,std::char_traits<char>,std::allocator<char> > > >,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall remoting::protocol::ChannelMultiplexer::*)(std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &)>,base::internal::TypeList<base::WeakPtr<remoting::protocol::ChannelMultiplexer> const &,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &> >,void __cdecl(void)>::Run+0x47 [base/bind_internal.h @ 346]
base::debug::TaskAnnotator::RunTask+0x1e9 [base/debug/task_annotator.cc @ 63]
content::TaskQueueManager::ProcessTaskFromWorkQueue+0x170 [content/renderer/scheduler/task_queue_manager.cc @ 515]
content::TaskQueueManager::DoWork+0xe3 [content/renderer/scheduler/task_queue_manager.cc @ 473]
base::internal::Invoker<IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall content::TaskQueueManager::*)(bool)>,void __cdecl(content::TaskQueueManager *,bool),base::internal::TypeList<base::WeakPtr<content::TaskQueueManager>,bool> >,base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr<content::TaskQueueManager> >,base::internal::UnwrapTraits<bool> >,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall content::TaskQueueManager::*)(bool)>,base::internal::TypeList<base::WeakPtr<content::TaskQueueManager> const &,bool const &> >,void __cdecl(void)>::Run+0x3f [base/bind_internal.h @ 346]
base::debug::TaskAnnotator::RunTask+0x1e9 [base/debug/task_annotator.cc @ 63]
base::MessageLoop::RunTask+0x204 [base/message_loop/message_loop.cc @ 451]
base::MessageLoop::DoWork+0x1b2 [base/message_loop/message_loop.cc @ 571]
base::MessagePumpDefault::Run+0xb7 [base/message_loop/message_pump_default.cc @ 33]
base::MessageLoop::RunHandler+0x30 [base/message_loop/message_loop.cc @ 414]
base::MessageLoop::Run+0x16 [base/message_loop/message_loop.cc @ 308]
content::RendererMain+0x3ab [content/renderer/renderer_main.cc @ 221]
content::RunNamedProcessTypeMain+0x101 [content/app/content_main_runner.cc @ 382]
content::ContentMainRunnerImpl::Run+0xa6 [content/app/content_main_runner.cc @ 768]
content::ContentMain+0x23 [content/app/content_main.cc @ 19]
ChromeMain+0x6b [chrome/app/chrome_dllmain.cc @ 69]
chrome+0x49bf!unknown
chrome!IsSandboxedProcess+0x212b6!unknown
kernel32!BaseThreadInitThunk+0x12!unknown
ntdll!RtlInitializeExceptionChain+0x63!unknown
ntdll!RtlInitializeExceptionChain+0x36!unknown

You can go to https://code.google.com/p/syzygy/wiki/SyzyASanBug to get more information about how to treat this bug.

### cl...@chromium.org (2015-04-13)

ch.dumez@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### tk...@chromium.org (2015-04-14)

The code was introduced by https://chromium.googlesource.com/chromium/blink/+/d7ab54800174990f3af758df43ead30a3b7f0a87%5E%21/WebCore/dom/XMLDocumentParserLibxml2.cpp .



### in...@chromium.org (2015-04-14)

[Empty comment from Monorail migration]

### ph...@chromium.org (2015-04-27)

Sorry, I don't see how my change from 2010 could have caused a regression now. Also, note that it's just extracting existing code to a function and using that function in one additional place.

I took a look and didn't see anything obvious.

FWIW this can be reproduced on Linux ASAN with above repro case.

### mb...@chromium.org (2015-04-27)

tkent: It seems like you've done the most analysis here. Would you mind taking another look at it or helping to find another owner?

If you don't have time to check for any reason, assign it to me for further triage.

### tk...@chromium.org (2015-04-29)

I can't make time for this until end of May.


### mb...@chromium.org (2015-05-01)

It looks like in some cases after xmlParseChunk runs into an error, ctxt->input->cur is pointing inside of a freed buffer.

Specifically, it's happening in this case:

int
xmlParseChunk(xmlParserCtxtPtr ctxt, const char *chunk, int size,
              int terminate) {
        ...
	res =xmlParserInputBufferPush(ctxt->input->buf, size, chunk);
	if (res < 0) {
	    ctxt->errNo = XML_PARSER_EOF;
	    ctxt->disableSAX = 1;
	    return (XML_PARSER_EOF);
	}
	ctxt->input->base = ctxt->input->buf->buffer->content + base;
	ctxt->input->cur = ctxt->input->base + cur; // We never get here if there was an error, so we're still pointing to junk.

int
xmlParserInputBufferPush(xmlParserInputBufferPtr in,
	                 int len, const char *buf) {
        ...
	nbchars = xmlCharEncInFunc(in->encoder, in->buffer, in->raw); // Calls xmlBufferGrow on in->buffer before it hits the error.
	if (nbchars < 0) {
	    xmlIOErr(XML_IO_ENCODER, NULL);
	    in->error = XML_IO_ENCODER;
	    return(-1);
	}

I don't know enough about this to know the right way to fix this, but I threw https://codereview.chromium.org/1116303004 together to verify that stopping parsing after seeing an error here stops the crash.

tasak: Would you be a good owner for this? If not, do you know anyone that might be able to own it or suggest a proper fix?

### mb...@chromium.org (2015-05-05)

Filed an upstream bug at Daniel's request.

https://bugzilla.gnome.org/show_bug.cgi?id=748972

### ve...@gmail.com (2015-05-07)

First you have no explicit reproducer based just on the software at stake,
then it's a 5 years old forked version with conversion of all C files, then
it's heavilly patched. Tell me why I should go debug this ? How is it gonna
benefit the community of libxml2 users at large ?
Not a proper way to proceed with other open source projects.

First reproduce with a recent version of the code, then try to isolate
a reproducer, thanks !

Daniel

https://bugzilla.gnome.org/show_bug.cgi?id=748972#c3

--------------------------
Current version is 2.9.1, reproduce with something decently recent and
I may take time, otherwise it's just a waste, sorry.
2.7.7 is from Mar 15 2010 more than *five years ago*, get a f...g clue
and update, I don't want to waste time on a forked version from half
a decade ago !
---------------------------

### ti...@google.com (2015-05-08)

To @veillard's point - if we're running a version a five year old version of libxml2 with a lot of backports and customization, it's very much on us to prove that this issue is in a recent version if we want anything upstreamed.

@tasak: considering #20, how do you want to proceed here?

### ve...@gmail.com (2015-05-09)

I don't want to be a pest but since 2.7.7 there have been 14 patches touching just
the encoding.c file, including 3 patches within months of that release about encoding
error fixups, and an "off by one error in encoding" in 2011.
The buffer code has been completely revamped since then too,
  in a nutshell: update the situation is untenable!

I will also point that the version of libxml2 you use is basically what we have in
RHEL-6, that you refuse to support RHEL with Chrome, but on the other hand I should
support you as a free upstream running a snapshot from that time, see the irony and
the unfairness ? Want a supported libxml2 from that area, use the libxml2 I maintain
in RHEL6 :-)

Daniel

### in...@chromium.org (2015-05-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-05-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-05-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-13)

phajdan.jr@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ph...@chromium.org (2015-06-15)

I uploaded https://codereview.chromium.org/1151453002 for review but it fails tests.

I've asked for help in https://goto.google.com/csied but nobody replied.

I think this needs more attention from people actually familiar with XML usage in chromium and blink.

### rs...@chromium.org (2015-06-15)

[Empty comment from Monorail migration]

### ke...@chromium.org (2015-06-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-15)

[Empty comment from Monorail migration]

### es...@chromium.org (2015-06-17)

scottmg, do you think you might be able to help find an owner for this? Thank you!

### sc...@chromium.org (2015-06-17)

Paweł was working on upgrading libxml/libxslt which seems like the right first step. I guess I can try to land that? (I really don't know anything about xml, other than it sucks though, tbh.)

### sc...@chromium.org (2015-06-17)

Wow, this is quite a mess. :(

### bu...@chromium.org (2015-06-18)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=197389

------------------------------------------------------------------
r197389 | scottmg@chromium.org | 2015-06-18T19:43:23.496022Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/LayoutTests/TestExpectations?r1=197389&r2=197388&pathrev=197389

Add expected failures for pending libxml update

Chromium side change at https://codereview.chromium.org/1193533007/.

R=dpranke@chromium.org
BUG=501659,463958

Review URL: https://codereview.chromium.org/1181403003
-----------------------------------------------------------------

### cl...@chromium.org (2015-06-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-06-20)

[Empty comment from Monorail migration]

### ph...@chromium.org (2015-06-23)

FWIW Scott's CL to do the update is https://codereview.chromium.org/1193533007 . Thanks, Scott!

### bu...@chromium.org (2015-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8285ba172641308c6d4775cc38d637ceacb0422a

commit 8285ba172641308c6d4775cc38d637ceacb0422a
Author: scottmg <scottmg@chromium.org>
Date: Tue Jun 23 19:00:06 2015

Upgrade to libxml 2.9.2 and libxslt 1.1.28

The previous version of libxml was released in 2008, so this is a large
jump.

One notable functionality change is that the parser no longer accepts

  <stuff xmlns:stream="a"xmlns="b">

(with no space between the end quote of "a" and the xmlns= attribute).

This seems correct to not accept, but could potentially cause some minor
compatibility differences. This is the change in
xmpp_login_handler_unittest.js.

A second difference is that the column number reported in error
conditions has changed in some cases. This causes some expected-error
LayoutTests to differ in textual output. These seem reasonable and
should hopefully not cause any major compatibility issues.

Blink suppressions at https://codereview.chromium.org/1181403003/ which
need to land first.

BUG=463958,502468

Review URL: https://codereview.chromium.org/1193533007

Cr-Commit-Position: refs/heads/master@{#335721}

[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/remoting/webapp/base/js/xmpp_login_handler_unittest.js
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/BUILD.gn
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/README.chromium
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/build/generate-win32-headers.bat
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/libxml.gyp
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/linux/config.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/linux/include/libxml/xmlversion.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/linux/xml2-config
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/mac/config.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/mac/include/libxml/xmlversion.h
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/patches/LoadLibraryA
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/patches/bug_651202
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/patches/icu
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/patches/icu-configure
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/patches/icu-win32
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/patches/snprintf_config
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/patches/snprintf_win32config
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/patches/win32-clobber-makefile
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/patches/win32-no-posix-error-codes
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/patches/xmlregexp-bogus-cast
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/ChangeLog
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/Copyright
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/DOCBparser.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/HTMLparser.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/HTMLtree.c
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/INSTALL
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/Makefile.am
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/Makefile.tests
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/NEWS
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/README
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/README.tests
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/SAX.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/SAX2.c
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/acconfig.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/acinclude.m4
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/aclocal.m4
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/bakefile/Bakefiles.bkgen
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/bakefile/Readme.txt
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/bakefile/libxml2.bkl
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/buf.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/buf.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/c14n.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/catalog.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/chvalid.c
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/config.guess
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/config.h.in
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/config.sub
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/configure
[rename] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/configure.ac
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/debugXML.c
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/depcomp
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/dict.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/elfgcchack.h
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/enc.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/encoding.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/entities.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/error.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/globals.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/hash.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/Makefile.am
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/DOCBparser.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/HTMLparser.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/HTMLtree.h
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/Makefile.am
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/SAX.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/SAX2.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/c14n.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/catalog.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/debugXML.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/dict.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/encoding.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/entities.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/globals.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/hash.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/list.h
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/nanoftp.h
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/nanohttp.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/parser.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/parserInternals.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/relaxng.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/schemasInternals.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/schematron.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/tree.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/valid.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xlink.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xmlIO.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xmlautomata.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xmlerror.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xmlexports.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xmlmodule.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xmlreader.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xmlsave.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xmlschemas.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xmlschemastypes.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xmlstring.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xmlversion.h.in
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xmlwriter.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xpath.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xpathInternals.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/libxml/xpointer.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/win32config.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/include/wsockcompat.h
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/install-sh
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/legacy.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/libxml-2.0-uninstalled.pc.in
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/libxml-2.0.pc.in
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/libxml.3
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/libxml.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/libxml.spec.in
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/libxml2-config.cmake.in
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/libxml2.spec
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/libxml2.syms
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/list.c
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/ltmain.sh
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/macos/README
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/macos/libxml2.mcp.xml.sit.hqx
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/macos/src/XMLTestPrefix.h
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/macos/src/XMLTestPrefix2.h
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/macos/src/config-mac.h
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/macos/src/libxml2_GUSIConfig.cp
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/macos/src/macos_main.c
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/missing
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/mkinstalldirs
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/nanoftp.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/nanohttp.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/parser.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/parserInternals.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/pattern.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/relaxng.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/runsuite.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/runtest.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/runxmlconf.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/save.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/schematron.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testAutomata.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testC14N.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testHTML.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testModule.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testRegexp.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testRelax.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testSAX.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testSchemas.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testThreads.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testThreadsWin32.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testXPath.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testapi.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testchar.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testdict.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testlimits.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/testrecurse.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/threads.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/timsort.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/tree.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/trio.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/trio.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/triodef.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/trionan.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/trionan.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/triostr.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/uri.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/valid.c
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxml/src/win32/Makefile
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/Makefile.bcb
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/Makefile.mingw
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/Makefile.msvc
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/VC10/README.vc10
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/VC10/RuleSet1.ruleset
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/configure.js
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/libxml2.def.src
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/wince/libxml2.vcb
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/wince/libxml2.vcl
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/wince/libxml2.vco
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/wince/libxml2.vcp
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/wince/libxml2.vcw
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/wince/wincecompat.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/win32/wince/wincecompat.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xinclude.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xlink.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xml2-config.1
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xml2-config.in
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmlIO.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmlcatalog.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmllint.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmlmemory.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmlmodule.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmlreader.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmlregexp.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmlsave.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmlschemas.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmlschemastypes.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmlstring.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmlunicode.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xmlwriter.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xpath.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xpointer.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xstc/Makefile.am
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xstc/xstc.py
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xzlib.c
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/src/xzlib.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/win32/config.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxml/win32/include/libxml/xmlversion.h
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/AUTHORS
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/BUILD.gn
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/ChangeLog
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/FEATURES
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/Makefile.am
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/NEWS
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/OWNERS
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/README
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/README.chromium
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/TODO
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxslt/acconfig.h
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxslt/build/generate-win32-headers.bat
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxslt/compile
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxslt/config.guess
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/config.h.in
[delete] http://crrev.com/dea8f652a25ffa68e366529697caee1a5617cf23/third_party/libxslt/config.sub
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/configure.in
[add] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/libexslt/Makefile.am
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/libexslt/common.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/libexslt/crypto.c
[modify] http://crrev.com/8285ba172641308c6d4775cc38d637ceacb0422a/third_party/libxslt/libexslt/date.c
[modify] http://crrev.com/8

### bu...@chromium.org (2015-06-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/127d99b4c173af397cb46ee089c80630adfb5a14

commit 127d99b4c173af397cb46ee089c80630adfb5a14
Author: scottmg <scottmg@chromium.org>
Date: Wed Jun 24 00:16:12 2015

Update libxml gyp and BUILD.gn, was missing some .h files

This caused the analyze step to be too aggressive in skipping things
which caused https://codereview.chromium.org/1204813002 to land and
break many compiles.

(Case-insensitive sort order preserved to make it clear what changes
in this CL, I'll do a separate no-op that sorts the list properly.)

BUG=463958, 502468, 503747

Review URL: https://codereview.chromium.org/1207543002

Cr-Commit-Position: refs/heads/master@{#335822}

[modify] http://crrev.com/127d99b4c173af397cb46ee089c80630adfb5a14/third_party/libxml/BUILD.gn
[modify] http://crrev.com/127d99b4c173af397cb46ee089c80630adfb5a14/third_party/libxml/libxml.gyp


### sc...@chromium.org (2015-06-25)

I cconfirm that I can reproduce with the original fuzzer test case on syzyasan-r336139 (i.e. after libxml 2.9.2 and libxslt 1.1.28)

### in...@chromium.org (2015-06-25)

Daniel (veillard@) can you please take a look, now that it reproduces on libxml, libxslt trunk.

### sc...@chromium.org (2015-06-25)

(I'm doing a build locally, I don't really know anything about related code, but I'll see if it's something obvious or if there's a simpler repro at least.)

### sc...@chromium.org (2015-06-29)

Some update on this:
- the associated linux repro doesn't repro using -fsanitize=address with xmllint at libxml2 ToT
- Merging these recent semi-related fixes onto 2.9.2
https://git.gnome.org/browse/libxml2/commit/?id=9aa37588ee78a06ca1379a9d9356eab16686099c
https://git.gnome.org/browse/libxml2/commit/?id=709a952110e98621c9b78c4f26462a9d8333102e
does not avoid the UAF in chrome.


### ve...@gmail.com (2015-06-30)

Re #43: how do I reproduce the problem in a standalone way under gdb ?

  thanks,

Daniel

### ve...@gmail.com (2015-06-30)

When I mean standalone, I mean I can crash any C library doing allocation
as part of a rogue program. And considering the complexity of chromium,
the fact you are the only ones ever reporting this, and the fact that IIRC
you don't use the native encoding of the input but convert everything upfront
before handling it to libxml2 (unless things have changed since that was explained
to me years ago, but I doubt it changed).
Also passing the input directly to xmllint doesn't seems to raise the error,
so it's really related to the way chromium uses libxml2.
I'm ready to debug this but I need to be able to run this on gdb/valgrind on my
box, with a libxml2 I compiled, and if possible outside of the full chromium
binary.

  thanks,

Daniel

### sc...@chromium.org (2015-06-30)

Thanks Daniel. Per #45, I'm not sure how to reproduce standalone yet. I agree with your assessment that it seems quite possible that it's Blink's usage.

FWIW, the usage is here https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/xml/parser/XMLDocumentParser.cpp&l=555

### sc...@chromium.org (2015-06-30)

Hi again Daniel,

I attach here a git format-patch with a standalone repro vs. libxml2 ToT.

With the patch applied, I can reproduce with

$ export CFLAGS="-fsanitize=address"
$ ./autogen.sh && make && ./testrepro

I don't really know if Blink is using libxml2 correctly, but hopefully this will let us collectively decide if it's a valid usage or not.

From my naive point of view I think we're hitting this UAF because xmlParseChunk() is careful to early out when

    if (ctxt->instate == XML_PARSER_EOF)
        return(-1);

however, xmlSwitchEncoding() is not.

Around parser.c:12344 when xmlParserInputBufferPush() fails, the error state is set, but the buffer is not updated and so then points to garbage when xmlSwitchEncoding() tries to access ctxt->input->cur.

So, I think the question then, is if it is valid to call xmlSwitchEncoding() after the context is in an error state after xmlParseChunk().


(Let me know if you would prefer this moved to bugzilla, I wasn't sure how concerned the security team would be about posting a repro externally.)

### sc...@chromium.org (2015-06-30)

[[[ er, early out because of

    if ((ctxt->errNo != XML_ERR_OK) && (ctxt->disableSAX == 1))
        return(ctxt->errNo);

but same idea. ]]]

### sc...@chromium.org (2015-06-30)

For security-team: I put a Blink-side patch here: https://codereview.chromium.org/1216783004/

I'm out on vacation for a while after today, so if anyone is concerned that this get fixed in the near term, that would be my suggested fix.

### cl...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-22)

scottmg@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### pd...@chromium.org (2015-07-22)

This needs a new owner as scottmg said he'd be on vacation for some time. He's uploaded a patch, just needs someone to see it through.

@dominicc, would you be up for finding an owner for this?

### do...@chromium.org (2015-07-22)

Sure, let me look at this.

### do...@chromium.org (2015-07-22)

I can work on this first thing next week. I'll try adding a test of some sort to scottmg's patch and pushing it along.

### pd...@chromium.org (2015-07-22)

Thanks dominicc! Removing the nag label.

### cl...@chromium.org (2015-07-24)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5283746868101120

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_media

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x632000000a76
Crash State:
  xmlSwitchEncoding
  blink::parseChunk
  blink::XMLDocumentParser::doWrite
  

Minimized Testcase (96.04 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94xTwJPjLqmnG1srP3koc6Jsvy0bGAgn1dwZfpkl6pXukPkjWQz0iFyYDBcSKVCAKOCiXaauJQB6FF382vg9WhQADQmZKQ5jfS3gbIbkWT0EOZ1p-qWlVFxL9MPlooLp9V216Oh8QZyHzKguOOATTTmTCrjCNTgLnATtA9zvZC0jBAg8Lw

Filer: mbarbella

### do...@chromium.org (2015-07-28)

I am CQing scottmg's splendid patch. I thought about ways to test this, but I think we either end up with a vacuous test that switchEncoding doesn't switch encoding when the XML parser state has an error, or something that just works under ASAN, but reducing these enormous funny ClusterFuzz files by hand is no fun. It's probably more productive to work on a long-term solution to carrying around libxml.

### bu...@chromium.org (2015-07-28)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=199561

------------------------------------------------------------------
r199561 | scottmg@chromium.org | 2015-07-28T05:45:25.123372Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/xml/parser/XMLDocumentParser.cpp?r1=199561&r2=199560&pathrev=199561

Don't call xmlSwitchEncoding when parser is in invalid state

BUG=463958

Review URL: https://codereview.chromium.org/1216783004
-----------------------------------------------------------------

### in...@chromium.org (2015-07-28)

[Empty comment from Monorail migration]

### do...@chromium.org (2015-07-28)

Thanks for that patch scottmg.

### cl...@chromium.org (2015-07-28)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-08-30)

This is already in M46, though let's consider a post-stable merge to M45 if the opportunity presents itself.

### bu...@chromium.org (2015-09-08)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=201920

------------------------------------------------------------------
r201920 | scottmg@chromium.org | 2015-09-08T16:56:56.260463Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/resources/big.xml?r1=201920&r2=201919&pathrev=201920

Landing .xml resource for https://codereview.chromium.org/1316673007/

Resource for https://codereview.chromium.org/1316673007/, landed
separately so that patch can go through CQ (as it won't upload the .xml
because it's too large.)

TBR=dominicc@chromium.org
BUG=528078, 463958

Review URL: https://codereview.chromium.org/1328093005 .
-----------------------------------------------------------------

### bu...@chromium.org (2015-09-09)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=201992

------------------------------------------------------------------
r201992 | scottmg@chromium.org | 2015-09-09T18:55:44.252715Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-big-document-expected.txt?r1=201992&r2=201991&pathrev=201992
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-big-document.html?r1=201992&r2=201991&pathrev=201992
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/xml/parser/XMLDocumentParser.cpp?r1=201992&r2=201991&pathrev=201992
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/xmlhttprequest/resources/big.xml?r1=201992&r2=201991&pathrev=201992

Fix handling of large xml documents

libxml 2.9.0 (we updated from 2.7.x to 2.9.2 for M45) added a
default-on abort on > 10,000,000 byte documents which is a bit
arbitrary and is causing problems for users. The _HUGE option
makes it not do this. My assumption is that this is reasonable
behaviour security-wise as: 1) we were doing it this way until
recently; and 2) it shouldn't be any worse in the renderer than
just doing `for (;;) x+='y';`

(There's a big trivial xml file in
LayoutTests/http/tests/xmlhttprequest/resources/big.xml
that goes with the test, but git cl upload won't upload it. I
guess I'll dcommit just that file first?)

R=dominicc@chromium.org
BUG=528078,463958
TEST=LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-big-document.html

Review URL: https://codereview.chromium.org/1316673007
-----------------------------------------------------------------

### bu...@chromium.org (2015-09-10)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=202063

------------------------------------------------------------------
r202063 | scottmg@chromium.org | 2015-09-10T18:05:43.121719Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/xmlhttprequest/resources/big.xml?r1=202063&r2=202062&pathrev=202063
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-big-document-expected.txt?r1=202063&r2=202062&pathrev=202063
   A http://src.chromium.org/viewvc/blink/branches/chromium/2490/LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-big-document.html?r1=202063&r2=202062&pathrev=202063
   M http://src.chromium.org/viewvc/blink/branches/chromium/2490/Source/core/xml/parser/XMLDocumentParser.cpp?r1=202063&r2=202062&pathrev=202063

Merge 201992 "Fix handling of large xml documents"

> Fix handling of large xml documents
> 
> libxml 2.9.0 (we updated from 2.7.x to 2.9.2 for M45) added a
> default-on abort on > 10,000,000 byte documents which is a bit
> arbitrary and is causing problems for users. The _HUGE option
> makes it not do this. My assumption is that this is reasonable
> behaviour security-wise as: 1) we were doing it this way until
> recently; and 2) it shouldn't be any worse in the renderer than
> just doing `for (;;) x+='y';`
> 
> (There's a big trivial xml file in
> LayoutTests/http/tests/xmlhttprequest/resources/big.xml
> that goes with the test, but git cl upload won't upload it. I
> guess I'll dcommit just that file first?)
> 
> R=dominicc@chromium.org
> BUG=528078,463958
> TEST=LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-big-document.html
> 
> Review URL: https://codereview.chromium.org/1316673007

TBR=scottmg@chromium.org

Review URL: https://codereview.chromium.org/1327253003
-----------------------------------------------------------------

### bu...@chromium.org (2015-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2ef6a940f303d1af0c46f5e4d07cfce8cbe0c9f4

commit 2ef6a940f303d1af0c46f5e4d07cfce8cbe0c9f4
Author: scottmg <scottmg@chromium.org>
Date: Wed Sep 16 19:52:09 2015

Cherry-pick xslt linebreak fix

We're currently using libxslt-1.1.28 which is the most recent tagged
version. Cherry-pick this fix that's not yet released, identified by
git bisect, and confirmed that it fixes the bug in Blink.

Added layout test in Blink to be landed after this lands here:
https://codereview.chromium.org/1344243002

R=thakis@chromium.org
BUG=530587, 463958, 502468

Review URL: https://codereview.chromium.org/1347873002

Cr-Commit-Position: refs/heads/master@{#349196}

[modify] http://crrev.com/2ef6a940f303d1af0c46f5e4d07cfce8cbe0c9f4/third_party/libxslt/README.chromium
[modify] http://crrev.com/2ef6a940f303d1af0c46f5e4d07cfce8cbe0c9f4/third_party/libxslt/libxslt/xslt.c


### bu...@chromium.org (2015-09-16)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=202385

------------------------------------------------------------------
r202385 | scottmg@chromium.org | 2015-09-16T20:59:14.323988Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/xsl/xslt-line-breaks-expected.txt?r1=202385&r2=202384&pathrev=202385
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/xsl/xslt-line-breaks.html?r1=202385&r2=202384&pathrev=202385

Add line break preservation xslt test

Layout test for fix in https://codereview.chromium.org/1347873002.
Without fix, crashes with stack overflow.

(To be landed only after the fix lands above lands.)

BUG=530587, 463958, 502468

Review URL: https://codereview.chromium.org/1344243002
-----------------------------------------------------------------

### bu...@chromium.org (2015-09-17)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=202455

------------------------------------------------------------------
r202455 | scottmg@chromium.org | 2015-09-17T17:09:27.932177Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-big-document-expected.txt?r1=202455&r2=202454&pathrev=202455
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-big-document.html?r1=202455&r2=202454&pathrev=202455
   M http://src.chromium.org/viewvc/blink/branches/chromium/2454/Source/core/xml/parser/XMLDocumentParser.cpp?r1=202455&r2=202454&pathrev=202455
   A http://src.chromium.org/viewvc/blink/branches/chromium/2454/LayoutTests/http/tests/xmlhttprequest/resources/big.xml?r1=202455&r2=202454&pathrev=202455

Merge 201992 "Fix handling of large xml documents"

> Fix handling of large xml documents
> 
> libxml 2.9.0 (we updated from 2.7.x to 2.9.2 for M45) added a
> default-on abort on > 10,000,000 byte documents which is a bit
> arbitrary and is causing problems for users. The _HUGE option
> makes it not do this. My assumption is that this is reasonable
> behaviour security-wise as: 1) we were doing it this way until
> recently; and 2) it shouldn't be any worse in the renderer than
> just doing `for (;;) x+='y';`
> 
> (There's a big trivial xml file in
> LayoutTests/http/tests/xmlhttprequest/resources/big.xml
> that goes with the test, but git cl upload won't upload it. I
> guess I'll dcommit just that file first?)
> 
> R=dominicc@chromium.org
> BUG=528078,463958
> TEST=LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-big-document.html
> 
> Review URL: https://codereview.chromium.org/1316673007

TBR=scottmg@chromium.org

Review URL: https://codereview.chromium.org/1353903002
-----------------------------------------------------------------

### bu...@chromium.org (2015-09-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7365225cea73278300d68b10d17e94d667a9c7f1

commit 7365225cea73278300d68b10d17e94d667a9c7f1
Author: Scott Graham <scottmg@chromium.org>
Date: Thu Sep 17 20:15:27 2015

Cherry-pick xslt linebreak fix

We're currently using libxslt-1.1.28 which is the most recent tagged
version. Cherry-pick this fix that's not yet released, identified by
git bisect, and confirmed that it fixes the bug in Blink.

Added layout test in Blink to be landed after this lands here:
https://codereview.chromium.org/1344243002

R=thakis@chromium.org
BUG=530587, 463958, 502468

Review URL: https://codereview.chromium.org/1347873002

Cr-Commit-Position: refs/heads/master@{#349196}
(cherry picked from commit 2ef6a940f303d1af0c46f5e4d07cfce8cbe0c9f4)

Review URL: https://codereview.chromium.org/1351153002 .

Cr-Commit-Position: refs/branch-heads/2490@{#312}
Cr-Branched-From: 7790a3535f2a81a03685eca31a32cf69ae0c114f-refs/heads/master@{#344925}

[modify] http://crrev.com/7365225cea73278300d68b10d17e94d667a9c7f1/third_party/libxslt/README.chromium
[modify] http://crrev.com/7365225cea73278300d68b10d17e94d667a9c7f1/third_party/libxslt/libxslt/xslt.c


### bu...@chromium.org (2015-09-17)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/7365225cea73278300d68b10d17e94d667a9c7f1

commit 7365225cea73278300d68b10d17e94d667a9c7f1
Author: Scott Graham <scottmg@chromium.org>
Date: Thu Sep 17 20:15:27 2015


### bu...@chromium.org (2015-09-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0cc6bdb67b06017c5757fdb690039137073f4653

commit 0cc6bdb67b06017c5757fdb690039137073f4653
Author: scottmg@chromium.org <scottmg@chromium.org>
Date: Thu Sep 10 18:05:43 2015

Merge 201992 "Fix handling of large xml documents"

> Fix handling of large xml documents
> 
> libxml 2.9.0 (we updated from 2.7.x to 2.9.2 for M45) added a
> default-on abort on > 10,000,000 byte documents which is a bit
> arbitrary and is causing problems for users. The _HUGE option
> makes it not do this. My assumption is that this is reasonable
> behaviour security-wise as: 1) we were doing it this way until
> recently; and 2) it shouldn't be any worse in the renderer than
> just doing `for (;;) x+='y';`
> 
> (There's a big trivial xml file in
> LayoutTests/http/tests/xmlhttprequest/resources/big.xml
> that goes with the test, but git cl upload won't upload it. I
> guess I'll dcommit just that file first?)
> 
> R=dominicc@chromium.org
> BUG=528078,463958
> TEST=LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-big-document.html
> 
> Review URL: https://codereview.chromium.org/1316673007

TBR=scottmg@chromium.org

Review URL: https://codereview.chromium.org/1327253003

git-svn-id: svn://svn.chromium.org/blink/branches/chromium/2490@202063 bbb929c8-8fbe-4397-9dbb-9b2b20218538

[add] http://crrev.com/0cc6bdb67b06017c5757fdb690039137073f4653/third_party/WebKit/LayoutTests/http/tests/xmlhttprequest/resources/big.xml
[add] http://crrev.com/0cc6bdb67b06017c5757fdb690039137073f4653/third_party/WebKit/LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-big-document-expected.txt
[add] http://crrev.com/0cc6bdb67b06017c5757fdb690039137073f4653/third_party/WebKit/LayoutTests/http/tests/xmlhttprequest/xmlhttprequest-big-document.html
[modify] http://crrev.com/0cc6bdb67b06017c5757fdb690039137073f4653/third_party/WebKit/Source/core/xml/parser/XMLDocumentParser.cpp


### bu...@chromium.org (2015-09-24)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/0cc6bdb67b06017c5757fdb690039137073f4653

commit 0cc6bdb67b06017c5757fdb690039137073f4653
Author: scottmg@chromium.org <scottmg@chromium.org>
Date: Thu Sep 10 18:05:43 2015


### ti...@google.com (2015-10-09)

Congrats - $1000 for this report ($500 for the bug + $500 ClusterFuzz bonus).

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### cl...@chromium.org (2015-11-03)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/463958?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/502468]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081535)*
