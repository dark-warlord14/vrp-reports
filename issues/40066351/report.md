# memory corruption in MarkCompactCollector::ProcessMarkingWorklist(v8)

| Field | Value |
|-------|-------|
| **Issue ID** | [40066351](https://issues.chromium.org/issues/40066351) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2023-06-24 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:  

Ubuntu 22.04  

testde chromium version:  

Chromium 113.0.5624.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1111246.zip)  

Chromium 114.0.5688.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1124962.zip)  

Chromium 117.0.5850.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1161903.zip)

Repro steps:

1. python3 -m http.server 8000 --dir=|path|
2. ~/asan-linux-release/chrome --js-flags=--harmony-struct,--stress-incremental-marking --user-data-dir=/tmp/xx <http://localhost:8000/poc.html>

**Problem Description:**  

Note:

1. I found this issue while testing the patch for my previously submitted issue. Dinfuehr believed it to be a separate problem and asked me to create a new issue.  
   
   (<https://bugs.chromium.org/p/chromium/issues/detail?id=1450809#c20>)  
   
   I couldn't reproduce the heap-buffer-overflow again, but I was able to reproduce this problem.
2. According to testing, it is easy to repro using older versions of Chromium, but it's difficult to repro with the latest version, with a repro probability of less than 10%. The crash stack trace is almost the same between the old and new versions, and poc.html can be tested on the older version.  
   
   For example, versions like 113.0.5624.0 or 114.0.5688.0 can be easily reproduced.

**Additional Comments:**

\*\*Chrome version: \*\* 113.0.5624.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 246 B)
- [service-worker-test.js](attachments/service-worker-test.js) (text/plain, 467 B)
- [114.0.5688.0_asan.log](attachments/114.0.5688.0_asan.log) (text/plain, 5.4 KB)
- [117.0.5850.0_asan.log](attachments/117.0.5850.0_asan.log) (text/plain, 5.4 KB)
- [test.js](attachments/test.js) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2023-06-24)

[Empty comment from Monorail migration]

### ah...@google.com (2023-06-26)

Thanks for the report!

Setting severity to low similarly to https://crbug.com/chromium/1450809
Security_Impact-None since it's behind a feature flag.

I couldn't reproduce locally, dinfuehr@chromium.org could you please take a look?

Thanks

[Monorail components: Blink>JavaScript>GarbageCollection]

### di...@chromium.org (2023-06-27)

@pthier: Can you look at the stack trace linked in the other issue? (see https://bugs.chromium.org/p/chromium/issues/attachmentText?aid=601217). That one crashed in the string forwarding table. Maybe you have an idea what's going on.

The stacktrace here looks different though. I guess those are different issues again.

### di...@chromium.org (2023-06-27)

I was able to reproduce a crash with 114.0.5688.0 but that's not too surprising since there have been important bug fixes since then in e.g. 114.0.5700.0. We need this to reproduce on tip-of-tree. Otherwise I am wasting my time again with debugging bugs that have already been fixed. I can't reproduce yet and unfortunately the stack trace is too generic and doesn't help much. Without a working repro or some additional info this issue doesn't seem actionable.

### di...@chromium.org (2023-06-27)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-06-27)

This crash is indeed difficult to reproduce. I wrote a simple JavaScript code for automated testing with Puppeteer. It can be reproduced in about 2 minutes on my local machine. The path of chrome needs to be modified, and the number of browsers can also be modified according to the actual machine performance.
Can you try it? If it doesn't work, I have no other good solution for the time being.

- sudo apt-get install nodejs npm 
- sudo npm install -g puppeteer 
- node ./test.js 2>&1|grep -E 'Received'

tested version:
Chromium 116.0.5845.4(The latest dev version compiled by myself is more stable to reproduce crash.)
    is_asan = true
    is_debug = false
    enable_nacl = false
    treat_warnings_as_errors = false
    is_component_build=false
    dcheck_always_on = false

### di...@chromium.org (2023-06-28)

Thanks! I was able to reproduce this crash with that script.

### em...@gmail.com (2023-06-28)

Glad to hear you can reproduce.
BTW, after testing, this crash can be reproduced by using --shared-string-table alone (not considered experimental flag), so it should not be  "low".
thanks.

### di...@chromium.org (2023-06-28)

I have a CL here that should fix this issue. Can you check as well? https://chromium-review.googlesource.com/c/v8/v8/+/4650482

### em...@gmail.com (2023-06-28)

Thank you for the quick fix.
I tested for over half an hour, and the issue didn't repro again (before applying the patch, it could be reproduced within 2 minutes on my local pc).

### gi...@appspot.gserviceaccount.com (2023-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/046f74d2f08b8a8ae5c55fd032fe3ef8a9ae827c

commit 046f74d2f08b8a8ae5c55fd032fe3ef8a9ae827c
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Wed Jun 28 13:37:02 2023

[heap] Implement bailout for shared objects in unified GC

Client isolates should bail out of marking objects in the shared
heap, as such objects are always considered live in a local GC.

Bug: chromium:1457717
Change-Id: I92eb572bc2b714e086f1abbc607be3fc1d5d4f95
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4650482
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#88540}

[modify] https://crrev.com/046f74d2f08b8a8ae5c55fd032fe3ef8a9ae827c/src/heap/cppgc-js/unified-heap-marking-state-inl.h
[modify] https://crrev.com/046f74d2f08b8a8ae5c55fd032fe3ef8a9ae827c/src/heap/cppgc-js/unified-heap-marking-state.h
[modify] https://crrev.com/046f74d2f08b8a8ae5c55fd032fe3ef8a9ae827c/src/heap/cppgc-js/unified-heap-marking-state.cc
[modify] https://crrev.com/046f74d2f08b8a8ae5c55fd032fe3ef8a9ae827c/src/heap/mark-compact.cc
[modify] https://crrev.com/046f74d2f08b8a8ae5c55fd032fe3ef8a9ae827c/src/heap/concurrent-marking.cc


### gi...@appspot.gserviceaccount.com (2023-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/a6fe93b43d8e842f2b5ffd3e857723fdbfa6d958

commit a6fe93b43d8e842f2b5ffd3e857723fdbfa6d958
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Wed Jun 28 17:32:28 2023

[heap] Handle shared objects in traced handles conservative marking

Client isolates should bail out of marking objects in the shared
heap, as such objects are always considered live in a local GC.

Bug: chromium:1457717
Change-Id: If29d14029ce3a0884d7831fec9e88daa72a10bf6
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4650559
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#88541}

[modify] https://crrev.com/a6fe93b43d8e842f2b5ffd3e857723fdbfa6d958/src/heap/traced-handles-marking-visitor.h
[modify] https://crrev.com/a6fe93b43d8e842f2b5ffd3e857723fdbfa6d958/src/heap/traced-handles-marking-visitor.cc


### di...@chromium.org (2023-07-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-05)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-13)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-10-10)

This issue was migrated from crbug.com/chromium/1457717?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066351)*
