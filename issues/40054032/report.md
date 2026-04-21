# Security: determining size of CORB/CORP'd cross-origin responses

| Field | Value |
|-------|-------|
| **Issue ID** | [40054032](https://issues.chromium.org/issues/40054032) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>CORS, Internals>Network, Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | to...@gmail.com |
| **Assignee** | mm...@chromium.org |
| **Created** | 2020-12-01 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

When a CORB/CORP'd response is received, the browser will signal to the server to stop sending it. For HTTP/1.1 connections, this is done with a TCP FIN/RST packet, but only when a sufficient number of bytes of the response have been received. As such, if fewer bytes have been received, the connection will be kept alive. If more bytes than the threshold have been received, the connection will be killed.

**VERSION**  

Chrome Version: tested on 85.0.4183.121 stable & 89.0.4341.0 canary  

Operating System: tested on macOS 10.15.7, but not OS-specific

**REPRODUCTION CASE**  

Open leak-size.html (e.g. on <https://kul.tom.vg/leak-size-corb.html>) - this sends a (cross-origin) request to my server which will respond with a response of 24235 and 24234 random bytes (note: smaller after compression). In the first case, the threshold is reached and the connection will be closed (checked with another endpoint on the server that has Timing-Allow-Origin: \*). In the second case the connection is kept alive because the threshold was not reached.

This side-channel can be used to perform compression-based side-channel attacks (comparable to BREACH, HEIST - <https://tom.vg/papers/heist_blackhat2016.pdf>)

For mitigation, the browser should respond the same way, regardless of the size of the response (otherwise this introduces a side-channel that can be used to leak the differentiating property - in this case the response size).

**CREDIT INFORMATION**  

Reporter credit: Tom Van Goethem

## Attachments

- [leak-size-corb.html](attachments/leak-size-corb.html) (text/plain, 806 B)
- [get.php](attachments/get.php) (text/plain, 262 B)
- [sblob.txt](attachments/sblob.txt) (text/plain, 48.8 KB)
- [tao.php](attachments/tao.php) (text/plain, 90 B)

## Timeline

### [Deleted User] (2020-12-01)

[Empty comment from Monorail migration]

### mk...@chromium.org (2020-12-01)

+lukasza

[Monorail components: Internals>Sandbox>SiteIsolation]

### mk...@chromium.org (2020-12-01)

[Empty comment from Monorail migration]

### lu...@chromium.org (2020-12-01)

mmenke@, could you please help me figure out how clients/consumers of //net API can control when the connection is closed VS kept alive?  In particular - is it possible to change URLLoader::CompleteBlockedResponse to consistently close the connection (regardless of the size of the response)?  Would it make sense and help if:

1) URLLoader::CompleteBlockedResponse always called |url_request_->CancelWithError(net::ERR_BLOCKED_BY_CLIENT)|?

2) URLLoader::CompleteBlockedResponse always called |url_request_.reset()|?


I am also not sure how to test this aspect of the behavior.  Given this (and lack of familiarity with the //net API), I guess I would be rather happy if somebody from the networking team took over this bug :-).

[Monorail components: Internals>Network]

### lu...@chromium.org (2020-12-01)

Based on the bug report, the bug is not OS-specific.
Based on the bug report, the bug is found in M85 (stable) and M89 (canary)

### mm...@chromium.org (2020-12-01)

There's currently no way to force close a socket after headers are received - net/ keeps the socket open for 5 seconds trying to read the body, and if the body is read in its entirety in 5 seconds (Or if the body is over 16k), if throws away the socket.  Otherwise, it returns the socket to the socket pool.

Giving attackers the ability to effectively flush the socket pool for HTTP/1.1 sites also seems potentially problematic.

### es...@chromium.org (2020-12-01)

Tentatively triaging as Medium severity, since it's a cross-origin info leak but not full SOP circumvention.

### [Deleted User] (2020-12-01)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-02)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2020-12-03)

[+yhirano]

So the numbers here are before compression, and since the body is compressed, they have little relation to what's actually going on internally.

What's going on is this (ignoring the SSL layer and connection establishment):
1)  We read 4k bytes from the socket.
2)  We parse the headers from that, leaving us with 3888 body bytes.
3)  We pass the headers to the caller.
4)  Asynchronously at the network layer: Without waiting, we pass a body pipe to the caller, and write those body bytes to the pipe.
5)  Asynchronously at the network layer: We try to get more buffer space in the IPC buffer.  If we get it, we try to read more data from the socket.  This apparently does not complete.
6)  Asynchronously at the caller layer:  The caller gets the header bytes, and cancels the request, without waiting for the body.
7)  Back in the network layer, The cancel message reaches the HttpNetworkTransaction layer, which creates an HttpResponseBodyDrainer to read a maximum of 16k bytes.  If it reaches the end of the response, then we reuse the socket.  Otherwise, we throw it away.  If there were a pending read, we'd have to throw away the socket.  Since this repros consistently, and only reads 24k bytes from the socket, presumably that generally doesn't happen.

