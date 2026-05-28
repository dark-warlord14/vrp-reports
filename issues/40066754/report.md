# Security: Heap-use-after-free in Browser::GetBrowserForOpeningWebUi

| Field | Value |
|-------|-------|
| **Issue ID** | [40066754](https://issues.chromium.org/issues/40066754) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | sr...@chromium.org |
| **Created** | 2023-07-03 |
| **Bounty** | $3,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

When opening the picture-in-picture window, the browser pointer of the opener will be stored in `opener_browser_`(<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser.cc;l=924>):

```
Browser\* Browser::GetBrowserForOpeningWebUi() {  
  if (!is_type_picture_in_picture()) {  
    return this;  
  }  
  
  if (!opener_browser_) {  
    auto\* opener_web_contents =  
        PictureInPictureWindowManager::GetInstance()->GetWebContents();  
    // We should always have an opener web contents if the current browser is a  
    // picture-in-picture type.  
    DCHECK(opener_web_contents);  
    opener_browser_ = chrome::FindBrowserWithWebContents(opener_web_contents);  
  }  
  
  return opener_browser_;  
}  

```

When the opener window is closed and its browser will be released, using the `opener_browser_` pointer will trigger the Use-After-Free problem.  

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser.cc;l=924;bpv=1;bpt=1>

**VERSION**  

Chrome Version: stable  

but need feature DocumentPictureInPictureAPI,ClosedTabCache.

Bisect:  

Code since <https://chromium.googlesource.com/chromium/src/+/6cb47ce5cb826a801291f22573590729e4dc7ffd>

Operating System: TestOn MAC

**REPRODUCTION CASE**

Download asan-mac-release-1118297.zip(<https://storage.googleapis.com/chromium-browser-asan/mac-release/asan-mac-release-1165113.zip>) and unzip  

Start a http server at the folder of poc.html

1. Chromium --user-data-dir=test --enable-features=DocumentPictureInPictureAPI,ClosedTabCache poc.html
2. You can refer to the video(<https://drive.google.com/file/d/19izgo2xyaDb5xpDDLiPwnRgPJEIF9PHP/view?usp=sharing>) for the following operations.

> Click the `Create PiP` button.  
> 
> Click the popup PictureInPicture window, and Click `Bookmark Manager` in the Bookmarks menu bar.  
> 
> Close the bookmark page and click the `Close` button.  
> 
> Click `Bookmark Manager` in the Bookmarks menu bar

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: anonymous

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 319 B)
- [asan](attachments/asan) (text/plain, 29.7 KB)

## Timeline

### [Deleted User] (2023-07-03)

[Empty comment from Monorail migration]

### ma...@google.com (2023-07-06)

Thanks for the detailed report.

PiP folks, could you PTAL? Thank you.

Severity-High for browser process UAF mitigated by required specific user interaction. Impact-None because the required flags have not been enabled in Stable.

[Monorail components: Blink>Media>PictureInPicture]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-07-17)

This is the secondary security shepherd; can you please take a look at this bug or reassign this to someone who can make progress? Thanks!

I looked at the video, and one thing that stood out to me is it seems like the document picture-in-picture window is outliving the window that created it, which seems unexpected and what's leading to this bad outcome.

I'm raising the priority because while there is a bit of user interaction involved, it's not clear if the interaction with the bookmark manager is needed, or the real culprit here is that the pip window is outliving its creator.

### li...@google.com (2023-07-17)

+cc:steimel, bkeen FYI

thanks -- i'll take a look at this today.

### li...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### li...@google.com (2023-07-17)

haven't managed to repro exactly yet, but i can get window.close() to refuse to close the window from the console once i do roughly the same steps.  probably related, since that works fine if i skip opening the bookmark manager first.

### ma...@google.com (2023-07-17)

Setting FoundIn to current Stable release per the bisect information in the original report.

### li...@google.com (2023-07-18)

i've not been able to repro this, though i don' thave my mac handy.  i've been trying asan on windows.

anyway, i've watched some of the ctor / dtors for browser and webcontents, and nothing interesting happens when i close the opener's window -- no dtors run.  will poke at this more tomorrow.

### li...@google.com (2023-07-18)

ah i did manage it this time.  not sure what i was doing differently.  bookmarks bar isn't needed.  just "open pip" => "close window" with ClosedTabCache enabled, and the browser window closes while the pip window does not.  without ClosedTabCache, nothing bad happens and the pip window closes.

looks like moving the web contents to the cache prevents whatever transition normally causes the pip window to close.  if i had to guess, WebContentsObserver::OnContentsDestroyed, but that's just my guess based on the name "ClosedTabCache".

### li...@google.com (2023-07-18)

heh -- when moving the WebContents into the cache [1], TL;DR:

// TODO(https://crbug.com/1117377): Add a WebContents::SetInClosedTabCache()

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/sessions/closed_tab_cache.cc;drc=636048a55ca7e2e35d5a15ba10d64b03dfe8c588;l=82

### li...@google.com (2023-07-19)

+cc: ClosedTabCache folks

is the ClosedTabCache still a thing?  I don't see much action on it since 2021.  it looks to be off by default, and i don't see any references in finch configs to it.

### sr...@chromium.org (2023-07-19)

Hi liberato@, 

Previously ClosedTabCache was used in chrome://flags. No one is actively working on ClosedTabCache now, it could be revisited in the future as it still needs some work to launch it.

My understanding was everything was under feature flag, ClosedTabCache::CacheWebContents shouldn't be called when disabled. Any specific scenario we are seeing the security issue?

### ma...@google.com (2023-07-19)

We still track security issues in features that don't (yet) ship in any production versions of Chrome, so we don't inadvertently launch new features with known security issues. See https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-labels.md#toc-security-impact-none. 


### sr...@chromium.org (2023-07-19)

Thank you. Any AI we should take or document to ensure we fix the security if we plan on launching this feature in the future?

### ma...@google.com (2023-07-19)

If there's an umbrella bug or launch bug for this feature, marking it blocked on this would probably is simplest. 

### sr...@chromium.org (2023-07-20)

[Empty comment from Monorail migration]

### sr...@chromium.org (2023-07-20)

Thank you updated the umbrella bug to reflect that. 

### li...@google.com (2023-07-25)

=> sreejakshetty@ for tracking, since the feature is off for now.

happy to work with you on figuring out the right fix for pip -- one potential, probably really simple, fix is to close pip when the page is frozen for any reason.  however, i don't really understand all the implications of a frozen page, so i don't know if it's the right thing to do.  if you can shed more light on that part, it'd be helpful.

### sr...@chromium.org (2023-07-26)

Thank you liberato@. Currently there is no one actively working on that feature. I will ensure if someone works on it we fix this. Freezing hasn't been implemented for ClosedTabCache yet.

Here's more details about freezing: https://docs.google.com/document/d/1ovkMEVFlNNU5rfcOVZpdnWX89nagjOK47-fYXa2jRfs/edit?usp=sharing

### ma...@google.com (2023-07-27)

In general, we can't security bugs not let have an owner, I think, even if they're Security_Impact-None.

### ma...@google.com (2023-07-27)

Meant to say: we can't let security bugs not have an owner


### za...@google.com (2023-08-10)

Hey sreejakshetty@ do you have an update on this bug? Let me know if we should reassign.

### sr...@chromium.org (2023-08-11)

Hi zackhan@, We marked this bug as blocking for the launch of the feature. So currently no action items on my end. No one is working on that feature currently.

### wf...@chromium.org (2023-10-06)

Hello although nobody is working on this, we do need to make meaningful progress on security bugs.

A perfectly acceptable solution would be to just remove the ClosedTabCache code until the feature is being actively worked on - this removes the attack surface entirely for our users, and we would be able to mark the bug as Fixed.

### am...@chromium.org (2023-11-14)

[security shepherd] Hi sreejakshetty@ I wanted to +1 wfh@'s question / suggestion above. Has the removal of ClosedTabCache been considered? 
While the only SLO for SI-None bugs is code / feature shipping or enabled in OT, looking at ClosedTabCache code, it looks like no one has been actively working it. 
It's not ideal to known security issues in an attack surface that is not being actively worked. 
Looking at the pseudo-launch bug (https://crbug.com/chromium/1100946) it appears there is not an active launch plan for ClosedTabCache. It would be helpful if removing the code can be considered in the interim of active development on this feature. Thank you! 

### ch...@chromium.org (2023-12-01)

[security shepherd]

sreejakshetty@: Following up on this security bug. Echoing the previous suggestions above, if this feature is not actively being worked on, perhaps the code should be removed.

### sr...@chromium.org (2024-01-03)

I will start working on removing the ClosedTabCache code, as no one is actively working on it.

### ja...@chromium.org (2024-01-17)

Thanks for helping us make progress on this issue sreejakshetty@. This bug needs an update to show progress is being made. Can you provide an ETA for the fix?

Thanks!

[secondary security shepherd]

### th...@chromium.org (2024-02-01)

[secondary shepherd] Hi sreejakshetty@, thanks for your comment https://crbug.com/chromium/1459956#c28. Have you had any luck with removing the code? (will ping as well)

### is...@google.com (2024-02-01)

This issue was migrated from crbug.com/chromium/1459956?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1100946]
[Monorail components added to Component Tags custom field.]

### ar...@chromium.org (2024-03-11)

**[secondary security shepherd]**

I see the last two shepherd asked Sreeja for an update. Do you have any?
I will ping on chat in case this slip through the cracks.

Edit: I missed this was gated behind the ClosedCacheFeature. So that's not really urgent.

### sr...@chromium.org (2024-03-11)

Hi Security Sheriffs, I haven't gotten a chance to remove this code yet. Just sent a CL (crrev.com/c/5362357) to remove code.

As Arthur said this feature is behind a feature flag. Can we move this to P2?

### ma...@google.com (2024-04-08)

Thanks for working on the code removal!

> As Arthur said this feature is behind a feature flag. Can we move this to P2?

The priority of security issues is generally based on the severity, and for high severity issues the default is P1. We may raise that for issues where we see active/in-the-wild exploitation for example, but I don't think we usually lower the priority. (And automation might change it back even if I try, not sure.)

### ap...@google.com (2024-04-10)

Project: chromium/src
Branch: main

commit 819523b1637ea73310005d7c105150eaba6d73d7
Author: Sreeja Kamishetty <sreejakshetty@chromium.org>
Date:   Wed Apr 10 00:25:03 2024

    Remove ClosedTabCache feature code
    
    In 2021 we have introduced ClosedTabCache, to cache the recently closed
    tabs to improve performance of tab restores on android. But as owners
    have moved to different teams, this feature is not under current
    development or mainteance or got launched.
    
    Removing the code to resolve current security bugs or future security bugs.
    
    For more details on the design please see
    https://docs.google.com/document/d/1SF230MYWgroe4WikDMn82ETd3-HFRzylKtIk0HZRaOU/edit?usp=sharing
    
    BUG=40066754
    
    Change-Id: I9213f3f20c7442aad70c29d97d6cecd89116024c
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5362357
    Reviewed-by: Scott Violet <sky@chromium.org>
    Commit-Queue: Sreeja Kamishetty <sreejakshetty@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1284805}

