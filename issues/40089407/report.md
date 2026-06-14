# Security: OOB Write in QuicStreamSequencerBuffer::OnStreamData

| Field | Value |
|-------|-------|
| **Issue ID** | [40089407](https://issues.chromium.org/issues/40089407) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Network>QUIC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@gmail.com |
| **Assignee** | rc...@chromium.org |
| **Created** | 2017-10-26 |
| **Bounty** | $10,500.00 |

## Description

VULNERABILITY DETAILS
Parsed QUIC stream packets are handled by QuicStreamSequencerBuffer::OnStreamData.

The current 'gap' to be filled in by the packet is found by traversing
a list of gaps:

```
  std::list<Gap>::iterator current_gap = gaps_.begin();
  while (current_gap != gaps_.end() && current_gap->end_offset <= offset) {
    ++current_gap;
  }

  DCHECK(current_gap != gaps_.end());
```

When offset == -1, current_gap == gaps_.end(). Several bounds checks involving offset and size occur before current_gap is accessed, but offset + size is not checked for overflow, so all of the checks can be passed. If the `BufferBlock`s were not larger than the maximum frame size (see kBlockSizeBytes), this would lead to an OOB write of the blocks as well. Therefore I'm attaching a patch that fixes both of these conditions.

If changing the bounds check is too costly, the overflow check should be
sufficient (I believe this check is more necessary.)

Note that ASAN will not reveal this bug because the overflow happens inside the QuicStreamSequencerBuffer object, where -1 is written to the pointer that backs `std::unique_ptr<BufferBlock* []> blocks_`.

VERSION
Chrome Version: 62 Stable
Operating System: All

REPRODUCTION CASE
Follow the same steps as my other report crbug.com/777728, substituting
server_frame_overflow.patch for the quic_server patch. Or see the unit
tests in the attached fix.patch.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: Browser
Crash State: See crash.log. ASAN won't work so use a debug build to see the DCHECK.

## Attachments

- [crash.log](attachments/crash.log) (text/plain, 7.7 KB)
- [fix.patch](attachments/fix.patch) (application/octet-stream, 2.2 KB)
- [server_frame_overflow.patch](attachments/server_frame_overflow.patch) (application/octet-stream, 1.2 KB)
- [www.example.org.tar](attachments/www.example.org.tar) (application/octet-stream, 8.5 KB)

## Timeline

### el...@chromium.org (2017-10-26)

[Empty comment from Monorail migration]

[Monorail components: Internals>Network>QUIC]

### pa...@chromium.org (2017-10-31)

Assigning to rch, as the person who last touched the relevant code. :)

I think this is a Critical, because it's an OOB write in the browser process. If I'm wrong, we can downgrade it, but I'm feeling a bit anxious about it at the moment. :) When we have a sandboxed network process, this kind of thing will be a High, but we're not there yet. +pennymac FYI

