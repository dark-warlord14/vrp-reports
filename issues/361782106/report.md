# use-after-poison in mojo::SimpleWatcher::OnHandleReady

| Field | Value |
|-------|-------|
| **Issue ID** | [361782106](https://issues.chromium.org/issues/361782106) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | or...@chromium.org |
| **Created** | 2024-08-24 |
| **Bounty** | $8,000.00 |

## Description

tested OS:
Ubuntu and macOS
tested chrome version:
Chromium 129.0.6658.0 

repro steps:
./chrome  --user-data-dir=/tmp/xx2 http://localhost:8880/crash.html
The issue should reproduce in approximately 30 seconds.


After bisecting, it was confirmed that the issue started occurring after the following commit.
```
RTCDataChannel: Add support for the Blob type.

This enables support for both sending Blobs using RTCDataChannel.send()
and received Blobs in the 'MessageEvent' data member by setting the
'binaryType' field to "blob".

Bug: webrtc:2276, chromium:41370769
Change-Id: I0f820d1992c9270c5ea6dc7ef67554e350780cc2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3110559
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Auto-Submit: Florent Castelli <orphis@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1335968}
```

=================================================================
==1==ERROR: AddressSanitizer: use-after-poison on address 0x7e8c006b73e0 at pc 0x6091060f70b9 bp 0x7ffcc555b190 sp 0x7ffcc555b188
READ of size 4 at 0x7e8c006b73e0 thread T0 (chrome)
    #0 0x6091060f70b8 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple_watcher.cc:252:19
    #1 0x6091060f7f84 in Invoke<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), const base::WeakPtr<mojo::SimpleWatcher> &, int, unsigned int, mojo::HandleSignalsState> ./../../base/functional/bind_internal.h:738:12
    #2 0x6091060f7f84 in MakeItSo<void (mojo::SimpleWatcher::*)(int, unsigned int, const mojo::HandleSignalsState &), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState> > ./../../base/functional/bind_internal.h:954:5
    #3 0x6091060f7f84 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>) ./../../base/functional/bind_internal.h:1067:14
    #4 0x60910561ca24 in Run ./../../base/functional/callback.h:156:12
    #5 0x60910561ca24 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:203:34
    #6 0x609105684b36 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:486:11)> ./../../base/task/common/task_annotator.h:90:5
    #7 0x609105684b36 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
    #8 0x6091056838ca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #9 0x60910568589a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #10 0x609105509b7d in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:40:55
    #11 0x6091056864ea in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
    #12 0x6091055ab9af in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #13 0x60911ca36076 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:361:16
    #14 0x609102bbc19e in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:700:14
    #15 0x609102bbd09d in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:804:12
    #16 0x609102bbf80b in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1160:10
    #17 0x609102bba76a in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:331:36
    #18 0x609102bbad5b in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:344:10
    #19 0x6090f2033203 in ChromeMain ./../../chrome/app/chrome_main.cc:230:12
    #20 0x7e5c7a829d8f in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16

## Attachments

- crash.html (text/html, 883 B)
- asan.log (text/plain, 7.0 KB)

## Timeline

### ar...@chromium.org (2024-08-25)

Thanks! Nice report.

I can reproduce immediately. I get the same StackTrace.

This seems to be about WebRTC:

```
            let pc = new RTCPeerConnection();
            let channel = pc.createDataChannel('test');
            channel.close();
            channel.send(data);

```

This is high severity, as memory corruption in the renderer process.

- [phis@chromium.org](mailto:phis@chromium.org), could you please take a look?
- [guidou@chromium.org](mailto:guidou@chromium.org): FYI

### pe...@google.com (2024-08-25)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-08-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### go...@google.com (2024-08-26)

Reminder M129 is already in Beta and Stable promotion is coming soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### go...@google.com (2024-08-28)

Reminder M129 is already in Beta and Stable promotion is coming soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### go...@google.com (2024-09-03)

Reminder M129 is already in Beta and Stable promotion is coming VERY soon next week on Wednesday, Sept 11th. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### pe...@google.com (2024-09-04)

This issue appears to be blocking an upcoming release and is therefore an **Urgent Release Blocking Issue** as per <http://go/chrome-slo#release-blocking-issues>. Bumping the priority to P0 to better reflect the urgency.

If this is not a release blocking issue, please adjust the release block field. Adjusting the priority will have no affect, P0 will be re-applied whilever this is marked as a release blocking issue.

### or...@chromium.org (2024-09-06)

I have not been able to reproduce the issue locally with an ASan build on ToT, or even in the matching native test I added, but the fix is straightforward.

https://chromium-review.googlesource.com/c/chromium/src/+/5839728 is now under review and I will merge it asap to the M129 branch.

It was probably caused by a faulty rebase from the feature I added after some other recent changes in the file.


### ap...@google.com (2024-09-06)

Project: chromium/src
Branch: main

commit 373bdd2e98bc3c8ad0c0aa5299ad6b347689f6b3
Author: Florent Castelli <orphis@chromium.org>
Date:   Fri Sep 06 10:50:31 2024

    Check that the data channel is open before sending Blobs
    
    Bug: 361782106
    Change-Id: Id1a3a93cb4cfb287c38b199f82db21dc89e4c071
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5839728
    Reviewed-by: Guido Urdaneta <guidou@chromium.org>
    Commit-Queue: Florent Castelli <orphis@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1351950}

