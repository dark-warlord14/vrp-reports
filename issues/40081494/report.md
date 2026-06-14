# Security: HSTS bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40081494](https://issues.chromium.org/issues/40081494) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>SSL |
| **CVE IDs** | CVE-2015-0832 |
| **Reporter** | [Deleted User] |
| **Assignee** | rs...@chromium.org |
| **Created** | 2015-02-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

HSTS can be bypassed via FQDN hostnames in Chrome 40. This goes for preloaded domains too. I was able to reproduce this on domains such as: accounts.google.com., mail.google.com., crowdcurity.com., stripe.com., blockchain.info., etc...

I was using incognito mode during my tests. After the initial request, some domains set HSTS on the FQDN and that prevent further plain http requests (via a 307 internal redirect in Chrome). An example domain that did not get better was <http://crowdcurity.com./>. I could hit that domain over and over with plain http in one browser session.

This may be a regression bug. I found this same problem in FireFox and when I reported this to them then, Chrome 38 did not appear to have the issue. I reported it to Mozilla as <https://bugzilla.mozilla.org/show_bug.cgi?id=1085091>. Someone else had reported it to them concurrently a few days earlier (but it was and is still private so I could not have known). FireFox will have this fixed soon as CVE-2015-0832 under ticket <https://bugzilla.mozilla.org/show_bug.cgi?id=1065909>. Please use discretion in sharing this knowledge as it is not public yet but thought it would be useful for you to know (if you didn't already).

Obviously, this is bad for users being subjected to SSL stripping style attacks, etc...

**VERSION**  

Chrome Version: 40.0.2214.115 (64-bit) stable  

Operating System: Ubuntu Linux 14.04.2 LTS

**REPRODUCTION CASE**

0. begin packet sniffer on local machine. i used wireshark.
1. open affected version of chrome and navigate to <http://accounts.google.com./>
2. notice that the traffic was sent over plain unencrypted http in the network capture. for example, see attached screenshot.

## Attachments

- [wireshark.png](attachments/wireshark.png) (image/png, 263.0 KB)
- [net-internals-log.json](attachments/net-internals-log.json) (application/json, 389.8 KB)
- [net-internals-log-chrome-43.json](attachments/net-internals-log-chrome-43.json) (application/json, 401.9 KB)

## Timeline

### [Deleted User] (2015-02-24)

I was just re-thinking how I worded the description above...
Basically, the main problem is that this easy trick allows for bypassing the HSTS for preloaded domains. Non-preloaded domains have the stripping issue already by virtue of not being preloaded.

### in...@chromium.org (2015-02-24)

[Empty comment from Monorail migration]

### rs...@chromium.org (2015-02-24)

cc'ing brett for //url/OWNERS
cc'ing cbentzel for general net-stack
cc'ing ttuttle because this uses DNSDomainFromDot, and we were just talking about that in relation to another issue (note: not mentioning that issue here)

Issues like this have come up several times now, and I'm curious whether we should take a more systematic approach to this. For example, I'm not clear whether the Host: header sending the trailing '.' is a correct behaviour (at the HTTP layer), and we've had issues with DNS and with cert verification.

Having //url correct the URL as part of its canonicalization would help, but we need to preserve the '.' for DNS lookup to disable suffix search.

Brett: When working on GURL, was this something considered and dismissed? I'm just curious if I'm barking up a bad tree for attempting to deal with this systemically.

### ju...@chromium.org (2015-02-24)

I personally don't think Host: should send a trailing dot; to me, that is a detail of hostname resolution (disables suffix search), not part of the actual hostname we end up with.

AFAIK, DNSDomainFromDot should produce the same result whether or not there is a trailing dot.

### [Deleted User] (2015-02-24)

About not sending the trailing dot, that would mean an increase in ambiguity since relative names are ambiguous where absolute names are not. Whether that increase in ambiguity matters is a good question. What cases would that hit that might cause problems? It seems like increasing ambiguity is counter-productive, but I don't have a good answer right now. It would affect TLS SNI too. I know some servers are configured to handle the FQDN requests differently.

Also, a follow-up about how some domains were getting HSTS turned back on for the naked fqdn and some were not...

tl;dr: it may be a generally better practice to try to set hsts on all https responses instead of on just the non-fqdn domains that are expected.

I did some digging to figure out why some services were "healing" and some were not.
For example, crowdcurity.com was not and it was because they were redirecting to a different subdomain.
The initial request was to the naked fqdn and they ended up trying to set HSTS on the subsequent subdomain.
Thus, the HSTS header was not being explicitly set on the naked domain (fully qualified or not).

