# Security: Side-channel attack against Autofill Preview that can steal user's data (e.g., credit card number).

| Field | Value |
|-------|-------|
| **Issue ID** | [40052135](https://issues.chromium.org/issues/40052135) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jp...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2020-04-27 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

Bugs in Chrome's autofill and preview behavior:

1. A novel side-channel attack that can infer values in the user's profile during Preview (i.e., they don't need to actually use autofill). This is built by chaining a series of "smaller" attacks that bypass specific defenses and safeguards that Chrome has in place.
2. New "tricks" for hiding form elements that are autofilled by Chrome.

**VERSION**  

Chrome Version: version 81.0.4044.122 (Official Build) (64-bit)  

Operating System: MacOS Catalina, Windows 10

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

See attached PDF for details, demo videos, and links to demo pages.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Xu Lin (University of Illinois at Chicago), Panagiotis Ilia (University of Illinois at Chicago), Jason Polakis (University of Illinois at Chicago)

## Attachments

- [Autofill-Attacks.pdf](attachments/Autofill-Attacks.pdf) (application/pdf, 93.7 KB)

## Timeline

### me...@chromium.org (2020-04-27)

battre@: Could you please take a look? 

I'm assigning medium severity out of abundance of caution, but some of the examples seem to require querying a large number of potential matches.

[Monorail components: UI>Browser>Autofill]

### pa...@chromium.org (2020-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-28)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@chromium.org (2020-04-28)

Thanks for sharing! I'll think about mitigation strategies.

### ba...@chromium.org (2020-04-29)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f27c6dabf92d3cb6bf065e117d2733cfc038898e

commit f27c6dabf92d3cb6bf065e117d2733cfc038898e
Author: Christoph Schwering <schwering@google.com>
Date: Thu Apr 30 15:43:35 2020

[Autofill] Skip filling fields with non-matching renderer IDs.

autofill::form_util::ForEachMatchingFormFieldCommon() iterates over
a pair of vectors of WebFormControlElements and FormFieldData, respectively.
The assumption is that the elements at corresponding indices match with
each other.

This CL adds a check that both elements indeed have identical form
renderer IDs. If not, the pair is skipped.

