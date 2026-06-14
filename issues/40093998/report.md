# Security: Possible to override browser-initiated navigation using WindowClient.navigate

| Field | Value |
|-------|-------|
| **Issue ID** | [40093998](https://issues.chromium.org/issues/40093998) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>ServiceWorker, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2019-02-08 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

A service worker can call the WindowClient.navigate method to direct a page under its control to a specific URL. Unlike the usual methods of redirecting (e.g. window.location.href = ..., window.location.replace(...), etc), which don't work once the beforeunload event has been triggered, WindowClient.navigate does allow navigation after the event has been sent. This allows a page to redirect to another arbitrary location once the user tries to navigate away.

**VERSION**  

Chrome Version: Tested on 72.0.3626.96 (stable) and 74.0.3699.0 (canary)  

Operating System: Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. The attached files form a simple website. To begin with, download each of the files and place them in a directory.
2. In the directory you downloaded the files to, run the following command in a terminal:

python3 -m http.server 8080

This will start a simple web server that can be used to serve the files in the directory.  

3. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

4. This page will install a service worker (service\_worker.js).
5. It will also add an listener for the beforeunload event. Once the event is triggered, the page will send the service worker a message. Once the service worker has received the message, it will attempt to navigate the first window client it finds (i.e. the page opened in step 3) using the following call:

client.navigate("<https://www.google.com/>");

To verify that this works as expected, all you need to do it attempt to navigate away from the page, either using the back/forward buttons, or by entering an address in the address bar.

The method here may be somewhat timing dependent, in that if the service worker doesn't process the message until after the browser-initiated navigation has occurred, the WindowClient.navigate call will fail. From the testing I've done, it works reliably.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [index.html](attachments/index.html) (text/plain, 134 B)
- [main.js](attachments/main.js) (text/plain, 478 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 521 B)
- [index.html](attachments/index_53099748.html) (text/plain, 134 B)
- [main.js](attachments/main_53099749.js) (text/plain, 413 B)
- [service_worker.js](attachments/service_worker_53099750.js) (text/plain, 675 B)

## Timeline

### de...@gmail.com (2019-02-08)

I also have an alternate version of the site attached here. In this version, the service worker adds a fragment identifier on to the end of the current client URL and navigates to that. This means that when you attempt to navigate away, the page doesn't actually reload (since the only thing that changes is the fragment) and the user-initiated navigation is effectively cancelled.

### mm...@chromium.org (2019-02-08)

I've successfully reproduced the issue on Linux, so I suspect that almost all platforms are affected.

[Monorail components: Blink>ServiceWorker UI>Browser>Navigation]

### sh...@chromium.org (2019-02-09)

[Empty comment from Monorail migration]

### fa...@chromium.org (2019-02-12)

Navigation experts WDYT? Looks a bit tricky. The current sequence of events is probably:
1. (Renderer) Renderer dispatches the 'beforeunload' event.
2. (Renderer -> Renderer) Page sends SW (possibly out-of-process) the PostMessage IPC.
3. (Renderer -> Browser) SW sends Browser the NavigateClient IPC.
4. (Browser IO thread) Navigates the page.

We'd want to know at (4) that (1) already happened. Is there a way for the browser on the IO thread to know this without being racy? Is there some step 0 where the browser can already know the 'beforeunload' event is about to be dispatched?

Maybe ServiceWorkerProviderHost can be a WebContentsObserver and listen for BeforeUnloadFired/Cancelled, then reject any attempt to use the WindowClient.navigate API on it.

### ar...@chromium.org (2019-02-13)

Maybe step 0 you want is:
0. (browser -> Renderer): RenderFrameHostImpl::DispatchBeforeUnload()

It asks this frame and all its children to dispatch the 'beforeunload' event. Once it is done in all of them and if the users decides to 'proceed', then the navigation starts (navigation_handle is created).

However, I am not sure to know how you could prevent SW navigations knowing this without introducing bugs.
Does the SW navigation cancels the NavigationRequest while we are waiting for beforeunload? or after?

---

What we enforce is that a browser initiated navigation shouldn't be canceled by a renderer-initiated one.
The main check is here:
https://cs.chromium.org/chromium/src/content/browser/frame_host/navigator_impl.cc?type=cs&q=%22The+renderer-initiated+navigation+request+is+ignored+iff+a)+there+is%22&g=0&l=605
and for history-navigation here:
https://cs.chromium.org/chromium/src/content/browser/web_contents/web_contents_impl.cc?type=cs&q=%22Non-user+initiated+navigations+coming+from+the+renderer+should+be%22&g=0&l=4672

I am wondering what causes this mechanism to fail. Is it reached? Are SW initiated navigation considered renderer-initiated?

### fa...@chromium.org (2019-02-13)

Thanks Arthur.  Service Worker initiated navigation starts as an IPC from the SW to ServiceWorkerVersion::NavigateClient, which leads to  NavigateClientOnUI, which does  Navigator::RequestOpenURL.I'm not sure whether RequestOpenURL will end up in the NavigatorImpl::OnBeginNavigation function you linked to. Let me know if there's a better function to use than RequestOpenURL. I'll take a look on Friday if we end up in OnBeginNavigation.

This is reminiscent of https://crbug.com/904219 BTW. Maybe we need to step back and reconsider how to properly implement the WindowClient.navigate() and Clients.openWindow() APIs in a way that integrates well with Navigation code.

### fa...@chromium.org (2019-02-19)

The WindowClient.navigate() navigation replaces the omnibox navigation here:

#2 0x7f75cfe5b0c9 content::NavigationRequest::~NavigationRequest()
#3 0x7f75cfe5b45e content::NavigationRequest::~NavigationRequest()
#4 0x7f75cfe38b3a content::FrameTreeNode::CreatedNavigationRequest()
#5 0x7f75cfe6429f content::NavigatorImpl::Navigate()
#6 0x7f75cfe4451e content::NavigationControllerImpl::NavigateWithoutEntry()
#7 0x7f75cfe43695 content::NavigationControllerImpl::LoadURLWithParams()
#8 0x561359cef111 (anonymous namespace)::LoadURLInContents()
#9 0x561359cee798 Navigate()
#10 0x561359cd8b70 Browser::OpenURLFromTab()
#11 0x7f75d023b422 content::WebContentsImpl::OpenURL()
#12 0x7f75cfe64889 content::NavigatorImpl::RequestOpenURL()
#13 0x7f75d012c9dd content::service_worker_client_utils::(anonymous namespace)::NavigateClientOnUI()

I don't see OnBeginNavigation() entered.

It looks like a fix may be to do the same thing as https://crbug.com/chromium/879965?

### fa...@chromium.org (2019-02-19)

Yep that does the trick. Now I'll write a test.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e8bf23bbbc3976d6a3418a7298a39bbf35c7beb3

commit e8bf23bbbc3976d6a3418a7298a39bbf35c7beb3
Author: Matt Falkenhagen <falken@chromium.org>
Date: Tue Feb 19 11:41:18 2019

Prevent WindowClient.navigate() from cancelling a browser-initiated navigation.

Otherwise, a service worker can prevent you from navigating where you
want to go via the omnibox.

Note: this is similar to WebContentsImpl::OnGoToEntryAtOffset() for
renderer-initiated history navigations.

Bug: 930154
Change-Id: I3a687ccc8ba4420d2369adb24f63c2702bdeeff1
Reviewed-on: https://chromium-review.googlesource.com/c/1477454
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Auto-Submit: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#633231}
[modify] https://crrev.com/e8bf23bbbc3976d6a3418a7298a39bbf35c7beb3/content/browser/service_worker/service_worker_client_utils.cc
[modify] https://crrev.com/e8bf23bbbc3976d6a3418a7298a39bbf35c7beb3/content/browser/service_worker/service_worker_clients_api_browsertest.cc
[modify] https://crrev.com/e8bf23bbbc3976d6a3418a7298a39bbf35c7beb3/content/test/data/service_worker/client_api_worker.js
[add] https://crrev.com/e8bf23bbbc3976d6a3418a7298a39bbf35c7beb3/content/test/data/service_worker/request_navigate.html


### fa...@chromium.org (2019-02-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-20)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-25)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-28)

Congrats! The Panel decided to reward $500 for this report :)

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/930154?no_tracker_redirect=1

[Multiple monorail components: Blink>ServiceWorker, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093998)*
