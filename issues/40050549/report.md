# Security: heap-use-after-free in content::SpeechRecognizerImpl::Abort

| Field | Value |
|-------|-------|
| **Issue ID** | [40050549](https://issues.chromium.org/issues/40050549) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Speech |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ha...@chromium.org |
| **Created** | 2019-10-28 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

heap-use-after-free in content::SpeechRecognizerImpl::Abort

**VERSION**  

Chrome Version: asan-linux-release-709771

**REPRODUCTION CASE**  

./chrome --headless --screenshot repro.html

ADDITIONAL INFORMATION

# [1027/200927.988278:WARNING:ipc\_message\_attachment\_set.cc(49)] MessageAttachmentSet destroyed with unconsumed attachments: 0/1 [1027/200929.719037:INFO:headless\_shell.cc(620)] Written to file screenshot.png.

==16970==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b00001bdc8 at pc 0x5555627740c2 bp 0x7fffdf9002c0 sp 0x7fffdf9002b8  

READ of size 8 at 0x60b00001bdc8 thread T5 (Chrome\_IOThread)  

#0 0x5555627740c1 in content::SpeechRecognizerImpl::Abort(blink::mojom::SpeechRecognitionError const&) content/browser/speech/speech\_recognizer\_impl.cc:750:15  

#1 0x555562770f83 in AbortSilently content/browser/speech/speech\_recognizer\_impl.cc:702:10  

#2 0x555562770f83 in content::SpeechRecognizerImpl::ExecuteTransitionAndGetNextState(content::SpeechRecognizerImpl::FSMEventArgs const&) content/browser/speech/speech\_recognizer\_impl.cc:369:18  

#3 0x55556276d820 in content::SpeechRecognizerImpl::DispatchEvent(content::SpeechRecognizerImpl::FSMEventArgs const&) content/browser/speech/speech\_recognizer\_impl.cc:355:12  

#4 0x555568057852 in Run base/callback.h:98:12  

#5 0x555568057852 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:142:33  

#6 0x55556808f8f8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:365:23  

#7 0x55556808f277 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219:7  

#8 0x5555681c7e01 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:208:55  

#9 0x55556809168e in Run base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:12  

#10 0x55556809168e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#11 0x555568008651 in base::RunLoop::Run() base/run\_loop.cc:156:14  

#12 0x55556146cbc4 in content::BrowserProcessSubThread::IOThreadRun(base::RunLoop\*) content/browser/browser\_process\_sub\_thread.cc:158:11  

#13 0x5555680e126b in base::Thread::ThreadMain() base/threading/thread.cc:376:3  

#14 0x5555681ba7b1 in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:81:13  

#15 0x7ffff79b96da in start\_thread (/lib/x86\_64-linux-gnu/libpthread.so.0+0x76da)

0x60b00001bdc8 is located 8 bytes inside of 112-byte region [0x60b00001bdc0,0x60b00001be30)  

freed by thread T5 (Chrome\_IOThread) here:  

#0 0x55555e5cf36d in operator delete(void\*) /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:160:3  

#1 0x555568057852 in Run base/callback.h:98:12  

#2 0x555568057852 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:142:33  

#3 0x55556808f8f8 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:365:23  

#4 0x55556808f277 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219:7  

#5 0x5555681c7e01 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:208:55  

#6 0x55556809168e in Run base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:12  

#7 0x55556809168e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#8 0x555568008651 in base::RunLoop::Run() base/run\_loop.cc:156:14  

#9 0x55556146cbc4 in content::BrowserProcessSubThread::IOThreadRun(base::RunLoop\*) content/browser/browser\_process\_sub\_thread.cc:158:11  

#10 0x5555680e126b in base::Thread::ThreadMain() base/threading/thread.cc:376:3  

#11 0x5555681ba7b1 in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:81:13  

#12 0x7ffff79b96da in start\_thread (/lib/x86\_64-linux-gnu/libpthread.so.0+0x76da)

previously allocated by thread T0 (chrome) here:  

#0 0x55555e5ceb0d in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:99:3  

#1 0x55556144dadd in content::BrowserMainLoop::BrowserThreadsStarted() content/browser/browser\_main\_loop.cc:1384:39  

#2 0x555562421694 in Run base/callback.h:98:12  

#3 0x555562421694 in content::StartupTaskRunner::RunAllTasksNow() content/browser/startup\_task\_runner.cc:41:29  

#4 0x55556144bc41 in content::BrowserMainLoop::CreateStartupTasks() content/browser/browser\_main\_loop.cc:917:25  

#5 0x5555614548ad in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) content/browser/browser\_main\_runner\_impl.cc:128:15  

#6 0x55557907fb11 in headless::HeadlessContentMainDelegate::RunProcess(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, content::MainFunctionParams const&) headless/lib/headless\_content\_main\_delegate.cc:318:35  

#7 0x5555670821fd in RunBrowserProcessMain content/app/content\_main\_runner\_impl.cc:524:29  

#8 0x5555670821fd in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) content/app/content\_main\_runner\_impl.cc:960:10  

#9 0x555567081703 in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:868:12  

#10 0x55556722201f in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:423:29  

#11 0x55556707ca3f in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#12 0x55556721d7ef in headless::(anonymous namespace)::RunContentMain(headless::HeadlessBrowser::Options, base::OnceCallback<void (headless::HeadlessBrowser\*)>) headless/app/headless\_shell.cc:172:10  

#13 0x55556721c7e6 in HeadlessBrowserMain headless/app/headless\_shell.cc:861:10  

#14 0x55556721c7e6 in headless::HeadlessShellMain(int, char const\*\*) headless/app/headless\_shell.cc:806:10  

#15 0x55555e5d1618 in ChromeMain chrome/app/chrome\_main.cc:106:12  

#16 0x7ffff06efb96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

Thread T5 (Chrome\_IOThread) created by T0 (chrome) here:  

#0 0x55555e58fcca in pthread\_create /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_interceptors.cpp:214:3  

#1 0x5555681b99fe in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, base::PlatformThreadHandle\*, base::ThreadPriority) base/threading/platform\_thread\_posix.cc:120:13  

#2 0x5555680e04e4 in base::Thread::StartWithOptions(base::Thread::Options const&) base/threading/thread.cc:182:15  

#3 0x5555621a1842 in content::BrowserTaskExecutor::CreateIOThread() content/browser/scheduler/browser\_task\_executor.cc:341:19  

#4 0x555567081d7c in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) content/app/content\_main\_runner\_impl.cc:937:9  

#5 0x555567081703 in content::ContentMainRunnerImpl::Run(bool) content/app/content\_main\_runner\_impl.cc:868:12  

#6 0x55556722201f in service\_manager::Main(service\_manager::MainParams const&) services/service\_manager/embedder/main.cc:423:29  

#7 0x55556707ca3f in content::ContentMain(content::ContentMainParams const&) content/app/content\_main.cc:19:10  

#8 0x55556721d7ef in headless::(anonymous namespace)::RunContentMain(headless::HeadlessBrowser::Options, base::OnceCallback<void (headless::HeadlessBrowser\*)>) headless/app/headless\_shell.cc:172:10  

#9 0x55556721c7e6 in HeadlessBrowserMain headless/app/headless\_shell.cc:861:10  

#10 0x55556721c7e6 in headless::HeadlessShellMain(int, char const\*\*) headless/app/headless\_shell.cc:806:10  

#11 0x55555e5d1618 in ChromeMain chrome/app/chrome\_main.cc:106:12  

#12 0x7ffff06efb96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

SUMMARY: AddressSanitizer: heap-use-after-free content/browser/speech/speech\_recognizer\_impl.cc:750:15 in content::SpeechRecognizerImpl::Abort(blink::mojom::SpeechRecognitionError const&)  

Shadow bytes around the buggy address:  

0x0c167fffb760: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa  

0x0c167fffb770: fa fa fa fa fa fa 00 00 00 00 00 00 00 00 00 00  

0x0c167fffb780: 00 00 00 fa fa fa fa fa fa fa fa fa 00 00 00 00  

0x0c167fffb790: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa  

0x0c167fffb7a0: fa fa 00 00 00 00 00 00 00 00 00 00 00 00 00 fa  

=>0x0c167fffb7b0: fa fa fa fa fa fa fa fa fd[fd]fd fd fd fd fd fd  

0x0c167fffb7c0: fd fd fd fd fd fd fa fa fa fa fa fa fa fa 00 00  

0x0c167fffb7d0: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  

0x0c167fffb7e0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c167fffb7f0: fd fa fa fa fa fa fa fa fa fa fd fd fd fd fd fd  

0x0c167fffb800: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

Shadow gap: cc  

==16970==ABORTING

**CREDIT INFORMATION**  

Antti Levomäki and Christian Jalio from Forcepoint

## Attachments

- [repro.html](attachments/repro.html) (text/plain, 117.7 KB)

## Timeline

### cl...@chromium.org (2019-10-28)

[Comment Deleted]

### cl...@chromium.org (2019-10-28)

[Comment Deleted]

### cl...@chromium.org (2019-10-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6008750152220672.

### cl...@chromium.org (2019-10-28)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Speech]

### cl...@chromium.org (2019-10-28)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/9109135db0b25604af35c2031f41a61816584b0a ([EG2] Converts SaveProfileEGTest).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2019-10-28)

Detailed Report: https://clusterfuzz.com/testcase?key=6008750152220672

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60f0000171e8
Crash State:
  content::SpeechRecognizerImpl::Abort
  content::SpeechRecognizerImpl::ExecuteTransitionAndGetNextState
  content::SpeechRecognizerImpl::DispatchEvent
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=709912:709913

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6008750152220672

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6008750152220672 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ol...@chromium.org (2019-10-28)

My CL is iOS only.

### jd...@chromium.org (2019-10-28)

tommi@: can you take a look at this as the speech synth owner and help us triage it? It appears to trigger a crash of some kind in Chrome since roughly the beginning of time, so I can't easily bisect it further.

I'm dropping this to High given the required command line flags. Frankly, even that might be a stretch, but until we understand what's happening, better safe than sorry.

### jd...@chromium.org (2019-10-28)

[Empty comment from Monorail migration]

### to...@chromium.org (2019-10-28)

myid.shin - could this be related to the recent Mojo changes?
(e.g. here: https://chromium-review.googlesource.com/c/chromium/src/+/1872090)

### my...@igalia.com (2019-10-29)

Hi, tommi@,

I don't think Mojo changes are related to this issue since the CL only converted the old Mojo to the new one and it doesn't change any work flow.
And I've also reproduced this issue with reverting the CL. 

BTW,  I I took a look at this issue(I didn't do a bisect for this).

UAF issue is caused by accessing listener, SpeechRecognitionEventListener(=SpeechRecognitionManagerImpl) after destroying SpeechRecognitionManagerImpl.

SpeechRecognizerImpl::AbortRecognition --> Post to IO thread
BrowserMainLoop shutdown and SpeechRecognitionManagerImpl is nullptr
SpeechRecognizerImpl::Abort -> Access SpeechRecognitionManagerImpl and crash.


So, I could see to stop the reproduction if we use a weak pointer instead of |this| in SpeechRecognizerImpl::AbortRecognition.

void SpeechRecognizerImpl::AbortRecognition() {
  base::PostTask(FROM_HERE, {BrowserThread::IO},
                 base::BindOnce(&SpeechRecognizerImpl::DispatchEvent, weak_ptr_factory_.GetWeakPtr() /*instead of this*/,
                                FSMEventArgs(EVENT_ABORT)));
}

I think we might need a bisect given that this code was added a long time ago and that this issue has recently occurred.
WDYT?

### to...@chromium.org (2019-10-29)

Hans - this vaguely rings a bell - is this a duplicate of a previous issue in SpeechRecognizerImpl?

### sh...@chromium.org (2019-10-29)

[Empty comment from Monorail migration]

### ha...@chromium.org (2019-11-05)

+primiano

> Hans - this vaguely rings a bell - is this a duplicate of a previous issue in SpeechRecognizerImpl?

It doesn't ring a bell for me (but my memory of all this is fading), and I don't find anything in the bug tracker.

myid.shin, your solution sounds plausible. Want to send out a CL and cc myself and primiano?

### sh...@chromium.org (2019-11-19)

hans: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-04)

hans: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-27)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2020-01-07)

