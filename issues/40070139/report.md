# security: libmbim | out-of-bounds access on mbim-message.c

| Field | Value |
|-------|-------|
| **Issue ID** | [40070139](https://issues.chromium.org/issues/40070139) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-08-21 |
| **Bounty** | $250.00 |

## Description

**Steps to reproduce the problem:**

1. Tested on zork board Chromebook.

**Problem Description:**  

Found the OOB access by libfuzzer. Tested on zork board Chromebook.

Tested on main libmbim

```
commit 623d6bf0df63b57b2c466677140aadb705c67cc5 (HEAD, m/release-R117-15572.B, m/main, cros/stabilize-15572.4.B, cros/stabilize-15564.B, cros/stabilize-15563.B, cros/stabilize-15562.B, cros/stabilize-15561.B, cros/stabilize-15532.B, cros/stabilize-15531.B, cros/release-R117-15572.B, cros/main, main)  
Author: Aleksander Morgado <aleksandermj@chromium.org>  
Date:   Fri Jun 30 09:51:17 2023 +0000  
  
    UPSTREAM: libmbim-glib,message: fix leak when processing string array is aborted  
      

```

The ASan report indicates the following:

1. The buffer overflow occurred during a `READ` operation of size `3681698` at address `0x511000000dc0`.
2. The error seems to originate from a `memcpy` operation (from the stack trace).
3. The buffer overflow was detected when `_mbim_message_read_tlv_list` called `_mbim_tlv_new_from_raw`

The main area of concern is the loop where you are processing the TLV (Type-Length-Value) list:  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/libmbim/src/libmbim-glib/mbim-message.c;l=1203>

```
while ((tlv_list_raw_size > 0) && !inner_error) {  
    ...  
    tlv = _mbim_tlv_new_from_raw (tlv_list_raw, tlv_list_raw_size, &tlv_size, &inner_error);  
    ...  
    tlv_list_raw += tlv_size;  
    tlv_list_raw_size -= tlv_size;  
}  

```

5. The line `g_assert(raw_length >= sizeof(struct tlv));` the input buffer raw has at least the size of the struct tlv.
6. `tlv_size = sizeof(struct tlv) + GUINT32_FROM_LE (((struct tlv \*)raw)->data_length) + ((struct tlv \*)raw)->padding_length;` computes the size of the TLV. The potential problem is if the `data_length` or `padding_length` (both read directly from the raw buffer) are crafted in such a way (either by error or malicious intent) that their sum with `sizeof(struct tlv)` exceeds the actual size of the raw buffer `(raw_length)`, might end up with a size `(tlv_size)` larger than the input buffer.

Recommendation to fix:

```
if (tlv_size > raw_length) {  
    g_set_error(error, _ERROR_DOMAIN, _ERROR_CODE, "Invalid TLV size computed");  
    return NULL;  
}  

```
# **Additional Comments:**

==391==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x511000000dc0 at pc 0x56272d875511 bp 0x7ffccfc70040 sp 0x7ffccfc6f800  

READ of size 3681698 at 0x511000000dc0 thread T0  

#0 0x56272d875510 in memcpy (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x10a510) (BuildId: 102a0bdb9cbbb3f5)  

#1 0x7fc4d3293779 in memcpy(void\*, void const\* pass\_object\_size0, unsigned long) /build/amd64-generic/usr/include/bits/string\_fortified.h:51:12  

#2 0x7fc4d3293779 in g\_array\_append\_vals /build/amd64-generic/tmp/portage/dev-libs/glib-2.74.1-r1/work/glib-2.74.1-abi\_x86\_64.amd64/../glib-2.74.1/glib/garray.c:530:3  

#3 0x56272d91e822 in \_mbim\_message\_read\_tlv\_list /build/zork/tmp/portage/net-libs/libmbim-9999/work/libmbim-9999-build/../libmbim-9999/src/libmbim-glib/mbim-message.c:1203:15  

#4 0x56272d9d9869 in mbim\_message\_ms\_basic\_connect\_extensions\_v3\_modem\_configuration\_response\_get\_printable /build/zork/tmp/portage/net-libs/libmbim-9999/work/libmbim-9999-build/src/libmbim-glib/generated/mbim-ms-basic-connect-extensions.c:8851:14  

#5 0x56272d924184 in mbim\_message\_get\_printable\_full /build/zork/tmp/portage/net-libs/libmbim-9999/work/libmbim-9999-build/../libmbim-9999/src/libmbim-glib/mbim-message.c:2208:36  

#6 0x56272d91a1f6 in LLVMFuzzerTestOneInput /build/zork/tmp/portage/net-libs/libmbim-9999/work/libmbim-9999-build/../libmbim-9999/src/libmbim-glib/test/mbim\_message\_get\_printable\_full\_fuzzer.c:31:21  

#7 0x56272d81e100 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0xb3100) (BuildId: 102a0bdb9cbbb3f5)  

#8 0x56272d808970 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x9d970) (BuildId: 102a0bdb9cbbb3f5)  

#9 0x56272d80de34 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0xa2e34) (BuildId: 102a0bdb9cbbb3f5)  

#10 0x56272d839492 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0xce492) (BuildId: 102a0bdb9cbbb3f5)  

#11 0x7fc4d2e076c5 in \_\_libc\_start\_call\_main /var/tmp/portage/cross-x86\_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16  

#12 0x7fc4d2e07781 in \_\_libc\_start\_main@GLIBC\_2.2.5 /var/tmp/portage/cross-x86\_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../csu/libc-start.c:389:3  

#13 0x56272d7ffd60 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x94d60) (BuildId: 102a0bdb9cbbb3f5)

0x511000000dc0 is located 0 bytes after 256-byte region [0x511000000cc0,0x511000000dc0)  

allocated by thread T0 here:  

#0 0x56272d8eb095 in \_\_interceptor\_realloc (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x180095) (BuildId: 102a0bdb9cbbb3f5)  

#1 0x7fc4d32c61fa in g\_realloc /build/amd64-generic/tmp/portage/dev-libs/glib-2.74.1-r1/work/glib-2.74.1-abi\_x86\_64.amd64/../glib-2.74.1/glib/gmem.c:201:16  

#2 0x7fc4d32934e4 in g\_array\_maybe\_expand /build/amd64-generic/tmp/portage/dev-libs/glib-2.74.1-r1/work/glib-2.74.1-abi\_x86\_64.amd64/../glib-2.74.1/glib/garray.c:1000:21  

#3 0x7fc4d329339a in g\_array\_sized\_new /build/amd64-generic/tmp/portage/dev-libs/glib-2.74.1-r1/work/glib-2.74.1-abi\_x86\_64.amd64/../glib-2.74.1/glib/garray.c:287:7  

#4 0x56272d923122 in mbim\_message\_new /build/zork/tmp/portage/net-libs/libmbim-9999/work/libmbim-9999-build/../libmbim-9999/src/libmbim-glib/mbim-message.c:1890:11  

#5 0x56272d91a1cb in LLVMFuzzerTestOneInput /build/zork/tmp/portage/net-libs/libmbim-9999/work/libmbim-9999-build/../libmbim-9999/src/libmbim-glib/test/mbim\_message\_get\_printable\_full\_fuzzer.c:28:24  

#6 0x56272d81e100 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0xb3100) (BuildId: 102a0bdb9cbbb3f5)  

#7 0x56272d808970 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x9d970) (BuildId: 102a0bdb9cbbb3f5)  

#8 0x56272d80de34 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0xa2e34) (BuildId: 102a0bdb9cbbb3f5)  

#9 0x56272d839492 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0xce492) (BuildId: 102a0bdb9cbbb3f5)  

#10 0x7fc4d2e076c5 in \_\_libc\_start\_call\_main /var/tmp/portage/cross-x86\_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16  

#11 0x7fc4d2e07781 in \_\_libc\_start\_main@GLIBC\_2.2.5 /var/tmp/portage/cross-x86\_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../csu/libc-start.c:389:3  

#12 0x56272d7ffd60 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x94d60) (BuildId: 102a0bdb9cbbb3f5)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x10a510) (BuildId: 102a0bdb9cbbb3f5) in memcpy  

Shadow bytes around the buggy address:  

0x511000000b00: 00 00 00 06 fa fa fa fa fa fa fa fa fa fa fa fa  

0x511000000b80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x511000000c00: 00 00 00 00 00 00 00 00 00 00 00 06 fa fa fa fa  

0x511000000c80: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x511000000d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x511000000d80: 00 00 00 00 00 00 00 00[fa]fa fa fa fa fa fa fa  

0x511000000e00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x511000000e80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x511000000f00: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x511000000f80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x511000001000: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==391==ABORTING

```
  
**Chrome version: ** 117 **Channel: ** Dev  
  
**OS:** Chrome OS

```

## Timeline

### [Deleted User] (2023-08-21)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-08-21)

-> ChromeOS

### st...@google.com (2023-08-28)

[Empty comment from Monorail migration]

### st...@google.com (2023-08-28)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/297884986). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### [Deleted User] (2023-08-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-12)

stannor: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rh...@gmail.com (2023-09-13)

Given that the issue has been resolved in the bug tracker, may we mark this as "Fixed"? This will enable it to proceed to the next panel for consideration

### ch...@google.com (2023-09-14)

[Empty comment from Monorail migration]

[Monorail blocking: b/297884986]

### [Deleted User] (2023-09-27)

stannor: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-21)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-10-23)

Verified by 
ChromeOS-security-vm-rotation@google.com.

Exploitability The bug is not reachable directly but can potentially cause sensitive information disclosure

Privileges and Capabilities May access information in modem

Origin of fix It was fixed upstream and is a new issue.

Mitigation : Modem manager is a sandboxed service

Severity: agree with https://crbug.com/chromium/1474639#c10, : Triaged as severity-medium based on ChromeOs security severity guidelines. Not higher because this is an OOB read in a not directly accessible area in the modem. Not lower because could result in leaking sensitive info when part of a larger exploit.

### [Deleted User] (2023-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-12-06)

[Empty comment from Monorail migration]

### rh...@gmail.com (2023-12-07)

Hi chmiel@,

Thanks a lot for the reward in early December, also for ChromeOS VRP team and developer. Thank you so much

### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-29)

This issue was migrated from crbug.com/chromium/1474639?no_tracker_redirect=1

[Monorail blocking: b/297884986]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070139)*
