# Security: Cross-site read access to PDF files

| Field | Value |
|-------|-------|
| **Issue ID** | [40082671](https://issues.chromium.org/issues/40082671) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ra...@chromium.org |
| **Created** | 2015-08-13 |
| **Bounty** | $4,000.00 |

## Description

The out-of-process viewer exposes an API when its MIME-type is set to application/x-google-chrome-pdf, presumably to support the print preview.

Among the supported API is a method to select all text and get the contents of the selection. This allows any web page to read the contents of a PDF file from any source.

I have attached a proof of concept.

1. Open the page.
2. Input the URL of a PDF file (I've used the Bitcoin paper as an example).
3. Click on the "Show content" button.
4. The contens of the PDF will be displayed in the PDF.

This can be fully automated, websites could scan for popular URLs and automatically read the contents of a PDF. The only defence for users is to disable plugin loading by default. There are three settings, "Run all plugin content", "Detect and run important plugin content" and "Let me choose when to run plugin content". Only the last option protects users from this exploit.

## Attachments

- [pdf-universal-read.html](attachments/pdf-universal-read.html) (text/html, 1.2 KB)
- [verified-345289.png](attachments/verified-345289.png) (image/png, 24.9 KB)
- [embed.html](attachments/embed.html) (text/html, 363 B)
- [verified-345289-embed.png](attachments/verified-345289-embed.png) (image/png, 56.5 KB)

## Timeline

### ro...@robwu.nl (2015-08-13)

Typo.
"4. The contens of the PDF will be displayed in the PDF"
should be
"4. The contents of the PDF will be displayed in the text field"

### ro...@robwu.nl (2015-08-13)

This bug was introduced with d914d7d0903eda0b9ae77c5d0adb7a6a61c95e13 (42.0.2275.0), and is still affecting the ToT.

### ra...@chromium.org (2015-08-17)

I think this has actually always been possible by using the accessibility API that is exposed in our PDF plugin? 

I agree that we should fix it though. If we restricted these API calls to same-origin callers, it looks like it would break ChromeVox for cross-origin PDFs...so I'm not sure what to do there.

https://cs.corp.google.com/#clankium/src/chrome/browser/resources/chromeos/chromevox/chromevox/injected/pdf_processor.js&q=getAccessibilityJSON&type=cs&l=94


dmazzoni@: Do you know if I'm right? Do you have thoughts? 

### aa...@google.com (2015-08-22)

Raymes, Dominic, this is high severity cross origin bypass, we need to fix it asap. M-45 release date is early september, so we should get a fix in there soon.

### ro...@robwu.nl (2015-08-23)

[Comment Deleted]

### ro...@robwu.nl (2015-08-24)

This bug is not limited to the application/x-google-chrome-pdf MIME-type.
When a PDF is loaded using application/pdf (in <object> or <embed>), then the embedded PDF component extension will still relay messages received by object.postMessage(...), and responses will be send back via parent.postMessage. This allows the page that embeds the PDF to read the PDF data.

To fix the bug, I suggest the following:
1. application/x-google-chrome-pdf should not expose leaky APIs to web content, because it is merely an internal implementation detail used by print preview and the PDF component extension (introduced in 6ab4ef968bf9d10bd469ddb418b3e36edff16816).

2. The PDF component extension should stop relaying messages from untrusted web content to the PDF plugin. Check whether event.origin is whitelisted (Print preview or ChromeVox).

3. ChromeVox will break because the print processor runs in the page.
To solve this, I found two alternative options:
- Insert an iframe (containing a page from ChromeVox's origin) that directly communicates with the PDF component extension, via a MessagePort. The sender and receiver have to mutually authenticate each other, this can be done by communicating a random value over another channel (e.g. extension message passing API).
- Run ChromeVox in the component extension, and directly communicate between the component extension and ChromeVox.

I have already written a patch for 1 and 2, for option 3 I'm thinking of the second option.
Raymes, WDYT?

### ra...@chromium.org (2015-08-24)

Hey Rob, I have a fix in progress, I'm just writing tests for it. 

I don't have a fix for 3 above though so feel free to write a patch for this. I agree that the second option seems better.

Thanks for looking at this!

### bu...@chromium.org (2015-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fff450abc4e2fb330ba700547a8e6a7b0fb90a6e

commit fff450abc4e2fb330ba700547a8e6a7b0fb90a6e
Author: raymes <raymes@chromium.org>
Date: Tue Aug 25 06:02:08 2015

Prevent leaking PDF data cross-origin

BUG=520422

Review URL: https://codereview.chromium.org/1311973002

Cr-Commit-Position: refs/heads/master@{#345267}

[modify] http://crrev.com/fff450abc4e2fb330ba700547a8e6a7b0fb90a6e/chrome/browser/pdf/pdf_extension_test.cc
[modify] http://crrev.com/fff450abc4e2fb330ba700547a8e6a7b0fb90a6e/chrome/browser/resources/pdf/pdf.js
[modify] http://crrev.com/fff450abc4e2fb330ba700547a8e6a7b0fb90a6e/pdf/out_of_process_instance.cc


### ro...@robwu.nl (2015-08-25)

Your patch allows same-origin documents to use the PDF scripting API, which means that ChromeVox will still work if the PDF is hosted at the same origin.

ChromeVox was designed to work for the scenario where the PDF is directly opened in the (top-level) frame, so there is no regression in the behavior of ChromeVox. (I'm basing my assumption on the fact that the text layer covers the whole page, and the "Show original" link navigates to the PDF after clicking on it, even if the document's URL is different from the URL of the embedded PDF (https://chromium.googlesource.com/chromium/src/+/391f56c8f1e8da3874c54aa4d6aff1d9c736518d/chrome/browser/resources/chromeos/chromevox/chromevox/injected/pdf_processor.js#150)).

I've verified that the patch fixes the bug, as follows:
1. Web content can no longer use the <embed type="application/x-google-chrome-pdf"> (using the test case from the initial report, I now get a "Could not load Chromium PDF Viewer" infobar, see verified-345289.png).

2. Web content can no longer receive sensitive messages from <embed type="application/pdf"> (visit embed.html, and observe that errors are displayed (verified-345290-embed.png) instead of the actual messages).

3. The above is true, even for redirected documents. I tested this as follows:
 - Edit embed.html and change the PDF URL to http://localhost:4444/foo.pdf.
 - Use netcat (nc -l -p 4444)
 - Open embed.html in the latest version of Chromium
 - Go back to the terminal where netcat was started, and respond with a 302 redirect to a different PDF file.
 - Go back to Chrome and observe that postMessage error is still printed, and the actual origin of the PDF is used instead of the original URL that replied with a redirect.

### ra...@chromium.org (2015-08-26)

Thanks for testing Rob, very helpful. I will merge this tomorrow assuming there are no issues by then.

### ra...@chromium.org (2015-08-26)

[Empty comment from Monorail migration]

### pe...@google.com (2015-08-26)

[Automated comment] Less than 2 weeks to go before stable on M45, manual review required.

### ro...@robwu.nl (2015-08-27)

Raymes, your patch landed in 47.0.2494.0, so it should first be merged with 46, then 45.

### pe...@google.com (2015-08-27)

Approved for M46 (branch: 2490)

### bu...@chromium.org (2015-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a42545fa19dcbdca14c7e53e214b05b3d9356af5

commit a42545fa19dcbdca14c7e53e214b05b3d9356af5
Author: Raymes Khoury <raymes@chromium.org>
Date: Fri Aug 28 23:26:44 2015

Prevent leaking PDF data cross-origin

BUG=520422

Review URL: https://codereview.chromium.org/1311973002

Cr-Commit-Position: refs/heads/master@{#345267}
(cherry picked from commit fff450abc4e2fb330ba700547a8e6a7b0fb90a6e)

Review URL: https://codereview.chromium.org/1308323007 .

Cr-Commit-Position: refs/branch-heads/2490@{#78}
Cr-Branched-From: 7790a3535f2a81a03685eca31a32cf69ae0c114f-refs/heads/master@{#344925}

[modify] http://crrev.com/a42545fa19dcbdca14c7e53e214b05b3d9356af5/chrome/browser/pdf/pdf_extension_test.cc
[modify] http://crrev.com/a42545fa19dcbdca14c7e53e214b05b3d9356af5/chrome/browser/resources/pdf/pdf.js
[modify] http://crrev.com/a42545fa19dcbdca14c7e53e214b05b3d9356af5/pdf/out_of_process_instance.cc


### ra...@chromium.org (2015-08-31)

[Empty comment from Monorail migration]

### pe...@google.com (2015-08-31)

[Automated comment] Less than 2 weeks to go before stable on M45, manual review required.

### ti...@google.com (2015-08-31)

Possibly could take this in a patch release to M45. 

### ro...@robwu.nl (2015-08-31)

Tim, why do you want to schedule the patch for a patch release instead of the first stable release? The patch is relatively safe, has had enough time to bake, and it has been verified (#9).

Does this bug qualify for being a release blocker, or is that reserved for (security) bugs that are even worse?

### bu...@chromium.org (2015-09-01)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/a42545fa19dcbdca14c7e53e214b05b3d9356af5

commit a42545fa19dcbdca14c7e53e214b05b3d9356af5
Author: Raymes Khoury <raymes@chromium.org>
Date: Fri Aug 28 23:26:44 2015


### am...@google.com (2015-09-01)

Merge is approved for M45 branch 2454.


### bu...@chromium.org (2015-09-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/398696033a3f2e954aea68fdec10becb836a80b4

commit 398696033a3f2e954aea68fdec10becb836a80b4
Author: Raymes Khoury <raymes@chromium.org>
Date: Wed Sep 02 00:20:49 2015

Prevent leaking PDF data cross-origin

BUG=520422

Review URL: https://codereview.chromium.org/1311973002

Cr-Commit-Position: refs/heads/master@{#345267}
(cherry picked from commit fff450abc4e2fb330ba700547a8e6a7b0fb90a6e)

Review URL: https://codereview.chromium.org/1316803003 .

Cr-Commit-Position: refs/branch-heads/2454@{#446}
Cr-Branched-From: 12bfc3360892ec53cd00fc239a47e5298beb063b-refs/heads/master@{#338390}

[modify] http://crrev.com/398696033a3f2e954aea68fdec10becb836a80b4/chrome/browser/pdf/pdf_extension_test.cc
[modify] http://crrev.com/398696033a3f2e954aea68fdec10becb836a80b4/chrome/browser/resources/pdf/pdf.js
[modify] http://crrev.com/398696033a3f2e954aea68fdec10becb836a80b4/pdf/out_of_process_instance.cc


### ti...@google.com (2015-09-10)

#19 - bugs also need bake time on Beta as well before heading across to Stable as well. 

The merge at #22 made it to stable but didn't ship in the initial release of M45, so it's going to go out in a patch release.

### in...@chromium.org (2015-09-15)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-09-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-25)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-14)

Tagging for inclusion in M46 release notes (subject to reward panel decision).

### ro...@robwu.nl (2015-10-26)

The first patch release for 46 was published last week [1], but without a reference to this bug. Is this bug still on the radar of the reward panel?

 [1]: https://googlechromereleases.blogspot.com/2015/10/stable-channel-update_22.html

### ti...@google.com (2015-11-10)

As discussed via email, your bug is listed in today's release notes: http://googlechromereleases.blogspot.com/2015/11/stable-channel-update.html

$4000 for this report. Panel notes: High quality info leak with functioning exploit.

Thanks for another great report!

### cl...@chromium.org (2015-12-01)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ceb0e8fda9c584873757779437948e929a95b3c9

commit ceb0e8fda9c584873757779437948e929a95b3c9
Author: dmazzoni <dmazzoni@chromium.org>
Date: Thu Jan 07 22:13:21 2016

Run ChromeVox PDF extractor within Chrome's PDF extension

Previously it ran on the pdf page, outside of the extension.
By running inside the extension it works with local files
again.

BUG=574918,520422

Review URL: https://codereview.chromium.org/1561883004

Cr-Commit-Position: refs/heads/master@{#368172}

[modify] http://crrev.com/ceb0e8fda9c584873757779437948e929a95b3c9/chrome/browser/resources/chromeos/chromevox/chromevox/injected/pdf_processor.js


### pa...@chromium.org (2016-01-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-01-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### dc...@chromium.org (2017-10-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/520422?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082671)*
