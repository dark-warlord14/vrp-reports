# TLS session caching occurs before certificate validation

| Field | Value |
|-------|-------|
| **Issue ID** | [40078213](https://issues.chromium.org/issues/40078213) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>SSL |
| **Reporter** | an...@gmail.com |
| **Assignee** | rs...@chromium.org |
| **Created** | 2013-10-08 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.69 Safari/537.36

Steps to reproduce the problem:
1. Connect to a server with an invalid certificate
2. On server, replace certificate with a valid one
3. Refresh the page and observe that Chrome attempts to resume the session established in 1.

What is the expected behavior?
Because the certificate was invalid, the session should not have been cached.

What went wrong?
We found this bug when writing our paper on active network attackers and attacks on session integrity (where we discuss the truncation bugs mentioned in https://crbug.com/chromium/244260) as we were wondering whether it is possible to force TLS sessions (like one can force cookies) with an active network attacker.

It turns out that because Chrome tried to cache TLS sessions before the certificate chain is verified, there is a beatiful TLS session forcing attack that can allow a man in the middle to decrypt a TLS session because it established the master key on an unauthenticated session that can be resumed with the legitimate target website. The attack plays out as follows:

       |                                                         |                                                         |
   Nc  |     Client Hello (Nc, ciphers, ext_session_ticket       |  Client Hello (Nc, RSA_AES_CBC_SHA, ext_session_ticket) |   Nc
       |-------------------------------------------------------->|-------------------------------------------------------->|
       |                                                         |                                                         |
   Ns  |  Server Hello (Ns, RSA_AES_CBC_SHA, ext_session_ticket) |  Server Hello (Ns, RSA_AES_CBC_SHA, ext_session_ticket) |   Ns
       |<--------------------------------------------------------|<--------------------------------------------------------|
       |                                                         |                                                         |
   Ca  |            Certificate Ca, Server Hello Done            |            Certificate Ct, Server Hello Done            |   Ct
   Pa  |<--------------------------------------------------------|<--------------------------------------------------------|   Pt
       |                                                         |                                                         |
  PMS  |              Client Key Exchange {PMS}_Pa               |              Client Key Exchange {PMS}_Pt               |   PMS
       |-------------------------------------------------------->|-------------------------------------------------------->|
       |                                                         |                                                         |
       |              Change Cipher Spec, Finished               |              Change Cipher Spec, Finished               |
       |-------------------------------------------------------->|-------------------------------------------------------->|
       |                                                         |                                                         |
   T   |                   New Session Ticket T                  |                   New Session Ticket T                  |   T
       |<--------------------------------------------------------|<--------------------------------------------------------|
       |                                                         |                                                         |
       |              Change Cipher Spec, Finished               |              Change Cipher Spec, Finished               |
       |<--------------------------------------------------------|<--------------------------------------------------------|
       |                                                         |                                                         |
       |              *** certificate error ***                  |                 *** close connection ***                |
       |                                                                                                                   |
       |                                                 Client Hello (T)                                                  |
       |------------------------------------------------------------------------------------------------------------------>|
       |                                                                                                                   |
    Browser                                                   Attacker                                                   Target

Nc: client nonce, Ns: server nonce, Ca: attacker's certificate (invalid), Ct: target's certificate (valid),
PMS: pre-master secret, Pa: attacker's publick key, Pt: target's public key, T: session ticket

Because T is established with valid parameters (Nc, Ns and PMS), it can be resumed on the target website, but the attacker knows the session master key an can decrypt the traffic on the session. Note that the attack is not possible when a forward secrecy preserving key exchange is used, however, the man in the middle is able to force the use of old-school RSA key exchange to mount the attack.

As for 244260, credit goes to Antoine Delignat-Lavaud and Karthikeyan Bhargavan at Prosecco, Inria Paris for this one.
We tested other (non-Chromium based) browsers and found that they did not cache TLS sessions when a certificate error occurs.

Did this work before? N/A 

Chrome version: 30.0.1599.69  Channel: stable
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 11.8 r800

## Attachments

- [ssl-cache-session.txt](attachments/ssl-cache-session.txt) (text/x-diff; charset=us-ascii, 2.8 KB)
- [mitm-dhe.pdf](attachments/mitm-dhe.pdf) (application/pdf; charset=binary, 39.6 KB)

## Timeline

### me...@chromium.org (2013-10-08)

Thanks for the report. CC'ing SSL experts.

### ag...@chromium.org (2013-10-08)

Let's assume that you have performed the exchange detailed in #1. Now:

1) The attacker has a session ticket, T, and the master key for it.
2) T is valid from the point of view of the server.
3) The client has a cached session, with a master key that the attacker also knows, and has linked T to it.

