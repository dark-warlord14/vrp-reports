# UAP in offline audio context

| Field | Value |
|-------|-------|
| **Issue ID** | [40095460](https://issues.chromium.org/issues/40095460) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection, Blink>WebAudio |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2019-06-20 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36

Steps to reproduce the problem:
1. Build asan 77.0.3832.0 version of chrome.Or download asan-linux-release-670818.
2. Release files from htm.zip into htm dir and put ws.js into the same level with htm dir.The directory tree looks like this
|----ws.js
|----htm  
    |----poc.html
    |----other res js file

3. Use nodejs to setup a webserver: node ws.js
(maybe you'll need to install express and websocket package:npm install express websocket)

3. Run chrome http://127.0.0.1:8605/poc.html

What is the expected behavior?

What went wrong?
When offline audio starts rendering, it would check the pre-render task and stop rendering loop if needed. Once rendering has been suspended, the rendering thread would post a Notify task into main thread. If the audio's execution context (frame pointer from v8 context) was removed and garbage-collected while the Notify task is in the sequence，once the main thread runs the task, the GetExecutionContext function will visit the frame and UAP happened.

I tested it on version 77.0.3828.0, 77.0.3830.0 and 77.0.3832.0.All can repro stably.It's might be a re-opened issue of 959700.

Did this work before? N/A 

Chrome version: 77.0.3832.0  Channel: n/a
OS Version: 16.04
Flash Version:

## Attachments

- [htm.zip](attachments/htm.zip) (application/octet-stream, 34.7 KB)
- [ws.js](attachments/ws.js) (text/plain, 1.1 KB)
- [chrome-use-after-poison-operator.txt](attachments/chrome-use-after-poison-operator.txt) (text/plain, 4.6 KB)

## Timeline

### me...@chromium.org (2019-06-20)

I was able to repro this after a retry.
hongchan@ could you please take a look? Thanks!

[Monorail components: Blink>WebAudio]

### ho...@chromium.org (2019-06-20)

haraken@

I would like to have your opinion on this. Calling ContextLifecycleStateObserver::GetExecutionContext() after the execution context is GCed would be illegal? If it is illegal, this could be a real problem because we have several other places doing the same thing. (A simple code search shows 41 occurrences)

Also this fails here: https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/webaudio/offline_audio_destination_node.cc?l=269
```
if (Context() && Context()->GetExecutionContext())
                            ^^^^^^^^^^^^^^^^^^^^^<UAP>
    Context()->ResolveSuspendOnMainThread(frame);
```

I am not sure how Context() can be valid when ExecutionContext is GCed.

### ho...@chromium.org (2019-06-20)

(The <UAP> note above needs the "code" font to be displayed correctly)

### rt...@chromium.org (2019-06-20)

This is very repeatable for me on Linux and crashes in a couple of sec.  Thanks for the updated test!

### ha...@chromium.org (2019-06-21)

Re #2:

> Calling ContextLifecycleStateObserver::GetExecutionContext() after the execution context is GCed would be illegal?

That's a far more fundamental problem. If the execution context is GCed, the |this| object is already gone. So you shouldn't be able to call ContextLifecycleStateObserver::GetExecutionContext() in the first place.



### mm...@chromium.org (2019-07-01)

Speculatively setting Security_Impact-Stable as per c#0. Please change if that's not correct.

### sh...@chromium.org (2019-07-05)

hongchan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2019-07-08)

I was also able to reproduce this almost instantly, but I can't understand how this is possible. 

A BaseAudioContext depends on an ExecutionContext. However, somehow Context() is valid when GetExecutionContext() crashes because it tries to access the memory that is already invalided (poisoned) by ASAN. I really don't think this is a WebAudio problem.

haraken@ Would you mind taking a look or assign someone more knowledgeable on GC?

[Monorail components: Blink>JavaScript>GC]

### rt...@chromium.org (2019-07-08)

[Empty comment from Monorail migration]

### ha...@chromium.org (2019-07-09)

I think this is a WebAudio's lifetime management problem.

> . However, somehow Context() is valid when GetExecutionContext() crashes because it tries to access the memory that is already invalided (poisoned) by ASAN. 

No, that crash means that Context() is already invalid. The UAP does not happen until it actually accesses a member of Context(), so it's firing at Context()->GetExecutionContext().

AudioHandler is pointing to AudioHandler::context_ using an UntracedMember. How is it guaranteed that the context_ is alive until OfflineAudioDestinationHandler::NotifySuspend is invoked?



### ho...@chromium.org (2019-07-09)

Hmm. I tried CHECK(Context()) right above the if statement and it doesn't crash. Also if it is invalid, how does it pass the if statement?

I feel like this is not a complete or proper fix, but it at least blocks UAP:
https://chromium-review.googlesource.com/c/chromium/src/+/1693163

Anything more than this will require a bit of refactoring/redesigning.

### ho...@chromium.org (2019-07-09)

Ah. Now I see. Context() looks valid because it's technically a raw pointer and it might point to some non-null garbage.

Thanks for the advice, haraken@!

### ho...@chromium.org (2019-07-09)

I also found another problem:
https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/webaudio/base_audio_context.cc?sq=package:chromium&g=0&l=115

The destination handler is being cleared without clearing its untraced |context_| member. I think we should call ClearContext() before nullifying the destination handler. Then we might be able to remove the little hack like IsExecutionContextDestroyed() flag.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2e0071db3e8af7c47a9962353913ffd7b7436e13

commit 2e0071db3e8af7c47a9962353913ffd7b7436e13
Author: Hongchan Choi <hongchan@chromium.org>
Date: Thu Jul 11 15:04:39 2019

Avoid accessing context's fields after destruction

AudioHandler::Context() returns an untraced raw pointer to the
context so checking its value might be pointing some non-null
garbage after the context is gone. In that case, invoking
GetExecutionContext() might return a pointer to some random
memory space.

By checking a local flag on ExecutionContext's validity,
we can avoid such memory access.

Bug: 977107
Test: ASAN build does not crash on a repro code with the fix.
Change-Id: I19020e019cc3d9d52de3bebbe23129e7dd7b0a5e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1693163
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#676431}

[modify] https://crrev.com/2e0071db3e8af7c47a9962353913ffd7b7436e13/third_party/blink/renderer/modules/webaudio/offline_audio_destination_node.cc


### ho...@chromium.org (2019-07-11)

I'll let this sit for few days and will try to merge M76 beta.

### ho...@chromium.org (2019-07-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-13)

Requesting merge to M76 because latest trunk commit (676431) appears to be after beta branch point (665002).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-13)

