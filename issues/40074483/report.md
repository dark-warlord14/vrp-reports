# Security: Inappropriate implementation in Fullscreen API

| Field | Value |
|-------|-------|
| **Issue ID** | [40074483](https://issues.chromium.org/issues/40074483) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>FullScreen, UI>Browser>Mobile>EdgeToEdge |
| **Platforms** | Android |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tw...@google.com |
| **Created** | 2023-10-10 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 120.0.6057.0 Canary  

Operating System: Android Pixel 7 Pro

**REPRODUCTION CASE**

1. Enable #DrawEdgeToEdge and #DrawWebEdgeToEdge flags
2. Go to <https://permission.site> and click Fullscreen

Note: 'Press Esc to exit fullscreen' warning doesn't display.

## Attachments

- [screen-20231011-031809.mp4](attachments/screen-20231011-031809.mp4) (video/mp4, 13.7 MB)

## Timeline

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### kr...@chromium.org (2023-10-10)

donnd@, sending it your way as you added the flags needed to reproduce. Setting it as medium as this could be part of an address bar spoof.

It was a bit hard to reproduce, I think maybe I had to double tap to zoom once but now it reproduces 100% of the time.

If I go away from Chrome and come back there will be an alert showing up.

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### kr...@chromium.org (2023-10-11)

[Empty comment from Monorail migration]

### do...@chromium.org (2023-10-11)

OK, I think this is effectively a P3 since users must flip a Flag and we will not run experiments that enable this flag. However P2 seems to be the limit on this type of bug.

How was this discovered? Does it also happen if you just enable #DrawEdgeToEdge and #DrawCutoutEdgeToEdge?

[Monorail components: UI>Browser>FullScreen UI>Browser>Mobile>EdgeToEdge]

### ch...@gmail.com (2023-10-11)

It is not reproduced if you enable #DrawEdgeToEdge and #DrawCutoutEdgeToEdge flags, it is only reproduced with DrawEdgeToEdge and DrawWebEdgeToEdge enabled.

### kr...@chromium.org (2023-10-11)

I could not reproduce with those settings. Lowering to Low if those flags are not going out to experiments.

How do you escape fullscreen on devices without a physical back button?

### ch...@gmail.com (2023-10-11)

[Empty comment from Monorail migration]

### do...@chromium.org (2023-10-11)

> How do you escape fullscreen on devices without a physical back button?
You should be able to swipe from the edge using the normal back gesture.

### [Deleted User] (2023-10-11)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-01)

[Empty comment from Monorail migration]

### ch...@gmail.com (2023-11-21)

Any update on this bug? 

### do...@chromium.org (2023-11-21)

The code associated with Fullscreen is being reworked as part of the Edge To Edge development, so this should get fixed as part of that rework and when it's launched (behind a flag  currently).


### [Deleted User] (2023-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-05)

[Empty comment from Monorail migration]

### do...@chromium.org (2024-01-10)

[Empty comment from Monorail migration]

### tw...@chromium.org (2024-01-10)

Donn, remind me is #DrawWebEdgeToEdge the flag for forcing all websites to draw edge to edge? 

If so, and we're not planning to experiment with it, then I think we can simply keep this in the backlog.

If we are planning to experiment with this flag at some point, though, I think we likely need to treat this as experiment blocking to avoid introducing a security regression.

### do...@chromium.org (2024-01-10)

That's right, this bug was reported as only happening when #DrawWebEdgeToEdge is enabled - activating E2E for all pages - which we have no plans to experiment with.
I hope some V2 version of E2E will be able to apply to all pages but that's not yet on the horizon.
I'm keeping this at P2 since there's lots of change happening in E2E and Fullscreen so when all that settles then we can repro and close.


### is...@google.com (2024-01-10)

This issue was migrated from crbug.com/chromium/1491283?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>FullScreen, UI>Browser>Mobile>EdgeToEdge]
[Monorail blocking: crbug.com/chromium/1430288]
[Monorail components added to Component Tags custom field.]

### ch...@gmail.com (2024-04-26)

I can't repro this even by enabling #totally-edge-to-edge flag. Is this fixed?

### tw...@chromium.org (2024-04-26)

Hello,

This bug was filed while the edge to edge feature was under development. We've done quite a bit of refactoring and bug fixing over the last few months in preparation for our initial experiments with the #DrawEdgeToEdge and #DrawCutoutEdgeToEdge flags.

It's likely one of the CLs for that experiment also fixed this #totally-edge-to-edge issue, however, I'm not sure which CL that would be off hand. Note that #totally-edge-to-edge isn't part of the experiment; rather, this is an additional flag to allow for developer testing.

+Amy, how would we typically handle closing out a security bug like this? Should it be a "Won't fix (Obsolete)"?

### ch...@gmail.com (2024-04-30)

Thanks for the reply!

### ch...@gmail.com (2024-05-01)

Amy, Friendly ping :-)

### am...@chromium.org (2024-05-02)

I'm closing this as Fixed for now. This will allow us to try and determine where / when this was resolved and if this should be considered a duplicate. As is and without further context of fix CL, this may be a unique low severity / low impact security issue eligible potential for VRP reward, so we should err on the side of caution and handle it as such.

### tw...@google.com (2024-05-02)

Thanks Amy!

### sp...@google.com (2024-05-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Thank you for the report. Based on this as a low impact, low severity issue, the Chrome VRP Panel has decided to award you $500 for this report. 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-15)

This should have been triaged as SI-None since this specific to features that were not enabled by default.

### pe...@google.com (2024-08-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you for the report. Based on this as a low impact, low severity issue, the Chrome VRP Panel has decided to award you $500 for this report. 
> 
> Thank you for your efforts and helping us make Chrome more secure for all users!
> 
> Cheers,
> Chrome VRP Panel Bot
> 
> 
> P.S. Two other things we'd like to mention:
> 
> * Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure w

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40074483)*
