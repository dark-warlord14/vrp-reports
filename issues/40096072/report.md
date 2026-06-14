# Security: UaF in MediaSession, Android only

| Field | Value |
|-------|-------|
| **Issue ID** | [40096072](https://issues.chromium.org/issues/40096072) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Session |
| **Platforms** | Android |
| **Reporter** | mm...@semmle.com |
| **Assignee** | be...@chromium.org |
| **Created** | 2019-08-23 |
| **Bounty** | $20,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

Summary: A use-after-free in MediaSessionImpl may allow a compromised renderer to escape the Chromium sandbox on Android.

In the MediaSessionControllersManager::RequestPlay method, a MediaSessionController is created and initialize here [1]. When certain conditions that can be controlled from the renderer that makes the called (via the OnMediaPlaying IPC [2]), MediaSessionImpl::AddPlayer will be called. Again, provided the renderer provides the correct parameters, AddPepperPlayer will be called [3].

AudioFocusDelegate::AudioFocusResult result =  

RequestSystemAudioFocus(AudioFocusType::kGain); // <--- a  

DCHECK\_NE(AudioFocusDelegate::AudioFocusResult::kFailed, result);

pepper\_players\_.insert(PlayerIdentifier(observer, player\_id)); <--- b

...  

return result != AudioFocusDelegate::AudioFocusResult::kFailed;

The AddPepperPlayer method will insert a PlayerIdentifier with the created MediaSessionController inside it as a raw pointer (b), regardless of the result of the RequestSystemAudioFocus call in (a). In non Android platform, this call always returns AudioFocusDelegate::AudioFocusResult::kDelay, however, on Android, the call can return AudioFocusDelegate::AudioFocusResult::kFailed if another higher priviledged audio is holding the focus, such as when the phone is ringing. When this happens, MediaSessionController::Initialize will return false, leaving the has\_session\_ field false [4]. This will then also return false to MediaSessionControllerManager::RequestPlay, causing the created controller to be destroyed [5]

bool MediaSessionControllersManager::RequestPlay  

...  

std::unique\_ptr<MediaSessionController> controller(  

new MediaSessionController(id, media\_web\_contents\_observer\_));

```
  if (!controller->Initialize(has_audio, is_remote, media_content_type,  
	                          position)) {  
	return false;  
  }  

```

When the controller is destroyed, it checks whether has\_session\_ is true, if so, remove itself from the MediaSession [6]. However, in this case, because has\_session\_ field is left false, such clean up will not happen, leaving a free'd pointer in the PlayerIdentifier in pepper\_players\_. Any other subsequent IPC call from the renderer that triggers the use of observer\_ in the player will then result in a use-after-free. For example, just by calling OnMediaPlaying to trigger another AddPepperPlayer will do, because the UpdateRoutedService method called within it will iterate through all the pepper\_players\_ and call a function of the observer\_. So this bug is at least triggerable from a compromised renderer.

In practice, an attacker can probably just wait for the OnSuspend [7] event from the renderer to determine whether the first AddPlayer failed, if not, remove the player(by calling OnMediaPlaying again) to reset has\_session\_, and call OnMediaPlaying again until the phone rings and AddPlayer failed, and then reliably trigger the bug.

Thank you very much for your help and please let me know if there is anything that I can be of help. Thanks.

1. <https://cs.chromium.org/chromium/src/content/browser/media/session/media_session_controllers_manager.cc?g=0&rcl=401b300585124bf3dd78d2e6bc78f69ea69d9f6f&l=78>
2. <https://cs.chromium.org/chromium/src/content/browser/media/media_web_contents_observer.cc?g=0&l=140&rcl=401b300585124bf3dd78d2e6bc78f69ea69d9f6f>
3. <https://cs.chromium.org/chromium/src/content/browser/media/session/media_session_impl.cc?g=0&l=299&rcl=401b300585124bf3dd78d2e6bc78f69ea69d9f6f>
4. <https://cs.chromium.org/chromium/src/content/browser/media/session/media_session_controller.cc?g=0&l=80&rcl=401b300585124bf3dd78d2e6bc78f69ea69d9f6f>
5. <https://cs.chromium.org/chromium/src/content/browser/media/session/media_session_controllers_manager.cc?g=0&rcl=401b300585124bf3dd78d2e6bc78f69ea69d9f6f&l=80>
6. <https://cs.chromium.org/chromium/src/content/browser/media/session/media_session_controller.cc?g=0&rcl=401b300585124bf3dd78d2e6bc78f69ea69d9f6f&l=26>
7. <https://cs.chromium.org/chromium/src/content/browser/media/session/media_session_controller.cc?g=0&rcl=401b300585124bf3dd78d2e6bc78f69ea69d9f6f&l=80>  
   
   **VERSION**  
   
   Chrome Version: built from master branch commit db6e511  
   
   Operating System: Android emulator, Pixel2 API 28

**REPRODUCTION CASE**

The patches media\_session\_host.patch and media\_session\_android.patch are used for reproducing the issue in different platforms. I can't get asan build to work on Android, so the android patch, which shows the actual problem uses a CHECK to show that a free'd pointer is retained. This requires some changes to the browser side code (MediaSessionImpl and MediaSessionController), but should not affect the vulnerability. The patch media\_session\_host.patch is provided for debugging. It involves a change to the MediaSessionImpl::AddPepperPlayer method so that it always returns false to emulate the Android situation, but otherwise no change to the browser side code. This patch is used to produce the asan log. Both patches contains modifications to the renderer that emulate a compromised renderer.

Android: As I said I struggle to get asan working on the Android emulator, so I had to insert an assertion in the destructor of MediaSessionController to check that it frees itself while a raw pointer of it still remains in pepper\_players\_. Using this I was able to produce a crash when visiting media\_session.html while the phone is ringing. (i.e. first call the phone, while it is ringing, open the custom built chromium with media\_session\_android.patch applied and media\_session.html) This is tested on a master built with commit db6e511

Linux: Apply the patch media\_session\_host.patch to commit faf9f3f and then open the page media\_session.html. This should crash with UaF.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Man Yue Mo of Semmle Security Research Team

## Attachments

- [media_session_android.patch](attachments/media_session_android.patch) (text/plain, 6.6 KB)
- [media_session_host.patch](attachments/media_session_host.patch) (text/plain, 6.0 KB)
- [media_session.html](attachments/media_session.html) (text/plain, 158 B)
- [media_session_controller_asan](attachments/media_session_controller_asan) (text/plain, 16.6 KB)
- [media_session_android.patch](attachments/media_session_android_53123729.patch) (text/plain, 4.4 KB)

## Timeline

### mb...@chromium.org (2019-08-23)

Thanks for the report!

beccahughes: Are you a good owner for this? Feel free to pass it back to me for re-triage if not.

### mb...@chromium.org (2019-08-23)

[Empty comment from Monorail migration]

[Monorail components: Internals>Media>Session]

### be...@chromium.org (2019-08-23)

Yes I can take a look at this

### be...@chromium.org (2019-08-23)

This is probably not too serious since pepper / flash is not available on Android. I have a fix here:

https://chromium-review.googlesource.com/c/chromium/src/+/1769180

### be...@chromium.org (2019-08-23)

[Empty comment from Monorail migration]

### be...@chromium.org (2019-08-23)

Fix has landed.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e30383d507bb7f94a42a32c42d98ff2dd4811166

commit e30383d507bb7f94a42a32c42d98ff2dd4811166
Author: Becca Hughes <beccahughes@chromium.org>
Date: Fri Aug 23 22:06:31 2019

[Media Session] Fix issues in media session

For more context, please see the bug. This CL
is two part:

1) Unconditionally remove the player from
   the media session
