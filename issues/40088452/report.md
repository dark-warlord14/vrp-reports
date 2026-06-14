# Security: CSP not inherited after navigation to JavaScript scheme uri

| Field | Value |
|-------|-------|
| **Issue ID** | [40088452](https://issues.chromium.org/issues/40088452) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **CVE IDs** | CVE-2017-5033 |
| **Reporter** | ma...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2017-07-24 |
| **Bounty** | $1,000.00 |

## Description

AFFECTED PRODUCTS
--------------------
chrome 59.0.3071.115


DESCRIPTION
--------------------
Blink in Google Chrome prior to 59.0.3071.115 for Mac, Windows, and Linux and 57.0.2987.108 for Android failed to correctly propagate CSP restrictions to javascript scheme pages, which allowed a remote attacker to bypass content security policy via a crafted HTML page.

PoC
--------------------
poc.html,which enable the content security policy,please put it on the local httpserver
and set a cookie for test
this attacks shows that your cookie is sent to a remote server bypass the content security policy
http://www.math1as.com/xsslog.txt shows the cookie received

SOLUTION
--------------------
apply CSP to javascript scheme URL


CREDIT
--------------------
This vulnerability was discovered by mathiaswu of <a href="http//xlab.tencent.com/">Tencent's Xuanwu Lab</a>.

REFERENCES
--------------------
this vulnerability and the payloads are refered to overt message on the internet

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 289 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### el...@chromium.org (2017-07-24)

To be clear, you're reporting that a security bug was Fixed in Chrome 59?

This sounds like https://crbug.com/chromium/669086.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### ma...@gmail.com (2017-07-24)

I use the latest chrome version "59.0.3071.115" to review this bug
and my operation system is windows 10
the result shows it was not fixed yet.
And please read the following tips:

1.the attack scenario is shown in my gif image
2.it is similar to CVE-2017-5033 but i use javascript:// to create html
instead of data:// , and my poc.html still works in the latest chrome.

### el...@chromium.org (2017-07-24)

Ah, so instead of "Prior to 59.0.3071.115" this is "Including 59.0.3071.115". The change mentioned in https://crbug.com/chromium/747847#c1 landed in 57.0.2938.0, so this would be a different issue. 

Testing reveals that the same behavior is present in 62.0.3165.0.



### el...@chromium.org (2017-07-24)

Firefox 55b11 blocks the request noting "Content Security Policy: The page’s settings blocked the loading of a resource at http://www.math1as.com/xrecv.php?data=secret (“default-src http://127.0.0.1”)."

Edge 25.10586.672/EdgeHTML13.10586 behaves like Chrome 62.

### ke...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-07-24)

estark@, can you take a look or help route this? Thanks.

### mk...@chromium.org (2017-07-25)

The issue here is that you're actually navigating the document itself. That is, `location.href = 'javascript:...';` has the same effect (as does `location.href = 'blob:...'`, for that matter).

I don't think there's actually anything in the spec to cover this case, but I think I agree with the interpretation Firefox landed on. If we inherit the origin, we ought to inherit the restrictions as well.

Andy, will you have time this week to take this? If not, I'll find time.

### sh...@chromium.org (2017-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-25)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-07)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2017-08-07)

There is a fix for this in the works and it should be submitted withing the next 24h.

### bu...@chromium.org (2017-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0ab2412a104d2f235d7b9fe19d30ef605a410832

commit 0ab2412a104d2f235d7b9fe19d30ef605a410832
Author: Andy Paicu <andypaicu@chromium.org>
Date: Mon Aug 07 16:02:31 2017

Inherit CSP when we inherit the security origin

This prevents attacks that use main window navigation to get out of the
existing csp constraints such as the related bug

Bug: 747847
Change-Id: I1e57b50da17f65d38088205b0a3c7c49ef2ae4d8
Reviewed-on: https://chromium-review.googlesource.com/592027
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#492333}
[add] https://crrev.com/0ab2412a104d2f235d7b9fe19d30ef605a410832/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/navigation/javascript-url-navigation-inherits-csp.html
[add] https://crrev.com/0ab2412a104d2f235d7b9fe19d30ef605a410832/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/navigation/support/test_csp_self_window.sub.html
[add] https://crrev.com/0ab2412a104d2f235d7b9fe19d30ef605a410832/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/navigation/support/test_csp_self_window.sub.html.sub.headers
[modify] https://crrev.com/0ab2412a104d2f235d7b9fe19d30ef605a410832/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/script-src-in-iframe-expected.txt
[modify] https://crrev.com/0ab2412a104d2f235d7b9fe19d30ef605a410832/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/0ab2412a104d2f235d7b9fe19d30ef605a410832/third_party/WebKit/Source/core/dom/Document.h
[modify] https://crrev.com/0ab2412a104d2f235d7b9fe19d30ef605a410832/third_party/WebKit/Source/core/frame/WebLocalFrameImpl.cpp
[modify] https://crrev.com/0ab2412a104d2f235d7b9fe19d30ef605a410832/third_party/WebKit/Source/core/loader/DocumentLoader.cpp
[modify] https://crrev.com/0ab2412a104d2f235d7b9fe19d30ef605a410832/third_party/WebKit/Source/core/loader/DocumentLoader.h


### sh...@chromium.org (2017-08-22)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2017-08-22)

Marking this as fixed for you, Andy. Since the patch isn't terribly complicated, and it's been baking on dev for a week, let's run it by awhalley@ to see if it's something we should try to merge back to beta.

WDYT, awhalley@, et al?

### sh...@chromium.org (2017-08-22)

This bug requires manual review: We are only 13 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-22)

