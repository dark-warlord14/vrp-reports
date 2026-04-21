# Security: = prepended in document.cookie allows to bypass __Secure and __Host prefixes

| Field | Value |
|-------|-------|
| **Issue ID** | [40060319](https://issues.chromium.org/issues/40060319) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Cookies |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2022-40958 |
| **Reporter** | ha...@gmail.com |
| **Assignee** | bi...@chromium.org |
| **Created** | 2022-07-18 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

document.cookie = "=\_\_Host-test=a" allows one to set cookie with \_\_Host-test=a

**VERSION**  

Chrome Version: [103.0.5060.114]  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Go to <http://httpbin.org/headers> and execute in console document.cookie = "=\_\_Host-test=a"
2. Now "Cookie": "\_\_Host-test=a" will appear as a header in <http://httpbin.org/headers>. It should not happen as \_\_Host- and \_\_Secure- prefixed cookies should only be set in secure context.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Timeline

### ha...@gmail.com (2022-07-18)

Additional notes: Also reproduces with Set-Cookie header

The pertinent issue is that when document.cookie = "=__Host-test=a" is executed, the name of the cookie is empty, and the value of the cookie is "=__Host-test=a". The unexpected result is that "__Host-test=a" value gets sent instead of "=__Host-test=a"

### ha...@gmail.com (2022-07-18)

I recommend rejecting cookies with empty names as a fix for this problem

### [Deleted User] (2022-07-18)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-18)

It does seem weird to allow a cookie with an empty name (and from some initial testing, it seems like Firefox doesn't allow a cookie with an empty name).

https://www.rfc-editor.org/rfc/rfc6265#section-5.2:~:text=If%20the%20name%20string%20is%20empty%2C%20ignore%20the%20set%2Dcookie%2Dstring%0A%20%20%20%20%20%20%20entirely. says to ignore set-cookie-string with an empty cookie name.

Though https://httpwg.org/specs/rfc6265.html#storage-model doesn't seem to mention this (not sure if this is an oversight).

I'm not 100% sure if this is a security bug; I'm setting this to low for now out of caution; however, hitting this problematic case requires the site itself to be doing weird things.

[Monorail components: Blink>Storage>CookiesAPI]

### [Deleted User] (2022-07-18)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-18)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-18)

Not sure why Monorail is warning about bounced emails to dylancutler@; moved to CC out of an abundance of caution.

Taking this out of the security queue too; I don't think that this is something that can really be exploited, though a buggy site could certainly do bad things to itself.

### ha...@gmail.com (2022-07-18)

Thanks for the reply, I am curious why you are not 100% sure this is a security bug? The impact of this is being able to bypass __Host- and __Secure- prefix restrictions which are security measures designed to counteract the problem of session fixation from non-secure origin. From a comment about only a buggy site being able to set a cookie, I think there is a confusion of what __Host- and __Secure- prefixed cookies do.

Cookies have been known to be vulnerable to the Weak Integrity problem. For example, a MITM attacker can spoof a HTTP site, and thus cause the browser to set cookies for the domain. A compromised subdomain can also set a cookie for a parent domain. This causes what is known as session fixation.

__Host- and __Secure- prefixing are designed by the browser to counteract against this, see https://bugs.chromium.org/p/chromium/issues/detail?id=567867. Basically, __Secure- prefixed cookies can only be set from a secure origin while __Host- can only be set from a secure origin and cannot specify the Domain attribute.

### ha...@gmail.com (2022-07-18)

See this also: https://googlechrome.github.io/samples/cookie-prefixes/

Can the severity get re-evaluated with the information about __Secure- and __Host- prefixes being taken into account

### mo...@chromium.org (2022-07-18)

Yeah, this does look bad...


### dc...@chromium.org (2022-07-18)

I think it's pretty clear it's a bug in the implementation in that we don't restrict it.

But it's not actually a direct risk to the security of end users; it requires the site itself to be buggy and setting cookies with an empty name (i.e. a malicious third-party can't use this bug). I think this is less severe than the partial CSP bypass that is given as an example of a low severity bug (https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-low-severity).

That being said, I do think we should fix this; if nothing else, for better cross-browser compatibility.

### ha...@gmail.com (2022-07-18)

Also the cookie name is stored empty in the browser, but the result is that the cookie is based on the entire cookie value:

So the cookie store will look like this
[EMPTY] | __Host-test=a
but the browser sends the header Cookie: __Host-test=a to the website. It is NOT due to a buggy website misinterpreting a cookie. 

If you are thinking about the site itself setting a cookie with an empty name, the attack scenario is that a malicious MITM or a compromised subdomain can set these prefixed cookies for a victim site to perform session fixation, effectively bypassing what this prefixes are meant to protect against.

I believe I have addressed the confusing parts. Hopefully, this clears up the confusion?


### dc...@chromium.org (2022-07-18)

+morlovich, can you weigh in on what you think the appropriate severity is here?

### ha...@gmail.com (2022-07-18)

Please let me know if you have any further questions in understanding why this is a security problem and I'll be able to help.

### dc...@chromium.org (2022-07-18)

I understand the issue with the Cookie: header, but I will admit I missed the MITM possibility in the analysis.

Given that HSTS bypass is considered medium, this is what I'm inclined to triage this at as well.

A site that doesn't serve any traffic on HTTP and only on HTTPS would not be vulnerable to this.

### dc...@chromium.org (2022-07-18)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-07-18)

Thanks! I would like to apologise for not including that part in earlier too! 😅

### ha...@gmail.com (2022-07-18)

> A site that doesn't serve any traffic on HTTP and only on HTTPS would not be vulnerable to this.

That's not true. A MITM can actually trick the user to click on a HTTP link and impersonate the HTTP site, even without the actual site serving HTTP traffic itself.
The only mitigation I can see, is the target site being HSTS preloaded on the browser (meaning that the browser is forced to only connect to the site on HTTPS and not HTTP)

I agree with the Medium severity. :)

