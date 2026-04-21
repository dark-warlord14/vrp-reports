#  Use After Free in PresentationConnectionCallbacks::OnSuccess

| Field | Value |
|-------|-------|
| **Issue ID** | [339588211](https://issues.chromium.org/issues/339588211) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>PresentationAPI |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2024-05-09 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

after issue 40053095 fixed, and then re -adds vulnerabilities.In function PresentationConnectionCallbacks::OnSuccess, Invoking Promise.resolve may trigger user callback. "request_" [0] can be freed in the callback and cause use-after-free.

PoC see https://issues.chromium.org/issues/40053095

[0] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/presentation/presentation_connection_callbacks.cc;l=83;bpv=0;bpt=1
void PresentationConnectionCallbacks::OnSuccess(
    const mojom::blink::PresentationInfo& presentation_info,
    mojo::PendingRemote<mojom::blink::PresentationConnection> connection_remote,
    mojo::PendingReceiver<mojom::blink::PresentationConnection>
        connection_receiver) {
  // Reconnect to existing connection.
  if (connection_ && connection_->GetState() ==
                         mojom::blink::PresentationConnectionState::CLOSED) {
    connection_->DidChangeState(
        mojom::blink::PresentationConnectionState::CONNECTING);
  }

  // Create a new connection.
  if (!connection_ && request_) {
    connection_ = ControllerPresentationConnection::Take(
        resolver_.Get(), presentation_info, request_);
  }

  connection_->Init(std::move(connection_remote),
                    std::move(connection_receiver));

  resolver_->Resolve(connection_);
#if BUILDFLAG(IS_ANDROID)
  PresentationMetrics::RecordPresentationConnectionResult(request_, true); //[0]
#endif
}


introduce commit 
https://chromium-review.googlesource.com/c/chromium/src/+/3540656


Fix 

@@ -77,11 +77,10 @@ void PresentationConnectionCallbacks::OnSuccess(
 
   connection_->Init(std::move(connection_remote),
                     std::move(connection_receiver));
-
-  resolver_->Resolve(connection_);
 #if BUILDFLAG(IS_ANDROID)
   PresentationMetrics::RecordPresentationConnectionResult(request_, true);
 #endif
+  resolver_->Resolve(connection_);
 }
 
 void PresentationConnectionCallbacks::OnError(


## Timeline

### ca...@chromium.org (2024-05-09)

Thanks for the report. It seems unlikely that the linked commit would cause this to regress since the original issue was only reproducible with multiple screens, while the commit adds metrics that are Android only (where there is no multiple screen support). Were you able to trigger this using the PoC in the original bug? If so, can you add the asan output or a video of the crash happening? Thanks

### ad...@google.com (2024-05-10)

New security shepherd here.

I'm reasonably convinced by this bug:

- I think there must be a way to trigger this code on Android, or there wouldn't be `#if BUILDFLAG(IS_ANDROID)` all over it. I suspect that casting can count as multiple displays sufficiently to trigger this bug.
- The original PoC didn't seem to have anything specific to multiple displays - it was just triggering this code.
- The only thing I'm not sure about is whether `request_` can definitely be freed in the same way that `connection_` could be freed in the previous bug, but I can't see any reason why that would be hard.

So I'm going to pass this through to the relevant folks in engineering, assuming this can be used for renderer RCE on Android since <https://chromium-review.googlesource.com/c/chromium/src/+/3540656> was introduced in M103.

### pe...@google.com (2024-05-10)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-10)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-05-20)

Project: chromium/src
Branch: main

commit b4ad3013edb113cb8321a8adce3ad2ec333620ea
Author: Muyao Xu <muyaoxu@google.com>
Date:   Mon May 20 22:51:10 2024

    [Presentation API] Fix potential UAF on Clank
    
    This fixes a potential UAF in PresentationConnectionCallbacks::OnSuccess.
    
    Bug: 339588211
    Change-Id: Ie1aec9bbbb35991b14d1c97c538ab1262ab23b0e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5551853
    Commit-Queue: Muyao Xu <muyaoxu@google.com>
    Reviewed-by: Mark Foltz <mfoltz@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1303501}

M       third_party/blink/renderer/modules/presentation/presentation_connection_callbacks.cc

https://chromium-review.googlesource.com/5551853


### pe...@google.com (2024-05-21)

Requesting merge to extended stable (M124) because latest trunk commit (1303501) appears to be after extended stable branch point (1274542).
Requesting merge to stable (M125) because latest trunk commit (1303501) appears to be after stable branch point (1287751).
Requesting merge to beta (M126) because latest trunk commit (1303501) appears to be after beta branch point (1300313).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-05-21)

