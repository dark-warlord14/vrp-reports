# Segmentation fault at WebCore::ImageLoader::updateFromElement due to malformed HTML

| Field | Value |
|-------|-------|
| **Issue ID** | [40083225](https://issues.chromium.org/issues/40083225) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ao...@gmail.com |
| **Assignee** | ch...@gmail.com |
| **Created** | 2010-09-16 |
| **Bounty** | $1,000.00 |

## Description

A HTML-document with the link '<a> <object type="image/png" data="/images/buttons/html401.p"> </a>' three times causes a renderer segmentation fault in 6.0.472.55 (Official Build 58392) beta and the corresponding Chromium build, running on Ubuntu 10.04 (i386). Not tested with other versions.

The erroneous address had values, 2f2f2f4e, 2b5, 1d and 21 during minimization, eip and esp being mostly constant.

Backtrace begins:
Program received signal SIGSEGV, Segmentation fault.
0x0138fec6 in WebCore::ImageLoader::updateFromElement (this=0x2c33e00)
    at third_party/WebKit/WebCore/loader/ImageLoader.cpp:189
189     third_party/WebKit/WebCore/loader/ImageLoader.cpp: No such file or directory.
        in third_party/WebKit/WebCore/loader/ImageLoader.cpp
(gdb) bt
#0  0x0138fec6 in WebCore::ImageLoader::updateFromElement (this=0x2c33e00)
    at third_party/WebKit/WebCore/loader/ImageLoader.cpp:189
#1  0x012ecbbd in WebCore::HTMLObjectElement::attach (this=0x2b499a0)
    at third_party/WebKit/WebCore/html/HTMLObjectElement.cpp:156
#2  0x011ecacb in WebCore::ContainerNode::attach (this=0x2c05000)
    at third_party/WebKit/WebCore/dom/ContainerNode.cpp:638
#3  0x012120e4 in WebCore::Element::attach (this=0x2c05000)
    at third_party/WebKit/WebCore/dom/Element.cpp:816
#4  0x011ecacb in WebCore::ContainerNode::attach (this=0x2b49a10)
    at third_party/WebKit/WebCore/dom/ContainerNode.cpp:638
#5  0x012120e4 in WebCore::Element::attach (this=0x2b49a10)
    at third_party/WebKit/WebCore/dom/Element.cpp:816
#6  0x012ecbea in WebCore::HTMLObjectElement::attach (this=0x2b49a10)
    at third_party/WebKit/WebCore/html/HTMLObjectElement.cpp:151
#7  0x012ed340 in WebCore::HTMLObjectElement::renderFallbackContent (
    this=0x2b49a10)
    at third_party/WebKit/WebCore/html/HTMLObjectElement.cpp:262
#8  0x014b4fde in WebCore::RenderEmbeddedObject::updateWidget (this=0x2bd552c, 
    onlyCreateNonNetscapePlugins=true)
    at third_party/WebKit/WebCore/rendering/RenderEmbeddedObject.cpp:308
#9  0x012ecb67 in WebCore::HTMLObjectElement::updateWidget (this=0x2b49a10)
    at third_party/WebKit/WebCore/html/HTMLObjectElement.cpp:164
#10 0x012f70c4 in WebCore::HTMLPlugInElement::updateWidgetCallback (
[...]


## Attachments

- [small.html](attachments/small.html) (text/plain; charset=us-ascii, 206 B)
- [small-2f2f2f4e.html](attachments/small-2f2f2f4e.html) (text/plain; charset=us-ascii, 228 B)
- [small-2.html](attachments/small-2.html) (text/plain; charset=us-ascii, 114 B)

## Timeline

### ao...@gmail.com (2010-09-16)

I just noticed the bug reporting guideline says also renderer OOM errors can be reported via the regular bug template. I recalled all memory handling related fatal signals were to be conservatively filed as potential security issues. This one at a glance looked like a bad read, so it probably should have been filed as a normal bug.

### js...@chromium.org (2010-09-16)

Can't get any crashes on Windows, but stable on Linux does crash. I'm syncing and kicking off a build now to investigate further.


### sc...@gmail.com (2010-09-16)

Heya Aki --

Thanks for being conservative for filing this one as security.
Seeing ASCII in a dereference register -- such as the "2f2f2f4e" case you quote above -- is always a bad sign.

In the debugger, there's clearly the use of a fully corrupted object:

#0  0x00000000019ef092 in WebCore::Node::document (this=0x622f736567616d69)
    at third_party/WebKit/WebCore/dom/Node.h:358
#1  0x0000000001d14279 in WebCore::ImageLoader::updateFromElement (
    this=0x7fffc43b9ba0)
    at third_party/WebKit/WebCore/loader/ImageLoader.cpp:189
#2  0x0000000001c46bb5 in WebCore::HTMLObjectElement::attach (
    this=0x7fffc47b48c0)
    at third_party/WebKit/WebCore/html/HTMLObjectElement.cpp:156
#3  0x0000000001af6622 in WebCore::ContainerNode::attach (this=0x7fffc4812f30)
...

Notice the "this" pointer at frame #0 !

The whole ImageLoader object seems hosed; perhaps a use-after-free.

