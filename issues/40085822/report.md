# expose() leaks privateClass via Object[@@hasInstance]

| Field | Value |
|-------|-------|
| **Issue ID** | [40085822](https://issues.chromium.org/issues/40085822) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ja...@googlemail.com |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-10-29 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36

Steps to reproduce the problem:
Steps:
1. ensure that there are no extensions installed that inject content scripts into google.com
2. unpack and install test-victim-extension.zip
3. open hijack.html in a new tab
4. click the link in hijack.html
5. wait a bit

What is the expected behavior?

What went wrong?
You should see a notification popup, created by the background script of the test extension in response to a message it received over the port that was opened by the content script.

The issue is the following line in the implementation of utils.expose():

    DCHECK(!(privateClass.prototype instanceof $Object.self));

`privateClass.prototype` is an object that unprivileged code should not be allowed to access, `$Object.self` is the global `Object`. This is buggy because, since ECMAScript 6, the `instanceof` operator performs the following steps (see <http://www.ecma-international.org/ecma-262/7.0/index.html#sec-instanceofoperator>):

1. If Type(C) is not Object, throw a TypeError exception.
2. Let instOfHandler be ? GetMethod(C, @@hasInstance).
3. If instOfHandler is not undefined, then Return ToBoolean(? Call(instOfHandler, C, « O »)).
[...]

In other words, `Object[Symbol.hasInstance](privateClass.prototype)` will be invoked if `Object[Symbol.hasInstance]` isn't `undefined`, meaning that by setting this property, `privateClass.prototype` can be leaked:

    // leak PortImpl
    Object.defineProperty(Object, Symbol.hasInstance, {value: function(obj){
      if (obj.constructor.name === 'PortImpl') {
        window.PortImpl = obj.constructor;
      }
    }});
    chrome.runtime; /* trigger lazy load of extensions::messaging */

Did this work before? N/A 

Chrome version: 54.0.2840.71  Channel: stable
OS Version: 
Flash Version: 

This is a slightly different vector with more or less the same impact as https://crbug.com/chromium/609569.

Introduced in <https://chromium.googlesource.com/chromium/src/+/931719c51866a7c2e272114517cc52aa6581adff>.

It might make sense to assign (or CC) rob@robwu.nl on this bug.

From a quick look, I can't find any way to actually abuse this on the dev channel - port IDs are now translated (and implicitly checked) in the renderer. However, in stable, it still works.

## Timeline

### ta...@google.com (2016-10-31)

rob@ and devlin@, I wonder if you could take a look at this. Thanks.

### ta...@google.com (2016-10-31)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions]

### ta...@google.com (2016-10-31)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-10-31)

Heh. Initially I did set the prototype of the private constructors to null, but changed it after review. After all hardening in the extension system a few months ago, I don't think that there is any exploitable security issue here, is it? Are you able to use this weakness to do anything unusual?

We could remove the DCHECK, null all constructors or do nothing.
Given that the JS bindings will disappear (https://crbug.com/chromium/653596) and there is no exploitable condition here, I think that the first or third option is the best. At this point it does not make sense to invest much more time in the JS bindings since they're gone soon anyway.

Devlin, WDYT?

### ja...@googlemail.com (2016-10-31)

> Are you able to use this weakness to do anything unusual?

Not in the dev channel, as far as I can tell - only in the stable channel, to hijack ports of extension scripts.

> Given that the JS bindings will disappear (https://crbug.com/chromium/653596)

Woohoo, awesome! :)

> and there is no exploitable condition here

Well, on the stable channel, there is.

> , I think that the first or third option is the best

I agree, removing the DCHECK for now is probably fine.

### sh...@chromium.org (2016-11-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-01)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-11-02)

The DCHECK is not useful on release channels, and the usefulness for development are limited, so I'll just remove the DCHECK. It will be safe to merge since it was supposed to be no-op on release channels anyway.

https://codereview.chromium.org/2474623002/

### rd...@chromium.org (2016-11-02)

@4, sorry for the delay.  Removing the DCHECK here sounds fine given the limited usefulness and lack of exploitable attack here.

### bu...@chromium.org (2016-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0d9edd7b2524090fb0a0461e7bd9e5caa1e8a36d

commit 0d9edd7b2524090fb0a0461e7bd9e5caa1e8a36d
Author: rob <rob@robwu.nl>
Date: Thu Nov 03 00:40:16 2016

[extension bindings] Remove leak of internal class

BUG=660678

Review-Url: https://codereview.chromium.org/2474623002
Cr-Commit-Position: refs/heads/master@{#429482}

[modify] https://crrev.com/0d9edd7b2524090fb0a0461e7bd9e5caa1e8a36d/extensions/renderer/resources/utils.js


### ro...@robwu.nl (2016-11-03)

Requesting merge of the above patch to M55 and M54. The patch is trivial (removing a debug assertion that is not enabled in release builds), so there is no risk of breaking anything.

### sh...@chromium.org (2016-11-03)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-11-03)

+ awhalley@ for merge review

### aw...@chromium.org (2016-11-03)

I agree the patch is trivial, but there's time to follow bake times for M55, so will give it a couple of days.  There are no plans to spin M54 at this point and we wouldn't spin just for this change, but keep the label on so we can consider it if we do.

### li...@chromium.org (2016-11-03)

For M54, we are planning a respin to ship a critical fix for Enterprise support, https://bugs.chromium.org/p/chromium/issues/detail?id=658606.

Richard could you please comment on the respin plans.

### di...@chromium.org (2016-11-03)

[Automated comment] Request affecting a post-stable build (M54), manual review required.

### di...@chromium.org (2016-11-03)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### di...@chromium.org (2016-11-04)

[Automated comment] Request affecting a post-stable build (M54), manual review required.

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-11-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/201becf497377723fb9ec92bb8dcc0cf4f164ca1

commit 201becf497377723fb9ec92bb8dcc0cf4f164ca1
Author: Rob Wu <rob@robwu.nl>
Date: Mon Nov 07 15:08:03 2016

[extension bindings] Remove leak of internal class

BUG=660678

Review-Url: https://codereview.chromium.org/2474623002
Cr-Commit-Position: refs/heads/master@{#429482}
(cherry picked from commit 0d9edd7b2524090fb0a0461e7bd9e5caa1e8a36d)

Review URL: https://codereview.chromium.org/2476303002 .

Cr-Commit-Position: refs/branch-heads/2883@{#474}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/201becf497377723fb9ec92bb8dcc0cf4f164ca1/extensions/renderer/resources/utils.js


### bu...@google.com (2016-11-07)

Approved for merging into M54 (build 2840), thanks for the fix!

### bu...@chromium.org (2016-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/15c15fc6d0703dcf6eef798b409164db183c05a8

commit 15c15fc6d0703dcf6eef798b409164db183c05a8
Author: Andrew R. Whalley <awhalley@chromium.org>
Date: Tue Nov 08 00:06:42 2016

[M54 merge][extension bindings] Remove leak of internal class

BUG=660678

Review-Url: https://codereview.chromium.org/2474623002
Cr-Commit-Position: refs/heads/master@{#429482}
(cherry picked from commit 0d9edd7b2524090fb0a0461e7bd9e5caa1e8a36d)

Review URL: https://codereview.chromium.org/2487543002 .

Cr-Commit-Position: refs/branch-heads/2840@{#828}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/15c15fc6d0703dcf6eef798b409164db183c05a8/extensions/renderer/resources/utils.js


### aw...@chromium.org (2016-11-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-14)

Thanks for this - $1,000 reward!

### ja...@googlemail.com (2016-11-18)

Please donate the reward to UNICEF.

### aw...@google.com (2016-11-18)

$2,000 has been donated via unicefusa.org - many thanks!

### sh...@chromium.org (2017-02-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/660678?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085822)*
