# Security: heap-buffer-overflow in CFXJSE_FormCalcContext::unfoldArgs

| Field | Value |
|-------|-------|
| **Issue ID** | [40050123](https://issues.chromium.org/issues/40050123) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ba...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-09-15 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

The bug present in CFXJSE\_FormCalcContext::unfoldArgs function in fxjs/xfa/cfxjse\_formcalc\_context.cpp file.  

PDFium supports not only javascript but also FormCalc script when XFA is enabled and content type is set to 'application/x-formcalc'.  

Interestingly, PDFium executes FormCalc script by converting FormCalc script to javascript, with custom global javascript object named 'pfm\_rt'.  

All FormCalc script which includes methods, operators(assignment, dot, ...etc) is converted to javascript.  

For example, assignment operator in FormCalc is translated to javascript code which calls assignment method of 'pfm\_rt' object.

The translation from FormCalc to javascript is processed by CFXJSE\_FormCalcContext::Translate function, in fxjs/xfa/cfxjse\_formcalc\_context.cpp file, which is called from CFXJSE\_Engine::RunScript function in fxjs/xfa/cfxjse\_engine.cpp.

bool CFXJSE\_Engine::RunScript(CXFA\_Script::Type eScriptType,  

WideStringView wsScript,  

CFXJSE\_Value\* hRetValue,  

CXFA\_Object\* pThisObject) {  

ByteString btScript;  

AutoRestorer<CXFA\_Script::Type> typeRestorer(&m\_eScriptType);  

m\_eScriptType = eScriptType;  

if (eScriptType == CXFA\_Script::Type::Formcalc) { // (Point 1)  

if (!m\_FM2JSContext) {  

m\_FM2JSContext = pdfium::MakeUnique<CFXJSE\_FormCalcContext>(  

GetIsolate(), m\_JsContext.get(), m\_pDocument.Get());  

}  

CFX\_WideTextBuf wsJavaScript;  

if (!CFXJSE\_FormCalcContext::Translate(wsScript, &wsJavaScript)) { // (Point 2)  

hRetValue->SetUndefined();  

return false;  

}  

btScript = FX\_UTF8Encode(wsJavaScript.AsStringView());  

} else {  

btScript = FX\_UTF8Encode(wsScript);  

}  

AutoRestorer<UnownedPtr<CXFA\_Object>> nodeRestorer(&m\_pThisObject);  

m\_pThisObject = pThisObject;

CFXJSE\_Value\* pValue =  

pThisObject ? GetOrCreateJSBindingFromMap(pThisObject) : nullptr;  

IJS\_Runtime::ScopedEventContext ctx(m\_pSubordinateRuntime.Get());  

return m\_JsContext->ExecuteScript(btScript.c\_str(), hRetValue, pValue); // (Point 3)  

}

CFXJSE\_Engine::RunScript function is used to exectue both FormCalc script and javascript. The only difference between FormCalc script and javascript is whether translation is performed or not.  

At (Point 1), checks the type of script. At (Point 2), Translation from FormCalc to javascript is performed if FormCalc script is given.  

AT (Point 3), executes (converted) javascript.

The translated javascript uses 'pfm\_rt' global object to perform FormCalc operations. The 'pfm\_rt' global object is available once FormCalc script type is given.  

The global property getter function, CFXJSE\_Engine::GlobalPropertyGetter in cfxjse\_engine.cpp, will return valid 'pfm\_rt' object if type of script is FormCalc.

const char kFormCalcRuntime[] = "pfm\_rt";  

void CFXJSE\_Engine::GlobalPropertyGetter(CFXJSE\_Value\* pObject,  

ByteStringView szPropName,  

CFXJSE\_Value\* pValue) {  

CXFA\_Object\* pOriginalObject = ToObject(pObject);  

CXFA\_Document\* pDoc = pOriginalObject->GetDocument();  

CFXJSE\_Engine\* lpScriptContext = pDoc->GetScriptContext();  

WideString wsPropName = WideString::FromUTF8(szPropName);

pValue->SetUndefined(); // Assume failure.  

if (lpScriptContext->GetType() == CXFA\_Script::Type::Formcalc) { // (Point 4) Check the type of script  

if (szPropName == kFormCalcRuntime) { //  

lpScriptContext->m\_FM2JSContext->GlobalPropertyGetter(pValue); // (Point 5) if type is FormCalc and target property is 'pfm\_rt', use special formcalc context.  

return;  

}  

...

(Exported) methods and properties of 'pfm\_rt' is implmeneted in 'fxjs/xfa/cfxjse\_formcalc\_context.cpp' source file.

const FXJSE\_FUNCTION\_DESCRIPTOR kFormCalcFM2JSFunctions[] = {  

{kFuncTag, "Abs", CFXJSE\_FormCalcContext::Abs},  

{kFuncTag, "Avg", CFXJSE\_FormCalcContext::Avg},  

{kFuncTag, "Ceil", CFXJSE\_FormCalcContext::Ceil},  

{kFuncTag, "Count", CFXJSE\_FormCalcContext::Count},  

{kFuncTag, "Floor", CFXJSE\_FormCalcContext::Floor},  

{kFuncTag, "Max", CFXJSE\_FormCalcContext::Max},  

{kFuncTag, "Min", CFXJSE\_FormCalcContext::Min},  

...

Here is the code of CFXJSE\_FormCalcContext::Oneof method.

void CFXJSE\_FormCalcContext::Oneof(CFXJSE\_Value\* pThis,  

ByteStringView bsFuncName,  

CFXJSE\_Arguments& args) {  

if (args.GetLength() < 2) {  

ToFormCalcContext(pThis)->ThrowParamCountMismatchException(L"Oneof");  

return;  

}

bool bFlags = false;  

std::unique\_ptr<CFXJSE\_Value> argOne = GetSimpleValue(pThis, args, 0);  

std::vector<std::unique\_ptr<CFXJSE\_Value>> parameterValues =  

unfoldArgs(pThis, args); // (Point 6)  

for (const auto& value : parameterValues) {  

if (simpleValueCompare(pThis, argOne.get(), value.get())) {  

bFlags = true;  

break;  

}  

}

args.GetReturnValue()->SetInteger(bFlags);  

}

At (Point 6), it calls other function, named unfoldArgs, with its arguments. The bug exists in the unfoldArgs function.

std::vector<std::unique\_ptr<CFXJSE\_Value>> CFXJSE\_FormCalcContext::unfoldArgs(  

CFXJSE\_Value\* pThis,  

CFXJSE\_Arguments& args) {  

std::vector<std::unique\_ptr<CFXJSE\_Value>> results;

// (Point 7)  

int32\_t iCount = 0;  

v8::Isolate\* pIsolate = ToFormCalcContext(pThis)->GetScriptRuntime();  

int32\_t argc = args.GetLength();  

std::vector<std::unique\_ptr<CFXJSE\_Value>> argsValue;  

static constexpr int kStart = 1;  

for (int32\_t i = 0; i < argc - kStart; i++) {  

argsValue.push\_back(args.GetValue(i + kStart));  

if (argsValue[i]->IsArray()) {  

auto lengthValue = pdfium::MakeUnique<CFXJSE\_Value>(pIsolate);  

argsValue[i]->GetObjectProperty("length", lengthValue.get()); // (Point 8)  

int32\_t iLength = lengthValue->ToInteger();  

iCount += ((iLength > 2) ? (iLength - 2) : 0);  

} else {  

++iCount;  

}  

}

for (int32\_t i = 0; i < iCount; i++) // (Point 9)  

results.push\_back(pdfium::MakeUnique<CFXJSE\_Value>(pIsolate));

int32\_t index = 0;  

for (int32\_t i = 0; i < argc - kStart; i++) {  

if (argsValue[i]->IsArray()) {  

auto lengthValue = pdfium::MakeUnique<CFXJSE\_Value>(pIsolate);  

argsValue[i]->GetObjectProperty("length", lengthValue.get()); // (Point 10)  

int32\_t iLength = lengthValue->ToInteger();  

if (iLength < 3)  

continue;

```
  auto propertyValue = pdfium::MakeUnique<CFXJSE_Value>(pIsolate);  
  auto jsObjectValue = pdfium::MakeUnique<CFXJSE_Value>(pIsolate);  
  argsValue[i]->GetObjectPropertyByIdx(1, propertyValue.get()); // (Point 11)  
  if (propertyValue->IsNull()) {  
    for (int32_t j = 2; j < iLength; j++) {  
      argsValue[i]->GetObjectPropertyByIdx(j, jsObjectValue.get());  
      GetObjectDefaultValue(jsObjectValue.get(), results[index].get());  
      index++;  
    }  
  } else {  
    for (int32_t j = 2; j < iLength; j++) { // (Point 12)  
      argsValue[i]->GetObjectPropertyByIdx(j, jsObjectValue.get());  
      jsObjectValue->GetObjectProperty(  
          propertyValue->ToString().AsStringView(), results[index].get()); // (Point 13)  
      index++;  
    }  
  }  
} else if (argsValue[i]->IsObject()) {  
  GetObjectDefaultValue(argsValue[i].get(), results[index].get());  
  index++;  
} else {  
  results[index]->Assign(argsValue[i].get());  
  index++;  
}  

```

}  

return results;  

}

This fucntions takes arguments and return the array which is flattened(unfolded) values from arguements.  

The return value(var name: results) is stored as type of std::vector.  

At (Point 7) it first traverses all arguments and calculate the total length of result. if array argument is given, it retrieves size from 'length' property (Point 8).  

After calculating total length of result, it initialized results vector with given total length (Point 9).  

At (Point 10) it gets argument array length again. and at (Point 12) for loop until argument array length, index of results is increased.  

Finally (Point 13) saves value to results vector element based on index.

The problem is that array length of argument could be modified(increased) between (Point 8) and (Point 10). The length of argument array is double-fetched.  

but at many points other javascript code would be executed and modifies the array.  

For example, At (Point 13), propertyValue->ToString() is called. The toString() javascript function of target object would be called and it could increase the length of next argument array.  

After that, In the next loop, Larger length of argument will be retrieved at (Point 10). But the size of vector was calculated by previous small length value, accessing the vector could be out-of-bounded.

To trigger this bug, Calling CFXJSE\_FormCalcContext::Oneof function with controllabe arguments. But normally it is impossible because javascript code which calls Oneof fuction is created from translation(FormCalc to javascript) and control the result of translation makes no sense.  

But calling other javascript function is possible. so define the javascript function to 'app.test' previously and later make FormCalc-converted script call 'app.test' function. The called 'app.test' function will freely access the 'pfm\_rt' global object because it's still on FormCalc context.  

With 'pfm\_rt' global object and controllabe arguments, calling pfm\_rt.Oneof with buggy arguments will trigger the bug.

Please note that CFXJSE\_FormCalcContext::concat\_fm\_object function have same root-cause bug too.

**VERSION**  

Chrome Version: PDFium with XFA enabled. Commit: c2da3ad9993bb1611691a18032a12306d0e378b3  

Operating System: All

**REPRODUCTION CASE**

1. Build pdfium\_test with XFA/ASAN enabled.
2. Load the attached poc pdf file
3. Crash occured

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: PDF plugin process  

Crash State: Address Sanitizer output

==23970==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6030000580b0 at pc 0x557a456dd0ca bp 0x7fffc195bc90 sp 0x7fffc195bc88  

READ of size 8 at 0x6030000580b0 thread T0  

#0 0x557a456dd0c9 in get buildtools/third\_party/libc++/trunk/include/memory:2624:19  

#1 0x557a456dd0c9 in CFXJSE\_FormCalcContext::unfoldArgs(CFXJSE\_Value\*, CFXJSE\_Arguments&) fxjs/xfa/cfxjse\_formcalc\_context.cpp:5359:72  

#2 0x557a456db49f in CFXJSE\_FormCalcContext::Oneof(CFXJSE\_Value\*, fxcrt::StringViewTemplate<char>, CFXJSE\_Arguments&) fxjs/xfa/cfxjse\_formcalc\_context.cpp:3112:7  

#3 0x557a456a2088 in (anonymous namespace)::V8FunctionCallback\_Wrapper(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) fxjs/xfa/cfxjse\_class.cpp:47:3  

#4 0x557a4583584d in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3  

#5 0x557a45834d06 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36  

#6 0x557a458343e1 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:141:5  

#7 0x557a46b3ce18 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4defe18)  

#8 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#9 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#10 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#11 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#12 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#13 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#14 0x557a46abc5d8 in Builtins\_ArgumentsAdaptorTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d6f5d8)  

#15 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#16 0x557a46abc5d8 in Builtins\_ArgumentsAdaptorTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d6f5d8)  

#17 0x557a46ac0499 in Builtins\_JSEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d73499)  

#18 0x557a46ac0277 in Builtins\_JSEntry (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d73277)  

#19 0x557a459ca832 in Call v8/src/execution/simulator.h:138:12  

#20 0x557a459ca832 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:266:33  

#21 0x557a459ca53d in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:358:10  

#22 0x557a4578571d in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api/api.cc:4835:7  

#23 0x557a456a703b in CFXJSE\_Context::ExecuteScript(char const\*, CFXJSE\_Value\*, CFXJSE\_Value\*) fxjs/xfa/cfxjse\_context.cpp:300:21  

#24 0x557a456ae680 in CFXJSE\_Engine::RunScript(CXFA\_Script::Type, fxcrt::StringViewTemplate<wchar\_t>, CFXJSE\_Value\*, CXFA\_Object\*) fxjs/xfa/cfxjse\_engine.cpp:153:23  

#25 0x557a47044ee1 in CXFA\_Node::ExecuteBoolScript(CXFA\_FFDocView\*, CXFA\_Script\*, CXFA\_EventParam\*) xfa/fxfa/parser/cxfa\_node.cpp:2696:22  

#26 0x557a470411db in ExecuteScript xfa/fxfa/parser/cxfa\_node.cpp:2656:10  

#27 0x557a470411db in CXFA\_Node::ProcessEventInternal(CXFA\_FFDocView\*, XFA\_AttributeValue, CXFA\_Event\*, CXFA\_EventParam\*) xfa/fxfa/parser/cxfa\_node.cpp:2360:14  

#28 0x557a47040854 in CXFA\_Node::ProcessEvent(CXFA\_FFDocView\*, XFA\_AttributeValue, CXFA\_EventParam\*) xfa/fxfa/parser/cxfa\_node.cpp:2337:9  

#29 0x557a46d89ff7 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:389:12  

#30 0x557a46d8a0d2 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:400:20  

#31 0x557a46d8a0d2 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:400:20  

#32 0x557a46d8a0d2 in CXFA\_FFDocView::ExecEventActivityByDeepFirst(CXFA\_Node\*, XFA\_EVENTTYPE, bool, bool) xfa/fxfa/cxfa\_ffdocview.cpp:400:20  

#33 0x557a46d8a50e in CXFA\_FFDocView::StartLayout() xfa/fxfa/cxfa\_ffdocview.cpp:91:3  

#34 0x557a4713d27c in CPDFXFA\_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:123:22  

#35 0x557a44a54ac6 in FPDF\_LoadXFA fpdfsdk/fpdf\_view.cpp:260:32  

#36 0x557a44980db5 in RenderPdf samples/pdfium\_test.cc:841:12  

#37 0x557a44980db5 in main samples/pdfium\_test.cc:1068:5  

#38 0x7f7ef9e6882f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

0x6030000580b0 is located 0 bytes to the right of 32-byte region [0x603000058090,0x6030000580b0)  

allocated by thread T0 here:  

#0 0x557a4497a77d in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:99:3  

#1 0x557a45704d78 in \_\_libcpp\_allocate buildtools/third\_party/libc++/trunk/include/new:238:10  

#2 0x557a45704d78 in allocate buildtools/third\_party/libc++/trunk/include/memory:1813:37  

#3 0x557a45704d78 in allocate buildtools/third\_party/libc++/trunk/include/memory:1546:21  

#4 0x557a45704d78 in std::\_\_1::\_\_split\_buffer<std::\_\_1::unique\_ptr<CFXJSE\_Value, std::\_\_1::default\_delete<CFXJSE\_Value> >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<CFXJSE\_Value, std::\_\_1::default\_delete<CFXJSE\_Value> > >&>::\_\_split\_buffer(unsigned long, unsigned long, std::\_\_1::allocator<std::\_\_1::unique\_ptr<CFXJSE\_Value, std::\_\_1::default\_delete<CFXJSE\_Value> > >&) buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:311:29  

#5 0x557a4570461c in void std::\_\_1::vector<std::\_\_1::unique\_ptr<CFXJSE\_Value, std::\_\_1::default\_delete<CFXJSE\_Value> >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<CFXJSE\_Value, std::\_\_1::default\_delete<CFXJSE\_Value> > > >::\_\_push\_back\_slow\_path<std::\_\_1::unique\_ptr<CFXJSE\_Value, std::\_\_1::default\_delete<CFXJSE\_Value> > >(std::\_\_1::unique\_ptr<CFXJSE\_Value, std::\_\_1::default\_delete<CFXJSE\_Value> >&&) buildtools/third\_party/libc++/trunk/include/vector:1622:49  

#6 0x557a456d79b1 in std::\_\_1::vector<std::\_\_1::unique\_ptr<CFXJSE\_Value, std::\_\_1::default\_delete<CFXJSE\_Value> >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<CFXJSE\_Value, std::\_\_1::default\_delete<CFXJSE\_Value> > > >::push\_back(std::\_\_1::unique\_ptr<CFXJSE\_Value, std::\_\_1::default\_delete<CFXJSE\_Value> >&&) buildtools/third\_party/libc++/trunk/include/vector:1663:9  

#7 0x557a456dbf80 in CFXJSE\_FormCalcContext::unfoldArgs(CFXJSE\_Value\*, CFXJSE\_Arguments&) fxjs/xfa/cfxjse\_formcalc\_context.cpp:5335:13  

#8 0x557a456db49f in CFXJSE\_FormCalcContext::Oneof(CFXJSE\_Value\*, fxcrt::StringViewTemplate<char>, CFXJSE\_Arguments&) fxjs/xfa/cfxjse\_formcalc\_context.cpp:3112:7  

#9 0x557a456a2088 in (anonymous namespace)::V8FunctionCallback\_Wrapper(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) fxjs/xfa/cfxjse\_class.cpp:47:3  

#10 0x557a4583584d in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:158:3  

#11 0x557a45834d06 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:111:36  

#12 0x557a458343e1 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:141:5  

#13 0x557a46b3ce18 in Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4defe18)  

#14 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#15 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#16 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#17 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#18 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#19 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#20 0x557a46abc5d8 in Builtins\_ArgumentsAdaptorTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d6f5d8)  

#21 0x557a46ac2ec0 in Builtins\_InterpreterEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d75ec0)  

#22 0x557a46abc5d8 in Builtins\_ArgumentsAdaptorTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d6f5d8)  

#23 0x557a46ac0499 in Builtins\_JSEntryTrampoline (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d73499)  

#24 0x557a46ac0277 in Builtins\_JSEntry (/home/banananapenguin/pdfium/pdfium/out/release\_asan/pdfium\_test+0x4d73277)  

#25 0x557a459ca832 in Call v8/src/execution/simulator.h:138:12  

#26 0x557a459ca832 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, v8::internal::(anonymous namespace)::InvokeParams const&) v8/src/execution/execution.cc:266:33  

#27 0x557a459ca53d in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution/execution.cc:358:10  

#28 0x557a4578571d in v8::Function::Call(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), int, v8::Local[v8::Value](javascript:void(0);)\*) v8/src/api/api.cc:4835:7  

#29 0x557a456a703b in CFXJSE\_Context::ExecuteScript(char const\*, CFXJSE\_Value\*, CFXJSE\_Value\*) fxjs/xfa/cfxjse\_context.cpp:300:21  

#30 0x557a456ae680 in CFXJSE\_Engine::RunScript(CXFA\_Script::Type, fxcrt::StringViewTemplate<wchar\_t>, CFXJSE\_Value\*, CXFA\_Object\*) fxjs/xfa/cfxjse\_engine.cpp:153:23  

#31 0x557a47044ee1 in CXFA\_Node::ExecuteBoolScript(CXFA\_FFDocView\*, CXFA\_Script\*, CXFA\_EventParam\*) xfa/fxfa/parser/cxfa\_node.cpp:2696:22  

#32 0x557a470411db in ExecuteScript xfa/fxfa/parser/cxfa\_node.cpp:2656:10  

#33 0x557a470411db in CXFA\_Node::ProcessEventInternal(CXFA\_FFDocView\*, XFA\_AttributeValue, CXFA\_Event\*, CXFA\_EventParam\*) xfa/fxfa/parser/cxfa\_node.cpp:2360:14  

#34 0x557a47040854 in CXFA\_Node::ProcessEvent(CXFA\_FFDocView\*, XFA\_AttributeValue, CXFA\_EventParam\*) xfa/fxfa/parser/cxfa\_node.cpp:2337:9

SUMMARY: AddressSanitizer: heap-buffer-overflow buildtools/third\_party/libc++/trunk/include/memory:2624:19 in get  

Shadow bytes around the buggy address:  

0x0c0680002fc0: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa  

0x0c0680002fd0: fd fd fd fd fa fa fd fd fd fd fa fa fd fd fd fd  

0x0c0680002fe0: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd  

0x0c0680002ff0: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa  

0x0c0680003000: fd fd fd fd fa fa fd fd fd fd fa fa 00 00 00 fc  

=>0x0c0680003010: fa fa 00 00 00 00[fa]fa fd fd fd fa fa fa fd fd  

0x0c0680003020: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa  

0x0c0680003030: 00 00 00 00 fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0680003040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0680003050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0680003060: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

Shadow gap: cc  

==23970==ABORTING

**CREDIT INFORMATION**  

Reporter credit: banananapenguin

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 6.7 KB)
- [poc.in](attachments/poc.in) (application/octet-stream, 1.9 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 13.1 KB)
- [poc_4141414141414141.pdf](attachments/poc_4141414141414141.pdf) (application/pdf, 7.2 KB)

## Timeline

### dt...@chromium.org (2019-09-16)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### dr...@chromium.org (2019-09-16)

This reproduces for me, sending to PDF team to investigate.

### hn...@chromium.org (2019-09-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-29)

thestig: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2019-10-02)

Impact=none, since this is XFA and not shipped to users.

### th...@chromium.org (2019-10-03)

[Empty comment from Monorail migration]

### ba...@gmail.com (2019-11-03)

Any updates? It seems that there is no update for a month on this security bug.
Additionally, Could you please check the security severity for this bug again? I think it should be high instead of medium since it is oobr bug on std::vector<std::unique_ptr<CFXJSE_Value>> type.
Thank you. Have a nice day.

### ts...@chromium.org (2019-11-04)

[Comment Deleted]

### ts...@chromium.org (2019-11-04)

The issue is XFA-Specific, and thus is not part of any shipping chrome, so it may get less attention that other security bugs.  Per the severity guidelines, "Medium severity bugs allow attackers to read or modify limited amounts of information", and an OOBR in a sandboxed process meets this criteria.  If you can show an OOB write leading to code execution, then we would reconsider. As such, the labels of severity-medium and impact-none are appropriate.

See https://www.chromium.org/developers/severity-guidelines

### ba...@gmail.com (2020-01-08)

Here is another PoC file showing possilbility of arbitrary-write primitive from this oobr bug.
The bug could be used to obtain invalid smart pointer(unique_ptr<CFXJSE_Value>) since oobr bug occured in std::vector<std::unique_ptr<CFXJSE_Value>>, 

void CFXJSE_FormCalcContext::NPV(CFXJSE_Value* pThis,
                                 ByteStringView bsFuncName,
                                 CFXJSE_Arguments& args) {
  ...
  std::vector<double> data(argc - 1);
  for (int32_t i = 1; i < argc; i++)
    data.push_back(ValueToDouble(pThis, argValues[i].get()));
  ...

I use CFXJSE_FormCalcContext::NPV function to fill the memory with controllable value(0x4141414141414141 = 2.2616345098039214499294757843E6). This filled memory will be used to buggy vector later.
By this initialization process, 'results[index].get()' of (point 13) will return controllable value(0x4141414141414141). The returned value will be used as second argument of CFXJSE_Value::GetObjectProperty call.

// fxjs/xfa/cfxjse_value.cpp
bool CFXJSE_Value::GetObjectProperty(ByteStringView szPropName,
                                     CFXJSE_Value* lpPropValue) {
  ...
  lpPropValue->ForceSetValue(hPropValue);     // (point 14)
  return true;
}

// fxjs/xfa/cfxjse_value.h
// Method of CFXJSE_Value: CFXJSE_Value::ForceSetValue
void ForceSetValue(v8::Local<v8::Value> hValue) {
  m_hValue.Reset(GetIsolate(), hValue);       // (point 15)
}
...
private:
 ...
 v8::Global<v8::Value> m_hValue;              // (point 16)

// v8/include/v8.h
void PersistentBase<T>::Reset(Isolate* isolate, const Local<S>& other) {
  TYPE_CHECK(T, S);
  Reset();
  if (other.IsEmpty()) return;
  this->val_ = New(isolate, other.val_);      // (point 17)
}

(point 14)~(point 16) shows continous call flow.
At (point 14), CFXJSE_Value::ForceSetValue method is called with controllable this pointer(lpPropValue).
At (point 15), PersistentBase<T>::Reset method is called with &m_hValue as this pointer. &h_hValue is also controllable since it is member variable of CFXJSE_Value (point 16).
At (point 16), The result of new allocation is assigned to this->val_. The this pointer is controllable therefore it results in writing pointer value(= huge value) to controllable address. arbirary-write will be achieved.

The assembly code is more straightforward to see.

0x555555d6ee80 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+160>:        mov    r12,QWORD PTR [r14]                 // (point 17) r14 = 0x4141414141414141.
0x555555d6ee83 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+163>:        mov    rdi,QWORD PTR [r14+0x8]
0x555555d6ee87 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+167>:        test   rdi,rdi
0x555555d6ee8a <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+170>:        je     0x555555d6ee99 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+185>
0x555555d6ee8c <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+172>:        call   0x555555d87ad0 <_ZN2v82V813DisposeGlobalEPm>
0x555555d6ee91 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+177>:        mov    QWORD PTR [r14+0x8],0x0
0x555555d6ee99 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+185>:        mov    bl,0x1
0x555555d6ee9b <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+187>:        test   r15,r15
0x555555d6ee9e <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+190>:        je     0x555555d6eeb3 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+211>
0x555555d6eea0 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+192>:        mov    rdi,r12
0x555555d6eea3 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+195>:        mov    rsi,r15
0x555555d6eea6 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+198>:        call   0x555555d879e0 <_ZN2v82V818GlobalizeReferenceEPNS_8internal7IsolateEPm>
0x555555d6eeab <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+203>:        mov    QWORD PTR [r14+0x8],rax             // (point 18) Writing some value to [r14+0x8]
0x555555d6eeaf <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+207>:        jmp    0x555555d6eeb3 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+211>
0x555555d6eeb1 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+209>:        xor    ebx,ebx
0x555555d6eeb3 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+211>:        lea    rdi,[rbp-0x50]
0x555555d6eeb7 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+215>:        call   0x555555d65bf0 <_ZN41CFXJSE_ScopeUtil_IsolateHandleRootContextD2Ev>
0x555555d6eebc <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+220>:        mov    eax,ebx
0x555555d6eebe <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+222>:        add    rsp,0x30
0x555555d6eec2 <_ZN12CFXJSE_Value17GetObjectPropertyEN5fxcrt18StringViewTemplateIcEEPS_+226>:        pop    rbx

Tested on pdfium_test with commit e83d8b4f0dd4b0c4edc3ea0d24d5fc0fcce40ed4 (Wed Jan 8 00:26:15 2020).
Below is build argument:
  is_debug = false
  pdf_use_skia = false
  pdf_use_skia_paths = false
  pdf_enable_xfa = true
  pdf_enable_v8 = true
  pdf_is_standalone = true
  is_component_build = false
  clang_use_chrome_plugins = false

### ba...@gmail.com (2020-01-08)

[Comment Deleted]

### ba...@gmail.com (2020-01-16)

[Comment Deleted]

### ba...@gmail.com (2020-01-16)

[Comment Deleted]

### ba...@gmail.com (2020-02-18)

The additional poc isn't enough to reconsider the bug? or just not-yet be checked? Please note that additional poc shows arbitrary write primitive with huge(pointer) value. it can lead to code execution with some leaked address information (e.g. play with ArrayBuffer address -> overwrite size of ArrayBuffer -> arbitrary r/w ->  hijack control flow)

Thank you. Have a good day.

### th...@chromium.org (2020-02-20)

Just slow. Sorry. Hopefully tsepez@ will have more time in the upcoming weeks.

### ts...@chromium.org (2020-03-02)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/67171

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-10)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/bc494f64097d51dfddb9e1c9b0a320dc274d319a

commit bc494f64097d51dfddb9e1c9b0a320dc274d319a
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Mar 10 23:25:10 2020

Fix faulty indexing CFXJSE_FormCalcContext::unfoldArgs().

Length properties may dynamically change from call to call, so
a pre-allocation may not be sufficient.

Bug: chromium:1004106
Change-Id: Ica860e7d585a8d10346ea407f8a8e3cfc1bd4a1b
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/67171
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/bc494f64097d51dfddb9e1c9b0a320dc274d319a/fxjs/xfa/cfxjse_formcalc_context.cpp
[add] https://pdfium.googlesource.com/pdfium/+/bc494f64097d51dfddb9e1c9b0a320dc274d319a/testing/resources/javascript/xfa_specific/bug_1004106.in


### ts...@chromium.org (2020-03-10)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/16697c2e77daabc27e1c17f1739bd663dfeafb72

commit 16697c2e77daabc27e1c17f1739bd663dfeafb72
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Mar 11 02:48:31 2020

Roll src/third_party/pdfium fe6381e8e366..dbb6fcdf4353 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/fe6381e8e366..dbb6fcdf4353

git log fe6381e8e366..dbb6fcdf4353 --date=short --first-parent --format='%ad %ae %s'
2020-03-11 tsepez@chromium.org Fix indexing in CFXJSE_FormCalcContext::concat_fm_object().
2020-03-11 tsepez@chromium.org Use WideStringViews in CPDF_InteractiveForm.
2020-03-10 tsepez@chromium.org Fix faulty indexing CFXJSE_FormCalcContext::unfoldArgs().

Created with:
  gclient setdep -r src/third_party/pdfium@dbb6fcdf4353

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1004106
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I08d130b1dcf9f28185533945ebbe082a6ea91deb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2097518
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#749031}

[modify] https://crrev.com/16697c2e77daabc27e1c17f1739bd663dfeafb72/DEPS


### [Deleted User] (2020-03-11)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-16)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-19)

Congrats! The Panel decided to award $7,500 for this report!

### na...@google.com (2020-03-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-06-20)

This issue was migrated from crbug.com/chromium/1004106?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050123)*
