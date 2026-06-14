# Security: Custom tab cookie handling

| Field | Value |
|-------|-------|
| **Issue ID** | [40059888](https://issues.chromium.org/issues/40059888) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P3 |
| **Component** | UI>Browser>Mobile>CustomTabs |
| **Reporter** | ph...@gmail.com |
| **Created** | 2022-06-07 |
| **Bounty** | $5,000.00 |

## Description

Reported in https://bugs.chromium.org/p/chromium/issues/detail?id=1235142#c16, but splitting into its own bug for separate consideration.

====

We also identified a potential issue in the way Chrome Custom Tabs handle SameSite strict cookies.

A Chrome Custom Tab sends cookies with the `SameSite` attribute set to `Strict` when a website is initially loaded in them. This poses a severe security concern.

## A) RFC 6265bis

RFC 6265bis specifies that "If the "SameSite" attribute's value is "Strict", the cookie will only be sent along with "same-site" requests." [^2] and that "Same-site cookies in "Strict" enforcement mode will not be sent along with top-level navigations which are triggered from a cross-site document context." [^3]

Opening a website in a Custom Tab represents a top-level navigation. It is, strictly speaking, not triggered from a cross-site document context. Thus, Chrome's behaviour, in our opinion, does not strictly violate this standard. However, opening a website in a Custom Tab is triggered from a _cross-platform_ context, which we believe should be treated equally to opening it from a cross-site document context for the reasons discussed in the following. 

## B) Security concerns

`SameSite` cookies are used to protect websites from XS attacks such as COSI and CSRF. `SameSite Lax` cookies in general provide a reasonable defense for those attacks, however do not provide protection against all COSI and CSRF attacks, such as when a website is opened in a pop-up. Also by using a Custom Tab in a way described in the very beginning of this bug report to run attacks similar to COSI and CSRF attacks, `SameSite Lax` cookies can be circumvented. `SameSite Strict` cookies provide an even more rigorous protection against those attacks, in which not even websites opened in a pop-up or websites opened by clicking on a link from another site send those cookies.

We understand that sending `SameSite Lax` cookies is necessary to offer the features Custom Tabs are designed for (such as, among others, SSO flows) and that this is a trade-off between usability and security. Also sending `SameSite Strict` cookies, however, circumvents one of the strongest and most rigorous mitigation strategy to tackle XS attacks. 

_Cross-platform_ context-initiated requests should be treated equally to cross-site document context-initiated requests, since the embedding context, i.e. the application that embeds the Custom Tab, can be operated by a malicious entity, as already described in the bug report. The embedding context can thus not be trusted and needs to be considered as a request originated from an untrusted entity, similarly as a cross-site document context-initiated request is considered as.

## C) Proposed changes

We propose to treat _cross-platform_-initiated requests equally to _cross-site_ document context-initiated requests, i.e. `SameSite` cookies in "Strict" enforcement mode should __also__ not be sent along with top-level navigations triggered from _cross-platform_ contexts. Firefox Custom Tabs already use this behaviour and thus mitigate the security concerns discussed in B).

[^1]: https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis-10
[^2]: https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis/#section-4.1.2.7
[^3]: https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis-10#section-5.4.7.1

## Timeline

### [Deleted User] (2022-06-07)

[Empty comment from Monorail migration]

### ye...@google.com (2022-06-07)

Assigning to peconn@ since they handled the other bug. Please reassign if needed.

[Monorail components: UI>Browser>Mobile>CustomTabs]

### [Deleted User] (2022-06-08)

[Empty comment from Monorail migration]

### pe...@chromium.org (2022-07-05)

Hey bingler@, I was wondering if you could help find the right person for this bug, it's going somewhat over my head.

As far as I understand it, the involvement with Custom Tabs is just "requests from Custom Tabs have a _cross-platform_ context", and the actual meat of the bug is: `SameSite` cookies in "Strict" enforcement mode should __also__ not be sent along with top-level navigations triggered from _cross-platform_ contexts

### bi...@chromium.org (2022-07-06)

Hi,

I think I'm the correct person, but I'm also not 100% clear on what this bug is trying to accomplish and how I'd help with that. I don't have access to the other bug linked in the description either.

* Are you looking for a design review?
* Are you looking for implementation assistance?

### pe...@chromium.org (2022-07-07)

I've cc'd you on the linked bug.

I think from the Custom Tabs point of view, we're doing things correctly, and is would be a bug (or feature request?) in the SameSite/cookies code, so I was hoping to hand this off to you.

Of course, it's up to you as to whether this is a serious issue and how it should be prioritised.

### bi...@chromium.org (2022-07-07)

I'm not sure this needs to be a change implemented in the cookie code or that the cookie code even needs to be aware of a "cross-platform" concept.

I'm not familiar with what the CCT start up process looks like but I expect that the initial navigation to the target url has a nullopt initiator value. The cookie code purposefully sends SameSite=Strict cookies on requests with a nullopt initiator and we withhold SameSite=Strict cookies if the initiator is cross-site.

So then one way to accomplish your goal would be to:
* identify a cross-platform context when loading the CCT
* Conditionally set the initiator of the initial request to an opaque origin. I.e.: `initiator = is_cross_platform_context ? url::Origin() : absl::nullopt`

### ad...@google.com (2022-07-15)

