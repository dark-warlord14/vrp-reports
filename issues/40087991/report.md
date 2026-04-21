# Security: Information Disclosure Issue in v8::wasm

| Field | Value |
|-------|-------|
| **Issue ID** | [40087991](https://issues.chromium.org/issues/40087991) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Reporter** | xi...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2017-06-06 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**

There is a out of boundary issue in v8::wasm::module-decoder, which will disclosure sensitive information in the heap.

In v8\src\wasm\module-decoder.cc, the function next(), DecodeModule(), and DecodeCustomSections() doesn't handle the custom section properly.

In next(),  

if (section\_code\_ == kUnknownSectionCode &&  

section\_end\_ > decoder\_.pc()) {  

// skip to the end of the unknown section.  

uint32\_t remaining =  

static\_cast<uint32\_t>(section\_end\_ - decoder\_.pc());  

decoder\_.consume\_bytes(remaining, "section payload");  

// fall through and continue to the next section.  

} else {  

return;  

}  

Here if section\_end\_ <= decoder\_.pc, the iterator simply exit. The section\_code\_ remains be kUnknownSectionCode.

Then in function DecodeModule(),  

if (section\_iter.more() && ok()) {  

errorf(pc(), "unexpected section: %s",  

SectionName(section\_iter.section\_code()));  

}  

Because section\_code\_ is kUnknownSectionCode, here will not trigger the errorf and everything is OK.

Then in DecodeCustomSections(), all the data will be treated as checked, and simply run through.  

So if we put a large section\_length here, the payload\_length will go out of the buffer boundary.

**VERSION**  

Chrome Version: [59.0.3071.86] + [stable]  

Operating System: [Windows 7 Service Pack1]

**REPRODUCTION CASE**  

Open the attach wasm\_exp.html, you'll see leaked heap values.

## Attachments

- [wasm_exp.html](attachments/wasm_exp.html) (text/plain, 498 B)

## Timeline

### el...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>WebAssembly]

### cl...@chromium.org (2017-06-06)

I can confirm the bug for v8 5.9.223.

The problem was fixed with https://chromium-review.googlesource.com/c/505490/, which landed in 6.0.247.

### jo...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-06-06)

We are working on a fix for the 5.9 branch.

### cl...@chromium.org (2017-06-06)

CL is here, to be merged into the 5.9 branch: https://chromium-review.googlesource.com/c/525754/

Jochen, PTAL.

### cl...@chromium.org (2017-06-06)

And a regression test for the master branch: https://chromium-review.googlesource.com/c/525538/

### jo...@chromium.org (2017-06-06)

What's the severity of the issue? Can you add Merge-Request labels and release block labels as appropriate please?

### bu...@chromium.org (2017-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/fa0d5be128ea9be4d72a0ff7d963dc118235af52

commit fa0d5be128ea9be4d72a0ff7d963dc118235af52
Author: Clemens Hammacher <clemensh@chromium.org>
Date: Tue Jun 06 15:55:02 2017

[wasm] Add regression test

The regression is already fixed. This just adds a regression test to
ensure it will never be reintroduced.

R=ahaas@chromium.org
BUG=chromium:729991

Change-Id: I5cf960cc756cbb7723041bc06a78d6a14c66e241
Reviewed-on: https://chromium-review.googlesource.com/525538
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#45739}
[add] https://crrev.com/fa0d5be128ea9be4d72a0ff7d963dc118235af52/test/mjsunit/regress/wasm/regression-729991.js


### cl...@chromium.org (2017-06-06)

This bug allows creating an ArrayBuffer which contains a copy of the memory of user-controlled size, starting inside the SeqOneByteString which holds the wasm module bytes.
Thus it must be considered to allow reading more or less arbitrary memory of the process.

The bug already existed in M58, but since M59 is just being release, merging back seems not necessary.

### sh...@chromium.org (2017-06-06)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), Abdul Syed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2017-06-06)

Release block labels seem inappropriate, as the bug is already out there.

### cl...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### ca...@chromium.org (2017-06-06)

Please tag with applicable OSs.

### cl...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-06-07)

Still waiting for official approval to land this CL directly on the 5.9 branch: https://chromium-review.googlesource.com/c/525754/

### sh...@chromium.org (2017-06-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-07)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-06-07)

Would somebody mind double checking what Chrome version v8 6.0.247 landed it? I get 60.0.3112.20 was released 6/6.  We should give this some more time to bake, but should certainly consider it for a 59 stable update if one occurs.

### el...@chromium.org (2017-06-07)

https://chromium.googlesource.com/chromium/src/+/92860763bac3133a6729756f0f7899f69c22e9b2 brought 6.0.249 to Chrome 60.0.3104.0. The prior roll was 6.0.242 for Chrome 60.0.3103.0.

### cl...@chromium.org (2017-06-07)

6.0.249 (containing a refactoring which fixed this bug) was rolled into chrome on May 17. This is contained in 60.0.3104.0.

We don't want to merge that CL back though. It's much lower risk to just land the CL referenced in #16 on the 5.9 branch.
I am waiting for Jochen (or someone else) to approve this.

### ab...@chromium.org (2017-06-07)

+ Adam Klein

### xi...@gmail.com (2017-06-08)

So I see this issue had already been fixed in the DEV branch.

May I ask that whether can I still receive the CVE and reward?

### sh...@chromium.org (2017-06-08)

[Empty comment from Monorail migration]

### ad...@chromium.org (2017-06-08)

Landing https://chromium-review.googlesource.com/c/525754/ on the v8 5.9 branch sounds good to me.

### bu...@chromium.org (2017-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/e23b659865e16de9482e19732650d57b3ff0b374

commit e23b659865e16de9482e19732650d57b3ff0b374
Author: Clemens Hammacher <clemensh@chromium.org>
Date: Fri Jun 09 09:12:47 2017

[wasm] Validate length of unknown sections

For empty unknown sections, the section iterator was just returning
without checking any succeeding sections. Instead, it should continue
explictly skipping over them, while checking that the payload length is
valid (i.e. in bounds of the module bytes).

R=ahaas@chromium.org, jochen@chromium.org
BUG=chromium:729991
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

Also-by: ahaas@chromium.org
Change-Id: Ia64068b40817a9da4cca836f1a21462265481a2b
Reviewed-on: https://chromium-review.googlesource.com/525754
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Reviewed-by: Adam Klein <adamk@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/branch-heads/5.9@{#71}
Cr-Branched-From: fe9bb7e6e251159852770160cfb21dad3cf03523-refs/heads/5.9.211@{#1}
Cr-Branched-From: 70ad23791a21c0dd7ecef8d4d8dd30ff6fc291f6-refs/heads/master@{#44591}
[modify] https://crrev.com/e23b659865e16de9482e19732650d57b3ff0b374/src/wasm/module-decoder.cc


### cl...@chromium.org (2017-06-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-15)

Congratulations! The VRP Panel decided to award $4,000 for this report!

### sh...@chromium.org (2017-09-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-10-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-02-17)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-17)

This issue was migrated from crbug.com/chromium/729991?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087991)*
