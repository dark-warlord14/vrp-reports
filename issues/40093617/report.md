# Security: Extensions can add host permissions for chrome:// pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40093617](https://issues.chromium.org/issues/40093617) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2019-01-02 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

chrome.permissions.request allows an extension to request additional permissions at run time. An extension can use this function to silently add host permissions for chrome:// pages. This process is silent because chrome:// hosts are specifically filtered out when generating the list of permission warning messages to show the user.

**VERSION**  

Chrome Version: Tested on 71.0.3578.98 (stable) and 73.0.3658.0 (canary)  

Operating System: Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. Install the attached extension.
2. Once installed, the extension will open a new tab pointing to a HTML file it contains (extension\_page.html).
3. This page will request additional permissions. To do that, it needs a user gesture. Therefore, you'll need to click the page.
4. Once clicked, the page will run the following command to request host permissions for the chrome://settings page:

chrome.permissions.request({permissions: [], origins: ["chrome://settings/\*"]});

This process will complete silently and the host permission will be granted. The page will print the updated set of permissions to the console, allowing you to verify that the permission has been added.

Ultimately, there doesn't seem to be too much you can do with host permissions for a chrome:// page. Having the permission means that you can appear to bypass some of the checks that are present for chrome:// pages. For example, making an XHR request for a chrome:// page typically fails with the following message:

Not allowed to load local resource: chrome://settings/

However, if you add the host permission using the steps above, that message will no longer be displayed, though the request will still fail (possibly because it's blocked on the browser side).

The chrome.cookies API will allow you to call its methods for a chrome:// page, provided you have the host permission, but chrome:// pages don't allow cookies, so it's not particularly useful.

Also, as a side note, it's not possible to remove chrome:// host permissions on the extension's details page - clicking the remove link does nothing and results in the following error being logged to the console:

Uncaught (in promise) Invalid host.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 78 B)
- [extension_page.html](attachments/extension_page.html) (text/plain, 134 B)
- [main.js](attachments/main.js) (text/plain, 357 B)
- [manifest.json](attachments/manifest.json) (text/plain, 374 B)

## Timeline

### de...@gmail.com (2019-01-02)

Relevant code:

The implementation for chrome.permissions.request can be found at:

https://cs.chromium.org/chromium/src/chrome/browser/extensions/api/permissions/permissions_api.cc?l=192&rcl=dd074fc80d030e65135ef39ea2e38fce0ee03458

There's a check within that function to see whether the permissions an extension is requesting appear in the manifest:

https://cs.chromium.org/chromium/src/chrome/browser/extensions/api/permissions/permissions_api.cc?l=223&rcl=dd074fc80d030e65135ef39ea2e38fce0ee03458

That check will pass, provided that an extension has the <all_urls> permission listed under permissions or optional_permissions. This is necessary, as you can't list chrome:// hosts in the manifest.json file. <all_urls> will match any host, though, including a chrome:// host.

Further down, the function checks whether there are any warning messages that need to be shown:

https://cs.chromium.org/chromium/src/chrome/browser/extensions/api/permissions/permissions_api.cc?l=297&rcl=dd074fc80d030e65135ef39ea2e38fce0ee03458

Internally, the GetAllPermissionIDs function filters out all hosts that use the chrome:// scheme:

https://cs.chromium.org/chromium/src/chrome/common/extensions/chrome_extensions_client.cc?l=136&rcl=060de2f58575d9fce493b91742dcb769e16728b0

This means that GetPermissionMessages won't return anything and the permission will be silently granted.

### ts...@chromium.org (2019-01-02)

Thanks for the report. Setting severity medium as this could make for a good intermediate step in a chain of exploits, though one could argue for severity low.

[Monorail components: Platform>Extensions UI>Browser>WebUI]

### sh...@chromium.org (2019-01-03)

[Empty comment from Monorail migration]

### dp...@chromium.org (2019-01-03)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-01-04)

Great find!  It's hard to say if this is medium or low, but it's definitely a security bug, and definitely something we should fix.  I'll have a CL up and hopefully land it today.

[Monorail components: -UI>Browser>WebUI]

### rd...@chromium.org (2019-01-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2019-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e13eb21898c7eba584f680e3d17ca1b9e28bc505

commit e13eb21898c7eba584f680e3d17ca1b9e28bc505
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Thu Jan 10 01:33:45 2019

[Extensions] Have URLPattern::Contains() properly check schemes

Have URLPattern::Contains() properly check the schemes of the patterns
when evaluating if one pattern contains another. This is important in
order to prevent extensions from requesting chrome:-scheme permissions
via the permissions API when <all_urls> is specified as an optional
permission.

Bug: 859600,918470

Change-Id: If04d945ad0c939e84a80d83502c0f84b6ef0923d
Reviewed-on: https://chromium-review.googlesource.com/c/1396561
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#621410}
[modify] https://crrev.com/e13eb21898c7eba584f680e3d17ca1b9e28bc505/chrome/browser/extensions/api/permissions/permissions_api_helpers.cc
[modify] https://crrev.com/e13eb21898c7eba584f680e3d17ca1b9e28bc505/chrome/browser/extensions/api/permissions/permissions_api_helpers_unittest.cc
[modify] https://crrev.com/e13eb21898c7eba584f680e3d17ca1b9e28bc505/chrome/browser/extensions/api/permissions/permissions_api_unittest.cc
[modify] https://crrev.com/e13eb21898c7eba584f680e3d17ca1b9e28bc505/chrome/browser/extensions/permissions_updater_unittest.cc
[modify] https://crrev.com/e13eb21898c7eba584f680e3d17ca1b9e28bc505/extensions/common/permissions/permissions_data.cc
[modify] https://crrev.com/e13eb21898c7eba584f680e3d17ca1b9e28bc505/extensions/common/url_pattern.cc
[modify] https://crrev.com/e13eb21898c7eba584f680e3d17ca1b9e28bc505/extensions/common/url_pattern_unittest.cc


