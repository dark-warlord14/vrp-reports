# [Autofill] Keyboard accessory, bottom sheet accept unintentional user input

| Field | Value |
|-------|-------|
| **Issue ID** | [40067505](https://issues.chromium.org/issues/40067505) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android |
| **Reporter** | st...@gmail.com |
| **Assignee** | jk...@google.com |
| **Created** | 2023-07-16 |
| **Bounty** | $2,000.00 |

## Description

The Autofill popup ignores (roughly) user input for 500 ms after it's shown to prevent security issues where the user is tricked into fast action (e.g., a double click) that unintentionally fill a form.

The keyboard accessory seems not to implement such a delay. A fast, strategically placed double tap can fill a form.

The same works with TTFCC, except that the bottom sheet takes longer to show up.

For reproduction, try the address and credit card forms from https://rsolomakhin.github.io/autofill/. It'd be easy combine this with, for example, a game to trick the user into tapping into a transparent field.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.7 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 498.6 KB)
- [poc-2.webm](attachments/poc-2.webm) (video/webm, 470.1 KB)
- [poc-2.html](attachments/poc-2.html) (text/plain, 1.7 KB)

## Timeline

### sc...@google.com (2023-07-16)

To add some background info, we introduced the 500 ms delay for mouse input on the popup as part of https://crbug.com/chromium/1279268 / crrev.com/c/3391381.
More recently we applied the same delay to keyboard input and, I believe, also taps on Android as part of https://crbug.com/chromium/1418364 / crrev.com/c/4281445.

+CC people familiar with these above bugs because this bug is locked down by default.

### jk...@google.com (2023-07-17)

Chris, how do you envision that this exploit would work? Place the (transparent) input field where the site expects the keyboard accessory to pop up?

FWIW, implementing this delay for the KeyboardAccessory would be a single line change, i.e. replacing https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/android/autofill/autofill_keyboard_accessory_view.cc;l=133 by the AcceptSuggestion() method of the controller.

For those more familiar with keyboard accessory: Are there any expected use cases/ common user interactions that would suffer from the introduction of such a delay?

### sc...@google.com (2023-07-17)

+CC Thomas who had filed https://crbug.com/chromium/1454962.

### sc...@google.com (2023-07-17)

> Place the (transparent) input field where the site expects the keyboard accessory to pop up?

Yes. I suppose the site can make a good enough guess using window.screen.height where the keyboard accessory will appear.

### st...@gmail.com (2023-07-17)

Or the VirtualKeyboard API could be used to get the exact bounds of the keyboard, if the keyboard has been opened beforehand.

https://developer.chrome.com/docs/web-platform/virtual-keyboard/#getting-the-current-geometry

### st...@gmail.com (2023-07-17)

This is the PoC for the tapjacking attack. I found that making the user tap the tap target (cookie) repeatedly makes it easier to repro than just doing a double-tap once. The position of the tap target needs to be manually set for the PoC, but the position could be guesstimated as mentioned in https://crbug.com/chromium/1465230#c4 and https://crbug.com/chromium/1465230#c5.

### st...@gmail.com (2023-07-17)

Using `AcceptSuggestion` instead of `AcceptSuggestionWithoutThreshold` (as described in https://crbug.com/chromium/1465230#c2) should fix this.

I am not sure, however, if it would take care of the following edge case:

1. User taps in the page and the keyboard accessory gets opened without the keyboard
2. User double taps and the keyboard gets opened with the accessory

Would the `time_view_shown_` cooldown be reset after step 2 in this case?

https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/ui/autofill/autofill_popup_controller_impl.cc;l=171;drc=54f2184c5bf221c0efaabdbe549f938066aab00f;bpv=1;bpt=1

If not, the following attack (using `showPicker()` to open both the datalist suggestions and autofill) could still take place:

### am...@chromium.org (2023-07-18)

Since this can be abused are result in security implications for users, I'm going to go ahead and set this carry over issue from 1454962 as a security bug. 


### [Deleted User] (2023-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-07-19)

schwering@, adding you as the owner tentatively! please re-assign if there is a more suitable owner for this bug?

### sc...@google.com (2023-07-19)

[Empty comment from Monorail migration]

### jk...@google.com (2023-07-21)

[Empty comment from Monorail migration]

### jk...@google.com (2023-07-21)

Note that there has been another report of the same issue. We are going experiment with enforcing the same (500ms) delay that is already used on Desktop for the Keyboard Accessory as well.

### gi...@appspot.gserviceaccount.com (2023-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3b57d3e90b4ce28a23dd7029add35ce9834600a9

commit 3b57d3e90b4ce28a23dd7029add35ce9834600a9
Author: Jan Keitel <jkeitel@google.com>
Date: Tue Jul 25 09:43:30 2023

Enforce time threshold before accepting KeyboardAccessory suggestions.

This CL enforces the same minimum time between showing the Autofill
suggestions and being able to accept them that is used elsewhere
(Desktop, legacy Autofill popup).

Bug: 1465230
Change-Id: I97e606fed01e377eb815ec2b60e18e3d767246b2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4705215
Commit-Queue: Jan Keitel <jkeitel@google.com>
Reviewed-by: Jihad Hanna <jihadghanna@google.com>
Reviewed-by: Bruno Braga <brunobraga@google.com>
Reviewed-by: Adem Derinel <derinel@google.com>
Reviewed-by: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/main@{#1174728}

[modify] https://crrev.com/3b57d3e90b4ce28a23dd7029add35ce9834600a9/components/autofill/core/common/autofill_features.cc
[modify] https://crrev.com/3b57d3e90b4ce28a23dd7029add35ce9834600a9/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/3b57d3e90b4ce28a23dd7029add35ce9834600a9/chrome/browser/ui/autofill/autofill_popup_controller_unittest.cc
[modify] https://crrev.com/3b57d3e90b4ce28a23dd7029add35ce9834600a9/tools/metrics/histograms/metadata/autofill/histograms.xml
[modify] https://crrev.com/3b57d3e90b4ce28a23dd7029add35ce9834600a9/chrome/browser/ui/android/autofill/autofill_keyboard_accessory_view.cc
[modify] https://crrev.com/3b57d3e90b4ce28a23dd7029add35ce9834600a9/chrome/browser/ui/autofill/autofill_keyboard_accessory_adapter.cc
[modify] https://crrev.com/3b57d3e90b4ce28a23dd7029add35ce9834600a9/components/autofill/core/common/autofill_features.h


### jk...@google.com (2023-07-26)

stw.stw.tom@: Could you try and see whether 117.0.5910.0 fixes the bug for you?

Thanks,
Jan

### st...@gmail.com (2023-07-26)

Hey Jan,

I've verified that your commit fixes this!

### jk...@google.com (2023-07-26)

Perfect, thank you for the fast response!

Chris, Dominic, Friedrich: What's your take on merging this back (to M116, M115 is definitely too late now)? I am agnostic on this.

Thanks
Jan

### fr...@chromium.org (2023-07-26)

Since the stable bot suggested a merge based on milestone and severity, I think merging to 116 makes sense. It's safe enough since there is one more Beta on Aug 2nd.
(I am also not hell-bent on this since the 5w delay until 117 would also be acceptable since there isn't a known exploit, is there?)

### ad...@chromium.org (2023-07-26)

jkeitel@ please mark this as Fixed, and then sheriffbot will apply our standard policy in requesting merge reviews. As this is medium severity, I think it will request a merge to beta but not to stable.

### jk...@google.com (2023-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-26)

[Empty comment from Monorail migration]

### jk...@google.com (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-27)

Merge review required: M116 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@google.com (2023-07-27)

1. Why does your merge fit within the merge criteria for these milestones?
It addresses a security issue.
2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium.googlesource.com/chromium/src/+/3b57d3e90b4ce28a23dd7029add35ce9834600a9
3. Have the changes been released and tested on canary?
Yes.
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
It is not a new feature, it is a (security) bug fix.
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No, it does not require manual verification.

### am...@chromium.org (2023-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-27)

116 merge approved for https://crrev.com/c/4705215 -- please merge this fix to branch 5845 at your convenience / before Tuesday 1 August so this fix can be included in the next M116/beta release -- ty 

### [Deleted User] (2023-07-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0b9ab27fdc7694a77bf18b17f322aea0a23d5bf6

commit 0b9ab27fdc7694a77bf18b17f322aea0a23d5bf6
Author: Jan Keitel <jkeitel@google.com>
Date: Fri Jul 28 15:44:20 2023

Enforce time threshold before accepting KeyboardAccessory suggestions.

This CL enforces the same minimum time between showing the Autofill
suggestions and being able to accept them that is used elsewhere
(Desktop, legacy Autofill popup).

(cherry picked from commit 3b57d3e90b4ce28a23dd7029add35ce9834600a9)

Bug: 1465230
Change-Id: I97e606fed01e377eb815ec2b60e18e3d767246b2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4705215
Commit-Queue: Jan Keitel <jkeitel@google.com>
Reviewed-by: Jihad Hanna <jihadghanna@google.com>
Reviewed-by: Bruno Braga <brunobraga@google.com>
Reviewed-by: Adem Derinel <derinel@google.com>
Reviewed-by: Christoph Schwering <schwering@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1174728}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4727924
Reviewed-by: Florian Leimgruber <fleimgruber@google.com>
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Reviewed-by: Viktor Semeniuk <vsemeniuk@google.com>
Cr-Commit-Position: refs/branch-heads/5845@{#888}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/0b9ab27fdc7694a77bf18b17f322aea0a23d5bf6/chrome/browser/ui/autofill/autofill_popup_controller_unittest.cc
[modify] https://crrev.com/0b9ab27fdc7694a77bf18b17f322aea0a23d5bf6/components/autofill/core/common/autofill_features.cc
[modify] https://crrev.com/0b9ab27fdc7694a77bf18b17f322aea0a23d5bf6/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/0b9ab27fdc7694a77bf18b17f322aea0a23d5bf6/tools/metrics/histograms/metadata/autofill/histograms.xml
[modify] https://crrev.com/0b9ab27fdc7694a77bf18b17f322aea0a23d5bf6/chrome/browser/ui/android/autofill/autofill_keyboard_accessory_view.cc
[modify] https://crrev.com/0b9ab27fdc7694a77bf18b17f322aea0a23d5bf6/components/autofill/core/common/autofill_features.h
[modify] https://crrev.com/0b9ab27fdc7694a77bf18b17f322aea0a23d5bf6/chrome/browser/ui/autofill/autofill_keyboard_accessory_adapter.cc


### [Deleted User] (2023-07-28)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-03)

Congratulations, Thomas! The VRP Panel has decided to award you $2,000 for your finding that resulted in the discovery of this issue through your original report as well as the communications and follow-through you presented here in the pathway to resolution of this issue. Thank you for your efforts! 

### st...@gmail.com (2023-08-03)

Thank you, I truly appreciate this being taken into consideration and I'm glad I have been able to help!

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/145c6539a80e3996ce96c730c0022e40a723ce1e

commit 145c6539a80e3996ce96c730c0022e40a723ce1e
Author: Jan Keitel <jkeitel@google.com>
Date: Tue Sep 19 23:46:26 2023

Clean up AutofillKeyboardAccessoryAcceptanceDelayThreshold feature.

The feature only ever served as a kill switch and landed in M116.

As part of cleaning up the feature, it also gets rid of
AcceptSuggestionWithoutThreshold, as this method is now only used in
tests.

Bug: 1465230
Change-Id: I7e500dc74bccbf809303b43a666e53642c51c1d3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4871900
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Auto-Submit: Jan Keitel <jkeitel@google.com>
Reviewed-by: Christoph Schwering <schwering@google.com>
Reviewed-by: Bruno Braga <brunobraga@google.com>
Commit-Queue: Ken Buchanan <kenrb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1198689}

[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/chrome/browser/ui/autofill/autofill_popup_controller_unittest.cc
[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/components/autofill/core/common/autofill_features.cc
[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/chrome/browser/ui/autofill/autofill_keyboard_accessory_adapter.h
[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/chrome/browser/ui/autofill/autofill_popup_controller.h
[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/chrome/browser/autofill/mock_autofill_popup_controller.h
[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/chrome/browser/ui/android/autofill/autofill_keyboard_accessory_view.cc
[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/components/autofill/core/common/autofill_features.h
[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/chrome/browser/ui/views/autofill/popup/popup_view_views_unittest.cc
[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/chrome/browser/webauthn/chrome_webauthn_autofill_mac_interactive_uitest.mm
[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/chrome/browser/ui/autofill/autofill_popup_controller_impl.h
[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/chrome/browser/webauthn/chrome_webauthn_autofill_interactive_uitest.cc
[modify] https://crrev.com/145c6539a80e3996ce96c730c0022e40a723ce1e/chrome/browser/ui/autofill/autofill_keyboard_accessory_adapter.cc


### [Deleted User] (2023-11-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fe...@gmail.com (2023-11-02)

Hello, I want to re-open my duplicate report, in the report
https://bugs.chromium.org/p/chromium/issues/detail?id=1459779#c_ts1698903367

I have provided the latest report, if my report is different from this report, and it is still affected in the latest version currently 119.

It's strange if it's compared to this report and it affects Android, whereas I'm on a desktop and it's a different POC.


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1465230?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1459192]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067505)*
