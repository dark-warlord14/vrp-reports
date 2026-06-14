# (WebCore::RenderObjectChildList::destroyLeftoverChildren) Use-after-free with nesting ruby tag and css propierties

| Field | Value |
|-------|-------|
| **Issue ID** | [40088588](https://issues.chromium.org/issues/40088588) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ja...@gmail.com |
| **Assignee** | ro...@gmail.com |
| **Created** | 2011-03-07 |
| **Bounty** | $1,000.00 |

## Description



==================
=    ADVISORY    =
==================


-Title: (WebCore::RenderObjectChildList::destroyLeftoverChildren) 
		Use-after-free with nesting ruby tag and css 
		propierties 
-OS: Windows XP SP3
-Sec-severity: (probably) High
-Tested on: Safari 5.0.3 (not affected) and Chrome 11.0.686.3 dev, 
		Chrome 9.0.597.107 (affected)


================
=    INTRO     =
================


I have had problems watching the source code, so I needed to find it directly 
from chromium page and download implicated files (this is an issue that i have since you changed the symbol url). Sorry if this analysis is not enough detailed but it's due to previous raison.

Also i've got different logs using the original poc (not reduced) and this. Anyway, i think that poc has been reduced correctly, but i've attached because maybe it hides another vuln or if you want to reproduce the original logs. 
On the other hand, other poc, very similar to this, produces a null ptr, poc and stacktrace are also attached for this case.

Then, i've included a meta tag for doing a refresh because it didn't crash automatically without it, you needed to reload and it usually got crashed in second time.


In summary (files):

-poc_reduced.html -> log[poc_reduced.html]_stable&dev

-poc_fuzz.html:
	-Stable channel -> log[poc_fuzz.html]_stable
	-Dev channel -> log[poc_fuzz.html]_dev

-poc_null_ptr.html -> log[poc_null_ptr.html]_stable&dev


===================
=   DESCRIPTION   =
===================


There is a vulnerability due to nesting of ruby tags and using some css properties, issue is a freed memory that it's used later, an use-after-free vulnerability.

I've got several crashes using two different pocs, one attached (original from fuzzer) and another reduced which it's included in this advisory.


This analysis is made using the reduced poc.


The stacktrace shows:

WARNING: Frame IP not in any known module. Following frames may be wrong.
0x0
chrome_1c30000!WebCore::RenderObjectChildList::destroyLeftoverChildren+0xd
chrome_1c30000!WebCore::RenderBlock::destroy+0x11
chrome_1c30000!WebCore::Node::detach+0x1b
chrome_1c30000!WebCore::ContainerNode::detach+0x29
chrome_1c30000!WebCore::Element::detach+0x2e
chrome_1c30000!WebCore::ContainerNode::detach+0x14
chrome_1c30000!WebCore::Element::detach+0x2e
chrome_1c30000!WebCore::ContainerNode::detach+0x14
chrome_1c30000!WebCore::Element::detach+0x2e
chrome_1c30000!WebCore::ContainerNode::detach+0x14
chrome_1c30000!WebCore::Element::detach+0x2e
chrome_1c30000!WebCore::ContainerNode::detach+0x14
chrome_1c30000!WebCore::Document::detach+0xe1


Document::detach begins to detach the document. Calls to ContainerNode::detach()(1) and it begins to detach each child. Repeating this process (2) and (3), and finally, last css propierty (4). In this point, goes to RenderBlock::destroy (5) and finally, it reaches the point (6) where pass to RenderObjectChildList::destroyLeftoverChildren(). In this point (7), it produces the use of a freed memory.


====================================
=       REFERENCED FUNCTIONS       =
====================================


void Document::detach()
{
    ...
    
    RenderObject* render = renderer();

    ...

    setRenderer(0);

    m_hoverNode = 0;
    m_focusedNode = 0;
    m_activeNode = 0;

    ContainerNode::detach(); <- (1)

    unscheduleStyleRecalc();

    if (render)
        render->destroy();
    
    ...
}


void ContainerNode::detach()
{
    for (Node* child = m_firstChild; child; child = child->nextSibling())
        child->detach(); <- (2)
    clearChildNeedsStyleRecalc();
    Node::detach(); <-- (4)
}


void Element::detach()
{
    RenderWidget::suspendWidgetHierarchyUpdates();

    cancelFocusAppearanceUpdate();
    if (hasRareData())
        rareData()->resetComputedStyle();
    ContainerNode::detach(); <- (3)

    RenderWidget::resumeWidgetHierarchyUpdates();
}

void Node::detach()
{
    ...

    if (renderer())
        renderer()->destroy(); <- (5)
    setRenderer(0);

    Document* doc = document();
    ...
}


void RenderBlock::destroy()
{

    children()->destroyLeftoverChildren(); <- (6)
    ...
}



void RenderObjectChildList::destroyLeftoverChildren()
{
    while (firstChild()) { <- (7)
        if (firstChild()->isListMarker() || (firstChild()->style()->styleType() == FIRST_LETTER && !firstChild()->isText()))
            firstChild()->remove();  // List markers are owned by their enclosing list and so don't get destroyed by this container. Similarly, first letters are destroyed by their remaining text fragment.
        else if (firstChild()->isRunIn() && firstChild()->node()) {
            firstChild()->node()->setRenderer(0);
            firstChild()->node()->setNeedsStyleRecalc();
            firstChild()->destroy();
        } else {
            // Destroy any anonymous children remaining in the render tree, as well as implicit (shadow) DOM elements like those used in the engine-based text fields.
            if (firstChild()->node())
                firstChild()->node()->setRenderer(0);
            firstChild()->destroy();
        }
    }
}


===================
=       POC       =
===================


This is the poc reduced, i've tried to change it, deleting ::before or any css propierty and it seems the most simple sample. As i've said, if you delete a ruby tag, new poc crashes with a null ptr.

-------------------------poc_reduced.html-----------------------------

<meta http-equiv="refresh" content="1;url=" />
<style>
		ruby::before{
			display: table;
			content: url("http://XX");
		}
</style>
	<ruby>
		<ruby>
			<ruby>
				<style>
					ruby{
						float: right;	
					}
				</style>
			</ruby>
		</ruby>
	</ruby>

----------------------------------------------------------------------


===================
=     CREDITS     =
===================


Vulnerability discovered (maybe not the first?) by:

Jose A. Vazquez of {http://spa-s3c.blogspot.com}


## Attachments

- [poc_fuzz.html](attachments/poc_fuzz.html) (text/html; charset=us-ascii, 110.1 KB)
- [log[poc_null_ptr.html]_stable&dev.txt](attachments/log[poc_null_ptr.html]_stable&dev.txt) (text/plain; charset=us-ascii, 17.2 KB)
- [log[poc_reduced.html]_stable&dev.txt](attachments/log[poc_reduced.html]_stable&dev.txt) (text/plain; charset=us-ascii, 16.7 KB)
- [poc_reduced.html](attachments/poc_reduced.html) (text/plain; charset=us-ascii, 272 B)
- [log[poc_fuzz.html]_dev.txt](attachments/log[poc_fuzz.html]_dev.txt) (text/plain; charset=us-ascii, 441 B)
- [log[poc_fuzz.html]_stable.txt](attachments/log[poc_fuzz.html]_stable.txt) (text/plain; charset=us-ascii, 544 B)
- [poc_null_ptr.html](attachments/poc_null_ptr.html) (text/plain; charset=us-ascii, 252 B)
- [full_advisory.txt](attachments/full_advisory.txt) (text/plain; charset=us-ascii, 22.9 KB)
- [new_reduced.html](attachments/new_reduced.html) (text/html; charset=us-ascii, 311 B)
- [new_stackframes.txt](attachments/new_stackframes.txt) (text/plain; charset=us-ascii, 4.7 KB)

## Timeline

### in...@chromium.org (2011-03-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-03-07)

We are removing the childs from the incorrect parent and hence we hit the assert ASSERT(child->parent() != this). I don't understand why we didn't just check child->parent == this in the first condition. 

Roland, can you please help to fix this. Please do use all the repros in the bug, since they look like variants of the same problem.


void RenderRubyAsInline::removeChild(RenderObject* child)
{
    // If the child's parent is *this (a ruby run or :before or :after content),
    // just use the normal remove method.
    if (child->isRubyRun() || child->isBeforeContent() || child->isAfterContent()) {
        RenderInline::removeChild(child);
        return;
    }

    // Otherwise find the containing run and remove it from there.
    ASSERT(child->parent() != this);
    RenderRubyRun* run = findRubyRunParent(child);
    ASSERT(run);
    run->removeChild(child);
}


void RenderRubyAsBlock::removeChild(RenderObject* child)
{
    // If the child's parent is *this (a ruby run or :before or :after content),
    // just use the normal remove method.
    if (child->isRubyRun() || child->isBeforeContent() || child->isAfterContent()) {
        RenderBlock::removeChild(child);
        return;
    }

    // Otherwise find the containing run and remove it from there.
    ASSERT(child->parent() != this);
    RenderRubyRun* run = findRubyRunParent(child);
    ASSERT(run);
    run->removeChild(child);
}

Another repro::
<body>
<style>
ruby.test
{
    float: left;   
}

ruby.test::before{
    display: table;
    content: url("http://XX");
}
</style>
<ruby>
    <ruby class="test">
        <ruby></ruby>
    </ruby>
</ruby>
</body>


### ro...@gmail.com (2011-03-08)

In theory, a RenderRuby... object should _only_ have RenderRubyRun objects or generated content as children, so - again, in theory - the condition should be the same as child->parent() == this.

In this case, this is thwarted by the generated block renderer that wraps the RenderRubyRun objects (which are inline) in anonymous blocks.

I opened a WebKit security bug: https://bugs.webkit.org/show_bug.cgi?id=55930 and submitted a patch there.

Note that in the next 4 days I'm side-lined as a WebKit gardener, so my replies may not be the fastest... :(

### ro...@gmail.com (2011-03-08)

Addendum: poc_fuzz.html also contains a CSS property 'color-profile' that is missing in a relevant switch statement and causes an - otherwise unrelated - ASSERT. My WebKit patch should also fix that.

### in...@chromium.org (2011-03-18)

Roland, ping !! Did you get a chance to look at Hyatt's comment. ?

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### ja...@gmail.com (2011-03-21)

14 days of submitted date, I'm not used to this long time waiting when I send advisories here. Lot of work?

Btw, https://crbug.com/chromium/75186#c4 talked about other issue...Have you open other thread to fix it?
Sorry if I didn't find it. It's so difficult to make an analysis and reductions without available source code since debugger, and for this reason, I posted fuzz output too. Do you know if also it's a security issue?

Regards,
Jose

### js...@chromium.org (2011-03-21)

[Comment Deleted]

### ja...@gmail.com (2011-03-21)

[Comment Deleted]

### ro...@gmail.com (2011-03-22)

My work on the upstream WebKit bug has been hampered by the events in Japan (where I live). It will probably take another week before I can resume. :( 

### js...@chromium.org (2011-03-22)

@rolandsteiner - That's entirely understandable. We don't have an immediately pending security release and (of course) you guys have far more important things to deal with right now. If you expect it to be while before you can get back to this just let us know and we'll see about finding someone to finish it off.

### ja...@gmail.com (2011-03-22)

Absolutely agree with last comment.
As the reporting party, you can take as time as necessary.

Regards,
Jose.

### js...@chromium.org (2011-03-22)

Moving m10 bugs to m11.

### in...@chromium.org (2011-04-04)

Roland, can you please ping Hyatt for a re-review.

### ro...@gmail.com (2011-04-13)

Patch landed upstream in WK r83787.

### sc...@gmail.com (2011-04-14)

I will investigate merging this to M11.

Roland, any idea how risky a change it is? Is the risk of breakage limited to the (not widely used) <ruby> tag?

### ro...@gmail.com (2011-04-14)

I don't think it'll be very risky - the only code that changed is for ruby (and only affects ruby that also have generated CSS content at that), plus an additional general safety check for generated content, that should make things rather safer.

### sc...@gmail.com (2011-04-15)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-15)

Merged to M11: http://trac.webkit.org/changeset/83995

### sc...@gmail.com (2011-04-15)

[Comment Deleted]

### sc...@gmail.com (2011-04-15)

I finally stopped sucking and merged it properly at:
http://trac.webkit.org/changeset/84009

### ja...@gmail.com (2011-04-16)

Thanks.

Ok. It would be perfect that you credit me like last time.
No, https://crbug.com/chromium/75186#c9 is the mail address that i'm using in my blog, so it is not the issue. In fact, I talked about https://crbug.com/chromium/75186#c8 (user mail which i've configured with "...", as you do). I cannot modify these comments.
Now also your comment xDD
Whoops! No matters, it's my mistake. Probably, I should change and send advisories using my public address :)

Btw, already is it patched in some channel? just for try it...

Regards,
Jose.

### js...@chromium.org (2011-04-16)

I can remove comments with information you don't want disclosed when this bug is made public (including these comments). Just let us know which ones.

### ja...@gmail.com (2011-04-16)

Comments #8 and #20 (just where it's used @javg...)
Many thanks.

### sc...@gmail.com (2011-04-19)

@Jose: should be fixed in Beta channel, e.g. http://googlechromereleases.blogspot.com/2011/04/beta-channel-update_18.html
But please wait until Chrome 11 goes stable before disclosing.

And... congrats! This bug qualifies for a provisional $1000 Chromium Security Reward on account of a good small test case, an accurate classification (use-after-free), good stack trace, etc. Thanks!

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

### ja...@gmail.com (2011-04-19)

Thanks!

Btw, about disclosure considerations, do you know what are the affected products? I've tested against Safari 5.0.5 and it was not affected. Maybe another webkit product?


### sc...@gmail.com (2011-04-22)

[Empty comment from Monorail migration]

### ja...@gmail.com (2011-04-22)

"poc_fuzz.html" is still crashing in Chrome dev, using the current update (http://googlechromereleases.blogspot.com/2011/04/dev-channel-update_20.html), where I think that it was fixed because "poc_reduced.html" didn't get crashed for me...

I've tested several machines (Note: WinXP-SP3)...can someone confirm it?

Soon (next few minutes) I will post new reduced poc and stackframes (I don't know if it's a related issue yet).



### in...@chromium.org (2011-04-22)

poc_fuzz.html is crashing on a null ptr (non security bug) in counters. don't worry about it, counter code is full of null ptrs :)

static RenderObject* nextInPreOrder(const RenderObject* object, const Element* stayWithin, bool skipDescendants = false)
{
    Element* self;
    Element* child;
    RenderObject* result;
    self = toElement(object->generatingNode());

### ja...@gmail.com (2011-04-22)

First look: One related-with-counters null ptr.
Perhaps other issue or related with this?





### ja...@gmail.com (2011-04-22)

yes :)

### ro...@gmail.com (2011-04-23)

Added a follow-up patch on the upstream bug.

### sc...@gmail.com (2011-05-04)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

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

This issue was migrated from crbug.com/chromium/75186?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088588)*
