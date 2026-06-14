# Heap-use-after-free in CPDF_ImageObject::~CPDF_ImageObject

| Field | Value |
|-------|-------|
| **Issue ID** | [40080450](https://issues.chromium.org/issues/40080450) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | ju...@foxitsoftware.com |
| **Created** | 2014-09-13 |
| **Bounty** | $2,000.00 |

## Description


Tested on:

OS: Ubuntu 12.04

Chromium: 39.0.2157.0 (Developer Build 67548025123b035f4beacfea3d948e1a1b8eba5b-refs/heads/master@{#294624})

You have to load the pdf into Chrome and refresh the tab to reproduce the issue.

ASAN-report:

==21750==ERROR: AddressSanitizer: heap-use-after-free on address 0x60700001cc10 at pc 0x000000581cb7 bp 0x7fff9b774300 sp 0x7fff9b7742f8
READ of size 4 at 0x60700001cc10 thread T0
    #0 0x581cb6 in CPDF_Image::IsInline() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/../../../include/fpdfapi/fpdf_resource.h:859
    #1 0x581b87 in CPDF_ImageObject::~CPDF_ImageObject() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_image.cpp:20
    #2 0x581d7a in CPDF_ImageObject::~CPDF_ImageObject() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_image.cpp:16
    #3 0x561167 in CPDF_Form::~CPDF_Form() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page.cpp:696
    #4 0x598a34 in CPDF_TilingPattern::~CPDF_TilingPattern() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_pattern.cpp:38
    #5 0x598a9a in CPDF_TilingPattern::~CPDF_TilingPattern() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_pattern.cpp:36
    #6 0x56f5d3 in CPDF_DocPageData::Clear(int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:232
.
.
.
0x60700001cc10 is located 32 bytes inside of 80-byte region [0x60700001cbf0,0x60700001cc40)
freed by thread T0 here:
    #0 0x4a791b in free ??:0
    #1 0x56ef4d in CPDF_DocPageData::Clear(int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:175
    #2 0x571b89 in CPDF_DocPageData::~CPDF_DocPageData() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:149
    #3 0x56eb5a in CPDF_PageModule::ReleaseDoc(CPDF_Document*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:70
    #4 0x59ff08 in CPDF_Document::~CPDF_Document() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_document.cpp:102
    #5 0x5a9c29 in CPDF_Parser::CloseParser(int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:76
    #6 0x5a9a6e in CPDF_Parser::~CPDF_Parser() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:61
.
.
.
previously allocated by thread T0 here:
    #0 0x4a7b9b in malloc ??:0
    #1 0x5714b8 in CPDF_DocPageData::GetImage(CPDF_Object*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:528
    #2 0x588245 in CPDF_StreamContentParser::AddImage(CPDF_Stream*, CPDF_Image*, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_parser.cpp:851
    #3 0x587f9c in CPDF_StreamContentParser::Handle_ExecuteXObject() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_parser.cpp:736
    #4 0x58486d in CPDF_StreamContentParser::OnOperator(char const*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_parser.cpp:380
    #5 0x58f193 in CPDF_StreamContentParser::Parse(unsigned char const*, unsigned int, unsigned int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_parser_old.cpp:52
.
.
.


## Attachments

- [chrome-heap-use-after-free-CPDFImageIsInline9.pdf](attachments/chrome-heap-use-after-free-CPDFImageIsInline9.pdf) (application/pdf, 952.8 KB)
- [foo.cc](attachments/foo.cc) (application/octet-stream, 422 B)

## Timeline

### aa...@google.com (2014-09-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-15)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5104550651363328

### bo...@foxitsoftware.com (2014-09-15)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-09-15)

@thestig, can you help to look at the this issue? Seems PDFiumEngine() is destructed twice. So how does the "src/pdf" code process "refresh"?

### bo...@foxitsoftware.com (2014-09-15)

414097 is a similar one.

### cl...@chromium.org (2014-09-15)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5104550651363328

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60d0000af560
Crash State:
  CPDF_ImageObject::~CPDF_ImageObject
  CPDF_ImageObject::~CPDF_ImageObject
  CPDF_PageObjects::~CPDF_PageObjects
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=294200:294571

Minimized Testcase (952.85 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94OjfSRARuUeoAIgGhRAxnt1AELRi3mh8yygIztD2oU8Ps57iRJo1z4Al4zMp3iz3fTWjTdZ_QAe0mkHsQg8MuYXl_NyBk4FReR3TqEWIjm8C6BGS0jPNm_9NuABLDqk0O9ZSyDoj8SONZgbD5Yx5klj5cyuFl0s5BnseaUhEnfqKjAMNw



### cl...@chromium.org (2014-09-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### th...@chromium.org (2014-09-17)

re: "double free"

There's no double free. PDFiumEngine has multiple destructors calling each other. Take the attached example, compile it with g++, and then run it in gdb with a breakpoint set at Foo::~Foo. You'll notice you hit the breakpoint twice even though there's no double free.

BTW, the stack trace locally is as follow. The line numbers may be off by a bit due to local changes.

#0  CPDF_Object::Release (this=0xcdcdcdcdcdcdcdcd)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_objects.cpp:10
#1  0x00007fffe7df4b83 in CPDF_Image::~CPDF_Image (this=0x7d4e9316e30)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_image.cpp:89
#2  0x00007fffe7df4521 in CPDF_ImageObject::~CPDF_ImageObject (this=0x7d4e9304bd0)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_image.cpp:21
#3  0x00007fffe7df45a9 in CPDF_ImageObject::~CPDF_ImageObject (this=0x7d4e9304bd0)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_image.cpp:16
#4  0x00007fffe7ddde7e in CPDF_PageObject::Release (this=0x7d4e9304bd0)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page.cpp:12
#5  0x00007fffe7de0e49 in CPDF_PageObjects::~CPDF_PageObjects (this=0x7d4e91b84a0)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page.cpp:696
#6  0x00007fffe7de1ea5 in CPDF_Form::~CPDF_Form (this=0x7d4e91b84a0)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page.cpp:956
#7  0x00007fffe7e019f4 in CPDF_TilingPattern::~CPDF_TilingPattern (this=0x7d4e9304d30)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_pattern.cpp:38
#8  0x00007fffe7e01a39 in CPDF_TilingPattern::~CPDF_TilingPattern (this=0x7d4e9304d30)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_pattern.cpp:36
#9  0x00007fffe7de9565 in CPDF_DocPageData::Clear (this=0x7d4e85d7020, bForceRelease=1)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:232
#10 0x00007fffe7deac9c in CPDF_DocPageData::~CPDF_DocPageData (this=0x7d4e85d7020)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:149
#11 0x00007fffe7de8f42 in CPDF_PageModule::ReleaseDoc (this=0x7d4e86f56e0, pDoc=0x7d4e804dd40)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_page/fpdf_page_doc.cpp:70
#12 0x00007fffe7e065b8 in CPDF_Document::~CPDF_Document (this=0x7d4e804dd40)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_document.cpp:102
#13 0x00007fffe7e141be in CPDF_Parser::CloseParser (this=0x7d4e83c4de0, bReParse=0)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:76
#14 0x00007fffe7e1409e in CPDF_Parser::~CPDF_Parser (this=0x7d4e83c4de0)
    at ../../third_party/pdfium/core/src/fpdfapi/fpdf_parser/fpdf_parser_parser.cpp:61
#15 0x00007fffe7d31f0a in FPDF_CloseDocument (document=0x7d4e804dd40)
    at ../../third_party/pdfium/fpdfsdk/src/fpdfview.cpp:598
#16 0x00007fffe7c60161 in chrome_pdf::PDFiumEngine::~PDFiumEngine (this=0x7d4e8655020)
    at ../../pdf/pdfium/pdfium_engine.cc:642
#17 0x00007fffe7c60509 in chrome_pdf::PDFiumEngine::~PDFiumEngine (this=0x7d4e8655020) 
    at ../../pdf/pdfium/pdfium_engine.cc:632
#18 0x00007fffe7c38c62 in base::DefaultDeleter<chrome_pdf::PDFEngine>::operator() (this=0x7d4e8497100, ptr=0x7d4e8655020)
    at ../../base/memory/scoped_ptr.h:137
#19 0x00007fffe7c38c1c in base::internal::scoped_ptr_impl<chrome_pdf::PDFEngine, base::DefaultDeleter<chrome_pdf::PDFEngine> >::reset (this=0x7d4e8497100, p=0x0) 
    at ../../base/memory/scoped_ptr.h:246
#20 0x00007fffe7c2784d in scoped_ptr<chrome_pdf::PDFEngine, base::DefaultDeleter<chrome_pdf::PDFEngine> >::reset (this=0x7d4e8497100, p=0x0)
    at ../../base/memory/scoped_ptr.h:367
#21 0x00007fffe7c175cd in chrome_pdf::Instance::~Instance (this=0x7d4e8496d20)
    at ../../pdf/instance.cc:316
#22 0x00007fffe7c17a99 in chrome_pdf::Instance::~Instance (this=0x7d4e8496d20)
    at ../../pdf/instance.cc:309
#23 0x00007fffe7d69aa0 in pp::Instance_DidDestroy (instance=-2045768307)
    at ../../ppapi/cpp/module.cc:89
...

### ts...@chromium.org (2014-09-17)

@bo, I don't see any evidence for a duplicate destruction of the pdfium engine. If refresh is involved, its probably because refresh causes shutdown to be run and that's where the trouble occurs.

I'd imagine that this is related to CPDF_DocPageData::Clear(FX_BOOL bForceRelease) getting called with bForceRelease == true.  It looks like there are two paths to a ref counted imageObject, one via the m_ImageMap and one the m_PatternMap through the pattern to the image.

When bForceRelease is true, it looks like we blow away all objects, ignoring reference counts.  Thus, the destructor for the pattern or the image object has to find the PageDocData, check if it is m_bForceRelease, and not destruct subordinate objects since we are counting on the top-level forced destruction to free them.

I really dislike the pattern of deleting a ref counted object other than through its ref count hitting zero.  But so long as we have it, it looks like there are perhaps several types of objects kept in maps in the DocPageData that need to honor it.

### ju...@foxitsoftware.com (2014-09-18)

[Empty comment from Monorail migration]

### ju...@foxitsoftware.com (2014-09-19)

It's pending in the review: https://codereview.chromium.org/582993002/.

### ju...@foxitsoftware.com (2014-09-19)

It has been fixed in https://pdfium.googlesource.com/pdfium/+/26019d4a79c84843c710cd9505bd40e9da0ca4c6.

### cl...@chromium.org (2014-09-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-21)

ClusterFuzz has detected this issue as fixed in range 295856:295875.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5104550651363328

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60d0000af560
Crash State:
  CPDF_ImageObject::~CPDF_ImageObject
  CPDF_ImageObject::~CPDF_ImageObject
  CPDF_PageObjects::~CPDF_PageObjects
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=294200:294571
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=295856:295875

Minimized Testcase (952.85 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94OjfSRARuUeoAIgGhRAxnt1AELRi3mh8yygIztD2oU8Ps57iRJo1z4Al4zMp3iz3fTWjTdZ_QAe0mkHsQg8MuYXl_NyBk4FReR3TqEWIjm8C6BGS0jPNm_9NuABLDqk0O9ZSyDoj8SONZgbD5Yx5klj5cyuFl0s5BnseaUhEnfqKjAMNw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@chromium.org (2014-09-23)

Matthew - Merge requested for M38 (branch 2125)

### [Deleted User] (2014-09-24)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-24)

Jun - please merge to M38 / branch 2125

### ma...@google.com (2014-09-26)

Please process the merge approval if you haven't.

### ti...@chromium.org (2014-09-29)

Bo / Jun - can you please merge this to branch 2125 ASAP?

### ti...@chromium.org (2014-09-29)

This merge is dependent on https://crbug.com/chromium/414661 - chasing.

### ju...@foxitsoftware.com (2014-09-29)

It's merged to M38 / branch 2125

### ti...@chromium.org (2014-09-29)

Thanks Jun

### am...@chromium.org (2014-09-30)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Atte - $2000 for this report. There were questions of the level of attacker control, which is why this was in the middle of the range at $2000.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-26)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/414046?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/414661]
[Monorail mergedwith: crbug.com/chromium/414097, crbug.com/chromium/416155]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080450)*
