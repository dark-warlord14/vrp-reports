# Security: XSS in chrome://downloads, enables extensions to run any program

| Field | Value |
|-------|-------|
| **Issue ID** | [40086079](https://issues.chromium.org/issues/40086079) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-11-25 |
| **Bounty** | $5,000.00 |

## Description

Chrome version: 54.0.2840.90 (stable), 55.0.2883.59 (beta), 57.0.2931.0 (Canary)

There is a XSS vulnerability in chrome://downloads that allows an extension to run a program without user interaction. The only requirement is that the user installs or upgrades to a malicious extension (this is not a difficult requirement).
In fact, https://crbug.com/chromium/671007 satisfies this requirement with low user interaction. Together, web pages can run arbitrary code outside Chrome with two clicks at a specfic spot in a web page.


Steps to reproduce:
1. Download ext.zip, create a directory and unzip it to the directory.
2. Visit chrome://extensions, enable developer mode and load the unpacked extension.
3. Wait a little bit, observe that chrome://downloads is opened.

Now the following happens (see video):
- The PoC performs XSS in chrome://downloads
- The PoC bypasses the dangerous file check (Chrome 55+, thanks to https://crbug.com/chromium/640673)
- The PoC launches an external program via the downloaded vbs script.



This exploit works because of multiple vulnerabilities:

### XSS in chrome://downloads
- innerHTML assignment at [1] using a variable from [2], created at [3]:
      var name = this.data.by_ext_name;
      return loadTimeData.getStringF('controlledByUrl', url, name);
  In the above code (from [3]), name is the extension name, which can have any value.

- So I can perform XSS in chrome://downloads by setting the extension name.

Proposed fix: Escape the name variable.


### CSP bypasses
I use https://crbug.com/chromium/668645 to bypass the following Content-Security-Policy of chrome://downloads:
script-src chrome://resources 'self' 'unsafe-eval';object-src 'none';child-src 'none';



### Bypass safe browsing / dangerous file check
- https://crbug.com/chromium/640673 removed the confirmation dialogs to simplify the download flow at chrome://downloads,
  assuming that when the user wants to download the file when they click in the page.
- However, the C++-side does not perform further validations on this condition.

Proposed fix: Require a user gesture in MdDownloadsDOMHandler::HandleSaveDangerous.


### Run a program outside of Chrome
- To run a program, a user should click on a button in chrome://downloads.
- Again, there is no C++-side check that the user did really click.

Proposed fix: Require a user gesture in MdDownloadsDOMHandler::HandleOpenFile.
(and maybe as a defense in depth, also in MdDownloadsDOMHandler::HandleOpenDownloadsFolder)


[1] https://chromium.googlesource.com/chromium/src/+/4a6882854516c760d962aea5924f52fd3c68184c/chrome/browser/resources/md_downloads/item.js#244
[2] https://chromium.googlesource.com/chromium/src/+/4a6882854516c760d962aea5924f52fd3c68184c/chrome/browser/resources/md_downloads/item.js#21
[3] https://chromium.googlesource.com/chromium/src/+/4a6882854516c760d962aea5924f52fd3c68184c/chrome/browser/resources/md_downloads/item.js#113

## Attachments

- [ext.zip](attachments/ext.zip) (application/octet-stream, 2.0 KB)
- [start-mspaint.ogv](attachments/start-mspaint.ogv) (video/ogg, 380.0 KB)

## Timeline

### ro...@robwu.nl (2016-11-25)

[cc dbeam@ for review]

Patch to fix XSS: https://codereview.chromium.org/2526323004

### ro...@robwu.nl (2016-11-25)

[+jochen for review too]
Patch to enforce user gesture: https://codereview.chromium.org/2535483003/

Before landing the patches, vulcanize should be run - https://cs.chromium.org/chromium/src/docs/vulcanize.md (Otherwise the changes won't make it into Chrome).
Locally I verified that either patch (after running vulcanize & compiling) breaks the exploit chain.

### bu...@chromium.org (2016-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f49156a6624e78d73636eb0f4113f541e599cefb

commit f49156a6624e78d73636eb0f4113f541e599cefb
Author: rob <rob@robwu.nl>
Date: Tue Nov 29 00:08:01 2016

Require user gesture for powerful download operations

BUG=668653
TEST=Manually clicking on the open download folder works,
running the test case from the bug report triggers NOTREACHED.
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2535483003
Cr-Commit-Position: refs/heads/master@{#434786}

[modify] https://crrev.com/f49156a6624e78d73636eb0f4113f541e599cefb/chrome/browser/resources/md_downloads/action_service.js
[modify] https://crrev.com/f49156a6624e78d73636eb0f4113f541e599cefb/chrome/browser/resources/md_downloads/crisper.js
[modify] https://crrev.com/f49156a6624e78d73636eb0f4113f541e599cefb/chrome/browser/ui/webui/md_downloads/md_downloads_dom_handler.cc
[modify] https://crrev.com/f49156a6624e78d73636eb0f4113f541e599cefb/content/renderer/web_ui_extension.cc


### ji...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### ji...@chromium.org (2016-11-29)

Adding a couple of labels. Thanks for contributing patches to this issue.

### bu...@chromium.org (2016-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6d9a7916b48581f72fda060a1210ebef7f89b229

commit 6d9a7916b48581f72fda060a1210ebef7f89b229
Author: rob <rob@robwu.nl>
Date: Tue Nov 29 23:21:10 2016

Remove XSS from chrome://downloads

BUG=668653
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2526323004
Cr-Commit-Position: refs/heads/master@{#435104}

[modify] https://crrev.com/6d9a7916b48581f72fda060a1210ebef7f89b229/chrome/browser/resources/md_downloads/compiled_resources2.gyp
[modify] https://crrev.com/6d9a7916b48581f72fda060a1210ebef7f89b229/chrome/browser/resources/md_downloads/crisper.js
[modify] https://crrev.com/6d9a7916b48581f72fda060a1210ebef7f89b229/chrome/browser/resources/md_downloads/item.js


### ro...@robwu.nl (2016-11-30)

[+jialiul to re-assess the severity]

This allows a full sandbox bypass, requiring nothing more than having a malicious extension installed. The video did no effort at hiding how the exploit operates, but in reality the exploit can be executed without the user noticing. Exploiting this bug is easy: buy an extension with many users, publish an update that uses this bug and profit.

Escaping the sandbox from a web page is rated as critical severity (https://www.chromium.org/developers/severity-guidelines). I think that the extension requirement is not enough mitigation to drop the severity by two levels in the class, so this should be rated Security_Severity-High.


Can I merge 6d9a7916b48581f72fda060a1210ebef7f89b229 with the first release of M-55?
The patch is dead simple and cannot have undesired side effects. I verified the fix in 57.0.2937.0 on Windows (using the steps to repro from the bug). (The other patch fixes another part of the exploit chain, but if there are no other XSS issues in chrome://downloads we should be fine.)

Adding Release blocker just to make sure that this merge request is evaluated before the M-55 release.

### sh...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-11-30)

awhalley@ for M55 merge review (FYI: We're cutting M55 Stable RC soon).

### aw...@chromium.org (2016-11-30)

Yea, we're out of time for M55, though we should keep to the standard flow for this and consider a merge if we do a stable update later on.

### di...@chromium.org (2016-11-30)

[Automated comment] Less than a week to go before stable on M55, we might already have a stable candidate build. Manual review required.

### di...@chromium.org (2016-11-30)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### di...@chromium.org (2016-11-30)

[Automated comment] Less than a week to go before stable on M55, we might already have a stable candidate build. Manual review required.

### bu...@chromium.org (2016-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/deb94aef51054feb86021d2168182caf3d26886b

commit deb94aef51054feb86021d2168182caf3d26886b
Author: Rob Wu <rob@robwu.nl>
Date: Wed Nov 30 22:50:51 2016

Remove XSS from chrome://downloads

BUG=668653
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2526323004
Cr-Commit-Position: refs/heads/master@{#435104}
(cherry picked from commit 6d9a7916b48581f72fda060a1210ebef7f89b229)

Review URL: https://codereview.chromium.org/2537893004 .

Cr-Commit-Position: refs/branch-heads/2924@{#218}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/deb94aef51054feb86021d2168182caf3d26886b/chrome/browser/resources/md_downloads/compiled_resources2.gyp
[modify] https://crrev.com/deb94aef51054feb86021d2168182caf3d26886b/chrome/browser/resources/md_downloads/crisper.js
[modify] https://crrev.com/deb94aef51054feb86021d2168182caf3d26886b/chrome/browser/resources/md_downloads/item.js


### aw...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-12-04)

How about the severity re-assessment as requested in https://crbug.com/chromium/668653#c7?

I found a way to easily install extensions from a web page (https://crbug.com/chromium/671007), so this effectively means that web pages can run arbitrary code outside the sandbox with minimal user interaction (e.g. double-click in a fixed location on a web page).

### ro...@robwu.nl (2016-12-04)

[Description Changed]

### aw...@chromium.org (2016-12-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-01-23)

We are not planning any further M55 stable releases.

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

We'll consider this for reward in conjunction with 668645.

### sh...@chromium.org (2017-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lu...@gmail.com (2017-10-26)

is there anyway i can view https://crbug.com/chromium/671007? i'm doing research for a uni paper

### aw...@google.com (2017-10-26)

luca.ermancio@ - added.

### lu...@gmail.com (2017-11-07)

[Comment Deleted]

### ma...@seznam.cz (2018-04-18)

Could you please add me, so that I can view https://crbug.com/chromium/671007 for a university research? Same situation as luca.ermancio@.

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-29)

Hi Rob, the VRP panel decided to award $5,000 for this report, thanks!

### aw...@chromium.org (2018-06-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/668653?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086079)*
