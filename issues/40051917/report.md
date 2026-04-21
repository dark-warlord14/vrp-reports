# Security: UAF in Speech Recognizer

| Field | Value |
|-------|-------|
| **Issue ID** | [40051917](https://issues.chromium.org/issues/40051917) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Speech |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2020-04-04 |
| **Bounty** | $25,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36

Steps to reproduce the problem:
Run the attached script. The vulnerability can be triggered in two ways.

1.
$python -m SimpleHTTPServer&
$./out/Asan/chrome --user-data-dir="/tmp/xxxx" http://localhost:8000/index.html http://localhost:8000/index.html

2.
$python -m SimpleHTTPServer&
$./out/Asan/chrome --user-data-dir="/tmp/xxxx" --headless --screenshot http://localhost:8000/index_headless.html

It may take several tries for the first trigger method. (For me about 3 success/ 5 times)

What is the expected behavior?

What went wrong?
```
void SpeechRecognizerImpl::StopAudioCapture() {
  base::PostTask(FROM_HERE, {BrowserThread::IO},
                 base::BindOnce(&SpeechRecognizerImpl::DispatchEvent, this,
                                FSMEventArgs(EVENT_STOP_CAPTURE)));
}
```
[1]
DispatchEvent can be executed in the IO thread after SpeechRecognitionManagerImpl is destroyed. 

Then call AbortSilently[2]:

```SpeechRecognizerImpl::ExecuteTransitionAndGetNextState(
    const FSMEventArgs& event_args) {
  const FSMEvent event = event_args.event;
  switch (state_) {
    case STATE_IDLE:
      switch (event) {
        [...]
        case EVENT_STOP_CAPTURE:
          return AbortSilently(event_args);
        [...]
```

Finally arrives at SpeechRecognizerImpl :: Abort[3]. It will access listener() and listener_ is SpeechRecognitionManagerImpl[4]:
```
SpeechRecognizerImpl::FSMState SpeechRecognizerImpl::Abort(
    const blink::mojom::SpeechRecognitionError& error) {
  DCHECK_CURRENTLY_ON(BrowserThread::IO);

  [...]

  if (state_ > STATE_WAITING_FOR_SPEECH && state_ < STATE_WAITING_FINAL_RESULT)
    listener()->OnSoundEnd(session_id());

  if (state_ > STATE_STARTING && state_ < STATE_WAITING_FINAL_RESULT)
    listener()->OnAudioEnd(session_id());

  if (error.code != blink::mojom::SpeechRecognitionErrorCode::kNone)
    listener()->OnRecognitionError(session_id(), error);

  listener()->OnRecognitionEnd(session_id());

  return STATE_ENDED;
```

This critical bug may cause the sandbox to escape without RCE.

[1]https://source.chromium.org/chromium/chromium/src/+/master:content/browser/speech/speech_recognizer_impl.cc;l=240;drc=57f988dd7c1f63f59b44282efcc9e6f1e85ac19c;bpv=1;bpt=0?originalUrl=https:%2F%2Fcs.chromium.org%2F
[2]https://source.chromium.org/chromium/chromium/src/+/master:content/browser/speech/speech_recognizer_impl.cc;l=374;drc=28442cacc3be1a7d05a898aba663025a143095ac;bpv=0;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F
[3]https://source.chromium.org/chromium/chromium/src/+/master:content/browser/speech/speech_recognizer_impl.cc;drc=28442cacc3be1a7d05a898aba663025a143095ac;bpv=0;bpt=1;l=720?originalUrl=https:%2F%2Fcs.chromium.org%2F
[4]https://source.chromium.org/chromium/chromium/src/+/master:content/browser/speech/speech_recognition_manager_impl.cc;l=295;drc=28442cacc3be1a7d05a898aba663025a143095ac;bpv=1;bpt=1?originalUrl=https:%2F%2Fcs.chromium.org%2F

Did this work before? N/A 

Chrome version:   Channel: n/a
OS Version: 
Flash Version: 

Reporter credit: Leecraso and Guang Gong of Alpha Lab, Qihoo 360.

## Attachments

- [index.html](attachments/index.html) (text/plain, 339 B)
- [asan](attachments/asan) (text/plain, 15.2 KB)
- [index_headless.html](attachments/index_headless.html) (text/plain, 2.0 KB)
- [asan_headless](attachments/asan_headless) (text/plain, 16.6 KB)

## Timeline

### li...@chromium.org (2020-04-06)

[Empty comment from Monorail migration]

### li...@chromium.org (2020-04-06)

hans@, would you be able to help take a look or re-assign? Thanks!

[Monorail components: Blink>Speech]

### le...@gmail.com (2020-04-06)

I think this vulnerability might be critical, because triggering it does not actually require any command line parameters or compromised renderer.

### ha...@chromium.org (2020-04-07)

Thanks for the excellent repro!

This sounds similar to https://crbug.com/chromium/1018677. Here's a fix: https://chromium-review.googlesource.com/c/chromium/src/+/2139701

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0b2aaaa8a4948d88b892c3e6cabc87848f248e52

commit 0b2aaaa8a4948d88b892c3e6cabc87848f248e52
Author: Hans Wennborg <hans@chromium.org>
Date: Wed Apr 08 11:38:23 2020

SpeechRecognizerImpl: use a WeakPtr to itself for all tasks

It seems that during shutdown, SpeechRecognizerImpl can go away before the
posted task runs. This is similar to crrev.com/729694.

Bug: 1067851
Change-Id: I1c43d3bfaf978891f4abaef8e452a088d0f18c5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2139701
Reviewed-by: Primiano Tucci <primiano@chromium.org>
Reviewed-by: Tommi <tommi@chromium.org>
Reviewed-by: Olga Sharonova <olka@chromium.org>
Commit-Queue: Hans Wennborg <hans@chromium.org>
Cr-Commit-Position: refs/heads/master@{#757385}

[modify] https://crrev.com/0b2aaaa8a4948d88b892c3e6cabc87848f248e52/content/browser/speech/speech_recognizer_impl.cc


### ha...@chromium.org (2020-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

Requesting merge to stable M81 because latest trunk commit (757385) appears to be after stable branch point (737173).

Requesting merge to beta M81 because latest trunk commit (757385) appears to be after beta branch point (737173).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-09)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2020-04-13)

