# heap use-after-free in link::VideoFrameSubmitter::~VideoFrameSubmitter()

| Field | Value |
|-------|-------|
| **Issue ID** | [40091440](https://issues.chromium.org/issues/40091440) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Paint |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2018-05-21 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36

Steps to reproduce the problem:
1. Build source code 
    config args.gn file as below:
		use_sanitizer_coverage = true
		is_asan = true
		is_debug = false
		enable_nacl = false
		treat_warnings_as_errors = false
	ninja -j4 -C out/chrome_asan chrome
2. Build a mini web server.
	I used python twisted module to build the webserver.
	1) cp 1.ogg(OR any other normal ogg file) to webserver/res/
	2) python webserver/web.py
3. ./chrome --no-sandbox http://127.0.0.1:8605/launcher.html
4. wait for about 0.5-1 minites and the number of child window is above 30 (not sure the exact figures)
5. close the browser

What is the expected behavior?

What went wrong?
When close the browser,a UAF crash happened.

With two different chrome version,we both got the UAF crash.
But the stacktrace is different.
The first one is in :68.0.3430.0 (Developer Build) (64-bit).
The second one is in:68.0.3429.0 (Developer Build) (64-bit).
And the stacktrace see the first_log.txt and second_log.txt

Did this work before? N/A 

Chrome version: 68.0.3429.0  Channel: n/a
OS Version: 16.04
Flash Version: 

1.Could stably get crash in 68.0.3429.0,occasionally in another.
2.the webserver and res see webserver.zip.

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [845136.zip](attachments/845136.zip) (application/octet-stream, 782.7 KB)

## Timeline

### cl...@chromium.org (2018-05-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4723698452660224.

### cl...@chromium.org (2018-05-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6178657681539072.

### mm...@chromium.org (2018-05-21)

I can't reproduce this locally. Will give another try on CF, but I'm skeptical about that You mention 1.ogg file, but I don't see it referenced in any of the HTML files you provided.

Also, Chrome blocks pop up windows by default, i.e. it doesn't open poc.html tabs for me until I allow it to do so.

Could you please double check whether the reproducer you've provided works? Also, would it be possible to remove user interaction (allow pop-ups) and make it more stable overall?

### cl...@chromium.org (2018-05-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5518790314688512.

### cl...@chromium.org (2018-05-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4915785496264704.

### cd...@gmail.com (2018-05-22)

Sorry for my mistake.Step 1 that mention 1.ogg file is a writing error，there is no need for 1.ogg and we should delete that step.

About the user interaction, used to make more windows, is not the import part of the crash.If the detail of crash is understood,maybe it can be removed.

How about try this args for chrome ?
"--no-sandbox --no-zygote  --incognito --expose-wasm --disable-translate --no-process-singleton-dialog --no-default-browser-check --no-first-run --new-window  --allow-file-access-from-files http://127.0.0.1:8605/launcher.html"

It's the args when crash first happen.(But in my OS,only "--no-sandbox" also works.)

Sorry for my mistake again and other repreoducer is OK.

### sh...@chromium.org (2018-05-22)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-05-30)

Max, are you able to repro using the flags in https://crbug.com/chromium/845136#c6?

### mm...@chromium.org (2018-05-31)

Nope. Just tried again using https://storage.cloud.google.com/chromium-browser-asan/linux-release/asan-linux-release-563379.zip and no luck

The best I've got was OOM, which is quite funny, given the amount of RAM I have.




### me...@chromium.org (2018-05-31)

Thanks Max. 

lethalantidote: Would you be able to take a look at this one? It looks Blink>Paint related but please reassign if that's not correct. Thanks.

[Monorail components: Blink>Paint]

### sc...@chromium.org (2018-06-01)

This is the destructor code so presumably the context_provider has been freed when this destructor is called.

VideoFrameSubmitter::~VideoFrameSubmitter() {
  if (context_provider_)
    context_provider_->RemoveObserver(this);
}

### me...@chromium.org (2018-06-01)

Looks like this changed in https://chromium.googlesource.com/chromium/src/+/df92bfed734a92c8f839af121218917ae599157d



### le...@chromium.org (2018-06-02)

So the first crash log looks like it is referring to a bug that already has a fix landed. As for the second crash log, I am looking into it. 

### le...@chromium.org (2018-06-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-06-02)

[Empty comment from Monorail migration]

### le...@chromium.org (2018-06-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-06-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8

commit 2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8
Author: CJ DiMeglio <lethalantidote@chromium.org>
Date: Tue Jun 12 21:13:26 2018

Makes VideoFrameSubmitter's ptr to context_provider scoped_refptr.

This CL prevents VideoFrameSubmitter from accessing a bare ptr of
|context_provider_| after it has been deleted by changing ptr to be a
scoped_refptr.

