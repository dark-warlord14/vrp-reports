# Security: Out-of-bound access in CFXJSE_FormCalcContext::Lower

| Field | Value |
|-------|-------|
| **Issue ID** | [40091718](https://issues.chromium.org/issues/40091718) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2018-06-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Out-of-bound access in CFXJSE\_FormCalcContext::Lower

**VERSION**  

Operating System: Windows 10  

PDFium with XFA enabled

Steps to reproduce the problem:

1. Build PDFIUm with XFA
2. run ./pdfium\_test.exe ./poc.pdf

Details

Bug is in function `CFXJSE_FormCalcContext::Lower`

```
// static  
void CFXJSE_FormCalcContext::Lower(CFXJSE_Value\* pThis,  
                                   const ByteStringView& szFuncName,  
                                   CFXJSE_Arguments& args) {  
  int32_t argc = args.GetLength();  
  if (argc < 1 || argc > 2) {  
    ToJSContext(pThis, nullptr)->ThrowParamCountMismatchException(L"Lower");  
    return;  
  }  
  
  std::unique_ptr<CFXJSE_Value> argOne = GetSimpleValue(pThis, args, 0);  
  if (ValueIsNull(pThis, argOne.get())) {  
    args.GetReturnValue()->SetNull();  
    return;  
  }  
  
  CFX_WideTextBuf lowStringBuf;  
  ByteString argString = ValueToUTF8String(argOne.get());  
  WideString wsArgString = WideString::FromUTF8(argString.AsStringView());  
  const wchar_t\* pData = wsArgString.c_str();  
  size_t i = 0;  
  while (i < argString.GetLength()) {  
    int32_t ch = pData[i];     // ==> out-of-bound access `pData`  
    if ((ch >= 0x41 && ch <= 0x5A) || (ch >= 0xC0 && ch <= 0xDE))  
      ch += 32;  
    else if (ch == 0x100 || ch == 0x102 || ch == 0x104)  
      ch += 1;  
  
    lowStringBuf.AppendChar(ch);  
    ++i;  
  }  
  lowStringBuf.AppendChar(0);  
  
  args.GetReturnValue()->SetString(  
      FX_UTF8Encode(lowStringBuf.AsStringView()).AsStringView());  
}  
  

```

Function `WideString::FromUTF8` converts string `argString` to unicode string `wsArgString`. After that, the `while` loop uses data from `wsArgString` (`pData` variable) with the length from `argString`! In the case, `argString` contains special character (non-printable character), the result unicode string `wsArgString` has smaller size than string `argString`! So there is out-of-bound access in `while` loop when `pData` from `wsArgString` is smaller than length of `argString`

To trigger this bug, I use the FormCalc function `Lower`. In poc file, i setup a handler for `initialize` event of a form like below:

```
    <event activity="initialize" name="event__initialize">  
        <script contentType="application/x-javascript">  
  
            xfa.resolveNodes('$record.Country.[Lower(Left(Name, 1)) == "a"]');  
  
        </script>  
    </event>  

```

This will trigger FormCalc function `Lower` handler, that is function `CFXJSE_FormCalcContext::Lower`. The string argument is passed to FormCalc function `Lower` is the string `argString`.

## Attachments

- deleted (application/octet-stream, 0 B)
- [stacktrace.txt](attachments/stacktrace.txt) (text/plain, 4.7 KB)

## Timeline

### oc...@chromium.org (2018-06-21)

rharrison, could you please take a look?

severity-medium as it seems to only be a read.

[Monorail components: Internals>Plugins>PDF]

### rh...@chromium.org (2018-06-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-06-21)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/d52a0afaa3e4374dee469e41db4389bf9c61c4a9

commit d52a0afaa3e4374dee469e41db4389bf9c61c4a9
Author: Ryan Harrison <rharrison@chromium.org>
Date: Thu Jun 21 18:29:44 2018

Use the length of calculated string instead of source

In this function a string is converted to UTF8, if there are
non-printing characters in the original string, the generated string
will be shorter. Thus using the original string length for iteration
range will cause an OOB read.

BUG=chromium:854623

Change-Id: I338005476c3de529709f3eae6892d27a6c7f2263
Reviewed-on: https://pdfium-review.googlesource.com/35810
Commit-Queue: Ryan Harrison <rharrison@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/d52a0afaa3e4374dee469e41db4389bf9c61c4a9/fxjs/cfxjse_formcalc_context.cpp
[modify] https://crrev.com/d52a0afaa3e4374dee469e41db4389bf9c61c4a9/fxjs/cfxjse_formcalc_context_embeddertest.cpp


### rh...@chromium.org (2018-06-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e07b592fd25ce35f5b959022f7d1720a974a315f

commit e07b592fd25ce35f5b959022f7d1720a974a315f
Author: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Fri Jun 22 01:07:52 2018

Roll src/third_party/pdfium 3d8131535e6b..c3cc2ab66d3d (4 commits)

https://pdfium.googlesource.com/pdfium.git/+log/3d8131535e6b..c3cc2ab66d3d


git log 3d8131535e6b..c3cc2ab66d3d --date=short --no-merges --format='%ad %ae %s'
2018-06-21 rharrison@chromium.org Clean up constant values for JS alert and beep
2018-06-21 hnakashima@chromium.org Use enum for stages of CPDF_Creator.
2018-06-21 hnakashima@chromium.org Do not save content stream if all page objects were removed from it.
2018-06-21 rharrison@chromium.org Use the length of calculated string instead of source


Created with:
  gclient setdep -r src/third_party/pdfium@c3cc2ab66d3d

The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:854623
TBR=dsinclair@chromium.org

Change-Id: I033b1457e15085df69d794da8d42dfcc3e015713
Reviewed-on: https://chromium-review.googlesource.com/1111057
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#569483}
[modify] https://crrev.com/e07b592fd25ce35f5b959022f7d1720a974a315f/DEPS


### sh...@chromium.org (2018-06-22)

[Empty comment from Monorail migration]

### hu...@gmail.com (2018-07-18)

Hi guys, I just wonder this report is elegant for your bug bounty program? 

### th...@chromium.org (2018-07-18)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-07-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-08-27)

Thanks for the report! The VRP panel decided to award $1,000 for this report - cheers.

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-09-28)

This issue was migrated from crbug.com/chromium/854623?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091718)*
