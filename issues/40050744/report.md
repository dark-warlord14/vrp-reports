# Security: Steal any local picture when open a local html file

| Field | Value |
|-------|-------|
| **Issue ID** | [40050744](https://issues.chromium.org/issues/40050744) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Loader, Blink>SecurityFeature, Blink>SecurityFeature>CORS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ti...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2019-11-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When open a local evil .html file(file://pic\_path), the local picture can be sent to an evil server.

In the stable version,the picture form the file:// domain treats as a tainted canvases.So it causes a console error : "Uncaught DOMException: Failed to execute 'toDataURL' on 'HTMLCanvasElement': Tainted canvases may not be exported."

However, in the latest dev version, the picture from the file domain can be exported with 'toDataURL'. As a result, the base64 code of this picture can be sent to a evil server.

**VERSION**  

Chrome Version: Version 80.0.3973.0 (Developer Build) (64-bit)  

Operating System: [Windows10 1909]

Test version:  

{  

"kind": "storage#object",  

"name": "win32-release\_x64/asan-win32-release\_x64-716878.zip",  

"size": "1539163928",  

"mediaLink": "<https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-716878.zip?generation=1574231960381428&alt=media>",  

"metadata": {  

"cr-commit-position": "refs/heads/master@{#716878}",  

"cr-commit-position-number": "716878",  

"cr-git-commit": "763b7d5ba7a01435a06eeccf40ff3692ff534471"  

},  

"updated": "2019-11-20T06:39:20.381Z"  

}

**REPRODUCTION CASE**

1. Open the server.py with python3. This evil server is used to receive the picture.
2. set the an existing picture path in the poc.html
3. Open the poc.html(file:/path/poc.html) with the latest dev chromium.

The picture will be sent to the evil server.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [server.py](attachments/server.py) (text/plain, 1.6 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### me...@chromium.org (2019-11-20)

Nice find! Bisected to https://chromium.googlesource.com/chromium/src/+log/b92cf6e2a7fd37968ef74f9da653c8bd777b0857..09829acab669a60ebb3a7c403a0b442eac451dc2

The only relevant looking CL in the range is https://chromium-review.googlesource.com/c/chromium/src/+/1882770

toyoshim: PTAL? I know your change is only a testing config, but there isn't anything else in the bisect range.

This also seems to be low severity, given that it only allows reading file URL to file URL. 

[Monorail components: Blink>SecurityFeature]

### ti...@gmail.com (2019-11-21)

I write an exploit to steal the chromium cache in Windows10.

### to...@chromium.org (2019-11-21)

This problem seems to happen when OOR-CORS is enabled.
So the bisect result was correct, maybe it uses the testing config rather than server distributed random config to make the bisect reliable?

OOR-CORS is planned to be launched at m79, and I confirmed that the issue is reproducible on current Chrome 79 beta with chrome://flags/#out-of-blink-cors Enabled.

meacer: You said the severity is low, but do you think this is a stable blocker?

[Monorail components: Blink>Loader Blink>SecurityFeature>CORS]

### to...@chromium.org (2019-11-21)

Just in case, the issue is reproducible even on Chrome 78 stable with OOR-CORS Enabled. But it's disabled by default. IIRC, 0.00006% users manually enable it.

### to...@chromium.org (2019-11-21)

getImageData() also returns bitmap data without throwing an exception if OOR-CORS is enabled.
This issue happens only when file:/// is accessed from file:///.
http(s):// accesses from file:/// are correctly tainted.

### to...@chromium.org (2019-11-21)

[Empty comment from Monorail migration]

### to...@chromium.org (2019-11-21)

The fix is almost ready; https://chromium-review.googlesource.com/c/chromium/src/+/1928606

Does anyone know if I can write a WPT that expects loading via file:// scheme to test this case.
I know LayoutTests can do it, but haven't wrote such tests in WPT.

### ki...@chromium.org (2019-11-21)

I don't recall there was a way to test file:// in WPT... unless something has been changed recently.

### yh...@chromium.org (2019-11-21)

IIUC it is not specified: https://fetch.spec.whatwg.org/#scheme-fetch

### to...@chromium.org (2019-11-21)

yep, I also noticed that the spec does not say anything on file://. so, we won't have the test in WPT regardless of possibility to write such tests.
I will write a layout test maybe in web_tests/fast/canvas/. there, we have similar tests for svg, but we need similar ones for gif or png.

### sh...@chromium.org (2019-11-21)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2019-11-26)

> meacer: You said the severity is low, but do you think this is a stable blocker?

I don't think it is, given that it's low severity bug, but then again, we can re-evaluate whether its medium.

### me...@chromium.org (2019-11-26)

Changing to impact-beta since the plan is to ship the feature in M79.

### yh...@chromium.org (2019-11-28)

Isn't this a severe problem?  IIUC this bugs gives an ability to read local file contents to malicious web developers.

### yh...@chromium.org (2019-11-28)

Ah, sorry, I misunderstood #1.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/69901e65bfea41eab02a3c0e947d076920f3494f

commit 69901e65bfea41eab02a3c0e947d076920f3494f
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date: Wed Dec 11 10:19:30 2019

OOR-CORS: Set FetchResponseType in FileURLLoader

Once OOR-CORS is enabled, Blink does not apply a file scheme
specific check for the canvas taint, and FileURLLoader should
set the correct FetchResponseType based on the request mode.

Change-Id: Ie0334d97db6e21b9f4e70c8787f3dc2c4ea1f89f
Bug: 1026546
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1928606
Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Auto-Submit: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#723762}

[modify] https://crrev.com/69901e65bfea41eab02a3c0e947d076920f3494f/content/browser/loader/cors_file_origin_browsertest.cc
[modify] https://crrev.com/69901e65bfea41eab02a3c0e947d076920f3494f/content/browser/loader/file_url_loader_factory.cc
[modify] https://crrev.com/69901e65bfea41eab02a3c0e947d076920f3494f/content/browser/loader/file_url_loader_factory.h
[add] https://crrev.com/69901e65bfea41eab02a3c0e947d076920f3494f/content/test/data/loader/image-taint.html


### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### ti...@gmail.com (2019-12-12)

Hi,
Is it a low severity bug because of the small range of influence？

All the IM app don't think the html file is a dangerous file. So it is can easily sent to other through various channels.
If the chrome is the default browser, we can steal any picture in any folder(IM chat log folder/chrome cache...).

So I think it's very easy to use, and it has relatively high level of threat.


### to...@chromium.org (2019-12-12)

OOR-CORS is not enabled on the stable, and will be incrementally rolled out.
When 100% users get the feature enabled, the next major update for 80 will happen in a few days.

I will merge this fix to m80.

### sh...@chromium.org (2019-12-12)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-13)

Your change meets the bar and is auto-approved for M80. Please go ahead and merge the CL to branch 3987 (refs/branch-heads/3987) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-13)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-12-13)

