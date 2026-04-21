# Security: URL bar spoofing in Payments API

| Field | Value |
|-------|-------|
| **Issue ID** | [40054187](https://issues.chromium.org/issues/40054187) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Payments, Internals>Plugins>PDF, Platform>Apps>BrowserTag, UI>Browser>Navigation |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2020-12-16 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 89.0.4357.0 (Developer Build) (x86\_64)  

Operating System: MacOS

**REPRODUCTION CASE**

1. Go to <https://skilful-reserve-239412.appspot.com/static/apps/navigation-tester> and install "Max Payment Method"
2. Go to <https://maxlgu.github.io/pr/max-nonbasiccard/>
3. Click on "Busy" button.
4. In payment dialog try to change <http://www.google.com> to <https://lbstyle.github.io/chromeUrls.pdf> then click on "Go!" button.
5. Click on the link

Actual: Observe that <https://lbstyle.github.io> URL displayed but the content area still shows google.com contents.

## Attachments

- [screen.mov](attachments/screen.mov) (video/quicktime, 4.1 MB)
- [chromeUrls.pdf](attachments/chromeUrls.pdf) (application/pdf, 7.9 KB)

## Timeline

### [Deleted User] (2020-12-16)

[Empty comment from Monorail migration]

### ca...@chromium.org (2020-12-16)

Assigning medium severity since this requires quite a lengthy setup, and the fact that the spoof is only inside the payments window, not the omnibox.

[Monorail components: Blink>Payments]

### ca...@chromium.org (2020-12-16)

maxlg: Can you help further triage this? My guess is that opening the pdf from inside the payments window should not be possible. Thanks!

### ma...@chromium.org (2020-12-16)

Haven't got a chance to digged deeply yet. 

CC Rouslan.

### ma...@chromium.org (2020-12-16)

[Empty comment from Monorail migration]

### ro...@google.com (2020-12-16)

Agreed that opening a PDF in the payment handler window should be disabled as one mitigation.

Another mitigation is to figure out which method in WebContentsObserver and WebContentsDelegate the code needs to override to detect the URL change:

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.h;l=72-88;drc=da37bf24c7c0f86579b4bb18ad85c5a906dcf88f

At this point, the code updates he URL on DidStartNavigation() and DidFinishNavigation(). Which method gets triggered when a URL is opened from a PDF?

### ro...@google.com (2020-12-16)

[Empty comment from Monorail migration]

### ma...@chromium.org (2020-12-16)

I've tried to reproduced on Android - the PaymentHandler UI keeps loading the pdf page. It seems like the triggering is blocked on Android because PH UI doesn't allow downloading.

### ro...@google.com (2020-12-16)

The repro works on Mac.

### ro...@google.com (2020-12-16)

Clicking the PDF link does not invoke either DidStartNavigation() and DidFinishNavigation() method.

### [Deleted User] (2020-12-16)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2020-12-16)

Progress of investigation:
(1) Has the navigation from pdf to "google.com" triggered the header to update? Yes, payment_handler_web_flow_view_controller#CreateHeaderContentView() is triggered by TitleWasSet().
(2) When the header is triggered to update in (1) , is the origin correct? No, the origin comes from ```web_contents()->GetVisibleURL().GetOrigin()``` and it still points to ```https://lbstyle.github.io/chromeUrls.pdf```
(3) Is other URLs in web_contents() correct? No, I've checked WebContents.GetURL(), GetLastCommittedURL(),  GetVisibleURL(). They all point to ```https://lbstyle.github.io```

### ma...@chromium.org (2020-12-16)

CCed folks who might know about pdf and web-contents.

### ma...@chromium.org (2020-12-16)

[Empty comment from Monorail migration]

### cr...@chromium.org (2020-12-16)

PDFs on desktop load in a GuestView, which has an inner WebContents separate from the top-level WebContents.  Normally, though, navigations in a PDF get intercepted and targeted at the top-level WebContents, causing the entire inner WebContents to go away rather than navigate.  You can verify this by clicking the link in the PDF after visiting https://lbstyle.github.io/chromeUrls.pdf in a normal tab.

I'm curious why that isn't happening in the Payments WebContents.  Agreed that it should be fixed, and it may make sense to block PDFs entirely within the Payments WebContents to be safe on top of that.

[Monorail components: Platform>Apps>BrowserTag UI>Browser>Navigation]

### ro...@google.com (2020-12-16)

> Block PDFs entirely within the Payments WebContents.

Is there a known method to accomplish this?

### cr...@chromium.org (2020-12-16)

https://crbug.com/chromium/1159267#c17: Not that I'm aware of.  You'd probably have to write a NavigationThrottle that blocks the PDF extension, unless there's another way to disable MimeHandlerViewGuest that the GuestView folks know about.

### cr...@chromium.org (2020-12-16)

Note that blocking PDFs in Payments WebContents may be useful, but I suspect this bug would also apply to many other non-tab WebContents use cases, so it may not be sufficient.

I'm curious if the PDF extension's approach for handling navigations within the PDF needs to be hardened to not rely on the embedder.  For example, kmoon@ points to this code as one place that might be involved:
https://source.chromium.org/chromium/chromium/src/+/master:extensions/browser/guest_view/mime_handler_view/mime_handler_view_guest.cc;l=253;drc=df7b5e3cc781f29d798ff7dad2f74fbec88d292d

WebContents* MimeHandlerViewGuest::OpenURLFromTab(
    WebContents* source,
    const content::OpenURLParams& params) {
  auto* delegate = embedder_web_contents()->GetDelegate();
  return delegate ? delegate->OpenURLFromTab(embedder_web_contents(), params)
                  : nullptr;
}

If we're depending on the WebContentsDelegate and non-standard cases like Payments don't pass it to the outer WebContents but somehow let it happen in the inner WebContents, that would be a problem.  (I'm not entirely sure if that's what's happening here.)

I'll also point to navigator.js as another place that we've seen issues in the past:
https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/resources/pdf/navigator.js;drc=a9c450d1237c78cfcf93603697c9972f7adf5187;l=105
(For example, this came up in security bugs like https://crbug.com/chromium/851821 and https://crbug.com/chromium/852716.)

### cr...@chromium.org (2020-12-16)

Actually, MimeHandlerViewGuest::OpenURLFromTab doesn't seem to be involved.  In a normal tab, PDF navigations end up in the outer WebContents NavigationController via this stack:

#0  content::NavigationControllerImpl::NavigateWithoutEntry(content::NavigationController::LoadURLParams const&) (this=0x634368c16d0, params=...)
    at ../../content/browser/renderer_host/navigation_controller_impl.cc:3024
#1  0x00007f6f7ddf859c in content::NavigationControllerImpl::LoadURLWithParams(content::NavigationController::LoadURLParams const&) (this=0x634368c16d0, params=...)
    at ../../content/browser/renderer_host/navigation_controller_impl.cc:1006
#2  0x000055d50506e8d2 in extensions::TabsUpdateFunction::UpdateURL(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, int, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >*) (this=
    0x63437a078e0, url_string=..., tab_id=2, error=0x7ffdf8fcf788)
    at ../../chrome/browser/extensions/api/tabs/tabs_api.cc:1473
#3  0x000055d50506dcc5 in extensions::TabsUpdateFunction::Run() (this=0x63437a078e0)
    at ../../chrome/browser/extensions/api/tabs/tabs_api.cc:1363
#4  0x000055d500d40ab8 in ExtensionFunction::RunWithValidation() (this=0x63437a078e0)
    at ../../extensions/browser/extension_function.cc:448
#5  0x000055d500d4987a in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int, base::RepeatingCallback<void (ExtensionFunction::ResponseType, base::ListValue const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&)> const&) (this=0x634342b71c0, 
    params=..., render_frame_host=0x63435175020, render_process_id=24, callback=...)
    at ../../extensions/browser/extension_function_dispatcher.cc:383
#6  0x000055d500d48f2c in extensions::ExtensionFunctionDispatcher::Dispatch(ExtensionHostMsg_Request_Params const&, content::RenderFrameHost*, int)
    (this=0x634342b71c0, params=..., render_frame_host=0x63435175020, render_process_id=24)
    at ../../extensions/browser/extension_function_dispatcher.cc:257
#7  0x000055d500dc0605 in extensions::ExtensionWebContentsObserver::OnRequest(content::RenderFrameHost*, ExtensionHostMsg_Request_Params const&) (this=
    0x634342b71a0, render_frame_host=0x63435175020, params=...)
    at ../../extensions/browser/extension_web_contents_observer.cc:313