### ha...@gmail.com (2022-07-19)

> The only mitigation I can see, is the target site being HSTS preloaded on the browser (meaning that the browser is forced to only connect to the site on HTTPS and not HTTP)

There is also the case of a compromised subdomain being able to set a cookie for the parent domain, bypassing what the __Host- prefix is meant to protect against. In that scenario no MITM is involved and HSTS does not mitigate this

I'll stop overanalysing this bug now :)

If you need any help in fix suggestion (I recommend rejecting empty cookie names as a fix to this problem.) or fix verification, feel free to ask more questions.

### mo...@chromium.org (2022-07-19)

Your suggestion is probably the best way of doing things as far as having a well-designed system is, but This is the Web(tm) so if we do it there is a good chance that it will turn out some important site relies on setting cookies with no name, and the urgency of a security fix will not really give us much of an opportunity to find that out w/o affecting the users.

There are also spec implications, see https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis-10#section-5.5 step 2 and https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis-10#section-5.6.3 step 4 (and the parsing algorithm in 5.4) --- this probably needs to be changed, too.

The conservative but very, very, very, ugly thing would be to search for =__Host and =__Secure in values of nameless cookies.  

I think Firefox actually rejects nameless cookies, though, so maybe there is a chance that doing the nice thing actually does work for a change (funnily our own behavior comes from trying to be Mozilla-compatible).

### mo...@chromium.org (2022-07-19)

+Mike for an opinion from someone involved(?) in the spec side of things?


### ha...@gmail.com (2022-07-19)

Firefox also has this problem too, I have also reported it to them with the same suggestion. Do you want me to cc you in the Bugzilla form?

Regarding empty cookie names, I am not sure if empty cookie names are even used in the wild, considering it is broken in the first place. Considering that a cookie store like the following

[EMPTY] | a

The cookie header will result in the browser sending the following cookie header, without any = sign. :

"Cookie": "a"

Thus, the cookie header sent by Chrome/Firefox when there is an empty name is malformed anyway as there is no = sign. Therefore, that's why I think the way to go about this is to reject empty cookie names as they break the cookie headers Chrome / Firefox use anyway 

### mo...@chromium.org (2022-07-19)

