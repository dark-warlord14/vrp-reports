# Generic CORS bypass that enables Cross-Site-Tracing (XST)

| Field | Value |
|-------|-------|
| **Issue ID** | [40060925](https://issues.chromium.org/issues/40060925) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>CORS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2022-09-11 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description


Generic CORS bypass that enables Cross-Site-Tracing (XST)


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


#### Which URL (or repository) have you found the vulnerability in?

all


---

### The problem


#### Please describe the technical details of the vulnerability

For several years, all the main browsers have all blocked the direct use of the TRACE method through fetch and XMLHttpRequest.

This is because a successful Cross-SiteTracing (XST) attack will expose credentials via authorization headers and cookies protected with httponly attributes. 

To bypass this restriction you can simply add an "X-Http-Method-Override: TRACE" header.

To be successful, this obviously requires a server that supports the TRACE method, and the X-Http-Method-Override header. If so, then any XSS issue can be leveraged into a full compromise of the session/authentication credentials.

```
fetch( 'https://realtime.www.linkedin.com/realtime/connect', {
   method: 'GET',
   mode: 'cors',
   headers: {
      'x-http-method-override': 'TRACE'
   }
} );
```




#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

An attacker can leverage the XSS/XST to bypass the browser protections and gain access to the session/authentication credentials.


---

### The cause


#### What version of Chrome have you found the security issue in?

all


#### Is the security issue related to a crash?

No


#### Choose the type of vulnerability

Other


#### How would you like to be publicly acknowledged for your report?

scarlet




## Timeline

### ch...@appspot.gserviceaccount.com (2022-09-11)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-09-12)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-09-13)

Seems related to https://crbug.com/1340879 , though that issue doesn't explicitly state "block trace methods". 
Setting severity and found-in per 1340879, and assigning to owner of that issue.
peconn, please feel free to mark this as a duplicate if desired. 

[Monorail components: Blink>SecurityFeature>CORS]

### [Deleted User] (2022-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-13)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2022-09-13)

Hi,

It appears this issue affects all the main browsers, and it also appears that the description above may not be the clearest possible.

I'll have another go at explaining, which should hopefully clear things up.

So a normal CORS fails because the TRACE method is blocked. This is something inherrent in all the major browsers, and was a deliberate change to stop XST.

You can see this in action if you browse to https://www.linkedin.com, then paste the following into the browser console. You'll see the browser block the request. All good.
```
fetch( 'https://realtime.www.linkedin.com/realtime/connect', {
      method: 'TRACE',
      mode: 'cors',
      cache: 'no-store'
} ).then( response => { console.log( response ) } ) 
```
Now instead, paste in the following. The CORS succeeds and the TRACE overide is sent. Not so good.
```
fetch( 'https://realtime.www.linkedin.com/realtime/connect', {
      method: 'GET',
      mode: 'cors',
      cache: 'no-store',
      headers: {
            'x-http-method-override': 'TRACE'
      }
} ).then( response => { console.log( response ) } ) 
```
All that is required are three things to leverage this into a working XST attack (which can be used with any XSS to bypass the httponly flags and also gain access to any authentication tokens in the header):

    a server that echos the CORS request headers (there are oodles of these);
    a server with TRACE enabled (there are also lots of these: people don't consider it an issue any more because CORS should protect it); and
    a server that responds to x-http-method-override: TRACE (less of these, but there are still plenty about).

Hopefully that helps your triage.


### [Deleted User] (2022-09-13)

[Empty comment from Monorail migration]

### ma...@gmail.com (2022-09-15)

This has been confirmed by firefox too, on ticket https://bugzilla.mozilla.org/show_bug.cgi?id=1790311

### ma...@gmail.com (2022-09-15)

As it is generic, it'll probably need some kind of coordinated release to avoid 0-daying each other

### pe...@chromium.org (2022-09-15)

tsepez@, I don't think this is the same root cause as https://crbug.com/chromium/1340879. That issue is about Android apps being able to add headers to Chrome's initial request when launching Chrome or a Custom Tab. This bug seems to have nothing specifically to do with Android, and looks like it's being triggered from a webpage.

### ts...@chromium.org (2022-09-15)

Ok, over to OWP for consideration. arthur, could you take a peek or find another owner?  Thanks.

### ma...@gmail.com (2022-09-17)

To help with the triage, I've run up a full PoC so that it is clear what the problem is, and how it works.

First browse to https://xst.scarlet.ae so the cookies are set (and you have something sensitive in the headers).

Then browse to any other site (such as https://www.google.com) so that CORS will be activated.

Then paste the following into the browser developer tools, console tab:
```
fetch( 'https://xst.scarlet.ae/', {
      method: 'POST',
      mode: 'cors',
      cache: 'no-store',
      credentials: 'include',
      headers: {
            'x-http-method-override': 'TRACE'
      }
} )
.then( ( response ) => response.text( ) ) 
.then( ( text ) => console.log( text ) ) 
```

You should now see the TRACE output, with the request headers, including cookies.


### ma...@gmail.com (2022-09-20)

Does anyone have a good contact that they can flag this to with Microsoft MSRC? I've logged it with the Edge team, but they have been slow to react. Ticket is: https://msrc.microsoft.com/report/vulnerability/VULN-073694

TIA

### ma...@gmail.com (2022-09-20)

Actually, I guess that prompts a broader question: is the piece of Chromium that is affected by this bug a generic piece that all the browsers built-on Chromium will naturally reuse (and so pickup the patch as part of their normal cycle), or is this something that they will/may have changed in their code?

### ad...@google.com (2022-09-21)

Other Chromium browsers will get access to this report as soon as it's fixed, and decide whether to absorb the fix as-is or if it needs rework. It's up to you if you wish to report it separately to other Chromium browsers, but generally reporting it here is sufficient.

arthursonzogni@ - could you take a look to triage this?

### ma...@gmail.com (2022-09-21)

makes sense: thanks

### [Deleted User] (2022-09-26)

arthursonzogni: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2022-09-27)

Sorry for the delay! I was OOO.

This is a bit out of my competence. AFAIU, Chrome forbids using several methods:
https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/cors/cors.cc;l=494-499;drc=a432cd59d51281057ba2a2673ca645a9600bb927
This includes "CONNECT", "TRACE", "TRACK".

TRACE is meant to reflect the requests header. This should be disabled on production servers, because it leads to the disclosure of sensitive information such as internal authentication. To protect weak server, Chrome blocks it by default apparently.

So far so good! Then we have "x-http-method-override", which is similar to a hack. It is not supported by Chrome. It is used to bypass web browser built-in protection. On server supporting it, it override the "method" field.

TLDR: In my opinion, everything works the way it is expected. We can't require web browser to block this, because if the goal of developer want to bypass browser protection, they can always add a new header under a different name like "x-http-method-override-2" and so on. This relies on servers to purposefully expose themselves to this kind of security issue.

So IMO, we should close this as WontFix. However, as I said, I am not competent here. I would like the last person who touched this behavior to confirm. +@toyoshim, could you please take a look?

### ma...@gmail.com (2022-09-28)

Well, there used to be a time that fetch and XMLHttpRequest allowed the CONNECT, TRACE and TRACK methods, but this was changed to stop CORS bypass (and specifically to stop XST attacks).

And you are right, a specific site could add in CORS support for an X-Cheesecake-Method header, which would allow them to do as they wished. But I think the important point to consider is that this would be intentional, and specific only to themselves.

With the generic headers outlined above, the support for these is already inherent in many app platforms, and enabled by default. In fact, I’d say that the vast majority of web sites have this issue today: an unrestricted CORS implementation, that allows any origin, with credentials, and the header overrides.

Due to the CORS protections, many sites no-longer consider TRACE to be an issue, and so are lax about removing the functionality.

That said, there are far less servers that actually respond to the TRACE method via the override headers, but they are still out there too.

Fixing the override headers seems to make sense in the browser, in the same way that fixing the TRACE method did too: it’s a global fix.


### ma...@gmail.com (2022-09-28)

In context: the firefox team have already implemented a fix, and Apple are likewise working on one too.

### ar...@chromium.org (2022-09-28)

What fix Firefox implemented? We might be interested doing following the same steps if this makes sense.

### ma...@gmail.com (2022-09-28)

I think they've simply blocked the use of the common method override headers:

-  x-http-method-override
-  x-http-method
-  x-method-override


### mk...@google.com (2022-09-29)

I don't see that in their codebase (at least, https://searchfox.org/mozilla-central/search?q=x-method-override&path=&case=false&regexp=false returns no results). Can you let us know who's doing the work on Mozilla's side and we'll CC them here. If we're going to change our behavior for these headers, we need to do it through the Fetch specification, and coordinate a bit.

For example, it might be reasonable instead to introspect these headers' values and limit them to exclude Fetch's forbidden methods (https://fetch.spec.whatwg.org/#forbidden-method).

Blocking the headers entirely would likely have some web-facing impact (and server-side impact on Node) that we should think through before taking action. It shows up in both Safe Browsing and GAIA APIs in Chromium (https://source.chromium.org/search?q=x-http-method-override%20f:cc&sq=&ss=chromium), and I'd like to understand those before breaking them. :)

### to...@chromium.org (2022-09-29)

I just quickly looked at the overview of this report, and may miss something important.
I think using such X-* headers results in sending a CORS preflight, and the server can have a choice to block such headers uses.
How does it bypass the CORS checks?

### to...@chromium.org (2022-09-29)

In the case of linkedin example, actually the second snippets triggers a CORS preflight, but just the linkedion servers accept it, using the x-http-method-override. So, this would not be a browser side bug, but just their server configured with a wrong CORS settings.

### mk...@google.com (2022-09-29)

That's a very good point that I didn't think of. :) Now that I actually run the example code provided, the request to https://realtime.www.linkedin.com/realtime/connect does generate a preflight with `access-control-request-headers: x-http-method-override`, which fails. That does seem to be a pretty solid mitigation, unless I'm missing some aspect of the attack flow.

### ma...@gmail.com (2022-09-29)

The core of what the issue is, is that this is an oversight in the WHATWG spec for fetch. If the override headers were listed in https://fetch.spec.whatwg.org/#forbidden-header-name then we probably wouldn't be having this conversation ;)

As it stands, there are a lot of servers that implement a relatively relaxed CORS. From a brief anaylsys through those with a safe harbour scheme, probably 90% have at least one URI that enables a CORS preflight with credentials, and also allows the override headers. That's a lot of servers.

On top of this, a large percentage of these also have URIs that respond to the override headers, so that you can send a GET request, but actually flip it to a POST, DELETE or indeed a TRACE.

Although the examples I've given previously are for TRACE, that is mostly because that is the aspect I have been working on (and indeed allows access to credentials and cookies, bypassing the httponly flag).

So as it stands, for a server with an open CORS and also responds to the override headers, you can bypass the CORS method restriction, and deliver a POST (or TRACE) when only GET has been allowed.

That bit is the CORS bypass.

Do you chaps have contacts within the WHATWG team? Fixing the standard seems sensible to me.

### ma...@gmail.com (2022-09-29)

The firefox patch is still in dev: https://bugzilla.mozilla.org/show_bug.cgi?id=1790311

### ma...@gmail.com (2022-09-30)

Apple are also working on a patch, but aren't the best of communicators.

### ma...@gmail.com (2022-09-30)

it may also be wise to add max-forwards to the list of forbidden headers too

### ma...@gmail.com (2022-09-30)

toyoshim@chromium.org : the firefox are looking for an introduction, so that a release can be coordinated. Are you happy for me to give them your details?

### ma...@gmail.com (2022-10-01)

Can you please add annevankesteren@gmail.com to this bug (WHATWG)?

### ma...@gmail.com (2022-10-01)

mkwst@google.com 
https://signaler-pa.clients6.google.com/punctual/multi-watch/channel

I'd say that given a bit of an adhoc browse through the Internet, that something like 90% of all hosts have an open CORS implementation, that appears to just reflect back the requested headers.

### ar...@google.com (2022-10-03)

> Can you please add annevankesteren@gmail.com to this bug (WHATWG)?
+ Anne ;-)

### ma...@gmail.com (2022-10-03)

ta!

### an...@gmail.com (2022-10-03)

https://github.com/whatwg/fetch/security/advisories/GHSA-9hrx-wr8g-chvg can be used for cross-browser discussion.

FWIW, I tend to agree that this is not a bug in CORS or browsers, but this would not be the first time we do something to be nice for servers.

Mike raises a good point though that some websites might well be relying on these `X-` method override headers to do something useful and blocking them would end up breaking that.

### ma...@gmail.com (2022-10-03)

Well, I agree that it's not a bug as such (the browsers implement the standard as it is), but it is still a security issue, isn't it?

If the goal of CORS is to limit the methods sent to the endpoint, then this is clearly a mechanism for bypassing the limit.

In practice, the issue is widespread:

A lot of CORS endpoints respond to the preflight request with a specific origin and method header, but often just parrot-back the contents of the request headers field. From my analysis, this applies to something like 90% of the servers in the field. All the vendors. All the major sites.

Then on top of this, a lot of the web servers and app frameworks also support the override headers by default.

If you combine those two things, then the CORS restriction for methods isn't effective in practice.


### mk...@chromium.org (2022-10-05)

+youennf@ from WebKit.

I think we've agreed on an approach in https://github.com/whatwg/fetch/security/advisories/GHSA-9hrx-wr8g-chvg that Anne's prepping a patch for. toyoshim@, do you have bandwidth to make that small change in our implementation?

### ma...@gmail.com (2022-10-15)

Everything progressing ok? Do you have an ETA for a release yet?

### to...@chromium.org (2022-10-18)

I see. The proposal sounds reasonable.
Let me drive this in chromium side.

The next branch cut will happen on Nov 10 for m109.
So, it would be a reasonable timeline.
https://chromiumdash.appspot.com/schedule

Maybe we just introduce these additional restrictions, but with a finch kill-switch, just in case.
We'd just roll it out on m109 if there is no critical compatibility issue, but we may revert it by a server managed runtime switch if we saw a serious problem.

### to...@chromium.org (2022-10-19)

cc: ricea@ as I will need a //net directory OWNER's review.
The forbidden header list is managed under //net/http today.

### to...@chromium.org (2022-10-19)

I will split the change into two parts as there are many callers spread in the repository.

So, the 1st CL is an API surface change to take a header value in addition to the name.
The 2nd CL will actually add the new name-value pairs to implement the spec change.

### to...@chromium.org (2022-10-19)

cc: sky for chrome/ review

### to...@chromium.org (2022-10-19)

+bashi@ as Adam is OOO this week?

### to...@chromium.org (2022-10-20)

+mmenke for //net review

### to...@chromium.org (2022-10-20)

For Matt:
The change is discussed at https://github.com/whatwg/fetch/security/advisories/GHSA-9hrx-wr8g-chvg with other browser vendors, but it's a private thread and approved github account is needed to access.

In short, we will add the following cases to the forbidden request headers.
- The header name is one of below
  1. X-HTTP-Method
  2. X-HTTP-Method-Override
  3. X-Method-Override
- AND, the value is one of below (== forbidden methods)
  1. CONNECT
  2. TRACE
  3. TRACK

### mm...@chromium.org (2022-10-20)

I think that behavior no longer falls under the concept of a "forbidden HTTP method", so we'll need to rename the function, and decide if we want to enforce some sort of more general forbidden value concept to it or figure out a reasonable explanation of what this is the only value restriction rule it enforces (e.g., the fetch spec forbids certain values that don't parse using the new fancy header format, I believe).  Anyhow, feel free to take a stab at it, I'll think about it a bit tomorrow.

### to...@chromium.org (2022-10-20)

https://drive.google.com/file/d/1-FZToLZ5KsTzzUhOHKQwbOqXWCu8kOgk/view?usp=sharing

Just in case, an internal document (in pdf) that contains the planned spec change.
I put some comments on that part that are related to my CLs. Please check my comments on
- the main change
- forbidden method is defined here
- this is refactored to support value checks
- same. added for parsing values
- callsite changes to call the parser with (name, value). they are mainly used by blink side fetch API implementation.

### gi...@appspot.gserviceaccount.com (2022-10-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d8638061f2f51264e31078b8ad446124e0eae6b9

commit d8638061f2f51264e31078b8ad446124e0eae6b9
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date: Fri Oct 21 08:30:12 2022

Net: API change to take a value to evaluate safe headers

This patch changes the net::HttpUtil::IsSafeHeader() API to take
a header value in addition to the name. This API change is needed
in a coming change, and this CL is a preparation to avoid mixing
the core change with mechanical changes spread around the code base.

This also affects blink::cors::IsForbiddenHeaderName().

Bug: 1362331
Change-Id: I517799b96c3a045c336d2a509691bb8cc1f173e0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3963942
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1062009}

