# use-after-poison in  operator-> (from HTMLImportsController::Dispose)

| Field | Value |
|-------|-------|
| **Issue ID** | [40091383](https://issues.chromium.org/issues/40091383) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>GarbageCollection, Blink>HTML>Modules |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2018-05-15 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36

Steps to reproduce the problem:
1.Get new version chrome:
 a) Build source code 
    config args.gn file as below:
		use_sanitizer_coverage = true
		is_asan = true
		is_debug = false
		enable_nacl = false
		treat_warnings_as_errors = false
	ninja -j16 -C out/chrome_asan chrome
2.python3.5m -m http.server 8605
3.  ./crhome --no-sandbox --no-zygote launcher.html

4. Get UAP in 30 seconds, occasionally get UAF or sig11 0x28.
Because UAF and sig11 are not stable, I only got the UAP symbolized log.

What is the expected behavior?

What went wrong?
launcher.html:(Depending on system performance, you may need to adjust the time.)
<script>
function test(){
 window.opener = null;
 myWindow = window.open("/poc.html",'','width=500,height=500') 
 setTimeout(function(){myWindow.close()} ,500);
}
test();
setInterval(function(){test()} ,600);
</script>

poc.html:
<object data="/res/1.pdf" type="application/pdf" width="300" height="200">
  alt : <a href="/res/1.pdf">x</a>
</object>
<object type="image/svg+xml" data="/res/1.svg" width="320" height="240">
  <param name="src" value="/res/1.svg">
  alt : <a href="/res/1.svg">x</a>
</object>
<object data="/res/1.html" type="application/html" width="300" height="200">
  alt : <a href="/res/1.html">x</a>
</object>
<object data="/res/1.css" type="application/css" width="300" height="/res/1.webm">
  alt : <a href="/res/1.css">x</a>
</object>

Did this work before? N/A 

Chrome version: Version 68.0.3430.0 (Developer Build) (64-bit)  Channel: dev
OS Version: Ubuntu 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [launcher.html](attachments/launcher.html) (text/plain, 223 B)
- [poc1.html](attachments/poc1.html) (text/plain, 816 B)
- [poc2.html](attachments/poc2.html) (text/plain, 3.4 KB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 6.0 MB)
- [launcher.html](attachments/launcher_53384809.html) (text/plain, 381 B)

## Timeline

### me...@chromium.org (2018-05-15)

I wasn't able to reproduce this in about 10 minutes of testing on trunk.
Labeling Medium Severity for now since the bug seems hard to trigger. cdsrc2016: do you have a more deterministic POC?

yhirano@ Could you please take a look if there is anything actionable here? 
Please let me know if you aren't the right owner for this.

[Monorail components: Blink]

### rb...@chromium.org (2018-05-15)

Crash appears to be in blink::HTMLImportsController::Dispose

Adding Blink>HTML>Modules and cc tyoshino who seems to have made the most interesting changes to that code.

[Monorail components: -Blink Blink>HTML>Modules]

### cd...@gmail.com (2018-05-16)

repro do not need to wait 10 minutes, 1 minute is enough. If you do not see a crash before 1 min or 30 tabs are created, reopen the browser.
Or according to the system performance can adjust this time (490 ms in my code). System performance is high, time can be reduced, system performance is low, and time is increased.

I made a small change to launcher and poc. Poc1.html is the minimised code, poc2.html is the original file. And I also attached my repro video.
Thank you~~~^-^


### cd...@gmail.com (2018-05-16)

found that repro does not require any options, just run ./chrome.

### sh...@chromium.org (2018-05-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-16)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-05-16)

I couldn't repro the UAP on 66 but I did repro it on trunk with the latest POC.

### yh...@chromium.org (2018-05-17)

I cannot produce the issue. Are you setting any environment variables such as ASAN_OPTIONS?

### cd...@gmail.com (2018-05-17)

My ASAN_OPTIONS setting is null.
--;
Please see https://crbug.com/chromium/843151#c3.




### yh...@chromium.org (2018-05-17)

According to the attached asan.log, it seems use-after-poison in HTMLImportsController::Dispose. It's strange that the function is simply calling a function for all objects in a heap vector. keishi@, can you take a look?

[Monorail components: Blink>MemoryAllocator>GarbageCollection]

### mm...@chromium.org (2018-05-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-30)

keishi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2018-06-15)

I can't reproduce this on either trunk or 3430 branch. I've tried lots of different timeouts. I think we're going to need a more reliable repro.

OP: can you try and repro on latest trunk build?

### sh...@chromium.org (2018-06-20)

keishi: Uh oh! This issue still open and hasn't been updated in the last 35 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-07-03)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-07-24)

I can still repro this UAP by different pocs,they have the same stack trace.

And i tried on new version 69.0.3494.0 again,can still repro.But it is not stable, either.
Could you please try this "launcher.html" and adjust the number of child window and the timeout to make it more stable? 

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-08-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-08-22)

ClusterFuzz testcase 4547954741084160 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-08-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2018-09-12)

