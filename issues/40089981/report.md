# Floats not cleared due to overflow (remaining usecase)

| Field | Value |
|-------|-------|
| **Issue ID** | [40089981](https://issues.chromium.org/issues/40089981) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | se...@gtempaccount.com |
| **Created** | 2011-04-18 |
| **Bounty** | $1,000.00 |

## Description

credit: miaubiz

branched from http://code.google.com/p/chromium/issues/detail?id=73962

## Attachments

- [checkFloats73962.html](attachments/checkFloats73962.html) (text/plain; charset=us-ascii, 1.0 KB)
- [a0f810758b15901be881b9f0d9f61f60.html](attachments/a0f810758b15901be881b9f0d9f61f60.html) (text/html; charset=iso-8859-1, 4.0 KB)
- [639e5a6bfae63b1c73388fa1c8aa3e92.html](attachments/639e5a6bfae63b1c73388fa1c8aa3e92.html) (text/html; charset=us-ascii, 6.7 KB)
- [8a99c05f32b97bccb58efc6dd77f198c.html](attachments/8a99c05f32b97bccb58efc6dd77f198c.html) (text/plain; charset=us-ascii, 1.0 KB)
- [f937de4b9adba72df7e7be2e7d0c6d24.html](attachments/f937de4b9adba72df7e7be2e7d0c6d24.html) (text/html; charset=iso-8859-1, 7.0 KB)
- [00167e7ff4ca78b5c58725d9a4451094.html](attachments/00167e7ff4ca78b5c58725d9a4451094.html) (text/html; charset=iso-8859-1, 7.0 KB)
- [3967b9cc687139407fd542a03ec6c175.html](attachments/3967b9cc687139407fd542a03ec6c175.html) (text/html; charset=us-ascii, 4.1 KB)
- [b7ae9b1d929f9f0a05d5ac0ee0b91ed3.html](attachments/b7ae9b1d929f9f0a05d5ac0ee0b91ed3.html) (text/html; charset=iso-8859-1, 6.3 KB)
- [5bdfe520a7f3334a8cb05f6c517621f8.html](attachments/5bdfe520a7f3334a8cb05f6c517621f8.html) (text/html; charset=us-ascii, 6.9 KB)
- [5505c199c975a71eebecfd9a16bf4322.html](attachments/5505c199c975a71eebecfd9a16bf4322.html) (text/html; charset=us-ascii, 6.9 KB)
- [8174df72d33c2259eb1e2f5d8cb317b5.html](attachments/8174df72d33c2259eb1e2f5d8cb317b5.html) (text/html; charset=us-ascii, 7.0 KB)
- [79746-30.zip](attachments/79746-30.zip) (application/zip; charset=binary, 37.0 KB)

## Timeline

### in...@chromium.org (2011-04-20)

miaubiz, i cannot reproduce in latest chrome build 12.0.742.0 (82260) with webkit 84325. I also ran it in MallocScribble and any free blocks should be detected, but it exited properly.

Can you please provide any other usecase that still crash for you.

### mi...@gmail.com (2011-04-20)

certainly.

### in...@chromium.org (2011-04-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-04-20)

Thanks Miaubiz.

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=59015

### in...@chromium.org (2011-04-22)

miaubiz: do you have more testcases with different stacks. I finally have a fix, so can test more now. Like you can send me like 20-30 more.

### mi...@gmail.com (2011-04-23)

this is the only stacktrace I am getting anymore.  here's 30 more of this stack.

### in...@chromium.org (2011-05-04)

Fixed in http://trac.webkit.org/changeset/85705.

### sc...@gmail.com (2011-05-07)

Merged to M12: http://trac.webkit.org/changeset/86003

### sc...@gmail.com (2011-06-02)

@miaubiz -- thanks for great work in this bug and also 73962. We'll reward them separately. $1000 for this one; thanks for the thoroughness in making sure we nailed all your test cases.

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

### sc...@gmail.com (2011-06-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-09)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

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

This issue was migrated from crbug.com/chromium/79746?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089981)*
