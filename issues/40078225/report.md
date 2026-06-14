# Security: Don't send encrypted extensions (Channel ID, NPN,OBC) when server certificate is untrusted

| Field | Value |
|-------|-------|
| **Issue ID** | [40078225](https://issues.chromium.org/issues/40078225) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>SSL |
| **Reporter** | ka...@gmail.com |
| **Assignee** | ag...@chromium.org |
| **Created** | 2013-10-10 |
| **Bounty** | $1,000.00 |

## Description

Desktop versions of Chrome currently implement the TLS Channel ID extension, as a follow up to Origin-Bound Certificates (OBC) implemented in earlier versions.

The Channel ID feature generates and presents a unique long-lived browser-specific identifier for each top-level domain that requests it.
Channel IDs are considered privacy sensitive and the specification seeks to protect against both passive and active network attackers [1, sec 6]  by 

(a) encrypting the Channel ID Proof-of-Key-Posession message and 
(b) requiring that this message only be sent if the negotiated ciphersuite is strong enough.

The encrypted message format is borrowed from NPN, where it is used to protect the NextProtocolMessage, and has also been used in the OBC implementation.
However, these privacy protections are completely broken by the way Chrome deals with untrusted server certificates, leading to active network attacks (and subdomain attacks)
that can recover the user's channel ID for arbitrary domains, including google.com

During a TLS Handshake, if Chrome receives an untrusted server certificate (e.g. a self-signed or expired cert or cert for another domain); it does not abort the Handshake.
It will in fact complete the Handshake and then send a fatal alert to close down the connection before it presents the suspicious certificate to the user.
This means that any encrypted extensions (such as Proof-of-Key-Posession in Channel ID, encrypted client certificates in OBC, or the NextProtocolMessage in NPN) will in fact 
be sent encrypted under the untrusted server's public key and can be decrypted by it. 
Notably that this is not a downgrade attack, it is a failure of server authentication.
Even if the client uses TLS 1.2 with the strongest available ciphersuite, the untrusted server will be able to obtain the channel ID.

This handshake behavior in Chrome leads to the following attack scenarios. 
We have implemented demos of these and verified them. We'd be happy to share our code:

1. An active network attacker who can tamper with the DNS cache at a client binds google.com to his own IP address.
   When the Chrome user arrives at the attacker's web server (thinking it is google.com) the server presents an arbitrary 
   self-signed certificate and completes the TLS handshake. 
   During Handshake, Chrome will automatically send the user's google.com Channel ID to the attacker.
   The connection will then be torn down (because of the bad certificate), but the attacker has obtained the user's unique identifier.

2. In the above attack, even if the target server (google.com) did not use Channel ID, a fresh one would have been created
    when connecting to the attacker's server; thus, it is possible for an active network attacker to use Chrome's Channel ID implementation
    to track users even on websites that normally do not use Channel ID. (E.g. it can track Facebook users by their facebook.com ChannelID).

3. A similar attack applies if an attacker can install a server at any subdomain of the target website (https://*.victim.com:*)
   Even if the attacker does not have any valid certificate for this subdomain or for related domain, it will still be able to steal the user's channel ID for victim.com.

Proof of concept
----------------

http://antoine.delignat-lavaud.fr/doc/tls_channel_id_privacy.avi

To try it yourself, set up an openssl server with a self-signed cert and channel id enabled, modify your /etc/hosts to point google.com at the server's IP address.
Open google.com on Chrome. Even though this server will not have google.com's certificate, Chrome will reveal the user's google.com ChannelID to the server.

Impact
------

Channel IDs are long-lived machine identifiers used across all Google servers (including accounts.google.com, googleusercontent.com and doubleclick.net).
As such, they are good candidates for tracking and deanonymising network users. 
The attacks above show that with the current design of Chrome's TLS handshake, these channel IDs can be farmed by any DNS-level 
active attacker or a subdomain attacker.

The important difference between Channel ID and cookies regarding tracking is that over HTTPS, only malicious
websites can tack users with cookies, whereas a DNS/related-domain attacker can track users (even across different
networks) using Channel ID. Thus, enabling Channel ID is a strictly greater privacy threat than enabling cookies.

We have focused on Channel ID in this report, but encrypted messages are also sent in NPN and in TLS-OBC.
Any presumed privacy guarantees for these protocols are also broken by the above vulnerability. 
We include below a list of specs that we are aware of that rely on sending encrypted data before the handshake is finished [1-4]; you may know of others.

As far as we know, False Start is not enabled before the server certificate is verified, but this would be good to check, since in that case, even application data may be leaked to the attacker.

[1] http://tools.ietf.org/html/draft-balfanz-tls-channelid-01 
[2] http://tools.ietf.org/html/draft-agl-tls-nextprotoneg-04
[3] http://tools.ietf.org/html/draft-balfanz-tls-obc-01
[4]  http://tools.ietf.org/html/draft-agl-tls-encryptedclientcerts-00

Fix
---

In a handshake where the server certificate has not been verified, either abort the Handshake, or else disable Channel ID, NPN, and related extensions that rely on encryption.
If, for interoperability, you do need to send the encrypted messages, send dummy messages in their place.


## Timeline

### cl...@chromium.org (2013-10-10)

meacer@: Can you please take a look or find someone else to own it.

### me...@chromium.org (2013-10-10)

This is about TLS extensions, CC'ing the experts again.

### cl...@chromium.org (2013-10-10)

meacer@: Can you please take a look or find someone else to own it.

### in...@chromium.org (2013-10-10)

CF is now fixed and won't try to find owner again. Sorry for c#3.

### ka...@gmail.com (2013-10-10)

Since I filed the report, we've found that the use of channel ID during session resumption (abbreviated handshake) interacts pretty badly with the way Chrome manages sessions with unauthenticated servers.
Essentially, because Chrome will happily resume sessions even if the certificate in the stored session is untrusted (and has not been approved by the user.)
This, along with the current issue described above, leads to an active attack that breaks Channel ID authentication: an attacker can pretend to own a user's channel ID and obtain his channel bound cookies from the server.

Below I summarize the Chrome session storage behavior. We filed this behavior as a bug (https://code.google.com/p/chromium/issues/detail?id=305220), but discussions over there remain inconclusive.
Here, we'll focus on the ramifications to Channel ID, as an addendum to the bug report.

Chrome's Session Management for Unauthenticated Servers
----------------------------------------------------------------------------------
Suppose an active attacker pretends to be google.com
Of course, he does not have google's certificate private key
So he presents a self-signed certificate to Chrome.
As we discussed above, in this case, Chrome will complete the handshake and then tear down the connection.

However, it will also store the session in its session database (while marking the server cert as unauthenticated.)
If the user then reloads the page, Chrome will in fact use the stored session to resume the connection.
The resumption will also complete successfully, but then the connection will again be torn down because of the bad server cert.

In fact, the resumption was quite redundant; since the server cannot even provide a new certificate, it was doomed to fail.
Hence, we believe that this behavior is buggy, and that the session with an unauthenticated server cert should not be used for resumption.
Still, that discussion is for https://crbug.com/chromium/305220.

Crucially, for our current issue, even during resumption, Chrome will send the channel ID, encrypted under the bad server cert.
Moreover, it will send a signature of .the resumption "finished" messages signed with the private key of the channel ID.
This leads to the following attack.

Attack
--------

First, the active attacker plays a man-in-the-middle between the client and google.com.
On the client side, he presents a self-signed certificate and Chrome completes the handshake, storing a session with id I (or ticket T) with a bad server certificate.
On the server side, he manages to set up a session with the same session id and session secrets (same master secret, same random values) [see https://crbug.com/chromium/305220 for details]

Second, when the client next connects to google.com, the active attacker simply proxies the messages to google.com
The client offers a session id to resume (even though the server cert in its session is bad)
Then google.com will accept this resumption (because the attacker set up a session with the same id)
The client will then sign the resumed handshake with its Channel ID for google.com and send it encrypted with its finished message. 

Third, when the resumed handshake completes, Chrome will try to tear down the connection, because of the bad server cert.
At this point, the active attacker takes over the connection, since it has the session keys (master secret and the new client random values)
It sends a request on behalf of the user, and in response the server will send it channel-bound cookies and other channel-bound information.
The active attacker has successfully taken over a TLS connection that is bound to an honest user's channel ID

Demo?
---------
We are working on a proof-of-concept; it is a bit tricky because of all the steps involved.	

Lessons and Fix
-----------------------

In our previous attacks, we focused on the confidentiality of the channel ID, specifically the channel ID public key.

This attack focuses on access control for the channel ID signature; if the client is willing to authenticate (sign) the attacker's TLS connection with his channel ID, then the attacker gets to impersonate the user's channel ID.
The bug/feature of Chrome's session management makes this possible.

The fix remains the same, Channel IDs should not be sent, during initial and abbreviated handshakes, if the server certiifcate associated with the session is not trusted.










On Oct 10, 2013, at 6:46 PM, chromium@googlecode.com wrote:

Updates:
	Status: Unconfirmed
	Owner: ---
	Cc: a...@chromium.org rsleevi@chromium.org pal...@chromium.org
	Labels: -Cr-Platform-Extensions Cr-Internals-Network-SSL

https://crbug.com/chromium/305951#c2 on https://crbug.com/chromium/305951 by meacer@chromium.org: Security: Don't send encrypted extensions (Channel ID, NPN,OBC) when server certificate is untrusted
http://code.google.com/p/chromium/issues/detail?id=305951

This is about TLS extensions, CC'ing the experts again.

-- 
You received this message because you starred the issue.
You may adjust your notification preferences at:
https://code.google.com/hosting/settings

Reply to this email to add a comment.

### rs...@chromium.org (2013-10-10)

[Empty comment from Monorail migration]

### rs...@chromium.org (2013-10-10)

Triaging based on https://crbug.com/chromium/305220

### cl...@chromium.org (2013-10-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-10)

Fixing bug priority based on security_severity-* and releaseblock-* labels.

### ba...@chromium.org (2013-10-10)

[Empty comment from Monorail migration]

### rs...@chromium.org (2013-10-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-10-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-10-12)

[Empty comment from Monorail migration]

### fe...@chromium.org (2013-10-13)

re #7

### ag...@chromium.org (2013-10-14)

Thanks for the report. Will be be addressing this.

### ag...@chromium.org (2013-10-14)

p.s. are you the same group as crbug.com/305220? I note that you've referenced it, but I'm not whether the privacy flags were just set too late. (I've been assuming that you're different people but now I'm wondering.)

### ag...@chromium.org (2013-10-14)

The attack in #5 is very good thanks, but I don't believe that you hit the underlying issue in ChannelID: it signs too little in the case of a resumption handshake. I don't think that you need either Chrome's resumption behaviour in the face of bad certificates nor a MITM to exploit it.

We have our client, an evil server (evil.com) and a good server (good.com). The evil server wishes to authenticate to good.com with the client’s ChannelID.

1. The client makes a connection (with a full handshake) to evil.com and evil.com starts a connection to good.com. The evil server ensures that the nonces and session IDs are the same for both connections by using the client’s nonce when connecting to good.com, and good.com’s nonce and session ID when replying to the client.

2. The evil server returns its true certificates to the client and uses an RSA key exchange with both connections. When the client sends its encrypted pre-master secret to evil.com, evil.com uses the same pre-master secret with its connection to good.com.

3. Now, both the client and the good server have a session cached with the same master secret and session ID. The evil server knows both values.

4. The client connects to evil.com again, this time using the session that it has cached. The evil server TCP forwards the handshake to good.com. The client believes that it’s connecting to evil.com, but will successfully handshake with good.com because both share the same session. The client will sign the handshake with its ChannelID key and now evil.com takes over the connection, using the master secret that it knows.

In the current ChannelID implementation, evil.com and good.com are different eTLD+1’s and so the client will actually sign the handshake with a private key specific to evil.com and not with the key specific to good.com. However, this is a privacy measure that wasn’t intended to be security critical. Also, it can be easily ignored by assuming that the good and evil server are actually evil.example.com and good.example.com. We still shouldn’t accept that servers in the same eTLD+1 can impersonate clients.

As a workaround, we're going to require that ChannelID connections use ECDHE. Resumption connections use the same cipher suite as the original session with our servers so requiring ECDHE should ensure that the attacker cannot choose the master secret. This is a little uncomfortable because it depends on a number of checks that now become security critical: that the DH point be in the correct subgroup. (Otherwise the server could return, say, an invalid point or zero for multiplicative DH.) However, our servers only support P-256 with ECDHE and verify that the point is on the curve, so I believe this is sufficient as a workaround.

(ChannelID isn't actually used for anything important yet, so it'll be 2-3 weeks before this workaround is deployed.)

For a fix, I'm proposing that the ChannelID signature, on a resumption handshake, cover the handshake hashes of the original handshake. For TLS 1.0, 1.1, this will be the SHA-1/MD5 combo. For TLS 1.2, this will be SHA-256 or SHA-384. The hash is extra information that the server and client will store in the session.

(I don't think just using the Finished from the original connection is sufficient because we need collision resistance and it's only 12 bytes.)

This change to ChannelID will be rolled out with a new extension number.


### ka...@gmail.com (2013-10-15)

Hi,

Yes, we are the same research group as 305220 (the reporter there is my student).

Yes, we have in fact hit on exactly the same underlying issue as you suggest, and I have written it up as a critique of the current Channel ID implementation, 
which I was going to send to the Channel ID authors rather than to Chrome since it is a bug in the standard and not in the implementation. 
But since you bring it up, let me summarize our thinking over here.

As you point out, signing the resumption is too weak, since the resumption hashes do not contain enough information. 

1. In particular, it means that Channel ID is currently unable to protect against active network attackers with misissued certificates (even though it is a design goal)
    If the attacker has a misissued certificate for xxx.google.com, he will be able to use the channel id signature on the resumed session to impersonate the user.
2. It also means that if the browser uses the same channel ID for two different web servers, it leads to a *web attack* where one of them could impersonate the other (as you describe)
   This is already the case for different subdomains of the same domain (e.g. *.tumblr.com or *.wordpress.com)

Both attacks rely on the weak integrity guarantees provided by both the RSA key exchange and the session resumption protocol.

These weaknesses in fact leads to an even more general attack on session renegotiation that we have discovered and are writing up for various parties, including Chrome and Microsoft.
I will be happy to discuss that report over email, but since it is not channel ID specific, this may not be the right forum.

Regarding the fixes:

- I buy that session resumption should sign more, and what you suggest may be enough

- However, I don't believe that forcing channelID to use ECDHE seems fragile.

 On the initial connection, the client may well force an ECDHE key exchange with evil.com, 
 but nothing stops evil.com from negotiating RSA with the server, and resending the DH-PMS encrypted under the server's public key.
 So we are again in a situation with two connections having the same keys but different algorithms.

 During resumption, we are now relying on the browser to detect the algorithm change in the ServerHello and reject it.
 Otherwise, since it has the right keys, it could easily just finish the handshake.
 We have written a couple of TLS client implementations and this is the kind of (seemingly redundant) check that is quite easy to miss.

Best,
Karthik

### ka...@gmail.com (2013-10-15)

(Correction: However, I *do* believe that forcing channelID to use ECDHE seems fragile.)


### ka...@gmail.com (2013-10-15)

We've been thinking about the workaround, and we think there is another case where forcing ECDHE may not be enough.  Channel ID has a bad interaction with session caching for False Start.

From what we understand, False Start is enabled for various DH cipher suites, and the way Chrome implements it is that the moment the client sends its finished message, the browser will cache the current session without waiting for the server finished. This is to enable the application to start sending data. (Note that I am assuming here that the server certificate is still properly validated before the session is cached.)

However, this brings back the Channel ID authentication attack, this time for DH ciphersuites.
-----
Phase 1:
C connects to attacker A using ECDHE
A forwards all messages from C to S and from S to C,  except A replaces S's cert with its own cert.
C sends its finished message and caches the session with A.
S sends its finished message and caches its session.
A does not forward the server finished message (it would be invalid) and closes or hangs the connection.
------
Result: C has a cached session for A that has the same session id, keys, and algorithms as a cached session at S
------

------
Phase 2:
C resumes session with A
A forwards all messages from C to S and S to C.
C sends its channel ID for domain A and signs resumption log
C and S complete the abbreviated handshake
------
Result: C and S have a valid connection through A.
            C thinks it is talking to A (and sees A's URL on the address bar)
            S may think it is talking to C's channel ID (if C uses the same channel ID with S and A, see above)
------

The end result is some fairly serious cross-origin violations (cross-frame attacks) where A can read C's channel-bound cookies.

One may argue that the False Start session caching implementation is buggy, in which case that needs to be fixed up for Channel ID to work correctly with the proposed workaround.

Alternatively, we should try to fix up session resumption, which as agl points out, is the culprit here and opens up a number of attacks on client authentication.

Best,
Karthik






### ka...@gmail.com (2013-10-15)

Can you CC google@bouchon.org on this bug?

Thanks,
Karthik

### ag...@chromium.org (2013-10-15)

[Empty comment from Monorail migration]

### ag...@chromium.org (2013-10-15)

Note: in terms of ChannelID authors, Chrome folks and production folks - we're all essentially the same people. The Chromium bug tracker is fine for reaching all of us.

In #18 I think you understood that the client would only negotiate ChannelID when ECDHE is being used. Rather I'm proposing that the *server* only accept ChannelID when ECDHE is being used. (Additionally, our servers will always use the cipher suite from the original handshake when resuming.)

I agree with your attack in #20 and believe that it's stopped by including a hash of the original handshake in the ChannelID signature. At the moment, ChannelID isn't used in a way that makes that problematic as far as I can see. (The presence of a ChannelID is only a check on cookie validity, it carries no authority by itself.) So I think having the server require ECDHE for ChannelID is still a reasonable band-aid while deploying a better fix.

### ka...@gmail.com (2013-10-15)

Ah yes, I see how the fix on the server side would work.
(I forget that you guys also control all Channel ID compatible servers, except maybe tlsinfo.nails.eu.org)

Yes, the hash of the handshake in the Channel ID signature feels like a solid fix. 


### ka...@gmail.com (2013-10-15)

I take it from #23 that this thread is probably going to be the best forum to discuss Channel ID redesigns, so I am copying the email I sent to Dirk, Ryan, and Adam yesterday. This is the report I referred to in #18.

After agl's nice attack description in #17, this will feel a little repetitive, but some of the elements in the report are different, so it may be good to include it on this thread for discussion.

I will note that agl's suggestion that the Channel ID signature should cover a hash of the initial handshake probably solves the problems mentioned in this report. We need to think a bit more about this.

---------

We have been studying the guarantees of Channel ID against various active network attackers and web attackers and
we believe that the protocol does not protect against impersonation attacks from two categories of attackers:

- Subdomain Website Attackers: 
   A website hosted at xxx.W.com can impersonate a user's W.com channel ID at *.W.com
- Active Network Attackers with Misissued Certificates: 
   An active attacker with a valid certificate for xxx.W.com can impersonate an attackers W.com channel ID at *.W.com

Note that these are not privacy leaks, these are full-on impersonation attacks.

As you will see in the traces below, the core vulnerability in the design stems from two components:

1. The RSA key exchange allows a client to have a connection with an attacker that has exactly the same master secret and keys as a connection between the attacker and the server.
     This is certainly well known in the crypto protocols community, but we still continue to get surprised by it in various settings.

2. The session resumption protocol does not authenticate enough details about the original session.
     In particular, it authenticates the master secret but not the client or server credentials.

As a result of 1 and 2, a channel ID signature on the session resumption log is not enough to authenticate the holder of the channel ID and this leads to impersonation attacks.

-----
Phase 1:
Suppose client C connects to an attacker server A using RSA key exchange
A acts as a web-man-in-the-middle between C and S
A forwards C's client hello to S 
A forwards S's server hello to C
A replaces S's certificate with its own
C sends its PMS encrypted under A's public key
C sends its channel ID for domain A and a proof-of-key-posession
A removes the channel ID
A reencrypts the PMS under S's public key and forwards it to S
Both handshakes complete (A has the master secret, so it can finish both handshakes)
-----
Result: C has a new connection+session with A and A has a new connection+session withS
              Both sessions have the same sid, mastersecret, and keys, but are associated to different server certificates
-----

-----
Phase 2:
Suppose client C resumes its connection to the attacker server A.
This time A acts as a transparent proxy and forwards all messages.
C sends its client hello to S via A (with sid, new client random)
S sends its server hello to C via A (with server random)
S finishes the handshake
C sends its channel ID for domain A and a proof-of-key-posession
C finishes the handshake
-----
Result: C has a new connection (same session) with A and A has a new connection (same session) with S
	      A still knows all the keys for both these connections.
	      Crucially, if S accepts C's channel ID and proof-of-key-posession, it will associate the connection to the user, even though the attacker did not know the channel ID private key.
-----

ATTACK:
-------------
Let us consider the conditions under which Phase 2 leads to an impersonation attack.

Suppose the domain of A is the same as the domain of S. This can happen in three cases (at least):

(a) A may be a subdomain website attacker who owns a hosted subdomain xxx.S.com 

(b) A may be an active network (DNS) attacker who binds xxx.S.com to its own IP address and has a misissued certificate for S

(c) A may be an active network (DNS) attacker with an arbitrary certificate but the user agent may be buggy and send the channel ID proof-of-posession anyway (Chrome https://crbug.com/chromium/305951)

Such attackers are part of the threat model of Channel ID and should be considered viable.

Now, why is the proof-of-key-posession accepted by S even though it was sent from C to A?
This is because there is nothing in the session resumption handshake log that indicates that C was sending the channel ID to A.
Notably, session information such as server certificates (or previous channel IDs) are not included in the channel ID signature.

FIX:
-----

The channel ID signature during resumption should include enough information about the initial handshake of the session to be unusable with other connections.

One possibility is to include the hash of the current session's server certificate in the channel ID signature.

For a more general fix, perhaps it would be useful to include the finished messages of the initial handshake (alongside the finished messages for the current handshake)


### ag...@chromium.org (2013-10-15)

The reason why we plan on adding the full handshake hash to the resumption ChannelID signature, rather than the Finished verify_data, is because it looks like we're depending the collision resistance in that case and 96 bits isn't much.

When the evil server is setting up the sessions with both the client and server it can add data to the handshake after the ClientKeyExchange message. In the case of the connection from evil.com to good.com, it can use a NextProtocol message. In the case of the connection from the client to evil.com, it could use the NewSessionTicket message, although that would actually mess things up. However, we cannot depend on the fact that a future TLS extension won’t add a message from server to client in that part of the handshake.

So the evil server can run a collision attack against the 96-bit Finished hash in order to make them equal in the two connections. They have ~50% chance of finding a collision with 2^48 work. Fast, Bitcoin mining hardware can do ~2^40 hashes/sec, intersecting the lists of hashes is likely to be the hard part. None the less, it does not have the security margin that we would like. The attacker may only have 60 seconds or so before a timeout, but they can try many times.

### js...@chromium.org (2013-10-19)

@rsleevi - Active man-in-the-middle is a significant mitigating factor, so this wouldn't exceed medium-severity (assuming the result is a full SSL/TLS compromise). See the reports on CRIME and BEAST for reference.


### ka...@gmail.com (2013-10-19)

[Comment Deleted]

### ka...@gmail.com (2013-10-19)

@jschuh, just a clarification, the attacks described in #17,#18, #20, #25 are not network attacks, they are mounted by a malicious website. 

The attack in #5 is indeed an active network attack, where the attacker needs to tamper (temporarily) with one DNS record at the client, and is then able to get the client to authenticate the attacker's connection with the server. This threat model is perhaps similar to CRIME, but a bit weaker than BEAST.  

### js...@chromium.org (2013-10-19)

Okay, please clarify, because I might have misread some context given number of comments and iterative discussion in this bug. Would one of these attacks allow an origin bypass and/or cookie theft entirely by a malicious website, without the use of any man-in-the middle?

### ka...@gmail.com (2013-10-19)

No, there is no attack here that would make me contest the medium-severity level.  My clarification was primarily to avoid characterizing this issue as an active network attack in the BEAST category.

To summarize the attacks, the worst that could happen is that a related subdomain attacker (at evil.example.com) may obtain the channel-bound cookies of users at (good.example.com) and impersonate them. But as far as I understand, nothing important uses Channel ID right now.

The second worst thing that could happen is that a related subdomain or active network attacker could read a user's Channel ID at various (google) websites and use this to track the user (slightly more effectively than with cookies).






### js...@chromium.org (2013-10-19)

Thanks for the clarification. My intent with the comparison to CRIME and BEAST was to baseline impact rather than draw direct equivalence. Sorry if that confused the discussion.

So, it sounds like medium-severity is right, even though it's a very interesting attack and will be eligible for reward / hall-of-fame.

### cl...@chromium.org (2013-10-24)

agl@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!)

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ka...@gmail.com (2013-10-24)

@agl's proposed fixes in #17, #23, #26 address my concerns on the authentication attacks in #17,#18, #20, #25

But coming back to the original active network attacks in #1, #5, do we have any proposals for stopping the handshake when a bad server certificate is received? Or at least disabling Channel ID in that case?

### ag...@chromium.org (2013-10-24)

Switching from our CAPI inspired model to one where we validate certificates during the callback has been a TODO for a while. We were aware that this could result in disclosure of NPN or ChannelID data to an active attacker.

(Although an active attacker can also control the cipher suite that such data is sent under, although we don't enable any too broken cipher suites.)

An active attacker can also inject HTML and run Panopticlick-style fingerprinting, which is probably even more telling.

So this is lower priority work and there are already a number of things that we know that we also need to do: solve the SSLv3 fallback issue, implement 1/n-1 splitting for Android, implement Certificate Transparency, more work to deploy TLS 1.2, AES-GCM and a ChaCha based ciphersuite, do something about working around F5 bugs etc. So I'm afraid that it falls somewhere in there.

(The priority of this bug reflects the attacks on ChannelID.)

### ka...@gmail.com (2013-10-28)

[Comment Deleted]

### ka...@gmail.com (2013-10-28)

[Comment Deleted]

### ag...@chromium.org (2013-10-28)

It occurs that this attack probably breaks anything that depends on tls-unique channel bindings [1]. Have you considered that direction? I'm not sure what does use them but I think it includes things like some SASL methods[2] and therefore XMPP[3]

[1] https://tools.ietf.org/html/rfc5929#section-3
[2] https://tools.ietf.org/html/rfc5802
[3] https://tools.ietf.org/html/rfc6120#section-13.8.1

### ka...@gmail.com (2013-10-28)

Yes, we're in touch with the channel binding spec authors and some SASL implementers.
tls-unique is thoroughly broken by this attack.

-K.c

### ka...@gmail.com (2013-10-28)

[Comment Deleted]

### an...@gmail.com (2013-10-28)

Yes, we are aware that SASL is broken (aud other similar channel ID mechanisms). We have notified the TLS Bindings working group.

### ka...@gmail.com (2013-10-28)

[Comment Deleted]

### ka...@gmail.com (2013-10-28)

[Comment Deleted]

### ka...@gmail.com (2013-10-28)

[For some reason, this post from yesterday keeps getting deleted; I am trying once more, replacing all references to google by website.com]

I understand that the active attacker scenario for ChannelID is not high priority, and that the website attacker will be mitigated by the proposed changes to the ChannelID spec and implementation.

This leaves one threat mentioned in the ChannelID spec (and its OBC predecessor): website/network attackers with stolen/misissued certificates. From the viewpoint of Chromium, this is probably even lower priority, but since we are discussing changes to the spec on this thread, I think it is worth discussing.

I don't fully understand how ChannelID (or OBC) can protect against such attackers considering the kinds of server-side proxies we've been considering in this thread. Perhaps one of you can clarify.

Consider an attacker A who has obtained/stolen a certificate for x.website.com and is either able to set up a server at x.website.com:NNNN or else controls an access point somewhere.
Then the following trace seems to break ChannelID authentication:
- Client C connects to x.website.com and authenticates with ChannelID
- A accepts the connection using its stolen certificate and returns a page with an embedded frame also sourced at x.website.com
- C connects to A again to load the frame
- This time, A forwards all of C's messages to any page S on *.website.com and forwards all messages back
- C will accept the certificate offered by S (since it covers *.website.com, hence x.website.com)
- C will authenticate with its ChannelID for the google.com TLD, which will be accepted by S
- C will load the mutually authenticated frame from S but its origin will remain x.website.com
- A can now at leisure poke into this frame to impersonate C at S

Am I getting something wrong? I don't see how to protect against such cross-frame attacks.

Best,
Karthik


### ag...@chromium.org (2013-10-28)

karthik: I'm sorry - you may have been hitting the spam filter :( Spam is a bit of a problem on the issue tracker.

At the TLS layer, ChannelID should prevent someone with a misissued certificate from impersonating a client when the server uses (EC)DHE.

However, as you have pointed out, this can be undone at a higher layer if the client will essentially accept instructions from an attacker because of the certificate. However, ChannelID isn't designed exclusively for web browsers - we have a bunch of automated traffic that also goes over TLS connections and, in those cases, there isn't enough flexibility in the client to do something like that. (We hope!) 

### bu...@chromium.org (2013-10-31)

------------------------------------------------------------------------
r232199 | agl@chromium.org | 2013-10-31T20:44:30.609620Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/ssl/ssl_config_service.cc?r1=232199&r2=232198&pathrev=232199
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/ssl/ssl_config_service.h?r1=232199&r2=232198&pathrev=232199
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_server_socket_nss.cc?r1=232199&r2=232198&pathrev=232199
   M http://src.chromium.org/viewvc/chrome/trunk/src/remoting/protocol/ssl_hmac_channel_authenticator.cc?r1=232199&r2=232198&pathrev=232199

net: require forward security for Chromoting SSL/TLS server connections.

BUG=305951

Review URL: https://codereview.chromium.org/46703003
------------------------------------------------------------------------

### in...@chromium.org (2013-10-31)

[Empty comment from Monorail migration]

### ag...@chromium.org (2013-10-31)

[Empty comment from Monorail migration]

### an...@gmail.com (2013-11-04)

As mentioned in https://crbug.com/chromium/305220, NSS allows to use <p,g,p-1> in the DHE server key exchange (NSS bug https://bugzilla.mozilla.org/show_bug.cgi?id=934545) which means that the same issue can occur on some servers that use DHE. We have not yet checked that ECDHE parameters are properly verified in major TLS implementations.

### rs...@chromium.org (2013-11-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-13)

Fixing impact labels.

### [Deleted User] (2013-11-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-11-15)

------------------------------------------------------------------------
r235344 | agl@chromium.org | 2013-11-15T16:13:28.533240Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_server_socket_nss.cc?r1=235344&r2=235343&pathrev=235344

Only use ECDHE when requiring forward secrecy.

BUG=305951
R=wtc@chromium.org

Review URL: https://codereview.chromium.org/72683005
------------------------------------------------------------------------

### bu...@chromium.org (2013-11-18)

------------------------------------------------------------------------
r235826 | agl@chromium.org | 2013-11-18T22:00:04.102568Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/ssl3con.c?r1=235826&r2=235825&pathrev=235826
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/sslnonce.c?r1=235826&r2=235825&pathrev=235826
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/ssl3ext.c?r1=235826&r2=235825&pathrev=235826
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/sslimpl.h?r1=235826&r2=235825&pathrev=235826
   A http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/patches/channelid2.patch?r1=235826&r2=235825&pathrev=235826
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/ssl/sslt.h?r1=235826&r2=235825&pathrev=235826
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/patches/applypatches.sh?r1=235826&r2=235825&pathrev=235826
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/third_party/nss/README.chromium?r1=235826&r2=235825&pathrev=235826

Support new ChannelID extension.

This change switches over to use the new-style ChannelID extension.

BUG=305951

Review URL: https://codereview.chromium.org/27589002
------------------------------------------------------------------------

### cl...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-21)

Medium Severity Bugs should not need this label. This is only for high+ severity bugs.

### cl...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-01-01)

is there work remaining in this bug. i see cls in c#53, c#54.

### rs...@chromium.org (2014-01-02)

inferno: There's longer term clean-up necessary, but the issue itself is resolved.

### in...@chromium.org (2014-01-02)

Closing based on c#59. This helps to trigger merge process. Longer term clean-up should be tracked in a seperate functional bug.

### cl...@chromium.org (2014-01-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-01-08)

[Empty comment from Monorail migration]

### ka...@google.com (2014-01-08)

can this wait until stable 2 for M32? we're cut with stable1

### la...@google.com (2014-01-08)

Leaving the Merge-Request for M-32, however we cut M33 at 241107, which comprehensively should have all the CLs referenced in this issue.

### ag...@chromium.org (2014-01-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-10)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-04-14)

My apologies for the delay here - $1000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-23)

Processing via our e-payment system can take up to 30 days, but the reward should be on its way to you. Please do NOT publicly disclose details until a fix has been released to all our users. Thanks again for your help!


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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/305951?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078225)*
