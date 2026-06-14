# pdfium: use-of-uninitialized-value in CRYPT_AESSetKey

| Field | Value |
|-------|-------|
| **Issue ID** | [40050928](https://issues.chromium.org/issues/40050928) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-12-09 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.130 Safari/537.36

Steps to reproduce the problem:
WARNING: MemorySanitizer: use-of-uninitialized-value
    #0 0x55bf74fdc460 in (anonymous namespace)::aes_setup(CRYPT_aes_context*, unsigned char const*, int) core/fdrm/fx_crypt_aes.cpp:535:16
    #1 0x55bf74fdba98 in CRYPT_AESSetKey(CRYPT_aes_context*, unsigned char const*, unsigned int, bool) core/fdrm/fx_crypt_aes.cpp:635:3
    #2 0x55bf75511cc3 in CPDF_SecurityHandler::AES256_SetPassword(CPDF_Dictionary*, fxcrt::ByteString const&, bool, unsigned char const*) core/fpdfapi/parser/cpdf_security_handler.cpp:667:3
    #3 0x55bf7550fa1b in CPDF_SecurityHandler::OnCreateInternal(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&, fxcrt::ByteString const&, bool) core/fpdfapi/parser/cpdf_security_handler.cpp:534:5
    #4 0x55bf755125ab in CPDF_SecurityHandler::OnCreate(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&) core/fpdfapi/parser/cpdf_security_handler.cpp:619:3
    #5 0x55bf751fc653 in CPDF_Creator::InitID() core/fpdfapi/edit/cpdf_creator.cpp:625:27
    #6 0x55bf751fb6ea in CPDF_Creator::Create(unsigned int) core/fpdfapi/edit/cpdf_creator.cpp:588:3
    #7 0x55bf74fb2c1d in (anonymous namespace)::DoDocSave(fpdf_document_t__*, FPDF_FILEWRITE_*, unsigned long, pdfium::Optional<int>) fpdfsdk/fpdf_save.cpp:202:25
    #8 0x55bf74fb27be in FPDF_SaveAsCopy fpdfsdk/fpdf_save.cpp:217:10
    #9 0x55bf74e7ec43 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:949:3
    #10 0x55bf74e7877d in main samples/pdfium_test.cc:1154:5

  Uninitialized value was stored to memory at
    #0 0x55bf74e21946 in __msan_memcpy /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/msan/msan_interceptors.cpp:1566:3
    #1 0x55bf74fe0326 in (anonymous namespace)::SHATransform(unsigned int*, unsigned int*) core/fdrm/fx_crypt_sha.cpp:94:10
    #2 0x55bf74fe016a in CRYPT_SHA1Update(CRYPT_sha1_context*, unsigned char const*, unsigned int) core/fdrm/fx_crypt_sha.cpp:388:5
    #3 0x55bf74fe0f1e in CRYPT_SHA1Finish(CRYPT_sha1_context*, unsigned char*) core/fdrm/fx_crypt_sha.cpp:415:3
    #4 0x55bf7551133d in CPDF_SecurityHandler::AES256_SetPassword(CPDF_Dictionary*, fxcrt::ByteString const&, bool, unsigned char const*) core/fpdfapi/parser/cpdf_security_handler.cpp:633:3
    #5 0x55bf7550fa1b in CPDF_SecurityHandler::OnCreateInternal(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&, fxcrt::ByteString const&, bool) core/fpdfapi/parser/cpdf_security_handler.cpp:534:5
    #6 0x55bf755125ab in CPDF_SecurityHandler::OnCreate(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&) core/fpdfapi/parser/cpdf_security_handler.cpp:619:3
    #7 0x55bf751fc653 in CPDF_Creator::InitID() core/fpdfapi/edit/cpdf_creator.cpp:625:27
    #8 0x55bf751fb6ea in CPDF_Creator::Create(unsigned int) core/fpdfapi/edit/cpdf_creator.cpp:588:3
    #9 0x55bf74fb2c1d in (anonymous namespace)::DoDocSave(fpdf_document_t__*, FPDF_FILEWRITE_*, unsigned long, pdfium::Optional<int>) fpdfsdk/fpdf_save.cpp:202:25
    #10 0x55bf74fb27be in FPDF_SaveAsCopy fpdfsdk/fpdf_save.cpp:217:10
    #11 0x55bf74e7ec43 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:949:3
    #12 0x55bf74e7877d in main samples/pdfium_test.cc:1154:5

  Uninitialized value was stored to memory at
    #0 0x55bf74fe00fe in CRYPT_SHA1Update(CRYPT_sha1_context*, unsigned char const*, unsigned int) core/fdrm/fx_crypt_sha.cpp:383:20
    #1 0x55bf74fe0f1e in CRYPT_SHA1Finish(CRYPT_sha1_context*, unsigned char*) core/fdrm/fx_crypt_sha.cpp:415:3
    #2 0x55bf7551133d in CPDF_SecurityHandler::AES256_SetPassword(CPDF_Dictionary*, fxcrt::ByteString const&, bool, unsigned char const*) core/fpdfapi/parser/cpdf_security_handler.cpp:633:3
    #3 0x55bf7550fa1b in CPDF_SecurityHandler::OnCreateInternal(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&, fxcrt::ByteString const&, bool) core/fpdfapi/parser/cpdf_security_handler.cpp:534:5
    #4 0x55bf755125ab in CPDF_SecurityHandler::OnCreate(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&) core/fpdfapi/parser/cpdf_security_handler.cpp:619:3
    #5 0x55bf751fc653 in CPDF_Creator::InitID() core/fpdfapi/edit/cpdf_creator.cpp:625:27
    #6 0x55bf751fb6ea in CPDF_Creator::Create(unsigned int) core/fpdfapi/edit/cpdf_creator.cpp:588:3
    #7 0x55bf74fb2c1d in (anonymous namespace)::DoDocSave(fpdf_document_t__*, FPDF_FILEWRITE_*, unsigned long, pdfium::Optional<int>) fpdfsdk/fpdf_save.cpp:202:25
    #8 0x55bf74fb27be in FPDF_SaveAsCopy fpdfsdk/fpdf_save.cpp:217:10
    #9 0x55bf74e7ec43 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:949:3
    #10 0x55bf74e7877d in main samples/pdfium_test.cc:1154:5

  Uninitialized value was stored to memory at
    #0 0x55bf74e21946 in __msan_memcpy /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/msan/msan_interceptors.cpp:1566:3
    #1 0x55bf74fe01cf in CRYPT_SHA1Update(CRYPT_sha1_context*, unsigned char const*, unsigned int) core/fdrm/fx_crypt_sha.cpp:391:3
    #2 0x55bf755112b3 in CPDF_SecurityHandler::AES256_SetPassword(CPDF_Dictionary*, fxcrt::ByteString const&, bool, unsigned char const*) core/fpdfapi/parser/cpdf_security_handler.cpp:629:3
    #3 0x55bf7550fa1b in CPDF_SecurityHandler::OnCreateInternal(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&, fxcrt::ByteString const&, bool) core/fpdfapi/parser/cpdf_security_handler.cpp:534:5
    #4 0x55bf755125ab in CPDF_SecurityHandler::OnCreate(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&) core/fpdfapi/parser/cpdf_security_handler.cpp:619:3
    #5 0x55bf751fc653 in CPDF_Creator::InitID() core/fpdfapi/edit/cpdf_creator.cpp:625:27
    #6 0x55bf751fb6ea in CPDF_Creator::Create(unsigned int) core/fpdfapi/edit/cpdf_creator.cpp:588:3
    #7 0x55bf74fb2c1d in (anonymous namespace)::DoDocSave(fpdf_document_t__*, FPDF_FILEWRITE_*, unsigned long, pdfium::Optional<int>) fpdfsdk/fpdf_save.cpp:202:25
    #8 0x55bf74fb27be in FPDF_SaveAsCopy fpdfsdk/fpdf_save.cpp:217:10
    #9 0x55bf74e7ec43 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:949:3
    #10 0x55bf74e7877d in main samples/pdfium_test.cc:1154:5

  Uninitialized value was stored to memory at
    #0 0x55bf74ff1320 in CRYPT_SHA256Finish(CRYPT_sha2_context*, unsigned char*) core/fdrm/fx_crypt_sha.cpp:486:3
    #1 0x55bf7550f9a7 in CPDF_SecurityHandler::OnCreateInternal(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&, fxcrt::ByteString const&, bool) core/fpdfapi/parser/cpdf_security_handler.cpp:533:5
    #2 0x55bf755125ab in CPDF_SecurityHandler::OnCreate(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&) core/fpdfapi/parser/cpdf_security_handler.cpp:619:3
    #3 0x55bf751fc653 in CPDF_Creator::InitID() core/fpdfapi/edit/cpdf_creator.cpp:625:27
    #4 0x55bf751fb6ea in CPDF_Creator::Create(unsigned int) core/fpdfapi/edit/cpdf_creator.cpp:588:3
    #5 0x55bf74fb2c1d in (anonymous namespace)::DoDocSave(fpdf_document_t__*, FPDF_FILEWRITE_*, unsigned long, pdfium::Optional<int>) fpdfsdk/fpdf_save.cpp:202:25
    #6 0x55bf74fb27be in FPDF_SaveAsCopy fpdfsdk/fpdf_save.cpp:217:10
    #7 0x55bf74e7ec43 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:949:3
    #8 0x55bf74e7877d in main samples/pdfium_test.cc:1154:5

  Uninitialized value was stored to memory at
    #0 0x55bf74ff03bf in (anonymous namespace)::sha256_process(CRYPT_sha2_context*, unsigned char const*) core/fdrm/fx_crypt_sha.cpp:245:17
    #1 0x55bf74fe16ce in CRYPT_SHA256Update(CRYPT_sha2_context*, unsigned char const*, unsigned int) core/fdrm/fx_crypt_sha.cpp:457:5
    #2 0x55bf74ff067f in CRYPT_SHA256Finish(CRYPT_sha2_context*, unsigned char*) core/fdrm/fx_crypt_sha.cpp:478:3
    #3 0x55bf7550f9a7 in CPDF_SecurityHandler::OnCreateInternal(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&, fxcrt::ByteString const&, bool) core/fpdfapi/parser/cpdf_security_handler.cpp:533:5
    #4 0x55bf755125ab in CPDF_SecurityHandler::OnCreate(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&) core/fpdfapi/parser/cpdf_security_handler.cpp:619:3
    #5 0x55bf751fc653 in CPDF_Creator::InitID() core/fpdfapi/edit/cpdf_creator.cpp:625:27
    #6 0x55bf751fb6ea in CPDF_Creator::Create(unsigned int) core/fpdfapi/edit/cpdf_creator.cpp:588:3
    #7 0x55bf74fb2c1d in (anonymous namespace)::DoDocSave(fpdf_document_t__*, FPDF_FILEWRITE_*, unsigned long, pdfium::Optional<int>) fpdfsdk/fpdf_save.cpp:202:25
    #8 0x55bf74fb27be in FPDF_SaveAsCopy fpdfsdk/fpdf_save.cpp:217:10
    #9 0x55bf74e7ec43 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:949:3
    #10 0x55bf74e7877d in main samples/pdfium_test.cc:1154:5

  Uninitialized value was stored to memory at
    #0 0x55bf74e21946 in __msan_memcpy /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/msan/msan_interceptors.cpp:1566:3
    #1 0x55bf74fe17e2 in CRYPT_SHA256Update(CRYPT_sha2_context*, unsigned char const*, unsigned int) core/fdrm/fx_crypt_sha.cpp:468:5
    #2 0x55bf7550f95a in CPDF_SecurityHandler::OnCreateInternal(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&, fxcrt::ByteString const&, bool) core/fpdfapi/parser/cpdf_security_handler.cpp:531:5
    #3 0x55bf755125ab in CPDF_SecurityHandler::OnCreate(CPDF_Dictionary*, CPDF_Array const*, fxcrt::ByteString const&) core/fpdfapi/parser/cpdf_security_handler.cpp:619:3
    #4 0x55bf751fc653 in CPDF_Creator::InitID() core/fpdfapi/edit/cpdf_creator.cpp:625:27
    #5 0x55bf751fb6ea in CPDF_Creator::Create(unsigned int) core/fpdfapi/edit/cpdf_creator.cpp:588:3
    #6 0x55bf74fb2c1d in (anonymous namespace)::DoDocSave(fpdf_document_t__*, FPDF_FILEWRITE_*, unsigned long, pdfium::Optional<int>) fpdfsdk/fpdf_save.cpp:202:25
    #7 0x55bf74fb27be in FPDF_SaveAsCopy fpdfsdk/fpdf_save.cpp:217:10
    #8 0x55bf74e7ec43 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:949:3
    #9 0x55bf74e7877d in main samples/pdfium_test.cc:1154:5

  Uninitialized value was created by a heap allocation
    #0 0x55bf74e76b09 in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/msan/msan_new_delete.cpp:45:35
    #1 0x55bf751fd50a in fxcrt::RetainPtr<CPDF_SecurityHandler> pdfium::MakeRetain<CPDF_SecurityHandler>() core/fxcrt/retain_ptr.h:155:23
    #2 0x55bf751fc48b in CPDF_Creator::InitID() core/fpdfapi/edit/cpdf_creator.cpp:624:28
    #3 0x55bf751fb6ea in CPDF_Creator::Create(unsigned int) core/fpdfapi/edit/cpdf_creator.cpp:588:3
    #4 0x55bf74fb2c1d in (anonymous namespace)::DoDocSave(fpdf_document_t__*, FPDF_FILEWRITE_*, unsigned long, pdfium::Optional<int>) fpdfsdk/fpdf_save.cpp:202:25
    #5 0x55bf74fb27be in FPDF_SaveAsCopy fpdfsdk/fpdf_save.cpp:217:10
    #6 0x55bf74e7ec43 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:949:3
    #7 0x55bf74e7877d in main samples/pdfium_test.cc:1154:5

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 78.0.3904.130  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-1032090.pdf](attachments/chromium-1032090.pdf) (application/pdf, 507 B)

