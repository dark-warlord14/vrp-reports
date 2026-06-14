# Security: ability to read cross domain image data using toDataURL and getImageData via createPattern 

| Field | Value |
|-------|-------|
| **Issue ID** | [40082834](https://issues.chromium.org/issues/40082834) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | is...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-08-22 |
| **Bounty** | $500.00 |

## Description

While converting some LayoutTests (and adding my own modifications) I came across a bug in how chrome handles 3rd party images loaded from a same origin page that forces a 301 redirect. By calling createPattern on the redirected image, it appears chrome either disregards the origin-clean flag, or some how it gets reset once createPattern is called on the 2d canvas context. I've created a proof of concept for this bug which you can find here:
http://sh0dan.org/chrome/canvas-read-remote-image-redirect.html. You'll note in the output that drawImage will cause security exceptions yet createPattern does not.

I ran the test against Chrome 6.0.472.41 beta. Firefox and opera both throw security exceptions. Also when the image src is set to a 3rd party URL directly (http://google.com.../logo1w.png), chrome will throw security exceptions for both drawImage and createPattern.

Thank you,
-Isaac

## Timeline

### in...@chromium.org (2010-08-22)

Thanks Isaac. Working on the fix, i can see in the error in origin calculation in src\third_party\WebKit\WebCore\html\canvas\CanvasRenderingContext2D.cpp

### in...@chromium.org (2010-08-22)

Fix is working out fine. I have checked for similar patterns for originClean() issues, but this was the only affected. No other file uses this. i will upload the patch with layouttest by tmrw. [Might need platform specific results for exceptions :)]

Very nice catch Isaac.

### in...@chromium.org (2010-08-22)

Posted patch to webkit bug - https://bugs.webkit.org/show_bug.cgi?id=44399.

### is...@gmail.com (2010-08-22)

Awesome, any chance I can get added to that bug in the webkit bug tracker? My user name is isaac.dawson@gmail.com. As always, thanks for the quick response. 

### in...@chromium.org (2010-08-23)

Isaac, i added you to the cc list on the webkit bug.

### is...@gmail.com (2010-08-23)

Just as a quick side note, this is in relation to some work I will be presenting at a conference around September 22nd-3rd. Any chance this bug will be fixed by then so I can mention it? 
Thanks.

### in...@chromium.org (2010-08-23)

This bug should get fixed on trunk by tmrw and be pushed to stable in upcoming version of chrome v6. So, i think we should be in good shape before your Sept 22 timeframe.

### sc...@gmail.com (2010-08-23)

Nice find, Isaac!!
Inferno's 1-line fix is on the same line that I fixed a separate similar bug on a few months back. See
http://code.google.com/p/chromium/issues/detail?id=39861
https://bugs.webkit.org/show_bug.cgi?id=36838
http://trac.webkit.org/changeset/56810
Unbelievable... I'm going to forgive myself for not spotting it, though :)

Isaac, please feel free to go ahead and present on the Sep 22nd whatever happens. And thanks for the heads up.

I've nudged the severity to Medium; that's how we've rated previous image disclosures.

### in...@chromium.org (2010-08-23)

Fixed in http://trac.webkit.org/changeset/65826.

Also merged to 472.

### bu...@gmail.com (2010-08-23)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=57104 

------------------------------------------------------------------------
r57104 | inferno@chromium.org | 2010-08-23 13:23:59 -0700 (Mon, 23 Aug 2010) | 28 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/http/tests/security/canvas-remote-read-remote-image-redirect-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/http/tests/security/canvas-remote-read-remote-image-redirect.html
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/html/canvas/CanvasRenderingContext2D.cpp?r1=57104&r2=57103

Merge 65826 - 2010-08-23  Abhishek Arya  <inferno@chromium.org>

        Reviewed by Dimitri Glazkov.

        Fix security origin calculation in createPattern. Need to use
        cachedImage->response().url() instead of cachedImage->url().
        https://bugs.webkit.org/show_bug.cgi?id=44399.

        Test: http/tests/security/canvas-remote-read-remote-image-redirect.html

        * html/canvas/CanvasRenderingContext2D.cpp:
        (WebCore::CanvasRenderingContext2D::createPattern):
2010-08-23  Abhishek Arya  <inferno@chromium.org>

        Reviewed by Dimitri Glazkov.

        Tests that calling getImageData(), toDataURL() on a canvas tainted by
        a createPattern of a different origin image using redirects from same origin
        is not allowed.
        https://bugs.webkit.org/show_bug.cgi?id=44399

        * http/tests/security/canvas-remote-read-remote-image-redirect-expected.txt: Added.
        * http/tests/security/canvas-remote-read-remote-image-redirect.html: Added.


BUG=53001

Review URL: http://codereview.chromium.org/3124040
------------------------------------------------------------------------


### sc...@gmail.com (2010-08-23)

@isaac.dawson: status update for you; I'd estimate that this fix will get deployed to users next week.
First question: what credit line do you want? Plain Isaac Dawson or with some affiliation also?

### is...@gmail.com (2010-08-24)

plain Isaac Dawson is fine as i found it on my own time ;).

### sc...@gmail.com (2010-08-24)

@isaac.dawson: congratulations! We'd like to provisionally offer you a $500 Chromium Security Reward.
Although not a high severity issue, the rewards panel found this bug to be clever on account of its subtlety. We were also swayed by your nicely reduced test case. Thank you.

### is...@gmail.com (2010-08-25)

Thank you!

### sc...@gmail.com (2010-09-02)

Fix is live to users: http://googlechromereleases.blogspot.com/2010/09/stable-and-beta-channel-updates.html
And payment is in the electronic system :)

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/53001?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082834)*