So the attacker can tell whether or not if the response+body was <=24k (compressed bytes, after SSL decoding - chunking overhead affects this a bit weirdly, since it is included in any body bytes in the first 4k read, but not in the 16k read).

If we just removed the HttpResponseBodyDrainer, we'd still have the problem, but we'd be dealing with an 8k limit.

In general, it seems like there's not much we can do about using socket reuse to get timing information, which may imply length.  But in this case, the CORB logic waits exactly until the headers are received, and then cancels the request, which I don't think is a common capability.

One way to fix this is to do the following:
1) Add an optional bool to ResourceRequest.  When set, the URLLoader will wait for a callback from the URLLoaderClient after it has passed along headers, before reading the response body.
2) Make that callback take a bool which, when set, cancels the request and forces the URLRequest to close its socket, if the request is HTTP/1.x (this capability doesn't exist, currently).
3) Make the CORB code use this new API.

It needs to be an optional new stage, because modifying all URLLoader consumers and implementations just isn't feasible, and we probably don't want to add an extra pair of IPC hops to all requests, anyways.  We might be able to restrict access to this API to consumers within the network service, to prevent other consumers from trying to use it (If you have layers of URLLoaders intercepting requests, then the new field won't work for some consumers, because of intermediary interceptors and the like).

I'm not too familiar with the CORB layer, but think the only caller that would need to use this is the CorsURLLoader, at least to fix this particular bug.

There are other options (e.g., add an API to URLLoader to close its socket, but then we couldn't destroy URLLoaders on completion, and we'd need to have URLRequests keep ownership of their sockets until the Mojo pipe had been cleanly closed).

Do we follow redirects for these requests?  We'd still reuse sockets that get redirects, with that proposal.

[Monorail components: Blink>SecurityFeature>CORS]

### to...@gmail.com (2020-12-03)

[Comment Deleted]

### mm...@chromium.org (2020-12-04)

I don't think we can prevent redirect sniffing using a similar pattern (If you want to know if evil.com's request to http:/foo.com/ is redirected to http://bar.com before CORB blocks it, there's nothing we can do - open up 6 connections to bar.com, and see if we close one - not sure if something similar is possible for same origin redirects)

That having been said, I think I have a path forward for CORB, which I hope to get out early next week.  I'm not sure how CORP is hooked up, so it it doesn't piggyback on the CORB path, will either need pointers to fix that, or someone else will need to fix it.

### to...@gmail.com (2020-12-04)

There might be a similar issue with other mechanisms that abort fetching; for instance using an AbortController, or framing resources that have X-Frame-Options. However, the way that connections are reset there does seem different, and seemingly less reproducible than the CORB case. For instance, I notice that the connection is killed when an iframe'd XFO resource of 41761 bytes (compressed, w/o TLS headers) is received; with 1 byte less, the connection is usually kept alive. It seems somewhat dependent on the time that TCP packets are received, and thus possibly subject to jitter (and perhaps not better than what can be achieved with a normal timing attack?).

### mm...@chromium.org (2020-12-04)

The CORB case doesn't look to have any racy calls (my theorizing about IPCs was wrong - I thought it was in the CORS code, but it's closer to the network), so it looks to be completely deterministic, unless reading form the socket doesn't return all bytes because of read sharding on the network/SSL layers due to packet divisions and latency.  Fortunately, that means it's easy to fix.

Looks like we don't block redirect for CORB, but even if we did, redirects would be sniffable without a fair bit more work.

With the other cancellation, I don't think there's any way to wait exactly until headers arrive to cancel the request, which makes them less reliable.

If we want to fix the XFO case, we'll need to update the IPC API to allow a wait before receiving headers and reading the body, so that we can ensure the request keep ahold of the socket and we can force it to close.  I assume we'd need to do the same for the AbortController case, but I'm completely unfamiliar with that API.

