# Security: [V8] [turboshaft] Yet another minus zero case missing when typing divisions.

| Field | Value |
|-------|-------|
| **Issue ID** | [40943982](https://issues.chromium.org/issues/40943982) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | in...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2023-11-19 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

Turboshaft misses a case that can lead to minus zero when typing divisions.

In v8/src/compiler/turboshaft/typer.h "FloatOperationTyper.Divide" we try to rule out minus zero:

```
// Try to rule out -0.  
bool maybe_minuszero =  
    // -0 / r (r > 0)  
    (l.has_minus_zero() && r_max > 0) // #1  
    // 0 / r (r < 0)  
    || (l.Contains(0) && r_min < 0) // #2  
    // -0.0..01 / r (r > 1)  
    || (l.Contains(0) && l_min < 0 && r_min > 1) // #3  
    // 0.0..01 / r (r < -1)  
    || (l.Contains(0) && l_max >= 0 && r_min < -1) // #4  
    // l / large (l < 0)  
    || (l_max < 0 && detail::is_minus_zero(l_max / r_max)) // #5  
    // l / -large (l > 0)  
    || (l_min > 0 && detail::is_minus_zero(l_min / r_min)); // #6  

```

However, the third case is wrong:

```
// -0.0..01 / r (r > 1)  
|| (l.Contains(0) && l_min < 0 && r_min > 1) // #3  

```

Consider this type for l:  

Float64[-inf, inf]|NaN  

and this type for r:  

Float64[1, 1e+308]|NaN  

With l having the actual value `-2.00084e-18` and r having the actual value `1e+308`.  

(These ranges are from yolo2.js) (See yolo2\_old\_ranges.js for slightly more detailed ranges but I can not reproduce these ranges on 0da78a49ceddd38910efcd7983e54e99b1166d0a. See works.js (ugly) for `Float64[-2.00084e-18, 4]|NaN` as a range for `l`)  

#1 isn't triggered, because l doesn't has the MinusZero flag.  

#2 isn't triggered, because r\_min is 1 and `1 < 0` is false.  

#3 isn't triggered, because r\_min is 1 and `1 > 1` is false.  

#4 isn't triggered, because r\_min is 1 and `1 < -1` is false.  

#5 isn't triggered, because l\_max is inf and `inf < 0` is false.  

#6 isn't triggered, because l\_min is -inf and `-inf > 0` is false.  

Because none of the conditions is true, the resulting range does NOT get the MinusZero flag.  

This is wrong, because `-2.00084e-18/1e+308` is clearly `-0`.

If we closely look at the third case, we can see where the issue is:  

We want to find cases where the result \*\*may\*\* be minus zero.  

When \*\*can\*\* this be the case? When l is `-0.0..01` and r \*\*can\*\* be greater than 1.  

r \*\*can\*\* be greater than 1 <=> r\_max > 1  

The condition as currently written checks something else:  

r is \*\*always\*\* greater than 1 <=> r\_min > 1

**VERSION**

Chrome Version: 120.0.6099.28 aka beta

V8 Version: 12.0.267.5

Operating System: Linux 6.1.0-13-amd64 #1 SMP PREEMPT\_DYNAMIC Debian 6.1.55-1 (2023-09-29) x86\_64 GNU/Linux

**REPRODUCTION CASE**

1. Place yolo2.js in v8/test/mjsunit/regress/
2. Run `gm x64.debug mjsunit/regress/yolo2 --verbose`
3. You should be greeted with an assertion violation.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: Assertion violation. (I did not yet have time to further investigate the impact)  

Crash State:

```
Type assertion failed!  
Node id: DebugPrint: Smi: 0x173 (371)  
  
Actual value: -0  
Expected type: DebugPrint: 0x4c100254769: [TurboshaftFloat64RangeType]  
 - map: 0x04c100001855 <Map[28](TURBOSHAFT_FLOAT64_RANGE_TYPE_TYPE)>  
 - special_values: 1  
 - _padding: 0  
 - min: -inf  
 - max: inf  
0x4c100001855: [Map] in ReadOnlySpace  
 - type: TURBOSHAFT_FLOAT64_RANGE_TYPE_TYPE  
 - instance size: 28  
 - elements kind: HOLEY_ELEMENTS  
 - enum length: invalid  
 - stable_map  
 - back pointer: 0x04c100000061 <undefined>  
 - prototype_validity cell: 0  
 - instance descriptors (own) #0: 0x04c1000006d9 <DescriptorArray[0]>  
 - prototype: 0x04c10000007d <null>  
 - constructor: 0x04c10000007d <null>  
 - dependent code: 0x04c1000006b5 <Other heap object (WEAK_ARRAY_LIST_TYPE)>  
 - construction counter: 0  
V8 is running with experimental features enabled. Stability and security will suffer.  
halting because of unreachable code at src/objects/turboshaft-types.tq:234:3  
Trace/breakpoint trap  

```

(Experimental features are due to the usage of `--turboshaft-assert-types`)

BISECT COMMIT:  

First commit that crashes with assertion violation (needs `--turboshaft`) (assert verification was added in this commit)  

<https://github.com/v8/v8/blob/c7970ae1fd52c8ae84329e46a1d33a32c9ceb454/src/compiler/turboshaft/typer.h#L672-L679>

First commit that crashes with assertion violation and doesn't need `--turboshaft` is ("obviously") this one:  

<https://github.com/v8/v8/commit/d07707d6cfbbbee0454ec017b5a050224659dd2d>

FIX  

A patch that fixes the issue for me is attached.  

Note that neither <https://github.com/v8/v8/commit/5717dde33c7d2f8a5df199d634ac96c1d2386b84> nor <https://github.com/v8/v8/commit/e1f7254f7a7042d9b4139e3847d3946e71bba663> caught this issue.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Simon Gerst (intrigus-lgtm)

## Attachments

- [works.js](attachments/works.js) (text/plain, 1.9 KB)
- [turboshaft_division.patch](attachments/turboshaft_division.patch) (text/plain, 569 B)
- [yolo2.js](attachments/yolo2.js) (text/plain, 870 B)
- [yolo2_old_ranges.js](attachments/yolo2_old_ranges.js) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2023-11-19)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-11-19)

