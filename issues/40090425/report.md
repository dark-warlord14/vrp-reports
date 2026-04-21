# Security: Extension with <all_urls> permission can read arbitrary local files and chrome:// pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40090425](https://issues.chromium.org/issues/40090425) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fr...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2018-02-08 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

An extension with the <all\_urls> permission can read any file on the file system and send its content to a remote host, using chrome.tabs.captureVisibleTab.

**VERSION**  

Chrome Version: 64.0.3282.140 + stable  

Operating System: Windows 10 Home, Version 1709

**REPRODUCTION CASE**  

The attachment is a POC extension that upon loading will :  

1- Create a new tab (using tabs.create) with its URL set to the value of the fileToFetch constant (DEFAULT set to file:///c:/) ;  

2- Listen for tabs updates and try to take a screenshot (using chrome.tabs.captureVisibleTab) of the newly opened tab  

3- If the screenshot fails (which will occur upon opening of file:///c:/ using tabs.create), reload the tab. This will cause the tab to be updated and a new screenshot to be taken ;  

4- When the screenshot is made the image data is displayed in extension console and send it to the exfiltration endpoint specified by the value of exfiltrationEndpoint constant.  

5- The opened tab is closed

From there it is easy to create a command and control server which will enable an attacker to navigate throught the file system and fetch arbitrary files.

## Attachments

- [SpyTab.zip](attachments/SpyTab.zip) (application/octet-stream, 1.1 KB)

## Timeline

### el...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions>API]

### in...@chromium.org (2018-02-08)

wjmaclean@, can you please take a look (could this be related to https://chromium.googlesource.com/chromium/src/+/f89035216b627283b79731c3e6a7957707ed9034)

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-02-08)

It's not clear to me what part of this isn't working as expected? 

An extension with <all_URLs> permission can navigate to any URL and can read content directly from any page loaded from any URL. This is an inherently powerful permission.

The use of reload() is a bit of a red-herring here. The initial attempt to screenshot the tab fails (likely because the surface isn't ready) but this can be worked around with setTimeout, e.g.

----
  extObj.tabs.onUpdated.addListener((tabid,c,tab) => {
    if (c.status === "complete")
      setTimeout(function(){extObj.tabs.captureVisibleTab(tab.windowId,captureCallback(tab.id)) }, 200);
  });
----

### fr...@gmail.com (2018-02-08)

In my opinion the thing that is not working properly is the fact that an extension can create a new tab to any resources. 

For example, Firefox restrict URL of resource that can be opened with tabs.create (see https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/tabs/create).

Moreover, it should be considered to further restrict screenshot capability if the tabs permission is not granted. No requiring it to take screenshot is "like" enabling injecting script to fetch page content.

Finally, screenshot should be disabled no matter the granted permission for chrome url and file on the file system. If not enforced, a malicious extension could only wait for you to access chrome://history/ to retrieve the browsing history without  requesting the history or the topsite permission. Therefore, leading to an extension "privilege" escalation.

### el...@chromium.org (2018-02-08)

The original POC continues to work when "Allow access to file URLs" is disabled within the extension's settings. /That/ seems like something that could be addressed by restricting captureVisibleTab() when the tab is on a file URI. Perhaps tab.create("file:///") and its ilk should be forbidden in that circumstance as well.

> the thing that is not working properly is the fact that an extension can 
> create a new tab to any resources 

It's correct to note that the tabs.create() method (https://developer.chrome.com/extensions/tabs#method-create) is powerful and it could be made less powerful by restricting it from navigating to chrome: or file: URLs. As you note, however, this doesn't really prevent spying by malicious extensions which can simply wait for the user to perform their own navigations.

> it should be considered to further restrict screenshot 
> capability if the tabs permission is not granted.

The documentation for https://developer.chrome.com/extensions/tabs#method-captureVisibleTab explicitly notes that it requires the powerful <all_urls> permission, and the documentation for the tabs API notes "The majority of the chrome.tabs API can be used without declaring any permission. However, the "tabs" permission is required in order to populate the url, title, and favIconUrl properties of Tab." I expect the idea is that "<all_urls>" match pattern supersedes the less powerful "tabs" permission, and thus the latter need not be explicitly declared. 

### rd...@chromium.org (2018-02-09)

Yeah, we should really be checking that the extension has permission to access the given page.  That will solve the case of capturing chrome:// and file:// (without permission) urls.  It seems like we should just be able to put this check in the TabsCaptureVisibleTabs function.

### el...@chromium.org (2018-02-09)

The TabsCaptureVisibleTabFunction::GetWebContentsForID function calls PermissionsData::CanCaptureVisiblePage. That function checks for the <all_urls> permission but, interestingly, even if all_urls permission isn't present, it then checks

 GetTabSpecificPermissions(tab_id)->HasAPIPermission(APIPermission::kTab)

meaning an extension with "activeTab" permission may use the API despite the claims in the documentation. (The captured image also includes all of the tab's subframes, even if they're cross-origin.) 

### go...@chromium.org (2018-02-13)

M65 Stable promotion is coming VERY soon. Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and request a merge  into the release branch ASAP. Thank you.

### wj...@chromium.org (2018-02-13)

Re-assigning, since it looks like elawrence@ is looking into this.

### el...@chromium.org (2018-02-13)

I'm not really an appropriate owner for this, I think we need someone on the extensions team to own both the overall policy/plan and the specific fixes to TabsCaptureVisibleTabFunction. 

@devlin, do you have suggestions for who that might be?

### oc...@chromium.org (2018-02-14)

Assigning to rdevlin.cronin@ for now.

### aw...@chromium.org (2018-02-16)

Removing ReleaseBlock-Stable, but once we have a fix in hand we should consider if it's safe enough to merge to 65 to be picked up in any stable refreshes.

### sh...@chromium.org (2018-02-24)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-10)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2018-03-14)

I'm diving into this now; sorry for the delay.

elawrence@: is this security_impact-Medium?  Capturing (but not executing script on) these pages when the extension has either been explicitly invoked or has all urls permission seems like Low to me, but I'll gladly defer to your expertise.

### rd...@chromium.org (2018-03-16)

+meacer

meacer@ and elawrence@, still curious for your take on security_impact level here.

Also, another note: I think this might be actively used by some screenshot extensions to take screenshots of e.g. settings pages (useful for filing bugs).  Are we okay breaking that use case?

### el...@chromium.org (2018-03-19)

meacer is more of an expert on our Extensions system than I am, but I do think this currently rates Severity_Medium, based on the current Severity guidelines[1]. If the attack were limited to pages which the user explicitly interacted (e.g. clicked a BrowserAction button), I'd be comfortable with Severity_Low, but I think the circumvention of the "Allow access to file URLs" checkbox is a pretty significant violation of user's expectations.

[1] https://chromium.googlesource.com/chromium/src/+/lkcr/docs/security/severity-guidelines.md#Medium-severity

In terms of the compatibility question, can we take the same approach-- e.g. an explicit user invocation via a BrowserAction allows the screenshot, but the all_urls permission alone does not?

### rd...@chromium.org (2018-03-26)

Discussed with meacer@ offline, and he suggested similar behavior.  So, what we have is:

<all_urls>: captureVisibleTab disallowed on chrome:// and file://
<all_urls> + allowed file access through settings: captureVisibleTab disallowed on chrome://, allowed on file://
activeTab granted: captureVisibleTab allowed on chrome://, ?? on file://
activeTab granted + allowed file access through settings: captureVisibleTab allowed on chrome:// and file://

?? -> This is dependent on https://crbug.com/chromium/816685, which will require file access in settings before granting active tab.

### bu...@chromium.org (2018-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0aca6bc05a263ea9eafee515fc6ba14da94c1964

commit 0aca6bc05a263ea9eafee515fc6ba14da94c1964
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Fri Apr 06 19:19:23 2018

[Extensions] Restrict tabs.captureVisibleTab()

Modify the permissions for tabs.captureVisibleTab(). Instead of just
checking for <all_urls> and assuming its safe, do the following:
- If the page is a "normal" web page (e.g., http/https), allow the
  capture if the extension has activeTab granted or <all_urls>.
- If the page is a file page (file:///), allow the capture if the
  extension has file access *and* either of the <all_urls> or
  activeTab permissions.
- If the page is a chrome:// page, allow the capture only if the
  extension has activeTab granted.

Bug: 810220

Change-Id: I1e2f71281e2f331d641ba0e435df10d66d721304
Reviewed-on: https://chromium-review.googlesource.com/981195
Commit-Queue: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#548891}
[modify] https://crrev.com/0aca6bc05a263ea9eafee515fc6ba14da94c1964/chrome/browser/extensions/active_tab_unittest.cc
[modify] https://crrev.com/0aca6bc05a263ea9eafee515fc6ba14da94c1964/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/0aca6bc05a263ea9eafee515fc6ba14da94c1964/chrome/common/extensions/permissions/permissions_data_unittest.cc
[modify] https://crrev.com/0aca6bc05a263ea9eafee515fc6ba14da94c1964/chrome/test/data/extensions/api_test/tabs/capture_visible_tab/test_disabled.js
[modify] https://crrev.com/0aca6bc05a263ea9eafee515fc6ba14da94c1964/chrome/test/data/extensions/api_test/tabs/capture_visible_tab_null_window/background.js
[modify] https://crrev.com/0aca6bc05a263ea9eafee515fc6ba14da94c1964/extensions/common/permissions/permissions_data.cc
[modify] https://crrev.com/0aca6bc05a263ea9eafee515fc6ba14da94c1964/extensions/common/permissions/permissions_data.h


### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### rd...@chromium.org (2018-04-18)

I think this should be fixed with #20 (which is already in 67).  I don't think we'll merge this back to 66, but I'll leave that to release managers and security experts to decide.

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-27)

Congrats francois.lajeunesse.robert@! The Chrome VRP panel has decided to award $2,000 for this report.  A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in the Chrome release notes?

### fr...@gmail.com (2018-04-27)

For release notes credit, mentionning my name François Lajeunesse-Robert is sufficient.

Thank you

### sh...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-27)

This bug requires manual review: M67 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-04-27)

+awhalley@ for M67 merge review. 

### el...@chromium.org (2018-04-27)

Commit from #20 initially landed in 67.0.3392.0

### go...@chromium.org (2018-04-27)

Removing "Merge-Review-67" label per https://crbug.com/chromium/810220#c32.

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### wo...@gmail.com (2022-05-22)

This fix (r548891) makes it impossible to invoke chrome.tabs.captureVisibleTab inside the newtab page declared in "chrome_url_overrides". The error is kActiveTabPermissionNotGranted even when calling the API from a window.onclick listener.

### wo...@gmail.com (2022-05-22)

...which is caused by the lack of a check for extension's own origin in 
https://crsrc.org/extensions/common/permissions/permissions_data.cc?q=PermissionsData::CanCaptureVisiblePage

### is...@google.com (2022-05-22)

This issue was migrated from crbug.com/chromium/810220?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090425)*
