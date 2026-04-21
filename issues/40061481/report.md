# Use-after-free in Mojo ChannelMac::SendMessageLocked

| Field | Value |
|-------|-------|
| **Issue ID** | [40061481](https://issues.chromium.org/issues/40061481) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo |
| **Platforms** | Mac |
| **Reporter** | he...@gmail.com |
| **Assignee** | rs...@chromium.org |
| **Created** | 2022-10-26 |
| **Bounty** | $30,000.00 |

## Description

**Steps to reproduce the problem:**  

please see the attached asan log

**Problem Description:**  

memory corruption

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.5383.0 \*\*Channel: \*\* Canary

**OS:** Mac OS

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 12.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 12.6 KB)
- [main.html](attachments/main.html) (text/plain, 7.0 KB)
- [sub1.html](attachments/sub1.html) (text/plain, 310.4 KB)
- [sub2.html](attachments/sub2.html) (text/plain, 298.6 KB)
- [sub3.html](attachments/sub3.html) (text/plain, 289.1 KB)

## Timeline

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### he...@gmail.com (2022-10-26)

I found this SEGV all of a sudden when I'm installing an online extension in google extension store, with Mac 109.0.5383.0 version Chromium. 
Sorry for that I couldn't provide a stable steps to reproduce, since this is flaky and I'm still investigating it. Thank you.

### me...@chromium.org (2022-10-28)

Thanks for the report. Were you able to get a reproduction case? I'm not sure how actionable the stack trace is as is, but perhaps mojo folks could chime in?

[Monorail components: Internals>Mojo]

### me...@chromium.org (2022-10-28)

[Empty comment from Monorail migration]

### he...@gmail.com (2022-10-31)

[Comment Deleted]

### ad...@google.com (2022-11-03)

Per https://crbug.com/chromium/1378564#c5 this requires non-default features (probably ipcz), so tagging as SI-None.

rockot@ this is an ipcz crash so it'd be great to take a look. As it's a mojo bug I'll assume it can be used to elevate privilege from an already-compromised renderer, so High severity.

### he...@gmail.com (2022-11-03)

[Comment Deleted]

### he...@gmail.com (2022-11-14)

[Comment Deleted]

### he...@gmail.com (2022-11-14)

After some investigations, I found that the root cause is clear and it may related to the race condition of the `send_buffer_` in `ChannelMac`.

## RCA

As the comments in [1] says, the `write_lock_` lock in `ChannelMac ` [1] protects the `send_buffer_` member. Therefore, `SendMessageLocked` function is protected by the `write_lock_` lock in the `Write` function [2]. 

However, not all places which uses (i.e., write) `send_buffer_ ` member are protected by the `write_lock_` correctly. The `ShutDownOnIOThread` and the `ChannelMac::StartOnIOThread` function, which runs on the dedicated thread [3] (i.e., SingleThreadTaskRunner), could also access the `send_buffer_ ` and reset/invalidate the backing buffer of `send_buffer_` in [4][5]. 

Therefore the `send_buffer_` is actually not protected by the racing condition. It is then used as the backing buffer of the `mach_msg_header_t` in [6].  
The data racing could cause the `send_buffer_ ` buffer become invalid, i.e., the `buffer` address becomes invalid, too. When the buffer is casted to `mach_msg_header_t` type and is cleared/memset by zero (i.e., the default value of the struct mach_msg_header_t) in [6], the invalid buffer write happens.

[1]https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/channel_mac.cc;l=717-718;drc=26f382174adc04c0d92e7dff24c6aed5d5e0246b

[2]https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/channel_mac.cc;l=87;drc=26f382174adc04c0d92e7dff24c6aed5d5e0246b

[3]https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/channel_mac.cc;l=76-84;drc=26f382174adc04c0d92e7dff24c6aed5d5e0246b

