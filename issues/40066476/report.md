# Security: Heap-use-after-free in KeyRotationLauncherImpl::SynchronizePublicKey

| Field | Value |
|-------|-------|
| **Issue ID** | [40066476](https://issues.chromium.org/issues/40066476) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Enterprise>Connectors |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2023-06-27 |
| **Bounty** | $4,000.00 |

## Description

**Steps to reproduce the problem:**

1. apply change.diff and compile Chromium with ASAN enabled
2. start a server at the folder of poc.html
3. create file `DeviceTrustSigningKey` in path `/etc/chromium/policies/enrollment/` if it is not exist.
4. run `./chrome --enable-features=UserDTCInlineFlowEnabled --user-data-dir=/tmp/noexist http://127.0.0.1:8605/poc.html`

**Problem Description:**

1. Analysis

In the function `KeyRotationLauncherImpl::SynchronizePublicKey`, there is a std::ref `key_pair`[1] that is passed into the task on ThreadPool thread. If we could free the `key_pair` before `key_pair` is used, UAF occurs.  

Although the comment says that std::ref is OK, this `browser-level object (DeviceTrustKeyManager)` may not outlive the threadpool, we could free it on the main thread and use it again on ThreadPool.

```
void KeyRotationLauncherImpl::SynchronizePublicKey(  
    const SigningKeyPair& key_pair,  
    SynchronizationCallback callback) {  
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);  
  if (key_pair.is_empty()) {  
    LogSynchronizationError(DTSynchronizationError::kMissingKeyPair);  
    std::move(callback).Run(absl::nullopt);  
    return;  
  }  
  
  auto dm_token = dm_token_storage_->RetrieveDMToken();  
  if (!dm_token.is_valid()) {  
    LogSynchronizationError(DTSynchronizationError::kInvalidDmToken);  
    std::move(callback).Run(absl::nullopt);  
    return;  
  }  
  
  auto dm_server_url = GetDmServerUrl();  
  if (!dm_server_url) {  
    LogSynchronizationError(DTSynchronizationError::kInvalidServerUrl);  
    std::move(callback).Run(absl::nullopt);  
    return;  
  }  
  
  // Passing the key pair by reference is fine in this case as it is owned by  
  // a browser-level object (DeviceTrustKeyManager) and will outlive any task  
  // running on the ThreadPool.  
  base::ThreadPool::PostTaskAndReplyWithResult(  
      FROM_HERE,  
      {base::MayBlock(), base::TaskPriority::USER_BLOCKING,  
       base::TaskShutdownBehavior::SKIP_ON_SHUTDOWN},  
      base::BindOnce(&CreateRequest, GURL(dm_server_url.value()),  
                     dm_token.value(), std::ref(key_pair)),  
      base::BindOnce(&KeyRotationLauncherImpl::OnUploadRequestCreated,  
                     weak_factory_.GetWeakPtr(), std::move(callback)));  
}  

```

To trigger this more easily, I add a sleep[2] to give us more time to free the `key_pair`.

```
absl::optional<const KeyUploadRequest> CreateRequest(  
    const GURL& dm_server_url,  
    const std::string& dm_token,  
    const SigningKeyPair& key_pair) {  
  return KeyUploadRequest::Create(dm_server_url, dm_token, key_pair);  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/device_trust/key_management/browser/key_rotation_launcher_impl.cc;l=119;drc=55953e4c436007ec2a0a0619ce7b79b29d28ec71;bpv=0;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/device_trust/key_management/browser/key_rotation_launcher_impl.cc;l=38;drc=55953e4c436007ec2a0a0619ce7b79b29d28ec71;bpv=0;bpt=0>

PS:

In addition to the modification that slows the ThreadPool, we also need to modify some prefs settings[3] and provide a valid `dm_token` and a valid `dm_server_url` to run this function. On the stable version, these can be achieved through configuration. You could see the `change.txt` for more info.

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/device_trust/device_trust_connector_service.cc;l=34>

2. Bisect

This problem is introduced in this commit: 7c419a0c861719b6e838fe8cb4e348629272a1a3  

<https://chromium-review.googlesource.com/c/chromium/src/+/4013569>

According to the chromiumdash, this commit is introduced since Chrome Stable 109.0.5415.74

3. Suggested Patch

Maybe you could pass a value rather than pass a reference of `key_pair`.

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.0.0 \*\*Channel: \*\* Stable

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 108 B)
- [change.txt](attachments/change.txt) (text/plain, 4.0 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 29.9 KB)
- [DeviceTrustSigningKey](attachments/DeviceTrustSigningKey) (text/plain, 218 B)
- [video.webm](attachments/video.webm) (video/webm, 883.1 KB)

## Timeline

### [Deleted User] (2023-06-27)

[Empty comment from Monorail migration]

### nh...@google.com (2023-06-27)

@seblalacette: The reporter believes https://chromium-review.googlesource.com/c/chromium/src/+/4013569 introduced this bug. Can you take a look or find someone else to look into this crash?

[Monorail components: Enterprise>Connectors]

### [Deleted User] (2023-06-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-28)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2023-07-05)

[Comment Deleted]

### [Deleted User] (2023-07-11)

seblalancette: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2023-07-13)

Adding CCs. pleblanc - is there someone who might have cycles to look at this? Thanks!

### me...@gmail.com (2023-07-19)

Any update?


### [Deleted User] (2023-07-25)

seblalancette: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-26)

cc'ing hmare@ who works on Device Trust reviewed https://chromium-review.googlesource.com/c/chromium/src/+/4013569 for additional visibility -- can you PTAL or boost this for awareness in the team for triage and prioritization. Thank you! 

### se...@chromium.org (2023-07-26)

Sorry for the delay, just double-checked the shutdown sequence and the DeviceTrustKeyManager does get deleted before the ThreadPool, meaning the comment in the code is wrong. The window of opportunity for this issue is extremely slim, I'll look into how we can fix that.

### se...@chromium.org (2023-07-26)

Just a small update: I was able to reproduce the issue simply by adding a sleep at the same location (CreateRequest function) and closing the browser. Eventually the UAF would occur.

I believe the right way to fix this is to use a scoped_refptr to own the key instead of a unique_ptr. The key itself is very expensive to load into memory, and is equally expensive to copy. That is why we were using references as much as possible - but switching over to scoped_refptr fixes the UAF we're seeing while not impacting the performance costs as much as copying the key.

### gi...@appspot.gserviceaccount.com (2023-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ae6edf10e28a2044433f1879020da5ea91e9f3aa

commit ae6edf10e28a2044433f1879020da5ea91e9f3aa
Author: Sebastien Lalancette <seblalancette@chromium.org>
Date: Wed Jul 26 19:31:30 2023

[DTC] Make SigningKeyPair Ref Counted

In the current implementation, the Device Trust SigningKeyPair instance
was held in a unique_ptr inside the DeviceTrustKeyManager, which is a
browser-level object. However, in the shutdown sequence, it gets deleted
before the ThreadPool. This means that there is a (very slim)
possibility that any task running on the ThreadPool making use of that
key could run into a UAF problem.

Since the key is expensive to load or copy, the best way forward it to
convert this unique_ptr to a thread-safe ref-counted scoped_refptr.

Fixed: 1458303,b:293289710
Change-Id: I035f9447c6380e988fc4f796fe27740f604d997e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4722086
Commit-Queue: Sébastien Lalancette <seblalancette@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Hamda Mare <hmare@google.com>
Cr-Commit-Position: refs/heads/main@{#1175607}

[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/installer/key_rotation_manager_impl.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/attestation/browser/device_attester_unittest.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/signing_key_util.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/signing_key_pair_unittest.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/browser/device_trust_key_manager_impl_unittest.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/win_key_persistence_delegate.h
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/signing_key_util.h
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/browser/key_rotation_launcher_unittest.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/mac_key_persistence_delegate.h
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/linux_key_persistence_delegate.h
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/mac_key_persistence_delegate.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/browser/key_rotation_launcher.h
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/attestation/desktop/desktop_attestation_service_unittest.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/win_key_persistence_delegate.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/browser/key_rotation_launcher_impl.h
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/signing_key_pair.h
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/browser/device_trust_key_manager_impl.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/scoped_key_persistence_delegate_factory.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/installer/key_rotation_manager_impl.h
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/linux_key_persistence_delegate.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/key_persistence_delegate.h
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/browser/key_rotation_launcher_impl.cc
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/mock_key_persistence_delegate.h
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/browser/mock_key_rotation_launcher.h
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/browser/device_trust_key_manager_impl.h
[modify] https://crrev.com/ae6edf10e28a2044433f1879020da5ea91e9f3aa/chrome/browser/enterprise/connectors/device_trust/key_management/installer/key_rotation_manager_unittest.cc


### [Deleted User] (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-27)

Requesting merge to extended stable M114 because latest trunk commit (1175607) appears to be after extended stable branch point (1135570).

Requesting merge to stable M115 because latest trunk commit (1175607) appears to be after stable branch point (1148114).

Requesting merge to beta M116 because latest trunk commit (1175607) appears to be after beta branch point (1160321).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-27)

Merge review required: M116 is already shipping to beta.

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

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-27)

Merge review required: M115 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-27)

Merge review required: M114 is already shipping to stable.

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

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-31)

116 merge approved, please merge this fix to branch 5845 at your earliest convenience so this fix can be included in next M116/Beta update 

not approving merge to M115 and M114 as of right now due to current hold pattern with release team on RC cut for M115 respin 

### am...@chromium.org (2023-08-01)

M115/Stable and M114/Extended RC recuts have already occurred for (delayed) release tomorrow, there are no further planned updates of 115 and 114; removing labels accordingly 

### se...@chromium.org (2023-08-02)

116 cherrypick sent for review (crrev.com/c/4743180)

### gi...@appspot.gserviceaccount.com (2023-08-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fa681f4993ba048ba26ef6c4e608e16083bc369a

commit fa681f4993ba048ba26ef6c4e608e16083bc369a
Author: Sebastien Lalancette <seblalancette@chromium.org>
Date: Wed Aug 02 17:56:38 2023

[cherrypick][DTC] Make SigningKeyPair Ref Counted

In the current implementation, the Device Trust SigningKeyPair instance
was held in a unique_ptr inside the DeviceTrustKeyManager, which is a
browser-level object. However, in the shutdown sequence, it gets deleted
before the ThreadPool. This means that there is a (very slim)
possibility that any task running on the ThreadPool making use of that
key could run into a UAF problem.

Since the key is expensive to load or copy, the best way forward it to
convert this unique_ptr to a thread-safe ref-counted scoped_refptr.

(cherry picked from commit ae6edf10e28a2044433f1879020da5ea91e9f3aa)

Fixed: 1458303,b:293289710
Change-Id: I035f9447c6380e988fc4f796fe27740f604d997e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4722086
Commit-Queue: Sébastien Lalancette <seblalancette@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Hamda Mare <hmare@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1175607}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4743180
Auto-Submit: Sébastien Lalancette <seblalancette@chromium.org>
Commit-Queue: Hamda Mare <hmare@google.com>
Cr-Commit-Position: refs/branch-heads/5845@{#1070}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/attestation/browser/device_attester_unittest.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/installer/key_rotation_manager_impl.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/signing_key_util.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/signing_key_pair_unittest.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/browser/device_trust_key_manager_impl_unittest.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/win_key_persistence_delegate.h
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/browser/key_rotation_launcher_unittest.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/signing_key_util.h
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/mac_key_persistence_delegate.h
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/linux_key_persistence_delegate.h
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/mac_key_persistence_delegate.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/browser/key_rotation_launcher.h
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/attestation/desktop/desktop_attestation_service_unittest.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/win_key_persistence_delegate.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/browser/key_rotation_launcher_impl.h
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/signing_key_pair.h
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/browser/device_trust_key_manager_impl.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/scoped_key_persistence_delegate_factory.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/installer/key_rotation_manager_impl.h
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/linux_key_persistence_delegate.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/key_persistence_delegate.h
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/browser/key_rotation_launcher_impl.cc
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/core/persistence/mock_key_persistence_delegate.h
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/browser/mock_key_rotation_launcher.h
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/browser/device_trust_key_manager_impl.h
[modify] https://crrev.com/fa681f4993ba048ba26ef6c4e608e16083bc369a/chrome/browser/enterprise/connectors/device_trust/key_management/installer/key_rotation_manager_unittest.cc


### am...@google.com (2023-08-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-02)

Congratulations, Krace! The VRP Panel has decided to award you $4,000 for this report of a moderately mitigated (by race condition and shutdown) security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### se...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1458303?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066476)*
