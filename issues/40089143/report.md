# RIP goes to zero with select tag, and form validation message with position:relative

| Field | Value |
|-------|-------|
| **Issue ID** | [40089143](https://issues.chromium.org/issues/40089143) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-03-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

rip == 0, or null pointer deref at 0x88

**VERSION**  

Chrome Version:  

Chromium 12.0.710.0 (Developer Build 78857) Ubuntu 10.10  

WebKit 534.26 (trunk@81520)

Operating System:  

Ubuntu 10.10:  

Linux 2.6.35-28-generic #49-Ubuntu SMP Tue Mar 1 14:39:03 UTC 2011 x86\_64

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

#0 0x0000000000000000 in ?? ()  

#1 0x00007ffff6676994 in remove (this=0x7ffff95ed048)  

at third\_party/WebKit/Source/WebCore/rendering/RenderObject.h:752  

#2 WebCore::RenderObject::destroy (this=0x7ffff95ed048)  

at third\_party/WebKit/Source/WebCore/rendering/RenderObject.cpp:2187

## Attachments

- [27.html](attachments/27.html) (text/plain; charset=us-ascii, 515 B)
- [valgrind_76966.txt](attachments/valgrind_76966.txt) (text/x-c; charset=us-ascii, 10.1 KB)

## Timeline

### mi...@gmail.com (2011-03-21)

tools bisect says:
http://build.chromium.org/f/chromium/perf/dashboard/ui/changelog.html?url=/trunk/src&range=77979:77982

which is: Roll WebKit DEPS 80725:80974


### mi...@gmail.com (2011-03-21)

valgrind log.

it says null pointer at 0x88.  don't know if it's a timing issue.  

### mi...@gmail.com (2011-03-21)

[Comment Deleted]

### in...@chromium.org (2011-03-22)

looks like a dup of http://trac.webkit.org/changeset/81613 and http://code.google.com/p/chromium/issues/detail?id=76528. will check when webkit rolls 

### sc...@gmail.com (2011-03-22)

Still sad tab in my Linux 64-bit trunk build, after the roll.

### in...@chromium.org (2011-03-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-03-22)

Kent, this is caused by the one liner change in http://trac.webkit.org/changeset/80773. Can you please take a look.

    // Needs to update layout now because we'd like to call isFocusable(), which
    // has !renderer()->needsLayout() assertion.
    document()->updateLayoutIgnorePendingStylesheets();

### tk...@chromium.org (2011-03-23)

I haven't found the root cause yet, but my findings at this moment are:

* I confirmed this was a use-after-free bug.

* RenderMenuList::m_innerBlock keeps a pointer to an anonymous block while m_innerBlock->addChild() can remove m_innerBlock.
   - See RenderMenuList::addChild(), and
   - removeLeftoverAnonymousBlock(this) at the bottom of RenderBlock::addChildIgnoringAnonymousColumnBlocks()

* Probably, http://trac.webkit.org/changeset/80773 doesn't have a code problem and it just exposed the bug.


### in...@chromium.org (2011-03-23)

Thanks a lot Kent. Happy to leave it in your able hands.

### tk...@chromium.org (2011-03-23)

The crash doesn't happen if I replace document.getElementById('submit').click() with document.getElementByTagName('select')[0].offsetLeft, which calls updateLayoutIgnorePendingStylesheets().

So, I think WebCore/html/ValidationMessage broke an assumption of RenderMenuList.  I should handle this bug :-P



### tk...@chromium.org (2011-03-23)

I found -webkit-animation was unrelated, and found a workaround.

The root cause is "div { positoin:relative; }".  It changes the style of a validation message div, and this style causes an optimization of anonymous blocks.


### in...@chromium.org (2011-03-23)

tracking webkit bug - https://bugs.webkit.org/show_bug.cgi?id=56901

### tk...@chromium.org (2011-03-24)

Fixed in WebKit: http://trac.webkit.org/changeset/81851
Need to merge it to M10 and M11 branches.


### in...@chromium.org (2011-03-24)

Thanks a lot Kent. We will handle the merges.

### sc...@gmail.com (2011-03-24)

There are no more M10 patches.
Merged to M11: http://trac.webkit.org/changeset/81888

### sc...@gmail.com (2011-04-14)

@miaubiz: great bug and thanks for the usual valgrind and even bisect awesomeness.
$1000.

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

### sc...@gmail.com (2011-04-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-04)

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

This issue was migrated from crbug.com/chromium/76966?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089143)*
