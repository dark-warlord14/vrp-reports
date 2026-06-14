# Security: missing the -0 case when intersecting and computing the Type::Range in NumberMax

| Field | Value |
|-------|-------|
| **Issue ID** | [40052054](https://issues.chromium.org/issues/40052054) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ja...@gmail.com |
| **Assignee** | ne...@chromium.org |
| **Created** | 2020-04-18 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

In the Typer phase Math.max and Math.min generate the wrong type by mistakenly removing the Type::MinusZero property of the input nodes.

The faulty code is within the operation-typer.cc file here:  

<https://chromium.googlesource.com/v8/v8.git/+/refs/heads/master/src/compiler/operation-typer.cc#1051>

In the cases that, for example, rhx is Type::MinusZero the following code:

```
  rhs = Type::Intersect(rhs, cache_->kInteger, zone());  

```

The aforementioned code will wrongly remove the Type::MinusZero and therefore rhs.IsNone() will yield true on the following lines of code:

```
   double min = std::max(lhs.IsNone() ? -V8_INFINITY : lhs.Min(),  
                          rhs.IsNone() ? -V8_INFINITY : rhs.Min());  
   double max = std::max(lhs.IsNone() ? -V8_INFINITY : lhs.Max(),  
                          rhs.IsNone() ? -V8_INFINITY : rhs.Max());  
   type = Type::Union(type, Type::Range(min, max, zone()), zone());  

```

This will lead to cases in which the Type::Range(min, max, zone()) is wrongly computed due to the first run being Range(-1, -1) and the next Typer run, before crashing, starting on Range(1, 1).

I haven't tried yet to exploit this behaviour but since it seems to omit the -0 case, which is similar to [crbug/880207](https://crbug.com/880207), I'm filing it as a security bug.

PROPOSED FIX for CASE 2:

```
  bool const lhs_maybe_minus_zero = lhs.Maybe(Type::MinusZero());  
  bool const rhs_maybe_minus_zero = rhs.Maybe(Type::MinusZero());  
  if (lhs_maybe_minus_zero)  
    lhs = Type::Union(lhs, Type::MinusZero(), zone());  
  if (rhs_maybe_minus_zero)  
    rhs = Type::Union(lhs, Type::MinusZero(), zone());  
  lhs = Type::Intersect(lhs, cache_->kInteger, zone());  
  rhs = Type::Intersect(rhs, cache_->kInteger, zone());  

```

**VERSION**  

v8 commit: 350e0f7997fdb936510ecc6132e84533393c5066  

Also hangs the renderer on the latest Chrome stable  

Operating System: All platforms.

**REPRODUCTION CASE**  

CASE 1  

function crash() {  

for (a=0;a<2;a++)  

for (let i = -0.0; i < 1000; i++) {  

confused = Math.max(-1, i);  

}  

confused[0];  

}

crash();  

%OptimizeFunctionOnNextCall(crash);  

crash();

CASE 2  

function crash() {  

let confused;  

for (let i = -0.0; i < 1000; i++) {  

confused = Math.max(-1, i);  

}  

confused[0];  

}

crash();  

%OptimizeFunctionOnNextCall(crash);  

crash();

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Crash State:  

Case 1  

Trace/breakpoint trap (core dumped)  

Case 2

# Fatal error in , line 0

# UpdateType error for node 75: NumberMax(73, 74)

73: SpeculativeToNumber[NumberOrOddball, FeedbackSource(#5)](41, 71, 31)  

74: SpeculativeToNumber[NumberOrOddball, FeedbackSource(#5)](17, 73, 31)

**CREDIT INFORMATION**  

Reporter credit: Javier Jimenez of SensePost (@n30m1nd). Also credit to Saelo and the AFL++ project.

## Timeline

### ja...@gmail.com (2020-04-19)

I did some further research on the Case 1 and it seems it could be exploitable same as Issue-1710 if a way to bypass the boundary checks is found:

REPRODUCTION CASE:
function crash() {
    let confused;
    for (a=0;a<2;a++) {
        for (let i = -0.0; i < 100; i++) {
            confused = Math.max(-1, i);
            console.log(Object.is(confused, -0));
        }
    }
}
%PrepareFunctionForOptimization(crash);
(crash());
%OptimizeFunctionOnNextCall(crash);
(crash());

RUN WITH:
/home/javier/Fuzzing/Victims/V8/clean/v8/out.gn/x64.release/d8 --allow-natives-syntax --debug-code --expose-gc --single-threaded --predictable --interrupt-budget=1024 --no-arguments confused-minus-0.js  | uniq -c

OUTPUT:
      1 true
     99 false
      1 true
     99 false
      1 [+] After optimisation
    200 false

On the run after optimisation, the optimiser ruled out the -0 case. yielding false all the 200 iterations.

### do...@chromium.org (2020-04-19)

+folks from https://crbug.com/chromium/880207 for further investigation. It's unclear to me whether this is as exploitable as 880207, so I'm assigning medium severity for the time being.

[Monorail components: Blink>JavaScript>Compiler]

### do...@chromium.org (2020-04-19)

Also +current v8 sheriff

### bm...@chromium.org (2020-04-20)

Over to V8 folks.

### ne...@chromium.org (2020-04-20)

Oh no. Thanks for the report, will look into that today.

### ne...@chromium.org (2020-04-20)

[Empty comment from Monorail migration]

### ne...@chromium.org (2020-04-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/4158af83db7bab57670a9254b766df784cd8a15e

commit 4158af83db7bab57670a9254b766df784cd8a15e
Author: Georg Neis <neis@chromium.org>
Date: Mon Apr 20 17:05:50 2020

[turbofan] Fix bug in Number.Min/Max typings

They try to be very precise about when the result can be -0,
but do so incorrectly. I'm changing the code to just do the
simple thing instead. Let's see how that affects performance.

Bug: chromium:1072171
Change-Id: I9737a84aa19d06685af5b7bca541e348dc37cca8
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2157028
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#67246}

[modify] https://crrev.com/4158af83db7bab57670a9254b766df784cd8a15e/src/compiler/operation-typer.cc
[add] https://crrev.com/4158af83db7bab57670a9254b766df784cd8a15e/test/mjsunit/compiler/regress-1072171.js
[modify] https://crrev.com/4158af83db7bab57670a9254b766df784cd8a15e/test/unittests/compiler/typer-unittest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f442b03fe2c1d38a72d23ca5c01c8091af0e4dc7

commit f442b03fe2c1d38a72d23ca5c01c8091af0e4dc7
Author: Francis McCabe <fgm@chromium.org>
Date: Mon Apr 20 18:01:02 2020

Revert "[turbofan] Fix bug in Number.Min/Max typings"

This reverts commit 4158af83db7bab57670a9254b766df784cd8a15e.

Reason for revert: causing UBSAN failures:

https://ci.chromium.org/p/v8/builders/ci/V8%20Linux64%20UBSan/10729?


Original change's description:
> [turbofan] Fix bug in Number.Min/Max typings
> 
> They try to be very precise about when the result can be -0,
> but do so incorrectly. I'm changing the code to just do the
> simple thing instead. Let's see how that affects performance.
> 
> Bug: chromium:1072171
> Change-Id: I9737a84aa19d06685af5b7bca541e348dc37cca8
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2157028
> Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
> Commit-Queue: Georg Neis <neis@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#67246}

TBR=neis@chromium.org,tebbi@chromium.org

Change-Id: I0d9b312e27f5a8bbbebeccdc9819fa94f10af139
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1072171
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2157646
Reviewed-by: Francis McCabe <fgm@chromium.org>
Commit-Queue: Francis McCabe <fgm@chromium.org>
Cr-Commit-Position: refs/heads/master@{#67249}

[modify] https://crrev.com/f442b03fe2c1d38a72d23ca5c01c8091af0e4dc7/src/compiler/operation-typer.cc
[delete] https://crrev.com/7f2e53a7d103d1c4290a12b3bd3ba78d3887a0bd/test/mjsunit/compiler/regress-1072171.js
[modify] https://crrev.com/f442b03fe2c1d38a72d23ca5c01c8091af0e4dc7/test/unittests/compiler/typer-unittest.cc


### do...@chromium.org (2020-04-21)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/898b8915b0e7fb996afa0f0a5e97f431d7e8e22e

commit 898b8915b0e7fb996afa0f0a5e97f431d7e8e22e
Author: Georg Neis <neis@chromium.org>
Date: Tue Apr 21 07:45:22 2020

Reland "[turbofan] Fix bug in Number.Min/Max typings"

This reverts commit f442b03fe2c1d38a72d23ca5c01c8091af0e4dc7.

Reason for reland: Wrongly reverted.

Original change's description:
> Revert "[turbofan] Fix bug in Number.Min/Max typings"
> 
> This reverts commit 4158af83db7bab57670a9254b766df784cd8a15e.
> 
> Reason for revert: causing UBSAN failures:
> 
> https://ci.chromium.org/p/v8/builders/ci/V8%20Linux64%20UBSan/10729?
> 
> 
> Original change's description:
> > [turbofan] Fix bug in Number.Min/Max typings
> > 
> > They try to be very precise about when the result can be -0,
> > but do so incorrectly. I'm changing the code to just do the
> > simple thing instead. Let's see how that affects performance.
> > 
> > Bug: chromium:1072171
> > Change-Id: I9737a84aa19d06685af5b7bca541e348dc37cca8
> > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2157028
> > Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
> > Commit-Queue: Georg Neis <neis@chromium.org>
> > Cr-Commit-Position: refs/heads/master@{#67246}
> 
> TBR=neis@chromium.org,tebbi@chromium.org
> 
> Change-Id: I0d9b312e27f5a8bbbebeccdc9819fa94f10af139
> No-Presubmit: true
> No-Tree-Checks: true
> No-Try: true
> Bug: chromium:1072171
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2157646
> Reviewed-by: Francis McCabe <fgm@chromium.org>
> Commit-Queue: Francis McCabe <fgm@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#67249}

TBR=neis@chromium.org,tebbi@chromium.org,fgm@chromium.org

Change-Id: Ida36ca584a5af5da887189328c8da195b26285d4
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1072171
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2157368
Reviewed-by: Georg Neis <neis@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#67263}

[modify] https://crrev.com/898b8915b0e7fb996afa0f0a5e97f431d7e8e22e/src/compiler/operation-typer.cc
[add] https://crrev.com/898b8915b0e7fb996afa0f0a5e97f431d7e8e22e/test/mjsunit/compiler/regress-1072171.js
[modify] https://crrev.com/898b8915b0e7fb996afa0f0a5e97f431d7e8e22e/test/unittests/compiler/typer-unittest.cc


### ne...@chromium.org (2020-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-22)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-04-22)

+adetaylor@ to review/approve

Please help answer questions in https://crbug.com/chromium/1072171#c13

### [Deleted User] (2020-04-23)

[Empty comment from Monorail migration]

### ne...@chromium.org (2020-04-24)

1. I don't know, that page is quite complicated.
2. https://chromium.googlesource.com/v8/v8.git/+/4158af83db7bab57670a9254b766df784cd8a15e
3. Yes.
4. Fix for high-severity security issue.
5. No.

### ne...@chromium.org (2020-04-24)

Regarding 1, the three "Merge Requirements" are satisfied.

### ad...@chromium.org (2020-04-24)

Approving merge to M83 (branch 4103) and M81 (branch 4044) assuming no problems are visible in Canary.

### ja...@gmail.com (2020-04-24)

[Comment Deleted]

### ja...@gmail.com (2020-04-24)

Hello, I see that although the severity was high and affecting stable, the "reward-topanel" label hasn't been set. Any insight on this and eligibility? Thanks!

### ad...@chromium.org (2020-04-24)

javijmor@gmail.com - this should indeed go via the VRP panel sometime in the next couple of weeks. Our processes should add reward-topanel in due course.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3e59f5e12080d34bd86c9268818da7e5f4172c62

commit 3e59f5e12080d34bd86c9268818da7e5f4172c62
Author: Georg Neis <neis@chromium.org>
Date: Mon Apr 27 10:29:06 2020

Merged: [turbofan] Fix bug in Number.Min/Max typings

Revision: 4158af83db7bab57670a9254b766df784cd8a15e

BUG=chromium:1072171
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=tebbi@chromium.org

Change-Id: I90584c0233ee97d485854ce9ac3919fd73692ba8
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2167273
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.3@{#14}
Cr-Branched-From: 1668abddd8147c49c8f2f90b78dc2701f3794a30-refs/heads/8.3.110@{#1}
Cr-Branched-From: 04a7a680a2838e1789f277495181e709e14a17ba-refs/heads/master@{#66926}

[modify] https://crrev.com/3e59f5e12080d34bd86c9268818da7e5f4172c62/src/compiler/operation-typer.cc
[add] https://crrev.com/3e59f5e12080d34bd86c9268818da7e5f4172c62/test/mjsunit/compiler/regress-1072171.js
[modify] https://crrev.com/3e59f5e12080d34bd86c9268818da7e5f4172c62/test/unittests/compiler/typer-unittest.cc


### ne...@chromium.org (2020-04-27)

Actually his bug is not present in 81.  javijmor@gmail.com, I'm not able to reproduce any hangs in stable using your examples.

### [Deleted User] (2020-04-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@chromium.org (2020-04-27)

[Empty comment from Monorail migration]

### ja...@gmail.com (2020-04-27)

neis@chromium the following cases did make the console to become unresponsive in the developer tools when I first reported it. Trying to execute any other commands would just not work but, no sad face tab though:

---- Math.max-crash.js
```
function crash() {
    let confused;
    for (let i = -0.0; i < 1000; i++) {
        confused = Math.max(0, i); 
    }
    confused[0]; // Any manipulation of "confused" will trigger a crash
}   

crash();
for (let i = 0; i < 1000; i++)
  crash();
```
---- Math.min-crash.js ----
```
function crash(x,...y) { 
    for (let i = -0.0; i < 10000; i++) {
        const zero = Math.ceil(y); // Changing this for [floor, round, trunc] function will still crash.
        const confused = Math.min(zero,i);
        confused[0];
    }
}   

crash();
for (let i = 0; i < 1000; i++)
  crash();
```
----------


Finally, while trying to exploit it and, in case it may help further, I managed to get a much more minimised version of the bug:
```
function opt() {
    let res;
    for (a=0;a<1;a++) {
        for (let i = -0.0; i < 1; i++) {
            res = Object.is(Math.max(-1, i), -0);
        }
    }
    return res;
}

%PrepareFunctionForOptimization(opt);
console.log(opt());
%OptimizeFunctionOnNextCall(opt);
console.log(opt());
```
Output:
```
./d8 --allow-natives-syntax minimised-NumberMax.js
true
false
```

### [Deleted User] (2020-04-27)

Setting milestone and target because of Security_Impact=Beta and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@chromium.org (2020-04-27)

I'm unable to reproduce any issues in 81.

### ja...@gmail.com (2020-04-27)

I've been looking around my notes and test cases and a few of them didn't have the `let` instruction, so these might seem to have re-set the `i` variable to 0 for the `for` loops, which might point at why the console was unresponsive when testing (infinitely looping). Apologies for the confusion. The first v8 commit where I found these crashing was 04a7a680a2838e1789f277495181e709e14a17ba, hope that helps tracing whether it made it further than beta.

### na...@google.com (2020-04-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-30)

Congrats! The Panel decided to award $7,500 for this report!

### na...@google.com (2020-05-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1072171?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052054)*