The non-= thing for Cookie: is actually in the spec, and how it's long worked. 

As for firefox, I tested on Firefox 91.11.0esr, but maybe that got changed in more recent non-ESR version?

I would indeed appreciate if you could connect me to the Mozilla folks working on this, as morlovich@google.com --- it may be good to come up with a consistent solution.

(I am leaning more towards "nameless cookies shouldn't have = in value", though maybe our spec people will suggest something else).


### ha...@gmail.com (2022-07-19)

Ah, didn't quite know about the non-= thing, 

Firefox doesn't allow cookies to be set in json Content-Type, so you actually have to go to http://httpbin.org to set the cookie before http://httpbin.org/headers

I'll cc you in the bugzilla form (they haven't yet triaged it though)

### ha...@gmail.com (2022-07-19)

I have cc'ed morlovich@google.com in the bugzilla form, can you confirm?

### mo...@chromium.org (2022-07-19)

It worked, thank you. And you were right: re: JSON mimetype making the difference in Firefox.

### mo...@chromium.org (2022-07-20)

So update: there is a problem in enforcing a combination property on name & value, since there is an extension API that changes them one at a time, so things can break if intermediate states look bad but final doesn't. 

So I am thinking of an alternate change: don't drop the leading = if the value has a =, too.  This has the advantage of being a tiny change, too, much simpler to review.

(Also WebLayer is using that + direct ParsedCookie to get back original serialization. ugh.)




### ha...@gmail.com (2022-07-20)

Imo, that sounds like the best solution to me without breaking much.

I think the vulnerability is also present in the parser algorithm of the RFC6265bis-10 spec so it needs to get updated there well, more specifically Step 4 of https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis-10#section-5.6.3. Any UAs that implements the RFC the strictly will likely be vulnerable.


### mo...@chromium.org (2022-07-20)

More context is related spec discussion:
https://github.com/httpwg/http-extensions/issues/1210

Looks like they were too worried about compatibility to accept specifying the serialization change, but it looks like they didn't think of the __Host/__Secure case...

