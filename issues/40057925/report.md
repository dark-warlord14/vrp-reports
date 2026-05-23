# Security: FencedFrames reachable from compromised renderer due to lacking features::isEnabled(kFencedFrames) checks in Browser Process and FencedFrame::Navigate can navigate to file:// and chrome:// origins

| Field | Value |
|-------|-------|
| **Issue ID** | [40057925](https://issues.chromium.org/issues/40057925) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>FencedFrames, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | bt...@gmail.com |
| **Assignee** | do...@chromium.org |
| **Created** | 2021-11-15 |
| **Bounty** | $17,000.00 |

## Description

**VULNERABILITY DETAILS**  

Two separate issues here. The first issue makes the second issue reachable on stable.

<https://crbug.com/chromium/1>  

FencedFrames are enabled behind the feature flag blink::features::kFencedFrames [1]. However, this feature flag is only checked in the renderer process, and not in the Browser Process while handling the mojo IPC CreateFencedFrame [2] allowing a compromised renderer can create MParch FencedFrames.

<https://crbug.com/chromium/2>  

MParch fenced frames implement a a single mojo method FencedFrame::Navigate. This method takes a GURL and passes it to NavigateFromFrameProxy without first calling GetProcess()->FilterURL on the renderer supplied url.

void FencedFrame::Navigate(const GURL& url) { /\* url from mojo \*/  

FrameTreeNode\* inner\_root = frame\_tree\_->root();  

blink::NavigationDownloadPolicy download\_policy;

const blink::LocalFrameToken initiator\_frame\_token =  

owner\_render\_frame\_host\_->GetFrameToken();  

inner\_root->navigator().NavigateFromFrameProxy( /\* Navigate \*/  

inner\_root->current\_frame\_host(), url, &initiator\_frame\_token,  

owner\_render\_frame\_host\_->GetProcess()->GetID(),  

owner\_render\_frame\_host\_->GetLastCommittedOrigin(),  

owner\_render\_frame\_host\_->GetSiteInstance(), content::Referrer(),  

ui::PAGE\_TRANSITION\_LINK,  

/\*should\_replace\_current\_entry=\*/true, download\_policy, "GET",  

/\*post\_body=\*/nullptr, /\*extra\_headers=\*/"",  

/\*blob\_url\_loader\_factory=\*/nullptr,  

network::mojom::SourceLocation::New(), /\*has\_user\_gesture=\*/false,  

absl::nullopt);  

}  

This allows a compromised renderer to navigate to file:// and chrome:// urls.

Note: when the feature flag FencedFrame/mparch is enabled this is reachable without a compromised renderer, however issue #1 makes this reachable from a compromised renderer even without that feature flag making this reachable on Stable from a compromised renderer.

From here the attacker can download an html file and then navigate to it in the file:// scheme resulting in an arbitrary file read (387033 && 996741).

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/common/features.cc;l=201;drc=1eb643c3057e64ff4d22468432ad16c4cab12879>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_frame_host_impl.cc;l=6886;drc=06cb60827cd585fca133e1acff65e5c576eb9692>

**VERSION**  

Chromium 96.0.4664.45 (x64.release Build) (x86\_64)  

Chromium head 38e201c9e8f00fe15d8c6a3203188f0698f08567 (x64.release Build) (x86\_64)  

OS: Ubuntu 18.04

**REPRODUCTION CASE**  

Apply renderer\_96\_0\_4664\_45.patch to 96.0.4664.45  

Run the webserver and browse to <https://localhost:8080/> (./out/x64.release/chrome --disk-cache-dir=/dev/null --disk-cache-size=1 --window-size=1200,1200 <http://localhost:8080>)  

Note: Same steps work for renderer\_cf0b23fa66619b63b2212606cd225be15f04fe05.patch for reproducing on head.  

Quick Repro Explainer: The attacker renderer process patch doesn't modify any of the feature flag values. It just appends an MPArch iframe to the document whenever document.title is set to "pwn" (simulating a comkpromised renderer).

## Attachments

- [25_fenced_frames.tar.gz](attachments/25_fenced_frames.tar.gz) (application/octet-stream, 2.1 KB)
- [renderer_96_0_4664_45.patch](attachments/renderer_96_0_4664_45.patch) (text/plain, 6.9 KB)
- [renderer_head.patch](attachments/renderer_head.patch) (text/plain, 7.0 KB)
- [repro.png](attachments/repro.png) (image/png, 57.9 KB)
- [repro.diff](attachments/repro.diff) (text/plain, 8.2 KB)
- [before.png](attachments/before.png) (image/png, 597.2 KB)
- [after.png](attachments/after.png) (image/png, 560.4 KB)

## Timeline

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

[Monorail components: Blink>FencedFrames]

### ts...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### bt...@gmail.com (2021-11-15)

Sorry took a while to build, but here's a patch that applies cleanly on head 38e201c9e8f00fe15d8c6a3203188f0698f08567.

I think it's also worth mentioning that it doesn't matter what the value of blink::features::kFencedFrames is for these reproductions because it is not checked in the browser process for MParch fenced frames. Meaning `kSetOnlyIfOverridden` doesn't play a role in guarding this (i.e. I'm not running with web runtime features enabled).

