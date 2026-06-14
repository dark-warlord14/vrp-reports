# Negative size parameter to memcpy in CPDF_SecurityHandler::GetUserPassword

| Field | Value |
|-------|-------|
| **Issue ID** | [40050878](https://issues.chromium.org/issues/40050878) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-12-04 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

This bug is present in GetUserPassword(const ByteString& owner\_password) method of core/fpdfapi/parser/cpdf\_security\_handler.cpp file.  

These lines of code cause this bug.

...  

ByteString okey = m\_pEncryptDict->GetStringFor("O");  

...  

int okeylen = okey.GetLength();  

if (okeylen > 32) {  

okeylen = 32;  

}  

uint8\_t okeybuf[64];  

memset(okeybuf, 0, sizeof(okeybuf));  

memcpy(okeybuf, okey.c\_str(), okeylen);  

...

If "okey" has more than 2147483647 characters "okeylen" will have a minus value.Because "okeylen" is an "int" type variable.  

So length passed to memcpy will be incorrect.

**VERSION**

Chrome Version: [78.0.3904.108] + [stable]  

\* Does not reproduce with official google-chrome stable release.  

Reproduce only with chromium stable release for Ubuntu with --no-sandbox option.  

\* Takes 15-25 minutes to reproduce

[80.0.3982.0] + (Local Development Build]  

\* Takes about 2 hours to reproduce this test case on my local chrome built with address sanitizer and debug symols.

Operating System: [Ubuntu 18.04 64 bit]

HARDWARE REQUIREMENTS

64 bit computer with 16GB Memory

**REPRODUCTION CASE**

1. Install chromium-browser and chromium-browser-dbgsym packages on Ubuntu.  
   
   chromium-browser-dbgsym is required only to get a backtrace.
2. Save attached template.pdf and addLargePassword.cpp file to same folder.
3. Build addLargePassword.cpp.  
   
   g++ -o addLargePassword addLargePassword.cpp  
   
   \* This c++ program creates a large pdf file, which is the test case.  
   
   This step is necessary because it is not possible to attach a large file.
4. Run addLargePassword to create the test case.  
   
   ./addLargePassword  
   
   This program will take about 10 minutes to complete.  
   
   Once finished this will create large.pdf file in same folder.
5. Open Ubuntu Terminal and open chromium-browser with no-sandbox option.  
   
   chromium-browser --no-sandbox
   
   \* PDF Plugin process crash, when I try to load large.pdf file on chromium with sandbox.  
   
   Official google-chrome also can't load this PDF file with or without sandbox.  
   
   This message was displayed on console, in both above cases.  
   
   FATAL:memory\_linux.cc(37)] Out of memory
6. Open large.pdf with chrome.  
   
   Chrome will take about 10-15 minutes to load this file.
7. Then Chrome will ask for a password for pdf file.
8. Type any text as password.
9. After about 5-10 minutes PDF Plugin process will crash.

Type of crash: [PDF Plugin process]

Crash State:  

[stacktrace]

This backtrace is taken from Ubuntu chromium-browser version 78.0.3904.108.  

#0 0x00007fb70b3fbcf4 in \_\_memmove\_avx\_unaligned\_erms () at ../sysdeps/x86\_64/multiarch/memmove-vec-unaligned-erms.S:427  

#1 0x000056318186b2bd in GetUserPassword() () at ../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_security\_handler.cpp:498  

#2 0x000056318186a9f4 in CheckOwnerPassword () at ../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_security\_handler.cpp:518  

#3 0x000056318186a9f4 in CheckPasswordImpl() () at ../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_security\_handler.cpp:422  

#4 0x000056318186994f in CheckPassword() () at ../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_security\_handler.cpp:400  

#5 0x0000563181869717 in CheckSecurity () at ../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_security\_handler.cpp:118  

#6 0x0000563181869717 in OnInit() () at ../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_security\_handler.cpp:110  

#7 0x0000563181864e0d in SetEncryptHandler() () at ../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:255  

#8 0x0000563181863528 in StartParseInternal() () at ../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:182  

#9 0x0000563181863488 in StartParse() () at ../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:157  

#10 0x00005631818588aa in LoadDoc() () at ../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_document.cpp:96  

