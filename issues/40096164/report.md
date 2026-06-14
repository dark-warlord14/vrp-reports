# Security: Possible to spoof URL through use of document.open

| Field | Value |
|-------|-------|
| **Issue ID** | [40096164](https://issues.chromium.org/issues/40096164) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2019-09-02 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

When a browser-initiated navigation is pending, a page can override it with something like location.reload, at least in the case where the page has user activation. If a page with user activation calls location.reload followed by document.open, any pending navigation will be cancelled, but the pending URL will be left in place.

**VERSION**  

Chrome Version: Tested on 76.0.3809.132 (stable) and 78.0.3899.0 (canary)  

Operating System: Windows 10 Pro, version 1903

**REPRODUCTION CASE**

1. Download index.html into a directory, then run the following command:

python3 -m http.server 8080

2. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

This page defines the following beforeunload handler:

setTimeout(() => {  

if (navigator.userActivation.isActive) {  

location.reload();  

document.open();  

}  

}, 0);

If you attempt to navigate away from the page, the initial location.reload call will override the navigation, at least when the page has user activation. The document.open call will then cancel that navigation and result in no navigation taking place at all. The pending URL will be left in place, however.

A way to test this is to click the page (therefore granting it user activation), then click a bookmark before the transient activation has expired. That is, within 5 seconds:

<https://cs.chromium.org/chromium/src/third_party/blink/common/frame/user_activation_state.cc?l=12&rcl=621a8ac1db055db57428fb350b390970ee9dd922>

This should result in the omnibox being updated, but no navigation taking place.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [index.html](attachments/index.html) (text/plain, 533 B)

## Timeline

### ct...@chromium.org (2019-09-03)

Thanks for the report!

arthursonzogni@ can you take a look? My feeling is that this may have the same root cause as https://crbug.com/chromium/998284.

Also cc'ing creis@ for navigation and mustaq@ for user activation.

[Monorail components: UI>Browser>Navigation]

### ar...@chromium.org (2019-09-05)

Yes, this look like a duplicate. It just uses another set of method to trigger / cancel navigations.
However, the fix I am proposing for https://crbug.com/chromium/998284 won't fix this issue. This issue is not the NavigationController has forgot to invalidate the URL after discarding the pending NavigationEntry. It is the pending NavigationEntry that is not discarded at all.

The location.reload() cancels the first navigation, because only one non-comitting navigation can happen at a time.
~~~
#4 0x7f699a1023cc content::NavigationRequest::~NavigationRequest()
#5 0x7f699a0bd3df std::__Cr::default_delete<>::operator()()
#6 0x7f699a0b82af std::__Cr::unique_ptr<>::reset()
#7 0x7f699a0b6899 content::FrameTreeNode::ResetNavigationRequest()
#8 0x7f699a0b66a1 content::FrameTreeNode::CreatedNavigationRequest()
#9 0x7f699a135fb7 content::NavigatorImpl::OnBeginNavigation()
~~~

Then the second navigation is canceled by window.open:
~~~
#4 0x7f699a1023cc content::NavigationRequest::~NavigationRequest()
#5 0x7f699a0bd3df std::__Cr::default_delete<>::operator()()
#6 0x7f699a0b82af std::__Cr::unique_ptr<>::reset()
#7 0x7f699a0b6899 content::FrameTreeNode::ResetNavigationRequest()
#8 0x7f699a1367ca content::NavigatorImpl::CancelNavigation()
#9 0x7f699a1078c6 content::NavigationRequest::OnRendererAbortedNavigation()
~~~

But we never discard the pending NavigationEntry of the first navigation.
Do you have any ideas how to fix this?

### cr...@chromium.org (2019-09-05)

It sounds like there are several related issues here-- see also ahemery@'s https://chromium-review.googlesource.com/c/chromium/src/+/1751205 for https://crbug.com/chromium/966914.

clamy@, what are your thoughts on when the pending entries should be discarded after the NavigationRequest refactorings to NavigationController?

### ah...@chromium.org (2019-09-05)

This look indeed like the bug I'm trying to fix. In my case it is canceled because the URL is invalid (chrome://1234 or something like that), but the behavior is similar. This is just coming fundamentally from the fact that NavigationRequests and pending NavigationEntrys have decoupled lifetimes. The CL that creis@ linked should fix this, but long term solution might involve something like what clamy@ did in https://chromium-review.googlesource.com/c/chromium/src/+/1333759

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-20)