(Serialization change in https://chromium-review.googlesource.com/c/chromium/src/+/3777298 ... we could also narrow it to search for =__Host or =_Secure, which is ugly but less likely to break people doing weird stuff)



### ha...@gmail.com (2022-07-20)

The narrowing it down to search for =__Host or =_Secure is okay as well, but beware of the OWS chars SP/HT between the = and the __Host

For instance, if I were to specify

=[OWS]__Host-test=a

The cookie header the browser will send:

Cookie: [OWS]__Host-test=a

Server will ignore [OWS] and interpret as __Host-test=a



### mi...@chromium.org (2022-07-20)

> https://www.rfc-editor.org/rfc/rfc6265#section-5.2:~:text=If%20the%20name%20string%20is%20empty%2C%20ignore%20the%20set%2Dcookie%2Dstring%0A%20%20%20%20%20%20%20entirely. says to ignore set-cookie-string with an empty cookie name.

We probably want to ignore 6265, and look at 6265bis instead.

5.4.3 of https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis#section-5.4 states:

>If the name-value-pair string lacks a %x3D ("=") character, then the name string is empty, and the value string is the value of name-value-pair.
> Otherwise, the name string consists of the characters up to, but not including, the first %x3D ("=") character, and the (possibly empty) value string consists of the characters after the first %x3D ("=") character.

So "=__Host-test=a" should be considered a valueless cookie, not a nameless cookie - the name is "__Host-test=a", per spec. Do we know where the leading `=` is getting dropped?

Aside: it's not great that the following works as the result of this bug: `document.cookie="=__Host-lol=3; Path=/headers"` - __Host cookies require "Path=/" and Secure. I suppose we could in theory also do some kind of __Host and __Secure constraint validation when pulling from the cookie jar as well, maybe as follow up work.





### mi...@chromium.org (2022-07-20)

> Do we know where the leading `=` is getting dropped?

Ah, nevermind. 

> Otherwise, the name string consists of the characters up to, but not including, the first %x3D ("=") character, and the (possibly empty) value string consists of the 
 characters after the first %x3D ("=") character.

### bi...@chromium.org (2022-07-20)

I think that searching for and rejecting nameless cookies with such problematic values is our best bet in terms of patching this hole while not causing other compatibility breakage elsewhere.

Actually, we should consider taking it one step further and look for nameless cookies that are prefixed with "__Secure-" or "__Host-" AND have a subsequent '=' somewhere. Cookie values are meant to be opaque and while a foot gun the cookie `Set-Cookie: =__Host-abcdefg` shouldn't be interpreted as a named cookie IF the server is parsing correctly (which is probably a big if).

Still, I am leaning toward proposing that the spec and Chrome be changed to reject any nameless cookies whose value is prefixed by:
`BWS "__Secure-" *cookie-octet "="` 
or
`BWS "__Host-" *cookie-octet "="` 
(I.e.: Optional whitespace followed by a cookie name prefix literal followed by a '=' somewhere)

It feels more correct in that it only captures values that are directly imitating named cookies and ignores technically fine (but foot gunny) values that "happen" to contain cookie prefix names. Open to feedback.



[Monorail components: -Blink>Storage>CookiesAPI Internals>Network>Cookies]

### [Deleted User] (2022-07-20)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mo...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-07-21)

@bingler, that seems okay as well.

Is there any reason why servers send cookie pairs such as =a=b instead of a=b outright? If the purpose of this special parsing was to accommodate servers which mistakenly send a cookie pair that starts with an =, I was thinking of adding a pre-processing step to when the UA receives the cookie pair, but before it splits the cookie pair into the cookie name and cookie value:

If the cookie pair starts with an = character, and there are at least two = characters in the cookie pair, then remove the leading = character before splitting the cookie pair into cookie name and cookie value

That way UAs can still support servers that erroneously send "=a=b", and if a legitimate server sends for instance a cookie pair "=__Host-test=b", UAs can support them as well.






### ha...@gmail.com (2022-07-21)

> If the cookie pair starts with an = character, and there are at least two = characters in the cookie pair, then remove the leading = character before splitting the cookie pair into cookie name and cookie value

Someone can still bypass the proposed patch above by preceding two =, (ie. ==__Host-test=a with the leading '=' removed will result in =__Host-test=a which will then get translated to [EMPTY] | __Host-test=a in the cookie store.

Thus, I propose the following:

If the cookie pair starts with an = character, and there are at least two = characters in the cookie pair, and there is at least one cookie octet in between the leading = character and the second = character, then remove the leading = character before splitting the cookie pair into cookie name and cookie value.

Running the above solution will result:

=__Host-test=a will result in __Host-test=a with the leading character which will then get translated to __Host-test | a in the cookie store.

==__Host-test=a will result in ==__Host-test=a since there isn't at least one cookie octet which will then get translated to EMPTY | =__Host-test=a in the cookie store which isn't a problem.

### bi...@chromium.org (2022-07-21)

> Is there any reason why servers send cookie pairs such as =a=b instead of a=b outright?

I can only guess why some servers do what they do, but I expect that if they send =a=b that they're not interested in a setting a cookie with
name: "a"
value : "b"

but rather they just want to store the literal string "a=b" (I doubt most usages are that simple).
I've seen some cookies where the cookie's value is a dictionary of some sort:
E.x.: `Set-Cookie: foo_dict=key1=value1,key2=value2` becomes
name: "foo_dict"
value: "key1=value1,key2=value2"

It's unfortunate that cookies are allowed both to set nameless cookies and use the '=' char in their value string, but here we are.

Because of that I don't believe we can implement your preprocessing idea as a cookie `Set-Cookie: =key1=value1,key2=value2` will become (if I'm understanding it correctly)
name: "key1"
value: "value1,key2=value2"

Which is quite different and likely to break the server.

Because cookie values are meant to be opaque to the UA (i.e.: we don't make any effort to parse or understand it) I'm hesitant to do any more parsing of the value than is strictly necessary to catch the offending string prefixes.

> Someone can still bypass the proposed patch above by preceding two =, (ie. ==__Host-test=a with the leading '=' removed will result in =__Host-test=a which will then get translated to [EMPTY] | __Host-test=a in the cookie store.

I believe this isn't a concern if we don't perform the preprocessing. 

What should happen (roughly) is:
* Chrome receives a request to create a cookie from `cookie_string`
* `cookie_string` is "==__Host-test=a"
* Following rfc6265bis we determine that
  cookie_name: ""
  cookie_value: "=__Host-test=a"
*We then search `cookie_value` for a prefix of `BWS "__Host-" *cookie-octet "="` 
* Because we encounter "=" first instead of `BWS` or "_" we abort the check as this cookie isn't prefixed with the problematic string.
* The cookie is stored
* When we send a request to the server we'll attach
   "=__Host-test=a"

The last step is the only one that raises my eyebrow, but it's still safe since we send nameless cookies without a preceding "=" and any properly configured server should interpret that as the cookie's value.

### bi...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### dv...@mozilla.com (2022-07-22)

> > Is there any reason why servers send cookie pairs such as =a=b instead of a=b outright?
> I can only guess why some servers do what they do, but I expect that if they send =a=b that they're not interested in a setting a cookie with name: "a" value : "b"

Do we know that there are, in fact, servers that send nameless cookies with an embedded equals? Or maybe more specifically, nameless cookies with an equal sign close enough to the start that it looks like an embedded name=value and not chunks of base64 with '=' padding at the end?

Mozilla doesn't have telemetry on anything like that, and we don't even know of an anecdotal single instance. Unfortunately our telemetry implementation/approval/shipping/gathering pipeline is way too slow to help guide a fix for this bug. As a short-term fix I fully support the solution in https://crbug.com/chromium/1345193#c33 as effective and conservative. I'm less happy about baking that into the spec if future data shows we could block these more broadly (e.g. like § 7.2 step 2 of the Cookie Store API https://wicg.github.io/cookie-store/#set-cookie-algorithm -- at least as of the 2022-07-06 draft)

### dv...@mozilla.com (2022-07-22)

My concern is with other named cookies. Hypothetically an attacker could perform session fixation by creating a fake "sessionid=" nameless cookie that doesn't get overwritten by the site when the user logs in and sets the real sessionid cookie. Depending on the order cookies are sent the fake one might be the one used by that web app.

### bi...@chromium.org (2022-07-22)

> As a short-term fix I fully support the solution in https://crbug.com/chromium/1345193#c33

We'd prefer to do this in concert with Firefox, so I'm glad we're in agreement. We'll begin implementing our fix and getting it merged.

I see in https://bugzilla.mozilla.org/show_bug.cgi?id=1779993#c14 that you're skipping 102, I assume this is because your 103 release is coming up soon? Or is there another reason?

> Do we know that there are, in fact, servers that send nameless cookies with an embedded equals?

I do not, and I do not have any data indicating one way or the other.
We know there are named cookies that use '=' within their values, and we know that nameless cookies exist. Assuming that the union of those two exist feels the safest.

> I'm less happy about baking that into the spec if future data shows we could block these more broadly 

I'm open to discussion on the other cookies, but given the security implications of the cookie name prefixes I feel it's still worthwhile to call those out specifically (even if a more general decision is made). But I'll save the rest of my thoughts for a different forum. Such as the eventual spec github issue that I'll file once both our fixes are implemented.

### mo...@chromium.org (2022-07-22)

[Empty comment from Monorail migration]

### mo...@chromium.org (2022-07-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f9580905b45edb8dfe7da6cd5f26421ab2b5c285

commit f9580905b45edb8dfe7da6cd5f26421ab2b5c285
Author: sbingler <bingler@chromium.org>
Date: Mon Jul 25 23:36:46 2022

Don't allow cookies with hidden cookie prefixes

Prevent the creation of any cookies that have an empty name field and
whose value impersonates a cookie name prefix.

This will also delete any previously stored cookies that meet the
conditions by causing them to fail their IsCanonical() check.

Bug: 1345193
Change-Id: I7e1adef3391bb7caee183204bb609cd63bcdaea7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3782906
Commit-Queue: Steven Bingler <bingler@chromium.org>
Reviewed-by: Maks Orlovich <morlovich@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1028000}

[modify] https://crrev.com/f9580905b45edb8dfe7da6cd5f26421ab2b5c285/net/cookies/canonical_cookie_unittest.cc
[modify] https://crrev.com/f9580905b45edb8dfe7da6cd5f26421ab2b5c285/net/cookies/canonical_cookie.cc
[modify] https://crrev.com/f9580905b45edb8dfe7da6cd5f26421ab2b5c285/net/cookies/canonical_cookie.h


### bi...@chromium.org (2022-07-26)

Request merge for extended, stable, and beta. 

CL (https://crbug.com/chromium/1345193#c45) missed the most recent canary build but I'm requesting merge now in case any discussion is needed.
The issue is not reproducible on ToT

### bi...@chromium.org (2022-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-26)

Merge review required: M104 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-26)

Merge review required: M103 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-26)

Merge review required: M102 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bi...@chromium.org (2022-07-27)

1. This is a medium severity security fix.
2. https://chromium-review.googlesource.com/c/chromium/src/+/3782906
3. Yes. I am unable to reproduce the issue on today's canary build.
4. No
5 No
6. Yes. 
*  Go to http://httpbin.org/headers and execute in console `document.cookie = "=__Host-test=a"`
* Refresh the page
* The test is considered passed if `"Cookie": "__Host-test=a",` does not appear in the page body.
 * Repeat steps for `document.cookie = "=__Secure-test=a"`

### bi...@chromium.org (2022-07-27)

@haxatron1@gmail.com

If possible, could please attempt to reproduce the issue using the latest canary build?
https://www.google.com/chrome/canary/

### ha...@gmail.com (2022-07-27)

I tested on canary and can confirm that executing the following in console will no longer save the cookies.
document.cookie="=__Host-test=a"
document.cookie="=__Secure-test=a"

In addition, I also tested setting the Set-Cookie headers on my local server and confirmed that the cookie is not saved.

Set-Cookie: =__Host-test=a
Set-Cookie: =__Secure-test=a

Therefore the vulnerability is fixed.

### [Deleted User] (2022-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-28)

Hello, bingler@, thank you for fixing this security bug. As there are no further planned releases of M103/stable and M102/Extended, I'm removing those labels accordingly. 
M104 Stable has already been cut for testing and QA before next week's release. This fix can be instead included in the M104 respin. 

This fix should also be backmerged to M105/dev which will soon be promoted to beta, so adding merge review for that accordingly. 

In the future, please simply update resolved security bugs to Fixed. Sheriffbot will take care of appropriate merge labeling based on severity, appropriate release branches, and timing of release cycle. Thank you. 

### am...@chromium.org (2022-07-28)

Also, thank you for responding to the merge review questionnaire in https://crbug.com/chromium/1345193#c51. Since this fix just landed on Canary about 24 hours ago, I'd like to allow it some more bake time on canary before reviewing for backmerge to 105 and 104. 

### mi...@chromium.org (2022-07-29)

Tagging as LTS-Merge-Candidate, as this would be important to get in M102 for ChromeOS users.

### rz...@google.com (2022-08-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

Presuming there are no stability issues or other concerns, please merge this fix to M105 (branch 5195) at your earliest convenience so this fix can be included in the M105 beta cut. 

The release team has requested a brief pause on merges to M104, so leaving this in the review queue for later merge approval at the appropriate time. 

### bi...@chromium.org (2022-08-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a6c6c86973b58da0873623dd6e1d7f66714c4588

commit a6c6c86973b58da0873623dd6e1d7f66714c4588
Author: sbingler <bingler@chromium.org>
Date: Tue Aug 02 18:46:09 2022

Don't allow cookies with hidden cookie prefixes

Prevent the creation of any cookies that have an empty name field and
whose value impersonates a cookie name prefix.

This will also delete any previously stored cookies that meet the
conditions by causing them to fail their IsCanonical() check.

(cherry picked from commit f9580905b45edb8dfe7da6cd5f26421ab2b5c285)

Bug: 1345193
Change-Id: I7e1adef3391bb7caee183204bb609cd63bcdaea7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3782906
Commit-Queue: Steven Bingler <bingler@chromium.org>
Reviewed-by: Maks Orlovich <morlovich@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028000}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3805460
Auto-Submit: Steven Bingler <bingler@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5195@{#166}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/a6c6c86973b58da0873623dd6e1d7f66714c4588/net/cookies/canonical_cookie_unittest.cc
[modify] https://crrev.com/a6c6c86973b58da0873623dd6e1d7f66714c4588/net/cookies/canonical_cookie.cc
[modify] https://crrev.com/a6c6c86973b58da0873623dd6e1d7f66714c4588/net/cookies/canonical_cookie.h


### rz...@google.com (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-03)

1. Just https://crrev.com/c/3803167
2. Low, no conflicts, but the author had to fix a failing test case.
3. 105
4. Yes

### am...@chromium.org (2022-08-04)

M104 merge approved, please go ahead and merge this fix to branch 5112 at your earliest convenience 

### gi...@appspot.gserviceaccount.com (2022-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fda728b799869fc0832b837d827b4ba9d267eef2

commit fda728b799869fc0832b837d827b4ba9d267eef2
Author: sbingler <bingler@chromium.org>
Date: Fri Aug 05 17:02:43 2022

Don't allow cookies with hidden cookie prefixes

Prevent the creation of any cookies that have an empty name field and
whose value impersonates a cookie name prefix.

This will also delete any previously stored cookies that meet the
conditions by causing them to fail their IsCanonical() check.

(cherry picked from commit f9580905b45edb8dfe7da6cd5f26421ab2b5c285)

Bug: 1345193
Change-Id: I7e1adef3391bb7caee183204bb609cd63bcdaea7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3782906
Commit-Queue: Steven Bingler <bingler@chromium.org>
Reviewed-by: Maks Orlovich <morlovich@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028000}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3812403
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Steven Bingler <bingler@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#1400}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/fda728b799869fc0832b837d827b4ba9d267eef2/net/cookies/canonical_cookie_unittest.cc
[modify] https://crrev.com/fda728b799869fc0832b837d827b4ba9d267eef2/net/cookies/canonical_cookie.cc
[modify] https://crrev.com/fda728b799869fc0832b837d827b4ba9d267eef2/net/cookies/canonical_cookie.h


### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-10)

1. Just https://crrev.com/c/3816934
2. Low, no conflicts but a build failure in the unit tests because the interface of CreateUnsafeCookieForTesting changed
3. 105
4. Yes

### mi...@chromium.org (2022-08-11)

For question 3 in the above comment, this has also been merged to 104 (see https://crbug.com/chromium/1345193#c67).

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-11)

Congratulations, Axel! The VRP Panel has decided to award you $2,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in reporting this issue to us and as it was worked to be resolved. Nice work! 

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### mi...@chromium.org (2022-08-15)

Coincidentally, someone posted about this type of attack on the 6265bis spec draft repo: https://github.com/httpwg/http-extensions/issues/2229

### ha...@gmail.com (2022-08-15)

I read that Github issue and its actually quite different. Their issue talks about the case of Set-Cookie: __Host-xsrf (without the preceding '=') which can only set a cookie __Host-xsrf with an empty value. I am not too sure about their described attack of defeating double CSRF protection though.

### dv...@mozilla.com (2022-08-16)

Yes, but then they worked their way to the same eventual conclusion and realized they shouldn't add any more to the GH issue. Instead they filed bugs against Firefox and Chrome that are essentially duplicates. They're arguing that the limited prefix rejection implemented here isn't sufficient. That may be, but it's cleaner to argue that in the new bug https://bugs.chromium.org/p/chromium/issues/detail?id=1351601 since this one has a fix and has been merged. 

