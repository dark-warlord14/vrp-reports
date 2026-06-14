# Security: chrome-devtools://devtools/remote/ can be modified by extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [40089992](https://issues.chromium.org/issues/40089992) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2017-12-23 |
| **Bounty** | $2,500.00 |

## Description

Chrome version: 63.0.3239.108

**VULNERABILITY DETAILS**  

chrome-devtools://devtools/remote/ loads a remote site (<https://chrome-devtools-frontend.appspot.com/>) and grants privileged APIs to this page.  

Chrome extensions can intercept and modify these requests and consequently read arbitrary data from local files and websites.

**VERSION**  

Chrome Version: 63.0.3239.108 (stable), 65.0.3303.0 (canary)

**REPRODUCTION CASE**  

Load the attached extension (e.g. via the "Load unpacked extension..." button that shows up after enabling Developer Mode at chrome://extensions ).

The extension will open chrome-devtools://remote/x.html, redirect the request via the webRequest extension API and use the privileges to show the contents of a local file.

## Attachments

- [devtools-remote-intercept.zip](attachments/devtools-remote-intercept.zip) (application/octet-stream, 1.3 KB)

## Timeline

### ro...@robwu.nl (2017-12-25)

This bug also applies to chrome://devtools/custom/ (which resolves to a remote resource when Chrome is started with --custom-devtools-frontend=<URL HERE>).

The call sites are:
DevToolsDataSource::StartRemoteDataRequest
DevToolsDataSource::StartCustomDataRequest

### ro...@robwu.nl (2017-12-26)

Patch: https://chromium-review.googlesource.com/c/chromium/src/+/844316

+cc reviewers

### rs...@chromium.org (2017-12-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2649de11c562aa96d336c06136a1a20c01711be0

commit 2649de11c562aa96d336c06136a1a20c01711be0
Author: Rob Wu <rob@robwu.nl>
Date: Wed Jan 10 00:32:10 2018

Hide DevTools frontend from webRequest API

Prevent extensions from observing requests for remote DevTools frontends
and add regression tests.

And update ExtensionTestApi to support initializing the embedded test
server and port from SetUpCommandLine (before SetUpOnMainThread).

BUG=797497,797500
TEST=browser_test --gtest_filter=DevToolsFrontendInWebRequestApiTest.HiddenRequests

Cq-Include-Trybots: master.tryserver.chromium.linux:linux_mojo
Change-Id: Ic8f44b5771f2d5796f8c3de128f0a7ab88a77735
Reviewed-on: https://chromium-review.googlesource.com/844316
Commit-Queue: Rob Wu <rob@robwu.nl>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#528187}
[modify] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/chrome/browser/extensions/api/chrome_extensions_api_client.cc
[modify] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/chrome/browser/extensions/api/chrome_extensions_api_client.h
[modify] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/chrome/browser/extensions/api/web_request/web_request_apitest.cc
[modify] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/chrome/browser/extensions/extension_apitest.cc
[modify] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/chrome/browser/ui/webui/devtools_ui.cc
[modify] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/chrome/browser/ui/webui/devtools_ui.h
[add] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/chrome/test/data/extensions/api_test/webrequest/devtoolsfrontend/fakedevtools.html
[add] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/chrome/test/data/extensions/api_test/webrequest/devtoolsfrontend/fakedevtools.js
[add] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/chrome/test/data/extensions/api_test/webrequest/test_devtools.html
[add] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/chrome/test/data/extensions/api_test/webrequest/test_devtools.js
[modify] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/extensions/browser/api/extensions_api_client.cc
[modify] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/extensions/browser/api/extensions_api_client.h
[modify] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/extensions/browser/api/web_request/web_request_permissions.cc
[modify] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/extensions/browser/api/web_request/web_request_permissions_unittest.cc
[modify] https://crrev.com/2649de11c562aa96d336c06136a1a20c01711be0/testing/buildbot/filters/mojo.fyi.network_browser_tests.filter


### ro...@robwu.nl (2018-01-14)

Verified fixed in 65.0.3322.0 using the STR from the report.

Requesting merge of 2649de11c562aa96d336c06136a1a20c01711be0 to M-64.

### sh...@chromium.org (2018-01-14)

This bug requires manual review: We are only 8 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-01-14)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-16)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-01-17)

Recommendation is to wait until M65. Awhalley@ - thoughts?

### ro...@robwu.nl (2018-01-17)

I recommend against waiting, and merge this with 64. My patch is straightforward and does not only fix this bug, but also https://crbug.com/chromium/797497.

The consequences of this bug are severe: an extension can easily abuse these vulnerabilities to run arbitrary code in privileged pages of the attacker's choice.
In https://crbug.com/chromium/798222 , I showed how this bug can be used to launch external programs outside of Chrome.

### rd...@chromium.org (2018-01-17)

And, of course, since Rob landed the fix, the bug is now all-but-disclosed.

I'd second a vote for merging (but will gladly defer to awhalley@).

### aw...@google.com (2018-01-17)

Given the assessment in #10 I'm increasing the severity to High. This will miss this week's M64 beta, but it's just made it into Dev. rdevlin.cronin@, what's your assessment of the regression risk of this change?

### rd...@chromium.org (2018-01-17)

From an extensions perspective, I think the risk is pretty low.

### aw...@google.com (2018-01-17)

abdulsyed@ - good for 64

### me...@chromium.org (2018-01-17)

