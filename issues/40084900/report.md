# Security: heap-buffer-overflow in opj_tcd_update_tile_data

| Field | Value |
|-------|-------|
| **Issue ID** | [40084900](https://issues.chromium.org/issues/40084900) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | [Deleted User] |
| **Assignee** | oc...@chromium.org |
| **Created** | 2016-07-20 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

A heap buffer overflow vulnerability is present in the openjpeg.

## File libopenjpeg20/tcd.c, line 1145:

OPJ\_UINT32 opj\_tcd\_get\_decoded\_tile\_size ( opj\_tcd\_t \*p\_tcd )  

{  

OPJ\_UINT32 i;  

OPJ\_UINT32 l\_data\_size = 0;  

opj\_image\_comp\_t \* l\_img\_comp = 00;  

opj\_tcd\_tilecomp\_t \* l\_tile\_comp = 00;  

opj\_tcd\_resolution\_t \* l\_res = 00;  

OPJ\_UINT32 l\_size\_comp, l\_remaining;

```
    l_tile_comp = p_tcd->tcd_image->tiles->comps;  
    l_img_comp = p_tcd->image->comps;  

    for (i=0;i<p_tcd->image->numcomps;++i) {    <--- `image->numcomps` is 0x10  
            l_size_comp = l_img_comp->prec >> 3; /\*(/ 8)\*/  
            l_remaining = l_img_comp->prec & 7;  /\* (%8) \*/  

            if(l_remaining) {  
                    ++l_size_comp;  
            }  

            if (l_size_comp == 3) {  
                    l_size_comp = 4;  
            }  

            l_res = l_tile_comp->resolutions + l_tile_comp->minimum_num_resolutions - 1;  
            l_data_size += l_size_comp \* (OPJ_UINT32)((l_res->x1 - l_res->x0) \* (l_res->y1 - l_res->y0));    <--- 0x4 or 0x10 \* (0x1064 \* 0x1064)  
            ++l_img_comp;  
            ++l_tile_comp;  
    }  

    return l_data_size;    <--- This function will return 0xF3B40.  

```
## }

To prove this vulnerability, I used the image as a following description.

```
`image->numcomps` is 0x10  
One of the `l_size_comp` is 0x4, the others is 0x10.  
`l_res->x1 - l_res->x0` is 0x1064  
`l_res->y1 - l_res->y0` is 0x1064  

Therefore, (0x4 \* 0x1064 \* 1064) + ((0x10 \* 0x1064 \* 0x1064) \* 0xF) = 0x1000F3B40 (Integer Overflow)  

```

As a result, the function `opj_tcd_get_decoded_tile_size` will return 0xF3B40.

## File libopenjpeg20/j2k.c, line 9562:

static OPJ\_BOOL opj\_j2k\_decode\_tiles ( opj\_j2k\_t \*p\_j2k,  

opj\_stream\_private\_t \*p\_stream,  

opj\_event\_mgr\_t \* p\_manager)  

{  

OPJ\_BOOL l\_go\_on = OPJ\_TRUE;  

OPJ\_UINT32 l\_current\_tile\_no;  

OPJ\_UINT32 l\_data\_size,l\_max\_data\_size;  

OPJ\_INT32 l\_tile\_x0,l\_tile\_y0,l\_tile\_x1,l\_tile\_y1;  

OPJ\_UINT32 l\_nb\_comps;  

OPJ\_BYTE \* l\_current\_data;  

OPJ\_UINT32 nr\_tiles = 0;

```
    l_current_data = (OPJ_BYTE\*)opj_malloc(1000);    <--- The size of `l_current_data` is 1000.  
    if (! l_current_data) {  
            opj_event_msg(p_manager, EVT_ERROR, "Not enough memory to decode tiles\n");  
            return OPJ_FALSE;  
    }  
    l_max_data_size = 1000;  

	for (;;) {  
            if (! opj_j2k_read_tile_header( p_j2k,  
                                    &l_current_tile_no,  
                                    &l_data_size,           <--- `l_data_size` will be 0xF3B40. (It is the return value of `opj_tcd_get_decoded_tile_size`)  
                                    &l_tile_x0, &l_tile_y0,  
                                    &l_tile_x1, &l_tile_y1,  
                                    &l_nb_comps,  
                                    &l_go_on,  
                                    p_stream,  
                                    p_manager)) {  
                    opj_free(l_current_data);  
                    return OPJ_FALSE;  
            }  

            if (! l_go_on) {  
                    break;  
            }  

            if (l_data_size > l_max_data_size) {  
                    OPJ_BYTE \*l_new_current_data = (OPJ_BYTE \*) opj_realloc(l_current_data, l_data_size);    <--- `opj_realloc` will reallocate memory with size 0xF3B40.  
                    if (! l_new_current_data) {  
                            opj_free(l_current_data);  
                            opj_event_msg(p_manager, EVT_ERROR, "Not enough memory to decode tile %d/%d\n", l_current_tile_no +1, p_j2k->m_cp.th \* p_j2k->m_cp.tw);  
                            return OPJ_FALSE;  
                    }  
                    l_current_data = l_new_current_data;  
                    l_max_data_size = l_data_size;  
            }  

```

---

## File libopenjpeg20/tcd.c, line 1352:

## OPJ\_BOOL opj\_tcd\_update\_tile\_data ( opj\_tcd\_t \*p\_tcd, OPJ\_BYTE \* p\_dest, OPJ\_UINT32 p\_dest\_length ) { ... 1372 for (i=0;i<p\_tcd->image->numcomps;++i) { ... 1388 switch (l\_size\_comp) 1389 { ... 1440 case 4: 1441 { 1442 OPJ\_INT32 \* l\_dest\_ptr = (OPJ\_INT32 \*) p\_dest; <--- The size of `p_dest` is still 0xF3B40. 1443 OPJ\_INT32 \* l\_src\_ptr = l\_tilec->data; 1444 1445 for (j=0;j<l\_height;++j) { <--- `l_height` is 0x1064. 1446 for (k=0;k<l\_width;++k) { <--- `l_width` is 0x1064. 1447 \*(l\_dest\_ptr++) = (\*(l\_src\_ptr++)); <--- out of bound write. 1448 } 1449 l\_src\_ptr += l\_stride; 1450 } 1451 1452 p\_dest = (OPJ\_BYTE\*) l\_dest\_ptr; 1453 } 1454 break; 1455 }

I can control the `l_tilec->data` using `J2K_MS_MCT` block.

**VERSION**  

Chrome Version: 51.0.2704.106 Stable / latest pdfium\_test  

Operating System: Windows 10 x64 / Ubuntu 16.04 x64

**REPRODUCTION CASE**  

Attached as poc.pdf

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Attached as pdfium\_ASAN\_trace.txt, chrome\_windbg\_trace.txt

(1f44.f7c): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

chrome\_child!opj\_tcd\_update\_tile\_data+0xca:  

00007fff`a9a46d56 8907 mov dword ptr [rdi],eax ds:00000215`b5c1e000=????????  

0:000> r  

rax=0000000000414141 rbx=00000215ca3dd318 rcx=00000215cbc69034  

rdx=0000000000000000 rsi=00000215c7afdf50 rdi=00000215b5c1e000  

rip=00007fffa9a46d56 rsp=0000001e5c71ac50 rbp=0000000000000000  

r8=0000000000001064 r9=0000000000000968 r10=0000000000001024  

r11=00000215ca3e8000 r12=0000000000000004 r13=0000000000000000  

r14=00000215b5b16010 r15=0000000000000000  

iopl=0 nv up ei pl nz na pe nc  

cs=0033 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010202  

chrome\_child!opj\_tcd\_update\_tile\_data+0xca:  

00007fff`a9a46d56 8907 mov dword ptr [rdi],eax ds:00000215`b5c1e000=????????  

0:000> u  

chrome\_child!opj\_tcd\_update\_tile\_data+0xca [c:\b\build\slave\win64\build\src\third\_party\pdfium\third\_party\libopenjpeg20\tcd.c @ 1440]:  

00007fff`a9a46d56 8907 mov dword ptr [rdi],eax 00007fff`a9a46d58 4903fc add rdi,r12  

00007fff`a9a46d5b 4983e901 sub r9,1 00007fff`a9a46d5f 75f0 jne chrome\_child!opj\_tcd\_update\_tile\_data+0xc5 (00007fff`a9a46d51) 00007fff`a9a46d61 4803ca add rcx,rdx  

00007fff`a9a46d64 4983ea01 sub r10,1 00007fff`a9a46d68 75df jne chrome\_child!opj\_tcd\_update\_tile\_data+0xbd (00007fff`a9a46d49) 00007fff`a9a46d6a e9e7000000 jmp chrome\_child!opj\_tcd\_update\_tile\_data+0x1ca (00007fff`a9a46e56) 0:000> dd rdi-32 00000215`b5c1dfce 41410041 41410041 41410041 41410041  

00000215`b5c1dfde 41410041 41410041 41410041 41410041 00000215`b5c1dfee 41410041 41410041 41410041 41410041  

00000215`b5c1dffe ???????? ???????? ???????? ???????? 00000215`b5c1e00e ???????? ???????? ???????? ????????  

00000215`b5c1e01e ???????? ???????? ???????? ???????? 00000215`b5c1e02e ???????? ???????? ???????? ????????  

00000215`b5c1e03e ???????? ???????? ???????? ????????

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 20.5 KB)
- [pdfium_asan_trace.txt](attachments/pdfium_asan_trace.txt) (text/plain, 9.0 KB)
- [chrome_windbg_trace.txt](attachments/chrome_windbg_trace.txt) (text/plain, 15.0 KB)
- [patch.txt](attachments/patch.txt) (text/plain, 2.4 KB)
- [poc2.pdf](attachments/poc2.pdf) (application/pdf, 28.1 KB)

## Timeline

### ke...@chromium.org (2016-07-20)

This is in pdfium, Tom is this something you can take a look at?

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### ts...@chromium.org (2016-07-21)

Passing the buck.

### [Deleted User] (2016-07-22)

* Fix Suggestion

### ke...@chromium.org (2016-07-22)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-07-22)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ke...@chromium.org (2016-07-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-07-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5675126008053760

### bu...@chromium.org (2016-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/80c4b164dcce4b2ea27e65788bc33443d9dbce32

commit 80c4b164dcce4b2ea27e65788bc33443d9dbce32
Author: ochang <ochang@chromium.org>
Date: Tue Jul 26 01:43:07 2016

Roll PDFium e283e47..d8cc503

https://pdfium.googlesource.com/pdfium.git/+log/e283e47..d8cc503

BUG=629919
TBR=thestig@chromium.org

Review-Url: https://codereview.chromium.org/2177383002
Cr-Commit-Position: refs/heads/master@{#407680}

[modify] https://crrev.com/80c4b164dcce4b2ea27e65788bc33443d9dbce32/DEPS


### [Deleted User] (2016-07-26)

ClusterFuzz does not work?

### [Deleted User] (2016-07-26)

Reducing the Run-time.

Please check new attached file.

Moreover, I can control these registers. (Tested on Win10 + 52.0.2743.82 Stable)

(22c8.2038): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome_child!opj_tcd_update_tile_data+0x72:
00007fff`a974f97e 448b4108        mov     r8d,dword ptr [rcx+8] ds:00414138`2d1df401=????????
0:000> r
rax=0000000000414104 rbx=0000018c963085f8 rcx=004141382d1df3f9   <-- `4141` is `J2K_MS_MCT` blocks.
rdx=000000000008281e rsi=0000018c92302860 rdi=0000018c963a6794
rip=00007fffa974f97e rsp=000000364892ac30 rbp=0000000000000001
 r8=0000000000000131  r9=00000000fffffffe r10=0000000000000000
r11=0000018c963286f0 r12=0000000000000004 r13=0000000000000000
r14=0000018c96307b80 r15=0000000000000000
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
chrome_child!opj_tcd_update_tile_data+0x72:
00007fff`a974f97e 448b4108        mov     r8d,dword ptr [rcx+8] ds:00414138`2d1df401=????????

### oc...@chromium.org (2016-07-27)

Thanks for the pocs and suggested patch. I've made small modifications and landed it so it should be fixed now.

### sh...@chromium.org (2016-07-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-30)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-07-30)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### go...@chromium.org (2016-08-01)

Before we approve merge to M53, Could you please confirm whether this change is baked/verified in Canary and safe to merge?


### go...@chromium.org (2016-08-02)

Approving merge to M53 branch 2785 based on chat with awhalley@. Please merge ASAP if possible before 5:00 PM PT today so we can take it for tomorrow's beta release. Thank you.

### go...@chromium.org (2016-08-02)

We're cutting M53 Beta RC today for release tomorrow. Please try to merge your change to M53 branch 2785 before 5:30 PM PT today so we can take it for this week beta. Thank you.

### bu...@chromium.org (2016-08-02)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/tools/buildspec/+/8b2094e9fb96be2e67bce39f13de425646e7d04d

commit 8b2094e9fb96be2e67bce39f13de425646e7d04d
Author: Oliver Chang <ochang@google.com>
Date: Tue Aug 02 22:43:59 2016


### oc...@chromium.org (2016-08-02)

Not sure why bugdroid didn't set the right labels. 

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-25)

Congratulations! The panel awarded $5,000 for this one.

### aw...@chromium.org (2016-08-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/629919?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084900)*
