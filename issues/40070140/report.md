# security: libmbim | heap-buffer-overflow on mbim-message.c

| Field | Value |
|-------|-------|
| **Issue ID** | [40070140](https://issues.chromium.org/issues/40070140) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-08-21 |
| **Bounty** | $750.00 |

## Description

**Steps to reproduce the problem:**

1. Tested on zork board Chromebook.

**Problem Description:**  

Found the OOB read by libfuzzer. Tested on zork board Chromebook.

Tested on main libmbim

```
commit 623d6bf0df63b57b2c466677140aadb705c67cc5 (HEAD, m/release-R117-15572.B, m/main, cros/stabilize-15572.4.B, cros/stabilize-15564.B, cros/stabilize-15563.B, cros/stabilize-15562.B, cros/stabilize-15561.B, cros/stabilize-15532.B, cros/stabilize-15531.B, cros/release-R117-15572.B, cros/main, main)  
Author: Aleksander Morgado <aleksandermj@chromium.org>  
Date:   Fri Jun 30 09:51:17 2023 +0000  
  
    UPSTREAM: libmbim-glib,message: fix leak when processing string array is aborted  
      

```

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/libmbim/src/libmbim-glib/mbim-message.c;l=1098>

```
tlv_size = ((guint64)sizeof (struct tlv) +  
            (guint64)GUINT32_FROM_LE (((struct tlv \*)tlv_raw)->data_length) + --> here  
            (guint64)((struct tlv \*)tlv_raw)->padding_length);  

```

1. The heap-buffer-overflow is triggered when the program tries to access the `data_length` member of the struct `tlv`, denoted by `(struct tlv \*)tlv_raw)->data_length`
2. the `tlv_offset` is computed by summing `information_buffer_offset` and `relative_offset`. The resultant offset `(tlv_offset)` is then used to retrieve the `raw` pointer to the `tlv` data using `G_STRUCT_MEMBER_P`. This method assumes that `tlv_offset` falls within the valid bounds of `self->data`, which may not always be the case. If information\_buffer\_offset or relative\_offset are corrupted or not properly validated, this can lead to tlv\_raw pointing outside the bounds of self->data.
3. The `tlv_raw` pointer, compute the `tlv_size` using the `data_length` and `padding_length` from the `struct`. If these values are tampered with or not correctly initialized, this calculation can lead to incorrect sizes, leading to potential `buffer-overflows`.

# **Additional Comments:**

==361==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x50c000000780 at pc 0x561c3d397f55 bp 0x7ffcd9601710 sp 0x7ffcd9601708  

READ of size 4 at 0x50c000000780 thread T0  

#0 0x561c3d397f54 in \_mbim\_message\_read\_tlv /build/zork/tmp/portage/net-libs/libmbim-9999/work/libmbim-9999-build/../libmbim-9999/src/libmbim-glib/mbim-message.c:1098:26  

#1 0x561c3d36f10f (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x18a10f) (BuildId: 102a0bdb9cbbb3f5)  

#2 0x561c3d2e0fc8 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0xfbfc8) (BuildId: 102a0bdb9cbbb3f5)  

#3 0x561c3d3692bb (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x1842bb) (BuildId: 102a0bdb9cbbb3f5)  

#4 0x561c3d36c59c (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x18759c) (BuildId: 102a0bdb9cbbb3f5)  

#5 0x561c3d36d6e4 in \_\_asan\_report\_load\_n (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x1886e4) (BuildId: 102a0bdb9cbbb3f5)

0x50c000000780 is located 0 bytes after 128-byte region [0x50c000000700,0x50c000000780)  

allocated by thread T0 here:  

#0 0x561c3d365095 in \_\_interceptor\_realloc (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x180095) (BuildId: 102a0bdb9cbbb3f5)  

#1 0x7f0225e071fa in g\_realloc /build/amd64-generic/tmp/portage/dev-libs/glib-2.74.1-r1/work/glib-2.74.1-abi\_x86\_64.amd64/../glib-2.74.1/glib/gmem.c:201:16  

#2 0x7f0225dd44e4 in g\_array\_maybe\_expand /build/amd64-generic/tmp/portage/dev-libs/glib-2.74.1-r1/work/glib-2.74.1-abi\_x86\_64.amd64/../glib-2.74.1/glib/garray.c:1000:21  

#3 0x7f0225dd439a in g\_array\_sized\_new /build/amd64-generic/tmp/portage/dev-libs/glib-2.74.1-r1/work/glib-2.74.1-abi\_x86\_64.amd64/../glib-2.74.1/glib/garray.c:287:7  

#4 0x561c3d39d122 in mbim\_message\_new /build/zork/tmp/portage/net-libs/libmbim-9999/work/libmbim-9999-build/../libmbim-9999/src/libmbim-glib/mbim-message.c:1890:11  

#5 0x561c3d3941cb in LLVMFuzzerTestOneInput /build/zork/tmp/portage/net-libs/libmbim-9999/work/libmbim-9999-build/../libmbim-9999/src/libmbim-glib/test/mbim\_message\_get\_printable\_full\_fuzzer.c:28:24  

#6 0x561c3d298100 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0xb3100) (BuildId: 102a0bdb9cbbb3f5)  

#7 0x561c3d282970 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x9d970) (BuildId: 102a0bdb9cbbb3f5)  

#8 0x561c3d287e34 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0xa2e34) (BuildId: 102a0bdb9cbbb3f5)  

#9 0x561c3d2b3492 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0xce492) (BuildId: 102a0bdb9cbbb3f5)  

#10 0x7f02259486c5 in \_\_libc\_start\_call\_main /var/tmp/portage/cross-x86\_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16  

#11 0x7f0225948781 in \_\_libc\_start\_main@GLIBC\_2.2.5 /var/tmp/portage/cross-x86\_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../csu/libc-start.c:389:3  

#12 0x561c3d279d60 (/usr/libexec/fuzzers/mbim\_message\_get\_printable\_full\_fuzzer+0x94d60) (BuildId: 102a0bdb9cbbb3f5)

SUMMARY: AddressSanitizer: heap-buffer-overflow /build/zork/tmp/portage/net-libs/libmbim-9999/work/libmbim-9999-build/../libmbim-9999/src/libmbim-glib/mbim-message.c:1098:26 in \_mbim\_message\_read\_tlv  

Shadow bytes around the buggy address:  

0x50c000000500: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x50c000000580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x50c000000600: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x50c000000680: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x50c000000700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x50c000000780:[fa]fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x50c000000800: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x50c000000880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x50c000000900: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x50c000000980: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x50c000000a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==361==ABORTING

\*\*Chrome version: \*\* 117 \*\*Channel: \*\* Dev

**OS:** Chrome OS

## Timeline

### [Deleted User] (2023-08-21)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-08-21)

-> ChromeOS

### st...@google.com (2023-08-28)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/297886079). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### rh...@gmail.com (2023-09-13)

Given that the issue has been resolved in the bug tracker, may we mark this as "Fixed"? This will enable it to proceed to the next panel for consideration

### ch...@google.com (2023-09-14)

[Empty comment from Monorail migration]

[Monorail blocking: b/297886079]

### ch...@google.com (2023-09-18)

Exploitability - Reporter added the fuzzer output showing the crash and the heap buffer overflow exploitablity.

Privileges and Capabilities - This is an OOB read issue, no privileges gained.

Origin of fix - Reporter is the original reporter. Reporter also created their fuzzer. Reporter explained the problem causing the buffer overflow clearly, which helps with the fix as well.

Mitigations - The leaked memory area is not directly accessible.

Severity assessment - OOB read in the system services is considered medium severity. Not high because OOB read happens for a limited amount of information that is not directly reachable. Not lower because there is still possibility of sensitive data leak if part of a larger exploit.



### ch...@google.com (2023-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-19)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-12-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-25)

This issue was migrated from crbug.com/chromium/1474640?no_tracker_redirect=1

[Monorail blocking: b/297886079]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070140)*