#11 0x00005631818d7dcc in LoadDocumentImpl() () at ../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:144  

#12 0x00005631818d7ff3 in FPDF\_LoadCustomDocument() () at ../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:277  

#13 0x000056318546a791 in LoadDocument() () at ../../pdf/pdfium/pdfium\_document.cc:102  

#14 0x000056318544f17a in TryLoadingDoc() () at ../../pdf/pdfium/pdfium\_engine.cc:2318  

#15 0x000056318544f1f6 in ContinueLoadingDocument() () at ../../pdf/pdfium/pdfium\_engine.cc:2354  

#16 0x000056318544f47a in OnGetPasswordComplete() () at ../../pdf/pdfium/pdfium\_engine.cc:2347

[Address Sanitizer Output]

This output was taken from chrome version 78.0.3904.0 (Developer Build) (64-bit), built with address sanitizer.  

This build can be downloaded from <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-693954.zip?generation=1567726569364535&alt=media>  

\* It takes about 30 minutes to reproduce this test case on this build.

==4226==ERROR: AddressSanitizer: negative-size-param: (size=-2147483648)  

#0 0x562fce41e507 in \_\_asan\_memcpy /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors\_memintrinsics.cpp:22:3  

#1 0x562fd6e1613d in CPDF\_SecurityHandler::GetUserPassword(fxcrt::ByteString const&) const third\_party/pdfium/core/fpdfapi/parser/cpdf\_security\_handler.cpp:498:3  

#2 0x562fd6e1495c in CheckOwnerPassword third\_party/pdfium/core/fpdfapi/parser/cpdf\_security\_handler.cpp:518:26  

#3 0x562fd6e1495c in CPDF\_SecurityHandler::CheckPasswordImpl(fxcrt::ByteString const&, bool) third\_party/pdfium/core/fpdfapi/parser/cpdf\_security\_handler.cpp:422:12  

#4 0x562fd6e11751 in CPDF\_SecurityHandler::CheckPassword(fxcrt::ByteString const&, bool) third\_party/pdfium/core/fpdfapi/parser/cpdf\_security\_handler.cpp:400:7  

#5 0x562fd6e10fc8 in CheckSecurity third\_party/pdfium/core/fpdfapi/parser/cpdf\_security\_handler.cpp:118:30  

#6 0x562fd6e10fc8 in CPDF\_SecurityHandler::OnInit(CPDF\_Dictionary const\*, CPDF\_Array const\*, fxcrt::ByteString const&) third\_party/pdfium/core/fpdfapi/parser/cpdf\_security\_handler.cpp:110:8  

#7 0x562fd6e01840 in CPDF\_Parser::SetEncryptHandler() third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:255:26  

#8 0x562fd6dfc382 in CPDF\_Parser::StartParseInternal() third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:182:16  

#9 0x562fd6dfc0e3 in CPDF\_Parser::StartParse(fxcrt::RetainPtr<IFX\_SeekableReadStream> const&, char const\*) third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:157:10  

#10 0x562fd6ddb4d1 in CPDF\_Document::LoadDoc(fxcrt::RetainPtr<IFX\_SeekableReadStream> const&, char const\*) third\_party/pdfium/core/fpdfapi/parser/cpdf\_document.cpp:96:38  

#11 0x562fd6f7b0ec in (anonymous namespace)::LoadDocumentImpl(fxcrt::RetainPtr<IFX\_SeekableReadStream> const&, char const\*) third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:144:41  

#12 0x562fd6f7ba46 in FPDF\_LoadCustomDocument third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:277:10  

#13 0x562fe8bebd49 in chrome\_pdf::PDFiumDocument::LoadDocument(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) pdf/pdfium/pdfium\_document.cc:102:9  

#14 0x562fe8bd8ba1 in chrome\_pdf::PDFiumEngine::TryLoadingDoc(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, bool\*) pdf/pdfium/pdfium\_engine.cc:2306:14  

#15 0x562fe8bd8e1f in chrome\_pdf::PDFiumEngine::ContinueLoadingDocument(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) pdf/pdfium/pdfium\_engine.cc:2342:17  

#16 0x562fe8bd984c in chrome\_pdf::PDFiumEngine::OnGetPasswordComplete(int, pp::Var const&) pdf/pdfium/pdfium\_engine.cc:2335:3

