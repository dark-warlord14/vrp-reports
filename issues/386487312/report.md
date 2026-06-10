# Debug check failed: position() + n <= buffer_.length() in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [386487312](https://issues.chromium.org/issues/386487312) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | pt...@chromium.org |
| **Created** | 2024-12-29 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 97879
    - link: https://crrev.com/02c8d9c11009c3b9b510fdc599e7e2115fc88b00
- Commit Message

```
commit 02c8d9c11009c3b9b510fdc599e7e2115fc88b00
Author: pthier <pthier@chromium.org>
Date:   Thu Dec 19 13:00:10 2024 +0100

    [conversions] Return std::string_view from *ToCString methods
    
    Previously, DoubleToCString, IntToCString, DoubleToFixedCString,
    DoubleToExponentialCString, DoubleToPrecisionCString and
    DoubleToRadixCString returned a 0-terminated C-String.
    However most users of these methods copy the C-String again (e.g. into
    a V8 Heap object), thus requiring another strlen() call to retrieve the
    length, that is already known within these methods.
    
    Therefore this CL changes the following:
    - *ToCString methods return a std::string_view (not 0-terminated)
      instead of a 0-terminated C-String.
    - The caller provides the required buffer to store the result.
      Previously the methods created a malloced buffer and transferred
      ownership to the caller. By requiring the caller to provide the
      buffer (1) ownership is clear and (2) the buffer can be stack
      allocated.
    - Rename *ToCString to *ToStringView to reflect the changed semantics.
    
    Bug: 380044242, 377438310
    Change-Id: If7b44d0dc8ff8551d4aaeac01f5d20e1528a9c3f
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6105411
    Commit-Queue: Patrick Thier <pthier@chromium.org>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#97879}
```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-97925/d8 poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/numbers/conversions.cc, line 96
# Debug check failed: position() + n <= buffer_.length() (108 vs. 107).
#
#
#
#FailureMessage Object: 0x7ffccf570d00
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-97925/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f04ba7f53e3]
    /tmp/d8-linux-debug-v8-component-97925/libv8_libplatform.so(+0x1ae6d) [0x7f04ba79de6d]
    /tmp/d8-linux-debug-v8-component-97925/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7f04ba7d65c4]
    /tmp/d8-linux-debug-v8-component-97925/libv8_libbase.so(+0x2bfd5) [0x7f04ba7d5fd5]
    /tmp/d8-linux-debug-v8-component-97925/libv8.so(v8::internal::SimpleStringBuilder::AddSubstring(char const*, int)+0x200) [0x7f04bdd41530]
    /tmp/d8-linux-debug-v8-component-97925/libv8.so(v8::internal::DoubleToPrecisionStringView(double, int, v8::base::Vector<char>)+0x502) [0x7f04bdd42912]
    /tmp/d8-linux-debug-v8-component-97925/libv8.so(+0x2c1cd4f) [0x7f04bd41cd4f]
    /tmp/d8-linux-debug-v8-component-97925/libv8.so(v8::internal::Builtin_NumberPrototypeToPrecision(int, unsigned long*, v8::internal::Isolate*)+0x7d) [0x7f04bd41c2dd]
    /tmp/d8-linux-debug-v8-component-97925/libv8.so(+0x218647d) [0x7f04bc98647d]
```

VERSION
Tested on v8 version: 13.3.0 - 13.3.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-97925.zip
2. Run: d8  poc.js

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy) and Nan Wang (@eternalsakura13)



## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 32 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-12-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5388912541237248.

### am...@chromium.org (2024-12-30)

Thanks for the report. I've gone ahead and uploaded this to clusterfuzz to confirm if will repro or not, because I'm fairly certain this is a duplicate of an issue that was resolved on 23 December.

### am...@chromium.org (2024-12-30)

it looks like this does still reproduced and this particular dcheck failure wasn't resolved as of yet; will triage accordingly

### 24...@project.gserviceaccount.com (2024-12-30)

Detailed Report: https://clusterfuzz.com/testcase?key=5388912541237248

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  position() + n <= buffer_.length() in conversions.cc
  v8::internal::SimpleStringBuilder::AddSubstring
  v8::internal::DoubleToPrecisionStringView
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=97878:97879

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5388912541237248

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### pe...@google.com (2024-12-31)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-12-31)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ap...@google.com (2025-01-09)

Project: v8/v8  

Branch: main  

Author: pthier <[pthier@chromium.org](mailto:pthier@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6162974>

[conversions] Fix toPrecision buffer length

---


Expand for full commit details
```
[conversions] Fix toPrecision buffer length 
 
