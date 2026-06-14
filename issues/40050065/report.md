# CSP bypass with about:srcdoc

| Field | Value |
|-------|-------|
| **Issue ID** | [40050065](https://issues.chromium.org/issues/40050065) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2019-09-05 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

I suspect following change caused this bug.  

<https://chromium.googlesource.com/chromium/src.git/+/2ce31ab03b0e860eefff56647617e9851937eb12>

Before above change, navigation inside iframe to `about:blank`, `data:`, `javascript:`, and `about:srcdoc` would commit navigation into existing process, so those url would inherited the origin/process of navigation initiator.

But after the change, if `<iframe src="//evil.com">` on victim.com tries to navigate to `about:srcdoc`, then this will inherit the origin of parent (i.e. victim.com) which is weird.

I was able to abuse this fact to bypass CSP. This is because CSP will try to inherit CSP from navigation initiator.

**VERSION**  

Chrome Version: 78.0.3903.0 canary  

Operating System: Windows 10

**REPRODUCTION CASE**  

Go to <https://test.shhnjk.com/unxssable.php?xss=%3Ciframe%20srcdoc=%22%3Cscript%3Ealert(origin);window.stop()%3C/script%3E%3Cmeta%20http-equiv=refresh%20content=%270;url=https://shhnjk.azurewebsites.net/csp_srcdoc.html%27%3E%22%3E%3C/iframe%3E>

## Attachments

- [unxssable.php](attachments/unxssable.php) (text/plain, 317 B)
- [csp_srcdoc.html](attachments/csp_srcdoc.html) (text/plain, 406 B)

## Timeline

### es...@chromium.org (2019-09-06)

Arthur, can you please take a look?

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### Ju...@microsoft.com (2019-09-06)

This should be Security_Severity-Medium. I can easily bypass most of CSP in Google by this bug.

### sh...@chromium.org (2019-09-07)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2019-09-09)

Thanks for the report!

I verified it:

[Before] https://chromium.googlesource.com/chromium/src.git/+/2ce31ab03b0e860eefff56647617e9851937eb12
Debug mode => The iframe crash due to a DCHECK.
Release mode => The iframe doesn't load properly. The about srcdoc data lives in another process)

[After] https://chromium.googlesource.com/chromium/src.git/+/2ce31ab03b0e860eefff56647617e9851937eb12
I can reproduce bypassing CSP.

Patch https://chromium.googlesource.com/chromium/src.git/+/2ce31ab03b0e860eefff56647617e9851937eb12 is not really the problem. We were protected previously, because the about:srcdoc wasn't able to load at all. Now it can.

So version above 78.0.3903.0 are affected.

### ar...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### el...@chromium.org (2019-09-09)

This does not look like an a11y bug.

### ar...@chromium.org (2019-09-09)

So this reproduce on chrome above 78.0.3903.0. (canary)

In https://crbug.com/chromium/1001982, I tried and succeed to extend it to every stable version of chrome. (M77, M76, M75, ...)

You can use this link:
https://test.shhnjk.com/unxssable.php?xss=%20<iframe%20name="iframe_a"%20srcdoc="<script>alert(origin)</script>%20<p>about-srcdoc%20iframe</p>%20<a%20href=%27https://go-back.glitch.me%27%20target=%27iframe_a%27>click%20here</a>"%20</iframe>

The injected HTML is:
~~~
<iframe name="iframe_a" srcdoc="
  <script>alert(origin)</script>
  <p>about-srcdoc iframe</p>
  <a href='https://go-back.glitch.me' target='iframe_a'>click here</a>"
</iframe>
~~~

You should see javascript execution with the main document origin.

# What changed in between https://crbug.com/chromium/1001283#c1 and this one?

There used to be two navigation code paths for loading about:srcdoc
 1) The normal one. Used only for browser initiated navigation.
 2) The edge-case-legacy one for loading about:srcdoc. Used for document initiated navigation.

I removed path 2) completely. Nowadays, every navigations to about:srcdoc are the same. They are always using path 1.
It looks like path 1 has always been broken, CSP is not properly inherited.

https://crbug.com/chromium/1001283#c1 relied on path 1) to be used. That's why it can only reproduce on M78+.
Here, I am using history.back() in order to force using path 1 on M76.

____________________________________________________


I tried debugging this.

Thanks to this in Document::Loader::FinishNavigationCommit(), we properly inherit the correct |initiator_origin| and |owner_document|.
~~~
  // TODO(dcheng): This differs from the behavior of both IE and Firefox: the
  // origin is inherited from the document that loaded the URL.
  if (loading_url_as_javascript_) {
    owner_document = frame_->GetDocument();
  } else if (Document::ShouldInheritSecurityOriginFromOwner(Url())) {
    Frame* owner_frame = frame_->Tree().Parent();
    if (!owner_frame)
      owner_frame = frame_->Loader().Opener();
    if (auto* owner_local_frame = DynamicTo<LocalFrame>(owner_frame)) {
      owner_document = owner_local_frame->GetDocument();
      initiator_origin = owner_document->GetSecurityOrigin();
    }
  }
~~~

However, later we don't use it. I don't know why?

