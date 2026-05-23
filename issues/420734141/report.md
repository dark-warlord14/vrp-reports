# Screen Share Dialog - Domain Spoof (Similar to permission prompt)

| Field | Value |
|-------|-------|
| **Issue ID** | [420734141](https://issues.chromium.org/issues/420734141) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>MediaCapture |
| **Platforms** | Windows |
| **Chrome Version** | 138.0.7204.4 (Official Build) canary (64-bit) |
| **CVE IDs** | CVE-2025-11211 |
| **Reporter** | am...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2025-05-28 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Open the vulnerable page in long domain name (possible above 75)
2. click the button to start screenshare
3. you can see the domain name is truncated and diff domain is showed

To reproduce this issue locally we can follow the below steps

1. Add a below entry in hosts file
   127.0.0.1 google.drivelogin.accounts.login.safeoauth.truested.newsafelogin.google.com.finallargedomain.com
2. place the attached files in one folder and start the server by running python3 filename.py
3. Now visit <https://googledrivelogin.accounts.logins.safeoauth.truested.newsafelogins.google.com.finallargedomain.com:4443/poc.html> in latest chrome
4. You can see the popup shows google.com at the end instead of finallargedomain.com

# Problem Description

Note: I have already reported this case but was closed as obsolete without further investigation, i have added details here, kindly check the poc video and this comment <https://issues.chromium.org/issues/420574505#comment4>

Firefox Ref of similar attack in permission prompt: <https://bugzilla.mozilla.org/show_bug.cgi?id=1920423>

I have seen the similar case in chrome too but i wasnt able to get that bug reference

HI Team, Chrome latest on windows is vulnerable for screenshare domain name spoof which allows the attacker to trick the victim to share the screen to malicious site thinking it of as google.com

Tested on windows 11 pro, chrome canary 138.0.7204.4 (Official Build) canary (64-bit)

# Summary

Screen Share Dialog - Domain Spoof (Similar to permission prompt)

# Custom Questions

#### Reporter credit:

Ameen Basha M K

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- [bandicam 2025-05-28 07-56-04-516.mp4](attachments/bandicam 2025-05-28 07-56-04-516.mp4) (video/mp4, 2.1 MB)
- [poc.html](attachments/poc.html) (text/html, 1.9 KB)
- [server.crt](attachments/server.crt) (application/x-x509-ca-cert, 1.0 KB)
- [server.key](attachments/server.key) (application/x-iwork-keynote-sffkey, 1.7 KB)
- [https_server_fileserve.py](attachments/https_server_fileserve.py) (text/x-python, 715 B)

## Timeline

### li...@chromium.org (2025-05-28)

Hello,

My apologies, it was not obvious in the first bug that the problem is that the domain is truncated to exclude the TLD.

This looks like a medium severity to me as a user could reasonably be tricked into sharing their screen with a malicious actor, but a user would still need to go through the permission dialogue to share the screen.

Not 100% certain which component this should go under, assigning to an owner of //content/browser/media/capture for now. Could you PTAL and reassign if necessary?

### am...@gmail.com (2025-05-29)

Thanks for the update i request for severity/priority change l, it have similar impact of permission dialog origin spoof.

I request for severity/priority revisit and opt for a quick fix initiation

### ch...@google.com (2025-05-29)

Setting milestone because of s2 severity.

### ch...@google.com (2025-05-29)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### al...@chromium.org (2025-05-29)

@el...@chromium.org, I think you/your team own the Dialog (or at least are more familiar with it)? Let me know if you disagree and Jordan or I can look into this.

### el...@chromium.org (2025-06-02)

@en...@chromium.org is the authority on the correct behavior here.

### am...@gmail.com (2025-06-17)

Frienfly ping, Do we have any update on this team?

### ch...@google.com (2025-06-17)

engedy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### am...@gmail.com (2025-06-26)

Friendly Reminder: Tewm any update on this case?

### ch...@google.com (2025-07-02)

engedy: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-17)

engedy: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-01)

engedy: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### am...@gmail.com (2025-08-01)

team any update on this issue?

### en...@chromium.org (2025-08-04)

