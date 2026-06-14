# Security: Stack-buffer-overflow in (anonymous namespace)::CalculateString

| Field | Value |
|-------|-------|
| **Issue ID** | [40086199](https://issues.chromium.org/issues/40086199) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | sw...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2016-12-12 |
| **Bounty** | $1,000.00 |

## Description

# **VULNERABILITY DETAILS** Rendering PDF file ../poc.pdf.

==19631==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7f901d33a25f at pc 0x7f916a0838ff bp 0x7ffcad0d5630 sp 0x7ffcad0d5628  

READ of size 16 at 0x7f901d33a25f thread T0  

#0 0x7f916a0838fe in std::\_\_1::ctype<char>::do\_widen(char const\*, char const\*, char\*) const buildtools/third\_party/libc++/trunk/src/locale.cpp:996:17  

#1 0x7f916a00e679 in widen buildtools/third\_party/libc++/trunk/include/\_\_locale:609:16  

#2 0x7f916a00e679 in std::\_\_1::\_\_num\_put<char>::\_\_widen\_and\_group\_float(char\*, char\*, char\*, char\*, char\*&, char\*&, std::\_\_1::locale const&) buildtools/third\_party/libc++/trunk/include/locale:1345  

#3 0x7f916a00c608 in std::\_\_1::num\_put<char, std::\_\_1::ostreambuf\_iterator<char, std::\_\_1::char\_traits<char> > >::do\_put(std::\_\_1::ostreambuf\_iterator<char, std::\_\_1::char\_traits<char> >, std::\_\_1::ios\_base&, char, double) const buildtools/third\_party/libc++/trunk/include/locale:1729:5  

#4 0x7f9169fbab78 in put buildtools/third\_party/libc++/trunk/include/locale:1408:16  

#5 0x7f9169fbab78 in std::\_\_1::basic\_ostream<char, std::\_\_1::char\_traits<char> >::operator<<(double) buildtools/third\_party/libc++/trunk/include/ostream:677  

#6 0x34f14ba in (anonymous namespace)::CalculateString(double, int, int\*, bool\*) third\_party/pdfium/fpdfsdk/javascript/PublicMethods.cpp:99:47  

#7 0x34eedfc in CJS\_PublicMethods::AFNumber\_Format(IJS\_Context\*, std::\_\_1::vector<CJS\_Value, std::\_\_1::allocator<CJS\_Value> > const&, CJS\_Value&, CFX\_WideString&) third\_party/pdfium/fpdfsdk/javascript/PublicMethods.cpp:793:14  

#8 0x34fedbb in void JSGlobalFunc<&CJS\_PublicMethods::AFNumber\_Format>(char const\*, v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) third\_party/pdfium/fpdfsdk/javascript/JS\_Define.h:450:8  

#9 0x522b7b in v8::internal::FunctionCallbackArguments::Call(void (\*)(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&)) v8/src/api-arguments.cc:19:3  

#10 0x740f1c in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::BuiltinArguments) v8/src/builtins/builtins-api.cc:106:36  

#11 0x73db65 in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:135:5  

#12 0x7f8ff8f04426 (<unknown module>)  

#13 0x7f8ff9004ad0 (<unknown module>)  

#14 0x7f8ff8f9f7c2 (<unknown module>)  

#15 0x7f8ff8f38080 (<unknown module>)  

#16 0x1416738 in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate\*, bool, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);)) v8/src/execution.cc:139:13  

#17 0x1415f03 in v8::internal::Execution::Call(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*) v8/src/execution.cc:176:10  

#18 0x542718 in v8::Script::Run(v8::Local[v8::Context](javascript:void(0);)) v8/src/api.cc:1984:7  

#19 0x352e374 in CFXJS\_Engine::Execute(CFX\_WideString const&, FXJSErr\*) third\_party/pdfium/fxjs/fxjs\_v8.cpp:469:25  

#20 0x340f46a in CJS\_Runtime::ExecuteScript(CFX\_WideString const&, CFX\_WideString\*) third\_party/pdfium/fpdfsdk/javascript/cjs\_runtime.cpp:206:14  

#21 0x3526b63 in CJS\_Context::RunScript(CFX\_WideString const&, CFX\_WideString\*) third\_party/pdfium/fpdfsdk/javascript/cjs\_context.cpp:48:24  

#22 0x2d499a4 in CPDFSDK\_InterForm::OnFormat(CPDF\_FormField\*, bool&) third\_party/pdfium/fpdfsdk/cpdfsdk\_interform.cpp:302:31  

#23 0x2d6d44f in CPDFSDK\_Widget::OnFormat(bool&) third\_party/pdfium/fpdfsdk/cpdfsdk\_widget.cpp:796:24  

#24 0x2d8c64b in CPDFSDK\_WidgetHandler::OnLoad(CPDFSDK\_Annot\*) third\_party/pdfium/fpdfsdk/cpdfsdk\_widgethandler.cpp:233:38  

#25 0x2d54680 in CPDFSDK\_PageView::LoadFXAnnots() third\_party/pdfium/fpdfsdk/cpdfsdk\_pageview.cpp:440:23  

#26 0x2d433d5 in CPDFSDK\_FormFillEnvironment::GetPageView(CPDF\_Page\*, bool) third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:586:14  

#27 0x2d350e8 in FormHandleToPageView third\_party/pdfium/fpdfsdk/fpdfformfill.cpp:58:39  

#28 0x2d350e8 in FORM\_OnAfterLoadPage third\_party/pdfium/fpdfsdk/fpdfformfill.cpp:658  

#29 0x4ffbc9 in GetPageForIndex(\_FPDF\_FORMFILLINFO\*, void\*, int) third\_party/pdfium/samples/pdfium\_test.cc:590:3  

#30 0x50072c in RenderPage(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, void\*, void\*&, FPDF\_FORMFILLINFO\_PDFiumTest&, int, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) third\_party/pdfium/samples/pdfium\_test.cc:604:20  

#31 0x502d12 in RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) third\_party/pdfium/samples/pdfium\_test.cc:820:9  

#32 0x504523 in main third\_party/pdfium/samples/pdfium\_test.cc:955:5  

#33 0x7f9168d4582f in \_\_libc\_start\_main (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

Address 0x7f901d33a25f is located in stack of thread T0 at offset 95 in frame  

#0 0x7f916a00becf in std::\_\_1::num\_put<char, std::\_\_1::ostreambuf\_iterator<char, std::\_\_1::char\_traits<char> > >::do\_put(std::\_\_1::ostreambuf\_iterator<char, std::\_\_1::char\_traits<char> >, std::\_\_1::ios\_base&, char, double) const buildtools/third\_party/libc++/trunk/include/locale:1672

This frame has 7 object(s):  

[32, 40) '\_\_fmt'  

[64, 94) '\_\_nar' <== Memory access at offset 95 overflows this variable  

[128, 136) '\_\_nb'  

[160, 217) '\_\_o'  

[256, 264) '\_\_op'  

[288, 296) '\_\_oe'  

[320, 328) 'ref.tmp54'  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext  

(longjmp and C++ exceptions \*are\* supported)  

SUMMARY: AddressSanitizer: stack-buffer-overflow buildtools/third\_party/libc++/trunk/src/locale.cpp:996:17 in std::\_\_1::ctype<char>::do\_widen(char const\*, char const\*, char\*) const  

Shadow bytes around the buggy address:  

0x0ff283a5f3f0: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff283a5f400: f1 f1 f1 f1 00 00 00 f2 f2 f2 f2 f2 00 00 00 00  

0x0ff283a5f410: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff283a5f420: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 f2  

0x0ff283a5f430: f2 f2 f2 f2 f2 f2 f2 f2 00 00 00 f3 f3 f3 f3 f3  

=>0x0ff283a5f440: f1 f1 f1 f1 00 f2 f2 f2 00 00 00[06]f2 f2 f2 f2  

0x0ff283a5f450: 00 f2 f2 f2 00 00 00 00 00 00 00 01 f2 f2 f2 f2  

0x0ff283a5f460: 00 f2 f2 f2 00 f2 f2 f2 00 f3 f3 f3 00 00 00 00  

0x0ff283a5f470: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff283a5f480: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x0ff283a5f490: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

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

==19631==ABORTING

**VERSION**  

Chrome Version: asan-linux-release-437664  

Operating System:

- Ubuntu 16.04.1 LTS 64bit (Server)
- Linux ubuntu 4.4.0-53-generic #74-Ubuntu SMP Fri Dec 2 15:59:10 UTC 2016 x86\_64 x86\_64 x86\_64 GNU/Linux

**REPRODUCTION CASE**

- ./pdfium\_test ./poc.pdf

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 15.6 KB)