I assume that the attacker is going to choose to make the two master keys equal?

If the client attempts to resume the session and the attacker doesn't interfere, then the keys will match up, because the master secrets of the two sessions are equal. However, the resumed session will be linked with the attacker's certificate chain, Ca, and will cause a certificate error in the client.

So it's likely that the client will need to be restarted before they can communicate with the true server due to the session cache, but a MITM can already implement a DoS attack.

Am I missing something that allows the attacker to do something worse?

### pa...@google.com (2013-10-08)

In the original bug report, we are missing a step 4: Session resumption succeeds? Or fails? If it fails, as agl assumes, then yeah it's a DoS. If it succeeds... :\

It seems "cleaner" to me to do caching after certificate chain validation succeeds, certainly.

### rs...@chromium.org (2013-10-08)

We always re-validate the chain, even when doing session resumption. That's why we carry a patch to allow us to cache the certificate chain in the session ID cache.

So I'm not sure there's an issue here, beyond what agl described in the DoS case. Have I missed something?

### an...@gmail.com (2013-10-09)

Adam: yes, the two master keys are supposed to be equal.
As you mention, the session will still be bound to an invalid certificate chain. Thus, the attack may not be very useful in practice as is - however, from a cryptographic protocol point of view, the ability to resume the attacker-negociated session on the target website is still a violation of the TLS security guarantees, which should be sufficient motivation to wait until the handshake is authenticated before caching it.

### rs...@chromium.org (2013-10-09)

I'm not sure I understand - the attacker-negotiated session will not be resumable with the actual website, because the attacker can't negotiate with the 'right' cert.

I'm not sure I see where the cryptographic risk is. The client will either offer a session that the (legitimate) server doesn't know, or it will offer a session and the negotiation will fail, because the security parameters of the negotiated handshakes are (by definition) different, because one factors in the fake cert and the other the real cert.

### an...@gmail.com (2013-10-10)

Let me rephrase the problem - in the above figure, T is a valid session ticket for the target website because its master key, generated from Nc, Ns and PMS, matches the one stored by the client. Thus, both the attacker and the victim are able to resume the session with the target website.

It is true that the session will remain associated with the attacker's certificate - however, the ability to resume the session with the victim website is an authentication failure. Even self-signed certificates should enforce authentication if you chose to verify the certificate by manual inspection and bypass the certificate warning. In this case, the certificate displayed will be the attacker's, but the session is resumed on the target website which uses a different certificate. Thus, this is still a violation of the TLS authentication guarantee.

### rs...@chromium.org (2013-10-10)

Triaging to Severity-High, based on https://sites.google.com/a/chromium.org/dev/developers/severity-guidelines and the attack described in https://crbug.com/chromium/305951



### cl...@chromium.org (2013-10-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-10)

Adding milestone and impact labels.

### sc...@gmail.com (2013-10-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-10-11)

[Empty comment from Monorail migration]

### an...@gmail.com (2013-10-11)

