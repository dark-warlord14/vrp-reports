# iOS: URL spoofing due to pages that commit but take a long time to paint

| Field | Value |
|-------|-------|
| **Issue ID** | [40052164](https://issues.chromium.org/issues/40052164) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Platforms** | iOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2020-04-30 |
| **Bounty** | $1,000.00 |

## Description

This URL spoofing works best for the users who have the slow internet. 

URL updates the omnibox before updating/blocking the content. 

## Attachments

- [spoof.html](attachments/spoof.html) (text/plain, 545 B)
- [attacker.html](attachments/attacker.html) (text/plain, 18 B)
- [Spoof for slow internet.mp4](attachments/Spoof for slow internet.mp4) (video/mp4, 210.5 KB)
- [Safari.mp4](attachments/Safari.mp4) (video/mp4, 1.1 MB)
- [TwitterSpoof (1).mp4](attachments/TwitterSpoof (1).mp4) (video/mp4, 2.4 MB)
- [ContentBug.mp4](attachments/ContentBug.mp4) (video/mp4, 5.2 MB)

## Timeline

### pa...@chromium.org (2020-04-30)

We are showing the attacker content while showing "accounts.google.com" in the Omnibox. That does seem wrong.

It seems mitigated (down to Medium, per https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md) by the fact that the attacker is limited by how much they can get out of the defender during a time frame the attacker does not control. (I.e. yes, it would work better for slow connections/slow pages).

Could a navigation and/or secure UX expert please take this one? Thank you!

[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox UI>Browser>Omnibox>SecurityIndicators]

### cr...@chromium.org (2020-04-30)

palmer@: Where did you repro it?  I'm having trouble getting it to work on Windows (Canary 84.0.4131.0 or Stable 81.0.4044.129).  Looks like it's getting blocked for a cross-origin frame access.

I also note that we don't show the pending URL for history.back/forward or the back button on Windows, using the following repro steps:
1) Visit http://csreis.github.io/tests/window-open.html
2) Click "Open about:blank window"
3) In DevTools of the original tab, run w.location.href = "http://tests.netsekure.org/slow.php?seconds=5"
4) After it commits, in DevTools of the original tab, run w.location.href = "simple.html"
5) Clear cache from the last hour to make the slow URL load again from the network.  (Or, open DevTools in the new tab and disable cache on the Network panel.)
6) In DevTools of the original tab, run w.history.back()


Is this a platform specific bug?  Maybe it's iOS specific?

### es...@chromium.org (2020-04-30)

Tentatively removing non-iOS labels since the video is iOS. Seems unlikely to be cross-platform. Adding some iOS people who might be able to repro and help triage.

### es...@chromium.org (2020-04-30)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>Omnibox>SecurityIndicators]

### pa...@chromium.org (2020-05-04)

I tried it out on Chrome OS, but I think I misinterpreted what I was seeing. What I can repro now (internal URL: fainting.sfo/spoof) doesn't exhibit any actual spoofy behavior (the origin shown in the Omnibox is always correct).

### cr...@chromium.org (2020-05-04)

Thanks.  eugenebut@: Are you able to repro on iOS, and can you route it in the right direction if so?  See my https://crbug.com/chromium/1076874#c2 for context.

### eu...@chromium.org (2020-05-04)

[Empty comment from Monorail migration]

### ga...@chromium.org (2020-05-05)

I can reproduce on a bad network, but the content of the page is not interactable (i.e. we see the attacker content but buttons and text fields are disabled). This is a know limitation of WebKit.
rayyanh12@: Do you confirm that this is the behaviour reported here?

### ra...@gmail.com (2020-05-05)

C#8: Yes. You're Correct. 

### ga...@chromium.org (2020-05-05)

creis@: Assigning it back to you for security assessment.
This is the default behaviour on most webpages on iOS (i.e. the URL changes and the content of the page is still there but it is impossible to interact with it).

### cr...@chromium.org (2020-05-05)

gambard@: Thanks.  It sounds like WebKit and desktop Chrome differ in whether they make the content of the page non-interactive, and maybe that's ok.

Still, we would have control over what Chrome on iOS shows in the address bar, right?  Is there a reason to show the pending URL for back/forward navigations, when we don't do that on desktop Chrome?  Seems like it should be safe to avoid that (in addition to WebKit's non-interactive page), and there may be some value in that for cases where the attacker's page puts up a message for the user to read, like a phone number to call.

If it helps for experimenting, I put together some of the steps in http://csreis.github.io/tests/slow-links.html, but you'll need a way to clear the cache before going back/forward to the slow URL.

