# Security:WebCore::HTMLTextAreaElement::updateValue+0xf

| Field | Value |
|-------|-------|
| **Issue ID** | [40087406](https://issues.chromium.org/issues/40087406) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | wo...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-01-31 |
| **Bounty** | $1,000.00 |

## Description

test on 8.0.552.237.

eax=66c9fe68 ebx=03a0cb84 ecx=0379b150 edx=03a0cc08 esi=03a0cb84 edi=0379b150
eip=722d7463 esp=0014eae4 ebp=0014eaf0 iopl=0         nv up ei pl nz na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010206
722d7463 ??              ???
2:025> k
ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
0014eae0 663a7642 0x722d7463
0014eaf0 6677f905 chrome_65c00000!WebCore::HTMLTextAreaElement::updateValue+0xf [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\html\htmltextareaelement.cpp @ 272]
0014eafc 6677f8d6 chrome_65c00000!WebCore::RenderTextControlMultiLine::~RenderTextControlMultiLine+0x1c [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\rendertextcontrolmultiline.cpp @ 42]
0014eb04 660e29a4 chrome_65c00000!WebCore::RenderTextControlMultiLine::`scalar deleting destructor'+0x8
0014eb10 660e292b chrome_65c00000!WebCore::RenderObject::arenaDelete+0x75 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderobject.cpp @ 2219]
0014eb28 66154583 chrome_65c00000!WebCore::RenderObject::destroy+0xc2 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderobject.cpp @ 2186]
0014eb38 660ee241 chrome_65c00000!WebCore::RenderBox::destroy+0x50 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderbox.cpp @ 209]
0014eb48 660ed537 chrome_65c00000!WebCore::Node::detach+0x1b [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\node.cpp @ 1220]
0014eb74 66101466 chrome_65c00000!WebCore::Node::~Node+0xb0 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\node.cpp @ 385]
0014ebbc 66151b15 chrome_65c00000!WebCore::Element::~Element+0x3d [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\element.cpp @ 79]
0014ebd8 6614fff8 chrome_65c00000!WebCore::removeAllChildrenInContainer<WebCore::Node,WebCore::ContainerNode>+0x5e [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\containernodealgorithms.h @ 64]
0014ebe0 66101466 chrome_65c00000!WebCore::ContainerNode::~ContainerNode+0x15 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\containernode.cpp @ 98]
0014ebf0 6638845c chrome_65c00000!WebCore::Element::~Element+0x3d [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\element.cpp @ 79]
0014ebf8 667396bf chrome_65c00000!WebCore::HTMLObjectElement::`scalar deleting destructor'+0x29
0014ec00 66150e2e chrome_65c00000!WebCore::TreeShared<WebCore::SVGElementInstance>::removedLastRef+0xa [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\platform\treeshared.h @ 122]
0014ec18 66150cea chrome_65c00000!WebCore::ContainerNode::dispatchPostAttachCallbacks+0x4e [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\containernode.cpp @ 707]
0014ec24 660f4d86 chrome_65c00000!WebCore::ContainerNode::resumePostAttachCallbacks+0x1a [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\containernode.cpp @ 673]
0014ec4c 660f6d30 chrome_65c00000!WebCore::Document::recalcStyle+0x1ce [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\document.cpp @ 1529]
0014ec60 660f6c4f chrome_65c00000!WebCore::Document::styleSelectorChanged+0x98 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\document.cpp @ 2839]
0014ec6c 663b5e23 chrome_65c00000!WebCore::Document::removePendingSheet+0x12 [d:\b\build\slave\chrome-official\build\src\third_party\webkit\webcore\dom\document.cpp @ 2798]


## Attachments

- [test0.xhtml](attachments/test0.xhtml) (text/html; charset=us-ascii, 395 B)

## Timeline

### sk...@chromium.org (2011-01-31)

Confirmed apparent memory corruption in 8.0.552.237: EIP is overwritten with ASCII chars.

This does not appear to affect: 9.0.597.83 beta, 10.0.648.6 dev or 11.0.656.0 (73133), so I am assuming this has already been fixed and should be pushed to stable soon.


### in...@chromium.org (2011-01-31)

It crashes canary and debug build on trunk quite easily. Reopening bug.

### in...@chromium.org (2011-01-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-31)

Filed WebKit Bug - https://bugs.webkit.org/show_bug.cgi?id=53429

### in...@chromium.org (2011-01-31)

Fixed in http://trac.webkit.org/changeset/77144

### in...@chromium.org (2011-01-31)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-03)

@wooshi: good to see a familiar face :)
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

### wo...@gmail.com (2011-02-09)

I'm surprised chrome's webkit now much stable than one year ago. Good job, guys.

### in...@chromium.org (2011-02-09)

Thanks Wushi for the compliment. We are trying our best to make it much more secure, even inside the sandbox.

### in...@chromium.org (2011-02-09)

m9 merged in http://trac.webkit.org/changeset/78094

still needs m10 merge.

### in...@chromium.org (2011-02-09)

merged to m10 in r78121.

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

This issue was migrated from crbug.com/chromium/71388?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087406)*
