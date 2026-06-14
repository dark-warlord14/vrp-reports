# heap-use-after-free on  IsSweepingInProgress()

| Field | Value |
|-------|-------|
| **Issue ID** | [40092105](https://issues.chromium.org/issues/40092105) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebAudio, Blink>Workers |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2018-08-03 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. Build source code 
    config args.gn file as below:
		use_sanitizer_coverage = true
		is_asan = true
		is_debug = false
		enable_nacl = false
		treat_warnings_as_errors = false
	ninja -j4 -C out/chrome_asan chrome
2. Build a mini web server.
	I used python twisted module to build the webserver.
	1) copy js source files and crash.html into the htm dirctory 
	2) run python web.py
3. ./chrome http://127.0.0.1:8605/crash.html

What is the expected behavior?

What went wrong?
Can stable get UAF crash after the page refresh several times.
I tried successfully on version 70.0.3508.3 and 70.0.3509.0.

Did this work before? N/A 

Chrome version: 70.0.3508.3  Channel: n/a
OS Version: 16.04
Flash Version: 

Firstly i consider that the reason is ~AudioWorkletThread() called in NoMainThread,which cause the race condition on "s_ref_count_",and lead the ThreadState to be freed earlier than it should be.(in release version,DCHECK(IsMainThread()) may not work).

So i verify it by this :
1.Run crash.html on debug version.
2.Add some check code in ~AudioWorkletThread() to judge if it's called in NoMainThread.

But the result is strange:
1.In debug version, the same crash won't happen.(got another signal 6 crash,they have absolutely different stacktrace)
2.After patch judge code,in the release version,crash happened few.
3.The output of judge code shows that  ~AudioWorkletThread() only called in MainThread.

1,2 show that maybe im right,but 3 shows not.

The judge code is very simple like "if(!IsMainThread()) \ LOG()<<"im right""

That's what i can provide ~ wish it helps.

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### cl...@chromium.org (2018-08-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6202086669418496.

### cl...@chromium.org (2018-08-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4893357789413376.

### cl...@chromium.org (2018-08-03)

Testcase 6202086669418496 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6202086669418496.

### cl...@chromium.org (2018-08-03)

Testcase 4893357789413376 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4893357789413376.

### cl...@chromium.org (2018-08-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6305341743300608.

### cl...@chromium.org (2018-08-03)

Testcase 6305341743300608 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6305341743300608.

### mm...@chromium.org (2018-08-03)

I can't reproduce it locally either. Can you please try any of the recent revisions, e.g. https://storage.cloud.google.com/chromium-browser-asan/linux-release/asan-linux-release-580151.zip ?

### cd...@gmail.com (2018-08-06)

I tried asan-linux-release-579753 ,it can repro.Could u please try this version?

And may you can change the upper limit of number i in crash.html(in code "var i = 0; i<260") from 230 to 260 to make it more stable? 

### sh...@chromium.org (2018-08-06)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2018-08-06)

Trying asan-linux-release-579753, no luck so far. How long does it take for you to reproduce the crash?

### mm...@chromium.org (2018-08-06)

Also, are you using any specific ASAN_OPTIONS?

### cd...@gmail.com (2018-08-07)

Thank you to handle this.

It's stable on one of my machine.The crash takes about 5 times of page refresh to repro.
On another machine,more random,it may take about 3 times or more than a hundred  times.

And i did not use any specific ASAN_OPTIONS, all i tried is just downloading the asan-linux-release-579753 and running it.



### sh...@chromium.org (2018-08-07)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2018-08-07)

Thanks for the info. Are you using a single process computer or a multi process one? That might cause a difference, I guess.

I'm keeping browser running your PoC for a while (5-10 minutes) and it doesn't crash.

This also might be somewhat related to https://crbug.com/chromium/861624.

### cl...@chromium.org (2018-08-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4580103611482112.

### cl...@chromium.org (2018-08-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4599681481703424.

### cl...@chromium.org (2018-08-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4668452665819136.

### cl...@chromium.org (2018-08-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5147258304331776.

### mm...@chromium.org (2018-08-07)

Trying a bunch of different configs on ClusterFuzz, maybe something succeeds to reproduce this.

### cl...@chromium.org (2018-08-07)

Testcase 4580103611482112 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4580103611482112.

### cl...@chromium.org (2018-08-07)

Testcase 5147258304331776 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5147258304331776.

### ji...@chromium.org (2018-08-07)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-08-07)

I've been running that for a couple hours locally -- still no crash :/

One more question: how much RAM do you have on the machine where the crash is reproducible?

### ji...@chromium.org (2018-08-07)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebAudio]

### rt...@chromium.org (2018-08-07)

Was able to reproduce this on my Linux (840) machine with ToT chromium from this morning.  Looks like it's a GC problem or a worklet shutdown problem.

+nhiroki for the worklet issue.

### ji...@chromium.org (2018-08-07)

Based on #25, assign to nhiroki@. 

### cd...@gmail.com (2018-08-08)

 mmoroz@  
I use a multi process one.And ram is 32GB or 24GB,both are OK. 



### sh...@chromium.org (2018-08-08)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rt...@chromium.org (2018-08-10)

[Empty comment from Monorail migration]

### ca...@chromium.org (2018-08-15)

nhiroki: Have you had a chance to look at this one? This is a high severity security vulnerability.

