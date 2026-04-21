# Mixed content can be bypassed by sandboxed pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40094749](https://issues.chromium.org/issues/40094749) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2019-04-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Typically, a https site can't use or access resources from a http site. The browser will block attempts by a https site to include a http iframe, for example.

A sandboxed iframe (specifically one that doesn't have the "allow-same-origin" flag set), however, can create a popup window that can include http content, even if the source of the window is a https site. The browser won't block the mixed content, nor will it display any warning that it's being included.

**VERSION**  

Chrome Version: Tested on 74.0.3729.108 (stable) and 76.0.3777.0 (canary)  

Operating System: Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. The attached files form a simple website. To begin with, download each of the files and place them in a directory.
2. In the directory you downloaded the files to, run the following command in a terminal:

python3 -m http.server 8080

This will start a simple web server that can be used to serve the files in the directory.  

3. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

4. This page is fairly simple; it simply includes a sandboxed iframe with the following attributes set:

<iframe src="iframe.html" sandbox="allow-scripts allow-popups"></iframe>

5. iframe.html contains a single link to the following location:

<https://derceg.gitlab.io/http_iframe/>

Once you click the link, the page will open in a new tab. The page itself includes a http iframe:

<iframe src="http://neverssl.com/"></iframe>

That iframe should be blocked, given that the site is loaded over https. Instead, the iframe loads successfully. The browser also doesn't display any indication that there's mixed content on the page.

If you want to reproduce this issue without having to refer to an external site, it's trivial to do. Simply open a https popup from a sandboxed iframe, as done above, then attempt to either include a http iframe or fetch a http resource and check whether or not the request succeeds.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [iframe.html](attachments/iframe.html) (text/plain, 158 B)
- [index.html](attachments/index.html) (text/plain, 152 B)
- [wpt.patch](attachments/wpt.patch) (text/plain, 1.0 KB)

## Timeline

### mm...@chromium.org (2019-04-26)

Thanks for your report. I'm not super familiar with the expected mixed content behavior, so handing this over to Carlos and Chris who can properly evaluate this.

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### mm...@chromium.org (2019-04-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### ca...@chromium.org (2019-04-26)

Thanks for the report, I can reproduce this in current Stable. It seems mixed content checker is not getting called for some reason in this case, I'll investigate further.

### sh...@chromium.org (2019-04-27)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### de...@gmail.com (2019-05-01)

You actually don't need to open a popup to achieve this. if you apply a sandbox to the top-level document, then you can include mixed content. Applying a sandbox to the top-level document can be done by setting an appropriate Content-Security-Policy header:

Content-Security-Policy: sandbox allow-scripts

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### ti...@chromium.org (2022-09-07)

[Empty comment from Monorail migration]

### ti...@chromium.org (2022-09-07)

Cc-ing reporter of duplicate crbug.com/1350608 on here.

### ti...@chromium.org (2022-09-07)

[Empty comment from Monorail migration]

### ti...@chromium.org (2022-09-07)

[Empty comment from Monorail migration]

### ti...@chromium.org (2022-09-07)

As noted in https://crbug.com/chromium/956979#c6, a top-level page can set the `Content-Security-Policy: sandbox allow-scripts;` header in order to bypass mixed content.

I have drafted a web platform test to reproduce this, but I'm not sure I can upload it to Gerrit (much less land it and have it merged upstream) due to the security visibility restriction on this bug. Carlos, this has been sitting around for a couple years now, can we open up this bug and can I land the WPT?

### ca...@chromium.org (2022-09-07)

I'm actually working on this currently (our team is doing a fixit and I re-picked it up as part of that). I think I can have a fix in a day or two. Would it be ok to wait until the fix lands to land the new (hopefully passing at that point) WPT?

### ca...@chromium.org (2022-09-07)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-09-07)

CL is out for review at crrev.com/c/3881204

### ti...@chromium.org (2022-09-08)

Of course! I can wait for sure. Thanks for the quick reply!

### gi...@appspot.gserviceaccount.com (2022-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/82a599bbfadf4289137db0fb78d1e696beea56cc

commit 82a599bbfadf4289137db0fb78d1e696beea56cc
Author: Carlos IL <carlosil@chromium.org>
Date: Wed Sep 14 18:35:54 2022

Use GetTupleOrPrecursorTupleIfOpaque instead of origin when making mixed content decisions about frames

Previously we used the origin, but it is not set for sandboxed frames,
this CL changes the logic so GetTupleOrPrecursorTupleIfOpaque is now used.

Test: A Web Platform Test covering this case is ready, and will be added
once this lands (see bug).

Bug: 956979
Change-Id: Iba125573e81360d1d9b2023065e27d3c5b27cf60
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3881204
Commit-Queue: Carlos IL <carlosil@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1047024}

