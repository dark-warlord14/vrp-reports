# Security: UaF in Aura

| Field | Value |
|-------|-------|
| **Issue ID** | [40050071](https://issues.chromium.org/issues/40050071) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mm...@semmle.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2019-09-06 |
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

Summary: UaF in the browser process that may allow sandbox escape from a compromised renderer.

I'm not totally sure what's happening here. This is triggered from the desktop capture mojo interface, but the UaF actually happens in Aura and may worth having someone there to take a look. I've so far seen 3 different asan stack traces. Two of them requires shutdown and one doesn't.

For capture\_shutdown\_asan(2), from the stack traces, my guess is that the notification view created in ScreenCaptureNotificationUI::Create [1] somehow got stored in a Widget as the raw pointer |non\_client\_view\_| [2] (capture\_shutdown\_asan) or |widget\_delegate\_| [3] (capture\_shutdown\_asan2). I'm not sure how it gets there. Then during shutdown, the MediaStreamUIProxy that owns the notification window [4] gets deleted before the Widget that retains the pointer to the window, and a UaF is triggered.

For capture\_uaf\_asan, the MediaStreamUIProxy got killed when VideoCaptureHost::Stop is called, which will ended up calling MediaStreamManager::DeleteRequest and deletes the DeviceRequest [5] that owns the MediaStreamUIProxy [6], while the notification window is still alive, (probably means that the Widget that holds a raw pointer to it continues to access it after MediaStreamUIProxy is destroyed)

Thank you very much for your help and please let me know if there is anything that I can help. Any insight and feedback into the root cause of the problem will be greatly appreciated. Thanks!

1. <https://cs.chromium.org/chromium/src/chrome/browser/ui/screen_capture_notification_ui.h?q=ScreenCaptureNotificationUI::Create&g=0&l=22&rcl=b538175ebbc41a0f71f7e72e87613b32ea66a267>
2. <https://cs.chromium.org/chromium/src/ui/views/widget/widget.h?g=0&l=1008&rcl=b538175ebbc41a0f71f7e72e87613b32ea66a267>
3. <https://cs.chromium.org/chromium/src/ui/views/widget/widget.h?g=0&rcl=b538175ebbc41a0f71f7e72e87613b32ea66a267&l=997>
4. <https://cs.chromium.org/chromium/src/chrome/browser/media/webrtc/desktop_capture_devices_util.cc?g=0&l=189&rcl=b538175ebbc41a0f71f7e72e87613b32ea66a267>
5. <https://cs.chromium.org/chromium/src/content/browser/renderer_host/media/media_stream_manager.cc?type=cs&g=0&l=1117&rcl=b538175ebbc41a0f71f7e72e87613b32ea66a267>
6. <https://cs.chromium.org/chromium/src/content/browser/renderer_host/media/media_stream_manager.cc?q=devicerequest&g=0&l=473&rcl=b538175ebbc41a0f71f7e72e87613b32ea66a267>

**VERSION**  

Chrome Version: Tested on build from master a33ffe0, Ubuntu 18.04.2 LTS but may affect other OS.

**REPRODUCTION CASE**

1. For capture\_shutdown\_asan(2): First run the following to copy the generated mojo files:

$ python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen  

$ python -m SimpleHTTPServer&

replace the mojo\_bindings.js file with the attached one.  

Then run

$out/asan/chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/abc

and open the page '<http://localhost:8000/capture_shutdown.html>', when prompted, select "Your entire screen" then Share. Wait for the notification window to appear (the one says "you are sharing your screen") then shut down the browser. Should be fairly reliable, but may require a couple of attempts. Most of the time I got capture\_shutdown\_asan.

2. For capture\_uaf\_asan: Repeat the steps before but use capture\_uaf.html and does not require shutting down the browser.  
   
   **CREDIT INFORMATION**  
   
   **Externally reported security bugs may appear in Chrome release notes. If**  
   
   **this bug is included, how would you like to be credited?**  
   
   Reporter credit: Man Yue Mo of Semmle Security Research Team

## Attachments

- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)
- [capture_shutdown_asan](attachments/capture_shutdown_asan) (text/plain, 12.8 KB)
- [capture_shutdown_asan2](attachments/capture_shutdown_asan2) (text/plain, 16.0 KB)
- [capture_shutdown.html](attachments/capture_shutdown.html) (text/plain, 3.4 KB)
- [mojo_bindings.js](attachments/mojo_bindings.js) (text/plain, 162.8 KB)
- [capture_uaf_asan](attachments/capture_uaf_asan) (text/plain, 11.8 KB)
- [capture_uaf.html](attachments/capture_uaf.html) (text/plain, 3.4 KB)

