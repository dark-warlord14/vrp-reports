# Security: Chrome for Android Delay Navigate then requestFullScreen will Hide Omnibox 

| Field | Value |
|-------|-------|
| **Issue ID** | [40057930](https://issues.chromium.org/issues/40057930) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>FullScreen, UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | su...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2021-11-16 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

After tap to the page to call requestFullScreen while JS in queue to execute HTML form.submit() delayed with queueMicroTask calling synchronous XHR, finally when form.submit() navigate to POST request URL, the omnibox will immediately disappear and hidden.

Interestingly, when put up spoof omnibox after the omnibox is hidden, it looks convincing that the spoof omnibox is legit (as on attached video).

However as the testcase using delay execution method, currently there are still chance for the omnibox still visible after navigate to POST request URL. on current testcase I think it has to do with the XHR timing GET delay?[value].

This similar to <https://crbug.com/chromium/639702> which hide omnibox after tap to the page.

**VERSION**

- Chrome 95.0.4638.74; Android 11; Mi 9T
- Chrome 95.0.4638.74; Android 6.0 (Google APIs); Android Emulator x86
- Chrome Dev 97.0.4692.10; Android 11; Mi 9T
- Chrome Dev 97.0.4692.10; Android 11; SM-J500F (2015 device)

**REPRODUCTION CASE**

1. Download and extract hideomniboxspoof.zip
2. Open terminal in extract directory
3. Run "node app.js" to serve the webserver
4. Visit the webserver ipaddress:8000 (i.e. 127.0.0.1:8000)
5. Tap anywhere on the page
6. Omnibox will hide immediately then spoofed with spoof omnibox.

**CREDIT INFORMATION**  

Reporter credit: Irvan Kurniawan (sourc7)

## Attachments

- [hideomniboxspoof.zip](attachments/hideomniboxspoof.zip) (application/octet-stream, 663.2 KB)
- [hideomnibox demonstration on Mi 9T.mp4](attachments/hideomnibox demonstration on Mi 9T.mp4) (video/mp4, 26.4 MB)

## Timeline

### [Deleted User] (2021-11-16)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-11-17)

Assigning to jinsukkim@ based on https://crbug.com/chromium/1264561.

[Monorail components: UI>Browser>FullScreen UI>Browser>Omnibox]

### [Deleted User] (2021-11-17)

[Empty comment from Monorail migration]

### tw...@chromium.org (2021-11-17)

cc fgorski@ for omnibox

### [Deleted User] (2021-11-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-30)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2021-12-08)

The hack devised a way to hide the toolbar controls by exploiting a subtle timing issue in handling fullscreen.

The fullscreen request puts Chrome into persistent fullscreen mode and hides toolbar first. The actual fullscreen mode is entered once the toolbar gets hidden as the second step. But the form.submit (loading the spoof page) that immediately follows the fullscreen request resets the process in the middle[1]. Therefore the toolbar gets hidden but the next step cannot proceed, leading to the effect of toolbar left hidden after the spoof page is loaded.

Do we always show toolbar (omnibox) when a new URL is loaded? Then the solution would be as simple as ensuring it gets visible upon TabObserver.onPageLoadFinished.

[1] exitFullscreen() is invoked here, and resets variables containing the pending fullscreen state.


### fg...@chromium.org (2021-12-08)

This is gold. Are you fixing this, Jinsuk, or do you someone else should take a look? (CCing some folks who might help and will definitely benefit from reading through this.)

Also, looks like I missed it earlier, when leaving for vacation.

### tw...@chromium.org (2021-12-08)

> [1] exitFullscreen() is invoked here, and resets variables containing the pending fullscreen state.

Is this FullscreenHtmlApiHandler#exitFullscreen()? If so, we have a layout change observer that's supposed to update SHOWN and it sounds like maybe that's getting skipped?

It'd be helpful to have a sketch of the code paths involved -- I'm thinking if we can it'd be good to reset browser controls state wherever we're currently hiding vs listening for a different signal like #onPageLoadFinished to reset state.

### ji...@chromium.org (2021-12-09)

> Are you fixing this, Jinsuk, or do you someone else should take a look? (CCing some folks who might help and will definitely benefit from reading through this.

I'm looking into this but would be great if someone else can take it over - I'm busy sheriffing crashes this week.

> Is this FullscreenHtmlApiHandler#exitFullscreen()? If so, we have a layout change observer that's supposed to update SHOWN and it sounds like maybe that's getting skipped?

Yes it is. I see BrowserControlsManager#updateBrowserControlOffsets() for hiding the toolbar invoked immediately after the FullscreenHtmlApiHandler#exitFullscreen(). Looks like that's why the code in layout change observer does not take effect.

### tw...@chromium.org (2021-12-10)

What's calling BrowserControlsManager#updateBrowserControlsOffsets() and with what values? 

### ji...@chromium.org (2021-12-14)

Weird - I cannot reproduce the issue after gclient sync. The test page redirects to the spoof page automatically without a tap on it, and the omnibox is not hidden any more. Let me try to sort it out a bit - may have to assign to someone else if I don't get it to work (or not work) again.

For the answer to twellington@'s question, I ran Chrome again to get the flow around BrowserControlsManager#updateBrowserControlsOffsets even though the problem is not reproducible now. The offsets might not be the same as the ones we need, but the calling sequence looks the same:

12-14 10:19:13.205 21679 21679 I crdebug : updateBrowserControlsOffsets top-control-offset: 0 top-content-offset: 196                               
12-14 10:19:13.205 21679 21679 I crdebug : 0] updateBrowserControlsOffsets(BrowserControlsManager.java:677)                             
12-14 10:19:13.205 21679 21679 I crdebug : 1] onOffsetsChanged(BrowserControlsManager.java:627)                                         
12-14 10:19:13.205 21679 21679 I crdebug : 2] access$600(BrowserControlsManager.java:62)                                                
12-14 10:19:13.205 21679 21679 I crdebug : 3] onBrowserControlsOffsetChanged(BrowserControlsManager.java:242)                           
12-14 10:19:13.205 21679 21679 I crdebug : 4] notifyControlsOffsetChanged(TabBrowserControlsOffsetHelper.java:99)                       
12-14 10:19:13.205 21679 21679 I crdebug : 5] setTopOffset(TabBrowserControlsOffsetHelper.java:75)                                      
12-14 10:19:13.205 21679 21679 I crdebug : 6] onTopControlsChanged(TabViewAndroidDelegate.java:74)                                      
12-14 10:19:13.205 21679 21679 I crdebug : 7] nativePollOnce(Native Method)                                                             
12-14 10:19:13.205 21679 21679 I crdebug : 8] next(MessageQueue.java:335)   

