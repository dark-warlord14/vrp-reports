# Heap-use-after-free in chromium_jpeg_read_scanlines

| Field | Value |
|-------|-------|
| **Issue ID** | [401846968](https://issues.chromium.org/issues/401846968) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | PDFium |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | at...@gmail.com |
| **Assignee** | fm...@chromium.org |
| **Created** | 2025-03-09 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5311346941820928

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7c0669357814
Crash State:
  chromium_jpeg_read_scanlines
  jpeg_common_read_scanlines
  fxcodec::JpegDecoder::GetNextLine
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1428594:1428603

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5311346941820928

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### ph...@chromium.org (2025-03-09)

Hi thestig@, could you help take a look at this critical security bugs, or find a right owner for it please?

### ch...@google.com (2025-03-10)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-03-10)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### th...@chromium.org (2025-03-10)

FWIW, in the blamelist, PDFium didn't change. Libjpeg-turbo did.

### ri...@google.com (2025-03-10)

Re-assigning to fmalita@, who authored the [CL](https://chromium-review.googlesource.com/c/chromium/deps/libjpeg_turbo/+/6264683/12/src/jdapistd.c#317) that might have caused this. Would you be able to help take a look?

### th...@chromium.org (2025-03-10)

The input from ClusterFuzz is just a PDF. I tried running pdfium\_fuzzer on it, but that didn't trigger issue. The issue may only repro when running a full browser with the PDF viewer.

### th...@chromium.org (2025-03-10)

Easier repro: `ASAN_OPTIONS=whatever_you_need out/asan/pdfium_test --use-renderer=agg clusterfuzz_input`

### th...@chromium.org (2025-03-10)

Can confirm the libjpeg-turbo 3.1.0 triggered this.

### ap...@google.com (2025-03-12)

Project: pdfium  

Branch: main  

Author: Florin Malita <[fmalita@chromium.org](mailto:fmalita@chromium.org)>  

Link:      <https://pdfium-review.googlesource.com/129450>

Propagate Rewind() errors in ScanlineDecoder::SkipToScanline()

---


Expand for full commit details
```
Propagate Rewind() errors in ScanlineDecoder::SkipToScanline() 
 
JpegDecoder::Rewind() can fail and destroy the jpeg context in the 
process. 
 
Rewind() failures should be propagated upstream, similar to 
ScanlineDecoder::GetScanline(), to avoid attempting to continue with 
an invalid context. 
 
Bug: 401846968 
Change-Id: I73e1d9ddc51745be0706fe74d93558f5683fbfa8 
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/129450 
Reviewed-by: Thomas Sepez <tsepez@google.com> 
Commit-Queue: Thomas Sepez <tsepez@google.com> 
Reviewed-by: Lei Zhang <thestig@chromium.org> 
Commit-Queue: Florin Malita <fmalita@chromium.org>

```

---

Files:

- M `core/fxcodec/scanlinedecoder.cpp`

---

Hash: 5a1649e98e7e39c11a2677172f350aa13018966d  

Date:  Wed Mar 12 11:29:08 2025


---

### 24...@project.gserviceaccount.com (2025-03-13)

ClusterFuzz testcase 5311346941820928 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1431820:1431832

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2025-03-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $9000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process + $2,000 fuzzer bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-21)

Congratulations attekett! Thank you for your past fuzzer contributions that resulted in this report!

### at...@gmail.com (2025-03-21)

Thanks.

### ch...@google.com (2025-04-02)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [136].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-04-02)

This fix landed on 136, no merge needed

### ch...@google.com (2025-06-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/401846968)*
