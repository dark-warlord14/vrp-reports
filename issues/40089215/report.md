# Security: URL bar does not update correctly on redirects with extension blocking requests

| Field | Value |
|-------|-------|
| **Issue ID** | [40089215](https://issues.chromium.org/issues/40089215) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions, UI>Browser>Navigation |
| **CVE IDs** | CVE-2017-15420 |
| **Reporter** | aa...@umich.edu |
| **Assignee** | cr...@chromium.org |
| **Created** | 2017-10-05 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS

Visiting a URL (URL-1) which redirects via JavaScript to URL-2 which responds with a 301 redirect to URL-3 while in Incognito mode does not update the URL bar to the final location as expected. URL-2 is seen in the URL bar when the URL-3's content is loaded including URL-2's HTTPS information.

VERSION

Chrome Version: 61.0.3163.100 + stable
Operating System: macOS Sierra 10.12.6

and

Chrome Version: 61.0.3163.100 + stable
Operating System: Window 7 Enterprise Version 6.1.7601 Service Pack 1 Build 7601


REPRODUCTION CASE

1) Install Ghostery extension from https://chrome.google.com/webstore/detail/ghostery/mlomiejdfkolichcflejclcbmpeaniij/related?hl=en

2) When Ghostery's initial configuration window opens, click "No" on all voluntary reporting prompts then click "Block All" in Blocking Options

3) Allow Ghostery in Incognito Mode (Dots -> More Tools -> Extensions -> Click "Allow in incognito" under Ghostery extension)

4) Open Incognito window

5) Navigate to https://umich.qualtrics.com/jfe/form/SV_b44dDpnanccGM8R

6) Observe that URL bar shows URL bar shows domain as "umich.qualtrics.com" but content is from "weblogin.umich.edu"

Warning: Do not open Chrome Inspector before loading initial URL because the browser may crash. A second bug report is inbound as this may be a separate issue. I will update this ticket with the second ticket's reference after it is issued.


## Attachments

- [URL-bar-mismatch.png](attachments/URL-bar-mismatch.png) (image/png, 237.3 KB)
- [Mismatch-Chrome-62-beta.png](attachments/Mismatch-Chrome-62-beta.png) (image/png, 217.5 KB)
- [Mismatch-Chrome-63-dev.png](attachments/Mismatch-Chrome-63-dev.png) (image/png, 230.2 KB)

## Timeline

### el...@chromium.org (2017-10-05)

I assume you can confirm that this only reproduces when Ghostery is installed? Are you able to reproduce it in a profile with /only/ that extension installed?

I cannot reproduce this in Chrome 62 or 63 on Mac (the omnibox shows the expected URL); the first request briefly results in a temporary error page for ERR_BLOCKED_BY_CLIENT before the final page loads.

When chrome://flags/#browser-side-navigation is set to DISABLED (mimic'ing the defaults in old Chrome), no page is loaded at all and the ERR_BLOCKED_BY_CLIENT is shown for an extension URL: chrome-extension://mlomiejdfkolichcflejclcbmpeaniij/app/templates/blocked_redirect.html

[Monorail components: UI>Browser>Navigation]

### aa...@umich.edu (2017-10-05)

Yes, I tested on both macOS and Windows with only Ghostery installed and trigger the bug consistently. I have not been able to trigger the bug when Ghostery is not installed.

I can reproduce in Chrome 62.0.3202.45 + beta and Chrome 63.0.3230.0 + dev via the same steps listed (screenshots attached).

### oc...@chromium.org (2017-10-05)

creis: Would you be the right person to take a look at this? Thanks.

Severity-Low for now 

### oc...@chromium.org (2017-10-05)

(oops, comment got cut off. severity-low for needing to install this extension)

### cr...@chromium.org (2017-10-05)

alexmos@, would you be able to take a look?  Nasko, Alex, Łukasz and I were just chatting about blocked navigations and where they're handled, so it sounds like this is relevant.  (At first glance, I'm unclear what would be different about the incognito case.)