### ga...@chromium.org (2020-05-06)

I am not able to reproduce the issue when navigating back/forward (i.e. the page is blank).
My steps are:
1. Navigate to http://csreis.github.io/tests/slow-links.html
2. Tap on the "Slow URL in this frame" link
3. Here the URL stays the same until the pending navigation is committed and the page is unchanged
4. Go back
5. Clear site data
6. Navigate forward
7. Here the page is blank but the URL is updated to the pending URL right away *OR* the URL is only updated when the navigation is committed (it actually depends on our restoration mechanism, one of them is loading a blank page before redirecting to the right URL, so we are sure that there is a blank page visible when the URL is updated).

Also, I am not sure to see how it relates to the original bug. Do you have an example where this is a concern?

### cr...@chromium.org (2020-05-06)

Ok, I found an iOS device to test on.  There's some trickiness to manually repro which is likely due to WebKit's back/forward cache, but it looks like you're right that Chrome doesn't show the pending URL on (most?) history navigations.  That makes me confused about the original repro and your https://crbug.com/chromium/1076874#c8, where the pending history navigation's URL appears to be displayed over the attacker's (non-interactive) content.  That's the case I'm concerned about-- even if it's non-interactive, it would be better not to show the pending history navigation's URL, and I'm unclear why we do it in the repro case but not in the steps on my test page.

In more detail:

Nasko and I have updated the slow URL to not be cacheable anymore, but that doesn't seem to prevent it from ending up in WebKit's back/forward cache.  However, navigating to a few other sites in the tab does seem to evict it from the back/forward cache, so that you can see the effect of a slow back/forward without having to clear site data.

Repro steps for the attack that I expected to work, but which actually prove that we don't show the pending history URL:
1. Navigate to http://csreis.github.io/tests/slow-links.html
2. Tap on the "window.open to slow URL in named popup" button.
3. The URL stays about:blank until it commits.  (Tangent: We decided to show the pending URL here on desktop in https://crbug.com/chromium/9682, but that's tricky to do safely and not important at the moment for iOS to implement.)
4. In the original tab, tap on the "Go same-origin in named popup" button.
5. In the new tab, to clear the back/forward cache, navigate to google.com, then chromium.org, then go back twice to simple.html.
6. In the original tab, tap on the "Go back in named popup" and immediately switch to the new tab.

At this point, there's a pending session history navigation to the slow URL, but we're still showing csreis.github.io in the address bar and not blanking out the content.  That's great.

I think we've just simulated steps 1-3 in the attached spoof.html.  I'm not sure whether step 4 makes a difference, but maybe that's triggering something that causes the victim URL to be displayed in the video?  I tried adding a similar "Go forward in named popup and interrupt" button to the test page, but it doesn't create a successful repro.

gambard@: If you're able to repro the original attack, can you take a look at why the pending URL is shown in that case but not the steps I've mentioned above?  My goal is that we don't show the pending URL there.  That said, I'm lowering this to Low severity given the additional mitigation that the page content is apparently non-interactive, and since the repro sounds like it may be unreliable (per https://crbug.com/chromium/1076874#c8).

### ga...@chromium.org (2020-05-07)

We update the visible URL when the navigation is committed (i.e. we start receiving data from the server). It is a WebKit feature that the previous page is still displayed (to avoid having to look at a blank page), and we have no control over it. We don't have any callback that would indicate "the previous page is no longer displayed".
I think this is also what all other platforms are doing (i.e. show the pending navigation as visible URL once it is committed).

### [Deleted User] (2020-05-07)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2020-05-07)

https://crbug.com/chromium/1076874#c14: Let's compare this to the video, just to make sure I understand you.  At 0:07, the address bar changes to accounts.google.com and a blue progress bar is shown, while the page still says "Attacker content" until 0:14.  I was under the impression that those 7 seconds were spent waiting for the network, with the back navigation pending and the pending URL visible.  Instead, it sounds like the back navigation actually committed at 0:07, making the URL visible, but it took another 7 seconds for the old page to start rendering and replace the painted image of the old page?

I'm surprised it takes that long for WebKit to stop showing the old page.  In desktop Chrome, we did implement a 4 second timer that blanks out the old page after a commit if no new paint has arrived by then.  (CC'ing kenrb@ for FYI.)  Not sure if that's feasible on iOS or not?  If it turns out that this spoof is due to WebKit's delayed rendering and not due to showing the pending URL, then it seems like we either add a paint timer, ask WebKit to change something, or WontFix.

Reporter: Does this affect Safari as well?

### ra...@gmail.com (2020-05-07)

In Safari, you cannot only spoof the content but the content is intractable and purely spoofable. 

### ra...@gmail.com (2020-05-07)

https://crbug.com/chromium/1076874#c17, It's the word *Interactive* not  intractable* --> The Content area is active too.

### eu...@chromium.org (2020-05-07)

[Empty comment from Monorail migration]

### ra...@gmail.com (2020-05-09)

[Comment Deleted]

### ra...@gmail.com (2020-05-09)

I don't know if you guys noticed but the SSL indicator (along with the URL)  does not reflect the contents of the current document window for as long as the website loads properly.

### ga...@chromium.org (2020-05-11)

https://crbug.com/chromium/1076874#c16: As a regular user of both Safari and Chrome, the old content being displayed and not interactable (for longer than 4s) is something I used to see daily in the metro.
From my tests, in that video the navigation is committed at 0:07 and the repaint of the new page happens at 0:14. Which is coherent with #9 as the content is not interactable during this time (the content is interactable until URL is committed).

I don't think it is possible to add a re-painter on Chrome.

For the SSL indicator I know, but it should always become less secure.

### ga...@chromium.org (2020-05-11)

https://crbug.com/chromium/938221 is the one tracking the radar.

### cr...@chromium.org (2020-05-14)

https://crbug.com/chromium/1076874#c22-23: Thanks!  I agree that having WebKit clear the page at commit time (https://crbug.com/chromium/938221) would be sufficient, but we don't do that in Blink either, so I'm not sure if it will get fixed.  With Blink/content, the old paint does stay visible for up to 4 seconds after the browser process hears about the navigation commit, until RenderWidgetHostImpl::new_content_rendering_timeout_ kicks in.  At that point, we call RenderWidgetHostImpl::ClearDisplayedGraphics() to clear the old paint.

Just curious, what's the limiting factor for doing a similar timer-based repaint in Chrome for iOS?  I suppose we probably don't have the ability to tell WKWebView to clear its painted image?  We don't have that for Blink either, but we control the compositing in the browser process perhaps more than in Chrome for iOS.  Putting a white overlay over the WKWebView might be possible (or hiding the WKWebView?), but I'm guessing that's probably fraught with issues (e.g., knowing when to show the WKWebView again, UI issues, etc).

Anyway, given that this particular issue is confirmed to be about the time between commit and first paint, I'm pretty sure it isn't limited to back/forward and could happen with navigating to any URL that is slow to paint.  Updating summary accordingly.  Whether we can do anything seems blocked on the WebKit radar issue, so I'll mark this as having an external dependency (unless you think there's a way to hide the old page without depending on that).

