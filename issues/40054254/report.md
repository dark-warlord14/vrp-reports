# Requests for script sent even when main document is text/plain

| Field | Value |
|-------|-------|
| **Issue ID** | [40054254](https://issues.chromium.org/issues/40054254) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>HTML>Parser |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | pr...@gmail.com |
| **Assignee** | ri...@arm.com |
| **Created** | 2020-12-21 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4356.6 Safari/537.36

Steps to reproduce the problem:
I've hosted a POC for easier reproduction which you can visit at;
https://cm2.pw/xza-sn.txt

The content is simply;
```
<script src=//cm2.pw></script>
```

What is the expected behavior?
No external requests should have been sent. Firefox is acting normally.

What went wrong?
External requests sent as if the page was rendered. Though, the script is not executed.

Did this work before? N/A 

Chrome version: 89.0.4356.6  Channel: dev
OS Version: 
Flash Version: 

It's probably for quick loading of external content- like preloading.

## Attachments

- [Screen Capture_google-chrome-unstable_20201221180426.png](attachments/Screen Capture_google-chrome-unstable_20201221180426.png) (image/png, 145.4 KB)
- [Screen Capture_google-chrome-unstable_20201222143334.mkv](attachments/Screen Capture_google-chrome-unstable_20201222143334.mkv) (application/octet-stream, 2.6 MB)
- [xza-sn.txt](attachments/xza-sn.txt) (text/plain, 31 B)
- [xza-meta.txt](attachments/xza-meta.txt) (text/plain, 94 B)
- [xza-meta-csp.txt](attachments/xza-meta-csp.txt) (text/plain, 100 B)
- [xza-csp.php](attachments/xza-csp.php) (text/plain, 195 B)
- [Screen Capture_google-chrome-unstable_20201223091240.png](attachments/Screen Capture_google-chrome-unstable_20201223091240.png) (image/png, 186.2 KB)

## Timeline

### pr...@gmail.com (2020-12-21)

I'm using cm2.pw which may seem same-origin but it sends requests to any other domain specified.

### [Deleted User] (2020-12-21)

[Empty comment from Monorail migration]

### pa...@chromium.org (2020-12-21)

I can't reproduce this in Chrome 87. On a page load of https://cm2.pw/xza-sn.txt, I see just the request for that page and the favicon. No request for //cm2.pw. Perhaps this bug is new in 88 or 89?

[Monorail components: Blink>HTML Blink>Loader]

### ca...@chromium.org (2020-12-22)

FWIW, I also can't reproduce in 89

### pr...@gmail.com (2020-12-22)

It doesn't work in 87. I'm in 89 dev and it's working. I've created a quick POC for demonstration. Also, please note that it also works for other tags. In the POC, you can see it's also sending requests to <img> tag.

### aj...@google.com (2020-12-22)

Verified on Canary (89.0.4364.0). Is not present on Stable (87).

Tentatively setting severity=Medium as it's not clear if this can be used to gather information such as cookies.

### aj...@google.com (2020-12-22)

Adding a couple of folks - any idea of a good person to own this?

I tried a bisect but got to the end without hitting a bad version so perhaps this is  controlled by an experiment?

[Monorail components: Blink>Loader>Preload Internals>Preload]

### tb...@chromium.org (2020-12-22)

I can repro this in incognito as well (Linux -- Chrome Dev) and with preload setting turned off. Bisect was not successful.

### pr...@gmail.com (2020-12-23)

Interestingly, it obeys the CSP rule but the violated directive indicates something else- see attached screenshot. Some weird behaviors I encountered worth noting are;
- It tries to apply some style because setting CSP default-src to 'none' will result in CSP violation. Try opening http://cm2.pw/xza-csp and see console.
- The meta tag is being parsed because if we specify CSP via meta tag, it doesn't load other resources as reported. See the difference in loading http://cm2.pw/xza-meta-csp.txt vs http://cm2.pw/xza-meta.txt

I hope it helps. If there's anything I can help with, please do let me know.

### [Deleted User] (2020-12-23)

Setting milestone and target because of Security_Impact=Beta and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-23)

[Empty comment from Monorail migration]

[Monorail components: -Blink>HTML]

### [Deleted User] (2020-12-23)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2020-12-24)

