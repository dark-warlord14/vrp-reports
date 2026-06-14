# QUIC proxying breaks end-to-end encryption

| Field | Value |
|-------|-------|
| **Issue ID** | [40093422](https://issues.chromium.org/issues/40093422) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Network, Internals>Network>QUIC |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | rc...@chromium.org |
| **Created** | 2018-12-12 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36

Example URL:

Steps to reproduce the problem:
In short, set up quic_server as a (not yet working) QUIC proxy and direct Chrome to proxy through the quic_server and observe what the quic_server can see.

The initial steps are the same as in https://www.chromium.org/quic/playing-with-quic

1. Generate certificates with net/tools/quic/certs/generate-certs.sh.
2. Add 2048-sha256-root.pem to local root certificate store.
3. Build quic_server.

Then start quic_server:

4. ./out/Debug/quic_server --mode=proxy --quic_proxy_backend_url=http://127.0.0.1:8080 --certificate_file=leaf_cert.pem --key_file=leaf_cert.pkcs8 --v=1 2>&1 | grep --line-buffered 'Received header'

(You don't actually need to have anything listening on local port 8080. quic_server returns "502 bad".)

5. open -n -a 'Google Chrome' --args --user-data-dir=/tmp/user1 --enable-quic --host-resolver-rules='MAP www.example.org 127.0.0.1' --origin-to-force-quic-on=www.example.org:6121 --proxy-server=quic://www.example.org:6121 https://google.com
6. Type something in the URL bar to trigger autocomplete.

What is the expected behavior?
quic_server can't observe the content of any HTTPS requests except the domain name.

HTTP requests should use CONNECT method through quic_server.

What went wrong?
quic_server is able to observe HTTPS content in clear text.

Examples (output from step 4):

[1212/145357.220644:VERBOSE1:quic_spdy_session.cc(562)] Received header list for stream 7: { :method=POST, :authority=accounts.google.com, :scheme=https, :path=/ListAccounts?gpsia=1&source=durations_metrics&json=standard, content-length=1, origin=https://www.google.com, content-type=application/x-www-form-urlencoded, user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36, accept-encoding=gzip, deflate, br, accept-language=en-US,en;q=0.9, cookie=<snip>, }

[1212/145400.246869:VERBOSE1:quic_spdy_session.cc(562)] Received header list for stream 11: { :method=GET, :authority=www.google.com, :scheme=https, :path=/complete/search?client=chrome-omni&gs_ri=chrome-ext-ansg&xssi=t&q=&oit=0&gs_rn=42&sugkey=<snip>, x-client-data=<snip>, user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36, accept-encoding=gzip, deflate, br, accept-language=en-US,en;q=0.9, cookie=<snip>, }

Did this work before? N/A 

Chrome version: 71.0.3578.80  Channel: stable
OS Version: OS X 10.14.1
Flash Version: 

This is a leftover bug from https://bugs.chromium.org/p/chromium/issues/detail?id=335275. It probably hasn't become a security bug since few are using QUIC proxies at the moment.

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### pb...@chromium.org (2018-12-12)

[Empty comment from Monorail migration]

[Monorail components: Internals>Network>QUIC]

### rc...@chromium.org (2018-12-12)

I'm unable to reproduce this behavior. I see the following output from quic_server:

...
[1212/134420.643655:VERBOSE1:quic_spdy_session.cc(581)] Received header list for stream 11: { :method=CONNECT, :authority=google.com:443, user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36, }
...

I find no entires which match both "Received header" and "https"

Can you collect a net-internals trace?

https://www.chromium.org/for-testers/providing-network-details

(You might need to follow the "Logging on startup" instructions).

### ia...@chromium.org (2018-12-12)

[Empty comment from Monorail migration]

### ki...@gmail.com (2018-12-12)

I'm not able to reproduce this on Linux either. I don't have a Mac right now, but I'm able to reproduce it on Windows.

NetLog from Windows is attached.

### ki...@gmail.com (2018-12-12)

I'm able to reproduce this on Linux after using an existing user profile. Starting from a blank user profile seems to prevent reproduction.

### rc...@chromium.org (2018-12-12)

Thank you VERY much for the prompt response!! This is alarming, but I *think* there's a chance it might be a bug related to the --origin-to-force-quic-on=www.example.org:6121 flag.

We suggest using that flag when testing the toy server because otherwise you'd need something to deliver an Alt-Svc header to tell chrome that the origin supports QUIC. But in the case of the proxy, we can get that information from the proxy's scheme. As such, I would not thing that --origin-to-force-quic-on=www.example.org:6121 would be required to use a QUIC proxy.

Can you attempt to repro without that flag?

### ki...@gmail.com (2018-12-12)

After taking out the flag I'm still able to reproduce it on Linux (with my existing user profile). The command line is:

chromium --enable-quic --host-resolver-rules='MAP www.example.org 127.0.0.1' --proxy-server=quic://www.example.org:6121 https://google.com

quic_server sees:

Received header list for stream 5: { :method=POST, :authority=www.googleapis.com, :scheme=https, :path=/oauth2/v4/token

### rc...@chromium.org (2018-12-12)

Oh, thanks for the comment about the non-empty directory being required to repro. I'm now able to repro as well.

### rc...@chromium.org (2018-12-12)

[Empty comment from Monorail migration]

### rc...@chromium.org (2018-12-12)

[Empty comment from Monorail migration]

### rc...@chromium.org (2018-12-12)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-12-13)

This likely also affects apps that use Cronet on Android and iOS.

### ca...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-12-13)

+ awhalley@ (Security TPM)

### pb...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-12-13)

+ benmason@, kbleicher@ and kariahda@ (M71 Release TPMs), this is M71 respin candidate as of now :(

### go...@chromium.org (2018-12-13)

per rch@, this doesn't affect iOS.

### ca...@chromium.org (2018-12-13)

Assigning to rch@ since they are working on a mitigation (by disabling QUIC via variations).

### ca...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

### rc...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-12-13)

OS-iOS mistakenly applied at #20, so removing it.

### me...@chromium.org (2018-12-13)

Chrome on iOS doesn't support QUIC, however Cronet (used by Youtube, Duo, Snap, etc) does. 

### me...@chromium.org (2018-12-13)

Cronet on Android uses system proxy resolver, which supports PAC scripts, but does NOT support WPAD.

### bh...@google.com (2018-12-13)

[Empty comment from Monorail migration]

### bh...@google.com (2018-12-13)

Re https://crbug.com/chromium/914497#c16, is this not holding the stable release for 71?

The Security_Severity-Critical makes this sound pretty bad.

On the other hand, if we have to respin it would be risky to do so next week, so this would mean 71 does not go out to CrOS devices until January. 

### go...@chromium.org (2018-12-13)

Re #26: Per https://crbug.com/chromium/914497#c18 rch@ is working on a mitigation (by disabling QUIC via Finch). So we may not have to respin M71 stable. rch@, could you pls confirm?

### la...@chromium.org (2018-12-13)

I think we still should respin. We can get a patch together to disable CONNECT soon (probably tonight) and mitigate this without disabling QUIC all together. My fear is that we don't know how well Google's servers will be able to handle all of Chrome having QUIC disabled.

### bh...@google.com (2018-12-13)

Doing a respin means defacto no 71 until next year due to the time it takes to qualify a new release and the impending staff reduction over the next few weeks due to holidays, at least for Chrome OS, can we disable QUIC for Chrome OS using a finch?

### la...@chromium.org (2018-12-13)

Yes, we can disable QUIC for all platforms for versions less than 71 such that if it takes a while to get 71 out for Chrome OS we'll be covered.

### me...@chromium.org (2018-12-13)

It looks like Cronet is actually not affected neither on Android nor on iOS.

### la...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e62461ede4cdb45b0bfec2e75785d2fddde768e0

commit e62461ede4cdb45b0bfec2e75785d2fddde768e0
Author: Brad Lassey <lassey@chromium.org>
Date: Thu Dec 13 04:21:09 2018

Disable the use of QUIC proxies for https:// URLs.

This is a partial revert of https://chromium-review.googlesource.com/c/chromium/src/+/858603

BUG=914497

Change-Id: I378b42b01367aca8642d49b682b121f6f8873786
Reviewed-on: https://chromium-review.googlesource.com/c/1375112
Reviewed-by: Brad Lassey <lassey@chromium.org>
Reviewed-by: Nick Harper <nharper@chromium.org>
Reviewed-by: Ryan Hamilton <rch@chromium.org>
Commit-Queue: Brad Lassey <lassey@chromium.org>
Cr-Commit-Position: refs/heads/master@{#616211}
[modify] https://crrev.com/e62461ede4cdb45b0bfec2e75785d2fddde768e0/net/http/http_stream_factory_job.cc
[modify] https://crrev.com/e62461ede4cdb45b0bfec2e75785d2fddde768e0/net/quic/quic_network_transaction_unittest.cc
[modify] https://crrev.com/e62461ede4cdb45b0bfec2e75785d2fddde768e0/net/socket/client_socket_pool_manager.cc


### rc...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

### al...@chromium.org (2018-12-13)

per https://crbug.com/chromium/914497#c31, so this bug doesn't apply to Clank either (no respin for 71 needed)?

### bu...@chromium.org (2018-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cd92d8fb7eab1c9b5a7a99bc804718157dbe7da3

commit cd92d8fb7eab1c9b5a7a99bc804718157dbe7da3
Author: Brad Lassey <lassey@chromium.org>
Date: Thu Dec 13 06:00:47 2018

Disable the use of QUIC proxies for https:// URLs.

This is a partial revert of https://chromium-review.googlesource.com/c/chromium/src/+/858603

BUG=914497

Change-Id: I378b42b01367aca8642d49b682b121f6f8873786
Reviewed-on: https://chromium-review.googlesource.com/c/1375112
Reviewed-by: Brad Lassey <lassey@chromium.org>
Reviewed-by: Nick Harper <nharper@chromium.org>
Reviewed-by: Ryan Hamilton <rch@chromium.org>
Commit-Queue: Brad Lassey <lassey@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#616211}(cherry picked from commit e62461ede4cdb45b0bfec2e75785d2fddde768e0)
Reviewed-on: https://chromium-review.googlesource.com/c/1375460
Reviewed-by: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/3639@{#2}
Cr-Branched-From: 4649b0ba5c9760073f53a859e782555c4c0e28e8-refs/heads/master@{#616124}
[modify] https://crrev.com/cd92d8fb7eab1c9b5a7a99bc804718157dbe7da3/net/http/http_stream_factory_job.cc
[modify] https://crrev.com/cd92d8fb7eab1c9b5a7a99bc804718157dbe7da3/net/quic/quic_network_transaction_unittest.cc
[modify] https://crrev.com/cd92d8fb7eab1c9b5a7a99bc804718157dbe7da3/net/socket/client_socket_pool_manager.cc


### rc...@chromium.org (2018-12-13)

aluo: Chrome on Android is affect, but not cronet on Android

### go...@chromium.org (2018-12-13)

I was trying to to trigger new canary with merge listed at #36 to get canary coverage, but canary trigger from branch 3639 is failing due to https://crbug.com/chromium/914686 :(

### rc...@chromium.org (2018-12-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-13)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rc...@chromium.org (2018-12-13)

Just an update that QUIC has been disabled via Finch as of last night.

### sh...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### rc...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### rc...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4cbcbf17db00a0011b5d232617d25db0cd3bee10

commit 4cbcbf17db00a0011b5d232617d25db0cd3bee10
Author: Ryan Hamilton <rch@chromium.org>
Date: Sat Dec 15 05:16:14 2018

Re-enable support for sending HTTPS URLs via QUIC proxies, but only when
the finch param enable_quic_proxies_for_https_urls is set.

This effectively reverts
  https://chromium-review.googlesource.com/c/chromium/src/+/1375112
and then fixes the underlying bug.

Bug: 914497,335275
Change-Id: Ief24db4226c9d063219ab7df20cf72f23973be23
Reviewed-on: https://chromium-review.googlesource.com/c/1377709
Commit-Queue: Ryan Hamilton <rch@chromium.org>
Reviewed-by: Zhongyi Shi <zhongyi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#616958}
[modify] https://crrev.com/4cbcbf17db00a0011b5d232617d25db0cd3bee10/components/network_session_configurator/browser/network_session_configurator.cc
[modify] https://crrev.com/4cbcbf17db00a0011b5d232617d25db0cd3bee10/components/network_session_configurator/browser/network_session_configurator_unittest.cc
[modify] https://crrev.com/4cbcbf17db00a0011b5d232617d25db0cd3bee10/net/http/http_network_session.cc
[modify] https://crrev.com/4cbcbf17db00a0011b5d232617d25db0cd3bee10/net/http/http_network_session.h
[modify] https://crrev.com/4cbcbf17db00a0011b5d232617d25db0cd3bee10/net/http/http_stream_factory_job.cc
[modify] https://crrev.com/4cbcbf17db00a0011b5d232617d25db0cd3bee10/net/http/http_stream_factory_job_controller.cc
[modify] https://crrev.com/4cbcbf17db00a0011b5d232617d25db0cd3bee10/net/quic/quic_network_transaction_unittest.cc
[modify] https://crrev.com/4cbcbf17db00a0011b5d232617d25db0cd3bee10/net/socket/client_socket_pool_manager.cc


### aw...@google.com (2018-12-17)

govind@ - good for 72

### aw...@google.com (2018-12-17)

[Comment Deleted]

### aw...@google.com (2018-12-17)

Requesting merge for M72 as I presume we'll want this out in Beta quickly 

### go...@chromium.org (2018-12-17)

Approving merge to M72 branch 3636 based on https://crbug.com/chromium/914497#c46 & 48. Please merge ASAP so we can pick it up for this week beta. Thank you.

### na...@google.com (2018-12-17)

[Empty comment from Monorail migration]

### rc...@chromium.org (2018-12-17)

I'll do the M72 merge now. I think we also want to merge to 71 as well so I'm requesting that now too.

### pa...@chromium.org (2018-12-17)

I think rch@ meant to request not reject.

### bu...@chromium.org (2018-12-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2044f4351e05d69808800e45d1dfbfc7adbec82a

commit 2044f4351e05d69808800e45d1dfbfc7adbec82a
Author: Ryan Hamilton <rch@chromium.org>
Date: Mon Dec 17 19:14:23 2018

[M72 merge] Disable the use of QUIC proxies for https:// URLs.

This is a partial revert of https://chromium-review.googlesource.com/c/chromium/src/+/858603

BUG=914497
TBR=lassey@chromium.org

(cherry picked from commit e62461ede4cdb45b0bfec2e75785d2fddde768e0)

Change-Id: I378b42b01367aca8642d49b682b121f6f8873786
Reviewed-on: https://chromium-review.googlesource.com/c/1375112
Reviewed-by: Brad Lassey <lassey@chromium.org>
Reviewed-by: Nick Harper <nharper@chromium.org>
Reviewed-by: Ryan Hamilton <rch@chromium.org>
Commit-Queue: Brad Lassey <lassey@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#616211}
Reviewed-on: https://chromium-review.googlesource.com/c/1380792
Cr-Commit-Position: refs/branch-heads/3626@{#401}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}
[modify] https://crrev.com/2044f4351e05d69808800e45d1dfbfc7adbec82a/net/http/http_stream_factory_job.cc
[modify] https://crrev.com/2044f4351e05d69808800e45d1dfbfc7adbec82a/net/quic/quic_network_transaction_unittest.cc
[modify] https://crrev.com/2044f4351e05d69808800e45d1dfbfc7adbec82a/net/socket/client_socket_pool_manager.cc


### rc...@chromium.org (2018-12-18)

summarizing offline conversation with govind: If we do a re-spin of M71, we'll merge this change up to M71. I'll be happy to do the merge, but if it's between 12/24 and 1/7 I'll be on vacation so zhongyi or lassey would be good choices.

### zh...@chromium.org (2018-12-19)

SGTM. I will be around during that period, just ping me if the re-spin will happen and I can help do the merge. 

### cr...@appspot.gserviceaccount.com (2018-12-19)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/2044f4351e05d69808800e45d1dfbfc7adbec82a

Commit: 2044f4351e05d69808800e45d1dfbfc7adbec82a
Author: rch@chromium.org
Commiter: rch@chromium.org
Date: 2018-12-17 19:14:23 +0000 UTC

[M72 merge] Disable the use of QUIC proxies for https:// URLs.

This is a partial revert of https://chromium-review.googlesource.com/c/chromium/src/+/858603

BUG=914497
TBR=lassey@chromium.org

(cherry picked from commit e62461ede4cdb45b0bfec2e75785d2fddde768e0)

Change-Id: I378b42b01367aca8642d49b682b121f6f8873786
Reviewed-on: https://chromium-review.googlesource.com/c/1375112
Reviewed-by: Brad Lassey <lassey@chromium.org>
Reviewed-by: Nick Harper <nharper@chromium.org>
Reviewed-by: Ryan Hamilton <rch@chromium.org>
Commit-Queue: Brad Lassey <lassey@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#616211}
Reviewed-on: https://chromium-review.googlesource.com/c/1380792
Cr-Commit-Position: refs/branch-heads/3626@{#401}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### na...@google.com (2018-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2018-12-19)

Thanks for the report. The Panel decided to reward $7,500.00 :) 

### na...@google.com (2018-12-19)

Since you are a new reporter a member of our finance will be in touch. 

Additionally, how would you like to be credited in release notes?

### ki...@gmail.com (2018-12-20)

Thank you. Please credit as Klzgrad in release notes.

Look forward to using QUIC proxies in Chrome again.

### na...@google.com (2018-12-20)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-03)

Are we intending to merge the fix from https://crbug.com/chromium/914497#c45 into M72?

### zh...@chromium.org (2019-01-03)

It's already merged in M72 per https://crbug.com/chromium/914497#c53, right?

### aw...@google.com (2019-01-03)

AIUI (possibly incorrectly!), https://crbug.com/chromium/914497#c53 disables proxy support, but 45 re-enables it with the security issue fixed. The former is indeed in M72, but the latter is only in M73. That's of course fine from a security point of view, I wasn't sure how much urgency there was in getting the functionality back.  Cheers!

### rc...@chromium.org (2019-01-08)

awhalley@ I don't think we're in a particular hurry to see the actual fix rolled out ASAP. I think it might just be safer to let it roll out organically. Sound plausible?

### aw...@google.com (2019-01-08)

Yep, that's fine - just wanted to check while there was still time :-)

### rc...@chromium.org (2019-01-09)

Thanks for checking!

### ki...@gmail.com (2019-01-16)

@rch I tried to verify the fix of re-enabling and couldn't turn it back on with --force-fieldtrials etc.

In https://chromium-review.googlesource.com/c/chromium/src/+/1377709, network_session_configurator.cc has this change:

  if (params->enable_quic) {
    params->enable_quic_proxies_for_https_urls =
        ShouldEnableQuicProxiesForHttpsUrls(quic_trial_params);
    params->enable_quic_proxies_for_https_urls = false;

Looks odd to me as the first assignment is rendered ineffective. Is this intending to re-enable it at a later time?

### rc...@chromium.org (2019-01-17)

*facepalm* Well that's thoroughly embarrassing. 

I've sent a CL out to fix:

https://chromium-review.googlesource.com/c/chromium/src/+/1417356 


### bu...@chromium.org (2019-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fd2335678e96c34d14f4b20f0d9613dfbd1ccdb4

commit fd2335678e96c34d14f4b20f0d9613dfbd1ccdb4
Author: Ryan Hamilton <rch@chromium.org>
Date: Thu Jan 17 18:31:05 2019

Fix a bug in network_session_configurator.cc in which support for HTTPS URLS in QUIC proxies was always set to false.

BUG=914497

Change-Id: I56ad16088168302598bb448553ba32795eee3756
Reviewed-on: https://chromium-review.googlesource.com/c/1417356
Auto-Submit: Ryan Hamilton <rch@chromium.org>
Commit-Queue: Zhongyi Shi <zhongyi@chromium.org>
Reviewed-by: Zhongyi Shi <zhongyi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#623763}
[modify] https://crrev.com/fd2335678e96c34d14f4b20f0d9613dfbd1ccdb4/components/network_session_configurator/browser/network_session_configurator.cc
[modify] https://crrev.com/fd2335678e96c34d14f4b20f0d9613dfbd1ccdb4/components/network_session_configurator/browser/network_session_configurator_unittest.cc


### ki...@gmail.com (2019-01-18)

[Comment Deleted]

### go...@chromium.org (2019-01-24)

We're not planning any further M71 releases, rejecting merge to M71. Please request merge to M72 if not already.

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/914497?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network, Internals>Network>QUIC]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093422)*
