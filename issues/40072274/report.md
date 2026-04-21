# Bypass PaymentRequest.show() calls after the first.

| Field | Value |
|-------|-------|
| **Issue ID** | [40072274](https://issues.chromium.org/issues/40072274) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Payments |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | np...@chromium.org |
| **Created** | 2023-09-14 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

PoC (use chrome canary): [https://mixolydian-wild-legal.glitch.me/?url=https://terjanq.me/xss.php?h[Cross-Origin-Opener-Policy]=same-origin](https://mixolydian-wild-legal.glitch.me/?url=https://terjanq.me/xss.php?h%5BCross-Origin-Opener-Policy%5D=same-origin)  

This opens a COOP protected window without user interaction that could repletely make query's for an XS-Search attack.

Use chrome canary as its a new feature <https://docs.google.com/document/d/16DHqqPWe5oM6Rucnn6Y1llhJ-DoEeLtTWFldJFg4iqA/edit>  

I will attach the files and a PoC video :)

**Problem Description:**  

By abusing the chrome page auto reloader such as with max redirects (<https://xsinator.com/testcases/files/maxredirect.php?n=19&url=https://mixolydian-wild-legal.glitch.me/?url=><ATTACKER PAGE>) you can bypass the following rule:  

PaymentRequest.show() calls after the first (per page load) require either transient user activation or delegated payment request capability.

**Additional Comments:**

\*\*Chrome version: \*\* 119 \*\*Channel: \*\* Canary

**OS:** Windows

## Attachments

- [xsleaks.mp4](attachments/xsleaks.mp4) (video/mp4, 523.7 KB)
- [index.html](attachments/index.html) (text/plain, 609 B)
- [index.js](attachments/index.js) (text/plain, 938 B)
- [manifest.json](attachments/manifest.json) (text/plain, 811 B)
- [pay.html](attachments/pay.html) (text/plain, 635 B)
- [pay.js](attachments/pay.js) (text/plain, 285 B)
- [service-worker.js](attachments/service-worker.js) (text/plain, 3.9 KB)

## Timeline

### [Deleted User] (2023-09-14)

[Empty comment from Monorail migration]

### nh...@google.com (2023-09-15)

Can you clarify what you think the security impact is here?

There might be a bug in when PaymentRequest.show() can show without user interaction, although in the video it looks like the tab is navigating away from and back to the poc site, and the payment request window is only showing once per load, as mentioned in https://docs.google.com/document/d/16DHqqPWe5oM6Rucnn6Y1llhJ-DoEeLtTWFldJFg4iqA/edit. When/how often the payment request window appears seems like a possible abuse issue instead of a security bug.

I don't see how COOP is relevant to this issue.

### nd...@protonmail.com (2023-09-15)

This mitigation is meant to be once per web contents, i.e. across navigation, so that a page can’t just reload to get another activationless show()

cross-origin-opener-policy restricts the opener after the first page load this means you can normally only leak 1 bit per user interaction as each attempt needs to open a new tab.

This bug removes the requirement for some side channel attacks:
- Timing how long it takes to navigate off the attackers page for example to detect a cached resource.
- Abuse the shared connection pool like if the XS-Search endpoint opens a connection to a host on a successful search.

The main migration for the attacks is that the attacker page needs to be the active window the ways I thought of are:
- Wait for user to go idle
- Use a tiny popup

### ar...@google.com (2023-09-18)

[secondary security shephard]

Thanks! 

FoundIn-118: According to https://chromestatus.com/feature/4879115349393408

+CC nburris@ owner of the new feature FYI.
+others FYI: rouslan@, danyao@

@reporter: Sorry, I am a bit lost. I was not able to figure out how to use this to leak cross-origin data.
This allow to make repeated call to `PaymentRequest.show()`. It has a supportedMethods which could be interpreted as an URL:
https://www.w3.org/TR/payment-method-id/#url-based-payment-method-identifiers
Then, I guess the URL might be fetched. Could you please help me understand what makes fetching the URL through the PaymentRequest more valuable to an attacker than what it could do with other methods? Is this concerns about bypassing some kind of third-party network partitioning?

[Monorail components: Blink>Payments]

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### ro...@chromium.org (2023-09-18)

Nick: Does it make sense to prevent this type of behavior* regardless of whether this is deemed a security bug?

* - The behavior seems to be repeatedly showing PaymentRequest.show() without a user gesture on the same tab, because the page navigates back and forth between two different origins.

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-09-19)

> what makes fetching the URL through the PaymentRequest more valuable to an attacker than what it could do with other methods
Renders a victim page with SameSite=Lax cookies but without the need to open a popup that would require a lot of user interaction if the website had COOP.
(1 tab per query)

Stuff like fetch(), xmlhttprequest would not be good enough since they dont send SameSite=Lax cookies that is set by default now as such would be an unauthenticated request.

> because the page navigates back and forth between two different origins.
Its not that simple its using a browser initiated reload I think the code that allows for the bypass is:
https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/payment_request_web_contents_manager.cc;drc=a6bdc8f2993883fc55eb9cb0945694299b056675;l=44 the use of !navigation_handle->IsRendererInitiated() should not imply user interaction

### np...@google.com (2023-09-19)

Yes, we do assume a browser initiated navigation (i.e. !NavigationHandle::IsRendererInitiated()) is user initiated. This should be the case based on the API comment[1], and there's at least one other usage of this API in Chrome that assumes browser initiated means user initiated, in PermissionRequestManager's implementation[2] to similarly restrict notification prompts to once per page load. I am not familiar with the "chrome page auto reloader" implementation details, but it sounds like this type of navigation should have IsRendererInitiated true if it is the result of a renderer redirect.

+japhet@ I see you've done some work in this area of navigations, do you think this type of navigation should be considered renderer initiated? Can you point us to how we might implement this?

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/public/browser/navigation_handle.h;l=162-175;drc=2b6336bcd18bd565f708ab329d13290eee695c02
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_request_manager.cc;l=429;drc=a61b95c63b0b75c1cfe872d9c8cdf927c226046e

### [Deleted User] (2023-09-19)

[Empty comment from Monorail migration]

### me...@google.com (2023-09-19)

Setting medium as severity, but being able to repeatedly show the payment dialog is only useful when chained with other issues, so this might arguably be low severity too. 

### nd...@protonmail.com (2023-09-19)

Makes sense for IsRendererInitiated to be true for when threes a automatic reload since its automatic and based of the renderers request.
This would also fix the download request limit https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/download_request_limiter.cc;drc=49a952fddb576b129aab7c6b333513b0d9e22adf;l=131

This function has been used for security checks in the past such as WAR
https://chromium-review.googlesource.com/c/chromium/src/+/3846133/28/extensions/browser/extension_navigation_throttle.cc
// A browser-initiated navigation is always considered trusted, and thus
  // allowed.
  if (!navigation_handle()->IsRendererInitiated())
    return content::NavigationThrottle::PROCEED;

### [Deleted User] (2023-09-20)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2023-09-21)

Reminder M118 is already in Beta and Stable promotion is coming VERY soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### ro...@google.com (2023-09-21)

[Empty comment from Monorail migration]

### ro...@google.com (2023-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2023-09-25)

Reminder M118 is already in Beta and Stable promotion is coming VERY soon. Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### np...@google.com (2023-09-25)

Fix in progress: https://chromium-review.googlesource.com/c/chromium/src/+/4890868
Investigation doc (internal): https://docs.google.com/document/d/1UW9Sc_M4t4nZ4FuHtT-AYYy-uU_45d_YtCeJorCuDoM/edit?usp=sharing

The quick fix that we'll merge to M118 is to disallow multiple activationless show() across any browser reload. I opened https://crbug.com/chromium/1486644 to look into a follow-up change to re-allow activationless show after a user-initiated browser reload, which will probably require some more complex changes on the NavigationHandle side.

### gi...@appspot.gserviceaccount.com (2023-09-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/509dcc533a5f12d5f0233fe6e4f062a5acd0a4b8

commit 509dcc533a5f12d5f0233fe6e4f062a5acd0a4b8
Author: Nick Burris <nburris@chromium.org>
Date: Tue Sep 26 15:07:27 2023

[PaymentRequest] Don't reset activationless show bit for browser reload

With this change, PaymentRequestWebContentsManager does not reset the
had_activationless_show_ bit on a browser reload, to disallow multiple
activationless show() calls across browser reloads.

Bug: 1482626
Change-Id: Idd0b9246b9cbf78d1f134eb60cfb9f81aefe2bf3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4890868
Commit-Queue: Nick Burris <nburris@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Auto-Submit: Nick Burris <nburris@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1201585}