[modify] https://crrev.com/d8638061f2f51264e31078b8ad446124e0eae6b9/third_party/blink/renderer/core/fetch/headers.cc
[modify] https://crrev.com/d8638061f2f51264e31078b8ad446124e0eae6b9/services/network/cors/cors_util.cc
[modify] https://crrev.com/d8638061f2f51264e31078b8ad446124e0eae6b9/third_party/blink/renderer/platform/loader/cors/cors.h
[modify] https://crrev.com/d8638061f2f51264e31078b8ad446124e0eae6b9/third_party/blink/renderer/platform/loader/cors/cors.cc
[modify] https://crrev.com/d8638061f2f51264e31078b8ad446124e0eae6b9/services/network/websocket.cc
[modify] https://crrev.com/d8638061f2f51264e31078b8ad446124e0eae6b9/chrome/browser/extensions/api/downloads/downloads_api.cc
[modify] https://crrev.com/d8638061f2f51264e31078b8ad446124e0eae6b9/net/http/http_util.cc
[modify] https://crrev.com/d8638061f2f51264e31078b8ad446124e0eae6b9/third_party/blink/renderer/core/loader/web_associated_url_loader_impl.cc
[modify] https://crrev.com/d8638061f2f51264e31078b8ad446124e0eae6b9/net/android/android_http_util.cc
[modify] https://crrev.com/d8638061f2f51264e31078b8ad446124e0eae6b9/net/http/http_util.h
[modify] https://crrev.com/d8638061f2f51264e31078b8ad446124e0eae6b9/net/http/http_util_unittest.cc
[modify] https://crrev.com/d8638061f2f51264e31078b8ad446124e0eae6b9/third_party/blink/renderer/core/xmlhttprequest/xml_http_request.cc


