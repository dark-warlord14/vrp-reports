# Security: Cross-origin pixel reading and history sniffing via SVG filter timing attack

| Field | Value |
|-------|-------|
| **Issue ID** | [40086661](https://issues.chromium.org/issues/40086661) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SVG, Privacy |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | fs...@chromium.org |
| **Created** | 2017-01-27 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

By rendering a FeConvolveMatrix SVG filter over a target iframe and timing its execution an attacking page can extract pixel values from a cross-origin page being iframe'd.

This also allows reading ones own origin for history sniffing.

This is based on previous work we did, see <http://cseweb.ucsd.edu/~dkohlbre/papers/subnormal.pdf>

**VERSION**  

Chrome Version: at least 54 to 57.02987.8  

Operating System: Ubuntu Linux 16.10, Windows 10, OSX 10.11.6, ChromeOS 55.0.2883.105.

**REPRODUCTION CASE**  

I've attached a PoC that reconstructs a 48x48 px region from the chosen origin into a canvas.  

It works very well on static pages, and will work intermittently on active pages.

Up the pixel multiplier if it doesn't seem to be working on your machine. (100-500 are reasonable ranges, and it depends on your build and env what works best)

screenshot of a successful run is also attached.

NOTES  

This must be run on a Chrome platform that supports GPU acceleration of SVG filters. (Ex: Mac mini isn't vulnerable)  

The attack does not run on the GPU, but takes advantage of the FTZ and DAZ FPU flags being disabled if the element being rendered is already texture backed.

This bug will be included in a USENIX Security conference submission (2/16/17) but will not be published for at least several months after that.

DETAILS  

Normally it appears that Skia sets the FPU DAZ and FTZ flags when executing SVG filters on the CPU. However, if the element being rendered is already in the GPU pipeline (forced with transform:rotateY(1deg)) then these flags are not set. We are taking advantage of floating point multiply timing differences on the CPU, which we get back to via making a kernel of size >36. see <https://cs.chromium.org/chromium/src/third_party/skia/src/effects/SkMatrixConvolutionImageFilter.cpp?l=304>

We are using timing differences in floating point multiplies between 0\*subnormal and 2.x\*subnormal. See <https://cs.chromium.org/chromium/src/third_party/skia/src/effects/SkMatrixConvolutionImageFilter.cpp?l=186> etc.

It is highly likely that other SVG filters are impacted by this bug in the same way. As long as you can cause a bail from the GPU so that the FTZ and DAZ flags aren't set any multiply with secret data is vulnerable. Division is vulnerable even with FTZ and DAZ.

## Attachments

- [chrome_convolve.html](attachments/chrome_convolve.html) (text/plain, 4.4 KB)
- [chrome_pxbench_exp.js](attachments/chrome_pxbench_exp.js) (text/plain, 7.9 KB)
- deleted (application/octet-stream, 0 B)
- [example_result.png](attachments/example_result.png) (image/png, 108.5 KB)
- [686253.png](attachments/686253.png) (image/png, 572.2 KB)
- [686253-MAC.png](attachments/686253-MAC.png) (image/png, 248.3 KB)
- [Accuracy_Win7.JPG](attachments/Accuracy_Win7.JPG) (image/jpeg, 108.5 KB)
- [Canary_Win7.JPG](attachments/Canary_Win7.JPG) (image/jpeg, 89.6 KB)
- [Linux.png](attachments/Linux.png) (image/png, 215.2 KB)
- [Windows (1).PNG](attachments/Windows (1).PNG) (image/png, 393.0 KB)
- [686253(Mac).png](attachments/686253(Mac).png) (image/png, 235.1 KB)
- [686253(Windows).PNG](attachments/686253(Windows).PNG) (image/png, 172.5 KB)
- [686253(Linux).png](attachments/686253(Linux).png) (image/png, 217.2 KB)

## Timeline

### es...@chromium.org (2017-01-27)

senorblanco, could you please take a look at this? Looks similar to other reports you've handled in the past (https://crbug.com/chromium/615851, https://crbug.com/chromium/586820). Thanks.

[Monorail components: Blink>SVG Privacy]

### [Deleted User] (2017-01-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-28)

[Empty comment from Monorail migration]

### se...@chromium.org (2017-02-01)

Note to self: this will probably require a fix similar to https://crrev.com/014a9a0ea7260b37773adb545b7cabbff80423b9 in that we'll enable flush-to-zero for denorms, but before going into the GPU path as well as the CPU path.

### [Deleted User] (2017-02-02)

As an additional note, even with FTZ/DAZ set any sqrt over secret data is timing vulnerable for single precision floats. I didn't see any of these when I looked through the filters.

For double precision (Skia looks like its all/mostly single precision) both div and sqrt are vulnerable even with FTZ/DAZ.

### pa...@chromium.org (2017-02-24)

jschuh and I were talking about this, and thought that there could be some CORS-based defense to this — the target site would have to opt in to cross-site SVG filtering before Chrome would let the attacking site run a filter. Is something like that possible?

### [Deleted User] (2017-06-28)

Hi,
We are going to be pushing out the final version of our paper (which includes a technical discussion of this bug) on Thursday (June 29th).
We can get the paper held back until the conference (Aug 16th), or we can omit some technical detail (ex: omit the name of the vulnerable filter) if there will be a patch available between now and August.
Let me know what the needed restrictions are.

### fs...@chromium.org (2017-06-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-06-28)

#7: Thank you for being nice. :) You can go ahead and disclose. fserb has a patch up for review now, and we think we can get it merged into 60 and maybe even 59. This bug will get updated when that lands, so you'll know. Thanks!

### fs...@chromium.org (2017-06-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/98168e6a9dbd0c52982e47e68baafeda3d8c0192

commit 98168e6a9dbd0c52982e47e68baafeda3d8c0192
Author: Fernando Serboncini <fserb@chromium.org>
Date: Wed Jun 28 20:30:33 2017

Disable subnormal floats on GL renderer filters and bg filters

This prevents timing attacks using SVG filters

Bug: 686253
Cq-Include-Trybots: master.tryserver.blink:linux_trusty_blink_rel
Change-Id: I54534bf93c4dfe954f667e5c210aa83d5c9abcf4
Reviewed-on: https://chromium-review.googlesource.com/552957
Commit-Queue: Fernando Serboncini <fserb@chromium.org>
Reviewed-by: enne <enne@chromium.org>
Cr-Commit-Position: refs/heads/master@{#483116}
[modify] https://crrev.com/98168e6a9dbd0c52982e47e68baafeda3d8c0192/cc/output/gl_renderer.cc


### pa...@chromium.org (2017-06-28)

fserb: Thanks again. :) Assuming that the PoC indeed does not work with your patch applied, you can go ahead and all allpublic to the labels when you mark this Fixed.

Also, what about Android and Fuchsia platforms? Any reason the attack would not have worked on those platforms?

### fs...@chromium.org (2017-06-30)

Btw, please let us know when the paper is out (and share it ;), so I can open the bug.

### fs...@chromium.org (2017-06-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-30)

This bug requires manual review: M60 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2017-06-30)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-06-30)