Wiring this through all paths (e.g., WebRequest extensions, ServiceWorker) will likely get rather involved and time consuming.  If we want to go down that path, we'll likely need someone else to take it on, since fixing network security issues is tangential to the work I'm doing targeting cross-first-party-site tracking.

I'll defer to the security team on whether they want to invest further resources in this, once I've landed my CL to address the CORB case.

### to...@gmail.com (2020-12-04)

> I don't think there's any way to wait exactly until headers arrive to cancel the request

I think the Promise returned by fetch() resolves when the first byte of the response arrives, so that should be when the headers arrive. Based on some very basic tests, it didn't seem to matter whether the request was cancelled just after the arrival of the headers, or a few ms later.

Regarding detecting redirects: detecting cross-site redirect can be achieved by abusing CSP (e.g. see https://xsleaks.dev/docs/attacks/navigations/#cross-origin-redirects), same-origin redirects can be detected by leveraging the maximum redirect chain length (e.g. see https://docs.google.com/presentation/d/1oczrX2iFZoy0Yohef647y2BsKhEZUVjloMHd7FIxddA/edit#slide=id.gae7bf0b4f7_0_1267) - not sure whether the intention is to mitigate these issues though.

Related to the CORB/P case, there's also COEP that can be abused: https://evil.com defines Cross-Origin-Embedder-Policy: require-corp, any resource without cross-site CORP will then be blocked. The way the socket is reset, seems similar/identical to the CORB/P case. E.g. on https://kul.tom.vg/coep.php running fetch('https://reuse.tom.vg/get1.php?x=16343', {mode: "no-cors", credentials: "include"}) does not reset the connection, whereas fetch('https://reuse.tom.vg/get1.php?x=16344', {mode: "no-cors", credentials: "include"}) does. (get1.php returns a non-CORB'ed response)

### mm...@chromium.org (2020-12-07)

[+shivanisha], for net/ review.

### mm...@chromium.org (2020-12-07)

I've uploaded a putative "fix" at https://chromium-review.googlesource.com/c/chromium/src/+/2575014.

It does not fully resolve the issue. It still lets the following 3 cases be distinguished:

1) Served from cache without revalidation (no change in live connections. Timing attacks would work here, too, presumably).
2) Redirect response or served from cache with revalidation (if there were no idle live connections before, there will be one after the request).
3) A new non-redirect response was received (if there were idle connections before, there is now one less idle connection).

There's not much we can do about 1) being distinguished from the other two, except adding a delay and grabbing a socket from the socket pool (if it has a matching socket - if it has matching busy sockets, we need to wait on getting ownership of one of those), and closing the socket once we have.  I guess one way we could do that would be to restart the request, ignoring any cache entry and wait on an actual response from the server, though that would give the third party a way of clobbering cache entries, which seems not great.  Due to grabbing the entry from the cache an extra time, it may still be slower than 2 or 3 (but then, the same is also possibly true for the case where we try to validate an existing cache entry).

The cases in 2) both release the HttpNetworkTransaction before calling into the URLLoader with headers/redirect information, so the connection has already been returned by the socket pool by the time we learn we want to force close the socket.  If we want to make those cases indistinguishable from 3), we may need a cache expert to figure out how to have the cache layer hold onto HttpNetworkTransaction longer.  I'm not a cache expert, and am not currently planning on tackling that.

We could do something draconian:  Never reuse sockets and never use the cache if we think we might need to block a request with corp/corb, but that seems impractical.  The fundamental issue here is making security decisions when we receive the response, instead of before we make the request.

### mm...@chromium.org (2020-12-07)

Note that the redirect case in 2) only affects CORP, since CORB doesn't block redirects (and thus, redirects are already potentially observable, indirectly - we also directly inform a potentially compromised renderer of the redirect, anyways)

### lu...@chromium.org (2020-12-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2451c8b3410f0b859d0348d119ddf309735d6876

commit 2451c8b3410f0b859d0348d119ddf309735d6876
Author: Matt Menke <mmenke@chromium.org>
Date: Tue Dec 08 22:42:51 2020

Close HTTP/1.1 sockets when blocked by CORB or CORP.

BUG=1154250

