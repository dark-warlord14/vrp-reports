# iframe sandbox allows redirecting to intents, including redirecting to navigation intents

| Field | Value |
|-------|-------|
| **Issue ID** | [40051530](https://issues.chromium.org/issues/40051530) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>IFrameSandbox, Internals>PlatformIntegration |
| **Platforms** | Android |
| **Reporter** | fr...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2020-02-16 |
| **Bounty** | $2,000.00 |

## Description



What about the HTML5 Sandbox? If you are not familiar with it, it’s just a way to impose restrictions to a webpage using the sandbox iframe attribute or the sandbox http header. For example, if we want to render content inside an iframe and make sure it does not run javascript (not even open new tabs) we can just use this tag:

POC

sandbox.html

<a href="https://search.app.goo.gl/?link=https%3A%2F%2Fapis.google.com%2Fadditnow%2Fl%3Fapplicationid%3D034375269201%26__ls%3Dogb%26__lu%3Dhttp%3A%2F%2F14.rs">click me</a>

chrome.html

<iframe src="sandbox.html" sandbox></iframe>

POC Url: http://gifsforu.000webhostapp.com/chrome.html

And the rendered page will be completely restricted. Essentially it can only render HTML/CSS but no javascript or access to things like cookies. In fact, if we use the sandbox granularity and allow at least new windows/tabs, all of them should inherit the sandboxed attributes and opened links from that iframe will still be sanboxed. However, using the  Firebase Dynamic Links (FDL) bypasses this completely.FDLs are smart URLs that allow you to send existing and potential users to any location within an iOS, Android or web app.



## Attachments

- [SVID_20200217_020825_1.mp4](attachments/SVID_20200217_020825_1.mp4) (video/mp4, 9.4 MB)
- [SVID_20200219_013939_1.mp4](attachments/SVID_20200219_013939_1.mp4) (video/mp4, 2.7 MB)

## Timeline

### rs...@chromium.org (2020-02-17)

palmer/torne: Could you help me confirm this is WontFix/WorkingAsIntended?

From the reproduce case, the iframe link goes to FDL, which then triggers the native intent/app selection, creating a navigation intent (hence the "Open in Chrome"), which then triggers a navigation. As best I can tell, iframe sandbox does not guard / prevent such navigations when redirecting through native.

https://html.spec.whatwg.org/multipage/iframe-embed-object.html#attr-iframe-sandbox is the relevant part of the spec, and I suspect https://html.spec.whatwg.org/multipage/origin.html#sandboxed-top-level-navigation-with-user-activation-browsing-context-flag is the relevant property here that is nominally designed to prevent navigation.

That said, I can see a possibility of perhaps attempting to block all native handlers for iframe sandboxes, so I'm not closing this outright, but I'm hoping some Android folks can help me triage this. I've tentatively labeled this Low/Stable, but it may be WAI/Not a security bug.

[Monorail components: Blink>SecurityFeature>IFrameSandbox Internals>PlatformIntegration]

### [Deleted User] (2020-02-17)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2020-02-17)

This doesn't seem desirable to me. The behaviour here is that the page is redirecting to an intent:// URL with a browser fallback URL in case the intent is not handled by any installed app.

We probably should not handle intent:// URLs or generally do any intent dispatching (e.g. for apps that claim http/https URLs) when the iframe sandbox is enabled in the first place, but even if we consider that "reasonable", it seems like if the intent is not handled, the browser fallback URL is invoked outside of the iframe sandbox, which seems equivalent to opening a new tab.

I'll have a fiddle with this tomorrow to see if the behaviour is working exactly how I'm assuming here, and show a simpler example (without the FDL thing) if I can.

### to...@chromium.org (2020-02-18)

OK, it's not quite as I thought but the security impact seems the same - the fallback URL does not actually work (though I'm not sure why). It does have to be a URL that matches an intent handler on the device which has the BROWSABLE category to permit it to be launched from the web; either an intent: URL or an app-specific scheme.

So the behaviour here that seems unexpected to me is just "sandboxed iframes can be navigated to URLs that trigger android app intents", which seems like it should be blocked from a fully sandboxed iframe - none of the sandbox permissions really quite match "launch an external app's url handler" but "allow-popups-to-escape-sandbox" might be closest?

It just happens that the FDL intent being invoked here ultimately causes another intent to be dispatched *back to the browser* to open a URL, which is treated the same as any other external intent received by Chrome; that part isn't security-relevant (once we allow external intents to be invoked they could do anything the target app can do by definition).

### pa...@chromium.org (2020-02-18)

[Empty comment from Monorail migration]

### fr...@gmail.com (2020-02-18)

New POC.Sandbox allow intent:// to open url

Example

Install Chrome & Microsoft Edge Browser In Android

