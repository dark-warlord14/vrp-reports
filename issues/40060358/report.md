# SameSite strict cookies bypass/cross-origin download via `e.dataTransfer.setData('DownloadURL', ...`

| Field | Value |
|-------|-------|
| **Issue ID** | [40060358](https://issues.chromium.org/issues/40060358) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>DataTransfer, UI>Browser>Downloads |
| **Platforms** | Mac, Windows |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | lu...@google.com |
| **Created** | 2022-07-21 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

Run the following on ANY origin.  

let link = document.createElement('a');  

link.innerText = 'foo'  

link.href = '#';  

link.addEventListener('dragstart', onDragStart, false);  

document.body.appendChild(link);

function onDragStart(e) {  

e.dataTransfer.setData('DownloadURL', 'application/octet-stream:demo:<https://terjanq.me/xss.php?headers>');  

e.dataTransfer.effectAllowed = 'all';  

}

Drag the foo text on to your desktop.  

The file should contain sec-fetch-site: 'none'

**Problem Description:**  

Cross-origin download is meant to be initiated cross-origin, so strict cookies are not sent and fetch metadata is correct.  

Also <https://bugs.chromium.org/p/chromium/issues/detail?id=714373> was meant to block cross-origin URLs and it seems more convincing this way as a download does not need to be user initiated but drag and drop does.

**Additional Comments:**  

<https://terjanq.me/xss.php?headers> can be replaced with any server that reports the sent headers.

\*\*Chrome version: \*\* 103.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [CatLeaks.mp4](attachments/CatLeaks.mp4) (video/mp4, 906.5 KB)
- [rule.mp4](attachments/rule.mp4) (video/mp4, 1.1 MB)

## Timeline

### [Deleted User] (2022-07-21)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-07-22)

I cannot reproduce this. I get an empty file on the desktop and the downloads bar shows "Failed - Blocked" for the file.

### nd...@protonmail.com (2022-07-22)

Thats strange on windows 10 I have tested both stable and canary and its working for me.
Is there any policy that would be preventing the download to that folder?

### nd...@protonmail.com (2022-07-23)

I think the code for it is at https://source.chromium.org/chromium/chromium/src/+/main:content/browser/download/drag_download_file.cc

### nd...@protonmail.com (2022-07-23)

Also tried in a sandbox still seems to work attached PoC video.
Contains SameSite strict cookies and also a cat.

### nd...@protonmail.com (2022-07-24)

Failed - Blocked can happen when asking for a file:// on https://
Not sure where its checked so might be able to bypass it but never tried.

### rs...@chromium.org (2022-07-25)

Could you provide a more complete reproduction then? Here is what I have setup:

% cat server.py 
#!/usr/bin/env python3

import http.server

PORT = 4000

class GetHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        resp = str(self.headers)
        print(resp)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(resp.encode('utf8'))


http.server.HTTPServer(('', PORT), GetHandler).serve_forever()

% cat test.html 
<html>
<body>
  hi
</body>
<script>
let link = document.createElement('a');
link.innerText = 'foo'
link.href = '#';
link.addEventListener('dragstart', onDragStart, false);
document.body.appendChild(link);

function onDragStart(e) {
  e.dataTransfer.setData('DownloadURL', 'application/octet-stream:demo:http://localhost:4000');
  e.dataTransfer.effectAllowed = 'all';
}

</script>

In two separate shells:
% python3 -m http.server
% python3 server.py

% curl http://localhost:4000
Host: localhost:4000
User-Agent: curl/7.83.1
Accept: */*

And seen in the shell running server.py:
----
Host: localhost:4000
User-Agent: curl/7.83.1
Accept: */*


127.0.0.1 - - [25/Jul/2022 18:15:15] "GET / HTTP/1.1" 200 -
----

Then I go to http://localhost:8000/test.html and drag the link “foo” to the desktop. A file is created but the contents are empty, the downloads bar shows “Failed - Blocked”, and the server.py server did not receive any HTTP request.

### nd...@protonmail.com (2022-07-26)

Code you provided works for me on windows 10 will test linux.

### nd...@protonmail.com (2022-07-26)

Im not able to repo the issue on Linux by setting the e.dataTransfer.effectAllowed = 'copy'; it seems to download the page instead.
Its recommended that this be tested on a windows device and maybe remove the "feature" as its very obscure.

### bh...@google.com (2022-07-26)

Cannot reproduce on both Linux and Windows. As noted for linux, the drag and drop downloads the page instead, and on windows, the download is blocked.

### nd...@protonmail.com (2022-07-26)

I was able to reproduce the issue with not being able to reproduce the issue.
Will look in to it.

### nd...@protonmail.com (2022-07-26)

The fix as shown in the video and the first comment is to run the code on example.com not localhost I wish I was making this up.


### nd...@protonmail.com (2022-07-26)

I now suspect the rule is protocol should be the same as the download url.
Please test with the correct protocol on windows 10 if this does not work I will have to get someone else to help repo it see if im missing anything else.


### nd...@protonmail.com (2022-07-26)

I have no idea why http://example.com/ works for the localhost case and localhost does not its a very strange bug.
Hope the video give you some idea when it works the issues with it may also be considered bugs.

### nd...@protonmail.com (2022-07-27)

I suspect its because http:// is consider insecure so downloads may get blocked that some reason includes localhost it self.

### nd...@protonmail.com (2022-07-27)

Annoying seems more of a testing issue tried downloading https://www.google.com from https://example.com and that works fine.
http://example.com can download from localhost but localhost or https:// can not.

### nd...@protonmail.com (2022-07-28)

Code in https://crbug.com/chromium/1346429#c7 works with one exception run the test.html directly as localhost gets blocked for an unknown reason unrelated to this bug normal https works fine.
Are you able to reproduce on windows 10 with that information works for me on a sandbox and I can confirm normal localhost does not work.

### bh...@google.com (2022-07-29)

Thanks for your patience. Here is my reading of the problem.

1) We had problems because of mixed content (https origin requesting http content) and untrusted content getting blocked.
2) When I tested with https server on my localhost, I created a self signed certificate, which was not being accepted. The navigation shows the user an interstitial, but the drag and drop is blocked I think.
3) This still does not work on Linux, probably because the drag and drop data not being supported there.

