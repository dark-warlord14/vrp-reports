# Heap-use-after-free in WebCore::FormAssociatedElement::formRemovedFromTree

| Field | Value |
|-------|-------|
| **Issue ID** | [40078523](https://issues.chromium.org/issues/40078523) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms |
| **Reporter** | at...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2013-12-08 |
| **Bounty** | $1,000.00 |

## Description

Tested on:

OS: Ubuntu 12.04

Chromium: ASAN 33.0.1732.0 (Developer Build 239266)

Repro-file:

<html>
<body>
	<div id="submenu">
	 <table>
	  <form id="cse-search-box">
	   <td align="right" >
	    <input name="q"/>
<script type="text/javascript"> 
var test0=document.getElementById("cse-search-box")
var test1=document.getElementById("submenu")

test0['q']
test1.innerHTML=''

setTimeout(function(){
test1.insertBefore(test0);
},50)

setTimeout(function(){location.reload()},1000)

</script>


ASAN-report:

==13809==ERROR: AddressSanitizer: heap-use-after-free on address 0x612000004a38 at pc 0x7f6edc992514 bp 0x7fffb113b150 sp 0x7fffb113b148
WRITE of size 8 at 0x612000004a38 thread T0 (chrome)
    #0 0x7f6edc992513 in WebCore::FormAssociatedElement::setForm(WebCore::HTMLFormElement*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/FormAssociatedElement.cpp:136:0
    #1 0x7f6edc7ba379 in WebCore::HTMLFormElement::removedFrom(WebCore::ContainerNode*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLFormElement.cpp:145:0
    #2 0x7f6edbbe437f in WebCore::ChildNodeRemovalNotifier::notifyNodeRemovedFromDocument(WebCore::Node&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNodeAlgorithms.h:237:0
    #3 0x7f6edbbd9ac3 in WebCore::ChildNodeRemovalNotifier::notify(WebCore::Node&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNodeAlgorithms.h:255:0
    #4 0x7f6edbbe0303 in WebCore::Private::NodeRemovalDispatcher<WebCore::Node, WebCore::ContainerNode, true>::dispatch(WebCore::Node&, WebCore::ContainerNode&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNodeAlgorithms.h:141:0
    #5 0x7f6edbbe0123 in void WebCore::Private::addChildNodesToDeletionQueue<WebCore::Node, WebCore::ContainerNode>(WebCore::Node*&, WebCore::Node*&, WebCore::ContainerNode&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/ContainerNodeAlgorithms.h:184:0
.
.
.
freed by thread T0 (chrome) here:
    #0 0x7f6ed8b767a9 in __interceptor_free _asan_rtl_:0
    #1 0x7f6edbae6d06 in derefIfNotNull<WebCore::Node> /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/PassRefPtr.h:56:0
    #2 0x7f6edbae6d06 in ~RefPtr /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:49:0
    #3 0x7f6edbae6d06 in ~RefPtr /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:49:0
    #4 0x7f6edbae6d06 in WTF::RefPtr<WebCore::Node>::operator=(WebCore::Node*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:113:0
    #5 0x7f6edc7bef8c in WebCore::HTMLFormElement::removeFromPastNamesMap(WebCore::HTMLElement&) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLFormElement.cpp:759:0
    #6 0x7f6edc7bed48 in WebCore::HTMLFormElement::removeFormElement(WebCore::FormAssociatedElement*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLFormElement.cpp:604:0
    #7 0x7f6edc992489 in WebCore::FormAssociatedElement::setForm(WebCore::HTMLFormElement*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/FormAssociatedElement.cpp:135:0
    #8 0x7f6edc7ba379 in WebCore::HTMLFormElement::removedFrom(WebCore::ContainerNode*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLFormElement.cpp:145:0
.
.
.

If this issue is not a duplicate, I'll try to analyze it little further tomorrow. :)


## Attachments

- [chrome-heap-use-after-free-WebCoreFormAssociatedElementsetForm10.html](attachments/chrome-heap-use-after-free-WebCoreFormAssociatedElementsetForm10.html) (text/html, 4.6 KB)

## Timeline

### cl...@chromium.org (2013-12-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-12-09)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5192943346384896

### ia...@chromium.org (2013-12-09)

Reproduced. I'll take this one.

### cl...@chromium.org (2013-12-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5192943346384896

Uploader: ianbeer@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x612000006538
Crash State:
  - crash stack -
  WebCore::FormAssociatedElement::formRemovedFromTree
  WebCore::HTMLFormElement::removedFrom
  - free stack -
  WebCore::HTMLFormElement::removeFromPastNamesMap
  WebCore::HTMLFormElement::removeFormElement
  


Unreliable crash found using linux_tsan_chrome_mp job type (history_size=6).


### tk...@chromium.org (2013-12-10)

[Empty comment from Monorail migration]

### ia...@chromium.org (2013-12-10)

On reload (when the Document gets deleted) the form element's m_pastNamesMap is holding the last ref to the HTMLInputElement:

void HTMLFormElement::removedFrom(ContainerNode* insertionPoint)
{
    Node* root = findRoot(this);
    Vector<FormAssociatedElement*> associatedElements(m_associatedElements);
    for (unsigned i = 0; i < associatedElements.size(); ++i)
        associatedElements[i]->formRemovedFromTree(root);
    HTMLElement::removedFrom(insertionPoint);
}


void FormAssociatedElement::formRemovedFromTree(const Node* formRoot)
{
    ASSERT(m_form);
    if (toHTMLElement(this)->highestAncestor() != formRoot)
        setForm(0);
}


void FormAssociatedElement::setForm(HTMLFormElement* newForm)
{
    if (m_form == newForm)
        return;
    willChangeForm()
    if (m_form)
        m_form->removeFormElement(this); <-- this gets free'd in here
    m_form = newForm;                    <-- UaF in ASAN
    if (m_form)
        m_form->registerFormElement(*this);
    didChangeForm();
}


void HTMLFormElement::removeFormElement(FormAssociatedElement* e)
{
...
    removeFromPastNamesMap(*toHTMLElement(e));
    removeFromVector(m_associatedElements, e);
}

[ typedef HashMap<AtomicString, RefPtr<Node> > PastNamesMap; ]

void HTMLFormElement::removeFromPastNamesMap(HTMLElement& element)
{
    if (!m_pastNamesMap)
        return;
    PastNamesMap::iterator end = m_pastNamesMap->end();
    for (PastNamesMap::iterator it = m_pastNamesMap->begin(); it != end; ++it) {
        if (it->value.get() == &element) {
            it->value = 0;                          <-- free (that was the last ref + no parent?)
            // Keep looping. Single element can have multiple names.
        }
    }
}

It looks like the HTMLInputElement is no longer a TreeShared child of the HTMLFormElement? When the HTMLFormElement drops the last ref the HTMLInputElement gets deleted despite its associated form still being alive?

The repro isn't too reliable - it has to reload quite a few times before hitting the UaF under ASAN which makes it a bit tricky to debug.

Reassigning to tkent.

### at...@gmail.com (2013-12-10)

Here is less minimized repro, that might be more reliable. On my machine it causes crash, on ASAN-build, on first refresh.

You could try to run it on your own minimization tools to see if you can get more reliable minimized repro.

### tk...@chromium.org (2013-12-11)

[Empty comment from Monorail migration]

### tk...@chromium.org (2013-12-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-12-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=163680

------------------------------------------------------------------------
r163680 | tkent@chromium.org | 2013-12-11T06:56:23.072022Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/past-names-crash-expected.txt?r1=163680&r2=163679&pathrev=163680
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/FormAssociatedElement.cpp?r1=163680&r2=163679&pathrev=163680
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/forms/past-names-crash.html?r1=163680&r2=163679&pathrev=163680

Fix a crash when a form control is in a past naems map of a demoted form element.

Note that we wanted to add the protector in FormAssociatedElement::setForm(),
but we couldn't do it because it is called from the constructor.

BUG=326854
TEST=automated.

Review URL: https://codereview.chromium.org/105693013
------------------------------------------------------------------------

### sc...@gmail.com (2013-12-11)

@tkent: thanks for a quick fix as always! You rock.

I see that you added the Security_Impact-Stable. I'm assuming this means that you're familiar enough with the code area that you're confident this bug affects Chrome 31 (current stable). Let me know if that is not what you mean. I'm adding extra flags for now, based on your use of that label.

(Normally, ClusterFuzz would work this all out for us, but ClusterFuzz struggles when the repro is not 100% reliable.)

Pre-emptively requesting merge to M32 (I think M31 is all finished)

### sc...@gmail.com (2013-12-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-12-11)

Also, I'm seeing if ClusterFuzz can make more sense of the repro in https://crbug.com/chromium/326854#c7
https://cluster-fuzz.appspot.com/testcase?key=6704532121714688

### tk...@chromium.org (2013-12-11)

#11,
Yes, this bug must affect M31 stable.



### la...@google.com (2013-12-11)

No more M31 stable releases.

### dx...@google.com (2013-12-11)

[Empty comment from Monorail migration]

### ka...@google.com (2013-12-12)

tkent how safe is this? shall we bake it more?

### tk...@chromium.org (2013-12-12)

#17,
The change is very safe to merge.



### ka...@google.com (2013-12-12)

ok ty.


### bu...@chromium.org (2013-12-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=163825

------------------------------------------------------------------------
r163825 | tkent@chromium.org | 2013-12-12T23:46:29.255214Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1700/LayoutTests/fast/forms/past-names-crash-expected.txt?r1=163825&r2=163824&pathrev=163825
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/core/html/FormAssociatedElement.cpp?r1=163825&r2=163824&pathrev=163825
   A http://src.chromium.org/viewvc/blink/branches/chromium/1700/LayoutTests/fast/forms/past-names-crash.html?r1=163825&r2=163824&pathrev=163825

Merge 163680 "Fix a crash when a form control is in a past naems..."

> Fix a crash when a form control is in a past naems map of a demoted form element.
> 
> Note that we wanted to add the protector in FormAssociatedElement::setForm(),
> but we couldn't do it because it is called from the constructor.
> 
> BUG=326854
> TEST=automated.
> 
> Review URL: https://codereview.chromium.org/105693013

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/114783002
------------------------------------------------------------------------

### bu...@chromium.org (2013-12-16)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=163945

------------------------------------------------------------------------
r163945 | tkent@chromium.org | 2013-12-16T08:47:00.250216Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLFormElement.h?r1=163945&r2=163944&pathrev=163945
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/FormAssociatedElement.cpp?r1=163945&r2=163944&pathrev=163945
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLFormElement.cpp?r1=163945&r2=163944&pathrev=163945

Fix assertion failure in FormAssociatedElement::formRemovedFromTree.

This is a regression by Blink r163680 [1].
FormAssociatedElement::formRemovedFromTree can be called with
m_deletionHasBegun. We should not update the reference counter in it.

Removing RefPtr<> for HTMLFormElement::m_pastNamesMap magically fixes the
original problem.

This CL has no tests. I couldn't make a test which works as a layout test.

[1] http://src.chromium.org/viewvc/blink?revision=163680&view=revision

BUG=326854,328456

Review URL: https://codereview.chromium.org/113423005
------------------------------------------------------------------------

### in...@chromium.org (2014-01-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-01-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=164445

------------------------------------------------------------------------
r164445 | tkent@chromium.org | 2014-01-03T06:13:24.778124Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/core/html/FormAssociatedElement.cpp?r1=164445&r2=164444&pathrev=164445
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/core/html/HTMLFormElement.cpp?r1=164445&r2=164444&pathrev=164445
   M http://src.chromium.org/viewvc/blink/branches/chromium/1700/Source/core/html/HTMLFormElement.h?r1=164445&r2=164444&pathrev=164445

Merge 163945 "Fix assertion failure in FormAssociatedElement::fo..."

> Fix assertion failure in FormAssociatedElement::formRemovedFromTree.
> 
> This is a regression by Blink r163680 [1].
> FormAssociatedElement::formRemovedFromTree can be called with
> m_deletionHasBegun. We should not update the reference counter in it.
> 
> Removing RefPtr<> for HTMLFormElement::m_pastNamesMap magically fixes the
> original problem.
> 
> This CL has no tests. I couldn't make a test which works as a layout test.
> 
> [1] http://src.chromium.org/viewvc/blink?revision=163680&view=revision
> 
> BUG=326854,328456
> 
> Review URL: https://codereview.chromium.org/113423005

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/99743004
------------------------------------------------------------------------

### in...@chromium.org (2014-01-08)

[Empty comment from Monorail migration]

### dh...@google.com (2014-01-09)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-01-13)

Thanks for the report! This one qualifies for a $1000 reward. It did not qualify at a higher reward level because there does not appear to be control between the free and use, and because the freed object is inside our Node heap partition.

### in...@chromium.org (2014-02-10)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### dh...@google.com (2014-02-28)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-28)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-04-14)

[Empty comment from Monorail migration]

### gl...@chromium.org (2015-06-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/326854?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/327715]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078523)*
