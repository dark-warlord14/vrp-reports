# Security: PDFium UAF in CFX_XMLElement::Save

| Field | Value |
|-------|-------|
| **Issue ID** | [40091128](https://issues.chromium.org/issues/40091128) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2018-04-18 |
| **Bounty** | $3,500.00 |

## Description

**VULNERABILITY DETAILS**  

UAF can be triggered in PDFium with XFA enabled when executing the following code.

```
xfa.data.saveXML("pretty");  

```
# ASAN Log:

==18204==ERROR: AddressSanitizer: heap-use-after-free on address 0x0781cb1c at pc 0x02efe64c bp 0x042ed134 sp 0x042ed124  

READ of size 8 at 0x0781cb1c thread T0  

==18204==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==18204==\*\*\* Most likely this means that the app is already \*\*\*  

==18204==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==18204==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==18204==\*\*\* or produce wrong results. \*\*\*  

#0 0x2efe666 in \_\_asan\_memcpy c:\b\rr\tmpkmvu8v\w\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cc:23  

#1 0x2a64d17 in CFX\_MemoryStream::WriteBlock C:\pdfium\core\fxcrt\cfx\_memorystream.cpp:124  

#2 0x1f2663c in IFX\_SeekableStream::WriteBlock C:\pdfium\core\fxcrt\fx\_stream.cpp:95  

#3 0x1f266f2 in IFX\_SeekableStream::WriteString C:\pdfium\core\fxcrt\fx\_stream.cpp:99  

#4 0x2a70d37 in CFX\_XMLElement::Save C:\pdfium\core\fxcrt\xml\cfx\_xmlelement.cpp:103  

#5 0x2d19d11 in CJX\_Node::saveXML C:\pdfium\fxjs\xfa\cjx\_node.cpp:357  

#6 0x2d16c65 in CJX\_Node::saveXML\_static C:\pdfium\fxjs\xfa\cjx\_node.h:30  

#7 0x2cec936 in CJX\_Object::RunMethod C:\pdfium\fxjs\xfa\cjx\_object.cpp:176  

#8 0x2d07c6c in CFXJSE\_Engine::NormalMethodCall C:\pdfium\fxjs\cfxjse\_engine.cpp:421  

#9 0x2672e15 in `anonymous namespace'::DynPropGetterAdapter_MethodCallback C:\pdfium\fxjs\cfxjse_class.cpp:96 #10 0x345c6e in v8::internal::FunctionCallbackArguments::Call C:\pdfium\v8\src\api-arguments.cc:29 #11 0x4fd2ec in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\pdfium\v8\src\builtins\builtins-api.cc:107  

#12 0x4fa309 in v8::internal::Builtin\_Impl\_HandleApiCall C:\pdfium\v8\src\builtins\builtins-api.cc:137  

#13 0x4f97c1 in v8::internal::Builtin\_HandleApiCall C:\pdfium\v8\src\builtins\builtins-api.cc:125

0x0781cb1c is located 12 bytes inside of 24-byte region [0x0781cb10,0x0781cb28)  

freed by thread T0 here:  

#0 0x2efe1e8 in free c:\b\rr\tmpkmvu8v\w\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:44  

#1 0x1f27f58 in fxcrt::ByteString::~ByteString C:\pdfium\core\fxcrt\bytestring.cpp:227  

#2 0x2a70beb in CFX\_XMLElement::Save C:\pdfium\core\fxcrt\xml\cfx\_xmlelement.cpp:100  

#3 0x2d19d11 in CJX\_Node::saveXML C:\pdfium\fxjs\xfa\cjx\_node.cpp:357  

#4 0x2d16c65 in CJX\_Node::saveXML\_static C:\pdfium\fxjs\xfa\cjx\_node.h:30  

#5 0x2cec936 in CJX\_Object::RunMethod C:\pdfium\fxjs\xfa\cjx\_object.cpp:176  

#6 0x2d07c6c in CFXJSE\_Engine::NormalMethodCall C:\pdfium\fxjs\cfxjse\_engine.cpp:421  

#7 0x2672e15 in `anonymous namespace'::DynPropGetterAdapter_MethodCallback C:\pdfium\fxjs\cfxjse_class.cpp:96 #8 0x345c6e in v8::internal::FunctionCallbackArguments::Call C:\pdfium\v8\src\api-arguments.cc:29 #9 0x4fd2ec in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\pdfium\v8\src\builtins\builtins-api.cc:107  

#10 0x4fa309 in v8::internal::Builtin\_Impl\_HandleApiCall C:\pdfium\v8\src\builtins\builtins-api.cc:137  

#11 0x4f97c1 in v8::internal::Builtin\_HandleApiCall C:\pdfium\v8\src\builtins\builtins-api.cc:125

previously allocated by thread T0 here:  

#0 0x2efe2cc in malloc c:\b\rr\tmpkmvu8v\w\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:60  

#1 0x1f28205 in fxcrt::StringDataTemplate<char>::Create C:\pdfium\core\fxcrt\string\_data\_template.h:39  

#2 0x1f28322 in fxcrt::ByteString::ByteString C:\pdfium\core\fxcrt\bytestring.cpp:184  

#3 0x1f3e802 in FX\_UTF8Encode C:\pdfium\core\fxcrt\fx\_string.cpp:71  

#4 0x1f393ab in fxcrt::WideString::UTF8Encode C:\pdfium\core\fxcrt\widestring.cpp:666  

#5 0x2a70b55 in CFX\_XMLElement::Save C:\pdfium\core\fxcrt\xml\cfx\_xmlelement.cpp:100  

#6 0x2d19d11 in CJX\_Node::saveXML C:\pdfium\fxjs\xfa\cjx\_node.cpp:357  

#7 0x2d16c65 in CJX\_Node::saveXML\_static C:\pdfium\fxjs\xfa\cjx\_node.h:30  

#8 0x2cec936 in CJX\_Object::RunMethod C:\pdfium\fxjs\xfa\cjx\_object.cpp:176  

#9 0x2d07c6c in CFXJSE\_Engine::NormalMethodCall C:\pdfium\fxjs\cfxjse\_engine.cpp:421  

#10 0x2672e15 in `anonymous namespace'::DynPropGetterAdapter_MethodCallback C:\pdfium\fxjs\cfxjse_class.cpp:96 #11 0x345c6e in v8::internal::FunctionCallbackArguments::Call C:\pdfium\v8\src\api-arguments.cc:29 #12 0x4fd2ec in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\pdfium\v8\src\builtins\builtins-api.cc:107  

#13 0x4fa309 in v8::internal::Builtin\_Impl\_HandleApiCall C:\pdfium\v8\src\builtins\builtins-api.cc:137  

#14 0x4f97c1 in v8::internal::Builtin\_HandleApiCall C:\pdfium\v8\src\builtins\builtins-api.cc:125

SUMMARY: AddressSanitizer: heap-use-after-free c:\b\rr\tmpkmvu8v\w\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cc:23 in \_\_asan\_memcpy  

Shadow bytes around the buggy address:  

0x30f03910: fd fa fa fa fd fd fd fa fa fa fd fd fd fd fa fa  

0x30f03920: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fa  

0x30f03930: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd  

0x30f03940: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa  

0x30f03950: fd fd fd fa fa fa fd fd fd fd fa fa 00 00 00 04  

=>0x30f03960: fa fa fd[fd]fd fa fa fa fd fd fd fd fa fa fd fd  

0x30f03970: fd fa fa fa 00 00 00 00 fa fa fd fd fd fa fa fa  

0x30f03980: fd fd fd fd fa fa 00 00 00 fa fa fa fd fd fd fd  

0x30f03990: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd  

0x30f039a0: fd fd fa fa fd fd fd fa fa fa fd fd fd fa fa fa  

0x30f039b0: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fa  

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

==18204==ABORTING

**VERSION**  

Chrome Version: PDFium with XFA enabled  

Operating System: All

**REPRODUCTION CASE**  

A minimized proof-of-concept file has been attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### st...@gmail.com (2018-04-18)

Please note it only affects XFA enabled PDFium. Some of the build arguments:

```
pdf_enable_xfa = true
pdf_enable_v8 = true
is_asan=true
```

### st...@gmail.com (2018-04-18)

I've uploaded a CL at https://pdfium-review.googlesource.com/c/pdfium/+/30890

### va...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2018-04-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6073114652573696.

### ds...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### st...@gmail.com (2018-04-19)

I think this should be Security_Severity-High :-)

