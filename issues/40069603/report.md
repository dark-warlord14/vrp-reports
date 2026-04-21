# Security: Heap buffer overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [40069603](https://issues.chromium.org/issues/40069603) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | bu...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-08-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Please note that this issue is totaly different from the <https://crbug.com/chromium/1472566>.

When handling the VIRGL\_CMD\_RESOURCE\_COPY\_REGION\_SIZE command, `vrend_resource_copy_fallback` function will be invoked eventually(<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/virglrenderer/src/vrend_renderer.c;l=10246>).

Specifically, `slice_size` is computed at the point[1]. If `res->target` is not `GL_TEXTURE_3D`, the function `vrend_get_texture_depth` will return 1 as the value of `depth`. So `total_size` is equal to `slice_size` at the point[2]. And the length of buffer `tptr` is `slice_size` at the point[3]. At the end of the function `vrend_resource_copy_fallback`, it invokes the functions `glTexSubImage` at the points[5-9]. Specifically, `tptr + slice_offset` is passed to those funtions. `slice_offset` is computed at the point[4]. Since the depth is 1, the value of `src_box->z`can be set to 1. Now `tptr + slice_offset` is pointed to the end of the buffer. So Heap buffer overflow occurs. (Assume the value of `slice_size` is 4 and the address of `tptr` is '0x1234000'. So the value of `slice_offset` is also 4. Now `tptr + slice_offset` is `0x1234004`, which is out of range`[0x1234000, 0x1234004)`.)

```
static uint32_t vrend_get_texture_depth(struct vrend_resource \*res, uint32_t level)  
{  
   uint32_t depth = 1; // [10]  
   if (res->target == GL_TEXTURE_3D)  
      depth = u_minify(res->base.depth0, level);  
   else if (res->target == GL_TEXTURE_1D_ARRAY || res->target == GL_TEXTURE_2D_ARRAY ||  
            res->target == GL_TEXTURE_CUBE_MAP || res->target == GL_TEXTURE_CUBE_MAP_ARRAY)  
      depth = res->base.array_size;  
  
   return depth;  
}  
  
static void vrend_resource_copy_fallback(struct vrend_resource \*src_res,  
                                         struct vrend_resource \*dst_res,  
                                         uint32_t dst_level,  
                                         uint32_t dstx, uint32_t dsty,  
                                         uint32_t dstz, uint32_t src_level,  
                                         const struct pipe_box \*src_box)  
{  
   // ...  
   slice_size = util_format_get_nblocks(src_res->base.format, u_minify(src_res->base.width0, src_level), u_minify(src_res->base.height0, src_level)) \* util_format_get_blocksize(src_res->base.format); // [1]  
     
   total_size = slice_size \* vrend_get_texture_depth(src_res, src_level); // [2]  
  
   tptr = malloc(total_size); // [3]  
   // ...  
  
   slice_offset = src_box->z \* slice_size; // [4]  
   cube_slice = (src_res->target == GL_TEXTURE_CUBE_MAP) ? src_box->z + src_box->depth : cube_slice;  
   i = (src_res->target == GL_TEXTURE_CUBE_MAP) ? src_box->z : 0;  
   for (; i < cube_slice; i++) {  
      GLenum ctarget = dst_res->target == GL_TEXTURE_CUBE_MAP ?  
                          (GLenum)(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i) : dst_res->target;  
      if (compressed) {  
         if (ctarget == GL_TEXTURE_1D) {  
            glCompressedTexSubImage1D(ctarget, dst_level, dstx,  
                                      src_box->width,  
                                      glformat, slice_size, tptr + slice_offset); // [5]  
         } else {  
            glCompressedTexSubImage2D(ctarget, dst_level, dstx, dsty,  
                                      src_box->width, src_box->height,  
                                      glformat, slice_size, tptr + slice_offset); // [6]  
         }  
      } else {  
         if (ctarget == GL_TEXTURE_1D) {  
            glTexSubImage1D(ctarget, dst_level, dstx, src_box->width, glformat, gltype, tptr + slice_offset); // [7]  
         } else if (ctarget == GL_TEXTURE_3D ||  
                    ctarget == GL_TEXTURE_2D_ARRAY ||  
                    ctarget == GL_TEXTURE_CUBE_MAP_ARRAY) {  
            glTexSubImage3D(ctarget, dst_level, dstx, dsty, dstz, src_box->width, src_box->height, src_box->depth, glformat, gltype, tptr + slice_offset); // [8]  
         } else {  
            glTexSubImage2D(ctarget, dst_level, dstx, dsty, src_box->width, src_box->height, glformat, gltype, tptr + slice_offset); // [9]  
         }  
      }  
      slice_offset += slice_size;  
   }  
   // ...  
}  

```

