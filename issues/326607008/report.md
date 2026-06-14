# UAF in chrome://download-internals on iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [326607008](https://issues.chromium.org/issues/326607008) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | iOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2024-02-24 |
| **Bounty** | $3,000.00 |

## Description

## VULNERABILITY DETAILS

Bitset: <https://chromium-review.googlesource.com/c/chromium/src/+/3072886>

`DownloadInternalsUIMessageHandler::RegisterMessages` add self as observer into the logger of background download service.

```
class DownloadInternalsUIMessageHandler : public web::WebUIIOSMessageHandler,
                                          public download::Logger::Observer {
 private:
  // WebUIIOSMessageHandler implementation.
  void RegisterMessages() override {
    // redacted ...

    if (download_service_)
      download_service_->GetLogger()->AddObserver(this); // <-- Add self as observer
  }
}

```

<https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/webui/ui_bundled/download_internals_ui.cc;l=65;drc=d236ab1a0320384b0267eec9b6765c666944984d>

However, there is not `RemoveObserver` in `~DownloadInternalsUIMessageHandler()`, so the observer will not be removed even though the object of DownloadInternalsUIMessageHandler is freed. The lifetime of DownloadInternalsUIMessageHandler object is bound with WebUI for chrome://download-internals on iOS. New tab with url: `chrome://download-internals` and then close it will result in a dangling observer in unchecked observers\_ of `download::LoggerImpl`.

```
namespace download {

class LoggerImpl : public Logger, public LogSink {
 // redacted ...
 private:
  base::ObserverList<Observer>::Unchecked observers_;   // <-- Observers is unchecked, can not prevent UAF if observer has been freed but not removed.
};

}  // namespace download

```

<https://source.chromium.org/chromium/chromium/src/+/main:components/download/internal/background_service/logger_impl.h;l=58;drc=8ba1bad80dc22235693a0dd41fe55c0fd2dbdabd>

So when the notification happened after the object of |DownloadInternalsUIMessageHandler| is freed, UAF will be triggered.

```
class DownloadInternalsUIMessageHandler : public web::WebUIIOSMessageHandler,
                                          public download::Logger::Observer {
  // download::Logger::Observer implementation.
  void OnServiceDownloadChanged(
      const base::Value::Dict& service_download) override {
    web_ui()->FireWebUIListener("service-download-changed", service_download);  // <-- UAF in web_ui()
  }
}

```

<https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/webui/ui_bundled/download_internals_ui.cc;l=87;drc=d236ab1a0320384b0267eec9b6765c666944984d>

Fix suggestion:

```
diff --git a/ios/chrome/browser/webui/ui_bundled/download_internals_ui.cc b/ios/chrome/browser/webui/ui_bundled/download_internals_ui.cc
index 9e35041dc4046..fecfe5d876062 100644
--- a/ios/chrome/browser/webui/ui_bundled/download_internals_ui.cc
+++ b/ios/chrome/browser/webui/ui_bundled/download_internals_ui.cc
@@ -34,7 +34,11 @@ class DownloadInternalsUIMessageHandler : public web::WebUIIOSMessageHandler,
   DownloadInternalsUIMessageHandler(const DownloadInternalsUIMessageHandler&) =
       delete;
   void operator=(const DownloadInternalsUIMessageHandler&) = delete;
-  ~DownloadInternalsUIMessageHandler() override = default;
+
+  ~DownloadInternalsUIMessageHandler() override {
+    if (download_service_)
+      download_service_->GetLogger()->RemoveObserver(this);
+  }
 
  private:
   // WebUIIOSMessageHandler implementation.

```
## VERSION

- Chrome Version: 122.0.6261.62 (Official Build) stable (64 bit)
- Operating System: iOS

## REPRODUCTION CASE

1. Open chrome://download-internals/ and close it
2. Open new tab with chrome://download-internals/, input any valid URL and click Download button

Another:

1. Run command `nc -l 8000` on linux.
2. Open `chrome://download-internals` on iOS, input `http://<your-ip>:8000/poc` and click Download, close the tab.
3. Ctrl + C to kill nc on linux, chrome on iOS crashed.

There is a POC video in attachements.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

- Type of crash: browser
- Crash ID: crash/c818bdbca3b2d430

