# UAF in AutocompleteController::Observer

| Field | Value |
|-------|-------|
| **Issue ID** | [40071901](https://issues.chromium.org/issues/40071901) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | or...@chromium.org |
| **Created** | 2023-09-11 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

Analysis coming soon.

**Problem Description:**  

UAF in browser

**Additional Comments:**

\*\*Chrome version: \*\* 119.0.5998.0 \*\*Channel: \*\* Dev

**OS:** Mac OS

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 32.3 KB)
- [background.js](attachments/background.js) (text/plain, 182 B)
- [manifest.json](attachments/manifest.json) (text/plain, 274 B)
- [1.js](attachments/1.js) (text/plain, 575.8 KB)
- [2.js](attachments/2.js) (text/plain, 305.8 KB)
- [default.html](attachments/default.html) (text/plain, 123 B)
- [default.js](attachments/default.js) (text/plain, 447.6 KB)

## Timeline

### [Deleted User] (2023-09-11)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-09-11)

Thanks for the report. Marking this as Needs-Feedback pending more information about POC, details about how to trigger this, and what the security implications are.

At a glance, this is a heap UAF in Realbox code (the search box on the NTP) but it's unclear to me how an attacker could exploit it (i.e., likely user input only on a non-web page). Once we have more information we can finish triaging this.

### he...@gmail.com (2023-09-12)

# Initial RCA

When |autocomplete_controller_| is constructed in [1], it takes a backing pointer from the |OmniboxController|, e.g., the |RealboxHandler| in this case. |RealboxHandler| is also a member of the |OmniboxPopupUI| which binds with the |OmniboxController| [2]. The |autocomplete_controller_| and |RealboxHandler| observe |OmniboxController| [3] and when the |OmniboxController| is destructed, both |OmniboxController| and |OmniboxPopupUI| destroyed. However, seems that the destruction of |OmniboxController| could happen before |OmniboxPopupUI|. When |OmniboxPopupUI| is destroyed, i.e., the |RealboxHandler| member is destructed, it tries to remove itself from the freed observer |OmniboxController|, resulting in UAF.

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/omnibox/browser/omnibox_controller.cc;l=26-28;drc=5ca8523b8c9ff9a7b3e7eb349d8fc7566f660675

[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/omnibox_popup/omnibox_popup_ui.cc;l=70-72;drc=46a961c0e060305fefce1c0a824c52550b3a7440

[3] https://source.chromium.org/chromium/chromium/src/+/main:components/omnibox/browser/omnibox_controller.cc;l=34;drc=5ca8523b8c9ff9a7b3e7eb349d8fc7566f660675

### he...@gmail.com (2023-09-12)

Note that the initial RCA might not be correct. I discovered this UAF from my internal fuzzer. 

The original PoC from the fuzzer is purely loading the PoC extension on the Mac Chromium 119.0.5998.0 version. However, it is flaky and only have a success rate of 1/10 to reproduce it. Moreover, I fail to minimize it due to the flaky.

The ASAN stack seems that the root cause related with the observation lifetime of the autocomplete controller.

### ct...@chromium.org (2023-09-13)

Ah this is an extension triggering this on the NTP, that makes a bit more sense for how this could be triggerable. Could you attach the PoC extension (either as-is or once you are able to minimize some)?

### he...@gmail.com (2023-09-14)

Attach the original (partly minimized) extension PoC. It is quite flaky as mentioned above.

./chrome --load-extension=/path/to/ext --enable-features=WebUIOmniboxPopup --user-data-dir=/tmp/anything

### me...@chromium.org (2023-09-20)

I'm unable to repro using a debug Asan build and the files in https://crbug.com/chromium/1480915#c6. Instead of a UAF, I get a check failure:

[4019:4079:0920/193238.517421:FATAL:throttling_network_interceptor.cc(80)] Check failed: conditions_->download_throughput() != 0 || conditions_->upload_throughput() != 0. 

Assuming this is still a browser process UAF, it would be critical, but being flaky and requiring an extension should downgrade severity one level. 

mahmadi, could you PTAL? Any chance this is related to https://crbug.com/chromium/1451266?

[Monorail components: UI>Browser>Omnibox]

### [Deleted User] (2023-09-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2023-09-25)

[Empty comment from Monorail migration]

### do...@chromium.org (2023-09-25)

Impact=None as this needs a disabled feature to be enabled.

### or...@chromium.org (2023-10-04)

The asan.txt file attached to original report has OmniboxPopupPresenter in the stack, which suggests this may be related to the WebUI Omnibox Popup, which is very much still in the prototyping stage, gated behind a feature flag. But is it possible to repro without that feature enabled? NTP Realbox uses the RealboxHandler as well, and we did refactor observation of the AutocompleteController around the same time we worked on the WebUI Omnibox Popup prototype.

### ma...@chromium.org (2023-10-30)

orinj@ assigning to you in case you see similar reports and end up having a fix for the UAF.

### ma...@chromium.org (2023-10-30)

[Empty comment from Monorail migration]

### or...@chromium.org (2023-10-30)

[Empty comment from Monorail migration]

### or...@chromium.org (2023-10-30)

More debugging needed, but so far from looking at the logs, I'm guessing this may be caused by double destruction of a widget hierarchy. Might be related to this parent setting code:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/omnibox/omnibox_popup_presenter.cc;drc=f2b354e2ddf7cda8c5605c40ca056fa6040ef5d4;l=53

Browser already destroyed; then popup widget destroyed; destruction of root view reaches for the same root. Just a guess from trying to make sense of the logs. Will spend some time on repro to confirm or reject my guess, and hopefully find a clean fix.

### gi...@appspot.gserviceaccount.com (2023-11-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/45079176ea38506889f7d745b3ff64a1ebd5286e

commit 45079176ea38506889f7d745b3ff64a1ebd5286e
Author: Orin Jaworski <orinj@google.com>
Date: Mon Nov 06 17:23:09 2023

[omnibox][webui] Bind with SessionID to fix stale omnibox controller UAF

Bug: 1494334, 1480915
Change-Id: Iac98f22ce925c0d22419c3afb7604a8c59bd13c0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4998969
Commit-Queue: Orin Jaworski <orinj@chromium.org>
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Moe Ahmadi <mahmadi@chromium.org>
Reviewed-by: Orin Jaworski <orinj@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1220356}

[modify] https://crrev.com/45079176ea38506889f7d745b3ff64a1ebd5286e/chrome/browser/ui/views/omnibox/omnibox_popup_presenter.cc
[modify] https://crrev.com/45079176ea38506889f7d745b3ff64a1ebd5286e/chrome/browser/ui/webui/omnibox_popup/omnibox_popup_ui.h
[modify] https://crrev.com/45079176ea38506889f7d745b3ff64a1ebd5286e/chrome/browser/ui/webui/omnibox_popup/omnibox_popup_ui.cc


### he...@gmail.com (2023-11-11)

After running PoC repeatedly for 2 hours in the ToT chromium after the patch, it didn't reproduced and I could verify that this is fixed. Feel free to mark as fixed.

### or...@chromium.org (2023-11-13)

Great, thanks for verifying!

### [Deleted User] (2023-11-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-16)

Congratulations! The Chrome VRP Panel has decided to award you $5,000 for this report of a mildly mitigated security bug, mitigated by precondition to install a malicious extension with debugger permissions and race condition. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-11-18)

[Empty comment from Monorail migration]

### is...@google.com (2023-11-18)

This issue was migrated from crbug.com/chromium/1480915?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1486314, crbug.com/chromium/1494334]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071901)*
