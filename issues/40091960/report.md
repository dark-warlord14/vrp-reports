# External protocl handler UI has focus on open by default

| Field | Value |
|-------|-------|
| **Issue ID** | [40091960](https://issues.chromium.org/issues/40091960) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>HTML>CustomHandlers, UI |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | gr...@hotmail.com |
| **Assignee** | do...@chromium.org |
| **Created** | 2018-07-18 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. Go to https://attack.shhnjk.com/force_open.html
2. Hold Enter key for a second
3. Observe that Google.com is opened in IE

What is the expected behavior?
Default focus should be in "cancel" button or no focus to either of them.

What went wrong?
Since external protocl handler can be opened with victim holding enter key for a second, this greatly increases attack surface for attackers. You can use MS Office handlers to open remote files, and so on. And this is already out of Chrome's sandbox.

Did this work before? N/A 

Chrome version: 67.0.3396.99  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### ct...@chromium.org (2018-07-18)

dominickn@: I know it's been a couple years since you made this "new" external protocol UI (https://crbug.com/chromium/601725), but do you have thoughts on changing the default focus to "Cancel" here?

I'm not sure if there's a straightforward way to do that in the current implementation. Swap the button types (accept/cancel) but keep the text? Change the accelerator for the cancel button to be Enter and the accelerator for Accept to be something else (like in https://cs.chromium.org/chromium/src/chrome/browser/ui/views/bookmarks/bookmark_bubble_view.cc?l=254)?

Tentatively assigning Sev-Medium (P-1). I'd say this reduces the effectiveness of the sandbox, but is may be mitigated by requiring user interaction (holding the enter key).

Adding other OSes since the external protocol handler is on all desktop platforms.

This also reminds me of https://crbug.com/chromium/637098 which abused holding down the enter key.

If we are worried about this (or similar tricks) being abused, we do have a metric "clickjacking.launch_url" which tracks how long the dialog is open.

[Monorail components: Blink>HTML>CustomHandlers UI]

### s....@gmail.com (2018-07-18)

BTW, this also works with holding down the Space key. Though the difference is that space key doesn't trigger open until the key gets released.

### do...@chromium.org (2018-07-19)

I think the very simple solution is to change the default button from Accept to Cancel. CL for this is up at https://chromium-review.googlesource.com/c/chromium/src/+/1142705.

I'm not sure I buy the argument that this greatly increases attack surface. Users holding down the Enter key just doesn't seem like that big of an attack vector - they still have to click a link to trigger an external protocol launch. Downgrading severity accordingly.

Also removing Chrome OS since this doesn't exist on Chrome OS.

### s....@gmail.com (2018-07-19)

>Users holding down the Enter key just doesn't seem like that big of an attack
>vector - they still have to click a link to trigger an external protocol launch.
Which link are you talking about? When I hold enter key for a second, that's enought to spawn IE. Am I missing something?

### do...@chromium.org (2018-07-19)

#4: ah, true, I was looking at a different test for this.

Nevertheless, I still think that the requirement for users to hold down Enter at a particular time is a sufficient mitigation to make this Low severity.

### s....@gmail.com (2018-07-19)

https://bugs.chromium.org/p/chromium/issues/detail?id=637098#c51 concluded that holding enter key wouldn't decrease the severity to low.

### do...@chromium.org (2018-07-19)

#5: these seem like rather different vulnerabilities to me. https://crbug.com/chromium/637098 bug exposes a user's file system to the web when Enter is held. This one launches a program on the user's computer when Enter is held. Here, more steps required to leak user information (the attacker needs a vulnerability in an installed app that is being launched or control of that app, or something along those lines). This is not something that the website necessarily has direct control over.

### do...@chromium.org (2018-07-19)

For Mac, users will need to enable Full Keyboard Access in their keyboard settings (so that Tab traverses buttons) to allow keyboard-only access to the dialog. This seems like a reasonable requirement (the change is that previously, Enter / Space would have accepted. Now they need Full Keyboard Access, then Tab to select the accept button, then Enter to use the keyboard to accept).

### bu...@chromium.org (2018-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ca025d47d93664b3dcce6b7cbe9ea58b7d085cd4

commit ca025d47d93664b3dcce6b7cbe9ea58b7d085cd4
Author: Dominick Ng <dominickn@chromium.org>
Date: Thu Jul 19 02:49:06 2018

Set Cancel as the default button for the external protocol dialog.

This ensures that users holding down the Enter or Space key cannot
accidentally trigger an external protocol launch.

BUG=865202

Change-Id: I2cec7b3c216b80641200c97dec2517a66b4e0b24
Reviewed-on: https://chromium-review.googlesource.com/1142705
Commit-Queue: Dominick Ng <dominickn@chromium.org>
Reviewed-by: Trent Apted <tapted@chromium.org>
Cr-Commit-Position: refs/heads/master@{#576340}
[modify] https://crrev.com/ca025d47d93664b3dcce6b7cbe9ea58b7d085cd4/chrome/browser/ui/views/external_protocol_dialog.cc
[modify] https://crrev.com/ca025d47d93664b3dcce6b7cbe9ea58b7d085cd4/chrome/browser/ui/views/external_protocol_dialog.h


### s....@gmail.com (2018-07-19)

FYI, I think it's bit unclear to users when external protocol request happens from iframe. No origin of requester shown. Maybe it's better to disable that from an iframe?

https://shhnjk.azurewebsites.net/iframer.php?url=//test.shhnjk.com/location.php?url=microsoft-edge:https://www.google.com

### s....@gmail.com (2018-07-20)

BTW, this bug was originally reported to Edge by 
"greencardesh@hotmail" (in a totally different form of bug).
I reported this to make sure that Chrome folks are aware about the bug and will fix before the finder's write-up.

So I don't need bounty on this bug even if this bug is eligible. But maybe bounty should be paid to "greencardesh@hotmail" instead.

But please add "Restrict-View-SecurityEmbargo" in this bug because Edge are yet to ship the patch.

Thanks.

### do...@chromium.org (2018-07-21)

#11: thanks for passing along the heads up. Do you know when Edge will ship the patch?

### sh...@chromium.org (2018-07-21)

[Empty comment from Monorail migration]

### s....@gmail.com (2018-07-21)

Nothing decided yet but we are planning for september's update (could be delayed).

### aw...@chromium.org (2018-07-23)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### do...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-08-06)

Thanks!  Will process the reward for greencardesh@

### s....@gmail.com (2018-08-06)

Thanks! Nice Label :D

### aw...@chromium.org (2018-08-06)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-08)

I presume Edge has now patched, so it's OK to open this up?

### s....@gmail.com (2019-01-08)

Yes, we patched it :)

### aw...@google.com (2020-07-07)

Remove allpublic from bugs that have Restrict-View-SecurityEmbargo

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/865202?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HTML>CustomHandlers, UI]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091960)*
