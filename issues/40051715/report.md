# Security: Possible to escape sandbox via devtools_page

| Field | Value |
|-------|-------|
| **Issue ID** | [40051715](https://issues.chromium.org/issues/40051715) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2020-03-08 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Using devtools\_page, an extension can customize the devtools. The page referred to by the extension will be loaded whenever the devtools is shown.

Using this ability, an extension can download and run an executable once the user opens the devtools on any page, without requiring any further interaction.

**VERSION**  

Chrome Version: Tested on 80.0.3987.132 (stable) and 82.0.4078.0 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**  

Note that the demonstration here is Windows-specific.

1. Install the attached extension. Note that the manifest.json file in the extension contains a reference to the extension ID. You'll need to update this once Chrome has set an ID, then reload the extension. This wouldn't be an issue for a published extension, since the ID would be fixed in that case.
2. Load a page (it doesn't matter exactly what), then open the devtools.
3. Wait 4 seconds.
4. A cmd.exe instance should be started.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [devtools.js](attachments/devtools.js) (text/plain, 2.0 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 300 B)
- [background.js](attachments/background.js) (text/plain, 863 B)
- [devtools.js](attachments/devtools_52951289.js) (text/plain, 2.3 KB)
- [manifest.json](attachments/manifest_52951290.json) (text/plain, 409 B)
- [page.html](attachments/page.html) (text/plain, 123 B)
- [page.js](attachments/page.js) (text/plain, 89 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 1 B)
- [devtools.html](attachments/devtools.html) (text/plain, 127 B)
- [devtools.js](attachments/devtools_52951341.js) (text/plain, 4.9 KB)
- [manifest.json](attachments/manifest_52951342.json) (text/plain, 137 B)

## Timeline

### de...@gmail.com (2020-03-08)

In the demonstration above, there's a few steps being taken:

1. The devtools_page value contains a javascript: URL. This URL runs within the context of the devtools itself. This means that as soon as the devtools is opened (on any page), the extension has access to the devtools context.

Note that it isn't necessary to use a javascript: URL; the issue can be reproduced in the same sort of way when devtools_page refers to a file within the extension. However, using a javascript: URL simplifies the demonstration.

2. The page being debugged is navigated to chrome://downloads.

3. At this point, the goal is download and run an arbitrary executable without any further interaction. This is made more complicated by the fact that unsafe downloads may be need explicit approval from the user, both when downloading and when opening.

To work around this, the extension uses methods available via the full devtools protocol. Specifically, Page.setDownloadBehavior is first called in the following way:

parent.SDK.targetManager.mainTarget().pageAgent().setDownloadBehavior("allow", "C:\\Users\\Public");

This then means that when the target file is downloaded, it won't be marked as dangerous.

4. The extension then dispatches a key event to the chrome://downloads page via SDK.targetManager.mainTarget().inputAgent().dispatchKeyEvent. This event goes through the devtools protocol and is treated as a real event.

This means that when the extension calls openFileRequiringGesture in the context of the chrome://downloads page a short while later, the request succeeds as the page looks like it's had a recent user gesture.

The end result is that the executable that's downloaded is run without any other interaction from the user.

### mp...@google.com (2020-03-11)

+rdevlin.cronin@ and yangguo@. Not sure if this is devtools or extensions issue. Perhaps extensions shouldn't be able to inject themselves into devtools for chrome:// protocol or other privileged protocols?

This may be a duplicate of https://crbug.com/795595, but the user gesture bypass for the chrome downloads page is interesting.

### [Deleted User] (2020-03-11)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2020-03-11)

[Empty comment from Monorail migration]

[Monorail components: Platform>DevTools Platform>Extensions]

### de...@gmail.com (2020-03-12)

For what it's worth, it's also possible to perform the same steps as above without any user interaction after extension install, provided the "debugger" permission is also set. There's an extension I've attached here that demonstrates this. Reproduction instructions are similar to those in the original demonstration:

1. Install the attached extension. Update the extension ID referenced in manifest.json then reload the extension.
2. Wait 6 seconds.
3. A cmd.exe instance should be started.

From what I can tell, the extension permissions prompt when specifying debugger and devtools_page is the same as when only specifying debugger, so the user might expect that the extension is only using the debugger permission.

### ya...@chromium.org (2020-03-13)

Similarly to related issues, I think that extensions should not have the ability to open devtools or have access to devtools UI.

### rd...@chromium.org (2020-03-18)

Thanks for the report!

This is definitely a bug.  Extensions shouldn't be allowed to attach and debug chrome:-scheme pages.  We have a good bit of code around this, which is predominantly by overriding DevToolsAgentHostClient::MayAttachToURL() here [1].  That prevents attaching to restricted pages (which chrome:-scheme pages are) and also webui pages.  So the fact that the extension is still able to send commands to it implies that that method isn't being correctly called or checked.

caseq@, mind taking a look from the devtools perspective, since it seems like this should be working if that method is being correctly called?  Feel free to punt back to me if that's not the case.

[1] https://cs.chromium.org/chromium/src/chrome/browser/extensions/api/debugger/debugger_api.cc?l=372-381&rcl=0a1c4d9781d7327bb1dccd2ce3d9ad2a530a0103

### [Deleted User] (2020-03-22)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-23)

caseq: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-24)

caseq: Uh oh! This issue still open and hasn't been updated in the last 16 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2020-03-24)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1df0bf470f22368104de9aee7ec95d96c5b0232a

commit 1df0bf470f22368104de9aee7ec95d96c5b0232a
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Mar 25 21:10:21 2020

DevTools extensions: validate devtools_page URLs

This ensures that the devtools_page URL has correct scheme and host,
both when loading the manifest and when pushing data to DevTools front-end.

Bug: 1059577
Change-Id: I69a7ccdccfae31781ead371a85d23df36f108665
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2118894
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#753369}

[modify] https://crrev.com/1df0bf470f22368104de9aee7ec95d96c5b0232a/chrome/browser/devtools/devtools_ui_bindings.cc
[modify] https://crrev.com/1df0bf470f22368104de9aee7ec95d96c5b0232a/chrome/common/extensions/chrome_manifest_url_handlers.cc
[modify] https://crrev.com/1df0bf470f22368104de9aee7ec95d96c5b0232a/chrome/common/extensions/docs/templates/articles/devtools.html
[modify] https://crrev.com/1df0bf470f22368104de9aee7ec95d96c5b0232a/chrome/common/extensions/manifest_tests/extension_manifests_devtools_unittest.cc
[add] https://crrev.com/1df0bf470f22368104de9aee7ec95d96c5b0232a/chrome/test/data/extensions/manifest_tests/devtools_extension_invalid_page_url.json
[add] https://crrev.com/1df0bf470f22368104de9aee7ec95d96c5b0232a/chrome/test/data/extensions/manifest_tests/devtools_extension_page_url_https.json


### de...@gmail.com (2020-03-26)

I've attached a demonstration extension that shows how to download and run an executable, even if devtools_page is set to a page within the extension.

Reproduction instructions:

1. Install the attached extension.
2. Load a page, then open the devtools.
3. Wait 8 seconds.
4. A cmd.exe instance should be started.

This version of the extension relies on the fact that the devtools_page entry remains loaded in the devtools, no matter what the target page is and that it's possible to inspect a devtools window that the user has opened via chrome://inspect/.

These abilities mean that once the user has opened the devtools on a page (it doesn't matter what page), the extension can redirect to chrome://inspect/, then inspect the devtools window that was opened. At that stage, the extension has the ability to run code within the context of the devtools and the demonstration proceeds in the same way as above.

As an overview of the various situations:

1. devtools_page set to extension page, user opens devtools, possible to run executable.
2. devtools_page set to javascript: URL, no user interaction, possible to read local files and run code within the context of other extensions.
3. devtools_page set to javascript: URL, debugger permission also requested, no user interaction, possible to run executable.

### ca...@chromium.org (2020-03-27)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4d33ef9730cae7a86b46690f434ced6cf8173642

commit 4d33ef9730cae7a86b46690f434ced6cf8173642
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Mon Mar 30 06:23:18 2020

DevTools: only allow inspectWorker if client can attach to browser

Bug: 1059577, 1064852
Change-Id: I2994be49f53aa8fc52fbd7cee543fa65521670f0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2121434
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#754408}

[modify] https://crrev.com/4d33ef9730cae7a86b46690f434ced6cf8173642/chrome/browser/extensions/api/debugger/debugger_apitest.cc
[add] https://crrev.com/4d33ef9730cae7a86b46690f434ced6cf8173642/chrome/test/data/extensions/api_test/debugger_inspect_worker/background.js
[add] https://crrev.com/4d33ef9730cae7a86b46690f434ced6cf8173642/chrome/test/data/extensions/api_test/debugger_inspect_worker/inspected_page.html
[add] https://crrev.com/4d33ef9730cae7a86b46690f434ced6cf8173642/chrome/test/data/extensions/api_test/debugger_inspect_worker/manifest.json
[add] https://crrev.com/4d33ef9730cae7a86b46690f434ced6cf8173642/chrome/test/data/extensions/api_test/debugger_inspect_worker/service_worker.js
[modify] https://crrev.com/4d33ef9730cae7a86b46690f434ced6cf8173642/content/browser/devtools/protocol/service_worker_handler.cc
[modify] https://crrev.com/4d33ef9730cae7a86b46690f434ced6cf8173642/content/browser/devtools/protocol/service_worker_handler.h
[modify] https://crrev.com/4d33ef9730cae7a86b46690f434ced6cf8173642/content/browser/devtools/render_frame_devtools_agent_host.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/a08cb9b5eb602e1bc0921629309ebdad5208f8d1

commit a08cb9b5eb602e1bc0921629309ebdad5208f8d1
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Wed Apr 01 22:27:20 2020

Disable extensions when inspecting DOM UI

This disables front-end extensions when DevTools are attached to
privileged pages.

Bug: 1059577, 795595
Change-Id: I0971fd993bee63eea347ffa800c3cc72e09ba334
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2128732
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Tim van der Lippe <tvanderlippe@chromium.org>

[modify] https://crrev.com/a08cb9b5eb602e1bc0921629309ebdad5208f8d1/front_end/extensions/ExtensionServer.js
[modify] https://crrev.com/a08cb9b5eb602e1bc0921629309ebdad5208f8d1/front_end/Tests.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/67fd81d2f51379aa9e89be61863b6f213524225c

commit 67fd81d2f51379aa9e89be61863b6f213524225c
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Apr 02 06:54:10 2020

Roll src/third_party/devtools-frontend/src 0a34c98ea0b0..4d123409dc1a (2 commits)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/0a34c98ea0b0..4d123409dc1a

git log 0a34c98ea0b0..4d123409dc1a --date=short --first-parent --format='%ad %ae %s'
2020-04-01 caseq@chromium.org Improve code hygiene in ExtensionServer
2020-04-01 caseq@chromium.org Disable extensions when inspecting DOM UI

Created with:
  gclient setdep -r src/third_party/devtools-frontend/src@4d123409dc1a

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1059577,chromium:1064519,chromium:795595
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: I9b945356218e8de1b56c79f9b114606beab046d5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2133415
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#755721}

[modify] https://crrev.com/67fd81d2f51379aa9e89be61863b6f213524225c/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3c0f2556708b39f7cb223ea33306a7fbb10ca01f

commit 3c0f2556708b39f7cb223ea33306a7fbb10ca01f
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Fri Apr 03 19:47:18 2020

DevTools: add tests for extensions on DOM UI pages

This is the chrome-side counterpart of
https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2128732

Bug: 1059577, 795595
Change-Id: Iec2ee772a42b4c7bc2249627c0839f7506f0cd1d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2129344
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#756375}

[modify] https://crrev.com/3c0f2556708b39f7cb223ea33306a7fbb10ca01f/chrome/browser/devtools/devtools_sanity_browsertest.cc
[add] https://crrev.com/3c0f2556708b39f7cb223ea33306a7fbb10ca01f/chrome/test/data/devtools/extensions/chrome_scheme/devtools.html
[add] https://crrev.com/3c0f2556708b39f7cb223ea33306a7fbb10ca01f/chrome/test/data/devtools/extensions/chrome_scheme/devtools.js
[add] https://crrev.com/3c0f2556708b39f7cb223ea33306a7fbb10ca01f/chrome/test/data/devtools/extensions/chrome_scheme/manifest.json


### ca...@chromium.org (2020-04-03)

Requesting a merge to m81, but ultimately deferring it to the security team's judgement on whether the severity of the issue justifies merge at this stage.

### [Deleted User] (2020-04-03)

This bug requires manual review: We are only 3 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2020-04-03)

Can this CL wait for next M81 respin? 

So that the change will be well baked in lower channels before merging to M81 branch.

+adetaylor@(Security TPM), are you ok with it?


### go...@chromium.org (2020-04-03)

Also there are multiple changes listed in this bug. Will of them need a merge to M81 if we decide to take in for M81 respin?

### ad...@chromium.org (2020-04-03)

I think let's wait and have this roll into M83 organically. It doesn't look like the sort of complexity/security benefit ratio we'd want to merge into the current stable release. Thanks for asking though caseq@.

### [Deleted User] (2020-04-04)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-06)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-08)

Congrats! The Panel decided to award $3,000 for this report. 

### na...@google.com (2020-04-08)

[Empty comment from Monorail migration]

### de...@gmail.com (2020-04-10)

About the fix in https://crbug.com/chromium/1059577#c16:

One thing I've noticed is that the change doesn't have the desired result when a different scheme is used for DOM UI pages. For example, Edge uses edge:// rather than chrome://.

### ca...@chromium.org (2020-04-10)

Thanks, that's a good point -- we should really pass the list of privileged schemes from the embedder (there's a TODO comment to that effect in the CL), or perhaps even just white-list http(s) there.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/82b85893c49370f96ccb53573536dc1493daf8f3

