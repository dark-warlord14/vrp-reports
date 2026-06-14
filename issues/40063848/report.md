# Security: XSS in SSL Certificate error page

| Field | Value |
|-------|-------|
| **Issue ID** | [40063848](https://issues.chromium.org/issues/40063848) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI |
| **Reporter** | e3...@gmail.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2012-08-15 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The "Issued to" field in SSL Certificate is printed in SSL Certificate error page without HTML Encoding its content.

**VERSION**  

Chrome Version: 21.0.1180.79 + stable  

Operating System: Windows 7 64 Bit.

**REPRODUCTION CASE**  

By forcing traffic from chrome to go through burp suite program,  

and fill HTML tags in "generate a CA-signed certificate with a specific hostname", this tags rendered every time a visit to https site occurred.  

attachment show the burp suite configuration, and the result in chrome.

## Attachments

- [ChromeCertXSS.png](attachments/ChromeCertXSS.png) (image/png; charset=binary, 92.6 KB)

## Timeline

### ts...@chromium.org (2012-08-15)

Thanks.  Couldn't help but notice that you injected an <input> tag rather than a <script>.  Is it possible to execute script on that page, or does it run into a Content-Security-Policy violation?

Over to palmer@ who may have a setup to reproduce this.


### pa...@chromium.org (2012-08-15)

I can reproduce it, but I can't run script. I tried two methods:

CN=<script>alert(document.domain)</script>

and

CN=<h1 onmouseover="alert(document.domain)">haha</h1>

In the first case, the page shows the CN as " ", and in the second, it renders the <h1>haha</h1> but the event handler does not run. So I think CSP is saving us here. Without CSP this would be a big deal. I'll crank the severity back up if anyone can show a way to actually execute script.

Obviously, we still need to HTML-escape the strings. I'll start on that now.

### pa...@google.com (2012-08-16)

tsepez found a way to exploit it. CSP does not save us! Bumping this up to medium; although exploitable, the attacker still has to get an obviously bad certificate signed by a public CA. We consider that a mitigating factor.

A patch is up for review now...

### bu...@chromium.org (2012-08-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=152210

------------------------------------------------------------------------
r152210 | palmer@chromium.org | 2012-08-18T01:58:42.646152Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ssl/ssl_error_info.cc?r1=152210&r2=152209&pathrev=152210

Properly EscapeForHTML potentially malicious input from X.509 certificates.

BUG=142956

TEST=Create an X.509 certificate with a CN field that contains JavaScript.
When you get the SSL error screen, check that the HTML + JavaScript is
escape instead of being treated as HTML and/or script.

Review URL: https://chromiumcodereview.appspot.com/10827364
------------------------------------------------------------------------

### in...@chromium.org (2012-08-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-24)

@e3amn2l: Nice find! I'd like to credit you in our upcoming release notes. What name or handle would you like me to use?

### bu...@chromium.org (2012-08-24)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=153297

------------------------------------------------------------------------
r153297 | cevans@chromium.org | 2012-08-24T21:36:31.100281Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1229/src/chrome/browser/ssl/ssl_error_info.cc?r1=153297&r2=153296&pathrev=153297

Merge 152210 - Properly EscapeForHTML potentially malicious input from X.509 certificates.

BUG=142956

TEST=Create an X.509 certificate with a CN field that contains JavaScript.
When you get the SSL error screen, check that the HTML + JavaScript is
escape instead of being treated as HTML and/or script.

Review URL: https://chromiumcodereview.appspot.com/10827364

TBR=palmer@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10878063
------------------------------------------------------------------------

### bu...@chromium.org (2012-08-24)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=153298

------------------------------------------------------------------------
r153298 | cevans@chromium.org | 2012-08-24T21:37:14.572784Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1180/src/chrome/browser/ssl/ssl_error_info.cc?r1=153298&r2=153297&pathrev=153298

Merge 152210 - Properly EscapeForHTML potentially malicious input from X.509 certificates.

BUG=142956

TEST=Create an X.509 certificate with a CN field that contains JavaScript.
When you get the SSL error screen, check that the HTML + JavaScript is
escape instead of being treated as HTML and/or script.

Review URL: https://chromiumcodereview.appspot.com/10827364

TBR=palmer@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10869053
------------------------------------------------------------------------

### e3...@gmail.com (2012-08-24)

Please credit me as: "Emanuel Bronshtein" in upcoming release notes.

### sc...@gmail.com (2012-08-24)

@e3amn2l: thanks! We'd also like to offer you a $500 Chromium Security Reward for catching this!

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

### e3...@gmail.com (2012-08-25)

Thanks, to whom send my PayPal ID?

### sc...@gmail.com (2012-08-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### pa...@chromium.org (2013-02-25)

@e3amn2l: Arg, payment on this one totally slipped through the cracks. So sorry for the long delay! Someone will contact you shortly for steps on how to setup payment :) 

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-02-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/142956?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063848)*