### bt...@gmail.com (2021-11-15)

Also, this is what the browser should look like when running the reproduction. To navigate to some other chrome:// or file:// origin do something like this in devtools

```
document.body.getElementsByTagName("fencedframe")[0].src = "file:///etc/passwd";
document.body.getElementsByTagName("fencedframe")[0].src = "chrome://history";
document.body.getElementsByTagName("fencedframe")[0].src = "chrome://crash";
...
```

### cr...@chromium.org (2021-11-16)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation UI>Browser>Navigation]

### bt...@gmail.com (2021-11-19)

Uploaded a CL here if anyone else on this issue wants to take a look: https://chromium-review.googlesource.com/c/chromium/src/+/3285267

### do...@chromium.org (2021-11-19)

Just to keep everybody updated here, I'm working with btiszka@ on helping him get his CL above landed ^. The actual code change is pretty easy and mostly involves:
 - Turning the feature off by default to be more considerate to the gap in between now and the Origin Trial
 - Checking that the FencedFrames feature is enabled from the browser process, and that its feature param is MAPrch

The CL has been tricky due to the complexity of the VirtualTestSuites configuration and expectations (which btiszka@ is not very familiar with), but I think we have a handle on it now.

This will protect fenced frames being used by compromised renderers in general, and as a follow-up I'm working on crbug.com/1243568 which will restrict which kinds of URLs a fenced frame is allowed to navigate to. crbug.com/1243568 has been filed long before this bug was just to let people know that we are aware fenced frames can currently navigate to URLs that it shouldn't be allowed to -- it's just that the impl isn't complete yet.

### [Deleted User] (2021-12-04)

dom: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/874303093082ebf6c83ca7f650b41de1af6615bb

commit 874303093082ebf6c83ca7f650b41de1af6615bb
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Tue Dec 07 20:53:49 2021

Ensure the FencedFrames feature is enabled when handling mojo ipc

R=dom@chromium.org
R=linnan@chromium.org
R=lukasza@chromium.org

Bug: 1270358
Change-Id: Ib70fe27b97cda58caf8915e1d86ac7253b25ac76
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3285267
Reviewed-by: Dominic Farolino <dom@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#949142}

[add] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/fenced_frame/basic-expected.html
[modify] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/content/browser/bad_message.h
[modify] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/third_party/blink/common/features.cc
[modify] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/third_party/blink/web_tests/TestExpectations
[add] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/README.md
[rename] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/navigate-by-name-expected.txt
[modify] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/tools/metrics/histograms/enums.xml
[add] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/prerender.https-expected.txt
[modify] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/chrome/browser/extensions/api/declarative_net_request/declarative_net_request_browsertest.cc
[modify] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/third_party/blink/web_tests/webexposed/element-instance-property-listing-expected.txt
[modify] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/third_party/blink/web_tests/webexposed/global-interface-listing-expected.txt
[modify] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/content/browser/renderer_host/render_frame_host_impl.cc
[add] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/fenced_frame/visibility-changed-expected.html
[modify] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/third_party/blink/web_tests/VirtualTestSuites
[modify] https://crrev.com/874303093082ebf6c83ca7f650b41de1af6615bb/content/browser/security_exploit_browsertest.cc


### gi...@appspot.gserviceaccount.com (2021-12-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851

commit 4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851
Author: Jiewei Qian <qjw@chromium.org>
Date: Wed Dec 08 00:26:10 2021

Revert "Ensure the FencedFrames feature is enabled when handling mojo ipc"

This reverts commit 874303093082ebf6c83ca7f650b41de1af6615bb.

Reason for revert: Speculative reverting for breaking Win10 / Win7 bots