I made a dummy CL fixing the issue:
https://chromium-review.googlesource.com/c/chromium/src/+/1789541/
(I don't know what it is worth)

I don't really understand how InitializeContentSecurityPolicy() is architectured.
andypaicu@. You worked on GetLastOriginDocumentCSP() and I think you might be the right person to look at this. Do you think you can own this issue? If you don't want, it is fine and I will try to do it myself.

### Ju...@microsoft.com (2019-09-09)

Wow, nice catch arthursonzogni@!

### Ju...@microsoft.com (2019-09-09)

[Empty comment from Monorail migration]

### ar...@chromium.org (2019-09-10)

Reassigning to me, since Andy is OOO.

### sh...@chromium.org (2019-09-10)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2019-09-10)

A gathered a fix and a regression test in:
https://chromium-review.googlesource.com/c/chromium/src/+/1789541

### ar...@chromium.org (2019-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ca6496df420bca8470640b9f9c13e64762bced25

commit ca6496df420bca8470640b9f9c13e64762bced25
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Fri Sep 20 11:20:49 2019

Test and fix about:srcdoc inheritance.

Make about:srcdoc to inherit CSP from its parent.

Bug: 1001982
Change-Id: I5e750a8d821e6a8e8cc81e6c8a0feeb7583de020
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1789541
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Camille Lamy <clamy@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#698438}

[modify] https://crrev.com/ca6496df420bca8470640b9f9c13e64762bced25/content/browser/navigation_browsertest.cc
[modify] https://crrev.com/ca6496df420bca8470640b9f9c13e64762bced25/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/ca6496df420bca8470640b9f9c13e64762bced25/third_party/blink/renderer/core/loader/document_loader.ccx

### ar...@chromium.org (2019-09-20)

This is fixed and tested.

Let's wait a few days on Canary to confirm stability. Then I will ask a merge into M-78

### ar...@chromium.org (2019-09-24)

Hi, I would like to merge into M78 beta:
https://chromiumdash.appspot.com/commit/ca6496df420bca8470640b9f9c13e64762bced25

It has been tested on 79.0.3919.0 for 3 days (Sep 21 2019). I am not aware of any problems so far.

The patch is not really "simple", but it fixes a security issue. Without it, it is easy to bypass Content-Security-Policy.
The security issue is not something that regressed in M77. It was there for a while.

Another question for the person CCed in this issue. Do you think we need to attempt a merge request into M77 in case a respin happens?

### ar...@chromium.org (2019-09-24)

The bot didn't updated this issue. I will do it myself:

[M78] Invalidate the URL systematically when DiscardNonCommittedEntries()

The NavigationController was not invalidating the URL when a pending
entry was removed.

To fix this, be more systematic, more stupid. Always invalidate the URL
when DiscardNonCommittedEntries() is called.

(cherry picked from commit 69a6a1b82a0fb87e6a87b39c48416ddd59636a5c)

Bug: 998284.
Change-Id: I01f1d16bcb25fa827bf68a52db4de531429a8564
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1781434
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Tao Bai <michaelbai@chromium.org>
Reviewed-by: Tommy Li <tommycli@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#697145}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1814828
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/branch-heads/3904@{#383}
Cr-Branched-From: 675968a8c657a3bd9c1c2c20c5d2935577bbc5e6-refs/heads/master@{#693954}

### ar...@chromium.org (2019-09-24)

Ooops, sorry wrong bug. Please forgot about https://crbug.com/chromium/1001283#c18.

### sh...@chromium.org (2019-09-24)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-09-24)

merge approved to M78, branch:3904, pls merge the changes before 12pm PST today Tuesday Sept 24 so it can be included in tomorrow's beta release

### ar...@chromium.org (2019-09-24)

Here is the cherry-pick: https://chromium-review.googlesource.com/c/chromium/src/+/1821906
I need a final review. I am leaving the office now.

### go...@chromium.org (2019-09-24)

Please merge your change to M78 branch 3904 by 12:30 PM PT, today (09/24) so we can pick it up for tomorrow's beta release. Thank you.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2539b2ec8b9f04af4dde3b8b9df2afc9983f5bd7

commit 2539b2ec8b9f04af4dde3b8b9df2afc9983f5bd7
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Wed Sep 25 07:53:25 2019

[M78] Test and fix about:srcdoc inheritance.

Make about:srcdoc to inherit CSP from its parent.

Change-Id: I5e750a8d821e6a8e8cc81e6c8a0feeb7583de020
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1789541
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Camille Lamy <clamy@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#698438}

Bug: 1001283
Change-Id: I6b96df764ace87c6d594878a67177ad4a4335db4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1821906
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/branch-heads/3904@{#444}
Cr-Branched-From: 675968a8c657a3bd9c1c2c20c5d2935577bbc5e6-refs/heads/master@{#693954}

[modify] https://crrev.com/2539b2ec8b9f04af4dde3b8b9df2afc9983f5bd7/content/browser/navigation_browsertest.cc
[modify] https://crrev.com/2539b2ec8b9f04af4dde3b8b9df2afc9983f5bd7/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/2539b2ec8b9f04af4dde3b8b9df2afc9983f5bd7/third_party/blink/renderer/core/loader/document_loader.cc


### sh...@chromium.org (2019-09-25)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-27)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-04)

Congrats! The Panel decided to reward $3,000 for this report :) 

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1001283?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1001982]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050065)*