M       chrome/browser/BUILD.gn
M       chrome/browser/apps/app_service/browser_app_instance_tracker.cc
M       chrome/browser/profiles/chrome_browser_main_extra_parts_profiles.cc
M       chrome/browser/profiles/profile_keyed_service_browsertest.cc
D       chrome/browser/sessions/closed_tab_cache.cc
D       chrome/browser/sessions/closed_tab_cache.h
D       chrome/browser/sessions/closed_tab_cache_browsertest.cc
D       chrome/browser/sessions/closed_tab_cache_service.cc
D       chrome/browser/sessions/closed_tab_cache_service.h
D       chrome/browser/sessions/closed_tab_cache_service_factory.cc
D       chrome/browser/sessions/closed_tab_cache_service_factory.h
M       chrome/browser/ui/ash/shelf/browser_status_monitor.cc
M       chrome/browser/ui/browser_live_tab_context.cc
M       chrome/browser/ui/browser_tab_strip_model_delegate.cc
M       chrome/browser/ui/browser_tab_strip_model_delegate.h
M       chrome/browser/ui/browser_tabrestore.cc
M       chrome/browser/ui/browser_tabrestore.h
M       chrome/browser/ui/tabs/tab_strip_model.cc
M       chrome/browser/ui/tabs/tab_strip_model_delegate.h
M       chrome/browser/ui/tabs/tab_strip_model_observer.h
M       chrome/browser/ui/tabs/tab_strip_model_unittest.cc
M       chrome/browser/ui/tabs/test_tab_strip_model_delegate.cc
M       chrome/browser/ui/tabs/test_tab_strip_model_delegate.h
M       chrome/test/BUILD.gn

https://chromium-review.googlesource.com/5362357


### am...@chromium.org (2024-04-24)

Amazing -- thank you for landing the code removal!
I'm going to *temporarily* close this bug as fixed to be able to proceed with VRP process for the reporter of this bug. Once we have achieved that, I can either reopen it or we can ensure this is a blocker for the feature launch ClosedTabCache when work resumes for this feature.

### sp...@google.com (2024-05-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
The Chrome VRP panel decided to award you $2,000 for this report, based on this being a highly mitigated bug, mitigated by fairly significant user interaction. The reward amount also includes a $1,000 bisect bonus. 
Thank you for your efforts and reporting this issue to us!

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### pe...@google.com (2024-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066754)*
