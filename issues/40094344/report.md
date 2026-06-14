# UAF in TaskQueueImpl::CreateTaskRunner

| Field | Value |
|-------|-------|
| **Issue ID** | [40094344](https://issues.chromium.org/issues/40094344) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Workers |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | nh...@chromium.org |
| **Created** | 2019-03-21 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. run chromium 75.0.3736.0 asan .
2. Set up a webserver and put poc.html 
3. Run ./chrome  poc.html 

What is the expected behavior?

What went wrong?
When creating a sharedworker, the main thread fetchs a script and create a backing thread then notify the script was evaluated.
The shared worker thread handle its own task loop.But if worker shutdown at the special time, there might be something wrong.

Main thread : fetch script --> create thread --> notify WorkerScriptEvaluated --> get task queue
                                                                                         |
                                                                                         |<---- once it comes here at the same time, race occurs.
                                                                                         | 
Worker thread : start -->run task loop --> ready to die --> dispose task queue --> free task queue

If the race condition happened,shared worker thread will free its pausable_task_queue_ member and free the impl_ member.And the use of TaskQueueImpl in main thread would lead to a UAF problem.

The way to repro is creating a shared worker and refreshing the page.
Because of the valid in: base/task/sequence_manager/task_queue.cc

scoped_refptr<SingleThreadTaskRunner> TaskQueue::CreateTaskRunner(
    int task_type) {
...
  if (!impl_)    <---check 
    return CreateNullTaskRunner();
  return impl_->CreateTaskRunner(task_type);
}

The UAF could only take place in this situation:check succeed then impl_ is freed by sequence_manager_ during impl_->CreateTaskRunner is executing, which means,it might be hard to repro.
On one of my machine the time of repro may be serveral minutes while it only repro once on my another machine. 
And there might be another poc that makes it repro easier. 

Im not sure if this is correct, buf hope it helps.

Did this work before? N/A 

Chrome version: 75.0.3633.0  Channel: n/a
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### ke...@chromium.org (2019-03-22)

Thanks for the report.

I haven't been able to successfully repro with Cluster-fuzz but still trying to confirm. The ASAN output you've attached might be enough to start an investigation. Were you able to test on Chrome 73 or 74?

[Monorail components: Blink>Workers]

### cd...@gmail.com (2019-03-25)

It did not repro on chromium 74.0.3718.0.



### ke...@chromium.org (2019-03-26)

Is someone from the workers team able to have a look at this and evaluate it or help triage?

### li...@chromium.org (2019-03-29)

According to our guidelines, security bugs should have owners. Tentatively assigning to nhiroki to take a look, but feel free to reassign if someone else can help. Thanks!

### nh...@chromium.org (2019-04-01)

I'll take a look.

### nh...@chromium.org (2019-04-03)

WIP CL: https://chromium-review.googlesource.com/c/chromium/src/+/1549804

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e077ad65604e9a56c4c741b8ef054c42973da6a8

commit e077ad65604e9a56c4c741b8ef054c42973da6a8
Author: Hiroki Nakagawa <nhiroki@chromium.org>
Date: Fri Apr 05 11:01:32 2019

Worker: Don't call WorkerThread::GetTaskRunner() after worker thread termination starts

After WorkerThread::Terminate() (WebSharedWorkerImpl::TerminateWorkerThread())
is called, WorkerThread::GetTaskRunner() must not be called from the main
thread because the underlying WorkerScheduler can be destroyed on the worker
thread.

Bug: 944424
Change-Id: I5074db897c0ec7448b13730e459769d988d6f173
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1549804
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Reviewed-by: Hayato Ito <hayato@chromium.org>
Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org>
Cr-Commit-Position: refs/heads/master@{#648135}
[modify] https://crrev.com/e077ad65604e9a56c4c741b8ef054c42973da6a8/third_party/blink/renderer/core/exported/web_shared_worker_impl.cc
[modify] https://crrev.com/e077ad65604e9a56c4c741b8ef054c42973da6a8/third_party/blink/renderer/core/workers/worker_thread.h


### nh...@chromium.org (2019-04-08)

The fix was landed in 75.0.3758.0.

cdsrc2016@: Would you check whether this is still reproducible after 75.0.3758.0?

### mb...@chromium.org (2019-04-08)

[Empty comment from Monorail migration]

### cd...@gmail.com (2019-04-09)

I tried it on 75.0.3760.0 asan with changing refresh time in poc.html from 0 to 30(increased by 1).The result is good, it does not repro in that version.

### nh...@chromium.org (2019-04-09)

Great! Thank you for reporting this and confirming the fix. I'll mark this as fixed :)

### sh...@chromium.org (2019-04-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats! The Panel decided to reward $3,000 for this report! 

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### cd...@gmail.com (2019-04-15)

Thanks for the reward!

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-07-16)

This issue was migrated from crbug.com/chromium/944424?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094344)*