Open this url in chrome http://gifsforu.000webhostapp.com/Google.html

& click to "Click Here" .

Url open in edge via chrome sandbox.

### to...@chromium.org (2020-02-19)

Yeah - that is an app-specific scheme which is another one of the cases I mentioned in c#4. Same problem (allowing any intent dispatching at all from a sandboxed iframe).

### ts...@chromium.org (2020-03-11)

torne, feel free to re-assign as appropriate, but security bugs should always have an owner specified. Thanks!

### [Deleted User] (2020-03-11)

[Empty comment from Monorail migration]

### to...@chromium.org (2020-03-16)

Colin, you've been componentising this code for WL - thought I should cc you here to give you a heads up on this and maybe help find an owner :)

### bl...@chromium.org (2020-03-17)

Robert, would you be able to make a decision here from the Android security PoV?  c#4 seems to capture the problem well.

CC'ing folks who are involved with the Chrome external intent launching machinery.

### rs...@chromium.org (2020-03-17)

I agree that we should block <iframe sandbox> intent launching.

As to which token to permit it under, allow-popups-to-escape-sandbox could work. But launching an Activity also seems like a top-level navigation, so perhaps allow-top-navigation. While an Activity might not be a “browsing context” under the spec, launching one might constitute “closing the[] top-level browsing context.”

Perhaps we should chat with a spec person to get their perspective on which token to use. But generally restricting SGTM.

### bl...@chromium.org (2020-03-18)

Thanks!

I don't think that I'm the right person to drive this. Yaron/Michael, would it make sense for someone on your side to take this on?

### mt...@chromium.org (2020-03-18)

[Empty comment from Monorail migration]

### mt...@chromium.org (2020-03-26)

Pulling in mkwst@ here for spec-related questions.

If we were to block external android intents coming from sandboxed iframes, and allow based on either allow-popups-to-escape-sandbox or allow-top-navigation, would this require updating specs? Do you have opinions on which attribute to allow Android Intents under?

We already require a user gesture for launching external intents, so the distinction between allow-top-navigation and allow-top-navigation-by-user-activation doesn't really matter in this case.

### mk...@chromium.org (2020-03-27)

From a spec perspective, this would be a navigation that falls through step 16 of https://html.spec.whatwg.org/#navigating-across-documents into https://html.spec.whatwg.org/#process-a-navigate-url-scheme.


I agree with folks above that we ought to restrict intent navigation in a fully-sandboxed frame. It's not actually clear to me that we need to tie it to any of the existing sandbox flags: perhaps we could just disallow it entirely without an opt-out, as we do for plugins?

If we can't simply disallow it, I don't have a strong opinion between treating the intent navigation as a sandbox escape or a top-level navigation. The "escape-sandbox" bit of the former is appealing, and seems to reasonably represent the risk (but it's not a popup). The latter provides similar capabilities insofar as the frame could just navigate its parent to a page that triggered the intent. *shrug* I could justify either to myself. Flip a coin? :)

### mt...@chromium.org (2020-03-27)

Hmm thinking about this more, I think it kind of is a popup, in the same sense that target="_blank" is a popup - a different app is showing up over top of the main frame, but not navigating the main frame or anything (and by design BROWSABLE intent handlers should expect to be used by arbitrary insecure content). Top-level navigation doesn't really make sense because you're not actually navigating the main frame or interacting with it at all. The main use case that comes to mind would be for ads to open up the play store to their app. How common is it for ads to be sandboxed?

### fr...@gmail.com (2020-06-26)

Hi any update? It eligible for bounty?

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### mt...@chromium.org (2020-11-16)

Passing off to mkwst@ for triage. See  https://crbug.com/chromium/1148777.

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### fr...@gmail.com (2021-05-03)

Any update on this report? 

### fr...@gmail.com (2022-02-15)

Any information?

### pa...@chromium.org (2022-02-15)

[Empty comment from Monorail migration]

### ar...@google.com (2022-07-02)

I think I fixed it as part of:
https://chromestatus.com/feature/5680742077038592

This new feature was first asked in 2016:
https://github.com/whatwg/html/issues/2191#issuecomment-1006573881

And then a few month after this bug, there was: https://crbug.com/1148777



### [Deleted User] (2022-07-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-29)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts in reporting this issue to us and your patience while we addressed this issue! 

### am...@google.com (2022-07-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-10-14)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-18)

bugs discovered and fixed in head do not go through CVE and rel notes process; removing labels accordingly 

### is...@google.com (2023-01-18)

This issue was migrated from crbug.com/chromium/1052690?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>IFrameSandbox, Internals>PlatformIntegration]
[Monorail mergedwith: crbug.com/chromium/1223392]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051530)*
