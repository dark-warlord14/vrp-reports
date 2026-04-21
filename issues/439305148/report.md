# Mojo’s ChannelPosix incorrectly handles >128 file descriptors in a message, leading to fd confusion

| Field | Value |
|-------|-------|
| **Issue ID** | [439305148](https://issues.chromium.org/issues/439305148) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo |
| **Platforms** | Android, Linux, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ff...@google.com |
| **Created** | 2025-08-18 |
| **Bounty** | $30,000.00 |

## Description

VULNERABILITY DETAILS
If more than 128 file descriptors are sent in a single Mojo message on platforms using ChannelPosix (Linux, Android, ChromeOS), the extra file descriptors are silently dropped and never seen by the receiver. If more file descriptors are subsequently transmitted on the same channel, the receiver will incorrectly combine the new file descriptors with the original incomplete set, resulting in a corrupted message.

The problem affects all process types using Mojo (browser, renderer, GPU, etc.). Its impact varies depending on the Mojo interface being attacked; we provide three reproduction cases as examples, but in general any interface using an arbitrary number of file descriptors (e.g., handle<shared\_buffer>, BigBuffer, BigString16, etc.) in a single message may be vulnerable.

The root cause is that ChannelPosix::WriteNoLock[1] splits transmitted file descriptors into batches of 128 (kMaxSendmsgHandles). The first batch of 128 is sent correctly, but if all of the message data was also sent with the first message, subsequent batches *only* consist of file descriptors and have zero bytes of actual message data.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/channel_posix.cc;l=341;bpv=1>

The underlying message conduit (sendmsg(2)) does not support sending zero bytes of actual data together with non-zero ancillary data (cmsg(3)), because the socket is created with SOCK\_STREAM instead of SOCK\_DGRAM. Therefore, the subsequent file descriptor batches will be silently dropped.

On the receiving side, the original message with >128 file descriptors will correctly receive the first batch of 128 file descriptors, but then remain stuck (DispatchResult::kMissingHandles) until enough other file descriptors are received from subsequent messages.

This bug was introduced in 2019 by <https://source.chromium.org/chromium/chromium/src/+/5e25b795ba30601fbd543fb311e28c946de52560>.

VERSION
Chrome Version: 139.0.7258.5 (Official Build) beta (64-bit)
Operating System: Linux (Debian 13), Android (16), ChromeOS (unconfirmed but presumed vulnerable)

REPRODUCTION CASE
Three reproduction cases are attached. To reproduce, download all the .html files to a directory, run `python -m http.server`, and navigate to each specific PoC page.

###########################################################################

## poc1.html

###########################################################################

Simplest case; triggers an immediate browser or renderer segfault.

Sequence of events when clicking “Crash browser”:

1. Page uses postMessage to send 65 large ImageBitmaps to an iframe hosted by another renderer (requiring a trip through the browser process). Because each in-transit ArrayBuffer is represented by 2 file descriptors (1 on Android), this means sending 130 fds in a single message, causing the last 2 to become lost.
2. Page sends 1 small ImageBitmap to the same destination. This unblock processing of the message in the browser process.
3. The browser receives the incoming message (RemoteFrameHost.RouteMessageEvent) and attempts to copy image bitmaps into non-shared memory in CreateSkBitmapForPixelData.
4. Copying the first 64 bitmaps works normally, but the 65th bitmap is now pointing to the smaller shared memory segment sent in step 2, leading to an out-of-bounds read.

Sequence of events when clicking “Crash renderer”:

1. The page sends 65 transferable ArrayBuffers to the destination renderer. Again, the last one gets dropped, so the browser enqueues the message until another fd arrives.
2. The page sends 1 ArrayBuffer. The fd from this message unblocks the message enqueued in step one, so the browser tries to send 65 ArrayBuffers to the destination renderer. The last one is dropped, so the renderer is now holding the message in a queue until the next fd arrives. The message itself sent in this step is enqueued by the browser, because it is now missing an fd.
3. The page sends 1 smaller ArrayBuffer. The fd from this message unblocks the message queued by the browser in step 2, which in turn unblocks the message queued by the renderer in that same step.
4. The target renderer receives 65 ArrayBuffers, but the fd of the last one points to the *smaller* ArrayBuffer sent in step 2. The target renderer crashes when trying to copy the ArrayBuffer contents from shared memory.

Crucially, unlike ImageBitmaps, ArrayBuffers aren’t copied by the browser during transit, so the corrupted ArrayBuffer passes through the browser unnoticed.

###########################################################################

## poc2.html

###########################################################################

This variant uses fd confusion to disrupt the ipcz handshake sequence when a MessageChannel is transferred between two renderers. The effect is that the destination renderer is terminated immediately by ipcz with this error:

[257966:5:0815/230712.588877:ERROR:third\_party/ipcz/src/ipcz/router.cc:1124] Disconnecting Router due to failed introduction

Note that the destination frame can be a purely cross-origin page without any scripting or messaging access. Any other page/tab sharing its renderer will also be terminated. The PoC uses this to remove Google ads from bbc.com in another tab.

**Note**: This example requires the bbc page to load a google ad to show the exploit. There is a chance that bbc.com won't load any google ads due to pure chance, if that occurs please refresh until it does.

Sequence of events:

1. Page creates an iframe with the victim page.
2. Page sends 65 transferable ArrayBuffers to the target page with postMessage. Since the last one is lost, the message remains queued in the browser process.
3. Page sends a MessageChannel port to the target page. Its file descriptor will fill the remaining slot in the message from step 2, allowing that message to be sent to the target renderer. Because of the bug described in the issue, the last ArrayBuffer will *again* be lost on its way from the browser to the renderer, so the incoming message will remain queued in the destination renderer. The second message (with the MessageChannel port) will remain queued in the browser, because it no longer has a file descriptor.
4. Page sends one ArrayBuffer to the target page. This unblocks the MessageChannel port to be sent to the target renderer from the browser. However, the file descriptor from that message will now take the place of the last ArrayBuffer for the original message sent to the renderer. All 65 ArrayBuffers will now finally be delivered to the renderer, although the last one now points to the file descriptor of the MessageChannel.
5. Page sends one final ArrayBuffer, which unblocks the ArrayBuffer from step 4 to be sent to the renderer, which in turn unblocks the MessageChannel port from step 3 to finally be delivered to the renderer. However, that port’s file descriptor is now pointing to the ArrayBuffer from step 4.
6. Ipcz starts a handshake in the target renderer for the MessageChannel port. This fails because the MessageChannel’s file descriptor is actually an ArrayBuffer, and the renderer is killed.

#############################################################################

## poc3.html

###########################################################################

Demonstrates file descriptor confusion by reading console.log() output from a frame (poc3-victim.html). *Note*: in this case the victim must be sharing the renderer process with the attacker, so this attack is more realistic on platforms with limited site isolation (Android & Android WebView).

While this example uses console.log(), similar fd confusion can be achieved with other mojo frame APIs which use BigString16 or other types of shared memory (e.g., copy & paste, printing, drag & drop).

Sequence of events:

1. Page sends the following to a sandboxed iframe created by the attacker: 65 transferables (A), 1 transferable (B), and 1 transferable (C). This results in the following mojo channel states:
   
   - Main page => browser channel: transferable C waiting for 1 fd.
   - Browser => evil frame: transferable B waiting for 1 fd.
2. Victim page is loaded in another frame and does a console.log(). The fd from this unblocks transferable C in the main page => browser channel, which in turn unblocks transferable B in the browser => evil frame channel.
3. Evil frame receives a message with transferable B, but its fd actually points to the console.log() message from the victim frame. The evil frame is able to extract the message by reading the ArrayBuffer contents.

#############################################################################

## poc4.html

###########################################################################

Still being developed at the time of this submission. We believe it may be possible to do a sandboxed ACE/possible sandbox-escaping ACE by confusing mojo into believing that a user controlled transferable is instead a privileged transferable.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab + browser + frame
Crash State: attached

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Sahan Fernando & Anon

## Attachments

- poc1.html (text/html, 1.3 KB)
- poc1-stack-browser.txt (text/plain, 5.2 KB)
- poc1-stack-renderer.txt (text/plain, 8.8 KB)
- poc2.html (text/html, 942 B)
- poc3.html (text/html, 581 B)
- poc3-evil.html (text/html, 380 B)
- poc3-victim.html (text/html, 300 B)

## Timeline

### me...@google.com (2025-08-18)

Thanks for the report. I can reproduce the crashes using poc1. Tentatively assigning high severity.

ffred: Could you please take a look and reassign as appropriate? Thanks.

### aj...@google.com (2025-08-18)

OS: needs `is_posix && !mojo_use_apple_channel` (fuchsia is not posix)

### ch...@google.com (2025-08-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-08-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-08-20)

Project: chromium/src  

Branch:  main  

Author:  Fred Shih [ffred@chromium.org](mailto:ffred@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6868069>

Add a CHECK so mojo channel will crash on large num of handles

---


Expand for full commit details
```
     
    This is an interim fix as this behavior is currently unsupported and 
    affects stability. A future CL will support this behavior with more 
    complete changes to the IPC system. 
     
    This issue does not manifest in debug builds, because a DCHECK will 
    crash the browser before sending the message over IPC. 
     
    Bug: 439305148 
    Change-Id: Ic6b406cd42334e91672b11fb7d6f562cf9e1a7a1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6868069 
    Reviewed-by: Alex Gough <ajgo@chromium.org> 
    Commit-Queue: Fred Shih <ffred@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1504144}

```

---

Files:

- M `mojo/core/channel_posix.cc`

---

Hash: [f1f86cfab0c45a7bed9e4241ed9194b63522ea8c](https://chromiumdash.appspot.com/commit/f1f86cfab0c45a7bed9e4241ed9194b63522ea8c)  

Date: Wed Aug 20 20:09:04 2025


---

### ff...@google.com (2025-08-25)

Dropping this to P2/S2, because we have a CHECK which prevents this illegal operation now.

### aj...@chromium.org (2025-08-25)

Marking Fixed to allow merges of a security fix. Follow-up created as child.

### aj...@chromium.org (2025-08-25)

Note: I don't see any CHECK crashes in <https://crash.corp.google.com/browse?q=EXISTS+%28SELECT+1+FROM+UNNEST%28CrashedStackTrace.StackFrame%29+WHERE+RegExp_Contains%28FunctionName%2C%27ChannelPosix%3A%3AWriteNoLock%27%29%29+AND+ComparableVersion%28product.version%29+%3E%3D+ComparableVersion%28%27141.0.7369.0%27%29#-samplereports:30,productname:1000,productversion:40,processtype:120,+magicsignature:1000,magicsignature2:50,stablesignature:50,clientid:100,osversion:100,cpuinfo:100,url:30,runningfinchexperiments:40000> so this is likely safe to merge

### sa...@gmail.com (2025-08-26)

Hello,

I noticed I am not able to access the child issue. Could you please give me access so I could follow along with updates?

Cheers

### ff...@google.com (2025-08-26)

I've added you to the child issue. By the way, thank you for the PoCs, they made this bug a lot easier to isolate and repro!

### aj...@google.com (2025-09-03)

Fixing Severity to allow merges.

### sp...@google.com (2025-09-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $30000.00 for this report.

Rationale for this decision:
While this report didn't fully demonstrate memory corruption or RCE, we do believe this was a sufficient and high-impact report of a site-isolation bypass, qualifying for a $30,000 reward accordingly 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-09-04)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-09-04)

<https://crrev.com/c/6868069> approved for merge to M140 Stable; this fix was landed back on 20 August and there are no apparent stability or other issues from the introduction of this CHECK across Canary, Dev, or Beta. Please merge this fix to M140 Stable / branch 7339 by EOD tomorrow, 5 September so that this fix can be included in next weeks M140 Stable channel update. Thank you.

### sr...@chromium.org (2025-09-05)

@ff...@chromium.org can you please help complete the merges before EOD today so they are ready for stable RC cut next monday 

### ff...@google.com (2025-09-05)

ack -- will do


### ch...@google.com (2025-09-05)

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-09-05)

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-09-05)

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ff...@google.com (2025-09-05)

1. Security issue
2. crrev.com/c/6918692
3. Yes
4. Not a new feature
5. N/A
6. No verification necessary

### dx...@google.com (2025-09-05)

Project: chromium/src  

Branch:  refs/branch-heads/7339  

Author:  Fred Shih [ffred@chromium.org](mailto:ffred@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6918692>

Add a CHECK so mojo channel will crash on large num of handles

---


Expand for full commit details
```
     
    This is an interim fix as this behavior is currently unsupported and 
    affects stability. A future CL will support this behavior with more 
    complete changes to the IPC system. 
     
    This issue does not manifest in debug builds, because a DCHECK will 
    crash the browser before sending the message over IPC. 
     
    (cherry picked from commit f1f86cfab0c45a7bed9e4241ed9194b63522ea8c) 
     
    Bug: 439305148 
    Change-Id: Ic6b406cd42334e91672b11fb7d6f562cf9e1a7a1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6868069 
    Reviewed-by: Alex Gough <ajgo@chromium.org> 
    Commit-Queue: Fred Shih <ffred@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1504144} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6918692 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Reviewed-by: Srinivas Sista <srinivassista@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7339@{#1817} 
    Cr-Branched-From: 27be8b77710f4405fdfeb4ee946fcabb0f6c92b2-refs/heads/main@{#1496484}

```

---

Files:

- M `mojo/core/channel_posix.cc`

---

Hash: [b345ae9920e3a8d3ec027a015b9528d5e5dc3e25](https://chromiumdash.appspot.com/commit/b345ae9920e3a8d3ec027a015b9528d5e5dc3e25)  

Date: Fri Sep 5 20:02:47 2025


---

### pe...@google.com (2025-09-05)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ff...@google.com (2025-09-05)

1. No, the bug has been around for a while.
2. No, it is an independent change.

### pe...@google.com (2025-09-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-09-10)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6917122
2. Low - there was a small conflict.
3. 140
4. Yes, the issue was introduced in 2019.

### pe...@google.com (2025-09-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-09-10)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6922509
2. Low - there was no conflict.
3. 140
4. Yes, the issue was introduced in 2019.

### dx...@google.com (2025-09-27)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Fred Shih [ffred@chromium.org](mailto:ffred@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6922509>

[M138-LTS] Add a CHECK so mojo channel will crash on large num of handles

---


Expand for full commit details
```
     
    This is an interim fix as this behavior is currently unsupported and 
    affects stability. A future CL will support this behavior with more 
    complete changes to the IPC system. 
     
    This issue does not manifest in debug builds, because a DCHECK will 
    crash the browser before sending the message over IPC. 
     
    (cherry picked from commit f1f86cfab0c45a7bed9e4241ed9194b63522ea8c) 
     
    Bug: 439305148 
    Change-Id: Ic6b406cd42334e91672b11fb7d6f562cf9e1a7a1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6868069 
    Reviewed-by: Alex Gough <ajgo@chromium.org> 
    Commit-Queue: Fred Shih <ffred@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1504144} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6922509 
    Reviewed-by: Fred Shih <ffred@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Owners-Override: Michael Ershov <miersh@google.com> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3419} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `mojo/core/channel_posix.cc`

---

Hash: [09713b645171e52dfe683f17f5941cac57b35e9a](https://chromiumdash.appspot.com/commit/09713b645171e52dfe683f17f5941cac57b35e9a)  

Date: Sat Sep 27 05:02:21 2025


---

### dx...@google.com (2025-10-01)

Project: chromium/src  

Branch:  refs/branch-heads/6834  

Author:  Fred Shih [ffred@chromium.org](mailto:ffred@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6917122>

[M132-LTS] Add a CHECK so mojo channel will crash on large num of handles

---


Expand for full commit details
```
     
    This is an interim fix as this behavior is currently unsupported and 
    affects stability. A future CL will support this behavior with more 
    complete changes to the IPC system. 
     
    This issue does not manifest in debug builds, because a DCHECK will 
    crash the browser before sending the message over IPC. 
     
    (cherry picked from commit f1f86cfab0c45a7bed9e4241ed9194b63522ea8c) 
     
    Bug: 439305148 
    Change-Id: Ic6b406cd42334e91672b11fb7d6f562cf9e1a7a1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6868069 
    Reviewed-by: Alex Gough <ajgo@chromium.org> 
    Commit-Queue: Fred Shih <ffred@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1504144} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6917122 
    Reviewed-by: Fred Shih <ffred@chromium.org> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Owners-Override: Michael Ershov <miersh@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/6834@{#5650} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `mojo/core/channel_posix.cc`

---

Hash: [1963a0c12a5e313f06fca8cd9f1152cdf3b032da](https://chromiumdash.appspot.com/commit/1963a0c12a5e313f06fca8cd9f1152cdf3b032da)  

Date: Wed Oct 1 02:06:46 2025


---

### ch...@google.com (2025-12-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> While this report didn't fully demonstrate memory corruption or RCE, we do believe this was a sufficient and high-impact report of a site-isolation bypass, qualifying for a $30,000 reward accordingly

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/439305148)*