Fixed: 386487312 
Change-Id: I1247cafb0c27d2a1ea80c5c52e32926b07740ab4 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6162974 
Auto-Submit: Patrick Thier <pthier@chromium.org> 
Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98021}

```

---

Files:

- M `src/numbers/conversions.cc`
- M `src/numbers/conversions.h`
- A `test/mjsunit/regress/regress-386487312.js`

---

Hash: 245b6b0bc26657060a3055171c83789bd902be90  

Date:  Thu Jan 09 12:00:31 2025


---

### pe...@google.com (2025-01-09)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M133. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pt...@chromium.org (2025-01-09)

Answers to [comment #9](https://issues.chromium.org/issues/386487312#comment9):

> Which CLs should be backmerged? (Please include Gerrit links.)

<https://crrev.com/c/6162974>

> Has this fix been verified on Canary to not pose any stability regressions?

Not yet. I will wait until January 14th for the backmerge to give it time on canary, but before beta promotion.

> Does this fix pose any potential non-verifiable stability risks?

No.

> Does this fix pose any known compatibility risks?

No.

> Does it require manual verification by the test team? If so, please describe required testing.

No.

### 24...@project.gserviceaccount.com (2025-01-10)

ClusterFuzz testcase 5388912541237248 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=98020:98021

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2025-01-10)

**Merge approved:** your change passed merge requirements and is auto-approved for M133. Please go ahead and merge the CL to branch 6943 (refs/branch-heads/6943) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: None (Android), None (iOS), andywu (ChromeOS), None (Desktop)

### pb...@google.com (2025-01-10)

Your change has been approved to M133 branch, Please goahead and get the CL merged asap so that it would be part of next week M133 Beta promotion.

### ap...@google.com (2025-01-14)

Project: v8/v8  

Branch: refs/branch-heads/13.3  

Author: pthier <[pthier@chromium.org](mailto:pthier@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6172041>

Merged: [conversions] Fix toPrecision buffer length

---


Expand for full commit details
```
Merged: [conversions] Fix toPrecision buffer length 
 
Fixed: 386487312 
 
(cherry picked from commit 245b6b0bc26657060a3055171c83789bd902be90) 
 
Change-Id: I57d68c0da7524941bac31b7f79e2d3d442697a27 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6172041 
Commit-Queue: Patrick Thier <pthier@chromium.org> 
Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
Auto-Submit: Patrick Thier <pthier@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.3@{#14} 
Cr-Branched-From: 41dacffe436aeb9311879cb07648f1e36609a804-refs/heads/13.3.415@{#1} 
Cr-Branched-From: 3348638c0af67c885b30891a358c89a917ac9759-refs/heads/main@{#97937}

```

---

Files:

- M `src/numbers/conversions.cc`
- M `src/numbers/conversions.h`
- A `test/mjsunit/regress/regress-386487312.js`

---

Hash: 64efbc99faa1295771c69b30b33c7abea51f565e  

Date:  Thu Jan 09 12:00:31 2025


---

### pe...@google.com (2025-01-14)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pt...@chromium.org (2025-01-14)

> 1. Was this issue a regression for the milestone it was found in?

Yes

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

Yes, the original change was in M133.

### pe...@google.com (2025-01-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### qk...@google.com (2025-01-16)

Labeling as LTS-NotApplicable-126 because this bug was introduced on Dec 19 2024. So M126 doesn't have the suspected CL[1].

[1] https://chromium-review.googlesource.com/c/v8/v8/+/6105411

### pe...@google.com (2025-01-17)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pt...@chromium.org (2025-01-17)

Doesn't need to be merged to M132

> Was this issue a regression for the milestone it was found in?

Yes

> Is this issue related to a change or feature merged after the latest LTS Milestone?

Yes, the original change was in M133.

### sp...@google.com (2025-01-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process / renderer + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-17)

Thank you Zhenghang and Sakura for reporting this issue to us.

### rz...@google.com (2025-01-29)

Labelling as not applicable for LTS 132 as well, the suspected CL ([comment #18](https://issues.chromium.org/issues/386487312#comment18)) isn't present in 132.

### ch...@google.com (2025-04-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/386487312)*
