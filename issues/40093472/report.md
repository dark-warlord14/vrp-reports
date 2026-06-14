# Security: Background fetch leaks cross-origin response size

| Field | Value |
|-------|-------|
| **Issue ID** | [40093472](https://issues.chromium.org/issues/40093472) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>BackgroundFetch |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2018-12-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The background fetch functionality allows data to be downloaded in the background. Although a site can download cross-origin data using this method, it won't be able to access the response. The site can, however, determine the size of the cross-origin response, as this information is made available as part of the background fetch.

**VERSION**  

Chrome Version: Tested on 71.0.3578.98 (stable) and 73.0.3640.0 (canary)  

Operating System: Windows 7 Pro SP1

**REPRODUCTION CASE**

1. Background fetch is currently available as an origin trial, so you'll need to start Chrome with a specific flag to enable the functionality:

chrome --enable-blink-features=BackgroundFetch

2. The attached files form a simple website. To begin with, download each of the files and place them in a directory.
3. In the directory you downloaded the files to, run the following command in a terminal:

python3 -m http.server 8080

This will start a simple web server that can be used to serve the files in the directory.  

4. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

5. This page will install a service worker (service\_worker.js).
6. Once the service worker is active, the page will initiate a background fetch for a cross-origin file using the following call:

registration.backgroundFetch.fetch("test-fetch", ["https://www.google.com/images/branding/googlelogo/1x/googlelogo\_color\_272x92dp.png"]);

7. Once the background fetch has completed, the service worker will log the size of the response (read from the "downloaded" field present in the BackgroundFetchRegistration object) to the console.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [index.html](attachments/index.html) (text/plain, 134 B)
- [main.js](attachments/main.js) (text/plain, 264 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 138 B)

## Timeline

### ca...@chromium.org (2018-12-16)

Assigining low severity since this leaks only the size, passing over to background fetch folks for further triage. 

[Monorail components: Blink>BackgroundFetch]

### sh...@chromium.org (2018-12-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9158d4f74218bc6c775b406af86adf8e67a194c8

commit 9158d4f74218bc6c775b406af86adf8e67a194c8
Author: Rayan Kanso <rayankans@chromium.org>
Date: Tue Dec 18 17:19:45 2018

[Background Fetch] Apply CORS checks before sending progress events

Bug: 915446
Change-Id: I346d38e456b916de9e5acb7640510fdb5080431b
Reviewed-on: https://chromium-review.googlesource.com/c/1379765
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Reviewed-by: Mugdha Lakhani <nator@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Cr-Commit-Position: refs/heads/master@{#617542}
[modify] https://crrev.com/9158d4f74218bc6c775b406af86adf8e67a194c8/content/browser/background_fetch/background_fetch_delegate_proxy.cc
[modify] https://crrev.com/9158d4f74218bc6c775b406af86adf8e67a194c8/content/browser/background_fetch/background_fetch_job_controller.cc
[modify] https://crrev.com/9158d4f74218bc6c775b406af86adf8e67a194c8/content/browser/background_fetch/background_fetch_request_info.cc
[modify] https://crrev.com/9158d4f74218bc6c775b406af86adf8e67a194c8/content/browser/background_fetch/background_fetch_request_info.h
[modify] https://crrev.com/9158d4f74218bc6c775b406af86adf8e67a194c8/third_party/blink/web_tests/external/wpt/background-fetch/fetch.https.window-expected.txt
[modify] https://crrev.com/9158d4f74218bc6c775b406af86adf8e67a194c8/third_party/blink/web_tests/external/wpt/background-fetch/fetch.https.window.js


### ra...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-19)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-07)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### pa...@chromium.org (2019-01-17)

Congrats! The Panel decided to reward $1,000 for this report :) 

### de...@gmail.com (2019-01-17)

Thanks!

### aw...@google.com (2019-01-21)

[Empty comment from Monorail migration]

### ra...@chromium.org (2019-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-03-27)

This issue was migrated from crbug.com/chromium/915446?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/924516]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093472)*
