# UAF in JsCommunication, leading to RCE

| Field | Value |
|-------|-------|
| **Issue ID** | [481920229](https://issues.chromium.org/issues/481920229) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>WebView |
| **Platforms** | Android |
| **Chrome Version** | 144.0.0.0 |
| **Reporter** | po...@gmail.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2026-02-05 |
| **Bounty** | $7,000.00 |

## Description

# Steps to reproduce the problem

Tested on Pixel 9 Pro, Chromium version 144.0.7559.109.

1. Build `app.zip` and Install
2. `python -m http.server`
3. Visit `index.html`
4. UAF and Crash

# Problem Description

`JsCommunication` is a `content::RenderFrameObserver`, which is destructed along with the destruction of the `RenderFrameImpl` [1].
On iOS and Android platforms, application developers can use interfaces (such as [`addDocumentStartJavaScript`](https://developer.android.com/reference/androidx/webkit/WebViewCompat#addDocumentStartJavaScript(android.webkit.WebView,java.lang.String,java.util.Set%3Cjava.lang.String%3E))) to inject JavaScript code that runs at `DocumentEnd` or `DocumentStart`. JavaScript injected through this interface also runs in iframes. When the JavaScript executes, the scripts in the vector are processed one by one in a for-loop[2],[3].

```
void JsCommunication::OnDestruct() {
  delete this;              // [1]
}

void JsCommunication::RunScripts(mojom::DocumentInjectionTime injection_time) {
  url::Origin frame_origin =
      url::Origin(render_frame()->GetWebFrame()->GetSecurityOrigin());
  for (const auto& script : scripts_) {                  // [2]
    if (!script->origin_matcher.Matches(frame_origin)) {
      continue;
    }
    if (script->injection_time == injection_time) {
      if (script->js_world == content::ISOLATED_WORLD_ID_GLOBAL) {
        render_frame()->GetWebFrame()->ExecuteScript(
            blink::WebScriptSource(script->script));
      } else {
        render_frame()->GetWebFrame()->ExecuteScriptInIsolatedWorld(             // [3]
            script->js_world, blink::WebScriptSource(script->script),
            blink::BackForwardCacheAware::kAllow);
      }
    }
  }
}

```

The injected JavaScript can easily be redirected to code controlled by an attacker, for example, through getter, setter, or redefining functions in the prototype. An attacker can then remove the iframe, causing the `RenderFrameImpl` to be destroyed, which in turn destroys the `JsCommunication` object. When the next loop attempts to execute JavaScript, a UAF occurs, which is not protected by miraclePtr
Although triggering this UAF requires certain preconditions, in practice, many browsers (such as the Pawxy browser) utilize this interface, and it is also widely used by third-party libraries (e.g., react-native-webview).

1. `app.zip` is a simple WebView-based browser that injects two JavaScript codes via the `addDocumentStartJavaScript` interface.

```
    private void injectStartUpScripts() {
        if (WebViewFeature.isFeatureSupported(WebViewFeature.DOCUMENT_START_SCRIPT)) {
            Set<String> allowedOriginRules = Collections.singleton("*");
            try {
                WebViewCompat.addDocumentStartJavaScript(
                        webView,
                        "console.log(`${new Number(1.1)}`);",
                        allowedOriginRules
                );
//                WebViewCompat.addDocumentStartJavaScript(
//                        webView,
//                        "console.log(global_value)",
//                        allowedOriginRules
//                );
                WebViewCompat.addDocumentStartJavaScript(
                        webView,
                        "console.log('Second Script Injected');",
                        allowedOriginRules
                );
            } catch (Exception e) {
                Log.e(TAG, "addDocumentStartJavaScript failed");
            }
        } else {
            Toast.makeText(this, "addDocumentStartJavaScript not supported", Toast.LENGTH_SHORT).show();
        }
    }

```

2. Using this browser to visit the attacker’s webpage.
3. The attacker’s webpage redefines `Number.prototype.toString` inside an iframe.

```
node.contentWindow.Number.prototype.toString = function () {
  node.remove();
};

```

2. The first injected JavaScript executes and triggers the attacker’s code, which removes the iframe, ultimately leading to the destruction of `JsCommunication`.
3. In the next iteration of the loop, a UAF occurs.

# Summary

UAF in JsCommunication, leading to RCE

# Custom Questions

#### Reporter credit:

Am4deu$

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [8df049fc-f7d5-4f0f-94b8-76e914f9b6f9.dmp](attachments/8df049fc-f7d5-4f0f-94b8-76e914f9b6f9.dmp) (application/octet-stream, 158.5 KB)
- [app.zip](attachments/app.zip) (application/zip, 78.6 KB)
- [js_communication_poc.zip](attachments/js_communication_poc.zip) (application/zip, 1.8 KB)

## Timeline

### xi...@chromium.org (2026-02-05)

Thanks for the report. We are unable to reproduce the report based on the information provided. Can you please provide additional information (such as specific conditions needed to reproduce, such as GN arguments or required command line flags) or clarified reproduction steps? Without those, we may not be able to perform validation or root cause of this issue in a timely manner and may greatly increase the time to resolution and fix.

### po...@gmail.com (2026-02-06)

1. Build an APK using app.zip with Android Studio
2. Install that APK on Pixel
3. `cd js_communication_poc` and `python -m http.server`
4. Open the APP
5. Change the URL in the input box to the address where you have deployed your HTTP server, for example, http://192.168.3.123:8000
6. Click the button in the APP to visit this webpage
7. Renderer Process Crash
No additional command line flags are needed, no special GN arguments. The latest libmonochrome_64.so on pixel can trigger this crash.

### pe...@google.com (2026-02-06)

Thank you for providing more feedback. Adding the requester to the CC list.

### ts...@google.com (2026-02-06)

In particular, you'll need to provide steps for reproducing this in a shipping version of Chrome, rather than in some customized browser. Otherwise we can't take any action and will need to close this report.

### po...@gmail.com (2026-02-09)

This vulnerability affects Android Webview rather than Chrome.

### pe...@google.com (2026-02-09)

Thank you for providing more feedback. Adding the requester to the CC list.

### ts...@google.com (2026-02-11)

So a deliberately malicious browser app can embed a WebView and then execute code in the renderer. 
The question then becomes what does this allow an attacker to do that a malicious app can not on its own?
In particular, accessing memory directly may have a range of consequences, so we can treat this as a vulnerability. 


### ts...@google.com (2026-02-11)

Assigning per android_webview/OWNERS.

### el...@chromium.org (2026-02-11)

Going to call this FoundIn-144 based on the report, also stripping the iOS tag because we don't use Android WebView there.

### ch...@google.com (2026-02-12)

Setting milestone because of s2 severity.

### dx...@google.com (2026-02-12)

Project: chromium/src  

Branch:  main  

Author:  Dave Tapuska [dtapuska@chromium.org](mailto:dtapuska@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7567944>

[webview] Fix an issue around lifecycle of WebLocalFrame

---


Expand for full commit details
```
     
    Ensure that we monitor destruction of the JsCommunication object. 
     
    Bug: 481920229 
    Change-Id: Ibbc6eacf0cb44fc737b0228c5d231d6fddf0caea 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7567944 
    Commit-Queue: Dave Tapuska <dtapuska@chromium.org> 
    Reviewed-by: Bo Liu <boliu@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1584064}

```

---

Files:

- M `components/js_injection/renderer/js_communication.cc`
- M `components/js_injection/renderer/js_communication.h`

---

Hash: [34de88b274c41f245c28b123e03de9bc03e99163](https://chromiumdash.appspot.com/commit/34de88b274c41f245c28b123e03de9bc03e99163)  

Date: Thu Feb 12 17:47:21 2026


---

### po...@gmail.com (2026-02-13)

re #8. One attack scenario I can think of is that on Android, a user accesses a malicious website through a third-party browser, which is built using WebView and utilizes `addDocumentStartJavaScript` interface. The malicious website can achieve arbitrary code execution in the rendering process through this vulnerabilities. (We found that many third-party browsers use this interface to inject JS).

### ch...@google.com (2026-02-13)

Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1584064) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-02-13)

**Merge approved:** your change passed merge requirements and is auto-approved for M146. Please go ahead and merge the CL to branch 7680 (refs/branch-heads/7680) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dx...@google.com (2026-02-13)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Dave Tapuska [dtapuska@chromium.org](mailto:dtapuska@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7576314>

[M146] [webview] Fix an issue around lifecycle of WebLocalFrame

---


Expand for full commit details
```
     
    Ensure that we monitor destruction of the JsCommunication object. 
     
    (cherry picked from commit 34de88b274c41f245c28b123e03de9bc03e99163) 
     
    Bug: 481920229 
    Change-Id: Ibbc6eacf0cb44fc737b0228c5d231d6fddf0caea 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7567944 
    Commit-Queue: Dave Tapuska <dtapuska@chromium.org> 
    Reviewed-by: Bo Liu <boliu@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1584064} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7576314 
    Cr-Commit-Position: refs/branch-heads/7680@{#234} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `components/js_injection/renderer/js_communication.cc`
- M `components/js_injection/renderer/js_communication.h`

---

Hash: [626f0a125a55d1f69145210182bec4a79bfcee23](https://chromiumdash.appspot.com/commit/626f0a125a55d1f69145210182bec4a79bfcee23)  

Date: Fri Feb 13 21:23:35 2026


---

### ch...@google.com (2026-02-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Baseline. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline. Renderer RCE / memory corruption in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/481920229)*
