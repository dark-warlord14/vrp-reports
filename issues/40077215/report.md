# Same Origin Policy Bypass via getSVGDocument() method.

| Field | Value |
|-------|-------|
| **Issue ID** | [40077215](https://issues.chromium.org/issues/40077215) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | is...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2009-09-09 |
| **Bounty** | $500.00 |

## Description

Chrome Version       : Google Chrome	2.0.172.43 (Official Build )
WebKit	530.5
V8	1.1.10.15
User Agent	Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) 
AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.172.43 Safari/530.5
URLs (if applicable) : http://sh0dan.org/svg-test/svg-sopb.html
Other browsers tested:
  Add OK or FAIL after other browsers where you have tested this issue:
     Safari 4:
  Firefox 3.x: OK
         IE 7:
         IE 8:

What steps will reproduce the problem?
1. Load an SVG image in an object tag from a third party site. Set data as 
the uri of the svg file, type as "image/svg+xml"
2. Get a reference to the object and call the getSVGDocument() method.
3. This creates a reference to the objects contentDocument. 
4. From here it is possible to read/set properties of the contentDocument 
of the third party, including cookies.

What is the expected result?
Permission should be denied by same origin policy.

What happens instead?
Ability to read/write cookie data, and view other data from a third party 
sites contentDocument. 

Please provide any additional information below. Attach a screenshot if
possible.
Proof of Concept: http://sh0dan.org/svg-test/svg-sopb.html

Please note the "victim" site (peacecorpwiki) is not under my control, it 
is only used as a demonstration of the issue.
-Isaac


## Timeline

### ab...@chromium.org (2009-09-09)

Thanks for the report.  We'll handle this issue via the bugs.webkit.org issue tracker.  I'm going to move the report 
over there.  Do you have a bugs.webkit.org account I can CC so you can track the progress of this issue?

### ab...@chromium.org (2009-09-09)

Upstream issue is here:
https://bugs.webkit.org/show_bug.cgi?id=29064

### is...@gmail.com (2009-09-09)

No problem. I do now it should be: isaac.dawson@gmail.com.

### sc...@gmail.com (2009-09-09)

Great bug Isaac! Thanks for reporting it.
Also repro in Chrome v3 beta / Windows & Chrome v4 dev / Linux.
Seems like it should repro in Safari 4 due to being a bug in the Webkit base but does 
not seem to at first glance. Thanks to Safari 4's lack of a Javascript console 
(unless I'm on drugs) I can't tell if the test case simply needs a tweak or there is 
some other reason. Perhaps Adam has an insight?

Anyway, Isaac - how would you like to be credited when we release the security 
update? e.g. name and optional affiliation?

One last question, so we can assign a severity (Medium or High) depending on whether 
the victim site has to permit hosting of an SVG or not. Did you try the <object> tag 
with non-SVG data as the target? HTML or XML perhaps? Can you still get a cross-
domain handle to the remote document in any non-SVG case?

### ab...@chromium.org (2009-09-09)

w.r.t. not reproducing in Safari: I bet this is a bug in the V8 bindings.  Safari uses JSC bindings.

### sc...@gmail.com (2009-09-09)

Who should we cc? dglazkov@ ?

### is...@gmail.com (2009-09-09)

It appears that both embed and object works, as long it is an svg file. What is 
strange is that it appears even valid SVG files do not always work. For example, 
instead of using the PoC SVG URI try 
"http://people.mozilla.org/~dholbert/tests/smil/demos/clouds_v1.svg" and you will see 
getSVGDocument throws an error. I looked at it in burp proxy and found the only 
difference is that if the server responds with the proper content-type 
(image/svg+xml) getSVGDocment will work. If the server responds with text/xml, 
getSVGDocument will throw an error. So in your testing be aware of that fact. 

Additionally, I tried changing mime type to text/html and text/xml and I just get an 
exception when calling the getSVGDocument() method. Looks like SVG only (with the 
proper mime type) to me.

As for credit, just my name is fine thanks. 

### ab...@chromium.org (2009-09-09)

@scarybeasts: dglazkov is CCed on the upstream version of the bug.

### sc...@gmail.com (2009-09-09)

Thanks, Isaac. I propose "Medium" severity since it will not be possible to host SVGs 
on all (even many?) trusted domains.
Adam, what do you think? I know Wikipedia hosts SVGs (with content-type image/svg+xml) 
so we could always err on the side of caution and elect for "High" based on that 
alone...

### ab...@chromium.org (2009-09-09)

It's up to you.  I'd probably rate it high because hosting an SVG document is a perfectly normal thing to do.  In 
any case, I'm going to try to create a patch tonight.  I've almost got the PoC converted to a LayoutTest.

### ab...@chromium.org (2009-09-09)

Patch posted upstream for review.

### ab...@chromium.org (2009-09-10)

Committed webkit@48240: <http://trac.webkit.org/changeset/48240>

### ma...@gmail.com (2009-09-10)

Anthony, this needs to go onto the 195 branch.

### ab...@chromium.org (2009-09-12)

@isaac: Just to keep you updated, your patch should be in today's beta release, which you can download here:

http://www.google.com/landing/chrome/beta/

If you can verify that we've fixed the issue, that would be helpful.  You're catching us at an odd moment in our 
release cycle.  Hopefully we'll be able to push the patch to stable users in short order.

Thanks for bearing with us.

### is...@gmail.com (2009-09-12)

Looks good, just tested both embed and object tags and getSVGDocument just returns 
undefined for a 3rd party svg image file. I tested an svg file hosted in the same 
origin and that still works as expected. 
Thanks and great work getting this patched!

### sc...@gmail.com (2009-10-23)

Removing view restriction as this has been fixed for a long time now.

### sc...@gmail.com (2010-02-23)

[Empty comment from Monorail migration]

### ra...@gmail.com (2010-04-28)

Did this change go too far when the protocol is 'file:'?  

I get a similar failure that only happens on Chrome [5.0.342.9 beta], where Firefox
[Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.3) Gecko/20100401
Firefox/3.6.3] and Safari [Version 4.0.5 (6531.22.7)] both work.

Chrome reports:  

Unsafe JavaScript attempt to access frame with URL file://localhost/path/test.svg
from frame with URL file://localhost/path/test.html. Domains, protocols and ports
must match.

The object usage is simply:
    <object type="image/svg+xml" data="test.svg">SOME TEXT</object>

The result of the error is that getSVGDocument() call from this object returns undefined.

It appears to me that domains, protocols and ports match and Chrome is being overly
restrictive.  Is there some other reason that "file:" usage must fail?

A workaround is to use a http server.  Then, getSVGDocument returns a proper value. 
But that is not always convenient and seems like it should not be necessary.

Please advise if this should be handled in a new bug.  I don't know if the protocol
is to open a new issue or comment on the issue I believe should be re-opened.   

### js...@chromium.org (2010-04-28)

Please see https://crbug.com/chromium/4197 and the following blog post for a detailed explanation of the 
"file:" URL behavior: 
http://blog.chromium.org/2008/12/security-in-depth-local-web-pages.html


### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### je...@gmail.com (2011-03-23)

Problem always exists when trying to open a local html file which include a svg file embed. HTML/JS/SVG files are in the same directory but getSVGDocument returns undefined as if it was a cross domain call.

### js...@chromium.org (2011-10-05)

Batch update: fuzzily determined that this security bug affected a stable release.

### la...@chromium.org (2012-10-11)

[Empty comment from Monorail migration]

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

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/21338?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077215)*
