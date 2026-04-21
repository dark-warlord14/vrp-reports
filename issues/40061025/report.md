# Security: Bypass iframe sandbox on Android via intent:// URLs (possibly due to intent:// url popups not inheriting sandbox)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061025](https://issues.chromium.org/issues/40061025) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>IFrameSandbox, Mobile>Intents |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | mt...@chromium.org |
| **Created** | 2022-09-18 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to bypass certain iframe sandbox attributes on Android with a crafted HTML page containing intent:// URLs possibly due to intent:// url popups not inheriting sandbox.

There are 2 bugs at play here:

1: Usually, Chrome will block intent:// urls from opening inside iframes. However, it is possible to bypass this restriction if the sandbox allow-popups is present and the intent:// url is nested within a href in the data: url.

2: intent:// urls will trigger popups that do not inherit the sandbox. (In comparison, a regular popup will inherit the sandbox)

The attached PoC will demonstrate an sandbox without allow-downloads attribute bypass, there can be other types of bypasses which I am currently still investigating.

This bug should be fixed if 1 is fixed. (Meaning that an intent:// url in data: url should not be allowed to be opened.)

**VERSION**  

Chrome Version: [105.0.5195.136 Stable]  

Operating System: Android 11

**REPRODUCTION CASE**

1. Download attached files. Ensure that you change the ngrok URLs in poc.html to whatever you use.
2. Go to iframe.html, this puts poc.html in the sandbox.
3. Two links should be present, the intent-download as well as the control link.
4. From iframe.html, click on the control link, this shows the EXPECTED result, where downloads are blocked on popups.
5. From iframe.html, click on the intent-download link, this shows the ACTUAL result and the vulnerability itself, where downloads are incorrectly initiated, even without allow-downloads attribute on iframe sandbox indicating that the sandbox is not being inherited properly.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 264 B)
- [iframe.html](attachments/iframe.html) (text/plain, 63 B)
- [download.php](attachments/download.php) (text/plain, 91 B)
- [download.py](attachments/download.py) (text/plain, 375 B)
- [intent-sandbox-bypass.mp4](attachments/intent-sandbox-bypass.mp4) (video/mp4, 1.1 MB)

## Timeline

### [Deleted User] (2022-09-18)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-09-18)

Python version of download.php, be sure to change the URLs in poc.html to http://[YOUR_SERVER_URL]:8080 if you are using this.

### ha...@gmail.com (2022-09-18)

[Comment Deleted]

### ha...@gmail.com (2022-09-18)

[Comment Deleted]

### ha...@gmail.com (2022-09-18)

For both urls, be sure to change the URLs for the control setup and the intent-download setup*

1. Replace instances of [DOWNLOAD_URL+PORT] with your own url which you will be hosting download.py / download.php below

2. Additionally note the scheme parameter for the intent:// url, if you are using http, change the scheme parameter in the intent:// url to http, if you are using https, change the scheme parameter in the intent:// url to https

Format for control URL:

http://[DOWNLOAD_URL+PORT]

Format for intent-download URL:

data:text/html,<a href='intent://[DOWNLOAD_URL+PORT]%23Intent;scheme=http;package=com.android.chrome;end'>intent-download</a>


### ha...@gmail.com (2022-09-18)

Thought I should include a video as well.

### ha...@gmail.com (2022-09-18)

Actually on closer look, this is a allow-top-level navigation bypass, as intents do not open a new window but rather replace the address bar.

So the bug here is more that a combination of "data: uri, and the allow-popups attribute grants one the ability to perform a top-level navigation in a sandboxed iframe, causing a top level navigation which will escape the sandbox".  allow-popups alone shouldn't allow one to perform a top level navigation.



### ts...@chromium.org (2022-09-19)

Note: didn't setup environment to reproduce due to android/public server interaction. Foundin set based on reporter.
Arthur, I'm guessing you should be the best person to look at this, but do re-assign as appropriate.  Thanks!

[Monorail components: Blink>SecurityFeature>IFrameSandbox Mobile>Intents]

### [Deleted User] (2022-09-19)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-09-19)

Also found a similar issue (fixed in the past) here:
https://bugs.chromium.org/p/chromium/issues/detail?id=1196803

Maybe the people who fixed that can get added to this bug as well?

### ar...@chromium.org (2022-09-19)

Thanks for opening this! I am not sure to understand why this is a bug. I replied inline below. Could you please take a look?

