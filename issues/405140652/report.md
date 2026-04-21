# UAF when accessing member variable after destruction of throttle (SubframeHistoryNavigationThrottle)

| Field | Value |
|-------|-------|
| **Issue ID** | [405140652](https://issues.chromium.org/issues/405140652) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 134.0.0.0 |
| **Reporter** | xp...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2025-03-21 |
| **Bounty** | $4,000.00 |

## Description

# Steps to reproduce the problem

I will provide a reproduction of the UAF soon. Bear with me, please. Though I think the UAF is trivial.

# Problem Description

A `SubframeHistoryNavigationThrottle` is intended to defer subframe history navigations while the main frame commits main-frame same-document history navigations. When the `Resume()` method is called, it triggers a call to resume the current throttle [0](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/subframe_history_navigation_throttle.cc;drc=1563c4e1a33c72f24006ce2ee28eea7629632370;l=48). However, the call to `NavigationThrottle::Resume()` can synchronously delete `this`. This leads to a use-after-free when subsequently accessing the member variable `state_` [1](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/subframe_history_navigation_throttle.cc;drc=1563c4e1a33c72f24006ce2ee28eea7629632370;l=50).

```
void SubframeHistoryNavigationThrottle::Resume() {
  if (state_ == State::kDeferred) {
    NavigationThrottle::Resume(); [0]
  }
  state_ = State::kRunningAfterResumeSignal; [1]
}

```

This issue resembles [crbug.com/40063127](https://crbug.com/40063127).

**Suggested Fix**: Move the member variable assignment (`state_ = State::kRunningAfterResumeSignal;`) to before calling `Resume()`:

```
void SubframeHistoryNavigationThrottle::Resume() {
  state_ = State::kRunningAfterResumeSignal;
  
  if (state_ == State::kDeferred) {
    NavigationThrottle::Resume();
    // `Resume()` can synchronously delete this navigation throttle, so no code
    // after this call should reference the throttle instance.
  }
}

```
# Additional Comments

PoC soon.

# Summary

UAF when accessing member variable after destruction of throttle (SubframeHistoryNavigationThrottle)

# Custom Questions

#### Type of crash:

browser

#### Reporter credit:

Sven Dysthe @svn\_dy

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Timeline

### xp...@gmail.com (2025-03-21)

This bug was introduced with (bisect): <https://source.chromium.org/chromium/chromium/src/+/1563c4e1a33c72f24006ce2ee28eea7629632370>

### xp...@gmail.com (2025-03-21)

Oops, my original suggested fix would not work because we would never enter the condition below (it's late here 2am 😅).

Use weak pointer instead:

```
void SubframeHistoryNavigationThrottle::Resume() {
  if (state_ == State::kDeferred) {
    auto weak_this = weak_factory_.GetWeakPtr();
    NavigationThrottle::Resume();
    // The call to `Resume()` above might result in the deletion of `this`. Return immediately
    // if so.
    if (!weak_this)
      return;
  }
  state_ = State::kRunningAfterResumeSignal;
}

```

### sr...@google.com (2025-03-21)

Thanks Sven, I'm setting the needs-feedback label for now for the poc.

But already cc'ing the folks from the CL you found with your bisect as a heads up!

### to...@chromium.org (2025-03-24)

Thank you for the report
I will send a fix for a review now.

### sr...@google.com (2025-03-24)

toyoshim@, is it correct that this bug was introduced in https://chromium-review.googlesource.com/c/chromium/src/+/6334098? (I'm setting the foundin to 136 based on that)
Also, did you see the update in #3 suggesting to use a weak pointer instead?

@reporter: could you still provide a proof-of-concept so that we can verify that the issue has been fixed?

### xp...@gmail.com (2025-03-24)

Re #5: Thank you for taking up the issue! Would the condition `if (state_ == State::kDeferred)` ever evaluate to true after `state_` is set to `State::kRunningAfterResumeSignal`?

```
void SubframeHistoryNavigationThrottle::Resume() {
  state_ = State::kRunningAfterResumeSignal;
  if (state_ == State::kDeferred) { // Always false. `state_` is set to State::kRunningAfterResumeSignal before the condition
    NavigationThrottle::Resume();
    // Should do nothing here. See Resume()'s comment for details..
  }
}

```

Also see [comment #3](https://issues.chromium.org/issues/405140652#comment3). Maybe use a weak pointer.

### pe...@google.com (2025-03-24)

Thank you for providing more feedback. Adding the requester to the CC list.

### xp...@gmail.com (2025-03-24)

Re #6: I can. I'm currently working on a proof of concept. I am still learning the Chromium code base and architecture.

As a side note, the root cause of this issue mirrors [crbug.com/40063127](https://issues.chromium.org/issues/40063127) and [crbug.com/40063128](https://issues.chromium.org/issues/40063128).

### to...@chromium.org (2025-03-24)

Re: sroettger@ #6
Yes, this was introduced by the CL, but unfortunately that was a fix for a stable blocker crash, and already merged to the beta and stable.
So, the same issue should exist in the current 134 (might be only on Chrome OS now, because this was merged after the other platform stable releases)

Merge commit for m134
https://chromiumdash.appspot.com/commit/b8d8eead2ed4bc6f86401bb79d05b9ba9264b9d5

Merge commit for m135
https://chromiumdash.appspot.com/commit/849f51bc14da6a6b1e583287400e424d510b4fea

I think this UAF depends on very rare timing, and also needs to happen together with another rare event that another throttle cancels the request, e.g. the save browsing rejects the navigation, etc. So, the frequency would be less than the fixed crash. Anyway, I will move the fix forward, and will request a merge.

Re: Sven #9
No worries about the POC. I understand that this will actually happen in the production, but it may be very difficult to hit the case in a reliable way.

### dx...@google.com (2025-03-25)

Project: chromium/src  

Branch: main  

Author: Takashi Toyoshima [toyoshim@chromium.org](mailto:toyoshim@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6387055>

SubframeHistoryNavigationThrottle: Update the state\_ first

---


Expand for full commit details
```
     
    It's nice to update the `state_` before calling Resume() 
    to avoid an ordering issue. 
     
    Bug: 405140652 
    Change-Id: Ife607f8121eadcf30f86c5478a688bd7e61bccb1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6387055 
    Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1437323}

```

---

Files:

- M `content/browser/renderer_host/subframe_history_navigation_throttle.cc`

---

Hash: 94ec04ec6bd89868fe9508a76d058243db8f0623  

Date:  Tue Mar 25 06:28:14 2025


---

### ch...@google.com (2025-03-25)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: alonbajayo (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-03-25)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-03-25)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### to...@google.com (2025-03-26)

1. UAF security fix
2. <https://chromium-review.googlesource.com/6387055>
3. 136.0.7090.0, but would not be hard to verify the fix as the problem rarely happens, but theoretically clear.
4. no
5. n/a
6. no

### am...@chromium.org (2025-03-26)

<https://crrev.com/c/6387055> approved for merges
While this appears to be mitigated, with the preconditions of specific, rare timing alignments, and also needing to happen together with another event of another throttle canceling the request, we should also merge this fix to M134 since it will be Extended Stable support when M135 is promoted to Stable channel next week.

Please merge this fix to M135 Beta / branch 7049 by EOD Friday in the case that M135 Stable RC is recut for release next week (RC for M135 Early Stable was already cut yesterday).

Once M135 Stable ships, I'll need to revisit for M134 merge review to ensure this fix doesn't ship to Extended Stable before Stable channel.

### xp...@gmail.com (2025-03-26)

Good afternoon,

Would it be possible to grant me access to view the issues resolved by commit <https://source.chromium.org/chromium/chromium/src/+/1563c4e1a33c72f24006ce2ee28eea7629632370>, or alternatively, could a crash stack trace from those issues be shared here?

Thanks!

### am...@chromium.org (2025-03-26)

Hello, these are all reports from internal crash reporting so we are unable to provide access to those issues nor can we add data from that crash reporting here. 


### dx...@google.com (2025-03-27)

Project: chromium/src  

Branch: refs/branch-heads/7049  

Author: Takashi Toyoshima [toyoshim@chromium.org](mailto:toyoshim@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6400273>

[M135] SubframeHistoryNavigationThrottle: Update the state\_ first

---


Expand for full commit details
```
     
    It's nice to update the `state_` before calling Resume() 
    to avoid an ordering issue. 
     
    (cherry picked from commit 94ec04ec6bd89868fe9508a76d058243db8f0623) 
     
    Bug: 405140652 
    Change-Id: Ife607f8121eadcf30f86c5478a688bd7e61bccb1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6387055 
    Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1437323} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6400273 
    Auto-Submit: Takashi Toyoshima <toyoshim@chromium.org> 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Commit-Queue: Rakina Zata Amni <rakina@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7049@{#1424} 
    Cr-Branched-From: 2dab7846d0951a552bdc4f350dad497f986e6fed-refs/heads/main@{#1427262}

```

---

Files:

- M `content/browser/renderer_host/subframe_history_navigation_throttle.cc`

---

Hash: 72c296c7339d6aef250980661f6a2563f46e5da0  

Date:  Thu Mar 27 09:38:51 2025


---

### to...@google.com (2025-03-31)

still no response from 134 release managers.
should I ping directly?

### to...@google.com (2025-03-31)

Ah, I overlooked Amy's last comment, "Once M135 Stable ships, I'll need to revisit for M134...".
So, I will wait for Amy's next action.
Please let me know if I need to take action for this.
Thanks!

### pg...@google.com (2025-03-31)

setting oses to impact all desktop as it does not appear to be specific to windows - please correct me if this is a windows specific issue!

### pe...@google.com (2025-03-31)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2025-04-01)

Labelling as not applicable for LTS 132 and 126 because the suspected CL[1] isn't present in M132 and M126 according to the comment #6 and #10.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/6334098

### am...@chromium.org (2025-04-02)

<https://crrev.com/c/6387055> approved for merge to M134 Extended Stable, please merge this fix to branch 6998 by EOD Friday so this fix can ship in the next update of M134 Extended -- thank you

### sp...@google.com (2025-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
$3,000 for report of moderately mitigated (mitigated by precise timing, race condition with lower potential for exploitability) memory corruption in a non-sandboxed process + $1,000 bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-03)

Congratulations Sven! Thank you for your efforts and reporting this issue to us!

### sr...@google.com (2025-04-07)

I have CP'ed the M134 CL here - https://chromium-review.googlesource.com/c/chromium/src/+/6437145 and will land it as I need to cut the RC build for extended stable today

### dx...@google.com (2025-04-07)

Project: chromium/src  

Branch: refs/branch-heads/6998  

Author: Takashi Toyoshima [toyoshim@chromium.org](mailto:toyoshim@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6437145>

SubframeHistoryNavigationThrottle: Update the state\_ first

---


Expand for full commit details
```
     
    It's nice to update the `state_` before calling Resume() 
    to avoid an ordering issue. 
     
    (cherry picked from commit 94ec04ec6bd89868fe9508a76d058243db8f0623) 
     
    Bug: 405140652 
    Change-Id: Ife607f8121eadcf30f86c5478a688bd7e61bccb1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6387055 
    Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1437323} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6437145 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/6998@{#2999} 
    Cr-Branched-From: de9c6fafd8ae5c6ea0438764076ca7d04a0b165d-refs/heads/main@{#1415337}

```

---

Files:

- M `content/browser/renderer_host/subframe_history_navigation_throttle.cc`

---

Hash: 2848a3bac665b2558ad3934fe7ee61be9ff239a8  

Date:  Mon Apr 7 17:49:56 2025


---

### to...@chromium.org (2025-04-08)

thanks, srinivassista

I mistakenly overlooked the notification for the m134 approval.

### ch...@google.com (2025-07-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $3,000 for report of moderately mitigated (mitigated by precise timing, race condition with lower potential for exploitability) memory corruption in a non-sandboxed process + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/405140652)*