(This is probably Severity-Medium/P2 because of the MitM involved and low exploitability. However, thinking more about agl's comment on the cached certificate status of the session, we think there is a way of bypassing this defense as well)

### ag...@chromium.org (2013-10-11)

bouchon.org: yes, the underlying issue here is deeper than noted in #1. We're working though it.

### [Deleted User] (2013-10-11)

We should be able to apply a Chrome-specific patch to NSS as follows.

1. In net/third_party/nss/ssl/ssl3con.c, function ssl3_FinishHandshake,
remove the following code:

    if (ss->ssl3.hs.cacheSID) {
        (*ss->sec.cache)(ss->sec.ci.sid);
        ss->ssl3.hs.cacheSID = PR_FALSE;
    }

2. Add a new function SSL_CacheSession, modeled after SSL_InvalidateSession,
that executes the code we removed above:

SECStatus
SSL_CacheSession(PRFileDesc *fd)
{
    sslSocket *   ss = ssl_FindSocket(fd);
    SECStatus     rv = SECFailure;

    if (ss) {
        ssl_Get1stHandshakeLock(ss);
        ssl_GetSSL3HandshakeLock(ss);

        if (ss->ssl3.hs.cacheSID) {
            (*ss->sec.cache)(ss->sec.ci.sid);
            ss->ssl3.hs.cacheSID = PR_FALSE;
        }
        rv = SECSuccess;

        ssl_ReleaseSSL3HandshakeLock(ss);
        ssl_Release1stHandshakeLock(ss);
    }
    return rv;
}

3. In net/socket/ssl_client_socket_nss.cc, function
SSLClientSocketNSS::DoVerifyCertComplete, add the following code
at the end of the function, after the value of |result| is final:

  if (result == OK)
    SSL_CacheSession(nss_fd_);

Note: this should ideally be done by SSLClientSocketNSS::Core.

### [Deleted User] (2013-10-11)

The attached patch ssl-cache-session.txt is a proof of concept for the
approach I outlined above.

It does introduce a new issue: if False Start is used, we will cache the
session before we have verified the server's Finished message.

### ag...@chromium.org (2013-10-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-19)

rsleevi@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### an...@gmail.com (2013-10-19)

It is also worth noting that certificate validation happens after client authentication on current Chrome, i.e. the client certificate prompt is shown before the certificate error screen and if a certificate was selected (or cached from a previous session), it will still sign the handshake with the invalid certificate. You should make sure that this is no longer possible when this bug is fixed.

### js...@chromium.org (2013-10-19)

@rsleevi - Active man-in-the-middle is a significant mitigating factor, so this wouldn't exceed medium-severity (assuming the result is a full SSL/TLS compromise). See the reports on CRIME and BEAST for reference.


### cl...@chromium.org (2013-10-27)

rsleevi@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### an...@gmail.com (2013-11-04)

In the DHE key exchange, NSS accepts the server parameters <p, g, g^q> where p=2q+1 is such that q is prime and g is not a quadratic residue mod p. Then, g^q = p-1 and the computed PMS g^(q*Kc) is 1 if Kc is even (because g^(2q)=g^(p-1)=1 [mod p]) and p-1 if Kc is odd. Thus, if the server also accepts g^q in the client key exchange (this seems to be the case of about 15% of the Alexa Top 10k), then the same problem as for the RSA key exchange applies. I submitted a bug report to NSS at https://bugzilla.mozilla.org/show_bug.cgi?id=934545 to propose rejecting p-1 as a valid server public value in NSS.

The attached file describes how the attacker can synchronize the sessions with the client and victim server to have the same key.

### cl...@chromium.org (2013-11-05)

rsleevi@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### rs...@chromium.org (2013-11-06)

[Empty comment from Monorail migration]

### cb...@chromium.org (2013-11-10)

Moving to M31 since the M30 ship is near the end.

### cb...@chromium.org (2013-11-10)

[Empty comment from Monorail migration]

### cb...@chromium.org (2013-11-10)

wtc: I'm reassigning to you since rsleevi will be traveling this week.

### cb...@chromium.org (2013-11-11)

If this is really a P0 it should block stable release. If it should not block release let's move to P1.

### js...@chromium.org (2013-11-11)

I think we can all agree that @rsleevi just cares too much. This should have been Pri-1.

### cb...@chromium.org (2013-11-12)

moving ownership back to sleevi asthis is not a p0

### cl...@chromium.org (2013-11-15)

rsleevi@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cb...@chromium.org (2013-11-21)

rsleevi: Any progress here?

### cl...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-21)

Medium Severity Bugs should not need this label. This is only for high+ severity bugs.

### cl...@chromium.org (2013-11-23)

rsleevi@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-12-02)

