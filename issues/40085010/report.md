# cross-origin restriction bypass in track tag src

| Field | Value |
|-------|-------|
| **Issue ID** | [40085010](https://issues.chromium.org/issues/40085010) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>Track |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2016-08-03 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7

Steps to reproduce the problem:
1. At first the expected behavior here is as the following URL.
http://adlabtest.applinzi.com/test7.html

This document tries to load a cross-origin font like this.
<track src="http://zih.pub/subtitles.vtt" kind="subtitles" srclang="en" label="English" />   But the loading error is shown on the console because the track doesn't send an Access-Control-Allow-Origin header.
2.But the flaw I found is the following.
http://adlabtest.applinzi.com/test8.html
This video also loads same subtitle as 1) but it's through 302 redirector like this.
<track src="http://adlabtest.applinzi.com/redirct2.php" kind="subtitles" srclang="en" label="English" /> 

What is the expected behavior?

What went wrong?
bypass same-origin 

Did this work before? N/A 

Chrome version: Chrome 52.0.2743.82  Channel: stable
OS Version: 10
Flash Version: 

I found that  the request of loading subtitle(webVTT)  was made with no-cors mode when the URL of Loading subtitle was same-origin. However, that same-origin request may be redirected to another origin.
I test this vulnerability on Chrome 52.0.2743.82 m ( win10) It will be success

Test site:
http://adlabtest.applinzi.com/test8.html

step1:
At first the expected behavior here is as the following URL.
http://adlabtest.applinzi.com/test7.html

This document tries to load a cross-origin font like this.
<track src="http://zih.pub/subtitles.vtt" kind="subtitles" srclang="en" label="English" />   But the loading error is shown on the console because the track doesn't send an Access-Control-Allow-Origin header.

Setp2:
But the flaw I found is the following.
http://adlabtest.applinzi.com/test8.html
This video also loads same subtitle as 1) but it's through 302 redirector like this.
<track src="http://adlabtest.applinzi.com/redirct2.php" kind="subtitles" srclang="en" label="English" />  

redirct2.php:
<?php
header("Location: http://zih.pub/subtitles.vtt");
?>
By the way, you should open the switch of subtitles

Then, the subtitle can be loaded with bypassing CORS restriction and the track is successfully applied to the video.

Author : Haojun Hou and Shenrong Liu in ADLab of Venustech.
Could you please help me assign a CVE for this issue?

## Timeline

### ra...@chromium.org (2016-08-04)

japhet could please take a look at this?

I'm not quite sure the security implications of this because it seems similar to embedding static cross-origin content. lgarron: do you have any ideas?

[Monorail components: Blink>Media>Track]

### sh...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-05)

[Empty comment from Monorail migration]

### ha...@gmail.com (2016-08-14)

Excuse me, when this bug will be assigned a CVE number ? or could you please give me a rough idea what time ?

### yi...@chromium.org (2016-08-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-17)

japhet: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2016-08-21)

Sorry,could I know the latest developments about this vulnerability ?

### ha...@gmail.com (2016-08-23)

@sheriffbot@chromium.org, hi, could I know the latest developments about this vulnerability ? For example,is there a CVE for it?

### sh...@chromium.org (2016-09-01)

japhet: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2016-09-06)

Hi,it has been more than one month since I report this vulnerability,please let me konw the latest developments about it. 
I will be looking forward to your reply.

### ha...@gmail.com (2016-09-08)

Hi,it has been more than one month since I report this vulnerability,please let me konw the latest developments about it. 
I will be looking forward to your reply.

### ha...@gmail.com (2016-09-12)

Does anyone reply to me？

### ha...@gmail.com (2016-09-18)

Hi,it has been more than one month since I report this vulnerability,please let me konw the latest developments about it. 
I will be looking forward to your reply,please.

### el...@chromium.org (2016-09-21)

#14: Thanks for your report. We're still looking at this; it appears that the Track element behavior does not match the spec and is both too restrictive (https://crbug.com/chromium/472300) and not restrictive enough (this issue).

