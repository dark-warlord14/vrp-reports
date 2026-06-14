# Heap-use-after-free when a content script synchronously removes a frame at document_start or document_end

| Field | Value |
|-------|-------|
| **Issue ID** | [40083564](https://issues.chromium.org/issues/40083564) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-01-28 |
| **Bounty** | $1,500.00 |

## Description

Chrome version: stable (48.0.2564.82) and master (50.0.2629.0).  

This is a non-regression, I've also tried Chrome 25, 34, 35, 40 (Linux), 48.0.2552.0 (Mac and Win).

**What steps will reproduce the problem?**

1. Download the attached extension.
2. Start a HTTP server in that directory.
3. Start Chrome and load that directory as an extension (e.g. via chrome://extensions).
4. Visit <http://localhost/index_at_start.html>
5. Visit <http://localhost/index_at_end.html>

**What is the expected result?**  

The pages at step 4 and 5 are no more than <iframe src=..></iframe>  

The content script runs in the frame only and removes the frame itself.  

So. at step 4 and 5, you should just see a blank page.

What happens instead of that?  

At step 4 and 5, the tab crashes.  

I've attached the full stack traces, and also the stack trace for a debug build (both based on 3013c63965953c4fbf535eda79c1736a363681d7).

Here are the heads of the stack traces. It seems that the RenderFrameImpl::didCreateDocumentElement and RenderFrameImpl::didFinishDocumentLoad does does not account for the possibility that the frame can be destroyed by their observers.

document\_start:  

==24==ERROR: AddressSanitizer: heap-use-after-free on address 0x61800000b8b0 at pc 0x55a4f517e713 bp 0x7ffd9c33cea0 sp 0x7ffd9c33ce98  

READ of size 8 at 0x61800000b8b0 thread T0 (chrome)  

#0 0x55a4f517e712 in get base/memory/ref\_counted.h:307:27  

#1 0x55a4f517e712 in is\_valid base/memory/weak\_ptr.cc:43:0  

#2 0x55a4ff8e7fad in get base/memory/weak\_ptr.h:210:27  

#3 0x55a4ff8e7fad in operator-> base/memory/weak\_ptr.h:218:0  

#4 0x55a4ff8e7fad in didCreateDocumentElement content/renderer/render\_frame\_impl.cc:3308:0  

#5 0x55a4f960e8e9 in documentElementAvailable third\_party/WebKit/Source/web/FrameLoaderClientImpl.cpp:179:9

<https://chromium.googlesource.com/chromium/src/+/3013c63965953c4fbf535eda79c1736a363681d7/content/renderer/render_frame_impl.cc#3308>

document\_end:  

==49==ERROR: AddressSanitizer: heap-use-after-free on address 0x6060000f6470 at pc 0x55a4f517ea08 bp 0x7ffd9c33d3b0 sp 0x7ffd9c33d3a8  

READ of size 8 at 0x6060000f6470 thread T0 (chrome)  

#0 0x55a4f517ea07 in get base/memory/ref\_counted.h:307:27  

#1 0x55a4f517ea07 in HasRefs base/memory/weak\_ptr.h:127:0  

#2 0x55a4f517ea07 in GetRef base/memory/weak\_ptr.cc:54:0  

#3 0x55a5011c1df2 in GetWeakPtr base/memory/weak\_ptr.h:277:23  

#4 0x55a5011c1df2 in DidFinishDocumentLoad extensions/renderer/script\_injection\_manager.cc:154:0  

#5 0x55a4ff8e92c2 in didFinishDocumentLoad content/renderer/render\_frame\_impl.cc:3351:3  

#6 0x55a4fb960163 in finishedParsing third\_party/WebKit/Source/core/loader/FrameLoader.cpp:487:9

<https://chromium.googlesource.com/chromium/src/+/3013c63965953c4fbf535eda79c1736a363681d7/content/renderer/render_frame_impl.cc#3351>

## Attachments

- [index_at_start.html](attachments/index_at_start.html) (text/html, 91 B)
- [asan_at_document_start.log](attachments/asan_at_document_start.log) (text/plain, 12.1 KB)
- [asan_at_document_end.log](attachments/asan_at_document_end.log) (text/plain, 11.8 KB)
- [stack_trace_at_document_start.log](attachments/stack_trace_at_document_start.log) (text/plain, 5.1 KB)
- [manifest.json](attachments/manifest.json) (application/json, 545 B)
- [index_at_end.html](attachments/index_at_end.html) (text/html, 89 B)
- [remove_self.js](attachments/remove_self.js) (text/javascript, 44 B)
- [stack_trace_at_document_end.log](attachments/stack_trace_at_document_end.log) (text/plain, 4.4 KB)

## Timeline

### ro...@robwu.nl (2016-01-28)

[Empty comment from Monorail migration]

### rd...@chromium.org (2016-01-28)

+content/blink frame guru dcheng@.

### ro...@robwu.nl (2016-01-28)

I took a stab at trying to solve this: https://codereview.chromium.org/1642283002

### dc...@chromium.org (2016-01-28)

There was a past patch that attempted to solve this... I'm trying to find it.

Do content scripts have to run synchronously at document_start / document_end? There's an effort towards firing the load event in an async manner, so it'd make more sense to evolve in that direction for content scripts as well.

### dc...@chromium.org (2016-01-28)

Ah-ha, found the previous patch: https://codereview.chromium.org/112203003/

### dc...@chromium.org (2016-01-28)

Also see https://crbug.com/chromium/328342.

### mm...@chromium.org (2016-01-29)

Devlin, don't you mind if I assign you to be owner?

### rd...@chromium.org (2016-01-29)

@4
> Do content scripts have to run synchronously at document_start / document_end?
Synchronously with respect to the DOM, ideally, yes.  The point of document start is that it should inject before anything on the page has a chance to do anything, so executing in an async manner could break this.

Rob, do you want to own this, since you started working on it already?

### dc...@chromium.org (2016-01-29)

What about document end?

I'm hoping that if only document_start is synchronous, we don't have to add special code in the parser to handle weird edge cases like this (because really, we shouldn't have to).

### rd...@chromium.org (2016-01-29)

Hmm... We specify scripts "are injected immediately after the DOM is complete, but before subresources like images and frames have loaded."  I'm not sure how severe the implications of changing that to be async would be, but it would probably still break a few things.

### dc...@chromium.org (2016-01-29)

OK, so looking at the patch again, I guess it's sync document_start that's the problem for the parser. I guess the parser already has to handle some other weird cases, so maybe it's OK.

I do think we should try to figure out a better path forward for content scripts though... doing things async would make things easier to reason about. The HTML spec also says the DOMContentLoaded (roughly equivalent to document_end) and load (roughly equivalent to document_idle) should be async, so keeping the extension ones sync would be sad.

### ro...@robwu.nl (2016-01-29)

I just tested, and found that document_end is fired after the page's DOMContentLoaded event, so if needed, it's not that disastrous to slightly defer the document_end event.
But moving document_end is likely not needed, because I fixed the memory safety issues for document_end, and the source of the notification in Blink explicitly states that |this| shouldn't be touched after the notification: https://chromium.googlesource.com/chromium/src/+/ab81d6c319705c708cca4d6313a4cdd8f97b39d7/third_party/WebKit/Source/web/FrameLoaderClientImpl.cpp#432

document_start must be synchronous, because "the files are injected (...) before any other DOM is constructed or any other script is run." -- https://developer.chrome.com/extensions/content_scripts#run_at
Making document_start async would break this contact.

### dc...@chromium.org (2016-01-29)

I know we correctly handle it in Blink... but it would be even nicer if we didn't have to. We have a lot of WebFrameClient callbacks, and the fact that the embedder can randomly run script is generally unfortunate. There are bad interactions where the embedder running script can cause callbacks to arrive out of order, etc.

### dc...@chromium.org (2016-02-05)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-02-09)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-02-10)

[Empty comment from Monorail migration]

### dc...@chromium.org (2016-02-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

rob@: Uh oh! This issue is still open and hasn't been updated in the last 29 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ro...@robwu.nl (2016-03-12)

The CL is here: https://codereview.chromium.org/1642283002
but the (Blink) reviewers are not very responsive.

### bu...@chromium.org (2016-03-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb

commit 43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb
Author: rob <rob@robwu.nl>
Date: Sat Mar 19 01:05:01 2016

Deal with frame removal by content scripts

Blink and the RenderFrame implementations are currently not prepared to deal
with frame detachments in their callbacks. Consequently, extension code
(content scripts, chrome.app.window.create) that run arbitrary code in the
"document element created" and "document loaded" notifications may result in
unexpected invalidation of memory, resulting in a UAF.

This patch fixes the bug by moving all code that runs untrusted code from
observers to dedicated callbacks, which are only run at a safe point.
All document parsers in Blink have been modified to make sure that they still
work even when the document creation is interrupted by frame removal.

An extensive set of tests for all different kinds of documents, frame removal
methods (e.g. synchronously / in mutation events / ...) and injection points
(document start/end) have been added to avoid regressions.

BUG=582008

Review URL: https://codereview.chromium.org/1642283002

Cr-Commit-Position: refs/heads/master@{#382162}

[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/browser/extensions/execute_script_apitest.cc
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/renderer/chrome_content_renderer_client.cc
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/renderer/chrome_content_renderer_client.h
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/renderer/extensions/chrome_extensions_renderer_client.cc
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/renderer/extensions/chrome_extensions_renderer_client.h
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/about_blank_frame.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/audio.oga
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/audio.oga.mock-http-headers
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/audio_frame.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/empty.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/empty_frame.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/flag_document_end.js
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/image.png
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/image_frame.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/manifest.json
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/no_url_frame.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/plain.txt
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/plugin_file.pdf
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/plugin_file.pdf.mock-http-headers
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/plugin_frame.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/remove_self.js
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/srcdoc_html_frame.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/srcdoc_text_frame.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/test.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/test.js
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/txt_frame.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/video.ogv
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/video.ogv.mock-http-headers
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/video_frame.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/xhtml_document.xhtml
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/xhtml_document.xhtml.mock-http-headers
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/xhtml_frame.html
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/xml_document.xml
[add] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/chrome/test/data/extensions/api_test/executescript/destructive/xml_frame.html
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/content/public/renderer/content_renderer_client.h
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/content/renderer/mojo_bindings_controller.cc
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/content/renderer/mojo_bindings_controller.h
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/content/renderer/render_frame_impl.h
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/extensions/renderer/dispatcher.cc
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/extensions/renderer/dispatcher.h
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/extensions/renderer/extension_frame_helper.cc
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/extensions/renderer/extension_frame_helper.h
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/extensions/renderer/render_frame_observer_natives.cc
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/extensions/renderer/script_injection_manager.cc
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/extensions/shell/renderer/shell_content_renderer_client.cc
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/extensions/shell/renderer/shell_content_renderer_client.h
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/core/html/ImageDocument.cpp
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/core/html/MediaDocument.cpp
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/core/html/PluginDocument.cpp
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/core/html/parser/HTMLConstructionSite.cpp
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/core/html/parser/HTMLTreeBuilder.cpp
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/core/html/parser/TextDocumentParser.cpp
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/core/loader/DocumentLoader.cpp
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/core/loader/EmptyClients.h
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/core/loader/FrameLoader.h
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/core/loader/FrameLoaderClient.h
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/core/xml/parser/XMLDocumentParser.cpp
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/web/FrameLoaderClientImpl.cpp
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/Source/web/FrameLoaderClientImpl.h
[modify] https://crrev.com/43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb/third_party/WebKit/public/web/WebFrameClient.h


### ro...@robwu.nl (2016-03-19)

Finally, fixed.

I'll let this fix bake for a few days and then request a merge.

### cl...@chromium.org (2016-03-19)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ro...@robwu.nl (2016-03-23)

Requesting approval for merging 43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb.

### ti...@google.com (2016-03-23)

Your change meets the bar and is auto-approved for M50 (branch: 2661)

### bu...@chromium.org (2016-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9eaa751c333792682865e0705444eca748899637

commit 9eaa751c333792682865e0705444eca748899637
Author: Rob Wu <rob@robwu.nl>
Date: Wed Mar 23 17:04:19 2016

Deal with frame removal by content scripts

Blink and the RenderFrame implementations are currently not prepared to deal
with frame detachments in their callbacks. Consequently, extension code
(content scripts, chrome.app.window.create) that run arbitrary code in the
"document element created" and "document loaded" notifications may result in
unexpected invalidation of memory, resulting in a UAF.

This patch fixes the bug by moving all code that runs untrusted code from
observers to dedicated callbacks, which are only run at a safe point.
All document parsers in Blink have been modified to make sure that they still
work even when the document creation is interrupted by frame removal.

An extensive set of tests for all different kinds of documents, frame removal
methods (e.g. synchronously / in mutation events / ...) and injection points
(document start/end) have been added to avoid regressions.

BUG=582008

Review URL: https://codereview.chromium.org/1642283002

Cr-Commit-Position: refs/heads/master@{#382162}
(cherry picked from commit 43ea0649d4b70fdcf3e9fa5c03aee1bbba0b04bb)

Review URL: https://codereview.chromium.org/1825873002 .

Cr-Commit-Position: refs/branch-heads/2661@{#358}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/browser/extensions/execute_script_apitest.cc
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/renderer/chrome_content_renderer_client.cc
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/renderer/chrome_content_renderer_client.h
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/renderer/extensions/chrome_extensions_renderer_client.cc
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/renderer/extensions/chrome_extensions_renderer_client.h
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/about_blank_frame.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/audio.oga
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/audio.oga.mock-http-headers
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/audio_frame.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/empty.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/empty_frame.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/flag_document_end.js
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/image.png
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/image_frame.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/manifest.json
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/no_url_frame.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/plain.txt
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/plugin_file.pdf
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/plugin_file.pdf.mock-http-headers
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/plugin_frame.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/remove_self.js
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/srcdoc_html_frame.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/srcdoc_text_frame.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/test.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/test.js
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/txt_frame.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/video.ogv
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/video.ogv.mock-http-headers
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/video_frame.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/xhtml_document.xhtml
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/xhtml_document.xhtml.mock-http-headers
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/xhtml_frame.html
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/xml_document.xml
[add] https://crrev.com/9eaa751c333792682865e0705444eca748899637/chrome/test/data/extensions/api_test/executescript/destructive/xml_frame.html
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/content/public/renderer/content_renderer_client.h
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/content/renderer/mojo_bindings_controller.cc
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/content/renderer/mojo_bindings_controller.h
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/content/renderer/render_frame_impl.h
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/extensions/renderer/dispatcher.cc
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/extensions/renderer/dispatcher.h
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/extensions/renderer/extension_frame_helper.cc
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/extensions/renderer/extension_frame_helper.h
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/extensions/renderer/render_frame_observer_natives.cc
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/extensions/renderer/script_injection_manager.cc
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/extensions/shell/renderer/shell_content_renderer_client.cc
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/extensions/shell/renderer/shell_content_renderer_client.h
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/core/html/ImageDocument.cpp
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/core/html/MediaDocument.cpp
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/core/html/PluginDocument.cpp
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/core/html/parser/HTMLConstructionSite.cpp
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/core/html/parser/HTMLTreeBuilder.cpp
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/core/html/parser/TextDocumentParser.cpp
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/core/loader/DocumentLoader.cpp
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/core/loader/EmptyClients.h
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/core/loader/FrameLoader.cpp
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/core/loader/FrameLoader.h
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/core/loader/FrameLoaderClient.h
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/core/xml/parser/XMLDocumentParser.cpp
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/web/FrameLoaderClientImpl.cpp
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/Source/web/FrameLoaderClientImpl.h
[modify] https://crrev.com/9eaa751c333792682865e0705444eca748899637/third_party/WebKit/public/web/WebFrameClient.h


### ro...@robwu.nl (2016-03-23)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-23)

This will miss the next M49 (due tomorrow and cut yesterday) but let's merge to M49 to catch any additional stable builds that ship. 

### ti...@google.com (2016-03-24)

[Automated comment] Request affecting a post-stable build (M49), manual review required.

### ss...@google.com (2016-03-29)

Merge approved for M49 (branch 2623)

### ss...@google.com (2016-03-31)

It looks like this change is introducing a crash (crbug.com/590634, c#51) and the root cause is not verified, since we are still seeing the crash after the "fix" landed. Can we please close on that issue, before we merge this change in? Removing the merge-approval for now. Please re-request once we can verify that we have a fix for the crash introduced. 

### ss...@google.com (2016-03-31)

timwillis@, if I have messed up some Security label workflow by removing the approval above(c#31), please take a look and fix if needed. 

### ro...@robwu.nl (2016-03-31)

I triaged the new crash from https://crbug.com/chromium/590634, and it appears unrelated to my patch, so I'm requesting a merge again.

(and please cc me on the other issue. When I assigned the bug to someone else, I forgot to cc me and now I cannot access the issue any more).

### ti...@google.com (2016-03-31)

[Automated comment] Request affecting a post-stable build (M49), manual review required.

### ss...@google.com (2016-04-05)

timwillis@, this is a very large change for a post-stable release. Does this need to go into M49?

### ti...@google.com (2016-04-05)

#33 - cc'd you on https://crbug.com/chromium/590634

#35 - if you're uncomfortable taking this patch into M49 from a stability perspective and considering that M50 early stable is next week, I'm okay with delaying until M50 and not merging this to M-49. 

### ss...@google.com (2016-04-05)

Ok, let's please wait till M50 in that case. This is a rather large change and there is some speculation about whether or not the new crash is related to this, so it is risky to get this in M49, when M50 is just a couple weeks away. timwillis@, can you please either reject this merge or remove the merge request, whatever aligns to the security process?

### ss...@google.com (2016-04-05)

Rejecting as per c#36, so this doesn't show up in my radar anymore.

### ro...@robwu.nl (2016-04-05)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-13)

Thanks for the report! This one qualified for a $1500 reward.

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/582008?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083564)*
