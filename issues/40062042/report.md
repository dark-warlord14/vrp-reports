# Security: UAF in HandleExpandedPaths

| Field | Value |
|-------|-------|
| **Issue ID** | [40062042](https://issues.chromium.org/issues/40062042) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Enterprise, Enterprise>Connectors |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2022-12-05 |
| **Bounty** | $31,000.00 |

## Description

UAF in HandleExpandedPaths

**VULNERABILITY DETAILS**  

When processing the files read request from the clipboard, the current WebContent will be bound[1] into function `HandleExpandedPaths` as a callback.

```
void ChromeContentBrowserClient::IsClipboardPasteContentAllowed(  
    content::WebContents\* web_contents,  
    const GURL& url,  
    const ui::ClipboardFormatType& data_type,  
    const std::string& data,  
    IsClipboardPasteContentAllowedCallback callback) {  
    [...]  
    fsd_ptr->ExpandPaths(base::BindOnce(&HandleExpandedPaths, std::move(fsd),   <--- 1.  
                                        web_contents, std::move(dialog_data),  
                                        connector, std::move(paths),  
                                        std::move(callback)));  
    [...]  
}  

```

This callback will run asynchronously[2][3]:

```
void FilesScanData::ExpandPaths(base::OnceClosure done_closure) {  
  expand_paths_done_closure_ = std::move(done_closure);    <-------- the callback expand_paths_done_closure_.  
  
  base::ThreadPool::PostTaskAndReplyWithResult(  
      FROM_HERE, {base::TaskPriority::USER_VISIBLE, base::MayBlock()},  
      base::BindOnce(&GetPathsToScan, base_paths_),  
      base::BindOnce(&FilesScanData::OnExpandPathsDone, AsWeakPtr()));  <----[2] OnExpandPathsDone will be called after the ThreadPool task GetPathsToScan.  
}  
  
void FilesScanData::OnExpandPathsDone(  
    std::pair<ExpandedPathsIndexes, std::vector<base::FilePath>>  
        indexes_and_paths) {  
  expanded_paths_indexes_ = std::move(indexes_and_paths.first);  
  expanded_paths_ = std::move(indexes_and_paths.second);  
  std::move(expand_paths_done_closure_).Run();    <------[3] OnExpandPathsDone will run the callback expand_paths_done_closure_.  
}  

```

Therefore, if WebContent is destroyed before `OnExpandPathsDone` gets executed, the UAF will be triggered when it is accessed[4] later.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_content_browser_client.cc;l=6610;drc=c6170265ae74b21355d013d08a0ad7a0b449d388>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:components/enterprise/common/files_scan_data.cc;l=65;drc=96d6572877a23986bf712cf8676ea3978db4eb0f>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:components/enterprise/common/files_scan_data.cc;l=101;drc=96d6572877a23986bf712cf8676ea3978db4eb0f>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_content_browser_client.cc;l=1421;drc=c6170265ae74b21355d013d08a0ad7a0b449d388>

**VERSION**  

Chrome Version: M109 beta  

Operating System: test in win

Bisect:

<https://source.chromium.org/chromium/chromium/src/+/c6170265ae74b21355d013d08a0ad7a0b449d388>  

[rogerta@chromium.org](mailto:rogerta@chromium.org) might be the right owner.

**REPRODUCTION CASE**

Apply the patch (or enable the preference `enterprise_connectors.on_file_attached` as in \*). It has nothing to do with the vulnerability itself.

$ python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen  

$ python3 -m http.server 8000  

$ out/asan/chrome.exe --user-data-dir=xxxx --enable-blink-features=MojoJS "<http://localhost:8000/poc.html>"

[\*] <https://support.google.com/chrome/a/answer/11375053>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: browser.  

Crash State: see asan file.

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 43.3 KB)
- [enable_connectors.patch](attachments/enable_connectors.patch) (text/plain, 1.7 KB)
- [poc.html](attachments/poc.html) (text/plain, 622 B)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)

