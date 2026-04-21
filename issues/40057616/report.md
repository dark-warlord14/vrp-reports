# Security: the contents of iframe is placed outside of iframe when CSS "column-width" is defined in main frame.

| Field | Value |
|-------|-------|
| **Issue ID** | [40057616](https://issues.chromium.org/issues/40057616) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Paint |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ss...@snu.ac.kr |
| **Assignee** | pd...@chromium.org |
| **Created** | 2021-10-15 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

The contents of iframe is placed outside of iframe when CSS "column-width" is defined in main frame.

**VERSION**  

Chrome Version: 95.0.4638.49 + beta  

Operating System: Ubuntu 18.04

**REPRODUCTION CASE**  

(1) Download "parent.html" and "child.html"  

(2) Make a local server for "parent.html" by running "python3 -m http.server 9000"  

(2) Make the other local server for "child.html" by running "python3 -m http.server 8000" in terminal.  

(3) Open "<http://0.0.0.0:9000/parent.html>" in Chrome.

The contents of iframe should be in iframe,  

but the button element is drawn outside of iframe and it is also clickable.

This happens when the main frame and iframe are different domains.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Suhwan Song

## Attachments

- [parent.html](attachments/parent.html) (text/plain, 371 B)
- [child.html](attachments/child.html) (text/plain, 148 B)
- [Screenshot.png](attachments/Screenshot.png) (image/png, 130.2 KB)
- [Screenshot_click.png](attachments/Screenshot_click.png) (image/png, 148.8 KB)
- [parent.html](attachments/parent.html) (text/plain, 369 B)
- [chrome___version.png](attachments/chrome_version.png) (image/png, 783.0 KB)

## Timeline

### [Deleted User] (2021-10-15)

[Empty comment from Monorail migration]

### bd...@chromium.org (2021-10-15)

@pdr can you take a look at this? This seems simliar to 1119651

[Monorail components: Blink>Paint]

### [Deleted User] (2021-10-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-19)

[Empty comment from Monorail migration]

### ss...@snu.ac.kr (2021-10-29)

There was a minor error in parent.html so please use this parent.html instead.

### pd...@chromium.org (2021-11-03)

I'm unable to reproduce this in 95.0.4638.49 or 97.0.4685.0/canary.

Can you reproduce this in either stable or canary? If so, can you paste the full chrome://version (including variations)?

### sc...@chromium.org (2021-11-03)

[Empty comment from Monorail migration]

### sc...@chromium.org (2021-11-03)

I'll dupe the other one into this one, but note the other bug has a better test case. But this one has the security information and was the first report.

### sc...@chromium.org (2021-11-03)

[Empty comment from Monorail migration]

### sc...@chromium.org (2021-11-03)

[Empty comment from Monorail migration]

### sc...@chromium.org (2021-11-03)

[Empty comment from Monorail migration]

### ss...@snu.ac.kr (2021-11-04)

I can reproduce this bug in the recent stable version (95.0.4638.69).
This happens only when the main frame and iframe are different domains. If they have the same domain, this is not reproducible.

I attached the full chrome://version below.


Google Chrome	95.0.4638.69 (Official Build) (64-bit)
Revision	6a1600ed572fedecd573b6c2b90a22fe6392a410-refs/branch-heads/4638@{#984}
OS	Linux
JavaScript	V8 9.5.172.25
User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
Command Line	/usr/bin/google-chrome-stable --enable-crashpad --enable-crashpad --flag-switches-begin --enable-gpu-rasterization --flag-switches-end
Executable Path	/opt/google/chrome/google-chrome
Profile Path	/home/suhwan/.config/google-chrome/Default
Variations	f475deb0-377be55a
7e184ca7-ca7d8d80
90a7075b-8456389e
16b16054-377be55a
8e73c278-ca7d8d80
1fa5b2f3-377be55a
59b6f412-377be55a
60d4b352-377be55a
5fff72eb-377be55a
b3249ec4-6edc92c7
a9ef513c-1f8c5973
273268f8-a9c1148c
6cb5e962-377be55a
6e08fc3e-ca7d8d80
eddd0d82-ad1aa0
87f33ad6-ca7d8d80
5d093a14-377be55a
3095aa95-3f4a17df
e799dcad-12ede6a2
edb58ea9-377be55a
a2629469-377be55a
1bb6a450-ca7d8d80
6c5f69af-ca7d8d80
47bd2c48-ca7d8d80
1e7be480-377be55a
1e940a7c-ca7d8d80
76cbd0ec-12ede6a2
47b5f350-377be55a
7c2504d0-ca7d8d80
f2cb61f-377be55a
a2fd384c-5c0c03aa
5d77151b-377be55a
bf4029fe-364c5591
65570806-20f58b6f
e17bdae7-9c88f5c6
53fd5552-12ede6a2
dd8d67e-6edc92c7
f6f5c542-12ede6a2
a582a1b8-ad75ce17
fa659f2e-ca7d8d80
da2d8531-ca7d8d80
e87da360-ca7d8d80
6a5f15b-ca7d8d80
d89faab1-ca7d8d80
722b8030-eb2b3b01
5f2c0f7c-12ede6a2
e4a357e9-ca7d8d80
c129e4cd-ca7d8d80
f96fd6bf-baf1bee6
ff5d84e6-ca7d8d80
12325be2-ca7d8d80
8bccc03b-ca7d8d80
29c62d4-ca7d8d80
178e8b37-ca7d8d80
facdb7bf-ca7d8d80
2b4e7fda-7c67a119
ea90e0df-a5f02e39
d809cc5d-377be55a
7a911e9f-80311101
b75782da-ca7d8d80
8c8d8faf-6edc92c7
255dfea8-ca7d8d80
cbb84eed-4481e2ca
e153f4cb-377be55a
ca5a2953-ca7d8d80
3487aa71-ca7d8d80
c2983992-377be55a
5fe247df-ca7d8d80
ad46906e-ca7d8d80
234de0a0-ca7d8d80
261b9697-377be55a
d3566fbd-8ca19036
4ea303a6-ecbb250e
cb47d7a6-377be55a
f48aee36-377be55a
c9e4cf65-12ede6a2
3f92a30f-ca7d8d80
9af490f6-ca7d8d80
ad143c8a-ca7d8d80
ba0caa38-377be55a
2e36b1b8-ce2253d3
c1003591-ca7d8d80
fbe267b5-ca7d8d80
a0da97d6-ca7d8d80
a8a03ccf-ca7d8d80
f323d3f0-377be55a
5d2c15d5-c215f90e
5176c13e-ca7d8d80
7760b5b2-ca7d8d80
eb084fc2-a79d803f
9dea8d36-6edc92c7
e8c68789-ca7d8d80
1354da85-781294a7
ad4acdda-ca7d8d80
931c5f72-a13b54eb
494d8760-52325d43
3ac60855-486e2a9c
63dcb6a3-90ee1655
e706e746-e2e298f1
f296190c-22cd16e0
4442aae2-6e3b1976
f690cf64-75cb33fc
ed1d377-e1cc0f14
75f0f0a0-e1cc0f14
e2b18481-e1cc0f14
e7e71889-e1cc0f14
6aa685f2-ca7d8d80
b1ceb06f-d1372334
25692333-ca7d8d80
6ab03ba1-8cd0bc9c
2d3dfd19-ca7d8d80
e1368496-ca7d8d80
248e3a0-ca7d8d80
3b96a1d-ca7d8d80
dba92675-2e96769
595f5eb0-ca7d8d80
3673692f-12ede6a2
bef5c006-ca7d8d80
a16ee973-13c63153
b4e05be7-9c7cf9bf
1b4184a1-12040260
fb50494f-72cac062
7cbb4bd9-3d47f4f4
547e761a-3f4a17df
89f843ca-2cbb00ec
5e31bb48-75513c66
a9deeaf7-bcdae55b
d661ac70-20c6468c
a461b170-377be55a
dd82d379-33c3eba5
def27776-ca7d8d80
8d7344de-ca7d8d80
733cb831-ca7d8d80
6598898b-ca7d8d80
b53f3ef9-ca7d8d80

### gi...@appspot.gserviceaccount.com (2021-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/59e91c953a4fc1c552a301910bf23c6f0c9581df

commit 59e91c953a4fc1c552a301910bf23c6f0c9581df
Author: Xianzhu Wang <wangxianzhu@chromium.org>
Date: Thu Nov 04 20:49:37 2021

Fix paint location of RemoteFrameView foreign layer

Bug: 1260250
Change-Id: If0fa74fab0c075d7eb920bf3775d9726fa3eff9c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3261010
Reviewed-by: Philip Rogers <pdr@chromium.org>
Commit-Queue: Xianzhu Wang <wangxianzhu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#938483}

[add] https://crrev.com/59e91c953a4fc1c552a301910bf23c6f0c9581df/third_party/blink/web_tests/external/wpt/html/rendering/replaced-elements/embedded-content/cross-domain-iframe-in-multicol.sub-ref.html
[modify] https://crrev.com/59e91c953a4fc1c552a301910bf23c6f0c9581df/third_party/blink/renderer/core/frame/remote_frame_view.cc
[add] https://crrev.com/59e91c953a4fc1c552a301910bf23c6f0c9581df/third_party/blink/web_tests/external/wpt/html/rendering/replaced-elements/embedded-content/cross-domain-iframe-in-multicol.sub.html


### wa...@chromium.org (2021-11-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1f1fb48502a482888cbc6ab9c462e23e74a672b5

commit 1f1fb48502a482888cbc6ab9c462e23e74a672b5
Author: Xianzhu Wang <wangxianzhu@chromium.org>
Date: Thu Nov 04 23:29:18 2021

Fix composited plugin paint offset in multicol

Bug: 1260250
Change-Id: I675b5e1273da7a4bc388a688b6ecea4b4dafa7db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3262916
Reviewed-by: Philip Rogers <pdr@chromium.org>
Commit-Queue: Xianzhu Wang <wangxianzhu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#938581}

[add] https://crrev.com/1f1fb48502a482888cbc6ab9c462e23e74a672b5/third_party/blink/web_tests/plugins/plugin-in-multicol-expected.html
[add] https://crrev.com/1f1fb48502a482888cbc6ab9c462e23e74a672b5/third_party/blink/web_tests/plugins/plugin-in-multicol-expected.txt
[modify] https://crrev.com/1f1fb48502a482888cbc6ab9c462e23e74a672b5/third_party/blink/renderer/core/exported/web_plugin_container_impl.cc
[add] https://crrev.com/1f1fb48502a482888cbc6ab9c462e23e74a672b5/third_party/blink/web_tests/plugins/plugin-in-multicol.html


### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### wa...@chromium.org (2021-11-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-05)

Merge review required: M96 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wa...@chromium.org (2021-11-06)

1. The CL fixes a rendering regression and a potential security issue which exists in M-96 with ReleaseBlock-Stable
2. https://chromium-review.googlesource.com/c/chromium/src/+/3261010 and https://chromium-review.googlesource.com/c/chromium/src/+/3262916
3. Yes
4. It behind finch flag CompositeAfterPaint
5. N/A. Not ChromeOS specific.
6. Yes. This can be verified according to https://crbug.com/chromium/1260250#c0 or https://crbug.com/chromium/1266157.

### sr...@google.com (2021-11-08)

Merge approved for M96 branch:4664 please merge asap as we are cutting stable RC tomorrow ( Tuesday Nov 9)

### wa...@chromium.org (2021-11-08)

https://chromium-review.googlesource.com/c/chromium/src/+/3262916 also needs to be merged into M97.

### [Deleted User] (2021-11-08)

Merge approved: your change passed merge requirements and is auto-approved for M97. Please go ahead and merge the CL to branch 4692 (refs/branch-heads/4692) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/14f041fef841871714b6b56aa01026e82b6cf6c8

commit 14f041fef841871714b6b56aa01026e82b6cf6c8
Author: Xianzhu Wang <wangxianzhu@chromium.org>
Date: Mon Nov 08 21:11:19 2021

Fix paint location of RemoteFrameView foreign layer

(cherry picked from commit 59e91c953a4fc1c552a301910bf23c6f0c9581df)

Bug: 1260250
Change-Id: If0fa74fab0c075d7eb920bf3775d9726fa3eff9c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3261010
Reviewed-by: Philip Rogers <pdr@chromium.org>
Commit-Queue: Xianzhu Wang <wangxianzhu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#938483}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3268533
Commit-Queue: Philip Rogers <pdr@chromium.org>
Auto-Submit: Xianzhu Wang <wangxianzhu@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#870}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[add] https://crrev.com/14f041fef841871714b6b56aa01026e82b6cf6c8/third_party/blink/web_tests/external/wpt/html/rendering/replaced-elements/embedded-content/cross-domain-iframe-in-multicol.sub-ref.html
[modify] https://crrev.com/14f041fef841871714b6b56aa01026e82b6cf6c8/third_party/blink/renderer/core/frame/remote_frame_view.cc
[add] https://crrev.com/14f041fef841871714b6b56aa01026e82b6cf6c8/third_party/blink/web_tests/external/wpt/html/rendering/replaced-elements/embedded-content/cross-domain-iframe-in-multicol.sub.html


### gi...@appspot.gserviceaccount.com (2021-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/38893aebad0eb99bd3f27a7201d1aac52f0a4299

commit 38893aebad0eb99bd3f27a7201d1aac52f0a4299
Author: Xianzhu Wang <wangxianzhu@chromium.org>
Date: Mon Nov 08 21:24:41 2021

Fix composited plugin paint offset in multicol

(cherry picked from commit 1f1fb48502a482888cbc6ab9c462e23e74a672b5)

Bug: 1260250
Change-Id: I675b5e1273da7a4bc388a688b6ecea4b4dafa7db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3262916
Reviewed-by: Philip Rogers <pdr@chromium.org>
Commit-Queue: Xianzhu Wang <wangxianzhu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#938581}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3268458
Commit-Queue: Philip Rogers <pdr@chromium.org>
Auto-Submit: Xianzhu Wang <wangxianzhu@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#872}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[add] https://crrev.com/38893aebad0eb99bd3f27a7201d1aac52f0a4299/third_party/blink/web_tests/plugins/plugin-in-multicol-expected.html
[add] https://crrev.com/38893aebad0eb99bd3f27a7201d1aac52f0a4299/third_party/blink/web_tests/plugins/plugin-in-multicol-expected.txt
[modify] https://crrev.com/38893aebad0eb99bd3f27a7201d1aac52f0a4299/third_party/blink/renderer/core/exported/web_plugin_container_impl.cc
[add] https://crrev.com/38893aebad0eb99bd3f27a7201d1aac52f0a4299/third_party/blink/web_tests/plugins/plugin-in-multicol.html


### gi...@appspot.gserviceaccount.com (2021-11-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1cf0572c00f7e75f34c903818bcefc2627267762

commit 1cf0572c00f7e75f34c903818bcefc2627267762
Author: Xianzhu Wang <wangxianzhu@chromium.org>
Date: Mon Nov 08 21:27:28 2021

Fix composited plugin paint offset in multicol

(cherry picked from commit 1f1fb48502a482888cbc6ab9c462e23e74a672b5)

Bug: 1260250
Change-Id: I675b5e1273da7a4bc388a688b6ecea4b4dafa7db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3262916
Reviewed-by: Philip Rogers <pdr@chromium.org>
Commit-Queue: Xianzhu Wang <wangxianzhu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#938581}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3268461
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Xianzhu Wang <wangxianzhu@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4692@{#19}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[add] https://crrev.com/1cf0572c00f7e75f34c903818bcefc2627267762/third_party/blink/web_tests/plugins/plugin-in-multicol-expected.html
[add] https://crrev.com/1cf0572c00f7e75f34c903818bcefc2627267762/third_party/blink/web_tests/plugins/plugin-in-multicol-expected.txt
[modify] https://crrev.com/1cf0572c00f7e75f34c903818bcefc2627267762/third_party/blink/renderer/core/exported/web_plugin_container_impl.cc
[add] https://crrev.com/1cf0572c00f7e75f34c903818bcefc2627267762/third_party/blink/web_tests/plugins/plugin-in-multicol.html


### am...@google.com (2022-03-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-23)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. A member of our finance team will reach out to you soon to arrange payment. Sincere apologies for the delay in getting a reward issue to you as we work through a backlog of low severity reward decisions. Thank you for your patience, your efforts in finding security bugs in Chrome, and reporting this issue to us! 

### am...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### ss...@snu.ac.kr (2022-08-29)

Could you give CVE to this bug?

### am...@chromium.org (2022-11-16)

It looks like since this issue is labeled as Regression rather than a Security issue, it missed our automation. 
https://ccrev.com/c//3261010 was released in 97.0.4692.71 and https://ccrev.com/c/3262916 shipped in 98.0.4758.81, I would consider this as fixed in Release-0-M98.

Over to pgrace@ for CVE issuance -- can you please assign a CVE and make sure it can get included in the sweep-up process? Thank you!



### am...@chromium.org (2022-11-16)

pgrace@ - forgot to cc: you, please see comment above 

### pg...@google.com (2022-11-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-29)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-03)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1260250?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1266157]
[Monorail mergedinto: crbug.com/chromium/1266157]
[Monorail components added to Component Tags custom field.]

### ch...@google.com (2025-10-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057616)*