This bug meets the bar for merge to M60. Approving merge. (branch: 3112)

### ab...@chromium.org (2017-06-30)

Rejecting merge to M59. We've already rolled out to 100%. Please confirm if this bug is  critical enough to warrant a respin. However, reading the description and seeing this is a low priority bug, it doesn't appear to be. 

### bu...@chromium.org (2017-07-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a696ef7e95f81c321475c4a5171093df979ca31d

commit a696ef7e95f81c321475c4a5171093df979ca31d
Author: Fernando Serboncini <fserb@chromium.org>
Date: Tue Jul 04 14:24:30 2017

Disable subnormal floats on GL renderer filters and bg filters

This prevents timing attacks using SVG filters

TBR=fserb@chromium.org

(cherry picked from commit 98168e6a9dbd0c52982e47e68baafeda3d8c0192)

Bug: 686253
Cq-Include-Trybots: master.tryserver.blink:linux_trusty_blink_rel
Change-Id: I54534bf93c4dfe954f667e5c210aa83d5c9abcf4
Reviewed-on: https://chromium-review.googlesource.com/552957
Commit-Queue: Fernando Serboncini <fserb@chromium.org>
Reviewed-by: enne <enne@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#483116}
Reviewed-on: https://chromium-review.googlesource.com/558676
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Cr-Commit-Position: refs/branch-heads/3112@{#511}
Cr-Branched-From: b6460e24cf59f429d69de255538d0fc7a425ccf9-refs/heads/master@{#474897}
[modify] https://crrev.com/a696ef7e95f81c321475c4a5171093df979ca31d/cc/output/gl_renderer.cc


### pn...@chromium.org (2017-07-12)

Tested the issue on Mac OS 10.12.5, Ubuntu 14.04 and Windows 10 using Chrome Beta version M60 - 60.0.3112.66 as per the issue mentioned in original comment. Observed that test doesn’t initiate in the Windows and Ubuntu machines and an alert “Uncaught ReferenceError: init is not defined” is seen in the console after clicking on "RUN" button. However in Mac, test is completed.

@fserb -- Could you please let us know whether the behavior noticed on Mac is intended or not. It would help us in further testing the issue. Please refer the screenshots attached.

Please let us know if we have missed anything.

Thanks in advance.


### fs...@chromium.org (2017-07-12)

I don't know about the init thing (it was running fine on my Ubuntu) last I tried. It seems you are missing a file, did you download the JS file and it's on the same directory?

But the Mac output you are seeing means it didn't work (the Reconstruction image doesn't contain any information related to the Reference image). I.e., the fix fixed it.



### ma...@chromium.org (2017-07-12)

[Empty comment from Monorail migration]

### ma...@chromium.org (2017-07-12)

Below are the accuracy levels that i'm noticing for Latest Beta#60.0.3112.66.

Win7: [80.25]
Mac 10.12.5: [50.04]
Linux Ubuntu 14.04: [49.95]

Thank you!

### pa...@chromium.org (2017-07-12)

Re: #12: Should this bug be marked as affecting Android and/or Fuchsia also?

### fs...@chromium.org (2017-07-13)

Can you send a screenshot of the win7 one? I wanna see what 80% looks like.

### ma...@chromium.org (2017-07-13)

OK, seems like i was switching focus from SVG testing tab earlier, that might be the reason it was showing different accuracy? Now i'm seeing <50 on the same Win7 machine.

### fs...@chromium.org (2017-07-13)

hmm. This is weird.

### th...@gmail.com (2017-07-13)

[Comment Deleted]

### [Deleted User] (2017-07-13)

Hi,
To be clear (and I should've put this on the PoC itself!) any % accuracy not near 50% is bad.

If the recovered image looks like the input image, or even an inverted copy as in that Win7 example, then the attack still works.

Interestingly, that test is showing that for that configuration the timing deltas are backwards, but still exists.

### fs...@chromium.org (2017-07-13)

Yeah. I got that. Reopening on win7 to see what's up.

### pd...@chromium.org (2017-07-13)

I just got 61.6% on Win10 with 61.0.3141.7 so I think this may affect all windows.

### ma...@chromium.org (2017-07-13)

Here is the attached accuracy for Canary#61.0.3156.0 on Win7 w/ switching tab focus.

### se...@chromium.org (2017-07-13)

It looks like MSC doesn't define __SSE__ which is what we use to know if we can use _mm_set_csr(). We assume SSE2 as a min-spec in Chrome, so maybe this should be:

#if defined(ARCH_CPU_X86_FAMILY)

### fs...@chromium.org (2017-07-13)

Fix on the way.

### se...@chromium.org (2017-07-13)

Re:#24: When dealing with an earlier timing attack, I wrote an ARM version of 
the subnormal-float-disabler, but it did not fix the issue -- I couldn't 
figure out why. However, in the meantime, a patch landed to enable main-frame
before-activation in CC, which scrambled the timing enough to foil the
exploit.

### fs...@chromium.org (2017-07-13)

I take that back. :)


### bu...@chromium.org (2017-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a9563a849fc62ce0be68cb60fe740d48eff397a3

commit a9563a849fc62ce0be68cb60fe740d48eff397a3
Author: Fernando Serboncini <fserb@chromium.org>
Date: Thu Jul 13 23:05:37 2017

Use ARCH_CPU_X86_FAMILY instead of SSE, for subnormal float disabler

MSC doesn't define SSE, so this wasn't working properly on Windows

Bug: 686253
Change-Id: I5e49e9dec43228288261160d8e9eede9b4a6bf75
Reviewed-on: https://chromium-review.googlesource.com/570351
Commit-Queue: Fernando Serboncini <fserb@chromium.org>
Reviewed-by: Vladimir Levin <vmpstr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#486517}
[modify] https://crrev.com/a9563a849fc62ce0be68cb60fe740d48eff397a3/cc/base/math_util.cc
[modify] https://crrev.com/a9563a849fc62ce0be68cb60fe740d48eff397a3/cc/base/math_util.h


### sh...@chromium.org (2017-07-14)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fs...@chromium.org (2017-07-14)

Requesting a second merge on 60, because it wasn't working properly on Windows.

### sh...@chromium.org (2017-07-14)

This bug requires manual review: We are only 10 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fs...@chromium.org (2017-07-14)

The previous one was approved. This one is even simpler. It's replacing a #ifdef from __SSE__ to X86_ARCH so the code that used to run on mac/linux also gets triggered on windows. But it's literally 2 instructions. :)