## Timeline

### [Deleted User] (2022-12-05)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-12-06)

I'm not able to reproduce this with the patch and poc, are there any other steps required besides clicking the trigger button?

### le...@gmail.com (2022-12-06)

There are no other steps required. But since it requires a race between threads, please try a few more times, or you can try to copy one or more files into the clipboard to extend the time window[*] and then click the trigger button.

* https://source.chromium.org/chromium/chromium/src/+/main:components/enterprise/common/files_scan_data.cc;l=22;drc=96d6572877a23986bf712cf8676ea3978db4eb0f

### [Deleted User] (2022-12-06)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2022-12-06)

rogerta: I was not able to reproduce, but from the report, this seems like a legitimate regression. Can you PTAL? Thanks

Marking as high severity snce this is in the browser process, but requires MojoJS

[Monorail components: Enterprise Enterprise>Connectors]

### [Deleted User] (2022-12-06)

[Empty comment from Monorail migration]

### ro...@chromium.org (2022-12-06)

Taking a look.

### ro...@chromium.org (2022-12-06)

A UAF could happen as described.  ExpandPaths() starts a background task to explode directories into a set of all files descendent from them.  If the tab is closed before the background task can walk the directory trees to collect all the file names, when the background task replies to the originating task, an invalid web content pointer could be accessed.

Repro steps:
------------
1/ Make sure to enable content analysis (This can only be set via cloud-based enterprise policies so this code path won't happen for consumer users).
2/ Use the OS clipboard copy+paste to copy a directory containing a very large number of files.
3/ Close the tab quickly.

Content analysis works only on desktop platforms and cros.

Carlos: you probably had a hard time repro'ing because you need either a slow computer, a slow disk, a very large/deep directory, or some combination of those things.

This fix is to pass a WekPtr<WebContents> rather than a naked WebContents pointer and to check that it is still valid.

### ro...@chromium.org (2022-12-06)

To expand on repro step #2 above (on Windows):

2.1/ Open the Windows explorer.
2.2/ Select a large directory like C:\Windows and type Ctrl+C to copy it.
2.3/ Open a web page that accepts pasting from the clipboard.
2.4/ Type Ctrl+V to paste the files into the web page.


### do...@chromium.org (2022-12-06)

There was a similar potential UAF on the drag-drop side of things, the fix was to make a WebContentObserver to handle it closing:
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/tab_contents/chrome_web_contents_view_handle_drop.cc;l=74;drc=5f427e1afbe15d505d74be94879e971e48f1befe

Maybe that class should be refactored similarly like the logic now in FilesScanData was?

### le...@gmail.com (2022-12-07)

@rogerta:

To prevent misunderstanding, let me clarify:

1. In my local testing, a very large/deep directory is not needed. Success rate: 3/10 for no file copy, 9/10 for one file copy. (quad-core, 8 GB memory, SSD for virtual machine)

2. Even if you use a lot of files, it is unnecessary to paste the files into the web page or close the tab quickly, the JS code in the poc already does the same thing. Just copy the files you selected, and click the trigger button. If the `window.close()` in the JS code does not work, you can try the following patch:

diff --git a/third_party/blink/renderer/core/frame/dom_window.cc b/third_party/blink/renderer/core/frame/dom_window.cc
index ea903c66c43..6181e4da2c1 100644
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

### ro...@chromium.org (2022-12-07)

Can you clarify "3/10 for no file copy"?  This bug happens if you try to copy files, it does not happen if you try to copy text.  Do I understand the bug correctly?

Correct that a web page itself can trigger paste (via a user action like clicking a button), paste itself does not need to be a user action.  So agreed that a malicious web page could attempt to crash the browser.  So more generally the repro steps could be:

1/ User action to copy one or more files into the OS clipboard.
2/ User action on the web page to either paste or trigger malicious code.


### gi...@appspot.gserviceaccount.com (2022-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f5a4a5444bf4b0bede0ecf5270e85f93c745f97e

commit f5a4a5444bf4b0bede0ecf5270e85f93c745f97e
Author: Roger Tawa <rogerta@chromium.org>
Date: Wed Dec 07 16:38:54 2022

Fix UAF in HandleExpandedPaths.

Bug: 1395718
Change-Id: I81e2b901f323414f5cdb032850c19f706c0cc371
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4085202
Reviewed-by: Dominique Fauteux-Chapleau <domfc@chromium.org>
Commit-Queue: Roger Tawa <rogerta@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1080362}

