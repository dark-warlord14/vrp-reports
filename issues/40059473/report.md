# AddressSanitizer: heap-use-after-free in PermissionRequestChip::CreateBubble

| Field | Value |
|-------|-------|
| **Issue ID** | [40059473](https://issues.chromium.org/issues/40059473) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2022-04-26 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

The root cause of the problem is very clear by reading the code and asan log, now I am looking for a stable way to reproduce

**Problem Description:**

1. In function PermissionRequestChip::CreateBubble the PermissionPromptBubbleView object will be created and the prompt\_bubble->Show()[1] method will be called
2. During the execution of the Show method, resize may be triggered to cause the PermissionRequestChip to be freed, which will eventually lead to UAF at[2]

```
chrome/browser/ui/views/location_bar/permission_chip.cc:113  
views::View\* PermissionRequestChip::CreateBubble() {  
  PermissionPromptBubbleView\* prompt_bubble = new PermissionPromptBubbleView(  
      browser_, delegate(), chip_shown_time_, PermissionPromptStyle::kChip);  
  prompt_bubble->SetOnBubbleDismissedByUserCallback(base::BindOnce(  
      &PermissionRequestChip::OnPromptBubbleDismissed, base::Unretained(this)));  
  prompt_bubble->Show();							<<---[1]  
  prompt_bubble->GetWidget()->AddObserver(this);	<<---[2]  
  
  RecordChipButtonPressed();  
  
  return prompt_bubble;  
}  
  

```

=================================================================  

==12752==ERROR: AddressSanitizer: heap-use-after-free on address 0x122f8c0b7e18 at pc 0x7ffa8a1f126d bp 0x0096d6bfe160 sp 0x0096d6bfe1a8  

READ of size 8 at 0x122f8c0b7e18 thread T0  

==12752==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffa8a1f126c in base::internal::CheckedObserverAdapter::CheckedObserverAdapter C:\b\s\w\ir\cache\builder\src\base\observer\_list\_internal.cc:11  

#1 0x7ffa89fd7396 in base::ObserverList[views::WidgetObserver,0,1,base::internal::CheckedObserverAdapter](javascript:void(0);)::AddObserver C:\b\s\w\ir\cache\builder\src\base\observer\_list.h:279  

#2 0x7ffa89fd724a in views::Widget::AddObserver C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:461  

#3 0x7ffa94a6e1aa in PermissionRequestChip::CreateBubble C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\location\_bar\permission\_request\_chip.cc:119  

#4 0x7ffa94a71c90 in PermissionChip::ExpandAnimationEnded C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\location\_bar\permission\_chip.cc:206  

#5 0x7ffa8addf093 in gfx::LinearAnimation::Step C:\b\s\w\ir\cache\builder\src\ui\gfx\animation\linear\_animation.cc:88  

#6 0x7ffa8d9dd73b in gfx::AnimationContainer::Run C:\b\s\w\ir\cache\builder\src\ui\gfx\animation\animation\_container.cc:99  

#7 0x7ffa911ba62e in gfx::AnimationRunner::Step C:\b\s\w\ir\cache\builder\src\ui\gfx\animation\animation\_runner.cc:78  

#8 0x7ffa89ff8d2e in ui::Compositor::BeginMainFrame C:\b\s\w\ir\cache\builder\src\ui\compositor\compositor.cc:691  

#9 0x7ffa8fed524c in cc::SingleThreadProxy::DoBeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\single\_thread\_proxy.cc:1048  

#10 0x7ffa8fed71ec in cc::SingleThreadProxy::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\single\_thread\_proxy.cc:1010  

#11 0x7ffa8fed8850 in base::internal::Invoker<base::internal::BindState<void (cc::SingleThreadProxy::\*)(const viz::BeginFrameArgs &),base::WeakPtr[cc::SingleThreadProxy](javascript:void(0);),viz::BeginFrameArgs>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:748  

#12 0x7ffa8a2a8544 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#13 0x7ffa8d14bfc5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:386  

#14 0x7ffa8d14b599 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:291  

#15 0x7ffa8a35c2b6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#16 0x7ffa8a35a5f8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#17 0x7ffa8d14d780 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:498  

#18 0x7ffa8a21ab27 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#19 0x7ffa82f9352b in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1067  

#20 0x7ffa82f98987 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:157  

#21 0x7ffa82f8c989 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#22 0x7ffa89e45c53 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:659  

#23 0x7ffa89e48dcc in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1166  

#24 0x7ffa89e47efe in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1038  

#25 0x7ffa89e448cb in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_

**Additional Comments:**

\*\*Chrome version: \*\* 100.0.4896.127 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 16.7 KB)

