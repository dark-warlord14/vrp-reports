# WebCore::Document::recalcStyleSelector+0x7c

| Field | Value |
|-------|-------|
| **Issue ID** | [40079041](https://issues.chromium.org/issues/40079041) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | wo...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-02-08 |
| **Bounty** | $500.00 |

## Description

Hi, I think I found a bug of chrome, I test it on chrome 4 and 3 ,on 
version 4, maybe you need refresh some times, it works, and the stack like 
this:

00aff7a4 01c78fca 00084000 00000000 008f2e70 chrome_1c30000!
WebCore::Document::recalcStyleSelector+0x7c (CONV: thiscall) 
[c:\b\slave\chrome-official-2
\build\src\third_party\webkit\webcore\dom\document.cpp @ 2340]
00aff7b8 01cbc6cf 00000000 00d9a3c0 00d9a3c0 chrome_1c30000!
WebCore::Document::updateStyleSelector+0x4a (CONV: thiscall) 
[c:\b\slave\chrome-official-2
\build\src\third_party\webkit\webcore\dom\document.cpp @ 2271]
00aff7c8 01cbc6cf 00000000 00d9a440 00d9a440 chrome_1c30000!
WebCore::ContainerNode::removedFromDocument+0x4a (FPO: [0,1,2]) (CONV: 
thiscall) [c:\b\slave\chrome-official-2
\build\src\third_party\webkit\webcore\dom\containernode.cpp @ 608]
00aff7d8 01cbc6cf 00000000 008f78c0 008f78c0 chrome_1c30000!
WebCore::ContainerNode::removedFromDocument+0x4a (FPO: [0,1,2]) (CONV: 
thiscall) [c:\b\slave\chrome-official-2
\build\src\third_party\webkit\webcore\dom\containernode.cpp @ 608]
00aff7e8 01cbc6cf 00000000 008f4c30 008f4f00 chrome_1c30000!
WebCore::ContainerNode::removedFromDocument+0x4a (FPO: [0,1,2]) (CONV: 
thiscall) [c:\b\slave\chrome-official-2
\build\src\third_party\webkit\webcore\dom\containernode.cpp @ 608]
00aff7f8 01cbd08a 008f7e00 008f4ca4 01cbcffd chrome_1c30000!
WebCore::ContainerNode::removedFromDocument+0x4a (FPO: [0,1,2]) (CONV: 
thiscall) [c:\b\slave\chrome-official-2
\build\src\third_party\webkit\webcore\dom\containernode.cpp @ 608]
00aff804 01cbcffd 00aff820 00aff81c 008f4ca4 chrome_1c30000!
WebCore::Private::addChildNodesToDeletionQueue<WebCore::Node,WebCore::Conta
inerNode>+0x43 (FPO: [2,0,0]) (CONV: cdecl) [c:\b\slave\chrome-official-2
\build\src\third_party\webkit\webcore\dom\containernodealgorithms.h @ 139]

Maybe  this one is like those I have reported to ZDI, if so, forget it.

by the way, I got a lot of unexploitable bugs of chrome, These bugs are 
valuable? 




## Attachments

- [webkit21.rar](attachments/webkit21.rar) (application/x-rar, 1.0 KB)

## Timeline

### sc...@gmail.com (2010-02-10)

Thanks for the report, wooshi.

Are you the same person as Wushi from Team509? If so, pleased to meet you and I've 
been a fan of many of your bugs :)

I also can reproduce the crash. Do you have a reference (WebKit bug or ZDI 
identifier) that you think could be the same? (I tried this on Safari 4 and it does 
not seem to crash).

When you say "unexploitable" bugs, what type of bugs do you mean? Memory corruptions 
inside the sandbox would still typically be eligible for a $500 reward. NULL pointer 
derefs, recursion stack overflows, memory exhaustions, etc. typically would not be 
eligible for a reward.

### sc...@gmail.com (2010-02-10)