[modify] https://crrev.com/f5a4a5444bf4b0bede0ecf5270e85f93c745f97e/chrome/browser/chrome_content_browser_client.cc


### [Deleted User] (2022-12-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2022-12-07)

Hi rogerta@:

This vulnerability does not need to copy files, even if you copy text or keep empty in the clipboard, calling `clipHostptr.readFiles` will execute the same path. It's just that `filenames.size()`[*] is 0 at this time, which will cause the time window to be small.

[*] https://source.chromium.org/chromium/chromium/src/+/main:components/enterprise/common/files_scan_data.cc;l=22;drc=96d6572877a23986bf712cf8676ea3978db4eb0f

### [Deleted User] (2022-12-07)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2022-12-07)

Got it leecraso@.  Feel free to test the fix above when it hits canary.  Thanks for the bug report!

### ro...@chromium.org (2022-12-07)

[Empty comment from Monorail migration]

### le...@gmail.com (2022-12-07)

Very efficient fix, the patch works well in my local test.

### ro...@chromium.org (2022-12-07)

Thanks for confirmation.  I will make this bug as fixed.

### ro...@chromium.org (2022-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-07)

Requesting merge to beta M109 because latest trunk commit (1080362) appears to be after beta branch point (1070088).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-08)

Merge review required: M109 is already shipping to beta.

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
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-12)

m109 merge approved, please merge this fix to branch 5414 ASAP / NLT 3pm Pacific tomorrow, Tuesday 13 December so this fix can be included in the next M109/beta -- thank you! 

### pb...@google.com (2022-12-13)

Your merge has been approved for M109, please help complete your merges asap (before 2pm PST) today, so the change can be included in this week's RC build for beta releases.

We would like to get the changes as much beta time as possible, so please complete your merges asap to M109 branch(go/chrome-branches).

### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-16)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $30,000 for this report + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### [Deleted User] (2022-12-16)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-19)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ec6f661d691fe8504298010d77297b9daa6abfb4

commit ec6f661d691fe8504298010d77297b9daa6abfb4
Author: Roger Tawa <rogerta@chromium.org>
Date: Tue Jan 03 16:55:37 2023

Fix UAF in HandleExpandedPaths.

(cherry picked from commit f5a4a5444bf4b0bede0ecf5270e85f93c745f97e)

Bug: 1395718
Change-Id: I81e2b901f323414f5cdb032850c19f706c0cc371
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4085202
Reviewed-by: Dominique Fauteux-Chapleau <domfc@chromium.org>
Commit-Queue: Roger Tawa <rogerta@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1080362}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4132447
Reviewed-by: Krishna Govind <govind@chromium.org>
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/5414@{#1156}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/ec6f661d691fe8504298010d77297b9daa6abfb4/chrome/browser/chrome_content_browser_client.cc


### [Deleted User] (2023-01-03)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-01-04)

[Empty comment from Monorail migration]

### rz...@google.com (2023-01-05)

The changed code in IsClipboardPasteContentAllowed isn't present in M102 and HandleExpandedPaths isn't present in M102

### gm...@google.com (2023-01-31)

@rzanoni, please evaluate for 108.

### rz...@google.com (2023-02-01)

The fixed code isn't present in 108.

### [Deleted User] (2023-03-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1395718?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Enterprise, Enterprise>Connectors]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062042)*