Merge review required: M126 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-05-21)

Merge review required: M125 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-05-21)

Merge review required: M124 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

### mu...@google.com (2024-05-22)

There's no known poc so I will only merge it to Beta (M126).

### mu...@google.com (2024-05-22)

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>
  This CL fixes a potential security vulnerability

2. What changes specifically would you like to merge? Please link to Gerrit.
   <https://chromium-review.googlesource.com/c/chromium/src/+/5551853>
3. Have the changes been released and tested on canary?
   Yes.
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
   No.
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
   No. We don't know yet how this uaf could be triggered.

### am...@chromium.org (2024-05-24)

hi muyaoxu@ -- thanks for the fix. A known poc isn't a precondition for backmerge; since it does appear a potential UAF has been present since M103, we should probably consider a backmerge here. The only considerations to not backmerge is if this were determined to not be reachable or exploitable in Chrome OR if there was a stability, functional, or other risk or concern with backmerge.
The fix appears to be pretty minimal and does not seem to cause any issues on Canary since it was landed.
Therefore, I'm approving <https://crrev.com/c/5551853> for backmerge to M126 Beta (branch 6478), as well as M125 Stable (6422), and M124 Extended Stable (6367).
Please let me know if you have any issues or concerns with this.

Please complete all merges at soonest so this fix can be included in next week's updates for each -- thank you!

### pe...@google.com (2024-05-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-05-28)

Project: chromium/src
Branch: refs/branch-heads/6478

commit c60cbe5bfc60abe1204463d4a014e0d1b2e33aee
Author: Muyao Xu <muyaoxu@google.com>
Date:   Tue May 28 18:38:01 2024

    [Presentation API] Cherry Pick to M126 Beta - Fix potential UAF on Clank
    
    This fixes a potential UAF in PresentationConnectionCallbacks::OnSuccess.
    
    (cherry picked from commit b4ad3013edb113cb8321a8adce3ad2ec333620ea)
    
    Bug: 339588211
    Change-Id: Ie1aec9bbbb35991b14d1c97c538ab1262ab23b0e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5551853
    Commit-Queue: Muyao Xu <muyaoxu@google.com>
    Reviewed-by: Mark Foltz <mfoltz@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1303501}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5577494
    Commit-Queue: Krishna Govind <govind@chromium.org>
    Reviewed-by: Krishna Govind <govind@chromium.org>
    Owners-Override: Krishna Govind <govind@chromium.org>
    Auto-Submit: Muyao Xu <muyaoxu@google.com>
    Commit-Queue: Mark Foltz <mfoltz@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#743}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/modules/presentation/presentation_connection_callbacks.cc

https://chromium-review.googlesource.com/5577494


### ap...@google.com (2024-05-28)

Project: chromium/src
Branch: refs/branch-heads/6422

