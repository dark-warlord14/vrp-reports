# Security: heap-use-after-free on vrend_renderer_get_meminfo

| Field | Value |
|-------|-------|
| **Issue ID** | [40072461](https://issues.chromium.org/issues/40072461) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ph...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-09-15 |
| **Bounty** | $2,000.00 |

## Description

**-------------------------**

**VULNERABILITY DETAILS**  

virgl\_resource\_create can destroy prev allocated resource lead to UAF

```
  
static struct virgl_resource \*  
virgl_resource_create(uint32_t res_id)  
{  
   struct virgl_resource \*res;  
   enum pipe_error err;  
  
   res = calloc(1, sizeof(\*res));  
   if (!res)  
      return NULL;  
  
   err = util_hash_table_set(virgl_resource_table,   <- free prev allocated resource   
                             uintptr_to_pointer(res_id),  
                             res);  
   if (err != PIPE_OK) {  
      free(res);  
      return NULL;  
   }  
  
   res->res_id = res_id;  
   res->fd_type = VIRGL_RESOURCE_FD_INVALID;  
   res->fd = -1;  
  
   return res;  
}  

```

Stacktrace

```
==64948==ERROR: AddressSanitizer: heap-use-after-free on address 0x61400000d4a0 at pc 0x7f9b9337aeef bp 0x7ffed8e01b50 sp 0x7ffed8e01b48  
READ of size 8 at 0x61400000d4a0 thread T0  
    #0 0x7f9b9337aeee in vrend_renderer_get_meminfo /home/zx/virglrenderer/asan/../src/vrend_renderer.c:13104:14  
    #1 0x7f9b932f5391 in vrend_decode_get_memory_info /home/zx/virglrenderer/asan/../src/vrend_decode.c:1638:4  
    #2 0x7f9b932ead85 in vrend_decode_ctx_submit_cmd /home/zx/virglrenderer/asan/../src/vrend_decode.c:1971:13  
    #3 0x7f9b932d8d1a in virgl_renderer_submit_cmd /home/zx/virglrenderer/asan/../src/virglrenderer.c:296:11  
    #4 0x558c3263fbfa in FuzzMode1 /home/zx/virglrenderer/asan/../tests/fuzzer/virgl_fuzzer.c:244:4  
    #5 0x558c3263f1b8 in LLVMFuzzerTestOneInput /home/zx/virglrenderer/asan/../tests/fuzzer/virgl_fuzzer.c:263:4  
    #6 0x558c32624473 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const\*, unsigned long) (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0x24473) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
    #7 0x558c3260e1ef in fuzzer::RunOneTest(fuzzer::Fuzzer\*, char const\*, unsigned long) (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0xe1ef) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
    #8 0x558c32613f46 in fuzzer::FuzzerDriver(int\*, char\*\*\*, int (\*)(unsigned char const\*, unsigned long)) (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0x13f46) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
    #9 0x558c3263dd62 in main (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0x3dd62) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
    #10 0x7f9b92e29d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16  
    #11 0x7f9b92e29e3f in __libc_start_main csu/../csu/libc-start.c:392:3  
    #12 0x558c32608ab4 in _start (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0x8ab4) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
  
0x61400000d4a0 is located 96 bytes inside of 392-byte region [0x61400000d440,0x61400000d5c8)  
freed by thread T0 here:  
    #0 0x7f9b93acd542 in free (/usr/lib/llvm-14/lib/clang/14.0.0/lib/linux/libclang_rt.asan-x86_64.so+0xcd542) (BuildId: a6105a816e63299474c1078329a59ed80f244fbf)  
    #1 0x7f9b9334d4e0 in vrend_renderer_resource_destroy /home/zx/virglrenderer/asan/../src/vrend_renderer.c:8639:4  
    #2 0x7f9b9333e957 in vrend_pipe_resource_unref /home/zx/virglrenderer/asan/../src/vrend_renderer.c:7239:7  
    #3 0x7f9b932e6e19 in virgl_resource_destroy_func /home/zx/virglrenderer/asan/../src/virgl_resource.c:48:7  
    #4 0x7f9b9345d0a5 in util_hash_table_set /home/zx/virglrenderer/asan/../src/gallium/auxiliary/util/u_hash_table.c:101:7  
    #5 0x7f9b932e729d in virgl_resource_create /home/zx/virglrenderer/asan/../src/virgl_resource.c:95:10  
    #6 0x7f9b932e70b4 in virgl_resource_create_from_pipe /home/zx/virglrenderer/asan/../src/virgl_resource.c:118:10  
    #7 0x7f9b932d7a9e in virgl_renderer_resource_create_internal /home/zx/virglrenderer/asan/../src/virglrenderer.c:111:10  
    #8 0x7f9b932d7034 in virgl_renderer_resource_create /home/zx/virglrenderer/asan/../src/virglrenderer.c:126:11  
    #9 0x558c3263fbd5 in FuzzMode1 /home/zx/virglrenderer/asan/../tests/fuzzer/virgl_fuzzer.c:241:4  
    #10 0x558c3263f1b8 in LLVMFuzzerTestOneInput /home/zx/virglrenderer/asan/../tests/fuzzer/virgl_fuzzer.c:263:4  
    #11 0x558c32624473 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const\*, unsigned long) (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0x24473) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
    #12 0x558c3260e1ef in fuzzer::RunOneTest(fuzzer::Fuzzer\*, char const\*, unsigned long) (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0xe1ef) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
    #13 0x558c32613f46 in fuzzer::FuzzerDriver(int\*, char\*\*\*, int (\*)(unsigned char const\*, unsigned long)) (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0x13f46) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
    #14 0x558c3263dd62 in main (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0x3dd62) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
    #15 0x7f9b92e29d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16  
  
previously allocated by thread T0 here:  
    #0 0x7f9b93acd9d8 in __interceptor_calloc (/usr/lib/llvm-14/lib/clang/14.0.0/lib/linux/libclang_rt.asan-x86_64.so+0xcd9d8) (BuildId: a6105a816e63299474c1078329a59ed80f244fbf)  
    #1 0x7f9b93348278 in vrend_resource_create /home/zx/virglrenderer/asan/../src/vrend_renderer.c:8560:34  
    #2 0x7f9b93347eb3 in vrend_renderer_resource_create /home/zx/virglrenderer/asan/../src/vrend_renderer.c:8582:9  
    #3 0x7f9b932d7a03 in virgl_renderer_resource_create_internal /home/zx/virglrenderer/asan/../src/virglrenderer.c:107:15  
    #4 0x7f9b932d7034 in virgl_renderer_resource_create /home/zx/virglrenderer/asan/../src/virglrenderer.c:126:11  
    #5 0x558c3263f81b in FuzzMode1 /home/zx/virglrenderer/asan/../tests/fuzzer/virgl_fuzzer.c:225:4  
    #6 0x558c3263f1b8 in LLVMFuzzerTestOneInput /home/zx/virglrenderer/asan/../tests/fuzzer/virgl_fuzzer.c:263:4  
    #7 0x558c32624473 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const\*, unsigned long) (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0x24473) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
    #8 0x558c3260e1ef in fuzzer::RunOneTest(fuzzer::Fuzzer\*, char const\*, unsigned long) (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0xe1ef) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
    #9 0x558c32613f46 in fuzzer::FuzzerDriver(int\*, char\*\*\*, int (\*)(unsigned char const\*, unsigned long)) (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0x13f46) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
    #10 0x558c3263dd62 in main (/home/zx/virglrenderer/asan/tests/fuzzer/virgl_fuzzer+0x3dd62) (BuildId: b5c291a51f19702334fe2d272e56bc3f14fc5452)  
    #11 0x7f9b92e29d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16  
  
SUMMARY: AddressSanitizer: heap-use-after-free /home/zx/virglrenderer/asan/../src/vrend_renderer.c:13104:14 in vrend_renderer_get_meminfo  
Shadow bytes around the buggy address:  
  0x0c287fff9a40: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  
  0x0c287fff9a50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x0c287fff9a60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x0c287fff9a70: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa  
  0x0c287fff9a80: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  
=>0x0c287fff9a90: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd  
  0x0c287fff9aa0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  
  0x0c287fff9ab0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  
  0x0c287fff9ac0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  
  0x0c287fff9ad0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
  0x0c287fff9ae0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  
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
==64948==ABORTING  

```

**VERSION**  

ChromeOS: Virglrenderer [HEAD]

## Attachments

- deleted (application/octet-stream, 0 B)
- [virgl_fuzzer.c](attachments/virgl_fuzzer.c) (text/plain, 6.0 KB)

## Timeline

### ph...@gmail.com (2023-09-15)

Sorry wrong testcase

### [Deleted User] (2023-09-15)

[Empty comment from Monorail migration]

### nh...@google.com (2023-09-15)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-18)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/300859154). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/300859154]

### [Deleted User] (2023-09-19)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-23)

Verified by  ChromeOS-security-vm-rotation@google.com.

Exploitability: PoC (modified fuzzer) supplied which triggers the UaF behavior. The original device that was allocated need to rewritten but not all references to the original are destroyed.

Privileges and Capabilities: Potential for privilege escalation.

Origin of fix: Not known upstream until reported by the reporter. Reporter provided patch.

Mitigations: The resource need to be created with the same handle (not sure how possible that is)

Severity assessment: Medium (out of abundance of caution). There's no immediate demonstration in the PoC that you could be reachable from guest.

### [Deleted User] (2023-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-29)

This issue was migrated from crbug.com/chromium/1483307?no_tracker_redirect=1

[Monorail blocking: b/300859154]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072461)*
