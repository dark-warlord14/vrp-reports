# Security: DNS Cache Poisoning through resource exhaustion in Chrome.

| Field | Value |
|-------|-------|
| **Issue ID** | [40052323](https://issues.chromium.org/issues/40052323) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebRTC>Network, Internals>Network>DNS, Internals>Network>QUIC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2008-1447, CVE-2020-6557 |
| **Reporter** | [Deleted User] |
| **Assignee** | er...@chromium.org |
| **Created** | 2020-05-15 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

This vulnerability allows DNS Cache Poisoning through resource exhaustion in  

Chrome. Specifically, a malicious website can exhaust the ephemeral UDP port  

pool of end user operating systems and subsequently allow the attacker to  

poison the victim's local DNS Cache.

A research paper describing the vulnerability is currently work in progress  

and will be submitted to a peer-reviewed journal for publication.

\*IMPORTANT\* TLP:Amber (<https://www.cert.gov.to/?page_id=929>): Please do not  

disclose any information provided within this report on your own. This bug  

does not only affect Google Chrome. To ensure that all affected parties are  

able to investigate and fix the issue prior to publication, we will  

coordinate disclosure of this bug in collaboration with the German Federal  

Office For Information Security - BSI/CERT Bund.

Note: Please allocate a CVE number for this vulnerability and inform us about  

the number for future reference.

The vulnerability combines two techniques:  

(1) a port resource exhaustion vulnerability using WebRTC connection objects  

in JavaScript, and  

(2) out-of-process iframes using a specially constructed HTML file with  

corresponding attacker-controlled server farm to overcome per-process  

limitations.

Ad (1, port resource exhaustion using WebRTC connection objects):

- An attacker creates a RTCPeerConnection object with a modified SDP. The SDP  
  
  is munged to disable channel multiplexing by removing the "a=group:BUNDLE"  
  
  line, and extended by hundreds of media channels.
- By disabling multiplexing, each media channel allocates one or more UDP port  
  
  numbers. Chrome limits the number of connections per process to ca. 3000.
- By including a large number of media channels, a single WebRTC object can  
  
  silently cause a huge number of ephemeral UDP ports to be allocated in the  
  
  operating system.

The proof-of-concept code for this part of the attack is included in the  

attachment, and can be used locally to observe the port allocation up to the  

limit of ca. 3000 ports in a single browser tab.

Note that in theory this attack also works without disabling multiplexing,  

using a large number of WebRTC connection objects. However, a practical  

limitation makes this approach unfeasible: Each connection object consumes  

some CPU time even when idle due to an inefficient (polling) implementation,  

thus causing a DoS on the victim system long before the UDP port pool is  

exhausted. A more efficient WebRTC implementation could make such alternative,  

simpler attacks possible in the future since it would no longer rely on SDP  

offer manipulation to create enough WebRTC connections.

Ad (2, out-of-process iframes):

- To overcome resource limitations imposed by Chrome, the attacker embeds  
  
  multiple instances of the malicious website using out-of-process-iframes.
- By serving each instance of the website via a distinct (IP address, port)  
  
  combination, Chrome is forced to regard each iframe as an unrelated  
  
  site-instance. Each site-instance is properly isolated and assigned an  
  
  individual resource pool. Using six instances of the malicious website,  
  
  each occupying 3000 UDP ports, is enough to exhaust the entire ephemeral  
  
  port pool under Windows 10 (16400 ports).

Once Chrome has exhausted the entire ephemeral port pool of the victim, UDP  

port-randomization is effectively disabled and the operating system becomes  

vulnerable to DNS-Cache Poisoning, causing a client side vulnerability similar  

to a 10-year-old critical vulnerability in the DNS Protocol (DNS Cache  

Poisoning by Dan Kaminsky, see CVE-2008-1447).

Recommended course of action: We recommend to disallow WebRTC connections  

without multiplexing, and/or limiting the number of media streams in a single  

WebRTC connection to a reasonable small amount. We also recommend that the  

number of allocated UDP ports is restricted across all components of Chrome,  

as it is a scarce operating system resource. Otherwise, a resourceful attacker  

could still attempt to exhaust ports by a coordinated attack across multiple  

WebRTC connections, and/or multiple tabs or browser windows, across several  

domains.

Note that in addition to or instead of relying on WebRTC an attacker could  

also utilize HTTP2/QUIC, HTTP3 or other connections using the UDP protocol to  

occupy additional UDP ports.

**VERSION**  

Chrome Version: [81.0.4044.138] + [stable]  

Operating System: [Windows 10 Version 1909 (OS Build 18363.815)]

**REPRODUCTION CASE**  

A full reproduction requires a complex server setup and can not be provided  

in a single non-archive file. We can provide an archive with code,  

configuration files and setup instructions to recreate our environment on  

request. Using our setup, we have successfully poisoned a victim's cache in  

17 seconds. On average, poisoning takes between 4-5 minutes. This shows that  

the vulnerability is exploitable in practice even for attackers with limited  

resources.

**CREDIT INFORMATION**

Reporter credit:  

Matthias Gierlings and Marcus Brinkmann  

(Chair for Network and Data Security at Ruhr-University Bochum)

## Attachments

- [index.html](attachments/index.html) (text/plain, 12.5 KB)
- [artifacts-issue-1083278.tar.gz](attachments/artifacts-issue-1083278.tar.gz) (application/octet-stream, 572.5 KB)
- [chrome_issue_1083278.mp4](attachments/chrome_issue_1083278.mp4) (video/mp4, 7.1 MB)
- [linux_port_exhaustion_wireshark.png](attachments/linux_port_exhaustion_wireshark.png) (image/png, 226.2 KB)
- [kubuntu_normal_operations.png](attachments/kubuntu_normal_operations.png) (image/png, 222.4 KB)
- [kubuntu_exhausted_ports.png](attachments/kubuntu_exhausted_ports.png) (image/png, 194.5 KB)

## Timeline

### ct...@chromium.org (2020-05-15)

[Sheriff] Some initial triage to get some eyes on this. I'll update with more assessment in a bit. Adding Restrict-View-SecurityEmbargo per the reporter's request.

Ryan/Matt, could you take a look at this report or help loop in the right networking folks for this?

Reporter: Could you include the archive with the full setup? It's fine to zip multiple files together for a PoC and upload here.

[Monorail components: Internals>Network>Cache Internals>Network>DNS]

### rs...@chromium.org (2020-05-15)

Adding some tags based on the description, and adding in our resident DNS expert.

As I'm not sure if Monorail's autocc's for components interact negatively with security bugs, holding off adding WebRTC>Network

[Monorail components: -Internals>Network>Cache Internals>Network>HTTP2]

### rs...@chromium.org (2020-05-15)

OK, adding component since https://bugs.chromium.org/p/monorail/issues/detail?id=2527 was fixed :) 

[Monorail components: Blink>WebRTC>Network]

### mm...@chromium.org (2020-05-15)

It's not clear to me how UDP port exhaustion poisons the DNS cache, but if it does, that seems like an issue with the APIs that allow it (WebRTC and QUIC - note that H2 doesn't use UDP, and respects the global connection limit, while QUIC does not), rather than with Chrome's DNS code.

### ma...@ruhr-uni-bochum.de (2020-05-15)

[Comment Deleted]

### ma...@ruhr-uni-bochum.de (2020-05-15)

As requested I'm adding our artifacts to reproduce the issue. If required we can also create some demo videos of the attack and link them here.

### ma...@ruhr-uni-bochum.de (2020-05-15)

@mmenke@chromium.or: The actual poisoning is done by the attacker's sever sending spoofed DNS requests. Under normal circumstances poisoning would not be possible this way, because the attacker can not brute force the 32 Bits of randomness (16-bit transaction ID + 16 bit random UDP port) to forge a DNS Response. However when using WebRTC in Chrome to exhaust the entire ephemeral port pool of Windows 10, DNS Requests will be issued on a fixed port known to the attacker. Only 16-bit of randomness remain from the transaction ID. The attacker can brute-force this very quickly it takes around 4-5 minutes on average to poison a victim cache. We observed much quicker cases though, the fastest so far took 17 seconds.

We are not attacking Chromes DNS code, but we use Chrome to attack the operating system's resolver from the web. Once the Windows' cache has been poisoned
Chrome will be served the malicious entry by the OS.

### ma...@ruhr-uni-bochum.de (2020-05-15)

Attached is a short video file demonstrating the attack.

### mm...@chromium.org (2020-05-18)

Thanks for the clear explanation!  Adjusting labels (Leaving on DNS for now, though not really an issue for the DNS experts).

[Monorail components: -Internals>Network>HTTP2 Internals>Network>QUIC]

### gu...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### ma...@ruhr-uni-bochum.de (2020-05-18)

Concerning this OS-tag "Windows": While our exploit currently is geared towards Windows we have found some indication that other operating systems *may* be vulnerable to a modification of this exploit as well. This could potentially include Chrome OS and older versions of Android that do not use DoH. Unfortunately we don't have the platforms at hand to investigate. Should we involve the Android and Chrome OS team to keep them in the loop?

### ht...@chromium.org (2020-05-18)

This attack seems to be possible whenever you have a mechanism that is able to make the browser consume UDP ports.
The obvious defense would seem to be a browser-wide upper limit to the number of UDP ports allocated by the browser.

I got lost in the levels of indirection here, but noted that rockot@  had been assigned the blame for the code in which I got lost, so CCing him.


### ht...@chromium.org (2020-05-18)

The Right Place might be https://source.chromium.org/chromium/chromium/src/+/master:services/network/p2p/socket_udp.cc;l=70 which has sergeyu@ on the blamelist. Another CC.

### mm...@chromium.org (2020-05-18)

I think we should likely make a per-API limit on UDP ports.  We may well also want global limits on UDP ports as well, but with per-API limits we can, for instance, close idle QUIC UDP sockets when we want to make a new UDP socket, instead of making all QUIC connection attempts fail.  It also reduces the potential to use one UDP API to kill another UDP API.

### mm...@chromium.org (2020-05-18)

Also note that our own stub resolver uses UDP as well, and if we ever want to disable fallback to the platform resolver...We likely don't want QUIC or WebRTC to be able to block its lookups, either.

### ht...@chromium.org (2020-05-18)

If we can make a per-API limit on UDP ports, and can verify that sum(per-API limits) < 16K, that should be safer than an overall <16K limit.
Now that this attack is known, we can expect all UDP-using APIs to be used in the attack, so it's important that we don't miss any.
(I'm a bit surprised the ephemeral port range is 16K not 32K, btw....)


### ct...@chromium.org (2020-05-18)

[Sheriff] Tentatively setting  security labels: This seems like a Severity-High (since DNS poisoning would allow spoofing a site and executing JS as the spoofed origin) and Impact-Stable per the report.

It does seem plausible that this could be adapted to other OSes using the same underlying mechanism, so adding them for now. Reporter: Could you expand a bit on why you think Chrome OS and Android could be affected, and not e.g. Linux or Mac?

### ma...@ruhr-uni-bochum.de (2020-05-18)

Aside from WebRTC, HTTP2/QUIC and HTTP3 another possibility to occupy UDP ports could be the use of RTP, RTSP for instance with the <video> tag. Plugins could be problematic as well. As far as I know WebSockets currently only work over TCP, but if there there any plans for QUIC or UDP-WebSockets they need to be considered. Then there is SSDP, I'm not sure though if that is suitable to open a large number of connections.

### ma...@ruhr-uni-bochum.de (2020-05-18)

@cthomp@chromium.org: It was not my intention to imply that Linux or MacOS are not vulnerable, I explicitly mentioned Chrome OS and Android because both are Google products. If possible it might save some time if we involve these teams here, so they don't have to investigate the whole issue from scratch again.

I have attached a Wireshark trace showing predictable DNS-Query port usage under Linux (the port used for queries to the external DNS Server is not fixed but increases by 2 with every query). This is actually the reason why I believe that Chrome OS and Android may be vulnerable. It is likely that many if not all operating systems are affected and need patches. Even if all issues in Chrome are fixed an attacker may try to use other applications (electron apps, voice chat/videoconferencing software, instant messengers, online games ...) to achieve a similar result. 

### mm...@chromium.org (2020-05-18)

My suggestion:  When making a UDP socket, add a tag based on the creator.  Then if that creator exceeds its global quota, make that UDP socket fail in some way (creation, making a connection, or something) with a new error, ERR_UDP_QUOTA_EXCEEDED or somesuch.  Global quotas are tracked by a singleton and span all NetworkContexts/Profiles.  We can assert the combined per-tag quotas are globally less than some threshold.  We could optionally add some slack into the system (e.g., allow consumers to exceed their quota by up to x, but not allow all consumers collectively to exceed their quotas by y - X could even be set on a per-consumer basis), though I'm not sure that's worth doing.

Additionally, if any consumer want to have its own logic on top of that to close idle sockets on error can do so.  We should hopefully be able to do this for QUIC by doing something similar to what we do for TCP connections.  DNS already throttles requests globally, so shouldn't have issues there.  Not familiar with other consumers.

### mm...@chromium.org (2020-05-18)

One downside of global limits is they do leak data across profiles/NetworkContexts, though we have historically not been too concerned about that sort of global limit leak, though certainly something we should be aware of.

### ct...@chromium.org (2020-05-18)

re: https://crbug.com/chromium/1083278#c19 thanks for clarifying. Since it sounds like the mitigation would be at the WebRTC/QUIC/other API level in Chrome, then this likely does impact all Chrome platforms (except maybe iOS where we are dependent on WebKit, but we may want to track that as an ExternalDependency as well).

### er...@chromium.org (2020-05-18)

Getting to this late after being out for some mini vacation...

A quick explanation from the DNS perspective: DNS port randomization is a security mitigation that helps prevent an attacker from  just sending fake UDP DNS responses in hopes that one will get matched up with a legitimate DNS query and potentially replace the legitimate DNS response.  The idea is that the attacker would have to know or guess both the correct port and the correct 16-bit query ID (also random for each query).  If an attacker can predict the port used for a legitimate query, they would only need to guess (or spam) the 16-bit ID.

Note that an attacker that can intercept to see or manipulate the actual DNS messages is out of scope.  Such an attacker would already completely own UDP/TCP DNS because it's completely unencrypted and unvalidated.  Also out of scope for this attack is DoT and DoH because it's an encrypted connection.

Question: If this bug causes port exhaustion, leading to a much more limited pool of ports for DNS to use, is there a reliable way for the attacker to know what those limited remaining ports are? Even if DNS were limited to always using one port, the attacker would have to know what that port is to get any benefit.

### er...@chromium.org (2020-05-18)

Answering my own question after thinking about it a bit: I think there are ways the attacker could determine the limited port(s) in use.

Suppose if an attacker were probing random ports and IDs, they could potentially use a pool of IPv6 addresses to encode the port used in spoofed results.  Then if they get a connection attempt at one of their controlled IP addresses, by which address is used, they know one of the limited ports in use for DNS.  End result is the attacker only needs to get very lucky and guess the correct port/ID pair once, instead of every time, and after that their odds of making guesses to spoof DNS is greatly increased.

Alternately, since the entire OS is port-limited in this attack, maybe the attacker could control some other non-DNS server that the OS is interacting with using random ports.  The attacker could then use that server to observe what ports are being used.

### ma...@ruhr-uni-bochum.de (2020-05-18)

ericorth@chromium.org: The exploit demonstrated by us reads the free port via JavaScript from the RTCPeerConnection's local description (see webrtc.js) provided in the archive in https://crbug.com/chromium/1083278#c6. It is then leaked through a WebSocket to the attacker.

There is another approach to leak the port. If the attacker operates a DNS Server for his own domain, he can configure a wildcard entry "*.evil.com" on his server and then create XMLHttpRequests with a random prefix to "[random].evil.com". Because of the random prefix this will always miss the local cache and leak the victim's current port.

### ht...@chromium.org (2020-05-18)

Port randomization was always a stopgap; the real defense against cache poisoning is DNSSEC. But that's taking a little while to deploy.....
In order to set a target for how many ports we can allow Chrome to occupy, we need to ask "how many bits of randomness do we need for DNS poisoning defense". It's a pity that Windows already has stolen 2 of our 16 bits by making the ephemereal port range only 16K ports.

If 10 bits are enough, we need to make sure the OS has 1024 ports to play with, and we can let Chrome go to 32600. I kind of feel that we shouldn't take more than half the ephemereal range (there could be other victim apps), so an absolute max limit of 16000 ports sounds about right. That retains 13 bits of randomness.

If (say) there are 6 different eaters of UDP ports in Chrome, we could give each eater a limit of 2000 ports, leaving 4000 ports for future expansion.
Our current per-renderer limit for PeerConnections is 500, and we occasionally hear grumbles that this is too low from the distributed-cache folks. Most PeerConnections don't use more than one UDP port while working (a bit more while negotiating, because Reasons), so a limit of 2000 for UDP ports doesn't sound too constraining. But it's low enough that we need to have tests for what happens when we hit the limit.

Do the numbers seem like they're in the right ballpark?



### mm...@chromium.org (2020-05-18)

Not sure there's anyone on the list who can answer that - we have a per-NetworkContext (basically, per profile) limit of 256 total TCP connections for HTTP/H2, a similar limit for WebSockets, and a limit of 6 UDP sockets globally for DNS.  By those standards, 500 UDP sockets for a single renderer seems excessive.

### er...@chromium.org (2020-05-18)

All the suggestions in this thread around limiting port usage sounds good, but I wonder if it's sufficient or if we're still too vulnerable if an attacker finds similar ways to exhaust ports through other browsers or apps.  Maybe we could mitigate things further by having Chrome pre-reserve a small socket pool (eg 256 ports) exclusively for Chrome DNS.  Then if Chrome heuristically detects that a "random" port is not very random (maybe remember the last 10 or so port numbers used for DNS and check for repeats), we can use a random port from the pool to ensure we at least get the 256 points of entropy.  And as that pool is reserved exclusively for DNS, the ports in the pool wouldn't leak through anything other than DNS.  Doesn't help at all when the system resolver is used, but maybe a helpful mitigation for when Chrome is using its built-in resolver.

### mm...@chromium.org (2020-05-18)

When we receive a DNS response that doesn't match the query, do we fail the request (Or wait for another try), or do we continue waiting for a response?  If we fail, not sure how well that works...though I suppose if we fail the request, that provides some protection from this sort of attack.

### er...@chromium.org (2020-05-18)

If the port doesn't match, I assume the socket code won't match the response up with our UDP request, so Chrome would likely continue waiting.  If the port matches but the ID doesn't match, that would fail the DNS request with ERR_DNS_MALFORMED_RESPONSE, and we'd probably then fallback to the system resolver.

### er...@chromium.org (2020-05-18)

Another possible mitigation if our DNS code detects non-random ports: We switch to starting with a TCP attempt.

### mm...@chromium.org (2020-05-19)

That doesn't help much in the case we're using / falling back to the system resolver, though.

### er...@chromium.org (2020-05-19)

It does not, so it would have to be done in addition to all the port use restriction ideas above to cover when resolution goes out of our control.  But when we're using the built-in resolver, it would help quite a bit as an extra mitigation.  And maybe we could convince OS's to add similar mitigations into their own resolvers.

### ke...@chromium.org (2020-05-19)

Bumping this down to Sev-Medium because DNS attacks are reasonably well-mitigated on most of the web by way of HTTPS.

### ht...@chromium.org (2020-05-19)

From the perspective of DNS attacks, a counter that keeps track of ID mismatches on DNS responses and raises an alarm when it starts racing would probably be more useful than an UDP port limiter; the attack requires a number of ID mismatches for one successful poisoning. (Depending on how the attack is done, I think you can get away with a lot fewer than 2^32 fake responses - but still, that's a lot.)

As long as we're using the OS resolver, that's an OS level problem, but we should keep it in mind if we start using our own resolver.

BTW, http://unixwiz.net/techtips/iguide-kaminsky-dns-vuln.html (a 2008 writeup of the Kaminski attack) claimed that the MS resolver allocated 2500 UDP ports for DNS queries, so that it had a "safe" pool to randomize from. This may or may not be true in 2020.


### ht...@chromium.org (2020-05-19)

Query to #19: Do you know which DNS software is running on the Linux box you were testing this on?
It's probably either dnsmasq or bind - my bet would be dnsmasq, given that bind was around during the Kaminski panic.



### ma...@ruhr-uni-bochum.de (2020-05-20)

https://crbug.com/chromium/1083278#c34: HTTPS requires the attacker to launch a subsequent attack to attack TLS. Many of these attacks are considered hard because they require the attacker to be man in the middle, which is a relatively strong position to begin with. Using this method an attacker starting as a web-attacker can easily upgrade to a man in the middle position. That being said there are many attack vectors that are not covered by HTTPS because once the malicious record is in cache the entire OS is affected, not only the browser. Here are a few examples what an attacker may do without much effort:
- Redirect NTP connections to manipulate system time and have valid certificates or HSTS policies expire
- Perform a downgrade attack on mail server connections using optional STARTTLS to gain access to mail accounts
- Redirect applications with integrated auto updaters or package managers that allow installation of unsigned packages to a malicious server that delivers malware


### ma...@ruhr-uni-bochum.de (2020-05-20)

https://crbug.com/chromium/1083278#c36: The screenshot was made on a Kubuntu 18.04 LTS using systemd-resolved (https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html).

https://crbug.com/chromium/1083278#c35: Once the alarm triggers, the counter measure would be to fallback to TCP? 

### ht...@chromium.org (2020-05-20)

#38: Mitigations should be: Flush the DNS cache, and don't cache until the attack is over. And raise an alert.
Bind also introduced specific rules on what one could use cached additional info for after Kaminski, which helped mitigate the seriousness of the attack; I don't know if others do that.

Checking if systemd-resolved does port randomization under normal circumstances is well worth doing; +2 is not a very random change.

### ma...@ruhr-uni-bochum.de (2020-05-20)

#38 Under normal circumstances systemd-resolved does randomize. I just repeated the experiment with a current version of Kubuntu. The first screenshot shows normal operations, the second one the behavior under port exhaustion.

### ma...@ruhr-uni-bochum.de (2020-05-20)

https://crbug.com/chromium/1083278#c39: Note that flushing the cache upon alert gives an attacker additional control over the victim's cache he did not have previously. The proposed mechanism also flushes benign cache entries, which then have to be looked up again. This gives the attacker another opportunity in case the attack fails or where the victim had the target domain already cached prior to the attack. Of course temporarily disabling the cache will stop the attack as long as the cache stays inactive. But once cache is re-enabled the cache is empty and the attacker has at least a few tries until the alert triggers again. The attacker may also try to throttle the attack to stay below detection threshold at cost of success rate and execution time.  

Another way to counter the proposed detection mechanism may for the attacker to perform additional DNS lookups to his own domain. The log size of mismatched IDs will not be unlimited. Lets say we define 5 mismatches as alert threshold. The attacker can then guess four times risking a mismatch. Next he queries random subdomains [random].evil.com, which are answered with matching ids until the logged mismatches bubble out of the history. Then the attacker has another four tries. From there on it is rinse and repeat.

### ht...@chromium.org (2020-05-20)

https://crbug.com/chromium/1083278#c40: That's interesting - we now have 3 different patterns: Randomization, single-port and increase-port-by-2. Or the increase-port-by-2 behavior might be removed in a recent fix, since you say the last one was run with "a recent version of kubuntu". The Chromium and Android folks should be asked to check whether their current versions have good port randomization behavior, at least.

As to what-to-fix: I still think it's good if Chrome has a global limit to its number of UDP ports, just for general "be a nice customer" reasons, but not sure where in the Chrome code the guard needs to go, or if we need to shard it per port-using client (a single global limit is simpler). The DNS system also needs to be resilient to port exhaustion, but that's not strictly a Chrome issue.







### ma...@ruhr-uni-bochum.de (2020-05-20)

https://crbug.com/chromium/1083278#c42: I think the +2 on the older screenshot may have been an artifact of a situation where the port pool was *almost* exhausted. That could have happened if a few UDP sockets have been occupied by benign processes (for instance telemetry or updates in the background) during the port-blocking phase. Those ports were then freed afterwards leaving a hand full of ports for the resolver to choose from. For the attacker it does not really matter if ports are truly fixed or chosen in another predictable scheme. Once the ports are predictable the attack is possible.

A global limit on UDP ports is definitely a good idea, even though it will come at the cost of a side channel (the number of free/occupied UDP ports). If this
limit is truly global, that metric can be observed cross-origin.

### ht...@chromium.org (2020-05-20)

There is a global limit now: the number of available ports on the system, or (for POSIX systems) ulimit -n (file handles), whichever is smaller. So this is a cross-origin observable property already - but probing the limit will likely cause system disruption, so it's not a very covert side channel.


### ht...@chromium.org (2020-05-20)

[Empty comment from Monorail migration]

### er...@chromium.org (2020-05-20)

Re https://crbug.com/chromium/1083278#c42:
> The Chromium and Android folks should be asked to check whether their current versions have good port randomization behavior, at least.

Speaking for Chrome Browser DNS, I just did a quick doublecheck through the relevant code...

For Windows and Linux, DNS queries for web requests are delegated to the OS, so you'll get whatever port randomization behavior the OS provides.  Note that for Windows, when we do use our built-in resolver (only for stuff like diagnostic probes where spoofing is not a big security concern), no attempt is made to randomize ports in order to avoid triggering firewall warnings.  The socket is connected using what our socket code calls a DEFAULT_BIND, which appears to just connect the socket without a bind() call.

For other platforms, Chrome built-in DNS resolver is used for most web requests, and on all those platforms, it uses what our socket code calls RANDOM_BIND.  It appears that the resulting behavior is that Chrome will make 10 attempts to bind with a randomly generated port number (using base::RandInt(1024, 65535)).  If all 10 attempts result in address-in-use failures, we give up and bind to port 0, taking whatever the OS gives us.

### er...@chromium.org (2020-05-20)

And note that for the "other platforms" behavior, we still fallback to OS resolution on most failures.  So it's still important for the OS to have good port randomization behavior too.

### er...@chromium.org (2020-05-20)

Re https://crbug.com/chromium/1083278#c35:

One concern about detecting ID mismatches is that we'd have to be careful to have a reasonable threshold to avoid reacting too harshly to false positives.  Late legitimate responses to reused ports is something Chrome DNS has seen before.  Historically Chrome has deliberately just ignored mismatched-ID DNS responses instead of immediately failing them just to avoid performance hits on such non-attack cases.  The current behavior of immediately failing on mismatched ID seems to have been added in only a couple years ago and only as a complexity cleanup.

But overall, switching to TCP as primary (but maybe keeping UDP fallback) seems to be a reasonable response on detecting likely spoofing attacks or port exhaustion.  Good protection for only a modest performance hit.  Implementing into Chrome doesn't help us when the OS resolver is used, so not a complete solution unless we can convince everybody to do it, but it's absolutely in our power and a good security mitigation when we use the Chrome built-in resolver.

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### ma...@ruhr-uni-bochum.de (2020-06-02)

@hta@chromium.org: I have two quick questions: Could you grant access to this issue to my colleague lambdafu@gmail.com? Have you already allocated a CVE number for this issue, which we can use for reference?


### er...@chromium.org (2020-06-02)

Activity in this bug has slowed down lately, and nobody has been formally assigned as the primary owner.  What's the status? Does anybody in here feel responsible to own this or have any suggestions on anybody that should be added to be the owner? Somebody from Chrome Security?

Seems to me that there are 3 general areas under discussion:
*Potential fixes to webrtc to avoid the specific methods of port exhaustion
*Wider-picture changes to all port usage within Chrome to keep things under reasonable limits
*Mitigations within our DNS stack, eg switching to TCP on port exhaustion or detected attacks

As the Chrome DNS expert and primary owner of our DNS stack, I can be responsible for handling the mitigations within our DNS stack, but I don't have any relevant expertise on the rest of the issue.

### er...@chromium.org (2020-06-10)

Opened crbug.com/1093361 for the related mitigation work in the Chrome DNS stack.

### gu...@chromium.org (2020-06-10)

Assigning to hta@ to evaluate the WebRTC mitigations.

### [Deleted User] (2020-06-10)

hta: Uh oh! This issue still open and hasn't been updated in the last 21 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@ruhr-uni-bochum.de (2020-06-10)

Could I please get a response to https://crbug.com/chromium/1083278#c50 (Could you grant access to this issue to my colleague lambdafu@gmail.com? Have you already allocated a CVE number for this issue, which we can use for reference?)

### ht...@chromium.org (2020-06-10)

Matthias, could you please give lambdafu's full name? Given the warnings that you placed in the initial report, granting more access to unnamed parties makes me nervous - but since you started this bug, I'm taking your word that he or she is trustworthy.

No, I have not done anything about CVE numbers. That's not something I've previously tried to allocate. Can someone else on the thread take up that one?


### ma...@ruhr-uni-bochum.de (2020-06-10)

https://crbug.com/chromium/1083278#c56: The email address belongs to my colleague Marcus Brinkmann (see reporter credits of our original bug report). We worked together on this issue and also wrote the original issue report together. There is no need to be nervous, he already knows everything we discussed here.

### ma...@ruhr-uni-bochum.de (2020-06-17)

FYI we also reported https://bugs.chromium.org/p/chromium/issues/detail?id=1094876, which we found as a by-product during our research on https://crbug.com/chromium/1083278. It is related to the attack we discuss here.

### ct...@chromium.org (2020-06-23)

[Previous sheriff following up on this...] I've added lambdafu@gmail.com to this bug so they can view and participate (adding others at the request of the reporter is normal practice, so no concerns there). As for CVEs, we only do that in preparation for the fix reaching Stable, if I remember correctly. Security team will handle it as part of the release process.

### ma...@ruhr-uni-bochum.de (2020-06-24)

@cthomp: Thank you for the clarification on the CVE process and both hta and you for adding lambdafu.

### [Deleted User] (2020-06-25)

hta: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-26)

hta: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-28)

hta: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-29)

