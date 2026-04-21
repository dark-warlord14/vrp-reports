# Security: Url Hijacking using intent:// when onload  web page using bookmark (Google Chrome Android)

| Field | Value |
|-------|-------|
| **Issue ID** | [40058896](https://issues.chromium.org/issues/40058896) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Sandbox>SiteIsolation, Mobile>Intents, UI>Browser>Bookmarks |
| **Platforms** | Android |
| **Reporter** | sa...@gmail.com |
| **Assignee** | mt...@chromium.org |
| **Created** | 2022-02-24 |
| **Bounty** | $2,000.00 |

## Description

deleted

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-02-24)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-02-24)

So opening a webpage from bookmarks allows it to launch intents. I wonder if this is because the bookmark is loaded from the NTP which is WebUI, or some other interaction. The last bug about this is full of folks who are now gone. tedchoc@ I see you were involved, could you triage?

Severity Low since the last bug was as well? Popping calc from a webpage is spooky though it's not through ACE here.

It looks like this repros as far back as 74, maybe.

[Monorail components: Internals>Sandbox>SiteIsolation Mobile>Intents UI>Browser>Bookmarks]

### te...@chromium.org (2022-02-25)

[Empty comment from Monorail migration]

### mt...@chromium.org (2022-02-25)

I've known we could do this for a while, and popping calc unprompted isn't special on Android (Play has a web-exposed API that is able to launch any app as though from the app launcher, and nobody seems to think this is an issue). I would say this isn't a security issue at all, but I'll defer to security folks like rsesek on that.

Is there a reason we would want to prevent sites loaded from bookmarks from redirecting to an app? Maybe we should prefer to stay in browser because the user may be expecting that, but doesn't seem very important.

### te...@chromium.org (2022-02-25)

Does the site need to be bookmarked? From the video, it looks to be launched via a Most Visited Tile on the NTP.

Or does a MV tile or a bookmark launch result in the same experience (e.g. not an omnibox typed URL)? Where the other bug (331571) was explicitly discussing launching a website after typing in the omnibox.

### sa...@gmail.com (2022-02-25)

it can be run from both either from bookmarks or via a Most Visited Tile on the NTP.

### mt...@chromium.org (2022-02-25)

Yep, the other bug was explicitly only about omnibox navigations - any other kind of navigation as long as it's initiated by the user and not back/forward is allowed to redirect to an app, including launcher shortcuts, bookmarks, NTP tiles (and probably other things I've missed - maybe notifications?).

### rs...@chromium.org (2022-03-03)

> Is there a reason we would want to prevent sites loaded from bookmarks from redirecting to an app? Maybe we should prefer to stay in browser because the user may be expecting that, but doesn't seem very important.

It seems like a bypass of the redirect mitigation. Is the bookmark/NTP tile tap considered a user gesture for that purpose?

I agree that this seems like it may not be a security issue, though I could also consider it Sev-Low.

### [Deleted User] (2022-03-03)

[Empty comment from Monorail migration]

### mt...@chromium.org (2022-03-03)

> It seems like a bypass of the redirect mitigation. Is the bookmark/NTP tile tap considered a user gesture for that purpose?

I don't know what the original thinking was, but gesture is only a requirement for link-type navigations right now (though we're planning to fix that at least for form submits as those should definitely also require a gesture).

Probably the thinking was all other types are assumed to be triggered by the user?

### rs...@chromium.org (2022-03-04)

Sure. And the precondition for needing to have the page bookmarked or visited enough to be a NTP tile seems like a mitigating circumstance. I guess a different variant on the question is: are there cases where we shouldn’t enforce a user gesture requirement?

### mt...@chromium.org (2022-03-04)

>  are there cases where we shouldn’t enforce a user gesture requirement?
The only case that comes to mind is intent launches that redirect out of Chrome. The open question is whether Chrome browser UI initiated navigations should be considered to have a gesture and allow external navigation. Currently we allow it except for omnibox, which seems like a okay choice to me. 

