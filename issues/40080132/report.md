# Security: SPDY connection sharing logic errors allows for MITM

| Field | Value |
|-------|-------|
| **Issue ID** | [40080132](https://issues.chromium.org/issues/40080132) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>HTTP2, Internals>Network>SSL |
| **Reporter** | ag...@chromium.org |
| **Assignee** | rc...@chromium.org |
| **Created** | 2014-07-30 |
| **Bounty** | $1,000.00 |

## Description

Antoine Delignat-Lavaud from INRIA reports:

1) That we are connection pooling requests to bad certificates (i.e. ones that the user clicked through an interstitial for). As I recall, we intended for bad certs not to be pooling candidates but we may have missed the check.

(As an attack: give the victim an invalid cert for a captive portal site (https://captiveportal.com) that they click through. Speak SPDY or HTTP/2 and have SANs for example.com on that cert and fake DNS in order to get https://bank.com requests pooled onto that connection)

2) That connection pooling bypasses pinning. I think we might have simply missed this in the past. I believe that we need to add another condition to the pooling rules that we never pool across pinning domains. I hope TransportSecurityState is to hand when we make these decisions. If so, we might want to add an "IsEqualPinning" function to it that takes two hostnames and compares whether they have equal pins. For preloaded pins this is easy. For dynamic pins we can compare the pinsets, although we would then be depending on the fact that we require HPKP pins to include the current, good cert. This was previously just a footgun-amelioration measure.

## Attachments

- [spdy4.png](attachments/spdy4.png) (image/png, 61.8 KB)
- [spdy2.png](attachments/spdy2.png) (image/png, 48.6 KB)
- [spdy1.png](attachments/spdy1.png) (image/png, 57.8 KB)
- [spdy3.png](attachments/spdy3.png) (image/png, 58.3 KB)

## Timeline

### rs...@chromium.org (2014-07-30)

Do they have more details?

I don't understand the first point - it seems like conflating session caching with con section pooling. The two are somewhat orthogonal in their risks. We have always used the connection pools (HTTP keepalive, SPDY sessions) if the user has clicked through, but we remember the tainted state.

I suspect 2 is true for SPDY, because of its whole check to see if the cert contains other names its valid for, but it shouldn't be for HTTP, because the host/port tuple is the identity key in the con section pools. Even on session resumption, we still perform a pin check and cert validation.

### rs...@chromium.org (2014-07-30)

[Empty comment from Monorail migration]

### ag...@chromium.org (2014-07-30)

Antoine provided net-internals screenshots that I've attached here.

I don't think this is conflating the normal connection pools, although I might have the wrong name. I mean the the SPDY / HTTP/2 behaviour of merging requests to different domains into the same connection.

### wi...@chromium.org (2014-07-30)

[Empty comment from Monorail migration]

### wi...@chromium.org (2014-07-30)

Yeah, this is unfortunate =/

### rs...@chromium.org (2014-07-30)

[Empty comment from Monorail migration]

### rc...@chromium.org (2014-07-30)

I'll run with this. I think I understand the mitigation for #2 (checking the pins via TransportSecurityState). However, I don't understand know how to determine if, say, the SSLInfo for a SPDY connection indicates that the interstitial was clicked through? Can someone point me in the right direction there?

### rs...@chromium.org (2014-07-30)

@rch: I don't think #2 will be as simple as you mention. There's a reasonable amount of logic/complexity associated with pin checking that we don't want do just duplicate. That's the second part of https://crbug.com/chromium/391035 - filed for OpenSSL, but presumably applies here as well. I'm adding David, because I was just talking to him about this refactoring yesterday.

Regarding your point on 1, the SSLInfo doesn't track that. Well, other than you'll have an error status for the bits expressed in the CertStatus. The SSLConfig will tell you, by virtue of allowed_bad_certs. See https://code.google.com/p/chromium/codesearch#chromium/src/net/socket/ssl_client_socket_nss.cc&rcl=1406663800&l=3374 to understand what differentiates the two sockets.

### ag...@chromium.org (2014-07-30)

(cc'ing the reporter.)

### wi...@chromium.org (2014-07-30)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-07-30)

[Empty comment from Monorail migration]

### rc...@chromium.org (2014-07-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d7a7076b1b15ad982e40c02052dc60331b216623

commit d7a7076b1b15ad982e40c02052dc60331b216623
Author: rch@chromium.org <rch@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Jul 30 21:25:27 2014

Disable SPDY and QUIC session pooling.

BUG=398925
R=agl@chromium.org

Review URL: https://codereview.chromium.org/417013005

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@286598 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-30)

------------------------------------------------------------------
r286598 | rch@chromium.org | 2014-07-30T21:25:27.824824Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session_test.cc?r1=286598&r2=286597&pathrev=286598
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.cc?r1=286598&r2=286597&pathrev=286598
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory_test.cc?r1=286598&r2=286597&pathrev=286598
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=286598&r2=286597&pathrev=286598
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_unittest.cc?r1=286598&r2=286597&pathrev=286598
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.cc?r1=286598&r2=286597&pathrev=286598

Disable SPDY and QUIC session pooling.

BUG=398925
R=agl@chromium.org

Review URL: https://codereview.chromium.org/417013005
-----------------------------------------------------------------

### bu...@chromium.org (2014-07-30)

------------------------------------------------------------------
r286615 | rch@chromium.org | 2014-07-30T22:24:12.795900Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/spdy/spdy_session.cc?r1=286615&r2=286614&pathrev=286615
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/quic/quic_client_session.cc?r1=286615&r2=286614&pathrev=286615
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/quic/quic_stream_factory_test.cc?r1=286615&r2=286614&pathrev=286615
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=286615&r2=286614&pathrev=286615
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/spdy/spdy_session_unittest.cc?r1=286615&r2=286614&pathrev=286615

Merge 286598 "Disable SPDY and QUIC session pooling."

> Disable SPDY and QUIC session pooling.
> 
> BUG=398925
> R=agl@chromium.org
> 
> Review URL: https://codereview.chromium.org/417013005

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/426413002
-----------------------------------------------------------------

### bu...@chromium.org (2014-07-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5bc3f5918d9c6a35b4749c8aa67b8eeb6159f47c

commit 5bc3f5918d9c6a35b4749c8aa67b8eeb6159f47c
Author: rch@chromium.org <rch@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Jul 30 22:24:12 2014

Merge 286598 "Disable SPDY and QUIC session pooling."

> Disable SPDY and QUIC session pooling.
> 
> BUG=398925
> R=agl@chromium.org
> 
> Review URL: https://codereview.chromium.org/417013005

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/426413002

git-svn-id: svn://svn.chromium.org/chrome/branches/1985/src@286615 0039d316-1c4b-4281-b951-d872f2087c98



### rc...@chromium.org (2014-07-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-07-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c5a5de7086f92457ee880b9792046a8e5849a5d8

commit c5a5de7086f92457ee880b9792046a8e5849a5d8
Author: rch@chromium.org <rch@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Jul 30 22:53:22 2014

Revert 286615 "Merge 286598 "Disable SPDY and QUIC session pooli..."

> Merge 286598 "Disable SPDY and QUIC session pooling."
> 
> > Disable SPDY and QUIC session pooling.
> > 
> > BUG=398925
> > R=agl@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/417013005
> 
> TBR=rch@chromium.org
> 
> Review URL: https://codereview.chromium.org/426413002

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/414123007

git-svn-id: svn://svn.chromium.org/chrome/branches/1985/src@286626 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-30)

------------------------------------------------------------------
r286626 | rch@chromium.org | 2014-07-30T22:53:22.391256Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/spdy/spdy_session_unittest.cc?r1=286626&r2=286625&pathrev=286626
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/spdy/spdy_session.cc?r1=286626&r2=286625&pathrev=286626
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/quic/quic_client_session.cc?r1=286626&r2=286625&pathrev=286626
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/quic/quic_stream_factory_test.cc?r1=286626&r2=286625&pathrev=286626
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=286626&r2=286625&pathrev=286626

Revert 286615 "Merge 286598 "Disable SPDY and QUIC session pooli..."

> Merge 286598 "Disable SPDY and QUIC session pooling."
> 
> > Disable SPDY and QUIC session pooling.
> > 
> > BUG=398925
> > R=agl@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/417013005
> 
> TBR=rch@chromium.org
> 
> Review URL: https://codereview.chromium.org/426413002

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/414123007
-----------------------------------------------------------------

### bu...@chromium.org (2014-07-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/19e8b4a43997e5725105ee5dec62c5dd3ed1a648

commit 19e8b4a43997e5725105ee5dec62c5dd3ed1a648
Author: rch@chromium.org <rch@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Jul 30 22:57:53 2014

Merge 286598 "Disable SPDY and QUIC session pooling."

> Disable SPDY and QUIC session pooling.
> 
> BUG=398925
> R=agl@chromium.org
> 
> Review URL: https://codereview.chromium.org/417013005

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/429323003

git-svn-id: svn://svn.chromium.org/chrome/branches/1985/src@286628 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-30)

------------------------------------------------------------------
r286628 | rch@chromium.org | 2014-07-30T22:57:53.935551Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/spdy/spdy_session_unittest.cc?r1=286628&r2=286627&pathrev=286628
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/spdy/spdy_session.cc?r1=286628&r2=286627&pathrev=286628
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/quic/quic_client_session.cc?r1=286628&r2=286627&pathrev=286628
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/quic/quic_stream_factory_test.cc?r1=286628&r2=286627&pathrev=286628
   M http://src.chromium.org/viewvc/chrome/branches/1985/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=286628&r2=286627&pathrev=286628

Merge 286598 "Disable SPDY and QUIC session pooling."

> Disable SPDY and QUIC session pooling.
> 
> BUG=398925
> R=agl@chromium.org
> 
> Review URL: https://codereview.chromium.org/417013005

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/429323003
-----------------------------------------------------------------

### bu...@chromium.org (2014-07-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/43807b41850c6de9ee77a1a45f9c5f6fd42edafa

commit 43807b41850c6de9ee77a1a45f9c5f6fd42edafa
Author: matthewyuan@chromium.org <matthewyuan@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Jul 30 23:46:25 2014

Merge 286628 "Merge 286598 "Disable SPDY and QUIC session pooling.""

> Merge 286598 "Disable SPDY and QUIC session pooling."
> 
> > Disable SPDY and QUIC session pooling.
> > 
> > BUG=398925
> > R=agl@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/417013005
> 
> TBR=rch@chromium.org
> 
> Review URL: https://codereview.chromium.org/429323003

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/428373002

git-svn-id: svn://svn.chromium.org/chrome/branches/1985_122/src@286638 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bcb79371e8aca77dbd876549abcea23df1d376a3

commit bcb79371e8aca77dbd876549abcea23df1d376a3
Author: matthewyuan@chromium.org <matthewyuan@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Wed Jul 30 23:47:34 2014

Merge 286628 "Merge 286598 "Disable SPDY and QUIC session pooling.""

> Merge 286598 "Disable SPDY and QUIC session pooling."
> 
> > Disable SPDY and QUIC session pooling.
> > 
> > BUG=398925
> > R=agl@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/417013005
> 
> TBR=rch@chromium.org
> 
> Review URL: https://codereview.chromium.org/429323003

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/435473002

git-svn-id: svn://svn.chromium.org/chrome/branches/1985_128/src@286639 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-07-30)

------------------------------------------------------------------
r286638 | matthewyuan@chromium.org | 2014-07-30T23:46:25.200123Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/net/spdy/spdy_session_unittest.cc?r1=286638&r2=286637&pathrev=286638
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/net/spdy/spdy_session.cc?r1=286638&r2=286637&pathrev=286638
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/net/quic/quic_client_session.cc?r1=286638&r2=286637&pathrev=286638
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/net/quic/quic_stream_factory_test.cc?r1=286638&r2=286637&pathrev=286638
   M http://src.chromium.org/viewvc/chrome/branches/1985_122/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=286638&r2=286637&pathrev=286638

Merge 286628 "Merge 286598 "Disable SPDY and QUIC session pooling.""

> Merge 286598 "Disable SPDY and QUIC session pooling."
> 
> > Disable SPDY and QUIC session pooling.
> > 
> > BUG=398925
> > R=agl@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/417013005
> 
> TBR=rch@chromium.org
> 
> Review URL: https://codereview.chromium.org/429323003

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/428373002
-----------------------------------------------------------------

### bu...@chromium.org (2014-07-30)

------------------------------------------------------------------
r286639 | matthewyuan@chromium.org | 2014-07-30T23:47:34.678199Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=286639&r2=286638&pathrev=286639
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/net/spdy/spdy_session_unittest.cc?r1=286639&r2=286638&pathrev=286639
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/net/spdy/spdy_session.cc?r1=286639&r2=286638&pathrev=286639
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/net/quic/quic_client_session.cc?r1=286639&r2=286638&pathrev=286639
   M http://src.chromium.org/viewvc/chrome/branches/1985_128/src/net/quic/quic_stream_factory_test.cc?r1=286639&r2=286638&pathrev=286639

Merge 286628 "Merge 286598 "Disable SPDY and QUIC session pooling.""

> Merge 286598 "Disable SPDY and QUIC session pooling."
> 
> > Disable SPDY and QUIC session pooling.
> > 
> > BUG=398925
> > R=agl@chromium.org
> > 
> > Review URL: https://codereview.chromium.org/417013005
> 
> TBR=rch@chromium.org
> 
> Review URL: https://codereview.chromium.org/429323003

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/435473002
-----------------------------------------------------------------

### rc...@chromium.org (2014-08-01)

I'd like to merge this to Beta (m37, right?) to make sure we've fixed this everywhere.

### rc...@chromium.org (2014-08-01)

+amineer for m37 merge approval

### am...@chromium.org (2014-08-01)

merge approved for m37 branch 2062

### bu...@chromium.org (2014-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5c9f9e2ea265ee92d8d4bf870727c8ed952b7c0d

commit 5c9f9e2ea265ee92d8d4bf870727c8ed952b7c0d
Author: rch@chromium.org <rch@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Aug 01 20:03:58 2014

Merge 286598 "Disable SPDY and QUIC session pooling."

> Disable SPDY and QUIC session pooling.
> 
> BUG=398925
> R=agl@chromium.org
> 
> Review URL: https://codereview.chromium.org/417013005

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/433923005

git-svn-id: svn://svn.chromium.org/chrome/branches/2062/src@287077 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-08-01)

------------------------------------------------------------------
r287077 | rch@chromium.org | 2014-08-01T20:03:58.932264Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/net/spdy/spdy_session_unittest.cc?r1=287077&r2=287076&pathrev=287077
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/net/spdy/spdy_session.cc?r1=287077&r2=287076&pathrev=287077
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/net/quic/quic_client_session.cc?r1=287077&r2=287076&pathrev=287077
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/net/quic/quic_stream_factory_test.cc?r1=287077&r2=287076&pathrev=287077
   M http://src.chromium.org/viewvc/chrome/branches/2062/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=287077&r2=287076&pathrev=287077

Merge 286598 "Disable SPDY and QUIC session pooling."

> Disable SPDY and QUIC session pooling.
> 
> BUG=398925
> R=agl@chromium.org
> 
> Review URL: https://codereview.chromium.org/417013005

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/433923005
-----------------------------------------------------------------

### cb...@chromium.org (2014-08-01)

[Empty comment from Monorail migration]

### cb...@chromium.org (2014-08-01)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-08-04)

[Empty comment from Monorail migration]

### cb...@chromium.org (2014-08-04)

[Empty comment from Monorail migration]

### ag...@chromium.org (2014-08-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-08-08)

------------------------------------------------------------------
r288435 | rch@chromium.org | 2014-08-08T21:22:45.384613Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_security_headers_unittest.cc?r1=288435&r2=288434&pathrev=288435
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/transport_security_state_unittest.cc?r1=288435&r2=288434&pathrev=288435
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/transport_security_state.cc?r1=288435&r2=288434&pathrev=288435
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_nss.cc?r1=288435&r2=288434&pathrev=288435
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/transport_security_state.h?r1=288435&r2=288434&pathrev=288435
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/crypto/proof_verifier_chromium.cc?r1=288435&r2=288434&pathrev=288435

Centralize the logic for checking public key pins from ClientSocketNSS
and ProofVerifierChromium to TransportSecurityState::CheckPublicKeyPins.
This required adding an is_issued_by_known_root argument to this method.

In addition, CheckPublicKeyPins now only checks static pins if the
TransportSecurityState's enable_static_pins_ member is true. This defaults
to true only for official desktop builds. This also means that dynamic
pins are now checked on mobile and on non-official builds.

BUG=398925,391033

Review URL: https://codereview.chromium.org/433123003
-----------------------------------------------------------------

### bu...@chromium.org (2014-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8d60aa54abe0517d756c9d625ece75feabed613a

commit 8d60aa54abe0517d756c9d625ece75feabed613a
Author: rch@chromium.org <rch@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Aug 08 21:22:45 2014

Centralize the logic for checking public key pins from ClientSocketNSS
and ProofVerifierChromium to TransportSecurityState::CheckPublicKeyPins.
This required adding an is_issued_by_known_root argument to this method.

In addition, CheckPublicKeyPins now only checks static pins if the
TransportSecurityState's enable_static_pins_ member is true. This defaults
to true only for official desktop builds. This also means that dynamic
pins are now checked on mobile and on non-official builds.

BUG=398925,391033

Review URL: https://codereview.chromium.org/433123003

Cr-Commit-Position: refs/heads/master@{#288435}
git-svn-id: svn://svn.chromium.org/chrome/trunk/src@288435 0039d316-1c4b-4281-b951-d872f2087c98



### cl...@chromium.org (2014-08-09)

rch@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ag...@chromium.org (2014-08-10)

Opera folks: the reporter has all but disclosed this now: http://www.ietf.org/mail-archive/web/tls/current/msg13345.html


### [Deleted User] (2014-08-11)

Thanks. The blackhat paper has also been released (with the specifics about this attack removed) https://bh.ht.vc/vhost_confusion.pdf.  We have already released turning off sessions caching for SPDY and quick on android, and we aim to release for desktop tomorrow (12'th). 

Is the HSTS patch vital for this issue? As I see it, dynamic pinning is not widely used yet, and static pinning is turned off. Thus, it doesn't seem to have that big of an impact for us.

### ag...@chromium.org (2014-08-11)

haavardm: by session caching, I'm guessing that you mean connection sharing (i.e. the changes referenced above?)

The pinning change very likely doesn't matter for you.

### [Deleted User] (2014-08-11)

Sorry yes, that was a typo. I mean connection sharing.



### in...@chromium.org (2014-08-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-11)

Why is the bug not marked as Fixed ?

### ag...@chromium.org (2014-08-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-11)

Thanks!

### cl...@chromium.org (2014-08-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-08-13)

High severity would be an unmitigated, arbitrary origin bypass. Whereas this requires an active MitM plus the user clicking through a certificate warning. That's pretty significant mitigation, so this is medium-severity at worst.

### sg...@chromium.org (2014-08-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-08-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/17a3503b9f011d37a01dd7790806ade6f80da2b3

commit 17a3503b9f011d37a01dd7790806ade6f80da2b3
Author: rch@chromium.org <rch@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Thu Aug 14 01:00:11 2014

Refactor pooling logic into a helper method
Disable pooling when there are cert errors.
Disable pooling when pinning does not match for the new host.

BUG=398925

Review URL: https://codereview.chromium.org/425803014

Cr-Commit-Position: refs/heads/master@{#289433}
git-svn-id: svn://svn.chromium.org/chrome/trunk/src@289433 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-08-14)

------------------------------------------------------------------
r289433 | rch@chromium.org | 2014-08-14T01:00:11.753589Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.cc?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.h?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_unittest.cc?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.cc?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session_test.cc?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.cc?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory_test.cc?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.h?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.cc?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.h?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.h?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_network_session.cc?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_http_stream_test.cc?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.cc?r1=289433&r2=289432&pathrev=289433
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.h?r1=289433&r2=289432&pathrev=289433

Refactor pooling logic into a helper method
Disable pooling when there are cert errors.
Disable pooling when pinning does not match for the new host.

BUG=398925

Review URL: https://codereview.chromium.org/425803014
-----------------------------------------------------------------

### bu...@chromium.org (2014-08-15)

------------------------------------------------------------------
r289937 | rch@chromium.org | 2014-08-15T18:09:27.173986Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.cc?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.h?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.h?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_network_session.cc?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_http_stream_test.cc?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.cc?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.h?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.cc?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.h?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_unittest.cc?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.cc?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session_test.cc?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.cc?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory_test.cc?r1=289937&r2=289936&pathrev=289937
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.h?r1=289937&r2=289936&pathrev=289937

Revert 289433 "Refactor pooling logic into a helper method"

Reason for revert:
Causes crashes in canary.

> Refactor pooling logic into a helper method
> Disable pooling when there are cert errors.
> Disable pooling when pinning does not match for the new host.
> 
> BUG=398925
> 
> Review URL: https://codereview.chromium.org/425803014

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/476113003
-----------------------------------------------------------------

### bu...@chromium.org (2014-08-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/debe0fde0c897da880278fba6d4fbde05c927094

commit debe0fde0c897da880278fba6d4fbde05c927094
Author: rch@chromium.org <rch@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Aug 15 18:09:27 2014

Revert 289433 "Refactor pooling logic into a helper method"

Reason for revert:
Causes crashes in canary.

> Refactor pooling logic into a helper method
> Disable pooling when there are cert errors.
> Disable pooling when pinning does not match for the new host.
> 
> BUG=398925
> 
> Review URL: https://codereview.chromium.org/425803014

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/476113003

Cr-Commit-Position: refs/heads/master@{#289937}
git-svn-id: svn://svn.chromium.org/chrome/trunk/src@289937 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-08-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/31a0d4a5c7211de7311239f14e193ab669a8e9f5

commit 31a0d4a5c7211de7311239f14e193ab669a8e9f5
Author: matthewyuan@chromium.org <matthewyuan@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri Aug 15 18:42:12 2014

Revert 289433 "Refactor pooling logic into a helper method"

> Refactor pooling logic into a helper method
> Disable pooling when there are cert errors.
> Disable pooling when pinning does not match for the new host.
> 
> BUG=398925
> 
> Review URL: https://codereview.chromium.org/425803014

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/479643002

git-svn-id: svn://svn.chromium.org/chrome/branches/2124/src@289952 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-08-15)

------------------------------------------------------------------
r289952 | matthewyuan@chromium.org | 2014-08-15T18:42:12.503005Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/quic/quic_stream_factory.h?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/http/http_network_session.cc?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/quic/quic_http_stream_test.cc?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/spdy/spdy_test_utils.cc?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/spdy/spdy_test_utils.h?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/spdy/spdy_session_pool.cc?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/spdy/spdy_session_pool.h?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/spdy/spdy_session_unittest.cc?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/spdy/spdy_session.cc?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/quic/quic_client_session_test.cc?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/quic/quic_client_session.cc?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/quic/quic_stream_factory_test.cc?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/spdy/spdy_session.h?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/quic/quic_stream_factory.cc?r1=289952&r2=289951&pathrev=289952
   M http://src.chromium.org/viewvc/chrome/branches/2124/src/net/quic/quic_client_session.h?r1=289952&r2=289951&pathrev=289952

Revert 289433 "Refactor pooling logic into a helper method"

> Refactor pooling logic into a helper method
> Disable pooling when there are cert errors.
> Disable pooling when pinning does not match for the new host.
> 
> BUG=398925
> 
> Review URL: https://codereview.chromium.org/425803014

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/479643002
-----------------------------------------------------------------

### bu...@chromium.org (2014-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dc33fbbe670b3ff49209b4093e58df07959fcda9

commit dc33fbbe670b3ff49209b4093e58df07959fcda9
Author: rch@chromium.org <rch@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Mon Aug 18 19:15:58 2014

Refactor pooling logic into a helper method
Disable pooling when there are cert errors.
Disable pooling when pinning does not match for the new host.

BUG=398925

Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=289433

Review URL: https://codereview.chromium.org/425803014

Cr-Commit-Position: refs/heads/master@{#290320}
git-svn-id: svn://svn.chromium.org/chrome/trunk/src@290320 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-08-18)

------------------------------------------------------------------
r290320 | rch@chromium.org | 2014-08-18T19:15:58.904272Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_network_session.cc?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_http_stream_test.cc?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.cc?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.h?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.cc?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.h?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_response_body_drainer_unittest.cc?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_unittest.cc?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.cc?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session_test.cc?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.cc?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory_test.cc?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.h?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.cc?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.h?r1=290320&r2=290319&pathrev=290320
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.h?r1=290320&r2=290319&pathrev=290320

Refactor pooling logic into a helper method
Disable pooling when there are cert errors.
Disable pooling when pinning does not match for the new host.

BUG=398925

Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=289433

Review URL: https://codereview.chromium.org/425803014
-----------------------------------------------------------------

### bu...@chromium.org (2014-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/763fa4320dcef04e8bfaf65bdc32100b7ec9bd18

commit 763fa4320dcef04e8bfaf65bdc32100b7ec9bd18
Author: viettrungluu@chromium.org <viettrungluu@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Mon Aug 18 22:40:49 2014

Revert 289433 "Refactor pooling logic into a helper method"

(Test-only?) leaks (see bug). The lsan suppressions file tells me to
revert, not suppress.

BUG=404833

> Refactor pooling logic into a helper method
> Disable pooling when there are cert errors.
> Disable pooling when pinning does not match for the new host.
> 
> BUG=398925
> 
> Review URL: https://codereview.chromium.org/425803014

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/483043002

Cr-Commit-Position: refs/heads/master@{#290384}
git-svn-id: svn://svn.chromium.org/chrome/trunk/src@290384 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-08-18)

------------------------------------------------------------------
r290384 | viettrungluu@chromium.org | 2014-08-18T22:40:49.926638Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.h?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_unittest.cc?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.cc?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session_test.cc?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.cc?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory_test.cc?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.h?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.cc?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.h?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.h?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_network_session.cc?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_http_stream_test.cc?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.cc?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.h?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=290384&r2=290383&pathrev=290384
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.cc?r1=290384&r2=290383&pathrev=290384

Revert 289433 "Refactor pooling logic into a helper method"

(Test-only?) leaks (see bug). The lsan suppressions file tells me to
revert, not suppress.

BUG=404833

> Refactor pooling logic into a helper method
> Disable pooling when there are cert errors.
> Disable pooling when pinning does not match for the new host.
> 
> BUG=398925
> 
> Review URL: https://codereview.chromium.org/425803014

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/483043002
-----------------------------------------------------------------

### bu...@chromium.org (2014-08-18)

------------------------------------------------------------------
r290385 | viettrungluu@chromium.org | 2014-08-18T22:45:03.604328Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.h?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_network_session.cc?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_http_stream_test.cc?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.cc?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.h?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.cc?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.h?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_unittest.cc?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.cc?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session_test.cc?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.cc?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory_test.cc?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.h?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.cc?r1=290385&r2=290384&pathrev=290385
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.h?r1=290385&r2=290384&pathrev=290385

Revert 290384 "Revert 289433 "Refactor pooling logic into a help..."

Oops, reverted the original land, not the re-land.

> Revert 289433 "Refactor pooling logic into a helper method"
> 
> (Test-only?) leaks (see bug). The lsan suppressions file tells me to
> revert, not suppress.
> 
> BUG=404833
> 
> > Refactor pooling logic into a helper method
> > Disable pooling when there are cert errors.
> > Disable pooling when pinning does not match for the new host.
> > 
> > BUG=398925
> > 
> > Review URL: https://codereview.chromium.org/425803014
> 
> TBR=rch@chromium.org
> 
> Review URL: https://codereview.chromium.org/483043002

TBR=viettrungluu@chromium.org

Review URL: https://codereview.chromium.org/483963002
-----------------------------------------------------------------

### bu...@chromium.org (2014-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2b4c5746322f80829730033352f0aeb9d4a556e5

commit 2b4c5746322f80829730033352f0aeb9d4a556e5
Author: viettrungluu@chromium.org <viettrungluu@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Mon Aug 18 22:45:03 2014

Revert 290384 "Revert 289433 "Refactor pooling logic into a help..."

Oops, reverted the original land, not the re-land.

> Revert 289433 "Refactor pooling logic into a helper method"
> 
> (Test-only?) leaks (see bug). The lsan suppressions file tells me to
> revert, not suppress.
> 
> BUG=404833
> 
> > Refactor pooling logic into a helper method
> > Disable pooling when there are cert errors.
> > Disable pooling when pinning does not match for the new host.
> > 
> > BUG=398925
> > 
> > Review URL: https://codereview.chromium.org/425803014
> 
> TBR=rch@chromium.org
> 
> Review URL: https://codereview.chromium.org/483043002

TBR=viettrungluu@chromium.org

Review URL: https://codereview.chromium.org/483963002

Cr-Commit-Position: refs/heads/master@{#290385}
git-svn-id: svn://svn.chromium.org/chrome/trunk/src@290385 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/98ddfe8c2bf4422216654107daf9cd4940d07053

commit 98ddfe8c2bf4422216654107daf9cd4940d07053
Author: viettrungluu@chromium.org <viettrungluu@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Mon Aug 18 22:47:00 2014

Revert 290320 "Refactor pooling logic into a helper method"

Leaks (see bug).

Actually reverting the re-land this time.

BUG=404833

> Refactor pooling logic into a helper method
> Disable pooling when there are cert errors.
> Disable pooling when pinning does not match for the new host.
> 
> BUG=398925
> 
> Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=289433
> 
> Review URL: https://codereview.chromium.org/425803014

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/485943004

Cr-Commit-Position: refs/heads/master@{#290386}
git-svn-id: svn://svn.chromium.org/chrome/trunk/src@290386 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-08-18)

------------------------------------------------------------------
r290386 | viettrungluu@chromium.org | 2014-08-18T22:47:00.254872Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_unittest.cc?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.cc?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session_test.cc?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.cc?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory_test.cc?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.h?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.cc?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.h?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.h?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_network_session.cc?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_http_stream_test.cc?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.cc?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.h?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.cc?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_response_body_drainer_unittest.cc?r1=290386&r2=290385&pathrev=290386
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.h?r1=290386&r2=290385&pathrev=290386

Revert 290320 "Refactor pooling logic into a helper method"

Leaks (see bug).

Actually reverting the re-land this time.

BUG=404833

> Refactor pooling logic into a helper method
> Disable pooling when there are cert errors.
> Disable pooling when pinning does not match for the new host.
> 
> BUG=398925
> 
> Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=289433
> 
> Review URL: https://codereview.chromium.org/425803014

TBR=rch@chromium.org

Review URL: https://codereview.chromium.org/485943004
-----------------------------------------------------------------

### bu...@chromium.org (2014-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5db452206ce2503815abe55878179b2399cc906a

commit 5db452206ce2503815abe55878179b2399cc906a
Author: rch@chromium.org <rch@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Tue Aug 19 05:22:15 2014

Refactor pooling logic into a helper method
Disable pooling when there are cert errors.
Disable pooling when pinning does not match for the new host.

BUG=398925

Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=289433

Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=290320

Review URL: https://codereview.chromium.org/425803014

Cr-Commit-Position: refs/heads/master@{#290497}
git-svn-id: svn://svn.chromium.org/chrome/trunk/src@290497 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-08-19)

------------------------------------------------------------------
r290497 | rch@chromium.org | 2014-08-19T05:22:15.314908Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/socket/ssl_client_socket_pool_unittest.cc?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.cc?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_pool.h?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_response_body_drainer_unittest.cc?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session_unittest.cc?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.cc?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session_test.cc?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.cc?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory_test.cc?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_session.h?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.cc?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_client_session.h?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_stream_factory.h?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/http/http_network_session.cc?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/quic/quic_http_stream_test.cc?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.cc?r1=290497&r2=290496&pathrev=290497
   M http://src.chromium.org/viewvc/chrome/trunk/src/net/spdy/spdy_test_utils.h?r1=290497&r2=290496&pathrev=290497

Refactor pooling logic into a helper method
Disable pooling when there are cert errors.
Disable pooling when pinning does not match for the new host.

BUG=398925

Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=289433

Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=290320

Review URL: https://codereview.chromium.org/425803014
-----------------------------------------------------------------

### rc...@chromium.org (2014-08-20)

Requesting a merge to m38 of the final CL in this issue.

### [Deleted User] (2014-08-21)

Which cl is this request for?

### rc...@chromium.org (2014-08-21)

The merge request is for: 
  https://codereview.chromium.org/425803014/
It re-enables connection pooling for QUIC and SPDY sessions. This decreases latency for users, and reduces server load.


### rc...@chromium.org (2014-08-21)

matthewyuan: merge ping

### [Deleted User] (2014-08-25)

Approved for 38.

### bu...@chromium.org (2014-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe

commit 9058507e9ca2c218cf07c53a8ce61bd70231edfe
Author: Ryan Hamilton <rch@chromium.org>
Date: Mon Aug 25 19:05:50 2014

Merge 290497 "Refactor pooling logic into a helper method"

> Refactor pooling logic into a helper method
> Disable pooling when there are  cert errors.
> Disable pooling when pinning does not match for the new host.
>
> BUG=398925
>
> Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=289433
>
> Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=290320
>
> Review URL: https://codereview.chromium.org/425803014
>
> Cr-Commit-Position: refs/heads/master@{#290497}
> git-svn-id: svn://svn.chromium.org/chrome/trunk/src@290497 0039d316-1c4b-4281-b951-d872f2087c98
> (cherry picked from commit 5db452206ce2503815abe55878179b2399cc906a)

BUG=398925
TBR=matthewyuan

Review URL: https://codereview.chromium.org/498373002

Cr-Commit-Position: refs/branch-heads/2125@{#86}
Cr-Branched-From: b68026d94bda36dd106a3d91a098719f952a9477-refs/heads/master@{#290040}

[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/http/http_network_session.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/http/http_response_body_drainer_unittest.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/quic/quic_client_session.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/quic/quic_client_session.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/quic/quic_client_session_test.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/quic/quic_http_stream_test.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/quic/quic_stream_factory.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/quic/quic_stream_factory.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/quic/quic_stream_factory_test.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/socket/ssl_client_socket_pool_unittest.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/spdy/spdy_session.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/spdy/spdy_session.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/spdy/spdy_session_pool.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/spdy/spdy_session_pool.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/spdy/spdy_session_unittest.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/spdy/spdy_test_utils.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/9058507e9ca2c218cf07c53a8ce61bd70231edfe/net/spdy/spdy_test_utils.h


### wf...@chromium.org (2014-10-09)

The reward panel were disappointed that this vulnerability was publicly disclosed while we were still in the process of patching the issue - see #39. This meant we had to take additional costly steps at the server-side to protect our users.

The Chromium project takes responsible disclosure seriously and normally this would have excluded this report from a reward, since our rules[1] clearly state "Bugs disclosed publicly or to a third-party for purposes other than fixing the bug will typically not qualify for a reward".

However, we do recognize the severity of this bug and appreciate INRIA's continued collaboration in discovering and reporting important bugs like this to us, so although this report isn't eligible for our usual reward amounts[1], we are pleased to reward $1000 for your efforts.  Thanks for helping us protect our users!

[1] https://www.google.com/about/appsecurity/chrome-rewards/index.html

### cl...@chromium.org (2014-11-18)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-09)

Contacted Antoine regarding payment.

### la...@google.com (2015-03-04)

Migrate from Cr-Internals-Network-SPDY to Cr-Internals-Network-HTTP2

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/398925?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network>HTTP2, Internals>Network>SSL]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080132)*