rsleevi@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

- Your friendly ClusterFuzz

### cb...@chromium.org (2013-12-04)

Removing M31.

I talked to rsleevi and there is some progress being made on this.

### cl...@chromium.org (2013-12-10)

rsleevi@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-12-18)

rsleevi@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### fe...@chromium.org (2013-12-20)

rsleevi@, how's this going?

### bu...@chromium.org (2013-12-21)

------------------------------------------------------------------------
r242219 | rsleevi@chromium.org | 2013-12-21T00:09:19.221283Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/url_request/url_request_unittest.cc?r1=242219&r2=242218&pathrev=242219
   A http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/patches/sessioncache.patch?r1=242219&r2=242218&pathrev=242219
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/patches/applypatches.sh?r1=242219&r2=242218&pathrev=242219
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/README.chromium?r1=242219&r2=242218&pathrev=242219
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/exports_win.def?r1=242219&r2=242218&pathrev=242219
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/sslsecur.c?r1=242219&r2=242218&pathrev=242219
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/ssl3con.c?r1=242219&r2=242218&pathrev=242219
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/ssl.h?r1=242219&r2=242218&pathrev=242219
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_nss.cc?r1=242219&r2=242218&pathrev=242219

Defer TLS session caching until after certificate verification

BUG=305220
R=wtc@chromium.org, wtc

Review URL: https://codereview.chromium.org/93773007
------------------------------------------------------------------------

### rs...@chromium.org (2013-12-21)

[Empty comment from Monorail migration]

### rs...@chromium.org (2013-12-21)

Right. Android.

### bu...@chromium.org (2013-12-21)

------------------------------------------------------------------------
r242236 | rsleevi@chromium.org | 2013-12-21T01:17:52.669955Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/sslsecur.c?r1=242236&r2=242235&pathrev=242236
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/ssl3con.c?r1=242236&r2=242235&pathrev=242236
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/ssl.h?r1=242236&r2=242235&pathrev=242236
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_nss.cc?r1=242236&r2=242235&pathrev=242236
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/url_request/url_request_unittest.cc?r1=242236&r2=242235&pathrev=242236
   D http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/patches/sessioncache.patch?r1=242236&r2=242235&pathrev=242236
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/patches/applypatches.sh?r1=242236&r2=242235&pathrev=242236
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/README.chromium?r1=242236&r2=242235&pathrev=242236
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/exports_win.def?r1=242236&r2=242235&pathrev=242236

Revert 242219 "Defer TLS session caching until after certificate..."

> Defer TLS session caching until after certificate verification
> 
> BUG=305220
> R=wtc@chromium.org, wtc
> 
> Review URL: https://codereview.chromium.org/93773007

TBR=rsleevi@chromium.org

Review URL: https://codereview.chromium.org/120043007
------------------------------------------------------------------------

### rs...@chromium.org (2013-12-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-12-27)

