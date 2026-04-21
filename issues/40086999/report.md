# Security: HSTS Bypass via flooding of the HSTS policy file

| Field | Value |
|-------|-------|
| **Issue ID** | [40086999](https://issues.chromium.org/issues/40086999) |
| **Status** | Accepted |
| **Severity** | S1-High |
| **Priority** | P3 |
| **Component** | Internals>Network>DomainSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | a3...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2017-03-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When TransportSecurity file is very large，HSTS doesn't work for protecting the site that is first loaded by chrome.  

For example, the user's homepage and clicking a URL in other application(chrome is the default browser).  

A patient attacker can easily make the victim's TransportSecurity file large by letting the victim visit lots of different HSTS enabled sites.

I think this issue is caused asynchronous file IO.

In addition, is the TransportSecurity file's size unlimited a bug?

**VERSION**  

Chrome Version: [56.0.2924.87]  

Operating System: Only tested on Windows 10、Windows8.1，but maybe all platforms are influenced

**REPRODUCTION CASE**  

I tested on Windows 10、Windows8.1.  

1.make the TransportSecurity file large(200 MB is enough for my computer with SDD harddisk)  

In order to achieve this, you can create a TransportSecurity file manually (fast) or vist my poc website <https://ascii0x03.cn/webworker_hsts.html(patience> is needed).

2.make sure the TransportSecurity file is not in RAM  

Maybe logout or restart system is helpful. I think sometimes the system cache has an impact on the attack.

3.while starting chrome, open a HSTS enabled site  

there are two ways:  

(1)Start chrome with a homepage that is a hsts enabled site.  

(2)Click a HSTS enabled site URL that is without "https://" from other application(chrome is default browser).  

Here are some confusing results I got.  

clicked from microsoft word:  

domain attack result  

[www.baidu.com](http://www.baidu.com) ok  

[www.google.com](http://www.google.com) no (influenced by preload?)  

[www.paypal.com](http://www.paypal.com) ok  

[www.alipay.com](http://www.alipay.com) ok (not in preload?)  

<http://www.paypal.com> ok

clicked from QQ :  

domain attack result  

[www.baidu.com](http://www.baidu.com) ok  

[www.google.com](http://www.google.com) no  

[www.alipay.com](http://www.alipay.com) ok  

[www.paypal.com](http://www.paypal.com) no (WHY?)

NOTE:make sure the TransportSecurity file is not in RAM when start chrome.  

I used wireshark saw http request to hsts enabled sites by this way.

## Attachments

- [111.png](attachments/111.png) (image/png, 186.8 KB)
- [222.png](attachments/222.png) (image/png, 118.5 KB)

## Timeline

### el...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

[Monorail components: Internals>Network>DomainSecurityPolicy]

### el...@chromium.org (2017-03-10)

Lucas, can you have a look at this one? Sleevi noted that it's plausible because our TransportSecurityState::Persister isn't very optimized.

### sl...@google.com (2017-03-10)

Today's TSS::Persister just uses a JSON-backed pref-store, which means its going to be gated by disk load times. There's no intrinsic reason for this, other than the prefs file was the rage for things like this.

I don't think we'll find a good architectual solution here using that backend, because we don't facilitate streaming decodes of JSON. Switching to something like LevelDB or SQLite may be appropriate - I'm CC'ing shess@ to the extent of his advice on the 'recommended storage system' for something like this, as his guidance is extremely useful.

I'm not sure how other UAs are backing their dynamic HSTS/HPKP pins, but wouldn't be surprised if there's possibly similar inefficiencies.

And cc estark@ as FYI for all things Expect-*

### sl...@google.com (2017-03-10)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-11)

[Empty comment from Monorail migration]

### a3...@gmail.com (2017-03-12)

I know that Firefox stores HSTS/HPKP pins in SiteSecurityServiceState.txt text file. And the Firefox file only holds the first 1024 sites visited with HSTS headers to avoid long disk load time. Besides, it uses a visiting frequency score to make the "flooding attack" difficult. It is initialized at 0 the first time a domain is visited and is incremented by one (and only by one, regardless of the days that have passed between visits) for each subsequent day that the website is visited, taking as a reference the current system date and time in contrast to the value stored. The attacker must be patient for many days!

Reference Paper:http://link.springer.com/chapter/10.1007/978-3-319-48965-0_12

I don't think it's a nice way, but it is better than chrome's.
By the way, I don't understand why chrome must culculate the SHA hash. How is an attacker able to get the file?

### lg...@chromium.org (2017-03-13)

Waaaaait... are you saying Firefox caches HSTS entries by frequency of use? That sounds awfully unsafe, especially if only the 1024 most frequent are saved.

I checked against the spec, which does not seem to be explicit on whether the client MUST store the Known HSTS Host for the lifetime of the max-age if the site is always sending an HSTS header (section 6.1.1 doesn't use the word MUST [1], and section 8.1.1 only talks about what happens if the expiry date has passed), but does clearly state what to do if there is a dynamic max-age stored and then the site doesn't send an HSTS header [3]:

>    If a UA receives HTTP responses from a Known HSTS Host over a secure
>    channel but the responses are missing the STS header field, the UA
>    MUST continue to treat the host as a Known HSTS Host until the
>    max-age value for the knowledge of that Known HSTS Host is reached.

[1] https://tools.ietf.org/html/rfc6797#section-6.1.1
[2] https://tools.ietf.org/html/rfc6797#section-8.1.1
[3] https://tools.ietf.org/html/rfc6797#section-8.6

Unfortunately, I don't (directly) have access to that paper.

### lg...@chromium.org (2017-03-13)

> Unfortunately, I don't (directly) have access to that paper.

(Never mind, I found the magic login link for Googlers to access Springer papers.)

### sh...@chromium.org (2017-03-13)

If I understand HSTS right, it's kind of like a cookie?  Like it's a little piece of info which has to be served by the target itself, and carries forward with an expire time?

Preferences is a terrible way to store things.  It is way past the point where other people's poor decisions are likely to mess up your local priorities.  The OP mentioned 200MB - that's just challenging.

SQLite and leveldb may-or-may-not be great choices, if they result in disk accesses gating page fetches.  I think over time we've found that disk I/O is surprisingly expensive, often more expensive than network I/O.  The most similar thing I can think of offhand is safe-browsing malware/phishing database, which is ~13MB (but was more like 5MB back when these decisions were being made).  Initially, bare lookups by key were used, but those were far too slow.  So an in-memory bloom filter was introduced, with hits falling back to database lookups to verify, and those were too slow, so it ended up with the bloom filter followed by a server ping.  I _think_ the page fetch proceeds in parallel, but use is gated on the safe-browsing results.

[ObDisclosure: We've evolved from spinning disks being dominant to SSDs being dominant, but AFAICT in the fleet SSDs are often differently slow.  You can't rely on them having reliable RAM-but-slower access, I think.]

Even a bloom filter or prefix set (filter based on a rice encoding variant) probably won't help for 200MB attacks, though, unless you can use some interesting encoding or filtering system.  Safe browsing stored 32-bit hashes with about 32 bits of metadata apiece, which left the filter around 1/4 the raw database size, but 50MB or even 20MB is really a lot of memory for this!  Though I suppose if the attacks don't work, nobody will employ them, so maybe you don't have to worry about that kind of edge case.

There may be other safe-browsing-like possibilities, though.  Since the server itself has to serve the tidbit, there's perhaps a limit to how many TLDs and/or IPs can be involved.  So perhaps there could be a multi-level filter, where one level says "This is a high-collision space", so you can segregate the high-cost queries on disk from the low-cost queries in memory.

Or perhaps this could all feed into the safe-browsing machinery to put domains in a penalty box.  Not to deny them, but to confine them to a slow path to protect the fast-path domains.

### lg...@chromium.org (2017-03-13)

> Since the server itself has to serve the tidbit, there's perhaps a limit to how many TLDs and/or IPs can be involved. 

The solution that other browsers used for https://crbug.com/chromium/178980 (localStorage flooding using subdomains) is to apply a resource cap per eTLD+1 (#bytes on that bug, but here it would presumably be # of entries). I wouldn't have strong objections to such an approach, but I believe our hash-based storage format might not make it easy to look for all the *subdomains* of a given eTLD+1?

### rs...@chromium.org (2017-03-13)

@https://crbug.com/chromium/699461#c12: Right, but it's trivial to bypass those mechanisms with a pull request, so I don't know how much we should rely on them.

### a3...@gmail.com (2017-03-14)

@https://crbug.com/chromium/699461#c9：
Hah,copyright sometimes brings me trouble too.  :)
Only the 1024 most frequent hsts hosts are saved in Firefox really sounds awful, however, in general, I don't think most users have visited 1024 hsts hosts. And if I have visited paypal.com 30 days, the attacker need at least 30 days to flood hsts header. It's not easy.

### a3...@gmail.com (2017-03-14)

Limiting the number of hsts domain for per eTLD+1 sounds a good solution. If there're lots of hsts subdomains needed, the right way is using "includeSubDomains" directive.

There are two questions:
1. as mentioned in https://crbug.com/chromium/178980#c45, it would allow me.github.io to "starve" you.github.io with no ability for you.github.io.
https://bugs.chromium.org/p/chromium/issues/detail?id=178980#c45
2. Does the solution open a another gate for attackers to sniff user's browser history? (assume we limit 100 entries for bank.com, the attacker can set 99 entries  for *.bank.com, leaking the information that the user has visited *.bank.com in expire time.)

Maybe the questions above are negligible. 

### sh...@chromium.org (2017-03-28)

lgarron: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2017-04-05)

Friendly sheriff ping on this one. :)

### a3...@gmail.com (2017-04-10)

Can we apply cookie-split-loading? Cookie IO is more optimized.

https://www.chromium.org/developers/design-documents/cookie-split-loading

### sh...@chromium.org (2017-04-11)

lgarron: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### a3...@gmail.com (2017-04-21)

I am sorry that I'll share some details of this bug on a security conference by a poster， on May 22nd, 2017. I think probably it's hard to do such an attack in reality. Sorry for leving just one month to fix this bug before it is public. 

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### mm...@chromium.org (2017-11-15)

a3135134@, have you shared the details on a conference? I guess we can remove view restrictions then?

Lucas, could you please either post an update or re-assign this if you aren't working on this anymore? Your last comment is 8 months old.

### a3...@gmail.com (2017-11-21)

Yes. But it was not as detailed as this issue report. Probably you can remove view restrictions to help fix this bug faster. 

### es...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-02-20)

I don't think we have any inexpensive solution for the issue identified here.

The issue was made public last year and does not need view-restrictions.

### el...@chromium.org (2018-05-01)

We have not made any progress here, but the upcoming changes around the Network Service may have an impact here.

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### pa...@chromium.org (2018-06-05)

Perhaps we could limit the # of HSTS entries any given eTLD+1 can store? This would also be a defense against HSTS super-cookies, if we could make the limit low enough. "32 explicitly-named subdomains should be enough for anybody"; past that, sites should use includeSubDomains? Would that work? Or am I crazy again.

Any interest in picking this bug up?

### ma...@chromium.org (2018-06-06)

If there is some consensus on the best way forward I can take this.

If we go with the eTLD+1 option we'll have to change the JSON format because it's not possible to extract that information with the current format. //net OWNERS haven't been very keen on CLs that change the JSON format in the past though. But if we're going to change the format for this maybe we could clean up the format and address some of the other issues at the same time?

### pa...@chromium.org (2018-06-06)

I'll defer to net OWNERS, agl, and estark. I think a bypass of HSTS is worse than the loss of a weak defense against a forensic attacker that the current format provides. (agl devised the hostname hashing scheme to avoid leaking browsing history to a forensic attacker, if I recall correctly.)

It's a bit of a micro-optimization, but I can also imagine a much more compact format than JSON.

### rs...@chromium.org (2018-06-07)

Using public suffix + 1 as a storage restriction mitigation sadly falls apart, especially when it's easy to get added to public suffix list. That is, a single pull request for "*.evil.attacker.example.com" to the PSL means that every subdomain of .evil.attacker.example.com will constitute a public suffix, and they can just explore 32-subdomains-at-a-time.

So some of the fundamental challenges:
1) Is there a more efficient storage format that can allow quicker loading
2) How do we limit the effective size
  a) No limit
  b) Limit by some variation of domain
  c) Limit by number of entries

My understanding is that Mozilla chose 2.c) and chose the format in accordance with that. We don't have an overall cookie storage limit (AFAIK), just a per-domain limit, and while the format (SQLite) doesn't block loading, it's allowed to grow.

### nh...@chromium.org (2018-06-08)

My understanding is that we have both per-domain limits for cookies (kDomainMaxCookies) and an overall limit (kMaxCookies) in net/cookies/cookie_monster.h.

### a3...@gmail.com (2018-06-11)

I'm glad to see this old bug was picked up again.
The summary in #https://crbug.com/chromium/699461#c37 is great. I want to say: 
(1)As I mentioned in #https://crbug.com/chromium/699461#c18, there is an efficient loading way.
(2)HSTS is a security mechenism. If security is more important than efficient, we should delay browser's startup when loading security config files. If we don't delay the startup, there will be always risks.
(3)I don't think md5 format now is good. And palmer's suggestion is more reasonable. 

Here's the link of my short paper.
https://www.ieee-security.org/TC/SP2017/poster-abstracts/IEEE-SP17_Posters_paper_12.pdf



### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### mm...@chromium.org (2018-08-07)

Ryan, would you mind owning this?

### rs...@chromium.org (2018-08-07)

Sorry, I'm not a good person to own this.

### ji...@chromium.org (2018-08-09)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-08-23)

martijnc@ -- per https://crbug.com/chromium/699461#c35, do you want to own this?

### va...@chromium.org (2018-08-23)

nharper@ said he's interested so assigning it to him for now.

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### nh...@chromium.org (2019-05-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-06-13)

nharper: Were you able to make any progress on this medium-severity bug?

### nh...@chromium.org (2019-06-13)

No, I haven't made any progress on it.

### me...@chromium.org (2019-06-13)

Thanks for the update!

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-08-19)