Sample failures:
https://ci.chromium.org/p/chromium/builders/ci/WebKit%20Win10/92320
https://ci.chromium.org/p/chromium/builders/ci/Win10%20Tests%20x64/61648
https://ci.chromium.org/p/chromium/builders/ci/Win7%20Tests%20%281%29/121593

Bug:1270358

Original change's description:
> Ensure the FencedFrames feature is enabled when handling mojo ipc
>
> R=​dom@chromium.org
> R=​linnan@chromium.org
> R=​lukasza@chromium.org
>
> Bug: 1270358
> Change-Id: Ib70fe27b97cda58caf8915e1d86ac7253b25ac76
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3285267
> Reviewed-by: Dominic Farolino <dom@chromium.org>
> Reviewed-by: Reilly Grant <reillyg@chromium.org>
> Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> Reviewed-by: Daniel Cheng <dcheng@chromium.org>
> Reviewed-by: Koji Ishii <kojii@chromium.org>
> Commit-Queue: Daniel Cheng <dcheng@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#949142}

Bug: 1270358
Change-Id: I35f91ec19ad4cebf9a7e652cf0722a71606c4b9d
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3320770
Auto-Submit: Jiewei Qian <qjw@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Jiewei Qian <qjw@chromium.org>
Owners-Override: Jiewei Qian <qjw@chromium.org>
Cr-Commit-Position: refs/heads/main@{#949266}

[delete] https://crrev.com/c0a28c56cddfcb6c8e0796d07189633b350c7deb/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/fenced_frame/basic-expected.html
[modify] https://crrev.com/4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851/content/browser/bad_message.h
[modify] https://crrev.com/4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851/third_party/blink/common/features.cc
[modify] https://crrev.com/4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851/third_party/blink/web_tests/TestExpectations
[delete] https://crrev.com/c0a28c56cddfcb6c8e0796d07189633b350c7deb/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/README.md
[modify] https://crrev.com/4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851/tools/metrics/histograms/enums.xml
[delete] https://crrev.com/c0a28c56cddfcb6c8e0796d07189633b350c7deb/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/prerender.https-expected.txt
[modify] https://crrev.com/4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851/chrome/browser/extensions/api/declarative_net_request/declarative_net_request_browsertest.cc
[rename] https://crrev.com/4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851/third_party/blink/web_tests/wpt_internal/fenced_frame/navigate-by-name-expected.txt
[modify] https://crrev.com/4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851/third_party/blink/web_tests/webexposed/element-instance-property-listing-expected.txt
[modify] https://crrev.com/4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851/third_party/blink/web_tests/webexposed/global-interface-listing-expected.txt
[modify] https://crrev.com/4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851/content/browser/renderer_host/render_frame_host_impl.cc
[delete] https://crrev.com/c0a28c56cddfcb6c8e0796d07189633b350c7deb/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/fenced_frame/visibility-changed-expected.html
[modify] https://crrev.com/4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851/third_party/blink/web_tests/VirtualTestSuites
[modify] https://crrev.com/4f6e84a9e911b9e22ff36770e8ceb5e1d09dd851/content/browser/security_exploit_browsertest.cc


### gi...@appspot.gserviceaccount.com (2021-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2b3304ff64a1103b87b1c760fdc0eaa3c4465df5

commit 2b3304ff64a1103b87b1c760fdc0eaa3c4465df5
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Fri Dec 10 19:51:49 2021

Ensure that the MParch FencedFrame feature is enabled when handling mparch mojo IPC

Bug: 1270358
Change-Id: Id68b801f61f3360e1e959e044203d5c0d9f60e9e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3323525
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Dominic Farolino <dom@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Shivani Sharma <shivanisha@chromium.org>
Commit-Queue: Brendon T <btiszka@gmail.com>
Cr-Commit-Position: refs/heads/main@{#950637}

[modify] https://crrev.com/2b3304ff64a1103b87b1c760fdc0eaa3c4465df5/content/browser/bad_message.h
[modify] https://crrev.com/2b3304ff64a1103b87b1c760fdc0eaa3c4465df5/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/2b3304ff64a1103b87b1c760fdc0eaa3c4465df5/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/2b3304ff64a1103b87b1c760fdc0eaa3c4465df5/content/browser/security_exploit_browsertest.cc


### bt...@gmail.com (2021-12-15)

The patch in comment https://crbug.com/chromium/1270358#c15 fixes this issue. I verified by applying the attached renderer patch to tip-of-tree (c610e72984f5712e9c33143e6b8578e874a945e9). With the malicious renderer_patch applied and the fix reverted the IPC goes through and renders `file://etc/passwd`, with the fix applied the IPC does not go through. I also included a security_browser_test to mimic a compromised sending this mojo IPC.

I'm working on a second patch that will hide this feature in the browser process behind a feature flag in the same way other experimental features are hidden behind a feature flag until they are enabled for origin-tirals. More context in the comments of https://chromium-review.googlesource.com/c/chromium/src/+/3323525.

However, the second patch is needed to mark this as Fixed.

### bt...@gmail.com (2021-12-15)

Second CL is here: https://chromium-review.googlesource.com/c/chromium/src/+/3340017/1

### [Deleted User] (2021-12-19)

dom: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-12-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9b740966ebb4f42f8de032fa0d42f843d1d4845a

commit 9b740966ebb4f42f8de032fa0d42f843d1d4845a
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Mon Dec 20 08:50:18 2021

Reland "Ensure the FencedFrames feature is enabled when handling mojo ipc"

This is a reland of commit 874303093082ebf6c83ca7f650b41de1af6615bb, but also removes the experimental status from fenced frame runtime features. Some of this reland was incorporated and completed in 2b3304ff64a1103b87b1c760fdc0eaa3c4465df5.
Original change's description:
> Ensure the FencedFrames feature is enabled when handling mojo ipc
>
> R=dom@chromium.org
> R=linnan@chromium.org
> R=lukasza@chromium.org
>
> Bug: 1270358
> Change-Id: Ib70fe27b97cda58caf8915e1d86ac7253b25ac76
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3285267
> Reviewed-by: Dominic Farolino <dom@chromium.org>
> Reviewed-by: Reilly Grant <reillyg@chromium.org>
> Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> Reviewed-by: Daniel Cheng <dcheng@chromium.org>
> Reviewed-by: Koji Ishii <kojii@chromium.org>
> Commit-Queue: Daniel Cheng <dcheng@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#949142}

Bug: 1270358
Change-Id: If5d8239e9c946af001dfb8f54c42326d212b342b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3340017
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Reviewed-by: Dominic Farolino <dom@chromium.org>
Reviewed-by: Ben Wells <benwells@chromium.org>
Commit-Queue: Brendon T <btiszka@gmail.com>
Cr-Commit-Position: refs/heads/main@{#952860}

[modify] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/third_party/blink/renderer/platform/runtime_enabled_features.json5
[add] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/fenced_frame/basic-expected.html
[modify] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/third_party/blink/common/features.cc
[modify] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/third_party/blink/web_tests/TestExpectations
[add] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/README.md
[rename] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/navigate-by-name-expected.txt
[add] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/prerender.https-expected.txt
[modify] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/chrome/browser/extensions/api/declarative_net_request/declarative_net_request_browsertest.cc
[modify] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/third_party/blink/web_tests/webexposed/element-instance-property-listing-expected.txt
[modify] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/third_party/blink/web_tests/webexposed/global-interface-listing-expected.txt
[modify] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/content/browser/renderer_host/render_frame_host_impl.cc
[add] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/fenced_frame/visibility-changed-expected.html
[modify] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/third_party/blink/renderer/core/html/fenced_frame/fenced_frame_shadow_dom_delegate_test.cc
[modify] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/third_party/blink/web_tests/VirtualTestSuites
[modify] https://crrev.com/9b740966ebb4f42f8de032fa0d42f843d1d4845a/content/browser/security_exploit_browsertest.cc


### do...@chromium.org (2021-12-21)

I think we can close this now, since the remaining work is covered by https://bugs.chromium.org/p/chromium/issues/detail?id=1243568, and the "compromised renderer" part of this is done. Thanks to btiszka@gmail.com for filing this bug and submitting the CLs!

### bt...@gmail.com (2021-12-21)

Thanks for the mentoring me on the CL dom@! I also wanted to add that during my testing I found that https://crbug.com/chromium/2 was reachable only via compromised renderer and not when the feature flag was legitimately enabled which is a bug pattern I never thought about before this vulnerability and might apply to other origin trial features. (this also adds to the fact that https://crbug.com/chromium/2 is now fixed as well with the above CLs)

### [Deleted User] (2021-12-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-21)

Requesting merge to stable M96 because latest trunk commit (949142) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (949142) appears to be after beta branch point (938553).

Not requesting merge to dev (M98) because latest trunk commit (949142) appears to be prior to dev branch point (950365). If this is incorrect, please replace the Merge-NA-98 label with Merge-Request-98. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-21)

Merge review required: M97 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-21)

Merge review required: M96 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-12-22)

