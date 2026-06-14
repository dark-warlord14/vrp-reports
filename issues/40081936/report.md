# Apple OS X Yosemite 10.10.2 IOAccelSurface2::set_id_mode OOB read on IOAccelMachine2 from KEEN Team

| Field | Value |
|-------|-------|
| **Issue ID** | [40081936](https://issues.chromium.org/issues/40081936) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Mac |
| **CVE IDs** | CVE-2015-3705 |
| **Reporter** | sc...@gmail.com |
| **Assignee** | ia...@chromium.org |
| **Created** | 2015-04-25 |
| **Bounty** | $5,000.00 |

## Description

[Chromium bug variant of https://code.google.com/p/google-security-research/issues/detail?id=346 for reward consideration as an OS-level sandbox escape]

---
Credit is to KEEN Team.

This vulnerability can be triggered via Safari/Chrome sandbox context.
In function IOAccelSurface2::set_id_mode, which specific arguments, the function IOAccelSurface2::prune_buffers can be reached.
In function IOAccelSurface2::prune_buffers, the following code can be reached:
          v16 = *(_QWORD *)(this + 4912);
          if ( *(_BYTE *)(v1 + 4565) )
        v17 = IOAccelDisplayMachine2::getScanoutResource(v16, *(_DWORD *)(v1 + 4576), 0);
      else
        LODWORD(v17) = IOAccelDisplayMachine2::getFramebufferResource(
                         (IOAccelDisplayMachine2 *)v16,
                         *(_DWORD *)(v1 + 4568),
                         0);
      IOAccelSurface2::attach_buffer_at_index((IOAccelSurface2 *)v1, 0, (IOAccelResource2 *)v17);
Here v16 is IOAccelMachine2 object which is allocated when system is boot. *(_DWORD *)(v1 + 4568) is assigned as value 0xffff.
And in IOAccelDisplayMachine2::getScanoutResource, it tried to obtain the QWORD at IOAccelMachine2 + 0xffff * 8 + 136, which is OOB access.
__int64 __fastcall IOAccelDisplayMachine2::getScanoutResource(__int64 this, unsigned int a2, unsigned int a3)
{
  return IOAccelDisplayPipe2::getScanoutResource(*(IOAccelDisplayPipe2 **)(this + 8LL * a2 + 136), a3);
}
Because IOAccelMachine2 object is allocated during system boot phase, the value at IOAccelMachine2 + 0xffff * 8 + 136 is hard to control by crafting memory layout.
However it still has possibility to control it, in my case, the crash log indicated that the value can be controlled:
panic(cpu 0 caller 0xffffff800de1a46e): Kernel trap at 0xffffff7f8feeeb76, type 13=general protection, registers:
RAX: 0x0000000000000000, RBX: 0x0000000000000000, RCX: 0x0000000000000009, RDX: 0x0000000000000000
RSP: 0xffffff811945ba50, RBP: 0xffffff811945ba50, RSI: 0x0000000000000000, RDI: 0x4141414141414141
R8:  0x0000000fa0000000, R9:  0x0000000010000000, R10: 0xffffff80204f1f00, R11: 0x0000000000000000
R12: 0xffffff80232871e8, R13: 0x0000000000478014, R14: 0xffffff8023286000, R15: 0x0000000000000000
RFL: 0x0000000000010246, RIP: 0xffffff7f8feeeb76, CS:  0x0000000000000008, SS:  0x0000000000000010
Fault CR2: 0x00007fff570b37f0, Error code: 0x0000000000000000, Fault CPU: 0x0

Backtrace (CPU 0), Frame : Return Address
0xffffff80efd1dc70 : 0xffffff800dd2fe41 mach_kernel : _panic + 0xd1
0xffffff80efd1dcf0 : 0xffffff800de1a46e mach_kernel : _kernel_trap + 0x85e
0xffffff80efd1deb0 : 0xffffff800de36683 mach_kernel : _return_from_trap + 0xe3
0xffffff80efd1ded0 : 0xffffff7f8feeeb76 com.apple.iokit.IOAcceleratorFamily2 : __ZN19IOAccelDisplayPipe218getScanoutResourceEj + 0x6
0xffffff811945ba50 : 0xffffff7f8fee2413 com.apple.iokit.IOAcceleratorFamily2 : __ZN15IOAccelSurface213prune_buffersEv + 0x1b1
0xffffff811945ba90 : 0xffffff7f8fee06a0 com.apple.iokit.IOAcceleratorFamily2 : __ZN15IOAccelSurface211set_id_modeEjj + 0x412
0xffffff811945bad0 : 0xffffff800e2ff00c mach_kernel : _shim_io_connect_method_scalarI_scalarO + 0x24c
0xffffff811945bb60 : 0xffffff800e301163 mach_kernel : __ZN12IOUserClient14externalMethodEjP25IOExternalMethodArgumentsP24IOExternalMethodDispatchP8OSObjectPv + 0x263
0xffffff811945bbc0 : 0xffffff800e2fe9c3 mach_kernel : _is_io_connect_method + 0x1f3
0xffffff811945bd00 : 0xffffff800dde4a87 mach_kernel : _iokit_server + 0x2477
0xffffff811945be10 : 0xffffff800dd33f8c mach_kernel : _ipc_kobject_server + 0xfc
0xffffff811945be40 : 0xffffff800dd18a93 mach_kernel : _ipc_kmsg_send + 0x123
0xffffff811945be90 : 0xffffff800dd293bd mach_kernel : _mach_msg_overwrite_trap + 0xcd
0xffffff811945bf10 : 0xffffff800de059fa mach_kernel : _mach_call_munger64 + 0x19a
0xffffff811945bfb0 : 0xffffff800de36ea6 mach_kernel : _hndl_mach_scall64 + 0x16

And later on, there is a vtable call on that object, so code execution is possible.
For more information please refer to the PoC attached. By the way, the PoC should be slightly adjusted when runing at single Graphic card MacBook:
service = IOIteratorNext(iter);
//service = IOIteratorNext(iter); //comment this line when the MacBook only has one Graphic card.
---

## Timeline

### sc...@gmail.com (2015-04-25)

Apple tracking id: 622080617

### in...@chromium.org (2015-11-03)

Reassigning to Ian from PZ. Ian, please update bug if there is any update on PZ tracking bug.

### ia...@chromium.org (2015-11-03)

Fixed in https://support.apple.com/en-us/HT204942 as CVE-2015-3705 

### cl...@chromium.org (2015-11-03)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-11-23)

No merge required - taking to reward panel for sandbox escape consideration. 

### cl...@chromium.org (2016-02-11)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

- Your friendly ClusterFuzz

### ti...@google.com (2016-06-24)

Found this old bug in a cleanup before I jump ship (our old script had -reporter:scaryb...@gmail.com in it). $5,000 for this report.

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@google.com (2016-11-18)

[Empty comment from Monorail migration]

### is...@google.com (2016-11-18)

This issue was migrated from crbug.com/chromium/481296?no_tracker_redirect=1

[Auto-CCs applied]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081936)*
