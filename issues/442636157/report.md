# Chrome on Android: URL spoof triggered by address bar position Change

| Field | Value |
|-------|-------|
| **Issue ID** | [442636157](https://issues.chromium.org/issues/442636157) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Chrome Version** | 141.0.0.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pn...@chromium.org |
| **Created** | 2025-09-03 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# Steps to reproduce the problem

1. Open the test case page and tap the "Try it" button.
2. Keep your finger pressed inside the page until an alert dialog appears.
3. Try to move the address bar to the bottom, then dismiss the alert dialog.

# Problem Description

When moving the Chrome address bar to the bottom of the screen, the URL displayed in the address bar changes to google.com/csi, but the actual page content does not correspond to this URL. This mismatch between the visible URL and page content can mislead users into believing they are on a trusted site when they are not, potentially enabling URL spoofing attacks. This behavior poses a security risk by undermining user trust in the address bar’s accuracy.

This issue appears to be similar to [Issue 437147699](https://issues.chromium.org/issues/437147699), which also involves URL spoofing vulnerabilities related to address bar inconsistencies.

# Summary

Chrome on Android: URL spoof triggered by address bar position Change

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A \

## Attachments

- [testcase.html](attachments/testcase.html) (text/html, 921 B)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 313.9 KB)
- [screen-20250903-203504.mp4](attachments/screen-20250903-203504.mp4) (video/mp4, 5.7 MB)
- [screen-20250904-043644.mp4](attachments/screen-20250904-043644.mp4) (video/mp4, 7.9 MB)
- [screen-20250905-225353.mp4](attachments/screen-20250905-225353.mp4) (video/mp4, 6.6 MB)
- [screen-20250910-183221.mp4](attachments/screen-20250910-183221.mp4) (video/mp4, 13.8 MB)
- [screen-20250912-223243~2.mp4](attachments/screen-20250912-223243~2.mp4) (video/mp4, 3.4 MB)
- [cam2.html](attachments/cam2.html) (text/html, 1.1 KB)

## Timeline

### el...@chromium.org (2025-09-03)

Security shepherd: thanks for the report.

Since this requires the user to actually decide to move the omnibox themselves during a critical moment, this is a low-severity security bug. That said, -> pnoland@ who worked on [issue 437147699](https://issues.chromium.org/issues/437147699). I have not reproed this myself locally yet, but I'm going to assume it affects all channels.

### ch...@gmail.com (2025-09-03)

Thanks for the response.

Just wanted to note that I'm able to consistently reproduce the issue even after dismissing the alert dialog — the spoofed state persists beyond the "critical moment" mentioned. This means the user doesn't need to move the omnibox during the alert; it can happen afterward as well.

### ch...@gmail.com (2025-09-04)

I’d like to respectfully request reconsideration of the severity level. Currently, it's marked as S3, but I believe it warrants an S2 classification based on the following:

Persistence beyond user interaction: The spoofed state continues even after the alert dialog is dismissed, meaning the user does not have to interact during a critical moment for the issue to remain exploitable. This significantly lowers the bar for exploitation.

Potential for user deception: The spoofed UI can remain in place long enough to mislead users into taking sensitive actions (e.g., entering credentials), which aligns more with S2 impact guidelines.

Consistent reproducibility: As shown in the attached video (screen-20250903-203504.mp4), the issue can be reproduced reliably, further increasing its practical impact.

Given that the spoof persists beyond the original interaction point and may lead to real-world phishing scenarios, I believe an S2 classification more accurately reflects the risk to users.

### pn...@chromium.org (2025-09-04)

> Consistent reproducibility

N of 1, but I haven't been able to reproduce consistently at all. Once or twice across dozens of attempts. It may be experiment-dependent, so sharing chrome://version could help. This could be down to this being a race condition and my devices having different timing.

> Persistence beyond user interaction: The spoofed state continues even after the alert dialog is dismissed,

That's true, but we know that a user choosing to change the position of the toolbar is a rare event (most users will never do it; of the users who do perform this action, most will do it once or twice) and the user still has to choose to do it while on the spoofed site. This makes the attack less practical.

> Potential for user deception: The spoofed UI can remain in place long enough to mislead users into taking sensitive actions (e.g., entering credentials), which aligns more with S2 impact guidelines.

Are you sure about the entering credentials scenario? What happens if you add a form field to the proof of concept and then focus it in the spoofed state?

### ch...@gmail.com (2025-09-04)

I tested this on Chrome Canary (version 141.0.7388.0), and I updated my PoC (https://lbstyle.github.io/alert.html) with a few changes:

I adjusted the timing to increase reliability.

I replaced the example with an input field to simulate a realistic credential entry scenario.

In this spoofed state, I was able to focus the input field and enter information as if I were on a legitimate page — the spoof remained visually convincing throughout. This suggests the spoofed UI is not only persistent but also interactive, which could potentially mislead users into entering sensitive data.

### pn...@chromium.org (2025-09-04)

Thank you for updating the PoC. I still can't repro with Canary 142.0.7392.0 or Stable but I will try some more tomorrow.

If you interact with the omnibox in the spoofed state, what happens? What is the reported url of the current page?

### ch...@gmail.com (2025-09-04)

Thanks for following up. Actually, in the spoofed state, the omnibox is not clickable or interactable at all—even when I try to tap on it, it doesn’t respond or open.

### pn...@chromium.org (2025-09-04)

I have a theory about what's happening here. The key is this:

> Keep your finger pressed inside the page until an alert dialog appears.

There is code that suppresses toolbar captures until all active gestures end. Some testing shows that this code is not very robust and can end up in a state where we indefinitely suppress or allow captures due to an imbalance of gesture end and begin events. In this case, I think we're missing the end event for the gesture and the capture ends up being indefinitely stale. Changing the toolbar position shows the captured bitmap during the animation, and apparently sometimes afterwards (this part I could not repro and is probably a different bug).

### pn...@chromium.org (2025-09-04)

I think I've reproed the "probably a different bug" part of this issue, where the toolbar becomes un-responsive because only the capture is showing. I think this state is independent of whether the capture is stale or not; I reproed it with an up to date capture.
In this state, we are neither:

- Calling BrowserControlsManager#scheduleVisibilityUpdate when calling setControlsPosition (normal when BCIV is on) nor
- Receiving browser controls offset change events in BrowserControlsManager, which would also cause us to call scheduleVisibilityUpdate

The result is we show the capture but the toolbar view is hidden and uninteractive. This might be related to BCIV; hopefully Peilin can help out regardless.

### dx...@google.com (2025-09-04)

Project: chromium/src  

Branch:  main  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/6917456>

Reset active gesture count on tab change or crash

---


Expand for full commit details
```
     
    The active gesture count suppresses captures until the gesture ends. 
    This value can become invalid if we don't receive a balanced number of 
    acks for gesture begins and ends. Two ways that can happen are changing 
    tabs between acks or crashes; regardless, it's safe to reset the value 
    in both these cases. 
     
    Bug: 442636157, 434751393 
    Change-Id: Idb6be4ed8b53bdc2e2f594db01813c2e13c52801 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6917456 
    Reviewed-by: Sky Malice <skym@chromium.org> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1511136}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/compositor/CompositorViewHolder.java`

---

Hash: [649828b3c37c0b4b23f61857c6c0398e7ee590e8](https://chromiumdash.appspot.com/commit/649828b3c37c0b4b23f61857c6c0398e7ee590e8)  

Date: Thu Sep 4 20:57:15 2025


---

### ch...@gmail.com (2025-09-05)

Thanks for the quick fix — I really appreciate you digging into this. The explanation helped clarify a lot too!

### pe...@google.com (2025-09-05)

Just curious, how do we get from google.com/csi to about:blank back to google.com? The button just opens a new window and triggers an alert right?

### ch...@gmail.com (2025-09-05)

Yes, exactly — it just opens a new window and triggers an alert.

### pn...@chromium.org (2025-09-05)

To be clear, you no longer see "google.com/csi" in the address bar when reproducing this bug? Is the omnibox still unresponsive?

### pe...@google.com (2025-09-05)

No I didn't try to reproduce it yet, I was just looking at the video.

### ch...@gmail.com (2025-09-05)

Correct — I'm no longer seeing google.com/csi appear in the address bar when reproducing the issue.

### pe...@google.com (2025-09-08)

There isn't a navigation to google.com/csi though?

### ch...@gmail.com (2025-09-08)

No, it doesn’t navigate to google.com/csi.

### ch...@gmail.com (2025-09-10)

Just an update — I was able to reproduce the issue today on Canary 142.0.7401.0, and I do see a navigation to google.com/csi. Not sure what changed since last time, but the bug is happening again on my end.

### pe...@google.com (2025-09-10)

Is google.com/csi the url of another tab you have open? Or did you visit there first before going to your test page? Still confused where this comes from.

### ch...@gmail.com (2025-09-10)

After landing the patch, I initially couldn’t reproduce the bug when testing on Canary, as I wasn’t able to access google.com/csi. However, today I was able to reproduce the issue because I could access google.com/csi on Canary.

### pe...@google.com (2025-09-10)

I still don't understand where this url is coming from. When you say "access google.com/csi" what exactly are you referring to? Is it navigating to chrome://version? I just get a 404 when navigating to google.com/csi

### ch...@gmail.com (2025-09-10)

I think the confusion is from differences across devices. On my Android device (Pixel 7 Pro), window.open("https://www.google.com/csi") actually opens that URL and briefly shows it in the address bar. Then I overwrite the contents using document.write(), and it switches to about:blank with the alert.

On my another device (Samsung) (like yours), it seems the browser never completes the navigation to google.com/csi, and it opens directly to about:blank, so the spoofing behavior doesn’t trigger the same way. That’s why the URL doesn’t appear for you.

### ch...@gmail.com (2025-09-11)

Just to clarify — when you mentioned google.com/csi, did you mean https://www.google.com/csi or https://google.com/csi?

I ask because there’s a subtle difference between the two:
https://www.google.com/csi loads a blank page (200 OK, no content)

https://google.com/csi shows a visible 404 error page
That difference can affect whether the spoof works or not, depending on timing and device behavior.

### ch...@gmail.com (2025-09-11)

deleted

### ch...@gmail.com (2025-09-11)

After reinstalling my Canary build, I can no longer reproduce the bug — once the tab opens, it no longer shows https://www.google.com/csi in the address bar at all. Not sure what changed exactly, but the navigation doesn't appear anymore.

### ch...@gmail.com (2025-09-11)

Since I can no longer reproduce the issue — the navigation to https://www.google.com/csi no longer appears in the address bar — should this be considered fixed, or is there still more work needed here?

### pe...@google.com (2025-09-12)

I'm not confident enough to say this is fixed.

### ch...@gmail.com (2025-09-12)

Just a quick note — although I can’t repro the original behavior anymore, I’ve found another way to reproduce a similar issue, which might still be part of the same underlying bug. I’ll share more details shortly.

### ch...@gmail.com (2025-09-12)

1. Make sure the Chrome omnibox is at the bottom of the screen.

2. Visit https://lbstyle.github.io/ios.html
 and tap the button.

3. In the newly opened tab, wait until the g.cn page automatically navigates to https://lbstyle.github.io/cam2.html.

4.Now try to move the omnibox to the top.



### pe...@google.com (2025-09-15)

hmmm I'm seeing something else, my toolbar either doesn't move or disappears. Either way, there's a bug here. What is https://lbstyle.github.io/cam2.html doing? Is it just constantly refreshing itself?

### ch...@gmail.com (2025-09-15)

Yes.

### yf...@google.com (2025-09-15)

Are the previous issues still present? The issue in #31 is arguably a denial-of-service (at least how I see it on 2x devices). The outer page is just navigating your tab every second. Not ideal, but also not a realistic attack - if I were to try and interact with the content area the page would reload on me, anyway, right? Also, I don't see the old url on the bottom, the whole page is white, and there's jut the progress bar below the omnibox (and no omnibox) until it eventualy comes in or I minimize chrome and come back which seems to force it to be correct.

Anyway, all this to say, the most recent issue is a bug (and agreed there's likely still a timing bug in there) but I'm not convinced it's severe in #31

### ch...@gmail.com (2025-09-15)

You're right. The issue in #31 is more of a disruption than a critical security concern. While it does cause some UI problems, it's not a realistic attack, and as you mentioned, the page reloads on interaction, which mitigates any potential risks. Thanks for the clarification!

Also, regarding the original issue, I no longer see https://www.google.com/csi appear in the address bar on my Canary build. Since I no longer see the URL before the alert displays, I’m not able to reproduce the original bug anymore. This is the same behavior I described in comment #17, where I used to see https://www.google.com/csi briefly before the alert showed, but that no longer happens. It seems like that issue has been resolved on my end."

### yf...@google.com (2025-09-16)

Excellent, thanks for confirming! So it sounds like the fix in #11 is sufficient for this reported issue.

That said, we're still wary of races in this part of the codebase and are adding some instrumentation to try and debug issues that are detected

### ch...@gmail.com (2025-10-02)

Any update on this bug? thanks.

### pn...@chromium.org (2025-10-02)

I think the originally reported issue is fixed and can be marked as such; can you file a new bug for the issue reported in #31?

### ch...@gmail.com (2025-10-03)

I've filed a new bug for the issue mentioned in comment #31: Issue 448915976. Let me know if anything else is needed.

### sp...@google.com (2025-10-22)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

the panel determined that a reasonable and prudent user would not be put at risk by this bug given the level of interactions required

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-01-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> the panel determined that a reasonable and prudent user would not be put at risk by this bug given the level of interactions required
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https:/

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/442636157)*