Thanks for the report.

Given that calling `getDisplayMedia` kicks the user out of fullscreen, and then the full origin is correctly displayed in the address, I was initially inclined to classify this as "tamper with trusted browser UI, with extreme mitigating factors (S3)", consistent with the reasoning in <https://issues.chromium.org/issues/40089298#comment3>. However, it looks like the fullscreen logic needs some polish, as it does not cover the case when the site triggers the screen share dialog and then immediately enters fullscreen afterwards. Thus I will consider this mitigating factor to be not *currently* in effect. There are some further mitigating factors, namely: this only affects a single permission type (albeit a sensitive one), and the width and current line wrapping logic in the screen share dialog requires an unnaturally long origin, which somewhat dilutes the effectiveness of spoofing, as the trusted origin gets lost in the noise. All in all, these mitigating factors are relatively weak, so "low end of S2" seems appropriate.

We should apply the same changes as in <https://issues.chromium.org/issues/40095827#comment25> and <https://issues.chromium.org/issues/40095827#comment29>, and probably revisit polishing the fullscreen logic separately. Given the low-S2 severity, I'm tentatively putting down M141 for the fix, but happy if the team wants to consider cherry-picking back to M140.

### en...@chromium.org (2025-08-04)

Given this is specific to the display media chooser dialog, could I pass this bug to you, @al...@chromium.org or @to...@chromium.org? I'm not quite sure how your teams divide ownership, but based on quick chat with Tove, sounds their team might be best positioning to make this change.

### al...@chromium.org (2025-08-04)

For the permission bubble, this would be more @to...@chromium.org; whereas my team is more the actual capturer.

### ch...@google.com (2025-08-29)

tovep: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### to...@chromium.org (2025-08-30)

I have CL in progress to fix this issue: https://crrev.com/c/6845969. Hoping to land it on Monday.

### dx...@google.com (2025-09-01)

Project: chromium/src  

Branch:  main  

