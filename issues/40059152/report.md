# Security: Chrome Apps: Possible to read environment variables using suggestedName in chrome.fileSystem.chooseEntry

| Field | Value |
|-------|-------|
| **Issue ID** | [40059152](https://issues.chromium.org/issues/40059152) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Apps>API |
| **Platforms** | Windows |
| **Reporter** | st...@gmail.com |
| **Assignee** | sa...@chromium.org |
| **Created** | 2022-03-20 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

After reading <https://crbug.com/chromium/1247389>, I discovered that a very similar attack can be performed by a Chrome App using `chrome.fileSystem.chooseEntry` [0](https://developer.chrome.com/docs/extensions/reference/fileSystem/#method-chooseEntry) and setting the `suggestedName` to an environment variable name.

The fix should be identical, i.e. blocking `%` in file names.

**VERSION**  

Chrome Version: 102.0.4955.0 + stable  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Install the attached extension
2. Hold Enter for about a second

## Attachments

- [background.js](attachments/background.js) (text/plain, 92 B)
- [foreground.js](attachments/foreground.js) (text/plain, 303 B)
- [index.html](attachments/index.html) (text/plain, 67 B)
- [manifest.json](attachments/manifest.json) (text/plain, 336 B)

## Timeline

### [Deleted User] (2022-03-21)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-03-22)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-03-22)

Similar to https://crbug.com/1247389 but requires the user to install a malicious extension. So setting severity to Low. Repro'd in M98.

[Monorail components: Blink>Storage>FileSystem]

### an...@chromium.org (2022-03-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-22)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-03-22)

Afaik Chrome Apps are Chrome OS only at this point (and this is a Chrome Apps only API), so not sure why this is OS-Windows?

Also that API is not a Blink>Storage>FileSystem thing, not sure if there is a better component, but Platform>Extensions>API seems plausible? per chrome/browser/extensions/api/file_system/OWNERS sammc@ appears to own this feature.

[Monorail components: -Blink>Storage>FileSystem Platform>Extensions>API]

### an...@chromium.org (2022-03-22)

I reproduced this in Windows by installing the PoC as a browser extension using Developer mode. Maybe its not just Windows but rather all desktop platforms. Thanks for updating the Component, mek@.

### an...@chromium.org (2022-03-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-23)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2022-03-23)

The fileSystem API is a platform app API, not an extensions API.  Updating labels accordingly.

[Monorail components: -Platform>Extensions>API Platform>Apps>API]

### gi...@appspot.gserviceaccount.com (2022-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cbbc7f49e6a64389872037c8fca87f1fc3a429db

commit cbbc7f49e6a64389872037c8fca87f1fc3a429db
Author: Sam McNally <sammc@chromium.org>
Date: Tue Mar 29 10:15:21 2022

Filter out % from chrome apps filesystem API name suggestions.

Bug: 1308199
Change-Id: I4c141b722f8cce940dd65b3a35847ce36a0f8d23
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3546144
Reviewed-by: Ben Wells <benwells@chromium.org>
Commit-Queue: Sam McNally <sammc@chromium.org>
Cr-Commit-Position: refs/heads/main@{#986412}

[modify] https://crrev.com/cbbc7f49e6a64389872037c8fca87f1fc3a429db/chrome/browser/extensions/api/file_system/file_system_apitest.cc
[modify] https://crrev.com/cbbc7f49e6a64389872037c8fca87f1fc3a429db/extensions/browser/api/file_system/file_system_api.cc
[add] https://crrev.com/cbbc7f49e6a64389872037c8fca87f1fc3a429db/chrome/test/data/extensions/api_test/file_system/open_existing_suggested_name_filtering/background.js
[add] https://crrev.com/cbbc7f49e6a64389872037c8fca87f1fc3a429db/chrome/test/data/extensions/api_test/file_system/open_existing_suggested_name_filtering/manifest.json
[add] https://crrev.com/cbbc7f49e6a64389872037c8fca87f1fc3a429db/chrome/test/data/extensions/api_test/file_system/open_existing_suggested_name_filtering/test.html
[add] https://crrev.com/cbbc7f49e6a64389872037c8fca87f1fc3a429db/chrome/test/data/extensions/api_test/file_system/open_existing_suggested_name_filtering/test_util.js
[add] https://crrev.com/cbbc7f49e6a64389872037c8fca87f1fc3a429db/chrome/test/data/extensions/api_test/file_system/open_existing_suggested_name_filtering/test.js


### sa...@chromium.org (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-28)

Congratulations, Thomas! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1308199?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1308271]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059152)*