[4]https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/channel_mac.cc;l=225;drc=26f382174adc04c0d92e7dff24c6aed5d5e0246b

  void ShutDownOnIOThread() {
    base::CurrentThread::Get()->RemoveDestructionObserver(this);

    watch_controller_.StopWatchingMachPort();

    send_buffer_.reset();  // [4] clear up the send_buffer_, not protected by the `write_lock_`.

[5]https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/channel_mac.cc;l=185;drc=26f382174adc04c0d92e7dff24c6aed5d5e0246b


  void StartOnIOThread() {
    vm_address_t address = 0;
    const vm_size_t size = getpagesize();
    kern_return_t kr =
        vm_allocate(mach_task_self(), &address, size,
                    VM_MAKE_TAG(VM_MEMORY_MACH_MSG) | VM_FLAGS_ANYWHERE);
    MACH_CHECK(kr == KERN_SUCCESS, kr) << "vm_allocate";
    send_buffer_.reset(address, size);   // [5] reset the send_buffer_, i.e., invalidate the original buffer, not protected by the `write_lock_`.

[6]https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/channel_mac.cc;l=363-367;drc=3d9b8b1314797ae919a82bfe9b916ad29914f3dd

  bool SendMessageLocked(MessagePtr message) {
    DCHECK(!send_buffer_contains_message_);
    base::BufferIterator<char> buffer(
        reinterpret_cast<char*>(send_buffer_.address()), send_buffer_.size()); // [6] racing and might freed buffer is being used as the backing buffer

    auto* header = buffer.MutableObject<mach_msg_header_t>(); // [6] cast the buffer to the mach_msg_header_t type
    *header = mach_msg_header_t{};    // [6] write/clear/memset the invalid backing buffer 

## Patch suggestion

Add `write_lock_ ` lock protection in both `ShutDownOnIOThread` and `StartOnIOThread` function, which ensures that the `send_buffer_ ` is still valid during `SendMessageLocked`.


### he...@gmail.com (2022-11-14)

Note that in my local fuzzing environment, this invalid write also be reproduced by loading my fuzzer-generated web-page. It is not stable to reproduce, but seems that this issue could be triggered by the malicious web page.

### rs...@chromium.org (2022-11-14)

Thank you for the excellent analysis! This bug exists outside of Ipcz, so I’m going to tag this as affecting current stable & extended.

### [Deleted User] (2022-11-14)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-11-14)

This is actually a UAF caused by a data race. As noted in c#9, because ShutDownOnIOThread does not properly synchronize access, the `send_buffer_` can be deallocated (freed) while another thread attempts to Write() to it.

https://chromium-review.googlesource.com/c/chromium/src/+/4027242

### [Deleted User] (2022-11-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bd8a1e43aa93d5bb7674cb5a431e7375f7e2f192

commit bd8a1e43aa93d5bb7674cb5a431e7375f7e2f192
Author: Robert Sesek <rsesek@chromium.org>
Date: Tue Nov 15 18:02:26 2022

Fix a data race leading to use-after-free in mojo::ChannelMac ShutDown

Bug: 1378564
Change-Id: I67041b1e2ef08dd0ee1ccbf6d534249c539b74db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4027242
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/heads/main@{#1071700}

[modify] https://crrev.com/bd8a1e43aa93d5bb7674cb5a431e7375f7e2f192/mojo/core/channel_mac.cc
[modify] https://crrev.com/bd8a1e43aa93d5bb7674cb5a431e7375f7e2f192/mojo/core/channel_unittest.cc


### rs...@chromium.org (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-16)

Requesting merge to extended stable M106 because latest trunk commit (1071700) appears to be after extended stable branch point (1036826).

Requesting merge to stable M107 because latest trunk commit (1071700) appears to be after stable branch point (1047731).

Requesting merge to beta M108 because latest trunk commit (1071700) appears to be after beta branch point (1058933).

Requesting merge to dev M109 because latest trunk commit (1071700) appears to be after dev branch point (1070088).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-16)

Merge approved: your change passed merge requirements and is auto-approved for M109. Please go ahead and merge the CL to branch 5414 (refs/branch-heads/5414) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-16)

Merge review required: M108 has already been cut for stable release.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-16)

Merge review required: M107 is already shipping to stable.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-16)

Merge review required: M106 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2022-11-16)

1. Sev-High security vulnerability fix
2. https://chromium-review.googlesource.com/c/chromium/src/+/4027242
3. Yes, 110.0.5422.0
4. No
5. N/A
6. No

### am...@chromium.org (2022-11-18)

Thanks for landing this fix, Robert, as well as for the responses to the merge questionnaire above. Merge approved for M108; please merge this fix to branch 5359 at your earliest convenience. 

There are no further releases planned for 106/Extended and 107/Stable; Stable RC for M108 has already been cut so this fix will likely ship in the M108 respin. 

### gi...@appspot.gserviceaccount.com (2022-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/176c526846cbb5d71f6411fbbdbd18d56073375a

commit 176c526846cbb5d71f6411fbbdbd18d56073375a
Author: Robert Sesek <rsesek@chromium.org>
Date: Fri Nov 18 19:31:38 2022

Fix a data race leading to use-after-free in mojo::ChannelMac ShutDown

(cherry picked from commit bd8a1e43aa93d5bb7674cb5a431e7375f7e2f192)

Bug: 1378564
Change-Id: I67041b1e2ef08dd0ee1ccbf6d534249c539b74db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4027242
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Ken Rockot <rockot@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1071700}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4035114
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Robert Sesek <rsesek@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#881}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/176c526846cbb5d71f6411fbbdbd18d56073375a/mojo/core/channel_mac.cc
[modify] https://crrev.com/176c526846cbb5d71f6411fbbdbd18d56073375a/mojo/core/channel_unittest.cc


### pb...@google.com (2022-11-22)

[Bulk Edit] Your merge has been approved for M109 Branch, please help complete your merges asap, so the change can be included in next week's M109  dev/beta RC build.

### [Deleted User] (2022-11-22)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8b0292179f0767dbc69eafd1bb9f22bf2f8e0bfd

commit 8b0292179f0767dbc69eafd1bb9f22bf2f8e0bfd
Author: Robert Sesek <rsesek@chromium.org>
Date: Mon Nov 28 17:44:58 2022

Fix a data race leading to use-after-free in mojo::ChannelMac ShutDown

(cherry picked from commit bd8a1e43aa93d5bb7674cb5a431e7375f7e2f192)

Bug: 1378564
Change-Id: I67041b1e2ef08dd0ee1ccbf6d534249c539b74db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4027242
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Ken Rockot <rockot@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1071700}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4059974
Auto-Submit: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5414@{#251}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/8b0292179f0767dbc69eafd1bb9f22bf2f8e0bfd/mojo/core/channel_mac.cc
[modify] https://crrev.com/8b0292179f0767dbc69eafd1bb9f22bf2f8e0bfd/mojo/core/channel_unittest.cc


### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### he...@gmail.com (2022-11-30)

Upload the previous fuzzer-generated PoC as https://crbug.com/chromium/1378564#c10 mentioned, just host the html files and visit the main.html to repro. It may not stable to repro as previously mentioned.

Moreover, I could verify that the patch mentioned in https://crbug.com/chromium/1378564#c13 works and this UAF is fixed indeed. Thank you very much.

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations! The VRP Panel has decided to award you $30,000 for this report. The data race in this issue was at all not significant enough to consider it a mitigation of this sufficiently impactful bug. We appreciate your analysis throughout as well as providing the new POC to provide a different pathway in demonstrating the exploitability of this issue. Thank you for your efforts in discovering and reporting this issue to us --- great work! 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1378564?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061481)*