### ma...@chromium.org (2017-07-14)

bustamante@ for M60-Merge-Review.

### ab...@chromium.org (2017-07-15)

[Empty comment from Monorail migration]

### br...@chromium.org (2017-07-18)

Tested this issue on Ubuntu 14.04 and Windows-10 using chrome latest dev #61.0.3159.5 and observed the pixel rendering in different accuracy's. 

Attaching screen shot for reference, Could anyone please take a look on it and let us know if the fix is working as intended or not for M61? 

Thanks!

### se...@chromium.org (2017-07-18)

Yes, that looks "good" (as in, the results looks nothing like the reference, so nothing was sniffed -- doesn't matter that the different platforms give different results, just that they don't resemble the reference).

### bu...@chromium.org (2017-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0bc594ca693eb677b9ba658ee939eaa9abbf35c5

commit 0bc594ca693eb677b9ba658ee939eaa9abbf35c5
Author: Fernando Serboncini <fserb@chromium.org>
Date: Tue Jul 18 14:15:24 2017

Use ARCH_CPU_X86_FAMILY instead of SSE, for subnormal float disabler

MSC doesn't define SSE, so this wasn't working properly on Windows

TBR=fserb@chromium.org

(cherry picked from commit a9563a849fc62ce0be68cb60fe740d48eff397a3)

