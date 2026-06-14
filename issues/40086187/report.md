# Security: Address spoofing when switching away from tab and back

| Field | Value |
|-------|-------|
| **Issue ID** | [40086187](https://issues.chromium.org/issues/40086187) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox>SecurityIndicators |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gn...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2016-12-09 |
| **Bounty** | $2,000.00 |

## Description

DESCRIPTION:  

Address spoofing in Omnibox

**VERSION**  

Chrome Version: Version 55.0.2883.75 (64-bit) stable  

Operating System: Ubuntu 16.04.1 LTS

Chrome Version: Version 54.0.2840.85 stable  

Operating System: Android 6.0.1

POC:

<http://192.243.113.21/spoof/chrome/url1.html>

## Attachments

- [Screenshot from 2016-12-09 22-59-39.png](attachments/Screenshot from 2016-12-09 22-59-39.png) (image/png, 22.6 KB)
- [Spoofing.png](attachments/Spoofing.png) (image/png, 19.3 KB)
- [spoof.html](attachments/spoof.html) (text/plain, 1.2 KB)
- [spoof-simplified.html](attachments/spoof-simplified.html) (text/plain, 1.1 KB)

## Timeline

### el...@chromium.org (2016-12-09)

Thanks for reporting!

This looks like some sort of race condition in navigation. It's reproducible in the current Canary 57.2945. I end up with a few random other tabs open, but the markup shown in the screenshot does appear. I can't get script to run if I put it in the injected HTML (when I try, Amazon actually loads), but if I query the document's location via devtools, it thinks it's on Amazon. The markup appears to be inactive (I can't select the fake text, for instance).

[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox>SecurityIndicators]

### wr...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### na...@chromium.org (2016-12-12)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-12-12)

Yes, looks like a real bug.  I can also repro in 57.0.2949.0 on Windows.  Source of the attack page is attached.

There's something strange going on in the renderer, since DevTools says document.body is null.  And yes, no way to select the text or interact with the spoofed page.

That said, there's no heavy CPU use after the spoof is visible, and the omnibox doesn't reset after switch tabs and back or hitting escape in the omnibox.  This will be worth looking at in a debugger.

[Monorail components: UI>Security>UrlFormatting]

### dc...@chromium.org (2016-12-13)

I'm not able to repro, but there are various ways to end up with a null document.body: it's possible to do something like document.documentElement.removeChild(document.body).

### sh...@chromium.org (2016-12-13)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-12-15)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-12-16)

Ok, I've narrowed this down to a simpler repro case, which is attached.  The bug is that switching away from a tab and coming back seems to break Ken's unresponsiveness timer from https://crbug.com/chromium/497588 (or rather, it somehow breaks the blank paint that happens after the timer fires).  Ken, can you take a look?

In more depth:

The attack page opens a popup and puts some content into it.  It starts navigating to amazon.com, but it interrupts that load immediately after it commits and (usually) before the first paint.  (It interrupts by navigating to URL with a 204 response: https://www.google.com/csi.)  Because amazon.com has already committed, we leave that in the address bar, but because there was no paint, the attacker's content is still there.

If you take out all the alerts, you can see Ken's unresponsiveness timer kick in after 4 seconds and paint the entire page white.  However, switching to another tab and back (which the alerts accomplish) makes the attacker's content visible again.

I strongly suspect this is also related to what's happening in https://crbug.com/chromium/648117, but I haven't verified that yet.

I'm also CC'ing dtapuska@, because this reliably shows an unresponsiveness dialog after 30 seconds when visited in a Linux debug build, despite the fact that the other tab in the same process is responsive.  I suspect this is one way to get to https://crbug.com/chromium/615090, where the renderer is killed for being unresponsive when it isn't, perhaps due to a missing ack somewhere.  (Note that I'm not seeing that dialog on Windows Canary.)

### sh...@chromium.org (2016-12-24)

kenrb: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2017-01-03)

Ken has started looking.  We're wondering if something is holding onto the old image after EvictDelegatedFrame is called, but he hasn't found anything yet.  So far, it's unclear how the old image comes back after we clear it in the unresponsiveness timer.

He said there's no new compositor frame coming up from the renderer, so perhaps there's something in the Surfaces code that keeps it around.  We'll keep looking.

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/efd1189a0b3febada2bceb4c037fff1718306a3a

commit efd1189a0b3febada2bceb4c037fff1718306a3a
Author: kenrb <kenrb@chromium.org>
Date: Fri Mar 03 14:44:13 2017

Discard compositor frames from unloaded web content

After a navigation commits, it is still possible for the compositor to
resend a frame that draws the previous (now unloaded) page. In some
situations this works against the browser process' new content
rendering timer that attempts to clear a page after 4 seconds if a
navigation has committed but not yet painted in that time.

This CL adds a counter called content_source_id to that increments on
every non-same-page navigation commit under a given top-level
RenderWidget. It tags the CompositorFrameMetadata with this identifier,
and also sends it to the browser process with the
DidCommitProvisionaLoad IPC message. This enables the browser to
recognize compositor frames with stale IDs, corresponding to unloaded
pages.

BUG=672847
CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel;master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2707243005
Cr-Commit-Position: refs/heads/master@{#454578}

[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/cc/ipc/cc_param_traits_macros.h
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/cc/ipc/compositor_frame_metadata.mojom
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/cc/ipc/compositor_frame_metadata_struct_traits.cc
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/cc/ipc/compositor_frame_metadata_struct_traits.h
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/cc/ipc/struct_traits_unittest.cc
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/cc/output/compositor_frame_metadata.h
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/cc/trees/layer_tree_host.cc
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/cc/trees/layer_tree_host.h
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/cc/trees/layer_tree_host_impl.cc
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/cc/trees/layer_tree_host_unittest.cc
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/cc/trees/layer_tree_impl.cc
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/cc/trees/layer_tree_impl.h
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/content/browser/renderer_host/render_widget_host_impl.cc
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/content/browser/renderer_host/render_widget_host_impl.h
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/content/browser/renderer_host/render_widget_host_unittest.cc
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/content/common/frame_messages.h
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/content/renderer/gpu/render_widget_compositor.cc
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/content/renderer/gpu/render_widget_compositor.h
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/content/renderer/render_widget.cc
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/content/renderer/render_widget.h
[modify] https://crrev.com/efd1189a0b3febada2bceb4c037fff1718306a3a/content/test/test_render_view_host.h


### ke...@chromium.org (2017-03-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cee456faba216e014f2ce2ded37e2cde5fc19cfd

commit cee456faba216e014f2ce2ded37e2cde5fc19cfd
Author: sclittle <sclittle@chromium.org>
Date: Sat Mar 04 00:57:08 2017

Revert of Discard compositor frames from unloaded web content (patchset #11 id:200001 of https://codereview.chromium.org/2707243005/ )

Reason for revert:
It looks like this broke the MSAN bot:

https://uberchromegw.corp.google.com/i/chromium.webkit/builders/WebKit%20Linux%20Trusty%20MSAN

https://uberchromegw.corp.google.com/i/chromium.webkit/builders/WebKit%20Linux%20Trusty%20MSAN/builds/731

Original issue's description:
> Discard compositor frames from unloaded web content
>
> After a navigation commits, it is still possible for the compositor to
> resend a frame that draws the previous (now unloaded) page. In some
> situations this works against the browser process' new content
> rendering timer that attempts to clear a page after 4 seconds if a
> navigation has committed but not yet painted in that time.
>
> This CL adds a counter called content_source_id to that increments on
> every non-same-page navigation commit under a given top-level
> RenderWidget. It tags the CompositorFrameMetadata with this identifier,
> and also sends it to the browser process with the
> DidCommitProvisionaLoad IPC message. This enables the browser to
> recognize compositor frames with stale IDs, corresponding to unloaded
> pages.
>
> BUG=672847
> CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel;master.tryserver.chromium.linux:linux_site_isolation
>
> Review-Url: https://codereview.chromium.org/2707243005
> Cr-Commit-Position: refs/heads/master@{#454578}
> Committed: https://chromium.googlesource.com/chromium/src/+/efd1189a0b3febada2bceb4c037fff1718306a3a

TBR=enne@chromium.org,creis@chromium.org,danakj@chromium.org,kenrb@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=672847

Review-Url: https://codereview.chromium.org/2730203002
Cr-Commit-Position: refs/heads/master@{#454732}

[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/cc/ipc/cc_param_traits_macros.h
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/cc/ipc/compositor_frame_metadata.mojom
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/cc/ipc/compositor_frame_metadata_struct_traits.cc
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/cc/ipc/compositor_frame_metadata_struct_traits.h
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/cc/ipc/struct_traits_unittest.cc
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/cc/output/compositor_frame_metadata.h
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/cc/trees/layer_tree_host.cc
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/cc/trees/layer_tree_host.h
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/cc/trees/layer_tree_host_impl.cc
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/cc/trees/layer_tree_host_unittest.cc
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/cc/trees/layer_tree_impl.cc
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/cc/trees/layer_tree_impl.h
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/content/browser/renderer_host/render_widget_host_impl.cc
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/content/browser/renderer_host/render_widget_host_impl.h
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/content/browser/renderer_host/render_widget_host_unittest.cc
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/content/common/frame_messages.h
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/content/renderer/gpu/render_widget_compositor.cc
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/content/renderer/gpu/render_widget_compositor.h
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/content/renderer/render_widget.cc
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/content/renderer/render_widget.h
[modify] https://crrev.com/cee456faba216e014f2ce2ded37e2cde5fc19cfd/content/test/test_render_view_host.h


### sh...@chromium.org (2017-03-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-05)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), bhthompson@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34

commit 5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34
Author: kenrb <kenrb@chromium.org>
Date: Mon Mar 06 21:06:01 2017

(Reland) Discard compositor frames from unloaded web content

This is a reland of https://codereview.chromium.org/2707243005/ with a
small change to fix an uninitialized memory error that fails on MSAN
bots.

BUG=672847
TBR=danakj@chromium.org, creis@chromium.org
CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel;master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2731283003
Cr-Commit-Position: refs/heads/master@{#454954}

[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/cc/ipc/cc_param_traits_macros.h
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/cc/ipc/compositor_frame_metadata.mojom
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/cc/ipc/compositor_frame_metadata_struct_traits.cc
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/cc/ipc/compositor_frame_metadata_struct_traits.h
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/cc/ipc/struct_traits_unittest.cc
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/cc/output/compositor_frame_metadata.h
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/cc/trees/layer_tree_host.cc
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/cc/trees/layer_tree_host.h
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/cc/trees/layer_tree_host_impl.cc
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/cc/trees/layer_tree_host_unittest.cc
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/cc/trees/layer_tree_impl.cc
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/cc/trees/layer_tree_impl.h
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/content/browser/renderer_host/render_widget_host_impl.cc
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/content/browser/renderer_host/render_widget_host_impl.h
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/content/browser/renderer_host/render_widget_host_unittest.cc
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/content/common/frame_messages.h
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/content/renderer/gpu/render_widget_compositor.cc
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/content/renderer/gpu/render_widget_compositor.h
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/content/renderer/render_widget.cc
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/content/renderer/render_widget.h
[modify] https://crrev.com/5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34/content/test/test_render_view_host.h


### sh...@chromium.org (2017-03-07)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-13)

Nice one!  The VRP panel decided to award $2,000 for this bug.

### aw...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-04-03)

I had cleared merge labels for this, perhaps in error. A merge has been approved anyway on https://crbug.com/chromium/648117, which happens to be also fixed by this CL, so it is going into the M58 branch anyway.

### bu...@chromium.org (2017-04-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728

commit 5aa9a4a70f65068dcc5d8b84ca42cb05fb380728
Author: Ken Buchanan <kenrb@chromium.org>
Date: Mon Apr 03 15:21:16 2017

(Reland) Discard compositor frames from unloaded web content

This is a reland of https://codereview.chromium.org/2707243005/ with a
small change to fix an uninitialized memory error that fails on MSAN
bots.

BUG=672847,648117
TBR=danakj@chromium.org, creis@chromium.org
CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel;master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2731283003
Cr-Commit-Position: refs/heads/master@{#454954}
(cherry picked from commit 5d78b84d39bd34bc9fce9d01c0dcd5a22a330d34)

Review-Url: https://codereview.chromium.org/2793013002 .
Cr-Commit-Position: refs/branch-heads/3029@{#547}
Cr-Branched-From: 939b32ee5ba05c396eef3fd992822fcca9a2e262-refs/heads/master@{#454471}

[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/cc/ipc/cc_param_traits_macros.h
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/cc/ipc/compositor_frame_metadata.mojom
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/cc/ipc/compositor_frame_metadata_struct_traits.cc
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/cc/ipc/compositor_frame_metadata_struct_traits.h
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/cc/ipc/struct_traits_unittest.cc
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/cc/output/compositor_frame_metadata.h
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/cc/trees/layer_tree_host.cc
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/cc/trees/layer_tree_host.h
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/cc/trees/layer_tree_host_impl.cc
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/cc/trees/layer_tree_host_unittest.cc
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/cc/trees/layer_tree_impl.cc
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/cc/trees/layer_tree_impl.h
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/content/browser/renderer_host/render_widget_host_impl.cc
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/content/browser/renderer_host/render_widget_host_impl.h
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/content/browser/renderer_host/render_widget_host_unittest.cc
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/content/common/frame_messages.h
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/content/renderer/gpu/render_widget_compositor.cc
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/content/renderer/gpu/render_widget_compositor.h
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/content/renderer/render_widget.cc
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/content/renderer/render_widget.h
[modify] https://crrev.com/5aa9a4a70f65068dcc5d8b84ca42cb05fb380728/content/test/test_render_view_host.h


### aw...@google.com (2017-04-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-19)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-04-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/672847?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox>SecurityIndicators, UI>Security>UrlFormatting]
[Monorail mergedwith: crbug.com/chromium/712024]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086187)*