+Adetaylor@(Security TPM)

hans@ please reply to https://crbug.com/chromium/1067851#c9 which helps in approval process.

### pb...@google.com (2020-04-13)

Also want to check if we need the Cl to get merged to M83 Branch? if so please request cc'ing Srinivas.

### pb...@google.com (2020-04-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-04-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5682236318351360.

### ad...@chromium.org (2020-04-13)

I agree with https://crbug.com/chromium/1067851#c3 that this seems to be critical severity.

The fix is extremely simple and correct-looking, so I'm approving merge to M83 (branch 4103) and M81 (branch 4044). Please merge.

### ad...@chromium.org (2020-04-13)

Un-approving merge to 81 whilst I discuss further...

### ad...@chromium.org (2020-04-13)

Re-approving M81 merge.

### ad...@chromium.org (2020-04-13)

hans@ - I'm assuming this affects all platforms except iOS (most importantly, it affects Android and ChromeOS as well as the desktop platforms). As far as you know, is that correct? We may well want to trigger an out-of-sequence stable respin for this bug this week, so it's really important we get the platforms right. Thanks!

### ad...@chromium.org (2020-04-13)

leecraso@ - thanks for the report.

### aw...@google.com (2020-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-13)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-04-13)

Testcase 5682236318351360 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5682236318351360.

### ad...@chromium.org (2020-04-13)

Marking RBS as requested by release TPM team as this is Critical.

### ad...@chromium.org (2020-04-13)

govind@ intends to merge this into M83 today if it's a clean merge.

### go...@chromium.org (2020-04-13)

[Empty comment from Monorail migration]

### go...@chromium.org (2020-04-13)

M83 merge in CQ - https://chromium-review.googlesource.com/c/chromium/src/+/2147541

### na...@google.com (2020-04-13)

[Empty comment from Monorail migration]

### go...@chromium.org (2020-04-13)

+ Android and Chrome OS M81 Release TPMS , Clank Test lead for visibility.

### go...@chromium.org (2020-04-13)

Please merge your change to M83 branch 4103 ASAP (before 3:00 PM PT today,Monday) so we can pick it up for this week Dev/Beta release. Thank you.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1b59734a751aad771346c6c34f44800e2c3b0345

commit 1b59734a751aad771346c6c34f44800e2c3b0345
Author: Hans Wennborg <hans@chromium.org>
Date: Mon Apr 13 20:13:26 2020

SpeechRecognizerImpl: use a WeakPtr to itself for all tasks

It seems that during shutdown, SpeechRecognizerImpl can go away before the
posted task runs. This is similar to crrev.com/729694.

