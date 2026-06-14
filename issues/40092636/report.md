# Security: crosvm: integer overflow in PluginVcpu::handle_request

| Field | Value |
|-------|-------|
| **Issue ID** | [40092636](https://issues.chromium.org/issues/40092636) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P4 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | al...@gmail.com |
| **Assignee** | za...@chromium.org |
| **Created** | 2018-10-06 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

<https://chromium.googlesource.com/chromiumos/platform/crosvm/+/master/src/plugin/vcpu.rs#468>

the addition and multiplication here can overflow. when they do, |vec| will be smaller than was expected.

However, this memory will then, unsafely be treated as if there was enough space for |request\_entries.len()| elements:

<https://chromium.googlesource.com/chromiumos/platform/crosvm/+/master/src/plugin/vcpu.rs#480>

This results in a heap-buffer-overflow WRITE.

I note that I don't fully understand the context this is running in, it's not clear to me if this is crosvm handling messages from the kernel (which is a higher privileged level, and thus there's no security impact) or from the guest, in which case this would be a potential VM guest->host escape.

**VERSION**  

Chrome Version: Found on master, haven't checked if this affects release.  

Operating System: Chrome OS

**REPRODUCTION CASE**  

No test case, found by code review.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Alex Gaynor

FIX:

The correct fix is to replace:

size\_of::<kvm\_msrs>() + (request\_entries.len() \* size\_of::<kvm\_msr\_entry>())

With:

size\_of::<kvm\_msrs>().checked\_add(  

request\_entries.len().checked\_mul(size\_of::<kvm\_msr\_entry>()).ok\_or\_else(|| Err(SysError::new(EINVAL)))?  

).ok\_or\_else(|| Err(SysError::new(EINVAL)))?

Would it be helpful for me to upload a patch?

## Timeline

### al...@gmail.com (2018-10-06)

A quick grep for |vec_size_bytes| suggests that this pattern repeats itself in quite a few places. I have not analyzed which of these are potential vulnerabilities.

### me...@chromium.org (2018-10-08)

Thanks for the report, passing over to ChromeOS folks.

### jo...@chromium.org (2018-10-08)

Over to Zach and Dylan for triage. Notice c#1, we should probably check all those additions and multiplications.

Marking Sev-High until we figure out where this is used. A guest escape would be Sev-Critical.

[Monorail components: OS>Systems]

### za...@chromium.org (2018-10-08)

I have doubts that it is possible to have a large enough request_entries.len(). That vec is part of a protobuf that limited to MAX_VCPU_DATAGRAM_SIZE (256k bytes): https://chromium.googlesource.com/chromiumos/platform/crosvm/+/master/src/plugin/vcpu.rs#404

It's implausible that a protobuf of that size would have an array length large enough to trigger overflow when multiplied by sizeof(kvm_msr_entry) (16 bytes).

### jo...@chromium.org (2018-10-08)

At the same time, it would be great to not have to worry about these things in Rust/crosvm code -- that's kind of why we chose Rust in the first place.

### sh...@chromium.org (2018-10-09)

[Empty comment from Monorail migration]

### al...@gmail.com (2018-10-13)

Given the length constraint, I don't believe any of these are exploitable. (You can potentially get larger allocations than the input buffer due to protobuf's variable width encoding, but even accounting for that I don't think you can trigger an overflow).

It looks like this code was largely re-organized into a |vec_with_array_field| function. It'd probably be good to add overflow checking there as it could easily end up being used in a context where the argument isn't bounded in some fashion.

Not sure how y'all handle unexploitable-but-dangerous code.

### za...@chromium.org (2018-10-15)

> Not sure how y'all handle unexploitable-but-dangerous code.

That's a really good question that I've been trying to grapple with. Initially it seemed like we could limit the amount of unsafe code, but for a variety of good reasons that hasn't happened. Then I thought the fact that we commented each block of unsafe code and got it reviewed would act as a good mitigation, but it turns out its very easy to miss things like integer overflow, especially because its detection is contingent on the build profile. Now I'm thinking that using clippy more regularly might give us some meaningful protection, but I find that it produces code that is hard to reason about. For example, using wrapping_* and checked_*.unwrap() everywhere obfuscates the underlying arithmetic operation, which defeats the improvements to dangerous code, I feel.

So I don't know a very good solution. Maybe using integer-overflow checks even on release builds will be a good trade off here. What do you think? Do you have any good ideas to handle this dangerous code in Rust?

### al...@gmail.com (2018-10-15)

If this were my codebase, I'd make the following changes:

1) Switch to explicit checked_*() arithmetic in the places highlighted here
2) See if you can build for release with integer overflow panics enabled, and ship it that way
3) Migrate the other places that use this pattern to use |vec_with_array_field|. Those places are:

