# Security: Download notification can hide 'Press Esc to exit fullscreen and see download' warning

| Field | Value |
|-------|-------|
| **Issue ID** | [363640098](https://issues.chromium.org/issues/363640098) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | UI>Browser>Bubbles>Download |
| **Platforms** | Mac |
| **Reporter** | al...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2024-09-01 |
| **Bounty** | $500.00 |

## Description

Default notification in fullscreen and download notif is 'Press Esc to exit fullscreen and see download', but in this case after fullscren and file download success notif only 'To exit fullscreen press esc'

VERSION
Chrome Version : Version 128.0.6613.114 (Official Build) (x86_64)
Operating System: macOS Monterey

REPRODUCTION CASE

1. Open file index.html
2. Click Start


Ref :

https://issues.chromium.org/issues/40060572
https://issues.chromium.org/issues/40061921

## Attachments

- [record.mov](attachments/record.mov) (video/quicktime, 6.1 MB)
- [index.html](attachments/index.html) (text/html, 1.6 KB)
- [malicious-script.js](attachments/malicious-script.js) (text/javascript, 644 B)
- [test_windows.mp4](attachments/test_windows.mp4) (video/mp4, 4.5 MB)

## Timeline

### ad...@google.com (2024-09-02)

I reproduced this in Chrome 128 on OS X - even though a download is initated, we don't see any mention of Download in the full screen message and there's no visible evidence of a download happening at all.

The logic is [here](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/exclusive_access/exclusive_access_bubble_type.cc;l=48?q=IDS_FULLSCREEN_PRESS_TO_SEE_DOWNLOADS_AND_EXIT&start=11).

xinghuilu@, could I have your opinion here? To me, showing "To exit fullscreen press esc" seems nearly as good as "Press Esc to exit fullscreen and see download" in terms of avoiding spoofing, but I agree it's not quite as good, so I'm provisionally rating this as a S3 security bug. However if those messages are just best-efforts, and it's not considered security-relevant to indicate to the user that a download is occuring, feel free to WontFix this.

### al...@gmail.com (2024-09-02)

hii

but im testing in windows 11 notif  as "Press Esc to exit fullscreen and see download"  
why this different ?

i think to fix same case notif in windows to prevent spoofing

Thanks

### pe...@google.com (2024-09-02)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### xi...@chromium.org (2024-09-03)

We have historically considered similar bugs (<https://crbug.com/40061921>) as a security bug. However, this one is less severe because it only misses the download part. Users can still follow "Press Esc" to exit fullscreen, so I'll keep it as S3.

This is only reproducible on Mac. I'll take another look some time later this week.

### al...@gmail.com (2024-09-17)

after changing weeks
any update ?

Thanks

### al...@gmail.com (2024-10-02)

after changing month
any update ?

Thanks

### al...@gmail.com (2024-11-01)

after changing month
any update ?

Thanks

### ch...@chromium.org (2024-11-26)

I can take a look sometime...

This is content fullscreen aka HTML fullscreen, which is a different code path that's probably buggy.

### ap...@google.com (2025-01-10)

Project: chromium/src  

Branch: main  

Author: Lily Chen <[chlily@chromium.org](mailto:chlily@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6161794>

Fix logic for ExclusiveAccessBubble download notification override

---


Expand for full commit details
```
Fix logic for ExclusiveAccessBubble download notification override 
 
This modifies the logic for determining whether to show an "override" 
notification for an ExclusiveAccessBubble update where there is a 
download involved. This fixes a scenario that occurs a race between two 
calls to ExclusiveAccessBubbleViews::Update(), where one call is for 
a download in fullscreen mode, and another call is the notification for 
entering the fullscreen itself. If the fullscreen notification comes 
first and the download notification comes second, the current code works 
fine and the second Update() overrides the bubble with the correct 
text for notify_overridden. However, it is evidently possible for the 
download notification to come first, followed by the notification for 
entering fullscreen mode. This CL fixes the logic in that case, so that 
we also display the notify_overridden text if this ordering occurs. 
 
Bug: 363640098 
Change-Id: Ibb9d6ddc3875e9ff77566af22f6d20f39e36e1e1 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6161794 
Commit-Queue: Lily Chen <chlily@chromium.org> 
Reviewed-by: Mike Wasserman <msw@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1404936}

```

---

Files:

- M `chrome/browser/ui/views/exclusive_access_bubble_views.cc`
- M `chrome/browser/ui/views/exclusive_access_bubble_views_unittest.cc`

---

Hash: 0c8740fe00e049887087558ff326da6621865054  

Date:  Fri Jan 10 11:59:47 2025


---

### pe...@google.com (2025-01-14)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pe...@google.com (2025-01-14)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### al...@gmail.com (2025-01-22)

After fixed
Any update bounty or CVE ?

Thanks

### sp...@google.com (2025-01-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Thank you reward for report that resulted in a beneficial, informational change for Chrome users. 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-29)

Thank you for the report. This is an issue with very low potential for user harm, in that it strictly hides the filename being downloaded from the user and obfuscates a file is being downloaded. Based on this report, however, we were able to make a change that keeps users better informed and makes it apparent a file is being downloaded; therefore we did want to acknowledge and thank you for that.

### ch...@google.com (2025-04-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/363640098)*
