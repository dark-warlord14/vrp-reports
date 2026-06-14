# Security: TLS handshake and certificate signature forgery is possible using Bleichenbacher’s Low-Exponent Attack due to faulty ASN.1 length decoding

| Field | Value |
|-------|-------|
| **Issue ID** | [40080460](https://issues.chromium.org/issues/40080460) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Network>SSL |
| **CVE IDs** | CVE-2014-1568 |
| **Reporter** | br...@briansmith.org |
| **Assignee** | ag...@chromium.org |
| **Created** | 2014-09-14 |
| **Bounty** | $5,000.00 |

## Description

**VERSION**  

Chrome Version: All versions of Chrome that use NSS for TLS and/or certificate verification

Operating System: All operating systems where Chrome uses NSS for TLS and/or certificate verification

(I first reported this issue in Mozilla <https://crbug.com/chromium/1064670>, <https://bugzilla.mozilla.org/show_bug.cgi?id=1064670>. I am reporting it here to comply with Chromium's security bug reporting program.)

NSS's PKCS#1 signature verification logic uses the SEC\_QuickDERDecodeItem function to decode the DigestInfo part of the signature. Consequently, due to a bug in SEC\_QuickDERDecodeItem, NSS's PKCS#1 signature verification logic is (still) vulnerable to Bleichenbacher’s Low-Exponent Attack (See <https://www.cdc.informatik.tu-darmstadt.de/reports/reports/sigflaw.pdf> for a good explanation of the low-exponent attack and how to exploit it, and Mozilla <https://crbug.com/chromium/1064636>, Mozilla <https://crbug.com/chromium/351079>, and Mozilla <https://crbug.com/chromium/350640>.)

In quickder.c, the function definite\_length\_decoder is used to decode tags and lengths. It decodes the length as follows:

```
unsigned int data_len;  

// [...]  

data_len = buf[used_length++];  

if (data_len&0x80)  
{  
    int  len_count = data_len & 0x7f;  

    data_len = 0;  

    while (len_count-- > 0)  
    {  
        if (used_length >= length)  
        {  
            return NULL;  
        }  
        data_len = (data_len << 8) | buf[used_length++];  
    }  
}  

```

Note that there is no check that the encoding of the length is the shortest necessary encoding. And also note the integer overflow of data\_len.

See the attached test, which verifies that NSS's SEC\_QuickDERDecodeItem (a.k.a. QuickDER) accepts many malformed encodings of ASN.1 lengths. Note, in particular the test case where the length of the NULL item is encoded as { 0x90, <arbitrary junk>, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 }, which is wrongly interpreted by QuickDER as equivalent to { 0x00 } on both 32-bit and 64-bit platforms. (The attached GTest integrates into Gecko's mozilla::pkix test suite, for my own convenience. However, it doesn't use any of the mozilla::pkix or Gecko GTest utilities, so it should be easy to integrate it into your GTest-based test suite.)

This problem affects Chrome's verification of ServerKeyExchange messages in the TLS handshake, allowing MitM on a TLS connection by forging the ServerKeyExchange message's signature. It also may affect certificate verification on some platforms, allowing for forged certificates. It may also affect WebCrypto and any other parts of Chrome that may depend on PKCS#1 signature verification.

Credits: Antoine Delignat-Lavaud originally pointed out another issue with NSS's verification of PKCS#1 signatures, which is <https://crbug.com/chromium/106463>. After seeing his bug report, I discovered this separate issue with the decoding of ASN.1 lengths, which is a much easier (AFAICT) vulnerability to exploit to forge signatures. After I shared this vulnerability in the NSS bug database, Antoine Delignat-Lavaud successfully used it to forge a certificate that chains to a root CA trusted in some versions of NSS. He attached it to a different bug, <https://crbug.com/chromium/106463>. I won't attach his PoC here since he created it, not me; however, Adam Langley, Ryan Sleevi, and Wan-Teh Chang have access to Mozilla's <https://crbug.com/chromium/106463>, so they can access the PoC. Please make sure Antoine gets credit for creating the PoC certificate.

I recommend thoroughly reading all the comments in Mozilla <https://crbug.com/chromium/351079> and Mozilla <https://crbug.com/chromium/350640>. In particular, note that there may be compatibility issues with strictly matching DigestInfo byte-for-byte.

## Attachments

- [QuickDER-length.patch](attachments/QuickDER-length.patch) (application/octet-stream, 3.7 KB)
- [evp_pkcs1_padding_test.c](attachments/evp_pkcs1_padding_test.c) (application/octet-stream, 8.5 KB)
- [patch](attachments/patch) (text/plain, 27.8 KB)

## Timeline

### wf...@chromium.org (2014-09-14)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-09-16)

At the risk of being cruel, a quick punt to David if he can jump on it this week. David, let me know your Bugzilla and I (or Adam) can grant you access.

### ag...@chromium.org (2014-09-16)

I think Brian is going to write a patch (at least, based on the Mozilla bug). Then we need to coordinate with Mozilla about the release date.

Linux is a pain since we don't ship libnss. I'm not sure that it's feasible to write a patch to libssl to protect a buggy libnss so we might be dependent on the disto there.

### rs...@chromium.org (2014-09-16)

DigestInfo decoding of RSA happens outside of freebl, so in the worst case, we could divert our libssl to our own patched function. We've done this in the past before. 

### ag...@chromium.org (2014-09-16)

That would mean doing significant surgery on the process, right? Because certificate verification is also calling RSA verify. Previously did we patch a jmp into the code, or override the function with the dynamic linker?

### rs...@chromium.org (2014-09-16)

For SSL-layer, we already package libssl/ separately, so we previously just modified that source directly
For !Linux, we already manage NSS ourselves (third-party for iOS, portage-patched for ChromeOS)

But yes, you're right, I think cert verification will be tricky. I'd have to check which library it's in, but we MAY be able to do something like we do with libssl (that is, remove the .so from the pkg-config, then add in our own hermetic version)

### da...@chromium.org (2014-09-17)

> David, let me know your Bugzilla and I (or Adam) can grant you access.

I'm davidben@google.com there.

### ag...@chromium.org (2014-09-17)

State of this: Brian is handing off the patch. I'm out today but, if Kai or someone else doesn't pick it up today, then I'll try and setup an NSS build and take it tomorrow.

I've still to hear from anyone at Mozilla what their release timeline is however.

### br...@briansmith.org (2014-09-18)

BoringSSL already contains the defense against this class of issues.

In one of his bugzilla comments, agl mentions that BoringSSL uses the hardened PKCS#1 padding check for ServerKeyExchange, but not for certificate verification. Is this just because you always delegate certificate verification to the OS, or is there another (hidden?) PKCS#1 padding checking function?

Is there an OpenSSL project bug for upstreaming the BoringSSL implementation to OpenSSL? And, how is that upstreaming progressing? I have some concerns about the OpenSSL implementation as well, and I'd like to communicate with the people that already researched this for OpenSSL, if possible. In particular, if they could share their assessment of the exploitability of OpenSSL's implementation, that would be quite helpful.

I am concerned that other products also seem to accept non-canonical encodings of the tag and/or length fields of ASN.1 structures inside PKCS#1 signatures. 3 of 3 implementations I've looked at appear to have such issues (OpenSSL is one and wpa_supplicant is the other), though I haven't done the work to execute the actual Bleichenbacher short exponent attack to verify the exploitability. If you happen to have some code for forging signatures using the Bleichenbacher attack sitting around, it would be great if you could share it. This is why I do not have time to finish the NSS work; I'm confident that one of the 13 other people CC'd on that bug are qualified to "clean up" my patch while I look at the other products.

With all that in mind, making a big announcement about an emergency NSS release to fix this issue may not be a great idea. If I had to extrapolate from what I've found so far, there are likely several crypto libraries that are affected. The only thing that isn't clear is whether they are saved by being more diligent by the "at least 8 padding bytes" check and/or the lack of integer overflow in length decoding. But, I think that some of them may be susceptible to integer overflow in their decoding of the high-number encoding of ASN.1 tags, leading to similar results.

### ag...@chromium.org (2014-09-18)

> In one of his bugzilla comments, agl mentions that BoringSSL uses the hardened
PKCS#1 padding check for ServerKeyExchange, but not for certificate verification. Is this just because you always delegate certificate verification to the OS, or is there another (hidden?) PKCS#1 padding checking function?

It's because certificate verification is done by the OS.

I hadn't planned on upstreaming the BoringSSL code - it was just something that I didn't like the smell of when I was refactoring. However, if OpenSSL has problems then they're very welcome to take it.

### pa...@chromium.org (2014-09-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-09-19)

Can I please get access to the relevant Mozilla bugs? Thanks.

### br...@briansmith.org (2014-09-19)

agl posted some of his test cases into the NSS bug. I assume that you are also testing BoringSSL and also OpenSSL, since I think that you may still be affected by OpenSSL on Android or other platforms via their certificate verification libraries. Here are the test cases I sent in my OpenSSL bug report. The OpenSSL trunk fails most of the cases tests. Note in particular that it accepts the high tag number form and indefinite length encoding, which NSS does not accept. The OpenSSL team also told me that OpenSSL's ASN.1 decoder was recently patched on the trunk to be more lenient in accepting leading zeros in lengths, so there are definitely differences between various OpenSSL releases. Based on what I've been able to figure out, OpenSSL would be harder to exploit than NSS, because I've not found a way to insert arbitrary bytes. Still, the OpenSSL behavior is worrying to me because there are *many* places in a DigestInfo where you can play with the tag encoding and/or the length encoding.

Also, I exchanged some email with the Intel, who also independently discovered this issue across a variety of crypto libraries. According to them, their first discovery of the issue was in July, and they discovered the NSS issue in early September. To me, having multiple people independently discover the issue indicates that it is probably not that hard for others to figure out too.

### pa...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### ag...@chromium.org (2014-09-22)

(Note: originally reported by Antoine Delignat-Lavaud of INRIA. Brian Smith found significant extensions to the issue. It appears to have been concurrently found and reported by Intel PSIRT, but they were later.)

### ag...@chromium.org (2014-09-23)

We expect to do a stable and beta push of this on Wednesday, matching Firefox.

### bu...@chromium.org (2014-09-23)

Project: chromeos/overlays/chromeos-overlay
Branch : stabilize.5978.98.B
Author : Ryan Sleevi <rsleevi@chromium.org>
Commit : 9614312e55f7f0d83de068b4976a17599fe29c8b

Code-Review  0 : chrome-internal-fetch
Code-Review  +2: Josafat Garcia, Ryan Sleevi
Commit-Queue 0 : Ryan Sleevi, chrome-internal-fetch
Commit-Queue +1: Josafat Garcia
Verified     0 : Ryan Sleevi, chrome-internal-fetch
Verified     +1: Josafat Garcia
Change-Id      : I6ffbbe8d4bf864a8c41443b22b9f49650509ece5
Reviewed-at    : https://chrome-internal-review.googlesource.com/176784

M37_98:Backport fixes from NSS 3.17.1 for Mozilla https://crbug.com/chromium/1064636

BUG=chromium:414124
TEST=equery-${BOARD} shows NSS 3.16-r2 from the private overlay

app-crypt/nss/Manifest
app-crypt/nss/files/nss-3.14.2-solaris-gcc.patch
app-crypt/nss/files/nss-3.15-abort-on-failed-urandom-access.patch
app-crypt/nss/files/nss-3.15-chromeos-cert-nicknames.patch
app-crypt/nss/files/nss-3.15-gentoo-fixup-warnings.patch
app-crypt/nss/files/nss-3.15-gentoo-fixups.patch
app-crypt/nss/files/nss-3.15-x32.patch
app-crypt/nss/files/nss-3.15.4-enable-pem.patch
app-crypt/nss/files/nss-3.16-chromeos-oaep-and-aeskw.patch
app-crypt/nss/files/nss-3.16-chromeos-verify-digestinfo.patch
app-crypt/nss/nss-3.16-r1000.ebuild
app-crypt/nss/nss-3.16.ebuild
dev-libs/nss/Manifest
dev-libs/nss/files/nss-3.14.2-solaris-gcc.patch
dev-libs/nss/files/nss-3.15-abort-on-failed-urandom-access.patch
dev-libs/nss/files/nss-3.15-chromeos-cert-nicknames.patch
dev-libs/nss/files/nss-3.15-gentoo-fixup-warnings.patch
dev-libs/nss/files/nss-3.15-gentoo-fixups.patch
dev-libs/nss/files/nss-3.15-x32.patch
dev-libs/nss/files/nss-3.15.4-enable-pem.patch
dev-libs/nss/files/nss-3.16-chromeos-oaep-and-aeskw.patch
dev-libs/nss/files/nss-3.16-chromeos-verify-digestinfo.patch
dev-libs/nss/metadata.xml
dev-libs/nss/nss-3.16-r1000.ebuild
dev-libs/nss/nss-3.16.ebuild

### bu...@chromium.org (2014-09-23)

Project  : chromeos/overlays/chromeos-overlay
Branch   : release-R37-5978.B
Author   : Ryan Sleevi <rsleevi@chromium.org>
Committer: Josafat Garcia <josafat@google.com>
Commit   : 87e23abd55b53deece773699d2f939aba1bb04f8

Code-Review  +2: Josafat Garcia, Ryan Sleevi
Commit-Queue 0 : Ryan Sleevi
Commit-Queue +1: Josafat Garcia
Verified     0 : Ryan Sleevi
Verified     +1: Josafat Garcia
Commit Queue   : Chumped
Change-Id      : I6ffbbe8d4bf864a8c41443b22b9f49650509ece5
Reviewed-at    : https://chrome-internal-review.googlesource.com/177185

M37:Backport fixes from NSS 3.17.1 for Mozilla https://crbug.com/chromium/1064636

BUG=chromium:414124
TEST=equery-${BOARD} shows NSS 3.16-r2 from the private overlay

app-crypt/nss/Manifest
app-crypt/nss/files/nss-3.14.2-solaris-gcc.patch
app-crypt/nss/files/nss-3.15-abort-on-failed-urandom-access.patch
app-crypt/nss/files/nss-3.15-chromeos-cert-nicknames.patch
app-crypt/nss/files/nss-3.15-gentoo-fixup-warnings.patch
app-crypt/nss/files/nss-3.15-gentoo-fixups.patch
app-crypt/nss/files/nss-3.15-x32.patch
app-crypt/nss/files/nss-3.15.4-enable-pem.patch
app-crypt/nss/files/nss-3.16-chromeos-oaep-and-aeskw.patch
app-crypt/nss/files/nss-3.16-chromeos-verify-digestinfo.patch
app-crypt/nss/nss-3.16-r1000.ebuild
app-crypt/nss/nss-3.16.ebuild
dev-libs/nss/Manifest
dev-libs/nss/files/nss-3.14.2-solaris-gcc.patch
dev-libs/nss/files/nss-3.15-abort-on-failed-urandom-access.patch
dev-libs/nss/files/nss-3.15-chromeos-cert-nicknames.patch
dev-libs/nss/files/nss-3.15-gentoo-fixup-warnings.patch
dev-libs/nss/files/nss-3.15-gentoo-fixups.patch
dev-libs/nss/files/nss-3.15-x32.patch
dev-libs/nss/files/nss-3.15.4-enable-pem.patch
dev-libs/nss/files/nss-3.16-chromeos-oaep-and-aeskw.patch
dev-libs/nss/files/nss-3.16-chromeos-verify-digestinfo.patch
dev-libs/nss/metadata.xml
dev-libs/nss/nss-3.16-r1000.ebuild
dev-libs/nss/nss-3.16.ebuild

### bu...@chromium.org (2014-09-23)

Project  : chromeos/overlays/chromeos-overlay
Branch   : release-R38-6158.B
Author   : Ryan Sleevi <rsleevi@chromium.org>
Committer: Josafat Garcia <josafat@google.com>
Commit   : d578620bc892f1a0cb514cd7632e761b8de2ddcc

Code-Review  +2: Josafat Garcia, Ryan Sleevi
Commit-Queue 0 : Ryan Sleevi
Commit-Queue +1: Josafat Garcia
Verified     0 : Ryan Sleevi
Verified     +1: Josafat Garcia
Commit Queue   : Chumped
Change-Id      : I6ffbbe8d4bf864a8c41443b22b9f49650509ece5
Reviewed-at    : https://chrome-internal-review.googlesource.com/176741

M38:Backport fixes from NSS 3.17.1 for Mozilla https://crbug.com/chromium/1064636

BUG=chromium:414124
TEST=equery-${BOARD} shows NSS 3.16-r2 from the private overlay

app-crypt/nss/Manifest
app-crypt/nss/files/nss-3.14.2-solaris-gcc.patch
app-crypt/nss/files/nss-3.15-abort-on-failed-urandom-access.patch
app-crypt/nss/files/nss-3.15-chromeos-cert-nicknames.patch
app-crypt/nss/files/nss-3.15-gentoo-fixup-warnings.patch
app-crypt/nss/files/nss-3.15-gentoo-fixups.patch
app-crypt/nss/files/nss-3.15-x32.patch
app-crypt/nss/files/nss-3.15.4-enable-pem.patch
app-crypt/nss/files/nss-3.16-chromeos-oaep-and-aeskw.patch
app-crypt/nss/files/nss-3.16-chromeos-verify-digestinfo.patch
app-crypt/nss/nss-3.16-r1000.ebuild
app-crypt/nss/nss-3.16.ebuild
dev-libs/nss/Manifest
dev-libs/nss/files/nss-3.14.2-solaris-gcc.patch
dev-libs/nss/files/nss-3.15-abort-on-failed-urandom-access.patch
dev-libs/nss/files/nss-3.15-chromeos-cert-nicknames.patch
dev-libs/nss/files/nss-3.15-gentoo-fixup-warnings.patch
dev-libs/nss/files/nss-3.15-gentoo-fixups.patch
dev-libs/nss/files/nss-3.15-x32.patch
dev-libs/nss/files/nss-3.15.4-enable-pem.patch
dev-libs/nss/files/nss-3.16-chromeos-oaep-and-aeskw.patch
dev-libs/nss/files/nss-3.16-chromeos-verify-digestinfo.patch
dev-libs/nss/metadata.xml
dev-libs/nss/nss-3.16-r1000.ebuild
dev-libs/nss/nss-3.16.ebuild

### [Deleted User] (2014-09-23)

We at Opera currently don't have access to neither the commit nor the review. Is it possible to grant us access?

### jo...@chromium.org (2014-09-23)

[Empty comment from Monorail migration]

### ag...@chromium.org (2014-09-23)

haavardm: please see the prelim patch, attached. This is not the final patch that will go into NSS, but we believe that it works.

### br...@briansmith.org (2014-09-24)

In private conversation with Antoine, I got the impression that he knows of other ways that OpenSSL's ASN.1 parser is "too flexible" that are not covered by the posted test cases. I've recommended him to contact you about that. It may be a good idea to touch base to him on that topic.

### [Deleted User] (2014-09-24)

[Comment Deleted]

### [Deleted User] (2014-09-24)

agl: Thanks for the patch. 

Is this the full patch though? I can that it straightens up the DigestInfo parsing, but it does not touch the SEC_QuickDERDecodeItem implementation which is used directly both in src/net and src/crypto.

Ninja edit: s/chromium/crypto

### ag...@chromium.org (2014-09-24)

haavardm: that's what we're releasing with, although it's not the form of the patch that landed in NSS. (Note: NSS updates landed in public yesterday.)

It would be good for NSS to fix SEC_QuickDERDecodeItem, but its uses in Chromium aren't critical. The closest is in signature_verifier_nss.cc, but there it's just used to get an algorithm hint. That's probably a mistake since the object should know the algorithm already, but it doesn't present the same concerns as in core RSA verification. 

### [Deleted User] (2014-09-24)

agl: Any reason you don't use the NSS version?

I haven't got access to the discussions going on on the mozilla side so there's probably some info I'm missing. But SEC_QuickDERDecodeItem is used quite a lot of places inside of NSS so it seems strange to me that it has not been fixed. Especially if it is the main reason for this bug.

### ag...@chromium.org (2014-09-24)

The final NSS version was not ready in time.

I agree that at least the integer overflow would be good to fix in SEC_QuickDERDecodeItem, but NSS hasn't done that yet.

### in...@chromium.org (2014-09-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-25)

davidben@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### rs...@chromium.org (2014-09-25)

Fixed through the src-internal merge, but we'll still land the public fix from NSS 3.17.1

### cl...@chromium.org (2014-09-25)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### bu...@chromium.org (2014-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/93c6ad3a8909a8c4ad84634d6efe7698130a79c6

commit 93c6ad3a8909a8c4ad84634d6efe7698130a79c6
Author: Adam Langley <agl@google.com>
Date: Thu Sep 25 22:59:33 2014

net: roll NSS.

Brings in the following changes:

commit 87b96db4268293187d7cf741907a6d5d1d8080e0
Author: agl@chromium.org <agl@chromium.org>
Date:   Thu Sep 25 20:28:09 2014 +0000

    Update to NSS 3.16.7.

    This contains a fix for the RSA signature forgery bug (CVE-2014-1568):
    https://www.mozilla.org/security/announce/2014/mfsa2014-73.html

    Chrome and ChromeOS have already released updates containing this fix:
      http://googlechromereleases.blogspot.com/2014/09/stable-channel-update_24.html
      http://googlechromereleases.blogspot.com/2014/09/stable-channel-update-for-chrome-os_24.html

    https://codereview.appspot.com/142600043/

    (This the SVN version of the git change, referenced above. It seems that the
    NSS git is still a mirror from this SVN repo and thus one cannot commit to it
    directly.)

    git-svn-id: http://src.chromium.org/svn/trunk/deps/third_party/nss@292145 4ff67af0-8c30-449e-8e8b-ad334ec8d88c

BUG=414124

Review URL: https://codereview.chromium.org/603153004

Cr-Commit-Position: refs/heads/master@{#296814}

[modify] https://chromium.googlesource.com/chromium/src.git/+/93c6ad3a8909a8c4ad84634d6efe7698130a79c6/DEPS


### ag...@chromium.org (2014-09-25)

[Empty comment from Monorail migration]

### br...@briansmith.org (2014-09-26)

All the details of this have now been publicly disclosed:
https://www.reddit.com/r/netsec/comments/2hd1m8/rsa_signature_forgery_in_nss/cksnr02

### br...@briansmith.org (2014-09-29)

I want to point out one more detail, in case it got overlooked:

The PKCS#1 signatures that this bug is concerned with are of this form:

    00|01|FF...FF|00|P|S

P is some metadata prefix and S is the result of calculating a secure digest of the signed data, and the signed data is attacker-controlled. The bug was caused by the fact that NSS accepts unconstrained attacker-controlled data within the DigestInfoPrefix portion. The bug was fixed by requiring that the value of P be a member of a set of 10 predetermined values (the AlgorithmIdentifier prefixes for SHA-1 through SHA-512, with and without the NULL parameter encoded), on the assumption that this would make it nearly impossible to find a perfect cube using any of those prefixes, due to the preimage resistance of the accepted SHA-* digest functions and the scarcity of perfect cubes within the allowed ranges.

However, in SSL 3.0, TLS 1.0, and TLS 1.1, there is another form of PKCS#1 signature used for the ServerKeyExchange message:

    00|01|FF...FF|00|M|S

M is the MD5 digest of the signed data and S is the SHA1 digest of the signed data, where the attacker controls the signed data.

We don't usually give MD5 a lot of credit for its security. A very conservative design would call for assuming that MD5 offers no preimage or collision resistance whatsoever. (Researchers have little motivation to improve the existing attacks on MD5 for a variety of social reasons, so we'll likely never learn of significant improvements in breaking the preimage or collision resistance of MD5.) If one takes that conservative position, then one would agree that since the attacker controls the signed data, then effectively the attacker controls the value of the MD5 digest of the signed data. Such an annoying person would then be likely to claim that allowing an attacker-controlled value of M in 00|01|FF...|00|M|S is not clearly better than allowing an attacker-controlled value of P in 00|01|FF...FF|00|P|S. They may then demand some evidence that accepting values of the form 00|01|FF...FF|00|M|S is safe when accepting values of the other form was proven unsafe, or that we no longer accept values of the form 00|01|FF...|00|M|S. Given that we have to accept values of the form 00|01|FF...|00|M|S in signatures in order for TLS<1.2 to work (mostly), we should be motivated to show that it is indeed safe to accept such values. But, it is surprisingly difficult to do so in a convincing fashion without relying on MD5 being somewhat secure, unless one can prove that the attack is not possible when P (M) is always 16 bytes long.

For this and other reasons it makes more sense to convince ourselves that, when decoding whether it is safe to accept 00|01|FF...FF|00|P|S, we can make that decision purely on the length of the modulus, the value of E, the maximum allowed length of P, the length of S, and/or the security strength of the weakest digest algorithm accepted, without considering specific values of P.

I'm planning to expand on this thought (in public) soon, because I think it is an amusing tidbit. If you know anybody that has already thought this through, I'd love to chat with them.

### ag...@chromium.org (2014-09-29)

This only allows 16 bytes of control, which isn't that much for this case.

Also, it's not collision resistance that's at issue here, I think it's just preimage resistance. Let's say that you have 16 bytes that work for the attack - now you need to find an MD5 preimage for that. (And you also need it to be a valid public key for a SKX message, right?) Building an MD5 collision doesn't seem useful here.

But preimage attacks appear to be *really* hard, even MD4 has 2^95 preimage resistance: https://github.com/zooko/hash-function-survey/blob/master/preimage-attacks-color.rst

It's true that people aren't looking for preimage attacks against MD5 any longer, but they were for a long time (and against other hash functions) and preimage attacks were substantially less effective than collision attacks.

### da...@chromium.org (2014-09-29)

You'd also need your preimage to have a suitable SHA-1 hash for your perfect cube, since you don't get to change the two independently.

### ag...@chromium.org (2014-09-29)

Is it likely that you could handle the SHA-1 part separately. See section 5 of https://www.cdc.informatik.tu-darmstadt.de/reports/reports/sigflaw.pdf.

### br...@briansmith.org (2014-09-29)

Adam and Ben, I agree with you in the sense that it is nothing to panic about, especially because the signature of the ServerKeyExchange message covers client_random and server_random.

However, I think it would be useful to try to convince ourselves that any prefix of N bytes or less is safe, regardless of its value, for multiple reasons. First, that would take the debate about the strength of MD5 out of the equation. Also, when somebody (in the past or in the future) defines a new digest AlgorithmIdentifier, we could be sure that their choice of OID and/or parameters was not specially-chosen to be helpful in forging signatures.

I think the difficulty of an attack, assuming no specially-chosen AlgorithmIdentifier values, is a function of the preimage resistance of the digest algorithms. But, the difficulty is also reduced by how many perfect cubes there are in the allowed interval, because you just need *any* perfect cube that fits in the allowed interval. intuitively, we would expect that there shouldn't be enough perfect cubes to reduce the difficulty by a significant factor. But, it would be great to avoid relying on that. And, it seems like if one can prove that, then one isn't that far away from proving that a 16 byte prefix is too small to be useful to an attacker.

### ti...@chromium.org (2014-10-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-10-07)

Our reward panel decided on $5000 to INRIA for this bug. Woohoo!

We'll be in contact to facilitate the payment.

### ti...@google.com (2014-12-09)

Emailed antoine@delignat-lavaud.fr regarding reward payment.

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-01)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-08-15)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chromeos/overlays/chromeos-overlay/+/1872788ed4bc61a27e3b56818b72ba84a8e8a297

commit 1872788ed4bc61a27e3b56818b72ba84a8e8a297
Author: Ryan Sleevi <rsleevi@chromium.org>
Date: Tue Sep 23 08:55:56 2014


### is...@google.com (2018-08-15)

This issue was migrated from crbug.com/chromium/414124?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080460)*