Bug: 686253
Change-Id: I5e49e9dec43228288261160d8e9eede9b4a6bf75
Reviewed-on: https://chromium-review.googlesource.com/570351
Commit-Queue: Fernando Serboncini <fserb@chromium.org>
Reviewed-by: Vladimir Levin <vmpstr@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#486517}
Reviewed-on: https://chromium-review.googlesource.com/574741
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Cr-Commit-Position: refs/branch-heads/3112@{#632}
Cr-Branched-From: b6460e24cf59f429d69de255538d0fc7a425ccf9-refs/heads/master@{#474897}
[modify] https://crrev.com/0bc594ca693eb677b9ba658ee939eaa9abbf35c5/cc/base/math_util.cc
[modify] https://crrev.com/0bc594ca693eb677b9ba658ee939eaa9abbf35c5/cc/base/math_util.h


### rb...@chromium.org (2017-07-19)

Tested this issue on Windows-7,Mac 10.12.5 and Ubuntu 14.04 using chrome latest Beta #60.0.3112.72 and observed the pixel rendering in different accuracy's. 

Attaching screen shots for reference, Could anyone please take a look on it and let us know if the fix is working as intended or not for M60? 

Thank You!

### se...@chromium.org (2017-07-19)

LGTM

### rb...@chromium.org (2017-07-19)

Please find the Linux screen shot for reference.

### se...@chromium.org (2017-07-19)

Also LGTM

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-06)

Nice one! The Chrome VRP Panel decided to award $2,000 for this report.

### aw...@chromium.org (2018-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2018-01-06)

Wow! That is great news, thanks! :)

I realized I never responded to #13, sorry about that.
Paper and talk are at https://www.usenix.org/conference/usenixsecurity17/technical-sessions/presentation/kohlbrenner
Tools and PoCs are available at https://cseweb.ucsd.edu/~dkohlbre/floats

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/686253?no_tracker_redirect=1

[Multiple monorail components: Blink>SVG, Privacy]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086661)*
