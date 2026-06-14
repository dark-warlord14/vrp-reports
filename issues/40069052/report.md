# Security: virglrenderer | heap-buffer-overflow on vrend_set_constants

| Field | Value |
|-------|-------|
| **Issue ID** | [40069052](https://issues.chromium.org/issues/40069052) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-08-08 |
| **Bounty** | $4,000.00 |

## Description

**Steps to reproduce the problem:**  

Steps to reproduce the problem:

1. tested on google pixelbook go, build fuzzer and run with iris gpu

**Problem Description:**  

There's maybe missing boundary checking for following code that may lead to heap-buffer-overflow.  

Tested on real devices chromebook (Chromium 117.0.5928.0) with latest virglrenderer version under asan.

There's maybe missing boundary checking for following code that may lead to heap-buffer-overflow.  

Tested on real devices chromebook (Chromium 117.0.5928.0) with latest virglrenderer version under asan.

Few of error stack couldn't be symbolized due some technical environment.

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/virglrenderer/src/vrend_renderer.c;l=3403-3427?q=vrend_renderer.c>

```
void vrend_set_constants(struct vrend_context \*ctx,  
                         uint32_t shader,  
                         uint32_t num_constant,  
                         const float \*data)  
{  
   struct vrend_constants \*consts;  
  
   consts = &ctx->sub->consts[shader];  
   ctx->sub->const_dirty[shader] = true;  
  
   /\* avoid reallocations by only growing the buffer \*/  
   if (consts->num_allocated_consts < num_constant) {  
      free(consts->consts);  
      consts->consts = malloc(num_constant \* sizeof(float));  
      if (!consts->consts) {  
         consts->num_allocated_consts = 0;  
         return;  
      }  
  
      consts->num_allocated_consts = num_constant;  
   }  
  
   memcpy(consts->consts, data, num_constant \* sizeof(unsigned int)); --> here  
   consts->num_consts = num_constant;  
}  

```

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/virglrenderer/src/vrend_decode.c;l=279-295?q=vrend_decode.c&ss=chromiumos%2Fchromiumos%2Fcodesearch>

```
static int vrend_decode_set_constant_buffer(struct vrend_context \*ctx, const uint32_t \*buf, uint32_t length)  
{  
   uint32_t shader;  
   int nc = (length - 2);  
  
   if (length < 2)  
      return EINVAL;  
  
   shader = get_buf_entry(buf, VIRGL_SET_CONSTANT_BUFFER_SHADER_TYPE);  
   /\* VIRGL_SET_CONSTANT_BUFFER_INDEX is not used \*/  
  
   if (shader >= PIPE_SHADER_TYPES)  
      return EINVAL;  
  
   vrend_set_constants(ctx, shader, nc, get_buf_ptr(buf, VIRGL_SET_CONSTANT_BUFFER_DATA_START));  --> then here  
   return 0;  
}  

```

- in the function `vrend_set_constants`, the memory for `consts->consts` is allocated based on the value of `num_constant`. The size allocated is `num_constant \* sizeof(float)`.
- data is copied to this memory using memcpy based on the size `num_constant \* sizeof(unsigned int)`.
- the size passed to memcpy is based on unsigned int while the memory allocated for consts->consts is based on float. This can cause a problem if the sizes of float and unsigned int are different on other platform.
- the length argument in `vrend_decode_set_constant_buffer` is smaller than expected, the calculation for nc (number of constants) could produce a larger value than intended, which could then lead to copying more data than the allocated size.

bisect: <https://source.chromium.org/chromiumos/_/chromium/chromiumos/third_party/virglrenderer/+/c1b6c98589747e66e8b2b8db6b1e746498e7f552>

**Additional Comments:**

\*\*Chrome version: \*\* 117.0.5928.0 \*\*Channel: \*\* Dev

**OS:** Chrome OS

## Attachments

- [virgl-sub-issue-371.png](attachments/virgl-sub-issue-371.png) (image/png, 94.0 KB)

## Timeline

### rh...@gmail.com (2023-08-08)

asan_log:

=================================================================
==24009==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x504000037200 at pc 0x572938fdc82d bp 0x7ffd0a65d420 sp 0x7ffd0a65cbe8
READ of size 51284 at 0x504000037200 thread T0
SCARINESS: 26 (multi-byte-read-heap-buffer-overflow)
    #0 0x572938fdc82c in __asan_memcpy ??:0:0
    #1 0x7fdcb51e74e8 in vrend_set_constants /build/atlas/tmp/portage/media-libs/virglrenderer-9999/work/virglrenderer-9999-build/../virglrenderer-9999/src/vrend_renderer.c:3425:4
    #2 0x7fdcb51d5f2e in vrend_decode_set_constant_buffer /build/atlas/tmp/portage/media-libs/virglrenderer-9999/work/virglrenderer-9999-build/../virglrenderer-9999/src/vrend_decode.c:293:4
    #3 0x7fdcb51d15cb in vrend_decode_ctx_submit_cmd /build/atlas/tmp/portage/media-libs/virglrenderer-9999/work/virglrenderer-9999-build/../virglrenderer-9999/src/vrend_decode.c:1934:13
    #4 0x7fdcb51bd3a2 in virgl_renderer_submit_cmd /build/atlas/tmp/portage/media-libs/virglrenderer-9999/work/virglrenderer-9999-build/../virglrenderer-9999/src/virglrenderer.c:289:11
    #5 0x57293900cb51 in LLVMFuzzerTestOneInput /build/atlas/tmp/portage/media-libs/virglrenderer-9999/work/virglrenderer-9999-build/../virglrenderer-9999/tests/fuzzer/test5.c:188:10
    #6 0x572938f10840 in _ZN6fuzzer6Fuzzer15ExecuteCallbackEPKhm ??:?
    #7 0x572938f10065 in _ZN6fuzzer6Fuzzer6RunOneEPKhmbPNS_9InputInfoEbPb ??:?
    #8 0x572938f11635 in _ZN6fuzzer6Fuzzer16MutateAndTestOneEv ??:?
    #9 0x572938f12445 in _ZN6fuzzer6Fuzzer4LoopERNSt8__Fuzzer6vectorINS_9SizedFileENS1_9allocatorIS3_EEEE ??:?
    #10 0x572938f00455 in _ZN6fuzzer12FuzzerDriverEPiPPPcPFiPKhmE ??:?
    #11 0x572938f2bbd2 in main ??:?
    #12 0x7fdcb4e226c5 in __libc_start_call_main /var/tmp/portage/cross-x86_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #13 0x7fdcb4e22781 in __libc_start_main@GLIBC_2.2.5 /var/tmp/portage/cross-x86_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../csu/libc-start.c:389:3
    #14 0x572938ef24a0 in _start ??:?

0x504000037200 is located 0 bytes after 48-byte region [0x5040000371d0,0x504000037200)
allocated by thread T0 here:
    #0 0x572938fdd3ae in __interceptor_malloc ??:0:0
    #1 0x572938f2cc16 in _Znwm ??:?
    #2 0x572938f10065 in _ZN6fuzzer6Fuzzer6RunOneEPKhmbPNS_9InputInfoEbPb ??:?
    #3 0x572938f11635 in _ZN6fuzzer6Fuzzer16MutateAndTestOneEv ??:?
    #4 0x572938f12445 in _ZN6fuzzer6Fuzzer4LoopERNSt8__Fuzzer6vectorINS_9SizedFileENS1_9allocatorIS3_EEEE ??:?
    #5 0x572938f00455 in _ZN6fuzzer12FuzzerDriverEPiPPPcPFiPKhmE ??:?
    #6 0x572938f2bbd2 in main ??:?
    #7 0x7fdcb4e226c5 in __libc_start_call_main /var/tmp/portage/cross-x86_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #8 0x7fdcb4e22781 in __libc_start_main@GLIBC_2.2.5 /var/tmp/portage/cross-x86_64-cros-linux-gnu/glibc-2.35-r22/work/glibc-2.35/csu/../csu/libc-start.c:389:3
    #9 0x572938ef24a0 in _start ??:?

SUMMARY: AddressSanitizer: heap-buffer-overflow (/usr/libexec/fuzzers/test5+0x14482c) (BuildId: 1e547e3fcfb44790)
Shadow bytes around the buggy address:
  0x504000036f80: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa
  0x504000037000: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa
  0x504000037080: fa fa fd fd fd fd fd fa fa fa fd fd fd fd fd fa
  0x504000037100: fa fa fd fd fd fd fd fd fa fa fd fd fd fd fd fd
  0x504000037180: fa fa fd fd fd fd fd fd fa fa 00 00 00 00 00 00
=>0x504000037200:[fa]fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x504000037280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x504000037300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x504000037380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x504000037400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x504000037480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
==24009==ABORTING


### [Deleted User] (2023-08-08)

[Empty comment from Monorail migration]

### rh...@gmail.com (2023-08-08)

This bug is sub issue from https://gitlab.freedesktop.org/virgl/virglrenderer/-/issues/371.
I *think* the developer fixes the sub issue earlier than the main bug. 

The fix has landed for sub issue in virglrenderer on main https://gitlab.freedesktop.org/virgl/virglrenderer/-/merge_requests/1194

### rh...@gmail.com (2023-08-08)

information:

the main issue for https://gitlab.freedesktop.org/virgl/virglrenderer/-/issues/371 is crbug.com/1470824.
I am taking the initiative to report in two separate reports between the main issue and the sub-issue.


### bb...@google.com (2023-08-08)

Setting OS-Chrome and Tenative prio 1 as per crbug.com/1470824, as these seem intimately related and want the fix from upstream. 

### ch...@google.com (2023-08-09)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/295109386). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/295109386]

### [Deleted User] (2023-08-09)

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

Exploitability - Reporter uploaded the ASAN trace that shows the buffer overflow.

Privileges and Capabilities - No sandbox escape, no privileges gained. Exploit targets OOB read within the VM

Origin of fix - Reporter is the original reporter. No fix suggested by the reporter. On the other hand the reporter explained the problem causing the buffer overflow clearly, which helps with the fix.

Mitigations - VM escapes are low possibility so this is considered highly mitigated.

Severity assessment - Heap OOB read in the crosvm is considered medium severity. Not high because there isn't any VM escape or privileges gained. Not lower because sensitive data within the VM boundary can be leaked with a potential attack.

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-12-06)

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

This issue was migrated from crbug.com/chromium/1471158?no_tracker_redirect=1

[Monorail blocking: b/295109386]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069052)*