I'm not sure how I ended up owning this, but here's a patch anyway :-)
Patch: https://chromium-review.googlesource.com/c/chromium/src/+/1989069

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/57f988dd7c1f63f59b44282efcc9e6f1e85ac19c

commit 57f988dd7c1f63f59b44282efcc9e6f1e85ac19c
Author: Hans Wennborg <hans@chromium.org>
Date: Thu Jan 09 10:52:37 2020

Use a WeakPtr in SpeechRecognizerImpl::AbortRecognition

It seems that during shutdown, the object can go away before the posted
task runs.

Thanks to Miyoung Shin for looking into this.

Bug: 1018677
Change-Id: I1b3c7947eb3110ae6538249106a87f5c56f6238c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1989069
Reviewed-by: Primiano Tucci <primiano@chromium.org>
Reviewed-by: Tommi <tommi@chromium.org>
Reviewed-by: Olga Sharonova <olka@chromium.org>
Commit-Queue: Olga Sharonova <olka@chromium.org>
Cr-Commit-Position: refs/heads/master@{#729694}

[modify] https://crrev.com/57f988dd7c1f63f59b44282efcc9e6f1e85ac19c/content/browser/speech/speech_recognizer_impl.cc


### ha...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-09)

Requesting merge to stable M79 because latest trunk commit (729694) appears to be after stable branch point (706915).

Requesting merge to beta M80 because latest trunk commit (729694) appears to be after beta branch point (722274).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-01-09)

