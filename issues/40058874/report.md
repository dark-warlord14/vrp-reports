# Security: Private Network Access (PNA) Bypass Allows Access to localhost on macOS & Linux using 0.0.0.0

| Field | Value |
|-------|-------|
| **Issue ID** | [40058874](https://issues.chromium.org/issues/40058874) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>CORS>PrivateNetworkAccess |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2023-48022 |
| **Reporter** | sa...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2022-02-23 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Chrome is deprecating direct access to private network endpoints from public websites as part of the Private Network Access (PNA) specification (<https://developer.chrome.com/blog/private-network-access-preflight/>). Services listening on the localhost (127.0.0.0/8) are considered private according to the specification (<https://wicg.github.io/private-network-access/#ip-address-space-heading>). Chrome's PNA protection can be bypassed using the IP address 0.0.0.0 to access services listening on the localhost on macOS and Linux.

This can also be abused in DNS rebinding attacks targeting a web application listening on the localhost.

The impact is that an attacker can bypass Chrome's Private Network Access (PNA) protections to access HTTP resources listening on the localhost.

**VERSION**  

Chrome Version: 98.0.4758.102 stable  

Operating System: macOS (12.2.1) & Linux (Ubuntu 21.10)

**REPRODUCTION CASE**

The following test uses an HTML file hosted on a plaintext HTTP server. The victim needs to run a plaintext HTTP service listening on the localhost (127.0.0.1). For our test, the service on the localhost is hosting an image (favicon.ico in the example below). The sample HTML tries to access the image using an <img> HTML tag. The first <img> contains a src attribute pointing to the localhost. Chrome's PNS will block this access with the following console error: "Access to image at '<http://localhost:8080/favicon.ico>' from origin '<http://example.com>' has been blocked by CORS policy: The request client is not a secure context and the resource is in more-private address space `local`." The second <img> contains a src attribute pointing to the 0.0.0.0 IP address. This image will be displayed in Chrome and bypasses the PNA protection.

The following HTML needs to be hosted on a plaintext HTTP server (accessed using http://):

<!doctype html>

<html lang="en">
<body>
<p>Image localhost: <img src="http://localhost:8080/favicon.ico" alt="localhost test image"/></p>
<p>Image 0.0.0.0: <img src="http://0.0.0.0:8080/favicon.ico" alt="0.0.0.0 test image"/></p>
</body>
</html>

**CREDIT INFORMATION**  

Reporter credit: Roger Meyer

## Attachments

- [chrome-1-click-rce-fast.mov](attachments/chrome-1-click-rce-fast.mov) (video/quicktime, 17.8 MB)
- [0.0.0.0 Day.jpg](attachments/0.0.0.0 Day.jpg) (image/jpeg, 54.8 KB)

## Timeline

### [Deleted User] (2022-02-23)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-02-23)

I tried on M96, 98, and 100, but I see both get ERR_CONNECTION_REFUSED.

I'm loading the poc.html at http://localhost:8000/poc.html

### da...@chromium.org (2022-02-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>CORS>PrivateNetworkAccess]

### sa...@gmail.com (2022-02-24)

The ERR_CONNECTION_REFUSED you see sounds like the poc.html does not have the correct image source URL as the browser can't connect.

The attacker deploys poc.html on a HTTP server they control, e.g. a public server such as http://www.example.com/poc.html, or on their LAN such as http://www.example.local/poc.html - This can't be on the victim machine.

The victim runs their own HTTP server on their own machine, listening on the localhost interface (e.g. http://localhost:8000) with an image or favicon deployed under root /.

The poc.html file on attacker machine must include a link to the image served from the victim machine (e.g. http://localhost:8000/image.jpg / http://0.0.0.0:8000/image.jpg).

The victim browses to poc.html hosted on the attacker machine (e.g. http://www.example.local/poc.html) from their own machine. Chrome will load the second image (0.0.0.0) but not the first one (localhost).


### [Deleted User] (2022-02-24)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@chromium.org (2022-02-24)

Thanks for the report! It makes sense to me that the load would function: 0.0.0.0 is not considered a "local" address, but maybe it should! I think this is a specification concern as much as an implementation concern. Filed https://github.com/WICG/private-network-access/issues/71 for this.

### ti...@chromium.org (2022-02-24)

[Empty comment from Monorail migration]

### ti...@chromium.org (2022-02-24)

Not sure how to decide the security impact. This only affects a security measure that has not yet been rolled out to users.

### ti...@chromium.org (2022-02-24)

Or rather, not entirely and successfully been rolled out...

### da...@chromium.org (2022-02-24)

If it's not available to users then None. Thanks!

### da...@chromium.org (2022-02-24)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-02-24)

[Empty comment from Monorail migration]

### sa...@gmail.com (2022-02-25)

Regarding "not yet been rolled out to users": In the sample poc, the image loaded from localhost is blocked in Chrome version 98.0.4758.102 stable. This can be bypassed with the current stable Chrome version. Has phase 2 (described in https://developer.chrome.com/blog/private-network-access-preflight/#rollout-plan) already been rolled out?

### ti...@google.com (2022-03-01)

Sorry for the confusion - as I tried to clarify in https://crbug.com/chromium/1300021#c9, this has not been *entirely* and *successfully* rolled out. It started rolling out in Chrome 98, but has been rolled back since.

### gm...@gmail.com (2022-03-02)

[Comment Deleted]

### gm...@gmail.com (2022-03-02)

moving comment to better hopefully more approp thread

### ly...@google.com (2022-04-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5746e52b7b9a34cc817d40e46770933be2063d58

commit 5746e52b7b9a34cc817d40e46770933be2063d58
Author: Yifan Luo <lyf@chromium.org>
Date: Tue Apr 12 16:44:15 2022

[Private Network Access] Add use counter for 0.0.0.0

In security perspective, we intend to block the usage of 0.0.0.0
entirely. Before that, we add a use counter here to track the usage
to estimate the impact.

Bug: 1300021
Change-Id: I563ac5dac6a47946b62a659d58c4a08f315c17bf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3557995
Reviewed-by: Mike West <mkwst@chromium.org>
Reviewed-by: Titouan Rigoudy <titouan@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Yifan Luo <lyf@chromium.org>
Cr-Commit-Position: refs/heads/main@{#991571}

[modify] https://crrev.com/5746e52b7b9a34cc817d40e46770933be2063d58/docs/security/web-mitigation-metrics.md
[modify] https://crrev.com/5746e52b7b9a34cc817d40e46770933be2063d58/third_party/blink/public/mojom/web_feature/web_feature.mojom
[modify] https://crrev.com/5746e52b7b9a34cc817d40e46770933be2063d58/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/5746e52b7b9a34cc817d40e46770933be2063d58/third_party/blink/renderer/core/loader/resource_load_observer_for_worker.cc
[modify] https://crrev.com/5746e52b7b9a34cc817d40e46770933be2063d58/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/5746e52b7b9a34cc817d40e46770933be2063d58/third_party/blink/renderer/core/loader/resource_load_observer_for_frame.cc
[modify] https://crrev.com/5746e52b7b9a34cc817d40e46770933be2063d58/chrome/browser/net/private_network_access_browsertest.cc


### co...@gmail.com (2022-11-18)

At least one DNS resolver that allows users to filter traffic using blocklists and another one that uses DoH, are both returning 0.0.0.0 for blocked hostnames instead of NXDOMAIN, thus DNS rebinding attacks on localhost are possible.

People using those DNS resolvers might skew the above counter.

To test, try as root:
# nc -l -p 443 -s 127.0.0.1
(or -s 0.0.0.0 or without those)

Then either make sure the DNS resolver returns 0.0.0.0 for google.com and/or accounts.google.com and start chromium (which should attempt to open google by default)

But what you see instead is the netcat terminal receives some garbage text(a https attempt from chromium) which includes the hostname that it was tried ie. accounts.google.com
Or you can emulate the DNS resolver returning 0.0.0.0, by having this line in /etc/hosts:
0.0.0.0 www.google.com accounts.google.com
which functionally equivalent to the line:
127.0.0.1 www.google.com accounts.google.com

Tested Chromium Version 107.0.5304.110 (Official Build) snap (64-bit)

Firefox currently has this problem also: https://bugzilla.mozilla.org/show_bug.cgi?id=1475605#c3


### va...@chromium.org (2023-03-02)

Moving over after the rename to LocalNetworkAccess

[Monorail components: Blink>SecurityFeature>LocalNetworkAccess]

### ti...@chromium.org (2023-04-19)

[Empty comment from Monorail migration]

### ti...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

[Monorail components: -Blink>SecurityFeature>LocalNetworkAccess]

### gi...@appspot.gserviceaccount.com (2023-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d7488bd49b72709a4c82a4479d08204e5b9d4fad

commit d7488bd49b72709a4c82a4479d08204e5b9d4fad
Author: Yifan Luo <lyf@chromium.org>
Date: Thu Nov 30 13:06:54 2023

[Private Network Access] add chrome flag for 0.0.0.0

A use counter has been added a while ago: https://source.chromium.org/chromium/chromium/src/+/5746e52b7b9a34cc817d40e46770933be2063d58

We now add a blink and chrome flag and intend to deprecate it.

Bug: 1300021
Change-Id: I9b952674bd603163949dfce76adcd3427a1ad072
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5028016
Reviewed-by: Yifan Luo <lyf@chromium.org>
Reviewed-by: Jonathan Hao <phao@chromium.org>
Commit-Queue: Yifan Luo <lyf@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1231270}

[modify] https://crrev.com/d7488bd49b72709a4c82a4479d08204e5b9d4fad/third_party/blink/renderer/platform/runtime_enabled_features.json5
[modify] https://crrev.com/d7488bd49b72709a4c82a4479d08204e5b9d4fad/third_party/blink/common/features.cc
[modify] https://crrev.com/d7488bd49b72709a4c82a4479d08204e5b9d4fad/third_party/blink/public/common/features.h
[modify] https://crrev.com/d7488bd49b72709a4c82a4479d08204e5b9d4fad/tools/metrics/histograms/enums.xml


### is...@google.com (2023-11-30)

This issue was migrated from crbug.com/chromium/1300021?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1431423]
[Monorail components added to Component Tags custom field.]

### es...@chromium.org (2024-04-02)

This was reported afresh from an external researcher: https://issues.chromium.org/issues/332410234

Now that PNA for subresource requests has shipped, I'm going to re-classify this as a security vulnerability. This doesn't neatly fit into our severity guidelines, but I'm going to call this S2/Medium, along the lines of "not harmful on their own but potentially harmful when combined with other bugs" (since this would have to be combined with a vulnerable server on localhost).

### es...@chromium.org (2024-04-02)

I'm going to leave this as SecurityImpact-None because I *think* the relevant restriction is still in a deprecation origin trial, per https://chromestatus.com/feature/5436853517811712, meaning that any origin can opt out of the restriction, so it's not actually fully shipped yet. IMO resolving this bug should block fully shipping.

### av...@oligosecurity.io (2024-04-03)

1. Attackers can access any port-forwarding on the victim's machine.
2. Services bound on localhost or private network interfaces (Airtunes on MacOS, CUPS on Debian-based Linux, Containers, Kubernetes API).
3. This issue enables information disclosure on specific persons to fingerprint its visitors - like I did in http://ports.sh

It enabled eBay to port-scan their visitors: https://community.ebay.com/t5/Selling/Dear-Ebay-Why-are-you-scanning-my-ports/td-p/31022821/page/2

Together with DNS certificate transparency, attackers can leverage tailor-made payloads to trigger HTTP requests in internal networks, bypassing WAF and Firewalls.

Allowing 0.0.0.0 turns the browser into a localhost gateway, bypassing all CORS/PNA security measurements.

The browser intentionally blocked 127.0.0.1, localhost, and 192.168.X.X (the world understood it was a problem and started working on mitigating such private network access).
It was explicitly fixed for the above - must not be accessible through 0.0.0.0.



### av...@oligosecurity.io (2024-04-03)

Even if not used for RCE because it depends on a vulnerable service - 0.0.0.0 can be used (if not already) to fingerprint users, understand which VPN is used, and if the user has access to host visible via public DNS but that is accessible only from a VPN.

Certificate Transparency makes it easy to find DNS records that should be private but are public. They are only accessible inside the company VPN, but using 0.0.0.0 it can classify if a given user works for a specific company by the HTTP response to a public DNS record that is only accessible when inside the VPN.

It is not just RCE that depends on external services that are also exploitable.
The browser returns 2 different responses to the Javascript application when the service is accessible but not allowed, or when the connection is refused;
So information disclosure and fingerprinting are also attack vectors and are very easy to exploit.

It can be used for various spear-phishing attacks, as I demonstrated CVE-2023-48022 exploiting a visitor using a single HTTP request.
You don't even need to see or access the HTTP response! 

### av...@oligosecurity.io (2024-04-21)

Hey all, I wanted to understand better what is the status of the vulnerability.
The issue open in the standardization GitHub of PNA that you mentioned: https://github.com/WICG/private-network-access/issues/71
So I am trying to understand the next steps from your side.

Since we managed to exploit services on localhost through Chome in the latest versions, it still allows (by default) access to localhost and private network interfaces at the time of writing.
The video I shared above uses a 'no-cors' and 0.0.0.0 to get access to unauthorized services on LOCALhost. 
We demonstrated successful exploitation, information disclosure, and RCE thanks to this vulnerability - so I am trying to understand why the security impact is 'None'.

I’d be happy to hop on a call to show how the exploit can be easily reproduced, if not exploited in the wild already.
In the meantime, the video I shared shows it end to end. Although some websites that try to use 0.0.0.0 might break by the security fix, it is an important security feature for the safety of Chrome's users.

PNA is worthless as long as this vulnerability exists because it allows bypass of any existing PNA or CORS rule. What am I missing?
You have marked this bug as a vulnerability following my disclosure and reopened the issue, granting it P2 and S2.

Users are already getting attacked - just one example is how eBay has abused this exact design flaw to fingerprint users. We have reasons to believe that attackers are using this vulnerability to attack users behind firewalls inside private networks, and I don't think that access to 0.0.0.0 is disputable... I treat it like a backdoor, literally a backdoor to the private organization and LOCALhost. Localhost should be local, don't you agree?

We are of course following responsible disclosure and 90-day window as we do with the other browser's security programs, and would be happy to assist in any way we can.
Once the process is over. we plan to write on that matter publicly focusing on available exploitations, so everyone is aware of the risk. We believe attackers are already abusing it at the time of writing, as I demonstrated a 1-click RCE with Ray that is used in OpenAI and many large organizations.

Please let me know how you recommend we proceed. As mentioned, I’d be happy to assist with ideating for different solutions or in any other way you think is relevant.
Thanks for helping keep everyone safe!

### es...@chromium.org (2024-04-22)

SecurityImpact-None is an internal tracking label that we use to manage security bugs. The reason I assigned that label is because Private Network Access is a new security feature that isn't fully shipped yet. In particular, any website can opt out of Private Network Access restrictions through a "reverse origin trial" (https://developer.chrome.com/docs/web-platform/origin-trials#deprecation_trials), as I mentioned in comment #27. This means that the Private Network Access restriction is not an actual security boundary yet, thus we don't consider a bypass of Private Network Access to be a security bug, currently. In other words, even if this bug were fixed, a website could still trivially exploit the Ray bug you mention by opting into the reverse origin trial to be able to access the private network freely. (SecurityImpact-None is also the label we use when someone reports a security bug in a feature that is under development and not yet shipped to users.)

Do you have evidence that this bug is being abused in the wild (not just as a proof of concept, but as an actual attack), and if so can you share more details?

### av...@oligosecurity.io (2024-04-25)

Thanks for the clarifications!

We have demonstrated attacks in the wild to Amy Ressler from your team (Staff Security Engineer, Chrome security) in a video call. We contacted her after we found ShadowRay exploited in the wild. See Forbes - https://www.forbes.com/sites/thomasbrewster/2024/03/26/hackers-breach-hundreds-of-ai-compute-servers-researchers-say/ , and our technical blog post - https://www.oligo.security/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild.

A few additional examples are:
1. eBay was using this vulnerability to scan user's ports and fingerprinting (Forbes - https://www.forbes.com/sites/daveywinder/2020/05/25/did-you-know-ebay-is-probing-your-computer-heres-how-to-stop-it-windows-privacy-chrome-firefox-web-browser/?sh=65157c3b3a92 and Bleeping Computer - https://www.bleepingcomputer.com/news/security/ebay-port-scans-visitors-computers-for-remote-access-programs/)
2. Unit 42 by Palo Alto has identified a DNS rebinding attack (https://unit42.paloaltonetworks.com/dns-rebinding/)  that used this as an attack vector
3. Numerous CVEs in Chrome have addressed "localhost" explicitly, forgetting about 0.0.0.0: (see example1 - https://issues.chromium.org/issues/40092867#comment17 and example 2 - https://issues.chromium.org/issues/40092867#comment32). There is a bypass that enables access to localhost and bypasses 'localhost' security patches across the browser's codebase.

We have seen browsers talking about this problem years ago. Through the years Localhost was explicitly blocked - but all of these vulnerabilities are still possible through 0.0.0.0:
- PRE-Auth through localhost services (Ray, AZ-CLI, CUPS, VS Code, Argo Workflows, and anything that uses port-forward such as Kubernetes)
- Bypass or Firewall and WAF rules
- VPN internal organization access
- DNS rebinding, to localhost and private domains.
- Scan the ports of the visiting users
- Understand if an anonymous user who visits a website is an employee of a specific company or not through javascript (Fingerprinting for spear-phishing attacks).

Our report is not specific to "Ray" or a POC, nor does it depend on another vulnerability.
The problem resides in enabling access to all network interfaces without authorization or opt-in from the user perspective - and the family of vulnerabilities it enables as an attack vector.

We want to increase awareness of this family of vulnerabilities and this unintended behavior, which was abused in the past. We will of course follow the responsible disclosure and wait 90 days from the opening of the original report (https://issues.chromium.org/issues/332410234). In the meantime - we would be more than happy to assist and support the remediation efforts in any way! 
If you don't consider this a security bug - and are ok with us publishing a blog post to educate the market on this interesting attack vector prior to the 90 days, we would be happy to do so with your approval. 
Thanks for your time and for diving into the details! 
Please let us know what we should do next, and thanks for keeping everyone safe. 


### es...@chromium.org (2024-05-10)

Given that the issue is already discussed publicly (https://github.com/WICG/private-network-access/issues/71), I don't think there's any concern with you publishing a blog post. I just want to reiterate, however, that the bug is a bypass of a security restriction that is not yet fully rolled out. The default behavior of the web for decades has been that websites can trigger requests from the user's browser to the private network. Private Network Access is an in-progress project to introduce restrictions on this behavior, but no part of PNA is fully shipped yet.

### av...@oligosecurity.io (2024-05-23)

Thank you for your response.

"I just want to reiterate, however, that the bug is a bypass of a security restriction that is not yet fully rolled out. The default behavior of the web for decades has been that websites can trigger requests from the user's browser to the private network. Private Network Access is an in-progress project to introduce restrictions on this behavior, but no part of PNA is fully shipped yet."
Indeed. We agree that the security restriction has not been fully rolled out yet, therefore it is not considered a vulnerability (because PNA was never fully shipped).

With that said, it was claimed that "resolving this bug should block fully shipping." - so we DO expect 0.0.0.0 to be blocked by PNA policies before the feature is fully rolled out. Since 127.0.0.1 and localhost are blocked explicitly by PNA, we consider it a bypass and a vulnerability if PNA is fully rolled out in the current way, still enabling access to 0.0.0.0.

IMO 0.0.0.0 access should be Opt-In and not Opt-Out by end users.
The problem resides in enabling access to all network interfaces without authorization or opt-in from the end-user perspective.
Domain owners should NOT have the ability to access the private network of their visitors unless explicitly allowed, even through reverse origin trial. It is not different from a microphone or a camera - This is how I see it.

If a user chooses to allow 0.0.0.0 or 127.0.0.1 access from a certain domain or website, there is no problem! but please let the user opt-in and allow it first, by allowing this private access explicitly for a given domain, like the Microphone and Camera modals that prompt the user with a question.

Until PNA is fully rolled out (blocking also 0.0.0.0), Chromium's users will remain exposed to the family of vulnerabilities we presented above such as DNS rebinding attacks, client port-scanning, and various application-level attacks that use HTTP because they assume that localhost is so-called "local" and not accessible to browsers. 

This inherited issue does not originate in PNA or Chromium.
The community failed to fix this flaw for 18 years (https://bugzilla.mozilla.org/show_bug.cgi?id=354493) and we still failed.  The current state of PNA does not help against these attacks, because there's a bypass using 0.0.0.0, and if I understood it correctly, this flaw will not be fixed anytime soon.

### es...@chromium.org (2024-05-23)

> if I understood it correctly, this flaw will not be fixed anytime soon.

There is active work ongoing to block 0.0.0.0, please see https://chromestatus.com/feature/5106143060033536 for status.

### av...@oligosecurity.io (2024-05-24)

Thank you for the clarifications! Your work on PNA is truly amazing and non-trivial. 

### ar...@chromium.org (2024-12-13)

**(secondary security shepherd)**

> > if I understood it correctly, this flaw will not be fixed anytime soon.
> 
> There is active work ongoing to block 0.0.0.0, please see <https://chromestatus.com/feature/5106143060033536> for status.

Hi [estark@chromium.org](mailto:estark@chromium.org), the feature has shipped 3 month ago \o/

Could you please update this bug accordingly?

### es...@chromium.org (2024-12-13)

I'm going to close this bug because 0.0.0.0 has been incorporated into Private Network Access. Two caveats, however:
1.) We are re-evaluating the PNA approach and may end up rolling back the secure context restriction and expiring the deprecation trial. This would mean that there are effectively no restrictions on 0.0.0.0 or any other host on private networks until we roll out a new approach. See <https://groups.google.com/a/chromium.org/g/blink-dev/c/NCV3anf1KtU/m/WyL9rKjtAQAJ>.
2.) There is ongoing work in the Fetch spec to block 0.0.0.0 outside the PNA context, but that hasn't landed in the spec yet. See <https://github.com/whatwg/fetch/pull/1763>.

### av...@oligosecurity.io (2024-12-16)

I would like to confirm my understanding regarding the handling of 0.0.0.0 in the last stable version.
Specifically, does this mean that 0.0.0.0 can still be exploited as demonstrated in our DEF CON presentation (the "0.0.0.0-day" exploit)?

Following our disclosure, the plan (as outlined just four months ago) was to restrict 0.0.0.0 at the Private Network Access (PNA) level. This change was reportedly implemented in Chrome 128 based on my original report, as documented here: PNA Restriction for 0.0.0.0 - https://chromestatus.com/feature/5106143060033536

For reference:
- 0.0.0.0 Exploit Overview: https://en.wikipedia.org/wiki/0.0.0.0#0.0.0.0_day_exploit
- https://www.forbes.com/sites/thomasbrewster/2024/08/07/hackers-exploit-18-year-old-vulnerability-in-apple-google-and-mozilla-browsers/
- [DEF CON 2024] Oligo Security Blog Post on Exploiting Localhost APIs: https://www.oligo.security/blog/0-0-0-0-day-exploiting-localhost-apis-from-the-browser

However, based on your comment, my understanding is that:

PNA preflight checks will no longer block the NULL IP address (0.0.0.0).
To date, 0.0.0.0 is not blocked and will remain unblocked until further notice.

If this understanding is correct, this indicates that the issue is not resolved, the NULL IP ADDRESS bug still exists, and Remote Code Execution (RCE) via 0.0.0.0 remains an attack vector to exploit services running on private networks. as my original example, an HTTP POST request with mode "no-cors" will be sent and successfully received in services that run locally.

In contrast, Safari (WebKit) has already implemented restrictions for 0.0.0.0 following our disclosure, prior to any PNA mechanism, because the RFC claims this IP (NULL IP) should never be used as destination IP address. For the same reason, in Windows is blocking this IP in OS level.

Could you confirm if this interpretation is accurate or clarify what I might be missing?

### sp...@google.com (2024-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact privilege escalation that has contributed to overall Private Network Access considerations


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-19)

This report was a catalyst for our teams to consideration our approaches for Private Network Access. While there may not yet be a final resolution as of yet, we have a lot of data points. Thank you for your efforts and reporting this issue to us.

### av...@oligosecurity.io (2025-03-18)

Hi team,

After reporting and disclosing the following issue around PNA in Chromium:
https://issuetracker.google.com/issues/40058874

I have received the following message:

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has
> decided to award you $1000.00 for this report.
>
>
But I cannot see the issue in the website to claim my bounty.
Can you please help me with this?
Thanks.



*Avi Lumelsky*

CTO Office

avi@oligosecurity.io

oligosecurity.io <https://www.oligo.security/>


<https://streaklinks.com/BZW113rJCdBj8_Zs-wsE5pnk/https%3A%2F%2Fwww.linkedin.com%2Fcompany%2Foligo-security%2F>
<https://streaklinks.com/BZW113r_v_DeMGOHjwhrUv-9/https%3A%2F%2Fwww.facebook.com%2Fpeople%2FOligo-Security%2F100088584127824%2F>
<https://streaklinks.com/BZW113rvr1ZPxLOzTQ7ODagV/https%3A%2F%2Fwww.youtube.com%2F%40oligosecurity>



On Wed, Dec 18, 2024 at 11:56 PM <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/40058874
>
> *Changed*
>
> *sp...@google.com <sp...@google.com> added comment #40
> <https://issues.chromium.org/issues/40058874#comment40>:*
> ** NOTE: This is an automatically generated email **
>
> Hello,
>
> Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has
> decided to award you $1000.00 for this report.
>
> Rationale for this decision:
> report of lower impact privilege escalation that has contributed to
> overall Private Network Access considerations
>
>
> Important: If you aren't already registered with Google as a supplier,
> p2p-vrp@google.com will reach out to you. If you have registered in the
> past, no need to repeat the process – you can sit back and relax, and we
> will process the payment soon.
>
> If you have any payment related requests, please direct them to
> p2p-vrp@google.com. Please remember to include the subject of this email
> and the email address that the report was sent from.
>
>
> Thank you for your efforts and helping us make Chrome more secure for all
> users!
>
> Cheers,
> Chrome VRP Panel Bot
>
>
> P.S. One other thing we'd like to mention:
>
> * Please do NOT publicly disclose details until a fix has been released to
> all our users. Early public disclosure may cancel the provisional reward.
> Also, please be considerate about disclosure when the bug affects a core
> library that may be used by other products. Please do NOT share this
> information with third parties who are not directly involved in fixing the
> bug. Doing so may cancel the provisional reward. Please be honest if you
> have already disclosed anything publicly or to third parties. Lastly, we
> understand that some of you are not interested in money. We offer the
> option to donate your reward to an eligible charity. If you prefer this
> option, let us know and we will also match your donation - subject to our
> discretion. Any rewards that are unclaimed after 12 months will be donated
> to a charity of our choosing.
> Please contact security-vrp@chromium.org with any questions.
> _______________________________
>
> *Reference Info: 40058874 Security: Private Network Access (PNA) Bypass
> Allows Access to localhost on macOS & Linux using 0.0.0.0*
> component:  Public Trackers > 1362134 > Chromium > Blink >
> SecurityFeature > CORS > PrivateNetworkAccess
> <https://issues.chromium.org/components/1456363>
> status:  Fixed
> reporter:  sa...@gmail.com
> assignee:  es...@chromium.org
> cc:  ar...@chromium.org, avi@oligosecurity.io, ct...@chromium.org, and 5
> more
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P2
> severity:  S2
> duplicate:  40063934 <https://issues.chromium.org/issues/40063934>,
> 332410234 <https://issues.chromium.org/issues/332410234>
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, Security_Impact-None
> <https://issues.chromium.org/hotlists/5433277>, Unconfirmed
> <https://issues.chromium.org/hotlists/5437934>
> retention:  Component default
> Component Ancestor Tags:  Blink, Blink>SecurityFeature,
> Blink>SecurityFeature>CORS, Blink>SecurityFeature>CORS>PrivateNetworkAccess
> Component Tags:  Blink>SecurityFeature>CORS>PrivateNetworkAccess
> OS:  Android, Linux, Mac, Windows, ChromeOS
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 40058874
> <https://issues.chromium.org/issues/40058874> where you have the roles:
> starred, cc
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/40058874?unsubscribe=true>
>


### av...@oligosecurity.io (2025-03-18)

deleted

### am...@chromium.org (2025-03-18)

Hi Avi, apologies for this, but it appears there have been some wires crossed. This reward and reward message was posted on this report, which is not the report you submitted ([issue 332410234](https://issues.chromium.org/issues/332410234)), but the original report of this issue from 2022. You report was merged into this one as one of two duplicate reports of this root issue (the other from 2023, [issue 40063934](https://issues.chromium.org/issues/40063934)).
Our policies stipulate that only the first report of a given issue is eligible for a VRP reward in most cases.

Apologies for the confusion.

I have removed the above comment due to the PII included in the comment.

### av...@oligosecurity.io (2025-03-18)

The handling of this vulnerability was deeply flawed and unacceptable. The
original ticket from 2022 languished for two years without any meaningful
action, classified as a low priority hypothetical risk.
It was only through Oligo Security's rigorous research, proof-of-concept
exploit, and public disclosure at DEFCON that the true severity of this
issue came to light.

Our team definitively proved that 0.0.0.0 could be weaponized for remote
code execution from Gmail on engineers' local machines - a critical
security threat that was entirely overlooked by Chromium's team. The fact
that it took our intervention to elevate this from S4/P4 to P2 and spark
cross-browser collaboration is a damning indictment of the initial
assessment and follow-up. (Comment #26 broke the silence after 2 years of
inactivity: https://issues.chromium.org/issues/40058874#comment26)

Our research team's meeting with Amy Ressler from Chromium was necessary to
demonstrate the real-world risk that was previously dismissed. The
subsequent media coverage, including in Forbes, further underscores the
significance of our findings.

It is disingenuous and misleading to claim this as a "duplicate" when the
original report lacked any evidence of exploitability and sat idle for
years. Our work was instrumental in not only identifying the true scope of
the vulnerability but also in driving the eventual fix. The security of
countless users was at risk due to this oversight.

Given our pivotal role in exposing and resolving this long-standing
vulnerability, it is unconscionable to deny eligibility for a bounty. Our
efforts directly led to critical security improvements across major
browsers. To suggest otherwise is to grossly misrepresent the timeline and
impact of our research. We demand a full reassessment of the bounty
eligibility in light of these indisputable facts.


*Avi Lumelsky*

CTO Office

avi@oligosecurity.io

oligosecurity.io <https://www.oligo.security/>


<https://streaklinks.com/BZW113rJCdBj8_Zs-wsE5pnk/https%3A%2F%2Fwww.linkedin.com%2Fcompany%2Foligo-security%2F>
<https://streaklinks.com/BZW113r_v_DeMGOHjwhrUv-9/https%3A%2F%2Fwww.facebook.com%2Fpeople%2FOligo-Security%2F100088584127824%2F>
<https://streaklinks.com/BZW113rvr1ZPxLOzTQ7ODagV/https%3A%2F%2Fwww.youtube.com%2F%40oligosecurity>



On Tue, Mar 18, 2025 at 5:06 PM <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/40058874
>
> *Changed*
>
> *am...@chromium.org <am...@chromium.org> added comment #44
> <https://issues.chromium.org/issues/40058874#comment44>:*
>
> Hi Avi, apologies for this, but it appears there have been some wires
> crossed. This reward and reward message was posted on this report, which is
> not the report you submitted (issue 332410234
> <https://issues.chromium.org/issues/332410234>), but the original report
> of this issue from 2022. You report was merged into this one as one of two
> duplicate reports of this root issue (the other from 2023, issue 40063934
> <https://issues.chromium.org/issues/40063934>). Our policies stipulate
> that only the first report of a given issue is eligible for a VRP reward in
> most cases.
>
> Apologies for the confusion.
>
> _______________________________
>
> *Reference Info: 40058874 Security: Private Network Access (PNA) Bypass
> Allows Access to localhost on macOS & Linux using 0.0.0.0*
> component:  Public Trackers > 1362134 > Chromium > Blink >
> SecurityFeature > PrivateNetworkAccess
> <https://issues.chromium.org/components/1456363>
> status:  Fixed
> reporter:  sa...@gmail.com
> assignee:  es...@chromium.org
> cc:  ar...@chromium.org, avi@oligosecurity.io, ct...@chromium.org, and 5
> more
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P2
> severity:  S2
> duplicate:  40063934 <https://issues.chromium.org/issues/40063934>,
> 332410234 <https://issues.chromium.org/issues/332410234>
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-inprocess
> <https://issues.chromium.org/hotlists/5432630>, Security_Impact-None
> <https://issues.chromium.org/hotlists/5433277>
> retention:  Component default
> Component Ancestor Tags:  Blink, Blink>SecurityFeature,
> Blink>SecurityFeature>CORS, Blink>SecurityFeature>CORS>PrivateNetworkAccess
> Component Tags:  Blink>SecurityFeature>CORS>PrivateNetworkAccess
> OS:  Android, Linux, Mac, Windows, ChromeOS
> vrp-reward:  1000
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 40058874
> <https://issues.chromium.org/issues/40058874> where you have the roles:
> cc, starred
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/40058874?unsubscribe=true>
>


### am...@chromium.org (2025-03-18)

Hi Avi, Amy here. I am also the TL of our VRP.
While we appreciate your efforts here and your agree that your report did identify that the PNA spec and implementation failed to classify 0.0.0.0 as a local address, the root cause of PNA providing access to 0.0.0.0 and this CORS bypass was identified in this report in 2022 and another report (also merged into this one as a duplicate) in 2023. As I mentioned during that meeting, I believed we like had a report on this issue already. Afterwards, upon receiving your report, we did merge the Oligo report into this one as a duplicate.

> Our work was instrumental in not only identifying the true scope of the vulnerability but also in driving the eventual fix.

We do agree that your work did demonstrate full potential for security harm, however the Chrome-specific plans to mitigate this were made prior to and not directly related to your report in 2024.

We generally only reward a single root cause of an issue and this report was the first of three with the same root cause.
Because of this, we did not separately evaluate your report for a potential, separate reward.

That all being said, VRP reward decisions are made by us as a Panel, so I can not unilaterally make or provide a decision, but I'll add this to our queue for discussion at our weekly VRP Panel session for this week. Any update will be provided on your original report, [issue 332410234](https://issues.chromium.org/issues/332410234).

### av...@oligosecurity.io (2025-03-19)

Thanks Amy, for this and for your help over the past year.
We understand. It is more about getting credit for our contribution and
effort on this impactful research.
Anyway, we would like to donate the bounty (if found eligible), like we
always do.

Thanks in advance and looking forward to working with you in the future!
Avi and the Oligo Team


On Tue, Mar 18, 2025 at 9:54 PM <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/40058874
>
> *Changed*
>
> *am...@chromium.org <am...@chromium.org> added comment #46
> <https://issues.chromium.org/issues/40058874#comment46>:*
>
> Hi Avi, Amy here. I am also the TL of our VRP. While we appreciate your
> efforts here and your agree that your report did identify that the PNA spec
> and implementation failed to classify 0.0.0.0 as a local address, the root
> cause of PNA providing access to 0.0.0.0 and this CORS bypass was
> identified in this report in 2022 and another report (also merged into this
> one as a duplicate) in 2023. As I mentioned during that meeting, I believed
> we like had a report on this issue already. Afterwards, upon receiving your
> report, we did merge the Oligo report into this one as a duplicate.
>
> Our work was instrumental in not only identifying the true scope of the
> vulnerability but also in driving the eventual fix.
>
> We do agree that your work did demonstrate full potential for security
> harm, however the Chrome-specific plans to mitigate this were made prior to
> and not directly related to your report in 2024.
>
> We generally only reward a single root cause of an issue and this report
> was the first of three with the same root cause. Because of this, we did
> not separately evaluate your report for a potential, separate reward.
>
> That all being said, VRP reward decisions are made by us as a Panel, so I
> can not unilaterally make or provide a decision, but I'll add this to our
> queue for discussion at our weekly VRP Panel session for this week. Any
> update will be provided on your original report, issue 332410234
> <https://issues.chromium.org/issues/332410234>.
>
> _______________________________
>
> *Reference Info: 40058874 Security: Private Network Access (PNA) Bypass
> Allows Access to localhost on macOS & Linux using 0.0.0.0*
> component:  Public Trackers > 1362134 > Chromium > Blink >
> SecurityFeature > PrivateNetworkAccess
> <https://issues.chromium.org/components/1456363>
> status:  Fixed
> reporter:  sa...@gmail.com
> assignee:  es...@chromium.org
> cc:  ar...@chromium.org, avi@oligosecurity.io, ct...@chromium.org, and 5
> more
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P2
> severity:  S2
> duplicate:  40063934 <https://issues.chromium.org/issues/40063934>,
> 332410234 <https://issues.chromium.org/issues/332410234>
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-inprocess
> <https://issues.chromium.org/hotlists/5432630>, Security_Impact-None
> <https://issues.chromium.org/hotlists/5433277>
> retention:  Component default
> Component Ancestor Tags:  Blink, Blink>SecurityFeature,
> Blink>SecurityFeature>CORS, Blink>SecurityFeature>CORS>PrivateNetworkAccess
> Component Tags:  Blink>SecurityFeature>CORS>PrivateNetworkAccess
> OS:  Android, Linux, Mac, Windows, ChromeOS
> vrp-reward:  1000
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 40058874
> <https://issues.chromium.org/issues/40058874> where you have the roles:
> cc, starred
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/40058874?unsubscribe=true>
>


### dx...@google.com (2025-08-26)

Project: chromium/src  

Branch:  main  

Author:  Emily Stark [estark@google.com](mailto:estark@google.com)  

Link:    <https://chromium-review.googlesource.com/6874710>

Remove killswitch for treating 0.0.0.0 as non-public

---


Expand for full commit details
```
     
    This was a killswitch for a change that was made quite a while ago and 
    didn't cause any problems, so we don't need the killswitch anymore. 
     
    Bug: 40058874 
    Change-Id: I260a9dc8f9baf1ae7d098b69d80c22336914bc83 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6874710 
    Reviewed-by: Kenichi Ishibashi <bashi@chromium.org> 
    Commit-Queue: Emily Stark <estark@chromium.org> 
    Reviewed-by: Andrew Rayskiy <greengrape@google.com> 
    Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1506598}

```

---

Files:

- M `chrome/browser/net/private_network_access_browsertest.cc`
- M `content/browser/renderer_host/private_network_access_browsertest.cc`
- M `services/network/public/cpp/features.cc`
- M `services/network/public/cpp/features.h`
- M `services/network/public/cpp/ip_address_space_util.cc`
- M `services/network/public/cpp/ip_address_space_util_unittest.cc`

---

Hash: [87d3ef47c569f878efe16b7b7310cd473cd370a2](https://chromiumdash.appspot.com/commit/87d3ef47c569f878efe16b7b7310cd473cd370a2)  

Date: Tue Aug 26 17:09:30 2025


---

### jo...@gmail.com (2025-10-28)

To be clear... This still works and remains unfixed in the context of a DNS rebinding attack.

I've been using an instance of NCCGroup/singularity to exploit this vulnerability across a wide variety of vulnerable applications (currently under embargo).

### ct...@chromium.org (2025-10-29)

Re #49: Manual testing for me shows 0.0.0.0 is correctly treated as a loopback address by LNA. If you are seeing way to bypass LNA using 0.0.0.0, could you either provide repro steps here or file a new bug? Note that LNA is only shipping starting in Chrome 142 (for subresource/fetch/subframes, but not for WebSockets/WebTransport/WebRTC/etc. yet), so if you are testing in earlier versions (and not explicitly enabling the feature flag) this may just be working as expected.

### av...@oligosecurity.io (2026-03-20)

Great resource for all of us that I found very relevant: https://localmess.github.io/assets/bridges-to-self-localmess-usenix-security-26.pdf

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058874)*
