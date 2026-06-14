# Referrer Policy bypass using Navigation Timing API

| Field | Value |
|-------|-------|
| **Issue ID** | [40089983](https://issues.chromium.org/issues/40089983) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>PerformanceAPIs>NavigationTiming |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | np...@chromium.org |
| **Created** | 2017-12-23 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36

Steps to reproduce the problem:
1. Go to https://vuln.shhnjk.com/noref_nav.html

What is the expected behavior?
Referrer is not leaked.

What went wrong?
Referrer is indeed not leaked, but Navigation Timing API holds previous URL when redirected, which defeats Referrer Policy.

Did this work before? N/A 

Chrome version: 63.0.3239.108  Channel: stable
OS Version: OS X 10.13.2
Flash Version:

## Timeline

### el...@chromium.org (2017-12-23)

Interesting, thanks for the report. 

[Monorail components: Blink>PerformanceAPIs>NavigationTiming]

### el...@chromium.org (2017-12-25)

[Empty comment from Monorail migration]

### s....@gmail.com (2017-12-29)

Real world example:
Login to flickr (login.yahoo.com has "Referrer Policy: origin-when-cross-origin"), and then type following to the console.

>document.referrer
"https://login.yahoo.com/"

>performance.getEntriesByType("navigation")[0].toJSON().name
"https://login.yahoo.com/account/challenge/password?done=https%3A%2F%2Fapi.login.yahoo.com%2Foauth2%2Frequest_auth%3Fclient_id%3Ddj0yJmk9NTJmMkVmOFo3RUVmJmQ9WVdrOVdXeGhVMWx3TjJFbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD01OA--%26redirect_uri%3Dhttps%253A%252F%252Fwww.flickr.com%252Fsignin%252Fyahoo%252Foauth%252F%253Fredir%253Dhttps%25253A%25252F%25252Fwww.flickr.com%25252F%26response_type%3Dcode%26scope%3Dopenid%252Csdpp-w%26nonce%3Dc89cbe1f1b[reducted]caeb85fe7d9%26.scrumb%3D0&src=oauth2&crumb=Vc9W[reducted]n8&redirect_uri=https%3A%2F%2Fwww.flickr.com%2Fsignin%2Fyahoo%2Foauth%2F%3Fredir%3Dhttps%253A%252F%252Fwww.flickr.com%252F&authMechanism=primary&display=login&yid=[reducted]&sessionIndex=QQ--&acrumb=zDP[reducted]YZ"

And Navigation Timing API leak has some more strength.
1. It can contain hashes.
2. Redirect status code URL can be retained.

PoC without Referrer Policy
https://test.shhnjk.com/location.php?url=//shhnjk.com/#test

>document.referrer //referrer doesn't catch redirect URL
""

>performance.getEntriesByType("navigation")[0].toJSON().name
"https://test.shhnjk.com/location.php?url=//shhnjk.com/#test"


I think this is Medium, per https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md ("A bug that allows an attacker to reliably read or infer browsing history").

### el...@chromium.org (2018-01-04)

Reproduction confirmed in M63 to M65. 

In terms of severity, the Guidelines around allowing the "attacker to reliably read or infer browsing history" might be better stated as "allowing the attacker to reliably read or infer browsing history beyond what is normally exposed by the web platform." Because referrers are, by default, sent from HTTPS sites to HTTPS sites, the only scenarios impacted by this are those where the site is using Referrer Policy to disable the default behavior.

### s....@gmail.com (2018-01-04)

>Because referrers are, by default, sent from HTTPS sites to HTTPS sites, the
>only scenarios impacted by this are those where the site is using Referrer
>Policy to disable the default behavior.

This is totally different from referrer, so it will leak previous URL even if redirect is from HTTPS to HTTP.

PoC
https://test.shhnjk.com/location.php?url=http://shhnjk.com/#test

>performance.getEntriesByType("navigation")[0].toJSON().name
"https://test.shhnjk.com/location.php?url=//shhnjk.com/#test"


### s....@gmail.com (2018-02-20)

Available for 2 months :(

### td...@chromium.org (2018-02-20)

Assigning to tyoshino@ for triage.

### sh...@chromium.org (2018-02-20)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-02-20)

Sorry for the delay, OP.

I'm bumping this up to Severity Medium here; exposure of the URL from HTTPS to HTTP contexts is bad and exposure of the URL Fragment certainly seems very bad (due to the risk of token leaks, etc).

### sh...@chromium.org (2018-02-21)

tyoshino: Uh oh! This issue still open and hasn't been updated in the last 60 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-02-21)

[Empty comment from Monorail migration]

### td...@chromium.org (2018-03-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-07)

tyoshino: Uh oh! This issue still open and hasn't been updated in the last 74 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### td...@chromium.org (2018-03-07)

Assigning to kinuko@ for triage.

### ki...@chromium.org (2018-03-26)

In PerformanceNavigationTiming we initialize PerformanceResourceTiming with ResourceTimingInfo::InitialURL(), while we probably need to set the final response URL.

 https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/timing/PerformanceNavigationTiming.cpp?sq=package:chromium&l=24

### td...@chromium.org (2018-03-26)

Thanks for the details.

npm@ will be back shortly, assigning to him.

### np...@chromium.org (2018-04-03)

Yes, that makes sense. I think there is an easy fix for this. Just to be clear, for the example using https://test.shhnjk.com/location.php?url=//shhnjk.com/#test the output of performance.getEntriesByType("navigation")[0].toJSON().name should be 'https://shhnjk.com/#test', right?

### np...@chromium.org (2018-04-04)

Hmm actually my change breaks the resource-timing layout tests because the navigation and resource timing URLs are calculated in the same place. The ResourceTiming spec [1] says that the |name| is the URL from the resource request, even if the fetch causes a redirect. And in the NavigationTiming spec [2] the |name| is computed in step 11 but updated if the redirect occurs. So they are supposed to calculate |name| differently. Ilya, can you confirm this?  

[1] https://w3c.github.io/resource-timing/#sec-performanceresourcetiming
[2] https://w3c.github.io/navigation-timing/#processing-model

### np...@chromium.org (2018-04-04)

I suspect this will pass the bots because there's no tests for the |name| of navigation timing.
https://chromium-review.googlesource.com/c/chromium/src/+/996579

### ig...@chromium.org (2018-04-05)

> Hmm actually my change breaks the resource-timing layout tests because the navigation and resource timing URLs are calculated in the same place. The ResourceTiming spec [1] says that the |name| is the URL from the resource request, even if the fetch causes a redirect. And in the NavigationTiming spec [2] the |name| is computed in step 11 but updated if the redirect occurs. So they are supposed to calculate |name| differently. Ilya, can you confirm this? 

Yes, I believe that's correct. The difference here is that in NavTiming we don't want to leak the previous URL that led to the current page. In RT, the site knows the original URL and needs to lookup the timing based on that, not on the post-redirect URL (which it doesn't know).. perhaps there should be a "final url" field, but that's a separate discussion.

As such, current fix fixes one thing but breaks another. :(

### np...@chromium.org (2018-04-05)

Per my CL in #19 we can set the response Url just for PerformanceNavigationTiming, which won't affect ResourceTiming. I'll just need to add a test for the |name| attribute of navigation.

### bu...@chromium.org (2018-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/87e204e0aaf7445afbd0d50af6849d857517ae70

commit 87e204e0aaf7445afbd0d50af6849d857517ae70
Author: Nicolas Pena <npm@chromium.org>
Date: Fri Apr 06 14:46:02 2018

Fix the |name| of PerformanceNavigationTiming

Previously, the |name| of a PerformanceNavigationTiming entry was the initial
URL (the request URL). After this CL, it is the response URL, so for example
a url of the form 'redirect?location=newLoc' will have 'newLoc' as the |name|.

Bug: 797465
Change-Id: Icab53ad8027d066422562c82bcf0354c264fea40
Reviewed-on: https://chromium-review.googlesource.com/996579
Reviewed-by: Yoav Weiss <yoav@yoav.ws>
Commit-Queue: Nicolás Peña Moreno <npm@chromium.org>
Cr-Commit-Position: refs/heads/master@{#548773}
[modify] https://crrev.com/87e204e0aaf7445afbd0d50af6849d857517ae70/third_party/WebKit/LayoutTests/external/wpt/navigation-timing/nav2_test_redirect_server.html
[modify] https://crrev.com/87e204e0aaf7445afbd0d50af6849d857517ae70/third_party/WebKit/Source/core/timing/PerformanceNavigationTiming.cpp


### np...@chromium.org (2018-04-09)

Marking as Fixed per the test in #5

### sh...@chromium.org (2018-04-10)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-16)

Thanks for the report! The VRP panel decided to award $500 for this. Cheers!

### s....@gmail.com (2018-04-16)

Thanks awhalley@!
I would love to hear your comment on https://bugs.chromium.org/p/chromium/issues/detail?id=821640#c11 if possible.

Thanks!

### aw...@chromium.org (2018-04-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### np...@chromium.org (2018-06-08)

Looks like adding the milestone prompts the bot to request a merge even if it is not needed. This is already in M67.

### np...@chromium.org (2018-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/797465?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089983)*
