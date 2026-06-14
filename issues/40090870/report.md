# Security:  Several CORS security issues in browsers and specs, asking for comments

| Field | Value |
|-------|-------|
| **Issue ID** | [40090870](https://issues.chromium.org/issues/40090870) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Loader, Blink>Network>FetchAPI, Blink>SecurityFeature>CORS, Internals>Network |
| **CVE IDs** | CVE-2017-5638 |
| **Reporter** | wh...@gmail.com |
| **Assignee** | yh...@chromium.org |
| **Created** | 2018-03-21 |
| **Bounty** | $2,000.00 |

## Description

Hello,

I'm Jianjun Chen from Tsinghua University. Recently we conducted a security analysis on CORS(Cross Origin Resource Sharing) protocol and discovered a number of new CORS-related security issues. We tested mainstream browsers and found Chrome browser is affected.(See details in the attached paper)

The issues can be classified into three categories: 1) CORS relaxes the cross-origin “write” privilege in a number of subtle ways that are problematic in practice; 2) CORS brings new forms of risky trust dependencies into web interactions; 3) CORS is generally not well understood by developers, possibly due to its inexpressive policy and its complex and subtle interactions with other web mechanisms, leading to various misconfigurations.

Attachments have two demo videos of CORS-related attacks:

The first video demonstrated that malicious websites can obtain a shell on victim's internal server by crafting a malicious Content-Type header through CORS interfaces and exploiting Apache struts s2-045 vulnerability(CVE-2017-5638). 

The second video demonstrated that malicious websites can create a new file in victim's local file system, by exploiting Mac's built-in Apple file server. 

For more technical details and other cases, please refer to the attached paper.

Note that those cases in the paper are some examples,  we believe there are many other similar CORS exploits in the real world.

As many of those problems are not just implementation flaws, but fundamental issues in CORS protocols, we would like to hear your thoughts or comments, especially how to mitigate those attacks.

Thanks very much~

Jianjun Chen

## Attachments

- [CORS-paper.pdf](attachments/CORS-paper.pdf) (application/pdf, 188.6 KB)
- [cors-struts-s2-045.mov](attachments/cors-struts-s2-045.mov) (video/quicktime, 16.6 MB)
- [cors_afp.mov](attachments/cors_afp.mov) (video/quicktime, 2.8 MB)

## Timeline

### el...@chromium.org (2018-03-21)

Thanks for sharing; this is a nicely written paper.

Reading through the document, considering issues only in the browser itself (neglecting implementation problems in server software), I see:

https://crbug.com/chromium/1
-------
"CORS standards in limiting Content-Type to three specific values
(“text/plain”, “multipart/form-data”,“application/xform-url-encoded”),
these restrictions can be bypassed.
We found that all of them prefix-match the three values
and ignore the remaining values beyond the first comma
or semicolon. Thus, an attacker can still craft malicious
content in Content-Type headers by appending an attack
payload to a valid value"
----
The limited restriction here is then used to exploit an application-level vulnerability in the processing of this header by a particular server package.


https://crbug.com/chromium/2
-------
By exploiting the fact that XHR/Fetch do not limit header length, but most servers do, the client may accurately infer the length of a cross-origin cookie string. Chrome's Performance.getEntries() API directly exposes whether or not a request is successful (e.g. not a HTTP/400 returned for a RequestTooLarge). If a response has status code 400, the API will return empty response time. Information about the size of the user's cookie for a site may reveal whether they have an account on that site or have visited it before.

https://crbug.com/chromium/3
-------
CORS lacks limits on body format, a POST body in format text/plain may be misinterpreted by the server. If a server fails to validate the body's content-type, a text/plain body may be misinterpreted as a FormData serialized automatically by the browser. If the server does not expect an untrusted HTTP request to contain an arbitrary body (as Apple Filing Protocol), it may fail to protect itself.

https://crbug.com/chromium/4
-------
"Browsers are supposed to be always return error
when a server replies “Access-Control-Allow-Origin:
*” and “Access-Control-Allow-Credentials: true” for
a credential-included cross-origin request. However,
we found that this configuration combination can pass
the browser’s security check when they are in the response
for preflight requests."
----
Does Chrome exhibit this problem?


[Monorail components: Blink>Network>FetchAPI Blink>SecurityFeature>CORS]

### el...@chromium.org (2018-03-21)

Vis-a-vis #3: That one belongs more in the "Server implementation issue" category, however Chrome might also want to add port 548 (AFP) to Chrome's block list.

More generally, attacks against vulnerable services on localhost/RFC1918 addresses are covered by https://crbug.com/chromium/378566.

### wh...@gmail.com (2018-03-22)

