# Elevation of Privilege in GoogleUpdate with Windows

| Field | Value |
|-------|-------|
| **Issue ID** | [503393471](https://issues.chromium.org/issues/503393471) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Updater |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2024-1694 |
| **Reporter** | do...@pksecurity.io |
| **Assignee** | ga...@chromium.org |
| **Created** | 2026-04-16 |
| **Bounty** | $5,000.00 |

## Description

---

### Report description

Local Privilege Escalation / Arbitrary File Deletion via Directory Junction Traversal in base::DeletePathRecursively

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/base/files/file_enumerator_win.cc> & <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/base/files/file_util_win.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

**1 Executive Summary**

A critical Local Privilege Escalation (LPE) and Arbitrary File Deletion vulnerability exists in Chromium's Windows environment due to insecure handling of Directory Junctions (Reparse Points) within `base::DeletePathRecursively`. Attackers with low-privileged access (Medium Integrity) can plant a malicious NTFS Directory Junction in a user-writable path such as `%LocalAppData%\Google\Chrome\User Data`. When an elevated Chromium process (e.g., the Chrome Uninstaller executing as High Integrity) triggers `DeletePathRecursively` on this path to clear browsing data, the API blindly traverses the Junction and securely deletes the contents of the target directory. This can be weaponized to wipe protected system directories (e.g., `C:\Windows\System32` or `C:\Config.Msi`), resulting in severe Denial of Service (DoS) or SYSTEM level code execution (EoP) via file planting.

**2. Vulnerability Details**

- **Vulnerability Type:** Arbitrary File Deletion / Local Privilege Escalation (EoP)
- **Severity:** Critical (P1/S1) Affected Component: Chromium / Base Engine OS Layer (Windows)
- **Vulnerable Module:** `src/base/files/file_util_win.cc` & `src/base/files/file_enumerator_win.cc`
- **Vulnerable Function(s):** `FileEnumerator::FileInfo::IsDirectory()` and `base::DeleteFileRecursive()`

**3. Root Cause Analysis**

The root cause of this vulnerability lies in the implementation of the `FileEnumerator` and the `DeleteFileRecursive` algorithms inside the Chromium codebase for the Windows platform.

**Code Location:** `src/base/files/file_enumerator_win.cc`

**Function:** `FileEnumerator::FileInfo::IsDirectory()`

When the Windows kernel (`FindFirstFileExW`) scans an item that is a Directory Junction, it returns a bitmask containing both `FILE_ATTRIBUTE_DIRECTORY` and `FILE_ATTRIBUTE_REPARSE_POINT`.

However, Chromium's internal `IsDirectory()` implementation performs the following incomplete check:

```
bool FileEnumerator::FileInfo::IsDirectory() const {
  return (find_data().dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0;
}

```

Crucially, it fails to evaluate `FILE_ATTRIBUTE_REPARSE_POINT`.
Because of this flaw, when `src/base/files/file_util_win.cc` calls `DeleteFileRecursive(...)`, it perceives the malicious Junction merely as a valid subdirectory. It proceeds to make a recursive call appending `\*` to the junction path. The Windows OS seamlessly resolves the shortcut and directs the file enumeration into the attacker's chosen protected directory, causing the immediate and recursive deletion of the target's contents under the security context of the executing thread.

*(**Note:** The POSIX implementation inside `file_util_posix.cc` correctly refuses to traverse symlinks, making this gap specifically a Windows OS flaw).*

**4. Steps to Reproduce (Working PoC)**

**Phase 1: Environment Preparation (Target Creation)**

1. Install a fresh instance of Google Chrome on a Windows VM (Ensure the browser uses the default paths).
2. Launch Google Chrome at least once, then close it entirely. (This ensures the `%LocalAppData%\Google\Chrome\User Data` folder is instantiated).
3. Open an Elevated Command Prompt (**Administrator Mode**) to create a system-protected dummy folder simulating an OS-level target:

```
mkdir C:\Protected_Dummy
echo "CRITICAL SYSTEM FILE" > C:\Protected_Dummy\secret_system_file.txt

```

4. Secure the dummy file so standard users cannot delete it. In the Administrator Command Prompt, execute:

```
# File permissions change assigned only Administrator and System full-control access.

$Acl = Get-Acl "C:\Protected_Dummy\secret_system_file.txt"
$Acl.SetAccessRuleProtection($true, $false)
$AdminRule = New-Object System.Security.AccessControl.FileSystemAccessRule("Administrators","FullControl","Allow")
$SystemRule = New-Object System.Security.AccessControl.FileSystemAccessRule("SYSTEM","FullControl","Allow")
$Acl.AddAccessRule($AdminRule)
$Acl.AddAccessRule($SystemRule)
Set-Acl "C:\Protected_Dummy\secret_system_file.txt" $Acl

```

*(At this point, a normal Medium-Integrity user attempting to delete this folder/file will receive an "Access Denied" UAC error popup).*

**Phase 2: The Exploit Payload (Junction Creation)**

5. Open a **Standard (Non-Elevated)** Command Prompt.
6. The attacker (Standard user) plants the Directory Junction inside the Chrome `User Data` folder, forcibly pointing it to the protected system directory:

```
mklink /J "%LocalAppData%\Google\Chrome\User Data\Trap_Link" "C:\Protected_Dummy"

```

**Phase 3: Triggering the Vulnerable Execution**

7. Navigate to **Windows Settings > Apps > Installed apps** (or Control Panel).
8. Locate **Google Chrome** and select **Uninstall**.
9. The Chromium Uninstaller will prompt for UAC Elevation because it requires Administrator permissions to remove system-wide registry fragments. Click **Yes/Continue**.
10. In the Chrome uninstallation dialog, check the box: **"Also delete your browsing data?"**.
11. Click the **Uninstall** button.

**Phase 4: Verification & Impact**

12. After the uninstallation completes, navigate back to the **C:\Protected\_Dummy** folder.
13. **Result:** The `secret_system_file.txt` file has been irrevocably wiped! The `base::DeletePathRecursively()` function successfully bypassed its directory bounds by blindly traversing the attacker's `Trap_Link` junction with Administrator privileges, demonstrating a severe Arbitrary File Deletion / privilege escalation primitive.

**5. Real-World Business Impact (Google & Customers)**

The failure to restrict directory junction traversals inside a foundational API like `base::DeletePathRecursively` introduces a severe, widespread risk to both everyday consumers and Google's Enterprise user base.

**1. Catastrophic Denial of Service (OS Bricking) for Enterprise Customers:** If a malicious standard user or basic malware drops this silent junction trap, an automated rollout of Chrome updates or uninstallation scripts via Google Updater executing as SYSTEM will traverse the shortcut. This will irreparably wipe targeted critical OS directories (e.g., `C:\Windows\System32`), rendering enterprise workstations instantly unbootable (BSOD) and causing massive organizational downtime and data loss.

**2. Full System Compromise (Local Privilege Escalation):** Advanced Persistent Threats (APTs) or ransomware groups frequently weaponize "Arbitrary File Deletion" primitives to escalate their privileges to SYSTEM level code-execution. By forcing elevated Chromium processes to securely delete highly protected system services folders (e.g., `C:\Config.Msi` or `C:\ProgramData\...`), attackers can instantly bypass OS protection boundaries and plant their own malicious payloads into those system-trusted locations. This neutralizes Endpoint Detection and Response (EDR) solutions, allowing rootkit installations and full data exfiltration.

**3. Cascading Supply Chain Risk (Chromium Base Framework):** Because the flawed logic resides natively inside `src/base/files`, the impact extends far beyond just Google Chrome. Any downstream application built upon the Chromium framework—including hundreds of enterprise Electron apps, Microsoft Edge, Brave, and internal Google tooling on Windows OS—that utilizes `base::DeletePathRecursively` to manage user profiles or clear caches inherently inherits this zero-day Elevation of Privilege vulnerability.

**6. Technical Remediation & Proposed Fix**

The core vulnerability relies on the logic omitting validation for NTFS Reparse Points (Junctions and Symlinks) while traversing directories in the Windows environment.

We propose that the Chromium engineering team explicitly filter out `FILE_ATTRIBUTE_REPARSE_POINT` checks before attempting to apply recursive file enumeration on what the OS interprets as a directory structure.

**Location:** `src/base/files/file_util_win.cc`
**Function:** `DeleteFileRecursive(...)`

**Vulnerable Code Snippet:** Currently, when `DeleteFileRecursive` utilizes `traversal.GetInfo()`, the algorithm invokes the `IsDirectory()` helper and proceeds to blindly recurse if it returns true.

```
DWORD this_result = ERROR_SUCCESS;
    if (info.IsDirectory()) {
      if (recursive) {
        this_result = DeleteFileRecursive(current, pattern, true); // <--- Triggers traversal vulnerability
        // ...
      }
    }

```

**Proposed Code Patch (C++ Fix):**
The routine must be modified to aggressively interrogate the `dwFileAttributes` against the `FILE_ATTRIBUTE_REPARSE_POINT` flag. If the target is a junction or symlink, the utility should skip the recursive descent block entirely and proceed directly to `RemoveDirectory()` to drop the malicious shortcut itself securely without evaluating its contents.

```
DWORD this_result = ERROR_SUCCESS;
+    
+    // Extract the raw file attributes to verify for NTFS Reparse Points (Junctions/Symlinks).
+    const bool is_reparse_point = (info.find_data().dwFileAttributes & FILE_ATTRIBUTE_REPARSE_POINT) != 0;
-    if (info.IsDirectory()) {
+    // Only recurse into authentic directories, never into attacker-controlled junctions.
+    if (info.IsDirectory() && !is_reparse_point) {
       if (recursive) {
         this_result = DeleteFileRecursive(current, pattern, true);
         DCHECK_NE(static_cast<LONG>(this_result), ERROR_FILE_NOT_FOUND);
         DCHECK_NE(static_cast<LONG>(this_result), ERROR_PATH_NOT_FOUND);
         if (this_result == ERROR_SUCCESS &&
             !::RemoveDirectory(current.value().c_str())) {
           this_result = ReturnLastErrorOrSuccessOnNotFound();
         }
       }
+    } else if (info.IsDirectory() && is_reparse_point) {
+      // Safely delete the malicious junction artifact itself without entering it.
+      if (!::RemoveDirectory(current.value().c_str())) {
+        this_result = ReturnLastErrorOrSuccessOnNotFound();
+      }
     } else if (!::DeleteFile(current.value().c_str())) {
       this_result = ReturnLastErrorOrSuccessOnNotFound();
     }

```

Implementing this strict bitmask validation will seamlessly align the Windows `file_util_win.cc` logic with its POSIX (`file_util_posix.cc`) counterpart, rendering this LPE threat completely inert.

#### Impact analysis

**Impact Analysis**

**Who can exploit the vulnerability?**

Any local attacker or malicious payload (such as a macro or script in an initial phishing foothold) executing with basic, unprivileged/standard user rights (Medium Integrity) on a Windows host running Google Chrome or any Chromium-dependent application.

**What they gain when doing so?**

The attacker gains a devastating **Arbitrary File Deletion primitive executed as an Elevated Administrator/SYSTEM**. Because the attacker controls the target destination via the malicious Junction trap, what they ultimately gain is:

**1. Targeted Denial of Service (OS Destruction):**

By redirecting the Chromium `base::DeletePathRecursively` execution to core directories (like `C:\Windows\System32`), the attacker can irreversibly wipe essential operating system files, resulting in an unbootable OS (BSOD) and extensive corporate data loss.

**2. Local Privilege Escalation (Elevation to SYSTEM):**

Wiping specific highly-protected services or configuration folders (such as `C:\Config.Msi` or `C:\ProgramData\Microsoft`) strips downstream OS boundaries. An attacker can immediately rebuild these wiped nodes using standard permissions to drop malicious payloads, guaranteeing their rootkits are executed centrally as `SYSTEM` by the OS upon reboot or update—effectively owning the entire machine.

---

### The cause

#### What version of Chrome have you found the security issue in?

Version 147.0.7727.102

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Privilege Escalation

#### How would you like to be publicly acknowledged for your report?

sachinpatilsp

## Attachments

- [01_Target_Environment_Setup_with_Admin_ACLs.png](attachments/01_Target_Environment_Setup_with_Admin_ACLs.png) (image/png, 64.2 KB)
- [05_Malicious_Junction_Created_In_UserData.png](attachments/05_Malicious_Junction_Created_In_UserData.png) (image/png, 104.0 KB)
- [06_Vulnerable_Chrome_Version_Tested.png](attachments/06_Vulnerable_Chrome_Version_Tested.png) (image/png, 10.8 KB)
- [03_UAC_Delete_Protection_Triggered.png](attachments/03_UAC_Delete_Protection_Triggered.png) (image/png, 22.6 KB)
- [04_Planting_Malicious_Directory_Junction.png](attachments/04_Planting_Malicious_Directory_Junction.png) (image/png, 6.5 KB)
- [02_Verifying_Access_Denied_For_Standard_User.png](attachments/02_Verifying_Access_Denied_For_Standard_User.png) (image/png, 7.5 KB)
- [08_Initiating_The_Vulnerable_Execution_Trigger.png](attachments/08_Initiating_The_Vulnerable_Execution_Trigger.png) (image/png, 12.5 KB)
- [09_Arbitrary_File_Deletion_Confirmed.png](attachments/09_Arbitrary_File_Deletion_Confirmed.png) (image/png, 30.8 KB)
- [07_Pre_Execution_State_With_Target_Intact.png](attachments/07_Pre_Execution_State_With_Target_Intact.png) (image/png, 29.1 KB)
- [Poc Chromium Arbitrary File Deletion Eop.mp4](attachments/Poc Chromium Arbitrary File Deletion Eop.mp4) (video/mp4, 5.7 MB)
- [Poc Chromium Arbitrary File Deletion Eop.mp4](attachments/Poc Chromium Arbitrary File Deletion Eop_75630460.mp4) (video/mp4, 5.7 MB)
- [08_Initiating_The_Vulnerable_Execution_Trigger.png](attachments/08_Initiating_The_Vulnerable_Execution_Trigger_75630461.png) (image/png, 12.5 KB)
- [01_Target_Environment_Setup_with_Admin_ACLs.png](attachments/01_Target_Environment_Setup_with_Admin_ACLs_75630462.png) (image/png, 64.2 KB)
- [04_Planting_Malicious_Directory_Junction.png](attachments/04_Planting_Malicious_Directory_Junction_75630463.png) (image/png, 6.5 KB)
- [02_Verifying_Access_Denied_For_Standard_User.png](attachments/02_Verifying_Access_Denied_For_Standard_User_75630464.png) (image/png, 7.5 KB)
- [06_Vulnerable_Chrome_Version_Tested.png](attachments/06_Vulnerable_Chrome_Version_Tested_75630465.png) (image/png, 10.8 KB)
- [03_UAC_Delete_Protection_Triggered.png](attachments/03_UAC_Delete_Protection_Triggered_75630466.png) (image/png, 22.6 KB)
- [07_Pre_Execution_State_With_Target_Intact.png](attachments/07_Pre_Execution_State_With_Target_Intact_75630467.png) (image/png, 29.1 KB)
- [09_Arbitrary_File_Deletion_Confirmed.png](attachments/09_Arbitrary_File_Deletion_Confirmed_75630468.png) (image/png, 30.8 KB)
- [05_Malicious_Junction_Created_In_UserData.png](attachments/05_Malicious_Junction_Created_In_UserData_75630469.png) (image/png, 104.0 KB)

## Timeline

### ma...@google.com (2026-04-16)

Local attackers are outside Chrome's threat model.

<https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md#Why-arent-physically_local-attacks-in-Chromes-threat-model>

### sa...@gmail.com (2026-04-17)

Hi Security Team,

Thank you for the initial review. I completely understand that physically local attackers targeting Chrome's own user data fall outside the threat model. However, I kindly request a reassessment because this report demonstrates a Local Privilege Escalation (LPE) breaking a Windows OS security boundary via a Chrome component acting as a Confused Deputy. As explicitly stated in the **Chrome VRP reward guidelines: "Valid reports of LPE vulnerabilities should demonstrate exploitability that breaks an OS security boundary using a Chrome component."**

I would like to respectfully point out a direct precedent: **<https://issues.chromium.org/issues/40946325> (CVE-2024-1694)**, which was accepted, fixed, and rewarded by the Chrome VRP recently

**The similarities between that accepted issue and my report are identical in nature:**

1. Both involve a Medium/Standard user creating a Directory Junction / Symbolic Link in a user-writable path (`%AppData%\Local` vs `%LocalAppData%\Google\Chrome\User Data`).
2. Both involve an Elevated Chromium component (`GoogleUpdate.exe as SYSTEM` vs `Chrome Uninstaller as High Integrity`) blindly traversing the attacker-controlled junction.
3. **Both result in Arbitrary File Deletion of highly protected OS system files** (e.g., `C:\Windows\System32`), leading to Denial of Service or EoP via file planting.

Since the core vulnerability resides in the Chromium engine's `base::DeletePathRecursively` failing to check the `FILE_ATTRIBUTE_REPARSE_POINT` bitmask before traversing (**similar to the update service flaw**), it weaponizes the Chrome Uninstaller to bypass Windows UAC and OS boundaries.

Given the identical attack primitive, the explicit VRP rule for LPEs, and the impact mirroring **CVE-2024-1694**, could you please take a second look at the provided PoC video and reassess this report?

**Thank you for your time and continuous efforts.**

Sachin Patil

### ch...@google.com (2026-04-17)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-07-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/503393471)*
