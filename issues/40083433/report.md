# Security: Prompt boxes steal focus in popups

| Field | Value |
|-------|-------|
| **Issue ID** | [40083433](https://issues.chromium.org/issues/40083433) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P3 |
| **Component** | Blink>HTML |
| **Reporter** | dy...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2015-12-22 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Hello! This may seem trivial, but I've written a proof of concept. Using another bug I've reported to you (<https://crbug.com/chromium/467329>), chained with this one, I've managed to create a semi-effective keylogger that runs in the background and has the ability to gather keypresses at any given time. Essentially, When off screen, prompt boxes still steal focus, and anything the user is typing at the time will be inserted in to the prompt box. Upon pressing enter, the prompt box, filled with text inadvertently typed inside of it, will now have access to anything the user typed.

I will admit it requires some obliviousness to the fact your keys are not being registered on whatever you're actually typing in, but I feel users could easily be fooled, especially seeing as mouse functions work perfectly fine. The proof of concept I've attached will attempt to capture keys, and store them under the localStorage variable "keys". To launch it, simply press the button, feel free to close the original tab.

**VERSION**  

Chrome Version: 47.0.2526.106  

Operating System: Windows 10.0 Beta

## Attachments

- [KeyLogger-PoC.html](attachments/KeyLogger-PoC.html) (text/html, 1.2 KB)
- [KeyLogger-PoC.html](attachments/KeyLogger-PoC.html) (text/plain, 1.2 KB)
- [poc.html](attachments/poc.html) (text/html, 1.3 KB)
- [Screenshot 2025-06-27 at 2.05.57 PM.png](attachments/Screenshot 2025-06-27 at 2.05.57 PM.png) (image/png, 205.1 KB)

## Timeline

### jw...@chromium.org (2015-12-22)

Given that this steals keyboard input but doesn't actually write it to the origin, I think this is probably still a low severity bug, since it requires a user not to notice what's going on.

jochen@, since you're so into popovers/popunders these days, I'm assigning this to you, although if you have a suggestion of a better owner, feel free.

### jw...@chromium.org (2015-12-22)

[Empty comment from Monorail migration]

### jw...@chromium.org (2015-12-22)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-01-11)

msw (random OWNER of constrainted_windows). It looks like the right fix would be for the prompt (which is a constrained window) to show up in the middle of desktop (as it does on mac) if the parent window is off screen.

### ms...@chromium.org (2016-01-12)

I'm not actively working in this area, and I'm not sure who is; any ideas, Mike or Rachel?

Perhaps this is a stupid question, but why do we allow javascript to move windows offscreen?
(can such pages enter mouse lock and cause trouble that way? +Matt)
Should we be concerned about offscreen windows containing a text input field in the page itself?

I'm not sure that constrained windows can always be shown outside of their parent window bounds.
(they're clipped to the parent window bounds on Linux and non-Aero Windows, I think)

### dy...@gmail.com (2016-01-12)

Window constraints has its own issue here: https://code.google.com/p/chromium/issues/detail?id=467329
The idea of mouse lock is interesting. Another potential issue that arises from window movement is clickjacking. A window could be opened right before the user clicks a button, causing them to click something within the newly opened webpage. It wouldn't be as powerful as iframes, but would somewhat dampen the effects of x-frame-options.

### gr...@chromium.org (2016-01-12)

msw@: Unless Mike offers more answers - I don't think anybody is actively working in the ConstrainedWindows area. (And the changelog doesn't show any significant changes there, either)

+sky: Is there any point in just not allowing keyboard/mouse events into off-screen windows?



### wi...@chromium.org (2016-01-13)

No, I'm not aware of anyone working on this either. My recollection is the same as Mike's: the parent-child window relationships force clipping to the browser windows. Undoing these relationships would be difficult and probably trigger lots of unintended consequences.

### sk...@chromium.org (2016-01-13)

> +sky: Is there any point in just not allowing keyboard/mouse events into off-screen windows?

How could you get mouse events for offscreen windows? As far as key events going to offscreen windows, that is certainly possible. We could have checks that if a keyevent is sent to an offscreen window we attempt to move focus.

### mg...@chromium.org (2016-01-13)

#5 I tried to make it take a pointer lock and I can't think of a way to make that particular exploit work. Mouse lock only works in direct response to a user gesture. Popping open a window will not allow that window to automatically take a mouse lock (the user would have to click a button in the tiny/secret popup window). So I don't think that is of particular concern.

### dy...@gmail.com (2016-01-16)

After opening a prompt to enable pointer lock or media, tab+enter will automatically accept the prompt. I will probably create another issue with this, but I can see it being paired with this to gain mouse lock off screen.

### dy...@gmail.com (2016-01-16)

Actually scratch that, it's a different window for media controls.

### mg...@chromium.org (2016-01-17)

Not sure exactly what you mean, but if you have a specific way to programmatically create a new, tiny browser window and have it grab mouse lock, then please file a new security bug with sample code. That would definitely be a problem.

### dy...@gmail.com (2016-01-18)

No, sorry, I thought I had something, but I was misconceived.

### jo...@chromium.org (2016-01-21)

how about forcing a window on screen if we display a constrained window on top of it?

### sk...@chromium.org (2016-01-21)

It's the constrained window that is offscreen. Not knowing about the ramifications of popups, can we force the constrained window to be always on screen?

### jo...@chromium.org (2016-01-21)

https://crbug.com/chromium/571546#c8 says that it's hard / impossible

### sk...@chromium.org (2016-01-21)

I'm not suggesting changing clipping logic, just positioning behavior and only when we're processing a request from the renderer to set the location.
Mike, would that still have consequences?

### sk...@chromium.org (2016-01-21)

For clarity, I'm suggesting the same thing msw did in https://crbug.com/chromium/571546#c5. Don't let popups go offscreen.
wittman, what unintended consequences would happen if we did this?

### jo...@chromium.org (2016-01-21)

that's what https://code.google.com/p/chromium/issues/detail?id=467329 is about anyways, so yes, that'd be a good solution :)

### sk...@chromium.org (2016-01-21)

I can't view 467329. If they are the same, can we close this bug as a dup?

### wi...@chromium.org (2016-01-21)

Forcing the popup browser window to be on screen, so that the resulting constrained window is on screen sounds reasonable to me. My concern in #8 was around making the constrained window top-level, which would be a non-trivial change.

### jo...@chromium.org (2016-01-22)

the other issue (cc'd you) is about JS being able to move the window offscreen.

I think even if the user moved the window offscreen, the modal dialog should be visible (which is what this issue is about)

### sh...@chromium.org (2016-05-04)

[Empty comment from Monorail migration]

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-14)

This issue has been Available for over a year. If it's no longer important or seems unlikely to be fixed, please consider closing it out. If it is important, please re-triage the issue.

Sorry for the inconvenience if the bug really should have been left as Available. If you change it back, also remove the "Hotlist-Recharge-Cold" label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2017-07-14)

