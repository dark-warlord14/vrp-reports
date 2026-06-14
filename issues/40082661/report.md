# use after free in console.profile calls.

| Field | Value |
|-------|-------|
| **Issue ID** | [40082661](https://issues.chromium.org/issues/40082661) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals, Platform>DevTools |
| **Reporter** | ku...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2010-08-12 |
| **Bounty** | $500.00 |

## Description

chromium 6.0.490.0 (55524)



## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### ku...@gmail.com (2010-08-12)

[Comment Deleted]

### ku...@gmail.com (2010-08-12)

[Comment Deleted]

### ku...@gmail.com (2010-08-12)

[Comment Deleted]

### ku...@gmail.com (2010-08-12)

logout1
=========================

(1c54.3b78): Access violation - code c0000005 (!!! second chance !!!)
eax=0000001c ebx=00000001 ecx=02e98e30 edx=02dfd220 esi=05350155 edi=010ede8c
eip=0000001c esp=001ce464 ebp=001ce488 iopl=0         nv up ei pl nz na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
0000001c ??              ???
0:000> .exr -1
ExceptionAddress: 0000001c
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 0000001c
Attempt to execute non-executable address 0000001c
0:000> kP
ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
001ce460 6bf6fc2f 0x1c
001ce470 6bf71c8a chrome_6b2b0000!v8::internal::SymbolTableCleaner::VisitPointers(
			class v8::internal::Object ** start = 0x00000023, 
			class v8::internal::Object ** end = 0x6c66e938)+0x4f [c:\b\slave\chromium-rel-xp\build\src\v8\src\mark-compact.cc @ 381]
001ce4ac 6bf71cda chrome_6b2b0000!v8::internal::MarkCompactCollector::MarkLiveObjects(void)+0x12a [c:\b\slave\chromium-rel-xp\build\src\v8\src\mark-compact.cc @ 723]
001ce4c0 6befcd0d chrome_6b2b0000!v8::internal::MarkCompactCollector::CollectGarbage(void)+0x1a [c:\b\slave\chromium-rel-xp\build\src\v8\src\mark-compact.cc @ 77]
001ce4cc 6bf00f38 chrome_6b2b0000!v8::internal::Heap::MarkCompact(
			class v8::internal::GCTracer * tracer = 0x00000000)+0x6d [c:\b\slave\chromium-rel-xp\build\src\v8\src\heap.cc @ 734]
001ce4f4 6bf011bf chrome_6b2b0000!v8::internal::Heap::PerformGarbageCollection(
			v8::internal::AllocationSpace space = NEW_SPACE (0), 
			v8::internal::GarbageCollector collector = SCAVENGER (0), 
			class v8::internal::GCTracer * tracer = 0x00000001)+0x108 [c:\b\slave\chromium-rel-xp\build\src\v8\src\heap.cc @ 646]
001ce588 6bf241fb chrome_6b2b0000!v8::internal::Heap::CollectGarbage(
			int requested_size = 46, 
			v8::internal::AllocationSpace space = OLD_POINTER_SPACE (1))+0x5f [c:\b\slave\chromium-rel-xp\build\src\v8\src\heap.cc @ 416]
001ce598 6bf27d00 chrome_6b2b0000!v8::internal::Factory::NewFunctionPrototype(
			class v8::internal::Handle<v8::internal::JSFunction> function = class v8::internal::Handle<v8::internal::JSFunction>)+0x7b [c:\b\slave\chromium-rel-xp\build\src\v8\src\factory.cc @ 251]
001ce5c4 6bf84ee1 chrome_6b2b0000!v8::internal::Factory::CreateApiFunction(
			class v8::internal::Handle<v8::internal::FunctionTemplateInfo> obj = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, 
			v8::internal::Factory::ApiInstanceType instance_type = 1893900 (No matching enumerant))+0x130 [c:\b\slave\chromium-rel-xp\build\src\v8\src\factory.cc @ 848]
001ce5e8 00000000 chrome_6b2b0000!v8::internal::Runtime_CreateApiFunction(
			class v8::internal::Arguments args = class v8::internal::Arguments)+0x51 [c:\b\slave\chromium-rel-xp\build\src\v8\src\runtime.cc @ 729]


### ku...@gmail.com (2010-08-12)

logout 2
===================
(3898.328c): Access violation - code c0000005 (!!! second chance !!!)
eax=6f727027 ebx=02fa903c ecx=6c66966c edx=00000000 esi=6c66966c edi=0025edac
eip=6c2bf02b esp=0025ed7c ebp=00000000 iopl=0         nv up ei pl nz na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
chrome_6b2b0000!WTF::CrossThreadRefCounted<WTF::OwnFastMallocPtr<wchar_t const > >::deref+0xb:
6c2bf02b 8906            mov     dword ptr [esi],eax  ds:002b:6c66966c=6f727028
0:000> .exr -1
ExceptionAddress: 6c2bf02b (chrome_6b2b0000!WTF::CrossThreadRefCounted<WTF::OwnFastMallocPtr<wchar_t const > >::deref+0x0000000b)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 6c66966c
Attempt to write to address 6c66966c
0:000> kP
ChildEBP RetAddr  
0025ed7c 6c373fab chrome_6b2b0000!WTF::CrossThreadRefCounted<WTF::OwnFastMallocPtr<wchar_t const > >::deref(void)+0xb [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\javascriptcore\wtf\crossthreadrefcounted.h @ 126]
0025ed88 6bf44461 chrome_6b2b0000!WebCore::DocumentInternal::getElementByIdCallback(
			class v8::Arguments * args = <Memory access error>)+0x9b [c:\b\slave\chromium-rel-xp\build\src\build\release\obj\global_intermediate\webcore\bindings\v8document.cpp @ 1274]
0025ee80 6bf20638 chrome_6b2b0000!v8::internal::Builtin_FastHandleApiCall(
			class v8::internal::`anonymous-namespace'::BuiltinArguments<0> args = class v8::internal::`anonymous-namespace'::BuiltinArguments<0>)+0xa1 [c:\b\slave\chromium-rel-xp\build\src\v8\src\builtins.cc @ 1055]
0025eec4 6bf20706 chrome_6b2b0000!v8::internal::Invoke(
			bool construct = true, 
			class v8::internal::Handle<v8::internal::JSFunction> func = class v8::internal::Handle<v8::internal::JSFunction>, 
			class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, 
			int argc = 0, 
			class v8::internal::Object *** args = 0x00000000, 
			bool * has_pending_exception = 0x33000000)+0xc8 [c:\b\slave\chromium-rel-xp\build\src\v8\src\execution.cc @ 96]
0025eee8 6beec7a6 chrome_6b2b0000!v8::internal::Execution::Call(
			class v8::internal::Handle<v8::internal::JSFunction> func = class v8::internal::Handle<v8::internal::JSFunction>, 
			class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, 
			int argc = 0, 
			class v8::internal::Object *** args = 0x00000000, 
			bool * pending_exception = 0x00000000)+0x26 

### ku...@gmail.com (2010-08-12)

[Comment Deleted]

### ku...@gmail.com (2010-08-12)

[c:\b\slave\chromium-rel-xp\build\src\v8\src\execution.cc @ 121]
0025ef3c 6bb644c9 chrome_6b2b0000!v8::Script::Run(void)+0x156 [c:\b\slave\chromium-rel-xp\build\src\v8\src\api.cc @ 1255]
0025ef5c 6bb649c9 chrome_6b2b0000!WebCore::V8Proxy::runScript(
			class v8::Handle<v8::Script> script = class v8::Handle<v8::Script>, 
			bool isInlineCode = true)+0x109 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\bindings\v8\v8proxy.cpp @ 457]
0025ef98 6b9ff3dd chrome_6b2b0000!WebCore::V8Proxy::evaluate(
			class WebCore::ScriptSourceCode * source = 0x552f0000, 
			class WebCore::Node * node = 0x00000001)+0x169 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\bindings\v8\v8proxy.cpp @ 408]
