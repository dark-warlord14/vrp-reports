# Policy page opens a file dialogue even if the Allow​File​Selection​Dialogs policy is set to false

| Field | Value |
|-------|-------|
| **Issue ID** | [40051582](https://issues.chromium.org/issues/40051582) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | nu...@protonmail.com |
| **Assignee** | yd...@chromium.org |
| **Created** | 2020-02-21 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0

Steps to reproduce the problem:
1. Start the Chromium browser with the "AllowFileSelectionDialogue" policy disabled.
2. Open the internal policy page (chrome://policy).
3. Press the "Export to JSON" button.

What is the expected behavior?
The button shouldn't open a file selection dialog.

What went wrong?
The button opens a file dialog.

Did this work before? N/A 

Chrome version: 82.0.4062.3 (Official Build) dev (64-bit) (cohort: Dev)  Channel: stable
OS Version: 10.0
Flash Version: 32.0.0.330

This is a rather critical bug, as opening the file selection dialog usually allows access to the systems file explorer and therefore full access to execute files on the system.
This could compromise machines in public that users are only meant to be able to use chrome in; online browser VMs like caracal.club or Cryb; and other such systems.

## Attachments

- [0004992.mp4](attachments/0004992.mp4) (video/mp4, 1.6 MB)

## Timeline

### nu...@protonmail.com (2020-02-21)

Please also note that I tested this in both the developer version (82.0.4062.3 (Official Build) dev (64-bit) (cohort: Dev)) as well as the stable version (80.0.3987.116 (Official Build) (64-bit) (cohort: Stable Installs Only)) of Google Chrome and it worked in both.
I used Firefox to post this bug report, which is why the User Agent that was automatically included in the report is wrong.
The User Agent of the Chrome Browser in test was "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36".

### aj...@google.com (2020-02-22)

Thanks for the report.

I have confirmed that this is happening on chrome://policy and that no other chrome:// pages have this bug.

Assigning to ydago via "blame" from https://source.chromium.org/chromium/chromium/src/+/master:components/policy/resources/webui/policy.html.


[Monorail components: Enterprise]

### [Deleted User] (2020-02-22)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### po...@chromium.org (2020-02-22)

According to this comment it's WAI: https://cs.chromium.org/chromium/src/chrome/browser/ui/webui/policy_ui_handler.cc?l=1017&rcl=8d1fe43a8abd9cf0c2d6beb1fb7a19ab16c0401e
The code (and comment) was added in 2017: https://crrev.com/c/579568/ Feature bug is https://crbug.com/745889
urusant@ is not on the team anymore, so adding Georges.

### nu...@protonmail.com (2020-02-23)

Allowing the user to open a file selection dialog allows an user to delete, create, edit and run files on the system as they wish, and could compromise systems that users are only allowed to use Chrome/Chromium on.
There is no good reason why this should be allowed on the 'Export to JSON' button on the policy screen. Most reasons one may have to disable the file explorer dialog would also apply to this dialog.
This is dangerous, especially as it is not even warned about in the documentation of the AllowFileSelectionDialogs policy ('whenever the user performs an action which would provoke a file selection dialog [...] a message is displayed instead and the user is assumed to have clicked Cancel')

### po...@chromium.org (2020-02-24)

I agree that this may lead to unwanted behavior according to your description, however as not an expert on desktop platform I can't weigh how well it aligns with our guarantees for the policy on Windows, Linux, Mac. I refer to Chrome Enterprise Browser team to answer it.
However, if we'll want to fix it, we need to check other places where file dialog might be created as the code is not resilient to skipping policy checks :-(

### pa...@chromium.org (2020-02-25)

I am unassigning from Yann so that we can go over this bug in the prioritization session on Thursday and evaluate the priority.

### ge...@chromium.org (2020-02-26)

#6 makes a good point.

I have no objections to changing this behavior and honoring the policy.

### ke...@chromium.org (2020-02-28)

parstarmovj@: Was this looked at for triage on your side yesterday? It's flagged as a medium severity security bug so it should have an owner.

### pa...@chromium.org (2020-03-03)

Reassigning back to Yann then

Please consider disabling the export button when the policy is effective.

Yann, please consider this as a P1 (likely higher than most other things on the list so please prioritize accordingly).

As a side note - offering a copy JSON to clipboard might be beneficial in the presence of this policy. Filed this here https://bugs.chromium.org/p/chromium/issues/detail?id=1058001

### yd...@chromium.org (2020-03-03)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3ab7de11a8c950ad4a094a0092db50db8c7c25bd

commit 3ab7de11a8c950ad4a094a0092db50db8c7c25bd
Author: Yann Dago <ydago@chromium.org>
Date: Fri Mar 06 20:01:31 2020

Policy WebUI: Enforce AllowFileSelectionDialogs policy on export json

Bug: 1054966
Change-Id: I93f73023e6e6bdc24c329c36b2b14323522a078c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2085156
Commit-Queue: Yann Dago <ydago@chromium.org>
Auto-Submit: Yann Dago <ydago@chromium.org>
Reviewed-by: Julian Pastarmov <pastarmovj@chromium.org>
Cr-Commit-Position: refs/heads/master@{#747820}

[modify] https://crrev.com/3ab7de11a8c950ad4a094a0092db50db8c7c25bd/chrome/browser/ui/webui/policy_ui_browsertest.cc
[modify] https://crrev.com/3ab7de11a8c950ad4a094a0092db50db8c7c25bd/chrome/browser/ui/webui/policy_ui_handler.cc


### yd...@chromium.org (2020-03-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-07)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-09)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-11)

Congrats! The Panel decided to award $500 for this report!

### na...@google.com (2020-03-11)

[Empty comment from Monorail migration]

### aj...@chromium.org (2020-04-16)

CC aee@ & tiborg for visibility.

### ad...@google.com (2020-05-13)

nurmarvin@protonmail.com - thanks for the report; how would you like to be credited in the Chrome release notes?

### nu...@protonmail.com (2020-05-13)

I think I'll just go with my full name, which would be "Marvin Witt".

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-15)

Thanks!

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-06-13)

This issue was migrated from crbug.com/chromium/1054966?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051582)*