Change-Id: Iff9b03523b6265cb7e5ccc0bbbc43dd911ac9b9b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2575014
Reviewed-by: Shivani Sharma <shivanisha@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Cr-Commit-Position: refs/heads/master@{#834909}

[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/http/http_cache_writers.cc
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/http/http_transaction.h
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/http/http_cache_transaction.cc
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/http/http_network_transaction.h
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/services/network/throttling/throttling_network_transaction.h
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/url_request/url_request_context_builder.h
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/url_request/url_request_job.h
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/http/http_transaction_test_util.h
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/url_request/url_request.cc
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/http/http_network_transaction_unittest.cc
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/services/network/throttling/throttling_network_transaction.cc
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/url_request/url_request_job.cc
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/http/http_cache_writers.h
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/http/http_cache_transaction.h
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/services/network/url_loader_unittest.cc
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/services/network/url_loader.cc
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/http/http_transaction_test_util.cc
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/url_request/url_request_http_job.h
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/url_request/url_request_context_builder.cc
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/url_request/url_request_http_job.cc
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/http/http_network_transaction.cc
[modify] https://crrev.com/2451c8b3410f0b859d0348d119ddf309735d6876/net/url_request/url_request.h


### mm...@chromium.org (2020-12-08)

[lukasza]:  Given the caveats in https://crbug.com/chromium/1154250#c17, should we still mark this as fixed?

### mm...@chromium.org (2020-12-08)

Also worth noting the discussion of other, similar leaks being possible if requests are cancelled immediately when headers are received.

### lu...@chromium.org (2020-12-08)

RE: https://crbug.com/chromium/1154250#c21: mmenke@:

I am not sure if I feel qualified to answer this question.  (OTOH, I am not sure who else to check with; maybe we can also check with the reporter?).

FWIW, I _do_ think it is fine to close this bug as fixed:

- The originally reported issue *is* fixed AFAIU

- I am _personally_ not sure if closing _all_ side channels is feasible.  We should try to fix xs-leaks where possible, but IMHO the only ultimate defense is blocking the response at the server-side (via Sec-Fetch-Site validation and/or via CSRF-token validation).

### lu...@chromium.org (2020-12-08)

tomvangoethem@, does marking this bug as fixed sounds reasonable to you?  (see the fix in https://crbug.com/chromium/1154250#c20 + caveats in https://crbug.com/chromium/1154250#c17 + some thoughts in https://crbug.com/chromium/1154250#c23)

### mm...@chromium.org (2020-12-08)

I think it's worth pointing out that this issue is actually about leaks where requests are blocked but information is leaked anyways.  Servers would have to send different responses, or not send responses, in order to handle the cases under discussion here.

### to...@gmail.com (2020-12-08)

If I understand correctly, with this fix it is still possible to determine whether a resource was cached (which was already possible, and I guess would be mainly fixed through cache partitioning), whether it does a cross-origin redirect (currently also possible via CSP), or whether the response was CORB/P'd or not (was also possible before the fix). So all-in-all, a net win in terms of things that can be leaked.

Since the commit message only mentioned HTTP/1.1 connections, does this mean that for HTTP/2 connections there is no change, and just a RST_STREAM frame is sent?

Is there by any chance a built Chrome version available somewhere with this patch included? (I've basically run out of disk space so can't build Chrome right now)

### mm...@chromium.org (2020-12-08)

Correct.  The fix only addresses the ability to detect if body length is greater than a fixed size X when CORP/CORB blocks a request, over HTTP/1.x (Including HTTP/1.x over all types of proxies), and should have no effect on things received over HTTP/2 or HTTP/3.

Looks like https://download-chromium.appspot.com/ serves recent Chromium builds, though it hasn't reached 834909 yet, so doesn't quite have the fix yet.  Maybe give it 30 minutes or an hour?

### to...@gmail.com (2020-12-09)

I can confirm that the fix indeed prevents leaking the response size based on whether the connection was closed or not.

There is still a response size leak based on the time when the connection is closed though. This assumes that the attacker can determine the difference between 1 or 2 round-trip times. For instance, with this code:

await fetch(`https://reuse.tom.vg/tao.php`, {mode: "no-cors", credentials: "include"}); // open connection
let start = performance.now();
await fetch(`https://reuse.tom.vg/get.php?x=16890`, {mode: "no-cors", credentials: "include"});
console.log(performance.now() - start); // 34.645000007003546 (= 1 RTT)
await fetch(`https://reuse.tom.vg/tao.php`, {mode: "no-cors", credentials: "include"}); // open connection again
start = performance.now(); // 
await fetch(`https://reuse.tom.vg/get.php?x=16900`, {mode: "no-cors", credentials: "include"});
console.log(performance.now() - start); // 68.04499996360391 (= 2 RTT)

It seems that the connection is only killed after receiving a packet from the "second" TCP congestion window. The attacker could arbitrarily increment the TCP congestion window by first requesting a larger non-CORB/P'd response (for every ACK that the server receives, the TCP congestion window grows with 1) . It appears that connection are closed in the same as in other mechanisms, so perhaps not specific to this fix. Since it's leaking the size of response *despite* CORB/P, and not *because of* CORB/P, I guess it's maybe out of the scope of this issue?

### mm...@chromium.org (2020-12-16)

[tomvangoethem]:  Sorry for the slow follow-up.

I can reproduce this on Canary on OSX and Windows, but I have to use a larger size for the second request.  Looking at the request times from net-export, the difference looks to be it takes two RTTs to receive enough data for the SSL layer to decode, at which point we get the headers (disclaimer:  I don't know SSL). I was using gets of 10 bytes vs 169000 bytes.

Socket log from the second request (skipping over when it was used from the first request):
t=4465 [st=252]   +SOCKET_IN_USE  [dt=86]
                   --> source_dependency = 13888 (HTTP_STREAM_JOB)
t=4465 [st=252]      SOCKET_BYTES_SENT
                     --> byte_count = 381
t=4465 [st=252]      SSL_SOCKET_BYTES_SENT
                     --> byte_count = 359
t=4550 [st=337]      SOCKET_BYTES_RECEIVED
                     --> byte_count = 296
t=4550 [st=337]      SSL_SOCKET_BYTES_RECEIVED
                     --> byte_count = 274
t=4551 [st=338]      SOCKET_CLOSED
t=4551 [st=338]   -SOCKET_IN_USE

Note that the "SOCKET_BYTES_SENT" events are logged when we successfully write the encrypted to the TCP socket, and the "SSL_SOCKET_BYTES_SENT" are logged when we have successfully the non-encrypted bytes, logged as the SSL layer.  For the received bytes, SOCKET_BYTES_RECEIVED means encrypted bytes read from the socket, and SSL_SOCKET_BYTES_RECEIVED means decrypted bytes extracted from that.

For the fourth request:
t=4804 [st=251]   +SOCKET_IN_USE  [dt=167]
                   --> source_dependency = 13903 (HTTP_STREAM_JOB)
t=4804 [st=251]      SOCKET_BYTES_SENT
                     --> byte_count = 385
t=4804 [st=251]      SSL_SOCKET_BYTES_SENT
                     --> byte_count = 363
t=4889 [st=336]      SOCKET_BYTES_RECEIVED
                     --> byte_count = 1460
t=4889 [st=336]      SOCKET_BYTES_RECEIVED
                     --> byte_count = 1460
t=4890 [st=337]      SOCKET_BYTES_RECEIVED
                     --> byte_count = 5840
t=4890 [st=337]      SOCKET_BYTES_RECEIVED
                     --> byte_count = 4380
t=4890 [st=337]      SOCKET_BYTES_RECEIVED
                     --> byte_count = 1460
t=4970 [st=417]      SOCKET_BYTES_RECEIVED
                     --> byte_count = 1460
t=4970 [st=417]      SOCKET_BYTES_RECEIVED
                     --> byte_count = 2920
t=4970 [st=417]      SSL_SOCKET_BYTES_RECEIVED
                     --> byte_count = 4096
t=4971 [st=418]      SOCKET_CLOSED
t=4971 [st=418]   -SOCKET_IN_USE

So we had to receive 18980 encrypted bytes from the socket before we could extra anything.  I assume this is because of a 16 KB TLS frame/record/whatever.

So...options:
1)  Delay closing the sockets a fixed time on CORB blocking (Or a time in a random range).  The fixed time would likely cause problems if too long, or leak information if too short.
2)  Remove sockets from the pool if we might block something for CORB (or for all requests). This runs into potential issues around socket exhaustion.
3)  Once we block one request for CORB, block all subsequent requests to that origin.
4)  Do nothing.

