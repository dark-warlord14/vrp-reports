# Security: PDFium Out-of-Bounds Read in CPDF_DeviceCS::TranslateImageLine

| Field | Value |
|-------|-------|
| **Issue ID** | [40084088](https://issues.chromium.org/issues/40084088) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **CVE IDs** | CVE-2016-1686 |
| **Reporter** | st...@gmail.com |
| **Assignee** | oc...@chromium.org |
| **Created** | 2016-04-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached proof-of-concept file could crash the latest build of pdfium\_test.  

This is an Out-Of-Bounds Read issue.  

The exception information is presented as follows.

---

## Exception Information

(35a8.3bc8): Access violation - code c0000005 (!!! second chance !!!)  

eax=003cf532 ebx=003cf531 ecx=01248fc8 edx=014c8ff0 esi=00000000 edi=07e7bffe  

eip=0137f5bf esp=003cf4c4 ebp=003cf4e0 iopl=0 nv up ei pl zr na pe nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010246  

pdfium\_test!CPDF\_DeviceCS::TranslateImageLine+0x15f:  

0137f5bf 0fb64702 movzx eax,byte ptr [edi+2] ds:002b:07e7c000=??

---

## Stack Trace Information

pdfium\_test!CPDF\_DeviceCS::TranslateImageLine+0x15f [pdfium\core\fpdfapi\fpdf\_page\fpdf\_page\_colors.cpp @ 205]  

pdfium\_test!CPDF\_DIBSource::DownSampleScanline32Bit+0x2a1 [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 1428]  

pdfium\_test!CPDF\_DIBSource::DownSampleScanline+0x19a [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 1223]  

pdfium\_test!CFX\_ImageStretcher::ContinueQuickStretch+0xa8 [pdfium\core\fxge\dib\fx\_dib\_engine.cpp @ 909]  

pdfium\_test!CFX\_ImageRenderer::Continue+0x1c [pdfium\core\fxge\dib\fx\_dib\_main.cpp @ 1674]  

pdfium\_test!CFX\_AggDeviceDriver::ContinueDIBits+0x23 [pdfium\core\fxge\agg\fx\_agg\_driver.cpp @ 1789]  

pdfium\_test!CPDF\_ImageRenderer::Continue+0xf9 [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_image.cpp @ 857]  

pdfium\_test!CPDF\_RenderStatus::ContinueSingleObject+0xd3 [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 309]  

pdfium\_test!CPDF\_ProgressiveRenderer::Continue+0x2de [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 1103]  

pdfium\_test!FPDF\_RenderPage\_Retail+0x221 [pdfium\fpdfsdk\fpdfview.cpp @ 936]  

pdfium\_test!FPDF\_RenderPageBitmap+0x99 [pdfium\fpdfsdk\fpdfview.cpp @ 668]  

pdfium\_test!RenderPage+0x1b8 [pdfium\samples\pdfium\_test.cc @ 450]  

pdfium\_test!RenderPdf+0x2ef [pdfium\samples\pdfium\_test.cc @ 626]  

pdfium\_test!main+0x2e6 [pdfium\samples\pdfium\_test.cc @ 749]  

pdfium\_test!invoke\_main+0x1d [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 74]  

pdfium\_test!\_\_scrt\_common\_main\_seh+0xff [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 264]  

kernel32!BaseThreadInitThunk+0xe  

ntdll!\_\_RtlUserThreadStart+0x70  

ntdll!\_RtlUserThreadStart+0x1b

---

## Vulnerability Analysis

0:000> !heap -p -a edi  

address 07e7bffe found in  

\_DPH\_HEAP\_ROOT @ 1d1000  

in busy allocation ( DPH\_HEAP\_BLOCK: UserAddr UserSize - VirtAddr VirtSize)  

7e22bfc: 7e7b880 780 - 7e7b000 2000  

72c88e89 verifier!AVrfDebugPageHeapAllocate+0x00000229  

76f91d4e ntdll!RtlDebugAllocateHeap+0x00000030  

76f4b586 ntdll!RtlpAllocateHeap+0x000000c4  

76ef3541 ntdll!RtlAllocateHeap+0x0000023a  

0146f119 pdfium\_test!\_calloc\_base+0x00000047 [d:\th\minkernel\crts\ucrt\src\appcrt\heap\calloc\_base.cpp @ 33]  

013aa67a pdfium\_test!CCodec\_JpegDecoder::Create+0x0000011a [pdfium\core\fxcodec\codec\fx\_codec\_jpeg.cpp @ 435]  

013aa707 pdfium\_test!CCodec\_JpegModule::CreateDecoder+0x00000047 [pdfium\core\fxcodec\codec\fx\_codec\_jpeg.cpp @ 490]  

01391dba pdfium\_test!CPDF\_DIBSource::CreateDecoder+0x000001ba [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 587]  

0139427b pdfium\_test!CPDF\_DIBSource::StartLoadDIBSource+0x0000015b [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 312]  

0137c8d7 pdfium\_test!CPDF\_ImageCacheEntry::StartGetCachedBitmap+0x00000067 [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_cache.cpp @ 278]  

0137c9df pdfium\_test!CPDF\_PageRenderCache::StartGetCachedBitmap+0x000000cf [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_cache.cpp @ 125]  

01394084 pdfium\_test!CPDF\_ImageLoaderHandle::Start+0x00000044 [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 1504]  

0139402d pdfium\_test!CPDF\_ImageLoader::Start+0x0000005d [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 1565]  

01373400 pdfium\_test!CPDF\_ImageRenderer::StartLoadDIBSource+0x00000070 [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_image.cpp @ 343]  

01372e74 pdfium\_test!CPDF\_ImageRenderer::Start+0x00000074 [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_image.cpp @ 487]  

01354ef4 pdfium\_test!CPDF\_RenderStatus::ContinueSingleObject+0x000000b4 [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 330]  

01354d1e pdfium\_test!CPDF\_ProgressiveRenderer::Continue+0x000002de [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 1103]  

01329591 pdfium\_test!FPDF\_RenderPage\_Retail+0x00000221 [pdfium\fpdfsdk\fpdfview.cpp @ 936]  

01329e39 pdfium\_test!FPDF\_RenderPageBitmap+0x00000099 [pdfium\fpdfsdk\fpdfview.cpp @ 668]  

01323168 pdfium\_test!RenderPage+0x000001b8 [pdfium\samples\pdfium\_test.cc @ 450]  

0132355f pdfium\_test!RenderPdf+0x000002ef [pdfium\samples\pdfium\_test.cc @ 626]  

01328766 pdfium\_test!main+0x000002e6 [pdfium\samples\pdfium\_test.cc @ 749]  

01461ebd pdfium\_test!\_\_scrt\_common\_main\_seh+0x000000ff [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 264]  

7647338a kernel32!BaseThreadInitThunk+0x0000000e  

76ef9a02 ntdll!\_\_RtlUserThreadStart+0x00000070  

76ef99d5 ntdll!\_RtlUserThreadStart+0x0000001b

0:000> ?7e7b880 + 780  

Evaluate expression: 132628480 = 07e7c000

0:000> r  

eax=003cf532 ebx=003cf531 ecx=01248fc8 edx=014c8ff0 esi=00000000 edi=07e7bffe  

eip=0137f5bf esp=003cf4c4 ebp=003cf4e0 iopl=0 nv up ei pl zr na pe nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010246  

pdfium\_test!CPDF\_DeviceCS::TranslateImageLine+0x15f:  

0137f5bf 0fb64702 movzx eax,byte ptr [edi+2] ds:002b:07e7c000=??

Here 07e7c000 is greater than the upper bounds of the heap. It will cause a heap based out-of-bounds read issue.

---

## Credit

This vulnerability was discovered by Ke Liu of Tencent's Xuanwu LAB (<http://www.tencent.com/>).

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

PDFium Version: latest version built with Visual Studio 2015, both xfa and javascript were disabled.  

Operating System: [Windows 7 SP1]

**REPRODUCTION CASE**  

This issue was caused by the malformed JPEG image embedded in the PDF document.  

The malformed jpeg, the malformed pdf, and the normal jpeg were all attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

See at section VULNERABILITY DETAILS.

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### st...@gmail.com (2016-04-14)

------------------------
Additionally Analysis
------------------------
(28d8.2164): Access violation - code c0000005 (!!! second chance !!!)
eax=0027f48e ebx=0027f48d ecx=07558fc8 edx=014e8ff0 esi=00000000 edi=07f3cffe
eip=0139f5bf esp=0027f420 ebp=0027f43c iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
pdfium_test!CPDF_DeviceCS::TranslateImageLine+0x15f:
0139f5bf 0fb64702        movzx   eax,byte ptr [edi+2]     ds:002b:07f3d000=??

$$ local variables
0:000> dv
           this = 0x07558fc8
       pDestBuf = 0x0027f48c "!!&???"
        pSrcBuf = 0x07f3cffd "???"        <-------------------- ①
         pixels = 0n1
    image_width = 0n0
   image_height = 0n0
     bTransMask = 0n0
              k = <value unavailable>
              i = <value unavailable>
              
0:000> r edi
edi=07f3cffe                              <-------------------- ②

$$ we can conclude that pSrcBuf=edi-1 according to ① & ②.

0:000> u eip
pdfium_test!CPDF_DeviceCS::TranslateImageLine+0x15f [pdfium\core\fpdfapi\fpdf_page\fpdf_page_colors.cpp @ 205]:
0139f5bf 0fb64702        movzx   eax,byte ptr [edi+2]       ; pSrcBuf[3], oob access
0139f5c3 50              push    eax
0139f5c4 0fb64701        movzx   eax,byte ptr [edi+1]       ; pSrcBuf[2]
0139f5c8 50              push    eax
0139f5c9 0fb607          movzx   eax,byte ptr [edi]         ; pSrcBuf[1]
0139f5cc 50              push    eax
0139f5cd 0fb647ff        movzx   eax,byte ptr [edi-1]       ; pSrcBuf[0]
0139f5d1 50              push    eax

$$ we can see that only two bytes were available at the tail of the heap.
0:000> db edi
07f3cffe  ad a7 ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ..??????????????
07f3d00e  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
07f3d01e  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
07f3d02e  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
07f3d03e  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
07f3d04e  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
07f3d05e  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
07f3d06e  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????

------------------------
Source Code
------------------------
177  void CPDF_DeviceCS::TranslateImageLine(uint8_t* pDestBuf,
178                                         const uint8_t* pSrcBuf,
179                                         int pixels,
180                                         int image_width,
181                                         int image_height,
182                                         FX_BOOL bTransMask) const {
183    if (bTransMask && m_Family == PDFCS_DEVICECMYK) {
184      for (int i = 0; i < pixels; i++) {
185        int k = 255 - pSrcBuf[3];
186        pDestBuf[0] = ((255 - pSrcBuf[0]) * k) / 255;
187        pDestBuf[1] = ((255 - pSrcBuf[1]) * k) / 255;
188        pDestBuf[2] = ((255 - pSrcBuf[2]) * k) / 255;
189        pDestBuf += 3;
190        pSrcBuf += 4;
191      }
192      return;
193    }
194    if (m_Family == PDFCS_DEVICERGB) {
195      ReverseRGB(pDestBuf, pSrcBuf, pixels);
196    } else if (m_Family == PDFCS_DEVICEGRAY) {
197      for (int i = 0; i < pixels; i++) {
198        *pDestBuf++ = pSrcBuf[i];
199        *pDestBuf++ = pSrcBuf[i];
200        *pDestBuf++ = pSrcBuf[i];
201      }
202    } else {
203      for (int i = 0; i < pixels; i++) {
204        if (!m_dwStdConversion) {                                             // ------------------------------------
205          AdobeCMYK_to_sRGB1(pSrcBuf[0], pSrcBuf[1], pSrcBuf[2], pSrcBuf[3],  // Here pSrcBuf[3] caused an oob access
206                             pDestBuf[2], pDestBuf[1], pDestBuf[0]);          // ------------------------------------
207        } else {
208          uint8_t k = pSrcBuf[3];
209          pDestBuf[2] = 255 - std::min(255, pSrcBuf[0] + k);
210          pDestBuf[1] = 255 - std::min(255, pSrcBuf[1] + k);
211          pDestBuf[0] = 255 - std::min(255, pSrcBuf[2] + k);
212        }
213        pSrcBuf += 4;
214        pDestBuf += 3;
215      }
216    }

------------------------
Affected Version
------------------------
Latest version of pdfium is vulnerable (https://pdfium.googlesource.com/pdfium/+/bd9748d504555f100d34025d76a9e0119986bc3f).

### st...@gmail.com (2016-04-14)

------------------------
diff
------------------------
There are 4 bytes of difference. 

The first two bytes are located at sof0.
struct sof0 {
    marker      FF C0
    section     00 11
    precision   08
    Y_image     F9 10       // changed from [01 E0]
    X_image     02 80
    nr_comp     03
    comp[0]     01 11 00
    comp[1]     02 11 01
    comp[2]     03 11 01
}

The second two bytes are located at DHT.
struct DHT {
    marker      FF C4
    section     00 75  // changed from [00 74]
    
    huff_table[0]
        info    00
        length  01 01 01 01 01 01 01 00 00 00 00 00 00 00 00 00
        HTV     00 01 02 03 04 05 07
        
    huff_table[1]
        info    01
        length  [01] 01 01 01 01 01 00 00 00 00 00 00 00 00 00 00 // the first byte was extra inserted
        HTV     00 00 01 02 03 07
        
    ......
}
Here the structure of the DHT section was corrupted.


### ts...@chromium.org (2016-04-14)

@ochang, is this something we've seen before?  Thanks.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2016-04-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4963126709059584

### cl...@chromium.org (2016-04-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4963126709059584

Uploader: ochang@google.com
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x61c00000e800
Crash State:
  CPDF_DeviceCS::TranslateImageLine
  CPDF_DIBSource::DownSampleScanline32Bit
  CPDF_DIBSource::DownSampleScanline
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=289356:289512

Minimized Testcase (7.16 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94qS1ax0v2N44qRWnLdfMR7OiFlzNJo9HSjQLhQiPHT7t69Bm2FVOpVhPdYNwMc65bPqWUllvb4EdfJ6Q4hC_Uo2PCbcYZaZ92wSC0c6_RSicfzt49xyA3cMmEa3z2SX4YlhUvtSKw6q2xp3W7xgI5OEjA42Q

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### st...@gmail.com (2016-04-15)

Is it similar to this issue?
https://bugs.chromium.org/p/chromium/issues/detail?id=382820

### bu...@chromium.org (2016-04-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/7cf555202756c51ce2b5ae18efdeb6e1bb6a9e41

commit 7cf555202756c51ce2b5ae18efdeb6e1bb6a9e41
Author: ochang <ochang@chromium.org>
Date: Fri Apr 15 20:52:00 2016

Prevent a potential OOB read in TranslateImageLine.

Fixes a potential mismatch of |m_nComponents| between CPDF_DIBSource and
its CPDF_ColorSpace, from code attempting to recover from a failed decoder
initialisation in CPDF_DIBSource::CreateDecoder.

BUG=chromium:603518
R=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1892143003

[modify] https://crrev.com/7cf555202756c51ce2b5ae18efdeb6e1bb6a9e41/core/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp
[modify] https://crrev.com/7cf555202756c51ce2b5ae18efdeb6e1bb6a9e41/core/fpdfapi/fpdf_render/fpdf_render_loadimage_embeddertest.cpp
[add] https://crrev.com/7cf555202756c51ce2b5ae18efdeb6e1bb6a9e41/testing/resources/bug_603518.pdf


### bu...@chromium.org (2016-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/67b7f18b22c6f4476e97f4afae82a858b1ff97ca

commit 67b7f18b22c6f4476e97f4afae82a858b1ff97ca
Author: ochang <ochang@chromium.org>
Date: Fri Apr 15 23:12:40 2016

Roll PDFium 461129e..2ba3dc7

https://pdfium.googlesource.com/pdfium.git/+log/461129e..2ba3dc7

BUG=504658,603518

TEST=bots
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1893753002

Cr-Commit-Position: refs/heads/master@{#387739}

[modify] https://crrev.com/67b7f18b22c6f4476e97f4afae82a858b1ff97ca/DEPS


### oc...@chromium.org (2016-04-18)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-18)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### cl...@chromium.org (2016-04-18)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4963126709059584

Uploader: ochang@google.com
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x61c00000e800
Crash State:
  CPDF_DeviceCS::TranslateImageLine
  CPDF_DIBSource::DownSampleScanline32Bit
  CPDF_DIBSource::DownSampleScanline
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=289356:289512

Minimized Testcase (7.16 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94qS1ax0v2N44qRWnLdfMR7OiFlzNJo9HSjQLhQiPHT7t69Bm2FVOpVhPdYNwMc65bPqWUllvb4EdfJ6Q4hC_Uo2PCbcYZaZ92wSC0c6_RSicfzt49xyA3cMmEa3z2SX4YlhUvtSKw6q2xp3W7xgI5OEjA42Q

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### ss...@google.com (2016-04-18)

Merge approved for M51 (branch 2704)

### go...@chromium.org (2016-04-18)

Please merge your change to M51 branch 2704 ASAP (before 6:00 PM PST, today) so we can take it in for M51 last Dev release tomorrow.

### bu...@chromium.org (2016-04-18)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=86732

------------------------------------------------------------------
r86732 | ochang@google.com | 2016-04-18T19:53:43.499907Z

-----------------------------------------------------------------

### cl...@chromium.org (2016-04-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-19)

ClusterFuzz has detected this issue as fixed in range 387601:387928.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4963126709059584

Uploader: ochang@google.com
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x61c00000e800
Crash State:
  CPDF_DeviceCS::TranslateImageLine
  CPDF_DIBSource::DownSampleScanline32Bit
  CPDF_DIBSource::DownSampleScanline
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=289356:289512
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=387601:387928

Minimized Testcase (7.16 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94qS1ax0v2N44qRWnLdfMR7OiFlzNJo9HSjQLhQiPHT7t69Bm2FVOpVhPdYNwMc65bPqWUllvb4EdfJ6Q4hC_Uo2PCbcYZaZ92wSC0c6_RSicfzt49xyA3cMmEa3z2SX4YlhUvtSKw6q2xp3W7xgI5OEjA42Q

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ti...@google.com (2016-05-24)

Thanks for the great report! We'll consider this under our Chrome security reward program: https://www.google.com/about/appsecurity/chrome-rewards/ and update you with a decision soon.

### ti...@google.com (2016-05-25)

Our reward panel decided to award you $1,000 for this report. Congratulations!

We've credited you in our release notes as "Ke Liu of Tencent's Xuanwu LAB": https://googlechromereleases.blogspot.com/2016/05/stable-channel-update_25.html

Someone from our finance team will be in contact to collect details for payment within 7 days. If that doesn't happen, please either update this bug or contact me at timwillis@.

The CVE-ID for this issue is CVE-2016-1686. Usual boilerplate text below - let me know if you have any questions.

Thanks again for the report!


*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

### st...@gmail.com (2016-06-02)

Hi Timwillis, no one has contacted me so far.

### ti...@google.com (2016-06-02)

Thanks for letting me know - I'll chase today along with https://crbug.com/chromium/601362.

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/603518?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084088)*