[modify] https://crrev.com/509dcc533a5f12d5f0233fe6e4f062a5acd0a4b8/components/payments/content/payment_request_web_contents_manager.cc
[modify] https://crrev.com/509dcc533a5f12d5f0233fe6e4f062a5acd0a4b8/chrome/browser/payments/payment_handler_ui_browsertest.cc


### np...@google.com (2023-09-26)

Confirmed the fix in a local build, will also confirm in next Canary before merging to M118.

### pg...@google.com (2023-09-26)

marking the bug as fixed (=work completed on main, needs merges) so that our automation can apply the right labels (including merge request labels) and get the bug to the right places.

removing needs-feedback as the feedback requested has been provided

### [Deleted User] (2023-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-27)

Merge review required: M118 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### np...@google.com (2023-09-27)

1. This is a fix for a medium-severity security bug for a new feature in M118.
2. https://chromium-review.googlesource.com/c/chromium/src/+/4890868
3. Not release yet, but confirmed manually in a tip of tree build and will also confirm in the next canary release ASAP. The fix also has test coverage.
4. This is a fix for a small feature which is itself behind a flag that is enabled by default in M118.
5. N/A
6. N/A

### wf...@chromium.org (2023-09-27)

[vrp panel] I wonder if this should be Low and not Medium, the security impact here seems quite well mitigated...?

