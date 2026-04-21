# Security: heap-buffer-overflow vrend_read_from_iovec

| Field | Value |
|-------|-------|
| **Issue ID** | [40071366](https://issues.chromium.org/issues/40071366) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ph...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-09-05 |
| **Bounty** | $250.00 |

## Description

**VULNERABILITY DETAILS**  

vrend\_read\_from\_iovec call memcpy without check the buf size lead to heap buffer overflow

size\_t vrend\_read\_from\_iovec(const struct iovec \*iov, int iovlen,  

size\_t offset,  

char \*buf, size\_t count)  

{  

size\_t read = 0;  

size\_t len;

while (count > 0 && iovlen > 0) {  

if (iov->iov\_len > offset) {  

len = iov->iov\_len - offset;

```
  if (count < len) len = count;  

  memcpy(buf, (char\*)iov->iov_base + offset, len); <--- overflow here  
  read += len;  

  buf += len;  
  count -= len;  
  offset = 0;  
} else {  
  offset -= iov->iov_len;  
}  

iov++;  
iovlen--;  

```

}  

assert(offset == 0);  

return read;  

}

```
ASAN report  

```

==3856743==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000058294 at pc 0x7f33d4cccb9a bp 0x7ffd88af7d70 sp 0x7ffd88af7540  

WRITE of size 8 at 0x602000058294 thread T0  

#0 0x7f33d4cccb99 in \_\_asan\_memcpy (/usr/lib/llvm-14/lib/clang/14.0.0/lib/linux/libclang\_rt.asan-x86\_64.so+0xccb99) (BuildId: a6105a816e63299474c1078329a59ed80f244fbf)  

#1 0x7f33d4491de0 in vrend\_read\_from\_iovec /home/zx/virgl/dvirgl/asan/../src/iov.c:71:7  

#2 0x7f33d452354a in read\_transfer\_data /home/zx/virgl/dvirgl/asan/../src/vrend\_renderer.c:8706:16  

#3 0x7f33d44f196a in vrend\_resource\_copy\_fallback /home/zx/virgl/dvirgl/asan/../src/vrend\_renderer.c:10057:7  

#4 0x7f33d44eebac in vrend\_renderer\_resource\_copy\_region /home/zx/virgl/dvirgl/asan/../src/vrend\_renderer.c:10292:7  

#5 0x7f33d44996fd in vrend\_decode\_resource\_copy\_region /home/zx/virgl/dvirgl/asan/../src/vrend\_decode.c:997:4  

#6 0x7f33d44954f9 in vrend\_decode\_ctx\_submit\_cmd /home/zx/virgl/dvirgl/asan/../src/vrend\_decode.c:1943:13  

#7 0x7f33d448b51b in virgl\_renderer\_submit\_cmd /home/zx/virgl/dvirgl/asan/../src/virglrenderer.c:359:11  

#8 0x557f9998d8e7 in FuzzMode1 /home/zx/virgl/dvirgl/asan/../tests/fuzzer/virgl\_fuzzer.c:1694:7  

#9 0x557f999895f6 in LLVMFuzzerTestOneInput /home/zx/virgl/dvirgl/asan/../tests/fuzzer/virgl\_fuzzer.c:2382:3  

#10 0x557f999665e3 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const\*, unsigned long) (/home/zx/virgl/dvirgl/asan/tests/fuzzer/virgl\_fuzzer+0x295e3) (BuildId: 3e8892e9f2e3c9024da2c9eea8b7ab6062436ba0)  

#11 0x557f9995035f in fuzzer::RunOneTest(fuzzer::Fuzzer\*, char const\*, unsigned long) (/home/zx/virgl/dvirgl/asan/tests/fuzzer/virgl\_fuzzer+0x1335f) (BuildId: 3e8892e9f2e3c9024da2c9eea8b7ab6062436ba0)  

#12 0x557f999560b6 in fuzzer::FuzzerDriver(int\*, char\*\*\*, int (\*)(unsigned char const\*, unsigned long)) (/home/zx/virgl/dvirgl/asan/tests/fuzzer/virgl\_fuzzer+0x190b6) (BuildId: 3e8892e9f2e3c9024da2c9eea8b7ab6062436ba0)  

#13 0x557f9997fed2 in main (/home/zx/virgl/dvirgl/asan/tests/fuzzer/virgl\_fuzzer+0x42ed2) (BuildId: 3e8892e9f2e3c9024da2c9eea8b7ab6062436ba0)  

#14 0x7f33d4029d8f in \_\_libc\_start\_call\_main csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16  

#15 0x7f33d4029e3f in \_\_libc\_start\_main csu/../csu/libc-start.c:392:3  

#16 0x557f9994ac24 in \_start (/home/zx/virgl/dvirgl/asan/tests/fuzzer/virgl\_fuzzer+0xdc24) (BuildId: 3e8892e9f2e3c9024da2c9eea8b7ab6062436ba0)

0x602000058294 is located 0 bytes to the right of 4-byte region [0x602000058290,0x602000058294)  

allocated by thread T0 here:  

#0 0x7f33d4ccd7ee in \_\_interceptor\_malloc (/usr/lib/llvm-14/lib/clang/14.0.0/lib/linux/libclang\_rt.asan-x86\_64.so+0xcd7ee) (BuildId: a6105a816e63299474c1078329a59ed80f244fbf)  

#1 0x7f33d44f12f1 in vrend\_resource\_copy\_fallback /home/zx/virgl/dvirgl/asan/../src/vrend\_renderer.c:10031:11  

#2 0x7f33d44eebac in vrend\_renderer\_resource\_copy\_region /home/zx/virgl/dvirgl/asan/../src/vrend\_renderer.c:10292:7  

#3 0x7f33d44996fd in vrend\_decode\_resource\_copy\_region /home/zx/virgl/dvirgl/asan/../src/vrend\_decode.c:997:4  

#4 0x7f33d44954f9 in vrend\_decode\_ctx\_submit\_cmd /home/zx/virgl/dvirgl/asan/../src/vrend\_decode.c:1943:13  

#5 0x7f33d448b51b in virgl\_renderer\_submit\_cmd /home/zx/virgl/dvirgl/asan/../src/virglrenderer.c:359:11  

#6 0x557f9998d8e7 in FuzzMode1 /home/zx/virgl/dvirgl/asan/../tests/fuzzer/virgl\_fuzzer.c:1694:7  

#7 0x557f999895f6 in LLVMFuzzerTestOneInput /home/zx/virgl/dvirgl/asan/../tests/fuzzer/virgl\_fuzzer.c:2382:3  

#8 0x557f999665e3 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const\*, unsigned long) (/home/zx/virgl/dvirgl/asan/tests/fuzzer/virgl\_fuzzer+0x295e3) (BuildId: 3e8892e9f2e3c9024da2c9eea8b7ab6062436ba0)  

#9 0x557f9995035f in fuzzer::RunOneTest(fuzzer::Fuzzer\*, char const\*, unsigned long) (/home/zx/virgl/dvirgl/asan/tests/fuzzer/virgl\_fuzzer+0x1335f) (BuildId: 3e8892e9f2e3c9024da2c9eea8b7ab6062436ba0)  

#10 0x557f999560b6 in fuzzer::FuzzerDriver(int\*, char\*\*\*, int (\*)(unsigned char const\*, unsigned long)) (/home/zx/virgl/dvirgl/asan/tests/fuzzer/virgl\_fuzzer+0x190b6) (BuildId: 3e8892e9f2e3c9024da2c9eea8b7ab6062436ba0)  

#11 0x557f9997fed2 in main (/home/zx/virgl/dvirgl/asan/tests/fuzzer/virgl\_fuzzer+0x42ed2) (BuildId: 3e8892e9f2e3c9024da2c9eea8b7ab6062436ba0)  

#12 0x7f33d4029d8f in \_\_libc\_start\_call\_main csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

SUMMARY: AddressSanitizer: heap-buffer-overflow (/usr/lib/llvm-14/lib/clang/14.0.0/lib/linux/libclang\_rt.asan-x86\_64.so+0xccb99) (BuildId: a6105a816e63299474c1078329a59ed80f244fbf) in \_\_asan\_memcpy  

Shadow bytes around the buggy address:  

0x0c0480003000: fa fa 00 00 fa fa 01 fa fa fa 02 fa fa fa 06 fa  

0x0c0480003010: fa fa 07 fa fa fa 00 02 fa fa 00 03 fa fa 00 00  

0x0c0480003020: fa fa 01 fa fa fa 02 fa fa fa 00 03 fa fa 00 04  

0x0c0480003030: fa fa 00 07 fa fa 00 00 fa fa 01 fa fa fa 02 fa  

0x0c0480003040: fa fa 06 fa fa fa 07 fa fa fa 00 03 fa fa 00 00  

=>0x0c0480003050: fa fa[04]fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480003060: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480003070: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480003080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c0480003090: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c04800030a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==3856743==ABORTING

```
**VERSION**   
ChromeOS - virglrenderer  
  
  
**REPRODUCTION CASE**   
**Please include a demonstration of the security bug, such as an attached**   
**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**   
**make the file as small as possible and remove any content not required to**   
**demonstrate the bug, or any personal or confidential information.**   
  
**Please attach files directly, not in zip or other archive formats, and if**   
**you've created a demonstration site please also attach the files needed to**   
**reproduce the demonstration locally.**   
  
**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**   
**Type of crash: [tab, browser, etc.]**   
**Crash State: [see link above: stack trace \*with symbols\*, registers,**   
**exception record]**   
**Client ID (if relevant): [see link above]**   
  
**CREDIT INFORMATION**   
**Externally reported security bugs may appear in Chrome release notes. If**   
**this bug is included, how would you like to be credited?**   
Reporter credit: [zx]  

```

## Attachments

- [virgl_fuzzer.c](attachments/virgl_fuzzer.c) (text/plain, 8.1 KB)

## Timeline

### [Deleted User] (2023-09-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-05)

OS=Chrome since this is a virGL bug, over to ChromeOS security for triage 

### ch...@google.com (2023-09-11)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/299871941). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/299871941]

### [Deleted User] (2023-09-12)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-10)

Verified by 
ChromeOS-security-vm-rotation@google.com.
Exploitability - Not boundary check on memcpy destination.

Privileges and Capabilities - OOB may lead to stack overflow and eventually arbitrary code execution. For virgil render, it is local privilege escalation.

Origin of fix - virgilrender developer (upstream).

Mitigations - Indirect fix. The function has an assumption that the buf should have enough allocation. The mitigation ensures the buf allocation is sufficient.

Severity assessment - Medium, requires other bugs to trigger OOB write.

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### ch...@google.com (2023-11-15)

[Empty comment from Monorail migration]

### ch...@google.com (2023-11-15)

Congratulations! 
The VRP Panel has decided to award you $250 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

### am...@google.com (2023-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-16)

This issue was migrated from crbug.com/chromium/1479005?no_tracker_redirect=1

[Monorail blocking: b/299871941]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071366)*