As a follow up to the fix, should extensions be able to open chrome-devtools: URLs? An outright ban would break legitimate extensions that open devtools, but is there anything else we can do?

### ro...@robwu.nl (2018-01-18)

@#15
chrome-devtools: without target have no legitimate purpose because disconnected DevTools do not serve any user needs.
The only legitimate purpose for opening chrome-devtools: that I can think of is to engage in a remote debugging session (i.e. when the ws parameter is present).
But this use case can already be catered for by using the remote frontend URL directly.

So if you have little confidence in the ability to keep chrome-devtools: safe, then a way to reduce the impact is to rewrite chrome-devtools:-URLs to the remote frontend URL. Remote debugging should still work in this way, while extensions cannot exploit URL-based vulnerabilities of the chrome-devtools:-scheme.

If you are an advocate of this approach, I suggest to create a new bug and talk with Devlin and the DevTools team. And just in case, also search through the source code of all extensions in the Chrome Web Store to see if there are any extensions that use "chrome-devtools:".

### me...@google.com (2018-01-18)

My question was directed to everyone in this bug, including CC'ed folks. I wanted to get a first opinion before filing a separate bug.

I did indeed a search for extensions containing chrome-devtools before commenting. There are such extensions, but many of the usages come from code that is shared between extensions implying some sort of common library. I didn't dig deeper than that.

### rd...@chromium.org (2018-01-18)

@abdulsyed - ping on the merge?

(@meacer - haven't had a chance to dive into that yet, but I haven't forgotten. :))

### ab...@chromium.org (2018-01-19)

approving merge for M64 based on #12,#13,#14. Branch:3282

### ro...@robwu.nl (2018-01-19)

The patch had one non-trivial merge conflict due to 019b53cca7c5fbd33fe122ef6c572134b8fe7949.
To resolve this conflict, I omitted the "request.type != content::RESOURCE_TYPE_MAIN_FRAME" check in WebRequestPermissions::HideRequest. This does not change the behavior of Chrome on the release branch, and does not impact the intended functionality of my patch. These expectations are covered by the DevToolsFrontendInWebRequestApiTest.HiddenRequests test.

I verified the patch locally as follows (on the 63 branch; I assume that it also works on 64):
- Manually: Compile chrome, load the extension from the report and confirm that the extension was not able to modify the chrome-devtools:-page (404 not found will be shown, served by the remote server).
- Automatically: Compile browser_tests, and run:
  browser_test --gtest_filter=DevToolsFrontendInWebRequestApiTest.HiddenRequests

### bu...@chromium.org (2018-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4ac53f6cc73b9d697a286b197228fa2049136afc

commit 4ac53f6cc73b9d697a286b197228fa2049136afc
Author: Rob Wu <rob@robwu.nl>
Date: Fri Jan 19 11:43:03 2018

Hide DevTools frontend from webRequest API

Prevent extensions from observing requests for remote DevTools frontends
and add regression tests.

And update ExtensionTestApi to support initializing the embedded test
server and port from SetUpCommandLine (before SetUpOnMainThread).

BUG=797497,797500
TEST=browser_test --gtest_filter=DevToolsFrontendInWebRequestApiTest.HiddenRequests
TBR=rob@robwu.nl

(cherry picked from commit 2649de11c562aa96d336c06136a1a20c01711be0)

Cq-Include-Trybots: master.tryserver.chromium.linux:linux_mojo
Change-Id: Ic8f44b5771f2d5796f8c3de128f0a7ab88a77735
Reviewed-on: https://chromium-review.googlesource.com/844316
Commit-Queue: Rob Wu <rob@robwu.nl>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#528187}
Reviewed-on: https://chromium-review.googlesource.com/875984
Reviewed-by: Rob Wu <rob@robwu.nl>
Cr-Commit-Position: refs/branch-heads/3282@{#546}
Cr-Branched-From: 5fdc0fab22ce7efd32532ee989b223fa12f8171e-refs/heads/master@{#520840}
[modify] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/chrome/browser/extensions/api/chrome_extensions_api_client.cc
[modify] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/chrome/browser/extensions/api/chrome_extensions_api_client.h
[modify] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/chrome/browser/extensions/api/web_request/web_request_apitest.cc
[modify] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/chrome/browser/extensions/extension_apitest.cc
[modify] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/chrome/browser/ui/webui/devtools_ui.cc
[modify] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/chrome/browser/ui/webui/devtools_ui.h
[add] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/chrome/test/data/extensions/api_test/webrequest/devtoolsfrontend/fakedevtools.html
[add] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/chrome/test/data/extensions/api_test/webrequest/devtoolsfrontend/fakedevtools.js
[add] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/chrome/test/data/extensions/api_test/webrequest/test_devtools.html
[add] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/chrome/test/data/extensions/api_test/webrequest/test_devtools.js
[modify] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/extensions/browser/api/extensions_api_client.cc
[modify] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/extensions/browser/api/extensions_api_client.h
[modify] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/extensions/browser/api/web_request/web_request_permissions.cc
[modify] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/extensions/browser/api/web_request/web_request_permissions_unittest.cc
[modify] https://crrev.com/4ac53f6cc73b9d697a286b197228fa2049136afc/testing/buildbot/filters/mojo.fyi.network_browser_tests.filter


### aw...@google.com (2018-01-22)

I was a little exuberant in #12, returning to Medium severity after consultation.

### aw...@chromium.org (2018-01-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-22)

And $2,500 for this report - thanks!

### aw...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/797500?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089992)*
