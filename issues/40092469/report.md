# Security: Use-after-free in XFA_DataExporter_DealWithDataGroupNode

| Field | Value |
|-------|-------|
| **Issue ID** | [40092469](https://issues.chromium.org/issues/40092469) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2018-09-17 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in XFA\_DataExporter\_DealWithDataGroupNode

**VERSION**  

Operating System: Windows 10  

chrome with pdfium XFA enabled

**REPRODUCTION CASE**

1. Build chrome with XFA enabled
2. open file `poc.pdf` in chrome

Stack when crash

```
(219c.2c94): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\out\chromium_pdfium_xfa_12_09\chrome.dll  
eax=dddddddd ebx=009cc268 ecx=305d0478 edx=22382d46 esi=009cc268 edi=2f3baeb8  
eip=64030923 esp=009cbe30 ebp=009cbe3c iopl=0         nv up ei pl nz na pe nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206  
chrome!ToXMLElement+0x23:  
64030923 ff5004          call    dword ptr [eax+4]    ds:002b:dddddde1=????????  
  
3:039> kp  
 # ChildEBP RetAddr    
00 009cbe3c 651b2183 chrome!ToXMLElement(class CFX_XMLNode \* pNode = 0x305d0478)+0x23 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\core\fxcrt\xml\cfx_xmlelement.h @ 58]   
01 009cbe90 651b214a chrome!XFA_DataExporter_DealWithDataGroupNode(class CXFA_Node \* pDataNode = 0x305e3450)+0xa3 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\xfa_utils.cpp @ 497]   
02 009cbee4 651b214a chrome!XFA_DataExporter_DealWithDataGroupNode(class CXFA_Node \* pDataNode = 0x305e2ba0)+0x6a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\xfa_utils.cpp @ 489]   
03 009cbf38 651b214a chrome!XFA_DataExporter_DealWithDataGroupNode(class CXFA_Node \* pDataNode = 0x305e22f0)+0x6a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\xfa_utils.cpp @ 489]   
04 009cbf8c 651b214a chrome!XFA_DataExporter_DealWithDataGroupNode(class CXFA_Node \* pDataNode = 0x2f2cc6a8)+0x6a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\xfa_utils.cpp @ 489]   
05 009cbfe0 65a7ed34 chrome!XFA_DataExporter_DealWithDataGroupNode(class CXFA_Node \* pDataNode = 0x2f2cbdf8)+0x6a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\parser\xfa_utils.cpp @ 489]   
06 009cc0f0 65a7fe1a chrome!CJX_Node::saveXML(class CFX_V8 \* runtime = 0x2f3baeb8, class std::vector<v8::Local<v8::Value>,std::allocator<v8::Local<v8::Value> > > \* params = 0x009cc268)+0x344 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_node.cpp @ 363]   
07 009cc128 65a7d3e2 chrome!JSMethod<CJX_Node,&CJX_Node::saveXML>(class CJX_Node \* node = 0x2f2cbea8, class CFX_V8 \* runtime = 0x2f3baeb8, class std::vector<v8::Local<v8::Value>,std::allocator<v8::Local<v8::Value> > > \* params = 0x009cc268)+0x4a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\jse_define.h @ 21]   
08 009cc168 6513689d chrome!CJX_Node::saveXML_static(class CJX_Object \* node = 0x2f2cbea8, class CFX_V8 \* runtime = 0x2f3baeb8, class std::vector<v8::Local<v8::Value>,std::allocator<v8::Local<v8::Value> > > \* params = 0x009cc268)+0x52 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_node.h @ 30]   
09 009cc1dc 650facb5 chrome!CJX_Object::RunMethod(class fxcrt::WideString \* func = 0x009cc3b4, class std::vector<v8::Local<v8::Value>,std::allocator<v8::Local<v8::Value> > > \* params = 0x009cc268)+0x11d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cjx_object.cpp @ 176]   
0a 009cc28c 65a73ffb chrome!CFXJSE_Engine::NormalMethodCall(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x009cc420, class fxcrt::WideString \* functionName = 0x009cc3b4)+0x205 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cfxjse_engine.cpp @ 449]   
0b 009cc40c 12ca72e5 chrome!`anonymous namespace'::DynPropGetterAdapter_MethodCallback(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x009cc420)+0x33b [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\cfxjse_class.cpp @ 110]   
0c 009cc470 12ca628d v8!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo \* handler = 0x329d3dd5)+0x265 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api-arguments-inl.h @ 140]   
0d 009cc4d8 12ca4f54 v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate \* isolate = 0x28d08618, class v8::internal::Handle<v8::internal::HeapObject> function = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::HeapObject> new_target = class v8::internal::Handle<v8::internal::HeapObject>, class v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data = class v8::internal::Handle<v8::internal::FunctionTemplateInfo>, class v8::internal::Handle<v8::internal::Object> receiver = class v8::internal::Handle<v8::internal::Object>, class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments)+0x29d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 111]   
0e 009cc52c 12ca4a84 v8!v8::internal::Builtin_Impl_HandleApiCall(class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments, class v8::internal::Isolate \* isolate = 0x28d08618)+0x164 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 139]   
0f 009cc5a0 36d3de2a v8!v8::internal::Builtin_HandleApiCall(int args_length = 0n5, class v8::internal::Object \*\* args_object = 0x009cc5d8, class v8::internal::Isolate \* isolate = 0x28d08618)+0x64 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\builtins\builtins-api.cc @ 127]   
WARNING: Frame IP not in any known module. Following frames may be wrong.  
10 009cc5c0 2969d2b5 0x36d3de2a  
11 009cc60c 2969d2b5 0x2969d2b5  
12 009cc658 2969d2b5 0x2969d2b5  
13 009cc680 2968cc7a 0x2969d2b5  
14 009cc69c 2969d2b5 0x2968cc7a  
15 009cc6e4 2968cc7a 0x2969d2b5  
...  

