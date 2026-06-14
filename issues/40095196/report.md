# Security: Code run by redirecting same-origin download to a javascript: URL gains user activation and bypasses CSP

| Field | Value |
|-------|-------|
| **Issue ID** | [40095196](https://issues.chromium.org/issues/40095196) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2019-05-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

When redirecting a same-origin download to a javascript: URL, the code that runs has user activation and bypasses CSP.

This issue was found as part of <https://bugs.chromium.org/p/chromium/issues/detail?id=966914>.

**VERSION**  

Chrome Version: Tested on 74.0.3729.169 (stable) and 76.0.3804.1 (canary)  

Operating System: Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. The attached files form a simple website. To begin with, download each of the files and place them in a directory.
2. In the directory you downloaded the files to, run the following command in a terminal:

python3 server.py 8080

This will start a simple web server that can be used to serve the files in the directory. server.py is necessary here, as it firstly redirects requests received for download.txt:

if self.path == '/download.txt':  

self.send\_response(302)  

self.send\_header('Location', "javascript: window.open()")  

self.end\_headers()

This is important in step 4 below, where a download for this file will be initiated.

Secondly, it sets the following Content-Security-Policy header:

Content-Security-Policy: script-src 'self';

3. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

4. This page has a single link:

<a href="download.txt" id="download-link" download></a>

10 seconds after the page loads, JavaScript will click the link. When this happens, server.py will redirect the request received for download to the following javascript: URL:

javascript: window.open()

The window.open call here should fail, given that the page has had no user interaction. Instead, it succeeds.

This demonstrates two things: (1) that the script has user activation (otherwise the window.open call would fail) and (2) that CSP is bypassed (as an inline javascript: URL is executed, even though a "script-src" of "self" is used).

From debugging through the code, a same-origin download redirected to a javascript: URL is ultimately passed through the following function:

<https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/frame/web_local_frame_impl.cc?l=2055&rcl=fe24d6713f507dd7e4ff407a1ef769e07abef734>

As can be seen, this function grants user activation and sets a flag indicating CSP should be ignored. So it appears that this is the direct cause of the issue.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [index.html](attachments/index.html) (text/plain, 211 B)
- [main.js](attachments/main.js) (text/plain, 202 B)
- [server.py](attachments/server.py) (text/plain, 725 B)

## Timeline

### in...@chromium.org (2019-05-28)

andypaicu@, can you please take a look. please feel free to downgrade severity if needed.

[Monorail components: Blink>SecurityFeature]

### sh...@chromium.org (2019-05-29)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-12)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-27)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2019-06-28)

[Empty comment from Monorail migration]

### mk...@chromium.org (2019-07-01)

I'm somewhat amazed that we allow redirects to `javascript:`. Firefox, AFAIK, doesn't. I'm pretty sure the relevant algorithm in HTML would forbid this behavior as well. So, let's try to kill it instead of figuring out what the correct behavior would be.

+alexmos@ and creis@ in case they know things about this weird corner of navigation that I don't.

### ah...@chromium.org (2019-07-01)

Redirect to javascript URLs should never be allowed as far as I can tell. Added clamy@ who may know where the actual check is?

### mk...@chromium.org (2019-07-02)

I played with this a little bit last night, and it looks like it only happens for `<a download>` (which also means that it can only happen same-origin, which is excellent). Dropping that attribute kills the bug. Which is weird!

+jochen@: Anything you could point to in the download flow that might cause this behavior?

### jo...@chromium.org (2019-07-02)

i guess at this point, there's a missing check whether we can redirect to the target URL at all: https://cs.chromium.org/chromium/src/content/browser/download/download_manager_impl.cc?rcl=5d8528a007e471f04e85b1fa727fda02b9a4dbfb&l=537

I guess there's somewhere a helper method that decides whether we can redirect?

### jo...@chromium.org (2019-07-02)

and here: https://cs.chromium.org/chromium/src/content/browser/download/download_resource_handler.cc?rcl=5d8528a007e471f04e85b1fa727fda02b9a4dbfb&l=133

Yay for duplicate code paths for everything

### mk...@chromium.org (2019-07-02)

I don't know when the latter is executed. But the former is certainly involved in this bug. I'll put up a dumb patch in a minute and hope that someone who knows this codebase can help me make it less dumb. :)

### jo...@chromium.org (2019-07-02)

i think it's network service vs non-network service

### ah...@chromium.org (2019-07-02)

clamy@ told me yesterday there was a debate at some point regarding where checks for invalid URL schemes should be done with the network service. It was chosen to go on the client, but concerns were that sort of issues. Will be able to provide more info once she is in the office. Also added jam@ who is knowledgeable on the issue.

### mk...@chromium.org (2019-07-02)

I put up https://chromium-review.googlesource.com/c/chromium/src/+/1685093, which seems to work locally.

### cl...@chromium.org (2019-07-02)

Yes the context here is that we used to have checks in the network stack that prevented redirects to some URL schemes. During the development of the network service, there was some debate about where those checks should happen in the network service world. John's position I believe was that the network service shouldn't know about these kind of schemes it doesn't handle, so the checks should be the client responsibility. Nasko and myself were worried that by pushing those checks on the clients, some clients would forget them and we would get security bugs. The final decision was to put the responsibility for the checks on the clients.

This particular bug should be easy enough to fix, however we do stand the risk to see more of those popping up in the future. I think we should revisit the idea of doing some form of checking in the network service. For example, we could pass a list of schemes we forbid network redirects to at the creation/initialization of the network service. Thus, the network service doesn't have baked in knowledge of schemes it doesn't know how to handle, and we don't have to make sure that every client of the network service remembers to check redirects to every possible scheme.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/81fe93a5eb431f0794eb778b3d9778689c3dfd20

commit 81fe93a5eb431f0794eb778b3d9778689c3dfd20
Author: Mike West <mkwst@chromium.org>
Date: Wed Jul 17 08:23:45 2019

Prevent redirection to `javascript:...` during downloads.

Bug: 967780
Change-Id: I2703998615fea0f0a99cb7963f8440842ba3d92a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1685093
Reviewed-by: Jochen Eisinger <jochen@chromium.org>
Commit-Queue: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#678183}

[modify] https://crrev.com/81fe93a5eb431f0794eb778b3d9778689c3dfd20/content/browser/download/download_manager_impl.cc
[modify] https://crrev.com/81fe93a5eb431f0794eb778b3d9778689c3dfd20/content/browser/download/download_resource_handler.cc
[add] https://crrev.com/81fe93a5eb431f0794eb778b3d9778689c3dfd20/third_party/blink/web_tests/external/wpt/html/semantics/text-level-semantics/the-a-element/a-download-click-redirect-to-javascript.html
[add] https://crrev.com/81fe93a5eb431f0794eb778b3d9778689c3dfd20/third_party/blink/web_tests/external/wpt/html/semantics/text-level-semantics/the-a-element/resources/a-download-redirect-to-javascript.html


### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-08-19)

Hi Mike. Welcome back.

Is the revision referenced in c#16 a full fix for this? What else needs to happen before this bug can be marked as fixed?

Thanks!
- a friendly security marshal

### mk...@chromium.org (2019-08-19)

Yes. That patch should do it. Thanks!

### sh...@chromium.org (2019-08-20)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-27)

Not requesting merge to beta (M77) because latest trunk commit (678183) appears to be prior to beta branch point (681094). If this is incorrect, please replace the Merge-na label with Merge-Request-77. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-09-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-09-05)

Congrats! The Panel decided to reward $1,000 for this report

### na...@google.com (2019-09-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/967780?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095196)*
