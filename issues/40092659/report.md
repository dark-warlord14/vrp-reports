# Memory corruption (double free) caused by malformed XPath expression in XSLT

| Field | Value |
|-------|-------|
| **Issue ID** | [40092659](https://issues.chromium.org/issues/40092659) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ya...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-07-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

A memory corruption (double free) bug has been identified in libxml2's XPath engine, which can be triggered in Chrome/Chromium via a malformed XPath expression in XSL transformation. This bug is due to improper error handling of invalid XPath expressions, much like the one described in <https://crbug.com/chromium/63444>. One example of such expression is //book[author[count(count(\*)=2)>10]][1]. When this expression is processed by libxml2, an error is detected and the code moves on to error handling code, popping up remaining values in the value table of the XPath parser context, freeing unnecessary XPath objects, etc. However, in this process the context object is free()ed twice, once in:

(xmlXPathCompOpEvalPositionalPredicate() of xpath.c)  

11843 evaluation\_exit:  

11844 if (contextObj != NULL) {  

11845 if (ctxt->value == contextObj)  

11846 valuePop(ctxt);  

11847 xmlXPathReleaseObject(xpctxt, contextObj); => First free()  

11848 }  

11849 if (exprRes != NULL)  

11850 xmlXPathReleaseObject(ctxt->context, exprRes);

the other in:

(xmlXPathEvalExpression() of xpath.c)  

14964 do {  

14965 tmp = valuePop(pctxt);  

14966 if (tmp != NULL) {  

14967 xmlXPathReleaseObject(ctxt, tmp); => Second free() of the same object (or more precisely, address), memory corrupted  

14968 stack++;  

14969 }  

14970 } while (tmp != NULL);  

14971 if ((stack != 0) && (res != NULL)) {  

14972 xmlGenericError(xmlGenericErrorContext,  

14973 "xmlXPathEvalExpression: %d object left on the stack\n",  

14974 stack);  

14975 }  

14976 xmlXPathFreeParserContext(pctxt);  

14977 return(res);  

14978 }

**VERSION**  

Chrome 12.0.742.122 / Windows XP SP3  

Chromium 14.0.823.0 (Developer Build 92629) / Windows XP SP3  

Chromium 14.0.823.0 (Developer Build 92644 Linux) / Ubuntu 10.04 LTS

**REPRODUCTION CASE**  

Please see the attached files (repro.html, demo.xml and demo.xsl). Put them in the same web directory, load repro.html in the browser and a sad tab would show up.

## Attachments

- [demo.xsl](attachments/demo.xsl) (application/xml; charset=us-ascii, 336 B)
- [repro.html](attachments/repro.html) (text/plain; charset=us-ascii, 77 B)
- [demo.xml](attachments/demo.xml) (application/xml; charset=us-ascii, 293 B)

## Timeline

### sc...@gmail.com (2011-07-15)

I will investigate today, thanks for the report!

### sc...@gmail.com (2011-07-15)

Yes, definitely crash in the allocator on trunk.

#7  0x00007ffff7ff4cee in tc_malloc (size=16)
    at third_party/tcmalloc/chromium/src/tcmalloc.cc:1590
#8  0x00007ffff36b8f99 in xmlXPathNodeSetCreate (val=0x7fffd679de80)


### sc...@gmail.com (2011-07-15)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-15)

[Empty comment from Monorail migration]

### ve...@gmail.com (2011-07-19)

Okay, I can reproduce, I think something serious must be done about those

Daniel

### [Deleted User] (2011-07-19)

[just a new tool sanity check]
I can repro the bug under Dr. Memory on Windows with --single-process=yes

Here are the drmemory reports:
UNADDRESSABLE ACCESS: reading 0x2af418fc-0x2af41900 4 byte(s)     # timurrrr: Use-after-free after the first free()?
Note: next higher malloc: 0x2af41930-0x2af41960
Note: prev lower malloc:  0x2af41818-0x2af41848
 # 1 xmlXPathCacheFreeObjectList                        third_party\libxml\src\xpath.c:1824
 # 2 xmlXPathFreeCache                                  third_party\libxml\src\xpath.c:1843
 # 3 xmlXPathFreeContext                                third_party\libxml\src\xpath.c:6045
 # 4 xsltFreeTransformContext                           third_party\libxslt\libxslt\transform.c:581
 # 5 WebCore::XSLTProcessor::transformToString          third_party\webkit\source\webcore\xml\xsltprocessorlibxslt.cpp:351
 # 6 WebCore::Document::applyXSLTransform               third_party\webkit\source\webcore\dom\document.cpp:3998
 # 7 WebCore::Document::recalcStyleSelector             third_party\webkit\source\webcore\dom\document.cpp:2937
 # 8 WebCore::Document::styleSelectorChanged            third_party\webkit\source\webcore\dom\document.cpp:2825
 # 9 WebCore::Document::removePendingSheet              third_party\webkit\source\webcore\dom\document.cpp:2804
 #10 WebCore::ProcessingInstruction::sheetLoaded        third_party\webkit\source\webcore\dom\processinginstruction.cpp:200
 #11 WebCore::XSLStyleSheet::checkLoaded                third_party\webkit\source\webcore\xml\xslstylesheetlibxslt.cpp:104
 #12 WebCore::ProcessingInstruction::parseStyleSheet    third_party\webkit\source\webcore\dom\processinginstruction.cpp:242
 #13 WebCore::ProcessingInstruction::setXSLStyleSheet   third_party\webkit\source\webcore\dom\processinginstruction.cpp:230
 #14 WebCore::CachedXSLStyleSheet::checkNotify          third_party\webkit\source\webcore\loader\cache\cachedxslstylesheet.cpp:87
 #15 WebCore::CachedXSLStyleSheet::data                 third_party\webkit\source\webcore\loader\cache\cachedxslstylesheet.cpp:77
 #16 WebCore::CachedResourceRequest::didFinishLoading   third_party\webkit\source\webcore\loader\cache\cachedresourcerequest.cpp:166
 #17 WebCore::SubresourceLoader::didFinishLoading       third_party\webkit\source\webcore\loader\subresourceloader.cpp:197
 #18 WebCore::ResourceLoader::didFinishLoading          third_party\webkit\source\webcore\loader\resourceloader.cpp:444
 #19 WebCore::ResourceHandleInternal::didFinishLoading  resourcehandle.cpp:190
 #20 webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest webkit\glue\weburlloader_impl.cc:664
 #21 ResourceDispatcher::OnRequestComplete              content\common\resource_dispatcher.cc:431
 #22 DispatchToMethod<...>