## Timeline

### es...@chromium.org (2019-09-06)

Thanks for the report! Adding webrtc and Aura owners while I work on reproducing. Tentatively setting to High severity (memory corruption in browser process, requiring compromised renderer to exploit).

[Monorail components: Blink>WebRTC Internals>Aura Internals>Media>ScreenCapture UI>Aura]

### es...@chromium.org (2019-09-06)

Also tentatively setting Security_Impact-None since it requires a default-disabled feature to repro (--enable-blink-features=MojoJS).

### mm...@semmle.com (2019-09-06)

Thanks for looking into this. Sorry for not being clear in the description. The --enable-blink-features=MojoJS is just there to emulate a compromised renderer. It enables the mojo interface which a compromised renderer will have access to, so when you have a compromised renderer, you don't need to have this flag set. Thanks.

### mm...@semmle.com (2019-09-07)

OK I think I know what's happening now.

The |notification_ui| created in [1] is passed into RegisterMediaStream:

      notification_ui = ScreenCaptureNotificationUI::Create(                                   //<-- |notification_ui| created here
          GetStopSharingUIString(application_title, registered_extension_name,
                                 capture_audio, media_id.type));
    }
  }

  return MediaCaptureDevicesDispatcher::GetInstance()
      ->GetMediaStreamCaptureIndicator()
      ->RegisterMediaStream(web_contents, *devices, std::move(notification_ui));  //<-- passed into RegisterMediaStream
}

This then create a UIDelegate that owns it [2]. This UIDelegate is owned by a MediaStreamUIProxy that is owned by a DeviceRequest (as explained in the Vulnerability Details), which can be deleted by the mojo interface VideoCaptureHost::Stop.

Now  UIDelegate owns notification_ui as |ui_| [3]. When onStreamStart is called, it will call the |onStart| method of |ui_| [4]. This creates the relevant Widget [5], as well as passing the |this| pointer (which is the raw pointer to the original |notication_ui|) to the initialization parameters [6]:

  views::Widget::InitParams params(views::Widget::InitParams::TYPE_WINDOW);
  params.delegate = this;          //<-- passing |this| to the initialization params
  ...
  widget->Init(std::move(params)); //<-- |this| now used to initialize widget

|this| then becomes the raw |widget_delegate_| in |widget| [7]. As |widget|'s lifetime is not bound to the lifetime of the |notification_ui| (|ui_| in |UIDelegate|), when UIDelegate is destroyed, |widget| is still alive and |widget_delegate_| becomes a dangling pointer and subsequent uses of it causes UaF. 

So this issue is probably more of an issue in DesktopCapture rather than Aura (probably should change the title and components etc.) and I'd suggest to make sure that |widget| is destroyed before |ui_| in UIDelegate does. Thanks and please let me know if it makes sense.
                                                                                
1. https://cs.chromium.org/chromium/src/chrome/browser/media/webrtc/desktop_capture_devices_util.cc?g=0&l=197&rcl=b538175ebbc41a0f71f7e72e87613b32ea66a267
2. https://cs.chromium.org/chromium/src/chrome/browser/media/webrtc/media_stream_capture_indicator.cc?g=0&l=188&rcl=b538175ebbc41a0f71f7e72e87613b32ea66a267
3. https://cs.chromium.org/chromium/src/chrome/browser/media/webrtc/media_stream_capture_indicator.cc?g=0&l=144&rcl%3Db538175ebbc41a0f71f7e72e87613b32ea66a267
4. https://cs.chromium.org/chromium/src/chrome/browser/media/webrtc/media_stream_capture_indicator.cc?g=0&rcl%3Db538175ebbc41a0f71f7e72e87613b32ea66a267&l=170
5. https://cs.chromium.org/chromium/src/chrome/browser/ui/views/screen_capture_notification_ui_views.cc?rcl%3Db538175ebbc41a0f71f7e72e87613b32ea66a267&g=0&l=192
6. https://cs.chromium.org/chromium/src/chrome/browser/ui/views/screen_capture_notification_ui_views.cc?rcl%3Db538175ebbc41a0f71f7e72e87613b32ea66a267&g=0&l=195
7. https://cs.chromium.org/chromium/src/ui/views/widget/widget.cc?rcl%3Db538175ebbc41a0f71f7e72e87613b32ea66a267&g=0&l=320

