# Cross thread stack corruption caused by RTCVideoDecoderAdapter::InitializeSync 

| Field | Value |
|-------|-------|
| **Issue ID** | [461214000](https://issues.chromium.org/issues/461214000) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Media |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | al...@gmail.com |
| **Assignee** | tm...@chromium.org |
| **Created** | 2025-11-16 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS
Please provide a brief explanation of the security issue.

I'm looking at RTCVideoDecoderAdapter::InitializeSync in blink, it just seems like there's obvious stack corruption here if (and only if) you can stall the media task runner by at least 10 seconds.

The `waiter` and the `result` live on stack and are sent as cross thread unretained (raw) pointers to the media task runner.

This all looked safe up until <https://source.chromium.org/chromium/chromium/src/+/b039d4d54df561543de44411e98e3b798a38ef73> landed. That CL changed a previously unconditional wait to a timed wait.

I don't have the full context on that change (which seems to be a private bug) but it looks like it was switched to a timed wait to avoid a watchdog timer firing (likely because the callback was being dropped without firing somewhere?).

The timed wait however changes the safety of the CrossThreadUnretained pointers which now can point to stack memory after InitializeSync returns, if the timeout fires first and then the callback fires. The CL doesn't seem to discuss why it thinks these CrossThreadUnretained pointers are still safe.

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/peerconnection/rtc_video_decoder_adapter.cc;l=626-642>

(at main = 56ec591a1f9b1386cc10bf5fbff3ee5a79f25063)

```
bool RTCVideoDecoderAdapter::InitializeSync(
    const media::VideoDecoderConfig& config) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(decoding_sequence_checker_);
  TRACE_EVENT0("webrtc", "RTCVideoDecoderAdapter::InitializeSync");
  DVLOG(3) << __func__;
  // This function is called on a decoder thread.
  DCHECK(!media_task_runner_->RunsTasksInCurrentSequence());
  auto start_time = base::TimeTicks::Now();

  base::ScopedAllowBaseSyncPrimitivesOutsideBlockingScope allow_wait;
  bool result = false;
  base::WaitableEvent waiter(base::WaitableEvent::ResetPolicy::MANUAL,
                             base::WaitableEvent::InitialState::NOT_SIGNALED);
  auto init_cb =
      CrossThreadBindOnce(&FinishWait, CrossThreadUnretained(&waiter),
                          CrossThreadUnretained(&result));
  if (PostCrossThreadTask(
          *media_task_runner_.get(), FROM_HERE,
          CrossThreadBindOnce(&RTCVideoDecoderAdapter::Impl::Initialize,
                              weak_impl_, config, std::move(init_cb),
                              start_time,
                              CrossThreadUnretained(&decoder_type_)))) {
    // TODO(crbug.com/1076817) Remove if a root cause is found.
    if (!waiter.TimedWait(base::Seconds(10))) {
      RecordInitializationLatency(base::TimeTicks::Now() - start_time);
      return false;
    }

    RecordInitializationLatency(base::TimeTicks::Now() - start_time);
  }

  decoder_info_.implementation_name =
      "ExternalDecoder (" + media::GetDecoderName(decoder_type_) + ")";
  return result;
}

```

and (same file)

```
void FinishWait(base::WaitableEvent* waiter, bool* result_out, bool result) {
  DVLOG(3) << __func__ << "(" << result << ")";
  *result_out = result;
  waiter->Signal();
}

```

I don't think this is particularly exploitable because 10 seconds is a long time to stall the media thread and because an attacker needs to find something juicy where result is while also avoiding crashing when trying to signal the waiter, but this is very easy to fix and much more sound if the waiter and result were tossed in a scoped\_refptr or replaced by whatever the chromium version of promise + future are.

I don't have a full exploit and would not be at all peeved if this were demoted to a normal (non-security) bug, but I thought I'd give the security folks first crack at it because of stack corruption. My best proof of concept is simply putting an 11 second sleep at the start of RTCVideoDecoderAdapter::Impl::Initialize. Enough to see what happens when it get blocked up.

VERSION
Chrome Version: May 2020 through present including 142.0.7444.163 stable [x.x.x.x] + [stable, beta, or dev]
Operating System: Agnostic, but I'm on windows [Please indicate OS, version, and service pack level]

REPRODUCTION CASE
I don't have a full exploit and would not be at all peeved if this were demoted to a normal (non-security) bug, but I thought I'd give the security folks first crack at it because of stack corruption. My best proof of concept is simply putting an 11 second sleep at the start of RTCVideoDecoderAdapter::Impl::Initialize. Enough to see it write to the stack when it gets blocked up.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]
N/A

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Alex Converse, Discord Engineer

## Timeline

### an...@chromium.org (2025-11-17)

[security shepherd]: Thanks for the report! Assigning to @tm...@chromium.org who has worked on this change.

### da...@chromium.org (2025-11-17)

Agree it's wrong. I'd guess due to the `weak_impl_` binding the invalid access never occurs since we immediately destruct upon timeout:

- <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/peerconnection/rtc_video_decoder_adapter.cc;l=562;drc=807e0020b0482bcdf271c0de1fadcbd8cc63ed51>

Unsure how likely it is to beat the race here, but probably still worth fixing.

### ch...@google.com (2025-11-19)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-11-21)

Project: chromium/src  

Branch:  main  

Author:  Ted Meyer [tmathmeyer@chromium.org](mailto:tmathmeyer@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7180528>

Fix raw ptr to stack local binding

---


Expand for full commit details
```
     
    `result` and `waiter` are both stack local, captured by unretained raw 
    ptrs, passed across thread, and then deleted, potentially before that 
    thread can write back into them. 
     
    Now they are owned by RTCVideoDecodeAdapter, and only written into by an 
    init_cb which is bound to a weak_ptr to it, so they can never get UAF'd. 
     
    R=dalecurtis 
     
    Fixed: 461214000 
    Change-Id: I82702adc1af8d3d407053539971d93f78d7e7861 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7180528 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1548220}

```

---

Files:

- M `third_party/blink/renderer/platform/peerconnection/rtc_video_decoder_adapter.cc`
- M `third_party/blink/renderer/platform/peerconnection/rtc_video_decoder_adapter.h`

---

Hash: [93c16c1d586cf254df7bfe30e2af7724f88bb6c8](https://chromiumdash.appspot.com/commit/93c16c1d586cf254df7bfe30e2af7724f88bb6c8)  

Date: Fri Nov 21 02:28:52 2025


---

### sp...@google.com (2025-12-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Highly mitigated RCE with a bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-02-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Highly mitigated RCE with a bisect

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/461214000)*
