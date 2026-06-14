# Security:Chrome Address Bar URL Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40085742](https://issues.chromium.org/issues/40085742) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Reporter** | xi...@gmail.com |
| **Assignee** | na...@chromium.org |
| **Created** | 2016-10-20 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome Address Bar URL Spoofing

**VERSION**  

Chrome Version: 54.0.2840.59 (64-bit)+[Stable]  

Operating System: [MAC OS 10.12, Windows 7&10]

**REPRODUCTION CASE**  

Right click on the link, select open a page in a new window. Then,in the address bar will be displayed the first request URL as the final committed URL .

POC:

<a href="google.com::">11111</a>  

<a href="www.google.com::/url?q=http%3A%2F%2Fxisigr.com%2Ftest%2Fspoof%2Fchrome%2F3.html&sa=D&sntz=1&usg=AFQjCNG-QnLGG1ixIlOzlpZQn5cweSU3Cw">22222</a>  

<a href="xisigr.com::/test/spoof/chrome/5.html">33333</a>

Online demo: <http://xisigr.com/test/spoof/chrome/spoof_1.html>

## Attachments

- [spoof_1.htm](attachments/spoof_1.htm) (text/plain, 471 B)
- [AddressBarNotUpdatedOnRedirect.png](attachments/AddressBarNotUpdatedOnRedirect.png) (image/png, 32.5 KB)

## Timeline

### el...@chromium.org (2016-10-20)

Confirmed repro in latest Canary (56.0.2896.0). It looks like we fail to update the URL Bar with the final address after the browser gets back the Google.com-served redirect.

[Monorail components: UI>Browser>Omnibox]

### el...@chromium.org (2016-10-20)

In debug, clicking in the Omnibox crashes a DCHECK:

[9184:7300:1020/161124:FATAL:gurl.cc(179)] Check failed: false. Trying to get the spec of an invalid URL!

### el...@chromium.org (2016-10-21)

In older Chrome, navigation to the invalid URL failed with a blank white page. In current Chrome, navigation succeeds and the invalid URL is shown in the omnibox and fails to refresh on navigation.

You are probably looking for a change made after 316900 (known good), but no later than 316926 (first known bad).
CHANGELOG URL:
The script might not always return single CL as suspect as some perf builds might get missing due to failure.
  https://chromium.googlesource.com/chromium/src/+log/cd2fa46ade22a4c675adbeccccdb64a896d17ac5..78afb85b32b013e2b8af772e0dc36d3bb5c04808


### el...@chromium.org (2016-10-21)

creis@, can you PTAL?

CL https://chromium.googlesource.com/chromium/src/+/94a977f6dc4714f49841db1c2d831ab53e557f15 changed NavigationController::CreateNavigationEntry such that it calls a fixup function on the URL.

That fixup function changes a GURL with is_valid==true to one where is_valid==false.

