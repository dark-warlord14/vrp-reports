# Security: Cisco Talos Security Advisory for Google chrome product - TALOS-CAN-0174

| Field | Value |
|-------|-------|
| **Issue ID** | [40084343](https://issues.chromium.org/issues/40084343) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2016-1681 |
| **Reporter** | [Deleted User] |
| **Assignee** | oc...@chromium.org |
| **Created** | 2016-05-19 |
| **Bounty** | $3,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace, registers, exception record]**  

**Client ID (if relevant): [see link above]**

## Attachments

- [TALOS-CAN-0174 - Google Chrome PDFium jpeg2000 SIZ Code Execution Vulnerability.txt](attachments/TALOS-CAN-0174 - Google Chrome PDFium jpeg2000 SIZ Code Execution Vulnerability.txt) (text/plain, 18.2 KB)
- [TALOS-CAN-0174 - Google Chrome PDFium jpeg2000 SIZ Code Execution Vulnerability_POC.pdf](attachments/TALOS-CAN-0174 - Google Chrome PDFium jpeg2000 SIZ Code Execution Vulnerability_POC.pdf) (application/pdf, 1.2 KB)
- [Screen Shot 2016-05-19 at 14.22.41.png](attachments/Screen Shot 2016-05-19 at 14.22.41.png) (image/png, 425.2 KB)

## Timeline

### [Deleted User] (2016-05-19)

For further information about our disclosure process and PGP key for the vulnerability team, please see http://www.cisco.com/c/en/us/about/security-center/vendor-vulnerability-policy.html



### [Deleted User] (2016-05-19)

Please cc vulndev@cisco.com on all correspondence

### lg...@chromium.org (2016-05-19)

Text from the txt file (with stack traces snipped):

Cisco Talos Vulnerability Report
TALOS-CAN-0174
CVE-YYYY-NNNN

Google Chrome PDFium jpeg2000 SIZ Code Execution Vulnerability 


###  Summary

An exploitable  heap buffer overflow vulnerability exists in the Pdfium PDF reader included in the Google Chrome web browser. A specially crafted PDF document with embedded jpeg2000 image can cause a heap buffer overflow potentially resulting in an arbitrary code execution. An attacker can serve the malicious PDF file on a website and wait for a victim to visit to trigger this vulnerability. 


###  Tested Versions

Google Chrome 50.0.2661.94 
Pdfium Git 2016-05-08


###  Product URLs

