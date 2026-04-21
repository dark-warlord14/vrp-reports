# Security: Page can obtain autofill data with two consecutive taps using EyeDropper API (bypass of multiple prior fixes)

| Field | Value |
|-------|-------|
| **Issue ID** | [40065604](https://issues.chromium.org/issues/40065604) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill>AddressesAndMore, UI>Browser>Autofill>Payments |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | jk...@google.com |
| **Created** | 2023-06-09 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

A page can make a user select an autofill item with two consecutive taps with no user awareness by calling the EyeDropper API. Similar behavior with EyeDropper API + mouse was previously fixed in <https://crbug.com/chromium/1287364> [1]. The tap behavior without the EyeDropper API was previously fixed in <https://crbug.com/chromium/1341430> [2] and <https://crbug.com/chromium/1418837> [3].

Normally Chrome requires an intentional selection by the user and clear user awareness to select an autofill item.

I've tested this with addresses (which includes name + email) and credit cards. For sample input, see the video recording.

Bisect:  

The tap behavior starts reproducing after commit dabaa419e3d4d5e1ba950714f2cbdcb758192a45 ("Show the autofill/password generation dropdown on tap.", Jan 2020, M81).  

The EyeDropper API was enabled by default in commit 52d9b67c8e59a419fcd741967bb93bc186176442 ("[EyeDropper API] Enable EyeDropper API by default.", Aug 2021, M95). The PoCs worked without the EyeDropper API prior before this, but the mitigations introduced in M98 and higher made the EyeDropper API a requirement for similar PoCs.

All mouse/keyboard-based PoCs started reproducing starting in M67 or lower (probably when autofill on input-click was introduced).  

All tap-based PoCs started reproducing starting in M81 (when autofill on input-tap was introduced).  

All these autofill bugs were gradually fixed based on my other reports starting in M98 and above.

For full context, please see these related bugs (also see the earlier bugs that these bypassed):

[1] <https://crbug.com/chromium/1287364>: Page can use EyeDropper API to bypass mouse movement/keyboard input requirements for autofill (bypass of <https://crbug.com/chromium/1240472> fix)

[2] <https://crbug.com/chromium/1341430>: Page can obtain autofill data with two consecutive taps with minimal user awareness, bypasses <https://crbug.com/chromium/1240472> and <https://crbug.com/chromium/1279268> fixes

[3] <https://crbug.com/chromium/1418837>: After refactor, page can use EyeDropper API to bypass mouse movement/keyboard input requirements for autofill (regression of <https://crbug.com/chromium/1287364>)

**VERSION**  

Chrome Version: (All channels) 114.0.5735.110 Stable, 115.0.5790.24 Beta, 116.0.5817.5 Dev, 116.0.5822.0 Canary  

Operating System: Windows 10 Version 22H2 (Build 19045.2965)

**REPRODUCTION CASE**  

PoC for address:  

Prerequisites: Touchscreen device + have at least one address in chrome://settings/addresses

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-eye-dropper-two-taps.html>
2. Tap the same place twice in a row, anywhere in the page.

PoC for credit card:  

Prerequisites: Touchscreen device + have at least one credit card in chrome://settings/payments

1. Navigate to <https://alesandroortiz.com/security/chromium/autofill-eye-dropper-two-taps.html?creditcard>
2. (Same as prior PoC, tap twice in a row)

For all PoCs:  

Observed: Autofilled data is provided to page without autofill items being visible.  

Expected: Autofilled data is \*not\* provided to page unless autofill items are visible for minimum threshold of time (see commit 73db4bddcce5e5b9dd180ddbd0081c09dd1ef3d6 and earlier related commits).

**CREDIT INFORMATION**  

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [autofill-eye-dropper-two-taps.html](attachments/autofill-eye-dropper-two-taps.html) (text/plain, 3.4 KB)
- [autofill-eye-dropper-two-taps.mp4](attachments/autofill-eye-dropper-two-taps.mp4) (video/mp4, 97.1 KB)
- [crbug1453815-debug-1.html](attachments/crbug1453815-debug-1.html) (text/plain, 3.0 KB)
- [autofill-eye-dropper-jan2024.html](attachments/autofill-eye-dropper-jan2024.html) (text/plain, 3.7 KB)
- [timed-video.html](attachments/timed-video.html) (text/plain, 1.5 KB)
- [timed-video.mp4](attachments/timed-video.mp4) (video/mp4, 2.0 MB)
- [autofill-eye-dropper-june2024.mp4](attachments/autofill-eye-dropper-june2024.mp4) (video/mp4, 2.6 MB)

## Timeline

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-06-09)

Note that this report's PoC is the basically same PoC as https://crbug.com/chromium/1418837 (which was made public today) but with different instructions (tap instead of click).

### ar...@google.com (2023-06-12)

Thanks!