### gu...@chromium.org (2019-09-09)

marinaciocea@: Can you take a look?

### gu...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

[Monorail components: -Blink>WebRTC -Internals>Aura -Internals>Media>ScreenCapture -UI>Aura Blink>GetUserMedia>Desktop]

### ma...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### mm...@semmle.com (2019-09-27)

Just took another look at this bug. It looks like you have indeed delete the Widget in the destructor:

https://cs.chromium.org/chromium/src/chrome/browser/ui/views/screen_capture_notification_ui_views.cc?g=0&rcl=c227659d53e18a0cb19da676fc59f40a86a63e55&l=172

The problem is that, if |ScreenCaptureNotificationUIViews::OnStarted| gets called more than once, then multiple widgets get created in [1] and they all share the same WidgetDelegate, which is |this| (see ScreenCaptureNotificationUIViews::OnStarted). However, in that situation, the newly created Widget will overwrite the previous Widget and when you call |GetWidget| in the destructor, you are only deleting the Widget that is created the latest. So when the ScreenCaptureNotificationUIViews is deleted, Widgets that are created previously will still hold onto a raw pointer referencing to the ScreenCaptureNotificationUIViews,  causing UaF. To fix this, you can either store all the created Widgets in [1] in a field, and make sure they all got deleted in the destructor, or check whether |GetWidget| returns null (in which case a widget is already created) before creating a new one.

1. https://cs.chromium.org/chromium/src/chrome/browser/ui/views/screen_capture_notification_ui_views.cc?g=0&rcl=c227659d53e18a0cb19da676fc59f40a86a63e55&l=188

Thanks and please let me know if this makes sense.

### mm...@semmle.com (2019-09-27)

Also regarding https://crbug.com/chromium/1001503#c2, do you mind reviewing the Security_Impact? As I have explained in https://crbug.com/chromium/1001503#c3 that the --enable-blink-features=MojoJS is just there to emulate a compromised renderer and is not needed to trigger the bug if the renderer is assumed to be compromised. Thank you very much for your help.

### gu...@chromium.org (2019-09-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-27)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2019-10-09)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8fe61c82a970fff810d27a884997a78153a92546

commit 8fe61c82a970fff810d27a884997a78153a92546
Author: Marina Ciocea <marinaciocea@chromium.org>
Date: Wed Oct 09 20:29:30 2019

Screen capture UI: don't recreate the widget if it already exists.

Bug: 1001503
Change-Id: I28c6c8445407315d8b2e9ab364cfb86f451758d9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1848385
Commit-Queue: Marina Ciocea <marinaciocea@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Commit-Position: refs/heads/master@{#704321}

[modify] https://crrev.com/8fe61c82a970fff810d27a884997a78153a92546/chrome/browser/ui/views/screen_capture_notification_ui_views.cc


### ma...@chromium.org (2019-10-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-10)

Requesting merge to stable M77 because latest trunk commit (704321) appears to be after stable branch point (681094).

Requesting merge to beta M78 because latest trunk commit (704321) appears to be after beta branch point (693954).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-10)

This bug requires manual review: We are only 11 days from stable.
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
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-10-10)

merge approved for M78, branch:3904

### sr...@google.com (2019-10-10)

Please help complete the merge to M78 branch by End of day Friday Oct 11, 2019, PST time zone.  Stable RC build will be triggered early next week

### ma...@chromium.org (2019-10-11)

Merged to M78 in https://crrev.com/c/1853226.

### na...@google.com (2019-10-14)

[Empty comment from Monorail migration]

### sr...@google.com (2019-10-14)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-17)

Assuming this affects all the normal platforms so it gets onto the right release TPM lists.

### la...@google.com (2019-10-17)

rejecting for M77 as the release is in Stable and no more re-spins are planned

### na...@google.com (2019-10-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-10-18)

Congrats! The Panel decided to reward $20,000 for this report. 

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### mm...@semmle.com (2019-10-21)

natashapabrai@ Thanks! My employer has a policy of donating reward to charity. Do you mind donating the reward to TearFund (https://www.tearfund.org/) please? Thanks.

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-05)

marinaciocea@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### sh...@chromium.org (2020-01-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-29)

[Comment Deleted]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1001503?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050071)*
