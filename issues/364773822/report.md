# Non-error pages can reuse the error page policy container

| Field | Value |
|-------|-------|
| **Issue ID** | [364773822](https://issues.chromium.org/issues/364773822) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>PolicyContainer, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2024-09-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

For purposes of history navigation, the same history entry is used regardless of whether a navigation fails or not. When a failed navigation is committed, an empty policy container is used and saved for that history entry [1](https://source.chromium.org/chromium/chromium/src/+/22d2f41ff31ed07ddb8eb431a24682b170a27bc4:content/browser/renderer_host/render_frame_host_impl.cc;l=11372-11373) [2](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_policy_container_builder.cc;l=56-68;drc=fa1e0cf5238e2600039f60af6909aefbd4cf003c;bpv=1;bpt=1). It's also possible to make a successful history navigation wrongfully use this empty policy container, since for locally-schemed URLs, the computed policies are taken directly from the history entry [3](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_policy_container_builder.cc;l=268-275). This can lead to a CSP bypass.

Note that the PoC requires that the victim page has no XFO/CSP frame-ancestors (in order to make use of history navigations) and that there exists an about:srcdoc frame with controlled content, which could happen if e.g. a site allowed users to upload arbitrary HTML content and relied on a CSP on this content.

**VERSION**

Chrome Version: 128.0.6613.115 + stable, dev
Operating System: Windows 11 Version 10.0.22621 Build 22621

**REPRODUCTION CASE**

Please find the relevant PoC attached.

Note that the PoC abuses the fix in <https://issues.chromium.org/issues/40165505> to make an about:srcdoc session history entry navigation fail.

**CREDIT INFORMATION**

Reporter credit: Harry Chen

## Attachments

- [poc-srcdoc-sbx.html](attachments/poc-srcdoc-sbx.html) (text/html, 1.6 KB)

## Timeline

### ha...@gmail.com (2024-09-05)

Sorry, please find the relevant PoC *actually* attached here:

### ct...@chromium.org (2024-09-05)

Thanks for the report.

wjmaclean@ could you PTAL to help assess this report, since you worked on [Issue 40165505](https://issues.chromium.org/issues/40165505)? Adding some other navigations folks as well for visibility.

### aj...@google.com (2024-09-09)

(adding some labels & some folks)

### pe...@google.com (2024-09-09)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cr...@chromium.org (2024-09-11)

[Navigation Triage]
This seems to be more about how PolicyContainer is inherited than about:srcdoc blocking from <https://crbug.com/40165505>.

It sounds like the bug might involve the SchemeIsLocal case, which looks like it was introduced in <https://chromium-review.googlesource.com/c/chromium/src/+/2817740>.

Antonio, can you take a look? Happy to discuss if there are questions about the session history behavior.

### an...@chromium.org (2024-09-12)

The problem seems to be that, when the navigation fails, we store in history, on the `FrameNavigationEntry`, the intended url (which failed to load) alongside with the `PolicyContainer` of the error page. Ideally we would instead store the indented url and the intended `PolicyContainer` (which would have been applied if the navigation had been successful) but that seems complex to implement. Maybe we could just avoid retrieving the `PolicyContainer` from history if the `FrameNavigationEntry` corresponds to a failed navigation. My understanding however is that that information is not present on the `FrameNavigationEntry` at the moment.

I could add a boolean for whether `navigation_request->DidEncounterError()` and store it on the `FrameNavigationEntry`. I would then avoid applying the `PolicyContainer` from history if the `FrameNavigationEntry` ha that boolean=true. Does it make sense?

### cr...@chromium.org (2024-09-12)

Thanks!

Would it be possible to instead store a null PolicyContainer on FrameNavigationEntry when a failed navigation commits? It looks like we already need to support the null case in [[2](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_policy_container_builder.cc;l=56-68;drc=fa1e0cf5238e2600039f60af6909aefbd4cf003c)] from the report, and that would avoid having to add a new bit to FrameNavigationEntry, or worrying about other accesses to the FrameNavigationEntry's PolicyContainer that don't go through GetHistoryPolicies. (We have to be careful about adding new bits to FrameNavigationEntry in general, since that requires reasoning about whether they need to be persisted or not, which is a permanent change to the serialization format.)

Either way, I agree that we don't want the error page's PolicyContainer to be used when a successful load commits. Is that sufficient? Will the successful load then get the appropriate CSP/etc from somewhere else if there isn't one on the FrameNavigationEntry, or will the PolicyContainer be empty?

### ap...@google.com (2024-09-16)

Project: chromium/src
Branch: main

commit b8addf6f6466720e25979c462c6a90d9a72d373b
Author: Antonio Sartori <antoniosartori@chromium.org>
Date:   Mon Sep 16 07:59:21 2024

    Don't store PolicyContainerPolicies of error pages in history
    
    We should never reload the policies of an error page from history,
    since that might end up taking precedence over stricter policies
    inherited from the parent/initiator.
    
    Bug: 364773822
    Change-Id: I903dd11d8f7e771e1f8bc9dc640690da92d61177
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5860536
    Reviewed-by: Charlie Reis <creis@chromium.org>
    Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1355730}

M       content/browser/renderer_host/navigation_controller_impl.cc
M       content/browser/renderer_host/navigation_controller_impl.h
M       content/browser/renderer_host/policy_container_host_browsertest.cc
M       content/test/content_test_bundle_data.filelist
A       content/test/data/page_with_srcdoc_iframe_and_csp.html
A       content/test/data/page_with_srcdoc_iframe_and_csp.html.mock-http-headers

https://chromium-review.googlesource.com/5860536


### cr...@chromium.org (2024-09-17)

IIUC, I think this can be marked fixed as of r1355730 (130.0.6722.0). Feel free to correct me if I'm wrong.

### an...@chromium.org (2024-09-17)

Yes, thanks. I forgot to update the bug.

### sp...@google.com (2024-09-30)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact exploitation mitigation bypass 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-30)

Congratulations Harry! Thank you for your efforts and reporting this issue to us.

### ha...@gmail.com (2024-09-30)

Thank you very much!

### pe...@google.com (2024-12-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/364773822)*
