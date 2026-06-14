# Yet another double-free caused by malformed XPath expression in XSLT

| Field | Value |
|-------|-------|
| **Issue ID** | [40094117](https://issues.chromium.org/issues/40094117) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **CVE IDs** | CVE-2011-2834 |
| **Reporter** | ya...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-08-19 |
| **Bounty** | $1,000.00 |

## Description

This bug is quite similar in nature to <https://crbug.com/chromium/63444> and 89402. When the XPath engine processes some malformed expression, say //book[hello:world()][1], it first evaluates the //book part, resulting in a node set filled with book elements. After that, each of these elements is set as the new context node where subsequent predicate [hello:world()] is evaluated. This evaluation happens in function xmlXPathCompOpEvalPositionalPredicate() of xpath.c, and after a series of calls from that function, control finally moves into xmlXPathCompOpEval(), where the following code is executed:

13392 if (op->value5 == NULL)  

13393 func =  

13394 xmlXPathFunctionLookup(ctxt->context,  

13395 op->value4);  

13396 else {  

13397 URI = xmlXPathNsLookup(ctxt->context, op->value5);  

13398 if (URI == NULL) {  

13399 xmlGenericError(xmlGenericErrorContext,  

13400 "xmlXPathCompOpEval: function %s bound to undefined prefix %s\n",  

13401 (char \*)op->value4, (char \*)op->value5);  

13402 return (total);  

13403 }  

13404 func = xmlXPathFunctionLookupNS(ctxt->context,  

13405 op->value4, URI);  

13406 }  

13407 if (func == NULL) {  

13408 xmlGenericError(xmlGenericErrorContext,  

13409 "xmlXPathCompOpEval: function %s not found\n",  

13410 (char \*)op->value4);  

13411 XP\_ERROR0(XPATH\_UNKNOWN\_FUNC\_ERROR);  

13412 }

The code first calls xmlXPathNsLookup() to look for the namespace prefix 'hello', which obviously would fail and return NULL. Then this failure is signaled by a call to xmlGenericError() and control returns afterwards without setting any flags to indicate this error, like the code in line 13411 does.

14036 xmlXPathCompOpEval(ctxt, op);  

14037 if (ctxt->error != XPATH\_EXPRESSION\_OK)  

14038 return(-1);  

14039  

14040 resObj = valuePop(ctxt);  

14041 if (resObj == NULL)  

14042 return(-1);  

14043 break;  

14044 }  

14045  

14046 if (resObj) {  

14047 int res;  

14048  

14049 if (resObj->type == XPATH\_BOOLEAN) {  

14050 res = resObj->boolval;  

14051 } else if (isPredicate) {  

14052 /\*  

14053 \* For predicates a result of type "number" is handled  

14054 \* differently:  

14055 \* SPEC XPath 1.0:  

14056 \* "If the result is a number, the result will be converted  

14057 \* to true if the number is equal to the context position  

14058 \* and will be converted to false otherwise;"  

14059 \*/  

14060 res = xmlXPathEvaluatePredicateResult(ctxt, resObj);  

14061 } else {  

14062 res = xmlXPathCastToBoolean(resObj);  

14063 }  

14064 xmlXPathReleaseObject(ctxt->context, resObj);  

14065 return(res);  

14066 }

Now we've returned from xmlXPathCompOpEval() at line 14036. Since the error check in line 14037 doesn't reveal anything exceptional, the code assumes the XPath function was found and its result had been placed in the value table. So this 'resObj' is popped up from the value table (line 14040), converted to a boolean value (line 14060), and finally released by xmlXPathReleaseObject (line 14064). Actually this 'resObj' is the context object, wrapping one of the book elements from the aforementioned node set. This context object would be explicitly released afterwards, resulting in a double-free bug.

**VERSION**  

Chrome Version: 13.0.782.112 (Official Build 95650) / 15.0.857.0 (Developer Build 97295)  

Operating System: Windows XP SP3

**REPRODUCTION CASE**  

Please see the attached files (repro.html, demo.xml and demo.xsl). Put them in the same web directory, load repro.html in the browser and a sad tab would show up.

## Attachments

- [demo.xml](attachments/demo.xml) (application/xml; charset=us-ascii, 293 B)
- [repro.html](attachments/repro.html) (text/plain; charset=us-ascii, 77 B)
- [demo.xsl](attachments/demo.xsl) (application/xml; charset=us-ascii, 321 B)

## Timeline

### sc...@gmail.com (2011-08-19)

Let me see if my patch fixes this one too or not...

### sc...@gmail.com (2011-08-24)

Nope, definitely a new one. How many of these do you have, Yang?? :)

### ya...@gmail.com (2011-08-25)

Actually, none. I've completed the new round of test where the XPath engine has gone through a suite of test cases that sum up to 3GB+ in size. This is the only issue it turned out. So I doubt if there would be a new bug report titled 'Yet yet another double-free...' :-D

### sc...@gmail.com (2011-08-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-26)

Thanks for all your work on this Yang! Glad that things are looking more solid.
I've landed a simple fix to Chromium which simply sets the error flag in a couple of cases involving unknown prefix names.
I don't think any web pages should be depending on execution somehow continuing after using an invalid namespace, so the change should be safe for Chromium :D
I've pinged upstream libxml about whether it's a correct fix or not.


### ve...@gmail.com (2011-08-26)

Okay, I will look quickly. Do you have a CVE handy for it ?

  thanks,

Daniel

### sc...@gmail.com (2011-08-26)

Sure, use CVE-2011-2834

### sc...@gmail.com (2011-08-29)

Merged r98359 to M14 at r98648

### sc...@gmail.com (2011-09-08)

@yangdingning: thanks again for all your work on XPath! My pleasure to offer another $1000 Chromium Security Reward.

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

### sc...@gmail.com (2011-09-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-09-23)

Payment in system.

### js...@chromium.org (2011-10-05)

Batch update.

### ve...@gmail.com (2011-10-11)

BTW I commited upstream a fix which augments Chris patch with
a few other places where the interpretor was forgetting to set the
context error :-) I don't think they are big issues, one is a case of out
of memory error and the other one if the XPath compiled representation
is somehow broken, unlikely to happen:

http://git.gnome.org/browse/libxml2/commit/?id=1d4526f6f4ec8d18c40e2a09b387652a6c1aa2cd

  thanks !

Daniel

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

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

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-20)

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

This issue was migrated from crbug.com/chromium/93472?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094117)*