## Timeline

### dt...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox]

### [Deleted User] (2022-04-26)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-26)

+elklm: can you look at this? Assigning High severity as this is a browser process UaF, but needs user interaction in the form of a resize while a permission request is open (though I think this is probably on the boundary between Critical and High as permission prompts do show up reasonably often).

[Monorail components: UI>Browser>Permissions>Prompts]

### [Deleted User] (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-27)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2022-04-27)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-04-28)

CC'ing desktop UI folks to help us interpret the Windows-specific parts of the second stack trace (i.e. "freed by thread T0 here") in the attached `asan.txt` file.

Our understanding is that the first and second stack traces are from the very same invocation to PermissionRequestChip::CreateBubble(), where immediately after one another:
  (1) We try to show a bubble in PermissionPromptBubbleView::Show.
  (2) Add an observer to the new widget using views::Widget::AddObserver.

After (1), some re-layouts and some interactions with HWNDMessageHandler take place that we don't fully understand, and as a result of those interactions, we get into a state where the location bar gets hidden (at least that is our hypothesis). This results in PermissionRequestManager destroying, in a reentrant fashion, the PermissionRequestChip, so that when it starts observing the Widget in (2), it is already gone.

Can you help us understand better the circumstances under which showing a widget can hide the location bar in such a synchronous fashion? Obviously the fix will be more generic than that, but to correctly estimate the severity of the issue, and to verify our fix, it would be critical to understand how the issue can be reproduced.

### pk...@chromium.org (2022-04-28)

Repro: Visit permission.site in a debug browser, go fullscreen with F11, then click one of the buttons (e.g. "Camera") to trigger a permission request.  I get a segfault.

### pk...@chromium.org (2022-04-28)

I suspect we need to change hwnd_message_handler.cc:1354 to add something like `... && hwnd() != ::GetWindow(window_gaining_or_losing_activation, GW_OWNER)`.  We probably shouldn't kick out of fullscreen mode when losing activation to our own child.

### en...@chromium.org (2022-04-28)

Thanks, Peter, I can repro that.

Looks like there is logic error where we don't check if the location bar is visible before trying to show the permission chip (we do check it for other flavors of the UI). This resulted in my initial analysis being incorrect in assuming that we were entering fullscreen simultaneously to the bubble being opened. In reality, we were in full-screen to start with.

### el...@chromium.org (2022-04-29)

Thank you Peter, it is extremely helpful. 

You are probably looking for a change made after 976003 (known good), but no later than 976028 (first known bad).
CHANGELOG URL:
  https://chromium.googlesource.com/chromium/src/+log/777a31ab45bead36c83f22eb04749425115a0b70..995625cbe461240b136c33b501eaf9a2ce2c597e

Potential culprit CL https://chromium-review.googlesource.com/c/chromium/src/+/3485642

### el...@chromium.org (2022-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-29)

The older reward-topanel https://crbug.com/chromium/1305523 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### ky...@chromium.org (2022-04-29)

Some more information on this one. First of all, this requires that all the following experiment flags to be enabled:

permission-chip, permission-chip-gesture, permission-chip-request-type

The browser must also be in full-screen mode (F11).

What is happening is when PermissionRequestChip::ShowBubble() is called, upon return from prompt_bubble_->Show();, |this| will have been destroyed.

