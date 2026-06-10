# Security: showSaveFilePicker allowing to save .lnk and .local files on windows!

| Field | Value |
|-------|-------|
| **Issue ID** | [407453835](https://issues.chromium.org/issues/407453835) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ma...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2025-03-31 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

[File System Access API] Previously Fixed Restriction on .local Files Not Enforced

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/+/refs/tags/134.0.6998.187/content/browser/file_system_access/file_system_chooser.cc#319>

---

### The problem

#### Please describe the technical details of the vulnerability

The File System Access API previously ([issue 40053671](https://issues.chromium.org/issues/40053671)) restricted saving files with a `.local` extension. However, this restriction appears to be relaxed or fails to pass the tests, allowing users to create and save `.local` files.

### Version

ChromeOS

```
Google Chrome	134.0.6998.130 (Official Build) (64-bit) 
Revision	725298d6794058a772955701177cd7f81987fa57-refs/branch-heads/6998@{#2079}
Platform	16181.47.0 (Official Build) stable-channel octopus

```

Windows

```
Google Chrome	134.0.6998.166 (Official Build) (64-bit) (cohort: Stable) 
Revision	0b26d3a1ee1e44572492002c2e52ffcd13ac701b-refs/branch-heads/6998@{#2123}
OS	        Windows 10 Version 21H2 (Build 19044.1288)

```
### Affected Component

- **File:** [`file_system_chooser.cc`](https://chromium.googlesource.com/chromium/src/+/refs/tags/134.0.6998.187/content/browser/file_system_access/file_system_chooser.cc#319)
- **Chromium Version:** `134.0.6998.187`

### Steps to Reproduce (Using VSCode.dev)

1. Open [VSCode.dev](https://vscode.dev/).
2. Click on `File` > `Open Folder` and grant access to a test directory.
3. Create a new file and name it `test.local`.

The `test.local` file should be created successfully in the workspace folder.

### Expected Behavior

- Saving a file with a `.local` extension should be restricted.
- When testing in vscode.dev, there should be a warning of failed file creation (you can try by creating a `.lnk` or `.sfc` files).

### Suggested Fix

- Re-evaluate the enforcement mechanism for restricted file extensions in the File System Access API.

#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

As per this issue: [Security: showSaveFilePicker allowing to save .lnk and .local files on windows!](https://issues.chromium.org/issues/40053671), `.local` files may influence which DLLs an application loads on Windows.

Related docs: [Microsoft - Dynamic-link library redirection](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-redirection)

---

### The cause

#### What version of Chrome have you found the security issue in?

134.0.6998.130 stable

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Other

#### How would you like to be publicly acknowledged for your report?

vanillawebdev

## Attachments

- [cast (4).webm](attachments/cast (4).webm) (video/webm, 7.5 MB)

## Timeline

### za...@google.com (2025-03-31)

Hi thanks for reporting. I have tried to reproduce on M123 and M134 Chrome builds, they work as intended.
Here are the scenarios I tested, note the 2 builds behaved the same:

I create a new file and name it test.local, then the browser will prompt a save window with the name "test" in File Name input bar;

1. if I do nothing and click save, it will create a .download file for me - which is expected
   or
2. if I overwrite the default File Name with test.local, it will show a warning dialog saying the file type can be dangerous - also expected

I tagged asully@ just as an FYI, if they disagree.

After thoroughly testing the different builds, I think this behavior is expected. I will close this bug as WAI. Please open a new bug if you disagree. I have attached my testing video, please take a look. Thanks for reporting!

### as...@chromium.org (2025-04-01)

Thank you zackhan@ for the clear repro. This seems WAI as per the comment on <https://crrev.com/c/5875189>. CC @me...@chromium.org

### ch...@google.com (2025-07-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/407453835)*