arthursonzogni: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ah...@chromium.org (2019-09-20)

Still reproduces on ToT with my patch, so probably hitting the same issue from a different path.

### ar...@chromium.org (2019-09-20)

I am a bit tired of playing cat & mouse with URL spoof ;-)

Here is the plan for fixing URL spoof (once and for all)

1) I made a patch to systematically notify content/ embedders when a pending NavigationEntry is discarded:
https://chromium-review.googlesource.com/c/chromium/src/+/1781434

2) Now, I would like to systematically discard pending NavigationEntry when the matching NavigationRequest is deleted:
https://chromium-review.googlesource.com/c/chromium/src/+/1781434

In theory, it should fix every (or most of) the URL spoof we have now and in the future, as long as we properly delete the NavigationRequest.

I'm not sure what it's worth.
I don't know what my patch in (2) is worth. It will probably don't pass the trybot on its first try. I will iterate on it.

### ar...@chromium.org (2019-09-23)

Sorry wrong link for (2). The good one is:
https://chromium-review.googlesource.com/c/chromium/src/+/1815129

I also found a bug I need to fix before going further:
https://chromium-review.googlesource.com/c/chromium/src/+/1818522

### cr...@chromium.org (2019-09-24)

Thanks again for the report!  I'm reviewing the prereq CL in https://crbug.com/chromium/999932#c9.  I'd caution that the proposal in https://crbug.com/chromium/999932#c8 isn't a panacea-- I agree it should help with one class of URL spoof (where stale pending entries are shown), but not every type of URL spoof (e.g., renderers can get navigations classified as browser-initiated, etc).  Still, I think it's certainly worth pursuing, and it's a shorter term option than removing pending entries entirely in favor of NavigationRequests (as I think clamy@ was aiming for).

I'm also taking another look at the severity rating on this.  It sounds like the attacker does not have control over what URL is shown during the spoof, and that it depends on where the user tries to navigate.  That matches the "An address bar spoof where only certain URLs can be displayed, or with other mitigating factors" description for Medium severity.  Feel free to mention if there's a way for the attacker to control the visible URL, though.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2ef18ffc2f82e6f9d2d577cd00de8b30ad62d929

commit 2ef18ffc2f82e6f9d2d577cd00de8b30ad62d929
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Wed Sep 25 09:36:54 2019

Fix wrong NavigationRequest / pending NavigationEntry association.

When a new renderer initiated navigations starts it will either:
 1) Create a new pending navigation entry and use it.
 2) Reuse the existing pending navigation entry.

The problem is that (2) is very wrong. There is no reasons to do it.

For instance, when a main frame navigation starts, it creates a pending
NavigationEntry. Then if a subframe navigation starts, is reuses the
same pending NavigationEntry. This doesn't make sense.

Bug: 999932
Change-Id: I53152ab7b62bdf9bcf745b7512f3b1110d0b5e2c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1818522
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#699678}

[modify] https://crrev.com/2ef18ffc2f82e6f9d2d577cd00de8b30ad62d929/content/browser/frame_host/navigation_controller_impl_unittest.cc
[modify] https://crrev.com/2ef18ffc2f82e6f9d2d577cd00de8b30ad62d929/content/browser/frame_host/navigator_impl.cc
[modify] https://crrev.com/2ef18ffc2f82e6f9d2d577cd00de8b30ad62d929/content/browser/frame_host/navigator_impl.h


### sh...@chromium.org (2019-10-08)

arthursonzogni: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/66f711cb897066d58153f73b1e9b80366123c00e

commit 66f711cb897066d58153f73b1e9b80366123c00e
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Tue Oct 08 14:40:36 2019

Clear matching pending NavigationEntry on NavigationRequest deletion.

The goal is to fix a big class of URL spoof issues. They happen when
a NavigationRequest is canceled, but the associated pending navigation
entry remains. This causes the wrong URL to be displayed in the
omnibox.

To fix it, delete the matching pending NavigationEntry in the
NavigationRequest's destructor.

This is a bit more complex:
1) During an history navigation, several NavigationRequest can starts
   at the same time for iframes. All of them are associated with the
   same pending NavigationEntry.
2) A pending NavigationEntry can be used, discarded and reused. It can
   is used twice, but not associated with the same NavigationRequest(s)
   on every use.