Looks like use of a toast virtual function pointer? I wouldn't be surprised, since 
this seems to play with SVG <use> support, which has been known to have stale pointer 
issues in the past...

http://crash/reportdetail?reportid=4c20c6a6953fad0c

0xffffffff			
0x01f489d2	 [chrome.dll	 - document.cpp:2390]	
WebCore::Document::updateStyleSelector()
0x01f84530	 [chrome.dll	 - containernode.cpp:609]	
WebCore::ContainerNode::removedFromDocument()
0x01f84530	 [chrome.dll	 - containernode.cpp:609]	
WebCore::ContainerNode::removedFromDocument()
0x01f84530	 [chrome.dll	 - containernode.cpp:609]	
WebCore::ContainerNode::removedFromDocument()
0x01f84530	 [chrome.dll	 - containernode.cpp:609]	
WebCore::ContainerNode::removedFromDocument()
0x01f85070	 [chrome.dll	 - containernodealgorithms.h:139]	
WebCore::Private::addChildNodesToDeletionQueue<WebCore::Node,WebCore::ContainerNode>(
WebCore::Node * &,WebCore::Node * &,WebCore::ContainerNode *)
0x01f84fe3	 [chrome.dll	 - containernodealgorithms.h:47]	
WebCore::removeAllChildrenInContainer<WebCore::Node,WebCore::ContainerNode>(WebCore::
ContainerNode *)
0x01f838c2	 [chrome.dll	 - containernode.cpp:61]	
WebCore::ContainerNode::~ContainerNode()
0x0206fbd6	 [chrome.dll	 - svgelement.cpp:74]	
WebCore::SVGElement::~SVGElement()
0x0206e014	 [chrome.dll	 - svgstyledelement.cpp:59]	
WebCore::SVGStyledElement::~SVGStyledElement()
0x020ea7fb	 [chrome.dll	 - svgstyledlocatableelement.cpp:41]	
WebCore::SVGStyledLocatableElement::~SVGStyledLocatableElement()
0x0206eb30	 [chrome.dll	 - svgstyledtransformableelement.cpp:47]	
WebCore::SVGStyledTransformableElement::~SVGStyledTransformableElement()
0x0206f1cf	 [chrome.dll	 + 0x0043f1cf]	WebCore::SVGGElement::`scalar 
deleting destructor'(unsigned int)
0x01d25cb0	 [chrome.dll	 - user_data_dir_dialog.cc:62]	
RepostFormWarningView::DeleteDelegate()
0x020de5c1	 [chrome.dll	 - refptr.h:132]	
WTF::RefPtr<WebCore::HTMLMapElement>::operator=(WebCore::HTMLMapElement *)
0x01f9766b	 [chrome.dll	 - svguseelement.cpp:350]	
WebCore::SVGUseElement::buildPendingResource()
0x01f97350	 [chrome.dll	 - svguseelement.cpp:178]	
WebCore::SVGUseElement::recalcStyle(WebCore::Node::StyleChange)
0x01f4fe30	 [chrome.dll	 - element.cpp:876]	
WebCore::Element::recalcStyle(WebCore::Node::StyleChange)
0x01f47257	 [chrome.dll	 - document.cpp:1285]	
WebCore::Document::recalcStyle(WebCore::Node::StyleChange)
0x01f472fe	 [chrome.dll	 - document.cpp:1327]	
WebCore::Document::updateStyleIfNeeded()
0x01f4735c	 [chrome.dll	 - document.cpp:1344]	
WebCore::Document::updateStyleForAllDocuments()
0x0202c2a1	 [chrome.dll	 - scriptcontrollerbase.cpp:50]	
WebCore::ScriptController::executeScript(WebCore::ScriptSourceCode const &)
0x0200f3d5	 [chrome.dll	 - xmltokenizerlibxml2.cpp:869]	
WebCore::XMLTokenizer::endElementNs()

### sc...@gmail.com (2010-02-10)

Possibly good for $500 if this is indeed not a duplicate.

### ma...@gmail.com (2010-02-17)

Looping in some people who might know the svg code. This is apparently fixed in WebKit 
ToT, and the question on the table is "can we patch the 249 branch to avoid this, or do 
we need to bring in a series of webkit changes to <use> in svg?"

### bu...@gmail.com (2010-02-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=39544 

------------------------------------------------------------------------
r39544 | mal@chromium.org | 2010-02-19 21:11:26 -0800 (Fri, 19 Feb 2010) | 4 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-events-crash-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-on-disallowed-foreign-object-1-expected.checksum?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-on-disallowed-foreign-object-1-expected.png?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-on-disallowed-foreign-object-1-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-on-disallowed-foreign-object-3-expected.checksum?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-on-disallowed-foreign-object-3-expected.png?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-on-disallowed-foreign-object-3-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-on-disallowed-foreign-object-4-expected.checksum?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-on-disallowed-foreign-object-4-expected.png?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-on-disallowed-foreign-object-4-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-on-non-svg-namespaced-element-expected.checksum?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-on-non-svg-namespaced-element-expected.png?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-on-non-svg-namespaced-element-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-recursion-1-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-recursion-2-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-recursion-3-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/custom/use-recursion-4-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/hixie/error/017-expected.checksum?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/hixie/error/017-expected.png?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win/LayoutTests/svg/hixie/error/017-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win-vista/LayoutTests/svg/custom/use-on-disallowed-foreign-object-1-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win-vista/LayoutTests/svg/custom/use-on-disallowed-foreign-object-3-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win-vista/LayoutTests/svg/custom/use-on-disallowed-foreign-object-4-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win-vista/LayoutTests/svg/custom/use-on-non-svg-namespaced-element-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/data/layout_tests/platform/chromium-win-vista/LayoutTests/svg/hixie/error/017-expected.txt?r1=39544&r2=39543
   M http://src.chromium.org/viewvc/chrome/branches/249/src/webkit/tools/layout_tests/test_expectations.txt?r1=39544&r2=39543

Updated test expectations for svg <use> crash fix.

BUG= http://crbug.com/34978
TEST= layout tests pass on build bots.
------------------------------------------------------------------------


### bu...@gmail.com (2010-02-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=39545 

------------------------------------------------------------------------
r39545 | mal@chromium.org | 2010-02-19 21:21:27 -0800 (Fri, 19 Feb 2010) | 7 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/ChangeLog?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/W3C-SVG-1.1/animate-elem-40-t-expected.txt?r1=39545&r2=39544
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-content-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-content-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-content-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-deep-shadow-tree-content-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-deep-shadow-tree-content-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-deep-shadow-tree-content-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-shadow-tree-content-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-shadow-tree-content-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-shadow-tree-content-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-shadow-tree-content-with-symbol-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-shadow-tree-content-with-symbol-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-shadow-tree-content-with-symbol-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-use-on-symbol-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-use-on-symbol-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/relative-sized-use-on-symbol-expected.txt
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/use-dynamic-append-expected.txt?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/use-events-crash-expected.txt?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/use-on-disallowed-foreign-object-1-expected.txt?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/use-on-disallowed-foreign-object-3-expected.txt?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/use-on-disallowed-foreign-object-4-expected.txt?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/use-on-non-svg-namespaced-element-expected.txt?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/use-recursion-1-expected.txt?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/use-recursion-2-expected.txt?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/use-recursion-3-expected.txt?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/custom/use-recursion-4-expected.txt?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/hixie/error/017-expected.txt?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/text/text-text-05-t-expected.checksum?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/mac/svg/text/text-text-05-t-expected.png?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/platform/win/Skipped?r1=39545&r2=39544
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/relative-sized-content.xhtml
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/relative-sized-deep-shadow-tree-content.xhtml
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/relative-sized-shadow-tree-content-with-symbol.xhtml
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/relative-sized-shadow-tree-content.xhtml
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/relative-sized-use-on-symbol.xhtml
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/resources/use-instanceRoot-event-bubbling.js?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/resources/use-instanceRoot-event-listeners.js?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-clipped-hit.svg?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-dynamic-append.svg?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-instanceRoot-as-event-target-expected.txt?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-instanceRoot-as-event-target.xhtml?r1=39545&r2=39544
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-instanceRoot-event-listener-liveness-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/custom/use-instanceRoot-event-listener-liveness.xhtml
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/LayoutTests/svg/text/text-text-05-t.svg?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/GNUmakefile.am?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/WebCore.gypi?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/WebCore.pro?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/WebCore.vcproj/WebCore.vcproj?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/bindings/js/ScriptEventListener.cpp?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/bindings/v8/ScriptEventListener.cpp?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/dom/Node.cpp?r1=39545&r2=39544
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/manual-tests/svg-crash-hovering-use.svg
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/rendering/RenderSVGContainer.cpp?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/rendering/RenderSVGHiddenContainer.cpp?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/rendering/RenderSVGRoot.cpp?r1=39545&r2=39544
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/rendering/RenderSVGShadowTreeRootContainer.cpp
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/rendering/RenderSVGShadowTreeRootContainer.h
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/rendering/RenderSVGTransformableContainer.cpp?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/rendering/SVGRenderSupport.cpp?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/rendering/SVGRenderSupport.h?r1=39545&r2=39544
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/rendering/SVGShadowTreeElements.cpp
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/rendering/SVGShadowTreeElements.h
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/svg/SVGElement.cpp?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/svg/SVGElement.h?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/svg/SVGElementInstance.cpp?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/svg/SVGElementInstance.h?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/svg/SVGGElement.h?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/svg/SVGSVGElement.h?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/svg/SVGStyledElement.cpp?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/svg/SVGStyledElement.h?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/svg/SVGSymbolElement.h?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/svg/SVGUseElement.cpp?r1=39545&r2=39544
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/249/WebCore/svg/SVGUseElement.h?r1=39545&r2=39544

Fix a crash in svg with <use>.

BUG= http://crbug.com/34978
TEST= layout tests.

TBR= eseidel, cevans  (mostly FYI)
Review URL: http://codereview.chromium.org/652017
------------------------------------------------------------------------


### ma...@gmail.com (2010-02-20)

Ouch.

Hoping I don't have to revert because of test failures.

This is slated for a 4.1.249.xxxx update.

If anyone can figure out why some of the <clip> tests are failing (LayoutTests/svg/custom/clip-path-referencing-use.svg) that'd be awesome.

A typical text diff looks like

-KCanvasResource {id="clip" [type=CLIPPER] [clip data=[[winding=NON-ZERO] [path=M0.00,0.00 L200.00,0.00 L200.00,200.00 L0.00,200.00 Z]]]}
+KCanvasResource {id="clip" [type=CLIPPER] [clip data=[[winding=EVEN-ODD] [path=M0.00,0.00 L0.00,0.00 L0.00,0.00 L0.00,0.00 Z]]]}

I can't figure out why the path is all zeroes and the winding is EVEN-ODD.

### ma...@gmail.com (2010-02-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-02-24)

@wooshi: thanks again for the information. As you can see this bug was fixed in latest 
WebKit, but we needed to backport it. Subject to continued responsible disclosure, 
we'd like to offer you a $500 Chromium reward. Please e-mail me at cevans@chromium.org 
if you wish to accept.

For purposes of issuing credit, what is your <Name> of <Optional affiliation> ?

### sc...@gmail.com (2010-03-23)

Releasing due to fix in 4.1.249.1036.

### ku...@gmail.com (2010-03-24)

[Comment Deleted]

### ge...@gmail.com (2010-08-29)

Is it $500 or $509? https://sites.google.com/a/chromium.org/dev/Home/chromium-security

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/34978?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-04)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079041)*
