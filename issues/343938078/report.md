# Security: Android address bar URL spoof if page is scrolling and tab is switched

| Field | Value |
|-------|-------|
| **Issue ID** | [343938078](https://issues.chromium.org/issues/343938078) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Android |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | sk...@google.com |
| **Created** | 2024-06-01 |
| **Bounty** | $6,000.00 |

## Description

#### SUMMARY

The address bar can display another page's URL quite persistently after specific conditions, leading to origin spoofing.

When a user is scrolling down on a page, the browser hides the address bar (if it's been visible for at least 3 seconds). This is not an issue by itself.

When address bar is hidden, if the page is closed, a new tab is opened, or the user switches tabs quickly with the address bar not fully shown, the spoof occurs. The address bar will continue to show the previous page's URL.

#### VULNERABILITY DETAILS

The spoof can be triggered manually by a user (this is how I accidentally discovered it), or the opener closes the window while the user is scrolling. There may be other ways of triggering this spoof.

The issue only occurs if the address bar is fully hidden or is partially transitioning from hidden to showing. It does not seem to occur if the address bar is hiding from a fully-shown state.

The URL spoof persists after these actions:

- User switches to another app or home screen, and then returns to Chrome
- User switches tab
- Page or user creates new windows (even on different tabs)
- Page or user navigates to another page (even cross-origin + cross-site)
- User completely closes tab

The correct URL is shown after these actions:

- User scrolls on page (or tries to scroll on page, even if page isn't scrollable)

This seems to have been introduced by commmit `505e507589722777bcc973394f2c1f78b9768077` [1].

[1] `Don't relayout control container until scrolling ceases` <https://chromium.googlesource.com/chromium/src.git/+/505e507589722777bcc973394f2c1f78b9768077>

This change prevents address bar captures while the page is scrolling:

```
private final Runnable mUpdateVisibilityRunnable =
    new Runnable() {
        @Override
        public void run() {
            int visibility = shouldShowAndroidControls() ? View.VISIBLE : View.INVISIBLE;
            if (mControlContainer == null
                    || mControlContainer.getView().getVisibility() == visibility) {
                return;
            } else if (visibility == View.VISIBLE
                    && mContentViewScrolling        // <- If scrolling, update will be prevented
                    && ToolbarFeatures.shouldSuppressCaptures()) {
                // Don't make the controls visible until scrolling has stopped to avoid
                // doing it more often than we need to. onContentViewScrollingStateChanged
                // will schedule us again when scrolling ceases.
                return;
            }

            // ...
        }
    };

```

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/BrowserControlsManager.java;l=126;drc=3eff3c5eea572776f2839fed4d43d31162ed911a>

```
@Override
public void onContentViewScrollingStateChanged(boolean scrolling) {
    if (!scrolling                     // <- If scrolling, update will be prevented
            && ToolbarFeatures.shouldSuppressCaptures()
            && shouldShowAndroidControls()
            && mControlContainer.getView().getVisibility() != View.VISIBLE) {
        scheduleVisibilityUpdate();
    }

    mContentViewScrolling = scrolling;
}

```

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/BrowserControlsManager.java;l=267;drc=3eff3c5eea572776f2839fed4d43d31162ed911a>

ADDITIONAL CONTEXT

On Canary: On my device (using dark mode), when the address bar has a slightly darker background behind text, this will repro. On Stable, there isn't a background color change for some reason.
Seems like zooming in page with fingers also results in dark background behind text, but since the gesture is shorter, it's more difficult to perform the attack (even programatically).

I started noticing this during my Chrome normal usage since mid-2023, but it was elusive since I didn't know what was triggering it (despite my many, *many* attempts). After triggering this accidentally at least once a month for the past year, I finally figured out the reliable trigger a couple of days ago. It's possible others noticed this behavior too.

#### VERSION

Chrome Version: 127.0.6509.0 Canary, 125.0.6422.72 Stable.

Operating System: Android 12

#### BISECT

Starts reproducing on commit <https://chromium.googlesource.com/chromium/src.git/+/505e507589722777bcc973394f2c1f78b9768077>

Landed in 109.0.5368.0 in October 2022: <https://chromiumdash.appspot.com/commit/505e507589722777bcc973394f2c1f78b9768077>

Verified repro down to Android snapshot build 1060656 [1].

[1] <https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Android/1060656/>

#### REPRODUCTION CASE

There may be additional ways to reproduce this issue. This is the best PoC I could develop in a day. I may have an improved PoC within the next couple of weeks.

The PoC uses Video PiP to show user instructions, but if the user knows how to do this, one less tap is needed. A compromised renderer may also be able to automatically perform some of these actions (other than the scroll/fling).

##### Scenario 1: Attacker closes tab programatically

1. Navigate to <https://alesandroortiz.com/security/chromium/origin-spoof-scroll.html>
2. Tap anywhere once
3. Tap anywhere again
4. Wait for 3 second countdown to complete, then scroll/fling down slowly

Observed: After the tab is closed by opener (attacker) page, the address bar still shows the URL of the closed page.

Expected: The address bar always shows the URL of the currently committed page (...if not making a browser-initiated navigation)

##### Scenario 2: User manually switches tabs while page is scrolling

This is how I had accidentally triggered it (while browsing news sites and switching tabs quickly).

1. Navigate a tab to <https://example.com> (or any page to simulate the attacker page)
2. In the same tab group, navigate a tab to <https://www.google.com/accounts/about/> (or any tall page, such as news websites; this is the target page)
3. Wait 3 seconds after loading the tab.
4. Scroll/fling down on the target page until address bar is fully hidden
5. Do a fling up (i.e. scroll up and release finger so it continues scrolling) and immediately afterwards tap the other tab icon in the tab group switcher (at the bottom).

Observed: After the tab is switched, the address bar still shows the URL of the previous tab.

Expected: Same as Scenario 1.

#### CREDIT INFORMATION

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [origin-spoof-scroll.html](attachments/origin-spoof-scroll.html) (text/html, 3.5 KB)
- [origin-spoof-scroll.html](attachments/origin-spoof-scroll.html) (text/html, 3.5 KB)
- [origin-spoof-scroll-canary.mp4](attachments/origin-spoof-scroll-canary.mp4) (video/mp4, 6.8 MB)
- [origin-spoof-scroll-stable.mp4](attachments/origin-spoof-scroll-stable.mp4) (video/mp4, 6.5 MB)
- [origin-spoof-scroll-manual.mp4](attachments/origin-spoof-scroll-manual.mp4) (video/mp4, 7.5 MB)

## Timeline

### al...@alesandroortiz.com (2024-06-01)

Attached updated PoC (removes errant line).

Also attached videos:

- Scenario 1 in Canary (`-canary.mp4`)
- Scenario 1 in Stable (`-stable.mp4`)
- Scenario 2 (manual repro) in Canary (`-manual.mp4`)

The videos try to demonstrate various states where the spoof is preserved. The only case where the correct URL is restored is when the user finishes a page scroll. During scroll, the spoof persists.

Notice how on Canary the background of the address bar changes when the spoofing conditions are met. This was helpful to me when looking for spoof triggers, so mentioning it again here.

### al...@alesandroortiz.com (2024-06-01)

IIUC the 3 second delay before address bar hides on scroll is due to `MAX_FULLSCREEN_LOAD_DELAY_MS` [1]

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/tab/TabStateBrowserControlsVisibilityDelegate.java;l=36;drc=aed2f60917e3aa3cc3da98a3c443edce5933b07a>

### za...@google.com (2024-06-03)

Hi smaier@ can you please help triage this Clank issue, thank you. 

### sm...@google.com (2024-06-03)

I'm not a security nor layout nor URLBar expert, so forwarding to pnoland@ who's CL is pointed at as the culprit CL. Hope you can tell whether this is a bug.

### za...@google.com (2024-06-03)

Thanks for the quick response Sam. I am reassigning this to the CL owner right now. 

### sk...@google.com (2024-06-03)

Thanks for the report!

The purpose of the optimization in <https://crrev.com/c/3961571> was when we are in a long scroll/fling event, to delay switching from the captured toolbar to the android toolbar. It's possible these two would get out of sync, but usually this isn't a big deal, and it's actually less jarring to only transition once, at least when the issue isn't the wrong domain.

But the underlying assumption is that we're always in BrowserControlsState.BOTH mode. And that's not the case at all in this bug. We've switched tabs, TabBrowserControlsConstraintsHelper should have pushed down that we're now in BrowserControlsState.SHOWN, and it's no longer okay to be lazy about switching to the Java view. We need to switch right now, ignoring any in progress touch/motion/scroll/fling events. It looks like we can use the mBrowserVisibilityDelegate to work around this.

Testing this locally however, it seems like we also actually get a broken scrolling signal. onContentViewScrollingStateChanged(false) is never called. We can easily reset this in onObservingDifferentTab. This fixes Scenario #1, but not Scenario #2, which is trickier. The controls are already in the correct state, so everything no-ops. So we need to create an edge.

Not quite certain which approach is preferred, will send for feedback. Two different approaches to fix this:

- <https://crrev.com/c/5595208>
- <https://crrev.com/c/5594495>

I guess, Jinsuk, in particular I don't get all of the `setPositionsForTabToNonFullscreen()` related code. It feels a little redundant, both CLs call `scheduleVisibilityUpdate()` after. But maybe it's fine.

It's also possible we want to do both mitigations to be extra sure.

### al...@alesandroortiz.com (2024-06-04)

Thanks for quick work on this!

Also want to note that Scenario 1 (closing tab) also works manually: Follow Scenario 2 steps, and replace step 5 with "fling, then close current tab in tab group switcher". I definitely had accidental repros this way too over the past year.

### pe...@google.com (2024-06-04)

Setting milestone because of s2 severity.

### ap...@google.com (2024-06-05)

Project: chromium/src
Branch: main

commit f570d85522aa5656d38ae43b125185e442e0dc44
Author: Sky Malice <skym@chromium.org>
Date:   Wed Jun 05 20:24:48 2024

    Immediately show browser controls on SHOWN.
    
    The optimization to delay immediately show the browser controls during
    a scroll event was only intended to be used while in BOTH mode.
    However there are multiple ways to close or switch tabs while still
    being in a scroll. This caused our captured controls to be on the
    screen when they were unacceptably stale.
    
    To fix this, we now no longer perform this optimization when BOTH is
    set, and on the transition we calculate visibility.
    
    Bug: 343938078
    Change-Id: I9d79dccf5536ea68f59b69ef637c7771de5fb815
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5595208
    Reviewed-by: Calder Kitagawa <ckitagawa@chromium.org>
    Commit-Queue: Sky Malice <skym@chromium.org>
    Reviewed-by: Patrick Noland <pnoland@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Jinsuk Kim <jinsukkim@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1310849}

M       chrome/android/java/src/org/chromium/chrome/browser/fullscreen/BrowserControlsManager.java
M       chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/BrowserControlsManagerUnitTest.java
M       chrome/browser/browser_controls/android/java/src/org/chromium/chrome/browser/browser_controls/BrowserStateBrowserControlsVisibilityDelegate.java

https://chromium-review.googlesource.com/5595208


### ap...@google.com (2024-06-05)

Project: chromium/src
Branch: main

commit 44e9e45090b5b72d817abb4ecff492aaa3eec02e
Author: Sky Malice <skym@chromium.org>
Date:   Wed Jun 05 20:24:35 2024

    Reset scrolling on tab switch for browser controls.
    
    The signal for scrolling start and stopping was not consistently
    being sent when switching tabs, or closing the current tab. This
    change mitigates the problem by directly calling its scrolling
    observer to stop scrolling when the tab changes.
    
    This was problem because of an optimization that delayed showing
    the java view for the browser controls (toolbar) during a scroll
    event. But when scrolling was stuck on, we incorrectly left the
    captured controls on the screen when they were unacceptably stale.
    
    Bug: 343938078
    Change-Id: Ie1017ab0d67c61030df665638592996507e4f9de
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5594495
    Reviewed-by: Calder Kitagawa <ckitagawa@chromium.org>
    Reviewed-by: Patrick Noland <pnoland@chromium.org>
    Reviewed-by: Jinsuk Kim <jinsukkim@chromium.org>
    Commit-Queue: Sky Malice <skym@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1310848}

M       chrome/android/java/src/org/chromium/chrome/browser/fullscreen/BrowserControlsManager.java
M       chrome/android/java/src/org/chromium/chrome/browser/tab/TabBrowserControlsOffsetHelper.java
M       chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/BrowserControlsManagerUnitTest.java

https://chromium-review.googlesource.com/5594495


### al...@alesandroortiz.com (2024-06-05)

Verified as fixed in snapshot build 1310851 [1] on Android 12, using PoC from Scenario 1, manual trigger from Scenario 2, and manual trigger from [#comment8](https://issues.chromium.org/issues/343938078#comment8).

Thanks for quick fix!

[1] <https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Android/1310851/>

### sp...@google.com (2024-06-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $6000.00 for this report.

Rationale for this decision:
$5,000 for report of moderate impact security UI spoof + $1,000 bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### al...@alesandroortiz.com (2024-06-29)

Thanks for the reward!

Is the re-added `reward-topanel` label incorrect? Payment is already en route to my bank. (Love the new payment system!)

### am...@chromium.org (2024-07-01)

Yes -- it is incorrect. I had to make updates to our automation now that the bugcrowd workflow is up and running and it didn't kick in just yet to apply the correct reward-* label (here, reward-inprocess), which would have prevented reward-topanel from being reapplied.

### pe...@google.com (2024-09-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $5,000 for report of moderate impact security UI spoof + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/343938078)*