> 1: Usually, Chrome will block intent:// urls from opening inside iframes. However, it is possible to bypass this restriction if the sandbox allow-popups is present and the intent:// url is nested within a href in the data: url.

We used not to do anything for intent: and more generally any external URL. Recently, in M103, I introduced blocking them in sandboxed iframe:
https://chromestatus.com/feature/5680742077038592
Exceptions are when using one of:
- allow-popups
- allow-top-navigation
- allow-top-navigation-with-user-activation
- allow-top-navigation-to-custom-protocols
which you did with "allow-popups". So I believe allowing opening the external application is working as specified.

We may want to "improve" over the current specified behavior, but we should propose and discuss a "potential solution". The webappsec is a good group for this: https://github.com/w3c/webappsec/issues
If you have any ideas about what Chrome could improve, within our outside the specification. Feel free to let me know here.

Web compatibility is going to be the main issue here. It is hard to change things without breaking legitimate users.

2: intent:// urls will trigger popups that do not inherit the sandbox. (In comparison, a regular popup will inherit the sandbox)

Yes, intent:// are external URLs. They are handled outside of Chrome. "sandbox" concept do not exist there. I acknowledge the intent ask Android to open Chrome, which is likely the same application here.

### [Deleted User] (2022-09-19)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-09-19)

Hi, thanks for the reply!

Generally, allow-popups (without escape-sandbox) is used when a user allows ads to open a new page on Chrome without escaping the sandbox. The issue here is that now a malicious ad can open a new popup or top-level navigation that can escape the sandbox on Android if allow-popups are enabled (see the allow-downloads bypass generated from the sandbox in the video above), it makes allow-popups-to-escape-sandbox redundant on Android.

It can be argued that intent is an external application, but when the intent is pointing to chrome and chrome will not treat the intent url as an external navigation, but rather navigate the top on the current tab instead which wouldn't count as an external application.