This bug is unreproducible, but still happening. See crash stats on https://clusterfuzz.com/v2/testcase-detail/4547954741084160?noredirect=1 for 90 days window, last happened on Sep 4. We should try to fix based on free stack. Reopening.

### sh...@chromium.org (2018-09-13)

[Empty comment from Monorail migration]

### tk...@chromium.org (2018-09-26)

[Empty comment from Monorail migration]

### tk...@chromium.org (2018-09-26)

I don't understand the root cause, but try to add a workaround.

UAP on Oilpan heap isn't vulnerable in production, right?


### bu...@chromium.org (2018-09-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/54139dd9a60d8fb63d2379a08e2f2750eac2d959

commit 54139dd9a60d8fb63d2379a08e2f2750eac2d959
Author: Kent Tamura <tkent@chromium.org>
Date: Wed Sep 26 05:14:03 2018

Speculative fix for crashes in HTMLImportsController::Dispose().

Copy the loaders_ vector before iterating it.
This CL has no tests because we don't know stable reproduction.

Bug: 843151
Change-Id: I3d5e184657cbce56dcfca0c717d7a0c464e20efe
Reviewed-on: https://chromium-review.googlesource.com/1245017
Reviewed-by: Keishi Hattori <keishi@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/master@{#594226}
[modify] https://crrev.com/54139dd9a60d8fb63d2379a08e2f2750eac2d959/third_party/blink/renderer/core/html/imports/html_imports_controller.cc


### tk...@chromium.org (2018-09-26)

Let's check whether the number of crashes decreases or not later.

Crash summary link: https://crash.corp.google.com/browse?q=EXISTS+%28SELECT+1+FROM+UNNEST%28CrashedStackTrace.StackFrame%29+WHERE+FunctionName%3D%27blink%3A%3AHTMLImportLoader%3A%3ADispose%28%29%27%29#samplereports


### tk...@chromium.org (2018-10-05)

It seems the CL fixed the issue.  The first canary release with the CL is 71.0.3563.0, and crashes have never been reported since 71.0.3563.0.  The Dev release of this week, 71.0.3569.0, also reports no crashes.


### sh...@chromium.org (2018-10-05)

This bug requires manual review: We are only 10 days from stable.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-10-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ee6aa91dfb94d774b4cf117f35d748c78f08936f

commit ee6aa91dfb94d774b4cf117f35d748c78f08936f
Author: Kent Tamura <tkent@chromium.org>
Date: Tue Oct 09 01:29:56 2018

Merge "Speculative fix for crashes in HTMLImportsController::Dispose()." to M70 branch

Copy the loaders_ vector before iterating it.
This CL has no tests because we don't know stable reproduction.

Bug: 843151
Change-Id: I3d5e184657cbce56dcfca0c717d7a0c464e20efe
Reviewed-on: https://chromium-review.googlesource.com/1245017
Reviewed-by: Keishi Hattori <keishi@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#594226}(cherry picked from commit 54139dd9a60d8fb63d2379a08e2f2750eac2d959)
Reviewed-on: https://chromium-review.googlesource.com/c/1270199
Reviewed-by: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/branch-heads/3538@{#911}
Cr-Branched-From: 79f7c91a2b2a2932cd447fa6f865cb6662fa8fa6-refs/heads/master@{#587811}
[modify] https://crrev.com/ee6aa91dfb94d774b4cf117f35d748c78f08936f/third_party/blink/renderer/core/html/imports/html_imports_controller.cc


### cr...@appspot.gserviceaccount.com (2018-10-09)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/ee6aa91dfb94d774b4cf117f35d748c78f08936f

Commit: ee6aa91dfb94d774b4cf117f35d748c78f08936f
Author: tkent@chromium.org
Commiter: tkent@chromium.org
Date: 2018-10-09 01:29:56 +0000 UTC

Merge "Speculative fix for crashes in HTMLImportsController::Dispose()." to M70 branch

Copy the loaders_ vector before iterating it.
This CL has no tests because we don't know stable reproduction.

Bug: 843151
Change-Id: I3d5e184657cbce56dcfca0c717d7a0c464e20efe
Reviewed-on: https://chromium-review.googlesource.com/1245017
Reviewed-by: Keishi Hattori <keishi@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#594226}(cherry picked from commit 54139dd9a60d8fb63d2379a08e2f2750eac2d959)
Reviewed-on: https://chromium-review.googlesource.com/c/1270199
Reviewed-by: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/branch-heads/3538@{#911}
Cr-Branched-From: 79f7c91a2b2a2932cd447fa6f865cb6662fa8fa6-refs/heads/master@{#587811}

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-10-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-10-15)

Thanks for the report! The VRP panel decided to award $500. Cheers!

### aw...@chromium.org (2018-10-15)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-10-16)

Hi ~ Thanks for the reward!

### aw...@chromium.org (2018-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/843151?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GarbageCollection, Blink>HTML>Modules]
[Monorail mergedwith: crbug.com/chromium/876249, crbug.com/chromium/883279]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091383)*