Sounds to me like a chrome.tabs.update call is being made from the PDF extension, probably via navigateInCurrentTab in navigator.js?

Maybe there's some reason that isn't working in the Payments WebContents.  I wonder if it can't find the tab via chrome.tabs.update?

### ma...@chromium.org (2020-12-16)

+1 that MimeHandlerViewGuest::OpenURLFromTab is not involved - my local run shows that it's not invoked. Also, "WebViewGuest::OpenURLFromTab" is not invoked as well.

### cr...@chromium.org (2020-12-16)

That navigator.js code does look suspicious:

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/resources/pdf/navigator.js;drc=a9c450d1237c78cfcf93603697c9972f7adf5187;l=43

  navigateInCurrentTab: function(url) {
    // When the PDFviewer is inside a browser tab, prefer the tabs API because
    // it can navigate from one file:// URL to another.
    if (chrome.tabs && this.tabId_ != -1)
      chrome.tabs.update(this.tabId_, {url: url});
    else
      window.location.href = url;
  },


If the conditional fails, then we hit the window.location.href = url line, which is a recipe for this URL spoof.  Probably dates back to https://codereview.chromium.org/2300243004.

I wonder if PDF folks can remove that else, first of all.  We probably never want to navigate the inner WebContents.  Whether chrome.tabs should work in the Payments case is a separate question, and it may be that we don't want it to.

