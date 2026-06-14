# Security: Chrome accepts a certificate whose signature algorithms identifiers are different without any warning

| Field | Value |
|-------|-------|
| **Issue ID** | [40086759](https://issues.chromium.org/issues/40086759) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Certificate |
| **Reporter** | ch...@stu.xidian.edu.cn |
| **Assignee** | er...@chromium.org |
| **Created** | 2017-02-10 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

As for a certificate, when the declared signature algorithm identifier (e.g. Sha1WithRSAEncryption) is different from the actually used signature algorightm identifier (e.g. Sha256WithRSAEncryption), the certificate should be rejected. However, Chrome accepts such a certificate without any warning. This is a security bug.

**VERSION**  

Chrome Version: [54.0.2840.59] + [stable]  

Operating System: [Ubuntu v1604-LTS x64]

**REPRODUCTION CASE**

1. To open the "setting" menu of Chrome.
2. To click "show advanced settings".
3. To click "HTTPS/SSL:Manage certificate ..."
4. To click "Authorities" tab and to click "import". To select "basicCA.pem" which is attached to this report and to select "Trust this certificate for identifying websites".
5. To click "Your Certificates" tab and to click "import". To select "1.p12" which is also attached to this report and input the password "123654".
6. Chrome accepts "1.p12" without any warning and Chrome shows that "This certificate has been verified for the following useages: ...".
7. To view the imported "1.p12" and you will find that in the "Details" that the declared "Certificate Signature Algorithm" is "PKCS #1 SHA-1 With RSA Encryption" while the actually used "Certificate Signature Algorithm" is "PKCS #1 SHA-256 With RSA Encryption", which are different.

## Attachments

- [basicCA.pem](attachments/basicCA.pem) (application/octet-stream, 1.2 KB)
- [1.p12](attachments/1.p12) (application/octet-stream, 2.5 KB)
- [basicCA.p12](attachments/basicCA.p12) (application/octet-stream, 2.4 KB)
- [1.p12](attachments/1_53312944.p12) (application/octet-stream, 2.5 KB)
- [mismatched_sha1_sha256.pem](attachments/mismatched_sha1_sha256.pem) (application/octet-stream, 10.0 KB)

## Timeline

### ch...@stu.xidian.edu.cn (2017-02-10)

The same bug appears in Windows 7 reported as follows:

VERSION
Chrome Version: [53.0.2785.116 m (64-bit)] + [stable]
Operating System: [Windows 7 v6.1 build 7601, service pack 1]

REPRODUCTION CASE
1. To open the "setting" menu of Chrome.

2. To click "show advanced settings ...".

3. To click "HTTPS/SSL:Manage certificate ..."

4. To click the tab "Trusted Root Certification Authorities" and to click the button "Import...". To select "Personal Information Exchange (*.pfx;*.p12)" right to the "File name" in the "Open" window and to select "basicCA.p12" which is attached to this comment. To click "Open" and "Next" and to input the password "123654". To click: "Next", "Next", "Finish", and "Yes". It will be notified "The import was successful".

5. To click the tab "Personal" and to click the button "Import...". To select "Personal Information Exchange (*.pfx;*.p12)" right to the "File name" in the "Open" window and to select "1.p12" which is also attached to this comment. To click "Open" and "Next" and input the password "123654". To click: "Next", "Next", "Finish", and "Yes". It will be notified "The import was successful".

6. Chrome accepts "1.p12" without any warning. Double clicks on the imported certificate will show the information "This certificate is intended for the following purpose(s):...".

7. The tab "Details" of the certificate shows that: "Signature algorithm" is "sha1RSA" and "Signature hash algorithm" is "sha1". However the actually used signature and hash algorithms are "sha256RSA" and "sha256", respectively.

### el...@chromium.org (2017-02-10)

In Windows at least, certificate import is a mechanism of the Operating System, not the browser.

It's not clear to me that this is a security bug.

[Monorail components: Internals>Network>Certificate]

### pa...@chromium.org (2017-02-10)

Let's pass it to the experts and find out.

### rs...@chromium.org (2017-02-10)

Eric: I believe you did the scan of publicly trusted certs and remember the issues here?

The question at hand is the enforcement of the MUST in https://tools.ietf.org/html/rfc5280#section-5.1.1.2 

However, I'm entirely uncertain how, as a practical matter (e.g. given the WebPKI) this represents a security issue if the client doesn't enforce it. I can understand why it's ideal, but since the most it facilitates is a signature transplatation (or some hinky Diffie-Hellman implied params or DSA hijinks that X.509v3 supports but which we do not), and because such signatures must come from a CA that either Chrome trusts or that the user installed, I don't think it represents a security issue.

### er...@chromium.org (2017-02-10)

My analysis was for

signatureAlgorithm (https://tools.ietf.org/html/rfc5280#section-4.1.1.2)
  vs
Signature (https://tools.ietf.org/html/rfc5280#section-4.1.2.3)

And NOT the signatureAlgorihtm (https://tools.ietf.org/html/rfc5280#section-5.1.1.2) which was linked to in https://crbug.com/chromium/690821#c4.

My testing methodology involved looking at the certificates in the CT database at the time (December 2015).

The results then showed that only 5 target certificates had a mismatch between the signature algorithm identifiers. Specifically in these cases the mistake was listing sha1WithRSAEncryption in one place, but sha256WithRSAEncryption in the other.

A secondary problem, that I could not confirm via CT database, but which was described in other threads (I need to find the source material...) was an indication of certificates which use the same conceptual algorithm identifier, but with alternate encodings. In particular using an (incorrect) encoding for SHA1 but which is allowed elsewhere.

To address this concern, for the builtin verifier we settled on the following interpretation of "MUST contain the same algorithm identifier":

https://cs.chromium.org/chromium/src/net/cert/internal/verify_certificate_chain.cc?l=150

### er...@chromium.org (2017-02-10)

Summarizing the repro case:

  * TBSCertificate.signature = sha1WithRSAEncryption
  * Certificate.signatureAlgorithm = sha256WithRSAEncryption
  * The actual signature bytes are for sha256WithRSAEncryption (Certificate.signatureAlgorithm()

I agree that the described behavior is incorrect and non-compliant with RFC 5280.

Certificate.signatureAlgorithm is attacker controlled and not part of the signed payload. The verifier shouldn't be both skipping the equality check and using the Certificate version of the algorithm.

As far as whether this is exploitable, that depends on whether ALL the dependent code (Chromium and platform verifier) is diligently using Certificate.signatureAlgorithm throughout. If it is at times testing things via TBSCertificate.signature we may have problems.

For instance my fear would be if any code is deciding whether signature algorithms are weak or strong by looking at TBSCertificate.signature. If that were the case, one could construct a Certificate with a correct but weak signature (say MD5), but then policy checks prohibiting weak signatures would pass because they are looking at TBSCertificate.signature in the forged certificate data.

Assuming this is not possible (which is fragile), then I agree with Ryan's assessment that being able to control the signature algorithm probably isn't a source of vulnerability today. (Since we disallow weak signature algorithms).

### da...@chromium.org (2017-02-10)

Apart from the kinds of self inconsistency scenarios eroman mentioned (though ideally the policy code would be close to the code which picks algorithms to begin with), yeah I don't think the mismatch is a problem, in terms of signature forgery. It's weird that certificates and CRLs repeat their signature algorithm in the TBS part to begin with. TLS does not do this. OCSP responses don't do this either.

Though given certificates sadly do have this duplication, it'd be good to enforce when verifying to prevent the scenarios eroman@ mentions. Alas X.509 is full of mistakes. This is one of them. :-/

Note that crawling CT logs isn't actually going to tell us definitively about mismatches or misencodings of the outer part because they're not signed. A log needs to reject certs that differ only in the unsigned envelope to avoid an abuse problem. (That or the log needs to have a perfectly strict parser.)

### ch...@stu.xidian.edu.cn (2017-02-11)

I agree the the following comment by eroman@chromium.org:

"For instance my fear would be if any code is deciding whether signature algorithms are weak or strong by looking at TBSCertificate.signature. If that were the case, one could construct a Certificate with a correct but weak signature (say MD5), but then policy checks prohibiting weak signatures would pass because they are looking at TBSCertificate.signature in the forged certificate data."

### ji...@chromium.org (2017-02-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### rs...@chromium.org (2017-02-21)

Just making sure I've properly parsed https://crbug.com/chromium/690821#c6/https://crbug.com/chromium/690821#c7: It sounds like we're in agreement this is not a security issue, and can move this out of the security queue.

If so, we should remove this from the security queue and set priority appropriately. Eric, can you double-check and confirm?

### ch...@stu.xidian.edu.cn (2017-02-22)

Weak signature algorithms such as MD5+RSA 256/512 are prohibited due to security reasons.  Now even RSA 1024 is not good enough because it can be cracked within a bearably long time if crackers have powerful computers.

The issue we reported is that the certificate validation does not check the consistency of Certificate.signatureAlgorithm and TBSCertificate.signature. If a CA issues a certificate whose TBSCertificate.signature is "sha256WithRSAEncryption" but Certificate.signatureAlgorithm is "MD5+RSA 256/512/1024", this certificate can be cracked and then forged once it is captured by crackers. Such certificates cannot guarantee the security of communications on the Internet and may lead to security issues.  Therefore, it is necessary to fix this issue for security reasons.


### rs...@chromium.org (2017-02-22)

I appreciate your feedback, but it's unclear whether you're asserting a theoretical attack or a practical attack.

1) If a CA issues such a certificate, the CA has already violated the prime requirement of CA compliance (Baseline Requirements). As such, a CA is already at risk of distrusting. Conversely, it requires convincing a CA to issue such a certificate for this attack to be relevant, of which the ability and odds of doing so are quite low.
2) The key size is reflected in the subjectPublicKeyInfo, not in the signatureAlgorithm or certificate - thus I believe there's just confusion about this
3) Your sole attack relies on relying on the TBSCertificate.signature, rather than Certificate.signatureAlgorithm, however:
  - on macOS, we use certificate.signatureAlgorithm ( https://cs.chromium.org/chromium/src/net/cert/x509_certificate_mac.cc?rcl=de9c9d9f85b2931f1c5b813a49e673fac216d916&l=522 )
  - On Windows, we use certificate.signatureAlgorithm ( https://cs.chromium.org/chromium/src/net/cert/x509_certificate_win.cc?rcl=de9c9d9f85b2931f1c5b813a49e673fac216d916&l=425 )
  - On iOS, we use certificate.signatureAlgorithm ( https://cs.chromium.org/chromium/src/net/cert/x509_certificate_ios.cc?rcl=de9c9d9f85b2931f1c5b813a49e673fac216d916&l=363 )
  - On Android, we use certificate.signatureAlgorithm ( https://cs.chromium.org/chromium/src/net/cert/x509_certificate_openssl.cc?rcl=de9c9d9f85b2931f1c5b813a49e673fac216d916&l=382 )

So even without checking, I don't believe there's any vulnerability here. Have you tried what you're describing and believe it's otherwise?

The only place where we don't enforce consistency right now is on Linux, which is taking it from TBSCertificate.signature rather than Certificate.signatureAlgorithm (c.f.   https://cs.chromium.org/chromium/src/net/cert/x509_certificate_nss.cc?rcl=de9c9d9f85b2931f1c5b813a49e673fac216d916&l=243 and https://dxr.mozilla.org/mozilla-central/source/security/nss/lib/certdb/certdb.c#73 ), but there, the mitigation for #1 applies - no 'natural' certificate abuses this, and if you can compel a CA to sign whatever you want, then this is irrelevant because the CA will sign whatever you want.

### ch...@stu.xidian.edu.cn (2017-02-22)

Thank you for your comment.

In our previous comment, the TBSCertificate.signature should be the signature algorithm identifier in tbsCertificate and Certificate.signatureAlgorithm should be the actually used signature algorithm identifier.  The key size we mentioned refers to the tht of RSA which is used to sign a certificate. 



### sh...@chromium.org (2017-02-25)

eroman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### er...@chromium.org (2017-02-27)

I'll work on some tests for this today and then post an update.

### er...@chromium.org (2017-02-28)

I have completed my testing (on Linux)

This is definitely a security bug -- one can construct certificates signed using weak signature algorithms, and get Chrome to accept them as non-weak. Severity should be raised.

It appears that NSS checks Certificate.signatureAlgorithm when doing signature checks, whereas Chrome checks TBSCertificate.algorithm when doing policy checks, so the policy checking can be confused.

Specifically I was able to construct a SHA1 signed certificate, and have Chrome accept it as if it were a SHA256 signed one, using this combination:

  Certificate.signatureAlgorithm: Sha1
  Certificate.signatureValue:     Valid Sha1 signature of the forged TBSCertificate
  TBSCertificate.algorithm:       Sha256

I haven't tried to build an MD5 certificate at this time, but the same technique should be applicable.

The results of testing the following 8 permutations appear below (labeled A.1, A.2, ...):

  Certificate.signatureAlgorithm: (Sha1 | Sha256)
  Certificate.signatureValue:     (Sha1 | Sha256)
  TBSCertificate.algorithm:       (Sha1 | Sha256)

============= (A.1) ============= 

  Certificate.signatureAlgorithm: Sha1
  Certificate.signatureValue:     Sha1
  TBSCertificate.algorithm:       Sha256

RESULT: Considers the certificate (with a SHA1 signature) as valid and not using a weak signature.

CONCLUSION: BAD. This is an exploitable bug.

============= (A.2) ============= 

  Certificate.signatureAlgorithm: Sha256
  Certificate.signatureValue:     Sha256
  TBSCertificate.algorithm:       Sha1

RESULT: Verification at the NSS level, however Chrome treats this as a SHA1 certificate (ERR_CERT_WEAK_SIGNATURE_ALGORITHM)

CONCLUSION: Probably fine. This is a misissued certificate, and rejecting this isn't dangerous (although it is confused).

============= (B.1) ============= 

  Certificate.signatureAlgorithm: Sha1
  Certificate.signatureValue:     Sha256
  TBSCertificate.algorithm:       Sha1

RESULT: Verification fails (SEC_ERROR_BAD_SIGNATURE)
CONCLUSION: Fine.

============= (B.2) ============= 

  Certificate.signatureAlgorithm: Sha256
  Certificate.signatureValue:     Sha1
  TBSCertificate.algorithm:       Sha256

RESULT: Verification fails (SEC_ERROR_BAD_SIGNATURE)
CONCLUSION: Fine.

============= (C.1) =============

  Certificate.signatureAlgorithm: Sha1
  Certificate.signatureValue:     Sha256
  TBSCertificate.algorithm:       Sha256

RESULT: Verification fails (SEC_ERROR_BAD_SIGNATURE)
CONCLUSION: Fine.

============= (C.2) ============= 

  Certificate.signatureAlgorithm: Sha256
  Certificate.signatureValue:     Sha1
  TBSCertificate.algorithm:       Sha1

RESULT: Verification fails (SEC_ERROR_BAD_SIGNATURE)
CONCLUSION: Fine.

============= (D.1) ============= 

  Certificate.signatureAlgorithm: Sha1
  Certificate.signatureValue:     Sha1
  TBSCertificate.algorithm:       Sha1

RESULT: Verification fails, as Chrome considers SHA1 weak (ERR_CERT_WEAK_SIGNATURE_ALGORITHM)
CONCLUSION: Correct. This is a control test, as there is no actual mismatch of signature algorithms

============= (D.2) ============= 

  Certificate.signatureAlgorithm: Sha256
  Certificate.signatureValue:     Sha256
  TBSCertificate.algorithm:       Sha256

RESULT: Verification succeeds
CONCLUSION: Correct. This is a control test, as there is no actual mismatch of signature algorithms.



I will follow-up with a fix and verification for other platforms (I believe this only affects the NSS based verification).

### da...@chromium.org (2017-02-28)

Ugh. Nice catch!

### rs...@chromium.org (2017-02-28)

Right, that was the case called out in https://crbug.com/chromium/690821#c14. The mitigating factor here is that the CA must misissue it in the first place.

Our SHA-1 enforcement (client side) is part of a defense in depth approach to what we've taken on the policy side, so I'm not sure if the priority here requires raising, given the mitigating factors, but yeah, it should be an easy fix. Eric, are you comfortable driving that fix?

It's just changing https://cs.chromium.org/chromium/src/net/cert/x509_certificate_nss.cc?rcl=4e0d26ac80d31bbfa773948f61122c635c5487f4&l=244 to use cert->signatureWrap->signatureAlgorithm

### er...@chromium.org (2017-02-28)

If we are modeling SHA1 as weak, then this isn't just a concern over mis-issued certificate, but a maliciously crafted one.

And unless we are blacklisting MD5 as a supported algorithm at the NSS layer, it should be possible to do the same thing using even weaker signature algorithms; would you agree that is bad? (I'll verify that next).

> Eric, are you comfortable driving that fix?

Yep, on it.

### rs...@chromium.org (2017-02-28)

No. None of this undermines the signature verification to a trusted root, it only affects the internal Chrome policies.

That is, put differently, we know these certificates chain to trusted anchors, and thereby we know the policies in place to prevent CAs from issuing such certificates.

It *is* a risk if a CA is compromised or compelled to misissue - but under both of those threats, this does not prevent other, more malicious, activities.

So while I agree it's a degree that our security policy says we don't want to accept, our mitigating factors include the business relationships and policies that prevent such malicious certificates from being issued. This is just defense in depth.

### rs...@chromium.org (2017-02-28)

OK, so talked through with Eric a bit more: I was approaching this from a risk of collision, whereas Eric was concerned about second-preimage.

The attack is concerning if you can use a pre-existing signature (generated before the 'ban' on whatever signature algorithm), and use that to "sign" a certificate that presents itself as an acceptable algorithm within the TBSCertificate. The two mitigating factors for the feasibility of that attack are:
  1: The underlying hash algorithm still needs to be accepted by the cryptographic library in play. SHA-1 is still accepted on all our platforms, MD5 on a small number, and anything 'worse' than MD5 is not.
  2: The underlying hash algorithm needs to be vulnerable to a second-preimage.

These two mitigating factors for the use of existing certificates means it's unlikely to be exciting.

For a collision resistance, you need to be able to construct an 'evil' input and a 'good' input and obtain a fresh signature using a hash algorithm susceptible to a collision attack. The same mitigations exist as above, except s/second-preimage/collision/.

For collision attacks, because we've addressed via policy the use of the private key, it's a defense in depth. For second-preimage, we should have all of those algorithms hard disabled at the underlying layer.

There's other mitigations at play here as well - for example, an RSA signature is less vulnerable in this scenario, because the output of the EMSA-PKCS1-v1_5-ENCODE function (see RFC 3447) further binds the signature algorithm inside the signature itself.

I think the security analysis under both scenarios remain the same - this is low risk (e.g. impractical) for any CA-issued certificate, and would primarily affect the Enterprise issuance scenario, where the Enterprise is still actively issuing SHA-1 certificates, but relying on Chrome policy to block this. I'm not sure how we assess that threat scenario, but it does mean the impact is significantly smaller as a portion of overall users.

We have a quick fix though so that's good :)

### bu...@chromium.org (2017-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a77953fe670968fe6728796b77cedf48f0954d78

commit a77953fe670968fe6728796b77cedf48f0954d78
Author: eroman <eroman@chromium.org>
Date: Thu Mar 09 06:45:13 2017

Check TBSCertificate.algorithm and Certificate.signatureAlgorithm for
consistency when verifying certificates.

The underlying platform verifiers don't do this, which can lead to
confusion when trying to enforce policy for SHA1 on the verified chain.

* If the two signature algorithms don't match will fail with
  ERR_INVALID_CERT.

* If the chain contains a signature algorithm that we don't know how to
  parse, will also fail with ERR_INVALID_CERT

BUG=690821

Review-Url: https://codereview.chromium.org/2731603002
Cr-Commit-Position: refs/heads/master@{#455682}

[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/asn1_util.cc
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/asn1_util.h
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/cert_verify_proc.cc
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/cert_verify_proc_mac.cc
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/cert_verify_proc_unittest.cc
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/internal/signature_algorithm.cc
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/internal/signature_algorithm.h
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/internal/verify_certificate_chain.cc
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/x509_certificate.h
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/x509_certificate_ios.cc
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/x509_certificate_mac.cc
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/x509_certificate_nss.cc
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/x509_certificate_openssl.cc
[modify] https://crrev.com/a77953fe670968fe6728796b77cedf48f0954d78/net/cert/x509_certificate_win.cc


### er...@chromium.org (2017-03-09)

[Empty comment from Monorail migration]

### rs...@chromium.org (2017-03-09)

Eric: You marked this fixed, but this just landed in M-59. I think we want to consider merging to 58, possibly 57, correct?

### er...@chromium.org (2017-03-09)

Correct -- "fixed" refers to the patch landing in the source tree, meaning it will be fixed in M59.

Whether we choose merge to 57/58 depends on your severity assessment (which in https://crbug.com/chromium/690821#c23 sounded like low).

There is some compatibility risk from choosing to merge this change (should there be cases where our new signature algorithm parsing is stricter).

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

Sounds like we should at least take this in M58, I think it'll still make the first beta.

### sh...@chromium.org (2017-03-13)

Your change meets the bar and is auto-approved for M58. Please go ahead and merge the CL to branch 3029 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), bhthompson@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-03-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057

commit 37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057
Author: Eric Roman <eroman@chromium.org>
Date: Mon Mar 13 21:22:48 2017

Add support for MD2, MD4, and MD5 to SignatureAlgorithm.

(At a parsing level it is useful to recognize these for error handling,
even if in practice they aren't used when verifying signatures.)

Review-Url: https://codereview.chromium.org/2728953003
Cr-Commit-Position: refs/heads/master@{#455350}
(cherry picked from commit 37e84a0d658536248f4a4372551c36db2e614c1f)

BUG=690821

Review-Url: https://codereview.chromium.org/2750703002 .
Cr-Commit-Position: refs/branch-heads/3029@{#165}
Cr-Branched-From: 939b32ee5ba05c396eef3fd992822fcca9a2e262-refs/heads/master@{#454471}

[modify] https://crrev.com/37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057/net/cert/internal/parse_ocsp.cc
[modify] https://crrev.com/37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057/net/cert/internal/signature_algorithm.cc
[modify] https://crrev.com/37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057/net/cert/internal/signature_algorithm.h
[modify] https://crrev.com/37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057/net/cert/internal/signature_algorithm_unittest.cc
[modify] https://crrev.com/37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057/net/cert/internal/signature_policy.cc
[modify] https://crrev.com/37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057/net/cert/internal/verify_signed_data.cc
[modify] https://crrev.com/37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057/net/cert/x509_util_openssl.cc
[modify] https://crrev.com/37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057/net/data/verify_certificate_chain_unittest/generate-intermediate-signed-with-md5.py
[modify] https://crrev.com/37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057/net/data/verify_certificate_chain_unittest/generate-target-signed-with-md5.py
[modify] https://crrev.com/37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057/net/data/verify_certificate_chain_unittest/intermediate-signed-with-md5.pem
[modify] https://crrev.com/37ff2437dc0a3c4c0e6cf0976b1967bca2d5f057/net/data/verify_certificate_chain_unittest/target-signed-with-md5.pem


### bu...@chromium.org (2017-03-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8f0392d571b728f4a7d02067c129b1a44f3e19c2

commit 8f0392d571b728f4a7d02067c129b1a44f3e19c2
Author: Eric Roman <eroman@chromium.org>
Date: Mon Mar 13 21:34:32 2017

Check TBSCertificate.algorithm and Certificate.signatureAlgorithm for consistency when verifying certificates.

The underlying platform verifiers don't do this, which can lead to
confusion when trying to enforce policy for SHA1 on the verified chain.

* If the two signature algorithms don't match will fail with
  ERR_INVALID_CERT.

* If the chain contains a signature algorithm that we don't know how to
  parse, will also fail with ERR_INVALID_CERT

BUG=690821

Review-Url: https://codereview.chromium.org/2731603002
Cr-Commit-Position: refs/heads/master@{#455682}
(cherry picked from commit a77953fe670968fe6728796b77cedf48f0954d78)

Review-Url: https://codereview.chromium.org/2750723002 .
Cr-Commit-Position: refs/branch-heads/3029@{#166}
Cr-Branched-From: 939b32ee5ba05c396eef3fd992822fcca9a2e262-refs/heads/master@{#454471}

[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/asn1_util.cc
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/asn1_util.h
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/cert_verify_proc.cc
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/cert_verify_proc_mac.cc
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/cert_verify_proc_unittest.cc
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/internal/signature_algorithm.cc
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/internal/signature_algorithm.h
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/internal/verify_certificate_chain.cc
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/x509_certificate.h
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/x509_certificate_ios.cc
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/x509_certificate_mac.cc
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/x509_certificate_nss.cc
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/x509_certificate_openssl.cc
[modify] https://crrev.com/8f0392d571b728f4a7d02067c129b1a44f3e19c2/net/cert/x509_certificate_win.cc


### aw...@google.com (2017-03-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-15)

Thanks for the report! The panel decided to award $500 for this report, noting that even though the issue is very unlikely to be exploitable it did cause us to add some good checks. A member of our finance team will be in touch shortly to arrange payment.

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/690821?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086759)*