For example:
http://crowdcurity.com./ -> https://crowdcurity.com/ -> https://www.crowdcurity.com/ (with strict-transport-security:max-age=31557600; includeSubdomains)
They're using a CloudFlare page rule redirect for the intermediate redirect and CloudFlare hasn't added HSTS support to those yet.

accounts.google.com gets HSTS healed on the last request in the redirect chain. notice that the intermediate request to https://accounts.google.com./ does not attempt to set HSTS.

http://accounts.google.com./ -> https://accounts.google.com./ -> https://accounts.google.com/ManageAccount (with strict-transport-security:max-age=10893354; includeSubDomains)

mail.google.com does not get healed until a valid login request gets redirected back to mail.google.com

### in...@chromium.org (2015-02-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-18)

rsleevi@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-08)

rsleevi@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-04-30)

rsleevi@: Uh oh! This issue is still open and hasn't been updated in the last 63 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@google.com (2015-05-08)

@brettw - can you provide some insight here? (see c#3).

### br...@chromium.org (2015-05-08)

Sorry, I'm not clear what I'm being asked. If it's about trailing dot stripping, we definitely shouldn't be doing that. "google.com" and "google.com." could be completely different hosts.

### rs...@chromium.org (2015-05-08)

Sorry, I think we've fixed this bug in a related area lower, but haven't gotten around to confirming.

I disagree with Brett's assessment that google.com and google.com. are different. From a point of view of SOP, storage, and effective security, they're identical, even if "google.com" as presented by the user may have resolved via suffix search to google.com.bar.baz.evil.example

### br...@chromium.org (2015-05-08)

Yes, certain things should ignore the trailing dots, but they can't be removed by the URL layer ever IMO.

### rs...@chromium.org (2015-05-08)

This is an area where we're different from every other browser, FWIW, and for which our host normalization vs storage is different.

I'm appreciative that the trailing . need to be preserved (e.g. for hostname lookup), but for comparisons of the effective origin (cookies, persistence, storage), . vs no-. is equivalent. This is already true at the majority of our higher layers (including certificate validation).

### cl...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### es...@chromium.org (2015-05-19)

rsleevi@: As part of the security bug fixit, I tried to reproduce this in 42 and couldn't, so we might be able to close it. Do you think you could try it to make sure I'm not crazy?

### [Deleted User] (2015-05-20)

I can still reproduce this. 

For example, I just hit http://accounts.google.com./ and snooped the request/response in wireshark as plain http:

GET / HTTP/1.1
Host: accounts.google.com.
Connection: keep-alive
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8

HTTP/1.1 302 Moved Temporarily
Content-Type: text/html; charset=UTF-8
X-Frame-Options: DENY
Location: https://accounts.google.com/ManageAccount
Content-Encoding: gzip
Date: Wed, 20 May 2015 00:23:52 GMT
Expires: Wed, 20 May 2015 00:23:52 GMT
Cache-Control: private, max-age=0
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Length: 182
Server: GSE
Alternate-Protocol: 80:quic,p=1


### rs...@chromium.org (2015-05-20)

Mike: Can you provide a chrome://net-internals of this?

As of Chrome 41, this should have been fixed. https://crbug.com/chromium/456391 changed the DNS normalization such that "www.google.com" and "www.google.com." return the same canonical result as part of DNSDomainFromDot, which is what TransportSecurityState::CanonicalizeHost() uses to look-up information.

In testing on Chrome 42, 43, and 44, I'm unable to reproduce the problem. A chrome://net-internals log shows the URLRequestJob is immediately redirected by the TransportSecurityState to the https:// version

If you can reproduce, please indicate which version you used.

### [Deleted User] (2015-05-20)

Sure, I can reproduce this still and the requested log is attached. The version I'm using for this latest test is:
Google Chrome 42.0.2311.152 (official c707233f90c2f1d16db21143b8f009ff9b14c3bd-refs/branch-heads/2311@{#509})

To reproduce, I simply open a fresh incognito instance, type or copy/paste http://accounts.google.com./ into the omnibox, and hit enter.

### [Deleted User] (2015-05-20)

I just got an update to Chrome 43 this morning and reproduced it with that version too (log also attached).

The new version is Google Chrome 43.0.2357.65 (official d4165d5336fc2cd9a9ee89694c5f3e0a7e611774-refs/branch-heads/2357@{#385})

### rs...@chromium.org (2015-05-20)

Thanks, I've confirmed the issue - the key to reproducing was forcing the fully Incognito profile. This doesn't affect any pins that the user has observed (at least, not since M41), only static/preloaded pins, and looks like we regressed in https://crrev.com/298580 (it did the right thing before then). This also explains why it didn't show up in any of the unit tests I wrote.

Because we treat accounts.google.com. as a unique origin than accounts.google.com (for purposes of storage), this doesn't expose any stored information. It is more akin to a phishing scenario (in that the user would need to input their information), but still bad.

### rs...@chromium.org (2015-05-20)

And a more troubling result: We no longer match case-insensitively.

### rs...@chromium.org (2015-05-20)

[Empty comment from Monorail migration]

### da...@chromium.org (2015-05-20)

> Because we treat accounts.google.com. as a unique origin than accounts.google.com (for purposes of storage), this doesn't expose any stored information.

Wouldn't it still do something dumb with cookies? Or is our cookie logic also sensitive to the trailing dot?

### rs...@chromium.org (2015-05-20)

Basically, *everything* is sensitive to the trailing "." (treating it as a unique origin) except for

1) DNS (well, technically, it is sensitive in that it omits suffix search)
2) Certificate verification (because all cert names are implicitly trailing '.' and thus match either form)
3) Now HSTS/HPKP

Everything else treats it as a mismatch - that is, document.domain still reports with the trailing ".", blink's SecurityOrigins preserve the trailing "." (thus equivalencies of origins fail), the Host: header preserves the trailing ".", etc. So the primary concern is one about UI, since to the user, "accounts.google.com" and "accounts.google.com." are correct - even if they have separate storage models.

### [Deleted User] (2015-05-20)

Right, I think it's more common for the trailing dot to cause cookie problems as a result of server side mis-config. I've seen where a server will naively try to set a cookie with the domain attribute missing the trailing dot, even when it's provided in the the Host header and TLS SNI of the request. I would guess this usually happens because the nginx server_name directive treats "trailing-dot" the same as "no-trailing-dot". For example, one of the reverse proxy services had that problem for a long time which allowed avoiding their main tracking cookie -- they would wind up trying to set it for every request because the browser never accepted the cookie with mis-matched domain.

### bu...@chromium.org (2015-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c2dd599bdd35753da237172dc37a447e9d65c463

commit c2dd599bdd35753da237172dc37a447e9d65c463
Author: rsleevi <rsleevi@chromium.org>
Date: Wed May 20 23:29:02 2015

Normalize hostnames before searching for HSTS/HPKP preloads

The HSTS/HPKP preload set is pre-normalized at construction time.
Since the queries come from the GURL, not from the DNS layer,
we need to normalize the hostname before scanning for preloads.
This used to be handled by CanonicalizeHost(), which used the
same mechanism as the resolver, but the storage of the preloads
has changed to be more efficient, and thus no longer uses the
resolver-normalized form.

BUG=461481
R=davidben@chromium.org

Review URL: https://codereview.chromium.org/1149753002

Cr-Commit-Position: refs/heads/master@{#330834}

[modify] http://crrev.com/c2dd599bdd35753da237172dc37a447e9d65c463/net/http/transport_security_state.cc
[modify] http://crrev.com/c2dd599bdd35753da237172dc37a447e9d65c463/net/http/transport_security_state.h
[modify] http://crrev.com/c2dd599bdd35753da237172dc37a447e9d65c463/net/http/transport_security_state_unittest.cc


### aa...@google.com (2015-05-21)

Ryan, ok to mark this as Fixed or is there work remaining here ?

### rs...@chromium.org (2015-05-21)

Fixed in M-45; need to do the merge dances (the diff on the CL is larger than necessary due to needing to shuffle some code to avoid ODR)

### rs...@chromium.org (2015-05-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-21)

[Empty comment from Monorail migration]

### pe...@google.com (2015-05-21)

Approved for M44 (branch: 2403)

### pe...@google.com (2015-05-21)

[Automated comment] Request affecting a post-stable build (M43), manual review required.

### bu...@chromium.org (2015-05-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/808afe3a738062fb98b5ccd7762064f55b26ad7b

commit 808afe3a738062fb98b5ccd7762064f55b26ad7b
Author: Ryan Sleevi <rsleevi@chromium.org>
Date: Fri May 22 00:27:16 2015

Normalize hostnames before searching for HSTS/HPKP preloads

The HSTS/HPKP preload set is pre-normalized at construction time.
Since the queries come from the GURL, not from the DNS layer,
we need to normalize the hostname before scanning for preloads.
This used to be handled by CanonicalizeHost(), which used the
same mechanism as the resolver, but the storage of the preloads
has changed to be more efficient, and thus no longer uses the
resolver-normalized form.

BUG=461481
R=davidben@chromium.org

Review URL: https://codereview.chromium.org/1149753002

Cr-Commit-Position: refs/heads/master@{#330834}
(cherry picked from commit c2dd599bdd35753da237172dc37a447e9d65c463)

Review URL: https://codereview.chromium.org/1148093003

Cr-Commit-Position: refs/branch-heads/2403@{#63}
Cr-Branched-From: f54b8097a9c45ed4ad308133d49f05325d6c5070-refs/heads/master@{#330231}

[modify] http://crrev.com/808afe3a738062fb98b5ccd7762064f55b26ad7b/net/http/transport_security_state.cc
[modify] http://crrev.com/808afe3a738062fb98b5ccd7762064f55b26ad7b/net/http/transport_security_state.h
[modify] http://crrev.com/808afe3a738062fb98b5ccd7762064f55b26ad7b/net/http/transport_security_state_unittest.cc


### bu...@chromium.org (2015-05-22)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/808afe3a738062fb98b5ccd7762064f55b26ad7b

commit 808afe3a738062fb98b5ccd7762064f55b26ad7b
Author: Ryan Sleevi <rsleevi@chromium.org>
Date: Fri May 22 00:27:16 2015


### ti...@google.com (2015-05-22)

[Empty comment from Monorail migration]

### la...@google.com (2015-06-02)

Approved 43 (Branch 2357)

### bu...@chromium.org (2015-06-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e648e4b5848efceda338aff4d83819ce9b34c456

commit e648e4b5848efceda338aff4d83819ce9b34c456
Author: Ryan Sleevi <rsleevi@chromium.org>
Date: Fri Jun 05 06:30:09 2015

Normalize hostnames before searching for HSTS/HPKP preloads

The HSTS/HPKP preload set is pre-normalized at construction time.
Since the queries come from the GURL, not from the DNS layer,
we need to normalize the hostname before scanning for preloads.
This used to be handled by CanonicalizeHost(), which used the
same mechanism as the resolver, but the storage of the preloads
has changed to be more efficient, and thus no longer uses the
resolver-normalized form.

BUG=461481
R=davidben@chromium.org

Review URL: https://codereview.chromium.org/1149753002

Cr-Commit-Position: refs/heads/master@{#330834}
(cherry picked from commit c2dd599bdd35753da237172dc37a447e9d65c463)

Review URL: https://codereview.chromium.org/1157033008

Cr-Commit-Position: refs/branch-heads/2357@{#466}
Cr-Branched-From: 59d4494849b405682265ed5d3f5164573b9a939b-refs/heads/master@{#323860}

[modify] http://crrev.com/e648e4b5848efceda338aff4d83819ce9b34c456/net/http/transport_security_state.cc
[modify] http://crrev.com/e648e4b5848efceda338aff4d83819ce9b34c456/net/http/transport_security_state.h
[modify] http://crrev.com/e648e4b5848efceda338aff4d83819ce9b34c456/net/http/transport_security_state_unittest.cc


### ti...@google.com (2015-06-19)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-19)

[Empty comment from Monorail migration]

### [Deleted User] (2015-07-21)

Hi, just checking on this about the reward since the last update on that was about two months ago.

### ti...@google.com (2015-07-24)

Doesn't look like this one has made it to our panel yet - I'll make sure it's on the agenda for the next meeting.

### cl...@chromium.org (2015-08-27)

Bulk update: removing view restriction from closed bugs.

### [Deleted User] (2015-09-03)

Hi Tim, is there any update on the reward yet? Thanks!

### ti...@google.com (2015-09-28)

Updating this bug so people don't think I'm ignoring Mike - we've been emailing. This report is currently at the reward panel for review.



### ti...@google.com (2015-10-09)

Congratulations Mike - $1000 for this report!

I'll start payment next week, which means that you should have the cash ~2 weeks from today.

Thanks again and sorry for the delay.

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### [Deleted User] (2015-11-06)

Sweet, got it. Thanks Tim!

### ju...@chromium.org (2016-04-01)

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

This issue was migrated from crbug.com/chromium/461481?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081494)*
