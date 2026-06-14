# pdfium (XFA): wild-addr-read in GetWordBreakProperty

| Field | Value |
|-------|-------|
| **Issue ID** | [40051297](https://issues.chromium.org/issues/40051297) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-01-19 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.130 Safari/537.36

Steps to reproduce the problem:
AddressSanitizer: SEGV on unknown address 0x55ff3c6a0e55 (pc 0x55ff0b9b36d2 bp 0x7ffdfaf8b870 sp 0x7ffdfaf8b870 T0)
The signal is caused by a READ memory access.
SCARINESS: 20 (wild-addr-read)

    #0 0x55ff0b9b36d2 in (anonymous namespace)::GetWordBreakProperty(wchar_t) xfa/fde/cfde_texteditengine.cpp:110:24
    #1 0x55ff0b9b3386 in CFDE_TextEditEngine::Iterator::FindNextBreakPos(bool) xfa/fde/cfde_texteditengine.cpp:1281:32
    #2 0x55ff0b9b310f in CFDE_TextEditEngine::BoundsForWordAt(unsigned long) const xfa/fde/cfde_texteditengine.cpp:1228:27
    #3 0x55ff0ba0fbe0 in CFWL_Edit::OnButtonDoubleClick(CFWL_MessageMouse*) xfa/fwl/cfwl_edit.cpp:1145:47
    #4 0x55ff0ba0f3c1 in CFWL_Edit::OnProcessMessage(CFWL_Message*) xfa/fwl/cfwl_edit.cpp:1024:11
    #5 0x55ff0b94e1b0 in CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp:356:19
    #6 0x55ff0b94e1dc in non-virtual thunk to CXFA_FFTextEdit::OnProcessMessage(CFWL_Message*) xfa/fxfa/cxfa_fftextedit.cpp
    #7 0x55ff0ba29bcc in CFWL_NoteDriver::DispatchMessage(CFWL_Message*, CFWL_Widget*) xfa/fwl/cfwl_notedriver.cpp:148:16
    #8 0x55ff0ba29a8d in CFWL_NoteDriver::ProcessMessage(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_notedriver.cpp:108:8
    #9 0x55ff0ba3a195 in CFWL_WidgetMgr::OnProcessMessageToForm(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fwl/cfwl_widgetmgr.cpp:320:16
    #10 0x55ff0b91e31e in CXFA_FFField::SendMessageToFWLWidget(std::__1::unique_ptr<CFWL_Message, std::__1::default_delete<CFWL_Message> >) xfa/fxfa/cxfa_fffield.cpp:743:32
    #11 0x55ff0b91f200 in CXFA_FFField::OnLButtonDblClk(unsigned int, CFX_PTemplate<float> const&) xfa/fxfa/cxfa_fffield.cpp:448:3
    #12 0x55ff0b953036 in CXFA_FFWidgetHandler::OnLButtonDblClk(CXFA_FFWidget*, unsigned int, CFX_PTemplate<float> const&) xfa/fxfa/cxfa_ffwidgethandler.cpp:78:24
    #13 0x55ff0bbd21bb in CPDFXFA_WidgetHandler::OnLButtonDblClk(CPDFSDK_PageView*, fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int, CFX_PTemplate<float> const&) fpdfsdk/fpdfxfa/cpdfxfa_widgethandler.cpp:435:26
    #14 0x55ff08d67c18 in CPDFSDK_AnnotHandlerMgr::Annot_OnLButtonDblClk(CPDFSDK_PageView*, fxcrt::ObservedPtr<CPDFSDK_Annot>*, unsigned int, CFX_PTemplate<float> const&) fpdfsdk/cpdfsdk_annothandlermgr.cpp:167:9
    #15 0x55ff08dc3caa in CPDFSDK_PageView::OnLButtonDblClk(CFX_PTemplate<float> const&, unsigned int) fpdfsdk/cpdfsdk_pageview.cpp:320:26
    #16 0x55ff08de87eb in FORM_OnLButtonDoubleClick fpdfsdk/fpdf_formfill.cpp:419:21
    #17 0x55ff08d5779b in (anonymous namespace)::SendDoubleClickEvent(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::vector<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >, std::__1::allocator<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > > > const&) samples/pdfium_test_event_helper.cc:132:5
    #18 0x55ff08d56c53 in SendPageEvents(fpdf_form_handle_t__*, fpdf_page_t__*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test_event_helper.cc:160:7
    #19 0x55ff08d4f02f in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:697:5
    #20 0x55ff08d48b22 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:960:9
    #21 0x55ff08d451ca in main samples/pdfium_test.cc:1179:5

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 78.0.3904.130  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-1043510.pdf](attachments/chromium-1043510.pdf) (application/pdf, 831 B)
- [chromium-1043510.evt](attachments/chromium-1043510.evt) (application/octet-stream, 20 B)