[Monorail components: Internals>Plugins>PDF]

### km...@chromium.org (2020-12-16)

That sounds reasonable to me. The PDF viewer will always be embedded in the MHVG, so there shouldn't be a useful situation where this would occur. (Possibly for print preview, which doesn't use MHVG, but also doesn't need to support links, either...)

### km...@chromium.org (2020-12-16)

https://crbug.com/chromium/1032794 may also be similar (navigation in ChromeOS Quick View), which theoretically could be broken by this, but I think the behavior is also unwanted there. Should be sure to test that case, though.

### cr...@chromium.org (2020-12-16)

Agreed-- navigation of the inner WebContents is probably unwanted there as well.  kmoon@: Would you be a good owner for a change to that navigator.js file, or do you know who would be?

### km...@chromium.org (2020-12-17)

I don't have OWNERS on the JavaScript components of the PDF viewer, but rbpotter@ and dpapad@ do and work in that area a fair amount.

### ma...@chromium.org (2020-12-17)

creis@, I've been trying to add the navigation throttler. I am wondering how we can tell whether an outer WebContents is going to open a pdf? MineType doesn't seem to work as it is "text/html". Read the WIP CL[1] for more details.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/2595453/5

### km...@chromium.org (2020-12-17)

The decision as to whether or not a URL is opened as a PDF isn't made until the URL response headers (Content-Type) are received. (We don't know the true MIME type of the response until this point; actually, we even sniff a few bytes of the response body in some cases.) WillStartRequest() is too early in the navigation flow to detect if you're navigating to a PDF. (The request hasn't been issued yet.)

For example, see PDFIFrameNavigationThrottle and PluginResponseInterceptorURLLoaderThrottle.

### ma...@chromium.org (2020-12-17)

Ah, turns out I should use WillProcessResponse() instead. navigation_handle()->GetResponseHeaders()->GetMimeType(&mime_type)  returns the right type.

