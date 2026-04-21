# SameSite cookie bypass via Custom Scheme

| Field | Value |
|-------|-------|
| **Issue ID** | [40091076](https://issues.chromium.org/issues/40091076) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation, Mobile>Intents, UI>Browser>Navigation |
| **Platforms** | Android |
| **Reporter** | s....@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2018-04-11 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
1. Go to https://shhnjk.azurewebsites.net/SameSite.php (Sets SameSite cookie)
2. Go to https://test.shhnjk.com/samecustom.html
3. Click go

What is the expected behavior?
SameSite cookie not sent

What went wrong?
SameSite cookie can be sent using custom scheme (googlechrome://navigate?url=https://shhnjk.azurewebsites.net/SameSite.php)

Did this work before? N/A 

Chrome version: 65.0.3325.181  Channel: stable
OS Version: Android
Flash Version:

## Timeline

### el...@chromium.org (2018-04-11)

There are other places where using this scheme can bypass controls; see e.g.  https://crbug.com/chromium/804054 and https://crbug.com/chromium/822518.

I don't think we should allow navigation to this scheme from within Chrome.



### ca...@chromium.org (2018-04-13)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature Internals>Network>Cookies]

### ca...@chromium.org (2018-04-13)

mrefaat: Assigning this one to you since you have the other googlechrome:// scheme bugs, feel free to reassign if appropriate. 

### ca...@chromium.org (2018-04-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-14)

[Empty comment from Monorail migration]

### mr...@chromium.org (2018-04-19)

I work on Chrome for iOS, we don't use blink so this is bit irrelevant 

### ca...@chromium.org (2018-04-19)

I didn't realize the other googlechrome:// scheme bugs were iOS specific. Assigning this one to mkwst since it's SameSite cookie related. 

### sh...@chromium.org (2018-04-26)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-10)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### ca...@chromium.org (2018-06-07)

Friendly security sheriff ping. Mike: feel free to reassign this one as appropriate.

### do...@chromium.org (2018-07-23)

+andy, do you mind looking at this while mkwst is OOO?

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-10-04)

(Unassigning myself, marking untriaged in preparation to retriage with folks who will do a better job taking care of cookies than I've been able to)

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-12-11)

Misha, could you please help to find an owner here as per c#15? Thanks a lot!

### mm...@chromium.org (2018-12-11)

mmoroz:  This doesn't seem network stack related - the network stack neither knows nor cares what a custom scheme is.

### me...@chromium.org (2018-12-21)

Maks, could you assess what needs to be done?

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-05-23)

Most likely this is also a Sec-Fetch-Site bypass (since AFAIK SameSite cookies and Sec-Fetch-Site both rely on network::ResourceRequest::request_initiator).

[Monorail components: Internals>Sandbox>SiteIsolation]

### lu...@chromium.org (2019-05-31)

RE: https://crbug.com/chromium/831761#c1: elawrence@: I don't think we should allow navigation to this scheme from within Chrome.

I agree - we may want to try filtering out this scheme somehow (via FilterURL / ChildProcessSecurityPolicyImpl::CanRequestURL maybe?).  CC-ing nasko@ who has recently been looking into this kind of filtering for another scheme.

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-07-17)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b96a52adb25cf94380bb3fb32b0295f6419da5d6

commit b96a52adb25cf94380bb3fb32b0295f6419da5d6
Author: Mike West <mkwst@chromium.org>
Date: Wed Jul 24 17:08:50 2019

Disallow navigation to or embedding of `googlechrome://...` URLs.

Bug: 831761
Change-Id: Ibebe1585d06f16a94bc7bdb47c952e3cbefd981c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1705792
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Reviewed-by: Jochen Eisinger <jochen@chromium.org>
Commit-Queue: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#680487}

[modify] https://crrev.com/b96a52adb25cf94380bb3fb32b0295f6419da5d6/content/browser/child_process_security_policy_impl.cc
[modify] https://crrev.com/b96a52adb25cf94380bb3fb32b0295f6419da5d6/content/browser/child_process_security_policy_unittest.cc
[modify] https://crrev.com/b96a52adb25cf94380bb3fb32b0295f6419da5d6/content/browser/navigation_browsertest.cc
[modify] https://crrev.com/b96a52adb25cf94380bb3fb32b0295f6419da5d6/content/public/common/url_constants.cc
[modify] https://crrev.com/b96a52adb25cf94380bb3fb32b0295f6419da5d6/content/public/common/url_constants.h
[modify] https://crrev.com/b96a52adb25cf94380bb3fb32b0295f6419da5d6/content/renderer/render_thread_impl.cc
[modify] https://crrev.com/b96a52adb25cf94380bb3fb32b0295f6419da5d6/content/test/data/simple_links.html


### lu...@chromium.org (2019-07-24)