0025efd0 6bb5c77c chrome_6b2b0000!WebCore::ScriptController::evaluate(
			class WebCore::ScriptSourceCode * sourceCode = 0x6b2e0001, 
			WebCore::ShouldAllowXSS shouldAllowXSS = AllowXSS (0))+0x10d [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\bindings\v8\scriptcontroller.cpp @ 242]
0025eff0 6bce1f68 chrome_6b2b0000!WebCore::ScriptController::executeScript(
			class WebCore::ScriptSourceCode * sourceCode = 0x0305c014, 
			WebCore::ShouldAllowXSS shouldAllowXSS = AllowXSS (0))+0x8c [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\bindings\scriptcontrollerbase.cpp @ 62]
0025f00c 6bce2713 chrome_6b2b0000!WebCore::HTMLScriptRunner::executeScript(
			class WebCore::Element * element = 0x0000170a, 
			class WebCore::ScriptSourceCode * sourceCode = 0x0305c014)+0x48 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\html\htmlscriptrunner.cpp @ 160]
0025f10c 6bce2784 chrome_6b2b0000!WebCore::HTMLScriptRunner::runScript(
			class WebCore::Element * script = 0x0000170a, 
			int startingLineNumber = 50708500)+0x133 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\html\htmlscriptrunner.cpp @ 277]