M       third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc
M       third_party/blink/renderer/modules/peerconnection/rtc_data_channel_test.cc

https://chromium-review.googlesource.com/5839728


### or...@chromium.org (2024-09-06)

This should be fixed in ToT as sending anything after a close operation is not valid.

@govind With the fix being straightforward, I'll preemptively request a merge before the next canary version to save time.

### pe...@google.com (2024-09-07)

Merge review required: M129 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

### or...@chromium.org (2024-09-09)

1. Yes, it is a security fix.
2. https://chromium-review.googlesource.com/5839728
3. Yes
4. No
5. N/A
6. N/A

### am...@chromium.org (2024-09-09)

M129 merge approved, please merge this fix to branch 6668 ASAP, NLT 10am Pacific tomorrow so this fix can be included in the M129 Stable RC being cut tomorrow. Thank you!

### or...@chromium.org (2024-09-09)

Merge done in https://chromium-review.googlesource.com/c/chromium/src/+/5844814

### ap...@google.com (2024-09-09)

Project: chromium/src
Branch: refs/branch-heads/6668

commit f12d06e864dda469fc7070fed41af5a975fe46a4
Author: Florent Castelli <orphis@chromium.org>
Date:   Mon Sep 09 18:58:10 2024

    [M129 Merge] Check that the data channel is open before sending Blobs
    
    (cherry picked from commit 373bdd2e98bc3c8ad0c0aa5299ad6b347689f6b3)
    
    Bug: 361782106
    Change-Id: Id1a3a93cb4cfb287c38b199f82db21dc89e4c071
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5839728
    Reviewed-by: Guido Urdaneta <guidou@chromium.org>
    Commit-Queue: Florent Castelli <orphis@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1351950}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5844814
    Cr-Commit-Position: refs/branch-heads/6668@{#1045}
    Cr-Branched-From: 05bc664984ca075216b7f2198c88b9725bfa1b9b-refs/heads/main@{#1343869}

M       third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc
M       third_party/blink/renderer/modules/peerconnection/rtc_data_channel_test.cc

https://chromium-review.googlesource.com/5844814


### pe...@google.com (2024-09-09)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### am...@chromium.org (2024-09-09)

Thank you for merging. Resetting as P1 since the backport to 129 has been completed.

### qk...@google.com (2024-09-10)

https://crrev.com/c/5839728 is not applicable to LTS M120 branch because M120 LTS branch doesn't implement `void RTCDataChannel::send(Blob* data, ExceptionState& exception_state)` method. So I'm not sure if M120 LTS version was affected by this bug. So I add "LTS-NonApplicable-120" label to this bug.

### gu...@chromium.org (2024-09-10)

This applies only to M129+. No need to merge to LTS M120 or M126.

### sp...@google.com (2024-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for baseline report of memory corruption in a sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-11)

Congratulations Cassidy Kim! Thank you for your efforts and reporting this issue to us -- nice work!

### qk...@google.com (2024-09-19)

Labeling as LTS-NotApplicable-126 because of the comment #20.

### pe...@google.com (2024-12-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/361782106)*
