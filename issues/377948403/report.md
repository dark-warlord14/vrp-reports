# blank <select> and <optgroup> inside iframe can be drawn outside of iframe

| Field | Value |
|-------|-------|
| **Issue ID** | [377948403](https://issues.chromium.org/issues/377948403) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Compositing>Scroll |
| **Platforms** | Fuchsia, Linux, Mac, Windows |
| **Chrome Version** | 130.0.6723.116 |
| **Reporter** | tr...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2024-11-08 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Locate frame\_1920x1080.html and src.html to same directory
2. Open frame\_1920x1080.html, the grey box overflows outside of iframe

# Problem Description

Of the iframes placed in 3x3, only the iframe in the middle has src. The content that should only be drawn in this iframe is being drawn outside the iframe.
I haven't figured out how to turn a grey box into another shape since I don't know much about CSS, but I think it could be used for a variety of security attacks if it could be.

Not reproducible on chrome 129.0.6668.70

# Summary

blank <select> and <optgroup> inside iframe can be drawn outside of iframe

# Custom Questions

#### Reporter credit:

Dahyeon Park

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: Yes

## Attachments

- [frame_1920x1080.html](attachments/frame_1920x1080.html) (text/html, 1.0 KB)
- [screenshot.png](attachments/screenshot.png) (image/png, 69.9 KB)
- [src.html](attachments/src.html) (text/html, 226 B)
- [variations.txt](attachments/variations.txt) (text/plain, 96.2 KB)
- [bisect_result.txt](attachments/bisect_result.txt) (text/plain, 4.9 KB)
- [screencast.mp4](attachments/screencast.mp4) (video/mp4, 2.4 MB)

## Timeline

### wf...@chromium.org (2024-11-08)

I can't really reproduce this nor do I understand the implications.

I tried 132.0.6826.0, 130.0.6723.117 and also 129.0.6668.103 and they all look the same. I'm really not sure what I am even looking for here.

Can you provide instructions for how to determine that this issue is manifesting? Perhaps it would be possible for you to do a bisect if you can reliably reproduce, using the instructions here -> <https://www.chromium.org/developers/bisect-builds-py/>

### tr...@gmail.com (2024-11-09)

I realized that it only happens in 'chrome for testing' binaries, and I could reproduce with their latest stable & dev version.

### pe...@google.com (2024-11-09)

Thank you for providing more feedback. Adding the requester to the CC list.

### wf...@chromium.org (2024-11-11)

Thank you for your reply. I still don't really have enough information to understand the implications of this issue. Also, if this only affects Chrome for Testing then that is curious as there shouldn't be any differences there, but it would mean that this is not considered a security bug.

Are you able to run a bisect here?

### tr...@gmail.com (2024-11-12)

I was able to run bisect-builds.py and reproduce the bug. The result is attached as 'bisect_result.txt'.

And also I was able to reproduce the bug in latest canary build (1381164), which can be downloaded at (https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Linux_x64/1381164/). The screencast is also attached.

### pe...@google.com (2024-11-12)

Thank you for providing more feedback. Adding the requester to the CC list.

### ch...@chromium.org (2024-11-12)

I ran a bisect as well and came up with the same regression range for normal Chrome. The bug appears to be that the gray rectangle corresponding to the src.html frame is drawn outside the area it should be contained in (it extends to the left and right edges of the page). In Firefox 132.0.2 it does not extend past the area.

I'm not sure why this might be considered a security bug. It seems like the worst thing that could happen is the framed content can interfere with the appearance of adjacent content. I don't think this violates Chrome's security model (or the same origin policy, for example). Reporter, could you please clarify? (Setting needs-feedback and nextaction for reporter response to determine whether to downgrade to a normal Bug.)

Based on regression range from bisect, assigning to wangxianzhu@: Could you please review this issue? Your [crrev.com/c/5731972](https://crrev.com/c/5731972) seems to be the most suspicious looking change in the regression range.

### ch...@chromium.org (2024-11-12)

Setting Low severity provisionally, will reevaluate based on reporter's feedback.

### wa...@chromium.org (2024-11-12)

chlily@ can you share the regression range?

### wa...@chromium.org (2024-11-12)

Never mind [comment#10](https://issues.chromium.org/issues/377948403#comment10). I have confirmed the overflowing gray drawing is the scrollbar thumb. This doesn't reproduce with `--disable-features=AuraScrollbarUsesSolidColorThumb`, but reproduces regardless of AuraScrollbarUsesSolidColorThumb with `--enable-features=FluentScrollbar`.

### wa...@chromium.org (2024-11-12)

[+gastonr@microsoft.com](mailto:+gastonr@microsoft.com) because this also affects FluentScrollbar.

### wa...@chromium.org (2024-11-12)

Minimized test case:

```
<!DOCTYPE html>
<iframe srcdoc="
<select multiple style='transform: scale(500, 10)'>
  <optgroup style='height: 1000px'></optgroup>
</select>">
</iframe>

```

### tr...@gmail.com (2024-11-13)

#8 I reported this as a security related bug because I thought that if the gray box outside of the iframe can be changed into a different form (text, image, etc.), it would give the website user the wrong information. If changing this box to another shape is impossible, or if this type of bug isn't a security bug, I think it's right to be re-designated as a normal bug.

### pe...@google.com (2024-11-13)

Thank you for providing more feedback. Adding the requester to the CC list.

### pe...@google.com (2024-11-13)

The NextAction date has arrived: 2024-11-13
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ch...@chromium.org (2024-11-13)

Thanks for your feedback. Looks like the iframe can trigger this by itself (as opposed to requiring the outer frame to apply a CSS transform), so we can treat this as a security bug. It seems like this affects the content area only, but if it may also draw outside of the content area (e.g. covering up the omnibox) then the severity might need to be upgraded.

### wa...@chromium.org (2024-11-13)

The overflowing rendering can only be a rectangle, not possible to be other shapes. It can't draw outside of the content area.

This bug won't reproduce for cross-domain iframes if the iframe is isolated in a separate process.

### ap...@google.com (2024-11-13)

Project: chromium/src  

Branch: main  

Author: Xianzhu Wang <[wangxianzhu@chromium.org](mailto:wangxianzhu@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6014683>

Fix solid color thumb quad under large scale

---


Expand for full commit details
```
Fix solid color thumb quad under large scale 
 
If a layer has a large scale, visible_layer_rect() can't reliably 
clip a quad before scaling because a "pixel" in the layer is very 
large and scale-after-clip will create a quad exceeding the clip. 
 
clip 
  large-scale 
    layer 
 
Now share more code with the non-solid-color-thumb code path. 
 
For a AppendQuads method, to ensure the clip rect is applied, it's 
better to call PopulateScaledSharedQuadState() instead of creating a 
shared quad state by itself. 
 
Bug: 377948403 
Change-Id: I8d7dd08fe9fc7907685bfbaa1a5fd5682688aed0 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6014683 
Reviewed-by: Philip Rogers <pdr@chromium.org> 
Commit-Queue: Xianzhu Wang <wangxianzhu@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1382613}

```

---

Files:

- M `cc/layers/painted_scrollbar_layer_impl.cc`
- M `cc/layers/painted_scrollbar_layer_impl_unittest.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-overflow/scrollbar-large-scale-in-iframe-ref.html`
- A `third_party/blink/web_tests/external/wpt/css/css-overflow/scrollbar-large-scale-in-iframe.html`
- M `third_party/blink/web_tests/platform/linux/fast/sub-pixel/transformed-iframe-copy-on-scroll-expected.png`
- M `third_party/blink/web_tests/platform/win/fast/frames/iframe-scaling-with-scroll-expected.png`
- M `third_party/blink/web_tests/platform/win/fast/sub-pixel/transformed-iframe-copy-on-scroll-expected.png`

---

Hash: 4d86cee91c4307c8bb4fe2a8b6874b661482b179  

Date:  Wed Nov 13 22:17:29 2024


---

### pe...@google.com (2024-11-14)

The NextAction date has arrived: 2024-11-14
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ch...@chromium.org (2024-11-14)

Thanks for the speedy fix and for providing extra info in [comment #18](https://issues.chromium.org/issues/377948403#comment18).

I'm going to mark this as Fixed so our automation can follow up with next steps.

### pe...@google.com (2024-11-14)

\**This merge request uses Chrome's new merge process. Find more information at [go/chrome-merge-quickstart](http://go/chrome-merge-quickstart).*

M132 merge request created.

**Please update [crbug/379115680](https://crbug.com/379115680) to have this merge reviewed.**

### ap...@google.com (2024-11-15)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Xianzhu Wang <[wangxianzhu@chromium.org](mailto:wangxianzhu@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6025340>

Fix solid color thumb quad under large scale

---


Expand for full commit details
```
Fix solid color thumb quad under large scale 
 
If a layer has a large scale, visible_layer_rect() can't reliably 
clip a quad before scaling because a "pixel" in the layer is very 
large and scale-after-clip will create a quad exceeding the clip. 
 
clip 
  large-scale 
    layer 
 
Now share more code with the non-solid-color-thumb code path. 
 
For a AppendQuads method, to ensure the clip rect is applied, it's 
better to call PopulateScaledSharedQuadState() instead of creating a 
shared quad state by itself. 
 
(cherry picked from commit 4d86cee91c4307c8bb4fe2a8b6874b661482b179) 
 
Bug: 377948403 
Change-Id: I8d7dd08fe9fc7907685bfbaa1a5fd5682688aed0 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6014683 
Reviewed-by: Philip Rogers <pdr@chromium.org> 
Commit-Queue: Xianzhu Wang <wangxianzhu@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1382613} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6025340 
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Auto-Submit: Xianzhu Wang <wangxianzhu@chromium.org> 
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Cr-Commit-Position: refs/branch-heads/6834@{#236} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `cc/layers/painted_scrollbar_layer_impl.cc`
- M `cc/layers/painted_scrollbar_layer_impl_unittest.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-overflow/scrollbar-large-scale-in-iframe-ref.html`
- A `third_party/blink/web_tests/external/wpt/css/css-overflow/scrollbar-large-scale-in-iframe.html`
- M `third_party/blink/web_tests/platform/linux/fast/sub-pixel/transformed-iframe-copy-on-scroll-expected.png`
- M `third_party/blink/web_tests/platform/win/fast/frames/iframe-scaling-with-scroll-expected.png`
- M `third_party/blink/web_tests/platform/win/fast/sub-pixel/transformed-iframe-copy-on-scroll-expected.png`

---

Hash: b5ebac68ae8f622d27cc26d3a9abc72445c68c99  

Date:  Fri Nov 15 20:23:18 2024


---

### sp...@google.com (2024-11-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
baseline report of lower impact issue with potential for security UI spoof


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-28)

Thank you for your efforts and reporting this issue to us!

### am...@chromium.org (2024-11-28)

hello wangxianzhu@, thank you for resolving this issue. However, as a low severity security bug, this did not meet the qualifications for backmerge. [1] I noticed that this issue was altered from a vulnerability to bug then back to a vulnerability, which kicked allowed for the automation for non-security merges to be kicked off in c#22. Can you please provide context for the change from type-vulnerability to type-bug back to type-vulnerability again?
Thank you.

[1] <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/merge_request.md#Security-merge-triage>

### wa...@chromium.org (2024-11-28)

Vulnerability -> Bug: Based on [comment#8](https://issues.chromium.org/issues/377948403#comment8)

Bug -> Vulnerability: Based on [comment#17](https://issues.chromium.org/issues/377948403#comment17)

The merge to M-132 is because this is also a recent functionality regression, and the fix was just after the M-132 branch.

### pg...@google.com (2025-01-13)

This issue does not seem to be specific to Linux - adding other desktops as well, but please correct me if i am incorrect!

### ch...@google.com (2025-02-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/377948403)*
