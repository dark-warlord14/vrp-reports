# Visited links leak via CSS transitions and the transitionrun event (Windows 10, Linux)

| Field | Value |
|-------|-------|
| **Issue ID** | [40055758](https://issues.chromium.org/issues/40055758) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Animation, Privacy>Fingerprinting |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gl...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2021-05-05 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

By applying a CSS transition to the color of visited links, JavaScript can detect if a transition runs, and thus infer if a link is visited. For the setup, a div contains a bunch of links to test. Then, 'a' and 'div.changer a' are the \*same\* color, and 'a:visited' is a \*different\* color. Also a CSS transition to 'a' elements are added.

With the setup, visited links will fire transition events ('transitionrun','transitionstart',etc.) whenever the changer class is toggled, but unvisited links will not. This requires no user interaction and such history sniffing is not visible to a user.

**VERSION**  

Chrome Version: 90.0.4430.93 (64-bit) stable  

Operating Systems:  

I tested it on both Operating Systems with the same version of Chrome  

\* Ubuntu 20.04.2 LTS  

\* Windows 10 Home 20H2: OS build: 19042.867 + Windows Feature Experience Pack 120.2212.551.0

**REPRODUCTION CASE**  

See attached .html file.

**CREDIT INFORMATION**  

Reporter credit: George Liu <https://gliu20.github.io>

## Attachments

- [silent-exploit.html](attachments/silent-exploit.html) (text/plain, 1.5 KB)
- [silent-exploit-no-rAF.html](attachments/silent-exploit-no-rAF.html) (text/plain, 1.5 KB)
- [screencapture.webm](attachments/screencapture.webm) (video/webm, 9.3 MB)
- [firefox-transition.html](attachments/firefox-transition.html) (text/plain, 312 B)

## Timeline

### [Deleted User] (2021-05-05)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-05-05)

Thanks for reporting this!

Normally, we don't treat privacy bugs as security bugs, as covered at https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#are-privacy-issues-considered-security-bugs . However, I note our severity guidance does mention reliably inferring browser history as being an exception, as covered at https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md . I may have mis-triaged this, though, so I'll work to confirm this is still the case :)

flackr@: I noticed you added the transition events in https://source.chromium.org/chromium/chromium/src/+/5b648ebafd7ce9b6780bd0c14b57de2524e7b15c , would you be a good first person to take a look at this? I've confirmed this repros on macOS, so I'm going ahead and assuming all platforms are affected. Note that this relies on rAF, so I had to tab switch to get rAF to trigger :)

[Monorail components: Blink>Animation Privacy>Fingerprinting]

### fl...@chromium.org (2021-05-05)

I added transitionrun, transitionstart, and transitioncancel however transitionend has been available for a long time and likely provides the same information (whether a transition ran).

As for how we should be protecting against this, the animations code for interpolating colors has a pair of values for the visited and non-visited color. We should always trigger a transition regardless of whether the used color value changes as long as either the visited or non-visited style changes. In this way the transition running provides no information as it would run for a visited or non-visited link.

Kevin, can you ensure that we always initiate a transition animations regardless of whether we are using the visited or non-visited values?

### gl...@gmail.com (2021-05-05)

Thank you so much! 
For requiring a tab switch due to rAF, I've tested it and it seems like changing the tick function to 
`const tick = () => new Promise((resolve) => setTimeout(resolve,100));` also works, but I don't have a Mac to verify if this is the case. The only purpose of the tick function is to give a pause so that the browser can do any style calculations if necessary to determine if a transition should occur.

I've attached this variant below.

Also, this is my first time reporting a bug, but maybe it is Pri-1 judging from https://crbug.com/381808 and https://crbug.com/835590 ? I'm not sure either though so some confirmation would be nice. 

If there's anything else you need please let me know I'll be happy to help! 

### da...@chromium.org (2021-05-05)

Nice find! In the short term, I agree we'll need an animation-specific fix. Though I think this is yet another data point in the sea of reasons why we ought to do https://github.com/w3c/csswg-drafts/issues/3012 or something along those lines.

### [Deleted User] (2021-05-06)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-06)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2021-05-11)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-05-11)

Following the existing patterns of "visited stuff has an effect paint time, but no effect through APIs", the correct behavior seems to be:

 - Interpolate visited and unvisited colors separately. This was impractical earlier, but now that visited colors are their own properties, it should be feasible.
 - Interpolations on the visited colors produce paint-time effects, but do not trigger events.

In other words, if _only_ visited colors changed, there should be no events at all.

