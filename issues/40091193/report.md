# CSP should always inherit same-origin opener's CSP

| Field | Value |
|-------|-------|
| **Issue ID** | [40091193](https://issues.chromium.org/issues/40091193) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zx...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2018-04-24 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36

Steps to reproduce the problem:
click http://182.254.247.127/1.php

1.php:
```
<?php
header("Content-Security-Policy: script-src 'unsafe-inline'");
?>
<script type="text/javascript">
    w = window.open("1.txt", "sss");

    setTimeout(function(){
        w.document.write("<script src='http://182.254.247.127/1.js'></scri"+"pt>");
    }, 1000);
</script>
```

What is the expected behavior?
CSP should block it, like Firefox does

What went wrong?
When open a file(like 1.txt, 1, 1.xxx ... etc) which can't generate CSP itself using window.open(), it should always inherits it's opener's CSP

Did this work before? N/A 

Chrome version: 66.0.3359.117  Channel: stable
OS Version: OS X 10.13.4
Flash Version: Shockwave Flash 29.0 r0

## Timeline

### el...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### zx...@gmail.com (2018-04-25)

What's more, if open a file not exists using window.open, this is still effective.

### zx...@gmail.com (2018-04-25)

And I think this is not only about CSP, maybe about your security-context's inherits in same-origin, but CSP is the one affected the most, I can say CSP totally broken in Chrome, because if CSP initializing by file itself(.php header(), .html meta etc...), static file like .txt .js can't initialize CSP itself, if CSP initializing by http server's header mod(for example, Nginx's add_header), it will not affect 404 page.

### jo...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-04-26)

> What's more, if open a file not exists using window.open, this is still effective.

Can you please be precise about what exactly you mean here? Are you just saying "If your server serves a 404 page without a CSP directive, it is vulnerable"?

The general concern about "CSP headers are often forgotten for error pages and non-active content" is the motivating notion behind Origin Policy: https://wicg.github.io/origin-policy/.

If your "protected" page's CSP allows unsafe-inline to start with, it's not really going to provide much protection.

https://w3c.github.io/webappsec-csp/#initialize-document-csp notes that if a document comes from a local scheme and has an "opener browser context" its CSP should be applied to the openee, noting "Note: We do all this to ensure that a page cannot bypass its policy by embedding a frame or popping up a new window containing content it controls (blob: resources, or document.write())" but that does not protect against an attack whereby you document.write into a frame with a non-local scheme.

### zx...@gmail.com (2018-04-27)

> Can you please be precise about what exactly you mean here? Are you just saying "If your server serves a 404 page without a CSP directive, it is vulnerable"?

Yes, you are right, 404 page without CSP leads to totally bypass of CSP in unsafe-inline mod.

> The general concern about "CSP headers are often forgotten for error pages and non-active content" is the motivating notion behind Origin Policy

That's the point, first let's assume that CSP never exist in 404 page, then consider the following scenario:

An attacker find a XSS in `a.com/index.php` which CSP is `default-src 'none';script-src 'unsafe-inline';` but he want to steal cookie in `a.com/admin/index.php`, the cookie set `path=/admin` so he can't get the cookie in /index.php directly

Then he want to use a iframe set src to /admin/index.php to get the cookie, but it's restrict by CSP default-src 'none'.
But with 404 page without CSP he can complete the attack using window.open() in Chrome, I make an online demo in http://182.254.247.127/index.php

This attack failed in Firefox because Firefox set openee's security origin same to opener's when document.write, so I think this is not only a problem about CSP.

### el...@chromium.org (2018-05-04)

I believe this is basically dupe of https://crbug.com/chromium/764518 and https://crbug.com/chromium/751996

### zx...@gmail.com (2018-08-03)

[Comment Deleted]

### bu...@chromium.org (2018-11-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/108147dfd1ea159fd3632ef92ccc4ab8952980c7

commit 108147dfd1ea159fd3632ef92ccc4ab8952980c7
Author: Andy Paicu <andypaicu@chromium.org>
Date: Mon Nov 26 15:34:25 2018

Inherit the navigation initiator when navigating instead of the parent/opener

Spec PR: https://github.com/w3c/webappsec-csp/pull/358

Bug: 905301, 894228, 836148
Change-Id: I43ada2266d42d1cd56dbe3c6dd89d115e878a83a
Reviewed-on: https://chromium-review.googlesource.com/c/1314633
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#610850}
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/dom/document.h
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/dom/document_init.cc
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/dom/document_init.h
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/frame/csp/content_security_policy.cc
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/renderer/core/loader/frame_loader.h
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-in-child-frame-self-navigate-inherits.sub.html
[rename] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-in-main-window-self-navigate-inherits.sub.html
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-blob-scheme.html
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-blob-scheme.html.sub.headers
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-data-scheme.html
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-data-scheme.html.sub.headers
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-blob-scheme.html
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-blob-scheme.html.sub.headers
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-data-scheme.html
[add] https://crrev.com/108147dfd1ea159fd3632ef92ccc4ab8952980c7/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-data-scheme.html.sub.headers