ClusterFuzz testcase 6008750152220672 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=727557:727558

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2020-01-10)

This bug requires manual review: M80's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2020-01-10)

I'm not sure this is severe enough to consider merging, but I'll leave that decision to others.

### sr...@google.com (2020-01-10)

adetaylor@ can u review if this needs to be merged to M80

### ad...@google.com (2020-01-10)

[Comment Deleted]

### sr...@google.com (2020-01-10)

Merge approved for M80, branch:3987

### sh...@chromium.org (2020-01-11)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2020-01-13)

How is the change looking in canary so far?

### ha...@chromium.org (2020-01-13)

> How is the change looking in canary so far?

I haven't heard anything, so I assume it's good.

### sr...@google.com (2020-01-13)

Please help get your merges complete before 3pm PST today Monday Jan 13 so this can be included in the beta release tomorrow

### go...@google.com (2020-01-13)

M80 merge going thru CQ - https://chromium-review.googlesource.com/c/chromium/src/+/1998316. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0875eb6ea4bf56bd54f01097116451fa0f66d138

commit 0875eb6ea4bf56bd54f01097116451fa0f66d138
Author: Hans Wennborg <hans@chromium.org>
Date: Mon Jan 13 21:27:26 2020

Use a WeakPtr in SpeechRecognizerImpl::AbortRecognition

