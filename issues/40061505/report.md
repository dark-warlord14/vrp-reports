# UAF in ExtensionInstalledWaiter

| Field | Value |
|-------|-------|
| **Issue ID** | [40061505](https://issues.chromium.org/issues/40061505) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Mac |
| **Reporter** | ha...@gmail.com |
| **Assignee** | em...@chromium.org |
| **Created** | 2022-10-28 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**  

will attach details soon.

**Problem Description:**  

Browser UAF.

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.5384.0 \*\*Channel: \*\* Canary

**OS:** Mac OS

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 21.0 KB)

## Timeline

### ha...@gmail.com (2022-10-28)

I found this UAF accidently when I'm installing an online extension on Mac Chromium arm 109.0.5384.0 version. Seems that this is flaky and not stable to reproduce, please see the attached asan log for details.

## RCA

After initial investigation, I found that the root cause of this UAF seems clear. 

When we start to install an extension, the `ExtensionInstallUIDefault::ShowPlatformBubble` function [1] will be called. It binds the static `ShowUiOnToolbarMenu` function with the browser pointer as the done callback of the `ExtensionInstalledWaiter::WaitForInstall` function. 

In `ExtensionInstalledWaiter::WaitForInstall` function creates an self-destroyed instance of `ExtensionInstalledWaiter` [2]. Note that the `done_callback` of `ExtensionInstalledWaiter` is the aforementioned `ShowUiOnToolbarMenu` static function, bound with the browser pointer. In the constructor of `ExtensionInstalledWaiter`, it observes the `ExtensionRegistry` [3] of the extension loaded event. It will tries to call `ExtensionInstalledWaiter::RunCallbackIfExtensionInstalled()` once to see whether the extension is loaded at that time [5]. However, it has no affect if the extension hasn't been installed yet, i.e., the `IsExtensionInstalled` return false.  Then `ExtensionInstalledWaiter` will need to wait the observer to notify the extension loaded event.

When an extension is loaded, the observer will notify and calls `ExtensionInstalledWaiter::OnExtensionLoaded` function. `ExtensionInstalledWaiter::OnExtensionLoaded` function will posts a task, which bound the weak pointer with the `ExtensionInstalledWaiter::RunCallbackIfExtensionInstalled`. However, seems that the `ExtensionInstalledWaiter::OnExtensionRemovedOrBrowserClosed()` callback doesn't works (i.e., when the browser is closed, the waiter doesn't be destroyed in time), the weak pointer bound here has no affect to avoid lifetime problem. 

When the posted `ExtensionInstalledWaiter::RunCallbackIfExtensionInstalled` is scheduled, it will execute `done_callback_`. However, at this time, the browser pointer is invalid/freed, causing the UAF when the callbacks tries to access browser pointer in [7].



[1]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/extensions/extension_installed_bubble_view.cc;l=272-279;drc=50d8da971873550eb909b9c177cf6188e81ff4c3

void ExtensionInstallUIDefault::ShowPlatformBubble(
    scoped_refptr<const extensions::Extension> extension,
    Browser* browser,
    const SkBitmap& icon) {
  ExtensionInstalledWaiter::WaitForInstall(
      extension, browser,
      base::BindOnce(&ShowUiOnToolbarMenu, extension, browser, icon)); // [1] bind ShowUiOnToolbarMenu as callback
}

[2]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/extensions/extension_installed_waiter.cc;l=17-23;drc=50d8da971873550eb909b9c177cf6188e81ff4c3

// static
void ExtensionInstalledWaiter::WaitForInstall(
    scoped_refptr<const extensions::Extension> extension,
    Browser* browser,
    base::OnceClosure done_callback) {
  (new ExtensionInstalledWaiter(extension, browser, std::move(done_callback))) // [2]
      ->RunCallbackIfExtensionInstalled();
}

[3]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/extensions/extension_installed_waiter.cc;l=42-43;drc=50d8da971873550eb909b9c177cf6188e81ff4c3