It's less clear how useful this vector is to an attacker and whether it leaks any unique cross-origin information to the requesting page.

### el...@chromium.org (2016-09-21)

In terms of exploitability, it turns out that JavaScript /can/ read the cue text using <trackId>.track.cues[i].getCueAsHTML() which means this does offer a cross-origin read in violation of CORS. Exploitability appears to be limited, however, as the parser for WebVTT requires those characters appear atop the file ( https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/html/track/vtt/VTTParser.cpp?sq=package:chromium&dr=CSs&rcl=1474471143&l=130 ), which would mean that the attacker would need to attack e.g. a vulnerable JSONP endpoint to get these characters at the top of the target resource he was trying to steal.

The original repro site is down, so I've posted one here:

https://whytls.com/test/crossorigin/index.html
https://whytls.com/test/crossorigin/index-302.html

In Chrome 55.2867, the direct cross-origin reference shows the error message "Text track from origin 'https://www.whytls.com' has been blocked from loading: Not at same origin as the document, and parent of track element does not have a 'crossorigin' attribute. Origin 'https://whytls.com' is therefore not allowed access." and captions are not shown. In contrast, the redirected cross-origin reference yields no console message and the captions are loaded.

In Firefox 52.0a1, captions load when directly referenced across origin. When referenced indirectly via the same-origin URL that returns a cross-origin HTTP/302, Firefox does not follow the redirect and does not display the caption; there is no console warning.

In Internet Explorer 11, captions load only when same-origin; direct cross-origin references are ignored, and indirect references result in following the 302 and then ignoring the resulting download; no console error is shown.

Debuggers looking to step through this can walk through TextTrackLoader::load(const KURL& url, CrossOriginAttributeValue crossOrigin)



### bu...@chromium.org (2016-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e99cc8e5a48ff4978d401c48a64f06649f647f3f

commit e99cc8e5a48ff4978d401c48a64f06649f647f3f
Author: japhet <japhet@chromium.org>
Date: Thu Sep 29 20:21:38 2016

Check CORS policy on redirect in TextTrackLoader

BUG=633885
TEST=new case in http/tests/security/text-track-crossorigin.html