0025f11c 6bc66c10 chrome_6b2b0000!WebCore::HTMLScriptRunner::execute(
			class WTF::PassRefPtr<WebCore::Element> scriptElement = class WTF::PassRefPtr<WebCore::Element>, 
			int startLine = 0)+0x14 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\html\htmlscriptrunner.cpp @ 187]
0025f138 6bc672e6 chrome_6b2b0000!WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder(void)+0x90 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\html\htmldocumentparser.cpp @ 154]
0025f180 6bc676e6 chrome_6b2b0000!WebCore::HTMLDocumentParser::pumpTokenizer(
			WebCore::HTMLDocumentParser::SynchronousMode mode = AllowYield (0))+0xf6 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\html\htmldocumentparser.cpp @ 181]
0025f18c 6bc668b0 chrome_6b2b0000!WebCore::HTMLDocumentParser::append(
			class WebCore::SegmentedString * source = 0x00000001)+0x76 


### ku...@gmail.com (2010-08-12)

[c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\html\htmldocumentparser.cpp @ 259]
0025f1d4 6bb52d61 chrome_6b2b0000!WebCore::DecodedDataDocumentParser::appendBytes(
			class WebCore::DocumentWriter * writer = 0x00000001, 
			char * data = 0x058d3b10 "???", 
			int length = 0, 
			bool shouldFlush = true)+0xb0 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\dom\decodeddatadocumentparser.cpp @ 55]
0025f1f4 6b9f4a37 chrome_6b2b0000!WebCore::DocumentWriter::addData(
			char * str = 0x3e747069 "--- memory read error at address 0x3e747069 ---", 
			int len = 1635125773, 
			bool flush = true)+0x41 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\loader\documentwriter.cpp @ 200]
0025f204 6bd0edf3 chrome_6b2b0000!WebCore::FrameLoader::addData(
			char * bytes = 0x3e747069 "--- memory read error at address 0x3e747069 ---", 
			int length = 1635125773)+0x17 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\loader\frameloader.cpp @ 1152]
0025f220 6bd31206 chrome_6b2b0000!WebKit::WebFrameImpl::commitDocumentData(
			char * data = 0x3e747069 "--- memory read error at address 0x3e747069 ---", 
			unsigned int dataLen = 0x61760a0d)+0xa3 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webkit\chromium\src\webframeimpl.cpp @ 1022]

### ku...@gmail.com (2010-08-12)

[Comment Deleted]

### ku...@gmail.com (2010-08-12)

"Attempt to execute non-executable address 0000001c" 
's frequency is higher than
"Attempt to write to address 6c66966c" 