## Timeline

### pd...@gmail.com (2019-12-09)

I'm only tentatively reporting this as a security bug. It's unclear how this could be useful.

Also requires user cooperation.

1. Open PDF.
2. Enter password "PDF" when prompted.
3. Try to save or print PDF.

That's how it should work in Chrome anyway, because that's when Chrome calls FPDF_SaveAsCopy.


### pd...@gmail.com (2019-12-09)

Automatically reproducing with pdfium_test requires a small patch.

--- a/samples/pdfium_test.cc
+++ b/samples/pdfium_test.cc
@@ -30,6 +30,7 @@
 #include "public/fpdf_ext.h"
 #include "public/fpdf_formfill.h"
 #include "public/fpdf_progressive.h"
+#include "public/fpdf_save.h"
 #include "public/fpdf_structtree.h"
 #include "public/fpdf_text.h"
 #include "public/fpdfview.h"
@@ -842,7 +842,7 @@ void RenderPdf(const std::string& name,
         is_linearized = true;
       }
     } else {
-      doc.reset(FPDF_LoadCustomDocument(&file_access, nullptr));
+      doc.reset(FPDF_LoadCustomDocument(&file_access, "PDF"));
     }
   }
 
@@ -940,6 +940,14 @@ void RenderPdf(const std::string& name,
     }
   }
 
