# Security: heap-buffer-overflow vrend_write_to_iovec

| Field | Value |
|-------|-------|
| **Issue ID** | [40071209](https://issues.chromium.org/issues/40071209) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ph...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-09-02 |
| **Bounty** | $250.00 |

## Description

**VULNERABILITY DETAILS**  

heap-buffer-overflow vrend\_write\_to\_iovec

vrend\_write\_to\_iovec call memcpy without check for buf size lead to heap buffer overlow

```
  
size_t vrend_write_to_iovec(const struct iovec \*iov, int iovlen,  
			 size_t offset, const char \*buf, size_t count)  
{  
  size_t written = 0;  
  size_t len;  
  
  while (count > 0 && iovlen > 0) {  
    if (iov->iov_len > offset) {  
      len = iov->iov_len - offset;  
  
      if (count < len) len = count;  
  
      memcpy((char\*)iov->iov_base + offset, buf, len); // overflow when  len > buf size  
      written += len;  
  
      offset = 0;  
      buf += len;  
      count -= len;  
    } else {  
      offset -= iov->iov_len;  
    }  
    iov++;  
    iovlen--;  
  }  
    assert(offset == 0);  
  return written;  
}  
  

```

ASAN report

```
==4005811==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6120000080b8 at pc 0x7f85202ccae7 bp 0x7ffddbb644e0 sp 0x7ffddbb63cb0  
READ of size 256 at 0x6120000080b8 thread T0  
    #0 0x7f85202ccae6 in __asan_memcpy (/usr/lib/llvm-14/lib/clang/14.0.0/lib/linux/libclang_rt.asan-x86_64.so+0xccae6) (BuildId: a6105a816e63299474c1078329a59ed80f244fbf)  
    #1 0x7f851fade7b8 in vrend_write_to_iovec /home/zx/ovirgl/asan/../src/iov.c:100:7  
    #2 0x7f851fb504c0 in vrend_renderer_transfer_send_iov /home/zx/ovirgl/asan/../src/vrend_renderer.c:9509:10  
    #3 0x7f851fb469e8 in vrend_renderer_transfer_internal /home/zx/ovirgl/asan/../src/vrend_renderer.c:9579:14  
    #4 0x7f851fb4634c in vrend_renderer_transfer_iov /home/zx/ovirgl/asan/../src/vrend_renderer.c:9609:11  
    #5 0x7f851faebd41 in vrend_decode_transfer3d /home/zx/ovirgl/asan/../src/vrend_decode.c:1417:11  
    #6 0x7f851fae3895 in vrend_decode_ctx_submit_cmd /home/zx/ovirgl/asan/../src/vrend_decode.c:1943:13  
    #7 0x7f851fad4c1a in virgl_renderer_submit_cmd /home/zx/ovirgl/asan/../src/virglrenderer.c:289:11  
    #8 0x5577a2248928 in FuzzMode1 /home/zx/ovirgl/asan/../tests/fuzzer/virgl_fuzzer.c:240:4  
    #9 0x5577a22481d8 in LLVMFuzzerTestOneInput /home/zx/ovirgl/asan/../tests/fuzzer/virgl_fuzzer.c:259:4  
    #10 0x5577a222d493 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const\*, unsigned long) (/home/zx/ovirgl/asan/tests/fuzzer/virgl_fuzzer+0x24493) (BuildId: 51de998794e20d956919658f737f4e2248d5d50c)  
    #11 0x5577a222cbe9 in fuzzer::Fuzzer::RunOne(unsigned char const\*, unsigned long, bool, fuzzer::InputInfo\*, bool, bool\*) (/home/zx/ovirgl/asan/tests/fuzzer/virgl_fuzzer+0x23be9) (BuildId: 51de998794e20d956919658f737f4e2248d5d50c)  
    #12 0x5577a222e8c6 in fuzzer::Fuzzer::ReadAndExecuteSeedCorpora(std::vector<fuzzer::SizedFile, std::allocator<fuzzer::SizedFile> >&) (/home/zx/ovirgl/asan/tests/fuzzer/virgl_fuzzer+0x258c6) (BuildId: 51de998794e20d956919658f737f4e2248d5d50c)  
    #13 0x5577a222ed42 in fuzzer::Fuzzer::Loop(std::vector<fuzzer::SizedFile, std::allocator<fuzzer::SizedFile> >&) (/home/zx/ovirgl/asan/tests/fuzzer/virgl_fuzzer+0x25d42) (BuildId: 51de998794e20d956919658f737f4e2248d5d50c)  
    #14 0x5577a221d092 in fuzzer::FuzzerDriver(int\*, char\*\*\*, int (\*)(unsigned char const\*, unsigned long)) (/home/zx/ovirgl/asan/tests/fuzzer/virgl_fuzzer+0x14092) (BuildId: 51de998794e20d956919658f737f4e2248d5d50c)  
    #15 0x5577a2246d82 in main (/home/zx/ovirgl/asan/tests/fuzzer/virgl_fuzzer+0x3dd82) (BuildId: 51de998794e20d956919658f737f4e2248d5d50c)  
    #16 0x7f851f629d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16  
    #17 0x7f851f629e3f in __libc_start_main csu/../csu/libc-start.c:392:3  
    #18 0x5577a2211ad4 in _start (/home/zx/ovirgl/asan/tests/fuzzer/virgl_fuzzer+0x8ad4) (BuildId: 51de998794e20d956919658f737f4e2248d5d50c)  
  
0x6120000080b8 is located 0 bytes to the right of 248-byte region [0x612000007fc0,0x6120000080b8)  
allocated by thread T0 here:  
    #0 0x7f85202ce367 in posix_memalign (/usr/lib/llvm-14/lib/clang/14.0.0/lib/linux/libclang_rt.asan-x86_64.so+0xce367) (BuildId: a6105a816e63299474c1078329a59ed80f244fbf)  
    #1 0x7f851a0f4628  (/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so+0x6f4628) (BuildId: d04a40e4062a8d444ff6f23d4fe768215b2e32c7)  
  
SUMMARY: AddressSanitizer: heap-buffer-overflow (/usr/lib/llvm-14/lib/clang/14.0.0/lib/linux/libclang_rt.asan-x86_64.so+0xccae6) (BuildId: a6105a816e63299474c1078329a59ed80f244fbf) in __asan_memcpy  
Shadow bytes around the buggy address:  
  0x0c247fff8fc0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  
  0x0c247fff8fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x0c247fff8fe0: 00 00 00 00 00 00 00 00 04 fa fa fa fa fa fa fa  
  0x0c247fff8ff0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  
  0x0c247fff9000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
=>0x0c247fff9010: 00 00 00 00 00 00 00[fa]fa fa fa fa fa fa fa fa  
  0x0c247fff9020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x0c247fff9030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x0c247fff9040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x0c247fff9050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
  0x0c247fff9060: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  
Shadow byte legend (one shadow byte represents 8 application bytes):  
  Addressable:           00  
  Partially addressable: 01 02 03 04 05 06 07  
  Heap left redzone:       fa  
  Freed heap region:       fd  
  Stack left redzone:      f1  
  Stack mid redzone:       f2  
  Stack right redzone:     f3  
  Stack after return:      f5  
  Stack use after scope:   f8  
  Global redzone:          f9  
  Global init order:       f6  
  Poisoned by user:        f7  
  Container overflow:      fc  
  Array cookie:            ac  
  Intra object redzone:    bb  
  ASan internal:           fe  
  Left alloca redzone:     ca  
  Right alloca redzone:    cb  

```

**VERSION** :  

virglrenderer HEAD  

Operating System: ChromiumOS

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

**Reporter credit: [goes here]**

## Attachments

- [virgl_fuzzer.c](attachments/virgl_fuzzer.c) (text/plain, 7.7 KB)

## Timeline

### [Deleted User] (2023-09-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-05)

virGL is specific to ChromeOS, setting OS=Chrome so this issue can be triaged by ChromeOS security team

### st...@google.com (2023-09-07)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/299482841). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### ch...@google.com (2023-09-18)

[Empty comment from Monorail migration]

[Monorail blocking: b/299482841]

### [Deleted User] (2023-09-22)

stannor: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-06)

stannor: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-10-11)

Verified by 
ChromeOS-security-vm-rotation@google.com.
The function exploited is similar to https://b.corp.google.com/issues/299871941.

Exploitability - Not boundary check on memcpy source, OOB read, and then arbitrary bytes are written into iovec.

Privileges and Capabilities - OOB read and copy into iovec may lead to eventually arbitrary code execution. For virgil render, it is local privilege escalation.

Origin of fix - virgilrender developer (upstream).

Mitigations - Indirect fix. The function has an assumption that the buf should have enough allocation. The mitigation ensures that when calling this function, the buf allocation is sufficient.

Severity assessment - Medium, requires other bugs to trigger OOB write.

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### ch...@google.com (2023-11-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-18)

This issue was migrated from crbug.com/chromium/1478462?no_tracker_redirect=1

[Monorail blocking: b/299482841]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071209)*