Could I get access to crbug 1351601, please?

### ha...@gmail.com (2022-08-16)

It looks like the fix in https://bugs.chromium.org/p/chromium/issues/detail?id=1345193#c33 should be adjusted to cover the case where some servers interpret "__Host-test" as a nameless cookie.

So instead of 

`BWS "__Secure-" *cookie-octet "="
or
`BWS "__Host-" *cookie-octet "="

it should be:

`BWS "__Secure-" *cookie-octet
or
`BWS "__Host-" *cookie-octet

### am...@chromium.org (2022-08-16)

Hi dveditz@, I've cc'ed you to https://crbug.com/chromium/1351601 so you should have access to it now, thanks for digging into this

### am...@chromium.org (2022-08-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2f19801aeb77b140609594c6418d67cf6c2a7195

commit 2f19801aeb77b140609594c6418d67cf6c2a7195
Author: sbingler <bingler@chromium.org>
Date: Tue Aug 16 15:54:47 2022

[M102-LTS] Don't allow cookies with hidden cookie prefixes

M102 merge issues:
  Build failures in the unit tests because the interface of
  CreateUnsafeCookieForTesting changed

Prevent the creation of any cookies that have an empty name field and
whose value impersonates a cookie name prefix.

This will also delete any previously stored cookies that meet the
conditions by causing them to fail their IsCanonical() check.

