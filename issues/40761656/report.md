# Loading remotely hosted JavaScript files in V3

| Field | Value |
|-------|-------|
| **Issue ID** | [40761656](https://issues.chromium.org/issues/40761656) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | rd...@chromium.org |
| **Created** | 2021-04-19 |
| **Bounty** | $1,000.00 |

## Description


As per the migration guide (https://developer.chrome.com/docs/extensions/mv3/intro/mv3-overview/#remotely-hosted-code) of the chrome extension V3, the extension can't allow loading of remotely hosted code like JavaScript or Wasm files, and the script-src directive of Content security policy (CSP) does not allow external host URLs.

However, if we add the script-src-elem directive of Content security policy (CSP) it allows loading externally hosted JavaScript files.

Is this expected behavior? and does the script-src-elem directive adds any vulnerability?

PS: I have attached POC which loads remotely hosted JavaScript files without any issue when the script-src-elem directive present in the manifest file.


## Attachments

- [V3-loads-remote-hosted-code.zip](attachments/V3-loads-remote-hosted-code.zip) (application/octet-stream, 1.9 KB)

## Timeline

### dt...@chromium.org (2021-04-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy Platform>Extensions]

### [Deleted User] (2021-04-19)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-04-19)

Devlin, could you or someone on your team see if this is WAI? Thanks!

### [Deleted User] (2021-04-21)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rd...@chromium.org (2021-04-26)

Thanks for the report!

To clarify here, remotely-hosted code is disallowed in MV3 _by policy_ - this is not (and cannot be) guaranteed at the platform level (for many reasons).  Instead, we provide some basic limitations, predominantly to serve as "guardrails" for developers - these are intended to make it a little bit harder to execute remote code and largely reduce developers from unintentionally violating the policy (again, they are not meant to be 100% preventative).  I'm working on writing up a doc that explains this more thoroughly, which will hopefully be out in the coming weeks.  In that respect, this is *not* a security bug - executing remote code in extensions should *not* be considered a vulnerability.  Security folks, I'm comfortable removing the security-related labels here if there are no objections.

That said, we should have the platform limitations be "as good as they can be".  Because of this, though I wouldn't consider this a security issue, I would consider it a bug (or perhaps, feature enhancement) for the platform, and we should address it.

Karan, do you mind taking a look?

### ka...@chromium.org (2021-04-27)

Yeah this is something that I brought up in internal discussions a while back and was planning to fix soon. We don't currently account for style-src-attr and style-src-elem directives. 

I agree this is not a security bug. 

Also, for now please don't use these directives to get around the platform mitigations since you'd still be in violation of our remotely hosted code policy. 

### gi...@appspot.gserviceaccount.com (2021-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3

commit a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3
Author: Karandeep Bhatia <karandeepb@chromium.org>
Date: Thu Jun 03 19:50:41 2021

Extensions: Ensure default CSP is always applied for MV3 extensions.

Ensure the default CSP of "script-src 'self'; object-src 'self';" is
always applied in Blink for contexts corresponding to MV3 extensions.
This prevents extensions from relaxing their own CSP (say by using
Service Workers) and getting around remotely hosted code mitigations.
Since we always append the default CSP, this also fixes issues like
1200198 which are caused by the extension CSP parsing code not being
robust enough.

Bug:899726, 1200198

Change-Id: I1e3a60b22fdbd7ad130041813dff302096bda550
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2909458
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Antonio Sartori <antoniosartori@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#888978}

[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/chrome/browser/extensions/service_worker_apitest.cc
[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/chrome/renderer/chrome_content_renderer_client.cc
[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/chrome/renderer/chrome_content_renderer_client.h
[add] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/chrome/test/data/extensions/api_test/service_worker/worker_based_background/extension_csp_modification/extension_page.html
[add] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/chrome/test/data/extensions/api_test/service_worker/worker_based_background/extension_csp_modification/manifest.json
[add] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/chrome/test/data/extensions/api_test/service_worker/worker_based_background/extension_csp_modification/service_worker.js
[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/content/public/renderer/content_renderer_client.cc
[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/content/public/renderer/content_renderer_client.h
[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/content/renderer/renderer_blink_platform_impl.cc
[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/content/renderer/renderer_blink_platform_impl.h
[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/extensions/common/manifest_handlers/csp_info.cc
[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/extensions/common/manifest_handlers/csp_info.h
[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/third_party/blink/public/platform/platform.h
[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/third_party/blink/public/platform/web_vector.h
[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/a0a78c35bee7d01e1f9589f1fe5ab7d3ad18c2c3/third_party/blink/renderer/core/workers/worker_or_worklet_global_scope.cc


### gi...@appspot.gserviceaccount.com (2021-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a8409714e721ba63930ec12ae30cd5efa83fcedf

commit a8409714e721ba63930ec12ae30cd5efa83fcedf
Author: Karandeep Bhatia <karandeepb@chromium.org>
Date: Thu Jun 10 00:25:17 2021

Blink: Ensure embedder CSP is added to the policy container.

This is a follow-up to r888978. This ensures that if a document embeds a
local scheme subframe (for example a srcdoc iframe), the embedder
specified CSPs are correctly inherited to it.

Bug: 899726, 1200198
Change-Id: I235e08843183e226331c0b7854af520c06c7844b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2946278
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Antonio Sartori <antoniosartori@chromium.org>
Cr-Commit-Position: refs/heads/master@{#891036}

[modify] https://crrev.com/a8409714e721ba63930ec12ae30cd5efa83fcedf/chrome/browser/extensions/service_worker_apitest.cc
[modify] https://crrev.com/a8409714e721ba63930ec12ae30cd5efa83fcedf/chrome/test/data/extensions/api_test/service_worker/worker_based_background/extension_csp_modification/extension_page.html
[modify] https://crrev.com/a8409714e721ba63930ec12ae30cd5efa83fcedf/third_party/blink/renderer/core/loader/document_loader.cc


### ka...@chromium.org (2021-10-11)

This should be mostly fixed by the change in c#7. However the extension's CSP parser doesn't currently handle script-src-elem and script-src-attr for Mv3 extensions. We should fix that.

### ah...@chromium.org (2021-10-19)

[Security Bug Triage Rotation] Assigning to rdevlin@ for redispatch.


### ad...@chromium.org (2022-12-01)

[Empty comment from Monorail migration]

### rd...@chromium.org (2023-01-11)

> However the extension's CSP parser doesn't currently handle script-src-elem and script-src-attr for Mv3 extensions. We should fix that.

This doesn't really matter (from a security standpoint), since the minimum CSP (which is always applied) still has to be satisfied.  So even if the MV3 extension specifies an insecure value in e.g. script-src-elem, the minimum CSP will block it.  It'd be nice to fix that (from a consistency and developer clarity standpoint), but it's unrelated to this issue.

Closing this one out.

### [Deleted User] (2023-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-27)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us. 
It's important to note, at the time we are issuing this VRP reward, this user account has been deleted from monorail. We will defer on any processing of this reward in the case that the user returns to the system. If this message goes without a response for six months, this reward will be donated to a charitable organization. 

### am...@chromium.org (2023-01-28)

adding reward-decline for now as deleted-user account is breaking automation 

### [Deleted User] (2023-01-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-31)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-31)

 issue was originally reported by Avinash Madbhave and other team members from Excellarate (earlier Synerzip); Avinash is no longer part of the organization so reward will be extended to researchers on Synnerzip/Excellarate team 


### am...@chromium.org (2023-01-31)

Hello Atul and Nagmani of Synerzip; the labels have been updated so that this issue can get included in the week's automation and over the the finance team for processing later this week. Once that occurs, a member of the finance team will be in touch regarding payment processing. Please let me know if you have any questions. 

### am...@google.com (2023-02-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-04-20)

This issue was migrated from crbug.com/chromium/1200198?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>ContentSecurityPolicy, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40761656)*
