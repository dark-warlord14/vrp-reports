# UI/URL Spoofing by putting the page into fullscreen when a user opens the emoji dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40054574](https://issues.chromium.org/issues/40054574) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WindowDialog, UI>Browser>FullScreen |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2021-01-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

By waiting for a user to open the emoji dialog and at the same time forcing them to enter into fullscreen it is possible to overlap the fullscreen warning message and then perform UI/URL spoofing.

The attack works as follows:

1. User accesses attacker's website and right-clicks on an input field to make the context menu show up.
2. As soon as the context menu opens, the input field is moved up (to align it directly above where the fullscreen warning message is supposed to appear).
3. When the user selects the emoji option, the script forces the victim to enter fullscreen, which places the emoji dialog above the fullscreen warning message, hiding it.
4. The hidden fullscreen message will disappear after around 5 seconds, and later, when the user eventually closes the dialog, the message will be long gone and the page will remain spoofed.

This allows an effect similar to the UI/URL spoofing of <https://crbug.com/chromium/550017>.

Here's an unlisted video demonstrating the issue:  

<https://youtu.be/vdgtNchq7gQ>

**VERSION**  

Chrome Version: 88.0.4324.104 (Official Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Access <https://lbherrera.github.io/lab/emoji-spoof/index.html>
2. Right-click on the input field and select the "Emoji" option.
3. The page will enter into fullscreen and the message warning the user will be overlayed by the emoji dialog.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [index.html](attachments/index.html) (text/plain, 1.2 KB)

## Timeline

### [Deleted User] (2021-01-26)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-01-26)

Thanks for the report. I'll triage this bug. Please take the POC off Github so it isn't publicly accessible.

### va...@chromium.org (2021-01-26)

avi@, meacer@, cthomp@ -- between you three, one of you is probably the right owner. Please feel free to triage further as appropriate.

[Monorail components: Blink>WindowDialog UI>Browser>FullScreen]

### va...@chromium.org (2021-01-26)

Note that the "full screen" notification does appear momentarily before the emoji dialog appears on top of that.

### ct...@chromium.org (2021-01-26)

Seems plausible that we need to add the fullscreen block for the emoji dialog (like avi@ did for permissions dialogs and protocol handlers in crrev.com/c/2041871 and crrev.com/c/2044658). Unfortunately this doesn't look as straightforward as those cases, as I think the emoji dialog is a one-shot trigger to an OS-specific command rather than something we can easily track the lifetime of inside Chrome [1].

[1] https://source.chromium.org/chromium/chromium/src/+/master:ui/base/emoji/emoji_panel_helper.h;bpv=1;bpt=1

### av...@chromium.org (2021-01-26)

I cannot repro on the Mac; your PoC does a fullscreen trigger with keycode 91, which is not how context menus work on the Mac. Note also that the fullscreen bubble on the Mac is explicitly coded to show z-ordered over _every_ window, including the emoji palette, so I would be surprised if this could be made to work on the Mac.

Which platforms have you reproduced this on?

### he...@gmail.com (2021-01-26)

#2: The PoC is not public, it was hosted on a private repository and is served through GitHub Pages (access happens only through the full path), but I have removed the PoC as recommended.

#6: The PoC was only tested on Windows 10.

### [Deleted User] (2021-01-26)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### av...@chromium.org (2021-02-02)

As per https://crbug.com/chromium/1170584#c5, “Seems plausible that we need to add the fullscreen block for the emoji dialog” I will attempt to do so.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f8ab2f2363d4b08a75c1db76b5031c70858a3e5e

commit f8ab2f2363d4b08a75c1db76b5031c70858a3e5e
Author: Avi Drissman <avi@chromium.org>
Date: Thu Feb 04 02:12:56 2021

Drop fullscreen on invocation of the emoji dialog

The emoji dialog can be used to interfere with the fullscreen
bubble, so drop fullscreen.

Fixed: 1170584
Change-Id: I8acc69c7d41971e5f55a65528169ff57ab410e7a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2669847
Reviewed-by: Chris Thompson <cthomp@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#850406}

[modify] https://crrev.com/f8ab2f2363d4b08a75c1db76b5031c70858a3e5e/chrome/browser/renderer_context_menu/render_view_context_menu.cc


### [Deleted User] (2021-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-04)

Requesting merge to beta M89 because latest trunk commit (850406) appears to be after beta branch point (843830).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-05)

This bug requires manual review: M89's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-02-08)

avi@  request to provide answers to questions from https://crbug.com/chromium/1170584#c15

### av...@chromium.org (2021-02-08)

OP, the fix landed in 90.0.4409.0. Can you confirm that this no longer reproduces?

### he...@gmail.com (2021-02-08)

#17: I can confirm the PoC no longer reproduces in 90.0.4412.0.

### av...@chromium.org (2021-02-08)

1. Yes, it is a security fix.
2. https://chromium-review.googlesource.com/c/chromium/src/+/2669847
3. Yes.
4. No.
5. Security fix.
6. No.
7. n/a

### ad...@google.com (2021-02-09)

Approving merge to M89, branch 4389.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/15e7b81e4b0fd0aae3fc48e85d1232d9651ba24a

commit 15e7b81e4b0fd0aae3fc48e85d1232d9651ba24a
Author: Avi Drissman <avi@chromium.org>
Date: Tue Feb 09 03:09:13 2021

Drop fullscreen on invocation of the emoji dialog

The emoji dialog can be used to interfere with the fullscreen
bubble, so drop fullscreen.

(cherry picked from commit f8ab2f2363d4b08a75c1db76b5031c70858a3e5e)

Fixed: 1170584
Change-Id: I8acc69c7d41971e5f55a65528169ff57ab410e7a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2669847
Reviewed-by: Chris Thompson <cthomp@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#850406}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2682859
Auto-Submit: Avi Drissman <avi@chromium.org>
Commit-Queue: Chris Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/branch-heads/4389@{#829}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/15e7b81e4b0fd0aae3fc48e85d1232d9651ba24a/chrome/browser/renderer_context_menu/render_view_context_menu.cc


### he...@gmail.com (2021-02-22)

Hi, any updates regarding the panel decision for this issue? Thanks!

### ad...@google.com (2021-02-26)

Apologies, the panel has currently got quite a backlog of low and medium severity bugs. It hasn't been overlooked.

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### gi...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-04)

Congratulations, Luan! The VRP Panel has decided to award you $1,000 for this report. Thank you and nice work! 

### vs...@google.com (2021-03-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d98209611dc951a7c4ec2d00c299f993d4234769

commit d98209611dc951a7c4ec2d00c299f993d4234769
Author: Avi Drissman <avi@chromium.org>
Date: Thu Mar 04 13:59:56 2021

Drop fullscreen on invocation of the emoji dialog

The emoji dialog can be used to interfere with the fullscreen
bubble, so drop fullscreen.

(cherry picked from commit f8ab2f2363d4b08a75c1db76b5031c70858a3e5e)

Fixed: 1170584
Change-Id: I8acc69c7d41971e5f55a65528169ff57ab410e7a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2669847
Reviewed-by: Chris Thompson <cthomp@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#850406}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2731510
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1557}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/d98209611dc951a7c4ec2d00c299f993d4234769/chrome/browser/renderer_context_menu/render_view_context_menu.cc


### am...@google.com (2021-03-05)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1170584?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WindowDialog, UI>Browser>FullScreen]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054574)*
