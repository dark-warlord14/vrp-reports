#  spoof file reads and writes Document using PIP

| Field | Value |
|-------|-------|
| **Issue ID** | [403792431](https://issues.chromium.org/issues/403792431) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P3 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Windows |
| **Reporter** | sa...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2025-03-16 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
the vulnerability like https://issues.chromium.org/issues/40076120 or https://issues.chromium.org/issues/40057200 (read environment variable)

By cleverly positioning a pop-up it is possible to force the file dialog to spawn behind the PiP window, completely obscured. Since the dialog still receives focus, it's possible to trick the user into saving or opening a file at an arbitrary file path or read env environment  variable

VERSION
Chrome Version:  136.0.7069.0 (Official build) canary (64 bit)
Operating System: Windows 11

REPRODUCTION CASE
The repro currently assumes that you've set your  path  - this could be worked around by using the File System API.
The paths used are defined by the fileWritePath variables respectively. ( i use .gitconfig file in "%userprofile%")

1.  Open the stealx (1).html file in the browser
2.  Double Click the button
3 . Press Enter , Ctrl V then enter

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If
this bug is included, how would you like to be credited?
Reporter credit:

## Attachments

- [stealx (1).html](attachments/stealx (1).html) (text/html, 1.4 KB)
- [bandicam 2025-03-16 13-23-50-641.mp4](attachments/bandicam 2025-03-16 13-23-50-641.mp4) (video/mp4, 1.8 MB)

## Timeline

### ps...@google.com (2025-03-16)

Thanks for the report. steimel@ can you take a look to see if this is the same issue as 40076120. Tested and confirmed POC setting severity to match 40076120. 

### ch...@google.com (2025-03-17)

Setting milestone because of s2 severity.

### ch...@google.com (2025-03-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### st...@chromium.org (2025-03-18)

Yes this is the same issue. We ended up having to disable the fix from that issue since it caused some unforeseen other issues. I'm currently working on something that will mitigate this particular case, though the longer-term file dialog plan is father out than that

### sa...@gmail.com (2025-03-18)

Hi thank you but https://issues.chromium.org/issues/40076120 is already fix and i have tested in version 136 it cannot reproduced.

### ch...@google.com (2025-04-01)

steimel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-02)

steimel: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-03)

steimel: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-04)

steimel: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-04)

steimel: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-05)

steimel: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-06)

steimel: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-07)

steimel: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-04-08)

steimel: Uh oh! This issue still open and hasn't been updated in the last 21 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### st...@chromium.org (2025-04-08)

Sorry for the delay on this. I'm working on a new solution since the original solution of closing pips while file dialog are open caused too many issues. The new solution will be tucking pip windows off of the screen while file dialogs are open

### pg...@google.com (2025-04-21)

It is hard to track down a proper introduction point for ui issues but I imagine this issue was present from before M136 - removing the release block

### ch...@google.com (2025-04-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2025-04-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### st...@chromium.org (2025-04-23)

@pg...@chromium.org it looks like the bot is re-adding releaseblock stable every day. Is there something we need to change to prevent that?

### pg...@google.com (2025-04-23)

I think this should do the trick! thank you!

((will file a bug to have the bot check for the removal of a tag before re-adding it.. if that is what its missing))

### ch...@google.com (2025-05-08)

steimel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### st...@chromium.org (2025-05-12)

Update: I got lgtm from the main reviewer of the CL and working on getting owners reviews

### ch...@google.com (2025-05-27)

steimel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### st...@chromium.org (2025-05-29)

Update: I need one more reviewer to +1 it. We've had some discussions, but then I was OOO last week and they're OOO this week. Hopefully next week everything is resolved and I can land this

### st...@chromium.org (2025-06-09)

Update: The CL required some refactoring for an edge case I hadn't considered. That is done so now awaiting review again

### dx...@google.com (2025-06-10)

Project: chromium/src  

Branch: main  