I was able to replicate with your original setup (copy the javascript to a https example.org on windows machine). However, I am not able to judge if this is still a bug. The reason is as follows --
Sec-fetch-site header (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-Fetch-Site) is set to none, which is meant for user-originated operation. In the description for what qualifies as user-originated, it mentions drag and drop. In that sense, it is probably working as intended. However, I am also not able to understand the argument for limiting the download attribute on anchor tags to same origin, even though it is also user-originated.

CCing Min for thoughts.

[Monorail components: UI>Browser>Downloads]

### [Deleted User] (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-30)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2022-07-30)

"dragging-and-dropping a file into the browser window."
Setting "DownloadURL" is not a file but a request to make a cross-origin download with a custom name.
The URL is not originated from the user so in my opinion its Sec-Fetch-User and initiated cross-site. (Maybe the spec would tell me whats meant)

Like https://bugs.chromium.org/p/chromium/issues/detail?id=608669 I think this should also have the same-origin rule to avoid tricking the user into both leaking information cross-site and sending network requests with SameSite Strict cookies.

### nd...@protonmail.com (2022-07-30)

Drag-and-drop: It seems reasonable to distinguish behavior here based upon the source of the dragged content. If content is dragged from a tab, the user agent should be able to ascertain its origin, and set Sec-Fetch-Site accordingly. If content is dragged from elsewhere (the user agent’s bookmark bar, another app entirely, etc), then Sec-Fetch-Site: none may be appropriate.

https://w3c.github.io/webappsec-fetch-metadata/#directly-user-initiated

### nd...@protonmail.com (2022-07-31)

From what I can tell this is used in file:///C:/ so you can drag links to download files.
Seems like it could be abused also said in 2017 https://twitter.com/TimSeverien/status/890103436112535552

### bh...@google.com (2022-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-08-10)

Chrome security marshal here - CCing mkwst@ to comment on or delegate answering whether setting "Sec-Fetch-Site: none" is the correct behavior for a drag-and-drop initiated download.

### qi...@chromium.org (2022-08-25)

Sorry, I am not very familiar with  "Sec-Fetch-Site: none"  and its implications on drag-n-drop, can some one from the security team take a look and determine whether the current approach of setting "Sec-Fetch-Site: none" is sane?

### nd...@protonmail.com (2022-08-25)

Im not sure if it should even send Lax cookies, I dont think people would expect something dragged from one site to contain an authenticated response from a different site.

### za...@google.com (2022-08-26)

