# Security: Debug check failed: IsPrimitiveMap()

| Field | Value |
|-------|-------|
| **Issue ID** | [40061849](https://issues.chromium.org/issues/40061849) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | p4...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2022-11-21 |
| **Bounty** | $10,000.00 |

## Description

See details at https://crbug.com/chromium/1392061#c1.

## Attachments

- [test.js](attachments/test.js) (text/plain, 1.7 KB)

## Timeline

### p4...@gmail.com (2022-11-21)

This template is ONLY for reporting security bugs. If you are reporting a
Download Protection Bypass bug, please use the "Security - Download
Protection" template. For all other reports, please use a different
template.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com
/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs:
https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP:
http://g.co/ChromeBugRewards

NOTE: Security bugs are normally made public once a fix has been widely
deployed.

-------------------------

VULNERABILITY DETAILS
Please provide a brief explanation of the security issue.

The bug seems to be an issue in maglev. 

Its performance is getting a wrong object (maybe feedback of JSFunction) and then call Runtime_ToNumeric.

So it crashed at DCHECK when cast it as JSReceiver.

```c++
// ES6 section 9.2.1.2, OrdinaryCallBindThis for sloppy callee.
// static
MaybeHandle<JSReceiver> Object::ConvertReceiver(Isolate* isolate,
                                                Handle<Object> object) {
  if (object->IsJSReceiver()) return Handle<JSReceiver>::cast(object);
  if (object->IsNullOrUndefined(isolate)) {
    return isolate->global_proxy();
  }
  return Object::ToObject(isolate, object);
}

// static
MaybeHandle<Object> Object::ConvertToNumberOrNumeric(Isolate* isolate,
                                                     Handle<Object> input,
                                                     Conversion mode) {
  while (true) {
    if (input->IsNumber()) {
      return input;
    }
    if (input->IsString()) {
      return String::ToNumber(isolate, Handle<String>::cast(input));
    }
    if (input->IsOddball()) {
      return Oddball::ToNumber(isolate, Handle<Oddball>::cast(input));
    }
    if (input->IsSymbol()) {
      THROW_NEW_ERROR(isolate, NewTypeError(MessageTemplate::kSymbolToNumber),
                      Object);
    }
    if (input->IsBigInt()) {
      if (mode == Conversion::kToNumeric) return input;
      DCHECK_EQ(mode, Conversion::kToNumber);
      THROW_NEW_ERROR(isolate, NewTypeError(MessageTemplate::kBigIntToNumber),
                      Object);
    }
    ASSIGN_RETURN_ON_EXCEPTION(
        isolate, input,
 [*]       JSReceiver::ToPrimitive(isolate, Handle<JSReceiver>::cast(input),
                                ToPrimitiveHint::kNumber),
        Object);
  }
}
```




VERSION
v8 Version: commit 25b726493ae6db55f5f479029bee7617cac5bccd 
Operating System: all os

REPRODUCTION CASE
Please include a demonstration of the security bug, such as an attached
HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE
make the file as small as possible and remove any content not required to
demonstrate the bug, or any personal or confidential information.

Run the attached file in d8 with flag "--allow-natives-syntax --maglev", it will crash at the DCHECK failed.

Please attach files directly, not in zip or other archive formats, and if
you've created a demonstration site please also attach the files needed to
reproduce the demonstration locally.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab
Crash State: 
// Stderr:
// #
// # Fatal error in ../../src/objects/map-inl.h, line 332
// # Debug check failed: IsPrimitiveMap().
// #
// #
// #
// #FailureMessage Object: 0x7ffe3686c530Received signal 6


### [Deleted User] (2022-11-21)

[Empty comment from Monorail migration]

### p4...@gmail.com (2022-11-21)

[Comment Deleted]

### cl...@chromium.org (2022-11-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5588333540605952.

### cl...@chromium.org (2022-11-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6556639051317248.

### ve...@chromium.org (2022-11-21)

This is a security bug because we get confusion on registers (random values are swapped).

The steps to fix this are:
- don't emit exception phis for values that aren't assigned in a loop
   -> the problem is that a value should be live throughout a loop, but it's replaced with an exception phi even though the value doesn't change in the try-block
- eliminate catches that are unreachable (there are no throwing nodes in the try-block)
   -> the problem is that the value isn't spilled because there's no call/throw. If there were a throw, the value would have been spilled, and we would have been able to reload it.
- we should turn "can't load v27/n47, dropping the merge" into a (D)CHECK: if a loop header needs a node in a register, we can't just drop it
  -> this is fine on forward merges: if the value is dead (isn't in a register nor spilled), it normally can't be revived "in the future". This isn't true for loops though.


### dr...@chromium.org (2022-11-21)

[security sheriff] Thanks verwaest@! I'm assuming that confusion on registers can lead to memory corruption or code execution. Let me know if that's not the case.

### ve...@chromium.org (2022-11-22)

It could indeed, but note that this is a bug in a compiler that we're currently building, so there's currently no actual impact on users.

### ve...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### ve...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/a63f9912b71706f3483d945a9dce9977d46713e2

commit a63f9912b71706f3483d945a9dce9977d46713e2
Author: Toon Verwaest <verwaest@chromium.org>
Date: Thu Nov 24 10:13:13 2022

[maglev] Spill nodes that we'd otherwise fail to merge

This makes sure that catch-blocks don't accidentally drop values that
are only in registers, which can happen if we throw in deferred throwing
code (e.g., in ThrowReferenceErrorIfHole). At the latest we'll discover
such values when trying to merge after the catch block, noticing we
can't find the value through the catch-block. Unfortunately it's not
trivial to figure out where that merge happens, so we just
unconditionally spill the value.

For liveness holes (as the comment previously mentioned) the value
should already be dead and dropped on the merge. Running --maglev-stress
etc shows that no code currently hits this path, except for the added
test that shows the issue with catch blocks.

Bug: chromium:1392061
Change-Id: Ied0b1d4b430c9af2e7ae3dfc004ecb45037c5735
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4051605
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Auto-Submit: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84448}

[add] https://crrev.com/a63f9912b71706f3483d945a9dce9977d46713e2/test/mjsunit/maglev/regress/regress-crbug-1392061.js
[modify] https://crrev.com/a63f9912b71706f3483d945a9dce9977d46713e2/src/maglev/maglev-regalloc.cc
[modify] https://crrev.com/a63f9912b71706f3483d945a9dce9977d46713e2/src/maglev/maglev-graph.h
[modify] https://crrev.com/a63f9912b71706f3483d945a9dce9977d46713e2/src/maglev/maglev-graph-builder.h


### gi...@appspot.gserviceaccount.com (2022-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b18d3e8c0609a42f172ea25649865d4b7a32f960

commit b18d3e8c0609a42f172ea25649865d4b7a32f960
Author: Victor Gomes <victorgomes@chromium.org>
Date: Thu Nov 24 12:28:54 2022

Revert "[maglev] Spill nodes that we'd otherwise fail to merge"

This reverts commit a63f9912b71706f3483d945a9dce9977d46713e2.

Reason for revert: https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Linux64/50370/overview

Original change's description:
> [maglev] Spill nodes that we'd otherwise fail to merge
>
> This makes sure that catch-blocks don't accidentally drop values that
> are only in registers, which can happen if we throw in deferred throwing
> code (e.g., in ThrowReferenceErrorIfHole). At the latest we'll discover
> such values when trying to merge after the catch block, noticing we
> can't find the value through the catch-block. Unfortunately it's not
> trivial to figure out where that merge happens, so we just
> unconditionally spill the value.
>
> For liveness holes (as the comment previously mentioned) the value
> should already be dead and dropped on the merge. Running --maglev-stress
> etc shows that no code currently hits this path, except for the added
> test that shows the issue with catch blocks.
>
> Bug: chromium:1392061
> Change-Id: Ied0b1d4b430c9af2e7ae3dfc004ecb45037c5735
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4051605
> Reviewed-by: Leszek Swirski <leszeks@chromium.org>
> Commit-Queue: Leszek Swirski <leszeks@chromium.org>
> Commit-Queue: Toon Verwaest <verwaest@chromium.org>
> Auto-Submit: Toon Verwaest <verwaest@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#84448}

Bug: chromium:1392061
Change-Id: Iddbd7b19bc73e352dbd6867db990238f80adbdda
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4055504
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84455}

