# Security: Possible to navigate to extension resources not listed in web_accessible_resources

| Field | Value |
|-------|-------|
| **Issue ID** | [40051315](https://issues.chromium.org/issues/40051315) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | tj...@chromium.org |
| **Created** | 2020-01-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Typically, it's not possible to navigate to an extension resource not listed under web\_accessible\_resources. However, if a page opens an inaccessible resource in a new window, navigates the window to another page and then navigates back, the original extension resource will be loaded.

**VERSION**  

Chrome Version: Tested on 79.0.3945.130 (stable) and 81.0.4034.0 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. Install uBlock Origin.
2. Open the attached page (index.html).
3. When you click on this page, it will perform the following steps:

var newWindow = open("chrome-extension://cjpalhdlnbpafiamejdnhcphjbkeiagm/dashboard.html");

setTimeout(() => {  

newWindow.location.href = "about:blank";

```
setTimeout(() => {  
    newWindow.history.back();  
}, 1000);  

```

}, 1000);

Note that the extension resource will fail to load when the window is initially opened, it will load once the window has been navigated back at the end of the process.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [index.html](attachments/index.html) (text/plain, 657 B)

## Timeline

### ct...@chromium.org (2020-01-21)

Thanks for the report. Tentatively setting Severity-Medium as this potentially exposes extension resources to attacks by websites (e.g., site can pass input data via query params, and this could maybe be used to pass POST requests as well but I'm not sure).

rdevlin.cronin@ could you take a look? Thanks!


[Monorail components: Platform>Extensions]

### rd...@chromium.org (2020-01-24)

Ooh, fun!  Good find!

Alex, do you know if we treat navigations from history.back() as renderer-initiated?  If not, that's probably the root cause.  Otherwise, we'll have some more digging to do.

I don't know if I'll have a chance to dig into this in the near future, so also cc'ing tjudkins@ who might take it over depending on the path forward.

### al...@chromium.org (2020-01-24)

I think history.back() is actually a browser-initiated navigation (Devlin, is that what you meant?).  That seems to explain the problem here: the initial window.open navigation to a non-WAR is renderer-initiated and so it is blocked, then the history.back() is treated as a browser-initiated navigation, which bypasses the WAR checks.

Now, if I were to press the back button manually, I'd expect the non-WAR to load - same as if I were to type its URL into the omnibox (since it's me and not the web page trying to load the resource).  The problem is that today I don't think we can tell apart browser vs renderer-initiated session history navigations.  This is something I think we've been wanting to fix in the navigation code for some time but haven't yet.

[Monorail components: UI>Browser>Navigation]

### lu...@chromium.org (2020-01-24)

I wonder if the |initiator_origin| is replayed during the history navigation.  I believe it should be replayed (this is what we want for Sec-Fetch-Site - see r677046 and the SecFetchBrowserTest.BackNavigation test this CL added).  It the |initiator_origin| is indeed replayed, then we should be able to use it to decide to block the navigation (even if the navigation is marked as browser-initiated).

### lu...@chromium.org (2020-01-24)

I wonder what would break if we've tweaked ExtensionNavigationThrottle::WillStartOrRedirectRequest to look at the initiator origin instead:

OLD:
  // Browser-initiated requests are always considered trusted, and thus allowed.
  //
  // Note that GuestView navigations initiated by the embedder also count as a
  // browser-initiated navigation.
  if (!navigation_handle()->IsRendererInitiated())
    return content::NavigationThrottle::PROCEED;

NEW:
  // Navigations with no initiator (e.g. browser-initiated requests) are always considered trusted, and thus allowed.
  //
  // Note that GuestView navigations initiated by the embedder also count as a
  // browser-initiated navigation.
  if (!navigation_handle()->GetInitiatorOrigin().has_value())
    return content::NavigationThrottle::PROCEED;

### rd...@chromium.org (2020-01-24)

Good question.  I wonder what the other situations are in which the initiator origin has no value - can you think of others off the top of your head?

(Also, do you want to take a stab at this one, since you've already started thinking about it? :)  If not, Tim can probably take a look)

### al...@chromium.org (2020-01-24)

If you're looking to debug this, I think history.back() would go through LocalFrameClientImpl::NavigateBackForward() -> LocalFrameHost::GoToEntryAtOffset() -> RenderFrameHostImpl::GoToEntryAtOffset(), and then the WAR check that skips browser-initiated navigations is at https://cs.chromium.org/chromium/src/extensions/browser/extension_navigation_throttle.cc?l=130&rcl=23e3babcce528fc43321b6f35db21b99a24f63ee.  Maybe there's something else we can check there besides !NavigationHandle::IsRendererInitiated(), like for example if there's a user gesture.  Not sure how easy/practical it would be to convert history.back() etc to renderer-initiated navigations.

### al...@chromium.org (2020-01-24)

Ah, sorry, didn't see the previous posts before posting https://crbug.com/chromium/1043965#c7.  Checking the initiator origin seems like a good direction to me!

### lu...@chromium.org (2020-01-24)

RE: https://crbug.com/chromium/1043965#c6: do you want to take a stab at this one

I can help review, but I probably won't be able to take a closer look until late next week :-(

### rd...@chromium.org (2020-01-25)

-> Tim.  Sounds like a good first step might just be to make the change in #5, run it through the try bots, and see a) if it fixes the issue here and b) if anything else breaks. :)

### tj...@chromium.org (2020-01-25)

The change seems to fix it when trying to reproduce locally. Running it through the try bots now and will need to find a good place to put in a test for this case.

Is there anything we will need to cover for the case mentioned in the comment about the GuestView navigations initiated by the embedder?

### lu...@chromium.org (2020-01-27)

Thanks for helping with this bug!

RE: https://crbug.com/chromium/1043965#c11: Is there anything we will need to cover for the case mentioned in the comment about the GuestView navigations [...]

I don't know.  I hope that the WebViewTest.NavigateGuestToWebviewAccessibleResource test provides sufficient coverage here.

RE: https://crbug.com/chromium/1043965#c11: will need to find a good place to put in a test for this case

Maybe we can add a new testcase somewhere in chrome/browser/extensions/extension_resource_request_policy_apitest.cc?



### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0a8dee3cfe1957b2c632142051c863cb37e7b920

commit 0a8dee3cfe1957b2c632142051c863cb37e7b920
Author: Tim Judkins <tjudkins@chromium.org>
Date: Fri Jan 31 01:45:22 2020

[Extensions] Check for initiator origin in ExtensionNavigationThrottle.

Changes one of the checks in ExtensionNavigationThrottle to check if the
initiator origin of a navigation is empty, to more correctly handle
history.back() being used to navigate a window. Adds tests to cover this
case.

Also adds a test for a similar case which navigates a local frame, which
results in the navigation being blocked at the renderer level.

Bug: 1043965
Change-Id: I63e7e6775dbc56afdf3cd96452bf59939202370e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2021194
Commit-Queue: Tim Judkins <tjudkins@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Cr-Commit-Position: refs/heads/master@{#737162}

[modify] https://crrev.com/0a8dee3cfe1957b2c632142051c863cb37e7b920/chrome/browser/extensions/extension_resource_request_policy_apitest.cc
[modify] https://crrev.com/0a8dee3cfe1957b2c632142051c863cb37e7b920/chrome/test/data/frame_tree/page_with_two_frames_remote_and_local.html
[modify] https://crrev.com/0a8dee3cfe1957b2c632142051c863cb37e7b920/extensions/browser/extension_navigation_throttle.cc


### tj...@chromium.org (2020-01-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-31)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-03)

Requesting merge to beta M80 because latest trunk commit (737162) appears to be after beta branch point (722274).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-02-03)

This bug requires manual review: We are only 0 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-02-03)

pls answer questions in https://crbug.com/chromium/1043965#c18 for merge review

### tj...@chromium.org (2020-02-03)

Pinging @cries, @alexmos and @nasko to see if they think this should be merged to 80 or could be left to brew till 81. The impact isn't to severe in terms of what it allows so it may be fine to leave it for 81.

### tj...@chromium.org (2020-02-04)

And answering the questions in case we do want to merge: 

1. Does your merge fit within the Merge Decision Guidelines?
  - Yes, it is a security fix.
2. Links to the CLs you are requesting to merge.
  - Linked above, the only CL on this thread.
3. Has the change landed and been verified on master/ToT?
  - Yes.
4. Why are these changes required in this milestone after branch?
  - They are a security fix.
5. Is this a new feature?
  - No.

### ad...@google.com (2020-02-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-05)

I'll wait for views from @creis, @alexmos and @nasko regarding M80 merge.

### al...@google.com (2020-02-05)

My vote would be to not merge to M80:
1. The fix involves a new use of initiator origins, which carries a certain risk of regressions.  We've already had to deal with various corner cases in that area, and there's no guarantee that extensions won't have another one.
2. This isn't a recent regression, and loading a web-inaccessible-resource in a new window, while bad, doesn't seem as something critical enough to require a stable merge to me.  But I'm happy to defer to Devlin here. :)


### na...@google.com (2020-02-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2020-02-06)

Congrats the Panel decided to award $1,000 for this report! 

### ad...@chromium.org (2020-02-06)

SGTM - keeping for M81 then. Thanks.

### na...@google.com (2020-02-06)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-05-09)

This issue was migrated from crbug.com/chromium/1043965?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051315)*