The bug requires a particular device (touch screen) that I don't have available. As a result I can't reproduce. I tried:
- on linux with a mouse: the previous mitigations are effective.
- on linux emulating touch device using devtool: I can't reproduce
- on android: The autofill info are along the keyboard, so I can't reproduce.

@jkeitel, could you please take a look?

[Monorail components: UI>Browser>Autofill>AddressesAndMore UI>Browser>Autofill>Payments]

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-24)

jkeitel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-08)

jkeitel: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@google.com (2023-07-10)

I am getting a device to try and reproduce.

### jk...@google.com (2023-07-14)

I obtained a ChromeOS device with touch screen, but I cannot reproduce on that one either.

### al...@alesandroortiz.com (2023-07-14)

Hm, still repros on Windows on 114.0.5735.199 Stable, so might not repro on ChromeOS for some reason. I only have a non-touchscreen ChromeOS device, so can't test if a modified PoC might work on ChromeOS.

Hope you're able to test on a touchscreen Windows device soon.

### jk...@google.com (2023-07-27)

[Empty comment from Monorail migration]

### jk...@google.com (2023-07-28)

Alesandro,

I've been trying to reproduce it, but I don't manage to. I now have a Windows device with touchscreen and fail to reproduce it both on Stable (115.0.5790.110) and on Canary. Can you check whether this is still reproducible for you?

Thanks,
Jan

### al...@alesandroortiz.com (2023-07-28)

Hi Jan, I can still repro on 115.0.5790.110 Stable (same version you tried) and 117.0.5914.0 Canary. I'm using Windows 10 Version 22H2 (Build 19045.3208).

Also repros on Stable on Windows Sandbox running Windows 10 Version 2004 (Build 19041.3208) with animations disabled (animations have sometimes affected repro in other issues).

When you tap once and wait a few seconds, is the autofill prompt shown?

### jk...@google.com (2023-07-31)

Yes, the Autofill prompt is shown - not always exactly where I had clicked, but it always shows up.
However, when I double click, it at most highlights the Autofill popup menu entry - it never fills. That only happens when there's a significant delay between the popup showing and may next tap.

### jk...@google.com (2023-07-31)

*my next tap.

### al...@alesandroortiz.com (2023-07-31)

Hm, interesting. I tested on my boyfriend's Windows device and there it behaves slightly differently, probably the same way it behaves on your device based on your description.

On my device, there's a significant delay between the first tap and the autofill prompt being shown. The delay is caused by the eye dropper, much like in https://crbug.com/chromium/1287364.
However, on their device, there's no delay between the first tap and the autofill prompt being shown. The second tap only highlights the entry, and only fills after the 500ms threshold implemented in https://crbug.com/1279268#c43, which matches your description of "[Filling] only happens when there's a significant delay between the popup showing and [my] next tap".

Will troubleshoot further and try to provide an updated PoC that works on devices like yours. Maybe PoC needs some timing adjustments for eye dropper cancellation or other tweaks.

### al...@alesandroortiz.com (2023-07-31)

No luck so far, will continue trying later today or tomorrow when boyfriend's device becomes available again.

A couple of observations (mostly for myself):
On my device, when I tweak PoC so the autofill prompt is shown after first tap but the 2nd tap is still delayed by the eyedropper, the PoC still repros. The autofill prompt is shown, but then the eyedropper invocation delays the 2nd tap from being processed. The 2nd tap is registered after the 500ms threshold, which results in input elem being filled.

Also on my device, when I don't programmatically close the eye dropper, the issue still repros (eye dropper just remains visible). Not sure if this behavior is same or not on the other device.

My current theory is there's some sort of timing difference between the devices, since the repro on my device is affected by whether the eye dropper invocation is done immediately on mousedown or a few ticks after mousedown.

### al...@alesandroortiz.com (2023-07-31)

(I suppose the behavior observed on your device is still a security issue considering compromised renderers, since renderer gets autofill values on preview, but that would be a mitigating factor vs. regular renderer repro I have on my device.)

### al...@alesandroortiz.com (2023-07-31)

