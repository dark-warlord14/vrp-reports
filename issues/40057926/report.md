# Security: Scrolls are detectable cross-site upon using the Scroll to text fragment feature. 

| Field | Value |
|-------|-------|
| **Issue ID** | [40057926](https://issues.chromium.org/issues/40057926) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Scroll |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | te...@gmail.com |
| **Assignee** | bo...@chromium.org |
| **Created** | 2021-11-15 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

**-------------------------**

The browser behavior when a Scroll to text fragment match is found is to scroll to the part of the page containing the text match and highlight it.

What was discussed in the security docs about possible STTF attacks is a way to detect the scrolls to exfiltrate information via an attacker controlled iframe in the page or via network monitoring or lazy loaded image.

However, what i found allowed to detect a scroll without the need to partially have control over the targeted page. This is possible - the bug explanation next - because Scroll To Text Fragment feature is also possible inside an iframe, a malicious actor can embed a targeted page in a website in an iframe ( with a query for an STTF ), position that iframe in a way to be in the bottom of the attacker web page, then detect a scroll on the top page using onscroll EventListener.

The expected behavior here is that the scroll would happen inside the iframe only ,however , it also happens in the top window and the iframe ( or any levels below it if the STTF happened in an iframe inside the iframe ).

Linking this bug with the one here #1270469, this allowed to read cross-site files like authenticated javascript files and more.

Chrome Version: [ 95.0.4638.69] + [stable]  

Operating System: [Linux, Debian 8]

**REPRODUCTION CASE**

Below, i include a real proof of concept from a bug reported to Facebook, please keep this confidential. This poc demonstrates how STTF with a scroll detection would be used to extract information from pages that have XFO not set ( or frame-ancestors in csp).

Things to note in this poc ( please ignore the reset since they are specific to the target ):

- Iframe open a Facebook close\_popup
- close\_popup calls opener.location.replace with the current URL in Iframe but with a fragment #:~:text=SearchTerm
- Iframe location was changed due to a same-origin client-side redirect, STTF would work.
- The scroll happening in the top window, while the STTF match happened in the iframe.
- The scroll id detected with the onscroll eventlistener ( could be enhanced to ignore user manual scrolls )

<https://ysamm.com/ljezkjdlkezjdlkezjdez/fb_poc_sttf/bypass_iframe1.html>

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Youssef Sammouda

## Timeline

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-11-18)

nburris@ it looks like bokan@ is out and you are getting back soon enough, and nobody else owns scroll-to-text, so can you take a look when you get back?

[Monorail components: Blink>Scroll]

### [Deleted User] (2021-11-18)

[Empty comment from Monorail migration]

### mk...@google.com (2021-11-18)

Assigning to girard@ as per an internal thread.

### [Deleted User] (2021-11-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aa...@google.com (2021-11-19)

[Empty comment from Monorail migration]

### gi...@chromium.org (2021-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-30)

flackr: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fl...@chromium.org (2021-12-07)

Mehdi, could you look into this? The TLDR is that whether scroll to text succeeded in a subframe is observable to the root frame due to the main frame scrolling. We should either always scroll the subframe into view regardless of whether scroll to text succeeded, or only scroll the subframe without scrolling the main frame to bring the subframe into view. I think the latter - not scrolling the main frame - is better because this is consistent with scrolling element fragment anchors into view - e.g. https://jsbin.com/qoberuz/edit?html,css,js,output

### [Deleted User] (2021-12-14)

mehdika: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-24)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bo...@chromium.org (2021-12-30)

+1 to flackr@'s suggestion of just not scrolling the main frame in this case.

Curious though, how does the attacker manage to inject the search term into the iframe and the close_popup?

### bo...@chromium.org (2022-01-07)

mehdika@: Chatted with girard@ and flackr@ and it sounded like you had other things on your plate and hadn't started this yet so I think it'll take this one on. Hopefully you haven't taken a deep dive here yet.

### gi...@appspot.gserviceaccount.com (2022-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4ca8a782c0d417000ea8010c2f9b72c7f674920d

commit 4ca8a782c0d417000ea8010c2f9b72c7f674920d
Author: David Bokan <bokan@chromium.org>
Date: Wed Jan 12 15:26:22 2022

Refactor SafeToPropagateScrollToParent

This is a refactor CL, there is no intended behavior change.

