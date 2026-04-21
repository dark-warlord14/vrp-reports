# heap-use-after-free in WebDragSourceAura::CancelDrag

| Field | Value |
|-------|-------|
| **Issue ID** | [40060340](https://issues.chromium.org/issues/40060340) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Portals |
| **Platforms** | Linux, Windows |
| **Reporter** | xp...@gmail.com |
| **Assignee** | mc...@chromium.org |
| **Created** | 2022-07-20 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

0. Ensure you have portals experiment enabled.

1. Start a webserver and open poc.html.
2. Drag either test image or the "Drag Me" text.  
   
   UAF ensues

**Problem Description:**  

heap-use-after-free at RenderPassBuilderD3D12.cpp:125 in dawn::native::d3d12::RenderPassBuilder::GetHighestColorAttachmentIndexPlusOne

**Additional Comments:**  

N/A

\*\*Chrome version: \*\* 105.0.5191.1 \*\*Channel: \*\* Canary

**OS:** Windows

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 4.8 KB)
- [portal.html](attachments/portal.html) (text/plain, 165 B)
- [asan.txt](attachments/asan.txt) (text/plain, 21.3 KB)

## Timeline

### [Deleted User] (2022-07-20)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-07-21)

On Mac I just get a null deref rather than an ASan UAF, but the program does crash, but that might be because the crash is in WebDragSourceAura.

Because Portals are not enabled, this is Impact-None and Sev-Medium because of the drag interaction.

Based on the stack trace, it looks like the nested event loop from the drag is the culprit. The top stack frame is incorrect (likely due to linker optimizations).

[Monorail components: Blink>Portals]

### xp...@gmail.com (2022-07-25)

I don't exactly know how owners work, rsesek@chromium.org, but sadrul was last seen 60 days ago. Should a new owner be suggested?

### xp...@gmail.com (2022-08-11)

Any updates?

### th...@chromium.org (2022-08-15)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-08-15)

alexmos@, could you help find an owner for this ticket?

### xp...@gmail.com (2022-08-15)

This portal bug could be an incomplete fix for a recently disclosed portal issue [1]. The poc's look almost identical. The difference between these reports is that the portal is removed while user is still dragging from portal.html. The exploitability of this has been shown to be quite easy with a compromised renderer [2].

[1].
 https://crbug.com/1312144

[2].
https://bugs.chromium.org/p/chromium/issues/detail?id=1153595#c4

### al...@chromium.org (2022-08-15)

mcnee@, would you mind taking a look, given that you fixed https://crbug.com/chromium/1312144 which seems similar?  Also +dcheng@ who's very familiar with drag-and-drop in general.

### mc...@chromium.org (2022-08-16)

Yeah, the WebDragSourceAura::window_ is invalid due to portal activation during the drag and drop.

This also looks similar to https://crbug.com/chromium/1303330.

Listening for the destruction of the window and clearing the pointer fixes this. I'll put up a CL.

### mc...@chromium.org (2022-08-16)

CL: https://chromium-review.googlesource.com/c/chromium/src/+/3835023

### gi...@appspot.gserviceaccount.com (2022-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/83b4156f6c493dbfb338fc10905688a842219cee

commit 83b4156f6c493dbfb338fc10905688a842219cee
Author: Kevin McNee <mcnee@chromium.org>
Date: Wed Aug 17 01:54:58 2022

Ensure WebDragSourceAura::window_ is cleared when destroyed

In its current multi-WebContents architecture, portal adoption destroys
the aura::Window of the navigated away from page. If this happens during
a drag and drop nested run loop, we may go on to access a destroyed
WebDragSourceAura::window_. We now observe its destruction and clear the
pointer.

Bug: 1346048
Change-Id: I4e603422f5a0b2676328fc70f4d3203b6ec83210
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3835023
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1035837}

[modify] https://crrev.com/83b4156f6c493dbfb338fc10905688a842219cee/content/browser/web_contents/web_contents_view_aura.cc


### mc...@chromium.org (2022-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-17)

[Empty comment from Monorail migration]

### mc...@chromium.org (2022-08-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-09)

Congratulations, Sven! The VRP Panel has decided to award you $10,000 for this report. The reward amount was based on this issue being a mildly mitigated security bug as reflected in the updated Chrome VRP policies and reward amounts [1]. Thank you for your efforts in reporting this issue to us -- nice work! 

[1] https://g.co/chrome/vrp 

### xp...@gmail.com (2022-09-09)

Hi Amy, thank you! 

Bugs [1][2] are very similar to this issue, with [2] being almost identical. Is there a reason why this issue is not rewarded the same as [1] or [2]? Could the panel reconsider the amount rewarded?

[1]. https://crbug.com/1303330

[2]. https://crbug.com/1312144

### am...@chromium.org (2022-09-12)

Hi Sven, we are aware of the VRP reward difference between the two bugs as well as the similarity between the two bugs/bug reports themselves. In August, we updated our VRP rewards and policies [1], with one of the specific changes being around reports of security bugs with varying degrees of mitigations. While this bug is only very lightly mitigated by the drag, it is still a mitigation that slightly reduces the potential exploitability. This reward amount of $10,000 is still higher than the updated range for mildly mitigated bugs to reflect the very light mitigation presented by the drag. The VRP Panel discussed this issue throughly. 
While we are happy to re-assess, I'd like to level-set that the potential for a change in reward amount is very unlikely based on the stipulations presented here. 


[1] https://g.co/chrome/vrp 

### xp...@gmail.com (2022-09-12)

I appreciate the thorough explanation. I wasn't clear in my original comment. I am questioning why the bonus given to the 2 similar that wasn't offered here:

"+ $5,000 renderer bonus as this appears to be web accessible memory corruption of the browser process". 

I have read through the link you've provided and I have read the August VRP update email. I did not read changes pertaining to "renderer bonus. . . . appears to be web accessible memory corruption of the browser process" bonuses being removed from the offered reward potential. If it was mentioned elsewhere or I misunderstood the VRP rules/rewards, then please excuse my ignorance. 

Thank you.

### am...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-19)

Hi Sven, the bonus was not given as this issue is mitigated and not web-accessible/remote exploitable, if you refer to the rules page (https://g.co/chrome/vrp) the first table in the 'Reward Amounts' section is for fully web accessible bugs and is separate and discrete from the section and table for 'Reward Amounts for mitigated security bugs'. Only the web accessible table has the following footnote "[1] Amount based on precondition of a compromised renderer, otherwise the renderer RCE reward will also be added." This bonus does not apply for mitigated security bugs. 

### [Deleted User] (2022-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-11-23)

This issue was migrated from crbug.com/chromium/1346048?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1352581, crbug.com/chromium/1352691]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060340)*