For example, if you bookmarked a youtube video on desktop and it sync'd over to your phone, it might actually be desirable that it opens in the youtube app, though right now it would require youtube to do a client-side redirect because server redirects count as the initial navigation off of the bookmark as far as ExternalNavigationHandler is concerned, which don't allow the external navigation. (There are a bunch of inconsistencies like this we should probably resolve at some point)

### rs...@chromium.org (2022-03-04)

> The open question is whether Chrome browser UI initiated navigations should be considered to have a gesture and allow external navigation. Currently we allow it except for omnibox, which seems like a okay choice to me. 

Yup, agree that typed URLs should continue to not intent out (because of the presumed/inferred desire to do something within the browser). I could go either way on the browser-UI-navigations.

### mt...@chromium.org (2022-04-11)

How do we want to decide this? The current code is a mess and I'd like to make it consistent one way or the other on whether browser-UI-initiated navigations are blocked.

### mt...@chromium.org (2022-07-06)

Now that we have a Message to ask users if they want to leave Chrome, I think my suggestion would be to always stay in browser for browser-initiated navigations (other than Intents), and if a page redirects to an external protocol off of any browser-initiated navigation (including omnibox) we should show the message asking if the user wants to launch the app.

Thoughts rsesek/tedchoc/yfriedman?

### yf...@chromium.org (2022-07-12)

From a product perspective, we definitely intentionally treated the omnibox (and *only* the omnibox) specially wrt to typed urls so it makes sense that these two types of "browser-initiated" loads are treated differently. Even though they're both browser-initiated, from user POV, we're just special casing the omnibox.

I guess I'm fine with the proposal in #15 if it helps simplify things because I would still want to preserve that omnibox stays in chrome so if you need consistency that's the only way we can go

### te...@chromium.org (2022-07-12)

Nothing to add on top of yfriedman's comment. Keeping the behavior of the omnibox is certainly the top priority, and the proposal in c#15 seems to keep that while simplifying the logic overall.

### gi...@appspot.gserviceaccount.com (2022-07-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7646c97c4846bdc728c56092a0c157ee387ff840

commit 7646c97c4846bdc728c56092a0c157ee387ff840
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Fri Jul 22 22:14:28 2022

Show Message for browser-initiated navigations leaving Chrome

Right now our logic is pretty complicated for deciding whether a
browser-initiated navigation should be allowed to leave Chrome (and
it pre-dates the existence of a Message). We make exceptions for 30x
redirects from typed URLs, and allow non-typed browser initiated
navigations from things like bookmarks to redirect only through client
redirects, not 30x redirects.

This change unifies all browser-initiated navigations (excluding
Intents) to require the user to give consent to leave Chrome through a
Message.

Bug: 1300539
Change-Id: Ibc01ff8dadb4e184169dcbdd6ebc72e3f1b1066a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3780380
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1027445}

[modify] https://crrev.com/7646c97c4846bdc728c56092a0c157ee387ff840/components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java
[modify] https://crrev.com/7646c97c4846bdc728c56092a0c157ee387ff840/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
[modify] https://crrev.com/7646c97c4846bdc728c56092a0c157ee387ff840/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java
[modify] https://crrev.com/7646c97c4846bdc728c56092a0c157ee387ff840/components/external_intents/android/java/src/org/chromium/components/external_intents/RedirectHandler.java


### mt...@chromium.org (2022-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-17)

Congratulations, Hafiizh! The VRP Panel has decided to award you $2,000 for this report. A member of our finance team will reach out to you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### sa...@gmail.com (2022-08-23)

thank you amy, how long does it take for the reward to be processed?

### am...@chromium.org (2022-08-23)

You're very welcome. Thanks again for your report. 

>>how long does it take for the reward to be processed? 
This depends a lot on your locale and financial/banking institution after being enrolled, which will require some forms to be completed on your part. Please reach out to p2p-vrp@google.com with questions or issues concerning reward payment processing. 

### ad...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-11-08)

This issue was migrated from crbug.com/chromium/1300539?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Mobile>Intents, UI>Browser>Bookmarks]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058896)*
