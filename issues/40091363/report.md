# [LangFuzz] Crash @ MarkCompactCollector::SweepSpaces() or SeqTwoByteString::SeqTwoByteStringReadBlockIntoBuffer() (64 bit)

| Field | Value |
|-------|-------|
| **Issue ID** | [40091363](https://issues.chromium.org/issues/40091363) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript, Internals |
| **Reporter** | de...@googlemail.com |
| **Assignee** | er...@gmail.com |
| **Created** | 2011-05-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached archive contains two testcases:

- The minimized testcase "min.js" crashes at v8::internal::MarkCompactCollector::SweepSpaces() when run with --expose\_gc in an optimized shell of the V8 version as in recent Chrome 12.
- A less reduced testcase (two files, "part1.js" + "part2.js") crashes at SeqTwoByteString::SeqTwoByteStringReadBlockIntoBuffer() instead.

I was not able to test it in Chrome 12 directly because I don't have a build available that has window.gc() but the V8 version used is exactly the one of Chrome 12.

To reproduce the crash, run the tests like this:

$ shell --expose\_gc min.js

$ shell --expose\_gc part1.js part2.js

**VERSION**  

Chrome Version: 12.0.742.68 (beta)  

Operating System: Linux  

Tested with V8 from <http://v8.googlecode.com/svn/branches/3.2@8043>

ADDITIONAL INFORMATION

Trace of the first test (min.js):

==11787== Invalid read of size 1  

==11787== at 0x4E4F1B: v8::internal::MarkCompactCollector::SweepSpaces() (in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==11787== by 0x4E6539: v8::internal::MarkCompactCollector::CollectGarbage() (in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==11787== by 0x47B925: v8::internal::Heap::MarkCompact(v8::internal::GCTracer\*) (in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==11787== by 0x4850CD: v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer\*) (in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==11787== by 0x485448: v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector) (in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==11787== by 0x485883: v8::internal::Heap::CollectAllGarbage(bool) (in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==11787== by 0x44957A: v8::internal::GCExtension::GC(v8::Arguments const&) (in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==11787== by 0x42F3D1: v8::internal::Builtin\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) (in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==11787== by 0x9F48341: ???  

==11787== by 0x9F6D842: ???  

==11787== by 0x9F6D611: ???  

==11787== by 0x9F6B3B7: ???  

==11787== Address 0x36 is not stack'd, malloc'd or (recently) free'd  

==11787==  

==11787==  

==11787== Process terminating with default action of signal 11 (SIGSEGV)

Trace of the second test (part1.js + part2.js):

==8671== Invalid read of size 2  

==8671== at 0x4E7A13: v8::internal::SeqTwoByteString::SeqTwoByteStringReadBlockIntoBuffer(v8::internal::String::ReadBlockBuffer\*, unsigned int\*, unsigned int) (in /scratch/holle  

r/LangFuzz/v8\_chrome12-64/shell)  

==8671== by 0x5009EC: v8::internal::String::ReadBlock(v8::internal::String\*, unsigned char\*, unsigned int, unsigned int\*, unsigned int\*) (in /scratch/holler/LangFuzz/v8\_chrome12  

-64/shell)  

==8671== by 0x4AC9AD: unibrow::InputBuffer<v8::internal::String, v8::internal::String\*, 1024u>::FillBuffer() (in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==8671== by 0x4F7DDD: v8::internal::String::Utf8Length() (in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==8671== by 0x421404: v8::String::Utf8Value::Utf8Value(v8::Handle[v8::Value](javascript:void(0);)) (in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==8671== by 0x403CAE: Print(v8::Arguments const&) (in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==8671== by 0x42F3D1: v8::internal::Builtin\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*)  

(in /scratch/holler/LangFuzz/v8\_chrome12-64/shell)  

==8671== by 0x9F48341: ???  

==8671== by 0x9F70B7E: ???  

==8671== by 0x9F6F377: ???  

==8671== by 0x9F6DBE7: ???  

==8671== by 0x9F494A2: ???  

==8671== Address 0x418c000 is not stack'd, malloc'd or (recently) free'd  

==8671==  

==8671==  

==8671== Process terminating with default action of signal 11 (SIGSEGV)

## Attachments

- [testSweepSpaces.tgz](attachments/testSweepSpaces.tgz) (application/x-gzip; charset=binary, 6.1 KB)

## Timeline

### in...@chromium.org (2011-05-27)

Mads, can you please help to triage.

### ag...@chromium.org (2011-05-30)

[Empty comment from Monorail migration]

### ag...@chromium.org (2011-05-30)

[Empty comment from Monorail migration]

### er...@gmail.com (2011-06-01)

Stealing this

### sc...@gmail.com (2011-06-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-04)

Fixed and merged to M12, M13 by Erik.

### sc...@gmail.com (2011-06-04)

@decoder.oh: thanks for the report! We're delighted to offer a provisional $1000 Chromium Security Reward.

We've fixed it already and should get the fix out shortly.
We'll look into your other report soon to so if it is the same root issue or something different.

@erik.corry and @decoder.oh: I don't suppose either you have an idea of whether Chrome 11 is affected or not or whether this was a regression on the Chrome 12 branch?

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### er...@gmail.com (2011-06-04)

Chrome 11 is definitely not affected. The bug was in an optimization
targeted at the jslint benchmark.  Chrome11 does not have the optimization.

directly

### sc...@gmail.com (2011-06-04)

Thanks Erik!
And thank you @decoder.oh for catching that regression before we shipped it to stable!

### sk...@chromium.org (2011-06-06)

Fix: http://code.google.com/p/v8/source/detail?r=8166

### sc...@gmail.com (2011-06-09)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/84234?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript, Internals]
[Monorail mergedwith: crbug.com/chromium/84370]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091363)*
