# Security: Use of unvalidated URL in PDF viewer

| Field | Value |
|-------|-------|
| **Issue ID** | [40085645](https://issues.chromium.org/issues/40085645) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF, Internals>Sandbox>SiteIsolation |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-10-09 |
| **Bounty** | $2,500.00 |

## Description

Chrome version: Stable (53.0.2785.116) and latest (56.0.2886.0)

When a PDF is opened in Chrome, the PDFium plugin is used as follows:

(1) <embed> by webpage -> Chrome loads PDF plugin
  (2) PDF plugin loads <iframe> with PDF helper extension.
    (3) PDF helper extension loads <embed> with privileged plugin.
      (4) Privileged plugin trusts any messages from the host.

A limited API is available between (1) and (2); for same-origin PDFs, this includes reading the content of the PDF.
The plugin at (4) cannot be loaded by a web page (after https://crbug.com/chromium/520422).

Now I found that (3) is web-accessible [1] *and* trusts the query string to contain the real URL (originUrl_). This URL is used for multiple security decisions, including but not limited to:
- The originUrl_ can be set to a PDF that redirects elsewhere, and because the helper extension thinks that it's dealing with a same-origin PDF, it will happily leak cross-origin data.
- The API for chrome://print pages is more extensive, it can be used to load any PDF, and be used to open e.g. file:-URLs in a new tab.

I have attached a PoC for the above two examples.
1. Start server.py (this is for the second example).
2. If using Chrome 53, start with --isolate-extensions to force Site isolation for extensions (this is on a field trial in 53, and enabled by default in Chrome 54). This is needed to allow the chrome:// resources in the helper extension to load (otherwise the frame will run in the unprivileged tab process).
3. Open http://localhost:8100
4. Click on the second button, and see the content of a PDF at another origin being printed in the page.
5. Click on the first button, and see file:///etc/passwd (or C:\ on Windows) being opened in a new tab (this example does not work in Chrome 54+ any more because the helper extension can no longer embed the chrome://print plugin).


TL;DR Use of unvalidated URL, leading to multiple issues including a same origin bypass. Site isolation made the vulnerability exploitable.


[1] https://chromium.googlesource.com/chromium/src/+/bbf2420306f6d0a3c85d10a4115ab254b3912162/chrome/browser/resources/pdf/manifest.json#21
[2] https://chromium.googlesource.com/chromium/src/+/383ff955ecb5eddb6a91eae873f617f814426cc4/chrome/browser/resources/pdf/browser_api.js#182

## Attachments

- [index.html](attachments/index.html) (text/plain, 3.7 KB)
- [server.py](attachments/server.py) (text/plain, 817 B)
- [index.html](attachments/index_53236548.html) (text/plain, 1.0 KB)

## Timeline

### ro...@robwu.nl (2016-10-09)

Patch: https://codereview.chromium.org/2407713002

### ts...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### th...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-10-11)

I can't repro this on 53.0.2785.143 with --isolate-extensions. The embedded PDFs either fail to load or I see a blank PDF.

### ro...@robwu.nl (2016-10-11)

The PoC includes some browser version detection, and switches to a different method in Chrome 54. The post-53 code path is equivalent to opening data:application/pdf, in a new tab. Maybe whatever that necessitated the logic for 54+ is also needed in 53.0.2785.143. Try opening this tab and retry the PoC.

And when starting with --isolate-extensions, make sure that all Chrome processes were shut down before you started chrome. Otherwise the flag will not apply.

I tried the PoC with 53, 54, 55 and 56 before reporting.
Do note that the PoC that opens a file:-URL does not work in 54+ (maybe also not in 53.0.2785.143?). I haven't investigated why because the other example (reading data cross-origin) is much more severe and already shows why this should be fixed.

### ra...@chromium.org (2016-10-11)

Ah I realized I was running the standard python server instead of your one which handles redirects. Sorry for the confusion - I think the POCs probably work (at least the ones on the other bug did).

### cr...@chromium.org (2016-10-11)

Thanks for the report!

Just to clarify, --isolate-extensions is not enabled at all in M53.  It's enabled via Finch trial in M54 and enabled by default in M55.

That said, we should definitely get this fixed.

### bu...@chromium.org (2016-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c72f59f36a16c0cb64e0eebfc0999a09250740f0

commit c72f59f36a16c0cb64e0eebfc0999a09250740f0
Author: rob <rob@robwu.nl>
Date: Fri Oct 14 09:35:16 2016

Limit PDF helper extension to print preview only

These days, the helper extension is only used by the print preview.
So make sure that the helper extension is only activated in print
previews and fall back to the standard MimeHandler otherwise.
When the helper extension is unexpectedly loaded directly instead
of through the mime handler, the extension will fail to initialize.
This is totally desired!

BUG=654280
TEST=See bug report, also confirmed that print preview still works.
R=thestig@chromium.org
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2407713002
Cr-Commit-Position: refs/heads/master@{#425280}

[modify] https://crrev.com/c72f59f36a16c0cb64e0eebfc0999a09250740f0/chrome/browser/pdf/pdf_extension_test.cc
[modify] https://crrev.com/c72f59f36a16c0cb64e0eebfc0999a09250740f0/chrome/browser/resources/pdf/browser_api.js
[modify] https://crrev.com/c72f59f36a16c0cb64e0eebfc0999a09250740f0/chrome/browser/resources/pdf/pdf.js
[modify] https://crrev.com/c72f59f36a16c0cb64e0eebfc0999a09250740f0/content/public/test/browser_test_utils.cc
[modify] https://crrev.com/c72f59f36a16c0cb64e0eebfc0999a09250740f0/content/public/test/browser_test_utils.h
[modify] https://crrev.com/c72f59f36a16c0cb64e0eebfc0999a09250740f0/content/public/test/content_browser_test_utils.cc
[modify] https://crrev.com/c72f59f36a16c0cb64e0eebfc0999a09250740f0/content/public/test/content_browser_test_utils.h


### th...@chromium.org (2016-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-15)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-10-17)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-10-17)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### bu...@chromium.org (2016-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/37efdf4c7fdae4c604ad0b71781c36182b1517f0

commit 37efdf4c7fdae4c604ad0b71781c36182b1517f0
Author: Rob Wu <rob@robwu.nl>
Date: Mon Oct 17 11:58:22 2016

Limit PDF helper extension to print preview only

These days, the helper extension is only used by the print preview.
So make sure that the helper extension is only activated in print
previews and fall back to the standard MimeHandler otherwise.
When the helper extension is unexpectedly loaded directly instead
of through the mime handler, the extension will fail to initialize.
This is totally desired!

BUG=654280
TEST=See bug report, also confirmed that print preview still works.
R=thestig@chromium.org
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2407713002
Cr-Commit-Position: refs/heads/master@{#425280}
(cherry picked from commit c72f59f36a16c0cb64e0eebfc0999a09250740f0)

Review URL: https://codereview.chromium.org/2423983002 .

Cr-Commit-Position: refs/branch-heads/2883@{#147}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/chrome/browser/pdf/pdf_extension_test.cc
[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/chrome/browser/resources/pdf/browser_api.js
[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/chrome/browser/resources/pdf/pdf.js
[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/content/public/test/browser_test_utils.cc
[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/content/public/test/browser_test_utils.h
[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/content/public/test/content_browser_test_utils.cc
[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/content/public/test/content_browser_test_utils.h


### aw...@chromium.org (2016-10-18)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-10-24)

The exploit from the initial report relied on site isolation to work, but the vulnerability can also be exploited without site isolation:
1. Download server.py from the initial report plus the attached index.html in the same folder.
2. Start the server: python server.py 
3. Visit http://localhost:8100
4. Click on the button.

Result in 54.0.2840.59 (without patch): A cross-origin PDF is briefly loaded, its content is selected and shown by index.html.
Expected (in M55/M56, M54 with patch): the PDF is not opened. 

Requesting a merge of my patch to break the exploit in M54.

### aw...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-10-24)

[Automated comment] Request affecting a post-stable build (M54), manual review required.

### aw...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-10-25)

wfh: Do you think we want to take this for stable? 

### na...@chromium.org (2016-10-25)

If this bug allows reading of files cross-origin, then this is likely in the same realm as "A bypass of the same origin policy for pages that meet several preconditions", which is medium severity bug. Since the fix isn't complex, I think we should take it for M54, though that would require writing a postmortem.

### aw...@chromium.org (2016-10-26)

Downgrading to Medium after discussion with nasko@ and wfh@.

### aw...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/37efdf4c7fdae4c604ad0b71781c36182b1517f0

commit 37efdf4c7fdae4c604ad0b71781c36182b1517f0
Author: Rob Wu <rob@robwu.nl>
Date: Mon Oct 17 11:58:22 2016

Limit PDF helper extension to print preview only

These days, the helper extension is only used by the print preview.
So make sure that the helper extension is only activated in print
previews and fall back to the standard MimeHandler otherwise.
When the helper extension is unexpectedly loaded directly instead
of through the mime handler, the extension will fail to initialize.
This is totally desired!

BUG=654280
TEST=See bug report, also confirmed that print preview still works.
R=thestig@chromium.org
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2407713002
Cr-Commit-Position: refs/heads/master@{#425280}
(cherry picked from commit c72f59f36a16c0cb64e0eebfc0999a09250740f0)

Review URL: https://codereview.chromium.org/2423983002 .

Cr-Commit-Position: refs/branch-heads/2883@{#147}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/chrome/browser/pdf/pdf_extension_test.cc
[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/chrome/browser/resources/pdf/browser_api.js
[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/chrome/browser/resources/pdf/pdf.js
[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/content/public/test/browser_test_utils.cc
[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/content/public/test/browser_test_utils.h
[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/content/public/test/content_browser_test_utils.cc
[modify] https://crrev.com/37efdf4c7fdae4c604ad0b71781c36182b1517f0/content/public/test/content_browser_test_utils.h


### ro...@robwu.nl (2016-11-01)

(not merged, the above bugdroid comment is wrong - https://groups.google.com/a/chromium.org/d/msg/chromium-dev/sJ7gZLqyJ-g/k-CbRUrnBwAJ)

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9fb7fed591eb80fa9653f7d027f004afb8425b17

commit 9fb7fed591eb80fa9653f7d027f004afb8425b17
Author: raymes <raymes@chromium.org>
Date: Wed Nov 09 01:06:29 2016

Improve print preview checks in the PDF plugin

Special functionality is available in the PDF plugin for print preview. We
don't want to allow this functionality to be exposed when not in print
preview as it may have potential security implications. This CL improves
the checks that are used:
1) Check the document URL to determine whether we are in print preview, rather
than the URL that is passed in to load, which could be chosen by an attacker.
2) Add CHECKs to ensure we are in print preview mode and trying to load a print
preview document when print preview messages are received.

Note that we should never get into a state where these checks would be invalid
but this gives us defense in depth.

BUG=654280

Review-Url: https://codereview.chromium.org/2486683002
Cr-Commit-Position: refs/heads/master@{#430802}

[modify] https://crrev.com/9fb7fed591eb80fa9653f7d027f004afb8425b17/pdf/out_of_process_instance.cc
[modify] https://crrev.com/9fb7fed591eb80fa9653f7d027f004afb8425b17/pdf/out_of_process_instance.h


### aw...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-14)

The panel decided to reward an additional $1,000 for this bug.  I'll follow up in email shortly.

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/654280?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Plugins>PDF, Internals>Sandbox>SiteIsolation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085645)*