0x7f1a2ce28818 is located 24 bytes inside of 2147483680-byte region [0x7f1a2ce28800,0x7f1aace28820)  

allocated by thread T0 (chrome) here:  

#0 0x562fce41ef5d in malloc /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_malloc\_linux.cpp:145:3  

#1 0x562fd6a5dcd0 in PartitionAllocGenericFlags third\_party/pdfium/third\_party/base/allocator/partition\_allocator/partition\_alloc.h:397:48  

#2 0x562fd6a5dcd0 in Alloc third\_party/pdfium/third\_party/base/allocator/partition\_allocator/partition\_alloc.h:430:10  

#3 0x562fd6a5dcd0 in Create third\_party/pdfium/core/fxcrt/string\_data\_template.h:39:57  

#4 0x562fd6a5dcd0 in Create third\_party/pdfium/core/fxcrt/string\_data\_template.h:45:34  

#5 0x562fd6a5dcd0 in fxcrt::ByteString::ByteString(std::\_\_1::basic\_ostringstream<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) third\_party/pdfium/core/fxcrt/bytestring.cpp:187:19  

#6 0x562fd6e23593 in CPDF\_SyntaxParser::ReadString() third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp  

#7 0x562fd6e255c8 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:461:22  

#8 0x562fd6e26257 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:507:11  

#9 0x562fd6e28d05 in CPDF\_SyntaxParser::GetIndirectObject(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:559:33  

#10 0x562fd6e09292 in CPDF\_Parser::ParseIndirectObjectAt(long, unsigned int) third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:916:28  

#11 0x562fd6e0a1a0 in CPDF\_Parser::ParseIndirectObject(unsigned int) third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:865:12  

#12 0x562fd6ddadfc in CPDF\_Document::ParseIndirectObject(unsigned int) third\_party/pdfium/core/fpdfapi/parser/cpdf\_document.cpp:76:33  

#13 0x562fd6de96ee in CPDF\_IndirectObjectHolder::GetOrParseIndirectObject(unsigned int) third\_party/pdfium/core/fpdfapi/parser/cpdf\_indirect\_object\_holder.cpp:50:36  

#14 0x562fd6e01eb3 in CPDF\_Parser::GetEncryptDict() const third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:820:43  

#15 0x562fd6e016c4 in CPDF\_Parser::SetEncryptHandler() third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:247:41  

#16 0x562fd6dfc382 in CPDF\_Parser::StartParseInternal() third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:182:16  

#17 0x562fd6dfc0e3 in CPDF\_Parser::StartParse(fxcrt::RetainPtr<IFX\_SeekableReadStream> const&, char const\*) third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:157:10  

#18 0x562fd6ddb4d1 in CPDF\_Document::LoadDoc(fxcrt::RetainPtr<IFX\_SeekableReadStream> const&, char const\*) third\_party/pdfium/core/fpdfapi/parser/cpdf\_document.cpp:96:38  

#19 0x562fd6f7b0ec in (anonymous namespace)::LoadDocumentImpl(fxcrt::RetainPtr<IFX\_SeekableReadStream> const&, char const\*) third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:144:41  

#20 0x562fd6f7ba46 in FPDF\_LoadCustomDocument third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:277:10  

#21 0x562fe8bebd49 in chrome\_pdf::PDFiumDocument::LoadDocument(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) pdf/pdfium/pdfium\_document.cc:102:9  

#22 0x562fe8bd8ba1 in chrome\_pdf::PDFiumEngine::TryLoadingDoc(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, bool\*) pdf/pdfium/pdfium\_engine.cc:2306:14  

#23 0x562fe8bd8e1f in chrome\_pdf::PDFiumEngine::ContinueLoadingDocument(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) pdf/pdfium/pdfium\_engine.cc:2342:17  

#24 0x562fe8bd984c in chrome\_pdf::PDFiumEngine::OnGetPasswordComplete(int, pp::Var const&) pdf/pdfium/pdfium\_engine.cc:2335:3

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

Reporter credit: [anonymous]

## Attachments

- [template.pdf](attachments/template.pdf) (application/pdf, 619 B)
- [addLargePassword.cpp](attachments/addLargePassword.cpp) (text/plain, 564 B)