### sm...@chromium.org (2023-09-28)

> [vrp panel] I wonder if this should be Low and not Medium, the security impact here seems quite well mitigated...?

Not clear to me who this question is directed at, can you clarify who you are asking?

From the Blink>Payments perspective, we weren't convinced of the security impact, though we think it's a clear product bug that our anti-spam mitigation failed to handle this case and we're very grateful that it was reported. But we're also not the security experts, so we don't feel that we're well positioned to evaluate security impact!

### np...@google.com (2023-09-28)

Re merge-review-118, confirmed the fix in today's Canary 119.0.6034.3.

### nd...@protonmail.com (2023-09-28)

I don't mind this being set to Low based of the migration that it needs to be the active window.
Impact depends on how hard it is to get a user to go idle or ignore a very small window I dont think a user would just leave the attack running without a justification.

### am...@chromium.org (2023-09-28)

Hi smcgruer@ apologies for the ambiguity in the direction of question #29. Not directed specifically at you, but we always appreciate the input from the SME code / feature owners. 
We are also appreciative that this issue was reported to us, but from a security standpoint, this issue is pretty significantly mitigated by the preconditions and small window to exploit this and the high bar to convince a user to engage in this way. 
As such, and also with the reporter concurring (thanks, ndevtk!) I'm to downgrade the severity to low.  

I'm also removing the merge approval and RBS label. As a low severity issue, this is not a release blocking issue nor requires merge. 

### am...@google.com (2023-09-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-29)

Congratulations NDevTk! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### nd...@protonmail.com (2023-09-29)

Thanks :)

### gi...@appspot.gserviceaccount.com (2023-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/34520f73b407ae07c6e9b61fe161d08584a91ded

commit 34520f73b407ae07c6e9b61fe161d08584a91ded
Author: Nick Burris <nburris@chromium.org>
Date: Fri Sep 29 17:46:46 2023

Replace flaky PaymentRequestActivationlessShowTest

PaymentRequestActivationlessShowTest.WithBrowserReload was recently
added to test activationless show() behaviour across a browser reload.
The test is flaky after landing, so remove this test in favor of unit
testing.

Bug: 1482626
Change-Id: I1bafc4a735dbe5edec08fc28c4a40c12f5809101
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4903487
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Nick Burris <nburris@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1203355}

[modify] https://crrev.com/34520f73b407ae07c6e9b61fe161d08584a91ded/components/payments/content/payment_request_web_contents_manager_unittest.cc
[modify] https://crrev.com/34520f73b407ae07c6e9b61fe161d08584a91ded/chrome/browser/payments/payment_handler_ui_browsertest.cc


### [Deleted User] (2023-09-29)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M118, which branched on 2023-09-05 (Chromium branch: 5993, Chromium branch position: 1192594)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-09-29)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1482626?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072274)*