## Timeline

### pd...@gmail.com (2020-01-19)

Requires minor user interaction.

1. Double-click field.

### pd...@gmail.com (2020-01-19)

As it is pdfium_test cannot reproduce for lack of double-click support, so this patch is required.

--- a/samples/pdfium_test_event_helper.cc
+++ b/samples/pdfium_test_event_helper.cc
@@ -115,6 +115,24 @@ void SendFocusEvent(FPDF_FORMHANDLE form,
   int y = atoi(tokens[2].c_str());
   FORM_OnFocus(form, page, 0, x, y);
 }
+
+void SendDoubleClickEvent(FPDF_FORMHANDLE form,
+                          FPDF_PAGE page,
+                          const std::vector<std::string>& tokens) {
+  if (tokens.size() != 4 && tokens.size() != 5) {
+    fprintf(stderr, "doubleclick: bad args\n");
+    return;
+  }
+
+  int x = atoi(tokens[2].c_str());
+  int y = atoi(tokens[3].c_str());
+  uint32_t modifiers = tokens.size() >= 5 ? GetModifiers(tokens[4]) : 0;
+
+  if (tokens[1] == "left")
+    FORM_OnLButtonDoubleClick(form, page, modifiers, x, y);
+  else
+    fprintf(stderr, "doubleclick: bad button name\n");
+}
 }  // namespace
 
 void SendPageEvents(FPDF_FORMHANDLE form,
@@ -138,6 +156,8 @@ void SendPageEvents(FPDF_FORMHANDLE form,
       SendMouseMoveEvent(form, page, tokens);
     } else if (tokens[0] == "focus") {
       SendFocusEvent(form, page, tokens);
+    } else if (tokens[0] == "doubleclick") {
+      SendDoubleClickEvent(form, page, tokens);
     } else {
       fprintf(stderr, "Unrecognized event: %s\n", tokens[0].c_str());
     }


### pd...@gmail.com (2020-01-19)

Note: Chrome doesn't use XFA.

### pd...@gmail.com (2020-01-19)

[Comment Deleted]

### pd...@gmail.com (2020-01-19)

[Comment Deleted]

### pd...@gmail.com (2020-01-19)

This seems similar to a bug I once reported where the code only expected wchar_t to be <= 0xFFFF. In this case the value is a bit too far off which causes the SIGSEGV, but a different value which makes this an oob read can be easily produced.

AddressSanitizer: global-buffer-overflow on address 0x55db90eb1514 at pc 0x55db92bb5fb8 bp 0x7ffca01bdf10 sp 0x7ffca01bdf08
READ of size 1 at 0x55db90eb1514 thread T0
SCARINESS: 22 (1-byte-read-global-buffer-overflow-far-from-bounds)

### ct...@chromium.org (2020-01-21)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2020-01-21)

Thanks for the patch.  Always nice to improve the infrastructure.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-21)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/a216865467ddf9430fe1207adcd71c2d5318e3bc

commit a216865467ddf9430fe1207adcd71c2d5318e3bc
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Jan 21 23:57:21 2020

Add doubleclick event handling to pdfium_test_event_helper.cc

As suggested on the referenced bug by reporter.

Bug: chromium:1043510
Change-Id: I7d81240eee405fa24876f969472760e04638c2fa
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/65410
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/a216865467ddf9430fe1207adcd71c2d5318e3bc/samples/pdfium_test_event_helper.cc
[modify] https://pdfium.googlesource.com/pdfium/+/a216865467ddf9430fe1207adcd71c2d5318e3bc/testing/resources/javascript/mouse_events.evt
[modify] https://pdfium.googlesource.com/pdfium/+/a216865467ddf9430fe1207adcd71c2d5318e3bc/testing/resources/javascript/mouse_events_expected.txt


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/86119575bb6df8cfc5b1cbf2543e73d09e2c5de5