[https://www.google.com/chrome/browser/desktop/](https://www.google.com/chrome/browser/desktop/)


###  CVSSv3 Score

6.3 - CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:L


###  Details

A heap buffer overflow vulnerability is present in the jpeg2000 image parser library as used by the Chrome's PDF renderer, PDFium. The vulnerability is located in the underlying jpeg2000 parsing library, openjpeg, but is made exploitable in case of Chrome due to special build process. 

Namely, an existing assert call in the openjpeg library usually prevents the heap overflow from being reached, but in the release versions of Chrome the assertations are omited. The source of the vulnerability is located in the following code in function `opj_j2k_read_siz` in `j2k.c` file:

    ```
    for     (i = 0; i < l_nb_tiles; ++i) {
            l_current_tile_param->tccps = (opj_tccp_t*) opj_calloc(l_image->numcomps, sizeof(opj_tccp_t));
            if (l_current_tile_param->tccps == 00) {
                    opj_event_msg(p_manager, EVT_ERROR, "Not enough memory to take in charge SIZ marker\n");
                    return OPJ_FALSE;
            }

            ++l_current_tile_param;
    }
    ```

If in the above call to `opj_calloc`, which is a `calloc` wrapper, `numcomps` value happens to be zero, `calloc` will return a unique pointer which can be later passed to `free` (this is implementation dependent, but is so on modern Linux OSes). The unique pointer returned by `calloc` will usually be a small allocation (0x20 bytes in case of x64 code). This can lead to a heap buffer overflow later in the code when this buffer is being used. The overflow happens inside  `opj_j2k_read_SQcd_SQcc` function where previously allocated buffer is being dereferenced.  The first out of bounds memory write happens in the following code:

    ```
    l_tccp->qntsty = l_tmp & 0x1f;
    l_tccp->numgbits = l_tmp >> 5;
    ```

In the above code, `l_tccp` pointer will be pointing to the previously erroneously allocated area. The same structure is dereferenced during further out of bounds writes in the following code. 

First requirement for this overflow to happen, number of components to be 0, is actually checked against in an assert at the beginning of the function:  

    ```
    assert(p_comp_no <  p_j2k->m_private_image->numcomps);
    ```

If the required condition for the erroneous allocation is satisfied, the above assert would fail which indeed does happen in the default build of openjpeg library. But, since the release builds of Chrome and PDFium omit these asserts the point of buffer overflow can be reached. The attached jpeg2000 testcase (embedded inside a PDF) has it's SIZ marker truncated (SIZ marker begins with 0xFF51). Number of components specified in the SIZ marker is 0 and isn't followed by individual component information. This short circuits the code that is parsing the file in  `opj_j2k_read_siz` and leads to the required erroneous call to `calloc`. The only difference between a valid jpeg2000 file and the one that triggers this vulnerability is the fact that SIZ marker specifies 0 components. 


###  Crash Information 


For debugging purposes, both a standard and ASAN build of latest PDFium code were tested, resulting in following crashes.

Regular build crashes due to heap corruption. A heap buffer overflow has resulted in adjacent heap chunk metadata overwrite:

    ```
    [snip]
    ```

PDFium build with address sanitizer :

    ```

    [snip]
    ```

Debugging output of Chromium nightly build revision 392151 (latest at the time of writting):

    ```
    [snip]
    ```

Latest Chrome release crashes upon opening the attached PDF file in a similar manner. 


### Credit 

Discovered by Aleksandar Nikolic of Cisco Talos.
http://talosintel.com/vulnerability-reports/


### Timeline


YYYY-MM-DD - Vendor Disclosure
YYYY-MM-DD - Public Release


### lg...@chromium.org (2016-05-19)

I can reproduce this on 50.0.2661.102 m, but not on OSX.

Tom, could you triage?

### lg...@chromium.org (2016-05-19)

Adding labels.

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2016-05-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2016-05-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4883255072915456

### cl...@chromium.org (2016-05-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4883255072915456

Uploader: ochang@google.com
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x609000007854
Crash State:
  opj_read_bytes_LE
  opj_j2k_read_SPCod_SPCoc
  opj_j2k_read_cod
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=316264:316370

Minimized Testcase (1.22 Kb): https://cluster-fuzz.appspot.com/download/AMIfv972N_wu0T42irtG_KaHEZ3sxY8Dt8c9MyJl6AaovJvjPIkSs-jp06D4dnNHLM9WRdflZltm_SZbzAo3aYgS0iXFfpnIfWgQqnQAgdMRw9tbQuIT-FumtjhtMKK-CO9zxWTrSGAyfxap712SbxshO--JFeOswg

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### bu...@chromium.org (2016-05-20)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/3cbb6fbcc7077d94161ec95b7bc1421671317c65

commit 3cbb6fbcc7077d94161ec95b7bc1421671317c65
Author: ochang <ochang@chromium.org>
Date: Fri May 20 16:54:24 2016

openjpeg: Prevent a buffer overflow in opj_j2k_read_SPCod_SPCoc.

BUG=chromium:613160

Review-Url: https://codereview.chromium.org/2001663002

[add] https://crrev.com/3cbb6fbcc7077d94161ec95b7bc1421671317c65/third_party/libopenjpeg20/0015-read_SPCod_SPCoc_overflow.patch
[modify] https://crrev.com/3cbb6fbcc7077d94161ec95b7bc1421671317c65/third_party/libopenjpeg20/README.pdfium
[modify] https://crrev.com/3cbb6fbcc7077d94161ec95b7bc1421671317c65/third_party/libopenjpeg20/j2k.c


### [Deleted User] (2016-05-20)

Please advise any updates regarding timeline or tentative release schedule

### oc...@chromium.org (2016-05-20)

This hasn't rolled into chromium yet, but once it does, it will be merged into M51 for the upcoming stable release.

### bu...@chromium.org (2016-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3a89e0aab29cebcfe1f559387215c4b10be86b76

commit 3a89e0aab29cebcfe1f559387215c4b10be86b76
Author: ochang <ochang@chromium.org>
Date: Fri May 20 18:11:07 2016

Roll PDFium 8b45eb1..3cbb6fb

https://pdfium.googlesource.com/pdfium.git/+log/8b45eb1..3cbb6fb

BUG=613160
TBR=thestig@chromium.org

Review-Url: https://codereview.chromium.org/1999153002
Cr-Commit-Position: refs/heads/master@{#395117}

[modify] https://crrev.com/3a89e0aab29cebcfe1f559387215c4b10be86b76/DEPS


### oc...@chromium.org (2016-05-20)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-20)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### go...@chromium.org (2016-05-20)

Before we approve merge to M51, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

+ timwillis@ to get his opinion as this is a security merge

### oc...@chromium.org (2016-05-20)

This hasn't had time to bake, but it's a very safe merge (2 line change to fix an obvious mistake).

### go...@chromium.org (2016-05-20)

Thank you ochang@.

+sshruthi, as this is a DEPS change. Could you PTAL and approve if you think it is ok?

### ss...@google.com (2016-05-20)

Sounds alright. However, since we are not cutting the candidate today, let's not skip bake time this close to stable. Please merge in only after verifying on tonight's canary.

Merge approved for M51 (branch 2704)

### sh...@chromium.org (2016-05-21)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-05-23)

Please merge to M51 branch 2704 ASAP once it is verified/baked in canary. Thank you.

### [Deleted User] (2016-05-23)

Please advise CVE ID# if available

### ti...@google.com (2016-05-23)

#22: CVE-IDs are assigned are assigned just before public release. We'll update this bug with a CVE-ID before the first public mention of this issue is made.

### bu...@chromium.org (2016-05-23)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=88155

------------------------------------------------------------------
r88155 | ochang@google.com | 2016-05-23T18:05:09.241158Z

-----------------------------------------------------------------

### [Deleted User] (2016-05-24)

To verify and synchronize our internal signature and advisory release schedules, you are aiming to ship this in M51 on May 31st, correct? 


### ti...@google.com (2016-05-24)

#25: M51 will ship to ~5% of users starting tomorrow (pending a successful build process on this end), which is when the release notes will also be published on https://googlechromereleases.blogspot.com.

At that time, we will make a reference to this issue by the issue number (613160), provide a CVE and a title for the issue. Take a look at the link above to get an understanding of what our releases look like. 

Note that access to this bug and the details will be kept restricted at least until the fix has reached most of our users. That is usually one week after our scheduled release date - so we won't be making any significant details public until on/around June 6. 

Please let me know if you have additional questions.

### ss...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-25)

Our reward panel decided to award you $3,000 for this report. Congratulations!

Someone from our finance team will be in contact to collect payment details in the next week. Full details are on our Chrome Reward page at https://www.google.com/about/appsecurity/chrome-rewards/

Please also note that details of this bug won't become public until June. The reward is conditional on keeping the details of this bug confidential until 8 June 2016 to give our users two weeks to update. 

If you would like the restrictions removed from this bug after 8 June (two weeks from today), please let me know and we can make all details public at that time. If not, all fixed bugs are opened to the public 14 weeks after they are fixed (around 24 August for this issue).

The CVE-ID for this issue is CVE-2016-1681.

If you have any questions, please let me know. This bug will be referenced in our release notes [https://googlechromereleases.blogspot.com/] today as:

CVE-2016-1681: Heap overflow in PDFium. Credit to Aleksandar Nikolic of Cisco Talos.

If you have any questions, please let me know.

### ti...@google.com (2016-05-25)

Actually - I have a question on your disclosure policy referenced at #1.

"Fifteen days after the vulnerability report is delivered to the vendor, the report will also be supplied to the Carnegie Mellon Computer Emergency Response Team (CERT)."

Is this in the case of no response from the vendor or in all cases?

### ti...@google.com (2016-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2016-05-26)

 Aleksandar Nikolich email: anikolich@sourcefire.com is the discoverer of this vulnerability from our team. I've added him to the thread so he can provide contact information adequate for bounty payment. 


### [Deleted User] (2016-05-26)

In response to https://crbug.com/chromium/613160#c29 - You will provide your own CVE in coordination with CERT since you are listed as a participating CVE numbering authority and have also been responsive since initial contact.

### [Deleted User] (2016-05-26)

Can we coordinate/set release for (not before) June 8th?

### ti...@google.com (2016-05-26)

#33: We won't release any more details until auto-derestrict in late August. If you want us to open up access to this bug on or after June 8, ping this bug and we'll make access public.

For the purposes of your tracking:

2016-05-19: Bug reported
2016-05-19: Bug acknowledged
2016-05-20: Bug fixed, with fix publicly available in chromium
2016-05-25: Bug fix shipped in Chrome Stable 51.0.2704.63
2016-06-08: Talos releases details (and so can we on request)

I'll use the address in #31 for payment. Thanks.


### ti...@google.com (2016-05-26)

@ochang - this looks as though it missed M52. Can you please take care of the merge?

### ti...@google.com (2016-05-26)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### go...@chromium.org (2016-05-27)

Approving  merge to M52 branch 2743 based on chat with timiwllis@ - Approval is needed as it missed dev. Should be straightforward-just needs a deps roll.

### bu...@chromium.org (2016-05-27)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=88314

------------------------------------------------------------------
r88314 | ochang@google.com | 2016-05-27T16:45:47.598736Z

-----------------------------------------------------------------

### [Deleted User] (2016-06-08)

Confirming release 12 noon PST via Talos

### ti...@google.com (2016-06-08)

Thanks - feel free to update with a link to the site. Let me know if you want to make this issue publicly accessible, otherwise it will automatically happen in late August.

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### [Deleted User] (2016-06-08)

http://www.talosintel.com/reports/TALOS-2016-0174/

### ti...@google.com (2016-06-08)

Making public based on details in http://www.talosintel.com/reports/TALOS-2016-0174/.

@regiwils - can you please update the disclosure timeline at the bottom of the page to match #33? I note that you've provided this details for other disclosures (one e.g.: http://www.talosintel.com/reports/TALOS-2016-0164/). 

### aw...@chromium.org (2016-06-08)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-10)

FYI external write-up: http://blog.talosintel.com/2016/06/pdfium.html

### cl...@chromium.org (2016-07-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4883255072915456

Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x609000007854
Crash State:
  opj_read_bytes_LE
  opj_j2k_read_SPCod_SPCoc
  opj_j2k_read_cod
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=316264:316370

Minimized Testcase (1.22 Kb): https://cluster-fuzz.appspot.com/download/AMIfv978W2CLqLIXA8VteZlxl_4-4CF_Wwqcz5Was1sbzVTjOcWMnNA0NAjCBJboy9Hwbymmr7HsTMQPt6RDuHQc9C0GxX4V60tvHvVK7z6z3aSUCDAlO_wJDxbISVwsmG2KA0PIFmNldJ_MICwp8qOg9EiH6gp7Pw?testcase_id=4883255072915456

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-07-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4883255072915456

Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x609000007854
Crash State:
  opj_read_bytes_LE
  opj_j2k_read_SPCod_SPCoc
  opj_j2k_read_cod
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=316264:316370

Minimized Testcase (1.22 Kb): https://cluster-fuzz.appspot.com/download/AMIfv978W2CLqLIXA8VteZlxl_4-4CF_Wwqcz5Was1sbzVTjOcWMnNA0NAjCBJboy9Hwbymmr7HsTMQPt6RDuHQc9C0GxX4V60tvHvVK7z6z3aSUCDAlO_wJDxbISVwsmG2KA0PIFmNldJ_MICwp8qOg9EiH6gp7Pw?testcase_id=4883255072915456

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-07-28)

ClusterFuzz has detected this issue as fixed in range 395074:395128.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4883255072915456

Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x609000007854
Crash State:
  opj_read_bytes_LE
  opj_j2k_read_SPCod_SPCoc
  opj_j2k_read_cod
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=316264:316370
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=395074:395128

Minimized Testcase (1.22 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96aNGI9Jz4INbMd-M2gacXy0NVJ7CXcsp_9YmaOZYrAtvVkurAXAUckFbp2MRY29ioYl89MPxsVVuwFGb8Jfij3Yz9fHE-vKDbDeslONdlj68QH4zIaMgIYdUJhLL1G-TwgvUXPofaupN9VXl71xyYmzRcvbw?testcase_id=4883255072915456

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

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

This issue was migrated from crbug.com/chromium/613160?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084343)*
