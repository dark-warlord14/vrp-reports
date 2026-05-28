# Video Document In Document spoof login box

| Field | Value |
|-------|-------|
| **Issue ID** | [397878997](https://issues.chromium.org/issues/397878997) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ke...@gmail.com |
| **Assignee** | bk...@google.com |
| **Created** | 2025-02-20 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description

Video Document In Document spoof login box

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

Google Chrome

---

### The problem

#### Please describe the technical details of the vulnerability

### NOTE: Report is attached which will show images

### Description

A vulnerability in Google Chrome’s Picture-in-Picture (PiP) feature allows an attacker to display a persistent, fake authentication prompt—mimicking trusted interfaces like Apple’s login or Okta’s password box. This is done by having a video that looks exactly like a login box which does not show the origin. The main window will pickup the keystrokes. Although PiP requires user activation, the nearly 5-second timeout on transient activation (<https://developer.mozilla.org/en-US/docs/Glossary/Transient_activation>) can be exploited to show the deceptive popup while the user is on a completely different workspace. You can use the `blur` event to detect this.

<https://developer.mozilla.org/en-US/docs/Web/API/DocumentPictureInPicture/requestWindow>

#### System Details

Version tested: Version 131.0.6778.265 (Official Build) (arm64)  

OSX: Sonoma 14.5
Macbook Pro M3

### Proof of concept

1. Visit <https://com.apple.securityd.auth.system.service.scopefense.com/pocwin.html>
2. Click **Get pwned** (This could be any normal activity that triggers the transient activation)

[image:441c82ab-aedc-464d-adf1-ebf379ddf0ea]

3. The victim is likely to trust the prompt—believing it to be a legitimate out-of-browser request—and may enter credentials that can be stolen.

[image:3d3f589c-2bde-4ad6-86af-958f8827e9ef]

When they enter the password the video src tag will be switched everytime so it looks like a correct password entry. Since the video tag listens for enter tag to close the box, it will close when people click enter. The domain name does not matter as it is never shown

Video of the attack is provided here: <https://drive.proton.me/urls/KASADP51V8#Ma54GF0Ida1b>

### Impact

Users typically recognize legitimacy through persistent, out-of-browser popups. This vulnerability undermines that assurance, enabling attackers to create convincing fake login interfaces (such as OKTA, Google Auth, or 2FA prompts) with minimal visible indicators of their true origin.

### Remediation

Origin needs to be shown on video boxes as they can resemble web pages. Furthermore the transient keys should switch to sticky keys.

#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Everyone can exploit it and they can pop a fake window that looks exactly like common login boxes, which could trigger the user to enter credentials

---

### The cause

#### What version of Chrome have you found the security issue in?

Version 131.0.6778.265 (Official Build) (arm64)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Security UI Spoofing

#### How would you like to be publicly acknowledged for your report?

Kevin Joensen

## Attachments

- [finding (23).pdf](attachments/finding (23).pdf) (application/pdf, 2.8 MB)
- [pocwin.html](attachments/pocwin.html) (text/html, 2.2 KB)
- [v4.mp4](attachments/v4.mp4) (video/mp4, 623.3 KB)
- [v2.mp4](attachments/v2.mp4) (video/mp4, 647.3 KB)
- [v1.mp4](attachments/v1.mp4) (video/mp4, 964.4 KB)
- [v3.mp4](attachments/v3.mp4) (video/mp4, 1.0 MB)
- [Screen Recording 2025-02-20 at 11.56.07.mov](attachments/Screen Recording 2025-02-20 at 11.56.07.mov) (video/quicktime, 11.7 MB)
- [finalpoc.mov](attachments/finalpoc.mov) (video/quicktime, 37.8 MB)

## Timeline

### ke...@gmail.com (2025-02-20)

There is also the question of where the window is initially placed which is in the bottom right corner. This can be fixed by simply very quickly adding a large video and then a small video. Then the small video will start from the large videos top left corner. Hence you can now control the exact location.

I've made a small PoC where i move the window higher than initially simply by changing the video src. This can also be used to move it to the far top left corner.



### mp...@google.com (2025-02-21)

CC steimel@ from [issue 397460353](https://issues.chromium.org/issues/397460353)

### ke...@gmail.com (2025-02-21)

Here is the final PoC imitating a system upgrade from osx and stealing the users password. This is using the trick to place the window in the center to more properly cheat the user.

https://com.apple.securityd.auth.system.service.scopefense.com/pocfinal.html (There might be some delay on click due to fetching .mp4.. In a real attack this could easily be optimized out, so it looks like the video)

A video is attached also:

### mp...@google.com (2025-02-21)

Those are impressive PoCs. There are two issues:

1. This is unfortunately how OSes have chosen to implement security dialogs. They're awfully spoofable, but there's really not a whole lot we can do on the Chrome side.
2. On my machine the PIP window starts very small and in a weird corner of the screen, and if I hover over it with my mouse, it blurs and asks if I want to go back to the tab. I think that would alert a lot of people.

I assigned steimel@ to see if there's anything we can do. Maybe a border? Flash the origin above the video? Disallow borderless videos without a permission? It's tough to thread the needle between usability and mitigating hypothetical spoofs here.

### ke...@gmail.com (2025-02-21)

Thanks!

1. Fair enough
2. What machine are you on? I've tested on multiple macs and get the same result where it immediately pops to the right placement. Maybe there is some problems with videos loading too slow which ruins the quick src change. This can be fixed.

One additional mitigating idea would be disallowing hotswapping of the src attribute as soon as it is handed over to the PiP window. This is what allows me to flip between videos which mimics users entering their password.

### ke...@gmail.com (2025-02-25)

I don't know if there was some cache problems but the newest working payload is available here: https://com.apple.securityd.auth.system.service.scopefense.com/pocfinal.html

I just updated it as i had troubles reproducing, but it is reproducable now.

### ke...@gmail.com (2025-03-10)

Any updates on this?

### ke...@gmail.com (2025-03-24)

Hi team,

Just a gentle reminder. Any updates on this?

Best regards,

### ma...@google.com (2025-03-31)

(Re [#comment5](https://issues.chromium.org/issues/397878997#comment5):

> On my machine the PIP window starts very small and in a weird corner of the screen

The updated PoC linked from [#comment4](https://issues.chromium.org/issues/397878997#comment4) uses a trick where the PiP video is swapped for another one with different dimensions to achieve basically arbitrary placement on screen IIUC.)

### ke...@gmail.com (2025-04-09)

Hi Team,

It has been some months now. Is it possible to determine whether this is a vulnerability or not? I would really appreciate if this is determined so I can either wait or publish my research. As the comment above also mentions, **the PiP is placed arbitrarily, with arbitrary size**. It has to be a vulnerability, but if you don't agree, i'd just like to publish the research instead.

Best regards,
Kevin.

### st...@chromium.org (2025-04-09)

I agree that being able to move/resize the video pip window like that is a bug we need to fix

### ke...@gmail.com (2025-04-25)

Hi again,

Any updates on this?

### ke...@gmail.com (2025-05-08)

Hey team,

Ping.

### ke...@gmail.com (2025-05-19)

Hey Team,

Any updates on this?

Best regards,
Kevin.

### am...@chromium.org (2025-05-21)

Hi PiP / Media folks, from a security standpoint what is presented here would be considered a vulnerability, especially as presented via the POC and video demonstration in c#4. While we do *not* consider the lack of origin on the PiP window to be a security issue - that is WAI. We so, however, consider the issue of moving and resizing the window to the extent and degree presented to be a security issue, especially while also allowing for PiP to display arbitrary interactive content.

The most recent POC allows for a fairly convincing spoofing of MacOS security dialogs through video in the PiP window, presented in such as way that a user could be convinced to type a password that would be captured by the malicious website. I believe that given the newest POC, this should be considered medium / S2 severity rather than low. It probably should have been re-evaluated for severity following the updating of the POC originally provided in [comment #4](https://issues.chromium.org/issues/397878997#comment4) when the new payload / POC update was provided on 25 February.

In terms of c#12 it seems like to some extent the engineering team agrees this is something that should be resolved. Can an update please be provided here if this is still planned?

### ch...@google.com (2025-05-22)

steimel: Uh oh! This issue still open and hasn't been updated in the last 42 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### li...@chromium.org (2025-05-22)

This is a well-known potential abuse case; I remember doing something similar with the google login some years ago.  To be clear, this could be even more convincing: the site could, for example, update the image in the video pip window to add or remove circles as the user types keys / backspaces in the browser window.

As c#5 points out, the nature of OS-level prompts like this make them very easy to spoof.  The forced blur/back-to-tab UI treatment for pip on mouseover is designed to minimize this.  folks would (hopefully) try to focus it before typing, and then (hopefully) realize that real login boxes don't show mouseover text.  Adding the origin to the mouseover is an option, though if the existing UI treatment isn't enough, i. 's not clear to me that the user would pick up on that either.

Showing the origin temporarily over the video pip window when it first opens might also help some, but i'm wary of depending too much on transient hints like that.  They're easy to miss, especially if the content of the window around them is trying to distract your eye.  For that, or permanently showing the origin on or above the window, we'd have to talk to our UX friends (+cc:ryflores).

The idea about forcing the position by varying the video size is a nice trick; i hadn't thought of that one.  Probably we can work around that somehow, such as forcing it back to its previous position if the user hasn't moved it explicitly since the last size-based move.

### ke...@gmail.com (2025-05-22)

Hi li,

I'm unsure about this "To be clear, this could be even more convincing: the site could, for example, update the image in the video pip window to add or remove circles as the user types keys / backspaces in the browser"
This is exactly what the poc does? (https://com.apple.securityd.auth.system.service.scopefense.com/pocfinal.html)
It captures keystrokes and also changes the video to add a dot, and remove a dot depending on your keystroke.


I've looked abit at the "Back to tab" hover effect, and I have a super messy poc that halts the thread responsible for the overlay, but the video plays. This gives the effect that when you hover over, the "back to tab" never shows. But it is in a rough state, and works only partly. When I have more time I can continue researching that area if needed.

Thanks for the updates!

Best regards,
Kevin.


### li...@chromium.org (2025-05-22)

Oh, that is neat.  I mashed a few keys and got to four circles before i looked at the pip window too closely. For whatever reason, the poc quits updating the circles after about four keys, so i figured it was just a static image.  But yeah, that's exactly what i was trying to say.

Anyway, as far as stopping the back to tab effect, i don't think that adds too much right now.  The first question is whether we believe that what we're doing right now is good enough at a high level or not.  Getting too much into the details at this point, well, there's a never-ending supply of weeds to get into.  Figuring out which ones to look at, if any, depends on the answer to that first question.

### ke...@gmail.com (2025-05-22)

Ah cool. I only recorded 4 keys for the PoC so that is why it breaks :D

Fair enough, that makes sense! Feel free to ping me if you need anything.

### li...@chromium.org (2025-05-22)

=> bkeen@ for load balancing.

### li...@chromium.org (2025-05-23)

TL;DR from some discussions:

- there's no complete fix for this, or a long tail of similar bugs. the best we can do is tilt the odds a bit in our favor.
- we're considering some approaches based on showing the origin temporarily in certain cases.
- that change depends on some unrelated UI changes to video pip, which are in-flight.

### ke...@gmail.com (2025-06-10)

Any news on this? I suggest moving to public disclosure if this is determined to be a backlog item (almost half a year already). Public research on this would allow users to understand that PiP's can pop and mimick login boxes at arbitrary destinations and float over other windows, even outside the browser, with pixel perfect looks.

What do you think?

### bk...@google.com (2025-06-10)

kevinjoensen@: I am working on a design based on [comment#23](https://issues.chromium.org/issues/397878997#comment23) (temporarily showing the origin). I should have an update within the next couple of weeks.

### ke...@gmail.com (2025-06-11)

Awesome that sounds great! Looking forward to seeing it.


Best regards,
Kevin.

### ch...@google.com (2025-06-25)

bkeen: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-10)

bkeen: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-07-15)

Project: chromium/src  

Branch:  main  

Author:  Benjamin Keen [bkeen@google.com](mailto:bkeen@google.com)  

Link:    <https://chromium-review.googlesource.com/6697443>

Update video picture-in-picture window title animation

---


Expand for full commit details
```
     
    This change updates the window animation by making the title (origin 
    and favicon), together with the controls top scrim, display for 5 
    seconds any time the picture-in-picture window is opened. 
     
    Any interaction with the window causes the animation to revert back to 
    the default implementation. 
     
    Reasoning for this change available at: 
    go/cme-video-pip-spoof-vulnerability-by-prompt-mimicking 
     
    Bug: 397878997 
    Change-Id: I2daf3d5915bc04d3a729a425e9a368e44d167a34 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6697443 
    Reviewed-by: Fr <beaufort.francois@gmail.com> 
    Commit-Queue: Benjamin Keen <bkeen@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1487129}

```

---

Files:

- M `chrome/browser/ui/views/overlay/video_overlay_window_views.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.h`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views_unittest.cc`

---

Hash: [247cd023ec889ccb73f505a32099cece5d6f1afb](http://crrev.com/247cd023ec889ccb73f505a32099cece5d6f1afb)  

Date: Tue Jul 15 18:54:01 2025


---

### dx...@google.com (2025-07-16)

Project: chromium/src  

Branch:  main  

Author:  [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com) [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/6758830>

Revert "Update video picture-in-picture window title animation"

---


Expand for full commit details
```
     
    This reverts commit 247cd023ec889ccb73f505a32099cece5d6f1afb. 
     
    Reason for revert: 
    LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/4809414306430976 
     
    Sample build with failed test: https://ci.chromium.org/b/8709248607020047073 
    Affected test(s): 
    [ninja://chrome/test:browser_tests/PictureInPicturePixelComparisonBrowserTest.VideoPlay](https://ci.chromium.org/ui/test/chromium/ninja:%2F%2Fchrome%2Ftest:browser_tests%2FPictureInPicturePixelComparisonBrowserTest.VideoPlay?q=VHash%3A91b15303e2090379) 
     
    If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F4809414306430976&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F6697443&type=BUG 
     
    Original change's description: 
    > Update video picture-in-picture window title animation 
    > 
    > This change updates the window animation by making the title (origin 
    > and favicon), together with the controls top scrim, display for 5 
    > seconds any time the picture-in-picture window is opened. 
    > 
    > Any interaction with the window causes the animation to revert back to 
    > the default implementation. 
    > 
    > Reasoning for this change available at: 
    > go/cme-video-pip-spoof-vulnerability-by-prompt-mimicking 
    > 
    > Bug: 397878997 
    > Change-Id: I2daf3d5915bc04d3a729a425e9a368e44d167a34 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6697443 
    > Reviewed-by: Fr <beaufort.francois@gmail.com> 
    > Commit-Queue: Benjamin Keen <bkeen@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1487129} 
    > 
     
    Bug: 397878997 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I56d01e621f23f87436b10b04c4591af1b42cf002 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6758830 
    Reviewed-by: Ming-Ying Chung <mych@chromium.org> 
    Commit-Queue: Ming-Ying Chung <mych@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Owners-Override: Ming-Ying Chung <mych@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1487377}

```

---

Files:

- M `chrome/browser/ui/views/overlay/video_overlay_window_views.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.h`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views_unittest.cc`

---

Hash: [c9ed5b66f2369599d278280878dfd0b186c4233c](http://crrev.com/c9ed5b66f2369599d278280878dfd0b186c4233c)  

Date: Wed Jul 16 02:12:52 2025


---

### dx...@google.com (2025-07-17)

Project: chromium/src  

Branch:  main  

Author:  Benjamin Keen [bkeen@google.com](mailto:bkeen@google.com)  

Link:    <https://chromium-review.googlesource.com/6759273>

Reland "Update video picture-in-picture window title animation"

---


Expand for full commit details
```
     
    This is a reland of commit 247cd023ec889ccb73f505a32099cece5d6f1afb 
     
    The failing test is fixed by forcing the title and scrim to not 
    visible, similar to how it is currently done for the controls. 
     
    Original change's description: 
    > Update video picture-in-picture window title animation 
    > 
    > This change updates the window animation by making the title (origin 
    > and favicon), together with the controls top scrim, display for 5 
    > seconds any time the picture-in-picture window is opened. 
    > 
    > Any interaction with the window causes the animation to revert back to 
    > the default implementation. 
    > 
    > Reasoning for this change available at: 
    > go/cme-video-pip-spoof-vulnerability-by-prompt-mimicking 
    > 
    > Bug: 397878997 
    > Change-Id: I2daf3d5915bc04d3a729a425e9a368e44d167a34 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6697443 
    > Reviewed-by: Fr <beaufort.francois@gmail.com> 
    > Commit-Queue: Benjamin Keen <bkeen@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1487129} 
     
    Bug: 397878997 
    Change-Id: Iae561fde0a4d9d9bece8882814056730a642e567 
    Include-Ci-Only-Tests: chromium.memory:Linux ASan LSan Tests (1)|browser_tests 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6759273 
    Commit-Queue: Benjamin Keen <bkeen@google.com> 
    Reviewed-by: Fr <beaufort.francois@gmail.com> 
    Cr-Commit-Position: refs/heads/main@{#1488536}

```

---

Files:

- M `chrome/browser/picture_in_picture/video_picture_in_picture_window_controller_browsertest.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.h`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views_unittest.cc`

---

Hash: [b2e3af66b3d34e1414ef87bee0a9a11319f688b1](http://crrev.com/b2e3af66b3d34e1414ef87bee0a9a11319f688b1)  

Date: Thu Jul 17 21:43:09 2025


---

### dx...@google.com (2025-07-18)

Project: chromium/src  

Branch:  main  

Author:  Benjamin Keen [bkeen@google.com](mailto:bkeen@google.com)  

Link:    <https://chromium-review.googlesource.com/6718973>

Implement media playback trust check for the video PiP overlay window

---


Expand for full commit details
```
     
    This change adds to the video picture-in-picture overlay window the 
    ability to check for "media playback trust". 
     
    The overlay window is considered trusted for media playback if all the 
    following conditions are met: 
      * MediaSession exists 
      * MediaSession routed frame exists 
      * The MediaSession routed frame is the primary main frame 
      * The origin URL has high media engagement or is a file 
     
    This signal will later be used to handle untrusted media playback. 
     
    Proposal document available at: 
    go/cme-video-pip-spoof-vulnerability-by-prompt-mimicking 
     
    Bug: 397878997 
    Change-Id: Ie52007d1ee17acadaf85eed5f75bd4fb58ae0f2c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6718973 
    Reviewed-by: Tommy Steimel <steimel@chromium.org> 
    Commit-Queue: Benjamin Keen <bkeen@google.com> 
    Reviewed-by: Fr <beaufort.francois@gmail.com> 
    Cr-Commit-Position: refs/heads/main@{#1489056}

```

---

Files:

- M `chrome/browser/picture_in_picture/video_picture_in_picture_window_controller_browsertest.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.h`
- M `content/test/content_test_bundle_data.filelist`
- A `content/test/data/media/picture_in_picture/iframe-one-video.html`
- M `content/test/data/media/picture_in_picture/one-video.html`

---

Hash: [4adb82512af566927fcda8574504324c27653f58](http://crrev.com/4adb82512af566927fcda8574504324c27653f58)  

Date: Fri Jul 18 21:51:29 2025


---

### ch...@google.com (2025-07-25)

bkeen: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ct...@chromium.org (2025-08-07)

Another mitigation was raised on an internal bug b/428658176 (see Comments 14 and 23) -- the Document PiP spec says that the site must not be able to move the window (https://wicg.github.io/document-picture-in-picture/#positioning), but here the multiple resizes are able to essentially polyfill that functionality. As one way to maybe address this, could we always anchor the window resizes to a "default corner" (in the common case, the lower-right corner of the window) to avoid allowing the window to move across the screen?

### bk...@google.com (2025-08-08)

That is a good approach, but I believe it comes with a couple of concerns. While anchoring the window resize to a default corner could mitigate the repositioning vulnerability, it may create an unexpected user experience as users don't expect a window to move during resize. Additionally, could this also introduce a new abuse vector? where a malicious page could entice a user to click something that is revealed under the PiP window, at the time it moves away during resize.

### dx...@google.com (2025-08-11)

Project: chromium/src  

Branch:  main  

Author:  Benjamin Keen [bkeen@google.com](mailto:bkeen@google.com)  

Link:    <https://chromium-review.googlesource.com/6824468>

Integrate media playback trust checks with title visibility

---


Expand for full commit details
```
     
    This change uses the media play trust checks and user interaction 
    criteria to determine when to hide the window title. 
     
    User interaction criteria is defined as the user intentionally 
    interacting with the picture-in-picture window, which includes the 
    following Event types: 
      * Key pressed 
      * Gesture tap 
      * Mouse pressed 
     
    There window title will remain visible, or be hidden, depending on the 
    following scenarios: 
      * If the window is trusted for media playback, the title behavior 
        remains unchanged, the title will hide after 5 seconds or on user 
        interaction 
      * If the window is not trusted for media playback: 
        * The title will remain visible after the 5 seconds timeout, if 
          there is no user interaction 
        * If the user interacts with the window before the hide timer 
          expires, the title will hide once the hide timer expires 
        * If the user interacts with the window after the hide timer 
          expires, the title will hide as normal 
     
    Note that user interaction is remembered for the lifetime of the window. 
    This means that once the user interaction criteria is met, future calls 
    to show/hide will remember the value, until the window is destroyed. 
     
    Bug: 397878997 
    Change-Id: Iba0d6dddf455652137e611cbefaa271be9484303 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6824468 
    Reviewed-by: Fr <beaufort.francois@gmail.com> 
    Commit-Queue: Benjamin Keen <bkeen@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1499753}

```

---

Files:

- M `chrome/browser/picture_in_picture/video_picture_in_picture_window_controller_browsertest.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.h`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views_unittest.cc`

---

Hash: [d1fbd5c92db9f68955367f7869d28514974af843](https://chromiumdash.appspot.com/commit/d1fbd5c92db9f68955367f7869d28514974af843)  

Date: Mon Aug 11 19:34:49 2025


---

### dx...@google.com (2025-08-11)

Project: chromium/src  

Branch:  main  

Author:  Alex Moshchuk [alexmos@chromium.org](mailto:alexmos@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6838014>

Revert "Integrate media playback trust checks with title visibility"

---


Expand for full commit details
```
     
    This reverts commit d1fbd5c92db9f68955367f7869d28514974af843. 
     
    Reason for revert: [Build gardener] Some new tests introduced in this CL are failing on linux-chromeos-chrome: 
    https://ci.chromium.org/ui/p/chrome/builders/ci/linux-chromeos-chrome/52847/test-results 
     
    Bug: 397878997 
    Original change's description: 
    > Integrate media playback trust checks with title visibility 
    > 
    > This change uses the media play trust checks and user interaction 
    > criteria to determine when to hide the window title. 
    > 
    > User interaction criteria is defined as the user intentionally 
    > interacting with the picture-in-picture window, which includes the 
    > following Event types: 
    >   * Key pressed 
    >   * Gesture tap 
    >   * Mouse pressed 
    > 
    > There window title will remain visible, or be hidden, depending on the 
    > following scenarios: 
    >   * If the window is trusted for media playback, the title behavior 
    >     remains unchanged, the title will hide after 5 seconds or on user 
    >     interaction 
    >   * If the window is not trusted for media playback: 
    >     * The title will remain visible after the 5 seconds timeout, if 
    >       there is no user interaction 
    >     * If the user interacts with the window before the hide timer 
    >       expires, the title will hide once the hide timer expires 
    >     * If the user interacts with the window after the hide timer 
    >       expires, the title will hide as normal 
    > 
    > Note that user interaction is remembered for the lifetime of the window. 
    > This means that once the user interaction criteria is met, future calls 
    > to show/hide will remember the value, until the window is destroyed. 
    > 
    > Bug: 397878997 
    > Change-Id: Iba0d6dddf455652137e611cbefaa271be9484303 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6824468 
    > Reviewed-by: Fr <beaufort.francois@gmail.com> 
    > Commit-Queue: Benjamin Keen <bkeen@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1499753} 
     
    Bug: 397878997 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I2f9c7206ea47337ba19a02d991447d10e3fc03cb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6838014 
    Owners-Override: Alex Moshchuk <alexmos@chromium.org> 
    Commit-Queue: Alex Moshchuk <alexmos@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1499869}

```

---

Files:

- M `chrome/browser/picture_in_picture/video_picture_in_picture_window_controller_browsertest.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.h`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views_unittest.cc`

---

Hash: [c8fd1ea88af1a30b51bbca0a289516e5f8ec1378](https://chromiumdash.appspot.com/commit/c8fd1ea88af1a30b51bbca0a289516e5f8ec1378)  

Date: Mon Aug 11 22:53:00 2025


---

### dx...@google.com (2025-08-18)

Project: chromium/src  

Branch:  main  

Author:  Benjamin Keen [bkeen@google.com](mailto:bkeen@google.com)  

Link:    <https://chromium-review.googlesource.com/6846700>

Reland "Integrate media playback trust checks with title visibility"

---


Expand for full commit details
```
     
    This is a reland of commit d1fbd5c92db9f68955367f7869d28514974af843 
     
    To fix the original issue we now run the tests with the feature enabled. 
     
    Original change's description: 
    > Integrate media playback trust checks with title visibility 
    > 
    > This change uses the media play trust checks and user interaction 
    > criteria to determine when to hide the window title. 
    > 
    > User interaction criteria is defined as the user intentionally 
    > interacting with the picture-in-picture window, which includes the 
    > following Event types: 
    >   * Key pressed 
    >   * Gesture tap 
    >   * Mouse pressed 
    > 
    > There window title will remain visible, or be hidden, depending on the 
    > following scenarios: 
    >   * If the window is trusted for media playback, the title behavior 
    >     remains unchanged, the title will hide after 5 seconds or on user 
    >     interaction 
    >   * If the window is not trusted for media playback: 
    >     * The title will remain visible after the 5 seconds timeout, if 
    >       there is no user interaction 
    >     * If the user interacts with the window before the hide timer 
    >       expires, the title will hide once the hide timer expires 
    >     * If the user interacts with the window after the hide timer 
    >       expires, the title will hide as normal 
    > 
    > Note that user interaction is remembered for the lifetime of the window. 
    > This means that once the user interaction criteria is met, future calls 
    > to show/hide will remember the value, until the window is destroyed. 
    > 
    > Bug: 397878997 
    > Change-Id: Iba0d6dddf455652137e611cbefaa271be9484303 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6824468 
    > Reviewed-by: Fr <beaufort.francois@gmail.com> 
    > Commit-Queue: Benjamin Keen <bkeen@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1499753} 
     
    Bug: 397878997 
    Change-Id: Ied852549f738814280a654f5ae3f2a9ae0ef16c8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6846700 
    Commit-Queue: Benjamin Keen <bkeen@google.com> 
    Reviewed-by: Fr <beaufort.francois@gmail.com> 
    Cr-Commit-Position: refs/heads/main@{#1502878}

```

---

Files:

- M `chrome/browser/picture_in_picture/video_picture_in_picture_window_controller_browsertest.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.h`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views_unittest.cc`

---

Hash: [73a1a5aecd3cb295fac563e50db2440ef12038ae](https://chromiumdash.appspot.com/commit/73a1a5aecd3cb295fac563e50db2440ef12038ae)  

Date: Mon Aug 18 19:32:23 2025


---

### ch...@google.com (2025-08-23)

bkeen: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### bk...@google.com (2025-08-25)

With <https://chromium-review.googlesource.com/6846700>, this should be fixed. I'll wait for the video controls update release (<https://crbug.com/360357715>) before closing out this bug.

### pg...@google.com (2025-09-02)

Hi Benjamin, if this bug itself is no longer a security concern, we should mark this as fixed so that we can do appropriate backmerging and/or publication of this bug!

Is <https://crbug.com/360357715> a blocker?

### bk...@google.com (2025-09-02)

Hi Grace, yes. This change depends on the video picture in picture controls update. What is the process for situations like this?

### aw...@google.com (2025-09-15)

(answering for Grace as she's sadly left the team)

I think the best approach would be to close this bug (which I'll do now), and then the automation will come along and potentially tag for merge review. Then the person doing the merge reviews will take into account that <https://chromium-review.googlesource.com/6846700> would also be needed when assessing the risk/benefit.

### ch...@google.com (2025-09-16)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### bk...@google.com (2025-09-16)

Thanks Andrew, I've added the "Fixed By Code Changes" CLs and will mark as fixed again.

Re-Adding a reminder here, for future reviewers, that this fix depends on <https://crbug.com/360357715>, which has not launched yet.

### ke...@gmail.com (2025-09-17)

Hi,

Will this get a CVE? And when will it be public?

Best regards,

### sp...@google.com (2025-09-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
UI spoofing, low impact, and mitigated.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-12-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/397878997)*