(cherry picked from commit f9580905b45edb8dfe7da6cd5f26421ab2b5c285)
(cherry picked from commit e118b7e282002908b0135a2107fec25cedc4436e)

Bug: 1345193
Change-Id: I7e1adef3391bb7caee183204bb609cd63bcdaea7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3782906
Commit-Queue: Steven Bingler <bingler@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028000}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3816934
Owners-Override: Michael Ershov <miersh@google.com>
Reviewed-by: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1305}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/2f19801aeb77b140609594c6418d67cf6c2a7195/net/cookies/canonical_cookie_unittest.cc
[modify] https://crrev.com/2f19801aeb77b140609594c6418d67cf6c2a7195/net/cookies/canonical_cookie.cc
[modify] https://crrev.com/2f19801aeb77b140609594c6418d67cf6c2a7195/net/cookies/canonical_cookie.h


### gi...@appspot.gserviceaccount.com (2022-08-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fd17c8980cae5ee6b7a23ff4a964f26ae2328702

commit fd17c8980cae5ee6b7a23ff4a964f26ae2328702
Author: sbingler <bingler@chromium.org>
Date: Tue Aug 16 16:42:16 2022

[M96-LTS] Don't allow cookies with hidden cookie prefixes

Prevent the creation of any cookies that have an empty name field and
whose value impersonates a cookie name prefix.

