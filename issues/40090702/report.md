# use-after-free in imageloader with fallbackcontent

| Field | Value |
|-------|-------|
| **Issue ID** | [40090702](https://issues.chromium.org/issues/40090702) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ch...@gmail.com |
| **Created** | 2011-05-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free

**VERSION**  

Chrome Version: all  

Win 7 - 11.0.696.65 (Official build 84435)  

Linux x64 - 13.0.759.0 (Developer Build 84563) Ubuntu 11.04  

OSX 10.6 Snow Leopard - 11.0.696.65

**REPRODUCTION CASE**  

only works from a server, and the referenced files should exist but not have a reasonable mimetype, for example touch lol.wut should work.

<object type="image/jpeg" data="/aaaaaaa/lol.wut">
<object type="image/jpeg" data="/aaaaaaa/lol.wut">

test url:  

<http://miau.biz/6bfefc3b-21ef-43c1-861e-95ab3cae1a80.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: sad tab  

Crash State:

Address 0x10e16078 is 8 bytes inside a block of size 40 free'd  

at 0x4C29146: free (vg\_replace\_malloc.c:913)  

by 0x131916C: WebCore::HTMLObjectElement::renderFallbackContent()

Address 0x5151515151515179 is not stack'd, malloc'd or (recently) free'd  

General Protection Fault  

at 0x17ABD2A: WebCore::ImageLoader::updateFromElement()

## Attachments

- [mini.html](attachments/mini.html) (text/plain; charset=us-ascii, 102 B)

## Timeline

### in...@chromium.org (2011-05-08)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-08)

This sounds very similar to http://code.google.com/p/chromium/issues/detail?id=55831 (I cc:ed you, miaubiz). It's supposed to be fixed a while ago :-/

Cris, weren't you taking care of that one, along with Adam?

### mi...@gmail.com (2011-05-08)

            m_imageLoader.clear();
            detach();
            attach();
            return;


this is back in the wrong order?

http://trac.webkit.org/changeset/69360/trunk/WebCore/html/HTMLObjectElement.cpp

### mi...@gmail.com (2011-05-08)

n/m.  it was rolled back in 69430 and fixed differently in 72230

### mi...@gmail.com (2011-05-08)

"In the meantime an unrelated patch has made it so you can't hit this from http and https schemas (file still works though)."

now it's the opposite of this.  so http works but file doesn't.

### mi...@gmail.com (2011-05-08)

in 55831 the referred file should _not_ exist, while as now, it _should_ exist.

### sc...@gmail.com (2011-05-09)

Btw, nice catch @miaubiz. Adding reward-topanel label for future consideration :)

### [Deleted User] (2011-05-18)

I have a patch for this. Probably we should have done this for the original bug. The previous bug was caused by a load error on stacked image objects with the same target. This one is caused by a decode error but has a very similar outcome.

Basically if we just clear the image from the image loader rather than delete the image loader everything works as expected and the image loader will get deleted later once we fall back through it on the stack.

### [Deleted User] (2011-05-18)

filed upstream as https://bugs.webkit.org/show_bug.cgi?id=61005

Miaubiz: do you have a webkit.org account that you would like me to CC?

### [Deleted User] (2011-05-18)

patch landed on webkit in http://trac.webkit.org/changeset/86725

### in...@chromium.org (2011-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2011-05-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-05-23)

merged to m12 in 87088

### mi...@gmail.com (2011-05-24)

@cdn: sorry, I don't.  thanks for the offer tho.

### sc...@gmail.com (2011-06-02)

@miaubiz: thanks for catching this one! Seems like it helped us finish making this area robust :)
$1000

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

### sc...@gmail.com (2011-06-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-09)

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

This issue was migrated from crbug.com/chromium/81949?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090702)*
