# Security: XML object's heap memory difference leaking or potential ASLR bypass in libXML

| Field | Value |
|-------|-------|
| **Issue ID** | [40060669](https://issues.chromium.org/issues/40060669) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>XML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | aq...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2022-08-24 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

XML object's heap memory difference leaking or potential ASLR bypass in libXML

**VERSION**  

Chrome Version: 104.0.5112.101  

Operating System: win10 21h2 19044.1889

**REPRODUCTION CASE**  

The vulnerability is in：  

void  

xsltGenerateIdFunction(xmlXPathParserContextPtr ctxt, int nargs)

<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/third_party/libxslt/src/libxslt/functions.c>

1. The val is calculated by  
   
   ctxt->context->node - &base\_address  
   
   or  
   
   nodelist->nodeTab[x] - &base\_address.

The base\_address is a global variable so it has a fixed address.

2. if we can find a way to make ctxt->context->node or nodelist->nodeTab[x] to be a fixed value, eg. null pointer (0), then we will get leaked base\_address
3. otherwise, we can calculate the gap between each heap object of different nodes, which can simplify the exploiting step

Fix advice:  

Do not use address gap as its fixed address, instead, use a hash, like crc(gap+salt)

Reproduce:

visit <http://127.0.0.1/cdcatalog_generateid.xml>, F12 to check

we can see x="idm[…x…]", this means the node has a gap to the static variable, with the difference -x

[1.png]

Author:Kaijie Xu @<https://twitter.com/kaijieguigui>

## Attachments

- 1.png (image/png, 39.5 KB)
- poc.zip (application/octet-stream, 781 B)

## Timeline

### [Deleted User] (2022-08-24)

[Empty comment from Monorail migration]

### es...@chromium.org (2022-08-26)

Thanks for the report. I'm redirecting to libxml owners and removing security labels since it's unclear how this could be exploited (assumes a separate bug e.g. null pointer deref).

[Monorail components: Blink>XML]

### va...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### va...@chromium.org (2022-08-29)

Thanks for filing the issue...!! 

Reporter@ - Could you please share the minimal reproducible test file/URL to reproduce the issue to test from our end and also requesting you to provide screencast for better understanding of the issue.



### aq...@gmail.com (2022-08-29)

Hi, the root cause of this problem is the generate-id() function uses address of a heap object minus address of a static variable. The attachment in #1 can be considered to be a minimal testcase. 

The security consideration is: the address of a static variable is fixed during the lifetime of a process, and can be used to calculate the loading address of the process. Which can weaken the protection of ASLR.

Also it can leak the memory layout of different XML objects. If you know one of these object (by other vulnerability), you will easily calculate address of all the objects in current page, which can make you write exploit easier.

### [Deleted User] (2022-08-29)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2022-08-29)

jarhar@ can you please triage this?

### ja...@chromium.org (2022-08-29)

Thanks for filing this issue! Unfortunately I'm not very familiar with the internals of libxml yet.
+wellnhofer@aevum.de do you have any thoughts about this?

### we...@aevum.de (2022-08-30)

This is a long-standing issue, also with regard to determinism and reproducible builds. Here's the relevant entry in the old bug tracker: https://bugzilla.gnome.org/show_bug.cgi?id=751621

I can have a look at it. Feel free to open an issue in the new bug tracker: https://gitlab.gnome.org/GNOME/libxslt/-/issues

### we...@aevum.de (2022-08-31)

Upstream fix: https://gitlab.gnome.org/GNOME/libxslt/-/commit/82f6cbf8ca61b1f9e00dc04aa3b15d563e7bbc6d and the previous three commits.

### aq...@gmail.com (2022-08-31)

Thank you very much for the quick fix, by the way, will there be any CVE applied for this issue?

### gi...@appspot.gserviceaccount.com (2022-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e5cea94b5b37065fff55221065ba4423a5213c08

commit e5cea94b5b37065fff55221065ba4423a5213c08
Author: Joey Arhar <jarhar@chromium.org>
Date: Fri Sep 02 23:49:21 2022

Roll libxslt from 19f97e1a to 5d8d8dd8

2022-09-01 wellnhofer@aevum.de cmake: Enable GCC compiler warnings
2022-09-01 wellnhofer@aevum.de Update GCC compiler warnings
2022-09-01 wellnhofer@aevum.de Fix various compiler warnings
2022-09-01 wellnhofer@aevum.de Fix compiler warnings in xsltGenerateIdFunction
2022-08-31 wellnhofer@aevum.de Clean up attributes in source doc
2022-08-31 wellnhofer@aevum.de Make generate-id() deterministic
2022-08-31 wellnhofer@aevum.de Store RVT ownership in 'compression' member
2022-08-31 wellnhofer@aevum.de Store key status of source nodes as bit flag
2022-08-31 wellnhofer@aevum.de Infrastructure to store extra data in source nodes
2022-08-31 wellnhofer@aevum.de Run CI tests with -fsanitize=integer
2022-08-30 wellnhofer@aevum.de Fix EXSLT functions tests when libxml2 is built --without-debug
2022-08-30 wellnhofer@aevum.de Make CI tests exit on failure
2022-08-30 wellnhofer@aevum.de Run Python 3 CI job with minimal configuration
2022-08-30 wellnhofer@aevum.de Disable Python bindings for debugger
2022-08-30 wellnhofer@aevum.de Don't declare disabled functions

Fixed: 1356211
Bug: 934413
Change-Id: Ie54ebe6f48f2302772908436adc043f6bd6e4f14
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3868147
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Auto-Submit: Joey Arhar <jarhar@chromium.org>
Commit-Queue: Stephen Chenney <schenney@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1042845}

