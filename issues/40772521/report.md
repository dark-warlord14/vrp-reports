# Security: Use-after-free in NavigatorShare::OnConnectionError

| Field | Value |
|-------|-------|
| **Issue ID** | [40772521](https://issues.chromium.org/issues/40772521) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebShare |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | er...@chromium.org |
| **Created** | 2021-06-15 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webshare/navigator_share.cc;drc=71003be7ce59254518062bb7fa11ba4dc5106f0b;l=321>

```
void NavigatorShare::OnConnectionError() {  
  for (auto& client : clients_) {  
    client->OnConnectionError();  
  }  
  clients_.clear();  
  service_remote_.reset();  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webshare/navigator_share.cc;drc=b6d364a7c841ce51a9bc2d2a32a84ce5787e63eb;l=170>

```
void NavigatorShare::ShareClientImpl::OnConnectionError() {  
  resolver_->Reject(MakeGarbageCollected<DOMException>(  
      DOMExceptionCode::kAbortError,  
      "Internal error: could not connect to Web Share interface."));  
}  

```

`NavigatorShare::ShareClientImpl::OnConnectionError` calls `Reject`, which can synchronously run a user-defined JavaScript  

function. If the function calls `NavigatorShare::share`, it will modify the `clients_` hash  

set and invalidate the iterator used in the range-based for loop. The invalidated iterator will  

cause a use-after-free condition in the next iteration of the loop.

**VERSION**

Chromium 93.0.4542.2 (Developer Build)

## Timeline

### [Deleted User] (2021-06-15)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-06-15)

Hi, can you provide a PoC? Still, this looks likely to be a bug, and maybe it just needs a ScriptForbiddenScope. Assigning OWNERS here.

[Monorail components: Blink>WebShare]

### [Deleted User] (2021-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-15)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b11d329df72b61188f8d7d35a7b7fcbf3421b899

commit b11d329df72b61188f8d7d35a7b7fcbf3421b899
Author: Eric Willigers <ericwilligers@chromium.org>
Date: Wed Jun 16 06:30:24 2021

Web Share: Swap before iterating

We move the set clients_ to a local variable, before
iterating over the elements.

Bug: 1219870
Change-Id: I7ea94c53d6d3df5dbfc67abaa36f16b1eb9a1369
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2963936
Auto-Submit: Eric Willigers <ericwilligers@chromium.org>
Reviewed-by: Alexey Baskakov <loyso@chromium.org>
Commit-Queue: Eric Willigers <ericwilligers@chromium.org>
Cr-Commit-Position: refs/heads/master@{#892895}

[modify] https://crrev.com/b11d329df72b61188f8d7d35a7b7fcbf3421b899/third_party/blink/renderer/modules/webshare/navigator_share.cc


### [Deleted User] (2021-06-29)

ericwilligers: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### er...@chromium.org (2021-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-30)

Requesting merge to stable M91 because latest trunk commit (892895) appears to be after stable branch point (870763).

Requesting merge to beta M92 because latest trunk commit (892895) appears to be after beta branch point (885287).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-30)

This bug requires manual review: M92's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### er...@chromium.org (2021-07-01)

1.  Yes.  Web Share is covered by tests. 
chrome/browser/webshare/share_service_browsertest.cc
third_party/blink/web_tests/external/wpt/web-share/

The change has been in Canary for some time.

The merge is safe.


2. CL:  https://chromium-review.googlesource.com/c/chromium/src/+/2963936

3. Yes

4. Only 92.

5. The bug was found after branchpoint.

6. No

7. N/A

8. N/A
 

### sr...@google.com (2021-07-01)

Merge approved for M92 branch:4515 please merge asap

### sr...@google.com (2021-07-01)

Please complete your merges before 12pm PST friday as we head out to long weekend and lot of you might be OOO next week (no meetings week)., We are planning a beta release next thursday so we get critical beta coverage on some of the fixes before the Stable RC cut, so please help land your fixes asap. 

### er...@chromium.org (2021-07-01)

No merged needed. Abandoning https://chromium-review.googlesource.com/c/chromium/src/+/3001085

#811265 unknowingly fixed the bug.
M91 #870763 is not affected by the bug.
M92 #885287 is not affected by the bug.
#886962 reintroduced the bug.
#892895 fixed the bug.
M93 will not be affected by the bug.


### [Deleted User] (2021-07-03)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-07-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-22)

Congratulations! The VRP Panel has decided to award you $7,500 for this report! Nice find and thank you for this report!

### am...@google.com (2021-07-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### ja...@google.com (2021-09-08)

M90 #857950 is not affected by this bug. 

### [Deleted User] (2021-10-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wx...@gmail.com (2021-10-08)

Does this bug have any poc? Because the "reject" function  seems can't execute user-defined js  like "resolve". And the reject object can't be controlled by user.

### wx...@gmail.com (2021-10-08)

Seems a fake bug?

### am...@chromium.org (2022-02-07)

Despite that this was rewarded and provided a CVE, after later review, it was determined this issue was erroneously labeled/handled as a security bug, as it has been determined and confirmed that it's not possible to synchronously trigger user JavaScript execution from inside Reject(). If a POC can be submitted to disprove this assertion in this and/or other reports and demonstrate exploitability, we would welcome that information as well as reassess this and other similar reports. 
Updating type to reflect this update. 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1219870?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40772521)*