This bug requires manual review: M76 has already been promoted to the beta branch, so this requires manual review
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
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### ho...@chromium.org (2019-07-15)

Re #19:

1. Not sure what the definitive answer on this, but It was found after M76 beta period. And the code change is tiny (1-line) so it's straightforward to merge.
2. https://chromium-review.googlesource.com/c/chromium/src/+/1693163
3. Yes.
4, It's P1 and has impact on security
5. No.
6. No.

### ab...@google.com (2019-07-15)

branch:3809

### cr...@appspot.gserviceaccount.com (2019-07-15)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/e85c8c90b6bb6f01149cfa603c5472a082f2719a

Commit: e85c8c90b6bb6f01149cfa603c5472a082f2719a
Author: hongchan@chromium.org
Commiter: hongchan@chromium.org
Date: 2019-07-15 17:32:24 +0000 UTC

Avoid accessing context's fields after destruction

AudioHandler::Context() returns an untraced raw pointer to the
context so checking its value might be pointing some non-null
garbage after the context is gone. In that case, invoking
GetExecutionContext() might return a pointer to some random
memory space.

By checking a local flag on ExecutionContext's validity,
we can avoid such memory access.

(cherry picked from commit 2e0071db3e8af7c47a9962353913ffd7b7436e13)

Bug: 977107
Test: ASAN build does not crash on a repro code with the fix.
Change-Id: I19020e019cc3d9d52de3bebbe23129e7dd7b0a5e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1693163
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#676431}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1701610
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/branch-heads/3809@{#843}
Cr-Branched-From: d82dec1a818f378c464ba307ddd9c92133eac355-refs/heads/master@{#665002}


### na...@google.com (2019-07-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-17)

Congrats! The Panel decided to reward $3,000 for this report!

### cd...@gmail.com (2019-07-18)

Thanks for the reward, Cheers!

### na...@google.com (2019-07-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-29)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### aw...@google.com (2020-07-15)

Hi cdsrc2016@ - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### is...@google.com (2020-07-15)

This issue was migrated from crbug.com/chromium/977107?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>GarbageCollection, Blink>WebAudio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095460)*
