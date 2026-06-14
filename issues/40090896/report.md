# Security: Bug in BoringSSL P-256 point_add

| Field | Value |
|-------|-------|
| **Issue ID** | [40090896](https://issues.chromium.org/issues/40090896) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network>SSL |
| **Reporter** | da...@xcx.cc |
| **Assignee** | da...@chromium.org |
| **Created** | 2018-03-23 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**VULNERABILITY DETAILS**

Received by email from Daniel Hirche [daniel@xcx.cc](mailto:daniel@xcx.cc):  

"""  

Hi David,

I have a question regarding the branch checking for equal inputs in  

<https://github.com/google/boringssl/blob/master/third_party/fiat/p256.c#L1121>

This should be unreachable, however, if it hits, it would just set the  

\*temporary\* coordinates (x\_out,y\_out,z\_out) to 2\*(X1:Y1:Z1) and then  

return without any real result.

I'm not sure if this was supposed to fall through or if it should set  

set the actual output (X3:Y3:Z3) = 2\*(X1:Y1:Z1) and then return?

(I'm guessing the latter if I understand  

<https://github.com/mit-plv/fiat-crypto/blob/79f8b5f39ed609339f0233098dee1a3c4e6b3080/src/Curves/Weierstrass/Jacobian.v#L169>  

correctly).  

"""

Daniel is right and there is indeed a bug in that code. Putting together fix now. AGL and I don't believe this one is exploitable, but it's the sort of rare bug in the corner of crypto code that we're really really happy to folks look at for us. Does this stuff fall under VRP?

**VERSION**  

Chrome Version: 65+  

Operating System: all

## Timeline

### el...@chromium.org (2018-03-23)

[Empty comment from Monorail migration]

### da...@chromium.org (2018-03-23)

Reasoning for why it's probably not exploitable:

The relevant multiplications in ECC are:
- keygen (randomly-generated scalar times G)
- ECDH (randomly-generated scalar times attacker-supplied P)
- ECDSA sign (randomly-generated scalar times G)
- ECDSA verify (two-point multiplication, goal would be to forge a signature)

For single-point multiplication, this case should not occur. Even if it did, P-256 is a prime order curve, so whether it comes up is purely a function of the scalar, which is not under attacker control in ECDH, ECDSA signing, and keygen, so those operations aren't really a concern.

For two-point multiplication, this case does indeed come up, but it results in a relation between G and P, giving the discrete log, so forging an ECDSA signature with this is as hard as finding the private key anyway.

The hole in this argument: the relation between G and P might be trivial, if the case can come up with a single-point with ECDSA verify's windowing. AGL and I can't find a way to do anything useful with this though. We don't think it's possible to delete all bits in one of the scalars to make it zero, which would be the obvious vector.

### bu...@chromium.org (2018-03-23)

The following revision refers to this bug:
  https://boringssl.googlesource.com/boringssl/+/5fca61391822252baf3dc37529ba02f6d7611acf

commit 5fca61391822252baf3dc37529ba02f6d7611acf
Author: David Benjamin <davidben@google.com>
Date: Fri Mar 23 21:12:29 2018

Fix typo in point_add.

Rather than writing the answer into the output, it wrote it into some
awkwardly-named temporaries. Thanks to Daniel Hirche for reporting this
issue!

Bug: chromium:825273
Change-Id: I5def4be045cd1925453c9873218e5449bf25e3f5
Reviewed-on: https://boringssl-review.googlesource.com/26785
Reviewed-by: Adam Langley <agl@google.com>
Commit-Queue: David Benjamin <davidben@google.com>
CQ-Verified: CQ bot account: commit-bot@chromium.org <commit-bot@chromium.org>

[modify] https://crrev.com/5fca61391822252baf3dc37529ba02f6d7611acf/crypto/fipsmodule/ec/ec_test.cc
[modify] https://crrev.com/5fca61391822252baf3dc37529ba02f6d7611acf/third_party/fiat/p256.c
[modify] https://crrev.com/5fca61391822252baf3dc37529ba02f6d7611acf/crypto/fipsmodule/ec/internal.h


### da...@chromium.org (2018-03-23)

I'll request a merge for M66 next week, once it's been on canary for a bit.

### sh...@chromium.org (2018-03-24)

[Empty comment from Monorail migration]

### da...@chromium.org (2018-03-27)

Requesting merge for M66. It's been on canary for a few days now.

### sh...@chromium.org (2018-03-27)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2018-03-27)

Please add affected OSs.

### da...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-03-29)

Approving merge to M66. Branch:3359

### da...@chromium.org (2018-03-29)

Thanks! (It's a DEPS change, so I'll need you to stamp https://chrome-internal-review.googlesource.com/c/chrome/tools/buildspec/+/597800 for me.)

### bu...@chromium.org (2018-04-02)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/tools/buildspec/+/e8e2576fdfe5bba8534cd5eafc5b7541b4ac2c82

commit e8e2576fdfe5bba8534cd5eafc5b7541b4ac2c82
Author: David Benjamin <davidben@google.com>
Date: Mon Apr 02 16:06:06 2018


### da...@chromium.org (2018-04-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2018-04-02)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-04-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-10)

Hi daniel@xcx.cc - the Chrome VRP panel decided to award $500 for this report. A member of our finance team will be in touch to arrange for payment. Many thanks!

### aw...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/825273?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090896)*
