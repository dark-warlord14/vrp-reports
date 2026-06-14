# Security: Openjpeg security fix may be missing

| Field | Value |
|-------|-------|
| **Issue ID** | [40054821](https://issues.chromium.org/issues/40054821) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2020-27844 |
| **Reporter** | s....@salesforce.com |
| **Assignee** | dh...@chromium.org |
| **Created** | 2021-02-12 |
| **Bounty** | $500.00 |

## Description

From an e-mail to security@chromium.org:

===

I am reaching out to request information regarding a CVE related to openjpeg (<CVE-2020-27844>).

For CVE-2020-27844:
I do see a fix was made in https://github.com/uclouvain/openjpeg/issues/1299 made it into the 2.4.0 release of openjpeg, but that doesn't look to be taken as an upgrade in Chromium. Is there a timeline for when Chromium will be upgrading to opnejpeg 2.4.0.

===

We do seem to include libopenjpeg within Pdfium, so sending to thestig@. (cc jorgelo@ as this seems to be in ChromeOS too)

thestig@, please also add a CPEPrefix per
https://chromium.googlesource.com/chromium/src.git/+/master/docs/adding_to_third_party.md

which would seem to be cpe:/a:uclouvain:openjpeg:2.3 at the moment, but presumably you're about to change that to 2.4. This will enable us automatically to spot such issues in the future.

## Timeline

### rs...@chromium.org (2021-02-12)

Pdfium appears to use version 2.3.1, and looking at the fix, the change was to opj_j2k_write_sod (https://source.chromium.org/chromium/chromium/src/+/master:third_party/pdfium/third_party/libopenjpeg20/j2k.c;l=4616;drc=c7f07638b82ddb17aaee73c55b5af55e725355d8). The copy of that function used by Pdfium does not appear to have the vulnerable code, though it’s hard to tell if l_remaining_data is still vulnerable to any type of overflow.

### [Deleted User] (2021-02-12)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-02-12)

Yeah I've also now had a look.

It looks to me like maybe we've missed two evolutions of a fix here:
1) addition of an assert
2) later, replacement of the assert with the runtime check.

but I haven't dug deeper. If it were me, though, I'd be setting severity high based on this paranoia :) Then again it wouldn't surprise me if we don't actually use the _encoding_ side of openjpeg at all in pdfium, so this might be Security_Impact-None.

At the very least we should add a CPEPrefix to the README.pdfium so I wouldn't want to see this bug closed entirely.

tsepez@, thestig@ is OOO until March 8th - do you have context here?

### ts...@chromium.org (2021-02-12)

Bouncing over to print team.

### [Deleted User] (2021-02-12)

[Empty comment from Monorail migration]

### dh...@chromium.org (2021-02-12)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-02-12)

dhoss@ would you be kind enough to cc me on https://bugs.chromium.org/p/pdfium/issues/detail?id=1634?

### dh...@chromium.org (2021-02-12)

Done :) 

### ad...@chromium.org (2021-02-12)

Thanks. We'll keep this open as a tracking bug, so we can properly mark it as fixed in the Chromium release notes, as we've had a couple of external enquiries about it. If you happen to mention this bug number in the CL which fixes pdfium:1634, that would make everything happen automagically, but otherwise hopefully we'll manually spot it and mark this as fixed at the same time.

dhoss@: do you believe that these vulnerabilities _do_ affect Chromium? i.e. we do go through the affected code paths? If so we definitely want to get the fixes landed in the next few of days so we can get them into M89 initial release.

### ad...@chromium.org (2021-02-12)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-02-12)

[Empty comment from Monorail migration]

### dh...@chromium.org (2021-02-12)

Re https://crbug.com/chromium/1177875#c9: I have no experience with now PDFium uses OpenJPEG, but I've pushed off this update long enough - so I'll try to get the update done ASAP.

> Then again it wouldn't surprise me if we don't actually use the _encoding_ side of openjpeg at all in pdfium

While I believe the encoding side does get used in PDFium...

> do you believe that these vulnerabilities _do_ affect Chromium?

...I can't think of anywhere that code path would be entered by Chromium.

### [Deleted User] (2021-02-14)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dh...@chromium.org (2021-02-17)

