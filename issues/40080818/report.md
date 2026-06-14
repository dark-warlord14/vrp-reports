# Security: Cookie injection by Proxy with 407 response

| Field | Value |
|-------|-------|
| **Issue ID** | [40080818](https://issues.chromium.org/issues/40080818) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals, Internals>Network, Internals>Network>Proxy |
| **Reporter** | il...@gmail.com |
| **Assignee** | ju...@chromium.org |
| **Created** | 2014-11-08 |
| **Bounty** | $500.00 |

## Description

Chrome mistakenly accepts cookies in a 407 response of CONNECT request from proxy.

**VERSION**  

Chrome Version: All  

Operating System: All

**REPRODUCTION CASE**

1. Set up a HTTP proxy in Chrome.
2. Navigate to <https://mail.google.com>.  
   
   Chrome actually sends a CONNECT request:  
   
   CONNECT mail.google.com:443 HTTP/1.1  
   
   Host: mail.google.com
3. The proxy responds a 407 message, including Set-Cookie headers.  
   
   HTTP/1.1 407 Proxy Authentication Required  
   
   Proxy-Authenticate: Basic realm=”auth"  
   
   Set-Cookie: SID=malicious; domain=.mail.google.com; path=/; SECURE;
4. Chrome mistakenly accepts the malicious cookies.

## Timeline

### ta...@opera.com (2014-11-10)

This appears to be a duplicate of bug #137891, which is already marked as fixed as of 2012.

### il...@gmail.com (2014-11-10)

It seems that Chrome rejects all error responses to CONNECT requests, except 407. I test it in all platforms (Windows, OS X, Linux, Android, iOS). 

Android WebView is also affected. Especially, in WebView, the Proxy-Authenticate header is not required, it means that cookies will be injected silently.

### ta...@opera.com (2014-11-10)

[Empty comment from Monorail migration]

### ta...@opera.com (2014-11-10)

Reproduced in 40.0.2202.3 dev-m Win, using Fiddler to intercept the CONNECT and replace it with an appropriate response.

### cb...@chromium.org (2014-11-10)

[Empty comment from Monorail migration]

### cb...@chromium.org (2014-11-10)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-18)

ttuttle@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-11-25)

ttuttle@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ju...@chromium.org (2014-12-01)

[Empty comment from Monorail migration]

### ju...@chromium.org (2014-12-01)

[Empty comment from Monorail migration]

### rc...@chromium.org (2014-12-02)

+asanka

### cb...@chromium.org (2014-12-06)

ttuttle: Do you plan to fix this? I'm assuming it's a straightforward issue of stripping cookie header in a 407 response to a CONNECT?

### ju...@chromium.org (2014-12-06)

I'm working on it right now, but in the codereview, folks want me to whitelist headers instead of blacklisting, and that breaks a bunch of tests (e.g. ones that expect to be able to receive the response).

### cb...@chromium.org (2014-12-06)

OK, thanks for the update.

### cl...@chromium.org (2014-12-13)

ttuttle@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cb...@chromium.org (2014-12-13)

ttuttle: You mentioned that you had an outstanding CL for this. Is it
still in the works?

### in...@chromium.org (2014-12-16)

ttuttle@chromium.org, friendly ping.

### cl...@chromium.org (2015-01-04)

ttuttle@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7933c117fd16b192e70609c331641e9112af5e42

commit 7933c117fd16b192e70609c331641e9112af5e42
Author: ttuttle <ttuttle@chromium.org>
Date: Tue Jan 06 00:55:24 2015

Sanitize headers in Proxy Authentication Required responses

BUG=431504

Review URL: https://codereview.chromium.org/769043003

Cr-Commit-Position: refs/heads/master@{#310014}

[modify] http://crrev.com/7933c117fd16b192e70609c331641e9112af5e42/net/http/http_network_transaction_unittest.cc
[modify] http://crrev.com/7933c117fd16b192e70609c331641e9112af5e42/net/http/http_proxy_client_socket.cc
[modify] http://crrev.com/7933c117fd16b192e70609c331641e9112af5e42/net/http/proxy_client_socket.cc
[modify] http://crrev.com/7933c117fd16b192e70609c331641e9112af5e42/net/http/proxy_client_socket.h
[modify] http://crrev.com/7933c117fd16b192e70609c331641e9112af5e42/net/spdy/spdy_proxy_client_socket.cc


### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-25)

ttuttle@: Uh oh! This issue is still open and hasn't been updated in the last 49 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-01-25)

Please don't forget to mark bug as FIxed :)

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-17)

Merge requested to M41 (branch 2272)

### pe...@google.com (2015-02-17)

[Automated comment] Less than 2 weeks to go before stable on M41, manual review required.

### pe...@chromium.org (2015-02-18)

Merge approved for M41 branch 2272.

### pe...@chromium.org (2015-02-20)

Note: M41 stable cut happens in days, and you're approved for merge.  Get it in there!  (Let me know if you need any help, or aren't confident.)

### ti...@google.com (2015-02-23)

ttuttle: please merge this to M41 (branch 2272).

### ju...@chromium.org (2015-02-23)

Eek, sorry, will do.

### ju...@chromium.org (2015-02-23)

...just tried to cherry-pick this onto 2272, and it says the resulting commit is empty. It looks like it already made it onto that branch when it originally landed.

### pe...@chromium.org (2015-02-24)

Yup, it's in there.  No merge required, thank you.

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congratulations - $500 for this report.

Notes from reward panel: It seems it's already possible to do cookie forcing for sites that are exclusively HTTPS with HSTS, you just need a single HTTP request to _any_ origin. This particular attack also requires a non-default config. That said, the panel felt that because we made a change to this behavior and considering the severity of the issue, a reward of $500 was appropriate.

You'll be credited in the release notes as "iliwoy" - please let me know if you'd like to use a different name ASAP.

Someone from our finance team will get in contact with you in the next week or two to collect your details to arrange payment. If you don't hear from them, please either update this bug or contact me directly.

A CVE will also be assigned to this bug for your reference - stay tuned.

### ti...@google.com (2015-03-03)

Assigning CVE.

### ti...@google.com (2015-03-11)

[Empty comment from Monorail migration]

### il...@gmail.com (2015-03-13)

[Comment Deleted]

### cl...@chromium.org (2015-05-04)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/431504?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals, Internals>Network, Internals>Network>Proxy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080818)*
