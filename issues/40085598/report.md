# Security: Heap-use-after-free in Field::UpdateFormField

| Field | Value |
|-------|-------|
| **Issue ID** | [40085598](https://issues.chromium.org/issues/40085598) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2016-10-05 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

This is a variation of <https://crbug.com/chromium/632709>. This bug happens because of below mentioned code in Field::UpdateFormField method.

std::vector<CPDFSDK\_Widget\*> widgets;  

pInterForm->GetWidgets(pFormField, &widgets);  

int nFieldType = pFormField->GetFieldType();  

if (nFieldType == FIELDTYPE\_COMBOBOX || nFieldType == FIELDTYPE\_TEXTFIELD) {  

for (CPDFSDK\_Annot\* pAnnot : widgets) {  

FX\_BOOL bFormatted = FALSE;  

CPDFSDK\_Annot::ObservedPtr pObserved(pAnnot);  

CFX\_WideString sValue =  

static\_cast<CPDFSDK\_Widget\*>(pObserved.Get())->OnFormat(bFormatted);  

if (pObserved) {  

static\_cast<CPDFSDK\_Widget\*>(pObserved.Get())  

->ResetAppearance(bFormatted ? &sValue : nullptr, FALSE);  

}  

}  

.......

Fix for <https://crbug.com/chromium/632709> introduced ObservedPtr to prevent a deleted single object being used again. But it is not sufficient when there are multiple CPDFSDK\_Annot objects with same name. All CPDFSDK\_Annot objects can be deleted through call to  

static\_cast<CPDFSDK\_Widget\*>(pObserved.Get())->OnFormat(bFormatted);.  

Then next iteration of for loop will use deleted CPDFSDK\_Annot object.

**VERSION**  

Chrome Version: [53.0.2785.143] + [stable]  

[55.0.2882.0] + [TOT]

Operating System: [Ubuntu 16.04, Windows 10]

**REPRODUCTION CASE**

1. Open testcase.pdf with chrome.
2. Wait 6 seconds
3. PDF plugin process will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [PDF plugin process]  

Crash State: Address Sanitizer Output

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x607000018210 at pc 0x561332df3073 bp 0x7fff0decc190 sp 0x7fff0decc188  

READ of size 8 at 0x607000018210 thread T0 (chrome)  

#0 0x561332df3072 in \_\_root ./out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:877:65  

#1 0x561332df3072 in \_\_find\_equal<CFX\_Observable<CPDFSDK\_Annot>::ObservedPtr \*> ./out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1597:0  

#2 0x561332df3072 in \_\_insert\_unique ./out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1856:0  

#3 0x561333285fab in insert ./out/asan/../../buildtools/third\_party/libc++/trunk/include/set:602:25  

#4 0x561333285fab in AddObservedPtr ./out/asan/../../third\_party/pdfium/core/fxcrt/cfx\_observable.h:58:0  

#5 0x561333285fab in ObservedPtr ./out/asan/../../third\_party/pdfium/core/fxcrt/cfx\_observable.h:21:0  

#6 0x561333285fab in UpdateFormField ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:276:0  

#7 0x561333287846 in SetBorderStyle ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:520:9  

#8 0x5613332870ea in borderStyle ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:443:7  

#9 0x56133329f7d2 in JSPropSetter<Field, &Field::borderStyle> ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/JS\_Define.h:114:8  

#10 0x5613262a677f in Call ./out/asan/../../v8/src/api-arguments-inl.h:131:3  

#11 0x56132643b4cb in SetPropertyWithAccessor ./out/asan/../../v8/src/objects.cc:1435:10  

#12 0x561326471c58 in SetPropertyInternal ./out/asan/../../v8/src/objects.cc:4679:16  

#13 0x561326470d70 in SetProperty ./out/asan/../../v8/src/objects.cc:4711:9  

#14 0x56132627a3f9 in Store ./out/asan/../../v8/src/ic/ic.cc:1573:3  

#15 0x56132628f583 in \_\_RT\_impl\_Runtime\_StoreIC\_Miss ./out/asan/../../v8/src/ic/ic.cc:2423:5  

#16 0x56132628f583 in Runtime\_StoreIC\_Miss ./out/asan/../../v8/src/ic/ic.cc:2408:0  

#11 0x7fa6d5f043a6 (<unknown module>)  

#12 0x7fa6d6005233 (<unknown module>)  

#13 0x7fa6d6005053 (<unknown module>)  

#14 0x7fa6d5f52be2 (<unknown module>)  

#15 0x7fa6d5f2c320 (<unknown module>)  

#17 0x56132605c40a in Invoke ./out/asan/../../v8/src/execution.cc:139:13  

#18 0x56132605bbb2 in Call ./out/asan/../../v8/src/execution.cc:176:10  

#19 0x56132560cc6b in Run ./out/asan/../../v8/src/api.cc:1865:7  

#20 0x56133330141a in Execute ./out/asan/../../third\_party/pdfium/fxjs/fxjs\_v8.cpp:477:25  

#21 0x5613332302bc in ?? ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_runtime.cpp:241:14  

#22 0x5613332fbeea in RunScript ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_context.cpp:52:24  

#23 0x5613332e8516 in RunJsScript ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/app.cpp:615:15  

#24 0x5613332e8516 in TimerProc ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/app.cpp:603:0  

.............

0x607000018210 is located 16 bytes inside of 80-byte region [0x607000018200,0x607000018250)  

freed by thread T0 (chrome) here:  

#0 0x561324be335b in operator delete(void\*) ??:?  

#1 0x561332dfcc4f in ~CPDFSDK\_PageView ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_pageview.cpp:71:23  

#2 0x561332df1d2e in RemovePageView ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:157:3  

#3 0x561328dc4bf2 in Unload ./out/asan/../../pdf/pdfium/pdfium\_page.cc:112:7  

#4 0x561328d98cba in CalculateVisiblePages ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:2650:20  

#5 0x561328db2a1d in GetMostVisiblePage ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:2290:3  

#6 0x561328d95594 in Form\_GetCurrentPage ./out/asan/../../pdf/pdfium/pdfium\_engine.cc:3502:21  

#7 0x561332df126f in ?? ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:69:38  

#8 0x561333259bec in pageNum ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Document.cpp:220:52  

#9 0x56133326d8ee in JSPropGetter<Document, &Document::pageNum> ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/JS\_Define.h:89:8  

#10 0x5613262a7467 in Call ./out/asan/../../v8/src/api-arguments-inl.h:32:1  

#11 0x561326433e95 in GetPropertyWithAccessor ./out/asan/../../v8/src/objects.cc:1352:34  

#12 0x5613264318fa in GetProperty ./out/asan/../../v8/src/objects.cc:998:16  

#13 0x5613268c0e6c in GetObjectProperty ./out/asan/../../v8/src/runtime/runtime-object.cc:34:32  

#14 0x5613268ca1ea in \_\_RT\_impl\_Runtime\_GetProperty ./out/asan/../../v8/src/runtime/runtime-object.cc:345:3  

#15 0x5613268ca1ea in Runtime\_GetProperty ./out/asan/../../v8/src/runtime/runtime-object.cc:338:0  

#15 0x7fa6d5f043a6 (<unknown module>)  

#16 0x7fa6d600470e (<unknown module>)  

#17 0x7fa6d5f52be2 (<unknown module>)  

#18 0x7fa6d5f2c320 (<unknown module>)  

#16 0x56132605c40a in Invoke ./out/asan/../../v8/src/execution.cc:139:13  

#17 0x56132605bbb2 in Call ./out/asan/../../v8/src/execution.cc:176:10  

#18 0x56132560cc6b in Run ./out/asan/../../v8/src/api.cc:1865:7  

#19 0x56133330141a in Execute ./out/asan/../../third\_party/pdfium/fxjs/fxjs\_v8.cpp:477:25  

#20 0x5613332302bc in ?? ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_runtime.cpp:241:14  

#21 0x5613332fbeea in RunScript ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/cjs\_context.cpp:52:24  

#22 0x561332df74c9 in OnFormat ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_interform.cpp:314:34  

#23 0x561332e132e9 in OnFormat ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_widget.cpp:802:24  

#24 0x561333285fc9 in UpdateFormField ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:278:60  

#25 0x561333287846 in SetBorderStyle ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:520:9  

#26 0x5613332870ea in borderStyle ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:443:7

previously allocated by thread T0 (chrome) here:  

#0 0x561324be271b in operator new(unsigned long) ??:?  

#1 0x561332e2881a in NewAnnot ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_widgethandler.cpp:64:29  

#2 0x561332dff0a9 in LoadFXAnnots ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_pageview.cpp:506:47  

#3 0x561332df0cbf in GetPageView ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:63:14  

#4 0x561332de3d43 in FormHandleToPageView ./out/asan/../../third\_party/pdfium/fpdfsdk/fpdfformfill.cpp:57:29  

#5 0x561332de3d43 in FORM\_OnAfterLoadPage ./out/asan/../../third\_party/pdfium/fpdfsdk/fpdfformfill.cpp:650:0  

#6 0x561328dc4e42 in GetPage ./out/asan/../../pdf/pdfium/pdfium\_page.cc:127:7  

#7 0x561332df12fb in GetPageView ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_document.cpp:75:38  

#8 0x561332df59ff in GetWidget ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_interform.cpp:113:28  

#9 0x561332df5f12 in GetWidgets ./out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_interform.cpp:138:31  

#10 0x5613332861ad in UpdateFormField ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:296:17  

#11 0x56133329a7b9 in SetValue ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:2778:11  

#12 0x561333299bb1 in value ./out/asan/../../third\_party/pdfium/fpdfsdk/javascript/Field.cpp:2674:7  

......................

## Attachments

- [testcase.pdf](attachments/testcase.pdf) (application/pdf, 3.4 KB)

## Timeline

### ch...@gmail.com (2016-10-05)

* Fix for https://crbug.com/chromium/632709 is not yet merged to stable chrome version 53.0.2785.143. So this test case crash stable version due to https://crbug.com/chromium/632709. That crash happens before next iteration of for loop in Field::UpdateFormField which is the reason mentioned in this bug.

### cl...@chromium.org (2016-10-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5551157751840768

### ts...@chromium.org (2016-10-05)

[Empty comment from Monorail migration]

### ts...@chromium.org (2016-10-05)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### sh...@chromium.org (2016-10-06)

[Empty comment from Monorail migration]

### ds...@chromium.org (2016-10-12)

The relevant bit of javascript:

  function movePage() {
    this.pageNum = 2;
  }

  function test() {
    this.getField('cmb1').value = 'two';
    this.getField('cmb1').borderStyle = 'dashed';
  }

  app.setTimeOut('movePage()',3000);
  app.setTimeOut('test()',6000);




### ds...@chromium.org (2016-10-12)

When we execute the OnFormat call we'll end up executing javascript attached to the node. That javascript does n = this.pageNum. This will force a call out to the embedder to calculate the current page number.

In Chromium, this call will |CalculateVisiblePages|. Part of calculate visible pages is to cleanup pages which aren't currently onscreen. In this case, the page we're working with has been moved off screen, so Chromium cleans up the page, but we're currently working with the page, so when we get back to the calling code the page object and all its annotations have been deleted by the page unload.

### ds...@chromium.org (2016-10-12)

CL up for review: https://codereview.chromium.org/2418533002/

### ds...@chromium.org (2016-10-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bf6a6765d44b09c64b8c75d749efb84742a250e7

commit bf6a6765d44b09c64b8c75d749efb84742a250e7
Author: dsinclair <dsinclair@chromium.org>
Date: Wed Oct 12 17:36:50 2016

[pdf] Defer page unloading in JS callback.

One of the callbacks from PDFium JavaScript into the embedder is to get the
current page number. In Chromium, this will trigger a call to
CalculateMostVisiblePage that method will determine the visible pages and unload
any non-visible pages. But, if the originating JS is on a non-visible page
we'll delete the page and annotations associated with that page. This will
cause issues as we are currently working with those objects when the JavaScript
returns.

This Cl defers the page unloading triggered by getting the most visible page
until the next event is handled by the Chromium embedder.

BUG=chromium:653090

Review-Url: https://codereview.chromium.org/2418533002
Cr-Commit-Position: refs/heads/master@{#424781}

[modify] https://crrev.com/bf6a6765d44b09c64b8c75d749efb84742a250e7/pdf/pdfium/pdfium_engine.cc


### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-21)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-10-21)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### aw...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-24)

Congratulations, the panel has awarded $3,000 for this report.  Cheers!

### aw...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### th...@chromium.org (2016-10-24)

Will merge.

### bu...@chromium.org (2016-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ff05b41fda6ab437bd48d7eaaaf538bf7a60479a

commit ff05b41fda6ab437bd48d7eaaaf538bf7a60479a
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Oct 24 20:33:44 2016

M55: [pdf] Defer page unloading in JS callback.

One of the callbacks from PDFium JavaScript into the embedder is to get the
current page number. In Chromium, this will trigger a call to
CalculateMostVisiblePage that method will determine the visible pages and unload
any non-visible pages. But, if the originating JS is on a non-visible page
we'll delete the page and annotations associated with that page. This will
cause issues as we are currently working with those objects when the JavaScript
returns.

This Cl defers the page unloading triggered by getting the most visible page
until the next event is handled by the Chromium embedder.

BUG=chromium:653090

Review-Url: https://codereview.chromium.org/2418533002
Cr-Commit-Position: refs/heads/master@{#424781}
(cherry picked from commit bf6a6765d44b09c64b8c75d749efb84742a250e7)

Review URL: https://codereview.chromium.org/2446613003 .

Cr-Commit-Position: refs/branch-heads/2883@{#256}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/ff05b41fda6ab437bd48d7eaaaf538bf7a60479a/pdf/pdfium/pdfium_engine.cc


### aw...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ff05b41fda6ab437bd48d7eaaaf538bf7a60479a

commit ff05b41fda6ab437bd48d7eaaaf538bf7a60479a
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Oct 24 20:33:44 2016

M55: [pdf] Defer page unloading in JS callback.

One of the callbacks from PDFium JavaScript into the embedder is to get the
current page number. In Chromium, this will trigger a call to
CalculateMostVisiblePage that method will determine the visible pages and unload
any non-visible pages. But, if the originating JS is on a non-visible page
we'll delete the page and annotations associated with that page. This will
cause issues as we are currently working with those objects when the JavaScript
returns.

This Cl defers the page unloading triggered by getting the most visible page
until the next event is handled by the Chromium embedder.

BUG=chromium:653090

Review-Url: https://codereview.chromium.org/2418533002
Cr-Commit-Position: refs/heads/master@{#424781}
(cherry picked from commit bf6a6765d44b09c64b8c75d749efb84742a250e7)

Review URL: https://codereview.chromium.org/2446613003 .

Cr-Commit-Position: refs/branch-heads/2883@{#256}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/ff05b41fda6ab437bd48d7eaaaf538bf7a60479a/pdf/pdfium/pdfium_engine.cc


### di...@google.com (2016-11-04)

[Automated comment] removing mislabelled merge-merged-2840

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/653090?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085598)*
