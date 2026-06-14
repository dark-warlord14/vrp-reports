# Security: SEE_MASK_FLAG_NO_UI behavior changes in Windows 10, allowing SmartScreen bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40090721](https://issues.chromium.org/issues/40090721) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | jk...@cornell.edu |
| **Assignee** | as...@chromium.org |
| **Created** | 2018-03-07 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

In the next Windows Release (Redstone 4), Windows Defender SmartScreen will honor the SEE\_MASK\_FLAG\_NO\_UI flag. This flag is passed through shellexecute when a user runs an executable, or other supported file, through the chrome download manager. Edge/Firefox/Windows Explorer do not pass this flag and are unaffected.

There are three problematic scenarios

1. Known malware - Blocked silently: We will not show any SmartScreen UI for these types of files, but the user will have no opportunity to override the block through chrome. The user will not have any indication that executing the file did anything.
2. Unknowns - The file is unknown to our service. This is a large number of files and all will be allowed. There is a chance for polymorphic malware to be bucketed here.
3. Offline - User is unable to contact smartscreen. Always allowed.

When SEE\_MASK\_FLAG\_NO\_UI is not set, all 3 cases will result in a block experience for the user.

**VERSION**  

Chrome Version: [64.0.3282.186] + [stable]  

Operating System: Windows 10 (Redstone 4)

**REPRODUCTION CASE**  

Known malware: <https://demo.smartscreen.msft.net/download/known/knownmalicious.exe>  

Unknown program: <https://demo.smartscreen.msft.net/download/unknown/freevideo.exe>  

Offline: Any of the above with internet on the machine off

## Timeline

### el...@chromium.org (2018-03-08)

I'm not sure why Chrome would pass SEE_MASK_FLAG_NO_UI here. 

[Monorail components: UI>Browser>Downloads]

### mb...@chromium.org (2018-03-09)

asanka: Would you mind taking a look at this?

### as...@chromium.org (2018-03-09)

I'll have a look.

### sh...@chromium.org (2018-03-10)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-03-16)

Did Microsoft document the change to SEE_MASK_FLAG_NO_UI anywhere? It seems surprising that this would be changed (loosening security) after over six years.

The comment on the constant suggests that we're doing this deliberately, but it's a bit misleading in that we only invoke the "openas" verb if the error returned from ShellExecute is explicitly "ERROR_NO_ASSOCIATION".

https://cs.chromium.org/chromium/src/ui/base/win/shell.cc?l=38&rcl=50905e908c1d8b750e730861696d59872d4c99eb

// Default ShellExecuteEx flags used with the "explore", "open" or default verb.
//
// See kDefaultOpenFlags for description SEE_MASK_NOASYNC flag.
// SEE_MASK_FLAG_NO_UI is used to suppress any error message boxes that might be
// displayed if there is an error in opening the file. Failure in invoking the
// "open" actions result in invocation of the "saveas" verb, making the error
// dialog superfluous.
const DWORD kDefaultOpenFlags = SEE_MASK_NOASYNC | SEE_MASK_FLAG_NO_UI;


### el...@chromium.org (2018-03-16)

I've confirmed this behavior change with a Partner SDE in Windows; the original reporter is from Microsoft as well.

Redstone 4 appears to be slated for a ship date in April. 

### as...@chromium.org (2018-03-16)

I believe I added the comment and the flag. The flag as documented was referring only to an error message. I believe we ran tests at the time to ensure that "this file was downloaded from the internet" warning would still show up.

I agree with #5 that the new behavior of loosened security in the presence of this flag is unexpected and not something that's implied by the documentation as it currently stands.

I'll remove the flag since it's likely to cause more harm than good at this point.

### as...@chromium.org (2018-03-17)

+sky@ for ui/base/win review.
+grt@ for chrome/installer review.

### bu...@chromium.org (2018-03-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bd0fde2518644eea1cc53a01e3e3cce1c70e7157

