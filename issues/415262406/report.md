# Intersection Observer v2 API fails to reliably determine target's visibility, which enables clickjacking against Google One Tap

| Field | Value |
|-------|-------|
| **Issue ID** | [415262406](https://issues.chromium.org/issues/415262406) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Geometry |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@icloud.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2025-05-03 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

1. Sign in to your Google account
2. Go to <https://lbstyle.github.io/sandbox.html>
3. Tap the cat as fast as possible multiple times
4. Your email should appear on the website

# Problem Description

This is similar to [issue 333708039](https://issues.chromium.org/issues/333708039)

# Summary

Stealing emails via FedCM clickjacking in Chrome Android

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- [testcase.html](attachments/testcase.html) (text/html, 1.9 KB)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 795.2 KB)
- [testcase.html](attachments/testcase.html) (text/html, 1.9 KB)
- [screen-20250626-205457.mp4](attachments/screen-20250626-205457.mp4) (video/mp4, 3.3 MB)

## Timeline

### ch...@gmail.com (2025-05-05)

Please change the bug's title : 

Stealing emails via Google One Tap clickjacking in Chrome Android

### yi...@chromium.org (2025-05-05)

This is actually not FedCM. Adding SiwG folks to take a look.

### yi...@chromium.org (2025-05-05)

hi Nick, does the SiwG page have any input protector to avoid such clickjacking? 

### dc...@chromium.org (2025-05-05)

Sorry, I was still trying to triage this bug. I actually haven't been able to reproduce this yet, but I don't know if this is because other issues with Clank: when I try clicking the cat in the repro link, I end up getting a tab that doesn't render at all.

### ch...@gmail.com (2025-05-05)

Please use this testcase.html

### ch...@gmail.com (2025-05-05)

(Tested in Google Pixel 7 Pro)

### dc...@chromium.org (2025-05-06)

OK I was able to reproduce after fiddling around a bit. I am going to leave this as medium severity since it does have a fairly visible side effect.

I'm going to tentatively tag this with mobile and desktop OSes; while the PoC is certainly mobile-specific, and the PoC is easier to execute on Android due to the constrained window sizes, there's no instrinsic reason this is impossible on desktop.

### ch...@google.com (2025-05-06)

Setting milestone because of s2 severity.

### ch...@google.com (2025-05-06)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### np...@google.com (2025-05-06)

Do we have input protection on Android? I couldn't reproduce spam tapping with FedCM API but I'm not aware of anything we do ourselves, so maybe just BottomSheet itself has it? Or why doesn't it work with FedCM?

### yi...@chromium.org (2025-05-06)

We have the input protection on the FedCM UI: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/android/webid/internal/java/src/org/chromium/chrome/browser/ui/android/webid/AccountSelectionMediator.java?q=symbol%3A%5Cborg.chromium.chrome.browser.ui.android.webid.AccountSelectionMediator.shouldInputBeProcessed%5Cb%20case%3Ayes

### gu...@google.com (2025-05-06)

From the video at #1, it seems a popup was opened (and the 'Confirm' button on that page was clicked).
Reassigned to Amiel to check why the frozen period doesn't work for the 'Confirm' button.

### np...@google.com (2025-05-06)

Ah I forgot my own code :')

### np...@google.com (2025-05-06)

Given the above, I just want to note this is not a Chromium security issue. So unfortunately I don't think it would qualify for the chromium bounty

### am...@google.com (2025-05-07)

We currently don't have a frozen period for the Confirmation popup. We could add a similar 700ms freeze period (which we have for the One Tap dialog) where we ignore clicks to the Confirm button. This would give the chance for the user to register the context change and hopefully stop clicking.

Would this fix be enough for this issue?

### ch...@gmail.com (2025-05-07)

Could you please clarify why this doesn't qualify as a Chromium security issue? I'd like to understand the reasoning. Thanks.

### np...@google.com (2025-05-07)

To clarify, I'm not in the security team nor handle the bounty program. But this is not a Chromium security issue since the clickjacking occurs on a script-created dialog, not a browser-created dialog. The fix needs to come from that script, and it is not a browser issue.

### ch...@gmail.com (2025-05-13)

Any update on this bug? - Thanks

### am...@google.com (2025-05-14)

I'm holding on the fix until the proposed fix is determined to be enough for the issue

### am...@google.com (2025-05-22)

I'll implement the proposed fix

### ch...@gmail.com (2025-05-22)

Since this is not considered a Chromium security issue and the root cause lies in a script-created dialog, I understand it's outside the scope of the browser's responsibility.

Just to confirm — has this issue been reported to issuetracker.google.com, given that it's not a Chrome bug but may still fall under another relevant Google product?

### am...@google.com (2025-05-30)

Our product's team, Google Identity Service, is already working on the issue.

### ch...@google.com (2025-06-14)

amielreveche: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### am...@google.com (2025-06-20)

The fix has been submitted and should be in production by end of next week.

A 700ms is added before any clicks can be process on the confirm button to allow the context change to register to the user.

### ch...@google.com (2025-06-20)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### np...@google.com (2025-06-23)

Added the hotlist since this is a non-Chrome security issue so there is no Chrome change associated with the fix.

### ch...@gmail.com (2025-06-26)

Fixed.

### am...@chromium.org (2025-06-30)

This was reopened since `fixed by code changes` field was not updated. Since this is not resolved by a Chromium code change, I've updated the field as NA.

We have no way to pass issues from our component to the Google VRP for evaluation. I'm assigning this to the WOOPS team for their evaluation and to determine if / how they would like to consider this issue for a reward.

### am...@chromium.org (2025-06-30)

also cc'ing straka@ from Google VRP; Martin, please LMK if I need to include anyone else on here for Google VRP evaluation

### am...@google.com (2025-06-30)

thanks to the marvels of being added to the correct ACLs, I can now send this over to the Google VRP component.

### sp...@google.com (2025-06-30)

*NOTE: This is an automatically generated email*

Hi! Many thanks for sharing your report.

This email confirms we've received your message. We'll investigate the issue you've reported and get back to you once we have an update. In the meantime, you might want to take a look at the [list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Also, if you have not already done so, create a profile on [the Google Bughunters site](https://bughunters.google.com/) if you'd like us to publicly recognize your contribution:

- [Leaderboard](https://bughunters.google.com/leaderboard) – You'll be added here if we issue a reward for your report.
- [Honorable Mentions](https://bughunters.google.com/leaderboard/honorable-mentions) – You'll be added here if you are not in the Hall of Fame, but we file a security vulnerability bug based on your report.

**Note that we only act on reports concerning vulnerabilities or technical security problems in one of our products. This is not the correct channel if you need to resolve a problem with your account, or want to report non-security bugs or suggest a new product feature.**

Cheers,   

Google Security Bot

[Follow us](https://twitter.com/googlevrp) on Twitter!

### im...@google.com (2025-07-01)

Thank you, I forwarded this report to the Google VRP reward panel. They will review it to see whether it is eligible for a reward. This usually takes a couple of weeks, please be patient.

Thank you,  

The Google Bug Hunters team

### sp...@google.com (2025-07-01)

*NOTE: This is an automatically generated email*

Hey,

We just want to let you know that your report was **triaged** and we're currently looking into it.

You should receive further information in a couple of days, but it might take up to a week if we're particularly busy. In the meantime, you might want to take a look at [the list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Thanks,   

Google Security Bot

### mo...@google.com (2025-07-15)

The Google VRP panel would not like to reward this, as it looks like there's a browser level mitigation being developed at <https://crbug.com/40063020>. Back to Chrome VRP to decide on marking this as duplicate of that tracking bug.

### am...@chromium.org (2025-07-15)

Restricting this for now since it was put back in the Chromium tracker as a "customer issue" and derestricted.

### am...@chromium.org (2025-07-15)

in reference to c#35; this cannot be considered a duplicate of an active, unresolved issue from 2023. While technically I could see the logic of this being considered as a duplicate, given the higher level report and attempt at a broader mitigation conveyed in that report. That attempt at a broader mitigation remains unresolved with no ETA. It also seems potentially not possible given the continued feature development of other Chrome features resulting in new windows / dialogs with potential security UI surfaces.

Regardless of the future *potential* outcome of [crbug.com/40063020](https://crbug.com/40063020), this issue presented in this particular report is related to an issue in Google Identity Service and was resolved by a code change therein. Therefore, this cannot be considered a duplicate report of [crbug.com/40063020](https://crbug.com/40063020).

I've opened a discussion with Google VRP to better understand the discussion and outcome.

### ch...@gmail.com (2025-07-15)

Thank you for the update regarding my report. I saw that it's being considered for duplication with the issue tracked at https://crbug.com/40063020, and that a browser-level mitigation is being developed.

Could you please clarify why this would make the issue ineligible for a reward? I’d appreciate a bit more context to better understand how this fits within the VRP's reward policy.

### am...@chromium.org (2025-07-15)

re c#38, the Google VRP team has routed this issue back to Chrome, so there is no one on this report that can answer your question. As mentioned in c#37, I have reached out to Google VRP to understand why they do not consider this eligible for a VRP reward.

Since this vulnerability is in Google Identity Services and not Chrome Browser, this seems better scoped to Google VRP, in our opinion. I will update this issue with the outcome of those discussions once they are completed.

### am...@chromium.org (2025-07-23)

To follow up on c#39, as previously discussed this issue was not related to browser code and would only be potentially eligible for Google VRP, given that the issue was introduced and resolved in Google Identity Services.

The Google VRP declines to reward this with the following rationale, "It's a dupe of a bug we closed as infeasible 6 years ago." We could route this issue back to them but it would simply be closed as infeasible and as a duplicate of a previous issue. As a action button that does not have a delay at page load is not something that will be corrected in all Google apps and does not meet their bar for Google VRP reward.

### ch...@google.com (2025-10-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/415262406)*
