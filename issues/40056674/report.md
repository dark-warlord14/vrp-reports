# Security: Overlong iframe CSP attribute allows you to send near-arbitrary length headers to a server and induce server errors

| Field | Value |
|-------|-------|
| **Issue ID** | [40056674](https://issues.chromium.org/issues/40056674) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 1s...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2021-07-26 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

a large iframe csp attribute results in chrome sending a Sec-Fetch-CSP header without any length limit on the request to the iframe's src.

this allows a malicious attacker to induce server errors when the request headers are too large, and the error is detectable via measuring timing of the iframe's onload event.

Therefore, this attack can be used to do things such as measure the \*exact\* length of a user's cookies for any website that has SameSite=None cookies. It can also be used to probe if resources are cached (although, one would need to defeat the partitioned cache as well), as if the resource is cached, the server would not return an error.

In bug id #959757, the length of the Referer header was limited in order to prevent these sorts of xs-leak attacks.

**VERSION**  

Chrome Version: 91.0.4472.164 + stable  

Operating System: Windows 20H2 19042.1110

**REPRODUCTION CASE**  

See attached file. Network tab indicates that request to <https://example.com> returns a 431, and the sent request headers have an extremely long Sec-Fetch-CSP header.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Ankur Sundara

## Attachments

- [iframe_csp_poc.html](attachments/iframe_csp_poc.html) (text/plain, 295 B)
- [iframe_csp_timing_poc.html](attachments/iframe_csp_timing_poc.html) (text/plain, 933 B)

## Timeline

### [Deleted User] (2021-07-26)

[Empty comment from Monorail migration]

### 1s...@gmail.com (2021-07-26)

see attached POC to demonstrate that the error is detectable via timing.

when I set the cspLen to 49137 or 49138 (may differ for you due to user-agent differences, but should be about the same), the total request time is ~2974.1

when I set the cspLen to 49139 though, the headers cross the threshold of becoming too large for example.com's server to process, and the server starts returning 431's. this results in a total request time of ~6424.5, which is over 2x the previous time and easily detectable.

there may be an easier way to detect iframes refusing to load as well, but timing was the most obvious way that came to mind.

### do...@chromium.org (2021-07-27)

+CSP folks, can you please follow up on this and help triage?

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### an...@google.com (2021-07-27)

I believe limiting the csp attribute to a reasonable length (4Kb, like for the Referer header?) makes sense. We should probably block loading iframes which have longer csp attributes.

### an...@chromium.org (2021-07-27)

[Empty comment from Monorail migration]

### mk...@google.com (2021-07-27)

I agree with Antonio above. We should likely cap the length of the CSP attribute in a similar way to the cap we placed on the `referer` header. When `referer` exceeds that length, we strip it down to an origin, which is pretty clearly safe. I'm not sure the same applies to CSP (since developers could, for whatever reason, have only gotten to `script-src` in the 4097th bit of their policy). Failing the request seems reasonable, as would swapping the policy out with something known-safe like `default-src 'none'` (which would have basically the same effect, since the page would likely not accept the result).

Perhaps Antonio has time to make that behavioral change?

### [Deleted User] (2021-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-27)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### 1s...@gmail.com (2021-08-02)

I believe capping the CSP length and swapping the policy w/ something known-safe would work.


Also, reporter credit (if applicable) should be updated to: Matt Dyas, Ankur Sundara

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-10)

antoniosartori: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8af66de55aad1b8230a6ec4f14fef8ba0f19a498

commit 8af66de55aad1b8230a6ec4f14fef8ba0f19a498
Author: Antonio Sartori <antoniosartori@chromium.org>
Date: Tue Aug 24 15:01:17 2021

Limit length of 'csp' attribute

Most servers limit the length of request headers anywhere. 4Kb seems
like a reasonable limit, which some popular http servers have by
default, and which we already enforce for Referer
(https://crrev.com/c/1595872).

I would have liked the constant 4096 to be shared between //content
and blink. This would have required putting it somewhere like in
//services/network or in //third_party/blink/common, creating a new
file for it. I thought it would be easier to avoid that for this
change.

It would be safer to not load the iframe document, or to impose some
very strict CSP like "default-src 'none'", instead than just ignoring
the 'csp' attribute if that's too long. However, ignoring is what we
already do if the attribute contains illegal characters or does not
match the CSP grammary or is not subsumed by the parent iframe's csp
attribute. For this change, I believe it's better to stay consistent
with that, and later change the CSPEE code to block loading in all
those cases.

Bug: 1233067
Change-Id: Ie9cd3db82287a76892cca76a0bf0d4a1613a3055
Fixed: 1233067
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057048
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/main@{#914730}

[modify] https://crrev.com/8af66de55aad1b8230a6ec4f14fef8ba0f19a498/content/browser/content_security_policy_browsertest.cc
[modify] https://crrev.com/8af66de55aad1b8230a6ec4f14fef8ba0f19a498/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/8af66de55aad1b8230a6ec4f14fef8ba0f19a498/third_party/blink/renderer/core/html/html_iframe_element.cc
[modify] https://crrev.com/8af66de55aad1b8230a6ec4f14fef8ba0f19a498/third_party/blink/web_tests/external/wpt/content-security-policy/embedded-enforcement/required_csp-header.html


### [Deleted User] (2021-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-25)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-01)

Congratulations, Ankur! The VRP Panel has decided to award you $2000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for reporting this issue to us! 

### 1s...@gmail.com (2021-09-02)

Thanks so much! :)

### am...@google.com (2021-09-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### gi...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5077260de3eabb46737bb778b875b3e42426bed4

commit 5077260de3eabb46737bb778b875b3e42426bed4
Author: Antonio Sartori <antoniosartori@chromium.org>
Date: Thu Nov 04 15:16:26 2021

[M90-LTS] Limit length of 'csp' attribute

Most servers limit the length of request headers anywhere. 4Kb seems
like a reasonable limit, which some popular http servers have by
default, and which we already enforce for Referer
(https://crrev.com/c/1595872).

I would have liked the constant 4096 to be shared between //content
and blink. This would have required putting it somewhere like in
//services/network or in //third_party/blink/common, creating a new
file for it. I thought it would be easier to avoid that for this
change.

It would be safer to not load the iframe document, or to impose some
very strict CSP like "default-src 'none'", instead than just ignoring
the 'csp' attribute if that's too long. However, ignoring is what we
already do if the attribute contains illegal characters or does not
match the CSP grammary or is not subsumed by the parent iframe's csp
attribute. For this change, I believe it's better to stay consistent
with that, and later change the CSPEE code to block loading in all
those cases.

M90 merge issues:
  content/browser/content_security_policy_browsertest.cc is not
  present on M90

(cherry picked from commit 8af66de55aad1b8230a6ec4f14fef8ba0f19a498)

Bug: 1233067
Change-Id: Ie9cd3db82287a76892cca76a0bf0d4a1613a3055
Fixed: 1233067
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057048
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#914730}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3240285
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1658}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/5077260de3eabb46737bb778b875b3e42426bed4/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/5077260de3eabb46737bb778b875b3e42426bed4/third_party/blink/renderer/core/html/html_iframe_element.cc
[modify] https://crrev.com/5077260de3eabb46737bb778b875b3e42426bed4/third_party/blink/web_tests/external/wpt/content-security-policy/embedded-enforcement/required_csp-header.html


### rz...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1233067?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056674)*
