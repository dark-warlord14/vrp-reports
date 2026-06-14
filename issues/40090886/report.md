# Security: Bug in X509_VERIFY_PARAM_set1_host() with namelen 0

| Field | Value |
|-------|-------|
| **Issue ID** | [40090886](https://issues.chromium.org/issues/40090886) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network>SSL |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2018-8970 |
| **Reporter** | ti...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2018-03-22 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

BoringSSL's and LibreSSL's X509\_VERIFY\_PARAM\_set1\_host() function behaves differently than OpenSSL's implementation in a rather subtle and hard to detect way. As a consequence, X509\_VERIFY\_PARAM\_set1\_host(param, "hostname", 0) does NOT validate the hostname against SAN fields with LibreSSL and BoringSSL. Under OpenSSL it works perfectly fine and correctly validates hostname against SAN/CN.

The function signature is

int X509\_VERIFY\_PARAM\_set1\_host(X509\_VERIFY\_PARAM \*param,  

const char \*name, size\_t namelen);

OpenSSL allows namelen == 0, which is equivalent to namelen == strlen(name) for NULL terminated strings. However LibreSSL and BoringSSL consider namelen == 0 like name == NULL. Both libraries clear the value of X509\_VERIFY\_PARAM\_ID->host and return success (1). Both OpenSSL and LibreSSL 2.7.0 document contain "If name is NUL-terminated, namelen may be zero, otherwise namelen must be set to the length of name."

The bug is in line <https://boringssl.googlesource.com/boringssl/+/master/crypto/x509/x509_vpm.c#103>

I wrote this message to LibreSSL security team. Bob Beck replied that LibreSSL took the implementation from BoringSSL.

---

LibreSSL introduced X509\_VERIFY\_PARAM\_set1\_host() from OpenSSL 1.0.2.  

The function sets the expected DNS hostname for a connection. During  

cert chain validation, hostname is matched against subject alternative  

name fields.

The implementation in LibreSSL 2.7.0 is broken. I have attached an  

example program. With OpenSSL 1.1.0, the example fails with:

$ gcc client.c -lcrypto -lssl -o client && ./client Error connecting to  

server  

140315902109312:error:1416F086:SSL  

routines:tls\_process\_server\_certificate:certificate verify  

failed:ssl/statem/statem\_clnt.c:1230:  

X509 verify error: Hostname mismatch

With LibreSSL 2.7.0 the example program doesn't refuse the peer's  

certificate. It's a bug in LibreSSL's implementation of  

X509\_VERIFY\_PARAM\_set1\_host() and int\_x509\_param\_set\_hosts() because  

namelen == 0 is handled incorrectly. It's documented as "If name is  

NUL-terminated, namelen may be zero, otherwise namelen must be set to  

the length of name.". However the function stops early when namelen is  

0. As consequence of the bug, X509\_VERIFY\_PARAM\_ID's host value is never  

set and the hostname is never verified during the handshake.

## The attached patch fixes the issue for me. Please request a CVE for this bug.

**VERSION**  

All version of boringssl including git master.

**REPRODUCTION CASE**  

See attachmen

## Attachments

- [client.c](attachments/client.c) (text/plain, 2.4 KB)

## Timeline

### sl...@google.com (2018-03-22)

[Empty comment from Monorail migration]

[Monorail components: Internals>Network>SSL]

### bu...@chromium.org (2018-03-22)

The following revision refers to this bug:
  https://boringssl.googlesource.com/boringssl/+/e759a9cd84198613199259dbed401f4951747cff

commit e759a9cd84198613199259dbed401f4951747cff
Author: Adam Langley <alangley@gmail.com>
Date: Thu Mar 22 17:19:07 2018

Support the OpenSSL “pass zero for strlen” when setting X.509 hostnames.

BoringSSL does not generally support this quirk but, in this case, we
didn't make it a fatal error and it's instead a silent omission of
hostname checking. This doesn't affect Chrome but, in case something is
using BoringSSL and using this trick, this change makes it safe.

BUG=chromium:824799

Change-Id: If417817b997b9faa9963c09dfc95d06a5d445e0b
Reviewed-on: https://boringssl-review.googlesource.com/26724
Commit-Queue: Adam Langley <alangley@gmail.com>
Commit-Queue: David Benjamin <davidben@google.com>
Reviewed-by: David Benjamin <davidben@google.com>
CQ-Verified: CQ bot account: commit-bot@chromium.org <commit-bot@chromium.org>

[modify] https://crrev.com/e759a9cd84198613199259dbed401f4951747cff/crypto/x509/x509_vpm.c
[modify] https://crrev.com/e759a9cd84198613199259dbed401f4951747cff/crypto/x509/x509_test.cc


### ag...@chromium.org (2018-03-22)

Thank you for the report. We deliberately don't want to support magic behaviour in APIs like a length of zero not meaning zero. However, in this case a) we didn't make zero an error and b) using an empty string is dangerous.

