# Security: Heap buffer overflow due to Integer Overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [40069462](https://issues.chromium.org/issues/40069462) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | bu...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-08-13 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

When handling the VIRGL\_CMD\_RESOURCE\_COPY\_REGION\_SIZE command, `vrend_resource_copy_fallback` function will be invoked eventually(<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/virglrenderer/src/vrend_renderer.c;l=10246>).

Specifically, `total_size` and `slice_size` are 32-bit integer. It's possible to trigger the Integer overflow issue at the point[1] and [2]. So the buffer allocated at the point[3] can be problematic. Meanwhile, integer overflow issues can also occur in other functions like `read_transfer_data` at the point[4].

```
static void vrend_resource_copy_fallback(struct vrend_resource \*src_res,  
                                         struct vrend_resource \*dst_res,  
                                         uint32_t dst_level,  
                                         uint32_t dstx, uint32_t dsty,  
                                         uint32_t dstz, uint32_t src_level,  
                                         const struct pipe_box \*src_box)  
{  
   uint32_t total_size, src_stride, dst_stride, src_layer_stride;  
   // ...  
   uint32_t slice_size, slice_offset;  
  
   slice_size = util_format_get_nblocks(src_res->base.format, u_minify(src_res->base.width0, src_level), u_minify(src_res->base.height0, src_level)) \* util_format_get_blocksize(src_res->base.format); // [1]  
     
   total_size = slice_size \* vrend_get_texture_depth(src_res, src_level); // [2]  
  
   tptr = malloc(total_size); // [3]  
   // ...  
}  

```
```
static void read_transfer_data(const struct iovec \*iov,  
                               unsigned int num_iovs,  
                               char \*data,  
                               enum virgl_formats format,  
                               uint64_t offset,  
                               uint32_t src_stride,  
                               uint32_t src_layer_stride,  
                               struct pipe_box \*box,  
                               bool invert)  
{  
   int blsize = util_format_get_blocksize(format);  
   uint32_t size = vrend_get_iovec_size(iov, num_iovs);  
   uint32_t send_size = util_format_get_nblocks(format, box->width,  
                                              box->height) \* blsize \* box->depth; // [4]  
   // ...  

```

**VERSION**

virglrenderer-0.10.4

**REPRODUCTION CASE**

1. Put the test\_oob.c into test/fuzzer, apply the build.diff and build the test
2. Run the test\_oob bin. The ASAN log can be like:

=================================================================  

==72494==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f94578757fe at pc 0x000000432554 bp 0x7ffd2de6aa40 sp 0x7ffd2de6a200  

READ of size 2 at 0x7f94578757fe thread T0  

#0 0x432553 in memcpy (/tmp/virglrenderer/build/tests/fuzzer/test\_oob+0x432553)  

#1 0x7f957377f899 (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0x20c899)  

#2 0x7f9573d5f68e (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0x7ec68e)  

#3 0x7f9574384a32 (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0xe11a32)  

#4 0x7f9573787421 (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0x214421)  

#5 0x7f9573934a1e (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0x3c1a1e)  

#6 0x7f9573937958 (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0x3c4958)  

#7 0x7f957393d698 (/usr/lib/x86\_64-linux-gnu/dri/swrast\_dri.so+0x3ca698)  

#8 0x7f957900eb06 in vrend\_renderer\_resource\_copy\_region (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x29b06)  

#9 0x7f9578ffadd2 in vrend\_decode\_resource\_copy\_region (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x15dd2)  

#10 0x7f9578ff9ada in vrend\_decode\_ctx\_submit\_cmd (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x14ada)  

#11 0x4c8abb in main (/tmp/virglrenderer/build/tests/fuzzer/test\_oob+0x4c8abb)  

#12 0x7f9578b2a082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16  

#13 0x41c31d in \_start (/tmp/virglrenderer/build/tests/fuzzer/test\_oob+0x41c31d)

0x7f94578757fe is located 0 bytes to the right of 4294967294-byte region [0x7f9357875800,0x7f94578757fe)  

allocated by thread T0 here:  

#0 0x49757d in malloc (/tmp/virglrenderer/build/tests/fuzzer/test\_oob+0x49757d)  

#1 0x7f957900e4c1 in vrend\_renderer\_resource\_copy\_region (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x294c1)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/tmp/virglrenderer/build/tests/fuzzer/test\_oob+0x432553) in memcpy  

Shadow bytes around the buggy address:  

0x0ff30af06aa0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff30af06ab0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff30af06ac0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff30af06ad0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ff30af06ae0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0ff30af06af0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00[06]  

0x0ff30af06b00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0ff30af06b10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0ff30af06b20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0ff30af06b30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0ff30af06b40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==72494==ABORTING

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [build.diff](attachments/build.diff) (text/plain, 559 B)
- [log_helper.diff](attachments/log_helper.diff) (text/plain, 1.3 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 1.5 KB)
- [test_oob_asan.txt](attachments/test_oob_asan.txt) (text/plain, 3.1 KB)
- [test_oob.c](attachments/test_oob.c) (text/plain, 8.0 KB)