Open to other ideas.  While I'm happy to talk about potential solutions here or write code if we decide to do something deep in the depths of the network layer, I think someone more knowledgeable about security should take lead here.

### mm...@chromium.org (2020-12-16)

[lukasza]:  Tossing this back to you to determine if we want to add further mitigations on top of CORB.

### to...@gmail.com (2020-12-16)

> I assume this is because of a 16 KB TLS frame/record/whatever

I think this is the case indeed: the client needs to compute MAC checksum on the entire TLS frame before it can be decrypted.

It doesn't seem that the proposed options would mitigate the problem: it doesn't really matter when the connection is closed, what matters is that the attacker can figure out when the decision to block something is made (i.e. time when fetch resolves). 

This issue does not just affect CORB: any other mechanism that results in a measurable & predictable browser action (guess this would typically be to block something) depending on the response headers or first bytes of the response would be affected (e.g. X-Frame-Options). Perhaps it's more convenient if I open a new issue about it, as it's a bit out of scope of the current one?

### lu...@chromium.org (2020-12-16)

RE: c30: mmenke@:

AFAIU, the next step is evaluating the options listed toward the end of https://crbug.com/chromium/1154250#c29 above.

I think we can rule out #3, because subsequent fetches should not be blocked after fetching a 404 image (which will typically return text/html which will be blocked by CORB).

