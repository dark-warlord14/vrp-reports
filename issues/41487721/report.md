# Security: Spoofing request source of Apple mobile configuration profile downloads by UI impersonation

| Field | Value |
|-------|-------|
| **Issue ID** | [41487721](https://issues.chromium.org/issues/41487721) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | ni...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2024-01-02 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

When receiving a response with a MIME type of "application/x-apple-aspen-config", Chromium for iOS shows a confirmation dialog to ask whether to download the iOS configuration profile, and after that, opens SFSafariViewController.  

<https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/download/model/safari_download_tab_helper.mm;l=14>

This process can be invoked from an inactive tab in the background, and the confirmation dialog doesn't show the caller's origin, so it can impersonate as if the active tab in the foreground is asking to download the iOS configuration profile.

**VERSION**  

Chrome Version: 120.0.6099.119 stable  

Operating System: iOS 17.1.2

**REPRODUCTION CASE**  

The following URL is a page to reproduce the spoofing.  

<https://csrf.jp/2024/mobileconfig/>

This page opens "google.com" in a new window, and a few seconds later, this page itself moves to the other URL that returns MIME type of "application/x-apple-aspen-config".  

At this time, Chromium shows a confirmation dialog on the window of "google.com", not on the attacker's window.  

If the user is tricked into believing that the request is from Google and presses the "Continue" button, a configuration profile download process is initiated on the SFSafariViewController.

**CREDIT INFORMATION**  

Reporter credit: Muneaki Nishimura (nishimunea)

## Attachments

- [chromium-ios-mobileconfig-download-ui-spoofing.gif](attachments/chromium-ios-mobileconfig-download-ui-spoofing.gif) (image/gif, 423.0 KB)
- [current.png](attachments/current.png) (image/png, 522.1 KB)
- [proposed-fix.png](attachments/proposed-fix.png) (image/png, 519.9 KB)
- [LongURL.png](attachments/LongURL.png) (image/png, 1.8 MB)

## Timeline

### [Deleted User] (2024-01-02)

[Empty comment from Monorail migration]

### ph...@chromium.org (2024-01-03)

I can reproduce this bug.  Not sure whether the issue is 

[Monorail components: Mobile>iOSWeb>Security]

### ph...@chromium.org (2024-01-03)

ajuma@: Could you help triage this bug to a right owner please?

### [Deleted User] (2024-01-03)

[Empty comment from Monorail migration]

### aj...@chromium.org (2024-01-03)

I think we should include the origin in the prompt (so instead of "This website is...", we'd say "example.com is...") and also restrict profile downloads to https URLs (or else we can't be confident that the origin we are showing in the prompt is the real source of the profile).

Gauthier, wdyt?

### [Deleted User] (2024-01-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2024-01-04)

Chatted with Gauthier and decided that including the origin makes sense, but that we should check with UXW as well.

### aj...@chromium.org (2024-01-05)

Here are screenshots of the current prompt and the proposed one that includes the origin.

### aj...@chromium.org (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### aj...@chromium.org (2024-01-09)

[Empty comment from Monorail migration]

### ga...@chromium.org (2024-01-15)

What would it look like if the site has a very long name?

### aj...@chromium.org (2024-01-15)

The dialog becomes scrollable, as in this screenshot.

### im...@google.com (2024-01-16)

I think we should include what happens when the configuration profile is downloaded.  Also, in the case when the name is very long we should truncate the name so the user doesn't have a super long scroll.

### aj...@chromium.org (2024-01-16)

How about

"example.com is trying to download a configuration profile. A configuration profile can modify your {iPhone, iPad}'s settings."

Also, instead of truncating, maybe we should disallow cases of very long host names (e.g., greater than 50 characters), to avoid tricking the user. As an extreme example, we wouldn't want to truncate "googleisnottheownerofthissitewithaverylongname.com" to "google...", so it might be better to not offer this feature when the host name is that long.

### im...@google.com (2024-01-16)

Your suggestion works.  One small note, we can use "device settings" if the string can't be dynamic.
"example.com is trying to download a configuration profile. A configuration profile can modify your {iPhone, iPad}'s settings."

Can we just truncate at 50 characters instead of disallowing if over 50 characters?



### aj...@google.com (2024-01-16)

Thanks! 

I’m worried that truncation will lead to spoofing bugs. If we truncate the host at X characters, we’ll get bugs where an attacker registers a longer domain so that the first X characters look the same as a legitimate host. 

### im...@google.com (2024-01-17)

thanks for the added context on why truncating isn't the the best solution. If we disallow after 50 characters, does that mean the file will download without notifying the user? If so, we should go with your initial option of the long scroll. It's not ideal but better than not notifying the user and hopefully will be an edge case.

### ga...@chromium.org (2024-01-17)

I am not sure it is really useful to add explanation about what the profile is doing (either the person know what they are doing and it is clear, or they don't and we would need a much bigger explanation). For me "A configuration profile can modify your {iPhone, iPad}'s settings." is not super clear (but that's only my opinion).

For the website name, I think we should go with the full website name, but putting it last (so the user has a chance to read the prompt before being potentially overwhelmed by a very long name).

### gi...@appspot.gserviceaccount.com (2024-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f4eba56a3a691798d1114425ce9b10171e57c05e

commit f4eba56a3a691798d1114425ce9b10171e57c05e
Author: Ali Juma <ajuma@chromium.org>
Date: Tue Jan 23 23:45:20 2024

[iOS] Add host to prompt for downloading mobileconfig files

This adds the host name to the prompt that is shown before
downloading a mobileconfig file, and restricts this feature to URLs
that are either secure or local, since otherwise the host name
found in the URL cannot be trusted.

Change-Id: I5d85509bf15746db907f1e249c791479e6cb1b3e
Bug: 1515169
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5214169
Reviewed-by: Gauthier Ambard <gambard@chromium.org>
Commit-Queue: Ali Juma <ajuma@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1251131}

[modify] https://crrev.com/f4eba56a3a691798d1114425ce9b10171e57c05e/ios/chrome/app/strings/ios_strings_grd/IDS_IOS_DOWNLOAD_MOBILECONFIG_FILE_WARNING_MESSAGE.png.sha1
[modify] https://crrev.com/f4eba56a3a691798d1114425ce9b10171e57c05e/ios/chrome/app/strings/ios_strings.grd
[modify] https://crrev.com/f4eba56a3a691798d1114425ce9b10171e57c05e/ios/chrome/browser/ui/download/safari_download_coordinator_unittest.mm
[modify] https://crrev.com/f4eba56a3a691798d1114425ce9b10171e57c05e/ios/chrome/browser/ui/download/safari_download_coordinator.mm
[modify] https://crrev.com/f4eba56a3a691798d1114425ce9b10171e57c05e/ios/chrome/browser/download/model/browser_download_service.mm


### aj...@chromium.org (2024-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations! The Chrome VRP Panel has decided to award you $2,000 for this report of a security UI spoof. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1515169?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-18)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-18)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

### pe...@google.com (2024-05-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41487721)*