"Attempt to write to address 6c66966c" come out only once.

### ku...@gmail.com (2010-08-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-13)

can anyone from devtools team take a look at it. note that you need to run the repro for around 10-15 min and put it on a website (not run locally).

### in...@chromium.org (2010-08-13)

[Empty comment from Monorail migration]

### pf...@chromium.org (2010-08-13)

[Empty comment from Monorail migration]

### pf...@chromium.org (2010-08-13)

[Empty comment from Monorail migration]

### yu...@chromium.org (2010-08-16)

Should DevTools window be open or the browser just needs to be neavgated to the index.html?

### ku...@gmail.com (2010-08-16)

the browser just needs to be neavgated to the index.html

### js...@chromium.org (2010-08-16)

yurys@ - Just open the file, but it's not a clean repro and we're currently at a loss to determine the cause. So, you may need to leave it running for a while. (In some cases it took more than 10 minutes before it hit the memory corruption.)

### yu...@chromium.org (2010-08-17)

Might be a profiler issue, adding mnaganov to cc list.

### mn...@chromium.org (2010-08-17)

Just checked: I've removed all 'window.console.profile' invocations, and still got a crash.

### ku...@gmail.com (2010-08-18)

[Comment Deleted]

### ku...@gmail.com (2010-08-18)

output
===============
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
chrome_68010000!v8::internal::Top::CaptureCurrentStackTrace+0x1b6:
68c9ccc6 8b6b27          mov     ebp,dword ptr [ebx+27h] ds:002b:02ad9820=????????
0:000> .exr -1
ExceptionAddress: 68c9ccc6 (chrome_68010000!v8::internal::Top::CaptureCurrentStackTrace+0x000001b6)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 02ad9820
Attempt to read from address 02ad9820
0:000> kP
ChildEBP RetAddr  
004ce960 68c6c9b0 chrome_68010000!v8::internal::Top::CaptureCurrentStackTrace(
			int frame_limit = <Memory access error>, 
			v8::StackTrace::StackTraceOptions options = <Memory access error>)+0x1b6 [c:\b\slave\chromium-rel-xp\build\src\v8\src\top.cc @ 402]
004ce988 688e1fdd chrome_68010000!v8::StackTrace::CurrentStackTrace(
			int frame_limit = <Memory access error>, 
			v8::StackTrace::StackTraceOptions options = <Memory access error>)+0x60 [c:\b\slave\chromium-rel-xp\build\src\v8\src\api.cc @ 1614]
004ce9d8 690de06b chrome_68010000!WebCore::ScriptCallStack::create(
			class v8::Arguments * arguments = <Memory access error>, 
			unsigned int skipArgumentCount = <Memory access error>, 
			int framCountLimit = <Memory access error>)+0x3d [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\bindings\v8\scriptcallstack.cpp @ 94]
004ce9f8 68cc2ef7 chrome_68010000!WebCore::ConsoleInternal::dirxmlCallback(
			class v8::Arguments * args = 0x60003500)+0x4b [c:\b\slave\chromium-rel-xp\build\src\build\release\obj\global_intermediate\webcore\bindings\v8console.cpp @ 61]