Some notes on viability of #1:
1a. Blocking of images/scripts/stylesheets should be rare (since only html/json/xml/pdf/etc are blocked, such image/script/stylesheet wouldn't work anyway).  Therefore the extra latency shouldn't cause too much of an impact in practice.
1b. I am less sure about, delaying the result/promise of a `fetch('https://example.com/upload', {mode='no-cors'})` API call.  If the response is text/html then it will be blocked by CORB.

Which I think means that we end up with:
Option1: Extra delay: Unsure if feasible (see the previous paragraph)
Option2: Ruled out (see https://crbug.com/chromium/1154250#c29)
Option3: Ruled out (see the 2nd paragraph in the current comment)
Option4: Do nothing


RE: https://crbug.com/chromium/1154250#c28: tomvangoethem@:

I guess that in addition to the size of the response body, an attacker may also be able to determine how long it took to fetch the response headers (even though CORB strips most of the response headers and CORP errors out and doesn't send the response headers at all).

I think that one useful piece of data here would be how much of jitter/randomness would need to be introduced here.  This might inform the decision on whether to proceed with Option1 from https://crbug.com/chromium/1154250#c29.  I'll try asking chrome-security@ about the jitter size, but any feedback is welcomed.

### mm...@chromium.org (2020-12-16)

Sorry, for 1). We'd have to keep the request alive as well as the socket.  In addition to delaying the response, there's also the 6 sockets per origin limit to think about.

### [Deleted User] (2020-12-31)

lukasza: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@chromium.org (2021-01-05)

So far I've tried discussing this bug with 1) chromium-security@ chat and 2) mmenke@.  Some notes below:

*) It seems chromium-security@ consensus is that 1) delaying CORB blocking by a random duration wouldn't in practice affect attacker's ability to use the timing side channel and 2) that we would have to delay CORB blocking by a fixed duration (so that an attacker cannot distinguish 2 CORB-blocked responses based on their timing).

*) The attacker might be able to affect network timings (certainly to their server, but quite possibly also to other servers [e.g. by spamming network resources]).  This ability presents a risk that an attacker might be able to influense/control the CORB blocking delay.  To prevent that, CORB might need to track the *maximum* delay (between A) request start and B) time of CORB blocking).

*) mmenke@ points out that delaying when CORB blocking happens affects not only CORB-blocked-responses, but *all* responses (maybe in the future just the responses within a particular (NIK, target) tuple), because delaying CORB blocking might lead to exhausting available sockets.  This means that delaying when CORB blocking happens would affect more than the timing of broken/empty/CORB-blocked images (or broken/empty/CORB-blocked javascript).  This is concerning - it seems like a pretty big performance risk.  On one hand, this concern might be somewhat mitigated by only delaying for QUIC (where the risk of exhaustion is smaller) and not delaying for HTTP.  On the other hand, once network resources are per-NIK, it seems that the risk of socket exhaustion gets bigger (because the per-NIK socket pool will be smaller than the global socket pool).

*) mkwst@ is skeptical that we can be really effective defending against side channels (and might instead need to ask websites to defend themselves using fetch metadata-based policies).

I am not quite sure what it all means for how to proceed.  Maybe the "do nothing" option is the best option we have?

### mm...@chromium.org (2021-01-05)

So there's global socket pool exhaustion (There's a 256 limit) and a per origin / per-origin+NIK limit (which is 6).  I don't think we need to be too concerned about the global limit, but rather the per origin limit.   Global limit is much smaller for proxies, however (32, I think), so the global limit may come into play when a proxy is in use.