Friendly nudge again from the security marshal. We'd love to see this making progress. Thanks!

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ea578fed8c1989b35fc2cd600532a917c7db286f

commit ea578fed8c1989b35fc2cd600532a917c7db286f
Author: Matt Menke <mmenke@chromium.org>
Date: Fri May 29 18:56:16 2020

Don't pretty print TransportSecurityState file.

Users don't generally view this file in a text editor, so we should
not pretty print this file, to both speed up loading and reduce our disk
footprint.

We'll soon be keying Expect-CT data by NetworkIsolationKey, which will
also bloat up this file a bit, so let's decrease its size before that
happens.

Bug: 699461, 969893
Change-Id: I2d6815997dd41e2fcfa98f144c783bdd0f5ef583
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2220907
Reviewed-by: Nick Harper <nharper@chromium.org>
Commit-Queue: Matt Menke <mmenke@chromium.org>
Cr-Commit-Position: refs/heads/master@{#773275}

[modify] https://crrev.com/ea578fed8c1989b35fc2cd600532a917c7db286f/net/http/transport_security_persister.cc


### [Deleted User] (2020-07-14)

nharper: Uh oh! This issue still open and hasn't been updated in the last 396 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-28)

nharper: Uh oh! This issue still open and hasn't been updated in the last 410 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### nh...@chromium.org (2020-09-09)

There are two issues that have been discussed on this issue.

1) If the TransportSecurity file isn't loaded by the time an HTTP (not-S) request is made, the HSTS policy check is skipped.
2) There are no limits on how big the TransportSecurity file can grow.