This will also delete any previously stored cookies that meet the
conditions by causing them to fail their IsCanonical() check.

(cherry picked from commit f9580905b45edb8dfe7da6cd5f26421ab2b5c285)

Bug: 1345193
Change-Id: I7e1adef3391bb7caee183204bb609cd63bcdaea7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3782906
Commit-Queue: Steven Bingler <bingler@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1028000}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3803167
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Steven Bingler <bingler@chromium.org>
Reviewed-by: Michael Ershov <miersh@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1685}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/fd17c8980cae5ee6b7a23ff4a964f26ae2328702/net/cookies/canonical_cookie_unittest.cc
[modify] https://crrev.com/fd17c8980cae5ee6b7a23ff4a964f26ae2328702/net/cookies/canonical_cookie.cc
[modify] https://crrev.com/fd17c8980cae5ee6b7a23ff4a964f26ae2328702/net/cookies/canonical_cookie.h


### am...@google.com (2022-08-16)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-16)

[Empty comment from Monorail migration]

### bi...@chromium.org (2022-08-16)

[Empty comment from Monorail migration]

### bi...@chromium.org (2022-08-17)

+CC squarcina@
Who filed https://crbug.com/chromium/1351601

### ha...@gmail.com (2022-09-24)

This issue has been fixed in Firefox as well as CVE-2022-40958: Bypassing Secure Context restriction for cookies with __Host and __Secure prefix - https://www.mozilla.org/en-US/security/advisories/mfsa2022-41/#CVE-2022-40958

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1345193?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1351601]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060319)*
