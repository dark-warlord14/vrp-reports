# UNKNOWN in v8::internal::MarkCompactCollector::PrepareThreadForCodeFlushing

| Field | Value |
|-------|-------|
| **Issue ID** | [40057135](https://issues.chromium.org/issues/40057135) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ms...@chromium.org |
| **Created** | 2012-04-22 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes the D8 shell (version as in Chrome 20.0.1105.0 dev, rev 11316) in function v8::internal::Marking::MarkBitFrom with an invalid read from a non-null address (0x100000018).

**VERSION**  

Chrome Version: 20.0.1105.0 dev  

Operating System: Ubuntu 11.10 64 bit

Note: I was not able to test this in the specified Chrome revision itself because I don't have a debug build available that supports --expose\_gc for testing. However, the D8 revision used is exactly that in the given Chrome version.

**REPRODUCTION CASE**  

function f(x, y) {  

if (x == 149999) {  

x+'';  

gc();  

}  

}  

for (var i = 0; i < 150000; i++) {  

new f(i);  

}

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

Trace from D8 with Valgrind:

==5979== Invalid read of size 8  

==5979== at 0x52D830: v8::internal::Marking::MarkBitFrom(unsigned char\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5979== by 0x537B2D: v8::internal::MarkCompactCollector::PrepareThreadForCodeFlushing(v8::internal::Isolate\*, v8::internal::ThreadLocalTop\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5979== by 0x539E44: v8::internal::MarkCompactCollector::PrepareForCodeFlushing() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5979== by 0x53A024: v8::internal::MarkCompactCollector::MarkLiveObjects() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5979== by 0x53EAB8: v8::internal::MarkCompactCollector::CollectGarbage() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5979== by 0x4ABF17: v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5979== by 0x4AC733: v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector, char const\*, char const\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5979== by 0x4ACF5A: v8::internal::Heap::CollectAllGarbage(int, char const\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5979== by 0x46DC41: v8::internal::GCExtension::GC(v8::Arguments const&) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5979== by 0x43DBED: v8::internal::Builtin\_HandleApiCall(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==5979== by 0xCDFC4906361: ???  

==5979== by 0xCDFC493D484: ???  

==5979== Address 0x100000018 is not stack'd, malloc'd or (recently) free'd  

==5979==

## Timeline

### in...@chromium.org (2012-04-23)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-04-24)

Giving to Michael to take a look.

### ms...@chromium.org (2012-04-25)

Fixed on V8 bleeding edge. Will merge to 3.9 branch which is also affected. Analysis coming up.

http://code.google.com/p/v8/source/detail?r=11436

### in...@chromium.org (2012-04-25)

Sheriff, please triage and help to add the milestone, secimpacts tags.

### ke...@chromium.org (2012-04-25)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-04-25)

@mstarzinger: Do you know what kind of crash this is? ASAN is not diagnosing it very well, so I'm not clear if it's an OOB read or a use-after-free. It doesn't easily repro locally for me so it's hard to assess security severity.

### ke...@chromium.org (2012-04-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=38364512

Uploader: kenrb@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x000100000068
Crash State:
  - crash stack -
  v8::internal::MarkCompactCollector::PrepareThreadForCodeFlushing
  v8::internal::MarkCompactCollector::PrepareForCodeFlushing
  v8::internal::MarkCompactCollector::MarkLiveObjects
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=130896:130956

Minimized Testcase (0.14 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96NsFNsWJF01duHSgdbKr3GP7M9ptmhkafmhaWf2nKgEhAP5TGzSwTMCoF_WejznWt-Irh4DiNOFUfCS3eVLtxfrDqmix1yqhAvTAE-sfd0fepJ7YUt7mYbAmrGyB7NSvTIwLg4PSQ4WuA4sHT4FwLqOPRx7A
<script>
function f(x, y) {
  if (x == 149999) { 
        x+''; 
        gc(); 
  }
}
for (var i = 0; i < 150000; i++) {
  new f(i);
}
</script>

### kc...@chromium.org (2012-04-26)

>>  Do you know what kind of crash this is?

The address 0x000100000068 is 2^32 + 0x68
Both valgrind and asan have no clue about the address,
so this is a *wild* dereference, probably caused by integer overflow. 

### sc...@gmail.com (2012-04-26)

I'd guess a type confusion. Looks like a structured few bytes that are clearly not a pointer.

### sc...@gmail.com (2012-04-26)

[Empty comment from Monorail migration]

### ms...@chromium.org (2012-04-26)

Here is an analysis (which should answer https://crbug.com/chromium/124594#c6):

One type of stack-frame generated by the deoptimizer was missing a reference. Hence the stack-slot containing the arguments count (as tagged SMI) was treated as a reference. Taking our limits into account this leads to the following situation. On ia32/ARM it is possible to manipulate bits in the address range from 0x0 to 0x8080 where the offset is controlled by the number of arguments of the inlined function. On x64 it is possible to manipulate bits at (n < 32) + 0x68 where n is the number of arguments of the inlined function. And "manipulating a bit" in this setting means, first reading it, then potentially flipping it on.

IMHO, on ia32 the situation seems harmless, whereas on x64 it becomes tricky. But I am no security expert.

### cl...@chromium.org (2012-04-26)

ClusterFuzz has detected this issue as fixed in range 134088:134098.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=38364512

Uploader: kenrb@chromium.org

Crash Type: UNKNOWN
Crash Address: 0x000100000068
Crash State:
  - crash stack -
  v8::internal::MarkCompactCollector::PrepareThreadForCodeFlushing
  v8::internal::MarkCompactCollector::PrepareForCodeFlushing
  v8::internal::MarkCompactCollector::MarkLiveObjects
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=130896:130956
Fixed: https://cluster-fuzz.appspot.com/revisions?range=134088:134098

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96NsFNsWJF01duHSgdbKr3GP7M9ptmhkafmhaWf2nKgEhAP5TGzSwTMCoF_WejznWt-Irh4DiNOFUfCS3eVLtxfrDqmix1yqhAvTAE-sfd0fepJ7YUt7mYbAmrGyB7NSvTIwLg4PSQ4WuA4sHT4FwLqOPRx7A

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ke...@chromium.org (2012-04-26)

Thanks for the analysis Michael.

### sc...@gmail.com (2012-05-04)

I'm confused by the expression "(n < 32) + 0x68" above for the 64-bit case.

Taken literally, "(n < 32)" will result in 0 or 1, leading to a harmless dereference address of 0x68 or 0x69

If perhaps "(n << 32)" was meant, then it does seem non-harmless, but statistically unlikely that any of the attacker's options will hit a mapped address (even with a heap spray). Medium would be appropriate in this case.

Stripped tags until we get confirmation on the expression.

### ms...@chromium.org (2012-05-04)

Sorry for the confusion, the expression should have been "(n << 32) + 0x68". So a left shift by 32bit and then adding a fixed offset. That's the situation on x64 only.

### sc...@gmail.com (2012-05-04)

Thanks! Putting back medium :) Setting OS-Linux since that's our only 64-bit option.

### sc...@gmail.com (2012-05-04)

Thanks decoder! $500 for this one. It's a memory corruption but with a very significant constraint.

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

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

This issue was migrated from crbug.com/chromium/124594?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail mergedwith: crbug.com/chromium/125425]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057135)*