- src/plugin/vcpu.rs L460
- vhost/src/lib.rs L100
- x86_64/src/regs.rs L133

I'm also involved in the nascent Rust secure coding team, and I'd like to use this (and a few other instances of integer overflow problems) to try to answer the following questions:

1) Is there a general way to improve the integer overflow + unsafe combination leading to problems?
2) Is there a specific solution to the problem here? Which seems to be rooted in the need to allocate a struct+inline array, which doesn't have a safe-rust syntax.

### za...@chromium.org (2018-10-15)

1) My initial version for vec_with_array_field used checked arithmetic, but I couldn't get it reviewed for readability concerns, and I can't say I disagree. I tried a weird macro based solution here: https://chromium.googlesource.com/chromiumos/platform/crosvm/+/master/gpu_buffer/src/lib.rs#107 but I'm not very pleased with its syntax and fragility.
2) We're going to try that and see how it goes in terms of performance regressions: https://chromium-review.googlesource.com/c/chromiumos/platform/crosvm/+/1282064
3) Good point. We should do that.

With respect to the Rust secure coding team you mentioned, I'm curious if there is a way to follow along with that effort. Is there a mailing list I can join to get updates?

### al...@gmail.com (2018-10-15)

https://github.com/rust-secure-code is the github org, it's really just getting started at this moment. FWIW the folks really driving it are over in your cousin org, Fuschia, so they may have even more context to share.

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-21)

dgreid: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dg...@chromium.org (2018-10-22)

This didn't end up being an actual issue as it was covered by an early bounds check.

However, we are looking to enable overflow detection by default in the next release.

assign to zach to make sure that launches.

### za...@chromium.org (2018-10-22)

The CL to enable overflow checks landed here: https://chromium-review.googlesource.com/c/chromiumos/platform/crosvm/+/1282064

I forgot to put the bug number in the CL.

### sh...@chromium.org (2018-10-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-02)

Many thanks for the report, alex.gaynor@! The Chrome VRP panel decided to award $5,000 for this report. A member of our finance team will be in touch to arrange for payment.  Cheers!

### aw...@google.com (2018-11-02)

[Empty comment from Monorail migration]

### al...@gmail.com (2018-11-02)

Thanks! As a heads up in case it affects who'll process this, I'd like to donate this money to charity.

### aw...@google.com (2018-11-05)

Hi alex.gaynor@ - very many thanks, that's most generous! I'll send you details on how the donation works shortly.

### sh...@chromium.org (2019-01-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mp...@google.com (2019-01-29)

Alex, can Rust automatically subscribe variables used in unsafe code to automatic integer overflow checking, regardless of the build profile? Of course it wouldn't eliminate all logic errors stemming from integer overflow, that could lead to UB in unsafe code, but perhaps this would prevent exploitability of a large swath of common overflow errors like this one?

### al...@gmail.com (2019-01-29)

If by "can" you mean "does it", the answer is no. If you mean, "could it be expanded to do so", I think with the semantics of the language and the structure of the Rust compiler (as I understand it, not an expert), it could maybe be altered to handle some cases. Specifically cases where a computation flows into an unsafe block in the same function -- I think anything intraprocedural would be out of scope. But I think it'd be complex, and limited.

For example, would the following case be handled:

// Integer overflows in safe code, and something is allocated with less space than was expected
let vec = vec![0; length * height];

for i in 0..length {
    for j in 0..height {
        unsafe { vec.get_unchecked(i * height + j); }
    }
}

The unsafety is a combination of the overflow in safe code, which flowed into the safe constructor, and then elsewhere an unsafe subscript operation.

The more I write, the more I become convinced that dataflow analysis is probably not the right tool t address this.

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/892904?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092636)*
