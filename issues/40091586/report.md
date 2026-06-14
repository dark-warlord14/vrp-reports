# Parsing issue with -webkit-calc

| Field | Value |
|-------|-------|
| **Issue ID** | [40091586](https://issues.chromium.org/issues/40091586) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | mi...@chromium.org |
| **Created** | 2011-06-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

the following is badly parsed:  

<a style="-webkit-box-reflect:above 1px -webkit-calc(1)">

**VERSION**  

Chrome Version: beta and daily, not stable.

Google Chrome 12.0.742.77 (Official Build 87574) beta  

WebKit 534.30 (branches/chromium/742@87761)

Chromium 14.0.786.0 (Developer Build 87939) Ubuntu 11.04  

OS Linux  

WebKit 535.1 (trunk@88122)

Operating System: ubuntu 64bits

**REPRODUCTION CASE**  

<a style="-webkit-box-reflect:above 1px -webkit-calc(1)">

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:  

Address 0x3ff0000000000000 is not stack'd, malloc'd or (recently) free'd  

Process terminating with default action of signal 11 (SIGSEGV)  

General Protection Fault  

\_ZN7WebCoreL17equalIgnoringCaseERKNS\_15CSSParserStringEPKc.clone.5 (CSSParser.cpp:144)  

WebCore::CSSParser::isGeneratedImageValue(WebCore::CSSParserValue\*) const (CSSParser.cpp:5542)

## Attachments

- [calc.html](attachments/calc.html) (text/plain; charset=us-ascii, 58 B)
- [vg-85003.txt](attachments/vg-85003.txt) (text/x-c; charset=us-ascii, 7.8 KB)

## Timeline

### mi...@gmail.com (2011-06-05)

vg log

### sc...@gmail.com (2011-06-06)

Please tell me that's different from the other CSS calc() parsing bug? It would be embarrassing if we had to pay you for the same bug twice :)


### in...@chromium.org (2011-06-06)

calc() looks to come back, the stack is different but results in the same bad valuelist. This probably regressed in http://trac.webkit.org/changeset/83415.

Mike, can you please take a look. Also, can you please try to look into some more error scenarios when parsing -webkit-calc. We want more failsafe parsing :)

m_valueList has bad data after the parsing. Its 2nd and 3rd indexes are bad.

bool CSSParser::parseBorderImage(int propId, bool important, RefPtr<CSSValue>& result)
{
    // Look for an image initially.  If the first value is not a URI, then we're done.
    BorderImageParseContext context(primitiveValueCache());
    CSSParserValue* val = m_valueList->current();
    if (val->unit == CSSPrimitiveValue::CSS_URI && m_styleSheet) {
        // FIXME: The completeURL call should be done when using the CSSImageValue,
        // not when creating it.
        context.commitImage(CSSImageValue::create(m_styleSheet->completeURL(val->string)));
    } else if (isGeneratedImageValue(val)) {

### in...@chromium.org (2011-06-06)

Thanks miaubiz for finding this nice parsing bug, this is an interesting area and it will be awesome to find more bugs other than calc :)

### mi...@chromium.org (2011-06-06)

Gah! Will take a look now.

And believe me - I do want failsafe parsing! :(

### sc...@gmail.com (2011-06-06)

Thanks, Mike.
It looks like we'll ship this security regression to M12 on account of unfortunate timing. We'll want to patch it in the first M12 security patch, so getting it fixed over the next few days would be ideal.

### mi...@chromium.org (2011-06-08)

The correct code was already in the master calc patch - I mistakenly sliced it out when carving off a smaller patch <facepalm>. Fortunately it's a simple fix that should patch cleanly.

Filed as a security bug at https://bugs.webkit.org/show_bug.cgi?id=62276

### mi...@chromium.org (2011-06-08)

I've uploaded the fix and tests on the webkit bug. Sorry I didn't get to this sooner (been sick the last few days).

### in...@chromium.org (2011-06-09)

http://trac.webkit.org/changeset/88448

### sc...@gmail.com (2011-06-09)

Thanks for getting to this so quickly Mike, much appreciated. We'll take care of the rest (merging to M12 first patch etc).

### mi...@chromium.org (2011-06-10)

No worries. I'm just sorry to have left the bug in there in the first place :(

### sc...@gmail.com (2011-06-14)

Merged to M13: http://trac.webkit.org/changeset/88749
Merged to M12: http://trac.webkit.org/changeset/88750

### sc...@gmail.com (2011-06-16)

@miaubiz: thanks for catching this regression and enabling us to fix it quickly. Definitely happy to offer you a $1000 Chromium Security Reward.

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

This issue was migrated from crbug.com/chromium/85003?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091586)*
