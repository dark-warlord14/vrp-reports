# [Resource Timing] Missing PerformanceResourceTiming entries for iframe Requests that don't receive a Response

| Field | Value |
|-------|-------|
| **Issue ID** | [40053435](https://issues.chromium.org/issues/40053435) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Loader, Blink>PerformanceAPIs |
| **Platforms** | Mac, Windows |
| **Reporter** | fa...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2020-09-24 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.53 Safari/537.36

Steps to reproduce the problem:
1. Load test.html
2. Observe that Broken never gets a performance entry

What is the expected behavior?
I expect all cases to generate a performance entry as it does in Firefox and IE (I'm not able to test Safari).

What went wrong?
The broken iframe does not have an entry.

Did this work before? No 

Does this work in other browsers? Yes

Chrome version: 86.0.4240.53  Channel: beta
OS Version: 10.0
Flash Version: 

This seems related to https://crbug.com/chromium/460879 but specifically for iframes. It doesn't seem like iframes were specifically excluded in https://github.com/w3c/resource-timing/issues/12.

## Attachments

- [test.html](attachments/test.html) (text/plain, 1.1 KB)

## Timeline

### jh...@chromium.org (2020-09-25)

[Empty comment from Monorail migration]

### sw...@chromium.org (2020-09-25)

Able to reproduce the issue on reported chrome #86.0.4240.53 using Windows 10 and Mac 10.15.6 by following steps as per https://crbug.com/chromium/1131929#c0.
NOTE: Issue is not seen on Ubuntu 16.04

Reproducible in:
------------------------
Canary: 87.0.4273.0
Dev: 87.0.4270.0
Beta: 86.0.4240.55	
stable: 85.0.4183.121

The behavior is seen from M-75. This is non regression issue hence marking it as untriaged and requesting some one from dev team to look into the issue. 
Thanks..

### td...@chromium.org (2020-10-15)

Over to npm@ for triage.

### np...@chromium.org (2020-10-15)

We do need an entry for a failed request, as it is a security problem to enable distinguishing between successful and failed fetches. From what I understand the iframe entries are created from Navigation Timing for the iframe:

DocumentLoader::BodyLoadingFinished
RemoteFrameOwner::AddResourceTiming
RenderFrameHostImpl::ForwardResourceTimingToParent

Obviously we don't need/have a NavigationTiming entry for an iframe that does not end up existing. But I imagine DocumentLoader will still exist for a failed iframe? Is it possible for loader folks to call the AddResourceTiming method on failure as well?

[Monorail components: Blink>HTML>IFrame Blink>Loader]

### np...@chromium.org (2020-10-15)

[Empty comment from Monorail migration]

### np...@chromium.org (2020-10-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-19)

[Empty comment from Monorail migration]

[Monorail components: -Blink>HTML>IFrame]

### np...@chromium.org (2020-10-22)

Ok, marking as available for now, look forward to thoughts from Blink Loader folks.

### to...@chromium.org (2020-10-23)

[Empty comment from Monorail migration]

### to...@chromium.org (2020-10-23)

[Empty comment from Monorail migration]

### oc...@google.com (2020-10-26)

Severity-Low as this gives the ability to distinguish between failed and successful fetches.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### yo...@chromium.org (2020-12-01)

The cause for this seems to be:
* The response that DocumentLoader gets for the error iframe is a chrome-error:// scheme, so not reported (we only report HTTP pages)
* Even if we were to report it, the response URL is the error URL, not the original request URL.

I'm taking a stab at fixing this. 

### yo...@chromium.org (2020-12-03)

https://chromium-review.googlesource.com/c/chromium/src/+/2567925 should fix the error case (still missing tests).
Might be interesting to also look at e.g. 204s to see if they are properly reported.

### yo...@chromium.org (2020-12-03)

[Empty comment from Monorail migration]

### yo...@chromium.org (2020-12-04)

[Empty comment from Monorail migration]

### ar...@chromium.org (2020-12-04)

The pending fix is:
https://chromium-review.googlesource.com/c/chromium/src/+/2567925
which make error documents to reveal informations to their parents, the same way normal documents does.

So to fix the cross-origin leak, we need to send more data toward the cross-origin parent? This sounds counter-intuitive at first, and potentially risky, since those are internal pages. We need to double check the cure is not worse than the disease.

I don't know anything about the PerformanceObserver, so I can't help much. What kind of new data will be sent to the parent?
I tried locally, this give something like this:
{
  connectEnd: 0
  connectStart: 0
  decodedBodySize: 0
  domainLookupEnd: 0
  domainLookupStart: 0
  duration: 23.164999904111028
  encodedBodySize: 0
  entryType: "resource"
  fetchStart: 13993.94499999471
  initiatorType: "iframe"
  length: 0
  name: "https://example.com/"
  nextHopProtocol: ""
  redirectEnd: 0
  redirectStart: 0
  requestStart: 0
  responseEnd: 14017.109999898821
  responseStart: 0
  secureConnectionStart: 0
  serverTiming: Array(0)
  startTime: 13993.94499999471
  transferSize: 0
  workerStart: 0
}

Maybe this will be okay. Could you please double check this won't be a problem?
To be worthwhile doing, the new data should be indistinguishable from non-error pages. Is it the case? Otherwise, we would end up with the original problem.

+CC nasko@ as FYI. Since this is about error pages, and you worked on isolating some of them.

### yo...@chromium.org (2020-12-07)

> So to fix the cross-origin leak, we need to send more data toward the cross-origin parent? 

Yes. As this information is exposed for iframes, not exposing it for some reveals information about them.

> We need to double check the cure is not worse than the disease.

Makes sense to be sure.

> What kind of new data will be sent to the parent?

We do report non-null startTime, fetchStart, responseEnd and duration, where startTime==fetchStart and duration == (responseEnd - fetchStart)

name is the pre-redirect, pre-error URL

> To be worthwhile doing, the new data should be indistinguishable from non-error pages. Is it the case?

I believe so, other than timing attacks. But the current values I see would make sense also for non-error pages. (i.e. they are not extremely low)

As the CL is now ready to land, let me know if y'all think it's safe to do.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eb493883a20b1e05a759c3006ee35a93d10ffa72

commit eb493883a20b1e05a759c3006ee35a93d10ffa72
Author: Yoav Weiss <yoavweiss@chromium.org>
Date: Tue Dec 08 12:40:16 2020

[resource-timing] ResourceTimingInfo for failed navigations

Failed navigations currently don't get a ResourceTiming entry.
This CL changes that by properly reporting them.

Bug: 1131929, 1105875
Change-Id: I0808f35e1b0d596c2bafa7630ed873c947254c5e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2567925
Commit-Queue: Yoav Weiss <yoavweiss@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#834675}

[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/public/web/web_security_policy.h
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/content/renderer/render_thread_impl.cc
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/renderer/core/exported/web_security_policy.cc
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/renderer/platform/weborigin/scheme_registry.h
[add] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/web_tests/external/wpt/resource-timing/iframe-failed-commit.html
[add] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/web_tests/external/wpt/resource-timing/resources/csp-default-none.html.headers
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/renderer/core/frame/remote_frame_owner.cc
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/renderer/platform/weborigin/scheme_registry.cc
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/public/web/web_navigation_params.h
[modify] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/renderer/core/loader/document_loader.h
[add] https://crrev.com/eb493883a20b1e05a759c3006ee35a93d10ffa72/third_party/blink/web_tests/external/wpt/resource-timing/resources/csp-default-none.html


### yo...@chromium.org (2020-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-08)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-17)

Congratulations! We deemed this to be a security bug and the VRP bug has deemed it is eligible for a reward of $1000 :) Someone from our finance team will be in touch. We'll also credit this to you in the Chrome release notes - how would you like to be credited?

### fa...@gmail.com (2020-12-17)

I appreciate the reward and the credit! My full name is fine for credit purposes, James Hartig.

The target version is 87? Will this bug be updated once it's released? 

### yo...@chromium.org (2020-12-17)

Right now it's targeted for 89. I'll attempt to merge back to 88. As Security Severity is low, I don't think this requires a stable re-spin for 87 (but y'all let me know if I'm wrong on that front)

### [Deleted User] (2020-12-17)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yo...@chromium.org (2020-12-17)

1. We are in phase 2, and this is a low severity non-regression security issue. As such I'm not sure it merits a merge back to 88.
2. https://chromium-review.googlesource.com/c/chromium/src/+/2567925
3. The change has landed in M88. I verified and tested it, but not sure if anyone else did.
4. I don't believe so
5. This is a security issue resulting in cross-site information leaks
6. No
7. N/A

### fa...@gmail.com (2020-12-17)

> Right now it's targeted for 89. I'll attempt to merge back to 88.

Thanks for the clarification. Makes sense I just misunderstood the labels.

### ad...@google.com (2020-12-17)

Hi Yoav & James, I agree with https://crbug.com/chromium/1131929#c28 that this doesn't merit a merge. It'll be released in M89.

### ad...@google.com (2020-12-17)

[Empty comment from Monorail migration]

### yo...@chromium.org (2021-01-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1131929?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Loader, Blink>PerformanceAPIs]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053435)*