------------------------------------------------------------------------
r242585 | rsleevi@chromium.org | 2013-12-27T02:14:24.649010Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/README.chromium?r1=242585&r2=242584&pathrev=242585
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/exports_win.def?r1=242585&r2=242584&pathrev=242585
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/sslsecur.c?r1=242585&r2=242584&pathrev=242585
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/ssl3con.c?r1=242585&r2=242584&pathrev=242585
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/ssl.h?r1=242585&r2=242584&pathrev=242585
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_session_cache_openssl_unittest.cc?r1=242585&r2=242584&pathrev=242585
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_nss.cc?r1=242585&r2=242584&pathrev=242585
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_openssl.cc?r1=242585&r2=242584&pathrev=242585
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_session_cache_openssl.cc?r1=242585&r2=242584&pathrev=242585
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/url_request/url_request_unittest.cc?r1=242585&r2=242584&pathrev=242585
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_session_cache_openssl.h?r1=242585&r2=242584&pathrev=242585
   A http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/patches/sessioncache.patch?r1=242585&r2=242584&pathrev=242585
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/patches/applypatches.sh?r1=242585&r2=242584&pathrev=242585

Defer TLS session caching until after certificate verification

BUG=305220
R=wtc

Review URL: https://codereview.chromium.org/112183006
------------------------------------------------------------------------

### rs...@chromium.org (2013-12-27)

Setting MR for M-33 first, although with the holidays, this may need to hit a canary or two (including on Android).

Extensive unit tests though! Because no one was ever led astray by unit tests.

### mb...@chromium.org (2013-12-30)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-01-06)

Ping on Merge-Request

### in...@chromium.org (2014-01-06)

I think bug has to be in fixed status for Merge-Requested notification to work for RM.

### la...@google.com (2014-01-07)

Was just waiting based on https://crbug.com/chromium/305220#c48 for more feedback.  Flipping the approved bit, if you folks are confident.

### bu...@chromium.org (2014-01-07)

------------------------------------------------------------------------
r243342 | wtc@chromium.org | 2014-01-07T18:47:13.795979Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/net/third_party/nss/patches/applypatches.sh?r1=243342&r2=243341&pathrev=243342
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/net/third_party/nss/README.chromium?r1=243342&r2=243341&pathrev=243342
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/net/third_party/nss/ssl/exports_win.def?r1=243342&r2=243341&pathrev=243342
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/net/third_party/nss/ssl/sslsecur.c?r1=243342&r2=243341&pathrev=243342
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/net/third_party/nss/ssl/ssl3con.c?r1=243342&r2=243341&pathrev=243342
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/net/third_party/nss/ssl/ssl.h?r1=243342&r2=243341&pathrev=243342
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/net/socket/ssl_session_cache_openssl_unittest.cc?r1=243342&r2=243341&pathrev=243342
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/net/socket/ssl_client_socket_nss.cc?r1=243342&r2=243341&pathrev=243342
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/net/socket/ssl_client_socket_openssl.cc?r1=243342&r2=243341&pathrev=243342
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/net/socket/ssl_session_cache_openssl.cc?r1=243342&r2=243341&pathrev=243342
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/net/url_request/url_request_unittest.cc?r1=243342&r2=243341&pathrev=243342
   M http://src.chromium.org/viewvc/chrome/branches/1750/src/net/socket/ssl_session_cache_openssl.h?r1=243342&r2=243341&pathrev=243342
   A http://src.chromium.org/viewvc/chrome/branches/1750/src/net/third_party/nss/patches/sessioncache.patch?r1=243342&r2=243341&pathrev=243342

Merge 242585 "Defer TLS session caching until after certificate ..."

> Defer TLS session caching until after certificate verification
> 
> BUG=305220
> R=wtc
> 
> Review URL: https://codereview.chromium.org/112183006

TBR=rsleevi@chromium.org

Review URL: https://codereview.chromium.org/126233002
------------------------------------------------------------------------

### in...@chromium.org (2014-01-08)

I think this should just go into m33. Do you think this is worth the risk to take in m32 stable patch 1 or patch 2 ?

### mb...@google.com (2014-02-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-03-04)

Thanks for the report! This one qualifies for a $500 reward. This did not qualify at a higher reward level because of the number of mitigating factors involved.

### cl...@chromium.org (2014-04-14)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-04-15)

Starting payment process.

### ti...@chromium.org (2014-04-18)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you (Req #233622). Thanks again for your help!

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/305220?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078213)*
