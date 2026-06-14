# Information and credential disclosure by file:// URLs (Android)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061639](https://issues.chromium.org/issues/40061639) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Platforms** | Android |
| **Reporter** | ch...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-07-20 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Hi again. I found this bug more risky than UXSS, here is details. Google Chrome allows user to open local files through 'file://' wrapper. Malicious application can start Google Chrome with data set to 'file:///some/local/file' and if this file is binary, Chrome immediately download (really copy) it to Download folder on the SD Card. So I found, that possible to open cookies file (/data/data/com.android.chrome/app\_chrome/Default/Cookies) and start Chrome like this  

shell@android:/ $ am start -n com.android.chrome/com.android.chrome.Main -d 'file:///data/data/com.android.chrome/app\_chrome/Default/Cookies'  

This Cookies file unreadable by malicious application, but can be read by Google Chrome. After browser start, Cookies file will be copied to /sdcard/Downloads/Cookies.bin and can be readable by every application on the system. Also, it's possible to copy another files, such as History, Local Storage, Bookmarks, Cache, etc. Example:

shell@android:/sdcard/Download $ ls -la  

-rw-rw-r-- root sdcard\_rw 86016 2012-07-20 00:29 Cookies.bin  

-rw-rw-r-- root sdcard\_rw 102400 2012-07-20 00:58 History.bin

I've tested it on my Galaxy Nexus  

FIX: probably the best way - ask user if he wants to download files or not, and don't download it automatically.

**VERSION**  

Chrome Version: 18.0.1025123 + stable  

Operating System: Android 4.1 and below

**REPRODUCTION CASE**  

am start -n com.android.chrome/com.android.chrome.Main -d 'file:///data/data/com.android.chrome/app\_chrome/Default/Cookies'

Best Regards,  

Artem Chaykin

## Timeline

### pa...@chromium.org (2012-07-20)

Thanks again, Artem!

Assigning to Grace so she can route it to the right person or handle it. Potential solutions:

* Prompt before downloading
* Open only files underneath file:///sdcard (these are the only files intended to be public on the device)
* Whitelist of downloadable file types, not including "binary"
* others?

### pa...@chromium.org (2012-07-20)

[Empty comment from Monorail migration]

### kl...@chromium.org (2012-07-20)

I think we want to restrict to file:///sdcard/.

Dan, please take a look at this. Thanks.

### [Deleted User] (2012-07-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-02)

Please do read Mark's email titled "Code Yellow: Security Bug Backlog" on chrome-team mailing list.

### [Deleted User] (2012-08-04)

This issue is fixed by: https://gerrit-int.chromium.org/#change,22996 .
We have disabled all binary file downloads for the file:// scheme.


### sc...@gmail.com (2012-08-20)

@chaykin.artem: thanks for the report! This qualifies for a $500 Chromium Security Reward.

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

### pa...@google.com (2012-08-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-27)

[Empty comment from Monorail migration]

### pa...@google.com (2012-08-27)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-09-12)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-09-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### sc...@gmail.com (2012-10-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-19)

Payment sent for wire as part of $1000 batch

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

### pa...@google.com (2013-10-04)

+dfalcantara FYI

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/138210?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/144820]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061639)*
