# mXSS: Potential XSS via noembed tags parsed by DOMParser APIs

| Field | Value |
|-------|-------|
| **Issue ID** | [40094073](https://issues.chromium.org/issues/40094073) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>HTML>Parser |
| **Platforms** | Windows |
| **Reporter** | ma...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2019-02-19 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3710.0 Safari/537.36

Steps to reproduce the problem:
Chrome decodes HTML entities inside <noembed> tags when it is parsed by DOMParser APIs.

For example:
A <noembed> B &lt;/noembed&gt; C &lt;img src=x onerror=alert(1)&gt;  D </noembed> E

This HTML will be:

A <noembed> B </noembed> C <img src=x onerror=alert(1)>  D </noembed> E

You can check this behavior: https://vulnerabledoma.in/chrome_mxss_domparser_noembed.html

By abusing this behavior, an attacker might do XSS attacks by changing safe HTML to XSS-able HTML.
This type of bug is known as "mXSS" (mutation-based XSS). For more information, see this paper: https://cure53.de/fp170.pdf
See also: https://crbug.com/chromium/805924 and https://crbug.com/chromium/527499

As far as I know, only Chrome behaves like this.
I attached the same HTML file as the above PoC.

What is the expected behavior?
Chrome's DOMParser API should not decode HTML entities inside <noembed> tags.

What went wrong?
Chrome's DOMParser API decodes HTML entities inside <noembed> tags.

Did this work before? N/A 

Chrome version: 74.0.3710.0  Channel: canary
OS Version: 10.0
Flash Version:

## Attachments

- [chrome_mxss_domparser_noembed.html](attachments/chrome_mxss_domparser_noembed.html) (text/plain, 660 B)

## Timeline

### me...@chromium.org (2019-02-19)

tkent: Can you PTAL or reassign if necessary? Thanks.

Tentatively assigning low severity based on previous reports (https://crbug.com/chromium/805924 and  https://crbug.com/chromium/527499).

[Monorail components: Blink>HTML]

### tk...@chromium.org (2019-02-20)

I'll ask kouhei@ for review.


[Monorail components: -Blink>HTML Blink>HTML>Parser]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bc45ada2b0d2960c0cbb266f45d927dbc459316d

commit bc45ada2b0d2960c0cbb266f45d927dbc459316d
Author: Kent Tamura <tkent@chromium.org>
Date: Wed Feb 20 04:34:51 2019

domparsing: HTML Parser: Remove conditional parsing of <noembed> content

The HTML Parser had raw text handling for <noembed> content only if plugins
were runnable. However, the HTML specification doesn't ask such behavior,
and it didn't match to our HTML serializer.  We should always handle it as
raw text.

Bug: 933211
Change-Id: Iade5197a14aeffb6b540c8e9f1ed1880c651955b
Reviewed-on: https://chromium-review.googlesource.com/c/1477556
Auto-Submit: Kent Tamura <tkent@chromium.org>
Commit-Queue: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Cr-Commit-Position: refs/heads/master@{#633571}
[modify] https://crrev.com/bc45ada2b0d2960c0cbb266f45d927dbc459316d/third_party/blink/renderer/core/html/parser/html_document_parser.cc
[modify] https://crrev.com/bc45ada2b0d2960c0cbb266f45d927dbc459316d/third_party/blink/renderer/core/html/parser/html_parser_options.cc
[modify] https://crrev.com/bc45ada2b0d2960c0cbb266f45d927dbc459316d/third_party/blink/renderer/core/html/parser/html_parser_options.h
[modify] https://crrev.com/bc45ada2b0d2960c0cbb266f45d927dbc459316d/third_party/blink/renderer/core/html/parser/html_preload_scanner_fuzzer.cc
[modify] https://crrev.com/bc45ada2b0d2960c0cbb266f45d927dbc459316d/third_party/blink/renderer/core/html/parser/html_tokenizer.cc
[modify] https://crrev.com/bc45ada2b0d2960c0cbb266f45d927dbc459316d/third_party/blink/renderer/core/html/parser/html_tokenizer_fuzzer.cc
[modify] https://crrev.com/bc45ada2b0d2960c0cbb266f45d927dbc459316d/third_party/blink/renderer/core/html/parser/html_tree_builder.cc
[modify] https://crrev.com/bc45ada2b0d2960c0cbb266f45d927dbc459316d/third_party/blink/renderer/core/html/parser/html_tree_builder_simulator.cc
[modify] https://crrev.com/bc45ada2b0d2960c0cbb266f45d927dbc459316d/third_party/blink/web_tests/external/wpt/domparsing/DOMParser-parseFromString-html.html


### tk...@chromium.org (2019-02-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-20)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-25)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-28)

Congrats! The Panel decided to reward $500 for this report :)

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### ma...@gmail.com (2019-04-25)

Hello, this bug should have been fixed on Chrome 74 but apparently it is not listed in https://chromereleases.googleblog.com/2019/04/stable-channel-update-for-desktop_23.html
Is it overlooked?

### sh...@chromium.org (2019-05-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/933211?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094073)*
