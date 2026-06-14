# Use after free in WebCore::ContainerNode::parserAddChild

| Field | Value |
|-------|-------|
| **Issue ID** | [40091608](https://issues.chromium.org/issues/40091608) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2011-06-06 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

buffer overflow?

**VERSION**  

Chrome Version:

Google Chrome 11.0.696.77 (Official Build 87952)  

WebKit 534.24 (branches/chromium/696@86868)

Chromium 14.0.786.0 (Developer Build 87944) Ubuntu 11.04  

OS Linux  

WebKit 535.1 (trunk@88122)

Operating System: ubuntu 64bit, osx

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:  

Address 0x36855f10 is 0 bytes inside a block of size 120 free'd  

Address 0x4141414141414401 is not stack'd, malloc'd or (recently) free'd  

General Protection Fault  

WebCore::ContainerNode::parserAddChild(WTF::PassRefPtr[WebCore::Node](javascript:void(0);)) (ContainerNode.cpp:686)

vg logs attached for chromium and google chrome

## Attachments

- [parserAddChild.html](attachments/parserAddChild.html) (text/html; charset=us-ascii, 32.1 KB)
- [vg-parserAddChild-google-chrome.txt](attachments/vg-parserAddChild-google-chrome.txt) (text/plain; charset=us-ascii, 7.6 KB)
- [vg-parserAddChild.txt](attachments/vg-parserAddChild.txt) (text/x-c; charset=us-ascii, 28.2 KB)
- [test.html](attachments/test.html) (text/plain; charset=us-ascii, 32.1 KB)
- [test2.html](attachments/test2.html) (text/plain; charset=us-ascii, 32.1 KB)
- [parserAddChild-original.html](attachments/parserAddChild-original.html) (application/xml; charset=us-ascii, 54.2 KB)

## Timeline

### ts...@chromium.org (2011-06-06)

Use-after-free per VG.
Renderer crash in production build, but trips an assert in the debug build:

0x0000000001f2b5c3 in WebCore::HTMLToken::beginEndTag<unsigned short> (
    this=0x7fffe16960b0, characters=105)
    at third_party/WebKit/Source/WebCore/html/parser/HTMLToken.h:110
110	        ASSERT(m_type == Uninitialized);
(gdb) where
#0  0x0000000001f2b5c3 in WebCore::HTMLToken::beginEndTag<unsigned short> (
    this=0x7fffe16960b0, characters=105)
    at third_party/WebKit/Source/WebCore/html/parser/HTMLToken.h:110
#1  0x0000000001f2070e in WebCore::HTMLTokenizer::nextToken (
    this=0x7fffbc0b6640, source=..., token=...)
    at third_party/WebKit/Source/WebCore/html/parser/HTMLTokenizer.cpp:416
#2  0x0000000001f16d6c in WebCore::HTMLDocumentParser::pumpTokenizer (
    this=0x7fffe1696000, mode=WebCore::HTMLDocumentParser::ForceSynchronous)
    at third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:265
#3  0x0000000001f16818 in WebCore::HTMLDocumentParser::pumpTokenizerIfPossible
    (this=0x7fffe1696000, mode=WebCore::HTMLDocumentParser::ForceSynchronous)
    at third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:175
#4  0x0000000001f17146 in WebCore::HTMLDocumentParser::insert (
    this=0x7fffe1696000, source=...)
    at third_party/WebKit/Source/WebCore/html/parser/HTMLDocumentParser.cpp:324
#5  0x00000000023d5d1f in WebCore::Document::write (this=0x7fffe1c4c800, 
    text=..., ownerDocument=0x7fffe1c4c800)
    at third_party/WebKit/Source/WebCore/dom/Document.cpp:2274
#6  0x00000000023d5d81 in WebCore::Document::write (this=0x7fffe1c4c800, 
    text=..., ownerDocument=0x7fffe1c4c800)
    at third_party/WebKit/Source/WebCore/dom/Document.cpp:2284
#7  0x00000000022db59e in WebCore::V8HTMLDocument::writeCallback (args=...)
    at third_party/WebKit/Source/WebCore/bindings/v8/custom/V8HTMLDocumentCustom.cpp:116
#8  0x0000000001822634 in v8::internal::HandleApiCallHelper<false> (args=..., 
    isolate=0x7ffff7e56000) at v8/src/builtins.cc:1105
#9  0x000000000181d3c2 in v8::internal::Builtin_Impl_HandleApiCall (args=..., 
    isolate=0x7ffff7e56000) at v8/src/builtins.cc:1122
#10 0x000000000181d393 in v8::internal::Builtin_HandleApiCall (args=..., 
    isolate=0x7ffff7e56000) at v8/src/builtins.cc:1121



### ts...@chromium.org (2011-06-06)

[Empty comment from Monorail migration]

### ts...@chromium.org (2011-06-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-06)

@abarth: seems to be in html/parser, maybe this is ideal for you to look at? :)

### ab...@chromium.org (2011-06-06)

I can't reproduce at TOT.

### ab...@chromium.org (2011-06-06)

Interesting.  I can repro in 14.0.785.0 canary.

### ab...@chromium.org (2011-06-06)

Silly me.  I had JavaScript disabled because I was looking at a different bug earlier.  I've got it in the debugger now.

### ab...@chromium.org (2011-06-06)

inferno has a fix for this issue.

### in...@chromium.org (2011-06-06)

Filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=62160

### in...@chromium.org (2011-06-07)

Adam is looking at it, so assigning to him.

miaubiz, please note that you will qualify for the bigger reward if you provide a reduced testcase. in this case, you might get an exception since the testcase needed to be big > 32767. as an example, see the clean reduction that i made.

### mi...@gmail.com (2011-06-07)

you can make the first line all A's. attached.

I'm also attaching the original unreduced file for comparison.

### in...@chromium.org (2011-06-09)

http://trac.webkit.org/changeset/88411

### in...@chromium.org (2011-06-09)

Also need to merge http://trac.webkit.org/changeset/88434.

### in...@chromium.org (2011-06-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-14)

Merged to M12: http://trac.webkit.org/changeset/88827, http://trac.webkit.org/changeset/88828


### sc...@gmail.com (2011-06-14)

Merged to M13: http://trac.webkit.org/changeset/88831, http://trac.webkit.org/changeset/88832

MERGE MACHINE

### sc...@gmail.com (2011-06-16)

@miaubiz: thanks! Repro a little large but definitely a $500 Chromium Security Reward for stamping out interesting bugs in the HTML parser.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-07-03)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/85102?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091608)*