SafeToPropagateScrollToParent is a bit on FrameView used to prevent
propagating a ScrollIntoView operation across origin boundaries. In most
cases, ScrollIntoView does propagate across these boundaries but we
prevent it for fragment scrolls. Hence, when scrolling to a fragment,
this bit is set on the first frame whose ancestor is cross-origin and
unset when the ScrollIntoView is completed. This was added in:
https://crrev.com/521ec7e

This is an awkward way to modify the behavior of ScrollIntoView since it
sets state on an external object and the caller must remember to unset
this state after the call. This CL replaces this mechanism with a
parameter in ScrollIntoViewParams which causes the origin check to
happen inside ScrollRectToVisible. Fragment scrolls use this parameter
to prevent crossing origin boundaries.

Note: The setting of the SafeToPropagateScrollToParent bit in
FrameLoader was redundant as the bit gets set again from
ElementFragmentAnchor.

Bug: 1270470
Change-Id: Id3aa57c7230ce737cd7f21cb2d8442cd093c3f2f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3378873
Reviewed-by: Robert Flack <flackr@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#958085}

[modify] https://crrev.com/4ca8a782c0d417000ea8010c2f9b72c7f674920d/third_party/blink/renderer/core/page/scrolling/fragment_anchor.cc
[modify] https://crrev.com/4ca8a782c0d417000ea8010c2f9b72c7f674920d/third_party/blink/renderer/core/layout/layout_box.cc
[modify] https://crrev.com/4ca8a782c0d417000ea8010c2f9b72c7f674920d/third_party/blink/renderer/core/dom/element.h
[modify] https://crrev.com/4ca8a782c0d417000ea8010c2f9b72c7f674920d/third_party/blink/renderer/core/scroll/scroll_alignment.h
[modify] https://crrev.com/4ca8a782c0d417000ea8010c2f9b72c7f674920d/third_party/blink/renderer/core/page/scrolling/element_fragment_anchor.cc
[modify] https://crrev.com/4ca8a782c0d417000ea8010c2f9b72c7f674920d/third_party/blink/renderer/core/frame/local_frame_view.h
[modify] https://crrev.com/4ca8a782c0d417000ea8010c2f9b72c7f674920d/third_party/blink/renderer/core/scroll/scroll_alignment.cc
[modify] https://crrev.com/4ca8a782c0d417000ea8010c2f9b72c7f674920d/third_party/blink/renderer/core/dom/element.cc
[modify] https://crrev.com/4ca8a782c0d417000ea8010c2f9b72c7f674920d/third_party/blink/renderer/core/frame/local_frame_view.cc
[modify] https://crrev.com/4ca8a782c0d417000ea8010c2f9b72c7f674920d/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/4ca8a782c0d417000ea8010c2f9b72c7f674920d/third_party/blink/public/mojom/scroll/scroll_into_view_params.mojom


### gi...@appspot.gserviceaccount.com (2022-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/83b205f6d15059268afd272b91742bd0c0fbcbab

commit 83b205f6d15059268afd272b91742bd0c0fbcbab
Author: David Bokan <bokan@chromium.org>
Date: Thu Jan 13 15:19:13 2022

Text Directive: Don't bubble scrolls across origin

Bug: 1270470
Change-Id: I29225d927b5c48f564adfbcf203dd7f36dc6c9e9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3377864
Reviewed-by: Robert Flack <flackr@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#958610}

[add] https://crrev.com/83b205f6d15059268afd272b91742bd0c0fbcbab/third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/iframe-scroll.sub.html
[add] https://crrev.com/83b205f6d15059268afd272b91742bd0c0fbcbab/third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/resources/self-text-directive-iframe.html
[modify] https://crrev.com/83b205f6d15059268afd272b91742bd0c0fbcbab/third_party/blink/renderer/core/fragment_directive/text_fragment_anchor.cc


### bo...@chromium.org (2022-01-13)

Security folks: as-is, the fix will go out in M99. Should we push for a merge to M98?

### te...@google.com (2022-01-13)

If it's not too much effort having it sooner in M98 sounds better because the impact can be quite severe. When is M98 release? 

### bo...@chromium.org (2022-01-13)

Planned stable cut is Jan 25 - release is Feb 1. Ok - I'll confirm the fix in the next canary (would appreciate others also give it a shake) and, assuming everything is ok, I'll request a merge.

### bo...@chromium.org (2022-01-18)

