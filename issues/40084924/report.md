# Heap-use-after-free in CPDFSDK_Document::KillFocusAnnot

| Field | Value |
|-------|-------|
| **Issue ID** | [40084924](https://issues.chromium.org/issues/40084924) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2016-07-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

CPDFSDK\_Document::RemovePageView method has these 2 lines.

pPageView->KillFocusAnnotIfNeeded();  

delete pPageView;

Attached testfocus.pdf file can reenter CPDFSDK\_Document::RemovePageView method through pPageView->KillFocusAnnotIfNeeded() call and execute "delete pPageView".

testfocus.pdf file has 3 text fields named txt1, txt2, txt2.  

Document javascript of testfocus.pdf contains->  

this.getField('txt1').setFocus();  

this.pageNum = 2;

Focus lost event handler javascript of txt1 text field contains->  

this.getField('txt2').setFocus();

**VERSION**  

Chrome Version: [52.0.2743.82 m] + [stable]  

[54.0.2805.0] + [TOT]  

Operating System: [Ubuntu Linux 14.04, Windows 10]

**REPRODUCTION CASE**

1. Open testfocus.pdf file in chrome.  
   
   Chrome pdf plugin will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [PDF plugin process]  

Crash State: Address Sanitizer output

AddressSanitizer: heap-use-after-free on address 0x606000060da0 at pc 0x55ca32f80b22 bp 0x7fffa18112b0 sp 0x7fffa18112a8  

READ of size 8 at 0x606000060da0 thread T0 (chrome)  

#0 0x55ca32f80b21 in KillFocusAnnot ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_mgr.cpp:434:24  

#1 0x55ca32f7fe6f in KillFocusAnnot ./out/Asan/../../third\_party/pdfium/fpdfsdk/include/fsdk\_mgr.h:555:23  

#2 0x55ca32f7fe6f in KillFocusAnnotIfNeeded ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_mgr.cpp:628:0  

#3 0x55ca32f7fe6f in RemovePageView ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_mgr.cpp:356:0  

#4 0x55ca2aa21f42 in Unload ./out/Asan/../../pdf/pdfium/pdfium\_page.cc:110:7  

#5 0x55ca2a9f5dfa in CalculateVisiblePages ./out/Asan/../../pdf/pdfium/pdfium\_engine.cc:2633:20  

#6 0x55ca2a9f67f2 in ScrolledToYPosition ./out/Asan/../../pdf/pdfium/pdfium\_engine.cc:892:3  

#7 0x55ca2aa3dd79 in HandleMessage ./out/Asan/../../pdf/out\_of\_process\_instance.cc:407:14  

..............

0x606000060da0 is located 0 bytes inside of 56-byte region [0x606000060da0,0x606000060dd8)  

freed by thread T0 (chrome) here:  

#0 0x55ca23edb9fb in operator delete(void\*) ??:?  

#1 0x55ca32f842e2 in ReleaseAnnot ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_annothandler.cpp:101:20  

#2 0x55ca32f81145 in ~CPDFSDK\_PageView ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_mgr.cpp:500:23  

#3 0x55ca32f7fe77 in RemovePageView ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_mgr.cpp:357:3  

#4 0x55ca2aa21f42 in Unload ./out/Asan/../../pdf/pdfium/pdfium\_page.cc:110:7  

#5 0x55ca2a9f5dfa in CalculateVisiblePages ./out/Asan/../../pdf/pdfium/pdfium\_engine.cc:2633:20  

#6 0x55ca2aa100ad in ?? ./out/Asan/../../pdf/pdfium/pdfium\_engine.cc:2277:3  

#7 0x55ca2a9f29f4 in Form\_GetCurrentPage ./out/Asan/../../pdf/pdfium/pdfium\_engine.cc:3466:21  

#8 0x55ca333f65b9 in FFI\_GetCurrentPage ./out/Asan/../../third\_party/pdfium/fpdfsdk/include/fsdk\_mgr.h:115:14  

#9 0x55ca333f65b9 in setFocus ./out/Asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:3247:0  

#10 0x55ca334128a7 in JSMethod<Field, &Field::setFocus> ./out/Asan/../../third\_party/pdfium/fpdfsdk/javascript/JS\_Define.h:158:8  

#11 0x55ca25a31069 in Call ./out/Asan/../../v8/src/api-arguments.cc:19:3  

#12 0x55ca25c0f824 in HandleApiCallHelper<false> ./out/Asan/../../v8/src/builtins/builtins.cc:240:36  

#13 0x55ca25c0d27e in Builtin\_Impl\_HandleApiCall ./out/Asan/../../v8/src/builtins/builtins.cc:269:5  

#13 0x7fa1d00063a6 (<unknown module>)  

#14 0x7fa1d006fab5 (<unknown module>)  

#15 0x7fa1d0046682 (<unknown module>)  

#16 0x7fa1d002676e (<unknown module>)  

#14 0x55ca263aa154 in Invoke ./out/Asan/../../v8/src/execution.cc:111:13  

#15 0x55ca263a9b2f in Call ./out/Asan/../../v8/src/execution.cc:168:10  

#16 0x55ca25a4900b in Run ./out/Asan/../../v8/src/api.cc:1909:23  

#17 0x55ca33459ac3 in FXJS\_Execute ./out/Asan/../../third\_party/pdfium/fxjs/fxjs\_v8.cpp:467:25  

#18 0x55ca3338b5ec in ?? ./out/Asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_runtime.cpp:224:14  

#19 0x55ca33454d9b in RunScript ./out/Asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_context.cpp:54:24  

#20 0x55ca32f56096 in ?? ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_actionhandler.cpp:531:28  

#21 0x55ca32f56dbd in ExecuteFieldAction ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_actionhandler.cpp:250:9  

#22 0x55ca32f56a5e in DoAction\_Field ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_actionhandler.cpp:106:10  

#23 0x55ca32f6edba in OnAAction ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_baseform.cpp:1894:28  

#24 0x55ca32f98db7 in OnKillFocus ./out/Asan/../../third\_party/pdfium/fpdfsdk/formfiller/cffl\_iformfiller.cpp:480:18  

#25 0x55ca32f891de in ?? ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_annothandler.cpp:733:29  

#26 0x55ca32f868a2 in Annot\_OnKillFocus ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_annothandler.cpp:325:27

previously allocated by thread T0 (chrome) here:  

#0 0x55ca23edb3fb in operator new(unsigned long) ??:?  

#1 0x55ca32f8708c in NewAnnot ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_annothandler.cpp:448:29  

#2 0x55ca32f84092 in NewAnnot ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_annothandler.cpp:77:27  

#3 0x55ca32f7edb1 in LoadFXAnnots ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_mgr.cpp:964:47  

#4 0x55ca32f7e480 in GetPageView ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_mgr.cpp:277:14  

#5 0x55ca32f4c983 in FormHandleToPageView ./out/Asan/../../third\_party/pdfium/fpdfsdk/fpdfformfill.cpp:44:29  

#6 0x55ca32f4c983 in FORM\_OnAfterLoadPage ./out/Asan/../../third\_party/pdfium/fpdfsdk/fpdfformfill.cpp:641:0  

#7 0x55ca2aa22191 in GetPage ./out/Asan/../../pdf/pdfium/pdfium\_page.cc:125:7  

#8 0x55ca32f7f24e in FFI\_GetPage ./out/Asan/../../third\_party/pdfium/fpdfsdk/include/fsdk\_mgr.h:109:14  

#9 0x55ca32f7f24e in GetPageView ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_mgr.cpp:289:0  

#10 0x55ca32f6f7f6 in GetWidget ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_baseform.cpp:2055:28  

#11 0x55ca333f6505 in setFocus ./out/Asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:3243:27  

#12 0x55ca334128a7 in JSMethod<Field, &Field::setFocus> ./out/Asan/../../third\_party/pdfium/fpdfsdk/javascript/JS\_Define.h:158:8  

#13 0x55ca25a31069 in Call ./out/Asan/../../v8/src/api-arguments.cc:19:3  

#14 0x55ca25c0f824 in HandleApiCallHelper<false> ./out/Asan/../../v8/src/builtins/builtins.cc:240:36  

#15 0x55ca25c0d27e in Builtin\_Impl\_HandleApiCall ./out/Asan/../../v8/src/builtins/builtins.cc:269:5  

#14 0x7fa1d00063a6 (<unknown module>)  

#15 0x7fa1d006f895 (<unknown module>)  

#16 0x7fa1d0046682 (<unknown module>)  

#17 0x7fa1d002676e (<unknown module>)  

#16 0x55ca263aa154 in Invoke ./out/Asan/../../v8/src/execution.cc:111:13  

#17 0x55ca263a9b2f in Call ./out/Asan/../../v8/src/execution.cc:168:10  

#18 0x55ca25a4900b in Run ./out/Asan/../../v8/src/api.cc:1909:23  

#19 0x55ca33459ac3 in FXJS\_Execute ./out/Asan/../../third\_party/pdfium/fxjs/fxjs\_v8.cpp:467:25  

#20 0x55ca3338b5ec in ?? ./out/Asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_runtime.cpp:224:14  

#21 0x55ca33454d9b in RunScript ./out/Asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_context.cpp:54:24  

#22 0x55ca32f55840 in RunDocumentOpenJavaScript ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_actionhandler.cpp:549:28  

#23 0x55ca32f55840 in DoAction\_JavaScript ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_actionhandler.cpp:36:0  

#24 0x55ca32f7f6ed in ProcJavascriptFun ./out/Asan/../../third\_party/pdfium/fpdfsdk/fsdk\_mgr.cpp:307:34  

#25 0x55ca2a9fd453 in FinishLoadingDocument ./out/Asan/../../pdf/pdfium/pdfium\_engine.cc:1116:3  

#26 0x55ca2aa12e11 in ContinueLoadingDocument ./out/Asan/../../pdf/pdfium/pdfium\_engine.cc:2546:5  

#27 0x55ca2a9fbbd2 in LoadDocument ./out/Asan/../../pdf/pdfium/pdfium\_engine.cc:2435:5  

#28 0x55ca2aa37ee5 in DidRead ./out/Asan/../../pdf/document\_loader.cc:418:5

## Attachments

- [testfocus.pdf](attachments/testfocus.pdf) (application/pdf, 3.3 KB)
- [testfocus2.pdf](attachments/testfocus2.pdf) (application/pdf, 3.6 KB)

## Timeline

### ke...@chromium.org (2016-07-22)

My attempts to reproduce this have all come up empty (can't get the asan build to run in VMs). Are you able to triage this Oliver?

[Monorail components: Internals>Plugins>PDF]

### ke...@chromium.org (2016-07-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-23)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-07-24)

Attached another test case (testfocus2.pdf). This test case has a different address sanitizer output. But this has a common cause with first test case (testfocus.pdf).

This part of back trace is same in both test cases.
Unload ./out/Asan/../../pdf/pdfium/pdfium_page.cc:110:7
CalculateVisiblePages ./out/Asan/../../pdf/pdfium/pdfium_engine.cc:2633:20
 ?? ./out/Asan/../../pdf/pdfium/pdfium_engine.cc:2277:3
Form_GetCurrentPage ./out/Asan/../../pdf/pdfium/pdfium_engine.cc:3466:21
FFI_GetCurrentPage ./out/Asan/../../third_party/pdfium/fpdfsdk/include/fsdk_mgr.h:115:14
in setFocus ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/Field.cpp:3247:0

So I think common cause of both test cases is setFocus method in pdfium/fpdfsdk/javascript/Field.cpp can synchronously call Unload of pdf/pdfium/pdfium_page.cc.

Reproduction steps
------------------
1. Open testfocus2.pdf with chromium browser.

Address Sanitizer output
--------------------------

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x60600007d088 at pc 0x557c01857f41 bp 0x7ffea73c93a0 sp 0x7ffea73c9398
WRITE of size 4 at 0x60600007d088 thread T0 (chrome)
    #0 0x557c01857f40 in SetAppModified ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_baseform.cpp:724:18
    #1 0x557c01857f40 in ResetAppearance ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_baseform.cpp:753:0
    #2 0x557c01cdc036 in UpdateFormField ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/Field.cpp:232:18
    #3 0x557c01cdd6f6 in SetBorderStyle ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/Field.cpp:465:9
    #4 0x557c01cdcfc1 in borderStyle ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/Field.cpp:388:7
    #5 0x557c01cf570c in JSPropSetter<Field, &Field::borderStyle> ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/JS_Define.h:116:8
    #6 0x557bf4edbe18 in Call ./out/Asan/../../v8/src/api-arguments-inl.h:101:3
    #7 0x557bf502c299 in SetPropertyWithAccessor ./out/Asan/../../v8/src/objects.cc:1249:10
    #8 0x557bf5062db7 in SetPropertyInternal ./out/Asan/../../v8/src/objects.cc:4420:16
    #9 0x557bf5061e9d in SetProperty ./out/Asan/../../v8/src/objects.cc:4452:9
    #10 0x557bf4ea6047 in Store ./out/Asan/../../v8/src/ic/ic.cc:1594:3
    #11 0x557bf4eba111 in __RT_impl_Runtime_StoreIC_Miss ./out/Asan/../../v8/src/ic/ic.cc:2412:5
    #12 0x557bf4eba111 in Runtime_StoreIC_Miss ./out/Asan/../../v8/src/ic/ic.cc:2396:0
    #11 0x7efe38a063a6  (<unknown module>)
    #12 0x7efe38a7006b  (<unknown module>)
    #13 0x7efe38a6ff27  (<unknown module>)
    #14 0x7efe38a46682  (<unknown module>)
    #15 0x7efe38a2676e  (<unknown module>)
    #13 0x557bf4ca8154 in Invoke ./out/Asan/../../v8/src/execution.cc:111:13
    #14 0x557bf4ca7b2f in Call ./out/Asan/../../v8/src/execution.cc:168:10
    #15 0x557bf434700b in Run ./out/Asan/../../v8/src/api.cc:1909:23
    #16 0x557c01d57ac3 in FXJS_Execute ./out/Asan/../../third_party/pdfium/fxjs/fxjs_v8.cpp:467:25
    #17 0x557c01c895ec in ?? ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/cjs_runtime.cpp:224:14
    #18 0x557c01d52d9b in RunScript ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/cjs_context.cpp:54:24
    #19 0x557c01d43755 in RunJsScript ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/app.cpp:522:15
    #20 0x557c01d43755 in TimerProc ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/app.cpp:510:0
    #21 0x557c01d21ff9 in TimerProc ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/JS_Object.cpp:155:30
    .........

0x60600007d088 is located 40 bytes inside of 56-byte region [0x60600007d060,0x60600007d098)
freed by thread T0 (chrome) here:
    #0 0x557bf27d99fb in operator delete(void*) ??:?
    #1 0x557c018822e2 in ReleaseAnnot ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_annothandler.cpp:101:20
    #2 0x557c0187f145 in ~CPDFSDK_PageView ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:500:23
    #3 0x557c0187de77 in RemovePageView ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:357:3
    #4 0x557bf931ff42 in Unload ./out/Asan/../../pdf/pdfium/pdfium_page.cc:110:7
    #5 0x557bf92f3dfa in CalculateVisiblePages ./out/Asan/../../pdf/pdfium/pdfium_engine.cc:2633:20
    #6 0x557bf930e0ad in ?? ./out/Asan/../../pdf/pdfium/pdfium_engine.cc:2277:3
    #7 0x557bf92f09f4 in Form_GetCurrentPage ./out/Asan/../../pdf/pdfium/pdfium_engine.cc:3466:21
    #8 0x557c01cf45b9 in FFI_GetCurrentPage ./out/Asan/../../third_party/pdfium/fpdfsdk/include/fsdk_mgr.h:115:14
    #9 0x557c01cf45b9 in setFocus ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/Field.cpp:3247:0
    #10 0x557c01d108a7 in JSMethod<Field, &Field::setFocus> ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/JS_Define.h:158:8
    #11 0x557bf432f069 in Call ./out/Asan/../../v8/src/api-arguments.cc:19:3
    #12 0x557bf450d824 in HandleApiCallHelper<false> ./out/Asan/../../v8/src/builtins/builtins.cc:240:36
    #13 0x557bf450b27e in Builtin_Impl_HandleApiCall ./out/Asan/../../v8/src/builtins/builtins.cc:269:5
    #13 0x7efe38a063a6  (<unknown module>)
    #14 0x7efe38a6fab5  (<unknown module>)
    #15 0x7efe38a46682  (<unknown module>)
    #16 0x7efe38a2676e  (<unknown module>)
    #14 0x557bf4ca8154 in Invoke ./out/Asan/../../v8/src/execution.cc:111:13
    #15 0x557bf4ca7b2f in Call ./out/Asan/../../v8/src/execution.cc:168:10
    #16 0x557bf434700b in Run ./out/Asan/../../v8/src/api.cc:1909:23
    #17 0x557c01d57ac3 in FXJS_Execute ./out/Asan/../../third_party/pdfium/fxjs/fxjs_v8.cpp:467:25
    #18 0x557c01c895ec in ?? ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/cjs_runtime.cpp:224:14
    #19 0x557c01d52d9b in RunScript ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/cjs_context.cpp:54:24
    #20 0x557c0186a4a4 in OnFormat ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_baseform.cpp:2247:34
    #21 0x557c0186a0a0 in OnFormat ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_baseform.cpp:790:24
    #22 0x557c01cdbfea in UpdateFormField ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/Field.cpp:231:42
    #23 0x557c01cdd6f6 in SetBorderStyle ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/Field.cpp:465:9
    #24 0x557c01cdcfc1 in borderStyle ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/Field.cpp:388:7
    #25 0x557c01cf570c in JSPropSetter<Field, &Field::borderStyle> ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/JS_Define.h:116:8
    #26 0x557bf4edbe18 in Call ./out/Asan/../../v8/src/api-arguments-inl.h:101:3

previously allocated by thread T0 (chrome) here:
    #0 0x557bf27d93fb in operator new(unsigned long) ??:?
    #1 0x557c0188508c in NewAnnot ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_annothandler.cpp:448:29
    #2 0x557c01882092 in NewAnnot ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_annothandler.cpp:77:27
    #3 0x557c0187cdb1 in LoadFXAnnots ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:964:47
    #4 0x557c0187c480 in GetPageView ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:277:14
    #5 0x557c0184a983 in FormHandleToPageView ./out/Asan/../../third_party/pdfium/fpdfsdk/fpdfformfill.cpp:44:29
    #6 0x557c0184a983 in FORM_OnAfterLoadPage ./out/Asan/../../third_party/pdfium/fpdfsdk/fpdfformfill.cpp:641:0
    #7 0x557bf9320191 in GetPage ./out/Asan/../../pdf/pdfium/pdfium_page.cc:125:7
    #8 0x557c0187d24e in FFI_GetPage ./out/Asan/../../third_party/pdfium/fpdfsdk/include/fsdk_mgr.h:109:14
    #9 0x557c0187d24e in GetPageView ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:289:0
    #10 0x557c0186d7f6 in GetWidget ./out/Asan/../../third_party/pdfium/fpdfsdk/fsdk_baseform.cpp:2055:28
    #11 0x557c01cdd663 in GetWidget ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/Field.cpp:293:35
    #12 0x557c01cdd663 in SetBorderStyle ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/Field.cpp:457:0
    #13 0x557c01cdcfc1 in borderStyle ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/Field.cpp:388:7
    #14 0x557c01cf570c in JSPropSetter<Field, &Field::borderStyle> ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/JS_Define.h:116:8
    #15 0x557bf4edbe18 in Call ./out/Asan/../../v8/src/api-arguments-inl.h:101:3
    #16 0x557bf502c299 in SetPropertyWithAccessor ./out/Asan/../../v8/src/objects.cc:1249:10
    #17 0x557bf5062db7 in SetPropertyInternal ./out/Asan/../../v8/src/objects.cc:4420:16
    #18 0x557bf5061e9d in SetProperty ./out/Asan/../../v8/src/objects.cc:4452:9
    #19 0x557bf4ea6047 in Store ./out/Asan/../../v8/src/ic/ic.cc:1594:3
    #20 0x557bf4eba111 in __RT_impl_Runtime_StoreIC_Miss ./out/Asan/../../v8/src/ic/ic.cc:2412:5
    #21 0x557bf4eba111 in Runtime_StoreIC_Miss ./out/Asan/../../v8/src/ic/ic.cc:2396:0
    #18 0x7efe38a063a6  (<unknown module>)
    #19 0x7efe38a7006b  (<unknown module>)
    #20 0x7efe38a6ff27  (<unknown module>)
    #21 0x7efe38a46682  (<unknown module>)
    #22 0x7efe38a2676e  (<unknown module>)
    #22 0x557bf4ca8154 in Invoke ./out/Asan/../../v8/src/execution.cc:111:13
    #23 0x557bf4ca7b2f in Call ./out/Asan/../../v8/src/execution.cc:168:10
    #24 0x557bf434700b in Run ./out/Asan/../../v8/src/api.cc:1909:23
    #25 0x557c01d57ac3 in FXJS_Execute ./out/Asan/../../third_party/pdfium/fxjs/fxjs_v8.cpp:467:25
    #26 0x557c01c895ec in ?? ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/cjs_runtime.cpp:224:14
    #27 0x557c01d52d9b in RunScript ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/cjs_context.cpp:54:24
    #28 0x557c01d43755 in RunJsScript ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/app.cpp:522:15
    #29 0x557c01d43755 in TimerProc ./out/Asan/../../third_party/pdfium/fpdfsdk/javascript/app.cpp:510:0

### cl...@chromium.org (2016-07-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5172293382963200

### cl...@chromium.org (2016-07-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4604273421975552

### oc...@chromium.org (2016-07-25)

Looks like this repros in Chrome, but not pdfium_test on CF. Dan, mind taking a look at this one?

### ke...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-07-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4604273421975552

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x60c0000e9aa8
Crash State:
  CPDFSDK_Widget::ResetAppearance
  Field::UpdateFormField
  Field::SetBorderStyle
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=309333:309369

Minimized Testcase (3.59 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96ddlhmdXdAEwKxB45Nb5ie2Ps3xfgFjdZfaY5zm_KXQHEgWeLwkyFSe2VkyBnwh9ih2ue-BlhghAqmiUlHe8FZMzFto7xsfLsleEKzzj8PsuY6aan_OoFRLFhkMrlv1JRAjJ7cdu4YmCRuHicc-zsiqhGvDg?testcase_id=4604273421975552

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### sh...@chromium.org (2016-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-07-26)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/49dce65dc78bcd5a0c78a8bbdf2809cf20212220

commit 49dce65dc78bcd5a0c78a8bbdf2809cf20212220
Author: dsinclair <dsinclair@chromium.org>
Date: Tue Jul 26 19:09:42 2016

Remove pageview from map immediately

There seems to be an ownership issue in the page annotation code where removing
the annotations can result in removing the parent page view. This is fine except
that removing the parent page view removes the annotations and you can end up
with a use-after-free.

This CL removes the page view from the documents page map immediately and then
proceeds with the cleanup. Then, if we try to remove that page again it won't
be found and we won't double free.

BUG=chromium:630654

Review-Url: https://codereview.chromium.org/2179283005

[modify] https://crrev.com/49dce65dc78bcd5a0c78a8bbdf2809cf20212220/fpdfsdk/fsdk_mgr.cpp


### ds...@chromium.org (2016-07-26)

The work-around has landed which should resolve the use after free.

### ds...@chromium.org (2016-07-26)

Work around reverted due to linux_asan embedder test issues.

### bu...@chromium.org (2016-07-26)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/f2cee9894b9f7cf2e50060965ad1eedd90ab55b6

commit f2cee9894b9f7cf2e50060965ad1eedd90ab55b6
Author: dsinclair <dsinclair@chromium.org>
Date: Tue Jul 26 19:19:43 2016

Revert of Remove pageview from map immediately (patchset #1 id:1 of https://codereview.chromium.org/2179283005/ )

Reason for revert:
Looks like this broke linux_asan embedder tests.

https://build.chromium.org/p/client.pdfium/builders/linux_asan/builds/1152/steps/embeddertests/logs/stdio

Original issue's description:
> Remove pageview from map immediately
>
> There seems to be an ownership issue in the page annotation code where removing
> the annotations can result in removing the parent page view. This is fine except
> that removing the parent page view removes the annotations and you can end up
> with a use-after-free.
>
> This CL removes the page view from the documents page map immediately and then
> proceeds with the cleanup. Then, if we try to remove that page again it won't
> be found and we won't double free.
>
> BUG=chromium:630654
>
> Committed: https://pdfium.googlesource.com/pdfium/+/49dce65dc78bcd5a0c78a8bbdf2809cf20212220

TBR=thestig@chromium.org,weili@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=chromium:630654

Review-Url: https://codereview.chromium.org/2188523002

[modify] https://crrev.com/f2cee9894b9f7cf2e50060965ad1eedd90ab55b6/fpdfsdk/fsdk_mgr.cpp


### bu...@chromium.org (2016-07-27)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/461eeafe191068ac8c32f2717907fc6a22a667d2

commit 461eeafe191068ac8c32f2717907fc6a22a667d2
Author: dsinclair <dsinclair@chromium.org>
Date: Wed Jul 27 14:40:05 2016

Reland of Remove pageview from map immediately

This reverts commit f2cee9894b9f7cf2e50060965ad1eedd90ab55b6.

This CL removes the default parameter from the CPDFSDK_Document::GetPageView
|ReNew| flag and updates the code as needed. In
CFFL_FormFillter::KillFocusForAnnot we flip the flag to |FALSE| as we don't want
to re-create the page view if it is already removed. If we don't do this then
the page view will be re-created in the map, the page associated to the page
view, but then the page can be deleted out from under the pageview as it isn't
owned by the page view.

BUG=chromium:630654

Review-Url: https://codereview.chromium.org/2179163004

[modify] https://crrev.com/461eeafe191068ac8c32f2717907fc6a22a667d2/fpdfsdk/formfiller/cffl_combobox.cpp
[modify] https://crrev.com/461eeafe191068ac8c32f2717907fc6a22a667d2/fpdfsdk/formfiller/cffl_formfiller.cpp
[modify] https://crrev.com/461eeafe191068ac8c32f2717907fc6a22a667d2/fpdfsdk/formfiller/cffl_formfiller.h
[modify] https://crrev.com/461eeafe191068ac8c32f2717907fc6a22a667d2/fpdfsdk/formfiller/cffl_textfield.cpp
[modify] https://crrev.com/461eeafe191068ac8c32f2717907fc6a22a667d2/fpdfsdk/fpdfformfill.cpp
[modify] https://crrev.com/461eeafe191068ac8c32f2717907fc6a22a667d2/fpdfsdk/fpdfxfa/fpdfxfa_doc.cpp
[modify] https://crrev.com/461eeafe191068ac8c32f2717907fc6a22a667d2/fpdfsdk/fsdk_baseform.cpp
[modify] https://crrev.com/461eeafe191068ac8c32f2717907fc6a22a667d2/fpdfsdk/fsdk_mgr.cpp
[modify] https://crrev.com/461eeafe191068ac8c32f2717907fc6a22a667d2/fpdfsdk/include/fsdk_mgr.h
[modify] https://crrev.com/461eeafe191068ac8c32f2717907fc6a22a667d2/fpdfsdk/javascript/Document.cpp
[modify] https://crrev.com/461eeafe191068ac8c32f2717907fc6a22a667d2/fpdfsdk/javascript/Field.cpp


### ds...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-07-27)

dsinclair, Does above changeset fix bug mentioned in https://crbug.com/chromium/630654#c4 (testfocus2.pdf)?

### ds...@chromium.org (2016-07-27)

Looks like testfocus2 is a separate issue. Can you file a new bug with that file attached?

### ch...@gmail.com (2016-07-27)

This fix is not yet available with chrome Tot. I ll create a new issue after I update my local repository with fix.

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-07-28)

Is this pdfium fix rolled to chromium source repository?

### sh...@chromium.org (2016-07-28)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-07-28)

dsinclair, Does this fix work when used with chrome?
I built chrome with a copy of pdfium trunk and testfocus.pdf still reproduces for me. But this time UAF object is CPDF_Page.

### ds...@chromium.org (2016-07-28)

testfocus.pdf works correctly for me with chrome. I'm not seeing any UAF's when using that file.

### ch...@gmail.com (2016-07-28)

I think something is wrong with the way I updated pdfium. I will update chrome when fix is rolled to chrome and test.

### bu...@chromium.org (2016-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/436bf1c042b07d2fee38c430de5232b7b5d688e6

commit 436bf1c042b07d2fee38c430de5232b7b5d688e6
Author: ochang <ochang@chromium.org>
Date: Thu Jul 28 17:30:22 2016

Roll PDFium d8cc503..6f10254

https://pdfium.googlesource.com/pdfium.git/+log/d8cc503..6f10254

BUG=630654
TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2190853004
Cr-Commit-Position: refs/heads/master@{#408419}

[modify] https://crrev.com/436bf1c042b07d2fee38c430de5232b7b5d688e6/DEPS


### ch...@gmail.com (2016-07-29)

Reported https://crbug.com/chromium/632709 for testfocus2.pdf.

### ch...@gmail.com (2016-07-30)

testfocus.pdf crashed on chrome asan build downloaded from https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-408734.zip?generation=1469842261978000&alt=media
That file is created on 2016-07-30.

dsinclair, Can you give me a link to the file you are testing please? It is possible that this issue reproduces on my computer's configuration only.


### sh...@chromium.org (2016-07-30)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-07-30)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### cl...@chromium.org (2016-07-31)

ClusterFuzz has detected this issue as fixed in range 408633:408661.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4604273421975552

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free WRITE 4
Crash Address: 0x60c0000e9aa8
Crash State:
  CPDFSDK_Widget::ResetAppearance
  Field::UpdateFormField
  Field::SetBorderStyle
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=309333:309369
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=408633:408661

Minimized Testcase (3.59 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96ddlhmdXdAEwKxB45Nb5ie2Ps3xfgFjdZfaY5zm_KXQHEgWeLwkyFSe2VkyBnwh9ih2ue-BlhghAqmiUlHe8FZMzFto7xsfLsleEKzzj8PsuY6aan_OoFRLFhkMrlv1JRAjJ7cdu4YmCRuHicc-zsiqhGvDg?testcase_id=4604273421975552

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### go...@chromium.org (2016-08-01)

+awhalley@, can we take this merge in for M53? Fix is already verified by clusterfuzz per https://crbug.com/chromium/630654#c33.

### aw...@chromium.org (2016-08-01)

Good for M53 merge.

### go...@chromium.org (2016-08-01)

Approving merge to M53 branch 2785 based on https://crbug.com/chromium/630654#c35. Please merge ASAP so we can take it for this week beta release on Wednesday.

### aw...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-02)

Another great report and $3,000, many thanks!

### bu...@chromium.org (2016-08-02)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/tools/buildspec/+/ff55db1bffa06fd8a7be527967cee1d3c5add668

commit ff55db1bffa06fd8a7be527967cee1d3c5add668
Author: Dan Sinclair <dsinclair@chromium.org>
Date: Tue Aug 02 17:16:51 2016


### ds...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-08-08)

[Comment Deleted]

### ch...@gmail.com (2016-08-08)

testfocus.pdf file still crash in chrome ASAN builds.

* testfocus.pdf did not crash on windows debug build for me.
  But when I debugged below mentioned UAF existed in windows debug build too.

Chrome versions:
1. chrome beta 53.0.2785.46 downloaded from -
https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-beta-53.0.2785.46.zip?generation=1470397538179000&alt=media
2. 54.0.2822.0 (64-bit) - Tot ASAN build

Address Sanitizer Output from chrome beta 53.0.2785.46
-------------------------------------------------------

==6798==ERROR: AddressSanitizer: heap-use-after-free on address 0x610000003ee8 at pc 0x5606a2c6eb4c bp 0x7ffe18905440 sp 0x7ffe18905438
WRITE of size 8 at 0x610000003ee8 thread T0 (chrome)
    #0 0x5606a2c6eb4b in SetView third_party/pdfium/core/fpdfapi/fpdf_page/include/cpdf_page.h:53:39
    #1 0x5606a2c6eb4b in CPDFSDK_PageView::~CPDFSDK_PageView() third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:508
    #2 0x5606a2c6d686 in CPDFSDK_Document::RemovePageView(CPDF_Page*) third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:361:3
    #3 0x5606970c1af2 in chrome_pdf::PDFiumPage::Unload() pdf/pdfium/pdfium_page.cc:110:7
    #4 0x560697094afa in chrome_pdf::PDFiumEngine::CalculateVisiblePages() pdf/pdfium/pdfium_engine.cc:2619:20
    #5 0x5606970954f2 in chrome_pdf::PDFiumEngine::ScrolledToYPosition(int) pdf/pdfium/pdfium_engine.cc:892:3
    #6 0x5606970de499 in chrome_pdf::OutOfProcessInstance::HandleMessage(pp::Var const&) pdf/out_of_process_instance.cc:407:14
..........

0x610000003ee8 is located 168 bytes inside of 192-byte region [0x610000003e40,0x610000003f00)
freed by thread T0 (chrome) here:
    #0 0x5606964a723b in operator delete(void*) (/home/chamal/programs/chrome-asan-prebuilts/asan-linux-beta-53.0.2785.46/chrome+0x2a7223b)
    #1 0x5606970c1b04 in chrome_pdf::PDFiumPage::Unload() pdf/pdfium/pdfium_page.cc:112:5
    #2 0x560697094afa in chrome_pdf::PDFiumEngine::CalculateVisiblePages() pdf/pdfium/pdfium_engine.cc:2619:20
    #3 0x5606970aed0d in chrome_pdf::PDFiumEngine::GetMostVisiblePage() pdf/pdfium/pdfium_engine.cc:2263:3
    #4 0x5606970916f4 in chrome_pdf::PDFiumEngine::Form_GetCurrentPage(_FPDF_FORMFILLINFO*, void*) pdf/pdfium/pdfium_engine.cc:3452:21
    #5 0x5606a30edf69 in FFI_GetCurrentPage third_party/pdfium/fpdfsdk/include/fsdk_mgr.h:115:14
    #6 0x5606a30edf69 in Field::setFocus(IJS_Context*, std::__1::vector<CJS_Value, std::__1::allocator<CJS_Value> > const&, CJS_Value&, CFX_WideString&) third_party/pdfium/fpdfsdk/javascript/Field.cpp:3262
    #7 0x5606a310a9a7 in void JSMethod<Field, &Field::setFocus>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) third_party/pdfium/fpdfsdk/javascript/JS_Define.h:158:8
    #8 0x56069ad83699 in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) v8/src/api-arguments.cc:19:3
    #9 0x560699f23b14 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::(anonymous namespace)::BuiltinArguments) v8/src/builtins.cc:5311:36
    #10 0x560699fa0e67 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins.cc:5341:5
    #11 0x7f668ba06146  (<unknown module>)
    #12 0x7f668ba6838d  (<unknown module>)
    #13 0x7f668ba42262  (<unknown module>)
    #14 0x7f668ba25d6e  (<unknown module>)
    #15 0x56069a4586f4 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>) v8/src/execution.cc:98:13
    #16 0x56069a4580cf in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:155:10
    #17 0x560699e76f09 in v8::Script::Run(v8::Local<v8::Context>) v8/src/api.cc:1871:23
    #18 0x5606a30a3c83 in FXJS_Execute(v8::Isolate*, CFX_WideString const&, FXJSErr*) third_party/pdfium/fpdfsdk/jsapi/fxjs_v8.cpp:465:25
    #19 0x5606a308639c in CJS_Runtime::Execute(CFX_WideString const&, CFX_WideString*) third_party/pdfium/fpdfsdk/javascript/cjs_runtime.cpp:224:14
    #20 0x5606a315993b in CJS_Context::RunScript(CFX_WideString const&, CFX_WideString*) third_party/pdfium/fpdfsdk/javascript/cjs_context.cpp:54:24
    #21 0x5606a2c42fe6 in CPDFSDK_ActionHandler::RunFieldJavaScript(CPDFSDK_Document*, CPDF_FormField*, CPDF_AAction::AActionType, PDFSDK_FieldAction&, CFX_WideString const&) third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:531:28
    #22 0x5606a2c43d0d in CPDFSDK_ActionHandler::ExecuteFieldAction(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_Document*, CPDF_FormField*, PDFSDK_FieldAction&, std::__1::set<CPDF_Dictionary*, std::__1::less<CPDF_Dictionary*>, std::__1::allocator<CPDF_Dictionary*> >*) third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:250:9
    #23 0x5606a2c439ae in CPDFSDK_ActionHandler::DoAction_Field(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_Document*, CPDF_FormField*, PDFSDK_FieldAction&) third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:106:10
    #24 0x5606a2c5c4da in CPDFSDK_Widget::OnAAction(CPDF_AAction::AActionType, PDFSDK_FieldAction&, CPDFSDK_PageView*) third_party/pdfium/fpdfsdk/fsdk_baseform.cpp:1897:28
    #25 0x5606a2e3c9a7 in CFFL_IFormFiller::OnKillFocus(CPDFSDK_Annot*, unsigned int) third_party/pdfium/fpdfsdk/formfiller/cffl_iformfiller.cpp:480:18
    #26 0x5606a2c768ee in CPDFSDK_BFAnnotHandler::OnKillFocus(CPDFSDK_Annot*, unsigned int) third_party/pdfium/fpdfsdk/fsdk_annothandler.cpp:733:29
    #27 0x5606a2c73fb2 in CPDFSDK_AnnotHandlerMgr::Annot_OnKillFocus(CPDFSDK_Annot*, unsigned int) third_party/pdfium/fpdfsdk/fsdk_annothandler.cpp:325:27
    #28 0x5606a2c6e0a0 in CPDFSDK_Document::KillFocusAnnot(unsigned int) third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:436:24
    #29 0x5606a2c6d67e in KillFocusAnnot third_party/pdfium/fpdfsdk/include/fsdk_mgr.h:554:23
    #30 0x5606a2c6d67e in KillFocusAnnotIfNeeded third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:631
    #31 0x5606a2c6d67e in CPDFSDK_Document::RemovePageView(CPDF_Page*) third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:360
    #32 0x5606970c1af2 in chrome_pdf::PDFiumPage::Unload() pdf/pdfium/pdfium_page.cc:110:7

previously allocated by thread T0 (chrome) here:
    #0 0x5606964a6c3b in operator new(unsigned long) (/home/chamal/programs/chrome-asan-prebuilts/asan-linux-beta-53.0.2785.46/chrome+0x2a71c3b)
    #1 0x5606a2c359d8 in FPDF_LoadPage third_party/pdfium/fpdfsdk/fpdfview.cpp:525:22
    #2 0x5606970c1cec in chrome_pdf::PDFiumPage::GetPage() pdf/pdfium/pdfium_page.cc:123:13
    #3 0x5606a2c6c96e in FFI_GetPage third_party/pdfium/fpdfsdk/include/fsdk_mgr.h:109:14
    #4 0x5606a2c6c96e in CPDFSDK_Document::GetPageView(int) third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:289
    #5 0x5606a2c5cf16 in CPDFSDK_InterForm::GetWidget(CPDF_FormControl*) const third_party/pdfium/fpdfsdk/fsdk_baseform.cpp:2058:28
    #6 0x5606a30edeb5 in Field::setFocus(IJS_Context*, std::__1::vector<CJS_Value, std::__1::allocator<CJS_Value> > const&, CJS_Value&, CFX_WideString&) third_party/pdfium/fpdfsdk/javascript/Field.cpp:3258:27
    #7 0x5606a310a9a7 in void JSMethod<Field, &Field::setFocus>(char const*, char const*, v8::FunctionCallbackInfo<v8::Value> const&) third_party/pdfium/fpdfsdk/javascript/JS_Define.h:158:8
    #8 0x56069ad83699 in v8::internal::FunctionCallbackArguments::Call(void (*)(v8::FunctionCallbackInfo<v8::Value> const&)) v8/src/api-arguments.cc:19:3
    #9 0x560699f23b14 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::(anonymous namespace)::BuiltinArguments) v8/src/builtins.cc:5311:36
    #10 0x560699fa0e67 in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments, v8::internal::Isolate*) v8/src/builtins.cc:5341:5
    #11 0x7f668ba06146  (<unknown module>)
    #12 0x7f668ba6816d  (<unknown module>)
    #13 0x7f668ba42262  (<unknown module>)
    #14 0x7f668ba25d6e  (<unknown module>)
    #15 0x56069a4586f4 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, bool, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, v8::internal::Handle<v8::internal::Object>) v8/src/execution.cc:98:13
    #16 0x56069a4580cf in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) v8/src/execution.cc:155:10
    #17 0x560699e76f09 in v8::Script::Run(v8::Local<v8::Context>) v8/src/api.cc:1871:23
    #18 0x5606a30a3c83 in FXJS_Execute(v8::Isolate*, CFX_WideString const&, FXJSErr*) third_party/pdfium/fpdfsdk/jsapi/fxjs_v8.cpp:465:25
    #19 0x5606a308639c in CJS_Runtime::Execute(CFX_WideString const&, CFX_WideString*) third_party/pdfium/fpdfsdk/javascript/cjs_runtime.cpp:224:14
    #20 0x5606a315993b in CJS_Context::RunScript(CFX_WideString const&, CFX_WideString*) third_party/pdfium/fpdfsdk/javascript/cjs_context.cpp:54:24
    #21 0x5606a2c42790 in RunDocumentOpenJavaScript third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:549:28
    #22 0x5606a2c42790 in CPDFSDK_ActionHandler::DoAction_JavaScript(CPDF_Action const&, CFX_WideString, CPDFSDK_Document*) third_party/pdfium/fpdfsdk/fsdk_actionhandler.cpp:36
    #23 0x5606a2c6ce0d in CPDFSDK_Document::ProcJavascriptFun() third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:307:34
    #24 0x56069709c153 in chrome_pdf::PDFiumEngine::FinishLoadingDocument() pdf/pdfium/pdfium_engine.cc:1116:3
    #25 0x5606970b1a71 in chrome_pdf::PDFiumEngine::ContinueLoadingDocument(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) pdf/pdfium/pdfium_engine.cc:2532:5
    #26 0x56069709a8d2 in chrome_pdf::PDFiumEngine::LoadDocument() pdf/pdfium/pdfium_engine.cc:2421:5
...........

### ds...@chromium.org (2016-08-08)

Reopening as per #43

### ds...@chromium.org (2016-08-08)

I'm not seeing any issues with an ASan build on Linux with testfocus.pdf. Will try on Windows to see if it crashes there for me.

### ch...@gmail.com (2016-08-09)

dsinclair, Can you give me a link to the ASAN build that you are testing? So I can test whether there is something wrong with my local build.

Also are you testing on a larger screen where all 3 pages of pdf file are visible? Testfocus.pdf file should scroll to 3rd page (by Javascript) and 1st page should become invisible, in order for bug to reproduce.

### ds...@chromium.org (2016-08-09)

I built Chrome locally, so there is no link to download the ASan build I used. All 3 pages are not visible and it does scroll to the third page on opening the document. I don't believe the first page becomes invisible though.

I will test on Windows later this week when I have access to a Windows machine.

### sh...@chromium.org (2016-08-10)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2016-08-10)

As per comments above, there is still a crash happening.

### ch...@gmail.com (2016-08-17)

dsinclair, Does not crash in chrome version 54.0.2831.0.

### ds...@chromium.org (2016-08-17)

Marking as fixed as per #50. I'm guessing this was fixed by https://pdfium.googlesource.com/pdfium.git/+/ef523dd36aea991084b8b934df846014a5c09c6f

### aw...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/630654?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084924)*