[delete] https://crrev.com/1b8a23b246e4e59f27c7b5cd32dc2fc913d8e034/test/mjsunit/maglev/regress/regress-crbug-1392061.js
[modify] https://crrev.com/b18d3e8c0609a42f172ea25649865d4b7a32f960/src/maglev/maglev-graph.h
[modify] https://crrev.com/b18d3e8c0609a42f172ea25649865d4b7a32f960/src/maglev/maglev-regalloc.cc
[modify] https://crrev.com/b18d3e8c0609a42f172ea25649865d4b7a32f960/src/maglev/maglev-graph-builder.h


### gi...@appspot.gserviceaccount.com (2022-11-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/46d21053377caf859610e03e62b8710c2c0b6f00

commit 46d21053377caf859610e03e62b8710c2c0b6f00
Author: Toon Verwaest <verwaest@chromium.org>
Date: Fri Nov 25 11:18:00 2022

[maglev] Spill values across throw->catch

If a value is used after a try-block finishes, we need to make sure that
the catch-block can restore its value. Otherwise we'd accidentally drop
the value on register merge thinking we're in a liveness hole on the
merge after the catch (since the catch cleared all the registers). This
then breaks JumpLoops that need to restore the value in a specific
register.

Bug: v8:7700, chromium:1392061
Change-Id: I7255ccf9b36bf36583ad612882137b251c48caed
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4055111
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Auto-Submit: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84483}

[add] https://crrev.com/46d21053377caf859610e03e62b8710c2c0b6f00/test/mjsunit/maglev/regress/regress-crbug-1392061.js
[modify] https://crrev.com/46d21053377caf859610e03e62b8710c2c0b6f00/src/maglev/maglev-regalloc.cc


### p4...@gmail.com (2022-11-29)

[Comment Deleted]

### ve...@chromium.org (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations, Bohan Liu! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-07)

This issue was migrated from crbug.com/chromium/1392061?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061849)*
