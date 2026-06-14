# Sandbox IPC  out-of-bounds write in CrossCallParamsEx::CreateFromBuffer

| Field | Value |
|-------|-------|
| **Issue ID** | [40082774](https://issues.chromium.org/issues/40082774) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | cp...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2010-08-19 |
| **Bounty** | $1,000.00 |

## Description

It is a variation of https://crbug.com/chromium/32915 which we overlooked at that time.

Credits to Adobe's security team for the find.

In crosscall_server.cc CrossCallParamsEx::CreateFromBuffer


GetActualBufferSize(param_count, buffer_base) returns an untrusted value which we check to be not too big and not zero, but it can be set to a small value.

This causes problems because we overlay (via placement new) an object of type CrossCallParamsEx on memory of a size that can be smaller than sizeof(CrossCallParamsEx).

Then 1) the default ctor of CrossCallParamsEx will write zeros outside the allocated memory, corrupting nearby heap allocation.

In all likelihood the set of tests in the following loop fail and cause the early exit.

for (size_t ix =0; ix != param_count; ++ix) {
  address = copied_params->GetRawParameter(..)
  if ((address < ..) ||
      (address > ..) ... || ..) {
     // Malformed
     return NULL;
  }
}

The belief here is based on the fact that GetRawParameter(..) now points to random memory on the heap that is not *directly* attacker controlled. So whatever this memory is needs to 1) make some sense and 2) be useful for an attack.

Seems hard but we have seem crazy feats, in particular the heap might contain previous IPC values.








## Timeline

### sc...@gmail.com (2010-08-19)

[Empty comment from Monorail migration]

### ke...@chromium.org (2010-08-19)

How long on a fix for the branch? 

### bu...@gmail.com (2010-08-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=56796 

------------------------------------------------------------------------
r56796 | cpu@chromium.org | 2010-08-19 18:06:17 -0700 (Thu, 19 Aug 2010) | 7 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/src/crosscall_params.h?r1=56796&r2=56795
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/src/crosscall_server.cc?r1=56796&r2=56795
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/src/ipc_unittest.cc?r1=56796&r2=56795

Sbox IPC fix

BUG=52682
TEST=included


Review URL: http://codereview.chromium.org/3142022
------------------------------------------------------------------------


### bu...@gmail.com (2010-08-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=56798 

------------------------------------------------------------------------
r56798 | cpu@chromium.org | 2010-08-19 18:27:20 -0700 (Thu, 19 Aug 2010) | 12 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/src/crosscall_params.h?r1=56798&r2=56797
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/src/crosscall_server.cc?r1=56798&r2=56797
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/src/ipc_unittest.cc?r1=56798&r2=56797

Revert 56796 - Sbox IPC fix

Tests failing on vista 

BUG=52682
TEST=included


Review URL: http://codereview.chromium.org/3142022

TBR=cpu@chromium.org
Review URL: http://codereview.chromium.org/3122031
------------------------------------------------------------------------


### bu...@gmail.com (2010-08-20)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=56938 

------------------------------------------------------------------------
r56938 | cpu@chromium.org | 2010-08-20 16:31:45 -0700 (Fri, 20 Aug 2010) | 11 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/src/crosscall_params.h?r1=56938&r2=56937
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/src/crosscall_server.cc?r1=56938&r2=56937
   M http://src.chromium.org/viewvc/chrome/trunk/src/sandbox/src/ipc_unittest.cc?r1=56938&r2=56937

Sbox IPC fix

Second take, I had off-by-one bad check in line 164

for more info see review 3142022

BUG=52682
TEST=included


Review URL: http://codereview.chromium.org/3130037
------------------------------------------------------------------------


### bu...@gmail.com (2010-08-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=56972 

------------------------------------------------------------------------
r56972 | mal@chromium.org | 2010-08-20 19:33:51 -0700 (Fri, 20 Aug 2010) | 14 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/472/src/sandbox/src/crosscall_params.h?r1=56972&r2=56971
   M http://src.chromium.org/viewvc/chrome/branches/472/src/sandbox/src/crosscall_server.cc?r1=56972&r2=56971
   M http://src.chromium.org/viewvc/chrome/branches/472/src/sandbox/src/ipc_unittest.cc?r1=56972&r2=56971

