# Windows download logic flaw: % triggers double extension sanitization bypass (.lnk .lnk, .scf .scf)

| Field | Value |
|-------|-------|
| **Issue ID** | [444803530](https://issues.chromium.org/issues/444803530) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | br...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2025-09-13 |
| **Bounty** | $3,000.00 |

## Description

**Description**

Chrome on Windows can be tricked into delivering **dangerous file types** (for example, **.lnk** or **.scf**) despite the download sanitization that should rewrite them to **.download**.

When a suggested filename includes certain **%** sequences after a space following the extension, Chrome strips the **%** tokens, then **re-applies the original extension**, yielding a **double extension** (for example, **file.lnk .lnk**). As a result, the forbidden extension survives instead of being rewritten.

This appears to be a **Windows-only issue**, because the Windows file dialog expands or strips `%…%` patterns and the sanitization path subsequently reattaches the stale extension.

**Examples**

- `Content-Disposition: attachment; filename="file.lnk %%"`  
  
  **Result:** `file.lnk .lnk` (expected: **file.download**)
- `Content-Disposition: attachment; filename="file.scf .%%"`  
  
  **Result:** `file.scf .scf` (expected: **file.download**)

**Expected behavior**
Dangerous extensions (for example, **.lnk**, **.scf**) should always be rewritten to **.download**. No combination of spaces or **%** should allow the original extension to persist or reappear.

**Observed behavior**
Appending `" %%"` (or similar) after the extension leads to a **double extension**, allowing **.lnk** or **.scf** to survive (for example, **file.lnk .lnk**). This bypasses Chrome’s dangerous-file protection and presents users with a misleading, executable shortcut.

**Security impact**
This is a **sanitization bypass** that enables delivery of files Chrome intends to block. A user can be tricked into saving and executing a Windows shortcut (**.lnk**) that appears benign (for example, disguised as an “image” or document link). Impact includes **code execution** or **persistence** via shortcut abuse.

**Steps to reproduce**

1. Run the attached PoC server (**poc.py**). It serves a page with two tiles and download endpoints that set **Content-Disposition**.
2. Visit `http://127.0.0.1:8000/` in Chrome on **Windows**.
3. **Right-click → “Save link as…”** on:
   - **Control:** `/download?case=lnk_plain` → `filename="file.lnk"` (should be rewritten to **.download**).
   - **Bypass:** `/download?case=lnk_pct` → `filename="file.lnk %%"` (often shows **file.lnk .lnk**).
4. Observe the suggested filename in the Save dialog and the final saved name.

Note: The PoC serves a harmless **payload.download** file so the saved file is never HTML. It isolates the filename/extension behavior under **Content-Disposition**.

**Affected versions (observed)**

- Stable: **140.0.7339.128**
- Beta: **141.0.7390.16**
- Dev: **142.0.7405.4**

**Bisect results (observed)**

- Last known developer build **without** the issue: `Win/1023679` (**105.0.5178.0 Dev**).
- First developer build **with** the issue: `Win/1025642` (**105.0.5190.0 Dev**).
- This aligns with commit **5e105f0bc3443e873924b92778574ffbb792c645**, which landed in 105.0.5183.0 and modified the Windows filename sanitization logic.

**Root cause (high level)**

- On Windows, the Save dialog layer strips `%…%` from the basename. With inputs like `"file.lnk %%"`, this leaves `"file.lnk "` (with a trailing space).
- Later, the download target logic calls safe-name handling with the **pre-sanitization extension** (for example, **.lnk**) while the **post-sanitized basename** appears extensionless.
- The safe-name logic then **re-attaches** the old extension, producing **file.lnk .lnk** and bypassing the **.lnk → .download** rewrite.

**PoC**
Attach **poc.py** (serves a self-contained HTML page and `Content-Disposition` endpoints). Usage:

## Attachments

- [poc.py](attachments/poc.py) (text/x-python, 9.1 KB)

## Timeline

### br...@gmail.com (2025-09-14)

I can prepare and submit a patch with a unit test if the team would like, please let me know if that would be useful.

### ch...@google.com (2025-09-16)

Setting milestone because of s2 severity.

### ch...@google.com (2025-09-16)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-09-30)

xinghuilu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-15)

xinghuilu: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-30)

xinghuilu: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-10-31)

Project: chromium/src  

Branch:  main  

Author:  Kovacs Zeteny [brightbulbapp@gmail.com](mailto:brightbulbapp@gmail.com)  

Link:    <https://chromium-review.googlesource.com/6990751>

Windows: fix bug that could re-attach dangerous extension

---


Expand for full commit details
```
     
    This CL ensures that after environment variable markers and trailing 
    characters are stripped from a filename on Windows, the extension is 
    derived from the sanitized basename. Without this, Chrome could fall 
    back to re-attaching the original extension, leading to cases like 
    ".txt .txt" or allowing blocked types such as ".lnk" to reappear. 
     
    Bug: 444803530 
    Change-Id: Ie8f19b7ef4777721e7ac1376957cda55250142b4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6990751 
    Reviewed-by: Min Qin <qinmin@chromium.org> 
    Reviewed-by: Xinghui Lu <xinghuilu@chromium.org> 
    Commit-Queue: Min Qin <qinmin@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1538683}

```

---

Files:

- M `chrome/browser/download/download_target_determiner.cc`
- M `chrome/browser/download/download_target_determiner_unittest.cc`

---

Hash: [5e9cd600b865a126eb6d14ffb06dd311d6267faa](https://chromiumdash.appspot.com/commit/5e9cd600b865a126eb6d14ffb06dd311d6267faa)  

Date: Fri Oct 31 17:07:46 2025


---

### br...@gmail.com (2025-11-03)

Hello, this CL: <https://chromium.googlesource.com/chromium/src/+/5e9cd600b865a126eb6d14ffb06dd311d6267faa> fixes the issue, can it be marked as fixed?

### xi...@chromium.org (2025-11-04)

Thanks for fixing this issue!

### sp...@google.com (2025-11-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
1k for the bug (highly mitigated exploitation mitigation bypass), 1k for the patch, 1k for the bisect = 3k


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-02-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> 1k for the bug (highly mitigated exploitation mitigation bypass), 1k for the patch, 1k for the bisect = 3k

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/444803530)*
