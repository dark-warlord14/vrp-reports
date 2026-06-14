# getThumbnail() CHECK leaks number of available PDF pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40059101](https://issues.chromium.org/issues/40059101) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | dh...@chromium.org |
| **Created** | 2022-03-15 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36

Steps to reproduce the problem:
let w = open('https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf');
setTimeout(_ => w[0].postMessage({type: 'getThumbnail', page: '1337'}, "*"), 1000);

What is the expected behavior?
Not crash pdf viewer maybe page should be the maximum in this case.

What went wrong?
Crashed the PDF viewer this maybe detected via print and that would leak how many pages a pdf has.

Crashed report ID: 

How much crashed? Just one tab

Is it a problem with a plugin? N/A 

Did this work before? N/A 

Chrome version: 99.0.4844.51  Channel: stable
OS Version: 10.0

Also did https://bugs.chromium.org/p/chromium/issues/detail?id=1305740 that may allow detecting what pdf loaded.

## Timeline

### dt...@chromium.org (2022-03-15)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### km...@chromium.org (2022-03-15)

Looks like this is related to the fix for https://crbug.com/chromium/1283198, although a CHECK is better than an OOB access.

Not clear to me that it's possible to detect whether the frame crashed or not, but I question why we need this API at all (https://crbug.com/chromium/1279958).

### km...@chromium.org (2022-03-15)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-03-15)

[Empty comment from Monorail migration]

### km...@chromium.org (2022-03-15)

Not sure what the right set of labels is here, but given that this is a different manifestation of the same underlying issue as https://crbug.com/chromium/1283198, probably should consider this bug to go back to the same milestones.

### [Deleted User] (2022-03-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-15)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2022-03-15)

Ah I should have noticed this would be considered a security bug :/

Regarding PDF detection  I said it because it seems stuff like print are detectable with device performance monitoring https://devicemonitor.glitch.me/ (probably wont work for other people without changes)
That said theirs probably easier ways of doing it like https://xsleaks.dev/docs/attacks/timing-attacks/execution-timing/#busy-event-loop but then it needs to not have XFO.

### nd...@protonmail.com (2022-03-15)

Nevermind it does not need XFO im changing that to in case it has coop.

### nd...@protonmail.com (2022-03-15)

It seems it is possible to detect print with iframes as if an iframe has done print() doing print() on the parent wont block code execution.

### nd...@protonmail.com (2022-03-16)

If the API is not used then I agree it should be removed it allows leaking if a window reference is a pdf and if theirs a password.
print can be abused to detect crashes
selectAll maybe iframe attack to abuse copy and paste
getSelectedText/getThumbnail if theirs a message listener that forwards messages then it leaks text from pdfs. 

I made PoC for print() detection from iframes... the "Device monitor" does work but needs changing to detect print no idea why it works.

### km...@chromium.org (2022-03-16)

Thinking maybe this should have gone to the Untriaged state first, rather than straight to Available; correcting now.

### [Deleted User] (2022-03-16)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2022-03-17)

While I would normally have a way to detect print() from iframes like did on https://ndev.tk/print.html without needing to use device performance leaks (annoying due to cpu usage),
It seems PDFs are different this allow for https://bugs.chromium.org/p/chromium/issues/detail?id=1307087 so hopefully the leak is not created by fixing it.
Also embed tags that have a pdf block the top print() for seemingly no reason.

### nd...@protonmail.com (2022-03-17)

I can confirm https://crbug.com/chromium/1307087 makes this exploitable via the opener.

### ad...@google.com (2022-03-17)

kmoon@ thanks for adding this to the security queue in https://crbug.com/chromium/1306443#c5.

Regarding whether this is security-relevant,
* if the crash is truly a CHECK failure (as opposed to DCHECK) then it's _probably_ not security-relevant in the same sense as the buffer overflow in https://crbug.com/chromium/1283198. That CHECK will occur in release builds, giving us a nice safe crash instead of an exploitable buffer overflow.
* However, because other tabs can detect the crash, this does indeed seem like a good way to leak the number of pages in the PDF. That is security-relevant.

Severity:
https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-medium-severity is used for "A bug that allows an attacker to reliably read or infer browsing history". I don't think this leak is equivalently powerful, so I'm going to rate this Low severity.

Security bugs need to be assigned so I'm setting you as the assignee kmoon@.

