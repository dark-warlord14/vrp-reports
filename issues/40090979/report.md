# pdfium: oob array write in CPDF_StreamParser::ParseNextElement

| Field | Value |
|-------|-------|
| **Issue ID** | [40090979](https://issues.chromium.org/issues/40090979) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-04-02 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.70 Safari/537.36

Steps to reproduce the problem:
../../core/fpdfapi/page/cpdf_streamparser.cpp:277:3: runtime error: index 256 out of bounds for type 'uint8_t [256]'
    #0 0x86138d in CPDF_StreamParser::ParseNextElement() ../../core/fpdfapi/page/cpdf_streamparser.cpp:277:28
    #1 0x8743ce in CPDF_StreamContentParser::Parse(unsigned char const*, unsigned int, unsigned int) ../../core/fpdfapi/page/cpdf_streamcontentparser.cpp:1525:20
    #2 0x7cc1a5 in CPDF_ContentParser::Continue(IFX_PauseIndicator*) ../../core/fpdfapi/page/cpdf_contentparser.cpp:170:24
    #3 0x7df177 in CPDF_PageObjectHolder::ContinueParse(IFX_PauseIndicator*) ../../core/fpdfapi/page/cpdf_pageobjectholder.cpp:40:18
    #4 0x64d090 in FPDF_LoadPage ../../fpdfsdk/fpdfview.cpp:714:10

https://cs.chromium.org/chromium/src/third_party/pdfium/core/fpdfapi/page/cpdf_streamparser.cpp?l=277&rcl=8f4f0ede809a9bae283538f5c6930c5d7ba13585

The code is as follows.

  while (1) {
    // m_WordSize == 255
    if (m_WordSize < kMaxWordBuffer)
      m_WordBuffer[m_WordSize++] = ch;
      // m_WordSize == 256
    ...
  }

  m_WordBuffer[m_WordSize] = 0; // BUG

So while m_WordSize is checked against kMaxWordBuffer (256), it is incremented next line, which causes the invalid access few lines later.

What is the expected behavior?

What went wrong?
^

Did this work before? No 

Chrome version: 66.0.3359.70  Channel: beta
OS Version: Ubuntu 14.04
Flash Version:

## Attachments

- [chromium-828049.pdf](attachments/chromium-828049.pdf) (application/pdf, 330 B)

## Timeline

### pd...@gmail.com (2018-04-02)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-04-02)

Setting serverity low, as it turns out, this can only overwrite the first byte of the adjacent m_wordsize field with a 0, which doesn't seem very useful. If the structure were re-shuffled someday, then this could be more serious.

### ts...@chromium.org (2018-04-02)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-04-02)

I'll cobble a quick fix.  Note that ASAN can't catch these intra-field overflows, first thing I'm going to try is to put the inline array last and see if we get a hit.

### ts...@chromium.org (2018-04-02)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/29530

### th...@chromium.org (2018-04-03)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2018-04-03)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-04-03)

topanel, in case they want to argue for higher severity.

### bu...@chromium.org (2018-04-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fb4fb2f860216f7076d1634dc08d1d88ade52659

commit fb4fb2f860216f7076d1634dc08d1d88ade52659
Author: pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Tue Apr 03 19:33:43 2018

Roll src/third_party/pdfium/ 75304f915..232b918d1 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/75304f915c5c..232b918d1f0f

$ git log 75304f915..232b918d1 --date=short --no-merges --format='%ad %ae %s'
2018-04-03 tsepez Re-arrange so inline vectors come last in structs.
2018-04-03 thestig Roll pdfium/third_party/freetype/src/ 713d68ee9..7109495c5 (21 commits)
2018-04-03 tsepez Off-by-one in CPDF_StreamParser::ParseNextElement()

Created with:
  roll-dep src/third_party/pdfium
BUG=chromium:828049


The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=dsinclair@chromium.org

Change-Id: I2892003f57e749fed8957a758722ec702d166bfd
Reviewed-on: https://chromium-review.googlesource.com/992888
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#547792}
[modify] https://crrev.com/fb4fb2f860216f7076d1634dc08d1d88ade52659/DEPS


### sh...@chromium.org (2018-04-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-16)

Thanks pdknsk@ - the VRP panel decided to award $500 for this report.  Also, how would you like to be credited in the release notes?

### aw...@google.com (2018-04-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### pd...@gmail.com (2018-04-17)

Thanks. Please just credit me as pdknsk.

(An email I sent didn't show up. I guess you cannot email-reply to secret bugs.)

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/828049?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090979)*