### su...@gmail.com (2021-12-14)

> Weird - I cannot reproduce the issue after gclient sync. The test page redirects to the spoof page automatically without a tap on it, and the omnibox is not hidden any more. Let me try to sort it out a bit - may have to assign to someone else if I don't get it to work (or not work) again.

Ok, I've sort it out try to increase the delay from /delay?400 to /delay?2000 and iteration < 999 to iteration < 800. I have tested this on multiple device it now the same as on PoC video.

### tw...@chromium.org (2021-12-14)

Re #12 -- So the call is coming from #onTopControlsChanged?

Trying to help brainstorm places we could update the code, but it's a bit tough without knowing the full flow... do you mind walking me through what methods get called (i.e. traces) for when we start to enter fullscreen & hide controls, get interrupted, then exit fullscreen but don't reset browser controls state properly?

### ji...@chromium.org (2021-12-20)

Here is the flow I observed when the problem happens:

Tapping the screen initiates a fullscreen request. Since the browser controls are not hidden, it only sets the persistent fullscreen mode to true, sets the pending fullscreen option, and returns: 

12-20 21:00:23.624 27537 27537 I crdebug : enter-persistent-fullscreen persistent-mode: false control-hidden: false option: false
12-20 21:00:23.625 27537 27537 I crdebug : 1] enterPersistentFullscreenMode(FullscreenHtmlApiHandler.java:339)
12-20 21:00:23.625 27537 27537 I crdebug : 2] lambda$onEnterFullscreen$0$org-chromium-chrome-browser-fullscreen-FullscreenHtmlApiHandler(FullscreenHtmlApiHandler.java:276)
12-20 21:00:23.625 27537 27537 I crdebug : 3] run(Unknown Source:6)
12-20 21:00:23.625 27537 27537 I crdebug : 4] onEnterFullscreen(FullscreenHtmlApiHandler.java:282)
12-20 21:00:23.625 27537 27537 I crdebug : 5] enterFullscreenModeForTab(ActivityTabWebContentsDelegateAndroid.java:372)
12-20 21:00:23.625 27537 27537 I crdebug : 6] enterFullscreenModeForTab(TabWebContentsDelegateAndroidImpl.java:159)
12-20 21:00:23.625 27537 27537 I crdebug : 7] nativePollOnce(Native Method)
12-20 21:00:23.625 27537 27537 I crdebug : 8] next(MessageQueue.java:335)

