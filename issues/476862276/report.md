# Chrome (Windows): Opening download “demo. txt” executes sibling “demo. txt.exe” (object-level target confusion / unsafe Shell fallback)

| Field | Value |
|-------|-------|
| **Issue ID** | [476862276](https://issues.chromium.org/issues/476862276) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>PlatformIntegration |
| **Platforms** | Windows |
| **Reporter** | li...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2026-01-19 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

Chrome (Windows): Opening download “demo. txt” executes sibling “demo. txt.exe” (object-level target confusion / unsafe Shell fallback)

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

chrome://downloads/

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

On Windows, Chrome’s **Open** action for a downloaded file can execute a **different** sibling executable than the file shown/selected in the download UI. Specifically, clicking the download entry displayed as `demo. txt` results in Chrome creating a process for `demo. txt.exe`. This is an **object-level target confusion / intent-to-execution mismatch (A ≠ B)**, not a user UI mistake.

## Environment

- Platform: Windows 11 25H2 / Google Chrome Version 144.0.7559.60 (Official Build) (64-bit)
- Component: Chrome download bubble and `chrome://downloads` (“Open” action)
- Directory: `C:\Users\potat\Downloads\`

## Payload

cmd /c "type nul > \?%CD%\demo. txt"

## Steps to reproduce

1. Place two files in the same folder (`Downloads`):
   - `demo. txt` (text file)
   - `demo. txt.exe` (any Windows executable; e.g., a benign PoC that launches Calculator)
2. Trigger a download entry for `demo. txt` in Chrome so it appears in the download bubble and in `chrome://downloads` (e.g., download it from a test server).
3. In Chrome, click the download entry **`demo. txt`** (or click **Open**) in either:
   - the download bubble, or
   - `chrome://downloads`.

## Observed result

Chrome executes `demo. txt.exe` instead of opening `demo. txt`.

### ProcMon evidence (process creation)

Process Monitor shows Chrome eventually performing **Process Create** for:

- Path: `C:\Users\potat\Downloads\demo. txt.exe`
- Command line: `"C:\Users\potat\Downloads\demo. txt.exe"`

This occurs after Chrome attempts to access `...\demo. txt` and fails/gets denied, then falls back and ends up launching the sibling `...\demo. txt.exe`.

### Object-level proof (NTFS File ID mismatch)

The clicked file (`demo. txt`) and the executed file (`demo. txt.exe`) are **different NTFS objects**:

- `fsutil file queryfileid "C:\Users\potat\Downloads\demo. txt"`
  - File ID: `0x00000000000000000080000000001542`
- `fsutil file queryfileid "C:\Users\potat\Downloads\demo. txt.exe"`
  - File ID: `0x0000000000000000000d0000000018ad`

Since the File IDs differ, Chrome’s “Open” action is not bound to the download entry’s file object (A ≠ B).

## Expected result

Clicking “Open” for a download entry must open that **exact downloaded file object**, or **fail closed** with an error. It must not execute a different file (especially an executable) as a fallback.

## Security guidance (Microsoft)

Microsoft’s Windows Shell security guidance explicitly recommends that callers of **ShellExecute / ShellExecuteEx** provide an **unambiguous** execution target and use a **fully qualified path**, rather than relying on the Shell to locate/resolve the file. It states:

- “Make sure you provide an unambiguous definition of the application that is to be executed.”
- “When providing the executable file's path, provide the fully qualified path. Do not depend on the Shell to locate the file.”
- Searching default locations can be used in spoofing attacks; use a fully qualified path to ensure accessing the desired file.

Reference: <https://learn.microsoft.com/en-us/windows/win32/shell/sec-shell>

In this case, Chrome’s “Open” action for a download entry should remain bound to the downloaded file object (fail closed on error), rather than delegating to ambiguous Shell resolution that can result in executing a different file.

#### Impact analysis

This issue provides a **download-to-execution phishing primitive** on Windows: a victim is presented with a benign-looking Chrome download entry `demo. txt` and clicks **Open** (in the download bubble or `chrome://downloads`), but Chrome can instead execute a **different sibling executable** `demo. txt.exe` (A≠B).

**RCE is straightforward and does not require complex exploitation**: no memory corruption, no sandbox escape, and no multi-step chain. The attacker only needs to place two files in the same download location (`demo. txt` and an attacker-controlled `demo. txt.exe`). After a single user action, Chrome launches the attacker-controlled EXE, resulting in **arbitrary code execution in the context of the current user**. If the user runs Chrome with elevated rights (or is a local administrator), the attacker gains the same privilege level; otherwise it still enables user-level code execution and typical follow-on actions at that privilege level (persistence, credential theft, data exfiltration, lateral movement attempts).

Because the UI indicates the clicked item is a non-executable `.txt` file while the OS action performed is execution of an `.exe`, this can be used for **high-confidence social engineering/phishing** (misleading file-type expectation) and may bypass a user’s normal caution that would apply to explicitly downloaded executables.

---

### The cause

#### What version of Chrome have you found the security issue in?

Google Chrome Version 144.0.7559.60 (Official Build) (64-bit)

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Remote Code Execution (RCE)

#### How would you like to be publicly acknowledged for your report?

Han Liu (Xi’an Jiaotong University, School of Cyber Science and Engineering)

## Attachments

- [chrome_windows_download_open_exec_mismatch.zip](attachments/chrome_windows_download_open_exec_mismatch.zip) (application/zip, 3.4 MB)
- [demo. txt](attachments/demo. txt) (application/octet-stream, 0 B)
- [demo. txt.exe](attachments/demo. txt.exe) (application/x-msdownload, 48.0 KB)

## Timeline

### el...@chromium.org (2026-01-20)

Security shepherd: thanks for the report. I don't think this is a security bug really since you still have to trick the user into both downloading a malicious binary and clicking a similar download entry, but this *is* one of the most bizarre functional bugs I think I've ever seen, so, wow. I'll leave it as a Sev-3 vulnerability for now and ask Rob to double-check me.

Over to robliao@ who loves this kind of stuff :)