e.g. annotating thusly:
std::unique_ptr<NavigationEntry> NavigationController::CreateNavigationEntry(
    const GURL& url,
    const Referrer& referrer,
    ui::PageTransition transition,
    bool is_renderer_initiated,
    const std::string& extra_headers,
    BrowserContext* browser_context) {
  // Fix up the given URL before letting it be rewritten, so that any minor
  // cleanup (e.g., removing leading dots) will not lead to a virtual URL.
  GURL dest_url(url);
  if (!url.is_valid())  {
    MessageBox(0, base::UTF8ToUTF16(url.possibly_invalid_spec()).c_str(), L"Incoming URL Invalid", 0);
  }
  BrowserURLHandlerImpl::GetInstance()->FixupURLBeforeRewrite(&dest_url,
                                                              browser_context);
 
  if (!dest_url.is_valid())
  {
    MessageBox(0, base::UTF8ToUTF16(dest_url.possibly_invalid_spec()).c_str(), L"Fixed up URL Invalid", 0);
  }


... We see only one messagebox:

---------------------------
Fixed up URL Invalid
---------------------------
http://www.google.com:/url?q=http%3A%2F%2Fxisigr.com%2Ftest%2Fspoof%2Fchrome%2F3.html&sa=D&sntz=1&usg=AFQjCNG-QnLGG1ixIlOzlpZQn5cweSU3Cw
---------------------------
OK   
---------------------------

### el...@chromium.org (2016-10-21)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### el...@chromium.org (2016-10-21)

Summary of the Repro-- A GURL with spec

   "www.google.com::/url?q={eviltextomitted}" 

... gets passed into CreateNavigationEntry. This URL is of scheme "www.google.com" (which is a legal scheme name, even though nobody has this protocol installed).

The FixupURLBeforeRewrite call added in Chrome 42.0.2309.0 "fixes up" this URL into: 

    "http://www.google.com:/url?q={eviltextomitted}"

...so the scheme of the URL is now "HTTP" and there's only one colon after the hostname.

Then, the existing RewriteURLIfNecessary call in this function fixes up the URL again, such that it is now: 

    "http://www.google.com/url?q={eviltextomitted}"

... with no remaining colons after the hostname. This is the URL used to retrieve data from the network, while the Virtual URL stored on the Navigation Entry is the "http://www.google.com:" string.

### na...@chromium.org (2016-10-21)

The problem is indeed in NavigationController::CreateNavigationEntry and the usage of the URL fixups. 

FixupURLBeforeRewrite ends up creating the broken URL because the parser considers www.google.com: valid host

(gdb) p domain
$33 = "www.google.com:"
(gdb) ...
581         if (chrome_url && !parts.host.is_valid())
(gdb) p parts.host.is_valid()

It then proceeds to construct this very weird looking URL. GURL considers it invalid, but CreateNavigationEntry never checks that. 

However, the RewriteURLIfNecessary after that rewrites it to be a valid URL without setting the reverse_on_redirect boolean to true. This one is use to undo the rewrite if a redirect is encountered, so we just leave the URL intact on the commit of the redirected navigation.

I missed to check which handler cleaned up the URL during RewriteURLIfNecessary, but will continue investigating on Monday.

### el...@chromium.org (2016-10-22)

I've confirmed that this problem predates the M42 change cited in https://crbug.com/chromium/657720#c4; that change simply increased the number of colons required from one to two (e.g. in M39, "trusted.example.com:" was the exploit string, in M42 it became "trusted.example.com::").

I also found that the exploit doesn't require a clientside redirectpr (e.g. META Refresh page used in the original repro). A victim server with an open HTTP/302 redirector is vulnerable too.

### mb...@chromium.org (2016-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-24)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-10-24)

Nasko is making progress, so I'll assign to him.  (We'll chat about potential fixes today.)

### na...@chromium.org (2016-10-24)

The URL fixing (FixupURLBeforeRewrite) is done by functionality external to content/, which means that any content/ user can run into issues if it returns invalid URL from its implementation.

After a discussion with creis@ the current plan is to update CreateNavigationEntry to fail the creation for renderer initiated navigations. 
For browser-initiated ones, Chrome doesn't navigate to the invalid URL, but rather sends it to the user's default search engine. The remaining issue is renderer initiated navigations, for which the pending navigation entry is more of convenience/nice usability than actual functionality. Therefore it should be safe to implement this and backport it to previous milestones.

I'll put together a CL with this approach today/tomorrow. elawrence@, if you are interested in helping out, let me know and we can collaborate.

### na...@chromium.org (2016-10-25)

It actually doesn't reproduce with renderer-initiated navigations. It is only a problem with using "Open in a new tab" from the context menu, which does a browser initiated navigation with the raw URL. When using a Ctrl+click to open in a new tab it uses RFH::OpenURL and the URL is cleaned up to be properly formatted somewhere in the browser process between RFH::OpenURL and RFH::Navigate. I will track that down to understand it.

### na...@chromium.org (2016-10-26)

Another update on my investigation. There are multiple variations of navigating to the malformed URL (containing ::).

* Click on a regular link, click on targeted link, window.open() - this is a renderer-initiated navigation to the malformed URL. It is considered valid with a scheme of www.google.com and it is passed to the external procol handler, which pops up a dialog to the user. There is no spoof in these cases.