### to...@chromium.org (2022-10-24)

Submitting the main CL.
Firefox also lands their CL today.
I already confirmed that my patch also passes their adding WPT tests.

### gi...@appspot.gserviceaccount.com (2022-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6463750f04d29188da9129bec4a8016724386c26

commit 6463750f04d29188da9129bec4a8016724386c26
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date: Mon Oct 24 06:16:27 2022

Net: Update net::HttpUtil::IsSafeHeader to follow the latest spec

This patch adds new forbidden cases from the fetch standard.
The code is implemented behind a feature flag, but enabled by default.
This is for the case if this change breaks something big in the real
world.

Bug: 1362331
Change-Id: I6d2f4203f89978bd7bd79527f1640a69b4db4c21
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3967950
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1062673}

[modify] https://crrev.com/6463750f04d29188da9129bec4a8016724386c26/net/base/features.h
[modify] https://crrev.com/6463750f04d29188da9129bec4a8016724386c26/net/base/features.cc
[modify] https://crrev.com/6463750f04d29188da9129bec4a8016724386c26/net/http/http_util_unittest.cc
[modify] https://crrev.com/6463750f04d29188da9129bec4a8016724386c26/net/http/http_util.cc


### to...@chromium.org (2022-10-25)

Fixed!

### [Deleted User] (2022-10-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### ma...@gmail.com (2022-11-18)