### ro...@chromium.org (2026-01-20)

Possible ShellExecute issue? Wouldn't be surprised. I'll take a quick look.

### dc...@chromium.org (2026-01-21)

This is unfortunate behavior, and we should fix it. It's a bit borderline about whether or not it's a security issue... I think it's low at best so I'll leave it there for now.

### ro...@chromium.org (2026-01-23)

Repro confirmed. Investigating.

### ro...@chromium.org (2026-01-23)

Sure enough, `ShellExecuteEx` is eagerly trying to run the exe, likely performing some sort of file extension resolution.

Scene of the Issue:

```
0:008> kc6
 # Call Site
00 SHELL32!ShellExecuteExW
01 chrome!ui::win::`anonymous namespace'::InvokeShellExecute
02 chrome!ui::win::OpenFileViaShell
03 chrome!platform_util::internal::PlatformOpenVerifiedItem
04 chrome!platform_util::`anonymous namespace'::VerifyAndOpenItemOnBlockingThread
0:008> .frame 1
01 00000074`4d7feba0 00007ffd`b9c31083     chrome!ui::win::`anonymous namespace'::InvokeShellExecute+0x1b3 [C:\b\s\w\ir\cache\builder\src\ui\base\win\shell.cc @ 67] 
0:008> dt sei
Local var @ 0x744d7febf0 Type _SHELLEXECUTEINFOW
   +0x000 cbSize           : 0x70
   +0x004 fMask            : 0x100 (SEE_MASK_NOASYNC)
   +0x008 hwnd             : (null) 
   +0x010 lpVerb           : (null) 
   +0x018 lpFile           : 0x00005ff4`03a83650  "C:\Temp\demo. txt"
   +0x020 lpParameters     : (null) 
   +0x028 lpDirectory      : 0x00005ff4`0ac74e90  "C:\Temp"
   +0x030 nShow            : 0n1 (SW_SHOWNORMAL)
   +0x038 hInstApp         : (null) 
   +0x040 lpIDList         : (null) 
   +0x048 lpClass          : (null) 
   +0x050 hkeyClass        : (null) 
   +0x058 dwHotKey         : 0
   +0x060 hIcon            : (null) 
   +0x060 hMonitor         : (null) 
   +0x068 hProcess         : (null) 

