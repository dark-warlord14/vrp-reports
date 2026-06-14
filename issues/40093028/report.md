# Security: Sites can open extension pages using WindowClient.navigate

| Field | Value |
|-------|-------|
| **Issue ID** | [40093028](https://issues.chromium.org/issues/40093028) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>ServiceWorker, Platform>Extensions, UI>Browser>Navigation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2018-11-11 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Normally, sites are prevented from being able to open extension pages. While this restriction applies to methods like window.open() or window.location.href = ..., it doesn't apply when a site triggers a navigation event using WindowClient.navigate(). In that case, the page will be loaded even if it's an extension page.

A site can also do this by creating a notification, then opening an extension page using clients.openWindow() in the notification click handler.

**VERSION**  

Chrome Version: Tested on 70.0.3538.102 (stable) and 72.0.3607.0 (canary)  

Operating System: Windows 10 Pro, version 1803

**REPRODUCTION CASE**

1. Install uBlock Origin.
2. The attached files form a simple website. To begin with, download each of the files and place them in a directory.
3. In the directory you downloaded the files to, run the following command in a terminal:

python3 -m http.server 8080

This will start a simple web server that can be used to serve the files in the directory.  

4. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

5. This page will install a service worker (service\_worker.js). Once the service worker is active, the page will send it a message.
6. Once the service worker has received the message, it will retrieve a list of all window clients, using clients.matchAll(). It will then navigate the first client (i.e. the page opened in step 4) to the uBlock Origin dashboard using the following call:

client.navigate("chrome-extension://cjpalhdlnbpafiamejdnhcphjbkeiagm/dashboard.html");

As mentioned in the summary above, it's also possible for a site to open an extension page in a notification click handler by using clients.openWindow(). For example:

clients.openWindow("chrome-extension://cjpalhdlnbpafiamejdnhcphjbkeiagm/dashboard.html")

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [index.html](attachments/index.html) (text/plain, 134 B)
- [main.js](attachments/main.js) (text/plain, 227 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 578 B)

## Timeline

### ke...@chromium.org (2018-11-12)

creis@ can you have a look at this? I've verified it on Windows.

[Monorail components: Platform>Extensions UI>Browser>Navigation]

### cr...@chromium.org (2018-11-12)

Looks like WindowClient is a Service Worker API.  Agreed that it's concerning if WindowClient.navigate can bypass the usual renderer-initiated navigation checks.  Let's figure out what checks are missing before deciding on severity, but this is probably at least Medium.

falken@: Do you know how this is implemented?

[Monorail components: Blink>ServiceWorker]

### cr...@chromium.org (2018-11-13)

I've checked and this doesn't seem to allow navigations to chrome:// URLs, which would be worse.  It appears to be a web-accessible-resource bypass, probably implying that ShouldAllowOpenURL isn't being called.  (When testing with another extension, I can confirm it allows navigating to a non-web-accessible-resource, whereas navigations to web-accessible-resources are always allowed.)

Devlin, what's the severity for a web accessible resources bypass?  I'm getting mixed messages from https://crbug.com/chromium/598265, https://crbug.com/chromium/821586, and https://crbug.com/chromium/899688, but perhaps this is Low after all?

Note that https://crbug.com/chromium/899688 is another issue from the same reporter on Oct 29, which looks very similar except for the use of fetch instead of navigate.  Not sure if fetch is meant to have the same web-accessible-resources checks, but CC'ing lazyboy@ (who is the owner of that issue).

Matt: It looks like NavigateClientOnUI in service_worker_client_utils.cc is using WebContents::OpenURL, which apparently doesn't go through ChromeContentBrowserClientExtensionsPart::ShouldAllowOpenURL.  Maybe we can find a better alternative.

Camille/Arthur: Is there a better navigation entry point for ServiceWorker code to be using here, which would go through ShouldAllowOpenURL?  Or should we include a call to that on this path?

### rd...@chromium.org (2018-11-13)

> Devlin, what's the severity for a web accessible resources bypass?  I'm getting mixed messages from  https://crbug.com/chromium/598265 ,  https://crbug.com/chromium/821586 , and https://crbug.com/chromium/899688, but perhaps this is Low after all?

Generally, a web-accessible-resources bypass (by itself) would be considered Low, I think.  Obviously if there's additional capabilities leaked (e.g., loading an extension page in the web page's process, or gaining access to extension APIs), they can be higher.  I think in this case, Low is probably correct.

