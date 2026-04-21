# Security: UAF in MojoPipe

| Field | Value |
|-------|-------|
| **Issue ID** | [40075342](https://issues.chromium.org/issues/40075342) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo, Internals>Mojo>Bindings |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2023-10-20 |
| **Bounty** | $30,000.00 |

## Description

UAF in InterfaceEndpoints

Not protected by BackupRefPtr / MiraclePtr, without any user interaction, and the compromised renderer may not be needed.

**VULNERABILITY DETAILS**  

When the message pipe is disconnected, `OnPipeError` will traverse all endpoints of the current associated group:

```
void OnPipeError() {  
  ...  
    for (auto iter = endpoints_.begin(); iter != endpoints_.end();) {  
      Endpoint\* endpoint = iter->second.get();  
      ++iter;  
  
      if (endpoint->client())  
        endpoints_to_notify.push_back(endpoint);  
  
      MarkPeerClosedAndMaybeRemove(endpoint);  
    }  
  ...  
}  

```

If both the current endpoint and the peer endpoint are closed, the endpoint will be destructed:

```
void MarkPeerClosedAndMaybeRemove(Endpoint\* endpoint) {  
  lock_.AssertAcquired();  
  endpoint->set_peer_closed();  
  endpoint->SignalSyncMessageEvent();  
  if (endpoint->closed() && endpoint->peer_closed())  
    endpoints_.erase(endpoint->id());  
}  

```

When the endpoint is destructed, all sync messages it saves will also be cleared. And eventually, the endpoints of these sync messages will be erased from `endpoints_`:

```
class Endpoint {  
...  
  base::circular_deque<std::pair<uint32_t, MessageWrapper>> sync_messages_;  
...  
}  
===>>  
~MessageWrapper() {  
  if (value_.associated_endpoint_handles()->empty())  
    return;  
  
  controller_->lock_.AssertAcquired();  
  {  
    base::AutoUnlock unlocker(controller_->lock_);  
    value_.mutable_associated_endpoint_handles()->clear();  
  }  
}  
  
class COMPONENT_EXPORT(MOJO_CPP_BINDINGS_BASE) Message {  
...  
std::vector<ScopedInterfaceEndpointHandle> associated_endpoint_handles_;  
...  
}  
  
===>>  
ScopedInterfaceEndpointHandle::~ScopedInterfaceEndpointHandle() {  
  state_->Close(absl::nullopt);  
}  
  
===>>  
void Close(const absl::optional<DisconnectReason>& reason) {  
  ...  
  if (cached_group_controller) {  
    cached_group_controller->CloseEndpointHandle(cached_id, reason);// <<-----------  
  } else if (cached_peer_state) {  
    cached_peer_state->OnPeerClosedBeforeAssociation(reason);  
  }  
}  
  
===>>  
void CloseEndpointHandle(  
      mojo::InterfaceId id,  
      const absl::optional<mojo::DisconnectReason>& reason) override {  
  if (!mojo::IsValidInterfaceId(id))  
    return;  
  {  
    base::AutoLock locker(lock_);  
    DCHECK(base::Contains(endpoints_, id));  
    Endpoint\* endpoint = endpoints_[id].get();  
    DCHECK(!endpoint->client());  
    DCHECK(!endpoint->closed());  
    MarkClosedAndMaybeRemove(endpoint);// <<-----------  
  }  
  
  if (!mojo::IsPrimaryInterfaceId(id) || reason)  
    control_message_proxy_.NotifyPeerEndpointClosed(id, reason);  
}  
  
===>>  
void MarkClosedAndMaybeRemove(Endpoint\* endpoint) {  
  lock_.AssertAcquired();  
  endpoint->set_closed();  
  if (endpoint->closed() && endpoint->peer_closed())  
    endpoints_.erase(endpoint->id());// <<-----------  
}  

```

Then return and continue traversing the `endpoints_`. This UAF will be triggered when updating and accessing the iterator.

```
void OnPipeError() {  
  ...  
    for (auto iter = endpoints_.begin(); iter != endpoints_.end();) {  
      Endpoint\* endpoint = iter->second.get(); // <<-----------  
      ++iter;  
  
      if (endpoint->client())  
        endpoints_to_notify.push_back(endpoint);  
  
      MarkPeerClosedAndMaybeRemove(endpoint);  
    }  
  ...  
}  

```

**VERSION**  

Chrome Version: M118 stable  

Operating System: test on win

Bisect:

The relevant code causing the vulnerability seems to have been introduced very early:  

<https://source.chromium.org/chromium/chromium/src/+/2859a2ac06ab5d9df6706cc45525dc4a2085051c>  

Not sure if the introduction of newer code caused this vulnerability.

The owner should be assigned: [rockot@chromium.org](mailto:rockot@chromium.org)  

All branches (dev/beta/stable) are impacted.

**REPRODUCTION CASE**

Apply the patch poc.diff\*

$ python3 -m http.server 8000  

$ out/asan/chrome.exe --user-data-dir=xxxx "<http://localhost:8000/poc.html>"

\*. Since the bug itself has nothing to do with the two interfaces used, there may be a way that does not require the compromised renderer patch.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: browser.  

Crash State: see asan file.

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 29.5 KB)
- [poc.diff](attachments/poc.diff) (text/plain, 3.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 394 B)
- [sync_call.html](attachments/sync_call.html) (text/plain, 192 B)
- [sync_call.html](attachments/sync_call.html) (text/plain, 277 B)