Please merge your change to M80 branch 3987 ASAP so we can pick it up for next week beta release. Thank you.

### go...@chromium.org (2019-12-15)

Requesting to merge to M80 branch 3987 ASAP. Please use branch CQ for merge. Thank you.

### na...@google.com (2019-12-16)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-12-16)

Requesting to merge to M80 branch 3987 ASAP. Please use branch CQ for merge. Thank you.

Note: We're cutting M80 Beta RC soon for release this week. 

### sr...@google.com (2019-12-16)

Please get your merges complete to M80 branch asap. I am cutting beta/dev RC today by 5:00 PM PST so would like to include these merges in build before holidays

### to...@chromium.org (2019-12-17)

now it's in CQ: https://chromium-review.googlesource.com/c/chromium/src/+/1971172
thanks!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/887220f4d4e777dc40904d97880c3eea41564ecb

commit 887220f4d4e777dc40904d97880c3eea41564ecb
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date: Tue Dec 17 06:17:34 2019

OOR-CORS: Set FetchResponseType in FileURLLoader

Once OOR-CORS is enabled, Blink does not apply a file scheme
specific check for the canvas taint, and FileURLLoader should
set the correct FetchResponseType based on the request mode.

(cherry picked from commit 69901e65bfea41eab02a3c0e947d076920f3494f)