Thank you for the patch, too! The ideal fix in Chromium land is to use base/numerics (https://chromium.googlesource.com/chromium/src.git/+/lkcr/base/numerics/README.md), in this case perhaps `CheckAdd`. One might also imagine changing `typedef uint64_t QuicStreamOffset;` to `using QuicStreamOffset = base::CheckedNumeric<uint64_t>;` or such.

There may be more code like this in QUIC; an audit may be necessary?

### ne...@gmail.com (2017-10-31)

Changing the type of QuicStreamOffset to a CheckedNumeric is probably the way to go here; I went for simplicity to minimize the chance of a perf regression. I also have a fuzzer that I'd be willing to share once these fixes are merged to kick off an audit. I only have 4 cores :)

### sh...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-31)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-10-31)

We're starting our ramp-up for M62 Stable and urgently need to know what the full impact of this bug is. Can you please comment on how critical this bug is?

### ab...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### ne...@gmail.com (2017-10-31)

Hi, I think this is not exploitable as-is because only -1 can be written to the blocks_ pointer (only tested on Linux though). Any slight refactoring could immediately make it exploitable so it should be fixed ASAP, though a few days on Canary would probably be a net win in terms of avoiding a regression.

I think the stack buffer overflow on the other hand is truly Critical (crbug.com/777728), and should be a M62 Stable release blocker.

I did spend a few days analyzing these bugs before reporting them, so I'm pretty sure my analysis here is accurate.

### aw...@chromium.org (2017-10-31)

M62 stable is released and currently ramping up.  The first order of business is to get a fix tested and in to canary. rch@ - does the supplied patch look reasonable?

### pa...@chromium.org (2017-10-31)

+inferno: See #3, we may have a new fuzzer. :)

### pa...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### cb...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-01)

I'll get a fix landed ASAP

### aw...@chromium.org (2017-11-01)

Per discussion, downgrading to severity High. crbug.com/777728 remains critical.

### rc...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-01)

https://chromium-review.googlesource.com/c/chromium/src/+/748282 should be landing soon.

### sh...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a96567f02a0881561c964e5c11afe9c1af17a5f7

commit a96567f02a0881561c964e5c11afe9c1af17a5f7
Author: Ryan Hamilton <rch@chromium.org>
Date: Wed Nov 01 16:05:25 2017

Fix OOB Write in QuicStreamSequencerBuffer::OnStreamData

BUG=778505

Cq-Include-Trybots: master.tryserver.chromium.android:android_cronet_tester;master.tryserver.chromium.mac:ios-simulator-cronet
Change-Id: I1dfd1d26a2c7ee8fe047f7fe6e4ac2e9b97efa52
Reviewed-on: https://chromium-review.googlesource.com/748282
Commit-Queue: Ryan Hamilton <rch@chromium.org>
Reviewed-by: Zhongyi Shi <zhongyi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#513144}
[modify] https://crrev.com/a96567f02a0881561c964e5c11afe9c1af17a5f7/net/quic/core/quic_stream_sequencer_buffer.cc
[modify] https://crrev.com/a96567f02a0881561c964e5c11afe9c1af17a5f7/net/quic/core/quic_stream_sequencer_buffer_test.cc


### go...@chromium.org (2017-11-01)

Please request a merge to M63 once change listed at #21 is baked/verified in Canary. Thank you.

+awhalley@ for M63 merge review.

### rc...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

### rc...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-02)

This bug requires manual review: M63 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-11-02)

+awhalley@ for M63 merge review. Thank you.

### sh...@chromium.org (2017-11-03)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-11-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-05)

govind@ - good for M63

### go...@chromium.org (2017-11-05)

Approving merge to M63 branch 3239 based on https://crbug.com/chromium/778505#c31. Please merge before 4:00 PM PT, Monday (11/06) so we can take it for next week Beta release. Thank you.

### aw...@chromium.org (2017-11-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-11-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5cfdea08a3679bd9267f6642945a8b4698977e58

commit 5cfdea08a3679bd9267f6642945a8b4698977e58
Author: Ryan Hamilton <rch@chromium.org>
Date: Mon Nov 06 18:27:25 2017

[m63 merge] Fix OOB Write in QuicStreamSequencerBuffer::OnStreamData

BUG=778505
TBR=rch@chromium.org

(cherry picked from commit a96567f02a0881561c964e5c11afe9c1af17a5f7)

Cq-Include-Trybots: master.tryserver.chromium.android:android_cronet_tester;master.tryserver.chromium.mac:ios-simulator-cronet
Change-Id: I1dfd1d26a2c7ee8fe047f7fe6e4ac2e9b97efa52
Reviewed-on: https://chromium-review.googlesource.com/748282
Commit-Queue: Ryan Hamilton <rch@chromium.org>
Reviewed-by: Zhongyi Shi <zhongyi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#513144}
Reviewed-on: https://chromium-review.googlesource.com/755001
Reviewed-by: Ryan Hamilton <rch@chromium.org>
Cr-Commit-Position: refs/branch-heads/3239@{#390}
Cr-Branched-From: adb61db19020ed8ecee5e91b1a0ea4c924ae2988-refs/heads/master@{#508578}
[modify] https://crrev.com/5cfdea08a3679bd9267f6642945a8b4698977e58/net/quic/core/quic_stream_sequencer_buffer.cc
[modify] https://crrev.com/5cfdea08a3679bd9267f6642945a8b4698977e58/net/quic/core/quic_stream_sequencer_buffer_test.cc


### rc...@chromium.org (2017-11-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-07)

[Empty comment from Monorail migration]

### wf...@chromium.org (2017-11-08)

This is Critical as it's a browser bug accessible from the web. We assume all bugs are exploitable under certain conditions and so while the analysis in #10 is appreciated, it should not be taken into account for the purposes of bug severity.

### aw...@chromium.org (2017-11-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-11-09)

Superb! The VRP panel decided to award $10,500 for this bug :-)

### aw...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### ma...@google.com (2020-04-30)

[Empty comment from Monorail migration]

### is...@google.com (2020-04-30)

This issue was migrated from crbug.com/chromium/778505?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089407)*