Author: Tommy Steimel [steimel@chromium.org](mailto:steimel@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6449682>

[pip] Tuck picture-in-picture windows when a file dialog is open

---


Expand for full commit details
```
     
    Picture-in-picture windows can occlude file dialogs, and initially we 
    tried to prevent this by closing all pip windows whenever a file 
    dialog was open. This created its own set of problems, so that feature 
    was disabled. 
     
    This is a replacement of that feature: instead of closing pip windows, 
    this moves them off to the side of the screen, preventing them from 
    obscuring the file dialog without having to actually close them. 
     
    go/picture-in-picture-tucking-design-doc 
     
    Bug: 403792431, 384050903, 415979072 
    Change-Id: I280333c32a02aee3c345c839e88848de6820ebe2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6449682 
    Reviewed-by: Evan Liu <evliu@google.com> 
    Commit-Queue: Tommy Steimel <steimel@chromium.org> 
    Reviewed-by: Frank Liberato <liberato@chromium.org> 
    Reviewed-by: Fr <beaufort.francois@gmail.com> 
    Cr-Commit-Position: refs/heads/main@{#1471975}

```

---

Files:

- M `chrome/browser/file_select_helper.cc`
- M `chrome/browser/file_select_helper.h`
- M `chrome/browser/picture_in_picture/BUILD.gn`
- A `chrome/browser/picture_in_picture/picture_in_picture_window.h`
- M `chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc`
- M `chrome/browser/picture_in_picture/picture_in_picture_window_manager.h`
- M `chrome/browser/picture_in_picture/picture_in_picture_window_manager_unittest.cc`
- A `chrome/browser/picture_in_picture/scoped_tuck_picture_in_picture.cc`
- A `chrome/browser/picture_in_picture/scoped_tuck_picture_in_picture.h`
- M `chrome/browser/ui/BUILD.gn`
- M `chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.cc`
- M `chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.h`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.cc`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views.h`
- M `chrome/browser/ui/views/overlay/video_overlay_window_views_unittest.cc`
- A `chrome/browser/ui/views/picture_in_picture/OWNERS`
- A `chrome/browser/ui/views/picture_in_picture/README.md`
- A `chrome/browser/ui/views/picture_in_picture/picture_in_picture_tucker.cc`
- A `chrome/browser/ui/views/picture_in_picture/picture_in_picture_tucker.h`
- A `chrome/browser/ui/views/picture_in_picture/picture_in_picture_tucker_unittest.cc`
- M `chrome/test/BUILD.gn`
- M `media/base/media_switches.cc`
- M `media/base/media_switches.h`
- M `tools/metrics/histograms/metadata/media/enums.xml`
- M `tools/metrics/histograms/metadata/media/histograms.xml`

---

Hash: 923d0eca9ed86960af9e735f8a4b2271fa17fb37  

Date:  Tue Jun 10 18:52:42 2025


---

### sa...@gmail.com (2025-06-10)

Is this already fixed?

### st...@chromium.org (2025-06-10)

The CL that just landed should fix it. It's not in canary yet though

### sa...@gmail.com (2025-06-10)

If this ia already fixed the bug status is set to fixed not accepted isnt it?

### st...@chromium.org (2025-06-16)

Fix landed in 139.0.7232.0

### pg...@google.com (2025-06-16)

handling merges in issue 384050903 - removing merge labels from here 

... there were no merge labels but i got way ahead. consider this a note to my future self lol

### sp...@google.com (2025-06-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact user information disclosure / security UI spoof 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-18)

This was actually a duplicate of a previous reported issue and we did not noticed that in the CL before rewarding this.
Merging this as a duplicate in the correct direction.

### am...@chromium.org (2025-06-18)

This reporter of this issue has opened a new report ([issue 425906331](https://issues.chromium.org/issues/425906331)) conveying this issue is not yet resolved, which I have merged into this issue as a duplicate seeing how this fix was only recently landed.

### sa...@gmail.com (2025-06-18)

hi bug https://issues.chromium.org/issues/425906331 is bypass of this report (not duplicate of this report) . this report already fixed

### am...@chromium.org (2025-06-18)

Apologies, but I'm not sure I am following that this is a bypass. Based on the information provided in your report of 425906331, this appears that this issue was not fully resolved. Some further explanation of this being a bypass would be necessary for us to see it as such, especially since that report uses one of the same POCs as provided in this report with the same outcome / impact.

### sa...@gmail.com (2025-06-19)

This is not a complete bypass but the fix in 403792431 is not perfect so it can be exploited again. In the fix 403792431 the pip window is tucked on the right side of the screen so the file dialog is not behind the pip window. However, this fix should keep the pip window in its position without being able to be resized or moved which causes the file dialog to be behind it.

### dx...@google.com (2025-06-25)

Project: chromium/src  

Branch: main  

Author: Tommy Steimel [steimel@chromium.org](mailto:steimel@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6670016>

[pip] Ensure pip windows stay tucked when resized for child dialogs

---


Expand for full commit details
```
     
    We tuck picture-in-picture windows to the side of the screen while file 
    dialogs are open. We also resize document picture-in-picture windows 
    when they have a large child dialog to ensure the child dialog is not 
    clipped. If the child dialog resizing happens after the window is 
    tucked for a separate file dialog, then the window ends up on the 
    screen. To avoid this problem, this CL ensures that a document 
    picture-in-picture window is re-tucked if necessary when it resizes for 
    a child dialog. 
     
    Bug: 425906331, 403792431 
    Change-Id: Icff3024c9e99188a57c4d78a00e7104bc48a5b22 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6670016 
    Reviewed-by: Benjamin Keen <bkeen@google.com> 
    Commit-Queue: Tommy Steimel <steimel@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1478268}

```

---

Files:

- M `chrome/browser/ui/views/frame/picture_in_picture_browser_frame_view.cc`

---

Hash: 908575d645b16c1b4178872aff0b7304c96afa40  

Date:  Wed Jun 25 00:04:20 2025


---

### am...@chromium.org (2025-06-30)

Thank you for the updated fix. Re-merging this issue as a duplicate to the previously reported [issue 384050903](https://issues.chromium.org/issues/384050903). It was only after this was rewarded that we realized there was another report of this issue.

### ch...@google.com (2025-10-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### aj...@chromium.org (2025-10-23)

Please unrestrict pocs, description and comments.

### sa...@gmail.com (2025-10-23)

hi sorry i have unrestricted it thank you

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/403792431)*
