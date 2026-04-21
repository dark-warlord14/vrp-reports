# Security: UAF in P2PSocketTcpServer::DoAccept

| Field | Value |
|-------|-------|
| **Issue ID** | [40057990](https://issues.chromium.org/issues/40057990) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>Network |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | or...@chromium.org |
| **Created** | 2021-11-23 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

P2PSocketTcpServer::DoAccept would call HandleAcceptResult if the result of Accept is not equal to net::ERR\_IO\_PENDING [1]. And HandleAcceptResult subsequently calls OnError if the result is negative [2]. This will destroy the P2PSocketTcpServer instance by erasing it from a flat\_map in P2PSocketManager [3]. However, DoAccept continues to access class members in a while loop after its destruction, which leads to UAF.

void P2PSocketTcpServer::DoAccept() {  

while (true) {  

int result = socket\_->Accept(&accept\_socket\_, accept\_callback\_);  

if (result == net::ERR\_IO\_PENDING) {  

break;  

} else {  

HandleAcceptResult(result); // ======> [1]  

}  

}  

}

void P2PSocketTcpServer::HandleAcceptResult(int result) {  

if (result < 0) {  

if (result != net::ERR\_IO\_PENDING)  

OnError(); // ======> [2]  

return;  

}  

// ...  

}

void P2PSocketManager::DestroySocket(P2PSocket\* socket) {  

auto iter = sockets\_.find(socket);  

DCHECK(iter != sockets\_.end());  

sockets\_.erase(iter); // ======> [3]  

}

[1] <https://source.chromium.org/chromium/chromium/src/+/refs/tags/96.0.4664.45:services/network/p2p/socket_tcp_server.cc;l=74;drc=db9ae7941adc1d95c943accce9e0151d265fd640>  

[2] <https://source.chromium.org/chromium/chromium/src/+/refs/tags/96.0.4664.45:services/network/p2p/socket_tcp_server.cc;l=82;drc=db9ae7941adc1d95c943accce9e0151d265fd640>  

[3] <https://source.chromium.org/chromium/chromium/src/+/refs/tags/96.0.4664.45:services/network/p2p/socket_manager.cc;l=209;drc=58cd53660b6ef18dd3efa66e6f8ad0eb3e644d6c>

**VERSION**  

Chrome Version: 96.0.4664.45 (stable)

**REPRODUCTION CASE**  

I think the quick way to demonstrate the UAF is to trigger ENFILE (Too many open files) error on Linux platform by spawning lots of tcp connections to P2PSocketTcpServer.

1. Apply the patch.diff. This simulates the compromised renderer to send mojo request to setup a P2PSocketTcpServer. (It seems that we can't do it through mojo JS because the mojo call 'CreateSocket' requires native parameters)
2. Setup a HTTPServer and navigate to poc.html  
   
   python -m SimpleHTTPServer 8000  
   
   ./chrome <http://localhost:8000/poc.html>
3. Run spawn\_nc.sh which simply uses 'nc' command to establish tcp connections to P2PSocketTcpServer. When the number of opened sockets hits the system limit, Accept would return ERR\_INSUFFICIENT\_RESOURCES as result which triggers the UAF.  
   
   /bin/bash ./spawn\_nc.sh

NOTE:  

I noticed that the buggy code was deleted in <https://chromium-review.googlesource.com/c/chromium/src/+/3229278> , but the code still exists in currently official stable version (96.0.4664.45).

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 2.3 KB)
- [poc.html](attachments/poc.html) (text/plain, 70 B)
- [spawn_nc.sh](attachments/spawn_nc.sh) (text/plain, 129 B)
- [asan.log](attachments/asan.log) (text/plain, 35.8 KB)

## Timeline

### [Deleted User] (2021-11-23)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-23)

: how feasible would it be to merge https://chromium-review.googlesource.com/c/chromium/src/+/3229278 to M96 do you think? The buggy code appears gone in M97.

[Monorail components: Blink>WebRTC>Network]

### [Deleted User] (2021-11-23)

[Empty comment from Monorail migration]

### ni...@chromium.org (2021-11-24)

I'm was under the impression that the deleted code wasn't reachable at all in chromium. 
If code can't be reached without the patch, a merge seems uncalled for.

If a merge is desired, it might be easier to just disable CreateServerTcpSocket , like this change, https://chromium-review.googlesource.com/c/chromium/src/+/3226139/4/chrome/services/sharing/webrtc/ipc_packet_socket_factory.cc, and the similar code in 
third_party/blink/renderer/platform/p2p/ipc_socket_factory.c.

Someone more familiar with chrome code and processes than I am need to make that call.

### [Deleted User] (2021-11-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jt...@gmail.com (2021-11-25)


The asan log indicates the reachability of the buggy code:
Render side sends a `CreateSocket` mojo request to P2PSocketManager which lives in the Network service. The first parameter `P2PSocketType` specifies the type of socket to be created, which is a P2PSocketTcpServer in this case.

The purpose of this patch is only to simulate a compromised renderer to send the mojo request. On current stable version of chrome, this bug can be exploited for sandbox escaping.

### ni...@chromium.org (2021-11-25)

Thanks for explaining. So if an attacker has compromised the renderer process, this bug could be used by the attacker to also compromise the browser process?

I'm not familiar with this code, but to me, it seems the conceptually simplest fix would be to delete all support for TCP server sockets from the mojo api. Disabling CreateServerTcpSocket (making it always return null) would have about the same effect. 

### jt...@gmail.com (2021-11-25)

> So if an attacker has compromised the renderer process, this bug could be used by the attacker to also compromise the browser process?
Yes, more precisely, the UAF happens in Network service instead of the main browser process : )

