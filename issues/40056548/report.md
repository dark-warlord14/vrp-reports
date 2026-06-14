# Security: Autofill info can be captured by innocuous social engineering

| Field | Value |
|-------|-------|
| **Issue ID** | [40056548](https://issues.chromium.org/issues/40056548) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI, UI>Browser>Autofill |
| **Reporter** | si...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2012-04-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

A web page can be crafted that captures a user's autofill details when they press down, down, enter with nothing shown on screen (for me, at least). Pressing DDE could easily be socially engineered as part of a game, especially if there's some way of detecting when a user presses a key in the cycle.

**VERSION**  

Chrome Version: 18.0.1025.152 + stable  

Operating System: Windows 7 SP1

**REPRODUCTION CASE**  

It's attached. Your address should appear when you follow the instructions if you have it saved.

## Attachments

- [autofillsec.html](attachments/autofillsec.html) (text/html; charset=us-ascii, 819 B)

## Timeline

### js...@chromium.org (2012-04-12)

David, I'll take a closer look at this today and finish triage (unless you get to it first).

### [Deleted User] (2012-04-12)

isherman has been working in this area most recently.

### is...@chromium.org (2012-04-12)

Yikes.  That is a very slick reproduction case -- thanks for sharing it.

Ideally, we'll be able to query WebKit to check whether the popup was actually visible, and close it if it's not visible.  Investigating...

### in...@chromium.org (2012-04-13)

What is the bug here ? Is autofill popup not visible and not come on top ? That will help us adjust security severity.

### si...@gmail.com (2012-04-13)

[Comment Deleted]

### si...@gmail.com (2012-04-13)

It can be opened without being visible by putting it in a scrolled div.

### in...@chromium.org (2012-04-13)

[Empty comment from Monorail migration]

### is...@chromium.org (2012-04-20)

Upstreamed as [ https://bugs.webkit.org/show_bug.cgi?id=84420 ].  I have most of a fix ready... 

### in...@chromium.org (2012-04-27)

http://trac.webkit.org/changeset/115400

### in...@chromium.org (2012-05-01)

We should ignore r115400 and use this new patch - http://trac.webkit.org/changeset/115702

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### in...@chromium.org (2012-05-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-16)

Fixing milestone.

### sc...@gmail.com (2012-05-22)

Already in M20, no need for merge.

### sc...@gmail.com (2012-06-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

### sh...@chromium.org (2016-06-14)

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

### aw...@chromium.org (2016-11-29)

Nice one, the panel decided to award $1,000 for this!

### aw...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-06-08)

The reward for this report is being donated to the Against Malaria Foundation :-)

### is...@google.com (2018-06-08)

This issue was migrated from crbug.com/chromium/122925?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI, UI>Browser>Autofill]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056548)*