## Timeline

### cl...@chromium.org (2016-12-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4776053236301824

### ts...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### wr...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF Internals>Skia>PDF]

### sh...@chromium.org (2016-12-13)

[Empty comment from Monorail migration]

### ds...@chromium.org (2016-12-13)

https://codereview.chromium.org/2572543004/

### bu...@chromium.org (2016-12-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/992ecf7c189e5cabf43e5ad862511cf63d030966

commit 992ecf7c189e5cabf43e5ad862511cf63d030966
Author: dsinclair <dsinclair@chromium.org>
Date: Wed Dec 14 13:45:57 2016

Verify precision length before converting to string.

This CL updates the CalculateString method to make sure the number of digits
of precision is valid before doing the stringstream conversion.

BUG=chromium:673336

Review-Url: https://codereview.chromium.org/2572543004

[modify] https://crrev.com/992ecf7c189e5cabf43e5ad862511cf63d030966/fpdfsdk/javascript/PublicMethods.cpp


### ds...@chromium.org (2016-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d44f4e2d1968eba9b3f9bd15f5cc2f5d39deddbf

commit d44f4e2d1968eba9b3f9bd15f5cc2f5d39deddbf
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Wed Dec 14 15:12:25 2016

Roll src/third_party/pdfium/ 974b4a6c4..a9caab94c (2 commits).

