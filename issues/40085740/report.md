# Security: Heap-use-after-free in InspectedContext::createInjectedScript

| Field | Value |
|-------|-------|
| **Issue ID** | [40085740](https://issues.chromium.org/issues/40085740) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-10-19 |
| **Bounty** | $1,500.00 |

## Description

Chrome version: 54.0.2840.59 (stable) and latest (56.0.2892.0)

Steps to reproduce (the order of steps does not matter):
1. Open attached file in Chrome.
2. Open the Devtools (F12, inspect element, whatever).

Expected: Nothing special should happen.
Actual: Tab crashes due to a use-after-free.

More info:
When console.log is called while the devtools is active (or when the devtools is opened after console.log has been called), InjectedScriptSource.js (aka injected-script-source.js since https://crbug.com/chromium/635948) is executed. This script runs in the context of the web page, so any script on the web can manipulate the JavaScript objects and change the state in unexpected ways. For example, scripts can destroy the context when the script is run. The C++ caller that injects this script (InspectedContext::createInjectedScript) does not account for this, leading to a UAF.

## Attachments

- [uaf-inspector-injected-script.html](attachments/uaf-inspector-injected-script.html) (text/plain, 161 B)
- [manifest.json](attachments/manifest.json) (text/plain, 242 B)
- [background.js](attachments/background.js) (text/plain, 697 B)

## Timeline

### ro...@robwu.nl (2016-10-19)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-10-19)

Patch: https://codereview.chromium.org/2432163004

### ro...@robwu.nl (2016-10-19)

Another PoC: An extension that automates the crash.

Steps to reproduce:
1. Create a directory.
2. Download attached files, put it in the folder.
3. Visit chrome://extensions, enable developer mode.
4. Click on the Load unpacked extension button.
5. Load the extension -- and observe that example.com is opened and crashes.

(alternatively I can upload the extension to the Chrome Web Store and victims can install it with a single click).

### ro...@robwu.nl (2016-10-19)

+kozyatinskiy for review of the CL.

I've looked into adding a regression test to v8, but there are some things that stop me from doing that:

- The test infrastructure looks very recent (https://crbug.com/635948), including tests will probably cause test failures on release branches.

- The test scenario is a bit convoluted: The context is destroyed during execution. It seems that v8/inspector does not include logic to destroy the inspected context.

- I don't know how to build the inspector test target.
  I tried:
  $ tools/dev/v8gen.py x64.release
  $ ninja -C out.gn/x64.release
  After modifying the test files, running ninja again does not cause any new compilation (which is weird because I touched C++ test code).

Manually running the tests from this bug report shows that my CL fixed the bug though.

### ko...@chromium.org (2016-10-20)

Thank you for great report.
Our long-term solution: don't call user code from injected-script-source.js. We'll achieve it by migrating this JS code into native.
Tests are not running on try bots now and we run new tests only on revisions after they were added and release branches should not be a problem.
We don't have contextDestoyed logic, but we can introduce it similar with setTimeout function in inspector-test.cc.
I think that inspector is disabled by default. You need to enable it, I'm not sure that v8gen.py support passing additional arguments but you can run:
$ gn args out.gn/x64.release
and add v8_enable_inspector = true manually and then rebuild with ninja.

### mb...@chromium.org (2016-10-20)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-10-20)

Thanks for the tips. I managed to compile the inspector-test target and managed to run a test as follows:
./out.gn/x64.release/inspector-test test/inspector/protocol-test.js test/inspector/console/<filename>.js

If the ultimate goal is to not call user code from injected-script-source.js, then how can I create a test that destroys the context when that specific file is run? I have already added a "detach" global function to the utils extension in inspector-test.cc, but I don't know how to call this function at the right moment.

I'm still looking for a way to run arbitrary code in the inspected context (correct me if I'm wrong --- I should look for a way to run code in backend_runner->context_, right?).

Do you have any suggestions for either of these two?

### sh...@chromium.org (2016-10-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-20)

[Empty comment from Monorail migration]

### ko...@chromium.org (2016-10-20)

I think that root of this issue - navigation happens during InjectedScriptSource initialization because user defined setter on Object.prototype:

Object.defineProperty(Object.prototype, "primitiveTypes", {
  configurable: true,
  set: function(v) {
    // detaching context.
  }
});

You can put your detaching logic inside of this setter.

To evaluate code in inspected context you can just call:
Protocol.Runtime.evaluate({ expression: "code" }).then(.. process result ..).
Or add function at the begin with:
InspectorTest.addScript(`
function foo() {
}`);
and then call this function with the same command:
Protocol.Runtime.evaluate({ expression: "foo()" });


### ro...@robwu.nl (2016-10-28)

Although bugdroid did not visit the issue, the patch landed at https://chromium.googlesource.com/v8/v8.git/+/cb2a39d36762da3a800d9b5e734319d1141070b9
Verified fixed in Chromium 56.0.2904.0 (V8 5.6.163 according to chrome://version)https://chromium.googlesource.com/v8/v8.git/+/cb2a39d36762da3a800d9b5e734319d1141070b9 ), using the automated steps to reproduce from https://crbug.com/chromium/657568#c3 (=Chrome does not crash any more).

I'll request a merge once the patch has baked on Canary.

### sh...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-30)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-10-31)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### go...@chromium.org (2016-10-31)

**** Bulk edit -  please ignore if not applicable ****

Please merge your change to M55 branch 2883 today before 5:00 PM PT or latest by tomorrow, Tuesday (11/01/16) 4:00 PM PT so we can take it for this week Beta release. 

### ko...@chromium.org (2016-11-01)

Thank you.
Since inspector is inside of V8. You need to request merge in V8 [1] instead of Chromium:
- add Merge-Request-5.5 label,
- add Blink>JavaScript component,
- add hablich@chromium.org to cc.

[1] https://github.com/v8/v8/wiki/Merging-&-Patching

[Monorail components: Blink>JavaScript]

### di...@chromium.org (2016-11-01)

[Automated comment] No milestone found on Merge-Request (i.e. merge-request-# label).

### ro...@robwu.nl (2016-11-01)

I contacted hablich by mail before requesting a merge, and he said that a merge request in Chromium's issue tracker is also ok.

### ko...@chromium.org (2016-11-01)

Ok, thank you!

[Monorail components: -Blink>JavaScript]

### go...@chromium.org (2016-11-01)

If there is a merge needed for M55, please merge ASAP otherwise remove "Merge-Approved-55" label. Thank you.

### bu...@chromium.org (2016-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/bb3c09d59250f64f65c628edf4fd182868ab67d0

commit bb3c09d59250f64f65c628edf4fd182868ab67d0
Author: rob <rob@robwu.nl>
Date: Wed Nov 02 08:57:04 2016

Merged: Avoid using stale InspectedContext pointers

Revision: cb2a39d36762da3a800d9b5e734319d1141070b9

BUG=chromium:657568
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=kozyatinskiy@chromium.org

Review-Url: https://codereview.chromium.org/2470563002
Cr-Commit-Position: refs/branch-heads/5.5@{#32}
Cr-Branched-From: 3cbd5838bd8376103daa45d69dade929ee4e0092-refs/heads/5.5.372@{#1}
Cr-Branched-From: b3c8b0ce2c9af0528837d8309625118d4096553b-refs/heads/master@{#40015}

[modify] https://crrev.com/bb3c09d59250f64f65c628edf4fd182868ab67d0/AUTHORS
[modify] https://crrev.com/bb3c09d59250f64f65c628edf4fd182868ab67d0/src/inspector/injected-script.cc
[modify] https://crrev.com/bb3c09d59250f64f65c628edf4fd182868ab67d0/src/inspector/inspected-context.cc
[modify] https://crrev.com/bb3c09d59250f64f65c628edf4fd182868ab67d0/src/inspector/inspected-context.h
[modify] https://crrev.com/bb3c09d59250f64f65c628edf4fd182868ab67d0/src/inspector/v8-inspector-session-impl.cc


### ro...@robwu.nl (2016-11-02)

Do I need to do anything else to get the patch in M55, or will it roll automatically?

And should the patch be taken to M54? It is low-risk and fixes a UAF.

### ko...@chromium.org (2016-11-02)

FYI: this code in M54 is located in third_party/WebKit/core/inspector, it was moved to V8 in M55.

### go...@chromium.org (2016-11-02)

Per https://crbug.com/chromium/657568#c22, this is already merged to M55. If nothing is pending for M55, please remove "Merge-Approved-55" label. Thank you.

### ro...@robwu.nl (2016-11-03)

Removing Merge-Approved-55 since merge-merged-5.5 is apparently sufficient.

Looks like this landed in 5.5.372.16, so it missed the most recent beta release.

Can we take the patch to stable?

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-07)

Nice one, the panel has awarded $1,500 for this bug!

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-12-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-06-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/657568?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085740)*