Perhaps there should be a subtle difference between allow-popups and allow-top-navigation regarding external urls (ie: allow-popups shouldn't be able to open intent urls pointing to the app itself or googlechrome:// (as this would result in a top navigation when opened in Chrome rather than a popup)

### ad...@google.com (2022-09-19)

(auto-cc on security bug)

### mt...@chromium.org (2022-09-20)

Yeah this is a bit of a thorny issue because we don't have a way to fall back to loading a URL in the iframe if the external navigation fails.

We only consider external protocols like intent:// for external navigation when navigating from an iframe, so if an iframe wanted to open youtube it would have to send an intent URL like 'intent://www.youtube.com/#Intent;scheme=https;end', which would fall back to opening in the browser.

What we probably have to do is plumb the sandbox attributes up to the Java layer and pass them through any intents we send so that if we receive the intent after an intent picker we know that it came from a sandboxed iframe and either block it or open a window with the same sandbox attributes applied...

### [Deleted User] (2022-09-20)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-20)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2022-09-22)

mthiesse@ I don't think its an issue with the self-intent not inheriting the sandbox as it is doing a top level navigation, but rather allow-popups allows one to do a top-level navigation by abusing self intents, therefore escaping the sandbox. Is it possible to block self intents in iframe sandboxes or even entirely? I did test intents with fallback URLs in an iframe sandbox and they were expectedly blocked (unless my tests went wrong)

### mt...@chromium.org (2022-09-22)

altimin@ had suggested applying the sandbox attributes to any new top level navigations resulting from a self-intent (those navigations shouldn't load in the iframe hosting tab), and thus not escaping the sandbox in Chrome.

Mostly a question for navigation folks, but do we need to make a distinction between a popup and a top level navigation in a new tab here on Android? The two look identical to users. Is a navigation from the subframe that doesn't have an opener somehow worse from a security perspective? Does that iframe hosting page see any difference here?

### ar...@chromium.org (2022-09-28)

Would it be possible when Android do not want to handle the intent: to turn it into a redirect toward the URL? This way, we maintain the original navigation code path and can apply consistently the same policies: sandbox, csp, COOP, COEP, referrer, ... We also keep the navigation inside the frame it belongs.

This is probably more "correct" and slightly more future-proof. Otherwise, I worry about this to be used to bypass every future security property we might want to add. Ideally we want to come back to this only once.

### mt...@chromium.org (2022-09-28)

> Would it be possible when Android do not want to handle the intent: to turn it into a redirect toward the URL?
As mentioned above, we don't have a way to fall back to loading a URL in the iframe if the external navigation fails.

This is a problem with how iframe navigations are hooked into the external navigation code. Maybe somebody on the navigation side would know how to turn this into a throttle that allows us to change the URL? Right now we're called through RunExternalProtocolDialog which doesn't give us enough control.

See https://source.chromium.org/chromium/chromium/src/+/main:components/navigation_interception/intercept_navigation_delegate.h;bpv=1;bpt=1;l=73?gsn=HandleExternalProtocolDialog&gs=kythe%3A%2F%2Fchromium.googlesource.com%2Fchromium%2Fsrc%3Flang%3Dc%252B%252B%3Fpath%3Dcomponents%2Fnavigation_interception%2Fintercept_navigation_delegate.h%23Vt9PUtnhoND3cBskThgENPEjh_lCndEwMFLpIiG_EJc


### ar...@google.com (2022-09-28)

> This is a problem with how iframe navigations are hooked into the external navigation code. Maybe somebody on the navigation side would know how to turn this into a throttle that allows us to change the URL? Right now we're called through RunExternalProtocolDialog which doesn't give us enough control.

I wouldn't recommend using a NavigationThrottle, because they are not meant to modify the navigation.
Fortunately, it seems RunExternalProtocolDialog is not using a NavigationThrottle. Content/ calls the embedder here:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/navigation_url_loader_impl.cc;l=709-717;drc=a432cd59d51281057ba2a2673ca645a9600bb927;bpv=1;bpt=1
```
      bool handled = GetContentClient()->browser()->HandleExternalProtocol(
          resource_request_->url, web_contents_getter_, frame_tree_node_id_,
          navigation_ui_data_.get(), request_info_->is_primary_main_frame,
          FrameTreeNode::GloballyFindByID(frame_tree_node_id_)
              ->IsInFencedFrameTree(),
          request_info_->sandbox_flags,
          static_cast<ui::PageTransition>(resource_request_->transition_type),
          resource_request_->has_user_gesture, initiating_origin,
          initiator_document_.AsRenderFrameHostIfValid(), &loader_factory);
```

It seems content/ ask the embedder to handle the request and provide a `loader_factory` to load data from. I guess the embedder need provide URLLoader that are redirecting toward the appropriate URL.

### mt...@chromium.org (2022-10-03)

Arthur, would you be willing to hook up the URLLoader? I can take care of HandleExternalProtocol returning a URL to redirect to, but it would probably be best of somebody from the navigation team takes care of hooking up the redirection as I have no idea what I'm doing there :).

### ar...@chromium.org (2022-10-05)

> Arthur, would you be willing to hook up the URLLoader?

I don't have the bandwidth and I believe I won't be effective modifying code outside of content/. If you can add some regression tests, and provide some code pointers where the URL can be retrieve, I think I would be able to add a fix on top of it.

I was thinking: The HandleExternalProtocol API have an output parameter `loader_factory`, I would fill it with an URL loader redirecting toward the URL you want. So the content/ embedder would write:
```
*loader_factor = base::MakeRefCounted<SingleRequestURLLoaderFactory>(
  base::BindOnce(RedirectToCallback, url));
```

and

```
void RedirectToCallback(
    GURL url,
    const network::ResourceRequest& /*resource_request*/,
    mojo::PendingReceiver<network::mojom::URLLoader> /*pending_receiver*/,
    mojo::PendingRemote<network::mojom::URLLoaderClient> pending_client) {

  auto response_head = network::mojom::URLResponseHead::New();
  response_head->encoded_data_length = 0;
  response_head->headers = base::MakeRefCounted<net::HttpResponseHeaders>(
      net::HttpUtil::AssembleRawHeaders(
          base::StringPrintf("HTTP/1.1 %s Found\r\n", url)));

  mojo::Remote<network::mojom::URLLoaderClient> client(
      std::move(pending_client));
  client_->OnReceiveRedirect(net::RedirectInfo::ComputeRedirectInfo(...),
                             std::move(response_head));
}
```

### [Deleted User] (2022-10-19)

arthursonzogni: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-31)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2022-10-31)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7120a08e5942251029642804b62b7388d6853cfe

commit 7120a08e5942251029642804b62b7388d6853cfe
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Fri Nov 25 19:04:56 2022

Refactor InterceptNavigationDelegate#handleSubframeExternalProtocol

