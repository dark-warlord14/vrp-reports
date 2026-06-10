# Security: DNS Rebinding on HTTPS

| Field | Value |
|-------|-------|
| **Issue ID** | [40095277](https://issues.chromium.org/issues/40095277) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Network>SSL |
| **Platforms** | Android, Fuchsia, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ta...@computest.nl |
| **Assignee** | ag...@chromium.org |
| **Created** | 2019-06-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

A DNS rebinding attack is possible against a server that uses HTTPS by abusing TLS session resumption.

BACKGROUND  

A DNS rebinding attack works as follows: an attacker \*A\* waits for a user \*C\* to visit the attacker’s website, say <http://attacker.example>. The DNS record for attacker.example initially points to an IP address of the attacker with a low TTL. Once the page is loaded, JavaScript repeatedly attempts to communicate back to <http://attacker.example> using the XMLHttpRequest API. As this is in the same origin, the attacker can influence almost everything about the request and can read almost every part of the response.

The attacker then updates this DNS record to point to a different server (not owned by \*A\*) instead. This means that the requests intended for attacker.example end up at a different server after the record expires, say, server.example owned by \*S\*. If this server does not check the HTTP Host header of the request, then it may accept and process it.

The proper way to prevent this attack is to ensure that web servers verify that the Host header on every request matches a host that is in use by that server. Another workaround that is commonly recommended is to use HTTPS, as the attack as described does not work with HTTPS: when the DNS record is updated and \*C\* connects to server.example, \*C\* will notice that the server does not present a valid certificate for attacker.example, therefore the connection will be aborted.

The most interesting scenarios for this attack involve attacking a device on the network (or even on the local machine) of \*C\*. This is due to a number of reasons, one of which is the problems with HTTPS.

ATTACK  

It is possible to perform a DNS rebinding attack to a HTTPS server by abusing TLS session resumption in a specific way. Contrary to the “normal” DNS rebinding attack, \*A\* needs to be able to communicate with \*S\* to establish a session that \*C\* will later resume. This attack is similar to the Triple-Handshake Attack (3SHAKE) (<https://www.mitls.org/pages/attacks/3SHAKE>), however, the measures that were taken by TLS implementations in response to that attack do not adequately defend against this attack.

Just like in the 3SHAKE attack, \*A\* can set up two connections \*C\* → \*A\* and \*A\* → \*S\* that have the same encryption keys and then pass the session ID or session ticket from \*S\* on to \*C\*. This is known as an “Unknown Key-Share Attack”. Contrary to the 3SHAKE attack, however, \*A\* can update the DNS record for attacker.example before the session is resumed. TLS resumption does not re-transmit the certificate of the server, both endpoints will assume that the certificate is still the same as for the previous connection. Therefore, when \*C\* resumes the connection at \*S\*, \*C\* assumes it has an encrypted connection authenticated by attacker.example, while \*S\* assumes it has sent the certificate for server.example on this connection.

To any web applications running on \*S\*, the connection will appear to be originating from \*C\*’s IP address. If the website on server.example has functionality that is IP restricted to only be available to \*C\*, then \*A\* will be able to interact with this functionality on behalf of \*C\*.

In more detail:

1. \*C\* opens a connection to \*A\*, using client random r1 in the ClientHello message.
2. \*A\* opens a connection to \*S\*, using the same client random r1. \*A\* advertises only the ciphers \*C\* included that use RSA key exchange and \*A\* does not advertise the “extended master secret” TLS extension.
3. \*S\* replies to \*A\* with server random r2 and session ID s in the ServerHello message.
4. \*A\* replies to \*C\* with server random r2 and session ID s and the same cipher suite as chosen for the other connection, but \*A\*’s own certificate. \*A\* makes sure that the extended master secret extension is not enabled here either.
5. \*C\* sends an encrypted pre-master secret to \*A\*. \*A\* decrypts this value using the private RSA key corresponding to \*A\*’s certificate to obtain its value, p.
6. \*A\* also sends p in a ClientKeyExchange to \*S\*, now encrypted with the public key of \*S\*.
7. Both connections finish. The master secret for both is derived only from r1, r2 and p. Therefore, they are identical. \*A\* knows this master secret, so it can cleanly finish both handshakes and exchange data on both connections.
8. \*A\* sends a page containing JavaScript to \*C\*.
9. \*A\* updates the DNS record for attacker.example to point to \*S\*’s IP address instead.
10. \*A\* closes the connections with \*C\* and \*S\*.
11. Due to an XHR request from \*A\*’s JavaScript, \*C\* will reconnect. It receives the new DNS record, therefore it resumes the connection at \*S\*, which will work as it recognizes the session ID and the keys match. As it is a resumption, the certificate message is skipped.
12. JavaScript from \*A\* can now send HTTP requests to \*S\* within the origin of attacker.example.

See the attached image for a diagram of this attack.

Cipher selection  

\*A\* can force the use of a specific cipher suite on the first two connections, assuming both \*C\* and \*S\* support it. It can indicate support for only the desired cipher suite(s) on the connection \*A\* → \*S\* and then select the same cipher suite on the \*C\* → \*A\* connection.

When a session is resumed, the same cipher suite is used as the original connection did. Because \*A\* removed certain cipher suites, the ClientHello that is used for resumption will most certainly indicate stronger ciphers than the cipher the original connection had. A server could detect this and then decide to perform a full handshake instead, because this way a stronger cipher suite would be used. It appears that no servers actually do this.

Extended master secret  

In response to the 3SHAKE attack, the extended master secret (EMS) extension was added to TLS in RFC 7627 (<https://tools.ietf.org/html/rfc7627>). This extension appears to be implemented by most browsers, however, support on servers is still limited. This extension would make the Unknown Key-Share attack impossible, as the full contents of the initial handshake messages (including the certificates) are included in the master secret computation, not just the random values.

The attack is impossible if both client and server support EMS and enforce its usage. However, as server support is limited (browser) clients currently do not require it.

When the extension is not required but supported by both the client and the server, it could be used to detect the above attack and refuse resumption (making the attack impossible as well). If the server receives a ClientHello that indicates support for EMS and which attempts to resume a session that did not use EMS, it must refuse to resume it and perform a full handshake instead.

This is described in RFC 7627 as follows:

```
o  If the original session did not use the "extended_master_secret"  
  extension but the new ClientHello contains the extension, then the  
  server MUST NOT perform the abbreviated handshake.  Instead, it  
  SHOULD continue with a full handshake (as described in  
  Section 5.2) to negotiate a new session.  

```

This is, however, not universally followed by servers. Most notably, we found that IIS indicates support for EMS in the full-handshake ServerHello, but when a ClientHello is received that indicates support for EMS that requests to resume a session that did not use EMS, IIS allows it to be resumed. We also found that one of the larger CDN providers is vulnerable in the same way.

The attack also works when the server does not support EMS, but the client does. The Interoperability Considerations in §5.4 of RFC 7627 only say the following about that:

If a client or server chooses to continue an abbreviated handshake to  

resume a session that does not use the extended master secret, then  

the current connection becomes vulnerable to a man-in-the-middle  

handshake log synchronization attack as described in Section 1.  

Hence, the client or server MUST NOT use the current handshake's  

"verify\_data" for application-level authentication. In particular,  

the client MUST disable renegotiation and any use of the "tls-unique"  

channel binding [RFC5929] on the current connection.

This section only highlights risks for renegotiation and channel binding on this connection. The ability to perform a DNS rebinding attack does not seem to have been considered here. To address that risk, the only option is to not resume connections for which EMS was not used and for which the remote IP address has changed.

Other configurations  

The sequence of handshake messages is different when session tickets are used instead of ID-based resumption, but the attack still works in pretty much the same way.

While the example above used the RSA key exchange, as noted by the 3SHAKE attack the DHE or ECDHE key exchanges are also affected if the client accepts arbitrary DHE groups or ECDHE curves and does not verify that these are secure. Support for DHE is removed in all common browsers (except Firefox) and arbitrary ECDHE curves appears to never have been supported in browsers. TLS 1.3 is not affected, as in that version the EMS extension is incorporated into the design.

SNI also influences the process. On the initial connection, the attacker can pick the name that is indicated for SNI. While a large portion of webservers is configured to reject unknown Host headers, almost no HTTPS servers were found that reject the handshake when an unknown SNI name is received, servers most often reply with a certain “default” certificate. We found that some servers require the SNI name for a resumption to be equal to the SNI name for the original connection. If this is not the case then it may be possible to change the selected virtual host based on the SNI name of the first connection, though we did not find a server configured like this in practice.

It may also be possible for \*A\* to send a client certificate to \*S\* on the first connection, and then attribute the messages sent after the resumption to \*A\*’s identity. We did not find a concrete attack that would be possible using this, but for other protocols that rely on TLS it may be an issue.

The attack as described relies on \*A\* updating their DNS record. Even with a minimal TTL, this may require a long time for all caches to obtain the updated record. This is not required for the attack: \*A\* can include two IP addresses in the in the A/AAAA record, the first being \*A\*’s own address, the second the address of the victim. Once \*A\* has delivered the JavaScript and session ID/ticket, \*A\* can reject connections from the user (by sending a TCP RST response), which means the browser will fall back to the second IP address, therefore connecting to \*S\* instead.

Exploitation  

We wrote a tool to accept TLS connections and perform the attack by establishing a connection to a remote server with the same master secret and forwarding the session ID. By subsequently refusing connections, it was possible to cause browsers to resume its session at the remote server instead.

We have performed this attack successfully against the following browsers:

\* Safari 12.1.1 on macOS 10.14.5.  

\* Chrome 74.0.3729.169 on macOS 10.14.5.  

\* Safari on iOS 12.3.  

\* Microsoft Edge 44.17763.1.0 on Windows 10.  

\* Chrome 74.0.3729.169 on Windows 10.  

\* Internet Explorer 11 on Windows 7.  

\* Chrome 74.0.3729.61 on Android 10.

As mentioned, we also found the following server vulnerable to allowing a resumption of a non-EMS connection using an EMS ClientHello:

\* IIS 10.0.17763.1 on Windows 10.

Firefox is (currently) not vulnerable, as its TLS session storage separates sessions by remote IP address and will not attempt to resume if the IP address has changed. (<https://bugzilla.mozilla.org/show_bug.cgi?id=415196>)

IMPACT  

To summarize, this vulnerability can be used by an attacker to bypass IP restrictions on a web application, provided that the web server:

\* supports TLS session resumption;  

\* does not support the EMS TLS extension (or does not enforce it, like IIS);  

\* can be connected to by an attacker;  

\* does not verify the Host header on requests or the targeted web application is the fallback virtual host;  

\* has functionality that is restricted based on IP address.

As it cannot be determined automatically whether a website has functionality that is IP restricted, we could not determine the exact scale of vulnerable websites. Based on a scan of the top 1M most popular websites, we estimate that about 30% of webservers fulfil the first 2 requirements.

RECOMMENDATION  

TLS clients should not attempt to resume a connection for which the EMS extension was not used and the remote IP address has changed, as it leaves it open to this attack.

TLS servers that implement RFC 7627 should follow the security considerations in that document and refuse to resume a session that did not use EMS if the resumption ClientHello does include the extension.

DISCLOSURE  

As this vulnerability can be exploited quite quickly and affects Chrome, Safari, Internet Explorer and Edge (and in a different way, IIS), we suggest a coordinated disclosure when security updates have been released for all of these products. We suggest publishing this attack 90 days from now, i.e. on September 1, 2019.

We will send a separate disclosure to the CDN provider that does not describe the full attack.

**VERSION**  

Chrome 74.0.3729.169 on macOS 10.14.5.  

Chrome 74.0.3729.169 on Windows 10.  

Chrome 74.0.3729.61 on Android 10.

**CREDIT INFORMATION**  

Reporter credit: Thijs Alkemade from Computest.

## Attachments

- [Rebinding.001.png](attachments/Rebinding.001.png) (image/png, 60.3 KB)
- [iis.pcapng](attachments/iis.pcapng) (application/octet-stream, 6.5 KB)

## Timeline

### ke...@chromium.org (2019-06-03)

[Empty comment from Monorail migration]

### rs...@chromium.org (2019-06-03)

[Empty comment from Monorail migration]

### ag...@chromium.org (2019-06-04)

Thank you for this detailed report.

> TLS clients should not attempt to resume a connection for which the EMS extension was not used and the remote IP address has changed

On first pass, that seems plausible although we will need to consider it more carefully, measure the impact, etc. It's still problematic if an attacker can capture the client's TCP connection and redirect it without the client seeing a different IP address. However, in that case I guess the attacker would very likely be able to meet any IP-based restrictions in any case.

> A server could detect this and then decide to perform a full handshake instead, because this way a stronger cipher suite would be used. It appears that no servers actually do this.

Have you tested Google servers for this property? (I.e. I think our servers, and a number of others, will not resume a session if they would have picked a different cipher suite.)

> we found that IIS indicates support for EMS in the full-handshake ServerHello, but when a ClientHello is received that indicates support for EMS that requests to resume a session that did not use EMS, IIS allows it to be resumed. We also found that one of the larger CDN providers is vulnerable in the same way.

That is quite surprising!

### ta...@computest.nl (2019-06-04)

> On first pass, that seems plausible although we will need to consider it more carefully, measure the impact, etc. It's still problematic if an attacker can capture the client's TCP connection and redirect it without the client seeing a different IP address. However, in that case I guess the attacker would very likely be able to meet any IP-based restrictions in any case.

You can probably gather data on this much better than I could, but I think the impact on client-side performance would be small. As noted elsewhere, Firefox has never attempted to resume at a different remote IP address.

There are scenarios where the client does not actually know the remote IP address (and therefore can't tell that it changed), for example when connecting through a SOCKS5/SOCKS4a proxy with remote DNS, that's indeed something to consider. A scenario where the attacker can capture the packet and redirect it, yet the attacker could not have generated it themselves seems unlikely to me.

I had not realized before that this could also affect Firefox when a SOCKS proxy is in use. I will investigate this further to determine if I should send this report to Mozilla too.


> Have you tested Google servers for this property? (I.e. I think our servers, and a number of others, will not resume a session if they would have picked a different cipher suite.)

Good point, this was a side-note that surprised me, but I hadn't fully investigated it on its own (I shouldn't have formulated it this strongly). Google servers will indeed not accept a resumption if a better cipher could be negotiated by a full handshake. I thought it was rejecting the resumption due to TLS 1.3 fallback protection.


>> we found that IIS indicates support for EMS in the full-handshake ServerHello, but when a ClientHello is received that indicates support for EMS that requests to resume a session that did not use EMS, IIS allows it to be resumed. We also found that one of the larger CDN providers is vulnerable in the same way.

> That is quite surprising!

I forgot that I have a pcap that shows this, I'll attach it. It has 3 ClientHellos from 192.168.56.1 to 192.168.56.101: the first starts a new session without EMS, the second resumes that session with EMS indicated (which the server accepts), the third does a full handshake with EMS (to show that it is supported).

### wf...@chromium.org (2019-06-04)

[Empty comment from Monorail migration]

### da...@chromium.org (2019-06-04)

I would probably only classify this as Low if anything. The only power this gives an attacker is the ability to spoof IP-address-based authentication to a publicly-accessible HTTPS server. That's quite questionable behavior as it is. On top of it, the server needs to have done a host of other things wrong (lack EMS and fail to check the Host header, the latter of which is the usual story for DNS rebinding).

Re the mitigation, we could soften the impact of it (I'm not sure how common EMS is these days) by limiting the mitigation to static RSA rather than ECDHE, but that may be more trouble than is worth it.

### da...@chromium.org (2019-06-04)

Have you reported the IIS EMS bug to Microsoft? That one ought to be fixed.

### ta...@computest.nl (2019-06-04)

Yes, I've sent the same report to Microsoft at the same time, but I haven't heard back yet aside from an auto-response.

### sh...@chromium.org (2019-06-05)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### ta...@computest.nl (2019-06-07)

I've also reported the issue for the scenario where a proxy is in use to Mozilla. If you want to discuss it with them, it has the bugzilla ID 1556937. Apple has also acknowledged receiving the report and has given it the ID 714643497.

### me...@chromium.org (2019-06-11)

Severity=Low per https://crbug.com/chromium/969684#c6.

[Monorail components: Internals>Network>SSL]

### sh...@chromium.org (2019-06-12)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/26cf55a65b24b25def0690a8f8cda954e01d9eb3

commit 26cf55a65b24b25def0690a8f8cda954e01d9eb3
Author: Adam Langley <agl@chromium.org>
Date: Mon Jul 01 21:14:57 2019

Key RSA-KX TLS sessions on the destination IP address too.

(This could allow the normal caching rules when EMS was implemented by
the server but, rather than add complexity here, those servers should
update from using plain RSA.)

BUG=969684

Change-Id: I9d01fbe3613f41308ffd507fa1e8bfcd4813426e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1680926
Reviewed-by: David Benjamin <davidben@chromium.org>
Commit-Queue: Adam Langley <agl@chromium.org>
Cr-Commit-Position: refs/heads/master@{#673820}

[modify] https://crrev.com/26cf55a65b24b25def0690a8f8cda954e01d9eb3/net/socket/ssl_client_socket_impl.cc
[modify] https://crrev.com/26cf55a65b24b25def0690a8f8cda954e01d9eb3/net/socket/ssl_client_socket_impl.h
[modify] https://crrev.com/26cf55a65b24b25def0690a8f8cda954e01d9eb3/net/socket/ssl_client_socket_unittest.cc


### ag...@chromium.org (2019-07-01)

The above change will key RSA sessions by destination IP address. It doesn't care about whether the server supports EMS.

The change is schedule for Chrome 77 but, since we're considering this a low-impact bug, I'm fine with disclosure at any time.

Thanks for reporting.



### sh...@chromium.org (2019-07-02)

[Empty comment from Monorail migration]

### ta...@computest.nl (2019-07-08)

FWIW, those changes look correct to me, I could not reproduce the attack with a recent Chrome Canary build. I've tried a couple of things to bypass it, but those didn't work:

* Negotiating ECDHE first, renegotiating to RSA. Doesn't work as it's not possible to resume a session which was established by renegotiation.
* ECDHE for C -> A, RSA for A -> S. I think it would be possible to establish the same master secret for these connections by selecting two ciphersuites that only differ in the key exchange and RSA encrypting the ECHDE shared secret from the other connection. However, in this case resumption will fail as the resumption's ServerHello indicates a different ciphersuite. Implementations seem to check if this suite matches the previous connection correctly.
* Using non-contributory key shares for Curve25519. BoringSSL seems to properly check fo the all-zero output.



About disclosure, Apple is requesting more time and would like to contact you about it. I will share the bug number with them so they can reference the right issue.

### ag...@chromium.org (2019-07-08)

Thanks for double-checking!

> About disclosure, Apple is requesting more time and would like to contact you about it. I will share the bug number with them so they can reference the right issue.

The Apple folks should already have the right contacts for us but, in case not, please point them my way.

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### ta...@computest.nl (2019-07-23)

As Microsoft has also asked for a delay in disclosure we have agreed to delay our publication until October 8th.

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

Given the other vendors involved, marking as SecurityEmbargo so this doesn't automatically become visible 14 weeks after fix.

### ad...@google.com (2019-09-09)

talkemade@computest.nl - we will be listing this in the release notes for M77. I'm currently going to say "IP address spoofing to servers" per https://crbug.com/chromium/969684#c6, but if you'd like me to obfuscate those few words even more than please do make a suggestion.

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### ta...@computest.nl (2019-09-10)

Will that entry in the release notes show that it is related to the changes committed by Adam in 26cf55a65b24b25def0690a8f8cda954e01d9eb3? If it's not then I think that description is fine. If it is then I think it would be better to obfuscate it a bit more as Apple and Microsoft are still working on fixes.

### na...@google.com (2019-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-30)

Congrats! The Panel decided to reward $500 for this report :) 

### na...@google.com (2019-09-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### aw...@google.com (2020-07-07)

Remove allpublic from bugs that have Restrict-View-SecurityEmbargo

### am...@chromium.org (2021-03-22)

reward unclaimed; donated to charitable organization 

### is...@google.com (2021-03-22)

This issue was migrated from crbug.com/chromium/969684?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2025-05-20)

Opening this one for public disclosure given that the restrictions on this issue were temporarily set back in 2019 for coordinated disclosure purposes. Feels safe to open this up given that this was restricted six years ago.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095277)*