ExtensionInstalledWaiter::ExtensionInstalledWaiter(
    scoped_refptr<const extensions::Extension> extension,
    Browser* browser,
    base::OnceClosure done_callback)
    : extension_(extension),
      browser_(browser),
      done_callback_(std::move(done_callback)) {
  extension_registry_observation_.Observe(
      extensions::ExtensionRegistry::Get(browser->profile())); // [3] observe the extension installation


[4]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/extensions/extension_installed_waiter.cc;l=78-81;drc=50d8da971873550eb909b9c177cf6188e81ff4c3

void ExtensionInstalledWaiter::OnExtensionLoaded(
    content::BrowserContext* browser_context,
    const extensions::Extension* extension) {
  if (extension != extension_.get())
    return;

  // Only call Wait() after all the other extension observers have had a chance
  // to run.
  base::ThreadTaskRunnerHandle::Get()->PostTask(
      FROM_HERE,
      base::BindOnce(&ExtensionInstalledWaiter::RunCallbackIfExtensionInstalled, // [4]
                     weak_factory_.GetWeakPtr()));
}

[5]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/extensions/extension_installed_waiter.cc;l=56;drc=50d8da971873550eb909b9c177cf6188e81ff4c3

void ExtensionInstalledWaiter::RunCallbackIfExtensionInstalled() {
  if (IsExtensionInstalled()) { // [5]
    std::move(done_callback_).Run(); // [5]
    delete this;
    return;
  }
}

[6]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/extensions/extension_installed_waiter.cc;l=84-86;drc=50d8da971873550eb909b9c177cf6188e81ff4c3

[7]https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/extensions/extension_installed_bubble_view.cc;l=267-269;drc=50d8da971873550eb909b9c177cf6188e81ff4c3


void ShowUiOnToolbarMenu(scoped_refptr<const extensions::Extension> extension,
                         Browser* browser,
                         const SkBitmap& icon) {
  ExtensionInstalledBubbleView::Show(
      browser, std::make_unique<ExtensionInstalledBubbleModel>(
                   browser->profile(), extension.get(), icon)); // [7] acccess the invalided `browser->profile()`
}

### [Deleted User] (2022-10-28)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-10-28)

Thanks for the report. This is a flaky UAF in browser process mitigated with user interaction so I'm assigning high severity.

emiliapaz, could you PTAL? I'll try to see if this reproes on stable. Thanks.

[Monorail components: Platform>Extensions]

### [Deleted User] (2022-10-29)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@chromium.org (2022-11-01)

To summarize: 

1. ShowPlatformBubble() creates an ExtensionInstalledWaiter to wait for the extension to finish installing with a callback ShowUiOnToolbarMenu that contains a pointer to the browser
2. ExtensionInstalledWaiter listens for extension loading (through extension registry observation) and browser closing (through extension removal watcher)
3a. If extension finishes loading, installed waiter is notified and it calls the callback
or
3b. If browser is closed, installed waiter is notified and it deletes itself

This was discussed in crbug.com/1281205. Bug was closed because ExtensionRemovalWatcher should be listening for browser closing and deleting the waiter before it listens for the loaded extension.

However, as reported in this bug that's not the case. There is some type of race condition and ExtensionRemovalWatcher notifying the browser closure happens after the load. I'll investigate this

### em...@chromium.org (2022-11-01)

I was not able to reproduce in Linux or Mac.

ExtensionRemovalWatcher::OnBrowserClosing(Browser* browser) should listen for browser closing before ExtensionInstalledWaiter listens for ExtensionRegistryObserver::OnExtensionLoaded. The window for this to happen has to be very small.

Unsure of why this race condition happens. Something that caught my attention is that we are listening for notifications in two places (waiter and watcher). The order where the observers are registered matters if they listen for the same call. For example: say both ExtensionInstalledWaiter and ExtensionRemovalWatcher listen for `OnExtensionLoaded`

class ExtensionInstalledWaiter : public extensions::ExtensionRegistryObserver {
  ExtensionInstalledWaiter(...) {
    extension_registry_observation_.Observe(extensions::ExtensionRegistry::Get(...);
    removal_watcher_ = std::make_unique<ExtensionRemovalWatcher>(...);
  }

  void OnExtensionLoaded(...) override {
     LOG(INFO) << "waiter: on extension loaded"   
  };  

 base::ScopedObservation<extensions::ExtensionRegistry,
                          extensions::ExtensionRegistryObserver>
      extension_registry_observation_{this};

  std::unique_ptr<ExtensionRemovalWatcher> removal_watcher_;
};

class ExtensionRemovalWatcher : public BrowserListObserver,
                                public extensions::ExtensionRegistryObserver {
  void OnExtensionLoaded(...) override {
     LOG(INFO) << "watcher: on extension loaded"   
  };  
}

When an extension is loaded, listeners are called a) waiter and then b) watcher.