### sh...@chromium.org (2018-08-17)

nhiroki: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nh...@chromium.org (2018-08-21)

Sorry for delayed action.

I understand the problem. See uaf.log on the original report. When WebThreadSupportingGC owns the underlying WebThread, WebThreadSupportingGC::ShutdownOnThread() stops the thread scheduler[1] and queued tasks never run. However, AudioWorklet injects its own WebThread into WebThreadSupportingGC[2], so WebThreadSupportingGC::ShutdownOnBackingThread() doesn't stop the thread scheduler and a GC task unexpectedly runs after ThreadState is detached.

[1] https://chromium.googlesource.com/chromium/src/+/ca5188075f09cd2e9790b3b863407313f21c1748/third_party/blink/renderer/platform/web_thread_supporting_gc.cc#70
[2] https://chromium.googlesource.com/chromium/src/+/8818a0a43de6f5d4e8d377cbf9634bf09ccb6642/third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc#73

[Monorail components: Blink>Workers]

### nh...@chromium.org (2018-08-21)

Probably WebThreadSupportingGC creates a WebThread based on WebThreadCreationParams.thread_type at [3] instead of AudioWorkletThread::EnsureSharedBackingThread()[2] so that WebThreadSupportingGC owns the thread and stops the scheduler on shutdown.

[3] https://chromium.googlesource.com/chromium/src/+/e830534349791e9fa99b52dd7b8e201d426d12bf/third_party/blink/renderer/platform/web_thread_supporting_gc.cc#38

### ho...@chromium.org (2018-08-21)

Thanks for taking a look on that. I see that it can be a problem, but how do we resolve this? When WebThreadSupportingGC doesn't own the thread, somehow should it signal AudioWorkletThread to do the shutdown there when it is going away?

### ho...@chromium.org (2018-08-21)

I made the https://crbug.com/chromium/870678#c34 before I saw #33. The plan in #33 sounds sensible.

### nh...@chromium.org (2018-08-21)

^^^ Probably WebThreadSupportingGC *SHOULD* create a WebThread based on WebThreadCreateParams.thread_type at [3].

I'm going to make a patch after 2 days ooo (Aug 22-23). If you're interested in fixing this, feel free to own this issue without waiting for me :)

### nh...@chromium.org (2018-08-21)

Ah, I made the https://crbug.com/chromium/870678#c36 before I saw #34 and #35 :p

### ho...@chromium.org (2018-08-22)

nhiroki@: Well, I've tried and I think we have a couple of issues.

1. Who does own this new WebThreadSupportingGC? I think it should be AudioWorkletThread, but you might have a different idea.
2. AudioWorkletThread::s_backing_thread_ is a raw & static pointer, so changing it to unique_ptr is not really feasible. (Please advise if you know how) Without the smart pointer, can we still expect it to behave like what you explained above?
3. To set the thread priority, base::ThreadPriority is needed in AudioWorkletThread. I don't think it can be used in modules/.

Here's WIP CL: https://chromium-review.googlesource.com/c/chromium/src/+/1185740

WDYT?

### nh...@chromium.org (2018-08-24)

Reg c#38: Thank you for working on this. I replied in the WIP CL:
https://chromium-review.googlesource.com/c/chromium/src/+/1185740#message-503b84e96cca48e1f1d373dd8cebd5e1cb3d5725

### ho...@chromium.org (2018-08-24)

FWIW, I can't reproduce this bug locally. The fix in CL is still valid and good to have, so I hope we can land it before M70 cut.

### bu...@chromium.org (2018-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6c0be75b8eb80192a5fb12aa56bbec075f466274

commit 6c0be75b8eb80192a5fb12aa56bbec075f466274
Author: Hongchan Choi <hongchan@chromium.org>
Date: Mon Aug 27 18:01:16 2018

Change the ownership of backing thread in AudioWorkletThread

To clarify the life cycle of backing thread in AudioWorkletThread,
now WorkletThreadHolder<AudioWorkletThread> owns the thread in a
form of WebThreadSupportingGC. By doing so, this CL removes a
static singleton WebThread instance from AudioWorkletThread class.

Bug: 870678
Test: All existing AudioWorklet tests (layout, unit) passes.
Change-Id: I4b9a0a2daebbead53604fbee4dda8052fe09cd37
Reviewed-on: https://chromium-review.googlesource.com/1185740
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Reviewed-by: Hiroki Nakagawa <nhiroki@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#586314}
[modify] https://crrev.com/6c0be75b8eb80192a5fb12aa56bbec075f466274/third_party/blink/renderer/modules/webaudio/audio_worklet_thread.cc
[modify] https://crrev.com/6c0be75b8eb80192a5fb12aa56bbec075f466274/third_party/blink/renderer/modules/webaudio/audio_worklet_thread.h
[modify] https://crrev.com/6c0be75b8eb80192a5fb12aa56bbec075f466274/third_party/blink/renderer/platform/web_thread_supporting_gc.cc


### ho...@chromium.org (2018-08-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-11)

Hello! The VRP panel looked at this bug and, considering it medium severity, awarded $1,000. Thanks!

### aw...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-09-12)

Thanks :) 

### aw...@google.com (2018-09-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/870678?no_tracker_redirect=1

[Multiple monorail components: Blink>WebAudio, Blink>Workers]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092105)*