We get another fullscreen request here but no change happens yet, as the controls are still hidden:

12-20 21:00:23.626 27537 27537 I crdebug : enter-persistent-fullscreen persistent-mode: true control-hidden: false option: false
12-20 21:00:23.627 27537 27537 I crdebug : 1] enterPersistentFullscreenMode(FullscreenHtmlApiHandler.java:339)
12-20 21:00:23.627 27537 27537 I crdebug : 2] lambda$onEnterFullscreen$0$org-chromium-chrome-browser-fullscreen-FullscreenHtmlApiHandler(FullscreenHtmlApiHandler.java:276)
12-20 21:00:23.627 27537 27537 I crdebug : 3] run(Unknown Source:6)
12-20 21:00:23.627 27537 27537 I crdebug : 4] onEnterFullscreen(FullscreenHtmlApiHandler.java:282)
12-20 21:00:23.627 27537 27537 I crdebug : 5] enterFullscreenModeForTab(ActivityTabWebContentsDelegateAndroid.java:372)
12-20 21:00:23.627 27537 27537 I crdebug : 6] fullscreenStateChangedForTab(TabWebContentsDelegateAndroidImpl.java:164)
12-20 21:00:23.627 27537 27537 I crdebug : 7] nativePollOnce(Native Method)
12-20 21:00:23.627 27537 27537 I crdebug : 8] next(MessageQueue.java:335)

We're supposed to get browser controls offset change next and then process the pending fullscreen state to enter the fullscreen mode. But a new URL (spoofpage) gets loaded, which cancels the fullscreen entrance sequences. The pending fullscreen option is nulled out. 

12-20 21:00:23.705 27537 27537 I crdebug : exit-fullscreen persistent-mode: true pending-option: org.chromium.chrome.browser.fullscreen.FullscreenOptions@5160125
12-20 21:00:23.705 27537 27537 I crdebug : 1] exitPersistentFullscreenMode(FullscreenHtmlApiHandler.java:366)
12-20 21:00:23.705 27537 27537 I crdebug : 2] onExitFullscreen(FullscreenHtmlApiHandler.java:295)
12-20 21:00:23.705 27537 27537 I crdebug : 3] exitFullscreenModeForTab(ActivityTabWebContentsDelegateAndroid.java:378)
12-20 21:00:23.705 27537 27537 I crdebug : 4] exitFullscreenModeForTab(TabWebContentsDelegateAndroidImpl.java:169)
12-20 21:00:23.705 27537 27537 I crdebug : 5] nativePollOnce(Native Method)
12-20 21:00:23.705 27537 27537 I crdebug : 6] next(MessageQueue.java:335)
12-20 21:00:23.705 27537 27537 I crdebug : 7] loop(Looper.java:183)
12-20 21:00:23.705 27537 27537 I crdebug : 8] main(ActivityThread.java:7656)


12-20 21:00:23.774 27537 27537 I crdebug : exit-fullscreen persistent-mode: false pending-option: null
12-20 21:00:23.774 27537 27537 I crdebug : 1] exitPersistentFullscreenMode(FullscreenHtmlApiHandler.java:366)
12-20 21:00:23.774 27537 27537 I crdebug : 2] onDidFinishNavigation(FullscreenHtmlApiHandler.java:234)
12-20 21:00:23.774 27537 27537 I crdebug : 3] didFinishNavigation(TabWebContentsObserver.java:323)
12-20 21:00:23.774 27537 27537 I crdebug : 4] didFinishNavigation(WebContentsObserverProxy.java:122)
12-20 21:00:23.774 27537 27537 I crdebug : 5] nativePollOnce(Native Method)
12-20 21:00:23.774 27537 27537 I crdebug : 6] next(MessageQueue.java:335)
12-20 21:00:23.774 27537 27537 I crdebug : 7] loop(Looper.java:183)
12-20 21:00:23.774 27537 27537 I crdebug : 8] main(ActivityThread.java:7656)


Now we get the expected browser control offset change that would have hidden the omnibox:

