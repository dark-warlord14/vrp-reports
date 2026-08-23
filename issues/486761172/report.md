# Chrome on Windows can be tricked into saving a dangerous .url InternetShortcut without the .download

| Field | Value |
|-------|-------|
| **Issue ID** | [486761172](https://issues.chromium.org/issues/486761172) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Chrome Version** | 145.0.7632.110 (Official Build) (64-bit) |
| **Reporter** | ra...@gmail.com |
| **Assignee** | ya...@google.com |
| **Created** | 2026-02-23 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Run: poc\_alt.py (serves on 127.0.0.1:8001).
2. Chrome on Windows → open <http://127.0.0.1:8001/>.
3. Right-click “Bypass: photo.jpg %25%25.url” → “Save link as…”.
4. Save dialog suggests photo.jpg .url (type: Internet Shortcut). No .download rewrite.
5. Save & open: launches calc.exe (payload).

# Problem Description

- Windows shell strips %…% from the suggested filename, making the basename appear extensionless.
- GenerateSafeFileName() in download\_target\_determiner.cc (Windows path) calls net::GenerateSafeFileName() with old\_extension captured before sanitization.
- Because the basename now seems extensionless, the dangerous-extension rewrite is skipped, and .url is reattached verbatim.

# Summary

Chrome on Windows can be tricked into saving a dangerous .url InternetShortcut without the .download

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [poc_alt.py](attachments/poc_alt.py) (text/x-python, 4.8 KB)
- [poc_chrome.mp4](attachments/poc_chrome.mp4) (video/mp4, 34.1 MB)

## Timeline

### an...@chromium.org (2026-02-23)

This appears to be a variant of <https://issues.chromium.org/issues/444803530>.
@li...@google.com can you PTAL and re-route as necessary?

### ra...@gmail.com (2026-02-23)

Yeah you right, but its only work for rewriting .url extention. and also using %25%25 rather than %%

### ch...@google.com (2026-02-24)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-24)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2026-03-10)

liu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ra...@gmail.com (2026-03-17)

Any update ? 

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  main  

Author:  Andrew Liu [liu@chromium.org](mailto:liu@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7639229>

Fix Windows "Save As" dialog extension bypass

---


Expand for full commit details
```
     
    When a user downloads a file, Chrome sanitizes the filename by 
    removing environment variables to prevent evaluation on the client. 
    However, an attacker could supply a filename like "photo.jpg %%.url". 
    The single-pass environment variable removal would strip "%%" and 
    leave "photo.jpg .url". 
     
    Because the Windows "Save As"" dialog natively strips trailing spaces 
    and dots from the basename of a file, "photo.jpg .url" is displayed 
    to the user simply as "photo.jpg", hiding the true ".url" extension. 
    Because Chrome's GenerateSafeFileName was unaware of this native 
    Windows trimming, it allowed the file to be saved as an Internet 
    Shortcut without proper sanitization. 
     
    This CL fixes the bypass by implementing an iterative sanitization 
    loop in `DownloadTargetDeterminer`. This loop mimics the exact basename 
    trimming behavior of the Windows "Save As" dialog, reconstructing and 
    cleaning the filename until it stabilizes. This ensures that any 
    hidden extensions are exposed and properly evaluated by 
    `GenerateSafeFileName`. 
     
    Bug: 486761172 
    Change-Id: I532f733d8eee0ee23f34eebd7d44f6c66a6a6964 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7639229 
    Reviewed-by: Min Qin <qinmin@chromium.org> 
    Reviewed-by: Lily Chen <chlily@chromium.org> 
    Commit-Queue: Andrew Liu <liu@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1601428}

```

---

Files:

- M `chrome/browser/download/download_target_determiner.cc`
- M `chrome/browser/download/download_target_determiner_unittest.cc`

---

Hash: [9c229906472adc5a601eef5e419b2a6726e91cc7](https://chromiumdash.appspot.com/commit/9c229906472adc5a601eef5e419b2a6726e91cc7)  

Date: Wed Mar 18 18:36:07 2026


---

### ra...@gmail.com (2026-03-24)

Is this report eligible for bounty?

### ra...@gmail.com (2026-04-06)

Hi ! any update ? 

### ra...@gmail.com (2026-04-28)

Any update ? 

### ya...@google.com (2026-04-29)

[liu@chromium.org](mailto:liu@chromium.org) implemented a fix for this bug which should land in Chrome 148.0.7778.47

### ch...@google.com (2026-05-14)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### sp...@google.com (2026-05-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Low Severity / Low Impact - Below baseline exploit mitigation bypass


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ra...@gmail.com (2026-05-21)

Thank you, Team !

### ch...@google.com (2026-08-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486761172)*