Merge 56938 - Sbox IPC fix

Second take, I had off-by-one bad check in line 164

for more info see review 3142022

BUG=52682
TEST=included


Review URL: http://codereview.chromium.org/3130037

TBR=cpu@chromium.org
Review URL: http://codereview.chromium.org/3135041
------------------------------------------------------------------------


### ma...@google.com (2010-08-21)

Fix is on the Chrome 6 branch now.

### in...@chromium.org (2010-08-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-08-23)

Thanks all for getting this fixed so quickly.

### sc...@gmail.com (2010-08-25)

Copying in the original high-quality report:
---

Bug Title: Exploitable write buffer overflow while handling a cross-call in CrossCallParamsEx::CreateFromBuffer( ); this can potentially be used to escape the sandbox.


Description:
There is insufficient validation of the cross-call parameters in CrossCallParamsEx::CreateFromBuffer() [src\sandbox\src\crosscall_server.cc] that allows the sandbox to cause a heap buffer overflow in the broker. This may be used to escape the sandbox by corrupting adjoining heap memory.

The bug is in the following section of the code:
   actual_size = GetActualBufferSize(param_count, buffer_base);
   if ((actual_size > buffer_size) || (0 == actual_size)) {
     // It is too big or too many declared parameters.
     return NULL;
   }
   // Now we copy the actual amount of the message.
   actual_size += sizeof(ParamInfo);  // To get the last offset.
   *output_size = actual_size;
   backing_mem = new char[actual_size];
   memset(backing_mem, 0, actual_size);
   copied_params = new(backing_mem)CrossCallParamsEx();

GetActualBufferSize() returns param_info_[NUMBER_PARAMS].offset_ (which is attacker controlled) and can be some small value like 1. After adding 0xc bytes for ParamInfo, actual_size = 0xd. The allocated backing_mem is of this size.
Calling the placement new constructor CrossCallParamsEx( ) [which is of size 0x4c] will overwrite past the allocated size (0xd) into offset 0x3C etc.
In case this causes an access-violation, the __except( ) would catch it. More serious would be the corruption of adjoining memory areas, which could help an exploit running in the sandbox in getting additional access and/or breaking out of the sandbox.

More details
------------
(Note that the traces are from our private builds and may differ)

faulting instruction:
eax=00000000 ebx=03570134 ecx=00000000 edx=00000000 esi=0304bff0 edi=0000000d
eip=00420fe1 esp=03bafbf8 ebp=03bafc34 iopl=0         nv up ei pl nz na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010206
sandbox::CrossCallParamsEx::CreateFromBuffer+0xc1:
00420fe1 89463c          mov     dword ptr [esi+3Ch],eax ds:0023:0304c02c=????????

backtrace:
ChildEBP RetAddr  Args to Child
03bafc34 0041c383 03570134 00020000 03bafd94 sandbox::CrossCallParamsEx::CreateFromBuffer+0xc1
03bafd9c 0041c5e1 034f6fd8 03570134 03bafe54 sandbox::SharedMemIPCServer::InvokeCallback+0x33
03bafe8c 7c927e91 034f6fd8 031a8f00 031a8fc0 sandbox::SharedMemIPCServer::ThreadPingEventReady+0xf1

!exploitable output:
"Exploitable - User Mode Write AV starting at sandbox::CrossCallParamsEx::CreateFromBuffer+0x00000000000000c1 (Hash=0x6e243d59.0x19765f60)".

### sc...@gmail.com (2010-08-26)

This qualifies for a $1000 Chromium Security Reward because of the severity (high) and great detail in the e-mail report.
The original reporters of the bug are not on the cc: so I'll tell them on the e-mail thread.

### sc...@gmail.com (2010-09-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-02)

Ashutosh's half of the payment is in the electronic system.

### sc...@gmail.com (2010-12-20)

Vineet's half of the payment is in the electronic system. Marking this bug as fully paid.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

This issue was migrated from crbug.com/chromium/52682?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082774)*
