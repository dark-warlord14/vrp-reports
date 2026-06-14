# Bad cast to RenderBlock with floating select element with required attribute 

| Field | Value |
|-------|-------|
| **Issue ID** | [40088645](https://issues.chromium.org/issues/40088645) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | md...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2011-03-08 |
| **Bounty** | $500.00 |

## Description

Chrome Version : <Copy from: 'about:version'>  

**URLs (if applicable) :**  

Other browsers tested: Also tested Chrome 10.x on Mac and it FAILED

**What steps will reproduce the problem?**

1. Go here <http://jsfiddle.net/EWa7Z/>
2. Submit the form without first picking an option
3. Submit again or pick an option

**What is the expected result?**

I expect that the form will let me select an option and then validate correctly.

**What happens instead?**

Chrome Crashes

Please provide any additional information below.

Another issue also exists with the validation not updating when using keyword to navigation. You can repeat this by going here, <http://jsfiddle.net/EWa7Z/>, click submit, then (after chrome focues on the select) use your arrow keys to select an option.

## Timeline

### tk...@chromium.org (2011-03-09)

Confirmed.
This looks a bug of validation message bubble.


### tk...@chromium.org (2011-03-09)

[Empty comment from Monorail migration]

### tk...@chromium.org (2011-03-09)

Posted a patch to WebKit: https://bugs.webkit.org/show_bug.cgi?id=55995


### in...@chromium.org (2011-03-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-09)

[Empty comment from Monorail migration]

### tk...@chromium.org (2011-03-15)

Fixed in WebKit.

We need to merge the following two changes to M10 and M11 branches:
http://trac.webkit.org/changeset/80773
http://trac.webkit.org/changeset/81088

M9 or prior don't have this issue.



### sc...@gmail.com (2011-03-15)

Status -> WillMerge to make sure we do the merges.

### sc...@gmail.com (2011-03-19)

Merged to M11:
http://trac.webkit.org/changeset/81541
http://trac.webkit.org/changeset/81542

@mdhgriffiths: this turned out to be a security bug. It there some more descriptive name you'd like us to credit you with in our release notes?

### md...@gmail.com (2011-03-19)

[Comment Deleted]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### md...@gmail.com (2011-04-01)

@scarybeasts, You can give credit to me, Michael Griffiths.

Also, is this a security bug that qualifies for a bounty reward?

Thanks!

### sc...@gmail.com (2011-04-15)

@mdhgriffiths: as it happens... this DOES qualify for a provisional $500 Chromium Security Reward :D We normally don't reward things not reported as Security issues, but see below for rules etc.

---
NOTE: normally we do not reward security bugs unless initially filed with the
security template. Sometimes we make an exception for the first time an individual
files a security bug as a non-security issue.
For full guidelines on filing security bugs, see:
http://www.chromium.org/Home/chromium-security/reporting-security-bugs
---

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

### md...@gmail.com (2011-04-15)

@scarybeasts: Thank you! I can't wait to brag to my co-workers lol :P

I'll be sure to test more next time and to properly label the issue. How do I go about getting this bounty?

Thanks again! You, and Google have just made my day! 

### sc...@gmail.com (2011-04-15)

@mdhgriffiths: first we get the fix out to the stable channel (should be within a couple of weeks thanks to our 6-week release cycle). Then, ping cevans@chromium.org to start the payment process. Thanks :)

### md...@gmail.com (2011-04-15)

Thanks, Sounds good! Let me know when it's good :)

### sc...@gmail.com (2011-04-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-04-29)

Ok, ping cevans@chromium.org to set up payment :)

### md...@gmail.com (2011-04-29)

[Comment Deleted]

### md...@gmail.com (2011-04-29)

Sweet! Thanks again! :) I've sent cevans an email. (Thats what you meant by ping, right? :P)

### sc...@gmail.com (2011-08-12)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/75347?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088645)*