## Timeline

### [Deleted User] (2023-10-20)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-10-21)

I did not repro myself as the provided asan trace and analysis appeared reasonable.

Setting severity-high as it is a UAF in the browser process, but appears to require a compromised/patched renderer (at least with the provided poc, as noted there may be other ways to trigger?)

Assuming this could affect any platform since it is in ipc/.

Setting foundin to the current extended-stable as this appears to be long-standing code.

[Monorail components: Internals>Core]

### [Deleted User] (2023-10-21)

[Empty comment from Monorail migration]

### le...@gmail.com (2023-10-21)

Yes, after my testing, this vulnerability also exists on at least Linux and Android. However, due to the differences in the message pipe implementation details between the platforms, the provided poc is only applicable to Windows. So please try this poc on Windows.


If it still cannot be reproduced, please fine-tune the timeout in `sync_call.html`. Or use the `sync_call.html` file attached to this comment.

### [Deleted User] (2023-10-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2023-10-31)

Ping.

### am...@chromium.org (2023-10-31)

adding other mojo SMEs to have a look rather than just leaving this assigned to a single potential owner 

[Monorail components: -Internals>Core Internals>Mojo Internals>Mojo>Bindings]

### [Deleted User] (2023-11-04)

rockot: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2023-11-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/686454625aa1bdc70a9215bdbb98c165c9c96b0f

commit 686454625aa1bdc70a9215bdbb98c165c9c96b0f
Author: Ken Rockot <rockot@google.com>
Date: Tue Nov 07 23:11:56 2023

Fix IPC Channel pipe teardown