2) Do not add a pepper player if focus fails

BUG=997190

Change-Id: I2f20d94762a2908c7531ce35cc2df110e5ba13aa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1769180
Commit-Queue: Becca Hughes <beccahughes@chromium.org>
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/heads/master@{#690096}

[modify] https://crrev.com/e30383d507bb7f94a42a32c42d98ff2dd4811166/content/browser/media/session/media_session_controller.cc
[modify] https://crrev.com/e30383d507bb7f94a42a32c42d98ff2dd4811166/content/browser/media/session/media_session_controller.h
[modify] https://crrev.com/e30383d507bb7f94a42a32c42d98ff2dd4811166/content/browser/media/session/media_session_controller_unittest.cc
[modify] https://crrev.com/e30383d507bb7f94a42a32c42d98ff2dd4811166/content/browser/media/session/media_session_impl.cc
[modify] https://crrev.com/e30383d507bb7f94a42a32c42d98ff2dd4811166/content/browser/media/session/media_session_impl.h
[modify] https://crrev.com/e30383d507bb7f94a42a32c42d98ff2dd4811166/content/browser/media/session/media_session_impl_browsertest.cc


### sh...@chromium.org (2019-08-24)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-24)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-24)

Requesting merge to stable M76 because latest trunk commit (690096) appears to be after stable branch point (665002).

Requesting merge to beta M77 because latest trunk commit (690096) appears to be after beta branch point (681094).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-24)

This bug requires manual review: M77 has already been promoted to the beta branch, so this requires manual review
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
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-08-26)

[Empty comment from Monorail migration]

### be...@chromium.org (2019-08-27)

[Empty comment from Monorail migration]

### be...@chromium.org (2019-08-29)

This has been approved, please merge ASAP.

### sh...@chromium.org (2019-09-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-09-03)

We're not planning M76 respin as M77 goes to stable next week. Rejecting merge to M76.

### be...@chromium.org (2019-09-04)

Not sure we need this for Android based on comments in c#4. mlamouri@ could you comment since Becca is out?

### mm...@semmle.com (2019-09-05)