004cea54 68cc31ff chrome_68010000!v8::internal::HandleApiCallHelper<0>(
			class v8::internal::`anonymous-namespace'::BuiltinArguments<1> args = class v8::internal::`anonymous-namespace'::BuiltinArguments<1>)+0x167 [c:\b\slave\chromium-rel-xp\build\src\v8\src\builtins.cc @ 972]
004ceb40 68ca2ac5 chrome_68010000!v8::internal::Builtin_HandleApiCall(
			class v8::internal::`anonymous-namespace'::BuiltinArguments<1> args = class v8::internal::`anonymous-namespace'::BuiltinArguments<1>)+0xf [c:\b\slave\chromium-rel-xp\build\src\v8\src\builtins.cc @ 989]

### ku...@gmail.com (2010-08-18)


004ceb84 68ca2b96 chrome_68010000!v8::internal::Invoke(
			bool construct = true, 
			class v8::internal::Handle<v8::internal::JSFunction> func = class v8::internal::Handle<v8::internal::JSFunction>, 
			class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, 
			int argc = 3473485, 
			class v8::internal::Object *** args = 0x0035004d, 
			bool * has_pending_exception = 0x02a18fed)+0xc5 [c:\b\slave\chromium-rel-xp\build\src\v8\src\execution.cc @ 96]
004ceba8 68c70756 chrome_68010000!v8::internal::Execution::Call(
			class v8::internal::Handle<v8::internal::JSFunction> func = class v8::internal::Handle<v8::internal::JSFunction>, 
			class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, 
			int argc = 0, 
			class v8::internal::Object *** args = 0x00000000, 
			bool * pending_exception = 0x00000000)+0x26 [c:\b\slave\chromium-rel-xp\build\src\v8\src\execution.cc @ 121]
004cebfc 688e04dd chrome_68010000!v8::Script::Run(void)+0x156 [c:\b\slave\chromium-rel-xp\build\src\v8\src\api.cc @ 1257]
004cec1c 688e09e9 chrome_68010000!WebCore::V8Proxy::runScript(
			class v8::Handle<v8::Script> script = class v8::Handle<v8::Script>, 
			bool isInlineCode = true)+0x10d [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\bindings\v8\v8proxy.cpp @ 457]
004cec58 68778c6d chrome_68010000!WebCore::V8Proxy::evaluate(
			class WebCore::ScriptSourceCode * source = 0x056a0000, 
			class WebCore::Node * node = 0x00000001)+0x169 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\bindings\v8\v8proxy.cpp @ 408]
004cec90 688d87cc chrome_68010000!WebCore::ScriptController::evaluate(
			class WebCore::ScriptSourceCode * sourceCode = 0x68040001, 
			WebCore::ShouldAllowXSS shouldAllowXSS = AllowXSS (0))+0x10d [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\bindings\v8\scriptcontroller.cpp @ 249]
004cecb0 68a5bea8 chrome_68010000!WebCore::ScriptController::executeScript(
			class WebCore::ScriptSourceCode * sourceCode = 0x0059b014, 
			WebCore::ShouldAllowXSS shouldAllowXSS = AllowXSS (0))+0x8c [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\bindings\scriptcontrollerbase.cpp @ 62]
004ceccc 68a5c4de chrome_68010000!WebCore::HTMLScriptRunner::executeScript(
			class WebCore::Element * element = 0x00000238, 
			class WebCore::ScriptSourceCode * sourceCode = 0x0059b014)+0x48 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\html\htmlscriptrunner.cpp @ 162]
004cedcc 68a5c6b4 chrome_68010000!WebCore::HTMLScriptRunner::runScript(
			class WebCore::Element * script = 0x00000238, 
			int startingLineNumber = 5877780)+0x12e 

### ku...@gmail.com (2010-08-18)

[c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\html\htmlscriptrunner.cpp @ 291]
004ceddc 689e08e0 chrome_68010000!WebCore::HTMLScriptRunner::execute(
			class WTF::PassRefPtr<WebCore::Element> scriptElement = class WTF::PassRefPtr<WebCore::Element>, 
			int startLine = 0)+0x14 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\html\htmlscriptrunner.cpp @ 189]
004cedf8 689e0eb3 chrome_68010000!WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder(void)+0x90 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\html\htmldocumentparser.cpp @ 177]
004cee58 689e12b6 chrome_68010000!WebCore::HTMLDocumentParser::pumpTokenizer(
			WebCore::HTMLDocumentParser::SynchronousMode mode = AllowYield (0))+0x103 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\html\htmldocumentparser.cpp @ 204]
004cee64 689dfe90 chrome_68010000!WebCore::HTMLDocumentParser::append(
			class WebCore::SegmentedString * source = 0x00001101)+0x76 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\html\htmldocumentparser.cpp @ 282]