While we don't have the same calls in the waiter and watcher, it could be adding more levels that make the browser listener be delayed in very specific cases. ExtensionRemovalWatcher is only used here, and its functionality can be moved directly to the waiter to a) remove not needed class, b) reduce confusion (no need to listen for extension registry observer in different places for same class)  and c) potentially fix not listening for browser or a race condition



### ad...@google.com (2022-11-03)

emiliapaz@ thanks for working on this. As the reporter says, the UAF is flaky, but the ASAN report shows there's a real bug. As you can't reproduce it, a speculative fix sounds like a good plan as you propose.

Has any code here changed lately? If not, please add the label FoundIn-106 so that our various triage bots know that this isn't a recent regression.

### gi...@appspot.gserviceaccount.com (2022-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2dc34b98e965a89418073ee0a200fbba7569ef91

commit 2dc34b98e965a89418073ee0a200fbba7569ef91
Author: Emilia Paz <emiliapaz@chromium.org>
Date: Thu Nov 03 17:49:59 2022

[Extensions] Listen for extension unloaded and browser closing in waiter

ExtensionInstalledWaiter listens for extension unloaded and browser
closed via an instance of ExtensionRemovalWatcher. The watcher was
introduced as a separate class because it was expected to be used by
other callers [1]. However, that is not the case and now it adds more
complexity.

Moved the observers to the waiter, and deleted the watcher class. No functionality changed.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/1965563/6..11/chrome/browser/ui/extensions/extension_tracker.h#b44

Bug: 1379242
Change-Id: Ieb92daf6e64679c996aeaa4097cf7eac2d84c62a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3997798
Commit-Queue: Emilia Paz <emiliapaz@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1067100}

[modify] https://crrev.com/2dc34b98e965a89418073ee0a200fbba7569ef91/chrome/browser/ui/extensions/extension_installed_waiter.h
[modify] https://crrev.com/2dc34b98e965a89418073ee0a200fbba7569ef91/chrome/browser/ui/extensions/extension_installed_waiter.cc
[delete] https://crrev.com/1c174f8519b2926ff3e621467b6aa282b4934f4a/chrome/browser/ui/extensions/extension_removal_watcher.cc
[modify] https://crrev.com/2dc34b98e965a89418073ee0a200fbba7569ef91/chrome/browser/ui/BUILD.gn
[delete] https://crrev.com/1c174f8519b2926ff3e621467b6aa282b4934f4a/chrome/browser/ui/extensions/extension_removal_watcher.h


### em...@chromium.org (2022-11-03)

happyercat@
a) Is there a way to reproduce it on ASAN? I tried this steps, but wasn't able to trigger the UAF:
  1. Setup gn args:
     is_asan = true
   is_debug = false 
  2. Build and run: $ASAN_OPTIONS=detect_odr_violation=0 out/asan/chrome
  3. Open an extension in CWS and click "Add to Chrome". Before extension loads, close the browser.
  NO UAF

b) Can you reproduce it after crrev.com/c/3997798 landed?