Bug: 1075734
Change-Id: I5f84cb8f808eeafa2224db367cc4911705bd7d67
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2172830
Reviewed-by: Dominic Battré <battre@chromium.org>
Reviewed-by: Vadym Doroshenko  <dvadym@chromium.org>
Commit-Queue: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/master@{#764276}

[modify] https://crrev.com/f27c6dabf92d3cb6bf065e117d2733cfc038898e/chrome/renderer/autofill/form_autocomplete_browsertest.cc
[modify] https://crrev.com/f27c6dabf92d3cb6bf065e117d2733cfc038898e/components/autofill/content/renderer/form_autofill_util.cc


### sc...@google.com (2020-05-10)

Thanks a lot for sharing this attack.

Our understanding is that in theory it’s capable of giant search spaces of size 2^200, but practical memory limitations make it infeasible for stealing credit card numbers or email addresses without prior knowledge. Phone numbers, on the other hand, seem to be a very realistic target for the attack (e.g., combined with IP geo lookup to narrow down the search space). Do you concur with this estimate?

Our plan is to address the issue in two ways:

For one thing, we’ll restrict the number of times each piece of information from an address/payment profile is filled into a form. Due to the existence of confirmation fields the general limit can not be as low as one, but we will restrict the number of filling to a single digit number (except for credit cards where the digits may need to be filled into different fields, but they have a very large search space). This should reduce the probeable option space to less than 1000 items. We will conduct further analysis to reduce the number of fillings.

For another, we’ll make Chrome not fill form fields that were created after parsing the form (CL from https://crbug.com/chromium/1075734#c7). (This applies to newly created elements only, not to elements where merely the attributes have changed. Replacing an <input> with a <select> does require creating a new element.) This will break the dynamic field replacement attack and enforce the limit of 200 <option>s per <select>.

Thanks again for reporting the issue.


### sc...@google.com (2020-05-10)

meacer@, Do you have any thoughts on merging the CL(s) that address this bug into a release branch?

### [Deleted User] (2020-05-13)

battre: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jp...@gmail.com (2020-05-13)

Sorry for the late reply but we've had some deadlines on our side. 

I agree with the estimate about phone numbers; other equally sensitive PII can similarly be inferred, e.g., street addresses -- our attack can cover all named geographic places in a major city (NYC has ~102K). While the search spaces for other values are larger, this attack can be combined with other pieces of information (e.g., browser fingerprints) to create appropriate candidate value sets. As such, an option space of 1000 is obviously not as bad as our current attack, but remains a privacy threat nonetheless since it can be combined with the aforementioned additional pieces of information as part of more targeted attacks. 

The dynamic replacement mitigation makes sense, but we would need to investigate it a bit more and see if the decision to "ignore" elements whose attributes have changed can be misused by attackers. 

Could you provide some info on your plans for mitigating the other attack we outlined (i.e., hidden elements that get autofilled without users being aware of them)? While the preview attack is far more egregious, this remains an important issue as average users can trivially be tricked into disclosing very sensitive information. 

### ba...@chromium.org (2020-05-13)

We looked into your mitigation proposals but think that we cannot implement them:

- It is very hard (maybe impossible) to detect reliably whether form elements are hidden (there are many ways to hide them) and on some websites form filling only works because we fill these fields (e.g. the credit card forms by Stripe are split into multiple iframes, each with one visible <input>; the first iframe contains hidden fields that get filled and pushes the value to the visible  <input> fields in the other iframes). We are planning to attack this by providing more transparency into which fields will be filled. We don't have a deadline for that because it requires some bigger rethinking of the UI overall.

- Making the style properties invisible is also very hard (I worked on that for <input type="text"> fields) and there were many edge cases that broke previous attempts.

- The last mitigation (enforcing that the type does not change) was implemented in commit f27c6dabf92d3cb6bf065e117d2733cfc038898e.

koerber@ is working on a CL to limit the number of input elements per type.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/af59e4ea98835b3926dce614096e6153296190dc

commit af59e4ea98835b3926dce614096e6153296190dc
Author: Matthias Körber <koerber@google.com>
Date: Thu May 14 20:42:33 2020

[Autofill] Limits the times a value is filled into a form.

With this change, the value of a specific field type can only be
filled a limited number of times into a specific form.

Bug: 1075734
Change-Id: I7af1535d4877a4847ab84a5c11c70a1be35647a3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2172299
Commit-Queue: Matthias Körber <koerber@google.com>
Reviewed-by: Dominic Battré <battre@chromium.org>
Auto-Submit: Matthias Körber <koerber@google.com>
Cr-Commit-Position: refs/heads/master@{#768957}

[modify] https://crrev.com/af59e4ea98835b3926dce614096e6153296190dc/components/autofill/core/browser/autofill_manager.cc
[modify] https://crrev.com/af59e4ea98835b3926dce614096e6153296190dc/components/autofill/core/browser/autofill_manager_unittest.cc
[modify] https://crrev.com/af59e4ea98835b3926dce614096e6153296190dc/components/autofill/core/common/autofill_constants.h


### [Deleted User] (2020-05-28)

battre: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@chromium.org (2020-05-28)

I think that we consider the limitations we put in place now as sufficient.

### [Deleted User] (2020-05-29)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-01)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-01)

Not requesting merge to beta (M84) because latest trunk commit (768957) appears to be prior to beta branch point (768962). If this is incorrect, please replace the Merge-na label with Merge-Request-84. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-06-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-06-11)

Congrats! The Panel decided to award $500 for this report! 

### jp...@gmail.com (2020-06-11)

Hello,

thanks for the award. Please add my PhD student (xulin1874@gmail.com) to the discussion so she can claim
the award since she did most of the work.

Regarding the boilerplate reminders in the previous email, we have not publicly disclosed our findings.
However, they are currently part of our research under submission at an academic security conference.
Obviously we will follow the standard guidelines for responsible disclosure.

Thanks,
Jason Polakis

### na...@google.com (2020-06-11)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-13)

Sorry that nobody acted upon https://crbug.com/chromium/1075734#c21 until now - done!

### ad...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### xu...@gmail.com (2020-07-16)

Hello, 

I've tested the attack on Chrome 84.0.4147.89 for non-cc/phone elements, and the attack is still working for 40K entries. Here is the demo page for email type: https://xlin48.people.uic.edu/project/preview.html

Regards,
Xu

### ba...@chromium.org (2020-07-21)

Thank you for the update. We will re-investigate.

After an risk assessment and weighing this against some other urgent things, we had to conclude that we may not be able to work on this immediately, unfortunately. I've set up a NextAction to bring this back.

### [Deleted User] (2020-07-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### jd...@chromium.org (2020-11-23)

Hi battre@: friendly ping from a security sheriff. It's been several months since the NextAction date, which itself was kicking the can down the road a bit. Has there been any movement here? What needs to happen to move this security bug along?

Thanks!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/18d3f86206e88156e2eb20c1f691b3b40a779150

commit 18d3f86206e88156e2eb20c1f691b3b40a779150
Author: Christoph Schwering <schwering@google.com>
Date: Tue Nov 24 23:39:39 2020

[Autofill] Limit preview and filling only for non-state fields.

The number of times a value is filled into different fields is limited.
The exception are state fields because websites sometimes have one
state select box for each country and display the relevant select
box once the respective country has been selected.

This CL simplifies this mechanism and makes it more explicit by
encoding the type-dependent limits in TypeValueFormFillingLimit().
As a side effect, the limits apply not just to filled fields but also
unfilled fields of the same type.

Bug: 1075734, 1084903
Change-Id: Icc5e8e082850ed44d9c7fbbc911d03a95033d81f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2557977
Commit-Queue: Matthias Körber <koerber@google.com>
Reviewed-by: Matthias Körber <koerber@google.com>
Auto-Submit: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/master@{#830778}

[modify] https://crrev.com/18d3f86206e88156e2eb20c1f691b3b40a779150/components/autofill/core/browser/autofill_manager.cc
[modify] https://crrev.com/18d3f86206e88156e2eb20c1f691b3b40a779150/components/autofill/core/browser/autofill_manager_unittest.cc
[modify] https://crrev.com/18d3f86206e88156e2eb20c1f691b3b40a779150/components/autofill/core/common/autofill_constants.h


### ad...@google.com (2020-12-21)

schwering@ is https://crbug.com/chromium/1075734#c35 a complete fix? If so it'd be good to mark this bug as Fixed so that Sheriffbot initiates merge proceedings, and we can get on with crediting and rewarding the reporter.

### sc...@google.com (2020-12-22)

Yes, it's a complete fix afaik. Thanks for the reminder!

### vs...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### gi...@google.com (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-03-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b772b48067c431bdbd773be25595c7b9c93f9724

commit b772b48067c431bdbd773be25595c7b9c93f9724
Author: Christoph Schwering <schwering@google.com>
Date: Thu Mar 04 17:21:46 2021

[Autofill] Limit preview and filling only for non-state fields.

The number of times a value is filled into different fields is limited.
The exception are state fields because websites sometimes have one
state select box for each country and display the relevant select
box once the respective country has been selected.

This CL simplifies this mechanism and makes it more explicit by
encoding the type-dependent limits in TypeValueFormFillingLimit().
As a side effect, the limits apply not just to filled fields but also
unfilled fields of the same type.

(cherry picked from commit 18d3f86206e88156e2eb20c1f691b3b40a779150)

Bug: 1075734, 1084903
Change-Id: Icc5e8e082850ed44d9c7fbbc911d03a95033d81f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2557977
Commit-Queue: Matthias Körber <koerber@google.com>
Reviewed-by: Matthias Körber <koerber@google.com>
Auto-Submit: Christoph Schwering <schwering@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#830778}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2731409
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1560}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/b772b48067c431bdbd773be25595c7b9c93f9724/components/autofill/core/browser/autofill_manager.cc
[modify] https://crrev.com/b772b48067c431bdbd773be25595c7b9c93f9724/components/autofill/core/browser/autofill_manager_unittest.cc
[modify] https://crrev.com/b772b48067c431bdbd773be25595c7b9c93f9724/components/autofill/core/common/autofill_constants.h


### vs...@google.com (2021-03-08)

[Empty comment from Monorail migration]

### ko...@chromium.org (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1075734?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052135)*
