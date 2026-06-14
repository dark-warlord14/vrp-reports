# Flickering WebGL with {alpha:false} on mali-400

| Field | Value |
|-------|-------|
| **Issue ID** | [40050541](https://issues.chromium.org/issues/40050541) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebGL |
| **Platforms** | Android |
| **Reporter** | iv...@gmail.com |
| **Assignee** | ka...@chromium.org |
| **Created** | 2019-10-26 |
| **Bounty** | $500.00 |

## Description

Steps to reproduce the problem:
1. Take a device ASUS_Z00VD ( Mali-400 ), 
2. launch any webgl demo , for example https://jsfiddle.net/Hackerham/ksr7z421/2/ , that has {alpha:false} in context creation params
3. look at the flickering

What is the expected behavior?
no flickering

What went wrong?
Here's attached webgl conformance test.

Did this work before? No 

Does this work in other browsers? No
 https://github.com/kiorisun claims the problem persists in other browsers too.

Chrome version: 77.0.3865.120  Channel: n/a
OS Version: 
Flash Version: 

I'm surprised no one reported that. We (PixiJS devs) know it for some time.

Also, possible that https://bugs.chromium.org/p/chromium/issues/detail?id=722132
is related to the issue.

Known workaround: use {alpha: true}

Phone testing was provided by https://github.com/kiorisun , he's to shy to report it here :) We can ask him names of other phone models where its happenning.

## Attachments

- [webgl-conformance-1.0.4-beta- (1).txt](attachments/webgl-conformance-1.0.4-beta- (1).txt) (text/plain, 188.1 KB)
- [main.js](attachments/main.js) (text/plain, 4.5 KB)
- [index.html](attachments/index.html) (text/plain, 333 B)
- [test1.js](attachments/test1.js) (text/plain, 4.5 KB)

## Timeline

### iv...@gmail.com (2019-10-26)

I wrote it here because 

1. The report has to be published somewhere
2. Maybe there is a browser-side workaround

I'm interested in establishing the fact that issue exists and its not pixijs-related problem, PixiJS just uses {alpha:false} by default since beginning.

### kb...@chromium.org (2019-10-28)

Kai: could you please triage this? Thanks.


### ta...@kiorisun.com (2019-10-28)

Tested on Asus ZenFone(ASUS_Z00VD), android 5.1, latest chrome

I reported this to Ivan. I'm not sure it's fair to say it's no pixi related, I think it's fair to say it's related to some specific usage of webgl.
These examples:
http://webglsamples.org/lots-o-images/lots-o-images-draw-elements.html
https://lemon07r.github.io/openfl-bunnymark/

Show no flickering whatsoever.


This one however, doesn't even flicker, it's just white:
https://britzl.github.io/Bunnymark/

All of the pixi v3+ examples flicker without {alpha:true}. But I tested phaser 2 in the past, which uses pixi v2 and it didn't flicker. And I believe it doesn't set alpha to true by default.

My guess is this GPU has issues with some webgl features, but not sure which.
I hope the provided webgl conformance tests help.

Please let me know if any further testing is required. I'll try to find the time to run it on the phone.

### ka...@chromium.org (2019-10-29)

I tried this on a GT-N5110 and was able to reproduce on 68.0.3440.34 with
- alpha:false, premultipliedAlpha: false
- alpha:true, premultipledAlpha: false
- alpha:true, premultipliedAlpha: true
(I didn't try any other options.)
I also saw frames arriving out of order on get.webgl.org.

I put a top-of-tree chrome build at r710112 and suddenly the WebGL canvas was rendering uninitialized data. get.webgl.org was ok but still rendering out of order.

I tried enabling use_virtualized_gl_contexts, which is necessary for synchronization on Mali-T*. This fixed get.webgl.org completely, and got rid of the garbage.
However the jsfiddle is still flickering. Perhaps the uninitialized data bug is an unrelated recent regression? In any case, we will need to expand that workaround.

Now, with use_virtualized_gl_contexts, it DOES seem to be necessary to use both alpha:false and premultipliedAlpha:false.
If either is set to true, the flickering goes away.

### ta...@kiorisun.com (2019-10-29)

Is this issue related to the mali OGL implementation? and EGL_SWAP_BEHAVIOR(or lack of EGL_BUFFER_PRESERVED), as per here:
http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0363d/CJAEEJCF.html

Also, this seems to be a similar issue:
https://github.com/CreateJS/EaselJS/issues/887

Hope it helps.

### ka...@chromium.org (2019-10-29)

I believe the uninitialized data could be a bug related to tile flushing in these devices' eglMakeCurrent implementation. We have a well-established workaround for this, where we virtualize the contexts on top of one GL context instead of using eglMakeCurrent.

The flickering could be tile related, though not directly to EGL_SWAP_BEHAVIOR, because (I think) this is happening on a regular GL texture, not an EGL surface.

I'll have to look into whether preserveDrawingBuffer affects this bug as it does the EaselJS one.

### ka...@chromium.org (2019-10-29)

With top-of-tree plus the virtualized gl contexts workaround, it still flickers regardless of the value of preserveDrawingBuffer.

### ka...@chromium.org (2019-10-29)

Found the commit that triggered the canvas ALWAYS showing uninitialized data instead of just flickering: ccfb91233bc2d34233d7c52192416ad7feb55260
It's unclear why this doesn't appear on all devices (such as the original report device) or why we haven't gotten reports of this.
But fortunately we already know the fix. This at least tells us it's not so recent that we should do a mergeback.

btw, no context creation attributes seem to prevent the uninitialized canvas contents.

### ka...@chromium.org (2019-10-29)

It turns out that it's probably the 2d-canvas-to-webgl-texture copy path that breaks with Aaron's change. Since that's relatively rare (plus this clearly doesn't happen on all Mali-400 devices), it explains why we haven't heard about it.

### ka...@chromium.org (2019-10-29)

[Empty comment from Monorail migration]

### ka...@chromium.org (2019-10-30)

We spend some time debugging this and learned that it seems to be a bug in the disable_gl_rgb_format workaround. This workaround was created for https://crbug.com/chromium/449150 for a *Linux* Mali-400 device, and turns out not to be necessary for *Android* Mali-400 device. There are a few things we want to do here:

- Limit this workaround to Linux only.
- Understand why that path is broken and fix it. The problem is in the clearing of the alpha channel. Due to the workaround, we use an RGBA texture to emulate the alpha:false backbuffer. It's clear that at some point, the RGBA texture's alpha channel is inadvertently getting cleared to 0, making the canvas transparent.
- Try to simplify related code by making premultiplied_alpha_false_texture_ not be a SharedImage if it doesn't need to be.

### iv...@gmail.com (2019-10-30)

[Comment Deleted]

### ka...@chromium.org (2019-10-30)

Sorry, I sort of hijacked this bug report to also include the uninitialized data bug - should have made it separate. Since that one is a security issue, I restricted the bug. Generally security bugs will become public after 14 weeks.

### iv...@gmail.com (2019-10-30)

Yes, I deduced that shortly after I typed the message. OK then, I wont tell specifics to anyone, I'm proud to be a part of security issue!

### ka...@chromium.org (2019-10-30)

Here's that first CL. It didn't automatically send a message to this bug for some reason (maybe it breaks with restrict-view-cc).
https://chromium-review.googlesource.com/c/chromium/src/+/1888954

### ka...@chromium.org (2019-10-30)

Two more CLs on the way:

https://chromium-review.googlesource.com/c/chromium/src/+/1891137 (hopefully)
https://chromium-review.googlesource.com/c/chromium/src/+/1891139

### ka...@chromium.org (2019-10-30)

Both have landed. This should be fixed in Chrome 80 (stable early Feb).

Thank you for the report which uncovered these issues!

### ka...@chromium.org (2019-10-30)

[Empty comment from Monorail migration]

### ka...@chromium.org (2019-10-30)

I'm going to change the category of this bug to "security" so it'll automatically become public after 14 weeks. This might remove your access to the bug, sorry if that happens.

### ka...@chromium.org (2019-10-30)

[Empty comment from Monorail migration]

### ta...@kiorisun.com (2019-10-31)

@kainino If I understand correctly the build will be available via play store in February, correct?
Also, if for any reason the bug persists can we just reply here or do we open a new report?

### ka...@chromium.org (2019-10-31)

Yeah, that's the expected schedule:
https://chromiumdash.appspot.com/schedule

Please try this out on Canary when it rolls out (probably 1-2 days):
https://chromiumdash.appspot.com/commit/840c5167b44a060db8c34c4f1005835bae23206b
You can compare the version of Canary on that page (once it appears) with the one on your device.

If you see the issue again soon or on Canary after this change rolls out, please reply here. If it crops up again after a while, it would be best to file a new bug. Mention "https://crbug.com/chromium/1018528" in that bug so we can link them. Thanks again!

### sh...@chromium.org (2019-10-31)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-31)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-31)

[Empty comment from Monorail migration]

### ta...@kiorisun.com (2019-11-01)

Tested latest canary on my mali-400 phone, good news is Pixi v5 now works. The bad news is I think this isn't fully resolved.
I tried opening js fiddle and it sort of opened, but it wasn't ok on my phone, so i took the code saved it in a JS file and loaded it via an html file, through a localhost.
The code renders ok on my desktop but renders a blank on the mali phone. Maybe it has to do with the copy from canvas to webgl that you mentioned. IDK
I tested setting alpha:true and it works as expected.

Let me know if there are any other things I should test that can help. 

### ta...@kiorisun.com (2019-11-01)

I tried with stencil:false and it worked. But now even after deleting the cache everything works, whatever options i set. So i think I might have messed something previously in testing today and it's 100% fixed. Thanks again!

### ka...@chromium.org (2019-11-01)

Glad to hear it! Let me know if the problem pops up again.

### na...@google.com (2019-11-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-05)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M79. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-05)

This bug requires manual review: M79 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2019-11-05)

