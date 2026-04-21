# Security: out-of-bounds write in tgsi_scan_shader

| Field | Value |
|-------|-------|
| **Issue ID** | [40064163](https://issues.chromium.org/issues/40064163) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-04-22 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

This is found by fuzz. After some debugging, it seems that an out-of-bounds write occurred in tgsi\_scan\_shader, which caused the value of ctx->dst\_bufs to be rewritten, and finally triggered a crash in strbuf\_fmt. I don’t know why the out-of-bounds write was not captured at the first time.

**VERSION**

virglrenderer-0.10.4

**REPRODUCTION CASE**

1. Compile tests with -fsanitize=address
2. ./virgl\_fuzzer

**CREDIT INFORMATION**

Reporter credit: rinngo

## Attachments

- [crash.log](attachments/crash.log) (text/plain, 3.1 KB)
- [test](attachments/test) (text/plain, 700 B)
- [crash.log](attachments/crash.log) (text/plain, 3.7 KB)
- [test](attachments/test) (text/plain, 584 B)

## Timeline

### [Deleted User] (2023-04-22)

[Empty comment from Monorail migration]

### za...@google.com (2023-04-24)

Containers out of bounds are not security vulnerability[1] since now they are protected by by libc++ hardening on all platforms crbug.com/1335422. Closing this bug as wont fix and tagging myself but feel free to reopen this one. 

[1] https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#indexing-a-container-out-of-bounds-hits-a-libcpp_verbose_abort_is-this-a-security-bug

### fi...@gmail.com (2023-04-24)

Are you kidding me? It is not a containers out of bounds. Please reopen it and forward it to chmiel.

### fi...@gmail.com (2023-04-24)

virglrenderer is a pure C project and has nothing to do with C++.

### fi...@gmail.com (2023-04-25)

This crash dump is more accurately. Stack buffer overflow is a security bug just like in other reports https://crbug.com/1379201. 

### za...@google.com (2023-04-25)

Thanks for reporting and sorry for the confusion as I thought it was a container out of bounds. I took a look again and I am reopening this bug.

chmiel@ can you please take a look at this virgl_fuzzer bug? Thanks. 

### za...@google.com (2023-04-25)

[Empty comment from Monorail migration]

### ad...@google.com (2023-04-25)

virgl appears to be ChromeOS specific so sending to ChromeOS security sheriffs.

### fi...@gmail.com (2023-04-26)

The cause of this bug is that `fulldecl->Range.Last` is under control, with no check.

src/gallium/auxiliary/tgsi/tgsi_scan.c:263

### ch...@google.com (2023-04-26)

Your report will be worked on in the Buganizer system ( link: https://issuetracker.google.com/issues/279731753 ). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

[Monorail blocking: b/279731753]

### [Deleted User] (2023-05-06)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-09)

It's fixed by https://gitlab.freedesktop.org/virgl/virglrenderer/-/merge_requests/1105 and will be backport in crrev/c/4511774

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-25)

Congratulations on another one, rinngo! The VRP Panel has decided to award you $7,000 for this report of a security bug in virgl renderer which runs in a sandboxed process on ChromeOS. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2023-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-15)

This issue was migrated from crbug.com/chromium/1436013?no_tracker_redirect=1

[Monorail blocking: b/279731753]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064163)*
