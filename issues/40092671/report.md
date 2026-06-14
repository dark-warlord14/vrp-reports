# Security: Extensions can continue to temporarily execute code and access file after being uninstalled

| Field | Value |
|-------|-------|
| **Issue ID** | [40092671](https://issues.chromium.org/issues/40092671) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Mac, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2018-10-11 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Once uninstalled, all tabs associated with an extension will be closed. While an extension is still installed, it can open a new tab pointing to about:blank from one of its pages. The new tab will have its origin set to the origin used by the chrome extension page that opened it. Therefore, extension content can be freely included in the new tab.

Once the extension is uninstalled, the original extension page will be closed, but the about:blank page will remain. Extension code running within that tab will continue to run. Although the standard extension API methods fail after the extension has been uninstalled, file access (if it was previously provided) will still be active. This allows the code within the tab to continue to access local files for the duration of the session (or until the tab is closed).

**VERSION**  

Chrome Version: 69.0.3497.100 + stable  

Operating System: Windows 10 Pro, version 1803

**REPRODUCTION CASE**

1. Install the attached extension. Ensure that "Allow access to file URLs" is enabled.
2. Once the extension is installed, it will open a new tab, pointing to a HTML file it contains. JavaScript code included in this file will then use window.open to open a new tab pointing to about:blank. The original page will then update the about:blank page to include about\_page.js from the extension.
3. On the about:blank page, about\_page.js will make an XHR request to file:///C:/ every 4 seconds. It will log the response it receives to the console.
4. The extension should then be uninstalled via the Extensions page. This will close the extension page that was opened in step 2. The about:blank page will not be closed, however. At this point, the standard extension API methods will stop working (though I didn't test all of them, so it's possible some of the bindings might still work). However, if the extension had file access, the about:blank page will continue to have file access. It can then continue to request arbitrary local files until the user closes the browser or closes the tab.

This doesn't work when the user changes the "Allow access to file URLs" setting. Even though the about:blank page won't be closed, it's local file requests will fail.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [temporary_persistence_poc.zip](attachments/temporary_persistence_poc.zip) (application/octet-stream, 2.0 KB)
- [about_page.js](attachments/about_page.js) (text/plain, 356 B)
- [background.js](attachments/background.js) (text/plain, 78 B)
- [extension_page.html](attachments/extension_page.html) (text/plain, 153 B)
- [extension_page.js](attachments/extension_page.js) (text/plain, 393 B)
- [manifest.json](attachments/manifest.json) (text/plain, 374 B)

## Timeline

### wf...@chromium.org (2018-10-11)

files. extracted.

### wf...@chromium.org (2018-10-11)

devlin, can you take a look at this? potentially this would allow a malicious extension to stay resident after it was removed.

[Monorail components: Platform>Extensions]

### rd...@chromium.org (2018-10-11)

I'm not sure that code running after we uninstall/disable the extension is something we can easily prevent.  This case is somewhat trivially fixable, since we could just close any about:blank tab with the extension origin as its effective origin, but it's just about impossible to un-inject content scripts from a page.  I think extension code being able to run until all the tabs have been closed or refreshed is largely unavoidable.

### de...@gmail.com (2018-10-12)

Just being able to run code might not be much of an issue. An extension could open its own web page to do something similar. However, continuing to be able to access files, even after uninstallation, sounds like a problem. When you toggle "Allow access to file URLs", the access is revoked, but it's not revoked upon uninstallation.

### de...@gmail.com (2018-10-12)

There's a related issue that comes up when changing the "Allow access to file URLs" setting - an extension can use a similar technique to retain file access for the duration of the session (or until the tab is closed). The issue has been logged here: https://bugs.chromium.org/p/chromium/issues/detail?id=894812

### sh...@chromium.org (2018-10-12)

[Empty comment from Monorail migration]

### ke...@google.com (2018-11-26)

[Empty comment from Monorail migration]

### ke...@google.com (2018-11-26)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-05-10)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/14025c6109627068bff5193317ecc660fcc37b93

commit 14025c6109627068bff5193317ecc660fcc37b93
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Thu Jun 27 17:56:14 2019

[Extensions] Close opaque-origin windows opened by extensions on extension unload

When an extension is unloaded, we close any tabs that were on the
extension origin to prevent it from running any further. However, an
extension can also open a window with an opaque origin (e.g.,
about:blank) and modify it (e.g. to include a script tag). We should
close these windows on extension unload as well to prevent it from
continuing to run.

Note that it's pretty much fundamentally impossible to truly prevent
continued execution by the extension, such as in the case of content
scripts (there's no such thing as un-injecting a content script), but
it's good to fix this specific case.

See bug for more details.

Bug: 894477
Change-Id: Ie6cdd9b6c05279ca9178e291a4d785ae53f69906
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1589246
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#672971}

[modify] https://crrev.com/14025c6109627068bff5193317ecc660fcc37b93/chrome/browser/extensions/extension_unload_browsertest.cc
[modify] https://crrev.com/14025c6109627068bff5193317ecc660fcc37b93/chrome/browser/ui/browser.cc


### va...@chromium.org (2019-07-16)

Devlin -- it looks like the CL in https://crbug.com/chromium/894477#c11 fixes this bug?
If so, please mark it Fixed.
Otherwise, please add a comment describing what's left to help the triage

-Thanks, Security Marshall

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### me...@chromium.org (2020-01-07)

Pinging Devlin to mark this as fixed (if it is indeed).

### rd...@chromium.org (2020-01-08)

Thanks for the ping!

I think the scenario described here should be fixed, yes.  (Though note again that *truly* stopping *all* execution of extension code is pretty much impossible, due to content scripts)

### sh...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-14)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-30)

Congrats! The Panel decided to award $500 for this report!

### na...@google.com (2020-01-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-13)

I'm going to credit this in the M81 release notes and assign a CVE, as even though the commit in https://crbug.com/chromium/894477#c11 landed in a Chrome version many moons ago, it seems to have taken until now to be certain that this is fixed.

### ad...@chromium.org (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/894477?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092671)*
