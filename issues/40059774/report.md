# Security: UAF in PermissionPromptBubbleView

| Field | Value |
|-------|-------|
| **Issue ID** | [40059774](https://issues.chromium.org/issues/40059774) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Views, UI>Browser>Permissions>Prompts |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2022-05-27 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

The life cycle of `PermissionRequestManager`[1] is bound to `WebContents`. It will save itself[2] as a raw pointer `delegate_`[3] and could be destroyed before `PermissionPromptBubbleView`.

After making the replacement from `OnWidgetClosing` to `OnWidgetDestroyed`[4], the task `SerializeTreeUpdates`[5] could be run after `PermissionRequestManager` gets destroyed, but before `OnWidgetDestroyed` is run asynchronously. Accessing[6] the delegate will trigger the uaf.

And this bug is different from [7].

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_request_manager.h;l=70;drc=d48ea0e86f5ecc4e8b08915197652671a4203312>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_request_manager.cc;l=709;drc=67172ba3828a038c491384620c3f854bd6d0ece9>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view.h;l=96;drc=67172ba3828a038c491384620c3f854bd6d0ece9;bpv=1;bpt=1>  

[4]. <https://chromium-review.googlesource.com/c/chromium/src/+/3648307>  

[5]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/views_ax_tree_manager.cc;l=119;drc=c2edca82e19d2a4809bb7dcbdd6c3bfc010e645c>  

[6]. <https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/ax_widget_obj_wrapper.cc;l=48;drc=c18d28eeccef8b4b63e541f84ab5a75eb3b34f69>  

[7]. <https://chromium-review.googlesource.com/c/chromium/src/+/3665781>

NOTE: This bug is NOT reliant on profile destruction. `window.close` in poc aims to close current WebContent rather than the entire browser.

**VERSION**  

Chrome Version: head with AccessibilityTreeForViews

**REPRODUCTION CASE**  

$ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-features=AccessibilityTreeForViews "<http://localhost:8000/poc.html>"  

Click the trigger button.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 13.5 KB)
- [poc.html](attachments/poc.html) (text/plain, 360 B)
- [poc_new.html](attachments/poc_new.html) (text/plain, 510 B)

## Timeline

### [Deleted User] (2022-05-27)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-05-28)

Unfortunately this poc.html doesn't reproduce because "scripts may close only the windows that were opened by them". Do you have an alternate way of destroying the web contents?

### le...@gmail.com (2022-05-28)

Three solutions:

1. Run `$ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-features=AccessibilityTreeForViews "http://localhost:8000/poc.html" ` in terminal.

2. Use `poc_new.html`. Click the trigger button to open a new tab. Then click the button in the new tab to trigger.

3. Patch the code to simulate a compromised renderer to solve this limitation:

diff --git a/third_party/blink/renderer/core/frame/dom_window.cc b/third_party/blink/renderer/core/frame/dom_window.cc
index 6ef9baba740..900007718e5 100644
--- a/third_party/blink/renderer/core/frame/dom_window.cc
+++ b/third_party/blink/renderer/core/frame/dom_window.cc
@@ -399,22 +399,22 @@ void DOMWindow::Close(LocalDOMWindow* incumbent_window) {
       WebFeature::kWindowProxyCrossOriginAccessClose,
       WebFeature::kWindowProxyCrossOriginAccessFromOtherPageClose);

