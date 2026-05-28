# Security: Desktop permission prompt tapjacking

| Field | Value |
|-------|-------|
| **Issue ID** | [40067456](https://issues.chromium.org/issues/40067456) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Views |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2023-07-14 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

On desktop platforms, the permission prompt UI protects against unwanted clicks.  

This is implemented in `InputEventActivationProtector::IsPossiblyUnintendedInteraction`, which ignores the interaction if there was a previous interaction less than 500ms ago.

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:ui/views/input_event_activation_protector.cc;l=55;drc=316850595842d7b40953b16f96e7615b1bfa57a7>

```
  if (!event.IsMouseEvent() && !event.IsTouchEvent()) {  
    return false;  
  }  

```

Looking at this code makes it seem that it takes both mouse and touch events into consideration, but when I tested this on my device, it works for mouse events only.  

This leaves the permission prompt UI vulnerable to tapjacking attacks.

**VERSION**  

Chrome Version: 117.0.5889.0  

Operating System: Windows 11 with a touchscreen display

**REPRODUCTION CASE**

1. Open poc.html
2. Repeatedly tap on the cookie

[poc-click.webm] shows the correct behavior with clicks.  

[poc-touch.webm] shows the vulnerable behavior with taps, where the permission prompt is accepted before even being visible.

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 527 B)
- [poc-click.webm](attachments/poc-click.webm) (video/webm, 281.5 KB)
- [poc-touch.webm](attachments/poc-touch.webm) (video/webm, 92.7 KB)

## Timeline

### [Deleted User] (2023-07-14)

[Empty comment from Monorail migration]

### bo...@chromium.org (2023-07-16)

Thanks for the report. I'm unable to reproduce this behavior since I lack access to a touch-enabled desktop device, so I'm triaging based entirely on the included recording. Consequently, I'm setting FoundIn to M114 exclusively on the guess that this behavior has been around a while. 

@elainechien, as you investigate please update the FoundIn label if you determine this behavior was introduced more recently than M114. 

[Monorail components: Internals>Views]

### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### st...@gmail.com (2023-07-16)

Thanks - regrading the severity, shouldn't this be Medium? (exposure of sensitive data with the help of user interaction) Both https://crbug.com/chromium/1411524 and https://crbug.com/chromium/1160485 are also Medium and they have comparable preconditions and impact.

### bo...@chromium.org (2023-07-17)

Thanks for the follow up. For transparency I'm regarding this report as Low severity/impact because the exposure of user data (Medium) has the precondition of UI interactions. Our severity guidelines [1] warrant downgrading security severity when a bug is "Not web accessible, [and] reliant solely on direct UI interaction to trigger." That is the case for this report, hence this report is at most a Low severity security bug. 

[1] https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md

### [Deleted User] (2023-07-17)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-07-17)

(I am a bot: this is an auto-cc on a security bug)

### el...@chromium.org (2023-07-20)

I see that the functionality to protect against unwanted clicks was added recently. Potentially the protection in touch mode wasn't fully supported. I'll take a look.

### el...@google.com (2023-07-24)

[Empty comment from Monorail migration]

### el...@chromium.org (2023-07-28)

Talked to tungnh@ who mentioned that the implementation was mainly focused on click rather than touch. 

tungnh@ - if this is something that your team has investments in then feel free to take this bug. Otherwise I can keep it in my queue for now and see if there's a quick addition to the existing code that can support touch. 

### st...@gmail.com (2023-10-17)

The same issue exists in the new PWA install dialog. I am not sure if it uses the same input protection implementation as the permission prompt or if it's different and should be tracked as a separate bug.

### is...@google.com (2023-10-17)

This issue was migrated from crbug.com/chromium/1465000?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ap...@google.com (2024-07-03)

Project: chromium/src
Branch: main

commit 22b26969353c3c4899a8b7cc9e19ace3389e1ea2
Author: Andy Paicu <andypaicu@chromium.org>
Date:   Wed Jul 03 08:05:32 2024

    Ensure the input protector also covers taps
    
    Screen taps are considered gesture events and therefore the input
    protectors does not cover them. This CL addresses that and adds tests
    for gesture and touch events.
    
    Bug: 347588491
    Fixed: 40067456
    Change-Id: Ibaecaad9edee965c7458a0318b546322cc65047a
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5664719
    Reviewed-by: Thomas Nguyen <tungnh@chromium.org>
    Reviewed-by: Peter Kasting <pkasting@chromium.org>
    Commit-Queue: Andy Paicu <andypaicu@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1322641}

M       ui/views/input_event_activation_protector.cc
M       ui/views/window/dialog_client_view_unittest.cc

https://chromium-review.googlesource.com/5664719


### pe...@google.com (2024-07-10)

Merge rejected: M127 is already shipping to beta and this issue is marked as a Priority:P2,P3 or Type:feature request.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### sp...@google.com (2024-07-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
$1,000 for report of lower impact security UI spoof 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-02)

Congratulations, Thomas! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-10-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067456)*
