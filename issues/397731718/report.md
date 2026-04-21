# Debug check failed: index < length_ (2200 vs. 2200).

| Field | Value |
|-------|-------|
| **Issue ID** | [397731718](https://issues.chromium.org/issues/397731718) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2025-02-20 |
| **Bounty** | $7,000.00 |

## Description

The issue 395329242 that we previously reported has been merged into issue 394644268.

However, even after applying the patch for issue 394644268 (https://chromium-review.googlesource.com/c/v8/v8/+/6236978),, the DCHECK can still be triggered in the latest d8 (#98715).

Therefore, we kindly request you to investigate this issue further.

## Timeline

### mp...@google.com (2025-02-20)

Assigning leszeks@ and CC'ing current v8 sheriff. Severity and FoundIn are provisional.

### le...@chromium.org (2025-02-20)

I cannot reproduce this:

```
$ git rev-parse HEAD
ee4c9aa22bc52de0df4a1d9c88c3c209473a528f

$ cat /tmp/test.js
try {
    d8.test.setFlushDenormals(true);
} catch (v11) {}
try {
    print((-1e-301).toString(2));
} catch (v13) {}

$ out/x64.debug/d8 /tmp/test.js
-0

```

### ki...@gmail.com (2025-02-20)

Still available at `d8-linux-debug-v8-component-98750`

```
$ cat /tmp/test.js           
try {
  d8.test.setFlushDenormals(true);
} catch (v11) {}
try {
  (-1e-301).toString(2);
} catch (v13) {}                                                                                                                                                                                   

$ /tmp/d8-linux-debug-v8-component-98750/d8 /tmp/test.js


#
# Fatal error in ../../src/base/vector.h, line 77
# Debug check failed: index < length_ (2200 vs. 2200).
#
#
#
#FailureMessage Object: 0x7ffe792af3e0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-98750/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7efc36263433]
    /tmp/d8-linux-debug-v8-component-98750/libv8_libplatform.so(+0x1b1bd) [0x7efc3620e1bd]
    /tmp/d8-linux-debug-v8-component-98750/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7efc36246914]
    /tmp/d8-linux-debug-v8-component-98750/libv8_libbase.so(+0x2b2d5) [0x7efc362462d5]
    /tmp/d8-linux-debug-v8-component-98750/libv8.so(v8::internal::DoubleToRadixStringView(double, int, v8::base::Vector<char>)+0x23d) [0x7efc3374e96d]
    /tmp/d8-linux-debug-v8-component-98750/libv8.so(+0x3f3b684) [0x7efc33f3b684]
    /tmp/d8-linux-debug-v8-component-98750/libv8.so(v8::internal::Runtime_DoubleToStringWithRadix(int, unsigned long*, v8::internal::Isolate*)+0x90) [0x7efc33f3b220]
    /tmp/d8-linux-debug-v8-component-98750/libv8.so(+0x22f283d) [0x7efc322f283d]
[1]    3421562 trace trap  /tmp/d8-linux-debug-v8-component-98750/d8 /tmp/test.js

```

### le...@chromium.org (2025-02-20)

can you share your gn args?

### le...@chromium.org (2025-02-20)

Ok, I can reproduce with a component build -- curious.

### ki...@gmail.com (2025-02-20)

Interesting. BTW the binary I used to reproduce came from `gs://v8-asan/linux-debug/d8-linux-debug-v8-component-98750.zip`.

### le...@chromium.org (2025-02-20)

So, it looks like this *is* the same issue, but the fix doesn't work in the component build (because the `delta > 0` check I introduced is getting optimized away by LLVM).

### ap...@google.com (2025-02-20)

Project: v8/v8  

Branch: main  

Author: Leszek Swirski <[leszeks@chromium.org](mailto:leszeks@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6286167>

[conversions] Check for denormal flushing in DoubleToRadixString

---


Expand for full commit details
```
[conversions] Check for denormal flushing in DoubleToRadixString 
 
Explicitly check the denormal flushing flag in DoubleToRadixString, to 
avoid the compiler optimizing away checks against zero. 
 
Bug: 382005099 
Fixed: 397731718 
Change-Id: If9298e68827bf2e5a1fd987b04b2536bf937a19f 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6286167 
Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98833}

```

---

Files:

- M `src/numbers/conversions.cc`

---

Hash: 00b8fba79ed2d14ec8e7fb1e2bcc38f3d59afaef  

Date:  Thu Feb 20 14:19:24 2025


---

### 24...@project.gserviceaccount.com (2025-02-20)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### ph...@google.com (2025-02-20)

Setting milestone because of s0/s1 severity.

### ph...@google.com (2025-02-20)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M133. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M134. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### 24...@project.gserviceaccount.com (2025-02-21)

ClusterFuzz testcase 4564776768176128 is verified as fixed in https://clusterfuzz.com/revisions?job=mac_asan_d8_dbg&range=98832:98833

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2025-02-21)

Merge review required: M134 is already shipping to beta.

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
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-02-21)

Merge review required: M133 is already shipping to stable.

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
Owners: andywu (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-02-21)

Merge review required: M132 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), alonbajayo (ChromeOS), srinivassista (Desktop)

