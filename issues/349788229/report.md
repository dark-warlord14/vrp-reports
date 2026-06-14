# Fatal error in ../../src/heap/mark-compact.cc, line 3665

| Field | Value |
|-------|-------|
| **Issue ID** | [349788229](https://issues.chromium.org/issues/349788229) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>GarbageCollection |
| **Platforms** | Linux |
| **Reporter** | da...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2024-06-27 |
| **Bounty** | $7,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
Please provide a brief explanation of the security issue.

The weak reference in the GC is located in a read-only region.

commit 5659831: [heap] Simplify condition for weakref triviality check | https://chromium-review.googlesource.com/c/v8/v8/+/5659831's modification to src/heap/mark-compact.cc appears to be causing the issue.

Unfortunately, I didn't include the symbols in the original backtrace of this issue, so I'll list the symbols below that I checked manually.

v8/src/heap/heap.cc, L:2360
v8/src/heap/heap.cc, L:2715
v8/src/heap/mark-compact.cc, L:444
v8/src/heap/mark-compact.cc, L:2945
v8/src/heap/mark-compact.cc, L:3665

VERSION
Chrome Version: V8 main branch, Since commit 5659831 ([heap] Simplify condition for weakref triviality check
)
Operating System: Ubuntu 22.04 LTS

REPRODUCTION CASE
Please include a demonstration of the security bug, such as an attached HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE make the file as small as possible and remove any content not required to demonstrate the bug, or any personal or confidential information.

./d8 --expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --harmony --js-staging ./mark-compact.cc_L3665_DCHECK_Fail_PoC.js

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: Debug check failed: !InReadOnlySpace(value).
Crash State: [see link above: stack trace *with symbols*, registers, exception record]

// CRASH INFO
// ==========
// INSTANCE TAG: e855c14c
// TERMSIG: 6
// STDERR:
// #
// # Fatal error in ../../src/heap/mark-compact.cc, line 3665
// # Debug check failed: !InReadOnlySpace(value).
// #
// #
// #
// #FailureMessage Object: 0x7d9b5c65dc60
// ==== C stack trace ===============================
// 
//     ../v8/out/fuzzbuild/d8(___interceptor_backtrace+0x46) [0x5cb9123318c6]
//     ../v8/out/fuzzbuild/d8(v8::base::debug::StackTrace::StackTrace()+0x22) [0x5cb91275ff32]
//     ../v8/out/fuzzbuild/d8(+0x6138747) [0x5cb912758747]
//     ../v8/out/fuzzbuild/d8(V8_Fatal(char const*, int, char const*, ...)+0x346) [0x5cb91272ef8e]
//     ../v8/out/fuzzbuild/d8(+0x610d9ec) [0x5cb91272d9ec]
//     ../v8/out/fuzzbuild/d8(v8::internal::MarkCompactCollector::ClearNonTrivialWeakReferences()+0x9af) [0x5cb91400830f]
//     ../v8/out/fuzzbuild/d8(v8::internal::MarkCompactCollector::ClearNonLiveReferences()+0x47b2) [0x5cb913fd3fe2]
//     ../v8/out/fuzzbuild/d8(v8::internal::MarkCompactCollector::CollectGarbage()+0x8b) [0x5cb913fca4cb]
//     ../v8/out/fuzzbuild/d8(v8::internal::Heap::MarkCompact()+0x292) [0x5cb913c75e22]
//     ../v8/out/fuzzbuild/d8(v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*)+0x12c4) [0x5cb913c73124]
//     ../v8/out/fuzzbuild/d8(+0x771f155) [0x5cb913d3f155]
//     ../v8/out/fuzzbuild/d8(+0x771e60c) [0x5cb913d3e60c]
//     ../v8/out/fuzzbuild/d8(+0xbdc28f3) [0x5cb9183e28f3]
// Received signal 6

Client ID (if relevant): commit 5659831 ~ Now

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: If this is confirmed as valid and a condition of receiving the reward, I would like to claim it, but I don't know how to do so at this time.

## Attachments

- [mark-compact.cc_L3665_DCHECK_Fail_PoC.js](attachments/mark-compact.cc_L3665_DCHECK_Fail_PoC.js) (text/javascript, 2.8 KB)
- [gn.args](attachments/gn.args) (application/octet-stream, 602 B)

## Timeline

### el...@chromium.org (2024-06-27)

Security shepherd: thanks for the report. This does not repro for me using v8 @ 72d3347be0e342007f841604ea98dd622f0210ed. Which v8 revision are you testing at? Also, what are your v8 build flags?

### da...@gmail.com (2024-06-27)

I missed mentioning some additions to the original report.

The modified Fuzzilli that works locally for me reports this as flaky.

I also note that this issue is reproduced well with 72d3347be0e342007f841604ea98dd622f0210ed, and I suspect that the reason you're having trouble reproducing it is because it requires some additions to gn.args.

I'm attaching the gn.args I used to detect this issue.

### pe...@google.com (2024-06-27)

Thank you for providing more feedback. Adding the requester to the CC list.

### ah...@google.com (2024-07-01)

[primary security shepherd]
Please note that the previous shepherd wasn't able to repro. I didn't try to repro with the provided gn args
Setting a provisional severity of High (S1)
Setting a provisional Found In of the current Extended Stable.
Assigning it to the current V8 shepherd: ishell@google.com


### pe...@google.com (2024-07-01)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-01)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### is...@chromium.org (2024-07-02)

Thank you for the report! I reproduced the issue.

### is...@chromium.org (2024-07-02)

[This DCHECK](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/mark-compact.cc;l=3665?q=%22DCHECK(!InReadOnlySpace(value));%22&ss=chromium) fails because the value is the `UndefinedMap` read-only root.

### da...@gmail.com (2024-07-03)

I have a few questions

1. before I report any issue, is there any way I can verify that the report of the issue I've identified is not an already reported issue? 
Obviously, there were no similar reported issues at the time I created the report, including this one, but I've experienced a few times where the status changed to duplicate out of the blue like this one. If you know of any, I'd be very grateful to know.

2. is there any way to see the original issue that was reported before my report (in this case 350256147)? 

3. is there any way to access ClusterFuzz.com?


### is...@chromium.org (2024-07-03)

Yes, this was reported before the [issue 350256147](https://issues.chromium.org/issues/350256147). amyressler@, could you please comment?

### da...@gmail.com (2024-07-03)

If the tone of my comment seems a bit out of context, it's probably because I'm making some errors as a non-English speaker... 

I just don't like to be redundant in reporting any issues. 

In the case of this report, I didn't see any existing reports in the 'seamiller issue', but it was a duplicate of issue 350256147, so I'd like to know if there's some way I can check if the issue I'm reporting is a duplicate before I report it.

### ni...@chromium.org (2024-07-03)

I merged the two issues and kept [issue 350256147](https://issues.chromium.org/issues/350256147) open because I thought it is more general, in the sense that it contains repros for two different failing `DCHECK`s.  

The first is what is also reported here.  

Both were caused by my CLs (<https://crrev.com/c/5648710> and <https://crrev.com/c/+/5659831>).

I'm afraid I didn't think too much about the originality of the reports, when I merged the issues.  

From the point of view of doing my work (i.e., fixing the possible vulnerability), merging them in this way seemed to be the right thing to do.  

I apologise, if by doing so I did an injustice.
If that is the case, I am sure that the security team will resolve this fairly.

### am...@chromium.org (2024-07-03)

re: comment #10 and comment #12 

Hi, no worries about tone. We understand that a lot of folks are English as a first language speakers. But appreciate you clarifying. 

> 1. before I report any issue, is there any way I can verify that the report of the issue I've identified is not an already reported issue?
You can check the tracker for similar disclosed similar issues -- fixed past security vulnerabilities and open by default functional issues. 
Unfortunately, if the issue is a security issue and was recently discovered and is not resolved or yet publicly disclosed, it will be restricted (as an open vulnerability should be) and it won't come up in your queries. 

A protip here is that if you discovered the issue from your own fuzzing and there are past resolved issues that were fuzzer / clusterfuzz discovered, you should expect that your report will collide as a duplicate with either a clusterfuzz report or a report of another person running their own fuzilli based fuzzer. 

> Obviously, there were no similar reported issues at the time I created the report, including this one, but I've experienced a few times where the status changed to duplicate out of the blue like this one. If you know of any, I'd be very grateful to know.
It's not really out of the blue. While you may believe you report to be the first instance of a bug, an earlier version of that issue may not have been triaged just yet and identified as the same issue. 
With V8 issues, lot of researchers are running fuzzers and there have been instances of 6-8 reports for the same issue from different sources within a few hours of each other. 


>2. is there any way to see the original issue that was reported before my report (in this case 350256147)? 
Unfortunately no, due to privacy reasons, we cannot cc: other reporters to duplicate reports from other sources. 
You'll have access to that report when is publicly disclosed. 

> 3. is there any way to access ClusterFuzz.com?
Not at this time. We are working toward providing external researchers the capability to upload your testcases directly to clusterfuzz, but that is still a work in progress. 
There will be an announcement once that is launched. 

ALL this being said, however, your report was reported earlier than crbug.com/350256147 and this was merged in the incorrect direction. 
I am going to open this issue as in-progress as being blocked on issue 350256147 so this can be corrected since there is a fix that is already associated with the other report. 


### pe...@google.com (2024-07-04)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### ni...@chromium.org (2024-07-04)

I had marked this issue as a duplicate of [issue 350256147](https://issues.chromium.org/issues/350256147) and closed it.  

It was later reopened (comment 14) for reasons unrelated to the process of fixing the possible vulnerability.  

[The fix](https://crrev.com/c/5676327) was associated with [issue 350256147](https://issues.chromium.org/issues/350256147) and both issues were closed as fixed.

The issue was caused by <https://crrev.com/c/5648710> and <https://crrev.com/c/+/5659831>.  

The former landed in 128.0.6561.0.  

There has been no branch cut since then.  

The fix landed last night and has not yet appeared in a release.

Based on the above, I don't think there is any need for backmerging in any channel.

### sp...@google.com (2024-07-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-17)

Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-10-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/349788229)*
