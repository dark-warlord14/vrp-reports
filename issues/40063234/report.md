# Security: Cookie theft from Chrome by malicious Android app

| Field | Value |
|-------|-------|
| **Issue ID** | [40063234](https://issues.chromium.org/issues/40063234) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Platforms** | Android |
| **Reporter** | pa...@google.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2012-08-10 |
| **Bounty** | $500.00 |

## Description

This is a Chrome tracking bug for internal bug b/6949780, reported by Takeshi TERADA <websec02.g02@gmail.com>. Thanks again, Takeshi! As before, we'll consider this bug for our vulnerability rewards program.

## Timeline

### sc...@gmail.com (2012-08-20)

@websec02.g02: thanks for your help! We'd like to offer you a $500 Chromium Security Reward.

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

### we...@gmail.com (2012-08-22)

Thanks @scarybeast and all.

I have a question related to this issue.

I have reported four issues that can be used for cookie theft.
Which of the four issues is this issue (#141889) related to?

Summaries of four issues are:

1.Chrome for Android JavaScript Injection
  Malicious apps can inject URLs with javascript: scheme into
  arbitrary Web pages. It can be used for cookie theft.

2.Chrome for Android Information Disclosure
  Chrome's behavior of automatic downloading can be abused to steal
  both online and local files (including cookie file) by malicious
  apps.

3.Chrome for Android Cookie Leakage
  Symbolic links can be used to spoof content-type of local files,
  so that malicious apps can force Chrome to render the cookie file
  as HTML. It results in cookie theft by malicious apps.

4.Subverting Chrome's Same-Origin Policy for Local Contents
  Symbolic links can also be used to spoof the origin of local files.
  It breaks Chrome's SOP for local files and results in cookie theft
  by malicious apps.

I sent these reports by email to security@google.com, which is not
a proper manner for Chrome-related issues.

So the question is, are you conscious of all four issues listed above?
If not, I should file the omitted ones in an appropriate manner.


### kl...@chromium.org (2012-08-22)

I believe all four cased have been addressed in the coming 18.1 release.

### sc...@gmail.com (2012-08-22)

@palmer: Any chance you can help map @websec02.g02 4 issues into Chromium bugs?

### pa...@google.com (2012-08-22)

This bug, filed internally as b/6949780, is #3.

http://code.google.com/p/chromium/issues/detail?id=137532, filed internally as b/6820083, is not among the above 4.

Internally, we have two reports from you about some application called GREE. Seems unrelated, and possibly duplicates? We also have one about Android app widgets.

I have not seen any of the other bugs you mention, unfortunately. However, http://code.google.com/p/chromium/issues/detail?id=138210 (reported by a different person) seems like it might be related to your #2.

So yes, please file the additional 3 bugs in this bug tracker, and I will make sure that we handle them properly. Thank you!

### we...@gmail.com (2012-08-23)

@palmer

Thank you so much for taking your time.
I will file 3 bugs in a proper manner in a few days.


### pa...@google.com (2012-08-23)

No, thank *you*, Takeshi! :) I am sorry your bug reports to security@google.com appear to have been lost. I'll make sure that doesn't happen again.

We are looking forward to more bug reports from you. :)

### pa...@google.com (2012-08-23)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-09-13)

One last chunk of cash for you. :)  We'd love to hear from you again.

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

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### sc...@gmail.com (2012-10-16)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-01-18)

Restrict-View-EditIssue is preferred since it allows anyone who can edit an issue (committers and contributors) to view the bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

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

This issue was migrated from crbug.com/chromium/141889?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063234)*