It looks like we forgot about this issue. We should have an owner to track this even if it's low severity. 

sky: Could you please help triage/find an owner? Thanks!

### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-11-11)

https://crbug.com/chromium/467329, which was mentioned earlier in this thread, has recently been marked as fixed.

I also can't repro this bug on Mac, Linux or Windows -- I need to activate the popup for it to start getting key input. Does this mean we can consider this bug as fixed?

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sk...@chromium.org (2019-12-18)

I'm going to close this out as I can't repro either. Please reopen with clear instructions if still possible.

### [Deleted User] (2020-03-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dy...@gmail.com (2020-03-26)

Hi, apologies for the delay here. I briefly revisited this bug on a whim, and noticed similar behavior, but I realized that the only reason the prompt doesn't focus is because it can no longer open on windows with 0 height. I've updated the PoC to instead make the window have a height of 1, and am again able to reproduce the issue.

### me...@chromium.org (2020-03-26)

dylanishappy1: Thanks for the updated PoC! Reopening as I can indeed repro on Mac: The prompt box in the popup gets focus after waiting for some time. (Can I also recommend removing or replacing `Math.random() * 10000` in the PoC since it makes the repro unpredictable?)

### [Deleted User] (2020-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### bd...@chromium.org (2020-10-14)

friendly marshal popping by. @sky do you have any updates with regards to this?

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-13)

[Comment Deleted]

### [Deleted User] (2021-08-13)

[Comment Deleted]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### ch...@chromium.org (2022-05-27)

[Empty comment from Monorail migration]

[Monorail components: -UI Security]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/571546?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### me...@google.com (2024-11-07)

This bug is still valid, but the original PoC doesn't work. At least on Mac, window.resizeTo seems to ignore very small windows like 0,1 so I changed it to 10,10 instead.

Attaching the updated PoC.

### wf...@chromium.org (2025-01-08)

[bug bash]. I can't find a good owner for this bug but seems to be HTML and so by a totally fair drawing of lots I'm assigning to masonf@ - please can you take a look at this security bug? Thanks.

### am...@chromium.org (2025-02-27)

this is not fixed, closing this as fixed only temporarily to troubleshoot some automation

### sp...@google.com (2025-02-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
lower impact security UI / user information disclosure bug


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-27)

Hello! Thank you for this nearly (but not quite!) 10 year old report.
We are going through some of our oldest security issues for disclosure and potential rewards.
This issue has already been disclosed for some time, but we did want to go ahead and issue a VRP reward for this report given that it's been open for some time and we can't guarantee when it will be resolved.

Thank you for your past efforts in discovering and reporting this issue to us. And thank for your patience while this remains in our backlog.

### dy...@gmail.com (2025-03-13)

Oh cool! Thanks for wrapping it up. Haven't thought about this one in a longggg time.

### ma...@chromium.org (2025-06-27)

> [bug bash]. I can't find a good owner for this bug but seems to be HTML and so by a totally fair drawing of lots I'm assigning to masonf@ - please can you take a look at this security bug? Thanks.

I'm finally getting a chance to look at this one, sorry. While I can see why this nominally might be marked as a security bug, I don't see how this would be abused in practice. On my Mac, the "hack" window is coerced to be on screen still - see attached screenshot. Even without that, it seems semi-unlikely that someone will type anything meaningful without seeing any output on the screen. Perhaps a password, if the timing were perfect I guess?

I'm somewhat at a loss for what mitigation might fix this, without breaking actual use cases. E.g. some applications I seem to remember use "controller" windows that orchestrate visible apps, so precluding them from ever having focus might cause some issue?

If there are concrete ideas, I'd love to hear them! Otherwise, I'm inclined to close this as WontFix (Infeasible).

### am...@chromium.org (2025-07-02)

I think it may be fair to close this as won't fix at this juncture given that we can't actually resolve this without potentially causing worse breakages. I we see the potential for abuse back in the time when it was reported that may not so realistically achievable in a real world scenario in 2025. 
I'm going to go ahead and close this one out accordingly.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083433)*
