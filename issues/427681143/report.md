# P2PSocket(this) object is freed, causing Use-After-Free vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [427681143](https://issues.chromium.org/issues/427681143) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 138.0.7163.0 |
| **Reporter** | ja...@gmail.com |
| **Assignee** | ht...@google.com |
| **Created** | 2025-06-25 |
| **Bounty** | $25,000.00 |

## Description

# Steps to reproduce the problem

Access poc.html after applying diff

# Problem Description

Access to the freed object starts at: `https://source.chromium.org/chromium/chromium/src/+/main:services/network/p2p/socket_tcp.cc;l=391`
return true: `https://source.chromium.org/chromium/chromium/src/+/main:services/network/p2p/socket_tcp.cc;l=377`
The object is freed at: `https://source.chromium.org/chromium/chromium/src/+/main:services/network/p2p/socket_tcp.cc;l=305`

In the SendPacket function called by SendBatch, as in the first link, the iterator is stopped via return false when this object is freed.

In the third link, this object is freed, but if you look at the second link, return true is returned, so SendBatch does not detect that this object is freed, and Use-After-Free occurs.

# Summary

P2PSocket(this) object is freed, causing Use-After-Free vulnerability

# Custom Questions

#### Type of crash:

Network Service

#### Crash state:

Access to this object that has been freed

#### Reporter credit:

