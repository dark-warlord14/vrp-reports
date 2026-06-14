# Restricted web APIs can easily be accessed from Chrome apps

| Field | Value |
|-------|-------|
| **Issue ID** | [40083654](https://issues.chromium.org/issues/40083654) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Apps, Platform>Apps>API |
| **CVE IDs** | CVE-2016-1638 |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | rd...@chromium.org |
| **Created** | 2016-02-09 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version: 48.0.2564.103 (stable, and earlier) and 50.0.2633.0 (HEAD)

Some web platform APIs are disabled in Chrome apps for security reasons (https://developer.chrome.com/apps/app_deprecated). This is implemented in platform_app.js [1].

These restrictions can be bypassed:
(I) The restriction of document.open/write/writeln/close is implemented by shadowing HTMLDocument.prototype.write, but Document.prototype.write should be shadowed instead.
  So, either of the following two ways allows the use of the restricted API:
  delete HTMLDocument.prototype.write;
  Document.prototype.write.call(document);

(II) window.onbeforeunload is shadowed by Object.defineProperty with configurable:true. This allows the property descriptor to be removed via the delete operator:
  delete window.onbeforeunload; // Remove restriction
  window.onbeforeunload = function() {
    return 'This should not be visible!';
  };

PoC for I: See https://crbug.com/chromium/585268 (document.write/close was used for that exploit).

PoC for II:
1. Download manifest.json and background.js
2. Load the app (either via chrome://extensions, or by uploading it to the Chrome Web Store and installing it).
3. The app uses the above trick, and then calls location.reload() to show a PoC.

Expected result: "window.onbeforeunload is not available in packaged apps." error in console.
Actual result  : Upon unload, a dialog shows up.


[1] https://chromium.googlesource.com/chromium/src/+/a9914da1b0b8710b2f500c735e29953c3e56db97/extensions/renderer/resources/platform_app.js


## Attachments

- [manifest.json](attachments/manifest.json) (application/json, 158 B)
- [unexpected-forbidden-dialog.png](attachments/unexpected-forbidden-dialog.png) (image/png, 8.8 KB)
- [background.js](attachments/background.js) (text/javascript, 411 B)

## Timeline

### ri...@chromium.org (2016-02-10)

Thanks for the detailed report!

Mind taking a look at this, jochen@ and haraken@? I'm not so familiar with this code, so can someone comment on the severity of bypassing these?

### ri...@chromium.org (2016-02-10)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-02-10)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-02-10)

Here is yet another way to bypass the beforeunload/unload restrictions:
platform_app.js disables "unload" and "beforeunload" in addEventListener by checking whether the first argument is strictly equal (===) to these event names.
This can be bypassed by passing an object that serializes to "unload" or "beforeunload", e.g. by constructing a string as follows:

   addEventListener(new String('beforeunload'), function(event) {
      event.returnValue = 'This is visible when the app page unloads';
   });


Regarding severity:
- unload/beforeunload: Modal dialogs (alert/confirm/prompt/..) are normally blocked. With this vulnerability, attackers can create modal dialogs that are not attributed to the Chrome app, and put any text in the message box (simply create a child frame and reload it). Here is a recent bug that recognizes beforeunload as a phishing vector: https://crbug.com/chromium/579113.
Another aspect is that modal dialogs enable nested message loops, which is risky (especially if Chrome apps are designed to not expect modal dialogs).

- document.write APIs: Can be used to reset the document. In https://crbug.com/chromium/585268, we saw that Chrome is not prepared to handle this, which resulted in a high-severity UAF (there were other ways to exploit that bug, but using document.write certainly had the highest impact).

Because of this, I think that this bug matches "Bugs that are not harmful independently, but can be combined with other bugs to cause harm." -- https://www.chromium.org/developers/severity-guidelines#TOC-Medium-Severity -> Medium.

### ri...@chromium.org (2016-02-11)

Makes sense, thanks for your help!

### cl...@chromium.org (2016-02-11)

[Empty comment from Monorail migration]

### ri...@chromium.org (2016-02-11)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-02-15)

ugh, this code makes me sad.

rdevlin.cronin@ does your kingdom include platform apps now?

### rd...@chromium.org (2016-02-16)

Oh probably. :)

It's easy enough to patch these particular issues - disable the methods on Document instead of HTMLDocument, don't do strict comparisons for onunload and related, remove the configurable, etc.  The underlying problem though is that we're trying to mangle things in JS that really should fundamentally be guaranteed at a lower level (probably somewhere in blink).  Unfortunately, I don't know the best way to begin going about that (or if it's even necessarily something we really want to do), and don't personally have time to implement it at the moment.

If anyone knows a way that this is already done in blink (or content/, or v8), lemme know - in the meantime, I'll go ahead and make these fixes to at least harden our security a little bit.

### bu...@chromium.org (2016-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dc42ae208c2744f7fb144b2e396358a1fc34db87

commit dc42ae208c2744f7fb144b2e396358a1fc34db87
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Mon Feb 22 20:09:24 2016

[Extensions] Update web API cloberring for platform apps

Platform App clobbering for certain Web APIs was incomplete.  Make it more
complete.  See bug for more details.

BUG=585282

Review URL: https://codereview.chromium.org/1716513002

Cr-Commit-Position: refs/heads/master@{#376784}

[add] https://crrev.com/dc42ae208c2744f7fb144b2e396358a1fc34db87/chrome/browser/extensions/app_window_overrides_browsertest.cc
[modify] https://crrev.com/dc42ae208c2744f7fb144b2e396358a1fc34db87/chrome/chrome_tests.gypi
[add] https://crrev.com/dc42ae208c2744f7fb144b2e396358a1fc34db87/chrome/test/data/extensions/app_forbidden_apis/document_apis/background.js
[add] https://crrev.com/dc42ae208c2744f7fb144b2e396358a1fc34db87/chrome/test/data/extensions/app_forbidden_apis/document_apis/manifest.json
[add] https://crrev.com/dc42ae208c2744f7fb144b2e396358a1fc34db87/chrome/test/data/extensions/app_forbidden_apis/onbeforeunload/background.js
[add] https://crrev.com/dc42ae208c2744f7fb144b2e396358a1fc34db87/chrome/test/data/extensions/app_forbidden_apis/onbeforeunload/manifest.json
[modify] https://crrev.com/dc42ae208c2744f7fb144b2e396358a1fc34db87/chrome/test/data/extensions/platform_apps/restrictions/main.js
[modify] https://crrev.com/dc42ae208c2744f7fb144b2e396358a1fc34db87/extensions/renderer/resources/platform_app.js


### ro...@robwu.nl (2016-02-26)

Can this patch go with the first 49 stable release?

### ti...@google.com (2016-02-26)

[Automated comment] Less than 2 weeks to go before stable on M49, manual review required.

### ss...@google.com (2016-02-26)

Merge approved for M49 (branch 2623)

### bu...@chromium.org (2016-02-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8e79fe67a8b03291c6acac311ed4ca6592798b6f

commit 8e79fe67a8b03291c6acac311ed4ca6592798b6f
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Fri Feb 26 20:08:10 2016

[Extensions] Update web API cloberring for platform apps

Platform App clobbering for certain Web APIs was incomplete.  Make it more
complete.  See bug for more details.

BUG=585282

Review URL: https://codereview.chromium.org/1716513002

Cr-Commit-Position: refs/heads/master@{#376784}
(cherry picked from commit dc42ae208c2744f7fb144b2e396358a1fc34db87)

Review URL: https://codereview.chromium.org/1744623002 .

Cr-Commit-Position: refs/branch-heads/2623@{#523}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[add] https://crrev.com/8e79fe67a8b03291c6acac311ed4ca6592798b6f/chrome/browser/extensions/app_window_overrides_browsertest.cc
[modify] https://crrev.com/8e79fe67a8b03291c6acac311ed4ca6592798b6f/chrome/chrome_tests.gypi
[add] https://crrev.com/8e79fe67a8b03291c6acac311ed4ca6592798b6f/chrome/test/data/extensions/app_forbidden_apis/document_apis/background.js
[add] https://crrev.com/8e79fe67a8b03291c6acac311ed4ca6592798b6f/chrome/test/data/extensions/app_forbidden_apis/document_apis/manifest.json
[add] https://crrev.com/8e79fe67a8b03291c6acac311ed4ca6592798b6f/chrome/test/data/extensions/app_forbidden_apis/onbeforeunload/background.js
[add] https://crrev.com/8e79fe67a8b03291c6acac311ed4ca6592798b6f/chrome/test/data/extensions/app_forbidden_apis/onbeforeunload/manifest.json
[modify] https://crrev.com/8e79fe67a8b03291c6acac311ed4ca6592798b6f/chrome/test/data/extensions/platform_apps/restrictions/main.js
[modify] https://crrev.com/8e79fe67a8b03291c6acac311ed4ca6592798b6f/extensions/renderer/resources/platform_app.js


### bu...@chromium.org (2016-02-29)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/8e79fe67a8b03291c6acac311ed4ca6592798b6f

commit 8e79fe67a8b03291c6acac311ed4ca6592798b6f
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Fri Feb 26 20:08:10 2016


### ti...@google.com (2016-02-29)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-29)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-02)

Congrats Rob - $1000 for this report. CVE-ID to follow.

### ti...@google.com (2016-03-02)

CVE-2016-1638

### cl...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/585282?no_tracker_redirect=1

[Multiple monorail components: Platform>Apps, Platform>Apps>API]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083654)*
