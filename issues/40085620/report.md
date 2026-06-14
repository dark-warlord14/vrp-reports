# Security: Bypass of same-origin policy via range requests in PDF plugin

| Field | Value |
|-------|-------|
| **Issue ID** | [40085620](https://issues.chromium.org/issues/40085620) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | th...@chromium.org |
| **Created** | 2016-10-07 |
| **Bounty** | $7,500.00 |

## Description

Chrome version: stable (53.0.2785.116) and latest (55.0.2882.0)

The built-in PDF plugin has a scripting interface that allows same-origin pages to read the content of the PDF file.
This "same-origin" check is based on the requested URL, after following all redirects, if any. This works fine, usually. Except the checks can be bypassed by forcing range requests and redirecting in a partial response.

Steps to reproduce:

1. Download the attached files.
2. Start the Python server.
3. Visit http://localhost:8080/
4. Input the URL of a PDF file (or use the existing example, the Bitcoin paper).
5. Click on the "Show content" button.
6. The contents of the (cross-origin) PDF is output.

NOTE: The above PoC is for PDF files, but the vulnerability can be abused to read any kind of data from other servers, by constructing the response in the following way: [PDF header] [padding] [cross-origin data via redirects] [padding] [PDF trailer].

## Attachments

- [index.html](attachments/index.html) (text/plain, 1.1 KB)
- [server.py](attachments/server.py) (text/plain, 2.1 KB)
- [poc-read-any.py](attachments/poc-read-any.py) (text/plain, 4.8 KB)

## Timeline

### ro...@robwu.nl (2016-10-07)

[Empty comment from Monorail migration]

### ts...@chromium.org (2016-10-07)

Lei, care to take a look at this? Thanks.

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2016-10-08)

Raymes, do you want to take this one since you fixed https://crbug.com/chromium/520422?

### th...@chromium.org (2016-10-09)

https://codereview.chromium.org/2407683002 - apparently I spend my weekends doing plumbing. ;)

### ra...@chromium.org (2016-10-09)

Thanks for picking it up!

### ro...@robwu.nl (2016-10-19)

Here is a PoC to read any kind of data from other servers.
To use:

1. python poc-read-any.py
   (this starts a local server at port 8081 and 8082)
2. Visit http://localhost:8081
   The demo page will display non-PDF content from localhost:8082.

If you want to test with a real server, edit poc-read-any.py and change line 14 to
victim_url = 'https://example.com'

### sh...@chromium.org (2016-10-23)

thestig: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/65c30fee167a96761f0bb9929dc44996d9e546fe

commit 65c30fee167a96761f0bb9929dc44996d9e546fe
Author: thestig <thestig@chromium.org>
Date: Tue Oct 25 20:18:31 2016

PDF: Don't follow redirects in the plugin.

The MimeHandler should have done it already.

BUG=653749

Review-Url: https://codereview.chromium.org/2409423004
Cr-Commit-Position: refs/heads/master@{#427452}

[modify] https://crrev.com/65c30fee167a96761f0bb9929dc44996d9e546fe/pdf/document_loader.cc


### th...@chromium.org (2016-10-26)

I can confirm the fix in a local build, but the fixed missed the 56.0.2901.0 canary by a small margin. I'll start with a M55 merge now, and we can consider the M54 merge later.

### di...@chromium.org (2016-10-26)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### di...@chromium.org (2016-10-26)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### th...@chromium.org (2016-10-26)

Merge landed: https://chromium.googlesource.com/chromium/src/+/f205daa53b8a4b4cd11d9a67c25847312e2e69df

+tsepez to help determine whether we should merge to M54. We may want to wait a little longer and make sure the CL does not cause any other breakages in normal use.

### ts...@chromium.org (2016-10-26)

I think we'd want this, but it does require baking first.

### ra...@chromium.org (2016-10-27)

I feel like this is on par with https://crbug.com/chromium/654280. Should we change to medium severity?

### ro...@robwu.nl (2016-10-27)

This bug allows cross-origin read access to any file type, not just PDFs (see https://crbug.com/chromium/653749#c6 for PoC). As such I think that a slightly higher severity and corresponding merging bar wouldn't be too bad.

### sh...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f205daa53b8a4b4cd11d9a67c25847312e2e69df

commit f205daa53b8a4b4cd11d9a67c25847312e2e69df
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Oct 26 21:23:27 2016

M55: PDF: Don't follow redirects in the plugin.

The MimeHandler should have done it already.

BUG=653749

Review-Url: https://codereview.chromium.org/2409423004
Cr-Commit-Position: refs/heads/master@{#427452}
(cherry picked from commit 65c30fee167a96761f0bb9929dc44996d9e546fe)

Review URL: https://codereview.chromium.org/2457543002 .

Cr-Commit-Position: refs/branch-heads/2883@{#313}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/f205daa53b8a4b4cd11d9a67c25847312e2e69df/pdf/document_loader.cc


### ro...@robwu.nl (2016-11-01)

This is not yet merged with M-54, bugdroid's comment above is wrong (https://groups.google.com/a/chromium.org/d/msg/chromium-dev/sJ7gZLqyJ-g/k-CbRUrnBwAJ).

How much baking do we need?

### th...@chromium.org (2016-11-01)

tsepez: Do we want to try a M54 merge? Not that it's a guarantee nothing will break, but we haven't heard of any breakages.

### ts...@chromium.org (2016-11-01)

Let's try it.

### th...@chromium.org (2016-11-01)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-11-01)

[Automated comment] Request affecting a post-stable build (M54), manual review required.

### aw...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-14)

Nice one! The panel decided to reward $7,500 for this bug.  Cheers!

### bu...@chromium.org (2016-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a8563ff4076d3ee37db3aaa85cf5226a8922e30f

commit a8563ff4076d3ee37db3aaa85cf5226a8922e30f
Author: raymes <raymes@chromium.org>
Date: Tue Nov 15 23:50:01 2016

Add test to ensure that URLs that redirect inside the PDF plugin fail to load

A URL that is passed to the PDF plugin should already have its redirects
resolved. If it doesn't, then the PDF that gets loaded may not have the same
origin as the one the PDF is assumed to be in. If that happens, it can cause
same origin policy violations. So redirects are disabled for requests made from
the plugin.

Redirects were disabled here: https://codereview.chromium.org/2409423004/.
There is one other place where we make a request in the plugin which has
disabled in this CL (the URLs that get loaded here are chrome internal
URLs so they should never trigger redirects anyway but this is done for
safety). This CL also adds some plumbing to ensure the redirect requests
trigger a document load failure message to be sent to JS so that we can
properly detect the load failure in tests.

BUG=653749

Review-Url: https://codereview.chromium.org/2455663004
Cr-Commit-Position: refs/heads/master@{#432293}

[modify] https://crrev.com/a8563ff4076d3ee37db3aaa85cf5226a8922e30f/chrome/browser/pdf/pdf_extension_test.cc
[add] https://crrev.com/a8563ff4076d3ee37db3aaa85cf5226a8922e30f/chrome/test/data/pdf/redirects_fail_test.js
[modify] https://crrev.com/a8563ff4076d3ee37db3aaa85cf5226a8922e30f/pdf/document_loader.cc
[modify] https://crrev.com/a8563ff4076d3ee37db3aaa85cf5226a8922e30f/pdf/out_of_process_instance.cc
[modify] https://crrev.com/a8563ff4076d3ee37db3aaa85cf5226a8922e30f/pdf/pdfium/pdfium_engine.cc


### aw...@google.com (2016-11-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-03-25)

This issue was migrated from crbug.com/chromium/653749?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085620)*