Thanks very much for your reply and also thanks for the summary, they are very professional.

---
For issue #4, I can’t reproduce it on Chrome now. Sorry, it may be my mistake. I’ll revise it in the paper.

———
For issue #3,  the boundary is hard to tell, it could be considered as a server-side issue, but this issue is unexploitable before CORS.

Blocking port 548 is effective approach for this case, but I'm a bit worried that there may be many other similar services exposed, eg redis(port 6379 ), memcache(port 11211).

Very glad to see that you are considering restricting access to localhost/RFC 1918 addresses. Although it can’t address all the intranet access problems, such as in IPv6 network, but it can solve most common cases.

Another more fundamental solution is always-preflight. The root cause of these problem is that browsers send attacker-crafted data directly, without asking the server whether is willing to be involved into the communication.  Thus, we can send a preflight request for all cross origin requests that allow users to customize headers and body, to get sending permission from servers.   It’s also an intuitive idea from access control perspective, all the network access(including sending requests and reading responses) are authorized by server-side.  

———
For the forgeable null value issue，null value of Origin header is shared by multiple different sources.  Will you consider using different values for different sources to avoid misconfiguration and confusion?

———
For risky trust dependency issue, is it possible to prevent HTTPS domains from trusting HTTP domains in browsers, just like HTTPS/HTTP mixed content are blocked now?

Those are just my suggestions, it's up to you. Thanks~

### mm...@chromium.org (2018-03-27)

toyoshim@, are you a right owner for this? Could you please take a look?

### to...@chromium.org (2018-03-28)

yep, I'll take a look.
mkwst@ is also the best to see the issues from spec side.

[Monorail components: Blink>Loader]

### to...@chromium.org (2018-03-28)

From the viewpoint of implementation side, the section 4.1 and 4.2 are very interesting, and I think we should have quick fixes to mitigate the problems.

For request headers:
 - need to have a reasonable size limit that should be smaller than one of typical servers, e.g. 4KB
 - should have strict BNF checks (content-type value may need spec side modifications to restrict available parameters)

For request bodies:
 - this may also need spec changes to enforce the body to be in specified mime-type's format, but impact may be big. no good idea to mitigate this quickly, but as elawrence@ said blocking more ports would be needed, e.g. all well-known ports except for http/https.

mkwst@: what do you think about them from the viewpoint of specs?

+Internals>Network and rdsmith@
We may want to implement some of protections above in //net for common use cases regardless of CORS adoption. WDYT?


[Monorail components: Internals>Network]

### to...@chromium.org (2018-03-28)

cc:yhirano from network api team explicitly

### mk...@chromium.org (2018-03-28)

A few thoughts after skimming the paper:

1.  I think it's reasonable to be more strict in our processing of `Content-Type` in particular. It seems like a bad idea to accept more than one value.

2.  I'm a bit skeptical of the value of grammar checks on some, but not all, of the headers CORS allows in simple requests. If there are reasonable restrictions we can place on everything we allow, great. It looks like we should be able to define sane behavior for the client hints headers, for example. Simply restricting `(` and `{` (as Safari's apparently doing?) seems like it might be a good first approximation.

3.  I'm more skeptical of parsing request bodies in the hopes of preventing mismatches between the content type declared and the content delivered. The `filename` exploit is certainly a clever PoC, though, so my skepticism may be misplaced.

4.  +igrigorik@ for the questions around `Performance.getEntries()` exposing error codes cross-origin. That does surprise me a bit.

5.  The binary bits are interesting. Limiting access to the AFP port is certainly an option, but I agree with the suggestion above that it won't be the only service exposed with similarly lax error-handling. Truncating bodies at `0x00` (or considering them non-simple) might be something reasonable to try

Also: rdsmith@ has unfortunately moved off of Chromium, but mmenke@ and rsleevi@ will almost certainly have opinions.



### mm...@chromium.org (2018-03-28)

Disclaimer:  I have not yet read the document, just searched (not even skimmed) for a couple sections referred to it in comments here, to better understand the comments.

I think failing in the case of multiple Content-Type values makes sense - I assume this is just for cross-origin XHR/fetch request headers, and not response headers.

When you say limit request header length, I assume you mean limit the request header length of what we allow the renderer to set, not the length the network stack allows?  The latter would likely have the same problem with sniffing aggregate network header length, except it would be completely contained within Chrome, and potentially be even easier to exploit.  It also seems more likely to break sites with a lot of cookies.  Restricting the headers a consumer can set directly via Javascript still has reasonable high breakage potential, but strikes me as a reasonable thing to try, though if that limit size + the size of cookies a site sets manage to exceed the size a server limits requests to, we're back where we started.