The original CL and revert landed before branch point for 98 with the reland/second CL landed occurring after branch point, after a precursory check on canary and presumption this has been tested based on the comments above (and no stability issue or other concerns are to be had), approving for merge to M98; please merge to branch 4758 at your earliest convenience. 
After there the confirmation of the above, will re-review for merge to M97 and M96 (as M96 will be going into Extended support as M97 goes into stable release). 
Please let me know if there are any issues or concerns with this plan. Thanks! 

### am...@google.com (2022-01-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-06)

Congratulations, Brendon! The VRP Panel has decided to award you $17,000 for this report + patch bonus. Thank you for all your efforts in landing this fix and reporting this issue! 

### do...@chromium.org (2022-01-06)

1. Why does your merge fit within the merge criteria for these milestones?
Due to the severity of the bug, it was requested that we merge these CLs into the release branches. That's all I know.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3323525 and https://chromium-review.googlesource.com/c/chromium/src/+/3340017

3. Have the changes been released and tested on canary?
Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
The changes only impact a feature that is under a flag, and is not being experimented with anywhere at the moment.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
No

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
I don't know -- I don't think so though.

### am...@google.com (2022-01-06)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-07)

Thanks, dom@ -- merge approved for M97 and M96, please merge to branch 4692 and 4664 at your earliest convenience 

