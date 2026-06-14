# Security: Extension can run code in the chrome-devtools://devtools (e.g. to read local files)

| Field | Value |
|-------|-------|
| **Issue ID** | [40089991](https://issues.chromium.org/issues/40089991) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2017-12-23 |
| **Bounty** | $2,500.00 |

## Description

Chrome version: 63.0.3239.108

The devtools may load remote sources via [1] (e.g. product_registry_impl [2]).
Chrome Extensions are able to intercept these requests and replace the content with arbitrary data, and thus run arbitrary JavaScript code at chrome-devtools://devtools. Arbitrary network resources and local files can be read in this way, and if there is a debuggable Node.js app, then this vulnerability can also be used to launch arbitrary processes.


The product_registry_impl module is only loaded in some devtools tabs (e.g. the Performance and the Network). The attached proof of concept opens the devtools with the Performance tab enabled and works on Chrome 63 and 64 (In Chrome 65 it is not fully automated because of 484f731aaead5d72c26a21ea012cd2a706146f19  - you have to open the performance tab of the devtools yourself).


Steps to reproduce:
1. Load the attached proof-of-concept extension (e.g. as an unpacked extension via chrome://extensions).
2. [Chrome 65+] Manually open the devtools and switch to the Performance tab.

Expected result:
- Nothing particular should happen in the devtools.

Actual result:
- The extension intercepts a script request, reads a local file via the devtools bindings and displays the results in a dialog in the Chrome extension.


Although not shown in the PoC, the vulnerability can silently be exploited without any further user interaction by forcing the Performance tab to be displayed initially:
Common.settings.createSetting('panel-selectedTab').set('timeline');

I have not investigated other modules declared "remote" [2], these might also provide entry points for exploitation.
I think that the best way to fix this bug is to hide script requests originating from the devtools from extensions.


[1] https://chromium.googlesource.com/chromium/src/+/525e4537ba0e2f4e3331a38fb35b646a4bae3b51/third_party/WebKit/Source/devtools/front_end/Runtime.js#133
[2] https://chromium.googlesource.com/chromium/src/+/525e4537ba0e2f4e3331a38fb35b646a4bae3b51/third_party/WebKit/Source/devtools/front_end/inspector.json#25

## Attachments

- [extension-privilege-escalation-via-devtools.zip](attachments/extension-privilege-escalation-via-devtools.zip) (application/octet-stream, 2.7 KB)

## Timeline

### ro...@robwu.nl (2017-12-24)

Besides abusing the devtools APIs itself, it is also possible to run code at any privileged page.

https://crbug.com/chromium/797511 demonstrates a memory safety issue on a chrome:-page. Normally the amount of user interaction would make exploitation impractical.
However, because of this bug, once a devtools has been opened, a malicious extension can navigate to any URL and run code in that page. Consequently, it has become trivial to exploit another vulnerability (which was previously difficult to abuse).

### ro...@robwu.nl (2017-12-25)

I would expect chrome-devtools://devtools/bundled/ to only serve *bundled* resources.
The fact that this does not happen surprises me.
Why can't these modules be bundled with the devtools?

The current implementation has several issues:
- Usability: a bad internet connectivity results in decreased functionality.
- Security: A MITM attacker can perform privilege escalation (in this bug, the MITM attacker is an extension, but a network attacker is also a possibility).
- Usability in Chromium: The remote devtools is based on the git revision of the build. Custom builds of Chromium have different hashes, so the remote resources are 404.

An example of an existing remote resource (Chromium 62.0.3202.94) is:
https://chrome-devtools-frontend.appspot.com/serve_file/@4fd852a98d66564c88736c017b0a0b0478e885ad/product_registry_impl/product_registry_impl_module.js

Since the revision is included in the URL, and unknown revisions return a 404, I presume that the content is static and known with the build. So if there is really a good reason for hosting the content remotely, then at the very least add an integrity check, e.g. by replacing the current XMLHttpRequest + self.eval implementation with a <script> tag and SRI (Subresource Integrity).

Remote devtools resources were introduced as an experiment in abf8b4a22fcbadff57034b1e7e601fbe464c8aca (https://crbug.com/chromium/459167), and promoted to a non-experiment in b9b50923d7ea3bd02ce35ee5d9069adb5fbb1234.
I cannot view https://crbug.com/chromium/459167, so I am cc-ing the patch authors to see whether it is feasible to:
- disable remote resources (bundle them0)  for devtools instantiated at chrome-devtools://devtools/bundled/
- (or if the previous is not possible) add integrity checks for remote scripts.



### ro...@robwu.nl (2017-12-25)

So to summarize the impact:

After a user installs a malicious extension (with very limited permissions), the attacker has arbitrary access to all network resources and local files without further user interaction.

Additionally, if the user opens the devtools, then the attacker can escalate to webui privileges (i.e. chrome:// pages, e.g. changing proxy settings, changing trust bits of certificates, extracting saved passwords and anything that Chrome can do).
A PoC of exploiting a vulnerability in an arbitrary webui page is shown in https://crbug.com/chromium/797511.

With only two user interactions (installing the malicious extension, opening the devtools), the attacker has persistent access to any local/network resource AND webUI privileges, because the malicious extension can navigate to chrome://flags and flip the --extensions-on-chrome-urls.

### ro...@robwu.nl (2017-12-26)

Patch: https://chromium-review.googlesource.com/c/chromium/src/+/844316

The patch was meant to solve https://crbug.com/chromium/797500 (restricting extension access to chrome-devtools://remote/), but it also breaks the security exploit of this bug report since the DevTools do not directly load the resource through a https:-URL, but through the chrome-devtools://devtools/remote-URL [1]
(the remoteBase parameter is derived from " chrome-devtools://devtools/bundled/inspector.html?remoteBase=https://chrome-devtools-frontend.appspot.com/serve_file/@3cda3761ecf33e0dbfceee709a730b955b73031f/ " ).

Although the immediate security issue has been mitigated, I recommend to consider my suggestions in https://crbug.com/chromium/797497#c2 before closing the bug.


[1] https://chromium.googlesource.com/chromium/src/+/d786d7cb2fa94b01959808a18ea3b01ccaf693c1/third_party/WebKit/Source/devtools/front_end/Runtime.js#1058

### rs...@chromium.org (2017-12-28)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2018-01-01)

I have improved the exploit to not require any user interaction to abuse this vulnerability (besides installing a malicious extension).

See https://crbug.com/chromium/798222 for a PoC.

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


### dg...@chromium.org (2018-01-16)

Remote modules are very important for DevTools, and we are not going to get rid of them. They save a lot of space in Chromium binary while allowing us to experiment and/or deliver many features no matter what the size impact they have.

Since we presumably fixed the "intercepted by extensions" usecase (thanks Rob Wu!), remote modules should be safe now. We are loading them through https from a page with pinned (known in advance) certificate. Do you think that's susceptible to MITM attacks?

### ro...@robwu.nl (2018-01-17)

#8 All right.
Then I'm marking this bug as fixed since the immediate security issue has been addressed, and you have confidence in the abilities of Chrome to not fall victim again to MITM of remote DevTools resources.

> We are loading them through https from a page with pinned (known in advance) certificate. Do you think that's susceptible to MITM attacks?

Are you referring to HPKP?
Google/Chrome is moving away from HPKP (and the affected domain is not using HPKP in the first place), so certificate pinning cannot be relied upon. If your threat model includes an attacker with network MITM abilities, then the remote DevTools module system is insecure (at the very least you need to include a hash for every externally hosted static file).
If you assume that the PKI is secure (and trust content from chrome-devtools-frontend.appspot.com), then no further action is required.

### sh...@chromium.org (2018-01-17)

[Empty comment from Monorail migration]

### mb...@google.com (2018-01-17)

[Empty comment from Monorail migration]

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

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-06)

And $2,500 for this one - thanks as ever!

### aw...@chromium.org (2018-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/797497?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089991)*
