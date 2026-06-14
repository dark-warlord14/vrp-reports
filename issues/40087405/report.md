# Stale nodes in Document::recalcStyleSelector

| Field | Value |
|-------|-------|
| **Issue ID** | [40087405](https://issues.chromium.org/issues/40087405) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | wo...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-01-31 |
| **Bounty** | $1,000.00 |

## Description

002cf380 692a6e9d 0x690074
002cf3dc 692a6cce chrome_68db0000!WebCore::Document::recalcStyleSelector+0x7e [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\document.cpp @ 2909]
002cf3f0 699306a2 chrome_68db0000!WebCore::Document::styleSelectorChanged+0x36 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\document.cpp @ 2823]
002cf3fc 698ea00d chrome_68db0000!WebCore::StyleElement::removedFromDocument+0x3c [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\styleelement.cpp @ 71]
002cf40c 69301b66 chrome_68db0000!WebCore::SVGStyleElement::removedFromDocument+0x14 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\svg\svgstyleelement.cpp @ 114]
002cf418 69301b07 chrome_68db0000!WebCore::Private::addChildNodesToDeletionQueue<WebCore::Node,WebCore::ContainerNode>+0x47 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\containernodealgorithms.h @ 139]
002cf438 692ffff8 chrome_68db0000!WebCore::removeAllChildrenInContainer<WebCore::Node,WebCore::ContainerNode>+0x50 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\containernodealgorithms.h @ 62]
002cf440 692b1466 chrome_68db0000!WebCore::ContainerNode::~ContainerNode+0x15 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\containernode.cpp @ 98]
002cf450 698d9414 chrome_68db0000!WebCore::Element::~Element+0x3d [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\element.cpp @ 79]
002cf478 698da93d chrome_68db0000!WebCore::SVGElement::~SVGElement+0xcc [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\svg\svgelement.cpp @ 82]
002cf480 698e96bf chrome_68db0000!WebCore::SVGSVGElement::`scalar deleting destructor'+0x8
002cf488 6940085a chrome_68db0000!WebCore::TreeShared<WebCore::SVGElementInstance>::removedLastRef+0xa [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\platform\treeshared.h @ 122]
002cf498 69400bb2 chrome_68db0000!WebCore::XMLDocumentParser::clearCurrentNodeStack+0x38 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\xmldocumentparser.cpp @ 112]
002cf4a0 6937d834 chrome_68db0000!WebCore::XMLDocumentParser::end+0x4d [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\xmldocumentparser.cpp @ 241]
002cf4ec 694011fc chrome_68db0000!WebCore::XMLDocumentParser::resumeParsing+0xad [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\xmldocumentparserlibxml2.cpp @ 1419]
002cf56c 693d3b2a chrome_68db0000!WebCore::XMLDocumentParser::notifyFinished+0xd0 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\xmldocumentparser.cpp @ 370]
002cf590 693d3b59 chrome_68db0000!WebCore::CachedScript::checkNotify+0x25 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\loader\cachedscript.cpp @ 100]
002cf598 692f86ac chrome_68db0000!WebCore::CachedScript::error+0x18 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\loader\cachedscript.cpp @ 107]
002cf5bc 692f85f6 chrome_68db0000!WebCore::Loader::Host::didFail+0xb3 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\loader\loader.cpp @ 459]
002cf5c8 693d1471 chrome_68db0000!WebCore::Loader::Host::didFail+0xc [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\loader\loader.cpp @ 428]


## Attachments

- [test0.xhtml](attachments/test0.xhtml) (text/html; charset=us-ascii, 829 B)

## Timeline

### in...@chromium.org (2011-01-31)

Thanks Wushi for another awesome bug !!

### in...@chromium.org (2011-01-31)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=53441

### in...@chromium.org (2011-01-31)

taking a look.

### in...@chromium.org (2011-01-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-01)

Committed - http://trac.webkit.org/changeset/77262

### sc...@gmail.com (2011-02-03)

@wooshi:
Congratulations! This bug provisionally qualifies for a Chromium Security Reward at the $1000 level, thanks to:
- Good quality, simple repro.
- Useful stack trace and register dump.
We should have the fix out to users within a few weeks.

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

### in...@chromium.org (2011-02-09)

merged to m9 in http://trac.webkit.org/changeset/78096.

still needs m10 merge.

### in...@chromium.org (2011-02-09)

merged to m10 in r78123

### sc...@gmail.com (2011-03-04)

Invoice finalized; payment is in e-payment system.

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

This issue was migrated from crbug.com/chromium/71386?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087405)*
