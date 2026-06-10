# requestFullscreen should consume user activation to prevent UI/URL spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40091651](https://issues.chromium.org/issues/40091651) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Fullscreen, Blink>Input |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2018-06-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The webkitRequestFullscreen function isn't consuming user gestures, allowing an attacker to set fullscreen on two different windows with the same click. When this happens, both warning messages saying the user entered fullscreen overlap, appearing as if they were only one. When the user presses ESC to exit the first fullscreen, they won't know that the second window is also in fullscreen, allowing the attacker to spoof the UI/URL.

The exploit works as follows:

1. User accesses attacker's website and clicks on a link.
2. A popup will open displaying a video.
3. When the user clicks to start the video, both background window and the popup are set into fullscreen (both fullscreen messages appear at the same time, overlapped).
4. In parallel with step 3, the background page is spoofed (it starts displaying an image of a fake omnibox and a fake Google page.
5. When the user exits the fullscreen video, the background page will still be in fullscreen and the victim will be oblivious to that.

**VERSION**  

Versão 67.0.3396.79 (Official Build) Stable (64-bits)  

Versão 69.0.3453.0 (Official Build) Canary (64-bits)

**REPRODUCTION CASE**

1. Open <https://lbherrera.github.io/lab/double-fullscreen/index.html>
2. Click on the link.
3. After the popup shows up, click anywhere on the video.
4. The page will enter fullscreen. After a few seconds, you can close it by pressing ESC.
5. You should be seeing the background page both spoofing the omnibox as well as faking a Google page.

## Attachments

- [spoof.mp4](attachments/spoof.mp4) (video/mp4, 1.7 MB)

## Timeline

### al...@chromium.org (2018-06-14)

+mustaq@ for user gestures, +foolip@ for fullscreen.

[Monorail components: Blink>Fullscreen]

### mu...@chromium.org (2018-06-14)

Assigning to foolip@ who owns fullscreen.

I suspect we are consistent with other browsers here, right?  Is there any valid use case where a page has to make multiple request per user activation?

### fo...@chromium.org (2018-06-14)

This is presumably an easy fix implementation-wise. The compat risk that comes to mind is requesting fullscreen and playing a video at the same time, if both of those were to consume the gesture. If only one does, does the order of calling div.requestFullscreen() and video.play() matter?

### mu...@chromium.org (2018-06-14)

I agree it's perhaps a simple impl change.

Playing video doesn't consume activation at all.  Currently only APIs that consume are window.open and video picture-in-picture.  The latter is pretty new, so I don't think we could have any compat problem with fullscreen.  The only case that could be a potential problem is popup+fullscreen.  If both would consume, whichever call reaches the browser first would win.


### he...@gmail.com (2018-06-14)

#4 - popup+fullscreen shouldn't be a problem because on the current implementation, if a popup reaches the browser first, the user gesture is consumed and fullscreen isn't set. If, instead, the fullscreen reaches the browser first, the gesture isn't consumed, but when the popup is opened, the fullscreen exits automatically.

### mu...@chromium.org (2018-06-14)

Good point, thanks.

That reminded me that we had https://crbug.com/chromium/729694 for it, I think I will merge that bug into this.


### wf...@chromium.org (2018-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### fo...@chromium.org (2018-08-30)

mustaq@, would the fix simply be to switch Frame::HasTransientUserActivation to Frame::ConsumeTransientUserActivation?

### mu...@chromium.org (2018-08-30)

Right, it's that simple!

### mu...@chromium.org (2018-09-17)

One quick note on top my last comment: while we can easily switch the call from "check" to "consume", this would cause the browser (and other OOPIF processes) to be updated after the "originating" renderer.  There would be a remote possibility of a race if two separate processes try to go fullscreen at the same time.  With popups, we avoided this by consuming on browser first.  Since (unlike popups) fullscreen doesn't create a new process, I don't think we need to worry so much about possible races.

(If my assumption is wrong, and we /need/ a browser-first consumption, the fullscreen call from the renderer will perhaps need a blocking IPC to browser, which is not great either.)


### aw...@google.com (2019-01-14)

(bulk edit: herrerahlb@gmail.com is the new email address for luan.herrera@hotmail.com)

### ct...@chromium.org (2019-01-24)

[Empty comment from Monorail migration]

### ct...@chromium.org (2019-01-24)

Bumping this to Severity-Medium and P-1 due to another report (https://crbug.com/chromium/924001) that uses the same root cause to block security UX (completely blocking the fullscreen warning, which is slightly but significantly different than the reported effect here).

Adding milestone labels as well.

### sh...@chromium.org (2019-01-25)

foolip: Uh oh! This issue still open and hasn't been updated in the last 148 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

foolip: Uh oh! This issue still open and hasn't been updated in the last 163 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fo...@chromium.org (2019-02-11)

I will attempt the fix suggested in https://bugs.chromium.org/p/chromium/issues/detail?id=852645#c9.

### mu...@chromium.org (2019-02-11)

My comment above (#c10) needs an update: we have a plan to move critical pieces in user activation to browser side.  As a result, now the fix should involve consuming on the browser side first (vs at renderer first as I suggested above).

Fullscreen is already handled by browser, so I believe it just needs passing the state of the browser's consumption call to renderer.



### mu...@chromium.org (2019-02-11)

[Empty comment from Monorail migration]

### fo...@chromium.org (2019-02-11)

mustaq@, do you have a code example of how that is done?

### mu...@chromium.org (2019-02-11)

Let me start a new thread about it.

### fo...@chromium.org (2019-02-21)

As discussed in chat, assigning over to mustaq@.

### mu...@chromium.org (2019-02-21)

cc-ing nzolghadr@, to prioritize.

[Monorail components: Blink>Input]

### nz...@chromium.org (2019-02-21)

Does the original repo work? I don't seem to be able to see the same effect with Chrome 72.

### he...@gmail.com (2019-02-21)

Just tested and it doesn't seem to work anymore. Looks like there was a change that broke it. I am getting "Failed to execute 'requestFullscreen' on 'Element': API can only be initiated by a user gesture." when trying to reproduce it.

### he...@gmail.com (2019-02-21)

It also seems that the attack in https://crbug.com/chromium/851302 was also broken (probably by the same change).

### nz...@chromium.org (2019-02-21)

mustaq@ are we good here then? Do you know whether there was a recent change in this space?

### mu...@chromium.org (2019-02-21)

Looks like UAv2 fixed the problem, yayy!  This is because the popup consumes the user activation on the browser side for the first window, so the fullscreen request fails.  (UAv2 has shipped in Chrome 72.)

herrerahlb@gmail.com: I can't access https://crbug.com/chromium/851302 for whatever reason.  Could you please verify if that one repro with chrome://flags/?#user-activation-v2 disabled?  Update this bug with the outcome please.



### mu...@chromium.org (2019-02-21)

Merged https://crbug.com/chromium/851302 into this.

Confirmed that the repro there (https://lbherrera.github.io/lab/fullscreen-spoof/index.html) is also fixed through UAv2.

Dropping the priority here accordingly.

Consuming on fullscreen is still the right approach: a single user activation shouldn't be allowed to call fullscreen twice.


### mu...@chromium.org (2019-02-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### mu...@chromium.org (2019-04-17)

Lan will start working on this in Q2.  This could break sites, so we will start with an easy patch on renderer side then move the consumption to browser.

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### la...@chromium.org (2019-05-09)

[Empty comment from Monorail migration]

### mu...@chromium.org (2019-05-14)

I looked into this repro closely to understand the abuse vector.  Looks like my comment in https://crbug.com/chromium/852645#c29 needs to be corrected: the reason it doesn't repro with UAv2 is because of UAv2's stricter visibility rules: clicking on the popup window doesn't make the activation available to the opener window.  So the opener window can't go fullscreen anymore.

Does that mean double-fullscreen calls can still be abused with UAv2 enabled, possibly without a popup?  Not sure.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/76ca4e08cc2babeeb6c9f8c0ae621cc6157f1702

commit 76ca4e08cc2babeeb6c9f8c0ae621cc6157f1702
Author: Lan Wei <lanwei@chromium.org>
Date: Wed May 29 16:06:54 2019

Only allow one full screen per user activation - experimental

When the user activation state is active, we should only allow one full
screen. This is a simply change to do an experiment to see if any
web page breaks.

Intent to ship link is
https://groups.google.com/a/chromium.org/forum/#!topic/blink-dev/Y58tbs-TSgE

Bug: 852645
Change-Id: Iebef20ba197ecd09e7067986073999e334b07498
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1594805
Reviewed-by: Mustaq Ahmed <mustaq@chromium.org>
Reviewed-by: Philip Jägenstedt <foolip@chromium.org>
Commit-Queue: Lan Wei <lanwei@chromium.org>
Cr-Commit-Position: refs/heads/master@{#664292}

[modify] https://crrev.com/76ca4e08cc2babeeb6c9f8c0ae621cc6157f1702/third_party/blink/renderer/core/fullscreen/fullscreen.cc
[modify] https://crrev.com/76ca4e08cc2babeeb6c9f8c0ae621cc6157f1702/third_party/blink/web_tests/TestExpectations
[add] https://crrev.com/76ca4e08cc2babeeb6c9f8c0ae621cc6157f1702/third_party/blink/web_tests/external/wpt/fullscreen/api/element-request-fullscreen-twice-manual.tentative.html
[add] https://crrev.com/76ca4e08cc2babeeb6c9f8c0ae621cc6157f1702/third_party/blink/web_tests/external/wpt/fullscreen/api/element-request-fullscreen-two-elements-manual.tentative.html
[add] https://crrev.com/76ca4e08cc2babeeb6c9f8c0ae621cc6157f1702/third_party/blink/web_tests/external/wpt/fullscreen/api/element-request-fullscreen-two-iframes-manual.tentative.html
[add] https://crrev.com/76ca4e08cc2babeeb6c9f8c0ae621cc6157f1702/third_party/blink/web_tests/fullscreen/api/document-exit-fullscreen-vs-request-expected.txt


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/41bd41c6007ff81340124077137ce9befa05e87e

commit 41bd41c6007ff81340124077137ce9befa05e87e
Author: Lan Wei <lanwei@chromium.org>
Date: Fri May 31 16:12:08 2019

Disable one fullscreen layout test

virtual/android/fullscreen/api/document-exit-fullscreen-vs-request.html
is flaky on chromium.linux bots, because of recent change of user
activation is consumed for fullscreen, disable it for now, we will fix
once we confirm this change will be accepted.
https://analysis.chromium.org/p/chromium/flake-portal/analysis/culprit?key=ag9zfmZpbmRpdC1mb3ItbWVyQwsSDEZsYWtlQ3VscHJpdCIxY2hyb21pdW0vNzZjYTRlMDhjYzJiYWJlZWI2YzlmOGMwYWU2MjFjYzYxNTdmMTcwMgw

Bug: 852645
Change-Id: Idd8799adf603f45c2e6c1de94cef8824c7de83c9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1636820
Reviewed-by: Philip Jägenstedt <foolip@chromium.org>
Commit-Queue: Lan Wei <lanwei@chromium.org>
Cr-Commit-Position: refs/heads/master@{#665141}

[modify] https://crrev.com/41bd41c6007ff81340124077137ce9befa05e87e/third_party/blink/web_tests/TestExpectations


### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### mu...@chromium.org (2019-06-21)

Let's turn it on in M77.

### mu...@chromium.org (2019-06-21)

It's already active on M76.

### li...@chromium.org (2019-08-07)

Is the work to fix this bug complete? Can we mark as fixed? Thanks!

### la...@chromium.org (2019-08-07)

No, we are watching issues caused by this change when M76 goes stable and also we need to improve the code. Thanks for checking.

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### mu...@chromium.org (2019-12-17)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/faea6bd47aca3112153092346e7413ecc4ccfe62

commit faea6bd47aca3112153092346e7413ecc4ccfe62
Author: Lan Wei <lanwei@chromium.org>
Date: Fri Jan 03 21:59:28 2020

Stop sending redundant EnterFullscreen messages to the browser

If we have a page hierarchy A(B(C)) and C tries to enter fullscreen by
calling Fullscreen::RequestFullscreen(). This eventually calls the
browser process at RenderFrameHostImpl::EnterFullscreen() for frame C.
RenderFrameHostImpl::EnterFullscreen() for C hides the UI and puts the
tab into fullscreen, and it also sends WillEnterFullscreen IPCs to A
and B, so that they can modify their fullscreen state as well.
In response to WillEnterFullscreen(), both A and B will call
Fullscreen::RequestFullscreen(), but with for_cross_process_descendant
being true, which skips a few things not needed for these ancestors
(such as whether fullscreen can be entered). However, currently both A
and B will each call RenderFrameHostImpl::EnterFullscreen() in the
browser process *again*.  The browser process notices that we're
already in fullscreen mode (UI already hidden, etc.), so it doesn't do
anything useful on these calls.

We should not send the extra EnterFullscreen messages for A and B. This
makes it so that we only hear RFHI::EnterFullscreen() from C, and it
makes it possible to enforce fullscreen security checks on C in
EnterFullscreen, without worrying whether it's C or its ancestors
sending this message.

Bug: 852645
Change-Id: I0d300ad2c88b46d379e2ecd0f3036a5fd486e123
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1967881
Commit-Queue: Lan Wei <lanwei@chromium.org>
Reviewed-by: Philip Jägenstedt <foolip@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#728306}

[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/core/exported/web_view_impl.cc
[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/core/exported/web_view_impl.h
[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/core/frame/fullscreen_controller.cc
[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/core/frame/fullscreen_controller.h
[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/core/fullscreen/fullscreen.cc
[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/core/html/media/html_video_element_persistent_test.cc
[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/core/page/chrome_client.h
[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/core/page/chrome_client_impl.cc
[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/core/page/chrome_client_impl.h
[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/modules/media_controls/elements/media_control_display_cutout_fullscreen_button_element_test.cc
[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/modules/media_controls/media_controls_display_cutout_delegate_test.cc
[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/modules/media_controls/media_controls_orientation_lock_delegate_test.cc
[modify] https://crrev.com/faea6bd47aca3112153092346e7413ecc4ccfe62/third_party/blink/renderer/modules/media_controls/media_controls_rotate_to_fullscreen_delegate_test.cc


### me...@chromium.org (2020-01-07)

lanwei: Is this now fixed?

### mu...@chromium.org (2020-01-10)

FYI for msw@: this might affect https://crbug.com/chromium/897300.

### al...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### la...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### do...@chromium.org (2020-01-22)

Friendly security marshall ping: can this bug be marked as Fixed now?

### la...@chromium.org (2020-01-22)

We have a simple hack right now, but we will have a full implementation soon,. Once we land it, we will mark it fix. I think we can remove the security tags right now. mustaq@ what do you think?

### mu...@chromium.org (2020-01-22)

The CL in https://crbug.com/chromium/852645#c37 resolved the main security concern.   Removing the security tags would be unwise because the concern was real.  I think the best option is to open a new bug that is blocked by this one.


### la...@chromium.org (2020-01-22)

Sure, I will create a new one, and we can mark this one fix.

### me...@chromium.org (2020-01-29)

lanwei: Have you had a chance to create the new bug?

### la...@chromium.org (2020-01-29)

Yes, this is the new issue, https://bugs.chromium.org/p/chromium/issues/detail?id=1046933 I will close this one, thank you for following up.

### me...@google.com (2020-01-29)

Thank you!

### mu...@chromium.org (2020-01-30)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-30)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-03)

Requesting merge to beta M80 because latest trunk commit (728306) appears to be after beta branch point (722274).

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

lanwei@ can you pls answer https://crbug.com/chromium/852645#c65 for merge review 

### la...@chromium.org (2020-02-03)

 srinivassista@ I do not know why it has been added a merge request, this issue does not need merge to M80. Could you please remove it, thank you.

### ad...@google.com (2020-02-05)

Re https://crbug.com/chromium/852645#c67 - as it's a medium severity, externally reported, security bug we'd normally consider merging back to the current stable release. However, we'd only do that if the fix is essentially trivially low stability risk. The fix here looks fairly complex - is that why you say we shouldn't merge this? If so, I agree.

### na...@google.com (2020-02-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2020-02-06)

Congrats the Panel decided to award $1,000 for this report! 

### na...@google.com (2020-02-06)

[Empty comment from Monorail migration]

### mu...@chromium.org (2020-02-06)

adetaylor@: No need to merge in M80.  The bug has already been fixed through renderer-side code at M76.

To avoid any confusion, our last few months' work here is about making the fix even better (browser-verified).  That supplemental work has been forked to https://crbug.com/chromium/1046933.

### sr...@google.com (2020-02-07)

Removing merge-review label per https://crbug.com/chromium/852645#c72 and https://crbug.com/chromium/852645#c67

### ad...@google.com (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@gmail.com (2020-05-31)

Strange, but this bug is reproduced in version chrome 83.0.4103.61 (Windows)

### al...@alesandroortiz.com (2020-05-31)

Re https://crbug.com/chromium/852645#c78 could be due to https://crbug.com/chromium/1085982 (restricted).

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/852645?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Fullscreen, Blink>Input]
[Monorail blocked-on: crbug.com/chromium/1035113, crbug.com/chromium/696617]
[Monorail blocking: crbug.com/chromium/1046933, crbug.com/chromium/848778]
[Monorail mergedwith: crbug.com/chromium/729694, crbug.com/chromium/851302, crbug.com/chromium/919992, crbug.com/chromium/924001]
[Monorail components added to Component Tags custom field.]

### ch...@chops-service-accounts.iam.gserviceaccount.com (2025-06-03)

The unexpected pass finder removed the last expectation associated with this bug. An associated CL should be landing shortly, after which this bug can be closed once a human confirms there is no more work to be done.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091651)*