Even though most of the discussion so far has been around what sort of policies might or might not work to add a limit to solve #2, the security issue here is #1 and should be solved first. Later we can consider solutions for limiting the size of the file.

I see two broad approaches for fixing #1. One is that whatever callsite creates a TransportSecurityPersister (e.g. URLRequestContextBuilder) needs to wait for the file to load before it can use its TransportSecurityState object. The other is to change TransportSecurityState::GetDynamicSTSState to call a callback with the result instead of returning a bool (and then refactor all callsites to support this asynchronous mode). I'm going to look into doing the second, even though it will likely involve a massive refactor, because I don't know if the first option is feasible.

### rs...@chromium.org (2020-09-10)

Nick: I'm curious about the concerns around the delay feasibility? It seems like we could do a hybrid approach: TransportSecurityState remains synchronous access, but there's the ability to query if it's loaded and (if not) asynchronously wait.

I think the design would end up similar to what you propose, in that it would likely add an additional state to the state machines of places waiting, but it avoids the need to constantly use TaskScheduler to wait for events, in the "normal" case (i.e. after first load), everything just works synchronously. I admit, it's a bit of a danger that a caller could use it without checking if it was loaded, but that would devolve into the current behaviour.

Just a thought.

### nh...@chromium.org (2020-09-10)

