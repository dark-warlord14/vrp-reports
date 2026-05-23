# Security: Refcount overflow in RefCountedThreadSafeBase

| Field | Value |
|-------|-------|
| **Issue ID** | [40056849](https://issues.chromium.org/issues/40056849) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Core |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | so...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2021-08-11 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

In the function "RefCountedThreadSafeBase::AddRefImpl":

"""  

ALWAYS\_INLINE void AddRefImpl() const {  

#if DCHECK\_IS\_ON()  

DCHECK(!in\_dtor\_);  

DCHECK(!needs\_adopt\_ref\_)  

<< "This RefCounted object is created with non-zero reference count."  

<< " The first reference to such a object has to be made by AdoptRef or"  

<< " MakeRefCounted.";  

#endif  

ref\_count\_.Increment();  

}  

"""

It lacks a checking about overflow here. On the other hand, the ref\_count is "atomic\_int", in 64bit system, we can overflow it as we have enough memory space.

We should add a checking about overflow like "RefCountedBase::AddRefImpl()":

"""  

void RefCountedBase::AddRefImpl() const {  

// An attacker could induce use-after-free bugs, and potentially exploit them,  

// by creating so many references to a ref-counted object that the reference  

// count overflows. On 32-bit architectures, there is not enough address space  

// to succeed. But on 64-bit architectures, it might indeed be possible.  

// Therefore, we can elide the check for arithmetic overflow on 32-bit, but we  

// must check on 64-bit.  

//  

// Make sure the addition didn't wrap back around to 0. This form of check  

// works because we assert that `ref_count_` is an unsigned integer type.  

CHECK(++ref\_count\_ != 0);  

}  

"""

SequencedTaskRunner inherits from RefCountedThreadSafeBase, we can add one refcount of SequencedTaskRunner when we bind a pending receiver/remote from renderer process. If the attacker compromised renderer process, it is easy to overflow the refcount of SequencedTaskRunner through binding many receivers. This will lead to use after free when the refcount wrap back around to 0. This is just one of the attack method, there are many classes inherits RefCountedThreadSafeBase so must be exist many other attack methods.

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: SorryMybad(@S0rryMybad) of Kunlun Lab

## Timeline

### [Deleted User] (2021-08-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-11)

Thanks for your report. It seems we do have this check in AddRefWithCheckImpl() but perhaps this was not added everywhere for binary size restrictions.

I think perhaps dcheng or tzik can comment on exactly why this ended up the way it is.

[Monorail components: Internals>Core]

### so...@gmail.com (2021-08-12)

Re https://crbug.com/chromium/1238642#c2:

1. At least the SequencedTaskRunner does NOT use the function AddRefWithCheckImpl so it can be overflow and it used in many code which can reach directly from renderer process.

2. Feels a bit confuse about Security_Severity-Low, there is a similar issue here:https://bugs.chromium.org/p/chromium/issues/detail?id=925864 which assign High.

### [Deleted User] (2021-08-12)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dc...@chromium.org (2021-08-13)

The severity is likely because there's no concrete bug that takes advantage of this (yet).

As for why we don't have the check, I suspect it has to do with the fact that we branch based on whether or not the refcount starts at 0 (for legacy stuff) or 1 (preferred but many things not migrated). However, interestingly enough, I think the CHECK() enforces by RefCounted actually enforces a different precondition than the CHECK() enforced by RefCountedThreadSafe.

The RefCounted CHECK is:

  CHECK(++ref_count_ != 0);

Which prevents wraparound but does *not* prevent zombie objects.

The RefCountedThreadSafe CHECK (for objects that have been updated to start at refcount 1) is:

  CHECK(ref_count_.Increment() > 0);

Increment() returns the 'prevoius' value, so this CHECK is enforcing that an object's refcount does not go from zero to one, which would indicate that an already-deleted object has its refcount bumped back up.

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### dc...@chromium.org (2021-08-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f2a78f3b4317331ff75bf844c25595e080a76695

commit f2a78f3b4317331ff75bf844c25595e080a76695
Author: Daniel Cheng <dcheng@chromium.org>
Date: Fri Nov 11 02:05:03 2022

Use helper for declaring refcount type rather than using base::subtle directly.

Implementation details of base::subtle are subject to change; non-base
code should not be using it directly.

Bug: 1238642
Change-Id: Ic47c40ced7a743594515a06f1be103cd7b3acb37
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4020813
Commit-Queue: Klaus Weidner <klausw@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Auto-Submit: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Klaus Weidner <klausw@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1070122}

[modify] https://crrev.com/f2a78f3b4317331ff75bf844c25595e080a76695/content/browser/xr/service/xr_runtime_manager_impl.h


### dc...@chromium.org (2022-11-15)

mpdenton points out that simply CHECK()ing on overflow has a theoretical race, where another thread could increment and decrement the refcount to trigger a UaF. I think this is something we are willing to live with for now.

We could try to mitigate against this by being more fancy; load the pre-increment value and check if it's already the max refcount, and CHECK if it is or compare-and-swap if it isn't. I feel like that would have a bigger perf impact than an atomic increment though.

(Also, sorry for the long delay in landing a patch here; I had a CL prepared a year ago but it ended up bouncing off the CQ since I tried to simultaneously fix IWYU errors. That's what I get for trying to clean up things...)

### gi...@appspot.gserviceaccount.com (2022-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5c8cdc936817c97618e21b656c6bafb7cfd7dea1

commit 5c8cdc936817c97618e21b656c6bafb7cfd7dea1
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Nov 15 08:14:11 2022

[base] Protect thread-safe refcounts against overflow.

Implementing tests for this also tickled a surprising edge case in the
way RefCounted/RefCountedThreadSafe signalled whether the refcount
should begin at 0 or 1. Previously, this was signalled using a static
data member; however, local classes (which the updated tests use) cannot
contain static data members.

As a result, this CL "minimally" updates the tagging mechanism to use a
type alias while leaving as much of the existing tagging mechanism
intact as possible.

Bug: 1238642
Change-Id: I16f3ab243745e11bbde755f826d430e85cc33a93
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3131643
Reviewed-by: Lei Zhang <thestig@chromium.org>
Owners-Override: Lei Zhang <thestig@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1071489}

[modify] https://crrev.com/5c8cdc936817c97618e21b656c6bafb7cfd7dea1/base/atomic_ref_count.h
[modify] https://crrev.com/5c8cdc936817c97618e21b656c6bafb7cfd7dea1/gpu/command_buffer/service/dxgi_shared_handle_manager.cc
[modify] https://crrev.com/5c8cdc936817c97618e21b656c6bafb7cfd7dea1/base/memory/ref_counted.h
[modify] https://crrev.com/5c8cdc936817c97618e21b656c6bafb7cfd7dea1/base/memory/ref_counted_delete_on_sequence.h
[modify] https://crrev.com/5c8cdc936817c97618e21b656c6bafb7cfd7dea1/base/memory/ref_counted_unittest.cc
[modify] https://crrev.com/5c8cdc936817c97618e21b656c6bafb7cfd7dea1/base/memory/scoped_refptr.h


### dc...@chromium.org (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-15)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Thank you for this report! The VRP Panel has decided to award you $1,000 reward to thank you for this report so we could make a security relevant change. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-02-21)

This issue was migrated from crbug.com/chromium/1238642?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056849)*