There were 3 commits on this bug but they didn't properly post due to Restrict-View-CC.

Only one is a security fix:
1. Yes, it just expands a very well-established gpu driver bug workaround to additional hardware. This fix prevents reading uninitialized GPU memory from web pages.
2. https://chromium-review.googlesource.com/c/chromium/src/+/1888954
3. It has landed but I have only tested it on a local ToT build.
4. Sheriffbot says so :)
5. No

### be...@google.com (2019-11-06)

Approved for merge to 79, branch 3945.

### sh...@chromium.org (2019-11-11)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2019-11-11)

Oops, forgot to update labels.
https://chromium-review.googlesource.com/c/chromium/src/+/1902254



### ka...@chromium.org (2019-11-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-21)

Congrats the Panel decided to reward $500 for this report!

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### iv...@gmail.com (2019-11-21)

Hello, Natasha!

It was collaboration between me andh KioriSun (comment number 3), can we split it 50/50? If so, please send him the form too.


### na...@google.com (2019-11-21)

Thanks for reaching out - I'm working with finance to get reward payment split between both of you. 


### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-06)

ivan.popelyshev@gmail.com - how would you (and KioriSun) like to be credited in the release notes?

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### iv...@gmail.com (2019-12-06)

Ivan Popelyshev

### ta...@kiorisun.com (2019-12-06)

You guys can credit me as André Bonatti

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1018528?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/449150, crbug.com/chromium/909937]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050541)*
