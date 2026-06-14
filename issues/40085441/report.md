# Security: Address bar spoof with location.replace()

| Field | Value |
|-------|-------|
| **Issue ID** | [40085441](https://issues.chromium.org/issues/40085441) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2016-09-19 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 55.0.2864.0 canary (64-bit)  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Launch chrome and navigate to index.html
2. Click on the button
3. Click on "Back to safety" which is on the interstitial page and wait
4. Observe

## Attachments

- [ScreenShot.png](attachments/ScreenShot.png) (image/png, 41.1 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [PoC.rar](attachments/PoC.rar) (application/octet-stream, 504 B)
- [Recording URL-Spoofing.mp4](attachments/Recording URL-Spoofing.mp4) (video/mp4, 457.6 KB)

## Timeline

### ch...@gmail.com (2016-09-19)

[Empty comment from Monorail migration]

### el...@chromium.org (2016-09-19)

[Comment Deleted]

[Monorail components: UI>Browser>Omnibox>OriginChip]

### el...@chromium.org (2016-09-19)

This looks like a variant of e.g. 643173 which should be fixed already.

I'm was able to reproduce with 55.2865 for a split second; 55.2864 has some known bugs around the origin chip e.g. 647803. 

### el...@chromium.org (2016-09-19)

Oh, interesting. This repros in 53.2785 and 54.2840 as well, and when you use "Back to safety" the spoofed content lives indefinitely.

So this is not related to recent changes. 

The mis-attributed HTML does appear to be non-interactive (I can't select text in it, for instance) limiting it somewhat but it could contain static spoofing content. Interestingly, if I open the developer tools, they show markup from Twitter, suggesting that maybe what's happening is the spoof content is somehow living in the interstitial and overlaying the victim site.

[Monorail components: Security>UX]

### el...@chromium.org (2016-09-19)

[Comment Deleted]

### pe...@chromium.org (2016-09-19)

Feel free assign to an appropriate owner Eric.

### sh...@chromium.org (2016-09-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-04)

elawrence: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2016-10-04)

Any updates?

### el...@chromium.org (2016-10-05)

creis@ - Any chance we've got an expert on interstitials that may know what's going on here before I dive in to try to figure it out?

### fe...@chromium.org (2016-10-05)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### cr...@chromium.org (2016-10-05)

Interstitials are in need of an owner, sadly.  Nasko, Mustafa, and I know them enough to help, though we're a bit starved for time at the moment.  We can help with suggestions or you can assign it to one of us for when we get a chance.

### cr...@chromium.org (2016-10-17)

Avi, would you be able to help investigate this one?

### sh...@chromium.org (2016-10-20)

elawrence: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2016-11-21)

Apologies-- I unfortunately haven't made any progress with this, so passing it along per https://crbug.com/chromium/648117#c13.

### lg...@chromium.org (2016-11-23)

[Empty comment from Monorail migration]

[Monorail components: -Security>UX UI>Security>UrlFormatting]

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-12-09)

Any updates on this bug?

### cr...@chromium.org (2016-12-12)

Sorry, I missed the reassignment.  I'll try to take a look this week.

At first glance, this looks similar to what's happening in https://crbug.com/chromium/672847, where the spoofed content can't be interacted with, and DevTools shows that document.body is null.  I'll see if I can find what's going on, and what's common between the two.

### cr...@chromium.org (2016-12-16)

Ken: I'm pretty sure this is the same bug as https://crbug.com/chromium/672847, and that it's due to a bug in the unresponsiveness timer from https://crbug.com/chromium/497588.  

Specifically, if you click "Back to Safety" between 2 and 4 seconds after the twitter.com popup appears, you'll see "Address Spoofing" disappear due to the unresponsiveness timer.  If you minimize the popup and show it again, "Address Spoofing" will come back.

If you're able to get a fix for https://crbug.com/chromium/672847, can you check whether it fixes this as well?

### ke...@chromium.org (2016-12-28)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-01-23)

Any updates?

### ke...@chromium.org (2017-01-23)

I haven't had time to work on this yet, but expect to in the near future.

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### ji...@chromium.org (2017-03-21)

[Empty comment from Monorail migration]

### ji...@chromium.org (2017-03-24)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-03-25)

Fixed per https://codereview.chromium.org/2702433002. Please read c#20 and c#21.

Charlie, Ken - can you double-check?

### ke...@chromium.org (2017-03-27)

Ah, thanks for calling it out. It looks like my patch did fix this, although I had not properly diagnosed what was happening here and I forgot to check after the fact.

Your approach is quite a bit different from how https://crbug.com/chromium/672847 worked, but the timer mechanism has now been made a lot more robust now and should be resilient to loopholes like this now. Thanks for the submission!

### sh...@chromium.org (2017-03-28)

[Empty comment from Monorail migration]

### ke...@chromium.org (2017-03-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-31)

Your change meets the bar and is auto-approved for M58. Please go ahead and merge the CL to branch 3029 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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


### aw...@google.com (2017-04-04)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-10)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-10)

Thanks for the report - the panel decided to award $500 for this bug.

### aw...@chromium.org (2017-04-10)

[Empty comment from Monorail migration]

### aw...@google.com (2017-04-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-04-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/648117?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Navigation, UI>Security>UrlFormatting]
[Monorail mergedwith: crbug.com/chromium/664750, crbug.com/chromium/676840, crbug.com/chromium/704537]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085441)*