12-20 21:00:23.804 27537 27537 I crdebug : updateBrowserControlsOffsets: top-control-offset: -196 top-content-offset: 0
12-20 21:00:23.804 27537 27537 I crdebug : 1] updateBrowserControlsOffsets(BrowserControlsManager.java:656)
12-20 21:00:23.804 27537 27537 I crdebug : 2] onOffsetsChanged(BrowserControlsManager.java:612)
12-20 21:00:23.804 27537 27537 I crdebug : 3] access$400(BrowserControlsManager.java:55)
12-20 21:00:23.804 27537 27537 I crdebug : 4] onBrowserControlsOffsetChanged(BrowserControlsManager.java:227)
12-20 21:00:23.804 27537 27537 I crdebug : 5] notifyControlsOffsetChanged(TabBrowserControlsOffsetHelper.java:99)
12-20 21:00:23.804 27537 27537 I crdebug : 6] setTopOffset(TabBrowserControlsOffsetHelper.java:75)
12-20 21:00:23.804 27537 27537 I crdebug : 7] onTopControlsChanged(TabViewAndroidDelegate.java:74)
12-20 21:00:23.804 27537 27537 I crdebug : 8] nativePollOnce(Native Method)

Since the pending fullscreen option was already reset to null, the fullscreen entrance process cannot proceed at this point when |maybeEnterFullscreenFromPendingState| is called:

12-20 21:00:23.804 27537 27537 I crdebug : maybeEnterFullscreenFromPendingState controls-hidden: true pending-option: null
12-20 21:00:23.805 27537 27537 I crdebug : 1] maybeEnterFullscreenFromPendingState(FullscreenHtmlApiHandler.java:357)
12-20 21:00:23.805 27537 27537 I crdebug : 2] $r8$lambda$RhHeXyx63gqPJdv56qqzFOBnVno(Unknown Source:0)
12-20 21:00:23.805 27537 27537 I crdebug : 3] onResult(Unknown Source:8)
12-20 21:00:23.805 27537 27537 I crdebug : 4] set(ObservableSupplierImpl.java:70)
12-20 21:00:23.805 27537 27537 I crdebug : 5] setPositionsForTab(BrowserControlsManager.java:568)
12-20 21:00:23.805 27537 27537 I crdebug : 6] updateBrowserControlsOffsets(BrowserControlsManager.java:675)
12-20 21:00:23.805 27537 27537 I crdebug : 7] onOffsetsChanged(BrowserControlsManager.java:612)
12-20 21:00:23.805 27537 27537 I crdebug : 8] access$400(BrowserControlsManager.java:55)


### tw...@chromium.org (2021-12-20)

> 12-20 21:00:23.804 27537 27537 I crdebug : updateBrowserControlsOffsets: top-control-offset: -196 top-content-offset: 0

This is hiding the controls?

Is there any way to cancel or reverse this since we technically should have exited fullscreen already and therefore don't want controls hidden.

> 12-20 21:00:23.804 27537 27537 I crdebug : maybeEnterFullscreenFromPendingState controls-hidden: true pending-option: null

Here, controls are hidden and pending options are null so this method will do nothing, right? I wonder if we should actually be reshowing the controls at this point?

### ji...@chromium.org (2021-12-21)

> This is hiding the controls?

> Is there any way to cancel or reverse this since we technically should have exited fullscreen already and therefore don't want controls hidden.

It is not easy to see what triggered this offset change when the event is invoked. So the cancellation/reversal might have a side effect.

> Here, controls are hidden and pending options are null so this method will do nothing, right? I wonder if we should actually be reshowing the controls at this point?

This sounds more promising. There could be other reasons the fullscreen sequence gets interrupted in the middle, but it would be fine to restore the browser controls in any case. Verified that this fixes the bug. crrev.com/c/3351312


### tw...@chromium.org (2021-12-22)

CL in-flight here & approved: https://chromium-review.googlesource.com/c/chromium/src/+/3351312
Submitting w/ a request to add a test as follow-up.

### gi...@appspot.gserviceaccount.com (2021-12-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5826dba7f25f6915bebf2711f8258f8f56b81439

commit 5826dba7f25f6915bebf2711f8258f8f56b81439
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Wed Dec 22 18:11:10 2021

Android: Restore omnibox when fullscreen gets canceled

Omnibox needs restoring if the process of entering fullscreen was
interrupted in the middle. This prevents a newly loaded URL
from being shown without the omnibox.