Setting provisional severity:high, found:118, and security_impact:none and assigning to the current V8 sheriff.

### an...@chromium.org (2023-11-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler>Turbofan]

### an...@chromium.org (2023-11-19)

[Empty comment from Monorail migration]

### sr...@google.com (2023-11-20)

Nico can you take a look? The impact is set to none right now, is it still the case that the turboshaft typing doesn't ship yet?

### ni...@chromium.org (2023-11-20)

Thanks for the very detailed report! I will take a look.

@sroettger: Right, typer is used internally only right now.

### an...@chromium.org (2023-11-30)

Hey Nico, secondary security shepherd here. Do you plan to work on this bug soon? Since this is a Security_Impact-None, can we block a feature bug with this bug - just to make sure we don't release w/o addressing this issue? Thanks!

### ni...@chromium.org (2023-11-30)

Will take a look at this soon. The typer, which is wrong here, is not used in production and there are no plans to ship this at any time soon, so this should definately not block anything.

### ja...@chromium.org (2023-12-14)

Hi  nicohartmann@, I know it isn't shipped yet, but maybe you can take a look. If it is a valid issue, you could add a TODO by the flag that enables this code to make sure this issue gets addressed before launching it. Thanks! [secondary security shepherd]

### ni...@chromium.org (2023-12-15)

Thanks for the extremely detailed investigation. Preparing the fix ...

### gi...@appspot.gserviceaccount.com (2023-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/6156ec06600705a66d51b6fc63e80567dc814840

commit 6156ec06600705a66d51b6fc63e80567dc814840
Author: Nico Hartmann <nicohartmann@chromium.org>
Date: Fri Dec 15 10:51:09 2023

[turboshaft] Fix another -0 case in typer

Bug: v8:12783, chromium:1503528
Change-Id: Ib3da21bc0225c65ec2bf22bc7ed59f4b3e7a0b1d
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5126171
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91545}

[add] https://crrev.com/6156ec06600705a66d51b6fc63e80567dc814840/test/mjsunit/regress/regress-1503528.js
[modify] https://crrev.com/6156ec06600705a66d51b6fc63e80567dc814840/src/compiler/turboshaft/typer.h


### ni...@chromium.org (2023-12-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-18)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-03)

Congratulations, Simon! The Chrome VRP Panel has decided to award you $10,000 for this high quality report of renderer memory corruption / RCE + $1,000 patch bonus. A member of our p2p-vrp finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! And Happy New Year! 

### am...@chromium.org (2024-01-03)

[Empty comment from Monorail migration]

### in...@gmail.com (2024-01-04)

Hi, amyressler@ thanks for the nice bounty and happy New Year as well :)

### am...@chromium.org (2024-01-04)

A note to the reporter, but also a general note and something I was remiss in including in https://crbug.com/chromium/1503528#c15, this issue is specific to the experimental configuration of V8 (as --turboshaft-assert-types is still in Experimental status ["V8 is running with experimental features enabled. Stability and security will suffer"] and is considered out of scope for Chrome VRP [1].

Due to this being a very high quality report AND being an issue that would have been unlikely to be discovered by other means, such as Clusterfuzz, the Chrome VRP has made a one-time exception in rewarding this issue. It should not be considered a precedent by this report or for others once this issue is publicly disclosure. VRP reporters should generally avoid submitting reports for issues in experimental status, unless they have otherwise demonstrated or determine that the code path is reachable and exploitable without enabling non-default features or that feature has been enabled in OT or finch experiments. Please do not submit reports for issues in experimental configuration and cite this report as the reasoning. 

[1] https://g.co/chrome/vrp/#scope-of-program

### am...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/1503528?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40943982)*