https://pdfium.googlesource.com/pdfium.git/+log/974b4a6c4bce..a9caab94c1f1

$ git log 974b4a6c4..a9caab94c --date=short --no-merges --format='%ad %ae %s'
2016-12-14 tsepez Avoid the ptr.reset(new XXX()) anti-pattern
2016-12-14 dsinclair Verify precision length before converting to string.

BUG=673336

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2574833003
Cr-Commit-Position: refs/heads/master@{#438517}

[modify] https://crrev.com/d44f4e2d1968eba9b3f9bd15f5cc2f5d39deddbf/DEPS


### cl...@chromium.org (2016-12-15)

ClusterFuzz has detected this issue as fixed in range 438516:438537.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4776053236301824

Job Type: linux_asan_pdfium
Crash Type: Stack-buffer-overflow READ 16
Crash Address: 0x7fe726a8e65f
Crash State:
  CalculateString
  CJS_PublicMethods::AFNumber_Format
  void JSGlobalFunc<&CJS_PublicMethods::AFNumber_Format>
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=432285:432416
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=438516:438537

Minimized Testcase (15.61 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95tjnHF445bTMSF1c2yM9jdt-mxgpuqqsG2lN-QqgX_42wHczzpjt3CKEHUlImjbHRxvxb__IAbSsltnPkAlVFMG5wojgyWIERKBwK8sA8UTTWQogrB51vXLBJU02uVt6Vr67rQtlFliTNQiqG9TlXSv5-7Eg?testcase_id=4776053236301824

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### aw...@google.com (2016-12-19)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-19)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-12-19)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### aw...@google.com (2016-12-19)

[Empty comment from Monorail migration]

### bu...@google.com (2016-12-21)

LGTM, approving for merge into M56

### sh...@chromium.org (2016-12-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-12-28)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Skia>PDF]

### sh...@chromium.org (2016-12-29)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-01-09)

[Empty comment from Monorail migration]

### aw...@google.com (2017-01-10)

The panel decided to award $1,000 for this report, but noted they would reconsider for a higher amount if it can be shown this bug leads to memory corruption

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-01-10)

[Empty comment from Monorail migration]

### bu...@google.com (2017-01-10)

Per discussion this should be merged to M56 (build 2924) now.

### sh...@chromium.org (2017-03-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-03-23)

This issue was migrated from crbug.com/chromium/673336?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086199)*