## CREDIT INFORMATION

Reporter credit: ChaobinZhang

## Attachments

- [ios-download-internals-uaf.mp4](attachments/ios-download-internals-uaf.mp4) (video/mp4, 550.5 KB)

## Timeline

### kr...@google.com (2024-02-26)

Rohit, can you take a look? A similar file here looks ok: <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/download_internals/download_internals_ui_message_handler.cc?q=download_internals_ui_message_handler.cc&ss=chromium%2Fchromium%2Fsrc>

### zh...@gmail.com (2024-02-26)

Simpler Reproduction Case:

1. Open chrome://download-internals/ and close it
2. Open new tab with chrome://download-internals/, input any valid URL and click Download button

### pe...@google.com (2024-02-28)

Setting milestone because of s0/s1 severity.

### ar...@chromium.org (2024-03-08)

[Secondary security shepherd]

@rohitrao: Did you make any progress?
+CC: xingliu@ who authored the patch causing the issue. You might want to help?

### pe...@google.com (2024-03-12)

rohitrao: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-03-15)

Project: chromium/src
Branch: main

commit 952757624c6c06c443c487771d070b52719d17b0
Author: Rohit Rao <rohitrao@chromium.org>
Date:   Fri Mar 15 16:42:14 2024

    [ios] Call RemoveObserver when destroying DownloadInternalsUIMessageHandler.
    
    Bug: 326607008
    Change-Id: Ifb091ed4917c253ea7d2122d9dfdc94734b1e75e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5371489
    Reviewed-by: Mike Dougherty <michaeldo@chromium.org>
    Commit-Queue: Rohit Rao <rohitrao@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1273470}

M       ios/chrome/browser/webui/ui_bundled/download_internals_ui.cc

https://chromium-review.googlesource.com/5371489


### pe...@google.com (2024-03-16)

Requesting merge to extended stable (M122) because latest trunk commit (1273470) appears to be after extended stable branch point (1250580).
Requesting merge to stable (M123) because latest trunk commit (1273470) appears to be after stable branch point (1262506).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### pe...@google.com (2024-03-16)

Merge review required: M123 has already been cut for stable release.

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
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-03-16)

Merge review required: M122 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

### am...@chromium.org (2024-03-20)

Since we don't have comparable Canary data for iOS as we do on other platforms, I can't review Canary data for this fix. (<https://crrev.com/c/5371489>)
The fix appears minimal and safe, so I'm approving for merge. Please ensure you have no concerns with potential stability or other risks before merging this fix.

Please merge this fix to M123 Stable / branch 6312 and M122 Extended / branch 6261 at your earliest convenience and before EOD Thursday, 21 March so this fix can be included in the next respective security updates -- thank you!

### am...@google.com (2024-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-22)

Congratulations ChaobinZhang! The Chrome VRP Panel has decided to award you $2,000 for this report of a heavily mitigated memory corruption bug + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us!

### zh...@gmail.com (2024-03-22)

Thank you very much!

### pe...@google.com (2024-03-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-03-28)

Project: chromium/src
Branch: refs/branch-heads/6312

commit b7d98516f47fd1d9e4e3b06926a3fbf78e51057a
Author: Rohit Rao <rohitrao@chromium.org>
Date:   Thu Mar 28 05:47:23 2024

    [ios] Call RemoveObserver when destroying DownloadInternalsUIMessageHandler.
    
    (cherry picked from commit 952757624c6c06c443c487771d070b52719d17b0)
    
    Bug: 326607008
    Change-Id: Ifb091ed4917c253ea7d2122d9dfdc94734b1e75e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5371489
    Reviewed-by: Mike Dougherty <michaeldo@chromium.org>
    Commit-Queue: Rohit Rao <rohitrao@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1273470}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5401488
    Auto-Submit: Rohit Rao <rohitrao@chromium.org>
    Commit-Queue: Mike Dougherty <michaeldo@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6312@{#728}
    Cr-Branched-From: 6711dcdae48edaf98cbc6964f90fac85b7d9986e-refs/heads/main@{#1262506}

M       ios/chrome/browser/webui/ui_bundled/download_internals_ui.cc

https://chromium-review.googlesource.com/5401488


### pe...@google.com (2024-06-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/326607008)*
