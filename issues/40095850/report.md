# Overflow of the transform scale CSS property freezes/crashes the renderer allowing cross-origin content spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40095850](https://issues.chromium.org/issues/40095850) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Compositing>Rasterization |
| **Platforms** | Linux, Windows |
| **Reporter** | he...@gmail.com |
| **Assignee** | er...@chromium.org |
| **Created** | 2019-07-29 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Setting a really large value for the transform scale CSS property of an iframe seems to freeze/crash the renderer, which allows an attacker to display cross-origin content on their page by changing the focus between tabs.

The use of a cross-origin iframe inside the crashed renderer also allows the attacker to display attacker-controlled content over the recently crashed renderer.

The attack's idea boils down to opening the real website in a new tab and after a few seconds closing it. This makes the attacker's page (which has the renderer crashed) be focused, which in turn will be displayed with the content of the old tab. If the user is not paying attention, it will be really hard to notice that the tabs changed and that the user is now in the attacker's page.

In the PoC I also add a long hash to the URL, which changes it to "about:blank#blocked". This is done to give more credibility to the attack.

**VERSION**  

Version 77.0.3860.5 (Official Build) dev (64-bit)  

Tested on Windows and Linux. Doesn't appear to be reproducible on Mac.

**REPRODUCTION CASE**

1. Access <https://lbherrera.github.io/lab/chrome-9a135d33/index.html> and click on the link.
2. After a few seconds, there should be cross-origin content displayed under the attacker's page.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

This bug is subject to a 90 day disclosure deadline. After 90 days elapse  

or a patch has been made broadly available (whichever is earlier), the bug  

report will become visible to the public.

## Timeline

### do...@chromium.org (2019-07-29)

Seems like the root cause might be in transform land (renderer freeze/crash), but I'm curious about the UI interaction. Do you mind putting up a video of what you're seeing?

Over to the CSS folks first.

[Monorail components: Blink>CSS]

### he...@gmail.com (2019-07-29)

dominickn@: https://youtu.be/QysV-5pfIkc

### sh...@chromium.org (2019-07-30)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-30)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@gmail.com (2019-07-31)

By the way, this also impacts stable.

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### fu...@chromium.org (2019-07-31)