Adding Devlin for extensions, though it may be general to other types of blocked navigations.

[Monorail components: Platform>Extensions]

### aa...@umich.edu (2017-10-05)

This bug may or may not be related to Issue #772113 as the same URL and very similar reproduction steps are required.

### aa...@umich.edu (2017-10-05)

Update: Possibly related Issue #772113 was closed as a duplicate of Issue #742955.

### sh...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### al...@chromium.org (2017-10-07)

Progress update.  I have a local repro of this, but it is very inconsistent.  About 2/3 of the time I end up at the blocked redirect page with no subsequent redirects, but the other 1/3 of the time there's a new navigation right after the blocked redirect page that eventually takes us to the page with the wrong omnibox contents.  If I keep pasting the starting URL into the omnibox and hitting enter, I eventually get a repro on Linux ToT.

I also think this isn't specific to incognito.  I reproed this the same way in a regular window.  

The repro seems to generally follow these steps:

1. We load https://umich.qualtrics.com/jfe/form/SV_b44dDpnanccGM8R

2. This load commits.

3. The new page does a window.location.replace to https://umich.qualtrics.com/SE?SID=SV_b44dDpnanccGM8R&Q_JFE=0

4. That load redirects to https://umich.qualtrics.com/SE/?SID=SV_b44dDpnanccGM8R&Q_JFE=0 (almost the same, note the extra slash before ?).  Let's call this url_from_step_4.

5. Ghostery cancels that load with webRequest API (onBeforeRequest).  Not quite sure about details, but I believe that in the cancellation callback, the extension then starts a new navigation (via chrome.tabs.update) to an extension resource URL chrome-extension://mlomiejdfkolichcflejclcbmpeaniij/app/templates/blocked_redirect.html (to show a friendly "redirect blocked" page to users)

6. As part of canceling the load, we set the error code on the NavigationHandle to ERR_BLOCKED_BY_CLIENT

7. We get a OnDidFailProvisionalLoadWithError for url_from_step_4.

8. We initiate a new browser-initiated navigation via RequestNavigation for the blocked_redirect.html URL from step 5.

9. We get a DidCommitProvisionalLoad for the (blocked) url_from_step_4, presumably for the error page.  As part of processing DidCommit we go through NavigationControllerImpl::RendererDidNavigateToExistingPage, and we execute this block of code from Nasko's r474535:

  // When a navigation in the main frame is blocked, it will display an error
  // page. To avoid loading the blocked URL on back/forward navigations,
  // do not store it in the FrameNavigationEntry's URL or PageState. Instead,
  // make it visible to the user as the virtual URL. Store a safe URL
  // (about:blank) as the one to load if the entry is revisited.
  // TODO(nasko): Consider supporting similar behavior for subframe
  // navigations, including AUTO_SUBFRAME.
  if (!rfh->GetParent() &&
      IsBlockedNavigation(navigation_handle->GetNetErrorCode())) {
    DCHECK(params.url_is_unreachable);
    active_entry->SetURL(GURL(url::kAboutBlankURL));
    active_entry->SetVirtualURL(params.url);
    if (frame_entry) {
      frame_entry->SetPageState(
          PageState::CreateFromURL(active_entry->GetURL()));
    }
  }

We set the virtual URL to url_from_step_4, because this is a blocked navigation (see step 5).

10. We get a request to start *another* renderer-initiated navigation to url_from_step_4.  This is probably the racy part, it doesn't happen if the blocked_redirect.html commits before this step.  I don't yet understand how the renderer is able to generate this, given that it should be at an error page from step 9.  Maybe the request was queued up as another navigation from JS just before we navigated to the error page?  In any case, it seems like it cancels the navigation to blocked_redirect.html, which doesn't commit after this point.

