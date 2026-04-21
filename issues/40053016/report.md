# Security: Extensions can use chrome.debugger API to access contents of local files

| Field | Value |
|-------|-------|
| **Issue ID** | [40053016](https://issues.chromium.org/issues/40053016) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2020-08-06 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Typically, extensions can't access local files without explicit user permission. However, by using the chrome.debugger API, an extension can navigate an iframe on a page to a file: location, then capture the contents of that page using the Page.captureSnapshot devtools protocol method.

**VERSION**  

Chrome Version: Tested on 84.0.4147.105 (stable) and 86.0.4224.0 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. Install the attached extension. Ensure that "Allow access to file URLs" isn't checked.
2. Once installed, the extension will open page.html in a new tab.
3. Once page.html has loaded, the extension will attach to it using chrome.debugger.attach and use Page.navigate to navigate an iframe on the page to file:///c:/. This navigation will result in the debugger being detached from the page (since the extension doesn't have access to local files).
4. The extension will then reattach the debugger to the page.
5. It will then call Page.captureSnapshot and log the result to the console:

chrome.debugger.sendCommand({tabId: tab.id}, "Page.captureSnapshot", {}, function (result) {  

console.log(result.data);  

});

This output should contain the contents of the file: iframe and can be seen by opening the devtools for the extension's background page.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 1.9 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 213 B)
- [page.html](attachments/page.html) (text/plain, 103 B)

## Timeline

### xi...@chromium.org (2020-08-06)

Thanks for the report. I wonder if the underlying issue is similar to https://crbug.com/1059676.

caseq@, handed over to you to decide on whether it is a duplicate. Thanks!

[Monorail components: Platform>DevTools]

### ha...@chromium.org (2020-08-07)

[Empty comment from Monorail migration]

### si...@chromium.org (2020-08-07)

IIUC, this means that an extension (regardless of permissions) can get the contents of everything the browser can navigate to.

### si...@chromium.org (2020-08-07)

Also note related bug crbug.com/1113558, in which Page.navigate is used to execute JavaScript.

### [Deleted User] (2020-08-07)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-07)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2020-08-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4838b76ae48797760fd8a362b4dc15325ccddcf5

commit 4838b76ae48797760fd8a362b4dc15325ccddcf5
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Aug 19 06:10:05 2020

Add more checks for chrome.debugger extensions

Bug: 1113558, 1113565
Change-Id: I99f2e030f9a38f1ffd6b6adc760ba15e5d231f96
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2342277
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Sigurd Schneider <sigurds@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#799514}

[modify] https://crrev.com/4838b76ae48797760fd8a362b4dc15325ccddcf5/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/4838b76ae48797760fd8a362b4dc15325ccddcf5/chrome/test/data/extensions/api_test/debugger_navigate_subframe/background.js
[add] https://crrev.com/4838b76ae48797760fd8a362b4dc15325ccddcf5/chrome/test/data/extensions/api_test/debugger_navigate_subframe/inspected_page.html
[add] https://crrev.com/4838b76ae48797760fd8a362b4dc15325ccddcf5/chrome/test/data/extensions/api_test/debugger_navigate_subframe/manifest.json
[modify] https://crrev.com/4838b76ae48797760fd8a362b4dc15325ccddcf5/content/browser/devtools/devtools_instrumentation.cc
[modify] https://crrev.com/4838b76ae48797760fd8a362b4dc15325ccddcf5/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/4838b76ae48797760fd8a362b4dc15325ccddcf5/content/browser/devtools/render_frame_devtools_agent_host.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5a809a08fd5ca32cb8d594664416db2f2dc8ebdc

commit 5a809a08fd5ca32cb8d594664416db2f2dc8ebdc
Author: Christian Dullweber <dullweber@chromium.org>
Date: Wed Aug 19 09:41:22 2020

Revert "Add more checks for chrome.debugger extensions"

This reverts commit 4838b76ae48797760fd8a362b4dc15325ccddcf5.

Reason for revert: 1119297

Original change's description:
> Add more checks for chrome.debugger extensions
> 
> Bug: 1113558, 1113565
> Change-Id: I99f2e030f9a38f1ffd6b6adc760ba15e5d231f96
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2342277
> Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
> Reviewed-by: Sigurd Schneider <sigurds@chromium.org>
> Reviewed-by: Yang Guo <yangguo@chromium.org>
> Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
> Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#799514}

TBR=dgozman@chromium.org,rdevlin.cronin@chromium.org,caseq@chromium.org,yangguo@chromium.org,sigurds@chromium.org

Change-Id: I01ad12ca99ac75197f9073e2c6c9d0eaa0d95147
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 1113558
Bug: 1113565
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2362920
Reviewed-by: Christian Dullweber <dullweber@chromium.org>
Commit-Queue: Christian Dullweber <dullweber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#799558}

[modify] https://crrev.com/5a809a08fd5ca32cb8d594664416db2f2dc8ebdc/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[delete] https://crrev.com/dda5b70c005af869ec6f5850bd46d83e8008bff5/chrome/test/data/extensions/api_test/debugger_navigate_subframe/background.js
[delete] https://crrev.com/dda5b70c005af869ec6f5850bd46d83e8008bff5/chrome/test/data/extensions/api_test/debugger_navigate_subframe/inspected_page.html
[delete] https://crrev.com/dda5b70c005af869ec6f5850bd46d83e8008bff5/chrome/test/data/extensions/api_test/debugger_navigate_subframe/manifest.json
[modify] https://crrev.com/5a809a08fd5ca32cb8d594664416db2f2dc8ebdc/content/browser/devtools/devtools_instrumentation.cc
[modify] https://crrev.com/5a809a08fd5ca32cb8d594664416db2f2dc8ebdc/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/5a809a08fd5ca32cb8d594664416db2f2dc8ebdc/content/browser/devtools/render_frame_devtools_agent_host.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a064db74c8734fbf47de2f3a3503832514857173

commit a064db74c8734fbf47de2f3a3503832514857173
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Fri Aug 21 19:31:34 2020

Reland "Add more checks for chrome.debugger extensions"

This reverts commit 5a809a08fd5ca32cb8d594664416db2f2dc8ebdc.

Reason for revert: I don't think the test failure is related. Please note it stopped before the revert landed (build no 91007 vs. 91010). This must have been a flake, or a independent failure that has been fixed by one of the front-end rolls.

Original change's description:
> Revert "Add more checks for chrome.debugger extensions"
> 
> This reverts commit 4838b76ae48797760fd8a362b4dc15325ccddcf5.
> 
> Reason for revert: 1119297
> 
> Original change's description:
> > Add more checks for chrome.debugger extensions
> > 
> > Bug: 1113558, 1113565
> > Change-Id: I99f2e030f9a38f1ffd6b6adc760ba15e5d231f96
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2342277
> > Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
> > Reviewed-by: Sigurd Schneider <sigurds@chromium.org>
> > Reviewed-by: Yang Guo <yangguo@chromium.org>
> > Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
> > Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
> > Cr-Commit-Position: refs/heads/master@{#799514}
> 
> TBR=dgozman@chromium.org,rdevlin.cronin@chromium.org,caseq@chromium.org,yangguo@chromium.org,sigurds@chromium.org
> 
> Change-Id: I01ad12ca99ac75197f9073e2c6c9d0eaa0d95147
> No-Presubmit: true
> No-Tree-Checks: true
> No-Try: true
> Bug: 1113558
> Bug: 1113565
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2362920
> Reviewed-by: Christian Dullweber <dullweber@chromium.org>
> Commit-Queue: Christian Dullweber <dullweber@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#799558}

TBR=dgozman@chromium.org,rdevlin.cronin@chromium.org,caseq@chromium.org,yangguo@chromium.org,sigurds@chromium.org,dullweber@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 1113558
Bug: 1113565
Change-Id: Ic98fc037028a210204b7935b0b8e50e4e36e2397
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2368446
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#800682}

[modify] https://crrev.com/a064db74c8734fbf47de2f3a3503832514857173/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/a064db74c8734fbf47de2f3a3503832514857173/chrome/test/data/extensions/api_test/debugger_navigate_subframe/background.js
[add] https://crrev.com/a064db74c8734fbf47de2f3a3503832514857173/chrome/test/data/extensions/api_test/debugger_navigate_subframe/inspected_page.html
[add] https://crrev.com/a064db74c8734fbf47de2f3a3503832514857173/chrome/test/data/extensions/api_test/debugger_navigate_subframe/manifest.json
[modify] https://crrev.com/a064db74c8734fbf47de2f3a3503832514857173/content/browser/devtools/devtools_instrumentation.cc
[modify] https://crrev.com/a064db74c8734fbf47de2f3a3503832514857173/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/a064db74c8734fbf47de2f3a3503832514857173/content/browser/devtools/render_frame_devtools_agent_host.h


### [Deleted User] (2020-08-22)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-08-24)

caseq@ is this commit intended to fix this bug? If so please mark it as fixed.

### [Deleted User] (2020-09-06)

caseq: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9940472e708a4003aee9edf9da42d68fde591e08

commit 9940472e708a4003aee9edf9da42d68fde591e08
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Tue Sep 08 17:50:37 2020

[m86] Reland "Add more checks for chrome.debugger extensions"

TBR=rdevlin.cronin@chromium.org

This reverts commit 5a809a08fd5ca32cb8d594664416db2f2dc8ebdc.

Reason for revert: I don't think the test failure is related. Please note it stopped before the revert landed (build no 91007 vs. 91010). This must have been a flake, or a independent failure that has been fixed by one of the front-end rolls.

Original change's description:
> Revert "Add more checks for chrome.debugger extensions"
>
> This reverts commit 4838b76ae48797760fd8a362b4dc15325ccddcf5.
>
> Reason for revert: 1119297
>
> Original change's description:
> > Add more checks for chrome.debugger extensions
> >
> > Bug: 1113558, 1113565
> > Change-Id: I99f2e030f9a38f1ffd6b6adc760ba15e5d231f96
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2342277
> > Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
> > Reviewed-by: Sigurd Schneider <sigurds@chromium.org>
> > Reviewed-by: Yang Guo <yangguo@chromium.org>
> > Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
> > Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
> > Cr-Commit-Position: refs/heads/master@{#799514}
>
> TBR=dgozman@chromium.org,rdevlin.cronin@chromium.org,caseq@chromium.org,yangguo@chromium.org,sigurds@chromium.org
>
> Change-Id: I01ad12ca99ac75197f9073e2c6c9d0eaa0d95147
> No-Presubmit: true
> No-Tree-Checks: true
> No-Try: true
> Bug: 1113558
> Bug: 1113565
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2362920
> Reviewed-by: Christian Dullweber <dullweber@chromium.org>
> Commit-Queue: Christian Dullweber <dullweber@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#799558}

TBR=dgozman@chromium.org,rdevlin.cronin@chromium.org,caseq@chromium.org,yangguo@chromium.org,sigurds@chromium.org,dullweber@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

(cherry picked from commit a064db74c8734fbf47de2f3a3503832514857173)

Bug: 1113558
Bug: 1113565
Change-Id: Ic98fc037028a210204b7935b0b8e50e4e36e2397
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2368446
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#800682}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2398884
Cr-Commit-Position: refs/branch-heads/4240@{#506}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/9940472e708a4003aee9edf9da42d68fde591e08/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/9940472e708a4003aee9edf9da42d68fde591e08/chrome/test/data/extensions/api_test/debugger_navigate_subframe/background.js
[add] https://crrev.com/9940472e708a4003aee9edf9da42d68fde591e08/chrome/test/data/extensions/api_test/debugger_navigate_subframe/inspected_page.html
[add] https://crrev.com/9940472e708a4003aee9edf9da42d68fde591e08/chrome/test/data/extensions/api_test/debugger_navigate_subframe/manifest.json
[modify] https://crrev.com/9940472e708a4003aee9edf9da42d68fde591e08/content/browser/devtools/devtools_instrumentation.cc
[modify] https://crrev.com/9940472e708a4003aee9edf9da42d68fde591e08/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/9940472e708a4003aee9edf9da42d68fde591e08/content/browser/devtools/render_frame_devtools_agent_host.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3b5f65c0aeca53ee01eb8caf3b93f3bbfcdea503

commit 3b5f65c0aeca53ee01eb8caf3b93f3bbfcdea503
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Fri Sep 18 22:35:09 2020

[m85] Reland "Add more checks for chrome.debugger extensions"

TBR=rdevlin.cronin@chromium.org

This reverts commit 5a809a08fd5ca32cb8d594664416db2f2dc8ebdc.

Reason for revert: I don't think the test failure is related. Please note it stopped before the revert landed (build no 91007 vs. 91010). This must have been a flake, or a independent failure that has been fixed by one of the front-end rolls.

Original change's description:
> Revert "Add more checks for chrome.debugger extensions"
>
> This reverts commit 4838b76ae48797760fd8a362b4dc15325ccddcf5.
>
> Reason for revert: 1119297
>
> Original change's description:
> > Add more checks for chrome.debugger extensions
> >
> > Bug: 1113558, 1113565
> > Change-Id: I99f2e030f9a38f1ffd6b6adc760ba15e5d231f96
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2342277
> > Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
> > Reviewed-by: Sigurd Schneider <sigurds@chromium.org>
> > Reviewed-by: Yang Guo <yangguo@chromium.org>
> > Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
> > Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
> > Cr-Commit-Position: refs/heads/master@{#799514}
>
> TBR=dgozman@chromium.org,rdevlin.cronin@chromium.org,caseq@chromium.org,yangguo@chromium.org,sigurds@chromium.org
>
> Change-Id: I01ad12ca99ac75197f9073e2c6c9d0eaa0d95147
> No-Presubmit: true
> No-Tree-Checks: true
> No-Try: true
> Bug: 1113558
> Bug: 1113565
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2362920
> Reviewed-by: Christian Dullweber <dullweber@chromium.org>
> Commit-Queue: Christian Dullweber <dullweber@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#799558}

TBR=dgozman@chromium.org,rdevlin.cronin@chromium.org,caseq@chromium.org,yangguo@chromium.org,sigurds@chromium.org,dullweber@chromium.org

(cherry picked from commit a064db74c8734fbf47de2f3a3503832514857173)

(cherry picked from commit 9940472e708a4003aee9edf9da42d68fde591e08)

Bug: 1113558
Bug: 1113565
Change-Id: Ic98fc037028a210204b7935b0b8e50e4e36e2397
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2368446
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#800682}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2398884
Cr-Original-Commit-Position: refs/branch-heads/4240@{#506}
Cr-Original-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2419133
Cr-Commit-Position: refs/branch-heads/4183@{#1863}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/3b5f65c0aeca53ee01eb8caf3b93f3bbfcdea503/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/3b5f65c0aeca53ee01eb8caf3b93f3bbfcdea503/chrome/test/data/extensions/api_test/debugger_navigate_subframe/background.js
[add] https://crrev.com/3b5f65c0aeca53ee01eb8caf3b93f3bbfcdea503/chrome/test/data/extensions/api_test/debugger_navigate_subframe/inspected_page.html
[add] https://crrev.com/3b5f65c0aeca53ee01eb8caf3b93f3bbfcdea503/chrome/test/data/extensions/api_test/debugger_navigate_subframe/manifest.json
[modify] https://crrev.com/3b5f65c0aeca53ee01eb8caf3b93f3bbfcdea503/content/browser/devtools/devtools_instrumentation.cc
[modify] https://crrev.com/3b5f65c0aeca53ee01eb8caf3b93f3bbfcdea503/content/browser/devtools/render_frame_devtools_agent_host.cc
[modify] https://crrev.com/3b5f65c0aeca53ee01eb8caf3b93f3bbfcdea503/content/browser/devtools/render_frame_devtools_agent_host.h


### ca...@chromium.org (2020-09-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-28)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-30)

Congratulations! The VRP panel has decided to award $5000 for this bug.

### ad...@google.com (2020-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1113565?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053016)*
