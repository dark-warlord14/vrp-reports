# Security: CSP Sandbox bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40079621](https://issues.chromium.org/issues/40079621) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@caballero.com.ar |
| **Assignee** | an...@chromium.org |
| **Created** | 2014-05-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

We can bypass the header('Content-Security-Policy:sandbox') and access the DOM of sandboxed URLs.  

What we are doing is very simple: inject code into the page \*before\* it has been loaded, so Chrome will honor that code even when it should discard it. In other words, Chrome should behave exactly as if the sandboxed URL were coming from a different domain, deleting injected code. Once it reads the header, boom, destroy injected code so it doesn't run.

**VERSION**  

Chrome Version: 35.0.1916.114 (Official Build 270117) m stable  

Operating System: Windows 8.1 Pro Fully Updated

**REPRODUCTION CASE**  

Attached is the PoC, but here's the explanation because it's quite simple:

1. We open a new window which is header-sandboxed.  
   
   w = window.open("sandboxed.php","","width=400,height=400");
2. Before it loads, we inject an event and code:  
   
   w.onload = new w.Function("alert(document.body.innerText);document.body.innerHTML = '<h1>HACKED BY THE MAIN WINDOW</h1>'");

That's it! Chrome will not delete the event/function so it will run in the sandboxed window.

Thanks!

## Attachments

- [Bypass_CSP_Sandbox.zip](attachments/Bypass_CSP_Sandbox.zip) (application/zip, 1.1 KB)

## Timeline

### wf...@chromium.org (2014-05-27)

mkwst@ can you take a look at this issue, or pass onto someone else.  Thanks!

### cl...@chromium.org (2014-05-27)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-10-07)

Any update on this?

### me...@chromium.org (2014-11-11)

Joel, perhaps you could take a look?

### jw...@chromium.org (2014-11-14)

Unfortunately, I won't be able to take a look at this for a week. Mike, I'm assigning back to you if you can take it, otherwise I'll take a look when I get back.

### me...@chromium.org (2015-02-18)

Mike, have you had a chance to look at this?

### cl...@chromium.org (2015-10-28)

[Empty comment from Monorail migration]

### ts...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature]

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### mk...@chromium.org (2017-08-24)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-02-15)

This still reproduces in Chrome 66.0.3348.0.

Here's a repro: https://whytls.com/test/csp/stealSandbox.html

I'm going to raise the severity of this issue based on the fact that this is technically a same-origin policy violation, and neither Edge nor Firefox seems to be vulnerable (although that might just be because they don't support the syntax used).



### sh...@chromium.org (2018-02-16)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 175 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-02-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-16)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-02-19)

Andy, mind taking a look at this?

[Monorail components: -Blink>SecurityFeature Blink>SecurityFeature>IFrameSandbox]

### sh...@chromium.org (2018-03-03)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 1375 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-19)

[Empty comment from Monorail migration]

### dc...@chromium.org (2018-05-09)

I think this particular bug is caused by the fact that we're incorrectly reusing the Window object.

I tested something like this:
  var w = window.open('same-origin-page-that-is-sandboxed.py');
  w.testProperty = 'abc';

Once same-origin-page-that-is-sandboxed.py loads, you'll notice that testProperty is (incorrectly) set. This is in violation of the steps specified in initializing a new Document [1], which state that we only skip creating a new Window if the new Document is same-origin. Since the Document is sandboxed, by definition, it is cross-origin.

[1] https://html.spec.whatwg.org/multipage/browsing-the-web.html#initialise-the-document-object

### es...@chromium.org (2018-05-16)

Security sheriff update: Per offline discussion, patch is in progress at https://chromium-review.googlesource.com/c/chromium/src/+/983558

### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### pa...@chromium.org (2018-06-06)

Friendly ping to dcheng and mkwst to review the CL when they get back. :)

### bu...@chromium.org (2018-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/90f878780cce9c4b0475fcea14d91b8f510cce11

commit 90f878780cce9c4b0475fcea14d91b8f510cce11
Author: Andy Paicu <andypaicu@chromium.org>
Date: Fri Jun 15 15:51:49 2018

Prevent sandboxed documents from reusing the default window

Bug: 377995
Change-Id: Iff66c6d214dfd0cb7ea9c80f83afeedfff703541
Reviewed-on: https://chromium-review.googlesource.com/983558
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#567663}
[modify] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/sandbox/sandbox-allow-scripts.sub.html
[rename] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/sandbox/support/sandboxed-post-message-to-parent.html
[add] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/sandbox/support/sandboxed-post-property-to-opener.html
[rename] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/sandbox/support/sandboxed-post-property-to-opener.html.sub.headers
[add] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/sandbox/support/unsandboxed-post-property-to-opener.html
[add] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/sandbox/window-reuse-sandboxed.html
[add] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/sandbox/window-reuse-unsandboxed.html
[modify] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/blink/renderer/core/execution_context/security_context.h
[modify] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/blink/renderer/core/frame/csp/content_security_policy.h
[modify] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/blink/renderer/core/frame/local_frame.cc
[modify] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/blink/renderer/core/frame/local_frame.h
[modify] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/90f878780cce9c4b0475fcea14d91b8f510cce11/third_party/blink/renderer/core/loader/frame_loader.cc


### an...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-19)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-06-19)

Since this has been present since M66, my preference is to target M69. 

### aw...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-21)

Hi manuel@ - the Chrome VRP panel has (eventually :-) awarded $1,000 for this report! A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in release notes?

### aw...@google.com (2018-06-21)

[Empty comment from Monorail migration]

### ma...@caballero.com.ar (2018-06-21)

Thanks a lot!

Money   --> Wikimedia Foundation
Credits --> My real name

Thanks!

### aw...@chromium.org (2018-06-21)

Thanks for your generosity Manuel! I've donated $2,000 to the Wikimedia Foundation on your behalf.

### ma...@caballero.com.ar (2018-06-21)

My pleasure!

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/377995?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>ContentSecurityPolicy, Blink>SecurityFeature>IFrameSandbox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079621)*