+  FPDF_FILEWRITE write;
+  write.version = 1;
+  write.WriteBlock = [](FPDF_FILEWRITE*, const void*, unsigned long) {
+    return 1;
+  };
+
+  FPDF_SaveAsCopy(doc.get(), &write, 0);
+
   FORM_DoDocumentAAction(form.get(), FPDFDOC_AACTION_WC);
   fprintf(stderr, "Rendered %d pages.\n", rendered_pages);
   if (bad_pages)


### pd...@gmail.com (2019-12-09)

[Comment Deleted]

### pd...@gmail.com (2019-12-09)

In a related matter, I think a bug might've snuck into a recent commit to CPDF_SecurityHandler::GetUserPassword. If okey.GetLength() is < 32, it triggers a span CHECK in the later while. (Doesn't affect this bug.)

### me...@chromium.org (2019-12-09)

I reproduced this on trunk.
Tom or Lei could you please take a look?

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2019-12-10)

I'll take a look. It's entirely possibly I botched something along the way while doing size_t / span code cleanup.

### sh...@chromium.org (2019-12-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-12-11)

re: https://crbug.com/chromium/1032090#c4 - Care to file a separate bug for that?

### th...@chromium.org (2019-12-11)

It feels like this bug is CPDF_SecurityHandler::OnCreateInternal() abusing uninitialized memory to add more entropy to |CPDF_SecurityHandler::m_EncryptKey|. Is Security_Severity-Medium still appropriate for that?

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### pd...@gmail.com (2019-12-11)

