# Security: NAT Slipstreaming via RTSP(TCP/554) allows attacker to access local udp ports

| Field | Value |
|-------|-------|
| **Issue ID** | [40055059](https://issues.chromium.org/issues/40055059) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebRTC>Network, Internals>Network |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vo...@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2021-03-04 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

By using the technique described by Samy Kankar in <https://samy.pl/slipstream/>, it is possible for an attacker to access any UDP port listening on the victim's machine by making them visit a malicious page when certain conditions are met. The victim's home router has to implement an RTSP ALG as described in the before mentioned post. This is the case for my TP-Link Archer A7 v5.0 wifi router running the latest available firmware.

RECOMMENDATIONS  

Port 554 should be included in the kRestrictedPorts restricted ports list (<https://chromium.googlesource.com/chromium/src.git/+/refs/heads/master/net/base/port_util.cc>).

**VERSION**  

Chrome Version: 89.0.4389.72 (Official Build) (64-bit)  

Operating System: Linux Mint 20 Ulyana

**REPRODUCTION CASE**  

\* The rtsp\_slipstream\_chrome.mp4 attachment is a proof of concept video.  

\* udp\_s.py is a simple UDP server that just logs every message received.  

\* rtsp\_s.py is a malicious server that listens on port 554 and implements the attack logic.  

\* punch.html simulates a malicious page the victim visits. In order for it to work you have to input: the victim's local IP address, the port for the local udp server, and the malicious URL that points to the server that is running rtsp\_s.py. After inputting the required information, click the PUNCH button and inspect the offset number returned. Adjust the padding according to the offset until you get an OK message. Once you do, the "It works!" should be displayed in the victim's local UDP server.  

\* TPLinkArcherA7defaultALGconfig.png is a screenshot of my TP-Link wifi router default ALG config.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: bananabr

## Attachments

- deleted (application/octet-stream, 0 B)
- rtsp_s.py (text/plain, 4.1 KB)
- udp_s.py (text/plain, 368 B)
- punch.html (text/plain, 4.4 KB)
- TPLinkArcherA7defaultALGconfig.png (image/png, 85.0 KB)
- webrtc_turn_554.png (image/png, 191.7 KB)

## Timeline

### [Deleted User] (2021-03-04)

[Empty comment from Monorail migration]

### vo...@gmail.com (2021-03-04)

If this is accepted as a valid report please credit it to https://twitter.com/bananabr

### do...@chromium.org (2021-03-04)

+//net OWNERs, do you mind investigating this?

[Monorail components: Internals>Network]

### mm...@chromium.org (2021-03-04)

Believe this is a dupe of https://crbug.com/chromium/1176076

### mm...@chromium.org (2021-03-04)

Err, https://crbug.com/chromium/1144646, rather.  https://crbug.com/chromium/1176076 is investigating cost of the solution

### ri...@chromium.org (2021-03-04)

#5 It looks like it's using plain HTTP rather than RTSP to forge the request, so it gets around the username length limitation added in https://crbug.com/chromium/1144646. It's pretty clear I shouldn't have unblocked port 554.

### vo...@gmail.com (2021-03-04)

The attack is based on version 1.0 of the NAT slipstream technique. No webRTC involved, just plain HTTP.

### ri...@chromium.org (2021-03-04)

I think we can go through the Blink process for the fix to this as we don't have to reveal that there is a known attack.

### vo...@gmail.com (2021-03-04)

Could you please tell me what going through the Blink process means?

### [Deleted User] (2021-03-04)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2021-03-04)

+bheenan to be aware of enterprise implications.

### bh...@google.com (2021-03-04)

Thanks for flagging. Should I read this as us planning on blocking 554 at some point during an 89 respin? If so, is it possible to wait for M90 to put this change in a major release?

### ad...@chromium.org (2021-03-05)

Looks like it was unblocked in https://crbug.com/chromium/1164418 which doesn't say much about what % of enterprises have their PAC on port 554. Can you provide that information Brendan? To help decide whether to put this fix into M89 refresh or M90. And obviously, even before we make that decision, I suggest you start enterprise comms to ask enterprises to move their proxy.pacs to a different port, because one way or another this is coming soon.

### ri...@chromium.org (2021-03-05)

#9 Basically the Blink process just means that I send an email to blink-dev@chromium.org to notify people that this is going to happen and give people a chance to raise objections. See https://groups.google.com/a/chromium.org/g/blink-dev/c/4Btz5xQ-gXc/m/iPDxYSEgAgAJ for example. There's a page about the Blink process here https://www.chromium.org/blink/launching-features but I would not be separating implementation and shipping, I would do them together.

### ri...@chromium.org (2021-03-05)

#12 If we're going to wait until M90 then we need to think about the patch gap. My email to blink-dev@ may trigger some people to take a closer look at port 554.

### bh...@google.com (2021-03-05)

We don't have any metrics that show how many enterprises are using port 554 unfortunately. The best information we have is that when we blocked it in the M87 refresh, we got multiple reports from enterprises who we have direct communication. Given that most of that feedback flows through a specialist team of 6 people who communicate directly with large customers, we operate under the assumption that multiple reports from that small sample size = large enough portion of enterprises to care. I understand that's a much hazier answer than you'd prefer lacking any actual numbers, but I don't want to make something up.

I will draft a communication warning customers this change is coming in an M89 refresh in case that's the direction we need to go.

### bh...@google.com (2021-03-05)

Drafting language here: https://docs.google.com/document/d/1vl87w4OUXNxQkt1gMG5NF18t4NDcIBmuRzb6ZgxpEiE/edit?disco=AAAALm_tx3E

We're updating the enterprise release notes on Tuesday anyways, so if we confirm this is going to be an 89 refresh (hopefully asap), we can include that notice in the updates.

### ad...@chromium.org (2021-03-05)

Thanks for https://crbug.com/chromium/1184562#c16.

I'm OK with making this change in M90 rather than an M89 refresh. _Yes_ this is a well-known bug and a blink-dev mail will make it even more well known, but severity is correctly medium rather than high, and on the whole we don't merge medium severity fixes when there are known compatibility changes.

Could you get the change landed ASAP so there's plenty of time for people to run into problems on dev, beta etc.?

### bh...@google.com (2021-03-05)

Okay thanks, I'll hold off on comms then. Please let me know asap if that plan changes

### ad...@chromium.org (2021-03-05)

Can I suggest you still aim to do comms now, to warn that this is coming in M90? It's only ~5 weeks away.

### bh...@google.com (2021-03-05)

True, since we're doing the release notes update anyways, this is a light lift. Take a look at the link in #17 and make sure you're happy with that please

### ri...@chromium.org (2021-03-08)

[Empty comment from Monorail migration]

### ri...@chromium.org (2021-03-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f4c60d46c304bf75110ff3f3a9f79f3f50a73823

commit f4c60d46c304bf75110ff3f3a9f79f3f50a73823
Author: Adam Rice <ricea@chromium.org>
Date: Mon Mar 08 16:44:09 2021

Add port 554 (rtsp) to the restricted list

Safari and Firefox are already blocking port 554, and usage is low.
Block it.

See intent to ship thread:

https://groups.google.com/a/chromium.org/g/blink-dev/c/kyVo08TtOp8/m/nu4B94LcCAAJ

BUG=1184562

Change-Id: I9e36617c6e4b196749aedf66c69cabd634f0c611
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2738913
Commit-Queue: Ryan Sleevi <rsleevi@chromium.org>
Auto-Submit: Adam Rice <ricea@chromium.org>
Reviewed-by: Ryan Sleevi <rsleevi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#860750}

[modify] https://crrev.com/f4c60d46c304bf75110ff3f3a9f79f3f50a73823/net/base/port_util.cc


### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### ri...@chromium.org (2021-03-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-12)

This bug requires manual review: M90's targeted beta branch promotion date has already passed, so this requires manual review
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

### ri...@chromium.org (2021-03-12)

1. Yes
  - The port blocking feature is unit tested, although not this specific port. A web platform test will be landing shortly.
  - The change has been in canary for several days.
  - The change just adds an extra value to an array, it is exceedingly safe.
2. https://crbug.com/chromium/1184562#c24 https://chromium-review.googlesource.com/c/chromium/src/+/2738913
3. Yes
4. We are only targeting M90.
5. Security issue.
6. No.
7. N/A

### ad...@chromium.org (2021-03-12)

Approving merge to M90, branch 4430.

### gi...@appspot.gserviceaccount.com (2021-03-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6ae26830c165f92eeaf24f85fea825f47be20d5a

commit 6ae26830c165f92eeaf24f85fea825f47be20d5a
Author: Adam Rice <ricea@chromium.org>
Date: Fri Mar 12 18:49:42 2021

Add port 554 (rtsp) to the restricted list

Safari and Firefox are already blocking port 554, and usage is low.
Block it.

See intent to ship thread:

https://groups.google.com/a/chromium.org/g/blink-dev/c/kyVo08TtOp8/m/nu4B94LcCAAJ

BUG=1184562
TBR=rsleevi@chromium.org

(cherry picked from commit f4c60d46c304bf75110ff3f3a9f79f3f50a73823)

Change-Id: I9e36617c6e4b196749aedf66c69cabd634f0c611
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2738913
Commit-Queue: Ryan Sleevi <rsleevi@chromium.org>
Auto-Submit: Adam Rice <ricea@chromium.org>
Reviewed-by: Ryan Sleevi <rsleevi@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#860750}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2756308
Reviewed-by: Adam Rice <ricea@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4430@{#407}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/6ae26830c165f92eeaf24f85fea825f47be20d5a/net/base/port_util.cc


### vo...@gmail.com (2021-03-16)

Will this bug get a CVE assigned by any chance?

### ad...@chromium.org (2021-03-16)

Yes, we'll assign a CVE when we release the fix, which looks like it'll be M90 - https://chromiumdash.appspot.com/schedule for dates.

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### vo...@gmail.com (2021-03-18)

Does the last label update means this bug is not eligible for a reward? This is my first time reporting bugs to you, I am not sure how the labeling system works yet.

### ad...@chromium.org (2021-03-18)

I can reassure you that it doesn't mean that. In fact it means nothing. A couple of small mistakes were made in our bot wrangling so apologies for the label churn.

ricea@ - do you consider this fixed? If so please mark the bug as such.

### ri...@chromium.org (2021-03-18)

#35 Oops, sorry, yes, fixed.

### vo...@gmail.com (2021-03-18)

#35 thanks for the prompt reply.

### [Deleted User] (2021-03-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-24)

[Comment Deleted]

### am...@google.com (2021-03-24)

Congratulations, vovohelo@! The VRP Panel has awarded you $3000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for efforts in this clever finding and reporting this issue!

### vo...@gmail.com (2021-03-25)

#42 Thanks a lot for the bounty. Glad I could contribute.

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### vo...@gmail.com (2021-03-29)

Does the port restrictions defined in kRestrictedPorts apply to WebRTC TURN/STUN connections as well?

### mm...@chromium.org (2021-03-30)

[+webrtc OWNERs]:  Do you folks know if WebRTC respects the forbidder/reserved ports list in net/base/port_util.h?  I'm not seeing any calls, but could be missing something.

[Monorail components: Blink>WebRTC>Network]

### st...@chromium.org (2021-03-30)

According to https://bugs.chromium.org/p/webrtc/issues/detail?id=12497 the relevant code to fix this issue is https://source.chromium.org/chromium/chromium/src/+/master:third_party/webrtc/p2p/base/turn_port.cc;l=947;drc=ffb7603b6025fbd6e79f360d293ab49092bded54 which does not use net/base/port_util.h

I'll let Harald comment on possible integration with port_util.h in Chrome.

### mm...@chromium.org (2021-03-30)

Thanks!  That does look to address 554, but not ports above 1024, some of which were also added for the same issue, I believe.

### vo...@gmail.com (2021-03-30)

#48 based on empirical testing I know that port 1720 is blocked as well, for example. As you mentioned this port is not covered by https://source.chromium.org/chromium/chromium/src/+/master:third_party/webrtc/p2p/base/turn_port.cc;l=947;drc=ffb7603b6025fbd6e79f360d293ab49092bded54 so there is probably another piece code responsible for this.

### vo...@gmail.com (2021-03-30)

#48 I just want to make sure the TCP port 554 blockage is also applied to webrtc, otherwise, an attacker can apply the same principles to perform the attack.
The attached image shows a traffic capture of conversation between my chrome instance and a custom malicious TURN server running on port TCP/554. As you can see, but adjusting the advertised TCP MSS and using any of the attributes an attacker has control of in a Allocate Request message it is possible to align the TCP segments and perform the nat slipstreaming attack.

### to...@chromium.org (2021-03-30)

@deadbeef - do you know the answer to https://crbug.com/chromium/1184562#c46?

### de...@chromium.org (2021-03-30)

Yes, it appears WebRTC does respect the rejected list: https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/platform/p2p/ipc_socket_factory.cc;l=764;drc=184bf7b03160ebf2217ab4711118d013a750908a;bpv=0;bpt=1

### mm...@chromium.org (2021-03-30)

That's in the renderer process, which we don't trust to make security-relevant decisions, so we probably want a check in the network process as well.

### vo...@gmail.com (2021-04-05)

Just posting an interesting idea.
One could use this vulnerability to create a NAT udp pin-hole to port 10080/UDP (amanda) on the victims machine. Once 10080/UDP is accessible, the attacker sends an empty UDP datagram to the 10080 port with a source port N. The victim's nf_conntrack module creates an UDP "new connection" entry like N:10080. If the router has the nf_conntrack_amanda and nf_nat_amanda enabled, it will start to watch for a UDP datagrams with a source port 10080 and destination port N. If such a datagram is generated by the victim, and if it contains a string like "CONNECT DATA port1 MESG port1 INDEX port1 STATE port1" inside its payload, the router will create tcp NAT pin-holes for ports 1, 2, and 3. The attacker could generate a LOT of udp datagrams targeting port N using webRTC untils the OS allocates port 10080 as a source port. If this happens before the UDP "new connection" is dropped from the conntrack connections table, the attacker would now have access to port 1, 2, and 3 from the Internet.

I don't have a PoC for this yet, but it is technically sound IMO. I will try to work on a PoC but even if I can't, it is an interesting way to use amanda as way to create TCP NAT pin-holes once an attacker is able to create UDP pin-holes freely,

### vo...@gmail.com (2021-04-05)

Don't know if this is reason enough to block port 10080/UDP as well.

### vo...@gmail.com (2021-04-05)

Just realized most modern OSes ephemeral ports range won't include 10080 by default. So the probability of this attack chain being successful is extremely low.

### ad...@google.com (2021-04-07)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### ja...@google.com (2021-04-13)

[Empty comment from Monorail migration]

### vo...@gmail.com (2021-04-20)

If you don't mind me asking, does this bug qualify me to the security HoF?

### am...@chromium.org (2021-04-20)

Hi, vovohelo@, the Chrome VRP does not presently have a HoF. 
Only the Google VRP has one (https://bughunter.withgoogle.com/). Generally to be ranked in a VRP HoF, a researcher has submitted more than one bug as the rankings include researchers who have reported multiple and very impactful bugs over time. In any case, as I mentioned, there is not a HoF for the Chrome VRP. Sorry! 

### vo...@gmail.com (2021-04-20)

No problem at all. Asking doesn't hurt.
Now that the patch is publicly available, is it OK to write a blog post about the bug? If not, how long should I wait?

Thanks!

### am...@chromium.org (2021-04-22)

Thank you for the question and for asking in advance of publicizing! We ask that you not write about or share information about the bug publicly just yet and that you wait until the bug itself becomes public, which is 14 weeks after the fix is landed. This provides adequate time for all user populations to be able to receive the release update with the fix. 
This bug will be auto-updated with the allpublic label during that time and, like with other comments/updates to this bug, you'll receive an email when that occurs. For your planning purposes, if my math is correct that date should be on/about 24 June 2021. Thanks!! 

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### vo...@gmail.com (2021-06-15)

As the vulnerability is already fixed, I deleted the rtsp_slipstream_chrome.mp4 as it contained information I don't want to disclose.

### ri...@chromium.org (2021-06-16)

#65 Thanks.

### [Deleted User] (2021-06-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@gmail.com (2021-06-28)

Now that security restrictions are removed, is it work to publish an article about the bug?

Thanks,

### ad...@chromium.org (2021-06-28)

Please go ahead, thanks for checking!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1184562?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WebRTC>Network, Internals>Network]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055059)*