The class PendingEntryRef is used to track one NavigationRequest being
associated with a pending NavigationEntry for a given history
navigation.

Bug: 999932
Change-Id: I14582fd1d954a6f831959db0bb5d96eb1f5d53b5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1815129
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#703713}

[modify] https://crrev.com/66f711cb897066d58153f73b1e9b80366123c00e/content/browser/frame_host/frame_tree_node.cc
[modify] https://crrev.com/66f711cb897066d58153f73b1e9b80366123c00e/content/browser/frame_host/navigation_controller_delegate.h
[modify] https://crrev.com/66f711cb897066d58153f73b1e9b80366123c00e/content/browser/frame_host/navigation_controller_impl.cc
[modify] https://crrev.com/66f711cb897066d58153f73b1e9b80366123c00e/content/browser/frame_host/navigation_controller_impl.h
[modify] https://crrev.com/66f711cb897066d58153f73b1e9b80366123c00e/content/browser/frame_host/navigation_request.cc
[modify] https://crrev.com/66f711cb897066d58153f73b1e9b80366123c00e/content/browser/frame_host/navigation_request.h
[modify] https://crrev.com/66f711cb897066d58153f73b1e9b80366123c00e/content/browser/frame_host/navigator_delegate.cc
[modify] https://crrev.com/66f711cb897066d58153f73b1e9b80366123c00e/content/browser/frame_host/navigator_delegate.h
[modify] https://crrev.com/66f711cb897066d58153f73b1e9b80366123c00e/content/browser/frame_host/navigator_impl.cc
[modify] https://crrev.com/66f711cb897066d58153f73b1e9b80366123c00e/content/browser/frame_host/navigator_impl.h
[modify] https://crrev.com/66f711cb897066d58153f73b1e9b80366123c00e/content/browser/navigation_browsertest.cc
[modify] https://crrev.com/66f711cb897066d58153f73b1e9b80366123c00e/content/browser/web_contents/web_contents_impl.h


### ar...@chromium.org (2019-10-08)

Fix landed \o/

M78 stable cut is in 7 days (October 15th). The patch fixing the issue is not trivial and I am worried we don't have enough time to prove it to be stable enough before going to stable.

Do you think we need to merge this into M78? or we can wait the M79 stable release in 60 days?

+govind@ FYI.

### go...@chromium.org (2019-10-08)

As this is "Security_Severity-Medium" and patch is not trivial, I'm leaning towards waiting for M79 but would like to take +adetaylor@ (Security TPM) input here. Thank you.

Note: M78 Stable cut is on Oct 15th, Stable release on Oct 22nd.

+srinivassista@ as FYI

### ad...@chromium.org (2019-10-08)

I'm OK with waiting till M79 as it's complex.

### ke...@chromium.org (2019-10-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-15)

Requesting merge to beta M78 because latest trunk commit (703713) appears to be after beta branch point (693954).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-15)

This bug requires manual review: We are only 6 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-10-15)

Rejecting the merge per https://crbug.com/chromium/999932#c16. Lets wait until M79

### na...@google.com (2019-10-23)

creis - can you give more information re: the  impact of this vulnerability for the VRP Panel to assess this report

### cr...@chromium.org (2019-10-28)

https://crbug.com/chromium/999932#c23: Sure.  (Sorry for the delay; I'm currently OOO for jury duty.)  https://crbug.com/chromium/999932#c10 sums up the medium severity rating, but I can elaborate a bit.

This bug makes it possible for an attacker's page to cancel a browser-initiated navigation and leave the URL in the address bar, while no navigation is in progress anymore.  That's definitely a URL spoof, and the attacker's page can change its appearance to try to pretend to be the URL in the address bar.

However, there are a few mitigating factors.  The most important is that the attacker's page does not have control over, or knowledge of, the URL of the browser-initiated navigation.  It would have to guess what the user typed in or navigated to and then attempt to spoof the result.  That's a limited URL spoof, since the attacker can't use it to spoof a victim URL of their choice.  Also, I don't think it would show the padlock for HTTPS URLs, though that's not a super effective way of drawing attention to the fact the URL hasn't committed.

Hope that helps!

### na...@google.com (2019-11-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-07)

Congrats! The Panel decided to reward $500 for this report. 

### na...@google.com (2019-11-07)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2020-01-17)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/999932?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1010567]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096164)*
