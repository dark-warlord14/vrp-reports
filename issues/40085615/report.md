# Security: Internal functions leaked when DevTools is open

| Field | Value |
|-------|-------|
| **Issue ID** | [40085615](https://issues.chromium.org/issues/40085615) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Reporter** | pi...@live.nl |
| **Assignee** | ko...@chromium.org |
| **Created** | 2016-10-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

If DevTools is open, then a script [1] is run in the context of the webpage. The script has some cases of `__proto__: null`, presumably to prevent accessors on `Object.prototype` from messing with the objects in there. However, the assignment `InjectedScript.primitiveTypes = ...` \*is\* interceptable, and the entire `InjectedScript` function is thereby leaked to the webpage.

Of particular interest is the `InjectedScript.RemoteObject.prototype._generatePreview` function. This calls the native function `InjectedScriptHost.getInternalProperties`. Its return value can be intercepted by overwriting `_appendPropertyDescriptors`. What is interesting is that the return value contains `Scope` objects. These are objects that map variable names to objects that are in scope of a given function. This can be used to obtain non-exposed variables in a script.

In particular, using some tricks it is possible to run a function that requires a user gesture without a user gesture, like I did in <https://crbug.com/chromium/468931>. (That issue has been fixed, but using this vulnerability that particular exploit can still be done if DevTools is open.)

The details: Using `getInternalProperties`, we can get `Event` in `webstore_custom_bindings.js`, a script used in the extension system but run for regular webpages. In turn, we can get `$Function` since it is in scope of `Event` in `event.js`. Overwriting `$Function.bind`, we can intercept a function defined in `bindings.js`. That function has `require` in scope, which can be used to obtain `getFileBindingsForApi` in `file_entry_binding_util.js`. This function has `GetModuleSystem` in scope, which can be used to obtain `requireNative`. Finally, this can be used to obtain `RunWithGesture` in the `guest_view_internal` native module.

**VERSION**  

Chrome Version: 55.0.2881.5 canary (64-bit). It does not reproduce in stable. I did not try beta/dev.  

Operating System: Windows 10

**REPRODUCTION CASE**  

See attachment. It is a bit dirty so as to trigger certain codepaths. Note that it only reproduces when DevTools is open.

[1] <https://chromium.googlesource.com/v8/v8/+/master/src/inspector/injected-script-source.js>

## Attachments

- [bug.html](attachments/bug.html) (text/plain, 2.1 KB)

## Timeline

### ts...@chromium.org (2016-10-06)

[Empty comment from Monorail migration]

[Monorail components: Platform>DevTools>Platform]

### ts...@chromium.org (2016-10-06)

[Empty comment from Monorail migration]

### dg...@chromium.org (2016-10-06)

Not sure whether this actually works in M54 (beta).

### ko...@chromium.org (2016-10-06)

Beta is affected, fix is on the way: https://codereview.chromium.org/2399003003/

### bu...@chromium.org (2016-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/fac3b6fa46b29142eafbb0060bcc4ffbe78c4cc4

commit fac3b6fa46b29142eafbb0060bcc4ffbe78c4cc4
Author: kozyatinskiy <kozyatinskiy@chromium.org>
Date: Fri Oct 07 01:16:10 2016

[inspector] filter useless in preview internal properties

Only subset of internal properties can be useful in preview, report only them.

BUG=chromium:653610
R=dgozman@chromium.org

Review-Url: https://codereview.chromium.org/2399003003
Cr-Commit-Position: refs/heads/master@{#40064}

[modify] https://crrev.com/fac3b6fa46b29142eafbb0060bcc4ffbe78c4cc4/src/inspector/v8-injected-script-host.cc
[add] https://crrev.com/fac3b6fa46b29142eafbb0060bcc4ffbe78c4cc4/test/inspector/debugger/object-preview-internal-properties-expected.txt
[add] https://crrev.com/fac3b6fa46b29142eafbb0060bcc4ffbe78c4cc4/test/inspector/debugger/object-preview-internal-properties.js


### sh...@chromium.org (2016-10-07)

[Empty comment from Monorail migration]

### ko...@chromium.org (2016-10-07)

[Empty comment from Monorail migration]

### bu...@google.com (2016-10-07)

Approved for M54

### bu...@chromium.org (2016-10-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c020bb514eecc71682d2d50110e5512b29f72f17

commit c020bb514eecc71682d2d50110e5512b29f72f17
Author: Alexey Kozyatinskiy <kozyatinskiy@chromium.org>
Date: Sat Oct 08 01:03:49 2016

[DevTools] filter useless in preview internal properties

Only subset of internal properties can be useful in preview, report only them.

BUG=chromium:653610
TBR=dgozman@chromium.org

Review URL: https://codereview.chromium.org/2403643002 .

Committed: https://crrev.com/fac3b6fa46b29142eafbb0060bcc4ffbe78c4cc4
Cr-Original-Commit-Position: refs/heads/master@{#40064}
Cr-Commit-Position: refs/branch-heads/2840@{#692}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/c020bb514eecc71682d2d50110e5512b29f72f17/third_party/WebKit/Source/platform/v8_inspector/V8InjectedScriptHost.cpp


### sh...@chromium.org (2016-10-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

Congratulations, the panel awarded $1,000 for this bug!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c020bb514eecc71682d2d50110e5512b29f72f17

commit c020bb514eecc71682d2d50110e5512b29f72f17
Author: Alexey Kozyatinskiy <kozyatinskiy@chromium.org>
Date: Sat Oct 08 01:03:49 2016

[DevTools] filter useless in preview internal properties

Only subset of internal properties can be useful in preview, report only them.

BUG=chromium:653610
TBR=dgozman@chromium.org

Review URL: https://codereview.chromium.org/2403643002 .

Committed: https://crrev.com/fac3b6fa46b29142eafbb0060bcc4ffbe78c4cc4
Cr-Original-Commit-Position: refs/heads/master@{#40064}
Cr-Commit-Position: refs/branch-heads/2840@{#692}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/c020bb514eecc71682d2d50110e5512b29f72f17/third_party/WebKit/Source/platform/v8_inspector/V8InjectedScriptHost.cpp


### sh...@chromium.org (2017-01-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-01-14)

This issue was migrated from crbug.com/chromium/653610?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085615)*