### rd...@chromium.org (2019-01-10)

This should be fixed with #7.  If all looks good on Monday, I'll request a merge back to 72 (71 is unlikely at this stage).

### rd...@chromium.org (2019-01-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-14)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-01-14)

All seems smooth.  Requesting merge to 72 so it goes out with the next release (I don't think this is severe enough to warrant a merge to 71 at this late stage).

### sh...@chromium.org (2019-01-14)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-01-15)

branch:3626

### bu...@chromium.org (2019-01-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3af68a868964ba47382b07d4848376e9a5735079

commit 3af68a868964ba47382b07d4848376e9a5735079
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Wed Jan 16 00:59:40 2019

[M72][Extensions] Have URLPattern::Contains() properly check schemes

Have URLPattern::Contains() properly check the schemes of the patterns
when evaluating if one pattern contains another. This is important in
order to prevent extensions from requesting chrome:-scheme permissions
via the permissions API when <all_urls> is specified as an optional
permission.

Bug: 859600,918470

TBR=rdevlin.cronin@chromium.org

(cherry picked from commit e13eb21898c7eba584f680e3d17ca1b9e28bc505)

Change-Id: If04d945ad0c939e84a80d83502c0f84b6ef0923d
Reviewed-on: https://chromium-review.googlesource.com/c/1396561
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#621410}
Reviewed-on: https://chromium-review.googlesource.com/c/1413892
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#706}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}
[modify] https://crrev.com/3af68a868964ba47382b07d4848376e9a5735079/chrome/browser/extensions/api/permissions/permissions_api_helpers.cc
[modify] https://crrev.com/3af68a868964ba47382b07d4848376e9a5735079/chrome/browser/extensions/api/permissions/permissions_api_helpers_unittest.cc
[modify] https://crrev.com/3af68a868964ba47382b07d4848376e9a5735079/chrome/browser/extensions/api/permissions/permissions_api_unittest.cc
[modify] https://crrev.com/3af68a868964ba47382b07d4848376e9a5735079/chrome/browser/extensions/permissions_updater_unittest.cc
[modify] https://crrev.com/3af68a868964ba47382b07d4848376e9a5735079/extensions/common/permissions/permissions_data.cc
[modify] https://crrev.com/3af68a868964ba47382b07d4848376e9a5735079/extensions/common/url_pattern.cc
[modify] https://crrev.com/3af68a868964ba47382b07d4848376e9a5735079/extensions/common/url_pattern_unittest.cc


### cr...@appspot.gserviceaccount.com (2019-01-16)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/3af68a868964ba47382b07d4848376e9a5735079

Commit: 3af68a868964ba47382b07d4848376e9a5735079
Author: rdevlin.cronin@chromium.org
Commiter: rdevlin.cronin@chromium.org
Date: 2019-01-16 00:59:40 +0000 UTC

[M72][Extensions] Have URLPattern::Contains() properly check schemes

Have URLPattern::Contains() properly check the schemes of the patterns
when evaluating if one pattern contains another. This is important in
order to prevent extensions from requesting chrome:-scheme permissions
via the permissions API when <all_urls> is specified as an optional
permission.

Bug: 859600,918470

TBR=rdevlin.cronin@chromium.org

(cherry picked from commit e13eb21898c7eba584f680e3d17ca1b9e28bc505)

Change-Id: If04d945ad0c939e84a80d83502c0f84b6ef0923d
Reviewed-on: https://chromium-review.googlesource.com/c/1396561
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#621410}
Reviewed-on: https://chromium-review.googlesource.com/c/1413892
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#706}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### rd...@chromium.org (2019-01-17)

Posting here re severity of this bug from offline questions:

derceg86@ did a good job of outlining a lot of the areas this does/doesn't work, including executing scripts (the extension can't), XHR/fetch (succeeds on blink but should be restricted by additional checks browser-side), accessing cookies (this technically succeeds, but WebUI pages don't have cookies), etc.

I don't think this can easily be used for privilege escalation - we have other process-related boundaries in place that help isolate these processes (these, for instance, are what block the fetch from succeeding).  The host permissions are really only needed for extension APIs, and most of those should have additional checks, because match patterns aren't everything (for instance, we always protect the webstore).  Executing script should always check PermissionsData::IsRestrictedURL(), which will prevent injection even if the match pattern is present (unless a specific commandline flag is there).  As a result of that, I think we *should* have redundant checks for most cases.

All that said, this was definitely a bug, and a somewhat alarming one, and I wouldn't be surprised if it could be used as a stage in an elaborate chain.  I think Severity-Low is probably accurate, since there isn't an immediate risk, but this was a hole in our permissions model.

### mb...@google.com (2019-01-23)

Changing severity based on c#18.

### na...@google.com (2019-01-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-01-24)

Congrats! The Panel has decided to reward $500 for this report. 

### na...@google.com (2019-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-04-19)

This issue was migrated from crbug.com/chromium/918470?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093617)*