004ceeb0 688cf6e4 chrome_68010000!WebCore::DecodedDataDocumentParser::appendBytes(
			class WebCore::DocumentWriter * writer = 0x00001101, 
			char * data = 0x056a10f0 "???", 
			int length = 4352, 
			bool shouldFlush = false)+0xb0 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\dom\decodeddatadocumentparser.cpp @ 55]


### ku...@gmail.com (2010-08-18)

(167c.16b0): Access violation - code c0000005 (!!! second chance !!!)
eax=005cf084 ebx=02ad97f9 ecx=005cf074 edx=00000037 esi=00000000 edi=00000008
eip=68c9ccc6 esp=004ce84c ebp=00000000 iopl=0         nv up ei pl zr na pe nc
Sorry for paste so many my intranet does't allow upload files

### ku...@gmail.com (2010-08-18)

[Comment Deleted]

### ku...@gmail.com (2010-08-18)

[Comment Deleted]

### in...@chromium.org (2010-08-26)

@kuzzcc, can you please help to reduce to a simple testscase that triggers more reliably and quickly. this can increase the likelyhood of a security reward.

### ku...@gmail.com (2010-08-27)

No longer crash chromium 7.0.507.0 (57625) :D

### [Deleted User] (2010-08-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-27)

@kuzcc, it still reproduces on trunk 7.0.506.0 (57453), 7.0.507.0 (57639). it is definitely bad because it crashes in tcmalloc free.

@pfeldman, did you get a chance to take a look.

>tcmalloc::SLL_Next(void * t=0x00000003)  Line 42 + 0x3 bytes
 tcmalloc::SLL_Pop(void * * list=0x00261b80)  Line 56 + 0xb bytes
 tcmalloc::ThreadCache::FreeList::Pop()  Line 200 + 0x9 bytes
 tcmalloc::ThreadCache::Allocate(unsigned int size=16, unsigned int cl=2)  Line 350
 `anonymous namespace'::do_malloc(unsigned int size=16)  Line 985 + 0x10 bytes
 malloc(unsigned int size=12)  Line 110 + 0x9 bytes
 generic_cpp_alloc(unsigned int size=12, bool nothrow=false)  Line 16 + 0x9 bytes
 operator new(unsigned int size=12)  Line 28 + 0xb bytes
 std::_Allocate<std::_List_nod<net::HttpCache::WorkItem *,std::allocator<net::HttpCache::WorkItem *> >::_Node>(unsigned int _Count=1, std::_List_nod<net::HttpCache::WorkItem *,std::allocator<net::HttpCache::WorkItem *> >::_Node * __formal=0x00000000)  Line 43 + 0xc bytes
 std::allocator<std::_List_nod<net::HttpCache::WorkItem *,std::allocator<net::HttpCache::WorkItem *> >::_Node>::allocate(unsigned int _Count=1)  Line 145 + 0xb bytes
 std::list<net::HttpCache::WorkItem *,std::allocator<net::HttpCache::WorkItem *> >::_Buynode()  Line 1172 + 0xd bytes
 std::list<net::HttpCache::WorkItem *,std::allocator<net::HttpCache::WorkItem *> >::list<net::HttpCache::WorkItem *,std::allocator<net::HttpCache::WorkItem *> >()  Line 436 + 0x2f bytes
 net::HttpCache::OnIOComplete(int result=0, net::HttpCache::PendingOp * pending_op=0x05ed4660)  Line 972
 net::HttpCache::BackendCallback::RunWithParams(const Tuple1<int> & params={...})  Line 149
 CallbackRunner<Tuple1<int> >::Run<int>(const int & a=0)  Line 84 + 0x1c bytes
 disk_cache::InFlightBackendIO::OnOperationComplete(disk_cache::BackgroundIO * operation=0x05c392c0, bool cancel=false)  Line 428
 disk_cache::InFlightIO::InvokeCallback(disk_cache::BackgroundIO * operation=0x05c392c0, bool cancel_task=false)  Line 64 + 0x18 bytes
 disk_cache::BackgroundIO::OnIOSignalled()  Line 15
 DispatchToMethod<disk_cache::BackgroundIO,void (__thiscall disk_cache::BackgroundIO::*)(void)>(disk_cache::BackgroundIO * obj=0x05c392c0, void (void)* method=0x52189df0, const Tuple0 & arg={...})  Line 537 + 0xb bytes
 RunnableMethod<disk_cache::BackgroundIO,void (__thiscall disk_cache::BackgroundIO::*)(void),Tuple0>::Run()  Line 327 + 0x1e bytes
 MessageLoop::RunTask(Task * task=0x05ed4ab0)  Line 408 + 0xf bytes
 MessageLoop::DeferOrRunPendingTask(const MessageLoop::PendingTask & pending_task={...})  Line 420
 MessageLoop::DoWork()  Line 524 + 0xc bytes
 base::MessagePumpForIO::DoRunLoop()  Line 442 + 0x19 bytes
 base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate=0x0486fc20, base::MessagePumpWin::Dispatcher * dispatcher=0x00000000)  Line 51 + 0xf bytes
 base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate=0x0486fc20)  Line 80 + 0x1c bytes
 MessageLoop::RunInternal()  Line 256 + 0x2a bytes
 MessageLoop::RunHandler()  Line 229
 MessageLoop::Run()  Line 207
 base::Thread::Run(MessageLoop * message_loop=0x0486fc20)  Line 141
 base::Thread::ThreadMain()  Line 164 + 0x16 bytes
 `anonymous namespace'::ThreadFunc(void * closure=0x00c6f600)  Line 26 + 0xf bytes
 	kernel32.dll!@BaseThreadInitThunk@12()  + 0xe bytes	
 	ntdll.dll!___RtlUserThreadStart@8()  + 0x23 bytes	
 	ntdll.dll!__RtlUserThreadStart@8()  + 0x1b bytes	