### ke...@chromium.org (2021-05-11)

Investigating the issue... Triggering a transition on a style change regardless of whether the link was visited is not trivial to implement since the visited color is not updated in the computed style for links that have not been visited (not relevant for painting).  An alternate solution would be to suppress reporting of transition events on properties for an element inside of a link if the property is potentially affected by the visited state.  This fix simply requires resetting the event delegate for transitions that should not be visible in JS.  If we adopt this strategy, then we should also ensure that getAnimations does not report these transitions.


### fl...@chromium.org (2021-05-11)

We should ensure that we have consistency in wpt since such changes to animations / dispatched events will be developer visible.

Note that for animations, we should still fire events even if visited color is the only property being animated. This is because even animations with no properties still are spec'd to run and produce events. The firing of these events at the appropriate times also gives away nothing of the output state.

For transitions, I can see an argument that since transitions are only created if the property changes, then we could treat a visited-only property change as not having any transition from a developer-visible standpoint. This seems like something that should be explicitly called out in the spec, though we should also check what Firefox and Safari do to see if they have chosen the same or a different position.

### gl...@gmail.com (2021-05-11)

I'm not too familiar with C++, but from my limited knowledge, I'm pretty sure the Firefox source code appears to be using a function `GetVisitedDependentColor(&nsStyleText::mColor);` [1] which returns the normal link color regardless of visited state. 

The code that handles transition events uses that function so it never knows the true color of a link. I remember finding it in their source code, but I can't seem to find it right now. I'll update this if I can remember which file I was looking at.

[1] https://searchfox.org/mozilla-central/search?q=GetVisitedDependentColor&path=&case=false&regexp=false


### an...@chromium.org (2021-05-11)

>  Triggering a transition on a style change regardless of whether the link was visited is not trivial to implement since the visited color is not updated in the computed style for links that have not been visited (not relevant for painting).

(I should have mentioned this earlier during our chat): We don't store it on ComputedStyle for unvisited links *currently*, but I think it's only a performance optimization, and not necessarily an important one either (not sure). If we really want the "transition when either change" behavior, we can look into always storing it.

> Note that for animations, we should still fire events even if visited color is the only property being animated.

Hmm, is it possible to create a visited-dependent *animation* though?

> explicitly called out in the spec

Yes, that would be nice. AFAIK almost none of the current :visited behavior is really specified in detail. There's a high-level carte blanche in https://drafts.csswg.org/selectors-4/#link. And there are some nice MDN pages on the subject that serve as a de-facto spec for the style team. :-)

Overall it seems like the behavior we should aim for is to appear as if all links are permanently unvisited, as seen from JS. This is why I think the two colors should ideally be interpolated separately, where the visited interpolation is "silent". It may be too much work / not worth it, though, if there are simpler ways to plug the leak.

> which returns the normal link color regardless of visited state. 

Are you saying Firefox transitions (visually) as if the link is unvisited, even if it isn't? (I would just check myself, but getting late in my timezone ...)

### gl...@gmail.com (2021-05-11)

> Are you saying Firefox transitions (visually) as if the link is unvisited, even if it isn't? (I would just check myself, but getting late in my timezone ...)
Yep, that is correct. Except that once it's done transitioning, it seems to do another paint to correct for the visited/un-visited discrepancies. I've attached a video of this in case it helps, and I've compared it to Chrome in the attached screencapture. I also attached the file I used to create the video in case you want to try it on your machine.

The red color is for visited. The blue color is for on hover. The black color is for not visited links.

### gl...@gmail.com (2021-05-11)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-05-12)

gliu10000@: That's interesting. It's one way of plugging the leak I guess. :-)

Looks like Webkit (tested with Epihpany TP) has the same visual behavior as us: they transition from the visited color.

### gi...@appspot.gserviceaccount.com (2021-05-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ce84f05208f522fb8e0bf5a7e374abb5cd7435f1

commit ce84f05208f522fb8e0bf5a7e374abb5cd7435f1
Author: Kevin Ellis <kevers@chromium.org>
Date: Fri May 14 14:24:39 2021

Fix leaking of visited links via CSS transitions.