Author:  Tove Petersson [tovep@chromium.org](mailto:tovep@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6845969>

Allow line-breaks in long domain names in the screen-sharing dialog

---


Expand for full commit details
```
     
    This change is gated by the DesktopMediaPickerMultiLineTitle feature- 
    flag. 
     
    Bug: 420734141 
    Enabled-by-default-reason: kill-switch 
    Change-Id: Id50de3cd3c03c47d8b2532b7a53b49af55702e44 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6845969 
    Commit-Queue: Tove Petersson <tovep@chromium.org> 
    Reviewed-by: Elad Alon <eladalon@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1509168}

```

---

Files:

- M `chrome/browser/ui/views/desktop_capture/desktop_media_picker_views.cc`
- M `chrome/browser/ui/views/desktop_capture/desktop_media_picker_views.h`
- M `chrome/browser/ui/views/desktop_capture/desktop_media_picker_views_browsertest.cc`

---

Hash: [21bf550775547eac9059dd49d54156432486cb21](https://chromiumdash.appspot.com/commit/21bf550775547eac9059dd49d54156432486cb21)  

Date: Mon Sep 1 13:40:15 2025


---

### dx...@google.com (2025-09-01)

Project: chromium/src  

Branch:  main  

Author:  Tove Petersson [tovep@chromium.org](mailto:tovep@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6905684>

Add fieldtrial config for DesktopMediaPickerMultiLineTitle.

---


Expand for full commit details
```
     
    Bug: 420734141 
    Change-Id: Iff9d4f76b7e9d87430e1a69ebe606d78723c5748 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6905684 
    Reviewed-by: Palak Agarwal <agpalak@chromium.org> 
    Commit-Queue: Tove Petersson <tovep@chromium.org> 
    Reviewed-by: Elad Alon <eladalon@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1509259}

```

---

Files:

- M `testing/variations/fieldtrial_testing_config.json`

---

Hash: [ae6326fa28b6bb38a2c9da18f9ea88845a0356e3](https://chromiumdash.appspot.com/commit/ae6326fa28b6bb38a2c9da18f9ea88845a0356e3)  

Date: Mon Sep 1 17:58:10 2025


---

### dx...@google.com (2025-09-02)

Project: chromium/src  

Branch:  main  

Author:  Tove Petersson [tovep@chromium.org](mailto:tovep@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6905222>

Reject getDisplayMedia calls from domains longer than 255 characters

---


Expand for full commit details
```
     
    This change is gated by the DisplayMediaRejectLongDomains feature-flag. 
     
    Bug: 420734141 
    Change-Id: I6e117c4a4ae27786e2096a0da8bb0cb2e8cf6ae7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6905222 
    Reviewed-by: Elad Alon <eladalon@chromium.org> 
    Commit-Queue: Tove Petersson <tovep@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1509516}

```

---

Files:

- M `chrome/browser/media/webrtc/display_media_access_handler.cc`
- M `chrome/browser/media/webrtc/display_media_access_handler.h`
- M `chrome/browser/media/webrtc/display_media_access_handler_unittest.cc`
- M `testing/variations/fieldtrial_testing_config.json`

---

Hash: [74e314f5f71cc35cc723bbfe940c09d2559a764a](https://chromiumdash.appspot.com/commit/74e314f5f71cc35cc723bbfe940c09d2559a764a)  

Date: Tue Sep 2 13:02:50 2025


---

### en...@chromium.org (2025-09-05)

Thanks for these fixes here!

Drive-by question: in the CL in [#comment20](https://issues.chromium.org/issues/420734141#comment20), you talk about the feature enabled by default with a kill-switch, but it looks like the feature is disabled by default unless enabled through the field trial framework. Could we flip the line wrapping fix specifically to be on by default?

Another question: When/how often do we expect the DesktopMediaPickerDialogView not to have a BubbleFrameView?

### ch...@google.com (2025-09-05)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### to...@chromium.org (2025-09-05)

I originally intended to launch this behind a kill-switch, but due to concerns about other layout ramifications, I instead chose to take a more cautious approach and launch it through a finch experiment. I see now, that I missed to remove a reference to it being a kill-switch in the CL.

From what I can see, DesktopMediaPickerDialogView should always have a BubbleFrameView when opened in the browser, but this is not statically guaranteed, so it needs to be checked. The proper fix here is to update the inheritance for the DesktopMediaPickerDialogView, but that looked like a bigger change, so in the interest to get this fix in with the M141 release, this needs to be done as a follow-up.

### to...@chromium.org (2025-09-05)

1. This is a security issue.
2. https://chromium-review.googlesource.com/c/chromium/src/+/6905222
3. The change has been released on Canary. It has been partially tested in Canary and partially through a local build.
4. It's a UI-change to fix a security issue. The fix is behind a finch flag that is not active in any release channels.
5. N/A
6. No

### ch...@google.com (2025-09-05)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-09-08)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ts...@google.com (2025-09-08)

Approved to merge the experiment to Beta.

### to...@chromium.org (2025-09-09)

Apparently the two first CLs didn't make the branch cut either as I originally thought:

- <https://chromium-review.googlesource.com/c/chromium/src/+/6845969>
- <https://chromium-review.googlesource.com/c/chromium/src/+/6905684>

so I need approval to merge them as well.

### ch...@google.com (2025-09-09)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### to...@chromium.org (2025-09-09)

1. This is a security issue.
2. Changes to be merged:

- <https://chromium-review.googlesource.com/c/chromium/src/+/6845969>
- <https://chromium-review.googlesource.com/c/chromium/src/+/6905684>

3. The change has been released on Canary. It has been partially tested in Canary and partially through a local build.
4. It's a UI-change to fix a security issue. The fix is behind a finch flag that is not active in any release channels.
5. N/A
6. No

### sr...@chromium.org (2025-09-09)

adding awhalley@ and icer@ to review/approve the merge

### aw...@google.com (2025-09-09)

It's tsepez@ and yangsharon@ for merge reviews.

### dx...@google.com (2025-09-10)

Project: chromium/src  

Branch:  refs/branch-heads/7390  

Author:  Tove Petersson [tovep@chromium.org](mailto:tovep@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6930279>

Reject getDisplayMedia calls from domains longer than 255 characters

---


Expand for full commit details
```
     
    This change is gated by the DisplayMediaRejectLongDomains feature-flag. 
     
    (cherry picked from commit 74e314f5f71cc35cc723bbfe940c09d2559a764a) 
     
    Bug: 420734141 
    Change-Id: I6e117c4a4ae27786e2096a0da8bb0cb2e8cf6ae7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6905222 
    Reviewed-by: Elad Alon <eladalon@chromium.org> 
    Commit-Queue: Tove Petersson <tovep@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1509516} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6930279 
    Cr-Commit-Position: refs/branch-heads/7390@{#557} 
    Cr-Branched-From: d481efce5eb300acbb896686676ebd0352a6f1db-refs/heads/main@{#1509326}

```

---

Files:

- M `chrome/browser/media/webrtc/display_media_access_handler.cc`
- M `chrome/browser/media/webrtc/display_media_access_handler.h`
- M `chrome/browser/media/webrtc/display_media_access_handler_unittest.cc`
- M `testing/variations/fieldtrial_testing_config.json`

---

Hash: [45d060dcdf6b6d3099e76ac3aa86e26c00bf7885](https://chromiumdash.appspot.com/commit/45d060dcdf6b6d3099e76ac3aa86e26c00bf7885)  

Date: Wed Sep 10 08:41:28 2025


---

### dx...@google.com (2025-09-10)

Project: chromium/src  

Branch:  main  

Author:  Tove Petersson [tovep@chromium.org](mailto:tovep@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6935148>

Consolidate media picker field trials for long domain names

---


Expand for full commit details
```
     
    This change consolidates the following two features into the 
    DisplayMediaPickerLongDomains study: 
    - DesktopMediaPickerMultiLineTitle 
    - DisplayMediaRejectLongDomains 
     
    Bug: 420734141 
    Change-Id: I836157cb95c5914e2e52e0f68cda2fa867d6da22 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6935148 
    Reviewed-by: Johannes Kron <kron@chromium.org> 
    Commit-Queue: Tove Petersson <tovep@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1513706}

```

---

Files:

- M `testing/variations/fieldtrial_testing_config.json`

---

Hash: [218b397042ce7f3d04f5d6a1992a1eaec69c7a87](https://chromiumdash.appspot.com/commit/218b397042ce7f3d04f5d6a1992a1eaec69c7a87)  

Date: Wed Sep 10 14:56:42 2025


---

### ts...@google.com (2025-09-11)

Approval for the CLs in #32 to merge to M-141 (already has Approved tag so nothing else to set, I think).

### ts...@google.com (2025-09-11)

This is sev-medium, so declining a merge to stable. 

### sp...@google.com (2025-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
mitigated baseline UI spoof


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### to...@chromium.org (2025-09-12)

Looking at these CLs:

- <https://chromium-review.googlesource.com/c/chromium/src/+/6845969>
- <https://chromium-review.googlesource.com/c/chromium/src/+/6905684>

I now see that they already are on the 7390 branch. I was mislead by chromiumdash which reports that their first release was on M142. Anyhow, these CLs don't need to be merged, so I believe we are done here.

Thank you and sorry for the confusion.

### to...@google.com (2025-09-29)

Canary overview metrics (Sep 21-27): <http://uma/p/chrome/variations?sid=084a22eeab3b9cf043406aaafe1be415>

No significant changes except:

- Memory.Gpu.PrivateMemoryFootprint: A significant change to this metric is not expected. The change is not significant for any of the 6 previous 7-day periods and screen-capture usage is generally low on Canary, so this is likely a statistical fluke.

Let's continue the rollout to Beta to gather more data, while keeping an eye on the Memory.Gpu.PrivateMemoryFootprint metric.

### bo...@chromium.org (2025-10-09)

Hey y'all, are we confident the CVE number is assigned correctly? It looks like [another bug](https://issues.chromium.org/issues/441917796) was assigned CVE-2025-11211, but the bugs don't look similar to me.

Edit: You may also want to take a look at the release notes for [141.0.7390.54/55](https://chromereleases.googleblog.com/2025/09/stable-channel-update-for-desktop_30.html) and [141.0.7390.65](https://chromereleases.googleblog.com/2025/10/stable-channel-update-for-desktop.html) to make sure credit attribution is reflected accurately.

### aw...@google.com (2025-10-16)

Mind taking a look icer@?

### to...@chromium.org (2025-10-24)

Beta overview metrics (Oct 15-22): <https://uma.googleplex.com/p/chrome/variations?sid=968eefb9eb0ff5204abc217427cac531>

All significant movements are marked as having insufficient data except:

- Memory.Gpu.PrivateMemoryFootprint: Unlike in Canary, this metric now shows a 30 percent improvement. A significant change to this metric as a result of this change is not expected and is likely a statistical fluke.

Generally screen-sharing is not used enough on Canary and Beta to get sufficient numbers for an analysis. Let’s continue the rollout to stable 1% to gather more data.

### ch...@google.com (2025-12-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### to...@chromium.org (2026-01-07)

1% stable overview metrics (Dec 1-14): <https://uma.googleplex.com/p/chrome/variations?sid=29c8212ac9ee89e67c8fcf8d76a0c32a>

All significant movements looks unrelated to this change and are marked as having insufficient data.

Let’s continue the rollout to 100% stable.

### dx...@google.com (2026-01-08)

Project: chromium/src  

Branch:  main  

Author:  Tove Petersson [tovep@google.com](mailto:tovep@google.com)  

Link:    <https://chromium-review.googlesource.com/7408636>

Enable DesktopMediaPickerMultiLineTitle and DisplayMediaRejectLongDomains

---


Expand for full commit details
```
     
    Additionally, the DisplayMediaRejectLongDomains field trial has been removed. 
     
    Bug: 420734141 
    Change-Id: I6a2f0bc5934c8e7490575e16eb3e21b8029acd85 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7408636 
    Reviewed-by: Johannes Kron <kron@chromium.org> 
    Commit-Queue: Tove Petersson <tovep@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1566223}

```

---

Files:

- M `chrome/browser/media/webrtc/display_media_access_handler.cc`
- M `chrome/browser/ui/views/desktop_capture/desktop_media_picker_views.cc`
- M `testing/variations/fieldtrial_testing_config.json`

---

Hash: [83a37b97567d79bcde3e3b7b257b564c951f1829](https://chromiumdash.appspot.com/commit/83a37b97567d79bcde3e3b7b257b564c951f1829)  

Date: Thu Jan 8 12:55:08 2026


---

### dx...@google.com (2026-01-14)

Project: chromium/src  

Branch:  main  

Author:  Tove Petersson [tovep@google.com](mailto:tovep@google.com)  

Link:    <https://chromium-review.googlesource.com/7460955>

Cleanup DesktopMediaPickerMultiLineTitle, DisplayMediaRejectLongDomains

---


Expand for full commit details
```
     
    These features are now launched and the code is enabled by default. 
     
    Bug: 420734141 
    Change-Id: I80e717b354f8d1b168330f64e787cb60b54307d1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7460955 
    Commit-Queue: Palak Agarwal <agpalak@chromium.org> 
    Reviewed-by: Palak Agarwal <agpalak@chromium.org> 
    Auto-Submit: Tove Petersson <tovep@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1568963}

```

---

Files:

- M `chrome/browser/media/webrtc/display_media_access_handler.cc`
- M `chrome/browser/media/webrtc/display_media_access_handler.h`
- M `chrome/browser/media/webrtc/display_media_access_handler_unittest.cc`
- M `chrome/browser/ui/views/desktop_capture/desktop_media_picker_views.cc`
- M `chrome/browser/ui/views/desktop_capture/desktop_media_picker_views.h`
- M `chrome/browser/ui/views/desktop_capture/desktop_media_picker_views_browsertest.cc`

---

Hash: [d7068a5306f710c71541b8750465eff828a8c62a](https://chromiumdash.appspot.com/commit/d7068a5306f710c71541b8750465eff828a8c62a)  

Date: Wed Jan 14 08:57:00 2026


---

## Bounty Award

> mitigated baseline UI spoof

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/420734141)*