### eu...@chromium.org (2020-05-14)

We can't tell WKWebView to clear the paint. We could place a white overlay between webView:didCommitNavigation: and webView:didFinishNavigation: callbacks if navigation has changed the origin, but this may cause bugs in edge cases.

### cr...@chromium.org (2020-05-14)

I agree it sounds tricky to get right without more awareness of the WKWebView paint timing.  I'm not sure if webView:didFinishNavigation is the same as WebContentsObserver::DidFinishNavigation, but the latter happens after the new page has finished loading. If so, we wouldn't show any of the incremental paints as the page renders, if the overlay was shown that long (affecting perception of page load time).  In Blink/content, we're able to show the first new paint as soon as it arrives, and I'm guessing we won't get a notification of that from WKWebView.

### eu...@chromium.org (2020-05-14)

webView:didCommitNavigation: is similar to WebContentsObserver::DidFinishNavigation (except that webView:didCommitNavigation: in not called for same-document navigations or if the page was loaded from back-forward cache). webView:didFinishNavigation: is similar to WebContentsObserver::DidFinishLoad.

In WKWebView new paint usually arrives some time after webView:didFinishNavigation:

### ga...@chromium.org (2020-05-20)

[Empty comment from Monorail migration]

### ga...@chromium.org (2020-05-20)

Assigning to creis as it is a security decision.

### cr...@chromium.org (2020-05-20)

https://crbug.com/chromium/1076874#c29: Sorry, I'm unclear-- which security decision do I need to reply about?  I tried to update the status in https://crbug.com/chromium/1076874#c24, indicating that this issue is blocked on an external dependency on WKWebView (in https://crbug.com/chromium/938221).  In comments 25-27, we've confirmed that Chrome for iOS appears unable to clear the stale painted content without significant UX downsides (e.g., not being able to show the new page as soon as it starts painting).  Thus, it appears we're dependent on WKWebView to more effectively clear the stale paint, possibly after a delay.

