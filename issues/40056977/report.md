# oob in function  StartupPagesHandler::HandleEditStartupPage

| Field | Value |
|-------|-------|
| **Issue ID** | [40056977](https://issues.chromium.org/issues/40056977) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Settings |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2021-08-23 |
| **Bounty** | $6,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36

Steps to reproduce the problem:
1.this is simmilar as https://crbug.com/chromium/1242392
2.the fucntion check the index, but somethin wrong here 
3.```
if (index < 0 || index > startup_custom_pages_table_model_.RowCount()) {
reject()
}
```

if the index == startup_custom_pages_table_model_.RowCount()

if will cause oob in the code

```
if (settings_utils::FixupAndValidateStartupPage(url_string, &fixed_url)) {
    std::vector<GURL> urls = startup_custom_pages_table_model_.GetURLs();
    urls[index] = fixed_url;
```

the urls will cause oob.

What is the expected behavior?

What went wrong?
above all.

Did this work before? N/A 

Chrome version: 92.0.4515.159  Channel: stable
OS Version: 10.0

## Attachments

- [poc.png](attachments/poc.png) (image/png, 49.1 KB)
- [overflow.txt](attachments/overflow.txt) (text/plain, 15.8 KB)
- [0001-fix-heap-bufferoverflow-in-startup_page_handler.patch](attachments/0001-fix-heap-bufferoverflow-in-startup_page_handler.patch) (text/plain, 1.1 KB)

## Timeline

### wx...@gmail.com (2021-08-23)

the fix is easy 
```
index < 0 || index >= startup_custom_pages_table_model_.RowCount()
```

### [Deleted User] (2021-08-23)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-08-23)

Do you need poc to prove it? I think the bug is so obvious

### wx...@gmail.com (2021-08-24)

here is the asan output and my small patch to print, and my poc

```
  arr2 = ["test", 1, "http://www.google.com"];
  chrome.send("editStartupPage", arr2);
```

you should have one startup page. I will continue to test the function HandleAddStartupPage so that we can just excute js to crash without startup page.

### wx...@gmail.com (2021-08-24)

the step is
-  open "chrome://setting"
-  set a startup page
- inspect the window, and excute my js.
the it will crash.


### wx...@gmail.com (2021-08-25)

here is the patch 

### dr...@chromium.org (2021-08-25)

This reproduces as claimed. Again, there's the high burden of chaining this with another bug that injects JS to chrome://settings, so assigning medium severity.

I don't see more specific owners for this handler, so triaging to a general chrome/browser/resources/settings/ owner. dpapad@, khorimoto@ - can you take a look?

[Monorail components: UI>Settings]

### [Deleted User] (2021-08-25)

[Empty comment from Monorail migration]

### kh...@chromium.org (2021-08-25)

Re-assigning to dpapad@ since this is browser settings, not OS settings.

### [Deleted User] (2021-08-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dp...@chromium.org (2021-09-01)

Candidate fix at https://chromium-review.googlesource.com/c/chromium/src/+/3137314 (same as the one proposed at https://crbug.com/chromium/1242404#c6).

### wx...@gmail.com (2021-09-01)

Please also check the https://crbug.com/chromium/1242423

### gi...@appspot.gserviceaccount.com (2021-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f59d2d874a6f757bf8c8c3297b39852b71ca701a

commit f59d2d874a6f757bf8c8c3297b39852b71ca701a
Author: dpapad <dpapad@chromium.org>
Date: Thu Sep 02 07:07:58 2021

Settings: Fix incorrect out of bounds check in StartupPagesHandler.

Fixed: 1242404
Change-Id: I7fb2c4ea8b7cbb48cbd2457ee25721db4c991b28
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3137314
Auto-Submit: dpapad <dpapad@chromium.org>
Reviewed-by: John Lee <johntlee@chromium.org>
Commit-Queue: dpapad <dpapad@chromium.org>
Cr-Commit-Position: refs/heads/main@{#917564}

[modify] https://crrev.com/f59d2d874a6f757bf8c8c3297b39852b71ca701a/chrome/browser/ui/webui/settings/settings_startup_pages_handler.cc


### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-08)

Congratulations on another one! The VRP Panel has decided to award you $6,000 for this report. Nice work! 

### wx...@gmail.com (2021-09-08)

Still waiting fro you in next bug :)

### wx...@gmail.com (2021-09-09)

would you like to consider to add the bug bounty and set the Security_Severiy to High? I think If someone have a UXSS bug in chrome://setting, it will use the uxss to execute js to get RCE without user's  interaction.

### am...@chromium.org (2021-09-09)

We discussed this report fairly thoroughly already during today's panel; given that this requires chaining another vulnerability (only which is theoretically being presented here) to inject and execute the js code to trigger this vulnerability, the severity and reward amount were deemed adequate for this report. Thank you. 

### wx...@gmail.com (2021-09-09)

thank you for your reply:)

### am...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-09-10)

from the https://crbug.com/chromium/1201031, it seems that it also need to visit a specific url and navigate to it, open devtools to inject js. but its Severity is High, and the rewatd is higher than me....


### am...@chromium.org (2021-09-10)

hello, yes https://crbug.com/chromium/1201031 did obtain a higher reward; that issue contained two separate reports for two individual vulnerabilities that resulted in UAFs in the browser process. Each report was of very high quality and contained a symbolized stack stack trace for each and excellent analysis which allowed the developers to quickly identify and address the root cause for each. Thanks. 

### wx...@gmail.com (2021-09-10)

Thanks :P

### wx...@gmail.com (2021-09-17)

hello, developer, could you look at the https://crbug.com/chromium/1242423?

### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-22)

[Empty comment from Monorail migration]

### gi...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/73f05938f913cdd42142bc0bf2fe355b6d0e439e

commit 73f05938f913cdd42142bc0bf2fe355b6d0e439e
Author: dpapad <dpapad@chromium.org>
Date: Tue Oct 26 13:49:04 2021

[M90-LTS] Settings: Fix incorrect out of bounds check in StartupPagesHandler.

M90 merge notes:
  Minor conflict because callback_id is a pointer in M90

(cherry picked from commit f59d2d874a6f757bf8c8c3297b39852b71ca701a)

Fixed: 1242404
Change-Id: I7fb2c4ea8b7cbb48cbd2457ee25721db4c991b28
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3137314
Auto-Submit: dpapad <dpapad@chromium.org>
Commit-Queue: dpapad <dpapad@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917564}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3237367
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1648}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/73f05938f913cdd42142bc0bf2fe355b6d0e439e/chrome/browser/ui/webui/settings/settings_startup_pages_handler.cc


### rz...@google.com (2021-10-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1242404?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056977)*
