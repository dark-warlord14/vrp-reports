#  Security: libtiff CVE vulnerabilities in Chromium 106.0.5249.103

| Field | Value |
|-------|-------|
| **Issue ID** | [40062114](https://issues.chromium.org/issues/40062114) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2022-0891, CVE-2022-1354, CVE-2022-1355, CVE-2022-2867, CVE-2022-2868, CVE-2022-2869, CVE-2022-2953, CVE-2022-3570, CVE-2022-3597, CVE-2022-3598, CVE-2022-3599, CVE-2022-3626, CVE-2022-3627 |
| **Reporter** | sa...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2022-12-07 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

BDBA scan of Electron 21.1.1 - Chromium version 106.0.5249.103 gives various CVE's for libtiff

**VERSION**  

Chrome Version: Chromium 106.0.5249.103  

Operating System: windows/linux (issues found from BDBA scans)

**REPRODUCTION CASE**  

CVE's can be found on CVE website for libtiff. I have also posted the links below. Fix commits are listed in the CVE case.

CVE-2022-0891 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-0891>)  

CVE-2022-2868 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2868>)  

CVE-2022-2867 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2867>)  

CVE-2022-2869 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2869>)  

CVE-2022-1354 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-1354>)  

CVE-2022-1355 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-1355>)  

CVE-2022-3570 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3570>)  

CVE-2022-2953 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2953>)  

CVE-2022-3626 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3626>)  

CVE-2022-3599 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3599>)  

CVE-2022-3597 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3597>)  

CVE-2022-3627 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3627>)  

CVE-2022-3598 (<https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3598>)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

n/a

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: not needed, just pointing out existing CVEs for the libtiff library

## Timeline

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-07)

Thanks.

thestig@, in https://crbug.com/chromium/1396254 it looks like you cherry-picked the latest libtiff vulnerability fix.

It looks to me like all the above CVEs don't actually affect the main part of libtiff, but just all its subsidiary tools. Plus in https://crbug.com/chromium/1396254 you say that
> The code is behind chrome://flag entry which isn't on by default
Does that apply to all of libtiff?

Overall it looks like there are multiple reasons why there's probably not a real vulnerability here, but it'd be good to have your confirmation. And I suspect we'll keep getting similar bugs reported until or unless we formally upgrade to libtiff 4.4.0.

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2022-12-07)

I was a bit behind on https://crbug.com/chromium/1396254, and on upgrading libtiff to the latest version in general. However, I've been watching many of the other CVEs go by and https://crbug.com/chromium/1399080#c2 is indeed correct in that they affect the tools libtiff comes with, and not the core TIFF decoding library.

I'll go through this CVE list and explain where they stand.

### th...@chromium.org (2022-12-07)

CVE-2022-0891: Tool only
CVE-2022-2868: Tool only
CVE-2022-2867: Tool only
CVE-2022-2869: Tool only
CVE-2022-1354: Listed as tool only, but will cherry-pick https://gitlab.com/libtiff/libtiff/-/commit/87f580f39011109b3bb5f6eca13fac543a542798
CVE-2022-1355: Tool only
CVE-2022-3570: Tool only
CVE-2022-2953: Tool only
CVE-2022-3626: Tool only
CVE-2022-3599: Listed as tool only, but will cherry-pick https://gitlab.com/libtiff/libtiff/-/commit/e813112545942107551433d61afd16ac094ff246
CVE-2022-3597: Tool only
CVE-2022-3627: Tool only
CVE-2022-3598: Tool only

### th...@chromium.org (2022-12-07)

I'm also not sure if CVE-2022-1354 is applicable, because it involved OJPEG, and https://pdfium.googlesource.com/pdfium/+/cc380bd2fbd7583438ab81151cdbfbfa61682228 disabled OJPEG support in PDFium's copy of libtiff.

### gi...@appspot.gserviceaccount.com (2022-12-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/596d32946e0f58fae5dd938e601c88a84d24047c

commit 596d32946e0f58fae5dd938e601c88a84d24047c
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Dec 08 00:29:06 2022

Cherry-pick libtiff commit to fix OJPEG hack.

Apply [1], even though OJPEG support is disabled.

[1] https://gitlab.com/libtiff/libtiff/-/commit/87f580f39011109b3bb5f6eca13fac543a542798

Bug: chromium:1399080
Change-Id: Iced64900732de884647950203c0eed8bcb42a9e6
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/102210
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/596d32946e0f58fae5dd938e601c88a84d24047c/third_party/libtiff/0038-fix-ojpeg-hack.patch
[modify] https://pdfium.googlesource.com/pdfium/+/596d32946e0f58fae5dd938e601c88a84d24047c/third_party/libtiff/README.pdfium
[modify] https://pdfium.googlesource.com/pdfium/+/596d32946e0f58fae5dd938e601c88a84d24047c/third_party/libtiff/tif_dirread.c


### gi...@appspot.gserviceaccount.com (2022-12-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/56adfa042c8ffd5ceaf4f4b17f66bbcc4d5eba7e