Thanks for looking into it. 

The bug itself does not require the use of pepper/flash. It is caused by the fact that a compromised renderer can provide bogus information and cause the browser to insert a |PlayerIdentifier| in the |pepper_players_| map. The |pepper_players_| set is just a generic set of PlayerIdentifier, which does not depend on pepper/flash being available and exists on Android [1]. This can be seen from the reproduction case when the assertion failed on Android, confirming that a dangling pointer is created in the |pepper_players_| set. The UaF is then triggered by calling ComputeServiceForRouting, which will go through all different |PlayerMap| (including |pepper_players_|) and call |render_frame_host| in the observer (which is now free'd in the |pepper_players_|), this again is generic code and also happens on Android. [2] So I believe this issue is relevent for Android.

In longer term, if pepper/flash is not available on Android, then it may make sense to remove the |pepper_players_| set in the Android build altogether.

Thanks!

1. https://cs.chromium.org/chromium/src/content/browser/media/session/media_session_impl.h?gsn=WebURL&q=pepper_players_&g=0&targetos=android&rcl=401b300585124bf3dd78d2e6bc78f69ea69d9f6f&l=305

2. https://cs.chromium.org/chromium/src/content/browser/media/session/media_session_impl.cc?gsn=WebURL&targetos=android&g=0&rcl=401b300585124bf3dd78d2e6bc78f69ea69d9f6f&l=1222

### ad...@chromium.org (2019-09-06)

In the absence of beccahughes@ I've gone through and had a look at this.

The fix does look like it fixes the UaF as reported. There are other changes to the related object lifetimes within the fix so I can't entirely convince myself that it's 100% safe.

This is a pretty serious one. Bugs which allow escapes from the renderer are pretty rare and very serious, so I think this needs to be merged if we possibly can get sufficient confidence, even at this very short notice before M77. benmason@ - I'll discuss with you on chat what we can do to see if we can get that confidence.

### ad...@google.com (2019-09-06)

I just e-mailed the team in question for a second opinion, but have since looked at the contents of the M77 branch in git. It looks like this fix is present!

Cherry-picked on Aug 27th as 2ac83ddf4400ae7eb76dc826d8f7b881892e1f97.

### be...@google.com (2019-09-06)

Removing merge approved label as this is merged as per c#21. Thanks Adrian!

### na...@google.com (2019-09-09)

mlamouri - can you verify if this report is exploitable for the VRP Panel to assess for a reward. 

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### ml...@google.com (2019-09-27)

If I understand correctly, the security issue here was in the browser process and in order to be used, requires an already compromised renderer. The affected code wouldn't run in production on Android (which is why it was a DCHECK) but a compromised renderer may be able to create a media player with the type Pepper. In that case, the browser process would go through the DCHECK and hit the security issue as described by OP.

I cannot assess fully the security issue severity/exploitability here but I would point out two things:
 - the security issue requires an already compromised renderer process. I do not know if it has any impact on the severity/exploitability of the issue.
 - the security issue requires Chrome to not be able to get audio focus which in practice is during a phone call. We have metrics about this and these events aren't very common. It would also not be easy to reliably figure out if the user is having a phone call. The easiest way would be to try to play something and see it being paused immediately after but that means that the page would have to play something continuously until the user places or receives a phone call which would likely get the page to be left by the user.

With the caveats above, an attacker that has a compromised renderer could attempt to use this vulnerability on every page visit and randomly be able to catch some users having phone calls.

### mm...@semmle.com (2019-09-30)

Thanks for the analysis. 

Regarding the first point. The issue does require a compromised renderer to hit the affected code in production, so the impact of the issue is a sandbox escape.

Regarding the second point. A compromised renderer does not need to play a sound to find out whether the user is having a phone call. I've attached another patch that emulates what a compromised renderer can do. If you patch an affected version of Chromium with the attached file to emulate a compromised renderer, and then open the page media_session.html with the patched version of Chromium. Then while the page is open, Chromium will trigger the bug and crash anytime when the phone rings (as long is it is not answered within 1/2 sec, probably can make it shorter). I do not notice any audible sound while the page is opened (at least on an emulator) and all it is needed to trigger the bug is for the page to be opened for long enough until the phone rings. The page also does not to be on the main tab to trigger the bug. (i.e. A user can open the page, then switch to view another page, and the bug will still be triggered if the phone rings)

Thank you very much for your help!

### na...@google.com (2019-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-04)

Congrats! The Panel decided to reward $20,000 for this report :) 

### na...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### mm...@semmle.com (2019-10-08)

natashapabrai@ Thank you very much for your help! My employer has a policy of donating reward to charity. Do you mind donating the reward to WWF (wwf.org.uk) please? Thanks.

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/997190?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### x4...@gmail.com (2025-06-13)

Reporter: Could you please tell me if you were able to get asan working for chromium android? I am struggling with the same and even after building it from source the app won't run.

Thanks in advnace!

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096072)*
