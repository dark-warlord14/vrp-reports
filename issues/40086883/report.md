# Security: type confusion in JSPropGetter of pdfium 

| Field | Value |
|-------|-------|
| **Issue ID** | [40086883](https://issues.chromium.org/issues/40086883) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | hi...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2017-02-24 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

embed the following simple JavaScript into a PDF  

var obj = new this.constructor;  

obj.author=3;  

open it in Chrome, you'll see the crashed pdfviewer plugin

the constructor of the document object(or app,console,global etc) should not been exported to user JavaScript. when an object is created with these constructors, the internal fields of the objects is not initialized, call any access property will cause a type confusion. the crash is as follows:  

Program received signal SIGSEGV, Segmentation fault.  

0x000000000078c8f5 in std::unique\_ptr<CJS\_EmbedObj, std::default\_delete<CJS\_EmbedObj> >::get (this=0xe97ff80000000008)  

at ../../build/linux/debian\_wheezy\_amd64-sysroot/usr/lib/gcc/x86\_64-linux-gnu/4.6/../../../../include/c++/4.6/bits/unique\_ptr.h:217  

217 { return std::get<0>(\_M\_t); }  

(gdb) bt  

#0 0x000000000078c8f5 in std::unique\_ptr<CJS\_EmbedObj, std::default\_delete<CJS\_EmbedObj> >::get (this=0xe97ff80000000008)  

at ../../build/linux/debian\_wheezy\_amd64-sysroot/usr/lib/gcc/x86\_64-linux-gnu/4.6/../../../../include/c++/4.6/bits/unique\_ptr.h:217  

#1 0x000000000078c719 in CJS\_Object::GetEmbedObject (this=0xe97ff80000000000) at ../../third\_party/pdfium/fpdfsdk/javascript/JS\_Object.h:47  

#2 0x00000000007c111b in JSPropGetter<Document, &Document::author> (prop\_name\_string=0x91ad23 "author", class\_name\_string=0x91ad1a "Document", property=..., info=...)  

at ../../third\_party/pdfium/fpdfsdk/javascript/JS\_Define.h:84  

#3 0x00000000007bcf41 in CJS\_Document::get\_author\_static (property=..., info=...) at ../../third\_party/pdfium/fpdfsdk/javascript/Document.h:306  

#4 0x00007ffff747d46d in v8::internal::PropertyCallbackArguments::Call (this=<optimized out>, f=<optimized out>, name=...) at ../../v8/src/api-arguments-inl.h:32  

#5 0x00007ffff7529de7 in v8::internal::Object::GetPropertyWithAccessor (it=<optimized out>) at ../../v8/src/objects.cc:1353  

#6 0x00007ffff7529079 in v8::internal::Object::GetProperty (it=<optimized out>) at ../../v8/src/objects.cc:999  

#7 0x00007ffff7465c93 in v8::internal::LoadIC::Load (this=<optimized out>, object=..., name=...) at ../../v8/src/ic/ic.cc:644  

#8 0x00007ffff7472c37 in v8::internal::\_\_RT\_impl\_Runtime\_LoadIC\_Miss (args=..., isolate=<optimized out>) at ../../v8/src/ic/ic.cc:2615  

#9 0x00007ffff747280a in v8::internal::Runtime\_LoadIC\_Miss (args\_length=<optimized out>, args\_object=<optimized out>, isolate=<optimized out>)  

at ../../v8/src/ic/ic.cc:2598

a poc is attached as poc1.pdf

**VERSION**  

Chrome Version: [56.0.2924.87] + [stable]  

Operating System: [any]

## Attachments

- [poc1.pdf](attachments/poc1.pdf) (application/pdf, 948 B)

## Timeline

### ke...@chromium.org (2017-02-24)

jochen@, can you please take a look at this as it is V8 and PDFium? Also can you triage as I am not sure what the implication of a type confusion here is?

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2017-02-24)

CL up at https://pdfium-review.googlesource.com/2839, which fixes the initialization issue.  Hiding the constructor seems more difficult.

### ts...@chromium.org (2017-02-24)

Probably sev high, bad address is uninitialized, and attacker may have some control over it via spraying, etc.

### sh...@chromium.org (2017-02-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2017-02-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2017-02-27)

CL landed, but over to jochen to check.

### bu...@chromium.org (2017-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4d175c2a5ab773d3d65acdf915149bef17ef2371

commit 4d175c2a5ab773d3d65acdf915149bef17ef2371
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Mon Feb 27 21:22:29 2017

Roll src/third_party/pdfium/ 73c9f3bb3..9162ff85c (2 commits).

https://pdfium.googlesource.com/pdfium.git/+log/73c9f3bb3d82..9162ff85c323

$ git log 73c9f3bb3..9162ff85c --date=short --no-merges --format='%ad %ae %s'
2017-02-24 thestig Fix nits from commit db764708.
2017-02-24 tsepez Fix uninitialized memory read in CJS_Object::GetEmbedObject()

Created with:
  roll-dep src/third_party/pdfium
BUG=695826

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2720883002
Cr-Commit-Position: refs/heads/master@{#453341}

[modify] https://crrev.com/4d175c2a5ab773d3d65acdf915149bef17ef2371/DEPS


### th...@chromium.org (2017-02-27)

We should merge to M57 once we verify the fix.

### jo...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-14)

tsepez: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2017-03-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-14)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-03-14)

+  awhalley@ for M57 merge review. Please note M57 is already in stable and we're only taking critical and safe merges in. Thank you.

### aw...@google.com (2017-03-14)

There might be a 57 spin early next week, at which point this will have had the required 48 hours in Beta for a stable merge and we should take it.

Note *please* mark bugs as fixed when the fix lands - otherwise it gets missed in the queries that help ensure security bugs get merged as needed.  Thanks! 

### hi...@gmail.com (2017-03-15)

There is another security bug labeled with M-57, Maybe you should consider it too.
https://bugs.chromium.org/p/chromium/issues/detail?id=695830

### sh...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-21)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-22)

govind@ - good for 57

### am...@chromium.org (2017-03-22)

Approved for 57.  We're cutting our next candidate in a couple hours, please merge immediately.

### aw...@google.com (2017-03-22)

Unfortunately this didn't merge cleanly and the trybots were having problems (though it built locally) - not picking up in 57 out of an abundance of caution.

### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-31)

Nice one! The panel decided to award $3,000 for this bug - cheers!

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/695826?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086883)*