### lu...@chromium.org (2021-01-06)

[Empty comment from Monorail migration]

### lu...@chromium.org (2021-01-13)

I've chatted with nasko@ and we think it should be okay to resolve this bug as WontFix at this time:

1. We think leaving this bug WontFixed is not great, but is also not terrible from security perspective:
    1.1. This only allows leaking of a binary/boolean bit: whether the response was bigger or smaller than X bytes
    1.2. Vulnerable website can protect themselves via server-side blocking (based on Sec-Fetch-Site and/or generic XSRF-protection techniques).

We might revisit this point if we learn about A) attacks in the wild or B) practical attacks against specific sites where the single-bit leak is sufficient to leak more cross-site data.

2. We think that this bug should be marked as WontFix, because the essence of the attack (leaking whether the response was bigger or smaller than X bytes) remains unfixed (even after r834909).

### mm...@chromium.org (2021-01-13)

Lukasza:  Should we open this bug up to the public?  Also, we did land one mitigation.  Not sure if that makes this reward-able or not.

### lu...@chromium.org (2021-01-13)

adetaylor@, I assume that
- this bug will automatically become public after X weeks since resolving it as WontFix
- this bug will be considered by the VRP panel because of the `reward-topanel` label I've just added?

Please shout if these assumptions are incorrect (and also feel free to take another look to vet the decision to resolve the bug as WontFix).

### ad...@chromium.org (2021-01-13)

You're right about it being opened up. As to whether it goes before the VRP panel, I think Sheriffbot might try to prevent that as it was marked as WontFix, but I've manually added it to the docket.

### am...@google.com (2021-01-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2021-01-14)

The VRP panel has decided to award $500 for this report. Someone from our finance team will be in touch. Thanks!

### to...@gmail.com (2021-01-14)

Doesn't the majority of XSLeaks methods leak single-bit information? The valuable information comes from applying it to different endpoints or with different parameters (e.g. XS-Search)?

I think the latter issue (that came up in https://crbug.com/chromium/1154250#c28) is not exactly related to the original report, as it's not limited to CORB/CORP, but rather is caused by the (mis)alignment of TLS records and TCP packets, in particular the initial congestion window. Any observable action that is taken by the browser on the response headers can be used to infer the response size (whether or not it fit in the initial congestion window). While I'm all for using server-side blocking based on Sec-Fetch-* headers, this issue can also be fixed on the server side by starting with smaller TCP record lengths in the beginning of the connection (e.g. see the nginx patch that Cloudflare is running: https://blog.cloudflare.com/optimizing-tls-over-tcp-to-reduce-latency/). I checked the top 100k most popular HTTP/1.1 hosts, and found that for 40.79% the first TLS record containing the response body is smaller than ~14kb (initcwnd); these hosts are not affected by the latter issue (as the blocking always happens after the first bytes of the response have been received).

If I understand correctly, the TLS/TCP alignment had no effect on the originally reported issue that has been fixed in r834909, so this issue had a larger impact than the remaining one.

### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### lu...@chromium.org (2021-01-14)

RE: tomvangoethem@: Doesn't the majority of XSLeaks methods leak single-bit information? The valuable information comes from applying it to different endpoints or with different parameters (e.g. XS-Search)?

I admit that I may be missing some things about XS-Leak / XS-Search attacks - I am always happy to learn more.  I assumed that the attack described by this bug requires that an attacker has quite precise control over the size of the response (so that in an XS-Search attack, the attacker may deduce if the search results matches something or not) and that this level of control (around the threshold for 1 vs 2 TCP round trips) may be difficult to achieve in practice (e.g. that both matched and non-match XS-Search results would be above the threshold).



At any rate, I think that we both agree that even leaking a single byte might be exploited in _some_ situations / against _some_ victim sites (and fixing the side-channel leaks would be important for _these_ sites).  I think that in https://crbug.com/chromium/1154250#c38 and https://crbug.com/chromium/1154250#c35 I am trying to argue that fixing the XS-Leak seems infeasible on the client-side (for this particular leak + possibly in general) - it seems that (per https://crbug.com/chromium/1154250#c35) the only robust defense would carry a significant performance penalty.  And therefore, maybe defenses against the XS-Leak should instead be implemented on the server-side (via Sec-Fetch-Site, etc).  And if we really think that this is the position that Chrome should take, then it seems that we should resolve the bug as WontFix.

Would you agree that server-side blocking (e.g. based on Sec-Fetch-Site) is 1) a robust defense that 2) XS-Search-vulnerable-websites should be able to deploy in practice?  If so, do you think it might be reasonable to focus-on/recommend the robust, server-side defense (given that we don't see an acceptable client-side solution)?

### to...@gmail.com (2021-01-15)

> If so, do you think it might be reasonable to focus-on/recommend the robust, server-side defense (given that we don't see an acceptable client-side solution)?

For the particular issue introduced in https://crbug.com/chromium/1154250#c28 I agree that it should be fixed server-side (ideally using Sec-Fetch metadata, or alternatively by reducing TLS record sizes).

The position that I would like to see Chrome take is to limit side-channel leaks where possible/feasible; as per https://crbug.com/chromium/1154250#c35 and per my own failed attempts to come up with an elegant client-side solution, I think the remaining issue should indeed be marked as WontFix. While the consequence of this remaining issue is similar to the one that was originally reported, the root cause is different. So all in all, I think the outcome is as it should be: the leak that could be fixed was fixed, and the one that can't "easily" be fixed is not.

I think it's important to make a distinction between the two issues: the one originally reported was caused by the Chrome-specific implementation (and could be fixed by adapting the implementation), the other issue, introduced in https://crbug.com/chromium/1154250#c28, is caused by the way that the server sends TLS records to the client, and the fact that the client can only start decrypting & processing them once the entire record has been received. I think that it's a fair assumption that not all (side-)effects caused by parsing the headers can be masked, and therefor the issue can't realistically be mitigated on the client side.

### lu...@chromium.org (2021-01-15)

RE: https://crbug.com/chromium/1154250#c48: tomvangoethem@:

I think you are arguing for 1) resolving the current bug as "fixed" (rather than as "won't fix") and 2) also possibly opening a separate bug for the issue from https://crbug.com/chromium/1154250#c28?  This makes sense - let me tweak the bug status...