Friendly ping from Chrome security marshal, can someone take a look and if this behavior is intended or do we need a fix?

### nd...@protonmail.com (2022-08-28)

Also a bypass of an iframe sandbox without "allow-downloads" :-)

### za...@google.com (2022-08-29)

[Empty comment from Monorail migration]

### bh...@google.com (2022-08-29)

I am not an expert on when and which headers should be sent. mkwst@ can you help identify the right owner?

### ad...@google.com (2022-09-21)

mkwst@ please take a look.

### [Deleted User] (2022-09-21)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 61 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-22)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-05)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 75 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@google.com (2022-10-11)

Thanks for the ping, I missed this when it was assigned to me.

It seems pretty clear that we ought to be sending something other than `Sec-Fetch-Site: none`. It looks like the request's initiator isn't correctly set when initiating the download (at least, it isn't correct at https://source.chromium.org/chromium/chromium/src/+/main:components/download/internal/common/in_progress_download_manager.cc;drc=9d944ac3fe93c73eb6e7ab9cf1dd890f2ae86ddc;l=318), but I'm not sure where that set of parameters needs to be instantiated. Reassigning this to dtrainor@ in the hopes that they might know this code better.

That said, I wouldn't consider this a "High" severity bug, both because of the limited scope of the bypass, and the drag-to-desktop requirement. Both would suggest "Medium" to me, but I'll defer to security sheriffs' take there.

### bh...@google.com (2022-10-28)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-11-07)

Hi there, this your friendly Security Marshal stopping by. 

I agree with @mkwst's observations about severity in https://crbug.com/chromium/1346429#c39. Dropping to Medium Severity because requirement to drag-and-drop to desktop significantly limits scope for exploitation. 

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### dt...@chromium.org (2022-12-01)

qinmin@ can you take a look based on #39 in response to your comment about Sec-Fetch-Site:none?

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-03-22)

Is the DownloadURL feature even used by websites seems like its mainly a file:// thing.

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-07-21)

I don't think qinmin@ looked :(

### qi...@chromium.org (2023-07-21)

Is this happening to drag and drop only?

### nd...@protonmail.com (2023-07-21)

Looks to be it is called drag_download_file.cc

### qi...@chromium.org (2023-07-22)

unfortunately, my knowledge on "Sec-Fetch-Site" header is weak. Assigning to lukasza@ as he worked on many "Sec-Fetch-Site" related CLs.

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### lu...@chromium.org (2023-08-30)

Let me try to note what I learned about this bug.

1. Automated tests are difficult.
    * Adding `CHECK(false)` to `DragDownloadFile::InitiateDownload` failed only 3 `content_browsertests` (see https://crrev.com/c/4818005), all of which are constructing `DragDownloadFile` from test code.  In other words, there is no automated test coverage of product-code constructing `DragDownloadFile` and calling `DragDownloadFile::InitiateDownload`
    * I don't see a way to provide automated test coverage. Long time ago I tried to improve the test coverage of drag-and-drop by creating `chrome/browser/ui/views/drag_and_drop_interactive_uitest.cc`.  These tests don't work on Windows (a comment in the test sources says "There is no known way to execute test-controlled tasks during a drag-and-drop loop run by Windows OS").  And AFAIR these tests never worked on MacOS.  (AFAICT `DragDownloadFile` is constructed only from A) content/browser/web_contents/web_contents_view_mac.mm and B) from content/browser/web_contents/web_contents_view_aura.cc but only if IS_WIN)

2. Plumbing the initiator origin is difficult

2.1. BUILDFLAG(IS_WIN) / PrepareDragForDownload in content/browser/web_contents/web_contents_view_aura.cc doesn't currently have a way to get the initiator origin.

2.1.1. DragDrop has `did_originate_from_renderer`, but doesn't have information about the initiator origin
2.1.2. WebContents can't be used, because we don't know if the drag has originated from the top-level frame VS one of subframes.  It seems that WebContents are plumbed through from WebContentsViewAura::StartDragging which AFAICS can't tell which frame the drag originated from.

2.2. WebContentsViewMac::DragPromisedFileTo in content/browser/web_contents/web_contents_view_mac.mm is even tricker, because it gets called long after the drag has started.

### lu...@chromium.org (2023-08-30)

