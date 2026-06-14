# Security: V8ValueConverter::ToV8Value is insecure (e.g. heap-use-after-free in MimeHandlerViewContainer::PostMessage

| Field | Value |
|-------|-------|
| **Issue ID** | [40084169](https://issues.chromium.org/issues/40084169) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **CVE IDs** | CVE-2016-1679 |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-04-25 |
| **Bounty** | $3,500.00 |

## Description

Chrome version: 50.0.2661.75 (and also master - 52.0.2716.0)

V8ValueConverter::ToV8Value may run arbitrary JavaScript code via setters when a base::Value is converted to a v8::Value [1]. This makes no sense and is a source of security issues.

For instance, MimeHandlerViewContainer::PostMessageFromValue uses V8ValueConverter to convert a DictionaryValue to a v8::Value, using an untrustworthy ScriptContext [2]. This allows attackers to intercept the setter of a property and trigger a use-after-free.

The attached PoC (top-with-pdf.html) does the following:
1. Load a PDF file in a frame (to activate the built-in PDF viewer that uses the vulnerable MimeHandlerViewContainer).
2. Define a property setter for the "type" key in the iframe that removes the frame ("type" because this is defined in [3]).
3. Call window.print() in the iframe to trigger the value conversion.
4. The setter from step 2 is triggered, and the frame is removed.

After step 4, Chrome with ASAN crashes the renderer because of a UAF in MimeHandlerViewContainer::PostMessage (see attached log file).

Although this specific UAF could be solved by using weak pointers, I believe that the best solution is to modify V8ValueConverter::ToV8Value to NOT trigger setters, since it makes no sense to allow it, especially because there are many other callers of V8ValueConverter::ToV8Value that are similarly vulnerable, including but not limited to cross-process postMessage on the web [4] and lots of extension code (see e.g. the attached zip file plus ASAN stack trace for a simple extension that causes a crash at [5]).


[1] https://chromium.googlesource.com/chromium/src/+/c864f52514c7e8cf9992a524e0294b1cc32c1db5/content/child/v8_value_converter_impl.cc#264
[2] https://chromium.googlesource.com/chromium/src/+/f6f806674c4f6ebbb8b20197ae5b6c7a40bba08f/extensions/renderer/guest_view/mime_handler_view/mime_handler_view_container.cc#269
[3] https://chromium.googlesource.com/chromium/src/+/10098ae32d6cd53775282b9bcc1cfc697cd0a00c/chrome/renderer/printing/chrome_print_web_view_helper_delegate.cc#77
[4] https://chromium.googlesource.com/chromium/src/+/91da0781306a006952e67ee4423a59a5a0da8fb6/content/renderer/render_frame_impl.cc#2083
[5] https://chromium.googlesource.com/chromium/src/+/f6f806674c4f6ebbb8b20197ae5b6c7a40bba08f/extensions/renderer/messaging_bindings.cc#304

## Attachments

- [top-with-pdf.html](attachments/top-with-pdf.html) (text/plain, 1.4 KB)
- [asan-cr-50.0.2661.75.log](attachments/asan-cr-50.0.2661.75.log) (text/plain, 23.3 KB)
- [messaging_bindings_npe.zip](attachments/messaging_bindings_npe.zip) (application/octet-stream, 1.8 KB)
- [messaging_bindings_npe-asan.log](attachments/messaging_bindings_npe-asan.log) (text/plain, 9.1 KB)

## Timeline

### ro...@robwu.nl (2016-04-25)

And here is a proposed patch: https://codereview.chromium.org/1918793003

### ro...@robwu.nl (2016-04-25)

+jochen for reviewing the patch.

### va...@chromium.org (2016-04-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>Bindings]

### rs...@chromium.org (2016-04-26)

Tagging as M50 based on the ASan log for 50.0.2661.75.

### bu...@chromium.org (2016-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b5bdf3778209179111c9f865af00940e74aa20e7

commit b5bdf3778209179111c9f865af00940e74aa20e7
Author: rob <rob@robwu.nl>
Date: Wed Apr 27 11:27:06 2016

V8ValueConverter::ToV8Value should not trigger setters

BUG=606390

Review URL: https://codereview.chromium.org/1918793003

Cr-Commit-Position: refs/heads/master@{#390045}

[modify] https://crrev.com/b5bdf3778209179111c9f865af00940e74aa20e7/content/child/v8_value_converter_impl.cc
[modify] https://crrev.com/b5bdf3778209179111c9f865af00940e74aa20e7/content/child/v8_value_converter_impl_unittest.cc


### ro...@robwu.nl (2016-04-27)

Verified fixed in 52.0.2719.0 (390054).

Chrome no longer crashes using the STR from the report.

I'll request merges later this week.

### cl...@chromium.org (2016-04-27)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ro...@robwu.nl (2016-04-28)

Requesting to merge b5bdf3778209179111c9f865af00940e74aa20e7 with M-51.

### ti...@google.com (2016-04-28)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### bu...@chromium.org (2016-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dfadac5e2b85dfed5076434e4152aed9fc4c80ac

commit dfadac5e2b85dfed5076434e4152aed9fc4c80ac
Author: Rob Wu <rob@robwu.nl>
Date: Thu Apr 28 14:55:07 2016

V8ValueConverter::ToV8Value should not trigger setters

BUG=606390

Review URL: https://codereview.chromium.org/1918793003

Cr-Commit-Position: refs/heads/master@{#390045}
(cherry picked from commit b5bdf3778209179111c9f865af00940e74aa20e7)

Review URL: https://codereview.chromium.org/1930953002 .

Cr-Commit-Position: refs/branch-heads/2704@{#286}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/dfadac5e2b85dfed5076434e4152aed9fc4c80ac/content/child/v8_value_converter_impl.cc
[modify] https://crrev.com/dfadac5e2b85dfed5076434e4152aed9fc4c80ac/content/child/v8_value_converter_impl_unittest.cc


### ro...@robwu.nl (2016-04-28)

Requesting to merge b5bdf3778209179111c9f865af00940e74aa20e7 with M-50.

The patch has been in Canary since today, and the unit test and manual tests confirm that the bug has been resolved.

The risk of merging is low because there is nothing in Chromium that expects side effects (setters to be triggered) when doing the value conversion (and that is also why this was a security bug).

### ti...@google.com (2016-04-29)

[Automated comment] Request affecting a post-stable build (M50), manual review required.

### go...@chromium.org (2016-05-06)

Approving Merge to M50 branch 2661 based on https://crbug.com/chromium/606390#c11. Please merge to M50 branch 2661 ASAP. We're planning M50 Stable release next week. Thank you.

### bu...@chromium.org (2016-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6a66d73c561f07ff61f46311467cc451b5bcb86b

commit 6a66d73c561f07ff61f46311467cc451b5bcb86b
Author: Rob Wu <rob@robwu.nl>
Date: Fri May 06 10:56:46 2016

V8ValueConverter::ToV8Value should not trigger setters

BUG=606390

Review URL: https://codereview.chromium.org/1918793003

Cr-Commit-Position: refs/heads/master@{#390045}
(cherry picked from commit b5bdf3778209179111c9f865af00940e74aa20e7)

Review URL: https://codereview.chromium.org/1959613002 .

Cr-Commit-Position: refs/branch-heads/2661@{#659}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/6a66d73c561f07ff61f46311467cc451b5bcb86b/content/child/v8_value_converter_impl.cc
[modify] https://crrev.com/6a66d73c561f07ff61f46311467cc451b5bcb86b/content/child/v8_value_converter_impl_unittest.cc


### bu...@chromium.org (2016-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/54cc1bc318e2ca7a5dc441eba5240d9b2eac2063

commit 54cc1bc318e2ca7a5dc441eba5240d9b2eac2063
Author: Rob Wu <rob@robwu.nl>
Date: Fri May 06 18:37:15 2016

Revert change to v8_value_converter_impl_unittest.cc

To resolve compilation errors on a release branch caused by
6a66d73c561f07ff61f46311467cc451b5bcb86b.

BUG=609878,606390

Review URL: https://codereview.chromium.org/1959633004 .

Cr-Commit-Position: refs/branch-heads/2661@{#661}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/54cc1bc318e2ca7a5dc441eba5240d9b2eac2063/content/child/v8_value_converter_impl_unittest.cc


### ti...@google.com (2016-05-09)

-merge-merged-2661 as reverted. Please re-add when landing again.

### ro...@robwu.nl (2016-05-09)

Adding label again - only the test case was reverted because the test used APIs that are not on stable (https://crbug.com/chromium/609878). The fix itself is on M-50.

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-25)

Congrats Rob - $3500 for this report ($3000 for the bug, $500 for the patch).

CVE-ID is CVE-2016-1679

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-04)

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

This issue was migrated from crbug.com/chromium/606390?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084169)*