While this doesn't affect Chrome, it's not the sort of robustness that we aim for. Had we made a zero length an error from the beginning, we could be sure that nothing was depending on this. However, since we screwed that up, the safest course, sadly, appears to be to support this magic in case people assume OpenSSL semantics.

Normally I would unrestrict this bug but you mentioned that Libre might be affected. I didn't know that they pulled from us but, in light of that, we'll let this bug follow the usual disclosure path and keep it limited for now.

While I suspect that, since this isn't an issue in Chrome, it wouldn't qualify under the VRP, I'll tag this anyway as I think it's a sound concern and not every security fix has to happen once the fire is burning.

### ti...@gmail.com (2018-03-22)

Thanks Adam,

Bob Beck from LibreSSL security team told me that they are going to release a new version of LibreSSL very soon. Only LibreSSL 2.7.0 is affected. LibreSSL 2.6 and earlier didn't have the X509_VERIFY_PARAM_set1_host() API. Bob also told me that LibreSSL 2.7.0 qualifies as beta release. The latest stable is 2.6.4.

The feature was added after I complained (https://github.com/libressl-portable/portable/issues/381) that the lack of API is breaking new SSL module feature in upcoming Python 3.7.0 release. After all Python core devs agreed to break compatibility with OpenSSL 0.9.8 and 1.0.1, I replaced Python's custom hostname matching code with X509_VERIFY_PARAM_set1_host(). I got tired of all the security bugs in our code.

Anyway, I'll drop a note on this ticket as soon as LibreSSL 2.7.1 is out.

### ti...@gmail.com (2018-03-24)

LibreSSL 2.7.1 is out. You can lift the restriction.

### sh...@chromium.org (2018-03-24)

[Empty comment from Monorail migration]

### ti...@gmail.com (2018-03-25)

FYI, MITRE has assigned CVE-2018-8970 for the LibreSSL bug.

I haven't requested a CVE # for BoringSSL. I leave it to your discretion. By the way, the issue was noticed before. Bug report https://bugs.chromium.org/p/boringssl/issues/detail?id=30 not only complaints about lack of documentation but also about different behavior with namelen=0. Déjà vu!

### ti...@gmail.com (2018-03-26)

Yesterday I recalled, why I used X509_VERIFY_PARAM_set1_host(param, hostname, 0) in CPython rather than X509_VERIFY_PARAM_set1_host(param, hostname, strlen(hostname)). OpenSSL's wiki entry for hostname validation https://wiki.openssl.org/index.php/Hostname_validation suggests 0 as namelen parameter.

The page is also the first Google hit for search phrases like "openssl check hostname" and "openssl validate hostname". I guess more projects are using 0 instead of strlen(hostname). A quick search revealed that Mongo DB's C driver has namelen=0, too.

### ag...@chromium.org (2018-03-26)

> By the way, the issue was noticed before.

Sigh. I think we were estimating that Chromium's certificate verifier would be ready much faster at that point in time.

> OpenSSL's wiki entry for hostname validation https://wiki.openssl.org/index.php/Hostname_validation suggests 0 as namelen parameter.

And suggests not checking any return value :(

Thanks. We'll seek to fix that too.

### ag...@chromium.org (2018-03-30)

To follow-up here:

https://boringssl.googlesource.com/boringssl/+/1902d818ac4fef9497dfe5d0ce6f2c99f585bdff has been landed which tightens a number of things, including making passing zero as a length an error, and a case that causes all future validations to fail in case (as was documented in the wiki) the result is ignored.

That change does other things too, see the description.

The [wiki page](https://wiki.openssl.org/index.php/Hostname_validation) has been updated to a) check the return value and b) not use the zero-length trick.

### ag...@chromium.org (2018-04-04)

Derestricting since this doesn't affect Chromium and LibreSSL have done a release.

### ag...@chromium.org (2018-04-04)

(Trying again to derestrict.)

### aw...@chromium.org (2018-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-10)

Hi tiran79@gmail.com - the Chrome VRP panel decided to award $500 for this report. A member of our finance team will be in touch to arrange for payment. Cheers!

### aw...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-03)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/824799?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090886)*