(gdb) print *this
$9 = {<WebCore::CachedResourceClient> = {<WTF::FastAllocBase> = {<No data fields>}, _vptr.CachedResourceClient = 0x7fffc43b9b70}, 
  m_element = 0x622f736567616d69, 
  m_image = {<WebCore::CachedResourceHandleBase> = {
      m_resource = 0x682f736e6f747475}, <No data fields>}, m_failedLoadURL = {
    m_string = {m_impl = {<WTF::FastAllocBase> = {<No data fields>}, 
        m_ptr = 0x702e3130346c6d74}}}, m_firedBeforeLoad = false, 
  m_firedLoad = false, m_imageComplete = false, m_loadManually = false}


Reproduces easily on 64-bit Linux; 6.0.472.59 and 7.0.517.5.



### ao...@gmail.com (2010-09-17)

@scarybeasts: Thanks for the pointer. This clearly is in rather bad shape. I only looked a few instructions around the error position disassembly, which didn't look too harmful to me, and Valgrind didn't spot anything fishy before the low read, so I deduced this is probably just an invalid read. Obviously should have also looked at the frame contents to see how the other values are doing.

Maybe I'd better stick to being conservative for now, at least for cases which affect stable. :)

Attached a case minimized to crashing at the above mentioned 2f2f2f4e address.

### ao...@gmail.com (2010-09-17)

The object data of the above file allows almost direct writing to the location where this points to. For examples replacing x with fiddlesticks gives.

Program received signal SIGSEGV, Segmentation fault.
0x01391196 in WebCore::ImageLoader::updateFromElement (this=0x2c0d280)
    at third_party/WebKit/WebCore/loader/ImageLoader.cpp:189
189     third_party/WebKit/WebCore/loader/ImageLoader.cpp: No such file or directory.
        in third_party/WebKit/WebCore/loader/ImageLoader.cpp
(gdb) x/s this
0x2c0d280:       "\300H\277\002:///home/aki/fiddlesticks"


### js...@chromium.org (2010-09-22)

@scarybeasts - You seem to be the only one who can reproduce this. Do you mind taking a closer look?


### js...@chromium.org (2010-09-30)

ping @scarybeasts.

### ao...@gmail.com (2010-09-30)

Alternative repro:
  <object type="image/png" data=".dtd">
  <object type="image/png" data=".dtd">
  <object type="image/png" data=".dtd">


### in...@chromium.org (2010-09-30)

I can reproduce the problem now on windows. Also see the culprit - http://trac.webkit.org/changeset/35697. 

### in...@chromium.org (2010-10-01)

Webkit bug filed - https://bugs.webkit.org/show_bug.cgi?id=46921

### in...@chromium.org (2010-10-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-10-08)

@cdn fixed in r69360: <http://trac.webkit.org/changeset/69360>

### in...@chromium.org (2010-10-08)

[Empty comment from Monorail migration]

### ch...@gmail.com (2010-10-08)

The fix does not work in all cases so we need to look at this more

### la...@chromium.org (2010-10-12)

Bulk moving to mstone 8, at this point work on m7 should effectively be closed.  If something in this bulk edit is not actively being worked on, please change the mstone to m9.

### ke...@google.com (2010-11-01)

Any update on this?  We're nearing the point we need to punt this.

### ch...@gmail.com (2010-11-01)

The latest news is that we are trying to get the original proposed fix in but no one is willing to r+ it. In the meantime an unrelated patch has made it so you can't hit this from http and https schemas (file still works though). I have asked ap@webkit who write that patch if he can comment on how we might be able to do the same for other schemas and am waiting on a response. There has also been discussion of merging the original patch to m7 and m8 and then hopefully getting a better fix in by m9.

### sc...@gmail.com (2010-11-01)

The M7 ship has sailed.

@kerz: we typically leave security bugs on a given milestone if they might still make a follow-up patch to that milestone.

### ke...@chromium.org (2010-11-03)

Wanted to know if this is really a blocker or not I guess.

### sc...@gmail.com (2010-11-03)

Ah, I see. No, I don't think we would block for this bug, so I'm removing the ReleaseBlock-Stable label.

We are however keen to fix it for the M8 release (or its subsequent refresh patch) so leaving the Mstone-8 label.

### ch...@gmail.com (2010-11-17)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-18)

Ok, we finally got to the bottom of this one, and it certainly qualifies for a $1000 Chromium Security Reward!
Thanks in particular for the alternate repro in https://crbug.com/chromium/55831#c8, as that was extremely helpful and enabled the non-Linux devs to start getting a handle on it :D

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

### in...@chromium.org (2010-11-18)

Fixed in http://trac.webkit.org/changeset/72230. Merge to 552 will be tricky as loader.cpp has merge issues and loader/cache directory did not exist (all those files were in loader dir itself).

### sc...@gmail.com (2010-11-18)

Maybe M9 is the better choice after all :-/

### ao...@gmail.com (2010-11-18)

Most excellent. This reward is going to Red Cross. We've already balanced this month's budget with the recent rewards :)

Surprisingly no duplicate issues have turned up even though this has been open for a while. Based on that probably not too much harm in delaying a merge.

### sc...@gmail.com (2010-11-21)

Payment is in the electronic system.

### in...@chromium.org (2010-12-10)

this is going to m9 considering the risk of merge and inability to merge since code changed.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-08)

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

This issue was migrated from crbug.com/chromium/55831?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083225)*
