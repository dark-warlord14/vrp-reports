# Security: HeapOverflow in Diagnostics

| Field | Value |
|-------|-------|
| **Issue ID** | [40059002](https://issues.chromium.org/issues/40059002) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebUI |
| **Platforms** | ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | as...@google.com |
| **Created** | 2022-03-07 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

When making a search in |kOpenDurationMetrics|[1], there is no check whether the query result is end(). The out of bounds will occur when using |kOpenDurationMetrics.end()|.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:ash/webui/diagnostics_ui/diagnostics_metrics_message_handler.cc;l=45;drc=653d9e451ef87567e8fcc5f105872e64d51a0220>

Fix suggestion:

diff --git a/ash/webui/diagnostics\_ui/diagnostics\_metrics\_message\_handler.cc b/ash/webui/diagnostics\_ui/diagnostics\_metrics\_message\_handler.cc  

index 73b7407ba5ba3..787c04d75dbc2 100644  

--- a/ash/webui/diagnostics\_ui/diagnostics\_metrics\_message\_handler.cc  

+++ b/ash/webui/diagnostics\_ui/diagnostics\_metrics\_message\_handler.cc  

@@ -43,7 +43,8 @@ void EmitScreenOpenDuration(const NavigationView screen,  

});

auto\* iter = kOpenDurationMetrics.find(screen);

- DCHECK(iter != kOpenDurationMetrics.end());

- if (iter == kOpenDurationMetrics.end())
- return;

base::UmaHistogramLongTimes100(std::string(iter->second), time\_elapsed);  

}

**VERSION**  

Chrome Version: stable  

Operating System: ChromeOS

**REPRODUCTION CASE**

browsing `chrome://diagnostics` and open devtools

execute `chrome.send("recordNavigation",[1337,0]);` in console.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 7.5 KB)

## Timeline

### [Deleted User] (2022-03-07)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-07)

Assuming this is not legitimately reachable, something like content::ReceivedBadMessage() would be more appropriate. However, I think that may not be reachable from ash; dpapad@, can we provide a method on non-Mojo WebUI handlers for reporting a bad message from WebUI?

(The component for //ash/webui/diagnostics_ui no longer exists)

[Monorail components: UI>Browser>WebUI]

### [Deleted User] (2022-03-07)

[Empty comment from Monorail migration]

### as...@google.com (2022-03-08)

[Empty comment from Monorail migration]

### ze...@chromium.org (2022-03-08)

We should also fix the DCHECK's on line 98-99 too.

https://source.chromium.org/chromium/chromium/src/+/main:ash/webui/diagnostics_ui/diagnostics_metrics_message_handler.cc;l=98

Although in this case it will trigger a CHECK in base::Value::List if you send less than 2 args.

Also for future reference the component is in buganizer here - ChromeOS > Software > System Services > Diagnostics

We also have a bug to convert this MessageHandler to mojo.

### [Deleted User] (2022-03-08)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@google.com (2022-03-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4e2fe38d1a0abf9930691ea0988eb4f3c9dcde4b

commit 4e2fe38d1a0abf9930691ea0988eb4f3c9dcde4b
Author: Ashley Prasad <ashleydp@google.com>
Date: Mon Mar 14 16:15:24 2022

diagnostics: validate recordNavigation args before use

- Replace DCHECK with if statement to ensure integrity of incoming
metric arguments prior to use in EmitScreenOpenDuration.
- Ensure iterator for kOpenDurationMap is not accessed when
requested key is not found and add NOTREACHED to clarify it is not
an expected code route.
- Test bad input does not crash tests or trigger metrics update.

Bug: 1303614
Change-Id: Ib1cca36ed5fd80f2001417c5e8daba38a39b27eb
Test: Run testing/xvfb.py out/Default/browser_tests --gtest_filter=DiagnosticsApp* and --gtest_filter=*DiagnosticsAppIntegrationTest*.  Manually tested behavior of chrome.send for 'recordNavigation' on ChromeOS.
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3510988
Reviewed-by: Zentaro Kavanagh <zentaro@chromium.org>
Auto-Submit: Ashley Prasad <ashleydp@google.com>
Commit-Queue: Ashley Prasad <ashleydp@google.com>
Cr-Commit-Position: refs/heads/main@{#980588}

[modify] https://crrev.com/4e2fe38d1a0abf9930691ea0988eb4f3c9dcde4b/ash/webui/diagnostics_ui/diagnostics_metrics_message_handler_unittest.cc
[modify] https://crrev.com/4e2fe38d1a0abf9930691ea0988eb4f3c9dcde4b/ash/webui/diagnostics_ui/diagnostics_metrics_message_handler.cc
[modify] https://crrev.com/4e2fe38d1a0abf9930691ea0988eb4f3c9dcde4b/chrome/browser/ash/web_applications/diagnostics_app_integration_browsertest.cc


### le...@gmail.com (2022-04-06)

Seems like it can be marked as fixed for future merges.

### le...@gmail.com (2022-05-13)

It seems that this issue has been forgotten. lol

### dc...@chromium.org (2022-05-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-05-19)

This fix seems to have been silently backmerged to 101, so refraining from adding merge labels 

### am...@google.com (2022-05-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-24)

Congratulations, Leecraso and Guang Gong. The VRP Panel has decided to award you $5,000 for this report given that this issue isn't web accessible and requires user interaction to trigger. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### le...@gmail.com (2022-05-31)

Will this issue be assigned a cve number?

### [Deleted User] (2022-08-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1303614?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059002)*
