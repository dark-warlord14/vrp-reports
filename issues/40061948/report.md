# Malicious PowerShell module file can be downloaded without any warning and can be bypassed the Chrome security

| Field | Value |
|-------|-------|
| **Issue ID** | [40061948](https://issues.chromium.org/issues/40061948) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | sm...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2022-11-29 |
| **Bounty** | $500.00 |

## Description

---

### Report description


Malicious PowerShell module file can be downloaded without any warning and can be bypassed the Chrome security


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

According to the documentation of Chromium Code: https://source.chromium.org/chromium/chromium/src/+/main:components/safe_browsing/content/resources/download_file_types.asciipb;l=119?q=ALLOW_ON_USER_GESTURE%20ps1
-------------------------------------------------
# Windows PowerShell files
file_types {
  extension: "ps1"
  uma_value: 43
  ping_setting: FULL_PING
  platform_settings {
    platform: PLATFORM_TYPE_WINDOWS
    danger_level: ALLOW_ON_USER_GESTURE
    auto_open_hint: DISALLOW_AUTO_OPEN
  }
}
file_types {
  extension: "ps1xml"
  uma_value: 44
  ping_setting: FULL_PING
  platform_settings {
    platform: PLATFORM_TYPE_WINDOWS
    danger_level: ALLOW_ON_USER_GESTURE
    auto_open_hint: DISALLOW_AUTO_OPEN
  }
}
file_types {
  extension: "ps2"
  uma_value: 45
  ping_setting: FULL_PING
  platform_settings {
    platform: PLATFORM_TYPE_WINDOWS
    danger_level: ALLOW_ON_USER_GESTURE
    auto_open_hint: DISALLOW_AUTO_OPEN
  }
}
file_types {
  extension: "ps2xml"
  uma_value: 46
  ping_setting: FULL_PING
  platform_settings {
    platform: PLATFORM_TYPE_WINDOWS
    danger_level: ALLOW_ON_USER_GESTURE
    auto_open_hint: DISALLOW_AUTO_OPEN
  }
}
file_types {
  extension: "psc1"
  uma_value: 47
  ping_setting: FULL_PING
  platform_settings {
    platform: PLATFORM_TYPE_WINDOWS
    danger_level: ALLOW_ON_USER_GESTURE
    auto_open_hint: DISALLOW_AUTO_OPEN
  }
}
file_types {
  extension: "psc2"
  uma_value: 48
  ping_setting: FULL_PING
  platform_settings {
    platform: PLATFORM_TYPE_WINDOWS
    danger_level: ALLOW_ON_USER_GESTURE
    auto_open_hint: DISALLOW_AUTO_OPEN
  }
}
-------------------------------------------------
these file types danger_level are ALLOW_ON_USER_GESTURE mode. 
Though, PSM1 is also PowerShell module file which can be functioned by Malware code. PSM1 is not in list of any NOT_DANGEROUS, ALLOW_ON_USER_GESTURE, DANGEROUS section.
Further, it can be bypassed Chrome Security features when the Safe Browsing level is high level.


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Attacking Scenario:
1) According to the Chromium Code, PSM1 is not listed of any  NOT_DANGEROUS, ALLOW_ON_USER_GESTURE, DANGEROUS level. So, if the Chrome browser is up to date or the security level is high, it can be easily download the PSM1 file without any warning or user permission. And this hole attacker may use to invade end user.
2) PS1 file is on ALLOW_ON_USER_GESTURE level, though it only import the module file, which is not so suspicious. 
3) After downloading files (PS1 & PSM1), when target opens the ps1 file the system will be hacked.


---

### The cause


#### What version of Chrome have you found the security issue in?

107.0.5304.122 (Official Build) (64-bit)


#### Is the security issue related to a crash?

No


#### Choose the type of vulnerability

Privilege Escalation 


#### How would you like to be publicly acknowledged for your report?

Online




## Attachments

- [chrome.mp4](attachments/chrome.mp4) (video/mp4, 9.8 MB)

