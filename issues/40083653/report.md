# Heap-use-after-free in LoadWatcher::CallbackAndDie (chrome.app.window.create)

| Field | Value |
|-------|-------|
| **Issue ID** | [40083653](https://issues.chromium.org/issues/40083653) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Apps, Platform>Extensions |
| **CVE IDs** | CVE-2016-1635 |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-02-08 |
| **Bounty** | $2,000.00 |

## Description

Chrome Version: 48.0.2564.103 (stable, and earlier) and 50.0.2633.0 (HEAD)

- extensions::LoadWatcher::CallbackAndDie is called when DidCreateDocumentElement is triggered.
- CallbackAndDie calls a user-defined JavaScript function and then deletes the LoadWatcher instance.
- JavaScript code can easily replace the document (e.g. via document.close/write)
- DidCreateDocumentElement is triggered whenever a document is created/replaced.
- The LoadWatcher instance + user-defined callback code is instantiated by the chrome.app.window.create app method.

All together, this means that malicious Chrome apps can cause CallbackAndDie to be called re-entrantly when the callback of chrome.apps.window.create replaces the document of the new app window, which results in a use-after-free (and double-frees).

See the attached app (manifest.json and background.js), and the stack trace generated with ASAN.
The head of the trace is repeated a couple of times, which shows that the PoC was able to trigger CallbackAndDie multiple times at one run.

==10==ERROR: AddressSanitizer: heap-use-after-free on address 0x6040001542d0 at pc 0x561616d0218b bp 0x7ffecbfe7110 sp 0x7ffecbfe7108
READ of size 8 at 0x6040001542d0 thread T0 (chrome)
    #0 0x561616d0218a in CallbackAndDie extensions/renderer/render_frame_observer_natives.cc:54:5
    #1 0x561615439f50 in didCreateDocumentElement content/renderer/render_frame_impl.cc:3351:7
    #2 0x56160f450872 in documentElementAvailable third_party/WebKit/Source/web/FrameLoaderClientImpl.cpp:181:9
    #3 0x561610cbe283 in dispatchDocumentElementAvailableIfNeeded third_party/WebKit/Source/core/html/parser/HTMLConstructionSite.cpp:387:9
    #4 0x561610cbe283 in insertHTMLHtmlStartTagBeforeHTML third_party/WebKit/Source/core/html/parser/HTMLConstructionSite.cpp:401:0
    #5 0x561610bda60b in defaultForBeforeHTML third_party/WebKit/Source/core/html/parser/HTMLTreeBuilder.cpp:2536:5
    #6 0x561610bda60b in processCharacterBuffer third_party/WebKit/Source/core/html/parser/HTMLTreeBuilder.cpp:2295:0
    #7 0x561610bbd6fa in processCharacter third_party/WebKit/Source/core/html/parser/HTMLTreeBuilder.cpp:2257:5
    #8 0x561610bbd6fa in processToken third_party/WebKit/Source/core/html/parser/HTMLTreeBuilder.cpp:404:0
    #9 0x561610bba81b in constructTree third_party/WebKit/Source/core/html/parser/HTMLTreeBuilder.cpp:382:9
    #10 0x561610b07847 in constructTreeFromHTMLToken third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:719:5
    #11 0x561610b00320 in pumpTokenizer third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:664:9
    #12 0x561610b0ad59 in pumpTokenizerIfPossible third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:302:5
    #13 0x561610b0ad59 in insert third_party/WebKit/Source/core/html/parser/HTMLDocumentParser.cpp:768:0
    #14 0x5616105f4e9a in write third_party/WebKit/Source/core/dom/Document.cpp:2877:5
    #15 0x5616105f52fe in write third_party/WebKit/Source/core/dom/Document.cpp:2882:5
    #16 0x5616105f60e2 in write third_party/WebKit/Source/core/dom/Document.cpp:2899:5
    #17 0x56161292f479 in writeMethod /cr/src/out_asan/Release/gen/blink/bindings/core/v8/V8Document.cpp:4598:5
    #18 0x56161292f479 in writeMethodCallback /cr/src/out_asan/Release/gen/blink/bindings/core/v8/V8Document.cpp:4608:0
    #19 0x56160ee44fd5 in Call v8/src/arguments.cc:33:3
    #20 0x56160e1042fe in HandleApiCallHelper<false> v8/src/builtins.cc:3580:34
    #21 0x56160e124ca4 in Builtin_Impl_HandleApiCall v8/src/builtins.cc:3604:3
    #22 0x56160e124ca4 in Builtin_HandleApiCall v8/src/builtins.cc:3601:0


## Attachments

- [manifest.json](attachments/manifest.json) (application/json, 168 B)
- [asan.log](attachments/asan.log) (text/plain, 35.1 KB)
- [background.js](attachments/background.js) (text/javascript, 545 B)

## Timeline

### dc...@chromium.org (2016-02-09)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-02-09)

Patch: https://codereview.chromium.org/1684953002/

### ri...@chromium.org (2016-02-10)

Thanks for the great report/working on a fix! Feel free to ping here if you need any reviewers added to this bug.

### ri...@chromium.org (2016-02-10)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-02-10)

Adding reviewers from https://codereview.chromium.org/1642283002/ (note: this is NOT the crbug for that CL), to give more context on whether to use microtasks or not.

This bug is about a UAF caused by re-entrancy via chrome.app.window.create. I tried to fix it by posting a task to the message loop, but that caused multiple tests to fail, because these tests assumed that the document created by chrome.app.window.create has not finished loading yet (which is not true if the callback is called after a PostTask).

The similarity with the CL that you were reviewing is that in both cases, untrusted JavaScript code has to be run after the document root is inserted. In my first patch, I allowed RenderFrameObserver::DidCreateDocumentElement to invalidate the RenderFrame while notifying the observers (previously, invalid memory was accessed in the observers if the frame was detached during the notification) (https://codereview.chromium.org/1642283002/patch/60001/70030).

Then I tried microtasks because it was suggested by a reviewer. But now I think that microtasks are not suitable, due to the disadvantages in https://codereview.chromium.org/1642283002/#msg13, and because it makes code that wants to inject scripts ASAP more difficult to understand and maintain.

Now you've got more context, please continue reviewing https://codereview.chromium.org/1642283002/ :)

### ro...@robwu.nl (2016-02-10)

Devlin: I'm going to submit https://codereview.chromium.org/1684953002/ for review.

There were multiple issues with that bit of code:
- Re-entrancy of CallbackAndDie (this issue)
- Using a raw pointer that is not guaranteed to be valid (https://crbug.com/chromium/568130)
- Not accounting for detachment of frames (similar to https://crbug.com/chromium/582008).

I've fixed the first two bugs, the last one will be fixed together with the fix for https://crbug.com/chromium/582008 (because these have the same root causes).

### bu...@chromium.org (2016-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5a15b72a270b514cd442872221a788a303bdaa88

commit 5a15b72a270b514cd442872221a788a303bdaa88
Author: rob <rob@robwu.nl>
Date: Wed Feb 10 22:45:57 2016

Fix re-entrancy and lifetime issue in RenderFrameObserverNatives::OnDocumentElementCreated

BUG=585268,568130

Review URL: https://codereview.chromium.org/1684953002

Cr-Commit-Position: refs/heads/master@{#374758}

[modify] http://crrev.com/5a15b72a270b514cd442872221a788a303bdaa88/extensions/renderer/render_frame_observer_natives.cc
[modify] http://crrev.com/5a15b72a270b514cd442872221a788a303bdaa88/extensions/renderer/render_frame_observer_natives.h


### ro...@robwu.nl (2016-02-16)

Verified that the bug is Fixed with 50.0.2653.0 using the reproduction steps that I posted in the initial report.

Now I still get a crash, but it has a different root cause, and it will be resolved once https://crbug.com/chromium/582008 is fixed.

Received signal 11 SEGV_MAPERR 0000000001e8
#0 0x558eb884656b base::debug::(anonymous namespace)::StackDumpSignalHandler()
#1 0x7f494405dd60 <unknown>
#2 0x558eb6c44c17 blink::Document::loader()
#3 0x558eb6dbb625 blink::HTMLDocumentParser::startBackgroundParser()
#4 0x558eb6dbb570 blink::HTMLDocumentParser::forcePlaintextForTextDocument()
#5 0x558eb6dedc41 blink::TextDocumentParser::insertFakePreElement()
#6 0x558eb6dedb2f blink::TextDocumentParser::appendBytes()
#7 0x558eb70ea6b7 blink::DocumentWriter::addData()
#8 0x558eb70e2c30 blink::DocumentLoader::commitData()
#9 0x558eb70e3d3b blink::DocumentLoader::processData()
#10 0x558eb70e3c18 blink::DocumentLoader::dataReceived()

Requesting merge of 5a15b72a270b514cd442872221a788a303bdaa88 to 49.

### ti...@google.com (2016-02-16)

Your change meets the bar and is auto-approved for M49 (branch: 2623)

### go...@chromium.org (2016-02-16)

[Comment Deleted]

### go...@chromium.org (2016-02-16)

Please merge your change to M49 (branch: 2623) before 5:00 PM PST Today [02/16] if you would like to make it to M49 Beta push tomorrow [02/17].

### cl...@chromium.org (2016-02-16)

[Empty comment from Monorail migration]

### rd...@chromium.org (2016-02-16)

Rob, will you be able to merge this in by 5p PST?  If not, I can do it.

### bu...@chromium.org (2016-02-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/680671c19fb1e808dec7cfa23148d82203c3ac2f

commit 680671c19fb1e808dec7cfa23148d82203c3ac2f
Author: Rob Wu <rob@robwu.nl>
Date: Tue Feb 16 22:40:27 2016

Fix re-entrancy and lifetime issue in RenderFrameObserverNatives::OnDocumentElementCreated

BUG=585268,568130

Review URL: https://codereview.chromium.org/1684953002

Cr-Commit-Position: refs/heads/master@{#374758}
(cherry picked from commit 5a15b72a270b514cd442872221a788a303bdaa88)

Review URL: https://codereview.chromium.org/1702783002 .

Cr-Commit-Position: refs/branch-heads/2623@{#414}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[modify] http://crrev.com/680671c19fb1e808dec7cfa23148d82203c3ac2f/extensions/renderer/render_frame_observer_natives.cc
[modify] http://crrev.com/680671c19fb1e808dec7cfa23148d82203c3ac2f/extensions/renderer/render_frame_observer_natives.h


### bu...@chromium.org (2016-02-17)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/680671c19fb1e808dec7cfa23148d82203c3ac2f

commit 680671c19fb1e808dec7cfa23148d82203c3ac2f
Author: Rob Wu <rob@robwu.nl>
Date: Tue Feb 16 22:40:27 2016


### mb...@chromium.org (2016-02-22)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-02-22)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-02)

Congratulations - $2,000 for this report. 

Note from the panel: Although you are an active contributor to the code in question, it appears as though you didn't make modifications that are related to this bug, so this report is eligible for reward. Just as a note for future reference, if it does appear that you've made modifications to areas of code that result in a bug, it's unlikely we'll be able to reward in those cases.

CVE-ID to follow. Thanks again Rob!

### ti...@google.com (2016-03-02)

CVE-2016-1635

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-25)

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

This issue was migrated from crbug.com/chromium/585268?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Apps, Platform>Extensions]
[Monorail mergedwith: crbug.com/chromium/585737]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083653)*