Bug: 1205981
Change-Id: I0c39e32dee8c71bbf4ab3792f3da29bd0b765575
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2889431
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Commit-Queue: Kevin Ellis <kevers@chromium.org>
Cr-Commit-Position: refs/heads/master@{#882965}

[modify] https://crrev.com/ce84f05208f522fb8e0bf5a7e374abb5cd7435f1/third_party/blink/renderer/core/animation/css/css_animations.cc
[modify] https://crrev.com/ce84f05208f522fb8e0bf5a7e374abb5cd7435f1/third_party/blink/renderer/core/css/element_rule_collector.cc
[modify] https://crrev.com/ce84f05208f522fb8e0bf5a7e374abb5cd7435f1/third_party/blink/renderer/core/css/element_rule_collector_test.cc
[add] https://crrev.com/ce84f05208f522fb8e0bf5a7e374abb5cd7435f1/third_party/blink/web_tests/animations/transition-visited.html


### ke...@chromium.org (2021-05-14)

Issue resolved.  If either the visited or unvisited style changes for a transition property we create a transition.  Visually, we apply the corresponding style, but it either case we report the unvisited style to JavaScript (via document.getAnimations() --> animation.effect.getKeyframes()). Using the sample code from the original comment,  a transitionrun event will be fired for each anchor element regardless of whether visited. That's Rob for the suggested approach to address the issue.



### [Deleted User] (2021-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-14)

[Empty comment from Monorail migration]

### gl...@gmail.com (2021-05-14)

Thank you so much and for the quick fix!

### [Deleted User] (2021-05-14)

Requesting merge to beta M91 because latest trunk commit (882965) appears to be after beta branch point (965).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-14)

This bug requires manual review: We are only 10 days from stable.
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
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2021-05-14)

Re https://crbug.com/chromium/1205981#c23:
1. Yes, this is a privacy fix.
2. https://chromium-review.googlesource.com/c/chromium/src/+/2889431
3. The change has landed on ToT
4. Unclear, M91 may be sufficient
5. Fixes a privacy exploit
6. Not a new feature
7 NA

### pb...@google.com (2021-05-15)

+Adetaylor(Security TPM) for Merge-decision

Note : The change has just landed on 92.0.4507.0 which went out couple of hours back.

### ad...@chromium.org (2021-05-17)

I'm inclined not to merge this to M91 at this late stage. As a medium severity bug, I think we can let this flow through beta to find out if any websites are disrupted by this change.

### am...@google.com (2021-05-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-05-20)

Congratulations, George! The VRP Panel has decided to award you $5000 for this report. Someone from our finance team will be in touch soon to arrange payment. Nice work! 

### gl...@gmail.com (2021-05-20)

Thank you so much for the reward! I really appreciate it! :)

### am...@google.com (2021-05-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### gi...@google.com (2021-08-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/17b41519ac9ed6eddb2771522dfdb604e2c36d0b

commit 17b41519ac9ed6eddb2771522dfdb604e2c36d0b
Author: Kevin Ellis <kevers@chromium.org>
Date: Thu Aug 05 13:25:28 2021

[M90-LTS] Fix leaking of visited links via CSS transitions.

(cherry picked from commit ce84f05208f522fb8e0bf5a7e374abb5cd7435f1)

Bug: 1205981
Change-Id: I0c39e32dee8c71bbf4ab3792f3da29bd0b765575
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2889431
Commit-Queue: Kevin Ellis <kevers@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#882965}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3066245
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1553}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/17b41519ac9ed6eddb2771522dfdb604e2c36d0b/third_party/blink/renderer/core/animation/css/css_animations.cc
[modify] https://crrev.com/17b41519ac9ed6eddb2771522dfdb604e2c36d0b/third_party/blink/renderer/core/css/element_rule_collector.cc
[modify] https://crrev.com/17b41519ac9ed6eddb2771522dfdb604e2c36d0b/third_party/blink/renderer/core/css/element_rule_collector_test.cc
[add] https://crrev.com/17b41519ac9ed6eddb2771522dfdb604e2c36d0b/third_party/blink/web_tests/animations/transition-visited.html


### rz...@google.com (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nd...@protonmail.com (2021-10-27)

Seems duplicate of https://bugs.chromium.org/p/chromium/issues/detail?id=713521 :/

### er...@microsoft.com (2021-10-28)

RE #39: That's the correct umbrella bug for this ~class~ of issue, yes, as noted in https://crbug.com/chromium/1205981#c5. This bug is a concrete ~instance~ of that class of bug.

### nd...@protonmail.com (2022-02-26)

"This bug is a concrete ~instance~ of that class of bug." Im not sure what you mean this bug can still be exploited easily without user interaction the browser history should never be exposed to a different website.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1205981?no_tracker_redirect=1

[Multiple monorail components: Blink>Animation, Privacy>Fingerprinting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055758)*