InterceptNavigationDelegate#handleSubframeExternalProtocol needs a
separate return type from shouldIgnoreNavigation so that subframe
navigations can return a GURL to redirect to.

A followup change will cause the GURL to be returned in place of
clobbering the tab for subframe navigations, which will then be used to
redirect the subframe instead of clobbering the top level frame.

No functional changes intended. Some ContextualSearchManager tests
weren't written correctly and needed updating.

Bug: 1365100, 1316518
Change-Id: Ia5e2a09d97078780476a72cf2c510212fde0e99c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4053000
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Reviewed-by: Colin Blundell <blundell@chromium.org>
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1075824}

[modify] https://crrev.com/7120a08e5942251029642804b62b7388d6853cfe/content/public/android/java/src/org/chromium/content_public/browser/NavigationHandle.java
[modify] https://crrev.com/7120a08e5942251029642804b62b7388d6853cfe/chrome/android/java/src/org/chromium/chrome/browser/compositor/bottombar/OverlayContentDelegate.java
[modify] https://crrev.com/7120a08e5942251029642804b62b7388d6853cfe/chrome/android/java/src/org/chromium/chrome/browser/contextualsearch/ContextualSearchManager.java
[modify] https://crrev.com/7120a08e5942251029642804b62b7388d6853cfe/chrome/android/javatests/src/org/chromium/chrome/browser/contextualsearch/ContextualSearchInstrumentationBase.java
[modify] https://crrev.com/7120a08e5942251029642804b62b7388d6853cfe/components/navigation_interception/android/java/src/org/chromium/components/navigation_interception/InterceptNavigationDelegate.java
[modify] https://crrev.com/7120a08e5942251029642804b62b7388d6853cfe/chrome/android/java/src/org/chromium/chrome/browser/compositor/bottombar/contextualsearch/ContextualSearchPanel.java
[modify] https://crrev.com/7120a08e5942251029642804b62b7388d6853cfe/chrome/android/java/src/org/chromium/chrome/browser/compositor/bottombar/OverlayPanelContent.java
[modify] https://crrev.com/7120a08e5942251029642804b62b7388d6853cfe/chrome/android/javatests/src/org/chromium/chrome/browser/tab/InterceptNavigationDelegateTest.java
[modify] https://crrev.com/7120a08e5942251029642804b62b7388d6853cfe/chrome/android/javatests/src/org/chromium/chrome/browser/contextualsearch/ContextualSearchManagerTest.java
[modify] https://crrev.com/7120a08e5942251029642804b62b7388d6853cfe/components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateImpl.java


### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### mt...@chromium.org (2022-11-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1a49e4d5407c2b4125c9184dac0c3f28b1477b56

commit 1a49e4d5407c2b4125c9184dac0c3f28b1477b56
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Fri Dec 02 21:54:40 2022

Support redirecting frames for external protocols on Android

Some external protocol navigations in subframes can end up causing
navigations in the browser, from fallback URLs, incognito
dialogs, etc.

This change adds the c++ plumbing to support redirecting the frame
instead of clobbering the tab or opening a new tab. Followup changes
will add the Java plumbing to use this path rather than the current
tab clobbering path (and add more tests).

Bug: 1365100
Change-Id: I8e5d483d1aefdb3ccccdaaad27abd7d07883bfd8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4057867
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Auto-Submit: Michael Thiessen <mthiesse@chromium.org>
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Clark DuVall <cduvall@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1078783}