Change-Id: Ie0334d97db6e21b9f4e70c8787f3dc2c4ea1f89f
Bug: 1026546
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1928606
Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Auto-Submit: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#723762}
TBR: yhirano@chromium.org
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1971172
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#196}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/887220f4d4e777dc40904d97880c3eea41564ecb/content/browser/loader/cors_file_origin_browsertest.cc
[modify] https://crrev.com/887220f4d4e777dc40904d97880c3eea41564ecb/content/browser/loader/file_url_loader_factory.cc
[modify] https://crrev.com/887220f4d4e777dc40904d97880c3eea41564ecb/content/browser/loader/file_url_loader_factory.h
[add] https://crrev.com/887220f4d4e777dc40904d97880c3eea41564ecb/content/test/data/loader/image-taint.html


### na...@google.com (2019-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-19)

Congrats! The Panel decided to reward $1,000 for this report!

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e93b5dc01f1fcc6ef4efd0880a8cf60abdd23a42

commit e93b5dc01f1fcc6ef4efd0880a8cf60abdd23a42
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Tue Dec 24 09:28:16 2019

Use FetchResponseType::kBasic in content::CreateFileURLLoader

The header comment is saying "this does not restrict filesystem access
*in any way*", so bypassing CORS is the expected behavior.

Bug: 1035575, 1036693,1026546
Change-Id: I1af6a25c9865d8c1f5f367db2ff277a9f5c101ac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1980649
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Auto-Submit: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#727362}

[modify] https://crrev.com/e93b5dc01f1fcc6ef4efd0880a8cf60abdd23a42/content/browser/loader/file_url_loader_factory.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/30e09ff259a285fe0722222d3c4417ab70f66d0f

commit 30e09ff259a285fe0722222d3c4417ab70f66d0f
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Sat Jan 04 01:55:27 2020

Use FetchResponseType::kBasic in content::CreateFileURLLoader

The header comment is saying "this does not restrict filesystem access
*in any way*", so bypassing CORS is the expected behavior.

(cherry picked from commit e93b5dc01f1fcc6ef4efd0880a8cf60abdd23a42)

Bug: 1035575, 1036693,1026546
Change-Id: I1af6a25c9865d8c1f5f367db2ff277a9f5c101ac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1980649
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Auto-Submit: Yutaka Hirano <yhirano@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#727362}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1985834
Reviewed-by: Shik Chen <shik@chromium.org>
Reviewed-by: Charlie Harrison <csharrison@chromium.org>
Commit-Queue: Shik Chen <shik@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#404}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/30e09ff259a285fe0722222d3c4417ab70f66d0f/content/browser/loader/file_url_loader_factory.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/df83dca40fb3006fddb4a81574b2b3f9fae988b1

commit df83dca40fb3006fddb4a81574b2b3f9fae988b1
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Tue Jan 07 06:24:55 2020

Add "BypassSecurityChecks" suffix to content::CreateFileURLLoader

According to the comment "this does not restrict filesystem access
*in any way*", so make it look dangerous.

Bug: 1035575, 1036693,1026546
Change-Id: Iadd64b3b1be417b469b8d85144de21c86f67ceba
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1981414
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Ken Rockot <rockot@google.com>
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#728817}

[modify] https://crrev.com/df83dca40fb3006fddb4a81574b2b3f9fae988b1/chrome/browser/chrome_content_browser_client.cc
[modify] https://crrev.com/df83dca40fb3006fddb4a81574b2b3f9fae988b1/content/browser/loader/file_url_loader_factory.cc
[modify] https://crrev.com/df83dca40fb3006fddb4a81574b2b3f9fae988b1/content/public/browser/file_url_loader.h
[modify] https://crrev.com/df83dca40fb3006fddb4a81574b2b3f9fae988b1/extensions/browser/extension_protocols.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5a6058700ef20b5fc8b4e69b7684af0b0bc07128

commit 5a6058700ef20b5fc8b4e69b7684af0b0bc07128
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Wed Jan 08 05:09:07 2020

Add a test for response type for extension resources

This is a regression test for https://crrev.com/c/1980649. Resources
contained in an extension should be accessible from the extension's
background page.

Bug: 1035575, 1036693,1026546
Change-Id: Ic08cec5d526cc5594a6bf507deca43c96d6258f2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1981419
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#729233}

[modify] https://crrev.com/5a6058700ef20b5fc8b4e69b7684af0b0bc07128/chrome/browser/extensions/fetch_apitest.cc


### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-03-19)

This issue was migrated from crbug.com/chromium/1026546?no_tracker_redirect=1

[Multiple monorail components: Blink>Loader, Blink>SecurityFeature, Blink>SecurityFeature>CORS]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050744)*