```

### ro...@chromium.org (2026-01-23)

Yep, and ShellExecute is indeed updating the path:

```
SHELL32!CShellExecute::_DoExecute:
00007ffe`733ef664 48895c2418      mov     qword ptr [rsp+18h],rbx ss:00000074`48fff900=0000017847d26270
0:065> dU poi(@rcx+230h)  <------------------------- Roughly target path for CShellExecute
00000178`4fcb3eb0  "C:\Temp\demo. txt"
0:065> ba w8 @rcx+230h
0:065> g
Breakpoint 4 hit
SHELL32!wil::details::unique_storage<wil::details::resource_policy<unsigned short * __ptr64,void (__cdecl*)(void * __ptr64),&CoTaskMemFree,wistd::integral_constant<unsigned __int64,0>,unsigned short * __ptr64,unsigned short * __ptr64,0,std::nullptr_t> >::reset+0x1b:
00007ffe`73391d5b 488b5c2430      mov     rbx,qword ptr [rsp+30h] ss:00000074`48fff5a0=000001784fcb3eb0
0:065> dU poi(@rbx)       <------------------------- New path!
00000178`4fdd8fb0  "C:\Temp\demo. txt.exe"
0:065> kn5
 # Child-SP          RetAddr               Call Site
00 00000074`48fff570 00007ffe`734e0d6e     SHELL32!wil::details::unique_storage<wil::details::resource_policy<unsigned short * __ptr64,void (__cdecl*)(void * __ptr64),&CoTaskMemFree,wistd::integral_constant<unsigned __int64,0>,unsigned short * __ptr64,unsigned short * __ptr64,0,std::nullptr_t> >::reset+0x1b
01 00000074`48fff5a0 00007ffe`7338c3ca     SHELL32!CShellExecute::CreateParsingBindCtx+0x154c46
02 00000074`48fff890 00007ffe`733ef75d     SHELL32!CShellExecute::ParseOrValidateTargetIdList+0x52
03 00000074`48fff8f0 00007ffe`733eda92     SHELL32!CShellExecute::_DoExecute+0xf9

```

### ro...@chromium.org (2026-01-23)

Haven't dug through all the details, but the working hypothesis is that ShellExecute will attempt to perform a legacy filename resolution to a filename ending with `.pif, .com, .exe, .bat, .lnk, or .cmd` if it receives a path without a valid extension. Extensions cannot have spaces, and thus `demo. txt` doesn't have an extension in the view of the Windows shell, triggering the resolution to `demo. txt.exe`.

`ShellExecute` should check to see if the path does indeed exist first, but that is a bug for Microsoft to fix.

The workaround for Chromium is to parse the path ourselves into an IDList and then pass that to `ShellExecute`. That appears to bypass legacy filename resolution.

### li...@gmail.com (2026-01-23)

Thanks for the investigation and stack traces. ShellExecuteW’s legacy filename resolution seems to be Windows compatibility/usability behavior, and it seems that resolving to an IDList/PIDL (Explorer-style) before invoking ShellExecute might help avoid A-click/B-execute (demo. txt → demo. txt.exe). Many thanks for looking into this.  :)

### dx...@google.com (2026-01-26)

Project: chromium/src  

Branch:  main  

Author:  Robert Liao [robliao@chromium.org](mailto:robliao@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7514332>

Manually Parse Paths to IDLists for ShellExecute

---


Expand for full commit details
```
     
    ShellExecute may perform incorrect legacy resolution for paths 
    that do not appear to have a valid extension (Example: file. ext). 
     
    Extensions cannot have spaces like in "file. ext", which convinces 
    ShellExecute to think that this is a legacy path like "chrome" that 
    needs to resolve to "chrome.exe". 
     
    ShellExecute will append one of the following extensions in an attempt 
    to "find" the corrected path, even if the provided path already 
    exists: 
      - .pif 
      - .com 
      - .exe 
      - .bat 
      - .lnk 
      - .cmd 
     
    There doesn't appear to be a way to tell ShellExecute through 
    SHELLEXECUTEINFO to avoid performing this legacy resolution other than 
    having the caller pre-parse the path into an ID list and passing the 
    ID list through SHELLEXECUTEINFO::lpIDList. 
     
    Fixed: 476862276 
    Bug: 478206473 
    Change-Id: I6c9b1d7b66a61fc4ab84ab7d5296ab099d96aa2b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7514332 
    Commit-Queue: Jesse McKenna <jessemckenna@google.com> 
    Auto-Submit: Robert Liao <robliao@chromium.org> 
    Reviewed-by: Jesse McKenna <jessemckenna@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1574631}

