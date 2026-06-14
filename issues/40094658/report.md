# Redirect to chrome:// URIs via Location: header

| Field | Value |
|-------|-------|
| **Issue ID** | [40094658](https://issues.chromium.org/issues/40094658) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2011-09-04 |
| **Bounty** | $2,337.00 |

## Description

**VULNERABILITY DETAILS**  

Usually, Google Chrome don't allow redirect to chrome:// URIs.

For example,

<meta http-equiv="refresh" content="0;url=chrome://about">

and

<script>location.href="chrome://about"</script>

don't redirect.

But Location: header is different.  

I could redirect to "chrome://about" via following header.

Location:chrome://about

I think this behavior is bad.

**VERSION**  

Chrome Version: 13.0.782.220 stable  

Operating System: Windows Vista sp2

## Timeline

### js...@chromium.org (2011-09-05)

I just tested, and the redirect does work. The DOMUI process restrictions prevent settings manipulation, and same-origin prevents the data from getting read by a web site. So, it does seem to be pretty well mitigated, but we really shouldn't be allowing it regardless.

(Adding in some people who might have a quick pointer on what's going on here.)

### ke...@google.com (2011-09-08)

This looks fairly easy to diagnose: renderer checks the scheme for meta refresh and JS redirects against WebSecurityPolicy, but this doesn't apply to HTTP redirects because they are handled at a different layer. I don't know, but might this be intentional because it doesn't have the same security implications?

It might be simple to change this, URLRequestHttpJob::IsSafeRedirect looks like a reasonable place to start.

### sc...@gmail.com (2011-09-08)

There are security implications. A web page must never be able to redirect to chrome:// under any circumstances. We've had really unpleasant XSS there in the past. Tom's CSP work should cut down on that, but still...

Fancy tackling it? :)

### ke...@chromium.org (2011-09-08)

Sure.

### ke...@google.com (2011-09-09)

This is turning out to be tricky. about://* and chrome://* internally use a lot of chrome: redirects, so it would appear that blocking them in ChildProcessSecurityPolicy breaks several things that some people might consider important (like chrome://settings).

At this point it looks like we want to do something like allowing chrome:// redirects conditionally based on the origin of the redirect, but this is sounding complicated and easy to get wrong, so I'm soliciting feedback.

Does anyone in the cc: line have any thoughts on how to address this bug?

### ke...@chromium.org (2011-09-12)


There is a simple change to URLRequestHttpJob that looks like it fixes the issue without any undesirable side effects:
http://codereview.chromium.org/7873007

I'd like feedback from someone in net/OWNERS if this would be acceptable. I haven't written a unit test because this might be too hacky, but other approaches have some significant trade-offs also.

Another possibility would be to try to do this in WebKit, because it does some processing of HTTP redirects. If it denied redirects based on a check to SecurityOrigin::canDisplay() then this would resolve the issue, but would also change behavior in other browsers. I don't know whether or not this would cause problems.

### sc...@gmail.com (2011-09-13)

[Empty comment from Monorail migration]

### rv...@chromium.org (2011-09-14)

[Empty comment from Monorail migration]

### ke...@chromium.org (2011-09-23)

Upstreamed to WebKit as: https://bugs.webkit.org/show_bug.cgi?id=68706

### [Deleted User] (2011-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2011-09-28)

[Empty comment from Monorail migration]

### ke...@chromium.org (2011-10-04)

Landed upstream.

Committed r96610: <http://trac.webkit.org/changeset/96610>

### js...@chromium.org (2011-10-05)

Batch update: Guessing based on search criteria that this security bug impacted a stable release.

### in...@chromium.org (2011-10-07)

merged to m15 in r96957

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

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

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-16)

[Empty comment from Monorail migration]

### aw...@google.com (2016-12-16)

We're going over old bugs that might have missed going in front of the VRP panel.  The panel decided to award $1,000 for this bug, plus an additional $1337!

### aw...@chromium.org (2016-12-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/95374?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094658)*
