# Security: PresentationRequest dialog can appear over the wrong tab

| Field | Value |
|-------|-------|
| **Issue ID** | [40055761](https://issues.chromium.org/issues/40055761) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Cast>UI, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2021-05-06 |
| **Bounty** | $1,000.00 |

## Description

(Internal tracker: [b/187720839](https://issues.chromium.org/issues/187720839))

Chrome Version: 92.0.4498.0 (Official Build) canary (x86\_64)  

Operating System: macOS

**REPRODUCTION CASE**

1. Open the testcase and click on the button
2. Switch another tab e.g google.com

- Observe that the PresentationRequest dialog appear over google.com page (The same behavior in <https://crbug.com/chromium/1143057>)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 479 B)
- [Screen Shot 2021-05-06 at 2.55.12 AM.png](attachments/Screen Shot 2021-05-06 at 2.55.12 AM.png) (image/png, 211.5 KB)
- [screen.mov](attachments/screen.mov) (video/quicktime, 1.2 MB)
- [screen.mov](attachments/screen.mov) (video/quicktime, 1.0 MB)

## Timeline

### [Deleted User] (2021-05-06)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-05-06)

Thanks for reporting this! I'm presently unable to reproduce this on 92.0.4499.0 (Canary) or on 90.0.4430.93 (Stable). When I navigate to another tab, once the timer fires, the PoC tab is re-highlighted before displaying the prompt (that is, it shows on the local page, not on the google.com example)

Could you perhaps provide a screen recording of your reproduction steps, just to make sure I'm not missing any steps?

[Monorail components: UI>Browser>Permissions>Prompts]

### ch...@gmail.com (2021-05-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-06)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2021-05-06)

Thanks! Sorry, I'm still having trouble reproducing (and, for all I know, it could be related to my local network here and the devices I have for casting)

Could you paste the *full* details from chrome://version ? This would help determine if there might be an experiment group that you could be running in that could be confounding this :)

### rs...@chromium.org (2021-05-06)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-05-06)

Google Chrome	92.0.4498.0 (Official Build) canary (x86_64)
Revision	9324fb761d7ee2ca67a3786282af8b303c9d292d-refs/branch-heads/4498@{#1}
OS	macOS Version 10.12.6 (Build 16G2136)
JavaScript	V8 9.2.146
User Agent	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4498.0 Safari/537.36
Command Line	/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary -psn_0_40970 --flag-switches-begin --enable-experimental-web-platform-features --enable-experimental-webassembly-features --javascript-harmony --enable-features=GlobalMediaControlsCastStartStop,ParallelDownloading,Portals,PortalsCrossOrigin,RawClipboard,ReadLater,WebPaymentsExperimentalFeatures --flag-switches-end --restore-last-session --origin-trial-disabled-features=SecurePaymentConfirmation
Executable Path	/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary
Profile Path	/Users/iamtech/Library/Application Support/Google/Chrome Canary/Profile 22
Variations	84085631-377be55a
90a7075b-535a3667
16b16054-3f4a17df
1fa5b2f3-ed8899de
59b6f412-11f108a5
60d4b352-ab54a14d
d7561e8c-ee63ae02
b3249ec4-3f4a17df
a9ef513c-f23d1dea
da89714-ac581675
3fa8d059-377be55a
8ae424bf-62410d2b
87f33ad6-3f4a17df
afb5d7b8-69245e55
3c98d047-3f4a17df
aed6e5d4-5a8057d0
8816d952-377be55a
6025934e-3f4a17df
4d936449-37049b31
2c3bc653-d017481
fcd625f7-3f4a17df
7638c831-857014ec
38b9885d-ca7d8d80
edb58ea9-f23d1dea
a2629469-f23d1dea
51a53749-3f4a17df
deb1cb12-26df0418
41e765a5-f23d1dea
8e44abde-cad95a63
47b5f350-377be55a
7c2504d0-bd58b24e
8f83697a-199a5257
dbf7a8af-25d42946
f2cb61f-1234653b
dc2bb3ae-b5998b3c
c3aebffb-3f4a17df
a2fd384c-5c0c03aa
f90aa7cd-3f4a17df
65570806-998676
dd8d67e-3f4a17df
c2455b5c-a2d707c6
a582a1b8-ad75ce17
da2d8531-f23d1dea
8e3b682d-f23d1dea
b9b6628c-3f4a17df
1d606bb5-f23d1dea
d89faab1-ec6b837d
3042ad4b-a0e56f74
e4a357e9-2045969c
2e753575-f23d1dea
3fd33f16-45db657a
6262de83-3f4a17df
7b7adda-69181036
83a11282-8f2cf18e
5a53e38-e3bb0dc9
332a4d9b-cad95a63
9914b7bf-3f4a17df
e79de56c-20b01172
357a64de-20b01172
142e58d7-c97686a1
4902b7bc-3f4a17df
fa6aa590-3a447918
c992f345-8af6a0d6
9bfe3ed7-ca7d8d80
28114f9b-f2718d9f
d8692482-ca7d8d80
a120b571-23ea8a4
291d0672-ca7d8d80
7a911e9f-39529a76
255dfea8-6ae6fcb2
7dec9614-377be55a
bdbcc4a1-351587f5
cbb84eed-4e2e67e4
e153f4cb-77f964a1
ca5a2953-81658715
3487aa71-27a0c3c6
12366760-3f4a17df
5fe247df-b9a99422
ad46906e-18a10ae6
cb9831f4-377be55a
4ea303a6-ecbb250e
f48aee36-377be55a
1c00821b-17ba6352
f515e29f-3f4a17df
970244bf-7d3f0946
6d3e17fc-f23d1dea
be96751-3f4a17df
2810dd28-3f4a17df
d520a9f0-377be55a
ef4764d7-22e20947
fbe267b5-ca7d8d80
4f6db7c8-3f4a17df
a1c083c6-3f4a17df
92136dde-58f537db
f31b480d-3f4a17df
6a9d5557-60f2bba
7760b5b2-9a39cffa
546c3f13-f23d1dea
931c5f72-c39258b0
494d8760-52325d43
3ac60855-486e2a9c
63dcb6a3-d2276ecd
e706e746-f911fcfa
f296190c-116bbed1
4442aae2-a5822863
f690cf64-6e3b1976
ed1d377-e1cc0f14
75f0f0a0-6bdfffe7
e2b18481-6e597ede
e7e71889-e1cc0f14
23032e71-f23d1dea
b1ceb06f-6b7b34d
6a2df91f-3f4a17df
e1368496-3f4a17df
248e3a0-a3a14831
a46926f0-f13a635d
dba92675-f23d1dea
16d8ab13-48123131
fb0a7744-3d47f4f4
497bad44-3d47f4f4
fb50494f-72cac062
f7ac31c9-3f4a17df
547e761a-3f4a17df
89f843ca-584aa0f
5e31bb48-75513c66
abb39457-f2718d9f
a9deeaf7-7d3f0946
a461b170-64207fb2
dd82d379-fa554100
def27776-9723ae37


### [Deleted User] (2021-05-06)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2021-05-07)

Thanks! I'm still having trouble reproducing this, and none of your current experiments seem like it would affect this. That said, given the past pattern, I'd like to tentatively play defensively while we work to reproduce.

Mark: Could you help me with this? From looking through the code, it seems the Media Router code is responsible for the cast device selection, which seems to be what's triggered by PresentationRequest (AFAICT). If you look at https://bugs.chromium.org/p/chromium/issues/detail?id=1143057#c2 and https://bugs.chromium.org/p/chromium/issues/detail?id=1143057#c10 you can see there have been past issues with respect to the active web contents versus the requesting web contents.

Like I mentioned in https://crbug.com/chromium/1206131#c2, when I try to reproduce this, I do have focus shifted to the requesting web contents, but perhaps you'll recognize conditions that might enable this to be better reproduced (especially since the UI I encounter for the prompt is different than what's presented in https://crbug.com/chromium/1206131#c3)

### mf...@chromium.org (2021-05-07)

It looks like we are passing the correct WebContents* to the UI code from content/browser; the pinned toolbar icon might play some role in whether we focus that tab when the dialog is shown.

[Monorail components: Internals>Cast>UI]

### mf...@chromium.org (2021-05-07)

Moving back into triage for the Cast in Chrome folks.

### [Deleted User] (2021-05-08)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-08)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@chromium.org (2021-05-10)

I was able to repro on 92.0.4493.0. This requires chrome://flags/#global-media-controls-cast-start-stop enabled (--enable-features=GlobalMediaControlsCastStartStop), which is currently in Canary/Dev experiment.

rsleevi@, what's your opinion on the severity of the bug in terms of whether we should halt the Canary/Dev experiment or block the upcoming beta experiment? Note that the origin of the requesting tab is still shown in the dialog.

### ta...@chromium.org (2021-05-10)

[Description Changed]

### ta...@chromium.org (2021-05-10)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-05-10)

D'oh! I missed that command-line flag when I diff'ed variations. Thank you so much takumif.

We've consistently treated these as Medium severity, under the basis of "A bug that allows web content to tamper with trusted browser UI", although as you note, whether or not that UI has the origin displayed in it may be a mitigating factor here.

estark: You're my go-to person for UI questions. I think the answer for https://crbug.com/chromium/1206131#c14 is that if this is only in a Finch-controlled trial, we should halt the trial until it can be fixed. Does that sound right?

### rs...@chromium.org (2021-05-10)

[Empty comment from Monorail migration]

### ta...@chromium.org (2021-05-10)

Muyao PTAL

### es...@chromium.org (2021-05-10)

I would probably call this Low severity (with the origin displayed in the dialog being a mitigating factor), or possibly even call it a privacy bug rather than a security bug. There are 2 differences from https://crbug.com/chromium/1143057, which we labeled Medium:
- In 1143057, the origin was displayed but only as a passive disclosure, whereas here it's a chooser pattern and the user has to consciously choose the origin that they want to present -- making it less likely that the user will be misled by the tab over which the dialog is showing.
- In 1143057, the attack scenario was that a malicious origin would get access to a USB device, when the user thought they were granting access to a trustworthy origin (the tab over which the prompt showed). Here the attack scenario is that a malicious origin presents itself when the user intended to present a different origin. That seems much less severe as an attack.

In any case, I agree that the right thing to do is pause the Finch trial and restart it when there's a fix.

### rs...@chromium.org (2021-05-10)

[Empty comment from Monorail migration]

### mu...@google.com (2021-05-10)

I've created this CL to pause the experiment. https://critique-ng.corp.google.com/cl/373008678

I will look into this issue ASAP.

### [Deleted User] (2021-05-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f8360c27f55e8e0a649f4ffdc7aff601eef6a4b1

commit f8360c27f55e8e0a649f4ffdc7aff601eef6a4b1
Author: Muyao Xu <muyaoxu@google.com>
Date: Wed May 12 03:13:23 2021

[Zenith] Ensure the Zenith dialog is shown over the correct tab

This CL activates the WebContents that initiated the PresentationRequest
before showing the Zenith dialog so that the dialog always appear over
the correct tab.

Bug: b/187720839, 1206131
Change-Id: I69c5475f82742871bc2ec22be24ef0cf98a63c27
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2888366
Commit-Queue: Muyao Xu <muyaoxu@google.com>
Reviewed-by: Takumi Fujimoto <takumif@chromium.org>
Cr-Commit-Position: refs/heads/master@{#881856}

[modify] https://crrev.com/f8360c27f55e8e0a649f4ffdc7aff601eef6a4b1/chrome/browser/ui/views/media_router/media_router_dialog_controller_views.cc
[modify] https://crrev.com/f8360c27f55e8e0a649f4ffdc7aff601eef6a4b1/chrome/browser/ui/views/media_router/media_router_dialog_controller_views_browsertest.cc
[modify] https://crrev.com/f8360c27f55e8e0a649f4ffdc7aff601eef6a4b1/components/media_router/browser/presentation/start_presentation_context.h


### ke...@chromium.org (2021-05-13)

muyaoxu@: Is this issue now resolved?

### ch...@gmail.com (2021-05-13)

Yes.

muyaoxu, thanks for the quick fix!

### ke...@chromium.org (2021-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-15)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-28)

Hi Khalil! The VRP Panel has decided to award you $1,000 for this report. Thank you for reporting this issue! 

### am...@google.com (2021-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1206131?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Cast>UI, UI>Browser>Permissions>Prompts]
[Monorail blocking: crbug.com/chromium/1107158]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055761)*
