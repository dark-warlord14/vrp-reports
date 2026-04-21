# CSP frame-src bypass using: window.open + javascript-url + about:srcdoc + doubly-nested-iframe.

| Field | Value |
|-------|-------|
| **Issue ID** | [40053051](https://issues.chromium.org/issues/40053051) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | dd...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2020-08-11 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36

Steps to reproduce the problem:
1.use `sudo php -S 0.0.0.0:80` to start a web server, and put the bypass-default-src.html and bypass-script-src.html into the web root directory
2.open http://127.0.0.1/bypass-default-src.html and http://127.0.0.1/bypass-script-src.html in your chrome
3.you will see `default-src 'self'` and `script-src 'self'` have been bypassed

What is the expected behavior?
bypass-default-src.html can not load https://xlab.tencent.com
bypass-script-src.html can not load http://d1iv3.me/test.js

What went wrong?
CSP inheritance mechanism error

Did this work before? N/A 

Chrome version: 84.0.4147.125  Channel: stable
OS Version: OS X 10.15.6
Flash Version:

## Attachments

- [bypass-default-src.html](attachments/bypass-default-src.html) (text/plain, 269 B)
- [bypass-script-src.html](attachments/bypass-script-src.html) (text/plain, 262 B)
- [unsafe-inline.html](attachments/unsafe-inline.html) (text/plain, 238 B)
- [bypass-default-src-none.html](attachments/bypass-default-src-none.html) (text/plain, 269 B)
- [Screenshot from 2020-08-17 18-14-40.png](attachments/Screenshot from 2020-08-17 18-14-40.png) (image/png, 221.5 KB)
- [chrome_canary_87.png](attachments/chrome_canary_87.png) (image/png, 82.1 KB)

## Timeline

### dd...@gmail.com (2020-08-11)

what's more object-src, child-src, img-src related policies can also be bypassed, here we just use default-src and script-src as examples

### va...@chromium.org (2020-08-13)

It appears to me that this is not a bug, it is working as intended.

The description of 'unsafe-inline' states:
Allows the use of inline resources, such as inline <script> elements, javascript: URLs, inline event handlers, and inline <style> elements.

Both POCs here rely on the use of javascript: to load remote resources.

Assigning to mkwst@ to confirm. Adding Security_Severity-Low out of an abundance of caution.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### va...@chromium.org (2020-08-13)

[Empty comment from Monorail migration]

### dd...@gmail.com (2020-08-13)

I need to emphasize that the CSPs that are bypassed in the POC are default-src and script-src, not unsafe-inline. 
The iframe src and script src in the iframe srcdoc needed to follow the default-src'self' and script-src'self', but in this issue they didn't.

If you don’t know what went wrong, you can refer to the behavior of Safari and Firefox.

What's more, i think this issue should be **Security_Severity-Medium**

### dd...@gmail.com (2020-08-13)

And as you said, "Both POCs here rely on the use of javascript: to load remote resources.", and javascript: can be executed because of unsafe-line.

I can give you an example (unsafe-inline.html) to explain why unsafe inline javascript cannot load remote resources when default-src 'none' is enabled. 

You can compare `bypass-default-src-none.html` and `unsafe-inline.html` in the attachments


### mk...@chromium.org (2020-08-13)

Does this reproduce in Canary?

arthursonzogni@ has made some recent changes in this area.

### dd...@gmail.com (2020-08-13)

I can reproduce this issue in Canary. The version of my Canary: 86.0.4231.0 canary (x86_64)

### dd...@gmail.com (2020-08-17)

any progress?

### ar...@chromium.org (2020-08-17)

I confirm. I tried on M84 and M86.
I got two different results, both wrong.

I also tried variations:
1) default-src 'self'
2) default-src 'none'
3) frame-src 'self'
4) frame-src 'none'

but got the same wrong results. It seems the frame-src directive isn't enforced.
I am guessing the sequence: window.open + execute javascript-URL + srcdoc + loading a doubly nested iframe, was enough to confuse the implementation somehow.

I won't have time before the M86 branch cut to investigate more. We need to take another look next week.

### dd...@gmail.com (2020-09-01)

any progress? I have tested the POC on Canary 87.0.4250.0 (which is the latest version), it still works (bypassed the CSP successfully)



### ar...@chromium.org (2020-09-02)

pmeuleman@ and antoniosartori@ are going to improve how a given policy, like
CSP, are inherited across documents/navigations. (PolicyContainer)

There are many CSP bugs around inheritance below:
- https://crbug.com/chromium/1117687
- https://crbug.com/chromium/1115628
- https://crbug.com/chromium/1115298
- https://crbug.com/chromium/1115045
- https://crbug.com/chromium/1109167
- https://crbug.com/chromium/971231
- https://crbug.com/chromium/957606

I believe their future work might fix several issues in this list.

### dd...@gmail.com (2020-10-12)

Hi, any progress?

### ar...@chromium.org (2020-10-13)

> Hi, any progress?

A lot of progress.
antoniosartori@ and pmeuleman@ are working on "defining" properly how things in general are inherited toward new documents with a local scheme (about:, data:, javascript:, ...)

This will fix all the issues with CSP. Moreover this isn't limited to CSP as it will also contains several other properties.
Doing the right thing takes times. This won't be fixed in weeks, but months.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-04)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-04)

This has been fixed by this CL https://chromium-review.googlesource.com/c/chromium/src/+/2667858

Regression test here https://chromium-review.googlesource.com/c/chromium/src/+/2725520

### [Deleted User] (2021-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-04)

[Empty comment from Monorail migration]

### dd...@gmail.com (2021-03-05)

Should this issue be Security_Severity-Medium?

### gi...@appspot.gserviceaccount.com (2021-03-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d2cb713d42b11273c00e57fcf91b25022b387abb

commit d2cb713d42b11273c00e57fcf91b25022b387abb
Author: Antonio Sartori <antoniosartori@chromium.org>
Date: Fri Mar 05 10:36:57 2021

CSP: Add WPT for nested inheritance

This CL adds a Web Platform Test for an edge case of multiple
Content-Security-Policy inheritance for a nested iframe.

Bug: 1115045,1149272
Change-Id: I492408b8c0f7a3e6cd7dc7e74769c9c8876a34ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2725520
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#860179}

[add] https://crrev.com/d2cb713d42b11273c00e57fcf91b25022b387abb/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/javascript-url-srcdoc-cross-origin-iframe-inheritance.html
[add] https://crrev.com/d2cb713d42b11273c00e57fcf91b25022b387abb/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/support/javascript-url-srcdoc-cross-origin-iframe-inheritance-helper.sub.html
[add] https://crrev.com/d2cb713d42b11273c00e57fcf91b25022b387abb/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/support/postmessage-top.html


### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-31)

Congratulations, dddliv3@! The VRP Panel has decided to award you $3000 for this report. A member of our finance team will be in touch soon to arrange payment. In the meantime, please let me know how you would like to be credited for this issue (name/handle you'd like us to use) in the release notes. Nice work! 


### dd...@gmail.com (2021-04-01)

Thanks for the bounty!

My credit info: Tianze Ding (@D1iv3) of Tencent Security Xuanwu Lab

### am...@google.com (2021-04-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-06-24)

This issue was migrated from crbug.com/chromium/1115045?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053051)*
