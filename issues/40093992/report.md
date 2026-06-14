# Code review: ReadBits may return uninitialized value due to unchecked return status.

| Field | Value |
|-------|-------|
| **Issue ID** | [40093992](https://issues.chromium.org/issues/40093992) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Media |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ad...@microsoft.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2019-02-08 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134

Steps to reproduce the problem:
Found through code review, no repro steps provided. Instead there's an analysis and a proposed fix.

What is the expected behavior?
ReadBits core library internal api's can fail returning uninitialized memory. The apis are used for ~20 different locations doing media processing (mpeg, mp4, mp2t, ac3, vp9). Depending on the usage it's possible the memory leak goes over IPC from the GPU process into the renderer as well.

What went wrong?
Several issues happening at the same time: not checking return values and not initializing stack variables. In this case the combination of both can lead to using/leaking uninitialized memory via the generic read bit_reader_core functionality.

%SDXROOT%\media\base\container_names.cc
static uint64_t ReadBits(BitReader* reader, int num_bits) {
  DCHECK_GE(reader->bits_available(), num_bits);
  DCHECK((num_bits > 0) && (num_bits <= 64));
  uint64_t value;<--------- uninitialized 
  reader->ReadBits(num_bits, &value); <- not checking the return value of ReadBits
  return value; <----- returning value (may be uninitialized)
}

Following the code downstream it goes into 
%SDXROOT%\media\base\bit_reader_core.h
 template<typename T> bool ReadBits(int num_bits, T* out) {
    DCHECK_LE(num_bits, static_cast<int>(sizeof(T) * 8));
    uint64_t temp; <-------- Uninitialized 
    bool ret = ReadBitsInternal(num_bits, &temp); <- may fail returning ret ==false 
    *out = static_cast<T>(temp); <-------- temp may be uninitialized, copied to *out
    return ret; <-------- may return false but the caller doesn't validate
  }

Lastly we make it to ReadBitsInternal.
%SDXROOT%\media\base\bit_reader_core.cc
bool BitReaderCore::ReadBitsInternal(int num_bits, uint64_t* out) {
...
if (num_bits > nbits_ && !Refill(num_bits)) {
    // Any subsequent ReadBits should fail:
    // empty the current bit register for that purpose.
    nbits_ = 0;
    reg_ = 0;
    return false; <--- issue happens here, out is uninitialized, returning false, the rest of the chain doesn't check the return value
  }
...
}

Proposed fix:
1. container_names.cc ReadBits <- should check return value, return 0 on failure
2. bit_reader_core.h ReadBits <- should initialize temp, should check the return value of ReadBitsInternal before copying to *out
3. ReadBitsInternal could set *out to 0 on failure, but the first 2 fixes would make this a defense in depth only

Did this work before? No 

Chrome version: 64.0.3282.140  Channel: n/a
OS Version: 10.0
Flash Version: 

Please reach out if you need additional details.
Thanks, 
 Adrian

## Timeline

### ad...@microsoft.com (2019-02-08)

%SDXROOT% = location of GitHub clone of https://github.com/chromium/chromium/blob/master/ 

e.g. %SDXROOT%\media\base\container_names.cc == https://github.com/chromium/chromium/blob/master/media/base/container_names.cc

### do...@chromium.org (2019-02-08)

Thanks for the report. Looks to me like this code hasn't changed since 2014.

+media OWNERs, do you mind following up here?

[Monorail components: Internals>Media]

### sh...@chromium.org (2019-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-08)

[Empty comment from Monorail migration]

### ch...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/929f77d4173022a731ae91218ce6894d20f87f35

commit 929f77d4173022a731ae91218ce6894d20f87f35
Author: Chris Cunningham <chcunningham@chromium.org>
Date: Sat Feb 23 00:30:57 2019

Cleanup media BitReader ReadBits() calls

Initialize temporary values, check return values.
Small tweaks to solution proposed by adtolbar@microsoft.com.

Bug: 929962
Change-Id: Iaa7da7534174882d040ec7e4c353ba5cd0da5735
Reviewed-on: https://chromium-review.googlesource.com/c/1481085
Commit-Queue: Chrome Cunningham <chcunningham@chromium.org>
Reviewed-by: Dan Sanders <sandersd@chromium.org>
Cr-Commit-Position: refs/heads/master@{#634889}
[modify] https://crrev.com/929f77d4173022a731ae91218ce6894d20f87f35/media/base/bit_reader_core.cc
[modify] https://crrev.com/929f77d4173022a731ae91218ce6894d20f87f35/media/base/bit_reader_core.h
[modify] https://crrev.com/929f77d4173022a731ae91218ce6894d20f87f35/media/base/container_names.cc


### ch...@chromium.org (2019-02-23)

[Empty comment from Monorail migration]

### ch...@chromium.org (2019-02-23)

(Doesn't need verification)

### sh...@chromium.org (2019-02-23)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-25)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-28)

Congrats! The Panel decided to reward $500 for this report :) 

### na...@google.com (2019-02-28)

Please let me know how you would like to be credited in our release notes for your contributions. 

### ad...@microsoft.com (2019-02-28)

Hey,

Please credit me as Adrian Tolbaru (adtolbar@microsoft.com).
For the reward i'd like to donate it to charity, if possible to http://www.shadowlandfoundation.org

Thanks,
 Adrian 

### aw...@google.com (2019-03-05)

[Empty comment from Monorail migration]

### aw...@google.com (2019-03-07)

[Comment Deleted]

### aw...@google.com (2019-03-07)

[Comment Deleted]

### sh...@chromium.org (2019-03-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-03-23)

+adetaylor@ & awhalley@, not sure why sheriffbot is requesting merge for this. We saw similar issue with previous milestones too.



CL listed at #6 landed way before M74 branch #3729 on March 7th at chromium revision 638880.

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/929962?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093992)*