### am...@chromium.org (2025-02-21)

This fix just landed yesterday, so we'll revisit this for merge review on Monday to M134 Stable RC being cut on Tuesday.

### ch...@google.com (2025-02-21)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### am...@chromium.org (2025-02-24)

<https://crrev.com/c/6286167> approved for merges; please merge this fix to 133 / 13.3 asap -- before 8am Pacific tomorrow (Monday) so this fix can be in the last respin of M133 Stable and M134 beta / 13.4 before 8am Pacific on Tuesday so this fix can be included in the M134 Stable RC

### le...@chromium.org (2025-02-24)

Preparing a merge to M134, we don't have the prerequisites from [crbug.com/382005099](https://crbug.com/382005099) in M133 to merge there. I don't think this is exploitable anyway, since afaict the OOB write will be because of an infinite loop.

### ap...@google.com (2025-02-24)

Project: v8/v8  

Branch: refs/branch-heads/13.4  

Author: Leszek Swirski <[leszeks@chromium.org](mailto:leszeks@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6299389>

Merged: [conversions] Check for denormal flushing in DoubleToRadixString

---


Expand for full commit details
```
Merged: [conversions] Check for denormal flushing in DoubleToRadixString 
 
Explicitly check the denormal flushing flag in DoubleToRadixString, to 
avoid the compiler optimizing away checks against zero. 
 
Bug: 382005099 
Fixed: 397731718 
(cherry picked from commit 00b8fba79ed2d14ec8e7fb1e2bcc38f3d59afaef) 
 
Change-Id: Ia83aa98f5cce7f5a02455043fc06144cf495a56d 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6299389 
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.4@{#27} 
Cr-Branched-From: 0f87a54dade4353b6ece1d7591ca8c66f90c1c93-refs/heads/13.4.114@{#1} 
Cr-Branched-From: 27af2e9363b2701abc5f3feb701b1dad7d1a9fe8-refs/heads/main@{#98459}

```

---

Files:

- M `src/numbers/conversions.cc`

---

Hash: b135b516afe6f7913826ce3821af6e744bdb41a8  

Date:  Thu Feb 20 14:19:24 2025


---

### pe...@google.com (2025-02-24)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ha...@google.com (2025-02-24)

Removing M133 approval per comment #20.

### go...@google.com (2025-02-24)

[Bulk Edit] 

Please merge your change to M134 by 10:00 AM PT tomorrow so we can take it in for this week's M134 Early Stable release.
 
If it is already merged,  please adjust the merge fields and bug status accordingly.

M134 branch details: https://chromiumdash.appspot.com/branches



### sp...@google.com (2025-02-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process / renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-27)

Congratulations! Thank you for your efforts and reporting this issue to us!

### qk...@google.com (2025-03-03)

Labelling as not applicable for LTS 132, because the suspected CL[1] isn't present in M132.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/6236978

### rz...@google.com (2025-03-04)

Labelling as not applicable for LTS 126 as well.

### ch...@google.com (2025-05-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### cl...@chromium.org (2025-07-07)

Re [comment #20](https://issues.chromium.org/issues/397731718#comment20): Is S1 actually accurate here? If this is not exploitable, should we treat it as denial of service instead and convert to a bug?

## Bounty Award

> report of memory corruption in a sandboxed process / renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/397731718)*
