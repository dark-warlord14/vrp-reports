# Security: UAF/double free with XSLT XPath expressions containing function calls in predicates

| Field | Value |
|-------|-------|
| **Issue ID** | [40087901](https://issues.chromium.org/issues/40087901) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>XML |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | we...@aevum.de |
| **Assignee** | sc...@chromium.org |
| **Created** | 2017-05-27 |
| **Bounty** | $3,500.00 |

## Description

**VULNERABILITY DETAILS**  

Certain function calls inside XPath predicates can lead to use-after-free and double-free errors when executed by libxml2's XPath engine via an XSLT transformation.

**VERSION**  

Chrome Version: 61.0.3114.0 dev  

Operating System: macOS 10.12.4

**REPRODUCTION CASE**  

See the attached files xpath-pred-func-uaf.xml and xpath-pred-func-uaf.xsl. If you open the XML file locally, make sure to run Chrome with --allow-file-access-from-files.

These files also reproduce the error reliably with the "xsltproc" command line tool on Linux and macOS.

FULL DETAILS  

When calling XPath functions, the XPath engine of libxml2 fails to verify correct stack usage. This isn't a problem in most cases where functions report an error to the XPath engine, because this usually leads to an early exit from the XPath evaluation. But if a function fails to signal an error and leaves the stack in an unexpected state, the evaluation continues. This can cause UAF errors triggered by code in xmlXPathCompOpEvalPositionalPredicate if the function call occurs within a certain sequence of XPath predicates (and maybe in other situations as well), eventually leading to a double free in multiple locations.

One such problematic function is "format-number" which leaves the XPath stack in an unexpected state without signaling an error if it receives an unknown decimal format name as third parameter.

FIXING THE ISSUE  

I have several larger, unpublished patches that clean up parts of libxml2's XPath engine which are related to this bug. Since more invasive changes to libxml2 can easily lead to regressions, I plan to review them more carefully before eventually committing. I'll attach a minimal patch that addresses the issue shortly.

DISCLOSURE  

I contribute to libxml2 occasionally. I haven't shared details about this issue with anyone yet. I didn't write any parts of the code that actually lead to the bug. This bug was found with libFuzzer and ASan in preparation of integrating libxslt with Google's OSS-Fuzz project.

## Attachments

- [xpath-pred-func-uaf.xml](attachments/xpath-pred-func-uaf.xml) (text/plain, 604 B)
- [xpath-pred-func-uaf.xsl](attachments/xpath-pred-func-uaf.xsl) (text/plain, 302 B)
- [xpath-pred-func-uaf.patch](attachments/xpath-pred-func-uaf.patch) (application/octet-stream, 795 B)

## Timeline

### we...@aevum.de (2017-05-27)

This issue will be tracked in GNOME Bugzilla here:

    https://bugzilla.gnome.org/show_bug.cgi?id=783160

Please mention if you want to be CC'd. Unless there are any objections, I'll add the details to the (protected) Bugzilla entry in a couple of days.

### el...@chromium.org (2017-05-28)

[Empty comment from Monorail migration]

[Monorail components: Blink>XML]

### ke...@chromium.org (2017-05-29)

Thanks for the report.

dominicc@, do you mind owning this?

### do...@chromium.org (2017-05-30)

Ken--No problem, thank you for routing it to me.

Nick--Thank you for the report. No objections to reporting it to the security bug upstream.

### do...@chromium.org (2017-05-30)

[Empty comment from Monorail migration]

### mb...@chromium.org (2017-05-30)

[Empty comment from Monorail migration]

### we...@aevum.de (2017-06-01)

Here's a minimal patch that should fix the problem.


### we...@aevum.de (2017-07-24)

There's a libxml2 release planned for August and the patch above will soon be committed upstream. The full details will be withheld for now.

### sh...@chromium.org (2017-07-27)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-09-14)

dominicc: According to https://crbug.com/chromium/727039#c8, this should already be fixed in upstream libxml2. Can you please check? Thanks.

### we...@aevum.de (2017-09-21)

This issue is now fixed upstream: https://git.gnome.org/browse/libxml2/commit/?id=0f3b843b3534784ef57a4f9b874238aa1fda5a73

### in...@chromium.org (2017-09-26)

Dominicc is no longer at Google.

Scott, can you please roll libxml2 forward with patch from c#12 ?

### sc...@chromium.org (2017-09-26)

I've never rolled it, but I will try to take a look some time.

Anyone else on Blink>XML want to care about libxml2/xslt by any chance?

### sc...@chromium.org (2017-10-03)

[Empty comment from Monorail migration]

### sc...@chromium.org (2017-10-03)

Roll CL at https://chromium-review.googlesource.com/c/chromium/src/+/698864.

### sc...@chromium.org (2017-10-03)

Looks like libxslt is in need of rolling too, I guess I'll try that while I'm hanging out having fun.

### sc...@chromium.org (2017-10-03)

Looks like configure.js doesn't work any more in libxslt (or at least not for me). Filed crbug.com/771324 for that.

### bu...@chromium.org (2017-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/75915266f693b8a7bc8c16ba66ddd91ce8b62495

commit 75915266f693b8a7bc8c16ba66ddd91ce8b62495
Author: Scott Graham <scottmg@chromium.org>
Date: Wed Oct 04 00:31:16 2017

Roll libxml to 0f3b843b3534784ef57a4f9b874238aa1fda5a73

Follows recipe in
https://cs.chromium.org/chromium/src/third_party/libxml/chromium/roll.py?l=25

Bug: 727039
Change-Id: Iad741672da34aa2abdd4e5566cb12c8840e0831d
Reviewed-on: https://chromium-review.googlesource.com/698864
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Scott Graham <scottmg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#506245}
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/README.chromium
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/linux/config.h
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/linux/include/libxml/xmlversion.h
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/linux/xml2-config
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/mac/config.h
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/mac/include/libxml/xmlversion.h
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/Makefile.am
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/Makefile.in
[add] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/README.zOS
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/SAX2.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/aclocal.m4
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/configure
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/configure.ac
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/elfgcchack.h
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/entities.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/genUnicode.py
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/include/Makefile.in
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/include/libxml/Makefile.in
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/libxml.h
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/libxml.spec.in
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/libxml2.spec
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/nanoftp.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/nanohttp.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/parser.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/parserInternals.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/testapi.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/threads.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/tree.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/uri.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/valid.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/xmlIO.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/xmlunicode.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/src/xpath.c
[modify] https://crrev.com/75915266f693b8a7bc8c16ba66ddd91ce8b62495/third_party/libxml/win32/include/libxml/xmlversion.h


### sc...@chromium.org (2017-10-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-05)

[Empty comment from Monorail migration]

### as...@chromium.org (2017-10-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-10-11)

Groovy!  The Chrome VRP panel decided to reward $3,500 for this report!

### aw...@chromium.org (2017-10-14)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-27)

This bug requires manual review: M63 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-10-27)

+awhalley@ (Security TPM) for M63 merge review

### aw...@chromium.org (2017-10-30)

No merge needed. 

mbarbella@ I'm surprised sheriffbot didn't request a merge to M62 after the commit, and that it requested a merge to M63 now - mind taking a look?  Cheers.

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/727039?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087901)*