Thanks prakash0x00 - it would be great if you could upload those examples as attachments.

As most people are on vacation it might take a while for people to respond.

### pr...@gmail.com (2020-12-25)

Thank you! I just realized I forgot to attach the image in my last email. So, I'm attaching here. Happy holidays :)

### sr...@google.com (2021-01-04)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-01-04)

srinivassista@ this appears to be a legitimate regression which is why it is RB-S. ajgo@ did you determine whether this bug affects 88? If so we'll be holding the release to await a fix.

### sr...@google.com (2021-01-05)

kouhei@ kinuko@ can you ptal and help assign to a owner who can look and get a fix ready for M88 before next week stable RC cut

### fa...@chromium.org (2021-01-06)

I was on holiday. I will take a look for triage.

### fa...@chromium.org (2021-01-06)

I cannot repro this on Mac Canary 89.0.4379.0 or on Linux Chromium ToT. This might be controlled by an experiment which makes it difficult to debug.

If someone can reproduce this still on canary, can you share the entire contents of chrome://version here?

### ki...@chromium.org (2021-01-06)

Interestingly I can't repro this on my ToT build (on Linux, 89.0.4380.0) or Canary (on Mac, 89.0.4379.0), 
while I was able to repro this on my Dev on Mac (89.0.4356.6).

Might it be due to some flags, or this gets fixed between 89.0.4356.6 and 89.0.4379.0?

### ki...@chromium.org (2021-01-06)

From the Dev build that I was able to repro:

Google Chrome	89.0.4356.6 (Official Build) dev (x86_64)
Revision	8689d5f68d3ce081fb0b81230a4f316c03221418-refs/branch-heads/4356@{#11}
OS	macOS Version 10.14.5 (Build 18F132)
JavaScript	V8 8.9.146

Variations	583720e7-d7c239a
84085631-377be55a
90a7075b-7fc01d00
16b16054-3f4a17df
b0f75187-48db8a45
91f8f623-f23d1dea
59b6f412-cf05fe7d
60d4b352-30821c44
4ca682fe-682471ec
b3249ec4-3f4a17df
82b62ecf-e7d7ef40
a9ef513c-f23d1dea
da89714-4267e969
1d52c63e-ca7d8d80
55c044d3-3f4a17df
95b880ad-ca7d8d80
8ae424bf-26bf9cdb
9d6a857b-4804dae4
3c98d047-f23d1dea
74f8fa8f-f23d1dea
4d2d969c-27a0c3c6
ca05d627-3f4a17df
4d936449-1978aa4
6d6d60a5-1b0f4679
38b9885d-7a8348dd
1298fecf-fa5291ee
9e604a08-8b3820f7
d97d6ab5-f562af19
41e765a5-f23d1dea
8e44abde-3f4a17df
dc742ded-1fa49821
6f212d51-3f4a17df
8f83697a-ca7d8d80
8f000ce6-ca7d8d80
dbf7a8af-dd20d31b
f2cb61f-3f4a17df
c3aebffb-f23d1dea
8470b833-4d5912c3
195288ce-9c9fa216
a6baf2da-e24c5b30
b67c7fd1-f23d1dea
65570806-f7fb3d30
2cff698a-548d881a
9f9c8297-3f4a17df
a582a1b8-ad75ce17
1d606bb5-3de9d90b
247004c0-377be55a
3042ad4b-a0e56f74
e4a357e9-79b0fbfd
10bea3af-bb72e3e9
3fd33f16-1d4e34ed
13200569-b4779eec
676784ca-89266556
bebfb376-f054aa61
2729b628-1663e292
df6713a3-f23d1dea
5252c71-ca7d8d80
5a53e38-afe2ea9b
6a116980-64062496
e4b8f636-3f4a17df
fab3c74d-3f4a17df
e79de56c-3f4a17df
357a64de-f23d1dea
142e58d7-f2d1370b
a168b3cd-f23d1dea
3ee82fb3-3a447918
fa6aa590-ca7d8d80
c992f345-ca7d8d80
165e16d1-3f4a17df
f403643c-dfe0d329
28114f9b-629cd37d
8155c77d-ca7d8d80
d8692482-ca7d8d80
a042f0b2-ca7d8d80
638e38ae-125ca470
7a911e9f-a3a14831
38fb2686-ca7d8d80
bdbcc4a1-5f02e174
9baaefe3-f23d1dea
f8870c0a-ee63ae02
dad74fac-f23d1dea
e153f4cb-77f964a1
2f990be4-f2718d9f
1c1d6a98-f23d1dea
3487aa71-86f8c66a
53c99a5a-7b205e52
d3566fbd-ca7d8d80
ae85586a-3f4a17df
4ea303a6-e8073b2e
7048821f-352b4361
a5c209bc-ca7d8d80
5213bf1c-5419e7bd
c46bc5ff-f23d1dea
f48aee36-3f4a17df
e4e7724d-3f4a17df
2ce51440-3f4a17df
d6f4076c-29c53a5
cda97d6c-f23d1dea
4fff8ec0-3f4a17df
3d415583-f23d1dea
58cac63b-41ac8554
78063874-f23d1dea
ef4764d7-71c5eda6
d0ff70be-ee63ae02
a375a87b-f23d1dea
7760b5b2-6bb23449
1625732c-377be55a
9ca8521a-1855b0
39baae47-ca7d8d80
931c5f72-ffe31356
97f5b53e-3f4a17df
494d8760-52325d43
3ac60855-486e2a9c
63dcb6a3-eaceac83
e706e746-c61982e5
f296190c-4235cfc1
4442aae2-6e597ede
f690cf64-6e597ede
ed1d377-e1cc0f14
75f0f0a0-a5822863
e2b18481-a5822863
e7e71889-e1cc0f14
3a8271ac-12c226
b1ceb06f-51f64ec2
7975f5b5-ca7d8d80
e1368496-3f4a17df
27435f03-ddc7a09a
a5fa7f3a-efad1e7f
cddbdd4e-f23d1dea
af948703-7b6a47ba
fb50494f-3d47f4f4
8db2e42f-d00b53ff
5e31bb48-2ba52008
75b51224-fd9b29fc
3ed25c66-f23d1dea
a461b170-3f4a17df
dd82d379-95b900e
1fadabdc-4a2705f0


### fa...@chromium.org (2021-01-06)

Thanks. I cannot repro on a Chromium build on Linux at that version 89.0.4356.6:

Chromium	89.0.4356.6 (Developer Build) (64-bit)
Revision	8689d5f68d3ce081fb0b81230a4f316c03221418-refs/branch-heads/4356@{#11}
OS	Linux
JavaScript	V8 8.9.146
User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4356.6 Safari/537.36
Command Line	out/Default/chrome --user-data-dir=/tmp/zjhzjz --flag-switches-begin --flag-switches-end
Executable Path	/work/chrome/src/out/Default/chrome
Profile Path	/tmp/zjhzjz/Default
Variations	317c6f31-7924aa1e
b0f75187-3f4a17df
f88a4127-2874767e
1d52c63e-71a21aa6
55c044d3-3f4a17df
95b880ad-3f4a17df
3fa8d059-3fa8d059
8ae424bf-8ae424bf
fc1c890b-3f4a17df
9d6a857b-834dc75
74f8fa8f-74f8fa8f
6d6d60a5-1b0f4679
7c1bc906-5b0c5a6b
8950ab95-3f4a17df
1298fecf-3f4a17df
9a13dddd-3f4a17df
9e604a08-9e604a08
71ed337-71ed337
41e765a5-c9d32f6d
e9b35dd7-3f4a17df
34cec289-3f4a17df
dc742ded-cff8907
6f212d51-3f4a17df
8470b833-3f4a17df
195288ce-3f549db2
853cc81d-853cc81d
345a470a-6b1d6b1c
35de6590-9a61cc01
247004c0-3f4a17df
4fa0e976-3f4a17df
d16d5274-3f4a17df
b1c1108d-7f5e2445
8b943c2e-3f4a17df
3042ad4b-9fa4b1c7
e4a357e9-3f4a17df
10bea3af-d6018680
353e3078-1d4e34ed
676784ca-3f4a17df
76500833-3f4a17df
32b4d334-3f4a17df
5252c71-3f4a17df
f394654f-1690ecf7
63777dd8-61ca18c2
149efb5c-3f4a17df
164e9c81-3f4a17df
a168b3cd-3f4a17df
29c62d4-3f4a17df
3ee82fb3-3f4a17df
c743f1fa-3f4a17df
9e5c75f1-30e1b12b
f403643c-6843e1ea
d8692482-fe3984ae
35856c93-fba8dfb0
409d0de4-3f4a17df
dad74fac-3f4a17df
e153f4cb-afe2ea9b
2f990be4-6cf6392a
3487aa71-26bbc519
6b988f02-3f4a17df
e840aad6-3f4a17df
23a898eb-fc93cf74
53c99a5a-6fed37b6
44f6f28f-4af31d64
cfc474d9-bca3480e
e06975bf-928c6685
ce12bb93-7c7ea110
ae85586a-3f4a17df
4ea303a6-3f4a17df
7048821f-47956228
8c4a4826-135b76e5
9dbcde90-3f4a17df
5417468-3f4a17df
2ce51440-3f4a17df
d6f4076c-3f4a17df
dcf9ab0d-3f4a17df
4fff8ec0-3f4a17df
28be2392-3f4a17df
d8a3c963-cfbda022
ef4764d7-c9f4d4ef
a05687fd-9e57a090
a375a87b-3f4a17df
7760b5b2-3f4a17df
1625732c-3f4a17df
a31fbbab-3f4a17df
32ffd3e7-a4c26c20
1354da85-f1a864dc
931c5f72-3f4a17df
8239ce46-3f4a17df
97f5b53e-97f5b53e
b1ceb06f-6b7b34d
5915d2b-3f4a17df
6a2df91f-6a2df91f
ffc4ca9f-ffc4ca9f
e1368496-3d47f4f4
27435f03-65a1acc8
a5fa7f3a-3f4a17df
bf71d7e4-3f4a17df
b53f3ef9-3f4a17df


### tb...@chromium.org (2021-01-06)

I can repro it consistenly on 89.0.4356.6 (Official Build) dev (Linux).

Variations	84085631-377be55a
90a7075b-c35b35af
16b16054-f23d1dea
b0f75187-f23d1dea
8907c951-377be55a
91f8f623-3f4a17df
59b6f412-cf05fe7d
60d4b352-30821c44
4ca682fe-682471ec
b3249ec4-3f4a17df
82b62ecf-e7d7ef40
a9ef513c-f23d1dea
da89714-4ad60575
1d52c63e-ca7d8d80
55c044d3-f23d1dea
95b880ad-f23d1dea
8ae424bf-26bf9cdb
9d6a857b-4804dae4
74f8fa8f-b947d8e6
4d2d969c-27a0c3c6
ca05d627-3f4a17df
4d936449-1978aa4
6d6d60a5-dec40624
38b9885d-ca7d8d80
1298fecf-fa5291ee
9e604a08-87838f9d
8e44abde-3f4a17df
dc742ded-1fa49821
6f212d51-65bced95
8f83697a-642f0130
8f000ce6-2ec2b923
dbf7a8af-ca7d8d80
f2cb61f-f23d1dea
c3aebffb-3f4a17df
2bad31a-3f4a17df
8470b833-72dac69b
195288ce-ca7d8d80
a6baf2da-f23d1dea
e820ebea-e5d1a081
b67c7fd1-f23d1dea
2cff698a-548d881a
a582a1b8-ad75ce17
1d606bb5-3de9d90b
247004c0-377be55a
3042ad4b-a0e56f74
e4a357e9-43949b56
10bea3af-bb72e3e9
b5b4a391-65bced95
3fd33f16-1d4e34ed
13200569-b4779eec
676784ca-56f8618f
bebfb376-f054aa61
2729b628-4bb5c16f
5252c71-65bced95
5a53e38-8dcd7229
fab3c74d-f23d1dea
e79de56c-f23d1dea
357a64de-3f4a17df
142e58d7-6f77aaec
22d5aaf8-ca7d8d80
a168b3cd-3f4a17df
3ee82fb3-3a447918
fa6aa590-ca7d8d80
c992f345-ca7d8d80
165e16d1-3f4a17df
f403643c-dfe0d329
28114f9b-a3a14831
8155c77d-f23d1dea
37b46535-726b2da0
a042f0b2-ca7d8d80
638e38ae-125ca470
7a911e9f-d5c77a9
38fb2686-ca7d8d80
bdbcc4a1-76ab633a
9baaefe3-3f4a17df
f8870c0a-5419e7bd
dad74fac-3f4a17df
e153f4cb-6cf79a79
2f990be4-f2718d9f
1c1d6a98-f23d1dea
3487aa71-26bbc519
6b988f02-65bced95
e840aad6-f23d1dea
53c99a5a-7b205e52
d3566fbd-ca7d8d80
ae85586a-3f4a17df
4ea303a6-ecbb250e
7048821f-31208845
a5c209bc-ca7d8d80
5213bf1c-ee63ae02
c46bc5ff-f23d1dea
3d7e3f6a-2eb01455
f48aee36-65bced95
e4e7724d-3f4a17df
2ce51440-3f4a17df
d6f4076c-aa0c56c8
cda97d6c-3f4a17df
4fff8ec0-3f4a17df
3d415583-f23d1dea
58cac63b-ca7d8d80
78063874-f23d1dea
ef4764d7-bd357d6b
d0ff70be-ee63ae02
a375a87b-3f4a17df
7760b5b2-6bb23449
9ca8521a-993b9ffd
bf15c287-65bced95
39baae47-ca7d8d80
931c5f72-c89460a
97f5b53e-3f4a17df
494d8760-52325d43
f624d1fa-80deee2a
3ac60855-3ec2a267
63dcb6a3-2624949d
e706e746-da90e0d0
f296190c-9d9eea77
4442aae2-4ad60575
f690cf64-a90023b1
ed1d377-e1cc0f14
75f0f0a0-d7f6b13c
e2b18481-92bb99a9
e7e71889-e1cc0f14
3a8271ac-12c226
b1ceb06f-6b7b34d
f98b6633-f9a43703
ad4e39a2-65bced95
7975f5b5-ca7d8d80
e1368496-3f4a17df
27435f03-ddc7a09a
a5fa7f3a-efad1e7f
1166396-60b4259
fb50494f-72cac062
8db2e42f-d00b53ff
5e31bb48-75513c66
3ed25c66-80162158
dd82d379-a7795cab
b53f3ef9-65bced95
1fadabdc-309fb3bf


### tb...@chromium.org (2021-01-06)

Just bisected this https://source.chromium.org/chromium/chromium/src/+/master:tools/variations/bisect_variations.py since I was able to repro this consistently.

I can repro with --enable-features=ForceSynchronousHTMLParsing, but can't repro with --disable-features=ForceSynchronousHTMLParsing. falken@ also seemed to confirm the findings on his browswer.

Assigning to masonfreed@ who owns the experiment. Also, cc'ing 	richard.townsend@arm.com since it seems related to https://crbug.com/chromium/901056 (Thanks falken@ for the link).


### fa...@chromium.org (2021-01-06)

Thanks. Yes I could confirm tbansal's findings on Mac Canary 89.0.4379.0. As the feature looks disabled by default and is only enabled by experiment on 89+, I'll reset Security_Impact too.

[Monorail components: -Blink>Loader -Blink>Loader>Preload -Internals>Preload Blink>HTML>Parser]

### fa...@chromium.org (2021-01-06)

[Empty comment from Monorail migration]

### ri...@arm.com (2021-01-06)

OK, this is pretty bad - I think the issue stems from TextDocumentParser being a subset of HTMLDocumentParser and hence it's feeding the plain HTML string into the HTMLPreloadScanner upon ::Append, should be a fairly simple fix but I'll try to add a test to confirm the expected behaviour.

### ri...@arm.com (2021-01-06)

Successfully generated a WPT test to expose the problem. 

### ri...@arm.com (2021-01-06)

Think I currently have a fix for the issue, now undergoing internal review @arm and validation.

### ri...@arm.com (2021-01-06)

WIP CL here: https://chromium-review.googlesource.com/c/chromium/src/+/2613008

### [Deleted User] (2021-01-06)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2e945073ad9561cb5671c1305d1defb6a8219e76

commit 2e945073ad9561cb5671c1305d1defb6a8219e76
Author: Richard Townsend <Richard.Townsend@arm.com>
Date: Thu Jan 07 18:14:58 2021

fix: disable prefetching for TextDocument

The synchronous HTMLDocumentParser mode was incorrectly dispatching
preloads for text/plain documents by interpreting their contents as
HTML. This CL extends the HTMLDocumentParser's constructor, adds a
new enum to disable this behaviour, and a Web Platform Test to show
that the unintended prefetching no longer happens.

Bug: 1160665
Change-Id: I07902d58e3bc06ce6ecc07c341e997846d6e5a64
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2613008
Commit-Queue: Richard Townsend <richard.townsend@arm.com>
Reviewed-by: Mason Freed <masonfreed@chromium.org>
Cr-Commit-Position: refs/heads/master@{#841110}

[modify] https://crrev.com/2e945073ad9561cb5671c1305d1defb6a8219e76/third_party/blink/renderer/core/html/parser/html_document_parser.cc
[add] https://crrev.com/2e945073ad9561cb5671c1305d1defb6a8219e76/third_party/blink/web_tests/external/wpt/preload/avoid-prefetching-on-text-plain-inner.html
[add] https://crrev.com/2e945073ad9561cb5671c1305d1defb6a8219e76/third_party/blink/web_tests/external/wpt/preload/avoid-prefetching-on-text-plain-inner.html.headers
[add] https://crrev.com/2e945073ad9561cb5671c1305d1defb6a8219e76/third_party/blink/web_tests/external/wpt/preload/avoid-prefetching-on-text-plain.html
[modify] https://crrev.com/2e945073ad9561cb5671c1305d1defb6a8219e76/third_party/blink/web_tests/TestExpectations
[modify] https://crrev.com/2e945073ad9561cb5671c1305d1defb6a8219e76/third_party/blink/renderer/core/html/parser/text_document_parser.cc
[modify] https://crrev.com/2e945073ad9561cb5671c1305d1defb6a8219e76/third_party/blink/renderer/core/html/parser/html_document_parser.h
[modify] https://crrev.com/2e945073ad9561cb5671c1305d1defb6a8219e76/third_party/blink/web_tests/VirtualTestSuites


### ri...@arm.com (2021-01-08)

[Empty comment from Monorail migration]

### fa...@chromium.org (2021-01-08)

Thanks richard.townsend for the quick fix and tbansal for the sleuthing of variations!

### ri...@arm.com (2021-01-08)

It's not quite fixed yet (the regression test I introduced is flaky) but the underlying issue should have been sorted - hasn't hit canary just yet though. 

### ri...@arm.com (2021-01-08)

Moving back to WIP as there seems to be a couple of stability problems with the above change (apologies).

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/53671fc6ba1ba7963fe8418c676c3f8251d387be

commit 53671fc6ba1ba7963fe8418c676c3f8251d387be
Author: Richard Townsend <Richard.Townsend@arm.com>
Date: Fri Jan 08 19:29:30 2021

fixup: ensure HTMLPreloadScanner construction on Append

Attempts to fix an ASAN-detected crash for IsPrefetchOnly() Documents.

Bug: 901056, 1164226, 1160665, 1164377
Change-Id: I74c75c58d3e2d9319f67997e3b08d1ab7d5e008d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2618362
Reviewed-by: Mason Freed <masonfreed@chromium.org>
Commit-Queue: Richard Townsend <richard.townsend@arm.com>
Cr-Commit-Position: refs/heads/master@{#841588}

[modify] https://crrev.com/53671fc6ba1ba7963fe8418c676c3f8251d387be/third_party/blink/renderer/core/html/parser/html_document_parser.cc


### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### pr...@gmail.com (2021-01-27)

Hi, any updates here? Is this eligible for bounty?

### ad...@chromium.org (2021-01-27)

richard.townsend@ - please mark this as fixed if https://crbug.com/chromium/1160665#c38 is complete...?

prakash0x00@ - when this is marked fixed it will go to the VRP panel for consideration of reward.

### [Deleted User] (2021-01-27)

I can confirm that with 90.0.4399.0 (which includes the https://crbug.com/chromium/1160665#c38 patch), this issue is fixed.

### [Deleted User] (2021-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-28)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-18)

Hello, Prakash! The VRP Panel has decided to award you $500 for this report. Thank you for this submission and your efforts!

### aw...@google.com (2021-02-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1160665?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1164166, crbug.com/chromium/1164226, crbug.com/chromium/1164377]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054254)*
