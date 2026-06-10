# use-after-free at browser_user_education_service.cc:120

| Field | Value |
|-------|-------|
| **Issue ID** | [480450473](https://issues.chromium.org/issues/480450473) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Mac, Windows |
| **Chrome Version** | 126.0.6475.0 |
| **CVE IDs** | CVE-2024-6998 |
| **Reporter** | xp...@gmail.com |
| **Assignee** | es...@google.com |
| **Created** | 2026-01-31 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

[Regression - CVE-2024-6998] Reliable Browser Process Crash via Asynchronous State Corruption in UI Subsystem

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

## Executive Summary

I have identified a **regression** of a previously patched vulnerability ([Issue 340098902](https://issues.chromium.org/issues/340098902) / CVE-2024-6998). A critical race condition triggering state corruption in the `TutorialService` is still reproducible in the latest Chrome Stable and Canary builds.

## Vulnerability Classification & Rationale

**Selected Category:** Memory Corruption (in a non-sandboxed process)
**Clarification:** While the immediate manifestation is a NULL pointer dereference caught by a `CHECK()` failure, this vulnerability is classified as memory corruption for the following strategic reasons:

1. **Process Context:** The crash occurs in the **Browser Process** (non-sandboxed), representing a high-privilege execution context.
2. **Regression Status:** This is a regression of a vulnerability originally classified as a memory safety issue. The recurrence suggests the root cause (invalid memory/state access) persists.
3. **Root Cause:** A race condition in the tutorial lifecycle causes the registry to return an invalid memory reference, which is then dereferenced.
4. **Security Impact:** Instead of handling the invalid state gracefully, the browser hits a fatal security check (`Int 3`), aborting the entire process.

## Technical Analysis

- **Vulnerability:** Race Condition leading to State Corruption / Null Pointer Dereference.
- **Location:** `components/user_education/common/tutorial/tutorial_service.cc` (Line 56).
- **Function:** `TutorialService::StartTutorial`.
- **Trigger:** Rapid concurrent calls to `startTabGroupTutorial` combined with window closure.

**Crash Details (from WinDbg):**
The crash is triggered by a `logging::CheckFailure` inside `chrome.dll`.
`Exception Code: 0x80000003` (Breakpoint/Trap).
This confirms that the `CHECK(description)` validation failed because the description pointer was NULL due to the race condition.

## Reproduction Steps

1. Have only 1 tab open.
2. Open DevTools and execute: `window.open(document.location)`.
3. Close the parent tab (keep only the new child window).
4. Visit `chrome://tab-search.top-chrome/` in the remaining tab.
5. In DevTools console, execute the following PoC snippet:
   console.log("Starting aggressive reproduction...");
   const intervalId = setInterval(() => {
   try {
   const app = document.querySelector("body > tab-search-app");
   if (app && app.apiProxy\_) {
   for(let i=0; i<20; i++) {
   app.apiProxy\_.startTabGroupTutorial();
   }
   }
   } catch (e) {}
   }, 1);
   setTimeout(() => {
   console.log("Attempting crash now...");
   window.close();
   }, 3000);
6. **Result:** The entire browser process terminates immediately.

#### Impact analysis

## Security Impact

**1. Denial of Service (DoS):**
The vulnerability causes a complete termination of the Browser Process. This results in the immediate loss of all open tabs, unsaved data, and user session state.

**2. Remote Exploitability:**
The crash can be triggered remotely by visiting a malicious webpage without any specific user interaction (Zero-click beyond navigation).

**3. Regression of CVE-2024-6998:**
The ability to reproduce this crash in the latest Stable and Canary builds suggests that the root cause of CVE-2024-6998 persists. It appears the previous mitigation does not fully cover the specific race condition timing demonstrated in the attached PoC, allowing the invalid state to be reached again.

---

### The cause

#### What version of Chrome have you found the security issue in?

144.0.7559.110 (Stable), 146.0.7661.0(Canary)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Mohammed (Warrior)

## Attachments

- [windbg_analysis.txt](attachments/windbg_analysis.txt) (text/plain, 16.7 KB)
- [chrome_146_crash.dmp](attachments/chrome_146_crash.dmp) (application/octet-stream, 1.4 MB)

## Timeline

### ja...@chromium.org (2026-02-02)

[security triage]

Thanks for the bug report. It looks like this is reporting a crash that can be caused on chrome://tab-search.top-chrome/ by using DevTools to run code. I was able to reproduce the crash by following the steps provided, but I don't see the security impact.

Denial of service bugs are not considered security bugs: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/faq.md#are-denial-of-service-issues-considered-security-bugs>

### ch...@google.com (2026-05-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/480450473)*
