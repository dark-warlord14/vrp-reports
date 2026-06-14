# Security: Sites can bypass restrictions on multiple downloads by redirecting page to about:srcdoc

| Field | Value |
|-------|-------|
| **Issue ID** | [40095288](https://issues.chromium.org/issues/40095288) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads, UI>Browser>Navigation |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2019-06-04 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Typically, sites are restricted to a single download without further user interaction or acceptance. However, by opening a new window and redirecting it to about:srcdoc, a page can download an unlimited number of times. This is because about:srcdoc is rewritten to chrome://srcdoc in some cases and chrome:// pages have permission to initiate automatic downloads by default. This is also true of extension pages.

**VERSION**  

Chrome Version: Tested on 74.0.3729.169 (stable) and 77.0.3814.1 (canary)  

Operating System: Windows 10 Pro, version 1809

**REPRODUCTION CASE**

1. The attached files form a simple website. To begin with, download each of the files and place them in a directory.
2. In the directory you downloaded the files to, run the following command in a terminal:

python3 server.py 8080

This will start a simple web server that can be used to serve the files in the directory.  

3. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

4. This page sets up a click handler that initially opens a new window:

var newWindow = open("<https://www.google.com>", "\_blank");

After two seconds, it navigates this window to about:srcdoc:

newWindow.location.href = "about:srcdoc";

Note that the browser ends up rewriting this to chrome://srcdoc.

It then starts downloading the same file every 5 seconds:

setInterval(() => {  

newWindow.location.href = "download.txt";  

}, 5000);

This works because the ChromeUI scheme explicitly has permission to initiate automatic downloads:

<https://cs.chromium.org/chromium/src/components/content_settings/core/browser/content_settings_registry.cc?l=257&rcl=81ccee3c1849f0f1b5fb6e30048cb8033c80d594>

This is true even though chrome://srcdoc is an invalid page and doesn't actually load anything (except for a standard error page).

Note that about:srcdoc isn't rewritten to chrome://srcdoc in all cases. From what I can tell, it's done when the page that initiates the redirect is cross-origin. That is, if you use window.open to open a same-origin page and redirect that to about:srcdoc, no rewrite will occur. If, however, you open a cross-origin page and redirect that to about:srcdoc, the rewrite to chrome://srcdoc will occur.

Additionally, as can be seen from the above link, extension pages are also whitelisted. This means the following sequence of calls will also work:

var newWindow = open("chrome-extension://ghbmnnjooekpmoecnnnilnnbdlolhkhi/page\_embed\_script.js", "\_blank");

setInterval(() => {  

newWindow.location.href = "download.txt";  

}, 5000);

page\_embed\_script.js is a file in the default installed Google Docs Offline extension. It's listed in web\_accessible\_resources, making it possible for websites to load it in a window.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [download.txt](attachments/download.txt) (text/plain, 0 B)
- [index.html](attachments/index.html) (text/plain, 136 B)
- [main.js](attachments/main.js) (text/plain, 316 B)
- [server.py](attachments/server.py) (text/plain, 488 B)

## Timeline

### wf...@chromium.org (2019-06-04)

Thank you for your report. Initial triage.

[Monorail components: UI>Browser>Downloads]

### sh...@chromium.org (2019-06-05)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2019-06-10)

engedy do you know anyone who could look at this bug?

### sh...@chromium.org (2019-06-11)

[Empty comment from Monorail migration]

### dt...@chromium.org (2019-06-11)

+qinmin who is handling triage for downloads.  Min can you work with engedy and make sure this gets covered?

### qi...@chromium.org (2019-06-11)

I feel the root cause of the issue is that we are allowing a page to navigate to chrome:// URL. engedy@ or jochen@, would you please take a look?

[Monorail components: UI>Browser>Navigation]

### cr...@chromium.org (2019-06-12)

Yes, the rewriting to chrome://srcdoc is big problem.  That's a great find!  Not sure why it only happens on cross-site redirects, but this is an important bug to fix due to the potential privilege escalation.  I don't immediately see ways to run code within a WebUI process as a result of this (since chrome://srcdoc is an error page), but the download bypass does suggest we're incorrectly classifying the download based on the last committed URL rather than the initiating URL.

Adding nasko@, arthursonzogni@, and clamy@ for looking at why we might be rewriting to chrome://srcdoc.  Separately, can any downloads folks point to the logic that picks which URL to use when deciding whether downloads are allowed?

### sh...@chromium.org (2019-06-12)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2019-06-12)

Download are using the URL of the originating webcontents (in this case, it is chrome://srcdoc) to query for contentSettings:
https://cs.chromium.org/chromium/src/chrome/browser/download/download_request_limiter.cc?q=downloadrequestlim&g=0&l=573

### qi...@chromium.org (2019-06-12)

One workaround to this is to pass resource_request->request_initiator into delegate_->CheckDownloadAllowed() here: https://cs.chromium.org/chromium/src/content/browser/download/download_manager_impl.cc?q=downloadmanagerimpl&dr=CSs&l=933.

And later on use the initiator origin to query the contentSettings. But I am not sure there are any side effects.

### cr...@chromium.org (2019-06-12)

https://crbug.com/chromium/970378#c9: Oh wow, that's using WebContents::GetURL(), which has additional problems-- it would return the pending URL if there was one.  (That's deprecated in https://crbug.com/chromium/237908.)  I like the idea of using request_initiator if that works.

lukasza@: Can you comment on whether that's safe to use here?

### lu...@chromium.org (2019-06-12)

Using network::ResourceRequest::request_initiator sounds like a good idea.  The initiator seen by NavigationRequest::OnWillProcessResponseChecksComplete should be trustworthy (i.e. either computed by the browser process, or verified earlier via VerifyBeginNavigationCommonParams / VerifyOpenURLParams [this is a navigation, so I am not including VerifyDownloadUrlParams here]).  OTOH, I am not sure if using an origin of a subframe is okay here (or if some things [like contentSettings] need to work with the origin of the top-level frame).

### lu...@chromium.org (2019-06-12)

RE: https://crbug.com/chromium/970378#c7: why we might be rewriting to chrome://srcdoc

I wonder if //components/url_formatter/url_fixer.cc should be tweaked so that it not only knows about about:blank, but also about about:srcdoc:

  // 'about:blank' is special-cased in various places in the code so it
  // shouldn't be transformed into 'chrome://blank' as the code below will do.
  if (base::LowerCaseEqualsASCII(scheme, url::kAboutScheme)) {
    GURL about_url(base::ToLowerASCII(trimmed));
    if (about_url.IsAboutBlank())
      return about_url;
  }

This feels like a separate bug.  I hope that using network::ResourceRequest::request_initiator or content::CommonNavigationParams::initiator_origin (rather than WebContents::GetURL) for the downloads-policy decision should help both in the chrome://srcdoc as well as chrome-extension:// case (since these are the origins of the old document that is being navigated to a downloadable resource, but these are different from the initiator origin [the attacker's origin]).

### lu...@chromium.org (2019-06-12)

FWIW, I've opened a separate https://crbug.com/chromium/973628 to track the problematic about:srcdoc -> chrome://srcdoc rewriting.  We should still look into using request_initiator to fix the multiple downloads bug (in part, because I don't think we can prevent web-initiated navigations to web-accessible chrome-extension:// resources).

### na...@chromium.org (2019-06-13)

[Empty comment from Monorail migration]

### na...@chromium.org (2019-06-13)

I think we can add another layer of verification. Still need to confirm locally in a debugger, but I think the reason this worked is that the opened window was navigated cross-process, which means the subsequent navigation to about:srcdoc is routed through a RenderFrameProxy(Host). Since about:srcdoc always inherits the parent origin, I don't think it is valid for us to receive about:srcdoc URL as part of FrameHostMsg_OpenURL_Params. 

### lu...@chromium.org (2019-06-14)

The verification in https://crbug.com/chromium/970378#c16 might be tricky, since we can't just terminate a renderer that sends about:srcdoc URL as part of FrameHostMsg_OpenURL_Params - such IPC can be legitimately sent today by a non-compromised / non-malicious / non-buggy renderer.  To add such IPC enforcement we would need to also tweak the renderer-side code to disallow navigating to about:srcdoc URLs (which seems to be allowed today).

### na...@chromium.org (2019-06-14)

I don't think we should be allowing navigations to URL that is "about:srcdoc" as that has no real meaning. We should file a separate bug that disallows this behavior and at that point we could start enforcing it on the browser side. For the record, Firefox 67 displays an error page when a frame is navigated to 'about:srcdoc' with the message "Hmm. That address doesn’t look right. Please check that the URL is correct and try again.".

### lu...@chromium.org (2019-06-14)

https://crbug.com/chromium/974300 was fixed, so the original repro might not work anymore here, but chrome-extension repro should still work and therefore we still need to make sure that:
1) request_initiator is plumbed through as necessary/appropriate
2) WebContents::GetURL() is avoided

