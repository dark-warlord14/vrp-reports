# Security: Temporary addressbar spoof with PDF navigation to sites with long response time

| Field | Value |
|-------|-------|
| **Issue ID** | [40085816](https://issues.chromium.org/issues/40085816) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF, UI>Browser>Navigation, UI>Browser>Omnibox |
| **Reporter** | gr...@hotmail.com |
| **Assignee** | de...@chromium.org |
| **Created** | 2016-10-28 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

On Chrome Version 54.0.2840.71 m (64-bit), I was able to spoof '<https://www.facebook.com:81>' for a good few seconds. We are able to modify the document and its title right before loading which could make it seem like the page navigated.

The same method could (theoretically) be used on web servers with a way to perform a DoS. Say '<https://www.facebook.com/someFile?some.function>' is vulnerable to a DoS attack where the response takes a longer time than usual, then we can use this trick to spoof that URI as well. Naturally a DDoS attack could work as well (which are pretty common these days)

Also, the document is active during this spoof which means we can have the user submit a fake login for example.

Potential fix: Do not change the URI on drag and drop, or at least set the document to 'about:blank' when this happens.

**VERSION**  

Chrome Version: 54.0.2840.71 + stable  

Operating System: Windows 8.1 64-bit

**REPRODUCTION CASE**  

View attached PoC.

## Attachments

- [wut.html](attachments/wut.html) (text/plain, 297 B)
- [wut.html](attachments/wut_53257044.html) (text/plain, 840 B)

## Timeline

### el...@chromium.org (2016-10-28)

Drag/drop seems like a low-risk vector; it'd be far more compelling if there was a way to get a spoof this without requiring that level of user-interaction.

We kinda need the URL to change in this scenario so that the user understands that something is happening in response to their action, but it does create a spoofing risk as reported in this report.

[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox]

### gr...@hotmail.com (2016-10-28)

Note: Loading random websites with non-existent ports takes ~20 seconds for Chrome to show a 'this page took too long' error msg. Which could still be enough time to trick some users. 

### gr...@hotmail.com (2016-10-28)

@elawre... I will try to see if I can find another way to trigger the behavior, with a lower level of user interaction. Will update you when I finish.

### cr...@chromium.org (2016-10-28)

I don't think there's likely to be anything we can do here.

Drag n drop is basically no different than having the page tell the user to "copy this link and paste it in the address bar."  When the user initiates any navigation in the address bar, we intentionally show that URL until it commits or fails, even if the navigation is slow.  It's true that the currently visible page can change its appearance during this time, but it doesn't have much control over where the user is trying to navigate.

Mitigating factors: the spinner is still going, and Chrome doesn't show the lock icon for HTTPS URLs until the pending URL commits.

Note that pages themselves can't initiate this attack on their own-- when they start a navigation, we don't show the pending URL until it commits.

Also note that navigations might not commit (e.g., they might turn out to be a download or 204 response, leaving you on the current page), so we can't clear the current page during a slow navigation.

Nasko or Peter, do you have any thoughts on improving what Chrome does here?  If not, I think this can be marked WontFix.

### gr...@hotmail.com (2016-10-28)

I had a hunch and it worked. Here is a PoC with _no user interaction_, again note that I'm using unavailable port to spoof 'http://www.facebook.com:83' for a few seconds, but this can be used on any website if the target website is vulnerable to D/Dos attacks (which includes most websites IMO).

Download new PoC attached.

### cr...@chromium.org (2016-10-28)

Interesting.  The approach in https://crbug.com/chromium/660498#c5 seems to work in Chrome 54.0.2840.59 (stable) but not Chrome 56.0.2903.0 (canary).  I wonder if it was fixed recently.

It looks like we were treating navigations from script code within embedded PDFs as browser-initiated, which would allow them to show up in the address bar.  Do any of the PDF folks know when that changed?  Maybe a bisect would help.

[Monorail components: Internals>Plugins>PDF]

### gr...@hotmail.com (2016-10-28)

Could you please change title?

### cr...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### na...@chromium.org (2016-10-28)

A quick bisect gives range of two CLs - https://chromium.googlesource.com/chromium/src/+log/a3c4a786757f0b365392d648e654f7cfda8c5b88..d9afdaaf5198350a06c484e4b7fbb3de50e3914a.

One of them (https://chromium.googlesource.com/chromium/src/+/374249e767a68d8da073a4ed3a4f29236451174c) is changing how PDFs navigate, so I'd suspect that is the root cause of the change in behavior. Adding rob@robwu.nl, as he was the author.

### cr...@chromium.org (2016-10-28)

Thanks Nasko.  I want to understand a few things about that fix, since it looks like it would be switching things from renderer-initiated (window.location.href) to browser-initiated (chrome.tabs.update), which would be the opposite of what I'd expect.

### ta...@google.com (2016-10-28)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-10-28)

My change changes the navigation method from location.href to chrome.tabs.update. Having the bug "fixed" is a side effect (and seemingly unexpected for the reason given by Charlie), but the root cause still exists.

To manually reproduce the issue (even in the latest version with my patch):

1. Visit data:text/html,<embed src="data:application/pdf,">
2. Inspect element of the PDF embed to open the JS console.
3. Run location.href = "http://facebook.com:83"

In the past I discovered that navigations initiated by the PDF plugin helper extension cause the tab to navigate. This may have something to do with the fact that the PDF extension helper is embedded in a guest view. The folks who own the guest view may know more.

Paul, Fady: Please take a look at this issue. Why is an omnibox spoof possible here?

### sh...@chromium.org (2016-10-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-29)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-10-30)

Hmm, also it seems better if chrome.tabs.update was guaranteed to behave the same as window.location.href in that the URL doesn't update until the page has actually navigated (I can't think of a good reason for it not to).

### ro...@robwu.nl (2016-10-31)

@raymes chrome.tabs.update behaves as expected.
location.href is behaving unexpectedly (=URL updates before actual navigation).

### ra...@chromium.org (2016-10-31)

Right, but in #10 creis mentioned that it was a browser-initiated navigation with the implication being that it should not behave in the way described in #15. I wanted to make sure that it should behave in the way described in #15. That is, that the URL doesn't update until the page has actually navigated.

### na...@chromium.org (2016-10-31)

The omnibox "spoof" in this report happens when the navigation is browser-initiated. In an existing window, only browser-initiated navigations will show the pending URL in the omnibox. You can see the logic in NavigationControllerImpl::GetVisibleEntry().

I don't fully understand why moving from location.href usage to chrome.tabs.update will result in fixing it, as chrome.tabs.update seems to be  a browser-initiated navigation (TabsUpdateFunction::UpdateURL calls NavigationController::LoadURL with no explicit parameter for renderer-initiated). If someone can debug through the two code paths to understand the difference, that would be awesome.

### ra...@chromium.org (2016-10-31)

paulmeyer: are you able to take a look? This is guest view + extensions related.

### pa...@chromium.org (2016-10-31)

[Empty comment from Monorail migration]

### wj...@chromium.org (2016-10-31)

[Empty comment from Monorail migration]

### lf...@chromium.org (2016-10-31)

I'll take a look.

### cr...@chromium.org (2016-11-02)

There's a lot of interesting aspects to this bug and how it is affected by recent CLs, so I'll try to lay out what we understand so far.  First off, thanks for the report!  It's clear that there were (and may still be) some issues with how navigations are handled within PDFs, and this is helping to find them.

1) In M54, the spoof works because the PDF's navigation is handled by an extension built into Chrome, which (at the time) used location.href to do the navigation.  It's an example of a "confused deputy" problem, where an untrusted PDF tricks the extension into doing something powerful on its behalf.  Specifically, extensions are generally given WebUI objects, and thus some code in NavigatorImpl::RequestOpenURL converts all of their renderer-initiated navigations into browser-initiated navigations.  (This conversion was meant for pages like the NTP and Bookmarks Manager, but it applied to all extensions.)  The spoof itself happens because we show pending URLs for browser-initiated navigations (like typing in the address bar) but not renderer-initiated navigations (like link clicks), as implemented in NavigationControllerImpl::GetVisibleEntry.  We could avoid showing the pending URL if we stop treating the navigation as browser-initiated.

