# Security: Displaying a page action popup from the omnibox prevents an infobar from displaying

| Field | Value |
|-------|-------|
| **Issue ID** | [40052000](https://issues.chromium.org/issues/40052000) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>Infobars |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pk...@chromium.org |
| **Created** | 2020-04-12 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 84.0.4110.0 (Official Build) canary (64-bit)  

Operating System: All

**REPRODUCTION CASE**

1. Install the attached extension.
2. the extension will open a new tab
3. Observe, that URL is updated incorrectly to gmail.com but content page is incorrect.

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 4.4 KB)
- [Screen Shot 2020-04-12 at 8.10.02 AM.png](attachments/Screen Shot 2020-04-12 at 8.10.02 AM.png) (image/png, 97.4 KB)

## Timeline

### xi...@chromium.org (2020-04-13)

Thanks for the report. Not sure if this is WAI as extensions are supposed to have such permission. +rdevlin.cronin@ for the input. Feel free to reassign. Thanks!

[Monorail components: Platform>Extensions]

### [Deleted User] (2020-04-14)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2020-04-15)

This uses an extension that has access to all sites in order to manipulate the content of a site.  That is definitely WAI, and is not a security vulnerability.  This is easily achievable through a number of mechanisms, including content scripts, webRequest, and the debugger API.

What this extension does is basically:
- Open a new tab to gmail.com
- Debug that tab
- Intercept the network request and substitute it with `"<script>document.write('hello world');document.location='tel:+12133';setTimeout('alert()', 300)<\/script>"`

This results in the "hello world" and an alert being shown on gmail.com.  This is all WAI.