dcheng@, can you PTAL as one of //ui/base/dragdrop/OWNERS?  Based on https://crbug.com/chromium/1346429#c53, it seems to me that the main problem with this bug is in the drag-and-drop feature area which 1) doesn't provide a way to discover the origin (or a frame) that the drag originated from, and 2) (maybe less importantly) doesn't provide a way for adding automated test coverage.

[Monorail components: Blink>DataTransfer]

### lu...@chromium.org (2023-08-30)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-08-30)

It's easy to stamp the origin into the dragdata if that's something we need. The main complication is we'd need to move StartDragging() from a per-widget IPC to a per-frame IPC. There were previously a bunch of layering issues here, but we might have fixed enough of them that this move wouldn't be that hard to make now.

Originally, I was going to suggest that the value of the Sec-Fetch-Site header could be set at StartDragging() time as well, but it sounds like it needs to take the redirect chain into account.

Re: testing, this is unlikely to improve any time soon, especially for DownloadURL which is already a non-standard drag data type and relies heavily on integration with native drag-and-drop mechanisms to accomplish its task.

### gi...@appspot.gserviceaccount.com (2023-09-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2d79e96434e7350e9503ebc167284678b358e8de

commit 2d79e96434e7350e9503ebc167284678b358e8de
Author: Daniel Cheng <dcheng@chromium.org>
Date: Fri Sep 01 03:28:57 2023

Change StartDragging IPC to be per-frame.

This allows per-frame info, such as origin, to be attributed to drags.

Bug: 1346429
Change-Id: Ia0b947bb0062458071ca07616f8dd741689b5b9c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4828259
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1191144}

[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/content/public/test/fake_render_widget_host.h
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/third_party/blink/renderer/core/frame/web_frame_widget_impl.cc
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/third_party/blink/public/mojom/page/widget.mojom
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/third_party/blink/renderer/core/frame/web_frame_widget_impl.h
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/third_party/blink/public/mojom/frame/frame.mojom
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/third_party/blink/renderer/core/web_test/web_test_web_frame_widget_impl.cc
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/third_party/blink/renderer/core/testing/fake_local_frame_host.h
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/third_party/blink/renderer/core/testing/fake_local_frame_host.cc
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/content/browser/renderer_host/render_widget_host_impl.h
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/third_party/blink/renderer/core/frame/web_frame_widget_test.cc
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/content/test/test_render_view_host.cc
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/third_party/blink/renderer/core/page/chrome_client_impl.cc
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/content/public/test/fake_render_widget_host.cc
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/third_party/blink/renderer/core/web_test/web_test_web_frame_widget_impl.h
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/content/browser/renderer_host/render_widget_host_impl.cc
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/third_party/blink/renderer/core/frame/frame_test_helpers.cc
[modify] https://crrev.com/2d79e96434e7350e9503ebc167284678b358e8de/third_party/blink/renderer/core/frame/frame_test_helpers.h


### lu...@chromium.org (2023-09-02)

Let me take the bug again and try to plumb the initiator origin information through StartDragging.

WIP CLs:

* https://crrev.com/c/4818005: Use `GlobalRenderFrameHostId` in `DragDownloadFileUI`. 
* https://crrev.com/c/4836877: Plumb `source_rfh` via `StartDragging`, into `DragDownloadFile`.
* TODO: Using the right initiator origin in DragDownloadFile
* TODO: Discussing and implementing passing the right initiator origin in other scenarios (e.g. dragging a link into the omnibox?).

### lu...@chromium.org (2023-09-02)

[Empty comment from Monorail migration]

### lu...@chromium.org (2023-09-02)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-09-02)

Oh I already have a WIP CL for plumbing the drag origin to the OS (but not actually using the origin) Let me know how you'd prefer to proceed.

### nd...@protonmail.com (2023-09-02)

I tried dragging a URL in the omnibox and it did not navigate without me pressing enter I might be missing something.

But on this topic:
The PDF viewer (that can be clickjacked) uses chrome.tabs.create which does not use the initiator (inactive bug) https://bugs.chromium.org/p/chromium/issues/detail?id=1275113 and I think bypasses WAR with a server redirect.


### dc...@chromium.org (2023-09-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2cb89f90a30a123cec3acab6bbdb3756fb56318f

commit 2cb89f90a30a123cec3acab6bbdb3756fb56318f
Author: Daniel Cheng <dcheng@chromium.org>
Date: Thu Sep 28 00:46:54 2023

Plumb origin through for drags.

This repurposes the data type used to tag drags as renderer-initiated by
also using it to store the origin of the source of the drag data.

Currently, opaque origins are not plumbed through end-to-end. An opaque
origin will still cause the drag to be treated as renderer-tainted;
however, when reading out the origin, a new unique opaque origin will be
created.

Bug: 1346429
Change-Id: I52467e30d590473ded1eb2dd15fb40ff8ceabb23
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4837192
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1202178}