https://crbug.com/pdfium/1436

### th...@chromium.org (2019-12-12)

Thanks. I'll take a look at that.

BTW, I'm also in the process of adding --password support to pdfium_test, so one can do testing here with less pdfium_test.cc patching. https://pdfium-review.googlesource.com/63712

### th...@chromium.org (2019-12-12)

Security folks: Any thoughts on https://crbug.com/chromium/1032090#c11?

### mm...@chromium.org (2019-12-13)

If it's indeed used for entropy initialization, than this is not a security issue. It's not even a bug in PDFium code then, but in order to help fuzzers work better it'd be nice to patch that initialization not to do that under `#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION` condition.

### th...@chromium.org (2019-12-13)

+agl: Any recommentations on what the code here should do? https://pdfium.googlesource.com/pdfium.git/+/ca411935/core/fpdfapi/parser/cpdf_security_handler.cpp#526

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/8d0d0b553acd2775c6d664b36b854540045587a8

commit 8d0d0b553acd2775c6d664b36b854540045587a8
Author: Lei Zhang <thestig@chromium.org>
Date: Sat Dec 14 00:34:54 2019

Exercise saving encrypted PDFs in CPDFSecurityHandlerEmbedderTests.

After opening and rendering the encrypted "hello world" PDFs, save them
and make sure the saved copies also open and render.