There are a couple of ways to fix this, one is localized to the permission request classes, the other involves slight changes to full-screen mode behavior. The former being a safer fix than the latter.

For the permission request fix, the PermissionChip class would need to track it's own deletion and quickly exit all the methods without "touching" |this|.

The other fix would change the Windows full_screen_handler() behavior when a bubble is shown over a full-screen browser. Could certainly introduce more regressions.


### gi...@appspot.gserviceaccount.com (2022-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4ee270c3650e0ac81be73dceb664e073e2c01ce0

commit 4ee270c3650e0ac81be73dceb664e073e2c01ce0
Author: Illia Klimov <elklm@google.com>
Date: Fri Apr 29 20:28:25 2022

Do not create PermissionRequestChip in fullscreen mode.

Bug: 1319797,1316452,1321086
Change-Id: Ie5b66accd922f2443cf537e664d4ecbbe2866e70
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3613373
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Cr-Commit-Position: refs/heads/main@{#997887}

[modify] https://crrev.com/4ee270c3650e0ac81be73dceb664e073e2c01ce0/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc
[modify] https://crrev.com/4ee270c3650e0ac81be73dceb664e073e2c01ce0/chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view.cc


### do...@chromium.org (2022-04-30)

Thanks for fixing the issue!

+cc amyressler +cc adetaylor for VRP discussion between this and the merged-in https://crbug.com/chromium/1305523. To me, the conclusion that the fix in https://crbug.com/chromium/1305523 was for a more contrived version of this actual underlying bug makes sense. That is, we should consider this bug for VRP, but not https://crbug.com/chromium/1305523.

### en...@chromium.org (2022-04-30)

Re: https://crbug.com/chromium/1319797#c15: 
 (1) Agreed with the recommendation in favor of a localized fix. This has now been landed in crrev.com/c/3613373.
 (2) You are correct that this requires PermissionRequestChip-related experiment flags to be enabled. Note, however, that the necessary flags used to be enabled by a 1% Stable experiment that we had been running for M98+. On 4/28 we terminated this experiment, therefore as of now, the issue has now minimal stable/extended impact, albeit non-zero, as some users will be lagging behind to update that field trial state.
 (3) You are also correct that the browser needs to be in full-screen mode, note, however, that it can be content-initiated full-screen, so unfortunately that is not much of a mitigating factor here.

Re: https://crbug.com/chromium/1319797#c17, that is an accurate characterization of the situation, thank you!

Requesting merges to Beta/Stable/Extended channels. Amy, please see caveat (2) above when reviewing.

### [Deleted User] (2022-04-30)

Merge review required: M102 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-30)

Merge review required: M101 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-30)

Merge review required: M100 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-02)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-05-03)

1. Why does your merge fit within the merge criteria for these milestones?
Security UAF crash.
2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3613373
3. Have the changes been released and tested on canary?
Yes. Landed on 103.0.5034.0, no new crashes since that.
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
Not a feature, bug fix. 
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
The crash is not longer effects stable as the feature was disabled. It should be manually 
Steps:
1. Install Chrome version 103.0.5034.0 and above on Windows. (other OSs are not affected)
2. Enable these experiments: permission-chip, permission-chip-gesture, permission-chip-request-type
3. Navigate to https://permission.site/ and verify that no permissions are granted.
4. Enter full screen via F11, 
5. Request permissions. (MIDI or Camera or Geolocation). There should be no crash

### am...@chromium.org (2022-05-03)

Thank you engedy@ for the info in https://crbug.com/chromium/1319797#c18 given the impact and minor mitigation of full screen mode requirement, and that some users may still be in field experiment, I believe we should backmerge this fix to the active release channels. 
M102 merge approved, please merge this fix to 5005 at your earliest convenience. 
M101 and M100 merges approved, please merge this fix to branches 4951 and 4896 respectively (nlt EOD Friday, 6 May) so this fix can be included in the next security refresh for Stable and Extended Stable. 

### gi...@appspot.gserviceaccount.com (2022-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f5c8a150a47f6270ef58085a55992d6f67ca16a3