Bug: 1270593
Change-Id: I6e2f31f6552d030cd0098853abec1f885fd281da
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3351312
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Theresa Sullivan <twellington@chromium.org>
Cr-Commit-Position: refs/heads/main@{#953585}

[modify] https://crrev.com/5826dba7f25f6915bebf2711f8258f8f56b81439/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java


### ji...@chromium.org (2022-01-04)

Unfortunately the CL above had a regression https://crbug.com/chromium/1283531  FullscreenHtmlApiHandler.maybeEnterFullscreenFromPendingState is also called with the same boolean |controlsHidden|(true) when entering the persistent fullscreen mode by the page being scrolled down. Previously the method didn't do anything but now the new code added in the CL gets triggered, and restores the omnibox.

I'm trying to figure out a way to tell them apart. If that's not easy, doing this in TabObserver.onPageLoadFinished if the omnibox is hidden (as suggested at https://crbug.com/chromium/1270593#c7) could be a way to go.




### tw...@chromium.org (2022-01-04)

>  entering the persistent fullscreen mode by the page being scrolled down

Just confirming, this is from FullscreenHtmlApiHandler around line 194, where we're observing browser controls state and trying to enter fullscreen mode when controls are full hidden? Looking at the code again after break, that make sense.. sorry we missed it the first time!

In the failure case for this bug, since we start with a call to #enterPersistentFullscreenMode (right?), I wonder if we could explore setting up some tracking in FullscreemHtmlApiHandler to know that we started entering fullscreen mode & never finished when #maybeEnterFullscreenFromPendingState is called.

I'm a bit wary of #onPageLoadFinished.. quoting CL comment: Should we actually show the omnibox when a page load is started? Also, is it ever possible to load a URL without exiting fullscreen (not sure off hand)?

### gi...@appspot.gserviceaccount.com (2022-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/928a8265d3000206a8b11073e983010bb64cb8f4

commit 928a8265d3000206a8b11073e983010bb64cb8f4
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Wed Jan 05 03:51:42 2022

Revert "Android: Restore omnibox when fullscreen gets canceled"

This reverts commit 5826dba7f25f6915bebf2711f8258f8f56b81439.

Reason for revert: numerous regressions 

Original change's description:
> Android: Restore omnibox when fullscreen gets canceled
>
> Omnibox needs restoring if the process of entering fullscreen was
> interrupted in the middle. This prevents a newly loaded URL
> from being shown without the omnibox.
>
> Bug: 1270593
> Change-Id: I6e2f31f6552d030cd0098853abec1f885fd281da
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3351312
> Reviewed-by: Theresa Sullivan <twellington@chromium.org>
> Commit-Queue: Theresa Sullivan <twellington@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#953585}

Bug: 1270593, 1282326, 1282325, 1283531
Change-Id: I1ea3460e2d1f6f2b242ac54e6b2cb566067662ac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3362751
Reviewed-by: Jinsuk Kim <jinsukkim@chromium.org>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#955530}

[modify] https://crrev.com/928a8265d3000206a8b11073e983010bb64cb8f4/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java


### ji...@chromium.org (2022-01-05)

|mPendingFullscreenOption| is nulled out both when fullscreen request gets canceled in the middle at pending state[1]  and when fullscreen is entered successfully[2].  Therefore it is not possible to tell the two cases apart - whether we are back in normal screen mode by a canceled request or by exit after a successful fullscreen mode.  

> In the failure case for this bug, since we start with a call to #enterPersistentFullscreenMode (right?), I wonder if we could explore setting up some tracking in FullscreemHtmlApiHandler to know that we started entering fullscreen mode & never finished when #maybeEnterFullscreenFromPendingState is called.

Ack. The approach I'm taking in crrev.com/c/3362010 is, instead of nulling out |mPendingFullscreenOption| for a canceled fullscreen request, it flips a flag inside the option to record the cancel event. This is for FullscreenHtmlApiHandler internal use only, invisible to the classes outside the package that reference the option object (not used by the equality either). The flag then can be used later in #maybeEnterFullscreenFromPendingState to restore the omnibox for the situation in interest. Only after then, the option gets nulled out.


[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java;l=378;drc=affba65e089bc0d7c2c1720f6d12e12a5cf32ae0
[2] 
https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java;l=363;drc=affba65e089bc0d7c2c1720f6d12e12a5cf32ae0


### gi...@appspot.gserviceaccount.com (2022-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/57192a3615a7aae0e4ace6558965f355c2e0ec27

commit 57192a3615a7aae0e4ace6558965f355c2e0ec27
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Fri Jan 07 02:13:46 2022

Android: Handle fullscreen requests canceled at pending state

Introduces a new flag |mCanceled| in pending fullscreen option. This
is set to true when the fullscreen request gets canceled at pending
state, therefore browser controls needs restoring.

Bug: 1270593
Change-Id: Idd63f53317fbdc3560cee5ae374befb98a759a0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3362010
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#956338}

[modify] https://crrev.com/57192a3615a7aae0e4ace6558965f355c2e0ec27/chrome/browser/fullscreen/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenOptions.java
[modify] https://crrev.com/57192a3615a7aae0e4ace6558965f355c2e0ec27/chrome/android/java/src/org/chromium/chrome/browser/tab/TabBrowserControlsConstraintsHelper.java
[modify] https://crrev.com/57192a3615a7aae0e4ace6558965f355c2e0ec27/chrome/android/chrome_junit_test_java_sources.gni
[modify] https://crrev.com/57192a3615a7aae0e4ace6558965f355c2e0ec27/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[add] https://crrev.com/57192a3615a7aae0e4ace6558965f355c2e0ec27/chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerUnitTest.java


### ji...@chromium.org (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

Requesting merge to extended stable M96 because latest trunk commit (956338) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (956338) appears to be after stable branch point (938553).

Requesting merge to dev M98 because latest trunk commit (956338) appears to be after dev branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-08)

Merge review required: M98 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-08)

Merge review required: M97 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-08)