This prepares CPDFSecurityHandlerEmbedderTests so it is easier to do
more testing afterwards to trigger a bug in CPDF_SecurityHandler.

Bug: chromium:1032090
Change-Id: I714ba26df42451a6606f33501f99517b603c6cdc
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/63810
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/8d0d0b553acd2775c6d664b36b854540045587a8/core/fpdfapi/parser/cpdf_security_handler_embeddertest.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/4cc552c9df635b0a4f62f88adda9adf5b058014e

commit 4cc552c9df635b0a4f62f88adda9adf5b058014e
Author: Lei Zhang <thestig@chromium.org>
Date: Sat Dec 14 00:58:45 2019

Save encrypted files without IDs in CPDFSecurityHandlerEmbedderTests.

Add methods to CPDF_Parser and CPDF_CrossRefTable to strip the /ID entry
from the PDF trailer. Use this in CPDFSecurityHandlerEmbedderTests to
exercise the PDF creation code paths where they attempt to write out new
encryption dictionaries. This uncovered at least 2 bugs in the code, so
some of the new test code is disabled for now, with TODOs to fix them.

Bug: chromium:1032090,pdfium:1440
Change-Id: Ic285e4ed7ff89b3dc9c604f3e51c5345a4f64f27
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/63752
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/4cc552c9df635b0a4f62f88adda9adf5b058014e/core/fpdfapi/parser/cpdf_parser.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/4cc552c9df635b0a4f62f88adda9adf5b058014e/core/fpdfapi/parser/cpdf_parser.h
[modify] https://pdfium.googlesource.com/pdfium/+/4cc552c9df635b0a4f62f88adda9adf5b058014e/core/fpdfapi/parser/cpdf_cross_ref_table.h
[modify] https://pdfium.googlesource.com/pdfium/+/4cc552c9df635b0a4f62f88adda9adf5b058014e/core/fpdfapi/parser/cpdf_security_handler_embeddertest.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fc0334e61323cf84e425d1a5b67b5f413616ebbd

commit fc0334e61323cf84e425d1a5b67b5f413616ebbd
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Dec 14 04:10:07 2019

Roll src/third_party/pdfium fc3b3ed16213..068b907f128c (7 commits)

https://pdfium.googlesource.com/pdfium.git/+log/fc3b3ed16213..068b907f128c

