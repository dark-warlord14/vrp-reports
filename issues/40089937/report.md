# Security: chrome.devtools.inspectedWindow.eval executes within privileged pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40089937](https://issues.chromium.org/issues/40089937) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions, Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gr...@hotmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2017-12-17 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Extensions are normally not allowed to execute javascript within privileged pages for many reasons. Though it seems like we can use "chrome.devtools.inspectedWindow.eval" to execute JS in any page we want.

Given that the manifest contains permission for only "<all\_urls>" it should not work within privileged pages. I think it should follow similar restrictions as "chrome.tabs.executeScript"

**VERSION**  

Chrome Version: 63.0.3239.108 (Official Build) (64-bit)  

Operating System: Windows 10 x64

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug.**

1. Install attached extension
2. Go to a privileged page like about:downloads
3. Open web inspector
4. Navigate to 'My panel'

## Attachments

- [devtools-panels.zip](attachments/devtools-panels.zip) (application/octet-stream, 5.2 KB)
- [PoC.zip](attachments/PoC.zip) (application/octet-stream, 1.7 KB)

## Timeline

### el...@chromium.org (2017-12-18)

Interesting. Thanks for the report!

[Monorail components: Platform>DevTools>Platform Platform>Extensions>API]

### el...@chromium.org (2017-12-18)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-12-23)

[Empty comment from Monorail migration]

### gr...@hotmail.com (2017-12-24)

FWIW, we can also execute JS using the following:

     chrome.devtools.panels.elements.createSidebarPane("Font Properties",
          function(sidebar) {
            sidebar.setExpression('alert("Alert from setExpression")','test')
          });

Same behavior as inspectedWindow.eval 

### al...@chromium.org (2017-12-26)

[Empty comment from Monorail migration]

### gr...@hotmail.com (2017-12-27)

Here is a more minimized testcase using both ways to execute JS. I removed the permissions setting within the manifest and it still works, seems like devtools extensions ignore it completely.



### rs...@chromium.org (2017-12-28)

Tentatively labeling as medium, since this does require the user to install an extension.

### gr...@hotmail.com (2017-12-28)

It's also possible to automatically execute the JS as soon as the web console appears using the following (within devtools.js) instead:

chrome.devtools.panels.create(
  "My Panel",
  "icons/star.png",
  "devtools/panel/panel.html",
  function(panel){
	  chrome.devtools.inspectedWindow.eval('alert()');
  }
); 

### sh...@chromium.org (2017-12-28)

[Empty comment from Monorail migration]

### dg...@chromium.org (2017-12-28)

I think this is a feature rather than a bug. It requires an extension with devtools permission to be installed, and DevTools being manually open by the user on chrome:// page.
What do security folks think?

### gr...@hotmail.com (2017-12-28)

You could just ask a user to hold CTRL+SHFT+I and this would work, I don't think thats unlikely though definitely a slight mitigation. Past similar bugs have been considered security sensitive with medium severity: 456841, 38920, 30937, 42356, 83010
I also wonder if there is a problem with having devtool extensions abide by the manifest permission setting? I can't imagine that would break anything.

### sh...@chromium.org (2018-01-01)

kozy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-01-03)

[Empty comment from Monorail migration]

### ko...@chromium.org (2018-01-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-15)

caseq: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-01-26)

caseq: Ping. Are you the right person for this bug?

### me...@chromium.org (2018-01-26)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-26)

rob@robwu.nl's notes from https://crbug.com/chromium/798184:

"
Other affected APIs are:
https://developer.chrome.com/extensions/devtools_panels#method-ExtensionSidebarPane-setExpression
https://developer.chrome.com/extensions/devtools_inspectedWindow#method-reload

dgozman added a comment (https://bugs.chromium.org/p/chromium/issues/detail?id=795595#c10 ) where he questioned whether this is a feature/bug and cited some manual interaction requirements to support that claim. All of these interactions can be automated via extensions, as I have shown in the PoC in https://crbug.com/chromium/795595#c2.

Extensions should not be able to automatically run scripts in privileged pages, since it can be used to completely compromise Chrome (and also run local programs, see https://crbug.com/chromium/798222).
"

There is additional information and a PoC in that bug as well.

### oc...@chromium.org (2018-02-19)

Friendly ping from the security sheriff. dgozman, would do you think about rob's comment in #18?

### sh...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### gr...@hotmail.com (2018-05-16)

May I get an update on this issue? A similar problem ha been fixed in Firefox and I am planning to do a writeup somewhere around June.

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### gr...@hotmail.com (2018-09-13)

Benign ping, any update on this?

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-11-12)

Just to note that the reporter has made this bug public: https://leucosite.com/WebExtension-Security-Part-2/

caseq@: Do you have any plans to work on this soon? This is a P1 that has been open for almost 11 months.

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-04-12)

caseq and other devtools folks, ping?

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### dg...@chromium.org (2019-05-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### ca...@chromium.org (2019-10-30)

[Empty comment from Monorail migration]

### ca...@chromium.org (2019-10-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

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


### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

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


### ad...@google.com (2020-05-13)

caseq@ do you consider this now fixed? If so please mark the bug Fixed so it can get picked up for release notes, etc.

### ca...@chromium.org (2020-05-15)

I think we can close this, although there's a bit of the follow-up work (e.g. plumb proper set of restricted schemes, fix the test flakiness)

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-16)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-19)

Requesting merge to beta M83 because latest trunk commit (756375) appears to be after beta branch point (756066).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-19)

This bug requires manual review: Request affecting a post-stable build
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
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ci...@google.com (2020-05-19)

Merge approved.

### na...@google.com (2020-05-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-21)

Congrats! The Panel decided to award $2,000 for this report

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### sr...@google.com (2020-05-28)

Please complete the merge to M83 branch asap, as we will cut the re-spin RC tomorrow.

### ca...@chromium.org (2020-05-28)

No merge required -- the original fix made it into trunk as of 83.0.4103.0: https://storage.googleapis.com/chromium-find-releases-static/67f.html#67fd81d2f51379aa9e89be61863b6f213524225c

The subsequent CL is only a test, no need to merge that.

### na...@google.com (2020-05-29)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-22)

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


### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/795595?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools>Platform, Platform>Extensions>API]
[Monorail mergedwith: crbug.com/chromium/1019524, crbug.com/chromium/798184]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089937)*
