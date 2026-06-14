# Cross-Directory Shared Worker

| Field | Value |
|-------|-------|
| **Issue ID** | [40089832](https://issues.chromium.org/issues/40089832) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Workers |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | nh...@chromium.org |
| **Created** | 2017-12-07 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36
Platform: 10176.5.0

Steps to reproduce the problem:
1. Place attached HTML file in different directory (e.g. Desktop and Documents)
2. Open both files in different tabs

What is the expected behavior?
Shared Worker does not establish.

What went wrong?
Chrome treats different directories as cross-origin. But Shared Worker doesn't follow this way.

Did this work before? N/A 

Chrome version: 64.0.3282.11  Channel: dev
OS Version: 
Flash Version:

## Attachments

- [test.html](attachments/test.html) (text/plain, 6.3 KB)

## Timeline

### ke...@chromium.org (2017-12-08)

I see User agent: Intel Mac OS X 10_13_1

Can you please confirm if this bug is Chrome OS specific or if it reproduced on macOS as well?

### s....@gmail.com (2017-12-08)

For dev build, only Chrome OS. But you can test in Canary for any other OS. You just need to make sire that your build has patch of https://bugs.chromium.org/p/chromium/issues/detail?id=787103

### sh...@chromium.org (2017-12-08)

Thank you for providing more feedback. Adding requester "kerrnel@chromium.org" to the cc list and removing "Needs-Feedback" label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2017-12-08)

nhiroki@, can you PTAL?

### ke...@chromium.org (2017-12-08)

Assuming this report is correct, I'll assign it the same severity as 787103.

[Monorail components: Blink>Workers]

### sh...@chromium.org (2017-12-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-12-10)

[Empty comment from Monorail migration]

### nh...@chromium.org (2017-12-11)

I'll investigate this.

### nh...@chromium.org (2017-12-11)

CC: falken@ and kinuko@ for visibility.

### nh...@chromium.org (2017-12-11)

https://crbug.com/chromium/455882 looks relevant (falken@, thank you letting me know this issue!)

According to the issue, "file://" URLs should have opaque origins and never communicate with each other regardless of directory (CC: dcheng@ who is the owner of that issue).

### nh...@chromium.org (2017-12-11)

^^^ +dcheng@ for c#11

### nh...@chromium.org (2017-12-11)

FYI: I heard mkwst@ is trying to make file:// handling more interoperable:
https://github.com/whatwg/html/issues/3099

### nh...@chromium.org (2017-12-11)

My plan:
1) Check the behavior before my fix (see c#2) and make the current impl aligned with it for M64 merge if it's reasonable.
2) Fix the behavior based on the discussion (see c#13) in a separate crbug issue.

### nh...@chromium.org (2017-12-11)

Hm... apparently url::Origin::Create() doesn't parse file:// as a unique origin. Is this intended?

https://chromium.googlesource.com/chromium/src/+/f5505f4d5057f7315ea9d9229c28060c057d878c/url/origin_unittest.cc#139

### nh...@chromium.org (2017-12-11)

Looks like this is not a recent regression.

I created layout tests[1] for following cases:

1) create 2 shared workers from the same script URL on file:// URL document, and make sure they are separate.
2) in addition to 1), create a shared worker from the same script URL on another file:// document in a different directory, and make sure they are separate instances.

Then, I ran these tests on Chrome 63 with "--allow-file-access-from-files" and confirmed the workers are unexpectedly shared among them.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/818365

### s....@gmail.com (2017-12-11)

FYI, Chrome doesn't allow SharedWorker in opaque origins. Tested with data URL as well as CSP sandbox without allow-same-origin.

### mk...@chromium.org (2017-12-11)

> apparently url::Origin::Create() doesn't parse file:// as a unique origin

`file:` URLs are currently sitting somewhere between being completely opaque, and having a real origin. I would very much like for that not to be the case anymore, hence the discussion in https://github.com/whatwg/html/issues/3099.

Still, given that we treat `file:` as an opaque origin in a document context (e.g. `window.origin` returns `null` for `file:///whatever/`), we should be failing the origin check in step 11.2 of https://html.spec.whatwg.org/#dom-sharedworker, preventing reuse, so our behavior is incorrect.

### s....@gmail.com (2017-12-11)

See https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/workers/SharedWorker.cpp?l=71

 if (!document->GetSecurityOrigin()->CanAccessSharedWorkers()) {
    exception_state.ThrowSecurityError(
        "Access to shared workers is denied to origin '" +
        document->GetSecurityOrigin()->ToString() + "'.");
    return nullptr;
  }