### ku...@gmail.com (2010-08-28)

I only got if remove console.profile it no longer crash me 

### in...@chromium.org (2010-08-30)

@pfeldman, @mnaganov : Here is the smallest reproducer i could get that crashes with same tcmalloc stacktrace [have no idea of how code works which can possibly reduce it even more] ::. Can you please take a look. Please give it like 10-15min for the crash to happen. Verified on chromium 7.0.509.0 (57813) on windows.
can try internal link - www/~aarya/no_crawl/index.htm

-----console.htm----
<script>
window.console.profile(document.createElement("td"),eval,null,null);
window.console.profile(1000000000,window.console.time);
window.console.profile(null,null,1000000000);
</script>
------index.htm-----
<META HTTP-EQUIV="refresh" CONTENT="0;url=index.htm">
<iframe src="console.htm"></iframe>

### mn...@chromium.org (2010-08-30)

Thanks for reducing the test case.

Is this really an M6 bug? I don't think we'll be in time to merge the fix.

### ku...@gmail.com (2010-08-30)

Crash Google Chrome 6.0.472.51 (Official Build 57639) too

### js...@chromium.org (2010-08-30)

Security issues are handled differently than other bugs. Their priority is normally higher (based on severity), and the fixes can get merged over the life of a branch. Since this is an externally reported high severity bug, we target the fix for the current stable branch.


### in...@chromium.org (2010-08-30)

Mikhail, the first v6 security patch should be out in roughly 2 weeks timeframe. We should aim for the fix in that timeframe if possible. Sorry for bugging yu, it wouldn't be that important if it was not a secseverity high.

### mn...@chromium.org (2010-08-31)

Yes, I understand the importance of this bug and working on it.

### mn...@chromium.org (2010-08-31)

An update on this issue:

What I found is that the first two calls to 'window.console.profile' are basically ignored for all times except the first page load because they are trying to start a profile with a name that already exists. While the third call starts a new profile every time. And since the number of simultaneously collected profiles is unbounded in V8, this may lead to heap exhaustion.

