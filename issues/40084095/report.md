# Security: Leak of extension privates via utils module

| Field | Value |
|-------|-------|
| **Issue ID** | [40084095](https://issues.chromium.org/issues/40084095) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **CVE IDs** | CVE-2016-1687 |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-04-14 |
| **Bounty** | $1,000.00 |

## Description

Chrome version: 52.0.2709.0 and earlier

To shield extension code from unwanted interference by extensions, the internal state of extensions is stored using "privates", which stored the variables in a hidden/private property using V8 magic.

The util extension module offers utils.expose to construct a JavaScript class with an internal implementation that is hidden from the public. This also makes use of privates. The class is constructed by concatenating a fixed JavaScript string with three times a name in UtilsNativeHandler::CreateClassWrapper [1]. Everything from JavaScript should also be validated in C++ because there have been many bugs that show that the JavaScript part of the extension bindings is fragile.


When %s in UtilsNativeHandler::CreateClassWrapper [1] is replaced three times with the next snippet, the "privates" function (and the private values of all modules that depend on it) is leaked.

a(){}`/*/return arguments


I have attached a PoC that uses https://crbug.com/chromium/603725 to load the utils module with the above snippet.
If you load the page and open the JS console, then you'll see a public extension object together with its private implementation. 


[1] https://chromium.googlesource.com/chromium/src/+/8ce1943be5284c67fb79cae9bf1576624fba97b6/extensions/renderer/utils_native_handler.cc#26

## Attachments

- [module-system-get-privates50.html](attachments/module-system-get-privates50.html) (text/plain, 9.9 KB)
- [privates-not-private.png](attachments/privates-not-private.png) (image/png, 52.4 KB)

## Timeline

### ts...@chromium.org (2016-04-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-15)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-04-15)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-04-20)

I'll submit a patch for this to offload you.

### ro...@robwu.nl (2016-04-21)

privates' implementation is unreliable at the moment. Even without leaking |privates|, it is possible to steal most private properties just by overriding Object.prototype. For instance, stealing "private" implementation:

Object.defineProperty(Object.prototype, 'impl', {
  get() { console.log('getting impl',this, this.impl__); },
  set(v) { if (v!==true) { this.impl__ = v;console.log('setting impl', this, v); } },
});

### rd...@chromium.org (2016-04-21)

I think privates() should mostly only be used to hide implementation details for objects, rather than for storing anything destructive.  I think this is mostly true, but there's almost certainly some holes.  Those should probably be fixed, because I doubt privates() will ever be entirely private.

That said, if we just replace privates(this).impl with Object.defineProperty(privates(this), 'impl', {...}), can we at least get around making it this easy?

### ro...@robwu.nl (2016-04-21)

I'll set __proto__ to null, then privates can reliably be private - as it promises.

This is guaranteed to be private:
privates(foo).impl = bar

But this is not, if impl inherits from a prototype that can be modified by a third party:
privates(foo).impl.unsafe = bar

### rd...@chromium.org (2016-04-21)

for the expose() case, are there any times we wouldn't want impl to have __proto__ null?  Or can we enforce that?  Of course, then we'd have privates(foo).impl.bar.unsafe unless bar was __proto__ null, but, well, we already have that problem anyway.

(There are in privates(), e.g. with guestView where there's an internal Element)

### ro...@robwu.nl (2016-04-22)

With inheritance, __proto__ is not necessarily null (({__proto__:null}).__proto__ === undefined, by the way). But there is no reason for private classes to inherit from Object.

I have uploaded a new patch that adds a DCHECK and ran try bots. To keep the patch focused, I think that I'll comment out the DCHECK and use the try bot results to submit another CL.

### bu...@chromium.org (2016-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/77e0fbe12e32b16d5c1d7c0380b45fde363004b2

commit 77e0fbe12e32b16d5c1d7c0380b45fde363004b2
Author: rob <rob@robwu.nl>
Date: Fri Apr 22 23:16:54 2016

Ensure that privates are private.

- Remove JS code injection functionality from UtilsNativeHandler.
- Ensure that utils.expose only exposes public properties.
- Prevent privates from getting poisoned via arbitrary constructor invocations.
- Prevent privates from leaking through prototypes.

BUG=603748

Review URL: https://codereview.chromium.org/1903303002

Cr-Commit-Position: refs/heads/master@{#389292}

[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/chrome/renderer/resources/extensions/automation/automation_event.js
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/chrome/renderer/resources/extensions/automation/automation_node.js
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/chrome/renderer/resources/extensions/enterprise_platform_keys/key_pair.js
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/chrome/renderer/resources/extensions/enterprise_platform_keys/subtle_crypto.js
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/chrome/renderer/resources/extensions/enterprise_platform_keys/token.js
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/chrome/renderer/resources/extensions/platform_keys/key.js
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/chrome/renderer/resources/extensions/platform_keys/subtle_crypto.js
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/chrome/renderer/resources/extensions/web_view/chrome_web_view.js
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/extensions/renderer/module_system.cc
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/extensions/renderer/module_system_unittest.cc
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/extensions/renderer/resources/event.js
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/extensions/renderer/resources/messaging.js
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/extensions/renderer/resources/utils.js
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/extensions/renderer/resources/web_request_internal_custom_bindings.js
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/extensions/renderer/safe_builtins.cc
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/extensions/renderer/utils_native_handler.cc
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/extensions/renderer/utils_native_handler.h
[modify] https://crrev.com/77e0fbe12e32b16d5c1d7c0380b45fde363004b2/extensions/test/data/utils_unittest.js


### bu...@chromium.org (2016-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/931719c51866a7c2e272114517cc52aa6581adff

commit 931719c51866a7c2e272114517cc52aa6581adff
Author: rob <rob@robwu.nl>
Date: Thu Apr 28 22:29:29 2016

Sanitize inheritance in callers of utils.expose

- Let all private classes inherit from the null prototype.
- Use safe built-ins.
- Minor drive-by fixes (code style).

BUG=603748,591164

Review-Url: https://codereview.chromium.org/1915753002
Cr-Commit-Position: refs/heads/master@{#390510}

[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/chrome/renderer/resources/extensions/automation/automation_event.js
[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/chrome/renderer/resources/extensions/automation/automation_node.js
[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/chrome/renderer/resources/extensions/enterprise_platform_keys/key_pair.js
[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/chrome/renderer/resources/extensions/enterprise_platform_keys/subtle_crypto.js
[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/chrome/renderer/resources/extensions/enterprise_platform_keys/token.js
[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/chrome/renderer/resources/extensions/platform_keys/key.js
[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/chrome/renderer/resources/extensions/platform_keys/subtle_crypto.js
[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/chrome/renderer/resources/extensions/web_view/chrome_web_view.js
[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/extensions/renderer/resources/event.js
[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/extensions/renderer/resources/messaging.js
[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/extensions/renderer/resources/utils.js
[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/extensions/renderer/resources/web_request_internal_custom_bindings.js
[modify] https://crrev.com/931719c51866a7c2e272114517cc52aa6581adff/extensions/renderer/safe_builtins.cc


### ro...@robwu.nl (2016-04-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-29)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ro...@robwu.nl (2016-05-02)

Requesting approval for merging 77e0fbe12e32b16d5c1d7c0380b45fde363004b2 and 931719c51866a7c2e272114517cc52aa6581adff with M-51.

### ti...@google.com (2016-05-02)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### go...@chromium.org (2016-05-02)

Please merge your change to M51 branch 2704 by EOD today or latest by tomorrow 4:00 PM PST in order to make it to this week beta release. Thank you.

### bu...@chromium.org (2016-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f2b970209b08639170042334a2f1f2342f8a9113

commit f2b970209b08639170042334a2f1f2342f8a9113
Author: Rob Wu <rob@robwu.nl>
Date: Mon May 02 20:22:38 2016

Ensure that privates are private.

- Remove JS code injection functionality from UtilsNativeHandler.
- Ensure that utils.expose only exposes public properties.
- Prevent privates from getting poisoned via arbitrary constructor invocations.
- Prevent privates from leaking through prototypes.

BUG=603748

Review URL: https://codereview.chromium.org/1903303002

Cr-Commit-Position: refs/heads/master@{#389292}
(cherry picked from commit 77e0fbe12e32b16d5c1d7c0380b45fde363004b2)

Review URL: https://codereview.chromium.org/1938123002 .

Cr-Commit-Position: refs/branch-heads/2704@{#337}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/chrome/renderer/resources/extensions/automation/automation_event.js
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/chrome/renderer/resources/extensions/automation/automation_node.js
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/chrome/renderer/resources/extensions/enterprise_platform_keys/key_pair.js
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/chrome/renderer/resources/extensions/enterprise_platform_keys/subtle_crypto.js
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/chrome/renderer/resources/extensions/enterprise_platform_keys/token.js
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/chrome/renderer/resources/extensions/platform_keys/key.js
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/chrome/renderer/resources/extensions/platform_keys/subtle_crypto.js
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/chrome/renderer/resources/extensions/web_view/chrome_web_view.js
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/extensions/renderer/module_system.cc
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/extensions/renderer/module_system_unittest.cc
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/extensions/renderer/resources/event.js
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/extensions/renderer/resources/messaging.js
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/extensions/renderer/resources/utils.js
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/extensions/renderer/resources/web_request_internal_custom_bindings.js
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/extensions/renderer/safe_builtins.cc
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/extensions/renderer/utils_native_handler.cc
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/extensions/renderer/utils_native_handler.h
[modify] https://crrev.com/f2b970209b08639170042334a2f1f2342f8a9113/extensions/test/data/utils_unittest.js


### bu...@chromium.org (2016-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c29bc7edad5f1e80cad11d50a1cd880456cb54cb

commit c29bc7edad5f1e80cad11d50a1cd880456cb54cb
Author: Rob Wu <rob@robwu.nl>
Date: Mon May 02 20:25:29 2016

Sanitize inheritance in callers of utils.expose

- Let all private classes inherit from the null prototype.
- Use safe built-ins.
- Minor drive-by fixes (code style).

BUG=603748,591164

Review-Url: https://codereview.chromium.org/1915753002
Cr-Commit-Position: refs/heads/master@{#390510}
(cherry picked from commit 931719c51866a7c2e272114517cc52aa6581adff)

Review URL: https://codereview.chromium.org/1939833003 .

Cr-Commit-Position: refs/branch-heads/2704@{#339}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/chrome/renderer/resources/extensions/automation/automation_event.js
[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/chrome/renderer/resources/extensions/automation/automation_node.js
[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/chrome/renderer/resources/extensions/enterprise_platform_keys/key_pair.js
[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/chrome/renderer/resources/extensions/enterprise_platform_keys/subtle_crypto.js
[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/chrome/renderer/resources/extensions/enterprise_platform_keys/token.js
[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/chrome/renderer/resources/extensions/platform_keys/key.js
[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/chrome/renderer/resources/extensions/platform_keys/subtle_crypto.js
[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/chrome/renderer/resources/extensions/web_view/chrome_web_view.js
[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/extensions/renderer/resources/event.js
[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/extensions/renderer/resources/messaging.js
[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/extensions/renderer/resources/utils.js
[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/extensions/renderer/resources/web_request_internal_custom_bindings.js
[modify] https://crrev.com/c29bc7edad5f1e80cad11d50a1cd880456cb54cb/extensions/renderer/safe_builtins.cc


### ro...@robwu.nl (2016-05-03)

I'll leave this at beta (M-51).

https://crbug.com/chromium/603732 shows a UAF that used another vulnerability to exploit the bug from a regular web page. When that other vulnerability is fixed, the UAF was still exploitable by extensions (use this bug to trigger the UAF at privates(port).impl in [1]). Since the UAF was fixed, there is no immediate need for merging the fixes (that harden the extension bindings) to stable.


[1] https://chromium.googlesource.com/chromium/src/+/931719c51866a7c2e272114517cc52aa6581adff/extensions/renderer/resources/messaging.js#199

### ro...@robwu.nl (2016-05-06)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-05-06)

https://crbug.com/chromium/609569 showed another way to exploit this vulnerability (leakage of privates via prototypes), so I'm requesting a merge of 77e0fbe12e32b16d5c1d7c0380b45fde363004b2 and 931719c51866a7c2e272114517cc52aa6581adff with M-50 to fix the issue.

These patches are defences in the extension bindings against malicious pages and do not change the normal* behavior of extensions or web pages, and have been in canary for over a week. Therefore it should be safe to merge.

* https://crbug.com/chromium/609569 is an example of abnormal behavior. Web pages should not be able to interfere with the functionality of extensions on other pages.

### ti...@google.com (2016-05-06)

[Automated comment] Request affecting a post-stable build (M50), manual review required.

### ti...@google.com (2016-05-06)

In addition to #21, this change has had >48 hours on Beta (51.0.2704.36) and is an externally reported medium severity issue. I support the merge to M-50 before the cut on Monday next week.

### go...@chromium.org (2016-05-06)

Thank you Tim.

Approving merge to M50 branch 2661, based on https://crbug.com/chromium/603748#c21 and #23. Please merge asap (latest before 1:00 PM PST Monday), so we can take it for next week Stable refresh release. Thank you.

### ro...@robwu.nl (2016-05-06)

I just tried to merge, but found a merge conflict because 5fb2548448bd1b76a59d941b729d7a7f90d53bc8 is missing on M-50.

Unfortunately, that patch triggered a performance regression (https://crbug.com/chromium/608444) caused by https://crbug.com/chromium/606207. These bugs have all been fixed in canary two days ago, but the fix (https://bugs.chromium.org/p/chromium/issues/detail?id=606207#c27) still needs to be merged with M-51 and M-50.

So, I will hold off with merging the two patches until 5fb2548448bd1b76a59d941b729d7a7f90d53bc8 is merged with M-50. This probably means that this patch will not be in the third M-50 release.

timwillis@ Please confirm whether this is the right thing to do, and adjust the labels if necessary.

### ti...@google.com (2016-05-09)

Thanks Rob for the detailed update! Considering your findings, let's hold off on merging this to M-50.

Updating labels to leave this in the Merge-Triage - please change to Merge-Request-50 when ready to land again.

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-25)

Rob - $1000 for this report (Panel notes: $500 for the bug + $500 for the patch).

I'll add it to your tab. CVE-ID is CVE-2016-1687

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-05)

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

This issue was migrated from crbug.com/chromium/603748?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/609569]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084095)*
