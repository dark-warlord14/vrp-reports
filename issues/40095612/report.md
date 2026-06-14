# UAP in SetDispatchContext

| Field | Value |
|-------|-------|
| **Issue ID** | [40095612](https://issues.chromium.org/issues/40095612) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo>Bindings |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2019-07-05 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36

Steps to reproduce the problem:
1. Build asan version of chrome.Or use asan-linux-release-674733 directly.
2. Put ws.js and other js(release from res.zip) into the same dir with poc.html and use nodejs to setup a webserver: node ws.js
3. Run chrome  http://127.0.0.1:8605/poc.html

What is the expected behavior?

What went wrong?
Can get UAP crash stably.

Did this work before? N/A 

Chrome version: 77.0.3844.0  Channel: n/a
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [ws.js](attachments/ws.js) (text/plain, 1.2 KB)

## Timeline

### li...@chromium.org (2019-07-08)

Assigning to Ken, who's made some recent changes to binding_set.h. Would you be able to help take a look at this? Feel free to reassign if you're not the right owner for this. Thanks!

[Monorail components: Internals>Mojo>Bindings]

### ro...@google.com (2019-07-09)

This is not a bug in BindingSet, but probably in FileSystemDispatcher: https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/filesystem/file_system_dispatcher.h?rcl=3eaaeefc782c0ab628c00987e6f8bc34b88ba5c0&l=29

Generally when we see UAP it's because a garbage-collected object owns one or more Mojo bindings bound to itself, and fails to properly reset those bindings before being GCed. I see that this class is finalized though, so I have no idea specifically what's going wrong in this case. Adding some Blink folks for insight/advice, and assigning to tonikitoo@ as (I think) primary author of this code.

### to...@chromium.org (2019-07-09)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-07-09)

Being finalized has nothing to do with cleaning up before being GCed, that just means that the constructor will eventually run. What is generally the easiest fix for these kinds of issues is adding a pre-finalizer and have that pre-finalizer close the mojo bindings.

### ha...@chromium.org (2019-07-10)

+1 to what Marjin said. (Unfortunately) for now Blink's GC objects that own mojo bindings manually need to reset the bindings in pre-finalizers...


### ro...@google.com (2019-07-17)

[Empty comment from Monorail migration]

### ro...@google.com (2019-07-17)

[Empty comment from Monorail migration]

### to...@chromium.org (2019-07-17)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-08-07)

Friendly ping from the security marshal. Just want to make sure this is being worked on, as this is a high severity bug impacting stable.

### to...@chromium.org (2019-08-09)

Sorry about the delay. I posted a fix in 1744375 Close FileSystemOperationListener bindings on PreFinalizer.
I am trying to verify it now before submitting.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cfd44efa92afda3eb1944ae2f862bd444553a78c

commit cfd44efa92afda3eb1944ae2f862bd444553a78c
Author: Antonio Gomes <tonikitoo@igalia.com>
Date: Fri Aug 09 20:14:51 2019

Close FileSystemOperationListener bindings on PreFinalizer

This is a speculative CL to the UAP observed on crbug.com/c/981492.
It basically early-closes FileSystemDispatcher's mojo bindings manually,
a common for Blink's GC objects that own mojo bindings.

BUG=981492
R=haraken@chromium.org, mek@chromium.org

Change-Id: I0ffff4798532df5dda1ee74e4bbe8a887b5c68ee
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1744375
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Auto-Submit: Antonio Gomes <tonikitoo@igalia.com>
Cr-Commit-Position: refs/heads/master@{#685700}

[modify] https://crrev.com/cfd44efa92afda3eb1944ae2f862bd444553a78c/third_party/blink/renderer/modules/filesystem/file_system_dispatcher.cc
[modify] https://crrev.com/cfd44efa92afda3eb1944ae2f862bd444553a78c/third_party/blink/renderer/modules/filesystem/file_system_dispatcher.h


### to...@chromium.org (2019-08-10)

I verified that [1] does not crash anymore. It is the first asan chrome binary that contains the fix.

https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-685701.zip?generation=1565383493216712&alt=media

### sh...@chromium.org (2019-08-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-10)

Requesting merge to beta M77 because latest trunk commit (685700) appears to be after beta branch point (681094).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-10)

This bug requires manual review: M77 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-08-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-08-14)

Congrats! The Panel decided to reward $3,000 for this report!

### na...@google.com (2019-08-14)

[Empty comment from Monorail migration]

### ad...@google.com (2019-08-19)

Had a quick chat with livvielin@ and we don't see any reason to believe this wouldn't also affect 76, so adding M-76 milestone and merge requests. This is an externally reported, high severity, stably-reproducing UaP so we should merge back to 76 if we possibly can. But of course only if we are completely confident of the stability of the fix.

### ad...@google.com (2019-08-21)

Assuming applicable to all major platforms.

### sr...@google.com (2019-08-22)

This has not been merged to M77 yet, so i would say we should wait for M77 for this , let me know if you think other wise adetaylor@

### ad...@google.com (2019-08-22)

OK. Sounds good.

### la...@google.com (2019-08-23)

tonikitoo@ - please respond to C#15 to consider M77 merge request

### to...@chromium.org (2019-08-23)

re https://crbug.com/chromium/981492#c15

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Yes

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/1744375

3. Has the change landed and been verified on master/ToT?

Yes

4. Why are these changes required in this milestone after branch?

Stability

5. Is this a new feature?

No

6. If it is a new feature, is it behind a flag using finch?

N/A

### sr...@google.com (2019-08-23)

[Empty comment from Monorail migration]

### la...@google.com (2019-08-24)

merge approved for M77 branch 3865

### sh...@chromium.org (2019-08-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@igalia.com (2019-08-27)

the cherry-pick has been created and merged at https://chromium-review.googlesource.com/c/chromium/src/+/1773398

### be...@chromium.org (2019-08-29)

This has been approved, please merge ASAP.

### to...@igalia.com (2019-08-29)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/981492?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095612)*
