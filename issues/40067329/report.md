# XSS on chrome://file-manager, abusable by extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [40067329](https://issues.chromium.org/issues/40067329) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Sandbox>SiteIsolation, Platform>Extensions |
| **Platforms** | ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-07-13 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**

1. Install the extension attached below on a ChromeOS device
2. Alert box running in the origin of chrome://file-manager

**Problem Description:**  

The Files app on ChromeOS (chrome://file-manager) internally uses the JS Origin Private File System API for storing some files.

But these files can also be viewed in the browser with the filesystem: protocol. These pages have the origin of the domain they were created on (in this case chrome://file-manager) and are capable of displaying HTML with no CSP.

In this case, this leads to a quick XSS from something like a Chrome Extension. The extension can download an HTML file, read its path, and open the corresponding filesystem: URL, which will run the HTML file's code in the context of chrome://file-manager.

The extension attached in the POC uses the chrome.downloads permission to achieve this, but it should in theory be possible without the permission.

With the ability to run code on the chrome:// URL, a malicious extension could:

1. use the chrome.send API
2. import and run internal scripts like Mojo scripts from chrome://resources
3. read all local downloaded files by simply fetching their filesystem: paths

**Additional Comments:**

\*\*Chrome version: \*\* 117.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [chrome_url_xss_extension.zip](attachments/chrome_url_xss_extension.zip) (application/octet-stream, 1010 B)
- [chrome_url_xss_poc.mp4](attachments/chrome_url_xss_poc.mp4) (video/mp4, 273.6 KB)
- [Screenshot 2023-07-13 2.11.05 AM.png](attachments/Screenshot 2023-07-13 2.11.05 AM.png) (image/png, 39.1 KB)
- [background.js](attachments/background.js) (text/plain, 1.9 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 251 B)
- [chrome_url_xss_extension2.zip](attachments/chrome_url_xss_extension2.zip) (application/octet-stream, 1.2 KB)
- [chrome_url_xss_poc2.mp4](attachments/chrome_url_xss_poc2.mp4) (video/mp4, 626.0 KB)

## Timeline

### [Deleted User] (2023-07-13)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-13)

In addition to the three effects listed in the original post, the XSS can also be used to get the source code of any Chrome page, as seen in the attached image.

Reporter credit for this bug: Derin Eryilmaz.

### ma...@gmail.com (2023-07-13)

[Comment Deleted]

### da...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions]

### da...@chromium.org (2023-07-13)

The file manager should not display arbitrary HTML in the context of chrome:// which has additional powers. Running arbitrary HTML in chrome:// would be high sev, downgrading 1 due to requirement for an extension.

[Monorail components: Internals>Sandbox>SiteIsolation]

### da...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-07-13)

I am not able to verify which version of chrome this can occur on. I will pessimistically put FoundIn-114. If it was introduced later than 114, the label should be moved up.

### da...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-13)

I could reproduce the bug behind this on version 105, although the chrome.downloads API wasn't working properly, so I couldn't get a proper POC. I wouldn't be surprised if it works in even older versions.

### [Deleted User] (2023-07-13)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### si...@google.com (2023-07-13)

Temporarily assigning to myself for further triage and priortisation.

### ma...@gmail.com (2023-07-13)

Woah, I figured out something new that could make this XSS even more dangerous. Because the XSS in its original form is on a filesystem: page, it doesn't have access to things such as the private APIs on chrome://file-manager.

But while I was messing around, I figured that the filesystem: URL can get access to the window (and thus APIs) of the actual files app interface. Normally, this would be easy to do with window.open, because the filesystem: URL and the pure chrome:// one have the same origin. But because chrome://file-manager opens as an app, I originally thought communication would be impossible.

Steps for gaining access to the real chrome page:

1. Run something like `var FILEMANAGER = window.open("invalid:url")` from the filesystem: page with the XSS. It must be an invalid URL, and thus "unrendered by the browser". about:blank will not work, for some reason .
2. Use chrome.tabs.update() from the extension to redirect the "unrendered" tab to chrome://file-manager. This opens it as an actual tab and not as an app. But it's in a semi-broken state for some reason.
3. Use chrome.tabs.reload() from the extension, which somehow takes the file-manager tab out of this broken state.
4. `FILEMANAGER.window` (a working chrome://file-manager context) can now be accessed from the filesystem: page

By gaining this access, an extension can:
1. Use chrome.fileManagerPrivate and all _eighty-five_ of its private API functions. Creating and editing files is trivial.
2. Probably have better access to Mojo and chrome.send because the requests are now coming from a "pure" Chrome URL

A modified version of my POC extension has been attached with these new changes. 

### jo...@chromium.org (2023-07-14)

[Empty comment from Monorail migration]

### jo...@chromium.org (2023-07-14)

[Empty comment from Monorail migration]

### or...@chromium.org (2023-07-14)

joelhockey and I chatted this morning. There are a couple of issues/bugs that allow for the exploit, but the starting point is that we incorrectly load "filesystem:chrome://file-manager" as a proper WebUI i.e. it has a WebUIController. This is because `url::Origin("filesystem:chrome://file-manager") == url::Origin("chrome://file-manager")` so we happily load the page as a WebUI.

Before WebUIConfigMap we used to compare hosts and `GURL("filesystem://chrome://file-manager).host() != GURL("chrome://file-manager").host()`. This bug was added in 115[1]. Before then, it was possible to open filesystem:chrome://file-manager URLs but it wouldn't get access to chrome.send() or Mojo. The second POC would also not work. We verified this by changing WebUIConfigMap to not create WebUIs for filesystem urls.

I think the short term fix would be to change WebUIConfigMap::GetConfig()[2] to use a GURL instead of a url::Origin and to filter out any filesystem, and possible blob, URLs. This should at least mitigate the exploit. I can take this part.

Beyond that, there are a couple of other issues:

0. Extensions can use chrome.downloads to get the full path of a downloaded file. Then they can use that path to get the user hash which they can use in other parts of the exploit.
1. Extensions can open user files using filesystem://chrome://file-manager/external. (We couldn't figure out what made chrome://file-manager special here. Maybe it's possible to open files under other WebUIs).
2. We run filesystem:chrome:// URLs as if they were in the chrome:// origin even when they point to files outside of the WebUI's resources.
3. The fact that a filesystem:chrome:// URL can open a chrome:// tab and have access to `window` from the second tab. We're lucky the WebUI infra notices the first tab has incorrect WebUI bindings and crashes it before it can do anything.

I can take the WebUIConfig fix, but would be good if someone else familiar with WebUI took on the other issues. Nasko, do you think someone from your team could take a look at those?

[1] https://crrev.com/c/4503585
[2] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/public/browser/webui_config_map.h;l=53-54;drc=4e1b7bc33d42b401d7d9ad1dcba72883add3e2af

### ma...@gmail.com (2023-07-14)

@17

First of all, I can indeed confirm that the second POC doesn't fully work on Chrome 105, and that the filesystem url crashes upon trying. Although the filesystem: page by itself can still do things like fetch Chrome URLs on 105 (see https://crbug.com/chromium/1464456#c2)

As for your point 0, it's worth noting that there are likely a lot of ways that this could be done. An extension could read something like file:///var/log/arc.1.log which also contains the user hash.
For your point 1, I think that chrome.fileManagerPrivate.getVolumeRoot or a similar internal is probably configured to host its OPFS filesystem on chrome://file-manager.

Also, why is the browser allowed to display filesystem:chrome:// URLs, anyway? file-manager is the only origin that uses them and it never displays them with that protocol. It's not the best solution, but I suppose you could just stop the browser from loading those URLs.

### ch...@google.com (2023-07-14)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/291154025). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.



[Monorail blocking: b/291154025]

### or...@chromium.org (2023-07-14)

Yeah, it's still a problem that we render those URLs as chrome:// URLs in 105, but at least we don't grant it Mojo, chrome.send(), and  chrome.fileManagerPrivate, like in after 115.

Point 0: Makes sense! Thanks for the context.

Point 1. Ohh interesting. That would explain why we don't see anything in the backend of the WebUI that loads the files.

### ch...@google.com (2023-07-14)

Dear all,

can you please proceed here: https://issuetracker.google.com/issues/291154025

Please don't post updates here....everything needs to be done in https://issuetracker.google.com/issues/291154025



### [Deleted User] (2023-07-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2023-07-15)

[Comment Deleted]

### lu...@chromium.org (2023-07-16)

I don't have access to:
https://issuetracker.google.com/issues/291154025 (or its internal version), with neither of my accounts @chromium.org or @google.com.

### ch...@google.com (2023-07-17)

lucmult@ you have now access...please try again

### or...@chromium.org (2023-07-17)

chmiel: Any reason why not all the people cc'ed on this bug were copied to the internal bug? There's a lot of people cc'ed here that have important context for the bug.

### ch...@google.com (2023-07-17)

Can you please add the missing people who are cc'ed on the bug report. I am not sure who all should be included (Security Bug access should be very limited and I don't know the cc'ed people) , so I would appreciate your help in adding the appropriate people.

### cr...@chromium.org (2023-07-17)

Please include me on the bug.  This is important for Site Isolation and I don't have access to https://issuetracker.google.com/issues/291154025.

### al...@chromium.org (2023-07-17)

I don't have access to https://issuetracker.google.com/issues/291154025 either.  Please include me as well, as ortuno@ has asked me to review a part of the fix.

### am...@chromium.org (2023-07-17)

I've gone ahead and added you both to the buganizer bug -- creis@ and alexmos@

### am...@chromium.org (2023-07-17)

everyone who has been cc'ed to this issue as of now has also been cc'ed to b/291154025 

### dc...@chromium.org (2023-07-18)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-22)

By the way, another side effect of this is that chrome-untrusted URLs can be opened with:

chrome.fileManagerPrivate.openURL('chrome-untrusted://terminal')

---

https://chromium.googlesource.com/chromium/src/+/main/extensions/docs/security_faq.md#why-do-we-not-allow-extensions-to-open-or-close-chrome_untrusted_scheme-pages

### [Deleted User] (2023-07-31)

chmiel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2023-08-05)

A practical future attack from this XSS (if the victim user has crostini installed) would be to edit the .bashrc file for crostini and open terminal using https://crbug.com/chromium/1464456#c33. With this, you could get permanent code execution in crostini.

### ch...@google.com (2023-08-08)

Project: chromium/src
Branch: refs/branch-heads/5790

commit b2354da6b23520367fb7e1a972866cc75989ae13
Author: Giovanni Ortuño Urquidi <ortuno@chromium.org>
Date:   Fri Jul 28 06:21:59 2023

    [Merge M115] webui: Filter out non-chrome scheme URLs in WebUIConfigMap
   
    url::Origin::Create() drops filesystem: and blob: from URLs so filter
    those out before using Create().
   
    (cherry picked from commit b46c37206ab6f8df2c2ce8f23383c967360dab55)
   
    (cherry picked from commit 1ae7ab6ff83e8c0e82a28252ba7962e87b8ed288)
   
    Bug: b/291154025
    Change-Id: Ia8fd0d1048deaef346accd7b4cb64b448e8dc9f1
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4686653
    Commit-Queue: Giovanni Ortuno Urquidi <ortuno@chromium.org>
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1172220}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4719366
    Cr-Original-Commit-Position: refs/branch-heads/5845@{#833}
    Cr-Original-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4728383
    Auto-Submit: Giovanni Ortuno Urquidi <ortuno@chromium.org>
    Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
    Cr-Commit-Position: refs/branch-heads/5790@{#1864}
    Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

M       chrome/browser/ash/system_extensions/system_extensions_install_manager.cc
M       chrome/browser/ash/web_applications/demo_mode_app_integration_browsertest.cc
M       chrome/browser/chrome_content_browser_client.cc
M       content/browser/service_worker/service_worker_context_wrapper.cc
M       content/browser/webui/web_ui_browsertest.cc
A       content/browser/webui/webui_config_map_unittest.cc
M       content/public/browser/webui_config_map.cc
M       content/public/browser/webui_config_map.h
M       content/public/test/scoped_web_ui_controller_factory_registration.cc
M       content/public/test/scoped_web_ui_controller_factory_registration.h
M       content/test/BUILD.gn

https://chromium-review.googlesource.com/4728383
08:23
08:23
CLs: Merged:​crrev/c/4686653, crrev/c/4719366      crrev/c/4686653, crrev/c/4719366, crrev/c/4728383
CLs: Pending:​crrev/c/4728383      <none>

### [Deleted User] (2023-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-08)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-10)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-09-08)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ma...@gmail.com (2023-09-14)

WOW, thanks for the reward! 🥳

### am...@chromium.org (2023-09-14)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thanks for your efforts and reporting this issue to us -- great finding and good job! 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-11-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ce4f7ae7f80f0c04023b7d337e156b74b600fe76

commit ce4f7ae7f80f0c04023b7d337e156b74b600fe76
Author: David Bienvenu <davidbienvenu@chromium.org>
Date: Mon Nov 27 23:02:49 2023

Fix timeout in WebUiConfig Death tests

WebUiConfigTest.GetAndRemoveNonChromeUrls was running 6
EXPECT_DEATH_IF_SUPPORTEDs, which occasionally timed out on some Windows
bots because each EXPECT_DEATH takes over 5 seconds. This CL makes
it a parameterized test, parameterized by the URL being tested.

Bug: 1464456
Change-Id: Id388451b85bb04f54970a4234456299dd8c97054
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5063672
Reviewed-by: Demetrios Papadopoulos <dpapad@chromium.org>
Commit-Queue: David Bienvenu <davidbienvenu@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1229593}

[modify] https://crrev.com/ce4f7ae7f80f0c04023b7d337e156b74b600fe76/content/browser/webui/webui_config_map_unittest.cc


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1464456?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, Platform>Extensions]
[Monorail blocking: b/291154025]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067329)*
