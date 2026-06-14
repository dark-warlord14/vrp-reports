# <a ping="..."> should be covered by connect-src CSP directive

| Field | Value |
|-------|-------|
| **Issue ID** | [40085892](https://issues.chromium.org/issues/40085892) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature |
| **Reporter** | lu...@chromium.org |
| **Assignee** | lu...@chromium.org |
| **Created** | 2016-11-07 |
| **Bounty** | $500.00 |

## Description

REPRO (layout test):

<html>
<head>
<meta http-equiv="Content-Security-Policy" content="connect-src http://127.0.0.1:8000">
<script>
if (window.testRunner) {
  testRunner.overridePreference("WebKitHyperlinkAuditingEnabled", 1);
  testRunner.dumpAsText();
  testRunner.waitUntilDone();
}
function onload() {
  if (window.testRunner) {
    anchor = document.getElementById('anchor');
    anchor.click();
  }
}
</script>
</head>
<body onload="onload();">
  <p>
    Tests whether "ping" attribute of an &lt;at&gt; / "anchor" tag is subject
    to CSP enforcement (via 'connect-src').
  </p>
  <p>
    <a href="/resources/notify-done.html"
       ping="https://localhost:8443/resources/dummy.txt"
       id="anchor"
       >Link</a>
  </p>
</body>
</html>


EXPECTED BEHAVIOR: ping is blocked by connect-src

ACTUAL BEHAVIOR: ping is not blocked

## Timeline

### lu...@chromium.org (2016-11-07)

I've proposed a fix at https://crrev.com/2483903003

### np...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### sh...@chromium.org (2016-11-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3678dd47cb4ccb61fa4281dfdcc5b92adc6c21de

commit 3678dd47cb4ccb61fa4281dfdcc5b92adc6c21de
Author: lukasza <lukasza@chromium.org>
Date: Tue Nov 08 16:24:06 2016

<a ping="..."> should be covered by connect-src CSP directive.

BUG=663048

Review-Url: https://codereview.chromium.org/2483903003
Cr-Commit-Position: refs/heads/master@{#430629}

[add] https://crrev.com/3678dd47cb4ccb61fa4281dfdcc5b92adc6c21de/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/connect-src-anchor-ping-expected.txt
[add] https://crrev.com/3678dd47cb4ccb61fa4281dfdcc5b92adc6c21de/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/connect-src-anchor-ping.html
[modify] https://crrev.com/3678dd47cb4ccb61fa4281dfdcc5b92adc6c21de/third_party/WebKit/Source/core/loader/PingLoader.cpp


### lu...@chromium.org (2016-11-08)

I plan to request a merge after a few days of bake time on Canary.  There is some risk that the new CSP blocking will start blocking something important or unintended, but that risk should be mitigated (IMO) by still having ~3 weeks of bake time on M55/Beta branch before it becomes the Stable branch.

### sh...@chromium.org (2016-11-09)

[Empty comment from Monorail migration]

### lu...@chromium.org (2016-11-10)

The fix from https://crbug.com/chromium/663048#c5 was initially included in 56.0.2914.0, so we probably want a few more days on the Canary channel before requesting a merge to Beta.

I think the merge to Beta should be relatively safe - blocked a.ping requests are unlikely to be end-user visible.

### lu...@chromium.org (2016-11-14)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-11-14)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### bu...@chromium.org (2016-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3609fbe23fd52b425d28c73ec678616f2cf3af39

commit 3609fbe23fd52b425d28c73ec678616f2cf3af39
Author: Lukasz Anforowicz <lukasza@chromium.org>
Date: Mon Nov 14 17:59:10 2016

<a ping="..."> should be covered by connect-src CSP directive.

BUG=663048

Review-Url: https://codereview.chromium.org/2483903003
Cr-Commit-Position: refs/heads/master@{#430629}
(cherry picked from commit 3678dd47cb4ccb61fa4281dfdcc5b92adc6c21de)

Review URL: https://codereview.chromium.org/2500023002 .

Cr-Commit-Position: refs/branch-heads/2883@{#560}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[add] https://crrev.com/3609fbe23fd52b425d28c73ec678616f2cf3af39/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/connect-src-anchor-ping-expected.txt
[add] https://crrev.com/3609fbe23fd52b425d28c73ec678616f2cf3af39/third_party/WebKit/LayoutTests/http/tests/security/contentSecurityPolicy/connect-src-anchor-ping.html
[modify] https://crrev.com/3609fbe23fd52b425d28c73ec678616f2cf3af39/third_party/WebKit/Source/core/loader/PingLoader.cpp


### aw...@chromium.org (2016-11-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-06)

Adding reward-topanel since this was spun out of externally reported https://crbug.com/chromium/661126

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-13)

Thanks for the report! Our panel decided to award $500 for this report.  A member of our finance team will be in touch shortly to arrange payment.

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-02-15)

This issue was migrated from crbug.com/chromium/663048?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/661126]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085892)*