commit 82b85893c49370f96ccb53573536dc1493daf8f3
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Thu May 07 21:07:58 2020

Revert "DevTools: add tests for extensions on DOM UI pages"

This reverts commit 3c0f2556708b39f7cb223ea33306a7fbb10ca01f.

Reason for revert: test is extremely flaky

Per https://analysis.chromium.org/p/chromium/flake-portal/flakes/occurrences?key=ag9zfmZpbmRpdC1mb3ItbWVyUgsSBUZsYWtlIkdjaHJvbWl1bUBicm93c2VyX3Rlc3RzQERldlRvb2xzRXh0ZW5zaW9uVGVzdC5UZXN0RXZhbHVhdGVPbkNocm9tZVNjaGVtZQw this flakily fails about 10 times an hour.

Original change's description:
> DevTools: add tests for extensions on DOM UI pages
> 
> This is the chrome-side counterpart of
> https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2128732
> 
> Bug: 1059577, 795595
> Change-Id: Iec2ee772a42b4c7bc2249627c0839f7506f0cd1d
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2129344
> Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
> Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
> Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#756375}

TBR=dgozman@chromium.org,rdevlin.cronin@chromium.org,caseq@chromium.org,bmeurer@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 1059577, 795595
Change-Id: I2919088167b064086b315d8c3a64df569d95c844
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2188512
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#766575}