Thanks mkwst@!  Is passing a googlechrome://navigate?url=... URL via FrameHostMsg_DownloadUrl also a possible attack vector?  

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### jd...@chromium.org (2020-05-26)

mkwst@: ping re: https://crbug.com/chromium/831761#c30.

This bug hasn't moved anywhere in 10 months. What can be done to help it along?

### ch...@chromium.org (2020-05-26)

Hm, the repro no longer works for me on M81 on Android.

### s....@gmail.com (2020-05-26)

googlechrome: might not be supported anymore in that case. But this might work.
https://twitter.com/sirdarckcat/status/1255465623863341056

### [Deleted User] (2020-07-14)

morlovich: Uh oh! This issue still open and hasn't been updated in the last 824 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-28)

morlovich: Uh oh! This issue still open and hasn't been updated in the last 838 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2020-07-28)

Should this really be assigned to morlovich? Not really a cookie issue, more of a navigation/scheme issue.

### lu...@chromium.org (2020-07-29)

Right - it seems that the issue is that renderer-initiated navigations to googlechrome://navigate?url=https://shhnjk.azurewebsites.net/SameSite.php become browser-initiated navigations.  SameSite cookies is only one example of what is broken when an attacker can trigger browser-initiated navigations (Sec-Fetch-Site + ability to navigate to chrome:// URLs seems like another).

[Monorail components: -Blink>SecurityFeature -Internals>Network>Cookies Mobile>Intents UI>Browser>Navigation]

### lu...@chromium.org (2020-07-29)

qinmin@, I wonder if you could PTAL?  I see that after your r779166 intents propagate initiatorOrigin and isRendererInitiated - maybe this is sufficient to stop the SameSite cookies bypass here?

### qi...@chromium.org (2020-07-29)

Yes, it should stop bypasses that use the googlechrome scheme. But I am not sure what happens if the intent is sent to another app to jump back to chrome:

In https://bugs.chromium.org/p/chromium/issues/detail?id=1092453,  we have a case that the following intent can be used to jump back to Chrome to open a content URL:
android-app://com.google.android.googlequicksearchbox/android-app/com.android.chrome/content/media/external/downloads/xx 

We have a fix for the content scheme. But I am not sure if this is applicable to http URLs. If HTTP URLs are allowed, then the navigation will be treated as a browser initiated navigation.

Assinging to morlovich@ as suggested by #44.

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### jd...@chromium.org (2020-11-23)

Gentle ping from a Security 👮‍♂️. What's the next step to keep this moving this to completion? Thanks!

### mm...@chromium.org (2020-11-23)

https://crbug.com/chromium/831761#c44 was actually a suggestion that this should *not* be assigned to morlovich, since this isn't a network-layer cookie issue, but rather an issue with navigations / how we allow Chrome to be navigated.

### lu...@chromium.org (2020-11-23)

RE: https://crbug.com/chromium/831761#c47: qinmin@: Yes, it [r779166] should stop bypasses that use the googlechrome scheme

Given this, maybe this bug can be resolved as Fixed (since this bug report is specifically about the googlechrome scheme).

Please shout if you think that resolving this bug is a mistake and/or if there are specific follow-up bugs that should be opened.
(I am not sure if any additional test follow-up is needed, but I assume for now that the extra ExternalNavigationDelegateImplTest, IntentWithRequestMetadataHandlerTest and ExternalNavigationHandlerTest from r779166 provide sufficient coverage)


RE: https://crbug.com/chromium/831761#c47: qinmin@: I am not sure what happens if the intent is sent to another app to jump back to chrome:

I wonder if this (this = another Android app acting as an open proxy for launching browser-initiated navigations in Chrome) could be treated as 1) a separate security bug, 2) possibly a bug in the Android app, rather than a bug in Chrome.  Do we know of any such apps (especially pre-installed apps, or common apps)?

### lu...@chromium.org (2020-12-08)

Resolving the bug as fixed (as explained in https://crbug.com/chromium/831761#c54 above).  (I confirmed offline with the reporter that this sounds okay.)

### [Deleted User] (2020-12-08)

Not requesting merge to beta (M88) because latest trunk commit (680487) appears to be prior to beta branch point (827102). If this is incorrect, please replace the Merge-na label with Merge-Request-88. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-17)

Congratulations, the VRP panel has decided to award $1000 for this issue. I'll also figure out what release this shipped in, and go and update the relevant release notes and allocate a CVE... that whole process might take me a few weeks because it's something I do relatively rarely. The "relnotes_update_needed" note is to make sure I don't forget! Thanks for the report.

### s....@gmail.com (2020-12-17)

Thanks!

### ad...@google.com (2020-12-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/831761?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Mobile>Intents, UI>Browser>Navigation]
[Monorail blocking: crbug.com/chromium/786673, crbug.com/chromium/843478, crbug.com/chromium/979231]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091076)*