### sr...@google.com (2022-01-07)

This issue has been approved for merge to M98, we are cutting beta RC build today end of the day for a release on Monday . Please help complete your merges asap so this change can bake in beta at the earliest. 

### gi...@appspot.gserviceaccount.com (2022-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3c964808805d55dae3b1a56b2761895dc4dc392d

commit 3c964808805d55dae3b1a56b2761895dc4dc392d
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Fri Jan 07 20:19:30 2022

[Merge to M98]: Ensure that the MParch FencedFrame feature is enabled when handling mparch mojo IPC

(cherry picked from commit 2b3304ff64a1103b87b1c760fdc0eaa3c4465df5)

Bug: 1270358
Change-Id: Id68b801f61f3360e1e959e044203d5c0d9f60e9e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3323525
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Dominic Farolino <dom@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Shivani Sharma <shivanisha@chromium.org>
Commit-Queue: Brendon T <btiszka@gmail.com>
Cr-Original-Commit-Position: refs/heads/main@{#950637}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3368209
Commit-Queue: Dominic Farolino <dom@chromium.org>
Auto-Submit: Dominic Farolino <dom@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#404}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/3c964808805d55dae3b1a56b2761895dc4dc392d/content/browser/bad_message.h
[modify] https://crrev.com/3c964808805d55dae3b1a56b2761895dc4dc392d/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/3c964808805d55dae3b1a56b2761895dc4dc392d/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/3c964808805d55dae3b1a56b2761895dc4dc392d/content/browser/security_exploit_browsertest.cc


### gi...@appspot.gserviceaccount.com (2022-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5

commit 556ad8e9dc252b6ffb5924ce0a20d3217f96bde5
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Fri Jan 07 23:00:30 2022

[Merge to M98]: Reland "Ensure the FencedFrames feature is enabled when handling mojo ipc"

This is a reland of commit 874303093082ebf6c83ca7f650b41de1af6615bb, but also removes the experimental status from fenced frame runtime features. Some of this reland was incorporated and completed in 2b3304ff64a1103b87b1c760fdc0eaa3c4465df5.
Original change's description:
> Ensure the FencedFrames feature is enabled when handling mojo ipc
>
> R=dom@chromium.org
> R=linnan@chromium.org
> R=lukasza@chromium.org
>
> Bug: 1270358
> Change-Id: Ib70fe27b97cda58caf8915e1d86ac7253b25ac76
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3285267
> Reviewed-by: Dominic Farolino <dom@chromium.org>
> Reviewed-by: Reilly Grant <reillyg@chromium.org>
> Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
> Reviewed-by: Daniel Cheng <dcheng@chromium.org>
> Reviewed-by: Koji Ishii <kojii@chromium.org>
> Commit-Queue: Daniel Cheng <dcheng@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#949142}

(cherry picked from commit 9b740966ebb4f42f8de032fa0d42f843d1d4845a)

Bug: 1270358
Change-Id: If5d8239e9c946af001dfb8f54c42326d212b342b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3340017
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Reviewed-by: Dominic Farolino <dom@chromium.org>
Reviewed-by: Ben Wells <benwells@chromium.org>
Commit-Queue: Brendon T <btiszka@gmail.com>
Cr-Original-Commit-Position: refs/heads/main@{#952860}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3372326
Reviewed-by: Stephen Chenney <schenney@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Dominic Farolino <dom@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#412}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/third_party/blink/renderer/platform/runtime_enabled_features.json5
[add] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/fenced_frame/basic-expected.html
[modify] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/third_party/blink/common/features.cc
[modify] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/third_party/blink/web_tests/TestExpectations
[add] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/README.md
[rename] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/navigate-by-name-expected.txt
[add] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/wpt_internal/fenced_frame/prerender.https-expected.txt
[modify] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/chrome/browser/extensions/api/declarative_net_request/declarative_net_request_browsertest.cc
[modify] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/third_party/blink/web_tests/webexposed/element-instance-property-listing-expected.txt
[modify] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/third_party/blink/web_tests/webexposed/global-interface-listing-expected.txt
[modify] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/content/browser/renderer_host/render_frame_host_impl.cc
[add] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/third_party/blink/web_tests/virtual/fenced-frame-shadow-dom/fenced_frame/visibility-changed-expected.html
[modify] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/third_party/blink/renderer/core/html/fenced_frame/fenced_frame_shadow_dom_delegate_test.cc
[modify] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/third_party/blink/web_tests/VirtualTestSuites
[modify] https://crrev.com/556ad8e9dc252b6ffb5924ce0a20d3217f96bde5/content/browser/security_exploit_browsertest.cc


### gi...@appspot.gserviceaccount.com (2022-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6e5abb702af92d5ab91c33994b2cd288f4f22beb

commit 6e5abb702af92d5ab91c33994b2cd288f4f22beb
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Sat Jan 08 13:50:10 2022

[Merge to M97]: Ensure that the MParch FencedFrame feature is enabled when handling mparch mojo IPC

(cherry picked from commit 2b3304ff64a1103b87b1c760fdc0eaa3c4465df5)

Bug: 1270358
Change-Id: Id68b801f61f3360e1e959e044203d5c0d9f60e9e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3323525
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Dominic Farolino <dom@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Shivani Sharma <shivanisha@chromium.org>
Commit-Queue: Brendon T <btiszka@gmail.com>
Cr-Original-Commit-Position: refs/heads/main@{#950637}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3371768
Commit-Queue: Dominic Farolino <dom@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#1388}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/6e5abb702af92d5ab91c33994b2cd288f4f22beb/content/browser/bad_message.h
[modify] https://crrev.com/6e5abb702af92d5ab91c33994b2cd288f4f22beb/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/6e5abb702af92d5ab91c33994b2cd288f4f22beb/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/6e5abb702af92d5ab91c33994b2cd288f4f22beb/content/browser/security_exploit_browsertest.cc


### gi...@appspot.gserviceaccount.com (2022-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3d6a86ed0b1f97357e3840a74c85a5471de47ad3

commit 3d6a86ed0b1f97357e3840a74c85a5471de47ad3
Author: Brendon Tiszka <btiszka@gmail.com>
Date: Wed Jan 12 03:49:51 2022

[Merge to M96]: Ensure that the MParch FencedFrame feature is enabled when handling mparch mojo IPC

(cherry picked from commit 2b3304ff64a1103b87b1c760fdc0eaa3c4465df5)

Bug: 1270358
Change-Id: Id68b801f61f3360e1e959e044203d5c0d9f60e9e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3323525
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Dominic Farolino <dom@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Shivani Sharma <shivanisha@chromium.org>
Commit-Queue: Brendon T <btiszka@gmail.com>
Cr-Original-Commit-Position: refs/heads/main@{#950637}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3371797
Auto-Submit: Dominic Farolino <dom@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1390}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/3d6a86ed0b1f97357e3840a74c85a5471de47ad3/content/browser/bad_message.h
[modify] https://crrev.com/3d6a86ed0b1f97357e3840a74c85a5471de47ad3/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/3d6a86ed0b1f97357e3840a74c85a5471de47ad3/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/3d6a86ed0b1f97357e3840a74c85a5471de47ad3/content/browser/security_exploit_browsertest.cc


### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1270358?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>FencedFrames, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation]
[Monorail mergedwith: crbug.com/chromium/1270353]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057925)*
