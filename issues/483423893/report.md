# WebSocketConnector.Connect() passes renderer-controlled site_for_cookies and storage_access_api_status unvalidated, enabling third-party cookie blocking bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [483423893](https://issues.chromium.org/issues/483423893) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Network>WebSockets |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ke...@gmail.com |
| **Assignee** | cf...@chromium.org |
| **Created** | 2026-02-10 |
| **Bounty** | $1,000.00 |

## Description

  WebSocketConnector.Connect() takes site_for_cookies and
  storage_access_api_status as renderer-supplied Mojo parameters. Neither is
  validated against browser-side state before being passed through to the
  network stack.

  Data flow (zero validation at every hop):
    Renderer → WebSocketConnectorImpl::Connect() (websocket_connector_impl.cc:123)
    → NetworkContext::CreateWebSocket() (network_context.cc:1948)
    → websocket_stream.cc:143 url_request_->set_site_for_cookies(site_for_cookies)
    → websocket_stream.cc:148-154 sets kStorageAccessGrantEligible override

  A compromised renderer spoofs site_for_cookies to the target origin and
  storage_access_api_status to kAccessViaAPI, then opens a cross-site WebSocket.
  The network stack treats the connection as first-party with a Storage Access
  grant, bypassing third-party cookie blocking. SameSite=None cookies from the
  target are included in the handshake.

  SameSite=Lax/Strict cookies are NOT affected — the browser-controlled
  initiator_origin still reflects the true cross-site context.

  The codebase already has a browser-controlled alternative ready:
    network_context.mojom:1409-1411:
    "Currently, |isolation_info|'s SiteForCookies field is ignored,
     but it will eventually replace the |site_for_cookies| parameter."

  Fix: use isolation_info.SiteForCookies() and derive storage_access_api_status
  from browser-side permission state.

  Related: RestrictedCookieManager::ValidateAccessToCookiesAt() has the same
  trust issue — site_for_cookies mismatches are LOG(ERROR) only per
  crbug.com/402207912.

  VERSION
  Chrome Version: 143.0.7499.192 stable
  Operating System: Linux (Kali 6.18.3) — bug is platform-independent

  REPRODUCTION CASE
  See attached ws-cookie-bypass-poc.py.

Prerequisites:
  - Chromium 143+ installed (or set CHROMIUM=/path/to/chrome)
  - openssl CLI (for cert generation)
  - Python 3 + websockets (pip install websockets)
  - /etc/hosts: 127.0.0.1 example.test target-domain.example
  - Run: python3 ws-cookie-bypass-poc.py


  Output:
    Phase 1 (control, unmodified forward): 0 cookies — correct
    Phase 2 (spoofed SFC + SAA status): session_none=LEAKED_NONE — bypass

  The PoC uses MojoInterfaceInterceptor to capture a real Connect() message,
  modifies site_for_cookies and storage_access_api_status in-place, and forwards
  through a new WebSocketConnector pipe. Requires --enable-blink-features=MojoJS
  to simulate compromised renderer Mojo access.

Reporter Credit: Richard Belisle


## Attachments

- [ws-cookie-bypass-poc.py](attachments/ws-cookie-bypass-poc.py) (text/x-python, 15.5 KB)
- [ws-session-hijack-poc.zip](attachments/ws-session-hijack-poc.zip) (application/zip, 9.4 KB)

## Timeline

### li...@chromium.org (2026-02-12)

Not too sure this is strictly a security issue, it might be more of a privacy issue, Chris could you confirm if that's an accurate assessment?

### ke...@gmail.com (2026-02-12)

   Howdy.  I certainly understand the 3PC blocking functions as a privacy feature, but in this
  case it's being exploited into the security realm. The impact here is cross-site
  cookie theft from a compromised renderer, a site isolation boundary violation. A
  renderer for attacker.com steals victim.com's SameSite=None cookies via spoofed IPC
  parameters in the WebSocket handshake. The bypass affects SameSite=None cookies
  specifically; Lax/Strict are protected by the browser-controlled initiator_origin.
  However, SameSite=None is the required setting for SSO tokens, federated auth, and
  payment session cookies, making these some of the highest-value targets. A single stolen
  SSO cookie often gives access to every service behind that identity provider for that identity.

   This fits Chrome's compromised renderer threat model: renderer-controlled
  site_for_cookies and storage_access_api_status flow unvalidated into cookie
  inclusion decisions for arbitrary origins. The browser-side
  isolation_info.SiteForCookies exists and is correct but is explicitly ignored.

   The PoC confirms victim.com's cookies are exfiltrated in the WebSocket handshake
  from an attacker.com renderer.

Just my two cents.  -Richard 


### cf...@chromium.org (2026-02-12)