2) In M55 and M56, Rob's r425287 changes the extension from using location.href to using the chrome.tabs API (to fix https://crbug.com/chromium/654279).  This approach doesn't appear to get treated as browser-initiated so we don't show the pending URL.  (Like comments 17-18, though, I'd like to verify how this happens in the code to be safe.)  Still, I think there's a bit of a tradeoff here-- I have the impression that the chrome.tabs API is more powerful and is allowed to navigate to more URLs than location.href (e.g., chrome:// URLs).  This means we'd be at higher risk for confused deputy attacks, with only isValidUrl_ in navigator.js to prevent it.  I haven't spotted any concrete problems there yet, but it seems a bit concerning.  It also looks like navigator.js will fall back to using location.href in some cases, which may mean we're still vulnerable to the URL spoof.

3) What's really interesting is that Devlin landed r428747 (removing WebUI objects from most extensions for https://crbug.com/chromium/659798) just yesterday!  This also would have been a sufficient fix, since it means we don't convert the navigation from renderer-initiated to browser-initiated, and thus we don't show the pending URL.  In fact, it may be a bit better, since there's no risk to falling back to location.href in some cases.  However, I'm still not sure if it will get reverted for breaking any existing extensions.  Thus, it's probably too risky to merge to M55.

Overall, it looks like M56 is pretty well protected with the combination of the two CLs, assuming they both stick.  I'd like to better understand whether M55 is safe with just Rob's fix, since it depends on not falling back to the location.href path (which looks like it might be possible in some cases).  I'd also like to verify that isValidUrl_ provides sufficient defense against other confused deputy attacks, where the PDF tries to navigate to URLs it shouldn't be allowed to.