[modify] https://crrev.com/82a599bbfadf4289137db0fb78d1e696beea56cc/content/browser/renderer_host/mixed_content_navigation_throttle.cc


### ti...@chromium.org (2022-09-15)

I'm not sure this is fixed. See the attached patch for my test, which still fails. You can apply it with `$ git apply wpt.patch`, I've just learned. Otherwise, `$ patch -p1 < wpt.patch`.

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-10-06)

Sorry about the delay, I missed https://crbug.com/chromium/956979#c43. My manual test with the repro steps mentioned in the original report did fix the issue for that case. I'll take a look at the WPT.

### ti...@chromium.org (2022-10-07)

No worries, thanks for taking a look!

### ca...@chromium.org (2022-10-07)

Looks like the issue is that my previous CL only fixed the //content side, which is used for frames, but not the same issue on the blink side, which is used for subresource fetches, and what is being tested by the WPT. I sent a CL out with the blink-side fix at crrev.com/c/3938316

### gi...@appspot.gserviceaccount.com (2022-10-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5fddf8b11fad3fce40726d96f673f3a6388fb3a0

commit 5fddf8b11fad3fce40726d96f673f3a6388fb3a0
Author: Carlos IL <carlosil@chromium.org>
Date: Mon Oct 10 17:30:11 2022

Use GetOriginOrPrecursorOriginIfOpaque for mixed content checks

This is the same fix as crrev.com/c/3881204 but on the blink side.

Test: A WPT is ready (and how we noticed the fix was not complete), and
will be added once this lands (see bug).

Bug: 956979
Change-Id: Id41745106fd66aa20ccac3783109f38f7059d746
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3938316
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Carlos IL <carlosil@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1057015}

[modify] https://crrev.com/5fddf8b11fad3fce40726d96f673f3a6388fb3a0/third_party/blink/renderer/core/loader/mixed_content_checker.cc


### ca...@chromium.org (2022-10-10)

tiouan: In my testing, your WPT passes now with the CL in #48, so I think you can land it now.

### ti...@chromium.org (2022-10-11)

Ok thanks! I might add a test with a frame too, to exercise the case you first fixed. I'll send you the CL to review.

### gi...@appspot.gserviceaccount.com (2022-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4c9aa435eac318ff3beb11130e5f66b580f58c9a

commit 4c9aa435eac318ff3beb11130e5f66b580f58c9a
Author: Titouan Rigoudy <titouan@chromium.org>
Date: Tue Oct 11 20:07:40 2022

[Mixed Content] WPT tests for sandboxed documents.

Bug: chromium:956979
Change-Id: I884b1c561d49c859b44e46c99ac9d4a7c7d7b852
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3945033
Commit-Queue: Carlos IL <carlosil@chromium.org>
Auto-Submit: Titouan Rigoudy <titouan@chromium.org>
Reviewed-by: Carlos IL <carlosil@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1057632}

[add] https://crrev.com/4c9aa435eac318ff3beb11130e5f66b580f58c9a/third_party/blink/web_tests/external/wpt/mixed-content/csp.https.window.js.headers
[add] https://crrev.com/4c9aa435eac318ff3beb11130e5f66b580f58c9a/third_party/blink/web_tests/external/wpt/mixed-content/csp.https.window.js
[modify] https://crrev.com/4c9aa435eac318ff3beb11130e5f66b580f58c9a/third_party/blink/web_tests/external/wpt/common/dispatcher/dispatcher.js


### ca...@chromium.org (2022-11-02)

Marking this as fixed now

### [Deleted User] (2022-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-03)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations, David! The VRP Panel has decided to award you $1,000 for this report. It's not often we see six-digit bug numbers at the VRP Panel these days and we appreciate your abundance of patience while this issue was resolved. Thanks for your efforts and reporting this issue to us! 

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/956979?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature, Blink>SecurityFeature>IFrameSandbox]
[Monorail mergedwith: crbug.com/chromium/1350608]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094749)*