commit 56adfa042c8ffd5ceaf4f4b17f66bbcc4d5eba7e
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Dec 08 00:31:22 2022

Cherry-pick libtiff commit to revise handling of TIFFTAG_INKNAMES.

Apply [1] and resolve all the merge conflicts.

[1] https://gitlab.com/libtiff/libtiff/-/commit/e813112545942107551433d61afd16ac094ff246

Bug: chromium:1399080
Change-Id: Id5f5c078016fb3a302de41aa431b10fdfd1d2b3d
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/102230
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/56adfa042c8ffd5ceaf4f4b17f66bbcc4d5eba7e/third_party/libtiff/tif_dir.c
[modify] https://pdfium.googlesource.com/pdfium/+/56adfa042c8ffd5ceaf4f4b17f66bbcc4d5eba7e/third_party/libtiff/tif_print.c
[modify] https://pdfium.googlesource.com/pdfium/+/56adfa042c8ffd5ceaf4f4b17f66bbcc4d5eba7e/third_party/libtiff/tif_dirwrite.c
[modify] https://pdfium.googlesource.com/pdfium/+/56adfa042c8ffd5ceaf4f4b17f66bbcc4d5eba7e/third_party/libtiff/tif_dirinfo.c
[modify] https://pdfium.googlesource.com/pdfium/+/56adfa042c8ffd5ceaf4f4b17f66bbcc4d5eba7e/third_party/libtiff/README.pdfium
[modify] https://pdfium.googlesource.com/pdfium/+/56adfa042c8ffd5ceaf4f4b17f66bbcc4d5eba7e/third_party/libtiff/tif_dir.h
[add] https://pdfium.googlesource.com/pdfium/+/56adfa042c8ffd5ceaf4f4b17f66bbcc4d5eba7e/third_party/libtiff/0039-handling-of-tifftag-inknames.patch


### ad...@google.com (2022-12-08)

Thanks! It sounds like the only one which might (_might_) affect Chromium is CVE-2022-3599, and that's an OOB read, so I'm labelling up this bug as medium severity. If we become sure that this does not affect Chromium, please reclassify this as type=Bug.

### [Deleted User] (2022-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-08)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-12-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/596e4283c1e421e1e9014102d681dae35c955a26

commit 596e4283c1e421e1e9014102d681dae35c955a26
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Dec 09 03:47:51 2022

Roll PDFium from 4e9c5b7500a7 to 9a02c9040e16 (5 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/4e9c5b7500a7..9a02c9040e16

2022-12-09 kmoon@chromium.org Avoid MSVC warning D9025 when pdf_use_cxx20=false
2022-12-08 kmoon@chromium.org Add test for masked image clipping issue
2022-12-08 thestig@chromium.org Undo check for invalid URIs in FPDFAction_GetURIPath().
2022-12-08 thestig@chromium.org Cherry-pick libtiff commit to revise handling of TIFFTAG_INKNAMES.
2022-12-08 thestig@chromium.org Cherry-pick libtiff commit to fix OJPEG hack.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1396248,chromium:1399080
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Ic81d9de06e3eed7265af5ba2855da2d5e4796029
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4091286
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1081305}

[modify] https://crrev.com/596e4283c1e421e1e9014102d681dae35c955a26/DEPS


### th...@chromium.org (2022-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-09)

Requesting merge to beta M109 because latest trunk commit (1081305) appears to be after beta branch point (1070088).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [109].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-10)

Requesting merge to beta M109 because latest trunk commit (1081305) appears to be after beta branch point (1070088).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [109].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-11)

Requesting merge to beta M109 because latest trunk commit (1081305) appears to be after beta branch point (1070088).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [109].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2022-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-12)

Requesting merge to beta M109 because latest trunk commit (1081305) appears to be after beta branch point (1070088).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [109].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-12)

There does not appear to be any compelling reason to not backmerge this so on the side of caution, let's go ahead and get this roll into M109.
thestig@ please merge to branch 5414 at your earliest convenience / before 3pm PST tomorrow (Tuesday) 13 December so this can also be included in next M109/beta on Wednesday -- thank you! 

### th...@chromium.org (2022-12-12)

OTOH, should this receive the same severity classification as https://crbug.com/chromium/1396254? See https://bugs.chromium.org/p/chromium/issues/detail?id=1396254#c16

### am...@chromium.org (2022-12-12)

ah, I missed the comment about this libtiff code being behind a flag not enabled by default in https://crbug.com/chromium/1396254. Thanks for calling that out. Should still stay a security bug but adjusting to SI-None and removing merge approval. 

### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-16)

Thank you for this report! The VRP Panel would like to extend a $500 award to thank you for reporting this to us. A member of our finance team will be in touch to arrange payment. Thank you again! 

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1399080?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-05-20)

hello -- the finance team did not receive a response when they reached out to process the VRP reward for this report. As such, this reward is considered abandoned. As is policy for abandoned VRP rewards, it will be doubled and donated to a charitable cause.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062114)*