### [Deleted User] (2021-01-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-15)

Requesting merge to beta M88 because latest trunk commit (834909) appears to be after beta branch point (827102).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-15)

This bug requires manual review: We are only 3 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2021-01-15)

+adetaylor@ (Security TPM) for M88 merge review,  we already cut M88 Stable RC for Android.  Thank you.

### mm...@chromium.org (2021-01-15)

While I suspect we could merge this fairly safely, I don't think we want to, given its size and complexity.

### ad...@google.com (2021-01-15)

Yes, I'd rather wait till M89.

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### gi...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b55530a59e0de569c58ea96a6fa7235d4d811bf1

commit b55530a59e0de569c58ea96a6fa7235d4d811bf1
Author: Matt Menke <mmenke@chromium.org>
Date: Fri Mar 05 09:03:58 2021

Close HTTP/1.1 sockets when blocked by CORB or CORP.

[M86 Merge]: Dropped changes in url_loader_unittest.cc

BUG=1154250

(cherry picked from commit 2451c8b3410f0b859d0348d119ddf309735d6876)

Change-Id: Iff9b03523b6265cb7e5ccc0bbbc43dd911ac9b9b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2575014
Reviewed-by: Shivani Sharma <shivanisha@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#834909}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2731749
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1562}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/http/http_cache_transaction.cc
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/http/http_cache_transaction.h
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/http/http_cache_writers.cc
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/http/http_cache_writers.h
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/http/http_network_transaction.cc
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/http/http_network_transaction.h
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/http/http_network_transaction_unittest.cc
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/http/http_transaction.h
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/http/http_transaction_test_util.cc
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/http/http_transaction_test_util.h
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/url_request/url_request.cc
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/url_request/url_request.h
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/url_request/url_request_context_builder.cc
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/url_request/url_request_context_builder.h
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/url_request/url_request_http_job.cc
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/url_request/url_request_http_job.h
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/url_request/url_request_job.cc
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/net/url_request/url_request_job.h
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/services/network/throttling/throttling_network_transaction.cc
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/services/network/throttling/throttling_network_transaction.h
[modify] https://crrev.com/b55530a59e0de569c58ea96a6fa7235d4d811bf1/services/network/url_loader.cc


### vs...@google.com (2021-03-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1154250?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>CORS, Internals>Network, Internals>Sandbox>SiteIsolation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054032)*