Merge review required: M96 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2022-01-10)

+Amy (Security TPM) for merge review

### am...@chromium.org (2022-01-10)

hi jinsukkim@, since this fix was just landed late last week following the revert, please update with responses to one of the merge review questionnaire in https://crbug.com/chromium/1270593#c29-31. Thank you! 

### ji...@chromium.org (2022-01-10)

1. Why does your merge fit within the merge criteria for these milestones? Bug fix for a high-severity security issue
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit. crrev.com/c/3362010
3. Have the changes been released and tested on canary? Yes
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels? No
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2022-01-11)

Merge approved to m98, please merge to branch 4758 as soon as possible (before 12p PST, Tuesday, 11 January) so this fix can be included the next beta release on Wednesday. Thanks! 

### gi...@appspot.gserviceaccount.com (2022-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5342e92ac42713522f09dd71292bd8fd62181a29

commit 5342e92ac42713522f09dd71292bd8fd62181a29
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Tue Jan 11 21:00:01 2022

Android: Handle fullscreen requests canceled at pending state

Introduces a new flag |mCanceled| in pending fullscreen option. This
is set to true when the fullscreen request gets canceled at pending
state, therefore browser controls needs restoring.

(cherry picked from commit 57192a3615a7aae0e4ace6558965f355c2e0ec27)

