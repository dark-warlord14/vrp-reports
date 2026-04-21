# Security: use-after-free/data-race (in off-by-default JavaScriptExperimentalSharedMemory feature)

| Field | Value |
|-------|-------|
| **Issue ID** | [40066213](https://issues.chromium.org/issues/40066213) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | kv...@googlecontrib.kvakil.me |
| **Assignee** | pt...@chromium.org |
| **Created** | 2023-06-22 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

When the (off-by-default) JavaScriptExperimentalSharedMemory feature is enabled, the V8 flag --shared-string-table is enabled. When this V8 flag is enabled, concurrent string externalization in V8 can lead to use-after-free issues and data races.

**VERSION**  

Chrome Version: believed in stable, see below  

Operating System: Linux

**REPRODUCTION CASE**

I don't have a reproduction case against Chrome. I'll give the details assuming you have a V8 build. I believe these details could be used to

1. Check out V8 ToT (currently d1aa68564201fe9e941e4ab7461ae09c45e5ba2d).
2. Apply the following patch locally which makes reproduction more reliable:

```
diff --git a/src/objects/string.cc b/src/objects/string.cc  
index cd47d81c06..7a686a0243 100644  
--- a/src/objects/string.cc  
+++ b/src/objects/string.cc  
@@ -477,8 +477,10 @@ bool String::MakeExternal(v8::String::ExternalOneByteStringResource\* resource) {  
   
   // Externalizing twice leaks the external resource, so it's  
   // prohibited by the API.  
-  DCHECK(  
-      this->SupportsExternalization(v8::String::Encoding::ONE_BYTE_ENCODING));  
+  for (int i = 0; i < 20; i++) {  
+    CHECK(  
+        this->SupportsExternalization(v8::String::Encoding::ONE_BYTE_ENCODING));  
+  }  
   DCHECK(resource->IsCacheable());  
 #ifdef ENABLE_SLOW_DCHECKS  
   if (v8_flags.enable_slow_asserts) {  

```

3. Compile with the following out/x64.release/args.gn:

```
is_tsan = true  
is_component_build = false  
is_debug = false  
target_cpu = "x64"  
#  
# probably not important for repro:  
v8_enable_sandbox = true  
use_goma = false  
v8_enable_backtrace = true  
v8_enable_disassembler = true  
v8_enable_object_print = true  
v8_enable_verify_heap = true  
dcheck_always_on = false  

```

4. To reproduce the data race (attached as data-race.txt), run the following. Note this uses test/mjsunit/regress/regress-crbug-1394741.js which already exists in the V8 repo. On my system it reproduces after around 1000 executions.

```
tools/run-tests.py --outdir=out/x64.release --variants=stress --random-seed-stress-count=1000000 --total-timeout-sec=120 --exit-after-n-failures=1 --isolates mjsunit/regress/regress-crbug-1394741  

```

This data race occurs because concurrent externalization can cause data races in v8::internal::Heap::ExternalStringTable::AddString. v8::String::MakeExternal grabs the internalized\_string\_access mutex on the isolate, which incidentally serializes accesses to the external string table. But as you can see there are other code paths which invoke RegisterExternalString directly which can race with it. As another example, v8::String::NewExternalOneByte on the public API invokes v8::internal::Factory::NewExternalStringFromOneByte which doesn't grab this mutex. This leads to two threads modifying the vector at once.

5. To reproduce the use-after-free (attached as uaf.txt), you basically just need to run the same test a bunch of times in parallel. I have a pretty beefy system, so 500 tests in parallel is the magic number for me:

```
for j in {1..10}; do  
  for i in {1..500}; do  
    out/x64.release/d8 --test test/mjsunit/mjsunit.js test/mjsunit/regress/regress-crbug-1394741.js --isolate test/mjsunit/mjsunit.js test/mjsunit/regress/regress-crbug-1394741.js --nohard-abort --testing-d8-test-runner --stress-incremental-marking --expose-gc --expose-externalize-string --shared-string-table >/dev/null &  
  done |& tee -a logs  
  wait  
done  

```

**CREDIT INFORMATION**  

Reporter credit: Keyhan Vakil

## Attachments

- [uaf.txt](attachments/uaf.txt) (text/plain, 17.0 KB)
- [data-race.txt](attachments/data-race.txt) (text/plain, 11.2 KB)

## Timeline

### [Deleted User] (2023-06-22)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-06-22)

Over to the current V8 shepherd. Setting impact none since it is behind an experimental flag.

[Monorail components: Blink>JavaScript]

### is...@chromium.org (2023-06-23)

[Empty comment from Monorail migration]

### pt...@chromium.org (2023-06-23)

[Empty comment from Monorail migration]

### kv...@googlecontrib.kvakil.me (2023-06-23)

The data race I think only occurs in this particular code path because there's an unprotected call to factory->NewExternalOneByteString in the CompileExtension function. Every other call is properly protected. I will put up a CL to fix by changing to v8::String::NewExternalOneByte.

Still not sure about the UAF. Also I was able to reproduce it more easily after fixing the data race issue and then just using the test runner to perform 10000 runs. (I'm running tsan 10,000 times here because I'm trying to change something & don't want to break anything.)

### pt...@chromium.org (2023-06-23)

Thanks for the report and your update.
We think that the UAF has the same root cause as the data race (due to the data race in push_back, the vector gets corrupted, which results in the UAF issue).
We were not able to reproduce it after the data race was fixed (locally), which we did by protecting Heap::RegisterExternalString in general and not just v8::String::NewExternalOneByte.
If you are still able to repro the UAF, we would be happy to get more details. We were unable to capture a rr trace or similar to verify our assumption, but the stack traces we saw suggested that the std::vector was corrupted.

### kv...@googlecontrib.kvakil.me (2023-06-25)

Sorry, I missed your earlier reply. Yes, I think you're right that the UAF no longer reproduces once the data race is fixed. I agree that the right solution needs to protect Heap::RegisterExternalString.

Here's a CL to fix + test: https://chromium-review.googlesource.com/c/v8/v8/+/4643869 , but it sounds like you might have a better solution in the works.

### di...@chromium.org (2023-06-27)

This issue doesn't affect production as it requires --shared-string-table (which isn't enabled by default) but also --expose-gc (which is used for testing).

### gi...@appspot.gserviceaccount.com (2023-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/9b14eaef2380a3cd24676690e04c980bacf70cf1

commit 9b14eaef2380a3cd24676690e04c980bacf70cf1
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Tue Jun 27 16:56:45 2023

[heap] Protect external string table of the shared space isolate

The external string table of the shared space isolate is used from
client isolates as well and thus needs to be protected. While
String::MakeExternal already protected access to the external string
table, e.g. --expose-gc would go through a different code path
where synchronization was missing (Factory::NewExternalOneByteString).

This CL adds synchronization to the ExternalStringTable::AddString
method.

Bug: chromium:1457095
Change-Id: I432d87837107a721b66ee2dacc97c42e04c9f46f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4643049
Reviewed-by: Patrick Thier <pthier@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#88525}

[modify] https://crrev.com/9b14eaef2380a3cd24676690e04c980bacf70cf1/src/objects/string.cc
[modify] https://crrev.com/9b14eaef2380a3cd24676690e04c980bacf70cf1/test/cctest/test-shared-strings.cc
[modify] https://crrev.com/9b14eaef2380a3cd24676690e04c980bacf70cf1/src/heap/heap.h
[modify] https://crrev.com/9b14eaef2380a3cd24676690e04c980bacf70cf1/src/heap/heap-inl.h


### di...@chromium.org (2023-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-07)

[Empty comment from Monorail migration]

### kv...@googlecontrib.kvakil.me (2023-07-08)

I think technically we need to grab the lock in Heap::VisitExternalResources too (exposed to the API via v8::Isolate::VisitExternalResources). Looks like the last use in Chromium was removed long ago (https://source.chromium.org/chromium/chromium/src/+/c0744bf02879b407753fe209cb7fdb3a7adfa914), so maybe removing the API could work too.

### pt...@chromium.org (2023-07-12)

You are right. This API is unused and we can/should remove it.
I created a new tracking bug to remove it (since this requires multiple steps over different releases): https://crbug.com/v8/14172

### am...@google.com (2023-07-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-19)

Congratulations, Keyhan! The VRP Panel has decided to award you $10,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- great work and nice report! 

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-10-13)

This issue was migrated from crbug.com/chromium/1457095?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066213)*