```

---

Files:

- M `ui/base/win/shell.cc`

---

Hash: [4333ac30e1d439c5f1781c3c57472d397e4ba6f3](https://chromiumdash.appspot.com/commit/4333ac30e1d439c5f1781c3c57472d397e4ba6f3)  

Date: Mon Jan 26 18:36:28 2026


---

### ch...@google.com (2026-03-10)

WARNING: Removing security\_release value because the issue is not on security\_impact-stable or security\_impact-extended hotlists. Please add to the correct hotlist if the issue is on a release branch.

### li...@gmail.com (2026-03-10)

Hi :)  just a quick heads-up: I've added the missing security_impact-stable hotlist. Could you please help re-add the Security_Release: 0-M146 label when you have a moment? Thank you!

### ch...@google.com (2026-03-28)

WARNING: Removing security\_release value because the issue is not on security\_impact-stable or security\_impact-extended hotlists. Please add to the correct hotlist if the issue is on a release branch.

### li...@gmail.com (2026-03-28)

It looks like the bot removed `Security_Release: 0-M146` again at 3:47 PM.

I had already added `security_impact-stable` on Mar 10, so I suspect there may be some internal hotlist or permission that my external account cannot set.

Could you please help add the issue to the correct stable-security hotlist internally and re-apply the label?

Thank you.

### dx...@google.com (2026-04-10)

Project: chromium/src  

Branch:  main  

Author:  Will Harris [wfh@chromium.org](mailto:wfh@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7722299>

Add regression test for path resolution from ShellExecute

---


Expand for full commit details
```
     
    In crrev.com/c/7514332 stricter path resolution was added to make sure 
    legacy filename resolution did not result in the incorrect target being 
    picked when calling ShellExecute. 
     
    This CL adds a regression test for this behavior, to verify both the old 
    and new codepaths behave as expected. 
     
    In the old codepath, the test EXE is executed, but in the new codepath 
    the shellexecute launches the .txt file as expected. 
     
    BUG=476862276 
     
    Change-Id: Iec580286dcd559d1d76acccebeb2cca657a23f37 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7722299 
    Reviewed-by: Robert Liao <robliao@chromium.org> 
    Commit-Queue: Will Harris <wfh@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1613106}

