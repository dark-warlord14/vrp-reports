# Security: Android - Bypass the Protection of input fields cache (Autofill) Bypass 1398579

| Field | Value |
|-------|-------|
| **Issue ID** | [40062823](https://issues.chromium.org/issues/40062823) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android |
| **Reporter** | el...@gmail.com |
| **Assignee** | fr...@chromium.org |
| **Created** | 2023-01-29 |
| **Bounty** | $3,000.00 |

## Description

# **VULNERABILITY DETAILS**

this is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit. this vulnerability allows attackers to steal the cache of input fields like usernames, e-mail addresses, telephone numbers from any site like twitter, google and any others (Chrome Autofill Saved Data).

## ==================== Here in this Ticket I've Chained Two Bugs:

<https://crbug.com/chromium/1358647> > this bug fixed in Chrome Desktop before, in this bug the (Picture In Picture)PIP Overlay Covers the autofill data and make it invisible to users, Security Team Pushed two CLs

A) <https://chromium.googlesource.com/chromium/src/+/87cf1589bb30dde902d74657840c8486b605a9b1> ,Add GetWindowBounds for PictureInPicture  

The window bounds would be used to check for any overlaps with the Autofill popup in the next CLs.

B) <https://chromium.googlesource.com/chromium/src/+/ff1874e9b31c51520032643e4ce3101a42743dee> ,Hide Autofill popup if it overlaps with picture-in-picture window.

This CL introduces BoundsOverlapWithPictureInPictureWindow used in  

autofill\_popup\_view\_native\_views.cc to determine whether there is an  

overlap between the picture-in-picture window and the autofill popup.  

If it does, it hides the autofill popup.

- But this wasn't Introduced to Chrome for Android.  
  
  =====================

<https://crbug.com/chromium/1398579> > fixed Autofill data visibility by Setting Minimum autofill row height in android to (50x50dip) at (AnchoredPopupWindow.java) to avoid Being docked as a line and to protect user from selecting sensitive info without being aware.

# <https://chromium-review.googlesource.com/c/chromium/src/+/4123739/21/ui/android/java/src/org/chromium/ui/widget/AnchoredPopupWindow.java#41> <https://chromium-review.googlesource.com/c/chromium/src/+/4123739/21/ui/android/java/src/org/chromium/ui/widget/AnchoredPopupWindow.java#42>

Merging the two above i can Construct a new Bypass Same As <https://crbug.com/chromium/1358647> by Hiding Autofill data behind PIP Overlay that is same color to Autofill popup in Android ,as i have picked the color and made simple giphy.webm same color of autofill popup , and bypassed the fix of minimum popup row height introduced in <https://crbug.com/chromium/1398579>

# ===================== **VERSION**

Exploit tested with the following properties:  

Google Chrome DEV (Android) Version 111.0.5557.0 /Google Pixel6 Android 13.

## ===================== **REPRODUCTION CASE** :

the exploit use a vulnerability in showing of cache of input fields. your browser suggests the saved entries of input fields like saved user logins (username, email, phone number...) or cached search word any similar entered things.

nobody will send critical information to unknown sites. but this can be hide by full bypassing the visibility of all fields and suggests. in this case nobody are able to notice that they are sending their data to unknown attackers.

## ===================== REPRODUCTION STEPS:

(Play a little Game(Sniper) like in this one(<https://crbug.com/chromium/1398579>) to get hijacked any cached input of fieldname "username",email,telephone,address,card-number,.....), But Here I've made a simple poc withot game as requested in main one <http://crbug.com/1398579#c4>

\*\*Before Repro you can add some data under chrome://settings/addresses and add some records

1-visit <https://vrphunt.com/chrome/android/dyn-autofill/bypass-autofill-restrictions.html>

\*\* Note: Fields opacity visible to you so that you can see how attack works\*\*

2- Tap on Body >> this will open (Picture In Picture)PIP-Overlay that is same color to autofill popup.

3-Tap on Body again >> this tab will show one row in autofill data popup behind PIP-Overlay, I've used Virtual Keyboard API to force Hide Android KB while taping on input field.

4-Tap on Left bottom Corner (Between Dashed and Solid Red Lines), >> this will make the victim blindly select autofill data , Check Green Box behind with Autofill Data will be sent to Attacker Side.

Autofill data Will be shown in the Green Box

# ========= Observed:

Autofill popup can be made hidden behind PIP Overlay and User Can Unknowly Select secret Autofill Data and send to attacker C&C server without being aware.

# Expected:

Sensitive browser UI is always visible to user ,so Hide Autofill popup if it overlaps with picture-in-picture Overlay and user should see the auto fill data

# Fix:

Hide Autofill popup if it overlaps with picture-in-picture window.

> > this Check should be also introduced in Chrome for Android to prevent such like this attacks  
> > 
> > <https://chromium.googlesource.com/chromium/src/+/ff1874e9b31c51520032643e4ce3101a42743dee>

\*\*Poc Video shows the behavior and How attack works.\*\*

# \*\*Offline Poc Files also Attached you can host on webserver and test , But Online Demo Works Perfect as shown . \*\*

Notes:

This is Similar to

<https://crbug.com/chromium/1398579> <https://crbug.com/chromium/1358647>

---

**CREDIT INFORMATION**  

Reporter credit: Ahmed ElMasry

---

Thank you for your attention. with kind Regards

## Attachments

- [PoC.mp4](attachments/PoC.mp4) (video/mp4, 8.3 MB)
- [base.css](attachments/base.css) (text/plain, 3.0 KB)
- [bypass-autofill-restrictions.html](attachments/bypass-autofill-restrictions.html) (text/plain, 4.0 KB)
- [giphy.webm](attachments/giphy.webm) (video/webm, 6.5 KB)
- [with_keyboard.png](attachments/with_keyboard.png) (image/png, 193.0 KB)
- [no_keyboard.png](attachments/no_keyboard.png) (image/png, 128.3 KB)

## Timeline

### [Deleted User] (2023-01-29)

[Empty comment from Monorail migration]

### rs...@chromium.org (2023-01-31)

Thanks for the report! I can reproduce this on an Android emulator device.

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2023-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-31)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vi...@google.com (2023-02-02)

[Empty comment from Monorail migration]

### li...@google.com (2023-02-03)

[Empty comment from Monorail migration]

### yr...@chromium.org (2023-02-06)

[Empty comment from Monorail migration]

### yr...@chromium.org (2023-02-09)

I tested this on a Pixel 5 phone with screenshots attached, for both scenarios when virtual keyboard is enabled or disabled. The autofill suggestion shows up as a row above the keyboard, so it doesn't really get overlapped with the PiP window easily. Even if I move PiP window onto the autofill bubble, user still needs to click on the bubble for the suggestion to be applied, while clicking on the PiP window or webpage has no effect, so I don't think it's easy for user to apply suggestion without noticing it.

If we want to follow the non-android case to hide the autofill suggestion when it overlaps with PiP window, we need to do the following (another easier solution is to just disable autofill when there's a PiP window):
1. Know the screen location where autofill bubble shows
2. Know the screen location of the PiP window as user moves it
3. Check if these two locations overlap and show/hide autofill accordingly

Even if we may be able to reuse BoundsOverlapWithPictureInPictureWindow() [1] to check if the locations overlap, I feel that we still need to add new methods to get the 2 screen locations since Android views are different from normal web views. I still need to do more research to see how Android autofill view works and how to add listener on PiP window to return its location as user moves it. Since I'm not familiar with those codes and have another project with deadline, and this issue is not urgent as I analyzed above, I would come back to work on this once I have more time in the future.

Notes:

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/autofill/popup/popup_view_utils.cc;l=318;drc=a9356254845e55ea4fbc45455b39b51ed7e85505;bpv=0;bpt=0

[2] Potential Android autofill view class to look into further https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/android/autofill/autofill_popup_view_android.cc;bpv=0;bpt=1

[3] Looked into overriding performOnConfigurationChanged(Configuration newConfig) in PictureInPictureActivity.java for (2) but seems like it can't give the screen location of PiP window https://developer.android.com/guide/topics/resources/runtime-changes 

[4] Sample test website is missing this line `navigator.virtualKeyboard.overlaysContent = true;` for keyboard to hide https://developer.chrome.com/docs/web-platform/virtual-keyboard/#opting-in-to-the-new-virtual-keyboard-behavior, and this can be added in chrome://inspect#devices when inspecting Android chrome webpage

### el...@gmail.com (2023-02-09)

Hi ..,
I see you are testing that on chrome canary which has "The replacement of the autofill dropdown"  

As per https://bugs.chromium.org/p/chromium/issues/detail?id=1398579#c12  battre@ stated that there would be a new replacement for autofill  but still not stable enough.

So, please follow instructions above and test that  on ( Chrome DEV ) for more debugging, and  shown behavior in poc video .

This issue is similar to 1398579 and can be exploited by same way using games.

If you feel you are not the right owner and not familiar enough with that area battre@ could you ask  fhorschig@ to take ownership or re-route this?


Thanks 


### yr...@chromium.org (2023-02-09)

I did test with a Chrome dev version, so that autofill replacement thing might already be enabled, and I'm not sure how to disable it via a flag or something. 

I thinking having someone familiar with Android autofill would be the best person to fix this issue, as I only know part about Android picture-in-picture. If you can find a better owner that's great. If you still want me to fix it, it's gonna take a while and I still need to reach out to Android autofill folks for help.

### el...@gmail.com (2023-02-09)

Hi Yiren..,

Thanks for your attention and reply .,

Happy to help you here if i can.., replying to your concerns

>>so that autofill replacement thing might already be enabled, and I'm not sure how to disable it via a flag or something. 

Rep:/
Just under chrome://flags search for Autofill suggestions as keyboard accessory view
Like below link and select Disabled  then Relunch Chrome DEV .

chrome://flags/#autofill-keyboard-accessory-view

Default works for me in version 111.0.5563.8 (Official Build) dev (64-bit)  for Android 

----------

>> I thinking having someone familiar with Android autofill would be the best person to fix this issue, as I only know part about Android picture-in-picture.

Rep:/ from my previous Autofill related issues vidhanj@google.com , mamir@chromium.org works in Autofill part  and also fhorschig@chromium.org  , Friedrich fixed the main bug https://crbug.com/chromium/1398579, he can join you , just ask him 

beaufort.francois@gmail.com François works in PIP part , can join you .

All what i need is to help you if i can :), you are most welcome to fix this ,i appreciate your efforts and hard work in advance.

Mike mlerman@
Could you add folks mentioned in this comment please to work with Yiren  yrw@

Thank you All.


### yr...@chromium.org (2023-02-10)

With the flag autofill-keyboard-accessory-view disabled, I'm able to reproduce this issue with a similar result in the video. 

For either the flag is enabled or not, I saw the BoundsOverlapWithPictureInPictureWindow() [1] check is never triggered. Since I'm not familiar with autofill codes, it's probably the autofill team's responsibility to add in this check in autofill classes for Android too. I've heard that vidhanj@ doesn't have capacity to work on this issue, so someone else from autofill team needs to be looped in.

The best we PiP team can do is to make sure PictureInPictureWindowManager::GetPictureInPictureWindowBounds() returns the correct bounds for Android, which currently we don't since OverlayWindowAndroid::GetBounds() [2] only returns the PiP window size and doesn't know the PiP window's physical location on Android.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/autofill/popup/popup_view_utils.cc;l=318;drc=a9356254845e55ea4fbc45455b39b51ed7e85505;bpv=0;bpt=0
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/android/overlay/overlay_window_android.cc;l=238;bpv=1;bpt=0;drc=21f84c617ad57db20ee58d67a0914e69db759c5a

### el...@gmail.com (2023-02-10)

Thanks Yiren for your analysis.,

>>I've heard that vidhanj@ doesn't have capacity to work on this issue, so someone else from autofill team needs to be looped in.

Rep:/

Friedrich fixed the main bug https://crbug.com/chromium/1398579
fhorschig@chromium.org

You can CC him to this case , and ask him if he could help.

Thanks 
 


### ml...@chromium.org (2023-02-14)

Hi, we're working to enabling the Keyboard Accessory flag more broadly in the coming milestones. I expect that by the time we root-cause and land a fix to this issue, we'll have enabled (or be close to enabling) the flag anyways, rendering the fix moot.

As such, I suggest this issue is functionally obselete.

### el...@gmail.com (2023-02-14)

Thanks Mike mlerman@ for Cc'ing Friedrich fhorschig@ ,

>>we're working to enabling the Keyboard Accessory flag more broadly in the coming milestones. I expect that by the time we root-cause and land a fix to this issue, we'll have enabled (or be close to enabling) the flag anyways, rendering the fix moot.

Rep://
Keyboard Accessory flag  is still <not> enabled by default in dev version , and it's not necessary for anyone to use the new Autofill  UI , for example , there will be some users will use Old Autofill UI  as it's very simple and show detailed data ,so the fix should be here at least after releasing the new one and getting user feedbacks after being landed in more stable releases, as it's the majority of users.

Once the Keyboard Accessory flag is here in settings flags, there will be a choice to user to select old autofill or new one, and by neglecting this issue fix ,all users that will switch to old autofill by disabling flag after being set  in (stable release),will be affected by this bug, if the flag settings was removed  totally from settings and NEW Autofill  UI  will be forced to all users , we can say that this issue fix is not necessary and functional obselete,

We need to protect All Users Right?
+NEW UI will be protected if the flag is enabled as default.
+Old UI will not be protected if they decided to use OLD Autofill UI
+If the new UI is enforced and no way yo change to old one neglect this fix.
+Old UI users deserve protecting them by Fixing this issue , and as mentioned in main bug description and Yiren Comment https://crbug.com/chromium/1411109#c12 ,the bug fix seem to be straight forward, as some of code fix was landed before but still not triggered.

Thanks 

### fr...@chromium.org (2023-02-14)

Re #15
It's correct that the feature is not enabled by default at the moment. I'll update this bug next week with whether this remains the case and by which milestone we intend to change it.

It's incorrect to assume that the default-enabled status is the source of truth for the distribution of a fix. It's exactly what it sounds like: the default state. If there is an urgent reason to change it for all users, that's possible and not restricted to a version.

It's incorrect to assume there will be a settings toggle. If the accessory rolls out, there will be no way back to the old UI. Users cannot decide against this. (Putting Chrome into an unsupported, experimental state by enabling/disabling chrome:flags at will is not something we can guard against. The option space is too large and it's why we deprecate flags after launch.)