[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/web_contents/web_contents_view_mac.mm
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/app_shim_remote_cocoa/web_drag_source_mac.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/web_contents/web_contents_view_child_frame.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/renderer_host/render_view_host_delegate_view.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/app_shim_remote_cocoa/web_contents_view_cocoa.mm
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/web_contents/web_contents_view_aura_unittest.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/app_shim_remote_cocoa/web_contents_view_cocoa.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/web_contents/web_contents_view_android.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/dragdrop/os_exchange_data_provider_win.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/renderer_host/render_widget_host_impl.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/dragdrop/os_exchange_data_provider_mac.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/x/x11_os_exchange_data_provider.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/dragdrop/os_exchange_data_provider_win.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/dragdrop/os_exchange_data_provider_non_backed.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/dragdrop/os_exchange_data_provider_non_backed_unittest.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/dragdrop/os_exchange_data.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/dragdrop/os_exchange_data_provider.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/renderer_host/render_view_host_unittest.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/clipboard/clipboard_constants.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/app_shim_remote_cocoa/web_drag_source_mac.mm
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/renderer_host/render_widget_host_unittest.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/web_contents/web_contents_view_mac.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/web_contents/web_drag_source_mac_unittest.mm
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/common/web_contents_ns_view_bridge.mojom
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/x/x11_os_exchange_data_provider.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/app_shim_remote_cocoa/web_contents_ns_view_bridge.mm
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/dragdrop/os_exchange_data_provider_non_backed.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/dragdrop/os_exchange_data_unittest.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/dragdrop/os_exchange_data_provider_mac.mm
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/chrome/browser/ui/views/drag_and_drop_interactive_uitest.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/web_contents/web_contents_view_aura.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/renderer_host/render_widget_host_impl.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/web_contents/web_contents_view_aura.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/web_contents/web_contents_view_child_frame.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/browser/web_contents/web_contents_view_android.cc
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/content/app_shim_remote_cocoa/web_contents_ns_view_bridge.h
[modify] https://crrev.com/2cb89f90a30a123cec3acab6bbdb3756fb56318f/ui/base/dragdrop/os_exchange_data.h


### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1346429?no_tracker_redirect=1

[Multiple monorail components: Blink>DataTransfer, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

### nd...@protonmail.com (2024-02-05)

I noticed the "Plumb origin through for drags" got merged but this still seems to work in the latest chrome version :(

### nd...@protonmail.com (2024-04-17)

I think the bot got more annoying, don't really need a email about lu...@chromium.org   ->   lu...@google.com looks like the same person but now on google domain!

### nd...@protonmail.com (2024-07-02)

For context there's a Firefox bug to `support proposed DownloadURL format string on DataTransfer object`  

<https://bugzilla.mozilla.org/show_bug.cgi?id=570164#c18> supports blocking cross-origin downloads.

### ap...@google.com (2024-07-15)

Project: chromium/src
Branch: main

commit fe310d6b6175bf4b1d3c06f011ce5c27ce1d100d
Author: Lukasz Anforowicz <lukasza@chromium.org>
Date:   Mon Jul 15 20:53:31 2024

    Populate initiator origin in `DragDownloadFileUI::InitiateDownload`.
    
    This CL propagates the initiator origin via
    `content::DragDownloadFile::DragDownloadFileUI::InitiateDownload`
    into `download::DownloadUrlParameters::set_initiator`.
    
    Note that the initiator origin comes from trustworthy, browser-side data:
    
    - `RenderFrameHostImpl::StartDragging` passes `GetLastCommittedOrigin()`
      into `RenderViewHostDelegateView::StartDragging`
    - `WebContentsViewAura::StartDragging` stores the origin into into
      `ui::OSExchangeDataProviderFactory` using a call to
      `ui::OSExchangeDataProviderFactory::MarkRendererTaintedFromOrigin`.
      On Windows this CL takes the origin from
      `OSExchangeDataProviderFactory` and passes it directly into
      `DragDownloadFile`'s constructor.
    - `WebContentsViewMac::StartDragging` ends up storing the origin in
      `WebDragSource` from `web_drag_source_mac.mm`.  On Mac this CL takes
      this origin and also passes it (indirectly, via mojo) into
      `DragDownloadFile`'s constructor.
    
    @lukasza has manually tested this CL on Windows using the repro steps
    from https://crbug.com/40060358 (@dcheng has kindly tried the repro
    steps on Mac).  Note that `DragDownloadFile` is used on Windows and Mac,
    but not on Linux (i.e. the repro wouldn't have worked on Linux).
    
    Fixed: 40060358
    Change-Id: I24b180473e140cbb8a56640444f2f4a306aa42fc
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5692867
    Reviewed-by: Daniel Cheng <dcheng@chromium.org>
    Reviewed-by: Avi Drissman <avi@chromium.org>
    Commit-Queue: Łukasz Anforowicz <lukasza@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1327773}

M       content/app_shim_remote_cocoa/web_drag_source_mac.mm
M       content/app_shim_remote_cocoa/window_occlusion_browsertest_mac.mm
M       content/browser/download/drag_download_file.cc
M       content/browser/download/drag_download_file.h
M       content/browser/download/drag_download_file_browsertest.cc
M       content/browser/web_contents/web_contents_view_aura.cc
M       content/browser/web_contents/web_contents_view_mac.h
M       content/browser/web_contents/web_contents_view_mac.mm
M       content/common/web_contents_ns_view_bridge.mojom

https://chromium-review.googlesource.com/5692867


### nd...@protonmail.com (2024-07-17)

Thanks for the fixing the initiator

- "sec-fetch-site": "cross-site"
- Strict cookies are not sent

Lax cookies are still sent so the attack from <https://issuetracker.google.com/issues/40060358#comment6> would still work in most cases.

### nd...@protonmail.com (2024-07-17)

A same-origin DownloadURL for me gets "Blocked by your organization" so the request always needs to be made cross-origin the opposite of what I was trying to do :/

### nd...@protonmail.com (2024-07-17)

Also affects stable so I don't think its a breaking change might be specific to terjanq.me usage.

### lu...@google.com (2024-07-24)

RE: [#comment79](https://issues.chromium.org/issues/40060358#comment79): Lax cookies are still sent so the attack from <https://issuetracker.google.com/issues/40060358#comment6> would still work

The observed behavior matches my expectations - I think everything is working as intended at this point. In particular:

- A website/origin cannot in general initiate a **cross-origin** http request that would include strict cookies and/or `Sec-Fetch-Site` set to `none` or `same-origin`. **Except** that before this bug was fixed there was a loophole in the form of drag-and-drop-initiated downloads.
- But AFAIU lax cookies are included in all http requests - a cross-origin website/origin is able to trigger sending lax cookies to another origin with XHR / `fetch` / navigation links / etc. So sending lax cookies doesn't require exploring or abusing more exotic use cases like the drag-and-drop-initiated downloads. If sending lax cookies is a problem, then we would need to discuss it as a new, separate bug.

---

RE: [#comment80](https://issues.chromium.org/issues/40060358#comment80)-[#comment81](https://issues.chromium.org/issues/40060358#comment81)

I apologize, but I didn't understand the feedback in these comments. Did same-origin DownloadURL stop working for you recently? I think that [#comment81](https://issues.chromium.org/issues/40060358#comment81) says that it didn't stop working because of the change in <https://crrev.com/c/5692867>, but may have stopped working for other reasons?

As I explained above, I assume that everything works as intended now. If this is not the case, then maybe it would be helpful to phrase the current (new or remaining) problem in terms of: repro steps, expected behavior, and actual behavior.

---

Thank you very much for reporting this bug. My apologies that it took so long to author and land a fix.

### nd...@protonmail.com (2024-07-24)

If a cross-site download is authenticated it could contain private information that with abusing a custom file name could trick the user into leaking for example by making it look like there sharing a unrelated photo.  

If I understand correctly Lax cookies are never sent on cross-site requests except when its a top navigation, That would be SameSite=None (if its not authenticated there's no leak)

Did same-origin DownloadURL stop working for you recently? It did not work but I don't think its recent if its worth looking into that would be a separate bug.

### lu...@google.com (2024-07-24)

RE: [#comment83](https://issues.chromium.org/issues/40060358#comment83): Lax cookies are never sent on cross-site requests except when its a top navigation

Oh, I see. That may very well be the case. I may have reached a wrong conclusion when trying to extrapolate how setting the initiator\_origin should make downloads consistent with other scenarios.

So I think this means that the open question is: should downloads behave as top-level navigations VS as subresource requests (as observed for example via presence of lax cookies, `Sec-Fetch-Mode: navigate`, `Sec-Fetch-Dest`, etc.). I believe that at least *some* downloads behave (i.e. begin their life / initiate http request) as navigations (e.g. clicking a link and getting a response with `Content-Disposition: attachment`).

### lu...@google.com (2024-07-24)

Let me make a quick edit above: I should have said "as **top-level** navigations"...

### nd...@protonmail.com (2024-07-25)

This comment looks to say about downloads being treated as top-level navigations
<https://source.chromium.org/chromium/chromium/src/+/main:components/download/internal/common/download_utils.cc;l=381;drc=28534bc9f8fe33909a37a0222b6747720eee8e94>

```
// Treat downloads like top-level frame navigations to be consistent with
// cookie behavior. Also, since web-initiated downloads bypass the disk
// cache, sites can't use download timing information to tell if a
// cross-site URL has been visited before."

```

I still don't know why cookie behavior is this way, sounds like a 3rd party cookie blocking bypass without opening a new popup.

### sp...@google.com (2024-07-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
$1,000 for report of lower impact user information disclosure with high preconditions / user gesture 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-25)

Congratulations NDevTK -- thanks for your efforts and reporting this issue to us!

### nd...@protonmail.com (2024-07-25)

Thanks :)

There's still the open question about lax cookies (since there the default) for DownloadURL.

### lu...@google.com (2024-07-26)

RE: [#comment89](https://issues.chromium.org/issues/40060358#comment89):

AFAIU there are ways to make it more difficult for a subframe to initiate top-level navigations (e.g. popup blocking, `iframe.sandbox`, etc.), but if the subframe can trick the user into shift-clicking a link, then a top-level navigation will happen anyway. Other user gestures (e.g. right click link, select "open in new window" in the context menu) also exist. So, it seems to me that an attacker can abuse both top-level navigations (e.g. shift-click) and downloads (e.g. drag-and-drop to a desktop) to trigger sending lax cookies to a cross-origin victim server. And therefore if there is a problem, then it probably should be solved holistically, rather than just focusing on the downloads-based attack vector.

I don't feel confident in my understanding of the cookies landscape, so I also asked others in Chrome Security for their feedback. I got pointed to <https://datatracker.ietf.org/doc/html/draft-west-first-party-cookies-07#section-4.1.1> which seems to say that 1) triggering a top-level navigation is only a "speedbump" for an attacker, but 2) lax cookies may still be a valid protection mechanism if the defender doesn't care about protection for `GET` requests (but may still care about `POST`). From that perspective drag-and-drop-initiated downloads seem ok, because they issue `GET` requests.

### lu...@google.com (2024-07-26)

/cc @mkwst and @bingler - could you take a quick peek to vet my understanding of the lax cookies VS downloads behavior (see [#comment90](https://issues.chromium.org/issues/40060358#comment90) above, but also [#comment82](https://issues.chromium.org/issues/40060358#comment82) - [#comment86](https://issues.chromium.org/issues/40060358#comment86)).

### nd...@protonmail.com (2024-07-26)

If a user opens a popup it should contain lax cookies.  

This issue was about downloading a page that was not intended to be downloadable.

Could have also worked with the "save link as" feature.  

Now its protected by checking for "sec-fetch-site": "cross-site" or strict cookies.

Would be good for privacy to not send 3rd party cookies for downloads without user activation like the html attribute `download="leak"` but for sandboxed iframes downloads may be disabled anyway.

### bi...@chromium.org (2024-08-22)

Whoops, I missed that I was CC'd.

Your understanding is correct.

Lax cookies are sent in same-site contexts (like Strict cookies) and when the browser is performing a top-level navigation. It's also possible to skirt that restriction by trying to open a new window; either directly or attempting to convince the user to do so.

Allowing Lax cookies for a download request doesn't seem unreasonable to me. The draft cookie spec actually [encourages using a Lax cookie as a "read" token](https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis#name-top-level-navigations), which would suit a download request.

### pe...@google.com (2024-10-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060358)*