https://cs.chromium.org/chromium/src/third_party/WebKit/Source/platform/weborigin/SecurityOrigin.h?l=176

bool CanAccessSharedWorkers() const { return !IsUnique(); }

https://cs.chromium.org/chromium/src/third_party/WebKit/Source/platform/weborigin/SecurityOrigin.h?l=199

// The origin is a globally unique identifier assigned when the Document is
  // created. http://www.whatwg.org/specs/web-apps/current-work/#sandboxOrigin
  //
  // There's a subtle difference between a unique origin and an origin that
  // has the SandboxOrigin flag set. The latter implies the former, and, in
  // addition, the SandboxOrigin flag is inherited by iframes.
  bool IsUnique() const { return is_unique_; }


Comment is talking about sandbox origin but check is for opaque origin.

### pa...@chromium.org (2017-12-11)

[Empty comment from Monorail migration]

### dc...@chromium.org (2017-12-11)

I think part of the problem is that how file:// URLs are processed is not well documented enough, and that's leading to a lot of confusion elsewhere in the code.

As mkwst@ said, the problem is file:// origins are only 'mostly' opaque today: we don't actually parse them as opaque origins. We remember the scheme and such, and don't mark the opaque bit.

However, when we do access checks or serialize the origin to a string, we treat the origin as if it were opaque (mostly, depending on the settings).

mkwst@, do you think it'd break a lot of things to just change origin creation so it creates an opaque origin in the ctor if legacy behavior isn't enabled (i.e. for android WebView)? That seems like the simplest fix in the long-term. A short-term fix would involve a manual check for IsLocal() and having shared worker treat that as opaque. =(

### nh...@chromium.org (2017-12-14)

If it's not feasible to make file:// origins opaque soon, I'll work on the short-term fix dcheng@ suggested.

### mk...@chromium.org (2017-12-14)

Based on usage numbers overall (4% of navigations on Windows!?!), I don't think we're going to be able to make quick changes to `file://`. I'm adding metrics to see how far we can get in https://crbug.com/794098.

### bu...@chromium.org (2018-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29

commit 8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29
Author: Hiroki Nakagawa <nhiroki@chromium.org>
Date: Wed Jan 10 14:52:03 2018

SharedWorker: Treat worker script on file:// URLs as opaque origins

After this CL, shared workers treat worker scripts on file:// URLs as
if they have opaque origins.

In addition, this CL...

- adds fast/workers/shared-worker-file-url.html for testing file:// URLs,
- moves layout tests that no longer run on file:// from fast/workers/ to
  http/tests/, and
- makes some browser tests run on http:// environment instead of file://
  environment.

Bug: 793074
Change-Id: I61b3410245a5fb51701bdf2ec31c61aeae57a3b9
Reviewed-on: https://chromium-review.googlesource.com/818365
Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#528311}
[modify] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/content/browser/shared_worker/shared_worker_instance.cc
[modify] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/content/browser/shared_worker/shared_worker_instance_unittest.cc
[modify] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/content/browser/shared_worker/worker_browsertest.cc
[add] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/fast/workers/resources/shared-worker-file-url-window.html
[add] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/fast/workers/resources/shared-worker-file-url-worker.js
[add] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/fast/workers/shared-worker-file-url.html
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/resources/create-shared-worker-frame.html
[add] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/resources/shared-worker-common.js
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/resources/shared-worker-count-connections.js
[add] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/resources/shared-worker-create-common.js
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/resources/shared-worker-iframe.html
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/resources/shared-worker-lifecycle.js
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/resources/shared-worker-name.js
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/shared-worker-in-iframe-expected.txt
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/shared-worker-in-iframe.html
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/shared-worker-lifecycle-expected.txt
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/shared-worker-lifecycle.html
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/shared-worker-name-expected.txt
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/shared-worker-name.html
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/shared-worker-shared-expected.txt
[rename] https://crrev.com/8ec63cd6d0aaf1b5be1ded592d0d7b5263d31a29/third_party/WebKit/LayoutTests/http/tests/workers/shared-worker-shared.html


### nh...@chromium.org (2018-01-17)

[Empty comment from Monorail migration]

### nh...@chromium.org (2018-01-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-17)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-29)

Thanks for the report!  The VRP panel looked at this, and concluded that it would likely not be of much use to an attacker, I'm afraid.

### s....@gmail.com (2018-01-29)

Yup, I agree. Thanks for the reward!

### aw...@chromium.org (2018-01-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-09)

This bug requires manual review: M65 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-09)

[Bulk Edit]

+awhalley@ (Security TPM) for M65 merge review

### aw...@google.com (2018-02-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/793074?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089832)*