### ha...@gmail.com (2022-11-07)

Hello, thanks for the quick fix.

a) Seems that the racing window is narrow and the reproduction is indeed flaky. Sorry for that I currently failed to provide a stable reproduction.

b) I think the speculative fix crrev.com/c/3997798 sounds good. From the point of the previous analysis and the asan stack log, I think it fixes this UAF. Feel free to mark as fixed. Thank you.

### em...@chromium.org (2022-11-07)

SGTM. If you happen to encounter the UAF again please reopen the ticket (or file a new one).

### [Deleted User] (2022-11-07)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@chromium.org (2022-11-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-07)

[Empty comment from Monorail migration]

### ad...@google.com (2022-11-07)

Thanks for setting the label!

### [Deleted User] (2022-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-08)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-08)

Requesting merge to extended stable M106 because latest trunk commit (1067100) appears to be after extended stable branch point (1036826).

Requesting merge to stable M107 because latest trunk commit (1067100) appears to be after stable branch point (1047731).

Requesting merge to beta M108 because latest trunk commit (1067100) appears to be after beta branch point (1058933).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-08)

Merge review required: M108 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-08)

Merge review required: M107 is already shipping to stable.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-08)

Merge review required: M106 is already shipping to stable.

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

### em...@chromium.org (2022-11-08)

1. Why does your merge fit within the merge criteria for these milestones?
Fixes UFA

2. What changes specifically would you like to merge?
https://chromium-review.googlesource.com/c/chromium/src/+/3997798

3. Have the changes been released and tested on canary?
Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No


### am...@chromium.org (2022-11-11)

M108 merge approved, please merge this fix to branch 5359 by 12pm Pacific time Monday so this fix can be included in M108/Stable cut 

(there are no further planned releases of M107/stable and M106/extended, removing those merge labels) 

### sr...@google.com (2022-11-14)

Please help monitor and land the merge to M108 - I have CP'ed the merge here - https://chromium-review.googlesource.com/c/chromium/src/+/4025775

### gi...@appspot.gserviceaccount.com (2022-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/92f1dd89d7857966649536422384ae6b987af59d

commit 92f1dd89d7857966649536422384ae6b987af59d
Author: Emilia Paz <emiliapaz@chromium.org>
Date: Mon Nov 14 19:17:41 2022

[Extensions] Listen for extension unloaded and browser closing in waiter

ExtensionInstalledWaiter listens for extension unloaded and browser
closed via an instance of ExtensionRemovalWatcher. The watcher was
introduced as a separate class because it was expected to be used by
other callers [1]. However, that is not the case and now it adds more
complexity.

Moved the observers to the waiter, and deleted the watcher class. No functionality changed.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/1965563/6..11/chrome/browser/ui/extensions/extension_tracker.h#b44

(cherry picked from commit 2dc34b98e965a89418073ee0a200fbba7569ef91)

Bug: 1379242
Change-Id: Ieb92daf6e64679c996aeaa4097cf7eac2d84c62a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3997798
Commit-Queue: Emilia Paz <emiliapaz@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1067100}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4025775
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#820}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/92f1dd89d7857966649536422384ae6b987af59d/chrome/browser/ui/extensions/extension_installed_waiter.h
[modify] https://crrev.com/92f1dd89d7857966649536422384ae6b987af59d/chrome/browser/ui/extensions/extension_installed_waiter.cc
[delete] https://crrev.com/e3d2acd64a3076c09107521ac6ecd6e79c341f8f/chrome/browser/ui/extensions/extension_removal_watcher.cc
[modify] https://crrev.com/92f1dd89d7857966649536422384ae6b987af59d/chrome/browser/ui/BUILD.gn
[delete] https://crrev.com/e3d2acd64a3076c09107521ac6ecd6e79c341f8f/chrome/browser/ui/extensions/extension_removal_watcher.h


### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-17)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug. Thank you for your efforts in reporting this issue to us! 

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1379242?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061505)*