Seems like the issue need to be re-triaged ? 

### rs...@chromium.org (2021-11-29)

nisse: You deleted socket_tcp_server.cc in  https://chromium-review.googlesource.com/c/chromium/src/+/3229278, so can that be merged to M96?

### rs...@chromium.org (2021-11-29)

(please don’t re-assign to me but put back to Untraiged instead).

### ni...@chromium.org (2021-11-30)

That could be merged, I think (I've mostly been involved on the webrtc side of things, and not so familiar with chromium processes and tradeoffs). There are also smaller possible fixes.

### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### jt...@gmail.com (2021-12-07)

Hi, any updates on this issue? The bug still exists in today's stable refresh and I think it would affect the extended stable branch of M96.

### ni...@chromium.org (2021-12-08)

Florent, please let me know what assistance you need from me to get the fixed merged, since I'm unfamiliar with the process.

### [Deleted User] (2021-12-08)

orphis: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### or...@chromium.org (2021-12-14)

[Empty comment from Monorail migration]

### or...@chromium.org (2021-12-14)

[Empty comment from Monorail migration]

### or...@chromium.org (2021-12-14)

Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
Yes, this is a security issue of high severity.

What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3229278

Have the changes been released and tested on canary?
Yes, since M97

Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No, removal of unused code which could be used in combination with another attack defeat the Chrome sandbox.



### [Deleted User] (2021-12-14)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-15)

Approving merge to M96, please merge to branch 4664.

### gi...@appspot.gserviceaccount.com (2021-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bb3e11c96bf15ed294d988692deb233b75047f55

commit bb3e11c96bf15ed294d988692deb233b75047f55
Author: Niels Möller <nisse@chromium.org>
Date: Mon Dec 20 10:38:40 2021

[Merge to M96] Delete P2PSocketTcpServer and related incoming TCP code.

Originally reviewed on
https://chromium-review.googlesource.com/c/chromium/src/+/3229278,
Delete P2PSocketTcpServer and related incoming TCP code.
(cherry picked from commit 7a969cb95bc5ba5f558ad12e57c7a3ab959a930a)

Originally reviewed on
https://chromium-review.googlesource.com/c/chromium/src/+/3226139,
Mark IpcPacketSocketFactory::CreateServerTcpSocket as UNREACHED
(cherry picked from commit 4b1700bfdc9173ecd6dc5024b40c0f9f821fc115)

Bug: webrtc:13065, chromium:1272967
Change-Id: I453da6a768b5b1a5ee34b27cc845c975ab1a495b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3344755
Reviewed-by: Florent Castelli <orphis@chromium.org>
Reviewed-by: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Clark DuVall <cduvall@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lambros Lambrou <lambroslambrou@chromium.org>
Reviewed-by: Josh Nohle <nohle@chromium.org>
Commit-Queue: Niels Möller <nisse@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1328}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/services/network/p2p/socket_test_utils.h
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/third_party/blink/renderer/platform/p2p/socket_client_impl.h
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/third_party/blink/renderer/platform/p2p/socket_client_impl.cc
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/third_party/blink/renderer/platform/p2p/socket_client_delegate.h
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/remoting/test/fake_socket_factory.h
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/chrome/services/sharing/webrtc/ipc_packet_socket_factory.cc
[delete] https://crrev.com/1200b0528e7f662295e7cdc941dbe55d3834ac7c/services/network/p2p/socket_tcp_server.h
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/services/network/p2p/socket.cc
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/chrome/services/sharing/webrtc/p2p_socket_client.h
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/remoting/protocol/chromium_socket_factory.h
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/services/network/BUILD.gn
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/third_party/blink/renderer/platform/p2p/ipc_socket_factory.h
[delete] https://crrev.com/1200b0528e7f662295e7cdc941dbe55d3834ac7c/services/network/p2p/socket_tcp_server_unittest.cc
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/services/network/p2p/socket_test_utils.cc
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/third_party/blink/renderer/platform/p2p/ipc_socket_factory.cc
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/remoting/protocol/chromium_socket_factory.cc
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/services/network/public/cpp/p2p_socket_type.h
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/services/network/public/mojom/p2p.mojom
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/chrome/services/sharing/webrtc/p2p_socket_client.cc
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/remoting/test/fake_socket_factory.cc
[modify] https://crrev.com/bb3e11c96bf15ed294d988692deb233b75047f55/chrome/services/sharing/webrtc/p2p_socket_client_delegate.h
[delete] https://crrev.com/1200b0528e7f662295e7cdc941dbe55d3834ac7c/services/network/p2p/socket_tcp_server.cc


### am...@google.com (2022-01-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-06)

Congratulations on another one! The VRP Panel has decided to award you $5,000 fro this report. Thank you for this report and nice work! 

### am...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-14)

Hello OP, because the fix for this issue did not link this bug report ID, our automation was not able to pick up this issue for inclusion in the release notes or to obtain a CVE when the fix shipped on Stable-- sincere apologies for that! Updated with the appropriate labels to ensure that gets corrected in the coming days.  

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1272967?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057990)*