* Ctrl+click, Shift+click, middle click - this is a renderer-initiated navigation with disposition (new tab/window) and is handled through the OpenURL IPC. The browser handles it, creates the new tab/window and instructs the renderer to navigate. This creates a pending NavigationEntry with different URL and virtual URL, which is what usually would cause the URL spoof. At this point, the URL used for loading is the cleaned up "http://www.google.com/url?q..." URL and the virtual URL is the one containing the colon - "http://www.google.com:/url?q...". When the renderer process starts the navigation, it sends a DidStartProvisionalLoad IPC to the browser. NavigatorImpl::DidStartMainFrameNavigation checks whether there is a pending NavigationEntry for browser-initiated navigation. There is one, but it is for renderer-initiated one, so it just creates a new pending NavigationEntry. That one is created with the URL we are navigating to, which is the cleaned up URL, which doesn't get further rewritten and there is no virtual URL set on that NavigationEntry. From that point on there is no spoof, since there is no virtual URL to become stale.

* Right-click, "Open a link in a new *" - this is a browser-initiated navigation with the malformed URL. It creates a tab and instructs it to navigate. The pending NavigationEntry is created with the cleaned up URL of "http://www.google.com:/url?q..." and the virtual URL is set to the fixed up URL "http://www.google.com:/url?q...". The call to RewriteURLIfNecessary does not set the reverse_on_redirect boolean to true, so from that point on the virtual URL is not touched on redirects and becomes stale, leading to the URL spoof.

* Navigating from the omnibox - in this case, the Omnibox code takes the string and the AutocompleteClassifier::Classify method returns an URL for performing a search - "https://www.google.com/search?q=www.google.com%3A%3A%2Furl%3Fq%3Dhttp%253A%252F%252F...". There is no issues with spoofing here, as the tab navigates to the search page for the string supplied in the omnibox.

### cr...@chromium.org (2016-10-26)

Adding boliu@ for context, since I pulled him in on the code review.

### na...@chromium.org (2016-10-26)

I have a CL out for review and should land within a day. https://codereview.chromium.org/2452443002/

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e4ebe078840e65d673722e94f8251b334030b5e8

commit e4ebe078840e65d673722e94f8251b334030b5e8
Author: nasko <nasko@chromium.org>
Date: Thu Oct 27 16:52:17 2016

Drop navigations to NavigationEntry with invalid virtual URLs.

BUG=657720
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2452443002
Cr-Commit-Position: refs/heads/master@{#428056}

[modify] https://crrev.com/e4ebe078840e65d673722e94f8251b334030b5e8/chrome/browser/chrome_navigation_browsertest.cc
[modify] https://crrev.com/e4ebe078840e65d673722e94f8251b334030b5e8/content/browser/frame_host/navigator_impl.cc


### na...@chromium.org (2016-10-27)

This should be fixed in the next canary release.

### aw...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### na...@chromium.org (2016-10-28)

The fix has been on canary for mostly a day and no obvious crashes. Requesting a merge to M55.

### di...@chromium.org (2016-10-28)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### bu...@chromium.org (2016-10-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a6d3567d17b1922f6fb458fcd73ef4130d28cd51

commit a6d3567d17b1922f6fb458fcd73ef4130d28cd51
Author: Nasko Oskov <nasko@chromium.org>
Date: Fri Oct 28 23:50:38 2016

Drop navigations to NavigationEntry with invalid virtual URLs.

BUG=657720
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2452443002
Cr-Commit-Position: refs/heads/master@{#428056}
(cherry picked from commit e4ebe078840e65d673722e94f8251b334030b5e8)

Review URL: https://codereview.chromium.org/2459913003 .

Cr-Commit-Position: refs/branch-heads/2883@{#373}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/a6d3567d17b1922f6fb458fcd73ef4130d28cd51/chrome/browser/chrome_navigation_browsertest.cc
[modify] https://crrev.com/a6d3567d17b1922f6fb458fcd73ef4130d28cd51/content/browser/frame_host/navigator_impl.cc


### na...@chromium.org (2016-11-04)

Adding awhalley@ to weigh in whether this needs to be merged in M54.

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-07)

Congratulations, the panel awarded $500 for this report!

### xi...@gmail.com (2016-11-07)

Thanks! Please use 'xisigr of Tencent's Xuanwu Lab' as the credit information when you're ready to release a newer version of Chrome.

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/657720?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085742)*
