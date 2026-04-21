# Security: HSTS not applied to WebSocket

| Field | Value |
|-------|-------|
| **Issue ID** | [40081328](https://issues.chromium.org/issues/40081328) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Network>WebSockets, Internals>Network>SSL |
| **Reporter** | [Deleted User] |
| **Assignee** | ri...@chromium.org |
| **Created** | 2015-02-04 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

The script in the attached poc.html uses the WebSocket API to make an insecure, "plain HTTP", request to "accounts.google.com".

Verification that the insecure request is made can be accomplished easily by capturing traffic locally with Wireshark.

"accounts.google.com" has HSTS configured on it to only use https, and is even in the HSTS pre-load list (although being in the pre-load list does not matter for this bug as it affects non-pre-loaded sites as well).

This means that HSTS policy is not being applied to WebSocket requests, and leaves users open to "ssl stripping", cookie forcing, etc...

I believe that Firefox handled this issue with <https://bugzilla.mozilla.org/show_bug.cgi?id=664284>.  

Mentioned in that link, someone said that this was handled in chromium by <http://src.chromium.org/viewvc/chrome?revision=82069&view=revision>.  

But, in the almost four years since then, this seems to have been undone (or it wasn't actually handled).

**VERSION**  

Chrome Version: 40.0.2214.95 Stable  

Operating System: Ubuntu Linux 14.04.1 LTS

**REPRODUCTION CASE**  

Begin capturing traffic locally and then open the attached poc.html into an affected version of Chrome. You'll see the non-TLS traffic, including non-secure cookies, etc... in the packet capture.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 196 B)

## Timeline

### ke...@chromium.org (2015-02-04)

Ryan, do you know what is going on here? Is this known behavior?

### sl...@google.com (2015-02-04)

Adam: This appears to be a potential regression due to the WebSockets refactoring. It also appears that the test meant to catch these regressions was removed by the refactoring.

Could you please look at this ASAP?

### sl...@google.com (2015-02-04)

oh, and to be clear: I don't think the refactoring itself dropped the logic. By bringing things in line with the rest of //net, you in-advertantly got bit by the scheme-specific rewrite of HSTS in https://code.google.com/p/chromium/codesearch#chromium/src/net/url_request/url_request.cc&rcl=1422997819&l=1034

The fix should be easy - changing GetHSTSRedirect to "do the right thing" for ws -> wss as it does for http -> https - but I'm more concerned with how we missed testing.

### ri...@chromium.org (2015-02-05)

It was handled in the old implementation (or at least code and tests existed, I haven't personally tested it).

The tests weren't directly applicable to the new implementation. I scanned them before deleting them, but failed to notice the HSTS test among the defunct WebSocket-over-SPDY tests.

Sorry for the oversight.

### [Deleted User] (2015-02-05)

Hi, my compliments to you on the quick initial triage of this bug.

Since the severity is set to low, I wanted to add some color as to why I think this should be handled with higher priority.

First, WebSockets are not constrained by the same origin policy. This means that a network attacker that can inject such a (simple) script into a victim's response, or can get a victim to access an attacker controlled resource containing such a script, can coerce the victim's browser into sending authentication/session data (such as that typically carried in the HTTP Authorization and Cookie headers) from any domain using such data over the network in plaintext where it can be captured by the network attacker. Fortunately, cookies marked as "secure" are NOT sent in the clear by this bug.

However, since a successful WebSocket handshake matches an HTTP upgrade request, a network attacker does have the ability to set cookies (via the Set-Cookie header) on a target/victim domain. This can lead to the user's cookie store being overflowed, or subjected to cookie tossing (both of which can affect cookies marked as secure by either ejecting them or overriding them). Such attacks can be used to fixate a user session or cause a user to work within the context of an attacker supplied account etc...

### ri...@chromium.org (2015-02-05)

I have a fix under review at https://codereview.chromium.org/903553005/

I would like advice on a couple of questions:

1. Are we in a hurry? This functionality really should have a browser_tests test to make it completely implementation-independent, but browser_tests make everything slower. If we are in a hurry I could add the browser test in a separate CL.
2. Do we need to be discreet? The CL I've uploaded is private, but it is not discreet about what issue it is fixing. I could make it less obvious if necessary.

### ke...@chromium.org (2015-02-05)

#5: Thank you for the report, by the way. This is a good catch and we appreciate it. You make a good case, I am bumping up to medium severity. Plus, HSTS is something we want to promote wider usage of, which is a non-technical reason to ensure we have prompt response on problems with it.

ricea@: This should get merged to m41 sufficiently before release that it has bake time. I think that probably gives you enough time to write a browser test but your call.

Don't worry about discretion in the CL description. Private CLs are the best we can reasonably do.

### cl...@chromium.org (2015-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2015-02-05)

#7: Sounds good.
Thanks to all involved.

### bu...@chromium.org (2015-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3

commit cb76ac67dca0a133cdfa96678ac5cd2a65af96a3
Author: Adam Rice <ricea@chromium.org>
Date: Fri Feb 20 05:33:25 2015

Apply HSTS to WebSocket connections.

With this change, ws: connections to hosts which have an existing HSTS
pin will be automatically changed to use wss:, ie. SSL.

In addition, Strict-Transport-Security headers that are sent from a wss:
server with a valid SSL certificate will be enforced on subsequent ws:
and http: connections to the same host.

This CL also modifies HttpNetworkTransaction to treat wss: the same as
https:.

BUG=455215, 446480
TEST=net_unittests
R=rsleevi@chromium.org, tyoshino@chromium.org

Review URL: https://codereview.chromium.org/903553005

Cr-Commit-Position: refs/heads/master@{#317252}

[modify] http://crrev.com/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3/chrome/browser/net/websocket_browsertest.cc
[add] http://crrev.com/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3/chrome/test/data/websocket/check-hsts.html
[add] http://crrev.com/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3/chrome/test/data/websocket/set-hsts.html
[add] http://crrev.com/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3/chrome/test/data/websocket/set-hsts.html.mock-http-headers
[add] http://crrev.com/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3/net/data/websocket/set-hsts_wsh.py
[modify] http://crrev.com/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3/net/http/http_network_transaction.cc
[modify] http://crrev.com/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3/net/http/http_network_transaction.h
[modify] http://crrev.com/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3/net/http/http_network_transaction_unittest.cc
[modify] http://crrev.com/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3/net/url_request/url_request.cc
[modify] http://crrev.com/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3/net/url_request/url_request_unittest.cc
[modify] http://crrev.com/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3/net/websockets/websocket_end_to_end_test.cc
[modify] http://crrev.com/cb76ac67dca0a133cdfa96678ac5cd2a65af96a3/net/websockets/websocket_stream.cc


### ri...@chromium.org (2015-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-20)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ri...@chromium.org (2015-02-24)

Verified on Canary. Request merge.

### ti...@google.com (2015-02-25)

Looks like this already in M42 as it branched at 317474. From a security perspective, we can let this roll in with M42, so I'm going to remove the merge-requested label for now. 

ricea: If you really want this in M41, please re-add the merge request label and also remove the "Release-0-M42" label. Thanks.

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-14)

[Comment Deleted]

### [Deleted User] (2015-04-14)

Hi Tim, thanks for the update and the reward. Please use the name Mike Ruddy. Also, could you edit out my email from your last comment? Thanks!

### ti...@google.com (2015-04-14)

(This is a repost of https://crbug.com/chromium/455215#c16 - was deleted to remove an email address)

Congratulations Mike - our reward panel has decided to award you $500 for helping us with this report.

Someone from our finance area should be in contact in two weeks to collect payment details. Please contact me directly if this doesn't happen.

We'll credit you in our release notes as "Mike Ruddy". Please let me know if you'd like to use another name or handle.

Cheers,
Tim

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### [Deleted User] (2015-04-29)

Hi Tim,

I have not been contacted by finance about this bug bounty yet.

Thanks,
Mike

### ti...@google.com (2015-04-29)

Thanks Mike - I'll email you directly.


### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-29)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2015-05-29)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

### tk...@chromium.org (2015-11-26)

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

This issue was migrated from crbug.com/chromium/455215?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Network>WebSockets, Internals>Network>SSL]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081328)*
