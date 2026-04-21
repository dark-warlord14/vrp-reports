# Security: CORB allows for cross-origin leaks on social networks

| Field | Value |
|-------|-------|
| **Issue ID** | [40093907](https://issues.chromium.org/issues/40093907) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature, Blink>SecurityFeature>ORB, Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | vo...@chromium.org |
| **Created** | 2019-01-30 |
| **Bounty** | $2,000.00 |

## Description

While the purpose of Cross-Origin Read Blocking (CORB) is to mitigate against side-channel attacks, it (ironically) has made some cross-origin leaks possible again. Consider the following:
<script src=https://www.chromium.org/ onload=alert(0) onerror=alert(1)></script>

Before CORB was implemented, such a 200 HTTP response with a "nosniff" header and a non-executable MIME type (text/html) would have caused the onerror event handler to fire. But because CORB replaces the original response (including headers) with an empty response instead, the onerror event handler does not fire (and the onload event handler fires instead).

And on the other hand:
<script src=https://www.chromium.org/error onload=alert(0) onerror=alert(1)></script>

This would normally trigger the onerror event handler as it's an error response (which it still does).

Previously, it was not possible to distinguish between the two cases as both would have triggered the onerror event handler. But now that CORB creates a distinction, this introduces cross-origin leaks on popular social networks that could, for instance, allow an attacker to deanonymize users—or check if the currently logged-in user is a member of a certain group and what not—based on whether or not CORB blocks the response when attempting to load authenticated, user-specific resources (e.g., <script src=https://social.network.tld/user/1111/messages.json onload=alert(0) onerror=alert(1)>).

I've reported such leaks to the affected social networks, and they're currently working on mitigating these issues on their end. However, I believe these web applications are actually following best practices, and it's more of a Chromium issue that needs to be addressed (especially that this is not an issue on other browsers—e.g., Firefox).

Please consider not removing the view restrictions for the time being in case you decide not to make any changes regarding this issue; thanks!

## Attachments

- [deanonymize.html](attachments/deanonymize.html) (text/plain, 629 B)

## Timeline

### me...@chromium.org (2019-01-31)

Thanks for the report. This looks like a legitimate issue. 
However, to it appears to be the same problem as reported in https://crbug.com/chromium/925274.
lukasza and sroettger does this look like a duplicate of https://crbug.com/chromium/925274?

[Monorail components: Blink>SecurityFeature]

### sh...@chromium.org (2019-01-31)

[Empty comment from Monorail migration]

### lu...@chromium.org (2019-01-31)

Yes - thank you very much for the report!  This does indeed seem to be a duplicate of https://crbug.com/chromium/925274, so let me resolve it as such.

### lu...@chromium.org (2019-02-01)

Un-duplicating based on the comment in https://crbug.com/925274#c10

So, is the problem mainly related to the fact that CORB drops the 'X-Content-Type-Options' and 'Content-Type' headers, which means that scripts/stylesheets won't retain the behavior from:

> If destination is script-like and mimeType is failure or is not a JavaScript MIME type, then return blocked.

> If destination is "style" and mimeType is failure or its essence is not "text/css", then return blocked.

Is this a fair characterization of the problem?


I guess this is a bug in Chrome implementation and also a spec bug (because the spec asks to perform CORB checks in step 5 of section "4.1. Main fetch", and only asks to perform nosniff checks in step 11 of the same section).  Maybe we need to augment this part of the spec:

> Return a new response whose status is noCorsResponse’s status, HTTPS state is noCorsResponse’s HTTPS state, and CSP list is noCorsResponse’s CSP list.

to say that 'X-Content-Type-Options' and 'Content-Type' headers should be retained.

[Monorail components: Internals>Sandbox>SiteIsolation]

### an...@gmail.com (2019-02-01)

I'd against suggest to more strongly consider fixing https://github.com/whatwg/fetch/issues/727. I.e., to not give CORB a different kind of response, but instead use a network error. This will make CORB observable for some requests, but that should not be more problematic than returning a network error for the wrong MIME type.

Letting parts of the response leak in order for a later part of the system to trigger some kind of error handling seems rather error prone, as this bug demonstrates.

### an...@gmail.com (2019-02-01)

s/against/again/ (apologies)

### 0x...@gmail.com (2019-02-01)

Re #4: Yes, that's an accurate description of the problem (and the proposed change would indeed be a sufficient fix).

Ideally, we don't want responses blocked by CORB to be distinguishable from non-blocked responses. I believe that returning a network error or using an empty response are both unfavorable as they both create detectable distinctions that would result in info leaks depending on how a given endpoint behaves....

Regarding how much such info leaks matter in practice, I can provide real-world attack scenarios if this might be helpful (not sure if that'd be OK though—maybe I can CC a Twitter/Facebook security engineer to shed some light on the implications of such issues in relation to their respective platforms). But generally speaking, these info leaks do have non-trivial privacy implications for social network users in particular and are not easy for developers to fix.

### 0x...@gmail.com (2019-02-03)

On a side note, it seems that Monorail is also affected by these info leaks to some extend. Though for a bug tracker like Monorail, potential leaks are probably limited to things like who the current user is and what level of access the current user might have....

For instance, let's say that evil.com wants to check if its current visitor is lukasza@ or annevankesteren@; this info can be leaked via the endpoint "https://bugs.chromium.org/u/{userId}/queries". You can check the attached HTML document for a basic proof of concept.


### an...@gmail.com (2019-02-04)

It's not clear to me that "bleeding" enough of the response to the rest of the system so the rest of the system can fail with a network error if needed is sound. I'm rather worried about keeping that working well long term and without error.

It's also not clear to me that reliably returning a network error is problematic. It wouldn't be for any of the examples given thus far.

A problem might be if the (determined) MIME type of the response varies on a cookie. However, that can generally already be observed via other ways. E.g., script does not execute for a non-2xx response.

### me...@chromium.org (2019-02-13)

I presume this affects stable channel.

### sh...@chromium.org (2019-02-13)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2019-02-15)

Re (#c9):

I think that CORB serves its purpose as long as the sensitive parts of an HTTP response are blocked (that is, response body and custom headers). The examples given thus far are only subject to the current CORB behavior of blocking HTTP responses, and as such, switching to network errors won't be a problem in these cases.

> However, that can generally already be observed via other ways. E.g., script does not execute for a non-2xx response.

This is not always the case though. It's not uncommon that an endpoint returns a 200 HTTP response either way even when the response is empty or just some error message. In such cases, a network error raised for one of the responses would surely introduce a leak that wouldn't be reliably observable otherwise....

### sh...@chromium.org (2019-02-16)

lukasza: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@chromium.org (2019-02-19)

I think that based on https://docs.google.com/document/d/1kdqstoT1uH5JafGmRXrtKE4yVfjUVmXitjcvJ4tbBvM we are currently leaning toward resolving this as WontFix and asking websites to protect themselves either by:

1. blocking the response entirely (e.g. by using XSRF token, or in the future by relying on Sec-Fetch-Site)

or

2. making search-success indistinguishable from search-failure (e.g. by applying Cross-Origin-Resource-Policy response header to both).

### 0x...@gmail.com (2019-02-20)

I think what's outlined in https://docs.google.com/document/d/1kdqstoT1uH5JafGmRXrtKE4yVfjUVmXitjcvJ4tbBvM is an overgeneralization of the original issue here. The idea was simply that retaining the XCTO and CT headers in CORB-blocked responses would throw an error later due to a MIME type mismatch. When this error is not thrown (because CORB strips both the XCTO and CT headers), this makes a side-channel attack possible in the wild (which was previously not possible before CORB).

Retaining the actual headers might not be necessary to fix this issue. All that's required from the browser side is to enforce the behavior outlined at "https://fetch.spec.whatwg.org/#should-response-to-request-be-blocked-due-to-nosniff?" regardless of CORB.

### lu...@chromium.org (2019-03-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-05)

creis: Uh oh! This issue still open and hasn't been updated in the last 33 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2019-03-28)

Friendly security sheriff ping. creis, is there any movement on this? Thanks for your help!

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### dr...@chromium.org (2019-05-30)

Friendly security sheriff ping - any update on this?

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-08-07)

Friendly security marshal ping. creis, any updates?

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

### [Deleted User] (2020-07-14)

creis: Uh oh! This issue still open and hasn't been updated in the last 530 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-28)

creis: Uh oh! This issue still open and hasn't been updated in the last 544 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@chromium.org (2020-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### lu...@chromium.org (2020-12-07)

[Empty comment from Monorail migration]

### lu...@chromium.org (2020-12-07)

(extra CCs are related to an XS-leak of a somewhat different nature from https://crbug.com/chromium/1154250)

### an...@gmail.com (2020-12-08)

Could you CC me on that newer issue Lukasz? Appreciate it!

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-22)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-28)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-25)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-05)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-16)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-27)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-06)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### lu...@chromium.org (2022-07-13)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ORB]