### dr...@chromium.org (2018-11-14)

Updating to low severity based on #4

### fa...@chromium.org (2018-11-20)

I agree WebContents::OpenURL() looks insufficient and the SW code should be doing more of NavigatorImpl::RequestOpenURL(), like calling ShouldAllowOpenURL. 

(repeating c#3): Camille/Arthur: Is there a better navigation entry point for ServiceWorker code to be using here, which would go through ShouldAllowOpenURL?  Or should we include a call to that on this path?

If not, I'll just add a call to ShouldAllowOpenURL.

### ar...@chromium.org (2018-11-20)

> (repeating c#3): Camille/Arthur: Is there a better navigation entry point for ServiceWorker code to be using here, which would go through ShouldAllowOpenURL?  Or should we include a call to that on this path?

It's hard to say. Path using ShouldAllowOpenURL are:
 (1) RenderFrameHostImpl::OnOpenURL() -> NavigatorImpl::RequestOpenURL()
 (2) RenderFrameProxyHost::OnOpenURL() -> NavigateFromFrameProxy()
 (3) RenderFrameHostImpl::CreateNewWindow()

Reusing the existing path look better, but I don't know if you will be able to.
It seems to depend on which RenderFrame openURL is called. I don't think you can have it and if it matters.

### fa...@chromium.org (2018-11-21)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-11-21)

+Kinuko for context for the CL.

### bu...@chromium.org (2018-11-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/18c5c5dcef9cfccff64f0c23f920ef22822271a9

commit 18c5c5dcef9cfccff64f0c23f920ef22822271a9
Author: Matt Falkenhagen <falken@chromium.org>
Date: Mon Nov 26 02:55:37 2018

service worker: Make navigate/openWindow go through more security checks.

WindowClient.navigate() and Clients.openWindow() were implemented in
a way that directly navigated to the URL without going through
some checks that the normal navigation path goes through. This CL
attempts to fix that:
- WindowClient.navigate() now goes through Navigator::RequestOpenURL()
  instead of directly through WebContents::OpenURL().
- Clients.openWindow() now calls more ContentBrowserClient functions
  for manipulating the navigation before invoking
  ContentBrowserClient::OpenURL().

Bug: 904219
Change-Id: Ic38978aee98c09834fdbbc240164068faa3fd4f5
Reviewed-on: https://chromium-review.googlesource.com/c/1345686
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Cr-Commit-Position: refs/heads/master@{#610753}
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/chrome/browser/chrome_content_browser_client.cc
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/chrome/browser/chrome_content_browser_client.h
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/chrome/browser/chrome_content_browser_client_unittest.cc
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/browser/service_worker/service_worker_client_utils.cc
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/browser/service_worker/service_worker_client_utils.h
[add] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/browser/service_worker/service_worker_clients_api_browsertest.cc
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/browser/service_worker/service_worker_context_wrapper.h
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/browser/service_worker/service_worker_process_manager.cc
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/browser/service_worker/service_worker_process_manager.h
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/browser/service_worker/service_worker_version.cc
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/public/browser/content_browser_client.cc
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/public/browser/content_browser_client.h
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/shell/browser/shell_content_browser_client.cc
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/shell/browser/shell_content_browser_client.h
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/test/BUILD.gn
[add] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/test/data/service_worker/client_api_worker.js
[modify] https://crrev.com/18c5c5dcef9cfccff64f0c23f920ef22822271a9/content/test/data/service_worker/create_service_worker.html


### fa...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-07)

Many thanks for the report. The Chrome VRP panel decided to reward $500. A member of our finance team will be in touch to arrange payment.

### aw...@google.com (2018-12-07)

[Empty comment from Monorail migration]

### de...@gmail.com (2018-12-07)

Thank you!

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/904219?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>ServiceWorker, Platform>Extensions, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093028)*