(rethinking https://crbug.com/chromium/1453815#c18: there are easier ways for compromised renderer to get preview values, such as arrow down, etc. so ignore https://crbug.com/chromium/1453815#c18)

### al...@alesandroortiz.com (2023-08-01)

Some progress:

I was able to get your behavior (no repro) on my device... on a fresh Windows profile.
For some reason, my usual Windows profile consistently repros, while a fresh profile does not repro. On my usual Windows profile, even a fresh browser profile, VMs, no other windows/apps, etc. does not seem to break repro.

I have no idea what might be different between the profiles, other than potential cruft from years of use or a Windows setting that is different between these OS profiles. Maybe I've changed a setting that somehow affects this too, but I can't think of any. The touchscreen and mouse settings appear to be the same between the devices.

The main difference that affects repro seems to be the delay after which the autofill+eyedropper are both shown. When there's repro, the delay is significant. When there's no repro, the delay is quite low (almost instant).

I was able to also remove some potential variability by using inputElem.showPicker() in this PoC (also attached): https://aogarantiza.com/chromium/crbug1453815-debug-1.html

### al...@alesandroortiz.com (2023-08-01)

(Also, the fact that the input elem moves does not affect repro. I tried keeping the element in a static position, and had no effect on repro on any device).

### al...@alesandroortiz.com (2023-08-01)

Jan, can you try on your Windows device within Windows sandbox? There I was able to get repro on my device while on the fresh OS profile.

Windows Sandbox requires Windows 10 Pro or Enterprise (or others that aren't Home); not sure what your device has.
See full prereqs here: https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-overview

If you don't have Windows Sandbox available, maybe any regular Hyper-V VM will work too but I haven't tested this.

### al...@alesandroortiz.com (2023-08-01)

Interestingly, clicking twice also works in Windows Sandbox... so at least in Windows Sandbox, https://crbug.com/chromium/1287364 also repros.

As a note, if OS settings matter, a Hyper-V VM might behave differently than Windows Sandbox if they have different OS settings within VM.

### al...@alesandroortiz.com (2023-08-01)

Not sure if I had mentioned it before, but the main difference seems to be the delay before the eye dropper is shown.

Using this page [1], in repro env, the eye dropper appears after a noticeable delay. In non-repro env, the eye dropper appears immediately.

This suggests the delay in showing the eye dropper is affecting repro. Not sure exactly how/why this delay affects autofill rendering; maybe it's similar to https://crbug.com/chromium/1287364.

[1] https://aogarantiza.com/chromium/eyedropper.html

### jk...@google.com (2023-08-04)

Hi Alesandro,

Thanks a million for helping to let me reproduce this. I can now reproduce on the Windows sandbox. It's not reliable and requires me to hit a very exact spot on the screen, but it does work in some cases.

I am checking to see how we can fix this.

Jan

### jk...@google.com (2023-08-04)

[Empty comment from Monorail migration]

### al...@alesandroortiz.com (2023-08-04)

Hi Jan, glad you were able to reproduce! The location offset issue might be because of screen pixel density and/or resolution differences. Feel free to adjust the offsets in the PoC from https://crbug.com/chromium/1453815#c20 lines 84-85. I also had to adjust positioning slightly when testing on my boyfriend's device which has different display hardware.

Does clicking twice also repro for you, per https://crbug.com/chromium/1453815#c23? That one was more surprising for me. After you investigate, let me know if that one requires a separate crbug.

Next week I'll try to test in a Hyper-V VM with at least a couple different Windows images (if I can get more than one) to see if behavior is the same or not vs. Sandbox vs. fresh host profile. This should help us figure out if variation likely is due to OS settings, or something Hyper-V specific that happens to also occur on my main host profile, some combination, or something else entirely.

Maybe I'll also see if I can use some techniques documented by Bruce Dawson to help determine reason for eyedropper delay, but that analysis method may be out of my wheelhouse.

Hopefully your investigation sheds some light on why eyedropper delay variation is occurring. If not, it may remain a mystery unless a Windows expert is looped.

### jk...@google.com (2023-08-04)

Hi Alesandro,

I think I have a decent idea of what's happening, but we're trying to figure what the best long-term approach is. That's turning out to be trickier than previous fixes... ;-)
I've yet to try the clicking, but I'll do that next week.

Thanks again for all the help!

Jan

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### jk...@google.com (2023-08-23)

Hi Alesandro,

Just a quick note: This is not forgotten, we're working on it.

Re clicking: I cannot reproduce that behavior at the moment - it currently only works for me if you use touch gestures.

### gi...@appspot.gserviceaccount.com (2023-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8910f60dfeedc4836542775530930604788bea18

commit 8910f60dfeedc4836542775530930604788bea18
Author: Jan Keitel <jkeitel@google.com>
Date: Tue Aug 29 08:22:27 2023

Add time parameter for AutofillPopupController::AcceptSuggestion.

This CL adds a parameter to AutofillPopupController::AcceptSuggestion
that describes the time at which the user event that caused the
decision to accept the Autofill suggestion was triggered.

As of now, most callers populate the field with base::TimeTicks::Now(),
but in principle this allows to pass the actual time when the event was
triggered by the user (as opposed to when it got processed by Chrome).
In cases of high latency between event triggering and event processing,
this becomes relevant.

Bug: 1475902, 1453815
Change-Id: Ie24198f53ae5d8df0b5124c24b70b2446a2883ad
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4811898
Reviewed-by: Bruno Braga <brunobraga@google.com>
Commit-Queue: Jan Keitel <jkeitel@google.com>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Reviewed-by: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/main@{#1189392}

[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/autofill/autofill_popup_controller_unittest.cc
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/components/autofill/core/common/autofill_features.cc
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/views/autofill/popup/popup_row_strategy_unittest.cc
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/autofill/autofill_keyboard_accessory_adapter.h
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/autofill/autofill_popup_controller.h
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/autofill/mock_autofill_popup_controller.h
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/views/autofill/popup/popup_cell_view.h
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/android/autofill/autofill_keyboard_accessory_view.cc
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/components/autofill/core/common/autofill_features.h
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/views/autofill/popup/popup_view_views.cc
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/views/autofill/popup/popup_view_views_unittest.cc
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/views/autofill/popup/popup_row_view_unittest.cc
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/autofill/autofill_popup_controller_impl.h
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/views/autofill/popup/popup_cell_view_unittest.cc
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/cocoa/touchbar/credit_card_autofill_touch_bar_controller.mm
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/views/autofill/popup/popup_cell_view.cc
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/android/autofill/autofill_popup_view_android.cc
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/autofill/autofill_keyboard_accessory_adapter.cc
[modify] https://crrev.com/8910f60dfeedc4836542775530930604788bea18/chrome/browser/ui/views/autofill/popup/popup_view_views.h


### al...@alesandroortiz.com (2023-09-26)

Hi, I'm still able to repro on my main device on 119.0.6029.0 Canary using both PoCs [1,2], even with --enable-features=AutofillPopupUseLatencyInformationForAcceptThreshold. I haven't tested on another device using Windows Sandbox.

Fix in https://crbug.com/chromium/1453815#c29 landed on Canary 118 behind that feature flag, so it doesn't seem to fix the issue: https://chromiumdash.appspot.com/commit/8910f60dfeedc4836542775530930604788bea18

[1] https://alesandroortiz.com/security/chromium/autofill-eye-dropper-two-taps.html
[2] https://aogarantiza.com/chromium/crbug1453815-debug-1.html

Sorry for the delay in testing the fix.

### al...@alesandroortiz.com (2023-09-26)

(For completeness, also still repros on 117.0.5938.89 Stable, but that's expected since patch hasn't landed there yet.)

### jk...@google.com (2023-09-27)

Hi Alesandro, yeah, that's correct, this does not fix the gesture issues yet. However, if you have a moment: Could you check whether running Chrome with
--enable-features=AutofillPopupDisablePaintChecks,AutofillPopupUseLatencyInformationForAcceptThreshold still works in preventing the old attack using just a mouse?

The background is that I am looking at a different kind of exploit prevention using timing instead of paint checks that would eventually also protect against gestures/taps.

Thanks,
Jan

### [Deleted User] (2023-09-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@alesandroortiz.com (2023-09-28)

Re: https://crbug.com/chromium/1453815#c34, the old attack being https://crbug.com/chromium/1287364?

I looked at the flags you mentioned, and see `AutofillPopupDisablePaintChecks` disables the `MouseObservedOutsideItemBounds` [1] check. This causes a series of regressions even with `AutofillPopupUseLatencyInformationForAcceptThreshold` enabled.

I now tested these PoCs on 119.0.6034.2 Canary with --enable-features=AutofillPopupDisablePaintChecks,AutofillPopupUseLatencyInformationForAcceptThreshold
* https://aogarantiza.com/chromium/autofill-1287364-updated.html (which is PoC from https://crbug.com/chromium/1287364 with updated positioning)
* https://alesandroortiz.com/security/chromium/autofill-eye-dropper-two-taps.html
* https://aogarantiza.com/chromium/crbug1453815-debug-1.html

Compared to 117.0.5938.92 Stable and 119.0.6034.2 Canary with default flags:

* The first PoC has a partial regression that by itself doesn't rise to a security issue, but likely would cause regressions of older bugs that were fixed by the `MouseObservedOutsideItemBounds` [1] check with lightly-updated PoCs.
* The EyeDropper PoCs definitely have security regressions. The EyeDropper API delays the autofill prompt rendering, and once the autofill prompt is shown, the user can select the autofill item without awareness if the user is still clicking or holding down the enter key after the initial press.

A quick way to test this with the existing PoCs is by following these repro steps:
With mouse:
1. Navigate to https://alesandroortiz.com/security/chromium/autofill-eye-dropper-two-taps.html
2. Repeatedly click for several seconds until output box is green.

Observed: Autofill item is selected due to lack of `MouseObservedOutsideItemBounds` check.

Unfortunately, I also might have found yet another bypass that repros on Stable (and also still repros with the new flags on Canary), so will file that shortly if confirmed it doesn't overlap with any of the existing open crbugs.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/autofill/autofill_popup_controller_impl.cc;l=237;drc=145c6539a80e3996ce96c730c0022e40a723ce1e

### al...@alesandroortiz.com (2023-10-07)

As promised, filed https://crbug.com/chromium/1490773 for the bypass I found while writing https://crbug.com/chromium/1453815#c36.

### jk...@google.com (2023-10-09)

Thank you, Alesandro. Can you cc me on the bug, please?

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### jk...@google.com (2023-11-09)

[Empty comment from Monorail migration]

### jk...@google.com (2023-12-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### jk...@google.com (2024-01-23)

Hi Alesandro,

It has been a while, but this has been far trickier than anticipated. However, I think I might have a robust solution now. I would appreciate it if you could check whether starting Chrome with the following command line parameter solves the issue: --enable-features=AutofillPopupImprovedTimingChecks

If that works, it would also be good to know whether --enable-features=AutofillPopupImprovedTimingChecks,AutofillPopupDisablePaintChecks still fixes the issue.

On my builds, these measures prevent the double/triple click attacks - including on a Windows laptop with touch screen running Canary in sandbox mode.

Note that you'll need Chrome version 122.0.6260.0 or newer.

Thank you,
Jan

### al...@alesandroortiz.com (2024-01-25)

I started testing the repros with and without the flags yesterday, but might be a few hours/days before I have some more details. Seems like my environment has changed since October 2023, so I'm no longer able to repro on my host OS (the EyeDropper delay is gone). Even in Sandbox, there's some behavior differences with some of the PoCs, so working through those for more consistent repro as I test.

I'll advance that there _appears_ be a scenario where the attack still works without the autofill popup being visible, but I'm still investigating. Not sure yet if it's related to this bug, or if it's yet another bug.

### al...@alesandroortiz.com (2024-01-25)

s/since October/since August/

### al...@alesandroortiz.com (2024-01-26)

Jan, you mentioned in crbug.com/1490773#c18 that the touch issue still reproduces for you in Sandbox. I'm having difficulties with the repro as it worked before, without flags and with --no-experiments to ensure that nothing else is interfering.

The original PoC [1] seems to behave differently than it did in June-September 2023. Before, the autofill prompt was not visible at all. Now, the PoC requires 3 taps, with the 2nd and 3rd tap occurring after the autofill prompt is visible.

Another PoC [2] (from https://crbug.com/chromium/1453815#c36 here / https://crbug.com/chromium/1287364) still repros with 2 taps, but the autofill prompt is visible after the first tap which might make the attack less effective.

I would consider that if the autofill prompt is visible for a meaningful amount of time for the issue to be mostly mitigated, although I'm not sure if the current repro is at least 500ms (with [1] it seems like at least 500ms, with [2] it seems less than 500ms)

I'll try bisecting to see if it's due to the Chrome version, or if something in my environment caused repro behavior to change.

If I get baseline repro working as it did before, then I'll be able to better compare with the AutofillPopupImprovedTimingChecks flag enabled. If I'm unable to get it working, I'll do tests with the flag enabled for any behavior changes anyway in case they mitigate the current behavior in the other PoC [2].

[1] https://alesandroortiz.com/security/chromium/autofill-eye-dropper-two-taps.html
[2] https://aogarantiza.com/chromium/autofill-1287364-updated.html

### al...@alesandroortiz.com (2024-01-26)

Hm, actually, I'm able to repro the original behavior in 121.0.6167.86 Stable. The repro issues I was having were in 122.0.6261.3 Canary and 123.0.6265.0 Canary.

I'm running Stable with --no-experiments as well, so not sure why there's a behavior difference without the new AutofillPopupImprovedTimingChecks flag.

I'll try running these different versions via bisect tool to see if I can get repro on there, so I can then test with the flag.

### al...@alesandroortiz.com (2024-01-26)

Finally unblocked. In Sandbox, was able to get consistent repro using snapshot build 1250557 from https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/1250557/ which includes https://chromium-review.googlesource.com/c/chromium/src/+/5145027 (r1249609). I don't know why Canary doesn't repro, but Stable + snapshots do repro. Might be a build args difference affecting performance, since perf is somewhat important to repro.

After comparing with and without the AutofillPopupImprovedTimingChecks flag, I've verified that it's _mostly_ fixed with the flag:

* In scenarios where the autofill prompt is never visible (or very briefly visible), this issue is fixed. This was the most important scenario.

* However, in scenarios where the autofill prompt is visible but the user taps twice quickly (like in https://crbug.com/chromium/1287364 and https://crbug.com/chromium/1341430) this still reproduces reliably without meeting the 500ms threshold. Tested with this PoC although I'm working on an updated one for this particular issue: https://aogarantiza.com/chromium/autofill-1287364-updated.html

The behavior for these PoCs also seems identical (read: mostly fixed) with both flags enabled: AutofillPopupImprovedTimingChecks,AutofillPopupDisablePaintChecks

I haven't tested older PoCs for regressions, and there's a chance enabling AutofillPopupDisablePaintChecks might cause regressions as noted in https://crbug.com/chromium/1453815#c36 even with the new timing checks. I'll test this soon.

### jk...@google.com (2024-01-26)

Alesandro, I really appreciate your continued testing and chasing down more edge cases.

I am a bit puzzled that the 500 ms threshold is not met - do you have measurements/video that indicates by how much? I'd love to this a PoC for that. I have one more idea for hardening the checks further still, but it'd be good to try a PoC first.

Thank you for all your work! Hopefully we'll be able to really close this one soon. It's been haunting me.
Jan

### al...@alesandroortiz.com (2024-01-26)

Updated PoC (also attached): https://aogarantiza.com/chromium/autofill-eye-dropper-jan2024.html

It's basically the same PoC as https://aogarantiza.com/chromium/autofill-1287364-updated.html (from https://crbug.com/chromium/1287364) with some timings adjusted.

Will see if I can record screen to demonstrate visually and properly measure time.

### al...@alesandroortiz.com (2024-01-26)

> It's been haunting me.

Sorry 😅

### al...@alesandroortiz.com (2024-01-26)

Worth noting that earlier I tested a modified PoC that did not invoke the EyeDropper, and the attack stopped reproducing, so the EyeDropper is still important in the PoC from https://crbug.com/chromium/1453815#c51 (so it's not a completely separate bug).

### al...@alesandroortiz.com (2024-01-27)

This is probably not the best way to measure, but based on video recording timing, I'm seeing deltas of 200-400ms that get accepted, below the 500ms threshold. In practice, the timing doesn't provide the user enough time to see/react before the 2nd tap (again, just like https://crbug.com/chromium/1287364 and https://crbug.com/chromium/1341430).

See attached video file and hacked-together analysis tool. Put both files in the same directory, and open the HTML file in your browser. Then press a "Skip to" button and move ahead 10ms at a time to observe the timings of touch events.

The dark circles in the video are the touch event indicators from the OS. The video was supposed to be recorded at 120fps, but not sure about actual frame rate.

My analysis of this video (and similar results in other videos):
1st tap: 0.590
2nd tap: 0.790
Delta: 200ms
--
1st tap: 3.290
2nd tap: 3.590
Delta: 300ms
--
1st tap: 5.580
2nd tap: 5.900
Delta: 320ms

### jk...@google.com (2024-01-30)

Alesandro, as always, much appreciated. Without looking at the exact timestamps in your video, I had another idea yesterday night what could be causing this loop hole. The code is in review now and will hopefully land on Canary in a few days. I'll let you know and might need your support once more.

Thank you! :)
Jan

### al...@alesandroortiz.com (2024-02-01)

As requested in crbug.com/1490773#c22:

With snapshot build 1255305 and AutofillPopupImprovedTimingChecksV2 enabled, all the PoCs in this crbug are mitigated. 🎉

Specifically, tested with these PoCs:
https://alesandroortiz.com/security/chromium/autofill-eye-dropper-two-taps.html
https://aogarantiza.com/chromium/autofill-eye-dropper-jan2024.html
https://aogarantiza.com/chromium/autofill-1287364-updated.html
https://aogarantiza.com/chromium/crbug1453815-debug-1.html

Do you also need me to test with AutofillPopupDisablePaintChecks enabled? As mentioned in https://crbug.com/chromium/1453815#c49, that will require more substantial testing.

I also verified that without invoking the EyeDropper [1], the user experience works well in non-repro environments. However, in repro environments, it seems like about 1500ms (1.5s) is required to accept the input using either clicks or taps, measured from first click/tap until last click/tap. Not sure if this is acceptable from a UX perspective, since it's quite a significant delay.

[1] https://aogarantiza.com/chromium/autofill-test4.html (autofill without invoking EyeDropper)

### jk...@google.com (2024-02-02)

Yes, finally! :) Thanks, Alesandro!

I am waiting for one more confirmation on another bug report before I will start rolling this out. Re required delay and impact on user experience: Yep, that's a fair question, but ultimately a reflection of the state the reproduction environment needs to be in for the exploit to work (reliably) in the first place. The reason that this exploit worked is that Chrome's UI thread in the browser process must be congested, which messes with timing information. In principle, that state should not be reachable.

I am considering to roll this fix out step wise and look at metrics to see what percentage of users experience any additional delay. My hope is that the fraction is near zero.

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1453815?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Autofill>AddressesAndMore, UI>Browser>Autofill>Payments]
[Monorail blocked-on: crbug.com/chromium/1475902]
[Monorail components added to Component Tags custom field.]

### al...@alesandroortiz.com (2024-02-06)

Thanks for your persistence with this, Jan!

When you have prod metrics, please comment with the results in case it's relevant in future bugs. Hopefully it's near zero, but I did experience it on my higher-end laptop's host OS for at least a year.

Do you still want me to test with AutofillPopupDisablePaintChecks(+AutofillPopupImprovedTimingChecksV2) enabled, or do you plan to mitigate only with AutofillPopupImprovedTimingChecksV2?

### jk...@google.com (2024-02-21)

So far, metrics are looking good - less than 0.01% see more than a couple hundred ms of extra delay. I tweaked one more aspect and hopefully the delay won't look too jarring on your device after that.

It'll probably take about a month to roll out securely - once that's done, I might get back to you about the paint checks. For now, I am leaving them on anyways.

Thanks Alesandro!

### jk...@google.com (2024-05-02)

Hi Alesandro,

This should now have reached 100% stable on the current stable build. Could you please verify that it is working as expected?

Thanks,
Jan

### al...@alesandroortiz.com (2024-05-07)

Re-verified as fixed on 124.0.6367.119 Stable with no special flags enabled on Windows 10 Version 22H2 (Build 19045.4170) (host machine), with PoCs listed in [#comment57](https://issues.chromium.org/issues/40065604#comment57).

However, I'll need to test some variations since [issue 40074360](https://issues.chromium.org/issues/40074360) still repros, so there's a chance this still repros with a modified PoC. :/

### al...@alesandroortiz.com (2024-05-07)

I think I'm seeing basically same behavior as the newer repro of [issue 40074360](https://issues.chromium.org/issues/40074360). Maybe this behavior is a separate issue or WAI with the new mitigation (I've lost track of the mitigations at this point).

With updated PoC [1], which changes EyeDropper delay from 40ms to 1ms and user instructions to "repeatedly tap the page", nearly-identical behavior is observed in Sandbox.

When the autofill prompt does become visible, it is immediately interactive. If the user is still tapping, the user likely won't have time to react and stop tapping before the autofill prompt is selected.

On host machine, it's also immediately interactive but visible long enough for user to react and stop in most cases.

I did the same verification as <https://issues.chromium.org/issues/40074360#comment28> in same environment, and it still repro'd without flag and was mitigated with flag on the older build. As noted over there, something is different between previous verification and now.

[1] <https://aogarantiza.com/chromium/autofill-eye-dropper-may2024.html>

### al...@alesandroortiz.com (2024-05-07)

Based on <https://issues.chromium.org/issues/40074360#comment19>, it doesn't seem WAI even if repro steps are a bit different than earlier PoCs and attack isn't fully hidden.

> As long as there are at least 500ms between the popup showing and the popup being acceptable, then that's intended behavior

### al...@alesandroortiz.com (2024-06-13)

Following up on [#comment64](https://issues.chromium.org/issues/40065604#comment64) + 65, since this issue also still seemed to repro in May.

### jk...@google.com (2024-06-18)

Hi Alesandro,

I just tried reproducing this on Linux, Windows (including by running inside a Sandbox), and MacOS, and I cannot reproduce the issue. In none of the cases does double/triple tapping lead to an accepted Autofill suggestion. Do you have any advice on how to possibly reproduce?

Thanks,
Jan

### al...@alesandroortiz.com (2024-06-18)

Attached repro video on my host Windows machine on 126.0.6478.61 Stable. It's immediately interactable.

I updated the PoC to not move the input field for a while, since that might cause repro to be less reliable if you don't make the subsequent tap within a certain radius.

<https://aogarantiza.com/chromium/autofill-eye-dropper-june2024.html>

On your device, the tap is being correctly blocked for 500ms after prompt is actually visible to you?

If it still doesn't repro as shown in video, try making one tap, waiting a tiny bit, then tapping twice. Or furiously tapping repeatedly (like a cookie clicker game).

Maybe also try different power settings on your device. I'm able to repro reliably on low and high power settings (i.e. more/less hardware throttling), but maybe on your device it does make a difference.

If none of the above works, I can also try updating the PoC to simulate some sluggishness, since I was able to do so in [#comment64](https://issues.chromium.org/issues/40065604#comment64) (but am not able to repro fully invisible prompt now).

### jk...@google.com (2024-06-20)

Hi Alesandro,

Once again, thank you for your support. I have now been able to reproduce in some cases.

I hope we can finally get this resolved once and for all. Maybe there's been a change in where some of the delay that is introduced by the eye dropper occurs in the rendering pipeline. Let me try one more experiment. I'll try and add the code ASAP so that it should hit Canary next week. Once that happens, I'll get back to you.

Thanks,
Jan

### al...@alesandroortiz.com (2024-06-20)

Glad you got repro! Sorry this has been a pain to fix. 🙁

### jk...@google.com (2024-06-24)

Hi Alesandro,

Okay, here we go again: Can you try adding `--enable-features=AutofillPopupMeasureTimeAfterPaint` on any version that is at least `128.0.6549.0` and see whether that fixes the issue? It does for me on Canary in a sandbox on a Win device with touchscreen.

As always: Thank you for all your support!
Jan

### al...@alesandroortiz.com (2024-06-25)

Seems fixed, at least with <https://aogarantiza.com/chromium/autofill-eye-dropper-june2024.html> PoC with `--enable-features=AutofillPopupMeasureTimeAfterPaint` [1] on 128.0.6557.0 Canary.

I'll verify the other PoCs in this bug and related bugs shortly.

[1] <https://chromium-review.googlesource.com/c/chromium/src/+/5645183>

### al...@alesandroortiz.com (2024-06-25)

🎉 We can finally mark this as fixed. 🎉

Verified as fixed with these PoCs, both on host device and on Windows Sandbox, with various power settings, with `--enable-features=AutofillPopupMeasureTimeAfterPaint` [1] on 128.0.6557.0 Canary:

- <https://alesandroortiz.com/security/chromium/autofill-eye-dropper-two-taps.html> [1]
- <https://aogarantiza.com/chromium/crbug1453815-debug-1.html>
- <https://aogarantiza.com/chromium/autofill-1287364-updated.html>
- <https://aogarantiza.com/chromium/autofill-eye-dropper-jan2024.html>
- <https://aogarantiza.com/chromium/autofill-eye-dropper-june2024.html>

Repro note: Without the `AutofillPopupMeasureTimeAfterPaint` flag, the first PoC [1] repros on Windows Sandbox. This had stopped reproducing at some point after one of the earlier fixes, so something definitely regressed at some point. But enabling `AutofillPopupMeasureTimeAfterPaint` breaks repro, so we're still good. :)

Jan, thanks again for all your time and effort on this!

### al...@alesandroortiz.com (2024-06-25)

The same CL + feature flag also fixed [issue 40074360](https://issues.chromium.org/issues/40074360) :)

### al...@alesandroortiz.com (2024-06-25)

For the VRP Panel:

In addition to the bypass that is the subject of the original report ([#comment1](https://issues.chromium.org/issues/40065604#comment1)), there are additional bypasses found after each round of patches. See below for pointers to comments (adjacent comments are also helpful for context). I kept all the bypasses in this one crbug to avoid a series of bypass crbugs.

If possible, please consider treating each of the following as separate reports in terms of reward [1], since they each had their own set of research, PoCs, and patches.

1. Original report (bypasses of previous fixes in other crbugs):
   
   - Report: [#comment1](https://issues.chromium.org/issues/40065604#comment1)
   - Fix (`AutofillPopupImprovedTimingChecks`): [#comment45](https://issues.chromium.org/issues/40065604#comment45)
2. Bypass of [#comment45](https://issues.chromium.org/issues/40065604#comment45) fix:
   
   - Bypass reported: [#comment50](https://issues.chromium.org/issues/40065604#comment50) + [#comment52](https://issues.chromium.org/issues/40065604#comment52)
   - Fix (`AutofillPopupImprovedTimingChecksV2`): [#comment57](https://issues.chromium.org/issues/40065604#comment57) / <https://issues.chromium.org/issues/40074360#comment23>
3. Bypass of [#comment57](https://issues.chromium.org/issues/40065604#comment57) fix:
   
   - Bypass reported: [#comment64](https://issues.chromium.org/issues/40065604#comment64) + [#comment68](https://issues.chromium.org/issues/40065604#comment68)
   - Fix (`AutofillPopupMeasureTimeAfterPaint`): [#comment71](https://issues.chromium.org/issues/40065604#comment71)

If there's any additional info, bisecting, etc. that will help increase reward further, please let me know and I'll provide them. Thanks!

[1] From [VRP rules](https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules#:~:text=decide%20that%20a%20single%20report%20actually%20constitutes%20multiple%20bugs):

> we may [...] decide that a single report actually constitutes multiple bugs

### jk...@google.com (2024-06-27)

Thanks a million, Alesandro! I am preparing to switch on the flag permanently. Once that CL makes it to Canary, I'll mark this bug as fixed and it'll go to the VRP.

### jk...@google.com (2024-06-28)

This is now default-enabled on Canary as of `128.0.6562.0` and I am thus marking the bug as fixed.

Alesandro, thank you for all your work on this, the repeated detailed and helpful feedback, and the iterations of your exploit prototypes. This was a really thorny bug to fix and it would have been near impossible without your support.

Jan

### sp...@google.com (2024-07-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
$10,000 total reward for this report of multiple user information disclosure issues: $5,000 for high-quality, moderate impact user information disclosure + $2,000 for report of lower impact information disclosure + $2,000 for report of lower impact information disclosure + $1,000 bisect bonus 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-03)

Congratulations Alesandro! Thanks for your diligent efforts and good reporting of these issues -- nice work!

### al...@alesandroortiz.com (2024-07-03)

Thanks for the rewards and for considering the bypasses separately!

### pe...@google.com (2024-10-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $10,000 total reward for this report of multiple user information disclosure issues: $5,000 for high-quality, moderate impact user information disclosure + $2,000 for report of lower impact information disclosure + $2,000 for report of lower impact information disclosure + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065604)*
