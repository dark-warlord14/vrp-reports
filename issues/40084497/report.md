# Security: Devtools old remote frontend allows running privileged scripts via overwriting localStorage settings

| Field | Value |
|-------|-------|
| **Issue ID** | [40084497](https://issues.chromium.org/issues/40084497) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Reporter** | gr...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2016-06-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Specially crafted input to whitelisted URLs on Devtools remote frontend, allows an attacker to manipulate Devtool settings stored in localStorage. One possible injection point that allows attacker to run arbitrary javascript code is via watchExpression that runs in the context of the website when DevTools is launched. Other injection points of arbitrary javascript expression is through conditional breakpoints on specific pages.

**VERSION**  

Chrome Version: 51.0.2704.84 m stable  

Operating System: All

**REPRODUCTION CASE**

1. Copy paste "chrome-devtools://devtools/remote/serve\_rev/@180642/devtools.html?settings={%22watchExpressions%22:%22[%22alert(document.domain)%22]%22}" to omnibar
2. Press CTRL-SHIFT-I [in windows] to open DevTools, Switch to Sources panel ( default panel setting can possibly be controlled by injecting the 'lastActivePanel' setting )
3. Observe alert 'devtools'

An example of it running privileged javascript code [to access filesystem] is attached. It basically injects an expression that checks for location.host==devtools, and access filesystem using DevToolsAPI.sendMessageToEmbedder("loadNetworkResource",...) calls.  

[you can observe the 1st file on filesystem displayed on webpage]

## Attachments

- [Devtools-Crafted-URI1.txt](attachments/Devtools-Crafted-URI1.txt) (text/plain, 1.4 KB)

## Timeline

### np...@chromium.org (2016-06-09)

Thanks for the report.  Can you produce a demonstration that doesn't require pasting a URL into the omnibox?  The same alert() can be generating with a pasted javascript:alert() URL.

### gr...@gmail.com (2016-06-09)

This issue has some similarity to 571121 (where it is discussed in length). One of the other attack vector mentioned there is by using a malicious extension (with zero permission) that can open chrome-devtools:// URLs.

The main security issue is the ability to change Devtools' settings stored in localStorage by visiting the URL.

The maximum impact is demonstrated by execution privilege script (in Step#2) that gets access to filesystem (attached Devtools.Crafted-URL1.txt in orig report). If the inspected page is a regular webpage, it can read cookie-data etc. and send it to the attacker.


### np...@chromium.org (2016-06-09)

I repro'd the example on M51 stable.  Maybe these chrome-devtools:// links write to settings should require the referrer's scheme to be the same.

dgozman@ -- Can you find an appropriate owner?
Grabbing cc list from http://crbug.com/571121



[Monorail components: Platform>DevTools>Platform]

### gr...@gmail.com (2016-06-10)

PoC Video (Unlisted): https://drive.google.com/file/d/0BzBNDrWkH6nFcmNqWDU3czJTTTA/view?usp=sharing


### sh...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### np...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

dgozman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gr...@gmail.com (2016-07-04)

FYI - One more Attack vector (besides malicious extension; copy-pasting URLs) is by sending a crafted chrome-devtools link via "Google Tone" extension. The extension allows sending URLs of any schemes to nearby machines.

### sh...@chromium.org (2016-07-06)

dgozman: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### ta...@google.com (2016-07-13)

Can't we just set a minimal CL for whatever appengine code is serving that?

That seems like a quick easy fix.

### dg...@chromium.org (2016-07-23)

I don't think this is a problem. It requires user to 1) open url which cannot be linked to and 2) open DevTools for that page manually.

It's equivalent to opening DevTools for DevTools and executing any code in console, which anyone can do if they want.

Any thoughts from security experts?

### ta...@google.com (2016-07-23)

The problem is that an extension with no permissions can navigate to that URL.

This is a variant of https://crbug.com/chromium/571121, afaik the same discussion applies.

### dg...@chromium.org (2016-07-23)

IIUC, this one requires the additional step of opening DevTools after navigation to the specific url (see step 2 in original report).

### ta...@google.com (2016-07-23)

Ah, I missed that - that does make it very low severity!

But...it does seem prudent to have a way to prevent loading earlier revisions in case a bug does surface that is exploitable from just URL parameters (or with more realistic interaction)?

### gr...@gmail.com (2016-07-23)

IMHO, at the very least, we wouldn't want a malicious extension overwriting DevTools' localStorage settings. For it to cause any sort of damage, the DevTools needs to opened to inspect a page at some point in time. 


### ta...@google.com (2016-07-23)

Oh I see, so if at anypoint in future you open devtools, it still fires?

Well, that does seem bad?

### gr...@gmail.com (2016-07-23)

The overwritten settings is persisted. You can set malicious watch-expression, or conditional (with malicious expression) breakpoints on various webpages, that can fire when devtools/sources-panel is opened to inspect that page. 

### bu...@chromium.org (2016-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d5e6098dc2e984befc836f482845137245fa04e2

commit d5e6098dc2e984befc836f482845137245fa04e2
Author: dgozman <dgozman@chromium.org>
Date: Tue Jul 26 01:11:02 2016

[DevTools] Do not use "settings" query param.

Implemented the same functionality on embedder side.
Also, sanitizing "settings" query param for remote frontends.

BUG=618037

Review-Url: https://codereview.chromium.org/2177983004
Cr-Commit-Position: refs/heads/master@{#407666}

[modify] https://crrev.com/d5e6098dc2e984befc836f482845137245fa04e2/chrome/browser/devtools/devtools_window.cc
[modify] https://crrev.com/d5e6098dc2e984befc836f482845137245fa04e2/chrome/browser/devtools/devtools_window.h
[modify] https://crrev.com/d5e6098dc2e984befc836f482845137245fa04e2/content/shell/browser/layout_test/blink_test_controller.cc
[modify] https://crrev.com/d5e6098dc2e984befc836f482845137245fa04e2/content/shell/browser/layout_test/layout_test_devtools_frontend.cc
[modify] https://crrev.com/d5e6098dc2e984befc836f482845137245fa04e2/content/shell/browser/layout_test/layout_test_devtools_frontend.h
[modify] https://crrev.com/d5e6098dc2e984befc836f482845137245fa04e2/content/shell/browser/shell_devtools_frontend.cc
[modify] https://crrev.com/d5e6098dc2e984befc836f482845137245fa04e2/content/shell/browser/shell_devtools_frontend.h
[modify] https://crrev.com/d5e6098dc2e984befc836f482845137245fa04e2/third_party/WebKit/Source/devtools/front_end/devtools.js
[modify] https://crrev.com/d5e6098dc2e984befc836f482845137245fa04e2/third_party/WebKit/Source/devtools/front_end/main/Main.js


### dg...@chromium.org (2016-07-27)

I think we can merge the fix to M53 after it bakes in canary for a while.

### aw...@chromium.org (2016-08-01)

Hi dgozman@ - this hasn't been in any of the queries for M53 consideration since it's not yet marked as fixed.  Are you expecting any more code changes?

### dg...@chromium.org (2016-08-01)

I prefer to bake the fix in canary for a little longer. It's one of the non-obvious areas, where we'd better be more careful. We still have plenty of time for M53, and I don't want to merge this to M52.

### dg...@chromium.org (2016-08-08)

Requesting to merge https://chromium.googlesource.com/chromium/src.git/+/d5e6098dc2e984befc836f482845137245fa04e2 to M53.

### di...@chromium.org (2016-08-08)

Your change meets the bar and is auto-approved for M53 (branch: 2785)

### bu...@chromium.org (2016-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/956afd761251b3e5897165a5ea5434e84f0882fb

commit 956afd761251b3e5897165a5ea5434e84f0882fb
Author: Dmitry Gozman <dgozman@chromium.org>
Date: Mon Aug 08 17:13:39 2016

Merge to 2785 "[DevTools] Do not use "settings" query param."
> [DevTools] Do not use "settings" query param.
>
> Implemented the same functionality on embedder side.
> Also, sanitizing "settings" query param for remote frontends.
>
> BUG=618037
>
> Review-Url: https://codereview.chromium.org/2177983004
> Cr-Commit-Position: refs/heads/master@{#407666}
(cherry picked from commit d5e6098dc2e984befc836f482845137245fa04e2)
TBR=pfeldman

Review URL: https://codereview.chromium.org/2223093002 .

Cr-Commit-Position: refs/branch-heads/2785@{#529}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/956afd761251b3e5897165a5ea5434e84f0882fb/chrome/browser/devtools/devtools_window.cc
[modify] https://crrev.com/956afd761251b3e5897165a5ea5434e84f0882fb/chrome/browser/devtools/devtools_window.h
[modify] https://crrev.com/956afd761251b3e5897165a5ea5434e84f0882fb/content/shell/browser/layout_test/blink_test_controller.cc
[modify] https://crrev.com/956afd761251b3e5897165a5ea5434e84f0882fb/content/shell/browser/layout_test/layout_test_devtools_frontend.cc
[modify] https://crrev.com/956afd761251b3e5897165a5ea5434e84f0882fb/content/shell/browser/layout_test/layout_test_devtools_frontend.h
[modify] https://crrev.com/956afd761251b3e5897165a5ea5434e84f0882fb/content/shell/browser/shell_devtools_frontend.cc
[modify] https://crrev.com/956afd761251b3e5897165a5ea5434e84f0882fb/content/shell/browser/shell_devtools_frontend.h
[modify] https://crrev.com/956afd761251b3e5897165a5ea5434e84f0882fb/third_party/WebKit/Source/devtools/front_end/devtools.js
[modify] https://crrev.com/956afd761251b3e5897165a5ea5434e84f0882fb/third_party/WebKit/Source/devtools/front_end/main/Main.js


### dg...@chromium.org (2016-08-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

The panel has decided to award $1,000 for this bug, noting that it's more heavily mitigated than other related reports.  Many thanks as ever!

### gr...@gmail.com (2016-08-31)

Thanks :)

### aw...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lo...@gmail.com (2016-11-25)

Hi dgozman, your patch only filter the input from PC chrome, how to protect the mobile version?

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/618037?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084497)*