### km...@chromium.org (2020-12-17)

One more thing: The PDF viewer actually isn't the only extension that makes use of MimeHandlerView and its associated infrastructure. It's also used by the (formerly) QuickOffice extension (used to view Office file types), so it might be worthwhile to make sure a similar issue can't occur with that extension.

### ma...@chromium.org (2020-12-17)

Do you know how we can identify the page of QuickOffice type?

### km...@chromium.org (2020-12-17)

You probably want to check if the MIME type would be handled by an extension. This is the most "future proof" approach.

There's an allow list of extensions that are allowed to register MIME type handlers:
https://source.chromium.org/chromium/chromium/src/+/master:extensions/common/manifest_handlers/mime_types_handler.cc;l=29;drc=06805e7f64715706c1cf0dad0b04f481b0eda70c

I would take a step back and ask if this is the right approach, though. Maybe allow listing specific navigations is what you really want, rather than banning certain kinds of navigations? Or we can just fix the bug in the PDF viewer.

### km...@chromium.org (2020-12-17)

(Or we should find some other way to prevent these navigations within a MHVG in general.)

### ma...@chromium.org (2020-12-17)

https://crbug.com/chromium/1159267#c32, how can I get a list of these mine types?

### km...@chromium.org (2020-12-17)

These are defined by the mime_types field in the extension's manifest.json. There's no limit on which MIME types an extension can claim, so it's better not to hard-code a list of MIME types. I'd look at PluginResponseInterceptorURLLoaderThrottle for inspiration.

### ma...@chromium.org (2020-12-17)

[Empty comment from Monorail migration]

### ma...@chromium.org (2020-12-17)

WIP CL lives here: https://chromium-review.googlesource.com/c/chromium/src/+/2595453/18

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d648f4554e8474dd53462f05fae7bbf9caa1f1e6

commit d648f4554e8474dd53462f05fae7bbf9caa1f1e6
Author: Liquan (Max) Gu <maxlg@chromium.org>
Date: Fri Dec 18 05:28:44 2020

Disallow desktop Payment Handler UI from navigating to PDF

Context:
Opening a PDF in Payment Handler UI is a use case that's too rare to
support. This CL disallows this behaviours to avoid any PDF-related
risks.

Before this CL, the WebContents in desktop PaymentHandler UI could
navigate to a pdf file.

After the CL, the WebContents could not navigate to PDF file.

Bug: 1159267
Change-Id: Ic682bbf8a9c75e40658f1e17e423cf77b0847386
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2595453
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Liquan (Max) Gu <maxlg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#838419}

[modify] https://crrev.com/d648f4554e8474dd53462f05fae7bbf9caa1f1e6/chrome/browser/chrome_content_browser_client.cc
[add] https://crrev.com/d648f4554e8474dd53462f05fae7bbf9caa1f1e6/chrome/browser/payments/payment_handler_navigation_throttle.h
[modify] https://crrev.com/d648f4554e8474dd53462f05fae7bbf9caa1f1e6/components/payments/content/payment_handler_host.h
[modify] https://crrev.com/d648f4554e8474dd53462f05fae7bbf9caa1f1e6/components/payments/content/BUILD.gn
[modify] https://crrev.com/d648f4554e8474dd53462f05fae7bbf9caa1f1e6/chrome/browser/BUILD.gn
[add] https://crrev.com/d648f4554e8474dd53462f05fae7bbf9caa1f1e6/chrome/browser/payments/payment_handler_navigation_throttle.cc
[add] https://crrev.com/d648f4554e8474dd53462f05fae7bbf9caa1f1e6/components/payments/content/payments_userdata_key.cc
[add] https://crrev.com/d648f4554e8474dd53462f05fae7bbf9caa1f1e6/components/payments/content/payments_userdata_key.h
[modify] https://crrev.com/d648f4554e8474dd53462f05fae7bbf9caa1f1e6/chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc


### ma...@chromium.org (2020-12-18)

The mitigation has been landed, so no longer stable blocking.

### ro...@chromium.org (2020-12-18)

In what version of Chrome did the new PDF viewer launch?

### [Deleted User] (2020-12-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2020-12-18)

https://crbug.com/chromium/1159267#c40, if you meant which version of Chrome will carry the fix, the answer is the one after 89.0.4358.0. Do I understand your question correctly?

### ma...@chromium.org (2020-12-18)

Maybe I should put 'fixed' to calm the sheriffbot?

The vulnerability has been fixed. The remaining work is not on the critical path of this bug. The remaining work are:
(1) allow-list certain mine-types instead of disallowing pdf.
(2) block the QuickOffice request (which (1) would fix automatically).
(3) reject the pdf request on Android which doesn't open a pdf viewer right now.

### ch...@gmail.com (2020-12-18)

I tested this on Chromium build revision #838466 and I couldn’t navigate to PDF file. Thanks for the quick fix!

### [Deleted User] (2020-12-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-19)

[Empty comment from Monorail migration]

### cr...@chromium.org (2021-01-09)

https://crbug.com/chromium/1159267#c43: Thanks for the fix and listing the followup tasks.  Can you file bugs for anything remaining, so that they don't get forgotten?

It looks like the more general PDF navigator.js problem from https://crbug.com/chromium/1159267#c22 was also not yet resolved, which can affect other features.  Looks like mcnee@ is addressing that part in https://chromium-review.googlesource.com/c/chromium/src/+/2618602 for https://crbug.com/chromium/1158381.  (Thanks!)

### ma...@chromium.org (2021-01-11)

Thanks, I've just created crbug.com/1165367 for the remaining work.

### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4fd38d8662aa141fb586140088b85042f0f1089b

commit 4fd38d8662aa141fb586140088b85042f0f1089b
Author: Liquan (Max) Gu <maxlg@chromium.org>
Date: Fri Jan 15 02:14:51 2021

[Android][Payments] Throttle payment handler pages on mime-types

Motivation:
Now, payment handler supports pages of any mime type on Android. This
exposes payment handlers to the vulnerabilities of some less maintained
mime-types. In order to make payment handlers safer to use, this CL
limits the mime types of payment handlers on Android by allowlisting.

Changes:
* Moved the WebContents user data setting logic into
  markPaymentHandlerWebContents() to
  payment_handler_navigation_throttle.cc.
* Let both Android & desktop's payment handler coordinators use the
  method to annotate a payment handler web-contents.
* Moved the throttle from //chrome/browser to //components to make it
  more convenient to depend on.

Bug: 1165367, 1159267
Change-Id: Ibc75bad9b47b2586e4222c2556c4bf6fb6bd28cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2614918
Commit-Queue: Liquan (Max) Gu <maxlg@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#843892}

[rename] https://crrev.com/4fd38d8662aa141fb586140088b85042f0f1089b/components/payments/content/payment_handler_navigation_throttle.h
[modify] https://crrev.com/4fd38d8662aa141fb586140088b85042f0f1089b/chrome/browser/chrome_content_browser_client.cc
[modify] https://crrev.com/4fd38d8662aa141fb586140088b85042f0f1089b/components/payments/content/android/BUILD.gn
[add] https://crrev.com/4fd38d8662aa141fb586140088b85042f0f1089b/components/payments/content/android/payment_handler_navigation_throttle_android.cc
[modify] https://crrev.com/4fd38d8662aa141fb586140088b85042f0f1089b/components/payments/content/BUILD.gn
[modify] https://crrev.com/4fd38d8662aa141fb586140088b85042f0f1089b/chrome/browser/BUILD.gn
[modify] https://crrev.com/4fd38d8662aa141fb586140088b85042f0f1089b/chrome/android/java/src/org/chromium/chrome/browser/payments/handler/PaymentHandlerCoordinator.java
[rename] https://crrev.com/4fd38d8662aa141fb586140088b85042f0f1089b/components/payments/content/payment_handler_navigation_throttle.cc
[add] https://crrev.com/4fd38d8662aa141fb586140088b85042f0f1089b/components/payments/content/android/java/src/org/chromium/components/payments/PaymentHandlerNavigationThrottle.java
[modify] https://crrev.com/4fd38d8662aa141fb586140088b85042f0f1089b/chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a611cef536b8a7d9ba1aaa5e00b643e5f4d000ea

