# UAP in UpdatePlaceholderImage

| Field | Value |
|-------|-------|
| **Issue ID** | [40095512](https://issues.chromium.org/issues/40095512) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | aa...@chromium.org |
| **Created** | 2019-06-26 |
| **Bounty** | $5,500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36

Steps to reproduce the problem:
1. Build asan 77.0.3835.0 version of chrome.
2. Release files from res.zip into the same dir level with poc.html.
3. Setup a webserver by node. node ws.js

What is the expected behavior?

What went wrong?
Can get uap crash stably.
I tested it on 77.0.3835.0,77.0.3828.0 and 77.0.3833.0.

Seems like that UnregisterPlaceholder() should be called in dispose() no matter placeholder_frame_ is null or not.That's also the patch suggestion.

Did this work before? N/A 

Chrome version: 77.0.3835.0  Channel: n/a
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- [asan.log](attachments/asan.log) (text/plain, 5.8 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### jd...@chromium.org (2019-06-27)

I can reproduce this (but it does take a bit).

aaronhk@: can you take a look at this? I'm also CCing fserb@ just in case.

The reporter is referencing here: https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/html/canvas/html_canvas_element.cc?l=155

[Monorail components: Blink>Canvas]

### sh...@chromium.org (2019-07-10)

aaronhk: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-25)

aaronhk: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-08-07)

Friendly ping from the security marshal. Just want to make sure this is being worked on, as it is a high severity bug impacting stable.

### aa...@chromium.org (2019-08-08)

@jdeblasio? How did you repro? Following the steps in one I get, in order, following the steps in #1:

`node ws.js`
Error: Cannot find module 'express'

So I try:
`npm install express`
`node ws.js`
Failed to load websocket module. Run "npm install websocket" and try again.

Now installing `npm install websocket` the server hangs with `node ws.js`, opening `http://localhost:8605/` (guessed the port from the code) and just get a `Cannot GET /`

If I try instead to `npm install` inside that directory it says
npm WARN saveError ENOENT: no such file or directory, open '/usr/local/.../package.json'

Renaming package-lock.json to package.json and running `npm install` again just restarts the process.


### aa...@chromium.org (2019-08-08)

Looks like the `ws.js` linked to in crbug.com/964214 might be what we need

### aa...@chromium.org (2019-08-08)

Okay, I can repro on ToT using the `ws.js` described in #7. It just takes a while.

### aa...@chromium.org (2019-08-08)

Fix suggested by OP works: https://chromium-review.googlesource.com/c/chromium/src/+/1744642

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2df8ea19c5bba87209e452cea8473c05ea7d5250

commit 2df8ea19c5bba87209e452cea8473c05ea7d5250
Author: Aaron Krajeski <aaronhk@chromium.org>
Date: Thu Aug 08 21:06:55 2019

Always unregister placeholder image in canvas

It's possible that it has been disposed but its ID still exists. This
can lead to UAP bugs.

Bug: 978793
Change-Id: Idb4639cb78110878a28ab3c50807174343a66033
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1744642
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Reviewed-by: Aaron Krajeski <aaronhk@chromium.org>
Commit-Queue: Fernando Serboncini <fserb@chromium.org>
Commit-Queue: Aaron Krajeski <aaronhk@chromium.org>
Cr-Commit-Position: refs/heads/master@{#685345}

[modify] https://crrev.com/2df8ea19c5bba87209e452cea8473c05ea7d5250/third_party/blink/renderer/core/html/canvas/html_canvas_element.cc


### aa...@chromium.org (2019-08-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-13)

Requesting merge to stable M76 because latest trunk commit (685345) appears to be after stable branch point (665002).

Requesting merge to beta M77 because latest trunk commit (685345) appears to be after beta branch point (681094).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-13)

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

### ab...@google.com (2019-08-13)

Approved for 77. 

Is this critical for M76? We are already at 100% stable rollout and only considering absolutely critical merges.

### ad...@google.com (2019-08-13)

It looks to be a trivial fix to an externally-reported UaF, so I do think we should merge it into M76 just in case we do another respin.

### fs...@chromium.org (2019-08-13)

I agree with #16.

### aa...@chromium.org (2019-08-13)

Done, cherry-picked into M76

### aa...@chromium.org (2019-08-13)

Oh wait, I jumped the gun. Need the merge approval for M76 before I can proceed.

### ab...@google.com (2019-08-13)

Thanks for more context. Approved for M76

### na...@google.com (2019-08-19)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-08-21)

Is the change merged to M76 and M77? If yes, please provide merged CLs here, remove "Merge-Approved-76" & "Merge-Approved-77" label and apply "merge-merged-3809" & "Merge-merged-3865" labels. 

### aa...@google.com (2019-08-21)

M76:
https://chromium-review.googlesource.com/c/chromium/src/+/1744642

M77:
https://chromium-review.googlesource.com/c/chromium/src/+/1764269

### ad...@google.com (2019-08-21)

Assuming it affects Android too.

### na...@google.com (2019-08-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-21)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-08-21)

Congrats! The Panel decided to reward $5,000 plus a $500 patching bonus for this report!

### na...@google.com (2019-08-21)

[Empty comment from Monorail migration]

### sr...@google.com (2019-08-22)

aaronhk@ Can you confirm if  this change got verified in Beta and dev channels ?

### ad...@google.com (2019-08-26)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2019-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2019-08-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/978793?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095512)*