Of course we want to protect all users. I'd like to highlight that https://crbug.com/chromium/1411109#c14 is very right in questioning whether we find a fix in time, though. This is definitely non-trivial and if we have to decide between fixing vs replacing the surface, it seems sensible to do the latter. If we know that replacing isn't possible in the near future, I'll check in again. (I hope to have clarity by next week already.)

### el...@gmail.com (2023-02-15)

Thanks Friedrich fhorschig@  , waiting your feedback and update next week. thanks again for your time in advance


### fr...@chromium.org (2023-02-20)

Reviews are ongoing.

### fr...@chromium.org (2023-02-24)

[Empty comment from Monorail migration]

### fr...@chromium.org (2023-02-27)

[Empty comment from Monorail migration]

### fr...@chromium.org (2023-03-01)

(Review delays)

### el...@gmail.com (2023-03-14)

Hi Friedrich fhorschig@ any further updates on this? is this under your radar?
Thanks 

### fr...@chromium.org (2023-03-15)

Yes. The plan proceeds as anticipated.
We gradually roll out the keyboard accessory and thus, making this issue obsolete for all users with 112 or later.
There is no way to fix it faster than this. (I'll leave this bug open until we have confirmation that the fix reached all users ... it will take some weeks but work retroactively.)

### yr...@chromium.org (2023-03-15)

Setting Friedrich as owner to better track this

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### fr...@chromium.org (2023-05-19)

Rollout has completed. Users don't experience this anymore.

### [Deleted User] (2023-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-19)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-05-22)

Thanks Friedrich fhorschig@ for your time, taking care of this report and following up, i confirm that the fix has been rolled out to users.


### fr...@chromium.org (2023-05-23)

Thanks for the confirmation!

### am...@google.com (2023-05-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-25)

Congratulations, Ahmed! The VRP Panel has decided to award you $3,000 for this report. The reward amount was determine based on this particular variation of this issue being quite substantially mitigated. Thank you for your efforts and reporting this issue to us! 

### el...@gmail.com (2023-05-26)

Thanks Amy for the reward!


### am...@google.com (2023-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-11)

Hi Ahmed, please remember we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted them. Thanks! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1411109?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062823)*