Bug: 845136
Cq-Include-Trybots: luci.chromium.try:linux_layout_tests_slimming_paint_v2;master.tryserver.blink:linux_trusty_blink_rel;master.tryserver.chromium.linux:linux_layout_tests_slimming_paint_v2
Change-Id: Ia574a206519857ddb4169aaec281b64e3689e8ce
Reviewed-on: https://chromium-review.googlesource.com/1087514
Commit-Queue: CJ DiMeglio <lethalantidote@chromium.org>
Reviewed-by: Justin Novosad <junov@chromium.org>
Reviewed-by: Frank Liberato <liberato@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Sadrul Chowdhury <sadrul@chromium.org>
Cr-Commit-Position: refs/heads/master@{#566570}
[modify] https://crrev.com/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8/content/renderer/media/gpu/gpu_video_accelerator_factories_impl.cc
[modify] https://crrev.com/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8/content/renderer/media/gpu/gpu_video_accelerator_factories_impl.h
[modify] https://crrev.com/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8/content/renderer/media/media_factory.cc
[modify] https://crrev.com/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8/media/DEPS
[modify] https://crrev.com/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8/media/video/BUILD.gn
[modify] https://crrev.com/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8/media/video/gpu_video_accelerator_factories.h
[modify] https://crrev.com/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8/media/video/mock_gpu_video_accelerator_factories.h
[modify] https://crrev.com/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8/third_party/blink/public/platform/web_video_frame_submitter.h
[modify] https://crrev.com/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8/third_party/blink/renderer/platform/graphics/DEPS
[modify] https://crrev.com/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8/third_party/blink/renderer/platform/graphics/video_frame_submitter.cc
[modify] https://crrev.com/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8/third_party/blink/renderer/platform/graphics/video_frame_submitter.h
[modify] https://crrev.com/2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8/third_party/blink/renderer/platform/graphics/video_frame_submitter_test.cc


### le...@chromium.org (2018-06-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-15)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-06-16)

Approving merge for M68. Branch:3440

### aw...@chromium.org (2018-06-18)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-06-18)

Pls merge you change to M68 branch 3440 ASAP so we can pick it up for this week Beta release. Merge has to happen latest by 1:00 PM PT tomorrow, Tuesday (06/19), so we can pick it up for Wednesday Beta release.





### bu...@chromium.org (2018-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5

commit 1fb6003331dfd2794ae6c654b91fe3ad8109c5a5
Author: CJ DiMeglio <lethalantidote@chromium.org>
Date: Mon Jun 18 22:08:58 2018

Makes VideoFrameSubmitter's ptr to context_provider scoped_refptr.

>>>>>>> 2fa8c2c72da4... Makes VideoFrameSubmitter's ptr to context_provider scoped_refptr.
This CL prevents VideoFrameSubmitter from accessing a bare ptr of
|context_provider_| after it has been deleted by changing ptr to be a
scoped_refptr.

(cherry picked from commit 2fa8c2c72da47e87f4e9a9221b3ddab97ee66fd8)

Bug: 845136
Cq-Include-Trybots: luci.chromium.try:linux_layout_tests_slimming_paint_v2;master.tryserver.blink:linux_trusty_blink_rel;master.tryserver.chromium.linux:linux_layout_tests_slimming_paint_v2
Change-Id: Ia574a206519857ddb4169aaec281b64e3689e8ce
Reviewed-on: https://chromium-review.googlesource.com/1087514
Commit-Queue: CJ DiMeglio <lethalantidote@chromium.org>
Reviewed-by: Justin Novosad <junov@chromium.org>
Reviewed-by: Frank Liberato <liberato@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Sadrul Chowdhury <sadrul@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#566570}
Reviewed-on: https://chromium-review.googlesource.com/1105313
Reviewed-by: CJ DiMeglio <lethalantidote@chromium.org>
Cr-Commit-Position: refs/branch-heads/3440@{#425}
Cr-Branched-From: 010ddcfda246975d194964ccf20038ebbdec6084-refs/heads/master@{#561733}
[modify] https://crrev.com/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5/content/renderer/media/gpu/gpu_video_accelerator_factories_impl.cc
[modify] https://crrev.com/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5/content/renderer/media/gpu/gpu_video_accelerator_factories_impl.h
[modify] https://crrev.com/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5/content/renderer/media/media_factory.cc
[modify] https://crrev.com/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5/media/DEPS
[modify] https://crrev.com/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5/media/video/BUILD.gn
[modify] https://crrev.com/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5/media/video/gpu_video_accelerator_factories.h
[modify] https://crrev.com/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5/media/video/mock_gpu_video_accelerator_factories.h
[modify] https://crrev.com/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5/third_party/blink/public/platform/web_video_frame_submitter.h
[modify] https://crrev.com/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5/third_party/blink/renderer/platform/graphics/DEPS
[modify] https://crrev.com/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5/third_party/blink/renderer/platform/graphics/video_frame_submitter.cc
[modify] https://crrev.com/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5/third_party/blink/renderer/platform/graphics/video_frame_submitter.h
[modify] https://crrev.com/1fb6003331dfd2794ae6c654b91fe3ad8109c5a5/third_party/blink/renderer/platform/graphics/video_frame_submitter_test.cc


### aw...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-21)

Hi cdsrc2016@ - the VRP panel decided to reward $500 for this report. Thanks!

### aw...@google.com (2018-06-21)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-06-24)

Thanks a lot for the reward !
BTW, will this one be assigned a CVE ? 

### sh...@chromium.org (2018-09-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-10-09)

I'm afraid we only issue CVEs to bugs found in the stable channel :-( 

### is...@google.com (2018-10-09)

This issue was migrated from crbug.com/chromium/845136?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091440)*