I'm skeptical of the benefits of trying to validate the contents of the upload body.  We'd need to have yet another standard around how to do this, with its own bugs and inconsistencies, that will likely have subtle differences in implementation in different browsers.  It's only only useful if the protocol spoofing data can't be made to look like both a valid Content-Type of the advertised type, and something acceptable to a local service.  I'm less concerned with simple character limitations (e.g., disallowing certain characters, like nulls, for certain types) as opposed to more complicated rules, since behavior mismatches are less likely and there's less spec-bloat with that, but it still seems like it doesn't really address the problem.

### mm...@chromium.org (2018-03-28)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-03-28)

RE #9: Yes, the goal would be to limit the |Content-Type| values allowable as parameters to |setRequestHeader()| for "simple" requests. Note that https://crbug.com/chromium/826874 was just filed against our lack of checks here, noting that Firefox deems requests whose Content-Type contains a comma as "non-simple" and thus subject to preflight. 

The goal of the limitation on "simple" requests in the spec was designed to prevent sending any Content-Type value that was not already possible via HTML Forms ("If a site's already vulnerable to sneaky POSTs, CORS-XHR won't make it worse"). To that end, we probably shouldn't allow parameters other than charset and charset values should probably be constrained to legal character encoding names.


### yh...@chromium.org (2018-03-29)

https://crbug.com/chromium/1:
Making the check whether preflight is needed stricter makes sense, but I would like to discuss that as a spec issue. Otherwise developers will be confused.

We have https://mimesniff.spec.whatwg.org/#parsing-a-mime-type so it should be not so difficult to express the logic in the spec language.

https://crbug.com/chromium/2:
As requests with preflight are much less problematic (as the origin is explicitly recognized from the server before the actual request is sent), this is a variation of the first issue, right? We could say that when the total size of CORS-safelisted-headers exceeds 100 bytes then the request needs preflight, for example.

Again, I would like to solve this as a spec issue.

### yh...@chromium.org (2018-03-29)

> #11

We have boundary too.

### sh...@chromium.org (2018-03-29)

[Empty comment from Monorail migration]

### ig...@chromium.org (2018-03-30)

> 4. +igrigorik@ for the questions around `Performance.getEntries()` exposing error codes cross-origin. That does surprise me a bit.

ResourceTiming does not expose error codes directly. We've had many requests for that, but that's still TBD. What *is* exposed today is the fact that a fetch was initiated, and then depending on whether that fetch passes the TAO check, different metrics are exposed. Related discussion: https://github.com/w3c/resource-timing/issues/12

### el...@chromium.org (2018-03-30)

RE #15: Yeah, "directly" probably wasn't the best choice of words. The idea is that, in the scenario described (where a request returns either HTTP/200 or HTTP/400), ResourceTiming acts as a reliable oracle as which was returned. 

There'd be a similar oracle for e.g. an Image (based on whether onload vs onerror was fired) but Image doesn't allow the attacker to send arbitrary headers/bodies.

### ig...@chromium.org (2018-03-30)

Hmm, I'm not sure I understand the scenario in question then.. :)

XHR allows you to query status, what does getEntries give you that you can't already obtain via XHR directly?

### el...@chromium.org (2018-03-30)

RE #17: Ah, that's a good point that I should've noticed.

Here's the claim from the paper:

  In fact, the attacker cannot directly observe whether
  a response is 200 or 400 because browsers have normalized
  such low-level information for security considerations.
  However, the attacker can utilize timing sidechannels
  to differentiate the response status. One general
  timing channel is response time. If the attacker issues the
  “simple” request towards a large file or a time-consuming
  URL, a 200 response will be significantly slower than a
  400 response. In Chrome, the Performance.getEntries()
  API directly exposes whether or not a request is successful:
  if a response has status code 400, the API will return
  empty response time

### ig...@chromium.org (2018-03-30)

Hmm, I see. That description lacks a lot of nuance..

The timing attack against large file vs 404 is definitely a *thing*, but that can be observed without RT — e.g. load whatever resource you want via img and time the callback on on{load, error}. For RT specifically, cross-origin fetches are subject to timing-allow-origin opt-in: *iff* the origin provides the opt-in then we exposed detailed timing data, otherwise all cross-origin fetches expose same high level metrics (e.g. "duration", which you can already time via onload callbacks). As such, I don't believe RT exposes anything new here. Let me know if otherwise. 

Related: https://www.igvita.com/2016/08/26/stop-cross-site-timing-attacks-with-samesite-cookies/

As an aside, the GitHub discussion I pointed to earlier was around whether RT should expose timing information for TAO-authed responses. We converged on "yes" and I believe that's still correct.