Bug: 1270593
Change-Id: Idd63f53317fbdc3560cee5ae374befb98a759a0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3362010
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#956338}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3381299
Cr-Commit-Position: refs/branch-heads/4758@{#518}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/5342e92ac42713522f09dd71292bd8fd62181a29/chrome/browser/fullscreen/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenOptions.java
[modify] https://crrev.com/5342e92ac42713522f09dd71292bd8fd62181a29/chrome/android/java/src/org/chromium/chrome/browser/tab/TabBrowserControlsConstraintsHelper.java
[modify] https://crrev.com/5342e92ac42713522f09dd71292bd8fd62181a29/chrome/android/chrome_junit_test_java_sources.gni
[modify] https://crrev.com/5342e92ac42713522f09dd71292bd8fd62181a29/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[add] https://crrev.com/5342e92ac42713522f09dd71292bd8fd62181a29/chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerUnitTest.java


### am...@google.com (2022-01-11)

merge approved for M96 and M97, please merge to branches 4664 and 4692 respectively, before noon PST on Friday, 14 Jan, so this fix can be included in the next extended and stable channel security refreshes -- thank you! 

### am...@google.com (2022-01-11)

sorry, please ignore my deadline for the M96 merge since this is an Android fix (and Android is not impacted by Extended release), but please do still merge the fix to Extended/96, we are trying to keep all current release channels up to date with relevant security patches for embedders. ty!

### gi...@appspot.gserviceaccount.com (2022-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/708b1652778fffdb76a2e54a9cd6ffa3809f622f

commit 708b1652778fffdb76a2e54a9cd6ffa3809f622f
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Wed Jan 12 01:42:41 2022

Android: Handle fullscreen requests canceled at pending state

Introduces a new flag |mCanceled| in pending fullscreen option. This
is set to true when the fullscreen request gets canceled at pending
state, therefore browser controls needs restoring.

(cherry picked from commit 57192a3615a7aae0e4ace6558965f355c2e0ec27)

Bug: 1270593
Change-Id: Idd63f53317fbdc3560cee5ae374befb98a759a0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3362010
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#956338}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3380265
Cr-Commit-Position: refs/branch-heads/4664@{#1387}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/708b1652778fffdb76a2e54a9cd6ffa3809f622f/chrome/browser/fullscreen/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenOptions.java
[modify] https://crrev.com/708b1652778fffdb76a2e54a9cd6ffa3809f622f/chrome/android/java/src/org/chromium/chrome/browser/tab/TabBrowserControlsConstraintsHelper.java
[modify] https://crrev.com/708b1652778fffdb76a2e54a9cd6ffa3809f622f/chrome/android/chrome_junit_test_java_sources.gni
[modify] https://crrev.com/708b1652778fffdb76a2e54a9cd6ffa3809f622f/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[add] https://crrev.com/708b1652778fffdb76a2e54a9cd6ffa3809f622f/chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerUnitTest.java


### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-13)

Congratulations! The VRP Panel has decided to award you $7500 for this report. Thank you for reporting this issue to us and great work! 

### go...@chromium.org (2022-01-14)

M97 merge is reporting CQ failure - https://chromium-review.googlesource.com/c/chromium/src/+/3379752.
Multiple retried didn't help - https://ci.chromium.org/p/chromium-m97/builders/try/android-marshmallow-arm64-rel?limit=100. So we won't be able to take this merge in for next week't M97 respin.

+benmason@ as FYI

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### su...@gmail.com (2022-01-16)

> Congratulations! The VRP Panel has decided to award you $7500 for this report. Thank you for reporting this issue to us and great work!

Thank you very much for the reward! I really appreciate it!

### [Deleted User] (2022-01-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@google.com (2022-01-18)

As per https://crbug.com/chromium/1270593#c42, merge to M97 is failing so won't be able to take this for this week's re-spin.

### gi...@appspot.gserviceaccount.com (2022-01-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e2d4274e25bc2d642f99c6cee97b5015ff67c9af

commit e2d4274e25bc2d642f99c6cee97b5015ff67c9af
Author: Jinsuk Kim <jinsukkim@chromium.org>
Date: Fri Jan 21 00:34:04 2022

Android: Handle fullscreen requests canceled at pending state

Introduces a new flag |mCanceled| in pending fullscreen option. This
is set to true when the fullscreen request gets canceled at pending
state, therefore browser controls needs restoring.

(cherry picked from commit 57192a3615a7aae0e4ace6558965f355c2e0ec27)

Bug: 1270593
Change-Id: Idd63f53317fbdc3560cee5ae374befb98a759a0b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3362010
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#956338}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3379752
Reviewed-by: Krishna Govind <govind@chromium.org>
Commit-Queue: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#1469}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/e2d4274e25bc2d642f99c6cee97b5015ff67c9af/chrome/browser/fullscreen/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenOptions.java
[modify] https://crrev.com/e2d4274e25bc2d642f99c6cee97b5015ff67c9af/chrome/android/java/src/org/chromium/chrome/browser/tab/TabBrowserControlsConstraintsHelper.java
[modify] https://crrev.com/e2d4274e25bc2d642f99c6cee97b5015ff67c9af/chrome/android/chrome_junit_test_java_sources.gni
[modify] https://crrev.com/e2d4274e25bc2d642f99c6cee97b5015ff67c9af/chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandler.java
[modify] https://crrev.com/e2d4274e25bc2d642f99c6cee97b5015ff67c9af/chrome/android/junit/src/org/chromium/chrome/browser/read_later/ReadingListUtilsUnitTest.java
[add] https://crrev.com/e2d4274e25bc2d642f99c6cee97b5015ff67c9af/chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerUnitTest.java


### am...@chromium.org (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1270593?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>FullScreen, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057930)*
