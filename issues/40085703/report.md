# Security: Cross-origin object leak via fetch

| Field | Value |
|-------|-------|
| **Issue ID** | [40085703](https://issues.chromium.org/issues/40085703) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Reporter** | pi...@live.nl |
| **Assignee** | yu...@chromium.org |
| **Created** | 2016-10-15 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The promise returned by `fetch.call(crossOriginWindow)` is created in the cross-origin context. Direct cross-origin scripting is not possible because cross-origin function constructors don't work anymore (<https://crbug.com/chromium/541703>). But the attacker can e.g. call other functions of the cross-origin page.

**VERSION**  

Chrome Version: 56.0.2891.0 canary (64-bit). Does not reproduce in stable; the promise is generated in the correct context there. Possibly commit [1] might be the cause, but I'm not sure.  

Operating System: Windows 10

**REPRODUCTION CASE**  

See attachments. Save in the same directory, then open parent.html. The sandboxed child is able to call `Function.foo` of the parent page.

[1] <https://chromium.googlesource.com/chromium/src/+/afb9da1a91b0d1742a765b7a35f27e1be6645596>

## Attachments

- [parent.html](attachments/parent.html) (text/plain, 206 B)
- [child.html](attachments/child.html) (text/plain, 173 B)
- [parent.html](attachments/parent_53140324.html) (text/plain, 77 B)
- [child.html](attachments/child_53140325.html) (text/plain, 448 B)

## Timeline

### pi...@live.nl (2016-10-16)

In fact, I found a way to bypass the function constructor restrictions. That is, UXSS is possible. The trick is to create and resolve a promise, and call the function constructor in the `then` callback:

  var parent_Promise = fetch.call(parent).constructor;
  var parent_Function = parent_Promise.constructor;
  new parent_Promise(function(resolve) {
    resolve();
  }).then(function() {
    var f = new parent_Function("document.body.style.backgroundColor = 'red';");
    f();
  });

### mm...@chromium.org (2016-10-17)

Thanks for your report!

dcheng@, would you mind helping to triage this?

### dc...@chromium.org (2016-10-17)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-10-17)

Actually hmm, bisect-builds.py narrows this down to https://chromium.googlesource.com/chromium/src/+log/2ba53c9cf88833aabbb642e53de195fb150e28f0..d14e966090ffb39319f6baeb364426a00b5ede7b

There's a v8 roll which has https://chromium.googlesource.com/v8/v8/+/d008b9efcbddf299feefe7b420fd7e1601512ba5, so maybe jochen@ should be looking at this one.

### mm...@chromium.org (2016-10-18)

Thanks dcheng@!

[Monorail components: Blink>JavaScript]

### jo...@chromium.org (2016-10-18)

Thx for the report, the work-around for the function constructor check looks interesting, I'll investigate how to fix this.

Assigning back to yukishiino@ for using the wrong context in fetch

### jo...@chromium.org (2016-10-18)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>Bindings Blink>Network>FetchAPI]

### yu...@chromium.org (2016-10-18)

I've found that my CL mentioned caused this regression.  This is purely a binding issue, not related to Fetch API.

[Monorail components: -Blink>Network>FetchAPI]

### sh...@chromium.org (2016-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-18)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@chromium.org (2016-10-18)

Just FYI, I sent out a CL: http://crrev.com/2418413004

### sh...@chromium.org (2016-10-19)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9e04d69152b9c2ac7b4e395213c0e19c52e69bcc

commit 9e04d69152b9c2ac7b4e395213c0e19c52e69bcc
Author: yukishiino <yukishiino@chromium.org>
Date: Wed Oct 19 13:19:13 2016

binding: Creates a reject promise always in the current realm.

Regular promises are created in the relevant real of the context
object.  However, reject promises are special, they must be
created in the current realm as same as exceptions must be
created in the current realm.

BUG=656274

Review-Url: https://chromiumcodereview.appspot.com/2418413004
Cr-Commit-Position: refs/heads/master@{#426171}

[add] https://crrev.com/9e04d69152b9c2ac7b4e395213c0e19c52e69bcc/third_party/WebKit/LayoutTests/http/tests/security/promise-realm.html
[modify] https://crrev.com/9e04d69152b9c2ac7b4e395213c0e19c52e69bcc/third_party/WebKit/Source/bindings/core/v8/GeneratedCodeHelper.h
[modify] https://crrev.com/9e04d69152b9c2ac7b4e395213c0e19c52e69bcc/third_party/WebKit/Source/bindings/templates/methods.cpp.tmpl


### yu...@chromium.org (2016-10-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-19)

[Comment Deleted]

### aw...@chromium.org (2016-10-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-20)

[Empty comment from Monorail migration]

### yu...@chromium.org (2016-10-21)

I confirmed that the fix is working fine with Canary(precise64) Version 56.0.2896.3 unknown (64-bit).
Request a merge to M55.

### di...@chromium.org (2016-10-21)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### bu...@chromium.org (2016-10-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4152354ad141e5f759ee0d80a95b1a8bb49143e7

commit 4152354ad141e5f759ee0d80a95b1a8bb49143e7
Author: Yuki Shiino <yukishiino@chromium.org>
Date: Fri Oct 21 07:07:09 2016

binding: Creates a reject promise always in the current realm.

Regular promises are created in the relevant real of the context
object.  However, reject promises are special, they must be
created in the current realm as same as exceptions must be
created in the current realm.

BUG=656274

Review-Url: https://chromiumcodereview.appspot.com/2418413004
Cr-Commit-Position: refs/heads/master@{#426171}
(cherry picked from commit 9e04d69152b9c2ac7b4e395213c0e19c52e69bcc)

Review URL: https://codereview.chromium.org/2438253002 .

Cr-Commit-Position: refs/branch-heads/2883@{#227}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[add] https://crrev.com/4152354ad141e5f759ee0d80a95b1a8bb49143e7/third_party/WebKit/LayoutTests/http/tests/security/promise-realm.html
[modify] https://crrev.com/4152354ad141e5f759ee0d80a95b1a8bb49143e7/third_party/WebKit/Source/bindings/core/v8/GeneratedCodeHelper.h
[modify] https://crrev.com/4152354ad141e5f759ee0d80a95b1a8bb49143e7/third_party/WebKit/Source/bindings/templates/methods.cpp.tmpl


### aw...@chromium.org (2016-10-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-27)

Congratulations, the panel has awarded $5,000 for this report.  Many thanks!

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4152354ad141e5f759ee0d80a95b1a8bb49143e7

commit 4152354ad141e5f759ee0d80a95b1a8bb49143e7
Author: Yuki Shiino <yukishiino@chromium.org>
Date: Fri Oct 21 07:07:09 2016

binding: Creates a reject promise always in the current realm.

Regular promises are created in the relevant real of the context
object.  However, reject promises are special, they must be
created in the current realm as same as exceptions must be
created in the current realm.

BUG=656274

Review-Url: https://chromiumcodereview.appspot.com/2418413004
Cr-Commit-Position: refs/heads/master@{#426171}
(cherry picked from commit 9e04d69152b9c2ac7b4e395213c0e19c52e69bcc)

Review URL: https://codereview.chromium.org/2438253002 .

Cr-Commit-Position: refs/branch-heads/2883@{#227}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[add] https://crrev.com/4152354ad141e5f759ee0d80a95b1a8bb49143e7/third_party/WebKit/LayoutTests/http/tests/security/promise-realm.html
[modify] https://crrev.com/4152354ad141e5f759ee0d80a95b1a8bb49143e7/third_party/WebKit/Source/bindings/core/v8/GeneratedCodeHelper.h
[modify] https://crrev.com/4152354ad141e5f759ee0d80a95b1a8bb49143e7/third_party/WebKit/Source/bindings/templates/methods.cpp.tmpl


### aw...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### di...@google.com (2016-11-04)

[Automated comment] removing mislabelled merge-merged-2840

### di...@google.com (2016-11-04)

[Automated comment] removing mislabelled merge-merged-2840

### sh...@chromium.org (2017-01-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-01-25)

This issue was migrated from crbug.com/chromium/656274?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085703)*