### yh...@chromium.org (2018-04-03)

[Empty comment from Monorail migration]

### to...@chromium.org (2018-04-03)

Content-Type (and crbug.com/826874):
As c#11 says Firefox already disallows commas in simple requests. But we still want to limit parameters, maybe allowing only charset and boundary in simple requests, or disallowing all?
As yhirano@ suggested, it would be nice to discuss this in the spec first. But not sure if we can discuss this in public. Mike, any preference to discuss this issue in the spec side? We may want to implement rough checks before discussing this in public, or discuss the spec at a closed place?

Limit request header length:
+1 on mmenke@'s c#9, or using preflight on large headers that yhirano@ suggested at c#12 though we want to have a spec side discussion for the latter case.

Body validation:
mmenke@: Which TCP destination ports are forbidden to connect over XHR/fetch in Chrome network stack? I feel ports <= 1024 except for http/https are reasonable to be forbidden, and can mitigate the issue.

### mm...@chromium.org (2018-04-03)

Chrome's network stack doesn't know what an XHR is, so they have the same port restrictions as any other HTTP request.  The list is here:  https://cs.chromium.org/chromium/src/net/base/port_util.cc?type=cs&q=file:src/net+ports.*%5C%7B&sq=package:chromium&l=22

I'd be fine with further restricting it, though XHR-specific restrictions would probably need to be implemented in the (untrusted) renderer process.  Since a compromised renderer could lie about what are XHRs and what are not, anyways, not sure we'd gain any real security benefit from moving extra restrictions outside of the renderer, anyways.

### to...@chromium.org (2018-04-03)