```

## Attachments

- deleted (application/octet-stream, 0 B)
- [log_crash.txt](attachments/log_crash.txt) (text/plain, 25.1 KB)

## Timeline

### rs...@chromium.org (2018-09-17)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### rh...@chromium.org (2018-09-17)

[Empty comment from Monorail migration]

### rh...@chromium.org (2018-09-17)

[Empty comment from Monorail migration]

### rh...@chromium.org (2018-09-17)

I am able reproduce on Linux just using pdfium_test under ASAN. The root cause of this appears to be in CJS_Result CJX_Node::loadXML. Specifically a CXFA_DocumentParser is being created and run, but the resulting CFX_XMLDocument is never being moved out of the parser. The XMLDocument actually owns the nodes that are being created, so when the parser local var goes out of scope the doc and thus the nodes are being deleted, but there are still unowned references to them later.

The other place we parse XFA XML is in CXFA_FFDoc::ParseDoc, where the caller takes ownership of the XML Doc to avoid this problem. I am not really sure the correct way to resolve this, someone needs to own the XML Doc after parsing, but I am unclear who/how.

dsinclair, can you take a look at this? Since I believe it was your CL, https://pdfium-review.googlesource.com/c/pdfium/+/31313, that introduced this ownership pattern.

### ds...@chromium.org (2018-09-17)

I'm not going to have time to investigate this in the near future.

### hu...@gmail.com (2018-09-18)

[Comment Deleted]

### ds...@chromium.org (2018-09-18)

XFA is not enabled on any branch of Chromium.

### hu...@gmail.com (2018-09-18)

[Comment Deleted]

### ts...@chromium.org (2018-09-18)

This is what we call severity high (potential consequence), impact none (not shipped).  Adjusting as such.

### bu...@chromium.org (2018-09-18)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/7ea611fb82308b4b8f9dc150a9d79334435c53b6

commit 7ea611fb82308b4b8f9dc150a9d79334435c53b6
Author: Ryan Harrison <rharrison@chromium.org>
Date: Tue Sep 18 17:50:35 2018

Transfer ownership of nodes to top-level XML doc

For XFA, XML nodes are owned by the XML doc that they were created by,
but references to them are stored elsewhere. For a PDF document there
is one top-level XML document created and retained when the initial
XFA XML is parsed. Another can be created if loadXML is called by
JS. In the existing code the XML doc that owns the newly created nodes
is local to loadXML. So the nodes are destroyed right after putting
refernces to them into the main XFA data structures.

This CL adds in a method to transfer ownership of the XML nodes from
one doc to another, and uses it to correctly retain the newly created
nodes, by having them owned by the top-level XML doc.

BUG=chromium:884664

Change-Id: Id29b4edbfe44aefb9713328e4e217e830f7e9e14
Reviewed-on: https://pdfium-review.googlesource.com/42690
Reviewed-by: Henrique Nakashima <hnakashima@chromium.org>
Commit-Queue: Ryan Harrison <rharrison@chromium.org>

[modify] https://crrev.com/7ea611fb82308b4b8f9dc150a9d79334435c53b6/core/fxcrt/xml/cfx_xmldocument.h
[modify] https://crrev.com/7ea611fb82308b4b8f9dc150a9d79334435c53b6/core/fxcrt/xml/cfx_xmldocument.cpp
[modify] https://crrev.com/7ea611fb82308b4b8f9dc150a9d79334435c53b6/fxjs/xfa/cjx_node.cpp


### rh...@chromium.org (2018-09-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-09-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7966a719595712580ffa67dedcbfd2faa2022864

commit 7966a719595712580ffa67dedcbfd2faa2022864
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Sep 18 19:05:52 2018

Roll src/third_party/pdfium 6fc8d877d745..c3099d1c6942 (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/6fc8d877d745..c3099d1c6942


git log 6fc8d877d745..c3099d1c6942 --date=short --no-merges --format='%ad %ae %s'
2018-09-18 hnakashima@chromium.org Change signature of FPDFPageObjMark_Get(Name|ParamKey).
2018-09-18 rharrison@chromium.org Transfer ownership of nodes to top-level XML doc


Created with:
  gclient setdep -r src/third_party/pdfium@c3099d1c6942

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:884664
TBR=dsinclair@chromium.org

Change-Id: Ifcdc87b0ee64b981f34c47a61775113428f8f887
Reviewed-on: https://chromium-review.googlesource.com/1231497
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#592133}
[modify] https://crrev.com/7966a719595712580ffa67dedcbfd2faa2022864/DEPS


### sh...@chromium.org (2018-09-19)

[Empty comment from Monorail migration]

### hu...@gmail.com (2018-10-11)

[Comment Deleted]

### aw...@google.com (2018-11-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-12)

And $3,000 for this one too!

### aw...@google.com (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-12-26)

This issue was migrated from crbug.com/chromium/884664?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092469)*
