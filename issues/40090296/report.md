# mXSS: Potential XSS via MathML gotten from innerHTML

| Field | Value |
|-------|-------|
| **Issue ID** | [40090296](https://issues.chromium.org/issues/40090296) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>HTML>Parser |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2018-01-25 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3329.1 Safari/537.36

Steps to reproduce the problem:
Chrome returns HTML of different structure when a crafted HTML including MathML is gotten from innerHTML property.

By abusing this behavior, an attacker might do XSS attacks by changing safe HTML to XSS-able HTML.
This type of bug is known as "mXSS" (mutation-based XSS). For more information, see this paper: https://cure53.de/fp170.pdf

Steps to Reproduce:
1. Go to https://vulnerabledoma.in/chrome_mxss_mathml_annotation-xml.html . This page has a crafted HTML including MathML like the following:

<math><annotation-xml encoding="text/html"><xmp>&lt;/xmp&gt;&lt;img src=x onerror=alert(1)&gt;</xmp></math>

2. Click "Reassign user-generated HTML to innerHTML" button.  JavaScript is executed by being changed to XSS-able HTML like the following:

<math><annotation-xml encoding="text/html"><xmp></xmp><img src=x onerror=alert(1)></xmp></math>

What is the expected behavior?
Chrome should not change the HTML structure in innerHTML.

What went wrong?
Chrome should return correct HTML.

Did this work before? N/A 

Chrome version: 66.0.3329.1  Channel: n/a
OS Version: 10.0
Flash Version: 

As far as I know, a script and style tag also have same issue:

<math><annotation-xml encoding="text/html"><style>&lt;/style&gt;&lt;img src=x onerror=alert(1)&gt;</style></math>
<math><annotation-xml encoding="text/html"><script>&lt;/script&gt;&lt;img src=x onerror=alert(1)&gt;</script></math>

## Timeline

### el...@chromium.org (2018-01-28)

Cool issue, thanks!

Verified repro in 64-66 on Mac; not repro in Firefox.

[Monorail components: Blink>HTML]

### me...@chromium.org (2018-01-30)

The only other mXSS bug we have is https://crbug.com/chromium/527499 and it's low severity so I'm assigning the same here. I don't think we support MathML and it doesn't seem to have an owner, so not sure who should own this.

### me...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### tk...@chromium.org (2018-03-14)

I think this is an HTML parser bug.
If <xmp> is in a <annotation-xml>, it seems the <xmp> doesn't trigger RAW TEXT parsing mode. On the other hand, HTML serializer correctly handle <xmp> content as RAW TEXT.



[Monorail components: -Blink>HTML Blink>HTML>Parser]

### tk...@chromium.org (2018-03-14)

Oh, no, it may be a serializer bug.
Even if <xmp> content should be serialized as raw text, we need to escape </xmp>.  Safari and Firefox do it.



[Monorail components: -Blink>HTML>Parser Blink>HTML]

### tk...@chromium.org (2018-03-15)

I identified an HTMLTreeBuilderSimulator bug.


[Monorail components: -Blink>HTML Blink>HTML>Parser]

### bu...@chromium.org (2018-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/133bc5c262b2555af223263452e9875a95db9eb7

commit 133bc5c262b2555af223263452e9875a95db9eb7
Author: Kent Tamura <tkent@chromium.org>
Date: Fri Mar 16 05:33:23 2018

HTML parser: Fix "HTML integration point" implementation in HTMLTreeBuilderSimulator.

HTMLTreeBuilderSimulator assumed only <foreignObject> as an HTML
integration point. This CL adds <annotation-xml>, <desc>, and SVG
<title>.

Bug: 805924
Change-Id: I6793d9163d4c6bc8bf0790415baedddaac7a1fc2
Reviewed-on: https://chromium-review.googlesource.com/964038
Commit-Queue: Kent Tamura <tkent@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Cr-Commit-Position: refs/heads/master@{#543634}
[add] https://crrev.com/133bc5c262b2555af223263452e9875a95db9eb7/third_party/WebKit/LayoutTests/external/wpt/html/syntax/parsing/html-integration-point.html
[modify] https://crrev.com/133bc5c262b2555af223263452e9875a95db9eb7/third_party/WebKit/Source/core/html/parser/HTMLTreeBuilderSimulator.cpp
[modify] https://crrev.com/133bc5c262b2555af223263452e9875a95db9eb7/third_party/WebKit/Source/core/html/parser/HTMLTreeBuilderSimulator.h


### tk...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-11)

Hi! The Chrome VRP Panel decided to award $500 for this report - cheers!

### aw...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/805924?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090296)*