### bu...@chromium.org (2018-04-19)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/f24afac5e17e10f70336912ff85d8cb9c783f8a8

commit f24afac5e17e10f70336912ff85d8cb9c783f8a8
Author: Ke Liu <stackexploit@gmail.com>
Date: Thu Apr 19 04:11:42 2018

Fix UAF in CFX_XMLElement::Save

Use a ByteString object to store the returned value of
WideString.UTF8Encode() instead of using a ByteStringView object
to store the returned value of WideString.UTF8Encode().AsStringView().

Bug: chromium:834149
Change-Id: I8fa8dd7920140730c0417c188572d7b53e4ffb48
Reviewed-on: https://pdfium-review.googlesource.com/30890
Reviewed-by: dsinclair <dsinclair@chromium.org>
Commit-Queue: dsinclair <dsinclair@chromium.org>

[modify] https://crrev.com/f24afac5e17e10f70336912ff85d8cb9c783f8a8/core/fxcrt/xml/cfx_xmlelement.cpp


### bu...@chromium.org (2018-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8f9aa8cbf310d86979bd0dce86d67298f4d66abd

commit 8f9aa8cbf310d86979bd0dce86d67298f4d66abd
Author: pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Thu Apr 19 05:23:42 2018

Roll src/third_party/pdfium/ e06880f8e..f24afac5e (1 commit)

https://pdfium.googlesource.com/pdfium.git/+log/e06880f8eb98..f24afac5e17e

$ git log e06880f8e..f24afac5e --date=short --no-merges --format='%ad %ae %s'
2018-04-19 stackexploit Fix UAF in CFX_XMLElement::Save

Created with:
  roll-dep src/third_party/pdfium
BUG=chromium:834149


The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=dsinclair@chromium.org

Change-Id: I1d0f74993959719fce90b7221c127ed55062146a
Reviewed-on: https://chromium-review.googlesource.com/1018599
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#551950}
[modify] https://crrev.com/8f9aa8cbf310d86979bd0dce86d67298f4d66abd/DEPS


### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### ds...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-23)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-27)

Hi stackexploit@ - the VRP panel agreeded that this should be High, and awarded $3,000 for the bug and $500 for the fix. Cheers as always :-)

### aw...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-07-27)

This issue was migrated from crbug.com/chromium/834149?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091128)*
