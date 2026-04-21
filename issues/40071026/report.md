# Security:  Trick user into thinking they have escaped fullscreen on MacOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40071026](https://issues.chromium.org/issues/40071026) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen, UI>Browser>Permissions>Prompts |
| **Platforms** | Mac, Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2023-08-31 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

On MacOS, a permission dialog can be dismissed using "Esc" key which is the same key as exiting fullscreen. When the permission dialog occurs after a site enters the user into fullscreen, and if a user presses "Esc" afterwards it will be routed to the permission dialog instead of the fullscreen and dismiss the dialog instead of the fullscreen. This means that an attacker could place a fake omnibox  

and trick the user into thinking that they have exited fullscreen and with the fake omnibox, spoof other website URLs.

**VERSION**  

Chrome Version: 116.0.5845.140 (Official Build) (x86\_64) [Stable]  

Operating System: MacOS Version 11.7 (Build 20G817)

**REPRODUCTION CASE**

1. Open the HTML file and click to enter fullscreen
2. Press "Esc". "Insert omnibox here" text should appear. An attacker can use this opportunity to trick the user into thinking that they have exited fullscreen and draw a fake omnibox once the user pressed "Esc"

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [escape-spoof.html](attachments/escape-spoof.html) (text/plain, 394 B)
- [Untitled_ Aug 31, 2023 6_45 PM.webm](attachments/Untitled_ Aug 31, 2023 6_45 PM.webm) (video/webm, 251.2 KB)
- [escape-spoof.webm](attachments/escape-spoof.webm) (video/webm, 379.7 KB)
- [escape-spoofing.html](attachments/escape-spoofing.html) (text/plain, 29.4 KB)

## Timeline

### [Deleted User] (2023-08-31)

[Empty comment from Monorail migration]

### ph...@chromium.org (2023-08-31)

I can reproduce on MacOS stable.  On linux, pressing esc will both dismiss the permission prompt and escaping from full screen mode.

Hi kerenzhu@.  Could you take a look at this security bug please?  I found your ldap on another bug related to full screen.

[Monorail components: UI>Browser>FullScreen UI>Browser>Permissions>Prompts]

### [Deleted User] (2023-08-31)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-08-31)

Assuming the attacker successfully replicates the whole Top Chrome UI using HTML (which https://crbug.com/chromium/1477587#c0 does not demonstrate), it will be obvious to the user that the permission prompt is anchored to a wrong position. In the attack, the prompt is positioned to the top border of screen, whereas in normal case it should be positioned to the omnibox. 

WontFix unless more deceptive attack is provided.


### ha...@gmail.com (2023-08-31)

This isn't a case of user not knowing whether fullscreen was entered, but tricking the user into thinking they exited fullscreen though once the user presses escape, so I am not sure why the prompt positioning comes into play here. The theoretical attack would be that the top Chrome UI only shows after Escape is pressed at which point the prompt is dismissed.

### ha...@gmail.com (2023-08-31)

[Comment Deleted]

### ha...@gmail.com (2023-08-31)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-08-31)

kerenzhu@, please see https://crbug.com/chromium/1477587#c7 for omnibox spoof and https://crbug.com/chromium/1477587#c6 for the PoC, going back to my point ---

Why would the prompt positioning be relevant here? It is expected that when the user enters fullscreen, that the prompt would be placed on the top left. And when pressing "Esc", this prompt will disappear so the prompt will not be anchored to the omnibox.

Furthermore, on Linux as mentioned in https://crbug.com/chromium/1477587#c2 pressing "Esc" will exit the fullscreen and dialog, on Windows that happens too.

### ha...@gmail.com (2023-08-31)

Sorry, new escape-spoof.html doesn't contain anything -- fixing..

### ha...@gmail.com (2023-08-31)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-08-31)

Thanks for the explanation. The setup of having the omnibox shows up after closing permission prompt looks much more deceptive to me. Reopen.

The fix will be to align mac's behavior with Linux and Window, that the fullscreen should exit and the permission prompt should close on a single esc press. 

### [Deleted User] (2023-08-31)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-15)

kerenzhu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2023-09-26)

Sorry, this seems to affect Windows too. Linux is not affected.

### ke...@chromium.org (2023-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

kerenzhu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-10-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

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

This issue was migrated from crbug.com/chromium/1477587?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>FullScreen, UI>Browser>Permissions>Prompts]
[Monorail components added to Component Tags custom field.]

### ke...@chromium.org (2024-10-10)

It seems that on Mac M129 and later, in content fullscreen, most permission requests won't trigger a permission bubble. Some permission requests (e.g. Screen Sharing) will force exit of fullscreen. This prevents the security issue described in this bug from happening.

(note that for user-triggered fullscreen, the permission bubbles is displayed just fine).

On Win M129, pressing Esc dismisses the bubble and exit fullscreen at the same time.

Closing, as this is no longer reproducible.

### pg...@google.com (2024-10-10)

thank you for the update!

changing status to Fixed, as we had confirmed this was reproducible at the time of report, but has since been fixed

### sp...@google.com (2024-11-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
$3,000 for report of lower impact security UI spoof


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-14)

Congratulations on another one, Axel! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2025-01-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $3,000 for report of lower impact security UI spoof

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071026)*