INVALID HEAP ARGUMENT: free 0x2af1ed80     # timurrrr: looks like the second free()
 # 1 xmlXPathCacheFreeObjectList                        third_party\libxml\src\xpath.c:1826
 # 2 xmlXPathFreeCache                                  third_party\libxml\src\xpath.c:1843
 # 3 xmlXPathFreeContext                                third_party\libxml\src\xpath.c:6045
 # 4 xsltFreeTransformContext                           third_party\libxslt\libxslt\transform.c:581
 # 5 WebCore::XSLTProcessor::transformToString          third_party\webkit\source\webcore\xml\xsltprocessorlibxslt.cpp:351
 # 6 WebCore::Document::applyXSLTransform               third_party\webkit\source\webcore\dom\document.cpp:3998
 # 7 WebCore::Document::recalcStyleSelector             third_party\webkit\source\webcore\dom\document.cpp:2937
 # 8 WebCore::Document::styleSelectorChanged            third_party\webkit\source\webcore\dom\document.cpp:2825
 # 9 WebCore::Document::removePendingSheet              third_party\webkit\source\webcore\dom\document.cpp:2804
 #10 WebCore::ProcessingInstruction::sheetLoaded        third_party\webkit\source\webcore\dom\processinginstruction.cpp:200
 #11 WebCore::XSLStyleSheet::checkLoaded                third_party\webkit\source\webcore\xml\xslstylesheetlibxslt.cpp:104
 #12 WebCore::ProcessingInstruction::parseStyleSheet    third_party\webkit\source\webcore\dom\processinginstruction.cpp:242
 #13 WebCore::ProcessingInstruction::setXSLStyleSheet   third_party\webkit\source\webcore\dom\processinginstruction.cpp:230
 #14 WebCore::CachedXSLStyleSheet::checkNotify          third_party\webkit\source\webcore\loader\cache\cachedxslstylesheet.cpp:87
 #15 WebCore::CachedXSLStyleSheet::data                 third_party\webkit\source\webcore\loader\cache\cachedxslstylesheet.cpp:77
 #16 WebCore::CachedResourceRequest::didFinishLoading   third_party\webkit\source\webcore\loader\cache\cachedresourcerequest.cpp:166
 #17 WebCore::SubresourceLoader::didFinishLoading       third_party\webkit\source\webcore\loader\subresourceloader.cpp:197
 #18 WebCore::ResourceLoader::didFinishLoading          third_party\webkit\source\webcore\loader\resourceloader.cpp:444
 #19 WebCore::ResourceHandleInternal::didFinishLoading  resourcehandle.cpp:190
 #20 webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest webkit\glue\weburlloader_impl.cc:664
 #21 ResourceDispatcher::OnRequestComplete              content\common\resource_dispatcher.cc:431
 #22 DispatchToMethod<...>

### [Deleted User] (2011-07-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-29)

@yangdingning: thanks again! I'm going to look at creating a simple patch for this next week.
Did you have any interest in evaluating the other error handling paths for similar bugs? I might as well fix all the obvious ones at once, and of course, any extra bugs would likely lead to a higher reward.

### ya...@gmail.com (2011-07-29)

I'm currently working on improvements of my test case generation tool. When this is done, another round of testing would be carried out on libxml2, but I can't promise that would find anything new :-)
btw, I made my tool to be generic, not tailored for any specific kind of bugs. But the two bugs it was able to find in libxml2 are both related to improper error handling. It might be interesting to develop a tool for this specific kind of bug. I'll try if time permits.

### sc...@gmail.com (2011-08-03)

Thanks for the info, Yang :) I'm going to try and fix this today.

### sc...@gmail.com (2011-08-04)

http://src.chromium.org/viewvc/chrome?view=rev&revision=95382


### sc...@gmail.com (2011-08-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-16)

@yangdingning: thanks again, I'm a big fan of your grammar-based fuzzing. This is a good report and a good bug, hence I'm happy to offer you another $1000 Chromium Security Reward.

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

### ya...@gmail.com (2011-08-19)

@scarybeasts: thanks for your kind words!
FYI, the tool has found another double free bug in libxml2 similar to this one. I've opened https://crbug.com/chromium/93472 to report this bug, hopefully the description in that report will be of some help.

### sc...@gmail.com (2011-08-24)

Payment in system...

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-12-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-07-13)

CC'ing Debian libxml maintainer.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/89402?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092659)*
