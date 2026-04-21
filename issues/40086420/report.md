# Security: Content-Security-Policy reporting leaks the URL fragment

| Field | Value |
|-------|-------|
| **Issue ID** | [40086420](https://issues.chromium.org/issues/40086420) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | co...@linkmauve.fr |
| **Assignee** | mk...@chromium.org |
| **Created** | 2017-01-05 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Adding a Content-Security-Policy header containing a report-uri can lead to the leak of the current URL fragment to the web server, even though it should never be sent according to <https://www.w3.org/TR/CSP/#deprecated-serialize-violation>

This turns an otherwise active attack (serving an evil JavaScript file to the user to make it leak the fragment) into a passive and deferred attack, using a mechanism otherwise made to improve the security.

**VERSION**  

Chrome Version: 55.0.2883.87 + stable  

Operating System: Android 7.1.1 as well as ArchLinux current

**REPRODUCTION CASE**  

A testcase based on nginx, 0bin and a Python script is attached, with a README included containing the setup steps. 0bin being a pastebin software doing client-side encryption and putting the AES key in the fragment for easy sharing.

I am hosting this setup at [1], you can use it as follows:

- Go to [2] using Chromium (affected) and Firefox (unaffected).
- List all of the previously-reported violations at [3].
- See how the document-uri differs between those, with Chromium leaking the AES key in the fragment.

[1] <https://zerobin.linkmauve.fr/>  

[2] <https://zerobin.linkmauve.fr/paste/o8Z-9Pnv#8vanDKS8wskq+hG-si9hVhBWj6OY1BE7MS1Rd+9cuB1>  

[3] <https://zerobin.linkmauve.fr/report-csp-violation>

## Timeline

### el...@chromium.org (2017-01-06)

Confirmed with Chrome 57.2973

[Monorail components: Blink>SecurityFeature]

### el...@chromium.org (2017-01-06)

Looks like it just needs a simple tweak to the three URIs used by ContentSecurityPolicy::postViolationReport()?

https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/frame/csp/ContentSecurityPolicy.cpp?q=document-uri&sq=package:chromium&l=1163

### mm...@chromium.org (2017-01-09)

Mike, could you please help to find an owner?

### mk...@chromium.org (2017-01-09)

Yeah, we're calling `getString()` in a few places we should be calling `strippedForUseAsReferrer()`. I'll fix it.

### sh...@chromium.org (2017-01-09)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-03-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fea16c8b60ff3d0756d5eb392394963b647bc41a

commit fea16c8b60ff3d0756d5eb392394963b647bc41a
Author: mkwst <mkwst@chromium.org>
Date: Mon Mar 20 12:42:10 2017

CSP: Strip the fragment from reported URLs.

We should have been stripping the fragment from the URL we report for
CSP violations, but we weren't. Now we are, by running the URLs through
`stripURLForUseInReport()`, which implements the stripping algorithm
from CSP2: https://www.w3.org/TR/CSP2/#strip-uri-for-reporting

Eventually, we will migrate more completely to the CSP3 world that
doesn't require such detailed stripping, as it exposes less data to the
reports, but we're not there yet.

BUG=678776

Review-Url: https://codereview.chromium.org/2619783002
Cr-Commit-Position: refs/heads/master@{#458045}

[add] https://crrev.com/fea16c8b60ff3d0756d5eb392394963b647bc41a/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/report-strips-fragment.html
[modify] https://crrev.com/fea16c8b60ff3d0756d5eb392394963b647bc41a/third_party/WebKit/Source/core/frame/csp/ContentSecurityPolicy.cpp


### aw...@google.com (2017-03-31)

mkwst@ - are you expecting to make any more changes here, or can this be marked as fixed? Thanks!

### me...@chromium.org (2017-04-05)

Adding koczkatamas@ who reported this separately in https://crbug.com/chromium/700035.

### el...@chromium.org (2017-04-19)

I believe this can be marked as fixed.  

commit fea16c8b60ff3d0756d5eb392394963b647bc41a was:
  initially in 59.0.3047.0

Unfortunately, the repro from #0 appears to have become unavailable (404 for all resources).

### ko...@gmail.com (2017-04-19)

I can confirm that the fragment is not leaked in Chrome 59 anymore. ( Based on my PoC attached to https://bugs.chromium.org/p/chromium/issues/detail?id=700035 )

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-28)

Your change meets the bar and is auto-approved for M59. Please go ahead and merge the CL to branch 3071 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-28)

Congratulations! The VRP panel decided to award $2,000 for this report.  A member of our finance team will be in touch shortly to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-04-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-05-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2017-05-05)

As noted in c#11, this originally landed in M59, so no merge is needed.

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-21)

collabora@linkmauve.fr - Please claim your reward by April 30 2020 otherwise it will be donated to charity.

### co...@linkmauve.fr (2020-04-28)

Hi, I haven’t been able to claim it yet because I don’t work yet, I am an individual so I don’t have a company to use the VAT number for.  I have sent an email to p2p-vrp about this issue and I’m now waiting for their answer.

Do you think I need to create a company to claim this reward?

### na...@google.com (2020-05-05)

Hi collabora@linkmauve.fr  - I can follow up with the p2p-vrp team and see what is going on. 

### ad...@google.com (2020-10-23)

collabora@linkmauve.fr - our finance team report difficulty getting in touch with you. Could you check that you haven't received e-mails from them (since May) which have got trapped in a spam folder or similar? We will be donating this reward to charity if we don't hear from you within a week. Thanks!

### co...@linkmauve.fr (2020-10-29)

Ugh, again… I’ll sort this asap, and sorry for the inconvenience!

### ad...@chromium.org (2020-10-29)

OK great. Thanks!

### ad...@google.com (2020-12-11)

collabora@linkmauve.fr - hi. Once again our finance team are having trouble. Do you have an alternative e-mail where they can get in touch with you? Feel free to e-mail me at adetaylor@chromium.org, and adetaylor@google.com - probably best use both just in case something is indeed getting trapped in a spam filter. Please also comment on here when you've e-mailed.

### ad...@google.com (2020-12-14)

collabora@linkmauve.fr - we'll donate the reward to charity at the end of this week.

### am...@google.com (2021-01-19)

Reward has been donated to charity 

### co...@linkmauve.fr (2021-01-19)

Err, I did the thing with Embark and got a notification that it was complete last Thursday (14th of January), I was expecting things to go smooth from then on. :s

Was there something more I had to do?

### ad...@chromium.org (2021-01-19)

I'm very sorry collabora@linkmauve.fr. Our rules are to donate to charity after a year of the reward being unclaimed. We obviously bent that rule - it's been nearly four years of difficult communication - but we couldn't extend indefinitely. I continued to get messages from our finance team that you were unresponsive even in the past couple of weeks, and with your lack of reply to https://crbug.com/chromium/678776#c34 and https://crbug.com/chromium/678776#c35 I decided that we needed to finally close down this case.

The only good news I can give you is that we double up charity rewards, so effectively you've donated $4000 to charity.

### am...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### is...@google.com (2021-01-21)

This issue was migrated from crbug.com/chromium/678776?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/700035]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086420)*