### an...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-11-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d72a833dad8deabbf0e49ef16073542142db88a6

commit d72a833dad8deabbf0e49ef16073542142db88a6
Author: Mounir Lamouri <mlamouri@chromium.org>
Date: Mon Nov 26 20:19:56 2018

Revert "Inherit the navigation initiator when navigating instead of the parent/opener"

This reverts commit 108147dfd1ea159fd3632ef92ccc4ab8952980c7.

Reason for revert:
FindIt suggests a 74% chance that this is the cause of the following issues:
https://ci.chromium.org/buildbot/chromium.webkit/WebKit%20Linux%20Trusty%20Leak/26833

Original change's description:
> Inherit the navigation initiator when navigating instead of the parent/opener
> 
> Spec PR: https://github.com/w3c/webappsec-csp/pull/358
> 
> Bug: 905301, 894228, 836148
> Change-Id: I43ada2266d42d1cd56dbe3c6dd89d115e878a83a
> Reviewed-on: https://chromium-review.googlesource.com/c/1314633
> Commit-Queue: Andy Paicu <andypaicu@chromium.org>
> Reviewed-by: Mike West <mkwst@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#610850}

TBR=mkwst@chromium.org,andypaicu@chromium.org

Change-Id: If3ccf72cf8a4285926429f2855f32c1b0c606c5b
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 905301, 894228, 836148
Reviewed-on: https://chromium-review.googlesource.com/c/1351285
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Commit-Queue: Mounir Lamouri <mlamouri@chromium.org>
Cr-Commit-Position: refs/heads/master@{#610930}
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/dom/document.h
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/dom/document_init.cc
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/dom/document_init.h
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/frame/csp/content_security_policy.cc
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/renderer/core/loader/frame_loader.h
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-in-child-frame-self-navigate-inherits.sub.html
[rename] https://crrev.com/d72a833dad8deabbf0e49ef16073542142db88a6/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-self-navigate-inherits.sub.html
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-blob-scheme.html
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-blob-scheme.html.sub.headers
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-data-scheme.html
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-data-scheme.html.sub.headers
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-blob-scheme.html
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-blob-scheme.html.sub.headers
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-data-scheme.html
[delete] https://crrev.com/081fd44ad92323c8562b7f952f7eef8a61232505/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-data-scheme.html.sub.headers


### aw...@chromium.org (2018-11-27)

[Empty comment from Monorail migration]

### an...@chromium.org (2018-11-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/29c42edb32d7e6825ea1d06a7d097668382dd91c

commit 29c42edb32d7e6825ea1d06a7d097668382dd91c
Author: Andy Paicu <andypaicu@chromium.org>
Date: Tue Dec 04 12:29:42 2018

Rework of "inherit the navigation initiator when navigating"

Spec: https://w3c.github.io/webappsec-csp/#initialize-document-csp

This is a rework and reland of https://chromium-review.googlesource.com/c/chromium/src/+/1314633

The initial patch got reverted because it did not pass the trusty leak
build checks. The issue was that holding to the initiator document as a
member in FrameLoader was holding said document alive unreasonably long.
Instead this rework holds a copy of the initiator's CSP.

Bug: 905301, 894228, 836148
Change-Id: Ic12c28d20c53def5d6753449c3c4da7de5242ca2
Reviewed-on: https://chromium-review.googlesource.com/c/1353978
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#613521}
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/dom/document.h
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/dom/document_init.cc
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/dom/document_init.h
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/frame/csp/content_security_policy.cc
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/renderer/core/loader/frame_loader.h
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-in-child-frame-self-navigate-inherits.sub.html
[rename] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-in-main-window-self-navigate-inherits.sub.html
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-blob-scheme.html
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-blob-scheme.html.sub.headers
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-data-scheme.html
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/sandboxed-data-scheme.html.sub.headers
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-blob-scheme.html
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-blob-scheme.html.sub.headers
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-data-scheme.html
[add] https://crrev.com/29c42edb32d7e6825ea1d06a7d097668382dd91c/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/unsandboxed-data-scheme.html.sub.headers


### an...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2018-12-20)

Thank you for your report, the Panel has decided to reward $500 this report. 

### na...@google.com (2018-12-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-03-12)

This issue was migrated from crbug.com/chromium/836148?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091193)*