The feasibility concerns around delaying use of the TransportSecurityState are simply me not being familiar with the callers of URLRequestContextBuilder::Build (which is the only place outside of ios and test code that creates a TransportSecurityPersister) to know how easy/hard it would be to add an async wait to them.

The hybrid approach sounds like it could work. Somewhere in URLRequest or HttpNetworkTransaction could check  that the TransportSecurityState object is ready, and if not wait for it to be ready, and then all operations are synchronous.

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### bd...@chromium.org (2020-10-13)

friendly marshal, are there any updates?

### nh...@chromium.org (2020-10-19)

https://chromium-review.googlesource.com/c/chromium/src/+/2413174 is in progress.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### aa...@gmail.com (2020-10-31)

Do we get paid if reward potential?

### nh...@chromium.org (2020-11-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### yf...@chromium.org (2020-11-20)

lowering priority given recent unassigning and how long it's been out

### [Deleted User] (2020-11-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-11-23)

Re https://crbug.com/chromium/699461#c77 the VRP panel will decide on this bug after it's fixed. I appreciate that's taking a really long time on this one.

### ad...@google.com (2020-11-23)

Emily, given Nick's departure, can you find a reasonable owner to take this forward?

### es...@chromium.org (2020-12-29)

I'm not sure if we're going to have cycles to prioritize this soon, however cc'ing carlosil@ since it's possible this is relevant to stuff he's investigating for moving public key pins to a different model that might give us more flexibility in how we load data from disk that need to block network requests.

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-22)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2021-02-24)

