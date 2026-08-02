# UAF in WebViewImpl::Minimize

| Field | Value |
|-------|-------|
| **Issue ID** | [492899974](https://issues.chromium.org/issues/492899974) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | pc...@google.com |
| **Created** | 2026-03-16 |
| **Bounty** | $11,000.00 |

## Description

### Summary

[WebViewImpl::PostDelayedRejectionForAWCPromise](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/exported/web_view_impl.cc;l=3312) posts a 5-second timeout with `Unretained(this)`, but [WebViewImpl::Close](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/exported/web_view_impl.cc;l=1184) destroys the object without canceling it. Closing the window before the timeout fires causes the UAF in `RejectAWCPromise`.

### Details

In [WebViewImpl::Minimize](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/exported/web_view_impl.cc;l=3165) and [WebViewImpl::PostDelayedRejectionForAWCPromise](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/exported/web_view_impl.cc;l=3312), the implementation stores callback state and posts a raw `this` callback:

```
void WebViewImpl::PostDelayedRejectionForAWCPromise(uint64_t id) {
  GetPage()
      ->GetAgentGroupScheduler()
      .DefaultTaskRunner()
      ->PostNonNestableDelayedTask(
          FROM_HERE,
          BindOnce(&WebViewImpl::RejectAWCPromise, Unretained(this), id),
          kWindowingControlsChangeTimeout);
}

```

In [WebViewImpl::Close](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/exported/web_view_impl.cc;l=1184), the object is destroyed without canceling that timeout:

```
void WebViewImpl::Close() {
  CHECK(page_);
  AllInstances().erase(this);
  CancelPagePopup();
  receiver_.reset();
  dev_tools_emulator_->Shutdown();
  page_->WillBeDestroyed();
  page_.Clear();

  if (web_view_client_)
    web_view_client_->OnDestruct();

  web_view_client_ = nullptr;

  for (auto& observer : observers_)
    observer.WebViewDestroyed();

  delete this;
}

```

The `PostDelayedRejectionForAWCPromise` assumes the object will still exist five seconds later, but `Close()` can tear down the page and `delete this` first, leading to the UAF. This is a fairly typical lifetime issue.

### Bisection

This issue is introduced by the commit <https://chromium-review.googlesource.com/c/chromium/src/+/7566969>, which introduce the `PostDelayedRejectionForAWCPromise` function for posting async tasks with timeout.

### Reproduction

Download the chrome in `https://storage.googleapis.com/chromium-browser-asan/mac-release-arm64/asan-mac-release-1598431.zip`

Reproducing this issue requires an PWA app installed, make sure your user-data-dir contains the installed app.

1. Serve the PWA app page for `awc-app.html`, `awc-app.webmanifest`, `awc-keepalive.html`, `awc-sw.js`, using `python3 -m http.server 8080`, visit the localhost:8080/awc-app.html to installed the PWA app and record its app id.
2. Run the extension (`background.js`, `content_script.js`, `manifest.json`) against the app id:

```
./chrome --user-data-dir=PROFILE_WITH_PWA --enable-features=DesktopPWAsAdditionalWindowingControls --app-id=YOUR_APP_ID --load-extension=/path/to/ext

```

You would observe the UAF shown in `asan.txt`.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 20.0 KB)
- [awc-app.html](attachments/awc-app.html) (text/html, 1.9 KB)
- [awc-app.webmanifest](attachments/awc-app.webmanifest) (application/octet-stream, 208 B)
- [awc-keepalive.html](attachments/awc-keepalive.html) (text/html, 187 B)
- [awc-sw.js](attachments/awc-sw.js) (text/javascript, 966 B)
- [background.js](attachments/background.js) (text/javascript, 3.9 KB)
- [content_script.js](attachments/content_script.js) (text/javascript, 1.3 KB)
- [manifest.json](attachments/manifest.json) (application/json, 566 B)

## Timeline

### dc...@chromium.org (2026-03-16)