**VERSION**

virglrenderer-0.10.4

**REPRODUCTION CASE**

1. Put the test\_oob.c into test/fuzzer, apply the build.diff and build the test
2. Run the test\_oob bin. The ASAN log can be like:

=================================================================  

==112556==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000024334 at pc 0x000000432564 bp 0x7ffe1333de20 sp 0x7ffe1333d5e0  

READ of size 2 at 0x602000024334 thread T0  

#0 0x432563 in memcpy (/tmp/virglrenderer/build/tests/fuzzer/test\_oob+0x432563)  

#1 0x7f4cb777f899 (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0x20c899)  

#2 0x7f4cb7d5f68e (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0x7ec68e)  

#3 0x7f4cb8384a32 (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0xe11a32)  

#4 0x7f4cb7787421 (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0x214421)  

#5 0x7f4cb7934a1e (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0x3c1a1e)  

#6 0x7f4cb7937958 (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0x3c4958)  

#7 0x7f4cb793d698 (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0x3ca698)  

#8 0x7f4cbcff0b56 in vrend\_renderer\_resource\_copy\_region (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x29b56)  

#9 0x7f4cbcfdcde2 in vrend\_decode\_resource\_copy\_region (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x15de2)  

#10 0x7f4cbcfdbaea in vrend\_decode\_ctx\_submit\_cmd (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x14aea)  

#11 0x4c8ac5 in main (/tmp/virglrenderer/build/tests/fuzzer/test\_oob+0x4c8ac5)  

#12 0x7f4cbcb0c082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16  

#13 0x41c32d in \_start (/tmp/virglrenderer/build/tests/fuzzer/test\_oob+0x41c32d)

0x602000024334 is located 0 bytes to the right of 4-byte region [0x602000024330,0x602000024334)  

allocated by thread T0 here:  

#0 0x49758d in malloc (/tmp/virglrenderer/build/tests/fuzzer/test\_oob+0x49758d)  

#1 0x7f4cbcff04d9 in vrend\_renderer\_resource\_copy\_region (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x294d9)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/tmp/virglrenderer/build/tests/fuzzer/test\_oob+0x432563) in memcpy  

Shadow bytes around the buggy address:  

0x0c047fffc810: fa fa fd fd fa fa 00 04 fa fa 00 00 fa fa 04 fa  

0x0c047fffc820: fa fa 00 00 fa fa 00 04 fa fa 04 fa fa fa 00 fa  

0x0c047fffc830: fa fa 00 04 fa fa 00 00 fa fa 00 04 fa fa 00 00  

0x0c047fffc840: fa fa 04 fa fa fa 00 00 fa fa 00 04 fa fa 04 fa  

0x0c047fffc850: fa fa 00 fa fa fa 00 04 fa fa 00 00 fa fa 01 fa  

=>0x0c047fffc860: fa fa 00 00 fa fa[04]fa fa fa fa fa fa fa fa fa  

0x0c047fffc870: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fffc880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fffc890: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fffc8a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fffc8b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

Shadow gap: cc  

==112556==ABORTING

## Attachments

- [test_oob_asan.txt](attachments/test_oob_asan.txt) (text/plain, 3.3 KB)
- [build.diff](attachments/build.diff) (text/plain, 559 B)
- [test_oob.c](attachments/test_oob.c) (text/plain, 7.6 KB)

## Timeline

### [Deleted User] (2023-08-15)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-08-16)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-17)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/296341505). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/296341505]

### [Deleted User] (2023-08-17)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-10)

Verified by 

jadmanski@google.com.
Exploitability: Test case that triggers sanitizer failure provided, no specific exploit.

Privileges and Capabilities: Can trigger read-past-the-end issue on heap. Does not seem to allow for control over the address or writes.

Origin of fix: Not known upstream until reported by the reporter.

Mitigations: VM escape is unlikely here.

Severity assessment: Medium severity. Allows limited read access, no write or execution.

### [Deleted User] (2023-10-10)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-18)

Congratulations! 
The VRP Panel has decided to award you $1000 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions

### am...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-16)

This issue was migrated from crbug.com/chromium/1473015?no_tracker_redirect=1

[Monorail blocking: b/296341505]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069603)*