[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libxslt/xsltlocale.c
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libxslt/pattern.c
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/configure.ac
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libxslt/xsltInternals.h
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libxslt/transform.c
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libexslt/crypto.c
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libexslt/functions.c
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libxslt/functions.c
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libxslt/attributes.c
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/CMakeLists.txt
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libxslt/xsltutils.h
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libxslt/keys.c
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libxslt/xsltutils.c
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libxslt/variables.c
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libxslt/numbers.c
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/src/libxslt/variables.h
[modify] https://crrev.com/e5cea94b5b37065fff55221065ba4423a5213c08/third_party/libxslt/README.chromium


### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### aq...@gmail.com (2022-09-17)

[Comment Deleted]

### am...@google.com (2022-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### aq...@gmail.com (2022-10-06)

Tip: the permission of this post is currently accessible to anyone, but it is not my operation that makes it so, please pay attention to this problem.

### am...@chromium.org (2022-10-07)

Hello, thank you for that, we are well aware and this was opened some time ago when this report was converted to type bug. Out of caution, I'll switch to bug-security, however the original bug in the upstream repo is also accessible. 
The VRP Panel has decided to award you $1,000 for this report. A member of our finance team will be in touch with you to arrange payment. Thank you for your efforts and reporting this issue to us! 

### [Deleted User] (2022-10-07)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-10-07)

[Empty comment from Monorail migration]

### aq...@gmail.com (2022-10-07)

[Comment Deleted]

### aq...@gmail.com (2022-10-07)

[Comment Deleted]

### am...@chromium.org (2022-10-07)

The Google VRP leaderboard is located here: https://bughunters.google.com/leaderboard
You would need to have a profile/account with the same email address you used to report this issue for that report to be associated with a bughunters profile. 

### aq...@gmail.com (2022-10-07)

[Comment Deleted]

### [Deleted User] (2022-10-07)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-08)

[Empty comment from Monorail migration]

### aq...@gmail.com (2022-11-12)

[Comment Deleted]

### aq...@gmail.com (2022-12-13)

Hi, Would like to ask if this vulnerability will be assigned a CVE number?

### am...@chromium.org (2022-12-13)

Hello, it looks like the fix rolled out in M107/Stable, for some reason our automation did not pull this in -- apologies for that. Updating accordingly and we'll update this with a CVE and in the release notes soon. 

### [Deleted User] (2023-01-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### aq...@gmail.com (2023-03-02)

Would like to ask if this vulnerability information will be published on https://chromereleases.googleblog.com/ ?

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2023-07-28)

This issue was migrated from crbug.com/chromium/1356211?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060669)*
