# Security: Heap-use-after-free in ScriptInjector

| Field | Value |
|-------|-------|
| **Issue ID** | [40084746](https://issues.chromium.org/issues/40084746) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-07-02 |
| **Bounty** | $1,000.00 |

## Description

When an extension is unloaded (or reloaded), all content scripts are unregistered. If this happens in the middle of an injection, a UAF occurs, see attached PoC and explanation.

STR:
1. Load the attached extension.
2. The extension will open example.com and synchronously show a dialog.
3. While the dialog is being displayed, the extension will reload itself.
   As a result, all existing content script registrations are invalidated.
4. Dismiss the dialog.

The above causes a crash, because a dialog activates a nested message loop, and causes the UserScriptSet::UpdateUserScripts to run before the script injection completes (this invalidates the UserScript* of UserScriptInjector).
When the alert dialog is dismissed, the script returns and control is handed back to ScriptInjection, which calls multiple ScriptInjector methods that use stale UserScript pointers.

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 325 B)
- [background.js](attachments/background.js) (text/plain, 853 B)
- [contentscript.js](attachments/contentscript.js) (text/plain, 260 B)
- [asan-51.0.2704.79.log](attachments/asan-51.0.2704.79.log) (text/plain, 12.7 KB)

## Timeline

### ro...@robwu.nl (2016-07-02)

Patch: https://codereview.chromium.org/2116923002/

### ro...@robwu.nl (2016-07-03)

When I submitted that patch, it worked locally (i.e. without the fix the unit test crashes, with the patch the test passes). After running the try jobs the tests failed. I investigated it and found that it is caused by https://crbug.com/chromium/604675, which removes nested message loops for JS modal dialogs.

To reproduce on HEAD, open the devtools, put a breakpoint in the content script at the line of the alert dialog and refresh the page (manually or automated via an extension or remote debugging protocol). When the breakpoint is hit, a nested message loop is started. After continuing execution, the tab crashes for exactly the same reason as in the original report.

### pa...@chromium.org (2016-07-04)

Thanks for the report and the patch!

### ro...@robwu.nl (2016-07-04)

+rockot for review

### bu...@chromium.org (2016-07-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a80776332fd8c99b58beab5d91a6675e85013628

commit a80776332fd8c99b58beab5d91a6675e85013628
Author: rob <rob@robwu.nl>
Date: Mon Jul 04 23:45:35 2016

Avoid using stale UserScript pointers

BUG=625393
TEST=Manually. Compile Chrome with ASAN and follow the steps from the bug report.

Review-Url: https://codereview.chromium.org/2116923002
Cr-Commit-Position: refs/heads/master@{#403725}

[modify] https://crrev.com/a80776332fd8c99b58beab5d91a6675e85013628/extensions/renderer/user_script_injector.cc


### ro...@robwu.nl (2016-07-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-05)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-07-06)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-07-12)

Why wasn't the merge of a80776332fd8c99b58beab5d91a6675e85013628 to M-53 autoapproved? You can easily verify that it fixes the bug.

1. Start an ASAN build of Chrome.
2. Install an arbitrary extension, e.g. AdBlock Plus.
3. Visit any page where the content script is active, e.g. example.com.
4. Open the developer tools, go to the Sources tab, Content scripts, and put a breakpoint at the first line in the content script.
5. Reload the page, observe that the breakpoint is triggered.
6. Reload the extension (at chrome://extensions). ---- if this is not an unpacked extension, enable developer mode to see the background console link, open the background console and run chrome.runtime.reload()
7. Go back to the devtools from step 4-5.
8. Continue execution of the content script (after the breakpoint of step 5).

Before the patch: UAF / crash.
After the patch : No UAF.

(patch initially verified on the M-51 branch, now verified again on 54.0.2794.0, revision 404631)

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-07-15)

Also requesting merge approval for M-52 because of the lack of feedback to the M-53 merge request. I'd like to merge the fix before 52 is promoted to stable.

### go...@chromium.org (2016-07-15)

+ awhalley@, should we take this merge in for M52 and M53? Fix has been verified on M54 Canary. Please see https://crbug.com/chromium/625393#c9 for more details. 

### aw...@chromium.org (2016-07-15)

Yep, this is good to take for both.

### go...@chromium.org (2016-07-15)

Approving merge to M52 branch 2743 and M53 branch 2785 based on https://crbug.com/chromium/625393#c13. Please merge ASAP (latest by 4:00 PM PST Monday, 07/18). Thank you.

### bu...@chromium.org (2016-07-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6e7bc2880fd80e78320a7eb67894e4386ededeec

commit 6e7bc2880fd80e78320a7eb67894e4386ededeec
Author: Rob Wu <rob@robwu.nl>
Date: Sat Jul 16 08:58:27 2016

Avoid using stale UserScript pointers

BUG=625393
TEST=Manually. Compile Chrome with ASAN and follow the steps from the bug report.

Review-Url: https://codereview.chromium.org/2116923002
Cr-Commit-Position: refs/heads/master@{#403725}
(cherry picked from commit a80776332fd8c99b58beab5d91a6675e85013628)

Review URL: https://codereview.chromium.org/2155863003 .

Cr-Commit-Position: refs/branch-heads/2785@{#169}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/6e7bc2880fd80e78320a7eb67894e4386ededeec/extensions/renderer/user_script_injector.cc


### bu...@chromium.org (2016-07-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c4ddb314883ff49a717d3f5d90e11c6126dd028e

commit c4ddb314883ff49a717d3f5d90e11c6126dd028e
Author: Rob Wu <rob@robwu.nl>
Date: Sat Jul 16 09:00:27 2016

Avoid using stale UserScript pointers

BUG=625393
TEST=Manually. Compile Chrome with ASAN and follow the steps from the bug report.

Review-Url: https://codereview.chromium.org/2116923002
Cr-Commit-Position: refs/heads/master@{#403725}
(cherry picked from commit a80776332fd8c99b58beab5d91a6675e85013628)

Review URL: https://codereview.chromium.org/2158683002 .

Cr-Commit-Position: refs/branch-heads/2743@{#656}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/c4ddb314883ff49a717d3f5d90e11c6126dd028e/extensions/renderer/user_script_injector.cc


### aw...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

Thanks Rob!  $1,000 for this one.

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/625393?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084746)*