[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/web_package/prefetched_signed_exchange_cache.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/services/network/public/cpp/BUILD.gn
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/web_package/web_bundle_interceptor_for_trustable_file.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/components/navigation_interception/DEPS
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/service_worker/service_worker_controllee_request_handler.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/chrome/browser/external_protocol/external_protocol_handler.h
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/service_worker/service_worker_controllee_request_handler.h
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/components/navigation_interception/intercept_navigation_delegate.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/web_package/web_bundle_interceptor_for_file.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/chrome/browser/external_protocol/external_protocol_handler_unittest.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/chrome/browser/chrome_content_browser_client.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/web_package/web_bundle_interceptor_for_history_navigation_with_existing_reader.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/web_package/signed_exchange_request_handler.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/BUILD.gn
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/components/navigation_interception/intercept_navigation_delegate.h
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/worker_host/worker_script_loader.h
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/chrome/browser/external_protocol/external_protocol_handler.cc
[rename] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/services/network/public/cpp/single_request_url_loader_factory.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/chrome/android/javatests/src/org/chromium/chrome/browser/tab/InterceptNavigationDelegateTest.java
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/service_worker/service_worker_main_resource_loader_interceptor.h
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/preloading/prefetch/prefetch_url_loader_interceptor.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/web_package/web_bundle_interceptor_for_network.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/service_worker/service_worker_fetch_dispatcher.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/loader/navigation_url_loader_impl.h
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/service_worker/service_worker_main_resource_loader_unittest.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/loader/navigation_url_loader_impl_unittest.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/web_package/signed_exchange_cert_fetcher.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/loader/navigation_url_loader_impl.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/chrome/test/data/navigation_interception/iframe_with_external_navigation.html
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/public/browser/content_browser_client.h
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/web_package/web_bundle_interceptor_for_history_navigation_from_file_or_from_trustable_file.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/web_package/web_bundle_interceptor_for_history_navigation_from_network.cc
[rename] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/services/network/public/cpp/single_request_url_loader_factory.h
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/web_package/web_bundle_interceptor_for_tracked_navigation_from_trustable_file_or_from_network.cc
[modify] https://crrev.com/1a49e4d5407c2b4125c9184dac0c3f28b1477b56/content/browser/web_package/web_bundle_interceptor_for_tracked_navigation_from_file.cc


### ha...@gmail.com (2022-12-31)

Looking back at this report, I was wrong about my assumption that Chrome will not open the intent from an iframe, it turns out it does (not sure what happened in testing, I think I may have forgotten the "end" portion for the intent URL...

I have here a test site which shows the different ways I know of an intent that can cause a top-level navigation (It is a top-level navigation because the it is redirecting a new tab to the URL in an allow-popups only sandbox, it may be useful in testing the fix --

https://different-heavenly-healer.glitch.me/intent-sandbox-tests.html 

If you test, only (1) fallback urls respect the sandbox. Both (2) self-intents and (3) self-intent through the picker do not. 



### ha...@gmail.com (2022-12-31)

^ Correction for above -- It is a top-level navigation because the it is redirecting the *current* tab to the URL specified in the intent 

### gi...@appspot.gserviceaccount.com (2023-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5174b2669233382244250f7f1e1352303dbcb2c0

commit 5174b2669233382244250f7f1e1352303dbcb2c0
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Fri Jan 13 20:57:44 2023

Refactor ExternalNaviagation Tab Clobbering into InterceptNavigationImpl

No functional changes (outside of an edge cases where we forgot to call
the async action callback and missed clearing history for a clobbered
tab in the case of a link to another browser).

This change moves the tab clobbering logic into
InterceptNavigationDelegateImpl, and also makes the async action
callback mandatory, so it can't be mistakenly missed in the future.
This will allow us to implement fallback URL support for subframes.

Bug: 1365100
Change-Id: I79ddb3f1cc2cbb71a160b24f366023918bcf1279
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4159610
Reviewed-by: Colin Blundell <blundell@chromium.org>
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1092598}

[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/base/test/android/javatests/src/org/chromium/base/test/BaseJUnit4ClassRunner.java
[add] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/base/android/java/src/org/chromium/base/RequiredCallback.java
[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/chrome/android/java/src/org/chromium/chrome/browser/tab/InterceptNavigationDelegateClientImpl.java
[add] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/base/test/android/javatests/src/org/chromium/base/test/UnitTestLifetimeAssertRule.java
[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/weblayer/browser/java/org/chromium/weblayer_private/ExternalNavigationDelegateImpl.java
[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateClient.java
[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationDelegate.java
[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/chrome/android/java/src/org/chromium/chrome/browser/externalnav/ExternalNavigationDelegateImpl.java
[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java
[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationParams.java
[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/weblayer/browser/java/org/chromium/weblayer_private/InterceptNavigationDelegateClientImpl.java
[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java
[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/base/BUILD.gn
[modify] https://crrev.com/5174b2669233382244250f7f1e1352303dbcb2c0/components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateImpl.java


### gi...@appspot.gserviceaccount.com (2023-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9655c8b26d7111ca26d6d03122861ddcc891df17

commit 9655c8b26d7111ca26d6d03122861ddcc891df17
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Fri Jan 13 21:06:33 2023

Support fallback URLs in subframes

If a subframe external navigation fails and a fallback URL is used, that
fallback URL should redirect the frame that performed the navigation.

A followup change will support async actions using fallback URLs as
well.

Functionality changes are flag-guarded in case things unexpectedly
break.

Bug: 1365100
Change-Id: Id1b6120c51a0961fe524bff671c791ff3ea2c498
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4068379
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1092610}

[modify] https://crrev.com/9655c8b26d7111ca26d6d03122861ddcc891df17/chrome/android/java/src/org/chromium/chrome/browser/tab/InterceptNavigationDelegateClientImpl.java
[modify] https://crrev.com/9655c8b26d7111ca26d6d03122861ddcc891df17/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalIntentsFeatures.java
[modify] https://crrev.com/9655c8b26d7111ca26d6d03122861ddcc891df17/components/external_intents/android/external_intents_features.h
[modify] https://crrev.com/9655c8b26d7111ca26d6d03122861ddcc891df17/chrome/android/javatests/src/org/chromium/chrome/browser/tab/InterceptNavigationDelegateTest.java
[modify] https://crrev.com/9655c8b26d7111ca26d6d03122861ddcc891df17/components/external_intents/android/external_intents_features.cc
[modify] https://crrev.com/9655c8b26d7111ca26d6d03122861ddcc891df17/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java
[modify] https://crrev.com/9655c8b26d7111ca26d6d03122861ddcc891df17/chrome/android/java/src/org/chromium/chrome/browser/tab/InterceptNavigationDelegateTabHelper.java
[modify] https://crrev.com/9655c8b26d7111ca26d6d03122861ddcc891df17/components/external_intents/android/java/src/org/chromium/components/external_intents/InterceptNavigationDelegateImpl.java


### gi...@appspot.gserviceaccount.com (2023-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/29b2b78e9a513fd68d5b9f74033be0222135bc7f

commit 29b2b78e9a513fd68d5b9f74033be0222135bc7f
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Thu Jan 26 03:31:25 2023

Load subfame Intents to Chrome in the subframe

If a subframe navigates to an external protocol (like intent:) that
Chrome can handle, and that intent doesn't resolve to another Activity,
we should just handle that URL by loading it in the subframe to
maintain sandbox attributes.

Some tests were abusing the fact that subframes could previously send
intents to Chrome, so I modified the test code to return a fake
ResolveInfo for the Settings activity (so that the Message code can
still find an app to draw an icon for).

Bug: 1365100
Change-Id: I7772d04bf7375a867fd639bbec796142fa43f771
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4174394
Reviewed-by: Yaron Friedman <yfriedman@chromium.org>
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1097223}

[modify] https://crrev.com/29b2b78e9a513fd68d5b9f74033be0222135bc7f/components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java
[modify] https://crrev.com/29b2b78e9a513fd68d5b9f74033be0222135bc7f/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalIntentsFeatures.java
[modify] https://crrev.com/29b2b78e9a513fd68d5b9f74033be0222135bc7f/components/external_intents/android/external_intents_features.h
[modify] https://crrev.com/29b2b78e9a513fd68d5b9f74033be0222135bc7f/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
[modify] https://crrev.com/29b2b78e9a513fd68d5b9f74033be0222135bc7f/components/external_intents/android/external_intents_features.cc
[add] https://crrev.com/29b2b78e9a513fd68d5b9f74033be0222135bc7f/chrome/test/data/android/url_overriding/navigation_to_self_with_fallback_parent.html
[modify] https://crrev.com/29b2b78e9a513fd68d5b9f74033be0222135bc7f/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java
[add] https://crrev.com/29b2b78e9a513fd68d5b9f74033be0222135bc7f/chrome/test/data/android/url_overriding/navigation_to_self_with_fallback.html


### mt...@chromium.org (2023-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-03)

Congratulations, Axel! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@chromium.org (2023-02-03)

The first two commits landed on 110, and the following three on 111, since some of latest commits involve security relevant work, especially the latest fix (29b2b78e9a513fd68d5b9f74033be0222135bc7f) I'm not going to include/consider this as fixed in the first release of M110 shipping on Tuesday. 
This should be included fixed in M111 or we can discuss backmerging some or all of the latest commits to M110 to be included in M110/Stable respin in a little over two weeks. 

### mt...@chromium.org (2023-02-03)

None of the security-relevant changes landed in 110, only the final change actually makes a difference security-wise. I don't think we should try to merge this to 110.

### am...@google.com (2023-02-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1365100?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>IFrameSandbox, Mobile>Intents]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061025)*