Once we verify a few of these things, I'm guessing it will be safe to mark this as fixed.

### lf...@chromium.org (2016-11-02)

Re #23:

For 2), the change to use chrome.tabs API changes the navigation code path from going through MimeHandlerViewGuest::OpenURLFromTab to using extensions::TabsUpdateFunction::UpdateURL, which directly navigates the WebContents (https://cs.chromium.org/chromium/src/chrome/browser/extensions/api/tabs/tabs_api.cc?l=1323).

By navigating directly, we bypass the WebContentsDelegate which normally updates the UI in https://cs.chromium.org/chromium/src/chrome/browser/ui/browser_navigator.cc?l=573. As you noted, switching to another tab and back updates the UI and causes the spoof to happen even with the chrome.tabs API.

I think Devlin's change remove the WebUI from this RFH is the proper long-term fix, but if it's too dangerous for merging into M55 we could consider overriding the is_renderer_initiated parameter in MimeHandlerViewGuest::OpenURLFromTab.


### lf...@chromium.org (2016-11-02)

Actually, my idea above doesn't work for chrome.tabs API, since chrome.tabs API bypasses everything and goes directly to NavigationControllerImpl::LoadURL, which treats all navigations as browser initiated.

Any navigations using the chrome.tabs API will be vulnerable to this type of spoof.


### cr...@chromium.org (2016-11-02)

Comments 24-25: Yes, that's what I was afraid of with the confused deputy aspect of the problem.  It's not safe for the Mime Handler extension to use the chrome.tabs API on behalf of untrusted PDFs, and Devlin's CL doesn't protect us because we're still using chrome.tabs in most cases (which is treated as browser-initiated, as you note).

To say it explicitly, the spoof is still possible on Canary if you switch to another tab and then back while the pending navigation is still in progress.  The only reason it isn't happening by default is because we're bypassing NotifyNavigationStateChanged in tabs_api.cc, and thus not repainting the omnibox.  This is a little bit less effective as a spoof, but still a concerning problem.

One possibility is switching all chrome.tabs navigations to be considered renderer-initiated as well, by using LoadURLWithParams instead of LoadURL.  I don't know what compatibility impact that will have, though.  Devlin, is there a way to tell whether this is feasible?

Another possibility might be switching the extension's navigator.js away from using chrome.tabs entirely, and then relying on Devlin's WebUI CL to have the navigations treated as renderer-initiated.  Can someone comment on whether the Mime Handler extension would be able to do that?

### lf...@chromium.org (2016-11-02)

Re #26: I don't think we can switch navigator.js entirely away from chrome.tabs without breaking file:// to file:// navigations. Just adding the parameter back (that was removed in Rob's CL) also wouldn't work, as it would allow spoofs from file:// URLs.

Changing all chrome.tabs navigations to be treated as renderer-initiated is interesting, I tried and it seems to work (minus a DCHECK that can probably be removed in TabsUpdateFunction::UpdateURL). I wonder if that would break anything.


### ro...@robwu.nl (2016-11-02)

Have you also tried to open chrome-pages such as chrome://downloads? There are multiple addon that just open such kind of pages, and normally navigation to chrome: from a web page is forbidden.

### lf...@chromium.org (2016-11-02)

Re#28: That gets blocked in navigator.js isValidUrl_. I'm not a fan of doing those security checks in the renderer process, but in this case the renderer is privileged, as it's hosting the pdf extension.



### ro...@robwu.nl (2016-11-02)

@29 In #27 you said changing all chrome.tabs calls to renderer-initiated. Did you mean the extension ApI (which I assumed, and would also affect third-party extensions), or the PDFium extension?

### lf...@chromium.org (2016-11-02)

I meant the extension API. It would definitely affect other extensions, but would it actually break any real world usage?


### ro...@robwu.nl (2016-11-02)

#31 If navigations to chrome:// URLs or file:// URLs are no longer possible in Chrome extensions, then yes, real-world extensions would be affected.

There are extensions in the CWS that open chrome://downloads, chrome://extensions and others. I surely encountered them when I reviewed/audited Chrome extensions.

### lf...@chromium.org (2016-11-02)

The is_renderer_initiated param doesn't seem to be used to block any navigations to chrome:// or file:// URLs, so those navigations would still work, but it might be used for other things that could break.

Maybe Charlie or Devlin could have some ideas?


### rd...@chromium.org (2016-11-02)

My guess is that would break things, but it's hard to say for sure without knowing exactly what the differences are.  Charlie mentioned in #23 that

> I have the impression that the chrome.tabs API is more powerful and is allowed to navigate to more URLs than location.href (e.g., chrome:// URLs)

which implies that renderer-initiated navigations to chrome:// urls would fail, so there's already some confusion around what this actually allows.  (FWIW, I can confirm that just clicking on an <a href="chrome://settings"> doesn't work - so there is logic there somewhere.)  If we can lay out exactly what the privilege differences are between renderer- and browser-initiated navigations, that would help.

Overall, though, my suspicion is that it *will* break valid use cases for extensions.  In a simple case, a session restorer basically needs to be able to open any tab, so if there are any tabs that renderer-initiated navigations *wouldn't* open, that would break.

### cr...@chromium.org (2016-11-03)

Ok, I've been investigating, and I think Lucas's idea makes sense.  It appears that the is_renderer_initated bit is not what determines whether the chrome.tabs API is allowed to navigate to chrome:// URLs, so that will continue to work.  It will affect whether the pending URL is visible in the omnibox, which is good for preventing the spoof.  I also don't think that will be much of a regression for existing extensions, since we don't refresh the omnibox anyway (unless you switch tabs and come back).

I'm giving this a try at https://codereview.chromium.org/2475033002/, to see what the bots think.  We'll want to sanity check that nothing else is broken by this, but I think it may be a reasonable way forward.

(To be clear, location.href wasn't allowed to go to chrome:// URLs before or after Devlin's removal of WebUI for extensions, and chrome.tabs API is allowed to go to chrome:// URLs whether it's classified as browser-initiated or renderer-initiated.)



### cr...@chromium.org (2016-11-03)

Hmm, the CL is failing the ExtensionApiTest.Tabs2 test, which tries to check the tab's URL immediately after starting the load.  This is not a good practice in general, and I'm disappointed we're exposing GetVisibleURL in the tabs API rather than GetLastCommittedURL.  Still, it's possible that some extensions may make a similar check (in which case their code is going to be fragile for other reasons).

I'll try to discuss this with Devlin on the CL.

### bu...@chromium.org (2016-11-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2097de33a1f3d04e78d93e9e2f16aad4b97e47d7

commit 2097de33a1f3d04e78d93e9e2f16aad4b97e47d7
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Sat Nov 12 01:29:11 2016

[Extensions] Don't show the pending URL for chrome.tabs API navigations

For the pdf extension, treat navigations as renderer-initiated. Ideally,
we want this to become default for all extensions, but that risks
breakage.

Based on creis@'s patch at https://codereview.chromium.org/2475033002/.

BUG=660498
TEST=See bug for repro steps.

Review-Url: https://codereview.chromium.org/2492863003
Cr-Commit-Position: refs/heads/master@{#431726}

[modify] https://crrev.com/2097de33a1f3d04e78d93e9e2f16aad4b97e47d7/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/2097de33a1f3d04e78d93e9e2f16aad4b97e47d7/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc
[modify] https://crrev.com/2097de33a1f3d04e78d93e9e2f16aad4b97e47d7/chrome/browser/extensions/api/tabs/tabs_test.cc
[add] https://crrev.com/2097de33a1f3d04e78d93e9e2f16aad4b97e47d7/chrome/test/data/extensions/api_test/tabs/pdf_extension_test.html


### cr...@chromium.org (2016-11-14)

Looks like this is fixed in version 56.0.2917.0 (just confirmed in 56.0.2919.0).  Thanks for the report, and to Devlin for landing the fix (which was narrowed to the PDF extension)!

I'm marking it fixed since we're safe on trunk.  I'm not thrilled about relying on isValidUrl_ against other confused deputy issues, but we're probably ok for now.  Too late for M54, but we may want to consider merging to M55.

Since Rob's r425287 is already on M55, I think we just need to merge Devlin's recent r431726.  The WebUI removal work in r428747 would be useful if we knew of exploitable cases that the PDF extension falls back to location.href, but maybe it's ok to wait for M56 for that one.

Devlin, do you agree?  If so, let's request a M55 merge.

### rd...@chromium.org (2016-11-14)

Yep, sgtm.  Requesting merge.

### di...@chromium.org (2016-11-14)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### sh...@chromium.org (2016-11-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/50cfe8d0926f013a794afe49e39cc48fe2e3848b

commit 50cfe8d0926f013a794afe49e39cc48fe2e3848b
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Tue Nov 15 14:57:56 2016

[Extensions] Don't show the pending URL for chrome.tabs API navigations

For the pdf extension, treat navigations as renderer-initiated. Ideally,
we want this to become default for all extensions, but that risks
breakage.

Based on creis@'s patch at https://codereview.chromium.org/2475033002/.

BUG=660498
TEST=See bug for repro steps.

Review-Url: https://codereview.chromium.org/2492863003
Cr-Commit-Position: refs/heads/master@{#431726}
(cherry picked from commit 2097de33a1f3d04e78d93e9e2f16aad4b97e47d7)

Review URL: https://codereview.chromium.org/2506463003 .

Cr-Commit-Position: refs/branch-heads/2883@{#573}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/50cfe8d0926f013a794afe49e39cc48fe2e3848b/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/50cfe8d0926f013a794afe49e39cc48fe2e3848b/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc
[modify] https://crrev.com/50cfe8d0926f013a794afe49e39cc48fe2e3848b/chrome/browser/extensions/api/tabs/tabs_test.cc
[add] https://crrev.com/50cfe8d0926f013a794afe49e39cc48fe2e3848b/chrome/test/data/extensions/api_test/tabs/pdf_extension_test.html


### bu...@chromium.org (2016-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6c0d227bc9eae0114258f6ad1e00973dda4d424d

commit 6c0d227bc9eae0114258f6ad1e00973dda4d424d
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Tue Nov 15 22:34:22 2016

[Extensions] Add missing include

Fix failure from crrev.com/2097de33a1f3d04e78d93e9e2f16aad4b97e47d7

BUG=665517
BUG=660498
NOTRY=true (cast_shell_linux flaking out of control)

Review-Url: https://codereview.chromium.org/2502063002
Cr-Commit-Position: refs/heads/master@{#432274}

[modify] https://crrev.com/6c0d227bc9eae0114258f6ad1e00973dda4d424d/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc


### bu...@chromium.org (2016-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3f28bcf03c189df58ea901477706aad2b5b355dd

commit 3f28bcf03c189df58ea901477706aad2b5b355dd
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Tue Nov 15 22:46:27 2016

[Extensions] Add missing include

Fix failure from crrev.com/2097de33a1f3d04e78d93e9e2f16aad4b97e47d7

BUG=665517
BUG=660498

Review-Url: https://codereview.chromium.org/2502063002
Cr-Commit-Position: refs/heads/master@{#432274}
(cherry picked from commit 6c0d227bc9eae0114258f6ad1e00973dda4d424d)

Review URL: https://codereview.chromium.org/2504513003 .

Cr-Commit-Position: refs/branch-heads/2883@{#579}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/3f28bcf03c189df58ea901477706aad2b5b355dd/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc


### aw...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

The panel decided to award $2,000 for this bug!

### gr...@hotmail.com (2016-11-30)

Thank you for the generous bounty :)

### aw...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/660498?no_tracker_redirect=1

[Multiple monorail components: Internals>Plugins>PDF, UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085816)*