### ts...@chromium.org (2022-07-20)

Hey nasko, is there someone else on the team that might take a look at this very old bug?

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-28)

This issue has not been updated for 60 or more days - lowering its priority to P2.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-25)

security marshal here -

clamy@ this aged bug might be related to some of the work you might be doing? it looks like way back when in https://crbug.com/chromium/927091#c14 we were considering closing this as a wontfix. do you have any insight/opinions?

### cr...@chromium.org (2023-01-27)

clamy@: Can you help triage this as an XSLeaks issue?  We probably have more context on how to treat such issues these days (e.g., when they are actionable vs WontFix).

### cl...@chromium.org (2023-01-27)

+vogelheim: I think this one should be fixed when we launch error handling in ORB.

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-11-23)

vogelheim@: Would you mind providing an update on this? It looks like there has been some code landed for ORB error handling but work is still ongoing, but it isn't obvious what would be sufficient to resolve this bug.

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### vo...@google.com (2023-12-11)

https://crbug.com/chromium/927091#c83: We have implemented ORB "v0.2" error handling, which would raise a network error in these situations, and which IMHO should fix this issue.

Because this change is web observable and potentially has compatibility impact, we're launching this gradually via server side experiments. It's currently enabled at 1% of stable. My intent is to ramp it up to 100% in early 2024 (after the Chrome production freeze). I'll leave this bug open until ORB "v0.2" has launched to 100%.

### yu...@google.com (2024-01-06)

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-30)

This issue was migrated from crbug.com/chromium/927091?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature, Blink>SecurityFeature>ORB, Internals>Sandbox>SiteIsolation]
[Monorail mergedinto: crbug.com/chromium/925274]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-02-14)

reopening this issue that was closed as a duplicate due to a bug in the issue tracker migration (reported and tracked as internal migration feedback issue [b/325072672](https://issues.chromium.org/issues/325072672))

### am...@chromium.org (2024-02-14)

assigning to vogelheim@ as per source issue linked in c#116

### vo...@google.com (2024-02-21)

Per [#comment86](https://issues.chromium.org/issues/40093907#comment86): ORB "v0.2", which signals CORB/ORB-blocked with a network error, is default-enabled in M123. This should finally resolve this issue. Sorry this took a bit.

### am...@google.com (2024-02-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-29)

Congratulations! The Chrome VRP Panel has decided to award you $2,000 for this report of user information disclosure. Thank you for your efforts in discovering and reporting this issue to us back in 2019! Sorry it took some time in getting it resolve and we appreciate you patience in the meantime.

### pe...@google.com (2024-05-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093907)*
