# Extensions without file URL access can use the `Page.navigate` CDP command to open `view-source:file:` URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [491766258](https://issues.chromium.org/issues/491766258) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools, Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2026-03-11 |
| **Bounty** | $2,000.00 |

## Description

## VULNERABILITY DETAILS

### Summary

A malicious extension can use the `chrome.debugger.sendCommand` API with the `Page.navigate` CDP command to navigate to `view-source:file:` URLs without the user enabling `Allow access to file URLs`. On Windows, this can be exploited using a UNC path to leak NTLM hashes to an attacker-controlled server.

### Attack Preconditions

The victim installs a malicious extension provided by the attacker, or a legitimate extension has a vulnerability that allows an attacker to control the URL passed to the `Page.navigate` CDP command.

### Impact Analysis

On Windows, the attacker can set up a server to capture NTLM hashes leaked via a `view-source:file:` URL using a UNC path, similar to bugs like [Issue 391114799](https://issues.chromium.org/issues/391114799) and [Issue 40060207](https://issues.chromium.org/issues/40060207). After acquiring the NTLM hashes, the attacker can perform offline cracking or use them with other techniques to gain access to Active Directory-based networks.

On macOS and Linux, the impact might be limited since I couldn't find a way to leak the page content of a `view-source:file:` URL without file URL access permissions.

### Bisect and Root Cause Analysis

Unlike [IsFileUrl](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/extension_tab_util.cc;l=140-143;drc=152d856fc77c3ba05f9fe3261dbc745c73b63333), which correctly checks for `view-source:` URLs and unwraps them to check the inner URL's scheme, [PageHandler::Navigate](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/protocol/page_handler.cc;l=878-882;drc=e2a6aae100f3db23e9540c326e910488473ec419) doesn't unwrap `view-source:` URL to check the inner URL's scheme. This allows `view-source:file:` URLs to be navigated to without file URL access permission:

```
  if (gurl.SchemeIsFile() && !may_read_local_files_) {
    callback->sendFailure(
        Response::ServerError("Navigating to local URL is not allowed"));
    return;
  }

```

The check for file URLs was introduced in this commit:

<https://source.chromium.org/chromium/chromium/src/+/925a1926434ee8e71b7adac47989df27e64b69d6>

## VERSION

Chrome Version: 145.0.7632.76 stable

Operating System: Linux, Mac, Windows

This vulnerability is also present in Chrome 147.0.7727.0 canary.

## REPRODUCTION CASE

1. Set up [Responder](https://github.com/lgandx/Responder) for catching NTLM hashes. The server can be set up with the installation guide provided in the repository or set up with Docker as follows (make sure to replace `<INTERFACE>` with the actual network interface you want to listen on):
   ```
   docker run --rm -ti --network host kalilinux/kali-rolling
   # Inside the container
   apt update && apt install -y responder
   responder -v -I <INTERFACE>
   
   ```
2. Create a directory structure like this with the attached file:
   ```
   poc
   ├── background.js
   └── manifest.json
   
   ```
3. Replace `<YOUR IP>` in `background.js` with the actual IP address of your machine where Responder is running.
4. Load the extension in Chrome by navigating to `chrome://extensions`, enabling `Developer mode`, and clicking `Load unpacked`. Select the `poc` directory.
5. Disable the `Allow access to file URLs` option for the extension in `chrome://extensions` to make sure the PoC is running without the permission.
6. After disabling the permission, the `background.js` script should reload and use `chrome.debugger.sendCommand` API with `Page.navigate` CDP command to navigate to the `view-source:file:////<YOUR IP>/leak` URL.
7. Even though the extension doesn't have the permission to access file URLs, `Page.navigate` should still successfully navigate the tab to the `view-source:file:` URL.
8. You should see the NTLM hashes being captured in the console output of Responder.

> Note: To simply prove that navigation to `view-source:file:` URLs works without file URL access, instead of using UNC path, you can update `TARGET_URL` in `background.js` to use something like `view-source:file:///etc/hosts` on Linux/macOS or `view-source:file:///C:/Windows/System32/drivers/etc/hosts` on Windows to see if the URL can be loaded without file URL access permissions. The reproduction steps above are specifically for demonstrating the NTLM hash leak on Windows.

## CREDIT INFORMATION

Reporter credit: lebr0nli of National Yang Ming Chiao Tung University, Dept. of CS, Security and Systems Lab.

## Attachments

- [background.js](attachments/background.js) (text/javascript, 845 B)
- [manifest.json](attachments/manifest.json) (application/json, 164 B)
- [background.js](attachments/background_74232067.js) (text/javascript, 913 B)
- [manifest.json](attachments/manifest_74232093.json) (application/json, 164 B)
- [receiver.js](attachments/receiver.js) (text/javascript, 2.9 KB)
- [background.js](attachments/background_74336653.js) (text/javascript, 2.2 KB)
- [server.py](attachments/server.py) (text/x-python, 1.7 KB)
- [receiver.html](attachments/receiver.html) (text/html, 895 B)
- [manifest.json](attachments/manifest_74336635.json) (application/json, 210 B)

## Timeline

### al...@gmail.com (2026-03-11)

Hi team,

I initially considered filing a separate report for the `Target.createTarget` CDP command, which is also vulnerable to this exact bypass. However, since the root cause, exploitation method, and impact are fundamentally the same, I decided it would be much more efficient to append the details here. This should help the engineering team implement a comprehensive fix and save the triage team from processing a duplicate report.

Similar to `PageHandler::Navigate`, [TargetHandler::CreateTarget](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/devtools/protocol/target_handler.cc;l=173-176;drc=89de898a64d26e49c8cbb154ac8de32fb60f6a9f) employs the same flawed code pattern that fails to unwrap the `view-source:` scheme to check the inner URL:

```
  if (!may_read_local_files_ && gurl.SchemeIsFile()) {
    return protocol::Response::ServerError(
        "Creating a target with a local URL is not allowed");
  }

```

The file URL check in `TargetHandler::CreateTarget` was originally introduced in this commit:
<https://source.chromium.org/chromium/chromium/src/+/e166400fa4c632c5150d75bf587e8a34285fb783>

I have attached a new PoC (`background.js` and `manifest.json`) that uses `Target.createTarget` instead of `Page.navigate` for this specific vector. The reproduction steps remain exactly the same as the original report.

Please let me know if you need any further information, or if you would actually prefer me to report this separately. If so, I'd be happy to file a new issue for it.

### ya...@google.com (2026-03-12)

Danil, looks like we need to blocklist view-source: urls from Page.navigate as well?

### ch...@google.com (2026-03-12)

Setting milestone because of s2 severity.

### ch...@google.com (2026-03-12)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dc...@chromium.org (2026-03-12)

@ya...@chromium.org @da...@chromium.org Not just `Page.navigate`; `Target.createTarget` as well as noted above by the reporter. I'm not sure if there are other entry points that check for file URLs, but if they do, they should cover this case as well.

### al...@gmail.com (2026-03-14)

Hi team,

> On macOS and Linux, the impact might be limited since I couldn't find a way to leak the page content of a view-source:file: URL without file URL access permissions.

Regarding my previous statement, I realized I was incorrect. This vulnerability is actually **exploitable across all platforms** by using with the `tabCapture` API, which means the attacker can read local files content, similar to bugs like [Issue 40054742](https://issues.chromium.org/issues/40054742).

> If I understand correctly, the `tabCapture` API's ability to capture `file:` URL content is intended behavior, as discussed in [comment #59 and comment #60 of Issue 40054742](https://issues.chromium.org/issues/40054742#comment60)?

The attachment is the PoC that will take a screenshot of `view-source:file:///etc/passwd`, and send the screenshot to the attacker's server (`attacker.test:1337`) without file URL access permissions.

**Steps to reproduce:**

1. Create a directory structure like this with the attached files:
   ```
   poc
   ├── background.js
   ├── manifest.json
   ├── receiver.html
   ├── receiver.js
   └── server.py
   
   ```
2. Update the `/etc/hosts` file to make `attacker.test` resolve to `127.0.0.1`.
3. Run `python3 server.py` to start the attacker's server, which will receive the exfiltrated content.
4. Load the extension in Chrome by navigating to `chrome://extensions`, enabling `Developer mode`, and clicking `Load unpacked`. Select the `poc` directory.
5. Ensure the `Allow access to file URLs` option is disabled for the extension in `chrome://extensions` to verify that the PoC runs without the permission.
6. Navigate to any standard web page (e.g., `https://www.example.com`) and click the extension icon to trigger the PoC.
7. You should see a new tab (`receiver.html`) being created, which will begin capturing the tab of the standard web page.
8. `background.js` will then navigate the captured tab (`example.com`) to `view-source:file:///etc/passwd` to load the contents of the `/etc/passwd` file.
9. `receiver.js` will capture a screenshot of the loaded page and send it to the attacker's server, even without file URL access.
10. You can visit `http://attacker.test:1337/` to view the exfiltrated content rendered via a `data:image/png;base64,...` URL.

> Note for Windows: You can change `view-source:file:///etc/passwd` in `background.js` to `view-source:file:///C:/Windows/System32/drivers/etc/hosts`.

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7657250>

Enforce file access restrictions for view-source:file:// URLs in DevTools.

---


Expand for full commit details
```
     
    This change modifies DevTools Protocol handlers for Target.createTarget and Page.navigate to correctly check for file access permissions when the provided URL uses the view-source: scheme with an inner file:// URL. Previously, the view-source: wrapper bypassed the file access checks. 
     
    Bug: 491766258 
    Change-Id: I84ae1358599ddc15523f87f66996dbbe91c65d02 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7657250 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1602263}

```

---

Files:

- M `chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc`
- M `chrome/browser/devtools/protocol/target_handler.cc`
- M `chrome/test/data/devtools/extensions/can_inspect_url/devtools.js`
- M `content/browser/devtools/protocol/devtools_protocol_browsertest.cc`
- M `content/browser/devtools/protocol/page_handler.cc`

---

Hash: [b6097c77bc161bfc3538b1695e80aa33b7b2d0b4](https://chromiumdash.appspot.com/commit/b6097c77bc161bfc3538b1695e80aa33b7b2d0b4)  

Date: Thu Mar 19 22:16:03 2026


---

### dx...@google.com (2026-03-20)

Project: chromium/src  

Branch:  main  

Author:  [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com) [luci-bisection@appspot.gserviceaccount.com](mailto:luci-bisection@appspot.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7686253>

Revert "Enforce file access restrictions for view-source:file:// URLs in DevTools."

---


Expand for full commit details
```
     
    This reverts commit b6097c77bc161bfc3538b1695e80aa33b7b2d0b4. 
     
    Reason for revert: 
    LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/5654982561890304 
     
    Sample build with failed test: https://ci.chromium.org/b/8686857324760706417 
    Affected test(s): 
    [://chrome/test\:browser_tests!gtest::DevToolsExtensionHostsPolicyTest#CantInspectBlockedHost](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:browser_tests%21gtest::DevToolsExtensionHostsPolicyTest%23CantInspectBlockedHost?q=VHash%3Ad6414a3317d1d770) 
    [://chrome/test\:browser_tests!gtest::DevToolsExtensionTest#CantInspectViewSourceComponentExtension](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:browser_tests%21gtest::DevToolsExtensionTest%23CantInspectViewSourceComponentExtension?q=VHash%3Ad6414a3317d1d770) 
     
    If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F5654982561890304&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F7657250&type=BUG 
     
    Original change's description: 
    > Enforce file access restrictions for view-source:file:// URLs in DevTools. 
    > 
    > This change modifies DevTools Protocol handlers for Target.createTarget and Page.navigate to correctly check for file access permissions when the provided URL uses the view-source: scheme with an inner file:// URL. Previously, the view-source: wrapper bypassed the file access checks. 
    > 
    > Bug: 491766258 
    > Change-Id: I84ae1358599ddc15523f87f66996dbbe91c65d02 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7657250 
    > Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    > Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    > Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1602263} 
    > 
     
    Bug: 491766258 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I9906e25c4ccaf25284fa92627ca7e52e9f7344be 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686253 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Finnur Thorarinsson <finnur@chromium.org> 
    Reviewed-by: Danil Somsikov <dsv@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1602609}

```

---

Files:

- M `chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc`
- M `chrome/browser/devtools/protocol/target_handler.cc`
- M `chrome/test/data/devtools/extensions/can_inspect_url/devtools.js`
- M `content/browser/devtools/protocol/devtools_protocol_browsertest.cc`
- M `content/browser/devtools/protocol/page_handler.cc`

---

Hash: [5ceb87315ed051a1a1b28d228a5bc3a0f43e4f63](https://chromiumdash.appspot.com/commit/5ceb87315ed051a1a1b28d228a5bc3a0f43e4f63)  

Date: Fri Mar 20 15:03:59 2026


---

### dx...@google.com (2026-03-26)

Project: devtools/devtools-frontend  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7704616>

Handle test output messages that arrive before the waiter is ready.

---


Expand for full commit details
```
     
    The waitForTestResultsAsMessage function now buffers test output messages received via top.postMessage in earlyTestResults if the waiter is not yet active. This prevents missing test results that are posted very quickly after the test starts. When waitForTestResultsAsMessage is called, it first checks the buffer before setting up a waiter. 
     
    Bug: 491766258 
    Change-Id: Ib34bb6e87ab1036e1c52ecbcd057050dc490fe7b 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/7704616 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org>

```

---

Files:

- M `front_end/Tests.js`

---

Hash: [5b4a14ceeeb42f9d14815501ffb066915889406b](https://chromiumdash.appspot.com/commit/5b4a14ceeeb42f9d14815501ffb066915889406b)  

Date: Thu Mar 26 19:56:19 2026


---

### dx...@google.com (2026-03-26)

Project: chromium/src  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7690211>

Reland "Enforce file access restrictions for view-source:file:// URLs in DevTools."

---


Expand for full commit details
```
     
    This reverts commit 5ceb87315ed051a1a1b28d228a5bc3a0f43e4f63. 
     
    Reason for revert: fix the tests 
     
    Original change's description: 
    > Revert "Enforce file access restrictions for view-source:file:// URLs in DevTools." 
    > 
    > This reverts commit b6097c77bc161bfc3538b1695e80aa33b7b2d0b4. 
    > 
    > Reason for revert: 
    > LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/5654982561890304 
    > 
    > Sample build with failed test: https://ci.chromium.org/b/8686857324760706417 
    > Affected test(s): 
    > [://chrome/test\:browser_tests!gtest::DevToolsExtensionHostsPolicyTest#CantInspectBlockedHost](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:browser_tests%21gtest::DevToolsExtensionHostsPolicyTest%23CantInspectBlockedHost?q=VHash%3Ad6414a3317d1d770) 
    > [://chrome/test\:browser_tests!gtest::DevToolsExtensionTest#CantInspectViewSourceComponentExtension](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:browser_tests%21gtest::DevToolsExtensionTest%23CantInspectViewSourceComponentExtension?q=VHash%3Ad6414a3317d1d770) 
    > 
    > If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F5654982561890304&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F7657250&type=BUG 
    > 
    > Original change's description: 
    > > Enforce file access restrictions for view-source:file:// URLs in DevTools. 
    > > 
    > > This change modifies DevTools Protocol handlers for Target.createTarget and Page.navigate to correctly check for file access permissions when the provided URL uses the view-source: scheme with an inner file:// URL. Previously, the view-source: wrapper bypassed the file access checks. 
    > > 
    > > Bug: 491766258 
    > > Change-Id: I84ae1358599ddc15523f87f66996dbbe91c65d02 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7657250 
    > > Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    > > Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    > > Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    > > Cr-Commit-Position: refs/heads/main@{#1602263} 
    > > 
    > 
    > Bug: 491766258 
    > No-Presubmit: true 
    > No-Tree-Checks: true 
    > No-Try: true 
    > Change-Id: I9906e25c4ccaf25284fa92627ca7e52e9f7344be 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686253 
    > Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    > Commit-Queue: Finnur Thorarinsson <finnur@chromium.org> 
    > Reviewed-by: Danil Somsikov <dsv@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1602609} 
     
    Bug: 491766258 
    Change-Id: Idc488a65c3bada92959036d9c8496be137b7a45b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7690211 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1605784}

```

---

Files:

- M `chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc`
- M `chrome/browser/devtools/protocol/target_handler.cc`
- M `chrome/test/data/devtools/extensions/can_inspect_url/devtools.js`
- M `content/browser/devtools/protocol/devtools_protocol_browsertest.cc`
- M `content/browser/devtools/protocol/page_handler.cc`

---

Hash: [c0168779d2d185e302faea1e0595269dcf8eb9a0](https://chromiumdash.appspot.com/commit/c0168779d2d185e302faea1e0595269dcf8eb9a0)  

Date: Thu Mar 26 21:22:30 2026


---

### dx...@google.com (2026-03-26)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7705431>

Roll DevTools Frontend from 1a9e4397442d to 5b4a14ceeeb4 (1 revision)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/1a9e4397442d..5b4a14ceeeb4 
     
    2026-03-26 dsv@chromium.org Handle test output messages that arrive before the waiter is ready. 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/devtools-frontend-chromium 
    Please CC chrome-devtools-staff+oncall-change@google.com,liviurau@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:491766258 
    Change-Id: I26f7e58a1588313d8b769a192e784f51380552c0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7705431 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1605804}

```

---

Files:

- M `DEPS`
- M `third_party/devtools-frontend/src`

---

Hash: [f882ae0c63c487197e9b2856438b4c5e90bf2a42](https://chromiumdash.appspot.com/commit/f882ae0c63c487197e9b2856438b4c5e90bf2a42)  

Date: Thu Mar 26 22:01:04 2026


---

### dx...@google.com (2026-03-27)

Project: chromium/src  

Branch:  main  

Author:  Joel Hockey [joelhockey@chromium.org](mailto:joelhockey@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7707712>

Revert "Reland "Enforce file access restrictions for view-source:file:// URLs in DevTools.""

---


Expand for full commit details
```
     
    This reverts commit c0168779d2d185e302faea1e0595269dcf8eb9a0. 
     
    Reason for revert: CantInspectNewTabPage failing on bots 
    https://ci.chromium.org/ui/p/chrome/builders/ci/android-desktop-16-x64-rel-emu-tests/4340/blamelist 
     
    Original change's description: 
    > Reland "Enforce file access restrictions for view-source:file:// URLs in DevTools." 
    > 
    > This reverts commit 5ceb87315ed051a1a1b28d228a5bc3a0f43e4f63. 
    > 
    > Reason for revert: fix the tests 
    > 
    > Original change's description: 
    > > Revert "Enforce file access restrictions for view-source:file:// URLs in DevTools." 
    > > 
    > > This reverts commit b6097c77bc161bfc3538b1695e80aa33b7b2d0b4. 
    > > 
    > > Reason for revert: 
    > > LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/5654982561890304 
    > > 
    > > Sample build with failed test: https://ci.chromium.org/b/8686857324760706417 
    > > Affected test(s): 
    > > [://chrome/test\:browser_tests!gtest::DevToolsExtensionHostsPolicyTest#CantInspectBlockedHost](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:browser_tests%21gtest::DevToolsExtensionHostsPolicyTest%23CantInspectBlockedHost?q=VHash%3Ad6414a3317d1d770) 
    > > [://chrome/test\:browser_tests!gtest::DevToolsExtensionTest#CantInspectViewSourceComponentExtension](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:browser_tests%21gtest::DevToolsExtensionTest%23CantInspectViewSourceComponentExtension?q=VHash%3Ad6414a3317d1d770) 
    > > 
    > > If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F5654982561890304&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F7657250&type=BUG 
    > > 
    > > Original change's description: 
    > > > Enforce file access restrictions for view-source:file:// URLs in DevTools. 
    > > > 
    > > > This change modifies DevTools Protocol handlers for Target.createTarget and Page.navigate to correctly check for file access permissions when the provided URL uses the view-source: scheme with an inner file:// URL. Previously, the view-source: wrapper bypassed the file access checks. 
    > > > 
    > > > Bug: 491766258 
    > > > Change-Id: I84ae1358599ddc15523f87f66996dbbe91c65d02 
    > > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7657250 
    > > > Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    > > > Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    > > > Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    > > > Cr-Commit-Position: refs/heads/main@{#1602263} 
    > > > 
    > > 
    > > Bug: 491766258 
    > > No-Presubmit: true 
    > > No-Tree-Checks: true 
    > > No-Try: true 
    > > Change-Id: I9906e25c4ccaf25284fa92627ca7e52e9f7344be 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686253 
    > > Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    > > Commit-Queue: Finnur Thorarinsson <finnur@chromium.org> 
    > > Reviewed-by: Danil Somsikov <dsv@chromium.org> 
    > > Cr-Commit-Position: refs/heads/main@{#1602609} 
    > 
    > Bug: 491766258 
    > Change-Id: Idc488a65c3bada92959036d9c8496be137b7a45b 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7690211 
    > Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    > Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    > Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1605784} 
     
    Bug: 491766258 
    Change-Id: I0e7b6f2ae2fae10631a8ff130c8323b6910bad70 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7707712 
    Auto-Submit: Joel Hockey <joelhockey@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Owners-Override: Joel Hockey <joelhockey@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1605986}

```

---

Files:

- M `chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc`
- M `chrome/browser/devtools/protocol/target_handler.cc`
- M `chrome/test/data/devtools/extensions/can_inspect_url/devtools.js`
- M `content/browser/devtools/protocol/devtools_protocol_browsertest.cc`
- M `content/browser/devtools/protocol/page_handler.cc`

---

Hash: [5817758bad9f3302fe38f32173e450b10b0de4a1](https://chromiumdash.appspot.com/commit/5817758bad9f3302fe38f32173e450b10b0de4a1)  

Date: Fri Mar 27 06:15:26 2026


---

### dx...@google.com (2026-03-31)

Project: chromium/src  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7705342>

Reland "Reland "Enforce file access restrictions for view-source:file:// URLs in DevTools.""

---


Expand for full commit details
```
     
    This reverts commit 5817758bad9f3302fe38f32173e450b10b0de4a1. 
     
    Reason for revert: Fixed the tests 
     
    Original change's description: 
    > Revert "Reland "Enforce file access restrictions for view-source:file:// URLs in DevTools."" 
    > 
    > This reverts commit c0168779d2d185e302faea1e0595269dcf8eb9a0. 
    > 
    > Reason for revert: CantInspectNewTabPage failing on bots 
    > https://ci.chromium.org/ui/p/chrome/builders/ci/android-desktop-16-x64-rel-emu-tests/4340/blamelist 
    > 
    > Original change's description: 
    > > Reland "Enforce file access restrictions for view-source:file:// URLs in DevTools." 
    > > 
    > > This reverts commit 5ceb87315ed051a1a1b28d228a5bc3a0f43e4f63. 
    > > 
    > > Reason for revert: fix the tests 
    > > 
    > > Original change's description: 
    > > > Revert "Enforce file access restrictions for view-source:file:// URLs in DevTools." 
    > > > 
    > > > This reverts commit b6097c77bc161bfc3538b1695e80aa33b7b2d0b4. 
    > > > 
    > > > Reason for revert: 
    > > > LUCI Bisection has identified this change as the cause of a test failure. See the analysis: https://ci.chromium.org/ui/p/chromium/bisection/test-analysis/b/5654982561890304 
    > > > 
    > > > Sample build with failed test: https://ci.chromium.org/b/8686857324760706417 
    > > > Affected test(s): 
    > > > [://chrome/test\:browser_tests!gtest::DevToolsExtensionHostsPolicyTest#CantInspectBlockedHost](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:browser_tests%21gtest::DevToolsExtensionHostsPolicyTest%23CantInspectBlockedHost?q=VHash%3Ad6414a3317d1d770) 
    > > > [://chrome/test\:browser_tests!gtest::DevToolsExtensionTest#CantInspectViewSourceComponentExtension](https://ci.chromium.org/ui/test/chromium/:%2F%2Fchrome%2Ftest%5C:browser_tests%21gtest::DevToolsExtensionTest%23CantInspectViewSourceComponentExtension?q=VHash%3Ad6414a3317d1d770) 
    > > > 
    > > > If this is a false positive, please report it at http://b.corp.google.com/createIssue?component=1199205&description=Analysis%3A+https%3A%2F%2Fci.chromium.org%2Fui%2Fp%2Fchromium%2Fbisection%2Ftest-analysis%2Fb%2F5654982561890304&format=PLAIN&priority=P3&title=Wrongly+blamed+https%3A%2F%2Fchromium-review.googlesource.com%2Fc%2Fchromium%2Fsrc%2F%2B%2F7657250&type=BUG 
    > > > 
    > > > Original change's description: 
    > > > > Enforce file access restrictions for view-source:file:// URLs in DevTools. 
    > > > > 
    > > > > This change modifies DevTools Protocol handlers for Target.createTarget and Page.navigate to correctly check for file access permissions when the provided URL uses the view-source: scheme with an inner file:// URL. Previously, the view-source: wrapper bypassed the file access checks. 
    > > > > 
    > > > > Bug: 491766258 
    > > > > Change-Id: I84ae1358599ddc15523f87f66996dbbe91c65d02 
    > > > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7657250 
    > > > > Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    > > > > Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    > > > > Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    > > > > Cr-Commit-Position: refs/heads/main@{#1602263} 
    > > > > 
    > > > 
    > > > Bug: 491766258 
    > > > No-Presubmit: true 
    > > > No-Tree-Checks: true 
    > > > No-Try: true 
    > > > Change-Id: I9906e25c4ccaf25284fa92627ca7e52e9f7344be 
    > > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7686253 
    > > > Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    > > > Commit-Queue: Finnur Thorarinsson <finnur@chromium.org> 
    > > > Reviewed-by: Danil Somsikov <dsv@chromium.org> 
    > > > Cr-Commit-Position: refs/heads/main@{#1602609} 
    > > 
    > > Bug: 491766258 
    > > Change-Id: Idc488a65c3bada92959036d9c8496be137b7a45b 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7690211 
    > > Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    > > Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    > > Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    > > Cr-Commit-Position: refs/heads/main@{#1605784} 
    > 
    > Bug: 491766258 
    > Change-Id: I0e7b6f2ae2fae10631a8ff130c8323b6910bad70 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7707712 
    > Auto-Submit: Joel Hockey <joelhockey@chromium.org> 
    > Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    > Owners-Override: Joel Hockey <joelhockey@chromium.org> 
    > Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    > Cr-Commit-Position: refs/heads/main@{#1605986} 
     
    Bug: 491766258 
    Change-Id: I219de975470abfcc6e03df3bee618069169bdc8b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7705342 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1607523}

```

---

Files:

- M `chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc`
- M `chrome/browser/devtools/protocol/target_handler.cc`
- M `chrome/test/data/devtools/extensions/can_inspect_url/devtools.js`
- M `content/browser/devtools/protocol/devtools_protocol_browsertest.cc`
- M `content/browser/devtools/protocol/page_handler.cc`

---

Hash: [1f5d394c07145c007178a7ae65205b572d79c22e](https://chromiumdash.appspot.com/commit/1f5d394c07145c007178a7ae65205b572d79c22e)  

Date: Tue Mar 31 00:59:52 2026


---

### ch...@google.com (2026-04-01)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-04-01)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dx...@google.com (2026-04-01)

Project: chromium/src  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7706236>

Enable DevToolsExtensionHostsPolicyTest.CantInspectBlockedHost and simplify devtools.js output.

---


Expand for full commit details
```
     
    The CantInspectBlockedHost test is no longer disabled on Linux/ChromeOS 
    builds, as the underlying issue has been resolved. The devtools.js 
    output function is simplified to send the test result message only once, 
    removing the unnecessary periodic sending. 
     
    Bug: 491766258 
    Change-Id: I21d5c9e988adeb09171edca5c0da340361114b8f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7706236 
    Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1608396}

```

---

Files:

- M `chrome/test/data/devtools/extensions/can_inspect_url/devtools.js`

---

Hash: [9708b3dbae9fb35774ddbde7d1207eec660d245e](https://chromiumdash.appspot.com/commit/9708b3dbae9fb35774ddbde7d1207eec660d245e)  

Date: Wed Apr 1 09:49:38 2026


---

### aj...@google.com (2026-05-20)

Low severity as the debugger permission is required.

### sp...@google.com (2026-05-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline || Lower Impact. Web platform privilege escalation


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491766258)*