commit c4c47751f92557c9b254e830e6925b5458b331c9
Author: Muyao Xu <muyaoxu@google.com>
Date:   Tue May 28 18:37:04 2024

    [Presentation API]Cherry Pick to M125 Stable-Fix potential UAF on Clank
    
    This fixes a potential UAF in PresentationConnectionCallbacks::OnSuccess.
    
    (cherry picked from commit b4ad3013edb113cb8321a8adce3ad2ec333620ea)
    
    Bug: 339588211
    Change-Id: Ie1aec9bbbb35991b14d1c97c538ab1262ab23b0e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5551853
    Commit-Queue: Muyao Xu <muyaoxu@google.com>
    Reviewed-by: Mark Foltz <mfoltz@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1303501}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5577158
    Auto-Submit: Muyao Xu <muyaoxu@google.com>
    Commit-Queue: Krishna Govind <govind@chromium.org>
    Owners-Override: Krishna Govind <govind@chromium.org>
    Reviewed-by: Krishna Govind <govind@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6422@{#1175}
    Cr-Branched-From: 9012208d0ce02e0cf0adb9b62558627c356f3278-refs/heads/main@{#1287751}

M       third_party/blink/renderer/modules/presentation/presentation_connection_callbacks.cc

https://chromium-review.googlesource.com/5577158


### ap...@google.com (2024-05-28)

Project: chromium/src
Branch: refs/branch-heads/6478

commit c60cbe5bfc60abe1204463d4a014e0d1b2e33aee
Author: Muyao Xu <muyaoxu@google.com>
Date:   Tue May 28 18:38:01 2024

    [Presentation API] Cherry Pick to M126 Beta - Fix potential UAF on Clank
    
    This fixes a potential UAF in PresentationConnectionCallbacks::OnSuccess.
    
    (cherry picked from commit b4ad3013edb113cb8321a8adce3ad2ec333620ea)
    
    Bug: 339588211
    Change-Id: Ie1aec9bbbb35991b14d1c97c538ab1262ab23b0e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5551853
    Commit-Queue: Muyao Xu <muyaoxu@google.com>
    Reviewed-by: Mark Foltz <mfoltz@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1303501}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5577494
    Commit-Queue: Krishna Govind <govind@chromium.org>
    Reviewed-by: Krishna Govind <govind@chromium.org>
    Owners-Override: Krishna Govind <govind@chromium.org>
    Auto-Submit: Muyao Xu <muyaoxu@google.com>
    Commit-Queue: Mark Foltz <mfoltz@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#743}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/modules/presentation/presentation_connection_callbacks.cc

https://chromium-review.googlesource.com/5577494


### ap...@google.com (2024-05-28)

Project: chromium/src
Branch: refs/branch-heads/6367

commit 696f7633f70b09de3b988aa843f54b0954e3d6fd
Author: Muyao Xu <muyaoxu@google.com>
Date:   Tue May 28 21:35:53 2024

    [Presentation API] Cherry Pick to Extended Stable - Fix potential UAF on Clank
    
    This fixes a potential UAF in PresentationConnectionCallbacks::OnSuccess.
    
    (cherry picked from commit b4ad3013edb113cb8321a8adce3ad2ec333620ea)
    
    Bug: 339588211
    Change-Id: Ie1aec9bbbb35991b14d1c97c538ab1262ab23b0e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5551853
    Commit-Queue: Muyao Xu <muyaoxu@google.com>
    Reviewed-by: Mark Foltz <mfoltz@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1303501}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5577159
    Commit-Queue: Mark Foltz <mfoltz@chromium.org>
    Auto-Submit: Muyao Xu <muyaoxu@google.com>
    Cr-Commit-Position: refs/branch-heads/6367@{#1244}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       third_party/blink/renderer/modules/presentation/presentation_connection_callbacks.cc

https://chromium-review.googlesource.com/5577159


### pg...@google.com (2024-05-29)

Hello, reporter - thank you for the report! How would you like to be credited for the discovery?

### sp...@google.com (2024-05-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
While we were able to make a security relevant change, the report lacks a POC and /or demonstration of the potential or reachability of UAF or exploitability.

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are not already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-30)

Thank you for your effort and reporting this issue to us!

### ha...@gmail.com (2024-05-30)

credit:anymous

### pe...@google.com (2024-08-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### kd...@gmail.com (2025-12-14)

Hi, while trying to reproduce this bug, I failed to do so, and noted that this may be an FP. Feel free to point out if I'm wrong.

```
  WeakPersistent<ControllerPresentationConnection> connection_; // [0]
  Persistent<PresentationRequest> request_; // [1]

```

Following the Oilpan document (<https://chromium.googlesource.com/chromium/src/+/main/third_party/blink/renderer/platform/heap/BlinkGCAPIReference.md>),
only the Weakxxx Object suffer from the GC issues, while the Persistent / Member do not.
Specifically, original [b/40053095](https://issues.chromium.org/issues/40053095) can free the `client_` [0] because `client_` is a WeakPersistent object, which does not guarantee the object is alive.
However, the `request_` in this report is a `Persistent` object [1], "which makes the referred object alive unconditionally". Thus, I consider this issue as an FP.

## Bounty Award

> While we were able to make a security relevant change, the report lacks a POC and /or demonstration of the potential or reachability of UAF or exploitability.
> 
> Thank you for your efforts and helping us make Chrome more secure for all users!
> 
> Cheers,
> Chrome VRP Panel Bot
> 
> 
> P.S. Two other things we'd like to mention:
> 
> * Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339588211)*