```

---

Files:

- M `ui/base/BUILD.gn`
- M `ui/base/win/shell.cc`
- M `ui/base/win/shell.h`
- A `ui/base/win/shell_test_helper.cc`
- A `ui/base/win/shell_unittest.cc`

---

Hash: [92b45f7cab0b07fb383c9d52366a4786fa4ff321](https://chromiumdash.appspot.com/commit/92b45f7cab0b07fb383c9d52366a4786fa4ff321)  

Date: Fri Apr 10 21:32:42 2026


---

### dx...@google.com (2026-04-13)

Project: chromium/src  

Branch:  main  

Author:  Shunya Shishido [sisidovski@chromium.org](mailto:sisidovski@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7753879>

Revert "Add regression test for path resolution from ShellExecute"

---


Expand for full commit details
```
     
    This reverts commit 92b45f7cab0b07fb383c9d52366a4786fa4ff321. 
     
    Reason for revert: ShellTest.OpenFileWithSpaceInExtension/AutomaticallyParsed fails on Windows. 
     
    Original change's description: 
    > Add regression test for path resolution from ShellExecute 
    > 
    > In crrev.com/c/7514332 stricter path resolution was added to make sure 
    > legacy filename resolution did not result in the incorrect target being 
    > picked when calling ShellExecute. 
    > 
    > This CL adds a regression test for this behavior, to verify both the old 
    > and new codepaths behave as expected. 
    > 
    > In the old codepath, the test EXE is executed, but in the new codepath 
    > the shellexecute launches the .txt file as expected. 
    > 
    > BUG=476862276 
    > 
    > Change-Id: Iec580286dcd559d1d76acccebeb2cca657a23f37 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7722299 
    > Reviewed-by: Robert Liao <robliao@chromium.org> 
    > Commit-Queue: Will Harris <wfh@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1613106} 
     
    Bug: 476862276, 501987421 
    Change-Id: Ic1cdff4ef9cdb51ee89cb69c726f1ec88e915578 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7753879 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Shunya Shishido <sisidovski@chromium.org> 
    Owners-Override: Shunya Shishido <sisidovski@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1613470}

```

---

Files:

- M `ui/base/BUILD.gn`
- M `ui/base/win/shell.cc`
- M `ui/base/win/shell.h`
- D `ui/base/win/shell_test_helper.cc`
- D `ui/base/win/shell_unittest.cc`

---

Hash: [d186f62fd974b4673cede59f9fdcff367bda4c41](https://chromiumdash.appspot.com/commit/d186f62fd974b4673cede59f9fdcff367bda4c41)  

Date: Mon Apr 13 02:04:37 2026


---

### dx...@google.com (2026-04-23)

Project: chromium/src  

Branch:  main  

Author:  Will Harris [wfh@chromium.org](mailto:wfh@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7784892>

Reland "Add regression test for path resolution from ShellExecute"

---


Expand for full commit details
```
     
    This is a reland of commit 92b45f7cab0b07fb383c9d52366a4786fa4ff321 
     
    The previous CL neglected to take into account that the test binary must 
    be standalone (no dependencies on other DLLs) to execute within the 
    temporary directory and this is not the case for asan or component 
    builds. 
     
    The updated CL therefore disables the test on these configurations, and 
    coverage is ensured in all other configurations. 
     
    Original change's description: 
    > Add regression test for path resolution from ShellExecute 
    > 
    > In crrev.com/c/7514332 stricter path resolution was added to make sure 
    > legacy filename resolution did not result in the incorrect target being 
    > picked when calling ShellExecute. 
    > 
    > This CL adds a regression test for this behavior, to verify both the old 
    > and new codepaths behave as expected. 
    > 
    > In the old codepath, the test EXE is executed, but in the new codepath 
    > the shellexecute launches the .txt file as expected. 
    > 
    > BUG=476862276 
    > 
    > Change-Id: Iec580286dcd559d1d76acccebeb2cca657a23f37 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7722299 
    > Reviewed-by: Robert Liao <robliao@chromium.org> 
    > Commit-Queue: Will Harris <wfh@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1613106} 
     
    Bug: 476862276 
    Change-Id: If91ad550753b2a6cf33de2343cecc61dbf797df5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7784892 
    Reviewed-by: Robert Liao <robliao@chromium.org> 
    Commit-Queue: Will Harris <wfh@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1619838}

```

---

Files:

- M `ui/base/BUILD.gn`
- M `ui/base/win/shell.cc`
- M `ui/base/win/shell.h`
- A `ui/base/win/shell_test_helper.cc`
- A `ui/base/win/shell_unittest.cc`

---

Hash: [4c0c96571f3e4adaa1fbede51b85ee92c8b4dbe9](https://chromiumdash.appspot.com/commit/4c0c96571f3e4adaa1fbede51b85ee92c8b4dbe9)  

Date: Thu Apr 23 23:45:13 2026


---

### ch...@google.com (2026-05-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-05-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
web platform privilege escalation, low impact


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

## Bounty Award

> web platform privilege escalation, low impact

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/476862276)*
