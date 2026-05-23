# (Switch statement) Google Chrome on iPadOS 26.0 sad tabs

| Field | Value |
|-------|-------|
| **Issue ID** | [445738066](https://issues.chromium.org/issues/445738066) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **CVE IDs** | CVE-2025-43427 |
| **Reporter** | nt...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2025-09-18 |
| **Bounty** | Confirmed (amount unknown) |

## Description

VULNERABILITY DETAILS

Open the following testcase in Google Chrome on iPadOS 26.0.

VERSION
Chrome Version: 140.0.7339.122
Operating System: iPadOS 26.0 (23A341)

REPRODUCTION CASE

As attached.

I will have a bisection result soon.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab
Crash State: Sad tab on iPadOS 26.0

This also happens on Safari.

I'll be attaching JavaScriptCore stacks soon because Google Chrome on iOS should be using WebKit (jsc).

As per https://issues.chromium.org/issues/360520332 - I will file with Apple Security and paste the ID here soon.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Gary Kwong

## Attachments

- [testcase.html](attachments/testcase.html) (text/html, 174 B)
- [debug-stack.txt](attachments/debug-stack.txt) (text/plain, 3.1 KB)
- [opt-stack.txt](attachments/opt-stack.txt) (text/plain, 4.9 KB)

## Timeline

### nt...@gmail.com (2025-09-18)

Stack with a debug JavaScriptCore build.

### nt...@gmail.com (2025-09-18)

Stack with a ASan opt JavaScriptCore build.

### nt...@gmail.com (2025-09-18)

I have an ID of OE1103672426361 from Apple.

### nt...@gmail.com (2025-09-18)

The following changesets may be related as possible regressors:

```
5085bf6dcfc2-297160
5085bf6dcfc2d22a7f35f1077bfa0d56ca783e33 is the first bad commit
commit 5085bf6dcfc2d22a7f35f1077bfa0d56ca783e33
Author: Yusuke Suzuki <ysuzuki@apple.com>
Date:   Wed Jul 9 06:25:16 2025 -0700

    [JSC] Add list style switch
    https://bugs.webkit.org/show_bug.cgi?id=295480
    rdar://155116968

    Reviewed by Yijia Huang.

    Previously, we were giving up using switch_imm / switch_char when
    JumpTable becomes too large. But this is problematic since we starts
    using if-else instead, and failing to offer structured control flow
    information well to Baseline / DFG / FTL as they can do some
    optimizations based on these control structures.

    In this patch, we introduce ImmList and CharList. When the range is too
    large, we start using list of imm & offset / char & offset instead of
    jumptable. In LLInt, we do a slow path. In Baseline, DFG, FTL, we do
    BinarySwitch based on this information. To make code simple, we add fast
    path for switch_imm / switch_char properly in JIT code so we do not need
    to handle these different tables in JIT operations functions much.

    /snip

    Canonical link: https://commits.webkit.org/297160@main


5d2ec41c81f0-297526
5d2ec41c81f0bab202d687d1bf941cfe53433f2d is the first crash commit
commit 5d2ec41c81f0bab202d687d1bf941cfe53433f2d
Author: Chris Dumez <cdumez@apple.com>
Date:   Thu Jul 17 09:07:21 2025 -0700

    Drop WTF_ALLOW_UNSAFE_BUFFER_USAGE in wtf/TrailingArray.h
    https://bugs.webkit.org/show_bug.cgi?id=296002

    Reviewed by Darin Adler.

    This tested as performance neutral on Speedometer and JetStream.

    /snip

    Canonical link: https://commits.webkit.org/297526@main
```

### xi...@chromium.org (2025-09-18)

Thanks for the report. Triaged the same way as https://crbug.com/360520332

### ch...@google.com (2025-09-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-09-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-10-03)

michaeldo: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### nt...@gmail.com (2026-01-01)

Apple has assigned CVE-2025-43427 to this issue, and the issue is now marked as Resolved.

I tested that this testcase no longer causes a sad tab as of iPadOS 26.1.

May I know what is next here?

### nt...@gmail.com (2026-01-29)

Ping? May I know if there are any updates?

### sp...@google.com (2026-02-20)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Controlled assertion failure

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-05-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Controlled assertion failure
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/445738066)*