commit 86119575bb6df8cfc5b1cbf2543e73d09e2c5de5
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jan 22 09:46:36 2020

Roll src/third_party/pdfium c3e55aa23f88..a216865467dd (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/c3e55aa23f88..a216865467dd

git log c3e55aa23f88..a216865467dd --date=short --first-parent --format='%ad %ae %s'
2020-01-21 tsepez@chromium.org Add doubleclick event handling to pdfium_test_event_helper.cc
2020-01-21 thestig@chromium.org Fix some nits in CPDF_TextPage code.

Created with:
  gclient setdep -r src/third_party/pdfium@a216865467dd

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1043510
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I9254e43b033930e1573eccc14e5d5a0e9f8bc9d5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2013907
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#733917}

[modify] https://crrev.com/86119575bb6df8cfc5b1cbf2543e73d09e2c5de5/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-22)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/60d25a32173d602f98207a1b75e5e5263e5f4181

commit 60d25a32173d602f98207a1b75e5e5263e5f4181
Author: Tom Sepez <tsepez@chromium.org>
Date: Wed Jan 22 17:57:34 2020

Bounds check in GetWordBreakProperty()

wchar_t might be wider than 16 bits on non-windows platforms.

- Make tables static and provide accessor functions.

Bug: chromium:1043510
Change-Id: Ib573971692e8c35d299ed0fb376039878827ef7d
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/65411
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/60d25a32173d602f98207a1b75e5e5263e5f4181/xfa/fde/cfde_texteditengine.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/60d25a32173d602f98207a1b75e5e5263e5f4181/xfa/fde/cfde_wordbreak_data.h
[modify] https://pdfium.googlesource.com/pdfium/+/60d25a32173d602f98207a1b75e5e5263e5f4181/xfa/fde/cfde_wordbreak_data.cpp
[add] https://pdfium.googlesource.com/pdfium/+/60d25a32173d602f98207a1b75e5e5263e5f4181/testing/resources/javascript/xfa_specific/bug_1043510.pdf
[add] https://pdfium.googlesource.com/pdfium/+/60d25a32173d602f98207a1b75e5e5263e5f4181/testing/resources/javascript/xfa_specific/bug_1043510.evt


### ts...@chromium.org (2020-01-22)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a4e6a75d0db43210948fbc7595960638ce0b5c78

commit a4e6a75d0db43210948fbc7595960638ce0b5c78
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jan 23 01:02:48 2020

Roll src/third_party/pdfium a216865467dd..c040c8f85051 (9 commits)

https://pdfium.googlesource.com/pdfium.git/+log/a216865467dd..c040c8f85051

git log a216865467dd..c040c8f85051 --date=short --first-parent --format='%ad %ae %s'
2020-01-22 thestig@chromium.org Clean up CPDF_TextPage.
2020-01-22 thestig@chromium.org Rename FPDF functions in cpdf_formfield.h.
2020-01-22 thestig@chromium.org Rename CPDF_TextPage's enum values to kFoo.
2020-01-22 thestig@chromium.org Git rid of FPDFText_Direction.
2020-01-22 thestig@chromium.org Rename enum class FPDFText_MarkedContent.
2020-01-22 thestig@chromium.org Rename FPDF_CHAR_INFO class to CPDF_TextPage::CharInfo.
2020-01-22 tsepez@chromium.org Tidy cfde_wordbreak_data.cpp
2020-01-22 thestig@chromium.org Run coverage.py with --no-component-view.
2020-01-22 tsepez@chromium.org Bounds check in GetWordBreakProperty()

Created with:
  gclient setdep -r src/third_party/pdfium@c040c8f85051

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1043510
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Ife40755f9b64b19135628feae01f4884b5bb9830
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2015457
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#734286}

[modify] https://crrev.com/a4e6a75d0db43210948fbc7595960638ce0b5c78/DEPS


### sh...@chromium.org (2020-01-23)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-30)

Congrats! The Panel decided to award $7,500 for this report!

### na...@google.com (2020-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-04-30)

This issue was migrated from crbug.com/chromium/1043510?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051297)*