Update: I landed 2.4.0 in PDFium. I also added a CPEPrefix for the future.

The list of other known security issues with 2.3.1 are:
https://github.com/uclouvain/openjpeg/issues/1293
https://github.com/uclouvain/openjpeg/issues/1294
https://github.com/uclouvain/openjpeg/issues/1297

Again, I'm not completely sure, but I think they all enter codepaths pertaining to encoding which I don't believe get entered by Chromium. Do we still want to merge the change?

### ad...@chromium.org (2021-02-17)

Thanks!

> I'm not completely sure, but I think they all enter codepaths pertaining to encoding which I don't believe get entered by Chromium

In that case I'll keep this as a security bug out of an abundance of caution, but ramp it down to medium severity.

Then - please mark this as Fixed, and in a couple of days sheriffbot will initiate merge procedures (to M89 but not M88). That sounds about right.

### ad...@chromium.org (2021-02-17)

[Empty comment from Monorail migration]

### dh...@chromium.org (2021-02-19)

Stable cut for M89 is on Tuesday (Feb 23) -- The CL we'd want to merge is crrev.com/854990.

### [Deleted User] (2021-02-19)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dh...@chromium.org (2021-02-19)

1) Yes
2) crrev.com/854990
3) Landed on ToT
4) No
5) This is a security change
6) No
7) N/A

### [Deleted User] (2021-02-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-20)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-02-21)

Approving merge to M89 - branch 4389.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-22)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d

commit 157601b9b923c7f8a32ffb770e1c97a89337b31d
Author: Daniel Hosseinian <dhoss@chromium.org>
Date: Mon Feb 22 19:30:49 2021

M89: Upgrade OpenJPEG to 2.4.0

Upgrade OpenJPEG by copying the files from 2.4.0 and then applying
patches. Patch files that are no longer relevant are deleted.

Some parts of patch 3 are no longer applicable.

The bug from patch 36 was fixed by upstream commit
024b8407392cb0b82b04b58ed256094ed5799e04.

Add a new patch 39 to remove the unused opj_mqc_renorme() function.

Fixed: pdfium:1634
Change-Id: Iaf5e208ea1f32a84aedb09744e0df084621f73dd
Bug: pdfium:1634, chromium:1177875
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/78050
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Daniel Hosseinian <dhoss@chromium.org>
(cherry picked from commit a81ff7286463b41d1055353a1e5ed6a2501a8b63)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/78170
Auto-Submit: Daniel Hosseinian <dhoss@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/mct.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0006-tcd_init_tile.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0022-jp2_apply_pclr_overflow.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0005-jp2_apply_pclr.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/pi.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/mct.c
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/openjpeg.c
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/mqc.c
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/pi.c
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/jp2.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0014-opj_jp2_read_ihdr_leak.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/mqc.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/jp2.c
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0023-opj_j2k_read_mct_records.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/openjpeg.h
[add] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0039-opj_mqc_renorme.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0012-mct_sse.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0003-dwt-decode.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0015-read_SPCod_SPCoc_overflow.patch
[delete] https://pdfium.googlesource.com/pdfium/+/d3664703dfa9dc530246de50a16b8e8523b676d6/third_party/libopenjpeg20/0038-opj_j2k_validate_param.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/j2k.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/opj_config.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0009-opj_pi_next.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/tcd.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/mqc_inl.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/j2k.c
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/tcd.c
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0035-opj_image_data_free.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/t2.c
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/t1.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0025-opj_j2k_add_mct_null_data.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/t2.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0026-use_opj_uint_ceildiv.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/t1.c
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/dwt.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/opj_common.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0019-tcd_init_tile.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/README.pdfium
[delete] https://pdfium.googlesource.com/pdfium/+/d3664703dfa9dc530246de50a16b8e8523b676d6/third_party/libopenjpeg20/0036-opj_j2k_update_image_dimensions.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/opj_codec.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/opj_intmath.h
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/dwt.c
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/opj_config_private.h
[delete] https://pdfium.googlesource.com/pdfium/+/d3664703dfa9dc530246de50a16b8e8523b676d6/third_party/libopenjpeg20/0037-tcd_init_tile.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0011-j2k_update_image_data.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0007-jp2_read_cmap.patch
[modify] https://pdfium.googlesource.com/pdfium/+/157601b9b923c7f8a32ffb770e1c97a89337b31d/third_party/libopenjpeg20/0016-read_SQcd_SQcc_overflow.patch


### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### gi...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### dh...@chromium.org (2021-03-03)

May I ask the reason for why we're merging to M86, but not M87 or M88?

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-03-03)

There's a ChromeOS LTS branch for enterprises. They support M86 for six months.

### am...@google.com (2021-03-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-11)

[Comment Deleted]

### am...@google.com (2021-03-11)

Hi, Sean@Tableau. Our VRP Panel would like to extend a thank you reward of $500 to you for being kind enough to reach out and report this issue in one of our third party dependencies. A member of our finance team will be in touch soon to arrange payment. Thanks again for reporting this to us!

### am...@google.com (2021-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-04-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-28)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd

commit a9aff888733a52abd08f0b842c1bf540d829f9dd
Author: Daniel Hosseinian <dhoss@chromium.org>
Date: Wed Apr 28 16:54:16 2021

M86: Upgrade OpenJPEG to 2.4.0

Upgrade OpenJPEG by copying the files from 2.4.0 and then applying
patches. Patch files that are no longer relevant are deleted.

Some parts of patch 3 are no longer applicable.

The bug from patch 36 was fixed by upstream commit
024b8407392cb0b82b04b58ed256094ed5799e04.

Add a new patch 39 to remove the unused opj_mqc_renorme() function.

Fixed: pdfium:1634
Fixed: chromium:1177875
Change-Id: Iaf5e208ea1f32a84aedb09744e0df084621f73dd
Bug: pdfium:1634
Bug: chromium:1177875
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/78050
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Daniel Hosseinian <dhoss@chromium.org>
(cherry picked from commit a81ff7286463b41d1055353a1e5ed6a2501a8b63)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/78290
Reviewed-by: Daniel Hosseinian <dhoss@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0003-dwt-decode.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0005-jp2_apply_pclr.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0006-tcd_init_tile.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0007-jp2_read_cmap.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0009-opj_pi_next.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0011-j2k_update_image_data.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0012-mct_sse.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0014-opj_jp2_read_ihdr_leak.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0015-read_SPCod_SPCoc_overflow.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0016-read_SQcd_SQcc_overflow.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0019-tcd_init_tile.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0022-jp2_apply_pclr_overflow.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0023-opj_j2k_read_mct_records.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0025-opj_j2k_add_mct_null_data.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0026-use_opj_uint_ceildiv.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0035-opj_image_data_free.patch
[delete] https://pdfium.googlesource.com/pdfium/+/6c9c6d2b55be956c59d5bfccd0fc8eb6c16f4624/third_party/libopenjpeg20/0036-opj_j2k_update_image_dimensions.patch
[delete] https://pdfium.googlesource.com/pdfium/+/6c9c6d2b55be956c59d5bfccd0fc8eb6c16f4624/third_party/libopenjpeg20/0037-tcd_init_tile.patch
[delete] https://pdfium.googlesource.com/pdfium/+/6c9c6d2b55be956c59d5bfccd0fc8eb6c16f4624/third_party/libopenjpeg20/0038-opj_j2k_validate_param.patch
[add] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/0039-opj_mqc_renorme.patch
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/README.pdfium
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/dwt.c
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/dwt.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/j2k.c
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/j2k.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/jp2.c
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/jp2.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/mct.c
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/mct.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/mqc.c
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/mqc.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/mqc_inl.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/openjpeg.c
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/openjpeg.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/opj_codec.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/opj_common.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/opj_config.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/opj_config_private.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/opj_intmath.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/pi.c
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/pi.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/t1.c
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/t1.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/t2.c
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/t2.h
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/tcd.c
[modify] https://pdfium.googlesource.com/pdfium/+/a9aff888733a52abd08f0b842c1bf540d829f9dd/third_party/libopenjpeg20/tcd.h


### [Deleted User] (2021-08-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-09-17)

reward processed for donation at the request of reporter! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1177875?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/pdfium/1634]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054821)*