commit a611cef536b8a7d9ba1aaa5e00b643e5f4d000ea
Author: Liquan (Max) Gu <maxlg@chromium.org>
Date: Wed Jan 20 00:39:05 2021

[Android][Payments] Throttle payment handler pages on mime-types

Motivation:
Now, payment handler supports pages of any mime type on Android. This
exposes payment handlers to the vulnerabilities of some less maintained
mime-types. In order to make payment handlers safer to use, this CL
limits the mime types of payment handlers on Android by allowlisting.

Changes:
* Moved the WebContents user data setting logic into
  markPaymentHandlerWebContents() to
  payment_handler_navigation_throttle.cc.
* Let both Android & desktop's payment handler coordinators use the
  method to annotate a payment handler web-contents.
* Moved the throttle from //chrome/browser to //components to make it
  more convenient to depend on.

(cherry picked from commit 4fd38d8662aa141fb586140088b85042f0f1089b)

Bug: 1165367, 1159267
Change-Id: Ibc75bad9b47b2586e4222c2556c4bf6fb6bd28cd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2614918
Commit-Queue: Liquan (Max) Gu <maxlg@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#843892}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2633934
Reviewed-by: Danyao Wang <danyao@chromium.org>
Cr-Commit-Position: refs/branch-heads/4389@{#30}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[rename] https://crrev.com/a611cef536b8a7d9ba1aaa5e00b643e5f4d000ea/components/payments/content/payment_handler_navigation_throttle.h
[modify] https://crrev.com/a611cef536b8a7d9ba1aaa5e00b643e5f4d000ea/chrome/browser/chrome_content_browser_client.cc
[modify] https://crrev.com/a611cef536b8a7d9ba1aaa5e00b643e5f4d000ea/components/payments/content/android/BUILD.gn
[add] https://crrev.com/a611cef536b8a7d9ba1aaa5e00b643e5f4d000ea/components/payments/content/android/payment_handler_navigation_throttle_android.cc
[modify] https://crrev.com/a611cef536b8a7d9ba1aaa5e00b643e5f4d000ea/components/payments/content/BUILD.gn
[modify] https://crrev.com/a611cef536b8a7d9ba1aaa5e00b643e5f4d000ea/chrome/browser/BUILD.gn
[modify] https://crrev.com/a611cef536b8a7d9ba1aaa5e00b643e5f4d000ea/chrome/android/java/src/org/chromium/chrome/browser/payments/handler/PaymentHandlerCoordinator.java
[rename] https://crrev.com/a611cef536b8a7d9ba1aaa5e00b643e5f4d000ea/components/payments/content/payment_handler_navigation_throttle.cc
[add] https://crrev.com/a611cef536b8a7d9ba1aaa5e00b643e5f4d000ea/components/payments/content/android/java/src/org/chromium/components/payments/PaymentHandlerNavigationThrottle.java
[modify] https://crrev.com/a611cef536b8a7d9ba1aaa5e00b643e5f4d000ea/chrome/browser/ui/views/payments/payment_handler_web_flow_view_controller.cc


### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-21)

Hello, Khalil- the VRP Panel has decided to award you $500 for this report! Nice job! 

### [Deleted User] (2021-01-21)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1159267?no_tracker_redirect=1

[Multiple monorail components: Blink>Payments, Internals>Plugins>PDF, Platform>Apps>BrowserTag, UI>Browser>Navigation]
[Monorail blocking: crbug.com/chromium/1165367]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054187)*
