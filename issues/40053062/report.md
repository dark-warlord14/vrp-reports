# Security: Full CSP bypass through blob: URIs

| Field | Value |
|-------|-------|
| **Issue ID** | [40053062](https://issues.chromium.org/issues/40053062) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gi...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2020-08-12 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome does not properly inherit a CSP through blob URIs even though they share the same origin as the context thats creates them.

As long as an attacker can execute JavaScript on a victim page, this allows CSP to be entirely bypassed by creating a blob URI and assigning it to the top frame's location.

Note that this vulnerability is not present in Firefox because it treats blob URIs similarly to about:blank. As far as I can tell, the spec is unclear about this: <https://w3c.github.io/FileAPI/#originOfBlobURL>.

**VERSION**  

Chrome Version: 84.0.4147.105 stable  

Operating System: Windows 10 OS Version 1903 (Build 18362.959)

This vulnerability is also present in Chrome canary 86.0.4231.0.

**REPRODUCTION CASE**  

There are two origins involved in this PoC.  

attacker origin: <https://cgpq29r51wfnl2zd-attacker.okay.blue>  

victim origin: <https://cgpq29r51wfnl2zd-victim.netlify.app>

All paths on the victim origin have a CSP of: default-src 'none'; script-src 'unsafe-inline'

There is also a secret value located at <https://cgpq29r51wfnl2zd-victim.netlify.app/secret>. Because of CSP, the victim origin is normally not able to fetch() the secret.

Therefore, if you visit <https://cgpq29r51wfnl2zd-victim.netlify.app/blocked> an error should appear in the console.

However, if you visit the attacker page at <https://cgpq29r51wfnl2zd-attacker.okay.blue>, the secret value should appear in an alert().

Analysis:  

\* The attacker page first loads the victim page in an iframe.  

\* The victim page then uses URL.createObjectURL to create a blob URI containing HTML which fetches /secret.  

\* The victim page then assigns the blob URI to parent.location. This replaces the parent attacker page, allowing the contents of the blob URI to execute without any CSP restrictions.  

\* Note that sandbox="allow-top-navigation" is used on the attacker page so the victim page can set the top frame's location without any user interaction.  

\* The contents of /secret are then displayed in an alert(). They could also easily be sent to the attacker's server.

The attacker page, the victim page, the secret page, and the blocked page are attached.

**CREDIT INFORMATION**  

Reporter credit: Philip Papurt

## Attachments

- [attacker.html](attachments/attacker.html) (text/plain, 147 B)
- [victim.html](attachments/victim.html) (text/plain, 263 B)
- [blocked.html](attachments/blocked.html) (text/plain, 103 B)
- [secret.html](attachments/secret.html) (text/plain, 41 B)

## Timeline

### va...@chromium.org (2020-08-12)

mkwst: This seems eerily similar to https://crbug.com/chromium/1115298 so assigning it to you.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### mk...@chromium.org (2020-08-13)

And I'm assigning it to Arthur. :)

Ideally, it won't reproduce in Canary, as he's made some recent changes in response to other issues.

### ar...@google.com (2020-08-13)

This also reproduce on Canary.
I think I imagine what happens here. This will likely be fixed together with:
- https://crbug.com/chromium/1109167
- https://crbug.com/chromium/1115298
which have likely the same cause.

### va...@chromium.org (2020-08-13)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-14)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-28)

arthursonzogni: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2020-09-02)

pmeuleman@ and antoniosartori@ are going to improve how a given policy, like
CSP, are inherited across documents/navigations. (PolicyContainer)

There are many CSP bugs around inheritance below:
- https://crbug.com/chromium/1117687
- https://crbug.com/chromium/1115628
- https://crbug.com/chromium/1115298
- https://crbug.com/chromium/1115045
- https://crbug.com/chromium/1109167
- https://crbug.com/chromium/971231
- https://crbug.com/chromium/957606

I believe their future work might fix several issues in this list.

### [Deleted User] (2020-09-16)

arthursonzogni: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### na...@chromium.org (2021-02-24)

[security bug triage]: Ping on getting this prioritized along with https://crbug.com/chromium/1117687.

### an...@chromium.org (2021-02-25)

This CL https://chromium-review.googlesource.com/c/chromium/src/+/2667858 fixes the inheritance mechanism for CSPs and will close this bug.

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-04)

https://chromium-review.googlesource.com/c/chromium/src/+/2725520 has been merged and this is fixed.

Regression test here https://chromium-review.googlesource.com/c/chromium/src/+/2721995.

### [Deleted User] (2021-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-04)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M89. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-04)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-03-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/89859c05f4f266a60fabcc9f57d8eee20e7ffe61

commit 89859c05f4f266a60fabcc9f57d8eee20e7ffe61
Author: Antonio Sartori <antoniosartori@chromium.org>
Date: Fri Mar 05 10:35:50 2021

CSP: Add WPTs for inheritance to blob URLs

This CL adds Web Platform Tests checking that we correctly inherit
Content Security Policy from the navigation initiator if a
cross-origin child frame navigates the top frame to a blob URL.

Bug: 1115628,1149272
Change-Id: I3214333f61eb48542b0ba6712cfb58ee0342f796
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2721995
Reviewed-by: Mike West <mkwst@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Cr-Commit-Position: refs/heads/master@{#860177}

[add] https://crrev.com/89859c05f4f266a60fabcc9f57d8eee20e7ffe61/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/blob-url-inherits-from-initiator.sub.html
[add] https://crrev.com/89859c05f4f266a60fabcc9f57d8eee20e7ffe61/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/support/navigate-parent-to-blob.html


### ad...@google.com (2021-03-10)

https://chromium-review.googlesource.com/c/chromium/src/+/2667858 landed after M90 branch point so adding M90 merge request.

### ad...@google.com (2021-03-10)

Approving merge to M90, branch 4430.

I'm going to reject merge to M89 as it's medium severity, and anything to do with CSP could conceivably have unforeseen compatibility consequences.

### am...@google.com (2021-03-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-10)

Congratulations, Philip! The VRP Panel has decided to award you $5000 for this report. Someone from the finance team will be in touch with you soon to arrange payment. Thanks for your contributions and nice work! 

### am...@google.com (2021-03-11)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-11)

In https://crbug.com/chromium/1115628#c18 I copied the wrong CL.

This has been fixed by https://chromium-review.googlesource.com/c/chromium/src/+/2667858

### sr...@google.com (2021-03-15)

Please merge your CL to M90 branch asap ( before 3pm PST, tuesday March 16, 2021). This will help get the CL's into this weeks beta release on wednesday.

### an...@chromium.org (2021-03-16)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-16)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-16)

Same as https://bugs.chromium.org/p/chromium/issues/detail?id=1115298#c33, not merging in M90.

### an...@chromium.org (2021-03-16)

Same as https://bugs.chromium.org/p/chromium/issues/detail?id=1115298#c33, not merging in M90.

### gi...@gmail.com (2021-04-17)

Would it be possible to change the reporter credit to "Philip Papurt (@ginkoid)" on this issue, https://crbug.com/chromium/1117687, and https://crbug.com/chromium/1190608. Thanks!


### am...@chromium.org (2021-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-06-01)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vs...@google.com (2021-06-14)

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

This issue was migrated from crbug.com/chromium/1115628?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053062)*
