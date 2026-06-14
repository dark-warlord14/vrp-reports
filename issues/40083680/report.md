# Bad cast on SVG use element due to mismatched shadow and instance pointers

| Field | Value |
|-------|-------|
| **Issue ID** | [40083680](https://issues.chromium.org/issues/40083680) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ku...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2010-10-10 |
| **Bounty** | $1,000.00 |

## Description

chrome 7.0.544.0 dev chromium 8.0.551.0 (62092)
Operating System: [Windows xp sp3]

testcase.svg
====
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"> 
<feComponentTransfer id="crash"> 
</feComponentTransfer> 
<use xlink:href="#foo"> 
 <view id="foo"> 
  <use xlink:href="#crash"> 
   <use> 
   </use> 
  </use> 
 </view> 
</use> 
</svg>

## Timeline

### in...@chromium.org (2010-10-10)

Thanks kuzzcc for this nice bug.

(bf4.1b30): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=400921fb ebx=04c7f5a0 ecx=04509d80 edx=53a56f50 esi=04509d80 edi=0452cd00
eip=400921fb esp=04bcf1dc ebp=044eba00 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
400921fb ??              ???
0:014> .exr -1
ExceptionAddress: 400921fb
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 400921fb
Attempt to execute non-executable address 400921fb
0:014> kP
ChildEBP RetAddr
WARNING: Frame IP not in any known module. Following frames may be wrong.
04bcf1d8 5348d5c0 0x400921fb
04bcf1f8 5348d587 chrome_522e0000!WebCore::updateContainerOffset(
                        class WebCore::SVGElementInstance * targetInstance = 0x
3a52ed8)+0x50
04bcf21c 5348d587 chrome_522e0000!WebCore::updateContainerOffset(
                        class WebCore::SVGElementInstance * targetInstance = 0x
3a52ed8)+0x17
04bcf240 5348d68b chrome_522e0000!WebCore::updateContainerOffset(
                        class WebCore::SVGElementInstance * targetInstance = 0x
3a52ed8)+0x17
04bcf260 5348f809 chrome_522e0000!WebCore::SVGUseElement::updateContainerOffset
(void)+0x6b
04bcf284 534c35d5 chrome_522e0000!WebCore::SVGUseElement::buildShadowAndInstanc
Tree(
                        class WebCore::SVGShadowTreeRootElement * shadowRoot =
x53a52ed8)+0x209
04bcf2a0 5348d721 chrome_522e0000!WebCore::RenderSVGShadowTreeRootContainer::up
ateFromElement(void)+0xf5
04bcf2b4 52afddb5 chrome_522e0000!WebCore::SVGUseElement::recalcStyle(
                        WebCore::Node::StyleChange change = <Memory access erro
>)+0x71
04bcf2dc 52aaa506 chrome_522e0000!WebCore::Element::recalcStyle(
                        WebCore::Node::StyleChange change = 1403333164 (No matc
ing enumerant))+0x425
04bcf2f8 52aadb3b chrome_522e0000!WebCore::Document::recalcStyle(
                        WebCore::Node::StyleChange change = Inherit (2))+0x166
04bcf304 52c78c9c chrome_522e0000!WebCore::Document::styleSelectorChanged(
                        WebCore::StyleSelectorUpdateFlag updateFlag = 2 (No mat
hing enumerant))+0x9b
04bcf310 52bb1571 chrome_522e0000!WebCore::XMLDocumentParser::end(void)+0x2c

### in...@chromium.org (2010-10-10)

in debugger, hits assert

void SVGUseElement::associateInstancesWithShadowTreeElements(Node* target, SVGElementInstance* targetInstance)
{
    if (!target || !targetInstance)
        return;

    SVGElement* originalElement = targetInstance->correspondingElement();

    if (originalElement->hasTagName(SVGNames::useTag)) {
#if ENABLE(SVG) && ENABLE(SVG_USE)
        // <use> gets replaced by <g>
        ASSERT(target->nodeName() == SVGNames::gTag);

### in...@chromium.org (2010-10-10)

btw, does crash v6 stable as well. :(

### ku...@gmail.com (2010-10-11)

Sorry! too busy to fill the information

### in...@chromium.org (2010-10-11)

[Empty comment from Monorail migration]

### la...@chromium.org (2010-10-12)

Bulk moving to mstone 8, at this point work on m7 should effectively be closed.  If something in this bulk edit is not actively being worked on, please change the mstone to m9.

### js...@chromium.org (2010-10-12)

Reported upstream with more detail: 
https://bugs.webkit.org/show_bug.cgi?id=47561

### in...@chromium.org (2010-10-12)

We should aim v7 1st patch for this.

### js...@chromium.org (2010-10-18)

Landed upstream: http://trac.webkit.org/changeset/69936


### sc...@gmail.com (2010-10-18)

@kuzzcc: congratulations! This provisionally qualifies for a $1000 Chromium Security Reward. Thank you for a very clear report with simple repro and version numbers.
Please, do include an exception record in future reports :)

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

### in...@chromium.org (2010-10-22)

merged to m8 in r70357. m7 in r70358

### js...@chromium.org (2010-11-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-12)

Payment is in electronic system.

### sc...@gmail.com (2010-11-12)

Payment is in electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/58657?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083680)*