I've confirmed the fix in Windows 99.0.4838.0 using https://bokand.github.io/textfrag/iframe-xorigin.html#:~:text=dates%20to%202006.

Requesting merge to M98 for the CLs in #15 and #16

### [Deleted User] (2022-01-18)

Merge review required: M98 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bo...@chromium.org (2022-01-18)

1. Why does your merge fit within the merge criteria for these milestones?
This is a security issue

2. What changes specifically would you like to merge? Please link to Gerrit.
The CLs from comments #15 and #16
https://chromium-review.googlesource.com/c/chromium/src/+/3378873
https://chromium-review.googlesource.com/c/chromium/src/+/3377864

3. Have the changes been released and tested on canary?
Yes - since 99.0.4829.0

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
N/A

### am...@chromium.org (2022-01-21)

hello bokan@, thanks for fixing this issue. In the future, please go ahead and update status to fixed on security bugs, once the resolving CLs are landed. This will allow the bot to make the correct decisions and labeling, and you don't need to manually request merges. :) 

### am...@chromium.org (2022-01-21)

merge of both CLs approved for M98, please go ahead and merge to branch 4758 before 11am PST, Tuesday, 25 January -- thank you! 

### go...@chromium.org (2022-01-21)

Please merge your change to M98 branch 4758 ASAP. Thank you. 

### [Deleted User] (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

[Empty comment from Monorail migration]

### go...@chromium.org (2022-01-24)

Please merge your change to M98 branch 4758 ASAP so we can take it in for M98 Stable RC cut. RC cut tomorrow, Tuesday noon PT. Thank you. 

### gi...@appspot.gserviceaccount.com (2022-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/908c81facdeca04307499e6539f13aac07375d31

commit 908c81facdeca04307499e6539f13aac07375d31
Author: David Bokan <bokan@chromium.org>
Date: Tue Jan 25 00:44:13 2022

Refactor SafeToPropagateScrollToParent

This is a refactor CL, there is no intended behavior change.

SafeToPropagateScrollToParent is a bit on FrameView used to prevent
propagating a ScrollIntoView operation across origin boundaries. In most
cases, ScrollIntoView does propagate across these boundaries but we
prevent it for fragment scrolls. Hence, when scrolling to a fragment,
this bit is set on the first frame whose ancestor is cross-origin and
unset when the ScrollIntoView is completed. This was added in:
https://crrev.com/521ec7e

This is an awkward way to modify the behavior of ScrollIntoView since it
sets state on an external object and the caller must remember to unset
this state after the call. This CL replaces this mechanism with a
parameter in ScrollIntoViewParams which causes the origin check to
happen inside ScrollRectToVisible. Fragment scrolls use this parameter
to prevent crossing origin boundaries.

Note: The setting of the SafeToPropagateScrollToParent bit in
FrameLoader was redundant as the bit gets set again from
ElementFragmentAnchor.

(cherry picked from commit 4ca8a782c0d417000ea8010c2f9b72c7f674920d)