Devtools shows rasterization threads use a massive amount of time (didn't finish in 8 seconds at which point I stopped the tracing).


[Monorail components: -Blink>CSS Blink>Paint Internals>Compositing]

### sc...@chromium.org (2019-07-31)

If we're stuck in raster threads then this is GPU. Maybe we are sending malformed content, though more likely we're overflowing something in the transform code and the raster is failing badly as a result. Maybe something going negative interacting with a loop counting down to zero?

[Monorail components: -Blink>Paint -Internals>Compositing Internals>Compositing>Rasterization]

### pd...@chromium.org (2019-07-31)

This is a creative attack. Note that in the reproduction, you need to wait 5 seconds to see the attack.

This attack is possible because we attempt to keep the page usable after running out of gpu memory. I don't think it would be feasible to just crash in this situation. Could we force out-of-memory to raster white instead of nothing?

### do...@chromium.org (2019-08-01)

That is quite compelling - upping the priority to High We ideally want a fix for this merged to M77.

### pd...@chromium.org (2019-08-01)

[Empty comment from Monorail migration]

### en...@chromium.org (2019-08-01)

I verified by setting always_clear=true (https://osscs.corp.google.com/chromium/chromium/src/+/master:components/viz/service/display/gl_renderer.cc;l=464?q=gl_renderer.cc&ss=chromium) that the page turns blue when clears are on.  This confirms for me that we are definitely not drawing anything here and are reusing the backbuffer from the previous frame.

I think forcing out-of-memory to raster white is not the solution I would recommend.  In general, our solution to this has been to use AppendQuadsToFillScreen (https://osscs.corp.google.com/chromium/chromium/src/+/master:cc/trees/layer_tree_host_impl.cc;l=1045) which doesn't (shouldn't?) consider out of memory quads.  It uses occlusion to figure out what's been drawn in a frame and fills in quads behind them to make sure everything is covered.  I suspect that's probably what's not working here.

### en...@chromium.org (2019-08-01)

[Empty comment from Monorail migration]

### en...@chromium.org (2019-08-02)

It does seem like we're not considering oom tiles when we're generating AppendQuadsToFillScreen, which means that if everything on screen was oom but it "covered" the screen, we wouldn't generate them.  This is easy enough to fix by modifying the unoccluded_screen_space_region we pass to AppendQuadsToFillScreen if num_tiles_missing > 0.  However, this doesn't seem to fix the problem as I would expect it to.

I thought that maybe it was the drawing occlusion in viz::Display that was culling these additional quads I was adding, but that doesn't seem to be it either.  Still investigating.

### en...@chromium.org (2019-08-05)

[Empty comment from Monorail migration]

### en...@chromium.org (2019-08-10)

I was out a few days this week, but I spent some time looking into this.

It looks like although we're not considering oom tiles properly as a part of occlusion, that's a separate bug that should get fixed.  (Probably by just always appending quads to fill the screen when any tiles are missing.)

However, in this case, there are no oom tiles.  There's a layer that covers the whole screen and is marked contents opaque.  It is not a solid color itself but its four tiles are detected as being as solid color (and thus causing occlusion that blocks AppendQuadsToFillScreen filling the background).  However, the reason for this is that in SolidColorAnalyzer::DetermineIfSolidColor, if the offsets are empty (!) then we return transparent which we treat as "yes this is a solid color, but it is transparent".

In PictureLayerImpl::AppendQuads, we fall down the individual tile is a solid color, but because alpha <0 we don't emit anything.  This is probably a second tangential bug that needs to be fixed.  If a layer is content_opaque, we should not get in that path.  This at least needs a DCHECK.

This bug is """fixed""" by returning base::nullopt in the solid color analyzer if offsets are empty, or by disabling solid color analysis.  It looks like the issue is ultimately that the rtree bounds have overflowed as they are -2147483648,-2147483648 2147483647x2147483647.  I think maybe we need to ignore painting things that are outside the positive quadrant of space, but this needs a little bit more investigation before I can make sure that fix is ok.

It seems like there's a few things here to fix.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6b0d88c990d4c2dd844d05072ef5f10a8b63dc25

commit 6b0d88c990d4c2dd844d05072ef5f10a8b63dc25
Author: Adrienne Walker <enne@chromium.org>
Date: Sat Aug 17 02:05:20 2019

cc: When tiles are missing, always append fill quads

Currently the occlusion tracker in cc doesn't consider whether or not
layers have missing tiles (due to oom, or otherwise).  This will lead to
incorrect calculations for the unoccluded area to append quads to fill
the screen in.  Fix this with a workaround to always fill the entire
screen in these cases.

This does not fix https://crbug.com/chromium/988590, but was discovered during the
investigation of that issue, so I'm linking it to that bug.

Bug: 988590
Change-Id: I940bde8b3c976f311d6e7869ee84f0dda9a94384
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1754277
Reviewed-by: Khushal <khushalsagar@chromium.org>
Commit-Queue: enne <enne@chromium.org>
Cr-Commit-Position: refs/heads/master@{#687922}

[modify] https://crrev.com/6b0d88c990d4c2dd844d05072ef5f10a8b63dc25/cc/trees/layer_tree_host_impl.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2bbd2b7e0c4e0550628845e664ca0f959d4f3dfa

commit 2bbd2b7e0c4e0550628845e664ca0f959d4f3dfa
Author: Adrienne Walker <enne@chromium.org>
Date: Mon Aug 19 19:37:45 2019

cc: clip painting rects to the positive values

Layers start at the origin and not in negative space and we should
never need these values.  This prevents rtree complexity and
bounds overflow.

Bug: 988590
Change-Id: I4fa77c11fc5f0411997e2697291b9e554958c9f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1749703
Reviewed-by: Philip Rogers <pdr@chromium.org>
Commit-Queue: enne <enne@chromium.org>
Cr-Commit-Position: refs/heads/master@{#688210}

[modify] https://crrev.com/2bbd2b7e0c4e0550628845e664ca0f959d4f3dfa/cc/paint/display_item_list.h
[modify] https://crrev.com/2bbd2b7e0c4e0550628845e664ca0f959d4f3dfa/cc/paint/display_item_list_unittest.cc
[modify] https://crrev.com/2bbd2b7e0c4e0550628845e664ca0f959d4f3dfa/third_party/blink/renderer/platform/graphics/compositing/paint_chunks_to_cc_layer_test.cc


### en...@chromium.org (2019-08-19)

[Empty comment from Monorail migration]

### en...@chromium.org (2019-08-21)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8b967ae051605ec89a12fe2c9c59ec019722ddac

commit 8b967ae051605ec89a12fe2c9c59ec019722ddac
Author: enne <enne@chromium.org>
Date: Wed Aug 21 01:17:49 2019

Revert "cc: clip painting rects to the positive values"

This reverts commit 2bbd2b7e0c4e0550628845e664ca0f959d4f3dfa.

Reason for revert: record performance regressions

Original change's description:
> cc: clip painting rects to the positive values
> 
> Layers start at the origin and not in negative space and we should
> never need these values.  This prevents rtree complexity and
> bounds overflow.
> 
> Bug: 988590
> Change-Id: I4fa77c11fc5f0411997e2697291b9e554958c9f7
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1749703
> Reviewed-by: Philip Rogers <pdr@chromium.org>
> Commit-Queue: enne <enne@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#688210}

TBR=pdr@chromium.org,enne@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 988590,995751,995811,995898,995932
Change-Id: I5d582a6f70fa0285dd7f527461efbbe54d70499c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1762941
Reviewed-by: enne <enne@chromium.org>
Commit-Queue: enne <enne@chromium.org>
Cr-Commit-Position: refs/heads/master@{#688831}

[modify] https://crrev.com/8b967ae051605ec89a12fe2c9c59ec019722ddac/cc/paint/display_item_list.h
[modify] https://crrev.com/8b967ae051605ec89a12fe2c9c59ec019722ddac/cc/paint/display_item_list_unittest.cc
[modify] https://crrev.com/8b967ae051605ec89a12fe2c9c59ec019722ddac/third_party/blink/renderer/platform/graphics/compositing/paint_chunks_to_cc_layer_test.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3cd3ad223d3004b066281f76458b13df31c8dbc8

commit 3cd3ad223d3004b066281f76458b13df31c8dbc8
Author: Adrienne Walker <enne@chromium.org>
Date: Wed Aug 21 23:52:28 2019

cc: don't allow transparent quads for opaque layers

This is a DCHECK + workaround for https://crbug.com/chromium/988590.

https://chromium-review.googlesource.com/c/chromium/src/+/1749703
solves root of the problem, and will avoid this DCHECK for
this particular content.

Bug: 988590
Change-Id: I0e66ba388c11bbc3805ead42343d7fe7af7a79da
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1752873
Commit-Queue: enne <enne@chromium.org>
Reviewed-by: Khushal <khushalsagar@chromium.org>
Cr-Commit-Position: refs/heads/master@{#689250}

[modify] https://crrev.com/3cd3ad223d3004b066281f76458b13df31c8dbc8/cc/debug/debug_colors.cc
[modify] https://crrev.com/3cd3ad223d3004b066281f76458b13df31c8dbc8/cc/debug/debug_colors.h
[modify] https://crrev.com/3cd3ad223d3004b066281f76458b13df31c8dbc8/cc/layers/picture_layer_impl.cc


### en...@chromium.org (2019-08-22)

Given that there was a performance regression in https://crrev.com/2bbd2b7e0c4e0550628845e664ca0f959d4f3dfa, I think the correct patch to merge is the one in https://crbug.com/chromium/988590#c23 once it's baked a little.

### en...@chromium.org (2019-08-27)

Apparently the patch in https://crbug.com/chromium/988590#c23 causes bad visual bugs in https://crbug.com/chromium/997583, and so I'm reverting that too.

Recapping where we are, I think the options to address this original spoofing bug look like this:

(1) Somebody from ui team investigates why https://chromium-review.googlesource.com/c/chromium/src/+/1752873 caused black squares on a bluetooth overlay in https://crbug.com/chromium/997583.  This seems likely to be some ui layer that's claiming to be opaque but then isn't and probably needs to either say it isn't or clear itself.  Then reland that patch.

(2) Reland https://chromium-review.googlesource.com/c/chromium/src/+/1749703 and accept minor recording performance regressions, listed in https://crbug.com/chromium/995751, https://crbug.com/chromium/995811, https://crbug.com/chromium/995898, and https://crbug.com/chromium/995932.  It's not clear how real these are, but since I had another idea for how to address this https://crbug.com/chromium/988590, I just cautiously reverted rather than wasting too much time on it.

(3) Have cc's use of rtrees handle the case where overflow has happened on the bounds, and always return everything in the rtree for both solid color analysis and raster.  This is a little bit more of a complicated spot fix, but shouldn't be too difficult.

(4) If desperate for an easily mergeable fix for older versions, we could have GLRenderer (and other direct renderers?) always clear the back buffer to some color (like we clear blue for debug).


I'm going to hand this off to vmiura to triage and decide where to go from here.  I had hoped #1 would be a reasonable fix, but clearly it's more complicated.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/027e3983872fcd0f48badef935f59d641fdb10c4

commit 027e3983872fcd0f48badef935f59d641fdb10c4
Author: enne <enne@chromium.org>
Date: Tue Aug 27 20:08:45 2019

Revert "cc: don't allow transparent quads for opaque layers"

This reverts commit 3cd3ad223d3004b066281f76458b13df31c8dbc8.

Reason for revert: causes black squares on ui layers that lie about opaqueness

Original change's description:
> cc: don't allow transparent quads for opaque layers
> 
> This is a DCHECK + workaround for https://crbug.com/chromium/988590.
> 
> https://chromium-review.googlesource.com/c/chromium/src/+/1749703
> solves root of the problem, and will avoid this DCHECK for
> this particular content.
> 
> Bug: 988590
> Change-Id: I0e66ba388c11bbc3805ead42343d7fe7af7a79da
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1752873
> Commit-Queue: enne <enne@chromium.org>
> Reviewed-by: Khushal <khushalsagar@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#689250}

TBR=enne@chromium.org,khushalsagar@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: 988590,997583
Change-Id: Id5cb90d22b3b5bf070a8223d90a5fa30f958f12c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1773207
Reviewed-by: enne <enne@chromium.org>
Commit-Queue: enne <enne@chromium.org>
Cr-Commit-Position: refs/heads/master@{#690855}

[modify] https://crrev.com/027e3983872fcd0f48badef935f59d641fdb10c4/cc/debug/debug_colors.cc
[modify] https://crrev.com/027e3983872fcd0f48badef935f59d641fdb10c4/cc/debug/debug_colors.h
[modify] https://crrev.com/027e3983872fcd0f48badef935f59d641fdb10c4/cc/layers/picture_layer_impl.cc


### sh...@chromium.org (2019-08-28)

vmiura: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vm...@google.com (2019-08-28)

ericrk@ assigning to you as discussed offline.


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/05c7bb4df0f4674fa8b9e1fbf102a0bcfbfda622

commit 05c7bb4df0f4674fa8b9e1fbf102a0bcfbfda622
Author: Eric Karl <ericrk@chromium.org>
Date: Fri Aug 30 22:06:27 2019

Handle overflow in cc RTree

Updates the cc RTree class to handle overflow:
  - GetBounds becomes GetBoundsOrDie and can only be called when
    has_valid_bounds().
  - All other functions are unchanged, operating correctly, but less
    efficiently, when !has_valid_bounds().

Updates DisplayItemList to handle cases when !has_valid_bounds().

Bug: 988590
Change-Id: I8612c5e219a7aa9774fc24cb69372df975562bbc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1777049
Commit-Queue: Eric Karl <ericrk@chromium.org>
Reviewed-by: Philip Rogers <pdr@chromium.org>
Reviewed-by: enne <enne@chromium.org>
Cr-Commit-Position: refs/heads/master@{#692247}

[modify] https://crrev.com/05c7bb4df0f4674fa8b9e1fbf102a0bcfbfda622/cc/base/rtree.h
[modify] https://crrev.com/05c7bb4df0f4674fa8b9e1fbf102a0bcfbfda622/cc/base/rtree_unittest.cc
[modify] https://crrev.com/05c7bb4df0f4674fa8b9e1fbf102a0bcfbfda622/cc/paint/display_item_list.cc


### la...@google.com (2019-09-04)

ericrk@ - how is the CL doing on the Canary? Do you plan to bring it to M77?

### er...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-04)

Dropping this from M77. 

ericrk@ - please assign a new milestone target. Thanks.

### er...@chromium.org (2019-09-04)

I think it's best to roll out through M78

### er...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-05)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-06)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $500 for this report :)

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-20)

Not requesting merge to beta (M78) because latest trunk commit (692247) appears to be prior to beta branch point (693954). If this is incorrect, please replace the Merge-na label with Merge-Request-78. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### he...@gmail.com (2020-01-08)

Hey, per https://crbug.com/chromium/988590#c6 I think this is missing a CVE given it affected the stable version.

### he...@gmail.com (2021-07-27)

Don't mind this message, just checking whether it will be picked up by the new platform.

### is...@google.com (2021-07-27)

This issue was migrated from crbug.com/chromium/988590?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095850)*