11. The request from step 10 continues and goes through four other redirects before arriving at the final URL of https://weblogin.umich.edu/?cosign-shibboleth.umich.edu&https://shibboleth.umich.edu/idp/Authn/UWLogin?conversation=e1s1

12. When we commit that URL, we go through RendererDidNavigateToExistingPage, which updates the NavigationEntry's URL to weblogin.umich.edu, but it does *not* update the virtual URL (entry->update_virtual_url_with_url() is false), leaving us with the virtual URL set in step 9, which is url_from_step_4 (i.e., umich.qualtrics.com).  This results in omnibox later pulling in the wrong virtual URL for display.

It seems weird that we kick off a renderer-initiated navigation while we're on an error page after a blocked navigation.  Charlie or Nasko - any thoughts on why this is happening, and why it's allowed to cancel an ongoing browser-initiated navigation (to blocked_redirect.html)?  Also, in general, is it problematic that we've set up the virtual URL for the error page entry but haven't set update_virtual_url_with_url(), so the virtual URL might become stale?  You probably have better context on r474535 than me.

Also, I'm not sure what the intent of Ghostery here is, but it seems it also wants this navigation blocked?  This is what happens most of the time for me anyway.


### al...@chromium.org (2017-10-11)

Quick update after chatting with creis@ yesterday.  First, Charlie has a CL from a while ago that would convert location.replace to use NEW_PAGE with replacement, rather than EXISTING_PAGE, and it seems like that would help here, because instead of reusing the old NavigationEntry, we'd be creating a new one, so the stale virtual URL won't stick around in step 12.

Second, we might need to revisit Nasko's fix in r474535 and just not set virtual URLs at all on blocked navigations, because of the danger from this kind of confusion.  If the purpose of setting it is only to let users see the blocked URL, it doesn't seem that bad if we just don't show anything, or show about:blank instead.  I'll reassign over to Nasko for now to get his thoughts on this once he's back.

I'm still not quite sure how step 10 is happening, i.e., how exactly the renderer queues up the navigation that starts after the error page commits.  That would need a bit more digging to understand.


### na...@chromium.org (2017-10-25)

Setting creis@ as the owner, since he has a patch in progress that likely fixes this issue as well.

### cr...@chromium.org (2017-10-26)

Should be fixed by r511942.

### sh...@chromium.org (2017-10-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-11-06)

Nice one! The VRP Panel has decided to award $500 for this report. A member of our finance team will be in touch to arrange payment.  Also, how would you like to be credited in release note?  Cheers!

### aw...@chromium.org (2017-11-09)

[Empty comment from Monorail migration]

### aa...@umich.edu (2017-11-12)

awhalley: "Drew Springall (@_aaspring_)" would work great. Thanks.

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### aa...@umich.edu (2018-02-02)

awhalley@: When you tagged this as CVE-2017-15420, I went back and looked at the Chrome release notes (https://chromereleases.googleblog.com/2017/12/stable-channel-update-for-desktop.html) and saw that the CVE was attributed to someone else that reported it after me. I figured they found a broader bug that included this one so they got the CVE. Then I saw yesterday's Debian security update attributes it to me (https://lists.debian.org/debian-security-announce/2018/msg00026.html). Can you clarify what's going on? Thanks.

### sh...@chromium.org (2018-02-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-07)

Hi aaspring@ - very sorry for the months that have passed since your query in https://crbug.com/chromium/771848#c22 (I wasn't CCed on the bug at the time so never got a notification).

What happened is that the change that fixed both this and https://crbug.com/chromium/777419 was associated with https://crbug.com/chromium/777419, so the automation picked up the reporter of that bug for the release notes, even though you reported it first. This bug appear, with the same CVE, in these release notes:

https://chromereleases.googleblog.com/2018/01/stable-channel-update-for-desktop_24.html

properly crediting you. Even though they were fixed together, they perhaps could have been fixed separately, which per MITRE's CVE counting rules means they should be given a separate CVE.  I'll investigate what the best options are here.

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/771848?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089215)*