Bug: 1067851
Change-Id: I1c43d3bfaf978891f4abaef8e452a088d0f18c5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2139701
Reviewed-by: Primiano Tucci <primiano@chromium.org>
Reviewed-by: Tommi <tommi@chromium.org>
Reviewed-by: Olga Sharonova <olka@chromium.org>
Commit-Queue: Hans Wennborg <hans@chromium.org>
Cr-Commit-Position: refs/heads/master@{#757385}
(cherry picked from commit 0b2aaaa8a4948d88b892c3e6cabc87848f248e52)

TBR=hans@chromium.org

Change-Id: I1c43d3bfaf978891f4abaef8e452a088d0f18c5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2147541
Reviewed-by: Krishna Govind <govind@chromium.org>
Reviewed-by: Adrian Taylor <adetaylor@google.com>
Commit-Queue: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#105}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/1b59734a751aad771346c6c34f44800e2c3b0345/content/browser/speech/speech_recognizer_impl.cc


### ha...@chromium.org (2020-04-14)

Apologies for being slow to reply, Monday was a public holiday here.

Regarding the severity, this is a browser-process use-after-free that can be triggered from JavaScript. I'd imagine it's pretty hard to exploit though, and also it happens during browser shutdown, so while it certainly makes sense to merge it I can't judge whether it is bad enough to trigger any respins.

As for affected platforms, I believe this affects all desktop platforms, but not Android or iOS.

Android doesn't use SpeechRecognizerImpl, but has its own SpeechRecognizerImplAndroid variant instead. (These are created in SpeechRecognitionManagerImpl::CreateSession).

On iOS this is not an issue since blink isn't used.


I don't actually know how to merge this to release branches, but am happy to stamp any patches to do so (already done for M83).

### be...@chromium.org (2020-04-14)

I have prepped the CL here: https://chromium-review.googlesource.com/c/chromium/src/+/2148952

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9a8f835f66472f044da1d0a88c574c6b7f6d776f

commit 9a8f835f66472f044da1d0a88c574c6b7f6d776f
Author: Hans Wennborg <hans@chromium.org>
Date: Tue Apr 14 15:21:17 2020

SpeechRecognizerImpl: use a WeakPtr to itself for all tasks

It seems that during shutdown, SpeechRecognizerImpl can go away before the
posted task runs. This is similar to crrev.com/729694.

(cherry picked from commit 0b2aaaa8a4948d88b892c3e6cabc87848f248e52)

Bug: 1067851
Change-Id: I1c43d3bfaf978891f4abaef8e452a088d0f18c5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2139701
Reviewed-by: Primiano Tucci <primiano@chromium.org>
Reviewed-by: Tommi <tommi@chromium.org>
Reviewed-by: Olga Sharonova <olka@chromium.org>
Commit-Queue: Hans Wennborg <hans@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#757385}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2148952
Reviewed-by: Ben Mason <benmason@chromium.org>
Reviewed-by: Hans Wennborg <hans@chromium.org>
Commit-Queue: Ben Mason <benmason@chromium.org>
Cr-Commit-Position: refs/branch-heads/4044@{#926}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/9a8f835f66472f044da1d0a88c574c6b7f6d776f/content/browser/speech/speech_recognizer_impl.cc


### ad...@google.com (2020-04-14)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-15)

Congrats! The Panel decided to award you $25,000 for this report. 

### na...@google.com (2020-04-15)

[Empty comment from Monorail migration]

### ol...@chromium.org (2020-04-29)

[Empty comment from Monorail migration]

### jo...@chromium.org (2020-04-30)

(As part of testing a new process to reduce the Chrome OS patch gap I have cherry-picked this fix for M80 -- this is just a test.)

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b69991a9b701904ef9bdfd01090d978b00100522

commit b69991a9b701904ef9bdfd01090d978b00100522
Author: Hans Wennborg <hans@chromium.org>
Date: Thu Apr 30 00:20:16 2020

SpeechRecognizerImpl: use a WeakPtr to itself for all tasks

It seems that during shutdown, SpeechRecognizerImpl can go away before the
posted task runs. This is similar to crrev.com/729694.

(cherry picked from commit 0b2aaaa8a4948d88b892c3e6cabc87848f248e52)

(cherry picked from commit 9a8f835f66472f044da1d0a88c574c6b7f6d776f)

Bug: 1067851
Change-Id: I1c43d3bfaf978891f4abaef8e452a088d0f18c5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2139701
Reviewed-by: Primiano Tucci <primiano@chromium.org>
Reviewed-by: Tommi <tommi@chromium.org>
Reviewed-by: Olga Sharonova <olka@chromium.org>
Commit-Queue: Hans Wennborg <hans@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#757385}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2148952
Reviewed-by: Ben Mason <benmason@chromium.org>
Reviewed-by: Hans Wennborg <hans@chromium.org>
Commit-Queue: Ben Mason <benmason@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4044@{#926}
Cr-Original-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2173741
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Commit-Queue: Jorge Lucangeli Obes <jorgelo@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#1040}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/b69991a9b701904ef9bdfd01090d978b00100522/content/browser/speech/speech_recognizer_impl.cc


### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1067851?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1067853, crbug.com/chromium/1075847]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051917)*