rsleevi: I'm catching up on this bug, trying to figure out what the status is here. It looks like the CL in https://chromium-review.googlesource.com/c/chromium/src/+/2413174 is in decent shape, with some open comments and a question about how we're going to measure and evaluate perf impact. Would it be reasonable for me to see if I can find someone to pick up that CL and see it through? (Mostly interested to know if there were any offline chats or context arguing that that CL should be abandoned.)

### es...@chromium.org (2021-02-24)

Ah, carlosil tells me that the network service component delay API he's working on will subsume this, so I'm going to go ahead and assign it to him.

### ca...@chromium.org (2021-02-24)

To add more context, my wait for critical component API is somewhat based on crrev.com/c/2413174, and even though this bug is not the critical component API, we can reuse the waiting parts I will add. Instead of having two different ways URLRequestJob::Start can be delayed.

### nh...@chromium.org (2021-02-24)

The net/http/transport_security_* changes in crrev.com/c/2413174 are probably good to carry forward. It sounds like there's other work being done on blocking the network service on certain conditions, so the URLRequest changes from that CL can probably be replaced by that work.

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-28)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-07-08)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-07-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-13)

[Comment Deleted]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-25)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2021-10-25)

I'm downgrading this to Severity-Low. While our severity guidelines [1] specifically call out an HSTS bypass as Sev-Medium, this case is more limited since it's a race at browser startup. An attacker would have to pack HSTS, then get Chrome to restart, ensuring that the target site was loaded at startup, and then it might work if I/O is slow enough and the HSTS state is large enough.

[1] https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/699461?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/892338]
[Monorail components added to Component Tags custom field.]

### ct...@chromium.org (2025-03-19)

cc'ing bingler@ -- I think this might get incidentally fixed by your efforts on restricting HSTS to top-level frames?

### am...@chromium.org (2025-03-21)

temporarily setting this as fixed, but we are still waiting confirmation from bingler@ ^^

### sp...@google.com (2025-03-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact exploitation mitigation bypass 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-21)

Hello! Thank you for this 8 year old report. We are going through some of our oldest security issues for disclosure and potential rewards. This issue has already been disclosed for some time, but we did want to go ahead and issue a VRP reward for this report given that it's been open for some time (and also may already been resolved). Thanks for your patience!

### ct...@chromium.org (2025-03-21)

Re: my [comment #170](https://issues.chromium.org/issues/40086999#comment170), re-reading the HSTS tracking prevention explainer [1](https://github.com/explainers-by-googlers/HSTS-Tracking-Prevention) it sounds like subresources still *update* the dynamic HSTS state but won't have it *applied* to them. So I think this is still relevant even after the HSTS tracking prevention work ships.

### a3...@gmail.com (2026-01-11)

What a surprise! I have forgot this. But this story tell me: Google never forget. Thank you guys.

## Bounty Award

> report of lower impact exploitation mitigation bypass

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086999)*