I don't have access to the Radar issue in https://crbug.com/chromium/938221 and I'm not involved with the discussions to improve WKWebView, so I'm probably not the right owner for this bug.  Can we assign this to someone following the Radar issue?  Let me know if there's another question I need to weigh in, on though!

### ga...@chromium.org (2020-05-20)

It is unclear because I forgot to actually ask the question... :D
The questions were:
1. Should we consider this a security issue?
2. Should we just dupe it in https://crbug.com/chromium/938221?

Also, if you want to access the radar: go/applebugs (no required, we are tracking it).

### ra...@gmail.com (2020-05-20)

[Comment Deleted]

### ra...@gmail.com (2020-05-20)

Adding my part from the security perspective by providing an attack scenerio; copying my comment from here; https://bugs.chromium.org/p/chromium/issues/detail?id=1083337#c7

there could be some cases where the attacker's page puts up a message for the user to read, like a phone number to call. In the end attacker wants to make sure user is convinced by his hacking skills. For eg; he can put up a message "Twitter.com is hacked by me  - If you want to hack any social media accounts Contact me on this number - $5000 for one account." - Attacker can fool many users out there since people are  crazy out there to pay thousands of bucks to have someone to hack others accounts. Using this bug, attacker can convince them paying into thousands of bucks.

### ke...@chromium.org (2020-05-20)

We have historically treated these as security issues in desktop and Android Chrome, basically for the reason cited in https://crbug.com/chromium/1076874#c33.

I think duping these into a single bug makes sense since there I'd expect that there is going to be a single fix for all of them.

### ra...@gmail.com (2020-05-21)

[Comment Deleted]

### ra...@gmail.com (2020-05-21)

https://crbug.com/chromium/1083838 is about producing the concept in incognito mode; and the behavior was consistent that I wasn't able to create a spoofed page on normal mode and did it in incognito mode with same internet speed and at the same time. Although it's weird I can reproduce the same bug on normal mode too now. Which means this https://crbug.com/chromium/1083838 isn't consistent. If this was WKWebView bug; the spoofing vector should be consistent, right? which mean all these bug are treatable. Maybe?

Attaching the same video from https://crbug.com/chromium/1083838 for your ease.

Chrome version: 81 - iOS version: 13.3.1

### ra...@gmail.com (2020-05-22)

[Comment Deleted]

### ra...@gmail.com (2020-05-22)

https://crbug.com/chromium/1081081: Safari vs chrome v81 (iOS 13.3.1) which means these are fixable? Since I couldn't reproduce the same in Safari.

### cr...@chromium.org (2020-06-06)

Sorry for the delay.

https://crbug.com/chromium/1076874#c31-34:
Yes, not clearing the previous page's paint after a cross-origin commit is a security issue.  I would personally suggest leaving this open as an external dependency, blocked on https://crbug.com/chromium/938221, allowing this to be resolved when that gets fixed.  (I'm not too opposed to kenrb's suggestion to dupe them all into the same bug, but I think it's worth checking the repro steps from each of the bugs against the WebKit fix when it arrives.  If we dupe too many into the same bug, it's possible we might not notice if some of them aren't addressed.)

Someone from the Chrome for iOS team should try to drive https://crbug.com/chromium/938221 to a resolution, because multiple bugs are dependent on it.  I'll remove myself as owner from this, since I'm not involved with that fix nor working on this one.

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### eu...@chromium.org (2021-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ra...@gmail.com (2021-07-05)

[Comment Deleted]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### aj...@chromium.org (2023-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1076874?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail blocked-on: crbug.com/chromium/938221]
[Monorail mergedwith: crbug.com/chromium/1083838, crbug.com/chromium/1484993]
[Monorail components added to Component Tags custom field.]

### mi...@google.com (2024-06-13)

Re [#comment40](https://issues.chromium.org/issues/40052164#comment40), the blocking bug was closed as fixed, so this should be re-tested now.

### ti...@chromium.org (2025-01-16)

(primary shepherd)

I was unable to reproduce on an IOS 18 device with the fix. However, given that this bug is so old there is a chance that the poc just doesn't apply anymore either. [rayyanh12@gmail.com](mailto:rayyanh12@gmail.com) if you are able to reproduce with a modified poc or find a variant please open a new bug. Thanks again for the report!

### pe...@google.com (2025-01-16)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pe...@google.com (2025-01-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-01-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-23)

Thank you for your efforts and reporting this issue to us!

### ch...@google.com (2025-04-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052164)*