It seems that during shutdown, the object can go away before the posted
task runs.

Thanks to Miyoung Shin for looking into this.

(cherry picked from commit 57f988dd7c1f63f59b44282efcc9e6f1e85ac19c)

Bug: 1018677
Change-Id: I1b3c7947eb3110ae6538249106a87f5c56f6238c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1989069
Reviewed-by: Primiano Tucci <primiano@chromium.org>
Reviewed-by: Tommi <tommi@chromium.org>
Reviewed-by: Olga Sharonova <olka@chromium.org>
Commit-Queue: Olga Sharonova <olka@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#729694}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1998316
Reviewed-by: Krishna Govind <govind@chromium.org>
Reviewed-by: Hans Wennborg <hans@chromium.org>
Commit-Queue: Hans Wennborg <hans@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#497}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/0875eb6ea4bf56bd54f01097116451fa0f66d138/content/browser/speech/speech_recognizer_impl.cc


### go...@google.com (2020-01-13)

Test failure reported - https://chromium-review.googlesource.com/c/chromium/src/+/1998316.

Try jobs failed on following builders:
  luci.chromium.try-beta/linux-chromeos-rel JOB_FAILED https://ci.chromium.org/b/8891351525448987248
    1 Test Suite(s) failed.
    
    **non_viz_content_browsertests** failed because of:
    
    - WithoutCORBProtectionSniffing/CrossSiteDocumentBlockingTest.AppCache_NetworkFallback/0

Is it ok to have merge listed at #35 with above test failure in M80?

### na...@google.com (2020-01-14)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-01-14)

hans@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### go...@chromium.org (2020-01-14)

Please update bug with M80 Beta result tomorrow morning so we can approve merge to M79 for respin this week. 

### go...@chromium.org (2020-01-14)

