# Security: body of POST request initiated 302-redirect chain can be recovered by script on last page in chain using XSS Auditor

| Field | Value |
|-------|-------|
| **Issue ID** | [40078631](https://issues.chromium.org/issues/40078631) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | ne...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2014-01-06 |
| **Bounty** | $500.00 |

## Description

This issue is not XSS Auditor bypass.

**VULNERABILITY DETAILS**  

When a POST request initiates a chain of 302 redirects, XSSAuditor for last (first non-302) page is initialized using URL of last page and POST body of first (initial) request. If attacker controls that last page, he can use char-by-char bruting to recover POST body of initial request in linear time.

More detailed:

1. Attacker asks user to login using victim.com (for example).
2. In typical case, user will be redirected back to attacker's site after login. So, for example, if user password is submitted to login.html, sequense of requests and responces could be like that: POST <http://victim/login.html> - 302 redirect to <http://victim/somethingother> -> GET <http://victim/somethingother> - 302 redirect to <http://attacker/something> -> GET <http://attacker/something> - 200 OK.
3. If attacker added <script> to this last return url on step 1, XSS Auditor will try to detect XSS in script tags. XSS Auditor's init() is called with POST body from request to login.html, but filters document controlled by attacker. Attacker could add <script> tag with document.write and see if it is filtered. XSS Auditor checks if <script> tag contents is contained in request, so attacker could be trying add one char to already bruted part and recover full request body char-by-char in linear time.

This issue and <https://crbug.com/chromium/331060> are completely different in how to achive XSS auditor initialized for attacker controlled page using body of request to another domain but are absolutely identical in method of recovering POST body after that.

I don't know if this issue is security issue as <https://tools.ietf.org/html/draft-ietf-httpbis-p2-semantics-17#section-7.3> allows request body be repeated to attacker in the example above, but I'm sure I have seen in the debugger that XSS Auditor's init() is called with request body containing my facebook password for filtering page on other site that that asked me to login with my facebook account.

**VERSION**  

Chrome Version: both stable and beta seems to be affected  

Operating System: tested on Linux

**REPRODUCTION CASE**  

I've made simple "redirecting after login" webserver victim\_server.py, and I use body-recovering code I've posted in <https://crbug.com/chromium/331060> in attacker\_redirect.html. For reproducting, follow these steps:

1. python victim\_server.py
2. make attacker\_redirect.html accessible through http:// not file:// as we want allow victim redirect back to it
3. open http://.../attacker\_redirect.html in chromium
4. click "login using victim"
5. enter your "password" on victim site (it could be any [a-z]\* string) and press "submit"
6. see alert from attacker containing string you entered

## Attachments

- [attacker_redirect.html](attachments/attacker_redirect.html) (text/html, 2.0 KB)
- [victim_server.py](attachments/victim_server.py) (text/plain, 1.2 KB)

## Timeline

### ia...@chromium.org (2014-01-06)

abarth, tsepez, could you take a look at this?

### ts...@chromium.org (2014-01-06)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-01-07)

Adam, it looks like we need to clear the post body when we receive a redirect.

### cl...@chromium.org (2014-01-07)

[Empty comment from Monorail migration]

### ne...@gmail.com (2014-01-08)

May be a stupid question, but is there a way to gain POST request body with javascript without using XSS Auditor even in same origin case?  

For example, if somebody added something like <script src="http://very-cool-widget/script.js"> on his site, then such widget can recover POST body using method I've described in this issue.

I don't think that is really security issue as if attacker found a way to execute javascript in victim's origin, he can do a lot of other thinks (like simply changing form action, or even if he is not able to do that, he can redraw form with a message like "error, please submit again"). I'm asking because I have not found any other way to do that with javascript (may be I'm just a noob).

### ts...@chromium.org (2014-01-08)

Hey Neex, for the sake of completeness, can you tell me which version of chrome you were using?

### ne...@gmail.com (2014-01-08)

I've tested sample exploit above on linux using chromium 31.0.1650.63 from ubuntu repository, google chrome 32.0.1700.68 and trunk build 34.0.1770.0.

### ts...@chromium.org (2014-01-09)

CL up at https://codereview.chromium.org/128823003/

### bu...@chromium.org (2014-01-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=164749

------------------------------------------------------------------------
r164749 | tsepez@chromium.org | 2014-01-09T07:54:09.674092Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/script-tag-post-redirect.html?r1=164749&r2=164748&pathrev=164749
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/resources/static-script.html?r1=164749&r2=164748&pathrev=164749
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/http/tests/security/xssAuditor/script-tag-post-redirect-expected.txt?r1=164749&r2=164748&pathrev=164749
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/html/parser/XSSAuditor.cpp?r1=164749&r2=164748&pathrev=164749

XSSAuditor takes post body from current request, not the original request.

In the face of a redirect, the information in the original body can't be
reflected in the final page, when we redirect from post to get, since the
get has no body.  And for a 307-style redirect from post to post, the body
will appear in the final post.

This avoids some false positives and also the possibility of some info
leaks from the original post.

BUG=331725
R=abarth@chromium.org

Review URL: https://codereview.chromium.org/128823003
------------------------------------------------------------------------

### in...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ts...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### dh...@google.com (2014-01-16)

Requesting merge for M32 and M33.

### dx...@chromium.org (2014-01-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-01-17)

We'll let this bake until M33.

### la...@google.com (2014-01-18)

Approved for M33 (1750)

### bu...@chromium.org (2014-01-22)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=165546

------------------------------------------------------------------------
r165546 | tsepez@chromium.org | 2014-01-22T20:13:18.374930Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/http/tests/security/xssAuditor/script-tag-post-redirect-expected.txt?r1=165546&r2=165545&pathrev=165546
   M http://src.chromium.org/viewvc/blink/branches/chromium/1750/Source/core/html/parser/XSSAuditor.cpp?r1=165546&r2=165545&pathrev=165546
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/http/tests/security/xssAuditor/script-tag-post-redirect.html?r1=165546&r2=165545&pathrev=165546
   A http://src.chromium.org/viewvc/blink/branches/chromium/1750/LayoutTests/http/tests/security/xssAuditor/resources/static-script.html?r1=165546&r2=165545&pathrev=165546

Merge 164749 "XSSAuditor takes post body from current request, n..."

> XSSAuditor takes post body from current request, not the original request.
> 
> In the face of a redirect, the information in the original body can't be
> reflected in the final page, when we redirect from post to get, since the
> get has no body.  And for a 307-style redirect from post to post, the body
> will appear in the final post.
> 
> This avoids some false positives and also the possibility of some info
> leaks from the original post.
> 
> BUG=331725
> R=abarth@chromium.org
> 
> Review URL: https://codereview.chromium.org/128823003

TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/145183002
------------------------------------------------------------------------

### dh...@chromium.org (2014-02-11)

[Empty comment from Monorail migration]

### dh...@google.com (2014-02-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-02-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-03-04)

Thanks for the report! This one qualifies for a $500 reward. 

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-17)

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

This issue was migrated from crbug.com/chromium/331725?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078631)*