What is interesting here is that the extension chooses to use the debugger API, and suppresses the debugging infobar by setting `document.location='tel:+12133'`.  This results in a popup being shown from the omnibox, which somehow suppresses the infobar from being shown.  (I haven't dug into this extensively, but commenting out that part of the script results in the infobar being correctly shown.)

In this particular case, that's not particularly scary - again, this type of modification can happen easily in any number of mechanisms.  But the debugger API provides a lot more power, too, which is why we have an infobar.  I think that suppression is the only bug here.  Updating description to match.

pkasting@, as owner of infobars, mind taking a look and retriaging as appropriate?

[Monorail components: UI>Browser>Infobars]

### pk...@chromium.org (2020-04-16)

In some preliminary testing outside a debugger, the infobar is shown, but quickly dismissed, probably due to some kind of navigation.  I'll need to use a debugger to see what the precise navigation event sequence is, as well as thinking more broadly about the right fix here (e.g. probably the "debugging this page" infobar should never expire until either explicitly dismissed or the extension is no longer able to control the page).

### rd...@chromium.org (2020-04-16)

We may even want to have the infobar persist even if the extension is unable to control the page _anymore_ (until dismissed by the user) to prevent a cycle of attach(), <manipulate>, detach() by the extension to hide its behavior.

### pk...@chromium.org (2020-04-16)

Fair enough.  That makes the change simple; I'll just do that.

### pk...@chromium.org (2020-04-16)

More complicated than I thought.  This infobar is already set to not expire; however, the navigation request detaches the dev tools agent host, which closes the infobar.  So basically, we're in the scenario you describe in https://crbug.com/chromium/1070066#c7.  If we keep the infobar up we have to ensure it doesn't hold any dangling pointers.  Hopefully doable...

### pk...@chromium.org (2020-04-17)

Hoo boy.  This has the most complicated ownership and referencing structure of any infobar code I've seen.  I think I'm going to have to try and undo https://codereview.chromium.org/1448903004 , accomplish its aims without using an indirection object, and then see if I can hook the host directly to the infobar delegate in such a way that the callbacks are canceled (maybe via subscription objects) if the host detaches.

That, or else I'm going to have to stare at the existing web of objects and pointers long enough to figure out how to tweak it to accomplish the goals here.  :/

### sr...@google.com (2020-04-20)

M83 has been promoted to beta last week, with COVID-19 we want to get all blockers reviewed/fixed as early as possible so that we can bake them in beta longer. Please help review this RBS and if this is indeed critical bug fix, help get the fix ready for merge asap and merge to M-83 branch. if this is not a blocker, please remove the RBS label.

### pk...@chromium.org (2020-04-20)

I wouldn't mind if the security folks could adjust the categorization of this bug as appropriate per https://crbug.com/chromium/1070066#c5 -- that description seems accurate to me.

I don't think this is RBS.

### pk...@chromium.org (2020-04-21)

Today I wrote up notes on all the different classes involved here and I have a better idea how to fix.  I think the first paragraph of https://crbug.com/chromium/1070066#c10 was on target, and this will be easier to do than I feared.  (Famous last words)

Devlin - do we _ever_ need to auto-close the infobar, e.g. if the extension is uninstalled entirely while the infobar is showing?  Or should it just remain up forever once it appears, until the user explicitly dismisses it, no matter what has happened to the extension, tabs being debugged, etc.?

### rd...@chromium.org (2020-04-21)

Thanks for looking into this, pkasting@!

(Just as background)
Today, my understanding is: Infobar shows while the extension is debugging the page (% this bug).  If the user hits cancel to close the infobar, the extension is force-detached.  If the extension detaches, the infobar will also close.

I would be fine with changing this to:
Infobar shows when the extension starts debugging the page.  If the user hits cancel to close the infobar, the extension is force-detached.  The infobar never auto-dismisses.

If we go that route:
- We may need to modify the dismiss callbacks in extension_dev_tools_infobar.  They might have some implicit expectation that the extension still exists.  (I haven't audited them to verify one way or the other.)
- We may want to change the text of the infobar [1].  It currently says "Alpha is debugging this browser" (where "Alpha" is the extension).  We might want to say something like "Alpha started debugging this browser", so that it's correct even if it's no longer actively debugging.

This would potentially make the flow a bit noisier for some users (those who had extensions that drove the attach / detach cycle, and didn't stop debugging from the infobar).  Given a) how scary debugging is and b) how noisy the debug flow currently is, I'm fine with this extra friction.

+meacer@ as well for an Enamelite's point of view.

[1] https://source.chromium.org/chromium/chromium/src/+/master:chrome/app/generated_resources.grd;l=3255;drc=91e7365fd6e2ff83edbc1f87a1e8d540735ca453

### [Deleted User] (2020-04-21)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2020-04-21)

I'm not sure why Sheriffbot is so convinced this is a regression.  AFAICT, this was probably ~always the case.

### pk...@chromium.org (2020-04-21)

Your understanding of the current behavior is correct.  Your suggested string change SGTM; I don't know whether we need to get any sort of PM or tech writer input on this (I doubt it, I plan to just change it).  I will worry about making sure of the correct lifetimes of callbacks involved in this flow while I make my change.

### rd...@chromium.org (2020-04-21)

I don't think we need PM / TW here - I'd view this simply as "fixing a bug".  I'd like meacer@'s thoughts from an Enamel perspective, but, assuming there are no objections, I'd say we're good to go.

### me...@chromium.org (2020-04-21)

No objections to the string change. I also don't think this is a medium severity bug since the extension needs the devtools permission. We can change it to Low if you all agree.

### pk...@chromium.org (2020-04-21)

Low is fine with me.

### rd...@chromium.org (2020-04-21)

I could go either way on the severity.  On the one hand, it does need devtools permission.  On the other, it can hide the fact that the extension is using that permission.  So... <shrug>.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f8b1793382a1ccf2d6ae6626b92fb3540c5eef7f

commit f8b1793382a1ccf2d6ae6626b92fb3540c5eef7f
Author: Peter Kasting <pkasting@chromium.org>
Date: Wed Apr 29 19:07:14 2020

Remove extension dev tools infobar only when the user closes/cancels it.

Previously, the bar also disappeared if it was no longer applicable,
i.e. no more extensions were attached.  This is problematic since the
extension may have made persistent changes to the page, and the user
needs to be guaranteed an opportunity to see something telling them
that.

Bug: 1070066
Change-Id: I3bf573013037752be9654c2840b153b5ab8d85a3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2159967
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#763940}

[modify] https://crrev.com/f8b1793382a1ccf2d6ae6626b92fb3540c5eef7f/chrome/app/generated_resources.grd
[modify] https://crrev.com/f8b1793382a1ccf2d6ae6626b92fb3540c5eef7f/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/f8b1793382a1ccf2d6ae6626b92fb3540c5eef7f/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[modify] https://crrev.com/f8b1793382a1ccf2d6ae6626b92fb3540c5eef7f/chrome/browser/extensions/api/debugger/extension_dev_tools_infobar.cc
[modify] https://crrev.com/f8b1793382a1ccf2d6ae6626b92fb3540c5eef7f/chrome/browser/extensions/api/debugger/extension_dev_tools_infobar.h


### pk...@chromium.org (2020-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-30)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-04)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-07)

Congrats! The Panel awarded $500 for this report. 

### na...@google.com (2020-05-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1070066?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Browser>Infobars]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052000)*