bingler@ As a bit more context here, this is an external vulnerability report from some folks at TU Wien. It _appears_ to be reported internally by myself because I split it off from another external report.

We (in Chrome security) don't make any claims that this is a valid vulnerability report. The current behavior might be working as intended. We will be reliant on you CCT + cookies experts to decide whether this is a valid risk to Chrome/CCT users.

I hope this helps explain the origin of where this request comes from!

### bi...@chromium.org (2022-07-15)

Thanks adetaylor@, I think that helps.

peconn@, I think it would be helpful to meet up and discuss the issue that way. We can sort out who needs to do what more easily that way I think. Should I schedule something with you or someone else?

### ad...@google.com (2022-07-15)

Cool. When/if you decide whether this is a real bug, please would you take a look at go/whos-the-sheriff and ask them to add a suitable FoundIn label based on your analysis? We need to set that label such that any security fixes get merged to the right branches and so that reporters are properly credited, but it's a bit fiddly to set, so it's probably best to get the security sheriff to do it. Thanks!

### ph...@gmail.com (2023-02-21)

Hello! Am I right under the assumption, that the issue was fixed in [this](https://source.chromium.org/chromium/chromium/src/+/17de49605ad55134f155c94af7155f0968c15f11) commit?

### ad...@google.com (2023-02-21)

mthiesse@ please could you comment on whether this and https://crbug.com/chromium/1368230 are duplicates?

### mt...@chromium.org (2023-02-24)

I'm going to assume _Cross-platform_ does not actually mean cross platform, and instead means launches from other apps into Chrome? (Also this issue was never specific to CCTs)

If so, yes I think this probably is a duplicate, or more precisely the same underlying problem triggered in different ways.

### ph...@gmail.com (2023-02-27)

Responding to mthiesse@, yes, with cross-platform we mean launching a website in Chrome from another application. The way we understood cross-platform is that native Android applications aka the "mobile platform" can interfere with the "web platform", thus cross-platform.

Now that https://crbug.com/chromium/1368230 does not carry security view restrictions anymore, we also believe that our bug and https://crbug.com/chromium/1368230 are not exact duplicates, but have the same root cause: Intents are treated as top-level user-initiated navigations in Chrome on Android. Our bug uses intents to open a CCT to circumvent SameSite Strict cookie restrictions, whereas https://crbug.com/chromium/1368230 uses self-intents to achieve this goal. The threat models of both bugs are different, but the capabilities remain the same. The bugs lever out one of the strongest mitigation strategies for cross-site leaks. In conjunction with https://crbug.com/chromium/12354142, which was the parent report for this bug until it was split, our approach was able to stealthily infer user information by opening a target website in a CCT which is loaded with SameSite strict cookies, immediately hiding the CCT and monitoring the navigation events (including the loading time) of the tab.

In our bug report, we furthermore suggested treating such cross-platform requests equally to cross-site requests that are not triggered by user activation. Our bug report, however, was not followed up on since July 2022, which is 1 month before #1368230. We understand that issues at the intersection of mobile and web platforms are more challenging to triage: indeed, this bug was fixed after a web-only bug that underlies the same issue was found. Nevertheless, we believe that our bug report should have been put into more consideration and not kept in a pending state for so long.

Considering that our original report included in #1235142 is from June, 2023 (3 months before #1368230), we kindly ask to be publicly credited for the issue alongside Axel Chong. As academic researchers, public acknowledgments are essential to substantiate claims about the novelty of our findings. Furthermore, based on this explanation, is it possible to be considered for a portion of the reward?

### bi...@chromium.org (2023-02-27)

Speaking from the cookies side of things, as far I can tell our cookie code is working as intended.

What needs to be determined is how CCT should interact with cookies, namely how the initiator of the navigation should be set.
I'm not the one to make that decision, but judging by the attack described it does seem like we should consider a change.

Similar to https://crbug.com/chromium/1368230 I expect the fix to be setting the initiator to a cross-site origin if the navigation comes from "cross-site" CCT (for whatever definition of cross-site makes the most sense for CCTs)

### mt...@chromium.org (2023-02-27)

I think this issue is also Fixed, but I'll leave it up to the security team to resolve the duplication/acknowledgement questions.

### ad...@google.com (2023-02-28)

From https://crbug.com/chromium/1334240#c14, https://crbug.com/chromium/1334240#c15 and https://crbug.com/chromium/1334240#c16 it seems that we're all agreed that this is the same root cause as https://crbug.com/chromium/1368230, and therefore this should be marked as a duplicate.

As the earlier bug, I agree this deserves credit. Labeling as such. Thanks for the report and for your understanding.

### [Deleted User] (2023-02-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-01)

adding release label to ensure this gets pulled into rel-notes-update process to be credited along with Axel Chong in the security fix notes for the M109 update when that is updated 

### [Deleted User] (2023-03-01)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-09)

Congratulations! The VRP Panel has decided to award you $5,000 for your initial and earlier reported discovery of this issue. Thank you for you for reaching out and letting us know this issue that you reported had been resolved and tied to another issue. We apologies for the overlook here and appreciate your patience while we correct it in terms of VRP reward and acknowledgement. 

### am...@google.com (2023-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2023-07-28)

This issue was migrated from crbug.com/chromium/1334240?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1368230]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059888)*