I didn't manually reproduce this one due to the number of incoming bugs, but it seems quite trivially broken so triaging it as such.

### ch...@google.com (2026-03-17)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2026-03-17)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dr...@chromium.org (2026-03-23)

pchodur@ - this does look like a valid RBS, so please take a look as soon as possible. Stable RC cut for 147 is Tuesday March 24, so please get the fix landed on trunk, verified on canary, and request a merge to 147.

### he...@gmail.com (2026-03-23)

The possible fix is trivial, we can turn `Unretained(this)` into the weak pointer in the post task.

Thank you very much!

### pc...@google.com (2026-03-26)

Thanks for finding this! I just pushed [a CL](https://chromium-review.git.corp.google.com/c/chromium/src/+/7705593) to fix that.

drubery@ I think we might not need to merge it to 147. This whole functionality is behind a feature flag that is currently disabled by default.

### dr...@chromium.org (2026-03-27)

Ah, thanks! If it's behind a disabled-by-default feature flag, then we can update the labels.

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  main  

Author:  pchodur [pchodur@google.com](mailto:pchodur@google.com)  

Link:    <https://chromium-review.googlesource.com/7749106>

Move AWC callbacks to WebFrameWidgetImpl

---


Expand for full commit details
```
     
    This commit moves the logic for handling callbacks from WebViewImpl to 
    WebFrameWidgetImpl. The reason for this is that the WebFrameWidget is 
    more proper place for window-state related code, and to enable using 
    weak pointer with the callbacks in a following commit. 
     
    Bug: 492899974 
    Link: https://chromium-review.googlesource.com/id/I890cfc4488f9a05e8b13fd522ed4bcbd6a6a6964 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7749106 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Commit-Queue: Patryk Chodur <pchodur@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1619119}

```

---

Files:

- M `third_party/blink/renderer/core/exported/web_view_impl.cc`
- M `third_party/blink/renderer/core/exported/web_view_impl.h`
- M `third_party/blink/renderer/core/exported/web_view_test.cc`
- M `third_party/blink/renderer/core/frame/web_frame_widget_impl.cc`
- M `third_party/blink/renderer/core/frame/web_frame_widget_impl.h`
- M `third_party/blink/renderer/core/frame/web_frame_widget_test.cc`

---

Hash: [ddfab6d51cca0f550652b8529eac87d2eebe7320](https://chromiumdash.appspot.com/commit/ddfab6d51cca0f550652b8529eac87d2eebe7320)  

Date: Wed Apr 22 22:05:42 2026


---

### dx...@google.com (2026-04-22)

Project: chromium/src  

Branch:  main  

Author:  pchodur [pchodur@google.com](mailto:pchodur@google.com)  

Link:    <https://chromium-review.googlesource.com/7768392>

Fix UAF in WebViewImpl::Minimize

---


Expand for full commit details
```
     
    This commit fixes a discovered use after free in the WebViewImpl::Minimize, as 
    well as other Additional Windowing Controls functions. Now, the delayed timeout 
    task for rejecting promises has a weak pointer to MainFrameData instead of an 
    Unretained pointer. 
     
    Bug: 492899974 
    Link: https://chromium-review.googlesource.com/id/I4f4a9bdfba056647bbbeb057b0f8db576a6a6964 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7768392 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Commit-Queue: Patryk Chodur <pchodur@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1619138}

```

---

Files:

- M `third_party/blink/renderer/core/frame/web_frame_widget_impl.cc`
- M `third_party/blink/renderer/core/frame/web_frame_widget_impl.h`

---

Hash: [b1a2341027ca7a2b452ac9db53ad07e224076e01](https://chromiumdash.appspot.com/commit/b1a2341027ca7a2b452ac9db53ad07e224076e01)  

Date: Wed Apr 22 22:30:35 2026


---

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High Quality. Sandbox escape / Memory corruption / RCE in a non-sandboxed process.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492899974)*