Since allowing unlimited number of simultaneously collected profiles is anyway bad, I fixed it in V8. I will merge a patch into Chrome 6 V8 branch.

### in...@chromium.org (2010-08-31)

Thank you very much Mikhail. Quick question - in the stacktrace, we were seeing memory corruption. So, if the problem was only heap exhaustion, then we should instead see like null ptr or int 3 crashes. Also, heap exhaustion would be a Denial of service and not a security bug per se. 

### mn...@chromium.org (2010-08-31)

Yes, the issue I found isn't the root cause of crash, but it also worth fixing. Currently I'm trying to spot the heap corruption by using available heap checking tools.

I already examined profiling in a standalone V8 using valgrind, and so far have found only one small bug related to uninitialized values, which I fixed too.

Working with Chrome is much harder because of its size, and the nature of the bug. E.g. I'm not sure, for how long should I run it under valgrind to get the crash. I will also try attacking the problem with debug implementations of malloc on Linux and OS X.

Hints and advices of how to deal with this issue are much appreciated.

### js...@chromium.org (2010-08-31)

Yeah, these kinds of memory corruption bugs are the hardest to track down, because with normal testing the crash is nowhere near the actual bug. It sounds like you're already doing exactly what I would do, but I would probably start by testing with the debug allocators.

### mn...@chromium.org (2010-09-01)

OK, thanks to libgmalloc on OS X, I found a memory overrun that can occur in profiling, and fixed it. I've merged it into V8's 2.2 branch (at r5393) -- the one used for Cr M6.

With this patch in place I can no longer reproduce the crash for the whole day.

Soeren from V8 team sent a mail to Jason Kersey and Anthony LaForge.

### js...@chromium.org (2010-09-01)

@mnaganov - Thanks, and great work. I'll also talk to @laforge and @kerz about merging this to v6.

### in...@chromium.org (2010-09-01)

Awesome turnaround time Mikhail, we could probably get this in 1st v6 patch :)

### sc...@gmail.com (2010-09-01)

@mnaganov: do you have a link to the specific change that fixed the overrun? I'm curious to take a look :)

### sc...@gmail.com (2010-09-02)

http://code.google.com/p/v8/source/detail?r=5393
(Oops - public mention of "memory overrun" :)

### sc...@gmail.com (2010-09-08)

Thank you again kuzzcc and congratulations! This bug report has provisionally qualified for a $500 Chromium Security Reward.
We were able to eventually discern a race condition based on the test case.

### in...@chromium.org (2010-09-08)

Mikhail, can you please confirm if the V8 change is merged to 472 branch so that it can come up in 1st v6 patch. If yes, please mark bug in status FixUnreleased.

### mn...@chromium.org (2010-09-08)

It looks like not.

As I see in 472's DEPS (http://src.chromium.org/viewvc/chrome/branches/472/src/DEPS?view=markup)
references V8 r5091:

  "src/v8":
    "http://v8.googlecode.com/svn/trunk@5091",

While my patch was merged into V8's 2.2 branch (for Cr6) as r5393: http://code.google.com/p/v8/source/detail?r=5393

### in...@chromium.org (2010-09-08)

Mark, can you please update the v8 deps for 472 and trigger the code update.

### sc...@gmail.com (2010-09-08)

Assigning to mal@ :)

### sc...@gmail.com (2010-09-09)

Allegedly, since this is v8, the DEPS file will be auto-generated on the next build, and will pick up the latest on the v2.2 branch automagically.

Leaving WillMerge as we want to verify by looking at the generated DEPS file for the candidate build.

### sc...@gmail.com (2010-09-10)

Mark confirmed that the in-progress build is picking up http://v8.googlecode.com/svn/branches/2.2@5393

### sc...@gmail.com (2010-09-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-09-22)

Payment is in the electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2011-07-27)

Patch works. Don't crash in Google Chrome 12.0.742.122.

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/51919?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals, Platform>DevTools]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082661)*