commit f5c8a150a47f6270ef58085a55992d6f67ca16a3
Author: Illia Klimov <elklm@google.com>
Date: Tue May 03 16:33:30 2022

Do not create PermissionRequestChip in fullscreen mode.

(cherry picked from commit 4ee270c3650e0ac81be73dceb664e073e2c01ce0)

Bug: 1319797,1316452,1321086
Change-Id: Ie5b66accd922f2443cf537e664d4ecbbe2866e70
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3613373
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#997887}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3623902
Cr-Commit-Position: refs/branch-heads/5005@{#389}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/f5c8a150a47f6270ef58085a55992d6f67ca16a3/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc
[modify] https://crrev.com/f5c8a150a47f6270ef58085a55992d6f67ca16a3/chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view.cc


### [Deleted User] (2022-05-03)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f7b42a885d5831f5c4d7bd5f71d1f4b833473d9f

commit f7b42a885d5831f5c4d7bd5f71d1f4b833473d9f
Author: Illia Klimov <elklm@google.com>
Date: Tue May 03 16:34:02 2022

Do not create PermissionRequestChip in fullscreen mode.

(cherry picked from commit 4ee270c3650e0ac81be73dceb664e073e2c01ce0)

Bug: 1319797,1316452,1321086
Change-Id: Ie5b66accd922f2443cf537e664d4ecbbe2866e70
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3613373
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#997887}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3623668
Cr-Commit-Position: refs/branch-heads/4951@{#1152}
Cr-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}

[modify] https://crrev.com/f7b42a885d5831f5c4d7bd5f71d1f4b833473d9f/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc
[modify] https://crrev.com/f7b42a885d5831f5c4d7bd5f71d1f4b833473d9f/chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view.cc


### gi...@appspot.gserviceaccount.com (2022-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/533df6600f4af1d7099117b0b69ee22ab24ffdc4

commit 533df6600f4af1d7099117b0b69ee22ab24ffdc4
Author: Illia Klimov <elklm@google.com>
Date: Tue May 03 16:36:39 2022

Do not create PermissionRequestChip in fullscreen mode.

(cherry picked from commit 4ee270c3650e0ac81be73dceb664e073e2c01ce0)

Bug: 1319797,1316452,1321086
Change-Id: Ie5b66accd922f2443cf537e664d4ecbbe2866e70
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3613373
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#997887}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3623583
Cr-Commit-Position: refs/branch-heads/4896@{#1217}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/533df6600f4af1d7099117b0b69ee22ab24ffdc4/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc
[modify] https://crrev.com/533df6600f4af1d7099117b0b69ee22ab24ffdc4/chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view.cc


### rz...@google.com (2022-05-03)

[Empty comment from Monorail migration]

### rz...@google.com (2022-05-04)

Feature not needed, feature not available on M96.

### am...@google.com (2022-05-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-06)

Thank you for this report! Given that this issue was not demonstrated to be exploitable and the ability to reproduce and user gesture to do trigger was discovered by the developers, the VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and taking the time to report this issue to us. 

### m....@gmail.com (2022-05-06)

Thanks Amy.

I agree that the exploit window is very small。

Although I did not provide a method to reproduce this issue when I reported it, I provided an analysis of the root cause of the issue, which has basically determined the root cause of the issue. 
And this user interaction is easy to do as I explained here https://bugs.chromium.org/p/chromium/issues/detail?id=1305523#c6.

So I hope the VRP team will re-evaluate the bounty.

### am...@chromium.org (2022-05-06)

Thanks for pointing that out. Regardless, given the level of user interaction and the low-exploitability, this is comparable with the reward amounts for similar reports mitigated by user gesture and both reports were evaluated for reward amount. 

Happy to bring this back through a process for a re-evaluation, but without additional information or demonstration of this issue having higher potential exploitability, the reward amount is unlikely to be adjusted. 

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1319797?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Omnibox, UI>Browser>Permissions>Prompts]
[Monorail mergedwith: crbug.com/chromium/1305523]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059473)*
