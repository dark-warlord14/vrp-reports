# Security: It is possible to lock the pointer while window is not focused.

| Field | Value |
|-------|-------|
| **Issue ID** | [40057858](https://issues.chromium.org/issues/40057858) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Input>PointerLock |
| **Platforms** | Mac |
| **Reporter** | je...@gmail.com |
| **Assignee** | mu...@chromium.org |
| **Created** | 2021-11-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to lock the pointer when the window is not focused, this prevents users from unlocking the pointer using the escape key.

**VERSION**  

Chrome Version: 98.0.4694.0 (canary) and 95.0.4638.69 (stable)  

Operating System: macOS 11.6 (20G165)

**REPRODUCTION CASE**  

Please see lockPointerChangeFocus.html for a demonstration. Inside the file are additional comments on how the bug works.  

I have also attached a screenrecording demonstrating the problem.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Jesper van den Ende (Pelican Party Studios)

## Attachments

- [Screen Recording 2021-11-08 at 13.16.23.mp4.mp4](attachments/Screen Recording 2021-11-08 at 13.16.23.mp4.mp4) (video/mp4, 541.1 KB)
- [lockPointerChangeFocus.html](attachments/lockPointerChangeFocus.html) (text/plain, 2.3 KB)

## Timeline

### [Deleted User] (2021-11-08)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-11-08)

yoavweiss@ -- can you please help find a good owner for this issue? Thanks.

### va...@chromium.org (2021-11-08)

Setting Security_Severity-Medium based on some of the other bugs in this area.

### va...@chromium.org (2021-11-08)

[Comment Deleted]

### va...@chromium.org (2021-11-08)

I'm unable to reproduce this on r920001 (95.0.4638.0) on Linux.

### va...@chromium.org (2021-11-08)

I'm unable to reproduce this on r929491 (96.0.4664.0) on Linux.


### je...@gmail.com (2021-11-08)

I'm also not able to reproduce on Windows 10. I think this is a macOS only issue.

### yo...@chromium.org (2021-11-09)

avi@ - can you find an owner for this macOS issue?

### av...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

### lg...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lg...@chromium.org (2021-11-09)

Per the Pointer Lock spec (https://www.w3.org/TR/pointerlock-2/#requirements), "Pointer lock must be exited if the target becomes disconnected, or the user agent, window, or tab loses focus."

Switching tabs or windows while pointer lock is already active works as expected. But in this example, since the request is in flight during the switch, we *should* exit here:

https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_widget_host_impl.cc;l=2937?q=f:render_widget_host_impl.cc&ss=chromium

  if (!view_ || !view_->HasFocus()) {
    std::move(response).Run(blink::mojom::PointerLockResult::kWrongDocument);
    return;
  }

RenderWidgetHostViewMac::HasFocus() returns true iff we're first responder which is technically true, but doesn't match the intent of the above call or RenderWidgetHostViewAura (which delegates to aura::Window::HasFocus). Changing it to return true iff we're first responder *and* the window is key fixes this and seems generally correct from a platform consistency standpoint. But does it break other stuff? If it does break other stuff, will we ever find out from the trybots, given that focus-related tests are the flakiest? For that matter, does it fix other stuff? Let's find out I guess.

### lg...@chromium.org (2021-11-10)

Here's a run: https://chromium-review.googlesource.com/c/chromium/src/+/3270656

Not *too* many failures. Will repro locally. If we're in luck, the tests are just not making the window key and there's no actual non-test problem. If that isn't the case, I think we'll need to add an IsActive() method to RenderWidgetHostView and check for both focus and active when locking.

### lg...@chromium.org (2021-11-11)

"the tests are just not making the window key"

This is the case AFAICT, but I couldn't find an easy way to fix it (especially with asynchronous window activation).

Trying out some alternatives. 

### ad...@google.com (2021-11-11)

lgrey@ thanks for working on fixing this. I assume you have successfully reproduced this? Do you know the earliest affected release branch of Chrome? (94, 95, 96, 97 or 98?) The reporter says they reproduced it on M98 but we need to know if earlier branches are affected. Please could you label this with FoundIn-nn for the earliest affected such branch? That will allow sheriffbot to later request merges to all the correct branches, and will result in us adding credits in release notes, allocating CVEs etc. as appropriate too. Thanks!

### lg...@chromium.org (2021-11-11)

I would suspect it goes back to M69 when we switched to MacViews, if not earlier. I can check later when I have some time, but if anyone else wants to beat me to it, the repro steps in the report are straightforward and repro every time.

### lg...@chromium.org (2021-11-11)

Better: https://ci.chromium.org/ui/p/chromium/builders/try/mac-rel/839692/overview

Just a bunch of pointer lock tests broken, which isn't very unexpected

### lg...@chromium.org (2021-11-11)

1) There are real pointer lock failures lurking under the spurious ones: active status isn't propagated to child frames
2) There's a test called PointerLockOutOfFocus in there but it's ifdeffed USE_AURA :( On the bright side it still wouldn't have caused this.

Back to trying to figure out how to fix tests with the c#13 approach.

### lg...@chromium.org (2021-11-11)

s/caused this/caught this

### je...@gmail.com (2021-11-11)

I was able reproduce this in as far back as 63.0.3239.0
Anything before that and the tab crashes when trying to open the html file

### lg...@chromium.org (2021-11-11)

Thanks!

### [Deleted User] (2021-11-11)

[Empty comment from Monorail migration]

### je...@gmail.com (2021-11-12)

Fwiw I could also reproduce in
- 90.0.4430.0
- 91.0.4472.0
- 92.0.4515.0
- 93.0.4577.0
- 94.0.4606.0
- 95.0.4638.0
- 96.0.4664.0
- 97.0.4692.0
- 98.0.4700.0

### [Deleted User] (2021-11-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### lg...@chromium.org (2021-11-19)

[Empty comment from Monorail migration]

### lg...@chromium.org (2021-11-19)

Some context on the Aura/Mac divergence in https://crbug.com/chromium/859614. r574159 removed making the window key when the web view is focused (but: that was at a higher layer, and landed in 69, so I think it didn't cause this bug). Mostly posting this as a trail to explain what kind of problems making Mac and Aura behave similarly would involve.

Trying a new approach in patchset 3 of https://chromium-review.googlesource.com/c/chromium/src/+/3270656. Locally, the content and interactive UI tests that failed in c#13 pass with this, but the pointer lock tests do not. I don't really understand how WPT work, but hopefully there's a way to make the window key especially since they're running in Content Shell? +mustaq@ for pointer lock domain expertise and maybe some ideas about what to do re WPT

(NB: I'm out until 11/29, but 96 is already stable anyway).

### mu...@chromium.org (2021-11-19)

Which pointerlock WPTs are failing for you?  Are the tests failing because the window loses focus while in pointerlock, or because it fails to get initial focus?  I am assuming "keyWindow" is same as focused window, please correct me if this is not the case.

### mu...@chromium.org (2021-11-19)

Another thought: based on your comment above about "request is in flight", is relying on RenderWidgetHostViewMac::is_getting_focus_ a possible condition to consider?  Like rejecting lock request when it is set?

### lg...@chromium.org (2021-11-19)

Re: which ones, the builder's still in progress but the failures will stick:
https://ci.chromium.org/ui/p/chromium/builders/try/mac-rel/847287/test-results

Focus on Mac is more complex than on other platforms: what's usually called window activation is a separate concept (key window) from whether a view in the window has focus (first responder). The current implementation of RWHV restricts "focus" to the second concept.

It looks like they're failing because they never receive focus (in the key window sense!) in the first place. On my machine, it looks like Content Shell is running headless, so that might be why, or maybe the window is created but never made key which is a common problem in browser tests. Key status is also asynchronous, so it's likely we may need waits as well.


### lg...@chromium.org (2022-01-06)

Patchset 4 of https://ci.chromium.org/ui/p/chromium/builders/try/mac-rel/874549/test-results fixes the issue, and native tests pass. The WPT tests are passing locally, but not on the bots. Specifics:
https://ci.chromium.org/ui/p/chromium/builders/try/mac-rel/847287/test-results

mustaq@ do you know how we could fix the WPT tests? If not, who can we loop in from the pointer lock and/or web platform side to help with this?

### mu...@chromium.org (2022-01-06)

- Is only mac-rel bot affected with your change?  Please link the CL.
- I see both WPTs and non-WPT web tests failing.  Are those non-WPT web tests pass locally?  They are usually easier to debug than WPTs.

### lg...@chromium.org (2022-01-06)

CL is https://chromium-review.googlesource.com/c/chromium/src/+/3270656

Yes, only mac-rel is failing since the bug and fix are Mac-only. All of the tests pass locally (invoked like `third_party/blink/tools/run_web_tests.py --target release  external/wpt/pointerlock` etc.)

To be clear, the issue here is that the tests need to ensure that their window is key (as described in c#29) as a precondition. I'm not familiar enough with the web side to know if there are other features that require this, or how this is effected in web tests.

### mu...@chromium.org (2022-01-13)

[Empty comment from Monorail migration]

### lg...@chromium.org (2022-02-01)

I'm going to go ahead and unassign. I think https://chromium-review.googlesource.com/c/chromium/src/+/3270656 is directionally correct to fix this, but I don't have bandwidth to figure out what needs to happen with WPT.

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-05-25)

mustaq@ friendly security marshal here, do you think you can triage this? I am unaware of the context.

### [Deleted User] (2022-05-26)

mustaq: Uh oh! This issue still open and hasn't been updated in the last 133 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@chromium.org (2022-05-26)

We have a CL by lgrey@ already, which is failing tests.  One solution to the test failures is suggested in https://crbug.com/chromium/1267867#c32, and apparently we need to resolve some Mac-level focusing problem with WPTs---at least that's my interpretation.   We need a Mac expert to move that CL forward, I am not one unfortunately.

### lg...@chromium.org (2022-05-26)

I think you will need someone who is at the intersection of Mac and web platform expertise, because the Mac team (my team) is entirely unfamiliar with WPT or any kind of web tests AFAIK.

### th...@chromium.org (2022-06-13)

Security marshal here. mustaq@ / lgrey@ / ccameron@ -- do you have any ideas on who could be a good fit to own this ticket? Or do you know who else might have ideas on this?

### mu...@chromium.org (2022-06-13)

One option could be disabling the affected WPTs in Mac and land lgrey@'s CL to fix the bug quickly.  But the problem is that the number of failures is not small!

### mu...@chromium.org (2022-06-14)

Just realized that the failing tests include only a handful of WPTs.  The WPTs are newer (vs the Chrome-specific non-WPT tests), so have smaller compat implications.  At this point, the failing non-WPTs should be the main blocker for the fix!

Specially the failing tests that should not at all depend on pointerlock!   E.g. fast/dom/Window/mozilla-focus-blur.html

To find those, we need to run a dry-run disabling:
external/wpt/pointerevents/pointerlock/*
external/wpt/pointerlock/*
pointer-lock/*


### lg...@chromium.org (2022-06-14)

https://ci.chromium.org/ui/p/chromium/builders/try/mac-rel/1027895/overview

http/tests/pointer-lock/* too?

### mu...@chromium.org (2022-06-16)

Sure, hopefully that's the last group :(

### [Deleted User] (2022-06-30)

mustaq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@chromium.org (2022-07-04)

The CL is ready to land: https://chromium-review.googlesource.com/c/chromium/src/+/3270656

### gi...@appspot.gserviceaccount.com (2022-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/34f3510f3108022e8570b713caed75a082971085

commit 34f3510f3108022e8570b713caed75a082971085
Author: Leonard Grey <lgrey@chromium.org>
Date: Wed Jul 06 17:55:37 2022

Mac: ensure window is key before granting pointer lock

RenderWidgetHostView's `HasFocus` should cover this but it doesn't and
making that change breaks a bunch of assumptions, so it would need a
great deal of care. Instead, add a new method `CanBeMouseLocked` which
delegates to `HasFocus` on all platforms but Mac, and adds the key
window check on Mac (https://developer.apple.com/design/human-interface-guidelines/components/presentation/windows/#macos-window-states)

Tests are disabled because web tests do not currently have a way to
ensure a window is key. mustaq@ will fix in a follow-up (see bug).

Bug: 1267867
Change-Id: I34282a7bade15a9c387147a8c67f38573d96922d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3270656
Reviewed-by: Mustaq Ahmed <mustaq@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Leonard Grey <lgrey@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1021252}

[modify] https://crrev.com/34f3510f3108022e8570b713caed75a082971085/content/browser/renderer_host/render_widget_host_view_mac.h
[modify] https://crrev.com/34f3510f3108022e8570b713caed75a082971085/content/browser/renderer_host/render_widget_host_view_mac.mm
[modify] https://crrev.com/34f3510f3108022e8570b713caed75a082971085/third_party/blink/web_tests/TestExpectations
[modify] https://crrev.com/34f3510f3108022e8570b713caed75a082971085/content/browser/renderer_host/render_widget_host_view_base.h
[modify] https://crrev.com/34f3510f3108022e8570b713caed75a082971085/content/browser/renderer_host/render_widget_host_impl.cc
[modify] https://crrev.com/34f3510f3108022e8570b713caed75a082971085/content/browser/pointer_lock_browsertest_mac.mm
[modify] https://crrev.com/34f3510f3108022e8570b713caed75a082971085/content/public/browser/render_widget_host_view.h
[modify] https://crrev.com/34f3510f3108022e8570b713caed75a082971085/content/browser/renderer_host/render_widget_host_view_base.cc


### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### mu...@chromium.org (2022-08-23)

[Empty comment from Monorail migration]

### mu...@chromium.org (2022-08-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

Updating as fixed based on cl in https://crbug.com/chromium/1267867#c49. please reopen if this assertion is incorrect. 

### am...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-09)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-06)

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1267867?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1354842]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057858)*