git log fc3b3ed16213..068b907f128c --date=short --first-parent --format='%ad %ae %s'
2019-12-14 tsepez@chromium.org Add virtual AddChangedContainer() to CXFA_Document::LayoutProcessorIface.
2019-12-14 thestig@chromium.org Save encrypted files without IDs in CPDFSecurityHandlerEmbedderTests.
2019-12-14 tsepez@chromium.org Move CXFA_Node::UpdateUIDisplay() to CFXA_FFDocView::UpdateUIDisplay()
2019-12-14 thestig@chromium.org Exercise saving encrypted PDFs in CPDFSecurityHandlerEmbedderTests.
2019-12-14 thestig@chromium.org Do more verification in CPDFSecurityHandlerEmbedderTests.
2019-12-14 thestig@chromium.org Make a set of CPDFSecurityHandlerEmbedderTests more consistent.
2019-12-13 tsepez@chromium.org Move CXFA_Node::GetNextWidget() to CXFA_FFWidget::GetNextFFWidget().

Created with:
  gclient setdep -r src/third_party/pdfium@068b907f128c

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1032090
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Ib1b35f299d32265fdddeefc9ef97c0f41a08bb62
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1968042
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#724908}

[modify] https://crrev.com/fc0334e61323cf84e425d1a5b67b5f413616ebbd/DEPS


### pd...@gmail.com (2019-12-14)

In a way, this might be a different kind of security bug, in that certain encrypted PDFs produced by pdfium are based on a cryptographically (relatively) weak key. According to the standard, the value of uninitialized memory is undefined (indeterminate), so in the range of predictable to unpredictable. I get the same m_EncryptKey in every run (for the same file).

### pd...@gmail.com (2019-12-14)

And across different files, there are relatively often similarities, like the last 20 bytes being 0.

### ag...@chromium.org (2019-12-16)

> +agl: Any recommentations on what the code here should do? https://pdfium.googlesource.com/pdfium.git/+/ca411935/core/fpdfapi/parser/cpdf_security_handler.cpp#526

I understand that code to be hashing the UNIX epoch time, 32 bytes of uninitialised memory, and the string "there" in order to create a "random" AES-256 key. Is that correct. If so, that should be changed. It's insufficiently random and actually leaks data: with a little heap grooming I'm sure that the uninitialised memory could be crafted to be significantly predictable save for, say, a single pointer. Then the contents of the key might leak ASLR offsets etc. (Or worse.)

In the context of Chromium, call crypto::RandBytes or, if that's too much of a dependency, use BoringSSL directly and call RAND_bytes.

### th...@chromium.org (2019-12-16)

https://pdfium-review.googlesource.com/63932 will use PDFium random number generator code instead of the current inputs.

https://pdfium-review.googlesource.com/63933 will then stop using this code path altogether, for now.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-16)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/088b831b71b74a00d8270962e3e3d215859f156c

commit 088b831b71b74a00d8270962e3e3d215859f156c
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Dec 16 22:43:52 2019

Fix MSAN errors in CPDF_SecurityHandler.

Use FX_Random_GenerateMT() where random data is needed, instead of
relying on uninitialized memory and other means to provide random data.
Re-enable portions of CPDFSecurityHandlerEmbedderTests that were
disabled for MSAN. Fix some nits along the way.

Bug: chromium:1032090
Change-Id: I8d870da2f0677d5af789332dfde7fe8bf8d26465
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/63932
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/088b831b71b74a00d8270962e3e3d215859f156c/core/fpdfapi/parser/cpdf_security_handler.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/088b831b71b74a00d8270962e3e3d215859f156c/core/fpdfapi/parser/cpdf_security_handler_embeddertest.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/53f076f8f7005d6dbdaf117338ae2c7a0d11e18a

commit 53f076f8f7005d6dbdaf117338ae2c7a0d11e18a
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Dec 17 01:40:00 2019