-  Settings* settings = GetFrame()->GetSettings();
-  bool allow_scripts_to_close_windows =
-      settings && settings->GetAllowScriptsToCloseWindows();
-
-  if (!page->OpenedByDOM() && GetFrame()->Client()->BackForwardLength() > 1 &&
-      !allow_scripts_to_close_windows) {
-    active_document->domWindow()->GetFrameConsole()->AddMessage(
-        MakeGarbageCollected<ConsoleMessage>(
-            mojom::ConsoleMessageSource::kJavaScript,
-            mojom::ConsoleMessageLevel::kWarning,
-            "Scripts may close only the windows that were opened by them."));
-    return;
-  }
-
-  if (!GetFrame()->ShouldClose())
-    return;
+  // Settings* settings = GetFrame()->GetSettings();
+  // bool allow_scripts_to_close_windows =
+  //     settings && settings->GetAllowScriptsToCloseWindows();
+
+  // if (!page->OpenedByDOM() && GetFrame()->Client()->BackForwardLength() > 1 &&
+  //     !allow_scripts_to_close_windows) {
+  //   active_document->domWindow()->GetFrameConsole()->AddMessage(
+  //       MakeGarbageCollected<ConsoleMessage>(
+  //           mojom::ConsoleMessageSource::kJavaScript,
+  //           mojom::ConsoleMessageLevel::kWarning,
+  //           "Scripts may close only the windows that were opened by them."));
+  //   return;
+  // }
+
+  // if (!GetFrame()->ShouldClose())
+  //   return;

   ExecutionContext* execution_context = nullptr;
   if (auto* local_dom_window = DynamicTo<LocalDOMWindow>(this)) {

### [Deleted User] (2022-05-28)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2022-05-30)

Thanks, poc_new.html was able to reproduce it very cleanly.

Since AccessibilityTreeForViews is off by default, setting Security_Impact-None. But it's browser process memory corruption with a single click, so adding severity critical. kylixrd@, dtseng@ - this definitely needs to be fixed before enabling AccessibilityTreeForViews anywhere, but doesn't need the urgent action that a normal critical severity vulnerability would merit.

[Monorail components: Internals>Views]

### ad...@google.com (2022-05-30)

(auto-cc on security bug)

### ky...@chromium.org (2022-06-08)

Reassigning to elklm@. This might be solved by the current refactoring going on here: https://chromium-review.googlesource.com/c/chromium/src/+/3644569

### le...@gmail.com (2022-06-09)

Unfortunately, this refactoring has nothing to do with this issue. In my local tests, the UAF can still be triggered after this refactoring.

### el...@chromium.org (2022-06-09)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-06-09)

Illia, this affects all prompt disposition types, right?

### el...@chromium.org (2022-06-13)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-06-13)

I was able to reproduce the crash without patching the code https://crbug.com/chromium/1329814#c3

@engedy - it affects all types that can end up in the default permission prompt bubble. So the default prompt and the normal chip. The quiet chip does not use PermissionPromptBubbleView, so it is not affected.

@kylixrd is that right that `AccessibilityTreeForViews` is a requirement for that? From my understanding, `OnWidgetDestroyed` is always async so we can get UAF even without the flag?

### pb...@chromium.org (2022-06-13)

Is the real problem here that `delegate_` doesn't outlive PermissionPromptBubbleView but PermissionPromptBubbleView is not notified of its destruction? This is just one path that tickles a UAF, but any other call could've done it.

From the asan stack it looks like this outlives the WebContents it's attached to, so you probably can't fix this by re-querying the WebContents for data. Should this store a WeakPtr to PermissionRequestManager which already has a WeakPtrFactory?

### el...@chromium.org (2022-06-13)

When tab is closing:
1. `PermissionRequestManager::OnVisibilityChanged` calls `PermissionRequestManager::DeleteBubble()` [1]
2. It ends up in `PermissionPromptImpl::~PermissionPromptImpl()` [2]
3. And it calls `PermissionPromptImpl::CleanUpPromptBubble()` [3]

My assumption that `widget->CloseWithReason` was previously destroying a widget and which was destroying `PermissionPromptBubbleView`. But now it does not do it, or at least it does not do it synchronously. So the `delegate_` gets destroyed but the view object and the widget still exist and it causes UAF. 

I see 2 options:
1. Use WeakPtr as suggested in https://crbug.com/chromium/1329814#c13 
2. Change `PermissionPromptBubbleView` is finalized

It feels like we should change how `PermissionPromptBubbleView` gets finalized so that everything is destroyed before `PermissionRequestManager` and not after. Is my understanding correct?

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/permissions/permission_request_manager.cc;l=433;drc=f51c47ef6c37f12d898997ba00010eb7fba0d090;bpv=1;bpt=1
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc;l=149;drc=0efb6d773049903754513a26452384975fd06740
[3] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc;l=243-249;drc=0efb6d773049903754513a26452384975fd06740

### dr...@chromium.org (2022-06-13)

[Empty comment from Monorail migration]

### el...@chromium.org (2022-06-14)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Permissions>Prompts]

### el...@chromium.org (2022-06-14)

[Empty comment from Monorail migration]

### el...@google.com (2022-06-23)

[Empty comment from Monorail migration]

### aj...@google.com (2022-06-25)

[Empty comment from Monorail migration]

### el...@google.com (2022-07-02)

[Empty comment from Monorail migration]

### ka...@chromium.org (2022-07-02)

[ChromeOS Stability Triage]
Thank you for cc'ing me! Since this is a duplicated of a bug linked to a high frequency crash, I am copying relevant labels here and making this a release blocker.

62 crashes from 48 unique clients in 104.0.5112.23
Frequency: 175 CPMH (http://go/cros-crash-rate-graph?f=signature:in:permissions%3A%3APermissionRequestManager%3A%3AGetRequestingOrigin)

#5 top crash of severity=FATAL (https://data.corp.google.com/sites/cros-ui-stability-triage/m104)

Please prioritize the fix by M104 stable (http://go/cros-ui-stability-slo)



### [Deleted User] (2022-07-03)

[Empty comment from Monorail migration]

### el...@google.com (2022-07-05)

In Review CL: https://chromium-review.googlesource.com/c/chromium/src/+/3738748

### el...@google.com (2022-07-05)

[Empty comment from Monorail migration]

### el...@google.com (2022-07-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0c85c0795b4830a77add242eb54ee7ba36ea5a0f

commit 0c85c0795b4830a77add242eb54ee7ba36ea5a0f
Author: Andy Paicu <andypaicu@chromium.org>
Date: Mon Jul 11 10:53:15 2022

Avoid using |delegate_| after the PermissionPromptBubbleView constructor.

When a tab is closed and WebContents is destroyed, a permission prompt bubble view will be finalized asynchronously. That can lead to a situation, where the view calls into freed WebContents.

More details: https://docs.google.com/document/d/1Ou320Q_O6iEVTI-EnhVzcSgheYwZ7tFow5mH2kA0-ZY/edit?resourcekey=0-2f8-Wmg-8avrewv1Om7MFA#heading=h.6qqfv5apsb0k

Bug: 1329814
Change-Id: Icdfadb79d7e08c13a2d077a142fd3d48d5a14eb6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3738748
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Reviewed-by: Olesia Marukhno <olesiamarukhno@google.com>
Cr-Commit-Position: refs/heads/main@{#1022643}

[modify] https://crrev.com/0c85c0795b4830a77add242eb54ee7ba36ea5a0f/chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view.h
[modify] https://crrev.com/0c85c0795b4830a77add242eb54ee7ba36ea5a0f/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc
[modify] https://crrev.com/0c85c0795b4830a77add242eb54ee7ba36ea5a0f/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/0c85c0795b4830a77add242eb54ee7ba36ea5a0f/chrome/browser/ui/permission_bubble/permission_bubble_browser_test_util.cc
[modify] https://crrev.com/0c85c0795b4830a77add242eb54ee7ba36ea5a0f/chrome/browser/ui/views/location_bar/permission_chip_unittest.cc
[modify] https://crrev.com/0c85c0795b4830a77add242eb54ee7ba36ea5a0f/chrome/browser/ui/permission_bubble/permission_bubble_browser_test_util.h
[modify] https://crrev.com/0c85c0795b4830a77add242eb54ee7ba36ea5a0f/components/permissions/permission_request_manager.h
[modify] https://crrev.com/0c85c0795b4830a77add242eb54ee7ba36ea5a0f/components/permissions/permission_prompt.h
[modify] https://crrev.com/0c85c0795b4830a77add242eb54ee7ba36ea5a0f/chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view.cc
[modify] https://crrev.com/0c85c0795b4830a77add242eb54ee7ba36ea5a0f/chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view_unittest.cc
[modify] https://crrev.com/0c85c0795b4830a77add242eb54ee7ba36ea5a0f/chrome/browser/ui/views/location_bar/permission_request_chip.cc


### el...@google.com (2022-07-11)

Market as fixed as with the above CL I'm no longer able to reproduce the crash locally. 

### [Deleted User] (2022-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-12)

Merge review required: M104 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@google.com (2022-07-12)


Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
Critical security UAF bug.
2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3738748
3. Have the changes been released and tested on canary?
Yes.
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
N/A
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
- Run `python3 -m http.server`
- chrome --user-data-dir=/tmp/xxxx --enable-features=AccessibilityTreeForViews "http://localhost:8000/poc.html" 
-- Use `poc_new.html`. Click the trigger button to open a new tab. Then click the button in the new tab to trigger.
- poc.html use from https://crbug.com/chromium/1329814#c3

### [Deleted User] (2022-07-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-12)

Hi Illia, thanks for landing this fix for this critical issue. I see that you added a merge request for this issue which is currently SI-None. Is AccessibilityTreesforViews in an active release channel in the near term? If not, we should just let this fix matriculate through the natural merge and release progression. If so, happy to re-review for merge approval.  

### el...@google.com (2022-07-13)

[Empty comment from Monorail migration]

### el...@google.com (2022-07-13)

Hi Amy, there are a few points to clarify:
 – The repro steps in the original report require the `AccessibilityTreeForViews` feature to be manually enabled, and I was not able to reproduce the crash without it.
 – However, we were independently notified (1333989, 1330228) that there are a number of crash reports [1] with the same crash stack trace on CrOS. These do not seem to have the `AccessibilityTreeForViews` flag explicitly enabled. We suspect there might be some other mechanism that turns on the flag on CrOS/Lacros by default (in which case the security impact is no longer none), or there is some other code path activates the same faulty A11Y logic (in which case we are talking about a variant of this security bug that does not require the flag and thus has more than none impact).
 – Based on both static code analysis, as well as the crash report, we suspect that the regression on our end occurred in M104 [2], and CrOS release managers would also like to see the crashers fixed in this release (see comment https://crbug.com/chromium/1329814#c21).
With that we would like to request a merge to M104. Please let us know if we should track the merge on this security bug, or if we should file a separate bug for that.

[1] https://crash.corp.google.com/browse?q=EXISTS+%28SELECT+1+FROM+UNNEST%28CrashedStackTrace.StackFrame%29+WHERE+FunctionName+LIKE+%27%25PermissionPromptBubbleView%3A%3AGetAccessibleWindowTitle%25%27%29+AND+product_name%3D%27Chrome_ChromeOS%27#+samplereports:25,productname:1000,productversion:120,magicsignature:1000,magicsignature2:50,stablesignature:50,clientid:500,day:100,hour:30

[2] https://chromium-review.googlesource.com/c/chromium/src/+/3651103


### [Deleted User] (2022-07-13)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-13)

Hi Illia, thanks for that context. I completely missed https://crbug.com/chromium/1329814#c21 in my evaluation, so thank you for pointing that out as additional background. I think between your https://crbug.com/chromium/1329814#c34 and that, there is enough context here to show display the need for merging this fix to M104 at this time rather than following the standard process for features not yet enabled. 
All that being said, M104 merge approved, please merge this fix to branch 5112 at your earliest convenience.

### am...@google.com (2022-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-13)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $20,000 for this report. Thank you for your efforts and great work! 

### el...@google.com (2022-07-14)

[Empty comment from Monorail migration]

### el...@google.com (2022-07-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/64b85f04feefb13873d98ad43a159ca1dfa91b62

commit 64b85f04feefb13873d98ad43a159ca1dfa91b62
Author: Andy Paicu <andypaicu@chromium.org>
Date: Thu Jul 14 08:13:55 2022

Avoid using |delegate_| after the PermissionPromptBubbleView constructor.

When a tab is closed and WebContents is destroyed, a permission prompt bubble view will be finalized asynchronously. That can lead to a situation, where the view calls into freed WebContents.

More details: https://docs.google.com/document/d/1Ou320Q_O6iEVTI-EnhVzcSgheYwZ7tFow5mH2kA0-ZY/edit?resourcekey=0-2f8-Wmg-8avrewv1Om7MFA#heading=h.6qqfv5apsb0k

(cherry picked from commit 0c85c0795b4830a77add242eb54ee7ba36ea5a0f)

Bug: 1329814
Change-Id: Icdfadb79d7e08c13a2d077a142fd3d48d5a14eb6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3738748
Commit-Queue: Illia Klimov <elklm@chromium.org>
Reviewed-by: Dominick Ng <dominickn@chromium.org>
Reviewed-by: Olesia Marukhno <olesiamarukhno@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1022643}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3757862
Owners-Override: Theodore Olsauskas-Warren <sauski@google.com>
Commit-Queue: Theodore Olsauskas-Warren <sauski@google.com>
Reviewed-by: Theodore Olsauskas-Warren <sauski@google.com>
Auto-Submit: Illia Klimov <elklm@google.com>
Cr-Commit-Position: refs/branch-heads/5112@{#867}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/64b85f04feefb13873d98ad43a159ca1dfa91b62/chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view.h
[modify] https://crrev.com/64b85f04feefb13873d98ad43a159ca1dfa91b62/chrome/browser/ui/views/permission_bubble/permission_prompt_impl.cc
[modify] https://crrev.com/64b85f04feefb13873d98ad43a159ca1dfa91b62/components/permissions/permission_request_manager.cc
[modify] https://crrev.com/64b85f04feefb13873d98ad43a159ca1dfa91b62/chrome/browser/ui/permission_bubble/permission_bubble_browser_test_util.cc
[modify] https://crrev.com/64b85f04feefb13873d98ad43a159ca1dfa91b62/chrome/browser/ui/views/location_bar/permission_chip_unittest.cc
[modify] https://crrev.com/64b85f04feefb13873d98ad43a159ca1dfa91b62/chrome/browser/ui/permission_bubble/permission_bubble_browser_test_util.h
[modify] https://crrev.com/64b85f04feefb13873d98ad43a159ca1dfa91b62/components/permissions/permission_prompt.h
[modify] https://crrev.com/64b85f04feefb13873d98ad43a159ca1dfa91b62/chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view.cc
[modify] https://crrev.com/64b85f04feefb13873d98ad43a159ca1dfa91b62/components/permissions/permission_request_manager.h
[modify] https://crrev.com/64b85f04feefb13873d98ad43a159ca1dfa91b62/chrome/browser/ui/views/permission_bubble/permission_prompt_bubble_view_unittest.cc
[modify] https://crrev.com/64b85f04feefb13873d98ad43a159ca1dfa91b62/chrome/browser/ui/views/location_bar/permission_request_chip.cc


### [Deleted User] (2022-07-14)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2022-07-14)

LTS merge should not be needed. This regressed due to a refactoring in M104, and is now fixed in M104.

### en...@chromium.org (2022-07-14)

After more analysis, it looks like that neither of the two recent WidgetObserver-related changes in M104 [1, 2] has to do with this UAF, as neither the old nor the new implementation of PermissionPromptBubbleView::OnWidgetDestroying mutated/mutates the PermissionPromptBubbleView instance's state in relation to its WebContents or its PermissionPrompt::Delegate. So the timing seems like a coincidence.

It now looks more likely that this is related to the AccessibilityTreeForViews work tracked in https://crbug.com/chromium/1049261. kylixrd@ and nektar@, could you please comment on the state of this work? Is it possible that one of the changes landed in the M104 timeframe already changed the behavior on Chrome OS around how/when/if AXTreeSerializer/AXWidgetObjWrapper is invoked even without the AccessibilityTreeForViews feature flag being enabled? We only seeing crashes on Chrome OS (except one or two dubious traces), but we are not seeing the feature flag being enabled anywhere.

[1]: https://chromium-review.googlesource.com/c/chromium/src/+/3651103
[2]: https://chromium-review.googlesource.com/c/chromium/src/+/3665781

### vo...@google.com (2022-07-14)

Not needed according to https://crbug.com/chromium/1329814#c43.

### am...@google.com (2022-07-15)

[Empty comment from Monorail migration]

### ky...@chromium.org (2022-07-20)

Adding elainechien@ as the owner of the above referenced reviews for more comment.

### el...@chromium.org (2022-07-20)

Hello, taking a look. From https://crbug.com/chromium/1329814#c44 it looks like we've concluded the CLs listed are not directly related to this UAF. On ToT PermissionPromptBubbleView also does not observer Widget closure/destroying events anymore. Happy to help if there are still issues though.

### ne...@chromium.org (2022-07-20)

"AccessibilityTreeForViews" will be launching around the end of this calendar year, so there is no immediate plan to turn it on.
I don't remember anything that had to do with "AccessibilityTreeForViews" affecting the "*Wrapper" classes used by Chrome OS under ui/views/accessibility.
@Kurt
Could you have a look as well please?


### ks...@microsoft.com (2022-07-20)

The common factor is that AXAuraObjCache is used for both ChromeOS and AccessibilityForViews - see https://source.chromium.org/chromium/chromium/src/+/main:ui/views/accessibility/views_ax_tree_manager.h;l=133?q=AXAuraObjCache%20&ss=chromium%2Fchromium%2Fsrc&start=31 

So there is a dependency between them, but it's the other way around - changes in AXAuraObjCache can influence AccessibilityTreeForViews, but due to encapsulation, AccessibilityTreeForViews shouldn't be impacting AXAuraObjCache. My guess is that this is an underlying issue in AXAuraObjCache (or related classes) that AccessibilityTreeForViews exposes more easily (due to lifetime, order of operations, etc.). It is also possible that AccessibilityTreeForViews is using AXAuraObjCache differently than ChromeOS, and may have some unique crashes/behaviors.

For reference, I fixed a few UAF's a while back that were actually issues in AXAuraObjCache that AccessibilityForViews had exposed:

https://chromium-review.googlesource.com/c/chromium/src/+/3517987
https://chromium-review.googlesource.com/c/chromium/src/+/3508957

Note that the repro's had AccessibilityForViews enabled, but the actual fixes were in AXAuraObjCache (or related classes).

In response to https://crbug.com/chromium/1329814#c44, I don't see any recent changes in AXTreeSerializer or AXWidgetObjWrapper that would have caused this. The only change I can find in this general area is https://chromium-review.googlesource.com/c/chromium/src/+/3650060, which could be related to these issues (and lines up with the timeline of the fixes referenced in https://crbug.com/chromium/1329814#c44).

### en...@chromium.org (2022-07-21)

Illia, it sounds like you were able to repro the crash locally. Can you please confirm that repro's with crrev.com/c/3650060, but does not with the commit just before it, to confirm that the regression was introduced in M104?

### el...@google.com (2022-07-22)

Was using `git bisect` and found that the earliest culprit is crrev.com/c/3648307. It crashes in `views::AXTreeSourceViews::GetParent(views::AXAuraObjWrapper*)`

No crashes before, hence M104 the regression was in M104. (Additionally, checked M103 release ASAN build manually, no crashes).

### en...@chromium.org (2022-07-22)

Thank you for getting to the bottom of this, Illia! This corroborates the original report, thus gives us some confidence that the regression indeed happened in M104, where the fix is already cherry picked to.

### vo...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-10-17)

This issue was migrated from crbug.com/chromium/1329814?no_tracker_redirect=1

[Multiple monorail components: Internals>Views, UI>Browser>Permissions>Prompts]
[Monorail mergedwith: crbug.com/chromium/1330228, crbug.com/chromium/1333989, crbug.com/chromium/1339547, crbug.com/chromium/1342463, crbug.com/chromium/1342480]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059774)*
