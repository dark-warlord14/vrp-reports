# Security: FencedFrame - Two way communication between embedder and frame

| Field | Value |
|-------|-------|
| **Issue ID** | [40061164](https://issues.chromium.org/issues/40061164) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>FencedFrames |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | so...@gmail.com |
| **Assignee** | lb...@google.com |
| **Created** | 2022-09-27 |
| **Bounty** | $6,000.00 |

## Description

**VULNERABILITY DETAILS**

I don't know this is a real bug, or it's a normal behavior, or a known sidechannel attack for fencedframes. If it's not a bug, then sorry for the inconvenience.

I found 3 cases with fencedframe:

1. I can create two way communication channel between the fencedframe and the embedder. (cross site, localhost <=> 127.0.0.1). You can see this on the attached video and the 2 html (embedder and frame).
2. I can focus any focusable element (link, input, button) in the fenced frame from the embedder (change the frame.src. Eg. frame.src = frame.src+"#id" will set the focus to #id element)
3. I can check when an id is exists in the frame or not (with the frame.src+hash and onblur event. The embedder fires onblur when the frame element exists and receive the focus)

The #2 and #3 are known behavior for iframe, but it's a fenced frame.

**VERSION**  

Chrome Version: 105.0.5195.125 stable  

Operating System: 5.18.0-14parrot1-amd64 #1 SMP PREEMPT\_DYNAMIC Debian 5.18.14-1parrot1 (2022-08-07) x86\_64 GNU/Linux

**REPRODUCTION CASE**

I attached the embedder.html and the frame.html as POC for #1. In this poc the embedder can send (any valid js) command to the frame, the frame evals that command then returns the result bit by bit to the embedder.

For cross origin testing I used this urls:  

Embedder => <http://127.0.0.1:8000/embedder.html>  

Frame => <http://localhost:8000/frame.html>

1. The embedder set the frame.src hash to any value (need to set src twice) (eg to frame.html#aaa)  
   
   2, The embedder stores the current timestamp
2. The frame detects onhashchange, and creates an input and sets it's id to this new hash value (aaa)
3. The frame starts a setTimeout(()=>document.location=document.location,millis). This will focus the input after millis time. The data is "encoded" into the length of the time.  
   
   5- When the input focused the frame removes the input (onfocus -> removechild)
4. The embedder receives the onblur event when the input focused in the frame. It's calculates the time beetween the src change and the onblur event. Here is the data, eg. 100-200ms = 0, 200-300 ms = 1, 500ms+ end of data.
5. The embedder creates an input with any id (eg. bbb)
6. The embedder calls an child iframe for change the embedder location with the new input id in the hash (embedder.html#bbb) (maybe can done without an iframe, but only this worked for me)
7. The embedder receives the focus from the frame
8. The embedder removes the input
9. Again from 1 for next bit until all bits are received

This POC works with fencedframe, but not for iframe. I don't know why it's not working with iframe, but it's only a side note, the fencedframe is the main target.

You can see it in action on the attached video.

2nd and 3rd case:

You need just change the fencedframe src to focus any element in the frame. And you can search for any id with the onblur event. This was my original poc, #1 bornt from this.

The focus.html shows how to scan a fenced frame for id-s and how to focus an element in the frame from outside (a link in this POC). This file for #2 and #3. I didn't create video for this cases. This is a simple code, I can't give better description than my code.

Sorry if something is not clear, this is my first ticket here and english is not my main language, but you can reach me anytime to clarify things.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: -  

Crash State: -

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Peter Nemeth - [sokkis@gmail.com](mailto:sokkis@gmail.com)

## Attachments

- [output.mp4](attachments/output.mp4) (video/mp4, 2.3 MB)
- [embedder.html](attachments/embedder.html) (text/plain, 4.8 KB)
- [frame.html](attachments/frame.html) (text/plain, 1.9 KB)
- [focus.html](attachments/focus.html) (text/plain, 1.5 KB)
- [index2.html](attachments/index2.html) (text/plain, 382 B)
- [2022-09-30 16-11-00.mp4](attachments/2022-09-30 16-11-00.mp4) (video/mp4, 641.5 KB)
- [2022-09-30 17-28-23.mp4](attachments/2022-09-30 17-28-23.mp4) (video/mp4, 715.8 KB)
- [embedder.html](attachments/embedder.html) (text/plain, 4.5 KB)
- [frame.html](attachments/frame.html) (text/plain, 2.4 KB)
- [Screen Shot 2022-09-30 at 9.57.05 AM.png](attachments/Screen Shot 2022-09-30 at 9.57.05 AM.png) (image/png, 189.4 KB)
- [embedder.html](attachments/embedder.html) (text/plain, 4.1 KB)
- [frame.html](attachments/frame.html) (text/plain, 2.8 KB)

## Timeline

### [Deleted User] (2022-09-27)

[Empty comment from Monorail migration]

### so...@gmail.com (2022-09-28)

Sorry, yesterday I missed this file. This is a simple html file and this is the frame of the focus.html poc.

### mp...@chromium.org (2022-09-30)

I'm not a fenced frame expert but it looks like possible issues with handling the # hash. dom@ can you PTAL?

[Monorail components: Blink>FencedFrames]

### [Deleted User] (2022-09-30)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-09-30)

Thanks for filing sokkis@! From running this locally, it seems like the attack in the demo is only possible when fenced frames are enabled with the ShadowDOM architecture via chrome://flags/#enable-fenced-frames, and not "multiple page architecture". Is that right? If these attacks aren't possible with MPArch, then I think that is OK since we're currently not using ShadowDOM architecture in the wild anymore, and are removing it entirely very soon https://chromium-review.googlesource.com/c/chromium/src/+/3918971.

### do...@chromium.org (2022-09-30)

+gtanzer@ for same-document FF navigations
+lbrady@ for focus stuff

### so...@gmail.com (2022-09-30)

Hi dom@,
Thank you for reply. I thnk I can reproduce with MPArch. Please check this video to verfiy my thesis.

(Can make a confusion that my code don't work if you load the page with a #hash in the url. I only append a hash and this makes error if any hash previusly exists in the main url)

### so...@gmail.com (2022-09-30)

But, wait.
It works only with 105. I updated chrome to 106.0.5249.61, and now my POC is not working, something fixed this in the 106. :-)
So, the problem solved, I think you can close this ticket.

### gt...@chromium.org (2022-09-30)

Same-document navigations through frame.src were disabled in MPArch with this CL, which is in effect from M106 onwards: https://chromium-review.googlesource.com/c/chromium/src/+/3785109

I believe this explains why Dom was only able to reproduce the issue for ShadowDOM locally (he was probably using Canary, which is M108), vs. M105 here.

In terms of why it works in fenced frames but not iframes, that might be a different in focus behavior; I'll defer to Liam.

### so...@gmail.com (2022-09-30)

Oh, I'm sorry, I am tired and slow today. (Was a teambuilding event at night :) )
Here is my new verson, optimized for 106. :D It works like a charm.
The frame now listen for onload event, and the embedder always sends the command to the frame. :)

### [Deleted User] (2022-09-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-30)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lb...@chromium.org (2022-09-30)

I was able to get your demo to work with iframes. This is on MacOS in both Stable 105.0.5195.125 and Canary 108.0.5330.0.

So it looks like iframes and fenced frames are both happily working with the FragmentAnchor class (I don't think we ever audited the FragmentAnchor path specifically, but I remember discussions in the past on URL restrictions).

It also looks like this focus pulling can happen with opaque-ads fenced frames as well, and I think this will bypass k-anonymity checks since the navigation is coming from within the frame after it loads. And with this, the embedding page can also pull focus out of a fenced frame without user activation.

Question for the team:
Are there legitimate use cases for URL fragments inside fenced frames? My first thought would be to not allow the `#id` part of a URL to do anything. But I think we're touching upon the larger url restrictions debate at this point.

### so...@gmail.com (2022-09-30)

And my last version for today. With this version, I was able to avoid reloading the frame at every data bit.

The problem is that the fencedframe can navigate itself to different hashes, thereby gaining focus, and the embedder can, by definition, do anything, so can obtain the focus anytime. The focus is the key, the frame can obtain the focus programmatically, without interaction.

Since with this method it is possible to create a protocol in which the master is changed after every request (it's sounds funny, but really, it's a simple 1 wire serial line with fixed baud rate and timing), this reload after every request can also be eliminated, since not only the embedder can receive data with the focus-blur time, but also the frame, they just need to know who is next in line who can ask the other, eg. they can communicate alternately. If I have time on the weekend, I'll do it just for fun. :D

### so...@gmail.com (2022-09-30)

I missed my proposal: don't allow the FF to change itself the hash or/and don't change the focus if the hash changed programmatically (with location).
Also as I see, not only the FF can change itself the hash, if I put a child FF into the FF, then also this can change the location and the hash of its parent. The fix in 106, what killed my original poc only prevents the embedder to make change, but not the FF or its children, so its easy to get around, this is why I can do a working poc for the 106 version. 
But the good news is that the #2 and #3 cases are resolved, so only the #1, the comminication channel is remaining.

### dx...@google.com (2022-09-30)

[Empty comment from Monorail migration]

### dx...@google.com (2022-10-04)

hey Dom, we are reviewing this on a weekly basis. If this is not needed in M107, can we move it out asap. thanks! 

### do...@chromium.org (2022-10-04)

[Empty comment from Monorail migration]

### lb...@chromium.org (2022-10-04)

[Empty comment from Monorail migration]

### lb...@google.com (2022-10-06)

[Empty comment from Monorail migration]

### dx...@google.com (2022-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-07)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lb...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2022-10-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/855a43d7acc395d80c3932d382061ade2c82626e

commit 855a43d7acc395d80c3932d382061ade2c82626e
Author: Liam Brady <lbrady@google.com>
Date: Thu Oct 20 21:37:34 2022

Fenced frame: have anchor focus require user activation

Currently, focus can be pulled across a fenced frame boundary without
any user activation by using anchor fragments (aka setting location.href
to a.com#anchor). We already have script-based focus properly gated, but
this is a corner case that we missed.

This CL adds a new variable to FocusParams(): `gate_on_user_activation`.
If set to true, then focus that crosses a fenced frame boundary will
only be allowed to happen if the target frame has transient user
activation. This check takes place in
`Frame::AllowFocusWithoutUserActivation()`.

This CL also updates the Focus() call in
`ElementFragmentAnchor::ApplyFocusIfNeeded` to set
`gate_on_user_activation` to true. This has the effect of treating
anchor focusing as a programmatic focus. However, there isn't a
legitimate use case where a fenced frame will need to pull focus into
itself without user gesture using anchor focusing, and, the behavior
will remain unchanged for anchor focusing that does not cross a fenced
frame boundary. So, it's okay to add this restriction.

Bug: 1368739
Change-Id: Ia25e96e23e19d780ac8a4c8edb60c0b2472a9e18
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3933078
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Commit-Queue: Liam Brady <lbrady@google.com>
Cr-Commit-Position: refs/heads/main@{#1061827}

[modify] https://crrev.com/855a43d7acc395d80c3932d382061ade2c82626e/third_party/blink/renderer/core/frame/frame.cc
[modify] https://crrev.com/855a43d7acc395d80c3932d382061ade2c82626e/third_party/blink/renderer/core/page/focus_controller.cc
[modify] https://crrev.com/855a43d7acc395d80c3932d382061ade2c82626e/third_party/blink/renderer/core/frame/dom_window.cc
[modify] https://crrev.com/855a43d7acc395d80c3932d382061ade2c82626e/third_party/blink/renderer/core/dom/element.h
[add] https://crrev.com/855a43d7acc395d80c3932d382061ade2c82626e/third_party/blink/web_tests/wpt_internal/fenced_frame/anchor-focus.https.html
[modify] https://crrev.com/855a43d7acc395d80c3932d382061ade2c82626e/third_party/blink/renderer/core/page/scrolling/element_fragment_anchor.cc
[modify] https://crrev.com/855a43d7acc395d80c3932d382061ade2c82626e/third_party/blink/renderer/core/dom/focus_params.h
[modify] https://crrev.com/855a43d7acc395d80c3932d382061ade2c82626e/third_party/blink/renderer/core/dom/element.cc
[modify] https://crrev.com/855a43d7acc395d80c3932d382061ade2c82626e/third_party/blink/renderer/core/frame/frame.h


### so...@gmail.com (2022-10-21)

I retested my poc with this changes on the head and I can't do workaround to communicate. The fix is working.

Thank you for fixing!

Peter

### lb...@google.com (2022-10-21)

[Empty comment from Monorail migration]

### lb...@google.com (2022-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-21)

Merge approved: your change passed merge requirements and is auto-approved for M108. Please go ahead and merge the CL to branch 5359 (refs/branch-heads/5359) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2fdf7e8916a23145ceffd9da92c1a8e5a5f5e85e

commit 2fdf7e8916a23145ceffd9da92c1a8e5a5f5e85e
Author: Liam Brady <lbrady@google.com>
Date: Fri Oct 21 23:50:32 2022

Fenced frame: have anchor focus require user activation

Currently, focus can be pulled across a fenced frame boundary without
any user activation by using anchor fragments (aka setting location.href
to a.com#anchor). We already have script-based focus properly gated, but
this is a corner case that we missed.

This CL adds a new variable to FocusParams(): `gate_on_user_activation`.
If set to true, then focus that crosses a fenced frame boundary will
only be allowed to happen if the target frame has transient user
activation. This check takes place in
`Frame::AllowFocusWithoutUserActivation()`.

This CL also updates the Focus() call in
`ElementFragmentAnchor::ApplyFocusIfNeeded` to set
`gate_on_user_activation` to true. This has the effect of treating
anchor focusing as a programmatic focus. However, there isn't a
legitimate use case where a fenced frame will need to pull focus into
itself without user gesture using anchor focusing, and, the behavior
will remain unchanged for anchor focusing that does not cross a fenced
frame boundary. So, it's okay to add this restriction.

(cherry picked from commit 855a43d7acc395d80c3932d382061ade2c82626e)

Bug: 1368739
Change-Id: Ia25e96e23e19d780ac8a4c8edb60c0b2472a9e18
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3933078
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Commit-Queue: Liam Brady <lbrady@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1061827}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3971895
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Dominic Farolino <dom@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#196}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/2fdf7e8916a23145ceffd9da92c1a8e5a5f5e85e/third_party/blink/renderer/core/frame/frame.cc
[modify] https://crrev.com/2fdf7e8916a23145ceffd9da92c1a8e5a5f5e85e/third_party/blink/renderer/core/page/focus_controller.cc
[modify] https://crrev.com/2fdf7e8916a23145ceffd9da92c1a8e5a5f5e85e/third_party/blink/renderer/core/frame/dom_window.cc
[modify] https://crrev.com/2fdf7e8916a23145ceffd9da92c1a8e5a5f5e85e/third_party/blink/renderer/core/dom/element.h
[modify] https://crrev.com/2fdf7e8916a23145ceffd9da92c1a8e5a5f5e85e/third_party/blink/renderer/core/page/scrolling/element_fragment_anchor.cc
[add] https://crrev.com/2fdf7e8916a23145ceffd9da92c1a8e5a5f5e85e/third_party/blink/web_tests/wpt_internal/fenced_frame/anchor-focus.https.html
[modify] https://crrev.com/2fdf7e8916a23145ceffd9da92c1a8e5a5f5e85e/third_party/blink/renderer/core/dom/focus_params.h
[modify] https://crrev.com/2fdf7e8916a23145ceffd9da92c1a8e5a5f5e85e/third_party/blink/renderer/core/dom/element.cc
[modify] https://crrev.com/2fdf7e8916a23145ceffd9da92c1a8e5a5f5e85e/third_party/blink/renderer/core/frame/frame.h


### lb...@google.com (2022-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-24)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-24)

[Empty comment from Monorail migration]

### gm...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations, Peter! The VRP Panel has decided to award you $5,000 for this report + $1,000 bisect bonus. Nice finding and report! A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### so...@gmail.com (2022-11-03)

Thank you very much! I am glad that this report was useful.

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1368739?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061164)*