Re: whether a 3rd-party-cookie-blocking-bypass is considered within Chrome's security threat model, there's a (somewhat) recent thread on that [here](https://groups.google.com/a/google.com/g/chrome-security/c/LgDQI-5GJrw/m/RADdawWeBQAJ), with the conclusion that it is not in the security threat model.

With that said, I have a clarification question or two on the PoC (I haven't run it myself):

1. The report says that attacker.com can steal victim.com's SameSite=None cookies via the WebSocket handshake. How does that happen? I.e., how does the compromised renderer actually read victim.com's cookies in the handshake? (If attacker.com can steal victim.com's cookies, that is in Chrome's threat model IIUC, but I'm not seeing that demonstrated here. Maybe I'm missing it.)
2. I *believe* the `storage_access_api_status` part of the bypass is unnecessary. I designed the Storage Access API in Chrome such that `storage_access_api_status` is untrusted (since as you point out, it comes from renderers which may be compromised). The network service [checks](https://crsrc.org/c/components/content_settings/core/common/cookie_settings_base.cc;drc=eb933bd728d3635ed088d5243b4d1733cc04add1;l=839-841) the `storage-access` permission grants (which are managed by the browser process) before cookies are actually accessed in 3P contexts. I.e., supplying a spoofed `storage_access_api_status` is not sufficient to bypass 3P cookie blocking.
   - With that said, if the renderer can supply a 1P `site_for_cookies`, then it can bypass 3P blocking entirely anyway. I'm not familiar enough with the WebSockets architecture to know whether WebSockets currently trust the renderer-supplied `site_for_cookies`.

### ke...@gmail.com (2026-02-13)

Hey, thanks for the thorough breakdown. You're right on the cookie reading piece, 
I was misunderstood. .

I traced through the code after your comment and confirmed: the renderer cannot
read victim.com's cookies from the WebSocket handshake. OnStartOpeningHandshake in
websocket.cc strips Cookie headers when has_raw_headers_access_ is false, and
HasRawHeadersAccess returns false for renderer processes. So no, the attacker
doesn't get to see the cookie values. That was a mistake in my original framing.

The cookies are still included in the HTTP Upgrade request that Chrome sends to    
victim.com. The server receives them and authenticates the connection normally. The
stripping only happens on the way back, when Chrome reports the handshake to the renderer via Mojo.
So the attacker never sees the cookie value, but the connection 
is already authenticated at that point. The WebSocket opens, and the attacker can
send and receive messages as the victim.


I updated my PoC to demonstrate this concretely. From a page at attacker.com with a
compromised renderer:

  1. Spoof site_for_cookies to victim.com via Intercept-Modify-Forward
  2. Chrome attaches victim.com's SameSite=None session cookie to the HTTP Upgrade
  3. The WebSocket opens (readyState=OPEN)
  4. Attacker sends a message and gets back an authenticated response with the
  victim's data

So it's session hijacking rather than cookie theft. The attacker can perform
actions as the victim over the WebSocket without ever seeing the raw cookie.

One important limitation I want to be upfront about: the Origin header is not
spoofed. It correctly shows the attacker's origin. I tested against two servers to
validate this. A server that checks Origin will reject the connection. A server
that doesn't check Origin (authenticates purely via cookies) is fully exploitable.
The PoC demonstrates both cases.

A lot of real-world WebSocket servers don't validate Origin (node.js, etc.) and rely on cookies
alone for auth, especially SSO-authenticated services using SameSite=None cookies.
That's the class of server this affects.

Happy to attach the updated PoC if that would be useful. It's self-contained and
tests both scenarios (with and without Origin checking).  

Apologies for the inaccurate initial submission. - Richard 
.  

### li...@chromium.org (2026-02-13)

Adding some WebSockets owners, can y'all answer if WebSockets trusts renderer supplied `site_for_cookies`?

Also reporter, if you can attach the updated PoC that would be great, thank you!

### ke...@gmail.com (2026-02-13)

Attaching the updated PoC (zip). setup.sh handles /etc/hosts   
and cert setup, then python3 poc.py runs the full demo against 
two WebSocket servers (one that checks Origin, one that        
doesn't).
                                                                 
For the WebSocket owners -- my understanding is that the 
renderer-supplied site_for_cookies in
WebSocketConnector.Connect() passes unvalidated through
WebSocketConnectorImpl::Connect() into
NetworkContext::CreateWebSocket(). The browser-controlled
isolation_info.SiteForCookies() exists but is explicitly not
used yet, with a TODO at network_context.mojom:1409-1411 noting
it will eventually replace the renderer-supplied parameter. Is
that right?  I've been wrong before :)

Thanks y'all. - Richard 

### pe...@google.com (2026-02-13)

Thank you for providing more feedback. Adding the requester to the CC list.

### ri...@chromium.org (2026-02-16)

I think removing the `site_for_cookies` parameter from the WebSocketConnector Connect() mojo API and instead using the one from `isolation_info` would be a correct and sufficient fix.

### dx...@google.com (2026-02-23)

Project: chromium/src  

Branch:  main  

Author:  Chris Fredrickson [cfredric@chromium.org](mailto:cfredric@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7595833>

Remove separate SiteForCookies arg from WebSocketConnector::Connect

---


Expand for full commit details
```
     
    This removes the SiteForCookies arg from WebSocketConnector::Connect, 
    since the impl already has an IsolationInfo which includes a 
    SiteForCookies that ought to be used instead. We also remove the 
    associated plumbing all the way to the callsites of 
    NetworkContext::CreateWebSocket, and update them accordingly. 
     
    Of those callsites, all but WebSocketConnectorImpl::Connect used 
    hardcoded SiteForCookies values that have been preserved or were 
    irrelevant (due to network::mojom::kWebSocketOptionBlockAllCookies). 
     
    Previously, WebSocketConnectorImpl::Connect used a value that was 
    dynamically computed by the renderer. Now, 
    WebSocketConnectorImpl::Connect uses the SiteForCookies from the 
    browser-supplied IsolationInfo (from RenderFrameHostImpl, 
    ServiceWorkerHost, DedicatedWorkerHost, or SharedWorkerHost, as 
    applicable). 
     
    Fixed: 483423893 
    Change-Id: I556f728dfd94f516b89fcabe87c2e38b66ec31ca 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7595833 
    Reviewed-by: Ken Buchanan <kenrb@chromium.org> 
    Commit-Queue: Christian Dullweber <dullweber@chromium.org> 
    Reviewed-by: Adam Rice <ricea@chromium.org> 
    Auto-Submit: Chris Fredrickson <cfredric@chromium.org> 
    Commit-Queue: Chris Fredrickson <cfredric@chromium.org> 
    Reviewed-by: Christian Dullweber <dullweber@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1588717}

```

---

Files:

- M `chrome/browser/net/websocket_browsertest.cc`
- M `components/private_ai/websocket_client.cc`
- M `content/browser/websockets/websocket_connector_impl.cc`
- M `content/browser/websockets/websocket_connector_impl.h`
- M `device/fido/cable/fido_tunnel_device.cc`
- M `device/fido/cable/v2_authenticator.cc`
- M `device/fido/cable/v2_test_util.cc`
- M `device/fido/enclave/enclave_websocket_client.cc`
- M `net/websockets/websocket_channel.cc`
- M `net/websockets/websocket_channel.h`
- M `net/websockets/websocket_channel_test.cc`
- M `net/websockets/websocket_end_to_end_test.cc`
- M `net/websockets/websocket_stream.cc`
- M `net/websockets/websocket_stream.h`
- M `net/websockets/websocket_stream_cookie_test.cc`
- M `net/websockets/websocket_stream_create_test_base.cc`
- M `net/websockets/websocket_stream_create_test_base.h`
- M `net/websockets/websocket_stream_test.cc`
- M `services/network/network_context.cc`
- M `services/network/network_context.h`
- M `services/network/public/mojom/network_context.mojom`
- M `services/network/test/test_network_context.h`
- M `services/network/websocket.cc`
- M `services/network/websocket.h`
- M `services/network/websocket_factory.cc`
- M `services/network/websocket_factory.h`
- M `services/network/websocket_factory_unittest.cc`
- M `third_party/blink/public/mojom/websockets/websocket_connector.mojom`
- M `third_party/blink/renderer/modules/websockets/websocket_channel_impl.cc`
- M `third_party/blink/renderer/modules/websockets/websocket_channel_impl_test.cc`

---

Hash: [e30962b8baf2af0d8f4a09e1d71a4403801d9524](https://chromiumdash.appspot.com/commit/e30962b8baf2af0d8f4a09e1d71a4403801d9524)  

Date: Mon Feb 23 16:12:52 2026


---

### ch...@google.com (2026-02-23)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### cf...@chromium.org (2026-02-23)

I'm triaging this as S3 (low) per <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>, since IIUC:

- The bug requires a compromised renderer as a precondition.
- The bug does not allow an attacker to read or write cookies belonging to another site.
- The bug is a SameSite=Strict & SameSite=Lax cookie bypass (allows an attacker to send 1P requests to an arbitrary victim). However, the SameSite attribute is known to not be fully protected in Chrome (see <https://chromium.googlesource.com/chromium/src/+/master/docs/security/compromised-renderers.md#wip_samesite-cookies>).
- Victim servers are still protected by the `Origin` header which can be used to reject possibly-malicious cross-site WebSocket connections if desired.

For the above reasons, I don't think it's necessary to merge the fix to current stable (M145) or beta (M146).

### ch...@google.com (2026-02-24)

The Found In field may only contain numeric values.
Some values were corrected.
You can see the changes by toggling full history on the issue.

### ch...@google.com (2026-02-24)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483423893)*
