# Security: Full CSP bypass through filesystem URIs

| Field | Value |
|-------|-------|
| **Issue ID** | [40053113](https://issues.chromium.org/issues/40053113) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gi...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2020-08-18 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome does not properly inherit a CSP through filesystem URIs even though they share the same origin as the context thats creates them.

As long as an attacker can execute JavaScript and load iframes in a victim page, this allows CSP to be fully bypassed by creating a filesystem URI and assigning it to the location of a grandchild frame whose parent is in a different origin than the top frame.

Note that this vulnerability is somewhat similar to <https://crbug.com/chromium/1115628>. However, I felt that this is worth reporting seperately because of the entirely different filesystem scheme and additional restrictions placed on filesystem URIs, requiring a very different frame structure.

**VERSION**  

Chrome Version: 84.0.4147.125 stable  

Operating System: Windows 10 OS Version 1903 (Build 18362.959)

This vulnerability is also present in Chrome canary 86.0.4237.0.

**REPRODUCTION CASE**  

There are two origins involved in this PoC.  

Attacker origin: <https://8a53k1sqt5elsz52-attacker.okay.blue>  

Victim origin: <https://8a53k1sqt5elsz52-victim.netlify.app>

All paths on the victim origin have a CSP of: default-src 'none'; script-src 'unsafe-inline'; frame-src <https://8a53k1sqt5elsz52-attacker.okay.blue>

There is also a secret value located at <https://8a53k1sqt5elsz52-victim.netlify.app/secret>. Because of CSP, pages on the victim origin are normally not able to fetch() the secret.

Therefore, if you visit <https://8a53k1sqt5elsz52-victim.netlify.app/blocked> an error should appear in the console.

However, if you visit <https://8a53k1sqt5elsz52-victim.netlify.app>, the secret value should appear in an alert().

Analysis:  

\* The victim page first loads the attacker page in an iframe.  

\* Upon load of the attacker iframe, the victim page creates a filesystem URI containing HTML which fetches /secret.  

\* The victim page then assigns the filesystem URI to an empty iframe in the attacker page using contentWindow.frames[0].location.  

\* The contents of /secret are then fetch()ed and displayed in an alert(). They could also easily be sent to the attacker's server.

The victim page, the attacker page, the secret page, and the blocked page are attached.

**CREDIT INFORMATION**  

Reporter credit: Philip Papurt

## Attachments

- [victim.html](attachments/victim.html) (text/plain, 663 B)
- [attacker.html](attachments/attacker.html) (text/plain, 34 B)
- [secret.html](attachments/secret.html) (text/plain, 41 B)
- [blocked.html](attachments/blocked.html) (text/plain, 103 B)

## Timeline

### mp...@chromium.org (2020-08-20)

Thanks for the report, adding the same owner/CC as https://crbug.com/chromium/1115628.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### [Deleted User] (2020-08-21)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

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

### [Deleted User] (2020-09-30)

arthursonzogni: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

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

### [Deleted User] (2021-02-22)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2021-02-23)

This would require PolicyContainer to be implemented, with support for CSP, with support for filesystem URL. The way to go is still long.

### [Deleted User] (2021-02-23)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@chromium.org (2021-02-24)

[security bug triage]: Hey Arthur, can we please prioritize this bug and have it fixed soon? It has been open for a while now. I think recently there has been some work on CSP inheritance and if that's correct, it will be great to get this bug and https://crbug.com/chromium/1115628 fixed.

### an...@chromium.org (2021-02-25)

This CL https://chromium-review.googlesource.com/c/chromium/src/+/2667858 fixes the inheritance mechanism for CSPs and will close this bug.

### an...@chromium.org (2021-02-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-04)

This has been fixed by https://chromium-review.googlesource.com/c/chromium/src/+/2667858 

Regression test here https://chromium-review.googlesource.com/c/chromium/src/+/2726511

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

### gi...@appspot.gserviceaccount.com (2021-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4357dc9e1c28b3225a52925b69ee642937fb110b

commit 4357dc9e1c28b3225a52925b69ee642937fb110b
Author: Antonio Sartori <antoniosartori@chromium.org>
Date: Wed Mar 10 09:24:07 2021

CSP: Add internal WPTs for filesystem URL inheritance

This change adds internal Web Platform Tests to check that we
correctly inherit Content Security Policies to filesystem URLs.

Bug: 1117687,1149272
Change-Id: I4f78d2dae42ba29d67918764198c71b5def2a5d7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2726511
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Cr-Commit-Position: refs/heads/master@{#861487}

[add] https://crrev.com/4357dc9e1c28b3225a52925b69ee642937fb110b/third_party/blink/web_tests/wpt_internal/content-security-policy/inheritance/filesystem-url-inherits-from-initiator.sub.html


### ad...@google.com (2021-03-10)

https://chromium-review.googlesource.com/c/chromium/src/+/2667858 landed after M90 branch point, so adding merge request to 90 as well as 89.

### ad...@google.com (2021-03-10)

Approving merge to M90, branch 4430.

I'm going to reject merge to M89 as it's medium severity, and anything to do with CSP could conceivably have unforeseen compatibility consequences.

### am...@google.com (2021-03-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-10)

Congratulations, Philip! The VRP Panel has decided to award you $5,000 for this report. As I mentioned in the other issue, a member from our finance team will be in touch with you soon to arrange payment. Thanks for your efforts and great work! 

### go...@chromium.org (2021-03-11)

Please merge your change to M90 branch 4430 ASAP. Thank you.

### an...@chromium.org (2021-03-11)

Unfortunately the fix https://chromium-review.googlesource.com/c/chromium/src/+/2667858 build upon some other changes and is not easily cherry-pickable. Moreover, as it completely changes the way we inherit CSPs, it comes with is own risks.

Because of that, I would prefer NOT to merge to M90.

(Same goes for all related bugs fixed by the same change.)

### am...@google.com (2021-03-11)

[Empty comment from Monorail migration]

### go...@chromium.org (2021-03-11)

*** Bulk Edit ***

Please merge your change to M90 branch 4430 ASAP. Thank you.

### go...@chromium.org (2021-03-12)

*** Bulk Edit ***

Please merge your change to M90 branch 4430 ASAP.

If it is merged already, please remove" "Merge-Approved-90" label, 
apply "merge-merged-4430" & "merge-merged-90 labels and provide merge CL link in bug.

Thank you.

### go...@chromium.org (2021-03-15)

*** Bulk Edit ***

Please merge your change to M90 branch 4430 ASAP.

If it is merged already, please remove" "Merge-Approved-90" label, 
apply "merge-merged-4430" & "merge-merged-90 labels and provide merge CL link in bug.

Thank you.

### sr...@google.com (2021-03-15)

Please merge your CL to M90 branch asap ( before 3pm PST, tuesday March 16, 2021). This will help get the CL's into this weeks beta release on wednesday.

### an...@chromium.org (2021-03-16)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-03-16)

Same as https://bugs.chromium.org/p/chromium/issues/detail?id=1115298#c33, not merging in M90.

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

This issue was migrated from crbug.com/chromium/1117687?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1130587]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053113)*