hta: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-30)

hta: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-01)

hta: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-02)

hta: Uh oh! This issue still open and hasn't been updated in the last 21 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-03)

hta: Uh oh! This issue still open and hasn't been updated in the last 22 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-04)

hta: Uh oh! This issue still open and hasn't been updated in the last 23 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-05)

hta: Uh oh! This issue still open and hasn't been updated in the last 24 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ht...@chromium.org (2020-07-06)

@mmenke: is the tag you're presently adding an appropriate tag to use in your suggestion in #20?


### mm...@chromium.org (2020-07-06)

@hta:  I don't think it is - I think we'd want to separate out QUIC and DNS, for instance, but my tags are per-URLRequest, which is much higher layer, and it seems a bit weird to take a tag for URLRequest but then just throw it out, so calls made directly at the UDP layer can take the tag using the same data structure.

### aw...@google.com (2020-07-07)

Bulk edit: Restrict-View-SecurityEmbargo shouldn't also have Restrict-View-SecurityTeam

### ht...@chromium.org (2020-07-08)

Linux reproduction of basic issue: Load attachment 1 from initial report in a browser window (you can execute this from file:///), and do the Unix command

lsof -i | grep 'UDP \*' | wc -l

to get number of listening ports.
It tops out at 3000, even when running multiple instances of the HTML file.

Version 83.0.4103.116 (Official Build) (64-bit)


### ht...@chromium.org (2020-07-08)

Created https://chromium-review.googlesource.com/c/chromium/src/+/2287311 to get the discussion started on what the proper way to do the limitation is.
Please add yourself as a reviewer to the CL if you want to discuss the code details; comment here on the general principles and on anything that's sensitive.


### ma...@ruhr-uni-bochum.de (2020-07-08)

https://crbug.com/chromium/1083278#c74: You can not reproduce the attack like that. If you execute the code from file, all iframes are same-site and no Site Isolation is applied. Hence you will not be able to occupy enough ports. You have to use the complete setup we provided and host the attacker website on a server as multiple distinct sites (our setup uses distinct ip addresses), otherwise this won't work.

### ht...@chromium.org (2020-07-08)

Re #75: I found an existing test that exercised "create max # of candidates", and it seems to have topped out around 3600 candidates per renderer process, which will create 7200 listening ports (due to not knowing if peer supports RTCP multiplexing or not, there are 2 listening ports per candidate). I think we need to limit the number of ports for Chrome, globally, to something below that, so the test is adequate for checking if the mitigation works or not.

I'll let others take care of DNS-based mitigations; I'm looking at the "limit number of ports allocated" mitigation.


### ht...@chromium.org (2020-07-08)

There is a per-renderer limit (I assume it's per-renderer) for P2P sockets here:

https://cs.chromium.org/chromium/src/services/network/p2p/socket_manager.cc?rcl=367687d808a760c8f3f21972ba24a415f6934f65&l=48

Currently set at 3000 sockets. My PoC CL uses 2000 as the global limit; the per-renderer limit is thus never hit. As part of this work, it should probably be lowered.

### ht...@chromium.org (2020-07-10)

Action plan (Google internal): https://docs.google.com/document/d/1KBrWJXxIgtVHLpFW6QVCBs4rBPlQv9VHmPYwgGSmWAY/edit#
Setting next action to post-vacation.


### mm...@chromium.org (2020-07-10)

SGTM.  Thanks for taking this on!

### ht...@chromium.org (2020-07-11)

[Empty comment from Monorail migration]

### ht...@chromium.org (2020-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### ht...@chromium.org (2020-08-06)

[Empty comment from Monorail migration]

### er...@chromium.org (2020-08-06)

Let's start the mitigation with a Chrome-global limit on UDP sockets:
* This global limit will be Finch controlled so it can be experimentally tuned
* Once the global limit is reached, requests for UDP sockets will be failed

We can start the global limit fairly high, perhaps in the 3000-6000  range.
Will target M86.

This leaves opportunity for finer-grained policies to mitigate denial-of-service. For instance, WebRTC being the specific vector for this attack may also benefit from lower per-renderer, or an additional per-origin limit too. But let's start with the catch-all to address the most pressing aspect.

### er...@chromium.org (2020-08-12)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5a8419292e1833f2dc81c3ab9dcf6a1c2788c121

commit 5a8419292e1833f2dc81c3ab9dcf6a1c2788c121
Author: Eric Roman <eroman@chromium.org>
Date: Thu Aug 13 01:28:25 2020

Add a per-process limit on open UDP sockets.

This adds a default limit of 6000 on the open UDP sockets throughout the entire process, configurable with the "LimitOpenUDPSockets" feature.

An "open UDP socket" specifically means a net::UDPSocket which successfully called Open(), and has not yet called Close().

Once the limit has been reached, opening UDP socket will fail with ERR_INSUFFICIENT_RESOURCES.

In Chrome Browser, UDP sockets are brokered through a single process (that hosting the Network Service), so this is functionally a browser-wide limit too.

Bug: 1083278

Change-Id: Ib95ab14b7ccf5e15410b9df9537c66c858de2d7d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2350395
Reviewed-by: David Schinazi <dschinazi@chromium.org>
Commit-Queue: Eric Roman <eroman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#797523}

[modify] https://crrev.com/5a8419292e1833f2dc81c3ab9dcf6a1c2788c121/net/BUILD.gn
[modify] https://crrev.com/5a8419292e1833f2dc81c3ab9dcf6a1c2788c121/net/base/features.cc
[modify] https://crrev.com/5a8419292e1833f2dc81c3ab9dcf6a1c2788c121/net/base/features.h
[add] https://crrev.com/5a8419292e1833f2dc81c3ab9dcf6a1c2788c121/net/socket/udp_socket_global_limits.cc
[add] https://crrev.com/5a8419292e1833f2dc81c3ab9dcf6a1c2788c121/net/socket/udp_socket_global_limits.h
[modify] https://crrev.com/5a8419292e1833f2dc81c3ab9dcf6a1c2788c121/net/socket/udp_socket_posix.cc
[modify] https://crrev.com/5a8419292e1833f2dc81c3ab9dcf6a1c2788c121/net/socket/udp_socket_posix.h
[modify] https://crrev.com/5a8419292e1833f2dc81c3ab9dcf6a1c2788c121/net/socket/udp_socket_unittest.cc
[modify] https://crrev.com/5a8419292e1833f2dc81c3ab9dcf6a1c2788c121/net/socket/udp_socket_win.cc
[modify] https://crrev.com/5a8419292e1833f2dc81c3ab9dcf6a1c2788c121/net/socket/udp_socket_win.h


### ht...@chromium.org (2020-08-13)

Attempted verification:

reducing the limit to 2000 and running the test fast/peerconnection/RTCPeerConnection-manyCandidates.html (which hits 3000) showed that the result of hitting the limit was a failure of the Listen() function (which ends up calling Bind()) with an error code of -12.

The test succeeded (it actually doesn't verify how many candidates are successfully allocated).



### er...@chromium.org (2020-08-13)

Thanks for verifying @hta! (If I understood #88, you are saying the limit worked right?)

I will post back once this makes it to Canary or Dev channel, at which point there will be an official binary to test.

### ad...@google.com (2020-08-17)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7ae5d573808071418ba5926c2454ead9843d9a51

commit 7ae5d573808071418ba5926c2454ead9843d9a51
Author: Eric Roman <eroman@chromium.org>
Date: Wed Aug 19 00:07:24 2020

Add browsertest verifying that UDP socket limit is enforced by Network Service.

This also moves udp_socket_test_util.cc into the test/ subdirectory, in order to satisfy existing DEPS rules.

Bug: 1083278
Change-Id: I45fd4ceb8b46e0464ff0cd2a41a897efa294f64b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2360125
Reviewed-by: David Schinazi <dschinazi@chromium.org>
Reviewed-by: John Abd-El-Malek <jam@chromium.org>
Commit-Queue: John Abd-El-Malek <jam@chromium.org>
Auto-Submit: Eric Roman <eroman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#799396}

[modify] https://crrev.com/7ae5d573808071418ba5926c2454ead9843d9a51/content/browser/network_service_browsertest.cc
[modify] https://crrev.com/7ae5d573808071418ba5926c2454ead9843d9a51/services/network/BUILD.gn
[modify] https://crrev.com/7ae5d573808071418ba5926c2454ead9843d9a51/services/network/network_context_unittest.cc
[rename] https://crrev.com/7ae5d573808071418ba5926c2454ead9843d9a51/services/network/test/udp_socket_test_util.cc
[rename] https://crrev.com/7ae5d573808071418ba5926c2454ead9843d9a51/services/network/test/udp_socket_test_util.h
[modify] https://crrev.com/7ae5d573808071418ba5926c2454ead9843d9a51/services/network/udp_socket_unittest.cc


### ad...@google.com (2020-08-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-19)

Thanks for the report. The VRP panel has decided to award $5000 for this. Somebody from our finance team will be in touch.

How exactly would you like to be credited? "Matthias Gierlings and Marcus Brinkmann (Chair for Network and Data Security at Ruhr-University Bochum)" is a little longer than we normally allow, but we can fit that in if you really would like. Or is "Matthias Gierlings and Marcus Brinkmann" OK?

I've allocated CVE-2020-6557 here.

Given the complexity of the fix I'm going to propose that we do not want to merge this into M85. I'll add Merge-Rejected-85, otherwise Sheriffbot will shortly add a merge request.

It would be good to know more about the co-ordinated disclosure plans. We will likely release this in M86 which is currently scheduled for October 6th. At that point we will provide a short description in the release notes, and file the CVE description a few days later, which will also be insufficient to exploit this bug. Let us know if you have any concerns there but otherwise we'll assume we can go ahead.

In terms of making this bug itself public, that's up to you. We will remove the label Restrict-View-SecurityEmbargo whenever you want. Normally we'd open it up to downstream Chromium embedders now, then to the public in approximately 14 weeks. We wouldn't normally want to open it to the public much before that, because it gives time for the fix to make it into the hands of most users, but we are open to discussion.

### ma...@ruhr-uni-bochum.de (2020-08-20)

#93 Thank you very much. To shorten the credits a bit we could instead write:
"Matthias Gierlings and Marcus Brinkmann (NDS Ruhr-University Bochum)". Would
that be short enough?

Originally we had planned for disclosure in September. However we have now 
received multiple requests (including yours) for a longer embargo. Our 
national CERT will aid in the coordination of the disclosure process between 
all affected parties. Can you please CC "certbund@bsi.bund.de" for this 
purpose? We will announce the disclosure date here, once we have found a date 
acceptable for everyone involved. Please do not lift the embargo before we 
announced the updated disclosure date here.

We suggest to remove the exploit code provided in the original report and in
#6, before this report becomes publicly visible. 

### ad...@google.com (2020-08-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-20)

Thanks for the shortened credit label; that works!

I've cc'd the CERT email address as requested.

### ad...@google.com (2020-10-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### ds...@chromium.org (2023-02-14)

[Empty comment from Monorail migration]

### li...@chromium.org (2023-02-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2023-03-15)

Can we remove the SecurityEmbargo on this?  It has been nearly 3 years.

### ma...@ruhr-uni-bochum.de (2023-03-15)

Yes you can release the embargo. The issue is public meanwhile[1], you can also remove the restrictions on 1094876 which is related to this issue here.

[1] https://www.usenix.org/conference/usenixsecurity23/presentation/gierlings

### mm...@chromium.org (2023-03-15)

Thanks, Matthias!

### [Deleted User] (2023-03-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1083278?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WebRTC>Network, Internals>Network>DNS, Internals>Network>QUIC]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052323)*