### qi...@chromium.org (2019-06-14)

There are some issues related to how things work in DownloadRequestLimiter:
1. Currently we show a popup dialog when more than 1 download is initiated on the page, with the "chrome://srcdoc" in the dialog. This is inaccurate as we need to change this to the request_initiator.  Omnibox also has a content setting dialog with the same url issue.
2. DownloadRequestLimiter maintains a TabDownloadState, Currently the TabDownloadState only has a global state for the current tab, either allowing 1 download/prompt/always allow/disallow. So it is per tab thingy. The state can get reset on user gesture or browser initiated navigation.  If we have more than 1 origin that can issue download request to the same tab at the same time, then we need to maintain some states about each origin (for example, always disable download from the localhost but always allow for the current url in the omnibox).  

### qi...@chromium.org (2019-06-14)

For #20,  we need to clarify what to do if "a.com" launches a new tab with "b.com", and then start using "location.href =" to create download on the new tab. 
1. if automatic download is enabled for "a.com", should all the download go through even if the TabDownloadState only allows 1 download?
2. if b.com triggers a download first(that causes prompt for the next download), will the download triggered by a.com next require prompting if automatically download is disabled?
3. if a.com triggers a download first, will the download triggered by b.com next require prompting if automatically download is disabled?

### qi...@chromium.org (2019-06-14)