commit bd0fde2518644eea1cc53a01e3e3cce1c70e7157
Author: Asanka Herath <asanka@chromium.org>
Date: Mon Mar 19 11:50:42 2018

Remove use of SEE_MASK_FLAG_NO_UI from Chrome Windows installer.

This flag was originally added to ui::base::win to suppress a specific
error message when attempting to open a file via the shell using the
"open" verb. The flag has additional side-effects and shouldn't be used
when invoking ShellExecute().

R=grt@chromium.org

Bug: 819809
Change-Id: I7db2344982dd206c85a73928e906c21e06a47a9e
Reviewed-on: https://chromium-review.googlesource.com/966964
Commit-Queue: Greg Thompson <grt@chromium.org>
Reviewed-by: Greg Thompson <grt@chromium.org>
Cr-Commit-Position: refs/heads/master@{#544012}
[modify] https://crrev.com/bd0fde2518644eea1cc53a01e3e3cce1c70e7157/chrome/installer/util/google_chrome_distribution.cc


### bu...@chromium.org (2018-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5bcdfd9c5595a61f67faece0a8305b9c91f4326c

commit 5bcdfd9c5595a61f67faece0a8305b9c91f4326c
Author: Asanka Herath <asanka@chromium.org>
Date: Wed Apr 04 13:46:29 2018

Remove usage of SEE_MASK_FLAG_NO_UI from ui::base::win

The flag was originally added to suppress messages from popping up if
the Windows shell failed to open the specified item.

Specifically, the ui::base::win::OpenAnyViaShell() function handles the
case where ShellExecute() returns ERROR_NO_ASSOCIATION when invoked with
the "open" verb by attempting to invoke the same using the "openas"
verb. Thus an intervening error message would not have been useful.
However the SEE_MASK_FLAG_NO_UI flag may suppress other error messages
and may also have side-effects beyond the display of failure messages.
See bug for details.

Bug: 819809
Change-Id: I8def155aa11b14f9a57a8f66add193dc281971cb
Reviewed-on: https://chromium-review.googlesource.com/966963
Commit-Queue: Asanka Herath <asanka@chromium.org>
Reviewed-by: Eric Lawrence <elawrence@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/heads/master@{#548039}
[modify] https://crrev.com/5bcdfd9c5595a61f67faece0a8305b9c91f4326c/ui/base/win/shell.cc
[modify] https://crrev.com/5bcdfd9c5595a61f67faece0a8305b9c91f4326c/ui/base/win/shell.h


### as...@chromium.org (2018-04-04)

Let's let this go through a Canary before considering a merge.

### as...@chromium.org (2018-04-04)

Assuming this sticks, the changes should roll out to Chrome stable in early June at the latest. Let's evaluate a merge after its vetted on Canary.

### sh...@chromium.org (2018-04-04)

[Empty comment from Monorail migration]

### as...@chromium.org (2018-04-06)

Requesting merge to M66.

The change in #10 has gone through a Canary cycle (first seen on 67.0.3389.0 on Apr 5). The code change results in no user visible behavior change yet. But will affect how Chrome interacts with Microsoft SmartScreen on upcoming Windows releases.

It was tested manually since there are no tests for how Chrome affects shell file open behavior. Tested on Windows 7 and Windows 10.


### sh...@chromium.org (2018-04-06)

This bug requires manual review: We are only 10 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-04-09)

do you know how this affect interactions with SmartScreen? Have we tested it throughly? What are the downsides if we wait until M67 for this fix?

### el...@chromium.org (2018-04-09)

The interaction problems with SmartScreen are outlined in #0-- to wit:

There are three problematic scenarios
1. Known malware - Blocked silently: We will not show any SmartScreen UI for these types of files, but the user will have no opportunity to override the block through chrome. The user will not have any indication that executing the file did anything.
2. Unknowns - The file is unknown to our service. This is a large number of files and all will be allowed. There is a chance for polymorphic malware to be bucketed here.
3. Offline - User is unable to contact smartscreen. Always allowed.

The risk of waiting for M67 is that Windows 10 users on the Spring Creator's update (rolling out this month) is that Chrome 66 users will be less secure than users of other browsers (Edge/Firefox) that do not set the NO_UI flag.

### as...@chromium.org (2018-04-09)

In addition to #17, I tested the CL prior to landing https://chromium-review.googlesource.com/c/chromium/src/+/966963#message-19bf0b7169584fbcb9fd443f50fa1f978f23758c



### jk...@cornell.edu (2018-04-09)

It turns out I was provided incorrect information about Firefox. They are also passing the no_ui flag. Feedback has been reported to them as well and they are in the process of making the same change.

Sorry for the misinformation earlier. I verified that the rest of the information in my bug report is correct. Just wanted to make you informed in case that changes your decision.

-Jimmy

### ab...@chromium.org (2018-04-10)

Approving merge to M66. Branch:3359

### as...@chromium.org (2018-04-11)

Re-opening for merge.

### bu...@chromium.org (2018-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e07d807c1d0ae31a9e5206f8220b2de5c100fdc7

commit e07d807c1d0ae31a9e5206f8220b2de5c100fdc7
Author: Asanka Herath <asanka@chromium.org>
Date: Wed Apr 11 13:20:20 2018

Remove usage of SEE_MASK_FLAG_NO_UI from ui::base::win

The flag was originally added to suppress messages from popping up if
the Windows shell failed to open the specified item.

Specifically, the ui::base::win::OpenAnyViaShell() function handles the
case where ShellExecute() returns ERROR_NO_ASSOCIATION when invoked with
the "open" verb by attempting to invoke the same using the "openas"
verb. Thus an intervening error message would not have been useful.
However the SEE_MASK_FLAG_NO_UI flag may suppress other error messages
and may also have side-effects beyond the display of failure messages.
See bug for details.

Bug: 819809
Change-Id: I8def155aa11b14f9a57a8f66add193dc281971cb
Reviewed-on: https://chromium-review.googlesource.com/966963
Commit-Queue: Asanka Herath <asanka@chromium.org>
Reviewed-by: Eric Lawrence <elawrence@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#548039}(cherry picked from commit 5bcdfd9c5595a61f67faece0a8305b9c91f4326c)
Reviewed-on: https://chromium-review.googlesource.com/1007174
Reviewed-by: Asanka Herath <asanka@chromium.org>
Cr-Commit-Position: refs/branch-heads/3359@{#679}
Cr-Branched-From: 66afc5e5d10127546cc4b98b9117aff588b5e66b-refs/heads/master@{#540276}
[modify] https://crrev.com/e07d807c1d0ae31a9e5206f8220b2de5c100fdc7/ui/base/win/shell.cc
[modify] https://crrev.com/e07d807c1d0ae31a9e5206f8220b2de5c100fdc7/ui/base/win/shell.h


### sh...@chromium.org (2018-04-11)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2018-04-11)

Thanks sheriffbot! I was waiting for the beta builders to finish their runs with the merged patch, which they just did. :P

### aw...@google.com (2018-04-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-18)

Thanks for the prompt fix asanka@!  Btw, there's no need to re-open for merge: security bugs should just be marked as fixed once there's a fix available, so scripts know there's a fix that should be merged.  Cheers!

### aw...@chromium.org (2018-04-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-20)

Hi jkf49@ - the VRP panel decided to reward $500 for this report - many thanks.  A member of our finance team will be in touch to arrange for payment.  Also, how would you like to credited in Chrome release notes?

### aw...@google.com (2018-04-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/819809?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ba...@gmail.com (2024-04-29)

For historical interest and archaeology only: In the April 2024 security update for Windows, this behavior was changed. 

Windows now shows a security UI (the legacy Windows Attachment Execution Services security prompt, rather than the SmartScreen Unknown Program prompt shown normally) if an unknown-reputation executable is launched via ShellExecute/ShellExecuteEx(SEE_MASK_FLAG_NO_UI)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090721)*