## Timeline

### sm...@gmail.com (2022-11-29)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2022-11-29)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-11-29)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-11-29)

drubery: Can you PTAL? It looks like psm1 should indeed be treated the same as other powershell extensions. I'm triageing this as medium severity based on other download protection bugs, but feel free to adjust accordingly (or close if WAI). Thanks!

Setting FoundIn as 106 since it's the latest extended stable, and it doesn't look like psm1 was ever included before.

[Monorail components: Services>Safebrowsing]

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-30)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sm...@gmail.com (2022-12-02)

Is there any update?

### sm...@gmail.com (2022-12-05)

I also report this to Microsoft for their chromium-based Edge Browser, which has also same issue. Their engineer suggests me to report this issue to Google, because of an upstream issue (Google Chrome). 


### sm...@gmail.com (2022-12-12)

It's almost 2 weeks, I didn't get any response for this issue.
Do you need more additional info? any additional attack scenario as POC?
Or should I approach to disclose this problem?

This is not only Google's issue, but also Microsoft chromium-based Edge browser also got this bug inherently to Google, and that's why they can't fix this from their side. 

So, please at least give some response about this issue. 

Thank you.

### [Deleted User] (2022-12-13)

drubery: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-12-22)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-12-23)

Thanks for the report. It is close to holiday season so please expect a formal response after the new year.

To clarify, this is not a bypass in Chrome security. Adding a file type as ALLOW_ON_USER_GESTURE  doesn't mean a warning will always be shown to user. Safe Browsing check is still performed on these files. If the file is identified as dangerous by Safe Browsing, a warning will still be shown. I agree we should still add psm1 in the download_file_types file, but it's probably a low severity issue.

### sm...@gmail.com (2022-12-24)

I agree with you, but unfortunately safe browsing never detect this file pattern as malicious or dangerous. I have tested 9-10 times, as my POC is just only opening a JPG file, but from intruder side, they can use this for complex malware attack. Even though, I have tested for steganography jpg malware, lnk malware, scr malware by using this simple dropper code with psm1 in safe browsing mode. But, it never could identify as malicious things.

### gi...@appspot.gserviceaccount.com (2023-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/10af36b805ebb169096e3052c4776fb2c1962c52

commit 10af36b805ebb169096e3052c4776fb2c1962c52
Author: Daniel Rubery <drubery@chromium.org>
Date: Tue Jan 03 23:52:39 2023

Add file type policy entry for PSM1

These files are another form of PowerShell file, and should be equivalent
to PS1 and others.

Fixed: 1394328
Change-Id: I91d777064d632f3fb2049e881ded5d73fba493e1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4133728
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1088484}

[modify] https://crrev.com/10af36b805ebb169096e3052c4776fb2c1962c52/components/safe_browsing/content/resources/download_file_types.asciipb
[modify] https://crrev.com/10af36b805ebb169096e3052c4776fb2c1962c52/components/safe_browsing/content/resources/download_file_types_experiment.asciipb
[modify] https://crrev.com/10af36b805ebb169096e3052c4776fb2c1962c52/tools/metrics/histograms/enums.xml


### sm...@gmail.com (2023-01-04)

 Just asking should i get any acknowledgement or bounty for this issue? 

### [Deleted User] (2023-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-04)

[Empty comment from Monorail migration]

### sm...@gmail.com (2023-01-19)

Is there an update regarding reward-topanel?

### am...@chromium.org (2023-01-23)

This is in the queue for evaluation by the VRP Panel at a future panel session. Reward decisions are made in order of security severity, but your issue will be reviewed at a future VRP panel session. Thank you for your patience. 

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-27)

Thank you for this report. While we don't consider this to be a security bug in Chrome's threat model, but more of a change to a security feature, we did want to thank you for this report. As such, we would like to extend to you a $500 VRP reward. Thank you for your efforts and reporting this issue to us!

### sm...@gmail.com (2023-01-27)

Thank You

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1394328?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1394329]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061948)*