[modify] https://crrev.com/82b85893c49370f96ccb53573536dc1493daf8f3/chrome/browser/devtools/devtools_sanity_browsertest.cc
[delete] https://crrev.com/3de250a49eedeb88c1e23fcc6429eba348f96161/chrome/test/data/devtools/extensions/chrome_scheme/devtools.html
[delete] https://crrev.com/3de250a49eedeb88c1e23fcc6429eba348f96161/chrome/test/data/devtools/extensions/chrome_scheme/devtools.js
[delete] https://crrev.com/3de250a49eedeb88c1e23fcc6429eba348f96161/chrome/test/data/devtools/extensions/chrome_scheme/manifest.json


### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0f93d79ad9a6002933a5eebe000df8eca702b55a

commit 0f93d79ad9a6002933a5eebe000df8eca702b55a
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Sat Aug 29 03:24:55 2020

Reland "DevTools: add tests for extensions on DOM UI pages"

This reverts commit 82b85893c49370f96ccb53573536dc1493daf8f3.

Reason for revert: let's give this test another change. it seems to reliable pass for me locally and I think the original failure was rather due to a front-end race fixed here: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2242769

Original change's description:
> Revert "DevTools: add tests for extensions on DOM UI pages"
> 
> This reverts commit 3c0f2556708b39f7cb223ea33306a7fbb10ca01f.
> 
> Reason for revert: test is extremely flaky
> 
> Per https://analysis.chromium.org/p/chromium/flake-portal/flakes/occurrences?key=ag9zfmZpbmRpdC1mb3ItbWVyUgsSBUZsYWtlIkdjaHJvbWl1bUBicm93c2VyX3Rlc3RzQERldlRvb2xzRXh0ZW5zaW9uVGVzdC5UZXN0RXZhbHVhdGVPbkNocm9tZVNjaGVtZQw this flakily fails about 10 times an hour.
> 
> Original change's description:
> > DevTools: add tests for extensions on DOM UI pages
> > 
> > This is the chrome-side counterpart of
> > https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/2128732
> > 
> > Bug: 1059577, 795595
> > Change-Id: Iec2ee772a42b4c7bc2249627c0839f7506f0cd1d
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2129344
> > Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
> > Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
> > Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
> > Cr-Commit-Position: refs/heads/master@{#756375}
> 
> TBR=dgozman@chromium.org,rdevlin.cronin@chromium.org,caseq@chromium.org,bmeurer@chromium.org
> 
> # Not skipping CQ checks because original CL landed > 1 day ago.
> 
> Bug: 1059577, 795595
> Change-Id: I2919088167b064086b315d8c3a64df569d95c844
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2188512
> Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
> Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#766575}

TBR=dgozman@chromium.org,mek@chromium.org,rdevlin.cronin@chromium.org,caseq@chromium.org,bmeurer@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 1059577
Bug: 795595
Change-Id: Ibd719500160685664de90415d718b88b4621b52e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2382487
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/master@{#802868}

[modify] https://crrev.com/0f93d79ad9a6002933a5eebe000df8eca702b55a/chrome/browser/devtools/devtools_sanity_browsertest.cc
[add] https://crrev.com/0f93d79ad9a6002933a5eebe000df8eca702b55a/chrome/test/data/devtools/extensions/chrome_scheme/devtools.html
[add] https://crrev.com/0f93d79ad9a6002933a5eebe000df8eca702b55a/chrome/test/data/devtools/extensions/chrome_scheme/devtools.js
[add] https://crrev.com/0f93d79ad9a6002933a5eebe000df8eca702b55a/chrome/test/data/devtools/extensions/chrome_scheme/manifest.json


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1059577?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions]
[Monorail mergedwith: crbug.com/chromium/1059676]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051715)*