jakebiles

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [asan](attachments/asan) (application/octet-stream, 21.2 KB)
- [diff](attachments/diff) (text/x-diff, 4.2 KB)
- [poc.html](attachments/poc.html) (text/html, 2.9 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-06-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5281347065020416.

### ca...@chromium.org (2025-06-26)

I was able to reproduce this on trunk with the provided patch. Triaging as high severity since it's memory corruption in the network service, but it can only be triggered with a compromised renderer. 
I wasn't able to bisect this since it requires a patch, but looking at the code nothing seems to have changed recently, so I'm tentatively assigning FoundIn to the current stable.


hta and sergeyu: Can you help further triage this (and reassign as appropriate)? Thanks

### ht...@google.com (2025-06-27)

This seems like a bizarre error report.
From the patch:

- DCHECK(state\_ == kStateOpen || state\_ == kStateError);
- if (state\_ == kStateOpen) {
- SendWithPacketId(address, data, options, unique\_id);
- }

- SendWithPacketId(address, data, options, unique\_id);

So in order to create an use-after-free, you have to remove a specific guard against calling this function in an inconsistent state?

I would like an explanation for why changing the code to create a vulnerability should be considered a vulnerability before investigating further.

### ja...@gmail.com (2025-06-27)

This vulnerability is a vulnerability that attacks the network process, which is an intermediate authority, after the renderer process exploit is complete.   

Therefore, modifying the renderer code to trigger the function running in the network process as above is a normal trigger method.

### ht...@google.com (2025-06-27)

Thank you for the explanation. So the patch is purely affecting the renderer, and is intended as a demonstration of what a compromised renderer could do in terms of Mojo calls to the network process, right?

### ch...@google.com (2025-06-27)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-06-27)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ht...@google.com (2025-06-30)

The design problem here seems to be that the P2PSocketTcpBase::DoSend() interface does not give any means of informing the caller that the P2PSocketTcpBase has been destroyed.

The destruction is not dispatched anywhere, so when DoSend() returns, the socket is already gone.
One redesign option is to make DoSend() have a bool return value indicating destruction.

Another option is to not destroy the socket immediately on error; this would make it easier to write code for, but needs a design that tells us when the socket is destroyed.

### ht...@google.com (2025-06-30)

I am trying to reproduce the error, but finding the right GN flags is taking its time.
Reporter: Can you add the args.gn file you were using to provoke the crash?

### ja...@gmail.com (2025-06-30)

```
is_asan = true
is_debug = false
is_component_build = false
enable_nacl = false
dcheck_always_on = false

```

### ht...@google.com (2025-06-30)

still having trouble. dcheck\_always\_on = false got me around the check on line 104, but I'm erroring out on the NOTREACHED on line 361. Which version did the POC work in?
The design problem is clear, however, so I may just make an unittest for it and let you verify that the POC doesn't POC after that.

### ja...@gmail.com (2025-06-30)

It was executed in commit 85ddf6764f4952cf60d36ae7adf61b7e621c3ac5.   

If you have restricted internet-related settings or are accessing a page that can access related functions, it seems that it will work normally if you turn it off and run it.

If the same error occurs with the above method, enter a value for `remote_address_` in the `P2PSocketTcpBase::Init` function according to the condition, and the error will not occur.

### ht...@google.com (2025-06-30)

That's 138.0.7163, May 5. Thank you.

### ht...@google.com (2025-06-30)

I now have an unit test that reproduces the symptom.
Without ASAN on, it crashes shortly afterwards at line 361 (the deallocated record doesn't have the right IP address in the right place), but with ASAN on, it reproduces as an UAF.
I'll get on with fix suggestion #1 (make DoSend() return a bool) tomorrow.

### dx...@google.com (2025-07-02)

Project: chromium/src  

Branch: main  

Author: Harald Alvestrand [hta@chromium.org](mailto:hta@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6694889>

Harden P2PSocketTcpBase::SendBatch against errors

---


Expand for full commit details
```
     
    This change ensures that even if errors occur that cause the socket 
    to be deleted during packet processing, SendBatch will terminate 
    correctly. 
     
    Bug: 427681143 
    Change-Id: I41da6789c8aab44b31c00c6a7844cd86b918561c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6694889 
    Reviewed-by: Sergey Ulanov <sergeyu@chromium.org> 
    Commit-Queue: Harald Alvestrand <hta@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1481925}

```

---

Files:

- M `services/network/p2p/socket_tcp.cc`
- M `services/network/p2p/socket_tcp.h`
- M `services/network/p2p/socket_tcp_unittest.cc`
- M `services/network/p2p/socket_test_utils.cc`
- M `services/network/p2p/socket_test_utils.h`

---

Hash: 0ccc849d2027de75122e5b187dc99bdf1cc24edf  

Date:  Wed Jul 2 22:15:22 2025


---

### ht...@google.com (2025-07-02)

Submitter, please check that the POC no longer POCs when possible.

### ch...@google.com (2025-07-03)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M138. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [138, 139].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ht...@google.com (2025-07-03)

Strange that it did not auto-detect the CL.

1: <https://chromium-review.googlesource.com/6694889> (from #16)

2: Landed in 140.0.7275.0 (July 3) - no reports so far.

3: Should not expose any new risks.

4: Should not have any compatibility risk.

5: No. Verification in browser requires a patched renderer process.

6: This is platform-independent code, so marking all OSes except iOS.

### ht...@chromium.org (2025-07-08)

It's been 5 days since I answered the questions, and this is still in "review". Is there a glitch in the automation?


### ja...@gmail.com (2025-07-09)

The patch seems to be correct.

### pg...@google.com (2025-07-09)

There is no glitch in the automation! the merge review process is manual and we had a staffing shortage! (:

This fix has been in canary for a while, and I do not see any relevant crashes

merge approved for M138 - please merge to branch 7204 by the end of the week to get this fix into the next respin!  

merge approved for M139 - please merge to branch 7258 by the end of the week to get this fix into the next beta release!

### ch...@google.com (2025-07-09)

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
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-07-09)

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
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ht...@chromium.org (2025-07-09)

Answers to #23 and #24 were given in #19.


### pg...@google.com (2025-07-09)

(Hm automation should definitely not be doing that when it has approved- tags on it - filing a bug for us to look into! please ignore comments 23/24)

### sr...@chromium.org (2025-07-09)

I have created the CP's to 138 and M139 and put them in CQ, please make sure they are good 

138 - https://chromium-review.googlesource.com/c/chromium/src/+/6719599
139 - https://chromium-review.googlesource.com/c/chromium/src/+/6720611


### dx...@google.com (2025-07-09)

Project: chromium/src  

Branch: refs/branch-heads/7258  

Author: Harald Alvestrand [hta@chromium.org](mailto:hta@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6720611>

Harden P2PSocketTcpBase::SendBatch against errors

---


Expand for full commit details
```
     
    This change ensures that even if errors occur that cause the socket 
    to be deleted during packet processing, SendBatch will terminate 
    correctly. 
     
    (cherry picked from commit 0ccc849d2027de75122e5b187dc99bdf1cc24edf) 
     
    Bug: 427681143 
    Change-Id: I41da6789c8aab44b31c00c6a7844cd86b918561c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6694889 
    Reviewed-by: Sergey Ulanov <sergeyu@chromium.org> 
    Commit-Queue: Harald Alvestrand <hta@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1481925} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6720611 
    Reviewed-by: Harald Alvestrand <hta@chromium.org> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7258@{#1023} 
    Cr-Branched-From: f600d0656fd5b5fe4a82981f533d31ed6939e2e4-refs/heads/main@{#1477651}

```

---

Files:

- M `services/network/p2p/socket_tcp.cc`
- M `services/network/p2p/socket_tcp.h`
- M `services/network/p2p/socket_tcp_unittest.cc`
- M `services/network/p2p/socket_test_utils.cc`
- M `services/network/p2p/socket_test_utils.h`

---

Hash: 05a400fbe69e3b845f119b6184a5663b7350379b  

Date:  Wed Jul 9 21:23:25 2025


---

### pe...@google.com (2025-07-09)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2025-07-09)

Project: chromium/src  

Branch: refs/branch-heads/7204  

Author: Harald Alvestrand [hta@chromium.org](mailto:hta@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6719599>

Harden P2PSocketTcpBase::SendBatch against errors

---


Expand for full commit details
```
     
    This change ensures that even if errors occur that cause the socket 
    to be deleted during packet processing, SendBatch will terminate 
    correctly. 
     
    (cherry picked from commit 0ccc849d2027de75122e5b187dc99bdf1cc24edf) 
     
    Bug: 427681143 
    Change-Id: I41da6789c8aab44b31c00c6a7844cd86b918561c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6694889 
    Reviewed-by: Sergey Ulanov <sergeyu@chromium.org> 
    Commit-Queue: Harald Alvestrand <hta@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1481925} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6719599 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Reviewed-by: Harald Alvestrand <hta@chromium.org> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#2011} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `services/network/p2p/socket_tcp.cc`
- M `services/network/p2p/socket_tcp.h`
- M `services/network/p2p/socket_tcp_unittest.cc`
- M `services/network/p2p/socket_test_utils.cc`
- M `services/network/p2p/socket_test_utils.h`

---

Hash: d897b04fba4cf1d1035eda267df1f14a29f4bc41  

Date:  Wed Jul 9 21:29:29 2025


---

### ht...@google.com (2025-07-09)

In reply to #29:

1. No. It is believed to be older. The feature that allowed this particular potential UAF was likely introduced by <https://chromium-review.googlesource.com/c/chromium/src/+/4480990> - this was merged to 115.0.5777.0
2. No.

### pe...@google.com (2025-07-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-07-11)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/6721044>
2. Medium - There were some conflicts in the unit tests.
3. 138 and 139
4. Yes. According to the [comment #31](https://issues.chromium.org/issues/427681143#comment31). The issue seems to exist from M115.

### sp...@google.com (2025-07-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
report of memory corruption in the network process, which is not sandboxed on all devices this issue was demonstrated to impact 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-07-21)

Congratulations! Thank you for your efforts and reporting this issue to us.

### dx...@google.com (2025-08-08)

Project: chromium/src  

Branch:  refs/branch-heads/6834  

Author:  Harald Alvestrand [hta@chromium.org](mailto:hta@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6721044>

[M132-LTS] Harden P2PSocketTcpBase::SendBatch against errors

---


Expand for full commit details
```
     
    This change ensures that even if errors occur that cause the socket 
    to be deleted during packet processing, SendBatch will terminate 
    correctly. 
     
    (cherry picked from commit 0ccc849d2027de75122e5b187dc99bdf1cc24edf) 
     
    Bug: 427681143 
    Change-Id: I41da6789c8aab44b31c00c6a7844cd86b918561c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6694889 
    Reviewed-by: Sergey Ulanov <sergeyu@chromium.org> 
    Commit-Queue: Harald Alvestrand <hta@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1481925} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6721044 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Harald Alvestrand <hta@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/6834@{#5618} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `services/network/p2p/socket_tcp.cc`
- M `services/network/p2p/socket_tcp.h`
- M `services/network/p2p/socket_tcp_unittest.cc`
- M `services/network/p2p/socket_test_utils.cc`
- M `services/network/p2p/socket_test_utils.h`

---

Hash: [0f600627b7f622c008a25adacf14ca7e4c69d690](http://crrev.com/0f600627b7f622c008a25adacf14ca7e4c69d690)  

Date: Fri Aug 8 10:10:04 2025


---

### ch...@google.com (2025-10-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/427681143)*
