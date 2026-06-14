# UAF in remote_cocoa::RenderWidgetHostNSViewBridge::DisplayPopupMenu

| Field | Value |
|-------|-------|
| **Issue ID** | [338162110](https://issues.chromium.org/issues/338162110) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Accessibility>Compatibility |
| **Platforms** | Mac |
| **Reporter** | ha...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2024-05-01 |
| **Bounty** | $10,000.00 |

## Description

deleted

## Attachments

- [PoC.html](attachments/PoC.html) (text/html, 174 B)

## Timeline

### th...@chromium.org (2024-05-01)

I can reproduce this on Mac on M126 but not M125 or M124. (On M124, I don't see the dropdown; on M125 I can see the dropdown but clicking "Mac" does not throw an error.) IIUC this is a UAF in the browser process with minimal user interactions needed, so I am marking this as Critical severity. I think this is likely Mac-specific; I don't see Mac as an option in the dropdown on Linux.

Assigning to [janewman@microsoft.com](mailto:janewman@microsoft.com) since it looks like you may have added this functionality recently (<https://crrev.com/c/5320280>). Could you PTAL?

### pe...@google.com (2024-05-01)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-01)

Setting Priority to P0 to match Severity s0. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ja...@microsoft.com (2024-05-01)

Not repro on my canary at 126.0.6450.0, building now to test on main. If I can repro consistently there, I'll do a bisect.

### th...@chromium.org (2024-05-01)

janewman@: just in case -- make sure you are building with asan (<https://chromium.googlesource.com/chromium/src/+/HEAD/docs/asan.md>).

### ja...@microsoft.com (2024-05-01)

@thefrog, I have been having a lot of trouble getting asan to build on my m1(arm) mac, but was able to pull down and run asan builds of 125 and 126, with the same result as you, no repro in 125 and repro in 126.

Findings so far:
I am able to reproduce this with any popup menu, doesn't have to be the one on chrome://accessibility, but currently it looks like we need to have accessibility enabled from there.

My alternate repro case:

1. Check the "web contents accessibility" checkbox.
2. Go to chrome://settings/appearance
3. Click on the "Mode" dropdown.

I see the renderer process that contains the dropdown is failing a check - perhaps that is connected, we are tearing down as the popup is created. If this is true, it could be tested by having a no-check + asan build and testing that scenario.
FWIW the check we are hitting is here: [CHECK\_EQ(ax\_menu\_list.AXObjectID(), current\_menu\_list\_axid\_);](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/accessibility/ax_object_cache_impl.cc;l=3882)

Looks like that was added here: <https://chromium-review.googlesource.com/c/chromium/src/+/5497817> and is already being reverted, so I would guess this issue will no longer repro in builds with the revert.

### ha...@gmail.com (2024-05-02)

I wrote the PoC,you can follow the command,and choose option.

out/Default/Chromium.app/Contents/MacOS/Chromium --force-renderer-accessibility=complete. <http://127.0.0.1:8080/PoC.html>

### ja...@microsoft.com (2024-05-02)

Now that [the revert](https://chromium-review.googlesource.com/c/chromium/src/+/5506576) has gone in, I believe that this issue will be mitigated as well. I'll test once tomorrow's canary has been built and report back. Either way, this is entirely unrelated to the accessibility internals page and [my CL to add a dropdown](https://crrev.com/c/5320280)

### ha...@gmail.com (2024-05-02)

I'm not sure whether this will be mitigated, because the fundamental reason is that the RenderWidgetHostViewMac object will be released when RenderProcessHostImpl::OnChannelError, and then the life cycle of the RenderWidgetHostNSViewBridge object belongs to RenderWidgetHostViewMac, so it will cause UAF.There is a high probability that the vulnerability can still be triggered in other ways. I think the root cause should be fixed.

### ja...@microsoft.com (2024-05-02)

I agree, the underlying issue remains, a renderer that hits a check or crashes at a similar time will likely cause the use after free to occur. My point was more that from a user-pain point of view, the revert will make this less likely to occur.

That said, from a security point of view, your are right, the issue is **not** mitigated.

However, this is outside of my realm of expertise (accessibility), and we should get this reassigned to someone who is more familiar with that area.

### ha...@gmail.com (2024-05-02)

raw\_ptr<remote\_cocoa::mojom::RenderWidgetHostNSView> ns\_view\_ = nullptr; maybe change this raa pointer to weak pointer

### ch...@chromium.org (2024-05-03)

ccameron: Could you please take a look at this P0 UAF? Thanks!

### am...@chromium.org (2024-05-06)

Hello, so I've reviewed this a few times, and while the user interaction here is moderate, I because it is minimal->moderate, I don't believe this classifies as a critical severity issue. Critical severity is generally reserved for fully remote exploitable issues that are no migited and result in memory corruption in a non-sandboxed process. As such, I've lowered this to high severity.
Please feel free to readjust if any my assertions are incorrect here.

### ha...@gmail.com (2024-05-07)

Yep,this should be high.

### pe...@google.com (2024-05-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ha...@gmail.com (2024-05-10)

Any update,developer?

### pe...@google.com (2024-05-18)

ccameron: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ti...@chromium.org (2024-05-20)

[Secondary shepherd]

Restoring the descrition as it had useful context. ccameron@ are you still a good owner for this?

### cc...@google.com (2024-05-20)

It might be best to go to mek@ now.

### me...@chromium.org (2024-05-22)

From reading the bug history it sounds to me like there is no longer an easy way to repro this issue? Is that correct? Or are there new repro steps that would let me look into this?

### ha...@gmail.com (2024-05-23)

yep, there is currently no new way to trigger this vulnerability, but it is best to change the pointer to weakptr. Maybe there will be other ways to trigger it in the future.

### me...@chromium.org (2024-05-23)

Checking out a revision from when this still repro'd made it pretty clear what was going on; this is a regression I introduced in M123 in <https://crrev.com/c/5270062>. Should be fixed by <https://chromium-review.googlesource.com/c/chromium/src/+/5564186>.

(and the raw pointer you identified has nothing to do with it; besides that changing it to a weak pointer wouldn't exactly be straight-forward since mojo::Remote doesn't have a way to get a weak pointer to its proxy).

### ap...@google.com (2024-05-23)

Project: chromium/src
Branch: main

commit 5c897e0ed5c8e2d65f730e11238c37e9c622b1f2
Author: Marijn Kruisselbrink <mek@chromium.org>
Date:   Thu May 23 17:02:12 2024

    Use absl::Cleanup rather than base::AutoReset in DisplayPopupMenu
    
    Since RenderWidgetHostNSViewBridge might get deleted while displaying a
    popup menu, it is not safe to use base::AutoReset to reset the
    showing_popup_menu_ member. So use absl::Cleanup with a weak pointer
    instead.
    
    Bug: 338162110
    Change-Id: Ic907b2e6541d095eebee2c13a778b2d46afa54ed
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5564186
    Reviewed-by: Leonard Grey <lgrey@chromium.org>
    Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1305164}

M       content/app_shim_remote_cocoa/render_widget_host_ns_view_bridge.mm

https://chromium-review.googlesource.com/5564186


### pe...@google.com (2024-05-24)

Requesting merge to beta (M126) because latest trunk commit (1305164) appears to be after beta branch point (1300313).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-05-24)

Merge review required: M126 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

### am...@chromium.org (2024-05-24)

A merge should not be needed here; the fix in c#24 is a functional change; the revert in #7 mitigated the UAF

### me...@chromium.org (2024-05-24)

I'm not sure I agree that the revert in #7 did anything to mitigate this UAF. It might have made it harder for users to accidentally run into the UAF, but it did nothing to make it harder attackers that want to hit this UAF to hit it; I'm fairly certain that any renderer crash while a <select> popup is open would hit this UAF, both of which are things a renderer can easily cause to happen.

### am...@chromium.org (2024-05-24)

Thanks for pointing that out, I see I was not throughout in reviewing this issue when I was interrupted. And while this issue goes back farther than 126, I don't think given the preconditions and the 1 byte write warrants this fix to only be backmerged as far as 126, current beta

### am...@chromium.org (2024-05-24)

reviewed <https://crrev.com/c/5564186> canary data; approved for merge to M126 beta; please merge this fix to branch 6478 by EOD Tuesday so this fix can be included in next week's M126 beta update

### ap...@google.com (2024-05-25)

Project: chromium/src
Branch: refs/branch-heads/6478

commit fdf61f65bc64b626197d77e259e4dfa9dc26e404
Author: Marijn Kruisselbrink <mek@chromium.org>
Date:   Sat May 25 00:13:11 2024

    Use absl::Cleanup rather than base::AutoReset in DisplayPopupMenu
    
    Since RenderWidgetHostNSViewBridge might get deleted while displaying a
    popup menu, it is not safe to use base::AutoReset to reset the
    showing_popup_menu_ member. So use absl::Cleanup with a weak pointer
    instead.
    
    (cherry picked from commit 5c897e0ed5c8e2d65f730e11238c37e9c622b1f2)
    
    Bug: 338162110
    Change-Id: Ic907b2e6541d095eebee2c13a778b2d46afa54ed
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5564186
    Reviewed-by: Leonard Grey <lgrey@chromium.org>
    Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1305164}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5571680
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Auto-Submit: Marijn Kruisselbrink <mek@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#598}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       content/app_shim_remote_cocoa/render_widget_host_ns_view_bridge.mm

https://chromium-review.googlesource.com/5571680


### sp...@google.com (2024-05-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
moderately mitigated memory corruption in a non-sandboxed process

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are not already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-30)

Thank you for your efforts and reporting this issue to us!

### ha...@gmail.com (2024-05-30)

Hi,Amy,

Why only 3k for one interaction?I think it should be higher than 3k

### wf...@chromium.org (2024-05-30)

Thanks for your query about the reward, Amy will respond to this next week.

### ha...@gmail.com (2024-06-05)

This [issue 325936438](https://issues.chromium.org/issues/325936438) rewards 6000 for so many interactions, but I only need to interact once and it only costs 3000

### am...@chromium.org (2024-06-05)

Thanks for your feedback. The report that you linked in c#26, while mitigated by user interaction, was of higher report quality, thus it received a $5,000 reward for the report itself (they also earned a $1,000 bisect bonus). The user interaction required in the other report also involved some interaction that is standard with the FedCM workflow.
This also isn't a single interaction, but is a bug that isn't remote exploitable and requires the user to choose to engage with chrome://accessbility and click to different options within the Accessibility modes and tree viewing options.
This is not something most users are going to engage by convincing (not of their own accord / need) and would also be a higher bar for an attacker to convince a user to engage in that way during a real world attack scenario.

### ha...@gmail.com (2024-06-05)

Hi Amy,

see c#8,Do you see my description?

out/Default/Chromium.app/Contents/MacOS/Chromium --force-renderer-accessibility=complete. <http://127.0.0.1:8080/PoC.html>

### am...@chromium.org (2024-06-11)

Hi, thanks for reaching out. I've added the reward-topanel tag since you have requested a reassessment.
But it seems that POC was not able to reliable, easily reproduce this issue. We will, however, take another look at a future VRP panel session.

### ha...@gmail.com (2024-06-12)

What I tested at the time was easy to reproduce, as long as there is option in the form

### sp...@google.com (2024-06-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
reassessment or secondary POC and additional information: mildly mitigated bug a non-sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-21)

Thanks again for reporting this issue to us and nice work!

### pe...@google.com (2024-08-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/338162110)*