### km...@chromium.org (2022-03-17)

This probably would be a better one for dhoss@ to tackle; they should be back on Monday. That said, I doubt they'll be ramped up to work on it on their first day back. :-)

### th...@chromium.org (2022-03-21)

Fixing https://crbug.com/chromium/1279958 may be the better long term solution. In the meanwhile, instead of crashing due to CHECK() failure, how about just silently ignoring bad messages?

### km...@chromium.org (2022-03-21)

I think that's a good suggestion, but there's a significant amount of work on the non-error path (to generate the thumbnail), so I think this would still leak information via a timing attack.

### km...@chromium.org (2022-03-21)

If we want to leave the scripting API in place, perhaps a good starting point is to restrict which origins can use it. There's no need to allow these calls to the Web in general.

### th...@chromium.org (2022-03-21)

SGTM

### km...@chromium.org (2022-03-21)

dhoss@ is back this week, and agreed to look into it, so reassigning accordingly.

### nd...@protonmail.com (2022-03-22)

I think the print message has a use for website's but this API should be same-origin and stuff like getThumbnail seem to have no use for websites.
Especially not via the opener.

### dh...@chromium.org (2022-03-22)

Yeah, I agree. This hook for thumbnails shouldn't exist, and it was only added for testing purposes. I refactored some code last year that will allow me to test thumbnails differently, so I'll just do that.

This would also allow us to remove the getThumbnail() method from PDFScriptingAPI.

### ad...@google.com (2022-03-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7fcb5f05cd1a1c6de9116419e4dd66ec2bb9447b

commit 7fcb5f05cd1a1c6de9116419e4dd66ec2bb9447b
Author: Daniel Hosseinian <dhoss@chromium.org>
Date: Wed Mar 23 00:58:35 2022

[pdf-viewer] Test thumbnail requests directly with PluginController

Add a new browser test, PDFExtensionJSTest.PluginController, for plugin
controller interactions.

Move `testRequestThumbnail()` to the new test, and call
`PluginController.requestThumbnail()` directly instead of calling it
through `PDFScriptingAPI`. This was made possible as of
crrev.com/820941.

This change allows for the removal of thumbnail methods in
`PDFScriptingAPI` and thumbnail handling code in
`PDFViewerElement.handleScriptingMessage()`. Consequently, thumbnails
will no longer be accessible by a PDF Viewer embedder.

Bug: 1306443
Change-Id: I480b0a501d82c4ffa4d3344a7cb9ec6f6f6d764b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3543173
Commit-Queue: Daniel Hosseinian <dhoss@chromium.org>
Auto-Submit: Daniel Hosseinian <dhoss@chromium.org>
Reviewed-by: K. Moon <kmoon@chromium.org>
Commit-Queue: K. Moon <kmoon@chromium.org>
Cr-Commit-Position: refs/heads/main@{#984124}

[modify] https://crrev.com/7fcb5f05cd1a1c6de9116419e4dd66ec2bb9447b/chrome/browser/resources/pdf/pdf_viewer.ts
[modify] https://crrev.com/7fcb5f05cd1a1c6de9116419e4dd66ec2bb9447b/chrome/browser/resources/pdf/pdf_scripting_api.ts
[modify] https://crrev.com/7fcb5f05cd1a1c6de9116419e4dd66ec2bb9447b/chrome/test/data/pdf/BUILD.gn
[modify] https://crrev.com/7fcb5f05cd1a1c6de9116419e4dd66ec2bb9447b/chrome/browser/pdf/pdf_extension_test.cc
[modify] https://crrev.com/7fcb5f05cd1a1c6de9116419e4dd66ec2bb9447b/chrome/test/data/pdf/basic_plugin_test.ts
[add] https://crrev.com/7fcb5f05cd1a1c6de9116419e4dd66ec2bb9447b/chrome/test/data/pdf/plugin_controller_test.ts


### dh...@chromium.org (2022-03-23)

Seems like I don't need to manually request a merge for this, and Sheriffbot will decide automatically [1]

[1] https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/merge_request.md#Security-merge-triage

### [Deleted User] (2022-03-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### nd...@protonmail.com (2022-04-22)

Thanks :)

### am...@chromium.org (2022-04-22)

YW! Congrats on another one! 

### am...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1306443?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1279958]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059101)*