Assigning this to myself as the most of fix should now be in DownloadRequestLimiter.

### qi...@chromium.org (2019-06-24)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/357184a997a266bc2a1c4e7a2ff21122f1c4c004

commit 357184a997a266bc2a1c4e7a2ff21122f1c4c004
Author: Min Qin <qinmin@chromium.org>
Date: Tue Jun 25 16:31:44 2019

Pass request initiator to check whether a download can proceed

Currently download use webcontents::GeURL() to check content settings.
But the download can actually be triggered by javascript from another
origin. This CL fixes the issue by passing the request initiator to
check the content settings.
Here is what included in this CL:
1. removed originating_web_contents param from TabDownloadState ctor,
this param is never used.
2. Adding an origin param to DownloadRequestLimiter::CanDownload() call,
and it will be used to check the content settings.
3. In DownloadRequestLimiter::CanDownloadImpl(), always do content
 setting check first. This fixes a bug that any site can always
 trigger a download first even if its automatic download setting is
 blocked
4. For restricted origins, record their download status. So that we can
differentiate origins that are blocked and origins that require prompt.

BUG=970378

Change-Id: I6f7efc8b5c6b27ff3eaec1bb436c5ffbb8c8b26d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1657031
Reviewed-by: Xing Liu <xingliu@chromium.org>
Reviewed-by: Scott Violet <sky@chromium.org>
Reviewed-by: Min Qin <qinmin@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#672091}

[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/background_fetch/background_fetch_browsertest.cc
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/background_fetch/background_fetch_delegate_impl.cc
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/download/chrome_download_manager_delegate.cc
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/download/chrome_download_manager_delegate.h
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/download/download_browsertest.cc
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/download/download_permission_request.cc
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/download/download_permission_request.h
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/download/download_request_limiter.cc
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/download/download_request_limiter.h
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/download/download_request_limiter_unittest.cc
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/ui/content_settings/content_setting_bubble_model.cc
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/ui/content_settings/content_setting_image_model_browsertest.cc
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/chrome/browser/ui/views/location_bar/content_setting_bubble_dialog_browsertest.cc
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/content/browser/download/download_manager_impl.cc
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/content/public/browser/download_manager_delegate.cc
[modify] https://crrev.com/357184a997a266bc2a1c4e7a2ff21122f1c4c004/content/public/browser/download_manager_delegate.h


### qi...@chromium.org (2019-06-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-26)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-15)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-25)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-09-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/970378?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Downloads, UI>Browser>Navigation]
[Monorail blocked-on: crbug.com/chromium/973628]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095288)*