Roll src/third_party/pdfium fc1099a3fbac..088b831b71b7 (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/fc1099a3fbac..088b831b71b7

git log fc1099a3fbac..088b831b71b7 --date=short --first-parent --format='%ad %ae %s'
2019-12-16 thestig@chromium.org Fix MSAN errors in CPDF_SecurityHandler.
2019-12-16 thestig@chromium.org Fix PDF encryption for revision 5 and 6.
2019-12-16 tsepez@chromium.org Move some CPDF_Object usage from CXFA_FFDoc up into CPDFXFA_Context.
2019-12-16 thestig@chromium.org Do more password verification when there is an ID change.
2019-12-16 thestig@chromium.org Verify saved copies can be opened with both passwords.

Created with:
  gclient setdep -r src/third_party/pdfium@088b831b71b7

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1032090
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I5aea33bd3547ca75f04312347b44f339bcd8507d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1970087
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#725364}

[modify] https://crrev.com/53f076f8f7005d6dbdaf117338ae2c7a0d11e18a/DEPS


### th...@chromium.org (2019-12-17)

If we want this for M-79 or M-80, we'll need to merge. I'll take a look Chromium's FPDF_SaveAsCopy() usage later to see how we can hit this problem.

### sh...@chromium.org (2019-12-17)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-18)

Requesting merge to beta M79 because latest trunk commit (725364) appears to be after beta branch point (706915).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-18)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-12-18)

+adetaylor@ for M79 & M80 merge review. 
Change is not yet in canary, this will also need a merge to M80, so adding Merge-Request-80 label. 

### sh...@chromium.org (2019-12-18)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-12-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-19)

Congrats! The Panel decided to reward $2,000 for this report!

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### sr...@google.com (2019-12-20)

thestig@ pls confirm if the verification on canary looks good and it is safe to merge to M80.

### ad...@google.com (2019-12-20)

Yes, we should merge to M80. I'm not completely sold on merging this to M79. As it's a roll of pdfium, it is bound to have some risk, and this is use of uninitialized data so doesn't merit high severity. I suggest we merge to M80 but no further.

### go...@chromium.org (2019-12-20)

Rejecting merge to M79 based on https://crbug.com/chromium/1032090#c39. 

### th...@chromium.org (2019-12-20)

I'm pretty sure Canary is good, because not only did we fix this code path, we actually stopped calling it. Given that, I think the easiest merge to M80 is to actually take just this ~3 line change to avoid calling this code. https://pdfium.googlesource.com/pdfium/+/aeecf1ab623450ec12aaeacd5fab476472124ee7%5E%21/#F0, rather than trying to merge https://pdfium.googlesource.com/pdfium/+/088b831b71b74a00d8270962e3e3d215859f156c, which has lots of merge conflicts.

There's two places in Chromium that directly call into the bad code via FPDF_SaveAsCopy():

1) OutOfProcessInstance::SaveToBuffer() - this code is behind a flag. The flag only defaults to on for Chrome OS. There's no experiments to turn on the flag. It's used when saving a PDF with form changes.

2) ConvertDocToBuffer() in pdfium_print.cc. This in turn is called by a bunch of printing-related code. I can't vouch for all the sources of PDFs that feeds into here.


### sr...@google.com (2019-12-23)

approving the merge of CL in https://crbug.com/chromium/1032090#c41 to M80 

merge approved for M80, branch:3987

### go...@chromium.org (2019-12-23)

Please merge your change to M80 branch 3987 ASAP. Thank you.

### sh...@chromium.org (2019-12-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-12-27)

Please merge your change to M80 branch 3987 ASAP. Thank you.

### sh...@chromium.org (2019-12-30)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-01-06)

Please help complete the merges to M80 branch:3987 by eod Monday Jan 6 so your changes can be included in this week's beta release. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-06)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/4411ca1cdecfe304a7db169bc828a3f4fc1e65f5

commit 4411ca1cdecfe304a7db169bc828a3f4fc1e65f5
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Jan 06 23:01:45 2020

M80: Avoid regenerating revision 5 and 6 encryption dictionaries.

Unlike revision 2 and 3, revision 5 and 6 encryption is not tied to the
document ID in the trailer. Thus regenerating the encryption dictionary
when the ID changes is completely unnecessary. Avoid doing this.

Unlike https://pdfium-review.googlesource.com/c/pdfium/+/63933, this
merge CL does not include the tests.

Change-Id: I074a9b6e03bcaa39c8fb18eed6487454bdc5bcd1
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/63933
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
(cherry picked from commit aeecf1ab623450ec12aaeacd5fab476472124ee7)

Bug: chromium:1032090
Change-Id: I16f5fb26c4abc3519a1042ef00a699919718f795
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/64673
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/4411ca1cdecfe304a7db169bc828a3f4fc1e65f5/core/fpdfapi/edit/cpdf_creator.cpp


### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1032090?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050928)*
