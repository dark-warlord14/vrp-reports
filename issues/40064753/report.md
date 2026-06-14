# Security: UXSS via com.android.browser.application_id Intent extra

| Field | Value |
|-------|-------|
| **Issue ID** | [40064753](https://issues.chromium.org/issues/40064753) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Platforms** | Android |
| **Reporter** | we...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2012-08-25 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

By sending a crafted intent to Chrome for Android, malicious Android  

apps can inject javascript: URIs into arbitrary Web pages loaded  

in Chrome. Injected javascript works in the context of the target  

Web page's domain, not a blank domain. So it can be used for Cookie  

theft or so. Such kind of vulns is often called Cross-Application  

Scripting.

**VERSION**  

Chrome Version: Chrome for Android v18.0.1025123  

Operating System: confirmed on Android 4.0.4 (Samsung Galaxy Nexus)

**REPRODUCTION CASE**  

A sample code of a malicious Android app is attached.

NOTE  

This issue was initially repoted to [security@google.com](mailto:security@google.com) on Jul. 7  

2012, but recently I heard from Google security team that the issue  

might not be filed in Chromium bug database. So now I re-submit  

the issue here which should be a legitimate place for reporting  

Chrome bugs.

## Attachments

- [poc1.txt](attachments/poc1.txt) (text/x-java; charset=us-ascii, 1.4 KB)

## Timeline

### js...@chromium.org (2012-08-26)

@palmer - I believe these are fixed on their trunk but you'd know best.

### pa...@google.com (2012-08-27)

No, this is a new bug that I don't think we have seen or dealt with yet. Thanks again Takeshi! I'm working on setting up and Android dev environment on my new machine so I can repro it, and I'll fill in the rest of the tags once I have done so.

### pa...@chromium.org (2012-08-27)

I have reproduced this. Nice! Updating the summary line.

So the next question is, what are the potential fixes? Here are some random ideas:

* Do we need this Intent extra? If not, can we get rid of it?

* Require that new URLs received via Intent with the com.android.browser.application_id Intent extra have the same origin as the current URL in the tab; if the origins don't match, start a new tab or reject/ignore the Intent.

* Ignore javascript: URIs received via Intents.

### pa...@chromium.org (2012-08-27)

[Empty comment from Monorail migration]

### [Deleted User] (2012-08-29)

Pri-2 / SecSeverity-Medium - so not making it into M18.1. We will consider for M18.2 

### kl...@chromium.org (2012-08-29)

Chris, need a little detail. How does this work? Does it because we open an intent in the same tab due to application_id match?

### pa...@chromium.org (2012-08-29)

Yes. The meat of the problem seems to be this line from Takeshi's poc1.txt (attached, see above):

    // Need a trick to prevent Chrome from loading the new URL in a new tab
    intent2.putExtra("com.android.browser.application_id", "com.android.chrome");



### ni...@chromium.org (2012-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2012-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2012-09-04)

[Empty comment from Monorail migration]

### ni...@chromium.org (2012-09-04)

Update: https://gerrit-int.chromium.org/#/c/24519/ submitted on master.
m18 CL: https://gerrit-int.chromium.org/#/c/24726/

### [Deleted User] (2012-09-06)

[Empty comment from Monorail migration]

### ni...@chromium.org (2012-09-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-09-12)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-09-13)

Thank you, Takeshi! This report qualifies for a $500 Chrome security reward.

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

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-10-03)

This issue was migrated from crbug.com/chromium/144813?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064753)*