Review-Url: https://codereview.chromium.org/2367583002
Cr-Commit-Position: refs/heads/master@{#421919}

[modify] https://crrev.com/e99cc8e5a48ff4978d401c48a64f06649f647f3f/third_party/WebKit/LayoutTests/http/tests/security/text-track-crossorigin-expected.txt
[modify] https://crrev.com/e99cc8e5a48ff4978d401c48a64f06649f647f3f/third_party/WebKit/LayoutTests/http/tests/security/text-track-crossorigin.html
[modify] https://crrev.com/e99cc8e5a48ff4978d401c48a64f06649f647f3f/third_party/WebKit/Source/core/loader/TextTrackLoader.cpp
[modify] https://crrev.com/e99cc8e5a48ff4978d401c48a64f06649f647f3f/third_party/WebKit/Source/core/loader/TextTrackLoader.h


### aw...@google.com (2016-10-04)

Hello!  Any more changes expected for this, or can we move it to Fixed?  Cheers.

### ja...@chromium.org (2016-10-04)

Do we want this for M54?

### di...@chromium.org (2016-10-04)

[Automated comment] Less than 2 weeks to go before stable on M54, manual review required.

### bu...@google.com (2016-10-04)

I'd like to take for M54, since it's a security fix.

### sh...@chromium.org (2016-10-05)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bb0c78373eba2faf792c9548fe2e939f4ca8b3ff

commit bb0c78373eba2faf792c9548fe2e939f4ca8b3ff
Author: Nate Chapin <japhet@chromium.org>
Date: Wed Oct 05 18:50:46 2016

Check CORS policy on redirect in TextTrackLoader

BUG=633885
TEST=new case in http/tests/security/text-track-crossorigin.html

Review-Url: https://codereview.chromium.org/2367583002
Cr-Commit-Position: refs/heads/master@{#421919}
(cherry picked from commit e99cc8e5a48ff4978d401c48a64f06649f647f3f)

Review URL: https://codereview.chromium.org/2400433002 .

Cr-Commit-Position: refs/branch-heads/2840@{#650}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/bb0c78373eba2faf792c9548fe2e939f4ca8b3ff/third_party/WebKit/LayoutTests/http/tests/security/text-track-crossorigin-expected.txt
[modify] https://crrev.com/bb0c78373eba2faf792c9548fe2e939f4ca8b3ff/third_party/WebKit/LayoutTests/http/tests/security/text-track-crossorigin.html
[modify] https://crrev.com/bb0c78373eba2faf792c9548fe2e939f4ca8b3ff/third_party/WebKit/Source/core/loader/TextTrackLoader.cpp
[modify] https://crrev.com/bb0c78373eba2faf792c9548fe2e939f4ca8b3ff/third_party/WebKit/Source/core/loader/TextTrackLoader.h


### sh...@chromium.org (2016-10-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

Congratulations! The panel decided to award $1,000 for the bug, noting the mitigations mentioned in https://crbug.com/chromium/633885#c16.  A member of our finance team will be in touch shortly.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### ha...@gmail.com (2016-10-17)

hi,I have two questions, first , How do I get a reward? Second, is there no description like "HaojunHou in ADLab of Venustech" in your vulnerability publication?
I will be looking forward to your reply.

### ha...@gmail.com (2016-10-17)

Hi,in the first time I reported this vulnerability , information about Author like "Haojun Hou in ADLab of Venustech" in it , but I check your vulnerability information publication , these information did not be present.

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bb0c78373eba2faf792c9548fe2e939f4ca8b3ff

commit bb0c78373eba2faf792c9548fe2e939f4ca8b3ff
Author: Nate Chapin <japhet@chromium.org>
Date: Wed Oct 05 18:50:46 2016

Check CORS policy on redirect in TextTrackLoader

BUG=633885
TEST=new case in http/tests/security/text-track-crossorigin.html

Review-Url: https://codereview.chromium.org/2367583002
Cr-Commit-Position: refs/heads/master@{#421919}
(cherry picked from commit e99cc8e5a48ff4978d401c48a64f06649f647f3f)

Review URL: https://codereview.chromium.org/2400433002 .

Cr-Commit-Position: refs/branch-heads/2840@{#650}
Cr-Branched-From: 1ae106dbab4bddd85132d5b75c670794311f4c57-refs/heads/master@{#414607}

[modify] https://crrev.com/bb0c78373eba2faf792c9548fe2e939f4ca8b3ff/third_party/WebKit/LayoutTests/http/tests/security/text-track-crossorigin-expected.txt
[modify] https://crrev.com/bb0c78373eba2faf792c9548fe2e939f4ca8b3ff/third_party/WebKit/LayoutTests/http/tests/security/text-track-crossorigin.html
[modify] https://crrev.com/bb0c78373eba2faf792c9548fe2e939f4ca8b3ff/third_party/WebKit/Source/core/loader/TextTrackLoader.cpp
[modify] https://crrev.com/bb0c78373eba2faf792c9548fe2e939f4ca8b3ff/third_party/WebKit/Source/core/loader/TextTrackLoader.h


### ha...@gmail.com (2016-11-01)

Hi,in the first time I reported this vulnerability , information about Author like "Haojun Hou in ADLab of Venustech" in it , but I check your vulnerability information publication , these information did not be present.
I will be looking forward to your reply.

### ha...@gmail.com (2016-11-21)

Hello, how can I get the reward? 

### aw...@google.com (2016-12-10)

Hello Haojun!  The advisory went live a while ago (https://googlechromereleases.blogspot.com/2016/10/stable-channel-update-for-desktop.html) but it looks like we ended up just using your email address. Sorry about that.  Would you like us to update it with the text you gave in #35?

I shall follow up on #36 via email.

### ha...@gmail.com (2016-12-10)

Ok,thanks.By the way, I have a question, how can I get the reward $1,000 for the bug ?

### sh...@chromium.org (2017-01-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/633885?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085010)*
