# Use-after-free in FrameLoader with no form post method

| Field | Value |
|-------|-------|
| **Issue ID** | [40092540](https://issues.chromium.org/issues/40092540) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-07-10 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free

**VERSION**  

Chrome Version: stable + trunk  

Operating System: linux 64bit

**REPRODUCTION CASE**  

src/third\_party/WebKit/LayoutTests/fast/events/form-iframe-target-before-load-crash.html

minus method="post"

## 4c4 < <form id="form1" style="display:none" target="test" action="http://anything.com"></form>

> ```
>     <form id="form1" style="display:none" method="post" target="test" action="http://anything.com"></form>  
> 
> ```

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:  

Invalid read of size 8  

at 0x1A52249: WebCore::FrameLoader::loadURL  

Address 0x3601b818 is 744 bytes inside a block of size 2,344 free'd  

Invalid write of size 1  

at 0x1A52250: WebCore::FrameLoader::loadURL  

Address 0x414141414141482e is not stack'd, malloc'd or (recently) free'd

## Attachments

- [761_2344.html](attachments/761_2344.html) (text/html; charset=us-ascii, 1.2 KB)
- [vg.txt](attachments/vg.txt) (text/plain; charset=us-ascii, 9.8 KB)
- [google-chrome-vg.txt](attachments/google-chrome-vg.txt) (text/plain; charset=us-ascii, 5.0 KB)
- [asan.txt](attachments/asan.txt) (text/plain; charset=us-ascii, 4.8 KB)

## Timeline

### in...@chromium.org (2011-07-10)

[Empty comment from Monorail migration]

### tk...@chromium.org (2011-07-11)

I'm not familiar with FrameLoader.  Adam, can you take a look at this?


### sc...@gmail.com (2011-07-11)

Adam's currently (very kindly) looking at a different bug, and he's generally busy with non-security items this quarter. So any suggestions for other people that might be able to tackle this?

### in...@chromium.org (2011-07-13)

I can fix it. It uses a variant of layouttest i used in http://trac.webkit.org/changeset/70517.

The Frame Protector needs to be in higher in the stack. This one uses the loadURL path since there is no form post method.

    if (request.resourceRequest().httpMethod() == "POST")
        loadPostRequest(request.resourceRequest(), referrer, request.frameName(), lockHistory, loadType, event, formState.get());
    else
        loadURL(request.resourceRequest().url(), referrer, request.frameName(), lockHistory, loadType, event, formState.get());

    // FIXME: It's possible this targetFrame will not be the same frame that was targeted by the actual
    // load if frame names have changed.
    Frame* sourceFrame = formState ? formState->sourceFrame() : m_frame;
    Frame* targetFrame = sourceFrame->loader()->findFrameForNavigation(request.frameName());
    if (targetFrame && targetFrame != sourceFrame) {
        if (Page* page = targetFrame->page())
            page->chrome()->focus();
    }



### in...@chromium.org (2011-07-13)

Filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=64457

### sc...@gmail.com (2011-07-13)

Committed r90936: <http://trac.webkit.org/changeset/90936>

### sc...@gmail.com (2011-07-16)

Merged to M13: http://trac.webkit.org/changeset/91143

### sc...@gmail.com (2011-07-20)

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

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-09)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed.. 

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

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

This issue was migrated from crbug.com/chromium/88846?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092540)*