+cindyb@ (Chrome OS M79 Release TPM)

### ad...@google.com (2020-01-14)

govind@ regarding https://crbug.com/chromium/1018677#c36, as far as I can see, the test failure is completely unrelated to the fix here, so it should be safe. I assume it's just a flakey test. It would be good to hear from hans@ as well though for a second opinion.

### go...@chromium.org (2020-01-15)

Thank you adetaylor@.

hans@, ptal https://crbug.com/chromium/1018677#c41 and reply please.  Also how is the change looking in Desktop Beta version 80.0.3987.53 which went out this morning? 



Note: We would like to cut M79 stable RC tomorrow, Wednesday morning .



### ha...@chromium.org (2020-01-15)

> ptal https://crbug.com/chromium/1018677#c41 and reply please

The test failure was on a tryjob on linux-chromeos-rel. The test is unrelated, and the second run on that trybot came back green, so that was just an unrelated test being flaky.

> Also how is the change looking in Desktop Beta version 80.0.3987.53 which went out this morning?

I haven't heard about any problems, so I assume it's fine.

### go...@chromium.org (2020-01-15)

Thank you hans@.

Approving merge to M79 branch 3945 based on comments #41 and #43. Please merge by EOD today (Munich time)  if change continue to look good in canary.

### ha...@chromium.org (2020-01-15)

> Please merge by EOD today (Munich time)  if change continue to look good in canary.

I don't know how to merge. Am I supposed to do this myself and are there instructions somewhere? The M80 merge was done by you I think?

### go...@chromium.org (2020-01-15)

Ah,ok. 
Here is M79 merge - https://chromium-review.googlesource.com/c/chromium/src/+/2001728.  Please review and trigger CQ when ready. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ba6d9c9556a4bb53a825edd481a41cc8aa63a3d3

commit ba6d9c9556a4bb53a825edd481a41cc8aa63a3d3
Author: Hans Wennborg <hans@chromium.org>
Date: Wed Jan 15 08:22:02 2020

Use a WeakPtr in SpeechRecognizerImpl::AbortRecognition

It seems that during shutdown, the object can go away before the posted
task runs.

Thanks to Miyoung Shin for looking into this.

TBR=olka
(cherry picked from commit 57f988dd7c1f63f59b44282efcc9e6f1e85ac19c)

Bug: 1018677
Change-Id: I1b3c7947eb3110ae6538249106a87f5c56f6238c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1989069
Reviewed-by: Primiano Tucci <primiano@chromium.org>
Reviewed-by: Tommi <tommi@chromium.org>
Reviewed-by: Olga Sharonova <olka@chromium.org>
Commit-Queue: Olga Sharonova <olka@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#729694}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2001728
Reviewed-by: Hans Wennborg <hans@chromium.org>
Commit-Queue: Hans Wennborg <hans@chromium.org>
Cr-Commit-Position: refs/branch-heads/3945@{#1043}
Cr-Branched-From: e4635fff7defbae0f9c29e798349f6fc0cce4b1b-refs/heads/master@{#706915}

[modify] https://crrev.com/ba6d9c9556a4bb53a825edd481a41cc8aa63a3d3/content/browser/speech/speech_recognizer_impl.cc


### ad...@google.com (2020-01-15)

[Empty comment from Monorail migration]

### ad...@google.com (2020-01-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-01-15)

[Empty comment from Monorail migration]

### ad...@google.com (2020-01-16)

Deleted https://crbug.com/chromium/1018677#c28 since I said something daft. The rest of the comment said:

> Yes, this definitely needs to go back to M80 and into the next M79 release.
> This is a use-after-free within the browser process which is triggered by untrustworthy internet content (https://clusterfuzz.com/viewer?testcase_id=6008750152220672&key=7ef832a7-91f0-4cde-bfb0-9fb3602e3c22) so this definitely qualifies as 'critical' severity. Such bugs are rare.

and I bumped the severity up to Critical.

### na...@google.com (2020-01-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-23)

Congrats the Panel decided to reward $5,000 for this report!

### na...@google.com (2020-01-23)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-23)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-12-17)

The VRP panel has reconsidered this bug and decided to award $15,000 in total (so $10,000 more).

### ad...@google.com (2021-02-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-11)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1018677?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050549)*