Thanks, mmenke@.
Since ports < 1024 (oops, it's exclusive) are defined as well-known ports for privileged services, it sounds reasonable to reject all ports other than http(s) in any HTTP request regardless of initiator, XHR/fetch or not?

### mm...@chromium.org (2018-04-03)

The problem with rejecting them all is we inevitable break corner case-y stuff.  If all browsers agree do it, sure, that sounds reasonable.  If it's just us, though, are the benefits worth the breakages, and increasing fragmentation of the web platform?

### to...@chromium.org (2018-04-03)

So, as a first step, we start from rejecting only 548 port to protect AFP protocol from known attacks?

Will wait for mkwst's answer how to discuss spec side security issues, including banning all well-known other ports.

Temporarily pass the ball to Mike.

### mm...@chromium.org (2018-04-03)

I'm fine with just banning 548, due to the attack.

### to...@chromium.org (2018-04-09)

+tbansal, for https://chromium-review.googlesource.com/c/chromium/src/+/1000879

### el...@chromium.org (2018-04-09)

Re #27: Is the specific ask here "Please consider doing some filtering/validity checking on Client-Hint headers on cross-origin requests to avoid introducing more vulnerabilities of the nature described in this issue"?

### to...@chromium.org (2018-04-10)

I created a spec thread https://github.com/whatwg/fetch/issues/694 to discuss disallowing the port 548 of afp.

### to...@chromium.org (2018-04-10)

Re #28. Yep, I'm asking tbansal to have a strict check for newly added CH headers. Adding him here is to share the background why we want the check though existing code didn't have a great check.

### sh...@chromium.org (2018-04-11)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-25)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wh...@gmail.com (2018-05-18)

Hi, 

Thanks very much for all your valuable comments, making the world a safer place.

Our paper has been accepted by USENIX security 2018, so we need to present this work in August at the conference. We would appreciate it if you could fix these issues before that time. Please let us know if you need more time to solve them.

Thanks again for your efforts. If you need any help(eg. testing experiments), please let us know. We are very glad to assist you in solving these issues.

Thanks,
Jianjun Chen

### yh...@chromium.org (2018-05-25)

Anne, the reason why I asked https://github.com/whatwg/fetch/pull/736#discussion_r190844358 is here (especially (2) in #1). 

### yh...@chromium.org (2018-05-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/83bd6269cde01114e981d7ac0ece5467c515a436

commit 83bd6269cde01114e981d7ac0ece5467c515a436
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Wed May 30 08:32:02 2018

Record request mode for each load

This CL records fetch request mode for each resource loading in order
to investigate a security issue.

Bug: 824130
Change-Id: I7314baeec20e8260c47eae053ccc324c55099c20
Reviewed-on: https://chromium-review.googlesource.com/1074850
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Ilya Sherman <isherman@chromium.org>
Reviewed-by: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/heads/master@{#562762}
[modify] https://crrev.com/83bd6269cde01114e981d7ac0ece5467c515a436/content/browser/loader/resource_dispatcher_host_impl.cc
[modify] https://crrev.com/83bd6269cde01114e981d7ac0ece5467c515a436/content/browser/loader/resource_dispatcher_host_impl.h
[modify] https://crrev.com/83bd6269cde01114e981d7ac0ece5467c515a436/tools/metrics/histograms/histograms.xml


### mm...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b8a8373b9d399a7fa84bd5732a3498c748dc7ac3

commit b8a8373b9d399a7fa84bd5732a3498c748dc7ac3
Author: Matt Menke <mmenke@chromium.org>
Date: Thu May 31 05:13:46 2018

Block outgoing requests on ports 427 and 548, used by AFP.

Bug: 824130, 847842
Change-Id: I40015be2f20ffb10ea0b95d5dc670a40002d9afc
Reviewed-on: https://chromium-review.googlesource.com/1078917
Commit-Queue: Matt Menke <mmenke@chromium.org>
Reviewed-by: Eric Roman <eroman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#563152}
[modify] https://crrev.com/b8a8373b9d399a7fa84bd5732a3498c748dc7ac3/net/base/port_util.cc


### an...@gmail.com (2018-05-31)

I updated https://github.com/whatwg/fetch/pull/736 to account for overall header list size of attacker-controlled headers. I also restricted what can be done in "no-cors".

As discussed with Jianjun Chen in the corresponding Firefox bug this is probably the best we can do, except for CORS preflighting all the things, which is highly unlikely to be web-compatible.

This adds quite a bit of logic to CORS (and as noted there's at least one follow-up issue still with regards to how to treat multiple duplicate headers), but it doesn't seem unwieldy or too complicated. Would appreciate your feedback.

### yh...@chromium.org (2018-06-01)

I'd like to merge 83bd6269cde01114e981d7ac0ece5467c515a436 to M68 for a quick feedback.

### sh...@chromium.org (2018-06-01)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-06-02)

Your change meets the bar and is auto-approved for M68. Please go ahead and merge the CL to branch 3440 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-06-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8581a0293170f9f8ca7d13ae7aafd1b2befc3b37

commit 8581a0293170f9f8ca7d13ae7aafd1b2befc3b37
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Mon Jun 04 01:03:19 2018

Record request mode for each load

This CL records fetch request mode for each resource loading in order
to investigate a security issue.

TBR=yhirano@chromium.org

(cherry picked from commit 83bd6269cde01114e981d7ac0ece5467c515a436)

Bug: 824130
Change-Id: I7314baeec20e8260c47eae053ccc324c55099c20
Reviewed-on: https://chromium-review.googlesource.com/1074850
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Ilya Sherman <isherman@chromium.org>
Reviewed-by: Adam Rice <ricea@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#562762}
Reviewed-on: https://chromium-review.googlesource.com/1084141
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/branch-heads/3440@{#126}
Cr-Branched-From: 010ddcfda246975d194964ccf20038ebbdec6084-refs/heads/master@{#561733}
[modify] https://crrev.com/8581a0293170f9f8ca7d13ae7aafd1b2befc3b37/content/browser/loader/resource_dispatcher_host_impl.cc
[modify] https://crrev.com/8581a0293170f9f8ca7d13ae7aafd1b2befc3b37/content/browser/loader/resource_dispatcher_host_impl.h
[modify] https://crrev.com/8581a0293170f9f8ca7d13ae7aafd1b2befc3b37/tools/metrics/histograms/histograms.xml


### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-06-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b6b2fbe67a6ac774639bc007a3739026cd508472

commit b6b2fbe67a6ac774639bc007a3739026cd508472
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Tue Jun 05 09:18:48 2018

Fix Net.ResourceDispatcherHost.RequestMode.* UMAs

We need to compare with lower_method, not method.

Bug: 824130
Change-Id: I5fe50288b1a61baf44cf8126c5cc8867aab337e1
Reviewed-on: https://chromium-review.googlesource.com/1086887
Reviewed-by: Adam Rice <ricea@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#564417}
[modify] https://crrev.com/b6b2fbe67a6ac774639bc007a3739026cd508472/content/browser/loader/resource_dispatcher_host_impl.cc


### yh...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### yh...@chromium.org (2018-06-05)

I'd like to merge b6b2fbe67a6ac774639bc007a3739026cd508472 to M68 for a quick feedback.

### sh...@chromium.org (2018-06-06)

Your change meets the bar and is auto-approved for M68. Please go ahead and merge the CL to branch 3440 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5927f37c81c5c9647955091ffadd342b31748b4c

commit 5927f37c81c5c9647955091ffadd342b31748b4c
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Thu Jun 07 07:39:39 2018

Fix Net.ResourceDispatcherHost.RequestMode.* UMAs

We need to compare with lower_method, not method.

TBR=yhirano@chromium.org

(cherry picked from commit b6b2fbe67a6ac774639bc007a3739026cd508472)

Bug: 824130
Change-Id: I5fe50288b1a61baf44cf8126c5cc8867aab337e1
Reviewed-on: https://chromium-review.googlesource.com/1086887
Reviewed-by: Adam Rice <ricea@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#564417}
Reviewed-on: https://chromium-review.googlesource.com/1090590
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/branch-heads/3440@{#235}
Cr-Branched-From: 010ddcfda246975d194964ccf20038ebbdec6084-refs/heads/master@{#561733}
[modify] https://crrev.com/5927f37c81c5c9647955091ffadd342b31748b4c/content/browser/loader/resource_dispatcher_host_impl.cc


### ca...@chromium.org (2018-06-07)

yhirano: Was that the last CL for this fix? If so, can this be marked as fixed? Thanks!

### yh...@chromium.org (2018-06-08)

> #51

No.

### ca...@chromium.org (2018-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-08-08)

Is this the bug that will track the changes to match the proposals added to the fetch spec: https://github.com/whatwg/fetch/pull/736 ?

### yh...@chromium.org (2018-08-09)

Yes, I'll implement it once the change is landed.

### an...@gmail.com (2018-08-16)

I've now landed the changed since nobody seemed to dislike them.

### an...@gmail.com (2018-08-16)

Note that I also wrote tests, available at https://github.com/web-platform-tests/wpt/pull/11432.

### yh...@chromium.org (2018-08-24)

I'm going to implement https://github.com/whatwg/fetch/pull/736.

### do...@gmail.com (2018-08-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-09-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/074455deb4bfb5b117c641f65b60f32471093878

commit 074455deb4bfb5b117c641f65b60f32471093878
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Thu Sep 06 14:01:27 2018

Strengthen requirements on CORS-safelisted request-headers

With this CL, some request headers that used to be treated as
CORS-safelisted are not CORS-safelisted any more. Specifically,

 - "accept", "accept-language" and "content-language" have a stronger
   check on its value
 - All headers whose value exceeds 128 bytes are treated as not
   CORS-safelisted
 - If the sum of value length of CORS-safelisted headers exceeds 1024,
   then all of them are treated as not CORS-safelisted.

This CL also implements
https://fetch.spec.whatwg.org/#no-cors-safelisted-request-header.

This is for https://github.com/whatwg/fetch/pull/736.

Bug: 824130
Cq-Include-Trybots: luci.chromium.try:linux_mojo
Change-Id: Ib12a7dbff6367717a43130ae59304dca55b7bf4e
Reviewed-on: https://chromium-review.googlesource.com/1196563
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Cr-Commit-Position: refs/heads/master@{#589153}
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/services/network/cors/cors_url_loader.cc
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/services/network/cors/preflight_controller.cc
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/services/network/public/cpp/cors/cors.cc
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/services/network/public/cpp/cors/cors.h
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/services/network/public/cpp/cors/cors_unittest.cc
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/services/network/public/cpp/cors/preflight_result.cc
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/services/network/public/cpp/cors/preflight_result_unittest.cc
[delete] https://crrev.com/ca58a477fe701fac2dcf129c534c8bb2b8f30172/third_party/WebKit/LayoutTests/external/wpt/fetch/api/cors/cors-preflight-not-cors-safelisted.any-expected.txt
[delete] https://crrev.com/ca58a477fe701fac2dcf129c534c8bb2b8f30172/third_party/WebKit/LayoutTests/external/wpt/fetch/api/cors/cors-preflight-not-cors-safelisted.any.worker-expected.txt
[delete] https://crrev.com/ca58a477fe701fac2dcf129c534c8bb2b8f30172/third_party/WebKit/LayoutTests/external/wpt/fetch/api/headers/headers-no-cors.window-expected.txt
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/third_party/blink/renderer/core/fetch/fetch_header_list.cc
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/third_party/blink/renderer/core/fetch/fetch_header_list.h
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/third_party/blink/renderer/core/fetch/fetch_header_list_test.cc
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/third_party/blink/renderer/core/fetch/headers.cc
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/third_party/blink/renderer/core/loader/threadable_loader.cc
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/third_party/blink/renderer/platform/loader/cors/cors.cc
[modify] https://crrev.com/074455deb4bfb5b117c641f65b60f32471093878/third_party/blink/renderer/platform/loader/cors/cors.h


### bu...@chromium.org (2018-09-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58

commit b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58
Author: Justin Donnelly <jdonnelly@chromium.org>
Date: Thu Sep 06 22:00:44 2018

Revert "Strengthen requirements on CORS-safelisted request-headers"

This reverts commit 074455deb4bfb5b117c641f65b60f32471093878.

Reason for revert: Suspected of causing check failures across a variety of tests on the Android CFI bot. See https://crbug.com/881538 for more details.

Original change's description:
> Strengthen requirements on CORS-safelisted request-headers
> 
> With this CL, some request headers that used to be treated as
> CORS-safelisted are not CORS-safelisted any more. Specifically,
> 
>  - "accept", "accept-language" and "content-language" have a stronger
>    check on its value
>  - All headers whose value exceeds 128 bytes are treated as not
>    CORS-safelisted
>  - If the sum of value length of CORS-safelisted headers exceeds 1024,
>    then all of them are treated as not CORS-safelisted.
> 
> This CL also implements
> https://fetch.spec.whatwg.org/#no-cors-safelisted-request-header.
> 
> This is for https://github.com/whatwg/fetch/pull/736.
> 
> Bug: 824130
> Cq-Include-Trybots: luci.chromium.try:linux_mojo
> Change-Id: Ib12a7dbff6367717a43130ae59304dca55b7bf4e
> Reviewed-on: https://chromium-review.googlesource.com/1196563
> Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
> Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#589153}

TBR=toyoshim@chromium.org,yhirano@chromium.org

Change-Id: I9952df291ff0aeaab0b50c6cff3de418b2272e71
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: 824130, 881538 
Cq-Include-Trybots: luci.chromium.try:linux_mojo
Reviewed-on: https://chromium-review.googlesource.com/1211958
Reviewed-by: Justin Donnelly <jdonnelly@chromium.org>
Commit-Queue: Justin Donnelly <jdonnelly@chromium.org>
Cr-Commit-Position: refs/heads/master@{#589323}
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/services/network/cors/cors_url_loader.cc
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/services/network/cors/preflight_controller.cc
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/services/network/public/cpp/cors/cors.cc
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/services/network/public/cpp/cors/cors.h
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/services/network/public/cpp/cors/cors_unittest.cc
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/services/network/public/cpp/cors/preflight_result.cc
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/services/network/public/cpp/cors/preflight_result_unittest.cc
[add] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/third_party/WebKit/LayoutTests/external/wpt/fetch/api/cors/cors-preflight-not-cors-safelisted.any-expected.txt
[add] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/third_party/WebKit/LayoutTests/external/wpt/fetch/api/cors/cors-preflight-not-cors-safelisted.any.worker-expected.txt
[add] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/third_party/WebKit/LayoutTests/external/wpt/fetch/api/headers/headers-no-cors.window-expected.txt
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/third_party/blink/renderer/core/fetch/fetch_header_list.cc
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/third_party/blink/renderer/core/fetch/fetch_header_list.h
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/third_party/blink/renderer/core/fetch/fetch_header_list_test.cc
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/third_party/blink/renderer/core/fetch/headers.cc
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/third_party/blink/renderer/core/loader/threadable_loader.cc
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/third_party/blink/renderer/platform/loader/cors/cors.cc
[modify] https://crrev.com/b39baca0258fc15e772b4bf6d2d5f5bfef3a8a58/third_party/blink/renderer/platform/loader/cors/cors.h


### bu...@chromium.org (2018-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3301bab535e31ab83871627aa38356586b452c5e

commit 3301bab535e31ab83871627aa38356586b452c5e
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Fri Sep 07 04:56:05 2018

Reland "Strengthen requirements on CORS-safelisted request-headers"

This is a reland of 074455deb4bfb5b117c641f65b60f32471093878

Original change's description:
> Strengthen requirements on CORS-safelisted request-headers
>
> With this CL, some request headers that used to be treated as
> CORS-safelisted are not CORS-safelisted any more. Specifically,
>
>  - "accept", "accept-language" and "content-language" have a stronger
>    check on its value
>  - All headers whose value exceeds 128 bytes are treated as not
>    CORS-safelisted
>  - If the sum of value length of CORS-safelisted headers exceeds 1024,
>    then all of them are treated as not CORS-safelisted.
>
> This CL also implements
> https://fetch.spec.whatwg.org/#no-cors-safelisted-request-header.
>
> This is for https://github.com/whatwg/fetch/pull/736.
>
> Bug: 824130
> Cq-Include-Trybots: luci.chromium.try:linux_mojo
> Change-Id: Ib12a7dbff6367717a43130ae59304dca55b7bf4e
> Reviewed-on: https://chromium-review.googlesource.com/1196563
> Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
> Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#589153}

Bug: 824130
Change-Id: Ia5caad12a51ee44713cf4cf11f42b1fc9ab831a9
Cq-Include-Trybots: luci.chromium.try:linux_mojo
Tbr: toyoshim@chromium.org
Reviewed-on: https://chromium-review.googlesource.com/1212425
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#589434}
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/services/network/cors/cors_url_loader.cc
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/services/network/cors/preflight_controller.cc
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/services/network/public/cpp/cors/cors.cc
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/services/network/public/cpp/cors/cors.h
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/services/network/public/cpp/cors/cors_unittest.cc
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/services/network/public/cpp/cors/preflight_result.cc
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/services/network/public/cpp/cors/preflight_result_unittest.cc
[delete] https://crrev.com/299669f962e6ab3d50f2e445f9878a1d07141263/third_party/WebKit/LayoutTests/external/wpt/fetch/api/cors/cors-preflight-not-cors-safelisted.any-expected.txt
[delete] https://crrev.com/299669f962e6ab3d50f2e445f9878a1d07141263/third_party/WebKit/LayoutTests/external/wpt/fetch/api/cors/cors-preflight-not-cors-safelisted.any.worker-expected.txt
[delete] https://crrev.com/299669f962e6ab3d50f2e445f9878a1d07141263/third_party/WebKit/LayoutTests/external/wpt/fetch/api/headers/headers-no-cors.window-expected.txt
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/third_party/blink/renderer/core/fetch/fetch_header_list.cc
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/third_party/blink/renderer/core/fetch/fetch_header_list.h
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/third_party/blink/renderer/core/fetch/fetch_header_list_test.cc
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/third_party/blink/renderer/core/fetch/headers.cc
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/third_party/blink/renderer/core/loader/threadable_loader.cc
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/third_party/blink/renderer/platform/loader/cors/cors.cc
[modify] https://crrev.com/3301bab535e31ab83871627aa38356586b452c5e/third_party/blink/renderer/platform/loader/cors/cors.h


### yh...@chromium.org (2018-09-07)

https://crbug.com/chromium/2 (at #1) is fixed.

### yh...@chromium.org (2018-09-10)

I think some are FIXED and others are WONTFIX, right? Feel free to reopen if I'm wrong.

### mm...@chromium.org (2018-09-10)

Thanks for the great work, Jianjun Chen!

### wh...@gmail.com (2018-09-10)

Great! Thank Yutaka and Matt for implementing the fix. Thank Anne for the specification improvement. Thank all of you for the valuable discussion.

### aw...@chromium.org (2018-09-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-28)

Hi whucjj@! Thanks for the report. The Chrome VRP panel decided to award $2,000 for this report. A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in Chrome release notes?

### aw...@chromium.org (2018-09-28)

[Empty comment from Monorail migration]

### wh...@gmail.com (2018-09-28)

Hi Andrew, thank you very much for the generous reward. I think "Jianjun Chen(@whucjj) from Tsinghua University" is OK for the credit. 

Again, thanks to all Chrome and Chromium team members for bring us such excellent products. 

### an...@gmail.com (2018-11-07)

I filed https://crbug.com/chromium/902681 as a follow-up, in public, since most of the standards work is already public.

### bu...@chromium.org (2018-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bb3ab7dd37f12b9cc28333cd7e84a89d0fd2bbb0

commit bb3ab7dd37f12b9cc28333cd7e84a89d0fd2bbb0
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Thu Nov 15 09:15:15 2018

Fix CORS-unsafe request-header byte

Bytes greater than 0x7f should not be considered as unsafe.

This CL also replaces "utf8" character conversions in
blink/renderer/platform/loader/cors/cors.cc to "latin1" as it's what's
done when actually converting blink::HTTPHeaderMap to
net::HttpRequestHeaders.

Bug: 824130, 902681
Change-Id: I01aacf814f1fc8a3ab8f191e1a9ec2bd01c1efee
Reviewed-on: https://chromium-review.googlesource.com/c/1335049
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#608300}
[modify] https://crrev.com/bb3ab7dd37f12b9cc28333cd7e84a89d0fd2bbb0/services/network/public/cpp/cors/cors.cc
[modify] https://crrev.com/bb3ab7dd37f12b9cc28333cd7e84a89d0fd2bbb0/services/network/public/cpp/cors/cors_unittest.cc
[modify] https://crrev.com/bb3ab7dd37f12b9cc28333cd7e84a89d0fd2bbb0/third_party/blink/renderer/platform/loader/cors/cors.cc


### sh...@chromium.org (2018-12-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/824130?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Loader, Blink>Network>FetchAPI, Blink>SecurityFeature>CORS, Internals>Network]
[Monorail mergedwith: crbug.com/chromium/826874]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090870)*