Fixed: 1494461
Change-Id: I43319db27ff96621cf8115b02adcd4e56d946b29
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5010531
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/heads/main@{#1221251}

[modify] https://crrev.com/686454625aa1bdc70a9215bdbb98c165c9c96b0f/ipc/ipc_mojo_bootstrap.cc
[modify] https://crrev.com/686454625aa1bdc70a9215bdbb98c165c9c96b0f/ipc/ipc_channel_mojo_unittest.cc
[modify] https://crrev.com/686454625aa1bdc70a9215bdbb98c165c9c96b0f/ipc/ipc_test.mojom


### gi...@appspot.gserviceaccount.com (2023-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0e4278682cf72c9e697741faaf29b6872519be6c

commit 0e4278682cf72c9e697741faaf29b6872519be6c
Author: Igor Kraskevich <kraskevich@google.com>
Date: Wed Nov 08 10:13:53 2023

Revert "Fix IPC Channel pipe teardown"

This reverts commit 686454625aa1bdc70a9215bdbb98c165c9c96b0f.

Reason for revert: [Gardener] This CL breaks ConnectTest.FailedNonBrokerReferral/MojoIpczMultiprocess test on multiple bots, for example https://ci.chromium.org/ui/p/chrome/builders/ci/android-arm-tests/21427/test-results

Original change's description:
> Fix IPC Channel pipe teardown
>
> Fixed: 1494461
> Change-Id: I43319db27ff96621cf8115b02adcd4e56d946b29
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5010531
> Reviewed-by: Robert Sesek <rsesek@chromium.org>
> Commit-Queue: Ken Rockot <rockot@google.com>
> Cr-Commit-Position: refs/heads/main@{#1221251}

Change-Id: I9a42a8983207062487ccc3324fe5f9da10320f2a
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5010368
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Igor Kraskevich <kraskevich@google.com>
Owners-Override: Igor Kraskevich <kraskevich@google.com>
Cr-Commit-Position: refs/heads/main@{#1221465}

[modify] https://crrev.com/0e4278682cf72c9e697741faaf29b6872519be6c/ipc/ipc_mojo_bootstrap.cc
[modify] https://crrev.com/0e4278682cf72c9e697741faaf29b6872519be6c/ipc/ipc_channel_mojo_unittest.cc
[modify] https://crrev.com/0e4278682cf72c9e697741faaf29b6872519be6c/ipc/ipc_test.mojom


### [Deleted User] (2023-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-08)

Requesting merge to extended stable M118 because latest trunk commit (1221251) appears to be after extended stable branch point (1192594).

Requesting merge to stable M119 because latest trunk commit (1221251) appears to be after stable branch point (1204232).

Requesting merge to beta M120 because latest trunk commit (1221251) appears to be after beta branch point (1217362).

Merge review required: a reverted commit was detected after the merge request.

Merge review required: a reverted commit was detected after the merge request.

Merge review required: a reverted commit was detected after the merge request.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cd4c1f165c16c6d8161b5372ef7f61c715e01a42

commit cd4c1f165c16c6d8161b5372ef7f61c715e01a42
Author: Ken Rockot <rockot@google.com>
Date: Wed Nov 08 23:22:16 2023

Reland: Fix IPC Channel pipe teardown

This is a reland with the new test temporarily disabled on Android
until it can run without disrupting other tests.

Fixed: 1494461
Change-Id: If1d83c2dce62020f78dd50abc460973759002a1a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5015115
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1221953}

[modify] https://crrev.com/cd4c1f165c16c6d8161b5372ef7f61c715e01a42/ipc/ipc_mojo_bootstrap.cc
[modify] https://crrev.com/cd4c1f165c16c6d8161b5372ef7f61c715e01a42/ipc/ipc_channel_mojo_unittest.cc
[modify] https://crrev.com/cd4c1f165c16c6d8161b5372ef7f61c715e01a42/ipc/ipc_test.mojom


### [Deleted User] (2023-11-09)

Requesting merge to extended stable M118 because latest trunk commit (1221953) appears to be after extended stable branch point (1192594).

Requesting merge to stable M119 because latest trunk commit (1221953) appears to be after stable branch point (1204232).

Requesting merge to beta M120 because latest trunk commit (1221953) appears to be after beta branch point (1217362).

Merge review required: a reverted commit was detected after the merge request.

Merge review required: a reverted commit was detected after the merge request.

Merge review required: a reverted commit was detected after the merge request.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119, 120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-10)

M120 merge approved for https://crrev.com/c/5015115
please merge this fix to 120 Beta / branch 6099 by EOD Monday, 13 November so this fix can be included in the next M120 beta release 

The reland landed too close to the deadline for merge approval for M119 Stable and M118 Extended, (these RCs are being cut today) so I'll revisit early next week for merge approval to Stable channels. TY! 

### gi...@appspot.gserviceaccount.com (2023-11-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1843907e089061348c6698e06bfb328d2ef23b91

commit 1843907e089061348c6698e06bfb328d2ef23b91
Author: Ken Rockot <rockot@google.com>
Date: Sat Nov 11 00:12:43 2023

[M120] Reland: Fix IPC Channel pipe teardown

This is a reland with the new test temporarily disabled on Android
until it can run without disrupting other tests.

(cherry picked from commit cd4c1f165c16c6d8161b5372ef7f61c715e01a42)

Fixed: 1494461
Change-Id: If1d83c2dce62020f78dd50abc460973759002a1a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5015115
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1221953}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5018970
Auto-Submit: Ken Rockot <rockot@google.com>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/6099@{#514}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/1843907e089061348c6698e06bfb328d2ef23b91/ipc/ipc_mojo_bootstrap.cc
[modify] https://crrev.com/1843907e089061348c6698e06bfb328d2ef23b91/ipc/ipc_channel_mojo_unittest.cc
[modify] https://crrev.com/1843907e089061348c6698e06bfb328d2ef23b91/ipc/ipc_test.mojom


### [Deleted User] (2023-11-11)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-11-13)

[Empty comment from Monorail migration]

### vo...@google.com (2023-11-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-13)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-13)

[Empty comment from Monorail migration]

### vo...@google.com (2023-11-13)

1. One https://crrev.com/c/5019828
2. Low - no conflicts, medium size
3. M120 but requested to M118 and M119
4. Yes

### am...@google.com (2023-11-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-16)

Congratulations leecraso and Guang! The Chrome VRP Panel has decided to award you $30,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- amazing work! 

### am...@chromium.org (2023-11-16)

119 and 118 merges approved for https://crrev.com/c/5015115
Please merge this fix to M119 Stable / branch 6045 and M118 Extended / branch 5993 at your earliest convenience. 
Since tomorrow begins release freeze through next week, this fix will be release in the next M119 Stable and M118 Extended Stable security updates on the following Tuesday. Thanks! 

### gi...@appspot.gserviceaccount.com (2023-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b61ae97f6c2d5c9a103bd811e248d96804639ca9

commit b61ae97f6c2d5c9a103bd811e248d96804639ca9
Author: Ken Rockot <rockot@google.com>
Date: Thu Nov 16 23:23:22 2023

[M119] Reland: Fix IPC Channel pipe teardown

This is a reland with the new test temporarily disabled on Android
until it can run without disrupting other tests.

(cherry picked from commit cd4c1f165c16c6d8161b5372ef7f61c715e01a42)

Fixed: 1494461
Change-Id: If1d83c2dce62020f78dd50abc460973759002a1a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5015115
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1221953}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5038080
Auto-Submit: Ken Rockot <rockot@google.com>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/branch-heads/6045@{#1383}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/b61ae97f6c2d5c9a103bd811e248d96804639ca9/ipc/ipc_mojo_bootstrap.cc


### gi...@appspot.gserviceaccount.com (2023-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e13061c50998fb8422c77a4e9d4143c749bcaca6

commit e13061c50998fb8422c77a4e9d4143c749bcaca6
Author: Ken Rockot <rockot@google.com>
Date: Thu Nov 16 23:44:43 2023

[M118] Reland: Fix IPC Channel pipe teardown

This is a reland with the new test temporarily disabled on Android
until it can run without disrupting other tests.

(cherry picked from commit cd4c1f165c16c6d8161b5372ef7f61c715e01a42)

Fixed: 1494461
Change-Id: If1d83c2dce62020f78dd50abc460973759002a1a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5015115
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1221953}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5037764
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Auto-Submit: Ken Rockot <rockot@google.com>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/branch-heads/5993@{#1618}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/e13061c50998fb8422c77a4e9d4143c749bcaca6/ipc/ipc_mojo_bootstrap.cc


### am...@google.com (2023-11-18)

[Empty comment from Monorail migration]

### na...@google.com (2023-11-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b56b8773b30717b596c8d0b99ba8d4fa9dd60c2a

commit b56b8773b30717b596c8d0b99ba8d4fa9dd60c2a
Author: Ken Rockot <rockot@google.com>
Date: Wed Nov 22 15:24:29 2023

[M114-LTS] Reland: Fix IPC Channel pipe teardown

This is a reland with the new test temporarily disabled on Android
until it can run without disrupting other tests.

(cherry picked from commit cd4c1f165c16c6d8161b5372ef7f61c715e01a42)

(cherry picked from commit 1843907e089061348c6698e06bfb328d2ef23b91)

Fixed: 1494461
Change-Id: If1d83c2dce62020f78dd50abc460973759002a1a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5015115
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1221953}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5018970
Auto-Submit: Ken Rockot <rockot@google.com>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/6099@{#514}
Cr-Original-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5019828
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1642}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/b56b8773b30717b596c8d0b99ba8d4fa9dd60c2a/ipc/ipc_mojo_bootstrap.cc
[modify] https://crrev.com/b56b8773b30717b596c8d0b99ba8d4fa9dd60c2a/ipc/ipc_channel_mojo_unittest.cc
[modify] https://crrev.com/b56b8773b30717b596c8d0b99ba8d4fa9dd60c2a/ipc/ipc_test.mojom


### vo...@google.com (2023-11-23)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1494461?no_tracker_redirect=1

[Multiple monorail components: Internals>Mojo, Internals>Mojo>Bindings]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075342)*
