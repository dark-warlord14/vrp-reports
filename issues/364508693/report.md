# User can unknowingly Permission Prompt Hidden behind PiP during Interaction

| Field | Value |
|-------|-------|
| **Issue ID** | [364508693](https://issues.chromium.org/issues/364508693) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2024-09-04 |
| **Bounty** | $1,000.00 |

## Description

#### SUMMARY

The Permission prompt can be obscured by a Picture-in-Picture (PiP) window for video or documents, potentially allowing a page to obtain permissions without user awareness.

Current address bar permission prompts do check for PiP window occlusion. This issue is very similar to [issue 342194497](https://issues.chromium.org/issues/342194497), with the key difference being that final approval of the permission dialogue requires pressing Enter twice. Since the prompt behind the PiP window is protected, the user is led to press Enter twice—first to close the PiP window and then to approve the permission. Therefore, Chrome should implement a delay here to mitigate this issue.

To minimize user interaction, a compromised renderer can open the PiP window, as seen in [issue 338398040](https://issues.chromium.org/issues/338398040).

#### VULNERABILITY DETAILS

A page can display a Video or Document PiP window over a normal window with a permission prompt, obscuring the prompt and unknowingly allowing it when the user interacts with the webpage.

An attacker can instruct the user to press keys while the permission prompt is obscured. For example, pressing Tab three times followed by Enter twice can result in the user granting permissions without their awareness.

#### VERSION

- Chrome Version: 130.0.6697.0 (Official Build) Canary (64-bit), 128.0.6613.120 (Official Build) (64-bit) Stable
- Operating System: Windows 11

#### REPRODUCTION CASE

**Note:** The Proof of Concept (PoC) uses Document PiP, but this also works with Video PiP.

**Prerequisites:** None required.

1. Download the attachment `poc.html` and `permission.html` files.
2. Host the page on a local server or open `poc.html` directly from the same folder.
3. Visit the webpage using the latest Chrome browser.
4. Click "Verify" and then "Start," press Tab three times, and confirm.
5. Press Enter twice and observe that the camera permission is unknowingly approved without the user's awareness.

**Observed:** The attacker can obtain permissions without the user’s awareness.

**Expected:** The attacker should not be able to obtain permissions without the user’s awareness.

#### CREDIT INFORMATION

Reporter credit: Shaheen Fazim

## Attachments

- [demo.mp4](attachments/demo.mp4) (video/mp4, 2.0 MB)
- [permission.html](attachments/permission.html) (text/html, 1.5 KB)
- [poc.html](attachments/poc.html) (text/html, 5.1 KB)

## Timeline

### fa...@gmail.com (2024-09-04)

Similar issue, see: [bug 342194497](https://issues.chromium.org/issues/342194497)

### ct...@chromium.org (2024-09-05)

Thanks for the report!

After turning on full keyboard access in the macOS Accessibility settings I was able to successfully reproduce on my large monitor -- however, the popup window and permission prompt are visible, just way off to the side and maybe easy to miss (see attached screenshot). When I try on my smaller laptop display, this no longer reproduces for me. Full keyboard access on macOS shows outlines for the element that is under focus, so I can see that the keyboard input is still controlling focus on the permission prompt which does seem to indicate that this is maybe possible, but maybe the occlusion checking is working and disabling submitting the "allow" decision while occluded?

Are there setup steps I'm missing here? Or is this maybe platform specific to Windows? I can quick try on Linux as well.

### fa...@gmail.com (2024-09-05)

Increasing the left and top values can completely hide it. I used the minimum left and top values to hide it on my PC. You can try changing them, or maybe use left=1500 and top=1500.

### fa...@gmail.com (2024-09-05)

If possible, could you try this on a Windows machine. My PoC is based on (made for) Windows 11 OS.

### ct...@chromium.org (2024-09-05)

It appears that focus goes back to the PiP window and/or the focus in the permission popup resets to the first element (so not Allow), breaking the PoC on macOS. I'll spin back up my Windows VM to test there as I do expect this may be platform dependent.

### ct...@chromium.org (2024-09-05)

Ah hmm I can't test in my VM because it doesn't have a camera device so the permission request just fails.

Routing this to PiP and permissions folks from [Issue 342194497](https://issues.chromium.org/issues/342194497) since this appears to be feasible (as evidenced by me being able to switch focus to the buttons on the occluded prompt), just this particularly poc may not be fully generalized.

Setting some security labels:

- Severity-Medium (S2) hidden interaction with permissions prompt (spoofing) but with significant user interaction required
- OS: Seems likely to be triggerable with some modifications on all Desktop platforms
- FoundIn-128

### st...@chromium.org (2024-09-05)

You can use `--use-fake-device-for-media-stream` to have a fake camera feed to ask permission for

### ct...@chromium.org (2024-09-05)

Ah excellent, with that flag I can confirm I can repro on Windows Canary M130, with chrome://flags#one-time-permission enabled and passing --use-fake-device-for-media-stream on the command line.

### pe...@google.com (2024-09-06)

Setting milestone because of s2 severity.

### pe...@google.com (2024-09-06)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### st...@chromium.org (2024-09-09)

@elklm: I can pretty easily add a delay such that after a prompt becomes unoccluded it is still uninteractable for some period of time. Do you have an opinion on how long a delay that should be? E.g. 2 seconds? 3 seconds? 5 seconds?

Or is there an alternative solution you think we should consider?

### el...@google.com (2024-09-10)

Here [1] you can see how we solved permission prompt clickjacking for another bug. It looks like we should be able to use the same logic here. It uses 500ms delay. If 500ms is too fast, maybe you can increase it to 1 second.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/permissions/permission_prompt_bubble.cc;l=71-78;drc=8e948282d37c0e119e3102236878d6f4d5052c16

### ap...@google.com (2024-09-12)

Project: chromium/src
Branch: main

commit 4fcc965f7b6a9aa9965bc84e0a180eda77a20467
Author: Tommy Steimel <steimel@chromium.org>
Date:   Thu Sep 12 13:25:16 2024

    pip occlusion: Prevent immediate interaction after unocclusion
    
    We currently prevent input into a permission prompt while it's occluded
    by a picture-in-picture window. However, some spoofs can still happen
    immediately after a prompt because unoccluded.
    
    This CL prevents permission dialogs from being interacted with
    immediately after they're no longer occluded by a picture-in-picture
    window.
    
    Bug: 364508693
    Change-Id: Ib52d1af8bc5216a50a089e319dea31f0bab108c1
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5854142
    Commit-Queue: Tommy Steimel <steimel@chromium.org>
    Reviewed-by: Elias Klim <elklm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1354501}

M       chrome/browser/ui/views/permissions/permission_prompt_base_view.cc

https://chromium-review.googlesource.com/5854142


### sp...@google.com (2024-09-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact web platform privilege escalation / security UI bug


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-19)

Congratulations Shaheen! While the permissions dialog is pretty well hidden from the user here, there are very high user interaction preconditions required here, as such we consider this a lower impact issue. We appreciate the efforts and reporting this issue to us!

### pe...@google.com (2024-12-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### dx...@google.com (2025-06-10)

Project: chromium/src  

Branch: main  

Author: Benjamin Keen [bkeen@google.com](mailto:bkeen@google.com)  

Link:      <https://chromium-review.googlesource.com/6614637>

Extend input protector to cover key events for permission prompts

---


Expand for full commit details
```
     
    This change extends input protector to also cover key events 
    (EventType::kKeyPressed and EventType::kKeyReleased) for permission 
    relevant prompts, in order to prevent unintentional key event actions. 
     
    Also disable input event protection for affected interactive tests that 
    perform automated button press. This is done to prevent the tests from 
    having to wait for the input protector timeout interval. 
     
    Bug: 364508693, 373794472, 416364499 
    Change-Id: I590074221366930c5af653554ae3d21d8191f883 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6614637 
    Reviewed-by: Mitsuru Oshima <oshima@chromium.org> 
    Reviewed-by: Keren Zhu <kerenzhu@chromium.org> 
    Reviewed-by: Florian Jacky <fjacky@chromium.org> 
    Reviewed-by: Lily Chen <chlily@chromium.org> 
    Commit-Queue: Benjamin Keen <bkeen@google.com> 
    Reviewed-by: Zachary Tan <tanzachary@chromium.org> 
    Reviewed-by: Luke Klimek <zgroza@chromium.org> 
    Reviewed-by: Slobodan Pejic <slobodan@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1472055}

```

---

Files:

- M `chrome/browser/smart_card/smart_card_permission_uitest.cc`
- M `chrome/browser/ui/ash/privacy_hub/geolocation_switch_interactive_uitest.cc`
- M `chrome/browser/ui/views/download/bubble/download_bubble_row_view.cc`
- M `chrome/browser/ui/views/download/bubble/download_bubble_row_view_unittest.cc`
- M `chrome/browser/ui/views/payments/payment_sheet_view_controller.cc`
- M `chrome/browser/ui/views/permissions/embedded_permission_prompt_interactive_uitest.cc`
- M `chrome/browser/ui/views/permissions/exclusive_access_permission_prompt_interactive_uitest.cc`
- M `chrome/browser/ui/views/permissions/permission_prompt_base_view.cc`
- M `chrome/browser/ui/views/permissions/permission_rhs_indicators_interactive_uitest.cc`
- M `chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.cc`
- M `ui/views/bubble/bubble_frame_view.cc`
- M `ui/views/input_event_activation_protector.cc`
- M `ui/views/input_event_activation_protector.h`
- M `ui/views/test/mock_input_event_activation_protector.h`
- M `ui/views/window/dialog_client_view.cc`
- M `ui/views/window/dialog_client_view.h`
- M `ui/views/window/dialog_client_view_unittest.cc`

---

Hash: 08e1033b8bb5fe55f3147f116552bdcd5569fa50  

Date:  Tue Jun 10 21:08:05 2025


---

## Bounty Award

> report of lower impact web platform privilege escalation / security UI bug

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/364508693)*
