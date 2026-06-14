# Security: virglrenderer | heap-buffer-overflow on vrend_decode_set_debug_mask

| Field | Value |
|-------|-------|
| **Issue ID** | [40068966](https://issues.chromium.org/issues/40068966) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-08-07 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. tested on google pixelbook go, build fuzzer and run with iris gpu

**Problem Description:**  

There's maybe missing boundary checking for following code that may lead to heap-buffer-overflow.  

Tested on real devices chromebook (Chromium 117.0.5928.0) with latest virglrenderer version under asan.

Few of error stack couldn't be symbolized due some technical environment.

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/virglrenderer/src/vrend_decode.c;l=1350-1372?q=src%2Fvrend_decode.c>

```
static int vrend_decode_set_debug_mask(struct vrend_context \*ctx, const uint32_t \*buf, uint32_t length)  
{  
   char \*flagstring;  
   size_t slen = sizeof(uint32_t) \* length;  
  
   if (length < VIRGL_SET_DEBUG_FLAGS_MIN_SIZE)  
      return EINVAL;  
  
   const uint32_t \*flag_buf = get_buf_ptr(buf, VIRGL_SET_DEBUG_FLAGSTRING_OFFSET);  
   flagstring = malloc(slen+1);  
  
   if (!flagstring) {  
      return ENOMEM;  
   }  
  
   memcpy(flagstring, flag_buf, slen); -->  
   flagstring[slen] = 0;  
   vrend_context_set_debug_flags(ctx, flagstring);  
  
   free(flagstring);  
  
   return 0;  
}  

```

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/virglrenderer/src/vrend_decode.c;l=369-384?q=src%2Fvrend_decode.c>

```
...  
      VREND_DEBUG(dbg_cmd, gdctx->grctx, "%-4d %-20s len:%d\n",  
                  cur_offset, vrend_get_comand_name(cmd), len);  
  
      TRACE_SCOPE_SLOW(vrend_get_comand_name(cmd));  
  
      ret = decode_table[cmd](gdctx->grctx, buf, len);  --> here  
      if (!vrend_check_no_error(gdctx->grctx) && !ret)  
         ret = EINVAL;  
      if (ret) {  
         vrend_printf("context %d failed to dispatch %s: %d\n",  
               gdctx->base.ctx_id, vrend_get_comand_name(cmd), ret);  
         if (ret == EINVAL)  
            vrend_report_buffer_error(gdctx->grctx, \*buf);  
         return ret;  
      }  

```

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/virglrenderer/src/virglrenderer.c;l=271-290?q=virglrenderer>

```
void virgl_renderer_context_destroy(uint32_t handle)  
{  
   TRACE_FUNC();  
   virgl_context_remove(handle);  
}  
  
int virgl_renderer_submit_cmd(void \*buffer,  
                              int ctx_id,  
                              int ndw)  
{  
   TRACE_FUNC();  
   struct virgl_context \*ctx = virgl_context_lookup(ctx_id);  
   if (!ctx)  
      return EINVAL;  
  
   if (ndw < 0 || (unsigned)ndw > UINT32_MAX / sizeof(uint32_t))  
      return EINVAL;  
  
   return ctx->submit_cmd(ctx, buffer, ndw \* sizeof(uint32_t));  
}  

```

1. The variable `slen` is calculated as `sizeof(uint32_t) \* length`, and then `flagstring` is allocated with a size of `slen + 1`. This is appropriate, as slen bytes are allocated for the content, plus one for the null terminator.
2. The value of `flag_buf` is obtained from a function `get_buf_ptr(buf, VIRGL_SET_DEBUG_FLAGSTRING_OFFSET)`. If this function returns a pointer to a region of memory that is smaller than slen, the memcpy call will read beyond the end of the buffer pointed to by flag\_buf, causing undefined behavior.

**Additional Comments:**  

cros stable version maybe effect but I tested on dev M117

\*\*Chrome version: \*\* 117.0.5928.0 \*\*Channel: \*\* Dev

**OS:** Chrome OS

## Timeline

### rh...@gmail.com (2023-08-07)

asan_log:

```
=================================================================
==29557==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x50d0000a53d1 at pc 0x578cde2857cd bp 0x7ffd2fe644e0 sp 0x7ffd2fe63ca8
READ of size 32 at 0x50d0000a53d1 thread T0
SCARINESS: 26 (multi-byte-read-heap-buffer-overflow)
    #0 0x578cde2857cc in __asan_memcpy ??:0:0
    #1 0x7eddaa0ebb18 in vrend_decode_set_debug_mask /build/atlas/tmp/portage/media-libs/virglrenderer-9999/work/virglrenderer-9999-build/../virglrenderer-9999/src/vrend_decode.c:1365:4
    #2 0x7eddaa0e41bb in vrend_decode_ctx_submit_cmd /build/atlas/tmp/portage/media-libs/virglrenderer-9999/work/virglrenderer-9999-build/../virglrenderer-9999/src/vrend_decode.c:1934:13
    #3 0x7eddaa0cfe46 in virgl_renderer_submit_cmd /build/atlas/tmp/portage/media-libs/virglrenderer-9999/work/virglrenderer-9999-build/../virglrenderer-9999/src/virglrenderer.c:289:11
    #4 0x578cde2b5bb7 in LLVMFuzzerTestOneInput /build/atlas/tmp/portage/media-libs/virglrenderer-9999/work/virglrenderer-9999-build/../virglrenderer-9999/tests/fuzzer/test1.c:207:13
    #5 0x578cde1b97e0 in _ZN6fuzzer6Fuzzer15ExecuteCallbackEPKhm ??:?
    #6 0x578cde1b9005 in _ZN6fuzzer6Fuzzer6RunOneEPKhmbPNS_9InputInfoEbPb ??:?
    #7 0x578cde1ba5d5 in _ZN6fuzzer6Fuzzer16MutateAndTestOneEv ??:?
    #8 0x578cde1bb3e5 in _ZN6fuzzer6Fuzzer4LoopERNSt8__Fuzzer6vectorINS_9SizedFileENS1_9allocatorIS3_EEEE ??:?
    #9 0x578cde1a93f5 in _ZN6fuzzer12FuzzerDriverEPiPPPcPFiPKhmE ??:?
    #10 0x578cde1d4b72 in main ??:?
    #11 0x7edda9d396c5 in __libc_start_call_main /var/tmp/portage/cross-x86_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #12 0x7edda9d39781 in __libc_start_main@GLIBC_2.2.5 /var/tmp/portage/cross-x86_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../csu/libc-start.c:389:3
    #13 0x578cde19b440 in _start ??:?

0x50d0000a53d1 is located 0 bytes after 65-byte region [0x50d0000a5390,0x50d0000a53d1)
allocated by thread T0 here:
    #0 0x578cde28634e in __interceptor_malloc ??:0:0
    #1 0x578cde1d5bb6 in _Znwm ??:?
    #2 0x578cde1b9005 in _ZN6fuzzer6Fuzzer6RunOneEPKhmbPNS_9InputInfoEbPb ??:?
    #3 0x578cde1ba5d5 in _ZN6fuzzer6Fuzzer16MutateAndTestOneEv ??:?
    #4 0x578cde1bb3e5 in _ZN6fuzzer6Fuzzer4LoopERNSt8__Fuzzer6vectorINS_9SizedFileENS1_9allocatorIS3_EEEE ??:?
    #5 0x578cde1a93f5 in _ZN6fuzzer12FuzzerDriverEPiPPPcPFiPKhmE ??:?
    #6 0x578cde1d4b72 in main ??:?
    #7 0x7edda9d396c5 in __libc_start_call_main /var/tmp/portage/cross-x86_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #8 0x7edda9d39781 in __libc_start_main@GLIBC_2.2.5 /var/tmp/portage/cross-x86_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../csu/libc-start.c:389:3
    #9 0x578cde19b440 in _start ??:?

SUMMARY: AddressSanitizer: heap-buffer-overflow (/usr/libexec/fuzzers/test1+0x1447cc) (BuildId: 1ccaa8c14e47ad35)
Shadow bytes around the buggy address:
  0x50d0000a5100: fa fa fa fa fd fd fd fd fd fd fd fd fd fa fa fa
  0x50d0000a5180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fd fd
  0x50d0000a5200: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x50d0000a5280: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x50d0000a5300: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x50d0000a5380: fa fa 00 00 00 00 00 00 00 00[01]fa fa fa fa fa
  0x50d0000a5400: fa fa fa fa fa fa fa fa fa fa fa fa fd fd fd fd
  0x50d0000a5480: fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa
  0x50d0000a5500: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fa
  0x50d0000a5580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x50d0000a5600: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
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
==29557==ABORTING

```

### rh...@gmail.com (2023-08-07)

I reported to virglrenderer 2 days ago on https://gitlab.freedesktop.org/virgl/virglrenderer/-/issues/370

### [Deleted User] (2023-08-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-08)

virGL renderer in ChromeOS, over to cros for triage 

### ch...@google.com (2023-08-08)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/294923710). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/294923710]

### [Deleted User] (2023-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-06)

[Empty comment from Monorail migration]

### rh...@gmail.com (2023-09-13)

Given that the issue has been resolved in the bug tracker, may we mark this as "Fixed"? This will enable it to proceed to the next panel for consideration

### ch...@google.com (2023-09-13)

Dear rhezashan@gmail.com,

We are still waiting for verification of the fix.
I'll resolve the bug as soon as the verification process is done! 



### rh...@gmail.com (2023-09-13)

Thanks for the update chmiel@, sorry for asking that kind of question.

### ch...@google.com (2023-09-18)

Exploitability - Reporter uploaded the ASAN trace to show the buffer overflow. This is enough to show the exploitability.

Privileges and Capabilities - No sandbox escape. Exploit targets within the VM

Origin of fix - This was reported to upstream by the reporter of this https://crbug.com/chromium/2 days before this report. No fix suggested by the reporter. On the other hand the reporter explained the problem causing the buffer overflow clearly, which helps with the fix.

Mitigations - VM escapes are low possibility so this is considered highly mitigated.

Severity assessment - Heap OOB read in the crosvm is considered medium severity. Not high because there isn't any VM escape or privileges gained. Not lower because sensitive data within the VM boundary can be leaked with a potential attack.

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-12-07)

[Empty comment from Monorail migration]

### rh...@gmail.com (2023-12-07)

Hi chmiel@,

Thanks a lot for the reward in early December, also for ChromeOS VRP team and developer. Thank you so much

### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-25)

This issue was migrated from crbug.com/chromium/1470827?no_tracker_redirect=1

[Monorail blocking: b/294923710]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40068966)*
