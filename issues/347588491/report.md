# Permission Element overlay and tapjacking

| Field | Value |
|-------|-------|
| **Issue ID** | [347588491](https://issues.chromium.org/issues/347588491) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Geometry, Blink>PermissionsAPI, Internals>Permissions>PermissionElement, UI>Browser>Permissions, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2024-06-16 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description

Prompt Element tapjacking

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

The Permission Element <permission> is a new alternative way for requesting permissions from users. It is available as an origin trial. [0](https://developer.chrome.com/blog/permission-element-origin-trial)

There's two security issues here:

1. The Permission Element, as explained in the Security section of the explainer [1](https://github.com/WICG/PEPC/blob/main/explainer.md#:~:text=PEPC%20might%20be-,partially%20covered,-(to%20hide%20the), ensures it is not coverable by other elements to avoid hiding the text and misleading users. It uses the Intersection Observer to do this. However, the Intersection Observer doesn't actually guarantee there is no graphics rendered above the Permission Element.

This can be abused using `-webkit-box-reflect`, which renders an element to a different position on the screen compared where it is located in the DOM, bypassing these checks.

2. The Permission Element, the same way as the classic permission request modal, ensures that the user can't be tricked to accept a permission by accident by abusing a temporal clickjacking attack.
   However, no checks are done for tap events. Double tapping on the specified point on the screen bypasses this and compromises the user's privacy and security by granting a permission to the camera and microphone (as an example).

Reproduction steps:

1. Open poc.html
2. Double-tap as instructed on the screen

Note: the position is semi-hardcoded in the PoC. Adjust it as needed. In a real-world scenario, this would be done automatically.

#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

An attacker can trick the user into double tapping on the screen, which results in unknowingly accepting the permission request modal and granting access to a permission like camera and microphone.

---

### The cause

#### What version of Chrome have you found the security issue in?

128.0.6541.0

#### Is the security issue related to a crash?

No

#### Choose the type of vulnerability

Permissions Bypass

#### How would you like to be publicly acknowledged for your report?

Thomas Orlita

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.4 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 641.1 KB)

## Timeline

### st...@gmail.com (2024-06-16)

Please update the title of this report to "Security: Permission Element overlay and tapjacking"

### pe...@google.com (2024-06-18)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-06-18)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### tu...@chromium.org (2024-06-19)

From the video, there are 2 problems here:
- [1] Bypassing primary UI (cover the button using CSS -webkit-box-reflect), still triggering the prompt
- [2] Bypassing the prompt (double clicking and the prompt has not been shown).

I'm having trouble replicating the 2, so for now I'll check out 1. It seems interesting and might be a common issue with IntersectionObserver.


### st...@gmail.com (2024-06-19)

> - [2] Bypassing the prompt (double clicking and the prompt has not been shown).

Note: it's double tapping -- not double clicking.

### tu...@chromium.org (2024-06-19)

Yeah, same to me, unreproducible, which platform are you using? Anw, thanks for bringing this interesting issue to our attention!

### ja...@gmail.com (2024-06-19)

Intersection Observer does handle ink overflow in some cases, such as drop shadows and blur. I guess `-webkit-box-reflect` was just missed?

### tu...@chromium.org (2024-06-19)

It's likely. CC @szager. Do you think we're missing `-webkit-box-reflect`?

### tu...@chromium.org (2024-06-19)

cced wangxianzhu as well

### st...@gmail.com (2024-06-26)

Regarding #7 - the tapjacking issue:

I am using a Windows laptop that has a touchscreen.

To help with the repro, can you try first tapping only once, to ensure you see the dialog pop up? It may be the case that due to a different layout on your end, the dialog is positioned differently, and the second tap dismisses it as a result of a touch outside the dialog. The button position is hardcoded in the PoC as I did not want to complicate it by adding dynamic position calculations -- but this can be done so this wouldn't be an issue if this were to be used in an attack. Either way, when double tapping, the dialog shouldn't be visible as it will most likely be dismissed before it's properly rendered on screen due to the subsequent second tap.

### an...@chromium.org (2024-07-03)

For issue number 2) I see that we already have crbug.com/40067456, so I suggest we use this bug to track the fix for issue number 1) and crbug.com/40067456 to track the fix for issue 2).

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


### ap...@google.com (2024-07-13)

Project: chromium/src
Branch: main

commit 7b745a452850671595c9e07bca4e586536e7a616
Author: Stefan Zager <szager@chromium.org>
Date:   Sat Jul 13 18:58:36 2024

    Check for box reflection when hit testing visual overflow
    
    Bug: chromium:347588491
    Change-Id: I491153f26829c6e9d19957ae8116019cac447da6
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5704205
    Reviewed-by: Xianzhu Wang <wangxianzhu@chromium.org>
    Commit-Queue: Stefan Zager <szager@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1327191}

M       third_party/blink/renderer/core/layout/layout_box_model_object.cc
A       third_party/blink/web_tests/external/wpt/intersection-observer/v2/box-reflect.html

https://chromium-review.googlesource.com/5704205


### pe...@google.com (2024-07-16)

Requesting merge to stable (M126) because latest trunk commit (1327191) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1327191) appears to be after beta branch point (1313161).
Merge review required: M126 is already shipping to stable.

Merge review required: M127 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2024-07-19)

This is a permissions bypass that requires minimal user interaction, updating to medium severity

### an...@google.com (2024-07-22)

FYI, there are 2 issues in this bug and only 1 is a permission bypass though it only works in specific circumstances (users using a touchscreen on desktop). This issue however is a duplicate of crbug.com/40067456 which did not get merge approval to 127. See also #c12.

The second problem (the webkit-box-reflect property) is a bypass of spam/annoyance mitigations we have to prevent permission prompt abuse but it's not a bypass of the permission prompt itself, users still have to accept the permission prompt. I don't think this requires a merge to 127/126.

### am...@chromium.org (2024-07-22)

Since the next M127 release is tomorrow and RC for which was already cut with no further beta releases by the time I reviewed this last week, this fix did / does not qualify for backmerge. I updated the severity during the merge review process at that time, but the removal of the merge labels does not seem to have stuck.

For the record, based on when the fix for [crbug.com/40067456](https://crbug.com/40067456) was landed, that should not have been rejected. It was auto-rejected by the bot because, while it was set as medium severity, the priority was incorrectly set as P2 rather than P1.

### sp...@google.com (2024-07-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$3,000 for report of exploit mitigation bypass


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-25)

Congratulations Thomas! Thank you for your efforts and reporting this issue to us -- nice work!

### qk...@google.com (2024-09-24)

Labelling as LTS-NotApplicable-120 due to #comment17.

### pe...@google.com (2024-10-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/347588491)*
