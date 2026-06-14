# Heap-use-after-free in WebCore::HTMLBodyElement::insertedInto

| Field | Value |
|-------|-------|
| **Issue ID** | [40079186](https://issues.chromium.org/issues/40079186) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HTML |
| **Reporter** | cl...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2014-03-25 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the current Chrome ASAN build.

The vulnerable function:

Node::InsertionNotificationRequest HTMLBodyElement::insertedInto(ContainerNode\* insertionPoint)  

{  

HTMLElement::insertedInto(insertionPoint);  

if (insertionPoint->inDocument()) {  

// FIXME: It's surprising this is web compatible since it means a marginwidth  

// and marginheight attribute can magically appear on the <body> of all documents  

// embedded through <iframe> or <frame>.  

Element\* ownerElement = document().ownerElement();  

if (isHTMLFrameElementBase(ownerElement)) {  

HTMLFrameElementBase& ownerFrameElement = toHTMLFrameElementBase(\*ownerElement);  

int marginWidth = ownerFrameElement.marginWidth();  

if (marginWidth != -1)  

setIntegralAttribute(marginwidthAttr, marginWidth);  

int marginHeight = ownerFrameElement.marginHeight();

The ownerElement object is a raw pointer and can be garbage collected in the DOMSubtreeModified event which is fired in setIntegralAttribute().

The fix should be pretty straight forward: Make ownerElement a RefPtr

**REPRODUCTION CASE**  

This testcase demonstrates the issue in a Chrome ASAN build. It requires the --js-flags=--expose-gc command line argument:

<script>
function start() {
o2=document.createElement('iframe');
document.body.appendChild(o2);
o2.setAttribute('marginwidth', 1);
o46=document.createElement('body');
o46.addEventListener('DOMSubtreeModified', cb\_bodyspecial\_13\_1);
o47=o2.contentDocument.documentElement;
o47.appendChild(o46);
}
function cb\_bodyspecial\_13\_1() {
o2.parentNode.removeChild(o2);
o2=null;
gc();
}
</script>
<body onload="start()">
</body>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached

## Attachments

- [out.txt](attachments/out.txt) (text/plain, 11.5 KB)

## Timeline

### cl...@gmail.com (2014-03-25)

ASAN output

### cl...@chromium.org (2014-03-25)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=4598283502616576.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4598283502616576

Uploader: clusterfuzz@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61100005ab10
Crash State:
  - crash stack -
  WebCore::HTMLBodyElement::insertedInto
  WebCore::ChildNodeInsertionNotifier::notifyNodeInsertedIntoDocument
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=193329:193330

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97qANqZAjWWlhb9NflgLw-73xsx0ZOJbbia37wsosBoZuUp93WSwfT4qVfFeK4Lqt1s0VWxBxtPH0E-jyNZeZFAprEsD_cu7wLDYAbjkpsXWCN4O3X0R0FUeQf81fmDP0u5HxlUdJKcJw2uI8Nz_FglxgHbVw



### in...@chromium.org (2014-03-25)

Cloudfuzzer, thanks for the nice bug and patch suggestion. Do you want to upload the patch yourself with this minimized test. it will qualify for the higher reward.

### cl...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### jw...@chromium.org (2014-03-25)

I'm assigning this bug to tkent for triaging purposes (tkent, feel free to reassign as is appropriate), but cloudfuzzer, feel free to lay claim to this and upload your patch to codereview.

### cl...@gmail.com (2014-03-25)

Inferno, thanks for the info. I am not familiar with the patch/review process, so I will leave this to those who are for now :)

### jw...@chromium.org (2014-03-25)

Okay, but if you change your mind, instructions are here: http://dev.chromium.org/developers/contributing-code

### jw...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### tk...@chromium.org (2014-03-25)

> The fix should be pretty straight forward: Make ownerElement a RefPtr

Unfortunately, it's not a complete fix.  There are multiple problems other than deletable ownerElement.

I'm not sure who should take this bug. morrita@, are you interested in this bug?



### tk...@chromium.org (2014-03-27)

I'm working on this because I'm not sure who should take this.


### bu...@chromium.org (2014-03-27)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=170216

------------------------------------------------------------------
r170216 | tkent@chromium.org | 2014-03-27T22:55:30.766226Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLBodyElement/body-inserting-iframe-crash.html?r1=170216&r2=170215&pathrev=170216
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLBodyElement?r1=170216&r2=170215&pathrev=170216
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLBodyElement.cpp?r1=170216&r2=170215&pathrev=170216
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/HTMLBodyElement.h?r1=170216&r2=170215&pathrev=170216
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/fast/dom/HTMLBodyElement/body-inserting-iframe-crash-expected.txt?r1=170216&r2=170215&pathrev=170216

Do not update attributes in HTMLBodyElement::insertedInto.

Use didNotifySubtreeInsertionsToDocument instead.

BUG=356095
TEST=automated
R=morrita@chromium.org

Review URL: https://codereview.chromium.org/212793007
-----------------------------------------------------------------

### in...@chromium.org (2014-03-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-28)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-03-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-29)

ClusterFuzz has detected this issue as fixed in range 260076:260092.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4598283502616576

Uploader: clusterfuzz@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x61100005ab10
Crash State:
  - crash stack -
  WebCore::HTMLBodyElement::insertedInto
  WebCore::ChildNodeInsertionNotifier::notifyNodeInsertedIntoDocument
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=193329:193330
Fixed: https://cluster-fuzz.appspot.com/revisions?range=260076:260092

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97qANqZAjWWlhb9NflgLw-73xsx0ZOJbbia37wsosBoZuUp93WSwfT4qVfFeK4Lqt1s0VWxBxtPH0E-jyNZeZFAprEsD_cu7wLDYAbjkpsXWCN4O3X0R0FUeQf81fmDP0u5HxlUdJKcJw2uI8Nz_FglxgHbVw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### tk...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### dx...@google.com (2014-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-04-01)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=170502

------------------------------------------------------------------
r170502 | tkent@chromium.org | 2014-04-01T01:57:39.303784Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/core/html/HTMLBodyElement.cpp?r1=170502&r2=170501&pathrev=170502
   M http://src.chromium.org/viewvc/blink/branches/chromium/1847/Source/core/html/HTMLBodyElement.h?r1=170502&r2=170501&pathrev=170502

Merge 170216 "Do not update attributes in HTMLBodyElement::inser..."

> Do not update attributes in HTMLBodyElement::insertedInto.
> 
> Use didNotifySubtreeInsertionsToDocument instead.
> 
> BUG=356095
> TEST=automated
> R=morrita@chromium.org
> 
> Review URL: https://codereview.chromium.org/212793007

TBR=tkent@chromium.org

Review URL: https://codereview.chromium.org/220483002
-----------------------------------------------------------------

### tk...@chromium.org (2014-04-01)

[Empty comment from Monorail migration]

### ka...@google.com (2014-04-01)

170216 is already on branch since we cut at 313. no merge needed.

### in...@chromium.org (2014-04-01)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-14)

Thanks for the report - $2000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-18)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you (Req #233621). Thanks again for your help!

### cl...@chromium.org (2014-07-04)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/356095?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079186)*