## Timeline

### [Deleted User] (2023-08-13)

[Empty comment from Monorail migration]

### bu...@gmail.com (2023-08-13)

`read_transfer_data` can be invoked by `vrend_resource_copy_fallback` at the point[5].


```
static void vrend_resource_copy_fallback(struct vrend_resource *src_res,
                                         struct vrend_resource *dst_res,
                                         uint32_t dst_level,
                                         uint32_t dstx, uint32_t dsty,
                                         uint32_t dstz, uint32_t src_level,
                                         const struct pipe_box *src_box)
{
   char *tptr;
   uint32_t total_size, src_stride, dst_stride, src_layer_stride;
   GLenum glformat, gltype;
   int elsize = util_format_get_blocksize(dst_res->base.format);
   int compressed = util_format_is_compressed(dst_res->base.format);
   int cube_slice = 1;
   uint32_t slice_size, slice_offset;
   int i;
   struct pipe_box box;

   if (src_res->target == GL_TEXTURE_CUBE_MAP)
      cube_slice = 6;

   if (src_res->base.format != dst_res->base.format) {
      virgl_error("Copy fallback failed due to mismatched formats %d %d\n", src_res->base.format, dst_res->base.format);
      return;
   }

   box = *src_box;
   box.depth = vrend_get_texture_depth(src_res, src_level);
   dst_stride = util_format_get_stride(dst_res->base.format, dst_res->base.width0);

   /* this is ugly need to do a full GetTexImage */
   slice_size = util_format_get_nblocks(src_res->base.format, u_minify(src_res->base.width0, src_level), u_minify(src_res->base.height0, src_level)) *
                util_format_get_blocksize(src_res->base.format);
   total_size = slice_size * vrend_get_texture_depth(src_res, src_level);

   tptr = malloc(total_size);
   if (!tptr)
      return;

   glformat = tex_conv_table[src_res->base.format].glformat;
   gltype = tex_conv_table[src_res->base.format].gltype;

   if (compressed)
      glformat = tex_conv_table[src_res->base.format].internalformat;

   /* If we are on gles we need to rely on the textures backing
    * iovec to have the data we need, otherwise we can use glGetTexture
    */
   if (vrend_state.use_gles) {
      uint64_t src_offset = 0;
      uint64_t dst_offset = 0;
      if (src_level < VR_MAX_TEXTURE_2D_LEVELS) {
         src_offset = src_res->mipmap_offsets[src_level];
         dst_offset = dst_res->mipmap_offsets[src_level];
      }

      src_stride = util_format_get_nblocksx(src_res->base.format,
                                            u_minify(src_res->base.width0, src_level)) * elsize;
      src_layer_stride = util_format_get_2d_size(src_res->base.format,
                                                 src_stride,
                                                 u_minify(src_res->base.height0, src_level));
      read_transfer_data(src_res->iov, src_res->num_iovs, tptr,
                         src_res->base.format, src_offset,
                         src_stride, src_layer_stride, &box, false); // [5]
``` 

### pg...@google.com (2023-08-13)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-14)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/295801194). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/295801194]

### [Deleted User] (2023-08-14)

[Empty comment from Monorail migration]

### bu...@gmail.com (2023-08-15)

When I upload the PATCH.diff, I find that I uploaded the wrong POC and ASAN info. Sorry for the inconvenience. 

Based on the above analysis, we can set the `args.width = 0x80000001;`. So both `slice_size` and `total_size ` is 2.  Consequently, Heap buffer overflow is triggered at the point[5]. You can apply the log_helper.diff patch to confirm this issue clearly. The log looks like:

```
gl_version 32 - es profile enabled
slice_size: 2, total_size: 2
blsize: 2, size: 200, send_size: 9320, bwx: 9320, bh: 1
num_iovs: 2, offset: 0, data: 602000024330, send_size: 2468
```

```
static void read_transfer_data(const struct iovec *iov,
                               unsigned int num_iovs,
                               char *data,
                               enum virgl_formats format,
                               uint64_t offset,
                               uint32_t src_stride,
                               uint32_t src_layer_stride,
                               struct pipe_box *box,
                               bool invert)
{
   int blsize = util_format_get_blocksize(format);
   uint32_t size = vrend_get_iovec_size(iov, num_iovs);
   uint32_t send_size = util_format_get_nblocks(format, box->width,
                                              box->height) * blsize * box->depth;
   uint32_t bwx = util_format_get_nblocksx(format, box->width) * blsize;
   int32_t bh = util_format_get_nblocksy(format, box->height);
   int d, h;

   if ((send_size == size || bh == 1) && !invert && box->depth == 1)
      vrend_read_from_iovec(iov, num_iovs, offset, data, send_size); // [5]
   else {
      if (invert) {
  // ..
```

The ASAN should be like:

=================================================================
==107848==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000024332 at pc 0x0000004326b3 bp 0x7ffc62daaa80 sp 0x7ffc62daa240
WRITE of size 100 at 0x602000024332 thread T0
    #0 0x4326b2 in memcpy (/tmp/virglrenderer/build/tests/fuzzer/test_oob+0x4326b2)
    #1 0x7f6c5672dd33 in vrend_read_from_iovec (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x13d33)
    #2 0x7f6c5674a817 in read_transfer_data (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x30817)
    #3 0x7f6c56743607 in vrend_renderer_resource_copy_region (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x29607)
    #4 0x7f6c5672fde2 in vrend_decode_resource_copy_region (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x15de2)
    #5 0x7f6c5672eaea in vrend_decode_ctx_submit_cmd (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x14aea)
    #6 0x4c8b15 in main (/tmp/virglrenderer/build/tests/fuzzer/test_oob+0x4c8b15)
    #7 0x7f6c5625f082 in __libc_start_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16
    #8 0x41c33d in _start (/tmp/virglrenderer/build/tests/fuzzer/test_oob+0x41c33d)

0x602000024332 is located 0 bytes to the right of 2-byte region [0x602000024330,0x602000024332)
allocated by thread T0 here:
    #0 0x49759d in malloc (/tmp/virglrenderer/build/tests/fuzzer/test_oob+0x49759d)
    #1 0x7f6c567434bf in vrend_renderer_resource_copy_region (/tmp/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x294bf)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/tmp/virglrenderer/build/tests/fuzzer/test_oob+0x4326b2) in memcpy
Shadow bytes around the buggy address:
  0x0c047fffc810: fa fa fd fd fa fa 00 04 fa fa 00 00 fa fa 04 fa
  0x0c047fffc820: fa fa 00 00 fa fa 00 04 fa fa 04 fa fa fa 00 fa
  0x0c047fffc830: fa fa 00 04 fa fa 00 00 fa fa 00 04 fa fa 00 00
  0x0c047fffc840: fa fa 04 fa fa fa 00 00 fa fa 00 04 fa fa 04 fa
  0x0c047fffc850: fa fa 00 fa fa fa 00 04 fa fa 00 00 fa fa 01 fa
=>0x0c047fffc860: fa fa 00 00 fa fa[02]fa fa fa fa fa fa fa fa fa
  0x0c047fffc870: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffc880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffc890: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffc8a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fffc8b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
  Shadow gap:              cc
==107848==ABORTING

I like the following patch can fix this issue:

diff --git a/src/vrend_renderer.c b/src/vrend_renderer.c
index d8ffec8..6919398 100644
--- a/src/vrend_renderer.c
+++ b/src/vrend_renderer.c
@@ -10004,12 +10004,12 @@ static void vrend_resource_copy_fallback(struct vrend_resource *src_res,
                                          const struct pipe_box *src_box)
 {
    char *tptr;
-   uint32_t total_size, src_stride, dst_stride, src_layer_stride;
+   uint64_t total_size, src_stride, dst_stride, src_layer_stride;
    GLenum glformat, gltype;
    int elsize = util_format_get_blocksize(dst_res->base.format);
    int compressed = util_format_is_compressed(dst_res->base.format);
    int cube_slice = 1;
-   uint32_t slice_size, slice_offset;
+   uint64_t slice_size, slice_offset;
    int i;
    struct pipe_box box;
 
@@ -10026,8 +10026,8 @@ static void vrend_resource_copy_fallback(struct vrend_resource *src_res,
    dst_stride = util_format_get_stride(dst_res->base.format, dst_res->base.width0);
 
    /* this is ugly need to do a full GetTexImage */
-   slice_size = util_format_get_nblocks(src_res->base.format, u_minify(src_res->base.width0, src_level), u_minify(src_res->base.height0, src_level)) *
-                util_format_get_blocksize(src_res->base.format);
+   slice_size = util_format_get_nblocks(src_res->base.format, u_minify(src_res->base.width0, src_level), u_minify(src_res->base.height0, src_level));
+   slice_size *= util_format_get_blocksize(src_res->base.format);
    total_size = slice_size * vrend_get_texture_depth(src_res, src_level);
 
    tptr = malloc(total_size);



### ch...@google.com (2023-10-10)

Verified by 
ChromeOS-security-vm-rotation@google.com.
Exploitability - Integer overflow leads to incorrect size/bound check --> Potential out of bound write. However, it is unclear how malicious code can manipulate the input sizes.
Privileges and Capabilities - Out of bound write in the renderer process means privilege escalation.
Origin of fix - Fixed by virgl developer.
Mitigations - better bound check of a box.
Severity assessment - Medium, if successfully exploited by a PoC, it will be of critical severity or high. It is assessed that this bug needs to be combined with other bugs so the box bound can be manipulated to be a very very big value, which is unlikely in the normal usage.

### ch...@google.com (2023-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-10)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-18)

Congratulations! 
The VRP Panel has decided to award you $5000 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions

### ch...@google.com (2023-10-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-16)

This issue was migrated from crbug.com/chromium/1472566?no_tracker_redirect=1

[Monorail blocking: b/295801194]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069462)*
