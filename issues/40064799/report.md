# Security: Chrome for Android Bypassing SOP for Local Files By Symlinks

| Field | Value |
|-------|-------|
| **Issue ID** | [40064799](https://issues.chromium.org/issues/40064799) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Platforms** | Android |
| **Reporter** | we...@gmail.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2012-08-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome for Android seems to forbid a local file to read another  

file, except for the originating file itself (\*). However it is  

possible to circumvent the restriction by a trick using symlink.

(\*) <http://code.google.com/p/chromium/issues/detail?id=37586>

This issue enables malicious Android apps to steal Chrome's  

private files such as Cookie file, bookmark file, and so on.

As an example, steps to steal Chrome's Cookie file are described  

below:

1. An attacker's app creates a malicious HTML file, and makes  
   
   Chrome load its URL with file: scheme. The malicious HTML  
   
   contains JavaScript code which, a few seconds later, tries  
   
   to read the content of the same URL with the malicious HTML  
   
   itself by XHR.
   
   <body>
   <u>Wait a few seconds.</u>
   <script>
   function doitjs() {
   var xhr = new XMLHttpRequest;
   xhr.onload = function() {
   alert(xhr.responseText);
   };
   xhr.open('GET', document.URL);
   xhr.send(null);
   }
   setTimeout(doitjs, 8000);
   </script>
   </body>
2. Before XHR fires, the attacker's app replaces the malicious  
   
   HTML file with a symlink pointing to Chrome's Cookie file.
3. When XHR fires, Chrome follows the symlink and provides the  
   
   content of the Chrome's Cookie file to the malicious HTML.

**VERSION**  

Chrome Version: Chrome for Android v18.0.1025123  

Operating System: confirmed on Android 4.0.4 (Samsung Galaxy Nexus)

**REPRODUCTION CASE**  

A sample code of a malicious Android app is attached.

NOTE  

This issue was initially reported to [security@google.com](mailto:security@google.com) on Aug. 11  

2012, but recently I heard from Google security team that the issue  

might not be filed in Chromium bug database. So now I re-submit  

the issue here which should be a legitimate place for reporting  

Chrome bugs.

This issue is a bit related to issue #141889 in terms of using  

symlink. So, like issue #141889, the issue described in this  

report might be already fixed (but unreleased).

## Attachments

- [poc3.txt](attachments/poc3.txt) (text/x-c++; charset=us-ascii, 2.6 KB)

## Timeline

### pa...@google.com (2012-08-27)

Thanks for reporting this, Takeshi!

Assigning to myself to make sure it's resolved. If not, I'll open it up to klobag and srikanth for assignment to whoever the right person is. Expect to see an update later on today.

### pa...@google.com (2012-08-27)

Thanks for reporting this, Takeshi!

Assigning to myself to make sure it's resolved. If not, I'll open it up to klobag and srikanth for assignment to whoever the right person is. Expect to see an update later on today.

### pa...@google.com (2012-08-27)

As of Chrome for Android 18.0.1025289, this issue is resolved. Chrome cannot load HTML_PATH (/data/data + MY_PKG + ...) due to net::ERR_ACCESS_DENIED. An earlier patch by Nilesh, to fix http://code.google.com/p/chromium/issues/detail?id=141889, resolved a whole class of file access attacks.

On an earlier version, 18.0.1025.166 (Official Build 143067), the exploit works perfectly as expected, so I am confident the fix is good. The fixed version should be out soon (early September, they say).

### pa...@chromium.org (2012-09-11)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-09-12)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-09-13)

Another $500 for Takeshi. Thanks for your good work!

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

Payment in system as part of $2500 batch

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

### pa...@google.com (2013-10-04)

+dfalcantara FYI

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

This issue was migrated from crbug.com/chromium/144866?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064799)*