## Timeline

### me...@chromium.org (2019-12-04)

Thanks for the report.

I wasn't able to reproduce this on trunk Chromium.

tsepez@ or thestig@ could you please take a look?

Given that:
1. This bug requires --no-sandbox.
2. It does not appear to affect any official version of Chrome (distro packages of Chromium might patch Chromium, so I'm not sure we can support them).
3. This bug seems very difficult to trigger (takes a long time and seems to require a large amount of RAM).

I'm inclined to mark this as a regular bug rather than a security bug (labeling low severity now out of caution). tsepez@ or thestig@ what do you think of this?

[Monorail components: Internals>Plugins>PDF]

### me...@chromium.org (2019-12-04)

This results in an out of memory error in trunk chromium.

### th...@chromium.org (2019-12-04)

I can try for a repro. Maybe |okeylen| and others should all become size_t, and maybe there should be a limit on the size of |okeylen|.

### th...@chromium.org (2019-12-04)

I'm also going to try UBSAN and see what it complains about.

### th...@chromium.org (2019-12-04)

Also OOM here, but I'll try some more and see if that's because we got a negative value.

### th...@chromium.org (2019-12-04)

OK, I nudged pdfium_test into triggering the negative |okeylen| value.

Someone may want to set the Security_Impact labels and what not.

### ts...@chromium.org (2019-12-04)

I would call this severity high, but impact none.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-04)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/270946946c93b5dcc33b24263cee3814f00f6e34

commit 270946946c93b5dcc33b24263cee3814f00f6e34
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Dec 04 21:44:19 2019

Fix wrong integer type CPDF_SecurityHandler::GetUserPassword().

Do not try to hold a size_t in an int. Slightly refactor the surrounding
code to be more compact.

Bug: chromium:1030583
Change-Id: I111577dd90b1f702e3d061c60c66798cf155b1ab
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/63152
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/270946946c93b5dcc33b24263cee3814f00f6e34/core/fpdfapi/parser/cpdf_security_handler.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2feb741c8903f28625c95aa7fe0fb707b26bb0f3

commit 2feb741c8903f28625c95aa7fe0fb707b26bb0f3
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Dec 05 01:25:03 2019

Roll src/third_party/pdfium 391d4f3130da..270946946c93 (1 commits)

https://pdfium.googlesource.com/pdfium.git/+log/391d4f3130da..270946946c93

git log 391d4f3130da..270946946c93 --date=short --first-parent --format='%ad %ae %s'
2019-12-04 thestig@chromium.org Fix wrong integer type CPDF_SecurityHandler::GetUserPassword().

Created with:
  gclient setdep -r src/third_party/pdfium@270946946c93

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1030583
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I089bf4bf8a06008f4f0d5e1c1f32b17d0ae49cf3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1951892
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#721786}

[modify] https://crrev.com/2feb741c8903f28625c95aa7fe0fb707b26bb0f3/DEPS


### th...@chromium.org (2019-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-05)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bb0adca4382c0b1737bf032c2ced6c36931b2b0c

commit bb0adca4382c0b1737bf032c2ced6c36931b2b0c
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Dec 06 21:16:06 2019

Roll src/third_party/pdfium 02a82546e547..f3883e32a739 (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/02a82546e547..f3883e32a739

git log 02a82546e547..f3883e32a739 --date=short --first-parent --format='%ad %ae %s'
2019-12-06 tsepez@chromium.org Fix typo in array name in HTMLSTR2Code()
2019-12-06 thestig@chromium.org Use more spans with CRYPT_ArcFour code.

Created with:
  gclient setdep -r src/third_party/pdfium@f3883e32a739

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1030583,chromium:1031523
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I3b0cd04114424aba91d9f4baacc29eb16831a31f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1955180
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#722613}

[modify] https://crrev.com/bb0adca4382c0b1737bf032c2ced6c36931b2b0c/DEPS


### th...@chromium.org (2019-12-06)

Whoops, I didn't mean to include the Bug: entry in the commit message for https://pdfium.googlesource.com/pdfium.git/+/c4d5accfdca3cae1c2d426f27289b212c1a524ae

### aw...@google.com (2019-12-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-17)

Congrats! The Panel decided to reward $500 for this report

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1030583?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050878)*