+awhalley@ for M61 merge review.

### ma...@gmail.com (2017-08-23)

[Comment Deleted]

### sh...@chromium.org (2017-08-23)

[Empty comment from Monorail migration]

### ma...@gmail.com (2017-08-23)

I'm sorry but please correct the information to 
"WenXu Wu of Tencent's Xuanwu Lab" 
if you are ready to release a new version chrome,Thank you for fixing this problem.

### aw...@chromium.org (2017-08-24)

govind@ - good for 61

### go...@chromium.org (2017-08-24)

Approving merge to M61 branch 3163 based on https://crbug.com/chromium/747847#c21. Please merge ASAP. Thank you.

### go...@chromium.org (2017-08-24)

Please merge your change to M61 branch 3163 by 4:00 PM PT tomorrow, Friday (08/25) so we can take it in for next week last M61 Beta release. Thank you.

### an...@chromium.org (2017-08-28)

Apologies, it seems I have missed this bug and that action was needed on my side.

I assume by now the cut-off point is missed.

### go...@chromium.org (2017-08-28)

Re #24, pls merge before 11:30 AM PT, Tuesday (08/29) so we can still take it in for this week LAST Beta release. Thank you.

### aw...@chromium.org (2017-08-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cb54da8199ba125d94cfcdd8edec14bef1ce3cf1

commit cb54da8199ba125d94cfcdd8edec14bef1ce3cf1
Author: Andy Paicu <andypaicu@chromium.org>
Date: Tue Aug 29 07:51:29 2017

Inherit CSP when we inherit the security origin

This prevents attacks that use main window navigation to get out of the
existing csp constraints such as the related bug

TBR=andypaicu@chromium.org

(cherry picked from commit 0ab2412a104d2f235d7b9fe19d30ef605a410832)

Bug: 747847
Change-Id: I1e57b50da17f65d38088205b0a3c7c49ef2ae4d8
Reviewed-on: https://chromium-review.googlesource.com/592027
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#492333}
Reviewed-on: https://chromium-review.googlesource.com/640379
Reviewed-by: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/branch-heads/3163@{#966}
Cr-Branched-From: ff259bab28b35d242e10186cd63af7ed404fae0d-refs/heads/master@{#488528}
[add] https://crrev.com/cb54da8199ba125d94cfcdd8edec14bef1ce3cf1/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/navigation/javascript-url-navigation-inherits-csp.html
[add] https://crrev.com/cb54da8199ba125d94cfcdd8edec14bef1ce3cf1/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/navigation/support/test_csp_self_window.sub.html
[add] https://crrev.com/cb54da8199ba125d94cfcdd8edec14bef1ce3cf1/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/navigation/support/test_csp_self_window.sub.html.sub.headers
[modify] https://crrev.com/cb54da8199ba125d94cfcdd8edec14bef1ce3cf1/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/script-src-in-iframe-expected.txt
[modify] https://crrev.com/cb54da8199ba125d94cfcdd8edec14bef1ce3cf1/third_party/WebKit/Source/core/dom/Document.cpp
[modify] https://crrev.com/cb54da8199ba125d94cfcdd8edec14bef1ce3cf1/third_party/WebKit/Source/core/dom/Document.h
[modify] https://crrev.com/cb54da8199ba125d94cfcdd8edec14bef1ce3cf1/third_party/WebKit/Source/core/loader/DocumentLoader.cpp
[modify] https://crrev.com/cb54da8199ba125d94cfcdd8edec14bef1ce3cf1/third_party/WebKit/Source/core/loader/DocumentLoader.h


### aw...@chromium.org (2017-09-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-01)

Nice one! The VRP panel decided to award $1,000 for this report!  A member of our finance team will be in touch to arrange for payment.

### aw...@chromium.org (2017-09-01)

[Empty comment from Monorail migration]

### aw...@google.com (2017-09-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/747847?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088452)*
