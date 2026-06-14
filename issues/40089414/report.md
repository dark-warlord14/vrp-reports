# Security: content security policy bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40089414](https://issues.chromium.org/issues/40089414) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2017-10-26 |
| **Bounty** | $1,000.00 |

## Description

AFFECTED PRODUCTS
--------------------
chrome 62.0.3202.62 stable


DESCRIPTION
--------------------
online demo:
http://xsser.math1as.com/csp.html
firefox & safari block the request,but chrome does not

in one word
"CSP not inherited after iframe navigate to about:blank scheme uri"

## Attachments

- [firefox.jpg](attachments/firefox.jpg) (image/jpeg, 68.4 KB)
- [safari.jpg](attachments/safari.jpg) (image/jpeg, 228.5 KB)

## Timeline

### ma...@gmail.com (2017-10-26)

a simple analyze & patch:
as andy write in https://chromium.googlesource.com/chromium/src.git/+/0ab2412a104d2f235d7b9fe19d30ef605a410832
"Inherit CSP when we inherit the security origin"
if the navigation happends in top frame, then the new page does not inherit the security origin
but when the navigation happends in iframe, then the element would inherit the security origin ,but forget to inhreit the CSP

as a matter of fact,this bug occurs because of when iframe location set to about:blank,when it navigate to about:blank again, it would not inhreit the CSP.

consider https://crbug.com/chromium/669086 and https://crbug.com/chromium/747847 so far

### ma...@gmail.com (2017-10-26)

the key point is in
third_party/WebKit/Source/core/dom/Document.cpp

      policy_to_inherit =
          inherit_from->GetSecurityContext()->GetContentSecurityPolicy();
      if (url_.IsEmpty() || url_.ProtocolIsAbout() || url_.ProtocolIsData() ||
          url_.ProtocolIs("blob") || url_.ProtocolIs("filesystem")) {
        GetContentSecurityPolicy()->CopyStateFrom(policy_to_inherit);
      }
    }
  }

after the check , CSP is not inhreit
inherit_from->GetSecurityContext()->GetContentSecurityPolicy(); may get a null result


### ma...@gmail.com (2017-10-26)

another possible reason is :
your code did not consider the following situation

when the top frame navigate from a.com to about:blank ,CSP did not need to inhreit because of the page did not inhreit origin.
but in iframe, it inhreit the origin (a.com) so that it need to consider CSP.
so you need to add check in plz navigate

### el...@chromium.org (2017-10-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### ma...@gmail.com (2017-10-30)

ping

### el...@chromium.org (2017-10-30)

Re #5: This issue will be triaged as a part of the normal Chrome security triage process. At first glance, it does not seem to be of particularly high severity.

### mb...@chromium.org (2017-10-30)

andypaicu: Would you mind taking a look?

### sh...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-09)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### an...@chromium.org (2017-11-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/209f225b2d51334eaf69ffdf002e25eaa1e0d448

commit 209f225b2d51334eaf69ffdf002e25eaa1e0d448
Author: Andy Paicu <andypaicu@chromium.org>
Date: Tue Nov 21 14:59:32 2017

Fixed bug where PlzNavigate CSP in a iframe did not get the inherited CSP

When inheriting the CSP from a parent document to a local-scheme CSP,
it does not always get propagated to the PlzNavigate CSP. This means
that PlzNavigate CSP checks (like `frame-src`) would be ran against
a blank policy instead of the proper inherited policy.

Bug: 778658
Change-Id: I61bb0d432e1cea52f199e855624cb7b3078f56a9
Reviewed-on: https://chromium-review.googlesource.com/765969
Commit-Queue: Andy Paicu <andypaicu@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#518245}
[add] https://crrev.com/209f225b2d51334eaf69ffdf002e25eaa1e0d448/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/generic/policy-inherited-correctly-by-plznavigate.html
[add] https://crrev.com/209f225b2d51334eaf69ffdf002e25eaa1e0d448/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/generic/policy-inherited-correctly-by-plznavigate.html.sub.headers
[add] https://crrev.com/209f225b2d51334eaf69ffdf002e25eaa1e0d448/third_party/WebKit/LayoutTests/external/wpt/content-security-policy/support/fail.html
[modify] https://crrev.com/209f225b2d51334eaf69ffdf002e25eaa1e0d448/third_party/WebKit/Source/core/dom/Document.cpp


### an...@chromium.org (2017-11-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

This bug requires manual review: M64 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-12-18)

Fix is already in 64.

### aw...@chromium.org (2018-01-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-22)

Thanks! $1,000 for this report from the VRP panel.

### aw...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/778658?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089414)*
