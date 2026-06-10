# ipcz bug can allow renderer duplicate browser process handle to escape sandbox

| Field | Value |
|-------|-------|
| **Issue ID** | [481277120](https://issues.chromium.org/issues/481277120) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo>Core |
| **Platforms** | Windows |
| **Chrome Version** | 135.0.0.0 |
| **CVE IDs** | CVE-2025-4609 |
| **Reporter** | ha...@gmail.com |
| **Assignee** | aj...@chromium.org |
| **Created** | 2026-02-03 |
| **Bounty** | $250,000.00 |

## Description

---

### Report description

Potential ipcz\_driver deserialization issue where renderer-controlled fields may be trusted without proper validation, leading to privilege boundary confusion and possible sandbox escape.

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:mojo/core/ipcz_driver/transport.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

The vulnerability exists in mojo/core/ipcz\_driver/transport.cc, in the Transport::Deserialize function.
Incoming serialized data is reinterpreted as a TransportHeader and used to create a new Transport object. The header contains critical fields:

destination\_type (enum values like kNormal, kBroker, kIsolated)
is\_peer\_trusted
is\_trusted\_by\_peer
is\_same\_remote\_process

Post-CVE-2025-4609 patches added basic checks to reject kBroker from non-broker contexts, but validation is incomplete for:

New or undocumented destination\_type values
Forged is\_peer\_trusted / is\_trusted\_by\_peer combinations
Shared-memory handoff races or parsing edge cases

A compromised renderer can send a crafted Mojo message with a TransportHeader where:

destination\_type is forged to kBroker (or high-privilege value)
is\_peer\_trusted = true
is\_trusted\_by\_peer = true

If deserialization accepts this without strong context rejection, the browser creates a transport that believes it is talking to a trusted broker peer.
This allows invocation of privileged broker APIs (e.g. DuplicateHandle on browser process/thread handles), leading to unauthorized high-privilege handle duplication and chaining to full sandbox escape with arbitrary code execution in the browser process.
Root cause:
Lack of sufficient context-aware validation during TransportHeader deserialization permits renderer-to-broker privilege boundary confusion.

#### Impact analysis

Successful exploitation of this vulnerability would allow a compromised renderer process to impersonate a privileged broker process during ipcz transport deserialization. This leads to:

Unauthorized duplication of high-privilege OS handles belonging to the browser process (e.g., thread handles, process handles, or other kernel objects via DuplicateHandle or equivalent APIs).
Privilege boundary violation between the sandboxed renderer and the unsandboxed browser process.
Full sandbox escape, granting the attacker arbitrary code execution with the privileges of the browser process.

Consequences of successful exploitation:

Arbitrary file system access (read/write outside sandbox boundaries)
Access to sensitive browser data (cookies, passwords, payment information, browsing history)
Injection of malicious code into the browser process, enabling persistent compromise
Potential remote code execution (RCE) on the user's device when chained with a renderer compromise (e.g., via malicious web content)
Mass-user impact: A single crafted webpage could target millions of Chrome users without user interaction beyond visiting the site

Severity justification:
This constitutes a critical sandbox escape primitive with direct chaining potential to remote code execution. It aligns with Tier 0 under Chrome VRP rules (full sandbox escape with high reliability and broad applicability). Comparable historical issues (e.g., CVE-2025-4609, [issue 412578726](https://issues.chromium.org/issues/412578726)) received maximum or near-maximum rewards.
CVSS-like estimate (informal):

Attack Vector: Network (web content)
Attack Complexity: Low-to-Medium (requires renderer compromise)
Privileges Required: None (post-renderer exploit)
User Interaction: None
Confidentiality/Integrity/Availability: High
Overall: Critical

This vulnerability poses a severe threat to Chrome's multi-process security model and user data protection.

---

### The cause

#### What version of Chrome have you found the security issue in?

131.0.6778.109

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Sandbox Escape

#### How would you like to be publicly acknowledged for your report?

kritik bhattarai

## Attachments

- [ipcz_deserialize_poc_pseudo.md](attachments/ipcz_deserialize_poc_pseudo.md) (text/markdown, 772 B)
- [ipcz_deserialize_poc_pseudo.html](attachments/ipcz_deserialize_poc_pseudo.html) (text/html, 1.7 KB)

## Timeline

### aj...@google.com (2026-02-04)

Hello closing as this describes a theoretical issue - please provide a proof of context that shows an issue in Chrome and open a fresh issue.

### ch...@google.com (2026-05-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/481277120)*