Bug: 1270470
Change-Id: Id3aa57c7230ce737cd7f21cb2d8442cd093c3f2f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3378873
Reviewed-by: Robert Flack <flackr@chromium.org>
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#958085}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3412706
Cr-Commit-Position: refs/branch-heads/4758@{#880}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/908c81facdeca04307499e6539f13aac07375d31/third_party/blink/renderer/core/page/scrolling/fragment_anchor.cc
[modify] https://crrev.com/908c81facdeca04307499e6539f13aac07375d31/third_party/blink/renderer/core/layout/layout_box.cc
[modify] https://crrev.com/908c81facdeca04307499e6539f13aac07375d31/third_party/blink/renderer/core/dom/element.h
[modify] https://crrev.com/908c81facdeca04307499e6539f13aac07375d31/third_party/blink/renderer/core/scroll/scroll_alignment.h
[modify] https://crrev.com/908c81facdeca04307499e6539f13aac07375d31/third_party/blink/renderer/core/page/scrolling/element_fragment_anchor.cc
[modify] https://crrev.com/908c81facdeca04307499e6539f13aac07375d31/third_party/blink/renderer/core/frame/local_frame_view.h
[modify] https://crrev.com/908c81facdeca04307499e6539f13aac07375d31/third_party/blink/renderer/core/scroll/scroll_alignment.cc
[modify] https://crrev.com/908c81facdeca04307499e6539f13aac07375d31/third_party/blink/renderer/core/dom/element.cc
[modify] https://crrev.com/908c81facdeca04307499e6539f13aac07375d31/third_party/blink/renderer/core/frame/local_frame_view.cc
[modify] https://crrev.com/908c81facdeca04307499e6539f13aac07375d31/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/908c81facdeca04307499e6539f13aac07375d31/third_party/blink/public/mojom/scroll/scroll_into_view_params.mojom


### [Deleted User] (2022-01-25)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f375e3ed7bae261e7bd1c7f4c91a535d8eea2010

commit f375e3ed7bae261e7bd1c7f4c91a535d8eea2010
Author: David Bokan <bokan@chromium.org>
Date: Tue Jan 25 04:07:57 2022

Text Directive: Don't bubble scrolls across origin

(cherry picked from commit 41aa6b50bf65bb2a6d246ce97e8f5f0af4bff863)

Bug: 1270470
Change-Id: I29225d927b5c48f564adfbcf203dd7f36dc6c9e9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3377864
Reviewed-by: Robert Flack <flackr@chromium.org>
Commit-Queue: David Bokan <bokan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#958610}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3413393
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4758@{#889}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[add] https://crrev.com/f375e3ed7bae261e7bd1c7f4c91a535d8eea2010/third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/iframe-scroll.sub.html
[add] https://crrev.com/f375e3ed7bae261e7bd1c7f4c91a535d8eea2010/third_party/blink/web_tests/external/wpt/scroll-to-text-fragment/resources/self-text-directive-iframe.html
[modify] https://crrev.com/f375e3ed7bae261e7bd1c7f4c91a535d8eea2010/third_party/blink/renderer/core/fragment_directive/text_fragment_anchor.cc


### bo...@chromium.org (2022-01-25)

> 1. Was this issue a regression for the milestone it was found in?
No

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?
No

The issue exists in M96 so a merge back there makes sense.


### bo...@chromium.org (2022-01-25)

Just a heads up that there are two CLs to merge here: #15 and #16

### am...@chromium.org (2022-01-26)

yes, both CL were approved for merge to M98 back in https://crbug.com/chromium/1270470#c24 on Friday, please merge commit 83b205f6d15059268afd272b91742bd0c0fbcbab to M98, branch 4758 ASAP/ NLT 10am PST tomorrow, Wednesday, 26 January so this fix can be included in the M98 stable cut tomorrow for stable release next week - thank you!

### am...@chromium.org (2022-01-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-26)

adding merge approval label for attention for second CL to be merged for by stable cut deadline tomorrow 

### bo...@chromium.org (2022-01-26)

Sorry, my comments in #32 and #33 were in response to the automated questionnaire in #30 about merging these changes to M96 LTS.

The fixes are already landed in M98 branch 4758 (#29 and #31)

### sr...@google.com (2022-01-26)

Dropping the merge approved label as the merges are complete. 

### am...@google.com (2022-01-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-28)

Congratulations, Youssef! The VRP Panel has decided to award you $2,000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for your efforts and nice work! 

### am...@google.com (2022-01-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### vo...@google.com (2022-02-02)

[Empty comment from Monorail migration]

### gm...@google.com (2022-02-22)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vo...@google.com (2022-02-22)

1. https://crrev.com/c/3378873, https://crrev.com/c/3377864 and to resolve merge conflicts at least https://crrev.com/c/3172857 and https://crrev.com/c/3270655
2. High - big amount of changes and conflicts
3. Yes M98
4. No

### gm...@google.com (2022-03-04)

I have got no reply about impact of not merging this into LTS. I will follow the TVCs advice in the previous comment and reject the merge for now. We can reevaluate for next release.

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-11)

Finance has informed us the the VRP reward for this issue has gone unclaimed, so we will be processing this $2,000 reward for a $4,000 donation to a charitable organization of our choosing is we do not receive any response. Setting a next action date of for donating the reward for this issue. 

### te...@gmail.com (2023-04-12)

Hello,

Sorry for the late reply. It seems this report was long forgotten by me.
Could you please assign this bounty to another email address which is
already registered with Embark.

Best Regards
Youssef

### am...@chromium.org (2023-04-12)

Hi Youssef, thanks for the response. Please reach out to the finance team at p2p-vrp@google.com so that they can reprocess this issue against the preferred email address and provide them the email address associated with the enrollment. 


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1270470?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057926)*