Just checking: did you chaps organise a CVE for this one, and if so, what is it? TIA

### am...@chromium.org (2022-11-18)

Hi, not a chap, but I can answer this question. CVEs are issued to security bugs when the fix is shipped in a Stable channel release. The fix was landed on 109 and as a fix for a low-severity issue, it will be released in 109/Stable. A CVE will be added directly to this bug report at that time. 

### ma...@gmail.com (2022-11-18)

Thanks!

### ad...@google.com (2022-12-12)

(removing a duplicate 'severity' label - it looks like Low was the more recent decision)

### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1362331?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1362332]
[Monorail components added to Component Tags custom field.]

### ap...@google.com (2024-04-18)

Project: chromium/src
Branch: main

commit b07526b70da574117dc583710a193f118d286d6d
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date:   Thu Apr 18 09:16:54 2024

    CORS: Remove kBlockNewForbiddenHeaders feature disabler
    
    As the feature is launched over one year ago, and we haven't
    seen any compatibility issue, this patch remove the feature flag
    as we don't need to revert the launch immediately.
    
    Bug: 40060925, 324455968
    Change-Id: I312eed569a96f46b97c026372644367264be3a25
    Fixed: 324455968
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5464886
    Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
    Commit-Queue: Adam Rice <ricea@chromium.org>
    Auto-Submit: Takashi Toyoshima <toyoshim@chromium.org>
    Reviewed-by: Adam Rice <ricea@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1289209}

M       net/base/features.cc
M       net/base/features.h
M       net/http/http_util.cc

https://chromium-review.googlesource.com/5464886


---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060925)*
