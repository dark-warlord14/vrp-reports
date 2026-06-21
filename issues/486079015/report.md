# .lnk File Download Bypass Using "Save As" Link (Bypass of #444803530)

| Field | Value |
|-------|-------|
| **Issue ID** | [486079015](https://issues.chromium.org/issues/486079015) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Chrome Version** | 145.0.7632.110 |
| **Reporter** | mu...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2026-02-20 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Run poc.py, and then open <http://127.0.0.1:8000/>
2. Right click `download me` hyperlink and then choose `Save File As`
3. Choose `Save` button and .lnk file will be downloaded

# Problem Description

This is a bypass of <https://issues.chromium.org/issues/444803530>, where an attacker uses a double percent sign (%%) to bypass Chrome’s dangerous file protection. Although it has already been fixed, it can still be bypassed by using a double “double percent sign,” such as: `file.lnk .%% .%%`

# Summary

.lnk File Download Bypass Using "Save As" Link (Bypass of #444803530)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [2026-02-20 22-02-04.mp4](attachments/2026-02-20 22-02-04.mp4) (video/mp4, 1.1 MB)
- [poc.py](attachments/poc.py) (text/x-python, 1003 B)

## Timeline

### an...@chromium.org (2026-02-23)

@li...@google.com can you PTAL?

### ch...@google.com (2026-02-24)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-24)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2026-03-04)

Project: chromium/src  

Branch:  main  

Author:  Andrew Liu [liu@chromium.org](mailto:liu@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7629495>

Filter out multiple "double percent signs" when normalizing download files

---


Expand for full commit details
```
     
    Bug: 486079015 
    Change-Id: I7047e2f0a210de1ae17cbb95884f3a6c6a6a6964 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7629495 
    Reviewed-by: Min Qin <qinmin@chromium.org> 
    Reviewed-by: Lily Chen <chlily@chromium.org> 
    Commit-Queue: Andrew Liu <liu@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1594178}

```

---

Files:

- M `chrome/browser/download/download_target_determiner.cc`
- M `chrome/browser/download/download_target_determiner_unittest.cc`

---

Hash: [8c1145d4b23d6a8cf2867b922716153f6ea72d9e](https://chromiumdash.appspot.com/commit/8c1145d4b23d6a8cf2867b922716153f6ea72d9e)  

Date: Wed Mar 4 20:47:47 2026


---

### mu...@gmail.com (2026-03-05)

Hello, I forgot to fill in the acknowledgment name in this report report. Could you please add `daffainfo` as the public acknowledgment? Thanks!

### mu...@gmail.com (2026-03-19)

Any update?

### ch...@google.com (2026-06-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. Exploit mitigation bypass with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486079015)*
